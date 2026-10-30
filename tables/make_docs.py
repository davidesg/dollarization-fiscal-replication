#!/usr/bin/env python3
"""Write the model catalogue from the guiones, the regenerated fits and the
drvec runs.

    python make_docs.py [--out DIR]       (after make_tables.py)

Writes to `docs/` (default):
  univariantes.md     one card per series: tables it feeds, adopted model and
                      its regenerated estimates and tests, the guion's nodes
                      and every version with its decision, references
  multivariantes.md   one card per system directory: where each `.pre` comes
                      from (matched by content to the univariate models), the
                      table runs and their results, the README, references

The text of the decisions is the guion's, verbatim (Spanish, as recorded).
Nothing here is typed by hand.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ROOT = os.path.join(REPO, "models")
SUITE = os.path.join(REPO, "output", "tables")
DOCS = os.path.join(REPO, "docs")
DEFAULT_OUT = DOCS
sys.path.insert(0, HERE)
import registry as R          # noqa: E402
import vecm_registry as VR    # noqa: E402


SYSTEMS = {
    "VECM_GAP_GY": "Sistema central (G/Y | GAP)",
    "VECM_AUG": "Central aumentado con BXE",
    "VECM_XSYS": "Entradas exógenas (IT empotrada, por resta)",
    "VECM_TRI": "Trivariante (G/Y, IPC_USA | IPC_EC)",
    "VECM_TRI_IRF": "Choque transitorio (IRF con bandas)",
    "VECM_SUB": "Submuestras de θ",
    "VECM_REC": "θ recursivo y estabilidad de β",
    "VECM_WTI": "Petróleo: WTI y G/Y",
    "VECM_PCE": "Robustez: deflactor del consumo",
    "VECM_GDPD": "Robustez: deflactor del PIB (autónomo)",
    "VECM_GDPD_G": "Robustez: deflactor del PIB (guiado)",
    "VECM_FISC": "VEC fiscal (gasto, ingresos)",
    "VECM_BOP": "VEC de las balanzas (créditos, débitos)",
}


def fnum(x, nd=3):
    return "—" if x is None else f"{x:.{nd}f}"


def cell(s: str) -> str:
    return (s or "").replace("|", "\\|").replace("\n", " ").strip()


# ── univariate cards ────────────────────────────────────────────────────────

def load_suite():
    rows = {}            # inp -> dict(tables=[...], fit=..., addon_of=...)
    for t in ("uni", "uni2", "ur", "ur_app"):
        p = os.path.join(SUITE, f"{t}.json")
        if not os.path.exists(p):
            continue
        js = json.load(open(p))["rows"]
        spec = R.TABLES[t]
        for _, grp in spec["groups"]:
            for row in grp:
                k = row["name"] + "|" + row["mnem"]
                for tag in ("main", "addon"):
                    if tag not in js.get(k, {}):
                        continue
                    f = js[k][tag]
                    e = rows.setdefault(f["model"], dict(tables=[], fit=f, roles=set()))
                    e["tables"].append(f"{spec['label']} «{row['name']}»"
                                       + (" (addon)" if tag == "addon" else ""))
                    e["roles"].add(tag)
                    for kk in ("under", "ur"):              # tab:ur has the d−1 side
                        if f.get(kk) is not None:
                            e["fit"][kk] = f[kk]
    return rows


def guion_for(inp: str):
    d = os.path.dirname(os.path.join(ROOT, inp))
    stem = os.path.basename(inp).split("_m")[0]
    for cand in (os.path.join(d, f"{stem}_guion.json"), *glob.glob(os.path.join(d, "*_guion.json"))):
        if os.path.exists(cand):
            return cand
    return None


def card_uni(inp: str, e: dict) -> list[str]:
    f = e["fit"]
    d = os.path.dirname(inp) or "."
    L = [f"### `{inp}`", ""]
    L.append(f"- **Tablas:** {'; '.join(dict.fromkeys(e['tables']))}")
    L.append(f"- **Ficheros:** especificación `{inp}` · óptimo adoptado `{f['adopted_pre']}` · "
             f"reestimado en `build/{os.path.basename(inp)[:-4]}.out`")
    L.append(f"- **Reproduce el `.pre` adoptado:** {'sí' if f['reproduces'] else 'NO'} "
             f"(máx |Δ| {f['maxdiff']:.1e}); logL {f['loglik']:.4f}")
    L.append("")
    # estimates
    L += ["| parámetro | estimación | e.t. | t |", "|---|---|---|---|"]
    for p in f["params"]:
        t = p["value"] / p["se"] if p["se"] else float("nan")
        L.append(f"| {cell(p['label'])} | {p['value']:.4f} | {p['se']:.4f} | {t:.2f} |")
    L.append("")
    itv = "; ".join(f"{i['type']} {i['date']} (×{i['n']})" for i in f["interventions"]) or "ninguna"
    mean = f["mean"]
    L.append(f"- λ = {f['lam']:g}, d = {f['d']}, D = {f['D']}; intervenciones: {itv}")
    L.append(f"- media de ∇ (o nivel si d = 0): "
             f"{fnum(mean['value'], 2) + ' (' + fnum(mean['se'], 2) + ')' if mean else 'sin μ'}; "
             f"σ = {fnum(f['sigma'], 3)}")
    q = f["q"]
    L.append(f"- residuos: Q({q['lag']}) = {q['stat']:.2f} (gl {q['df']}, p {fnum(q['p'])}); "
             f"JB = {fnum(f['jb'], 2)} (p {fnum(f['jb_p'])})")
    sf = f["sf"] or {}
    sfs = (f"no aplica ({sf['na'][:90]}…)" if "na" in sf else
           f"Φ = {sf['stat']:.2f} (críticos 10 % {sf['c10']:.2f}, 5 % {sf['c5']:.2f})"
           + (", sobre AR sobreajustado" if sf.get("overfit") else "") if "stat" in sf else "—")
    dc = f["dcd"] or {}
    L.append(f"- lado d+1: SF {sfs}; DCD⁺ LR {fnum(dc.get('stat'), 2)}, θ̂ {fnum(dc.get('theta'))}")
    un = f.get("under") or {}
    if un:
        L.append(f"- lado d−1: DCD⁻ LR {fnum(un.get('stat'), 2)}, θ̂ {fnum(un.get('theta'))}")
    if f.get("ur"):
        L.append("- identificación (ADF / KPSS, p): " + "; ".join(
            f"d={u['d']}: {u['adf_p']:.3f} / {u['kpss_p']:.3f}" for u in f["ur"]))
    L.append("")
    # guion
    g = guion_for(inp)
    if not g:
        L += ["*Sin guion en el directorio.*", ""]
        return L
    gj = json.load(open(g))
    L.append(f"**Guion** `{os.path.relpath(g, ROOT)}` (serie {gj.get('series')}, creado "
             f"{gj.get('created')}).")
    L.append("")
    nodes = [x["node"] for x in gj["entries"] if x.get("kind") == "node" and isinstance(x.get("node"), dict)]
    if nodes:
        L += ["| nodo | decidido | evidencia |", "|---|---|---|"]
        for n in nodes:
            L.append(f"| {cell(n.get('nodo'))} | {cell(str(n.get('decidido')))} | "
                     f"{cell(n.get('evidencia'))[:300]} |")
        L.append("")
    models = [x for x in gj["entries"] if x.get("kind") == "model"]
    stem = os.path.basename(inp)[:-4]
    adopted_here = [x for x in models if x.get("status") == "adopted"]
    match = [x for x in models if os.path.basename(x.get("inp_path") or "").startswith(stem)
             or os.path.basename(x.get("out_path") or "").startswith(stem)]
    L += ["| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |", "|---|---|---|---|---|---|---|---|"]
    for x in models:
        st = x.get("stats") or {}
        mark = " ◀" if x in match else ""
        L.append(f"| {x.get('version')} | {cell(x.get('name'))}{mark} | {x.get('status')} | "
                 f"{fnum(st.get('bic'), 1)} | {fnum(st.get('sigma_a'), 3)} | "
                 f"{'✓' if st.get('q_pass') else '✗' if st.get('q_pass') is False else '—'} | "
                 f"{fnum(st.get('jb_pvalue'))} | {cell(x.get('decision'))[:160]} |")
    L.append("")
    if not adopted_here:
        L.append("*El guion no marca ninguna versión como adoptada; el modelo de la tabla es el "
                 "del registro (`registry.py`), marcado ◀ si está en el guion.*")
        L.append("")
    for x in adopted_here + [x for x in match if x not in adopted_here]:
        L.append(f"**{x.get('name')}** ({x.get('status')}, {x.get('timestamp', '')[:10]})")
        if x.get("equation"):
            L.append(f"- ecuación: `{x['equation']}`")
        for k, lab in (("rationale", "motivo"), ("why_adopted", "por qué se adopta"),
                       ("problems_found", "problemas y salvedades")):
            if x.get(k):
                L.append(f"- {lab}: {cell(x[k])}")
        L.append("")
    ab = [x for x in models if x.get("status") == "abandoned" and x.get("why_abandoned")]
    if ab:
        L.append("Versiones abandonadas:")
        for x in ab:
            L.append(f"- **{x.get('name')}**: {cell(x['why_abandoned'])}")
        L.append("")
    return L


# ── multivariate cards ──────────────────────────────────────────────────────

def _sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def univariate_index():
    idx = {}
    for p in glob.glob(os.path.join(ROOT, "**", "*.pre"), recursive=True):
        rel = os.path.relpath(p, ROOT)
        if rel.startswith(("VECM_", "tables/", "replica/", "replica_")):
            continue
        idx.setdefault(_sha(p), []).append(rel)
    return idx


def card_sys(d: str, idx, fits) -> list[str]:
    L = [f"### {SYSTEMS.get(d, d)} — `{d}/`"]
    pres = sorted(glob.glob(os.path.join(ROOT, d, "**", "*.pre"), recursive=True))
    if pres:
        L += ["", "| `.pre` del sistema | univariante del que procede (mismo contenido) |", "|---|---|"]
        for p in pres:
            src = idx.get(_sha(p))
            L.append(f"| `{os.path.relpath(p, ROOT)}` | "
                     f"{', '.join('`' + s + '`' for s in src) if src else 'sin copia idéntica (versión propia del sistema)'} |")
    runs = [(n, a) for n, (dd, a) in VR.RUNS.items() if dd == d or dd.startswith(d + "/")]
    if runs:
        L += ["", "Corridas regeneradas por `make_tables.py` (en `tables/build/drvec/`):", "",
              "| corrida | argumentos | resultado |", "|---|---|---|"]
        for n, a in runs:
            F = fits.get(n)
            res = "—"
            if F:
                if F.get("boot"):
                    res = "; ".join(f"r={b['r']}: LR {b['lr']:.2f}, boot p {b['p']:.3f} ({b['reps']})"
                                    for b in F["boot"])
                elif F.get("alpha"):
                    import vecm
                    A, B = vecm.alpha_se(F), vecm.beta_se(F)
                    s = F["series"]
                    res = ("β " + ", ".join(f"{s[i]} {B[i][0][0]:.3f}" for i in range(len(s)))
                           + "; α " + ", ".join(f"{s[i]} {A[i][0][0]:.3f}"
                                                + (f" ({A[i][0][1]:.3f})" if A[i][0][1] else "")
                                                for i in range(len(s)))
                           + f"; logL {F['logL']:.3f}")
            L.append(f"| `{n}` | `{a}` | {res} |")
    rd = os.path.join(ROOT, d, "README.md")
    subs = sorted(glob.glob(os.path.join(ROOT, d, "*", "README.md")))
    for r in ([rd] if os.path.exists(rd) else []) + subs:
        L += ["", f"<details><summary>README `{os.path.relpath(r, ROOT)}`</summary>", ""]
        L += [re.sub(r"^#", "####", x) for x in open(r).read().strip().split("\n")]
        L += ["", "</details>"]
    outs = sorted(os.path.basename(x)[:-4] for x in glob.glob(os.path.join(ROOT, d, "*.out")))
    if outs:
        L += ["", f"Salidas en el directorio ({len(outs)}): " + ", ".join(f"`{o}`" for o in outs)]
    L.append("")
    return L


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    rows = load_suite()
    U = ["# Catálogo de modelos univariantes", "",
         "Generado por `tables/make_docs.py` a partir de los guiones de art "
         "y de las estimaciones regeneradas por `make_tables.py`. No editar a mano: las "
         "decisiones se cambian en el guion y se regenera.", "",
         "Cada ficha: tablas del paper que alimenta, ficheros, reproducción del óptimo, "
         "estimaciones (λ, d, intervenciones, ARMA, μ), diagnosis, contrastes formales de d "
         "por los dos lados, y el guion completo: nodos decididos con su evidencia y todas las "
         "versiones con su estado y decisión (◀ = el modelo de la tabla).", ""]
    order = sorted(rows, key=lambda k: (os.path.dirname(k), k))
    U += ["## Índice", ""] + [f"- [`{k}`](#{re.sub(r'[^a-z0-9_-]', '', k.lower().replace('/', '').replace('.', ''))})"
                              for k in order] + [""]
    for k in order:
        U += card_uni(k, rows[k])
    open(os.path.join(a.out, "univariantes.md"), "w").write("\n".join(U))

    import vecm
    fits = {}
    for n in VR.RUNS:
        p = os.path.join(REPO, "build", "drvec", n, n + ".out")
        if os.path.exists(p):
            fits[n] = vecm.parse(p)
    idx = univariate_index()
    M = ["# Catálogo de sistemas multivariantes", "",
         "Generado por `tables/make_docs.py`. Cada ficha: de qué univariante procede cada `.pre` (comparación por contenido "
         "con los modelos de art); las corridas que regenera `make_tables.py` con su resultado; "
         "el README del directorio y la lista de salidas.", ""]
    dirs = [d for d in SYSTEMS if os.path.isdir(os.path.join(ROOT, d))]
    M += ["## Índice", ""] + [f"- {SYSTEMS[d]} — `{d}/`" for d in dirs] + [""]
    for d in dirs:
        M += card_sys(d, idx, fits)
    open(os.path.join(a.out, "multivariantes.md"), "w").write("\n".join(M))
    print(f"written {a.out}/univariantes.md ({len(rows)} series), multivariantes.md ({len(dirs)} systems)")


if __name__ == "__main__":
    main()
