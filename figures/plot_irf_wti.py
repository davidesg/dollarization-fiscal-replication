"""
plot_irf_wti.py -- responses of G/Y and of the price gap to a WTI shock in the
system (WTI, G/Y | GAP), read from drvec's -irfboot CSV (no re-estimation).

Model: VECM_WTI/chain_fx: WTI, G/Y and GAP .pre, p = 4, case 2, r = 1, WTI's
weight in beta held at 0 (-fixb2row 1 0; LR 0.20, p 0.66), theta 0.357.
Run with the C drvec 0.13 (atsw-gui engines/drvec/bin/drvec): chain_fx_c013.*,
identical to the 0.10 run (chain_fx.*). drvec-py 0.1.0 refuses -xsys with
-fixb2row: pending for its next version (drvec-python TODO, Next).
Cholesky order WTI -> G/Y -> GAP; bands: parametric bootstrap, 499 replications.
Panel B adds theta x (response of G/Y), the long-run path the cointegrating
relation implies for the gap. Units 100 x ln.

Output: output/figures/fig_wti_irf.{pdf,png}
"""
import csv
import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker

HERE = os.path.dirname(os.path.abspath(__file__))
from _paths import FIG, SUITE
# Not reproducible with drvec-py 0.1.0 (-xsys with -fixb2row is refused): the
# figure reads the C drvec 0.13 output of the analysis, so SUITE must be set.
if not SUITE:
    raise SystemExit("plot_irf_wti.py: set SUITE=<revision-suite/Python/art_drvec>; "
                     "the run needs the C drvec (see the TODO of drvec-python)")
D = os.path.join(SUITE, "VECM_WTI")


def bands(path):
    out = {}
    with open(path) as f:
        for row in csv.reader(l for l in f if not l.startswith("#")):
            if row[0] == "what":
                continue
            out.setdefault((row[0], row[1], row[2]), []).append((int(row[3]),) + tuple(float(x) for x in row[4:]))
    return out


B = bands(os.path.join(D, "chain_fx_c013.irfboot"))
txt = open(os.path.join(D, "chain_fx_c013.out"), encoding="latin-1").read()
theta = -float(re.search(r"^\s+GY in ec1\s+(-?\d+\.\d+)", txt, re.M).group(1))

C_GY, C_GAP, MUTED = "#2a6fb0", "#c4572a", "#777777"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})
fig, ax = plt.subplots(1, 2, figsize=(12, 4.2))
for a, resp, color, title in ((ax[0], "GY", C_GY, "A"), (ax[1], "GAP", C_GAP, "B")):
    g = B[("irf", "WTI", resp)]
    k = [r[0] for r in g]
    a.fill_between(k, [r[2] for r in g], [r[6] for r in g], color=color, alpha=0.12, lw=0, label="95 % band")
    a.fill_between(k, [r[3] for r in g], [r[5] for r in g], color=color, alpha=0.22, lw=0, label="90 % band")
    a.plot(k, [r[1] for r in g], color=color, lw=2, label="G/Y" if resp == "GY" else "GAP")
    a.axhline(0, color=MUTED, lw=0.8)
    a.set_title(title, loc="left", fontsize=10)
    a.set_xlabel("quarters")
    a.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
gy = B[("irf", "WTI", "GY")]
ax[1].plot([r[0] for r in gy], [theta * r[1] for r in gy], color=C_GY, lw=1.2, ls="--",
           label=r"$\hat\theta\times$ response of G/Y")
ax[0].set_ylabel("100 × log points")
for a in ax:
    a.legend(frameon=False, fontsize=8, loc="upper left")
fig.tight_layout()
os.makedirs(FIG, exist_ok=True)
for ext in ("pdf", "png"):
    fig.savefig(os.path.join(FIG, f"fig_wti_irf.{ext}"), bbox_inches="tight", dpi=200)
print("written fig_wti_irf, theta", theta)
