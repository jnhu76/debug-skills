#!/usr/bin/env python3
from pathlib import Path
import argparse, json, shutil, time

ROOT = Path.cwd()
SNAP_ROOT = ROOT / '.skill-snapshots'

def copy_file(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.exists():
        shutil.copy2(src, dst)

parser = argparse.ArgumentParser()
sub = parser.add_subparsers(dest='cmd', required=True)

p1 = sub.add_parser('snapshot')
p1.add_argument('files', nargs='+')

p2 = sub.add_parser('restore')
p2.add_argument('snapshot_id')

p3 = sub.add_parser('status')

args = parser.parse_args()

if args.cmd == 'snapshot':
    snap_id = str(int(time.time()))
    snap_dir = SNAP_ROOT / snap_id
    manifest = []
    for name in args.files:
        p = (ROOT / name).resolve()
        try:
            rel = p.relative_to(ROOT)
        except ValueError:
            continue
        copy_file(p, snap_dir / rel)
        manifest.append(str(rel))
    snap_dir.mkdir(parents=True, exist_ok=True)
    (snap_dir / 'manifest.json').write_text(json.dumps({'files': manifest}, indent=2), encoding='utf-8')
    print(json.dumps({'snapshot_id': snap_id, 'files': manifest}, indent=2))

elif args.cmd == 'restore':
    snap_dir = SNAP_ROOT / args.snapshot_id
    manifest_path = snap_dir / 'manifest.json'
    if not manifest_path.exists():
        raise SystemExit('snapshot not found')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))['files']
    for rel in manifest:
        src = snap_dir / rel
        dst = ROOT / rel
        copy_file(src, dst)
    print(json.dumps({'snapshot_id': args.snapshot_id, 'restored': manifest}, indent=2))

elif args.cmd == 'status':
    print(json.dumps({
        'cwd': str(ROOT),
        'git_dir_exists': (ROOT / '.git').exists(),
        'snapshot_root': str(SNAP_ROOT),
    }, indent=2))
