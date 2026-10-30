"""
plot_convergence.py -- the convergence of the price gap after dollarisation,
2002M1-2008M6, from the convergence model of Table 3 (models/RIPC/A).

  data   100 ln(PE/PU), monthly, with the PPP alignment of the VECM
  fitted mu + omega_0/(1 - delta_1 B) xi_t^{S,2002M2}: the level of the gap
         without the seasonal harmonics, the Nyquist term and the AR noise
  tau*   mu + omega_0/(1 - delta_1), the long-run gap

The transition is 78 % complete after 12 months and 95 % after 24, which is why
the quarterly sample (Figure 1) starts in 2003Q1.

Output: output/figures/convergence.{pdf,png}
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "output", "figures")
PRE = os.path.join(REPO, "models", "RIPC", "A", "RIPC_m02_tr_ar2.pre")


def read_pre(path):
    """The data, mu and the transition (omega_0, delta_1) of the fue file."""
    lines = open(path, encoding="latin-1").read().splitlines()
    i = next(k for k, l in enumerate(lines) if l.startswith("** Time series"))
    y = np.array([float(l) for l in lines[i + 1:] if l.strip()])
    j = next(k for k, l in enumerate(lines) if l.startswith("** Mean parameter"))
    mu = float(lines[j + 1].split()[0])
    # after the list of deterministic variables: one line per coefficient (the
    # step's omega_0 last), the line of denominator orders, then delta_1
    k = next(k for k, l in enumerate(lines) if l.strip().startswith("step 2 2002"))
    vals = [l for l in lines[k + 1:] if l.strip() and not l.startswith("**")]
    ndet = int(lines[next(n for n, l in enumerate(lines) if l.startswith("** Number of deterministic")) + 1])
    omega0 = float(vals[1 + ndet - 1].split()[0])      # vals[0]: numerator orders
    delta1 = float(vals[1 + ndet + 1].split()[0])
    return y, mu, omega0, delta1


y, mu, w0, d1 = read_pre(PRE)
gap = 100 * np.log(y)
t = pd.date_range("2002-01-01", periods=len(gap), freq="MS") + pd.Timedelta(days=14)
k = np.arange(len(gap)) - 1                     # months since the step (2002M2)
level = mu + np.where(k >= 0, w0 * (1 - d1 ** (k + 1)) / (1 - d1), 0.0)
tau = mu + w0 / (1 - d1)

C_GAP, C_FIT, MUTED, INK = "#c4572a", "#2a6fb0", "#777777", "#222222"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})
fig, ax = plt.subplots(figsize=(10, 4.2))
ax.plot(t, gap, color=C_GAP, lw=1.6, label="100 × ln(PE/PU), monthly")
ax.plot(t, level, color=C_FIT, lw=2.0, label=r"fitted level $\mu+\omega_0/(1-\delta_1B)\,\xi_t^{S}$")
ax.axhline(tau, color=MUTED, lw=0.9, ls="--")
ax.axhline(mu, color=MUTED, lw=0.9, ls=":")
ax.text(t[-1], tau + 0.4, rf"$\tau^*={tau:.1f}$", color=INK, ha="right", va="bottom", fontsize=9)
ax.text(t[-1], mu + 0.15, rf"$\mu={mu:.1f}$", color=INK, ha="right", va="bottom", fontsize=9)
for m, share in ((12, "78 %"), (24, "95 %")):    # the 12th and 24th month of the step (1 - delta^12, 1 - delta^24)
    ax.plot([t[m]], [level[m]], "o", color=C_FIT, ms=5, zorder=5)
    ax.annotate(f"{share} of the transition", (t[m], level[m]), xytext=(8, -16),
                textcoords="offset points", fontsize=8, color=INK)
ax.axvline(pd.Timestamp("2003-01-01"), color=MUTED, lw=0.8, ls=":")
ax.text(pd.Timestamp("2003-01-15"), -76.2, "quarterly\nsample starts",
        color=MUTED, fontsize=8, va="bottom")
ax.set_ylabel("100 × ln(PE/PU)")
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.legend(frameon=False, loc="upper left", fontsize=9)
fig.tight_layout()
os.makedirs(OUT, exist_ok=True)
for ext in ("pdf", "png"):
    fig.savefig(os.path.join(OUT, f"convergence.{ext}"), bbox_inches="tight", dpi=200)
print(f"written convergence; mu {mu:.2f}, omega0 {w0:.4f}, delta1 {d1:.4f}, tau* {tau:.2f}, "
      f"12m {1 - d1 ** 12:.3f}, 24m {1 - d1 ** 24:.3f}")
