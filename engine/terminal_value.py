"""[R-TERM-01] — THE ONLY SANCTIONED WAY TO BUILD A TERMINAL VALUE.

WHY THIS MODULE EXISTS, and it is the same reason `beta_regression.own_stock_beta()` and
`cost_of_capital.py` exist. Every study in this repository once hand-rolled its own beta,
and every one of them was wrong in the same direction. Every study hand-rolls its own
terminal today, and the census (engine/valuation_calibration/terminal_census.py) measured
what that costs: FOUR OF TWELVE READABLE STUDIES PUBLISH A TERMINAL WORTH LESS THAN NOT
INVESTING AT ALL.

THE DEFECT THIS MODULE MAKES INEXPRESSIBLE. The reinvestment identity

    rr = g / ROIC        TV = NOPAT (1 - rr) / (W - g)

substitutes to

    TV = [ NOPAT - g . IC ] / (W - g)

so it charges `g x IC` every year, for ever. THE IDENTITY IS A STATEMENT ABOUT REAL GROWTH.
Where g is nominal and its real component is zero — which is what the house macro path
returns for every terminal it builds [R-MACRO-01] — the charge buys no capacity at all.
Read the charge as a capital-maintenance programme and the implied replacement cycle is

    IC / (g . IC)  =  1 / g

THE IMPLIED ASSET LIFE IS THE RECIPROCAL OF THE INFLATION RATE. It is not a fact about the
asset. At 7% terminal inflation it is 14.3 years; at 15% it is 6.7. A cement kiln does not
get younger because the currency got worse. ARCC's terminal computed to 14.3 years against
1/g of 14.3 to the decimal, charging 62.2% of terminal profit for ever against its own
FY2030 explicit capex of 1.76x book depreciation.

SO THE CONTRACT HERE TAKES REAL GROWTH AND NOTHING ELSE. A nominal rate cannot arrive as a
growth assumption: `real_growth` is what the caller supplies, inflation comes from the
house macro path, and the nominal rate is DERIVED. That is the same discipline
[R-MACRO-01] applies to the terminal risk-free rate and for the same reason — a quantity
that must be coherent with another is derived from it, never quoted beside it.

WHAT A TERMINAL COSTS, correctly. In a nominal steady state holding physical capacity:

    FCFF = NOPAT + D&A_book - maintenance_at_current_cost - real_growth_capex - pi . WC

  * NOPAT is already net of BOOK depreciation, which is struck on historical cost. So book
    D&A is added back and the real cash cost of replacement is charged instead. Omitting
    the add-back — which the ARCC terminal does while its own explicit window performs it —
    is a second, independent error, and it means ONE MODEL CARRIES TWO DEFINITIONS OF FREE
    CASH FLOW with the terminal holding 41% of enterprise value.
  * maintenance at current cost is IC_replacement / useful_life, and useful_life is a
    DISCLOSED figure from the accounting-policies note, never a house guess (SIGCM clause
    1). Two independent routes to this quantity agree on ARCC to within 3.9% — IC/30 gives
    1,706.4 and book D&A escalated over half an asset life gives 1,775.3 — which validates
    the replacement-cost base and the life together.

    THE AGE IS MEASURED WHERE THE ACCOUNTS GIVE IT [re-pointed 4 September 2026]. The
    `book_dna_escalated` basis escalates the book charge to current cost over the average
    AGE of the assets carrying it, and half the useful life is only that age under UNIFORM
    VINTAGES. Where a base is not in steady state the proxy is wrong, and the error scales
    with inflation, so it is invisible in a pegged market and severe in a high-inflation
    one. MEASURED ON EGCH: a depreciable gross cost of EGP 17.02bn against a charge of
    771.2mn implies a 22.07-year life, while accumulated depreciation of 3.44bn over the
    same charge puts the average age at 4.45 YEARS against the 11.04 half the life assumes
    — the plant was rebuilt recently and only 1.3% of the base sits fully depreciated. At
    Egypt's 7% terminal the two escalators are 1.352 and 2.110, so the proxy over-charges
    maintenance by 56%, and on that name it charged 144% of terminal profit and drove the
    equity negative. A company that has just built a new plant was being charged as though
    the plant were eleven years old.

    accumulated depreciation / the year's own charge IS the charge-weighted average age
    under straight-line, exactly — it is an identity off the accounts, not an estimate, and
    it is slightly OVERSTATED where assets sit fully depreciated and still in use, which
    errs toward charging more.

    TWO DISCLOSED CONDITIONS BREAK IT AND BOTH ARE CHECKABLE BEFORE IT IS USED. The identity
    holds because accumulated = age x charge, which needs the charge to be cost/life.
    (i) WHERE ASSETS ARE DEPRECIATED TO A RESIDUAL VALUE the charge is (cost - residual)/life,
    so the same accumulated balance buys MORE years and the ratio OVERSTATES the age.
    (ii) WHERE A USEFUL LIFE HAS BEEN REASSESSED the charge is not level across the base's
    history and the identity is broken outright rather than merely biased.

    FOUND ON THE THIRD NAME IT WAS TRIED ON, and the disagreement announced itself before the
    accounts did: AIRARABIA's identity-implied life came to 26.42 years against the 17.84 its
    own disclosed class lives weight to — 48% apart, which no rounding explains. The policy
    note then says both things outright: depreciation writes off cost "less their estimated
    residual values", and the group "changed the estimated useful life applied to certain
    assets" during the year. The measured age of 14.32 years is therefore not this fleet's
    age, and applying it would have moved that study -9.7% on a terminal carrying 95% of
    enterprise value. NOT APPLIED.

    SO THE CHEAP CROSS-CHECK IS THE ONE TO RUN FIRST: compare the identity's implied life
    (depreciable gross cost over the charge) with the life the DISCLOSED CLASS RATES weight
    to. Where they agree the residual is immaterial and the age is usable; where they diverge,
    the accounts are saying the charge is not cost/life and the age must not be read off it.

    AND THE CHECK IS CIRCULAR WHERE THE STUDY DERIVED ITS LIFE BY THE SAME IDENTITY, which is
    most of them, so saying so is part of running it. On the three names carrying a measured
    age the implied and adopted lives agree to 0.0% for exactly that reason and the agreement
    proves nothing; what does the work there is the SEPARATE evidence that the charge is
    cost/life — a policy note that writes off cost with no residual mentioned, a leg whose
    single disclosed life the identity reproduces (EMPOWER's intangibles at 30 years,
    RIYADHCABLE's software at 14.43 against a stated 15), and an implied life that sits inside
    the disclosed range rather than outside it (EGCH's 22.07 against class rates spanning 10.5
    to 25.3, on a base dominated by the plant carrying the 25.3). AIRARABIA is the case where
    the two lives came from genuinely different routes, and that is why the 48% gap was
    visible at all. Supply it and it is used; leave it and half the life is used
    and the record SAYS WHICH, so a reader can tell an assumption from a measurement.
    Per [R-COC-01]: WHEN A CHECK FIRES ON WORK THAT IS RIGHT, RE-POINT IT — never widen it
    and never move the number to satisfy it. The direction is not universal, which is the
    whole reason it needed measuring rather than correcting: of the three bases measured,
    one is younger than uniform, one older, and one far younger.
  * real growth capex is charged at the incremental capital the REAL growth needs, and only
    that. Zero real growth costs zero growth capex.
  * working capital grows with the price level, so pi x WC is a real cash cost of inflation
    and IS charged.

THE DOMINANCE ARGUMENT, AND A CORRECTION TO ITS FIRST FORM. This module first refused any
terminal below NOPAT_last / W, on the argument that a company can always decline to invest
and pay out instead. THAT FORMULATION WAS WRONG, AND IT WAS WRONG IN THE SAME WAY AS THE
DEFECT IT WAS BUILT TO CATCH: it treats BOOK depreciation — struck on historical cost — as
if it were the cash cost of replacing the asset. NOPAT is net of book D&A, so NOPAT/W is
the value of distributing NOPAT for ever while actually needing current-cost replacement
spending several times larger. That is not an available policy: a company that stops
replacing its plant does not become a perpetuity, it becomes a liquidation. Nor is "zero
NOMINAL growth" a choice a board can make — prices are set by the market.

It also fails arithmetically at high discount rates, where TV/floor tends to
FCFF(1+g)/NOPAT, a ratio BELOW ONE by construction whenever maintenance exceeds book D&A.
ARCC's own beta sensitivity grid found it: at a high beta the test fired on a perfectly
sound terminal. Under [R-COC-01]'s rule — when a check fires on work that is right, RE-POINT
IT, never widen it and never move the number to satisfy it — the test was re-pointed.

WHAT SURVIVES IS NARROWER AND IS ACTUALLY TRUE: a company is never obliged to spend GROWTH
capital. So a terminal may not charge growth capital beyond what its STATED REAL growth
requires. That is enforced structurally rather than by comparison — `real_growth` is what
the caller supplies, growth capex is computed from it, and zero real growth costs exactly
zero. The construction that charges g x IC cannot be expressed at all.

`floor` is still returned and is still worth reading, but it is now LABELLED FOR WHAT IT IS:
the value of a NOPAT perpetuity with maintenance at book depreciation. It is not a bound the
builder enforces. It earns its place because ARCC's retired construction fell 34.6% below
even that generous reading, which is how the defect was found.

VERIFY BY IMPORT, NOT BY PARSE — this module is checked by importing it, like every other
shared module in this engine.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Optional

# The closed list of grounds on which a terminal may sit below its own floor. Closed for
# [R-COC-01 AMENDED]'s reason: an open list lets any study opt out by inventing a reason,
# and "the business needs the capex" is not an obligation.
FLOOR_EXEMPTIONS = (
    'concession_capex_obligation',   # a concession or licence mandating the spend
    'take_or_pay_obligation',        # a contract compelling purchase or construction
    'regulatory_capex_mandate',      # a regulator's binding investment programme
)

# Where maintenance capital may come from. 'disclosed_life' is the standard.
MAINTENANCE_BASES = (
    'disclosed_life',        # IC_replacement / useful life from the accounting-policies note
    'disclosed_capex',       # the company's own stated maintenance capex
    'book_dna_escalated',    # book D&A escalated over half a disclosed life — a cross-check
)


class TerminalRefused(Exception):
    """A terminal that cannot be built as specified. It raises; it never warns."""


@dataclass
class TerminalInputs:
    """Everything a terminal needs, in the terminal year's own money."""
    nopat: float                  # terminal-year NOPAT, net of BOOK depreciation
    wacc: float                   # terminal WACC, from cost_of_capital.py
    inflation: float              # terminal inflation, from the house macro path
    real_growth: float = 0.0      # STATED real growth. Nominal is derived, never supplied.
    dna_book: float = 0.0         # book depreciation inside that NOPAT
    ic_replacement: Optional[float] = None
    useful_life_years: Optional[float] = None
    useful_life_source: str = ''  # the accounting-policies note it came from
    # THE AGE OF THE BASE, MEASURED RATHER THAN ASSUMED. `book_dna_escalated` escalates the
    # book charge to current cost over the average age of the assets carrying it, and that
    # age is an IDENTITY the accounts give: accumulated depreciation over the year's own
    # charge is, under straight-line, exactly the charge-weighted average age. Supply it
    # and it is used; leave it and half the useful life is used instead and SAID SO — see
    # `maintenance_age_basis` on the record. Slightly overstated where assets sit fully
    # depreciated and still in use, which errs toward charging more.
    average_age_years: Optional[float] = None
    average_age_source: str = ''  # the note the two figures were read from
    maintenance_basis: str = 'disclosed_life'
    maintenance_capex: Optional[float] = None   # where disclosed directly
    working_capital: float = 0.0
    incremental_capital_per_unit_growth: Optional[float] = None  # capital per 1.0 of real g
    floor_exemption: str = ''
    floor_exemption_disclosure: str = ''

    def nominal_growth(self) -> float:
        """DERIVED. (1+pi)(1+g_real) - 1 — never quoted, so it cannot disagree with itself."""
        return (1.0 + self.inflation) * (1.0 + self.real_growth) - 1.0


@dataclass
class Terminal:
    fcff: float
    tv: float
    floor: float
    nominal_growth: float
    maintenance: float
    growth_capex: float
    wc_charge: float
    dna_addback: float
    implied_cycle_years: Optional[float]
    below_floor: bool
    record: dict = field(default_factory=dict)


def build(i: TerminalInputs) -> Terminal:
    """The terminal, or a refusal. There is no third outcome."""
    if not (0.0 < i.wacc < 1.0):
        raise TerminalRefused(f'terminal rate {i.wacc} is not a rate')
    g = i.nominal_growth()
    if g >= i.wacc:
        raise TerminalRefused(
            f'derived nominal growth {g:.4%} is not below the terminal rate {i.wacc:.4%}; '
            f'the perpetuity does not converge')
    if i.maintenance_basis not in MAINTENANCE_BASES:
        raise TerminalRefused(
            f'maintenance basis {i.maintenance_basis!r} is not one of {MAINTENANCE_BASES}. '
            f'The list is closed so that a study cannot opt out by inventing a basis.')

    # --- capital maintenance, at CURRENT cost -----------------------------------------
    age, age_basis = None, 'not_applicable'
    if i.maintenance_capex is not None:
        maint = float(i.maintenance_capex)
    elif i.maintenance_basis == 'disclosed_life':
        if not i.ic_replacement or not i.useful_life_years:
            raise TerminalRefused(
                'maintenance on a disclosed life needs BOTH the replacement-cost capital '
                'base and the useful life. A life this desk chose is not a disclosed life '
                '(SIGCM clause 1): name the accounting-policies note or stop.')
        if not i.useful_life_source:
            raise TerminalRefused(
                'the useful life carries no source. Under SIGCM clause 1 a figure with no '
                'disclosure behind it is a figure this desk does not use.')
        maint = i.ic_replacement / float(i.useful_life_years)
    elif i.maintenance_basis == 'book_dna_escalated':
        if i.average_age_years is not None:
            if not (0.0 <= float(i.average_age_years) < 200.0):
                raise TerminalRefused(
                    f'average age {i.average_age_years} is not an age')
            if not i.average_age_source:
                raise TerminalRefused(
                    'the average age carries no source. It is an identity off the accounts '
                    '— accumulated depreciation over the year\'s own charge — so name the '
                    'note both figures were read from or do not supply it (SIGCM clause 1).')
            age = float(i.average_age_years)
            age_basis = 'measured'
        else:
            if not i.useful_life_years:
                raise TerminalRefused(
                    'escalating book D&A needs either the MEASURED average age of the base '
                    'or a life to take half of')
            age = float(i.useful_life_years) / 2.0
            age_basis = 'half_of_life'
        maint = i.dna_book * (1.0 + i.inflation) ** age
    else:
        raise TerminalRefused('disclosed_capex basis chosen but no maintenance_capex given')

    # --- growth capital, for REAL growth only ------------------------------------------
    if i.real_growth == 0.0:
        growth_capex = 0.0
    else:
        if i.incremental_capital_per_unit_growth is None:
            raise TerminalRefused(
                'real growth of %.3f%% was stated but no incremental capital was supplied. '
                'Real growth costs capital and the amount is a driver, not a residual. '
                'THE ONE THING THIS MODULE WILL NOT DO IS CHARGE g x IC: that implies '
                'replacing the whole asset base every 1/g years, which is a fact about the '
                'inflation rate and not about the asset.' % (100.0 * i.real_growth))
        growth_capex = i.real_growth * float(i.incremental_capital_per_unit_growth)

    wc_charge = i.inflation * i.working_capital
    fcff = i.nopat + i.dna_book - maint - growth_capex - wc_charge
    if fcff <= 0.0:
        raise TerminalRefused(
            f'terminal free cash flow is {fcff:,.1f}, not positive: a going concern that '
            f'consumes cash for ever is not a terminal, it is a liquidation, and it must be '
            f'valued as one')
    payout = fcff / i.nopat if i.nopat else float('inf')
    if not (0.0 < payout <= 1.0 + 1e-9):
        raise TerminalRefused(
            f'implied payout of terminal NOPAT is {payout:.1%}, outside [0, 1]: the '
            f'terminal distributes more than it earns')

    tv = fcff * (1.0 + g) / (i.wacc - g)
    # The NOPAT perpetuity at BOOK depreciation. A DIAGNOSTIC, not a bound — see the
    # docstring: it assumes a maintenance charge the company does not actually face, so it
    # is not an available policy and cannot dominate anything. Reported because the
    # retired g x IC construction fell below even this generous reading.
    floor = i.nopat / i.wacc
    below = tv < floor

    charge = maint + growth_capex + wc_charge - i.dna_book
    cycle  = (i.ic_replacement / charge) if (i.ic_replacement and charge > 0) else None
    t = Terminal(fcff=fcff, tv=tv, floor=floor, nominal_growth=g, maintenance=maint,
                 growth_capex=growth_capex, wc_charge=wc_charge, dna_addback=i.dna_book,
                 implied_cycle_years=cycle, below_floor=below)
    t.record = dict(
        rule='R-TERM-01', inputs=asdict(i), fcff=fcff, tv=tv, floor=floor,
        tv_vs_floor=tv / floor - 1.0, nominal_growth=g, real_growth=i.real_growth,
        maintenance=maint, maintenance_age_years=age,
        maintenance_age_basis=age_basis,
        maintenance_escalator=((1.0 + i.inflation) ** age) if age is not None else None,
        growth_capex=growth_capex, wc_charge=wc_charge,
        dna_addback=i.dna_book, net_capital_charge=charge,
        implied_cycle_years=cycle, one_over_g=(1.0 / g if g > 0 else None),
        payout_of_nopat=payout,
        note=('the nominal growth rate is DERIVED from the house inflation path and the '
              'stated real growth; the capital charge is maintenance at current cost plus '
              'the capital real growth actually needs, never g x IC'))
    return t


def assert_terminal(record: dict) -> None:
    """Hold a study's committed terminal record to this rule, from outside the study."""
    if not isinstance(record, dict):
        raise TerminalRefused('no terminal record')
    for k in ('tv', 'floor', 'nominal_growth', 'real_growth', 'net_capital_charge'):
        if k not in record:
            raise TerminalRefused(f'terminal record is missing {k}')
    g, gr = float(record['nominal_growth']), float(record['real_growth'])
    infl = (record.get('inputs') or {}).get('inflation')
    if infl is not None:
        want = (1.0 + float(infl)) * (1.0 + gr) - 1.0
        if abs(want - g) > 1e-9:
            raise TerminalRefused(
                f'nominal growth {g:.6f} does not reproduce from inflation {infl:.6f} and '
                f'stated real growth {gr:.6f} (would be {want:.6f}). A nominal rate that '
                f'does not derive is a typed rate, and nobody can tell whether it meant '
                f'inflation plus one point or inflation minus three.')
    # THE DOMINANCE TEST THAT SURVIVES: growth capital charged beyond what stated real
    # growth requires. A company is never obliged to spend it.
    gc = record.get('growth_capex')
    if gc is not None and gr == 0.0 and float(gc) > 0.0:
        raise TerminalRefused(
            f'growth capital of {float(gc):,.1f} is charged against a STATED REAL GROWTH of '
            f'zero. A company is never obliged to spend growth capital, so this terminal is '
            f'dominated by declining it. This is the g x IC construction: it charges the '
            f'nominal rate against the whole capital base and buys no capacity at all.')
    cyc, oog = record.get('implied_cycle_years'), record.get('one_over_g')
    if cyc and oog and abs(cyc / oog - 1.0) < 0.02:
        raise TerminalRefused(
            f'the implied replacement cycle is {cyc:.1f} years against 1/g of {oog:.1f} — '
            f'they agree, which is the signature of a g x IC charge. The implied asset life '
            f'is the reciprocal of the inflation rate and that is not a fact about the asset.')
