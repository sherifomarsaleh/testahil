"""Named per-run adapters that put the archive's forward ladder into a run's escalator.

ONE ADAPTER PER RUN, NAMED, because the runs do not agree on a seam and a reader that
guesses a convention silently finds nothing and reports it as a result [L-355]. Nine
runs carry nine shapes: a cumulative-factor function, a tuple of multipliers, a field
on a fiscal-year record, a trailing-mean helper called eight times with eight different
closures, a per-leg escalator in a sibling module, and one run whose projector takes a
macro override as an argument and needs no patch at all.

WHAT IS SUBSTITUTED AND WHAT IS NOT. Only the INFLATION path moves. Every driver rule,
volume path, margin rule, tax regime, commodity convention and currency mechanism stays
exactly as the run pre-registered it — and where a run derives its currency from its own
CPI print by purchasing-power parity, the substitution flows through to the currency too,
because [R-MACRO-01] requires one path and a model escalating costs on one inflation and
its currency on another is the incoherence that rule exists to close.

EVERY PATCH ASSERTS THAT IT LANDED. A substitution that silently fails to bind returns
the run's own answer under a new label, which is the absent answer wearing a clean one's
clothes [R-ENF-04] and is the single most likely way this whole exercise produces a
number that means nothing. This repository has caught a fixture that never injected its
condition five times; so `apply()` re-reads the quantity it patched and raises unless it
changed, and the caller additionally requires the PROJECTION to move wherever the
substituted rate differs from the run's own.

A RUN WITH NO SEAM IS DROPPED WITH ITS REASON, NEVER GUESSED AT.
"""
from __future__ import annotations

import contextlib


class PatchDidNotLand(RuntimeError):
    """The substitution was applied and the quantity did not move."""


def _assert_moved(what, before, after, rate):
    if before == after:
        raise PatchDidNotLand(
            "%s reads %r before and after the substitution to %.6f — the patch did not "
            "land, and a projection built on the run's own path under this label would "
            "be a fabricated cell" % (what, before, rate))


# ------------------------------------------------------------------ the adapters
@contextlib.contextmanager
def amoc(B, origin_label, h, rate, cum):
    """AMOC escalates through `cpi_path(origin, h, foresight)`, which RETURNS the
    cumulative factor — the cleanest seam in the book, so the ladder's own compounded
    factor is handed straight back."""
    old = B.cpi_path
    probe_before = old(origin_label, h, False)

    def patched(o, hh, foresight=False):
        if foresight:
            return old(o, hh, True)
        return cum if hh == h else (1.0 + rate) ** hh
    B.cpi_path = patched
    try:
        _assert_moved("AMOC cpi_path(%s,%d)" % (origin_label, h),
                      probe_before, patched(origin_label, h), rate)
        yield
    finally:
        B.cpi_path = old


@contextlib.contextmanager
def arcc(B, origin_label, h, rate, cum):
    """ARCC returns a TUPLE of multipliers from `_paths`; only the first is inflation.
    The currency and coal legs are left exactly as pre-registered."""
    old = B._paths
    probe_before = old(origin_label, h, False, False)

    def patched(o, hh, foresight, cpi_only):
        pi, fxm, coal = old(o, hh, foresight, cpi_only)
        if foresight:
            return pi, fxm, coal
        return (cum if hh == h else (1.0 + rate) ** hh), fxm, coal
    B._paths = patched
    try:
        _assert_moved("ARCC _paths(%s,%d)[0]" % (origin_label, h),
                      probe_before[0], patched(origin_label, h, False, False)[0], rate)
        yield
    finally:
        B._paths = old


@contextlib.contextmanager
def egch(B, origin_label, h, rate, cum):
    """EGCH reads ONE FIELD for both its domestic cost escalator and the
    purchasing-power wedge that drives its currency, so the field is what moves and the
    currency follows — which is the coherence [R-MACRO-01 AMENDED] found missing on this
    exact study."""
    rec = B.FY[origin_label]
    key = "cpi_eg_pct_last_published"
    old = rec[key]
    rec[key] = 100.0 * rate
    try:
        _assert_moved("EGCH FY[%s][%s]" % (origin_label, key), old, rec[key], rate)
        yield
    finally:
        rec[key] = old


@contextlib.contextmanager
def phdc(B, origin_label, h, rate, cum):
    """PHDC takes a trailing three-year mean of its own panel's CPI through the View's
    `ttm`, which serves several other fields — so the interception is BY FIELD NAME and
    nothing else is touched."""
    old = B.View.ttm

    def patched(self, field, n=3, transform=None):
        if field == "macro.cpi_pct":
            return 100.0 * rate
        return old(self, field, n, transform)
    B.View.ttm = patched
    try:
        yield
    finally:
        B.View.ttm = old


@contextlib.contextmanager
def tmgh(B, origin_label, h, rate, cum, cpi_dict=None):
    """TMGH calls one helper EIGHT times with eight different closures and the inflation
    call is the one whose closure holds the cpi mapping — so the interception is on
    CLOSURE IDENTITY, which is exact, rather than on argument shape, which would sweep in
    the seven conversion, cost, depreciation and collection ratios beside it."""
    old = B.ttm

    def patched(A, field, o, n=3, fn=None):
        if (field is None and fn is not None and cpi_dict is not None
                and getattr(fn, "__closure__", None)
                and any(c.cell_contents is cpi_dict for c in fn.__closure__)):
            return rate
        return old(A, field, o, n, fn)
    B.ttm = patched
    try:
        yield
    finally:
        B.ttm = old


@contextlib.contextmanager
def phar(B, origin_label, h, rate, cum):
    """PHAR's escalator lives in a SIBLING module and is keyed by leg — the knowable leg
    is the one this exercise runs, and the foresight leg is left alone so the run's own
    macro split still measures what it measured."""
    M = B.macro
    old = M.cpi_leg

    def patched(leg, origin_year, forecast_year):
        if leg == "knowable":
            return rate
        return old(leg, origin_year, forecast_year)
    M.cpi_leg = patched
    try:
        _assert_moved("PHAR macro.cpi_leg('knowable',%s)" % (origin_label,),
                      old("knowable", origin_label, origin_label + h),
                      patched("knowable", origin_label, origin_label + h), rate)
        yield
    finally:
        M.cpi_leg = old


@contextlib.contextmanager
def swdy(B, origin_label, h, rate, cum):
    """SWDY builds its multipliers in `paths(o)` and compounds them in `project`; the
    metal leg is held flat in dollars and converted, so it moves with the currency and
    NOT with this substitution, exactly as pre-registered."""
    old = B.paths
    probe_before = old(origin_label)

    def patched(o):
        p = dict(old(o))
        p["cpi"] = rate
        return p
    B.paths = patched
    try:
        _assert_moved("SWDY paths(%s)['cpi']" % (origin_label,),
                      probe_before["cpi"], patched(origin_label)["cpi"], rate)
        yield
    finally:
        B.paths = old


@contextlib.contextmanager
def none_needed(B, origin_label, h, rate, cum):
    """GBCO carries NO INFLATION TERM ANYWHERE — its own macro-split module says so in
    those words, and its zero macro share is that model's own published check. There is
    nothing to substitute, and inventing a term so the name joins the population would
    be the fabricated driver [R-FCAL-01] refuses. The cell is built on the run's own
    projection and the CONSEQUENCE is reported rather than hidden: a real-terms growth
    path cannot converge to a nominal terminal, so this name is expected to refuse on
    the bound and that refusal is a true statement about the model."""
    yield


ADAPTERS = {
    "AMOC": amoc,
    "ARCC": arcc,
    "EGCH": egch,
    "PHDC": phdc,
    "TMGH": tmgh,
    "PHAR": phar,
    "SWDY": swdy,
    "GBCO": none_needed,
    # SCEM takes a macro override as an ARGUMENT to its own projector and is handled
    # there — a run that already offers the hook is not patched, and that is the shape
    # every other run would have if anyone had known to ask for it.
}
