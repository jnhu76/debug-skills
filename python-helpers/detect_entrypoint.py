#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path.cwd()
candidates = []
patterns = ['main.cpp', 'main.c', 'main.go', 'main.py', 'app.py', 'server.py', 'index.js', 'main.rs']

for pattern in patterns:
    for p in ROOT.rglob(pattern):
        candidates.append({'path': str(p), 'reason': f'matched {pattern}'})

for p in ROOT.rglob('*_test.go'):
    candidates.append({'path': str(p), 'reason': 'go test candidate'})
for p in ROOT.rglob('test_*.py'):
    candidates.append({'path': str(p), 'reason': 'pytest candidate'})
for p in ROOT.rglob('*.spec.js'):
    candidates.append({'path': str(p), 'reason': 'node test candidate'})
for p in ROOT.rglob('*.cpp'):
    candidates.append({'path': str(p), 'reason': 'native source candidate'})

print(json.dumps({'cwd': str(ROOT), 'candidates': candidates[:40]}, indent=2))
