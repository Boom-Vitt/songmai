"""Read-only check of declared files in a Songmai Markdown handoff."""

import argparse
import re
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath


def check(handoff, root):
    text = handoff.read_text(encoding='utf-8-sig')
    section = []
    sections = 0
    active = False
    fence = None
    for line in text.splitlines():
        match = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if match:
            marker, tail = match.groups()
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not tail.strip():
                fence = None
            continue
        if fence is not None:
            continue
        if re.match(r'^##(?:\s|$)', line):
            active = line.rstrip() == '## ไฟล์อ้างอิง'
            sections += int(active)
        elif active and line.strip():
            section.append(line.strip())
    if sections != 1 or fence is not None:
        return ['expected exactly one reference section outside closed code fences'], 0
    if section == ['- ไม่มีไฟล์อ้างอิง']:
        return [], 0
    paths = []
    for line in section:
        match = re.fullmatch(r'- `([^`]+)`(?:\s+[^`]*)?', line)
        if not match:
            return ['malformed reference; use - `relative/path` — description'], 0
        paths.append(match.group(1))
    if not paths:
        return ['empty reference section; list files or - ไม่มีไฟล์อ้างอิง'], 0
    errors = []
    for path in paths:
        if (PurePosixPath(path).is_absolute() or PureWindowsPath(path).drive
                or '..' in PurePosixPath(path).parts or '\\' in path):
            errors.append(f'unsafe path: {path}')
            continue
        target = (root / path).resolve()
        if not target.is_relative_to(root):
            errors.append(f'outside workspace: {path}')
        elif not target.is_file():
            errors.append(f'missing file: {path}')
    return errors, len(paths)


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
    parser = argparse.ArgumentParser(description='Check declared handoff files; never read their contents or change them.')
    parser.add_argument('handoff', type=Path, help='Path to HANDOFF.md')
    parser.add_argument('--root', type=Path, help='Workspace root (default: handoff parent)')
    args = parser.parse_args()
    try:
        root = (args.root or args.handoff.parent).resolve()
        if not root.is_dir():
            raise ValueError('workspace root must be an existing directory')
        errors, count = check(args.handoff, root)
    except (OSError, UnicodeError, ValueError, RuntimeError) as error:
        errors, count = [str(error)], 0
    for error in errors:
        print(f'FAIL: {error}')
    if not errors:
        print(f'PASS: {count} file references exist inside workspace. Handoff accuracy is not checked.')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
