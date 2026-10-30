# Registry of the drvec / drtran runs: verification report

Generated 2026-10-28. Sources read: the `run*.sh` scripts in each `VECM_*` directory, `art_drvec/replicate.sh` and `replicate_boot.sh` (exact commands for VECM_GAP_GY, VECM_AUG, VECM_XSYS and VECM_TRI), the READMEs (VECM_AUG/m05, VECM_FISC, VECM_BOP), `VECM_REC/*.py`, `tables/vecm_registry.py`, `borrador/analisis/{mapa_paper,multivariantes}.md`, `TODO_REVISION.md` and `revision_empirica_2026-10.md` (`RESULTADOS_REVISION.md` does not exist under `revision-suite/Python/`; its sections are quoted inside `multivariantes.md`, which is what the `paper` field cites as RES). Where no script exists the command was inferred from the `.out` header and body (model, case, series order, sample, `-fdhess`, `alpha = A*psi`, `-fixb2row` rows, `-xlink`/`-xsys` blocks, bootstrap size) and then confirmed by rerunning.

All runs were redone with `drvec-py 0.1.0` / `drtran-py 0.2.4` on copies of the inputs. Every original `.out` is `DRVEC 0.10` (header), the transfer functions `DRTRAN 1.0`.

## Summary

- Runs in `analyses.py` (excluding `tables/vecm_registry.py`): 262 single drvec/drtran runs + 5 VECM_REC entries (3 python drivers covering 220 drvec calls, all reproduced exactly; 1 `-writeinp` fit; 1 numpy bootstrap).
- Verified, exact or within tolerance: **247** (all of them with logL difference 0 to 10 printed digits, except the drtran runs, which match to the 6 printed decimals; estimates max |d| <= 3e-5).
- Arguments confirmed but the optimum differs: **14** (all r = 2 trivariate deflator runs, VECM_GDPD / VECM_GDPD_G: the port reaches a HIGHER likelihood; r = 0 and r = 1 rows and LR(r = 0) match exactly).
- Not verifiable with the port: **1** (`wti:chain_fx`, `-xsys` + `-fixb2row` refused by drvec-py).
- Mismatches (wrong arguments): **0**. Unreconstructed: `-writeinp` of `rec:hjfull_free` (option not ported; fit itself verified).
- Registry runs (`tables/vecm_registry.py`, 30): all match their original `.out` (table below).

## Problems found

1. **drvec-py refuses `-xsys` with `-fixb2row`** (`wti:chain_fx`, the WTI -> G/Y -> GAP IRF/FEVD of RES 5.4 and TD C11). C drvec 0.10 accepted the combination. The error message does not even list `-fixb2row` among the incompatible options, so it looks like a port gap/bug rather than a design decision. Until fixed, the published IRF bands of the WTI chain cannot be regenerated with the Python port. `wti:chain` (same system without the restriction) matches exactly.
2. **r = 2 in the trivariate GDP-deflator systems is multimodal.** In 14 runs (VECM_GDPD all trivariate rank tests except cpre_p2; VECM_GDPD_G cpre_p2 and the r = 2 `-multistart` fits) the C 0.10 optimizer stopped at a worse local optimum for r = 2 (it printed negative LR(r <= 1) such as -38, -66). The port finds higher logL. Nothing quoted in the paper depends on it (all quoted statistics are LR(r = 0), which matches, and r = 0 is not rejected), but two statements in RES 6.3/6.4 rest on the r = 2 values: (a) 'r = 2 (case pre) with multistart 10 gives the same logL (-347.02 < -342.30 of r = 1)': the port gives -346.80 (VECM_GDPD) and -353.68 vs r = 1 -353.10 (VECM_GDPD_G); the conclusion (r = 2 worse than r = 1 under -case pre) still holds. (b) The `r <= 1` bootstrap p-values of `tri_boot499_*` in those directories were computed from a broken r = 2 fit; they are not quoted.
3. `VECM_PCE/tri_r2_pre_ms` matches exactly (-319.4645), so the PCE statement in RES 6.3 is reproduced.
4. Registry runs `fisc_b1`, `tb_b1`, `ca_b1` add `-fdhess`, and `tri3_A/B/C` omit it, relative to the original `.out` they correspond to (`fitA_p2_pre_r1_b1`, `TB_fitb1_p2`, `CA_fitb1_p2` were run without `-fdhess`; `weakex2_orig`, `testB_orig`, `testC_orig` with it). Same logL and estimates; only the standard errors differ (BFGS factor vs finite-difference Hessian). Not an error, but the old `.out` are not the files the tables regenerate.
5. `VECM_REC`: the drivers default to the C binary (`DRVEC=drvec for the replication repository set `DRVEC=drvec-py`. `hj_boot.py` reads `runs/hjfull_inp.{1,2}.inp`, written by C drvec `-writeinp`, which drvec-py does not implement: ship those two files as data or port `-writeinp`. The prefix `hjfull_inp` is inferred from the file names (no script records that call). `multivariantes.md` says '148 ajustes' for the recursive theta; the script and the CSV have 146 (37 forward + 36 backward, each weakly exogenous and free).
6. `VECM_WTI/tf_WTIraw_*_d` read `tf_WTI_*_d.cns` (stated in their `.out`), not the identically named-for-raw `.cns` that sits next to them; the contents are identical, so either works. The registry keeps what was actually run.
7. The FISC/BOP `.out` headers say 'case 3' although the README and the registry say `-case pre`; with both drifts free in the `.pre` files the two are the same model (verified: `-case pre` reproduces the logL exactly). Same for VECM_TRI `cp_*` (scripted with `-case pre`).

## Runs (`analyses.py` RUNS)

Command: `cd art_drvec/<dir> && drvec-py <args> -name <name>` (drtran: `drtran-py <args> -m <name>`). Bootstrap and `-irfboot` runs were verified without that option.

| key | dir | args | kind | status | verification |
|---|---|---|---|---|---|
| `biv:boot_p4_c2` | VECM_GAP_GY | `GY_M1.pre GAP.pre 4 0 0 -case 2 -lrtest -bootstrap 499` | boot | superseded | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |
| `biv:boot_p2_c2` | VECM_GAP_GY | `GY_M1.pre GAP.pre 2 0 0 -case 2 -lrtest -bootstrap 499` | boot | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |
| `biv:fit_p2_c2_r1` | VECM_GAP_GY | `GY_M1.pre GAP.pre 2 0 1 -case 2 -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (10/10 params) |
| `biv:rank_M1_c2_p1` | VECM_GAP_GY | `GY_M1.pre GAP.pre 1 0 0 -case 2 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `biv:rank_M1_c2_p2` | VECM_GAP_GY | `GY_M1.pre GAP.pre 2 0 0 -case 2 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `biv:rank_M1_c2_p3` | VECM_GAP_GY | `GY_M1.pre GAP.pre 3 0 0 -case 2 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `biv:rank_M1_c2_p4` | VECM_GAP_GY | `GY_M1.pre GAP.pre 4 0 0 -case 2 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `biv:rank_M1_c3_p1` | VECM_GAP_GY | `GY_M1.pre GAP.pre 1 0 0 -case 3 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `biv:rank_M1_c3_p2` | VECM_GAP_GY | `GY_M1.pre GAP.pre 2 0 0 -case 3 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `biv:rank_M1_c3_p3` | VECM_GAP_GY | `GY_M1.pre GAP.pre 3 0 0 -case 3 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `biv:rank_M1_c3_p4` | VECM_GAP_GY | `GY_M1.pre GAP.pre 4 0 0 -case 3 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `biv:gate_p4_c2` | VECM_GAP_GY | `GY_M1.pre GAP.pre 4 0 0 -case 2 -diagar -diagma -diagcov` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (7/7 params) |
| `biv:gate_p4_c3` | VECM_GAP_GY | `GY_M1.pre GAP.pre 4 0 0 -case 3 -diagar -diagma -diagcov` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (9/9 params) |
| `biv:rank_noint_p2` | VECM_GAP_GY | `GY_noint.pre GAP_noint.pre 2 0 0 -case 2 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `biv:fit_noint_p2` | VECM_GAP_GY | `GY_noint.pre GAP_noint.pre 2 0 1 -case 2 -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (10/10 params) |
| `biv:rank_noint_p4` | VECM_GAP_GY | `GY_noint.pre GAP_noint.pre 4 0 0 -case 2 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `biv:fit_noint_p4` | VECM_GAP_GY | `GY_noint.pre GAP_noint.pre 4 0 1 -case 2 -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (18/18 params) |
| `biv:rank_gynoint_p4` | VECM_GAP_GY | `GY_noint.pre GAP.pre 4 0 0 -case 2 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `biv:fit_gynoint_p4` | VECM_GAP_GY | `GY_noint.pre GAP.pre 4 0 1 -case 2 -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (18/18 params) |
| `biv:rank_gapnoint_p4` | VECM_GAP_GY | `GY_M1.pre GAP_noint.pre 4 0 0 -case 2 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `biv:fit_gapnoint_p4` | VECM_GAP_GY | `GY_M1.pre GAP_noint.pre 4 0 1 -case 2 -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (18/18 params) |
| `biv:rank_M2_p4` | VECM_GAP_GY | `GY_M2.pre GAP.pre 4 0 0 -case 2 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `biv:fit_M2_p4` | VECM_GAP_GY | `GY_M2.pre GAP.pre 4 0 1 -case 2 -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (18/18 params) |
| `biv:rank_M1_p4_c3` | VECM_GAP_GY | `GY_M1.pre GAP.pre 4 0 0 -case 3 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `biv:fit_M1_p4_c3` | VECM_GAP_GY | `GY_M1.pre GAP.pre 4 0 1 -case 3 -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (19/19 params) |
| `biv:c4b_pre` | VECM_GAP_GY | `GY_M1.pre GAP.pre 4 0 1 -case pre` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (18/18 params) |
| `biv:c4b_tr` | VECM_GAP_GY | `GY_M1.pre GAP.pre 4 0 1 -case pre -trend -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (19/19 params) |
| `biv:chk_fixb2` | VECM_GAP_GY | `GY_M1.pre GAP.pre 4 0 1 -case 2 -fixb2 -0.37` | restriction | exploratory | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (17/17 params) |
| `biv:chk_fixb2row` | VECM_GAP_GY | `GY_M1.pre GAP.pre 4 0 1 -case 2 -fixb2row 1 -0.37` | restriction | exploratory | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (17/17 params) |
| `biv:irfboot_wx` | VECM_GAP_GY | `GY_M1.pre GAP.pre 4 0 1 -case 2 -weakex 1 -irfboot 999` | irfboot | adopted | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (17/17 params); point fit only, -irfboot not rerun |
| `biv:irfboot_free` | VECM_GAP_GY | `GY_M1.pre GAP.pre 4 0 1 -case 2 -irfboot 999` | irfboot | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (18/18 params); point fit only, -irfboot not rerun |
| `aug:rank_p4_c2` | VECM_AUG/m05 | `GY.pre BXE.pre GAP.pre 4 0 0 -case 2 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 2 LR rows) |
| `aug:fit_p4_c2_r1` | VECM_AUG/m05 | `GY.pre BXE.pre GAP.pre 4 0 1 -case 2 -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (38/38 params) |
| `aug:fit_p2_c2_r2` | VECM_AUG/m05 | `GY.pre BXE.pre GAP.pre 2 0 2 -case 2 -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (24/24 params) |
| `aug:xl_bxe_fd` | VECM_AUG/m05 | `GY.pre GAP.pre 4 0 1 -case 2 -fdhess -xpre BXE.pre -xlink net_gap_bxe.txt` | exog | adopted | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (19/19 params) |
| `aug:xl_b1` | VECM_AUG/m05 | `GY.pre GAP.pre 4 0 1 -case 2 -fdhess -xpre BXE.pre -xlink net_b1.txt` | exog | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (19/19 params) |
| `aug:xl_s1` | VECM_AUG/m05 | `GY.pre GAP.pre 4 0 1 -case 2 -fdhess -xpre BXE.pre -xlink net_s1.txt` | exog | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (20/20 params) |
| `aug:xl_r1` | VECM_AUG/m05 | `GY.pre GAP.pre 4 0 1 -case 2 -fdhess -xpre BXE.pre -xlink net_r1.txt` | exog | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (20/20 params) |
| `aug_m04:rank_p4_c2` | VECM_AUG | `GY.pre BXE.pre GAP.pre 4 0 0 -case 2 -lrtest` | rank | superseded | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 2 LR rows) |
| `aug_m04:fit_p4_c2_r2` | VECM_AUG | `GY.pre BXE.pre GAP.pre 4 0 2 -case 2 -fdhess` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (42/42 params) |
| `aug_m04:fit_p4_c2_r1` | VECM_AUG | `GY.pre BXE.pre GAP.pre 4 0 1 -case 2 -fdhess` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (38/38 params) |
| `aug_m04:fit_p2_c2_r2` | VECM_AUG | `GY.pre BXE.pre GAP.pre 2 0 2 -case 2 -fdhess` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (24/24 params) |
| `aug_m04:boot_p4_c2` | VECM_AUG | `GY.pre BXE.pre GAP.pre 4 0 0 -case 2 -lrtest -bootstrap 499` | boot | superseded | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 2 LR rows); bootstrap not rerun |
| `aug_m04:xl_gap_bxe` | VECM_AUG | `GY.pre GAP.pre 4 0 1 -case 2 -xpre BXE.pre -xlink net_gap_bxe.txt` | exog | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (19/19 params) |
| `aug_m04:xl_b1` | VECM_AUG | `GY.pre GAP.pre 4 0 1 -case 2 -xpre BXE.pre -xlink net_b1.txt` | exog | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (19/19 params) |
| `aug_m04:xl_s1` | VECM_AUG | `GY.pre GAP.pre 4 0 1 -case 2 -xpre BXE.pre -xlink net_s1.txt` | exog | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (20/20 params) |
| `aug_m04:xl_r1` | VECM_AUG | `GY.pre GAP.pre 4 0 1 -case 2 -xpre BXE.pre -xlink net_r1.txt` | exog | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (20/20 params) |
| `aug_m04:xl_bxe_fd` | VECM_AUG | `GY.pre GAP.pre 4 0 1 -case 2 -xpre BXE.pre -xlink net_gap_bxe.txt -fdhess` | exog | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (19/19 params) |
| `xsys:xs_it` | VECM_XSYS | `IT.pre GY.pre GAP.pre 4 0 1 -case 2 -xsys 1` | exog | adopted | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (31/31 params) |
| `xsys:xs_it_fd` | VECM_XSYS | `IT.pre GY.pre GAP.pre 4 0 1 -case 2 -xsys 1 -fdhess` | exog | adopted | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (31/31 params) |
| `xsys:xl_it` | VECM_XSYS | `GY.pre GAP.pre 4 0 1 -case 2 -xpre IT.pre -xlink net_gap_it.txt` | exog | adopted | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (19/19 params) |
| `tri:boot_p2_c3` | VECM_TRI | `GY.pre PU.pre PE.pre 2 0 0 -case 3 -lrtest -bootstrap 499` | boot | adopted | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 2 LR rows); bootstrap not rerun |
| `tri:gate_p2_c2` | VECM_TRI | `GY.pre PU.pre PE.pre 2 0 0 -case 2 -diagar -diagma -diagcov` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (5/5 params) |
| `tri:rank_p2_c2` | VECM_TRI | `GY.pre PU.pre PE.pre 2 0 0 -case 2 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 2 LR rows) |
| `tri:gate_p2_c3` | VECM_TRI | `GY.pre PU.pre PE.pre 2 0 0 -case 3 -diagar -diagma -diagcov` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (8/8 params) |
| `tri:rank_p2_c3` | VECM_TRI | `GY.pre PU.pre PE.pre 2 0 0 -case 3 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 2 LR rows) |
| `tri:fit_p2_c3_r2` | VECM_TRI | `GY.pre PU.pre PE.pre 2 0 2 -case 3 -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (25/25 params) |
| `tri:fitG_p2_c3_r1` | VECM_TRI | `GY.pre PU.pre GAPc.pre 2 0 1 -case 3 -fdhess` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (22/22 params) |
| `tri:weakex1_orig` | VECM_TRI | `GY.pre PU.pre PE.pre 2 0 1 -case 3 -weakex 1 -fdhess` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (21/21 params) |
| `tri:weakex1_repar` | VECM_TRI | `GY.pre PU.pre GAPc.pre 2 0 1 -case 3 -weakex 1 -fdhess` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (21/21 params) |
| `tri:weakex2_orig` | VECM_TRI | `GY.pre PU.pre PE.pre 2 0 1 -case 3 -weakex 2 -fdhess` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (21/21 params) |
| `tri:weakex2_repar` | VECM_TRI | `GY.pre PU.pre GAPc.pre 2 0 1 -case 3 -weakex 2 -fdhess` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (21/21 params) |
| `tri:testB_orig` | VECM_TRI | `GY.pre PU.pre PE.pre 2 0 1 -case 3 -fixb2row 2 -1 -fdhess` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (21/21 params) |
| `tri:testB_repar` | VECM_TRI | `GY.pre PU.pre GAPc.pre 2 0 1 -case 3 -fixb2row 2 0 -fdhess` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (21/21 params) |
| `tri:testC_orig` | VECM_TRI | `GY.pre PU.pre PE.pre 2 0 1 -case 3 -fixb2row 2 -1 -weakex 2 -fdhess` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (20/20 params) |
| `tri:testC_repar` | VECM_TRI | `GY.pre PU.pre GAPc.pre 2 0 1 -case 3 -fixb2row 2 0 -weakex 2 -fdhess` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (20/20 params) |
| `tri:cp_r2` | VECM_TRI | `GY.pre PU.pre PE.pre 2 0 2 -case pre` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (24/24 params) |
| `tri:cp_r0` | VECM_TRI | `GY.pre PU.pre PE.pre 2 0 0 -case pre` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (16/16 params) |
| `tri:c4_c3` | VECM_TRI | `GY.pre PU.pre PE.pre 2 0 1 -case 3 -trend` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (23/23 params) |
| `triirf:tri_free` | VECM_TRI_IRF | `GY.pre PU.pre GAPc.pre 2 0 1 -case pre -fdhess` | fit | adopted | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (21/21 params) |
| `triirf:tri_A` | VECM_TRI_IRF | `GY.pre PU.pre GAPc.pre 2 0 1 -case pre -alpha A_gap.txt -fdhess` | restriction | adopted | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (19/19 params) |
| `triirf:tri_c4_A` | VECM_TRI_IRF | `GY.pre PU.pre GAPc.pre 2 0 1 -case pre -trend -alpha A_gap.txt -fdhess` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (20/20 params) |
| `triirf:tri_A_boot` | VECM_TRI_IRF | `GY.pre PU.pre GAPc.pre 2 0 1 -case pre -alpha A_gap.txt -irfboot 999` | irfboot | adopted | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (19/19 params); point fit only, -irfboot not rerun |
| `sub:sub_2005_wx` | VECM_SUB | `GY_M1.pre GAP_2005.pre 4 0 1 -case 2 -fdhess -weakex 1` | fit | adopted | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (17/17 params) |
| `sub:sub_2005_free` | VECM_SUB | `GY_M1.pre GAP_2005.pre 4 0 1 -case 2 -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (18/18 params) |
| `sub:sub_2007_wx` | VECM_SUB | `GY_M1.pre GAP_2007.pre 4 0 1 -case 2 -fdhess -weakex 1` | fit | adopted | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (17/17 params) |
| `sub:sub_2007_free` | VECM_SUB | `GY_M1.pre GAP_2007.pre 4 0 1 -case 2 -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (18/18 params) |
| `sub:sub_2010_wx` | VECM_SUB | `GY_M1.pre GAP_2010.pre 4 0 1 -case 2 -fdhess -weakex 1` | fit | adopted | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (17/17 params) |
| `sub:sub_2010_free` | VECM_SUB | `GY_M1.pre GAP_2010.pre 4 0 1 -case 2 -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (18/18 params) |
| `wti:rank_wtiraw_gy` | VECM_WTI | `WTIraw.pre GY.pre 2 0 0 -case 2 -lrtest -bootstrap 499` | boot | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |
| `wti:rank_tri_wti` | VECM_WTI | `WTI.pre GY.pre GAP.pre 4 0 0 -case 2 -lrtest -bootstrap 499` | boot | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 2 LR rows); bootstrap not rerun |
| `wti:chain` | VECM_WTI | `WTI.pre GY.pre GAP.pre 4 0 1 -case 2 -xsys 1 -fdhess` | exog | adopted | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (31/31 params) |
| `wti:chain_fx` | VECM_WTI | `WTI.pre GY.pre GAP.pre 4 0 1 -case 2 -xsys 1 -fixb2row 1 0 -fdhess -irfboot 499` | irfboot | adopted | **NOT VERIFIABLE**: NOT VERIFIABLE with drvec-py 0.1.0: it refuses -xsys together with -fixb2row (C drvec 0.10 accepted it; the .out reports 'beta restricted by -fixb2row (inputs embedded by -xsys in both)', 'WTI in ec*: held at 0 by -fixb2row', -fdhess and 499 refitted replications). wti:chain (same model without -fixb2row) matches exactly; the LR 0.20 of the restriction is printed in chain_fx.out |
| `wti:tf_WTI_b1s0` | VECM_WTI | `GY.pre WTI.pre -n tf_WTI_b1s0.net` | transfer | adopted | **OK**: logL match exactly; estimates max|d| 3.0e-06, s.e. max|d| 5.9e-04 (10/10 params) |
| `wti:tf_WTI_b1s0_d` | VECM_WTI | `GY.pre WTI.pre -n tf_WTI_b1s0_d.net -c tf_WTI_b1s0_d.cns` | transfer | robustness | **OK**: logL match exactly; estimates max|d| 2.5e-05, s.e. max|d| 3.9e-04 (9/9 params) |
| `wti:tf_WTI_b1s1` | VECM_WTI | `GY.pre WTI.pre -n tf_WTI_b1s1.net` | transfer | robustness | **OK**: logL match exactly; estimates max|d| 1.4e-05, s.e. max|d| 2.1e-03 (11/11 params) |
| `wti:tf_WTI_b1s1_d` | VECM_WTI | `GY.pre WTI.pre -n tf_WTI_b1s1_d.net -c tf_WTI_b1s1_d.cns` | transfer | robustness | **OK**: logL match exactly; estimates max|d| 2.5e-05, s.e. max|d| 7.5e-04 (9/9 params) |
| `wti:tf_WTIraw_b1s0` | VECM_WTI | `GY.pre WTIraw.pre -n tf_WTIraw_b1s0.net` | transfer | robustness | **OK**: logL match exactly; estimates max|d| 1.0e-06, s.e. max|d| 5.8e-05 (7/7 params) |
| `wti:tf_WTIraw_b1s0_d` | VECM_WTI | `GY.pre WTIraw.pre -n tf_WTIraw_b1s0_d.net -c tf_WTI_b1s0_d.cns` | transfer | robustness | **OK**: logL match exactly; estimates max|d| 2.4e-05, s.e. max|d| 7.3e-05 (6/6 params) |
| `wti:tf_WTIraw_b1s1` | VECM_WTI | `GY.pre WTIraw.pre -n tf_WTIraw_b1s1.net` | transfer | robustness | **OK**: logL match exactly; estimates max|d| 1.0e-06, s.e. max|d| 2.7e-04 (8/8 params) |
| `wti:tf_WTIraw_b1s1_d` | VECM_WTI | `GY.pre WTIraw.pre -n tf_WTIraw_b1s1_d.net -c tf_WTI_b1s1_d.cns` | transfer | robustness | **OK**: logL match exactly; estimates max|d| 2.4e-05, s.e. max|d| 1.9e-04 (6/6 params) |
| `fisc:rankA_p1_pre` | VECM_FISC | `REVno.pre G.pre 1 0 0 -case pre -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `fisc:rank_p1_pre` | VECM_FISC | `REV.pre G.pre 1 0 0 -case pre -lrtest` | rank | superseded | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `fisc:rankA_p2_pre` | VECM_FISC | `REVno.pre G.pre 2 0 0 -case pre -lrtest` | rank | adopted | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `fisc:rank_p2_pre` | VECM_FISC | `REV.pre G.pre 2 0 0 -case pre -lrtest` | rank | superseded | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `fisc:rankA_p3_pre` | VECM_FISC | `REVno.pre G.pre 3 0 0 -case pre -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `fisc:rank_p3_pre` | VECM_FISC | `REV.pre G.pre 3 0 0 -case pre -lrtest` | rank | superseded | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `fisc:boot499_p2_pre` | VECM_FISC | `REV.pre G.pre 2 0 0 -case pre -lrtest -bootstrap 499` | boot | superseded | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |
| `fisc:fit_p2_pre_r1` | VECM_FISC | `REV.pre G.pre 2 0 1 -case pre -fdhess` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (11/11 params) |
| `fisc:fit_p2_pre_r1_b1` | VECM_FISC | `REV.pre G.pre 2 0 1 -case pre -fixb2 -1` | restriction | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (10/10 params) |
| `bop:TB_rank_p2` | VECM_BOP | `M.pre X.pre 2 0 0 -case pre -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `bop:TB_rank_p3` | VECM_BOP | `M.pre X.pre 3 0 0 -case pre -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `bop:TB_boot_p3` | VECM_BOP | `M.pre X.pre 3 0 0 -case pre -lrtest -bootstrap 499` | boot | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |
| `bop:TB_fit_p3` | VECM_BOP | `M.pre X.pre 3 0 1 -case pre -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (15/15 params) |
| `bop:TB_fitb1_p3` | VECM_BOP | `M.pre X.pre 3 0 1 -case pre -fixb2 -1` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (14/14 params) |
| `bop:CA_rank_p1` | VECM_BOP | `CAd.pre CAc.pre 1 0 0 -case pre -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `bop:CA_rank_p2` | VECM_BOP | `CAd.pre CAc.pre 2 0 0 -case pre -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `bop:CA_rank_p3` | VECM_BOP | `CAd.pre CAc.pre 3 0 0 -case pre -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `bop:CA_boot_p3` | VECM_BOP | `CAd.pre CAc.pre 3 0 0 -case pre -lrtest -bootstrap 499` | boot | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |
| `bop:CA_fit_p3` | VECM_BOP | `CAd.pre CAc.pre 3 0 1 -case pre -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (15/15 params) |
| `bop:CA_fitb1_p3` | VECM_BOP | `CAd.pre CAc.pre 3 0 1 -case pre -fixb2 -1` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (14/14 params) |
| `bop:RT_rank_p1` | VECM_BOP | `Rd.pre Rc.pre 1 0 0 -case pre -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `bop:RT_rank_p2` | VECM_BOP | `Rd.pre Rc.pre 2 0 0 -case pre -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `bop:RT_fit_p2` | VECM_BOP | `Rd.pre Rc.pre 2 0 1 -case pre -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (11/11 params) |
| `bop:RT_fitb1_p2` | VECM_BOP | `Rd.pre Rc.pre 2 0 1 -case pre -fixb2 -1` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (10/10 params) |
| `pce:gate_p4_c2` | VECM_PCE | `GY.pre GAPPCE.pre 4 0 0 -case 2 -diagar -diagma -diagcov` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (7/7 params) |
| `pce:rank_c2_p1` | VECM_PCE | `GY.pre GAPPCE.pre 1 0 0 -case 2 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `pce:rank_c2_p2` | VECM_PCE | `GY.pre GAPPCE.pre 2 0 0 -case 2 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `pce:rank_c2_p3` | VECM_PCE | `GY.pre GAPPCE.pre 3 0 0 -case 2 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `pce:rank_c2_p4` | VECM_PCE | `GY.pre GAPPCE.pre 4 0 0 -case 2 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `pce:gate_p4_c3` | VECM_PCE | `GY.pre GAPPCE.pre 4 0 0 -case 3 -diagar -diagma -diagcov` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (9/9 params) |
| `pce:rank_c3_p1` | VECM_PCE | `GY.pre GAPPCE.pre 1 0 0 -case 3 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `pce:rank_c3_p2` | VECM_PCE | `GY.pre GAPPCE.pre 2 0 0 -case 3 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `pce:rank_c3_p3` | VECM_PCE | `GY.pre GAPPCE.pre 3 0 0 -case 3 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `pce:rank_c3_p4` | VECM_PCE | `GY.pre GAPPCE.pre 4 0 0 -case 3 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `pce:fit_p4_c2_r1` | VECM_PCE | `GY.pre GAPPCE.pre 4 0 1 -case 2 -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (18/18 params) |
| `pce:fit_p4_c2_r1_wx` | VECM_PCE | `GY.pre GAPPCE.pre 4 0 1 -case 2 -fdhess -weakex 1` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (17/17 params) |
| `pce:fit_p4_c3_r1` | VECM_PCE | `GY.pre GAPPCE.pre 4 0 1 -case 3 -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (19/19 params) |
| `pce:fit_p4_pre_r1` | VECM_PCE | `GY.pre GAPPCE.pre 4 0 1 -case pre -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (18/18 params) |
| `pce:fit_p2_c2_r1` | VECM_PCE | `GY.pre GAPPCE.pre 2 0 1 -case 2 -fdhess` | fit | adopted | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (10/10 params) |
| `pce:fit_p2_c2_r1_wx` | VECM_PCE | `GY.pre GAPPCE.pre 2 0 1 -case 2 -fdhess -weakex 1` | fit | adopted | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (9/9 params) |
| `pce:fit_p3_c2_r1` | VECM_PCE | `GY.pre GAPPCE.pre 3 0 1 -case 2` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (14/14 params) |
| `pce:boot999_p2_c2` | VECM_PCE | `GY.pre GAPPCE.pre 2 0 0 -case 2 -lrtest -bootstrap 999` | boot | adopted | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |
| `pce:boot999_p4_c2` | VECM_PCE | `GY.pre GAPPCE.pre 4 0 0 -case 2 -lrtest -bootstrap 999` | boot | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |
| `pce:tri_gate` | VECM_PCE | `GY.pre PCEUSA.pre PCEEC.pre 2 0 0 -case pre -diagar -diagma -diagcov` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (7/7 params) |
| `pce:tri_rank_p1` | VECM_PCE | `GY.pre PCEUSA.pre PCEEC.pre 1 0 0 -case pre -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 2 LR rows) |
| `pce:tri_rank_p2` | VECM_PCE | `GY.pre PCEUSA.pre PCEEC.pre 2 0 0 -case pre -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 2 LR rows) |
| `pce:tri_rank_p3` | VECM_PCE | `GY.pre PCEUSA.pre PCEEC.pre 3 0 0 -case pre -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 2 LR rows) |
| `pce:tri_r1` | VECM_PCE | `GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (21/21 params) |
| `pce:tri_A` | VECM_PCE | `GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -weakex 2` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (20/20 params) |
| `pce:tri_B` | VECM_PCE | `GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -fixb2row 2 -1` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (20/20 params) |
| `pce:tri_C` | VECM_PCE | `GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -fixb2row 2 -1 -weakex 2` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (19/19 params) |
| `pce:tri_c4_r1` | VECM_PCE | `GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -trend -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (22/22 params) |
| `pce:tri_c4_B` | VECM_PCE | `GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -trend -fixb2row 2 -1` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (21/21 params) |
| `pce:tri_c4_A` | VECM_PCE | `GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -trend -weakex 2` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (21/21 params) |
| `pce:tri_boot499_p2` | VECM_PCE | `GY.pre PCEUSA.pre PCEEC.pre 2 0 0 -case pre -lrtest -bootstrap 499` | boot | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 2 LR rows); bootstrap not rerun |
| `pce:tri_boot499_p2_c3` | VECM_PCE | `GY.pre PCEUSA.pre PCEEC.pre 2 0 0 -case 3 -lrtest -bootstrap 499` | boot | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 2 LR rows); bootstrap not rerun |
| `pce:tri_r2_pre_ms` | VECM_PCE | `GY.pre PCEUSA.pre PCEEC.pre 2 0 2 -case pre -multistart 10` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (24/24 params) |
| `gdpdg:gate_p3_c2` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 3 0 0 -case 2 -diagar -diagma -diagcov` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (5/5 params) |
| `gdpdg:gate_p3_c3` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 3 0 0 -case 3 -diagar -diagma -diagcov` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (7/7 params) |
| `gdpdg:rank_c2_p2` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 2 0 0 -case 2 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `gdpdg:fit_p2_c2_r1` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 2 0 1 -case 2 -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (10/10 params) |
| `gdpdg:fit_p2_c2_r1_wx` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 2 0 1 -case 2 -fdhess -weakex 1` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (9/9 params) |
| `gdpdg:boot999_p2_c2` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 2 0 0 -case 2 -lrtest -bootstrap 999` | boot | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |
| `gdpdg:rank_c2_p3` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 3 0 0 -case 2 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `gdpdg:fit_p3_c2_r1` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 3 0 1 -case 2 -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (14/14 params) |
| `gdpdg:fit_p3_c2_r1_wx` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 3 0 1 -case 2 -fdhess -weakex 1` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (13/13 params) |
| `gdpdg:boot999_p3_c2` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 3 0 0 -case 2 -lrtest -bootstrap 999` | boot | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |
| `gdpdg:rank_c3_p3` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 3 0 0 -case 3 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `gdpdg:fit_p3_c3_r1` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 3 0 1 -case 3` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (15/15 params) |
| `gdpdg:rank_c2_p1` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 1 0 0 -case 2 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `gdpdg:rank_c2_p4` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 4 0 0 -case 2 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `gdpdg:gate_p4_c2` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 4 0 0 -case 2 -diagar -diagma -diagcov` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (7/7 params) |
| `gdpdg:rank_c3_p1` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 1 0 0 -case 3 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `gdpdg:rank_c3_p2` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 2 0 0 -case 3 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `gdpdg:rank_c3_p4` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 4 0 0 -case 3 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `gdpdg:gate_p4_c3` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 4 0 0 -case 3 -diagar -diagma -diagcov` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (9/9 params) |
| `gdpdg:fit_p2_c3_r1` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 2 0 1 -case 3 -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (11/11 params) |
| `gdpdg:fit_p2_pre_r1` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 2 0 1 -case pre -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (10/10 params) |
| `gdpdg:fit_p3_pre_r1` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 3 0 1 -case pre -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (14/14 params) |
| `gdpdg:fit_p4_c3_r1` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 4 0 1 -case 3 -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (19/19 params) |
| `gdpdg:fit_p4_pre_r1` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 4 0 1 -case pre -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (18/18 params) |
| `gdpdg:fit_p4_c2_r1` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 4 0 1 -case 2 -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (18/18 params) |
| `gdpdg:fit_p4_c2_r1_wx` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 4 0 1 -case 2 -fdhess -weakex 1` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (17/17 params) |
| `gdpdg:tri_rank_cpre_p1` | VECM_GDPD_G | `GY.pre GDPDUSA.pre GDPDEC.pre 1 0 0 -case pre -lrtest` | rank | robustness | **ARGS OK, OPTIMUM DIFFERS**: args confirmed: logL(r=0), logL(r=1) and LR(r=0) = 21.6724 match exactly; the original .out has no r=2 row (port prints r=2 too) |
| `gdpdg:tri_rank_c3_p1` | VECM_GDPD_G | `GY.pre GDPDUSA.pre GDPDEC.pre 1 0 0 -case 3 -lrtest` | rank | robustness | **ARGS OK, OPTIMUM DIFFERS**: args confirmed: logL(r=0), logL(r=1) and LR(r=0) = 25.0774 match exactly; the original .out has no r=2 row (port prints r=2 too) |
| `gdpdg:tri_r2_pre_ms` | VECM_GDPD_G | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 2 -case pre -multistart 10` | fit | robustness | **ARGS OK, OPTIMUM DIFFERS**: args confirmed but optimum differs: port logL -353.680692128 > original -356.1879591585 (r=2 surface is multimodal; C 0.10 stopped at a worse local optimum; with -multistart 10 the per-start logLs that converged in C reappear in the port (e.g. seed/jitter 3), the port also converges the starts C failed); estimates max|d| 2.3e+02, s.e. max|d| 1.5e+02 (24/24 params) |
| `gdpdg:tri_r2_c3` | VECM_GDPD_G | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 2 -case 3 -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (25/25 params) |
| `gdpdg:tri_c4_r1` | VECM_GDPD_G | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 1 -case pre -trend -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (22/22 params) |
| `gdpdg:tri_c4_B` | VECM_GDPD_G | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 1 -case pre -trend -fixb2row 2 -1` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (21/21 params) |
| `gdpdg:tri_c4_A` | VECM_GDPD_G | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 1 -case pre -trend -weakex 2` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (21/21 params) |
| `gdpdg:tri_r1_p3` | VECM_GDPD_G | `GY.pre GDPDUSA.pre GDPDEC.pre 3 0 1 -case pre -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (30/30 params) |
| `gdpdg:boot999_p4_c2` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 4 0 0 -case 2 -lrtest -bootstrap 999` | boot | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |
| `gdpdg:boot999_p3_c3` | VECM_GDPD_G | `GY.pre GAPGDPD.pre 3 0 0 -case 3 -lrtest -bootstrap 999` | boot | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |
| `gdpdg:tri_boot499_cpre_p2` | VECM_GDPD_G | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 0 -case pre -lrtest -bootstrap 499` | boot | robustness | **ARGS OK, OPTIMUM DIFFERS**: args confirmed: logL(r=0), logL(r=1) and LR(r=0) = 11.0005 match exactly; r=2 optimum differs: port logL -356.188 > original -372.1459 (C 0.10 stopped at a worse local optimum, so the original LR(r<=1) -38.0873 becomes -6.1715); bootstrap not rerun |
| `gdpdg:tri_gate` | VECM_GDPD_G | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 0 -case pre -diagar -diagma -diagcov` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (7/7 params) |
| `gdpdg:tri_rank_cpre_p2` | VECM_GDPD_G | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 0 -case pre -lrtest` | rank | robustness | **ARGS OK, OPTIMUM DIFFERS**: args confirmed: logL(r=0), logL(r=1) and LR(r=0) = 11.0005 match exactly; r=2 optimum differs: port logL -356.188 > original -372.1459 (C 0.10 stopped at a worse local optimum, so the original LR(r<=1) -38.0873 becomes -6.1715) |
| `gdpdg:tri_rank_c3_p2` | VECM_GDPD_G | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 0 -case 3 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 2 LR rows) |
| `gdpdg:tri_boot499_c3_p2` | VECM_GDPD_G | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 0 -case 3 -lrtest -bootstrap 499` | boot | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 2 LR rows); bootstrap not rerun |
| `gdpdg:tri_rank_cpre_p3` | VECM_GDPD_G | `GY.pre GDPDUSA.pre GDPDEC.pre 3 0 0 -case pre -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 2 LR rows) |
| `gdpdg:tri_rank_c3_p3` | VECM_GDPD_G | `GY.pre GDPDUSA.pre GDPDEC.pre 3 0 0 -case 3 -lrtest` | rank | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 2 LR rows) |
| `gdpdg:tri_boot499_c3_p3` | VECM_GDPD_G | `GY.pre GDPDUSA.pre GDPDEC.pre 3 0 0 -case 3 -lrtest -bootstrap 499` | boot | robustness | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 2 LR rows); bootstrap not rerun |
| `gdpdg:tri_r1` | VECM_GDPD_G | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 1 -case pre -fdhess` | fit | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (21/21 params) |
| `gdpdg:tri_A` | VECM_GDPD_G | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 1 -case pre -weakex 2` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (20/20 params) |
| `gdpdg:tri_B` | VECM_GDPD_G | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 1 -case pre -fixb2row 2 -1` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (20/20 params) |
| `gdpdg:tri_C` | VECM_GDPD_G | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 1 -case pre -fixb2row 2 -1 -weakex 2` | restriction | robustness | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (19/19 params) |
| `gdpd:gate_p3_c2` | VECM_GDPD | `GY.pre GAPGDPD.pre 3 0 0 -case 2 -diagar -diagma -diagcov` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (5/5 params) |
| `gdpd:gate_p3_c3` | VECM_GDPD | `GY.pre GAPGDPD.pre 3 0 0 -case 3 -diagar -diagma -diagcov` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (7/7 params) |
| `gdpd:rank_c2_p2` | VECM_GDPD | `GY.pre GAPGDPD.pre 2 0 0 -case 2 -lrtest` | rank | superseded | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `gdpd:fit_p2_c2_r1` | VECM_GDPD | `GY.pre GAPGDPD.pre 2 0 1 -case 2 -fdhess` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (10/10 params) |
| `gdpd:fit_p2_c2_r1_wx` | VECM_GDPD | `GY.pre GAPGDPD.pre 2 0 1 -case 2 -fdhess -weakex 1` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (9/9 params) |
| `gdpd:boot999_p2_c2` | VECM_GDPD | `GY.pre GAPGDPD.pre 2 0 0 -case 2 -lrtest -bootstrap 999` | boot | superseded | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |
| `gdpd:rank_c2_p3` | VECM_GDPD | `GY.pre GAPGDPD.pre 3 0 0 -case 2 -lrtest` | rank | superseded | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `gdpd:fit_p3_c2_r1` | VECM_GDPD | `GY.pre GAPGDPD.pre 3 0 1 -case 2 -fdhess` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (14/14 params) |
| `gdpd:fit_p3_c2_r1_wx` | VECM_GDPD | `GY.pre GAPGDPD.pre 3 0 1 -case 2 -fdhess -weakex 1` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (13/13 params) |
| `gdpd:boot999_p3_c2` | VECM_GDPD | `GY.pre GAPGDPD.pre 3 0 0 -case 2 -lrtest -bootstrap 999` | boot | superseded | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |
| `gdpd:rank_c3_p3` | VECM_GDPD | `GY.pre GAPGDPD.pre 3 0 0 -case 3 -lrtest` | rank | superseded | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `gdpd:fit_p3_c3_r1` | VECM_GDPD | `GY.pre GAPGDPD.pre 3 0 1 -case 3` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (15/15 params) |
| `gdpd:rank_c2_p1` | VECM_GDPD | `GY.pre GAPGDPD.pre 1 0 0 -case 2 -lrtest` | rank | superseded | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `gdpd:rank_c2_p4` | VECM_GDPD | `GY.pre GAPGDPD.pre 4 0 0 -case 2 -lrtest` | rank | superseded | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `gdpd:gate_p4_c2` | VECM_GDPD | `GY.pre GAPGDPD.pre 4 0 0 -case 2 -diagar -diagma -diagcov` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (7/7 params) |
| `gdpd:rank_c3_p1` | VECM_GDPD | `GY.pre GAPGDPD.pre 1 0 0 -case 3 -lrtest` | rank | superseded | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `gdpd:rank_c3_p2` | VECM_GDPD | `GY.pre GAPGDPD.pre 2 0 0 -case 3 -lrtest` | rank | superseded | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `gdpd:rank_c3_p4` | VECM_GDPD | `GY.pre GAPGDPD.pre 4 0 0 -case 3 -lrtest` | rank | superseded | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows) |
| `gdpd:gate_p4_c3` | VECM_GDPD | `GY.pre GAPGDPD.pre 4 0 0 -case 3 -diagar -diagma -diagcov` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (9/9 params) |
| `gdpd:fit_p2_c3_r1` | VECM_GDPD | `GY.pre GAPGDPD.pre 2 0 1 -case 3 -fdhess` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (11/11 params) |
| `gdpd:fit_p2_pre_r1` | VECM_GDPD | `GY.pre GAPGDPD.pre 2 0 1 -case pre -fdhess` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (10/10 params) |
| `gdpd:fit_p3_pre_r1` | VECM_GDPD | `GY.pre GAPGDPD.pre 3 0 1 -case pre -fdhess` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (14/14 params) |
| `gdpd:fit_p4_c3_r1` | VECM_GDPD | `GY.pre GAPGDPD.pre 4 0 1 -case 3 -fdhess` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (19/19 params) |
| `gdpd:fit_p4_pre_r1` | VECM_GDPD | `GY.pre GAPGDPD.pre 4 0 1 -case pre -fdhess` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (18/18 params) |
| `gdpd:fit_p4_c2_r1` | VECM_GDPD | `GY.pre GAPGDPD.pre 4 0 1 -case 2 -fdhess` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (18/18 params) |
| `gdpd:fit_p4_c2_r1_wx` | VECM_GDPD | `GY.pre GAPGDPD.pre 4 0 1 -case 2 -fdhess -weakex 1` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (17/17 params) |
| `gdpd:tri_rank_cpre_p1` | VECM_GDPD | `GY.pre GDPDUSA.pre GDPDEC.pre 1 0 0 -case pre -lrtest` | rank | superseded | **ARGS OK, OPTIMUM DIFFERS**: args confirmed: logL(r=0), logL(r=1) and LR(r=0) = 23.6531 match exactly; r=2 optimum differs: port logL -368.5772 > original -392.7893 (C 0.10 stopped at a worse local optimum, so the original LR(r<=1) -66.6069 becomes -18.1827) |
| `gdpd:tri_rank_c3_p1` | VECM_GDPD | `GY.pre GDPDUSA.pre GDPDEC.pre 1 0 0 -case 3 -lrtest` | rank | superseded | **ARGS OK, OPTIMUM DIFFERS**: args confirmed: logL(r=0), logL(r=1) and LR(r=0) = 27.4687 match exactly; r=2 optimum differs: port logL -380.653 > original -390.899 (C 0.10 stopped at a worse local optimum, so the original LR(r<=1) -66.9654 becomes -46.4733) |
| `gdpd:tri_r2_pre_ms` | VECM_GDPD | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 2 -case pre -multistart 10` | fit | superseded | **ARGS OK, OPTIMUM DIFFERS**: args confirmed but optimum differs: port logL -346.7987271909 > original -347.0228141873 (r=2 surface is multimodal; C 0.10 stopped at a worse local optimum; with -multistart 10 the per-start logLs that converged in C reappear in the port (e.g. seed/jitter 3), the port also converges the starts C failed); estimates max|d| 1.9e+02, s.e. max|d| 7.6e+01 (24/24 params) |
| `gdpd:tri_r2_c3` | VECM_GDPD | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 2 -case 3 -fdhess` | fit | superseded | **ARGS OK, OPTIMUM DIFFERS**: args confirmed but optimum differs: port logL -341.321112029 > original -342.9324900147 (r=2 surface is multimodal; C 0.10 stopped at a worse local optimum); estimates max|d| 7.5e+02, s.e. max|d| 8.1e+01 (25/25 params) |
| `gdpd:tri_c4_r1` | VECM_GDPD | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 1 -case pre -trend -fdhess` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (22/22 params) |
| `gdpd:tri_c4_B` | VECM_GDPD | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 1 -case pre -trend -fixb2row 2 -1` | restriction | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (21/21 params) |
| `gdpd:tri_c4_A` | VECM_GDPD | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 1 -case pre -trend -weakex 2` | restriction | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (21/21 params) |
| `gdpd:tri_r1_p3` | VECM_GDPD | `GY.pre GDPDUSA.pre GDPDEC.pre 3 0 1 -case pre -fdhess` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (30/30 params) |
| `gdpd:boot999_p4_c2` | VECM_GDPD | `GY.pre GAPGDPD.pre 4 0 0 -case 2 -lrtest -bootstrap 999` | boot | superseded | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |
| `gdpd:boot999_p3_c3` | VECM_GDPD | `GY.pre GAPGDPD.pre 3 0 0 -case 3 -lrtest -bootstrap 999` | boot | superseded | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |
| `gdpd:tri_boot499_cpre_p2` | VECM_GDPD | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 0 -case pre -lrtest -bootstrap 499` | boot | superseded | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 2 LR rows); bootstrap not rerun |
| `gdpd:tri_gate` | VECM_GDPD | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 0 -case pre -diagar -diagma -diagcov` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (7/7 params) |
| `gdpd:tri_rank_cpre_p2` | VECM_GDPD | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 0 -case pre -lrtest` | rank | superseded | **OK**: rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 2 LR rows) |
| `gdpd:tri_rank_c3_p2` | VECM_GDPD | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 0 -case 3 -lrtest` | rank | superseded | **ARGS OK, OPTIMUM DIFFERS**: args confirmed: logL(r=0), logL(r=1) and LR(r=0) = 13.8332 match exactly; r=2 optimum differs: port logL -341.3211 > original -342.9325 (C 0.10 stopped at a worse local optimum, so the original LR(r<=1) -2.5741 becomes 0.6486) |
| `gdpd:tri_boot499_c3_p2` | VECM_GDPD | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 0 -case 3 -lrtest -bootstrap 499` | boot | superseded | **ARGS OK, OPTIMUM DIFFERS**: args confirmed: logL(r=0), logL(r=1) and LR(r=0) = 13.8332 match exactly; r=2 optimum differs: port logL -341.3211 > original -342.9325 (C 0.10 stopped at a worse local optimum, so the original LR(r<=1) -2.5741 becomes 0.6486); bootstrap not rerun |
| `gdpd:tri_rank_cpre_p3` | VECM_GDPD | `GY.pre GDPDUSA.pre GDPDEC.pre 3 0 0 -case pre -lrtest` | rank | superseded | **ARGS OK, OPTIMUM DIFFERS**: args confirmed: logL(r=0), logL(r=1) and LR(r=0) = 12.5315 match exactly; r=2 optimum differs: port logL -341.0907 > original -345.138 (C 0.10 stopped at a worse local optimum, so the original LR(r<=1) -19.0433 becomes -10.9487) |
| `gdpd:tri_rank_c3_p3` | VECM_GDPD | `GY.pre GDPDUSA.pre GDPDEC.pre 3 0 0 -case 3 -lrtest` | rank | superseded | **ARGS OK, OPTIMUM DIFFERS**: args confirmed: logL(r=0), logL(r=1) and LR(r=0) = 13.0115 match exactly; r=2 optimum differs: port logL -333.4115 > original -347.4222 (C 0.10 stopped at a worse local optimum, so the original LR(r<=1) -25.017 becomes 3.0044) |
| `gdpd:tri_boot499_c3_p3` | VECM_GDPD | `GY.pre GDPDUSA.pre GDPDEC.pre 3 0 0 -case 3 -lrtest -bootstrap 499` | boot | superseded | **ARGS OK, OPTIMUM DIFFERS**: args confirmed: logL(r=0), logL(r=1) and LR(r=0) = 13.0115 match exactly; r=2 optimum differs: port logL -333.4115 > original -347.4222 (C 0.10 stopped at a worse local optimum, so the original LR(r<=1) -25.017 becomes 3.0044); bootstrap not rerun |
| `gdpd:tri_r1` | VECM_GDPD | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 1 -case pre -fdhess` | fit | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (21/21 params) |
| `gdpd:tri_A` | VECM_GDPD | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 1 -case pre -weakex 2` | restriction | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (20/20 params) |
| `gdpd:tri_B` | VECM_GDPD | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 1 -case pre -fixb2row 2 -1` | restriction | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (20/20 params) |
| `gdpd:tri_C` | VECM_GDPD | `GY.pre GDPDUSA.pre GDPDEC.pre 2 0 1 -case pre -fixb2row 2 -1 -weakex 2` | restriction | superseded | **OK**: logL match exactly; estimates max|d| 0, s.e. max|d| 0 (19/19 params) |
| `rec:theta_recursive` | VECM_REC | `DRVEC=drvec-py python theta_recursive.py   # per sample: drvec GY_M1.pre GAP_<kind>_<a>_<b>_<wx|free>.pre 4 0 1 -case 2 -fdhess [-weakex 1] -name <kind>_<a>_<b>_<wx|free>; fwd: 2003Q1..t, t=2010Q4..2019Q4; bwd: s..2019Q4, s=2003Q1..2011Q4 (146 fits; the GAP .pre is trimmed by the script)` | fit | adopted | 146/146 drvec calls reproduce runs/*.out (logL max|d| 0, estimates max|d| 0) |
| `rec:hj_beta` | VECM_REC | `DRVEC=drvec-py python hj_beta.py   # per t: drvec GY_M1.pre runs/GAP_fwd_0_<t>_wx.pre 4 0 1 -case 2 -weakex 1 -fixb2row 1 -0.386336 -name hj_<t> (37 fits, t=31..67); LR against the free logL in theta_recursive.csv` | restriction | adopted | 37/37 drvec calls reproduce runs/*.out (logL max|d| 0, estimates max|d| 0) |
| `rec:hj_lambda` | VECM_REC | `DRVEC=drvec-py python hj_lambda.py   # per t: drvec GY_M1.pre runs/GAP_fwd_0_<t>_wx.pre 4 0 0 -case 2 -lrtest -name hjl_<t> (37 rank runs)` | rank | adopted | 37/37 drvec calls reproduce runs/*.out (logL max|d| 0, LR max|d| 0) |
| `rec:hjfull_free` | VECM_REC | `GY_M1.pre GAP.pre 4 0 1 -case 2 -writeinp runs/hjfull_inp` | fit | adopted | 1/1 drvec calls reproduce runs/*.out (logL max|d| 0, estimates max|d| 0); -writeinp is NOT ported in drvec-py (refused), so the hjfull_inp.*.inp files need the C drvec or must be shipped as data |
| `rec:hj_boot` | VECM_REC | `B=999 python hj_boot.py   # no drvec call: numpy conditional Johansen VECM on runs/hjfull_inp.{1,2}.inp, iid and wild bootstrap` | boot | adopted | not rerun (pure numpy bootstrap, no drvec call); its input comes from rec:hjfull_free |

## Runs already in `tables/vecm_registry.py` (cross-check against the original `.out`)

| registry run | original .out | verification |
|---|---|---|
| `biv_rank` | VECM_GAP_GY/boot999_p4_c2.out | rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |
| `biv_wx` | VECM_GAP_GY/fit_p4_c2_r1_wx.out | logL match exactly; estimates max|d| 0, s.e. max|d| 0 (17/17 params) |
| `biv_free` | VECM_GAP_GY/fit_p4_c2_r1.out | logL match exactly; estimates max|d| 0, s.e. max|d| 0 (18/18 params) |
| `aug_rank` | VECM_AUG/m05/boot_p4_c2.out | rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 2 LR rows); bootstrap not rerun |
| `aug_r2` | VECM_AUG/m05/fit_p4_c2_r2.out | logL match exactly; estimates max|d| 0, s.e. max|d| 0 (42/42 params) |
| `tri_rank` | VECM_TRI/cp_boot.out | rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 2 LR rows); bootstrap not rerun |
| `tri_r1` | VECM_TRI/cp_r1.out | logL match exactly; estimates max|d| 0, s.e. max|d| 0 (21/21 params) |
| `tri_A` | VECM_TRI/cp_A.out | logL match exactly; estimates max|d| 0, s.e. max|d| 0 (20/20 params) |
| `tri_B` | VECM_TRI/cp_B.out | logL match exactly; estimates max|d| 0, s.e. max|d| 0 (20/20 params) |
| `tri_C` | VECM_TRI/cp_C.out | logL match exactly; estimates max|d| 0, s.e. max|d| 0 (19/19 params) |
| `tri3_r1` | VECM_TRI/fit_p2_c3_r1.out | logL match exactly; estimates max|d| 0, s.e. max|d| 0 (22/22 params) |
| `tri3_A` | VECM_TRI/weakex2_orig.out | logL match exactly; estimates max|d| 0, s.e. max|d| 6.2e+00 (21/21 params) |
| `tri3_B` | VECM_TRI/testB_orig.out | logL match exactly; estimates max|d| 0, s.e. max|d| 3.9e+00 (21/21 params) |
| `tri3_C` | VECM_TRI/testC_orig.out | logL match exactly; estimates max|d| 0, s.e. max|d| 5.7e+00 (20/20 params) |
| `tri4_r1` | VECM_TRI/c4_r1.out | logL match exactly; estimates max|d| 0, s.e. max|d| 0 (22/22 params) |
| `tri4_A` | VECM_TRI/c4_A.out | logL match exactly; estimates max|d| 0, s.e. max|d| 0 (21/21 params) |
| `tri4_B` | VECM_TRI/c4_B.out | logL match exactly; estimates max|d| 0, s.e. max|d| 0 (21/21 params) |
| `tri4_C` | VECM_TRI/c4_C.out | logL match exactly; estimates max|d| 0, s.e. max|d| 0 (20/20 params) |
| `wti_rank` | VECM_WTI/rank_wti_gy.out | rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |
| `fisc_rank` | VECM_FISC/bootA499_p2_pre.out | rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |
| `fisc_free` | VECM_FISC/fitA_p2_pre_r1.out | logL match exactly; estimates max|d| 0, s.e. max|d| 0 (11/11 params) |
| `fisc_b1` | VECM_FISC/fitA_p2_pre_r1_b1.out | logL match exactly; estimates max|d| 0, s.e. max|d| 1.5e-02 (10/10 params) |
| `tb_rank` | VECM_BOP/TB_boot_p2.out | rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |
| `tb_free` | VECM_BOP/TB_fit_p2.out | logL match exactly; estimates max|d| 0, s.e. max|d| 0 (11/11 params) |
| `tb_b1` | VECM_BOP/TB_fitb1_p2.out | logL match exactly; estimates max|d| 0, s.e. max|d| 4.2e-02 (10/10 params) |
| `ca_rank` | VECM_BOP/CA_boot_p2.out | rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |
| `ca_free` | VECM_BOP/CA_fit_p2.out | logL match exactly; estimates max|d| 0, s.e. max|d| 0 (11/11 params) |
| `ca_b1` | VECM_BOP/CA_fitb1_p2.out | logL match exactly; estimates max|d| 0, s.e. max|d| 5.6e-02 (10/10 params) |
| `rt_rank` | VECM_BOP/RT_boot_p2.out | rank LR table match: logL(r) max|d| 0, LR max|d| 0 (printed to 4 dp; 1 LR rows); bootstrap not rerun |

## Inputs each directory needs

Only these files have to be copied into `<dir>` (paths relative to it). Registry runs included.

| dir | inputs |
|---|---|
| VECM_AUG | `BXE.pre`, `GAP.pre`, `GY.pre`, `net_b1.txt`, `net_gap_bxe.txt`, `net_r1.txt`, `net_s1.txt` |
| VECM_AUG/m05 | `BXE.pre`, `GAP.pre`, `GY.pre`, `net_b1.txt`, `net_gap_bxe.txt`, `net_r1.txt`, `net_s1.txt` |
| VECM_BOP | `CAc.pre`, `CAd.pre`, `M.pre`, `Rc.pre`, `Rd.pre`, `X.pre` |
| VECM_FISC | `G.pre`, `REV.pre`, `REVno.pre` |
| VECM_GAP_GY | `GAP.pre`, `GAP_noint.pre`, `GY_M1.pre`, `GY_M2.pre`, `GY_noint.pre` |
| VECM_GDPD | `GAPGDPD.pre`, `GDPDEC.pre`, `GDPDUSA.pre`, `GY.pre` |
| VECM_GDPD_G | `GAPGDPD.pre`, `GDPDEC.pre`, `GDPDUSA.pre`, `GY.pre` |
| VECM_PCE | `GAPPCE.pre`, `GY.pre`, `PCEEC.pre`, `PCEUSA.pre` |
| VECM_SUB | `GAP_2005.pre`, `GAP_2007.pre`, `GAP_2010.pre`, `GY_M1.pre` |
| VECM_TRI | `GAPc.pre`, `GY.pre`, `PE.pre`, `PU.pre` |
| VECM_TRI_IRF | `A_gap.txt`, `GAPc.pre`, `GY.pre`, `PU.pre` |
| VECM_WTI | `GAP.pre`, `GY.pre`, `WTI.pre`, `WTIraw.pre`, `tf_WTI_b1s0.net`, `tf_WTI_b1s0_d.cns`, `tf_WTI_b1s0_d.net`, `tf_WTI_b1s1.net`, `tf_WTI_b1s1_d.cns`, `tf_WTI_b1s1_d.net`, `tf_WTIraw_b1s0.net`, `tf_WTIraw_b1s0_d.net`, `tf_WTIraw_b1s1.net`, `tf_WTIraw_b1s1_d.net` |
| VECM_XSYS | `GAP.pre`, `GY.pre`, `IT.pre`, `net_gap_it.txt` |
| VECM_REC | `theta_recursive.py`, `hj_beta.py`, `hj_lambda.py`, `hj_boot.py`, plus `../VECM_GAP_GY/GY_M1.pre` and `../VECM_GAP_GY/GAP.pre` (the drivers write `runs/GAP_*.pre` themselves); `hj_boot.py` also needs `runs/hjfull_inp.1.inp`, `runs/hjfull_inp.2.inp` (C drvec `-writeinp`) |

Directories that are only superseded and could be left out of the public repository: `VECM_AUG` (parent, BXE m04), `VECM_GDPD` (autonomous deflator univariates; kept as the intermediate version), the REV-with-oil-step runs in `VECM_FISC` (`REV.pre`).

## Skipped / outside this registry

- Every `.out` in the relevant `VECM_*` directories is covered (262 here + 30 in the tables registry); none was skipped. Runs not quoted anywhere are kept with `status: exploratory` (`biv:chk_fixb2`, `biv:chk_fixb2row`: a consistency check that `-fixb2 v` equals `-fixb2row 1 v`) or `superseded`.
- `revision-suite/Python/wti_gy_v10.py` and its `wti_v10_output/{drvec,drtran}/` (rank_/fit_/tf_ runs with the old G/Y `GY_m01_ar1`, without the CFDD step): superseded by VECM_WTI; only the 'Antes' columns of RES 5.4 quote them. Its commands are generated in that script (`run_drvec`, `run_drtran`); not reconstructed here.
- `replica*` (re-runs of C drvec versions) ignored as instructed.
- Root-level `WTI_m*.out`, `GY_m01_ar1.out` and the univariate directories are fue/art outputs, not drvec.
