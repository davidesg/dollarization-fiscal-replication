# VECM_AUG re-estimated with the adopted BXE (m05, 2026-10-10)

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
