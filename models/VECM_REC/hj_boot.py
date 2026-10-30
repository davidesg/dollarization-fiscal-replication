"""
hj_boot.py -- Hansen-Johansen (1999) fluctuation test of the first eigenvalue,
calibrated by bootstrap.

Data: the DETERMINISTIC-FREE system of the main model, exported by drvec
(-writeinp): component 1 = nabla G/Y, component 2 = W = GAP - theta*G/Y with the
free full-sample theta (0.37189).  Levels are rebuilt as G/Y = cumsum(nabla G/Y)
and GAP = W + theta*G/Y (the origin of G/Y is irrelevant: it shifts GAP by
theta*c and leaves W unchanged).  Sample 2003Q2..2019Q4 (67 levels).

Test (Hansen and Johansen 1999, sec. 3; CATS's recursive eigenvalue test): in
the conditional (Johansen) VECM, case 2 (constant restricted to the
cointegrating space), k = 4 lags in levels, recursive first eigenvalue
lambda_1(t) on samples 2003Q2..t, t = 2010Q4..2019Q4;
xi(t) = log(lambda/(1 - lambda));  F = sup_t (T_t/T) |xi(t) - xi(T)|.
Null distribution of F by parametric bootstrap from the full-sample r = 1
VECM (iid resampling of the centred residuals and, as a check, wild
Rademacher), each replicate refitted recursively exactly as the data.

Also compared: the drvec exact-ML path of lambda_1(t) (hj_lambda.csv).
Writes hj_boot.csv, hj_boot_paths.csv and the figure fig_hj_lambda.
"""
import os, sys, csv
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "runs")
THETA = 0.37189
K = 4                      # lags in levels (p of the VECM)
B = int(os.environ.get("B", "999"))
rng = np.random.default_rng(20261010)


def read_comp(path):
    txt = open(path).read().split("Time series (stochastic and non-standard deterministic variables):")[1]
    return np.array([float(v) for v in txt.split()])


dgy = read_comp(os.path.join(RUNS, "hjfull_inp.1.inp"))
w = read_comp(os.path.join(RUNS, "hjfull_inp.2.inp"))
gy = np.cumsum(dgy)
gap = w + THETA * gy
Y = np.column_stack([gy, gap])            # 67 x 2, 2003Q2..2019Q4
N = len(Y)                                 # 67
# end indices: obs index in Y (0 = 2003Q2); 2010Q4 is quarter (2010-2003)*4+3 = 31 of the
# 68-obs calendar, i.e. index 30 here
ENDS = list(range(30, N))


def lags(X, k):
    return np.column_stack([X[k - i:len(X) - i] for i in range(1, k + 1)]) if k else np.zeros((len(X) - k, 0))


def johansen(Y, k):
    """First eigenvalue (case 2: restricted constant) and full r=1 fit pieces."""
    dY = np.diff(Y, axis=0)
    Z0 = dY[k - 1:]                                         # nabla Y_t
    Z1 = np.column_stack([Y[k - 1:-1], np.ones(len(Z0))])   # Y_{t-1}, 1
    Z2 = lags(dY, k - 1)[0:] if k > 1 else np.zeros((len(Z0), 0))
    if k > 1:
        Z2 = np.column_stack([dY[k - 1 - i:len(dY) - i] for i in range(1, k)])
    T = len(Z0)
    def res(A):
        if Z2.shape[1] == 0:
            return A
        b, *_ = np.linalg.lstsq(Z2, A, rcond=None)
        return A - Z2 @ b
    R0, R1 = res(Z0), res(Z1)
    S00, S11, S01 = R0.T @ R0 / T, R1.T @ R1 / T, R0.T @ R1 / T
    M = np.linalg.solve(S11, S01.T) @ np.linalg.solve(S00, S01)
    val, vec = np.linalg.eig(M)
    i = np.argmax(val.real)
    lam = float(val.real[i])
    beta = vec[:, i].real
    beta = beta / np.sqrt(beta @ S11 @ beta)
    alpha = S01 @ beta
    return lam, T, dict(beta=beta, alpha=alpha, Z2=Z2, Z0=Z0, Z1=Z1, R0=R0, R1=R1)


def path(Y):
    out = []
    for e in ENDS:
        lam, T, _ = johansen(Y[:e + 1], K)
        out.append((T, lam, np.log(lam / (1 - lam))))
    TT, xiT = out[-1][0], out[-1][2]
    F = max(T / TT * abs(xi - xiT) for T, _, xi in out)
    return F, out


def fit_r1(Y):
    """OLS r = 1 VECM with restricted constant: returns a simulator."""
    lam, T, d = johansen(Y, K)
    ec = d["Z1"] @ d["beta"]
    X = np.column_stack([ec, d["Z2"]])
    coef, *_ = np.linalg.lstsq(X, d["Z0"], rcond=None)
    E = d["Z0"] - X @ coef
    return d["beta"], coef, E


def simulate(Y, beta, coef, E, mode):
    T0 = K                                          # initial values: first K levels
    n = len(Y)
    Ys = np.zeros_like(Y)
    Ys[:T0] = Y[:T0]
    Ec = E - E.mean(axis=0)
    for t in range(T0, n):
        z1 = np.append(Ys[t - 1], 1.0)
        x = [z1 @ beta] + [v for i in range(1, K) for v in (Ys[t - i] - Ys[t - i - 1])]
        if mode == "iid":
            u = Ec[rng.integers(len(Ec))]
        else:                                       # wild Rademacher, same date
            u = Ec[t - T0] * rng.choice([-1.0, 1.0])
        Ys[t] = Ys[t - 1] + np.array(x) @ coef + u
    return Ys


if __name__ == "__main__":
    F_obs, pth = path(Y)
    beta, coef, E = fit_r1(Y)
    rows = [dict(end=e, T=T, lam=lam, xi=xi) for e, (T, lam, xi) in zip(ENDS, pth)]
    print(f"OLS (Johansen) path: lambda_1(T) = {pth[-1][1]:.4f}, F = {F_obs:.4f}")
    res = {}
    for mode in ("iid", "wild"):
        Fs = []
        for b in range(B):
            Fb, _ = path(simulate(Y, beta, coef, E, mode))
            Fs.append(Fb)
        Fs = np.array(Fs)
        res[mode] = Fs
        print(f"  bootstrap {mode:4s} B={B}: p = {np.mean(Fs >= F_obs):.3f}; "
              f"critical 90/95/99 % = {np.quantile(Fs, [.9, .95, .99]).round(3)}")
    with open(os.path.join(HERE, "hj_boot.csv"), "w", newline="") as f:
        wr = csv.writer(f); wr.writerow(["mode", "F_obs", "p", "q90", "q95", "q99", "B"])
        for mode, Fs in res.items():
            wr.writerow([mode, F_obs, np.mean(Fs >= F_obs), *np.quantile(Fs, [.9, .95, .99]), B])
    with open(os.path.join(HERE, "hj_boot_paths.csv"), "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)
    np.save(os.path.join(HERE, "hj_boot_F.npy"), np.vstack([res["iid"], res["wild"]]))
