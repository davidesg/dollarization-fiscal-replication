# Fiscal VEC: SPNF expenditure and revenue (drvec, 2026-10-10)

Univariates from `../MACRO/` (art, guided). Column order: REV in the ∇Y₂
block, G in Y₁, so W = g + b·re and the budget-constraint vector is b = −1.
p = 2 (AR(1) in ∇ in both + 1). Case `pre` (both drifts free, as in the
univariates).

| file | REV model | G model |
|---|---|---|
| `REV.pre` | `REV_m03_ar1` (CFDD 2008Q1 + oil step 2008Q4×3) | `G_m02_ar1` (CFDD 2008Q2) |
| `REVno.pre` | `REV_m05_nooil` (CFDD only; the oil fall left in the stochastic part) | same |

| run | result |
|---|---|
| `rank_p{1,2,3}_pre`, `boot499_p2_pre` | with the oil step: LR(r=0) 19.8 / 11.1 / 12.6; bootstrap p = 0.096; free b 0.78; (1, −1) LR 11.0 and nobody corrects with it imposed — **discarded**: the step gives REV a break that belongs to the ratio |
| `rankA_p{1,2,3}_pre`, `bootA499_p2_pre` | **variant A**: LR(r=0) 34.5 / **29.9** / 16.4; **bootstrap p = 0.002** (p = 2) → r = 1 |
| `fitA_p2_pre_r1` | free: b = 1.10 (0.02); α_G −0.47 (t −3.6), α_REV +0.14 (p 0.45) |
| `fitA_p2_pre_r1_b1` | **adopted: β = (1, −1) imposed** (`-fixb2 -1`); α_G −0.39 (t −4.0), α_REV −0.06 (t −0.4). LR against free 9.8: b ≠ 1 only tilts the vector to absorb the 2008 mean break of the relation (TAU), no economic reading |

Reading: expenditure and revenue cointegrate one-to-one; **expenditure does
the correcting** (≈ 40 % of a gap closed per quarter, half-life ≈ 1.4 q) and
revenue, driven by oil, is weakly exogenous. Under dollarization (no monetary
financing) the adjustment falls on spending.

## 28-oct-2026: ingresos verificables del BCE

`REVnoBCE.pre` = `../MACRO/REV_BCE/REVbce_g06_nooil_ar1.pre` (ingresos desde los
ficheros del BCE; la `v_4` de la hoja maestra no los reproduce desde 2012).
Runs `bce_rank_p{1,2,3}`, `bce_boot499_p2` (LR 22.5, **p 0.004** → r = 1),
`bce_fit_r1` (β libre −1.12), `bce_fit_r1_b1` (**adoptado**: β = (1, −1);
α_G −0.31 (t −3.6), α_REV −0.04; LR frente a libre 7.37). Lectura en la Sección 6.1 del paper.
