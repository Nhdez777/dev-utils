#!/usr/bin/env python3
"""
env-check.py — scan a project for .env variable usage and compare against .env.example
Usage: python env-check.py ./my-project
"""

import os
import re
import sys
from pathlib import Path

SKIP_DIRS = {'node_modules', '.git', 'dist', 'build', '__pycache__', '.next', 'venv'}
CODE_EXTS = {'.js', '.ts', '.tsx', '.jsx', '.py', '.sh', '.mjs', '.cjs'}
ENV_PATTERN = re.compile(r'process\.env\.([A-Z_][A-Z0-9_]*)|os\.environ(?:\.get)?\(["\']([A-Z_][A-Z0-9_]*)')


def find_env_usages(root: Path) -> dict[str, list[str]]:
    """Return {VAR_NAME: [file_path, ...]} for all env vars referenced in code."""
    usages: dict[str, list[str]] = {}
    for path in root.rglob('*'):
        if any(skip in path.parts for skip in SKIP_DIRS):
            continue
        if path.suffix not in CODE_EXTS:
            continue
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
        except (OSError, PermissionError):
            continue
        for match in ENV_PATTERN.finditer(text):
            var = match.group(1) or match.group(2)
            rel = str(path.relative_to(root))
            usages.setdefault(var, [])
            if rel not in usages[var]:
                usages[var].append(rel)
    return usages


def load_example_file(root: Path) -> set[str]:
    """Parse .env.example and return the set of defined variable names."""
    example_path = root / '.env.example'
    if not example_path.exists():
        print(f'Warning: no .env.example found at {example_path}')
        return set()
    defined: set[str] = set()
    for line in example_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            defined.add(line.split('=')[0].strip())
    return defined


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    if not root.is_dir():
        print(f'Error: {root} is not a directory')
        sys.exit(1)

    print(f'Scanning {root.resolve()}...\n')
    usages = find_env_usages(root)
    defined = load_example_file(root)

    missing = {var: files for var, files in usages.items() if var not in defined}

    if not missing:
        print('All env vars are documented in .env.example')
        return

    print(f'Missing from .env.example ({len(missing)} variable(s)):\n')
    for var, files in sorted(missing.items()):
        print(f'  {var}')
        for f in files[:3]:
            print(f'    └─ {f}')
        if len(files) > 3:
            print(f'    └─ ... and {len(files) - 3} more')
    print()


if __name__ == '__main__':
    main()
