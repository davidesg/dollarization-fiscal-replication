"""
hj_lambda.py -- recursive first eigenvalue for the Hansen-Johansen (1999)
fluctuation test, from drvec's EXACT likelihood.

With exact ML there is no eigenvalue problem, but the rank-1 LR defines the
same object:  2 [L(r=1) - L(r=0)] = -T log(1 - lambda_1), so

    lambda_1(t) = 1 - exp(-2 [L1(t) - L0(t)] / T_t).

Hansen-Johansen transform: xi(t) = log(lambda_1(t) / (1 - lambda_1(t))).
Fluctuation statistic (unscaled): F = sup_t (T_t / T) |xi(t) - xi(T)|;
the scale is calibrated by bootstrap (hj_lambda_boot.py), not by the
asymptotic variance formula.

Model: main (G/Y | GAP), G/Y M1 and GAP m04 .pre, p = 4, case 2, alpha free
(the rank test's model).  Forward samples 2003Q1 .. t, t = 2010Q4 .. 2019Q4,
cut by trimming the GAP .pre exactly as theta_recursive.py does.
Writes hj_lambda.csv.
"""
import os, re, csv, math, subprocess
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "runs")
DRVEC = os.environ.get("DRVEC", "drvec-py")
GY = os.path.join(HERE, "..", "VECM_GAP_GY", "GY_M1.pre")
E0, E1 = (2010 - 2003) * 4 + 3, 67          # 2010Q4 .. 2019Q4 (0-based end index)


def rank_logl(out):
    """{r: logL} from the rank table of a -lrtest .out."""
    ll = {}
    for m in re.finditer(r"^\s+([0-9])\s+([0-9]+)\s+(-?\d+\.\d+)\s+-?\d+\.\d+\s+-?\d+\.\d+\s*$", out, re.M):
        ll.setdefault(int(m.group(1)), float(m.group(3)))
    return ll


def run(e):
    tag = f"hjl_{e}"
    gp = os.path.join(WORK, f"GAP_fwd_0_{e}_wx.pre")      # same trimmed GAP as theta_recursive
    subprocess.run([DRVEC, GY, gp, "4", "0", "0", "-case", "2", "-lrtest", "-name", tag],
                   cwd=WORK, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3600)
    ll = rank_logl(open(os.path.join(WORK, tag + ".out"), encoding="latin-1").read())
    return e, ll


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=int(os.environ.get("NJOBS", "4"))) as ex:
        res = dict(ex.map(run, range(E0, E1 + 1)))
    rows = []
    for e in range(E0, E1 + 1):
        ll = res[e]
        T = e + 1 - 1                            # observations of nabla Y used (one consumed)
        lr = 2 * (ll[1] - ll[0])
        lam = 1 - math.exp(-lr / T)
        rows.append(dict(end=e, T=T, L0=ll[0], L1=ll[1], LR=lr, lam=lam,
                         xi=math.log(lam / (1 - lam)) if 0 < lam < 1 else float("nan")))
    xiT, TT = rows[-1]["xi"], rows[-1]["T"]
    for r in rows:
        r["fluct"] = r["T"] / TT * abs(r["xi"] - xiT)
    with open(os.path.join(HERE, "hj_lambda.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    for r in rows:
        print(f"{2003 + r['end'] // 4}Q{r['end'] % 4 + 1}  T={r['T']:2d}  LR {r['LR']:6.2f}  "
              f"lambda {r['lam']:.4f}  xi {r['xi']:+.3f}  (t/T)|xi-xiT| {r['fluct']:.3f}")
    print("F = sup (t/T)|xi_t - xi_T| =", round(max(r["fluct"] for r in rows), 4))
