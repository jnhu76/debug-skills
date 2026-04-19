#!/usr/bin/env python3
import argparse, json, subprocess, time

parser = argparse.ArgumentParser()
parser.add_argument('--cmd', required=True)
parser.add_argument('--timeout', type=int, default=20)
args = parser.parse_args()

start = time.time()
proc = subprocess.run(args.cmd, shell=True, capture_output=True, text=True, timeout=args.timeout)
print(json.dumps({
    'command': args.cmd,
    'returncode': proc.returncode,
    'stdout': proc.stdout[-12000:],
    'stderr': proc.stderr[-12000:],
    'duration_sec': round(time.time() - start, 3),
}, indent=2))
