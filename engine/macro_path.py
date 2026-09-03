"""ONE HOUSE MACRO PATH PER MARKET  [R-MACRO-01]

Every study in this repository set its own inflation. Five studies carried five
different rates for the same fiscal year in the same country (25.2%, 14.5%,
11.5%, 10.0%, and one with none at all), three different sovereign quotes, and
terminal inflations of 5%, 7% and about 15%. Nothing was wrong with any one of
them in isolation; what was wrong is that a company cannot be valued in an
economy the study next door does not recognise, and the differences moved fair
values by more than most of the driver work did.

Worse, the incoherence is DIRECTIONAL. Escalating costs at domestic inflation
while holding the currency or the selling price still is the same event counted
once and ignored once: it inflates every cost, freezes every price, and
manufactures a margin decline the forecast then reports as a finding [L-048].
PHDC's terminal growth of 12% against roughly 14.6% of inflation inside its own
terminal discount rate is a perpetual real decline nobody wrote down [L-055].
Both lessons were registered and bound nothing. This module is what makes them
bind.

WHAT THIS MODULE IS
    One dated, sourced path per market: an inflation ladder from the central
    bank's own published forecasts to a terminal, the policy-rate glide, the
    sovereign quote, the currency, the long-run cost-of-debt norm, the real-rate
    convention and the terminal equity risk premium. A study imports it and may
    not carry an inflation number of its own.

WHAT IT IS NOT
    It is not a forecast this house invents. Every level is either published by
    a named institution on a named date, or DERIVED here by an identity from
    numbers that are. The one class of number in between — a year between two
    published endpoints — is labelled "interpolated between published endpoints"
    in the file itself and is never described as anyone's forecast.

THE IDENTITIES, so that nothing downstream re-derives them differently:
    fx[t]/fx[t-1] - 1  =  (1+infl_local[t]) / (1+infl_foreign) - 1     (relative PPP)
    terminal rf        =  terminal inflation + the real-rate convention
    terminal g         =  terminal inflation + a STATED real growth (default 0)

A MARKET WITH NO SOURCED PATH RAISES. It does not fall back to a neighbour, a
region or a global average — the same stop-and-inform discipline the index
resolver already applies (`wacc_builder.market_index_path` refuses market AE
because it spans two exchanges). An empty answer is not a clean answer
[R-ENF-04].

    python3 engine/macro_path.py            # what is held, and how old
    python3 engine/macro_path.py EG         # one market in full
"""
from __future__ import annotations

import datetime as _dt
import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
PATHS = os.path.join(HERE, "macro_paths")

# The markets this repository covers. A file must exist for each; a file that
# carries no sourced path declares itself pending and every accessor RAISES.
MARKETS = ("EG", "AE", "SA", "QA", "IN", "KR", "US")

# A market is in TRANSITION when its policy rate sits materially above its own
# long-run level and the central bank publishes a disinflation path — there the
# cost-of-capital glide applies. A PEGGED market is already at its terminal by
# construction of the peg, the glide collapses to flat, and applying it produces
# nothing but complexity (measured at +0.0% on EAND).
REGIMES = ("transition", "pegged", "mature")

# How stale a sovereign quote may be before a build must re-source it. Not a
# free parameter: it is the interval over which an EGP sovereign quote has
# historically moved by more than the precision the cost of capital is stated
# to. Stated here once so that WS1's gate and any study read the same number.
SOVEREIGN_STALE_DAYS = 14


class MacroPathError(RuntimeError):
    """A macro path was asked for and cannot honestly be given."""


@dataclass(frozen=True)
class MacroPath:
    market: str
    currency: str
    as_of: str
    regime: str
    raw: dict = field(repr=False)

    # ---- inflation ---------------------------------------------------------
    @property
    def inflation_latest(self) -> float:
        return self.raw["inflation"]["latest"]["value"]

    @property
    def inflation_path(self) -> List[float]:
        """The annual inflation ladder, in year order."""
        return [r["value"] for r in self.raw["inflation"]["path"]]

    @property
    def inflation_years(self) -> List[int]:
        return [r["year"] for r in self.raw["inflation"]["path"]]

    def inflation(self, year: int) -> float:
        """Inflation in one calendar year. Beyond the ladder, the terminal.

        Never extrapolated: past the last published year the path IS the
        terminal, because a fabricated sixth year would be this module doing
        exactly what it exists to stop.
        """
        for r in self.raw["inflation"]["path"]:
            if r["year"] == year:
                return r["value"]
        if year > self.inflation_years[-1]:
            return self.terminal_inflation
        raise MacroPathError(
            "%s: %d is before the path's first year (%d); a study needing an "
            "earlier vintage must take it from the macro-history archive, not "
            "from the forward path" % (self.market, year, self.inflation_years[0]))

    @property
    def terminal_inflation(self) -> float:
        return self.raw["inflation"]["terminal"]["value"]

    @property
    def target(self) -> dict:
        return self.raw["inflation"]["target"]

    def index(self, n: int, start_year: Optional[int] = None) -> List[float]:
        """Cumulative price index over n years, base 1.0 at the start."""
        y0 = start_year or self.inflation_years[0]
        out, cum = [], 1.0
        for i in range(n):
            cum *= 1.0 + self.inflation(y0 + i)
            out.append(cum)
        return out

    # ---- currency ----------------------------------------------------------
    @property
    def fx_spot(self) -> float:
        return self.raw["fx"]["spot"]["value"]

    @property
    def us_inflation_lt(self) -> float:
        return self.raw["us_inflation_lt"]["value"]

    def depreciation_path(self, n: int, start_year: Optional[int] = None) -> List[float]:
        """Annual local-currency depreciation against the dollar, DERIVED.

        Relative purchasing-power parity on this path's own inflation ladder
        against long-run United States inflation. A study may not set this by
        hand: doing so is the second half of [L-048], and on AMOC it was worth
        a manufactured margin decline across the whole forecast.
        """
        y0 = start_year or self.inflation_years[0]
        f = self.us_inflation_lt
        return [(1.0 + self.inflation(y0 + i)) / (1.0 + f) - 1.0 for i in range(n)]

    def fx_path(self, n: int, base: Optional[float] = None,
                start_year: Optional[int] = None) -> List[float]:
        """USD/local average-rate path, derived from the same relation."""
        cum = base if base is not None else self.raw["fx"].get("average_2025", self.fx_spot)
        out = []
        for d in self.depreciation_path(n, start_year):
            cum *= 1.0 + d
            out.append(cum)
        return out

    # ---- rates -------------------------------------------------------------
    @property
    def policy_rate(self) -> float:
        return self.raw["policy_rate"]["current"].get(
            "overnight_deposit", self.raw["policy_rate"]["current"].get("main_operation"))

    @property
    def policy_path(self) -> List[float]:
        return list(self.raw["policy_rate"]["path"])

    @property
    def sovereign_10y(self) -> float:
        return self.raw["sovereign"]["yield_10y"]["value"]

    @property
    def sovereign_asof(self) -> str:
        return self.raw["sovereign"]["yield_10y"]["date"]

    def sovereign_age_days(self, on: Optional[str] = None) -> int:
        d0 = _dt.date.fromisoformat(self.sovereign_asof)
        d1 = _dt.date.fromisoformat(on) if on else _dt.date.today()
        return (d1 - d0).days

    def default_spread(self, basis: str) -> float:
        if basis not in ("rating", "cds"):
            raise MacroPathError("basis must be 'rating' or 'cds', not %r" % basis)
        return self.raw["sovereign"]["default_spread_%s" % basis]

    @property
    def real_rate_convention(self) -> float:
        return self.raw["real_rate_convention"]["value"]

    @property
    def kd_terminal(self) -> float:
        return self.raw["cost_of_debt_norm"]["terminal"]

    @property
    def erp_terminal(self) -> float:
        return self.raw["erp_terminal"]["value"]

    # ---- the derived terminal ---------------------------------------------
    @property
    def terminal_rf(self) -> float:
        """Terminal nominal risk-free: the inflation target in force plus the
        real-rate convention. DERIVED, never quoted — a terminal rate reverse
        engineered from a price is the quietest lever there is and is
        prohibited outright."""
        return self.terminal_inflation + self.real_rate_convention

    def terminal_growth(self, real: float = 0.0) -> float:
        """Terminal nominal growth = terminal inflation + a STATED real growth.

        The default is zero real growth, which is the conservative end and is
        still a claim; a study assuming real decline must say so and show the
        evidence, which is the falsifier [L-055] carries.
        """
        return self.terminal_inflation + real

    # ---- disclosure --------------------------------------------------------
    def sources(self) -> Dict[str, str]:
        """Every level in this path with the document it came from."""
        r = self.raw
        return {
            "inflation.latest": r["inflation"]["latest"]["source"],
            "inflation.path": r["inflation"]["path_source"],
            "inflation.target": r["inflation"]["target"]["source"],
            "inflation.terminal": r["inflation"]["terminal"]["source"],
            "policy_rate": r["policy_rate"]["current"]["source"],
            "policy_rate.path": r["policy_rate"]["path_basis"],
            "sovereign": r["sovereign"]["yield_10y"]["source"],
            "sovereign.spreads": r["sovereign"]["spread_source"],
            "fx": r["fx"]["spot"]["source"],
            "fx.derivation": r["fx"]["derivation"],
            "us_inflation_lt": r["us_inflation_lt"]["source"],
            "cost_of_debt_norm": r["cost_of_debt_norm"]["source"],
            "real_rate_convention": r["real_rate_convention"]["source"],
            "erp_terminal": r["erp_terminal"]["source"],
        }


_CACHE: Dict[str, MacroPath] = {}


def _file(market: str) -> str:
    return os.path.join(PATHS, "%s.json" % market.upper())


def held() -> Dict[str, str]:
    """Every market file on disk and its state — sourced, or pending and why."""
    out = {}
    for m in MARKETS:
        p = _file(m)
        if not os.path.exists(p):
            out[m] = "MISSING FILE"
            continue
        d = json.load(open(p))
        out[m] = ("sourced as of %s (%s)" % (d.get("as_of"), d.get("regime"))
                  if d.get("status", "sourced") == "sourced"
                  else "PENDING — %s" % d.get("pending_reason", "no reason recorded"))
    return out


def load(market: str) -> MacroPath:
    """The house path for one market, or a refusal that names what is missing."""
    m = (market or "").upper()
    if m in _CACHE:
        return _CACHE[m]
    if m not in MARKETS:
        raise MacroPathError(
            "%r is not a covered market. Covered: %s. A market is added by "
            "sourcing its path, never by defaulting to a neighbour."
            % (market, ", ".join(MARKETS)))
    p = _file(m)
    if not os.path.exists(p):
        raise MacroPathError("%s: no macro path file at %s. STOP AND SOURCE IT."
                             % (m, os.path.relpath(p, os.path.dirname(HERE))))
    d = json.load(open(p))
    if d.get("status", "sourced") != "sourced":
        raise MacroPathError(
            "%s: the macro path is PENDING — %s. No study may build against a "
            "market whose macro path has not been sourced; there is no fallback "
            "and a neighbouring market's path is not a substitute."
            % (m, d.get("pending_reason", "no reason recorded")))
    _validate(d, m)
    mp = MacroPath(market=m, currency=d["currency"], as_of=d["as_of"],
                   regime=d["regime"], raw=d)
    _CACHE[m] = mp
    return mp


def _validate(d: dict, m: str) -> None:
    """A sourced file is accepted only if it is internally coherent.

    These are the checks that make the file safe to import, not the checks that
    hold a MODEL to the path — those are assert_macro_coherence(), which runs
    over a study's own committed record.
    """
    if d.get("regime") not in REGIMES:
        raise MacroPathError("%s: regime %r is not one of %s"
                             % (m, d.get("regime"), ", ".join(REGIMES)))
    infl = d["inflation"]
    yrs = [r["year"] for r in infl["path"]]
    if yrs != sorted(yrs) or len(set(yrs)) != len(yrs):
        raise MacroPathError("%s: the inflation ladder's years are not strictly increasing: %s"
                             % (m, yrs))
    for r in infl["path"]:
        if not (-0.10 <= r["value"] <= 1.0):
            raise MacroPathError("%s: inflation %r in %d is outside anything this "
                                 "module will accept without a note"
                                 % (m, r["value"], r["year"]))
        if not r.get("basis"):
            raise MacroPathError("%s: the %d inflation step carries no basis. Every "
                                 "step is either published or labelled as "
                                 "interpolation between published endpoints."
                                 % (m, r["year"]))
    tgt, term = infl["target"]["value"], infl["terminal"]["value"]
    band = infl["target"].get("band", 0.0)
    if abs(term - tgt) > band + 1e-9:
        raise MacroPathError(
            "%s: terminal inflation %.4f sits outside the target band %.4f +/- %.4f. "
            "A terminal outside the band the central bank publishes is a house "
            "view about the central bank, and it must be argued in the file's own "
            "terminal source rather than left as a number." % (m, term, tgt, band))
    if len(d["policy_rate"]["path"]) < 2:
        raise MacroPathError("%s: the policy-rate path needs at least two points to "
                             "give the glide a shape" % m)
    for k in ("sovereign", "fx", "us_inflation_lt", "cost_of_debt_norm",
              "real_rate_convention", "erp_terminal"):
        if k not in d:
            raise MacroPathError("%s: the path carries no %s" % (m, k))
    for basis in ("rating", "cds"):
        if "default_spread_%s" % basis not in d["sovereign"]:
            raise MacroPathError("%s: no %s-basis default spread. Both bases are "
                                 "carried; the choice of central basis is a "
                                 "cost-of-capital decision, not a macro one." % (m, basis))
    # the derived terminal must be internally possible
    rf_t = term + d["real_rate_convention"]["value"]
    if not (0.0 < rf_t < d["cost_of_debt_norm"]["terminal"]):
        raise MacroPathError(
            "%s: the derived terminal risk-free rate %.4f does not sit below the "
            "long-run corporate borrowing norm %.4f. A corporate cannot borrow "
            "below its own sovereign." % (m, rf_t, d["cost_of_debt_norm"]["terminal"]))


# ---------------------------------------------------------------------------
def report(market: Optional[str] = None) -> int:
    if market:
        p = load(market)
        n = len(p.inflation_path)
        print("%s — %s, %s, as of %s" % (p.market, p.currency, p.regime, p.as_of))
        print("  inflation, latest      %.2f%%  (%s)"
              % (100 * p.inflation_latest, p.raw["inflation"]["latest"]["period"]))
        print("  inflation ladder       " + "  ".join(
            "%d %.1f%%" % (y, 100 * v) for y, v in zip(p.inflation_years, p.inflation_path)))
        print("  target                 %.1f%% +/- %.1fpp, %s"
              % (100 * p.target["value"], 100 * p.target.get("band", 0), p.target["horizon"]))
        print("  terminal inflation     %.2f%%" % (100 * p.terminal_inflation))
        print("  terminal risk-free     %.2f%%  = terminal inflation + %.2f%% real (DERIVED)"
              % (100 * p.terminal_rf, 100 * p.real_rate_convention))
        print("  terminal growth, 0 real %.2f%%" % (100 * p.terminal_growth()))
        print("  policy rate            %.2f%% now; path " % (100 * p.policy_rate)
              + " -> ".join("%.2f%%" % (100 * x) for x in p.policy_path))
        print("  sovereign 10y          %.2f%% as of %s (%d days old)"
              % (100 * p.sovereign_10y, p.sovereign_asof, p.sovereign_age_days()))
        if p.sovereign_age_days() > SOVEREIGN_STALE_DAYS:
            print("      STALE beyond %d days — re-source before any new strike"
                  % SOVEREIGN_STALE_DAYS)
        print("  default spread         rating %.2f%%  cds %.2f%%"
              % (100 * p.default_spread("rating"), 100 * p.default_spread("cds")))
        print("  currency               %.4f spot as of %s; derived depreciation "
              % (p.fx_spot, p.raw["fx"]["spot"]["date"])
              + " -> ".join("%.2f%%" % (100 * d) for d in p.depreciation_path(n)))
        print("  derived currency path  " + "  ".join("%.2f" % x for x in p.fx_path(n)))
        print("  terminal cost of debt  %.2f%%   terminal premium %.2f%%"
              % (100 * p.kd_terminal, 100 * p.erp_terminal))
        return 0
    print("HOUSE MACRO PATHS  [R-MACRO-01]")
    st = held()
    for m in MARKETS:
        print("  %-3s %s" % (m, st[m]))
    print("\nA market reading PENDING raises on load; nothing falls back to a "
          "neighbour.\nRead one in full with: python3 engine/macro_path.py EG")
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(report(sys.argv[1] if len(sys.argv) > 1 else None))
