# Replication files: *Inflation in a dollarized economy: the role of fiscal policy*

David E. Guerrero, Paul Carrillo-Maldonado, Maria T. Gonzalez-Perez and Alan E. Bunce.

This repository reproduces every table and figure of the paper's empirical
part with the **ATSW suite** (*A Time Series Workshop*, Box–Jenkins–Treadway
methodology), installed from PyPI.

The analysis has three layers:

- **Univariate models**, one per series, built with **art**. Every model
  carries its *guion*: the identification decisions, the evidence behind
  each one, and every version considered.
- **Cointegrated VARMA systems**, estimated with **drvec** by exact maximum
  likelihood on top of those univariate models. Cointegration ranks are
  tested with a parametric bootstrap and restrictions by likelihood-ratio
  tests.
- **Two transfer functions** from the oil price, to G/Y and to the price
  gap, estimated with **drtran** on the same univariate models.

## Install

```sh
pip install -r requirements.txt      # the atsw meta-package: fue, art, drtran, drvarma, sima, drvec
```

Python ≥ 3.10. The packages ship binary wheels (Linux, macOS, Windows), so
nothing needs compiling.

## Reproduce

```sh
make data           # data/*.csv from the downloaded sources, with every check (~1 min)
make univariate     # Tables 2, 3, 11-13                              (~2 min)
make multivariate   # Tables 5-7, 14, 15                              (~2 h: rank bootstraps)
make analyses       # the other drvec / drtran runs cited in the text (several hours)
make robustness     # Tables 4, 8-10 and the supplement tables        (needs analyses)
make figures        # Figures 1-7
make docs           # docs/: one card per model, from the guiones and the fits
make verify         # compare output/ with expected/
```

Everything is written to `output/` (tables, figures) and `build/`
(engine outputs). `make verify` checks the results against `expected/`:

- the `.tex` tables must be identical;
- the numbers must match to a relative 1e-6;
- the bootstraps use a fixed seed, so they reproduce exactly with the
  compiled engine.

## Tables and figures of the paper

Numbers are those of the October 2026 version. Each table is written by a
generator to `output/tables/<file>.tex`, never edited by hand.

| paper | label | file | program | target |
|---|---|---|---|---|
| Table 1 | `tab:hypotheses` | in the text | | |
| Table 2 | `tab:ur` | `tab_ur` | `tables/make_tables.py ur` | `univariate` |
| Table 3 | `tab:itv` | `tab_itv` | `tables/make_tables.py itv` | `univariate` |
| Table 4 | `tab:ripc` | `tab_ripc` | `tables/make_robustness.py ripc` | `robustness` |
| Table 5 | `tab:rank` | `tab_rank` | `tables/make_tables.py rank` | `multivariate` |
| Table 6 | `tab:vecm` | `tab_vecm` | `tables/make_tables.py vecm` | `multivariate` |
| Table 7 | `tab:validation` | `tab_valid` | `tables/make_tables.py valid` | `multivariate` |
| Table 8 | `tab:tf` | `tab_tf` | `tables/make_robustness.py tf` | `robustness` |
| Table 9 | `tab:prices` | `tab_prices` | `tables/make_robustness.py prices` | `robustness` |
| Table 10 | `tab:sensitivity` | `tab_sensitivity` | `tables/make_robustness.py sens` | `robustness` |
| Tables 11, 12 | `tab:uni`, `tab:uni2` | `tab_uni`, `tab_uni2` | `tables/make_tables.py uni uni2` | `univariate` |
| Table 13 | `tab:ur_app` | `tab_ur_app` | `tables/make_tables.py ur_app` | `univariate` |
| Tables 14, 15 | `tab:rank_app`, `tab:vecm_app` | `tab_rank_app`, `tab_vecm_app` | `tables/make_tables.py rank_app vecm_app` | `multivariate` |
| Figure 1 | `fig:gap_gy` | `gap_vs_gy` | `figures/plot_gap_gy.py` | `figures` |
| Figures 2-4 | `fig:DAS`, `fig:DAD`, `fig:equilibrium` | `fig_das`, `fig_dad`, `fig_equilibrium` | `figures/plot_theory.py` | `figures` |
| Figure 5 | `fig:convergence` | `convergence` | `figures/plot_convergence.py` | `figures` |
| Figure 6 | `fig:irf` | `fig_suite_irf_fevd` | `figures/plot_irf_fevd_suite.py` | `figures` |
| Figure 7 | `fig:wti_irf` | `fig_wti_irf` | `figures/plot_irf_wti.py` | `figures` (see below) |

The univariate rows come from `tables/registry.py` (one entry per series:
model, adopted optimum, panel) and the system rows from
`tables/vecm_registry.py` (one drvec command per run). Every other number
the text cites has its command in `tables/analyses.py`, with the section
that cites it; `docs/analyses_verification.md` checks each one against the
original output. The tables of the Online Supplement
(`tab_subsample`, `tab_irf_transitory`, the Johansen tables of
`tables/make_johansen.py`) are produced by the same targets.

## Interactive route

The same files load in the suite's assistants (MCP servers):

- **art** for the univariate models;
- **sima** for the systems (it drives drvec);
- **mtram** for the transfer function.

With them you can revisit any step instead of only re-running it: identify
a series again, change a decision, test the rank, rerun the bootstrap. See
the packages' documentation on PyPI.

## Contents

| path | what |
|---|---|
| `data/` | `raw/`: the source files as downloaded (`MANIFEST.csv`: source, URL, date, SHA-256); `build_data.py`: raw → `quarterly.csv`, `monthly.csv`, `metadata.csv`; `DATA.md`: sources, construction rules, PPP alignment, checks and open issues |
| `models/` | the univariate models (`.inp` specification, `.pre` adopted optimum, `.out` estimation, `*_guion.json` decision record) and the systems (`VECM_*/`, the `.pre` inputs of each run) |
| `tables/` | the table generator: `registry.py` (univariate rows), `vecm_registry.py` (drvec runs behind the tables), `make_tables.py`, `make_docs.py` |
| `tools/` | `run_analyses.py` (the remaining runs), `verify.py` |
| `figures/` | figure scripts |
| `expected/` | reference outputs: tables (`.tex`, `.json`), bootstrap replications (`.boot`) and IRF bands (`.irfboot`) |
| `docs/` | the model catalogue (generated; Spanish, as recorded in the guiones) |

### Univariate models (`models/`)

The directory layout is the analysis tree's:

| directory | series |
|---|---|
| `PE/`, `PU/`, `GAP/` | CPI Ecuador, CPI USA and their ratio |
| `GY_pasada2/` | G/Y (adopted); `GY_m01_ar1` and `GY_guion.json` in the root are its first pass |
| `MACRO/` | G, REV, TAU = G/REV, YN, YR |
| `EXT/` | BXE, SE, IT, X, M, CAc, CAd, Rc, Rd |
| `DEFL/` | PCE and GDP deflators. `*_G/` are the guided models (adopted); `GAPGDPD/` and `GDPDEC/` are the earlier autonomous ones, kept as intermediate |
| `WTI_m0*` (root) | WTI; `WTI_guion.json` |
| `RIPC/` | the monthly relative-price model of Proposition 1 and its components |

Each guion records which version was adopted (◀ in `docs/univariantes.md`).
The guiones, the run notes in `tables/analyses.py` and some directory
READMEs are the working record, in Spanish, and cite the authors' working
notes (`revision_empirica`, `RESULTADOS_REVISION`, `TODO`), which are not
included; the paper's section is given where it matters.

## Software

- **Licence:** GPL-2.0-or-later.
- **Engines:** drvec is the Python port of the ATSW C program; its wheels
  include the C engine for the long bootstraps.
- **Versions:** the exact versions that produced `expected/` are pinned in
  `requirements.txt` and recorded in every table's `.json` (`meta`).

## What this version does not reproduce

- **The system (WTI, G/Y | GAP) of Section 6.3 and Figure 7.** The adopted
  model holds the weight of WTI in the cointegrating vector at zero
  (`-xsys 1 -fixb2row 1 0`), a combination that drvec 0.1.0 does not accept
  yet. Those numbers and the figure were produced with the C drvec (versions
  0.10 and 0.13 give identical results). The commands are recorded in
  `tables/analyses.py` (`wti:chain`, `wti:chain_fx`); `make figures` skips
  Figure 7 when the C output is not available.
- **The fiscal runs on the master workbook's revenue series**, which cannot be
  verified from 2012 (`data/DATA.md`); the paper uses the Central Bank's
  revenue series, which is reproduced.

## Citation

See `CITATION.cff`.
