"""
plot_gap_gy.py -- Figure 1: the price gap and the expenditure ratio, 2003Q1-2019Q4,
one panel with two axes (the design of the original Figure 1).

Seasonal adjustment: each series loses the seasonal harmonics estimated in its own
univariate model (models/VECM_GAP_GY/GAP.pre and GY_M1.pre: cos/sin at the annual
frequency and, for G/Y, the Nyquist term (-1)^t), with fue's convention j = 1..n.
The 2008 steps are level, not seasonality, and stay in the series.

  left   100 x ln(PE/PU), PPP-aligned (2011)
  right  G/Y, NFPS expenditure, % of GDP
  band   2003-2006 mean +- 2 s.d. of the adjusted price gap, as in the text
  lines  dashed: the 2007 budget (28 Feb 2007); dotted: 2008Q2, when the
         fuel-import account enters the fiscal record

The two axes are scaled so that the Phase II means and the Phase III peaks of the
two series sit at the same heights.

Output: output/figures/gap_vs_gy.{pdf,png}
"""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "output", "figures")
MODELS = os.path.join(REPO, "models", "VECM_GAP_GY")


def read_pre(path):
    """Series (100 ln) and its seasonal component from a fue .pre file."""
    lines = open(path, encoding="latin-1").read().splitlines()
    freq = int(lines[next(i for i, l in enumerate(lines) if l.startswith("** Frequency")) + 1])
    k = next(i for i, l in enumerate(lines) if l.startswith("** Number of deterministic"))
    ndet = int(lines[k + 1])
    body = [l for l in lines[k + 2:] if l.strip() and not l.startswith("**")]
    names = body[:ndet]
    coefs = [float(body[ndet + 1 + i].split()[0]) for i in range(ndet)]   # body[ndet]: orders
    i = next(i for i, l in enumerate(lines) if l.startswith("** Time series"))
    y = 100 * np.log(np.array([float(l) for l in lines[i + 1:] if l.strip()]))
    j = np.arange(1, len(y) + 1)
    seas = np.zeros(len(y))
    for name, c in zip(names, coefs):
        w = name.split()
        if w[0] == "cos":
            seas += c * np.cos(2 * math.pi * int(w[1]) / freq * j)
        elif w[0] == "sin":
            seas += c * np.sin(2 * math.pi * int(w[1]) / freq * j)
        elif w[0] == "alter":
            seas += c * np.where(j % 2 == 0, 1.0, -1.0)
    return y, seas


gap, s_gap = read_pre(os.path.join(MODELS, "GAP.pre"))
lgy, s_gy = read_pre(os.path.join(MODELS, "GY_M1.pre"))
GAP = gap - s_gap                       # 100 ln(PE/PU), adjusted
GY = np.exp((lgy - s_gy) / 100) * 100   # % of GDP, adjusted
t = pd.period_range("2003Q1", periods=len(GAP), freq="Q").to_timestamp(how="start") + pd.Timedelta(days=45)

b06 = t < pd.Timestamp("2007-01-01")
mu, sd = GAP[b06].mean(), GAP[b06].std(ddof=1)
p2 = t < pd.Timestamp("2008-07-01")

# axes aligned on the Phase II means and the Phase III peaks
g_lo, g_hi = GAP[p2].mean(), GAP[~p2].max()
y_lo, y_hi = GY[p2].mean(), GY[~p2].max()
L_LO, L_HI = g_lo - 0.30 * (g_hi - g_lo), g_hi + 0.12 * (g_hi - g_lo)
f1, f2 = (g_lo - L_LO) / (L_HI - L_LO), (g_hi - L_LO) / (L_HI - L_LO)
R_RANGE = (y_hi - y_lo) / (f2 - f1)
R_LO = y_lo - f1 * R_RANGE
R_HI = R_LO + R_RANGE

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif", "serif"],
    "axes.spines.top": False, "axes.linewidth": 0.6,
    "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.major.size": 3.5, "ytick.major.size": 3.5,
    "xtick.direction": "out", "ytick.direction": "out", "pdf.fonttype": 42,
})
C_BLUE, C_RED, C_BAND = "#185FA5", "#A32D2D", "#639922"
C_P2, C_P3, C_GRID, C_VL = "#4a8018", "#BA7517", "#d8d8d8", "#2c2c2a"

fig, ax1 = plt.subplots(figsize=(6.5, 4.2))
x0, x1 = t[0] - pd.Timedelta(days=45), t[-1] + pd.Timedelta(days=45)
ax1.axvspan(x0, pd.Timestamp("2008-07-01"), color=C_P2, alpha=0.06, zorder=0, lw=0)
ax1.axvspan(pd.Timestamp("2008-07-01"), x1, color=C_P3, alpha=0.05, zorder=0, lw=0)
ax1.fill_between(t[b06], mu - 2 * sd, mu + 2 * sd, color=C_BAND, alpha=0.28, lw=0, zorder=1)
for yv in (mu - 2 * sd, mu + 2 * sd):
    ax1.axhline(yv, color=C_BAND, lw=0.5, ls=":", alpha=0.35, zorder=1)

ax2 = ax1.twinx()
ax2.plot(t, GY, color=C_RED, lw=1.6, marker="s", markersize=2.5, markerfacecolor="white",
         markeredgewidth=0.75, markeredgecolor=C_RED, linestyle="--", dashes=(5, 2.5), zorder=3)
ax2.set_ylim(R_LO, R_HI)
ax2.set_ylabel("Expenditure ratio (% of GDP, SA)", color=C_RED, fontsize=9.5, labelpad=6)
ax2.tick_params(axis="y", labelcolor=C_RED, labelsize=8.5, pad=3)
ax2.spines["right"].set_lw(0.6)
ax2.spines["right"].set_color(C_RED + "99")
ax2.spines["top"].set_visible(False)
ax2.yaxis.set_major_locator(mticker.MultipleLocator(5))

ax1.plot(t, GAP, color=C_BLUE, lw=2.2, marker="o", markersize=2.6, markerfacecolor="white",
         markeredgewidth=0.9, markeredgecolor=C_BLUE, zorder=4)
ax1.set_ylim(L_LO, L_HI)
ax1.set_ylabel(r"Price gap ($100\times\ln PE/PU$, SA)", color=C_BLUE, fontsize=9.5, labelpad=6)
ax1.tick_params(axis="y", labelcolor=C_BLUE, labelsize=8.5, pad=3)
ax1.spines["left"].set_color(C_BLUE + "99")
ax1.spines["bottom"].set_lw(0.6)
ax1.yaxis.set_major_locator(mticker.MultipleLocator(5))

bdate, cfdd = pd.Timestamp("2007-02-28"), pd.Timestamp("2008-04-01")
ax1.axvline(bdate, color=C_VL, ls="--", lw=0.9, alpha=0.60, zorder=5)
ax1.axvline(cfdd, color=C_VL, ls=":", lw=0.9, alpha=0.60, zorder=5)
ax1.text(bdate - pd.Timedelta(days=40), L_HI - 0.02 * (L_HI - L_LO), "28 Feb 2007:\n2007 budget",
         fontsize=6.5, color=C_VL, va="top", ha="right")
ax1.text(cfdd + pd.Timedelta(days=40), L_HI - 0.02 * (L_HI - L_LO), "2008Q2: change in\nthe fiscal record",
         fontsize=6.5, color=C_VL, va="top", ha="left")
ax1.text(pd.Timestamp("2005-08-01"), L_LO + 0.015 * (L_HI - L_LO), "Phase II (2002–mid-2008)",
         fontsize=7.2, color=C_P2, ha="center", va="bottom", fontweight="bold")
ax1.text(pd.Timestamp("2014-03-01"), L_LO + 0.015 * (L_HI - L_LO), "Phase III (from mid-2008)",
         fontsize=7.2, color=C_P3, ha="center", va="bottom", fontweight="bold")

ticks = [pd.Timestamp(f"{yr}-01-01") for yr in range(2003, 2021)]
ax1.set_xticks(ticks)
ax1.set_xticklabels([str(yr) if yr % 2 == 1 else "" for yr in range(2003, 2021)], fontsize=8.5)
ax1.set_xlim(x0, x1)
ax1.yaxis.grid(True, color=C_GRID, lw=0.4, alpha=0.55, zorder=0)
ax1.set_axisbelow(True)

h_gap = Line2D([0], [0], color=C_BLUE, lw=2.2, marker="o", ms=4, markerfacecolor="white",
               markeredgecolor=C_BLUE, markeredgewidth=0.9)
h_gy = Line2D([0], [0], color=C_RED, lw=1.6, ls="--", dashes=(5, 2.5), marker="s", ms=3.5,
              markerfacecolor="white", markeredgecolor=C_RED, markeredgewidth=0.75)
h_band = mpatches.Patch(facecolor=C_BAND, alpha=0.35, edgecolor="none")
ax1.legend(handles=[h_gap, h_gy, h_band],
           labels=["Price gap (left axis)", "Expenditure ratio (right axis)",
                   "2003\u20132006 mean $\\pm 2$ s.d."],
           loc="center right", fontsize=6.8, framealpha=0.93, edgecolor="#cccccc",
           fancybox=False, borderpad=0.5, labelspacing=0.38, handlelength=2.0, handletextpad=0.4)

fig.tight_layout(pad=0.5)
os.makedirs(OUT, exist_ok=True)
for ext in ("pdf", "png"):
    fig.savefig(os.path.join(OUT, f"gap_vs_gy.{ext}"), dpi=300, bbox_inches="tight")
plt.close(fig)
print(f"written gap_vs_gy; 2003-06 mean {mu:.2f}, s.d. {sd:.2f}; axes L [{L_LO:.1f}, {L_HI:.1f}] "
      f"R [{R_LO:.1f}, {R_HI:.1f}]; G/Y peak {GY[~p2].max():.1f}")
