"""
plot_irf_transitory.py -- B10: the transitory shock (Gonzalo-Ng P-T decomposition)
with parametric-bootstrap bands, read from drvec's -irfboot CSVs.

With the permanent shocks' series weakly exogenous, alpha_perp spans their
innovations, so the transitory shock beta'u, orthogonalised on alpha_perp'u,
is exactly the last Cholesky shock with the weakly exogenous series ordered
first. Its permanent effect is zero by construction (drvec prints gain 0).

  bivariate : (G/Y | GAP), p 4, case 2, r 1, G/Y weakly exogenous
              VECM_GAP_GY/irfboot_wx.irfboot, shock GAP
  trivariate: (G/Y, IPC_USA, GAPc), p 2, -case pre, r 1, alpha = (0, 0, a)
              (G/Y and IPC_USA weakly exogenous, LR 1.35, 2 df, p 0.51)
              VECM_TRI_IRF/tri_A_boot.irfboot, shock GAPc
Units 100 x ln. Writes output/figures/fig_suite_irf_transitory.{pdf,png}
and VECM_TRI_IRF/irf_transitory.csv.
"""
import os
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
from _paths import FIG, src


def bands(path):
    out = {}
    with open(path) as f:
        for row in csv.reader(l for l in f if not l.startswith("#")):
            if row[0] == "what":
                continue
            out.setdefault((row[0], row[1], row[2]), []).append((int(row[3]),) + tuple(float(x) for x in row[4:]))
    return out


BI = bands(src("biv:irfboot_wx", ".irfboot"))
TRI = bands(src("triirf:tri_A_boot", ".irfboot"))
series = (("bivariate", BI[("irf", "GAP", "GAP")], BI[("irf", "GAP", "GY")]),
          ("trivariate", TRI[("irf", "GAPc", "GAPc")], TRI[("irf", "GAPc", "GY")]))

print("GAP response to the transitory shock (100 x ln): point [95 %]  % of impact")
with open(os.path.join(FIG, "irf_transitory.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["system", "k", "point", "p2.5", "p5", "p50", "p95", "p97.5", "pct_of_impact", "gy_point"])
    for name, g, y in series:
        imp = g[0][1]
        print(name)
        for r, ry in zip(g, y):
            w.writerow([name, r[0]] + list(r[1:]) + [round(100 * r[1] / imp, 1), ry[1]])
            if r[0] in (0, 1, 2, 4, 5, 8, 10, 12, 16, 20):
                print(f"  k={r[0]:2d}  {r[1]:.3f} [{r[2]:.3f}, {r[6]:.3f}]  {100 * r[1] / imp:5.1f} %   G/Y {ry[1]:.3f}")

C_GAP, C_GY, MUTED, INK = "#c4572a", "#2a6fb0", "#777777", "#222222"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})
fig, ax = plt.subplots(1, 2, figsize=(12, 4.2), sharey=True)
titles = {"bivariate": "A",
          "trivariate": "B"}
for a, (name, g, y) in zip(ax, series):
    k = [r[0] for r in g]
    a.fill_between(k, [r[2] for r in g], [r[6] for r in g], color=C_GAP, alpha=0.12, lw=0, label="95 % band")
    a.fill_between(k, [r[3] for r in g], [r[5] for r in g], color=C_GAP, alpha=0.22, lw=0, label="90 % band")
    a.plot(k, [r[1] for r in g], color=C_GAP, lw=2, label="GAP")
    a.plot(k, [r[1] for r in y], color=C_GY, lw=1.2, ls="--", label="G/Y")
    a.axhline(0, color=MUTED, lw=0.8)
    a.set_title(titles[name], loc="left", fontsize=10)
    a.set_xlabel("quarters")
ax[0].set_ylabel("100 × log points")
ax[0].legend(frameon=False, fontsize=8, loc="upper right")
fig.tight_layout()
for ext in ("pdf", "png"):
    fig.savefig(os.path.join(FIG, f"fig_suite_irf_transitory.{ext}"), bbox_inches="tight", dpi=200)
print("written fig_suite_irf_transitory")
