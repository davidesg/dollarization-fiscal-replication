#!/usr/bin/env python3
"""Build the paper's LaTeX tables from the suite's models.

    python make_tables.py [uni uni2 ur rank vecm valid ...] [--out DIR] [--jobs N]

For every row in `registry.py`:

1. **Estimate the `.inp`** with art (`art.pipeline.estimar`: fue, exact ML,
   standard errors from the Hessian at the optimum). The fresh `.out` and
   `.pre` go to `build/`.
2. **Check the optimum against the adopted `.pre`** (the one the guion
   adopted): max |Δ| over every parameter. A row that does not reproduce
   is flagged in the report and in the table notes.
3. **Read the fresh `.out`** (parameters, s.e., covariance, Q, JB, σ) and run
   art's formal tests on the fitted model: Shin-Fuller (H0: AR unit root)
   and the DCD with an over-differencing witness (H0: θ = 1). Together
   they are art's pair for d against d + 1 at f = 0.

The multivariate tables (rank, vecm, valid) re-run drvec on the adopted
`.pre` files instead; see `vecm.py` and `vecm_registry.py`.

Outputs (in `--out`, default `output/tables/`):
  tab_<table>.tex     the table (deterministic seasonality throughout)
  <table>.json        every number, the checks and the software versions
  <table>_compare.md  suite against the values printed in the draft
"""
from __future__ import annotations

import argparse
import re
import json
import math
import os
import sys
import warnings

warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ROOT = os.path.join(REPO, "models")               # the models (same layout as the analysis tree)
BUILD = os.path.join(REPO, "build")
DEFAULT_OUT = os.path.join(REPO, "output", "tables")

sys.path.insert(0, HERE)
from registry import TABLES  # noqa: E402

TOL = 1e-4          # max |Δ| between the fresh optimum and the adopted .pre
BAND = 0.10         # quasi-cancellation band of the DCD witness, |1 − θ̂|


# ── estimation and extraction ───────────────────────────────────────────────

def _flat(m) -> list[float]:
    """Every parameter value of a fue model, in a fixed order."""
    v = []
    for itv in m.interventions:
        v += list(itv.omega) + list(itv.delta)
    for blk in (m.ar, m.ar_s, m.ma, m.ma_s):
        for f in blk:
            v += list(f)
    v += [f.coef for f in m.ar_f] + [f.coef for f in m.ma_f]
    if m.estimate_mu:
        v.append(m.mu)
    return [float(x) for x in v]


def _date(ts, at: int) -> str:
    y0, q0 = ts.start
    k = q0 - 1 + at
    return f"{y0 + k // ts.freq}Q{k % ts.freq + 1}"


def _seasonality(m) -> str:
    """f = 1 and f = 2, each deterministic (D), stochastic (S) or absent."""
    types = {i.type for i in m.interventions}
    out = []
    f1s, f2s = (m.ifadf[1], m.ifadf[2]) if len(m.ifadf) > 2 else (0, 0)
    for f, det, sto in ((1, {"cos", "sin"} & types, f1s), (2, {"alter"} & types, f2s)):
        out.append(f"f{f} S" if sto else f"f{f} D" if det else "")
    if m.ar_s:
        out.append(r"AR$_4$")
    return ", ".join(x for x in out if x) or "--"


SA_SOURCE = ("DEFL/GDPDUSA", "DEFL/PCEUSA")          # published seasonally adjusted only
SA_PART = ("DEFL/GAPGDPD", "DEFL/GAPPCE")            # ratio with a SA US component


def seas_cell(row: dict, f: dict) -> str:
    """How seasonality is treated: harmonics at f = 1, 2 (H), stochastic (S),
    a seasonal AR, or data adjusted at source."""
    s = f.get("seasonality") or "--"
    parts = []
    for tok in s.split(", "):
        if tok.startswith("f1 D"):
            parts.append("H$_1$")
        elif tok.startswith("f2 D"):
            parts.append("H$_2$")
        elif tok.endswith(" S"):
            parts.append(tok.split()[0].replace("f", "S$_") + "$")
        elif tok.startswith("AR$_4$"):
            parts.append(r"AR$_4$")
    cell = ", ".join(parts) or "--"
    if row["inp"].startswith(SA_SOURCE):
        cell = "SA$^{s}$"
    elif row["inp"].startswith(SA_PART):
        cell = r"US SA$^{s}$" if cell == "--" else cell + r", US SA$^{s}$"
    return cell


def _complex_ar2(phi1, phi2, cov):
    """Period and damping of a complex AR(2), delta-method s.e."""
    if phi2 >= 0 or phi1 ** 2 + 4 * phi2 >= 0:
        return None
    d = math.sqrt(-phi2)
    c = phi1 / (2 * d)
    w = math.acos(max(-1.0, min(1.0, c)))
    per = 2 * math.pi / w
    # gradients
    dd = (0.0, -0.5 / d)
    dc_dphi1 = 1 / (2 * d)
    dc_dphi2 = phi1 / (4 * d ** 3)          # ∂c/∂φ2 = φ1/(4 d³)
    dw = -1 / math.sqrt(1 - c * c)
    dper = tuple(-2 * math.pi / w ** 2 * dw * g for g in (dc_dphi1, dc_dphi2))

    def se(g):
        return math.sqrt(max(0.0, g[0] ** 2 * cov[0][0] + 2 * g[0] * g[1] * cov[0][1]
                             + g[1] ** 2 * cov[1][1]))
    return dict(period=per, period_se=se(dper), damping=d, damping_se=se(dd))


def _expand_ar(factors, cov):
    """Multiply the regular AR factors into one polynomial 1 − φ1 B − … .

    `factors` is a list of factors, each a list of parameters (idx, value).
    Returns [(φk, s.e.)] and the covariance of the φ's (delta method, numeric
    Jacobian), so that an AR(1)×AR(1) reads as the AR(2) it is.
    """
    import numpy as np
    flat = [p for f in factors for p in f]
    if not flat:
        return [], None
    x0 = np.array([p["value"] for p in flat])
    sizes = [len(f) for f in factors]

    def phis(x):
        poly, k = np.array([1.0]), 0
        for n in sizes:
            poly = np.convolve(poly, np.concatenate(([1.0], -x[k:k + n])))
            k += n
        return -poly[1:]
    h = 1e-6
    J = np.array([(phis(x0 + h * e) - phis(x0 - h * e)) / (2 * h)
                  for e in np.eye(len(x0))]).T
    C = np.array([[cov(a["idx"], b["idx"]) for b in flat] for a in flat])
    S = J @ C @ J.T
    v = phis(x0)
    return [(float(v[i]), float(math.sqrt(max(S[i, i], 0.0)))) for i in range(len(v))], S


def _sf_by_overfit(inp: str):
    """Shin-Fuller on an AR(p+1) overfit of a model with one AR factor whose
    only real root is negative; None when it does not apply."""
    import tempfile
    from art.pipeline import estimar
    from art.formal_tests import shin_fuller, shin_fuller_sobreajuste
    L = open(inp).read().split("\n")
    try:
        i = next(k for k, l in enumerate(L) if l.startswith("** Number and orders of regular AR"))
        nf, p = (int(x) for x in L[i + 1].split()[:2])
    except (StopIteration, ValueError):
        return None
    if nf != 1 or p < 1:
        return None
    L[i + 1] = f"1 {p + 1}"
    L.insert(i + 3 + p, "0.000000  1")
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, os.path.basename(inp))
        open(path, "w").write("\n".join(L))
        try:
            m2 = estimar(path)[1]
        except Exception:
            return None
        for test in (shin_fuller, lambda m: shin_fuller_sobreajuste(m).sf):
            try:
                s = test(m2)
                return dict(stat=s.phi_1u, c10=s.crit_10pct, c5=s.crit_5pct,
                            rejects=bool(s.stationary), overfit=True)
            except Exception:
                continue
    return None


def fit_row(row: dict, key: str = "inp") -> dict:
    import fue
    from art.pipeline import estimar
    from art.outfile import lee_texto_out, _estructura, _p_chi2
    from art.formal_tests import (shin_fuller, shin_fuller_sobreajuste,
                                  dcd_overdiff_regular, dcd_underdiff_regular)
    from art.identification import unit_root_tests

    inp = os.path.join(ROOT, row[key])
    stem = os.path.splitext(os.path.basename(inp))[0]
    ts, m = estimar(inp)
    os.makedirs(BUILD, exist_ok=True)
    out_path = os.path.join(BUILD, stem + ".out")
    pre_path = os.path.join(BUILD, stem + ".pre")
    m.write_out(out_path)
    m.write_pre(pre_path)

    # 2. the optimum against the adopted .pre
    adopted = row.get("pre") if key == "inp" else None
    adopted = os.path.join(ROOT, adopted) if adopted else os.path.splitext(inp)[0] + ".pre"
    ref = fue.load(adopted)[1]
    a, b = _flat(m), _flat(ref)
    maxdiff = (max(abs(x - y) for x, y in zip(a, b)) if len(a) == len(b) else float("inf"))

    # 3. the fresh .out
    txt = open(out_path, encoding="utf-8", errors="replace").read()
    r = lee_texto_out(txt)
    _, labels, _, lb, _, _ = _estructura(txt)
    params = [dict(idx=p.indice, label=labels.get(p.indice, p.bloque),
                   value=p.valor, se=p.se) for p in r.parametros]

    def cov(i, j):
        i, j = max(i, j), min(i, j)
        return r.covarianza[i - 1][j - 1] if r.covarianza else float("nan")

    regs = {}
    for p in params:
        if "[AR regular " in p["label"]:
            regs.setdefault(p["label"].split("[AR regular ")[1], []).append(p)
    phi, S = _expand_ar([regs[k] for k in sorted(regs)], cov)
    cplx = None
    if len(phi) == 2:                       # an AR(2): is it a cycle?
        cplx = _complex_ar2(phi[0][0], phi[1][0], S[:2, :2].tolist())
    # φ1..φ3 go in their columns; any other ARMA term goes to a table note
    other = [p for p in params if p["label"][0] in "φΦθΘ" and "[AR regular " not in p["label"]]
    other += [dict(label=f"φ{k + 1} [AR regular]", value=v, se=e)
              for k, (v, e) in enumerate(phi[3:], start=3)]
    phi = phi[:3]

    itvs = []
    for itv in m.interventions:
        if itv.type in ("step", "impulse"):
            itvs.append(dict(type=itv.type, date=_date(ts, itv.at),
                             n=len(itv.omega) + len(itv.delta),
                             omega=list(itv.omega), delta=list(itv.delta)))

    # standardized residuals by date, for the intervention table
    from fue.diagnostics import residuals_start
    e = m.residuals
    e = list(getattr(e, "values", None) if getattr(e, "values", None) is not None else e.data)
    y0, q0 = residuals_start(m)
    resid = {f"{y0 + (q0 - 1 + k) // ts.freq}Q{(q0 - 1 + k) % ts.freq + 1}": float(v) / r.sigma
             for k, v in enumerate(e)}

    u1 = 2 ** (m.ifadf[1] + m.ifadf[2]) if len(m.ifadf) > 2 else 1
    mu = next((p for p in params if p["label"] == "μ"), None)
    mean = (dict(value=mu["value"] / u1, se=mu["se"] / u1) if mu else None)

    q = next((x for x in lb if x[0] == 15), lb[-1] if lb else None)
    qd = dict(lag=q[0], stat=q[1], df=q[2], p=_p_chi2(q[1], q[2])) if q else None
    jb = r.residuos.jarque_bera

    sf = None
    try:
        s = shin_fuller(m)
        sf = dict(stat=s.phi_1u, c10=s.crit_10pct, c5=s.crit_5pct,
                  rejects=bool(s.stationary), overfit=False)
    except Exception as e0:
        # art declines SF when the AR has no positive real root (a negative
        # root says nothing about d) or there is no free AR: then the DCD
        # decides at f = 0. Only an all-complex AR is recovered by overfit.
        try:
            so = shin_fuller_sobreajuste(m)
            s = so.sf
            sf = dict(stat=s.phi_1u, c10=s.crit_10pct, c5=s.crit_5pct,
                      rejects=bool(s.stationary), overfit=True)
        except Exception:
            # a single negative real root: overfit the AR by one order (as in
            # the guiones, e.g. REV); the larger AR then gives a positive real
            # root (SF directly) or complex roots (SF on a further overfit)
            sf = _sf_by_overfit(inp) or dict(na=str(e0))
    dcd = None
    try:
        o = dcd_overdiff_regular(m)
        dcd = dict(stat=o.lr, theta=o.coef_free, r10=bool(o.rejects_10pct),
                   r5=bool(o.rejects_5pct))
    except Exception as e:
        dcd = dict(error=str(e))

    # the d − 1 side: was the last difference needed? (None when d = 0)
    under = None
    try:
        u = dcd_underdiff_regular(m)
        if u is not None:
            under = dict(stat=u.lr, theta=u.coef_free, r10=bool(u.rejects_10pct),
                         r5=bool(u.rejects_5pct))
    except Exception as e:
        under = dict(error=str(e))
    # identification: ADF and KPSS on the transformed series, d = 0 and 1
    ur = [dict(d=x.d, adf_stat=x.adf_stat, adf_p=x.adf_pvalue,
               kpss_stat=x.kpss_stat, kpss_p=x.kpss_pvalue, verdict=x.verdict)
          for x in unit_root_tests(ts, lam=float(m.boxlam), max_d=1)]

    return dict(model=row[key], adopted_pre=os.path.relpath(adopted, ROOT),
                under=under, ur=ur,
                reproduces=maxdiff < TOL, maxdiff=maxdiff,
                loglik=float(m.loglik), d=int(m.d), D=int(m.D), lam=float(m.boxlam),
                seasonality=_seasonality(m), phi=phi, complex=cplx, other=other,
                interventions=itvs, resid=resid, mean=mean, sigma=r.sigma, q=qd, jb=jb,
                jb_p=_p_chi2(jb, 2) if jb is not None else None, sf=sf, dcd=dcd,
                params=params)


# ── LaTeX ──────────────────────────────────────────────────────────────────

def f2(x, nd=2):
    if x is None:
        return "--"
    s = f"{x:.{nd}f}"
    if float(s) == 0:
        s = s.lstrip("-")                      # no "-0.0"
    return s.replace("-", "$-$")


def star(stat, p=None, c10=None, c5=None):
    if p is not None:
        return "$^{**}$" if p < 0.05 else "$^{*}$" if p < 0.10 else ""
    if c5 is not None and stat >= c5:
        return "$^{**}$"
    if c10 is not None and stat >= c10:
        return "$^{*}$"
    return ""


_OTHER = {"AR regular": r"\phi", "MA regular 1": r"\theta", "AR anual 1": r"\Phi_4", "MA anual 1": r"\Theta_4",
          "MA f-fijo 1": r"\theta_{f}", "AR regular 2": r"\phi'"}


def other_note(name, f):
    """ARMA terms with no column, for the table notes."""
    out = []
    for p in f["other"]:
        lab, blk = p["label"].split(" [")
        blk = blk.rstrip("]")
        sym = _OTHER.get(blk, lab)
        out.append(f"${sym}$ = {f2(p['value'])} ({f2(p['se'])})")
    return f"{name}: " + ", ".join(out) if out else ""


def itv_cell(f):
    if not f["interventions"]:
        return "--"
    tag = {"step": "S", "impulse": "I"}
    return "; ".join(f"{tag[i['type']]} {i['date'].replace('Q', ':')}"
                     + (f"$\\times${i['n']}" if i["n"] > 1 else "")
                     for i in f["interventions"])


NCOL = 13


def latex(spec: dict, fits: dict) -> str:
    L = []
    cap, lab = spec["caption"], spec["label"]
    L += [r"% Generated by Python/art_drvec/tables/make_tables.py -- do not edit.",
          r"\begin{table}\caption{" + cap + r"}\label{" + lab + "}",
          r"\begin{singlespace}\begin{scriptsize}\begin{center}",
          r"\setlength{\tabcolsep}{3pt}  % needs graphicx (\resizebox)",
          r"\resizebox{\textwidth}{!}{\begin{tabular}{lcccccccccccc}",
          r"\multicolumn{13}{c}{(Variables in logs, $100\ln$)}\vspace{.1in} \\ \thickhline",
          r"Variable & \multicolumn{3}{c}{AR} & Intervention & Seasonal & $I(d)$ "
          r"& Mean & SF & \multicolumn{3}{c}{Error ($\epsilon_t$)} & DCD \\",
          r"(Mnemonic) & $\hat\phi_1$ & $\hat\phi_2$ & $\hat\phi_3$ & at time & terms & $d$ "
          r"& (s.e.) & H$_0$: & $Q(15)$ & JB & $\hat\sigma_\epsilon$ & H$_0$: \\",
          r" & (s.e.) & (s.e.) & (s.e.) & & & & (\%) & $\phi=1$ & & $\chi^2(2)$ "
          r"& (\%) & $\vartheta=1$ \\ \thickhline"]
    bad, extra = [], []
    any_complex = False
    for k_, (title, rows) in enumerate(spec["groups"]):
        if not title.startswith("Panel"):
            t_ = re.sub(r"^Univariate Models? for (the )?", "", title)
            title = f"Panel {chr(65 + k_)}. {t_[:1].upper() + t_[1:]}"
        L.append(r"\multicolumn{13}{l}{" + title + r"}\vspace{.05in} \\ \hline")
        for row in rows:
            k = row["name"] + "|" + row["mnem"]
            f = fits[k]["main"]
            if not f["reproduces"]:
                bad.append(row["name"])
            ph = f["phi"] + [(None, None)] * (3 - len(f["phi"]))
            note = other_note(row["name"], f)
            if note:
                extra.append(note)
            sf = f["sf"] or {}
            sfc = (r"n.a.$^\S$" if "na" in sf else "--" if "stat" not in sf else
                   f2(sf["stat"], 1) + star(sf["stat"], c10=sf["c10"], c5=sf["c5"])
                   + (r"$^\dagger$" if sf.get("overfit") else ""))
            dc = f["dcd"] or {}
            dcc = ("--" if "stat" not in dc else f2(dc["stat"], 1)
                   + ("$^{**}$" if dc["r5"] else "$^{*}$" if dc["r10"] else ""))
            if dc.get("r5"):                   # the guiones decide at 5 %
                # why d is kept although the DCD rejects: in the band, or PE
                dcc += (r"$^{a}$" if dc["theta"] >= 1 - BAND else
                        r"$^{b}$" if row.get("d_rule") == "PE" else r"$^{?}$")
            q = f["q"]
            qc = f2(q["stat"]) + star(q["stat"], p=q["p"]) if q else "--"
            jbc = f2(f["jb"]) + star(f["jb"], p=f["jb_p"]) if f["jb"] is not None else "--"
            mean = f["mean"]
            name = (row["name"] + (r"$^\ddagger$" if not f["reproduces"] else "")
                    + (r"$^{c}$" if note else ""))
            L.append(f"{name} & {f2(ph[0][0])} & {f2(ph[1][0])} & {f2(ph[2][0])} & "
                     f"{itv_cell(f)} & {seas_cell(row, f)} & {f['d']} & "
                     f"{f2(mean['value']) if mean else '--'} & {sfc} & {qc} & {jbc} & "
                     f"{f2(f['sigma'])} & {dcc} \\\\")
            se = [f"({f2(e)})" if e is not None else "" for _, e in ph]
            L.append(f"$({row['mnem']})$ & {se[0]} & {se[1]} & {se[2]} & & & & "
                     f"{'(' + f2(mean['se']) + ')' if mean else ''} & & & & & \\\\")
            if f["complex"]:
                any_complex = True
                c = f["complex"]
                tail = " &" * (NCOL - 3) + r" \\"
                L.append(r"\cline{2-3}")
                L.append(r" & \multicolumn{2}{c}{$\hat p = " + f2(c["period"], 1)
                         + " (" + f2(c["period_se"], 1) + r")$}" + tail)
                L.append(r" & \multicolumn{2}{c}{$\hat d = " + f2(c["damping"])
                         + " (" + f2(c["damping_se"]) + r")$}" + tail)
        L.append(r"\hline")
    if L[-1] == r"\hline":
        L.pop()
    if spec["label"] == "tab:uni2":
        L += [r"\thickhline\end{tabular}}\end{center}\end{scriptsize}",
              r"\begin{footnotesize}\textbf{Notes:} As in Table~\ref{tab:uni}."
              + (r" $\hat p$, $\hat d$: period and damping of a complex AR(2) (delta method)."
                 if any_complex else "")
              + (r" $^{c}$ Further ARMA terms: " + "; ".join(extra) + "." if extra else "")
              + (r" $^\ddagger$ does not reproduce the adopted optimum." if bad else ""),
              r"\end{footnotesize}\end{singlespace}\end{table}", ""]
        return "\n".join(L)
    L += [r"\thickhline\end{tabular}}\end{center}\end{scriptsize}",
          r"\begin{footnotesize}\textbf{Notes:} Exact ML; data not seasonally adjusted (SA$^{s}$: published SA). "
          r"H$_1$, H$_2$: seasonal harmonics; S, I: step, impulse, date year:quarter ($\times k$ weights). "
          r"Mean: drift, \% per quarter, if $d=1$. SF, DCD: Section~\ref{subsec:univariate} and Table~\ref{tab:ur}. "
          r"$^{*}$, $^{**}$: rejection at 10\,\%, 5\,\%."
          + (r" $\hat p$, $\hat d$: period and damping of a complex AR(2)." if any_complex else "")
          + (r" $^{c}$ Further ARMA terms: " + "; ".join(extra) + "." if extra else "")
          + (r" $^\ddagger$ does not reproduce the adopted optimum." if bad else ""),
          r"\end{footnotesize}\end{singlespace}\end{table}", ""]
    return "\n".join(L)


def latex_ur(spec: dict, fits: dict) -> str:
    """The integration-order table: identification and the formal pair."""
    n = 10
    L = [r"% Generated by Python/art_drvec/tables/make_tables.py -- do not edit.",
         r"\begin{table}\caption{" + spec["caption"] + r"}\label{" + spec["label"] + "}",
         r"\begin{singlespace}\begin{footnotesize}\begin{center}",
         r"\setlength{\tabcolsep}{4pt}\begin{tabular}{@{}lcccccccc@{}}",
         r"\thickhline",
         r" & \multicolumn{4}{c}{Identification [$p$]} "
         r"& \multicolumn{3}{c}{Formal tests on the model} & \\",
         r" & \multicolumn{2}{c}{$d=0$} & \multicolumn{2}{c}{$d=1$} "
         r"& $d-1$ side & \multicolumn{2}{c}{$d+1$ side} & \\",
         r"Variable & ADF & KPSS & ADF & KPSS & DCD$^{-}$ & SF & DCD$^{+}$ & $d$ \\",
         r" & & & & & H$_0$: $\vartheta=1$ & H$_0$: $\phi=1$ & H$_0$: $\vartheta=1$ & \\ \thickhline"]
    bad = []
    for title, rows in spec["groups"]:
        L.append(r"\multicolumn{" + str(n - 1) + r"}{l}{" + title + r"} \\ \hline")
        for row in rows:
            f = fits[row["name"] + "|" + row["mnem"]]["main"]
            if not f["reproduces"]:
                bad.append(row["name"])
            u = {x["d"]: x for x in f["ur"]}

            def pv(x, k):
                return f2(x[k], 3) if x else "--"
            un = f["under"] or {}
            unc = ("--" if "stat" not in un else f2(un["stat"], 1)
                   + ("$^{**}$" if un["r5"] else "$^{*}$" if un["r10"] else ""))
            sf = f["sf"] or {}
            sfc = (r"n.a.$^\S$" if "na" in sf else "--" if "stat" not in sf else
                   f2(sf["stat"], 1) + star(sf["stat"], c10=sf["c10"], c5=sf["c5"])
                   + (r"$^\dagger$" if sf.get("overfit") else ""))
            dc = f["dcd"] or {}
            dcc = ("--" if "stat" not in dc else f2(dc["stat"], 1)
                   + ("$^{**}$" if dc["r5"] else "$^{*}$" if dc["r10"] else ""))
            if dc.get("r5"):
                dcc += (r"$^{a}$" if dc["theta"] >= 1 - BAND else
                        r"$^{b}$" if row.get("d_rule") == "PE" else r"$^{?}$")
            name = row["name"] + (r"$^\ddagger$" if not f["reproduces"] else "")
            L.append(f"{name} & {pv(u.get(0), 'adf_p')} & {pv(u.get(0), 'kpss_p')} & "
                     f"{pv(u.get(1), 'adf_p')} & {pv(u.get(1), 'kpss_p')} & "
                     f"{unc} & {sfc} & {dcc} & {f['d']} \\\\")
        L.append(r"\hline")
    if L[-1] == r"\hline":
        L.pop()
    if spec["label"] == "tab:ur_app":
        L += [r"\thickhline\end{tabular}\end{center}\end{footnotesize}",
              r"\begin{footnotesize}\textbf{Notes:} As in Table~\ref{tab:ur}."
              + (r" $^\ddagger$ does not reproduce the adopted optimum." if bad else ""),
              r"\end{footnotesize}\end{singlespace}\end{table}", ""]
        return "\n".join(L)
    L += [r"\thickhline\end{tabular}\end{center}\end{footnotesize}",
          r"\begin{footnotesize}\textbf{Notes:} ADF, KPSS: $p$-values on the log series, constant only. "
          r"Formal tests on the estimated univariate models (Section~\ref{subsec:univariate}): DCD$^{-}$, unit MA "
          r"root of the model in differences; SF, unit AR root; DCD$^{+}$, unit MA root after one more difference. "
          r"$^\dagger$: SF on an AR overfit; n.a.: SF does not apply; $^{a}$, $^{b}$: $d$ kept although DCD$^{+}$ "
          r"rejects (quasi-cancellation; 2008 step). $^{*}$, $^{**}$: rejection at 10\,\%, 5\,\%."
          + (r" $^\ddagger$ does not reproduce the adopted optimum." if bad else ""),
          r"\end{footnotesize}\end{singlespace}\end{table}", ""]
    return "\n".join(L)


# ── comparison with the draft ───────────────────────────────────────────────

def compare_md(spec, fits) -> str:
    L = [f"# {spec['label']}: suite against the draft", "",
         "Suite = re-estimated from the `.inp`; paper = the draft's table. "
         "`ok` = the fresh optimum equals the adopted `.pre` (max |Δ| < 1e-4).", "",
         "| row | model | ok | φ₁ | φ₂ | d | mean | SF | Q | JB | σ | DCD |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]

    def pair(s, p):
        s = "--" if s is None else f"{s:.2f}"
        p = "--" if p is None else f"{p:.2f}"
        return f"{s} / {p}"
    for title, rows in spec["groups"]:
        for row in rows:
            k = row["name"] + "|" + row["mnem"]
            for tag in ("main", "addon"):
                if tag not in fits[k]:
                    continue
                f = fits[k][tag]
                pp = row.get("paper", {})
                ph = f["phi"] + [(None, None)] * 2
                L.append(
                    f"| {row['name']}{' (addon)' if tag == 'addon' else ''} | `{os.path.basename(f['model'])}` "
                    f"| {'✓' if f['reproduces'] else '✗ %.1e' % f['maxdiff']} "
                    f"| {pair(ph[0][0], pp.get('phi1'))} | {pair(ph[1][0], pp.get('phi2'))} "
                    f"| {f['d']} / {pp.get('d', '--')} "
                    f"| {pair(f['mean']['value'] if f['mean'] else None, pp.get('mean'))} "
                    f"| {pair((f['sf'] or {}).get('stat'), pp.get('sf'))} "
                    f"| {pair(f['q']['stat'] if f['q'] else None, pp.get('q'))} "
                    f"| {pair(f['jb'], pp.get('jb'))} | {pair(f['sigma'], pp.get('sigma'))} "
                    f"| {pair((f['dcd'] or {}).get('stat'), pp.get('dcd'))} |")
    return "\n".join(L) + "\n"


def _qadd(q: str, k: int) -> str:
    y, n = int(q[:4]), int(q[-1]) - 1 + k
    return f"{y + n // 4}Q{n % 4 + 1}"


def itv_effects(f) -> dict:
    """Effect of each intervention on the level, quarter by quarter:
    nu_0 = omega_0, nu_j = -omega_j (Box-Jenkins signs, as fue)."""
    out = {}
    for i in f["interventions"]:
        nu = [i["omega"][0]] + [-w for w in i["omega"][1:]]
        for j, v in enumerate(nu):
            out[_qadd(i["date"], j)] = ({"step": "S", "impulse": "I"}[i["type"]], v)
    return out


def latex_itv(spec: dict, fits: dict) -> str:
    """Interventions and signs of the innovations around them, as in
    Dobado-Gonzalez, Garcia-Hiernaux and Guerrero (2012, Tables 1A-1B)."""
    Q = spec["quarters"]
    n = len(Q) + 1
    L = [r"% Generated by Python/art_drvec/tables/make_tables.py -- do not edit.",
         r"\begin{table}\caption{" + spec["caption"] + r"}\label{" + spec["label"] + "}",
         r"\begin{singlespace}\begin{footnotesize}\begin{center}",
         r"\setlength{\tabcolsep}{4pt}\begin{tabular}{@{}l" + "c" * len(Q) + "@{}}",
         r"\thickhline",
         r" & " + " & ".join(r"\multicolumn{" + str(k) + r"}{c}{" + ev + "}"
                            for ev, k in spec["events"]) + r" \\",
         r"Series & " + " & ".join(q.replace("Q", ":") for q in Q) + r" \\ \thickhline"]
    mark = {2: r"$+\,+$", 1: r"$+$", -1: r"$-$", -2: r"$-\,-$"}
    bad = []
    for title, rows in spec["groups"]:
        L.append(r"\multicolumn{" + str(n) + r"}{l}{" + title + r"} \\ \hline")
        for row in rows:
            f = fits[row["name"] + "|" + row["mnem"]]["main"]
            if not f["reproduces"]:
                bad.append(row["label"])
            eff = itv_effects(f)
            cells = []
            for q in Q:
                if q in eff:
                    t, v = eff[q]
                    cells.append(t + ("$+$" if v > 0 else "") + f2(v, 1))
                else:
                    z = f["resid"].get(q)
                    k = 0 if z is None or abs(z) < 1 else (2 if z >= 2 else 1 if z > 0 else
                                                           -2 if z <= -2 else -1)
                    cells.append(mark.get(k, ""))
            name = row["label"] + (r"$^\ddagger$" if not f["reproduces"] else "")
            L.append(name + " & " + " & ".join(cells) + r" \\")
    L += [r"\thickhline", r"\end{tabular}\end{center}",
          r"\textbf{Notes:} " + spec["notes"]
          + (r" $^\ddagger$: does not reproduce its adopted model." if bad else ""),
          r"\end{footnotesize}\end{singlespace}", r"\end{table}", ""]
    return "\n".join(L)


def main_vecm(names, out, jobs):
    """The multivariate tables: run (or reuse) every drvec run they need."""
    import vecm
    import vecm_registry as VR
    need = list(dict.fromkeys(n for t in names for n in vecm.needed(VR.TABLES[t])))
    outs = vecm.run_all(need, VR.RUNS, ROOT, BUILD, jobs=jobs)
    fits = {n: vecm.parse(p) for n, p in outs.items()}
    for t in names:
        spec = VR.TABLES[t]
        with open(os.path.join(out, f"tab_{t}.tex"), "w") as fh:
            fh.write(vecm.RENDER[spec["kind"]](spec, fits))
        with open(os.path.join(out, f"{t}.json"), "w") as fh:
            json.dump({n: dict(fits[n], args=VR.RUNS[n]) for n in vecm.needed(spec)},
                      fh, indent=1, ensure_ascii=False)
        print(f"[{t}] written to {out}")


def main():
    import vecm_registry as VR
    ap = argparse.ArgumentParser()
    ap.add_argument("tables", nargs="*", default=list(TABLES) + list(VR.TABLES))
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--jobs", type=int, default=6, help="parallel drvec runs")
    a = ap.parse_args()
    import art
    import fue
    os.makedirs(a.out, exist_ok=True)
    multi = [t for t in a.tables if t in VR.TABLES]
    if multi:
        main_vecm(multi, a.out, a.jobs)
    for name in (t for t in a.tables if t in TABLES):
        spec = TABLES[name]
        fits = {}
        for _, rows in spec["groups"]:
            for row in rows:
                k = row["name"] + "|" + row["mnem"]
                print(f"[{name}] {row['name']:<12} {row['inp']}", flush=True)
                fits[k] = {"main": fit_row(row)}
                if row.get("addon"):
                    fits[k]["addon"] = fit_row(row, "addon")
        meta = dict(art=getattr(art, "__version__", "?"), fue=getattr(fue, "__version__", "?"))
        with open(os.path.join(a.out, f"{name}.json"), "w") as fh:
            json.dump(dict(meta=meta, rows=fits), fh, indent=1, ensure_ascii=False)
        render = {"ur": latex_ur, "itv": latex_itv}.get(spec.get("kind"), latex)
        with open(os.path.join(a.out, f"tab_{name}.tex"), "w") as fh:
            fh.write(render(spec, fits))
        if spec.get("kind") not in ("ur", "itv"):
            with open(os.path.join(a.out, f"{name}_compare.md"), "w") as fh:
                fh.write(compare_md(spec, fits))
        nbad = sum(not v[t]["reproduces"] for v in fits.values() for t in v)
        print(f"[{name}] written to {a.out}; rows not reproducing: {nbad}")


if __name__ == "__main__":
    main()
