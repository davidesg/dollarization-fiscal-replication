"""drvec runs for the multivariate tables: execution with a cache, parsing,
and the LaTeX of tab:rank, tab:vecm and tab:validation.

Every run is re-executed from the adopted `.pre` files (copied to
`build/drvec/<run>/`). A run is skipped only when its key -- a hash of the
input files, the arguments and the drvec binary -- matches the one stored
next to its `.out`, so a bootstrap is recomputed whenever anything changes.
"""
from __future__ import annotations

import hashlib
import math
import os
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor

# reference: atsw-gui tag drvec-v0.12, built by build_drvec_ref.sh
DRVEC = os.environ.get("DRVEC") or shutil.which("drvec-py") or "drvec-py"


def _engine_id() -> str:
    """The engine in the cache key: the version banner of drvec-py."""
    global _ENGINE
    if _ENGINE is None:
        r = subprocess.run([DRVEC, "--version"], capture_output=True, text=True)
        _ENGINE = r.stdout
    return _ENGINE


_ENGINE = None


# ── running ────────────────────────────────────────────────────────────────

def _inputs(args: str, src: str) -> list[str]:
    """The files an argument string reads: the .pre and any -xlink / -xpre file."""
    toks = args.split()
    files = [t for t in toks if t.endswith(".pre")]
    for flag in ("-xlink", "-xpre"):
        if flag in toks:
            files.append(toks[toks.index(flag) + 1])
    return [f for f in dict.fromkeys(files) if os.path.exists(os.path.join(src, f))]


def _key(src: str, args: str) -> str:
    h = hashlib.sha256(args.encode())
    for f in _inputs(args, src):
        h.update(f.encode())
        h.update(open(os.path.join(src, f), "rb").read())
    h.update(_engine_id().encode())
    return h.hexdigest()


def run(name: str, src: str, args: str, build: str) -> str:
    """Run drvec for one entry (or reuse a cached run); returns the .out path."""
    work = os.path.join(build, "drvec", name)
    out = os.path.join(work, name + ".out")
    keyf = os.path.join(work, name + ".key")
    key = _key(src, args)
    if os.path.exists(out) and os.path.exists(keyf) and open(keyf).read() == key:
        return out
    os.makedirs(work, exist_ok=True)
    for f in _inputs(args, src):
        shutil.copy(os.path.join(src, f), work)
    with open(os.path.join(work, name + ".log"), "w") as log:
        subprocess.run([DRVEC, *args.split(), "-name", name], cwd=work,
                       stdout=log, stderr=subprocess.STDOUT, check=False)
    if not os.path.exists(out):
        raise RuntimeError(f"drvec produced no {name}.out; see {work}/{name}.log")
    with open(keyf, "w") as fh:
        fh.write(key)
    return out


def run_all(names, runs, root: str, build: str, jobs: int = 6) -> dict:
    """Run the named entries in parallel (bootstraps are the slow ones)."""
    def one(n):
        d, a = runs[n]
        print(f"[drvec] {n:<10} {d}: {a}", flush=True)
        return n, run(n, os.path.join(root, d), a, build)
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        return dict(ex.map(one, names))


# ── parsing ─────────────────────────────────────────────────────────────────

_NUM = r"(-?\d+\.\d+)"
_PAR = re.compile(r"^\s+(\S.*?)\s{2,}" + _NUM + r"\s+" + _NUM + r"\s+" + _NUM + r"\s+" + _NUM)


def parse(path: str) -> dict:
    txt = open(path, encoding="utf-8", errors="replace").read()
    lines = txt.split("\n")
    r = dict(path=path)
    m = re.search(r"^Series\s*:\s*(.+?)\s{2,}\(", txt, re.M)
    r["series"] = m.group(1).split() if m else []
    m = re.search(r"^Deterministic\s*:\s*(.+)$", txt, re.M)
    r["deterministic"] = m.group(1).strip() if m else ""
    m = re.search(r"^logelf\s*:\s*" + _NUM, txt, re.M)
    r["logL"] = float(m.group(1)) if m else None
    m = re.search(r"^npar\s*:\s*(\d+)", txt, re.M)
    r["npar"] = int(m.group(1)) if m else None

    # asymptotic rank table and the bootstrap table
    r["rank"], r["boot"] = [], []
    for i, L in enumerate(lines):
        if re.match(r"^\s+r\s+M-r\s+LR\s+10%\s+5%\s+1%\s+p-value\s+reps", L):
            for L2 in lines[i + 2:]:
                mm = re.match(r"^\s+(\d+)\s+(\d+)\s+" + _NUM + r"\s+" + _NUM + r"\s+"
                              + _NUM + r"\s+" + _NUM + r"\s+" + _NUM + r"\s+(\d+)", L2)
                if not mm:
                    break
                r["boot"].append(dict(r=int(mm.group(1)), lr=float(mm.group(3)),
                                      c10=float(mm.group(4)), c5=float(mm.group(5)),
                                      c1=float(mm.group(6)), p=float(mm.group(7)),
                                      reps=int(mm.group(8))))
        elif re.match(r"^\s+r\s+M-r\s+LR\s+10%\s+5%\s+1%\s*$", L):
            for L2 in lines[i + 2:]:
                mm = re.match(r"^\s+(\d+)\s+(\d+)\s+" + _NUM, L2)
                if not mm:
                    break
                r["rank"].append(dict(r=int(mm.group(1)), lr=float(mm.group(3))))

    # parameter table
    params = {}
    sec = None
    for L in lines:
        if L.startswith("Parameter") and "Estimate" in L:
            sec = "par"
            continue
        if sec == "par":
            if L.startswith("Signif. codes"):
                break
            mm = _PAR.match(L)
            if mm:
                params[mm.group(1).strip()] = tuple(float(mm.group(k)) for k in (2, 3, 4, 5))
    r["params"] = params

    # short run: Wald test that a variable enters no other equation
    r["drives"] = {}
    for mm in re.finditer(r"^D\.(\S+): what it does to the others:\n.*?\n\s+Wald chi2\((\d+)\) = " + _NUM
                          + r", p-value = " + _NUM, txt, re.M):
        r["drives"][mm.group(1)] = (float(mm.group(3)), int(mm.group(2)), float(mm.group(4)))

    # alpha and beta matrices of the model block
    def matrix(head):
        for i, L in enumerate(lines):
            if L.startswith(head):
                rows = []
                for L2 in lines[i + 1:]:
                    vals = re.findall(r"-?\d+\.\d+", L2)
                    if not vals or not L2.startswith(" "):
                        break
                    rows.append([float(v) for v in vals])
                return rows
        return None
    r["alpha"] = matrix("alpha matrix")
    r["beta"] = matrix("beta matrix")
    r["beta_fixed"] = "beta_2 matrix (s x r)  [FIXED" in txt

    # weak exogeneity (Wald), one variable at a time
    r["weakex_wald"] = {}
    for mm in re.finditer(r"^(\S+) \((?:nabla Y2|Y1) block\):\n\s+H0: this variable does not "
                          r"adjust\n\s+Wald chi2\((\d+)\) = " + _NUM + r", p-value = " + _NUM,
                          txt, re.M):
        r["weakex_wald"][mm.group(1)] = (float(mm.group(3)), float(mm.group(4)))
    # LR of an alpha restriction (-weakex), printed by drvec itself
    mm = re.search(r"LR = 2\(free - restr\.\)\s*:\s*" + _NUM + r"\ndegrees of freedom\s*:\s*(\d+)"
                   r".*?\np-value \(chi2\)\s*:\s*" + _NUM, txt, re.S)
    r["lr_restr"] = (float(mm.group(1)), int(mm.group(2)), float(mm.group(3))) if mm else None
    # multivariate diagnostics
    mm = re.search(r"Q\((\d+)\) = " + _NUM + r", p-value = " + _NUM, txt)
    r["Q"] = (int(mm.group(1)), float(mm.group(2)), float(mm.group(3))) if mm else None
    mm = re.search(r"JB\((\d+)\) = " + _NUM + r", p-value = " + _NUM, txt)
    r["JB"] = (int(mm.group(1)), float(mm.group(2)), float(mm.group(3))) if mm else None
    return r


def alpha_se(fit: dict) -> list[list]:
    """alpha (M x r) with its s.e.: (value, se or None when fixed at 0)."""
    s, A, P = fit["series"], fit["alpha"] or [], fit["params"]
    psi = [v for k, v in P.items() if k.startswith("psi[")]
    out, k = [], 0
    for i, row in enumerate(A):
        cells = []
        for j, a in enumerate(row):
            key = f"D.{s[i]} <- ec{j + 1}"
            if key in P:
                cells.append((P[key][0], P[key][1]))
            elif psi and abs(a) > 1e-12:            # -weakex: alpha = A psi
                cells.append((a, psi[k][1]))
                k += 1
            else:
                cells.append((a, None))
        out.append(cells)
    return out


def beta_se(fit: dict) -> list[list]:
    s, B, P = fit["series"], fit["beta"] or [], fit["params"]
    out = []
    for i, row in enumerate(B):
        cells = []
        for j, b in enumerate(row):
            key = f"{s[i]} in ec{j + 1}"
            cells.append((P[key][0], P[key][1]) if key in P else (b, None))
        out.append(cells)
    return out


def chi2_p(x: float, df: int) -> float:
    from scipy.stats import chi2
    return float(chi2.sf(x, df))


# ── LaTeX ──────────────────────────────────────────────────────────────────

def f(x, nd=2):
    if x is None:
        return "--"
    s = f"{x:.{nd}f}"
    if float(s) == 0:
        s = s.lstrip("-")
    return s.replace("-", "$-$")


def pstar(p):
    return "$^{**}$" if p < 0.05 else "$^{*}$" if p < 0.10 else ""


_HEAD = [r"% Generated by Python/art_drvec/tables/make_tables.py -- do not edit."]


_DET = {"2": "Case 2", "3": "Case 3", "free": "free drifts", "free+trend": "free drifts + trend"}


def _star(p):
    return "$^{**}$" if p < 0.05 else "$^{*}$" if p < 0.10 else ""


def _fixed(c):
    """estimate with its s.e. below; a value without s.e. is fixed (normalised or restricted)"""
    if c is None:
        return "", ""
    val, se = c
    if se is None:
        v = "0" if abs(val) < 5e-4 else ("1" if abs(val - 1) < 5e-4 else ("$-$1" if abs(val + 1) < 5e-4 else f(val, 3)))
        return v + r"$^{\circ}$", ""
    return f(val, 3), f"({f(se, 3)})"


def latex_rank(spec, fits) -> str:
    L = _HEAD + [
        r"\begin{table}\caption{" + spec["caption"] + r"}\label{" + spec["label"] + "}",
        r"\begin{singlespace}\begin{footnotesize}\begin{center}\setlength{\tabcolsep}{4pt}",
        r"\begin{tabular}{@{}lccccc@{}}", r"\thickhline",
        r" & & & \multicolumn{2}{c}{Parametric bootstrap} & \\",
        r"$H_0$ & $p$ & Deterministic terms & LR & 5\,\% c.v. & $\hat r$ \\",
        r" & & & [$p$] & & \\ \thickhline"]
    reps = set()
    for k, (title, run, p, case, radopt) in enumerate(spec["rows"]):
        F = fits[run]
        L.append(r"\multicolumn{6}{@{}l}{" + title + r"} \\ \hline")
        first = True
        for b in F["boot"]:
            reps.add(b["reps"])
            h0 = f"$r{'=' if b['r'] == 0 else r'\le'}{b['r']}$"
            L.append(rf"\quad {h0} & {p if first else ''} & {_DET.get(case, case) if first else ''} & "
                     rf"{f(b['lr'])}{_star(b['p'])} & {f(b['c5'])} & {radopt if first else ''} \\")
            L.append(rf" & & & [{f(b['p'], 3)}] & & \\[2pt]")
            first = False
    rep_txt = ", ".join(str(r) for r in sorted(reps, reverse=True))
    L += [r"\thickhline\end{tabular}\end{center}\end{footnotesize}",
          (r"\begin{footnotesize}\textbf{Notes:} As in Table~\ref{tab:rank}." if spec["label"] == "tab:rank_app" else
           r"\begin{footnotesize}\textbf{Notes:} Exact ML on the univariate models; $\beta$ normalised on the "
           r"variables after the bar. LR for $H_0$ against $r+1$; [$p$]: parametric bootstrap, "
           + rep_txt + r" replications (Section~\ref{subsec:estimation}). $^{*}$, $^{**}$: rejection at 10\,\%, 5\,\%."),
          r"\end{footnotesize}\end{singlespace}\end{table}", ""]
    return "\n".join(L)


_NAMES = {"GY": r"$\ln G_t/Y_t$", "GAP": r"$\ln PE_t/PU_t$", "BXE": r"$BXE_t$",
          "PU": r"$\ln PU_t$", "PE": r"$\ln PE_t$", "REV": r"$re_t$", "G": r"$g_t$",
          "M": r"$i_t$", "X": r"$x_t$", "CAd": r"$de_t$", "CAc": r"$cr_t$"}


def latex_vecm(spec, fits) -> str:
    two = any(len(alpha_se(fits[m[1]])[0]) > 1 for m in spec["models"])
    nb = 2 if two else 1
    n = 1 + 2 * nb + 5
    head1 = (r" & \multicolumn{" + str(nb) + r"}{c}{$\hat\beta$} & \multicolumn{" + str(nb) + r"}{c}{$\hat\alpha$} & "
             r"Weak & \multicolumn{4}{c}{Model} \\")
    sub = (" & ".join(["ec$_1$", "ec$_2$"] * 2) if two else r"$\hat\beta$ & $\hat\alpha$")
    head2 = (r"Variable & " + (sub if two else r" & ") + r" & exog. & LR restr. & Half-life & $Q_H$ & $JB_M$ \\")
    head3 = (r" & " + " & ".join(["(s.e.)"] * (2 * nb)) + r" & [$p$] & [$p$] & (quarters) & [$p$] & [$p$] \\")
    if not two:
        head1 = r" & $\hat\beta$ & $\hat\alpha$ & Weak & LR & Half- & $Q_H$ & $JB_M$ \\"
        head2 = r"Variable & & & exog. & restr. & life & & \\"
        head3 = r" & (s.e.) & (s.e.) & [$p$] & [$p$] & (q.) & [$p$] & [$p$] \\"
    L = _HEAD + [
        r"\begin{table}\caption{" + spec["caption"] + r"}\label{" + spec["label"] + "}",
        r"\begin{singlespace}\begin{footnotesize}\begin{center}\setlength{\tabcolsep}{3.5pt}",
        r"\begin{tabular}{@{}l" + "c" * (n - 1) + r"@{}}", r"\thickhline", head1, head2, head3, r"\thickhline"]
    for title, run, free, rlabel, hl in spec["models"]:
        F = fits[run]
        L.append(r"\multicolumn{" + str(n) + r"}{@{}l}{" + title + r"} \\ \hline")
        A, B = alpha_se(F), beta_se(F)
        # model-level diagnostics, on the row of the normalised (last) variable
        lrc = lrp = hlc = ""
        if free:
            G = fits[free]
            lr = 2 * (G["logL"] - F["logL"])
            df = G["npar"] - F["npar"]
            pv = chi2_p(lr, df)
            lrc, lrp = f(lr) + _star(pv), f"[{f(pv, 3)}]"
        if hl:
            a = A[F["series"].index(hl)][0][0]
            if 0 < abs(a) < 1:
                hlc = f(math.log(0.5) / math.log(1 - abs(a)), 1)
        qc, qp = (f"{f(F['Q'][1])}", f"[{f(F['Q'][2], 3)}]") if F["Q"] else ("", "")
        jc, jp = (f"{f(F['JB'][1])}", f"[{f(F['JB'][2], 3)}]") if F["JB"] else ("", "")
        last = len(F["series"]) - 1
        for i, v in enumerate(F["series"]):
            bs = [_fixed(x) for x in B[i]] + [("", "")] * 2
            as_ = [_fixed(x) for x in A[i]] + [("", "")] * 2
            w = F["weakex_wald"].get(v)
            wc, wp = (f(w[0]) + _star(w[1]), f"[{f(w[1], 3)}]") if w else ("--", "")
            top = [bs[j][0] for j in range(nb)] + [as_[j][0] for j in range(nb)]
            bot = [bs[j][1] for j in range(nb)] + [as_[j][1] for j in range(nb)]
            d1 = [lrc, hlc, qc, jc] if i == last else ["", "", "", ""]
            d2 = [lrp, "", qp, jp] if i == last else ["", "", "", ""]
            L.append(rf"\quad {_NAMES.get(v, v)} & " + " & ".join(top + [wc] + d1) + r" \\")
            L.append(" & " + " & ".join(bot + [wp] + d2) + r" \\[2pt]")
        if run in spec.get("shortrun", ()) and F.get("drives"):
            parts = []
            for v in F["series"]:
                if v in F["drives"]:
                    st, df, pv = F["drives"][v]
                    other = [x for x in F["series"] if x != v][0]
                    short = {"GY": "$G/Y$", "GAP": "GAP"}
                    parts.append(rf"{short.get(v, v)} $\to$ {short.get(other, other)} "
                                 rf"{f(st)}{_star(pv)} [{f(pv, 3)}]")
            L.append(r"\multicolumn{" + str(n) + r"}{@{}l}{\quad Short run, Wald (" + str(df) + r" df): "
                     + "; ".join(parts) + r"} \\[2pt]")
    L += [r"\thickhline\end{tabular}\end{center}\end{footnotesize}",
          (r"\begin{footnotesize}\textbf{Notes:} As in Table~\ref{tab:vecm}." if spec["label"] == "tab:vecm_app" else
           r"\begin{footnotesize}\textbf{Notes:} Exact ML. $^{\circ}$: fixed by the normalisation or a restriction. "
           r"Weak exog.: Wald test that the row of $\alpha$ is zero. Half-life: $\ln 0.5/\ln(1-|\alpha|)$. "
           r"$Q_H$, $JB_M$: multivariate portmanteau and Jarque--Bera. $^{*}$, $^{**}$: rejection at 10\,\%, 5\,\%."),
          r"\end{footnotesize}\end{singlespace}\end{table}", ""]
    return "\n".join(L)


def latex_valid(spec, fits) -> str:
    cases = spec["cases"]
    nc = len(cases)
    L = _HEAD + [
        r"\begin{table}\caption{" + spec["caption"] + r"}\label{" + spec["label"] + "}",
        r"\begin{singlespace}\begin{footnotesize}\begin{center}",
        r"\begin{tabular}{@{}ll" + "c" * nc + r"@{}}", r"\thickhline",
        r" & & " + " & ".join(cases) + r" \\",
        r"Test & $H_0$ & " + " & ".join(["LR"] * nc) + r" \\",
        r" & & " + " & ".join(["[$p$]"] * nc) + r" \\ \thickhline"]
    for title, pres, us in spec["panels"]:
        L.append(r"\multicolumn{" + str(nc + 2) + r"}{@{}l}{" + title + r"} \\ \hline")
        tests = list(spec["tests"]) + [("D", r"$\alpha_{%s}=0$ under relative PPP", None, 1)]
        for tag, h0, suf, df in tests:
            top, bot = [], []
            for pre in pres:
                if pre is None:          # not estimated for this panel
                    top.append("--"); bot.append("")
                    continue
                if suf is None:          # Test D: C against B
                    U, R = fits[pre + "_B"], fits[pre + "_C"]
                else:
                    U, R = fits[pre + "_r1"], fits[pre + "_" + suf]
                lr = 2 * (U["logL"] - R["logL"])
                p = chi2_p(lr, df)
                top.append(f(lr) + _star(p))
                bot.append(f"[{f(p, 3)}]")
            h = h0 % us if "%s" in h0 else h0
            L.append(f"{tag} & {h} & " + " & ".join(top) + r" \\")
            L.append(" & & " + " & ".join(bot) + r" \\[2pt]")
        top, bot = [], []
        for pre in pres:
            if pre is None:
                top.append("--"); bot.append("")
                continue
            R = fits[pre + "_B"]
            Bm = beta_se(R)
            gy = R["series"].index("GY")
            val, se = Bm[gy][0]
            top.append(f(-val, 3)); bot.append(f"({f(se, 3)})" if se is not None else "")
        L.append(r"\multicolumn{2}{@{}l}{$\hat\theta$ under relative PPP} & " + " & ".join(top) + r" \\")
        L.append(r" & & " + " & ".join(bot) + r" \\[2pt]")
    L += [r"\thickhline\end{tabular}\end{center}\end{footnotesize}",
          r"\begin{footnotesize}\textbf{Notes:} $p=2$, $r=1$. Tests A--C: LR "
          r"against the free model; D: C against B. Panel A estimates in Table~\ref{tab:vecm}. "
          r"$^{*}$, $^{**}$: rejection at 10\,\%, 5\,\%.",
          r"\end{footnotesize}\end{singlespace}\end{table}", ""]
    return "\n".join(L)


RENDER = {"rank": latex_rank, "vecm": latex_vecm, "valid": latex_valid}


def needed(spec) -> list[str]:
    k = spec["kind"]
    if k == "rank":
        return [r[1] for r in spec["rows"]]
    if k == "vecm":
        return [x for m in spec["models"] for x in (m[1], m[2]) if x]
    return [f"{pre}_{s}" for _, pres, _ in spec["panels"] for pre in pres if pre
            for s in ("r1", "A", "B", "C")]
