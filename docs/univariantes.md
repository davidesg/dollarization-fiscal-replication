# Catálogo de modelos univariantes

Generado por `tables/make_docs.py` a partir de los guiones de art y de las estimaciones regeneradas por `make_tables.py`. No editar a mano: las decisiones se cambian en el guion y se regenera.

Cada ficha: tablas del paper que alimenta, ficheros, reproducción del óptimo, estimaciones (λ, d, intervenciones, ARMA, μ), diagnosis, contrastes formales de d por los dos lados, y el guion completo: nodos decididos con su evidencia y todas las versiones con su estado y decisión (◀ = el modelo de la tabla).

## Índice

- [`WTI_m01_i0804.inp`](#wti_m01_i0804inp)
- [`DEFL/GAPGDPD_G/GAPGDPD_m03_x2_ar2.inp`](#deflgapgdpd_ggapgdpd_m03_x2_ar2inp)
- [`DEFL/GAPPCE/GAPPCE_m02_ar1_s0804.inp`](#deflgappcegappce_m02_ar1_s0804inp)
- [`DEFL/GDPDEC_G/GDPDEC_m04_x2_ar2.inp`](#deflgdpdec_ggdpdec_m04_x2_ar2inp)
- [`DEFL/GDPDUSA/GDPDUSA_m01_ar1.inp`](#deflgdpdusagdpdusa_m01_ar1inp)
- [`DEFL/PCEEC/PCEEC_m01_ar1.inp`](#deflpceecpceec_m01_ar1inp)
- [`DEFL/PCEUSA/PCEUSA_m02_ar3.inp`](#deflpceusapceusa_m02_ar3inp)
- [`EXT/BXE/BXE_m05_i0804x2.inp`](#extbxebxe_m05_i0804x2inp)
- [`EXT/CAc/CAc_m03_ar1_noseas.inp`](#extcaccac_m03_ar1_noseasinp)
- [`EXT/CAd/CAd_m04_ar1x1.inp`](#extcadcad_m04_ar1x1inp)
- [`EXT/IT/IT_m00.inp`](#extitit_m00inp)
- [`EXT/M/M_m03a_ar2.inp`](#extmm_m03a_ar2inp)
- [`EXT/Rc/Rc_m00.inp`](#extrcrc_m00inp)
- [`EXT/Rd/Rd_m01_ar1.inp`](#extrdrd_m01_ar1inp)
- [`EXT/SE/SE_m03_i0804x2.inp`](#extsese_m03_i0804x2inp)
- [`EXT/X/X_m03_ar1_noseas.inp`](#extxx_m03_ar1_noseasinp)
- [`GAP/GAP_m04_ar3_noalt.inp`](#gapgap_m04_ar3_noaltinp)
- [`GY_pasada2/GY_m03a_step0802.inp`](#gy_pasada2gy_m03a_step0802inp)
- [`MACRO/G/G_m02_ar1.inp`](#macrogg_m02_ar1inp)
- [`MACRO/REV_BCE/REVbce_g04_ar1.inp`](#macrorev_bcerevbce_g04_ar1inp)
- [`MACRO/TAU_BCE/TAUbce_g02_ar2_s0804x3.inp`](#macrotau_bcetaubce_g02_ar2_s0804x3inp)
- [`MACRO/YN/YN_m04_ar1_sar1.inp`](#macroynyn_m04_ar1_sar1inp)
- [`MACRO/YN/YN_m05_meg2.inp`](#macroynyn_m05_meg2inp)
- [`MACRO/YR/YR_m01_ar2.inp`](#macroyryr_m01_ar2inp)
- [`MACRO/YR/YR_m05_ar1.inp`](#macroyryr_m05_ar1inp)
- [`PE/PE_m03_ar1.inp`](#pepe_m03_ar1inp)
- [`PU/PU_m08_ar1_noalt.inp`](#pupu_m08_ar1_noaltinp)

### `WTI_m01_i0804.inp`

- **Tablas:** tab:ur_app «$\ln WTI_t$»
- **Ficheros:** especificación `WTI_m01_i0804.inp` · óptimo adoptado `WTI_m01_i0804.pre` · reestimado en `build/WTI_m01_i0804.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 2.2e-07); logL -263.3930

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | -70.3741 | 12.3334 | -5.71 |
| ω1 [det. 1] | 30.6533 | 12.3330 | 2.49 |
| ω2 [det. 1] | -32.6435 | 12.3330 | -2.65 |

- λ = 0, d = 1, D = 0; intervenciones: step 2008Q4 (×3)
- media de ∇ (o nivel si d = 0): sin μ; σ = 12.333
- residuos: Q(15) = 9.30 (gl 15, p 0.861); JB = 14.43 (p 0.001)
- lado d+1: SF Φ = 7.85 (críticos 10 % 1.06, 5 % 1.75), sobre AR sobreajustado; DCD⁺ LR 1.55, θ̂ 0.920
- lado d−1: DCD⁻ LR 141.75, θ̂ -0.104
- identificación (ADF / KPSS, p): d=0: 0.033 / 0.100; d=1: 0.000 / 0.100

**Guion** `WTI_guion.json` (serie WTI, creado 2026-10-05).

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 1 | PC1 | exploring | 561.7 | 15.999 | ✓ | 0.000 | lam=0, d=1 (decisión del analista: la serie deambula; reevaluar con Shin-Fuller/DCD), D=0 sin armónicos (HAC F=1.76 p=0.16) |
| 2 | PC2 ◀ | adopted | 539.4 | 12.333 | ✓ | 0.001 | Intervención Q4/2008×3 (step, 3 escalones), identificada por el dato (ΔAIC 4.7 frente a ×2) |
| 3 | PC3 | exploring | 561.1 | 12.154 | ✓ | 0.042 | Candidato d=0: AR(2)+mu+intervención 2008 en niveles, para Shin-Fuller (reevaluar d) |
| 4 | m03_i0804_s1404x4 | dead-end | 529.8 | 10.129 | ✓ | 0.621 |  |
| 5 | m04_mu | dead-end | 527.6 | 9.656 | ✓ | 0.465 | Media residual t=2.43 tras los dos escalones permanentes: se estima μ (la deriva entre caídas). |
| 6 | m05_no1502 | dead-end | 525.5 | 9.810 | ✓ | 0.568 |  |
| 7 | m06_s1404x2 | dead-end | 527.7 | 10.284 | ✓ | 0.522 |  |

**PC2** (adopted, 2026-10-05)
- ecuación: `∇[ln y_t] = I_t(1 itvs) + [1-φ(B)]⁻¹·a_t`
- motivo: Normalidad (JB=91.6) y suceso relevante; la intervención no cambia la identificación ARMA (paseo aleatorio)
- por qué se adopta: Revisión 29-oct-2026 (decisión del analista): ln WTI d=1, paseo aleatorio SIN deriva, escalón 2008T4 ×3. Una deriva en ∇ln WTI implicaría una tendencia creciente indefinida en el precio del petróleo, sin sentido económico; la μ de m04–m06 sólo compensa los dos escalones. No se interviene 2014T4: no hay justificación suficiente para esa intervención, aunque corregiría el JB (p 0.001), que se acepta. Es el modelo que entra en todos los sistemas de drvec (VECM_WTI/WTI.pre, mismo sha) y la fila WTI de tab:ur_app.

### `DEFL/GAPGDPD_G/GAPGDPD_m03_x2_ar2.inp`

- **Tablas:** tab:uni «$PGE/PGU$»; tab:ur_app «$\ln(PGE_t/PGU_t)$»
- **Ficheros:** especificación `DEFL/GAPGDPD_G/GAPGDPD_m03_x2_ar2.inp` · óptimo adoptado `DEFL/GAPGDPD_G/GAPGDPD_m03_x2_ar2.pre` · reestimado en `build/GAPGDPD_m03_x2_ar2.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 2.4e-05); logL -140.8176

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | -16.2846 | 1.9884 | -8.19 |
| ω1 [det. 1] | 4.9136 | 1.8735 | 2.62 |
| φ1 [AR regular 1] | 0.0904 | 0.1135 | 0.80 |
| φ2 [AR regular 1] | 0.4125 | 0.1203 | 3.43 |
| μ | 0.7725 | 0.4739 | 1.63 |

- λ = 0, d = 1, D = 0; intervenciones: step 2008Q4 (×2)
- media de ∇ (o nivel si d = 0): 0.77 (0.47); σ = 1.974
- residuos: Q(15) = 18.30 (gl 13, p 0.146); JB = 0.07 (p 0.966)
- lado d+1: SF Φ = 3.91 (críticos 10 % 1.06, 5 % 1.75); DCD⁺ LR 1.80, θ̂ 0.861
- lado d−1: DCD⁻ LR 12.94, θ̂ 0.281
- identificación (ADF / KPSS, p): d=0: 0.108 / 0.010; d=1: 0.000 / 0.058

**Guion** `DEFL/GAPGDPD_G/GAPGDPD_guion.json` (serie GAPGDPD, creado 2026-10-09).

| nodo | decidido | evidencia |
|---|---|---|
| dominio | ratio | [2026-10-09] Corrección de las expectativas: el deflactor de Ecuador entra EN BRUTO (NSA, BCE CNT 127); sólo el de EE. UU. (GDPDEF) está desestacionalizado. La ausencia de estacionalidad la establece el contraste (HAC F 1.27, p 0.29), no la construcción. |
| lambda | 0 | gap=-0.081; corr(nivel)=0.075; corr(log)=0.156; estadístico λ=1; regla de dominio `ratio` |
| d | 1 | d=0: ADF p=0.108, KPSS p=0.010; d=1: ADF p=0.000, KPSS p=0.058 |
| estacionalidad | D=0 (sin estacionalidad) | F-HAC=1.27, p=0.2920 |
| estacionalidad | D=0 (B1, armónicos deterministas) |  |
| ordenes | ARMA(2,0) | ARMA(2,0) sim=0.913; ARMA(0,2) sim=0.895; ARMA(1,2) sim=0.900 — sobre residuos de `GAPGDPD_m01_s0804.pre` |

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 5 | m00 | exploring | 325.6 | 2.663 | ✓ | 0.000 |  |
| 6 | m01_s0804 | exploring | 304.1 | 2.199 | ✗ | 0.554 |  |
| 9 | m02_ar2 | dead-end | 304.8 | 2.072 | ✓ | 0.881 |  |
| 10 | m03_x2_ar2 ◀ | adopted | 302.7 | 1.974 | ✓ | 0.966 |  |

**m03_x2_ar2** (adopted, 2026-10-09)
- ecuación: `∇[ln y_t] = μ + I_t(1 itvs) + [1-φ(B)]⁻¹·a_t`
- motivo: Coherencia con el componente: GDPDEC guiado pide 2008Q4×2 (×1 falla Treadway). Se reformula el escalón de m02 (×1) a ×2 manteniendo el AR(2) y μ, para comparar en la brecha. Decidido por el analista.
- por qué se adopta: Guiado: AR(2) completo + escalón 2008Q4×2 (ω₀ −16.3 t −8.2, ω₁ +4.9 t 2.62; efecto permanente −21.2 %, Wald p 0.000), coherente con el componente GDPDEC (×2, −21.7 %, AR(2) 0.10/0.40). LR ×2 frente a ×1: 6.38, 1 gl, p 0.012; AIC/BIC 291.6/302.7 frente a 296.0/304.9. Treadway ✓ (vecinos −1.53/+1.37, p 0.12). Diagnosis limpia (Q p-mín 0.12, JB p 0.97). Formales: SF 3.91, DCD sobredif θ̂ 0.861 LR 1.80 < 1.94, subdif LR 9.33: el par en f=0 COINCIDE en d=1. p del VECM = 3.

### `DEFL/GAPPCE/GAPPCE_m02_ar1_s0804.inp`

- **Tablas:** tab:uni «$PCE/PCU$»; tab:ur_app «$\ln(PCE_t/PCU_t)$»
- **Ficheros:** especificación `DEFL/GAPPCE/GAPPCE_m02_ar1_s0804.inp` · óptimo adoptado `DEFL/GAPPCE/GAPPCE_m02_ar1_s0804.pre` · reestimado en `build/GAPPCE_m02_ar1_s0804.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 5.1e-06); logL -102.8890

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | 3.4402 | 1.0080 | 3.41 |
| φ1 [AR regular 1] | 0.4925 | 0.1163 | 4.24 |
| μ | 0.5170 | 0.2672 | 1.93 |

- λ = 0, d = 1, D = 0; intervenciones: step 2008Q4 (×1)
- media de ∇ (o nivel si d = 0): 0.52 (0.27); σ = 1.121
- residuos: Q(15) = 20.47 (gl 14, p 0.116); JB = 8.17 (p 0.017)
- lado d+1: SF Φ = 7.26 (críticos 10 % 1.06, 5 % 1.75); DCD⁺ LR 2.49, θ̂ 0.907
- lado d−1: DCD⁻ LR 20.53, θ̂ 0.050
- identificación (ADF / KPSS, p): d=0: 0.144 / 0.010; d=1: 0.000 / 0.011

**Guion** `DEFL/GAPPCE/GAPPCE_guion.json` (serie GAPPCE, creado 2026-10-09).

| nodo | decidido | evidencia |
|---|---|---|
| dominio | ratio |  |
| lambda | 0 | gap=-0.154; corr(nivel)=0.352; corr(log)=0.506; estadístico λ=1 |
| d | 1 | d=0: ADF p=0.144, KPSS p=0.010; d=1: ADF p=0.000, KPSS p=0.011 |
| estacionalidad | D=0 (sin estacionalidad) | F-HAC=0.76, p=0.5225 |

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 5 | m00 | exploring | 231.9 | 1.323 | ✓ | 0.017 | Usuario confirma D=0 sin armónicos (HAC F=0.76 p=0.52). Modelo base ∇ln con μ para calibrar 2008 |
| 6 | m01_ar1 | exploring | 224.6 | 1.213 | ✓ | 0.021 | AR(1) antes que intervenir (como GAP IPC): PACF corta en 1; 2008 no distorsiona la identificación |
| 7 | m02_ar1_s0804 ◀ | adopted | 218.4 | 1.121 | ✓ | 0.017 | Prueba pedida por el analista: escalón Q4/2008 (como GAP del IPC, ω=+1.85) por coherencia; se mantiene sólo si ω es significativo y arregla el JB |
| 8 | m03_ar2 | dead-end | 222.6 | 1.121 | ✓ | 0.014 | Sobreparametrización de m02: AR(2) |
| 9 | m04_arma11 | dead-end | 222.6 | 1.121 | ✓ | 0.015 | Sobreparametrización de m02: ARMA(1,1) |
| 10 | m05_ar5 | dead-end | 231.7 | 1.089 | ✓ | 0.008 | Diagnóstico (no candidato): AR(5) completo para medir cuánto compra la barra del retardo 5 |
| 11 | m06_p0302 | dead-end | 218.2 | 1.085 | ✓ | 0.093 |  |

**m02_ar1_s0804** (adopted, 2026-10-09)
- ecuación: `∇[ln y_t] = μ + I_t(1 itvs) + [1-φ(B)]⁻¹·a_t`
- por qué se adopta: Modelo final de GAPPCE (cerrado por el analista 9-oct-2026): AR(1) + escalón Q4/2008 (ω=+3.44, t 3.4, LR 10.4 p≈0.001; espejo del desplome de PCEUSA; coherente con GAP IPC). AR(2), ARMA(1,1) no significativos; AR(5) diagnóstico LR 3.5, 4 gl, p≈0.47: la barra del retardo 5 (−0.34; 1/3 del par 2003Q2–2004Q3) no se modela. Salvedad: JB p 0.017 por asimetría (2003–04 convergencia post-dolarización, 2010Q1), sin suceso común; no se interviene. Formales: SF Φ=7.26 (d=1 basta), DCD sobredif θ̂=0.91 LR 2.49 → banda de cuasi-cancelación, d=1 por parsimonia (como PCEEC); subdif LR 15.7.
- problemas y salvedades: [diagnosis] el Jarque-Bera rechaza la normalidad (p=0.0168) [2026-10-10] Revisión 10-oct: el JB (p 0.017) lo explica un solo anómalo, 2003T2 (primera observación): con un impulso ahí (v11) el JB pasa (p 0.093) y el BIC no cambia (218.2 vs 218.4). Como no hay justificación extramuestral para intervenir 2003T2, no se interviene: m02 se mantiene con esta salvedad. Formales: SF 7.26, DCD θ̂ 0.91 (banda) → d=1.

### `DEFL/GDPDEC_G/GDPDEC_m04_x2_ar2.inp`

- **Tablas:** tab:uni «Ecuador»
- **Ficheros:** especificación `DEFL/GDPDEC_G/GDPDEC_m04_x2_ar2.inp` · óptimo adoptado `DEFL/GDPDEC_G/GDPDEC_m04_x2_ar2.pre` · reestimado en `build/GDPDEC_m04_x2_ar2.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 3.6e-05); logL -142.1051

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | -16.2250 | 2.0158 | -8.05 |
| ω1 [det. 1] | 5.4291 | 1.9061 | 2.85 |
| φ1 [AR regular 1] | 0.1008 | 0.1137 | 0.89 |
| φ2 [AR regular 1] | 0.4001 | 0.1202 | 3.33 |
| μ | 1.2415 | 0.4817 | 2.58 |

- λ = 0, d = 1, D = 0; intervenciones: step 2008Q4 (×2)
- media de ∇ (o nivel si d = 0): 1.24 (0.48); σ = 2.012
- residuos: Q(15) = 20.99 (gl 13, p 0.073); JB = 0.03 (p 0.986)
- lado d+1: SF Φ = 3.97 (críticos 10 % 1.06, 5 % 1.75); DCD⁺ LR 2.61, θ̂ 0.852
- lado d−1: DCD⁻ LR 13.68, θ̂ 0.492
- identificación (ADF / KPSS, p): d=0: 0.013 / 0.010; d=1: 0.000 / 0.033

**Guion** `DEFL/GDPDEC_G/GDPDEC_guion.json` (serie GDPDEC, creado 2026-10-09).

| nodo | decidido | evidencia |
|---|---|---|
| dominio | price_index | [2026-10-09] Corrección de las expectativas: la serie es el implícito del BCE EN BRUTO (NSA; Dem_Corr_bru/Dem_Cad_bru, CNT 127), no desestacionalizada. La estacionalidad hay que contrastarla (en el autónomo, HAC p 0.29). |
| lambda | 0 | gap=-0.127; corr(nivel)=0.237; corr(log)=0.364; estadístico λ=1; regla de dominio `price_index` |
| d | 1 | d=0: ADF p=0.013, KPSS p=0.010; d=1: ADF p=0.000, KPSS p=0.033 |
| estacionalidad | D=0 (sin estacionalidad) | F-HAC=1.28, p=0.2901 |
| estacionalidad | D=0 (B1, armónicos deterministas) |  |
| ordenes | ARMA(2,0) | ARMA(0,2)×(0,1)_4 sim=0.864; ARMA(2,0)×(0,1)_4 sim=0.862; ARMA(0,0)×(0,1)_4 sim=0.790 — sobre residuos de `GDPDEC_m02_s0804x2.pre` |

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 5 | m00 | exploring | 328.7 | 2.725 | ✓ | 0.000 |  |
| 6 | m01_s0804 | dead-end | 307.5 | 2.255 | ✗ | 0.758 |  |
| 7 | m02_s0804x2 | exploring | 307.8 | 2.191 | ✗ | 0.588 |  |
| 10 | m03_x2_h2_ar2 | dead-end | 305.2 | 2.012 | ✓ | 0.986 |  |
| 11 | m04_x2_ar2 ◀ | adopted | 305.2 | 2.012 | ✓ | 0.986 | [2026-10-10] Revisión 10-oct: formales SF 3.97 (d basta) frente a DCD sobre-dif. θ̂ 0.852, LR 2.61 fuera de la banda; sub-dif LR 9.56. Se mantiene d=1 por SF (c |
| 12 | m05_x2_h2_ar2 | dead-end | 315.0 | 1.970 | ✗ | 0.742 |  |
| 13 | m06_x1_ar2 | dead-end | 308.5 | 2.129 | ✓ | 0.999 |  |
| 14 | m07_d2_ar2ma1 | dead-end | 302.1 | 2.017 | ✓ | 0.784 |  |
| 15 | m08_d2_ma1 | dead-end | 297.0 | 2.068 | ✗ | 0.869 |  |

**m04_x2_ar2** (adopted, 2026-10-09)
- ecuación: `∇[ln y_t] = μ + I_t(1 itvs) + [1-φ(B)]⁻¹·a_t`
- motivo: Referencia anidada para el LR de los armónicos: AR(2) completo + 2008Q4×2, sin armónicos.
- por qué se adopta: Guiado: AR(2) completo + escalón 2008Q4×2 (ω₀ −16.2 t −8.0, ω₁ +5.4 t 2.85; efecto permanente −21.7 %, Wald p 0.000; LR ×2 vs ×1 7.46, p 0.006). Treadway ✓ (z en fechas +0.48/+0.43; vecinos −1.36/+1.10). Diagnosis limpia (Q15 p 0.073, Q4 p 0.056 con barra en 4 en el borde; JB p 0.99). AR(2) = (1−0.685B)(1+0.584B): persistencia + alternancia de periodo 2 (estacional estocástica estacionaria; la serie va en bruto), sin ciclo. Armónicos rechazados (LR 2.84, 3 gl, p 0.42). Formales: SF 3.97 (d=1 basta al 1 %), DCD subdif LR 9.56 (∇ genuina), DCD sobredif θ̂ 0.852, LR 2.61 > 1.94 (crítico subestimado por el escalón). d=1 por coherencia con la brecha, el IPC y el marco I(1) del VECM. p del VECM = 3.
- problemas y salvedades: [2026-10-09] d=2 queda ABIERTO. Par en f=0 discrepa fuera de la banda (θ̂ 0.852, a 0.148 de la frontera): SF 3.97 frente a DCD LR 2.61 > 1.94 (ley desnuda; el escalón ×2 resuena en f=0). KPSS en d=1 p 0.033. Candidatos d=2 estimados: m07 ∇²+AR(2)+MA(1) adecuado, AIC/BIC 291.1/302.1 (−3.1 frente a B) pero φ₂ t 1.4 y θ 0.85 a 1.4 e.t. de 1; m08 ∇²+MA(1) AIC/BIC 290.4/297.0 pero Q(15) p 0.039 (inadecuado). Pendiente: bootstrap del DCD con intervenciones (piloto en el TODO de art); este caso es donde la decisión depende del crítico.

### `DEFL/GDPDUSA/GDPDUSA_m01_ar1.inp`

- **Tablas:** tab:uni «USA»
- **Ficheros:** especificación `DEFL/GDPDUSA/GDPDUSA_m01_ar1.inp` · óptimo adoptado `DEFL/GDPDUSA/GDPDUSA_m01_ar1.pre` · reestimado en `build/GDPDUSA_m01_ar1.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 4.8e-05); logL 8.1123

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| φ1 [AR regular 1] | 0.4897 | 0.1054 | 4.65 |
| μ | 0.4627 | 0.0505 | 9.16 |

- λ = 0, d = 1, D = 0; intervenciones: ninguna
- media de ∇ (o nivel si d = 0): 0.46 (0.05); σ = 0.214
- residuos: Q(15) = 10.02 (gl 14, p 0.761); JB = 0.28 (p 0.868)
- lado d+1: SF Φ = 8.65 (críticos 10 % 1.06, 5 % 1.75); DCD⁺ LR 1.76, θ̂ 0.799
- lado d−1: DCD⁻ LR 27.98, θ̂ 0.458
- identificación (ADF / KPSS, p): d=0: 0.104 / 0.010; d=1: 0.000 / 0.053

**Guion** `DEFL/GDPDUSA/GDPDUSA_guion.json` (serie GDPDUSA, creado 2026-10-09).

| nodo | decidido | evidencia |
|---|---|---|
| lambda | 0 |  |
| dominio | price_index |  |
| d | 1 | d=0: ADF p=0.104, KPSS p=0.010; d=1: ADF p=0.000, KPSS p=0.053 |
| estacionalidad | D=0 (sin estacionalidad) | F-HAC=0.61, p=0.6120 |

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 5 | m01_ar1 ◀ | adopted | -7.8 | 0.214 | ✓ | 0.868 | Autónomo: D=0 (HAC p 0.61); PACF corta en 1, ACF decae: AR(1) con μ; sin anómalos dominantes (2009 z≈−2.6) |

**m01_ar1** (adopted, 2026-10-09)
- ecuación: `∇[ln y_t] = μ + [1-φ(B)]⁻¹·a_t`
- por qué se adopta: Autónomo: AR(1) con μ (φ 0.49, μ 0.46 %), diagnosis limpia (Q p 0.76, JB p 0.87), sin anómalos ni estacionalidad. Componente de F2 (el sistema es bivariante con la razón).

### `DEFL/PCEEC/PCEEC_m01_ar1.inp`

- **Tablas:** tab:uni «Ecuador»
- **Ficheros:** especificación `DEFL/PCEEC/PCEEC_m01_ar1.inp` · óptimo adoptado `DEFL/PCEEC/PCEEC_m01_ar1.pre` · reestimado en `build/PCEEC_m01_ar1.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 1.2e-05); logL -104.6076

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| φ1 [AR regular 1] | 0.5250 | 0.1107 | 4.74 |
| μ | 1.0064 | 0.2916 | 3.45 |

- λ = 0, d = 1, D = 0; intervenciones: ninguna
- media de ∇ (o nivel si d = 0): 1.01 (0.29); σ = 1.150
- residuos: Q(15) = 18.95 (gl 14, p 0.167); JB = 2.82 (p 0.244)
- lado d+1: SF Φ = 6.91 (críticos 10 % 1.06, 5 % 1.75); DCD⁺ LR 3.63, θ̂ 0.902
- lado d−1: DCD⁻ LR 27.29, θ̂ 0.100
- identificación (ADF / KPSS, p): d=0: 0.028 / 0.010; d=1: 0.204 / 0.010

**Guion** `DEFL/PCEEC/PCEEC_guion.json` (serie PCEEC, creado 2026-10-09).

| nodo | decidido | evidencia |
|---|---|---|
| dominio | price_index |  |
| lambda | 0 | gap=-0.218; corr(nivel)=0.494; corr(log)=0.712; estadístico λ=1; regla de dominio `price_index` |
| d | 1 | d=0: ADF p=0.028, KPSS p=0.010; d=1: ADF p=0.204, KPSS p=0.010 |
| estacionalidad | D=0 (sin estacionalidad) | F-HAC=0.65, p=0.5881 |
| ordenes | ARMA(1,0) | ARMA(1,0) sim=0.902; ARMA(0,1) sim=0.871; ARMA(0,2) sim=0.889 — sobre ∇^1∇_s^0 y(λ=0.0) |

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 6 | m00 | exploring | 232.5 | 1.330 | ✗ | 0.154 | Modelo base ∇ln con μ, sin ARMA, para calibrar anómalos/cambios de nivel antes de fijar órdenes |
| 7 | m01_ar1 ◀ | adopted | 217.6 | 1.150 | ✓ | 0.244 | ARIMA(1,1,0) con μ: PACF corta en 1, ACF decae; gana por AICc; como PE [2026-10-09] Modelo final de PCEEC (cerrado por el analista 9-oct-2026). Contrastes forma |
| 8 | m02_ma1 | dead-end | 222.0 | 1.189 | ✓ | 0.135 | ARIMA(0,1,1) con μ: candidato empatado, para comparar con m01 |
| 9 | m03_ar2 | dead-end | 221.7 | 1.149 | ✓ | 0.222 | Sobreparametrización de m01: AR(2) |
| 10 | m04_arma11 | dead-end | 221.7 | 1.149 | ✓ | 0.217 | Sobreparametrización de m01: ARMA(1,1) |
| 11 | m05_ar1_arm | dead-end | 226.0 | 1.114 | ✓ | 0.793 | Comprobación pedida por el analista: m01 + armónicos (f=1, f=2) para pasar HSM/MEG; se espera que no sean significativos |

**m01_ar1** (adopted, 2026-10-09)
- ecuación: `∇[ln y_t] = μ + [1-φ(B)]⁻¹·a_t`
- por qué se adopta: AR(1) frente a MA(1): AIC/BIC 4.3 menores, σ 1.13 vs 1.18 %, diagnosis limpia; PACF corta en 1; como PE. Adoptado por el analista; quedan sobreparametrización y contrastes formales (d=2).

### `DEFL/PCEUSA/PCEUSA_m02_ar3.inp`

- **Tablas:** tab:uni «USA»
- **Ficheros:** especificación `DEFL/PCEUSA/PCEUSA_m02_ar3.inp` · óptimo adoptado `DEFL/PCEUSA/PCEUSA_m02_ar3.pre` · reestimado en `build/PCEUSA_m02_ar3.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 4.4e-05); logL -4.3083

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | 0.4362 | 0.2606 | 1.67 |
| ω1 [det. 1] | -0.4446 | 0.2617 | -1.70 |
| ω2 [det. 1] | 2.3150 | 0.2658 | 8.71 |
| ω3 [det. 1] | 1.2313 | 0.2553 | 4.82 |
| φ1 [AR regular 1] | 0.3390 | 0.1161 | 2.92 |
| φ2 [AR regular 1] | -0.1298 | 0.1278 | -1.02 |
| φ3 [AR regular 1] | 0.3431 | 0.1190 | 2.88 |
| μ | 0.4727 | 0.0683 | 6.92 |

- λ = 0, d = 1, D = 0; intervenciones: step 2008Q2 (×4)
- media de ∇ (o nivel si d = 0): 0.47 (0.07); σ = 0.257
- residuos: Q(15) = 9.24 (gl 12, p 0.682); JB = 1.96 (p 0.376)
- lado d+1: SF Φ = 2.48 (críticos 10 % 1.06, 5 % 1.75); DCD⁺ LR 0.88, θ̂ 0.894
- lado d−1: DCD⁻ LR 9.73, θ̂ -0.245
- identificación (ADF / KPSS, p): d=0: 0.213 / 0.010; d=1: 0.000 / 0.088

**Guion** `DEFL/PCEUSA/PCEUSA_guion.json` (serie PCEUSA, creado 2026-10-09).

| nodo | decidido | evidencia |
|---|---|---|
| dominio | price_index |  |
| lambda | 0 | gap=-0.158; corr(nivel)=0.467; corr(log)=0.625; estadístico λ=1; regla de dominio `price_index` |
| d | 1 | d=0: ADF p=0.213, KPSS p=0.010; d=1: ADF p=0.000, KPSS p=0.088 |
| estacionalidad | D=0 (sin estacionalidad) | F-HAC=0.48, p=0.6997 |
| estacionalidad | D=0 (B1, armónicos deterministas) |  |
| ordenes | ARMA(3,0) | ARMA(3,0) sim=0.904; ARMA(0,1) sim=0.820; ARMA(1,0) sim=0.831 — sobre residuos de `PCEUSA_m01_s0802x4.pre` |

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 5 | m00 | exploring | 77.9 | 0.419 | ✓ | 0.000 | Usuario confirma D=0 sin armónicos (HAC F=0.48 p=0.70). Modelo base ∇ln con μ para calibrar el episodio de 2008 |
| 6 | m01_s0802x4 | exploring | 44.7 | 0.289 | ✗ | 0.154 | Escalón Q2/2008×4 (episodio del petróleo 2008: subida Q2–Q3, desplome Q4, recuperación Q1/2009); mejor configuración del dato (empate con Q3/2008×3, ΔAIC 0.86), |
| 9 | m02_ar3 ◀ | adopted | 42.3 | 0.257 | ✓ | 0.376 | AR(3) completo sobre m01 (escalón Q2/2008×4), sin intervenir 2015Q1: la calibración muestra que no cambia ningún retardo [2026-10-09] Modelo final de PCEUSA (ce |
| 10 | m03_ar1 | dead-end | 41.4 | 0.273 | ✓ | 0.636 | Rival parsimonioso AR(1) sobre m01 (como el IPC de EE. UU.) |
| 11 | m04_ar4 | dead-end | 46.2 | 0.257 | ✓ | 0.463 | Sobreparametrización de m02: AR(4) |
| 12 | m05_arma31 | dead-end | 46.1 | 0.256 | ✓ | 0.452 | Sobreparametrización de m02: ARMA(3,1) |
| 13 | m06_ar3_s0804x2 | dead-end | 38.1 | 0.265 | ✓ | 0.532 | Pregunta del analista: ¿se sostienen los dos escalones iniciales (Q2–Q3/2008, t≈1.7)? Poda → escalón Q4/2008×2 con el AR(3) de m02 |

**m02_ar3** (adopted, 2026-10-09)
- ecuación: `∇[ln y_t] = μ + I_t(1 itvs) + [1-φ(B)]⁻¹·a_t`
- por qué se adopta: AR(3) completo (sin subconjuntos, criterio del analista) con escalón Q2/2008×4: diagnosis limpia; frente a AR(1) LR 7.5, 2 gl, p≈0.02 y el AR(1) deja barras en 3 y 6; AR(4) y ARMA(3,1) no significativos. Factores: real 0.76 (persistencia de la inflación) y complejo d=0.67, periodo 3.3.

### `EXT/BXE/BXE_m05_i0804x2.inp`

- **Tablas:** tab:uni2 «Balance»; tab:ur_app «$\ln BXE_t = x_t - i_t$»
- **Ficheros:** especificación `EXT/BXE/BXE_m05_i0804x2.inp` · óptimo adoptado `EXT/BXE/BXE_m05_i0804x2.pre` · reestimado en `build/BXE_m05_i0804x2.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 3.9e-05); logL -222.3159

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | -3.3046 | 0.9727 | -3.40 |
| ω0 [det. 2] | 1.8407 | 0.9725 | 1.89 |
| ω0 [det. 3] | -30.8845 | 6.2778 | -4.92 |
| ω1 [det. 3] | 25.0466 | 6.2799 | 3.99 |
| φ1 [AR regular 1] | 0.5556 | 0.1012 | 5.49 |
| μ | -3.3026 | 1.7073 | -1.93 |

- λ = 0, d = 0, D = 0; intervenciones: impulse 2008Q4 (×2)
- media de ∇ (o nivel si d = 0): -3.30 (1.71); σ = 6.345
- residuos: Q(15) = 9.70 (gl 14, p 0.784); JB = 0.31 (p 0.855)
- lado d+1: SF Φ = 7.06 (críticos 10 % 1.06, 5 % 1.75); DCD⁺ LR 0.00, θ̂ 1.000
- identificación (ADF / KPSS, p): d=0: 0.081 / 0.100; d=1: 0.000 / 0.100

**Guion** `EXT/BXE/BXE_guion.json` (serie BXE, creado 2026-10-07).

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 1 | PC1 | exploring | 508.3 | 8.977 | ✗ | 0.011 | BXE: lam=0, d=0 (ACF estacionaria, KPSS no rechaza; X y M I(1) con tendencia común), B1 (hereda estacionalidad de M; requisito multivariante); m00 con mu |
| 2 | PC2 | exploring | 494.5 | 7.390 | ✗ | 0.964 | Escalón Q4/2008×3 (identificado por el dato; ganancia esperada nula: shock común a X y M) |
| 3 | PC3 | exploring | 474.8 | 6.179 | ✓ | 0.850 | BXE m01 + AR(1) |
| 4 | PC4 | exploring | 477.0 | 6.084 | ✓ | 0.838 | Sobreajuste: BXE m01 + AR(2) |
| 5 | PC5 | exploring | 473.3 | 6.307 | ✓ | 0.819 | Poda de (-1)^t: MEG f=2 determinista, LR 2.75 p=0.097 |
| 6 | PC6 ◀ | adopted | 469.9 | 6.345 | ✓ | 0.855 |  |

**PC6** (adopted, 2026-10-10)
- ecuación: `ln y_t = μ + D_t(1 arm.) + I_t(1 itvs) + [1-φ(B)]⁻¹·a_t`
- por qué se adopta: Revisión A7 (10-oct-2026): el escalón Q4/2008 ×3 de m04 tenía ganancia −3.19 no distinta de cero (Wald p 0.34). Se impone la restricción: impulso ×2 en Q4/2008 (−30.9, −25.0; efecto transitorio). LR 0.86 (1 gl, p 0.35), BIC 473.3 → 470.0, diagnosis ✓, Treadway ✓. MEG f2 sobre la línea base con (−1)ᵗ: determinista; d=0 confirmado (SF 6.8, DCD θ̂=1). Pendiente: reestimar VECM_AUG con este .pre.

### `EXT/CAc/CAc_m03_ar1_noseas.inp`

- **Tablas:** tab:uni2 «Credit»; tab:ur_app «$cr_t$»
- **Ficheros:** especificación `EXT/CAc/CAc_m03_ar1_noseas.inp` · óptimo adoptado `EXT/CAc/CAc_m03_ar1_noseas.pre` · reestimado en `build/CAc_m03_ar1_noseas.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 1.8e-05); logL -217.5348

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | -38.9762 | 6.3500 | -6.14 |
| ω1 [det. 1] | 20.3254 | 6.3018 | 3.23 |
| ω2 [det. 1] | -12.5197 | 6.3781 | -1.96 |
| φ1 [AR regular 1] | 0.0911 | 0.1259 | 0.72 |
| μ | 2.4987 | 0.8530 | 2.93 |

- λ = 0, d = 1, D = 0; intervenciones: step 2008Q4 (×3)
- media de ∇ (o nivel si d = 0): 2.50 (0.85); σ = 6.220
- residuos: Q(15) = 8.42 (gl 14, p 0.866); JB = 0.89 (p 0.642)
- lado d+1: SF Φ = 18.67 (críticos 10 % 1.06, 5 % 1.75); DCD⁺ LR 3.53, θ̂ 0.886
- lado d−1: DCD⁻ LR 6.45, θ̂ 0.826
- identificación (ADF / KPSS, p): d=0: 0.122 / 0.010; d=1: 0.001 / 0.100

**Guion** `EXT/CAc/CAc_guion.json` (serie CAc, creado 2026-10-07).

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 1 | PC1 | exploring | 485.4 | 7.986 | ✓ | 0.000 | CAc: lam=0, d=1, B1 (coherencia con X y Rc); m00 con mu |
| 2 | PC2 | exploring | 459.3 | 5.984 | ✓ | 0.531 | Escalón Q4/2008x3, coherente con X |
| 3 | PC3 | exploring | 461.7 | 5.901 | ✓ | 0.451 | Sobreajuste AR(1) sobre m01 |
| 4 | PC4 ◀ | adopted | 456.1 | 6.220 | ✓ | 0.642 | Poda de armónicos (MEG det.; LR 5.7 chi2(3) p=0.13), AR(1) mantenido como en X |

**PC4** (adopted, 2026-10-07)
- ecuación: `∇[ln y_t] = μ + I_t(1 itvs) + [1-φ(B)]⁻¹·a_t`
- por qué se adopta: Adopción registrada en la revisión del 10-oct-2026 (decidida el 7-oct, §4.13): ln CAc d=1, escalón Q4/2008×3 (−47.8 permanente), AR(1) mantenido como en X, sin armónicos. Formales 10-oct: SF 18.7 (d basta) frente a DCD sobre-dif. θ̂ 0.886, LR 3.53 fuera de la banda; sub-dif LR 2.66 (sin potencia con AR libre, BUG-0224). d=1 por SF (criterio PE: cambio de deriva + escalón permanente que resuena en f=0).

### `EXT/CAd/CAd_m04_ar1x1.inp`

- **Tablas:** tab:uni2 «Debit»; tab:ur_app «$de_t$»
- **Ficheros:** especificación `EXT/CAd/CAd_m04_ar1x1.inp` · óptimo adoptado `EXT/CAd/CAd_m04_ar1x1.pre` · reestimado en `build/CAd_m04_ar1x1.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 2.9e-05); logL -202.5115

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | 2.0881 | 0.4748 | 4.40 |
| ω0 [det. 2] | -2.4548 | 0.4733 | -5.19 |
| ω0 [det. 3] | 1.7306 | 0.3757 | 4.61 |
| ω0 [det. 4] | 11.0002 | 5.1714 | 2.13 |
| ω1 [det. 4] | 17.4367 | 5.3060 | 3.29 |
| ω2 [det. 4] | 22.3694 | 5.1453 | 4.35 |
| ω3 [det. 4] | 12.9668 | 5.3147 | 2.44 |
| φ1 [AR regular 1] | 0.6554 | 0.1123 | 5.84 |
| φ1 [AR regular 2] | -0.5062 | 0.1309 | -3.87 |
| μ | 2.0621 | 1.1568 | 1.78 |

- λ = 0, d = 1, D = 0; intervenciones: step 2008Q3 (×4)
- media de ∇ (o nivel si d = 0): 2.06 (1.16); σ = 4.960
- residuos: Q(15) = 14.11 (gl 13, p 0.366); JB = 0.74 (p 0.691)
- lado d+1: SF Φ = 4.23 (críticos 10 % 1.06, 5 % 1.75); DCD⁺ LR 0.38, θ̂ 0.948
- lado d−1: DCD⁻ LR 8.52, θ̂ 0.234
- identificación (ADF / KPSS, p): d=0: 0.151 / 0.010; d=1: 0.002 / 0.100

**Guion** `EXT/CAd/CAd_guion.json` (serie CAd, creado 2026-10-07).

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 1 | PC1 | exploring | 455.7 | 6.402 | ✓ | 0.215 | CAd: lam=0, d=1, B1; camino de M (90% de los débitos) |
| 2 | PC2 | exploring | 448.5 | 5.349 | ✓ | 0.745 | Escalón Q3/2008x4 como en M |
| 3 | PC3 | exploring | 449.5 | 5.221 | ✓ | 0.815 | CAd m01 + AR(1) (como M) |
| 4 | PC4 | exploring | 447.1 | 4.960 | ✓ | 0.691 | Sobreajuste CAd: AR(2) (ACF(2)=0.31) |
| 5 | PC5 ◀ | adopted | 447.1 | 4.960 | ✓ | 0.691 | AR(2) de CAd factorizado: (1-0.655B)(1+0.506B), estimado en forma factorizada |

**PC5** (adopted, 2026-10-07)
- ecuación: `∇[ln y_t] = μ + (−1)ᵗ + D_t(1 arm.) + I_t(1 itvs) + [1-φ(B)]⁻¹·a_t`
- por qué se adopta: Adopción registrada en la revisión del 10-oct-2026 (decidida el 7-oct, §4.13/§4.19): ln CAd d=1, armónicos f1/f2, escalón Q3/2008×4 (como M), AR(2) factorizado (1−0.655B)(1+0.506B). Formales 10-oct limpios: SF 4.23 y DCD θ̂ 0.95 (LR 0.38) coinciden en d=1, sub-dif LR 6.87; MEG f1, f2 deterministas.

### `EXT/IT/IT_m00.inp`

- **Tablas:** tab:uni2 «Net»; tab:ur_app «$\ln IT_t = rc_t - rd_t$»
- **Ficheros:** especificación `EXT/IT/IT_m00.inp` · óptimo adoptado `EXT/IT/IT_m00.pre` · reestimado en `build/IT_m00.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 4.3e-05); logL -265.5223

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | -2.1383 | 1.2797 | -1.67 |
| ω0 [det. 2] | -1.8282 | 1.2796 | -1.43 |
| ω0 [det. 3] | -3.3523 | 2.4290 | -1.38 |
| φ1 [AR regular 1] | -0.6915 | 0.0862 | -8.02 |
| μ | -0.2540 | 0.9215 | -0.28 |

- λ = 0, d = 1, D = 0; intervenciones: ninguna
- media de ∇ (o nivel si d = 0): -0.25 (0.92); σ = 12.670
- residuos: Q(15) = 16.32 (gl 14, p 0.294); JB = 0.74 (p 0.692)
- lado d+1: SF no aplica (Shin-Fuller no aplica: el AR no tiene raíz real positiva; en f=0 decide el DCD. Sus raíces…); DCD⁺ LR 1.06, θ̂ 0.943
- lado d−1: DCD⁻ LR 39.01, θ̂ 0.184
- identificación (ADF / KPSS, p): d=0: 0.894 / 0.042; d=1: 0.001 / 0.100

**Guion** `EXT/IT/IT_guion.json` (serie IT, creado 2026-10-07).

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 1 | PC1 ◀ | adopted | 552.1 | 12.670 | ✓ | 0.692 | IT: lam=0, d=1 (ADF/KPSS), B1 (coherencia con Rc y Rd; f=2 significativa sola), AR(1) por la alternancia heredada de Rd (PACF(1)=-0.70) |
| 2 | PC2 | exploring | 564.3 | 12.532 | ✓ | 0.648 | Candidato d=0: ln IT en niveles con AR(2) (absorbe ∇ y el AR negativo) para contrastar I(0) |
| 3 | m02_meg1 | exploring | 537.0 | 12.891 | ✓ | 0.572 | Revisión A8: MEG sobre m00 da f=1 estocástica (coef −0.80, LR 4.62, fuera de banda). Modelo S: (1+B²) + testigo MA_f, sin cos/sin de f=1. [2026-10-10] ALTERNATI |
| 4 | m03_ar2 | dead-end | 556.0 | 12.644 | ✓ | 0.624 | Revisión A8: sobreajuste de m00 a AR(2) para obtener raíz real positiva y leer Shin-Fuller (AR(1) −0.69 no la tiene). |

**PC1** (adopted, 2026-10-07)
- ecuación: `∇[ln y_t] = μ + (−1)ᵗ + D_t(1 arm.) + [1-φ(B)]⁻¹·a_t`
- por qué se adopta: Revisión A8 (10-oct). Se mantiene D=0 (armónicos deterministas) porque IT entra en el análisis multivariante (VECM_XSYS) y éste es mejor con D=0 (decisión del analista). ln IT d=1, AR(1) −0.69, μ: diagnosis limpia; d=1 confirmado (DCD sobre-dif. θ̂ 0.94; sub-dif. LR 38.4; candidato d=0 v2 con raíz 0.961, SF no rechaza) → I(1), no raíz 0.96. HECHO DOCUMENTADO: el MEG da f=1 estocástica (coef −0.80, LR 4.62, fuera de banda); el modelo S (v3, m02_meg1) es adecuado, con testigo λ² 0.80 (LR 4.62, genuina), f=2 determinista y BIC 537.0 frente a 552.1. Rc y Rd tienen f=1 determinista (coef −0.90 / −0.85, poca potencia): la estocasticidad está en el desfase estacional entre remesas y renta pagada.

### `EXT/M/M_m03a_ar2.inp`

- **Tablas:** tab:uni2 «Imports»; tab:ur_app «$i_t$»
- **Ficheros:** especificación `EXT/M/M_m03a_ar2.inp` · óptimo adoptado `EXT/M/M_m03a_ar2.pre` · reestimado en `build/M_m03a_ar2.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 2.3e-05); logL -201.4993

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | 2.1706 | 0.4900 | 4.43 |
| ω0 [det. 2] | -2.7648 | 0.4865 | -5.68 |
| ω0 [det. 3] | 1.5061 | 0.2763 | 5.45 |
| ω0 [det. 4] | 8.1958 | 5.1031 | 1.61 |
| ω1 [det. 4] | 17.1664 | 5.3508 | 3.21 |
| ω2 [det. 4] | 26.0841 | 5.2583 | 4.96 |
| ω3 [det. 4] | 14.3213 | 5.1243 | 2.79 |
| φ1 [AR regular 1] | 0.3431 | 0.1226 | 2.80 |
| φ2 [AR regular 1] | 0.2319 | 0.1259 | 1.84 |
| μ | 2.0992 | 1.3832 | 1.52 |

- λ = 0, d = 1, D = 0; intervenciones: step 2008Q3 (×4)
- media de ∇ (o nivel si d = 0): 2.10 (1.38); σ = 4.884
- residuos: Q(15) = 21.75 (gl 13, p 0.059); JB = 1.43 (p 0.489)
- lado d+1: SF Φ = 3.58 (críticos 10 % 1.06, 5 % 1.75); DCD⁺ LR 0.41, θ̂ 0.943
- lado d−1: DCD⁻ LR 4.64, θ̂ 0.288
- identificación (ADF / KPSS, p): d=0: 0.118 / 0.010; d=1: 0.001 / 0.100

**Guion** `EXT/M/M_guion.json` (serie M, creado 2026-10-07).

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 1 | PC1 | exploring | 461.1 | 6.662 | ✗ | 0.067 | M: lam=0 (común), d=1 (ADF/KPSS), B1 (HAC F=13.6, f=1 y f=2); m00 con mu |
| 2 | PC2 | exploring | 452.8 | 5.525 | ✗ | 0.386 | Variante A: step Q3/2008x4 (permanente) |
| 3 | PC3 | exploring | 453.3 | 5.373 | ✗ | 0.322 | Variante B: step Q2/2008x5 (transitorio) |
| 4 | PC4 | exploring | 444.1 | 5.010 | ✓ | 0.516 | Variante A + AR(1) |
| 5 | PC5 | exploring | 444.4 | 4.866 | ✓ | 0.541 | Variante B + AR(1) |
| 6 | m03a_ar2 ◀ | adopted | 445.0 | 4.884 | ✓ | 0.489 | Sobreajuste AR(2) sobre m02a (F6): Q(8) límite y CAd sale AR(2) |

**m03a_ar2** (adopted, 2026-10-09)
- ecuación: `∇[ln y_t] = μ + (−1)ᵗ + D_t(1 arm.) + I_t(1 itvs) + [1-φ(B)]⁻¹·a_t`
- motivo: Coherencia por agregación con CAd = M + Rd: AR(2) (1−0.655B)(1+0.506B). ¿Necesita M un segundo retardo?
- por qué se adopta: Revisión F6 (9 oct. 2026), decisión del analista. AR(2) = (1−0.683B)(1+0.340B), raíces reales, coherente con CAd (1−0.655B)(1+0.506B). Mejora Q(8) (p 0.046 → 0.073) y despeja d = 1: DCD 2.11 → 0.41, par SF/DCD coincide (SF 3.58). MEG f=1, f=2 deterministas. Ganancia del escalón 2008T3×4: −49.4 (era −43.5).
- problemas y salvedades: [2026-10-09] φ₂ = 0.232 (EE 0.126, t 1.84) sólo significativo al 10 %: LR 3.27 frente a m02a (p 0.071). AIC prefiere AR(2) (423.00 vs 424.27); BIC prefiere AR(1) (444.11 vs 445.05). Adoptado por coherencia con CAd y por el orden de integración, no por la significación de φ₂. Quedan picos de ACF en los retardos 7 y 14 (0.30, 0.26) que el AR(2) no recoge (Q(15) p 0.059); parecen episodios (2013, 2015–16), no dinámica ARMA.

### `EXT/Rc/Rc_m00.inp`

- **Tablas:** tab:uni2 «Credit»; tab:ur_app «$rc_t$»
- **Ficheros:** especificación `EXT/Rc/Rc_m00.inp` · óptimo adoptado `EXT/Rc/Rc_m00.pre` · reestimado en `build/Rc_m00.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 4.1e-07); logL -211.6731

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | 0.8548 | 0.6965 | 1.23 |
| ω0 [det. 2] | -2.0841 | 0.6964 | -2.99 |
| ω0 [det. 3] | 1.2194 | 0.3483 | 3.50 |
| μ | 1.1690 | 0.6965 | 1.68 |

- λ = 0, d = 1, D = 0; intervenciones: ninguna
- media de ∇ (o nivel si d = 0): 1.17 (0.70); σ = 5.699
- residuos: Q(15) = 15.07 (gl 15, p 0.446); JB = 4.11 (p 0.128)
- lado d+1: SF Φ = 9.89 (críticos 10 % 1.06, 5 % 1.75), sobre AR sobreajustado; DCD⁺ LR 2.40, θ̂ 0.876
- lado d−1: DCD⁻ LR 157.70, θ̂ -0.163
- identificación (ADF / KPSS, p): d=0: 0.032 / 0.100; d=1: 0.046 / 0.100

**Guion** `EXT/Rc/Rc_guion.json` (serie Rc, creado 2026-10-07).

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 1 | PC1 ◀ | adopted | 440.2 | 5.699 | ✓ | 0.128 | Rc: lam=0 (común), d=1 provisional (par formal decide), B1 (HAC F=5.88, f=1 y f=2); m00 con mu |
| 2 | PC2 | exploring | 442.5 | 5.618 | ✓ | 0.515 | Sobreajuste de m00 con AR(1); 2005T1 no intervenido (no decide órdenes) |
| 3 | PC3 | exploring | 456.6 | 5.806 | ✓ | 0.111 | Candidato d=0: ln Rc en niveles con AR(1), armónicos y mu (para cerrar d sin el DCD sub-dif dudoso, BUG-0224) |

**PC1** (adopted, 2026-10-07)
- ecuación: `∇[ln y_t] = μ + (−1)ᵗ + D_t(1 arm.) + [1-φ(B)]⁻¹·a_t`
- por qué se adopta: Adopción registrada en la revisión del 10-oct-2026 (decidida el 7-oct, §4.13): ln Rc d=1, armónicos f1/f2, μ, sin ARMA (AR(1) de v2 sobra), 2005T1 (z 3.33) no intervenido. Por abajo: sub-dif LR 158 y candidato d=0 (v3) con raíz 0.982, SF no rechaza. Por arriba (10-oct): DCD sobre-dif. θ̂ 0.876, LR 2.40 (> 2.15 con armónicos), un solo lado (sin AR libre): cambio de deriva de las remesas; d=1 (criterio PE).

### `EXT/Rd/Rd_m01_ar1.inp`

- **Tablas:** tab:uni2 «Debit»; tab:ur_app «$rd_t$»
- **Ficheros:** especificación `EXT/Rd/Rd_m01_ar1.inp` · óptimo adoptado `EXT/Rd/Rd_m01_ar1.pre` · reestimado en `build/Rd_m01_ar1.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 9.8e-06); logL -258.7923

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | 2.9383 | 1.1535 | 2.55 |
| ω0 [det. 2] | -0.2225 | 1.1538 | -0.19 |
| ω0 [det. 3] | 4.4719 | 2.2440 | 1.99 |
| φ1 [AR regular 1] | -0.6983 | 0.0854 | -8.17 |
| μ | 1.4623 | 0.8298 | 1.76 |

- λ = 0, d = 1, D = 0; intervenciones: ninguna
- media de ∇ (o nivel si d = 0): 1.46 (0.83); σ = 11.457
- residuos: Q(15) = 17.40 (gl 14, p 0.235); JB = 0.28 (p 0.867)
- lado d+1: SF no aplica (Shin-Fuller no aplica: el AR no tiene raíz real positiva; en f=0 decide el DCD. Sus raíces…); DCD⁺ LR 0.76, θ̂ 0.922
- lado d−1: DCD⁻ LR 40.03, θ̂ 0.053
- identificación (ADF / KPSS, p): d=0: 0.930 / 0.015; d=1: 0.009 / 0.100

**Guion** `EXT/Rd/Rd_guion.json` (serie Rd, creado 2026-10-07).

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 1 | PC1 | exploring | 579.7 | 16.142 | ✗ | 0.546 | Rd: lam=0, d=1 (ADF/KPSS), B1 (HAC f=2; amplitud de la alternancia cambia hacia 2009); m00 con mu |
| 2 | PC2 ◀ | adopted | 538.6 | 11.457 | ✓ | 0.867 | Opción A: AR(1) (PACF(1)=-0.70) para la alternancia de amplitud variable |

**PC2** (adopted, 2026-10-07)
- ecuación: `∇[ln y_t] = μ + (−1)ᵗ + D_t(1 arm.) + [1-φ(B)]⁻¹·a_t`
- por qué se adopta: Adopción registrada en la revisión del 10-oct-2026 (decidida el 7-oct, §4.13): ln Rd d=1, armónicos f1/f2, AR(1) −0.70 (alternancia semestral de cupones de amplitud variable), μ. Formales 10-oct limpios: DCD θ̂ 0.92 (LR 0.76), sub-dif LR 40.0; MEG f1, f2 deterministas.

### `EXT/SE/SE_m03_i0804x2.inp`

- **Tablas:** tab:uni2 «Current-account ratio»; tab:ur_app «$\ln SE_t = cr_t - de_t$»
- **Ficheros:** especificación `EXT/SE/SE_m03_i0804x2.inp` · óptimo adoptado `EXT/SE/SE_m03_i0804x2.pre` · reestimado en `build/SE_m03_i0804x2.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 4.7e-05); logL -221.6902

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | -3.0474 | 0.9424 | -3.23 |
| ω0 [det. 2] | 1.5286 | 0.9427 | 1.62 |
| ω0 [det. 3] | -0.9558 | 0.4865 | -1.96 |
| ω0 [det. 4] | -23.9880 | 6.1790 | -3.88 |
| ω1 [det. 4] | 19.9074 | 6.1788 | 3.22 |
| φ1 [AR regular 1] | 0.6079 | 0.0951 | 6.39 |
| μ | 0.6527 | 1.9060 | 0.34 |

- λ = 0, d = 0, D = 0; intervenciones: impulse 2008Q4 (×2)
- media de ∇ (o nivel si d = 0): 0.65 (1.91); σ = 6.283
- residuos: Q(15) = 6.34 (gl 14, p 0.957); JB = 0.95 (p 0.621)
- lado d+1: SF Φ = 6.06 (críticos 10 % 1.06, 5 % 1.75); DCD⁺ LR 0.00, θ̂ 1.000
- identificación (ADF / KPSS, p): d=0: 0.000 / 0.100; d=1: 0.000 / 0.100

**Guion** `EXT/SE/SE_guion.json` (serie SE, creado 2026-10-07).

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 1 | PC1 | exploring | 503.0 | 8.632 | ✗ | 0.720 | SE: lam=0, d=0 (ADF p<0.0001, KPSS no rechaza; CAc, CAd I(1)), B1 en niveles como BXE |
| 2 | PC2 | exploring | 494.1 | 7.364 | ✗ | 0.928 | Escalón Q4/2008x3 como en BXE |
| 3 | PC3 | exploring | 474.9 | 6.186 | ✓ | 0.902 | SE m01 + AR(1) (ACF(1)=0.53) antes de juzgar Treadway |
| 4 | PC4 | exploring | 478.2 | 6.140 | ✓ | 0.806 | Reformular a Q4/2008x4 (Treadway: vecino 2009T3 +2.21) manteniendo AR(1) |
| 5 | PC5 | exploring | 474.0 | 6.338 | ✓ | 0.977 | Poda (-1)^t como en BXE (LR 3.27 p=0.07) |
| 6 | PC6 ◀ | adopted | 472.9 | 6.283 | ✓ | 0.621 |  |

**PC6** (adopted, 2026-10-10)
- ecuación: `ln y_t = μ + (−1)ᵗ + D_t(1 arm.) + I_t(1 itvs) + [1-φ(B)]⁻¹·a_t`
- por qué se adopta: Revisión A9 (10-oct-2026): el escalón Q4/2008 ×3 de m02 tenía ganancia −5.49 no distinta de cero (Wald p 0.10) y fallaba Treadway (vecino 2009T3 z=+2.21). Impulso ×2 en Q4/2008 (−24.0, −19.9): LR 2.22 (1 gl, p 0.14), BIC 474.9 → 472.9, diagnosis ✓, Treadway ✓ (vecino −0.03).

### `EXT/X/X_m03_ar1_noseas.inp`

- **Tablas:** tab:uni2 «Exports»; tab:ur_app «$x_t$»
- **Ficheros:** especificación `EXT/X/X_m03_ar1_noseas.inp` · óptimo adoptado `EXT/X/X_m03_ar1_noseas.pre` · reestimado en `build/X_m03_ar1_noseas.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 3.1e-05); logL -224.0883

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | -43.8656 | 6.9925 | -6.27 |
| ω1 [det. 1] | 22.5225 | 6.9970 | 3.22 |
| ω2 [det. 1] | -14.6043 | 7.0270 | -2.08 |
| φ1 [AR regular 1] | 0.1478 | 0.1250 | 1.18 |
| μ | 2.6674 | 1.0010 | 2.66 |

- λ = 0, d = 1, D = 0; intervenciones: step 2008Q4 (×3)
- media de ∇ (o nivel si d = 0): 2.67 (1.00); σ = 6.859
- residuos: Q(15) = 6.94 (gl 14, p 0.937); JB = 1.31 (p 0.521)
- lado d+1: SF Φ = 17.00 (críticos 10 % 1.06, 5 % 1.75); DCD⁺ LR 2.62, θ̂ 0.895
- lado d−1: DCD⁻ LR 6.78, θ̂ 0.795
- identificación (ADF / KPSS, p): d=0: 0.168 / 0.010; d=1: 0.000 / 0.100

**Guion** `EXT/X/X_guion.json` (serie X, creado 2026-10-07).

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 1 | PC1 | exploring | 501.4 | 9.003 | ✓ | 0.000 | X: lam=0 (común a todos los componentes), d=1 (ADF/KPSS), B1 (requisito multivariante; HAC p=0.078 con anómalo 2008T4); m00 con mu |
| 2 | PC2 | exploring | 474.2 | 6.688 | ✓ | 0.582 | Escalón Q4/2008x3 (coherencia con WTI); subir a x4 si Treadway falla |
| 3 | PC3 | exploring | 475.7 | 6.552 | ✓ | 0.467 | Sobreajuste de m01 con AR(1) (pedido por el analista) |
| 4 | PC4 ◀ | adopted | 469.2 | 6.859 | ✓ | 0.521 | Poda de armónicos f=1,f=2 tras MEG determinista: LR conjunto 6.11 chi2(3) p=0.107 |
| 5 | PC5 | exploring | 464.7 | 6.895 | ✓ | 0.755 | Candidato rival d=2: ∇² ln X con AR(1) y MA(1), sin mu (DCD sobrediferenciación LR 2.62) |

**PC4** (adopted, 2026-10-07)
- ecuación: `∇[ln y_t] = μ + I_t(1 itvs) + [1-φ(B)]⁻¹·a_t`
- por qué se adopta: Adopción registrada en la revisión del 10-oct-2026 (decidida el 7-oct, §4.12): ln X d=1, escalón Q4/2008×3 (−53 permanente), AR(1) mantenido, sin armónicos (MEG det.; poda LR 6.11 p 0.107), μ 2.67 %. Formales 10-oct: SF 17.0 (d basta) frente a DCD sobre-dif. θ̂ 0.895, LR 2.62 fuera de la banda; candidato d=2 (v5) lee un cambio de deriva (boom 2003–08), no I(2): d=1 por SF (criterio PE, el escalón permanente resuena en f=0).

### `GAP/GAP_m04_ar3_noalt.inp`

- **Tablas:** tab:uni «$PE/PU$»; tab:ur «$\ln(PE_t/PU_t)$»
- **Ficheros:** especificación `GAP/GAP_m04_ar3_noalt.inp` · óptimo adoptado `GAP/GAP_m04_ar3_noalt.pre` · reestimado en `build/GAP_m04_ar3_noalt.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 4.4e-05); logL -64.0264

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | 0.0452 | 0.0847 | 0.53 |
| ω0 [det. 2] | 0.3744 | 0.0852 | 4.40 |
| ω0 [det. 3] | 2.2824 | 0.5753 | 3.97 |
| φ1 [AR regular 1] | 0.3968 | 0.1199 | 3.31 |
| φ2 [AR regular 1] | -0.0946 | 0.1305 | -0.73 |
| φ3 [AR regular 1] | 0.3634 | 0.1210 | 3.00 |
| μ | 0.2115 | 0.2168 | 0.98 |

- λ = 0, d = 1, D = 0; intervenciones: step 2008Q4 (×1)
- media de ∇ (o nivel si d = 0): 0.21 (0.22); σ = 0.626
- residuos: Q(15) = 8.43 (gl 12, p 0.751); JB = 1.96 (p 0.375)
- lado d+1: SF Φ = 1.38 (críticos 10 % 1.06, 5 % 1.75); DCD⁺ LR 0.00, θ̂ 0.990
- lado d−1: DCD⁻ LR 8.20, θ̂ -0.213
- identificación (ADF / KPSS, p): d=0: 0.711 / 0.010; d=1: 0.076 / 0.099

**Guion** `GAP/GAP_guion.json` (serie GAP, creado 2026-10-07).

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 1 | PC1 | exploring | 178.6 | 0.810 | ✗ | 0.160 | GAP: lam=0 (dominio; ln GAP = ln PE - ln PU), d=1 provisional, B1 (requisito multivariante); m00 con mu |
| 2 | PC2 | exploring | 165.6 | 0.710 | ✓ | 0.217 | AR(1) sobre m00 sin intervenir 2008 (como FUE R.2) |
| 3 | PC3 | exploring | 161.7 | 0.669 | ✓ | 0.782 | Evaluar escalón simple 2008T4 sobre m01 (AR(1)+mu) |
| 4 | PC4 | exploring | 161.6 | 0.626 | ✓ | 0.344 | AR(3) completo sobre m02 (r(3)=0.33 tras escalón 2008T4); sin operadores restringidos |
| 5 | PC5 ◀ | adopted | 157.5 | 0.626 | ✓ | 0.375 | m03 sin (-1)^t: MEG f=2 determinista, LR simplificación 0.10 p=0.75. d=1 (SF rechaza al 10%, DCD confirma) |

**PC5** (adopted, 2026-10-07)
- ecuación: `∇[ln y_t] = μ + D_t(1 arm.) + I_t(1 itvs) + [1-φ(B)]⁻¹·a_t`
- por qué se adopta: GAP m04 (decisión del analista, 7-oct-2026; revisado 10-oct sin cambios, TODO A4; revision_empirica §4.11): ∇ ln(PE/PU) con armónicos f=1, escalón 2008T4 +2.28, AR(3) completo (0.40, −0.09, 0.36; raíces 0.82 y 0.66∠±108.6°), μ 0.21 %/trim. mantenido por su lectura económica. Sin (−1)ᵗ: MEG f=2 determinista sobre m03 (LR 1.20) → poda correcta. El analista no pide sobreajuste a AR(4): residuos limpios. d=1: SF rechaza al 10 % (Φ 1.37) y DCD⁺ θ̂ 0.99; DCD⁻ LR 8.1. Es la entrada GAP.pre de VECM_GAP_GY (modelo central) y la fila PE/PU de tab:uni.

### `GY_pasada2/GY_m03a_step0802.inp`

- **Tablas:** tab:uni2 «$\Delta\gamma_t$»; tab:ur «$\ln(G_t/Y_t)$»
- **Ficheros:** especificación `GY_pasada2/GY_m03a_step0802.inp` · óptimo adoptado `VECM_GAP_GY/GY_M1.pre` · reestimado en `build/GY_m03a_step0802.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 2.0e-05); logL -223.4188

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | 6.1927 | 0.7437 | 8.33 |
| ω0 [det. 2] | -2.7633 | 0.7436 | -3.72 |
| ω0 [det. 3] | 3.8544 | 0.8471 | 4.55 |
| ω0 [det. 4] | 25.7836 | 6.2510 | 4.12 |
| φ1 [AR regular 1] | -0.5184 | 0.1066 | -4.86 |

- λ = 0, d = 1, D = 0; intervenciones: step 2008Q2 (×1)
- media de ∇ (o nivel si d = 0): sin μ; σ = 6.776
- residuos: Q(15) = 11.70 (gl 14, p 0.630); JB = 0.19 (p 0.910)
- lado d+1: SF no aplica (Shin-Fuller no aplica: el AR no tiene raíz real positiva; en f=0 decide el DCD. Sus raíces…); DCD⁺ LR 0.11, θ̂ 0.968
- lado d−1: DCD⁻ LR 21.27, θ̂ 0.297
- identificación (ADF / KPSS, p): d=0: 0.483 / 0.010; d=1: 0.004 / 0.100

**Guion** `GY_pasada2/GY_guion.json` (serie GY, creado 2026-10-07).

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 1 | PC1 | exploring | 481.8 | 8.025 | ✓ | 0.768 | Revisión desde cero (pasada 2): lam=0, d=1, B1 armónicos; modelo base m00 |
| 2 | PC2 | exploring | 477.3 | 7.511 | ✓ | 0.609 | AR(1) sin mu (empate AR/MA ya resuelto en la pasada 1 a favor de AR(1); coincide con FUE G_Z.2 salvo mu) |
| 3 | PC3 | exploring | 465.1 | 6.040 | ✓ | 0.460 | Intervención 2008Q2x4 (step, 4 escalones): el dato y la escalera de Ockham coinciden; el analista asume retardo del efecto CFDD respecto a ene-2008 |
| 4 | PC4 ◀ | adopted | 467.9 | 6.776 | ✓ | 0.910 | Reformulación parsimoniosa: escalón permanente 2008Q2 (1 ω) — parte 1 de 2 |
| 5 | PC5 | exploring | 461.0 | 6.041 | ✓ | 0.443 | Reformulación parsimoniosa: + impulso en el nivel 2008Q3-Q4 (2 ω) — parte 2 de 2 (transitorio: inversión pública y precio del combustible 2008) |
| 6 | MEG_f1 | exploring | 449.6 | 6.181 | ✓ | 0.141 | M2: integrar f=1 (1+B^2) con testigo MA_f libre para verificar si la estocasticidad es real o casi-cancelación (pérdida de potencia por el impulso 2008) |
| 7 | PC7 | exploring | 484.2 | 6.730 | ✓ | 0.955 | Candidato d=0 + escalón 2008Q2 (M1) con AR(2)+mu: ¿G/Y estacionaria salvo ruptura (Perron)? |

**PC4** (adopted, 2026-10-07)
- ecuación: `∇[ln y_t] = (−1)ᵗ + D_t(1 arm.) + I_t(1 itvs) + [1-φ(B)]⁻¹·a_t`
- por qué se adopta: G/Y M1 (decisión del analista, 7-oct-2026; revisado 10-oct, TODO A1/A2; revision_empirica §4.8): ln G/Y, d=1, armónicos f=1 y f=2 deterministas (MEG; requisito B1 del sistema), AR(1) −0.52, escalón 2008T2 +25.8 sin μ. El escalón está justificado con información extramuestral: la CFDD (subsidio a combustibles) entra en el gasto del SPNF desde enero de 2008 (BCE), con efecto visible desde 2008T2; es un cambio de registro y debe controlarse. M2 (M1 + impulso 2008T3–T4) se mantiene sólo como robustez: lo justifica el dato, no información externa. Contrastes formales 10-oct: d=1 por abajo (sub-dif LR 18.8), DCD sobre-dif θ̂≈1; MEG f1, f2 deterministas. Es la entrada GY_M1.pre de VECM_GAP_GY (modelo central) y la fila Δγ de tab:uni2.

### `MACRO/G/G_m02_ar1.inp`

- **Tablas:** tab:uni2 «Expenditure»; tab:ur_app «$g_t$»
- **Ficheros:** especificación `MACRO/G/G_m02_ar1.inp` · óptimo adoptado `MACRO/G/G_m02_ar1.pre` · reestimado en `build/G_m02_ar1.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 4.7e-05); logL -235.8920

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | 11.4624 | 0.9410 | 12.18 |
| ω0 [det. 2] | -5.0300 | 0.9408 | -5.35 |
| ω0 [det. 3] | 6.5490 | 0.8115 | 8.07 |
| ω0 [det. 4] | 31.7491 | 8.2114 | 3.87 |
| φ1 [AR regular 1] | -0.3887 | 0.1171 | -3.32 |
| μ | 2.3637 | 0.7324 | 3.23 |

- λ = 0, d = 1, D = 0; intervenciones: step 2008Q2 (×1)
- media de ∇ (o nivel si d = 0): 2.36 (0.73); σ = 8.171
- residuos: Q(15) = 12.12 (gl 14, p 0.597); JB = 1.72 (p 0.423)
- lado d+1: SF Φ = 12.21 (críticos 10 % 1.06, 5 % 1.75), sobre AR sobreajustado; DCD⁺ LR 2.78, θ̂ 0.915
- lado d−1: DCD⁻ LR 10.62, θ̂ -0.347
- identificación (ADF / KPSS, p): d=0: 0.093 / 0.010; d=1: 0.323 / 0.100

**Guion** `MACRO/G/G_guion.json` (serie G, creado 2026-10-10).

| nodo | decidido | evidencia |
|---|---|---|
| dominio | multiplicative |  |
| lambda | 0 | gap=+0.893; corr(nivel)=0.902; corr(log)=0.009; estadístico λ=0 |
| d | 1 | d=0: ADF p=0.093, KPSS p=0.010; d=1: ADF p=0.323, KPSS p=0.100 |
| estacionalidad | D=0 (B1, armónicos deterministas) | F-HAC=52.17, p=0.0000 |
| ordenes | ARMA(1,0) | ARMA(0,2) sim=0.922; ARMA(1,1) sim=0.960; ARMA(1,0) sim=0.914 — sobre residuos de `G_m01_s0802.pre` |

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 5 | m00 | exploring | 503.4 | 9.135 | ✓ | 0.850 | B1: armónicos f1 (cos/sin) + (−1)ᵗ, μ, sin ARMA |
| 6 | m01_s0802 | exploring | 502.4 | 8.790 | ✗ | 0.969 |  |
| 8 | m02_ar1 ◀ | adopted | 497.0 | 8.171 | ✓ | 0.423 | Analista: AR(1) regular (el más simple; el del paper, φ −0.20). La alternancia la juzga el MEG. |

**m02_ar1** (adopted, 2026-10-10)
- ecuación: `∇[ln y_t] = μ + (−1)ᵗ + D_t(1 arm.) + I_t(1 itvs) + [1-φ(B)]⁻¹·a_t`
- por qué se adopta: Revisión 10-oct (guiado). ln G (gasto SPNF): d=1, D=0 con armónicos f1/f2, escalón CFDD 2008T2 (+31.7 %, t 3.9; sólo el cambio de registro: el episodio 2007T3–2008T3 que el dato ve es la expansión fiscal y no se interviene para no borrar la señal; vecino 2008T1 +1.95σ con el escalón solo), AR(1) −0.39, μ 2.36 %. Diagnosis limpia (2009T1 z −3.18 ≈ umbral 3.17, no intervenido). Formales: DCD sobre-dif. θ̂ 0.915 (banda; un solo lado, AR negativo) → d=1; sub-dif LR 10.3; MEG f1 det., f2 coef −0.9075 (banda) → armónicos deterministas. Es a la vez el modelo con D=0 (no hace falta alternativa).
- problemas y salvedades: [diagnosis] anómalos por encima del umbral calibrado (3.17): Q1/2009 (z=-3.18)

### `MACRO/REV_BCE/REVbce_g04_ar1.inp`

- **Tablas:** tab:uni2 «Revenue»; tab:ur_app «$re_t$»
- **Ficheros:** especificación `MACRO/REV_BCE/REVbce_g04_ar1.inp` · óptimo adoptado `MACRO/REV_BCE/REVbce_g04_ar1.pre` · reestimado en `build/REVbce_g04_ar1.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 4.6e-05); logL -228.5551

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | -3.1587 | 0.9045 | -3.49 |
| ω0 [det. 2] | -1.4870 | 0.9042 | -1.64 |
| ω0 [det. 3] | 1.9386 | 0.5939 | 3.26 |
| ω0 [det. 4] | 26.4836 | 7.4013 | 3.58 |
| ω0 [det. 5] | -21.3837 | 7.6541 | -2.79 |
| ω1 [det. 5] | 39.3862 | 7.8140 | 5.04 |
| ω2 [det. 5] | -22.3879 | 7.5840 | -2.95 |
| φ1 [AR regular 1] | -0.2292 | 0.1221 | -1.88 |
| μ | 2.7736 | 0.7605 | 3.65 |

- λ = 0, d = 1, D = 0; intervenciones: step 2008Q1 (×1); step 2008Q4 (×3)
- media de ∇ (o nivel si d = 0): 2.77 (0.76); σ = 7.330
- residuos: Q(15) = 16.51 (gl 14, p 0.283); JB = 1.72 (p 0.424)
- lado d+1: SF Φ = 3.38 (críticos 10 % 1.06, 5 % 1.75), sobre AR sobreajustado; DCD⁺ LR 5.93, θ̂ 0.861
- lado d−1: DCD⁻ LR 4.91, θ̂ -0.000
- identificación (ADF / KPSS, p): d=0: 0.299 / 0.010; d=1: 0.000 / 0.083

**Guion** `MACRO/REV_BCE/REVbce_guion.json` (serie REV, creado 2026-10-28).

| nodo | decidido | evidencia |
|---|---|---|
| dominio | multiplicative |  |
| lambda | 0 | gap=+0.106; corr(nivel)=0.475; corr(log)=0.369; estadístico λ=0 |
| d | 1 | d=0: ADF p=0.299, KPSS p=0.010; d=1: ADF p=0.000, KPSS p=0.083 |
| estacionalidad | D=0 (B1, armónicos deterministas) | F-HAC=14.46, p=0.0000 |
| ordenes | ARMA(1,0) | ARMA(0,0) sim=0.935; ARMA(1,0) sim=0.953; ARMA(0,1) sim=0.945 — sobre residuos de `REVbce_g02_s0804x3.pre` |

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 1 | m03_ar1 | dead-end | 495.0 | 7.330 | ✓ | 0.424 | Misma especificación que REV_m03_ar1 sobre datos verificables del BCE. |
| 2 | m05_nooil | dead-end | 516.7 | 9.471 | ✓ | 0.000 | Especificación de REV_m05_nooil sobre los datos del BCE; entrada REVno.pre de VECM_FISC. |
| 7 | g00 | exploring | 517.4 | 10.140 | ✓ | 0.000 | B1: ∇ln REV con armónicos f=1, f=2 y μ, sin ARMA ni intervenciones (recorrido guiado nuevo, datos BCE). |
| 8 | g01_s0801 | exploring | 513.8 | 9.566 | ✓ | 0.000 | Escalón 2008T1: cambio de registro de la CFDD (neto → bruto). |
| 9 | g02_s0804x3 | exploring | 494.2 | 7.523 | ✓ | 0.129 | Escalón 2008T4×3 (petróleo), forma propuesta por art y confirmada por el analista. |
| 11 | g03_ar0 | dead-end | 494.2 | 7.523 | ✓ | 0.129 | Candidato ARMA(0,0) sobre g02 (ruido blanco). |
| 12 | g04_ar1 ◀ | adopted | 495.0 | 7.330 | ✓ | 0.424 | Candidato AR(1) sobre g02. |
| 13 | g05_ar2 | dead-end | 499.1 | 7.329 | ✓ | 0.462 | Sobreajuste AR(2) de g04 para recuperar el lado AR (Shin-Fuller) del par en f=0. |
| 14 | g06_nooil_ar1 | adopted | 516.7 | 9.471 | ✓ | 0.000 | Variante para el VEC fiscal: especificación adoptada (g04) sin el escalón del petróleo (sólo CFDD 2008T1), AR(1), μ. |

**g04_ar1** (adopted, 2026-10-28)
- ecuación: `∇[ln y_t] = μ + (−1)ᵗ + D_t(1 arm.) + I_t(2 itvs) + [1-φ(B)]⁻¹·a_t`
- motivo: Empate en el nodo de órdenes; el analista pide estimar (0,0) y AR(1). AR(1) es la especificación del modelo anterior y la de G.
- por qué se adopta: Recorrido guiado con datos verificables del BCE (28-oct-2026). ln REV, d=1, armónicos f=1,2 (HSM: deterministas), escalón CFDD 2008T1 (+26.5; neto→bruto, información del analista), escalón petróleo 2008T4×3 (ganancia −40.8 permanente, forma identificada por el dato), AR(1) −0.23 (t −1.88; se mantiene: AIC, JB y residuos mejoran frente a (0,0), LR 3.4 p 0.06, coherente con G), μ 2.77 %/trim. Diagnosis limpia (Q15 p 0.28, JB p 0.42). d=1: el par en f=0 discrepa (DCD sobre-dif. θ̂ 0.86 LR 5.93, crítico subestimado por los escalones permanentes; Shin-Fuller por sobreajuste AR(3) Φ 3.38, p 0.009) → d=1 por el criterio PE, como en el análisis anterior.

**g06_nooil_ar1** (adopted, 2026-10-28)
- ecuación: `∇[ln y_t] = μ + (−1)ᵗ + D_t(1 arm.) + I_t(1 itvs) + [1-φ(B)]⁻¹·a_t`
- motivo: Criterio del analista (mantenido del 10-oct): la caída del petróleo de 2008T4 es una ruptura de la razón G/REV (escalón +16.9 en TAU), no de los ingresos dentro del sistema; se deja en la parte estocástica de REV para que el VEC la vea en la relación.
- por qué se adopta: Entrada REVno del VEC fiscal (criterio del analista, mantenido): la especificación adoptada (v12) sin el escalón del petróleo; la caída 2008T4–2009T1 queda en la parte estocástica porque es una ruptura de la razón G/REV (TAU, escalón +16.9), no de los ingresos dentro del sistema. Por diseño el JB falla (41.1; 2009T1 z −4.13); Q limpia (p 0.58). AR(1) −0.14 (t −1.15) se mantiene por coherencia con v12.
- problemas y salvedades: [diagnosis] el Jarque-Bera rechaza la normalidad (p=0.0000); anómalos por encima del umbral calibrado (3.17): Q1/2009 (z=-4.13)

### `MACRO/TAU_BCE/TAUbce_g02_ar2_s0804x3.inp`

- **Tablas:** tab:uni2 «Deficit»; tab:ur_app «$\tau_t = g_t - re_t$»
- **Ficheros:** especificación `MACRO/TAU_BCE/TAUbce_g02_ar2_s0804x3.inp` · óptimo adoptado `MACRO/TAU_BCE/TAUbce_g02_ar2_s0804x3.pre` · reestimado en `build/TAUbce_g02_ar2_s0804x3.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 2.1e-05); logL -225.8202

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | 14.1826 | 0.8095 | 17.52 |
| ω0 [det. 2] | -4.1362 | 0.8097 | -5.11 |
| ω0 [det. 3] | 4.9154 | 1.0069 | 4.88 |
| ω0 [det. 4] | 23.3453 | 6.5687 | 3.55 |
| ω1 [det. 4] | -16.8230 | 8.2482 | -2.04 |
| ω2 [det. 4] | 23.2542 | 6.5918 | 3.53 |
| φ1 [AR regular 1] | 0.2444 | 0.1071 | 2.28 |
| φ2 [AR regular 1] | 0.4439 | 0.1102 | 4.03 |
| μ | -6.7679 | 3.9644 | -1.71 |

- λ = 0, d = 0, D = 0; intervenciones: step 2008Q4 (×3)
- media de ∇ (o nivel si d = 0): -6.77 (3.96); σ = 6.667
- residuos: Q(15) = 11.16 (gl 13, p 0.597); JB = 1.79 (p 0.408)
- lado d+1: SF Φ = 1.78 (críticos 10 % 1.06, 5 % 1.75); DCD⁺ LR 0.18, θ̂ 0.455
- identificación (ADF / KPSS, p): d=0: 0.591 / 0.010; d=1: 0.011 / 0.100

**Guion** `MACRO/TAU_BCE/TAUbce_guion.json` (serie TAU, creado 2026-10-28).

| nodo | decidido | evidencia |
|---|---|---|
| dominio | ratio |  |
| lambda | 0 | gap=+0.330; corr(nivel)=0.584; corr(log)=0.254; estadístico λ=0 |
| d | 0 | d=0: ADF p=0.591, KPSS p=0.010; d=1: ADF p=0.011, KPSS p=0.100 |
| estacionalidad | D=0 (B1, armónicos deterministas) | F-HAC=69.03, p=0.0000 |
| ordenes | ARMA(2,0) | ARMA(2,0) sim=0.960; ARMA(1,1) sim=0.946; ARMA(2,0)×(0,1)_4 sim=0.965 — sobre residuos de `TAUbce_g00.pre` |

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 1 | m02_ar2 | adopted | 489.6 | 6.667 | ✓ | 0.408 | Misma especificación que TAU_m02_ar2 sobre datos verificables del BCE. |
| 6 | g00 | exploring | 558.1 | 12.942 | ✗ | 0.553 | B1: ln TAU, d=0, armónicos f=1,2 y media; sin ARMA ni intervenciones. |
| 8 | g01_ar2 | exploring | 505.9 | 8.226 | ✓ | 0.838 | AR(2) sobre g00 (propuesta del nodo de órdenes). |
| 9 | g02_ar2_s0804x3 ◀ | adopted | 489.6 | 6.667 | ✓ | 0.408 | Contraste del escalón del petróleo 2008T4×3 en TAU con información extramuestral. |
| 10 | g03_s0801x2 | dead-end | 491.9 | 6.367 | ✓ | 0.209 | Contraste del registro de la CFDD en TAU: escalón 2008T1×2 (ingresos en T1, gasto en T2). |
| 11 | g04_s0801 | dead-end | 493.8 | 6.667 | ✓ | 0.409 | Registro de la CFDD en TAU: un solo escalón 2008T1 (sobre g02). |

**m02_ar2** (adopted, 2026-10-28)
- ecuación: `ln y_t = μ + (−1)ᵗ + D_t(1 arm.) + I_t(1 itvs) + [1-φ(B)]⁻¹·a_t`
- motivo: Revisión de datos 28-oct-2026: TAU = G/REV con los ingresos reconstruidos desde los ficheros del BCE (ver REV_BCE). Se reestima la especificación adoptada en TAU/TAU_m02_ar2 (d=0, armónicos, escalón petróleo 2008Q4×3, AR(2), μ).
- por qué se adopta: Decisión del analista (28-oct-2026): con los ingresos verificables del BCE se mantiene la especificación de TAU_m02_ar2 (d=0, armónicos, escalón petróleo 2008Q4×3, AR(2), μ). Diagnosis limpia (Q15 p 0.60, JB p 0.41). La media se toma la de esta estimación: μ −6.77 (3.96), antes −8.0; σ 6.21 → 6.66. Efecto permanente del escalón +16.9.

**g02_ar2_s0804x3** (adopted, 2026-10-28)
- ecuación: `ln y_t = μ + (−1)ᵗ + D_t(1 arm.) + I_t(1 itvs) + [1-φ(B)]⁻¹·a_t`
- motivo: El dato no exige intervenir (sin \|z\|>3, la calibración no cambia órdenes) pero el suceso es conocido; el analista pide contrastarlo. La fecha declarada fija la configuración Q4/2008×3.
- por qué se adopta: Recorrido guiado con datos verificables del BCE (28-oct-2026). ln TAU, d=0 (contra ADF/KPSS sin tratar, sesgados por la estacionalidad y la ruptura de 2008; confirmado por el par en f=0: Shin-Fuller Φ 1.78 > 1.75 al 5 %, DCD sobre-dif. θ̂ 0.46 LR 0.18), armónicos f=1,2 (HSM: deterministas), AR(2) (raíces 0.80 y −0.56), escalón petróleo 2008T4×3 contrastado con información extramuestral (ganancia +16.9 [7.3, 26.5], Wald p 0.0005; LR 28.9, 3 gl; AIC 492.6 → 469.6). Registro de la CFDD en 2008T1 no intervenido: se cancela en el cociente (g03, g04 abandonadas). Media de esta estimación −6.77 (3.96): superávit ≈ 7 % de los ingresos antes de 2008T4, déficit ≈ 10 % después. Diagnosis limpia (Q15 p 0.60, JB p 0.41).

### `MACRO/YN/YN_m04_ar1_sar1.inp`

- **Tablas:** tab:uni2 «Nominal»
- **Ficheros:** especificación `MACRO/YN/YN_m04_ar1_sar1.inp` · óptimo adoptado `MACRO/YN/YN_m04_ar1_sar1.pre` · reestimado en `build/YN_m04_ar1_sar1.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 4.9e-05); logL -152.1799

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | 5.3761 | 0.4587 | 11.72 |
| ω0 [det. 2] | -2.0249 | 0.4612 | -4.39 |
| ω0 [det. 3] | 2.8117 | 0.1818 | 15.47 |
| ω0 [det. 4] | -13.1853 | 2.1476 | -6.14 |
| ω1 [det. 4] | 8.2229 | 2.1698 | 3.79 |
| φ1 [AR regular 1] | 0.3376 | 0.1164 | 2.90 |
| Φ1 [AR anual 1] | 0.4349 | 0.1151 | 3.78 |
| μ | 2.0826 | 0.7250 | 2.87 |

- λ = 0, d = 1, D = 0; intervenciones: step 2008Q4 (×2)
- media de ∇ (o nivel si d = 0): 2.08 (0.72); σ = 2.328
- residuos: Q(15) = 12.84 (gl 13, p 0.460); JB = 1.36 (p 0.507)
- lado d+1: SF Φ = 12.34 (críticos 10 % 1.06, 5 % 1.75); DCD⁺ LR 0.43, θ̂ 0.949
- lado d−1: DCD⁻ LR 11.84, θ̂ 0.203
- identificación (ADF / KPSS, p): d=0: 0.041 / 0.010; d=1: 0.001 / 0.068

**Guion** `MACRO/YN/YN_guion.json` (serie YN, creado 2026-10-10).

| nodo | decidido | evidencia |
|---|---|---|
| dominio | multiplicative |  |
| lambda | 0 | gap=+0.184; corr(nivel)=0.715; corr(log)=0.531; estadístico λ=0 |
| d | 1 | d=0: ADF p=0.041, KPSS p=0.010; d=1: ADF p=0.001, KPSS p=0.068 |
| estacionalidad | D=0 (B1, armónicos deterministas) | F-HAC=163.81, p=0.0000 |
| ordenes | ARMA(1,1)×(1,0)_4 | ARMA(0,2)×(1,0)_4 sim=0.965; ARMA(0,2)×(0,1)_4 sim=0.963; ARMA(2,0)×(1,0)_4 sim=0.943 — sobre residuos de `YN_m01_s0804x2.pre` |

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 5 | m00 | exploring | 358.5 | 3.099 | ✓ | 0.005 | B1: armónicos f1 (cos/sin) + (−1)ᵗ, μ, sin ARMA |
| 6 | m01_s0804x2 | exploring | 347.7 | 2.685 | ✗ | 0.602 |  |
| 8 | m02_ar2 | exploring | 344.0 | 2.447 | ✗ | 0.373 | Analista: AR(2) regular completo como baseline B1 (como YR y el paper); el retardo 4 lo decide el MEG. |
| 9 | m03_ar2_sar1 | exploring | 340.6 | 2.303 | ✓ | 0.465 | Analista: la barra en el retardo 4 de m02 podría ser un pequeño AR(1)_4 estacionario (en vez de f=2 estocástica). m02 + AR_4(1), armónicos intactos. |
| 10 | m04_ar1_sar1 ◀ | adopted | 338.0 | 2.328 | ✓ | 0.507 | [2026-10-10] ALTERNATIVA DOCUMENTADA con D=0 (armónicos f1 y (−1)ᵗ deterministas): ln YN d=1, escalón 2008T4×2, AR(1) 0.34 × AR(1)_4 0.43, μ 2.08 %; diagnosis l |
| 11 | m05_meg2 | adopted | 334.1 | 2.320 | ✓ | 0.536 | MEG sobre m04 (alternativa D=0): f=2 estocástica (coef −0.85, LR 3.93). Raíz (1+B) + testigo, sin (−1)ᵗ; f=1 determinista se mantiene. |

**m04_ar1_sar1** (adopted, 2026-10-10)
- ecuación: `∇[ln y_t] = μ + (−1)ᵗ + D_t(1 arm.) + I_t(1 itvs) + [1-Φ(B^4)·φ(B)]⁻¹·a_t`
- motivo: Analista: podar φ₂ (t 1.26) de m03 → AR(1)×AR(1)_4.
- por qué se adopta: Modelo de las TABLAS DEL PAPER (decisión del analista, 10-oct-2026): las tablas usan estacionalidad determinista en todas las frecuencias y el análisis de estacionalidad estocástica (HSM) va al addon. YN m04: ∇ ln PIB nominal con armónicos, escalón 2008T4×2 (petróleo), AR(1) 0.34 × AR(1)₄ 0.43, μ 2.08 %/trim.; SF 12.3, DCD⁺ 0.4. m05_meg2 ((1+B) en f=2 con testigo) sigue adoptado como modelo del addon.

**m05_meg2** (adopted, 2026-10-10)
- ecuación: `(1+B)∇[ln y_t] = μ + D_t(1 arm.) + I_t(1 itvs) + [1-Φ(B^4)·φ(B)]⁻¹·[1-θ(B)]·a_t`
- por qué se adopta: Revisión 10-oct (guiado). ln YN: d=1; escalón 2008T4×2 (−13.0, −7.8; permanente ≈ −20.8 %, el suceso del deflactor/petróleo, coherente con GDPDEC_G ×2); armónicos f=1 deterministas (MEG LR 0); f=2 estocástica (MEG sobre m04: coef −0.85, LR 3.93) → (1+B) con testigo θ 0.85; AR(1) φ 0.44 × AR(1)_4 Φ 0.31 (t 2.2); μ 2.08 %/trim. Diagnosis limpia; SF/DCD coinciden en d=1. BIC 334.1, el mejor entre los adecuados.

### `MACRO/YN/YN_m05_meg2.inp`

- **Tablas:** tab:uni2 «Nominal» (addon)
- **Ficheros:** especificación `MACRO/YN/YN_m05_meg2.inp` · óptimo adoptado `MACRO/YN/YN_m05_meg2.pre` · reestimado en `build/YN_m05_meg2.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 3.7e-05); logL -150.2906

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | 5.3494 | 0.3443 | 15.53 |
| ω0 [det. 2] | -2.0746 | 0.3480 | -5.96 |
| ω0 [det. 3] | -12.9684 | 2.1214 | -6.11 |
| ω1 [det. 3] | 7.8240 | 2.1650 | 3.61 |
| φ1 [AR regular 1] | 0.4378 | 0.1395 | 3.14 |
| Φ1 [AR anual 1] | 0.3131 | 0.1398 | 2.24 |
| θ1 [MA regular 1] | -0.8481 | 0.1424 | -5.96 |
| μ | 4.1658 | 1.3128 | 3.17 |

- λ = 0, d = 1, D = 0; intervenciones: step 2008Q4 (×2)
- media de ∇ (o nivel si d = 0): 2.08 (0.66); σ = 2.320
- residuos: Q(15) = 14.24 (gl 12, p 0.286); JB = 1.25 (p 0.536)
- lado d+1: SF Φ = 8.20 (críticos 10 % 1.06, 5 % 1.75); DCD⁺ LR 1.04, θ̂ 0.930
- lado d−1: DCD⁻ LR 78.08, θ̂ -0.848
- identificación (ADF / KPSS, p): d=0: 0.041 / 0.010; d=1: 0.001 / 0.068

**Guion** `MACRO/YN/YN_guion.json` (serie YN, creado 2026-10-10).

| nodo | decidido | evidencia |
|---|---|---|
| dominio | multiplicative |  |
| lambda | 0 | gap=+0.184; corr(nivel)=0.715; corr(log)=0.531; estadístico λ=0 |
| d | 1 | d=0: ADF p=0.041, KPSS p=0.010; d=1: ADF p=0.001, KPSS p=0.068 |
| estacionalidad | D=0 (B1, armónicos deterministas) | F-HAC=163.81, p=0.0000 |
| ordenes | ARMA(1,1)×(1,0)_4 | ARMA(0,2)×(1,0)_4 sim=0.965; ARMA(0,2)×(0,1)_4 sim=0.963; ARMA(2,0)×(1,0)_4 sim=0.943 — sobre residuos de `YN_m01_s0804x2.pre` |

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 5 | m00 | exploring | 358.5 | 3.099 | ✓ | 0.005 | B1: armónicos f1 (cos/sin) + (−1)ᵗ, μ, sin ARMA |
| 6 | m01_s0804x2 | exploring | 347.7 | 2.685 | ✗ | 0.602 |  |
| 8 | m02_ar2 | exploring | 344.0 | 2.447 | ✗ | 0.373 | Analista: AR(2) regular completo como baseline B1 (como YR y el paper); el retardo 4 lo decide el MEG. |
| 9 | m03_ar2_sar1 | exploring | 340.6 | 2.303 | ✓ | 0.465 | Analista: la barra en el retardo 4 de m02 podría ser un pequeño AR(1)_4 estacionario (en vez de f=2 estocástica). m02 + AR_4(1), armónicos intactos. |
| 10 | m04_ar1_sar1 | adopted | 338.0 | 2.328 | ✓ | 0.507 | [2026-10-10] ALTERNATIVA DOCUMENTADA con D=0 (armónicos f1 y (−1)ᵗ deterministas): ln YN d=1, escalón 2008T4×2, AR(1) 0.34 × AR(1)_4 0.43, μ 2.08 %; diagnosis l |
| 11 | m05_meg2 ◀ | adopted | 334.1 | 2.320 | ✓ | 0.536 | MEG sobre m04 (alternativa D=0): f=2 estocástica (coef −0.85, LR 3.93). Raíz (1+B) + testigo, sin (−1)ᵗ; f=1 determinista se mantiene. |

**m04_ar1_sar1** (adopted, 2026-10-10)
- ecuación: `∇[ln y_t] = μ + (−1)ᵗ + D_t(1 arm.) + I_t(1 itvs) + [1-Φ(B^4)·φ(B)]⁻¹·a_t`
- motivo: Analista: podar φ₂ (t 1.26) de m03 → AR(1)×AR(1)_4.
- por qué se adopta: Modelo de las TABLAS DEL PAPER (decisión del analista, 10-oct-2026): las tablas usan estacionalidad determinista en todas las frecuencias y el análisis de estacionalidad estocástica (HSM) va al addon. YN m04: ∇ ln PIB nominal con armónicos, escalón 2008T4×2 (petróleo), AR(1) 0.34 × AR(1)₄ 0.43, μ 2.08 %/trim.; SF 12.3, DCD⁺ 0.4. m05_meg2 ((1+B) en f=2 con testigo) sigue adoptado como modelo del addon.

**m05_meg2** (adopted, 2026-10-10)
- ecuación: `(1+B)∇[ln y_t] = μ + D_t(1 arm.) + I_t(1 itvs) + [1-Φ(B^4)·φ(B)]⁻¹·[1-θ(B)]·a_t`
- por qué se adopta: Revisión 10-oct (guiado). ln YN: d=1; escalón 2008T4×2 (−13.0, −7.8; permanente ≈ −20.8 %, el suceso del deflactor/petróleo, coherente con GDPDEC_G ×2); armónicos f=1 deterministas (MEG LR 0); f=2 estocástica (MEG sobre m04: coef −0.85, LR 3.93) → (1+B) con testigo θ 0.85; AR(1) φ 0.44 × AR(1)_4 Φ 0.31 (t 2.2); μ 2.08 %/trim. Diagnosis limpia; SF/DCD coinciden en d=1. BIC 334.1, el mejor entre los adecuados.

### `MACRO/YR/YR_m01_ar2.inp`

- **Tablas:** tab:uni2 «Real»
- **Ficheros:** especificación `MACRO/YR/YR_m01_ar2.inp` · óptimo adoptado `MACRO/YR/YR_m01_ar2.pre` · reestimado en `build/YR_m01_ar2.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 2.7e-05); logL -116.0442

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | 5.6527 | 0.1313 | 43.06 |
| ω0 [det. 2] | -2.1021 | 0.1312 | -16.02 |
| ω0 [det. 3] | 2.9777 | 0.1117 | 26.66 |
| φ1 [AR regular 1] | 0.0219 | 0.1205 | 0.18 |
| φ2 [AR regular 1] | 0.2809 | 0.1219 | 2.30 |
| μ | 0.8704 | 0.2378 | 3.66 |

- λ = 0, d = 1, D = 0; intervenciones: ninguna
- media de ∇ (o nivel si d = 0): 0.87 (0.24); σ = 1.366
- residuos: Q(15) = 15.68 (gl 13, p 0.267); JB = 1.93 (p 0.380)
- lado d+1: SF Φ = 6.21 (críticos 10 % 1.06, 5 % 1.75); DCD⁺ LR 0.01, θ̂ 0.983
- lado d−1: DCD⁻ LR 8.72, θ̂ -0.647
- identificación (ADF / KPSS, p): d=0: 0.600 / 0.010; d=1: 0.267 / 0.078

**Guion** `MACRO/YR/YR_guion.json` (serie YR, creado 2026-10-10).

| nodo | decidido | evidencia |
|---|---|---|
| dominio | multiplicative |  |
| lambda | 0 | gap=+0.482; corr(nivel)=0.732; corr(log)=0.250; estadístico λ=0 |
| d | 1 | d=0: ADF p=0.600, KPSS p=0.010; d=1: ADF p=0.267, KPSS p=0.078 |
| estacionalidad | D=0 (B1, armónicos deterministas) | F-HAC=1010.14, p=0.0000 |
| ordenes | ARMA(1,1) | ARMA(2,0) sim=0.925; ARMA(2,1) sim=0.941; ARMA(0,2) sim=0.897 — sobre residuos de `YR_m00.pre` |

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 5 | m00 | exploring | 254.0 | 1.421 | ✓ | 0.231 | B1: armónicos f1 (cos/sin) + (−1)ᵗ, μ, sin ARMA |
| 7 | m01_ar2 ◀ | adopted | 257.3 | 1.366 | ✓ | 0.380 | Analista: AR(2) completo (PACF corta en 2; coincide con el paper) [2026-10-10] ALTERNATIVA DOCUMENTADA con D=0 (estacionalidad determinista, armónicos): baselin |
| 8 | m02_meg2 | exploring | 253.3 | 1.346 | ✓ | 0.451 | MEG sobre m01 (baseline): f=2 estocástica (LR 5.06, coef −0.81). Raíz (1+B) + testigo MA_f, sin (−1)ᵗ. |
| 9 | m03_meg12 | exploring | 247.9 | 1.386 | ✓ | 0.312 | MEG sobre m02: f=1 estocástica (LR 2.38, coef −0.86). Raíz (1+B²) + testigo MA_f, sin cos/sin de f=1. |
| 10 | m04_noar | exploring | 244.7 | 1.442 | ✓ | 0.307 |  |
| 11 | m05_ar1 | adopted | 244.0 | 1.389 | ✓ | 0.418 |  |

**m01_ar2** (adopted, 2026-10-10)
- ecuación: `∇[ln y_t] = μ + (−1)ᵗ + D_t(1 arm.) + [1-φ(B)]⁻¹·a_t`
- por qué se adopta: Modelo de las TABLAS DEL PAPER (decisión del analista, 10-oct-2026): las tablas usan estacionalidad determinista en todas las frecuencias y el análisis de estacionalidad estocástica (HSM) va al addon. YR m01: ∇ ln PIB real con armónicos, AR(2) 0.02 / 0.28, μ 0.87 %/trim. (= la fila del paper); SF 6.2, DCD⁺ 0.0. m05_ar1 (∇₄ con testigos MA_f) sigue adoptado como modelo del addon.

**m05_ar1** (adopted, 2026-10-10)
- ecuación: `(1+B²)(1+B)∇[ln y_t] = μ + [1-φ(B)]⁻¹·[1-θ(B)]·a_t`
- motivo: Analista: podar sólo el segundo orden del AR de m03 (φ₂ t 0.5) → AR(1); m04 sin AR fallaba Q(4).
- por qué se adopta: Revisión 10-oct (guiado). ln YR: d=1; MEG sobre el baseline B1 (m01, AR(2)+armónicos) da f=1 y f=2 estocásticas → ∇₄ con testigos MA_f (m03); poda del 2.º orden del AR (LR 0.26, p 0.61) → AR(1) φ 0.34 (t 2.2). Diagnosis limpia; SF/DCD coinciden en d=1; testigo f=2 θ 0.77 (genuina), f=1 λ² 0.87, LR 2.12 vs 2.06 (estocástica por margen mínimo). AIC/BIC 235.4/244.0, los mejores entre los adecuados. ∇₄ ln YR I(0), media 3.54 (0.88 %/trim.). El AR(2) φ₂ 0.28 del paper era la f=2 estocástica tratada como determinista.

### `MACRO/YR/YR_m05_ar1.inp`

- **Tablas:** tab:uni2 «Real» (addon)
- **Ficheros:** especificación `MACRO/YR/YR_m05_ar1.inp` · óptimo adoptado `MACRO/YR/YR_m05_ar1.pre` · reestimado en `build/YR_m05_ar1.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 2.9e-05); logL -113.6757

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| φ1 [AR regular 1] | 0.3376 | 0.1506 | 2.24 |
| θ1 [MA regular 1] | -0.7684 | 0.1263 | -6.08 |
| θ2 [MA f-fijo 1] | -0.8735 | 0.0784 | -11.14 |
| μ | 3.5388 | 0.8471 | 4.18 |

- λ = 0, d = 1, D = 0; intervenciones: ninguna
- media de ∇ (o nivel si d = 0): 0.88 (0.21); σ = 1.389
- residuos: Q(15) = 9.59 (gl 12, p 0.652); JB = 1.75 (p 0.418)
- lado d+1: SF Φ = 8.64 (críticos 10 % 1.06, 5 % 1.75); DCD⁺ LR 0.20, θ̂ 0.958
- lado d−1: DCD⁻ LR 55.22, θ̂ -0.768
- identificación (ADF / KPSS, p): d=0: 0.600 / 0.010; d=1: 0.267 / 0.078

**Guion** `MACRO/YR/YR_guion.json` (serie YR, creado 2026-10-10).

| nodo | decidido | evidencia |
|---|---|---|
| dominio | multiplicative |  |
| lambda | 0 | gap=+0.482; corr(nivel)=0.732; corr(log)=0.250; estadístico λ=0 |
| d | 1 | d=0: ADF p=0.600, KPSS p=0.010; d=1: ADF p=0.267, KPSS p=0.078 |
| estacionalidad | D=0 (B1, armónicos deterministas) | F-HAC=1010.14, p=0.0000 |
| ordenes | ARMA(1,1) | ARMA(2,0) sim=0.925; ARMA(2,1) sim=0.941; ARMA(0,2) sim=0.897 — sobre residuos de `YR_m00.pre` |

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 5 | m00 | exploring | 254.0 | 1.421 | ✓ | 0.231 | B1: armónicos f1 (cos/sin) + (−1)ᵗ, μ, sin ARMA |
| 7 | m01_ar2 | adopted | 257.3 | 1.366 | ✓ | 0.380 | Analista: AR(2) completo (PACF corta en 2; coincide con el paper) [2026-10-10] ALTERNATIVA DOCUMENTADA con D=0 (estacionalidad determinista, armónicos): baselin |
| 8 | m02_meg2 | exploring | 253.3 | 1.346 | ✓ | 0.451 | MEG sobre m01 (baseline): f=2 estocástica (LR 5.06, coef −0.81). Raíz (1+B) + testigo MA_f, sin (−1)ᵗ. |
| 9 | m03_meg12 | exploring | 247.9 | 1.386 | ✓ | 0.312 | MEG sobre m02: f=1 estocástica (LR 2.38, coef −0.86). Raíz (1+B²) + testigo MA_f, sin cos/sin de f=1. |
| 10 | m04_noar | exploring | 244.7 | 1.442 | ✓ | 0.307 |  |
| 11 | m05_ar1 ◀ | adopted | 244.0 | 1.389 | ✓ | 0.418 |  |

**m01_ar2** (adopted, 2026-10-10)
- ecuación: `∇[ln y_t] = μ + (−1)ᵗ + D_t(1 arm.) + [1-φ(B)]⁻¹·a_t`
- por qué se adopta: Modelo de las TABLAS DEL PAPER (decisión del analista, 10-oct-2026): las tablas usan estacionalidad determinista en todas las frecuencias y el análisis de estacionalidad estocástica (HSM) va al addon. YR m01: ∇ ln PIB real con armónicos, AR(2) 0.02 / 0.28, μ 0.87 %/trim. (= la fila del paper); SF 6.2, DCD⁺ 0.0. m05_ar1 (∇₄ con testigos MA_f) sigue adoptado como modelo del addon.

**m05_ar1** (adopted, 2026-10-10)
- ecuación: `(1+B²)(1+B)∇[ln y_t] = μ + [1-φ(B)]⁻¹·[1-θ(B)]·a_t`
- motivo: Analista: podar sólo el segundo orden del AR de m03 (φ₂ t 0.5) → AR(1); m04 sin AR fallaba Q(4).
- por qué se adopta: Revisión 10-oct (guiado). ln YR: d=1; MEG sobre el baseline B1 (m01, AR(2)+armónicos) da f=1 y f=2 estocásticas → ∇₄ con testigos MA_f (m03); poda del 2.º orden del AR (LR 0.26, p 0.61) → AR(1) φ 0.34 (t 2.2). Diagnosis limpia; SF/DCD coinciden en d=1; testigo f=2 θ 0.77 (genuina), f=1 λ² 0.87, LR 2.12 vs 2.06 (estocástica por margen mínimo). AIC/BIC 235.4/244.0, los mejores entre los adecuados. ∇₄ ln YR I(0), media 3.54 (0.88 %/trim.). El AR(2) φ₂ 0.28 del paper era la f=2 estocástica tratada como determinista.

### `PE/PE_m03_ar1.inp`

- **Tablas:** tab:uni «Ecuador»; tab:ur «$\ln PE_t$»
- **Ficheros:** especificación `PE/PE_m03_ar1.inp` · óptimo adoptado `PE/PE_m03_ar1.pre` · reestimado en `build/PE_m03_ar1.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 2.1e-05); logL -40.1910

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | -0.2319 | 0.0494 | -4.69 |
| ω0 [det. 2] | 0.1683 | 0.0495 | 3.40 |
| ω0 [det. 3] | 0.0295 | 0.0185 | 1.60 |
| ω0 [det. 4] | 1.5616 | 0.4531 | 3.45 |
| ω1 [det. 4] | -2.8694 | 0.4927 | -5.82 |
| ω2 [det. 4] | -1.6036 | 0.4502 | -3.56 |
| φ1 [AR regular 1] | 0.5057 | 0.1091 | 4.64 |
| μ | 0.6658 | 0.1082 | 6.15 |

- λ = 0, d = 1, D = 0; intervenciones: step 2008Q1 (×3)
- media de ∇ (o nivel si d = 0): 0.67 (0.11); σ = 0.440
- residuos: Q(15) = 20.96 (gl 14, p 0.103); JB = 0.70 (p 0.705)
- lado d+1: SF Φ = 7.71 (críticos 10 % 1.06, 5 % 1.75); DCD⁺ LR 7.38, θ̂ 0.777
- lado d−1: DCD⁻ LR 32.13, θ̂ 0.609
- identificación (ADF / KPSS, p): d=0: 0.516 / 0.010; d=1: 0.258 / 0.025

**Guion** `PE/PE_guion.json` (serie PE, creado 2026-10-07).

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 1 | PC1 | exploring | 154.9 | 0.678 | ✗ | 0.000 | IPC Ecuador: lam=0 (dominio), d=1 provisional, B1 armónicos; m00 con mu (la media de la inflación es la tasa de inflación) |
| 2 | PC2 | exploring | 132.6 | 0.539 | ✗ | 0.843 | Analista: dos escalones a partir de 2008Q1 (Q1/2008x2) en lugar del x3 que propone el mecanismo |
| 3 | PC3 | exploring | 128.2 | 0.506 | ✗ | 0.307 | Q1/2008x2 falla Treadway (vecino 2008Q3 z=+2.77); se construye Q1/2008x3 (forma identificada por el dato) |
| 4 | PC4 ◀ | adopted | 114.0 | 0.440 | ✓ | 0.705 | Analista: empezar por AR(1), lo que muestran ACF/PACF (pico dominante en lag 1) |
| 5 | PC5 | exploring | 114.2 | 0.426 | ✓ | 0.617 | Analista: estudiar AR(1)x AR(1)_4 (señal residual en lag 4: PACF +0.27, ACF +0.22) |
| 6 | m05_d2 | exploring | 109.1 | 0.427 | ✓ | 0.855 |  |
| 7 | m06_d2ma1 | exploring | 105.5 | 0.429 | ✓ | 0.802 | [2026-10-10] No se adopta: queda como salvedad de robustez de A5. ARIMA(0,2,1) θ=0.707 (sub-dif. LR 26.2), MEG f1,f2 deterministas, BIC 105.5 vs 114.0 de m03. E |

**PC4** (adopted, 2026-10-07)
- ecuación: `∇[ln y_t] = μ + (−1)ᵗ + D_t(1 arm.) + I_t(1 itvs) + [1-φ(B)]⁻¹·a_t`
- por qué se adopta: Revisión A5 (10-oct-2026): se mantiene d=1 (PE_m03_ar1). Shin-Fuller confirma d=1 (Φ=7.71); el DCD de sobrediferenciación pide d+1 (θ̂=0.78, LR 7.38) y el candidato ARIMA(0,2,1) (m06) tiene subdiferenciación LR 26.2 y BIC 105.5 frente a 114.0: el par en f=0 discrepa y la evidencia es ambigua entre d=1 y d=2. Decisión del analista: d=1, coherente con GAP I(1) y con la convergencia como fenómeno transitorio de la muestra.

### `PU/PU_m08_ar1_noalt.inp`

- **Tablas:** tab:uni «USA»; tab:ur «$\ln PU_t$»
- **Ficheros:** especificación `PU/PU_m08_ar1_noalt.inp` · óptimo adoptado `PU/PU_m08_ar1_noalt.pre` · reestimado en `build/PU_m08_ar1_noalt.out`
- **Reproduce el `.pre` adoptado:** sí (máx |Δ| 4.3e-05); logL -29.8547

| parámetro | estimación | e.t. | t |
|---|---|---|---|
| ω0 [det. 1] | -0.3263 | 0.0459 | -7.12 |
| ω0 [det. 2] | -0.2121 | 0.0463 | -4.58 |
| ω0 [det. 3] | 0.9635 | 0.3931 | 2.45 |
| ω1 [det. 3] | -0.6945 | 0.4047 | -1.72 |
| ω2 [det. 3] | 2.8804 | 0.4012 | 7.18 |
| ω3 [det. 3] | 1.1506 | 0.3861 | 2.98 |
| φ1 [AR regular 1] | 0.2692 | 0.1217 | 2.21 |
| μ | 0.5422 | 0.0644 | 8.42 |

- λ = 0, d = 1, D = 0; intervenciones: step 2008Q2 (×4)
- media de ∇ (o nivel si d = 0): 0.54 (0.06); σ = 0.378
- residuos: Q(15) = 17.28 (gl 14, p 0.242); JB = 0.66 (p 0.719)
- lado d+1: SF Φ = 13.35 (críticos 10 % 1.06, 5 % 1.75); DCD⁺ LR 1.12, θ̂ 0.923
- lado d−1: DCD⁻ LR 11.72, θ̂ -0.766
- identificación (ADF / KPSS, p): d=0: 0.222 / 0.010; d=1: 0.000 / 0.100

**Guion** `PU/PU_guion.json` (serie PU, creado 2026-10-07).

| v | nombre | estado | BIC | σ | Q ok | JB p | decisión |
|---|---|---|---|---|---|---|---|
| 1 | PC1 | exploring | 129.2 | 0.560 | ✓ | 0.000 | CPI USA: lam=0 (dominio), d=1 (ADF/KPSS coinciden), B1 armónicos; m00 con mu |
| 2 | PC2 | exploring | 97.8 | 0.391 | ✓ | 0.198 | Intervención step Q2/2008×4 (arranque fijado por el analista en T2) |
| 3 | PC3 | exploring | 101.1 | 0.413 | ✓ | 0.205 | Variante step Q2/2008×3 (s=2) frente a m01 (s=3) |
| 4 | PC4 | exploring | 96.9 | 0.376 | ✓ | 0.584 | B: AR(1) sobre m01 sin intervenir 2014T4–2015T1 (como FUE PU.x) |
| 5 | PC5 | exploring | 100.4 | 0.374 | ✓ | 0.771 | Sobreajuste de m03: AR(2) |
| 6 | PC6 | exploring | 94.4 | 0.350 | ✓ | 0.645 | Sobreajuste de m03: ARMA(1,1) |
| 7 | PC7 | exploring | 101.1 | 0.376 | ✓ | 0.584 | Sobreajuste de m03: AR(1)xAR(1)_4 (coherencia con PE-B) |
| 8 | PC8 | exploring | 101.7 | 0.364 | ✓ | 0.977 | Sobreajuste de m03: AR(1) x AR(2)_4 (pedido por el analista) |
| 9 | PC9 ◀ | adopted | 93.3 | 0.378 | ✓ | 0.719 | m03 sin (-1)^t: MEG f=2 determinista y LR simplificación 0.63 p=0.43 |

**PC9** (adopted, 2026-10-07)
- ecuación: `∇[ln y_t] = μ + D_t(1 arm.) + I_t(1 itvs) + [1-φ(B)]⁻¹·a_t`
- por qué se adopta: PU m08 (decisión del analista, 7-oct-2026; revisado 10-oct, TODO A6; revision_empirica §4.10): ∇ ln IPC_USA con armónicos f=1, escalón 2008T2×4 (ganancia −2.37) y AR(1); sin (−1)ᵗ (MEG f=2 determinista sobre m03 → poda correcta). No se interviene 2014–15 (decisión del analista: sin suceso único). d=1 por las dos vías y por abajo (SF 13.4, DCD⁺ θ̂ 0.92 en banda; DCD⁻ LR 7.8). Es la entrada PU.pre de VECM_TRI y la fila USA de tab:uni.
