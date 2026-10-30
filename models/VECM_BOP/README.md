# Balance-of-payments VECs: credits and debits (drvec, 2026-10-10)

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
