# Catálogo de sistemas multivariantes

Generado por `tables/make_docs.py`. Cada ficha: de qué univariante procede cada `.pre` (comparación por contenido con los modelos de art); las corridas que regenera `make_tables.py` con su resultado; el README del directorio y la lista de salidas.

## Índice

- Sistema central (G/Y | GAP) — `VECM_GAP_GY/`
- Central aumentado con BXE — `VECM_AUG/`
- Entradas exógenas (IT empotrada, por resta) — `VECM_XSYS/`
- Trivariante (G/Y, IPC_USA | IPC_EC) — `VECM_TRI/`
- Choque transitorio (IRF con bandas) — `VECM_TRI_IRF/`
- Submuestras de θ — `VECM_SUB/`
- θ recursivo y estabilidad de β — `VECM_REC/`
- Petróleo: WTI y G/Y — `VECM_WTI/`
- Robustez: deflactor del consumo — `VECM_PCE/`
- Robustez: deflactor del PIB (autónomo) — `VECM_GDPD/`
- Robustez: deflactor del PIB (guiado) — `VECM_GDPD_G/`
- VEC fiscal (gasto, ingresos) — `VECM_FISC/`
- VEC de las balanzas (créditos, débitos) — `VECM_BOP/`

### Sistema central (G/Y | GAP) — `VECM_GAP_GY/`

| `.pre` del sistema | univariante del que procede (mismo contenido) |
|---|---|
| `VECM_GAP_GY/GAP.pre` | `GAP/GAP_m04_ar3_noalt.pre` |
| `VECM_GAP_GY/GAP_noint.pre` | `GAP/GAP_m01_ar1.pre` |
| `VECM_GAP_GY/GY_M1.pre` | `GY_pasada2/GY_m03a_step0802.pre` |
| `VECM_GAP_GY/GY_M2.pre` | `GY_pasada2/GY_m03_step_pulse.pre` |
| `VECM_GAP_GY/GY_noint.pre` | `GY_m01_ar1.pre`, `GY_pasada2/GY_m01_ar1.pre` |

Corridas regeneradas por `make_tables.py` (en `tables/build/drvec/`):

| corrida | argumentos | resultado |
|---|---|---|
| `biv_rank` | `GY_M1.pre GAP.pre 4 0 0 -case 2 -lrtest -bootstrap 999` | r=0: LR 19.27, boot p 0.009 (999) |
| `biv_wx` | `GY_M1.pre GAP.pre 4 0 1 -case 2 -fdhess -weakex 1` | β GY -0.386, GAP 1.000; α GY -0.000, GAP -0.109 (0.031); logL -270.500 |
| `biv_free` | `GY_M1.pre GAP.pre 4 0 1 -case 2 -fdhess` | β GY -0.372, GAP 1.000; α GY -0.556 (0.428), GAP -0.109 (0.032); logL -269.725 |

### Central aumentado con BXE — `VECM_AUG/`

| `.pre` del sistema | univariante del que procede (mismo contenido) |
|---|---|
| `VECM_AUG/BXE.pre` | `EXT/BXE/BXE_m04_ar1_noalt.pre` |
| `VECM_AUG/GAP.pre` | `GAP/GAP_m04_ar3_noalt.pre` |
| `VECM_AUG/GY.pre` | `GY_pasada2/GY_m03a_step0802.pre` |
| `VECM_AUG/m05/BXE.pre` | `EXT/BXE/BXE_m05_i0804x2.pre` |
| `VECM_AUG/m05/GAP.pre` | `GAP/GAP_m04_ar3_noalt.pre` |
| `VECM_AUG/m05/GY.pre` | `GY_pasada2/GY_m03a_step0802.pre` |

Corridas regeneradas por `make_tables.py` (en `tables/build/drvec/`):

| corrida | argumentos | resultado |
|---|---|---|
| `aug_rank` | `GY.pre BXE.pre GAP.pre 4 0 0 -case 2 -lrtest -bootstrap 499` | r=0: LR 24.46, boot p 0.040 (499); r=1: LR 9.22, boot p 0.396 (499) |
| `aug_r2` | `GY.pre BXE.pre GAP.pre 4 0 2 -case 2 -fdhess` | β GY 0.034, BXE 1.000, GAP 0.000; α GY -0.226 (0.166), BXE -0.588 (0.153), GAP 0.003 (0.012); logL -481.862 |

<details><summary>README `VECM_AUG/m05/README.md`</summary>

#### VECM_AUG re-estimated with the adopted BXE (m05, 2026-10-10)

The parent directory used `BXE_m04_ar1_noalt` (2008Q4 step). The adopted
univariate is now `EXT/BXE/BXE_m05_i0804x2`: a ×2 impulse in 2008Q4, which
is transitory. The m04 step had a gain of −3.2 that was not significant
(Wald p 0.34). The other inputs did not change: `GY.pre`, `GAP.pre` and the
`net_*.txt` link files. `run_aug_m05.sh` reproduces every run.

| quantity | m04 (`..`) | m05 (here) |
|---|---|---|
| rank, LR r = 0 / r ≤ 1 (p = 4, case 2) | 25.0 / 9.5 | 24.5 / 9.2 |
| bootstrap 499, r = 0 / r ≤ 1 | p 0.034 / 0.384 | p 0.040 / 0.396 |
| r = 1: β (G/Y, BXE), α_BXE, α_GAP | −0.387, 0.376; −1.13; −0.048 (p 0.27) | −0.360, 0.334; −1.11; −0.054 (p 0.24) |
| r = 2, p = 4: θ (ec2) | 0.371 (0.034) | **0.371 (0.034)** |
| α_GAP on ec2 / on ec1 | −0.100 (t −3.1) / p 0.75 | −0.101 (t −3.1) / p 0.81 |
| ec1 = BXE + b·G/Y | b −0.040 (p 0.64) | b 0.034 (p 0.71) |
| G/Y weak exogeneity χ²(2) | p 0.24 | p 0.19 |
| GAP ← ∇BXE lags | p 0.17–0.81 | p 0.15–0.88 |
| Q(72) / multivariate JB | p ≈ 1 / 0.97 | p ≈ 1 / 0.95 |
| r = 2, p = 2: θ | 0.395 | 0.395 |
| `-xlink` GAP ← BXE (0,0,0): ω₀ | −0.0173 (0.0075), p 0.02 | −0.0171 (0.0075), LR 5.0, p 0.023 |
| b = 1 (`xl_b1`) | ω ≈ 0, p 0.97 | ω ≈ 0, p 0.99 |
| s = 1 (`xl_s1`): ω₁ | p 0.32 | p 0.34 |
| r = 1 (`xl_r1`): δ | p 0.33 | p 0.37 |

**Nothing changes.** θ is invariant to the external sector, and the GAP does
not respond to ec1 or to the lags of ∇BXE. The only effect is a small
contemporaneous level effect of BXE on GAP. It cannot be told apart from the
innovation correlation, so its direction is not identified.

The old C3 variant (BXE without its 2008 step subtracted) is superseded.
m05 has no permanent step left to subtract.

The `-xlink` runs also need `-xpre BXE.pre`, which supplies the input files.

</details>

### Entradas exógenas (IT empotrada, por resta) — `VECM_XSYS/`

| `.pre` del sistema | univariante del que procede (mismo contenido) |
|---|---|
| `VECM_XSYS/GAP.pre` | `GAP/GAP_m04_ar3_noalt.pre` |
| `VECM_XSYS/GY.pre` | `GY_pasada2/GY_m03a_step0802.pre` |
| `VECM_XSYS/IT.pre` | `EXT/IT/IT_m00.pre` |

### Trivariante (G/Y, IPC_USA | IPC_EC) — `VECM_TRI/`

| `.pre` del sistema | univariante del que procede (mismo contenido) |
|---|---|
| `VECM_TRI/GAPc.pre` | sin copia idéntica (versión propia del sistema) |
| `VECM_TRI/GY.pre` | `GY_pasada2/GY_m03a_step0802.pre` |
| `VECM_TRI/PE.pre` | `PE/PE_m03_ar1.pre` |
| `VECM_TRI/PU.pre` | `PU/PU_m08_ar1_noalt.pre` |

Corridas regeneradas por `make_tables.py` (en `tables/build/drvec/`):

| corrida | argumentos | resultado |
|---|---|---|
| `tri_rank` | `GY.pre PU.pre PE.pre 2 0 0 -case pre -lrtest -bootstrap 499` | r=0: LR 18.74, boot p 0.050 (499); r=1: LR 5.64, boot p 0.034 (499) |
| `tri_r1` | `GY.pre PU.pre PE.pre 2 0 1 -case pre -fdhess` | β GY -0.437, PU -0.592, PE 1.000; α GY 0.258 (0.223), PU 0.006 (0.016), PE -0.067 (0.016); logL -280.690 |
| `tri_A` | `GY.pre PU.pre PE.pre 2 0 1 -case pre -weakex 2` | β GY -0.422, PU -0.603, PE 1.000; α GY 0.251 (0.213), PU -0.000, PE -0.068 (0.017); logL -280.755 |
| `tri_B` | `GY.pre PU.pre PE.pre 2 0 1 -case pre -fixb2row 2 -1` | β GY -0.193, PU -1.000, PE 1.000; α GY 0.092 (0.286), PU -0.005 (0.022), PE -0.074 (0.018); logL -283.237 |
| `tri_C` | `GY.pre PU.pre PE.pre 2 0 1 -case pre -fixb2row 2 -1 -weakex 2` | β GY -0.200, PU -1.000, PE 1.000; α GY 0.108 (0.278), PU -0.000, PE -0.075 (0.018); logL -283.265 |
| `tri3_r1` | `GY.pre PU.pre PE.pre 2 0 1 -case 3 -fdhess` | β GY -0.486, PU -0.512, PE 1.000; α GY 0.375 (0.218), PU 0.009 (0.015), PE -0.060 (0.018); logL -279.818 |
| `tri3_A` | `GY.pre PU.pre PE.pre 2 0 1 -case 3 -weakex 2` | β GY -0.456, PU -0.541, PE 1.000; α GY 0.364 (0.225), PU -0.000, PE -0.062 (0.018); logL -279.969 |
| `tri3_B` | `GY.pre PU.pre PE.pre 2 0 1 -case 3 -fixb2row 2 -1` | β GY -0.191, PU -1.000, PE 1.000; α GY 0.139 (0.288), PU -0.005 (0.021), PE -0.073 (0.018); logL -282.924 |
| `tri3_C` | `GY.pre PU.pre PE.pre 2 0 1 -case 3 -fixb2row 2 -1 -weakex 2` | β GY -0.197, PU -1.000, PE 1.000; α GY 0.154 (0.283), PU -0.000, PE -0.074 (0.018); logL -282.953 |
| `tri4_r1` | `GY.pre PU.pre PE.pre 2 0 1 -case pre -trend -fdhess` | β GY -0.434, PU -0.552, PE 1.000; α GY 0.271 (0.405), PU 0.006 (0.017), PE -0.068 (0.032); logL -280.689 |
| `tri4_A` | `GY.pre PU.pre PE.pre 2 0 1 -case pre -trend -weakex 2` | β GY -0.417, PU -0.459, PE 1.000; α GY 0.302 (0.388), PU -0.000, PE -0.072 (0.028); logL -280.742 |
| `tri4_B` | `GY.pre PU.pre PE.pre 2 0 1 -case pre -trend -fixb2row 2 -1` | β GY -0.449, PU -1.000, PE 1.000; α GY 0.161 (0.157), PU 0.007 (0.012), PE -0.058 (0.017); logL -280.763 |
| `tri4_C` | `GY.pre PU.pre PE.pre 2 0 1 -case pre -trend -fixb2row 2 -1 -weakex 2` | β GY -0.421, PU -1.000, PE 1.000; α GY 0.157 (0.171), PU -0.000, PE -0.059 (0.017); logL -280.878 |

### Choque transitorio (IRF con bandas) — `VECM_TRI_IRF/`

| `.pre` del sistema | univariante del que procede (mismo contenido) |
|---|---|
| `VECM_TRI_IRF/GAPc.pre` | sin copia idéntica (versión propia del sistema) |
| `VECM_TRI_IRF/GY.pre` | `GY_pasada2/GY_m03a_step0802.pre` |
| `VECM_TRI_IRF/PU.pre` | `PU/PU_m08_ar1_noalt.pre` |

### Submuestras de θ — `VECM_SUB/`

| `.pre` del sistema | univariante del que procede (mismo contenido) |
|---|---|
| `VECM_SUB/GAP_2005.pre` | sin copia idéntica (versión propia del sistema) |
| `VECM_SUB/GAP_2007.pre` | sin copia idéntica (versión propia del sistema) |
| `VECM_SUB/GAP_2010.pre` | sin copia idéntica (versión propia del sistema) |
| `VECM_SUB/GY_M1.pre` | `GY_pasada2/GY_m03a_step0802.pre` |

### θ recursivo y estabilidad de β — `VECM_REC/`

### Petróleo: WTI y G/Y — `VECM_WTI/`

| `.pre` del sistema | univariante del que procede (mismo contenido) |
|---|---|
| `VECM_WTI/GAP.pre` | `GAP/GAP_m04_ar3_noalt.pre` |
| `VECM_WTI/GY.pre` | `GY_pasada2/GY_m03a_step0802.pre` |
| `VECM_WTI/GYnoint.pre` | `GY_m01_ar1.pre`, `GY_pasada2/GY_m01_ar1.pre` |
| `VECM_WTI/WTI.pre` | `WTI_m01_i0804.pre` |
| `VECM_WTI/WTIraw.pre` | `WTI_m00.pre` |

Corridas regeneradas por `make_tables.py` (en `tables/build/drvec/`):

| corrida | argumentos | resultado |
|---|---|---|
| `wti_rank` | `WTI.pre GY.pre 2 0 0 -case 2 -lrtest -bootstrap 499` | r=0: LR 11.01, boot p 0.140 (499) |

### Robustez: deflactor del consumo — `VECM_PCE/`

| `.pre` del sistema | univariante del que procede (mismo contenido) |
|---|---|
| `VECM_PCE/GAPPCE.pre` | `DEFL/GAPPCE/GAPPCE_m02_ar1_s0804.pre` |
| `VECM_PCE/GY.pre` | `GY_pasada2/GY_m03a_step0802.pre` |
| `VECM_PCE/PCEEC.pre` | `DEFL/PCEEC/PCEEC_m01_ar1.pre` |
| `VECM_PCE/PCEUSA.pre` | `DEFL/PCEUSA/PCEUSA_m02_ar3.pre` |

Corridas regeneradas por `make_tables.py` (en `tables/build/drvec/`):

| corrida | argumentos | resultado |
|---|---|---|
| `pce_r1` | `GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -fdhess` | — |
| `pce_A` | `GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -weakex 2` | — |
| `pce_B` | `GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -fixb2row 2 -1` | — |
| `pce_C` | `GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -fixb2row 2 -1 -weakex 2` | — |
| `pce4_r1` | `GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -trend -fdhess` | — |
| `pce4_A` | `GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -trend -weakex 2` | — |
| `pce4_B` | `GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -trend -fixb2row 2 -1` | — |
| `pce4_C` | `GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -trend -fixb2row 2 -1 -weakex 2` | — |

### Robustez: deflactor del PIB (autónomo) — `VECM_GDPD/`

| `.pre` del sistema | univariante del que procede (mismo contenido) |
|---|---|
| `VECM_GDPD/GAPGDPD.pre` | `DEFL/GAPGDPD/GAPGDPD_m02_ar2.pre` |
| `VECM_GDPD/GDPDEC.pre` | `DEFL/GDPDEC/GDPDEC_m04_arma11.pre` |
| `VECM_GDPD/GDPDUSA.pre` | `DEFL/GDPDUSA/GDPDUSA_m01_ar1.pre` |
| `VECM_GDPD/GY.pre` | `GY_pasada2/GY_m03a_step0802.pre` |

### Robustez: deflactor del PIB (guiado) — `VECM_GDPD_G/`

| `.pre` del sistema | univariante del que procede (mismo contenido) |
|---|---|
| `VECM_GDPD_G/GAPGDPD.pre` | `DEFL/GAPGDPD_G/GAPGDPD_m03_x2_ar2.pre` |
| `VECM_GDPD_G/GDPDEC.pre` | `DEFL/GDPDEC_G/GDPDEC_m04_x2_ar2.pre` |
| `VECM_GDPD_G/GDPDUSA.pre` | `DEFL/GDPDUSA/GDPDUSA_m01_ar1.pre` |
| `VECM_GDPD_G/GY.pre` | `GY_pasada2/GY_m03a_step0802.pre` |

### VEC fiscal (gasto, ingresos) — `VECM_FISC/`

| `.pre` del sistema | univariante del que procede (mismo contenido) |
|---|---|
| `VECM_FISC/G.pre` | `MACRO/G/G_m02_ar1.pre` |
| `VECM_FISC/REVBCE.pre` | `MACRO/REV_BCE/REVbce_g04_ar1.pre` |
| `VECM_FISC/REVnoBCE.pre` | `MACRO/REV_BCE/REVbce_g06_nooil_ar1.pre` |

Corridas regeneradas por `make_tables.py` (en `tables/build/drvec/`):

| corrida | argumentos | resultado |
|---|---|---|
| `fisc_rank` | `REVnoBCE.pre G.pre 2 0 0 -case pre -lrtest -bootstrap 499` | r=0: LR 22.51, boot p 0.004 (499) |
| `fisc_free` | `REVnoBCE.pre G.pre 2 0 1 -case pre -fdhess` | β REV -1.117, G 1.000; α REV 0.133 (0.156), G -0.376 (0.113); logL -455.992 |
| `fisc_b1` | `REVnoBCE.pre G.pre 2 0 1 -case pre -fixb2 -1 -fdhess` | β REV -1.000, G 1.000; α REV -0.038 (0.112), G -0.312 (0.086); logL -459.677 |

<details><summary>README `VECM_FISC/README.md`</summary>

#### Fiscal VEC: SPNF expenditure and revenue (drvec, 2026-10-10)

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

##### 28-oct-2026: ingresos verificables del BCE

`REVnoBCE.pre` = `../MACRO/REV_BCE/REVbce_g06_nooil_ar1.pre` (ingresos desde los
ficheros del BCE; la `v_4` de la hoja maestra no los reproduce desde 2012).
Runs `bce_rank_p{1,2,3}`, `bce_boot499_p2` (LR 22.5, **p 0.004** → r = 1),
`bce_fit_r1` (β libre −1.12), `bce_fit_r1_b1` (**adoptado**: β = (1, −1);
α_G −0.31 (t −3.6), α_REV −0.04; LR frente a libre 7.37). Lectura en la Sección 6.1 del paper.

</details>

### VEC de las balanzas (créditos, débitos) — `VECM_BOP/`

| `.pre` del sistema | univariante del que procede (mismo contenido) |
|---|---|
| `VECM_BOP/CAc.pre` | `EXT/CAc/CAc_m03_ar1_noseas.pre` |
| `VECM_BOP/CAd.pre` | `EXT/CAd/CAd_m04_ar1x1.pre` |
| `VECM_BOP/M.pre` | `EXT/M/M_m03a_ar2.pre` |
| `VECM_BOP/Rc.pre` | `EXT/Rc/Rc_m00.pre` |
| `VECM_BOP/Rd.pre` | `EXT/Rd/Rd_m01_ar1.pre` |
| `VECM_BOP/X.pre` | `EXT/X/X_m03_ar1_noseas.pre` |

Corridas regeneradas por `make_tables.py` (en `tables/build/drvec/`):

| corrida | argumentos | resultado |
|---|---|---|
| `tb_rank` | `M.pre X.pre 2 0 0 -case pre -lrtest -bootstrap 499` | r=0: LR 15.51, boot p 0.028 (499) |
| `tb_free` | `M.pre X.pre 2 0 1 -case pre -fdhess` | β M -1.042, X 1.000; α M 0.282 (0.081), X -0.109 (0.159); logL -409.116 |
| `tb_b1` | `M.pre X.pre 2 0 1 -case pre -fixb2 -1 -fdhess` | β M -1.000, X 1.000; α M 0.232 (0.086), X -0.222 (0.134); logL -410.069 |
| `ca_rank` | `CAd.pre CAc.pre 2 0 0 -case pre -lrtest -bootstrap 499` | r=0: LR 14.86, boot p 0.034 (499) |
| `ca_free` | `CAd.pre CAc.pre 2 0 1 -case pre -fdhess` | β CAd -1.073, CAc 1.000; α CAd 0.305 (0.079), CAc 0.023 (0.127); logL -405.335 |
| `ca_b1` | `CAd.pre CAc.pre 2 0 1 -case pre -fixb2 -1 -fdhess` | β CAd -1.000, CAc 1.000; α CAd 0.263 (0.085), CAc -0.123 (0.119); logL -407.298 |
| `rt_rank` | `Rd.pre Rc.pre 2 0 0 -case pre -lrtest -bootstrap 499` | r=0: LR 6.89, boot p 0.256 (499) |

<details><summary>README `VECM_BOP/README.md`</summary>

#### Balance-of-payments VECs: credits and debits (drvec, 2026-10-10)

Not in the paper's original analysis. drvec adds the adjustment
coefficients α, which show **who corrects** each balance. Three bivariate
systems use the adopted univariates (art, guided, `../EXT/`). Column order:
the debit sits in the ∇Y₂ block and the credit in Y₁, so W = credit + b·debit
and the balance vector is b = −1. With β = (1, −1), **a positive α on the
debit corrects and a negative α on the credit corrects**. Case `pre` (drifts
free, as in the univariates).

| file | model |
|---|---|
| `X.pre` | `X_m03_ar1_noseas` (exports, credit) |
| `M.pre` | `M_m03a_ar2` (imports, debit) |
| `CAc.pre` | `CAc_m03_ar1_noseas` (current-account credits) |
| `CAd.pre` | `CAd_m04_ar1x1` (current-account debits) |
| `Rc.pre` | `Rc_m00` (rents and transfers, credits) |
| `Rd.pre` | `Rd_m01_ar1` (rents and transfers, debits) |

Rank, LR(r = 0) and bootstrap (499) p-value. The rule from the univariates
gives p = 3 (trade, current account). Γ(2) is not significant at p = 3
(Wald p 0.062 / 0.063), so **p = 2 in both**. Rents and transfers: p = 2.

| balance | p = 1 | p = 2 | p = 3 | runs |
|---|---|---|---|---|
| trade (M, X) | | 15.5, **boot p 0.028** | 9.2, boot p 0.188 | `TB_rank_p*`, `TB_boot_p*` |
| current account (CAd, CAc) | 30.2 | 14.9, **boot p 0.034** | 8.8, boot p 0.210 | `CA_rank_p*`, `CA_boot_p*` |
| rents and transfers (Rd, Rc) | 11.2 | 6.9, boot p 0.256 | | `RT_rank_p*`, `RT_boot_p2` |

Fits at p = 2, r = 1 (`*_fit_p2` free, `*_fitb1_p2` with `-fixb2 -1`):

| balance | free b (s.e.) | LR (1, −1) | α debit | α credit |
|---|---|---|---|---|
| trade | 1.04 (0.03) | 1.91 (p 0.17) | **α_M +0.23 (t 2.7)** | α_X −0.22 (p 0.09) |
| current account | 1.07 (0.04) | 3.93 (p 0.047) | **α_CAd +0.26 (t 3.2)** | α_CAc −0.12 (p 0.30) |
| rents and transfers | 0.64 (0.16) | 2.83 (p 0.09) | α_Rd −0.04 (p 0.41) | α_Rc −0.07 (p 0.004) |

The free fits read the same way. Trade: α_M +0.28 (t 3.5), α_X −0.11
(p 0.50). Current account: α_CAd +0.31 (t 3.9), α_CAc +0.02 (p 0.85).

**Adopted: p = 2, r = 1, β = (1, −1) imposed** for trade and the current
account (analyst's decision). A vector other than (1, −1) has no economic
reading. In the current account the restriction is rejected only at the
margin, and at p = 3 it is not rejected (LR 2.15, p 0.14). Rents and
transfers **do not cointegrate** (r = 0), consistent with IT being I(1).

Reading: the balances close one to one, and **the debits (imports) do the
correcting**: about 25 % of a gap closes per quarter, a half-life of about
2.4 quarters. The credits, mostly oil exports, are weakly exogenous. Under
dollarization the external adjustment goes through absorption, as the fiscal
one goes through expenditure (`../VECM_FISC/`).

`.out` and `.log` are not tracked (`.gitignore`). Rerun them with drvec on
these `.pre` files: `-case pre -lrtest`, `-bootstrap 499`, and `-fixb2 -1`.

</details>
