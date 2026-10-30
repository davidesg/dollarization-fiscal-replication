#!/usr/bin/env python3
"""Compare the regenerated tables (output/tables) with the reference (expected/tables).

    python tools/verify.py [--rtol 1e-6] [--boot-atol 0.0]

- `tab_*.tex`: must be identical (they print rounded numbers).
- `*.json`: every number within `--rtol` (relative); software versions and
  file paths are ignored. Bootstrap p-values and critical values may be
  given an absolute tolerance with `--boot-atol` (the Monte Carlo error),
  for runs whose bootstrap did not use the compiled engine.

Exit status 0 when everything matches.
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "output", "tables")
EXP = os.path.join(REPO, "expected", "tables")
IGNORE = {"meta", "path", "out", "log", "versions", "software"}
BOOT_KEYS = ("p_boot", "pboot", "boot", "cv")


def walk(a, b, path, rtol, boot_atol, bad):
    if isinstance(b, dict):
        for k, v in b.items():
            if k in IGNORE:
                continue
            if not isinstance(a, dict) or k not in a:
                bad.append(f"{path}/{k}: missing")
                continue
            walk(a[k], v, f"{path}/{k}", rtol, boot_atol, bad)
    elif isinstance(b, list):
        if not isinstance(a, list) or len(a) != len(b):
            bad.append(f"{path}: length {len(a) if isinstance(a, list) else '?'} != {len(b)}")
            return
        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, f"{path}[{i}]", rtol, boot_atol, bad)
    elif isinstance(b, float) and isinstance(a, (int, float)):
        if math.isnan(b) and math.isnan(a):
            return
        tol = rtol * max(abs(b), 1e-12)
        if any(k in path.lower() for k in BOOT_KEYS):
            tol = max(tol, boot_atol)
        if abs(a - b) > tol:
            bad.append(f"{path}: {a!r} != {b!r}")
    elif a != b and isinstance(b, (int, bool)):
        bad.append(f"{path}: {a!r} != {b!r}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rtol", type=float, default=1e-6)
    ap.add_argument("--boot-atol", type=float, default=0.0)
    a = ap.parse_args()
    fails = 0
    for e in sorted(glob.glob(os.path.join(EXP, "tab_*.tex"))):
        o = os.path.join(OUT, os.path.basename(e))
        same = os.path.exists(o) and open(o, "rb").read() == open(e, "rb").read()
        print(f"{'ok  ' if same else 'DIFF'} {os.path.basename(e)}")
        fails += not same
    for e in sorted(glob.glob(os.path.join(EXP, "*.json"))):
        o = os.path.join(OUT, os.path.basename(e))
        if not os.path.exists(o):
            print(f"MISS {os.path.basename(e)}")
            fails += 1
            continue
        bad: list[str] = []
        walk(json.load(open(o)), json.load(open(e)), "", a.rtol, a.boot_atol, bad)
        print(f"{'ok  ' if not bad else 'DIFF'} {os.path.basename(e)}" + (f" ({len(bad)} numbers)" if bad else ""))
        for line in bad[:10]:
            print("     ", line)
        fails += bool(bad)
    print("all match" if not fails else f"{fails} file(s) differ")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
