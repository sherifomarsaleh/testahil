"""THE COST-OF-CAPITAL SCHEDULE, IN CODE  [R-COC-01]

The failure. The protocol has carried a sliding-schedule procedure since
13 July 2026 — each explicit year discounted at its own forward rate, gliding
from the explicit-window rate to a norm-built terminal, the glide's shape taken
from the cost-of-debt path, the terminal derived rather than quoted, and a
three-part integrity gate on the cost of debt. It is written down twice, in both
governing documents. On 2 September 2026 exactly ONE study in the repository
implemented it: AMOC, whose compute.py carries the glide, the monotonicity
assert and the `wacc_term < wacc_exp` assert inline. PHDC and TMGH discount every
explicit year and the terminal alike at a single crisis-level rate — 26.25% and
32.37% — which asserts that Egypt's cost of capital never normalises, while the
central bank publishes a disinflation path and the studies' own cost-of-debt
assumptions already contradict them.

That is the whole shape of this repository's recurring defect: the rule existed,
was correct, and was not present at the moment it bound. This module is the rule
made present. A study calls schedule() and gets the whole ladder; it cannot
accidentally discount a five-year forecast at a rate the economy is not expected
to hold, because that is not a thing this function can return.

WHAT IT DOES NOT DO. It does not decide the beta, which belongs to
beta_regression.own_stock_beta(); it takes the record and holds it to its own
gate. It does not invent a macro view: every terminal anchor comes from
macro_path, which is sourced. And it does not apply a glide where a glide has no
business being — a pegged market is already at its terminal by construction of
the peg, the glide collapses to flat, and this module returns a flat schedule
with that stated rather than manufacturing movement.

    python3 engine/cost_of_capital.py        # a worked schedule on the EG path
"""
from __future__ import annotations

import datetime as _dt
import math
import os
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import macro_path as MP                                              # noqa: E402

# One ERP basis is CENTRAL and the other is published as a sensitivity. The
# swap basis is the market's own live pricing of the sovereign's credit; the
# rating basis is an agency's judgement, updated in steps and often stale. Both
# are published; a study may name either as central, and must name one.
ERP_BASES = ("cds", "rating")
DEFAULT_ERP_BASIS = "cds"

# The country premium may be scaled by lambda where a company's exposure to its
# own sovereign genuinely differs from the market's. DEFAULT 1.0, and any other
# value is a stated, argued judgement -- never a quiet adjustment. The 1.52
# equity-to-bond scaling Damodaran publishes is carried as a named alternative
# and is disclosed beside whatever is adopted.
LAMBDA_DEFAULT = 1.0
LAMBDA_EQUITY_BOND_SCALING = 1.52

# Kd integrity, per the standing three-assert gate.
KD_TOLERANCE = 0.015          # within 150bp of the independently computed effective rate
KD_PEAK_HEADROOM = 0.005      # and no more than 50bp above the peak-year effective rate

# A sovereign quote older than this is re-sourced before a strike.
SOVEREIGN_STALE_DAYS = MP.SOVEREIGN_STALE_DAYS


class CostOfCapitalError(RuntimeError):
    """The schedule cannot be built honestly from what was supplied."""


@dataclass
class DebtBook:
    """The borrowings, split the way the Kd gate needs to see them."""
    gross_debt: float
    pct_local_currency: float
    currency_source: str                 # the facility note, bank by bank where disclosed
    kd_local_pretax: float               # MARGINAL: the company's own latest issue, else sovereign + spread
    kd_source: str
    effective_rates: Sequence[float] = ()   # independently computed: interest / average interest-bearing debt
    effective_rate_periods: Sequence[str] = ()
    kd_fx_local_equivalent: Optional[float] = None   # FX coupon + expected depreciation, never a raw FX coupon
    interest_bearing_note: str = ""       # what the denominator of the effective rate actually was
    # the ONE escape from the independent-rate check, and it is stop-and-inform:
    # name the disclosure that is missing, never the inconvenience
    effective_rate_unavailable: str = ""

    def blended_kd(self) -> float:
        if self.kd_fx_local_equivalent is None:
            return self.kd_local_pretax
        w = self.pct_local_currency
        return w * self.kd_local_pretax + (1 - w) * self.kd_fx_local_equivalent


@dataclass
class BetaRecord:
    """Whatever beta_regression produced, plus how it is to be used."""
    beta: float
    tier: int                             # 1 own-stock regression, 2 peer, 3 unity
    source: str
    r2: Optional[float] = None
    se: Optional[float] = None
    n: Optional[int] = None
    index_file: Optional[str] = None
    index_asof: Optional[str] = None
    conforming: bool = True
    shrunk_from: Optional[float] = None   # the raw beta, where Vasicek shrinkage was applied
    shrinkage_note: str = ""


@dataclass
class Schedule:
    market: str
    regime: str
    years: int
    # explicit window
    rf_observed: float
    default_spread: float
    rf_star: float
    erp: float
    erp_basis: str
    beta: float
    ke_exp: float
    kd_pretax: float
    kd_aftertax: float
    weight_equity: float
    weight_debt: float
    wacc_exp: float
    # terminal, every line derived
    rf_terminal: float
    erp_terminal: float
    ke_terminal: float
    kd_terminal_pretax: float
    kd_terminal_aftertax: float
    weight_debt_terminal: float
    wacc_terminal: float
    # the ladder
    glide_fractions: List[float]
    forward_wacc: List[float]
    discount_factors: List[float]
    terminal_discount_factor: float
    # evidence
    kd_integrity: Dict[str, object]
    disclosures: List[str] = field(default_factory=list)
    sensitivity: Dict[str, float] = field(default_factory=dict)

    def as_record(self) -> dict:
        """The shape a study commits and scripts/check_cost_of_capital.py reads."""
        return {
            "market": self.market, "regime": self.regime, "years": self.years,
            "rf_observed": self.rf_observed, "default_spread": self.default_spread,
            "rf_star": self.rf_star, "erp": self.erp, "erp_basis": self.erp_basis,
            "beta": self.beta, "ke_exp": self.ke_exp,
            "kd_pretax": self.kd_pretax, "kd_aftertax": self.kd_aftertax,
            "weight_equity": self.weight_equity, "weight_debt": self.weight_debt,
            "wacc_exp": self.wacc_exp,
            "rf_terminal": self.rf_terminal, "erp_terminal": self.erp_terminal,
            "ke_terminal": self.ke_terminal,
            "kd_terminal_pretax": self.kd_terminal_pretax,
            "kd_terminal_aftertax": self.kd_terminal_aftertax,
            "weight_debt_terminal": self.weight_debt_terminal,
            "wacc_terminal": self.wacc_terminal,
            "glide_fractions": self.glide_fractions,
            "forward_wacc": self.forward_wacc,
            "discount_factors": self.discount_factors,
            "terminal_discount_factor": self.terminal_discount_factor,
            "kd_integrity": self.kd_integrity,
            "sensitivity": self.sensitivity,
            "disclosures": self.disclosures,
        }

    @classmethod
    def from_record(cls, rec: dict) -> "Schedule":
        """Rebuild a Schedule from the record a study committed.

        A study reads back the schedule it published rather than recomputing one,
        so the numbers in its workbook and the numbers its gate checks are the
        same object. Any field the record does not carry is a defect in the
        record, not something to default quietly.
        """
        fields = cls.__dataclass_fields__
        missing = [k for k in fields
                   if k not in rec and fields[k].default is fields[k].default_factory is None]
        missing = [k for k in fields if k not in rec and
                   fields[k].default.__class__.__name__ == "_MISSING_TYPE" and
                   fields[k].default_factory.__class__.__name__ == "_MISSING_TYPE"]
        if missing:
            raise CostOfCapitalError(
                "the committed schedule record is missing %s. A record that cannot rebuild "
                "its own schedule is not a record of it." % ", ".join(missing))
        return cls(**{k: v for k, v in rec.items() if k in fields})

    def shifted(self, delta: float) -> "Schedule":
        """The WHOLE ladder moved by delta — the honest shape of a rate sensitivity.

        A sensitivity that replaces the schedule with a flat rate is not asking
        "what if capital costs more"; it is asking "what if the economy also never
        normalises", which is two questions at once and the second one is the
        assumption this module exists to remove.
        """
        import copy
        s = copy.deepcopy(self)
        s.wacc_exp += delta
        s.wacc_terminal += delta
        s.forward_wacc = [w + delta for w in self.forward_wacc]
        df, cum = [], 1.0
        for w in s.forward_wacc:
            cum /= (1 + w); df.append(cum)
        s.discount_factors = df
        s.terminal_discount_factor = df[-1]
        s.disclosures = list(self.disclosures) + [
            "SENSITIVITY: the whole schedule is shifted by %+.0f basis points; the shape "
            "is unchanged." % (10000 * delta)]
        return s

    def report(self) -> str:
        L = ["COST OF CAPITAL — %s (%s), %d explicit years" % (self.market, self.regime, self.years)]
        L.append("  EXPLICIT WINDOW")
        L.append("    risk-free observed        %7.2f%%" % (100 * self.rf_observed))
        L.append("    less own default spread   %7.2f%%   (country risk counted once)"
                 % (100 * self.default_spread))
        L.append("    normalised risk-free      %7.2f%%" % (100 * self.rf_star))
        L.append("    equity risk premium       %7.2f%%   (%s basis, central)"
                 % (100 * self.erp, self.erp_basis))
        L.append("    beta                      %7.4f" % self.beta)
        L.append("    cost of equity            %7.2f%%" % (100 * self.ke_exp))
        L.append("    cost of debt, pre-tax     %7.2f%%   after tax %.2f%%"
                 % (100 * self.kd_pretax, 100 * self.kd_aftertax))
        L.append("    weights                   %5.1f%% equity / %.1f%% debt, market value"
                 % (100 * self.weight_equity, 100 * self.weight_debt))
        L.append("    WACC, explicit window     %7.2f%%" % (100 * self.wacc_exp))
        L.append("  TERMINAL — every line derived, none quoted")
        L.append("    risk-free                 %7.2f%%   = terminal inflation + real convention"
                 % (100 * self.rf_terminal))
        L.append("    equity risk premium       %7.2f%%   normalised" % (100 * self.erp_terminal))
        L.append("    cost of equity            %7.2f%%" % (100 * self.ke_terminal))
        L.append("    cost of debt, pre-tax     %7.2f%%   long-run corporate norm"
                 % (100 * self.kd_terminal_pretax))
        L.append("    WACC, terminal            %7.2f%%" % (100 * self.wacc_terminal))
        L.append("  THE LADDER")
        L.append("    glide fractions           " + "  ".join("%.3f" % f for f in self.glide_fractions))
        L.append("    forward WACC              " + "  ".join("%.2f%%" % (100 * w) for w in self.forward_wacc))
        L.append("    discount factors          " + "  ".join("%.4f" % d for d in self.discount_factors))
        L.append("    terminal factor           %.4f   (the SAME factor as the last explicit year)"
                 % self.terminal_discount_factor)
        for d in self.disclosures:
            L.append("  · " + d)
        return "\n".join(L)


def _check_kd(book: DebtBook, rf_observed: float) -> Dict[str, object]:
    """The three-assert cost-of-debt gate. All three RAISE; none warns.

    Written after a study took Kd as the midpoint of a disclosed contractual
    range (15-25.27% -> 20.5%) while the rate the company actually paid,
    computed independently, was 24.0% — a 350bp understatement of the single
    input a levered valuation is most convex to.
    """
    if not book.currency_source:
        raise CostOfCapitalError(
            "Kd gate (i): the currency composition of the debt book is not sourced. A name "
            "with meaningful foreign-currency debt needs a currency-blended Kd, and a "
            "single-currency shortcut asserted rather than evidenced is a fail.")
    if len(book.effective_rates) < 2:
        # THE ONE ESCAPE, AND IT IS STOP-AND-INFORM RATHER THAN A WAIVER. Where the
        # disclosure genuinely cannot support the check -- most often because part of
        # the interest incurred is CAPITALISED into work in progress and the statements
        # do not separate it, so the P&L charge over the debt understates the rate by a
        # large multiple -- the study says so, names what is missing, and carries the
        # limitation into its own gap list. It may not simply be silent, and the reason
        # must name the disclosure, not the inconvenience.
        why = (book.effective_rate_unavailable or "").strip()
        if len(why) < 60 or "disclos" not in why.lower():
            raise CostOfCapitalError(
                "Kd gate (ii): an INDEPENDENTLY computed effective rate is required over "
                "at least two periods (interest INCURRED over average interest-bearing "
                "debt). %d supplied, and no adequate reason recorded. A disclosed "
                "contractual range's midpoint is not evidence, and 'not available' is not "
                "a reason -- name the disclosure that is missing."
                % len(book.effective_rates))
        return {
            "adopted_kd": book.blended_kd(),
            "effective_rates": list(book.effective_rates),
            "effective_rate_periods": list(book.effective_rate_periods),
            "effective_rate_unavailable": why,
            "currency_source": book.currency_source,
            "interest_bearing_note": book.interest_bearing_note,
            "pct_local_currency": book.pct_local_currency,
            "limitation": ("the independent effective-rate check could not be performed on "
                           "this company's disclosure; the adopted rate rests on the "
                           "sovereign plus a stated corporate spread and this is a "
                           "limitation of the study, recorded rather than passed over"),
        }
    if not book.interest_bearing_note:
        raise CostOfCapitalError(
            "Kd gate (ii): the effective rate's DENOMINATOR is not described. Dividing the "
            "finance charge by a broader liabilities total — customer advances, supplier "
            "balances, cheques under collection, none of which bear interest — understates "
            "the rate by a multiple and manufactures a bias that looks like evidence.")
    kd = book.blended_kd()
    latest = book.effective_rates[-1]
    peak = max(book.effective_rates)
    if abs(kd - latest) > KD_TOLERANCE:
        raise CostOfCapitalError(
            "Kd gate (iii): the adopted Kd of %.2f%% is %.0fbp from the most recent "
            "independently computed effective rate of %.2f%%, beyond the %.0fbp bound."
            % (100 * kd, 10000 * abs(kd - latest), 100 * latest, 10000 * KD_TOLERANCE))
    if kd > peak + KD_PEAK_HEADROOM:
        raise CostOfCapitalError(
            "Kd gate (iii): the adopted Kd of %.2f%% exceeds the peak-year effective rate "
            "of %.2f%% by more than %.0fbp."
            % (100 * kd, 100 * peak, 10000 * KD_PEAK_HEADROOM))
    if book.pct_local_currency >= 0.999 and kd < rf_observed:
        raise CostOfCapitalError(
            "the adopted Kd of %.2f%% sits BELOW the sovereign yield of %.2f%% on an "
            "all-local-currency book. A same-currency corporate cannot borrow below its "
            "own sovereign." % (100 * kd, 100 * rf_observed))
    return {
        "adopted_kd": kd,
        "effective_rates": list(book.effective_rates),
        "effective_rate_periods": list(book.effective_rate_periods),
        "latest_effective": latest, "peak_effective": peak,
        "within_tolerance_bp": 10000 * abs(kd - latest),
        "currency_source": book.currency_source,
        "interest_bearing_note": book.interest_bearing_note,
        "pct_local_currency": book.pct_local_currency,
    }


def schedule(market: str,
             beta: BetaRecord,
             debt: DebtBook,
             market_cap: float,
             tax_rate: float,
             years: int = 5,
             erp_basis: str = DEFAULT_ERP_BASIS,
             lambda_country: float = LAMBDA_DEFAULT,
             erp_explicit: Optional[float] = None,
             weight_debt_terminal: Optional[float] = None,
             build_date: Optional[str] = None,
             allow_stale_sovereign: bool = False) -> Schedule:
    """The whole ladder, from one call.

    Every explicit year is discounted at its own forward rate; the terminal value
    is capitalised at the terminal rate and brought home on the SAME cumulative
    factor as the last explicit year's cash flow. One date, one price of time —
    the common construction that discounts the explicit years at one rate and the
    terminal alone at a much lower one gave a pound arriving on 31-Dec-2030 a
    factor of 0.410 as a forecast cash flow and 0.532 inside the terminal value,
    a 30% premium for relabelling it.
    """
    path = MP.load(market)
    if erp_basis not in ERP_BASES:
        raise CostOfCapitalError("erp_basis must be one of %s" % ", ".join(ERP_BASES))

    age = path.sovereign_age_days(build_date)
    if age > SOVEREIGN_STALE_DAYS and not allow_stale_sovereign:
        raise CostOfCapitalError(
            "the %s sovereign quote is %d days old (as of %s) against a %d-day bound. "
            "Re-source it before striking a valuation on it, or pass "
            "allow_stale_sovereign=True and disclose the age in the study."
            % (market, age, path.sovereign_asof, SOVEREIGN_STALE_DAYS))

    if beta.tier == 1 and not beta.conforming:
        raise CostOfCapitalError(
            "a tier-1 beta is recorded as non-conforming. A composite regressor is a hard "
            "fail, not a fallback: fall to a same-country peer beta and say so.")

    rf_observed = path.sovereign_10y
    spread = path.default_spread(erp_basis)
    rf_star = rf_observed - spread                    # country risk counted ONCE
    if rf_star <= 0:
        raise CostOfCapitalError(
            "the normalised risk-free rate is not positive (%.2f%% less %.2f%%). Check that "
            "the default spread and the yield are on the same basis."
            % (100 * rf_observed, 100 * spread))

    erp = erp_explicit if erp_explicit is not None else path.raw.get("erp_%s" % erp_basis)
    if erp is None:
        # the path carries the sovereign spreads; the market ERP itself is a study
        # input from the country-risk file, and must be supplied rather than guessed
        raise CostOfCapitalError(
            "no explicit-window equity risk premium supplied and the %s path carries none. "
            "It comes from the country-risk file's own row for this sovereign, read fresh; "
            "it is never borrowed from a neighbour." % market)
    if lambda_country != LAMBDA_DEFAULT:
        erp = erp * lambda_country

    ke_exp = rf_star + beta.beta * erp
    kd_pre = debt.blended_kd()
    kd_at = kd_pre * (1 - tax_rate)
    kd_integrity = _check_kd(debt, rf_observed)

    total_cap = market_cap + debt.gross_debt
    if total_cap <= 0:
        raise CostOfCapitalError("total capital is not positive")
    we = market_cap / total_cap                        # MARKET-value equity, never book
    wd = debt.gross_debt / total_cap
    wacc_exp = we * ke_exp + wd * kd_at

    # ---- the terminal, every line derived ---------------------------------
    rf_t = path.terminal_rf
    erp_t = path.erp_terminal
    ke_t = rf_t + beta.beta * erp_t
    kd_t = path.kd_terminal
    kd_t_at = kd_t * (1 - tax_rate)
    wd_t = weight_debt_terminal if weight_debt_terminal is not None else wd
    wacc_t = (1 - wd_t) * ke_t + wd_t * kd_t_at

    disclosures = []
    pegged = path.regime != "transition"
    if pegged:
        # today IS the terminal: the glide collapses to flat rather than being
        # applied to manufacture movement the peg forbids
        fwd = [wacc_exp] * years
        fracs = [0.0] * years
        wacc_t = wacc_exp
        disclosures.append(
            "%s runs a %s regime, so the risk-free rate already sits at its long-run level "
            "and the schedule is FLAT by construction. Applying a glide here would "
            "manufacture movement the peg forbids and measures nothing (+0.0%% where it "
            "was tried)." % (market, path.regime))
    else:
        if wacc_t >= wacc_exp:
            raise CostOfCapitalError(
                "the terminal cost of capital (%.2f%%) is not below the explicit-window rate "
                "(%.2f%%) in a market the path calls a transition. Either the terminal "
                "anchors or the explicit inputs are wrong; a schedule that does not decline "
                "is a flat WACC wearing a ladder." % (100 * wacc_t, 100 * wacc_exp))
        # the glide's SHAPE is the cost-of-debt path's own cumulative progress,
        # so the front-loading is inherited from the easing calendar rather than
        # being a second free parameter
        kdp = list(path.policy_path)[:years]
        while len(kdp) < years:
            kdp.append(kdp[-1])
        span = kdp[0] - kdp[-1]
        if span <= 0:
            raise CostOfCapitalError(
                "the policy-rate path does not decline, so it cannot give the glide a shape. "
                "A market whose own rate path is flat is not in transition.")
        fracs = [(kdp[0] - k) / span for k in kdp]
        fwd = [wacc_exp - (wacc_exp - wacc_t) * f for f in fracs]
        for i in range(years - 1):
            if fwd[i] < fwd[i + 1] - 1e-12:
                raise CostOfCapitalError("the glide is not monotone: %s"
                                         % ["%.4f" % x for x in fwd])
        disclosures.append(
            "The glide fractions are the policy-rate path's own cumulative progress, so the "
            "front-loaded shape is inherited from the assumed easing calendar rather than "
            "being a second free parameter.")

    df, cum = [], 1.0
    for w in fwd:
        cum /= (1 + w)
        df.append(cum)
    terminal_df = df[-1]                # ONE DATE, ONE PRICE OF TIME

    disclosures.append(
        "Country risk enters once: the risk-free rate is normalised by this sovereign's own "
        "default spread (%.2f%%) on the %s basis, and the premium added back is on the same "
        "basis." % (100 * spread, erp_basis))
    disclosures.append(
        "The terminal is norm-built and no line in it is an observable quote: risk-free "
        "%.2f%% = the inflation target in force (%.2f%%) plus the real-rate convention "
        "(%.2f%%); cost of debt %.2f%% is the long-run corporate norm; the premium is "
        "normalised to %.2f%%."
        % (100 * rf_t, 100 * path.terminal_inflation, 100 * path.real_rate_convention,
           100 * kd_t, 100 * erp_t))
    if beta.shrunk_from is not None:
        disclosures.append("Beta shrunk from %.4f to %.4f: %s"
                           % (beta.shrunk_from, beta.beta, beta.shrinkage_note))
    if lambda_country != LAMBDA_DEFAULT:
        disclosures.append(
            "The country premium is scaled by lambda = %.2f. The default is 1.00 and any "
            "other value is a stated judgement; Damodaran's equity-to-bond scaling of %.2f "
            "is the named alternative." % (lambda_country, LAMBDA_EQUITY_BOND_SCALING))
    if age > SOVEREIGN_STALE_DAYS:
        disclosures.append(
            "DISCLOSED STALENESS: the sovereign quote is %d days old (as of %s), beyond the "
            "%d-day bound, and was accepted deliberately." % (age, path.sovereign_asof,
                                                              SOVEREIGN_STALE_DAYS))

    # the other ERP basis, published as a sensitivity rather than hidden
    other = "rating" if erp_basis == "cds" else "cds"
    other_spread = path.default_spread(other)
    sens = {}
    if erp_explicit is None:
        sens = {"note": "the alternative premium basis is published where the study carries it"}
    sens = dict(sens or {})
    sens["other_basis"] = other
    sens["other_default_spread"] = other_spread
    sens["rf_star_other_basis"] = rf_observed - other_spread

    return Schedule(
        market=market, regime=path.regime, years=years,
        rf_observed=rf_observed, default_spread=spread, rf_star=rf_star,
        erp=erp, erp_basis=erp_basis, beta=beta.beta, ke_exp=ke_exp,
        kd_pretax=kd_pre, kd_aftertax=kd_at,
        weight_equity=we, weight_debt=wd, wacc_exp=wacc_exp,
        rf_terminal=rf_t, erp_terminal=erp_t, ke_terminal=ke_t,
        kd_terminal_pretax=kd_t, kd_terminal_aftertax=kd_t_at,
        weight_debt_terminal=wd_t, wacc_terminal=wacc_t,
        glide_fractions=fracs, forward_wacc=fwd, discount_factors=df,
        terminal_discount_factor=terminal_df,
        kd_integrity=kd_integrity, disclosures=disclosures, sensitivity=sens)


class Discounter:
    """The schedule's discount factor for ANY year, explicit or beyond.

    The explicit years use the ladder. A cash flow arriving after the window --
    a residual order book converting over a further ten years, a recurring
    perpetuity's own capitalisation -- compounds on the LAST EXPLICIT FACTOR at
    the terminal rate. That is the whole of "one date, one price of time" in
    code: there is no year for which two different factors exist, and a study
    cannot give the same pound a cheaper ride by relabelling which block of the
    model it sits in.
    """

    def __init__(self, sched: "Schedule"):
        self.sched = sched
        self._df = list(sched.discount_factors)
        self._n = len(self._df)
        self._wt = sched.wacc_terminal

    def factor(self, year: int) -> float:
        """year is 1-based: 1 is the first explicit year."""
        if year < 1:
            raise CostOfCapitalError("year must be 1 or greater, not %r" % year)
        if year <= self._n:
            return self._df[year - 1]
        return self._df[-1] / (1 + self._wt) ** (year - self._n)

    def annuity(self, first_year: int, n: int) -> float:
        """Sum of factors for n years starting at first_year."""
        return sum(self.factor(first_year + k) for k in range(n))

    def perpetuity_factor(self, growth: float, from_year: Optional[int] = None) -> float:
        """The capitalisation multiple for a growing perpetuity struck at the end
        of the explicit window, brought home on that window's own factor."""
        y = from_year or self._n
        if self._wt <= growth:
            raise CostOfCapitalError(
                "a growing perpetuity needs the terminal rate (%.4f) above the growth "
                "(%.4f). A capped denominator is a free parameter hiding an impossible "
                "assumption." % (self._wt, growth))
        return (1 + growth) / (self._wt - growth) * self.factor(y)


def flat_schedule(rate: float, years: int, market: str = "EG",
                  why: str = "") -> Schedule:
    """A DEGENERATE schedule at one rate for every year.

    This exists for exactly one purpose: answering the question "what single flat
    rate would reproduce the traded price", which is a fair question to put to a
    reader who is used to seeing one rate. It is never a valuation construction,
    and the disclosure it carries says so.
    """
    fwd = [rate] * years
    df, cum = [], 1.0
    for w in fwd:
        cum /= (1 + w); df.append(cum)
    return Schedule(
        market=market, regime="flat (degenerate)", years=years,
        rf_observed=float("nan"), default_spread=float("nan"), rf_star=float("nan"),
        erp=float("nan"), erp_basis="cds", beta=float("nan"),
        ke_exp=float("nan"), kd_pretax=float("nan"), kd_aftertax=float("nan"),
        weight_equity=float("nan"), weight_debt=float("nan"), wacc_exp=rate,
        rf_terminal=float("nan"), erp_terminal=float("nan"), ke_terminal=float("nan"),
        kd_terminal_pretax=float("nan"), kd_terminal_aftertax=float("nan"),
        weight_debt_terminal=float("nan"), wacc_terminal=rate,
        glide_fractions=[0.0] * years, forward_wacc=fwd,
        discount_factors=df, terminal_discount_factor=df[-1],
        kd_integrity={"note": "not applicable to a degenerate flat schedule"},
        disclosures=["A FLAT schedule, used only to answer 'what one rate would "
                     "reproduce this price'. It is not a valuation construction. " + why])


def vasicek_shrink(beta_hat: float, se: float, prior: float, prior_sd: float) -> float:
    """Shrink a noisy regression beta toward a market-class prior.

    A beta measured with a standard error of 0.18 is not the same object as one
    measured with 0.03, and treating them alike is how a single noisy regression
    moves a valuation by a fifth. The weight is the ratio of precisions, so a
    tight estimate barely moves and a loose one moves a long way.
    """
    if se is None or se <= 0:
        return beta_hat
    w = (prior_sd ** 2) / (prior_sd ** 2 + se ** 2)
    return w * beta_hat + (1 - w) * prior


if __name__ == "__main__":
    # A worked schedule on the Egyptian path, using PHDC's own committed inputs.
    b = BetaRecord(beta=1.0493, tier=1, r2=0.299, se=0.1823, n=251,
                   index_file="engine/raw_indices/EG/EGX30.csv",
                   index_asof="2026-07-22", conforming=True,
                   source="own-stock weekly regression against the exchange's published index")
    d = DebtBook(gross_debt=33552.7, pct_local_currency=1.0,
                 currency_source="all eight borrowing lines on the balance sheet are EGP",
                 kd_local_pretax=0.255,
                 kd_source="the company's own latest issue",
                 effective_rates=(0.243, 0.251),
                 effective_rate_periods=("FY2024", "FY2025"),
                 interest_bearing_note=("finance cost over the average of the bank and loan "
                                        "lines only — customer advances and notes payable to "
                                        "land sellers bear no interest"))
    s = schedule("EG", b, d, market_cap=43470.8, tax_rate=0.225, years=5,
                 erp_explicit=0.0941, erp_basis="cds", allow_stale_sovereign=True)
    print(s.report())
