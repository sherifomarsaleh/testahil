"""Point-in-time own-stock betas, and the market-class prior they shrink toward.

LEVER 5 of the six the pre-registration fixed in order before any score existed.
The declared run carries BETA = 1.00 for every name at every origin, which is the
FULL-SHRINKAGE limit of a Vasicek estimator: a prior of 1.00 with no weight on the
name's own history at all. This module supplies the other end of that dial.

TWO THINGS ARE DELIBERATE.

(1) THE REGRESSION IS THE SANCTIONED ONE. beta_regression.own_stock_beta() resolves
    the exchange's published index itself, runs the data-quality gate on both series,
    matches the real trading week and applies the usability gate -- and it is called
    with an `asof` so the window ends at the origin. Every study in this repository
    once hand-rolled its own beta script and every one regressed against an
    equal-weight composite of the covered names, which on one name understated beta
    by about 40%. A calibration is not exempt from the rule that produced.

(2) THE SHRINKAGE WEIGHT IS DERIVED, NOT CHOSEN. Vasicek weights the name's own
    estimate by w = s2_prior / (s2_prior + se^2), where s2_prior is the CROSS-SECTIONAL
    dispersion of betas in the market class. That dispersion is MEASURED at each
    origin from the same point-in-time regressions on every name the market's library
    holds -- so a noisy beta is pulled hard toward the prior and a precise one is
    barely moved, and nothing about the strength of the pull was typed. A tuned
    shrinkage constant would be the free parameter the promotion rule forbids.

POINT-IN-TIME IS THE WHOLE CLAIM. A beta struck on today's window and applied at a
2016 origin is fabricated in vintage -- plausible on the page and invisible in the
pooled error afterwards, which is the exact failure the share-count clause of
[R-FCAL-01 AMENDED] names. Both series are truncated before the window is measured.
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, ENGINE)

import beta_regression as BR   # noqa: E402

PRIOR = 1.00          # the declared run's own beta: the prior is what it already uses
EXCHANGE = {"EG": "EGX"}
_CACHE: dict = {}


def _one(ticker, market, asof):
    key = (ticker, market, asof)
    if key not in _CACHE:
        try:
            _CACHE[key] = BR.own_stock_beta(ticker, market, EXCHANGE[market], asof=asof)
        except Exception as exc:
            _CACHE[key] = {"error": "%s: %s" % (type(exc).__name__, str(exc)[:90])}
    return _CACHE[key]


def _universe(market):
    d = os.path.join(ENGINE, "raw_ohlc", market)
    return sorted(f[:-4] for f in os.listdir(d) if f.endswith(".csv"))


def prior_dispersion(market, asof):
    """Cross-sectional SD of the market's USABLE point-in-time betas at this date.

    Only betas that pass the module's own usability gate enter the dispersion: an
    unusable estimate is not evidence about how far betas spread, and letting one in
    would widen the prior and so weaken the shrinkage of every other name -- a defect
    that would look like a result.
    """
    bs = []
    for tk in _universe(market):
        r = _one(tk, market, asof)
        if r.get("error") or not r.get("usable"):
            continue
        bs.append(r["beta"])
    if len(bs) < 5:
        return None, len(bs)
    m = sum(bs) / len(bs)
    return (sum((b - m) ** 2 for b in bs) / (len(bs) - 1)) ** 0.5, len(bs)


def shrunk(ticker, market, origin):
    """The Vasicek-shrunk point-in-time beta, with everything it rests on.

    Returns (beta, record). A name whose own regression is unusable at this origin
    falls to the PRIOR and says so -- which is the declared run's own value, so an
    unusable cell contributes nothing to the lever rather than silently contributing
    a bad number [R-ENF-04].
    """
    asof = "%d-12-31" % origin
    r = _one(ticker, market, asof)
    if r.get("error"):
        return PRIOR, {"beta": PRIOR, "why": "no point-in-time regression: %s" % r["error"]}
    if not r.get("usable"):
        return PRIOR, {"beta": PRIOR, "raw": r["beta"], "n": r["n"], "r2": r["r2"],
                       "why": "the regression fails its own usability gate: %s"
                              % r.get("gate_msg")}
    sd, n_names = prior_dispersion(market, asof)
    if sd is None:
        return PRIOR, {"beta": PRIOR, "raw": r["beta"],
                       "why": "only %d usable betas in the market at this origin — too "
                              "few to measure a prior dispersion" % n_names}
    w = sd ** 2 / (sd ** 2 + r["se"] ** 2)
    b = w * r["beta"] + (1 - w) * PRIOR
    return b, {"beta": b, "raw": r["beta"], "se": r["se"], "n": r["n"], "r2": r["r2"],
               "weight": w, "prior": PRIOR, "prior_sd": sd, "prior_names": n_names,
               "asof": asof, "index_file": r["index_file"], "conforming": r["conforming"],
               "window_years": r["window_years"]}


if __name__ == "__main__":
    for tk in ("ARCC", "EGCH", "PHDC", "TMGH", "AMOC"):
        for o in (2016, 2019, 2022, 2023):
            b, rec = shrunk(tk, "EG", o)
            if "raw" in rec and "weight" in rec:
                print("  %-5s %d  raw %.4f  se %.4f  w %.3f  -> %.4f   (prior sd %.3f "
                      "on %d names, n=%d)"
                      % (tk, o, rec["raw"], rec["se"], rec["weight"], b,
                         rec["prior_sd"], rec["prior_names"], rec["n"]))
            else:
                print("  %-5s %d  -> %.4f   %s" % (tk, o, b, rec["why"][:70]))
