"""Where the figure scripts read the engine outputs and write the figures.

The outputs come from build/ (`make multivariate`, `make analyses`); with the
environment variable SUITE set to revision-suite/Python/art_drvec they fall back
to the original outputs of the analysis (see tables/make_robustness.py).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "tables"))
import make_robustness as _mr       # noqa: E402

_mr.SUITE = os.environ.get("SUITE")
SUITE = _mr.SUITE
FIG = os.path.join(REPO, "output", "figures")
os.makedirs(FIG, exist_ok=True)


def src(key: str, ext: str = ".out") -> str:
    return _mr.out_path(key, ext)
