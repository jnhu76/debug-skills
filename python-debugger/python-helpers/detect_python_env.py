#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path.cwd()
checks = ['.venv', 'venv', 'pyproject.toml', 'requirements.txt', 'poetry.lock', 'pdm.lock', 'uv.lock']
found = []
for name in checks:
    for p in ROOT.rglob(name):
        found.append(str(p))
        break

strategy = 'unknown'
if any(p.endswith('/.venv') or p.endswith('/venv') for p in found):
    strategy = 'reuse-existing-venv'
elif any(p.endswith('poetry.lock') for p in found):
    strategy = 'poetry'
elif any(p.endswith('uv.lock') for p in found):
    strategy = 'uv'
elif any(p.endswith('pdm.lock') for p in found):
    strategy = 'pdm'
elif any(p.endswith('requirements.txt') or p.endswith('pyproject.toml') for p in found):
    strategy = 'project-python-env'

print(json.dumps({'cwd': str(ROOT), 'found': found, 'strategy': strategy}, indent=2))
