# Replication of "Inflation in a dollarized economy: the role of fiscal policy".
# Requires the ATSW suite from PyPI:  pip install -r requirements.txt
#
#   make data         data/*.csv from the downloaded sources in data/raw (with checks)
#   make univariate   tab:uni, tab:uni2, tab:ur, tab:ur_app, tab:itv  (art; about two minutes)
#   make multivariate tab:rank(_app), tab:vecm(_app), tab:validation (drvec; the rank
#                     bootstraps take about two hours with the compiled engine)
#   make analyses     every other drvec / drtran run the paper cites
#   make robustness   tab:ripc, tab:tf, tab:prices, tab:sensitivity, and the Online
#                     Supplement's tab:subsample, tab:irf_transitory and Johansen
#                     tables (make_johansen.py, from data/); needs `analyses`
#   make figures      IRF / FEVD figures (needs the -irfboot runs of `analyses`)
#   make docs         the model catalogue (docs/), from the guiones and the fits
#   make verify       compare output/ with expected/
#   make all          everything above, in order

PY     ?= python3
JOBS   ?= 4

.PHONY: all data univariate multivariate analyses robustness figures docs verify clean

all: data univariate multivariate analyses robustness figures docs verify

data:
	$(PY) data/build_data.py

univariate:
	$(PY) tables/make_tables.py uni uni2 ur ur_app itv

multivariate:
	$(PY) tables/make_tables.py rank rank_app vecm vecm_app valid --jobs $(JOBS)

analyses:
	$(PY) tools/run_analyses.py --jobs $(JOBS)

robustness:
	$(PY) tables/make_robustness.py
	$(PY) tables/make_johansen.py

figures:
	$(PY) figures/plot_theory.py
	$(PY) figures/plot_gap_gy.py
	$(PY) figures/plot_convergence.py
	$(PY) figures/plot_irf_fevd_suite.py
	$(PY) figures/plot_irf_transitory.py
	# Fig. 7 needs the C drvec output (SUITE=...); see the TODO of drvec-python
	-$(PY) figures/plot_irf_wti.py

docs:
	$(PY) tables/make_docs.py

verify:
	$(PY) tools/verify.py

clean:
	rm -rf build output
