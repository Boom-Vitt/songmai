"""Read-only check of declared files in a Songmai Markdown handoff."""

import argparse
import re
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath


def references(handoff):
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
        raise ValueError('expected exactly one reference section outside closed code fences')
    if section == ['- ไม่มีไฟล์อ้างอิง']:
        return []
    paths = []
    for line in section:
        match = re.fullmatch(r'- `([^`]+)`(?:\s+[^`]*)?', line)
        if not match:
            raise ValueError('malformed reference; use - `relative/path` — description')
        paths.append(match.group(1))
    if not paths:
        raise ValueError('empty reference section; list files or - ไม่มีไฟล์อ้างอิง')
    return paths


def resolve_reference(path, root):
    if (PurePosixPath(path).is_absolute() or PureWindowsPath(path).drive
            or '..' in PurePosixPath(path).parts or '\\' in path):
        raise ValueError(f'unsafe path: {path}')
    target = (root / path).resolve()
    if not target.is_relative_to(root):
        raise ValueError(f'outside workspace: {path}')
    if not target.is_file():
        raise ValueError(f'missing file: {path}')
    return target


def check(handoff, root):
    try:
        paths = references(handoff)
    except ValueError as error:
        return [str(error)], 0
    errors = []
    for path in paths:
        try:
            resolve_reference(path, root)
        except ValueError as error:
            errors.append(str(error))
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
