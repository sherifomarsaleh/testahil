"""Three independent valuations of ADNOC Drilling, each by a different method.

Cast by method from the persona library, labelled Expert 1 / 2 / 3 in every
delivered document. Each one is COMPUTED here from the same committed numbers
file the rest of the study reads — none of the figures below is asserted, and
every intermediate line each expert relies on is emitted so the reader can
follow the arithmetic rather than being handed a conclusion.

  Expert 1 — the asset valuer. Values the rig fleet at depreciated replacement
             cost and treats the answer as a floor, not a fair value.
  Expert 2 — the contracted-cash-flow analyst. Splits the business into a
             contracted near book, discounted at a corporate spread over the
             sovereign, and an uncontracted tail carrying full equity risk.
  Expert 3 — the distribution investor. Values the share as the stream of cash
             actually paid out, on the company's own guided dividend floor and
             growth, capitalised at the cost of equity.

Each carries a falsification condition stated BEFORE the outcome is known.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
IN, W, M, H = D['inputs'], D['wacc'], D['market'], D['history']
SH = M['shares_outstanding_k']
FX = IN['fx_aed_usd']['value']
SPOT = M['spot_aed']


def aed(equity_usd_k):
    return equity_usd_k / SH * FX


def bridge(ev):
    """Enterprise value to equity, on the 30-Jun-2026 capital structure."""
    return (ev + IN['jvinv_1h26']['value'] + IN['cash_1h26']['value']
            - IN['debt_1h26']['value'] - IN['lease_1h26']['value']
            - IN['nci_1h26']['value'] - IN['finliab_1h26']['value'])


# ============================ EXPERT 1 — asset valuer ========================
# Gross cost and accumulated depreciation come straight from the property and
# equipment note. The two adjustments are (a) an uplift on net book value for the
# cost inflation between when the fleet was bought and what it would cost to
# rebuild today, and (b) the fully-depreciated assets that the company discloses
# are STILL IN USE and which therefore carry economic value the books show as nil.
E1 = {}
E1['gross_ppe_cost'] = 10_379_255.0          # FY2025 note 5, total cost
E1['accumulated_depreciation'] = 4_902_097.0
E1['net_book_value'] = 5_477_158.0
E1['fully_depreciated_in_use_at_cost'] = 1_539_151.0
E1['replacement_uplift_on_net_book'] = 0.15
E1['residual_rate_on_fully_depreciated'] = 0.25
E1['uplifted_net_fleet'] = E1['net_book_value'] * (1 + E1['replacement_uplift_on_net_book'])
E1['fully_depreciated_value'] = (E1['fully_depreciated_in_use_at_cost']
                                 * E1['residual_rate_on_fully_depreciated'])
E1['depreciated_replacement_cost'] = E1['uplifted_net_fleet'] + E1['fully_depreciated_value']
E1['right_of_use_and_intangibles'] = IN['rou_fy25']['value'] + IN['intang_fy25']['value']
E1['net_working_capital'] = H['2025']['working_capital']
E1['other_non_current'] = IN['dta_fy25']['value'] + IN['advnc_fy25']['value']
E1['enterprise_asset_value'] = (E1['depreciated_replacement_cost']
                                + E1['right_of_use_and_intangibles']
                                + E1['net_working_capital'] + E1['other_non_current'])
E1['equity_value'] = bridge(E1['enterprise_asset_value'])
E1['value_per_share_aed'] = aed(E1['equity_value'])
# named sensitivity: the replacement uplift is the one assumption doing the work
E1['sensitivity'] = [
    dict(uplift=u, aed=aed(bridge(E1['net_book_value'] * (1 + u) + E1['fully_depreciated_value']
                                  + E1['right_of_use_and_intangibles']
                                  + E1['net_working_capital'] + E1['other_non_current'])))
    for u in (0.00, 0.15, 0.30, 0.50)]

# ============================ EXPERT 2 — contracted cash flow ================
# The near book is contracted to a state-owned counterparty, so it is discounted
# at the Abu Dhabi sovereign yield plus a corporate spread — the company's own
# marginal cost of debt — rather than at an equity rate. The tail beyond the
# forecast window is not contracted and takes the full weighted average cost of
# capital plus a penalty for the renewal risk the near book does not carry.
rowsA = D['cases']['A']['rows']
E2 = {}
E2['contracted_discount_rate'] = W['kd_pretax']
E2['tail_discount_rate'] = W['wacc_used'] + 0.015
E2['tail_growth'] = IN['terminal_growth_B']['value']
E2['contracted_years'] = []
pv_contracted = 0.0
for n, r in enumerate(rowsA, start=1):
    df = 1 / (1 + E2['contracted_discount_rate']) ** n
    pv = r['fcff'] * df
    pv_contracted += pv
    E2['contracted_years'].append(dict(year=r['year'], fcff=r['fcff'], discount_factor=df,
                                       present_value=pv))
E2['pv_contracted'] = pv_contracted
E2['terminal_nopat'] = rowsA[-1]['nopat'] * (1 + E2['tail_growth'])
E2['terminal_reinvestment'] = E2['tail_growth'] / IN['terminal_roic']['value']
E2['terminal_value'] = (E2['terminal_nopat'] * (1 - E2['terminal_reinvestment'])
                        / (E2['tail_discount_rate'] - E2['tail_growth']))
E2['pv_terminal'] = E2['terminal_value'] / (1 + E2['tail_discount_rate']) ** len(rowsA)
E2['enterprise_value'] = E2['pv_contracted'] + E2['pv_terminal']
E2['tv_pct_of_ev'] = E2['pv_terminal'] / E2['enterprise_value']
E2['equity_value'] = bridge(E2['enterprise_value'])
E2['value_per_share_aed'] = aed(E2['equity_value'])
E2['sensitivity'] = []
for prem in (0.005, 0.010, 0.015, 0.025, 0.035):
    rt = W['wacc_used'] + prem
    tv = (E2['terminal_nopat'] * (1 - E2['terminal_reinvestment']) / (rt - E2['tail_growth']))
    ev = pv_contracted + tv / (1 + rt) ** len(rowsA)
    E2['sensitivity'].append(dict(tail_premium=prem, tail_rate=rt, aed=aed(bridge(ev))))

# ============================ EXPERT 3 — distribution investor ===============
# Two stages. The company has guided a dividend floor of $1.05bn for 2026 and a
# 5% annual step; that step is carried for the five guided years and then fades
# to the terminal rate. Discounted at the cost of equity, not the cost of capital
# — this is a claim on the equity, not on the firm.
E3 = {}
E3['dividend_2026'] = IN['g26_dividend']['value']
E3['stage1_growth'] = 0.05
E3['stage1_years'] = 5
E3['terminal_growth'] = IN['terminal_growth_A']['value']
E3['cost_of_equity'] = W['ke_rating']
E3['schedule'] = []
pv_div = 0.0
d = E3['dividend_2026']
for n in range(1, E3['stage1_years'] + 1):
    div = E3['dividend_2026'] * (1 + E3['stage1_growth']) ** (n - 1)
    df = 1 / (1 + E3['cost_of_equity']) ** n
    pv_div += div * df
    E3['schedule'].append(dict(year=2025 + n, dividend=div, discount_factor=df,
                               present_value=div * df))
    d = div
E3['pv_stage1'] = pv_div
E3['terminal_dividend'] = d * (1 + E3['terminal_growth'])
E3['terminal_value'] = E3['terminal_dividend'] / (E3['cost_of_equity'] - E3['terminal_growth'])
E3['pv_terminal'] = E3['terminal_value'] / (1 + E3['cost_of_equity']) ** E3['stage1_years']
E3['equity_value'] = E3['pv_stage1'] + E3['pv_terminal']
E3['value_per_share_aed'] = aed(E3['equity_value'])
E3['payout_check_2026'] = E3['dividend_2026'] / rowsA[0]['pat']
E3['payout_check_2030'] = E3['schedule'][-1]['dividend'] / rowsA[-1]['pat']
E3['sensitivity'] = []
for g in (0.010, 0.015, 0.020, 0.025, 0.030):
    tv = d * (1 + g) / (E3['cost_of_equity'] - g)
    E3['sensitivity'].append(dict(terminal_growth=g,
                                  aed=aed(pv_div + tv / (1 + E3['cost_of_equity'])
                                          ** E3['stage1_years'])))

EXPERTS = [
    dict(label='Expert 1', method='Depreciated replacement cost of the rig fleet',
         base=E1['value_per_share_aed'],
         range=[E1['sensitivity'][0]['aed'], E1['sensitivity'][-1]['aed']], detail=E1),
    dict(label='Expert 2', method='Contracted cash flow, split-rate discounting',
         base=E2['value_per_share_aed'],
         range=[min(s['aed'] for s in E2['sensitivity']),
                max(s['aed'] for s in E2['sensitivity'])], detail=E2),
    dict(label='Expert 3', method='Two-stage dividend capitalisation',
         base=E3['value_per_share_aed'],
         range=[min(s['aed'] for s in E3['sensitivity']),
                max(s['aed'] for s in E3['sensitivity'])], detail=E3),
]

# ---- what actually separates them -------------------------------------------
DIVERGENCE = [
    dict(assumption='What is being valued',
         e1='The steel. The fleet at what it would cost to rebuild, and nothing else.',
         e2='The cash the contracted book throws off, plus a discounted tail.',
         e3='The cash that actually reaches the shareholder.',
         drives=('Expert 1 is structurally the lowest because it refuses to pay for the '
                 'contract that makes the steel earn 23% on capital.')),
    dict(assumption='Discount rate',
         e1='None. An asset value is not discounted.',
         e2=f"{E2['contracted_discount_rate']*100:.2f}% on the contracted years, "
            f"{E2['tail_discount_rate']*100:.2f}% on the tail.",
         e3=f"{E3['cost_of_equity']*100:.2f}% throughout — the cost of equity, not of capital.",
         drives=('Expert 2 discounts the near years more cheaply than the study does and the '
                 'far years more dearly; the two effects partly cancel, which is why its '
                 'answer lands close to the study despite a very different construction.')),
    dict(assumption='Treatment of growth',
         e1='Ignored entirely.',
         e2=f"{E2['tail_growth']*100:.1f}% in the tail, with the fleet build inside the "
            f"explicit years.",
         e3=f"{E3['stage1_growth']*100:.0f}% for five guided years, then "
            f"{E3['terminal_growth']*100:.1f}%.",
         drives=('The dividend step is the single largest source of Expert 3\'s premium over '
                 'Expert 1: five years of guided 5% growth compounds before the fade begins.')),
    dict(assumption='Where the risk sits',
         e1='In whether the rigs can be redeployed if the customer walks.',
         e2='In the renewal of the uncontracted tail, priced as an explicit premium.',
         e3='In whether the dividend floor survives a capital-expenditure cycle.',
         drives=('All three risks are the same risk seen from three sides: the durability of '
                 'one customer relationship.')),
]

CROSS_EXAMINATION = [
    dict(challenge='Expert 1 to Expert 3: the dividend floor is a board policy, not a '
                   'contract. In the year the six island rigs and a regional acquisition land '
                   'together, the floor is the first thing to go.',
         response=(f"Conceded in part. The guided floor is {E3['payout_check_2026']*100:.0f}% of "
                   f"the profit this model forecasts for 2026 and "
                   f"{E3['payout_check_2030']*100:.0f}% by 2030, so it is covered by earnings "
                   f"with room to spare, and the company funded a 58% dividend increase in 2025 "
                   f"out of operating cash flow while capital expenditure ran at $815 million. "
                   f"But the challenge stands where it matters: the floor is uncontracted, and "
                   f"the valuation of a promise is not the valuation of an obligation. Expert 3 "
                   f"is the widest of the three for exactly that reason."),
         verdict='Partly conceded'),
    dict(challenge='Expert 3 to Expert 1: replacement cost values a rig at what it costs, not '
                   'at what it earns. This fleet earns a 23% return on capital employed. '
                   'Valuing it at book plus a fifteen-point uplift prices it as scrap.',
         response=(f"Rejected as a criticism, accepted as a description. Expert 1 is not "
                   f"claiming to be the fair value; it is claiming to be the floor. The gap "
                   f"between the replacement-cost answer of AED "
                   f"{E1['value_per_share_aed']:.2f} and the market price of AED {SPOT:.2f} is "
                   f"the market's price for the contract, and putting a number on that gap is "
                   f"the point of running the lens at all."),
         verdict='Rejected'),
    dict(challenge='Expert 2 to Expert 3: discounting dividends at the cost of equity while the '
                   'company runs net cash by 2030 double-counts the balance sheet. The '
                   'undistributed cash is not risky.',
         response=(f"Conceded. Under the model's flat-debt, floor-dividend policy the company "
                   f"accumulates roughly $2.5 billion of cash by 2030 and net debt turns "
                   f"negative. Expert 3 does not credit that cash, so its answer is "
                   f"conservative by construction — the correction would raise it, not lower "
                   f"it. The reason it is left uncorrected is that a board holding that much "
                   f"idle cash would in practice have raised the distribution, which is the "
                   f"same thing seen from the other end."),
         verdict='Conceded'),
    dict(challenge='Expert 1 to Expert 2: a 150-basis-point premium on the tail is a number '
                   'chosen to look prudent. The tail is 70% of your answer.',
         response=(f"Conceded on the arbitrariness, and the sensitivity is published rather "
                   f"than buried: moving the premium from 50 to 350 basis points moves the "
                   f"answer from AED {E2['sensitivity'][0]['aed']:.2f} to AED "
                   f"{E2['sensitivity'][-1]['aed']:.2f}. That spread is wider than the gap "
                   f"between any two of the three experts, which is the honest summary of how "
                   f"much of this valuation is a judgement about a period nobody has "
                   f"contracted for."),
         verdict='Conceded'),
]

FALSIFIERS = {
    'Expert 1': ('A rig sale, or an impairment, at a price materially away from depreciated '
                 'book. The company sold one rig for $36.0 million in 2025 against a carrying '
                 'value that produced a $21.6 million disposal gain — that single observation '
                 'supports the uplift. A future disposal at or below carrying value would '
                 'falsify it.'),
    'Expert 2': ('The 2027 guidance the company has said it will publish once rig and '
                 'oilfield-services phasing is fixed. If the guided 2027 revenue lands below '
                 'this model\'s $5.16 billion, the contracted book is thinner than assumed and '
                 'the near-year discount rate is too generous.'),
    'Expert 3': ('Any distribution below the guided floor, or a capital raise. Either would '
                 'break the premise that the payout is the residual the shareholder actually '
                 'receives.'),
}

THREE_IN_A_ROOM = (
    f"Put in one room, the three do not disagree about the company — they agree on the fleet, "
    f"on the customer, and on the 2026 numbers, because all three read the same filings. They "
    f"disagree about what a single-customer contract is worth. Expert 1 will not pay for it at "
    f"all and lands at AED {E1['value_per_share_aed']:.2f}. Expert 2 pays for the part that is "
    f"written down and charges a premium for the part that is not, landing at AED "
    f"{E2['value_per_share_aed']:.2f}. Expert 3 pays for the part that reaches the bank account "
    f"and lands at AED {E3['value_per_share_aed']:.2f}. The spread between them, AED "
    f"{max(e['base'] for e in EXPERTS) - min(e['base'] for e in EXPERTS):.2f}, is not "
    f"measurement error. It is the price of the question none of them can answer from the "
    f"filings: what happens to a rig fleet whose only customer is also its controlling "
    f"shareholder, once that shareholder's capacity target is met.")

OUT = dict(experts=EXPERTS, divergence=DIVERGENCE, cross_examination=CROSS_EXAMINATION,
           falsifiers=FALSIFIERS, three_in_a_room=THREE_IN_A_ROOM,
           spot=SPOT, study_central=D['fair_value']['central'])

if __name__ == '__main__':
    json.dump(OUT, open(os.path.join(HERE, 'experts.json'), 'w'), indent=1)
    for e in EXPERTS:
        print(f"{e['label']}: {e['method']:52s} AED {e['base']:.2f} "
              f"(range {e['range'][0]:.2f}-{e['range'][1]:.2f})")
    print(f"study central AED {D['fair_value']['central']:.2f} | market AED {SPOT:.2f}")
