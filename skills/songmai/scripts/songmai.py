"""Seal a handoff's file evidence; resume only reads and compares it."""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
from check_handoff import references, resolve_reference


def digest(path):
    sha = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            sha.update(block)
    return sha.hexdigest()


def git_state(root, snapshot):
    if not shutil.which('git'):
        return None
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0')
    for name in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_COMMON_DIR'):
        env.pop(name, None)

    def git(*args, optional=False):
        result = subprocess.run(['git', '-c', 'core.fsmonitor=false', '-C', str(root), *args], env=env,
                                capture_output=True, timeout=10)
        if result.returncode and not optional:
            raise ValueError('Git inspection failed; snapshot cannot confirm workspace state')
        return result.stdout if result.returncode == 0 else None

    inside = git('rev-parse', '--is-inside-work-tree', optional=True)
    if inside is None or inside.strip() != b'true':
        return None
    paths = ['.']
    try:
        relative = snapshot.resolve().relative_to(root).as_posix()
        paths.append(f':(exclude,literal){relative}')
    except ValueError:
        pass
    head = git('rev-parse', '--verify', 'HEAD', optional=True)
    branch = git('symbolic-ref', '--quiet', '--short', 'HEAD', optional=True)
    dirty = hashlib.sha256()
    for args in (
        ['status', '--porcelain=v1', '-z', '--untracked-files=all'],
        ['diff', '--no-ext-diff', '--no-textconv', '--binary'],
        ['diff', '--cached', '--no-ext-diff', '--no-textconv', '--binary'],
    ):
        dirty.update(git(*args, '--', *paths) + b'\0')
    return {
        'head': head.decode('utf-8').strip() if head else None,
        'branch': branch.decode('utf-8').strip() if branch else None,
        'worktree_sha256': dirty.hexdigest(),
    }


def capture(handoff, root, snapshot):
    files = {}
    for path in references(handoff):
        target = resolve_reference(path, root)
        if target == snapshot.resolve():
            raise ValueError('snapshot cannot be a file reference; send it alongside the handoff')
        files[path] = digest(target)
    return {
        'version': 1,
        'created_at': datetime.now(timezone.utc).isoformat(),
        'handoff_sha256': digest(handoff),
        'files': files,
        'git': git_state(root, snapshot),
    }


def validate_snapshot(saved):
    if (not isinstance(saved, dict) or type(saved.get('version')) is not int
            or saved['version'] != 1):
        raise ValueError('invalid or unsupported Songmai snapshot')
    files = saved.get('files')
    hashes = [saved.get('handoff_sha256')]
    if (not isinstance(files, dict) or not isinstance(saved.get('created_at'), str)
            or 'git' not in saved):
        raise ValueError('invalid Songmai snapshot fields')
    hashes.extend(files.values())
    git = saved.get('git')
    if git is not None:
        if (not isinstance(git, dict) or set(git) != {'head', 'branch', 'worktree_sha256'}
                or not all(git[name] is None or isinstance(git[name], str) for name in ('head', 'branch'))):
            raise ValueError('invalid Git evidence in snapshot')
        hashes.append(git['worktree_sha256'])
    if not all(isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value) for value in hashes):
        raise ValueError('invalid SHA-256 evidence in snapshot')


def compare(saved, current):
    changes = []
    if saved['handoff_sha256'] != current['handoff_sha256']:
        changes.append('HANDOFF_CHANGED: เอกสารส่งไม้ถูกแก้หลัง seal; ตรวจเป้าหมายและงานค้างใหม่')
    for path in sorted(saved['files'].keys() | current['files'].keys()):
        if path not in saved['files']:
            changes.append(f'REFERENCE_ADDED: {path}')
        elif path not in current['files']:
            changes.append(f'REFERENCE_REMOVED: {path}')
        elif saved['files'][path] != current['files'][path]:
            changes.append(f'CHANGED: {path}')
    old_git, new_git = saved.get('git'), current['git']
    if (old_git is None) != (new_git is None):
        changes.append('GIT_CONTEXT_CHANGED: ความพร้อมของ Git ต่างจากตอนส่งไม้')
    elif old_git is not None:
        for name, label in (('branch', 'GIT_BRANCH_CHANGED'), ('head', 'GIT_HEAD_CHANGED'),
                            ('worktree_sha256', 'GIT_WORKTREE_CHANGED')):
            if old_git[name] != new_git[name]:
                changes.append(f'{label}: ตรวจ Git และ local edits ใหม่ก่อนทำต่อ')
    return changes


def seal(snapshot, current, replace):
    text = json.dumps(current, ensure_ascii=False, indent=2) + '\n'
    if not replace or not snapshot.exists():
        with snapshot.open('x', encoding='utf-8') as output:
            output.write(text)
        return
    validate_snapshot(json.loads(snapshot.read_text(encoding='utf-8')))
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=snapshot.parent,
                                         prefix='.songmai-', delete=False) as output:
            temporary = Path(output.name)
            output.write(text)
        os.replace(temporary, snapshot)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
    parser = argparse.ArgumentParser(description='Songmai: seal evidence, then detect stale handoffs without changing project files.')
    parser.add_argument('command', choices=['seal', 'resume'])
    parser.add_argument('handoff', type=Path)
    parser.add_argument('--root', type=Path, help='Workspace root (default: handoff parent)')
    parser.add_argument('--replace', action='store_true', help='Explicitly replace an existing valid snapshot after updating the handoff')
    args = parser.parse_args()
    if args.replace and args.command != 'seal':
        parser.error('--replace is only valid with seal')
    try:
        root = (args.root or args.handoff.parent).resolve()
        if not root.is_dir():
            raise ValueError('workspace root must be an existing directory')
        snapshot = args.handoff.with_suffix('.songmai.json')
        if snapshot == args.handoff:
            raise ValueError('handoff and snapshot must be different files')
        if snapshot.is_symlink():
            raise ValueError('snapshot must not be a symlink')
        current = capture(args.handoff, root, snapshot)
        if args.command == 'seal':
            seal(snapshot, current, args.replace)
            print(f'SEALED: {len(current["files"])} files → {snapshot.name}')
        else:
            if not snapshot.is_file():
                raise ValueError('UNSEALED: ไม่พบหลักฐานตอนส่งไม้; ให้ผู้ส่ง seal หลังตรวจงานจริง ห้ามถือว่าผ่าน')
            saved = json.loads(snapshot.read_text(encoding='utf-8'))
            validate_snapshot(saved)
            changes = compare(saved, current)
            if changes:
                print('\n'.join(changes))
                print('STALE: อ่านไฟล์ที่เปลี่ยนและตรวจใหม่; ผลทดสอบใน HANDOFF.md เป็นหลักฐานเก่า ห้ามใช้ยืนยันงานปัจจุบัน')
                return 1
            print(f'UNCHANGED: {len(current["files"])} referenced files. สถานะไฟล์ตรงกับตอนส่งไม้; ยังต้องตรวจเกณฑ์งานจริง')
            if current['git'] is None:
                print('GIT_NOT_CHECKED: ไม่มี Git repository หรือ Git executable; ตรวจเฉพาะเอกสารและไฟล์อ้างอิง')
        return 0
    except (OSError, UnicodeError, ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
        print(f'FAIL: {error}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
