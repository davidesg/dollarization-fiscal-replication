"""The drvec runs behind the multivariate tables.

Each run is (directory under art_drvec/, drvec arguments without -name). The
inputs are the adopted `.pre` files in that directory; `make_tables.py` copies
them to `build/drvec/<run>/` and runs drvec there (see `vecm.py`). Bootstrap
runs are cached by a hash of the inputs, the arguments and the drvec binary.

Order of the series: the nabla-Y2 block first, the Y1 block (normalised in
beta) last. With beta = (1, -1) imposed (`-fixb2 -1`), a positive alpha on the
Y2 variable and a negative alpha on the Y1 variable correct.
"""

RUNS = {
    # central bivariate (G/Y | GAP), p = 4, case 2
    "biv_rank": ("VECM_GAP_GY", "GY_M1.pre GAP.pre 4 0 0 -case 2 -lrtest -bootstrap 999"),
    "biv_wx": ("VECM_GAP_GY", "GY_M1.pre GAP.pre 4 0 1 -case 2 -fdhess -weakex 1"),
    "biv_free": ("VECM_GAP_GY", "GY_M1.pre GAP.pre 4 0 1 -case 2 -fdhess"),
    # augmented with BXE (m05), p = 4, case 2
    "aug_rank": ("VECM_AUG/m05", "GY.pre BXE.pre GAP.pre 4 0 0 -case 2 -lrtest -bootstrap 499"),
    "aug_r2": ("VECM_AUG/m05", "GY.pre BXE.pre GAP.pre 4 0 2 -case 2 -fdhess"),
    # trivariate (G/Y, PU | PE), p = 2, drifts free
    "tri_rank": ("VECM_TRI", "GY.pre PU.pre PE.pre 2 0 0 -case pre -lrtest -bootstrap 499"),
    "tri_r1": ("VECM_TRI", "GY.pre PU.pre PE.pre 2 0 1 -case pre -fdhess"),
    "tri_A": ("VECM_TRI", "GY.pre PU.pre PE.pre 2 0 1 -case pre -weakex 2"),
    "tri_B": ("VECM_TRI", "GY.pre PU.pre PE.pre 2 0 1 -case pre -fixb2row 2 -1"),
    "tri_C": ("VECM_TRI", "GY.pre PU.pre PE.pre 2 0 1 -case pre -fixb2row 2 -1 -weakex 2"),
    "tri3_r1": ("VECM_TRI", "GY.pre PU.pre PE.pre 2 0 1 -case 3 -fdhess"),
    "tri3_A": ("VECM_TRI", "GY.pre PU.pre PE.pre 2 0 1 -case 3 -weakex 2"),
    "tri3_B": ("VECM_TRI", "GY.pre PU.pre PE.pre 2 0 1 -case 3 -fixb2row 2 -1"),
    "tri3_C": ("VECM_TRI", "GY.pre PU.pre PE.pre 2 0 1 -case 3 -fixb2row 2 -1 -weakex 2"),
    "tri4_r1": ("VECM_TRI", "GY.pre PU.pre PE.pre 2 0 1 -case pre -trend -fdhess"),
    "tri4_A": ("VECM_TRI", "GY.pre PU.pre PE.pre 2 0 1 -case pre -trend -weakex 2"),
    "tri4_B": ("VECM_TRI", "GY.pre PU.pre PE.pre 2 0 1 -case pre -trend -fixb2row 2 -1"),
    "tri4_C": ("VECM_TRI", "GY.pre PU.pre PE.pre 2 0 1 -case pre -trend -fixb2row 2 -1 -weakex 2"),
    # trivariate with the consumption deflators (G/Y, PCU | PCE), p = 2
    "pce_r1": ("VECM_PCE", "GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -fdhess"),
    "pce_A": ("VECM_PCE", "GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -weakex 2"),
    "pce_B": ("VECM_PCE", "GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -fixb2row 2 -1"),
    "pce_C": ("VECM_PCE", "GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -fixb2row 2 -1 -weakex 2"),
    "pce4_r1": ("VECM_PCE", "GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -trend -fdhess"),
    "pce4_A": ("VECM_PCE", "GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -trend -weakex 2"),
    "pce4_B": ("VECM_PCE", "GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -trend -fixb2row 2 -1"),
    "pce4_C": ("VECM_PCE", "GY.pre PCEUSA.pre PCEEC.pre 2 0 1 -case pre -trend -fixb2row 2 -1 -weakex 2"),
    # WTI and G/Y, p = 2, case 2
    "wti_rank": ("VECM_WTI", "WTI.pre GY.pre 2 0 0 -case 2 -lrtest -bootstrap 499"),
    # fiscal (REV without the oil step | G), p = 2, drifts free
    "fisc_rank": ("VECM_FISC", "REVnoBCE.pre G.pre 2 0 0 -case pre -lrtest -bootstrap 499"),
    "fisc_free": ("VECM_FISC", "REVnoBCE.pre G.pre 2 0 1 -case pre -fdhess"),
    "fisc_b1": ("VECM_FISC", "REVnoBCE.pre G.pre 2 0 1 -case pre -fixb2 -1 -fdhess"),
    # balance of payments, p = 2, drifts free (debit | credit)
    "tb_rank": ("VECM_BOP", "M.pre X.pre 2 0 0 -case pre -lrtest -bootstrap 499"),
    "tb_free": ("VECM_BOP", "M.pre X.pre 2 0 1 -case pre -fdhess"),
    "tb_b1": ("VECM_BOP", "M.pre X.pre 2 0 1 -case pre -fixb2 -1 -fdhess"),
    "ca_rank": ("VECM_BOP", "CAd.pre CAc.pre 2 0 0 -case pre -lrtest -bootstrap 499"),
    "ca_free": ("VECM_BOP", "CAd.pre CAc.pre 2 0 1 -case pre -fdhess"),
    "ca_b1": ("VECM_BOP", "CAd.pre CAc.pre 2 0 1 -case pre -fixb2 -1 -fdhess"),
    "rt_rank": ("VECM_BOP", "Rd.pre Rc.pre 2 0 0 -case pre -lrtest -bootstrap 499"),
}

# tab:rank -- one block per system: (title, run, p, case label, rank adopted, note)
RANK = {
    "kind": "rank",
    "label": "tab:rank",
    "caption": "Cointegration rank",
    "rows": [
        ("Central: $(\\ln G_t/Y_t \\mid \\ln PE_t/PU_t)$", "biv_rank", 4, "2", 1),
        ("Augmented: $(\\ln G_t/Y_t \\mid BXE_t, \\ln PE_t/PU_t)$", "aug_rank", 4, "2", 2),
        ("Trivariate: $(\\ln G_t/Y_t, \\ln PU_t \\mid \\ln PE_t)$", "tri_rank", 2, "free", 1),
        ("Oil: $(\\ln WTI_t \\mid \\ln G_t/Y_t)$", "wti_rank", 2, "2", 0),
        ("Fiscal: $(re_t \\mid g_t)$", "fisc_rank", 2, "free", 1),
        ("Trade: $(i_t \\mid x_t)$", "tb_rank", 2, "free", 1),
        ("Current account: $(de_t \\mid cr_t)$", "ca_rank", 2, "free", 1),
        ("Rents and transfers: $(rd_t \\mid rc_t)$", "rt_rank", 2, "free", 0),
    ],
}

# tab:vecm -- the adopted models: (title, run, free run for the LR of the
# restriction or None, restriction label, half-life variable or None)
VECM = {
    "kind": "vecm",
    "label": "tab:vecm",
    "caption": "Adopted VARMA-VEC models: cointegrating vectors and adjustment",
    "shortrun": ("biv_wx",),
    "models": [
        (r"Bivariate $(G/Y\mid\text{GAP})$, $p=4$, Case~2, $\alpha_{G/Y}=0$ (adopted)", "biv_wx", "biv_free",
         r"$\alpha_{G/Y}=0$", "GAP"),
        (r"Bivariate, $\alpha$ free", "biv_free", None, None, "GAP"),
        ("Augmented, $p=4$, case 2, $r=2$", "aug_r2", None, None, None),
        (r"Trivariate $(G/Y, PU\mid PE)$, $p=2$, free drifts", "tri_r1", None, None, None),
        (r"Fiscal $(re\mid g)$, $p=2$, free drifts, $\beta=(1,-1)$ imposed", "fisc_b1", "fisc_free",
         r"$\beta=(1,-1)$", "G"),
        ("Trade, $p=2$, free drifts, $\\beta=(1,-1)$", "tb_b1", "tb_free",
         r"$\beta=(1,-1)$", "M"),
        ("Current account, $p=2$, free drifts, $\\beta=(1,-1)$", "ca_b1", "ca_free",
         r"$\beta=(1,-1)$", "CAd"),
    ],
}

# tab:validation -- trivariate tests against the unrestricted r = 1 model,
# three deterministic specifications
VALID = {
    "kind": "valid",
    "label": "tab:validation",
    "caption": "Trivariate system: tests of the reduction to the bivariate model",
    "cases": ["Case 3", "Free drifts", "Free drifts + trend"],
    # (title, run prefix per case or None, US price symbol)
    "panels": [
        (r"Panel A. Consumer price index, $(\ln G_t/Y_t, \ln PU_t \mid \ln PE_t)$",
         ["tri3", "tri", "tri4"], "PU"),
        (r"Panel B. Consumption deflator, $(\ln G_t/Y_t, \ln PCU_t \mid \ln PCE_t)$",
         [None, "pce", "pce4"], "PCU"),
    ],
    "tests": [
        ("A", r"$\alpha_{%s}=0$", "A", 1),
        ("B", r"$\beta_{%s}=-1$ (relative PPP)", "B", 1),
        ("C", "A and B jointly", "C", 2),
    ],
}

# Body: the systems that are central, justify a decision or can falsify the
# model (central, trivariate, oil, fiscal); appendix: the support
# systems (augmented with BXE, balance of payments).
_APP_RANK = ("aug_rank", "wti_rank", "tb_rank", "ca_rank", "rt_rank")
_APP_VECM = ("aug_r2", "tb_b1", "ca_b1")
RANK_APP = dict(RANK, label="tab:rank_app",
                caption="Cointegration rank of the other systems",
                rows=[r for r in RANK["rows"] if r[1] in _APP_RANK])
RANK = dict(RANK, rows=[r for r in RANK["rows"] if r[1] not in _APP_RANK])
VECM_APP = dict(VECM, label="tab:vecm_app",
                caption="Other VARMA-VEC models: cointegrating vectors and adjustment",
                models=[m for m in VECM["models"] if m[1] in _APP_VECM])
VECM = dict(VECM, models=[m for m in VECM["models"] if m[1] not in _APP_VECM])

TABLES = {"rank": RANK, "rank_app": RANK_APP, "vecm": VECM, "vecm_app": VECM_APP, "valid": VALID}
