"""
hj_beta.py -- Hansen-Johansen (1999) recursive test of beta constancy, as in
CATS (Juselius 2006, ch. 9): in every forward sample 2003Q1..t the LR of
H0: beta(t) = beta_T (the full-sample beta, theta_T = 0.386) inside the main
model (G/Y weakly exogenous), with beta free under H1.  Pointwise chi2(1).
LR = 2 [ logL(beta free) - logL(beta held, -fixb2row 1 -theta_T) ].
The free logL comes from theta_recursive.csv (same model, same sample).
"""
import os, re, csv, subprocess
from concurrent.futures import ThreadPoolExecutor
from scipy.stats import chi2
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "runs")
DRVEC = os.environ.get("DRVEC", "drvec-py")
GY = os.path.join(HERE, "..", "VECM_GAP_GY", "GY_M1.pre")
B2T = -0.386336
free = {int(r["end"]): r for r in csv.DictReader(open(os.path.join(HERE, "theta_recursive.csv")))
        if r["kind"] == "fwd" and r["wx"] == "1"}
def run(e):
    tag = f"hj_{e}"
    gp = os.path.join(WORK, f"GAP_fwd_0_{e}_wx.pre")
    subprocess.run([DRVEC, GY, gp, "4", "0", "1", "-case", "2", "-weakex", "1",
                    "-fixb2row", "1", str(B2T), "-name", tag], cwd=WORK,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1800)
    out = open(os.path.join(WORK, tag + ".out"), encoding="latin-1").read()
    ll = float(re.search(r"logelf\s+:\s+(-?\d+\.\d+)", out).group(1))
    return e, ll
with ThreadPoolExecutor(max_workers=int(os.environ.get("NJOBS", "3"))) as ex:
    res = dict(ex.map(run, sorted(free)))
rows = []
for e in sorted(free):
    lf = float(free[e]["logL"]); lr = 2 * (lf - res[e])
    rows.append(dict(end=e, n=e + 1, theta=float(free[e]["theta"]), logL_free=lf,
                     logL_held=res[e], LR=lr, p=chi2.sf(max(lr, 0), 1)))
with open(os.path.join(HERE, "hj_beta.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{2003 + r['end'] // 4}Q{r['end'] % 4 + 1}  n={r['n']:2d}  theta {r['theta']:.3f}  "
          f"LR {r['LR']:7.4f}  p {r['p']:.3f}  LR/3.84 {r['LR'] / 3.8415:.2f}")
print("max LR", max(r["LR"] for r in rows), " pointwise rejections at 5%:",
      sum(r["LR"] > 3.8415 for r in rows), "of", len(rows))
