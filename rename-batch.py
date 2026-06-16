#!/usr/bin/env python3
"""
rename-batch.py — bulk rename files using regex patterns
Usage: python rename-batch.py <directory> <pattern> <replacement> [--dry-run]

Examples:
  python rename-batch.py ./photos "IMG_(\d+)" "photo_\1"
  python rename-batch.py ./docs "(\w+)_v\d+" "\1_final" --dry-run
"""

import os
import re
import sys
import argparse
from pathlib import Path


def rename_batch(directory: str, pattern: str, replacement: str, dry_run: bool = False):
    target = Path(directory)
    if not target.is_dir():
        print(f'Error: {directory} is not a directory')
        sys.exit(1)

    regex = re.compile(pattern)
    files = [f for f in target.iterdir() if f.is_file()]
    renamed = 0
    skipped = 0

    print(f'{"[DRY RUN] " if dry_run else ""}Renaming files in {target.resolve()}\n')

    for f in sorted(files):
        new_name = regex.sub(replacement, f.stem) + f.suffix
        if new_name == f.name:
            skipped += 1
            continue
        new_path = f.parent / new_name
        print(f'  {f.name} → {new_name}')
        if not dry_run:
            f.rename(new_path)
        renamed += 1

    print(f'\n{"Would rename" if dry_run else "Renamed"} {renamed} file(s), skipped {skipped}.')


def main():
    parser = argparse.ArgumentParser(description='Bulk rename files using regex')
    parser.add_argument('directory', help='Target directory')
    parser.add_argument('pattern', help='Regex pattern to match (applied to filename stem)')
    parser.add_argument('replacement', help='Replacement string (supports backreferences like \\1)')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without renaming')
    args = parser.parse_args()
    rename_batch(args.directory, args.pattern, args.replacement, args.dry_run)


if __name__ == '__main__':
    main()
