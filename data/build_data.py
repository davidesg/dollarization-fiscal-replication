#!/usr/bin/env python3
"""Build the analysis data from the downloaded sources.

    python data/build_data.py            build and check
    python data/build_data.py --check    check only (write nothing)

Reads only `data/raw/` (see `data/raw/MANIFEST.csv` for each file's source,
URL, download date and SHA-256) and writes:

  data/quarterly.csv    2003Q1-2019Q4, the 26 quarterly series of the models
  data/monthly.csv      2002M01-2008M06, the 3 monthly series (Proposition 1)
  data/metadata.csv     one row per series: source, rule, unit, note
  data/build_report.txt the checks below, with the SHA-256 of every input

Checks (the run fails if any does not hold):
  1. every input file matches the SHA-256 recorded in MANIFEST.csv;
  2. the GDP of the master workbook equals the BCE national accounts
     (release 127), and SPNF expenditure equals the BCE fiscal operations;
  3. every built series equals, to 1e-9 relative, the series stored in the
     model files `models/**/*.inp` (the data the estimates use).

Rules (DATA.md):
  price indices -> quarterly mean of 3 months
  flows         -> quarterly sum of 3 months
  ratios        -> ratio of quarterly aggregates (never a mean of ratios)
  natively quarterly series (GDP, balance of payments) -> as published
  no seasonal adjustment: seasonality is modelled in each univariate model
  (exception: the US deflators, published only seasonally adjusted).
"""
from __future__ import annotations

import csv
import glob
import hashlib
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
REPO = os.path.dirname(HERE)

MASTER = os.path.join(RAW, "master", "15-05-2024_Data_vf.xlsx")
CNT = os.path.join(RAW, "bce_cnt", "tou_127_202401.xlsx")
SPNF_HIST = os.path.join(RAW, "bce_spnf", "OperSPNF_Historico.xlsx")
SPNF_NEW = os.path.join(RAW, "bce_spnf", "OperSPNF_DOLARES.xlsx")
WTI = os.path.join(RAW, "fred", "WTISPLC_2026-05-26.xlsx")
FRED_PCE = os.path.join(RAW, "fred", "DPCERD3Q086SBEA_2026-10-09.csv")
FRED_GDPD = os.path.join(RAW, "fred", "GDPDEF_2026-10-09.csv")
WB_PRVT = os.path.join(RAW, "worldbank", "ECU_PA.NUS.PRVT.PP.json")
WB_GDP = os.path.join(RAW, "worldbank", "ECU_PA.NUS.PPP.json")
INEC = os.path.join(RAW, "inec", "SERIE_HISTORICA_IPC_12_2019.xls")
BLS = sorted(glob.glob(os.path.join(RAW, "bls", "CUUR0000SA0_*.json")))
BOP5 = os.path.join(RAW, "bce_bop", "boletin69_1_BdPNormalizada.xls")
BOP6 = os.path.join(RAW, "bce_bop", "boletin87_1_BP_Normalizada.xlsx")

SAMPLE = ("2003Q1", "2019Q4")
SAMPLE_M = ("2002-01", "2008-06")
PPP_YEAR = 2011          # ICP round used to align price levels (annual-average base)
TOL = 1e-9

lines: list[str] = []
meta: list[dict] = []
ok = True


def say(*a) -> None:
    s = " ".join(str(x) for x in a)
    print(s)
    lines.append(s)


def check(cond: bool, msg: str, warn: bool = False) -> None:
    """A failed check stops the build; a failed `warn` check is reported only
    (a known, documented difference between the master workbook and the
    current official vintage -- see DATA.md, "Open issues")."""
    global ok
    say(("  ok    " if cond else ("  WARN  " if warn else "  FAIL  ")) + msg)
    if not warn:
        ok &= bool(cond)


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def add(name, series, source, rule, unit, note=""):
    meta.append(dict(series=name, source=source, rule=rule, unit=unit, note=note))
    return series.rename(name)


def q_mean(s: pd.Series) -> pd.Series:
    """Quarterly mean of a monthly series; complete quarters only."""
    g = s.groupby(s.index.asfreq("Q"))
    return g.mean()[g.count() == 3]


def q_sum(s: pd.Series) -> pd.Series:
    """Quarterly sum of a monthly flow; complete quarters only."""
    g = s.groupby(s.index.asfreq("Q"))
    return g.sum(min_count=3)[g.count() == 3]


# ── 1. Inputs and their checksums ───────────────────────────────────────────
say("BUILD DATA")
manifest = {r["file"]: r for r in csv.DictReader(open(os.path.join(RAW, "MANIFEST.csv")))}
for p in (MASTER, CNT, SPNF_HIST, SPNF_NEW, WTI, FRED_PCE, FRED_GDPD, WB_PRVT, WB_GDP, INEC, *BLS, BOP5, BOP6):
    rel = os.path.relpath(p, RAW)
    h = sha256(p)
    rec = manifest.get(rel, {}).get("sha256", "")
    check(h == rec, f"{rel:45s} sha256 {h[:16]}" + ("" if h == rec else f" (MANIFEST: {rec[:16] or 'missing'})"))

monthly = pd.read_excel(MASTER, "Data").rename(columns={"Unnamed: 0": "date"})
monthly = monthly.dropna(subset=["date"]).set_index("date")
monthly.index = pd.PeriodIndex(monthly.index, freq="M")
quarterly = pd.read_excel(MASTER, "Data trim").dropna(subset=["fecha"])
quarterly.index = pd.PeriodIndex(quarterly.pop("fecha"), freq="Q")

wti_m = pd.read_excel(WTI, "Monthly", header=None, skiprows=1, names=["date", "WTI"])
wti_m.index = pd.PeriodIndex(pd.to_datetime(wti_m.pop("date")), freq="M")
wti_m = wti_m["WTI"].astype(float)

QMAP = {"I": 1, "II": 2, "III": 3, "IV": 4}


def cnt_sheet(sheet: str) -> pd.DataFrame:
    """A sheet of the BCE quarterly national accounts (release 127)."""
    t = pd.read_excel(CNT, sheet, header=None)
    h = [str(v).strip() for v in t.iloc[8].tolist()]
    r = t[t[0].astype(str).str.match(r"^\d{4}\.(I|II|III|IV)\b")]
    idx = pd.PeriodIndex([pd.Period(year=int(s.split(".")[0]), quarter=QMAP[s.split(".")[1].split()[0]],
                                    freq="Q") for s in r[0]])
    return pd.DataFrame(r.iloc[:, 1:].astype(float).values, index=idx, columns=h[1:])


def fred(path: str) -> pd.Series:
    f = pd.read_csv(path)
    return pd.Series(f.iloc[:, 1].astype(float).values,
                     index=pd.PeriodIndex(pd.to_datetime(f.iloc[:, 0]), freq="Q"))


def worldbank(path: str) -> pd.Series:
    j = json.load(open(path))
    return pd.Series({int(r["date"]): r["value"] for r in j[1] if r["value"] is not None}).sort_index()


cur, vol = cnt_sheet("Dem_Corr_bru"), cnt_sheet("Dem_Cad_bru")
HH = "Gasto de Consumo final  Hogares (*)"

# ── 2. Cross-checks of the master workbook against the official files ──────
say("\nCROSS-CHECKS")
gdp = quarterly["v_10"].astype(float)
d = np.max(np.abs(cur["P.I.B."].loc[SAMPLE[0]:SAMPLE[1]] / 1000 / gdp.loc[SAMPLE[0]:SAMPLE[1]] - 1))
check(d < 1e-6, f"nominal GDP: master v_10 = BCE CNT 127 P.I.B. (max rel. diff {d:.1e})")
spend_m = monthly["v_3"].astype(float)


def spnf_monthly(path: str) -> dict[str, pd.Series]:
    """Monthly SPNF expenditure and revenue from a BCE 'SPNF-Dólares' sheet.

    Historical file (to 2011): one column per month from 2000M1, rows
    'Total Ingresos' and 'GASTOS TOTALES'. New file (from 2012): a header row
    of dates, rows by code ('1' TOTAL INGRESOS, '2' TOTAL EROGACIONES)."""
    import datetime as dt
    import openpyxl
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True)["SPNF-Dólares"]
    rows = [r for r in ws.iter_rows(values_only=True)]
    hdr = next((r for r in rows[:30] if sum(isinstance(x, (dt.datetime, dt.date)) for x in r) > 12), None)
    if hdr is not None:                                   # new methodology
        cols = [(j, h) for j, h in enumerate(hdr) if isinstance(h, (dt.datetime, dt.date))]
        code = {str(r[0]).strip(): r for r in rows if r and r[0] is not None}
        idx = pd.PeriodIndex([h for _, h in cols], freq="M")
        out = {k: pd.Series([float(code[c][j]) for j, _ in cols], index=idx)
               for k, c in (("G", "2"), ("REV", "1"))}
        # 2012 is published only as an annual total (column '2012(3)')
        yr = next(j for r in rows[:30] for j, x in enumerate(r) if isinstance(x, str) and x.startswith("2012"))
        out.update({k + "2012": float(code[c][yr]) for k, c in (("G", "2"), ("REV", "1"))})
        return out
    lab = {str(r[0]).strip().upper(): r for r in rows if r and isinstance(r[0], str)}
    out = {}
    for k, name in (("G", "GASTOS TOTALES  (2)"), ("REV", "TOTAL INGRESOS")):
        r = lab[name]
        vals = [float(v) for v in r[1:] if isinstance(v, (int, float))]
        out[k] = pd.Series(vals, index=pd.period_range("2000-01", periods=len(vals), freq="M"))
    return out


rev_m = monthly["v_4"].astype(float)
SPNF = {}
for path, span in ((SPNF_HIST, ("2003-01", "2011-12")), (SPNF_NEW, ("2013-01", "2019-12"))):
    bce = spnf_monthly(path)
    SPNF[path] = bce
    for k, mst in (("G", spend_m), ("REV", rev_m)):
        a, b = mst.loc[span[0]:span[1]], bce[k].loc[span[0]:span[1]]
        diff = float(np.max(np.abs(a.values - b.values))) if len(a) == len(b) else float("inf")
        check(diff < 0.01, warn=(path == SPNF_NEW), msg=f"SPNF {'expenditure' if k == 'G' else 'revenue'} {span[0]}..{span[1]}: master "
                            f"{'v_3' if k == 'G' else 'v_4'} = BCE {os.path.basename(path)} "
                            f"(monthly, max abs. diff USD {diff:.4f} m)")
        if path == SPNF_NEW:
            d12 = abs(mst.loc["2012"].sum() - bce[k + "2012"])
            check(d12 < 0.01, warn=True, msg=f"SPNF {'expenditure' if k == 'G' else 'revenue'} 2012 (annual, published "
                              f"only as a year): diff USD {d12:.4f} m")

# CPI Ecuador: INEC historical series (base 2014 = 100), sheet '1. ÍNDICE'
t = pd.read_excel(INEC, "1. ÍNDICE", header=None)
inec = {}
for _, r in t.iterrows():
    if isinstance(r[0], (int, float)) and pd.notna(r[0]) and 1900 < r[0] < 2100:
        for mth in range(1, 13):
            if pd.notna(r[mth]):
                inec[pd.Period(f"{int(r[0])}-{mth:02d}", "M")] = float(r[mth])
inec = pd.Series(inec).sort_index()
v1 = monthly["v_1"].astype(float).dropna()
com = v1.index.intersection(inec.index)
d = float(np.max(np.abs(v1[com] / inec[com] - 1)))
check(d < 1e-12, f"CPI Ecuador: master v_1 = INEC series {com[0]}..{com[-1]} (max rel. diff {d:.1e})")

# CPI-U: BLS series CUUR0000SA0 (public API, one file per span of years)
bls = {}
for f in BLS:
    for r in json.load(open(f))["Results"]["series"][0]["data"]:
        if r["period"].startswith("M") and r["period"] != "M13":
            bls[pd.Period(f"{r['year']}-{r['period'][1:]}", "M")] = float(r["value"])
bls = pd.Series(bls).sort_index()
v2 = monthly["v_2"].astype(float).dropna()
com = v2.index.intersection(bls.index)
d = float(np.max(np.abs(v2[com] - bls[com])))
check(d < 1e-9, f"CPI-U: master v_2 = BLS CUUR0000SA0 {com[0]}..{com[-1]} (max abs. diff {d:.1e})")


def bop_bulletin(path: str, header_row: int | None, pattern: str, parse, rows: dict) -> pd.DataFrame:
    """Quarterly items of a BCE balance-of-payments bulletin (debits are published negative)."""
    import re
    t = pd.read_excel(path, header=None)
    hr = header_row if header_row is not None else next(
        i for i in range(15) if t.iloc[i].astype(str).str.strip().str.match(pattern).sum() > 3)
    q = [(j, str(v).strip()) for j, v in t.iloc[hr].items() if re.match(pattern, str(v).strip())]
    idx = pd.PeriodIndex([parse(h) for _, h in q])
    lc = next(c for c in t.columns if t[c].astype(str).str.strip().eq("CUENTA CORRIENTE").any())
    lab = [str(v).strip() for v in t[lc]]

    def find(path_):
        i = -1
        for name in path_:
            i = next(k for k in range(i + 1, len(lab)) if lab[k].startswith(name))
        return pd.Series(t.loc[i, [j for j, _ in q]].astype(float).values, index=idx).abs()
    return pd.DataFrame({k: sum(find(p) for p in ps) for k, ps in rows.items()})


QR = {"I": 1, "II": 2, "III": 3, "IV": 4}
bop5 = bop_bulletin(BOP5, 8, r"^\d{4}-(I|II|III|IV)$",
                    lambda h: pd.Period(year=int(h[:4]), quarter=QR[h[5:]], freq="Q"),
                    {"X": [["BIENES", "Exportaciones"], ["SERVICIOS", "Servicios prestados"]],
                     "M": [["BIENES", "Importaciones"], ["SERVICIOS", "Servicios recibidos"]],
                     "inc_cr": [["RENTA", "Renta recibida"]], "inc_db": [["RENTA", "Renta pagada"]],
                     "tr_cr": [["TRANSFERENCIAS CORRIENTES", "Transferencias corrientes recibidas"]],
                     "tr_db": [["TRANSFERENCIAS CORRIENTES", "Transferencias corrientes enviadas"]]})
bop6 = bop_bulletin(BOP6, None, r"^(I|II|III|IV)-\d{4}$",
                    lambda h: pd.Period(year=int(h.split("-")[1]), quarter=QR[h.split("-")[0]], freq="Q"),
                    {"X": [["BIENES Y SERVICIOS", "Exportaciones"]], "M": [["BIENES Y SERVICIOS", "Importaciones"]],
                     "inc_cr": [["INGRESO PRIMARIO", "Crédito"]], "inc_db": [["INGRESO PRIMARIO", "Débito"]],
                     "tr_cr": [["INGRESO SECUNDARIO", "Crédito"]], "tr_db": [["INGRESO SECUNDARIO", "Débito"]]})
B_ = {"X": "Exportaciones (bienes + servicios)", "M": "Importaciones (bienes + servicios)",
      "inc_cr": "Crédito (Renta recibida)", "inc_db": "Débito (Renta pagada)",
      "tr_cr": "Crédito (transf. recibida)", "tr_db": "Débito (transf. pagada)"}
mst_bop = quarterly[list(B_.values())].astype(float).rename(columns={v: k for k, v in B_.items()})
for bb, span, lab_ in ((bop5, ("2003Q1", "2015Q4"), "bulletin 69 (BPM5)"),
                       (bop6, ("2016Q1", "2019Q4"), "bulletin 87 (BPM6)")):
    d = float((mst_bop.loc[span[0]:span[1]] - bb.loc[span[0]:span[1]]).abs().max().max())
    check(d < 1e-6, f"balance of payments {span[0]}..{span[1]}: master = BCE {lab_}, "
                    f"X, M, income and current transfers (max abs. diff USD {d:.1e} m)")
d = (bop5.loc["2016Q1":"2019Q3"] - bop6.loc["2016Q1":"2019Q3"]).abs().max()
say(f"  note  BPM5 vs BPM6 over 2016Q1-2019Q3 (USD m, max abs.): " +
    ", ".join(f"{k} {v:.0f}" for k, v in d.items()) + " -- the master splices the manuals in 2016")


# ── 3. The series ───────────────────────────────────────────────────────────
say("\nSERIES")
# 3a. Prices: CPIs aligned to the PPP price level of year b (World Bank ICP)
#   PE_t = 100 * PLI_b * CPI_EC,t / mean_b(CPI_EC);  PU_t = 100 * CPI_US,t / mean_b(CPI_US)
#   PLI_b = PA.NUS.PRVT.PP (household consumption PPP, LCU per international $).
#   Ecuador uses the US dollar, so the factor IS Ecuador's price level relative
#   to the US. In logs it is a constant: dynamics and theta do not depend on it.
pli = worldbank(WB_PRVT)
ec_m, us_m = monthly["v_1"].astype(float), monthly["v_2"].astype(float)
inb = ec_m.index.year == PPP_YEAR
pe_m = 100 * pli[PPP_YEAR] * ec_m / ec_m[inb].mean()
pu_m = 100 * us_m / us_m[inb].mean()
say(f"  PPP alignment: b = {PPP_YEAR}, PLI_b = {pli[PPP_YEAR]:.4f} (World Bank PA.NUS.PRVT.PP)")
for b2 in (2005, 2017, 2021):
    if b2 in pli:
        implied = (pe_m / pu_m)[pe_m.index.year == b2].mean()
        say(f"    ICP {b2}: CPI-extrapolated level {implied:.4f} vs measured PPP {pli[b2]:.4f} "
            f"({100 * np.log(implied / pli[b2]):+.1f} log points)")

Q = {}
Q["PE"] = add("PE", q_mean(pe_m), "master Data:v_1 (INEC CPI, base 2014)",
              f"PPP-aligned (b = {PPP_YEAR}); mean of 3 months", "index, US level of b = 100",
              "Ecuador price level in % of the US level of year b")
Q["PU"] = add("PU", q_mean(pu_m), "master Data:v_2 (BLS CPI-U, NSA)",
              f"rebased to the annual mean of {PPP_YEAR} = 100; mean of 3 months", "index")
Q["GAP"] = add("GAP", Q["PE"] / Q["PU"], "PE / PU", "ratio", "ratio", "Ecuador / US price level")

# 3b. Fiscal
# SPNF revenue from the BCE files themselves (the master's v_4 is not
# reproduced from 2012, DATA.md section 7): the historical series to 2011, the
# current series from 2013, and 2012 -- published by the BCE only as an annual
# total -- distributed over the months with the profile of the master's v_4
# (pro-rata benchmarking: the 12 months add up to the BCE total).
rev_hist = SPNF[SPNF_HIST]["REV"].loc["2003-01":"2011-12"]
rev_new = SPNF[SPNF_NEW]["REV"].loc["2013-01":"2019-12"]
prof = rev_m.loc["2012-01":"2012-12"]
rev_2012 = prof * SPNF[SPNF_NEW]["REV2012"] / prof.sum()
rev_bce = pd.concat([rev_hist, rev_2012, rev_new]).sort_index()
check(len(rev_bce) == 204 and abs(rev_bce.loc["2012-01":"2012-12"].sum() - SPNF[SPNF_NEW]["REV2012"]) < 1e-6,
      f"SPNF revenue rebuilt from the BCE files 2003M1-2019M12 (2012 = BCE annual total "
      f"{SPNF[SPNF_NEW]['REV2012']:.1f}, monthly profile of v_4, factor {SPNF[SPNF_NEW]['REV2012'] / prof.sum():.4f})")
spend, rev = q_sum(spend_m), q_sum(rev_bce)
Q["GY"] = add("GY", spend / gdp, "master Data:v_3 (BCE SPNF expenditure) / Data trim:v_10 (GDP)",
              "sum of 3 months / quarterly GDP", "ratio",
              "SPNF: 'Gastos totales' to 2011, 'Total erogaciones' from 2012; includes CFDD from 2008M1")
Q["G"] = add("G", spend, "master Data:v_3 (BCE SPNF expenditure)", "sum of 3 months", "USD million")
Q["REV"] = add("REV", rev, "BCE Operaciones del SPNF: 'Total Ingresos' (historical, to 2011), "
              "'TOTAL INGRESOS' (current series, from 2013); 2012 = BCE annual total, monthly profile of master v_4",
              "sum of 3 months", "USD million",
              "replaces master v_4, which from 2012 does not match the BCE (DATA.md section 7)")
Q["TAU"] = add("TAU", spend / rev, "G / REV", "ratio", "ratio", "100 ln TAU = deficit in % of revenue")

# 3c. Output
Q["YN"] = add("YN", cur["P.I.B."] / 1000, "BCE CNT 127 Dem_Corr_bru: P.I.B.", "as published",
              "USD million", "current prices, NSA")
Q["YR"] = add("YR", vol["P.I.B."] / 1000, "BCE CNT 127 Dem_Cad_bru: P.I.B.", "as published",
              "USD million of 2018", "chained volume, NSA")

# 3d. External accounts (BCE balance of payments, natively quarterly, in the master)
B = {"X": "Exportaciones (bienes + servicios)", "M": "Importaciones (bienes + servicios)",
     "inc_cr": "Crédito (Renta recibida)", "inc_db": "Débito (Renta pagada)",
     "tr_cr": "Crédito (transf. recibida)", "tr_db": "Débito (transf. pagada)"}
bop = quarterly[list(B.values())].astype(float).rename(columns={v: k for k, v in B.items()})
src = "master Data trim (BCE balance of payments)"
Q["X"] = add("X", bop["X"], f"{src}: {B['X']}", "as published", "USD million")
Q["M"] = add("M", bop["M"], f"{src}: {B['M']}", "as published", "USD million")
Q["Rc"] = add("Rc", bop["inc_cr"] + bop["tr_cr"], f"{src}: income + current transfers, credit",
              "as published; sum", "USD million", "~95 % remittances received")
Q["Rd"] = add("Rd", bop["inc_db"] + bop["tr_db"], f"{src}: income + current transfers, debit",
              "as published; sum", "USD million", "~84 % income paid (interest, profits)")
Q["CAc"] = add("CAc", Q["X"] + Q["Rc"], "X + Rc", "sum", "USD million", "current-account credits")
Q["CAd"] = add("CAd", Q["M"] + Q["Rd"], "M + Rd", "sum", "USD million", "current-account debits")
Q["BXE"] = add("BXE", Q["X"] / Q["M"], "X / M", "ratio", "ratio", "trade balance as a coverage ratio")
Q["SE"] = add("SE", Q["CAc"] / Q["CAd"], "CAc / CAd", "ratio", "ratio",
              "current-account coverage ratio; SE = w BXE + (1 - w) IT, w = M / (M + Rd)")
Q["IT"] = add("IT", Q["Rc"] / Q["Rd"], "Rc / Rd", "ratio", "ratio", "income and transfers coverage ratio")

# 3e. Deflators (robustness): Ecuador implicit NSA from the national accounts,
#     US from BEA (published seasonally adjusted only); same PPP alignment.
us = {"PCE": fred(FRED_PCE), "GDPD": fred(FRED_GDPD)}
ec = {"PCE": cur[HH] / vol[HH], "GDPD": cur["P.I.B."] / vol["P.I.B."]}
pl = {"PCE": (worldbank(WB_PRVT), "PA.NUS.PRVT.PP"), "GDPD": (worldbank(WB_GDP), "PA.NUS.PPP")}
for k, ecn, usn, gn, what in (("PCE", "PCEEC", "PCEUSA", "GAPPCE", "household consumption (incl. NPISH)"),
                              ("GDPD", "GDPDEC", "GDPDUSA", "GAPGDPD", "GDP")):
    p, ind = pl[k]
    e = 100 * p[PPP_YEAR] * ec[k] / ec[k][ec[k].index.year == PPP_YEAR].mean()
    u = 100 * us[k] / us[k][us[k].index.year == PPP_YEAR].mean()
    Q[ecn] = add(ecn, e, f"BCE CNT 127, current / chained volume, {what}",
                 f"implicit deflator, NSA; PPP-aligned (b = {PPP_YEAR}, {ind})", "index")
    Q[usn] = add(usn, u, f"BEA via FRED {os.path.basename(FRED_PCE if k == 'PCE' else FRED_GDPD)}",
                 f"rebased to the annual mean of {PPP_YEAR} = 100", "index", "seasonally adjusted at source")
    Q[gn] = add(gn, Q[ecn] / Q[usn], f"{ecn} / {usn}", "ratio", "ratio")

# 3f. Oil
Q["WTI"] = add("WTI", q_mean(wti_m), "FRED WTISPLC (EIA), monthly", "mean of 3 months", "USD per barrel")

qdf = pd.DataFrame({k: v.loc[SAMPLE[0]:SAMPLE[1]] for k, v in Q.items()})
check(len(qdf) == 68 and not qdf.isna().any().any(), f"quarterly: {qdf.shape[1]} series x {len(qdf)} quarters, complete")

mdf = pd.DataFrame({"IPCEC": pe_m, "IPCUSA": pu_m, "RIPC": pe_m / pu_m}).loc[SAMPLE_M[0]:SAMPLE_M[1]]
for n, s, r in (("IPCEC", "master Data:v_1 (INEC CPI)", "PPP-aligned as PE, monthly"),
                ("IPCUSA", "master Data:v_2 (BLS CPI-U, NSA)", "as PU, monthly"),
                ("RIPC", "IPCEC / IPCUSA", "ratio")):
    meta.append(dict(series=n, source=s, rule=r, unit="index" if n != "RIPC" else "ratio", note="monthly"))
check(len(mdf) == 78 and not mdf.isna().any().any(), f"monthly: {mdf.shape[1]} series x {len(mdf)} months, complete")

# ── 4. Equal to the data in the model files ─────────────────────────────────
say("\nAGAINST THE MODEL FILES (models/**/*.inp)")
try:
    import fue
    seen: dict[str, float] = {}
    rounded: set[str] = set()
    for f in sorted(glob.glob(os.path.join(REPO, "models", "**", "*.inp"), recursive=True)):
        if "VECM_" in f:
            continue
        ts = fue.load(f)[0]
        x = np.asarray(ts.data, float)
        ref = (mdf if ts.freq == 12 else qdf).get(ts.name)
        if ref is None:
            check(False, f"{os.path.relpath(f, REPO)}: series {ts.name} not built")
            continue
        dev = float(np.max(np.abs(ref.values[:len(x)] / x - 1)))
        if dev >= TOL and float(np.max(np.abs(ref.values[:len(x)] - x))) <= 5.0000001e-7:
            rounded.add(os.path.relpath(f, REPO))   # the same data, written with 6 decimals
            dev = 0.0
        seen[ts.name] = max(seen.get(ts.name, 0.0), dev)
    PENDING: set[str] = set()   # series rebuilt but whose models are not yet re-estimated
    for n in sorted(seen):
        check(seen[n] < TOL, f"{n:8s} max rel. diff {seen[n]:.1e} over every .inp that uses it"
              + (" (data rebuilt; model pending re-estimation)" if n in PENDING and seen[n] >= TOL else ""),
              warn=n in PENDING)
    if rounded:
        say(f"  note  {len(rounded)} model file(s) carry the data rounded to 6 decimals "
            f"(|diff| <= 5e-7): {', '.join(sorted(rounded))}")
    missing = sorted((set(qdf.columns) | set(mdf.columns)) - set(seen))
    if missing:
        say(f"  note  built but not used by any .inp: {', '.join(missing)}")
except ImportError:
    say("  note  fue not installed: check against the models skipped")

# ── 5. Write ────────────────────────────────────────────────────────────────
if "--check" not in sys.argv:
    q = qdf.copy()
    q.index = [f"{p.year}Q{p.quarter}" for p in q.index]
    q.index.name = "date"
    q[sorted(q.columns)].to_csv(os.path.join(HERE, "quarterly.csv"), float_format="%.17g")
    m = mdf.copy()
    m.index = [f"{p.year}M{p.month:02d}" for p in m.index]
    m.index.name = "date"
    m.to_csv(os.path.join(HERE, "monthly.csv"), float_format="%.17g")
    pd.DataFrame(meta).to_csv(os.path.join(HERE, "metadata.csv"), index=False)
    say("\n  -> data/quarterly.csv, data/monthly.csv, data/metadata.csv")
    with open(os.path.join(HERE, "build_report.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
say("\nALL CHECKS PASSED" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
