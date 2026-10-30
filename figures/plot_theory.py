"""
plot_theory.py -- the three diagrams of Section 3 (DAS, DAD, equilibrium), drawn
from the model's own equations so that notation and shapes match the text.

  DAS  pi_t = E_{t-1}[pi_t] + beta (yhat_t - yhat_n) - n_t   (short run, slope beta)
       vertical at yhat_n in the long run
  DAD  pi_t = pi_ft + theta (ghat_t - yhat_t) + s_t           (linear, slope -theta)
  Equilibrium: a rise in ghat shifts DAD right; output and inflation rise in the
  short run; in the long run output returns to yhat_n and the inflation
  differential settles at theta (ghat - yhat_n).

Parameter values are illustrative (no units on the axes).
Output: output/figures/fig_das.{pdf,png}, fig_dad.{pdf,png}, fig_equilibrium.{pdf,png}
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "output", "figures")
os.makedirs(OUT, exist_ok=True)

C_S, C_D, MUTED, INK = "#2a6fb0", "#c4572a", "#777777", "#222222"
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": INK, "mathtext.fontset": "cm"})

YN, PIF, BETA, THETA = 3.0, 2.0, 1.0, 0.8
G0, G1 = 3.6, 5.0
y = np.linspace(0.6, 5.6, 200)


def dad(g):
    return PIF + THETA * (g - y)


def axes(ax):
    ax.set_xlim(0.4, 6.4)
    ax.set_ylim(0, 6.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel(r"$\hat{y}_t$", loc="right")
    ax.set_ylabel(r"$\pi_t$", loc="top", rotation=0)


def guide(ax, x, yv, xl=None, yl=None):
    ax.plot([x, x], [0, yv], color=MUTED, lw=0.8, ls=":")
    ax.plot([0.4, x], [yv, yv], color=MUTED, lw=0.8, ls=":")
    if xl:
        ax.text(x, -0.12, xl, ha="center", va="top")
    if yl:
        ax.text(0.33, yv, yl, ha="right", va="center")


def save(fig, name):
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"), bbox_inches="tight", dpi=200)
    plt.close(fig)


# DAS -----------------------------------------------------------------------
pi_star = PIF + THETA * (G0 - YN)
fig, ax = plt.subplots(figsize=(6, 4))
axes(ax)
ax.plot(y, pi_star + BETA * (y - YN), color=C_S, lw=2)
ax.axvline(YN, color=C_S, lw=2, ls="--")
ax.text(5.65, pi_star + BETA * (5.6 - YN), "DAS (short run)", va="center", color=C_S)
ax.text(YN + 0.08, 6.0, "DAS (long run)", va="top", color=C_S)
guide(ax, YN, pi_star, r"$\hat{y}_n$", r"$\pi^{*}$")
ax.annotate("", xy=(YN + 0.25, 5.2), xytext=(4.9, pi_star + BETA * (4.9 - YN)),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.1, connectionstyle="arc3,rad=0.35"))
save(fig, "fig_das")

# DAD -----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6, 4))
axes(ax)
ax.plot(y, dad(G0), color=C_D, lw=2)
ax.plot(y, dad(G1), color=C_D, lw=2, alpha=0.45)
ax.axhline(PIF, color=MUTED, lw=1, ls="--")
ax.text(5.65, dad(G0)[-1], r"DAD$_0$", va="center", color=C_D)
ax.text(5.65, dad(G1)[-1], r"DAD$_1$", va="center", color=C_D, alpha=0.8)
ax.annotate("", xy=(2.75, PIF + THETA * (G1 - 2.75) - 0.05), xytext=(1.6, PIF + THETA * (G0 - 1.6) + 0.15),
            arrowprops=dict(arrowstyle="->", color=INK, lw=1))
ax.text(1.0, 5.6, r"$\uparrow \hat{g}_t$ or $\uparrow \pi_{ft}$", color=INK)
ax.text(0.33, PIF, r"$\pi_{ft}$", ha="right", va="center")
ax.text(5.65, PIF + 0.15, r"$\hat{g}_t=\hat{y}_t$", va="bottom", color=MUTED)
save(fig, "fig_dad")

# Equilibrium ---------------------------------------------------------------
pi1 = PIF + THETA * (G0 - YN)                       # initial long-run point
pi3 = PIF + THETA * (G1 - YN)                       # new long-run point
y2 = (PIF + THETA * G1 - pi1 + BETA * YN) / (BETA + THETA)   # SR: DAS0 meets DAD1
pi2 = pi1 + BETA * (y2 - YN)
fig, ax = plt.subplots(figsize=(6.5, 4.4))
axes(ax)
ax.plot(y, dad(G0), color=C_D, lw=2)
ax.plot(y, dad(G1), color=C_D, lw=2)
ax.plot(y, pi1 + BETA * (y - YN), color=C_S, lw=2)
ax.plot(y, pi3 + BETA * (y - YN), color=C_S, lw=2, alpha=0.45)
ax.axvline(YN, color=C_S, lw=2, ls="--")
for lab, yy, cc, al in ((r"DAD$_0$", dad(G0)[-1], C_D, 1), (r"DAD$_1$", dad(G1)[-1], C_D, 1)):
    ax.text(5.65, yy, lab, va="center", color=cc, alpha=al)
ax.text(1.0, pi1 + BETA * (1.0 - YN) - 0.35, r"DAS$_0$", color=C_S)
ax.text(1.6, pi3 + BETA * (1.6 - YN) - 0.4, r"DAS$_1$", color=C_S, alpha=0.8)
ax.text(YN + 0.08, 6.0, "DAS (long run)", va="top", color=C_S)
for (xx, yy, lab) in ((YN, pi1, "1"), (y2, pi2, "2"), (YN, pi3, "3")):
    ax.plot([xx], [yy], "o", color=INK, ms=5, zorder=5)
    ax.text(xx + 0.1, yy + 0.12, lab, color=INK)
arr = dict(arrowstyle="-|>", color=INK, lw=1.1)
ax.annotate("", xy=(1.55, PIF + THETA * (G1 - 1.55) - 0.08), xytext=(0.95, PIF + THETA * (G0 - 0.95) + 0.08), arrowprops=arr)
ax.annotate("", xy=(4.7, pi3 + BETA * (4.7 - YN) - 0.12), xytext=(5.05, pi1 + BETA * (5.05 - YN) + 0.12), arrowprops=arr)
path = dict(arrowstyle="-|>", color=INK, lw=1.3, ls="--", shrinkA=7, shrinkB=7)
ax.annotate("", xy=(y2, pi2), xytext=(YN, pi1), arrowprops=dict(path, connectionstyle="arc3,rad=0.45"))
ax.annotate("", xy=(YN, pi3), xytext=(y2, pi2), arrowprops=dict(path, connectionstyle="arc3,rad=0.45"))
guide(ax, YN, pi1, r"$\hat{y}_n$", r"$\pi^{*}$")
guide(ax, y2, pi2, r"$\hat{y}_2$", r"$\pi_2$")
guide(ax, YN, pi3, None, r"$\pi_3$")
save(fig, "fig_equilibrium")
print("written fig_das, fig_dad, fig_equilibrium")
