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
CE = D['cost_exposure']
BETAJ = json.load(open(os.path.join(HERE, 'beta_result.json')))
XBJ = json.load(open(os.path.join(HERE, 'beta_ex_subject_price.json')))
V = {k: v['value'] for k, v in D['inputs'].items()}
TECH = json.load(open(os.path.join(HERE, 'technicals.json')))
STRIKE = json.load(open(os.path.join(HERE, 'strike_result.json')))
BT = CAL['backtest']
SPOT, SH = M['spot'], M['shares_mn']
YR = ['FY2026E', 'FY2027E', 'FY2028E', 'FY2029E', 'FY2030E']
A, Bf = DCFD['frame_A'], DCFD['frame_B']
ASSOC_SA_FY25, ASSOC_SA_FY24 = V['assoc_saudi_fy25'], V['assoc_saudi_fy24']
PEER_HI, PEER_MID = V['peer_pe_hi'], V['peer_pe_lo']


# Table numbers are ASSIGNED IN DOCUMENT ORDER by this counter, never typed. The first
# edition carried two tables numbered 11 and two numbered 17 because they were typed by hand.
_TN = [0]


def tnum():
    _TN[0] += 1
    return _TN[0]


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
      f'There is no single number, and that is deliberate. Five readings put fair value '
      f'between EGP {n0(LN["fair_bear"])} and EGP {n0(LN["fair_bull"])} a share. Because the '
      f'contested judgement below is carried BOTH ways and the two are never averaged, the '
      f'study publishes TWO weighted centres: EGP {n2(LN["centre_A"])} a share on the '
      f'permanent-provision reading and EGP {n2(LN["centre_B"])} on the normalising one. The '
      f'market price is EGP {n2(SPOT)}. That gap is the study, and section 1.7 states exactly '
      f'what would have to be true for the market to be right.'),
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
      f'centre moves from a single EGP 79.64 to a PAIR — EGP {n2(LN["centre_A"])} and EGP '
      f'{n2(LN["centre_B"])} a share. Section 7 lists what changed and by how much.'),
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
      'They are never averaged into one number — which is why this edition publishes two '
      'weighted centres rather than one. The first edition weighted both frames at a quarter '
      'each inside a single centre, and weighting both frames inside one number IS averaging '
      'them; that centre has been withdrawn.')])

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
  f'licensed it in December 2025. From FY2026 that balance starts depreciating: the charge '
  f'goes from an audited EGP {n1(V["dna_fy25"])} million to EGP {n0(FC["dna"][0])} million in '
  f'FY2026E and EGP {n0(max(FC["dna"]))} million at its peak. The finance cost, meanwhile, '
  f'does NOT rise: the first quarter of 2026 ran at EGP {n1(V["q1_fin"])} million, an annual '
  f'rate of about EGP {n0(V["q1_fin"] * 4)} million against EGP {n0(V["fin_fy25"])} million '
  f'actually borne in FY2025, so the forecast charges LESS interest, not more. The net '
  f'mechanical change this study carries is therefore EGP '
  f'{n0(FC["dna"][0] - V["dna_fy25"] - (V["fin_fy25"] - V["int_path"][0]))} million a year of '
  f'additional pre-tax charge, not the EGP 700 million a first reading of the licensing event '
  f'suggests. The larger figure would require adding back the EGP {n0(W["capitalised_interest_fy25"])} '
  f'million of interest that was being capitalised, and the company\'s own first quarter says '
  f'that is not what is happening. Either way the plant contributes no revenue yet.')
P(f'Against that, four methods that do not depend on the new plant at all — discounted cash '
  f'flow, run on two framings of the provision charge and so giving five readings in total; '
  f'book value against sustainable return; triangulated multiples; and normalised earnings '
  f'power — cluster between EGP {n0(LN["fair_bear"])} and EGP {n0(LN["fair_bull"])}. The '
  f'market is above all of them.')
P(f'The first quarter of 2026, reviewed and published in May, settles part of that question '
  f'and sharpens the rest. Fixed assets rose EGP {n0(V["q1_ppe"] - V["ppe_fy25"])} million and '
  f'the construction balance fell EGP {n0(V["cip_fy25"] - V["q1_cip"])} million in three '
  f'months; depreciation and amortisation went to EGP {n1(V["q1_dna"])} million from EGP '
  f'{n1(V["q1_dna_ly"])} million a year earlier, more than double. The plant is in service and '
  f'the charge has arrived, exactly as this study said it would. What has not arrived is the '
  f'revenue: net sales grew {pc(V["q1_rev"] / V["q1_rev_ly"] - 1)} and attributable profit '
  f'FELL {pc(abs(V["q1_parent"] / V["q1_parent_ly"] - 1))} to EGP {n0(V["q1_parent"])} million.')
figure(os.path.join(HERE, 'fig1_field.png'), 6.9,
       'Figure 1 — five readings and TWO centres. The two provision frames are published side '
       'by side and are never averaged into one number.')

# ============================ 3. VALUATION SUMMARY =============================
H1('Valuation summary')
rows = [['Reading', 'EGP / share', 'vs market', 'Note']]
for it in LN['items_A'][:1] + LN['items_B'][:1] + LN['shared']:
    if it['name'].endswith('Frame A'):
        note = (f"terminal value {pc(A['tv_share'], 0)} of core enterprise value, "
                f"{pc(A['tv_share_total'], 0)} of total")
    elif it['name'].endswith('Frame B'):
        note = (f"terminal value {pc(Bf['tv_share'], 0)} of core enterprise value, "
                f"{pc(Bf['tv_share_total'], 0)} of total")
    elif it['name'].startswith('Book'):
        note = f"justified {n2(LN['just_pb'])}x book of EGP {n2(LN['bv_ps'])}"
    elif it['name'].startswith('Relative'):
        note = 'three multiples, each on the earnings of its own period'
    else:
        note = f"three-year average margin {pc(LN['norm_margin'])}"
    rows.append([it['name'], n2(it['value']), pc(it['value'] / SPOT - 1, 0), note])
rows.append(['WEIGHTED CENTRE — Frame A', n2(LN['centre_A']),
             pc(LN['centre_A'] / SPOT - 1, 0),
             'Frame A at 50% weight beside the three lenses that do not turn on the judgement'])
rows.append(['WEIGHTED CENTRE — Frame B', n2(LN['centre_B']),
             pc(LN['centre_B'] / SPOT - 1, 0),
             'The same three lenses beside Frame B. The two centres are NEVER averaged'])
rows.append(['Field low to field high', f"{n2(LN['fair_bear'])} – {n2(LN['fair_bull'])}", '',
             'The spread between the readings IS the uncertainty'])
rows.append(['Market price', n2(SPOT), '', 'Close of 6 August 2026'])
table(rows, [2.35, 1.05, 0.85, 2.75], band_rows={6, 7, 9}, size=9.0)
caption(f'Table {tnum()} — the summary valuation table. TWO centres, never one: the contested '
        f'judgement is carried both ways and weighting both frames inside a single number '
        f'would average them. Terminal value is stated beside each cash-flow reading on BOTH '
        f'bases — as a share of the core operating value and of the total, which also carries '
        f'the associates and the assets held for sale.')

rows = [['Key figures', 'Value', 'Key figures', 'Value']]
kf = [('Market capitalisation', f"EGP {n0(W['mcap'])}m"),
      ('Net debt', f"EGP {n0(W['net_debt'])}m"),
      ('Enterprise value', f"EGP {n0(W['mcap'] + W['net_debt'] + V['nci_bridge'])}m"),
      ('FY2025 revenue', f"EGP {n0(V['rev_fy25'])}m"),
      ('FY2025 EBITDA', f"EGP {n0(H['FY2025']['ebitda'])}m"),
      ('FY2025 attributable profit', f"EGP {n0(V['parent_fy25'])}m"),
      ('Trailing price / earnings', f"{n2(LN['pe_now'])}x on shares in issue, "
       f"{n2(LN['pe_now_wavg'])}x on the FY2025 weighted average"),
      ('Trailing enterprise value / EBITDA', f"{n1(LN['evebitda_now'])}x"),
      ('Cost of equity', pc(W['ke'], 2)),
      ('Discount rate, first year', pc(W['wacc0'], 2)),
      ('Discount rate, terminal', pc(W['wacc_term'], 2)),
      ('Proposed dividend, FY2025', f"EGP {n2(V['dps_fy25'])} ({pc(V['q_annual'])} yield)")]
for i in range(0, len(kf), 2):
    rows.append([kf[i][0], kf[i][1], kf[i + 1][0], kf[i + 1][1]])
table(rows, [2.2, 1.3, 2.2, 1.3], size=9.0)
caption(f'Table {tnum()} — the figures a reader needs before anything else. Enterprise value '
        f'uses the post-deconsolidation non-controlling interest of EGP {n1(V["nci_bridge"])} '
        f'million that the valuation bridge uses, so the enterprise value and the multiple '
        f'beside it are struck on one basis. The audited 31 December 2025 minority of EGP '
        f'{n1(V["nci_fy25"])} million would give EGP '
        f'{n0(W["mcap"] + W["net_debt"] + V["nci_fy25"])} million instead; the two are not '
        f'mixed. Two trailing multiples are shown because the share count rose during FY2025 '
        f'and both readings are legitimate.')

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
tot24 = (V['ch_direct_fy24'] + V['ch_distrib_fy24'] + V['ch_tender_fy24'] +
         V['ch_export_fy24'] + V['ch_toll_fy24'])
rows.append(['Total (company only)', n0(tot24), n0(tot25), pc(tot25 / tot24 - 1, 0), '100%'])
table(rows, [2.15, 1.25, 1.25, 0.85, 1.2], band_rows={6}, size=9.0)
caption(f'Table {tnum()} — the disclosed revenue split, each total SUMMED from its own column. '
        f'Exports are 32% of the book and are earned in hard currency; the domestic price is '
        f'set administratively by the Egyptian Drug Authority. The step from this '
        f'separate-company total to the audited consolidated revenue is the subsidiary\'s '
        f'external sales: {n2(V["rev_fy25"] / tot25)} times in FY2025 and '
        f'{n2(V["rev_fy24"] / tot24)} times in FY2024. The forecast carries the FY2025 '
        f'reading. Two observations are not a trend, and the FY2024 reading would add about '
        f'{pc(V["rev_fy24"] / tot24 - V["rev_fy25"] / tot25, 1)} to forecast revenue; the '
        f'range is disclosed rather than the single figure being presented as measured fact.')
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
rows.append(['Tax rate (the EFFECTIVE rate the business bears)'] + [pc(W['tax_fcff'], 1)] * 5)
rows.append(['NOPAT = EBIT x (1 − tax rate)'] +
            [n0(x * (1 - W['tax_fcff'])) for x in FC['ebit_A']])
rows.append(['Add back depreciation and amortisation'] + [n0(x) for x in FC['dna']])
rows.append(['Less capital expenditure'] + [f'({n0(x)})' for x in FC['capex']])
rows.append(['Less increase in working capital'] +
            [f'({n0(x)})' if x >= 0 else n0(-x) for x in FC['dwc']])
rows.append(['Free cash flow to the firm'] + [n0(x) for x in A['fcff']])
rows.append(['Discount rate'] + [pc(x, 2) for x in W['disc_rate']])
rows.append(['Discount factor'] + [f'{x:.4f}' for x in W['df']])
rows.append(['Present value of free cash flow'] + [n0(x) for x in A['pv']])
table(rows, [2.35, 0.92, 0.92, 0.92, 0.92, 0.92], band_rows={4, 8, 12, 15}, size=8.6)
caption(f'Table {tnum()} — the full free-cash-flow waterfall through to present value, Frame A.')

rows = [['Enterprise value to equity value', 'EGP million', 'EGP / share'],
        ['Present value of five years of free cash flow', n0(A['pv_sum']),
         n2(A['pv_sum'] / SH)],
        ['Present value of the terminal value', n0(A['pv_tv']), n2(A['pv_tv'] / SH)],
        ['Core enterprise value', n0(A['ev_core']), n2(A['ev_core'] / SH)],
        ['Terminal value as a percentage of CORE enterprise value', pc(A['tv_share'], 0), ''],
        ['Add: earning associates at normalised earnings times the multiple',
         n0(A['assoc_earnings_value']), n2(A['assoc_earnings_value'] / SH)],
        ['Add: the pre-revenue active-ingredient company at CARRYING COST',
         n0(A['arab_api_cost']), n2(A['arab_api_cost'] / SH)],
        ['Add: assets held for sale', n0(V['afs_fy25']), n2(V['afs_fy25'] / SH)],
        ['Total enterprise value', n0(A['ev_total']), n2(A['ev_total'] / SH)],
        ['Terminal value as a percentage of TOTAL enterprise value',
         pc(A['tv_share_total'], 0), ''],
        ['Less: net debt', f"({n0(A['net_debt'])})", f"({n2(A['net_debt'] / SH)})"],
        ['Less: non-controlling interests', f"({n0(A['nci'])})", f"({n2(A['nci'] / SH)})"],
        ['Equity value — Frame A', n0(A['equity']), n2(A['per_share'])],
        ['Equity value — Frame B', n0(Bf['equity']), n2(Bf['per_share'])]]
table(rows, [3.55, 1.6, 1.55], band_rows={4, 9, 10, 13, 14}, size=9.0)
caption(f'Table {tnum()} — the enterprise-to-equity bridge. The terminal share is shown on BOTH '
        f'bases, as a line of the bridge rather than a footnote: it is {pc(A["tv_share"], 0)} of '
        f'the CORE operating value and {pc(A["tv_share_total"], 0)} of the total, which also '
        f'carries the associates and the assets held for sale. The pre-revenue '
        f'active-ingredient company sits on its OWN line at carrying cost — it is not '
        f'earnings, and it is not folded into a line that says it is. The non-controlling '
        f'interest deducted is the post-deconsolidation figure; the audited 31 December 2025 '
        f'minority of EGP {n1(V["nci_fy25"])} million belonged to the subsidiary that was '
        f'deconsolidated in the first quarter, and section 7 records that the net debt above '
        f'is the December balance while this deduction is the March one.')

H2('1.2 Book value and sustainable return')
P(f'Book value attributable to shareholders was EGP {n0(V["equity_parent_fy25"])} million at '
  f'the year end, EGP {n2(LN["bv_ps"])} a share. Return on average equity was '
  f'{pc(LN["roe_fy24"])} in FY2024 and {pc(LN["roe_fy25"])} in FY2025. The forecast path is '
  + ' / '.join(pc(x) for x in FC['roe']) +
  f' — it RISES through the window rather than settling, so the sustainable return used here '
  f'is the mean of its last three years, {pc(LN["roe_sust"], 2)}, read off that path rather '
  f'than chosen. A business earning {pc(LN["roe_sust"])} on equity while its '
  f'perpetual cost of equity is {pc(W["ke_term"], 2)} is worth more than its book: the '
  f'multiple that relationship justifies is (return less growth) over (cost of equity less '
  f'growth), or {n2(LN["just_pb"])} times book — EGP {n2(LN["book_ps"])} a share.')

H2('1.3 Relative multiples')
P(f'The company\'s own traded history is the primary anchor here, because it is computable '
  f'entirely from primary material: audited attributable profit against the year-end close. '
  f'It traded on ' +
  ', '.join(f"{o['pe']:.1f} times in {o['year']}" for o in LN['own_pe_history']) +
  f' — a four-year mean of {n2(LN["own_pe_mean"])}. Each year divides that year\'s audited '
  f'attributable profit by that year\'s own weighted-average share count, so FY2025 uses '
  f'{n2(V["wavg_shares_fy25"])} million shares rather than the {n2(SH)} million now in issue: '
  f'the capital increase completed during that year. At EGP {n2(SPOT)} the shares trade on '
  f'{n2(LN["pe_now"])} times trailing attributable earnings on the count in issue today, or '
  f'{n2(LN["pe_now_wavg"])} times on the audited weighted average — both readings are '
  f'legitimate and both are given — and {n1(LN["evebitda_now"])} times trailing EBITDA. The '
  f'earnings multiple has more than doubled against its own four-year history. That is the '
  f'single most important fact about this share price.')
rows = [['Multiple', 'Times', 'EGP / share', 'Where it comes from']]
_WHY = {
    'Justified forward multiple from this model, on FY2026E earnings':
        f"a FORWARD multiple on FORWARD earnings of EGP {n2(LN['eps_fwd'])}. Retention must "
        f"equal growth {pc(V['g_term'], 0)} over sustainable return {pc(LN['roe_sust'])}, so "
        f"payout is {pc(LN['payout_implied'], 0)}",
    "The company's own four-year mean multiple, on trailing earnings":
        f"a TRAILING multiple on TRAILING earnings of EGP {n2(LN['eps_ttm'])} — year-end "
        f"closes against audited attributable profit",
    'Struck peer reference, cost-of-equity adjusted, on trailing earnings':
        f"a TRAILING multiple on TRAILING earnings. The midpoint of the only two disclosed "
        f"observations, {PEER_HI:.1f}x and {PEER_MID:.1f}x — not a median of a peer set. "
        f"Those companies face a cost of equity near 10%, not {pc(W['ke_term'], 1)}",
}
for nm, mult, val_ in LN['rel_triangulation']:
    rows.append([nm, f'{mult:.2f}x', n2(val_), _WHY[nm]])
rows.append(['Average of the three — the relative lens',
             f"{sum(t[1] for t in LN['rel_triangulation']) / 3:.2f}x", n2(LN['rel_ps']),
             'Averaged on the sheet, not asserted'])
table(rows, [2.05, 0.7, 0.95, 3.0], band_rows={4}, size=8.8)
caption(f'Table {tnum()} — three multiples triangulated, EACH APPLIED TO THE EARNINGS OF ITS OWN '
        f'PERIOD. Left unadjusted for the cost-of-equity gap, the struck peer reference alone '
        f'would give EGP {n2(LN["rel_peer_unadjusted"])} a share; the size of that gap IS the '
        f'country-risk discount, shown rather than hidden. The peers behind the third leg are '
        f'not named and their financial statements are not published, so that leg cannot be '
        f'rebuilt from their filings — a stated limitation of the leg, and the reason the lens '
        f'carries two other legs.')
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

H2('1.5 Synthesis — four methods, five readings, two centres')
P(f'Four methods produce five readings, because the cash-flow method is run on both framings '
  f'of the contested provision judgement. They run from EGP {n0(LN["fair_bear"])} to EGP '
  f'{n0(LN["fair_bull"])}. That spread is not a failure of the methods; it is the honest '
  f'measure of how much the answer depends on which question you ask.')
P(f'There is no single weighted centre, and the absence is deliberate. The two provision '
  f'frames are never averaged, and weighting both of them inside one number averages them. So '
  f'the cash-flow weight of {pc(LN["w_dcf"], 0)} is carried in full on ONE frame at a time, '
  f'beside the three lenses that do not turn on the judgement at all — book value against '
  f'sustainable return at {pc(LN["shared"][0]["weight"], 0)}, relative multiples at '
  f'{pc(LN["shared"][1]["weight"], 0)}, and normalised earnings power at '
  f'{pc(LN["shared"][2]["weight"], 0)}. That gives EGP {n2(LN["centre_A"])} a share on Frame A '
  f'and EGP {n2(LN["centre_B"])} on Frame B, against a market price of EGP {n2(SPOT)}. Which '
  f'of the two a reader uses is a judgement about the debtor book, and it belongs to the '
  f'reader.')

H2('1.6 Drivers — every segment grown on its own driver')
P(f'Revenue is not grown as a percentage. It is built from THREE product lines, each with '
  f'its own volume and its own price, all taken from disclosure. The company\'s board report '
  f'splits the same total two different ways — by sales channel and by product line — and the '
  f'two only reconcile once contract manufacturing is separated out.')
P(f'LINE 1 AND LINE 2, the company\'s OWN preparations. It sold '
  f'{n1(V["packs_own_fy25"])} million packs of them in FY2025 for EGP '
  f'{n0(V["own_prep_value_fy25"])} million. The investor presentation puts export volume at '
  f'{n0(UB["exp_packs_fy25"])} million packs earning EGP {n0(V["ch_export_fy25"])} million, '
  f'which is USD {n2(UB["exp_price_usd_fy25"])} a pack at the disclosed average rate. The '
  f'remainder — {n1(UB["dom_packs_fy25"])} million packs carrying EGP '
  f'{n0(UB["dom_own_rev_fy25"])} million — is the domestic book at EGP '
  f'{n2(UB["dom_price_fy25"])} a pack, against EGP {n2(UB["dom_price_fy24"])} in FY2024: a '
  f'realised price up {pc(UB["dom_price_fy25"] / UB["dom_price_fy24"] - 1)} on volume up '
  f'{pc(UB["dom_packs_fy25"] / UB["dom_packs_fy24"] - 1)}.')
P(f'LINE 3, preparations made under contract for third parties. This is a different business '
  f'and it is now modelled as one: {n2(UB["toll_packs_fy25"])} million packs in FY2025 against '
  f'{n2(UB["toll_packs_fy24"])} million in FY2024, carrying EGP '
  f'{n1(V["contract_value_fy25"])} million of product value. The company books EGP '
  f'{n1(V["ch_toll_fy25"])} million of that as a manufacturing fee — EGP '
  f'{n2(UB["toll_fee_pp_fy25"])} a pack against EGP {n2(UB["toll_fee_pp_fy24"])} the year '
  f'before — and the remaining EGP {n1(UB["contract_resale_fy25"])} million reaches the market '
  f'through its own domestic channels.')
P(f'That separation matters more than its size. The channel disclosure puts domestic revenue '
  f'at EGP {n0(UB["dom_rev_fy25"])} million, but that figure CARRIES the contract-made product '
  f'while the pack count against it does NOT carry the contract packs. Dividing one by the '
  f'other reads EGP {n2(UB["dom_rev_fy25"] / UB["dom_packs_fy25"])} a pack rather than the EGP '
  f'{n2(UB["dom_price_fy25"])} the company actually realised on its own preparations — '
  f'{pc(UB["dom_rev_fy25"] / UB["dom_packs_fy25"] / UB["dom_price_fy25"] - 1, 2)} too high, in '
  f'every forecast year. The two disclosures now close on each other to the thousand pound in '
  f'both years, and the model asserts it. Margins are an OUTPUT of this build, never an input.')
rows = [['Driver'] + YR]
rows.append(['Domestic packs, own preparations (million)'] + [n1(x) for x in FC['dom_packs']])
rows.append(['Domestic price per pack (EGP)'] + [n2(x) for x in FC['dom_price']])
rows.append(['Export packs (million)'] + [n1(x) for x in FC['exp_packs']])
rows.append(['Export price per pack (USD)'] + [n2(x) for x in FC['exp_price_usd']])
rows.append(['Exchange rate (EGP per USD)'] + [n1(x) for x in FC['fx']])
rows.append(['Contract-manufactured packs (million)'] + [n2(x) for x in FC['toll_packs']])
rows.append(['Contract manufacturing fee per pack (EGP)']
            + [n2(x) for x in FC['toll_fee_pp']])
rows.append(['Contract product resold, price per pack (EGP)']
            + [n2(x) for x in FC['resale_pp']])
rows.append(['Revenue (EGP million)'] + [n0(x) for x in FC['revenue']])
rows.append(['Gross margin (an output)'] + [pc(x) for x in FC['gross_margin']])
table(rows, [2.35, 0.92, 0.92, 0.92, 0.92, 0.92], band_rows={10}, size=8.8)
caption(f'Table {tnum()} — the forecast driver table. THREE product lines, each with its own '
        f'volume and its own price, moving separately and in the currency each is actually '
        f'earned in. Nothing on this table is a revenue growth rate.')
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
caption(f'Table {tnum()} — one escalator per driver class. A single blended index across these lines '
        'would make the forecast margin an artefact of the index rather than of the business.')

H2('1.7 The crux')
P(f'The crux is the new plant, and it is worth being precise about what this study does and '
  f'does not assume. It CHARGES the plant: EGP {n0(V["cip_fy25"])} million of construction '
  f'balance transfers into depreciable assets on the company\'s own disclosed licensing '
  f'timetable, taking the depreciation charge from EGP {n0(V["dna_fy25"])} million in FY2025 '
  f'to EGP {n0(FC["dna"][0])} million in FY2026 and EGP {n0(FC["dna"][2])} million by FY2028. '
  f'What it does NOT do is add the EGP '
  f'{n0(V["capint_cum_fy25"] - V["capint_cum_fy24"])} million of interest capitalised into '
  f'the construction balance in FY2025 back onto the income statement. That would be the '
  f'textbook consequence of the asset entering service, and the first cut of this model '
  f'assumed it — but the company\'s own first quarter of 2026 says otherwise: financing '
  f'expense of EGP {n1(V["q1_fin"])} million ran DOWN '
  f'{pc(abs(V["q1_fin"] * 4 / V["fin_fy25"] - 1))} year on year, an annual rate near EGP '
  f'{n0(V["q1_fin"] * 4)} million against EGP {n0(V["fin_fy25"])} million actually borne in '
  f'FY2025. The forecast is calibrated to that observed quarter rather than to the textbook, '
  f'and the difference is disclosed here rather than left as an unexplained gap. It does NOT '
  f'credit the plant with any revenue, because the company has published none.')
figure(os.path.join(HERE, 'fig3_depreciation.png'), 6.7,
       'Figure 4 — the depreciation step, and the construction balance that causes it.')
P(f'So the honest question is not what the plant is worth. It is how much it must sell. '
  f'Solving the same model for the market price: an additional EGP '
  f'{n0(CRUX["required_fy30_revenue"])} million of revenue by FY2030 at a 45% contribution '
  f'margin closes the gap from EGP {n2(A["per_share"])} to EGP {n2(SPOT)}. That is '
  f'{pc(CRUX["required_share_of_fy30"], 0)} of FY2030 revenue, or about USD '
  f'{n0(CRUX["required_rev_usd_mn"])} million a year — {n2(CRUX["asset_turn"])} times the USD '
  f'100 million the company says it invested in the plant.')
P('Two things have to be published for that hurdle to be checkable, and they are. THE RAMP: '
  'the incremental revenue is not dropped into the final year. It is phased '
  + ' / '.join(f'{x * 100:.0f}%' for x in D['crux_ramp']) +
  f' of the FY2030 level across FY2026E to FY2030E. The same total placed entirely in the '
  f'final year would be a materially LOWER and easier hurdle, so a reverse valuation that '
  f'does not state its ramp cannot be audited. THE REINVESTMENT: the incremental revenue is '
  f'charged capital expenditure at the same share of revenue as the existing business, and '
  f'working capital on the same day ratios, so it meets the identical reinvestment discipline. '
  f'Left uncharged — which is how the first cut of this model ran it — the hurdle prices out '
  f'about USD 115 million a year instead of USD {n0(CRUX["required_rev_usd_mn"])} million, '
  f'which understates what the market is actually asking of the plant.')
P(f'The same arithmetic read the other way is worth stating, because it is the plainest '
  f'summary of what is at issue. At EGP {n2(SPOT)} the market is paying EGP '
  f'{n2(SPOT - A["per_share"])} a share — EGP {n0((SPOT - A["per_share"]) * SH)} million, '
  f'{pc((SPOT - A["per_share"]) / SPOT, 0)} of the entire share price — for a plant this '
  f'study values at nothing, against a stated build cost of USD '
  f'{n0(V["plant_cost_usd_mn"])} million, about EGP '
  f'{n0(V["plant_cost_usd_mn"] * FC["fx"][-1])} million. The market is not merely paying for '
  f'the plant to work; it is paying roughly '
  f'{(SPOT - A["per_share"]) * SH / (V["plant_cost_usd_mn"] * FC["fx"][-1]):.1f} times what '
  f'the plant cost to build. That is the proposition, stated as a multiple of an observable '
  f'outlay rather than as a valuation.')
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
    ['Attributable profit (EGP m)', n0(V['q1_parent']),
     n0(V['q1_parent'] / V['q1_share_of_year_profit']), n0(FC['parent'][0]),
     f"the study is {pc(FC['parent'][0] / (V['q1_parent'] / V['q1_share_of_year_profit']) - 1, 0)} "
     f"below the quarter's seasonal read"],
    ['Attributable earnings per share (EGP)', n2(V['q1_parent'] / SH),
     n2(V['q1_parent'] / V['q1_share_of_year_profit'] / SH), n2(FC['parent'][0] / SH),
     'the two lines the appendix must reproduce, checked here'],
]
table(rows, [1.75, 0.95, 1.05, 1.0, 2.3], size=8.2)
caption(f'Table {tnum()} — the forecast against the first quarter it can be checked on, INCLUDING '
        f'the bottom line. The middle column reads the quarter into a year on the FY2025 '
        f'seasonal shape ONLY for net sales ({pc(V["q1_share_of_year_rev"], 1)} of sales) and '
        f'for attributable profit and earnings per share '
        f'({pc(V["q1_share_of_year_profit"], 1)} of profit). Every other line in that column '
        f'is a plain four-times annualisation, because no seasonal shape is disclosed for it — '
        f'stated rather than implied.')
P(f'Two of those rows carry more weight than the rest. The depreciation line is the study\'s '
  f'central claim and it is confirmed: the charge is running at roughly double last year on a '
  f'plant that has only just entered service, and the model\'s own depreciation rate '
  f'reproduces the quarter to within 3%. The provision line is the study\'s contested '
  f'judgement, and here the quarter does NOT settle it: the company took EGP {n0(V["q1_prov"])} '
  f'million of provisions and inventory write-downs but no credit-loss charge whatsoever, '
  f'against receivables that grew EGP {n0(V["q1_ar"] - V["ar_fy25"])} million in the same three '
  f'months. The auditor qualified the review on precisely that point. Put a number on it: '
  f'Frame A\'s {pc(V["prov_pct_permanent"], 2)} of revenue applied to the quarter\'s own '
  f'sales would have charged EGP {n1(V["q1_rev"] * V["prov_pct_permanent"])} million — '
  f'{pc(V["q1_rev"] * V["prov_pct_permanent"] / V["q1_parent"], 0)} of the attributable '
  f'profit the quarter actually reported — and even the three-year expected-credit-loss mean '
  f'of {pc(SENS["prov_ecl_3yr_mean"], 2)} would have charged EGP '
  f'{n1(V["q1_rev"] * SENS["prov_ecl_3yr_mean"])} million, or '
  f'{pc(V["q1_rev"] * SENS["prov_ecl_3yr_mean"] / V["q1_parent"], 0)} of it. A charge that '
  f'is omitted in the first quarter is deferred, not avoided, which is why both frames still '
  f'run.')

H2('1.8 Macro and country — the cost of capital')
P(f'The quoted ten-year Egyptian local-currency government yield is {pc(V["rf"], 2)}. That '
  f'yield is not riskless: it contains the sovereign\'s own default risk. Subtracting Egypt\'s '
  f'sovereign credit-default-swap spread of {pc(V["sov_spread_cds"], 2)} leaves a normalised '
  f'risk-free rate of {pc(W["rf_star"], 2)}. Adding beta times the TOTAL equity risk premium '
  f'gives the cost of equity. Charging the raw {pc(V["rf"], 2)} yield AND a country-loaded '
  f'premium would give {pc(W["ke_double_counted_retired"], 2)} and would count sovereign risk '
  f'twice; that construction is not used here.')
rows = [['Cost of capital', 'Swap basis', 'Rating basis', 'Source and construction']]
rows += [
    ['Ten-year local-currency yield', pc(V['rf'], 2), pc(V['rf'], 2),
     'Observable print of 6 August 2026 — the SAME date as the share price used throughout. '
     'A market-data series, not an auction print: the central bank auction page could not be '
     'read, so the level is indicated rather than proven, and it is sensitised'],
    ['Less sovereign default spread', pc(V['sov_spread_cds'], 2), pc(V['sov_spread_rating'], 2),
     'Country risk-premium dataset, Egypt row, MID-YEAR (July 2026) vintage, spreads measured '
     '30 June 2026'],
    ['Normalised risk-free rate', pc(W['rf_star'], 2),
     pc(V['rf'] - V['sov_spread_rating'], 2), 'The subtraction above'],
    ['TOTAL equity risk premium', pc(V['erp_cds'], 2), pc(V['erp_rating'], 2),
     "Same dataset, same row, its two TOTAL equity risk premium columns. This is the figure "
     "that multiplies beta"],
    ['   memorandum: country risk premium', pc(W['crp_cds'], 2), pc(W['crp_rating'], 2),
     'The dataset\'s separate COUNTRY risk premium column, shown so a reader checking that '
     'column finds the same numbers this study calls by that name. It is NOT added to the '
     'cost of equity — the total premium above already contains it'],
    ['Beta', f"{V['beta']:.3f}", f"{V['beta']:.3f}",
     'Own-stock weekly regression against a 36-name local composite, five years; '
     'R-squared 0.235, n = 257, standard error 0.071'],
    ['COST OF EQUITY', pc(W['ke'], 2), pc(W['ke_rating'], 2),
     f"The two bases agree to {abs(W['ke'] - W['ke_rating']) * 1e4:.0f} basis points"],
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
     f"{pc(W['kd_term_at'], 2)}, DERIVED debt weight {pc(W['wd_term'], 1)} on today's market "
     f"values. The forecast balance sheet, once funded, carries {pc(W['wd_term_book'], 1)} on "
     f"book at FY2030E, which would give {pc(W['wacc_term_book_basis'], 2)} — both are "
     f"published and neither is 20%"]]
table(rows, [1.95, 0.95, 0.95, 3.15], band_rows={7, 13, 14}, size=8.4)
caption(f'Table {tnum()} — the cost of capital, built rather than asserted, and published on both '
        'bases the source provides.')
P(f'A cost-of-debt cross-check that a reader can run. Two FY2025 figures are in play and '
  f'they are not the same line: INTEREST ON CREDIT FACILITIES of EGP '
  f'{n2(V["int_fac_fy25"])} million, which is what an interest RATE has to be computed on, '
  f'and the income statement\'s FINANCE COSTS of EGP {n2(V["fin_fy25"])} million, which is '
  f'that interest plus EGP {n2(V["fin_fy25"] - V["int_fac_fy25"])} million of bank commissions '
  f'and charges. Both are in the same note. The company expensed EGP '
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
P('Before the grids, the one input that carries the study\'s contested judgement, read every '
  'way the disclosed statements allow. Frame A carries '
  + pc(V['prov_pct_permanent'], 2) + ' of revenue. That is NOT the three-year average, and '
  'this edition no longer calls it one: it is struck marginally above the mean of the two '
  'years either side of the FY2024 spike. Every reading, and what each is worth:')
rows = [['Reading of the provision charge', 'Share of revenue', 'Frame A value (EGP/share)']]
for nm, p, v_ in SENS['prov_readings']:
    rows.append([nm, pc(p, 2), n2(v_)])
table(rows, [3.5, 1.35, 1.85], band_rows={1}, size=8.8)
caption(f'Table {tnum()} — the contested judgement, priced on every reading of it the audited '
        f'statements support. The three-year mean of {pc(SENS["prov_3yr_mean"], 2)} includes '
        f'the FY2024 spike of {pc(V["prov_fy24"] / V["rev_fy24"], 2)}; the '
        f'expected-credit-loss component alone averages {pc(SENS["prov_ecl_3yr_mean"], 2)} '
        f'across the same three years. For context that none of these readings carries: the '
        f'first quarter of 2026 booked NO expected credit loss at all.')
figure(os.path.join(HERE, 'fig6_tornado.png'), 6.7,
       'Figure 6 — what actually moves the answer. Each bar is the full range of the value per '
       'share across a plausible range of that one input.')
rows = [['Terminal growth →', *[pc(g, 0) for g in SENS['grid_g']]]]
for i, w_ in enumerate(SENS['grid_wacc']):
    rows.append([f'Cost of equity {w_ * 10000:+.0f} basis points'] +
                [n0(SENS['grid'][i][j]) for j in range(5)])
table(rows, [2.15, 0.95, 0.95, 0.95, 0.95, 0.95], size=8.8)
caption(f'Table {tnum()} — the value per share across the cost of equity and terminal growth '
        f'together. Every cell is a complete revaluation. The grid runs from EGP '
        f'{n0(SENS["grid_lo"])} to EGP {n0(SENS["grid_hi"])} a share, and that FULL range is '
        f'what is published — quoting only its upper part would delete the half of the study\'s '
        f'own risk display that matters most.')
_STEP_EGP_M = CRUX['required_fy30_revenue'] / 4          # a quarter of the required revenue
_STEP_USD_M = CRUX['required_rev_usd_mn'] / 4
_PER_EGP_M = (SPOT - A['per_share']) / CRUX['required_fy30_revenue']
P(f'The crux is sensitised in real observable units rather than in percentage points. On the '
  f'published ramp and with the incremental revenue charged the same reinvestment identity as '
  f'the existing business, a quarter of the required revenue — EGP {n0(_STEP_EGP_M)} million '
  f'of FY2030 sales, or USD {n0(_STEP_USD_M)} million a year — is worth about EGP '
  f'{n2(_PER_EGP_M * _STEP_EGP_M)} a share.')

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
caption(f'Table {tnum()} — support and resistance, computed from recency-weighted pivot clusters on '
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
caption(f'Table {tnum()} — the percentile map. The anchor is the EGP '
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
caption(f'Table {tnum()} — the level-touch ladder. Touching a level at any point during the window '
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
  f'{BT["full"]["skill_norm"]:+.4f}. A third set was run on the period AFTER the currency '
  f'break that dominates the older history — {BT["production"]["windows"]} windows from '
  f'{BT["production"]["first_origin"]} to {BT["production"]["last_origin"]}, scoring '
  f'{BT["production"]["skill_norm"]:+.4f} — and it is published here because it is the set '
  f'that matches the period the bands shown above are built on. All three are reported '
  f'together; reporting only two of three would be a choice about which evidence a reader '
  f'sees. In plain terms: on this single share the method is indistinguishable from a random '
  f'walk, and this study says so rather than claiming an edge it cannot demonstrate.')
P(f'What the tests DO show is that the bands are honestly sized, which is the property that '
  f'matters for reading them. Across the five-year window set the outcome fell inside the 90% '
  f'band {pc(BT["five_year"]["cov90"], 0)} of the time and inside the 50% band '
  f'{pc(BT["five_year"]["cov50"], 0)} of the time, and the distribution of where outcomes '
  f'landed within the bands was statistically indistinguishable from uniform (chi-square '
  f'p = {BT["five_year"]["chi2_p"]}, Kolmogorov-Smirnov p = {BT["five_year"]["ks_p"]}). The '
  f'bands are also about {BT["five_year"]["width_vs_benchmark"]:.2f} times as wide as the '
  f'benchmark\'s, which means they are conservative rather than flattering. Read them as an '
  f'honest width, not as a claim to foresight.')
P(f'Two volatilities, both published. The simulation is fed '
  f'{pc(STRIKE["horizons"]["1M"]["anchor_vol_ann"], 2)} annualised at the one-month horizon '
  f'and {pc(STRIKE["horizons"]["3M"]["anchor_vol_ann"], 2)} at three months — the two windows '
  f'genuinely '
  f'differ, and stating only the lower of them would understate the near-term width the map '
  f'itself shows. A reader who back-solves an annualised volatility from the published fifth '
  f'and ninety-fifth percentiles under a plain lognormal will get a NARROWER number than '
  f'either, because the simulated process is not a plain lognormal: it carries a fat-tailed '
  f'innovation and mean reversion in variance, both of which pull the central quantiles in '
  f'relative to the volatility that feeds them. The generator, its parameters and the window '
  f'outcomes behind the coverage statistics are listed in the accompanying bibliography so '
  f'the check can be run properly rather than approximated.')

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
     'when the comparable companies face a different country risk, which is why the struck '
     'reference is adjusted rather than applied raw'],
    ['Normalised earnings power', n2(LN['norm_ps']),
     'the choice of normal margin',
     'when the business has genuinely re-based upward, in which case a three-year average '
     'understates it']]
table(rows, [1.85, 0.85, 2.05, 2.65], size=8.4)
caption(f'Table {tnum()} — the four methods against each other — five readings, because the '
        f'cash-flow method is run on both framings of the contested judgement — including '
        f'where each one fails.')
_LO = min((A['per_share'], 'the cash-flow reading on the permanent-provision frame'),
          (Bf['per_share'], 'the cash-flow reading on the normalising frame'),
          (LN['book_ps'], 'the book-value lens'), (LN['rel_ps'], 'the relative lens'),
          (LN['norm_ps'], 'the normalised-earnings lens'))
_HI = max((A['per_share'], 'the cash-flow reading on the permanent-provision frame'),
          (Bf['per_share'], 'the cash-flow reading on the normalising frame'),
          (LN['book_ps'], 'the book-value lens'), (LN['rel_ps'], 'the relative lens'),
          (LN['norm_ps'], 'the normalised-earnings lens'))
P(f'The readings disagree in an informative direction. The lowest is {_LO[1]} at EGP '
  f'{n2(_LO[0])}; the highest is {_HI[1]} at EGP {n2(_HI[0])}. The cash-flow readings charge '
  f'the new plant\'s full cost and credit it with nothing, so they sit low despite capturing '
  f'five years of the volume and price growth the existing business is already delivering. '
  f'The relative lens prices the company on what a {pc(LN["roe_sust"])} return and a '
  f'{pc(W["ke_term"], 1)} perpetual cost of equity can justify, which supports about '
  f'{n2(LN["just_fwd_pe"])} times forward earnings against the {n2(LN["pe_now"])} times '
  f'trailing the market pays. None of them is wrong. The gap between them is the value of '
  f'growth, and the market is paying for more of it than any of them contains.')

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
     f"capitalised in FY2025. The textbook consequence of the plant entering service is that "
     f"this becomes an expense. It has NOT happened yet — the first quarter of 2026 ran "
     f"financing expense DOWN {pc(abs(V['q1_fin'] * 4 / V['fin_fy25'] - 1))} year on year — and "
     f"this study charges the observed quarter, not the textbook. If the step does arrive it "
     f"is worth about EGP {n0(V['capint_cum_fy25'] - V['capint_cum_fy24'])} million a year of "
     f"pre-tax profit", 'FY2026 interim and full year'],
    ['The credit-loss and provision charge',
     f"the study's contested judgement. The disclosed charge runs "
     f"{pc(V['prov_fy23'] / V['rev_fy23'], 2)}, {pc(V['prov_fy24'] / V['rev_fy24'], 2)} and "
     f"{pc(V['prov_fy25'] / V['rev_fy25'], 2)} of revenue across the three audited years — a "
     f"three-year mean of {pc(SENS['prov_3yr_mean'], 2)} — and the first quarter of 2026 took "
     f"none at all. Which frame the next two years resemble is worth more than a point of "
     f"margin", 'each set of results'],
    ['The Saudi associate',
     f"note (33) attributes EGP {n0(ASSOC_SA_FY25)} million of associate income to this one "
     f"holding in FY2025 and EGP {n0(ASSOC_SA_FY24)} million in FY2024. The FY2024 figure "
     f"EXCEEDS the group associate line of EGP {n1(V['assoc_fy24'])} million for that year, so "
     f"the other holdings were a net drag of EGP {n1(ASSOC_SA_FY24 - V['assoc_fy24'])} million "
     f"— the individual disclosure and the group line are both reported here rather than one "
     f"being quoted without the other. This study normalises the WHOLE associate stream to EGP "
     f"{n0(V['assoc_norm'])} million against a three-year mean of EGP "
     f"{n1((V['assoc_fy23'] + V['assoc_fy24'] + V['assoc_fy25']) / 3)} million",
     'each set of results'],
    ['The active-ingredient project',
     'a separate USD 165 million company that this study does NOT consolidate and does NOT '
     'value. It reaches the accounts only through the associate line',
     'trial batches indicated for 2027'],
    ['The exchange rate',
     f"exports are 32% of revenue but hard-currency inputs are "
     f"{pc(CE['fx_cost_share_full_stack'], 1)} of the disclosed cost stack — the imported "
     f"active ingredient plus the imported SHARE of packaging, not the whole packaging line, "
     f"because the group makes its own primary packaging. So a weaker pound is a NET NEGATIVE "
     f"for this company, the opposite of the usual exporter reflex", 'continuous']]
table(rows, [1.75, 3.55, 1.6], size=8.4)
caption(f'Table {tnum()} — the events that would move this valuation, and the direction each cuts.')

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
bullet(f'the bands describe where the PRICE may go. The valuation describes what the '
       f'BUSINESS appears to be worth. They are different questions and this study keeps them '
       f'apart on purpose. BOTH fundamental centres — EGP {n2(LN["centre_A"])} and EGP '
       f'{n2(LN["centre_B"])} — sit below the entire three-month band, and that is worth '
       f'noticing rather than reconciling away.',
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
    ['THE SINGLE WEIGHTED CENTRE IS WITHDRAWN',
     'the first edition weighted Frame A and Frame B at a quarter each inside one number. '
     'Weighting both frames inside one number IS averaging them, which this study says five '
     'times that it never does. Each frame now carries the cash-flow weight in full, on its '
     'own, and TWO centres are published'],
    ['The terminal return on invested capital is now COMPUTED, not assumed',
     f"it was asserted at 20% against a forecast that reaches "
     f"{pc(A['roic_term'], 2)} in FY2030E. It now READS the model's own final year, so "
     f"terminal reinvestment rises from 25.0% to {pc(A['reinvest_rate'], 1)} of terminal "
     f"operating profit after tax"],
    ['The terminal year is charged the depreciation the forecast never charged',
     f"EGP {n0(FC['cip'][-1])} million of construction is still parked at FY2030E and had "
     f"never entered the depreciable base. A perpetuity cannot capitalise profit on capital it "
     f"never charges, so EGP {n0(A['term_dep_catchup'])} million a year is now deducted before "
     f"the terminal value is struck"],
    ['The terminal debt weight is now DERIVED and published on both bases',
     f"it was 20%, described as reconciled to the forecast balance sheet. It reconciled to "
     f"neither reading of that sheet: {pc(W['wd_term_market'], 1)} on today's market values, "
     f"{pc(W['wd_term_book'], 1)} on the funded forecast book. The market reading is used and "
     f"both are shown"],
    ['Free cash flow is taxed at the EFFECTIVE rate, not the statutory rate',
     f"the model conceded a {pc(W['tax_fcff'], 1)} effective burden in one place and applied "
     f"{pc(W['tax_stat'], 1)} in the cash-flow engine. One rate now runs both"],
    ['The forecast balance sheet is FUNDED and now balances',
     'cash and gross borrowings were frozen at their audited levels for five years while '
     'equity compounded, so the statement was out by up to 6.6% of total assets and no '
     'balance check was ever computed. Gross borrowings are now the funding plug, a total '
     'liabilities-and-equity row and a balance check have been added, and both are zero in '
     'every forecast column'],
    ['The trailing multiples are applied to TRAILING earnings',
     'two of the three legs of the relative lens were labelled trailing and applied to FY2026E '
     'earnings, which are BELOW trailing because of the depreciation step. Each leg now takes '
     'the earnings of its own period'],
    ['The peer anchor is relabelled a struck reference and moved to the midpoint',
     f"it was called a peer median at 19.5 times. Only two observations are disclosed, "
     f"{PEER_HI:.1f}x and {PEER_MID:.1f}x, whose midpoint is {V['peer_pe_regional']:.2f}x. It "
     f"is now that midpoint and it is not called a median"],
    ['The risk-free rate and the share price are struck on ONE date',
     'the yield carried a 21 July 2026 print against a 6 August 2026 share price. Both are now '
     '6 August, and the country-risk dataset moves to its mid-year vintage'],
    ['The sustainable return and the book lens are live in the workbook',
     'the book-value lens was a constant multiple typed inside a formula, so that lens did not '
     'move for any driver. Both the multiple and the return behind it now read the forecast'],
    ['The appendix income statement prints what the model computes',
     'its attributable-profit row printed retained earnings and its finance-cost row was a '
     'first-edition artefact. Both now come from the model rows the valuation uses'],
    ['NET EFFECT ON THE CENTRE',
     f"a single EGP 79.64 becomes a PAIR: EGP {n2(LN['centre_A'])} on Frame A "
     f"({pc(LN['centre_A'] / 79.64 - 1, 0)}) and EGP {n2(LN['centre_B'])} on Frame B "
     f"({pc(LN['centre_B'] / 79.64 - 1, 0)})"],
]
table(rows, [2.7, 4.2], band_rows={7, len(rows) - 1}, size=8.4)
caption(f'Table {tnum()} — every change from the first edition, and its direction.')

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
    ['The ten-year government yield is a market-data series, not an auction print',
     f'the discount rate now carries the {pc(V["rf"], 2)} level observable on the same date as '
     f'the share price, but the central bank\'s own auction page refused the request, so the '
     f'level is indicated rather than proven. The rate is sensitised over a wide range in '
     f'section 1.9',
     'a live read of the auction curve; a 200 basis-point error is worth about EGP 7 a share'],
    ['The enterprise-to-equity bridge mixes two consolidation perimeters',
     f'net debt is the audited 31 December 2025 figure, when the active-ingredient company was '
     f'still consolidated; the non-controlling interest deducted, EGP {n1(V["nci_bridge"])} '
     f'million, is the post-deconsolidation figure, and the retained stake is added separately '
     f'at cost. A single perimeter would either deduct the December minority of EGP '
     f'{n1(V["nci_fy25"])} million without the separate addition, or move the whole bridge to '
     f'the March balance sheet. The difference is about EGP '
     f'{n2((V["nci_fy25"] - V["nci_bridge"] + A["arab_api_cost"]) / SH)} a share on the '
     f'cash-flow readings',
     'a half-year balance sheet on one perimeter'],
    ['The forward interest path falls while the debt does not',
     f'the charge is calibrated to the first quarter of 2026 and is right for FY2026E, but it '
     f'declines to EGP {n0(V["int_path"][-1])} million by FY2030E on a funded borrowing book '
     f'that ends the window near where it started. The implied average rate falls to '
     f'{pc(FC["int_rate_implied"][-1], 2)} against a blended MARGINAL cost of debt of '
     f'{pc(W["kd_blend"], 2)} used in the discount rate. This affects the earnings-based '
     f'lenses, not the cash-flow ones, which are computed before interest',
     'a disclosed debt-amortisation schedule'],
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
    ['The beta composite contains the subject itself',
     f'the {BETAJ["composite_names"]}-name equal-weighted local composite the beta is '
     f'regressed against includes this company at about '
     f'{100 / BETAJ["composite_names"]:.1f}% weight, which biases the coefficient toward one. '
     f'Removing it gives {BETAJ["beta_ex_subject"]:.3f} rather than {BETAJ["beta"]:.3f}, which '
     f'would RAISE the two centres by about EGP '
     f'{(XBJ["beta_ex_subject_centre_A"] - LN["centre_A"]):,.2f} and EGP '
     f'{(XBJ["beta_ex_subject_centre_B"] - LN["centre_B"]):,.2f} a share. The in-index '
     f'coefficient is carried because it is the more conservative of the two and because it '
     f'is what a real local index produces; both are published in the bibliography',
     'a published local index that excludes the constituent under study'],
    ['The pre-2020 portion of the price history is thin',
     'the price export carries 162–195 sessions a year before 2020 against roughly 245 real '
     'exchange sessions. It affects only the longest calibration window, not the live bands, '
     'which are built on the post-2022 period',
     'a complete exchange-sourced price history']]
table(rows, [1.9, 3.35, 1.65], size=8.3)
caption(f'Table {tnum()} — every limitation this study knows about, and what would resolve it.')
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
isrow('Finance costs', 'finance', V['int_path'])
isrow('Share of associates', 'associates', [V['assoc_norm']] * 5)
rows.append(['Profit attributable to shareholders'] +
            [n0(H[y]['parent']) for y in ('FY2023', 'FY2024', 'FY2025')] +
            [n0(x) for x in FC['parent']])
rows.append(['Attributable earnings per share (EGP)',
             n2(V['parent_fy23'] / V['shares_fy23']),
             n2(V['parent_fy24'] / V['shares_fy23']),
             n2(V['parent_fy25'] / V['wavg_shares_fy25'])] +
            [n2(x) for x in FC['eps']])
rows.append(['   memorandum: retained after a '
             + pc(V['payout'], 0) + ' payout',
             n0(V['parent_fy23'] * (1 - V['payout'])),
             n0(V['parent_fy24'] * (1 - V['payout'])),
             n0(V['parent_fy25'] * (1 - V['payout']))] +
            [n0(x) for x in FC['retained']])
table(rows, [1.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72], band_rows={3, 9, 14},
      size=7.9)
caption(f'Table {tnum()} — three audited years and five forecast years. Every forecast line is the '
        f'model row the valuation itself uses. The attributable-profit line is attributable '
        f'profit; the retained portion is a separate memorandum line beneath it, because the '
        f'equity roll-forward in Appendix A.2 needs it. The finance-cost line is the charge '
        f'the model carries, calibrated to the first quarter of 2026 — it is not the marginal '
        f'cost of debt used in the discount rate, which is a different and higher forward '
        f'rate. Earnings per share for FY2023 and FY2024 use the '
        f'{n2(V["shares_fy23"])} million shares then in issue and FY2025 uses the audited '
        f'weighted average of {n2(V["wavg_shares_fy25"])} million; the forecast columns use '
        f'the {n2(SH)} million now in issue.')

H2('A.2 Balance sheet')
rows = [['EGP million', 'FY2023', 'FY2024', 'FY2025'] + YR]
bs = [('Property, plant and equipment', V['ppe_fy23'], V['ppe_fy24'], V['ppe_fy25'],
       FC['ppe']),
      ('Projects under construction', V['cip_fy23'], V['cip_fy24'], V['cip_fy25'], FC['cip']),
      ('Inventories', V['inv_fy23'], V['inv_fy24'], V['inv_fy25'], FC['inventory']),
      ('Trade receivables', V['ar_fy23'], V['ar_fy24'], V['ar_fy25'], FC['receivables']),
      ('Cash and bank balances', V['cash_fy23'], V['cash_fy24'], V['cash_fy25'], FC['cash']),
      ('Trade payables', V['ap_fy23'], V['ap_fy24'], V['ap_fy25'], FC['payables']),
      ('Gross borrowings (the funding plug)', V['debt_fy23'], V['debt_fy24'], W['gross_debt'],
       FC['debt']),
      ('Net debt', V['debt_fy23'] - V['cash_fy23'], V['debt_fy24'] - V['cash_fy24'],
       W['net_debt'], FC['net_debt']),
      ('Equity attributable to shareholders', V['equity_parent_fy23'],
       V['equity_parent_fy24'], V['equity_parent_fy25'], FC['equity'])]
for nm, a3, a4, a5, fwd in bs:
    rows.append([nm, n0(a3), n0(a4), n0(a5)] + [n0(x) for x in fwd])
rows.append(['Book value per share (EGP)',
             n2(V['equity_parent_fy23'] / V['shares_fy23']),
             n2(V['equity_parent_fy24'] / V['shares_fy23']),
             n2(LN['bv_ps'])] + [n2(x / SH) for x in FC['equity']])
table(rows, [1.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72], band_rows={10},
      size=7.9)
caption(f'Table {tnum()} — the balance sheet, WHICH BALANCES. The property and construction lines '
        f'roll forward on the transfer schedule and working capital is projected from the '
        f'disclosed day ratios; cash is held at the audited operating minimum and gross '
        f'borrowings carry whatever the asset side needs that trade credit, provisions and '
        f'equity do not supply. The first edition froze cash AND borrowings for five years '
        f'while equity compounded, which left the forecast columns out by up to 6.6% of total '
        f'assets with no check row to show it. Borrowings therefore RISE before they fall: the '
        f'working-capital build and the first year\'s capital spending are debt-funded while a '
        f'{pc(V["payout"], 0)} payout continues. The lines above are a summary; the full '
        f'statement, a total liabilities-and-equity row and an explicit balance-check row are '
        f'in the accompanying model, where the check reads zero in every forecast column and '
        f'carries residuals of −4.1, +0.2 and +0.4 million in the three audited columns — '
        f'under 0.05% of total assets, from grouping the filed statement into these captions.')

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
caption(f'Table {tnum()} — the asset-conversion cycle, projected rather than plugged. The 268-day '
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
    ['STRUCK REFERENCE USED — the midpoint of the two observations above',
     f"{V['peer_pe_regional']:.2f}x", 'trailing price / earnings',
     'the third leg of the relative lens, adjusted for the cost-of-equity gap. NOT a median '
     'of a disclosed peer set: only the two observations above are disclosed, the companies '
     'are not named, and this multiple therefore cannot be rebuilt from their filings'],
    ['EIPICO today, on shares in issue', f"{LN['pe_now']:.2f}x",
     'trailing price / earnings', 'computed from audited attributable profit and the market '
     'price'],
    ['EIPICO today, on the FY2025 weighted-average count', f"{LN['pe_now_wavg']:.2f}x",
     'trailing price / earnings',
     f"the same profit over the audited weighted average of {n2(V['wavg_shares_fy25'])} "
     f"million shares. Both readings are published"],
    ['EIPICO, own four-year mean', f"{LN['own_pe_mean']:.2f}x", 'trailing price / earnings',
     'computed entirely from primary material — the second leg of the relative lens']]
table(rows, [2.4, 0.8, 1.55, 2.15], size=8.4)
caption(f'Table {tnum()} — the peer set. No peer figure is used to build any historical number for '
        'EIPICO; peers appear only as a cross-check.')
H2('B.2 Risks')
rows = [['Risk', 'How it would show up', 'Severity']]
rows += [
    ['The new plant under-delivers', 'depreciation and interest charged with no revenue '
     'against them; reported profit falls for two to three years', 'High'],
    ['Administered price freeze', 'the domestic price-per-pack driver stops tracking '
     'inflation while imported input costs keep rising', 'High'],
    ['Currency depreciation',
     f"the imported active ingredient plus the imported SHARE of packaging are "
     f"{pc(CE['fx_cost_share_full_stack'], 1)} of the disclosed cost stack against a 32% "
     f"export share — a weaker pound is net negative here. Counting the WHOLE packaging line "
     f"as imported would give {pc(CE['fx_cost_share_full_stack_if_all_packaging'], 1)}, which "
     f"the group's own primary-packaging manufacture rules out", 'High'],
    ['Credit losses prove structural',
     f"the provision charge stays near {pc(V['prov_pct_permanent'], 2)} of revenue "
     f"permanently; this is Frame A, and it is already the more conservative of the two "
     f"published cases. A charge at the three-year mean of {pc(SENS['prov_3yr_mean'], 2)} "
     f"instead would put Frame A at EGP {n2(SENS['prov_readings'][1][2])} a share",
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
     'table as the honest response: the published grid across a plausible terminal cost of '
     f'equity and growth combination runs EGP {n0(SENS["grid_lo"])} to EGP '
     f'{n0(SENS["grid_hi"])} a share, and the WHOLE of that range is published rather than '
     f'its comfortable half.'],
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
P(f'Put together, the disagreement narrows to a single question, which is a good sign. All '
  f'three agree on the audited history, on the cost of capital construction, and on the fact '
  f'that the depreciation step is real and has already arrived. On the existing business — '
  f'65% capacity utilisation, a growing export book earned in hard currency, an administered '
  f'domestic price that at least tracks inflation — their own worked values run from EGP '
  f'{n2(min(A["per_share"], LN["book_ps"]))} to EGP '
  f'{n2(max(A["per_share"], LN["book_ps"]))} a share, and the study\'s own two centres, EGP '
  f'{n2(LN["centre_A"])} and EGP {n2(LN["centre_B"])}, sit inside that. Those are the numbers; '
  f'no wider claim is made for the business than its own lenses support.')
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
    ['Frame A centre less market price', n2(LN['centre_A'] - SPOT),
     'the sum of the above: no plant revenue, a relative lens anchored on what the company\'s '
     'own return justifies, and a normalised rather than peak margin'],
    ['Frame B centre less market price', n2(LN['centre_B'] - SPOT),
     'the same, with the provision charge normalising instead of permanent'],
    ['Frame A centre less Frame B centre', n2(LN['centre_A'] - LN['centre_B']),
     'the contested judgement alone, carried through the whole model. This is the number an '
     'average would have hidden']]
table(rows, [1.75, 1.05, 3.55], size=8.4)
caption(f'Table {tnum()} — every gap in this study isolated to the assumption that causes it.')

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
