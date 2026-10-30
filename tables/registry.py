"""Which model is behind each row of the paper's tables.

Every row names the `.inp` of its adopted model. `make_tables.py` estimates
the `.inp` with art (fue, exact ML, Hessian at the optimum) and checks the
optimum against the adopted `.pre`. The `.pre` is never the source.
The paper's tables use deterministic seasonality throughout (analyst,
2026-10-10); where a series also has a stochastic-seasonality model (HSM),
`addon` names it: it is estimated and listed in the comparison report, and
belongs to the online addendum. `paper` holds the values printed in the
current draft, for the comparison report; it is not used to build the table.
"""

# paper keys: phi1, phi2, d, mean, sf, q, jb, sigma, dcd (None = "--")
# d_rule="PE": d kept by SF although the DCD asks d + 1 outside the band,
# because a permanent step or a drift change resonates at f = 0 (guion).

UNI2 = {
    "label": "tab:uni2",
    "caption": "Estimated univariate models for Output, the Balance of "
               "Payments and the Public Sector",
    "groups": [
        ("Univariate Models for Output", [
            dict(name="Real", mnem=r"\Delta y_t", inp="MACRO/YR/YR_m01_ar2.inp",
                 addon="MACRO/YR/YR_m05_ar1.inp",
                 paper=dict(phi1=0.02, phi2=0.28, d=1, mean=0.87, sf=12.4,
                            q=15.68, jb=1.90, sigma=1.37, dcd=0.0)),
            dict(name="Nominal", mnem=r"\Delta z_t", inp="MACRO/YN/YN_m04_ar1_sar1.inp",
                 addon="MACRO/YN/YN_m05_meg2.inp",
                 paper=dict(phi1=0.17, phi2=0.22, d=1, mean=1.82, sf=11.9,
                            q=17.09, jb=2.57, sigma=2.54, dcd=0.0)),
        ]),
        ("Univariate Models for the Balance of Trade", [
            dict(name="Exports", mnem=r"\Delta x_t", inp="EXT/X/X_m03_ar1_noseas.inp", d_rule="PE",
                 paper=dict(phi1=0.29, phi2=None, d=1, mean=1.86, sf=26.4,
                            q=11.37, jb=1.43, sigma=7.5, dcd=None)),
            dict(name="Imports", mnem=r"\Delta i_t", inp="EXT/M/M_m03a_ar2.inp",
                 paper=dict(phi1=0.42, phi2=None, d=1, mean=1.54, sf=19.8,
                            q=17.89, jb=1.46, sigma=5.05, dcd=None)),
            dict(name="Balance", mnem=r"tr_t = x_t - i_t",
                 inp="EXT/BXE/BXE_m05_i0804x2.inp",
                 paper=dict(phi1=0.80, phi2=-0.42, d=0, mean=-4.07, sf=None,
                            q=12.03, jb=0.32, sigma=6.75, dcd=0.0)),
        ]),
        ("Univariate Models for the Current Account", [
            dict(name="Credit", mnem=r"\Delta cr_t", inp="EXT/CAc/CAc_m03_ar1_noseas.inp", d_rule="PE",
                 paper=dict(phi1=0.19, phi2=None, d=1, mean=1.79, sf=31.9,
                            q=5.54, jb=0.35, sigma=7.0, dcd=None)),
            dict(name="Debit", mnem=r"\Delta de_t", inp="EXT/CAd/CAd_m04_ar1x1.inp",
                 paper=dict(phi1=0.27, phi2=None, d=1, mean=1.57, sf=27.2,
                            q=14.58, jb=4.57, sigma=5.75, dcd=None)),
            dict(name="Current-account ratio", mnem=r"SE_t = cr_t - de_t",
                 inp="EXT/SE/SE_m03_i0804x2.inp",
                 paper=dict(phi1=0.72, phi2=-0.26, d=0, mean=None, sf=None,
                            q=8.9, jb=0.67, sigma=6.82, dcd=0.0)),
        ]),
        ("Univariate Models for Rents and Transfers", [
            dict(name="Credit", mnem=r"\Delta rc_t", inp="EXT/Rc/Rc_m00.inp", d_rule="PE"),
            dict(name="Debit", mnem=r"\Delta rd_t", inp="EXT/Rd/Rd_m01_ar1.inp"),
            dict(name="Net", mnem=r"\Delta it_t",
                 inp="EXT/IT/IT_m00.inp"),
        ]),
        ("Univariate Models for the Public Sector Accounts", [
            dict(name="Expenditure", mnem=r"\Delta g_t", inp="MACRO/G/G_m02_ar1.inp",
                 paper=dict(phi1=-0.20, phi2=None, d=1, mean=2.83, sf=20.8,
                            q=10.4, jb=1.34, sigma=8.95, dcd=0.3)),
            dict(name="Revenue", mnem=r"\Delta re_t", inp="MACRO/REV_BCE/REVbce_g04_ar1.inp", d_rule="PE",
                 paper=dict(phi1=-0.30, phi2=None, d=1, mean=2.62, sf=64.7,
                            q=14.78, jb=1.61, sigma=8.41, dcd=0.0)),
            dict(name="Deficit", mnem=r"\tau_t = g_t - re_t",
                 inp="MACRO/TAU_BCE/TAUbce_g02_ar2_s0804x3.inp", d_rule="PE",
                 paper=dict(phi1=0.39, phi2=0.37, d=0, mean=1.83, sf=2.8,
                            q=14.02, jb=1.42, sigma=7.92, dcd=0.0)),
        ]),
        ("Univariate Model for Government Expenditure, percentage of Output", [
            dict(name=r"$\Delta\gamma_t$", mnem=r"\Delta(g_t - z_t)",
                 inp="GY_pasada2/GY_m03a_step0802.inp",
                 pre="VECM_GAP_GY/GY_M1.pre",
                 paper=dict(phi1=-0.37, phi2=None, d=1, mean=0.93, sf=31.12,
                            q=3.89, jb=1.04, sigma=7.40, dcd=0.5)),
        ]),
    ],
}

UNI = {
    "label": "tab:uni",
    "caption": "Estimated univariate price models",
    "groups": [
        ("Univariate Models for CPI Prices", [
            dict(name="Ecuador", mnem=r"\Delta pe_t", inp="PE/PE_m03_ar1.inp", d_rule="PE",
                 paper=dict(phi1=0.60, phi2=None, d=1, mean=0.75, sf=12.0,
                            q=20.16, jb=5.79, sigma=0.54)),
            dict(name="USA", mnem=r"\Delta pu_t", inp="PU/PU_m08_ar1_noalt.inp",
                 paper=dict(phi1=0.39, phi2=None, d=1, mean=0.50, sf=19.7,
                            q=17.07, jb=1.00, sigma=0.38)),
        ]),
        ("Univariate Models for the GDP Deflator", [
            dict(name="Ecuador", mnem=r"\Delta pge_t",
                 inp="DEFL/GDPDEC_G/GDPDEC_m04_x2_ar2.inp", d_rule="PE",
                 paper=dict(phi1=None, phi2=None, d=1, mean=0.98, sf=None,
                            q=19.3, jb=0.06, sigma=2.1)),
            dict(name="USA", mnem=r"\Delta pgu_t", inp="DEFL/GDPDUSA/GDPDUSA_m01_ar1.inp",
                 paper=dict(phi1=0.49, phi2=None, d=1, mean=0.47, sf=17.4,
                            q=11.03, jb=0.24, sigma=0.21)),
        ]),
        ("Univariate Models for the PCE Deflator", [
            dict(name="Ecuador", mnem=r"\Delta pce_t", inp="DEFL/PCEEC/PCEEC_m01_ar1.inp",
                 paper=dict(phi1=0.51, phi2=None, d=1, mean=0.98, sf=15.4,
                            q=19.4, jb=0.14, sigma=1.15)),
            dict(name="USA", mnem=r"\Delta pcu_t", inp="DEFL/PCEUSA/PCEUSA_m02_ar3.inp",
                 paper=dict(phi1=0.44, phi2=None, d=1, mean=0.44, sf=18.4,
                            q=14.47, jb=0.10, sigma=0.30)),
        ]),
        ("Univariate Models for Relative Prices", [
            dict(name="$PE/PU$", mnem=r"\Delta(pe_t - pu_t)",
                 inp="GAP/GAP_m04_ar3_noalt.inp",
                 paper=dict(phi1=0.49, phi2=None, d=1, mean=0.25, sf=16.0,
                            q=13.11, jb=3.01, sigma=0.71)),
            dict(name="$PGE/PGU$", mnem=r"\Delta(pge_t - pgu_t)",
                 inp="DEFL/GAPGDPD_G/GAPGDPD_m03_x2_ar2.inp",
                 paper=dict(phi1=None, phi2=None, d=1, mean=0.50, sf=None,
                            q=19.31, jb=0.22, sigma=2.0)),
            dict(name="$PCE/PCU$", mnem=r"\Delta(pce_t - pcu_t)",
                 inp="DEFL/GAPPCE/GAPPCE_m02_ar1_s0804.inp",
                 paper=dict(phi1=0.40, phi2=None, d=1, mean=0.54, sf=19.9,
                            q=13.54, jb=3.40, sigma=1.22)),
        ]),
    ],
}

# tab:ur replaces the draft's ADF/KPSS table (seasonally adjusted series,
# KPSS statistics off by two orders of magnitude, PCE levels listed as I(0)).
# Rows: the series that enter the multivariate analysis.
UR = {
    "kind": "ur",
    "label": "tab:ur",
    "caption": "Order of integration at $f=0$: identification and formal tests "
               "(2003Q1--2019Q4)",
    "groups": [
        ("Panel A. The central system", [
            dict(name=r"$\ln(G_t/Y_t)$", mnem="gy", inp="GY_pasada2/GY_m03a_step0802.inp",
                 pre="VECM_GAP_GY/GY_M1.pre"),
            dict(name=r"$\ln(PE_t/PU_t)$", mnem="gap", inp="GAP/GAP_m04_ar3_noalt.inp"),
            dict(name=r"$\ln PE_t$", mnem="pe", inp="PE/PE_m03_ar1.inp", d_rule="PE"),
            dict(name=r"$\ln PU_t$", mnem="pu", inp="PU/PU_m08_ar1_noalt.inp"),
        ]),
        ("Panel B. External sector, oil and robustness", [
            dict(name=r"$\ln BXE_t = x_t - i_t$", mnem="bxe", inp="EXT/BXE/BXE_m05_i0804x2.inp"),
            dict(name=r"$\ln SE_t = cr_t - de_t$", mnem="se", inp="EXT/SE/SE_m03_i0804x2.inp"),
            dict(name=r"$\ln IT_t = rc_t - rd_t$", mnem="it", inp="EXT/IT/IT_m00.inp"),
            dict(name=r"$\ln WTI_t$", mnem="wti", inp="WTI_m01_i0804.inp"),
            dict(name=r"$\ln(PGE_t/PGU_t)$", mnem="gapgdpd",
                 inp="DEFL/GAPGDPD_G/GAPGDPD_m03_x2_ar2.inp"),
            dict(name=r"$\ln(PCE_t/PCU_t)$", mnem="gappce",
                 inp="DEFL/GAPPCE/GAPPCE_m02_ar1_s0804.inp"),
        ]),
        ("Panel C. Fiscal and balance-of-payments systems", [
            dict(name=r"$g_t$", mnem="g", inp="MACRO/G/G_m02_ar1.inp"),
            dict(name=r"$re_t$", mnem="re", inp="MACRO/REV_BCE/REVbce_g04_ar1.inp", d_rule="PE"),
            dict(name=r"$\tau_t = g_t - re_t$", mnem="tau", inp="MACRO/TAU_BCE/TAUbce_g02_ar2_s0804x3.inp",
                 d_rule="PE"),
            dict(name=r"$x_t$", mnem="x", inp="EXT/X/X_m03_ar1_noseas.inp", d_rule="PE"),
            dict(name=r"$i_t$", mnem="m", inp="EXT/M/M_m03a_ar2.inp"),
            dict(name=r"$cr_t$", mnem="cac", inp="EXT/CAc/CAc_m03_ar1_noseas.inp", d_rule="PE"),
            dict(name=r"$de_t$", mnem="cad", inp="EXT/CAd/CAd_m04_ar1x1.inp"),
            dict(name=r"$rc_t$", mnem="rc", inp="EXT/Rc/Rc_m00.inp", d_rule="PE"),
            dict(name=r"$rd_t$", mnem="rd", inp="EXT/Rd/Rd_m01_ar1.inp"),
        ]),
    ],
}

# The paper's body carries the central system (Panel A, the I(1) premise of the
# cointegration); the appendix carries the other series (Panels B and C).
UR_APP = dict(UR, label="tab:ur_app",
              caption="Order of integration at $f=0$ (continued): other series, 2003Q1--2019Q4",
              groups=[g for g in UR["groups"] if not g[0].startswith("Panel A")])
UR = dict(UR, caption="Order of integration at $f=0$: the central system, 2003Q1--2019Q4",
          groups=[g for g in UR["groups"] if g[0].startswith("Panel A")])


def _row(inp: str, label: str) -> dict:
    """A row of UNI or UNI2, by its model, with the label of the ITV table."""
    for spec in (UNI, UNI2):
        for _, rows in spec["groups"]:
            for r in rows:
                if r["inp"] == inp:
                    return dict(r, label=label)
    raise KeyError(inp)


# The interventions of the univariate models and the signs of the innovations
# around them, in the format of Dobado-Gonzalez, Garcia-Hiernaux and Guerrero
# (JEH 2012, Tables 1A-1B). Every intervention falls in 2008Q1-2009Q3.
ITV = {
    "kind": "itv",
    "label": "tab:itv",
    "caption": "Interventions in the univariate models, 2008--2009",
    "quarters": ["2008Q1", "2008Q2", "2008Q3", "2008Q4", "2009Q1", "2009Q2", "2009Q3"],
    "events": [(r"\begin{tabular}[b]{@{}c@{}}Fuel subsidy\\recorded gross\end{tabular}", 1),
               (r"\begin{tabular}[b]{@{}c@{}}Commodity\\price peak\end{tabular}", 2),
               (r"\begin{tabular}[b]{@{}c@{}}Oil price collapse,\\global financial crisis\end{tabular}", 2),
               (r"\begin{tabular}[b]{@{}c@{}}Oil price\\recovery\end{tabular}", 2)],
    "groups": [
        ("Panel A. Oil and prices", [
            dict(name="WTI", mnem=r"\Delta wti_t", inp="WTI_m01_i0804.inp",
                 pre="VECM_WTI/WTI.pre", label="Oil price (WTI)"),
            _row("PE/PE_m03_ar1.inp", "CPI, Ecuador ($PE$)"),
            _row("PU/PU_m08_ar1_noalt.inp", "CPI, US ($PU$)"),
            _row("GAP/GAP_m04_ar3_noalt.inp", "Price gap ($PE/PU$)"),
            _row("DEFL/PCEEC/PCEEC_m01_ar1.inp", "Consumption deflator, Ecuador"),
            _row("DEFL/PCEUSA/PCEUSA_m02_ar3.inp", "Consumption deflator, US"),
            _row("DEFL/GAPPCE/GAPPCE_m02_ar1_s0804.inp", "Consumption-deflator gap"),
            _row("DEFL/GDPDEC_G/GDPDEC_m04_x2_ar2.inp", "GDP deflator, Ecuador"),
            _row("DEFL/GDPDUSA/GDPDUSA_m01_ar1.inp", "GDP deflator, US"),
            _row("DEFL/GAPGDPD_G/GAPGDPD_m03_x2_ar2.inp", "GDP-deflator gap"),
        ]),
        ("Panel B. Balance of payments", [
            _row("EXT/X/X_m03_ar1_noseas.inp", "Exports"),
            _row("EXT/M/M_m03a_ar2.inp", "Imports"),
            _row("EXT/BXE/BXE_m05_i0804x2.inp", "Trade balance (BXE)"),
            _row("EXT/CAc/CAc_m03_ar1_noseas.inp", "Current-account credit"),
            _row("EXT/CAd/CAd_m04_ar1x1.inp", "Current-account debit"),
            _row("EXT/SE/SE_m03_i0804x2.inp", "Current-account ratio (SE)"),
            _row("EXT/IT/IT_m00.inp", "Remittance balance (IT)"),
        ]),
        ("Panel C. Output and public sector", [
            _row("MACRO/YR/YR_m01_ar2.inp", "Real GDP"),
            _row("MACRO/YN/YN_m04_ar1_sar1.inp", "Nominal GDP"),
            _row("MACRO/G/G_m02_ar1.inp", "Expenditure ($G$)"),
            _row("MACRO/REV_BCE/REVbce_g04_ar1.inp", "Revenue"),
            _row("MACRO/TAU_BCE/TAUbce_g02_ar2_s0804x3.inp", "Deficit"),
            _row("GY_pasada2/GY_m03a_step0802.inp", "Expenditure ratio ($G/Y$)"),
        ]),
    ],
    "notes": r"S, I: step, impulse, with its effect on the level in that quarter "
             r"(100$\times$log). Elsewhere, the standardized innovation: $+\,+$, $-\,-$ beyond "
             r"two standard deviations; $+$, $-$ between one and two. Models in Tables~"
             r"\ref{tab:uni} and~\ref{tab:uni2}; WTI, Section~\ref{sec:wti}.",
}

TABLES = {"uni": UNI, "uni2": UNI2, "ur": UR, "ur_app": UR_APP, "itv": ITV}
