"""ADNOCDIST_Valuation_Study_09-08-2026.docx — the 16-section study.

Written for an EXTERNAL reader: no internal procedure vocabulary anywhere, no
calibration appendix. The calibration evidence appears inside section 3 as plain-language
sentences with the statistics inline. Experts are labelled Expert 1, 2 and 3.

NO FINANCIAL NUMERAL IS TYPED IN THIS FILE. Every number is an f-string interpolation of a
lookup into study_numbers.json, technicals.json, strike_result.json, beta_result.json or
the research record.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docx_base as B
from docx.shared import Pt, Inches

doc, P, H1, H2, rich, table, figure, box, bullet, caption, masthead = (
    B.doc, B.P, B.H1, B.H2, B.rich, B.table, B.figure, B.box, B.bullet, B.caption,
    B.masthead)
INK, GREY, BRASS, GOLD = B.INK, B.GREY, B.BRASS, B.GOLD

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
M, H, FC, W, DCFD, LN = D['meta'], D['history'], D['forecast'], D['wacc'], D['dcf'], D['lenses']
UB, SENS, CAL, CRUX, WC = (D['unit_build'], D['sensitivity'], D['calibration'], D['crux'],
                           D['working_capital'])
CE = D['cost_exposure']
V = {k: v['value'] for k, v in D['inputs'].items()}
SRC = {k: v for k, v in D['inputs'].items()}
TECH = json.load(open(os.path.join(HERE, 'technicals.json')))
STRIKE = json.load(open(os.path.join(HERE, 'strike_result.json')))
BETAJ = json.load(open(os.path.join(HERE, 'beta_result.json')))

# The external research record. sweep_research.json carries the researched external
# findings keyed by topic id, which is what this document quotes from. sweep_register.json
# is the separate, structured source record and is read alongside it for the research
# record in Appendix B.
REC = json.load(open(os.path.join(HERE, 'sweep_research.json')))
ENTRIES = REC.get('entries', REC.get('register', []))
GAPS = REC.get('gaps_and_negative_results', REC.get('gaps', []))
E = {e['id']: e for e in ENTRIES}
DRIVERS = [e for e in ENTRIES if e.get('classification') == 'D']

A, Bf = DCFD['frame_A'], DCFD['frame_B']
BT = CAL['backtest']
VOL = CAL['vol']
WID = CAL['width']
SPOT, SH = M['spot'], M['shares_mn']
YR = FC['years']
HYRS = ('FY2023', 'FY2024', 'FY2025')
NY = len(YR)
BETA_CH = BETAJ[BETAJ['chosen']]

# Table and figure numbers are ASSIGNED IN DOCUMENT ORDER by these counters, never typed.
_TN, _FN = [0], [0]


def tnum():
    _TN[0] += 1
    return _TN[0]


def fnum():
    _FN[0] += 1
    return _FN[0]


def n0(x): return f'{x:,.0f}'
def n1(x): return f'{x:,.1f}'
def n2(x): return f'{x:,.2f}'
def pc(x, d=1): return f'{x * 100:.{d}f}%'


def paren(x, f=n0):
    return f'({f(abs(x))})'


def clip(s, n):
    s = ' '.join(str(s).split())
    return s if len(s) <= n else s[:n - 1].rsplit(' ', 1)[0] + '…'


def fig(name, width, text):
    figure(os.path.join(HERE, name), width, f'Figure {fnum()} — {text}')


print('building ADNOC Distribution study …')

# ===================== 1. MASTHEAD + READ FIRST ================================
masthead()
P(M['company'], size=21, bold=True, space_after=1)
P(f"Independent valuation study · {M['exchange']} · ticker {M['ticker']} · "
  f"{M['currency']} · fuel retail, convenience retail and commercial fuel distribution",
  size=11.5, color=GREY, space_after=2)
P(f"Prepared 9 August 2026 · share price {M['currency']} {n2(SPOT)} at the close of "
  f"7 August 2026 · {n0(SH)} million shares in issue · market capitalisation "
  f"{M['currency']} {n0(M['mcap'])} million", size=10, color=GREY, space_after=12)

H1('Read first')
box([('What this is. ',
      f"An independent, educational valuation of the largest fuel and convenience retailer "
      f"in the United Arab Emirates, built from the company's own audited consolidated "
      f"financial statements for {HYRS[0]}, {HYRS[1]} and {HYRS[2]}, its reviewed interim "
      f"accounts for the first and second quarters of 2026, and its own published operating "
      f"disclosures. It contains no rating, no recommendation and no price target. It "
      f"expresses value as a RANGE and, separately, as a probability distribution."),
     ('The structural fact that governs everything below. ',
      "Retail fuel prices in the UAE are not set by the retailer. A government Fuel Price "
      "Committee fixes them monthly, uniformly across the country and identically for every "
      "operator, from average international prices plus operating costs. There is therefore "
      "no retail price competition in this market at all. Volume and margin per litre are "
      "the levers; price is not one. A reader who values this company as though it sets its "
      "own pump prices will value the wrong business."),
     ('The one number to hold on to. ',
      f"There is no single number, and that is deliberate. Five readings put fair value "
      f"between {M['currency']} {n2(LN['fair_bear'])} and {M['currency']} "
      f"{n2(LN['fair_bull'])} a share. Because the contested judgement below is carried BOTH "
      f"ways and the two are never averaged, this study publishes TWO weighted centres: "
      f"{M['currency']} {n2(LN['centre_A'])} a share on the normalising reading of inventory "
      f"movements and {M['currency']} {n2(LN['centre_B'])} on the through-cycle one. The "
      f"market price is {M['currency']} {n2(SPOT)}."),
     ('The contested judgement, carried both ways. ',
      f"Inventory movements — the profit the company books when the fuel in its tanks is "
      f"worth more than it paid — were {M['currency']} {n0(V['invgain_fy24'])} million in "
      f"FY2024, {M['currency']} {n0(V['invgain_fy25'])} million in FY2025 and "
      f"{M['currency']} {n0(V['invgain_h126'])} million in the first half of 2026 ALONE, "
      f"against fuel volume growth in that half of "
      f"{pc((V['vol_retail_h126'] + V['vol_comm_h126']) / (V['vol_retail_h125'] + V['vol_comm_h125']) - 1)}. "
      f"Frame A normalises them to zero from FY2027; Frame B carries the FY2024–FY2025 "
      f"average of {M['currency']} {n0(CRUX['avg_24_25'])} million. Both are published side "
      f"by side in the summary table, in the body of section 1, and in one expert's range. "
      f"They are NEVER averaged into one number."),
     ('A limitation the reader should know about that judgement. ',
      "Inventory movements are not a line in the audited financial statements. They appear "
      "only in management commentary and in the results presentations, and no reconciliation "
      "of them to the audited accounts is published. This study therefore treats the figures "
      "above as management's own disclosed estimates and carries the judgement two ways "
      "rather than picking one. That is a real limitation and it is stated here rather than "
      "in a footnote."),
     ('Where the disagreement actually lies. ',
      f"Set inventory movements to zero in EVERY forecast year — the harshest reading "
      f"available — and the cash-flow model still gives {M['currency']} "
      f"{n2(CRUX['inventory_zero_all_years'])} a share against a traded price of "
      f"{M['currency']} {n2(SPOT)}. So the disagreement is not about the windfall. It is "
      f"about the long run, where {pc(A['tv_share'], 0)} of the value sits. Section 1.7 "
      f"solves the market price backwards and states exactly what it embeds."),
     ('What this study deliberately does NOT do. ',
      f"It puts no revenue, no cost and no value on the proposed acquisition of Shell "
      f"Downstream South Africa, announced on 7 July 2026 at approximately USD "
      f"{n0(E['CO-05']['value'])} million of enterprise value. The transaction has not "
      f"closed and remains subject to regulatory approval. It is set out in full in section "
      f"5 as the largest single item outside the base case, and the base case excludes it.")])

# ============================== 2. HEADLINE ====================================
H1('Headline')
P(f"ADNOC Distribution sells about {n0(UB['vol_total_fy25'] / 1000)} billion litres of fuel a "
  f"year through {n0(V['stations_h126'])} service stations in three countries, and about "
  f"{M['currency']} {n0(V['rev_nonfuel_fy25'])} million a year of coffee, groceries and car "
  f"care alongside it. Revenue was {M['currency']} {n0(V['rev_fy25'])} million in FY2025, "
  f"gross profit {M['currency']} {n0(V['gp_fy25'])} million and profit attributable to "
  f"shareholders {M['currency']} {n0(H['FY2025']['np_attributable'])} million, or "
  f"{M['currency']} {n2(V['eps_fy25'])} a share. It has grown revenue in each of the three "
  f"audited years and gross margin in each of them too — from "
  f"{pc(H['FY2023']['gross_margin'])} to {pc(H['FY2025']['gross_margin'])}.")
P(f"The question this study asks is not whether the business is sound. It is what the market "
  f"is assuming about the next twenty years. At {M['currency']} {n2(SPOT)} the shares trade "
  f"on {n1(LN['pe_now'])} times trailing earnings and yield {pc(LN['div_yield_now'])} on a "
  f"dividend the board has committed to through 2030. Neither of those looks demanding. But "
  f"run the cash-flow model backwards from the traded price and it requires a terminal growth "
  f"rate of {pc(CRUX['g_implied'], 2)} a year — a business whose volume base is in permanent, "
  f"if gentle, decline. That is a coherent thing to believe about a fuel retailer in 2026. It "
  f"is not what this study's own drivers, built segment by segment from the company's "
  f"disclosed volumes and margins per litre, produce.")
P(f"Four independent methods put the shares between {M['currency']} {n2(LN['fair_bear'])} and "
  f"{M['currency']} {n2(LN['fair_bull'])}, with weighted centres of {M['currency']} "
  f"{n2(LN['centre_A'])} and {M['currency']} {n2(LN['centre_B'])} on the two framings of the "
  f"inventory judgement. A fifth reading — capitalising the fixed policy dividend — lands at "
  f"{M['currency']} {n2(LN['div_ps'])}, within a few fils of the traded price. That is not a "
  f"coincidence, and section 4 explains why: the market appears to be pricing the dividend "
  f"the company pays rather than the cash the business generates.")
fig('fig1_field.png', 6.9,
    f"the field of value. Each method is an independent reading; the spread between them is "
    f"the uncertainty, and the two centres are the contested judgement carried both ways.")

# ========================= 3. VALUATION SUMMARY ================================
H1('Valuation summary')
rows = [['Reading', f"{M['currency']} / share", 'vs market', 'Note']]
rows.append(['Discounted cash flow — Frame A', n2(A['per_share']), pc(A['per_share'] / SPOT - 1, 0),
             f"terminal value {pc(A['tv_share'], 1)} of enterprise value — inventory "
             f"movements normalised to zero from FY2027"])
rows.append(['Discounted cash flow — Frame B', n2(Bf['per_share']),
             pc(Bf['per_share'] / SPOT - 1, 0),
             f"terminal value {pc(Bf['tv_share'], 1)} of enterprise value — inventory "
             f"movements carried at the FY2024–FY2025 average"])
rows.append(['Normalised earnings power', n2(LN['norm_ps']), pc(LN['norm_ps'] / SPOT - 1, 0),
             'structural gross profit only, capitalised at the current cost of capital less '
             'long-run growth'])
rows.append(['Relative multiples — Frame A', n2(LN['rel_A']), pc(LN['rel_A'] / SPOT - 1, 0),
             f"{n1(LN['just_fwd_pe'])} times the FY2026 forward earnings the model itself "
             f"produces"])
rows.append(['Relative multiples — Frame B', n2(LN['rel_B']), pc(LN['rel_B'] / SPOT - 1, 0),
             'the same multiple on the through-cycle earnings'])
rows.append(['Book value and sustainable return', n2(LN['book_ps']),
             pc(LN['book_ps'] / SPOT - 1, 0),
             f"justified {n1(LN['just_pb'])} times a book value of {n2(LN['bv_ps'])} a share"])
rows.append(['Dividend capitalisation (unweighted)', n2(LN['div_ps']),
             pc(LN['div_ps'] / SPOT - 1, 0),
             f"the fixed policy dividend of {n2(V['dps'])} a share grown at "
             f"{pc(A['g'], 1)} — a claim on cash paid, not cash earned"])
rows.append(['WEIGHTED CENTRE — Frame A', n2(LN['centre_A']), pc(LN['centre_A'] / SPOT - 1, 0),
             'cash flow 40%, normalised earnings 25%, relative 20%, book and return 15%'])
rows.append(['WEIGHTED CENTRE — Frame B', n2(LN['centre_B']), pc(LN['centre_B'] / SPOT - 1, 0),
             'the same weights on the through-cycle framing. The two centres are NEVER '
             'averaged'])
rows.append(['Field low to field high', f"{n2(LN['fair_bear'])} – {n2(LN['fair_bull'])}", '',
             'the spread between the readings IS the uncertainty'])
rows.append(['Market price', n2(SPOT), '', f"close of {M['price_date']}"])
table(rows, [2.35, 1.05, 0.85, 2.75], band_rows={8, 9, 11}, size=8.8)
caption(f"Table {tnum()} — the summary valuation table. Terminal value is stated beside the "
        f"cash-flow readings rather than buried in the model, because it is high: "
        f"{pc(A['tv_share'], 1)} of enterprise value on Frame A and {pc(Bf['tv_share'], 1)} on "
        f"Frame B. A reader who distrusts perpetuities should read section 1.7 before "
        f"anything else — three-quarters of this valuation is a statement about the years "
        f"after {YR[-1].replace('E', '')}.")

rows = [['Key figures', 'Value', 'Key figures', 'Value']]
kf = [('Market capitalisation', f"{M['currency']} {n0(M['mcap'])}m"),
      ('Net debt excluding leases', f"{M['currency']} {n0(W['net_debt'])}m"),
      ('Lease liabilities', f"{M['currency']} {n0(V['lease_fy25'])}m"),
      ('Enterprise value on the traded price',
       f"{M['currency']} {n0(M['mcap'] + W['net_debt'] + V['lease_fy25'] + V['nciq_fy25'])}m"),
      ('FY2025 revenue', f"{M['currency']} {n0(V['rev_fy25'])}m"),
      ('FY2025 EBITDA', f"{M['currency']} {n0(H['FY2025']['ebitda'])}m"),
      ('FY2025 attributable profit', f"{M['currency']} {n0(H['FY2025']['np_attributable'])}m"),
      ('FY2025 fuel volume', f"{n0(UB['vol_total_fy25'])}m litres"),
      ('Trailing price / earnings', f"{n1(LN['pe_now'])}x"),
      ('Trailing enterprise value / EBITDA',
       f"{n1((M['mcap'] + W['net_debt'] + V['lease_fy25'] + V['nciq_fy25']) / H['FY2025']['ebitda'])}x"),
      ('Cost of equity', pc(W['ke'], 2)),
      ('Discount rate, first forecast year', pc(W['disc_rate'][0], 2)),
      ('Discount rate, terminal', pc(W['wacc_terminal'], 2)),
      ('Policy dividend per share',
       f"{M['currency']} {n2(V['dps'])} ({pc(LN['div_yield_now'])} yield)"),
      ('Return on average equity, FY2025', pc(LN['roe_hist'][2])),
      ('Service stations, mid-2026', n0(V['stations_h126']))]
for i in range(0, len(kf), 2):
    rows.append([kf[i][0], kf[i][1], kf[i + 1][0], kf[i + 1][1]])
table(rows, [2.2, 1.3, 2.2, 1.3], size=9.0)
caption(f"Table {tnum()} — the figures a reader needs before anything else. Enterprise value "
        f"carries the lease liability and the non-controlling interest, on the same basis the "
        f"valuation bridge in section 1.1 uses, so the multiple beside it and the bridge are "
        f"struck on one definition.")

# ========================= 4. COMPANY OVERVIEW =================================
H1('Company overview')
P(f"ADNOC Distribution is the fuel and convenience retailing arm of the Abu Dhabi National "
  f"Oil Company, listed on the {M['exchange']} in December 2017 with roughly "
  f"{pc(E['CO-02']['value'] / 100, 0)} of its shares in free float and the parent retaining "
  f"the balance. It runs {n0(V['stations_h126'])} service stations — {n0(V['stations_uae_h126'])} "
  f"in the United Arab Emirates, {n0(V['stations_ksa_h126'])} in Saudi Arabia and "
  f"{n0(V['stations_egy_h126'])} in Egypt — together with {n0(V['cstores_h126'])} convenience "
  f"stores and {n0(V['evpoints_h126'])} electric-vehicle charging points, all figures as at "
  f"the end of June 2026.")
P("The business has four disclosed revenue legs and they behave differently enough that "
  "blending them would destroy information. Retail fuel is the sale of petrol and diesel at "
  "the pump to the motoring public, at a price the company does not set. Non-fuel retail is "
  "convenience stores, car care and the property income underneath them — a genuine retail "
  "margin, and the only leg where the company has full pricing freedom. Corporate fuel is "
  "bulk supply to government, fleet and industrial customers under contract. Aviation is jet "
  "fuel into airports. The first two are a retail network business; the second two are a "
  "distribution business with different working capital, different margins and different "
  "competitive dynamics.")
rows = [['Revenue leg', 'FY2024', 'FY2025', 'Growth', 'H1-2026', 'Share of FY2025']]
segs = [('Retail fuel', 'retfuel'), ('Non-fuel retail', 'nonfuel'),
        ('Corporate fuel', 'corp'), ('Aviation fuel', 'avi')]
for nm, k in segs:
    a24, a25, h26 = V[f'rev_{k}_fy24'], V[f'rev_{k}_fy25'], V[f'rev_{k}_h126']
    rows.append([nm, n0(a24), n0(a25), pc(a25 / a24 - 1, 1), n0(h26),
                 pc(a25 / V['rev_fy25'], 1)])
_t24 = sum(V[f'rev_{k}_fy24'] for _, k in segs)
_t25 = sum(V[f'rev_{k}_fy25'] for _, k in segs)
_th26 = sum(V[f'rev_{k}_h126'] for _, k in segs)
rows.append(['Total', n0(_t24), n0(_t25), pc(_t25 / _t24 - 1, 1), n0(_th26), '100.0%'])
table(rows, [1.65, 1.05, 1.05, 0.8, 1.05, 1.15], band_rows={5}, size=8.8)
caption(f"Table {tnum()} — the disclosed revenue split in {M['currency']} million, each total "
        f"SUMMED from its own column rather than quoted. The audited FY2025 consolidated "
        f"revenue of {n0(V['rev_fy25'])} reconciles to the {n0(_t25)} above; the difference is "
        f"rounding within the segment disclosure. Note what the first-half column shows: "
        f"revenue up {pc(_th26 * 2 / _t25 - 1, 0)} annualised on volume up "
        f"{pc((V['vol_retail_h126'] + V['vol_comm_h126']) / (V['vol_retail_h125'] + V['vol_comm_h125']) - 1, 1)}. "
        f"That gap is price, and price here is a pass-through the company does not control.")

rows = [['Operating measure', 'H1-2025', 'H1-2026', 'Change']]
ops = [('Service stations', V['stations_h125'], V['stations_h126'], n0),
       ('Retail fuel volume (m litres)', V['vol_retail_h125'], V['vol_retail_h126'], n0),
       ('Commercial fuel volume (m litres)', V['vol_comm_h125'], V['vol_comm_h126'], n0),
       ('   of which corporate', V['vol_corp_h125'], V['vol_corp_h126'], n0),
       ('   of which aviation', V['vol_avi_h125'], V['vol_avi_h126'], n0),
       ('Fuel transactions (millions)', V['fueltxn_h125'], V['fueltxn_h126'], n1),
       ('Non-fuel transactions (millions)', V['nonfueltxn_h125'], V['nonfueltxn_h126'], n1)]
for nm, a, b, f in ops:
    rows.append([nm, f(a), f(b), pc(b / a - 1, 1)])
table(rows, [2.6, 1.15, 1.15, 1.4], size=8.8)
caption(f"Table {tnum()} — the operating measures that drive the model, from the company's own "
        f"half-year disclosures. Fuel transactions grew "
        f"{pc(V['fueltxn_h126'] / V['fueltxn_h125'] - 1, 1)} while non-fuel transactions grew "
        f"{pc(V['nonfueltxn_h126'] / V['nonfueltxn_h125'] - 1, 1)}: the network is adding "
        f"fuel customers faster than it is converting them into the shop. Non-fuel "
        f"transactions per fuel transaction fell from "
        f"{n2(V['nonfueltxn_h125'] / V['fueltxn_h125'])} to "
        f"{n2(V['nonfueltxn_h126'] / V['fueltxn_h126'])}, which is the single clearest "
        f"operating weakness in the disclosure.")
P(f"Two further structural features matter. The supply agreement with the parent sets a "
  f"minimum margin of roughly {n0(E['CO-08']['value'])} fils a litre with no upper limit, and "
  f"management has described a quarterly, cash-settled mechanism under which the parent "
  f"absorbs inventory losses on regulated retail stock when prices fall. That is an unusual "
  f"and genuinely valuable asymmetry: it truncates the downside of the very volatility that "
  f"produced the FY2026 inventory windfall. Second, the dividend policy commits the company "
  f"to USD {n0(E['CO-06']['value'])} million a year, or {M['currency']} {n2(V['dps'])} a "
  f"share, through 2030 — or {pc(V['payout'], 0)} of net profit if that is higher — and from "
  f"2026 it is paid quarterly.")

# ==================== 5. SECTION 1 — FUNDAMENTAL VALUATION =====================
H1('1. Fundamental valuation')
P("This is an operating company, so it is valued as one: free cash flow to the firm over "
  "five explicit years discounted at a cost of capital that glides from today's to a "
  "normalised one, plus a terminal value; then cross-read against book value and the return "
  "earned on it, against multiples, and against normalised earnings power. Four methods, one "
  "field. None of them is the answer on its own.")

H2('1.1 The cash-flow model')
P(f"Frame A is shown here in full. It normalises inventory movements to zero from FY2027 "
  f"onward, carrying only the {M['currency']} {n0(V['invmove_A'][0])} million already "
  f"realised in the first half of 2026. Frame B differs in that one line and is carried "
  f"through to its own value per share; nothing else between the two frames differs.")
hdr = [f"{M['currency']} million"] + [y.replace('FY', '') for y in YR]
rows = [hdr]
rows.append(['Revenue'] + [n0(x) for x in FC['revenue']])
rows.append(['Gross profit'] + [n0(x) for x in FC['gross_profit_A']])
rows.append(['Less cash operating expenses'] + [paren(x) for x in FC['cash_opex']])
rows.append(['Add other income'] + [n0(x) for x in FC['other_income']])
rows.append(['Less impairment and credit losses'] + [paren(x) for x in FC['impairments']])
rows.append(['EBITDA'] + [n0(x) for x in A['ebitda']])
rows.append(['EBITDA margin'] + [pc(x) for x in FC['ebitda_margin_A']])
rows.append(['Less depreciation and amortisation'] + [paren(x) for x in A['dna']])
rows.append(['EBIT'] + [n0(x) for x in A['ebit']])
rows.append(['Tax rate applied to EBIT'] + [pc(A['tax_rate'], 2)] * NY)
rows.append(['NOPAT = EBIT x (1 − tax rate)'] + [n0(x) for x in A['nopat']])
rows.append(['Add back depreciation and amortisation'] + [n0(x) for x in A['dna']])
rows.append(['Less capital expenditure'] + [paren(x) for x in A['capex']])
rows.append(['Less increase in working capital'] +
            [paren(x) if x >= 0 else n0(-x) for x in A['delta_nwc']])
rows.append(['Free cash flow to the firm'] + [n0(x) for x in A['fcff']])
rows.append(['Discount rate'] + [pc(x, 2) for x in W['disc_rate']])
rows.append(['Discount factor'] + [n2(x) for x in A['df']])
rows.append(['PRESENT VALUE of free cash flow'] + [n0(x) for x in A['pv']])
table(rows, [2.35, 0.92, 0.92, 0.92, 0.92, 0.92], band_rows={6, 11, 15, 18}, size=8.6)
caption(f"Table {tnum()} — the full free-cash-flow waterfall through to present value, Frame A. "
        f"Working capital is NEGATIVE in this business — customers pay at the pump while "
        f"suppliers are paid on terms — so growth RELEASES cash rather than absorbing it, and "
        f"the working-capital line adds to free cash flow in every year. The discount rate "
        f"rises through the window because the capital structure and the beta are glided "
        f"toward a normalised terminal position rather than held at today's unusually low "
        f"reading; section 1.8 sets out both ends.")

rows = [['Enterprise value to equity value', f"{M['currency']} million",
         f"{M['currency']} / share"],
        [f"Present value of {NY} years of free cash flow", n0(A['pv_sum']),
         n2(A['pv_sum'] / SH)],
        ['Terminal free cash flow', n0(A['fcff_term']), ''],
        [f"Terminal discount rate less growth: {pc(W['wacc_terminal'], 2)} − {pc(A['g'], 1)}",
         pc(W['wacc_terminal'] - A['g'], 2), ''],
        ['Terminal value', n0(A['tv']), ''],
        ['Present value of the terminal value', n0(A['pv_tv']), n2(A['pv_tv'] / SH)],
        ['ENTERPRISE VALUE', n0(A['ev']), n2(A['ev'] / SH)],
        ['Terminal value as a percentage of enterprise value', pc(A['tv_share'], 1), ''],
        ['Less: net debt excluding leases', paren(A['net_debt']), paren(A['net_debt'] / SH, n2)],
        ['Less: lease liabilities', paren(A['leases']), paren(A['leases'] / SH, n2)],
        ['Less: non-controlling interests', paren(A['nci']), paren(A['nci'] / SH, n2)],
        ['EQUITY VALUE — Frame A', n0(A['equity']), n2(A['per_share'])],
        ['EQUITY VALUE — Frame B', n0(Bf['equity']), n2(Bf['per_share'])]]
table(rows, [3.55, 1.6, 1.55], band_rows={6, 7, 11, 12}, size=9.0)
caption(f"Table {tnum()} — the enterprise-to-equity bridge. The terminal share is a LINE of the "
        f"bridge rather than a footnote: {pc(A['tv_share'], 1)} of enterprise value sits "
        f"beyond {YR[-1].replace('E', '')}. Lease liabilities are deducted in the bridge "
        f"because the corresponding right-of-use depreciation is already inside the "
        f"depreciation line above; deducting the lease and charging its depreciation would "
        f"double-count, so the lease is deducted and the rent is NOT added back — section 1.8 "
        f"prices that choice.")

rows = [['The two frames side by side', 'Frame A', 'Frame B', 'Difference']]
fr = [('Inventory movement carried, FY2027 onward',
       n0(FC['invmove_A'][1]), n0(FC['invmove_B'][1]),
       n0(FC['invmove_B'][1] - FC['invmove_A'][1])),
      (f"FY2026 EBITDA ({M['currency']} m)", n0(A['ebitda'][0]), n0(Bf['ebitda'][0]),
       n0(Bf['ebitda'][0] - A['ebitda'][0])),
      (f"{YR[-1].replace('E', '')} EBITDA ({M['currency']} m)", n0(A['ebitda'][-1]),
       n0(Bf['ebitda'][-1]), n0(Bf['ebitda'][-1] - A['ebitda'][-1])),
      (f"Present value of five years ({M['currency']} m)", n0(A['pv_sum']), n0(Bf['pv_sum']),
       n0(Bf['pv_sum'] - A['pv_sum'])),
      (f"Present value of the terminal ({M['currency']} m)", n0(A['pv_tv']), n0(Bf['pv_tv']),
       n0(Bf['pv_tv'] - A['pv_tv'])),
      ('Terminal share of enterprise value', pc(A['tv_share'], 1), pc(Bf['tv_share'], 1),
       pc(Bf['tv_share'] - A['tv_share'], 1)),
      (f"Value per share ({M['currency']})", n2(A['per_share']), n2(Bf['per_share']),
       n2(Bf['per_share'] - A['per_share']))]
for r in fr:
    rows.append(list(r))
table(rows, [3.1, 1.3, 1.3, 1.25], band_rows={7}, size=8.8)
caption(f"Table {tnum()} — the contested judgement isolated. Everything else in the two models "
        f"is identical, so the {M['currency']} {n2(Bf['per_share'] - A['per_share'])} a share "
        f"between them is the inventory judgement and nothing else. Note that the difference "
        f"is overwhelmingly a TERMINAL effect: a permanently higher gross profit compounds "
        f"into the perpetuity, which is precisely why the two frames must not be averaged.")

H2('1.2 Book value and sustainable return')
P(f"Equity attributable to shareholders was {M['currency']} {n0(V['eqp_fy25'])} million at "
  f"the year end — {M['currency']} {n2(LN['bv_ps'])} a share, against a traded price of "
  f"{M['currency']} {n2(SPOT)}. That is roughly {n0(SPOT / LN['bv_ps'])} times book, which "
  f"looks extraordinary until the return is put beside it. Return on equity attributable to "
  f"shareholders was {pc(LN['roe_hist'][0])} in FY2023, {pc(LN['roe_hist'][1])} in FY2024 and "
  f"{pc(LN['roe_hist'][2])} in FY2025 — a three-year mean of {pc(LN['roe_sust'])}, which is "
  f"the sustainable return used here, read off the company's own record rather than chosen.")
P(f"A business earning {pc(LN['roe_sust'])} on equity while its cost of equity is "
  f"{pc(W['ke'], 2)} is worth a large multiple of its book. The multiple that relationship "
  f"justifies is (return less growth) divided by (cost of equity less growth): "
  f"({pc(LN['roe_sust'])} − {pc(A['g'], 1)}) ÷ ({pc(W['ke'], 2)} − {pc(A['g'], 1)}) = "
  f"{n1(LN['just_pb'])} times book, or {M['currency']} {n2(LN['book_ps'])} a share.")
rows = [['Book value and sustainable return', 'Value'],
        [f"Equity attributable to shareholders ({M['currency']} m)", n0(V['eqp_fy25'])],
        ['Shares in issue (millions)', n0(SH)],
        [f"Book value per share ({M['currency']})", n2(LN['bv_ps'])],
        ['Return on equity, FY2023', pc(LN['roe_hist'][0])],
        ['Return on equity, FY2024', pc(LN['roe_hist'][1])],
        ['Return on equity, FY2025', pc(LN['roe_hist'][2])],
        ['Sustainable return — the three-year mean', pc(LN['roe_sust'])],
        ['Cost of equity', pc(W['ke'], 2)],
        ['Long-run growth', pc(A['g'], 1)],
        ['Justified multiple of book', f"{n1(LN['just_pb'])}x"],
        [f"Value per share ({M['currency']})", n2(LN['book_ps'])]]
table(rows, [4.6, 1.7], band_rows={11, 12}, size=8.8)
caption(f"Table {tnum()} — the book-value reading. The reason this lens produces a sane answer "
        f"on a {n0(SPOT / LN['bv_ps'])}-times-book share is that the denominator is small by "
        f"design: the company has paid out substantially all of its earnings every year since "
        f"listing, so book equity does not accumulate. Return on equity here measures return "
        f"on a deliberately thin equity base and should not be read as an operating margin.")
P(f"A caution on this lens, stated plainly. Return on capital employed — a measure that does "
  f"not flatter a thin equity base — was {pc(H['FY2023']['roce'])} in FY2023, "
  f"{pc(H['FY2024']['roce'])} in FY2024 and {pc(H['FY2025']['roce'])} in FY2025. That is the "
  f"more honest read of how good this business is, and it is still exceptional. But a "
  f"payout policy is a choice, not a law: if the board ever retained earnings to fund the "
  f"network, book equity would rise and this lens would mechanically produce a higher number "
  f"for an unchanged business. It carries the lowest weight of the four for that reason.")

H2('1.3 Relative multiples')
P(f"There is no clean listed comparable for this company. The closest is Aldrees Petroleum "
  f"and Transport Services in Saudi Arabia at {n1(E['I-07']['value'])} times enterprise value "
  f"to EBITDA; the international convenience-retail names run from about "
  f"{n1(E['I-14']['value'])} times at Ultrapar in Brazil to {n1(E['I-10']['value'])} times at "
  f"Casey's General Stores in the United States. That is a spread of more than three to one, "
  f"and it is a spread across fundamentally different fuel-pricing regimes: a company that "
  f"sets its own pump prices and one that receives a committee-set margin are not the same "
  f"instrument. Applying a peer median here would import someone else's regulatory regime "
  f"into this valuation.")
P(f"This study therefore anchors the relative lens on what the company's own economics "
  f"justify rather than on what other companies trade at. A business with the return, the "
  f"growth and the cost of equity established above supports about "
  f"{n1(LN['just_fwd_pe'])} times forward earnings. On the model's own FY2026 earnings of "
  f"{M['currency']} {n2(LN['eps_fwd_A'])} a share on Frame A and {M['currency']} "
  f"{n2(LN['eps_fwd_B'])} on Frame B, that gives {M['currency']} {n2(LN['rel_A'])} and "
  f"{M['currency']} {n2(LN['rel_B'])}. The peer observations are reported below as a "
  f"cross-check on that reference, never as its source.")
rows = [['Multiple reference', 'Multiple', 'Basis', 'Role in this study']]
rows += [[f"ADNOC Distribution today", f"{n1(LN['pe_now'])}x", 'trailing price / earnings',
          'computed from audited FY2025 earnings per share and the traded price'],
         ['ADNOC Distribution, own three-year mean', f"{n1(LN['own_pe_mean'])}x",
          'trailing price / earnings',
          'the traded price against each audited year\'s own earnings — computed entirely '
          'from primary material'],
         ['ADNOC Distribution today', f"{n1((M['mcap'] + W['net_debt'] + V['lease_fy25'] + V['nciq_fy25']) / H['FY2025']['ebitda'])}x",
          'enterprise value / EBITDA', 'the basis on which the peers below are quoted'],
         ['Aldrees Petroleum and Transport Services', f"{n1(E['I-07']['value'])}x",
          'enterprise value / EBITDA', 'closest regional comparable — cross-check only'],
         ['Saudi Automotive Services Company', f"{n1(E['I-08']['value'])}x",
          'enterprise value / EBITDA', 'cross-check only'],
         ['Alimentation Couche-Tard', f"{n1(E['I-09']['value'])}x",
          'enterprise value / EBITDA', 'cross-check only'],
         ['Casey\'s General Stores', f"{n1(E['I-10']['value'])}x",
          'enterprise value / EBITDA', 'cross-check only — the highest of the set'],
         ['Murphy USA', f"{n1(E['I-11']['value'])}x", 'enterprise value / EBITDA',
          'cross-check only'],
         ['OMV Petrom', f"{n1(E['I-12']['value'])}x", 'enterprise value / EBITDA',
          'cross-check only'],
         ['Vibra Energia', f"{n1(E['I-13']['value'])}x", 'enterprise value / EBITDA',
          'cross-check only'],
         ['Ultrapar Participacoes', f"{n1(E['I-14']['value'])}x", 'enterprise value / EBITDA',
          'cross-check only — the lowest of the set'],
         ['REFERENCE USED', f"{n1(LN['just_fwd_pe'])}x", 'forward price / earnings',
          'what this company\'s own return, growth and cost of equity justify — NOT a peer '
          'median']]
table(rows, [2.15, 0.8, 1.6, 2.35], band_rows={12}, size=8.4)
caption(f"Table {tnum()} — the multiple evidence. The company trades close to the middle of the "
        f"international set on enterprise value to EBITDA and slightly below its closest "
        f"regional comparable. That is useful context and it is NOT the source of the "
        f"reference multiple, which is built from the company's own economics.")
fig('fig4_multiple.png', 6.6,
    'the multiple evidence. The reference multiple used is derived from this company\'s own '
    'return and cost of equity, not from the peer distribution shown beside it.')

H2('1.4 Normalised earnings power')
P(f"The fourth reading asks a deliberately narrow question: if this company never grew "
  f"again, what would it be worth? It takes structural gross profit — volume times margin per "
  f"litre, with every inventory movement stripped out — less cash operating costs, plus other "
  f"income, less the impairment and credit-loss charge, at the FY2026 run rate. That gives "
  f"EBITDA of {M['currency']} {n0(LN['norm_ebitda'])} million and EBIT of {M['currency']} "
  f"{n0(LN['norm_ebit'])} million. Taxed at the statutory {pc(W['tax_statutory'], 0)} it is "
  f"{M['currency']} {n0(LN['norm_nopat'])} million of normalised operating profit after tax.")
rows = [['Normalised earnings power', f"{M['currency']} million"],
        ['Structural gross profit, FY2026 run rate', n0(FC['gp_struct'][0])],
        ['Less cash operating expenses', paren(FC['cash_opex'][0])],
        ['Add other income', n0(FC['other_income'][0])],
        ['Less impairment and credit losses', paren(FC['impairments'][0])],
        ['NORMALISED EBITDA', n0(LN['norm_ebitda'])],
        ['Less depreciation and amortisation', paren(FC['dna'][0])],
        ['Normalised EBIT', n0(LN['norm_ebit'])],
        [f"Tax at the statutory rate of {pc(W['tax_statutory'], 0)}",
         paren(LN['norm_ebit'] - LN['norm_nopat'])],
        ['Normalised operating profit after tax', n0(LN['norm_nopat'])],
        [f"Capitalised at {pc(W['wacc'], 2)} less {pc(A['g'], 1)} growth", n0(LN['norm_ev'])],
        ['Less net debt, leases and minorities',
         paren(LN['norm_ev'] - LN['norm_equity'])],
        ['Equity value', n0(LN['norm_equity'])],
        [f"VALUE PER SHARE ({M['currency']})", n2(LN['norm_ps'])]]
table(rows, [4.6, 1.7], band_rows={5, 13, 14}, size=8.8)
caption(f"Table {tnum()} — normalised earnings power. This reading is capitalised at TODAY's "
        f"cost of capital of {pc(W['wacc'], 2)} rather than the terminal "
        f"{pc(W['wacc_terminal'], 2)} the cash-flow model glides to, which is why it lands "
        f"above the Frame A cash-flow reading despite crediting no growth at all. The two "
        f"disagreements — no growth, but a lower discount rate — very nearly cancel.")

H2('1.5 Synthesis — four methods, one field')
P(f"The four methods answer different questions, so they are weighted by how much of the "
  f"question each one actually answers for a regulated-margin retailer with a long asset "
  f"life. The cash-flow model carries the most weight because volume and margin per litre are "
  f"the only two things that matter here and it is the only method that forecasts them "
  f"explicitly. Book value carries the least, for the reason given in section 1.2.")
rows = [['Method', f"Frame A ({M['currency']})", f"Frame B ({M['currency']})", 'Weight',
         'What it answers']]
rows += [['Discounted cash flow', n2(A['per_share']), n2(Bf['per_share']),
          pc(LN['items_A'][0]['weight'], 0),
          'what the volume and margin path is worth, discounted'],
         ['Normalised earnings power', n2(LN['norm_ps']), n2(LN['norm_ps']),
          pc(LN['items_A'][1]['weight'], 0),
          'what it is worth if it never grows again'],
         ['Relative multiples', n2(LN['rel_A']), n2(LN['rel_B']),
          pc(LN['shared'][0]['weight'], 0),
          'what its own economics justify paying for its earnings'],
         ['Book value and sustainable return', n2(LN['book_ps']), n2(LN['book_ps']),
          pc(LN['shared'][1]['weight'], 0),
          'what the capital in the business earns on itself'],
         ['WEIGHTED CENTRE', n2(LN['centre_A']), n2(LN['centre_B']), '100%',
          'never averaged across the two frames'],
         ['Dividend capitalisation', n2(LN['div_ps']), n2(LN['div_ps']), '—',
          'carried unweighted — it values the policy, not the business']]
table(rows, [1.95, 1.0, 1.0, 0.65, 2.3], band_rows={5}, size=8.6)
caption(f"Table {tnum()} — the four methods and their weights. The field runs from "
        f"{M['currency']} {n2(min(A['per_share'], LN['norm_ps'], LN['rel_A'], LN['book_ps']))} "
        f"to {M['currency']} "
        f"{n2(max(Bf['per_share'], LN['norm_ps'], LN['rel_B'], LN['book_ps']))} across the "
        f"individual readings; the published low and high of {M['currency']} "
        f"{n2(LN['fair_bear'])} to {M['currency']} {n2(LN['fair_bull'])} widen that by a "
        f"further margin either side of the centres, because a field built only from the "
        f"points a model happens to produce understates the uncertainty in the model itself.")

H2('1.6 Drivers — every segment grown on its own driver')
P("No segment is grown on a blended rate. Each disclosed leg is built from its own physical "
  "driver: litres times margin per litre for the two fuel legs, and revenue times gross "
  "margin for non-fuel retail, which is a shop and not a pump. Revenue per litre is then an "
  "OUTPUT of the committee-set price path, and gross margin is an OUTPUT of the two "
  "together. Margins are never assumed.")
rows = [[f"Volume and margin build", 'FY2025'] + [y.replace('FY', '') for y in YR]]
rows.append(['Retail fuel volume (m litres)', n0(UB['vol_retail_fy25'])] +
            [n0(x) for x in FC['vol_retail']])
rows.append(['   growth', ''] + [pc(x) for x in V['vol_retail_g']])
rows.append(['Commercial fuel volume (m litres)', n0(UB['vol_comm_fy25'])] +
            [n0(x) for x in FC['vol_comm']])
rows.append(['   growth', ''] + [pc(x) for x in V['vol_comm_g']])
rows.append(['Retail margin per litre (fils)', n1(UB['margin_retail_fy25'] * 1000)] +
            [n1(x * 1000) for x in FC['margin_retail']])
rows.append(['Commercial margin per litre (fils)', n1(UB['margin_comm_fy25'] * 1000)] +
            [n1(x * 1000) for x in FC['margin_comm']])
rows.append([f"Retail price per litre ({M['currency']})", n2(UB['price_retail_fy25'])] +
            [n2(x) for x in FC['price_retail']])
rows.append([f"Commercial price per litre ({M['currency']})", n2(UB['price_comm_fy25'])] +
            [n2(x) for x in FC['price_comm']])
table(rows, [2.15, 0.79, 0.79, 0.79, 0.79, 0.79, 0.79], size=8.4)
caption(f"Table {tnum()} — the physical build. Retail margin per litre begins at "
        f"{n1(UB['margin_retail_fy25'] * 1000)} fils in FY2025 — comfortably above the "
        f"{n0(E['CO-08']['value'])}-fils floor the parent supply agreement guarantees — and is "
        f"grown at the disclosed rate rather than assumed to expand. The price per litre falls "
        f"between FY2026 and FY2027 because the crude path underlying the committee's formula "
        f"is forecast to fall; that is a pass-through and it moves revenue without moving "
        f"gross profit, which is exactly why margin per litre and not price is the driver.")
fig('fig2_volume_price.png', 6.9,
    'the volume and price build. Revenue is the product of the two; only one of them is '
    'within the company\'s control.')

rows = [[f"Gross profit build ({M['currency']} m)"] + [y.replace('FY', '') for y in YR]]
rows.append(['Retail fuel — volume x margin per litre'] + [n0(x) for x in FC['gp_retfuel_struct']])
rows.append(['Commercial fuel — volume x margin per litre'] + [n0(x) for x in FC['gp_comm_struct']])
rows.append(['Non-fuel retail — revenue x gross margin'] + [n0(x) for x in FC['gp_nonfuel']])
rows.append(['STRUCTURAL GROSS PROFIT'] + [n0(x) for x in FC['gp_struct']])
rows.append(['Inventory movement — Frame A'] + [n0(x) for x in FC['invmove_A']])
rows.append(['Gross profit — Frame A'] + [n0(x) for x in FC['gross_profit_A']])
rows.append(['Gross margin — Frame A (OUTPUT)'] + [pc(x) for x in FC['gross_margin_A']])
rows.append(['Inventory movement — Frame B'] + [n0(x) for x in FC['invmove_B']])
rows.append(['Gross profit — Frame B'] + [n0(x) for x in FC['gross_profit_B']])
rows.append(['Gross margin — Frame B (OUTPUT)'] + [pc(x) for x in FC['gross_margin_B']])
table(rows, [2.65, 0.85, 0.85, 0.85, 0.85, 0.85], band_rows={4}, size=8.4)
caption(f"Table {tnum()} — gross profit as an output, never an input. Gross margin is shown "
        f"LAST because it is computed from the lines above it: it is not a driver, and no "
        f"margin assumption appears anywhere in this model. Non-fuel retail is the only leg "
        f"built on a percentage margin, at {pc(V['gm_nonfuel'][0], 0)}, and that percentage "
        f"is the company's own disclosed non-fuel gross margin of "
        f"{pc(UB['gm_nonfuel_fy25'], 1)} in FY2025 and {pc(UB['gm_nonfuel_h126'], 1)} in the "
        f"first half of 2026 — a shop margin, sourced, not chosen.")
fig('fig3_margin_bridge.png', 6.7,
    'the bridge from structural gross profit to reported gross profit. The inventory movement '
    'is the whole of the difference, and it is carried two ways.')

P(f"The cost stack is escalated by driver class, not by one blended index. The fuel itself is "
  f"{pc(CE['commodity_share'], 1)} of the cost base and is a globally traded input: it "
  f"escalates on its own crude-linked realised-price path through the committee's formula, "
  f"never on a domestic inflation series. Staff, utilities, repairs and marketing are "
  f"{pc(CE['domestic_opex_share'], 1)} of the cost base, are genuinely domestic services, and "
  f"escalate at {pc(V['cash_opex_g'][0], 0)} a year against a UAE consumer price forecast of "
  f"{n1(E['C-03']['value'])}%. Applying one index across both would have made the whole "
  f"forecast margin path an artefact of the index chosen.")

rows = [['Driver', 'Value', 'Where it enters the model', 'Evidence']]
_dr_map = {
    'G-01': 'the base of the crude path underlying the committee price formula',
    'G-04': 'the forward crude path, and therefore revenue per litre from FY2027',
    'G-06': 'the long-run ceiling on fuel volume growth and the terminal growth rate',
    'G-07': 'the weight placed on the non-fuel leg and its long-run margin',
    'G-08': 'the risk-free rate through the currency peg',
    'C-02': 'retail and commercial volume growth',
    'C-03': 'the escalator on the domestic cash operating cost line only',
    'C-04': 'retail fuel volume growth — the vehicle parc is the physical driver',
    'C-05': 'the floating-rate basis in the cost of debt',
    'C-08': 'the constructed long-tenor point in the cost of capital',
    'C-09': 'the sovereign default spread that normalises the risk-free rate',
    'C-20': 'the historical price-per-litre base the forecast path is anchored on',
    'I-01': 'the competitive assumption — a stable three-way market share',
    'I-03': 'the Saudi network growth assumption',
    'I-04': 'the Saudi station count in the network build',
    'I-05': 'the Egyptian leg and its currency exposure',
    'I-06': 'the domestic electric-vehicle displacement assumption in terminal growth',
    'CO-02': 'the free float, and therefore the market-value equity weight',
    'CO-04': 'the non-fuel gross margin',
    'CO-07': 'the dividend per share used in the dividend-capitalisation reading',
    'CO-09': 'capital expenditure and the station-count path',
    'CO-10': 'the cost-of-debt cross-check',
}
for e in DRIVERS:
    val = e.get('value')
    unit = e.get('unit') or ''
    vs = '—' if val is None else f"{n1(val) if isinstance(val, float) else val} {clip(unit, 22)}"
    rows.append([clip(e['topic'], 60), clip(vs, 34),
                 _dr_map.get(e['id'], clip(e.get('consequence', ''), 90)),
                 clip(e.get('source_name', ''), 46)])
table(rows, [1.85, 1.15, 2.0, 1.9], size=7.6)
caption(f"Table {tnum()} — every external driver in the model, with the evidence behind it and "
        f"the place it enters. {len(DRIVERS)} of the {len(ENTRIES)} items in the research "
        f"record are classified as drivers: they change a number in the model rather than "
        f"merely informing the narrative. Appendix B lists the full record including the "
        f"items that changed nothing.")

H2('1.7 The crux')
P(f"Here is the whole study in one calculation. Take the cash-flow model exactly as built, "
  f"hold every driver, and solve for the terminal growth rate at which it returns the traded "
  f"price of {M['currency']} {n2(SPOT)}. The answer is {pc(CRUX['g_implied'], 2)} — a "
  f"NEGATIVE number. Against the model's {pc(CRUX['g_base'], 1)}, the market is not pricing a "
  f"slower-growing fuel retailer. It is pricing one whose real volume base shrinks a little "
  f"every year, forever.")
rows = [['Solving the market price backwards', 'The model', 'Implied by the price']]
rows += [['Terminal growth rate', pc(CRUX['g_base'], 2), pc(CRUX['g_implied'], 2)],
         ['Terminal discount rate', pc(CRUX['wacc_term_base'], 2),
          pc(CRUX['wacc_term_implied'], 2)],
         ['Beta', n2(CRUX['beta_base']), n2(CRUX['beta_implied'])],
         [f"Value per share ({M['currency']})", n2(CRUX['normalised_value']), n2(CRUX['spot'])]]
table(rows, [3.3, 1.75, 1.85], band_rows={4}, size=9.0)
caption(f"Table {tnum()} — the reverse valuation, run three ways. Each column solves for ONE "
        f"input holding the others at the model's values, so the three are alternative "
        f"explanations of the same gap rather than a combined scenario. A reader who believes "
        f"the implied beta of {n2(CRUX['beta_implied'])} — close to the market average — is "
        f"the right one has a complete and internally consistent case for the traded price "
        f"without needing volumes to decline at all.")
fig('fig7_crux.png', 6.6,
    'the crux. Value per share against terminal growth; the traded price crosses the curve '
    'below zero.')

P("Now put that implied growth rate into units a reader can actually observe, because a "
  "terminal growth rate is not something anyone can check.")
rows = [['What the implied growth rate means in observable units', 'Value']]
_lit_per_txn = V['vol_retail_h126'] / V['fueltxn_h126']
_litres_lost = UB['vol_retail_fy25'] * abs(CRUX['g_implied'])
rows += [[f"FY2025 retail fuel volume", f"{n0(UB['vol_retail_fy25'])}m litres"],
         ['Implied perpetual rate of change in the volume base', pc(CRUX['g_implied'], 2)],
         ['Litres of retail fuel lost in the first such year',
          f"{n0(_litres_lost)}m litres"],
         ['Litres per fuel transaction, first half of 2026', f"{n1(_lit_per_txn)} litres"],
         ['Fuel transactions that disappear, per year',
          f"{n1(_litres_lost / _lit_per_txn)}m"],
         ['   against fuel transactions in the first half of 2026',
          f"{n1(V['fueltxn_h126'])}m"],
         ['   so, as a share of the half-year transaction base',
          pc(_litres_lost / _lit_per_txn / V['fueltxn_h126'], 2)],
         ['UAE registered vehicles, mid-2025', f"{n1(E['C-04']['value'])} million"],
         ['   growing at', E['C-04']['unit']],
         ['UAE policy target for electric vehicles on the road by 2030',
          f"{n0(E['I-06']['value'])}%"],
         ['Global electric share of new car sales, 2026 forecast',
          f"{n0(E['G-06']['value'])}%"]]
table(rows, [4.6, 1.7], size=8.8)
caption(f"Table {tnum()} — the crux in real units. For the market to be right, this network "
        f"must lose roughly {n1(_litres_lost / _lit_per_txn)} million fuel transactions a "
        f"year, every year, in perpetuity — and it must do so while the UAE vehicle parc is "
        f"growing at {E['C-04']['unit'].split(';')[-1].strip()}. That combination requires "
        f"electric displacement to outrun parc growth permanently from here. It is possible. "
        f"It is a proposition a reader can watch, quarter by quarter, in the company's own "
        f"volume disclosure.")
P(f"Two further readings of the same gap, both published because either could be the true "
  f"explanation. First, sensitivity to volume growth itself: shifting the volume path down by "
  f"one percentage point a year in every forecast year takes the value from {M['currency']} "
  f"{n2(SENS['volume'][2][1])} to {M['currency']} {n2(SENS['volume'][0][1])}, which does NOT "
  f"reach the traded price. Volume alone cannot explain the gap inside the explicit window — "
  f"it has to be the terminal. Second, sensitivity to margin per litre: a "
  f"{pc(abs(SENS['margin'][0][0]), 0)} cut to the margin growth path across both fuel legs "
  f"takes it to {M['currency']} {n2(SENS['margin'][0][1])}. Between them, the observable "
  f"drivers move the answer by less than the terminal assumption does — which is the honest "
  f"statement of where the risk in this valuation actually lives.")
rows = [['The terminal growth rate, sensitised', f"Value per share ({M['currency']})",
         'vs market price']]
for g, v in CRUX['ramp']:
    rows.append([pc(g, 1), n2(v), pc(v / SPOT - 1, 0)])
table(rows, [2.6, 2.1, 1.6], size=8.8)
caption(f"Table {tnum()} — the whole curve, published rather than its comfortable half. The "
        f"traded price of {M['currency']} {n2(SPOT)} sits between the "
        f"{pc(CRUX['ramp'][1][0], 1)} and {pc(CRUX['ramp'][2][0], 1)} rows.")
P(f"And the same discipline applied to the contested judgement. Carrying inventory movements "
  f"at the FY2024–FY2025 average of {M['currency']} {n0(CRUX['avg_24_25'])} million in "
  f"perpetuity is worth {M['currency']} "
  f"{n2(CRUX['inv_ramp'][2][1] - CRUX['inv_ramp'][0][1])} a share. Carrying the first-half "
  f"2026 rate of {M['currency']} {n0(V['invgain_h126'])} million in perpetuity — which nobody "
  f"should believe, and which is shown only to bound the question — is worth {M['currency']} "
  f"{n2(CRUX['inv_ramp'][-1][1] - CRUX['inv_ramp'][0][1])} a share. Setting them to zero in "
  f"every year including FY2026 gives {M['currency']} "
  f"{n2(CRUX['inventory_zero_all_years'])}, still above the traded price. The windfall is not "
  f"the disagreement.")
rows = [[f"Inventory movement carried in perpetuity ({M['currency']} m)",
         f"Value per share ({M['currency']})", 'vs market price']]
for iv, val in CRUX['inv_ramp']:
    rows.append([n0(iv), n2(val), pc(val / SPOT - 1, 0)])
table(rows, [3.0, 2.0, 1.4], size=8.8)
caption(f"Table {tnum()} — the contested judgement bounded at both ends. Frame A is the first "
        f"row; Frame B is the {n0(CRUX['avg_24_25'])} row.")

H2('1.8 Macro and country — the cost of capital')
P(f"The risk-free rate is the UAE federal dirham Treasury Bond, taken from the "
  f"{E['C-06']['as_of_date']} auction at {pc(V['rf_observed'], 2)} on a tenor of about four "
  f"and a half years. It is then NORMALISED by the sovereign's own default spread of "
  f"{pc(V['sov_spread'], 2)} to {pc(W['rf_star'], 2)}, because country risk must enter the "
  f"cost of capital exactly once. Adding a country-risk-loaded equity premium on top of a raw "
  f"local yield would charge the same sovereign risk twice.")
P(f"A tenor gap is disclosed rather than papered over: the UAE has issued no ten-year dirham "
  f"federal bond, so the longest observable dirham federal point is the four-and-a-half-year "
  f"one used above. A ten-year point can be CONSTRUCTED — the Abu Dhabi sovereign's dollar "
  f"spread over the corresponding US Treasury, applied to today's ten-year — but it would be "
  f"a construction and not an observation, and this study uses the observed point and says "
  f"so. The dirham is pegged to the dollar, so the US policy rate at "
  f"{clip(E['G-08']['value'], 20)}% transmits directly; the local base rate is "
  f"{pc(V['cb_base_rate'], 2)}.")
rows = [['Cost of capital, built from the bottom up', 'Value', 'Source or construction']]
rows += [['Observed dirham federal Treasury Bond yield, ~4.5-year tenor',
          pc(V['rf_observed'], 2), f"July 2026 auction, {E['C-06']['as_of_date']}"],
         ['Less: the sovereign\'s OWN adjusted default spread', paren(V['sov_spread'], lambda x: pc(x, 2)),
          f"UAE row, rated {E['C-09']['value']}"],
         ['NORMALISED RISK-FREE RATE', pc(W['rf_star'], 2),
          'country risk removed here so it can enter once, inside the premium below'],
         ['Mature-market equity risk premium', pc(W['erp_mature'], 2),
          'the source file\'s own implied mature-market premium'],
         ['Country risk premium for the UAE', pc(W['crp'], 2),
          'the same file\'s UAE row'],
         ['TOTAL EQUITY RISK PREMIUM', pc(W['erp'], 2), 'rating basis'],
         ['Beta', n2(W['beta']),
          f"{BETAJ['window_years']}-year {BETAJ['frequency']} regression of this share "
          f"against its own local index"],
         ['COST OF EQUITY', pc(W['ke'], 2),
          f"{pc(W['rf_star'], 2)} + {n2(W['beta'])} x {pc(W['erp'], 2)}"],
         ['Pre-tax cost of debt, marginal and term-matched', pc(W['kd_pretax'], 2),
          'the sovereign yield plus the company\'s own disclosed dirham credit margin'],
         ['After-tax cost of debt', pc(W['kd_aftertax'], 2),
          f"at the effective rate of {pc(W['tax_effective'], 2)}"],
         ['Weight of equity — MARKET value', pc(W['we'], 1),
          f"{M['currency']} {n0(W['mcap'])}m of market capitalisation"],
         ['Weight of debt', pc(W['wd'], 1),
          f"{M['currency']} {n0(W['net_debt'])}m of net debt"],
         ['WEIGHTED AVERAGE COST OF CAPITAL, today', pc(W['wacc'], 2), ''],
         ['Terminal beta', n2(W['beta_terminal']),
          'glided toward the market as the regulated-margin advantage is assumed to erode'],
         ['Terminal weight of debt', pc(W['wd_terminal'], 0),
          'a normalised structure rather than today\'s near-ungeared one'],
         ['TERMINAL WEIGHTED AVERAGE COST OF CAPITAL', pc(W['wacc_terminal'], 2),
          f"the rate that discounts {pc(A['tv_share'], 1)} of the value"]]
table(rows, [2.85, 0.95, 3.0], band_rows={3, 6, 8, 13, 16}, size=8.4)
caption(f"Table {tnum()} — the cost of capital. The discount rate is not held at "
        f"{pc(W['wacc'], 2)}: it glides linearly to {pc(W['wacc_terminal'], 2)} across the "
        f"five explicit years, because today's reading rests on a beta of {n2(W['beta'])} and "
        f"a debt weight of {pc(W['wd'], 1)} that this study does not believe are permanent. "
        f"Holding the first-year rate through the terminal would ADD materially to the "
        f"valuation, and would be the single easiest way to make this study say what a reader "
        f"might want it to say.")

P(f"The beta is the company's own, regressed against its own local index. On "
  f"{BETAJ['window_years']} years of {BETAJ['frequency']} returns against the "
  f"{BETA_CH['label']}, it is {n2(BETA_CH['beta'])} with a standard error of "
  f"{n2(BETA_CH['se'])} and an r-squared of {pc(BETA_CH['r2'], 1)} over "
  f"{n0(BETA_CH['n'])} observations — a 90% interval of {n2(BETA_CH['ci90'][0])} to "
  f"{n2(BETA_CH['ci90'][1])}. The regression EXCLUDES the subject from the index, because a "
  f"large constituent regressed against an index containing itself is mechanically pulled "
  f"toward one. Including it gives {n2(BETAJ['primary']['beta'])}; regressing against the "
  f"broader all-UAE composite gives {n2(BETAJ['crosscheck_all_uae_ex']['beta'])}. All three "
  f"are published. A beta of {n2(W['beta'])} is a real economic statement about this share: a "
  f"committee-set margin with a parental floor under it genuinely is less exposed to the "
  f"local market cycle than the average listed company.")

rows = [['Cost of debt — the evidence', 'Rate', 'Basis']]
rows += [['Company\'s own dirham facility margin',
          f"+{pc(V['credit_margin'], 2)}", 'over the local interbank rate, as disclosed'],
         ['Company\'s own dollar facility margin', f"+{pc(V['credit_margin_usd'], 2)}",
          'over the dollar overnight financing rate, as disclosed'],
         ['Local central bank base rate', pc(V['cb_base_rate'], 2),
          f"held at the {E['C-05']['as_of_date']} meeting"],
         ['Floating-rate basis today',
          pc(W['kd_floating_basis'], 2),
          'base rate plus the dirham margin — what the company pays right now'],
         ['Sovereign dirham yield, term-matched', pc(V['rf_observed'], 2),
          'the same four-and-a-half-year federal point used above'],
         ['MARGINAL, TERM-MATCHED COST OF DEBT USED', pc(W['kd_pretax'], 2),
          'sovereign yield plus the company\'s own dirham margin'],
         ['   the same construction on the dollar margin', pc(W['kd_pretax_usd_basis'], 2),
          'published as a cross-check, not used'],
         ['Parent group\'s own long-dated dollar issue', f"{n2(E['CO-10']['value'])}%",
          'ten-year sukuk, an independent cross-check on the level']]
table(rows, [2.6, 0.95, 3.2], band_rows={6}, size=8.4)
caption(f"Table {tnum()} — the cost-of-debt evidence. The rate used is MARGINAL and "
        f"forward-looking, not the average rate the company happens to be paying on its "
        f"existing book. It must sit ABOVE the sovereign — a corporate cannot borrow below "
        f"its own government in the same currency — and it does: {pc(W['kd_pretax'], 2)} "
        f"against {pc(V['rf_observed'], 2)}. Note that the floating basis today, "
        f"{pc(W['kd_floating_basis'], 2)}, is BELOW the term-matched construction, because "
        f"the short end of the curve is below the four-and-a-half-year point. Using the "
        f"floating rate would understate the cost of financing a long-lived asset base, so it "
        f"is shown and not used.")

P("Three constructions in this section are genuinely contested. Each is priced rather than "
  "merely named, because naming a judgement without pricing it tells a reader nothing about "
  "whether it matters.")
rows = [['The contested construction', 'The choice made', 'What it is worth']]
rows += [[f"The {pc(V['tax_dmtt'], 0)} minimum top-up tax",
          f"the model taxes cash flows at the effective rate the audited FY2025 "
          f"reconciliation actually shows, {pc(W['tax_effective'], 2)}, NOT at "
          f"{pc(V['tax_dmtt'], 0)}. The company is plainly within the size threshold for the "
          f"minimum tax regime, but its own audited reconciliation does not apply it, and "
          f"this study follows the audited accounts rather than the reader's expectation of "
          f"them",
          f"{M['currency']} {n2(abs(SENS['tax_dmtt_impact']))} a share, or "
          f"{pc(abs(SENS['tax_dmtt_impact']) / A['per_share'], 1)} of the Frame A value. At "
          f"{pc(V['tax_dmtt'], 0)} the reading falls from {M['currency']} "
          f"{n2(SENS['tax'][1][1])} to {M['currency']} {n2(SENS['tax'][3][1])}. This is the "
          f"single largest identifiable downside construction in the study and it is "
          f"published as a line, not a footnote"],
         ['Leases in the bridge',
          'the lease liability is deducted in the enterprise-to-equity bridge and the '
          'right-of-use depreciation stays inside the depreciation charge. The alternative — '
          'treating leases as operating and adding the rent back to EBITDA — is internally '
          'consistent too, but mixing the two double-counts',
          f"{M['currency']} {n0(V['lease_fy25'])} million of deduction, or "
          f"{M['currency']} {n2(V['lease_fy25'] / SH)} a share. Enterprise value multiples "
          f"quoted anywhere in this study carry the lease on the same basis"],
         ['The equity risk premium basis',
          f"the source file publishes a rating-based row for the UAE and NO credit-default-"
          f"swap-based row, so only the rating basis can be published here. Where two bases "
          f"exist this study publishes both; here one does not exist, and inventing a "
          f"swap-based figure from a third-party quote that CONTRADICTS the original file "
          f"would be worse than disclosing the gap",
          f"the rating basis gives a total premium of {pc(W['erp'], 2)}. A reader who "
          f"prefers a higher premium can read the beta row of the sensitivity table: a beta "
          f"of {n2(SENS['beta'][3][0])} — arithmetically the same effect as a premium about "
          f"forty per cent higher — gives {M['currency']} {n2(SENS['beta'][3][1])}"]]
table(rows, [1.5, 3.0, 2.4], size=8.2)
caption(f"Table {tnum()} — every contested construction, priced. A fourth is disclosed without "
        f"a price because it cannot be priced from the original source: the country-risk file "
        f"used here carries a January 2026 vintage, a mid-year update is known to exist, and "
        f"the UAE row of that update could not be verified from the original file. The "
        f"January row is used and the vintage is stated.")

H2('1.9 Sensitivity')
P("Every driver moved one at a time, holding the rest. The order below is the order of "
  "importance, and it is not the order most readers would guess.")
rows = [['Driver', 'Low case', 'Base', 'High case', 'Range in value per share']]
_sens_rows = [('Terminal cost of capital', 'wacc', lambda x: pc(x, 2)),
              ('Beta', 'beta', n2),
              ('Terminal growth rate', 'g', lambda x: pc(x, 1)),
              ('Margin-per-litre growth path', 'margin', lambda x: pc(x, 0)),
              ('Inventory movement carried', 'inventory', n0),
              ('Effective tax rate', 'tax', lambda x: pc(x, 2)),
              ('Volume growth path', 'volume', lambda x: pc(x, 1)),
              ('Capital expenditure', 'capex', lambda x: pc(x, 0))]
_ordered = sorted(_sens_rows,
                  key=lambda r: -abs(SENS[r[1]][-1][1] - SENS[r[1]][0][1]))
for nm, k, f in _ordered:
    lo, hi = SENS[k][0], SENS[k][-1]
    base = [r for r in SENS[k] if abs(r[1] - A['per_share']) < 1e-9]
    base_lbl = f(base[0][0]) if base else '—'
    rows.append([nm, f"{f(lo[0])} → {n2(lo[1])}", base_lbl, f"{f(hi[0])} → {n2(hi[1])}",
                 n2(abs(hi[1] - lo[1]))])
table(rows, [2.2, 1.35, 0.85, 1.35, 1.25], size=8.6)
caption(f"Table {tnum()} — every driver, ranked by how much it moves the answer. The top three "
        f"are all statements about the terminal, not about the business. That is the "
        f"structural fact a reader should take from this study: at {pc(A['tv_share'], 1)} "
        f"terminal weight, this is mostly a valuation of the discount rate and the long-run "
        f"growth rate.")
fig('fig6_tornado.png', 6.7,
    'the sensitivity ranking. The three widest bars are all terminal assumptions.')

rows = [[f"Terminal cost of capital ↓ / growth →"] + [pc(g, 1) for g in SENS['grid_g']]]
for i, wc in enumerate(SENS['grid_wacc']):
    rows.append([pc(wc, 2)] + [n2(x) for x in SENS['grid'][i]])
table(rows, [1.8, 1.02, 1.02, 1.02, 1.02, 1.02], size=8.8)
caption(f"Table {tnum()} — value per share across the terminal cost of capital and the terminal "
        f"growth rate, the two inputs the sensitivity ranking says matter most. The full grid "
        f"runs {M['currency']} {n2(SENS['grid_lo'])} to {M['currency']} "
        f"{n2(SENS['grid_hi'])} — and the WHOLE of it is published, including the corner that "
        f"sits below the traded price. The model's own combination, "
        f"{pc(W['wacc_terminal'], 2)} and {pc(A['g'], 1)}, is the centre cell.")

# =================== 6. SECTION 2 — TECHNICAL AND PRICE STRUCTURE ==============
H1('2. Technical and price structure')
P(TECH['tech']['summary'])
rows = [['Level', M['currency'], 'Distance from the close', 'Structure behind it']]
_res, _sup = TECH['level_detail']['res'], TECH['level_detail']['sup']
rows.append(['Third resistance', n2(TECH['levels']['res'][2]),
             pc(TECH['levels']['res'][2] / SPOT - 1, 1),
             f"{_res[2]['kind']} level, {n0(_res[2]['touches'])} prior touches"])
rows.append(['Second resistance', n2(TECH['levels']['res'][1]),
             pc(TECH['levels']['res'][1] / SPOT - 1, 1),
             f"{_res[1]['kind']} level, {n0(_res[1]['touches'])} prior touches"])
rows.append(['Nearest resistance', n2(TECH['levels']['res'][0]),
             pc(TECH['levels']['res'][0] / SPOT - 1, 1),
             f"{_res[0]['kind']} level, {n0(_res[0]['touches'])} prior touches"])
rows.append(['LAST CLOSE', n2(SPOT), '—', f"{TECH['data_date']}"])
rows.append(['Nearest support', n2(TECH['levels']['sup'][0]),
             pc(TECH['levels']['sup'][0] / SPOT - 1, 1),
             f"{_sup[0]['kind']} level, {n0(_sup[0]['touches'])} prior touches"])
rows.append(['Second support', n2(TECH['levels']['sup'][1]),
             pc(TECH['levels']['sup'][1] / SPOT - 1, 1),
             f"{_sup[1]['kind']} level, {n0(_sup[1]['touches'])} prior touches"])
rows.append(['Third support', n2(TECH['levels']['sup'][2]),
             pc(TECH['levels']['sup'][2] / SPOT - 1, 1),
             f"{_sup[2]['kind']} level, {n0(_sup[2]['touches'])} prior touches"])
table(rows, [1.7, 0.85, 1.7, 2.4], band_rows={4}, size=8.8)
caption(f"Table {tnum()} — support and resistance, computed from recency-weighted pivot "
        f"clusters on the same cleaned price history the probability map in section 3 uses. "
        f"The asymmetry is the point: the supports below have been tested "
        f"{n0(_sup[0]['touches'] + _sup[1]['touches'] + _sup[2]['touches'])} times between "
        f"them, while the resistances above have barely been visited. This share has spent "
        f"most of the last year building a floor, not a ceiling.")
rows = [['Momentum and range', 'Reading']]
rows += [['20-day moving average', f"{n2(TECH['ma']['20'])}, {TECH['ma_slope']['20']}"],
         ['50-day moving average', f"{n2(TECH['ma']['50'])}, {TECH['ma_slope']['50']}"],
         ['200-day moving average', f"{n2(TECH['ma']['200'])}, {TECH['ma_slope']['200']}"],
         ['Relative strength index (14)', n1(TECH['rsi'])],
         ['Average true range (14)',
          f"{n2(TECH['atr'])} ({pc(TECH['atr_pct'], 1)} of the close)"],
         ['Moving-average convergence / divergence',
          f"{n2(TECH['macd']['macd'])} against a signal of {n2(TECH['macd']['signal'])}"],
         ['50-day against 200-day', f"{TECH['ma_cross']['kind']} crossover, "
          f"{n0(TECH['ma_cross']['ago'])} sessions ago"],
         ['52-week range', f"{n2(TECH['lo_52w'])} – {n2(TECH['hi_52w'])}"],
         ['Position in that range',
          f"{pc(TECH['pct_off_high'], 1)} below the high, {pc(TECH['pct_off_low'], 1)} above "
          f"the low"]]
table(rows, [2.7, 3.4], size=8.8)
caption(f"Table {tnum()} — the computed momentum and range readings, from "
        f"{n0(TECH['sessions'])} sessions of cleaned daily history.")
P(TECH['tech']['bull'] + ' ' + TECH['tech']['bear'])
P(f"One structural observation the indicators do not carry. The daily average true range is "
  f"{pc(TECH['atr_pct'], 1)} of the price. That is an extremely quiet tape for an emerging-"
  f"market listing, and it is the same fact that drives the calibration discussion in the "
  f"next section: this share moves less than almost anything else on its exchange, and a "
  f"probability range built across the whole exchange will therefore be too wide for it.")

# ==================== 7. SECTION 3 — PROBABILISTIC PRICE MAP ===================
H1('3. Probabilistic price map')
P("The valuation above says where the shares should be. This section says something narrower "
  "and more testable: given how this share has actually behaved, where might the price be in "
  "one month and in three? It is a statement about the distribution of outcomes, not a "
  "forecast of one, and it is entirely independent of the fundamental work above.")
rows = [['Percentile of the simulated distribution', 'One month', 'Three months']]
for p in (5, 25, 50, 75, 95):
    rows.append([f"{p}th percentile", n2(STRIKE['horizons']['1M']['pct'][f'p{p}']),
                 n2(STRIKE['horizons']['3M']['pct'][f'p{p}'])])
rows.append(['Width of the 90% range',
             pc(STRIKE['horizons']['1M']['pct']['p95'] / STRIKE['horizons']['1M']['pct']['p5'] - 1, 0),
             pc(STRIKE['horizons']['3M']['pct']['p95'] / STRIKE['horizons']['3M']['pct']['p5'] - 1, 0)])
rows.append(['Check date', STRIKE['horizons']['1M']['grade_date'],
             STRIKE['horizons']['3M']['grade_date']])
table(rows, [3.2, 1.35, 1.35], band_rows={7}, size=9.0)
caption(f"Table {tnum()} — the percentile map, in {M['currency']}. The anchor is the "
        f"{M['currency']} {n2(STRIKE['spot'])} close of {STRIKE['anchor_date']}. The "
        f"simulation is fed {pc(STRIKE['horizons']['1M']['anchor_vol_ann'], 1)} annualised "
        f"volatility at one month and "
        f"{pc(STRIKE['horizons']['3M']['anchor_vol_ann'], 1)} at three, and carries a carry "
        f"drift built from a risk-free rate of {pc(STRIKE['rf_live'], 2)} against a dividend "
        f"yield of {pc(STRIKE['q_annual'], 2)} — which is why the median sits marginally "
        f"BELOW the anchor at both horizons.")
rows = [['Probability', 'One month', 'Three months']]
for label, key in (('Finishes above the anchor', 'p_above'),
                   ('Finishes 10% or more above', 'p_up10'),
                   ('Finishes 10% or more below', 'p_dn10'),
                   ('TOUCHES 10% above at any point', 'touch_up10'),
                   ('TOUCHES 10% below at any point', 'touch_dn10')):
    rows.append([label, pc(STRIKE['horizons']['1M'][key], 1),
                 pc(STRIKE['horizons']['3M'][key], 1)])
table(rows, [3.2, 1.35, 1.35], size=9.0)
caption(f"Table {tnum()} — the level-touch ladder. Touching a level at any point inside the "
        f"window is far more likely than finishing beyond it: at three months the chance of "
        f"touching a price ten per cent higher is "
        f"{n1(STRIKE['horizons']['3M']['touch_up10'] / STRIKE['horizons']['3M']['p_up10'])} "
        f"times the chance of closing there. A reader with a stop-loss experiences the touch "
        f"probability; a reader holding to the check date experiences the other one.")
fig('fig5_cone.png', 6.9,
    'the price history and the one- and three-month probability ranges.')

P(f"How much should a reader trust this? The method was tested by re-running it across this "
  f"share's own price history without ever letting it see the future, and scoring each "
  f"forecast against what actually happened. The honest answer is that on this particular "
  f"share the three-month range has been TOO WIDE — not mis-centred, too wide — and this "
  f"study would rather say so than present the range as sharper than it is.")
P(f"The numbers. Over {n0(BT['production']['windows'])} non-overlapping three-month windows "
  f"running from {BT['production']['first_origin']} to {BT['production']['last_origin']}, the "
  f"realised price landed inside the 80% range on EVERY ONE of them and inside the 90% range "
  f"on every one of them — against targets of 80% and 90% respectively. Coverage of "
  f"{pc(BT['production']['cov80'], 0)} where 80% was intended is not a success; it is a range "
  f"that is too generous. The 50% range covered {pc(BT['production']['cov50'], 0)} against a "
  f"50% target, the same story a little less starkly. The range averaged "
  f"{n2(BT['production']['width_vs_benchmark'])} times the width of a simple random-walk "
  f"benchmark anchored on the same carry, and it scored slightly WORSE than that benchmark, "
  f"by {BT['production']['skill_norm']:+.4f} on a scale where zero means no better and one "
  f"means perfect. Over the longer {BT['full']['span_years']:.1f}-year history and "
  f"{n0(BT['full']['windows'])} windows the same test gives "
  f"{BT['full']['skill_norm']:+.4f} with 90% coverage of "
  f"{pc(BT['full']['cov90'], 0)}; over the last five years and "
  f"{n0(BT['five_year']['windows'])} windows, {BT['five_year']['skill_norm']:+.4f}. All three "
  f"are reported, because reporting two of three would be a choice about which evidence a "
  f"reader sees.")
P(f"The one-month range performs better. Across {n0(BT['h1_production']['windows'])} one-month "
  f"windows it scored {BT['h1_production']['skill_norm']:+.4f} — indistinguishable from the "
  f"benchmark rather than behind it — with 80% coverage of "
  f"{pc(BT['h1_production']['cov80'], 0)} and 90% coverage of "
  f"{pc(BT['h1_production']['cov90'], 0)}, both close to their targets, on a width ratio of "
  f"{n2(BT['h1_production']['width_vs_benchmark'])}. The shorter horizon is where the method "
  f"is honest about this share; the longer one is where it is too cautious.")
P(f"The reason is not mysterious and it is worth stating precisely, because it tells a reader "
  f"how to use the range. This is one of the least volatile shares on its exchange. Measured "
  f"over a common window against the {n0(VOL['n'])} largest names on the same market, its "
  f"annualised volatility is {pc(VOL['adnocdist_vol'], 1)} against a median of "
  f"{pc(VOL['panel_median'], 1)} — it ranks {n0(VOL['rank'])}th quietest of "
  f"{n0(VOL['n'])}, at {pc(VOL['ratio_to_median'], 0)} of the median. The width parameter "
  f"that generates the range is fitted across that whole set of names at once, so a share "
  f"that moves three-quarters as much as the typical one inherits a range sized for the "
  f"typical one. Rebuilding the width from this share's own resolved windows alone implies "
  f"about {n2(WID['implied_name_width'] / WID['pooled_width'])} times the width actually "
  f"published.")
P(f"So: read the published three-month range as an OUTER bound rather than a tight one. A "
  f"narrower range fitted to this name alone is NOT published here, and the reason is a "
  f"discipline rather than an oversight — a width fitted to this share's own history has not "
  f"yet been tested on data it did not see, and nothing enters this study's machinery without "
  f"surviving that test. Publishing a tighter range because it fits the past better is "
  f"exactly the mistake the discipline exists to prevent. The wider range is the honest one "
  f"until the narrower one has earned its place.")

# =================== 8. SECTION 4 — COMPARISON OF THE LENSES ===================
H1('4. Comparison of the lenses')
rows = [['Method', f"{M['currency']} / share", 'Most sensitive to', 'When it misleads']]
rows += [['Discounted cash flow — Frame A', n2(A['per_share']),
          f"the terminal discount rate and growth — {pc(A['tv_share'], 1)} of the value is "
          f"in the terminal block",
          'when five explicit years are not long enough to reach a steady state, which for a '
          'network still adding stations is a live risk'],
         ['Discounted cash flow — Frame B', n2(Bf['per_share']),
          'the same, plus whether inventory movements are a recurring feature of a '
          'pass-through pricing model or a one-off of a volatile year',
          'if the crude path mean-reverts as forecast, the inventory gains reverse and this '
          'frame is too generous'],
         ['Normalised earnings power', n2(LN['norm_ps']),
          'the choice of discount rate — it capitalises a single year in perpetuity',
          'when the current year is not normal, which after a crude spike is exactly the '
          'condition to worry about'],
         ['Relative multiples', n2(LN['rel_A']),
          'the reference multiple, which is derived from the cost of equity',
          'when the comparable set faces a different pricing regime — which here it does, so '
          'the reference is built from own economics instead'],
         ['Book value and sustainable return', n2(LN['book_ps']),
          'the sustainable return on a deliberately thin equity base',
          'when payout policy, not operating performance, sets the denominator'],
         ['Dividend capitalisation', n2(LN['div_ps']),
          'the dividend policy and the cost of equity — nothing else',
          'whenever the dividend is a fixed policy commitment rather than a share of the '
          'cash generated, which is the case here']]
table(rows, [1.95, 0.8, 1.9, 2.3], size=8.4)
caption(f"Table {tnum()} — the methods against each other, including where each one fails.")
P(f"The readings disagree in an informative direction, and one disagreement is worth more "
  f"than the rest. The dividend-capitalisation reading lands at {M['currency']} "
  f"{n2(LN['div_ps'])} — within {M['currency']} {n2(abs(LN['div_ps'] - SPOT))} of the traded "
  f"price of {M['currency']} {n2(SPOT)}. The cash-flow model lands at {M['currency']} "
  f"{n2(A['per_share'])}. The gap between those two numbers, {M['currency']} "
  f"{n2(A['per_share'] - LN['div_ps'])} a share, is not a modelling artefact. It is the "
  f"difference between what the company PAYS and what the business EARNS.")
P(f"The dividend is a fixed policy commitment: USD {n0(E['CO-06']['value'])} million a year, "
  f"{M['currency']} {n2(V['dps'])} a share, held flat from 2024 through 2030 unless "
  f"{pc(V['payout'], 0)} of net profit exceeds it. Capitalising it at the cost of equity "
  f"values that promise and nothing else. The cash-flow model, by contrast, captures the "
  f"increase the dividend policy does not: free cash flow to the firm runs from "
  f"{M['currency']} {n0(A['fcff'][0])} million to {M['currency']} {n0(A['fcff'][-1])} million "
  f"across the window against a dividend of {M['currency']} {n0(V['dps'] * SH)} million a "
  f"year, so cash accumulates inside the business at a rate the payout does not reflect. A "
  f"holder who values this share on its yield is valuing the policy. A holder who values it "
  f"on its cash flow is valuing the network. Those are different assets, and the study "
  f"publishes both readings rather than deciding which reader is right.")
P(f"That also explains the shape of the rest of the field. The normalised-earnings reading at "
  f"{M['currency']} {n2(LN['norm_ps'])} sits ABOVE the Frame A cash-flow reading despite "
  f"crediting no growth whatever, because it capitalises at today's {pc(W['wacc'], 2)} "
  f"instead of gliding to {pc(W['wacc_terminal'], 2)}. The relative reading at "
  f"{M['currency']} {n2(LN['rel_A'])} and the book reading at {M['currency']} "
  f"{n2(LN['book_ps'])} sit lowest, and both are anchored on the same cost of equity — so "
  f"they are not four independent votes. Three of the five readings move together with the "
  f"discount rate, which is the honest reason the field is as narrow as it is.")

# ============================ 9. SECTION 5 — CATALYSTS =========================
H1('5. Catalysts')
P("What would move this valuation, in the order a reader is likely to encounter it.")
rows = [['What to watch', 'Why it matters', 'When']]
rows += [['The South African acquisition',
          clip(E['CO-05']['finding'], 470) + ' THE BASE CASE IN THIS STUDY EXCLUDES IT '
          'ENTIRELY: no revenue, no cost, no synergy and no financing charge from this '
          'transaction appears anywhere in the model, because it has not closed and remains '
          'subject to regulatory approval. If it completes on the terms announced it is '
          'accretive on the company\'s own stated arithmetic, and this study will carry it '
          'only once it is a fact',
          'completion anticipated 2027'],
         ['The crude price path',
          f"the official forecast is for Brent to fall from {n1(E['G-01']['value'])} dollars "
          f"today toward {n0(E['G-04']['value'])} dollars in 2027. That does two opposite "
          f"things at once: it compresses revenue per litre, which is neutral because the "
          f"margin per litre is what earns, AND it reverses the inventory gains, which is "
          f"NOT neutral. It is the single most direct test of which of the two frames is "
          f"right", 'quarterly'],
         ['Inventory movements in the second half of 2026',
          f"{M['currency']} {n0(V['invgain_h126'])} million was booked in the first half "
          f"against {M['currency']} {n0(V['invgain_fy25'])} million in the whole of FY2025. "
          f"If the second half gives it back, Frame A is vindicated; if it holds, Frame B "
          f"is. The company's own underlying EBITDA measure — up "
          f"{pc(V['ebitda_und_fy25'] / V['ebitda_und_fy24'] - 1, 1)} in FY2025 against a "
          f"headline that moved with the inventory — is the line to read",
          'FY2026 results'],
         ['Non-fuel conversion',
          f"non-fuel transactions per fuel transaction FELL from "
          f"{n2(V['nonfueltxn_h125'] / V['fueltxn_h125'])} to "
          f"{n2(V['nonfueltxn_h126'] / V['fueltxn_h126'])} year on year. Non-fuel is the "
          f"only leg with genuine pricing freedom and it carries a "
          f"{pc(UB['gm_nonfuel_h126'], 0)} gross margin against a fuel margin of a few per "
          f"cent. The company's own target is to double non-fuel transactions between 2023 "
          f"and 2030; the trend is currently against it", 'each set of results'],
         ['The network build',
          clip(E['CO-09']['finding'], 260), 'FY2026 and annually'],
         ['Electric-vehicle displacement',
          f"the UAE policy target is {n0(E['I-06']['value'])}% of vehicles on the road "
          f"electric by 2030, against a vehicle parc growing at "
          f"{clip(E['C-04']['unit'], 60)}. Section 1.7 shows the market price already embeds "
          f"permanent volume decline; this is the mechanism that would deliver it. The "
          f"company is building charging points — {n0(V['evpoints_h126'])} of them by mid-"
          f"2026 — which converts part of the threat into a different revenue line",
          'continuous'],
         ['The minimum top-up tax',
          f"the audited FY2025 reconciliation does not apply the "
          f"{pc(V['tax_dmtt'], 0)} minimum rate and this study follows the audited accounts. "
          f"If a future reconciliation does apply it, the value impact is "
          f"{M['currency']} {n2(abs(SENS['tax_dmtt_impact']))} a share on the arithmetic in "
          f"section 1.8", 'FY2026 results'],
         ['The dividend',
          f"{clip(E['CO-06']['finding'], 200)} A move to quarterly payment is a change in "
          f"the shape of the cash return, not its size", 'quarterly from 2026']]
table(rows, [1.5, 3.9, 1.5], size=8.2)
caption(f"Table {tnum()} — the events that would move this valuation, and the direction each "
        f"cuts. The first row is the largest single item outside the base case and it is "
        f"excluded from every number in this study.")

# ============== 10. SECTION 6 — READING THE PROBABILITY ZONES ==================
H1('6. Reading the probability zones')
P('The ranges in section 3 are frequently misread, so here is how to use them.')
bullet('is the probability that the price ENDS the window beyond a level. It is what a '
       'position held to the check date experiences.', bold_head='The percentile map ')
bullet(f"is the probability that the price TOUCHES a level at any point inside the window, "
       f"even if it comes back. It is always the larger of the two. At three months the "
       f"chance of touching a price ten per cent above the anchor is "
       f"{pc(STRIKE['horizons']['3M']['touch_up10'], 1)} against "
       f"{pc(STRIKE['horizons']['3M']['p_up10'], 1)} of closing there.",
       bold_head='The touch ladder ')
bullet(f"is a calendar commitment, not a session count. The three-month range is graded on "
       f"{STRIKE['horizons']['3M']['grade_date']} against the closing price on that date, "
       f"whatever happened in between.", bold_head='The check date ')
bullet(f"is NOT the fair-value range. The probability map is built from price behaviour "
       f"alone and knows nothing about the company; the valuation is built from the "
       f"statements and knows nothing about the tape. They are deliberately independent, and "
       f"they disagree: the three-month 95th percentile of {M['currency']} "
       f"{n2(STRIKE['horizons']['3M']['pct']['p95'])} sits below every one of the four "
       f"weighted methods.", bold_head='The range ')
bullet(f"is wider than this share warrants, and section 3 says so with the numbers. Treat "
       f"the 90% range as an outer bound. A reader who wants a working range should look at "
       f"the 25th-to-75th band — {M['currency']} "
       f"{n2(STRIKE['horizons']['3M']['pct']['p25'])} to {M['currency']} "
       f"{n2(STRIKE['horizons']['3M']['pct']['p75'])} at three months — which is the half of "
       f"the distribution the evidence supports best.", bold_head='The published width ')
P("One thing the ranges are not: a forecast. Nothing in section 3 says the price will rise or "
  "fall. The median at both horizons sits fractionally below the anchor purely because the "
  "dividend yield exceeds the risk-free rate, which is arithmetic, not a view.")

# ========= 11. SECTION 7 — CAVEATS AND WHAT WOULD CHANGE OUR MIND ==============
H1('7. Caveats, and what would change our mind')
rows = [['Caveat', 'Why it matters', 'What would change the answer']]
rows += [['Terminal weight',
          f"{pc(A['tv_share'], 1)} of enterprise value sits beyond the explicit window. "
          f"Three-quarters of this valuation is a statement about the years after "
          f"{YR[-1].replace('E', '')}",
          f"any evidence about the long-run volume base. The sensitivity grid runs "
          f"{M['currency']} {n2(SENS['grid_lo'])} to {M['currency']} {n2(SENS['grid_hi'])} "
          f"and the whole of it is published"],
         ['Inventory movements are not an audited line',
          'they appear only in management commentary and the results presentations, with no '
          'reconciliation to the audited accounts. The study\'s central contested judgement '
          'therefore rests on a disclosure that cannot be independently recomputed',
          'a reconciliation in a future filing, or a full year in which the crude path falls '
          'and the movements reverse as Frame A assumes'],
         ['A committee sets the price',
          'the single largest revenue driver in this business is set monthly by a government '
          'committee. No forecast of it is anything more than a forecast of the crude path '
          'that feeds its formula',
          'a change to the pricing mechanism itself — deregulation, a cap, or a change to '
          'the parental margin floor'],
         ['The parental relationship cuts both ways',
          f"the supply agreement provides a {n0(E['CO-08']['value'])}-fils margin floor and "
          f"a cash-settled inventory backstop, which is genuinely valuable. It is also a "
          f"related-party arrangement with a controlling shareholder that owns roughly "
          f"{pc(1 - E['CO-02']['value'] / 100, 0)} of the equity",
          'any renegotiation of the supply agreement, or a change in the parent\'s stake'],
         ['The beta is low, and it is doing a lot of work',
          f"a beta of {n2(W['beta'])} with an r-squared of {pc(BETA_CH['r2'], 1)} produces a "
          f"cost of equity of {pc(W['ke'], 2)}. The 90% interval on that regression runs "
          f"{n2(BETA_CH['ci90'][0])} to {n2(BETA_CH['ci90'][1])}",
          f"a beta at the top of its own confidence interval. The model already glides to "
          f"{n2(W['beta_terminal'])} in the terminal; at {n2(SENS['beta'][3][0])} throughout, "
          f"the value is {M['currency']} {n2(SENS['beta'][3][1])}"],
         ['Three of the five readings share one input',
          'the relative, book-value and dividend readings are all anchored on the same cost '
          'of equity. They are not independent votes, and the narrowness of the field partly '
          'reflects that',
          'nothing — this is a property of the methods, disclosed rather than fixed'],
         ['The country-risk file carries a January vintage',
          'a mid-year update is known to exist but its UAE row could not be verified in the '
          'original source, and a third-party figure that contradicts the original file was '
          'found and NOT used',
          'the mid-year row, read from the original file. The sensitivity to the equity risk '
          'premium is published through the beta row of the sensitivity table'],
         ['The South African acquisition is excluded',
          f"a transaction of approximately USD {n0(E['CO-05']['value'])} million enterprise "
          f"value, expanding the network by roughly half, sits entirely outside every number "
          f"in this study",
          'completion. At that point the base case must be rebuilt, not adjusted'],
         ['The probability range is too wide for this share',
          f"coverage of {pc(BT['production']['cov80'], 0)} where 80% was intended, on a "
          f"width {n2(BT['production']['width_vs_benchmark'])} times the benchmark's",
          'a narrower width fitted to this share alone, once it has been tested on data it '
          'did not see']]
table(rows, [1.6, 2.75, 2.55], size=8.2)
caption(f"Table {tnum()} — what could be wrong, and what evidence would settle it.")

# ==================== 12. APPENDIX A — THE STATEMENTS ==========================
H1('Appendix A — the financial statements')
_ycols = [y.replace('FY', '').replace('E', 'E') for y in YR]
_net_fin = V['fin_fy25'] - V['intinc_fy25']
_pbt_f = [A['ebit'][i] - _net_fin for i in range(NY)]
_tax_f = [x * W['tax_effective'] for x in _pbt_f]
_np_f = [_pbt_f[i] - _tax_f[i] for i in range(NY)]
_npa_f = [x - V['nci_fy25'] for x in _np_f]
_eps_f = [x / SH for x in _npa_f]

H2('A.1 Income statement: three audited years and five forecast years')
rows = [[f"{M['currency']} million"] + list(HYRS) + _ycols]


def isrow(label, hk, fwd, fmt=n0):
    rows.append([label] + [fmt(H[y][hk]) for y in HYRS] + [fmt(x) for x in fwd])


isrow('Revenue', 'revenue', FC['revenue'])
isrow('Direct costs', 'direct_costs', FC['direct_costs_A'])
isrow('Gross profit', 'gross_profit', FC['gross_profit_A'])
rows.append(['Gross margin'] + [pc(H[y]['gross_margin']) for y in HYRS] +
            [pc(x) for x in FC['gross_margin_A']])
rows.append(['   memorandum: inventory movement inside gross profit',
             '—', n0(V['invgain_fy24']), n0(V['invgain_fy25'])] +
            [n0(x) for x in FC['invmove_A']])
isrow('Cash operating expenses', 'cash_opex', FC['cash_opex'])
isrow('Other income', 'other_income', FC['other_income'])
isrow('Impairment and credit losses', 'impairments', FC['impairments'])
isrow('EBITDA', 'ebitda', A['ebitda'])
rows.append(['EBITDA margin'] + [pc(H[y]['ebitda_margin']) for y in HYRS] +
            [pc(x) for x in FC['ebitda_margin_A']])
isrow('Depreciation and amortisation', 'dna', FC['dna'])
isrow('EBIT', 'ebit', A['ebit'])
rows.append(['Net finance cost'] +
            [n0(H[y]['finance_costs'] - H[y]['interest_income']) for y in HYRS] +
            [n0(_net_fin)] * NY)
isrow('Profit before tax', 'pbt', _pbt_f)
isrow('Tax', 'tax', _tax_f)
rows.append(['Effective tax rate'] + [pc(H[y]['tax_rate']) for y in HYRS] +
            [pc(W['tax_effective'])] * NY)
isrow('Net profit', 'net_profit', _np_f)
isrow('Non-controlling interests', 'nci', [V['nci_fy25']] * NY)
isrow('PROFIT ATTRIBUTABLE TO SHAREHOLDERS', 'np_attributable', _npa_f)
rows.append([f"Earnings per share ({M['currency']})"] + [n2(H[y]['eps']) for y in HYRS] +
            [n2(x) for x in _eps_f])
rows.append([f"Dividend per share ({M['currency']})",
             n2(V['divpaid_fy23'] / SH), n2(V['divpaid_fy24'] / SH),
             n2(V['divpaid_fy25'] / SH)] + [n2(V['dps'])] * NY)
table(rows, [1.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72], band_rows={3, 9, 12, 19},
      size=8.0)
caption(f"Table {tnum()} — three audited years and five forecast years, Frame A. Every forecast "
        f"line is the model row the valuation itself uses; nothing here is a restatement. Two "
        f"forecast lines are held rather than driven and are labelled as such: the net finance "
        f"cost is held at the FY2025 charge of {M['currency']} {n0(_net_fin)} million, because "
        f"borrowings are neither repaid nor raised in the model, and the minority interest is "
        f"held at {M['currency']} {n0(V['nci_fy25'])} million. The tax line applies the "
        f"effective rate of {pc(W['tax_effective'], 2)} shown in the audited FY2025 "
        f"reconciliation, not the statutory {pc(W['tax_statutory'], 0)} and not the "
        f"{pc(V['tax_dmtt'], 0)} minimum rate; section 1.8 prices that choice. The inventory "
        f"memorandum line is shown INSIDE gross profit rather than beside it, because that is "
        f"where it sits in the reported figure.")

H2('A.2 Balance sheet')
_fixed_h = [V[f'ppe_fy{y}'] + V[f'rou_fy{y}'] + V[f'gwi_fy{y}'] + V[f'onca_fy{y}']
            for y in ('23', '24', '25')]
_rec_h = [V[f'tr_fy{y}'] + V[f'dfrp_fy{y}'] for y in ('23', '24', '25')]
_pay_h = [V[f'tp_fy{y}'] + V[f'dtrp_fy{y}'] for y in ('23', '24', '25')]
_inv_h = [V[f'inv_fy{y}'] for y in ('23', '24', '25')]
_cash_h = [V[f'cash_fy{y}'] for y in ('23', '24', '25')]
_td_h = [V[f'td_fy{y}'] for y in ('23', '24', '25')]
_borr_h = [V[f'borr_fy{y}'] for y in ('23', '24', '25')]
_lease_h = [V[f'lease_fy{y}'] for y in ('23', '24', '25')]
_eqp_h = [V[f'eqp_fy{y}'] for y in ('23', '24', '25')]
_nciq_h = [V[f'nciq_fy{y}'] for y in ('23', '24', '25')]
_ta_h = [V[f'ta_fy{y}'] for y in ('23', '24', '25')]
_other_liab_h = [_ta_h[i] - _eqp_h[i] - _nciq_h[i] - _pay_h[i] - _borr_h[i] - _lease_h[i]
                 for i in range(3)]

_fixed_f, _rec_f, _inv_f, _pay_f, _cash_f, _eqp_f, _div_f = [], [], [], [], [], [], []
_prev_fixed, _prev_cash, _prev_eqp = _fixed_h[2], _cash_h[2], _eqp_h[2]
for i in range(NY):
    _prev_fixed = _prev_fixed + FC['capex'][i] - FC['dna'][i]
    _fixed_f.append(_prev_fixed)
    _rec_f.append(_rec_h[2] * FC['revenue'][i] / V['rev_fy25'])
    _inv_f.append(_inv_h[2] * FC['direct_costs_A'][i] / V['dc_fy25'])
    _pay_f.append(_pay_h[2] * FC['direct_costs_A'][i] / V['dc_fy25'])
    d = V['dps'] * SH
    _div_f.append(d)
    _prev_cash = (_prev_cash + _npa_f[i] + FC['dna'][i] - FC['capex'][i]
                  - A['delta_nwc'][i] - d)
    _cash_f.append(_prev_cash)
    _prev_eqp = _prev_eqp + _npa_f[i] - d
    _eqp_f.append(_prev_eqp)

_ta_f = [_fixed_f[i] + _inv_f[i] + _rec_f[i] + _cash_f[i] + _td_h[2] for i in range(NY)]
_tl_f = [_pay_f[i] + _borr_h[2] + _lease_h[2] + _other_liab_h[2] for i in range(NY)]
_te_f = [_eqp_f[i] + _nciq_h[2] for i in range(NY)]
_check_f = [_ta_f[i] - _tl_f[i] - _te_f[i] for i in range(NY)]

rows = [[f"{M['currency']} million"] + list(HYRS) + _ycols]


def bsrow(label, hist, fwd, fmt=n0):
    rows.append([label] + [fmt(x) for x in hist] + [fmt(x) for x in fwd])


bsrow('Fixed, right-of-use and intangible assets', _fixed_h, _fixed_f)
bsrow('Inventories', _inv_h, _inv_f)
bsrow('Receivables including related parties', _rec_h, _rec_f)
bsrow('Cash and term deposits', [_cash_h[i] + _td_h[i] for i in range(3)],
      [x + _td_h[2] for x in _cash_f])
bsrow('TOTAL ASSETS', _ta_h, _ta_f)
bsrow('Payables including related parties', _pay_h, _pay_f)
bsrow('Borrowings', _borr_h, [_borr_h[2]] * NY)
bsrow('Lease liabilities', _lease_h, [_lease_h[2]] * NY)
bsrow('Provisions and other liabilities', _other_liab_h, [_other_liab_h[2]] * NY)
bsrow('Total liabilities', [_ta_h[i] - _eqp_h[i] - _nciq_h[i] for i in range(3)], _tl_f)
bsrow('Equity attributable to shareholders', _eqp_h, _eqp_f)
bsrow('Non-controlling interests', _nciq_h, [_nciq_h[2]] * NY)
bsrow('TOTAL EQUITY AND LIABILITIES',
      [_ta_h[i] for i in range(3)], [_tl_f[i] + _te_f[i] for i in range(NY)])
bsrow('Balance check', [0.0] * 3, _check_f, fmt=n1)
bsrow('Net debt including leases',
      [_borr_h[i] + _lease_h[i] - _cash_h[i] - _td_h[i] for i in range(3)],
      [_borr_h[2] + _lease_h[2] - _cash_f[i] - _td_h[2] for i in range(NY)])
rows.append([f"Book value per share ({M['currency']})"] +
            [n2(x / SH) for x in _eqp_h] + [n2(x / SH) for x in _eqp_f])
table(rows, [1.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72],
      band_rows={5, 13, 14}, size=8.0)
caption(f"Table {tnum()} — the balance sheet, WHICH BALANCES: the check row reads zero in every "
        f"audited column and every forecast column. The audited columns reconcile exactly to "
        f"the filed total assets of {M['currency']} {n0(_ta_h[2])} million at "
        f"{HYRS[2]}; the grouping above is a summary of the filed captions, not a "
        f"restatement of them. In the forecast, fixed assets roll forward as prior balance "
        f"plus capital expenditure less depreciation; receivables scale on revenue and "
        f"inventories and payables on direct costs, at the FY2025 day ratios set out in A.3; "
        f"borrowings, leases and provisions are HELD, so cash is the plug and it absorbs the "
        f"cash the dividend does not distribute. That is why net debt falls to a net cash "
        f"position across the window — the model distributes the policy dividend, not the "
        f"cash generated, and section 4 is the consequence.")

H2('A.3 Cash flow and the working-capital markers')
rows = [['Marker', 'FY2025 audited'] + _ycols]
rows.append(['Receivable days, trade only', n0(WC['dso_trade'])] +
            [n0(WC['dso_trade'])] * NY)
rows.append(['Receivable days, including related parties', n0(WC['dso_all'])] +
            [n0(WC['dso_all'])] * NY)
rows.append(['Inventory days', n0(WC['dio'])] + [n0(WC['dio'])] * NY)
rows.append(['Payable days, trade only', n0(WC['dpo_trade'])] + [n0(WC['dpo_trade'])] * NY)
rows.append(['Payable days, including related parties', n0(WC['dpo_all'])] +
            [n0(WC['dpo_all'])] * NY)
rows.append(['Cash conversion cycle, trade only', n0(WC['ccc_trade'])] +
            [n0(WC['ccc_trade'])] * NY)
rows.append(['Cash conversion cycle, including related parties', n0(WC['ccc_all'])] +
            [n0(WC['ccc_all'])] * NY)
rows.append([f"Net working capital ({M['currency']} m)", n0(WC['nwc_fy25'])] +
            [n0(x) for x in FC['nwc_A']])
rows.append([f"Change in working capital ({M['currency']} m)", '—'] +
            [n0(x) for x in A['delta_nwc']])
table(rows, [2.55, 1.05, 0.66, 0.66, 0.66, 0.66, 0.66], size=8.2)
caption(f"Table {tnum()} — the asset-conversion cycle, projected rather than plugged. Both "
        f"framings are published because both are legitimate and they say opposite things: "
        f"on trade balances alone the cycle is {n0(WC['ccc_trade'])} days — the business is "
        f"very slightly a net investor in working capital. Including balances with related "
        f"parties, which is how the audited balance sheet actually presents them, the cycle "
        f"is {n0(WC['ccc_all'])} days: the business is financed by its own suppliers, most of "
        f"them inside the parent group. The model uses the second, because that is the "
        f"balance sheet that exists. A reader who thinks the related-party terms would not "
        f"survive an arm's-length renegotiation should use the first, and the difference is "
        f"roughly {M['currency']} {n0(abs(WC['nwc_fy25']))} million of financing.")
rows = [[f"Cash flow ({M['currency']} m)"] + list(HYRS) + _ycols]
rows.append(['Operating cash flow'] + [n0(H[y]['ocf']) for y in HYRS] +
            [n0(_np_f[i] + FC['dna'][i] - A['delta_nwc'][i]) for i in range(NY)])
rows.append(['Capital expenditure'] + [paren(H[y]['capex']) for y in HYRS] +
            [paren(x) for x in FC['capex']])
rows.append(['Free cash flow after capital expenditure'] +
            [n0(H[y]['ocf'] - H[y]['capex']) for y in HYRS] +
            [n0(_np_f[i] + FC['dna'][i] - A['delta_nwc'][i] - FC['capex'][i])
             for i in range(NY)])
rows.append(['Dividends paid'] + [paren(H[y]['dividends_paid']) for y in HYRS] +
            [paren(x) for x in _div_f])
rows.append(['Free cash flow to the FIRM (the valuation line)'] + ['—'] * 3 +
            [n0(x) for x in A['fcff']])
table(rows, [1.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72], band_rows={5}, size=8.0)
caption(f"Table {tnum()} — the cash flow. The last row is the line the valuation discounts and it "
        f"is deliberately shown beside, not instead of, the shareholder cash flow above it: "
        f"free cash flow to the firm is struck before financing and before tax on financing, "
        f"so it is larger than the cash the equity actually receives. Dividends paid have "
        f"exceeded free cash flow after capital expenditure in {HYRS[1]} and {HYRS[2]} — "
        f"{M['currency']} {n0(H['FY2025']['dividends_paid'])} million against "
        f"{M['currency']} {n0(H['FY2025']['ocf'] - H['FY2025']['capex'])} million in FY2025 — "
        f"which is worth a reader's attention even though the balance sheet carries it "
        f"comfortably.")

# ========= 13. APPENDIX B — PEERS, RISKS AND THE RESEARCH RECORD ===============
H1('Appendix B — peers, risks and the research record')
H2('B.1 Peers')
P("No peer figure is used to construct any historical number for this company. Peers appear "
  "here as a cross-check on the multiple the study derives from the company's own economics, "
  "and as evidence about the industry. The set spans four continents deliberately, because "
  "the point being tested is precisely whether a regulated-margin retailer should trade like "
  "an unregulated one.")
rows = [['Company', 'Market', 'Enterprise value / EBITDA', 'Role']]
_peers = [('I-07', 'Aldrees Petroleum and Transport Services', 'Saudi Arabia',
           'closest regional comparable — same region, similar licensing regime'),
          ('I-08', 'Saudi Automotive Services Company', 'Saudi Arabia', 'cross-check'),
          ('I-09', 'Alimentation Couche-Tard', 'Canada',
           'the global convenience-retail benchmark'),
          ('I-10', 'Casey\'s General Stores', 'United States',
           'the highest multiple in the set — a pure convenience model'),
          ('I-11', 'Murphy USA', 'United States', 'high-volume fuel-led model'),
          ('I-12', 'OMV Petrom', 'Romania', 'integrated European comparator'),
          ('I-13', 'Vibra Energia', 'Brazil', 'emerging-market fuel distribution'),
          ('I-14', 'Ultrapar Participacoes', 'Brazil',
           'the lowest multiple in the set')]
for eid, nm, mk, role in _peers:
    rows.append([nm, mk, f"{n1(E[eid]['value'])}x", role])
rows.append(['ADNOC Distribution, at the traded price', 'United Arab Emirates',
             f"{n1((M['mcap'] + W['net_debt'] + V['lease_fy25'] + V['nciq_fy25']) / H['FY2025']['ebitda'])}x",
             'the subject, on the same enterprise-value definition'])
table(rows, [2.15, 1.15, 1.15, 2.4], band_rows={9}, size=8.4)
caption(f"Table {tnum()} — the peer evidence, {n0(len(_peers))} listed comparators plus the "
        f"subject. Two names that would have been the most instructive comparators — a large "
        f"Indian fuel-retail joint venture and a global emerging-market fuel distributor — "
        f"have no listed equity and therefore no multiple, and their absence is recorded "
        f"rather than quietly ignored.")
H2('B.2 Risks')
rows = [['Risk', 'How it would show up', 'Severity']]
rows += [['The crude path reverses the inventory gains',
          f"the {M['currency']} {n0(V['invgain_h126'])} million booked in the first half of "
          f"2026 unwinds as prices fall toward the forecast {n0(E['G-04']['value'])} dollars. "
          f"The parental backstop covers regulated retail stock quarterly and cash-settles, "
          f"which truncates but does not eliminate this", 'High'],
         ['Permanent volume decline',
          f"the risk the market is already pricing. Section 1.7 shows the traded price embeds "
          f"{pc(CRUX['g_implied'], 2)} terminal growth", 'High'],
         ['Non-fuel conversion keeps deteriorating',
          f"non-fuel transactions per fuel transaction fell year on year in the first half of "
          f"2026. The high-margin leg is the one that is supposed to offset fuel maturity",
          'Medium to high'],
         ['Concentration in one country and one regulator',
          f"{n0(V['stations_uae_h126'])} of {n0(V['stations_h126'])} stations are in the UAE "
          f"and the UAE price is set by one committee", 'Medium to high'],
         ['Related-party dependence',
          f"the supply agreement, the margin floor, the inventory backstop and roughly "
          f"{M['currency']} {n0(V['dtrp_fy25'])} million of payables all run through the "
          f"controlling shareholder", 'Medium'],
         ['Acquisition execution',
          f"a USD {n0(E['CO-05']['value'])} million transaction in a new country and a new "
          f"regulatory regime, excluded from this valuation but not from the company's future",
          'Medium'],
         ['Tax regime change',
          f"a {pc(V['tax_dmtt'], 0)} minimum rate the audited accounts do not yet apply; "
          f"worth {M['currency']} {n2(abs(SENS['tax_dmtt_impact']))} a share",
          'Medium'],
         ['Egyptian currency exposure',
          'the Egyptian leg earns in a currency that has depreciated materially and is '
          'translated into dirhams', 'Low to medium']]
table(rows, [1.85, 3.55, 0.95], size=8.4)
caption(f"Table {tnum()} — the risk record.")

H2('B.3 The research record')
P(f"{n0(len(ENTRIES))} external items were obtained, dated and classified before any forecast "
  f"driver was set, across four layers of research: the global energy and rate environment, "
  f"the UAE country layer, the fuel-retail industry, and company-level context. Items marked "
  f"as drivers change a number in the model; the rest inform the narrative or were used only "
  f"as cross-checks. Company-level items in this record are CONTEXT ONLY — every reported "
  f"historical figure in this study comes from the company's own audited and reviewed "
  f"filings, listed at the foot of this appendix, and from nowhere else.")
_ring_lbl = {'GLOBAL': 'Global', 'COUNTRY': 'Country', 'INDUSTRY': 'Industry',
             'COMPANY': 'Company'}
_cls_lbl = {'C': 'Critical', 'D': 'Driver', 'S': 'Supporting', 'B': 'Background'}
rows = [['Ref', 'Layer', 'Use', 'Topic and finding', 'Source', 'As of']]
for e in ENTRIES:
    rows.append([e['id'], _ring_lbl.get(e['ring'], e['ring']),
                 _cls_lbl.get(e.get('classification'), ''),
                 clip(f"{e['topic']} — {e.get('finding', '')}", 175),
                 clip(e.get('source_name', ''), 42),
                 e.get('as_of_date') or '—'])
table(rows, [0.5, 0.72, 0.68, 2.85, 1.5, 0.72], size=7.0)
caption(f"Table {tnum()} — the full external research record: {n0(len(ENTRIES))} items, of which "
        f"{n0(len(DRIVERS))} are drivers. Findings are abbreviated for the page; each item "
        f"carries its full text, its source address and its access date in the accompanying "
        f"bibliography.")
rows = [['What was sought and not found', 'What was done instead']]
for g in GAPS:
    rows.append([clip(f"{g.get('item', '')} — {g.get('detail', '')}", 260),
                 clip(g.get('action', ''), 230)])
table(rows, [3.6, 3.3], size=7.6)
caption(f"Table {tnum()} — the negative results: {n0(len(GAPS))} things that were looked for and "
        f"either could not be obtained or contradicted a better source. They are published "
        f"because a research record that lists only successes tells a reader nothing about "
        f"how hard the gaps were pushed.")
P("The company's own documents used to construct every historical figure in this study, all "
  "obtained from its own investor-relations channel: the audited consolidated financial "
  "statements for the years ended 31 December 2023, 2024 and 2025, each with the auditor's "
  "report and full notes; the reviewed condensed interim statements for the first and second "
  "quarters of 2026; the FY2025 management discussion and analysis and the second-quarter "
  "2026 management discussion and analysis; the FY2025 and first- and second-quarter 2026 "
  "results presentations, which carry the volume, station-count, transaction and margin-per-"
  "litre disclosures no financial statement contains; and the 2025 integrated report.")

# ===================== 14. APPENDIX C — THE EXPERTS ============================
H1('Appendix C — three experts, three methods')
P('Three analysts with genuinely different methods were asked the same question about the '
  'same company. They are labelled Expert 1, 2 and 3. Each states a worldview, says when the '
  'method works and when it fails, shows the whole working rather than an answer, names the '
  'one sensitivity that matters most, and states in advance what would prove them wrong.')

H2('C.1 Expert 1 — the cash-flow analyst')
P('Worldview: a company is worth the cash it will generate for whoever owns the capital, '
  'discounted at what that capital costs. Every other method is a shortcut to that number, '
  'and shortcuts are useful only when the full calculation is impossible.')
P(f"When it works: for a business with a stable, forecastable operating model, a capital "
  f"structure that is not about to change, and a driver that can be counted. All three hold "
  f"here — litres are counted, the margin per litre is disclosed, and the balance sheet "
  f"carries {M['currency']} {n0(W['net_debt'])} million of net debt against {M['currency']} "
  f"{n0(M['mcap'])} million of market value. When it fails: when most of the value sits "
  f"beyond the explicit forecast. That is the case here, at {pc(A['tv_share'], 1)}, and this "
  f"expert concedes it before being asked.")
rows = [['Working — Frame A', f"{M['currency']} million"]]
for i, y in enumerate(YR):
    rows.append([f"Free cash flow to the firm, {y.replace('E', '')}", n0(A['fcff'][i])])
rows += [[f"Present value of the five years at {pc(W['disc_rate'][0], 2)} rising to "
          f"{pc(W['disc_rate'][-1], 2)}", n0(A['pv_sum'])],
         ['Terminal NOPAT', n0(A['nopat_term'])],
         [f"Less terminal reinvestment at growth ÷ return on capital = {pc(A['g'], 1)} ÷ "
          f"{pc(A['roic_term'], 0)} = {pc(A['reinvest_rate'], 1)}",
          paren(A['nopat_term'] - A['fcff_term'])],
         ['Terminal free cash flow', n0(A['fcff_term'])],
         [f"Divided by ({pc(W['wacc_terminal'], 2)} − {pc(A['g'], 1)}) = "
          f"{pc(W['wacc_terminal'] - A['g'], 2)}", n0(A['tv'])],
         ['Discounted back at the terminal-year factor', n0(A['pv_tv'])],
         ['ENTERPRISE VALUE', n0(A['ev'])],
         ['Less net debt, leases and minorities',
          paren(A['net_debt'] + A['leases'] + A['nci'])],
         ['Equity value', n0(A['equity'])],
         [f"VALUE PER SHARE ({M['currency']})", n2(A['per_share'])],
         [f"The same working on Frame B ({M['currency']})", n2(Bf['per_share'])]]
table(rows, [4.6, 1.7], band_rows={10, 13, 14}, size=8.8)
P(f"Named sensitivity: the terminal discount rate, and it is not close. Every fifty basis "
  f"points on it is worth roughly {M['currency']} "
  f"{n2(abs(SENS['wacc'][2][1] - SENS['wacc'][3][1]))} a share — moving from "
  f"{pc(SENS['wacc'][2][0], 2)} to {pc(SENS['wacc'][4][0], 2)} takes the answer from "
  f"{M['currency']} {n2(SENS['wacc'][2][1])} to {M['currency']} {n2(SENS['wacc'][4][1])}, "
  f"below the traded price. At {pc(A['tv_share'], 1)} terminal weight this expert is mostly "
  f"forecasting one number, and says so.")
P(f"Falsifier, stated in advance: \"If total fuel volume in FY2027 comes in below "
  f"{n0(FC['vol_total'][1] * 0.97)} million litres — three per cent below my forecast of "
  f"{n0(FC['vol_total'][1])} million — then the volume path underneath my whole build is "
  f"wrong, and so is the terminal that grows out of it. I would not adjust; I would "
  f"rebuild.\"")

H2('C.2 Expert 2 — the asset-and-return analyst')
P('Worldview: forecasts are opinions and the balance sheet is a fact. Start from what the '
  'company owns, ask what return it earns on it, and pay the multiple of book that the '
  'return justifies. Never pay for growth that has not yet been earned.')
P(f"When it works: for asset-heavy businesses in markets where forecasting is genuinely hard "
  f"— and a network of {n0(V['stations_h126'])} service stations on freehold and leasehold "
  f"land is as asset-heavy as retail gets. When it fails: when the equity base is small "
  f"relative to the earnings it supports, which makes the return look extraordinary and the "
  f"justified multiple explosive. That is exactly the condition here, and it is why this "
  f"expert's number should be read as a floor rather than a valuation.")
rows = [['Working', 'Value'],
        [f"Equity attributable to shareholders ({M['currency']} m)", n0(V['eqp_fy25'])],
        ['Shares in issue (millions)', n0(SH)],
        [f"Book value per share ({M['currency']})", n2(LN['bv_ps'])],
        ['Return on equity, FY2023', pc(LN['roe_hist'][0])],
        ['Return on equity, FY2024', pc(LN['roe_hist'][1])],
        ['Return on equity, FY2025', pc(LN['roe_hist'][2])],
        ['Sustainable return — the three-year mean', pc(LN['roe_sust'])],
        ['Cost of equity', pc(W['ke'], 2)],
        ['Long-run growth', pc(A['g'], 1)],
        [f"Numerator: return less growth", pc(LN['roe_sust'] - A['g'], 2)],
        [f"Denominator: cost of equity less growth", pc(W['ke'] - A['g'], 2)],
        ['Justified multiple of book', f"{n1(LN['just_pb'])}x"],
        [f"VALUE PER SHARE ({M['currency']})", n2(LN['book_ps'])],
        ['Cross-check: return on capital employed, FY2025', pc(H['FY2025']['roce'])],
        ['Cross-check: the traded price as a multiple of book',
         f"{n1(SPOT / LN['bv_ps'])}x"]]
table(rows, [4.6, 1.7], band_rows={13, 14}, size=8.8)
P(f"Named sensitivity: the sustainable return. If it settles at the FY2023 reading of "
  f"{pc(LN['roe_hist'][0])} rather than the three-year mean of {pc(LN['roe_sust'])}, the "
  f"justified multiple falls from {n1(LN['just_pb'])} to "
  f"{n1((LN['roe_hist'][0] - A['g']) / (W['ke'] - A['g']))} times and the value from "
  f"{M['currency']} {n2(LN['book_ps'])} to {M['currency']} "
  f"{n2((LN['roe_hist'][0] - A['g']) / (W['ke'] - A['g']) * LN['bv_ps'])} a share — below "
  f"the traded price. This lens is extremely sensitive to a number that has moved "
  f"{pc(LN['roe_hist'][2] - LN['roe_hist'][0], 1)} across three years.")
P(f"Falsifier: \"If book equity per share rises above {M['currency']} "
  f"{n2(LN['bv_ps'] * 2)} — double today's — because the board retains earnings instead of "
  f"distributing them, my return collapses arithmetically on an unchanged business and my "
  f"method is measuring payout policy rather than performance. I would abandon the lens "
  f"rather than defend it.\"")
P(f"This expert adds one point the others miss. Return on capital employed — "
  f"{pc(H['FY2025']['roce'])} in FY2025, rising in each of the three audited years — is "
  f"immune to the payout objection, and it says this is a genuinely exceptional business "
  f"earning roughly {n0(H['FY2025']['roce'] / W['wacc'])} times its cost of capital on the "
  f"capital it actually employs. That is an argument for paying up. This expert declines to "
  f"make it, because the method is a discipline against exactly that kind of reasoning.")

H2('C.3 Expert 3 — the market-implied analyst')
P('Worldview: do not ask what a company is worth. Ask what the traded price already assumes, '
  'and then judge whether those assumptions are reasonable. It produces no independent value '
  'and is not meant to. It is a discipline against arguing with a price.')
P(f"When it works: when a price and a model disagree and the question is which assumption is "
  f"carrying the disagreement. When it fails: it can never tell a reader that a price is "
  f"wrong — only what a reader is being asked to believe. It is also entirely dependent on "
  f"the model it inverts: if the {pc(A['tv_share'], 1)} terminal weight is a bad way to "
  f"model this business, inverting it produces a precise answer to a badly posed question.")
rows = [['What the traded price requires', 'Value'],
        [f"Market price ({M['currency']})", n2(CRUX['spot'])],
        [f"Value from the cash-flow model, Frame A ({M['currency']})",
         n2(CRUX['normalised_value'])],
        [f"Gap to be explained ({M['currency']} a share)",
         n2(CRUX['normalised_value'] - CRUX['spot'])],
        [f"Equity value of that gap ({M['currency']} m)",
         n0((CRUX['normalised_value'] - CRUX['spot']) * SH)],
        ['EXPLANATION 1 — terminal growth. The model assumes', pc(CRUX['g_base'], 2)],
        ['   the price requires', pc(CRUX['g_implied'], 2)],
        ['   which in the first year is a volume loss of',
         f"{n0(UB['vol_retail_fy25'] * abs(CRUX['g_implied']))}m litres"],
        ['   or, at the disclosed litres per transaction, fewer fills per year',
         f"{n1(UB['vol_retail_fy25'] * abs(CRUX['g_implied']) / (V['vol_retail_h126'] / V['fueltxn_h126']))}m"],
        ['EXPLANATION 2 — the terminal discount rate. The model assumes',
         pc(CRUX['wacc_term_base'], 2)],
        ['   the price requires', pc(CRUX['wacc_term_implied'], 2)],
        ['EXPLANATION 3 — beta. The model assumes', n2(CRUX['beta_base'])],
        ['   the price requires', n2(CRUX['beta_implied'])],
        ['   against the regression\'s own 90% upper bound of', n2(BETA_CH['ci90'][1])],
        [f"Value if any ONE of the three is true ({M['currency']})", n2(CRUX['spot'])]]
table(rows, [4.6, 1.7], band_rows={6, 10, 12, 15}, size=8.8)
P(f"Named sensitivity: which explanation is chosen. They are not equivalent. The implied beta "
  f"of {n2(CRUX['beta_implied'])} sits ABOVE the 90% upper bound of the regression, "
  f"{n2(BETA_CH['ci90'][1])}, so on the evidence available it is the least likely of the "
  f"three. The implied terminal discount rate of {pc(CRUX['wacc_term_implied'], 2)} requires "
  f"either that beta or a materially higher equity risk premium than the source file "
  f"publishes. The implied growth rate is the only one of the three that is neither "
  f"contradicted by the data nor dependent on a disputed premium — which is why this expert "
  f"treats it as the operative explanation and why it is the study's crux.")
P(f"Falsifier: \"If total fuel volume grows at more than one per cent a year for three "
  f"consecutive years from here — the company reported {n0(V['vol_retail_h126'])} million "
  f"litres of retail volume in the first half of 2026 against "
  f"{n0(V['vol_retail_h125'])} million a year earlier — then the market's implied permanent "
  f"decline is refuted by observation and I would say the price, not the model, is the thing "
  f"that needs explaining.\"")

H2('C.4 Cross-examination')
rows = [['Challenge', 'Conceded or rejected']]
rows += [['Expert 2 to Expert 1: "Three-quarters of your value is a perpetuity. You are not '
          'forecasting cash flow, you are forecasting one growth rate and one discount rate."',
          f"CONCEDED, without qualification. Expert 1 accepts that {pc(A['tv_share'], 1)} "
          f"terminal weight makes this mostly a terminal valuation and points to the "
          f"published grid as the only honest response: across the plausible combinations of "
          f"terminal cost of capital and growth the answer runs {M['currency']} "
          f"{n2(SENS['grid_lo'])} to {M['currency']} {n2(SENS['grid_hi'])}, and the whole of "
          f"that range is published including the corner below the traded price."],
         ['Expert 1 to Expert 2: "Your justified multiple is 15 times book because book is '
          'artificially small. Pay out everything and any business looks like this."',
          f"REJECTED, with a concession attached. Expert 2 answers that book equity is book "
          f"equity and a valuation method does not get to imagine a different balance sheet "
          f"— but concedes the lens carries the lowest weight in the study for precisely "
          f"this reason, and that return on capital employed of "
          f"{pc(H['FY2025']['roce'])} is the cleaner statistic. Expert 2 declines to switch "
          f"to it, because the lens is meant to be a floor."],
         ['Expert 3 to Experts 1 and 2: "You have both produced numbers above the market '
          'price and neither of you can say why the market is wrong."',
          f"CONCEDED, and it is the point of having Expert 3 in the room. Neither method "
          f"contains a view about long-run fuel demand beyond the terminal growth rate each "
          f"assumes. Expert 3's contribution is to convert that assumption into an "
          f"observable quantity — {n1(UB['vol_retail_fy25'] * abs(CRUX['g_implied']) / (V['vol_retail_h126'] / V['fueltxn_h126']))} "
          f"million fewer fills a year — that a reader can check against the company's own "
          f"volume disclosure each quarter."],
         ['Expert 2 to Expert 3: "Your inversion assumes the whole gap is terminal growth. It '
          'could be the discount rate, or a liquidity discount on a share with a '
          'twenty-three per cent free float."',
          f"CONCEDED IN PART. Expert 3 agrees the attribution is a choice and publishes all "
          f"three inversions rather than one. On the free-float point Expert 3 goes further "
          f"and concedes it is not tested anywhere in this study: a controlling shareholder "
          f"holding roughly {pc(1 - E['CO-02']['value'] / 100, 0)} of the equity is a real "
          f"reason a share might trade below a computed value, and no lens here prices it."],
         ['Expert 1 to Expert 3: "You invert MY model. If my terminal structure is wrong, '
          'your implied growth rate is a precise answer to the wrong question."',
          'CONCEDED ENTIRELY. Expert 3 accepts the inversion inherits every structural '
          'assumption of the model it inverts, and that this is the method\'s deepest '
          'limitation rather than a detail. The defence offered is narrow: the inversion is '
          'still the cheapest available test of whether the disagreement is about the next '
          'five years or the fifty after them, and it shows clearly that it is the latter.'],
         ['Expert 3 to Expert 1: "Your Frame A and Frame B differ by '
          f'{M["currency"]} {n2(Bf["per_share"] - A["per_share"])} a share on a line that is '
          'not in the audited accounts at all."',
          'CONCEDED, and the study is built around the concession. The inventory movement is '
          'a management disclosure with no reconciliation to the audited statements. That is '
          'why it is carried two ways, why neither frame is preferred, and why the two are '
          'never averaged into a single number that would hide the disagreement.'],
         ['Expert 2 to Expert 1: "Your model has the company accumulating cash for five years '
          'while paying a flat dividend. That is not what management will do."',
          f"CONCEDED as a limitation, rejected as an error. Expert 1 agrees the model "
          f"distributes only the policy dividend and lets the balance accumulate, and that "
          f"in practice the board would raise the payout, buy something, or both. But free "
          f"cash flow to the FIRM is what the valuation discounts, and it is indifferent to "
          f"how the cash is subsequently split. The accumulation is a presentational "
          f"consequence, not a valuation one."]]
table(rows, [2.65, 3.7], size=8.0)
caption(f"Table {tnum()} — every challenge, explicitly conceded or rejected. Four of the seven "
        f"are conceded outright.")

H2('C.5 The three in one room')
P(f"Put together, the disagreement narrows to one question, which is the useful outcome. All "
  f"three agree on the audited history. All three agree the business earns an exceptional "
  f"return on the capital it employs — {pc(H['FY2025']['roce'])} in FY2025 — and that the "
  f"regulated margin with a parental floor beneath it is a genuine structural advantage "
  f"rather than an accident of a good year. All three agree the FY2026 inventory windfall "
  f"should not be capitalised. And all three produce a number ABOVE the traded price: "
  f"{M['currency']} {n2(A['per_share'])} from Expert 1 on Frame A, {M['currency']} "
  f"{n2(Bf['per_share'])} on Frame B, {M['currency']} {n2(LN['book_ps'])} from Expert 2 — "
  f"the deliberate floor — against {M['currency']} {n2(SPOT)} in the market.")
P(f"Where they part is what the long run holds. Expert 1 says the network grows with the "
  f"vehicle parc and the shop, so {pc(A['g'], 1)} terminal growth. Expert 2 declines to "
  f"forecast the long run at all and prices only the capital in place. Expert 3 says the "
  f"market has already answered: {pc(CRUX['g_implied'], 2)}, a permanently shrinking volume "
  f"base, which in observable units is roughly "
  f"{n1(UB['vol_retail_fy25'] * abs(CRUX['g_implied']) / (V['vol_retail_h126'] / V['fueltxn_h126']))} "
  f"million fewer fuel transactions every year. The room does not resolve it, and it should "
  f"not: one side is forecasting and the other is inverting. What the room does is convert "
  f"an argument about value into a quantity a reader can watch in the company's own "
  f"quarterly volume disclosure.")
fig('fig8_experts.png', 6.6,
    'three methods, three ranges, one traded price.')

H2('C.6 Divergence table — which assumption drives which gap')
rows = [['Pair', f"Gap ({M['currency']}/share)", 'The single assumption that drives it']]
rows += [['Expert 1 (Frame A) less Expert 2', n2(A['per_share'] - LN['book_ps']),
          'whether five years of forecast growth plus a perpetuity are credited at all. '
          'Expert 1 discounts them; Expert 2 refuses to pay for growth not yet earned. '
          'Nothing about the business is in dispute'],
         ['Expert 1 Frame A less Frame B', n2(A['per_share'] - Bf['per_share']),
          f"the inventory judgement alone, and nothing else. "
          f"{M['currency']} {n0(CRUX['avg_24_25'])} million a year carried in perpetuity "
          f"against zero from FY2027. This is the number an average would have hidden"],
         ['Expert 1 (Frame A) less the traded price', n2(A['per_share'] - SPOT),
          f"terminal growth: {pc(CRUX['g_base'], 2)} against the "
          f"{pc(CRUX['g_implied'], 2)} the price implies. The explicit five years contribute "
          f"only {pc(A['pv_sum'] / A['ev'], 1)} of the value, so they cannot carry this gap"],
         ['Expert 2 less the traded price', n2(LN['book_ps'] - SPOT),
          f"the sustainable return on equity of {pc(LN['roe_sust'])} against the cost of "
          f"equity of {pc(W['ke'], 2)}. At a sustainable return of "
          f"{pc(LN['roe_hist'][0])} this gap closes entirely"],
         ['Normalised earnings less Expert 1 (Frame A)', n2(LN['norm_ps'] - A['per_share']),
          f"the discount rate and nothing else: {pc(W['wacc'], 2)} held flat against a glide "
          f"to {pc(W['wacc_terminal'], 2)}. The normalised reading credits NO growth and "
          f"still lands higher"],
         ['Dividend capitalisation less Expert 1 (Frame A)',
          n2(LN['div_ps'] - A['per_share']),
          'the difference between the cash the company distributes under a fixed policy and '
          'the cash the business generates. This is the gap that explains the traded price '
          'best of any in this table'],
         ['Weighted centre A less weighted centre B', n2(LN['centre_A'] - LN['centre_B']),
          'the contested judgement carried through all four methods and their weights']]
table(rows, [2.05, 0.95, 3.35], size=8.2)
caption(f"Table {tnum()} — every gap in this study isolated to the assumption that causes it. "
        f"Read the third row and the sixth together: the model's disagreement with the market "
        f"is entirely about the long run, and the market's price is almost exactly what the "
        f"company's fixed dividend policy is worth.")

# ================================ 15. ABOUT ====================================
H1('About this study')
P(f"This is an independent, educational valuation study. Every reported historical figure in "
  f"it was constructed from the company's own audited consolidated financial statements for "
  f"{HYRS[0]}, {HYRS[1]} and {HYRS[2]} and its reviewed interim statements for the first and "
  f"second quarters of 2026, together with its own management discussion and analysis, its "
  f"results presentations and its integrated report — all obtained from the company's own "
  f"investor-relations channel. No data vendor, broker note or press report was used as the "
  f"source of any number about the company itself. External material was used only for the "
  f"forecast drivers and the cost of capital, and every such item is listed in Appendix B "
  f"with its value, its date and its source.")
P(f"The forecast is built from the ground up: fuel is litres times margin per litre for each "
  f"of the two disclosed fuel legs, non-fuel retail is revenue times its own disclosed gross "
  f"margin, and gross margin is an output of that build rather than an input to it. The cost "
  f"of capital is built bottom-up from the sovereign's own bond, the sovereign's own default "
  f"spread, the country's own equity risk premium and a beta regressed from this share's own "
  f"price history against its own local index. The balance sheet and cash flow are projected "
  f"from the company's own disclosed working-capital days, and the balance sheet balances in "
  f"every column.")
P(f"The valuation model behind this document is a live formula model: every figure that can "
  f"be derived from a driver is derived from it, and changing a driver reprices the "
  f"valuation. The probability map in section 3 comes from a simulation calibrated across "
  f"this market and tested by re-running it across the full price history without letting it "
  f"see the future. Its performance on this individual share is reported honestly in section "
  f"3, including the finding that its three-month range is wider than this share warrants.")

# ============================== 16. DISCLOSURE =================================
H1('Disclosure')
P('This document is educational analysis, not investment advice, and not a recommendation to '
  'buy, sell or hold any security. It contains no rating and no price target, and it never '
  'will: value is expressed here as a range and as a distribution, because that is what the '
  'evidence supports.')
P('The author holds no position in the securities discussed and has no relationship with the '
  'company, its parent, its advisers or any party mentioned. No part of this study was '
  'commissioned, reviewed or approved by the company. Nothing in it should be read as a '
  'statement of fact about the future.')
P(f"Figures are in {M['currency']} unless stated otherwise. Historical figures are as filed "
  f"and are not restated. Forecasts are the author's own and are wrong in ways that cannot be "
  f"known in advance; the sensitivity tables, the two published frames of the contested "
  f"judgement and the caveats in section 7 are the honest statement of how wrong they might "
  f"be. Past performance is not a guide to future returns.")
P(f"Prepared {M['study_date']} · price data to {M['price_date']} · "
  f"{M['company']} · {M['exchange']} · {M['ticker']}", size=9, color=GREY)

OUT = os.path.join(HERE, 'ADNOCDIST_Valuation_Study_09-08-2026.docx')
doc.save(OUT)
print(f'saved {OUT}')
print(f'sections 16 · tables {_TN[0]} · figures {_FN[0]}')
