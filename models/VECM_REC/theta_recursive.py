"""
theta_recursive.py -- recursive estimates of theta with drvec (exact ML).

Model: (G/Y | GAP), .pre G/Y M1 and GAP m04, p = 4, case 2, r = 1; main fit
with G/Y weakly exogenous (-weakex 1), and alpha free as a contrast.
The sample is cut by trimming the GAP .pre (drvec uses the COMMON sample of
the .pre files, lined up by date); the deterministics of each series come
from its own univariate model, evaluated on its own dates.

  forward : 2003Q1 .. end,   end = 2010Q4 .. 2019Q4
  backward: start .. 2019Q4, start = 2003Q1 .. 2011Q4

Writes theta_recursive.csv and $FIGURES/fig_theta_recursive.{pdf,png}.
"""
import os
import re
import csv
import subprocess
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "VECM_GAP_GY")
DRVEC = os.environ.get("DRVEC", "drvec-py")
WORK = os.path.join(HERE, "runs")
os.makedirs(WORK, exist_ok=True)

GAP = open(os.path.join(SRC, "GAP.pre")).read().split("\n")
HDR = next(i for i, l in enumerate(GAP) if l.strip().startswith("68") and "GAP" in l)
DAT = next(i for i, l in enumerate(GAP) if l.startswith("** Time series"))
DATA = [l for l in GAP[DAT + 1:] if l.strip()]
assert len(DATA) == 68
GY = os.path.join(SRC, "GY_M1.pre")


def qidx(y, q):
    return (y - 2003) * 4 + q - 1


def gap_pre(a, b, tag):
    """GAP .pre with observations a..b (0-based, inclusive)."""
    y, q = 2003 + a // 4, a % 4 + 1
    lines = GAP[:HDR] + [f" {b - a + 1}  {q} {y} GAP"] + GAP[HDR + 1:DAT + 1] + DATA[a:b + 1] + [""]
    path = os.path.join(WORK, f"GAP_{tag}.pre")
    open(path, "w").write("\n".join(lines))
    return path


NUM = r"(-?\d+\.\d+)"


def fit(job):
    kind, a, b, wx = job
    tag = f"{kind}_{a}_{b}_{'wx' if wx else 'free'}"
    gp = gap_pre(a, b, tag)
    args = [DRVEC, GY, gp, "4", "0", "1", "-case", "2", "-fdhess", "-name", tag]
    if wx:
        args += ["-weakex", "1"]
    subprocess.run(args, cwd=WORK, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1800)
    out = open(os.path.join(WORK, tag + ".out"), encoding="latin-1").read()
    m = re.search(r"GY in ec1\s+" + NUM + r"\s+" + NUM, out)
    al = re.search(r"(?:D\.GAP <- ec1|psi\[1 <- ec1\])\s+" + NUM + r"\s+" + NUM, out)
    lr = re.search(r"p-value \(chi2\)\s+:\s+" + NUM, out) if wx else None
    ll = re.search(r"logelf\s+:\s+" + NUM, out)
    res = dict(kind=kind, wx=int(wx), start=a, end=b, n=b - a + 1,
               theta=-float(m.group(1)) if m else None, se=float(m.group(2)) if m else None,
               alpha_gap=None, weakex_p=float(lr.group(1)) if lr else None,
               logL=float(ll.group(1)) if ll else None)
    if al:
        v = float(al.group(1))
        res["alpha_gap"] = -v if "psi" in al.group(0) else v
    return res


jobs = []
for e in range(qidx(2010, 4), 68):
    for wx in (True, False):
        jobs.append(("fwd", 0, e, wx))
for s0 in range(0, qidx(2011, 4) + 1):
    for wx in (True, False):
        jobs.append(("bwd", s0, 67, wx))

with ThreadPoolExecutor(max_workers=int(os.environ.get("NJOBS", "4"))) as ex:
    rows = list(ex.map(fit, jobs))

with open(os.path.join(HERE, "theta_recursive.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)


def lab(i):
    return f"{2003 + i // 4}Q{i % 4 + 1}"


for kind in ("fwd", "bwd"):
    print("forward (2003Q1 .. end)" if kind == "fwd" else "backward (start .. 2019Q4)")
    for r in rows:
        if r["kind"] == kind and r["wx"] == 1:
            fr = next(x for x in rows if x["kind"] == kind and x["wx"] == 0
                      and x["start"] == r["start"] and x["end"] == r["end"])
            key = lab(r["end"]) if kind == "fwd" else lab(r["start"])
            print(f"  {key}  n={r['n']:2d}  theta {r['theta']:.3f} ({r['se']:.3f})  "
                  f"alpha_GAP {r['alpha_gap']:.3f}  weakex p {r['weakex_p']:.3f}   "
                  f"| free theta {fr['theta']:.3f} ({fr['se']:.3f})")

# --- figure ---------------------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

C_WX, C_FR, MUTED, INK = "#2a6fb0", "#c4572a", "#777777", "#222222"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})
fig, ax = plt.subplots(1, 2, figsize=(12, 4.2), sharey=True)
for a_, kind, title, key in ((ax[0], "fwd", "A. Recursive: 2003Q1 to t", "end"),
                             (ax[1], "bwd", "B. Backward recursive: t to 2019Q4", "start")):
    for wx, col, name in ((1, C_WX, "G/Y weakly exogenous"), (0, C_FR, r"$\alpha$ free")):
        rr = sorted((r for r in rows if r["kind"] == kind and r["wx"] == wx), key=lambda r: r[key])
        x = [2003 + r[key] / 4 for r in rr]
        th = [r["theta"] for r in rr]
        if wx:
            a_.fill_between(x, [t - 1.96 * r["se"] for t, r in zip(th, rr)],
                            [t + 1.96 * r["se"] for t, r in zip(th, rr)], color=col, alpha=0.18, lw=0,
                            label="95 % (exact Hessian)")
        a_.plot(x, th, color=col, lw=2 if wx else 1.2, ls="-" if wx else "--", label=name)
    a_.axhline(0.386, color=INK, lw=0.8, ls=":")
    a_.text(a_.get_xlim()[1], 0.386, " full sample 0.386", va="center", color=MUTED, fontsize=8)
    a_.axhline(0.290, color=MUTED, lw=0.8, ls="-.")
    a_.text(a_.get_xlim()[1], 0.290, " paper 0.290", va="center", color=MUTED, fontsize=8)
    a_.set_title(title, loc="left", fontsize=10)
    a_.set_xlabel("end of sample" if kind == "fwd" else "start of sample")
ax[0].set_ylabel(r"$\hat\theta$")
ax[0].set_ylim(-0.1, 1.0)
ax[0].legend(frameon=False, fontsize=8, loc="lower right")
fig.text(0.01, -0.03, "drvec, exact ML; (G/Y | GAP), p = 4, case 2, r = 1; G/Y M1 and GAP m04 univariate "
         "models (deterministics of the .pre). Band: ±1.96 s.e. from the exact Hessian (-fdhess). "
         "Axis cut at 1.0 (start 2011Q4, n = 33: 0.88 ± 1.0).",
         fontsize=8, color=MUTED)
fig.tight_layout()
FIG = os.environ.get("FIGURES", os.path.join(HERE, "figures"))
os.makedirs(FIG, exist_ok=True)
for ext in ("pdf", "png"):
    fig.savefig(os.path.join(FIG, f"fig_theta_recursive.{ext}"), bbox_inches="tight", dpi=200)
print("written fig_theta_recursive")
