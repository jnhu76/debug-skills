#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path.cwd()
markers = {
    'xmake': ['xmake.lua'],
    'cmake': ['CMakeLists.txt'],
    'make': ['Makefile', 'makefile'],
    'meson': ['meson.build'],
    'cargo': ['Cargo.toml'],
    'go': ['go.mod'],
    'python': ['pyproject.toml', 'requirements.txt', 'setup.py'],
    'node': ['package.json'],
    'maven': ['pom.xml'],
    'gradle': ['build.gradle', 'build.gradle.kts'],
}

commands = {
    'xmake': {'build': 'xmake -m debug && xmake -r', 'run': 'xmake run', 'test': 'xmake run'},
    'cmake': {'build': 'cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug && cmake --build build -j', 'run': './build/<binary>', 'test': 'ctest --test-dir build --output-on-failure'},
    'make': {'build': 'make', 'run': './<binary>', 'test': 'make test'},
    'meson': {'build': 'meson setup build --buildtype=debug && meson compile -C build', 'run': './build/<binary>', 'test': 'meson test -C build'},
    'cargo': {'build': 'cargo build', 'run': 'cargo run', 'test': 'cargo test'},
    'go': {'build': 'go build ./...', 'run': 'go run .', 'test': 'go test ./...'},
    'python': {'build': '', 'run': 'python <entry.py>', 'test': 'pytest -q'},
    'node': {'build': '', 'run': 'npm run <script>', 'test': 'npm test'},
    'maven': {'build': 'mvn -q test', 'run': 'mvn -q exec:java', 'test': 'mvn -q test'},
    'gradle': {'build': './gradlew test', 'run': './gradlew run', 'test': './gradlew test'},
}

hits = []
for tool, names in markers.items():
    for name in names:
        found = list(ROOT.rglob(name))
        if found:
            hits.append({'tool': tool, 'marker': name, 'paths': [str(p) for p in found[:5]]})
            break

primary = hits[0]['tool'] if hits else 'unknown'
print(json.dumps({'cwd': str(ROOT), 'primary': primary, 'detected': hits, 'commands': commands.get(primary, {})}, indent=2))
