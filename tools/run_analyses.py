#!/usr/bin/env python3
"""Run the drvec / drtran analyses the paper cites (tables/analyses.py).

    python tools/run_analyses.py [--status adopted,robustness] [--dir VECM_WTI]
                                 [--name wti:chain] [--no-boot] [--jobs N] [--list]

Each run works in build/analyses/<dir>/<name>/, with a copy of only the
inputs it reads (models/<dir>/...), and leaves there its .out (and .boot /
.irfboot). A run whose inputs, arguments and engine version have not
changed since its last success is skipped (cache key in <name>.key).

The runs behind the tables are not here: they are in tables/vecm_registry.py
and run with `make multivariate`. `--status` defaults to every status
(adopted, robustness, superseded, exploratory). `--no-boot` drops the rank
bootstraps and the IRF bands (-bootstrap / -irfboot), which take most of the
time; the point estimates and LR tables are unchanged.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = os.path.join(REPO, "models")
BUILD = os.path.join(REPO, "build", "analyses")
sys.path.insert(0, os.path.join(REPO, "tables"))
from analyses import RUNS  # noqa: E402

ENGINES = {"drvec": os.environ.get("DRVEC") or shutil.which("drvec-py") or "drvec-py",
           "drtran": os.environ.get("DRTRAN") or shutil.which("drtran-py") or "drtran-py"}
NAME_FLAG = {"drvec": "-name", "drtran": "-m"}

# Runs the Python port does not accept yet (see docs/analyses_verification.md).
NOT_PORTED = {
    "rec:hjfull_free": "-writeinp is not in drvec-py; its outputs (runs/hjfull_inp.{1,2}.inp) are shipped in models/VECM_REC",
}


def _version(engine: str) -> str:
    try:
        return subprocess.run([ENGINES[engine], "--version"], capture_output=True, text=True).stdout
    except OSError:
        return ""


def _strip_boot(args: str) -> str:
    t = args.split()
    out, i = [], 0
    while i < len(t):
        if t[i] in ("-bootstrap", "-irfboot"):
            i += 2
            continue
        out.append(t[i])
        i += 1
    return " ".join(out)


def run_one(key: str, r: dict, no_boot: bool, versions: dict) -> tuple[str, str]:
    if key in NOT_PORTED:
        return key, f"SKIP  {NOT_PORTED[key]}"
    src = os.path.join(MODELS, r["dir"])
    if r["engine"] == "python":
        return run_python(key, r)
    args = _strip_boot(r["args"]) if no_boot else r["args"]
    work = os.path.join(BUILD, r["dir"], r["name"])
    h = hashlib.sha256((args + versions[r["engine"]]).encode())
    for f in r["inputs"]:
        h.update(f.encode())
        h.update(open(os.path.join(src, f), "rb").read())
    keyf = os.path.join(work, r["name"] + ".key")
    out = os.path.join(work, r["name"] + ".out")
    if os.path.exists(out) and os.path.exists(keyf) and open(keyf).read() == h.hexdigest():
        return key, "cached"
    os.makedirs(work, exist_ok=True)
    for f in r["inputs"]:
        os.makedirs(os.path.dirname(os.path.join(work, f)) or work, exist_ok=True)
        shutil.copy(os.path.join(src, f), os.path.join(work, f))
    cmd = [ENGINES[r["engine"]], *args.split(), NAME_FLAG[r["engine"]], r["name"]]
    with open(os.path.join(work, r["name"] + ".log"), "w") as log:
        p = subprocess.run(cmd, cwd=work, stdout=log, stderr=subprocess.STDOUT)
    if not os.path.exists(out):
        return key, f"FAIL  exit {p.returncode}; see {os.path.relpath(work, REPO)}/{r['name']}.log"
    open(keyf, "w").write(h.hexdigest())
    return key, "ok"


def run_python(key: str, r: dict) -> tuple[str, str]:
    """The VECM_REC drivers: run in a copy of the directory, next to a copy of
    the VECM_GAP_GY inputs they read (../VECM_GAP_GY/GY_M1.pre, GAP.pre)."""
    base = os.path.join(BUILD, "rec")
    work = os.path.join(base, r["dir"])
    if not os.path.isdir(work):
        shutil.copytree(os.path.join(MODELS, r["dir"]), work)
        shutil.copytree(os.path.join(MODELS, "VECM_GAP_GY"), os.path.join(base, "VECM_GAP_GY"))
    os.makedirs(os.path.join(work, "runs"), exist_ok=True)
    env = dict(os.environ, DRVEC=ENGINES["drvec"], FIGURES=os.path.join(REPO, "output", "figures"))
    script = next(t for t in r["args"].split() if t.endswith(".py"))
    for t in r["args"].split("#")[0].split():
        if "=" in t and not t.startswith("DRVEC"):
            k, v = t.split("=", 1)
            env[k] = v
    with open(os.path.join(work, script[:-3] + ".log"), "w") as log:
        p = subprocess.run([sys.executable, script], cwd=work, env=env, stdout=log, stderr=subprocess.STDOUT)
    return key, "ok" if p.returncode == 0 else f"FAIL  exit {p.returncode}; see {os.path.relpath(work, REPO)}/{script[:-3]}.log"


# the drivers depend on each other's outputs: run them in this order, after the rest
PY_ORDER = ["rec:theta_recursive", "rec:hj_beta", "rec:hj_lambda", "rec:hjfull_free", "rec:hj_boot"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", default="")
    ap.add_argument("--dir", default="")
    ap.add_argument("--name", default="")
    ap.add_argument("--no-boot", action="store_true")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    sel = {k: r for k, r in RUNS.items()
           if (not a.status or r["status"] in a.status.split(","))
           and (not a.dir or r["dir"].split("/")[0] == a.dir)
           and (not a.name or k == a.name)}
    if a.list:
        for k, r in sel.items():
            print(f"{k:28s} {r['status']:12s} {r['kind']:12s} {r['dir']:14s} {r['args']}")
        return 0
    versions = {e: _version(e) for e in ENGINES}
    rest = [k for k in sel if sel[k]["engine"] != "python"]
    py = [k for k in PY_ORDER if k in sel] + [k for k in sel if sel[k]["engine"] == "python" and k not in PY_ORDER]
    fails = 0
    with ThreadPoolExecutor(a.jobs) as ex:
        for k, msg in ex.map(lambda k: run_one(k, sel[k], a.no_boot, versions), rest):
            print(f"{k:28s} {msg}", flush=True)
            fails += msg.startswith("FAIL")
    for k in py:
        k, msg = run_one(k, sel[k], a.no_boot, versions)
        print(f"{k:28s} {msg}", flush=True)
        fails += msg.startswith("FAIL")
    print(f"{len(sel)} runs, {fails} failed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
