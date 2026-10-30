# Data: sources, construction and checks

Every number the models use is built by one script from the files as they
were downloaded:

```
data/raw/            the source files, unmodified (MANIFEST.csv: source, URL, download date, SHA-256)
   │
   └── data/build_data.py
          │  checks every input against its SHA-256
          │  cross-checks the master workbook against the official publications
          │  builds the 29 series (rules below)
          │  checks each series against the data stored in every model file (models/**/*.inp)
          ▼
data/quarterly.csv   2003Q1–2019Q4, 26 series
data/monthly.csv     2002M01–2008M06, 3 series (Proposition 1)
data/metadata.csv    source, rule, unit and note of every series
data/build_report.txt  the log of every check
```

Run `python data/build_data.py` (or `--check` to verify without writing).
The last check guarantees that the data in `data/*.csv` are exactly the data
the estimates in `models/` were computed on (relative difference < 1e-9;
in practice < 3e-15).

## 1. Source files (`data/raw/`)

| file | source | downloaded | used for |
|---|---|---|---|
| `master/15-05-2024_Data_vf.xlsx` | master workbook compiled by A. E. Bunce from INEC, BLS and Banco Central del Ecuador (BCE) publications | compiled 2024-05-15 | CPI Ecuador, CPI-U, SPNF expenditure and revenue, nominal GDP, balance of payments |
| `inec/SERIE_HISTORICA_IPC_12_2019.xls` | INEC, CPI base 2014 = 100, historical series 1969–2019 (December 2019 release) | 2026-10-28 | check of `v_1` |
| `bls/CUUR0000SA0_*.json` | BLS, CPI-U NSA, public API | 2026-10-28 | check of `v_2` |
| `bce_bop/boletin69_1_BdPNormalizada.xls` | BCE, balance-of-payments bulletin nº 69 (BPM5), file of 2019-12-20 | 2026-10-28 | check of the balance of payments 2003–2015 |
| `bce_bop/boletin87_1_BP_Normalizada.xlsx` | BCE, balance-of-payments bulletin nº 87 (BPM6), file of 2024-06-28 | 2026-10-28 | check of the balance of payments 2016–2019 |
| `bce_cnt/tou_127_202401.xlsx` | BCE, *Cuentas Nacionales Trimestrales*, release 127 (2024Q1) | 2026-10-07 | real and nominal GDP, government and household consumption, implicit deflators; check of the master GDP |
| `bce_spnf/OperSPNF_Historico.xlsx` | BCE, *Operaciones del Sector Público No Financiero*, historical series 2000–2011 | 2026-05-25 | **SPNF revenue 2003–2011**; check of the master SPNF series |
| `bce_spnf/OperSPNF_DOLARES.xlsx` | BCE, *Operaciones del SPNF*, series under the IMF GFSM 2014 (2012 annual; monthly from 2013) | 2026-05-25 | **SPNF revenue 2012–2019**; check of the master SPNF series |
| `fred/WTISPLC_2026-05-26.xlsx` | FRED, WTISPLC: spot crude oil price, West Texas Intermediate (EIA), monthly | 2026-05-26 | WTI |
| `fred/DPCERD3Q086SBEA_2026-10-09.csv` | FRED, DPCERD3Q086SBEA: PCE implicit price deflator (BEA), quarterly, SA | 2026-10-09 | US consumption deflator |
| `fred/GDPDEF_2026-10-09.csv` | FRED, GDPDEF: GDP implicit price deflator (BEA), quarterly, SA | 2026-10-09 | US GDP deflator |
| `worldbank/ECU_PA.NUS.PRVT.PP.json` | World Bank WDI, PA.NUS.PRVT.PP: PPP conversion factor, household final consumption, Ecuador (vintage of 2026-07-13) | 2026-10-07 | PPP alignment of the CPIs and of the consumption deflator |
| `worldbank/ECU_PA.NUS.PPP.json` | World Bank WDI, PA.NUS.PPP: PPP conversion factor, GDP, Ecuador (vintage of 2026-07-13) | 2026-10-07 | PPP alignment of the GDP deflator |

URLs and SHA-256 of every file are in `raw/MANIFEST.csv`.

**Re-download checks (2026-10-28).**
- **FRED:** WTISPLC, DPCERD3Q086SBEA and GDPDEF downloaded again are identical over 2003–2019 to the archived files.
- **World Bank PPP:** the vintage of 2026-10-08 has the same 2011 value, the anchor of the alignment. Some other years have been revised; they only enter the cross-round check of §4.
- **BCE SPNF files:** the BCE now serves them through an interactive (Power BI) page, and no stable file URL could be recorded.

### What the master workbook contains, and where each column comes from

The master workbook has these sheets:
- `Data`: monthly, 1999M9–2024M2;
- `Data trim`: quarterly;
- `Metadata`.

It was compiled from the official publications, but its `Metadata` sheet
names the variables without recording their sources or download dates. We
traced every column used here back to the official file it comes from and
archived that file in `raw/`. `build_data.py` re-checks each one on every
run:

| column | series | official source (file in `raw/`) | result |
|---|---|---|---|
| `Data:v_1` | CPI Ecuador, base 2014 = 100 | INEC, historical series to 2019M12 (`inec/SERIE_HISTORICA_IPC_12_2019.xls`) | **identical**, 1999M10–2019M12 |
| `Data:v_2` | CPI-U, all items, NSA, 1982–84 = 100 | BLS, CUUR0000SA0 (`bls/*.json`) | **identical**, 1999M10–2024M2 |
| `Data:v_3` | SPNF expenditure, monthly | BCE *Operaciones del SPNF*: "Gastos totales" (accrual) to 2011 (`bce_spnf/OperSPNF_Historico.xlsx`); "Total erogaciones" from 2012 (`bce_spnf/OperSPNF_DOLARES.xlsx`) | **identical** 2003–2011 (to USD 10,000). From 2012: identical except two months of 2013–2014 (USD 11 m and 7 m) and USD 0.15 m in 2012, revised by the BCE since |
| `Data:v_4` | SPNF revenue, monthly | as `v_3`. In the workbook `v_4 = v_3 + v_5` exactly (`v_5` = overall balance) | **identical** 2003–2011; **from 2012 not reproduced** (§7) |
| `Data trim:v_10` | nominal GDP, quarterly | BCE *Cuentas Nacionales Trimestrales*, release 127, `Dem_Corr_bru` (`bce_cnt/tou_127_202401.xlsx`) | **identical** (6e-8) |
| `Data trim`: exports and imports of goods and services; income and current transfers, credit and debit | balance of payments, quarterly | BCE *Boletín de Balanza de Pagos*: **nº 69** (5th manual, BPM5) for 2003–2015 (`bce_bop/boletin69_1_BdPNormalizada.xls`); **nº 87** (6th manual, BPM6) for 2016–2019 (`bce_bop/boletin87_1_BP_Normalizada.xlsx`) | **identical** in both periods (to 1e-11) |

**The balance of payments splices two manuals in 2016.** BPM5 "renta" and
"transferencias corrientes" become BPM6 primary and secondary income. The
two manuals overlap in 2016–2019Q3, and over that span they differ by up to
USD 286 m a quarter in exports, 269 m in imports, 79 m in income paid and
147 m in transfers received. The workbook takes BPM5 up to 2015 and BPM6
from 2016, with no adjustment. The univariate models of X, M, CAc and CAd
see no intervention there (see their guiones).

## 2. Construction rules

All series enter **not seasonally adjusted**. Seasonality is modelled inside
each univariate model, with deterministic harmonics validated by the
seasonal tests, or a seasonal difference where the tests require it. The
systems inherit it from the univariate models. Adjusting the series
beforehand with X-13 or TRAMO-SEATS would put an external filter into the
VAR. Such filters distort short-run dynamics and unit-root and
cointegration tests (Granger and Siklos 1995). The only exception is the
two US deflators, which BEA publishes seasonally adjusted only.

**Temporal aggregation.** Applied only to monthly series:

1. **Price indices and prices** are averaged over the 3 months. This is
   the statistical agencies' convention, and it is consistent with GDP and
   flow accounts that measure the whole period.
2. **Flows** (expenditure, revenue) are summed over the 3 months.
3. **Ratios** are ratios of the quarterly aggregates, never means of
   monthly ratios. Examples: Σ expenditure / quarterly GDP; X/M.
4. **Natively quarterly series** (GDP, balance of payments, deflators) are
   taken as published. Nothing is interpolated.
5. Only complete quarters are kept.

**Why quarterly, and why Proposition 1 is monthly.**
- The VAR is quarterly because G/Y is: GDP exists only quarterly.
- Proposition 1 uses only prices, which are monthly. Its window
  (2002–2008) is short, so aggregating it would cut its observations to a
  third.
- Temporal aggregation preserves the cointegrating rank and vector
  (Granger and Siklos 1995; Marcellino 1999). The power of the tests
  depends on the span in years more than on the frequency (Shiller and
  Perron 1985; Hakkio and Rush 1991; Pierse and Snell 1995).
- Aggregation does change the short-run dynamics. Averaging a random walk
  induces an MA(1) with ρ₁ = 0.25 in its differences (Working 1960; Tiao
  1972; Brewer 1973; Wei 2006, ch. 20). Half-lives estimated from averaged
  data are biased upwards (Taylor 2001). For this reason the monthly RIPC
  and the quarterly VECM half-lives should not be compared as the same
  magnitude.

**External accounts as ratios, not balances.** BXE = X/M and SE =
credits/debits. A balance such as X − M changes sign and admits no
logarithm, while ln(X/M) = ln X − ln M. If ln(X/M) is stationary, X and M
cointegrate with vector (1, −1).

## 3. The series

| series | construction | unit |
|---|---|---|
| `PE` | CPI Ecuador (`v_1`), PPP-aligned (§4), quarterly mean | index, US level of 2011 = 100 |
| `PU` | CPI-U (`v_2`), rebased to the annual mean of 2011 = 100, quarterly mean | index |
| `GAP` | `PE / PU`: Ecuador's price level relative to the US | ratio |
| `GY` | Σ₃ SPNF expenditure (`v_3`) / quarterly nominal GDP (`v_10`) | ratio |
| `G` | Σ₃ SPNF expenditure (`v_3`) | USD million |
| `REV` | Σ₃ SPNF revenue from the BCE files (not the workbook's `v_4`, §7): historical "Total Ingresos" 2003–2011; current "TOTAL INGRESOS" 2013–2019; 2012 = the BCE annual total (USD 35,335.2 m), distributed over the months with the monthly profile of `v_4` | USD million |
| `TAU` | `G / REV` (100 ln TAU ≈ deficit in % of revenue) | ratio |
| `YN` | nominal GDP, CNT 127 `Dem_Corr_bru` | USD million |
| `YR` | real GDP, chained volume, CNT 127 `Dem_Cad_bru` | USD million of 2018 |
| `X`, `M` | exports, imports of goods and services (balance of payments) | USD million |
| `Rc`, `Rd` | income + current transfers, credit / debit (Rc ≈ 95 % remittances; Rd ≈ 84 % income paid) | USD million |
| `CAc`, `CAd` | X + Rc, M + Rd: current-account credits and debits | USD million |
| `BXE` | X / M | ratio |
| `SE` | CAc / CAd. It is the **current-account** coverage ratio, not service exports; SE = w·BXE + (1 − w)·IT exactly, with w = M/(M + Rd) ≈ 0.89 | ratio |
| `IT` | Rc / Rd | ratio |
| `PCEEC`, `GDPDEC` | Ecuador's implicit deflators, current / chained volume (CNT 127, NSA): household consumption (incl. NPISH), GDP; PPP-aligned (§4) | index |
| `PCEUSA`, `GDPDUSA` | BEA implicit deflators (FRED), rebased to the annual mean of 2011 = 100 (SA at source) | index |
| `GAPPCE`, `GAPGDPD` | Ecuador / US deflator ratios | ratio |
| `WTI` | FRED WTISPLC, quarterly mean | USD per barrel |
| `IPCEC`, `IPCUSA`, `RIPC` | monthly CPIs, aligned as `PE`, `PU`, and their ratio, 2002M01–2008M06 | index, ratio |

The models take logs (Box-Cox λ = 0) of all of them.

## 4. PPP alignment of the price levels

`GAP` and `RIPC` are ratios of price **levels**, so that the level test of
Proposition 1 measures the distance to absolute PPP.

**Alignment formula.**

  R_t = PLI_b × (CPI_EC,t / mean_b CPI_EC) / (CPI_US,t / mean_b CPI_US)

- **b = 2011**, a round of the International Comparison Program (ICP),
  where PPPs are measured rather than extrapolated.
- **Base = the annual mean of b**, not a single month. ICP PPPs refer to
  annual average prices, and a single month (December is very seasonal in
  Ecuador) adds noise.
- **PLI_b = PA.NUS.PRVT.PP**, the household-consumption PPP: the ICP
  aggregate closest to a CPI basket. Ecuador uses the US dollar, so the
  factor *is* Ecuador's price level relative to the US. No exchange rate
  enters. PLI₂₀₁₁ = 0.5478.
- **One normalisation** for the quarterly GAP and the monthly RIPC.

**Consistency across ICP rounds.** The level is extrapolated from 2011 with
the CPIs and compared with the measured PPP:
- **2017:** +3.7 log points;
- **2021:** +10.6 log points (out of sample);
- **2005:** 0.0, but in the current World Bank vintage the 2005 value is a
  backcast from 2011, not an independent measurement.

Discrepancies of this size across rounds are documented (Deaton and Heston
2010). They bound the uncertainty of the **level**.

**What the alignment changes.** In logs the alignment is a constant:
- **unchanged:** θ, the adjustment coefficients and every cointegration
  test;
- **changed:** the level of GAP, the constant of the cointegrating vector
  and the level test of the RIPC.

**What it replaced.**
- The previous quarterly normalisation (CPIs rebased to December 2010, with
  a factor of undocumented origin) was 0.55 log points from this one.
- The previous monthly RIPC (rebased to December 2014 with the 2014 GDP
  PPP) was 8.9 log points lower.

The deflators are aligned in the same way, with the PPP of the same concept:
PA.NUS.PRVT.PP for household consumption and PA.NUS.PPP for GDP.

## 5. Definition changes in public expenditure

The SPNF expenditure series is the official, public one. It has two breaks
in definition, which the univariate model of G/Y treats as interventions
(`models/GY_pasada2/GY_guion.json`):

**2008: the CFDD enters.** From January 2008 the historical series includes
the financing of the CFDD (*Cuenta de Financiamiento de Derivados
Deficitarios*), which pays for fuel imports, under "Otros" in current
expenditure. That item rises from 3.1 % of GDP in 2007 to 9.1 % in 2008:
about 6 of the 10.9 points of the 2007–2008 jump in G/Y. In substance the
CFDD is a fuel subsidy, that is, public expenditure. Its entry in 2008 is
nonetheless a change of registration, visible from 2008Q2. The model of G/Y
controls for it with a step in 2008Q2, justified by this information from
outside the sample.

**2012: new methodology.** The series is reprocessed under the IMF GFSM
2014. No year is published under both definitions.

## 6. GDP

The nominal GDP (`v_10`) is the BCE's official quarterly series: base 2018,
retropolated 2000–2017, current prices, NSA, releases 126/127. A later
release (136, 2026Q2) leaves the annual totals of 2003–2019 unchanged and
reshapes only the quarterly profile of 2018–2019 (up to ±3 % in Q2 and
Q4).

## 7. Open issues

1. **SPNF revenue from 2012: the workbook is not used.** In the workbook,
   revenue is expenditure plus the overall balance (`v_4 = v_3 + v_5`). Up
   to 2011 it equals the BCE historical series. From 2012 its overall
   balance is smaller in magnitude than the current BCE "Resultado global":
   - 2013: −4,348 against −7,908 USD m;
   - 2016: −7,314 against −10,109 USD m.

   No row of the current BCE file and no monthly bulletin reproduces it.
   `REV` (and with it `TAU`) is therefore built from the BCE files
   themselves (§3). One part is not directly verifiable: the split of
   2012 into months, which takes the workbook's monthly profile scaled to
   the BCE annual total.

   **Caveat on levels.** With the BCE revenue, the annual SPNF deficit is
   8 % of GDP in 2013–2014 and 10.4 % in 2016, above figures commonly
   reported for those years. The workbook's overall balance was closer to
   them. The two may measure revenue differently (for instance the
   registration of fuel-derivative sales). Levels of the deficit should be
   checked against an official source (MEF, IMF) before being quoted.
   The dynamics used in the models (orders of integration, the fiscal VEC)
   are the same with either revenue series (models/VECM_FISC/README.md).
2. **Vintages.** SPNF expenditure 2012–2014 and the 2018–2019 quarterly
   GDP profile have been revised slightly since the workbook was compiled
   (§1, §6). The analysis uses the workbook's vintage throughout. FRED and
   the 2011 World Bank PPP are unchanged as of 2026-10-28.

## References

- Brewer, K. R. W. (1973). Some consequences of temporal aggregation and systematic sampling for ARMA and ARMAX models. *Journal of Econometrics*, 1(2), 133–154.
- Deaton, A. and Heston, A. (2010). Understanding PPPs and PPP-based national accounts. *American Economic Journal: Macroeconomics*, 2(4), 1–35.
- Granger, C. W. J. and Siklos, P. L. (1995). Systematic sampling, temporal aggregation, seasonal adjustment, and cointegration. *Journal of Econometrics*, 66(1–2), 357–369.
- Hakkio, C. S. and Rush, M. (1991). Cointegration: how short is the long run? *Journal of International Money and Finance*, 10(4), 571–581.
- Marcellino, M. (1999). Some consequences of temporal aggregation in empirical analysis. *Journal of Business & Economic Statistics*, 17(1), 129–136.
- Pierse, R. G. and Snell, A. J. (1995). Temporal aggregation and the power of tests for a unit root. *Journal of Econometrics*, 65(2), 333–345.
- Shiller, R. J. and Perron, P. (1985). Testing the random walk hypothesis: power versus frequency of observation. *Economics Letters*, 18(4), 381–386.
- Taylor, A. M. (2001). Potential pitfalls for the purchasing-power-parity puzzle? *Econometrica*, 69(2), 473–498.
- Tiao, G. C. (1972). Asymptotic behaviour of temporal aggregates of time series. *Biometrika*, 59(3), 525–531.
- Wei, W. W. S. (2006). *Time Series Analysis: Univariate and Multivariate Methods*, 2nd ed., ch. 20. Pearson.
- Working, H. (1960). Note on the correlation of first differences of averages in a random chain. *Econometrica*, 28(4), 916–918.
