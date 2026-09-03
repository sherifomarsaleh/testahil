"""The reverse read, as one construction every study can call.  [R-ENF-05]

WHAT IT SOLVES. Given a study's own committed free cash flows, its own terminal
value, its own terminal growth and its own bridge, this returns THE SINGLE FLAT
DISCOUNT RATE that reproduces a given equity price — and, on the identical
construction, the flat rate that reproduces the study's OWN enterprise value. The
two are the same quantity measured twice, so the disagreement between a study and
the market reads as one number rather than as a rate against a schedule.

WHY IT LIVES HERE AND NOT IN EACH STUDY. Written once per study it would be
written differently per study, and a diagnostic that is not comparable across
names cannot be pooled into the valuation calibration later. The five studies
already disagree on where they keep their cash flows; they must not also disagree
on what "the rate the price implies" means.

WHY THE TERMINAL FIGURES ARE RECOVERED RATHER THAN RE-DERIVED. The terminal cash
flow comes out of the study's own terminal value by the identity it was built
with, TV = FCFF_T / (WACC_T - g), and the date the terminal is brought home on
comes out of the study's own discount factors. Re-deriving either from drivers
would make this a second model rather than the same model read backwards, and the
whole claim of a reverse read is that it is the SAME model.

THE CONTAINMENT RULE. Nothing solved here may re-enter a valuation. A rate solved
from a price and then used is the reverse-engineered terminal the protocol
prohibits outright, arriving through a side door — which is why the result is
written to a study's diagnostics.json and assert_reverse_dcf() refuses any study
whose builders read that file back in.
"""
from __future__ import annotations

import math


def times_from_factors(df, fwd_wacc, tol=1e-6):
    """The cumulative discounting time of each explicit year, RECOVERED from the
    study's own factors rather than assumed.

    This is not fussiness. AMOC discounts each year to its year END and ARCC to a
    MID-PERIOD point from a valuation date half way through its first year; both
    are legitimate and [R-COC-01] lets a record declare its convention. Assuming
    either one here would put a real error into every reverse read silently —
    bringing a terminal home half a year later at 18% costs about 8% of its
    present value — and the error would look like a disagreement with the market
    rather than like a bug.

    Each year's own slice is solved from its own published forward rate, and the
    reconstruction is then checked against the published factors: a study whose
    factors do not reproduce from its own rates RAISES here rather than being
    read on a guess.
    """
    ts, cum_t, cum_df = [], 0.0, 1.0
    for x, r in zip(df, fwd_wacc):
        step = float(cum_df) / float(x)
        if step <= 0 or (1.0 + float(r)) <= 1.0:
            raise ValueError("a discount factor or forward rate is not usable")
        dt = math.log(step) / math.log(1.0 + float(r))
        cum_t += dt
        cum_df = float(x)
        ts.append(cum_t)
    # the check: the recovered times must reproduce the factors they came from
    chk, c = [], 1.0
    for t_prev, t, r in zip([0.0] + ts[:-1], ts, fwd_wacc):
        c *= (1.0 + float(r)) ** (t - t_prev)
        chk.append(1.0 / c)
    for a, b in zip(chk, df):
        if abs(a - float(b)) > tol * max(1.0, abs(float(b))):
            raise AssertionError(
                "the recovered discounting times do not reproduce the study's own "
                "factors (%.8f vs %.8f) — the convention is not what the rates say "
                "it is, and a reverse read on a guessed convention is a bug wearing "
                "the costume of a disagreement" % (a, float(b)))
    return ts


def resolve_times(coc_record, df, fwd_wacc):
    """The cumulative discounting times, DECLARED where a study declares them.

    [R-COC-01] as amended lets a record declare its discounting convention —
    the cumulative time of every explicit year and the slice of calendar each
    forward rate owns — and a record that declares nothing gets the end-of-year
    test. The same order applies here, and it is not interchangeable with the
    inversion below: ARCC's factors chain its forward rates over RATE EDGES at
    0, 0.5, 1.5 ... while discounting each year to its own MIDPOINT, so a
    per-year inversion recovers 1.03, 2.09, 3.13 where the study means 1, 2, 3.
    Reading a declared convention off the record is exact; inverting is a
    reconstruction, and a reconstruction is what you use when there is nothing
    to read.
    """
    conv = ((coc_record or {}).get("discounting_convention") or {})
    ts = conv.get("cumulative_years")
    if isinstance(ts, (list, tuple)) and len(ts) == len(df):
        return [float(t) for t in ts], "declared by the study"
    return times_from_factors(df, fwd_wacc), "recovered from the study's own factors"


def terminal_cash_flow(tv, wacc_terminal, g):
    """The cash flow the study itself capitalised, from its own terminal value."""
    return float(tv) * (float(wacc_terminal) - float(g))


def terminal_time(t_mid, df_last, df_tv, wacc_terminal):
    """The year the terminal is brought home on, read off the study's own factors.

    Studies differ on this and the difference is not cosmetic: bringing a terminal
    home half a year later at 18% costs about 8% of its present value. Assuming a
    convention here would put that error into every reverse read silently, so the
    convention is INFERRED from the two factors the study already published.
    """
    if not df_tv or not df_last:
        return float(t_mid[-1])
    ratio = float(df_last) / float(df_tv)
    if ratio <= 0:
        return float(t_mid[-1])
    return float(t_mid[-1]) + math.log(ratio) / math.log(1.0 + float(wacc_terminal))


def ev_at(r, fcff, t_mid, fcff_term, g, t_tv):
    """Enterprise value at one flat rate, on the study's own construction."""
    if r <= g:
        return float("inf")
    pv = sum(cf / (1.0 + r) ** t for cf, t in zip(fcff, t_mid))
    return pv + (fcff_term / (r - g)) / (1.0 + r) ** t_tv


def solve(target, fcff, t_mid, fcff_term, g, t_tv, hi=3.0):
    """The flat rate reproducing `target`.

    Bisection rather than a solver with a starting guess: above g the function is
    monotone decreasing in r, so the root is unique and the answer cannot depend
    on where the search began — which matters for a number whose whole purpose is
    to be compared across studies.
    """
    lo = float(g) + 1e-4
    for _ in range(400):
        mid = 0.5 * (lo + hi)
        if ev_at(mid, fcff, t_mid, fcff_term, g, t_tv) > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def read(fcff, t_mid, tv, wacc_terminal, g, df_last, df_tv, ev_study,
         equity_study, shares_mn, spot):
    """Both rates plus the arithmetic they stand on.

    `ev_study` and `equity_study` come from the study's own bridge, and their
    difference is what the price's equity value is carried back across — so the
    two rates are solved against the same bridge and differ only in the price
    they are asked to reproduce.
    """
    fcff_term = terminal_cash_flow(tv, wacc_terminal, g)
    t_tv = terminal_time(t_mid, df_last, df_tv, wacc_terminal)
    bridge_delta = float(equity_study) - float(ev_study)
    ev_spot = float(spot) * float(shares_mn) - bridge_delta
    return {
        "implied_rate_at_price": solve(ev_spot, fcff, t_mid, fcff_term, g, t_tv),
        "implied_rate_at_study_value": solve(float(ev_study), fcff, t_mid,
                                             fcff_term, g, t_tv),
        "terminal_cash_flow": fcff_term,
        "terminal_growth": float(g),
        "terminal_arrives_at_year": t_tv,
        "enterprise_value_at_spot": ev_spot,
        "enterprise_value_in_study": float(ev_study),
        "bridge_delta_equity_less_ev": bridge_delta,
    }
