"""EIPICO_Valuation_Study_09-08-2026.docx — the 16-section study.

Written for an EXTERNAL reader: no internal procedure vocabulary anywhere, no verdict
tokens, no calibration appendix. The calibration evidence appears inside section 3 as
plain-language sentences with the statistics inline. Experts are labelled Expert 1, 2 and 3.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docx_base as B
from docx.shared import Pt, Inches

doc, P, H1, H2, rich, table, figure, box, bullet, caption, masthead = (
    B.doc, B.P, B.H1, B.H2, B.rich, B.table, B.figure, B.box, B.bullet, B.caption, B.masthead)
INK, GREY, BRASS, GOLD = B.INK, B.GREY, B.BRASS, B.GOLD

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
M, H, FC, W, DCFD, LN = D['meta'], D['history'], D['forecast'], D['wacc'], D['dcf'], D['lenses']
UB, SENS, CAL, CRUX, WC = D['unit_build'], D['sensitivity'], D['calibration'], D['crux'], \
    D['working_capital']
V = {k: v['value'] for k, v in D['inputs'].items()}
TECH = json.load(open(os.path.join(HERE, 'technicals.json')))
STRIKE = json.load(open(os.path.join(HERE, 'strike_result.json')))
BT = CAL['backtest']
SPOT, SH = M['spot'], M['shares_mn']
YR = ['FY2026E', 'FY2027E', 'FY2028E', 'FY2029E', 'FY2030E']
A, Bf = DCFD['frame_A'], DCFD['frame_B']
ASSOC_SA_FY25, ASSOC_SA_FY24 = 427.906046, 190.021502   # note (33), by associate
PEER_HI, PEER_MID = 26.7, 16.0                          # market data, cross-check


def n0(x): return f'{x:,.0f}'
def n1(x): return f'{x:,.1f}'
def n2(x): return f'{x:,.2f}'
def pc(x, d=1): return f'{x * 100:.{d}f}%'


# ============================= 1. MASTHEAD + READ FIRST =======================
masthead()
P('Egyptian International Pharmaceutical Industries Company (EIPICO)', size=21, bold=True,
  space_after=1)
P('Independent valuation study · The Egyptian Exchange · ticker PHAR · Egyptian pounds',
  size=11.5, color=GREY, space_after=2)
P(f'Prepared 9 August 2026 · share price EGP {n2(SPOT)} at the close of 6 August 2026 · '
  f'{SH:,.3f} million shares in issue', size=10, color=GREY, space_after=12)

H1('Read first')
box([('What this is. ',
      'An independent, educational valuation of a listed Egyptian pharmaceutical '
      'manufacturer, built from the company\'s own audited financial statements. It contains '
      'no rating, no recommendation and no price target. It expresses value as a RANGE and, '
      'separately, as a probability distribution.'),
     ('What it is built on. ',
      'Four consecutive years of audited consolidated financial statements — FY2022 through '
      'FY2025 — with the auditor\'s report and full notes, together with the board of '
      'directors\' own operating statistics and the company\'s investor presentation. Every '
      'historical figure in this study traces to one of those documents. No data vendor, '
      'broker note or press report is used to build any number about the company itself.'),
     ('The one number to hold on to. ',
      f'Five independent lenses put fair value between EGP {n0(LN["fair_bear"])} and EGP '
      f'{n0(LN["fair_bull"])} a share, weighted centre EGP {n0(LN["fair_base"])}. The market '
      f'price is EGP {n2(SPOT)}. That gap is the study, and section 1.7 states exactly what '
      f'would have to be true for the market to be right.'),
     ('What this study deliberately does NOT do. ',
      'It does not put a revenue line on the company\'s new biologicals plant, because the '
      'company has published no volume, price or utilisation guidance for it. It charges the '
      'plant\'s depreciation and its interest, because both follow mechanically from the '
      'licence the company obtained in December 2025. Section 1.7 then solves for how much '
      'the plant must sell to justify the market price and states that in observable units.'),
     ('This is the second edition. ',
      'It folds in the reviewed first quarter of 2026 and the separately issued audited '
      'FY2023 and FY2024 statements, obtained after the first issue. The first quarter '
      'CONFIRMED the study\'s central mechanism — the construction balance is transferring '
      'and the depreciation charge has more than doubled — but it also came in softer than '
      'the first edition assumed on revenue, associates and capital spending. The weighted '
      f'central value moves from EGP 79.64 to EGP {n0(LN["fair_base"])} a share. Section 7 '
      'lists what changed and by how much.'),
     ('The first-quarter review is QUALIFIED. ',
      'The auditor qualified the conclusion on three matters: the associates\' own periodic '
      'statements were not received; the active-ingredient company was recognised at cost '
      'after loss of control rather than remeasured and equity-accounted; and NO '
      'expected-credit-loss charge was recognised in the quarter. The third goes straight to '
      'this study\'s contested judgement and is the reason it is still carried both ways.'),
     ('The contested judgement is carried both ways. ',
      'The credit-loss and provision charge is the study\'s single most consequential '
      'contested judgement. It is computed on two frames and both are published side by '
      'side, in the summary table, in the body, in the workbook and in an expert\'s range. '
      'They are never averaged into one number.')])

# ================================== 2. HEADLINE ================================
H1('Headline')
P(f'EIPICO is Egypt\'s largest pharmaceutical manufacturer by units and its largest '
  f'pharmaceutical exporter, and it has just finished building something big. Revenue grew '
  f'{pc(V["rev_fy25"] / V["rev_fy24"] - 1)} in FY2025 to EGP {n0(V["rev_fy25"])} million, '
  f'attributable profit rose {pc(V["parent_fy25"] / V["parent_fy24"] - 1)} to '
  f'EGP {n0(V["parent_fy25"])} million, and the shares have roughly doubled this year. The '
  f'question this study asks is not whether the business is good. It is whether EGP '
  f'{n2(SPOT)} a share already pays for a plant that has not yet sold anything.')
P(f'The company spent the last three years building EIPICO 3, a biologicals and biosimilars '
  f'facility it describes as the first in Egypt to manufacture from cell culture through to '
  f'finished product, at a stated cost of USD 100 million. At 31 December 2025 the '
  f'construction balance stood at EGP {n0(V["cip_fy25"])} million — larger than the entire '
  f'depreciated property base of EGP {n0(V["ppe_fy25"])} million. The Egyptian Drug Authority '
  f'licensed it in December 2025. From FY2026 that balance starts depreciating, and the '
  f'interest that was being capitalised into it starts hitting the income statement. Those '
  f'two mechanical changes take roughly EGP 700 million a year out of reported profit before '
  f'the plant contributes a pound of revenue.')
P(f'Against that, four lenses that do not depend on the new plant at all — discounted cash '
  f'flow on two framings of the provision charge, book value against sustainable return, '
  f'triangulated multiples, and normalised earnings power — cluster between EGP '
  f'{n0(LN["fair_bear"])} and EGP {n0(LN["fair_bull"])}. The market is above all of them.')
P(f'The first quarter of 2026, reviewed and published in May, settles part of that question '
  f'and sharpens the rest. Fixed assets rose EGP {n0(V["q1_ppe"] - V["ppe_fy25"])} million and '
  f'the construction balance fell EGP {n0(V["cip_fy25"] - V["q1_cip"])} million in three '
  f'months; depreciation and amortisation went to EGP {n1(V["q1_dna"])} million from EGP '
  f'{n1(V["q1_dna_ly"])} million a year earlier, more than double. The plant is in service and '
  f'the charge has arrived, exactly as this study said it would. What has not arrived is the '
  f'revenue: net sales grew {pc(V["q1_rev"] / V["q1_rev_ly"] - 1)} and attributable profit '
  f'FELL {pc(abs(V["q1_parent"] / V["q1_parent_ly"] - 1))} to EGP {n0(V["q1_parent"])} million.')
figure(os.path.join(HERE, 'fig1_field.png'), 6.9,
       'Figure 1 — five independent routes to a value per share, against the market price.')

# ============================ 3. VALUATION SUMMARY =============================
H1('Valuation summary')
rows = [['Lens', 'EGP / share', 'vs market', 'Note']]
for it in LN['items']:
    note = ''
    if it['name'].endswith('Frame A'):
        note = f"terminal value {pc(A['tv_share'], 0)} of enterprise value"
    elif it['name'].endswith('Frame B'):
        note = f"terminal value {pc(Bf['tv_share'], 0)} of enterprise value"
    elif it['name'].startswith('Book'):
        note = f"justified {n2(LN['just_pb'])}x book of EGP {n2(LN['bv_ps'])}"
    elif it['name'].startswith('Relative'):
        note = 'three multiples averaged, not asserted'
    else:
        note = f"three-year average margin {pc(LN['norm_margin'])}"
    rows.append([it['name'], n2(it['value']), pc(it['value'] / SPOT - 1, 0), note])
rows.append(['Weighted central fair value', n2(LN['fair_base']),
             pc(LN['fair_base'] / SPOT - 1, 0), 'A range, not a target'])
rows.append(['Field low to field high', f"{n2(LN['fair_bear'])} – {n2(LN['fair_bull'])}", '',
             'The spread between the lenses IS the uncertainty'])
rows.append(['Market price', n2(SPOT), '', 'Close of 6 August 2026'])
table(rows, [2.35, 1.05, 0.85, 2.75], band_rows={6, 8}, size=9.0)
caption('Table 1 — the summary valuation table. Terminal value as a percentage of enterprise '
        'value is stated beside the cash-flow lens rather than left in the workbook.')

rows = [['Key figures', 'Value', 'Key figures', 'Value']]
kf = [('Market capitalisation', f"EGP {n0(W['mcap'])}m"),
      ('Net debt', f"EGP {n0(W['net_debt'])}m"),
      ('Enterprise value', f"EGP {n0(W['mcap'] + W['net_debt'] + V['nci_fy25'])}m"),
      ('FY2025 revenue', f"EGP {n0(V['rev_fy25'])}m"),
      ('FY2025 EBITDA', f"EGP {n0(H['FY2025']['ebitda'])}m"),
      ('FY2025 attributable profit', f"EGP {n0(V['parent_fy25'])}m"),
      ('Trailing price / earnings', f"{n1(LN['pe_now'])}x"),
      ('Trailing enterprise value / EBITDA', f"{n1(LN['evebitda_now'])}x"),
      ('Cost of equity', pc(W['ke'], 2)),
      ('Discount rate, first year', pc(W['wacc0'], 2)),
      ('Discount rate, terminal', pc(W['wacc_term'], 2)),
      ('Proposed dividend, FY2025', f"EGP {n2(V['dps_fy25'])} ({pc(V['q_annual'])} yield)")]
for i in range(0, len(kf), 2):
    rows.append([kf[i][0], kf[i][1], kf[i + 1][0], kf[i + 1][1]])
table(rows, [2.2, 1.3, 2.2, 1.3], size=9.0)
caption('Table 2 — the figures a reader needs before anything else.')

# ============================= 4. COMPANY OVERVIEW =============================
H1('Company overview')
P('EIPICO was founded in 1980 in Tenth of Ramadan City with capital of EGP 7 million and '
  'began producing in 1985. It is today the largest operating subsidiary of the Arab Company '
  'for Drug Industries and Medical Appliances, which holds 51.34% of its shares. The '
  'rest of the share list is dominated by medical-profession institutions — an investment '
  'company, the professions federation and its pension fund together hold a further 12.02% — '
  'with 36.64% in other hands.')
P(f'The business is a vertically integrated generic and branded pharmaceutical manufacturer. '
  f'It runs 54 production lines across three plants, produced {n0(V["units_prod_fy25"])} '
  f'million units in FY2025 against {n0(V["units_cap"])} million of its own disclosed '
  f'capacity, and sold {n1(V["packs_sold_fy25"])} million packs of '
  f'{V["products_fy25"]} registered preparations across 27 therapeutic groups. It employs '
  f'about {n0(V["employees_fy25"])} people. It makes its own primary packaging through a '
  f'wholly-owned ampoule and vial subsidiary and a plastics factory, which is why the '
  f'packaging cost line is only partly exposed to imports.')
rows = [['Revenue channel', 'FY2024 (EGP m)', 'FY2025 (EGP m)', 'Growth', 'Share of FY2025']]
tot25 = (V['ch_direct_fy25'] + V['ch_distrib_fy25'] + V['ch_tender_fy25'] +
         V['ch_export_fy25'] + V['ch_toll_fy25'])
for nm, k in (('Direct domestic sales', 'direct'), ('Domestic distributors', 'distrib'),
              ('Government tenders and supply', 'tender'), ('Export', 'export'),
              ('Contract manufacturing', 'toll')):
    a24, a25 = V[f'ch_{k}_fy24'], V[f'ch_{k}_fy25']
    rows.append([nm, n0(a24), n0(a25), pc(a25 / a24 - 1, 0), pc(a25 / tot25, 0)])
rows.append(['Total (company only)', n0(V['rev_fy24'] / UB['consol_uplift']), n0(tot25),
             '', '100%'])
table(rows, [2.15, 1.25, 1.25, 0.85, 1.2], band_rows={6}, size=9.0)
caption('Table 3 — the disclosed revenue split. Exports are 32% of the book and are earned in '
        'hard currency; the domestic price is set administratively by the Egyptian Drug '
        'Authority.')
P(f'Two things about this company are unusual enough to change how it must be valued. First, '
  f'it is nearly currency-neutral on its balance sheet: the audited note shows a net monetary '
  f'position of minus USD 0.5 million at the year end, against a company that earns USD '
  f'{n0(V["export_usd_fy25"])} million of export revenue. It hedges by matching, not by '
  f'contract. Second, its two equity-accounted associates contributed EGP '
  f'{n0(V["assoc_fy25"])} million in FY2025 — {pc(V["assoc_fy25"] / V["parent_fy25"], 0)} of '
  f'attributable profit — against a carrying value of only EGP {n0(V["assoc_bv_fy25"])} '
  f'million. Carrying value is not a usable proxy for what that stake is worth, so this study '
  f'values it on its earnings instead.')

# ===================== 5. SECTION 1 — FUNDAMENTAL VALUATION ====================
H1('1. Fundamental valuation')
H2('1.1 The cash-flow model')
P(f'The company is valued as an operating business: free cash flow to the firm over five '
  f'explicit years, discounted on a rate that glides from today\'s cost of capital to a '
  f'normalised one, plus a terminal value. Frame A of the contested provision judgement is '
  f'shown here in full; Frame B differs only in that one line and is carried through to its '
  f'own value per share.')
hdr = ['EGP million'] + YR
rows = [hdr]
for label, key in (('Revenue', 'revenue'), ('EBITDA', None)):
    if key:
        rows.append([label] + [n0(x) for x in FC[key]])
rows.append(['EBITDA'] + [n0(FC['ebit_A'][i] + FC['dna'][i]) for i in range(5)])
rows.append(['EBITDA margin'] + [pc((FC['ebit_A'][i] + FC['dna'][i]) / FC['revenue'][i])
                                 for i in range(5)])
rows.append(['Less depreciation and amortisation'] + [f'({n0(x)})' for x in FC['dna']])
rows.append(['EBIT'] + [n0(x) for x in FC['ebit_A']])
rows.append(['Tax rate'] + [pc(V['tax_stat'], 1)] * 5)
rows.append(['NOPAT = EBIT x (1 − tax rate)'] +
            [n0(x * (1 - V['tax_stat'])) for x in FC['ebit_A']])
rows.append(['Add back depreciation and amortisation'] + [n0(x) for x in FC['dna']])
rows.append(['Less capital expenditure'] + [f'({n0(x)})' for x in FC['capex']])
rows.append(['Less increase in working capital'] +
            [f'({n0(x)})' if x >= 0 else n0(-x) for x in FC['dwc']])
rows.append(['Free cash flow to the firm'] + [n0(x) for x in A['fcff']])
rows.append(['Discount rate'] + [pc(x, 2) for x in W['disc_rate']])
rows.append(['Discount factor'] + [f'{x:.4f}' for x in W['df']])
rows.append(['Present value of free cash flow'] + [n0(x) for x in A['pv']])
table(rows, [2.35, 0.92, 0.92, 0.92, 0.92, 0.92], band_rows={4, 8, 12, 15}, size=8.6)
caption('Table 4 — the full free-cash-flow waterfall through to present value, Frame A.')

rows = [['Enterprise value to equity value', 'EGP million', 'EGP / share'],
        ['Present value of five years of free cash flow', n0(A['pv_sum']),
         n2(A['pv_sum'] / SH)],
        ['Present value of the terminal value', n0(A['pv_tv']), n2(A['pv_tv'] / SH)],
        ['Core enterprise value', n0(A['ev_core']), n2(A['ev_core'] / SH)],
        ['Terminal value as a percentage of enterprise value', pc(A['tv_share'], 0), ''],
        ['Add: equity-accounted associates on normalised earnings',
         n0(A['assoc_value']), n2(A['assoc_value'] / SH)],
        ['Add: assets held for sale', n0(V['afs_fy25']), n2(V['afs_fy25'] / SH)],
        ['Total enterprise value', n0(A['ev_total']), n2(A['ev_total'] / SH)],
        ['Less: net debt', f"({n0(A['net_debt'])})", f"({n2(A['net_debt'] / SH)})"],
        ['Less: non-controlling interests', f"({n0(A['nci'])})", f"({n2(A['nci'] / SH)})"],
        ['Equity value — Frame A', n0(A['equity']), n2(A['per_share'])],
        ['Equity value — Frame B', n0(Bf['equity']), n2(Bf['per_share'])]]
table(rows, [3.55, 1.6, 1.55], band_rows={4, 8, 11, 12}, size=9.0)
caption('Table 5 — the enterprise-to-equity bridge. Terminal value as a percentage of '
        'enterprise value is shown as a line of the bridge, not buried in a footnote.')

H2('1.2 Book value and sustainable return')
P(f'Book value attributable to shareholders was EGP {n0(V["equity_parent_fy25"])} million at '
  f'the year end, EGP {n2(LN["bv_ps"])} a share. Return on average equity was '
  f'{pc(LN["roe_fy24"])} in FY2024 and {pc(LN["roe_fy25"])} in FY2025; the forecast settles '
  f'at {pc(LN["roe_sust"])}. A business earning {pc(LN["roe_sust"])} on equity while its '
  f'perpetual cost of equity is {pc(W["ke_term"], 2)} is worth more than its book: the '
  f'multiple that relationship justifies is (return less growth) over (cost of equity less '
  f'growth), or {n2(LN["just_pb"])} times book — EGP {n2(LN["book_ps"])} a share.')

H2('1.3 Relative multiples')
P(f'The company\'s own traded history is the primary anchor here, because it is computable '
  f'entirely from primary material: audited attributable profit against the year-end close. '
  f'It traded on ' +
  ', '.join(f"{o['pe']:.1f} times in {o['year']}" for o in LN['own_pe_history']) +
  f' — a four-year mean of {n1(LN["own_pe_mean"])}. At EGP {n2(SPOT)} it trades on '
  f'{n1(LN["pe_now"])} times trailing attributable earnings and {n1(LN["evebitda_now"])} '
  f'times trailing EBITDA. The earnings multiple has more than doubled against its own '
  f'four-year history. That is the single most important fact about this share price.')
rows = [['Multiple', 'Times', 'EGP / share', 'Where it comes from']]
for nm, mult, val_ in LN['rel_triangulation']:
    rows.append([nm, f'{mult:.1f}x', n2(val_),
                 {'Justified forward multiple from this model':
                  f"retention must equal growth {pc(V['g_term'], 0)} over sustainable return "
                  f"{pc(LN['roe_sust'])}, so payout is {pc(LN['payout_implied'], 0)}",
                  "The company's own four-year mean multiple":
                  'year-end closes against audited attributable profit',
                  'Regional peer median, cost-of-equity adjusted':
                  'peers face a cost of equity near 10%, not '
                  f"{pc(W['ke_term'], 1)}"}[nm]])
rows.append(['Average of the three — the relative lens',
             f"{sum(t[1] for t in LN['rel_triangulation']) / 3:.1f}x", n2(LN['rel_ps']),
             'Averaged on the sheet, not asserted'])
table(rows, [2.05, 0.7, 0.95, 3.0], band_rows={4}, size=8.8)
caption('Table 6 — three multiples triangulated. Left unadjusted for the cost-of-equity gap, '
        f'the regional peer median alone would give EGP {n2(LN["rel_peer_unadjusted"])} a '
        f'share; the size of that gap IS the country-risk discount, shown rather than hidden.')
figure(os.path.join(HERE, 'fig4_multiple.png'), 6.6,
       'Figure 2 — the traded multiple against its own history and against what the model '
       'justifies.')

H2('1.4 Normalised earnings power')
P(f'FY2025 was the best operating year in the company\'s history: a {pc(H["FY2025"]["ebit_margin"])} '
  f'operating margin against {pc(H["FY2023"]["ebit_margin"])} in FY2023 and '
  f'{pc(H["FY2024"]["ebit_margin"])} in FY2024. This lens deliberately gives part of that '
  f'back. Applying the three-year average margin of {pc(LN["norm_margin"])} to FY2027 '
  f'revenue, financing it at that year\'s cost of debt, taxing it at {pc(V["tax_eff_fwd"])} '
  f'and adding the normalised associate contribution gives EGP {n2(LN["norm_pat_ps"])} a '
  f'share of sustainable earnings. Capitalised at the PERPETUAL cost of equity of '
  f'{pc(W["ke_term"], 2)} less {pc(V["g_term"], 0)} growth, on the '
  f'{pc(LN["payout_implied"], 0)} payout that growth rate permits, that is EGP '
  f'{n2(LN["norm_ps"])} a share. Using today\'s crisis-level cost of equity of '
  f'{pc(W["ke"], 2)} in a perpetuity would be a category error: a steady-state multiple takes '
  f'a steady-state rate.')

H2('1.5 Synthesis — four methods, one field')
P(f'The five values run from EGP {n0(LN["fair_bear"])} to EGP {n0(LN["fair_bull"])}. That '
  f'spread is not a failure of the methods; it is the honest measure of how much the answer '
  f'depends on which question you ask. The cash-flow lenses, which see the new plant\'s costs '
  f'but not its revenue, sit at the top of the field. The relative lens, which prices the '
  f'company on what its own economics justify, sits at the bottom. The weighted centre is EGP '
  f'{n0(LN["fair_base"])}, against a market price of EGP {n2(SPOT)}.')

H2('1.6 Drivers — every segment grown on its own driver')
P(f'Revenue is not grown as a percentage. Each book is built from a volume and a price, both '
  f'taken from disclosure. The company sold {n1(V["packs_own_fy25"])} million packs of its own '
  f'preparations in FY2025; the investor presentation puts export volume at '
  f'{n0(UB["exp_packs_fy25"])} million packs. The difference — {n1(UB["dom_packs_fy25"])} '
  f'million packs — is the domestic book, carrying EGP {n0(UB["dom_rev_fy25"])} million of '
  f'revenue, or EGP {n2(UB["dom_price_fy25"])} a pack, against EGP {n2(UB["dom_price_fy24"])} '
  f'in FY2024. Exports realise USD {n2(UB["exp_price_usd_fy25"])} a pack. Margins are an '
  f'OUTPUT of this build, never an input.')
rows = [['Driver'] + YR]
rows.append(['Domestic packs (million)'] + [n1(x) for x in FC['dom_packs']])
rows.append(['Domestic price per pack (EGP)'] + [n2(x) for x in FC['dom_price']])
rows.append(['Export packs (million)'] + [n1(x) for x in FC['exp_packs']])
rows.append(['Export price per pack (USD)'] + [n2(x) for x in FC['exp_price_usd']])
rows.append(['Exchange rate (EGP per USD)'] + [n1(x) for x in FC['fx']])
rows.append(['Revenue (EGP million)'] + [n0(x) for x in FC['revenue']])
rows.append(['Gross margin (an output)'] + [pc(x) for x in FC['gross_margin']])
table(rows, [2.35, 0.92, 0.92, 0.92, 0.92, 0.92], band_rows={7}, size=8.8)
caption('Table 7 — the forecast driver table. Volume and price move separately, in the '
        'currency each is actually earned in.')
figure(os.path.join(HERE, 'fig2_volume_price.png'), 6.9,
       'Figure 3 — revenue by book, and the volumes and prices underneath it.')

P('The cost side gets the same discipline, and this matters more than it sounds. The audited '
  'cost-of-sales note splits production cost into physically distinct lines, and each one is '
  'escalated on its OWN driver rather than on a single blended inflation index:')
rows = [['Cost line', 'Share of production cost', 'Escalated on']]
cs = V['cost_shares']
for nm, k, esc in (
        ('Imported active ingredients', 'materials',
         'a hard-currency price path passed through the exchange-rate path'),
        ('Packaging materials', 'packaging',
         f"{pc(V['esc_packaging_import_share'], 0)} on the hard-currency path, the balance "
         f"domestic — the group makes its own primary packaging"),
        ('Labour', 'labour', 'Egyptian wage growth, which is running above consumer prices'),
        ('Energy and utilities', 'energy',
         'the regulated tariff schedule, ABOVE consumer prices while subsidy reform runs'),
        ('Other consumables and services', 'services_other', 'domestic consumer prices'),
        ('Depreciation', 'depreciation',
         'nothing — it is excluded here and comes from the property roll-forward instead')):
    rows.append([nm, pc(cs[k], 1), esc])
table(rows, [1.85, 1.15, 3.7], size=8.8)
caption('Table 8 — one escalator per driver class. A single blended index across these lines '
        'would make the forecast margin an artefact of the index rather than of the business.')

H2('1.7 The crux')
P(f'The crux is the new plant, and it is worth being precise about what this study does and '
  f'does not assume. It CHARGES the plant: EGP {n0(V["cip_fy25"])} million of construction '
  f'balance transfers into depreciable assets on the company\'s own disclosed licensing '
  f'timetable, taking the depreciation charge from EGP {n0(V["dna_fy25"])} million in FY2025 '
  f'to EGP {n0(FC["dna"][0])} million in FY2026 and EGP {n0(FC["dna"][2])} million by FY2028. '
  f'The interest that had been capitalised into the construction balance — EGP '
  f'{n0(V["capint_cum_fy25"] - V["capint_cum_fy24"])} million in FY2025 alone — stops being '
  f'capitalised and starts being expensed. It does NOT credit the plant with any revenue, '
  f'because the company has published none.')
figure(os.path.join(HERE, 'fig3_depreciation.png'), 6.7,
       'Figure 4 — the depreciation step, and the construction balance that causes it.')
P(f'So the honest question is not what the plant is worth. It is how much it must sell. '
  f'Solving the same model for the market price: an additional EGP '
  f'{n0(CRUX["required_fy30_revenue"])} million of revenue by FY2030 at a 45% contribution '
  f'margin closes the gap from EGP {n2(A["per_share"])} to EGP {n2(SPOT)}. That is '
  f'{pc(CRUX["required_share_of_fy30"], 0)} of FY2030 revenue, or about USD '
  f'{n0(CRUX["required_rev_usd_mn"])} million a year — {n2(CRUX["asset_turn"])} times the USD '
  f'100 million the company says it invested in the plant.')
box([('Why this number is useful. ',
      f'It is observable. Roughly USD {n0(CRUX["required_rev_usd_mn"])} million a year of '
      f'biosimilar revenue by 2030 is a figure the company will eventually disclose, and a '
      f'reader can check this study against it. An asset turn of {n2(CRUX["asset_turn"])} '
      f'times on a specialist biologics facility is demanding but not absurd; whether it is '
      f'achievable in Egypt, at Egyptian reimbursement prices, on a product set still moving '
      f'through registration, is the question the market is answering yes to and this study '
      f'is declining to answer either way.')])
figure(os.path.join(HERE, 'fig7_crux.png'), 6.6,
       'Figure 5 — the crux stated as a reverse valuation.')
P('The first quarter of 2026 is the first real test of all this, and it is worth setting the '
  'forecast against it line by line rather than claiming a hit.')
rows = [['Line', 'Q1-2026 actual', 'Read into a full year', "This study's FY2026",
         'How the forecast stands against it']]
q1r = V['q1_rev'] / V['q1_share_of_year_rev']
rows += [
    ['Net sales (EGP m)', n0(V['q1_rev']), n0(q1r), n0(FC['revenue'][0]),
     f"{pc(FC['revenue'][0] / q1r - 1, 1)} against the quarter's run-rate"],
    ['Gross margin', pc(V['q1_gp'] / V['q1_rev']), '—', pc(FC['gross_margin'][0]),
     f"within {abs(FC['gross_margin'][0] - V['q1_gp'] / V['q1_rev']) * 1e4:,.0f} basis points"],
    ['Depreciation and amortisation (EGP m)', n1(V['q1_dna']), n0(V['q1_dna'] * 4),
     n0(FC['dna'][0]), 'the step is real; the study is ahead on timing only'],
    ['Transfers out of construction (EGP m)', n0(V['cip_fy25'] - V['q1_cip']),
     n0((V['cip_fy25'] - V['q1_cip']) * 4), n0(V['cip_transfer'][0]),
     'confirmed, and the study is if anything conservative'],
    ['Finance cost (EGP m)', n0(V['q1_fin']), n0(V['q1_fin'] * 4), n0(V['int_path'][0]),
     'reset to the quarter'],
    ['Provision charge as a share of sales', pc(V['q1_prov'] / V['q1_rev'], 2), '—',
     f"{pc(V['prov_pct_permanent'], 2)} / {pc(V['prov_pct_normalising'][0], 2)}",
     'no credit-loss charge was taken at all — see below'],
    ['Associates (EGP m)', n1(V['q1_assoc']), n0(V['q1_assoc'] * 4), n0(V['assoc_norm']),
     'the quarter is incomplete by the auditor\'s own statement'],
    ['Capital expenditure (EGP m)', n0(V['q1_capex']), n0(V['q1_capex'] * 4),
     n0(FC['capex'][0]), 'reset upward to the quarter'],
]
table(rows, [1.75, 0.95, 1.05, 1.0, 2.3], size=8.2)
caption('Table 11 — the forecast against the first quarter it can be checked on. The middle '
        'column reads the quarter into a year on the FY2025 seasonal shape, in which the first '
        'quarter carried 24.4% of sales and 22.1% of attributable profit.')
P(f'Two of those rows carry more weight than the rest. The depreciation line is the study\'s '
  f'central claim and it is confirmed: the charge is running at roughly double last year on a '
  f'plant that has only just entered service, and the model\'s own depreciation rate '
  f'reproduces the quarter to within 3%. The provision line is the study\'s contested '
  f'judgement, and here the quarter does NOT settle it: the company took EGP {n0(V["q1_prov"])} '
  f'million of provisions and inventory write-downs but no credit-loss charge whatsoever, '
  f'against receivables that grew EGP {n0(V["q1_ar"] - V["ar_fy25"])} million in the same three '
  f'months. The auditor qualified the review on precisely that point. A charge that is omitted '
  f'in the first quarter is deferred, not avoided, which is why both frames still run.')

H2('1.8 Macro and country — the cost of capital')
P(f'The quoted ten-year Egyptian local-currency government yield is {pc(V["rf"], 2)}. That '
  f'yield is not riskless: it contains the sovereign\'s own default risk. Subtracting Egypt\'s '
  f'sovereign credit-default-swap spread of {pc(V["sov_spread_cds"], 2)} leaves a normalised '
  f'risk-free rate of {pc(W["rf_star"], 2)}. Adding beta times the country equity risk premium '
  f'gives the cost of equity. Charging the raw {pc(V["rf"], 2)} yield AND a country-loaded '
  f'premium would give {pc(W["ke_double_counted_retired"], 2)} and would count sovereign risk '
  f'twice; that construction is not used here.')
rows = [['Cost of capital', 'Swap basis', 'Rating basis', 'Source and construction']]
rows += [
    ['Ten-year local-currency yield', pc(V['rf'], 2), pc(V['rf'], 2),
     'House reference print of 21 July 2026'],
    ['Less sovereign default spread', pc(V['sov_spread_cds'], 2), pc(V['sov_spread_rating'], 2),
     'Country risk-premium file, Egypt row, read 9 August 2026'],
    ['Normalised risk-free rate', pc(W['rf_star'], 2),
     pc(V['rf'] - V['sov_spread_rating'], 2), 'The subtraction above'],
    ['Country equity risk premium', pc(V['erp_cds'], 2), pc(V['erp_rating'], 2),
     'Same file, same row, the two published columns'],
    ['Beta', f"{V['beta']:.3f}", f"{V['beta']:.3f}",
     'Own-stock weekly regression against a 36-name local composite, five years; '
     'R-squared 0.235, n = 257, standard error 0.071'],
    ['COST OF EQUITY', pc(W['ke'], 2), pc(W['ke_rating'], 2),
     'The two bases agree to 11 basis points'],
    ['Cost of debt, local currency', pc(V['kd_egp'], 2), pc(V['kd_egp'], 2),
     'Sovereign yield plus 250 basis points — above the sovereign by construction'],
    ['Cost of debt, hard currency', pc(V['kd_fx_coupon'], 2), pc(V['kd_fx_coupon'], 2),
     'Dollar and euro term loans from two Gulf banks'],
    ['   carried at local-equivalent cost', pc(W['kd_fx_local_equiv'], 2),
     pc(W['kd_fx_local_equiv'], 2),
     f"coupon compounded with {pc(V['fx_dep_wacc'], 1)} expected currency depreciation"],
    ['Blended cost of debt, after tax', pc(W['kd_at'], 2), pc(W['kd_at'], 2),
     f"book split {pc(1 - W['w_fx'], 0)} local / {pc(W['w_fx'], 0)} hard currency, "
     'borrowings note (17)'],
    ['Weights (net debt basis)', f"{pc(W['we_net'], 0)} / {pc(W['wd_net'], 0)}",
     f"{pc(W['we_net'], 0)} / {pc(W['wd_net'], 0)}",
     'Market-value equity, never book equity'],
    ['DISCOUNT RATE, FIRST YEAR', pc(W['wacc0'], 2), '', 'On gross debt: '
     + pc(W['wacc0_gross'], 2) + ' — both published'],
    ['DISCOUNT RATE, TERMINAL', pc(W['wacc_term'], 2), '',
     f"cost of equity {pc(W['ke_term'], 2)}, cost of debt after tax "
     f"{pc(W['kd_term_at'], 2)}, debt weight {pc(V['wd_term'], 0)}"]]
table(rows, [1.95, 0.95, 0.95, 3.15], band_rows={6, 12, 13}, size=8.4)
caption('Table 9 — the cost of capital, built rather than asserted, and published on both '
        'bases the source provides.')
P(f'A cost-of-debt cross-check that a reader can run: the company expensed EGP '
  f'{n0(V["int_fac_fy25"])} million of interest in FY2025 and capitalised a further EGP '
  f'{n0(V["capint_cum_fy25"] - V["capint_cum_fy24"])} million into the construction balance. '
  f'On average gross debt of EGP {n0(W["avg_gross_debt"])} million that is '
  f'{pc(W["kd_eff_expensed"])} '
  f'expensed and {pc(W["kd_eff_allin"])} all-in. The {pc(W["kd_blend"])} marginal rate used '
  f'here sits inside that pair, which is the test that matters: a marginal rate below what '
  f'the company actually pays, or above what it actually incurs, would not be credible.')
P(f'One arithmetic point that looks wrong and is not. The first-year discount rate of '
  f'{pc(W["wacc0"], 2)} sits close to the {pc(V["rf"], 2)} quoted government yield. That is a '
  f'consequence of the normalisation, not an error: the quoted yield contains default risk '
  f'that this build strips out and re-charges inside the equity premium, where it belongs. '
  f'Comparing a cost of capital built on a normalised risk-free rate to a raw quoted yield is '
  f'comparing two different things.')

H2('1.9 Sensitivity')
figure(os.path.join(HERE, 'fig6_tornado.png'), 6.7,
       'Figure 6 — what actually moves the answer. Each bar is the full range of the value per '
       'share across a plausible range of that one input.')
rows = [['Terminal growth →', *[pc(g, 0) for g in SENS['grid_g']]]]
for i, w_ in enumerate(SENS['grid_wacc']):
    rows.append([f'Cost of equity {w_ * 10000:+.0f} basis points'] +
                [n0(SENS['grid'][i][j]) for j in range(5)])
table(rows, [2.15, 0.95, 0.95, 0.95, 0.95, 0.95], size=8.8)
caption('Table 10 — the value per share across the cost of equity and terminal growth '
        'together. Every cell is a complete revaluation.')
P(f'The crux is sensitised in real observable units rather than in percentage points: an '
  f'extra EGP {n0(CRUX["required_fy30_revenue"] / 4)} million of FY2030 revenue from the new '
  f'plant is worth roughly EGP {n0((SPOT - A["per_share"]) / 4)} a share, so each USD 20 '
  f'million a year of biosimilar sales is worth about EGP 11 a share.')

# ==================== 6. SECTION 2 — TECHNICAL & PRICE STRUCTURE ===============
H1('2. Technical and price structure')
P(TECH['tech']['summary'])
rows = [['Level', 'EGP', 'Distance from the close'],
        ['Third resistance', n2(TECH['levels']['res'][2]), pc(TECH['levels']['res'][2] / SPOT - 1, 1)],
        ['Second resistance', n2(TECH['levels']['res'][1]), pc(TECH['levels']['res'][1] / SPOT - 1, 1)],
        ['Nearest resistance', n2(TECH['levels']['res'][0]), pc(TECH['levels']['res'][0] / SPOT - 1, 1)],
        ['Last close', n2(SPOT), '—'],
        ['Nearest support', n2(TECH['levels']['sup'][0]), pc(TECH['levels']['sup'][0] / SPOT - 1, 1)],
        ['Second support', n2(TECH['levels']['sup'][1]), pc(TECH['levels']['sup'][1] / SPOT - 1, 1)],
        ['Third support', n2(TECH['levels']['sup'][2]), pc(TECH['levels']['sup'][2] / SPOT - 1, 1)]]
table(rows, [2.55, 1.0, 1.85], band_rows={4}, size=9.0)
caption('Table 11 — support and resistance, computed from recency-weighted pivot clusters on '
        'the same cleaned price history the probability map uses.')
P(f'The structural point matters more than the levels. The nearest support sits '
  f'{pc(TECH["levels"]["sup"][0] / SPOT - 1, 0)} below the last close. The move that took this share '
  f'from about EGP 90 in late July to EGP 150 on 3 August happened in four sessions, two of '
  f'them at the exchange\'s daily limit, and it left no traded structure behind it. A price '
  f'that gaps up through empty space has nothing under it if sentiment turns — which is why '
  f'the three-month probability band below is as wide as it is.')
P(TECH['tech']['bull'] + ' ' + TECH['tech']['bear'])

# ==================== 7. SECTION 3 — PROBABILISTIC PRICE MAP ===================
H1('3. Probabilistic price map')
P(f'The valuation above says where the shares should be. This section says something '
  f'different and narrower: given how this share has actually behaved, where might the price '
  f'be in one and three months? It is a statement about the distribution of outcomes, not a '
  f'forecast of one.')
rows = [['Percentile of the simulated distribution', 'One month', 'Three months']]
for p in (5, 25, 50, 75, 95):
    rows.append([f'{p}th percentile', n2(STRIKE['horizons']['1M']['pct'][f'p{p}']),
                 n2(STRIKE['horizons']['3M']['pct'][f'p{p}'])])
rows.append(['Check date', STRIKE['horizons']['1M']['grade_date'],
             STRIKE['horizons']['3M']['grade_date']])
table(rows, [3.2, 1.2, 1.2], band_rows={6}, size=9.0)
caption('Table 12 — the percentile map. The anchor is the EGP '
        f'{n2(STRIKE["spot"])} close of {STRIKE["anchor_date"]}.')
rows = [['Probability', 'One month', 'Three months']]
for label, key in (('Finishes above the anchor', 'p_above'),
                   ('Finishes 10% or more above', 'p_up10'),
                   ('Finishes 10% or more below', 'p_dn10'),
                   ('TOUCHES 10% above at any point', 'touch_up10'),
                   ('TOUCHES 10% below at any point', 'touch_dn10')):
    rows.append([label, pc(STRIKE['horizons']['1M'][key], 0),
                 pc(STRIKE['horizons']['3M'][key], 0)])
table(rows, [3.2, 1.2, 1.2], size=9.0)
caption('Table 13 — the level-touch ladder. Touching a level at any point during the window '
        'is far more likely than finishing beyond it.')
figure(os.path.join(HERE, 'fig5_cone.png'), 6.9,
       'Figure 7 — the price history and the one- and three-month bands.')
P(f'How much should a reader trust this? The method was tested by re-running it every quarter '
  f'across the whole cleaned price history, without ever letting it see the future, and '
  f'scoring each forecast against what actually happened. Over the last five years of those '
  f'tests — 19 non-overlapping three-month windows — it scored marginally better than a '
  f'random walk anchored on the same carry, by {BT["five_year"]["skill_norm"]:+.4f} on a '
  f'scale where zero means no better and one means perfect. Over the full '
  f'{BT["full"]["span_years"]:.1f}-year history and {BT["full"]["windows"]} windows it scored '
  f'{BT["full"]["skill_norm"]:+.4f}. In plain terms: on this single share the method is '
  f'indistinguishable from a random walk, and this study says so rather than claiming an edge '
  f'it cannot demonstrate.')
P(f'What the tests DO show is that the bands are honestly sized, which is the property that '
  f'matters for reading them. Across the five-year window set the outcome fell inside the 90% '
  f'band {pc(BT["five_year"]["cov90"], 0)} of the time and inside the 50% band '
  f'{pc(BT["five_year"]["cov50"], 0)} of the time, and the distribution of where outcomes '
  f'landed within the bands was statistically indistinguishable from uniform (chi-square '
  f'p = {BT["five_year"]["chi2_p"]}, Kolmogorov-Smirnov p = {BT["five_year"]["ks_p"]}). The '
  f'bands are also about {BT["five_year"]["width_vs_benchmark"]:.2f} times as wide as the '
  f'benchmark\'s, which means they are conservative rather than flattering. Read them as an '
  f'honest width, not as a claim to foresight.')

# =================== 8. SECTION 4 — COMPARISON OF THE LENSES ===================
H1('4. Comparison of the lenses')
rows = [['Lens', 'EGP / share', 'What it is most sensitive to', 'When it misleads']]
rows += [
    ['Discounted cash flow, Frame A', n2(A['per_share']),
     'the terminal discount rate and the terminal growth rate — '
     f"{pc(A['tv_share'], 0)} of the value is in the terminal block",
     'when five explicit years are not long enough to reach a steady state, which for a plant '
     'entering service is exactly the risk'],
    ['Discounted cash flow, Frame B', n2(Bf['per_share']),
     'the same, plus the speed at which the provision charge normalises',
     'if the credit losses are structural rather than cyclical'],
    ['Book value and sustainable return', n2(LN['book_ps']),
     'the sustainable return on equity and the perpetual cost of equity',
     'when a large part of the asset base is not yet earning — which is true here, with '
     f"EGP {n0(V['cip_fy25'])} million still in construction at the year end"],
    ['Relative multiples', n2(LN['rel_ps']),
     'the cost of equity, through all three of its inputs',
     'when the peer set faces a different country risk, which is why the peer median is '
     'adjusted rather than applied raw'],
    ['Normalised earnings power', n2(LN['norm_ps']),
     'the choice of normal margin',
     'when the business has genuinely re-based upward, in which case a three-year average '
     'understates it']]
table(rows, [1.85, 0.85, 2.05, 2.65], size=8.4)
caption('Table 14 — the four methods against each other, including where each one fails.')
P(f'The lenses disagree in an informative direction. The two cash-flow lenses are the HIGHEST '
  f'in the field even though they charge the new plant\'s full cost, because they capture five '
  f'years of the volume and price growth the existing business is already delivering. The '
  f'relative lens is the LOWEST because it prices the company on what a '
  f'{pc(LN["roe_sust"])} return and a {pc(W["ke_term"], 1)} perpetual cost of equity can '
  f'justify, and that arithmetic supports about {n1(LN["just_fwd_pe"])} times earnings, not '
  f'{n1(LN["pe_now"])}. Neither is wrong. The gap between them is the value of growth, and '
  f'the market is paying for more of it than either lens contains.')

# =============================== 9. SECTION 5 — CATALYSTS ======================
H1('5. Catalysts')
rows = [['What to watch', 'Why it matters', 'When']]
rows += [
    ['First disclosed revenue from the biologicals plant',
     f"the whole crux. Section 1.7 says roughly USD {n0(CRUX['required_rev_usd_mn'])} million a "
     f"year by 2030 is required to justify the market price; the first disclosure calibrates "
     f"how plausible that is", 'FY2026 results, and every quarter after'],
    ['The FY2026 depreciation charge',
     f"this study assumes it steps from EGP {n0(V['dna_fy25'])} million to about EGP "
     f"{n0(FC['dna'][0])} million as the construction balance transfers. A materially smaller "
     f"step means the plant is being commissioned more slowly than assumed",
     'FY2026 results'],
    ['Whether capitalised interest stops',
     f"EGP {n0(V['capint_cum_fy25'] - V['capint_cum_fy24'])} million of interest was "
     f"capitalised in FY2025. Once the plant is in service that becomes an expense, and "
     f"reported profit falls without anything changing in the business",
     'FY2026 interim and full year'],
    ['The credit-loss charge',
     'the study\'s contested judgement. Two years near 5% of revenue with a 9% year between '
     'them; which frame the next two years resemble is worth more than a point of margin',
     'each set of results'],
    ['The Saudi associate',
     f"contributed EGP {n0(ASSOC_SA_FY25)} million in FY2025 against EGP "
     f"{n0(ASSOC_SA_FY24)} million in FY2024. This study normalises it to EGP {n0(V['assoc_norm'])} million; if "
     f"the step-up holds, that is conservative", 'each set of results'],
    ['The active-ingredient project',
     'a separate USD 165 million company that this study does NOT consolidate and does NOT '
     'value. It reaches the accounts only through the associate line',
     'trial batches indicated for 2027'],
    ['The exchange rate',
     'exports are 32% of revenue but imported inputs are 79% of the cash cost stack, so a '
     'weaker pound is a NET NEGATIVE for this company — the opposite of the usual exporter '
     'reflex', 'continuous']]
table(rows, [1.75, 3.55, 1.6], size=8.4)
caption('Table 15 — the events that would move this valuation, and the direction each cuts.')

# =============== 10. SECTION 6 — READING THE PROBABILITY ZONES =================
H1('6. Reading the probability zones')
P('The bands in section 3 are frequently misread, so here is how to use them.')
bullet('is the probability that the price ENDS the window beyond a level. It is what a '
       'position held to the check date experiences.', bold_head='The percentile map ')
bullet('is the probability that the price TOUCHES a level at any point inside the window, '
       'even if it comes back. It is always the larger of the two, and it is what a stop-loss '
       'experiences. On the three-month window the difference is substantial: '
       f'{pc(STRIKE["horizons"]["3M"]["p_dn10"], 0)} of paths finish 10% or more below the '
       f'anchor, but {pc(STRIKE["horizons"]["3M"]["touch_dn10"], 0)} touch that level at some '
       f'point.', bold_head='The touch ladder ')
bullet('the 90% band is not a maximum. One outcome in ten is designed to fall outside it, and '
       'over a long enough run one will.', bold_head='A band is not a limit: ')
bullet(f'the bands here are wide — the three-month 90% band runs from EGP '
       f'{n2(STRIKE["horizons"]["3M"]["pct"]["p5"])} to EGP '
       f'{n2(STRIKE["horizons"]["3M"]["pct"]["p95"])} — because this share has been genuinely '
       f'volatile: the annualised volatility implied by its recent trading is about '
       f'{pc(STRIKE["horizons"]["3M"]["anchor_vol_ann"], 0)}. A narrow band on a share that '
       f'moved 44% in two sessions would be a lie.', bold_head='Width is information: ')
bullet('the bands describe where the PRICE may go. The valuation describes what the BUSINESS '
       'appears to be worth. They are different questions and this study keeps them apart on '
       'purpose. The weighted central fair value sits below the entire three-month band, and '
       'that is worth noticing rather than reconciling away.',
       bold_head='These are not a valuation: ')

# ============ 11. SECTION 7 — CAVEATS AND WHAT WOULD CHANGE OUR MIND ===========
H1('7. Caveats, and what would change our mind')
H2('7.1 What changed in this edition, and by how much')
rows = [['Change', 'Effect']]
rows += [
    ['FY2026 revenue growth reset from 17.5% to the quarter\'s 10.1%',
     'the largest single change; it lowers the base every later year compounds from'],
    ['FY2026 capital expenditure raised to the quarter\'s run-rate',
     'more cash out of free cash flow in the first forecast year'],
    ['Finance cost charged to profit reset to the quarter, and separated from the marginal '
     'cost of debt used in the discount rate',
     'raises forecast earnings; the two were being conflated and are now distinct rows'],
    ['Normalised associate contribution cut from EGP 320m to EGP 250m, the like-for-like '
     'three-year average', 'lowers the bridge; the quarter reported only EGP 13.1m, but the '
     'auditor states the associates\' statements were not received, so it is not decisive'],
    ['The active-ingredient company added to the bridge at carrying cost, and the '
     'non-controlling interest deducted there replaced with the post-deconsolidation figure',
     'both POSITIVE, and they are two halves of one event: that company left the consolidation '
     'in the quarter, taking EGP 284.7m of minorities out and adding EGP 228.5m of associate '
     'carrying value'],
    ['Dividend-distribution tax given its own line in all three history years, following the '
     'separately issued statements', 'lifts FY2023 operating profit by EGP 4.1m (0.34%); worth '
     'about EGP 0.12 a share'],
    ['NET EFFECT ON THE WEIGHTED CENTRAL VALUE',
     f"EGP 79.64 to EGP {n2(LN['fair_base'])} a share, {pc(LN['fair_base'] / 79.64 - 1, 0)}"],
]
table(rows, [2.7, 4.2], band_rows={7}, size=8.4)
caption('Table 17 — every change from the first edition, and its direction.')

rows = [['Caveat', 'What it costs the study', 'What would settle it']]
rows += [
    ['The first-quarter review conclusion is QUALIFIED on three matters',
     'no expected-credit-loss charge was recognised in the quarter; the associates\' own '
     'statements were not received; and the active-ingredient company was recognised at cost '
     'after loss of control rather than remeasured and equity-accounted. The first flatters '
     'the quarter\'s profit, the second makes the associate line incomplete, the third is a '
     'measurement question this study side-steps by carrying that company at cost',
     'an unqualified half-year review'],
    ['No revenue is modelled for the biologicals plant',
     'the cash-flow lenses are understated by whatever the plant earns. This is the largest '
     'single limitation and it is deliberate',
     'the company disclosing biosimilar revenue, volumes or utilisation'],
    ['The valuation bridge is anchored on the audited 31 December 2025 balance sheet, not on '
     'the March one',
     'net debt was EGP 9,065m at 31 March against EGP 7,364m at 31 December, but the quarter '
     'also paid the FY2025 dividend and built working capital, and the forecast still carries '
     'a full FY2026 of cash flow. Using the March balance sheet AND a full forecast year would '
     'charge the same quarter twice. On the March net debt alone the value would be about EGP '
     '10 a share lower',
     'a half-year balance sheet, at which point the anchor can move forward cleanly'],
    ['The ten-year government yield is a cached print, not a live read',
     'the discount rate carries the 21 July 2026 figure. The central bank\'s auction page '
     'refused the request. The rate is sensitised over a wide range in section 1.9',
     'a live read; a 200 basis-point error is worth about EGP 7 a share'],
    ['The associate contribution is normalised, not built up',
     'the associates published no accounts through this company\'s filings, so a EGP '
     f'{n0(V["assoc_norm"])} million normalisation stands in for a real forecast. It is worth '
     f'EGP {n2(V["assoc_norm"] * V["assoc_multiple"] / SH)} a share',
     'the Saudi associate publishing separate accounts'],
    ['Peer multiples are market data, not primary company data',
     'the relative lens\'s third leg rests on observed peer trading rather than on peer '
     'filings. It is one of three legs and is labelled as a cross-check throughout',
     'building each peer from its own audited statements'],
    ['One disclosed operating figure was restated between annual reports',
     f'the FY2024 tablet production line reads {n0(V["tablets_fy24_as_reported"])} million '
     f'units in the FY2024 report and {n0(V["tablets_fy24_restated"])} million in the FY2025 '
     f'report. The later filing is used. It affects a utilisation statistic, not a valuation '
     f'input',
     'a company explanation of the restatement'],
    ['The pre-2020 portion of the price history is thin',
     'the price export carries 162–195 sessions a year before 2020 against roughly 245 real '
     'exchange sessions. It affects only the longest calibration window, not the live bands, '
     'which are built on the post-2022 period',
     'a complete exchange-sourced price history']]
table(rows, [1.9, 3.35, 1.65], size=8.3)
caption('Table 16 — every limitation this study knows about, and what would resolve it.')
P(f'One caveat from the first edition is now closed: the FY2026 first-quarter interim, which '
  f'could not be reached at any official source online, was supplied directly and is in this '
  f'edition. The secondary reporting recorded then as an unverified cross-check turned out to '
  f'be accurate to the pound on both sales and attributable profit.')
P('What would change the conclusion, stated in advance so it can be checked: if the company '
  f'disclosed biosimilar revenue on a path toward USD {n0(CRUX["required_rev_usd_mn"])} '
  f'million a year, the cash-flow lenses would move to the market price and this study would '
  f'be wrong to have flagged the gap. If the FY2026 depreciation charge came in near EGP '
  f'{n0(V["dna_fy25"])} million rather than EGP {n0(FC["dna"][0])} million, the plant is not '
  f'in service and the whole timetable in this study shifts out a year.')

# ======================== 12. APPENDIX A — THE STATEMENTS ======================
H1('Appendix A — the financial statements')
H2('A.1 Income statement: three audited years and five forecast years')
rows = [['EGP million', 'FY2023', 'FY2024', 'FY2025'] + [y.replace('FY', '').replace('E', 'E')
                                                         for y in YR]]
def isrow(label, hk, fk, neg=False, fmt=n0):
    vals = [fmt(H[y][hk]) for y in ('FY2023', 'FY2024', 'FY2025')]
    vals += [fmt(x) for x in fk]
    rows.append([label] + vals)


isrow('Revenue', 'revenue', FC['revenue'])
isrow('Cost of sales', 'cogs', FC['cogs'])
isrow('Gross profit', 'gross_profit', FC['gross_profit'])
rows.append(['Gross margin'] + [pc(H[y]['gross_margin']) for y in
                                ('FY2023', 'FY2024', 'FY2025')] +
            [pc(x) for x in FC['gross_margin']])
isrow('Selling and marketing', 'marketing', FC['marketing'])
isrow('Research and development', 'rnd', FC['rnd'], fmt=n1)
isrow('General and administrative', 'ga', FC['ga'], fmt=n1)
isrow('Credit losses and provisions', 'provisions', FC['prov_A'])
isrow('Operating profit', 'ebit', FC['ebit_A'])
isrow('EBITDA', 'ebitda', [FC['ebit_A'][i] + FC['dna'][i] for i in range(5)])
isrow('Depreciation and amortisation', 'dna', FC['dna'], fmt=n1)
isrow('Finance costs', 'finance',
      [V['kd_path'][i] * W['gross_debt'] - 0.08 * V['cash_fy25'] for i in range(5)])
isrow('Share of associates', 'associates', [V['assoc_norm']] * 5)
rows.append(['Profit attributable to shareholders'] +
            [n0(H[y]['parent']) for y in ('FY2023', 'FY2024', 'FY2025')] +
            [n0(FC['equity'][i] - (FC['equity'][i - 1] if i else V['equity_parent_fy25']))
             for i in range(5)])
table(rows, [1.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72], band_rows={3, 9, 14},
      size=7.9)
caption('Table 17 — three audited years and five forecast years. The attributable-profit line '
        'in the forecast columns is the retained portion grossed back up at the payout ratio.')

H2('A.2 Balance sheet')
rows = [['EGP million', 'FY2023', 'FY2024', 'FY2025'] + YR]
bs = [('Property, plant and equipment', V['ppe_fy23'], V['ppe_fy24'], V['ppe_fy25'],
       FC['ppe']),
      ('Projects under construction', V['cip_fy23'], V['cip_fy24'], V['cip_fy25'], FC['cip']),
      ('Inventories', V['inv_fy23'], V['inv_fy24'], V['inv_fy25'], FC['inventory']),
      ('Trade receivables', V['ar_fy23'], V['ar_fy24'], V['ar_fy25'], FC['receivables']),
      ('Cash and bank balances', V['cash_fy23'], V['cash_fy24'], V['cash_fy25'],
       [V['cash_fy25']] * 5),
      ('Trade payables', V['ap_fy23'], V['ap_fy24'], V['ap_fy25'], FC['payables']),
      ('Gross borrowings', V['debt_fy23'], V['debt_fy24'], W['gross_debt'],
       [W['gross_debt']] * 5),
      ('Equity attributable to shareholders', V['equity_parent_fy23'],
       V['equity_parent_fy24'], V['equity_parent_fy25'], FC['equity'])]
for nm, a3, a4, a5, fwd in bs:
    rows.append([nm, n0(a3), n0(a4), n0(a5)] + [n0(x) for x in fwd])
rows.append(['Book value per share (EGP)',
             n2(V['equity_parent_fy23'] / V['shares_fy23']),
             n2(V['equity_parent_fy24'] / V['shares_fy23']),
             n2(LN['bv_ps'])] + [n2(x / SH) for x in FC['equity']])
table(rows, [1.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72], band_rows={9},
      size=7.9)
caption('Table 18 — the balance sheet. The property and construction lines roll forward on the '
        'transfer schedule; working capital is projected from the disclosed day ratios.')

H2('A.3 Cash flow and the working-capital markers')
rows = [['Marker', 'FY2025 audited'] + YR]
rows.append(['Inventory days', f"{WC['dio_fy25']:.0f}"] + [f'{d:.0f}' for d in V['dio']])
rows.append(['Receivable days', f"{WC['dso_fy25']:.0f}"] + [f'{d:.0f}' for d in V['dso']])
rows.append(['Payable days', f"{WC['dpo_fy25']:.0f}"] + [f'{d:.0f}' for d in V['dpo']])
rows.append(['Cash conversion cycle', f"{WC['ccc_fy25']:.0f}"] +
            [f'{V["dio"][i] + V["dso"][i] - V["dpo"][i]:.0f}' for i in range(5)])
rows.append(['Capital expenditure (EGP m)', n0(V['capex_fy25'])] +
            [n0(x) for x in FC['capex']])
rows.append(['Free cash flow to the firm (EGP m)', '—'] + [n0(x) for x in A['fcff']])
table(rows, [1.9, 1.15, 0.85, 0.85, 0.85, 0.85, 0.85], size=8.4)
caption('Table 19 — the asset-conversion cycle, projected rather than plugged. The 268-day '
        'inventory position is a stated policy: the company holds a strategic raw-material '
        'stockpile it says covers at least eight months.')

# ============ 13. APPENDIX B — PEERS, RISK REGISTER, RESEARCH RECORD ===========
H1('Appendix B — peers, risks and the research record')
H2('B.1 Peers')
rows = [['Company or reference', 'Multiple', 'Basis', 'Status in this study']]
rows += [
    ['Listed Saudi Arabian generics manufacturer', f'{PEER_HI}x',
     'trailing price / earnings',
     'market data, cross-check only'],
    ['Regional and international mid-cap generic manufacturers', f'~{PEER_MID:.0f}x',
     'trailing price / earnings', 'market data, cross-check only'],
    ['Peer median used', f"{V['peer_pe_regional']:.1f}x", 'trailing price / earnings',
     'the third leg of the relative lens, adjusted for the cost-of-equity gap'],
    ['EIPICO today', f"{LN['pe_now']:.1f}x", 'trailing price / earnings',
     'computed from audited attributable profit and the market price'],
    ['EIPICO, own four-year mean', f"{LN['own_pe_mean']:.1f}x", 'trailing price / earnings',
     'computed entirely from primary material — the first leg of the relative lens']]
table(rows, [2.4, 0.8, 1.55, 2.15], size=8.4)
caption('Table 20 — the peer set. No peer figure is used to build any historical number for '
        'EIPICO; peers appear only as a cross-check.')
H2('B.2 Risks')
rows = [['Risk', 'How it would show up', 'Severity']]
rows += [
    ['The new plant under-delivers', 'depreciation and interest charged with no revenue '
     'against them; reported profit falls for two to three years', 'High'],
    ['Administered price freeze', 'the domestic price-per-pack driver stops tracking '
     'inflation while imported input costs keep rising', 'High'],
    ['Currency depreciation', 'imported ingredients and packaging are 79% of the cash cost '
     'stack against a 32% export share — a weaker pound is net negative here', 'High'],
    ['Credit losses prove structural', 'the provision charge stays near 5% of revenue '
     'permanently; this is Frame A, and it is already the more conservative published case',
     'Medium'],
    ['Concentration in the domestic distributor channel', '39% of revenue passes through '
     'distributors, and the company itself says it deals with a small number of them',
     'Medium'],
    ['Refinancing', f"EGP {n0(W['gross_debt'])} million of gross borrowings against EGP "
     f"{n0(V['cash_fy25'])} million of cash, half of it hard-currency", 'Medium'],
    ['Controlling shareholder', 'a 51.34% holder whose interests may not align with the '
     'minority on capital allocation', 'Low to medium']]
table(rows, [1.85, 3.55, 0.95], size=8.4)
H2('B.3 The research record')
P('Every figure in this study traces to a numbered source in the accompanying bibliography, '
  'which lists the primary documents actually read, every input with its value, date and '
  'construction, the judgements made with what would overturn each one, the searches that '
  'found nothing, and the places where a secondary source disagrees with the audited filing. '
  'Four consecutive audited financial years were obtained from the company\'s own '
  'investor-relations page: FY2022, FY2023, FY2024 and FY2025, each with the auditor\'s '
  'report and full notes, and each carrying both separate and consolidated statements.')

# ==================== 14. APPENDIX C — THE EXPERT PANEL ========================
H1('Appendix C — three experts, three methods')
P('Three analysts with genuinely different methods were asked the same question. They are '
  'labelled Expert 1, 2 and 3. Each shows their working, names the one sensitivity that '
  'matters most to their answer, and states in advance what would prove them wrong.')

H2('C.1 Expert 1 — the cash-flow analyst')
P('Worldview: a company is worth the cash it will generate for whoever owns the capital, '
  'discounted at what that capital costs. Everything else is a shortcut to that number.')
P('When it works: for a business with a stable, forecastable operating model and a capital '
  'structure that is not about to change. When it fails: when most of the value sits beyond '
  'the explicit forecast — which is the case here, at '
  f'{pc(A["tv_share"], 0)} of enterprise value in the terminal block.')
rows = [['Working', 'EGP million'],
        ['Present value of five years of free cash flow', n0(A['pv_sum'])],
        ['Terminal free cash flow', n0(A['fcff_term'])],
        ['Terminal discount rate less growth',
         f"{pc(W['wacc_term'], 2)} − {pc(V['g_term'], 0)} = {pc(W['wacc_term'] - V['g_term'], 2)}"],
        ['Terminal value', n0(A['tv'])],
        ['Present value of the terminal value', n0(A['pv_tv'])],
        ['Core enterprise value', n0(A['ev_core'])],
        ['Associates and assets held for sale', n0(A['assoc_value'] + V['afs_fy25'])],
        ['Less net debt and minorities', f"({n0(A['net_debt'] + A['nci'])})"],
        ['Equity value', n0(A['equity'])],
        ['Value per share (EGP)', n2(A['per_share'])]]
table(rows, [4.6, 1.7], band_rows={7, 11}, size=8.8)
P(f'Named sensitivity: the terminal discount rate. Every 100 basis points on it is worth '
  f'roughly EGP {n0(abs(SENS["wacc"][2][1] - SENS["wacc"][3][1]))} a share. At '
  f'{pc(A["tv_share"], 0)} terminal weight, this expert is mostly forecasting one number.')
P(f'Falsifier, stated in advance: "If free cash flow to the firm in FY2027 comes in below EGP '
  f'{n0(A["fcff"][1] * 0.7)} million — 30% below my forecast — my five-year build is wrong '
  f'and so is the terminal that grows out of it."')

H2('C.2 Expert 2 — the asset-and-return analyst')
P('Worldview: forecasts are opinions; the balance sheet is a fact. Start from what the '
  'company owns, ask what return it earns on it, and pay a multiple of book that the return '
  'justifies. Never pay for growth you have not seen.')
P('When it works: for asset-heavy businesses and in markets where forecasting is genuinely '
  'hard. When it fails: when a large part of the asset base is not yet earning, which '
  'understates the return and therefore the multiple.')
rows = [['Working', 'Value'],
        ['Equity attributable to shareholders', f"EGP {n0(V['equity_parent_fy25'])}m"],
        ['Shares in issue', f'{SH:,.3f}m'],
        ['Book value per share', f"EGP {n2(LN['bv_ps'])}"],
        ['Return on average equity, FY2025', pc(LN['roe_fy25'])],
        ['Sustainable return on equity', pc(LN['roe_sust'])],
        ['Perpetual cost of equity', pc(W['ke_term'], 2)],
        ['Growth', pc(V['g_term'], 0)],
        ['Justified multiple of book = (return − growth) / (cost of equity − growth)',
         f"{n2(LN['just_pb'])}x"],
        ['Value per share (EGP)', n2(LN['book_ps'])]]
table(rows, [4.6, 1.7], band_rows={9, 10}, size=8.8)
P(f'Named sensitivity: the sustainable return. If it settles at 20% rather than '
  f'{pc(LN["roe_sust"])}, the justified multiple falls to '
  f'{n2((0.20 - V["g_term"]) / (W["ke_term"] - V["g_term"]))} times and the value to EGP '
  f'{n2((0.20 - V["g_term"]) / (W["ke_term"] - V["g_term"]) * LN["bv_ps"])} a share.')
P(f'Falsifier: "If return on average equity falls below 18% in either FY2026 or FY2027, the '
  f'{pc(LN["roe_sust"])} I am capitalising is a peak, not a level, and my multiple is too '
  f'high."')
P(f'This expert adds one point the others miss: EGP {n0(V["cip_fy25"])} million of the asset '
  f'base earned nothing in FY2025. Measured against capital that is actually working, the '
  f'return is far higher than {pc(LN["roe_sust"])} — which is an argument for paying up, and '
  f'this expert declines to make it, because the plant has not yet demonstrated a return.')

H2('C.3 Expert 3 — the market-implied analyst')
P('Worldview: do not ask what a company is worth. Ask what the market price already assumes, '
  'and judge whether those assumptions are reasonable. It is a discipline against arguing '
  'with a price.')
P('When it works: when a price has moved a long way and the question is what it now embeds. '
  'When it fails: it never produces an independent value — it can only tell you what you are '
  'being asked to believe.')
rows = [['What the market price requires', 'Value'],
        ['Market price', f'EGP {n2(SPOT)}'],
        ['Value from the cash-flow model without the new plant',
         f"EGP {n2(A['per_share'])}"],
        ['Gap to be explained', f"EGP {n2(SPOT - A['per_share'])} a share"],
        ['Equity value of that gap',
         f"EGP {n0((SPOT - A['per_share']) * SH)}m"],
        ['Additional FY2030 revenue required at a 45% contribution margin',
         f"EGP {n0(CRUX['required_fy30_revenue'])}m"],
        ['   as a share of FY2030 revenue', pc(CRUX['required_share_of_fy30'], 0)],
        ['   in US dollars a year', f"USD {n0(CRUX['required_rev_usd_mn'])}m"],
        ['   against the plant\'s stated cost of USD 100 million',
         f"{n2(CRUX['asset_turn'])}x asset turn"],
        ['Implied value per share if that is delivered', f'EGP {n2(SPOT)}']]
table(rows, [4.6, 1.7], band_rows={10}, size=8.8)
P(f'Named sensitivity: the contribution margin assumed on the new revenue. At 35% rather than '
  f'45%, the required revenue rises to about EGP '
  f'{n0(CRUX["required_fy30_revenue"] * 45 / 35)} million, or USD '
  f'{n0(CRUX["required_rev_usd_mn"] * 45 / 35)} million a year.')
P('Falsifier: "If the company discloses biosimilar revenue below USD 20 million a year in its '
  'third full year of operation, the price is not discounting a plausible ramp — it is '
  'discounting a hope."')

H2('C.4 Cross-examination')
rows = [['Challenge', 'Conceded or rejected']]
rows += [
    ['Expert 2 to Expert 1: "Three-quarters of your value is a terminal number. You are not '
     'forecasting cash flow, you are forecasting a perpetuity."',
     'CONCEDED. Expert 1 accepts the terminal weight is high and points to the sensitivity '
     'table as the honest response: the range across a plausible terminal rate and growth '
     'combination is EGP 68 to EGP 112, and that range is published rather than hidden.'],
    ['Expert 1 to Expert 2: "You are capitalising a return earned on a capital base that '
     'excludes a third of the assets. Your multiple is measured against the wrong '
     'denominator."',
     'REJECTED, with a qualification. Expert 2 answers that book equity is book equity, and '
     'that a plant which has not yet earned anything belongs in the denominator until it '
     'does — but concedes the lens will understate the company for as long as that remains '
     'true, and says so in the study.'],
    ['Expert 3 to both: "You are both producing numbers below the market price and neither of '
     'you can say why the market is wrong."',
     'CONCEDED, and it is the point. Neither cash-flow nor book-based lens contains the new '
     'plant\'s revenue. Expert 3\'s contribution is to convert that omission into a testable '
     'number rather than an argument.'],
    ['Expert 2 to Expert 3: "Your method assumes the gap is entirely the new plant. It could '
     'be the associates, or a re-rating of Egyptian equities generally."',
     'CONCEDED in part. Expert 3 agrees the attribution is a choice, and notes the associate '
     'stake would have to be worth roughly three times the value assumed here to close the '
     'gap on its own — which is possible, and is a second testable proposition rather than a '
     'refutation.'],
    ['Expert 1 to Expert 3: "A 45% contribution margin on biosimilars is your assumption, not '
     'a disclosure."',
     'CONCEDED. Expert 3 sensitises it explicitly rather than defending it, and the study '
     'publishes both.']]
table(rows, [2.65, 3.7], size=8.3)

H2('C.5 The three in one room')
P('Put together, the disagreement narrows to a single question, which is a good sign. All '
  'three agree on the audited history, on the cost of capital construction, and on the fact '
  'that the depreciation and interest step is real and arrives in FY2026. All three agree the '
  'existing business — 65% capacity utilisation, a growing export book earned in hard '
  'currency, an administered domestic price that at least tracks inflation — is worth '
  'somewhere between EGP 70 and EGP 100 a share.')
P(f'Where they part is what the new plant is worth today. Expert 1 says: nothing until it '
  f'produces cash, so EGP {n2(A["per_share"])}. Expert 2 says: nothing until it produces a '
  f'return, so EGP {n2(LN["book_ps"])}. Expert 3 says: the market says EGP '
  f'{n2(SPOT - A["per_share"])} a share, which requires USD '
  f'{n0(CRUX["required_rev_usd_mn"])} million a year of biosimilar sales, and that is a '
  f'proposition rather than a valuation. The room does not resolve it. It converts it into '
  f'something a reader can check in twelve months.')
figure(os.path.join(HERE, 'fig8_experts.png'), 6.6,
       'Figure 8 — three methods, three ranges, one market price.')

H2('C.6 Divergence table — which assumption drives which gap')
rows = [['Pair', 'Gap (EGP/share)', 'The single assumption that drives it']]
rows += [
    ['Expert 1 less Expert 2', n2(A['per_share'] - LN['book_ps']),
     'whether five years of forecast growth is credited at all. Expert 1 discounts it; Expert '
     '2 refuses to pay for growth not yet earned'],
    ['Expert 3 less Expert 1', n2(SPOT - A['per_share']),
     'entirely the biologicals plant\'s revenue, which Expert 1 sets to zero and Expert 3 '
     'infers from the price'],
    ['Frame A less Frame B', n2(A['per_share'] - Bf['per_share']),
     'the credit-loss and provision charge alone — 5.25% of revenue permanently against a '
     'decay to 2.5%. Nothing else differs between the two'],
    ['Study centre less market price', n2(LN['fair_base'] - SPOT),
     'the sum of the above: no plant revenue, a relative lens anchored on what the company\'s '
     'own return justifies, and a normalised rather than peak margin']]
table(rows, [1.75, 1.05, 3.55], size=8.4)
caption('Table 21 — every gap in this study isolated to the assumption that causes it.')

# ================================== 15. ABOUT ==================================
H1('About this study')
P('This is an independent, educational valuation study. It was prepared from the company\'s '
  'own audited financial statements and its own published operating disclosures, obtained '
  'directly from its investor-relations page. The valuation model behind it is a live '
  'spreadsheet: every figure that can be derived from a driver is a formula, and changing a '
  'driver reprices the model. That claim was tested on the delivered file rather than '
  'asserted — every formula cell was independently recalculated and reconciled to the model, '
  'and each input was perturbed in place to confirm the answer moves in the right direction.')
P('The probability map in section 3 comes from a simulation engine calibrated on the Egyptian '
  'market as a whole and tested by re-running it across the full price history without '
  'letting it see the future. Its performance on this individual share is reported honestly '
  'in section 3, including where it is no better than a random walk.')

# ================================ 16. DISCLOSURE ===============================
H1('Disclosure')
P('This document is educational analysis, not investment advice, and not a recommendation to '
  'buy, sell or hold any security. It contains no rating and no price target. Fair value is '
  'expressed as a range and as a distribution because that is what the evidence supports.',
  size=9.4)
P('The author holds no position in the securities discussed and receives no compensation from '
  'the company, its shareholders or any party with an interest in its share price. The study '
  'was not commissioned by, shown to, or reviewed by the company before publication.', size=9.4)
P('All historical financial figures are the company\'s own audited consolidated figures as '
  'published in its annual reports. Forward-looking figures are the author\'s estimates and '
  'will be wrong in detail; the sensitivity analysis in section 1.9 and the caveats in section '
  '7 state by how much and in which direction. Market data used for peer comparison is '
  'labelled as such and is not used to construct any figure about the subject company.',
  size=9.4)
P('Past performance and back-tested performance are not guides to future results. A '
  'probability band is not a guarantee: one outcome in ten is designed to fall outside a 90% '
  'band.', size=9.4)

OUT = os.path.join(HERE, 'EIPICO_Valuation_Study_09-08-2026.docx')
doc.save(OUT)
print('wrote', os.path.basename(OUT))
