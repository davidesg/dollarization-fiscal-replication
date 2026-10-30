"""
plot_irf_fevd_suite.py -- IRF and FEVD of the suite's main model, read from
drvec's own report (no re-estimation here).

Model: (G/Y | GAP), .pre G/Y M1 and GAP m04, p = 4, case 2, r = 1, exact ML.
Two fits:
  fit_p4_c2_r1      alpha free
  fit_p4_c2_r1_wx   G/Y weakly exogenous (-weakex 1; LR 1.55, p 0.21)
Orthogonalisation: drvec's, in the input's order G/Y -> GAP (the paper's
Cholesky order).  Units: 100*ln, so a response is in % (log points x 100).

Output: output/figures/fig_suite_irf_fevd.{pdf,png} and a table
(stdout, and VECM_GAP_GY/irf_fevd_suite.csv).
"""
import os
import re
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
from _paths import FIG, src
_KEY = {"fit_p4_c2_r1": "biv_free", "fit_p4_c2_r1_wx": "biv_wx", "irfboot_wx": "biv:irfboot_wx"}


def block(lines, start, ncol=2):
    """Rows `k v1 v2` (or `h p1% p2%`) after the line equal to `start`."""
    out, on = [], False
    for ln in lines:
        if ln.rstrip() == start:
            on = True
            continue
        if on:
            m = re.match(r"^\s+(\d+)\s+(-?[\d.]+)%?\s+(-?[\d.]+)%?\s*$", ln)
            if m:
                out.append((int(m.group(1)), float(m.group(2)), float(m.group(3))))
            elif out:
                break
    return out


def read(name):
    with open(src(_KEY[name]), encoding="latin-1") as f:
        L = f.read().splitlines()
    i0 = next(i for i, ln in enumerate(L) if "Impulse Response of the Levels" in ln)
    i1 = next(i for i, ln in enumerate(L) if "Forecast Error Variance Decomposition" in ln)
    irf_gy = block(L[i0:], "Shock to GY:")
    irf_gap = block(L[i0:], "Shock to GAP:")
    fevd_gap = block(L[i1:], "GAP:")
    gains = [float(x) for x in re.findall(r"GAP\s+: gain =\s+(-?[\d.]+)", "\n".join(L))]
    gains_gy = [float(x) for x in re.findall(r"GY\s+: gain =\s+(-?[\d.]+)", "\n".join(L))]
    return dict(irf_gy=irf_gy, irf_gap=irf_gap, fevd_gap=fevd_gap, gains=gains, gains_gy=gains_gy)


free = read("fit_p4_c2_r1")
wx = read("fit_p4_c2_r1_wx")


def bands(name):
    """<name>.irfboot (drvec -irfboot): {(what, shock, resp): [(k, pt, 2.5, 5, 50, 95, 97.5)]}"""
    out = {}
    path = src(_KEY[name], ".irfboot")
    if not os.path.exists(path):
        return out
    with open(path) as f:
        for row in csv.reader(l for l in f if not l.startswith("#")):
            if row[0] == "what":
                continue
            key = (row[0], row[1], row[2])
            out.setdefault(key, []).append((int(row[3]),) + tuple(float(x) for x in row[4:]))
    return out


B = bands("irfboot_wx")

# --- table ---------------------------------------------------------------
H = (1, 2, 4, 8, 12, 16, 20)
rows = []
print("FEVD of GAP, % due to the G/Y shock  [alpha free | G/Y weakly exogenous]")
for h in H:
    a = next(r for r in free["fevd_gap"] if r[0] == h)
    b = next(r for r in wx["fevd_gap"] if r[0] == h)
    print(f"  h = {h:2d}:  {a[1]:5.1f}  |  {b[1]:5.1f}")
    rows.append(dict(h=h, fevd_gy_free=a[1], fevd_gy_wx=b[1]))
print("IRF of GAP to a one-s.d. G/Y shock (x100 ln)  [free | wx]")
for k in (0, 1, 4, 8, 12, 16, 20):
    a = next(r for r in free["irf_gy"] if r[0] == k)
    b = next(r for r in wx["irf_gy"] if r[0] == k)
    print(f"  k = {k:2d}:  {a[2]:.4f}  |  {b[2]:.4f}")
    for r in rows:
        pass
print("long-run gains on GAP (G/Y shock, GAP shock): free", free["gains"][:2], " wx", wx["gains"][:2])
with open(os.path.join(FIG, "irf_fevd_suite.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["k", "irf_gap_gyshock_free", "irf_gap_gyshock_wx", "irf_gap_gapshock_free",
                "irf_gap_gapshock_wx", "fevd_gap_gy_free", "fevd_gap_gy_wx"])
    fev_f = {r[0]: r[1] for r in free["fevd_gap"]}
    fev_w = {r[0]: r[1] for r in wx["fevd_gap"]}
    for (k, _, a), (_, _, b), (_, _, c), (_, _, d) in zip(free["irf_gy"], wx["irf_gy"],
                                                          free["irf_gap"], wx["irf_gap"]):
        w.writerow([k, a, b, c, d, fev_f.get(k, ""), fev_w.get(k, "")])

# --- figure --------------------------------------------------------------
C_GY, C_GAP, INK, MUTED = "#2a6fb0", "#c4572a", "#222222", "#777777"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
                     "ytick.color": MUTED})
fig, ax = plt.subplots(1, 3, figsize=(13, 4))

k = [r[0] for r in wx["irf_gy"]]
def shade(a, key, color):
    if key not in B:
        return
    rows = B[key]
    kk = [r[0] for r in rows]
    a.fill_between(kk, [r[2] for r in rows], [r[6] for r in rows], color=color, alpha=0.12, lw=0, label="95 % band")
    a.fill_between(kk, [r[3] for r in rows], [r[5] for r in rows], color=color, alpha=0.22, lw=0, label="90 % band")
shade(ax[0], ("irf", "GY", "GAP"), C_GY)
shade(ax[1], ("irf", "GAP", "GAP"), C_GAP)
ax[0].plot(k, [r[2] for r in wx["irf_gy"]], color=C_GY, lw=2, label="G/Y weakly exogenous")
ax[0].plot(k, [r[2] for r in free["irf_gy"]], color=C_GY, lw=1.2, ls="--", label=r"$\alpha$ free")
ax[0].axhline(wx["gains"][0], color=MUTED, lw=0.8, ls=":")
# the permanent effect on GAP is theta times the permanent effect on G/Y itself
ax[0].text(20, wx["gains"][0], f"  gain {wx['gains'][0]:.2f}\n  (G/Y: {wx['gains_gy'][0]:.2f})",
           va="center", color=MUTED, fontsize=8)
ax[0].set_title("A", loc="left", fontsize=10)
ax[0].set_xlabel("quarters"); ax[0].set_ylabel("GAP, 100 × log points")
ax[0].legend(frameon=False, fontsize=8, loc="lower right")

ax[1].plot(k, [r[2] for r in wx["irf_gap"]], color=C_GAP, lw=2, label="G/Y weakly exogenous")
ax[1].plot(k, [r[2] for r in free["irf_gap"]], color=C_GAP, lw=1.2, ls="--", label=r"$\alpha$ free")
ax[1].axhline(0, color=MUTED, lw=0.8)
ax[1].set_title("B", loc="left", fontsize=10)
ax[1].set_xlabel("quarters")
ax[1].legend(frameon=False, fontsize=8)

h = [r[0] for r in wx["fevd_gap"]]
gy = [r[1] for r in wx["fevd_gap"]]
ax[2].bar(h, gy, color=C_GY, width=0.8, label="G/Y shock")
ax[2].bar(h, [100 - g for g in gy], bottom=gy, color=C_GAP, width=0.8, label="GAP shock")
ax[2].plot(h, [r[1] for r in free["fevd_gap"]], color=INK, lw=1, ls="--", label=r"G/Y share, $\alpha$ free")
if ("fevd", "GY", "GAP") in B:
    rows = B[("fevd", "GY", "GAP")]
    ax[2].errorbar([r[0] for r in rows], [r[1] for r in rows],
                   yerr=[[r[1] - r[3] for r in rows], [r[5] - r[1] for r in rows]],
                   fmt="none", ecolor=INK, elinewidth=0.8, capsize=2, label="90 % band (G/Y)")
ax[2].set_ylim(0, 100)
ax[2].set_title("C", loc="left", fontsize=10)
ax[2].set_xlabel("horizon h (quarters)"); ax[2].set_ylabel("%")
ax[2].legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=3)

fig.tight_layout()
os.makedirs(FIG, exist_ok=True)
for ext in ("pdf", "png"):
    fig.savefig(os.path.join(FIG, f"fig_suite_irf_fevd.{ext}"), bbox_inches="tight", dpi=200)
print("written", os.path.join(FIG, "fig_suite_irf_fevd.pdf"))
