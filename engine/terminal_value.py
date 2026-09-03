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
  * real growth capex is charged at the incremental capital the REAL growth needs, and only
    that. Zero real growth costs zero growth capex.
  * working capital grows with the price level, so pi x WC is a real cash cost of inflation
    and IS charged.

THE FLOOR, which needs no opinion and cannot be tuned because it has no parameters. A
company can always decline to invest beyond maintenance and pay the rest out. So

    TV  >=  NOPAT_last / W

A terminal below that is dominated by a policy the company can choose unilaterally, and a
study publishing it has chosen the worse of two worlds. This is a dominance argument, not a
judgement. It is returned beside every answer, always, and `assert_terminal()` refuses a
record that sits below it without a DISCLOSED CONTRACTUAL OBLIGATION to keep spending — a
concession, a licence condition or a take-or-pay, named and sourced, because that is the
only circumstance in which the no-investment option is genuinely unavailable.

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
        if not i.useful_life_years:
            raise TerminalRefused('escalating book D&A needs the life to escalate it over')
        maint = i.dna_book * (1.0 + i.inflation) ** (float(i.useful_life_years) / 2.0)
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

    tv    = fcff * (1.0 + g) / (i.wacc - g)
    floor = i.nopat / i.wacc
    below = tv < floor
    if below and i.floor_exemption not in FLOOR_EXEMPTIONS:
        raise TerminalRefused(
            f'terminal of {tv:,.1f} sits BELOW its own floor of {floor:,.1f} '
            f'({tv/floor - 1:+.1%}). A company can always decline to invest and pay out '
            f'instead, so this terminal is dominated by a policy it can choose '
            f'unilaterally. Publishing it chooses the worse of two worlds. To sit below the '
            f'floor a record must name a DISCLOSED obligation to keep spending, one of '
            f'{FLOOR_EXEMPTIONS}, with the disclosure that establishes it.')
    if below and not i.floor_exemption_disclosure:
        raise TerminalRefused(
            f'floor exemption {i.floor_exemption!r} carries no disclosure. An obligation '
            f'asserted is not an obligation.')

    charge = maint + growth_capex + wc_charge - i.dna_book
    cycle  = (i.ic_replacement / charge) if (i.ic_replacement and charge > 0) else None
    t = Terminal(fcff=fcff, tv=tv, floor=floor, nominal_growth=g, maintenance=maint,
                 growth_capex=growth_capex, wc_charge=wc_charge, dna_addback=i.dna_book,
                 implied_cycle_years=cycle, below_floor=below)
    t.record = dict(
        rule='R-TERM-01', inputs=asdict(i), fcff=fcff, tv=tv, floor=floor,
        tv_vs_floor=tv / floor - 1.0, nominal_growth=g, real_growth=i.real_growth,
        maintenance=maint, growth_capex=growth_capex, wc_charge=wc_charge,
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
    tv, floor = float(record['tv']), float(record['floor'])
    if tv < floor and record.get('floor_exemption') not in FLOOR_EXEMPTIONS:
        raise TerminalRefused(
            f'terminal {tv:,.1f} is below its floor {floor:,.1f} ({tv/floor-1:+.1%}) with '
            f'no disclosed obligation to keep spending')
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
    cyc, oog = record.get('implied_cycle_years'), record.get('one_over_g')
    if cyc and oog and abs(cyc / oog - 1.0) < 0.02:
        raise TerminalRefused(
            f'the implied replacement cycle is {cyc:.1f} years against 1/g of {oog:.1f} — '
            f'they agree, which is the signature of a g x IC charge. The implied asset life '
            f'is the reciprocal of the inflation rate and that is not a fact about the asset.')
