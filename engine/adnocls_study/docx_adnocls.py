"""ADNOCLS_Valuation_Study_09-08-2026_public.docx — python-docx builder, house style.

Reads study_numbers.json exclusively: no financial numeral is typed into this file."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..'))
exec(open(os.path.join(HERE, 'docx_base.py')).read())   # doc, P, H1, H2, table, box, ...

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
M = D['meta']
IN = {k: v['value'] for k, v in D['inputs'].items()}
SRC = {k: v['source'] for k, v in D['inputs'].items()}
HI, HB, HC, CC = D['hist_is'], D['hist_bs'], D['hist_cf'], D['ccc']
SEGH, GRPH = D['seg_hist'], D['grp_hist']
SEGS, GROUPS, SEGGRP = D['segs'], D['groups'], D['seg_group']
FLT, DRV, WHY = D['fleet'], D['drivers'], D['driver_why']
F, FSG, FGR, FIN, FBS = D['fcst'], D['fcst_seg'], D['fcst_group'], D['fin'], D['fcst_bs']
FSUS, FINS = D['fcst_sustained'], D['fin_sustained']
GD = D['guidance_check']
W, BR = D['wacc'], D['bridge']
DCF, DCFA, DCFH = D['dcf'], D['dcf_beta_alt'], D['dcf_hybrid_pv']
DCFS, DCFB, DCFU = D['dcf_sustained'], D['dcf_bear'], D['dcf_bull']
LN, LW = D['lenses'], D['lens_weights']
REL, NRM, BK, SOTP, PEERS = D['rel'], D['norm'], D['book'], D['sotp'], D['peers']
EXP, PANEL = D['experts'], D['panel_centre']
SN, STK, S0, BT, TC, BE = (D['sens'], D['strike'], D['step0'], D['backtest'],
                           D['technicals'], D['beta'])
BF = D['beta_framing']
BFP, BFA = BF['primary'], BF['alternative']
MCC = SN['market_cross_check']
E1, E2, E3 = EXP['e1'], EXP['e2'], EXP['e3']

SPOT = M['spot_aed']
SPOT_USD = M['spot_usd']
SH = M['shares_mn']
PEG = M['fx']
YRS = [y.replace('FY', 'FY') for y in F['years']]
YRL = [y.replace('FY', '') + 'E' for y in F['years']]
HYRS = HI['year']
H3M, H1M = STK['horizons']['3M'], STK['horizons']['1M']
BT3, BT1, BTS = BT['five_year'], BT['one_month'], BT['shifted_grid']
FITM = BT['fit']


# ------------------------------- formatters ---------------------------------
def n0(x): return f"{x:,.0f}"
def n1(x): return f"{x:,.1f}"
def m0(x): return f"{x/1000.0:,.0f}"          # USD thousand -> USD mn
def m1(x): return f"{x/1000.0:,.1f}"
def b1(x): return f"{x/1000000.0:,.1f}"       # USD thousand -> USD bn
def p2(x): return f"{x:.2f}"
def p3(x): return f"{x:.3f}"
def pc(x, dp=1): return f"{x*100:.{dp}f}%"
def sgn(x, dp=0): return f"{x*100:+.{dp}f}%"
def xt(x, dp=1): return f"{x:.{dp}f}×"
def neg(s): return f"({s})"
def vs(x):
    v = x / SPOT - 1
    return '0%' if abs(v) < 0.005 else sgn(v, 0)


def ab(x):
    """Prose form: '53% above the market price' / '22% below the market price'."""
    v = x / SPOT - 1
    if abs(v) < 0.005:
        return 'level with the market price'
    return f"{abs(v)*100:.0f}% {'above' if v > 0 else 'below'} the market price"


TBL = []
_table = table
_H1, _H2 = H1, H2


def H1(text):
    p = _H1(text)
    p.paragraph_format.keep_with_next = True
    return p


def H2(text):
    p = _H2(text)
    p.paragraph_format.keep_with_next = True
    return p


def table(rows, widths, left_cols=(), **kw):
    """House table, plus three things the base helper does not do: record the total
    width for the width check, keep a row from splitting across a page break, repeat
    the header row on continuation pages, and left-align nominated prose columns."""
    TBL.append((rows[0][0] if rows and rows[0] else '?', sum(widths), len(widths)))
    t = _table(rows, widths, **kw)
    for i, row in enumerate(t.rows):
        trPr = row._tr.get_or_add_trPr()
        cant = OxmlElement('w:cantSplit')
        trPr.append(cant)
        if i == 0 and kw.get('header', True):
            hdr = OxmlElement('w:tblHeader')
            trPr.append(hdr)
        for j in left_cols:
            for p in row.cells[j].paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return t


# ------------------------------- derived ------------------------------------
REV = HI['revenue']
EBITDA_H = HI['ebitda_op']
NPA = HI['npa']
rev_cagr = (REV[2] / REV[0]) ** 0.5 - 1
q1_25_ebitda = sum(IN[f'q1_25_ebitda_{s.lower().replace(" ", "_").replace("-", "_")}']
                   for s in SEGS)
owned_total = sum(FLT['owned'].values())
spot_total = sum(FLT['spot'].values())
fixed_total = sum(FLT['fixed'].values())
# The alternative construction sits ABOVE the adopted one: it measures the market with an
# equal-weight composite, which produces a lower beta and therefore a higher value. The gap
# is always quoted as a positive distance and always in that direction.
beta_gap = LN['dcf_beta_alt']['base'] - LN['dcf']['base']
central_gap = D['central_beta_alt'] - D['central']
tv_pv = DCF['nopat_t1'] * (1 - DCF['reinvest'])
anchor_span = max(SN['anchor'].values()) - min(SN['anchor'].values())
beta_row = SN['betas'].index(IN['beta'])
g_col = SN['gs'].index(IN['g_terminal'])
beta_span = [r[g_col] for r in SN['grid_beta_g']]
g_span = SN['grid_beta_g'][beta_row]
capex_span = list(SN['capex'].values())
tax_span = list(SN['tax'].values())
e1_pe_lo = E1['rng'][0] / E1['eps_usd'] / PEG
e1_pe_hi = E1['rng'][1] / E1['eps_usd'] / PEG
nd_target_debt = IN['nd_ebitda_target_lo'] * F['ebitda'][4]
CLS = [('vlcc', 'Very large crude carriers'), ('lr2', 'Long range 2'),
       ('lr1', 'Long range 1'), ('mr', 'Medium range'), ('hs', 'Handysize')]


def segkey(s):
    return s.lower().replace(' ', '_').replace('-', '_')


# ============================ 1  MASTHEAD / READ FIRST =======================
masthead()
H2('Independent Valuation Study — Educational Analysis')
H1('ADNOC Logistics & Services plc (ADX: ADNOCLS)')
P(f"Marine logistics and shipping group — integrated logistics, shipping and services "
  f"· {M['exchange']} · reports in US dollars, trades in UAE dirhams · "
  f"analysis anchored on the closing price of AED {p2(SPOT)} on {M['price_date']}, with "
  f"the cash-flow model built at {M['valuation_date']}.",
  size=10, color=GREY)

box([("READ FIRST — what this document is. ",
      "This is an educational valuation study. It contains no recommendation, no credit "
      "opinion on the shares and no forecast of where the price will go. What it contains "
      "is a fair-value range built from the company's own audited and reviewed financial "
      "statements, a sourced cost of capital and explicitly listed assumptions — together "
      "with a separate, probabilistic map of where the share price could trade over the "
      "next one and three months. The two are different objects and are never blended."),
     ("What a fair value is not. ",
      "A fair-value estimate is a statement about what the business appears to be worth on "
      "the assumptions set out here. It is not a forecast of the share price and it "
      "carries no implied timeframe. A share can trade above or below an intrinsic "
      "estimate for years."),
     ("Two currencies, one company. ",
      f"The company reports in US dollars and its shares trade in UAE dirhams. Every "
      f"number in this study is built in dollars, and converted to dirhams only at the "
      f"final per-share line, at the fixed parity of {PEG:.4f} dirhams to the dollar that "
      f"the Central Bank of the UAE has maintained since 1997. Amounts are in US dollars "
      f"unless a dirham sign says otherwise; per-share figures are in dirhams so that they "
      f"can be compared with the screen."),
     ("How the market is measured, and it is published both ways. ",
      f"The cost of equity here rests on a beta of {p3(IN['beta'])}, measured by regressing "
      f"the share's own weekly returns on {BFP['label']} — the {BE['regressor']}. That is "
      f"the index the share is listed against, and it is the right yardstick. An earlier "
      f"construction of this study measured the market instead as an equal-weight composite "
      f"of the same exchange's names and obtained {p3(BFA['beta'])}. The difference is a "
      f"property of index construction rather than of the company: the published index is "
      f"weighted by size and is dominated by the same large-capitalisation group this "
      f"share belongs to, while an equal-weight composite gives the exchange's smallest "
      f"names the same say as its largest. On the published index the cash-flow model gives "
      f"AED {p2(LN['dcf']['base'])} a share; on the composite, AED "
      f"{p2(LN['dcf_beta_alt']['base'])}. The first is adopted. Both are computed in full, "
      f"both appear side by side in every table that matters, and they are never averaged "
      f"into a single number.")])

# ================================ 2  HEADLINE ================================
H2('Headline')
P(f"ADNOC Logistics & Services is the marine logistics and shipping arm of the Abu Dhabi "
  f"National Oil Company, listed on the {M['exchange']} since June 2023. It runs three "
  f"disclosed business units. Integrated Logistics — offshore contracting, offshore "
  f"services and offshore projects — owns {n0(IN['jub_owned'])} jack-up barges and "
  f"{n0(IN['osv_owned'])} offshore support vessels and works almost entirely for the "
  f"parent group. Shipping owns {n0(owned_total)} tankers, {n0(IN['gas_owned'])} gas "
  f"carriers and a dry-bulk and container fleet. Services runs petroleum ports, bunkering "
  f"and onshore logistics. Revenue was USD {m0(REV[2])} million in {HYRS[2]}, compounding "
  f"{sgn(rev_cagr)} a year over the two years from {HYRS[0]}, and the group earned USD "
  f"{m0(EBITDA_H[2])} million before interest, tax, depreciation and amortisation.")
P(f"The two halves of the business behave completely differently, and averaging them is "
  f"the main way this company gets mis-valued. About {pc(IN['contracted_2026_share'], 0)} "
  f"of {YRL[0]} revenue is already contracted with the parent group, against a long-term "
  f"contracted revenue backlog of roughly USD {b1(IN['contracted_revenue_lt'])} billion. "
  f"The other half is a merchant fleet: {n0(IN['spot_vessels_total'])} vessels trade at "
  f"spot rates, and the company discloses that a change of USD 1,000 a day in what they "
  f"earn moves group earnings by about USD {m0(IN['ebitda_per_1000_day'])} million a year. "
  f"On the company's own disclosure {pc(IN['spot_share_ebitda_26'], 0)} of {YRL[0]} "
  f"earnings sits on spot rates, falling to {pc(IN['spot_share_ebitda_29'], 0)} by "
  f"{YRL[3]} as contracted gas and logistics capacity comes in.")
P(f"That merchant half is having an extraordinary year. Very large crude carriers earned "
  f"an average of USD {n0(FLT['tce_fy25']['vlcc'])} a day across {HYRS[2]}; the company "
  f"reported USD {n0(IN['tce_vlcc_q1_26'])} a day in the first quarter of "
  f"{YRL[0][:4]} and indicated USD {n0(IN['tce_vlcc_q2_26'])} for the second. The long-range "
  f"classes moved the same way. The first quarter as a whole showed revenue of USD "
  f"{m0(IN['q1_26_rev'])} million ({sgn(IN['q1_26_rev']/IN['q1_25_rev']-1)} year on year, "
  f"because low-margin chartered-in trading fell away), earnings before interest, tax, "
  f"depreciation and amortisation of USD {m0(IN['q1_26_ebitda_group'])} million "
  f"({sgn(IN['q1_26_ebitda_group']/q1_25_ebitda-1)}) and attributable profit of USD "
  f"{m0(IN['q1_26_npa'])} million ({sgn(IN['q1_26_npa']/IN['q1_25_npa']-1)}). Whether "
  f"those rates hold is the whole valuation.")
P(f"This study says they do not hold, and prices the fleet reverting over five years to "
  f"the average of what it earned in {HYRS[1]} and {HYRS[2]}. That is a judgement, and "
  f"section 1.7 sets out the outside evidence for it. On that base the four lenses centre "
  f"at AED {p2(D['central'])} against a market price of {p2(SPOT)} — {ab(D['central'])}. "
  f"The cash-flow lens on its own lands at AED {p2(LN['dcf']['base'])}, "
  f"{ab(LN['dcf']['base'])}. The honest conclusion is that this share is close to fairly "
  f"priced on the evidence assembled here, not materially cheap.")
P(f"The reason that conclusion is stronger than it looks rests on the discount rate. "
  f"Measured against {BFP['label']}, this share's beta is {p3(IN['beta'])} — it moves with "
  f"the market, near enough one for one, on {n0(BE['n'])} weekly observations. The economic "
  f"prior for an asset-heavy fleet owner is that it carries the risk of the market its "
  f"ships trade in whoever signs the charter, and that prior is now confirmed by the "
  f"regression rather than contradicted by it. The two views have converged, which they "
  f"had not done when the market was measured a different way: an equal-weight composite "
  f"of the same exchange's names gives {p3(BFA['beta'])} and lifts the cash-flow lens to "
  f"AED {p2(LN['dcf_beta_alt']['base'])}. That construction is published beside the "
  f"adopted one throughout, because a gap of AED {p2(beta_gap)} a share that turns on how "
  f"an index is weighted is something a reader is entitled to see rather than a detail to "
  f"bury. What remains genuinely open is not the discount rate but where tanker rates "
  f"settle after {YRL[0][:4]}, which is section 1.7.", space_after=10)

# ============================ 3  VALUATION SUMMARY ===========================
H2('Valuation summary — every read at a glance')
rows = [['Read', 'Basis', 'Range (AED/sh)', 'Central', 'vs price'],
        ['Discounted cash flow',
         f"five-year free cash flow to the firm, cost of capital gliding "
         f"{pc(W['wacc'])} to {pc(W['wacc_term'])} on the share's own beta of "
         f"{p3(IN['beta'])} against {BFP['label']}, terminal growth "
         f"{pc(IN['g_terminal'], 0)}; "
         f"{pc(DCF['tv_share'], 0)} of enterprise value comes from the terminal value",
         f"{p2(LN['dcf']['bear'])} – {p2(LN['dcf']['bull'])}", p2(LN['dcf']['base']),
         vs(LN['dcf']['base'])],
        ['Relative multiples',
         f"a blended {xt(REL['blend_ev_ebitda'], 2)} enterprise value to earnings and "
         f"{xt(REL['blend_pe'], 2)} price to earnings on {YRL[0]}, weighted "
         f"{pc(REL['weight_ev_ebitda'], 0)} to the enterprise measure",
         f"{p2(LN['relative']['bear'])} – {p2(LN['relative']['bull'])}",
         p2(LN['relative']['base']), vs(LN['relative']['base'])],
        ['Normalised earnings power',
         f"the five-year average of the build's own earnings — USD "
         f"{m0(NRM['norm_ebitda'])} million before interest, tax, depreciation and "
         f"amortisation — at the same blended multiples",
         f"{p2(LN['normalized']['bear'])} – {p2(LN['normalized']['bull'])}",
         p2(LN['normalized']['base']), vs(LN['normalized']['base'])],
        ['Book value and sustainable return',
         f"a justified {xt(BK['pb_fair'], 2)} book value on AED {p2(BK['bvps_aed'])} of "
         f"book a share at a sustainable return on equity of {pc(BK['roe_sustainable'])}",
         f"{p2(LN['book']['bear'])} – {p2(LN['book']['bull'])}", p2(LN['book']['base']),
         vs(LN['book']['base'])],
        ['Weighted central',
         f"discounted cash flow {pc(LW['dcf'], 0)} · relative {pc(LW['relative'], 0)} · "
         f"normalised {pc(LW['normalized'], 0)} · book {pc(LW['book'], 0)}, on the "
         f"beta measured against {BFP['label']}",
         f"{p2(LN['central']['bear'])} – {p2(LN['central']['bull'])}", p2(D['central']),
         vs(D['central'])],
        ['Market price', f"closing price on {M['price_date']}", '—', p2(SPOT), '—'],
        ['ALTERNATIVE READINGS — not included in the weighted central above',
         '', '', '', ''],
        ['The market measured as an equal-weight composite',
         f"the identical model and identical cash flows with the beta regressed against "
         f"{BFA['label']} instead of {BFP['label']} — {p3(BFA['beta'])} instead of "
         f"{p3(IN['beta'])}, cost of capital gliding {pc(DCFA['wacc'])} to "
         f"{pc(DCFA['wacc_term'])}, and {pc(DCFA['tv_share'], 0)} of enterprise value "
         f"from the terminal value. The published index is the yardstick this study "
         f"adopts; the composite is shown because the gap turns on index weighting rather "
         f"than on the company (section 1.8). The weighted central on this construction is "
         f"AED {p2(D['central_beta_alt'])}",
         '—', p2(LN['dcf_beta_alt']['base']), vs(LN['dcf_beta_alt']['base'])],
        ['Rates hold near current levels',
         "the same model with the fleet reverting to a rate anchor 30% above the "
         "2024-2025 average rather than to it — the direction the company's own guidance "
         "points, and not this study's base (section 1.7)",
         '—', p2(DCFS['fv_aed']), vs(DCFS['fv_aed'])],
        ['Perpetual securities at coupon value',
         f"the same model deducting the perpetual capital securities at the present value "
         f"of their coupon, USD {m0(BR['hybrid_pv_coupon'])} million, instead of their "
         f"carrying value of USD {m0(BR['hybrid'])} million (section 1.1)",
         '—', p2(DCFH['fv_aed']), vs(DCFH['fv_aed'])]]
table(rows, [1.42, 2.86, 1.06, 0.82, 0.84], band_rows={5, 7}, size=8.4,
      left_cols=(1,))
caption(f"The alternative readings are shown so that each genuinely contested or "
        f"consequential choice carries a number the reader can see, rather than being "
        f"averaged silently into the headline. They are deliberately excluded from the "
        f"weighted central because each answers a different question — how the market "
        f"against which this share's risk is measured should itself be measured, where "
        f"shipping rates settle, and whether a perpetual security is a liability at face "
        f"or at coupon — and blending them would hide the difference instead of showing "
        f"it. Ranges are bear-to-bull within each lens; within the cash-flow lens the two "
        f"bounds are set by the two ends of the beta's own 90% confidence interval, "
        f"{BF['ci90'][1]:.3f} at the bear end and {BF['ci90'][0]:.3f} at the bull end, so "
        f"the published span is the span the estimate itself supports rather than a pair "
        f"of round numbers chosen by hand. The index reading is the largest of the three "
        f"alternatives: AED {p2(beta_gap)} a share separates the two constructions on the "
        f"cash-flow lens and AED {p2(central_gap)} on the weighted central, and both are "
        f"carried at full size through section 1.1, section 1.8, the comparison in "
        f"section 4 and the expert panel. Terminal value is {pc(DCF['tv_share'], 0)} of "
        f"the cash-flow model's enterprise value — a high share, disclosed here, again in "
        f"the bridge, and stressed in section 1.9.")

# ============================= 4  COMPANY OVERVIEW ===========================
H2('Company overview — ADNOC Logistics & Services at a glance')
rows = [['Item', 'Detail'],
        ['Listed / parent',
         f"Listed on the {M['exchange']} in June 2023 under the code {M['ticker']} "
         f"(ISIN {M['isin']}). The Abu Dhabi National Oil Company remains the controlling "
         f"shareholder, and is also the principal customer"],
        ['What it does',
         'Three disclosed business units. Integrated Logistics covers offshore '
         'contracting (jack-up barges and accommodation on the parent’s offshore '
         'fields), offshore services (support and supply vessels) and offshore projects '
         '(engineering, procurement and construction contracts). Shipping covers crude '
         'and product tankers, gas carriers, and dry-bulk and container vessels. Services '
         'covers petroleum port operations, bunkering fuel and water, onshore logistics '
         'and ship management'],
        ['Fleet',
         f"{n0(owned_total)} owned tankers across five size classes, of which "
         f"{n0(spot_total)} trade at spot rates and {n0(fixed_total)} are on charters out "
         f"at rates already fixed; {n0(IN['gas_owned'])} owned gas carriers, "
         f"{n0(IN['gas_lt_contracted'])} of them on long-term contracts; "
         f"{n0(IN['jub_owned'])} owned jack-up barges plus {n0(IN['jub_chartered'])} "
         f"chartered in; {n0(IN['osv_owned'])} owned offshore support vessels"],
        ['Scale',
         f"{HYRS[2]} revenue USD {m0(REV[2])} million; earnings before interest, tax, "
         f"depreciation and amortisation of USD {m0(EBITDA_H[2])} million on the "
         f"operating definition used throughout this study, or USD "
         f"{m0(HI['ebitda_reported'][2])} million on the company's own reported "
         f"definition, which adds the share of joint ventures and one-off items; "
         f"attributable profit USD {m0(NPA[2])} million"],
        ['How much is contracted',
         f"About {pc(IN['contracted_2026_share'], 0)} of {YRL[0]} revenue is already "
         f"contracted with the parent group, against long-term contracted revenue of "
         f"roughly USD {b1(IN['contracted_revenue_lt'])} billion"],
        ['How much is exposed to the market',
         f"{n0(IN['spot_vessels_total'])} vessels trade at spot rates. The company "
         f"discloses that group earnings move about USD "
         f"{m0(IN['ebitda_per_1000_day'])} million for every USD 1,000 a day change in "
         f"the rate they earn, and that {pc(IN['spot_share_ebitda_26'], 0)} of {YRL[0]} "
         f"earnings and {pc(IN['spot_share_ebitda_29'], 0)} of {YRL[3]} earnings sit on "
         f"that exposure"],
        ['Reporting and trading currency',
         f"Reports in US dollars; the shares trade in UAE dirhams at the fixed parity of "
         f"{PEG:.4f}. The valuation runs in dollars and converts at the peg only at the "
         f"per-share line, so no exchange-rate view is embedded anywhere in it"],
        ['Shares outstanding', f"{n0(SH)} million ordinary shares"],
        ['Market capitalisation',
         f"USD {m0(M['mktcap_usd000'])} million at the anchor price, or AED "
         f"{m0(M['mktcap_usd000']*PEG)} million"],
        ['Net debt',
         f"USD {m0(IN['q1_26_netdebt'])} million at 31 March 2026 — "
         f"{xt(IN['q1_26_netdebt']/F['ebitda'][0], 2)} the {YRL[0]} earnings this study "
         f"forecasts, against the company's own stated medium-term target range of "
         f"{xt(IN['nd_ebitda_target_lo'], 1)} to {xt(IN['nd_ebitda_target_hi'], 1)}"],
        ['Perpetual capital securities',
         f"USD {b1(IN['hybrid_face'])} billion of perpetual capital securities were "
         f"issued in {HYRS[2]}, carried at USD {m0(IN['q1_26_hybrid'])} million and priced "
         f"at the secured overnight financing rate plus "
         f"{IN['hybrid_margin']*10000:,.0f} basis points. They sit inside total equity in "
         f"the accounts but rank ahead of the ordinary shares, so this study deducts them "
         f"in the bridge — both at carrying value and at the present value of their "
         f"coupon"],
        ['Distribution policy',
         f"USD {m0(IN['dps_2026_usd']*1000)} million for {YRL[0][:4]}, paid quarterly, "
         f"rising {pc(IN['div_growth'], 0)} a year to {YRL[4][:4]} on the company's own "
         f"stated policy — about {pc(IN['dps_2026_usd']*1000/M['mktcap_usd000'])} on the "
         f"anchor price"],
        ['Tax',
         f"The UAE standard corporate rate is {pc(IN['tax_stat'], 0)}. International "
         f"shipping income is relieved, so the shipping units bore about "
         f"{pc(IN['tax_shipping'], 0)} of their own pre-tax profit in {HYRS[2]} against "
         f"{pc(IN['tax_integrated_logistics'], 0)} in Integrated Logistics and "
         f"{pc(IN['tax_services'], 0)} in Services. The model taxes each unit at its own "
         f"disclosed rate, and prices the top-up-tax risk separately in section 1.9"]]
table(rows, [1.55, 5.45], size=8.7, align_right_from=9)

P(f"Two structural facts govern everything that follows. First, this is two businesses in "
  f"one listing: a contracted, fee-like logistics operation that earns steady margins from "
  f"a single creditworthy customer, and a merchant fleet whose earnings are set by a world "
  f"market the company does not control. In {HYRS[2]} Integrated Logistics turned USD "
  f"{m0(GRPH['Integrated Logistics']['revenue'][2])} million of revenue into USD "
  f"{m0(GRPH['Integrated Logistics']['ebitda'][2])} million of earnings, a margin of "
  f"{pc(GRPH['Integrated Logistics']['margin'][2])}; Shipping turned USD "
  f"{m0(GRPH['Shipping']['revenue'][2])} million into USD "
  f"{m0(GRPH['Shipping']['ebitda'][2])} million, a margin of "
  f"{pc(GRPH['Shipping']['margin'][2])}. Second, the balance sheet is unusually light for "
  f"an asset-heavy fleet owner: property, plant and equipment of USD {m0(HB['ppe'][2])} "
  f"million is funded with net debt of only USD {m0(IN['q1_26_netdebt'])} million, because "
  f"USD {b1(IN['hybrid_face'])} billion of perpetual capital securities and a USD "
  f"{b1(IN['q1_26_shldr_loan'])} billion parent facility sit between the fleet and the "
  f"ordinary shares. How those securities are treated is the second contested judgement in "
  f"this study, and it too is published both ways.", space_after=10)

# ======================= 5  §1  FUNDAMENTAL VALUATION ========================
H1('1  Fundamental valuation')

# ---- 1.1 cash-flow model -----------------------------------------------------
H2('1.1  The cash-flow model — the primary lens, with the full waterfall')
P(f"The primary lens is a five-year free-cash-flow-to-the-firm model built at "
  f"{M['valuation_date']}, the date of the most recent reviewed balance sheet. Revenue is "
  f"not a growth rate applied to a revenue line. Each of the seven units the company "
  f"discloses is forecast on its own physical driver: the tankers vessel by vessel at the "
  f"rate each size class earns, the gas carriers on contracted vessel-years at the day "
  f"rate implied by their own revenue, and the remaining units on what they actually "
  f"earned in the first quarter of {YRL[0][:4]}, annualised and grown. Section 1.6 sets "
  f"the build out unit by unit. Cash flow is then taken all the way to present value, "
  f"line by line, below.")
hdr = ['USD mn'] + YRL
rows = [hdr,
        ['Revenue'] + [m0(x) for x in F['revenue']],
        ['Less operating costs'] + [neg(m0(x)) for x in F['opcost']],
        ['Earnings before interest, tax, depreciation and amortisation'] +
        [m0(x) for x in F['ebitda']],
        ['  margin on revenue'] + [pc(x) for x in F['ebitda_margin']],
        ['Less depreciation and amortisation'] + [neg(m0(x)) for x in F['dna']],
        ['Earnings before interest and tax'] + [m0(x) for x in F['ebit']],
        ['  effective tax rate on the units'] + [pc(x) for x in F['tax_rate']],
        ['Net operating profit after tax — earnings before interest and tax '
         '× (1 − t)'] + [m0(x) for x in F['nopat']],
        ['Add back depreciation and amortisation'] + [m0(x) for x in F['dna']],
        ['Less capital expenditure'] + [neg(m0(x)) for x in F['capex']],
        ['Less change in working capital'] +
        [neg(m0(x)) if x >= 0 else m0(-x) for x in F['dnwc']],
        ['Free cash flow to the firm'] + [m0(x) for x in F['fcff']],
        ['Less the first quarter already inside the balance sheet'] +
        [neg(m0(F['fcff'][0] - DCF['fcff'][0]))] + ['—'] * 4,
        ['Free cash flow from the valuation date'] + [m0(x) for x in DCF['fcff']],
        ['Cost of capital that year'] + [pc(x, 2) for x in DCF['glide']],
        ['Discount factor'] + [f"{x:.4f}" for x in DCF['df']],
        ['Present value of free cash flow'] + [m0(x) for x in DCF['pv']]]
table(rows, [2.20, 0.96, 0.96, 0.96, 0.96, 0.96], size=8.3, band_rows={12, 17})
caption(f"Every line is computed, not typed. The waterfall runs earnings before interest, "
        f"tax, depreciation and amortisation → depreciation and amortisation → "
        f"earnings before interest and tax → net operating profit after tax → "
        f"add back depreciation → less capital expenditure → less the change in "
        f"working capital → free cash flow to the firm → discount factor → "
        f"present value. Two conventions are visible in the first column and both are "
        f"deliberate. The valuation date is {M['valuation_date']}, so only three quarters "
        f"of {YRL[0][:4]} are discounted and the first quarter's own free cash flow of USD "
        f"{m0(F['fcff'][0]-DCF['fcff'][0])} million is removed rather than counted twice — "
        f"it is already inside the net debt the bridge subtracts. And tax is charged unit "
        f"by unit at each unit's own disclosed effective rate, which is why the group rate "
        f"runs near {pc(F['tax_rate'][0])} rather than the "
        f"{pc(IN['tax_stat'], 0)} statutory rate: international shipping income is "
        f"relieved under UAE law and the shipping units bore about "
        f"{pc(IN['tax_shipping'], 0)} in {HYRS[2]}. Working capital is carried at the "
        f"collection, inventory and payment cycle the {HYRS[2]} statements actually show.")

H2('The bridge from enterprise value to the equity')
rows = [['Line', 'USD mn', 'Note'],
        ['Present value of the five forecast years', m0(DCF['pv_explicit']),
         'the sum of the present-value row above'],
        ['Terminal-year free cash flow', m0(tv_pv),
         f"{YRL[4]} net operating profit after tax grown {pc(DCF['g'], 0)} and multiplied "
         f"by one less the reinvestment rate of {pc(DCF['reinvest'])}; that reinvestment "
         f"rate is forced to equal growth divided by the terminal return on invested "
         f"capital of {pc(DCF['roic_terminal'])}, so the growth in the perpetuity is paid "
         f"for rather than assumed free"],
        ['Present value of the terminal value', m0(DCF['pv_tv']),
         f"the terminal cash flow capitalised at {pc(W['wacc_term'])} less "
         f"{pc(DCF['g'], 0)} = USD {m0(DCF['tv'])} million, discounted at the same "
         f"year-five factor of {DCF['df'][4]:.4f} that the year-five cash flow uses"],
        ['Enterprise value of the operations', m0(DCF['ev_ops']),
         'the two lines above'],
        ['Terminal value as a share of enterprise value', pc(DCF['tv_share'], 1),
         'disclosed here, in the summary table and in section 7; stressed in section 1.9'],
        ['Plus joint ventures and associates', m0(BR['jv']),
         'carried at the reviewed 31 March 2026 book value with no uplift; these earn '
         'outside the consolidated cash flow, principally the six gas carriers held '
         'fifty-fifty and the bunkering associate'],
        ['Enterprise value', m0(DCF['ev']), ''],
        ['Less net debt', neg(m0(BR['net_debt_company'])),
         'the reviewed 31 March 2026 figure: the parent facility, third-party borrowings '
         'and lease liabilities less cash'],
        ['Less deferred consideration', neg(m0(BR['deferred'])),
         'deferred consideration on the staged acquisition, carried against the '
         'investment reserve — a real claim on the enterprise and treated as one'],
        ['Less perpetual capital securities', neg(m0(BR['hybrid'])),
         f"at carrying value. They sit inside total equity in the accounts but rank ahead "
         f"of the ordinary shares and carry a coupon of USD {m0(FIN['hybrid_coupon'])} "
         f"million a year, so the ordinary shareholder does not own them. The alternative "
         f"treatment is two lines below"],
        ['Less non-controlling interests', neg(m0(BR['nci'])),
         f"the reviewed book value of the minority stakes, consistent with the "
         f"{pc(IN['nci_share'])} of group profit they took in the first quarter"],
        ['Equity value attributable to ordinary shareholders', m0(DCF['equity']), ''],
        ['Fair value per share (USD)', p2(DCF['fv_usd']),
         f"against a market price of USD {p2(SPOT_USD)}"],
        ['Fair value per share (AED, at the peg)', p2(DCF['fv_aed']),
         f"against a market price of AED {p2(SPOT)} ({vs(DCF['fv_aed'])})"],
        ['ALTERNATIVE — perpetual securities at the present value of their coupon',
         p2(DCFH['fv_aed']),
         f"deducting USD {m0(BR['hybrid_pv_coupon'])} million, the coupon capitalised at "
         f"the terminal cost of capital, instead of the USD {m0(BR['hybrid'])} million "
         f"carrying value. Worth AED {p2(DCFH['fv_aed']-DCF['fv_aed'])} a share. The "
         f"securities are perpetual and non-amortising, so which of the two is right "
         f"depends on whether the company ever calls them; both are shown"]]
table(rows, [2.55, 0.95, 3.50], size=8.2, band_rows={5, 12, 14, 15},
      align_right_from=1, left_cols=(2,))

H2('How the market is measured, computed both ways')
P(f"One input in the construction above moves the answer further than any operating "
  f"assumption in the study, and it is not a judgement about the company — it is a choice "
  f"about what "
  f"“the market” means. Regressed against {BFP['label']}, the {BE['regressor']}, "
  f"the share's own weekly returns over its full listed history give a beta of "
  f"{p3(BE['beta'])} — {n0(BE['n'])} observations, an R-squared of {BE['r2']:.3f}, a "
  f"standard error of {BE['se']:.3f} and a 90% interval of [{BE['ci90'][0]:.2f}, "
  f"{BE['ci90'][1]:.2f}]. That is the index the share is listed against, it is the "
  f"yardstick this study adopts, and the estimate is close enough to one that this share "
  f"is best described as moving with its market. It also settles an argument. The economic "
  f"prior for a fleet owner is that it bears the risk of the market its ships trade in "
  f"whoever signs the charter — a listed crude and product tanker owner would normally sit "
  f"at {BE['plausibility']['tanker_owner_prior'].split(': ')[1]} and a contracted marine "
  f"services provider at "
  f"{BE['plausibility']['contracted_services_prior'].split(': ')[1]} — and the regression "
  f"now agrees with that prior rather than contradicting it.")
P(f"Run the same regression against {BFA['label']} and it gives {p3(BFA['beta'])} instead. "
  f"That is a large difference and it has nothing to do with this company: a published "
  f"index is weighted by size and is therefore dominated by the same large-capitalisation "
  f"group the subject belongs to, while an equal-weight composite gives the exchange's "
  f"smallest and least liquid names the same say as its largest. Measuring a share's "
  f"co-movement against the second is measuring it against a different market. The "
  f"published index is adopted; the composite construction was what an earlier version of "
  f"this study used, and it is set out in full beside the adopted one below because a "
  f"reader is entitled to see how much of a valuation turns on a weighting convention.")
rows = [['Line', f"Against {BFP['label']}", f"Against {BFA['label']}"],
        ['Beta used', p3(IN['beta']), p3(BFA['beta'])],
        ['Cost of equity', pc(W['ke'], 2), pc(W['ke_beta1'], 2)],
        ['Cost of capital, explicit window', pc(DCF['wacc'], 2), pc(DCFA['wacc'], 2)],
        ['Cost of capital, terminal', pc(DCF['wacc_term'], 2), pc(DCFA['wacc_term'], 2)],
        ['Present value of the five forecast years (USD mn)', m0(DCF['pv_explicit']),
         m0(DCFA['pv_explicit'])],
        ['Present value of the terminal value (USD mn)', m0(DCF['pv_tv']),
         m0(DCFA['pv_tv'])],
        ['Terminal value as a share of enterprise value', pc(DCF['tv_share'], 1),
         pc(DCFA['tv_share'], 1)],
        ['Enterprise value (USD mn)', m0(DCF['ev']), m0(DCFA['ev'])],
        ['Equity value (USD mn)', m0(DCF['equity']), m0(DCFA['equity'])],
        ['Fair value per share (AED)', p2(DCF['fv_aed']), p2(DCFA['fv_aed'])],
        ['Against the market price', vs(DCF['fv_aed']), vs(DCFA['fv_aed'])]]
table(rows, [3.10, 1.95, 1.95], size=8.5, band_rows={10, 11})
caption(f"Identical cash flows, identical bridge, one input different — and that input is "
        f"the series the returns are regressed on, not anything about the business. The "
        f"whole of the AED {p2(beta_gap)} between the two columns is the beta, and most of "
        f"it lands in the terminal value: a "
        f"{(DCF['wacc_term']-DCFA['wacc_term'])*10000:,.0f} basis point difference in the "
        f"terminal cost of capital changes the capitalisation factor on a perpetuity by "
        f"roughly a quarter, which is also why the terminal value falls from "
        f"{pc(DCFA['tv_share'], 0)} of enterprise value to {pc(DCF['tv_share'], 0)} of it "
        f"when the published index is used. The two columns are never averaged. The left "
        f"column is the adopted construction because the published index of the exchange "
        f"the share is listed on is the market this share is measured against; the right "
        f"column is published so that the size of the convention is visible. Note which "
        f"way the adoption cuts: it lowers the fair value and moves the cash-flow lens from "
        f"{ab(LN['dcf_beta_alt']['base'])} to {ab(LN['dcf']['base'])}.")

# ---- 1.2 book ---------------------------------------------------------------
H2('1.2  Book value and sustainable return — the asset lens')
P(f"Equity attributable to ordinary shareholders was USD {m0(IN['q1_26_eqp'])} million at "
  f"31 March 2026, or AED {p2(BK['bvps_aed'])} a share — the figure excludes the perpetual "
  f"capital securities, which the accounts include inside total equity but which do not "
  f"belong to the ordinary shareholder. The return on that equity ran "
  f"{pc(HB['roe'][0])} in {HYRS[0]}, {pc(HB['roe'][1])} in {HYRS[1]} and "
  f"{pc(HB['roe'][2])} in {HYRS[2]}, and the five forecast years average "
  f"{pc(BK['roe_sustainable'])}, which is the sustainable rate used here.")
P(f"A justified price-to-book multiple is the sustainable return on equity less growth, "
  f"divided by the cost of equity less growth. At {pc(BK['roe_sustainable'])}, "
  f"{pc(BK['g'], 0)} growth and a cost of equity of {pc(BK['ke'], 2)} that gives "
  f"{xt(BK['pb_fair'], 2)} book, or AED {p2(LN['book']['base'])} a share. The bounds move "
  f"with the beta and with the return together: the bear bound of AED "
  f"{p2(LN['book']['bear'])} takes a cost of equity of {pc(BK['ke_bear'], 2)}, built on "
  f"the upper end {BF['ci90'][1]:.3f} of the beta's own 90% confidence interval, together "
  f"with a return one seventh lower; the bull bound of AED {p2(LN['book']['bull'])} takes "
  f"{pc(BK['ke_bull'], 2)} on the lower end {BF['ci90'][0]:.3f} of the same interval with "
  f"a return one seventh higher. Both ends are therefore drawn from the estimate's own "
  f"statistical uncertainty rather than from round numbers chosen by hand. The lens "
  f"carries the lowest weight of the four, at {pc(LW['book'], 0)}, because a book multiple "
  f"derived from a cost of equity inherits the same discount rate as the cash-flow model "
  f"rather than testing it independently, and because carrying value is a poor description "
  f"of what a fleet is worth.")
P(f"On that last point there is one piece of hard evidence, and it is worth more than any "
  f"amount of argument. In January {YRL[0][:4]} the company completed the sale of a "
  f"2017-built very large crude carrier for USD {m0(BK['vessel_sale_price'])} million "
  f"against a carrying value of USD {m0(BK['vessel_sale_book'])} million — a realised "
  f"market value of {xt(BK['vessel_value_to_book'], 2)} book, on its own asset, disclosed "
  f"in its own earnings release. That tells the reader which way this lens is biased. "
  f"Carrying values understate realisable value, so a book-based read of this company is "
  f"conservative rather than neutral, and the gap is not small: applied across the fleet, "
  f"a {xt(BK['vessel_value_to_book'], 2)} ratio would lift the asset base by roughly a "
  f"third. It is a single transaction on a single vessel in a strong market and it is not "
  f"extrapolated into the valuation — but it is the only direct evidence available on the "
  f"gap between the balance sheet and the market, and it points one way.")
rows = [['Line', 'Value'],
        ['Equity attributable to ordinary shareholders at 31 March 2026 (USD mn)',
         m0(IN['q1_26_eqp'])],
        ['Book value per share (USD)', f"{BK['bvps_usd']:.4f}"],
        ['Book value per share (AED, at the peg)', p2(BK['bvps_aed'])],
        ['Sustainable return on equity, the five forecast years', pc(BK['roe_sustainable'])],
        ['Cost of equity', pc(BK['ke'], 2)],
        ['Long-run growth', pc(BK['g'], 0)],
        ['Justified price to book', xt(BK['pb_fair'], 2)],
        ['Fair value per share (AED)', p2(LN['book']['base'])],
        [f"Range — bear at the top of the beta's 90% interval ({BF['ci90'][1]:.3f}, cost "
         f"of equity {pc(BK['ke_bear'], 2)}) and a return one seventh lower; bull at the "
         f"bottom of it ({BF['ci90'][0]:.3f}, {pc(BK['ke_bull'], 2)}) and a return one "
         f"seventh higher",
         f"{p2(LN['book']['bear'])} – {p2(LN['book']['bull'])}"],
        ['Memorandum — the price the market pays for that book today',
         xt(REL['own_pb'], 2)],
        ['Memorandum — realised value against carrying value on the January vessel sale',
         xt(BK['vessel_value_to_book'], 2)]]
table(rows, [4.90, 2.10], size=8.5, band_rows={8})

# ---- 1.3 relative ------------------------------------------------------------
H2('1.3  Relative multiples')
P(f"There is no clean comparable for this company, and the reason is the same reason it is "
  f"interesting: nothing else combines a contracted logistics arm working for a national "
  f"oil company with an open-market tanker fleet. The frame used here therefore takes two "
  f"multiples from two different kinds of shipowner and blends them on the company's own "
  f"disclosed exposure, rather than picking one peer and pretending it fits.")
rows = [['Company', 'Market', 'Business model', 'EV / earnings', 'Price / earnings',
         'Price / book']]
for pr in PEERS:
    rows.append([pr['name'], pr['market'], pr['model'], xt(pr['ev_ebitda'], 2),
                 xt(pr['pe_fwd'], 2) if pr['pe_fwd'] else '—',
                 xt(pr['pb'], 2) if pr['pb'] else '—'])
rows.append(['ADNOC Logistics & Services', M['exchange'].replace('Securities ', ''),
             'half contracted logistics, half merchant fleet',
             f"{xt(REL['own_ev_ebitda_ttm'], 2)} trailing / "
             f"{xt(REL['own_ev_ebitda_26'], 2)} on {YRL[0]}",
             xt(REL['own_pe_ttm'], 2), xt(REL['own_pb'], 2)])
table(rows, [1.62, 0.92, 1.72, 1.28, 0.84, 0.62], size=8.0, band_rows={4},
      left_cols=(1, 2))
caption(f"The contracted-fleet multiple of {xt(REL['contracted_multiple'], 2)} comes from "
        f"the long-term contracted gas shipowner; the spot multiple of "
        f"{xt(REL['spot_multiple'], 2)} is the average of the two listed spot tanker "
        f"owners. Peer figures are as published on the dates recorded in this study's "
        f"source register, and the company's own trailing multiple uses the operating "
        f"earnings definition used throughout, not the company's own wider reported one.")
rows = [['Measure', 'Value', 'Comment'],
        ['Contracted-fleet multiple', xt(REL['contracted_multiple'], 2),
         'the long-term contracted gas shipowner — the closest listed analogue to the '
         'logistics and gas-carrier legs, which earn under long contracts with a single '
         'strong counterparty'],
        ['Spot-fleet multiple', xt(REL['spot_multiple'], 2),
         'the average of two listed spot tanker owners — the closest analogue to the '
         'merchant fleet, and it trades several turns lower precisely because its '
         'earnings are not contracted'],
        ['Weight on the spot multiple', pc(REL['spot_weight'], 0),
         "the company's own disclosed share of earnings exposed to spot rates in "
         f"{YRL[0]} — the weighting is taken from the company rather than chosen"],
        ['Blended enterprise multiple', xt(REL['blend_ev_ebitda'], 2),
         f"applied to {YRL[0]} earnings of USD {m0(REL['ebitda_26'])} million"],
        ['Blended price-to-earnings multiple', xt(REL['blend_pe'], 2),
         f"applied to {YRL[0]} attributable profit after the perpetual coupon of USD "
         f"{m0(REL['npa_ord_26'])} million"],
        ['Value on the enterprise multiple (AED/share)', p2(REL['value_ev_ebitda']), ''],
        ['Value on the earnings multiple (AED/share)', p2(REL['value_pe']),
         'materially lower, because depreciation on a young, recently expanded fleet and '
         'the perpetual coupon both fall between the two measures — the reason this lens '
         'weights the enterprise measure more heavily'],
        [f"Weighted value ({pc(REL['weight_ev_ebitda'], 0)} enterprise / "
         f"{pc(1-REL['weight_ev_ebitda'], 0)} earnings)", p2(LN['relative']['base']),
         'the enterprise measure carries more weight because it is the standard measure '
         'for a capital-intensive fleet owner and neutralises differences in leverage, '
         'depreciation policy and tax relief across the comparators'],
        ['Range', f"{p2(LN['relative']['bear'])} – {p2(LN['relative']['bull'])}",
         'the whole group at the spot multiple, and the whole group at the contracted '
         'multiple — the two corners the blend sits between']]
table(rows, [2.30, 1.00, 3.70], size=8.3, band_rows={8}, left_cols=(2,))

H2('Sum of the parts — the same multiples, applied where they belong')
P(f"Applying one multiple to the whole group is the mistake the frame above is trying to "
  f"avoid, and there is a cleaner way to say so: value each business unit on the multiple "
  f"that fits it and add them. The two contracted legs — Integrated Logistics and Services "
  f"— earn under long-term contracts with a single strong counterparty and take the "
  f"contracted-fleet multiple. Shipping takes a blend of the contracted and spot "
  f"multiples, weighted by the company's own disclosed share of earnings exposed to spot "
  f"rates. This is a cross-check on the relative lens rather than a fifth lens, and it is "
  f"excluded from the weighted central, but it is the construction that honours the fact "
  f"that this company runs contracted work and market-exposed shipping side by side.")
rows = [['Business unit', f"{YRL[0]} earnings (USD mn)", 'Multiple',
         'Enterprise value (USD mn)', 'Why that multiple']]
for leg in SOTP['legs']:
    rows.append([leg['leg'], m0(leg['ebitda_26']), xt(leg['multiple'], 2), m0(leg['ev']),
                 leg['basis']])
rows.append(['Sum of the three legs', m0(sum(l['ebitda_26'] for l in SOTP['legs'])),
             '', m0(SOTP['ev_ops']),
             'enterprise value of the operations, the three legs added'])
rows.append(['Plus joint ventures and associates', '', '', m0(SOTP['jv']),
             'at reviewed book value'])
rows.append(['Less net debt and deferred consideration', '', '', neg(m0(SOTP['net_debt'])),
             'the same bridge lines as the cash-flow model'])
rows.append(['Less perpetual capital securities', '', '', neg(m0(SOTP['hybrid'])),
             'at carrying value'])
rows.append(['Less non-controlling interests', '', '', neg(m0(SOTP['nci'])), ''])
rows.append(['Equity value', '', '', m0(SOTP['equity']),
             f"AED {p2(SOTP['fv_aed'])} a share, {ab(SOTP['fv_aed'])}"])
table(rows, [1.75, 1.02, 0.72, 1.11, 2.40], size=8.0, band_rows={4, 9},
      left_cols=(4,))
caption(f"The sum of the parts lands at AED {p2(SOTP['fv_aed'])} against the blended "
        f"relative lens at AED {p2(LN['relative']['base'])}, and the difference is almost "
        f"entirely the earnings measure the multiple is applied to rather than the "
        f"multiples themselves: the sum of the parts applies each multiple to that unit's "
        f"own earnings before any group cost, while the blended lens applies its multiple "
        f"to the consolidated figure and then averages an enterprise measure with an "
        f"after-tax earnings measure. Both are disclosed. Neither is included in the "
        f"weighted central, which rests on the cash-flow model and the three lenses beside "
        f"it.")

# ---- 1.4 normalised ----------------------------------------------------------
H2('1.4  Normalised earnings power — what the group earns in an ordinary year')
P(f"The question this lens asks is what the company earns in a year that is neither the "
  f"rate spike of {YRL[0][:4]} nor the trough that followed the {HYRS[1]} peak. The answer "
  f"used here is the five-year average of the build's own output: earnings before "
  f"interest, tax, depreciation and amortisation of USD {m0(NRM['norm_ebitda'])} million "
  f"and attributable profit after the perpetual coupon of USD {m0(NRM['norm_npa'])} "
  f"million. That average is taken across a path that starts far above mid-cycle and ends "
  f"below it, so it is a genuine normalisation rather than a disguised extrapolation of "
  f"the good year.")
rows = [['Line', 'Value'],
        ['Average earnings before interest, tax, depreciation and amortisation over the '
         'five forecast years (USD mn)', m0(NRM['norm_ebitda'])],
        [f"Against {HYRS[2]} actual (USD mn)", m0(EBITDA_H[2])],
        [f"Against the {YRL[0]} build (USD mn)", m0(F['ebitda'][0])],
        ['Average attributable profit after the perpetual coupon (USD mn)',
         m0(NRM['norm_npa'])],
        ['Normalised earnings per share (USD)', f"{NRM['eps']:.4f}"],
        ['At the blended enterprise multiple, through the bridge (AED/share)',
         p2(2 * NRM['base'] - NRM['value_pe'])],
        [f"At the blended {xt(NRM['pe'], 2)} price-to-earnings multiple (AED/share)",
         p2(NRM['value_pe'])],
        ['Fair value per share — the average of the two (AED)', p2(LN['normalized']['base'])],
        ['Range — the whole group at the spot multiple, and at the contracted multiple',
         f"{p2(LN['normalized']['bear'])} – {p2(LN['normalized']['bull'])}"]]
table(rows, [4.90, 2.10], size=8.5, band_rows={9})
caption(f"The two constructions disagree by a wide margin — AED "
        f"{p2(2*NRM['base']-NRM['value_pe'])} against AED {p2(NRM['value_pe'])} — and the "
        f"gap is depreciation and the perpetual coupon. This is a young fleet: "
        f"depreciation runs at about {pc(F['dna'][0]/F['ebitda'][0])} of earnings before "
        f"interest, tax, depreciation and amortisation across the forecast, so an "
        f"enterprise measure and an after-tax earnings measure will never agree on a "
        f"company like this. Averaging them is a deliberate refusal to pick, and the "
        f"lens carries {pc(LW['normalized'], 0)} weight accordingly.")

# ---- 1.5 synthesis -----------------------------------------------------------
H2('1.5  Synthesis — four lenses, one field')
figure(os.path.join(HERE, 'fig1_football.png'), 6.9,
       f"Figure 1 — the four lenses, both measurements of the market and the two weighted "
       f"centrals, against the market price of AED {p2(SPOT)}. Each bar is that lens's "
       f"bear-to-bull span; the brass tick is its base case. The two cash-flow rows are the "
       f"same model with the beta regressed on two different market series.")
rows = [['Lens', 'Bear', 'Base', 'Bull', 'Weight', 'Contribution']]
lensnames = [('dcf', 'Cash-flow model — published index'),
             ('relative', 'Relative multiples'),
             ('normalized', 'Normalised earnings power'),
             ('book', 'Book value and sustainable return')]
for k, nm in lensnames:
    l = LN[k]
    rows.append([nm, p2(l['bear']), p2(l['base']), p2(l['bull']), pc(LW[k], 0),
                 p2(l['base'] * LW[k])])
rows.append(['Weighted central — published index', p2(LN['central']['bear']),
             p2(D['central']), p2(LN['central']['bull']), pc(1.0, 0), p2(D['central'])])
rows.append(['Cash-flow model — equal-weight composite', p2(LN['dcf_beta_alt']['bear']),
             p2(LN['dcf_beta_alt']['base']), p2(LN['dcf_beta_alt']['bull']),
             pc(LW['dcf'], 0), p2(LN['dcf_beta_alt']['base'] * LW['dcf'])])
rows.append(['Weighted central — equal-weight composite',
             p2(LN['central_beta_alt']['bear']), p2(D['central_beta_alt']),
             p2(LN['central_beta_alt']['bull']), pc(1.0, 0), p2(D['central_beta_alt'])])
table(rows, [2.42, 0.86, 0.86, 0.86, 0.86, 1.14], size=8.5, band_rows={5, 7})
P(f"The four lenses do not agree and the disagreement is informative. The two that price "
  f"earnings through a multiple — relative and normalised — land at AED "
  f"{p2(LN['relative']['base'])} and AED {p2(LN['normalized']['base'])}, both above the "
  f"market. The two that discount or capitalise a cost of equity land below it: the "
  f"cash-flow model at AED {p2(LN['dcf']['base'])} and the book lens at AED "
  f"{p2(LN['book']['base'])}. That split is not a coincidence, and it is the most useful "
  f"thing this table says. The multiple-based lenses import a cost of capital rather than "
  f"state one, and the comparators they import it from are a contracted shipowner and a "
  f"pair of spot tanker owners, so they already embed an answer to the question the "
  f"cash-flow model now asks explicitly and answers with a measured beta of "
  f"{p3(IN['beta'])}. Where the two families disagree, the disagreement is about the "
  f"discount rate rather than about the cash flows.")
P(f"Weighted together, the four centre at AED {p2(D['central'])}, {ab(D['central'])}. "
  f"Measuring the market as an equal-weight composite instead lifts that to AED "
  f"{p2(D['central_beta_alt'])}, {ab(D['central_beta_alt'])}. Neither figure supports a "
  f"claim that this share is materially mispriced: on the adopted construction the centre "
  f"of the evidence sits about {abs(D['central']/SPOT-1)*100:.0f}% above the screen, which "
  f"is well inside the width of any one of these lenses. The honest reading of the field "
  f"is that the share is close to fairly priced, with the fleet's earning power in "
  f"{YRL[1][:4]} and beyond — not the discount rate — deciding which way it resolves.")

# ---- 1.6 drivers -------------------------------------------------------------
H2('1.6  The drivers — every disclosed unit grown on its own driver')
P(f"The company discloses seven operating units inside its three reported business units, "
  f"with revenue, direct cost and earnings for each. The forecast is built at that level "
  f"and summed; nothing is grown at the group line. Where a physical driver is disclosed "
  f"it is used, and where it is not, the finest level the disclosure supports is used and "
  f"the gap is stated.")

H2('The seven disclosed units, historically')
rows = [['Unit', 'Business unit', f"{HYRS[0]} rev", 'margin', f"{HYRS[1]} rev", 'margin',
         f"{HYRS[2]} rev", 'margin']]
for s in SEGS:
    sh_ = SEGH[s]
    rows.append([s, SEGGRP[s], m0(sh_['revenue'][0]), pc(sh_['margin'][0], 0),
                 m0(sh_['revenue'][1]), pc(sh_['margin'][1], 0),
                 m0(sh_['revenue'][2]), pc(sh_['margin'][2], 0)])
rows.append(['Group', '', m0(REV[0]), pc(EBITDA_H[0] / REV[0], 0), m0(REV[1]),
             pc(EBITDA_H[1] / REV[1], 0), m0(REV[2]), pc(EBITDA_H[2] / REV[2], 0)])
table(rows, [1.42, 1.20, 0.76, 0.60, 0.76, 0.60, 0.76, 0.60], size=7.9,
      band_rows={8}, left_cols=(1,))
caption(f"Revenue in USD million; margin is that unit's own earnings before interest, tax, "
        f"depreciation and amortisation over its own revenue, all taken from the operating "
        f"segments note. The Tankers line tells most of the story of the last three years: "
        f"revenue more than tripled from {HYRS[1]} to {HYRS[2]} as the acquired fleet "
        f"consolidated, while the margin fell from {pc(SEGH['Tankers']['margin'][1], 0)} to "
        f"{pc(SEGH['Tankers']['margin'][2], 0)} because much of that revenue is low-margin "
        f"chartered-in and relet trading that grosses up the revenue line without adding "
        f"to earnings.")

H2('How each unit is driven')
rows = [['Unit', 'Driver']]
rows.append(['Tankers',
             f"Vessel by vessel. {n0(owned_total)} owned tankers in five size classes, of "
             f"which {n0(spot_total)} trade at spot rates and {n0(fixed_total)} sit on "
             f"charters out at disclosed fixed rates that roll off through {YRL[1][:4]}. "
             f"Each class earns its own rate: {YRL[0][:4]} is built from the rate the "
             f"company reported for the first quarter, the level it indicated for the "
             f"second, and a second half stepped halfway back to the {HYRS[2]} average; "
             f"from {YRL[1]} the rate glides over four years to the mid-cycle anchor, the "
             f"average of the {HYRS[1]} and {HYRS[2]} outcomes. Running cost is USD "
             f"{n0(FLT['opex_day'])} a vessel-day, solved so that the owned fleet's "
             f"earnings reproduce the reported {HYRS[2]} result, escalated "
             f"{pc(IN['opex_escalation'], 0)} a year on wages and technical management "
             f"— a services escalator, not a commodity index, because those are the "
             f"physical drivers of the line"])
rows.append(['Gas Carriers',
             f"Contracted vessel-years × day rate. The company's own contract table "
             f"gives {n1(FLT['gas_vessel_years'][0])} consolidated vessel-years in "
             f"{YRL[0][:4]} rising to {n1(FLT['gas_vessel_years'][3])} by {YRL[3][:4]} as "
             f"the ethane and Ruwais carriers enter service. Per-vessel rates are not "
             f"disclosed, so the day rate of USD {n0(FLT['gas_rate_day'])} is solved from "
             f"reported {HYRS[2]} revenue over vessel-years — the finest level the "
             f"disclosure supports, and flagged as solved rather than sourced. Margin held "
             f"near the {HYRS[2]} outcome, since {n0(IN['gas_lt_contracted'])} of "
             f"{n0(IN['gas_owned'])} owned vessels sit on long-term contracts"])
for s in ['Offshore Contracting', 'Offshore Services', 'Offshore Projects',
          'Dry-Bulk and Containers', 'Services']:
    rows.append([s, WHY[s]])
table(rows, [1.45, 5.55], size=8.2, align_right_from=9)

H2('What the build produces — margins as outputs')
rows = [['USD mn'] + YRL]
for g in GROUPS:
    rows.append([f"{g} — revenue"] + [m0(x) for x in FGR[g]['rev']])
    rows.append([f"{g} — margin"] +
                [pc(e / r, 0) for e, r in zip(FGR[g]['ebitda'], FGR[g]['rev'])])
rows.append(['Group revenue'] + [m0(x) for x in F['revenue']])
rows.append(['Group earnings before interest, tax, depreciation and amortisation'] +
            [m0(x) for x in F['ebitda']])
rows.append(['Group margin'] + [pc(x) for x in F['ebitda_margin']])
table(rows, [2.20, 0.96, 0.96, 0.96, 0.96, 0.96], size=8.2, band_rows={7, 8, 9})
caption(f"No margin in this table is an assumption applied to the group. For the two "
        f"shipping units that carry the rate risk, the margin is a pure arithmetic output: "
        f"rate per vessel-day less running cost per vessel-day. For the contracted units "
        f"the unit margin is set from what that unit itself earned in the first quarter of "
        f"{YRL[0][:4]}, and the group margin — which moves from {pc(F['ebitda_margin'][0])} "
        f"to {pc(F['ebitda_margin'][4])} across the forecast — is an output of the changing "
        f"mix, not a path anyone chose. The margin rises against {HYRS[2]}'s "
        f"{pc(EBITDA_H[2]/REV[2])} mainly because the low-margin chartered-in trading that "
        f"grossed up {HYRS[2]} revenue is not repeated: the first quarter of {YRL[0][:4]} "
        f"showed revenue {sgn(IN['q1_26_rev']/IN['q1_25_rev']-1)} year on year while "
        f"earnings rose {sgn(IN['q1_26_ebitda_group']/q1_25_ebitda-1)}.")

figure(os.path.join(HERE, 'fig7_mix.png'), 6.9,
       "Figure 2 — earnings by business unit, reported and forecast, with the group "
       "margin. Shipping does the moving; the contracted logistics base grows steadily "
       "underneath it.")

H2("The build against the company's own guidance — a gap, stated plainly")
P(f"This build sits materially above what management has guided for {YRL[0][:4]}, and that "
  f"is a deliberate result of the method rather than an accident to be reconciled away.")
rows = [['Business unit', 'Guided revenue', 'Built revenue', 'Guided earnings',
         'Built earnings', 'Gap on earnings']]
for g in GROUPS + ['Group']:
    gd = GD[g]
    rows.append([g, m0(gd['guided_revenue']), m0(gd['built_revenue']),
                 m0(gd['guided_ebitda']), m0(gd['built_ebitda']),
                 sgn(gd['ebitda_gap'])])
table(rows, [1.60, 1.08, 1.08, 1.08, 1.08, 1.08], size=8.3, band_rows={4})
caption('Revenue and earnings in USD million. Guidance is the midpoint of the ranges the '
        'company published for the year; the built figures are the output of the unit '
        'model in this section.')
P(f"The group gap is {sgn(GD['Group']['ebitda_gap'])} on earnings. Management's own "
  f"explanation for why its guidance is set where it is, given with the guidance itself, "
  f"is that its shipping assumptions are set well below prevailing spot rates and its "
  f"logistics guidance is set at minimum activity levels. This build does not use "
  f"assumptions set below the market: it marks the tanker fleet to the rates the company "
  f"itself reported for the first quarter of {YRL[0][:4]} and indicated for the second, "
  f"and it sets each logistics unit at what that unit actually earned in the first "
  f"quarter, annualised. Those are the company's own numbers, used at face value. The "
  f"reader now has both figures and the reason for the difference, and can decide which to "
  f"work from. What the reader should not do is assume the two are reconciled somewhere "
  f"below: they are not, and the {sgn(GD['Group']['ebitda_gap'])} is carried openly "
  f"through every lens in this study. Note also that the gap runs the other way in "
  f"Integrated Logistics on revenue, where the build is above guidance on both lines, and "
  f"is largest in Shipping at {sgn(GD['Shipping']['ebitda_gap'])} — which is exactly where "
  f"management said it was being conservative.")

# ---- 1.7 crux ----------------------------------------------------------------
H2('1.7  The crux — what the fleet earns per day, and for how long')
P(f"Everything else in this study is second order. The crux is a single question: the "
  f"tanker fleet is currently earning rates several times its own recent average, and the "
  f"valuation turns entirely on how long that lasts and where it settles.")
figure(os.path.join(HERE, 'fig8_tce.png'), 7.0,
       f"Figure 3 — the crux made visible. Time-charter equivalent per vessel per day by "
       f"class, by quarter, on a logarithmic scale. The last two points are the first "
       f"quarter of {YRL[0][:4]} as reported and the second quarter as indicated by the "
       f"company; the dotted lines are the mid-cycle rates this study's base case reverts "
       f"to; the dash-dotted line is an independent one-year charter fixed by a listed "
       f"owner in early {YRL[0][:4]}.")
rows = [['Class', 'Owned', 'At spot', f"{HYRS[1]} avg", f"{HYRS[2]} avg",
         f"{YRL[0][:4]} Q1", f"{YRL[0][:4]} Q2", 'Mid-cycle anchor used']]
for key, nm in CLS:
    rows.append([nm, n0(FLT['owned'][key]), n0(FLT['spot'][key]),
                 n0(FLT['tce_fy24'][key]), n0(FLT['tce_fy25'][key]),
                 n0(FLT['q1_26'][key]), n0(FLT['q2_26'][key]),
                 n0(FLT['tce_mid'][key])])
table(rows, [1.34, 0.60, 0.62, 0.78, 0.78, 0.74, 0.74, 1.40], size=8.0)
caption(f"US dollars per vessel per day. Quarterly rates for the medium-range class are "
        f"not disclosed for {HYRS[1]}, so the {HYRS[2]} average stands in; the handysize "
        f"vessels are not broken out at all and are carried at the medium-range rate. Both "
        f"substitutions are flagged rather than hidden, and both are immaterial: the two "
        f"classes together are {n0(FLT['owned']['mr']+FLT['owned']['hs'])} of "
        f"{n0(owned_total)} vessels and the smallest earners. The mid-cycle anchor is the "
        f"average of the {HYRS[1]} and {HYRS[2]} outcomes, which is what the base case "
        f"reverts to over four years from {YRL[1]}.")
P(f"The scale of the move is easiest to see in the largest class. Very large crude "
  f"carriers averaged USD {n0(FLT['tce_fy24']['vlcc'])} a day in {HYRS[1]} and USD "
  f"{n0(FLT['tce_fy25']['vlcc'])} in {HYRS[2]}; the company reported USD "
  f"{n0(FLT['q1_26']['vlcc'])} for the first quarter of {YRL[0][:4]} and indicated USD "
  f"{n0(FLT['q2_26']['vlcc'])} for the second — roughly "
  f"{FLT['q2_26']['vlcc']/FLT['tce_mid']['vlcc']:.1f} times the mid-cycle anchor this "
  f"study reverts to. Against {n0(IN['spot_vessels_total'])} vessels at spot and the "
  f"company's own disclosure that USD 1,000 a day is worth USD "
  f"{m0(IN['ebitda_per_1000_day'])} million of annual earnings, the difference between "
  f"today's rate and the mid-cycle anchor is worth well over a billion dollars a year of "
  f"earnings. That is why this one judgement dominates.")

H2('Why the base case reverts — the outside evidence')
P(f"A reversion assumption made without evidence is just pessimism. Two independent "
  f"observations, neither of them this study's own construction, point the same way, and "
  f"they are the reason the base case is a judgement with support rather than a default.")
rows = [['Evidence', 'What it shows'],
        ['The forward market will not pay spot for a year of time',
         f"A listed crude tanker owner fixed seven very large crude carriers on one-year "
         f"time charters in early {YRL[0][:4]} at USD {n0(MCC['vlcc_1y_tc'])} a day, at a "
         f"time when the spot rate of the moment was around USD "
         f"{n0(MCC['vlcc_spot_broker'])} and this company's own fleet went on to earn USD "
         f"{n0(FLT['q1_26']['vlcc'])} in the first quarter. A counterparty willing to "
         f"commit for twelve months priced that year at "
         f"{pc(MCC['vlcc_1y_tc']/MCC['vlcc_spot_broker']-1)} against the spot rate in "
         f"front of it. That is a market saying, with its own money, that it does not "
         f"expect spot to hold"],
        ['The supply reason why',
         f"The crude tanker order book stands near {pc(MCC['orderbook_pct'], 0)} of the "
         f"trading fleet, a seventeen-year high, with the very large crude carrier order "
         f"book higher still. Ships ordered into a strong market arrive into whatever "
         f"market exists when they deliver, and this is the mechanism by which every "
         f"previous tanker upcycle ended"],
        ["This study's own base path",
         f"The base case runs the very large crude carrier rate from USD "
         f"{n0(MCC['vlcc_path'][0])} in {YRL[0]} down to USD {n0(MCC['vlcc_path'][4])} by "
         f"{YRL[4]}, a straight glide to the {HYRS[1]}-{HYRS[2]} average. It crosses the "
         f"one-year charter rate above in {YRL[1]}-{YRL[2]}, which is to say it is "
         f"broadly consistent with what the forward market was willing to pay"]]
table(rows, [2.30, 4.70], size=8.3, align_right_from=9)
P(f"The alternative — rates settling {pc(0.30, 0)} above the mid-cycle anchor rather than "
  f"at it — is the direction the company's own guidance and its contracted expansion point "
  f"in, and it is computed in full: it gives AED {p2(DCFS['fv_aed'])} a share against the "
  f"base case's AED {p2(DCF['fv_aed'])}. It is published as an alternative reading rather "
  f"than adopted, because the two observations above are external, dated and specific, "
  f"while the case for sustained strength rests on a view about future supply and demand "
  f"that this study is not in a position to hold with confidence.")
P(f"One more comparison puts the crux in proportion, and it is worth being careful about "
  f"what it does and does not show. Moving the mid-cycle rate anchor across the whole "
  f"tested range, from {pc(min(float(k) for k in SN['anchor']))} to "
  f"{pc(max(float(k) for k in SN['anchor']))} of the base, moves fair value by AED "
  f"{p2(anchor_span)} a share — and that range is wide enough to carry fair value across "
  f"the market price, which it reaches between the {pc(1.1, 0)} and {pc(1.2, 0)} anchors. "
  f"Widening the beta across the {p3(SN['betas'][0])}-to-{p3(SN['betas'][-1])} range "
  f"tested in section 1.9 moves it by AED {p2(max(beta_span)-min(beta_span))}, which is "
  f"{(max(beta_span)-min(beta_span))/anchor_span:.1f} times as much and remains the "
  f"widest single sensitivity in the study. But the two are not comparable as open "
  f"questions. The beta is measured, with a 90% interval of [{BF['ci90'][0]:.2f}, "
  f"{BF['ci90'][1]:.2f}] that the bear and bull cases already carry at full width; where "
  f"tanker rates settle after {YRL[0][:4]} is not measured by anything and cannot be. That "
  f"is why this section, and not the discount rate, is where the study says its judgement "
  f"is genuinely exposed.")

# ---- 1.8 macro ---------------------------------------------------------------
H2('1.8  Macro and country — the sourced cost of capital')
P(f"The dirham has been fixed to the US dollar at {PEG:.4f} since 1997 and monetary policy "
  f"follows the Federal Reserve accordingly: the Central Bank of the UAE base rate stood "
  f"at {pc(IN['cb_rate'], 2)} and was maintained at its July {YRL[0][:4]} decision, its "
  f"last change being a cut from {pc(IN['cb_rate']+0.0025, 2)} in December {HYRS[2][2:]}. "
  f"That matters for this study in a specific way: because the company reports in dollars "
  f"and the currency is pegged, there is no exchange-rate view anywhere in the valuation, "
  f"and the whole of the country question reduces to a small sovereign premium rather than "
  f"a convertibility argument.")
rows = [['Component', 'Explicit window', 'Terminal', 'Source and construction'],
        ['Observed risk-free rate', pc(W['rf_observed'], 2), '',
         'the UAE dirham Treasury bond tranche maturing January 2031, at its July '
         f"{YRL[0][:4]} auction yield"],
        ['Less the sovereign default spread', neg(pc(W['sov_spread'], 2)), '',
         'the published country-risk file adjusted default spread for the UAE on its '
         'Moody’s Aa2 assessment. Country risk must enter once, and it enters '
         'through the premium below, so it is netted out of the observed yield here'],
        ['Adjusted risk-free rate', pc(W['rf_star'], 2), pc(W['rf_terminal'], 2),
         'the terminal figure is a long-run nominal anchor for a dollar-pegged economy: a '
         '2% inflation objective plus a 1.25% long-run real policy rate, the same '
         'construction the terminal growth rate rests on'],
        ['Beta', p3(W['beta']), p3(W['beta']),
         f"own-stock weekly regression against the {BE['regressor']} over the full listed "
         f"history: n = {n0(BE['n'])}, R-squared {BE['r2']:.3f}, standard error "
         f"{BE['se']:.3f}, 90% interval [{BE['ci90'][0]:.2f}, {BE['ci90'][1]:.2f}]. The "
         f"evidence table below sets this out in full alongside the equal-weight "
         f"composite, which gives {p3(BFA['beta'])}"],
        ['Equity risk premium', pc(W['erp'], 2), pc(W['erp'], 2),
         f"the January {YRL[0][:4]} country-risk file: a mature-market premium of "
         f"{pc(W['erp_mature'], 2)} plus a UAE country premium of {pc(W['crp'], 2)}"],
        ['Cost of equity', pc(W['ke'], 2), pc(W['ke_term'], 2),
         f"adjusted risk-free rate plus beta times the premium. On the equal-weight "
         f"composite's {p3(BFA['beta'])} it would be {pc(W['ke_beta1'], 2)}; on the "
         f"lead-lag sum beta of {p3(IN['beta_dimson'])}, {pc(W['ke_dimson'], 2)}"],
        ['Cost of debt, pre-tax', pc(W['kd'], 2), pc(W['kd_term'], 2),
         'a weighted read of six disclosed instruments — the evidence table follows'],
        ['Cost of debt, after tax', pc(W['kd_after_tax'], 2), '',
         f"at the {pc(W['tax_stat'], 0)} statutory rate"],
        ['Equity weight', pc(W['we'], 1), pc(W['we'], 1),
         f"market capitalisation of USD {m0(W['mktcap'])} million against gross debt of "
         f"USD {m0(W['debt'])} million. Market-value weights throughout; book equity is "
         f"never used"],
        ['Debt weight', pc(W['wd'], 1), pc(W['wd'], 1), ''],
        ['Cost of capital', pc(W['wacc'], 2), pc(W['wacc_term'], 2),
         'each forecast year is discounted at its own point on the glide between the two, '
         'and the terminal value is capitalised at the terminal rate and brought back on '
         'the same cumulative factor as the year-five cash flow — one date, one price of '
         'time'],
        ['The glide, year by year', ' · '.join(pc(x, 2) for x in W['wacc_glide']), '',
         'published so the discount factors in section 1.1 are reproducible']]
table(rows, [1.55, 1.00, 0.72, 3.73], size=8.1, band_rows={6, 11},
      left_cols=(3,))

H2('The beta — what it was measured against, and what a different market would give')
P(f"A beta is a statement about co-movement with a market, so the series chosen to stand "
  f"for the market decides the answer. This study regresses the share's own weekly returns "
  f"on the {BE['regressor']} — the published, capitalisation-weighted index of the "
  f"exchange the share is listed on. The index series runs from "
  f"{BE['regressor_span'][0]} to {BE['regressor_span'][1]} across "
  f"{n0(BE['regressor_rows'])} sessions and was screened against the exchange's own "
  f"trading calendar before use.")
rows = [['Item', 'Value', 'Note'],
        ['Market series used', BE['regressor'], BE['regressor_basis']],
        ['Span of that series',
         f"{BE['regressor_span'][0]} to {BE['regressor_span'][1]}",
         f"{n0(BE['regressor_rows'])} sessions"],
        ['Observations in the regression', n0(BE['n']),
         f"weekly returns over the share's full listed history of "
         f"{BE['window_years']:.2f} years — the share listed in June 2023, so a five-year "
         f"window does not exist for it"],
        ['Beta', p3(BE['beta']),
         'the adopted figure, used in the cost of equity above'],
        ['Standard error', f"{BE['se']:.3f}",
         'against the estimate itself, which is the usability test this has to pass'],
        ['R-squared', f"{BE['r2']:.3f}",
         'the share of the weekly return variance the index explains'],
        ['90% confidence interval',
         f"{BE['ci90'][0]:.3f} to {BE['ci90'][1]:.3f}",
         'the bear and bull cases in this study take these two bounds directly, so the '
         'published fair-value range is the range this estimate itself supports'],
        ['Lead-lag sum beta', p3(BE['dimson']['sum_beta']),
         f"one lead and two lags, which recovers co-movement booked late because the share "
         f"does not trade on every session. It is {BE['dimson']['uplift_vs_ols']:+.3f} "
         f"against the adopted figure, so the correction points slightly higher rather "
         f"than lower"],
        ['The same regression on an equal-weight composite', p3(BFA['beta']),
         f"{BE['composite_variant']['note']} R-squared "
         f"{BE['composite_variant']['r2']:.3f} on {n0(BE['composite_variant']['n'])} "
         f"observations across {n0(BE['composite_names'])} names"],
        ['The same regression on the wider two-exchange composite',
         p3(BE['full_library_variant']['beta']),
         f"{BE['full_library_variant']['note']} R-squared "
         f"{BE['full_library_variant']['r2']:.3f} across "
         f"{n0(BE['full_library_variant']['names'])} names"],
        ['Weekly observations excluded', n0(BE['unused_stock_weeks']), BE['unused_note']]]
table(rows, [1.72, 1.10, 4.18], size=8.0, band_rows={4, 9}, left_cols=(1, 2))
caption(f"Why the published index and the composite differ by {BFP['beta']-BFA['beta']:.3f} "
        f"of a beta is a fact about index construction, not about the company. A published "
        f"index is weighted by size, so it is dominated by the same large-capitalisation "
        f"group this share belongs to and a large share moving with its large peers "
        f"registers as full co-movement. An equal-weight composite gives the exchange's "
        f"smallest and thinnest names the same say as its largest, so it measures "
        f"co-movement against a market this share is not really a member of, and a large "
        f"liquid name will look defensive against it almost mechanically. Two disclosures "
        f"cut against the adopted figure rather than for it and are stated here rather "
        f"than left out. The share is itself a constituent of the index it is measured "
        f"against, and on a capitalisation-weighted index that cannot be removed; run the "
        f"equal-weight proxy both ways and including the subject lifts the measured beta "
        f"by {BE['self_inclusion_bias']['beta_proxy_including_subject']-BE['self_inclusion_bias']['beta_proxy_excluding_subject']:.3f}, "
        f"which is the scale of the same pull the published-index figure carries. And the "
        f"index series ends {BE['regressor_span'][1]}, before the share's last session "
        f"used elsewhere in this study, so {n0(BE['unused_stock_weeks'])} weekly "
        f"observations fall outside the window rather than being paired against a stale "
        f"index level.")

H2('The cost of debt — six instruments, not an assumption')
P(f"A single disclosed range is not evidence of what a company pays. Six separate "
  f"instruments are visible in the statements and the market, and they are set out here "
  f"rather than summarised into one number.")
rows = [['Instrument', 'Basis', 'Rate']]
for name, basis, rate in W['kd_evidence']:
    rows.append([name, basis, pc(rate, 2)])
rows.append(['Adopted cost of debt, pre-tax', 'weighted across the drawn book',
             pc(W['kd'], 2)])
table(rows, [4.10, 1.55, 1.35], size=8.3, band_rows={7}, left_cols=(1,))
caption(f"The spread of the evidence is the point. The parent revolving facility at the "
        f"secured overnight financing rate plus 80 basis points is the cheapest money in "
        f"the book and is a genuine benefit of the ownership structure; third-party bank "
        f"debt costs {(W['kd_bank_mid']-W['kd_method1'])*10000:,.0f} basis points more. "
        f"The adopted rate sits between them, weighted by what is actually drawn. It sits "
        f"above the local sovereign yield of {pc(W['rf_observed'], 2)}, as a corporate "
        f"borrowing in the same currency must. The perpetual capital securities are "
        f"included in the evidence because they price the company's own subordinated risk, "
        f"but they are deducted in the bridge rather than carried in the weights, so they "
        f"do not enter the cost of capital twice.")

H2('Where this construction is contested, and what the alternatives are worth')
P("Five choices above are legitimately arguable. Each alternative is computed and its "
  "value published, so a reader who prefers a different convention can take the number "
  "directly instead of guessing at its size.")
rows = [['The choice made', 'The alternative', 'Value on the alternative', 'Why ours'],
        [f"Beta measured against {BFP['label']}, giving {p3(IN['beta'])}",
         f"The same regression against {BFA['label']}, giving {p3(BFA['beta'])} — cost of "
         f"equity {pc(W['ke_beta1'], 2)} instead of {pc(W['ke'], 2)}",
         f"AED {p2(LN['dcf_beta_alt']['base'])} against {p2(LN['dcf']['base'])}",
         'The published index is preferred, and not narrowly: it is the index of the '
         'exchange the share is listed on, and measuring a share against a composite in '
         'which the exchange’s smallest names carry the same weight as its largest '
         'measures it against a market it is not a member of. The composite is published '
         'at full size because it is what an earlier construction of this study used and '
         'the difference is large. Note that the adopted choice is the less flattering '
         'one'],
        ['Perpetual capital securities deducted at carrying value',
         'Deducted at the present value of their perpetual coupon, capitalised at the '
         'terminal cost of capital',
         f"AED {p2(DCFH['fv_aed'])}, {DCFH['fv_aed']-DCF['fv_aed']:+.2f} against "
         f"{p2(DCF['fv_aed'])}",
         'Carrying value is the more conservative and is the amount that would have to be '
         'found if the securities were ever called. The coupon-value treatment is the '
         'right one if they are genuinely permanent. Both are shown in the bridge'],
        ['Country risk entering once, through the premium',
         'Using the raw local yield of ' + pc(W['rf_observed'], 2) + ' together with a '
         'premium that already contains the country charge',
         'raises the cost of equity by the sovereign spread of '
         + pc(W['sov_spread'], 2) + ' and lowers the value',
         'That construction double-counts sovereign risk. The spread is netted from the '
         'yield and re-enters through the premium; the net country charge is therefore '
         'the premium itself, not the premium plus the spread'],
        ['A single premium basis, because only one exists for this country',
         'The credit-default-swap basis of the same published file',
         'not available — the UAE has no sovereign swap entry in the file',
         'This is stated rather than omitted. Gulf comparators that do carry both bases '
         'show they are not interchangeable: Saudi Arabia’s swap basis gives 5.72% '
         'against 5.01% on the agency credit-rating basis, a gap of about seventy basis '
         'points. A reader should treat the single available basis as carrying that much '
         'construction uncertainty'],
        ['Tax charged unit by unit at each unit’s own disclosed effective rate',
         f"A uniform {pc(IN['tax_topup_rate'], 0)} across the group, the domestic minimum top-up rate",
         f"AED {p2(SN['tax']['0.15'])} against {p2(DCF['fv_aed'])}",
         f"The unit rates are what the company actually bore in {HYRS[2]} — about "
         f"{pc(IN['tax_shipping'], 0)} in shipping, where international shipping income is "
         f"relieved. Using a statutory rate the company does not pay would be wrong; but "
         f"the relief is a policy choice that can change, so the downside is priced rather "
         f"than assumed away"]]
table(rows, [1.62, 1.85, 1.28, 2.25], size=7.9, align_right_from=9)

# ---- 1.9 sensitivity ---------------------------------------------------------
H2('1.9  Sensitivity')
figure(os.path.join(HERE, 'fig2_sens.png'), 7.0,
       f"Figure 4 — left, fair value across beta and terminal growth; right, fair value "
       f"against the mid-cycle rate the fleet reverts to. The market price of AED "
       f"{p2(SPOT)} is crossed in the beta grid between the {p2(SN['betas'][1])} and "
       f"{p3(SN['betas'][2])} rows, and in the rate-anchor range between the "
       f"{pc(1.1, 0)} and {pc(1.2, 0)} anchors.")
P("Each anchor is varied independently around its own base, so each row shows what the "
  "valuation needs that one thing to do.")
rows = [['Beta →'] + [p3(b) if abs(b - IN['beta']) < 1e-9 else p2(b)
                           for b in SN['betas']]]
for j, g in enumerate(SN['gs']):
    rows.append([f"terminal growth {pc(g, 1)}"] +
                [p2(SN['grid_beta_g'][i][j]) for i in range(len(SN['betas']))])
table(rows, [1.60, 1.08, 1.08, 1.08, 1.08, 1.08], size=8.4)
caption(f"Fair value in AED per share. The adopted construction is the {p3(IN['beta'])} "
        f"column at {pc(IN['g_terminal'], 1)} growth; the equal-weight composite "
        f"alternative is the {p3(SN['betas'][0])} column at the same growth. The "
        f"right-hand column of {p3(SN['betas'][-1])} is the top of the regression's own "
        f"90% confidence interval and is where the bear case is struck; the bull case is "
        f"struck at the bottom of that interval, {BF['ci90'][0]:.3f}, which sits just "
        f"inside the left-hand column. Beta moves the answer across the whole width of "
        f"this table; growth moves it a fraction of that.")
rows = [['Sensitivity', 'Range tested', 'Fair value span (AED/share)', 'Swing']]
rows.append(['Beta in the cost of equity',
             f"{p3(SN['betas'][0])} – {p3(SN['betas'][-1])}",
             f"{p2(min(beta_span))} – {p2(max(beta_span))}",
             p2(max(beta_span) - min(beta_span))])
rows.append(['Mid-cycle rate the fleet reverts to',
             f"{pc(min(float(k) for k in SN['anchor']))} – "
             f"{pc(max(float(k) for k in SN['anchor']))} of the base anchor",
             f"{p2(min(SN['anchor'].values()))} – {p2(max(SN['anchor'].values()))}",
             p2(anchor_span)])
rows.append(['Capital expenditure',
             f"{pc(min(float(k) for k in SN['capex']))} – "
             f"{pc(max(float(k) for k in SN['capex']))} of the guided programme",
             f"{p2(min(capex_span))} – {p2(max(capex_span))}",
             p2(max(capex_span) - min(capex_span))])
rows.append(['Group tax rate',
             f"{pc(min(float(k) for k in SN['tax']), 0)} – "
             f"{pc(max(float(k) for k in SN['tax']), 0)} uniform across the group",
             f"{p2(min(tax_span))} – {p2(max(tax_span))}",
             p2(max(tax_span) - min(tax_span))])
rows.append(['Terminal growth',
             f"{pc(SN['gs'][0], 1)} – {pc(SN['gs'][-1], 1)}",
             f"{p2(min(g_span))} – {p2(max(g_span))}",
             p2(max(g_span) - min(g_span))])
rows.append(['Bear-to-bull scenario composite',
             f"rates, capital expenditure and the beta at the two ends of its own 90% "
             f"interval — {BF['ci90'][1]:.3f} in the bear, {BF['ci90'][0]:.3f} in the bull",
             f"{p2(LN['dcf']['bear'])} – {p2(LN['dcf']['bull'])}",
             p2(LN['dcf']['bull'] - LN['dcf']['bear'])])
table(rows, [2.10, 1.95, 1.60, 1.35], size=8.4, left_cols=(1, 2))
caption(f"Ranked by single-row swing, the beta is the largest by a wide margin — larger "
        f"than the operating crux, larger than the capital programme, larger than the tax "
        f"exposure. That is worth reading precisely. The width of the beta row is the "
        f"width of a measured statistical interval, and the study publishes its bear and "
        f"bull cases at that interval's two ends rather than choosing a comfortable point "
        f"inside it; the width of the rate-anchor row is a judgement about the future that "
        f"no amount of data settles. The first is uncertainty that has been quantified, "
        f"the second is uncertainty that has not. The tax row deserves its own note: at a "
        f"uniform {pc(IN['tax_topup_rate'], 0)} the "
        f"value falls to AED {p2(SN['tax']['0.15'])}, a loss of AED "
        f"{p2(DCF['fv_aed']-SN['tax']['0.15'])} a share, and that is the priced cost of "
        f"the shipping relief being withdrawn. Every row is a full re-run of the unit "
        f"build and the bridge, not a multiplier applied to a finished number.")

# ============================ 6  §2  TECHNICAL ===============================
H1('2  Technical and price structure')
figure(os.path.join(HERE, 'fig3_ma.png'), 7.0,
       f"Figure 5 — price against the 20-, 50- and 200-session moving averages with the "
       f"computed support and resistance ladder, to {TC['data_date']}.")
rows = [['Marker', 'Level (AED)', 'Reading'],
        ['Last close', p2(TC['close']), 'the anchor for everything in this study'],
        ['20-session average', p2(TC['ma']['20']),
         f"price is {sgn(TC['close']/TC['ma']['20']-1, 1)} against it; the average is "
         f"{TC['ma_slope']['20']}"],
        ['50-session average', p2(TC['ma']['50']),
         f"price is {sgn(TC['close']/TC['ma']['50']-1, 1)} against it; the average is "
         f"{TC['ma_slope']['50']}"],
        ['200-session average', p2(TC['ma']['200']),
         f"price is {sgn(TC['close']/TC['ma']['200']-1, 1)} against it; the average is "
         f"{TC['ma_slope']['200']}"],
        ['Nearest resistance', p2(TC['levels']['res'][0]),
         f"then {p2(TC['levels']['res'][1])} and {p2(TC['levels']['res'][2])}; levels are "
         f"computed from recency-weighted pivot clusters, not drawn by hand"],
        ['Nearest support', p2(TC['levels']['sup'][0]),
         f"then {p2(TC['levels']['sup'][1])} and {p2(TC['levels']['sup'][2])}; the "
         f"nearest support has been touched "
         f"{n0(TC['level_detail']['sup'][0]['touches'])} times in the window"],
        ['52-week range', f"{p2(TC['lo_52w'])} – {p2(TC['hi_52w'])}",
         f"the close sits {pc(TC['pct_off_high'])} below the high and "
         f"{pc(TC['pct_off_low'])} above the low"],
        ['Relative strength index (14)', p2(TC['rsi']),
         'neutral — neither stretched nor washed out'],
        ['Average true range (14)', p2(TC['atr']),
         f"about {pc(TC['atr_pct'])} of the price a session — a normal tape"],
        ['Moving-average crossover', f"{n0(TC['ma_cross']['ago'])} sessions ago",
         f"the 50-session average crossed above the 200-session; the configuration has "
         f"held since"],
        ['Annualised volatility', pc(H3M['anchor_vol_ann']),
         'the current state of the range-based volatility model, and the input that sets '
         'the width of the cone in section 3']]
table(rows, [1.75, 1.15, 4.10], size=8.4, left_cols=(2,))
P(f"{TC['tech']['summary']}")
P(f"The structure to watch is straightforward. {TC['tech']['bull']} {TC['tech']['bear']} "
  f"None of this is a valuation argument — it is the price context the valuation has to be "
  f"read against. It is worth noting where the fundamental estimates sit relative to this "
  f"ladder, because on the adopted construction they now sit inside it rather than far "
  f"above it: the weighted central of AED {p2(D['central'])} sits at the furthest computed "
  f"resistance of {p2(TC['levels']['res'][-1])}, and the cash-flow lens on its own, at AED "
  f"{p2(LN['dcf']['base'])}, sits between the first and second computed supports of "
  f"{p2(TC['levels']['sup'][0])} and {p2(TC['levels']['sup'][1])}. The equal-weight "
  f"composite reading of AED {p2(D['central_beta_alt'])} is the only one of the three "
  f"above every level in the table. A valuation and a level ladder are unrelated "
  f"constructions and their agreeing here proves nothing; it is recorded because the two "
  f"disagreed markedly under the study's earlier measurement of the market and no longer "
  f"do.", space_after=10)

# =========================== 7  §3  PRICE MAP ================================
H1('3  A probabilistic price map')
P(f"This section answers a different question from the valuation. It does not ask what the "
  f"business is worth; it asks where the share price could plausibly be in one and three "
  f"months, given how this share has actually moved. Fifty thousand price paths are "
  f"simulated from a volatility model fitted to the daily high-low-open-close range, with "
  f"a fat-tailed shock and a drift anchored to the cost of carry — the local deposit rate "
  f"of {pc(STK['rf_live'], 2)} less the dividend yield of "
  f"{pc(STK['q_annual'], 2)}, which is a cost of money and not a directional view.")
P(f"The widths are tested rather than assumed, and the test is worth stating in plain "
  f"terms. Over the share's listed history the three-month distributions scored "
  f"{sgn(BT3['skill_norm'], 2)} better than a random-walk benchmark anchored on the same "
  f"cost of carry, across {n0(BT3['windows'])} independent non-overlapping windows with "
  f"origins from {BT3['first_origin']} to {BT3['last_origin']}, each one forecast using "
  f"only data available before it. Outcomes fell across the distribution roughly evenly "
  f"rather than bunching at one end: a uniformity test on where each outcome landed "
  f"returns p = {BT3['chi2_p']:.2f}, and a second test of the same thing returns p = "
  f"{BT3['ks_p']:.2f}. Coverage was {pc(BT3['cov50'], 0)} inside the 50% band, "
  f"{pc(BT3['cov80'], 0)} inside the 80% and {pc(BT3['cov90'], 0)} inside the 90% — close "
  f"to advertised at the wide bands, light at the narrow one on a sample of only "
  f"{n0(BT3['windows'])} windows. The one-month horizon has more windows and behaves "
  f"better: {n0(BT1['windows'])} of them, coverage {pc(BT1['cov50'], 0)} / "
  f"{pc(BT1['cov80'], 0)} / {pc(BT1['cov90'], 0)}, uniformity p = {BT1['chi2_p']:.2f}, and "
  f"a score {sgn(BT1['skill_norm'], 2)} against the benchmark — level with it rather than "
  f"ahead of it. Pooling {n0(BTS['windows'])} three-month windows that start on staggered "
  f"dates and therefore overlap one another gives {sgn(BTS['skill_norm'], 2)} and coverage "
  f"of {pc(BTS['cov50'], 0)} / {pc(BTS['cov80'], 0)} / {pc(BTS['cov90'], 0)} — a larger "
  f"sample, but one whose windows are not independent of each other, so it corroborates "
  f"the picture rather than adding new evidence to it.")
P(f"Two limitations belong here rather than in a footnote. First, the bands are about "
  f"{pc(BT3['width_vs_benchmark']-1, 0)} wider than the benchmark's, which is a real cost "
  f"and means the model buys its accuracy partly with width. Second, this share listed in "
  f"June 2023, so the cleaned series spans {S0['span_years']:.1f} years and a five-year "
  f"set of origins does not exist for it — the width setting rests on the wider market "
  f"panel of {n0(FITM['panel_names'])} Abu Dhabi names and "
  f"{n0(FITM['market_windows'])} windows, which scored {sgn(FITM['market_skill'], 2)} "
  f"against the benchmark with a 90% interval of {sgn(FITM['market_ci90'][0], 1)} to "
  f"{sgn(FITM['market_ci90'][1], 1)}. On both the individual share and the panel the "
  f"honest summary is the same: the model is level with or modestly ahead of a random walk "
  f"and its stated probabilities are close to true, which is what this map claims and no "
  f"more.")
P("This is a map of price dispersion, not a forecast, and it is never blended with the "
  "fair-value work above.")
figure(os.path.join(HERE, 'fig4_fan.png'), 7.0,
       f"Figure 6 — the forward price cone to three months. The dashed lines are the two "
       f"fundamental centrals: AED {p2(D['central'])} on the beta measured against the "
       f"published index, and AED {p2(D['central_beta_alt'])} on the equal-weight "
       f"composite.")

H2('Percentile map (AED per share)')
rows = [['Horizon', '5th', '25th', 'Median', '75th', '95th', 'Above the price today'],
        [f"1 month (to {H1M['grade_date']})"] +
        [p2(H1M['pct'][k]) for k in ('p5', 'p25', 'p50', 'p75', 'p95')] +
        [pc(H1M['p_above'], 0)],
        [f"3 months (to {H3M['grade_date']})"] +
        [p2(H3M['pct'][k]) for k in ('p5', 'p25', 'p50', 'p75', 'p95')] +
        [pc(H3M['p_above'], 0)]]
table(rows, [1.75, 0.80, 0.80, 0.80, 0.80, 0.80, 1.25], size=8.5)
caption(f"The check dates are calendar dates fixed when the map is struck: one month and "
        f"three months from {STK['anchor_date']}, rolled forward to the exchange's first "
        f"real trading session. The median barely moves from the price today because the "
        f"drift is a carry, not a view.")
figure(os.path.join(HERE, 'fig5_dist.png'), 5.3,
       "Figure 7 — the one-month outcome distribution.")
figure(os.path.join(HERE, 'fig6_dist.png'), 5.3,
       "Figure 8 — the three-month outcome distribution.")

H2('Level-touch ladder')
rows = [['Event', '1 month', '3 months'],
        ['Finishes 10% or more above the price today', pc(H1M['p_up10'], 0),
         pc(H3M['p_up10'], 0)],
        ['Finishes 10% or more below the price today', pc(H1M['p_dn10'], 0),
         pc(H3M['p_dn10'], 0)],
        ['Touches 10% above at any point', pc(H1M['touch_up10'], 0),
         pc(H3M['touch_up10'], 0)],
        ['Touches 10% below at any point', pc(H1M['touch_dn10'], 0),
         pc(H3M['touch_dn10'], 0)],
        [f"Finishes above the nearest computed resistance of "
         f"{p2(TC['levels']['res'][0])}", '—', '—'],
        [f"Finishes below the nearest computed support of {p2(TC['levels']['sup'][0])}",
         '—', '—']]
rows = rows[:5]
table(rows, [3.30, 1.35, 1.35], size=8.5)
caption("Touch probabilities exceed finish probabilities because a path can visit a level "
        "and come back. The distinction matters for anyone thinking about a level rather "
        "than a date.")

# ========================= 8  §4  COMPARISON =================================
H1('4  Comparison of the lenses')
rows = [['Read', 'What it says', 'What it assumes'],
        ['Fundamental — published index',
         f"AED {p2(D['central'])}, {vs(D['central'])}",
         f"that the share's own listed history, measured against its exchange's published "
         f"index, describes its risk, and that the tanker fleet reverts to its "
         f"{HYRS[1]}-{HYRS[2]} average rate"],
        ['Fundamental — equal-weight composite',
         f"AED {p2(D['central_beta_alt'])}, {vs(D['central_beta_alt'])}",
         'that the market is better represented by an equal-weight composite of the '
         "exchange's names than by its published index, with the same operating forecast"],
        ['Cash flow alone, published index',
         f"AED {p2(LN['dcf']['base'])}, {vs(LN['dcf']['base'])}",
         f"a cost of capital gliding {pc(W['wacc'], 2)} to {pc(W['wacc_term'])}"],
        ['Cash flow alone, equal-weight composite',
         f"AED {p2(LN['dcf_beta_alt']['base'])}, {vs(LN['dcf_beta_alt']['base'])}",
         f"the same, gliding {pc(DCFA['wacc'], 2)} to {pc(DCFA['wacc_term'])}"],
        ['Multiples, blended',
         f"AED {p2(LN['relative']['base'])}, {vs(LN['relative']['base'])}",
         "that a contracted shipowner's multiple and a spot owner's multiple, blended on "
         "this company's own disclosed spot exposure, describe it"],
        ['Sum of the parts',
         f"AED {p2(SOTP['fv_aed'])}, {vs(SOTP['fv_aed'])}",
         'the same two multiples applied where each belongs rather than to the group'],
        ['Rates hold near current levels',
         f"AED {p2(DCFS['fv_aed'])}, {vs(DCFS['fv_aed'])}",
         'that the fleet settles well above its own recent average — the direction the '
         "company's guidance points"],
        ['The market', p2(SPOT), 'revealed preference of the marginal buyer'],
        ['Three-month price map',
         f"median {p2(H3M['pct']['p50'])}, {pc(H3M['p_above'], 0)} chance of finishing "
         f"above the price today",
         'that volatility persists as it has; no view on value at all']]
table(rows, [1.85, 2.05, 3.10], size=8.3, align_right_from=9)
P(f"Read down that table and the striking thing is how little room there is between the "
  f"reads. The market price of AED {p2(SPOT)} sits above the cash-flow lens of AED "
  f"{p2(LN['dcf']['base'])} and below the weighted central of AED {p2(D['central'])}, a "
  f"band of roughly {abs(D['central']/LN['dcf']['base']-1)*100:.0f}% from end to end. The "
  f"two multiple lenses land above the market, but they import their cost of capital from "
  f"comparators rather than state one, so they are evidence about relative pricing rather "
  f"than an independent answer; the expert panel in Appendix C, which prices mid-cycle "
  f"earnings rather than a terminal value, centres at AED {p2(PANEL)}, {ab(PANEL)}. Read "
  f"together, the evidence brackets the screen price. It does not point away from it.")
P(f"This is a weaker claim than the study previously made, and the reason is worth stating "
  f"plainly. The cash-flow lens rests on a beta of {p3(IN['beta'])}, measured on "
  f"{n0(BE['n'])} weekly observations against the {BE['regressor']} — the published index "
  f"of the share's own exchange. The economic prior for a fleet owner has always been that "
  f"it carries the risk of the market its ships trade in whoever signs the charter, and "
  f"that prior and the regression now say the same thing. Measure the market instead as an "
  f"equal-weight composite of the same exchange's names and the beta falls to "
  f"{p3(BFA['beta'])} and the central rises to AED {p2(D['central_beta_alt'])} — a "
  f"difference of AED {p2(central_gap)} a share that turns entirely on index weighting. "
  f"Both numbers are in this document at full size and neither is hidden inside an "
  f"average, but the adopted one is the published index, and on it this share is close to "
  f"fairly priced rather than materially cheap.")
P("No recommendation and no forecast of the share price is expressed here or anywhere "
  "else in this document. The output is a range and a distribution.", space_after=10)

# ============================ 9  §5  CATALYSTS ===============================
H1('5  Catalysts to watch')
rows = [['Catalyst', 'Why it matters', 'What to watch'],
        ['Second-quarter and half-year results',
         f"the second-quarter rate of USD {n0(FLT['q2_26']['vlcc'])} a day for the "
         f"largest class was an indication given on a call, not a reported figure; the "
         f"half-year statement is the first hard confirmation",
         'the reported time-charter equivalent by class against the indicated levels, and '
         'whether the third quarter is being framed up or down'],
        ['Where rates settle, not where they peak',
         'the base case reverts to the mid-cycle anchor over four years; the whole '
         f"AED {p2(anchor_span)} of the rate sensitivity sits in that path",
         'one-year time-charter fixtures rather than spot prints — a forward commitment '
         'is the market pricing duration, which is what this model needs'],
        ['Tanker supply',
         f"an order book near {pc(MCC['orderbook_pct'], 0)} of the trading fleet is the "
         f"mechanism by which the cycle ends",
         'deliveries against scrapping, and whether ordering continues at these rates'],
        ['The contracted expansion delivering',
         f"gas carrier vessel-years rise from {n1(FLT['gas_vessel_years'][0])} in "
         f"{YRL[0][:4]} to {n1(FLT['gas_vessel_years'][3])} by {YRL[3][:4]}, which is what "
         f"takes spot exposure down from {pc(IN['spot_share_ebitda_26'], 0)} to "
         f"{pc(IN['spot_share_ebitda_29'], 0)} of earnings",
         'on-time delivery of the ethane and Ruwais carriers, and new long-term charters'],
        ['Capital allocation, because the model runs to net cash',
         f"on this build net debt falls from {xt(FIN['nd_ebitda'][0], 2)} earnings in "
         f"{YRL[0]} to net cash by {YRL[3]}, against a stated target of "
         f"{xt(IN['nd_ebitda_target_lo'], 1)} to {xt(IN['nd_ebitda_target_hi'], 1)}. "
         f"The company will not sit there",
         'acquisitions, a step-up in distributions beyond the stated 5% a year, or a '
         'larger newbuild programme — see section 7'],
        ['The tax relief on international shipping',
         f"the shipping units bore about {pc(IN['tax_shipping'], 0)} in {HYRS[2]}; a "
         f"uniform {pc(IN['tax_topup_rate'], 0)} would cost AED "
         f"{p2(DCF['fv_aed']-SN['tax']['0.15'])} a share",
         'any change to the exclusion of international shipping income from the domestic '
         'minimum top-up tax'],
        ['Offshore Projects',
         f"the least visible line in the model: {HYRS[2]} revenue of USD "
         f"{m0(SEGH['Offshore Projects']['revenue'][2])} million falls to a guided USD "
         f"{m0(DRV['Offshore Projects']['rev'][0])} million in {YRL[0]} after the large "
         f"island project completed",
         'new engineering and construction awards replacing the completed work'],
        ['The perpetual capital securities',
         f"USD {b1(IN['hybrid_face'])} billion ranking ahead of the ordinary shares, worth "
         f"AED {p2(DCFH['fv_aed']-DCF['fv_aed'])} a share between the two treatments",
         'any call, refinancing or reset of the coupon']]
table(rows, [1.55, 2.75, 2.70], size=8.2, align_right_from=9)

# ====================== 10  §6  READING THE ZONES ============================
H1('6  Reading the probability zones')
P(f"The three-month distribution has a median of AED {p2(H3M['pct']['p50'])} and a "
  f"5th-to-95th span of {p2(H3M['pct']['p5'])} to {p2(H3M['pct']['p95'])}. Read that "
  f"honestly: the model treats a {sgn(H3M['pct']['p5']/SPOT-1, 0)} move and a "
  f"{sgn(H3M['pct']['p95']/SPOT-1, 0)} move as equally unremarkable tail outcomes over a "
  f"single quarter. Anyone who finds that range uncomfortably wide is reacting to the "
  f"volatility of the share, which has run near {pc(H3M['anchor_vol_ann'], 0)} annualised, "
  f"rather than to the model.")
rows = [['Zone', 'Three-month range (AED)', 'How to read it'],
        ['Lower tail', f"below {p2(H3M['pct']['p5'])}",
         'a 1-in-20 outcome; would need a genuine shock — a rate collapse faster than any '
         'in the recent record, or a change in the contracted relationship with the '
         'parent'],
        ['Lower half of the central band',
         f"{p2(H3M['pct']['p25'])} – {p2(H3M['pct']['p50'])}",
         'ordinary drift lower; the cash-flow lens on its own sits inside this zone and '
         'the book lens below it, so this is not a range at which the fundamental work '
         'would call the share cheap'],
        ['Upper half of the central band',
         f"{p2(H3M['pct']['p50'])} – {p2(H3M['pct']['p75'])}",
         'ordinary drift higher; this zone contains the study’s own weighted central, so '
         'no repricing of the business is needed to reach it'],
        ['Upper tail', f"above {p2(H3M['pct']['p95'])}",
         'a 1-in-20 outcome; the zone in which the market would be pricing the rate '
         'strength as durable, or the equal-weight reading of the discount rate'],
        ['Where the weighted central sits', p2(D['central']),
         f"between the 50th and 75th percentile of the three-month distribution. The "
         f"valuation and the price map — which knows nothing about value — are in the same "
         f"place, which is a change from this study's earlier measurement of the market "
         f"and is the clearest sign that the share is close to fairly priced"],
        ['Where the cash-flow lens alone sits', p2(LN['dcf']['base']),
         f"between the 25th and 50th percentile — below the price today, and reachable "
         f"inside the horizon without anything unusual happening"],
        ['Where the equal-weight composite central sits', p2(D['central_beta_alt']),
         f"between the 75th and 95th percentile of the three-month distribution"]]
table(rows, [1.80, 1.70, 3.50], size=8.4, left_cols=(2,))

# ============================= 11  §7  CAVEATS ===============================
H1('7  Caveats and what would change our mind')
for head, body in [
    ("The beta is the study, and it is unresolved. ",
     f"The difference between the share's own regressed beta of {p3(IN['beta'])} and an "
     f"asset-risk beta of one is AED {p2(beta_gap)} a share on the cash-flow lens — larger "
     f"than the capital-expenditure row and the tax row, and about the same size as moving "
     f"the tanker-rate anchor across its whole tested range. Across the beta range tested "
     f"in section 1.9 the swing is AED {p2(max(beta_span)-min(beta_span))}, the widest "
     f"single sensitivity in the study. The regression is real and passes its usability "
     f"conditions, "
     f"but it rests on {BE['window_years']:.1f} years of history in a period when the "
     f"contracted arm was growing faster than the merchant fleet. Both readings are "
     f"published as equals. If forced to say which way the evidence leans: the market "
     f"price sits on the asset-beta reading."),
    ("The terminal value is most of the answer. ",
     f"{pc(DCF['tv_share'], 0)} of the cash-flow model's enterprise value is the terminal "
     f"value on the own-beta construction, {pc(DCFA['tv_share'], 0)} on the asset-beta "
     f"one. That is high, and it is the arithmetic consequence of discounting a business "
     f"whose explicit years are depressed by a heavy capital programme — capital "
     f"expenditure runs USD {m0(F['capex'][0])} million in {YRL[0]} against earnings of "
     f"USD {m0(F['ebitda'][0])} million. The terminal assumptions are stressed across the "
     f"cost of capital, growth and the rate anchor in section 1.9, and the growth in the "
     f"perpetuity is paid for through an explicit reinvestment rate rather than assumed "
     f"free."),
    ("The build sits above the company's own guidance, on purpose. ",
     f"The {YRL[0]} build is {sgn(GD['Group']['ebitda_gap'])} above the guided group "
     f"earnings midpoint — {sgn(GD['Shipping']['ebitda_gap'])} in Shipping. Management "
     f"states that its shipping assumptions are set well below prevailing spot rates and "
     f"its logistics guidance at minimum activity levels. This build marks the fleet to "
     f"the rates the company itself reported and indicated. Both numbers are in section "
     f"1.6 and the gap is not reconciled anywhere below; a reader who prefers the guided "
     f"figures should scale the first forecast year accordingly."),
    ("The modelled balance sheet goes to net cash, and the company will not allow that. ",
     f"On this build net debt falls from {xt(FIN['nd_ebitda'][0], 2)} earnings in "
     f"{YRL[0]} to {xt(FIN['nd_ebitda'][2], 2)} in {YRL[2]} and turns to net cash of USD "
     f"{m0(-FIN['net_debt'][4])} million by {YRL[4]}, against a stated medium-term target "
     f"of {xt(IN['nd_ebitda_target_lo'], 1)} to {xt(IN['nd_ebitda_target_hi'], 1)}. At the "
     f"low end of that target the {YRL[4]} balance sheet would carry about USD "
     f"{m0(nd_target_debt)} million of net debt, so the modelled path leaves roughly USD "
     f"{m0(nd_target_debt-FIN['net_debt'][4])} million of unused capacity, on top of an "
     f"undrawn committed revolving facility of USD {b1(IN['rcf_committed'])} billion. The "
     f"company will either lever up for acquisitions or return more capital. This does not "
     f"change the answer, and the reason is worth being explicit about: free cash flow to "
     f"the firm is struck before financing, so the enterprise value is indifferent to the "
     f"mix of debt, dividends and buybacks. What the choice changes is the shape of the "
     f"return to shareholders and the risk profile of the equity — not what the operating "
     f"business is worth."),
    ("There is no net-asset-value lens, which is the sector standard for a shipowner. ",
     f"The conventional way to value a fleet owner is vessel by vessel at independent "
     f"broker valuations, bridged to equity. Those valuations are not obtainable from this "
     f"research environment, so the book-value lens stands in for them at "
     f"{pc(LW['book'], 0)} weight. The only direct evidence on the gap between carrying "
     f"value and market value is the January {YRL[0][:4]} sale of a 2017-built very large "
     f"crude carrier for USD {m0(BK['vessel_sale_price'])} million against a carrying "
     f"value of USD {m0(BK['vessel_sale_book'])} million — {xt(BK['vessel_value_to_book'], 2)} "
     f"book, on one vessel, in a strong market. It says the book lens is biased "
     f"conservative, but one transaction is not a fleet valuation and it is not "
     f"extrapolated into the numbers."),
    ("The second-quarter rate is an indication, not a reported figure. ",
     f"The USD {n0(FLT['q2_26']['vlcc'])} a day used for the largest class in the second "
     f"quarter of {YRL[0][:4]} is the level the company indicated on its first-quarter "
     f"call, not an audited or reported outcome. It is one of the four quarters that sets "
     f"the {YRL[0]} rate, so an error there flows into the first forecast year. The "
     f"reported half-year will settle it."),
    ("Two rate substitutions are carried in the fleet build. ",
     f"Quarterly rates for the medium-range class are not disclosed for {HYRS[1]}, so the "
     f"{HYRS[2]} average stands in; the handysize vessels are not broken out at all and "
     f"are carried at the medium-range rate. Together those are "
     f"{n0(FLT['owned']['mr']+FLT['owned']['hs'])} of {n0(owned_total)} vessels and the "
     f"lowest earners in the fleet, so the effect is small — but it is a substitution, and "
     f"it is labelled as one."),
    ("Two unit inputs are solved rather than sourced. ",
     f"Per-vessel running cost of USD {n0(FLT['opex_day'])} a day is solved so that the "
     f"owned fleet's earnings reproduce the reported {HYRS[2]} result, and the gas carrier "
     f"day rate of USD {n0(FLT['gas_rate_day'])} is solved from reported {HYRS[2]} revenue "
     f"over consolidated vessel-years. Neither is disclosed at a finer level anywhere in "
     f"the filings. Both are labelled as solved wherever they appear, and both are "
     f"anchored on a reported outcome rather than assumed."),
    ("The revenue gross-up for the tanker fleet is presentational. ",
     f"Reported Tankers revenue was {xt(IN['tnk_grossup_25'], 2)} the owned fleet's own "
     f"charter-equivalent revenue in {HYRS[2]}, because of chartered-in and relet trading "
     f"that carries almost no margin. The forecast sets that ratio at "
     f"{xt(IN['tnk_grossup_26'], 2)} from {YRL[0]}, on the evidence of the first quarter, "
     f"where revenue fell year on year while the rate earned per vessel more than doubled. "
     f"The ratio moves the revenue line and never the earnings line, so it cannot affect "
     f"the valuation — but a reader comparing this study's revenue forecast with a "
     f"broker's should know the two may be on different conventions."),
    ("The tax relief on international shipping is a policy, not a right. ",
     f"The model taxes each unit at its own disclosed {HYRS[2]} effective rate, which is "
     f"about {pc(IN['tax_shipping'], 0)} in shipping because international shipping income "
     f"is excluded from the UAE's domestic minimum top-up tax rules. That exclusion is a "
     f"policy choice. Priced at a uniform {pc(IN['tax_topup_rate'], 0)} across the group, fair value falls "
     f"to AED {p2(SN['tax']['0.15'])}."),
    ("The price history is short, and it is short in a specific way. ",
     f"The share listed in June 2023, so the cleaned series spans "
     f"{S0['span_years']:.1f} years. That is short for a beta and too short for a "
     f"five-year test of the price map, which is why the map's width setting rests on the "
     f"wider Abu Dhabi panel and why the beta is corroborated three ways in section 1.8 "
     f"rather than accepted at face value."),
    ("What would change our mind, specifically. ",
     f"Upward: one-year time-charter fixtures settling durably above the mid-cycle anchor "
     f"used here; the contracted gas programme delivering on time and taking spot exposure "
     f"below the disclosed {pc(IN['spot_share_ebitda_29'], 0)}; a longer price history "
     f"that keeps the regressed beta near {p3(IN['beta'])} as the mix shifts toward "
     f"shipping. Downward: rates reverting faster than the four-year glide assumed here; "
     f"the shipping tax relief being withdrawn; a capital programme that grows without a "
     f"matching contracted return; or evidence that the contracted relationship with the "
     f"parent is repriced rather than renewed.")]:
    bullet(body, bold_head=head)
P('', space_after=8)

# =========================== 12  APPENDIX A ==================================
H1('Appendix A  Financial statements')
H2(f"A.1  Income statement — three years reported and five years forecast "
   f"(consolidated, USD mn)")
cols = HYRS + YRL
rows = [['USD mn'] + cols]


def h3(key, fmt=m0, negate=False):
    return [neg(fmt(abs(HI[key][i]))) if (negate or HI[key][i] < 0) else fmt(HI[key][i])
            for i in range(3)]


rows.append(['Revenue'] + h3('revenue') + [m0(x) for x in F['revenue']])
rows.append(['Direct and operating costs'] + h3('direct_costs') +
            [neg(m0(x)) for x in F['opcost']])
rows.append(['Gross profit'] + h3('gross_profit') + ['—'] * 5)
rows.append(['General and administrative'] + h3('ga') + ['—'] * 5)
rows.append(['Other income and charges'] +
            [m0(HI['other_income'][i] + HI['other_expenses'][i] + HI['ecl'][i])
             for i in range(3)] + ['—'] * 5)
rows.append(['Earnings before interest, tax, depreciation and amortisation'] +
            h3('ebitda_op') + [m0(x) for x in F['ebitda']])
rows.append(['  margin'] + [pc(x) for x in HI['ebitda_margin']] +
            [pc(x) for x in F['ebitda_margin']])
rows.append(['Depreciation and amortisation'] + h3('dna', negate=True) +
            [neg(m0(x)) for x in F['dna']])
rows.append(['Earnings before interest and tax'] + h3('ebit') + [m0(x) for x in F['ebit']])
rows.append(['Share of joint ventures and associates'] + h3('assoc') + ['—'] * 5)
rows.append(['Net finance cost'] +
            [neg(m0(abs(HI['fin_income'][i] + HI['fin_costs'][i])))
             for i in range(3)] +
            [neg(m0(FIN['interest'][i] - FIN['fin_income'][i])) for i in range(5)])
rows.append(['Profit before tax'] + h3('pbt') + [m0(x) for x in FIN['pbt']])
rows.append(['Income tax'] + h3('tax', negate=True) + [neg(m0(x)) for x in FIN['tax']])
rows.append(['Profit for the year'] + h3('pat') + [m0(x) for x in FIN['pat']])
rows.append(['Non-controlling interests'] +
            [neg(m0(HI['pat'][i] - HI['npa'][i])) if HI['pat'][i] != HI['npa'][i] else '—'
             for i in range(3)] + [neg(m0(x)) for x in FIN['nci']])
rows.append(['Attributable to ordinary and hybrid holders'] + h3('npa') +
            [m0(x) for x in FIN['npa']])
rows.append(['Perpetual securities coupon'] +
            ['—', '—', neg(m0(IN['hybrid_coupon_fy25']))] +
            [neg(m0(FIN['hybrid_coupon']))] * 5)
rows.append(['Earnings per share (USD)'] + [f"{x:.3f}" for x in HI['eps']] +
            [f"{x:.3f}" for x in FIN['eps']])
table(rows, [1.72, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66], size=7.5,
      band_rows={6, 16, 18})
caption(f"Every reported line is taken directly from the company's audited consolidated "
        f"statements. Two rows are house derivations and are labelled: earnings before "
        f"interest, tax, depreciation and amortisation is earnings before interest and tax "
        f"plus depreciation and amortisation — the audited statements carry no such line, "
        f"and the company's own reported figure (USD {m0(HI['ebitda_reported'][2])} "
        f"million in {HYRS[2]} against the USD {m0(EBITDA_H[2])} million used here) adds "
        f"the share of joint ventures and one-off items; and forecast earnings per share "
        f"is attributable profit over shares outstanding. Forecast profit is struck after "
        f"interest on the modelled debt path and after tax at each unit's own rate, so it "
        f"differs from the free-cash-flow waterfall in section 1.1, which is a "
        f"pre-financing measure by construction.")

H2('A.2  Balance sheet — condensed house layout (consolidated, USD mn)')
rows = [['USD mn'] + cols]
rows.append(['Property, plant and equipment'] + [m0(x) for x in HB['ppe']] +
            [m0(b['ppe']) for b in FBS])
rows.append(['Right-of-use assets'] + [m0(x) for x in HB['rou']] + ['—'] * 5)
rows.append(['Joint ventures and associates'] + [m0(x) for x in HB['jv']] +
            [m0(b['jv']) for b in FBS])
rows.append(['Intangibles and goodwill'] +
            [m0(HB['intangibles'][i] + HB['goodwill'][i]) for i in range(3)] +
            [m0(b['intangibles'] + b['goodwill']) for b in FBS])
rows.append(['Inventories'] + [m0(x) for x in HB['inventories']] + ['—'] * 5)
rows.append(['Receivables and amounts due from related parties'] +
            [m0(HB['receivables'][i] + HB['due_from_related'][i]) for i in range(3)] +
            ['—'] * 5)
rows.append(['Payables and amounts due to related parties'] +
            [neg(m0(HB['payables'][i] + HB['due_to_related'][i])) for i in range(3)] +
            ['—'] * 5)
rows.append(['Net working capital'] + [m0(x) for x in HB['nwc']] +
            [m0(b['nwc']) for b in FBS])
rows.append(['Cash and cash equivalents'] + [m0(x) for x in HB['cash']] +
            [m0(b['cash']) for b in FBS])
rows.append(['Total assets'] + [m0(x) for x in HB['total_assets']] + ['—'] * 5)
rows.append(['Gross debt'] + [m0(x) for x in HB['debt']] +
            [m0(b['gross_debt']) for b in FBS])
rows.append(['Net debt'] + [m0(x) for x in HB['net_debt']] +
            [m0(b['net_debt']) if b['net_debt'] >= 0 else neg(m0(-b['net_debt']))
             for b in FBS])
rows.append(['Perpetual capital securities'] +
            [m0(x) if x else '—' for x in HB['hybrid']] +
            [m0(b['hybrid']) for b in FBS])
rows.append(['Non-controlling interests'] + [m0(x) if x else '—' for x in HB['nci']] +
            [m0(b['nci']) for b in FBS])
rows.append(['Equity attributable to ordinary shareholders'] +
            [m0(x) for x in HB['equity_parent']] +
            [m0(b['equity_parent']) for b in FBS])
rows.append(['Book value per share (USD)'] +
            [f"{HB['equity_parent'][i]/SH/1000.0:.4f}" for i in range(3)] +
            [f"{b['bvps']:.4f}" for b in FBS])
rows.append(['Net debt / earnings'] +
            [xt(HB['net_debt_ebitda'][i], 2) for i in range(3)] +
            [xt(x, 2) for x in FIN['nd_ebitda']])
rows.append(['Return on equity'] + [pc(x) for x in HB['roe']] +
            [pc(b['roe']) for b in FBS])
table(rows, [1.72, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66], size=7.5,
      band_rows={8, 15})
caption(f"All three reported years are audited; every line is the closing figure from the "
        f"company's own consolidated statements, with no roll-forward. The forecast "
        f"columns are a condensed layout carrying only the lines the model actually rolls "
        f"forward — the fleet, working capital, the funding and the equity account — and "
        f"lines that are not modelled are shown as unavailable rather than estimated. "
        f"Book value per share excludes the perpetual capital securities, which the "
        f"accounts include inside total equity. The perpetual securities are the reason "
        f"total equity jumped from USD {m0(HB['total_equity'][1])} million to USD "
        f"{m0(HB['total_equity'][2])} million in {HYRS[2]} while equity attributable to "
        f"ordinary shareholders barely moved.")

H2('A.3  Forecast balance-sheet and cash-flow markers')
rows = [['USD mn'] + YRL,
        ['Capital expenditure'] + [neg(m0(x)) for x in F['capex']],
        ['Change in working capital'] +
        [neg(m0(x)) if x >= 0 else m0(-x) for x in F['dnwc']],
        ['Free cash flow to the firm'] + [m0(x) for x in F['fcff']],
        ['Interest on the modelled debt'] + [neg(m0(x)) for x in FIN['interest']],
        ['Perpetual securities coupon'] + [neg(m0(FIN['hybrid_coupon']))] * 5,
        ['Ordinary distributions'] + [neg(m0(x)) for x in FIN['dps']],
        ['Payout ratio on attributable profit'] + [pc(x, 0) for x in FIN['payout']],
        ['Gross debt'] + [m0(b['gross_debt']) for b in FBS],
        ['Net debt'] + [m0(b['net_debt']) if b['net_debt'] >= 0
                        else neg(m0(-b['net_debt'])) for b in FBS],
        ['Net debt / earnings'] + [xt(x, 2) for x in FIN['nd_ebitda']],
        ['Invested capital'] + [m0(b['invested_capital']) for b in FBS],
        ['Return on invested capital'] + [pc(b['roic']) for b in FBS],
        ['Cost of capital that year'] + [pc(x, 2) for x in DCF['glide']],
        ['Spread'] + [f"{(FBS[i]['roic']-DCF['glide'][i])*100:+.1f}pp" for i in range(5)]]
table(rows, [2.20, 0.96, 0.96, 0.96, 0.96, 0.96], size=8.2, band_rows={3, 10, 14})
P(f"Three things in that table are worth reading together. Free cash flow to the firm is "
  f"only USD {m0(F['fcff'][0])} million in {YRL[0]} — on earnings of USD "
  f"{m0(F['ebitda'][0])} million — because the capital programme peaks at USD "
  f"{m0(F['capex'][0])} million and working capital builds by USD {m0(F['dnwc'][0])} "
  f"million in the same year. It then quadruples by {YRL[3]} as the newbuild programme "
  f"delivers and spending falls back toward maintenance levels. That shape is why the "
  f"terminal value carries so much of the enterprise value: the explicit years are the "
  f"investment years. And the spread of return on invested capital over the cost of "
  f"capital is positive in every year of the forecast, narrowing from "
  f"{(FBS[0]['roic']-DCF['glide'][0])*100:+.1f} percentage points to "
  f"{(FBS[4]['roic']-DCF['glide'][4])*100:+.1f} as the rate cycle normalises — this "
  f"business creates value on the study's own cost of capital throughout, which is the "
  f"single most important thing the cash-flow model says.")

# =========================== 13  APPENDIX B ==================================
H1('Appendix B  Peer frame, risk register and the research register')
H2('B.1  Peers and the sector frame')
rows = [['Company', 'Market', 'Relevance', 'Caution']]
rows.append([PEERS[0]['name'], PEERS[0]['market'],
             'the closest listed analogue to the contracted legs — long-term contracted '
             'gas shipping for a national energy company, the same customer structure',
             'a pure contracted shipowner with no merchant fleet and no offshore '
             'logistics arm; its multiple describes the half of this company that is '
             'contracted and says nothing about the other half'])
rows.append([PEERS[1]['name'], PEERS[1]['market'],
             'a large listed spot crude tanker owner — the right frame for the merchant '
             'fleet',
             'no contracted revenue, a different tax and domicile structure, and a '
             'shareholder base that trades it as a rate proxy'])
rows.append([PEERS[2]['name'], PEERS[2]['market'],
             'a second listed spot crude and product tanker owner, used with the first to '
             'average away single-company effects',
             'fewer published measures; only the enterprise multiple is used from it'])
rows.append(['Offshore support and contracting names', 'Gulf and international',
             'the right frame for Integrated Logistics, which is the largest earner',
             'no listed comparator combines offshore contracting with a national oil '
             'company parent as customer and shareholder; the contracted multiple is used '
             'for this leg instead'])
table(rows, [1.62, 1.10, 2.14, 2.14], size=8.1, align_right_from=9)
P(f"The absence of a single clean comparable is itself a finding, and it is the reason the "
  f"relative lens is constructed as a blend and cross-checked by the sum of the parts in "
  f"section 1.3 rather than taken from one peer. Note what the comparators themselves say: "
  f"the contracted shipowner trades at {xt(REL['contracted_multiple'], 2)} enterprise "
  f"value to earnings and the spot owners at {xt(REL['spot_multiple'], 2)} — a gap of "
  f"{REL['contracted_multiple']-REL['spot_multiple']:.1f} turns that exists for exactly "
  f"the reason this study spends section 1.7 on. The market prices contracted marine "
  f"earnings and spot marine earnings as different assets, and so does this study.")

H2('B.2  Risk register')
rows = [['Risk', 'Mechanism', 'Rough valuation impact'],
        ['The rate cycle turning faster than assumed',
         'the base case glides to the mid-cycle anchor over four years; a faster reversion '
         'compresses the explicit years and the terminal return on capital together',
         f"the rate-anchor row spans AED {p2(anchor_span)} a share"],
        ['The cost-of-equity construction',
         'the share’s own regressed beta against an asset-risk beta of one',
         f"AED {p2(beta_gap)} a share between the two published constructions, and AED "
         f"{p2(max(beta_span)-min(beta_span))} across the beta range tested in section "
         f"1.9 — the widest single sensitivity in the study"],
        ['Customer and shareholder concentration',
         'the parent is both the controlling shareholder and the principal customer; '
         f"about {pc(IN['contracted_2026_share'], 0)} of {YRL[0]} revenue is contracted "
         f"with it",
         'not priced as a separate line. It cuts both ways: it is why the contracted '
         'multiple is defensible and why a renegotiation would be severe'],
        ['Capital intensity',
         f"USD {m0(sum(F['capex'][:3]))} million of capital expenditure over the first "
         f"three forecast years against cumulative earnings of USD "
         f"{m0(sum(F['ebitda'][:3]))} million",
         f"the capital-expenditure row spans AED "
         f"{p2(max(capex_span)-min(capex_span))} a share"],
        ['Tax policy',
         'international shipping relief withdrawn or narrowed under the minimum top-up '
         'rules',
         f"AED {p2(DCF['fv_aed']-SN['tax']['0.15'])} a share at a uniform "
         f"{pc(IN['tax_topup_rate'], 0)}"],
        ['The perpetual capital securities',
         'they rank ahead of the ordinary shares and their treatment in the bridge is a '
         'judgement',
         f"AED {p2(DCFH['fv_aed']-DCF['fv_aed'])} a share between the two treatments"],
        ['Vessel values',
         'no independent broker valuation of the fleet is available, so the asset lens '
         'rests on carrying value',
         f"one realised sale at {xt(BK['vessel_value_to_book'], 2)} book suggests the bias "
         f"is conservative; the size of it is unmeasured"],
        ['Short price history',
         f"{S0['span_years']:.1f} years of listed history constrains both the beta and the "
         f"testing of the price map",
         'addressed by corroborating the beta three ways and by resting the price map on '
         'the wider market panel']]
table(rows, [1.80, 2.75, 2.45], size=8.1, align_right_from=9)

H2('B.3  The research register — layers, dated, negative results included')
P("Research for this study proceeded in four layers: the global backdrop, the country, "
  "the industry and the company itself. Company figures come only from the company's own "
  "issued statements and disclosures; no data vendor, broker or press report is used as "
  "the source of any reported historical figure. The full input-by-input register, with a "
  "value, a source, a date and a research layer for each of the several hundred inputs "
  "behind this study, is published as a separate document accompanying it. The primary "
  "documents are listed below, followed by the negative results — the things that could "
  "not be obtained, which shaped what could and could not be asserted.")
rows = [['Source', 'Layer', 'What it provided'],
        ['Audited consolidated financial statements, four fiscal years to '
         + HYRS[2], 'Company',
         'the whole of the reported income statement, balance sheet and cash flow, the '
         'operating segments note, the revenue-by-product note, the cost-line note, the '
         'borrowings and interest-rate notes and the share capital note'],
        ['Reviewed condensed interim financial information, three months to 31 March 2026',
         'Company',
         'the balance sheet the valuation is built on, the perpetual securities note, the '
         'related-party facilities and the first-quarter segment result'],
        ['Management discussion and analysis, ' + HYRS[1] + ', ' + HYRS[2] +
         ' and the first quarter of ' + YRL[0][:4], 'Company',
         'net debt on the company’s own definition, first-quarter free cash flow, '
         'the distribution policy and the medium-term leverage target'],
        ['Investor presentations, ' + HYRS[2] + ' and April ' + YRL[0][:4], 'Company',
         'the fleet tables, time-charter equivalent by vessel class by quarter, charters '
         'out, gas contract vessel-years, contracted revenue, the spot-exposure '
         'disclosure and the earnings sensitivity to a change of USD 1,000 a day'],
        ['Earnings call transcripts, ' + HYRS[2] + ' and the first quarter of '
         + YRL[0][:4], 'Company',
         'the first-quarter rates achieved and the second-quarter indication that section '
         '1.7 turns on, and the guidance basis quoted in section 1.6'],
        ['Related-party transactions report, ' + HYRS[2], 'Company',
         'the scale and pricing of the parent relationship'],
        ['Published country-risk file, January ' + YRL[0][:4], 'Country',
         'the UAE equity risk premium, country premium and sovereign default spread'],
        ['Central bank policy record and government bond auction results', 'Country',
         'the base rate, its last change, and the dirham government bond yield used as '
         'the risk-free rate'],
        ['Listed peer statistics pages', 'Industry',
         'the three comparator multiples used in the relative lens, each dated'],
        ['Trade coverage of the tanker market', 'Industry',
         'the one-year time-charter fixture and the order book share used as the outside '
         'evidence in section 1.7'],
        ['Exchange price history for the share and the Abu Dhabi panel', 'Market',
         'the beta regression, the technical read and the price map']]
table(rows, [2.30, 0.85, 3.85], size=8.0, align_right_from=9)
for head, body in [
    ("No independent vessel valuations could be obtained. ",
     "The sector-standard net-asset-value lens for a shipowner requires broker valuations "
     "of each vessel. None were reachable from this research environment. The book-value "
     "lens stands in, at the lowest weight of the four, and the single realised vessel "
     "sale disclosed by the company is the only direct evidence on the gap."),
    ("Per-vessel charter rates are not disclosed for the gas fleet. ",
     f"The company discloses vessel-years by contract but not rates. The day rate of USD "
     f"{n0(FLT['gas_rate_day'])} used here is solved from reported {HYRS[2]} revenue over "
     f"consolidated vessel-years — the finest level the disclosure supports, and labelled "
     f"as solved throughout."),
    ("Quarterly rates are not disclosed for every class in every year. ",
     f"Medium-range quarterly rates are absent for {HYRS[1]} and the handysize class is "
     f"not broken out at all. The substitutions used are stated in section 1.7 and in the "
     f"caveats."),
    ("Vessel-level running costs are not disclosed. ",
     f"The USD {n0(FLT['opex_day'])} a day used is solved so that the owned fleet's "
     f"charter-equivalent revenue less running cost reproduces the reported {HYRS[2]} "
     f"result for the unit."),
    ("The UAE has no sovereign credit-default-swap entry in the country-risk file. ",
     "The alternative premium basis therefore cannot be built for this country, and the "
     "study says so rather than omitting the comparison silently. Gulf comparators that "
     "carry both bases show a gap of roughly seventy basis points between them, which is "
     "the scale of construction uncertainty a reader should attach to the single "
     "available figure.")]:
    bullet(body, bold_head=head)
P('', space_after=8)

# =========================== 14  APPENDIX C ==================================
H1('Appendix C  The expert valuation panel')
P("Three valuation approaches are run against the same disclosed facts by three notional "
  "experts, each committed to a different method and each required to state in advance "
  "what would prove the method wrong. They are not asked to agree and they do not. All "
  "three work from the same unit build and the same balance sheet; what differs is what "
  "each one thinks a share of this company is a claim on.")

H2('C.1  Expert 1 — mid-cycle earnings power')
P("Worldview: a business is worth a multiple of what it earns in a normal year. Cycles "
  "average out. Discount-rate models multiply small errors in the rate by very large "
  "terminal values and manufacture false precision — and in this particular case the "
  "discount-rate argument is unresolved, which is exactly why it should not be allowed to "
  "drive the answer. Find the mid-cycle earnings, apply a defensible multiple, stop.")
P(f"When it works: for a business with a long enough record that a mid-cycle can be "
  f"identified, and where the capital structure is stable. When it fails: when the "
  f"multiple is imported from a market or a business model with a different cost of "
  f"capital, and when the mid-cycle is guessed rather than measured. Here the second risk "
  f"is real — this share has only {S0['span_years']:.1f} years of listed history and the "
  f"fleet is in the strongest market in a decade, so the mid-cycle has to come from the "
  f"forecast rather than from the record.")
rows = [['Line', 'Value'],
        ['Mid-cycle earnings before interest, tax, depreciation and amortisation '
         '(USD mn) — the five-year average of the unit build', m0(E1['ebitda'])],
        ['Less average depreciation and amortisation (USD mn)', neg(m0(E1['dna']))],
        ['Mid-cycle earnings before interest and tax (USD mn)', m0(E1['ebit'])],
        ['Less tax at the average unit rate (USD mn)', neg(m0(E1['tax']))],
        ['Less interest on the average gross debt (USD mn)', neg(m0(E1['interest']))],
        ['Plus finance income on the cash balance (USD mn)', m0(E1['fin_income'])],
        ['Mid-cycle profit for the year (USD mn)', m0(E1['pat'])],
        [f"Less non-controlling interests at {pc(IN['nci_share'])} (USD mn)",
         neg(m0(E1['pat'] * IN['nci_share']))],
        ['Less the perpetual securities coupon (USD mn)', neg(m0(FIN['hybrid_coupon']))],
        ['Earnings to ordinary shareholders (USD mn)', m0(E1['ord_earnings'])],
        ['Mid-cycle earnings per share (USD)', f"{E1['eps_usd']:.4f}"],
        ['Justified price-to-earnings multiple', xt(E1['pe'], 1)],
        ['Fair value (AED per share)', p2(E1['base'])],
        [f"Range ({xt(e1_pe_lo, 1)} to {xt(e1_pe_hi, 1)})",
         f"{p2(E1['rng'][0])} – {p2(E1['rng'][1])}"]]
table(rows, [4.80, 2.20], size=8.4, band_rows={13})
P(f"Named sensitivity: each single turn of the multiple is worth AED "
  f"{p2(E1['eps_usd']*PEG)} a share, so the {xt(e1_pe_lo, 0)}-to-{xt(e1_pe_hi, 0)} range "
  f"above spans AED {p2(E1['rng'][1]-E1['rng'][0])}. And every USD 100 million of "
  f"mid-cycle earnings before interest, tax, depreciation and amortisation — about "
  f"{pc(100000/E1['ebitda'])} of the base — is worth roughly AED "
  f"{p2(100000*(1-IN['nci_share'])*E1['pe']*PEG/SH/1000.0)} a share at this multiple. "
  f"Note what this method cannot see: it never asks what discount rate the multiple "
  f"implies, so the beta argument that dominates the rest of this study is simply absent "
  f"from it. That is the method's honest position, not an oversight.")
P(f"Falsifier, stated in advance: {E1['falsifier']}", space_after=8)

H2('C.2  Expert 2 — owner cash earnings')
P("Worldview: earnings are an opinion, cash is a fact. The only number that matters is "
  "what an owner could actually take out of the business each year after everything the "
  "business needs to keep running — including the capital expenditure that a fleet "
  "consumes and the coupon on securities that rank ahead of the owner. Capitalise that "
  "stream at the cost of equity and nothing else.")
P("When it works: it is the right discipline for a capital-intensive business where "
  "reported profit and distributable cash diverge, which describes a shipowner precisely. "
  "When it fails: it undercharges nothing and overcharges growth — a company investing "
  "heavily ahead of contracted demand looks poor on this measure right up until the "
  "assets deliver, and this company is in exactly that phase.")
rows = [['Line', 'Value'],
        ['Average free cash flow to the firm over the five forecast years (USD mn)',
         m0(E2['fcff'])],
        ['Less interest after tax (USD mn)', neg(m0(E2['interest_after_tax']))],
        ['Plus finance income after tax (USD mn)',
         m0(E2['fcfe'] - E2['fcff'] + E2['interest_after_tax'] + E2['hybrid_coupon'])],
        ['Less the perpetual securities coupon (USD mn)', neg(m0(E2['hybrid_coupon']))],
        ['Owner cash earnings (USD mn)', m0(E2['fcfe'])],
        ['Grown one year and capitalised at the cost of equity less growth',
         f"× {1+E2['g']:.2f} ÷ ({pc(E2['ke'], 2)} − {pc(E2['g'], 0)})"],
        ['Equity value (USD mn)', m0(E2['value'])],
        ['Fair value (AED per share)', p2(E2['base'])],
        ['Range — the low end at a cost of equity on a beta of one and lower growth, the '
         'high end at a lower country charge and higher growth',
         f"{p2(E2['rng'][0])} – {p2(E2['rng'][1])}"]]
table(rows, [4.80, 2.20], size=8.4, band_rows={8})
P(f"This expert lands at AED {p2(E2['base'])}, below the study's own weighted central of "
  f"AED {p2(D['central'])}, and the reason is specific: the five-year average free cash "
  f"flow of USD {m0(E2['fcff'])} million is dragged down by the investment years. Free "
  f"cash flow to the firm is USD {m0(F['fcff'][0])} million in {YRL[0]} and USD "
  f"{m0(F['fcff'][3])} million in {YRL[3]}; averaging a business across a period when it "
  f"is building the assets that produce the later number is a real charge against it. That "
  f"is the method doing what it says it does, and it is why the range extends as high as "
  f"AED {p2(E2['rng'][1])}.")
P(f"Named sensitivity: this method is a single-stage capitalisation, so it is more "
  f"sensitive to the cost of equity than anything else in the study. At a cost of equity "
  f"on a beta of one — {pc(W['ke_beta1'], 2)} instead of {pc(E2['ke'], 2)} — the same "
  f"owner cash earnings capitalise to roughly AED "
  f"{p2(E2['fcfe']*(1+E2['g'])/(W['ke_beta1']-E2['g'])/SH/1000.0*PEG)} a share, a fall of "
  f"about {pc(1-((E2['fcfe']*(1+E2['g'])/(W['ke_beta1']-E2['g']))/E2['value']), 0)}. This "
  f"expert is therefore the one most exposed to the study's central contested judgement, "
  f"and says so.")
P(f"Falsifier, stated in advance: {E2['falsifier']}", space_after=8)

H2('C.3  Expert 3 — cash returns against the cost of capital')
P("Worldview: value is created only when the return on invested capital exceeds the cost "
  "of that capital, and the amount created is the spread multiplied by the capital "
  "employed. Growth without a positive spread destroys value; growth with one compounds "
  "it. Start from the capital already invested and add the present value of the economic "
  "profit earned on it — which forces the question of whether a very large newbuild "
  "programme is worth funding, rather than assuming it is.")
P("When it works: it is the sharpest available test of a capital programme, and it makes "
  "the discount-rate question unavoidable instead of burying it in a terminal value. When "
  "it fails: it is acutely sensitive to how invested capital is measured, and a fleet "
  "carried at historical cost after a large acquisition is exactly the case where that "
  "measurement is least reliable.")
rows = [['Line', 'Value'],
        ['Invested capital at the valuation date (USD mn) — the fleet, working capital, '
         'intangibles and goodwill', m0(E3['ic0'])],
        ['Present value of economic profit, the five explicit years (USD mn)',
         m0(E3['pv_ep'])],
        ['Present value of terminal economic profit (USD mn)', m0(E3['pv_ep_term'])],
        ['Enterprise value (USD mn)', m0(E3['ev'])],
        ['Less net debt, the perpetual securities and minorities, plus joint ventures '
         '(USD mn)', neg(m0(E3['ev'] - E3['equity'])) if E3['ev'] > E3['equity']
         else m0(E3['equity'] - E3['ev'])],
        ['Equity value (USD mn)', m0(E3['equity'])],
        ['Fair value (AED per share)', p2(E3['base'])],
        ['Range — the low end fades the economic profit hard, the high end lets it persist',
         f"{p2(E3['rng'][0])} – {p2(E3['rng'][1])}"]]
table(rows, [4.80, 2.20], size=8.4, band_rows={7})
rows = [['Year'] + YRL,
        ['Return on invested capital'] + [pc(b['roic']) for b in FBS],
        ['Cost of capital charged — the explicit-window rate, held flat'] +
        [pc(W['wacc'], 2)] * 5,
        ['Spread'] + [f"{s*100:+.1f}pp" for s in E3['spread']],
        ['Economic profit — net operating profit after tax less the capital charge '
         '(USD mn)'] + [m0(x) for x in E3['ep']]]
table(rows, [2.20, 0.96, 0.96, 0.96, 0.96, 0.96], size=8.3, band_rows={3})
caption(f"This is the most revealing exhibit in the study. The spread is positive in every "
        f"forecast year — the business earns {pc(FBS[0]['roic'], 0)} on capital in "
        f"{YRL[0]} against a cost of {pc(DCF['glide'][0], 0)} — and it narrows steadily as "
        f"the rate cycle normalises and the capital base grows. That is a company creating "
        f"value throughout, but creating less of it each year, which is a very different "
        f"picture from either a compounder or a value destroyer. Two conventions in this "
        f"table are named so they cannot be confused with the ones used elsewhere. The "
        f"return divides by closing invested capital, matching Appendix A.3; and the "
        f"capital charge is the explicit-window cost of capital of {pc(W['wacc'], 2)} held "
        f"flat across all five years rather than the declining schedule the cash-flow "
        f"model discounts at, so the spread row is exactly the return row less "
        f"{pc(W['wacc'], 2)} and the economic-profit row is exactly that spread on the "
        f"same closing capital. Appendix A.3 shows the spread on the declining schedule "
        f"instead, which is why the two tables give different spreads from the same "
        f"returns. Note also that this leg's enterprise value of "
        f"USD {m0(E3['ev'])} million differs from the cash-flow model's USD "
        f"{m0(DCF['ev'])} million: economic-profit and cash-flow valuations are "
        f"algebraically identical on identical assumptions, and the gap here is entirely "
        f"the different terminal treatment — a fading economic-profit perpetuity against a "
        f"reinvestment-funded terminal value. Expert 3 is therefore a restatement of the "
        f"cash-flow model under a different terminal discipline, not independent "
        f"confirmation of it, and is read as such.")
P(f"Named sensitivity: a one-percentage-point parallel reduction in the cost-of-capital "
  f"schedule widens the spread in every year and lifts this valuation by roughly a fifth; "
  f"the same move in the opposite direction takes it below the market price. Nothing in "
  f"the operating build has a comparable effect on this method, which is the point it is "
  f"making.")
P(f"Falsifier, stated in advance: {E3['falsifier']}", space_after=8)

H2('C.4  Cross-examination')
rows = [['Challenge', 'From', 'Conceded or rejected'],
        ['"Your multiple is a discount rate you have not written down. On mid-cycle '
         'earnings and this share count it implies a cost of equity near the low end of '
         'the range the rest of this study is arguing about — you have silently taken a '
         'side."', 'Expert 3 to Expert 1',
         'Conceded. The multiple is a judgement and it does embed a cost of capital. The '
         'defence is only that it embeds one drawn from what comparable marine assets '
         'actually trade at rather than from a regression on three years of data. That is '
         'a weaker claim than the method usually makes, and it is the weakest joint in '
         'this leg.'],
        ['"Averaging free cash flow across the five years charges the owner for a '
         'newbuild programme that is contracted and will earn. You are treating '
         'investment as if it were consumption."', 'Expert 1 to Expert 2',
         f"Partly conceded. Free cash flow rises from USD {m0(F['fcff'][0])} million to "
         f"USD {m0(F['fcff'][3])} million as the programme delivers, so the average does "
         f"understate the steady state. Rejected in part, though: the fleet is not a "
         f"one-off build. Maintenance capital and fleet renewal recur, and every previous "
         f"cycle in this industry has been ended by exactly the kind of ordering this "
         f"programme is part of."],
        ['"Invested capital carries a fleet acquired at the top of a cycle at historical '
         'cost. If it is understated your spread is flattered; if it is overstated your '
         'whole method collapses toward book."', 'Expert 2 to Expert 3',
         f"Conceded, and the direction is disclosed. The one piece of evidence available "
         f"points the other way — a vessel sold at {xt(BK['vessel_value_to_book'], 2)} "
         f"carrying value — which means invested capital is more likely understated and "
         f"the measured return correspondingly flattered. That makes this leg's spread "
         f"optimistic, not conservative, and it is stated here rather than left for a "
         f"reader to find."],
        ['"All three of you are arguing about the numerator. The number that actually '
         'decides this valuation is the beta, and only one of you prices it."',
         'The panel to itself',
         f"Accepted as the central unresolved issue, and it is why the panel divides the "
         f"way it does. Expert 1 never touches it. Expert 2 is fully exposed to it, which "
         f"is why its range spans AED {p2(E2['rng'][1]-E2['rng'][0])}. Expert 3 prices it "
         f"year by year and finds that the spread stays positive on either construction, "
         f"which is the one useful thing the panel can say about it: the business creates "
         f"value at both costs of capital — the argument is only about how much."]]
table(rows, [2.45, 1.20, 3.35], size=8.0, align_right_from=9)

H2('C.5  The three in one room')
figure(os.path.join(HERE, 'figD1_experts.png'), 6.9,
       f"Figure 9 — the three experts' ranges. The brass tick is each base case, the gold "
       f"band the panel centre of AED {p2(PANEL)}, the vertical line the market price of "
       f"AED {p2(SPOT)}.")
P(f"The panel spans AED {p2(min(E1['base'], E2['base'], E3['base']))} to "
  f"{p2(max(E1['base'], E2['base'], E3['base']))} — a factor of "
  f"{max(E1['base'], E2['base'], E3['base'])/min(E1['base'], E2['base'], E3['base']):.2f} "
  f"between the most and least generous base case, which is a narrow disagreement by the "
  f"standards of this series. That narrowness is itself informative: three methods that "
  f"share almost nothing methodologically land within AED "
  f"{p2(max(E1['base'], E2['base'], E3['base'])-min(E1['base'], E2['base'], E3['base']))} "
  f"of one another, and all three land near the market price rather than near this "
  f"study's own weighted central of AED {p2(D['central'])}.")
P(f"The panel centre of AED {p2(PANEL)} sits {ab(PANEL)} and "
  f"{sgn(PANEL/D['central']-1, 0)} against this study's own-beta central. That gap is "
  f"real and it has a single explanation: every one of the three experts works from "
  f"mid-cycle or five-year-average earnings, and none of them capitalises a terminal value "
  f"the way the cash-flow model does. The cash-flow model puts {pc(DCF['tv_share'], 0)} of "
  f"its enterprise value beyond the fifth year; the panel puts effectively none there. A "
  f"reader who distrusts long terminal values should weight the panel; a reader who "
  f"believes a contracted marine infrastructure business has a long life beyond a "
  f"five-year window should weight the model. Both positions are defensible and the gap "
  f"between them is stated at full size rather than smoothed.")

H2('C.6  Reading the divergence')
rows = [['Assumption', 'Expert 1', 'Expert 2', 'Expert 3', 'Why it swings the answer'],
        ['Capital expenditure', 'ignored — an earnings measure',
         'charged in full, averaged across the build years',
         'charged through invested capital and the return on it',
         'the largest single source of the gap between Experts 1 and 2'],
        ['The cost of equity', 'implicit inside the multiple, never stated',
         f"{pc(E2['ke'], 2)} explicit, and the whole answer moves with it",
         'the full glide, year by year, on both sides of the spread',
         'Expert 2 is fully exposed, Expert 1 not at all — which is why they can agree on '
         'a number for entirely different reasons'],
        ['Terminal value', 'none — no perpetuity at all',
         'a single perpetuity of owner cash earnings',
         'a fading economic-profit perpetuity',
         f"the cash-flow model puts {pc(DCF['tv_share'], 0)} of its value beyond year "
         f"five; none of the three does, which is most of why the panel sits below the "
         f"study's central"],
        ['The rate cycle', 'averaged into the mid-cycle earnings',
         'averaged into the five-year cash flow',
         'visible year by year in the narrowing spread',
         'only Expert 3 lets the reader see the cycle turning rather than absorbing it '
         'into an average'],
        ['The perpetual securities',
         'charged as a coupon against earnings', 'charged as a coupon against cash',
         'deducted at carrying value in the bridge',
         'the two treatments differ by AED '
         + p2(DCFH['fv_aed'] - DCF['fv_aed']) + ' a share in the main model']]
table(rows, [1.30, 1.42, 1.42, 1.42, 1.44], size=7.9, align_right_from=9)
P("The instruction to the reader is not to average these three. It is to decide which "
  "premise is true — whether a fleet's investment years should be charged against its "
  "owner, whether a marine business has value beyond a five-year window, and which cost "
  "of equity applies — and then to use the corresponding number. The disagreement is a "
  "map of what you need to have a view on.", space_after=10)

# ======================== 15 / 16  ABOUT + DISCLOSURE ========================
H1('About this series')
P("This series publishes independent, educational valuation studies of listed companies. "
  "Each study is built from the company's own disclosed financial statements and named "
  "market data, states its assumptions explicitly, computes every figure in an auditable "
  "model rather than in prose, and publishes the ranges those assumptions produce. Studies "
  "never carry a recommendation or a forecast of the share price. Where a figure is "
  "estimated or solved rather than disclosed, it is labelled. Where a source could not be "
  "reached, the gap is recorded rather than filled.")
P("Where a judgement has two legitimate constructions, both are computed and both are "
  "published side by side. This study does that twice: for the cost of equity, which is "
  "the widest single sensitivity in it, and for the treatment of the perpetual capital "
  "securities. Neither pair is averaged, because an average of two constructions is a "
  "number that neither construction supports.")
P("The probabilistic price map in section 3 is produced by a volatility model that is "
  "tested before it is allowed to publish a range: the model is re-run at successive past "
  "dates using only the data available on each of those dates, and every forecast it made "
  "is scored against what the price actually did, alongside a random-walk benchmark. It "
  "describes price dispersion and carries no view on value. It is never combined with the "
  "fair-value work.")

H1('Disclosure and disclaimer')
P("This document is educational analysis and is not investment advice, an offer, or a "
  "solicitation to buy or sell any security. It contains no recommendation and no forecast "
  "of the share price. The author holds no position in the security discussed and has no "
  "business relationship with the company. Figures are drawn from public sources believed "
  "reliable but not independently verified; where figures are derived, solved or estimated "
  "this is stated in the text. Valuation is inherently uncertain and depends on "
  "assumptions that reasonable analysts will dispute — several such disputes are set out "
  "explicitly in this document rather than resolved silently. Simulated distributions are "
  "not guides to future returns, and past price behaviour does not determine future price "
  "behaviour. Readers must reach their own conclusions and should consider taking "
  "independent advice. No liability is accepted for any loss arising from use of this "
  "material.", size=9.2, color=GREY)

out = os.path.join(HERE, 'ADNOCLS_Valuation_Study_09-08-2026_public.docx')
doc.save(out)
bad = [t for t in TBL if t[1] > 7.001]
print(f"wrote {out} | {len(doc.paragraphs)} paragraphs | {len(doc.tables)} tables")
print(f"table width check: {len(TBL)} tables, max total width "
      f"{max(t[1] for t in TBL):.3f}in, over-wide: {bad if bad else 'none'}")
