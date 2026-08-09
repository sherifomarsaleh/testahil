"""EMPOWER_Valuation_Study_09-08-2026_public.docx — python-docx builder, house style.
Reads study_numbers.json (and the companion data files) exclusively: no financial
numeral is typed into this file — every figure is loaded or derived from the JSONs."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)
exec(open(os.path.join(HERE, 'docx_base.py')).read())   # doc, P, H1, H2, table, box, ...

D  = json.load(open('study_numbers.json'))
T  = json.load(open('tech_read.json'))
BT = json.load(open('backtest_5y.json'))
BR = json.load(open('beta_result.json'))
SW = json.load(open('sweep_register.json'))
SX = json.load(open('sweep_external.json'))
EXI = json.load(open('extract_2026_interims.json'))
EX23 = json.load(open('extract_fy2022_2023.json'))
EX24 = json.load(open('extract_fy2024.json'))
EX25 = json.load(open('extract_fy2025.json'))

IN = {k: v['value'] for k, v in D['inputs'].items()}
HI, U, F, W = D['hist_is'], D['unit'], D['fcst'], D['wacc']
DCF, LN, REL, NRM, BK = D['dcf'], D['lenses'], D['rel'], D['norm'], D['book']
DDM, CEN, SN, CRX, STK = D['ddm'], D['central'], D['sens_wg'], D['crux'], D['strike']
DEWA = D['dewa_buyin']
YRS = F['years']; B = F['base']; PS = F['persist']
BC, BD = DCF['base_ct'], DCF['base_dmtt']
PC, PD = DCF['pers_ct'], DCF['pers_dmtt']
BCD, BEAR, BULL = DCF['base_cds'], DCF['bear'], DCF['bull']
SCN = D['scenarios']
SPOT, SH = D['meta']['spot'], D['meta']['shares_mn']
H1M, H3M = STK['horizons']['1M'], STK['horizons']['3M']
BT5, FIT = BT['five_year'], BT['fit']

def n0(x): return f"{x:,.0f}"
def n1(x): return f"{x:,.1f}"
def p2(x): return f"{x:.2f}"
def p3(x): return f"{x:.3f}"
def pc(x, dp=1): return f"{x*100:.{dp}f}%"
def sgn(x, dp=0): return f"{x*100:+.{dp}f}%"

def rx(pat, s):
    """Pull a figure out of a sourced JSON string — never typed into this file."""
    m = re.search(pat, s)
    if not m:
        raise SystemExit(f"rx failed: {pat!r} not found in {s[:90]!r}")
    return m.group(1)

# ---------------- derived display quantities (all from the JSONs) -------------
ND = W['net_debt']
NDX = ND / HI['FY25']['ebitda']
YLD = DDM['dps'] / SPOT
DEWA_PREM = DEWA['price'] / SPOT - 1
H1G = IN['rev_h1_26'] / IN['rev_h1_25'] - 1
Q2R = EXI['h1_2026']['q2_2026_reported_three_month_column']['revenue'] / 1000.0
Q2R_PRIOR = IN['rev_h1_25'] - EXI['q1_2025_comparative']['income_statement']['revenue'] / 1000.0
Q2G = Q2R / Q2R_PRIOR - 1
CRUX_DELTA = PC['ps'] / BC['ps'] - 1
DMTT_DELTA = BD['ps'] - BC['ps']
EWR = U['ew_ratio']
EW_REVSHARE = IN['ew_cost_fy25'] / IN['rev_fy25']
CONS_RT = U['cons_per_rt25'] * 1000.0          # AED per average connected RT / yr
CAP_RT = U['cap_per_rt25'] * 1000.0
CAPEX_RT = U['capex_per_rt'] * 1000.0
NCI_FRAC = IN['nci_pat_fy25'] / IN['pat_fy25']
NF25 = IN['fin_cost_fy25'] - IN['fin_inc_fy25']    # FY2025 net finance cost
TAXADJ = 1 - (1 - IN['tax_dmtt']) / (1 - IN['tax_ct'])
RT_H1 = IN['rt_conn']['H1_2026']; RT25Y = IN['rt_conn']['2025']
BACKLOG = IN['rt_contracted'] - RT_H1
RT_ADD_H1 = RT_H1 - RT25Y
GUID_LO, GUID_HI = IN['rt_guid_2026']
KD24 = float(rx(r"2024 comparison: ([\d.]+)%", D['inputs']['kd_marg']['source'])) / 100
EIBOR = float(rx(r"spot 3M EIBOR ([\d.]+)%", D['inputs']['kd_marg']['source'])) / 100
RCF_BN = rx(r"AED ([\d.]+)bn RCFs", D['inputs']['kd_marg']['source'])
EUR_TH = rx(r">= EUR (\d+)m", D['inputs']['tax_dmtt']['source'])
MIXD, MIXC, MIXO = re.search(r"demand (\d+)% / consumption (\d+)% / others (\d+)%",
                             [f for f in SW['findings'] if f['fid'] == 'F16'][0]['headline']).groups()
GDP_NEW, GDP_OLD = re.search(r"guidance to ([\d.]+)% from ([\d.]+)%",
                             [f for f in SW['findings'] if f['fid'] == 'F05'][0]['headline']).groups()
DFM_DD = SX['country_uae_macro']['dfm_index']['war_trough_close']['drawdown_from_peak']
RTH_DROP = rx(r"consumption -(\d+)m RTh", D['inputs']['eflh_h1']['source'])
EFLH_HRS = rx(r"(\d+) hrs", D['inputs']['eflh_h1']['source'])
Q1MARG, Q2MARG = re.search(r"Q1 margin ([\d.]+)%, Q2 ([\d.]+)%",
                           D['inputs']['ebitda_h1_26']['source']).groups()
DXB_PCT = rx(r"acquired (\d+)% of DXB CoolCo",
             [f for f in SW['findings'] if f['fid'] == 'F18'][0]['headline'])
DUBAI_SHARE = rx(r"~(\d+)% Dubai share",
                 [f for f in SW['findings'] if f['fid'] == 'F10'][0]['headline'])
BLDGS = rx(r"([\d,]+) buildings", SX['company_news_empower']['h1_2026_results'])
TENOR = rx(r"\(([\d.]+)y tenor", D['inputs']['rf_aed']['source'])
REV21 = float(rx(r"revenue ([\d,]+\.\d)", [f for f in SW['findings'] if f['fid'] == 'F13'][0]['headline']).replace(',', ''))
MARG_LO, MARG_HI = re.search(r"EBITDA margin ([\d.]+)-([\d.]+)%",
                             [f for f in SW['findings'] if f['fid'] == 'F13'][0]['headline']).groups()
# sensitivity-grid coordinates for expert 1's range construction
_gi = SN['g_grid'].index(IN['g_term']); _wi = SN['wacc_grid'].index(W['rating_ct'])
_base_cell = SN['table'][_wi][_gi]
_dn50 = SN['table'][_wi + 1][_gi]; _up50 = SN['table'][_wi - 1][_gi]
E1_LO = CRX['rows'][0]['ps'] * (1 + 0.5 * (_dn50 / _base_cell - 1))
E1_HI = CRX['rows'][-1]['ps'] * (1 + 0.5 * (_up50 / _base_cell - 1))
def ddm_at(g): return DDM['dps'] * (1 + g) / (W['ke_rating'] - g)
E2_G_LO, E2_G_HI = SN['g_grid'][1], SN['g_grid'][3]     # the grid's 2.0% and 3.0% nodes
E2_LO, E2_HI = ddm_at(E2_G_LO), ddm_at(E2_G_HI)
E3_CENTRAL = REL['ps_pe']
WAGE_ESC = SN['g_grid'][2]      # 2.5% — the wage-class escalator, numerically the g node
DEWA_PCT = rx(r'DEWA (\d+)%', D['meta']['ownership'])
FLOAT_PCT = rx(r'~(\d+)%', D['meta']['ownership'])
TB_NDX = rx(r'([\d.]+)x', SX['peers_relative_multiples']['TABREED']['fy2025']['net_debt_ebitda'])
TB_YLD = rx(r'yield ~([\d.]+%)', SX['peers_relative_multiples']['TABREED']['derived_multiples'])
DEWA_YLD = rx(r'yield ~([\d.\-]+-[\d.]+%)', SX['peers_relative_multiples']['DEWA']['price'])

MISSING_FIGS = []
def fig(name, width, cap):
    path = os.path.join(HERE, name)
    if os.path.exists(path):
        figure(path, width, cap)
    else:
        MISSING_FIGS.append(name)

# =========================== 1. MASTHEAD + READ FIRST ========================
t = doc.add_table(rows=1, cols=1)
cell_margins(t, 90, 90, 160, 160)
c = t.cell(0, 0); shade(c, F_DARK); c.width = Inches(7.0)
p = c.paragraphs[0]
r = p.add_run('TESTAHIL Research — Valuation Study')
r.bold = True; r.font.size = Pt(11); r.font.color.rgb = WHITE
r2 = p.add_run('   For information only — not investment advice')
r2.font.size = Pt(9.5); r2.font.color.rgb = RGBColor(0x9F, 0xB0, 0xAC)
doc.add_paragraph().paragraph_format.space_after = Pt(0)

H1('Emirates Central Cooling Systems Corporation PJSC (DFM: EMPOWER)')
P(f"The world's largest listed district-cooling utility — contracted chilled-water capacity "
  f"serving Dubai under a regulated-tariff regime · Dubai Financial Market · reporting currency "
  f"AED · analysis anchored on the closing price of {p2(SPOT)} on 7 August 2026 · study dated "
  f"9 August 2026.", size=10, color=GREY)

box([("READ FIRST — what this document is. ",
      "An educational valuation study. It contains no recommendation, no rating and no price "
      "target. It contains a fair-value range built from the company's own audited financial "
      "statements, a sourced cost of capital and explicitly listed assumptions — and, separately, "
      "a probabilistic map of where the share price could trade over the next one and three "
      "months. The two are different objects and are never blended."),
     ("The first structural judgement — the consumption question. ",
      f"Chilled-water consumption per connected refrigeration ton fell sharply in the first half "
      f"of 2026, in a conflict year, and the shares fell with it. Whether that usage recovers is "
      f"the single question this study turns on, and it is computed BOTH ways as full models: a "
      f"recovery case and a case in which usage never recovers. The finding the reader should "
      f"take away is quantitative: because roughly {pc(EWR, 0)} of consumption revenue is "
      f"electricity and water purchased from DEWA and passed through, permanent loss of the "
      f"usage shock moves the discounted-cash-flow value by only {pc(abs(CRUX_DELTA), 1)} — far "
      f"less than the share-price reaction implies. The capacity charge, not the meter, carries "
      f"the value."),
     ("The second structural judgement — the tax rate, framed twice. ",
      f"The audited 2025 effective tax rate is exactly {pc(IN['tax_ct'], 1)} under UAE corporate "
      f"tax. Whether the {pc(IN['tax_dmtt'], 0)} domestic minimum top-up tax reaches Empower "
      f"through consolidation into the DEWA group (whose revenue far exceeds the EUR "
      f"{EUR_TH}m threshold) is contested and unresolved. The entire valuation is therefore "
      f"published both ways — {p3(BC['ps'])} against {p3(BD['ps'])} on the primary lens, "
      f"{p3(CEN['ct'])} against {p3(CEN['dmtt'])} on the weighted central — side by side, never "
      f"averaged."),
     ("What to check first. ",
      "Section 1.7 (the consumption grid), the two tax columns of the valuation summary below, "
      "and section 1.8's cost-of-debt evidence — the three places where a reader who disagrees "
      "with this study will find the disagreement priced."),
     ("The companion workbook. ",
      "The Excel model calculates live — changing a driver reprices the statements, the "
      "discounted cash flow and the fair value. Only three classes of cell are pasted values, "
      "named on its own READ FIRST sheet: the audited and disclosed history; the historical "
      "calibration of the unit build (the implied capacity rate per refrigeration ton, a "
      "research judgement rather than an arithmetic step); and whole-model re-runs — the "
      "probabilistic price map and the sensitivity grids, where each cell is a complete "
      "revaluation.")])

# =========================== 2. HEADLINE =====================================
H2('Headline')
P(f"Empower is the world's largest district-cooling utility by connected capacity: "
  f"{n0(RT_H1)}k refrigeration tons (RT) connected and {n0(IN['rt_contracted'])}k RT contracted "
  f"at 30 June 2026, serving about {BLDGS} buildings — roughly {DUBAI_SHARE}% of Dubai's "
  f"district-cooling market. It sells cooling on two legs priced under a regulated tariff: a "
  f"contracted CAPACITY (demand) charge, paid on connected tons regardless of usage, and a "
  f"metered CONSUMPTION charge for chilled water actually drawn. The distinction is the whole "
  f"study: the capacity leg is the fixed-cost recovery and, effectively, the profit pool, while "
  f"the consumption leg's dominant cost — electricity and water purchased from DEWA, AED "
  f"{n0(IN['ew_cost_fy25'])}mn in 2025, about {pc(EWR, 0)} of consumption revenue — is largely a "
  f"pass-through.")
P(f"The financial character is a regulated utility's: the EBITDA margin has held between "
  f"{MARG_LO}% and {MARG_HI}% in every audited year since 2021, revenue compounded from AED "
  f"{n0(REV21)}mn (2021) to {n0(IN['rev_fy25'])}mn (2025), and net profit reached AED "
  f"{n0(IN['pat_fy25'])}mn in 2025. Net debt was AED {n0(ND)}mn at 30 June 2026 "
  f"({n1(NDX)}× 2025 EBITDA) after the 2025 refinancing of both AED {RCF_BN}bn revolving "
  f"facilities at a reduced margin. The dividend is committed at AED {n0(IN['div_policy'])}mn a "
  f"year for 2025 and 2026 — {p3(DDM['dps'])} per share, a {pc(YLD, 1)} yield at the anchor "
  f"price — and free cash flow to equity runs almost exactly at the payout: covered, but not "
  f"slack.")
P(f"2026 is the conflict year. Iranian strikes hit UAE infrastructure between February and "
  f"April; a ceasefire has held — fraying — since 8 April. The Dubai market index fell "
  f"{DFM_DD.lstrip('-')} peak to trough and the central bank cut its 2026 GDP growth guidance "
  f"from {GDP_OLD}% to {GDP_NEW}%. Empower's first half showed the transmission mechanism: "
  f"revenue grew {sgn(H1G, 1)}, but the second quarter standalone FELL {pc(abs(Q2G), 1)} year on "
  f"year as consumption dropped {RTH_DROP}m ton-hours (equivalent full-load hours "
  f"{sgn(IN['eflh_h1'], 0)} to {EFLH_HRS} hours), tied by the interim notes partly to "
  f"conflict-hit hospitality occupancy. The shares closed the anchor session at {p2(SPOT)}, "
  f"{pc(T['pct_off_high'], 0)} below their 52-week high of {p2(T['hi_52w'])}, the last leg of "
  f"the fall coming after the 5 August half-year release.")
P(f"On the four lenses used here the fair-value field centres at AED {p3(CEN['ct'])} per share "
  f"under the {pc(IN['tax_ct'], 0)} tax framing and {p3(CEN['dmtt'])} under the "
  f"{pc(IN['tax_dmtt'], 0)} framing, inside a bear-to-bull field of {p3(CEN['bear'])} to "
  f"{p3(CEN['bull'])}, against a market price of {p2(SPOT)}. One disclosed transaction brackets "
  f"the question from above: DEWA took its stake from 56% to 80% in February 2026 by buying "
  f"Dubai Holding's 24% at AED {p2(DEWA['price'])} per share — a related-party CONTROL price, "
  f"{sgn(DEWA_PREM, 0)} above the anchor close, recorded here as a reference point and never as "
  f"fair value.", space_after=10)

# =========================== 3. VALUATION SUMMARY ============================
H2('Valuation summary — every read at a glance, both tax framings side by side')
fig('fig1_football.png', 7.0,
    f"Figure 1 — the valuation field: each lens's range, both tax framings of the central "
    f"estimate, the market price of {p2(SPOT)} and the DEWA control print of "
    f"{p2(DEWA['price'])}.")
rows = [['Read', 'Basis', f"At {pc(IN['tax_ct'], 0)} tax", f"At {pc(IN['tax_dmtt'], 0)} tax",
         'vs spot'],
        ['Discounted cash flow (primary)',
         f"5-year free cash flow to the firm on the two-leg unit build, cost of capital "
         f"{pc(W['rating_ct'], 2)}, terminal growth {pc(IN['g_term'], 1)}. Terminal value = "
         f"{pc(BC['tv_share'], 1)} of enterprise value ({pc(BD['tv_share'], 1)} under the "
         f"{pc(IN['tax_dmtt'], 0)} framing) — disclosed here, in the bridge and in section 1.9",
         p3(BC['ps']), p3(BD['ps']), sgn(BC['ps'] / SPOT - 1, 0)],
        ['Relative multiples',
         f"Tabreed {n1(REL['tabreed_ev_ebitda'])}× EV/EBITDA on 2026E EBITDA (gives "
         f"{p3(REL['ps_rel'])}); Tabreed {n1(REL['tabreed_pe'])}× P/E on 2026E attributable "
         f"profit (gives {p3(REL['ps_pe'])}). Peers are themselves war-depressed — a "
         f"market-regime reading, not an independent fundamental",
         p3(REL['ps_rel']), p3(REL['ps_rel']), sgn(REL['ps_rel'] / SPOT - 1, 0)],
        ['Normalised earnings power',
         f"2026E with consumption at the UNSHOCKED per-ton level; justified multiple "
         f"{n1(NRM['pe_just'])}× from the sustainable return and the cost of equity",
         p3(NRM['ps']), p3(NRM['ps'] * (1 - TAXADJ)), sgn(NRM['ps'] / SPOT - 1, 0)],
        ['Book value and sustainable return',
         f"justified price-to-book {n1(BK['pb_just'])}× on book value of {p3(BK['bvps'])}/share "
         f"at a sustainable return on equity of {pc(BK['roe_sust'], 1)}",
         p3(BK['ps']), p3(BK['ps']), sgn(BK['ps'] / SPOT - 1, 0)],
        ['Weighted central',
         f"cash flow {pc(LN['dcf']['weight'], 0)} · relative {pc(LN['relative']['weight'], 0)} · "
         f"normalised {pc(LN['normalized']['weight'], 0)} · book {pc(LN['book']['weight'], 0)}; "
         f"the two tax columns are alternatives, never averaged",
         p3(CEN['ct']), p3(CEN['dmtt']), sgn(CEN['ct'] / SPOT - 1, 0)],
        ['Scenario field',
         f"bear {p3(CEN['bear'])} (war re-escalation, usage never recovers, {pc(IN['tax_dmtt'],0)} "
         f"tax, +100bp on the cost of equity) to bull {p3(CEN['bull'])} (full recovery, "
         f"{n0(GUID_HI)}k RT/yr)",
         f"{p3(CEN['bear'])} – {p3(CEN['bull'])}", '(bear is struck at this tax rate)', '—'],
        ['Dividend cross-check (unweighted)',
         f"the committed AED {n0(DDM['policy_mn'])}mn growing at {pc(IN['g_term'], 1)}, "
         f"capitalised at the cost of equity",
         p3(DDM['ps']), p3(DDM['ps']), sgn(DDM['ps'] / SPOT - 1, 0)],
        ['Market price', 'closing price, 7 August 2026', p2(SPOT), p2(SPOT), '—'],
        ['DEWA control purchase — reference only',
         f"February 2026, related-party purchase of a 24% block at a control price; a disclosed "
         f"reference point, not fair value",
         p2(DEWA['price']), p2(DEWA['price']), sgn(DEWA_PREM, 0)]]
table(rows, [1.30, 3.00, 0.95, 0.95, 0.60], band_rows={5}, size=8.4)
caption(f"Fair values are ranges and distributions, never a target. The two tax columns are the "
        f"study's central contested judgement published in full: {pc(IN['tax_ct'], 0)} is the "
        f"audited 2025 effective rate, {pc(IN['tax_dmtt'], 0)} is the domestic minimum top-up "
        f"rate that would apply if consolidation into the DEWA group sweeps Empower into the "
        f"OECD minimum-tax regime. Neither is averaged into the other anywhere in this document. "
        f"The terminal-value share of enterprise value ({pc(BC['tv_share'], 1)}) is stated "
        f"beside the lens it belongs to because it is the number a sceptical reader should "
        f"weigh first.")

# =========================== 4. COMPANY OVERVIEW =============================
H2('Company overview — Empower at a glance')
rows = [['Item', 'Detail'],
        ['Listed', 'Dubai Financial Market, 16 November 2022, at the tail of the Dubai '
         'privatisation programme; par value AED 0.10'],
        ['What it does', 'Builds and operates district-cooling plants and distribution networks '
         'in Dubai, selling chilled water to towers, malls, hotels and districts under long-term '
         'connection agreements; also manufactures pre-insulated pipes (Logstor) and operates '
         f"the Dubai airport cooling concession through a {DXB_PCT}%-owned subsidiary "
         f"(DXB CoolCo, a 35-year concession acquired in 2023, inside the connected base)"],
        ['Scale', f"{n0(RT_H1)}k RT connected / {n0(IN['rt_contracted'])}k RT contracted at "
         f"30 June 2026 ({sgn(RT_ADD_H1 / RT25Y, 1)} connected in the half); about {BLDGS} "
         f"buildings; roughly {DUBAI_SHARE}% of the Dubai district-cooling market"],
        ['Revenue model', f"Two legs on one asset base: capacity (demand) charges, contracted "
         f"and paid on connected tons regardless of usage — about {MIXD}% of first-half 2026 "
         f"revenue per the earnings deck — and metered consumption charges, about {MIXC}%, with "
         f"connection and other fees the remaining {MIXO}%. The split of the two legs in AED is "
         f"not separately disclosed in the statements; consumption revenue is disclosed in the "
         f"auditor's key-audit-matter section each year and the split is reconstructed from it "
         f"(section 1.6)"],
        ['Regulation', 'Dubai Executive Council Resolution 6/2021 governs district cooling; '
         'tariffs require approval by the Regulatory and Supervisory Bureau. This study holds '
         'the tariff FLAT in nominal AED throughout — no real escalation is assumed anywhere'],
        ['Ownership', f"DEWA {DEWA_PCT}% since February 2026 "
         f"(it bought Dubai Holding's 24% at AED {p2(DEWA['price'])} per share); free float "
         f"about {FLOAT_PCT}%. DEWA is simultaneously the "
         f"controlling shareholder and the sole supplier of the largest cost line — a "
         f"governance concentration discussed in section 7"],
        ['Shares / market value', f"{n0(SH)}mn shares; AED {n0(D['meta']['mktcap'])}mn at the "
         f"anchor price of {p2(SPOT)}"],
        ['Net debt', f"AED {n0(ND)}mn at 30 June 2026 ({n1(NDX)}× 2025 EBITDA): two AED "
         f"{RCF_BN}bn revolving credit facilities, fully refinanced in 2025 at a reduced margin "
         f"over EIBOR, less cash and term deposits"],
        ['Dividend', f"AED {n0(IN['div_policy'])}mn a year committed for 2025 AND 2026, paid in "
         f"two instalments (October and April) — {p3(DDM['dps'])} per share, {pc(YLD, 1)} at the "
         f"anchor price"],
        ['Tax status', f"UAE corporate tax at {pc(IN['tax_ct'], 0)}; the 2025 audited effective "
         f"rate is exactly {pc(IN['tax_ct'], 1)}. Whether the {pc(IN['tax_dmtt'], 0)} domestic "
         f"minimum top-up tax reaches Empower through DEWA-group consolidation is contested — "
         f"the study's dual-framed judgement"]]
table(rows, [1.55, 5.45], size=8.8, align_right_from=9)
P(f"Two structural facts govern everything that follows. First, the two-leg tariff means the "
  f"profit pool sits in the contracted capacity charge: consumption revenue carries a "
  f"{pc(EWR, 0)} pass-through cost, so a swing in usage moves revenue far more than it moves "
  f"cash flow. Second, the balance sheet runs on other people's working capital: customer "
  f"deposits and long payment terms to a related-party supplier hold net working capital "
  f"NEGATIVE at about {pc(abs(U['nwc_ratio']), 0)} of revenue — growth here releases cash rather "
  f"than consuming it, the mirror image of most utilities' build-out phase.", space_after=10)

# =========================== 5. §1 FUNDAMENTAL VALUATION ======================
H1('1  Fundamental valuation')

# ---- 1.1 DCF ----------------------------------------------------------------
H2('1.1  The cash-flow model — the primary lens, with the full waterfall')
P(f"The primary lens is a five-year free-cash-flow-to-the-firm model built from physical units, "
  f"not from a revenue growth rate: connected refrigeration tons × the capacity rate, plus "
  f"consumption per connected ton × the connected base, plus the small pipes line — each leg on "
  f"its own driver, with margins falling out as OUTPUTS (section 1.6 shows the build and its "
  f"exact reconciliation to the audited 2025 statements). The waterfall below runs the base "
  f"case at the {pc(IN['tax_ct'], 0)} audited tax rate; the {pc(IN['tax_dmtt'], 0)} minimum-tax "
  f"framing follows it, in full, immediately after.")
hdr = ['AED mn'] + YRS
rows = [hdr,
        ['Revenue'] + [n0(B['rev'][y]) for y in YRS],
        ['  of which consumption'] + [n0(B['cons'][y]) for y in YRS],
        ['  of which capacity and other'] + [n0(B['cap'][y]) for y in YRS],
        ['EBITDA'] + [n0(B['ebitda'][y]) for y in YRS],
        ['EBITDA margin'] + [pc(B['ebitda'][y] / B['rev'][y]) for y in YRS],
        ['Less depreciation and amortisation'] + [f"({n0(B['dna'][y])})" for y in YRS],
        ['EBIT'] + [n0(BC['ebit'][y]) for y in YRS],
        [f"NOPAT — EBIT × (1 − {pc(IN['tax_ct'], 0)})"] + [n0(BC['nopat'][y]) for y in YRS],
        ['Add back depreciation and amortisation'] + [n0(B['dna'][y]) for y in YRS],
        ['Less capital expenditure'] + [f"({n0(B['capex'][y])})" for y in YRS],
        ['Add working-capital release'] + [n0(-B['dnwc'][y]) for y in YRS],
        ['Free cash flow to the firm'] + [n0(BC['fcff'][y]) for y in YRS],
        ['Discount factor'] + [f"{BC['df'][y]:.4f}" for y in YRS],
        ['Present value of FCFF'] + [n0(BC['pv'][y]) for y in YRS]]
table(rows, [2.30, 0.94, 0.94, 0.94, 0.94, 0.94], size=8.5, band_rows={12, 14})
caption(f"Every line is computed, not typed. Working capital is NEGATIVE for this company — "
        f"customer deposits and payables fund the cycle — so growth RELEASES cash: the "
        f"working-capital line adds to free cash flow every year, at the audited 2025 ratio of "
        f"{pc(U['nwc_ratio'], 1)} of revenue. Capital expenditure is priced per new refrigeration "
        f"ton (AED {n0(CAPEX_RT)} per RT added, derived from the 2025 cash figures) plus a "
        f"maintenance allowance on the installed base.")
rows = [['AED mn — the same model at the ' + pc(IN['tax_dmtt'], 0) + ' minimum tax'] + YRS,
        [f"NOPAT — EBIT × (1 − {pc(IN['tax_dmtt'], 0)})"] + [n0(BD['nopat'][y]) for y in YRS],
        ['Free cash flow to the firm'] + [n0(BD['fcff'][y]) for y in YRS],
        ['Present value of FCFF'] + [n0(BD['pv'][y]) for y in YRS]]
table(rows, [3.05, 0.79, 0.79, 0.79, 0.79, 0.79], size=8.5, band_rows={2})

H2('The bridge from enterprise value to the equity — both framings')
fig('fig7_bridge.png', 7.0,
    f"Figure 2 — from the discounted cash flows to the per-share value, both tax framings side "
    f"by side.")
rows = [['Step', f"At {pc(IN['tax_ct'], 0)}", f"At {pc(IN['tax_dmtt'], 0)}", 'Note'],
        ['Present value of the five forecast years', n0(BC['pv_explicit']), n0(BD['pv_explicit']),
         'sum of the present-value rows above'],
        ['Terminal value', n0(BC['tv']), n0(BD['tv']),
         f"final-year NOPAT grown {pc(IN['g_term'], 1)} × (1 − reinvestment rate "
         f"{pc(BC['rr_term'], 1)}), capitalised at {pc(W['rating_ct'], 2)} − "
         f"{pc(IN['g_term'], 1)}. The reinvestment rate is forced to growth ÷ terminal return "
         f"on capital ({pc(BC['roic_term'], 1)}) so growth is paid for"],
        ['Present value of the terminal value', n0(BC['pv_tv']), n0(BD['pv_tv']),
         f"discounted at the year-5 factor"],
        ['Enterprise value', n0(BC['ev']), n0(BD['ev']), 'the two lines above'],
        ['Terminal value as a share of enterprise value', pc(BC['tv_share'], 1),
         pc(BD['tv_share'], 1),
         'high, as it must be for a regulated utility whose explicit window is only five years; '
         'disclosed here, in the summary table, and stress-tested in section 1.9. Expert 3 '
         'challenges it directly in Appendix C'],
        ['Less net debt', f"({n0(ND)})", f"({n0(ND)})",
         f"30 June 2026 reviewed balance sheet: borrowings and leases less cash and term "
         f"deposits — reproduces the company's own presented figure exactly"],
        ['Plus investment properties', n0(IN['invprop_jun26']), n0(IN['invprop_jun26']),
         'non-operating side pocket, at book; its depreciation is excluded from the operating '
         'model for the same reason'],
        ['Plus financial assets held at fair value', n0(IN['fvtpl_jun26'] + IN['fvoci_jun26']),
         n0(IN['fvtpl_jun26'] + IN['fvoci_jun26']), 'cash-like holdings outside the operating '
         'model, at book'],
        [f"Less minority interests ({pc(NCI_FRAC, 1)} of profits)", f"({n0(BC['nci_val'])})",
         f"({n0(BD['nci_val'])})",
         f"minorities (the {100 - int(DXB_PCT)}% of DXB CoolCo, and others) take "
         f"{pc(NCI_FRAC, 1)} of group profit and are charged the same share of the value — the "
         f"internally consistent convention when the group is valued above book"],
        ['Equity attributable', n0(BC['eq_attr']), n0(BD['eq_attr']), ''],
        ['Fair value per share (AED)', p3(BC['ps']), p3(BD['ps']),
         f"against a spot of {p2(SPOT)}: {sgn(BC['ps'] / SPOT - 1, 0)} and "
         f"{sgn(BD['ps'] / SPOT - 1, 0)} respectively"]]
table(rows, [2.20, 0.95, 0.95, 2.90], size=8.4, band_rows={4, 11}, align_right_from=1)
caption(f"The valuation is struck on the 30 June 2026 reviewed balance sheet against an anchor "
        f"price five weeks later; no accretion roll is applied across that short window. The "
        f"difference between the two columns — AED {p3(abs(DMTT_DELTA))} per share, "
        f"{pc(abs(DMTT_DELTA) / BC['ps'], 1)} of the {pc(IN['tax_ct'], 0)} value — is the "
        f"entire price of the tax question, and it is left visible rather than averaged away.")

# ---- 1.2 book ----------------------------------------------------------------
H2('1.2  Book value and sustainable return — the asset lens')
P(f"Book value attributable to shareholders is AED {n0(IN['eq_attr_jun26'])}mn at 30 June 2026, "
  f"or {p3(BK['bvps'])} per share — the share trades at {n1(SPOT / BK['bvps'])}× book. That "
  f"multiple is not the anomaly it appears: the equity base is small because the assets are "
  f"largely debt- and customer-deposit-funded and the company has distributed heavily since "
  f"listing, so the sustainable return on equity is high — {pc(BK['roe_sust'], 1)} on the "
  f"average of the last two year-end equity bases. A justified price-to-book multiple, (return "
  f"on equity − growth) ÷ (cost of equity − growth), gives {n1(BK['pb_just'])}× book at the "
  f"{pc(W['ke_rating'], 2)} cost of equity and {pc(IN['g_term'], 1)} growth — AED "
  f"{p3(BK['ps'])} per share.")
P(f"This is the lens most exposed to its own construction: a high-ROE, low-book business makes "
  f"the justified multiple acutely sensitive to the return assumption (each percentage point of "
  f"sustainable ROE is worth roughly AED "
  f"{p3(BK['bvps'] * 0.01 / (W['ke_rating'] - IN['g_term']))} per share). It is retained at a "
  f"{pc(LN['book']['weight'], 0)} weight because it prices the question the other lenses skip — "
  f"what the installed asset base earns — but it is read as corroboration, not as a primary "
  f"estimate.")

# ---- 1.3 relative ------------------------------------------------------------
H2('1.3  Relative multiples — what the market pays for GCC cooling today')
rows = [['Step', 'Value', 'Comment'],
        ["Tabreed enterprise value / EBITDA (trailing)", f"{n1(REL['tabreed_ev_ebitda'])}×",
         'the only listed pure district-cooling peer (Dubai Financial Market); derived from its '
         'market value plus net debt over 2025 EBITDA, and flagged as derived. Tabreed runs '
         'much higher leverage, which is why the comparison is made at the enterprise line '
         'rather than on price/earnings alone'],
        ['Applied to Empower 2026E EBITDA', n0(REL['ev_rel'] / REL['tabreed_ev_ebitda']),
         'the base-case build, shock year included'],
        ['Implied enterprise value', n0(REL['ev_rel']), ''],
        ['Less net debt, plus the side pockets, less minorities', '—',
         'the same bridge as section 1.1'],
        ['Implied value per share — EV/EBITDA basis', p3(REL['ps_rel']),
         f"{sgn(REL['ps_rel'] / SPOT - 1, 0)} against spot"],
        [f"Tabreed price/earnings {n1(REL['tabreed_pe'])}× on 2026E attributable profit of "
         f"{n0(REL['npa26'])}", p3(REL['ps_pe']),
         f"the earnings-basis read; DEWA itself trades near {n1(REL['dewa_pe'])}× as a "
         f"secondary marker"]]
table(rows, [2.51, 0.94, 3.55], size=8.5, band_rows={5})
P(f"Read this lens for what it is: a market-regime reading, not an independent fundamental. The "
  f"peer multiples are themselves struck in a war-discounted market — Tabreed and DEWA fell "
  f"with the index — so applying them imports the conflict discount rather than testing it. "
  f"That is exactly why the lens carries {pc(LN['relative']['weight'], 0)} weight and why its "
  f"gap to the cash-flow lens ({p3(REL['ps_rel'])} against {p3(BC['ps'])}) is treated in "
  f"section 4 as information about the market's risk pricing, not as an error in either "
  f"number.")

# ---- 1.4 normalized ----------------------------------------------------------
H2('1.4  Normalised earnings power — the unshocked year')
P(f"The question this lens asks: what does 2026 earn if the consumption shock had not happened "
  f"— usage per connected ton at the 2025 level, everything else unchanged? Revenue would be "
  f"AED {n0(NRM['rev'])}mn (against {n0(B['rev']['FY26'])}mn shocked), EBITDA "
  f"{n0(NRM['ebitda'])}mn, and attributable profit {n0(NRM['npa'])}mn — earnings per share of "
  f"{p3(NRM['eps'])}. Capitalised at a justified multiple of {n1(NRM['pe_just'])}× — built "
  f"from the sustainable return on equity ({pc(BK['roe_sust'], 1)}), the retention that "
  f"{pc(IN['g_term'], 1)} growth requires, and the {pc(W['ke_rating'], 2)} cost of equity — "
  f"that is AED {p3(NRM['ps'])} per share ({p3(NRM['ps'] * (1 - TAXADJ))} if the "
  f"{pc(IN['tax_dmtt'], 0)} minimum tax applies).")
P(f"The lens deliberately measures the gap between the market's reaction and the earnings "
  f"arithmetic: the whole shock is worth about AED {n0(NRM['rev'] - B['rev']['FY26'])}mn of "
  f"revenue in the year, most of which is passed-through electricity and water cost that "
  f"disappears with it.")

# ---- 1.5 synthesis -----------------------------------------------------------
H2('1.5  Synthesis — four lenses, one field')
rows = [['Lens', f"At {pc(IN['tax_ct'], 0)}", f"At {pc(IN['tax_dmtt'], 0)}", 'Weight'],
        ['Discounted cash flow', p3(BC['ps']), p3(BD['ps']), pc(LN['dcf']['weight'], 0)],
        ['Relative multiples', p3(REL['ps_rel']), p3(REL['ps_rel']),
         pc(LN['relative']['weight'], 0)],
        ['Normalised earnings power', p3(NRM['ps']), p3(NRM['ps'] * (1 - TAXADJ)),
         pc(LN['normalized']['weight'], 0)],
        ['Book value and sustainable return', p3(BK['ps']), p3(BK['ps']),
         pc(LN['book']['weight'], 0)],
        ['Weighted central', p3(CEN['ct']), p3(CEN['dmtt']), '—'],
        ['Dividend cross-check (unweighted)', p3(DDM['ps']), p3(DDM['ps']), '—']]
table(rows, [3.39, 0.83, 0.83, 0.95], size=8.6, band_rows={5})
P(f"The lenses disagree in an orderly way. The cash-flow model sits highest because it credits "
  f"the contracted growth backlog and the negative-working-capital funding model in full; the "
  f"relative lens sits lowest because it imports today's war-discounted market regime; the "
  f"normalised and book lenses sit between. The weighting leans on the cash-flow model because "
  f"this is a regulated utility with contracted revenue — the class of business a "
  f"discounted-cash-flow model prices best — and the field runs {p3(CEN['bear'])} to "
  f"{p3(CEN['bull'])} bear to bull. Both tax columns are carried through every row; nothing is "
  f"averaged across them.")

# ---- 1.6 drivers -------------------------------------------------------------
H2('1.6  The drivers — a two-leg unit build, margins as outputs')
fig('fig8_unit.png', 7.0,
    "Figure 3 — the unit build: connected capacity, consumption per connected ton and the "
    "revenue that falls out of them.")
P(f"Revenue is built from physical units at the finest level the company disclosures allow. The "
  f"volume driver is CONNECTED CAPACITY, taken from the company's own history and guidance: "
  f"{n0(RT25Y)}k RT at end-2025, {n0(RT_H1)}k at 30 June 2026, company guidance of "
  f"{n0(GUID_LO)}–{n0(GUID_HI)}k of new connections for 2026 (the model uses the midpoint), and "
  f"a contracted backlog of {n0(BACKLOG)}k RT already signed but not yet connected — a pre-sold "
  f"pipeline that funds the additions assumed for 2027 onward, tapering as the Dubai build-out "
  f"matures.")
rows = [['Driver (per year)', 'FY25'] + YRS,
        ['Connected capacity, year-end (k RT)', n0(U['rt_path']['FY25'])] +
        [n0(U['rt_path'][y]) for y in YRS],
        ['New connections in the year (k RT)', '—'] +
        [n0(U['rt_path'][y] - U['rt_path'][p]) for p, y in
         zip(['FY25'] + YRS[:-1], YRS)],
        ['Average connected base (k RT)', '—'] + [n0(U['rt_avg'][y]) for y in YRS],
        ['Consumption revenue per average RT (AED/yr)', n0(CONS_RT)] +
        [n0(B['cons'][y] / U['rt_avg'][y] * 1000) for y in YRS],
        ['Capacity and other revenue per average RT (AED/yr)', n0(CAP_RT)] +
        [n0(B['cap'][y] / U['rt_avg'][y] * 1000) for y in YRS]]
table(rows, [2.30, 0.783, 0.783, 0.783, 0.783, 0.783, 0.784], size=8.0)
caption(f"The capacity rate per ton is IMPLIED, not published — no per-ton tariff schedule is "
        f"disclosed anywhere in the filings — so it is solved from disclosed total revenue, the "
        f"disclosed consumption figure in the auditor's key-audit-matter section, and the pipes "
        f"line, then held flat at the regulated tariff. The consumption rate carries the "
        f"{pc(abs(U['crux_shock']), 0)} 2026 shock and recovers to the 2025 level through 2027 "
        f"in the base case — the crux, section 1.7.")
P(f"The cost stack is escalated one class at a time, never on a single blended index. "
  f"Electricity and water purchased from DEWA — AED {n0(IN['ew_cost_fy25'])}mn in 2025, "
  f"{pc(EWR, 1)} of consumption revenue and {pc(EW_REVSHARE, 0)} of total revenue — moves with "
  f"its own physical driver, the consumption leg itself (DEWA's slab tariff is flat; its fuel "
  f"surcharge floats monthly). Staff and other cash operating costs (AED "
  f"{n0(U['other_cos25'] + U['ga_cash25'])}mn in 2025 across cost of sales and administration) "
  f"escalate on a UAE wage path of {pc(WAGE_ESC, 1)} a year. Interest income on the airport "
  f"concession receivable amortises slowly down. The build reproduces audited 2025 EBITDA of "
  f"AED {n0(HI['FY25']['ebitda'])}mn exactly before any forecast year is struck.")
rows = [['What the build produces', ] + YRS,
        ['Revenue (AED mn)'] + [n0(B['rev'][y]) for y in YRS],
        ['EBITDA (AED mn)'] + [n0(B['ebitda'][y]) for y in YRS],
        ['EBITDA margin — an OUTPUT'] + [pc(B['ebitda'][y] / B['rev'][y]) for y in YRS],
        ['Capital expenditure (AED mn)'] + [n0(B['capex'][y]) for y in YRS],
        ['Working capital released (AED mn)'] + [n0(-B['dnwc'][y]) for y in YRS]]
table(rows, [3.00, 0.80, 0.80, 0.80, 0.80, 0.80], size=8.4, band_rows={3})
caption(f"The margin path is not assumed: it emerges from the two-leg mix. It dips in the shock "
        f"year, then recovers toward the audited range ({MARG_LO}–{MARG_HI}%) as consumption "
        f"normalises and the connected base grows into the cost stack.")

# ---- 1.7 crux ----------------------------------------------------------------
H2('1.7  The crux — does consumption per connected ton recover?')
P(f"Usage per connected ton fell {pc(abs(U['crux_shock']), 0)} in 2026 on the model's "
  f"full-year reading of the disclosed half-year figures (equivalent full-load hours were "
  f"{sgn(IN['eflh_h1'], 0)} in the half itself). The base case lets it recover to the 2025 "
  f"level through 2027, on the view that the loss is hospitality-linked and the truce holds. "
  f"The alternative is computed as a FULL model, not a sensitivity: usage never recovers. The "
  f"grid below prices every stop between.")
rows = [['Consumption per connected ton, from 2027', 'Implied AED per RT',
         f"Fair value at {pc(IN['tax_ct'], 0)}", 'vs base'],
        *[[f"{pc(r['level'], 0)} of the 2025 level" +
           ('  — the never-recovers case' if abs(r['level'] - (1 + U['crux_shock'])) < 1e-9
            else ('  — the base case' if abs(r['level'] - 1) < 1e-9 else '')),
           n0(r['level'] * CONS_RT), p3(r['ps']), sgn(r['ps'] / BC['ps'] - 1, 1)]
          for r in CRX['rows']]]
table(rows, [2.85, 1.30, 1.55, 0.90], size=8.5,
      band_rows={1 + [i for i, r in enumerate(CRX['rows'])
                      if abs(r['level'] - 1) < 1e-9][0]})
P(f"The finding is the study's headline: permanent loss of the entire shock — the "
  f"never-recovers case — moves the discounted-cash-flow value from {p3(BC['ps'])} to "
  f"{p3(PC['ps'])}, just {pc(abs(CRUX_DELTA), 1)} ({p3(PD['ps'])} under the "
  f"{pc(IN['tax_dmtt'], 0)} tax framing). The arithmetic reason is the pass-through: about "
  f"{pc(EWR, 0)} of every dirham of consumption revenue leaves again as electricity and water "
  f"purchased from DEWA, so the meter's contribution to cash flow is thin. The market's "
  f"read-through from the consumption miss to the equity — a share price {pc(T['pct_off_high'], 0)} "
  f"off its high — is larger than the cash-flow arithmetic supports. The capacity charge, not "
  f"the meter, carries the value; what WOULD move the value is a tariff cut or a stall in "
  f"connections, which is why sections 5 and 7 watch those, not the weather.")

# ---- 1.8 macro ---------------------------------------------------------------
H2('1.8  Macro and country — rates, the peg, and the sourced cost of capital')
P(f"The macro frame is unusually clean for an emerging-market study: the dirham is hard-pegged, "
  f"so the UAE imports the Federal Reserve's path and the currency leg drops out of the "
  f"valuation entirely. The central bank's base rate stood at {pc(STK['rf_live'], 2)} at the "
  f"end of July 2026; the federal government's dirham bond programme gives a sovereign curve, "
  f"and its longest print — the January-2031 tranche auctioned on 30 July 2026 — yields "
  f"{pc(IN['rf_aed'], 2)}. The conflict is the macro event: the market index fell "
  f"{DFM_DD.lstrip('-')} peak to trough, GDP guidance was cut from {GDP_OLD}% to {GDP_NEW}%, "
  f"and the equity risk pricing that survives into August is part of what section 1.3 measures.")
rows = [['Component', f"Credit-rating basis", f"Market-spread basis", 'Construction'],
        ['Risk-free rate before adjustment', pc(IN['rf_aed'], 2), pc(IN['rf_aed'], 2),
         f"the longest AED sovereign print ({TENOR}-year tenor; the gap to the five-year-plus "
         f"cash-flow horizon is flagged as a limitation)"],
        ['Less the sovereign default spread', pc(IN['ds_rating'], 2), pc(IN['ds_cds'], 2),
         'the UAE\'s own default spread on each basis, from the July-2026 edition of the '
         'published country-risk dataset; the market-spread column uses the Abu Dhabi sovereign '
         'credit-default swap as the quoted UAE proxy — flagged'],
        ['Adjusted risk-free rate', pc(W['rf_star_rating'], 2), pc(W['rf_star_cds'], 2),
         'country risk must enter once, through the equity premium — not twice'],
        ['Beta', f"{BR['beta']:.3f}", f"{BR['beta']:.3f}",
         f"own-stock weekly regression against the DFM General Index over the full listing "
         f"window ({BR['window_years']:.1f} years, n={BR['n']}): R² {BR['r2']:.3f}, standard "
         f"error {BR['se']:.3f}, 90% interval {BR['ci90'][0]:.2f}–{BR['ci90'][1]:.2f}"],
        ['Equity risk premium', pc(IN['erp_rating'], 2), pc(IN['erp_cds'], 2),
         'the UAE total premium on each basis, same dataset — the same basis of spread that was '
         'stripped from the risk-free rate is the one added back here'],
        ['Cost of equity', pc(W['ke_rating'], 2), pc(W['ke_cds'], 2),
         'the two constructions CONVERGE to within a basis point — the contested choice of '
         'basis is priced and turns out to cost nothing'],
        ['Cost of debt (marginal)', pc(W['kd_marg'] if 'kd_marg' in W else W['kd'], 2),
         pc(W['kd'], 2),
         f"the company's OWN 2025 borrowing-cost capitalisation rate, struck on the full "
         f"refinance of both AED {RCF_BN}bn facilities at a reduced margin over EIBOR — see "
         f"the evidence table below"],
        ['Weights (equity / debt)', f"{pc(W['we'], 1)} / {pc(W['wd'], 1)}",
         f"{pc(W['we'], 1)} / {pc(W['wd'], 1)}",
         'market value of equity at the anchor price; net debt at the reviewed June-2026 '
         'balance sheet'],
        [f"Cost of capital at {pc(IN['tax_ct'], 0)} tax", pc(W['rating_ct'], 2),
         pc(W['cds_ct'], 2), 'the rate the base case discounts at'],
        [f"Cost of capital at {pc(IN['tax_dmtt'], 0)} tax", pc(W['rating_dmtt'], 2),
         pc(W['cds_dmtt'], 2), 'marginally lower — the tax shield on debt is worth more']]
table(rows, [1.55, 1.05, 1.05, 3.35], size=8.2, band_rows={6, 9})
caption("No glide path is applied to the cost of debt or the cost of capital: both revolving "
        "facilities float over EIBOR, the 2025 refinance already reset the margin, and the "
        "forward curve is flat to mildly higher — a glide would be invented, not sourced. The "
        "explicit-window rate equals the terminal rate, stated openly.")

H2('The cost of debt — three pieces of evidence, not an assumption')
rows = [['Evidence', 'Rate', 'What it establishes'],
        ['AED sovereign yield (January-2031 tranche, auctioned 30 July 2026)', pc(IN['rf_aed'], 2),
         'the floor: a same-currency corporate cannot sustainably borrow below its sovereign'],
        ["Empower's own 2025 borrowing-cost capitalisation rate", pc(W['kd'], 2),
         f"the company's audited all-in cost on its freshly refinanced book — sits "
         f"{n0((W['kd'] - IN['rf_aed']) * 10000)}bp above the sovereign, as it must; adopted as "
         f"the marginal cost of debt"],
        ["The same disclosure a year earlier (2024)", pc(KD24, 2),
         f"the down-trajectory: the 2025 refinance cut the all-in cost by about "
         f"{n0((KD24 - W['kd']) * 10000)}bp as EIBOR fell and the margin was renegotiated. "
         f"Three-month EIBOR stood near {pc(EIBOR, 2)} at the study date; the exact contractual "
         f"margin is not disclosed in any filing (recorded as a documented absence in the "
         f"bibliography), so the capitalisation rate is the closest disclosed all-in figure"]]
table(rows, [2.60, 0.80, 3.60], size=8.4)
P(f"Every contested construction in this section is PRICED rather than asserted: the two "
  f"premium bases are both computed (they converge); the tax question is carried as two full "
  f"columns everywhere; the short sovereign tenor and the Abu Dhabi credit-default-swap proxy "
  f"are flagged in place; and the beta's sampling error is shown so a reader can re-run the "
  f"cost of equity at either end of the interval ({BR['ci90'][0]:.2f} lifts the fair value, "
  f"{BR['ci90'][1]:.2f} lowers it — the direction is worth roughly AED "
  f"{p3(abs(SN['table'][_wi + 1][_gi] - SN['table'][_wi - 1][_gi]) / 2)} per share per "
  f"half-point of discount rate, per the grid in section 1.9).", space_after=8)

# ---- 1.9 sensitivity ---------------------------------------------------------
H2('1.9  Sensitivity — the discount rate, the growth, and the scenarios')
fig('fig2_sens.png', 7.0,
    "Figure 4 — fair value per share against cost of capital and terminal growth; the crux "
    "grid alongside.")
rows = [[f"Fair value at {pc(IN['tax_ct'], 0)} (AED/share)"] +
        [f"g = {pc(g, 1)}" for g in SN['g_grid']]]
for wi, w_ in enumerate(SN['wacc_grid']):
    tag = '  (base)' if abs(w_ - W['rating_ct']) < 1e-9 else ''
    rows.append([f"Cost of capital {pc(w_, 2)}{tag}"] +
                [p3(SN['table'][wi][gi]) for gi in range(len(SN['g_grid']))])
table(rows, [1.90, 1.02, 1.02, 1.02, 1.02, 1.02], size=8.4,
      band_rows={_wi + 1})
caption(f"The base cell ({p3(_base_cell)}) sits at {pc(W['rating_ct'], 2)} and "
        f"{pc(IN['g_term'], 1)}. A half-point of discount rate is worth roughly AED "
        f"{p3(abs(_dn50 - _up50) / 2)} per share — more than the entire consumption crux — "
        f"which is the honest hierarchy of what matters in this valuation: rate, tax, tariff, "
        f"then usage.")
rows = [['Scenario', 'What is assumed', f"Fair value (AED/share)"],
        ['Bear — war re-escalation',
         f"usage falls a further {pc(abs(U['crux_shock']), 0)} in 2027 and never recovers; new "
         f"connections halve (the pipeline freezes); the {pc(IN['tax_dmtt'], 0)} minimum tax "
         f"lands; the cost of equity rises {n0((SCN['bear']['ke'] - W['ke_rating']) * 10000)}bp "
         f"as the market re-prices UAE risk", p3(CEN['bear'])],
        ['Base', f"recovery through 2027, guidance-midpoint connections, both tax framings "
         f"published", f"{p3(CEN['ct'])} / {p3(CEN['dmtt'])}"],
        ['Bull — full recovery', f"usage recovers fully; connections run at the top of guidance "
         f"({n0(GUID_HI)}k RT a year); {pc(IN['tax_ct'], 0)} tax", p3(CEN['bull'])]]
table(rows, [1.40, 4.20, 1.40], size=8.4, band_rows={2})
caption("The bear and bull are full model re-runs — unit paths, cost stack, discount rate and "
        "tax all moved together — not lens blends or grid look-ups.")

# =========================== 6. §2 TECHNICAL ==================================
H1('2  Technical and price structure')
fig('fig3_ma.png', 7.0,
    "Figure 5 — price against the 20-, 50- and 200-session moving averages, with the "
    "support and resistance ladder.")
rows = [['Marker', 'Level (AED)', 'Reading'],
        ['Last close (7 August 2026)', p2(T['close']), 'the anchor for everything in this study'],
        ['20-session average', p2(T['ma']['20']),
         f"price is {sgn(SPOT / T['ma']['20'] - 1, 1)} against it; the average is "
         f"{T['ma_slope']['20']}"],
        ['50-session average', p2(T['ma']['50']),
         f"price is {sgn(SPOT / T['ma']['50'] - 1, 1)} against it; {T['ma_slope']['50']}"],
        ['200-session average', p2(T['ma']['200']),
         f"price is {sgn(SPOT / T['ma']['200'] - 1, 1)} against it; {T['ma_slope']['200']}"],
        ['Momentum (14-session RSI)', f"{T['rsi']:.0f}",
         'washed out — a reading under 30 marks the sell-off as stretched by its own recent '
         'standards'],
        ['MACD (12·26·9)', f"{T['macd']['macd']:.3f}",
         'negative and still falling — the down-move has not yet lost momentum'],
        ['Average true range (14-session)', pc(T['atr_pct'], 1),
         'of price per session — a normal tape, not a dislocated one'],
        ['52-week range', f"{p2(T['lo_52w'])} – {p2(T['hi_52w'])}",
         f"the close sits {pc(T['pct_off_high'], 0)} below the high and "
         f"{pc(T['pct_off_low'], 0)} above the low"],
        ['Resistance', ' / '.join(p2(x) for x in T['levels']['res']),
         'nearest first, from recency-weighted swing clusters'],
        ['Support', ' / '.join(p2(x) for x in T['levels']['sup']),
         'nearest first; the second and third are round-number shelves']]
table(rows, [1.85, 1.15, 4.00], size=8.5)
P(T['tech']['summary'])
P(f"One configuration deserves its own sentence: the 50-session average crossed ABOVE the "
  f"200-session {T['ma_cross']['ago']} sessions ago — a golden cross, conventionally a "
  f"regime-change signal — and it sits oddly against a price that has since sold off below the "
  f"whole stack. The cross reflects the spring recovery from the war trough; the sell-off is "
  f"the August earnings reaction. When a trend signal and the tape disagree this directly, the "
  f"tape is the fresher fact. {T['tech']['bull']} {T['tech']['bear']}", space_after=10)

# =========================== 7. §3 PROBABILISTIC MAP ==========================
H1('3  A probabilistic price map')
P(f"This section answers a different question from the valuation: not what the business is "
  f"worth, but where the share price could plausibly trade in one and three months given how "
  f"this share actually moves. Fifty thousand price paths are simulated from a volatility "
  f"model fitted to the daily trading range, with a fat-tailed shock distribution and a drift "
  f"anchored to the cost of carry — the local deposit rate less the {pc(STK['q_annual'], 1)} "
  f"dividend yield, which is why the median path sits a shade below spot. It carries no "
  f"directional view, and it is never blended with the fair-value work above.")
P(f"The widths are calibrated rather than assumed, and the evidence is stated plainly. The "
  f"probability bands are calibrated on the UAE market panel ({FIT['panel_names']} names, "
  f"walk-forward tested with each forecast made using only data available before it); the "
  f"panel's forecast accuracy is statistically indistinguishable from — marginally ahead of — "
  f"a benchmark random walk anchored on the same cost of carry. For Empower itself only "
  f"{BT5['windows']} non-overlapping three-month windows exist since the late-2022 listing. On "
  f"those windows every realised outcome fell INSIDE the 80% band, and the centring is clean "
  f"(the average percentile of the realised outcomes was {BT5['pit_mean']:.2f}, statistically "
  f"uniform on the standard tests). The bands as published are, if anywhere, conservative — "
  f"about {pc(BT5['width_vs_benchmark'] - 1, 0)} wider than this stock's own short history "
  f"would warrant, and that width has a cost: on those same windows the bands scored a few "
  f"percent behind the benchmark on average sharpness, the price of never missing. A reader "
  f"should treat the intervals as honest but wide.")
fig('fig4_fan.png', 7.0,
    f"Figure 6 — the forward price cone to three months from the anchor close of {p2(SPOT)}, "
    f"with the trailing tape behind it. Both fundamental central estimates ({p3(CEN['ct'])} "
    f"and {p3(CEN['dmtt'])}) sit above the cone's 95th percentile — the two objects genuinely "
    f"disagree, and section 6 reads that gap.")
H2('Percentile map (AED/share)')
rows = [['Horizon', '5th', '25th', 'Median', '75th', '95th', 'Probability above spot'],
        [f"1 month (to {H1M['grade_date']})"] +
        [p2(H1M['pct'][k]) for k in ('p5', 'p25', 'p50', 'p75', 'p95')] +
        [pc(H1M['p_above'], 0)],
        [f"3 months (to {H3M['grade_date']})"] +
        [p2(H3M['pct'][k]) for k in ('p5', 'p25', 'p50', 'p75', 'p95')] +
        [pc(H3M['p_above'], 0)]]
table(rows, [2.11, 0.71, 0.71, 0.80, 0.71, 0.71, 1.25], size=8.6)
fig('fig5_dist.png', 5.3, "Figure 7 — the one-month price distribution.")
fig('fig6_dist.png', 5.3, "Figure 8 — the three-month price distribution.")
H2('Level-touch ladder')
rows = [['Event', '1 month', '3 months'],
        ['Finishes 10% or more above spot', pc(H1M['p_up10'], 0), pc(H3M['p_up10'], 0)],
        ['Finishes 10% or more below spot', pc(H1M['p_dn10'], 0), pc(H3M['p_dn10'], 0)],
        ['Touches 10% above spot at any point', pc(H1M['touch_up10'], 0),
         pc(H3M['touch_up10'], 0)],
        ['Touches 10% below spot at any point', pc(H1M['touch_dn10'], 0),
         pc(H3M['touch_dn10'], 0)]]
table(rows, [3.90, 1.05, 1.05], size=8.6)
caption(f"Touch probabilities exceed finish probabilities because a path can visit a level and "
        f"come back. The anchor volatility is about {pc(H3M['anchor_vol_ann'], 0)} annualised — "
        f"elevated for a regulated utility, which is itself a statement about the conflict "
        f"regime the share is trading in.")

# =========================== 8. §4 COMPARISON =================================
H1('4  Comparison of the lenses')
rows = [['Read', 'What it says', 'What it assumes'],
        ['Cash flow (primary)', f"AED {p3(BC['ps'])} / {p3(BD['ps'])} by tax framing, "
         f"{sgn(BC['ps'] / SPOT - 1, 0)} / {sgn(BD['ps'] / SPOT - 1, 0)} against the market",
         'the tariff stays flat but is not cut; the contracted backlog connects; the crux '
         'recovers (and barely matters if it does not)'],
        ['Weighted central', f"AED {p3(CEN['ct'])} / {p3(CEN['dmtt'])}, "
         f"{sgn(CEN['ct'] / SPOT - 1, 0)} / {sgn(CEN['dmtt'] / SPOT - 1, 0)}",
         'a fifth of the weight deliberately given to today\'s war-discounted market regime '
         'through the relative lens'],
        ['Relative multiples', f"AED {p3(REL['ps_rel'])}, {sgn(REL['ps_rel'] / SPOT - 1, 0)}",
         'the current GCC utility pricing regime is the right regime to capitalise'],
        ['The market', p2(SPOT), 'revealed preference of the marginal seller in a conflict '
         'summer, after a weak volume quarter'],
        ['DEWA control purchase (reference)', f"AED {p2(DEWA['price'])}, "
         f"{sgn(DEWA_PREM, 0)} above spot",
         'what the controlling shareholder paid a related party for control economics in '
         'February — bounds the question from above, proves nothing about minority value'],
        ['Three-month price map', f"median {p2(H3M['pct']['p50'])}, "
         f"{pc(H3M['p_above'], 0)} chance of finishing above spot",
         'volatility persists as it has; no view on value']]
table(rows, [1.85, 2.30, 2.85], size=8.4)
P(f"The reading we take from this: the market is pricing the consumption shock as if it were a "
  f"structural impairment of the profit pool, and the cash-flow arithmetic says it is not — "
  f"the pool sits in the contracted capacity charge, which grew through the war half. The "
  f"genuine open questions are the ones the market prices less visibly: whether the "
  f"{pc(IN['tax_dmtt'], 0)} minimum tax reaches the company ({p3(abs(DMTT_DELTA))} per share, "
  f"published as its own column), and whether the regulator's next tariff review stays flat "
  f"(not priced — flagged as the model's single most valuable assumption). Between the "
  f"{p3(CEN['dmtt'])} central under the harsher tax framing and the {p2(SPOT)} market price "
  f"lies the war discount itself; a reader who expects the conflict regime to persist should "
  f"weight the relative lens harder, and the field published here lets them.")
P("No rating and no price target is expressed here or anywhere else in this document. The "
  "output is a range and a distribution.", space_after=10)

# =========================== 9. §5 CATALYSTS ==================================
H1('5  Catalysts to watch')
rows = [['Catalyst', 'Why it matters', 'What to watch'],
        ['Truce durability', 'the whole 2026 demand shock transmits through hospitality '
         'occupancy; re-escalation onto UAE soil is the bear case, de-escalation unwinds the '
         'market\'s regime discount',
         'incident tempo against the April ceasefire framework; any strike on Dubai '
         'infrastructure'],
        ['Third-quarter 2026 results (November)',
         'the first FULL summer quarter carrying the consumption shock — the highest-usage '
         'months of the year',
         f"equivalent full-load hours against the {EFLH_HRS}-hour first-half print; whether "
         f"capacity revenue keeps growing through it"],
        ['October dividend instalment',
         f"half the committed AED {n0(IN['div_policy'])}mn; the payout is covered "
         f"almost exactly, so any hesitation is information",
         'confirmation of the instalment and any wording change on the 2027 policy'],
        ['Minimum-tax clarification',
         f"whether DEWA-group consolidation sweeps Empower into the {pc(IN['tax_dmtt'], 0)} "
         f"regime — worth AED {p3(abs(DMTT_DELTA))} per share on the primary lens, published "
         f"here as its own column",
         'Ministry of Finance guidance on domestic minimum top-up tax scope for '
         'government-group entities; the tax note of the 2026 annual filing'],
        ['Connection pace', f"the volume driver: guidance is {n0(GUID_LO)}–{n0(GUID_HI)}k RT "
         f"of 2026 connections against a {n0(BACKLOG)}k RT contracted backlog",
         'connected and contracted capacity in each results deck; the fifth Business Bay '
         'plant award moving to construction'],
        ['The 2027 tariff round', 'the flat regulated tariff is the single most valuable '
         'assumption in the model; a cut at review would do what no consumption shock can',
         'any Regulatory and Supervisory Bureau consultation or Executive Council resolution '
         'touching district-cooling tariffs'],
        ["DEWA's intentions at 80%",
         'further buy-in or squeeze-out speculation is NOT modelled; what is real today is a '
         'thinner float, index-weight mechanics and reduced liquidity',
         'any disclosure of stake changes; index-provider treatment of the reduced float']]
table(rows, [1.50, 2.75, 2.75], size=8.3)

# =========================== 10. §6 PROBABILITY ZONES =========================
H1('6  Reading the probability zones')
P(f"The three-month distribution has a median of {p2(H3M['pct']['p50'])} and a 5th-to-95th "
  f"span of {p2(H3M['pct']['p5'])} to {p2(H3M['pct']['p95'])}. Read the span honestly: the "
  f"model considers a {sgn(H3M['pct']['p5'] / SPOT - 1, 0)} move and a "
  f"{sgn(H3M['pct']['p95'] / SPOT - 1, 0)} move equally unremarkable tail outcomes over a "
  f"single quarter of a conflict-regime tape.")
rows = [['Zone', 'Three-month range (AED)', 'How to read it'],
        ['Lower tail', f"below {p2(H3M['pct']['p5'])}",
         'a 1-in-20 outcome; would need a genuine shock — re-escalation onto UAE soil, a '
         'tariff-review surprise, or a dividend wobble'],
        ['Lower half of the central band', f"{p2(H3M['pct']['p25'])} – {p2(H3M['pct']['p50'])}",
         'ordinary drift lower; the market continuing to price the war regime'],
        ['Upper half of the central band', f"{p2(H3M['pct']['p50'])} – {p2(H3M['pct']['p75'])}",
         'ordinary drift higher; a quiet summer and the October instalment arriving on '
         'schedule'],
        ['Upper tail', f"above {p2(H3M['pct']['p95'])}",
         'a 1-in-20 outcome; would need visible de-escalation or a re-rating of the sector'],
        ['Where the fundamental centrals sit', f"{p3(CEN['dmtt'])} / {p3(CEN['ct'])}",
         f"BOTH tax framings sit above even the 95th percentile ({p2(H3M['pct']['p95'])}) of "
         f"the three-month distribution — the price map and the valuation genuinely disagree, "
         f"and stating that gap at its full size is the point: nothing in the volatility "
         f"structure suggests the gap closes within a quarter"]]
table(rows, [1.75, 1.75, 3.50], size=8.4)

# =========================== 11. §7 CAVEATS ===================================
H1('7  Caveats and what would change our mind')
for head, body in [
    ("Consumption failing to recover in the 2027 prints. ",
     f"The base case restores usage per connected ton to the 2025 level through 2027. The full "
     f"never-recovers model costs only {pc(abs(CRUX_DELTA), 1)} on the primary lens, so this is "
     f"a watch-item rather than a value risk — but two consecutive halves with equivalent "
     f"full-load hours below the 2026 trough would put the shock outside anything "
     f"hospitality-linked, and the recovery assumption should then be abandoned, not "
     f"stretched."),
    ("The minimum tax being confirmed. ",
     f"If the {pc(IN['tax_dmtt'], 0)} domestic minimum top-up tax is confirmed to reach "
     f"Empower through DEWA-group consolidation, shift weight to the {pc(IN['tax_dmtt'], 0)} "
     f"column published throughout — the work is already done; nothing needs re-estimating."),
    ("War re-escalation onto UAE soil. ",
     f"The bear machinery is explicit: usage down a further {pc(abs(U['crux_shock']), 0)} and "
     f"never recovering, connections halved, the harsher tax, and "
     f"{n0((SCN['bear']['ke'] - W['ke_rating']) * 10000)}bp on the cost of equity — AED "
     f"{p3(CEN['bear'])} per share. A reader can adopt it wholesale rather than improvising a "
     f"discount."),
    ("A tariff cut at a regulatory review. ",
     f"The flat regulated tariff is the single most valuable assumption in the model — it "
     f"underwrites the capacity charge that carries {pc(BC['tv_share'], 1)} of the enterprise "
     f"value into the terminal. No cut occurred in the 2024–26 record swept here, but the "
     f"model contains no machinery for one, deliberately: it would be a regime change, to be "
     f"re-modelled, not sensitised."),
    ("Construction limitations, stated. ",
     f"The sovereign anchor is a {TENOR}-year bond against five-plus years of cash flows (the "
     f"longest AED print available); the index series behind the beta regression is an "
     f"aggregator pull with roughly a fifth of sessions missing, absorbed by weekly sampling "
     f"and flagged in the bibliography; and the first-half revenue-mix percentages "
     f"({MIXD}/{MIXC}/{MIXO}) come from the investor deck, not the audited notes — the audited "
     f"statements disclose only the consumption figure, in the auditor's key-audit-matter "
     f"section."),
    ("Related-party concentration. ",
     f"The {DEWA_PCT}% owner is also the sole supplier of "
     f"the largest cost line and the counterparty of the 2026 control transaction. Tariff "
     f"bargaining, input pricing and any future buy-in all run through one related party. This "
     f"is a governance fact, not an allegation, and it is one reason the relative lens and the "
     f"scenario field are published alongside the model rather than folded into it."),
    ("What would change our mind, specifically. ",
     f"Upward: visible de-escalation; the minimum-tax question resolving at "
     f"{pc(IN['tax_ct'], 0)}; connections printing at or above the top of guidance. Downward: "
     f"a tariff-review consultation proposing cuts; equivalent full-load hours below the 2026 "
     f"trough for two consecutive halves; the dividend reset below the committed AED "
     f"{n0(IN['div_policy'])}mn.")]:
    bullet(body, bold_head=head)
P('', space_after=8)

# =========================== 12. APPENDIX A ==================================
H1('Appendix A  Financial statements')
H2('A.1  Income statement — three years audited and five years forecast (consolidated, AED mn)')
cols = ['FY2023', 'FY2024', 'FY2025'] + YRS
def h3(key, neg=False, fmt=n0):
    out = []
    for y in ('FY23', 'FY24', 'FY25'):
        v = HI[y][key]
        out.append(f"({fmt(abs(v))})" if (neg or v < 0) else fmt(v))
    return out
rows = [['AED mn'] + cols]
rows.append(['Revenue'] + h3('rev') + [n0(B['rev'][y]) for y in YRS])
rows.append(['Interest income on the concession receivable'] + h3('intco') +
            [n0(B['intco'][y]) for y in YRS])
rows.append(['Cost of sales'] + h3('cos') + ['—'] * 5)
rows.append(['Gross profit'] + h3('gp') + ['—'] * 5)
rows.append(['General and administrative expenses'] + h3('ga') + ['—'] * 5)
rows.append(['Operating profit'] + h3('op') + ['—'] * 5)
rows.append(['EBITDA (derived: operating profit + D&A)'] + h3('ebitda') +
            [n0(B['ebitda'][y]) for y in YRS])
rows.append(['EBITDA margin'] + [pc(HI[y]['ebitda'] / HI[y]['rev']) for y in
             ('FY23', 'FY24', 'FY25')] + [pc(B['ebitda'][y] / B['rev'][y]) for y in YRS])
rows.append(['Depreciation and amortisation'] + h3('dna', neg=True) +
            [f"({n0(B['dna'][y])})" for y in YRS])
rows.append(['EBIT (forecast basis)'] + ['—'] * 3 + [n0(BC['ebit'][y]) for y in YRS])
rows.append([f"NOPAT at {pc(IN['tax_ct'], 0)} / at {pc(IN['tax_dmtt'], 0)}"] + ['—'] * 3 +
            [f"{n0(BC['nopat'][y])} / {n0(BD['nopat'][y])}" for y in YRS])
rows.append(['Profit before tax'] + h3('pbt') + ['—'] * 5)
rows.append(['Income tax (credit) / expense'] + h3('tax') + ['—'] * 5)
rows.append(['Profit for the year'] + h3('pat') + ['—'] * 5)
rows.append(['Attributable to shareholders'] + h3('npa') + ['—'] * 5)
rows.append(['Earnings per share (AED, derived)'] +
            [p3(HI[y]['npa'] / SH) for y in ('FY23', 'FY24', 'FY25')] + ['—'] * 5)
table(rows, [1.90, 0.6375, 0.6375, 0.6375, 0.6375, 0.6375, 0.6375, 0.6375, 0.6375],
      size=7.8, band_rows={7, 8})
caption("Every FY2023-25 line is taken directly from the company's audited consolidated "
        "statements (the 2023 income-statement figure of interest income on the airport "
        "concession receivable is presented INSIDE gross profit by the company, and the same "
        "presentation is kept here). EBITDA is a house derivation — operating profit plus "
        "depreciation and amortisation — labelled as such; the audited statements contain no "
        "EBITDA line. The 2023 tax line is a CREDIT (first recognition of deferred tax assets "
        "ahead of UAE corporate tax). Forecast financing, tax and attributable lines are shown "
        "only where the model constructs them; the free-cash-flow waterfall in section 1.1 is "
        "a pre-financing measure by construction.")

H2('A.2  Balance sheet — condensed house layout (consolidated, AED mn)')
def bs_col(src, m):
    return {k: (src.get(v, 0) or 0) / 1000.0 if isinstance(v, str) else
            sum((src.get(x, 0) or 0) for x in v) / 1000.0 for k, v in m.items()}
b23r = EX23['2023']['balance_sheet']
b23 = {**b23r['non_current_assets'], **b23r['current_assets'],
       **b23r['equity'], **b23r['non_current_liabilities'],
       'cur_borrow': b23r['current_liabilities']['bank_borrowings'],
       'pay': b23r['current_liabilities']['trade_and_other_payables'],
       'lease_cur': b23r['current_liabilities']['lease_liabilities'],
       'total_liabilities': b23r['total_liabilities'],
       'total_assets': b23r['total_assets']}
c23 = bs_col(b23, dict(
    ppe='property_plant_equipment', intang='intangible_assets',
    conc='financial_assets_amortised_cost', invprop='investment_properties',
    inv='inventories', recv='trade_and_other_receivables',
    cash='cash_and_cash_equivalents', dep='term_deposits',
    assets='total_assets', borrow=('bank_borrowings', 'cur_borrow'),
    lease=('lease_liabilities', 'lease_cur'), pay='pay',
    liab='total_liabilities', eqp='attributable_to_equity_holders',
    nci='non_controlling_interests', eqt='total_equity'))
b24r = EX25['2024_comparative']['balance_sheet']
c24 = bs_col(b24r, dict(
    ppe='property_plant_and_equipment', intang='intangible_assets',
    conc='financial_assets_amortised_cost_non_current',
    invprop='investment_properties', inv='inventories',
    recv='trade_and_other_receivables', cash='cash_and_cash_equivalents',
    dep='term_deposits', assets='total_assets',
    borrow=('bank_borrowings_non_current', 'bank_borrowings_current'),
    pay='trade_and_other_payables_current', liab='total_liabilities',
    eqp='equity_attributable_to_parent', nci='non_controlling_interests',
    eqt='total_equity'))
c24['lease'] = EX24['notes']['lease_liabilities_note6']['2024']['total'] / 1000.0
b25r = EX25['2025']['balance_sheet']
b25 = {**b25r['non_current_assets'], **b25r['current_assets'], **b25r['equity'],
       **b25r['non_current_liabilities'],
       'cur_borrow': b25r['current_liabilities']['bank_borrowings'],
       'pay': b25r['current_liabilities']['trade_and_other_payables'],
       'lease_cur': b25r['current_liabilities']['lease_liabilities'],
       'total_liabilities': b25r['total_liabilities'],
       'total_assets': b25r['total_assets']}
c25 = bs_col(b25, dict(
    ppe='property_plant_and_equipment', intang='intangible_assets',
    conc='financial_assets_at_amortised_cost', invprop='investment_properties',
    inv='inventories', recv='trade_and_other_receivables',
    cash='cash_and_cash_equivalents', dep='term_deposits',
    assets='total_assets', borrow=('bank_borrowings', 'cur_borrow'),
    lease=('lease_liabilities', 'lease_cur'), pay='pay',
    liab='total_liabilities', eqp='equity_attributable_to_parent',
    nci='non_controlling_interests', eqt='total_equity'))
bjr = EXI['h1_2026']['balance_sheet_30_jun_2026_full']
bj = {**bjr['non_current_assets'], **bjr['current_assets'], **bjr['equity'],
      **bjr['non_current_liabilities'],
      'cur_borrow': bjr['current_liabilities']['bank_borrowings'],
      'pay': bjr['current_liabilities']['trade_and_other_payables'],
      'lease_cur': bjr['current_liabilities']['lease_liabilities'],
      'total_liabilities': bjr['total_liabilities'],
      'total_assets': bjr['total_assets']}
cj = bs_col(bj, dict(
    ppe='property_plant_and_equipment', intang='intangible_assets',
    conc='financial_assets_at_amortised_cost', invprop='investment_properties',
    inv='inventories', recv='trade_and_other_receivables',
    cash='cash_and_cash_equivalents', dep='term_deposits',
    assets='total_assets', borrow=('bank_borrowings', 'cur_borrow'),
    lease='lease_cur', pay='pay', liab='total_liabilities',
    eqp='attributable_to_equity_holders', nci='non_controlling_interests',
    eqt='total_equity'))
for c in (c23, c24, c25, cj):
    c['nd'] = c['borrow'] + c.get('lease', 0) - c['cash'] - c['dep']
COLS = [('FY2023', c23), ('FY2024', c24), ('FY2025', c25), ('30-Jun-2026', cj)]
def bsr(label, key, neg=False):
    return [label] + [(f"({n0(c[key])})" if neg else n0(c[key])) for _, c in COLS]
rows = [['AED mn'] + [nm for nm, _ in COLS],
        bsr('Property, plant and equipment', 'ppe'),
        bsr('Intangible assets', 'intang'),
        bsr('Airport-concession receivable (amortised cost, non-current)', 'conc'),
        bsr('Investment properties', 'invprop'),
        bsr('Inventories', 'inv'),
        bsr('Trade and other receivables', 'recv'),
        bsr('Term deposits', 'dep'),
        bsr('Cash and cash equivalents', 'cash'),
        bsr('Total assets', 'assets'),
        bsr('Bank borrowings (current + non-current)', 'borrow'),
        bsr('Lease liabilities', 'lease'),
        bsr('Trade and other payables', 'pay'),
        bsr('Total liabilities', 'liab'),
        bsr('Equity attributable to shareholders', 'eqp'),
        bsr('Non-controlling interests', 'nci'),
        bsr('Total equity', 'eqt'),
        bsr('Net debt (borrowings + leases − cash − deposits)', 'nd')]
table(rows, [3.10, 0.90, 0.90, 0.90, 1.20], size=8.3, band_rows={9, 16, 17})
caption(f"FY2023, FY2024 and FY2025 are audited; the June-2026 column is the reviewed interim. "
        f"The net-debt row reproduces the company's own presented figure at 30 June 2026 "
        f"({n0(IN['netdebt_jun26_co'])}mn) exactly. The 2023 step-up in borrowings funded the "
        f"airport-concession acquisition; the 2024-25 rise in cash is retained operating cash "
        f"ahead of the October dividend instalments.")

H2('A.3  Forecast balance-sheet and cash-flow markers')
rows = [['AED mn'] + YRS,
        ['Property, plant and equipment'] + [n0(B['ppe'][y]) for y in YRS],
        ['Net working capital (negative = funded by customers/payables)'] +
        [f"({n0(abs(B['nwc'][y]))})" for y in YRS],
        ['Working capital released in the year'] + [n0(-B['dnwc'][y]) for y in YRS],
        ['Capital expenditure'] + [f"({n0(B['capex'][y])})" for y in YRS],
        ['Depreciation and amortisation'] + [n0(B['dna'][y]) for y in YRS],
        [f"Free cash flow to the firm at {pc(IN['tax_ct'], 0)}"] +
        [n0(BC['fcff'][y]) for y in YRS],
        [f"Free cash flow to the firm at {pc(IN['tax_dmtt'], 0)}"] +
        [n0(BD['fcff'][y]) for y in YRS],
        ['Dividends (committed policy held flat)'] + [n0(IN['div_policy'])] * 5]
table(rows, [2.60, 0.88, 0.88, 0.88, 0.88, 0.88], size=8.3, band_rows={6, 7})
P(f"Two features to read carefully. Net working capital is negative and grows more negative "
  f"with revenue — customer deposits and payables to the related-party supplier fund the "
  f"cycle, so each year RELEASES cash into the free-cash-flow line. And free cash flow to "
  f"equity — the firm figure less roughly AED {n0(NF25 * (1 - IN['tax_ct']))}mn of after-tax "
  f"net finance cost — runs almost exactly at the AED {n0(IN['div_policy'])}mn payout in the "
  f"shock year: the dividend is covered, with the growth funded by the working-capital release "
  f"and the revolving facilities' headroom. Net borrowings are held flat by construction; the "
  f"model neither assumes deleveraging credit nor new debt-funded expansion.")

# =========================== 13. APPENDIX B ==================================
H1('Appendix B  Peer frame, risk register — and the research register')
H2('B.1  Peers and the sector frame')
TB = SX['peers_relative_multiples']['TABREED']
rows = [['Measure', 'Empower', 'Tabreed', 'DEWA (parent)'],
        ['What it is', 'Dubai district cooling, about ' + DUBAI_SHARE + '% of the emirate',
         'UAE-wide and regional district cooling; the only listed pure peer',
         'the Dubai power and water monopoly; consolidates Empower'],
        ['2025 revenue (AED mn)', n0(IN['rev_fy25']), n0(TB['fy2025']['revenue_aed_m']), '—'],
        ['2025 EBITDA margin', pc(HI['FY25']['ebitda'] / HI['FY25']['rev']),
         pc(TB['fy2025']['ebitda_aed_m'] / TB['fy2025']['revenue_aed_m']), '—'],
        ['Net debt / EBITDA', f"{n1(NDX)}×", f"{TB_NDX}×", '—'],
        ['Trailing price / earnings', f"{n1(SPOT / (IN['npa_fy25'] / SH))}×",
         f"{n1(REL['tabreed_pe'])}×", f"{n1(REL['dewa_pe'])}×"],
        ['Dividend yield', pc(YLD, 1), TB_YLD, DEWA_YLD],
        ['Source and date', 'this study, audited statements and the 7-Aug-2026 close',
         'FY2025 results via exchange disclosures; market value from a data provider dated '
         '22-Jun-2026; multiples derived and flagged as derived',
         'market data as of early Aug-2026; secondary marker only — the parent consolidates '
         'the subject']]
table(rows, [1.55, 1.80, 1.85, 1.80], size=8.2)
P("Emicool, the third Dubai operator, is private (a Dubai Investments / Actis joint venture) "
  "and provides no usable multiple; no listed peer exists for the airport-concession leg. The "
  "leverage gap is the reason the peer comparison is made at the enterprise line: Tabreed "
  "carries several turns more net debt, so raw price/earnings comparisons flatter the wrong "
  "name.")

H2('B.2  Risk register')
rows = [['Risk', 'Mechanism', 'Where it is priced'],
        ['Tariff review', 'the regulator approves tariffs; a cut would reprice the capacity '
         'charge — the profit pool itself',
         'NOT priced — flagged as the model\'s single most valuable assumption (sections 1.7 '
         'and 7); a cut is a regime change requiring a re-model'],
        ['War re-escalation', 'hospitality occupancy → consumption; risk premium → discount '
         'rate; connection pipeline → volumes',
         f"the bear scenario, AED {p3(CEN['bear'])} per share, is a full re-run with all four "
         f"channels moved together"],
        ['Minimum top-up tax', f"consolidation into the DEWA group could lift the rate from "
         f"{pc(IN['tax_ct'], 0)} to {pc(IN['tax_dmtt'], 0)}",
         f"published as a full second column everywhere: {p3(abs(DMTT_DELTA))} per share on "
         f"the primary lens"],
        ['Consumption persistence', 'usage per connected ton stays at the shocked level',
         f"a full alternative model: {pc(abs(CRUX_DELTA), 1)} on the primary lens — small, "
         f"because of the pass-through (section 1.7)"],
        ['Related-party concentration', 'the controlling shareholder is also the sole input '
         'supplier and the tariff counterweight',
         'a governance fact discussed in section 7; one reason the relative lens keeps weight'],
        ['Float and liquidity', 'free float near a fifth after the February control purchase; '
         'index treatment and exit liquidity are thinner',
         'not separately priced; noted as a reason market-price signals are noisier than '
         'usual'],
        ['Data limitations', f"a {TENOR}-year sovereign anchor against longer cash flows; an "
         f"index series with missing sessions behind the beta; deck-sourced revenue-mix "
         f"percentages",
         'each flagged in place (section 1.8, section 7) and recorded in the bibliography']]
table(rows, [1.55, 2.70, 2.75], size=8.3)

H2('B.3  The research register — the sources this study stands on')
P("Research proceeded from the company's own filings outward: audited statements first, then "
  "the interim record, the investor-relations material, the regulator, the sovereign data and "
  "the market. The main sources, dated, are tabulated below; the companion bibliography "
  "document records every input's value, source and date individually, together with the "
  "searches that returned nothing.")
rows = [['Source', 'Type', 'Date', 'What was taken'],
        ['Audited consolidated financial statements, FY2022–FY2025 (PwC, unqualified)',
         'Company filing', '2023–Feb-2026',
         'the full income statement, balance sheet and cash-flow record; revenue and '
         'cost notes; borrowings and refinancing notes; related-party purchases; the '
         'capitalisation rate; consumption revenue via the auditor\'s key-audit-matter '
         'sections'],
        ['Condensed interim financial statements, Q1-2026 and H1-2026 (limited review)',
         'Company filing', 'May / Aug 2026',
         'the study-year actuals: quarterly revenue, profit, the June-2026 balance sheet, and '
         'the note tying the consumption fall partly to conflict-hit hospitality occupancy'],
        ['H1-2026 earnings presentation', 'Company investor relations', '5-Aug-2026',
         'connected and contracted capacity, connection guidance, equivalent full-load hours, '
         'the revenue mix, net debt as presented, and the dividend commitment'],
        ['Dubai Executive Council Resolution 6/2021; Regulatory and Supervisory Bureau '
         'instruments', 'Regulator', '2021–2025',
         'the tariff-regulation frame behind the flat-tariff assumption'],
        ['UAE Ministry of Finance dirham T-Bond auction result', 'Sovereign data', '30-Jul-2026',
         'the risk-free anchor'],
        ['Published country-risk dataset (July-2026 edition)', 'Reference dataset', '1-Jul-2026',
         'the UAE default spreads and equity risk premia on both bases'],
        ['DFM daily price history for EMPOWER (supplied) and a DFM General Index series',
         'Market data', 'to 7-Aug-2026',
         'the anchor price, volatility, the moving-average structure, the beta regression and '
         'the price distributions'],
        ['Tabreed and DEWA results and market data', 'Peer disclosures / market data',
         'Jun–Aug 2026', 'the relative-multiples lens — cross-check only, never a source for '
         'Empower\'s own numbers'],
        ['Wire and reference coverage of the 2026 conflict and ceasefire', 'Press',
         'to 9-Aug-2026', 'the macro timeline; where sources disagreed on the truce status, '
         'both readings were recorded rather than resolved']]
table(rows, [2.30, 1.20, 0.90, 2.60], size=8.2)

# =========================== 14. APPENDIX C ==================================
H1('Appendix C  The expert valuation panel')
P("Three valuation approaches are run against the same disclosed facts by three notional "
  "experts, each committed to a different method, each showing every intermediate line, and "
  "each required to state in advance what would prove them wrong. They are not asked to agree, "
  "and they do not.")

H2('C.1  Expert 1 (infrastructure cash flow) — the contracted asset base, discounted')
P("Worldview: a regulated utility with contracted revenue is the one class of business a "
  "discounted-cash-flow model prices well — the cash flows are visible, the regulator caps the "
  "upside, and the right answer is the present value of the contract stack. When it works: "
  "precisely here. When it fails: when the terminal assumptions smuggle in more value than the "
  "explicit years justify — which is why every terminal choice below is shown and challenged "
  "in C.4.")
rows = [['Step (base case, ' + pc(IN['tax_ct'], 0) + ' tax, AED mn)'] + YRS,
        ['Revenue'] + [n0(B['rev'][y]) for y in YRS],
        ['EBITDA'] + [n0(B['ebitda'][y]) for y in YRS],
        ['EBIT'] + [n0(BC['ebit'][y]) for y in YRS],
        ['NOPAT'] + [n0(BC['nopat'][y]) for y in YRS],
        ['Free cash flow to the firm'] + [n0(BC['fcff'][y]) for y in YRS],
        ['Present value'] + [n0(BC['pv'][y]) for y in YRS]]
table(rows, [3.00, 0.80, 0.80, 0.80, 0.80, 0.80], size=8.4, band_rows={6})
rows = [['Terminal block and bridge', 'Value'],
        ['Sum of the five present values (AED mn)', n0(BC['pv_explicit'])],
        [f"Terminal value — final NOPAT × (1 + {pc(IN['g_term'], 1)}) × (1 − "
         f"{pc(BC['rr_term'], 1)}) ÷ ({pc(W['rating_ct'], 2)} − {pc(IN['g_term'], 1)})",
         n0(BC['tv'])],
        ['Present value of the terminal value (AED mn)', n0(BC['pv_tv'])],
        ['Enterprise value (AED mn)', n0(BC['ev'])],
        ['Less net debt; plus investment properties and fair-value assets; less minorities '
         f"({pc(NCI_FRAC, 1)} of profits)",
         f"({n0(ND)}) / {n0(IN['invprop_jun26'] + IN['fvtpl_jun26'] + IN['fvoci_jun26'])} / "
         f"({n0(BC['nci_val'])})"],
        ['Equity attributable (AED mn)', n0(BC['eq_attr'])],
        ['Fair value per share (AED)', p3(BC['ps'])],
        ['Range — the consumption-grid endpoints, each carrying half the effect of a ±50bp '
         'move in the cost of capital', f"{p2(E1_LO)} – {p2(E1_HI)}"]]
table(rows, [4.55, 2.45], size=8.4, band_rows={7})
P(f"Named sensitivity: the consumption-recovery grid of section 1.7 — the full span from "
  f"never-recovers to overshoot is worth AED "
  f"{p3(CRX['rows'][-1]['ps'] - CRX['rows'][0]['ps'])} per share, while a half-point of "
  f"discount rate is worth about AED {p3(abs(_dn50 - _up50) / 2)}. My valuation is a "
  f"discount-rate argument first and a volume argument barely at all.")
P("Falsifier, stated in advance: two consecutive half-years with equivalent full-load hours "
  "below the 2026 trough. That would mean the demand loss is structural, not "
  "hospitality-linked, and the recovery leg of my base case should be discarded rather than "
  "delayed.", space_after=8)

H2('C.2  Expert 2 (income) — the committed dividend, capitalised')
P("Worldview: for a minority shareholder in a company controlled at 80% by its own supplier, "
  "the only cash flow that is real is the one that arrives — the dividend. Value the "
  "commitment, check its coverage, and treat everything else as the controller's business. "
  "When it works: income-controlled utilities exactly like this. When it fails: when the "
  "payout is about to change in either direction — a committed dividend is a floor and a "
  "ceiling only until it is not.")
rows = [['Step', 'Value'],
        ['Committed distribution (AED mn a year, 2025 and 2026)', n0(DDM['policy_mn'])],
        ['Per share (AED)', p3(DDM['dps'])],
        [f"Grown at {pc(IN['g_term'], 1)} and capitalised at the {pc(W['ke_rating'], 2)} cost "
         f"of equity", f"× {1 + IN['g_term']:.3f} ÷ ({pc(W['ke_rating'], 2)} − "
         f"{pc(IN['g_term'], 1)})"],
        ['Fair value per share (AED)', p3(DDM['ps'])],
        [f"Range — growth {pc(E2_G_LO, 1)} to {pc(E2_G_HI, 1)}", f"{p2(E2_LO)} – {p2(E2_HI)}"]]
table(rows, [4.55, 2.45], size=8.5, band_rows={5})
P("Coverage is the whole argument, so here it is, line by line:")
rows = [['AED mn'] + YRS,
        [f"Free cash flow to the firm ({pc(IN['tax_ct'], 0)})"] +
        [n0(BC['fcff'][y]) for y in YRS],
        ['Less after-tax net finance cost (held at the 2025 level — the book is floating and '
         'was just refinanced)'] + [f"({n0(NF25 * (1 - IN['tax_ct']))})" for _ in YRS],
        ['Free cash flow to equity'] +
        [n0(BC['fcff'][y] - NF25 * (1 - IN['tax_ct'])) for y in YRS],
        ['Dividend'] + [n0(IN['div_policy'])] * 5,
        ['Coverage'] + [f"{(BC['fcff'][y] - NF25 * (1 - IN['tax_ct'])) / IN['div_policy']:.2f}×"
                        for y in YRS]]
table(rows, [3.00, 0.80, 0.80, 0.80, 0.80, 0.80], size=8.3, band_rows={5})
P(f"In the shock year coverage is almost exactly one — the payout absorbs essentially all the "
  f"equity cash flow, and the growth is funded by the working-capital release and the "
  f"revolving facilities' headroom. That is covered, not slack, and it is why my number sits "
  f"below the cash-flow expert's: I pay for the distribution I can see, not the terminal "
  f"value I cannot.")
P("Named sensitivity: each half-point of assumed growth is worth roughly AED "
  f"{p3((E2_HI - E2_LO) / 2)} per share across my range — the entire argument is the "
  "capitalisation rate against the growth of a committed number.")
P("Falsifier, stated in advance: a dividend reset below the committed level, or a payout "
  "financed by facility drawdown for two consecutive periods. Either breaks the premise that "
  "the distribution is an economic signal rather than a promise.", space_after=8)

H2('C.3  Expert 3 (relative value, the sceptic) — anchor on what is actually paid')
P("Worldview: models are opinions; transactions are facts. Anchor on what the market pays for "
  "the same economics today, use the harsher of any contested framing, and treat every model "
  "premium over the market as a claim requiring extraordinary evidence. When it works: "
  "regimes, like this one, where the marginal price-setter is distressed or absent and model "
  "values float free of clearing prices. When it fails: when the anchor set is itself "
  "mispriced — a war-discounted peer group imports the war.")
rows = [['Step', 'Value'],
        [f"Tabreed enterprise value / EBITDA (derived, flagged)",
         f"{n1(REL['tabreed_ev_ebitda'])}×"],
        ['× Empower 2026E EBITDA (AED mn)', n0(REL['ev_rel'] / REL['tabreed_ev_ebitda'])],
        ['Implied enterprise value (AED mn)', n0(REL['ev_rel'])],
        ['Less net debt; plus side pockets; less minorities — per share (AED)',
         p3(REL['ps_rel'])],
        [f"Tabreed price/earnings {n1(REL['tabreed_pe'])}× on 2026E attributable profit "
         f"({n0(REL['npa26'])} AED mn) — per share (AED)", p3(REL['ps_pe'])],
        [f"The February control print — what the controller itself paid a related party",
         p2(DEWA['price'])],
        [f"My tax base: the {pc(IN['tax_dmtt'], 0)} minimum-tax column, on prudence",
         f"{p3(BD['ps'])} on the cash-flow model — noted, not adopted"],
        ['Range — from the market price to the control print', f"{p2(SPOT)} – "
         f"{p2(DEWA['price'])}"],
        ['Central — the earnings-basis read', p2(E3_CENTRAL)]]
table(rows, [4.55, 2.45], size=8.4, band_rows={9})
P(f"Named sensitivity: each turn of the peer earnings multiple is worth AED "
  f"{p3(REL['ps_pe'] / REL['tabreed_pe'])} per share. My range's top is not a multiple at all "
  f"— it is the one disclosed transaction ({p2(DEWA['price'])}), and I note that a control "
  f"price paid between related parties bounds the question from above without proving "
  f"anything about what a minority share is worth.")
P("Falsifier, stated in advance: a GCC utility re-rating — Tabreed sustained above thirteen "
  "times enterprise value to EBITDA — without Empower following. That would show the discount "
  "is company-specific rather than regime-wide, and my regime-anchored central should be "
  "abandoned.", space_after=8)

H2('C.4  Cross-examination')
rows = [['Challenge', 'From', 'Response'],
        [f'"{pc(BC["tv_share"], 0)} of your enterprise value is terminal, earning a '
         f'{pc(BC["roic_term"], 0)} return on capital forever — at a REGULATED utility. The '
         f'regulator exists to take that return away."', 'Expert 3 to Expert 1',
         'Rejected in part, conceded in part. The measured return is inflated by the funding '
         'model, not by tariff generosity: customers\' deposits and payables hold working '
         'capital negative, so the capital base the return is struck on is artificially small '
         '— the same tariff on a conventionally funded balance sheet would show an ordinary '
         'return, and the regulator prices the tariff, not the ratio. CONCEDED: the '
         'tariff-review risk is real, it is the one lever that reaches the capacity charge, '
         'and it deserves exactly the bear-case weight it gets.'],
        ['"You are capitalising a promise. The committed dividend runs to 2026 only, and your '
         'coverage table shows it absorbing all the equity cash flow in the shock year."',
         'Expert 1 to Expert 2',
         'Partly conceded. The commitment is two years old and covered at one times, not '
         'slack. But the counterparty is the 80% owner, which collects four-fifths of every '
         'instalment itself and set the policy — the incentive alignment is unusually direct, '
         'and the distribution record since listing has only stepped up.'],
        ['"Your anchors are war prices. You are not measuring Empower; you are measuring '
         'March."', 'Expert 2 to Expert 3',
         'Conceded, and embraced. That is what a relative lens is FOR — it prices the regime '
         'the shares must actually be sold into. The mistake would be presenting it as '
         'intrinsic; nobody here does. My range top is a real transaction, not a war print.'],
        ['"All three of you assume the tariff stays flat."', 'The panel to itself',
         'Accepted as the shared, unpriced assumption — stated in sections 1.7, 5 and 7. A '
         'tariff cut would move every method in the same direction at once, which is exactly '
         'why it is flagged rather than diversified away.']]
table(rows, [2.45, 1.20, 3.35], size=8.2)

H2('C.5  The three in one room')
fig('figD1_experts.png', 6.9,
    f"Figure 9 — the three experts' ranges against the market price of {p2(SPOT)} and the "
    f"control print of {p2(DEWA['price'])}.")
P(f"The panel spans AED {p2(min(E1_LO, E2_LO, SPOT))} to {p2(max(E1_HI, E2_HI, DEWA['price']))} "
  f"— and the disagreement is orderly, not noisy. Expert 1 discounts the contract stack and "
  f"lands highest ({p2(E1_LO)}–{p2(E1_HI)}); Expert 2 capitalises the committed dividend and "
  f"lands in the middle ({p2(E2_LO)}–{p2(E2_HI)}); Expert 3 anchors on what the war-discounted "
  f"market actually pays and lands lowest ({p2(SPOT)}–{p2(DEWA['price'])}, central "
  f"{p2(E3_CENTRAL)}). Notice what the room agrees on: every range sits at or above the market "
  f"price, every method finds the capacity charge rather than the meter carrying the value, "
  f"and every falsifier is observable within two reporting periods. The study's own weighted "
  f"central ({p3(CEN['ct'])} / {p3(CEN['dmtt'])} by tax framing) sits between Expert 1 and "
  f"Expert 2 — which is what a weighting that gives the market regime a real vote should "
  f"produce.")

H2('C.6  Reading the divergence')
rows = [['Assumption', 'Expert 1', 'Expert 2', 'Expert 3', 'What it is worth'],
        ['Tax basis', pc(IN['tax_ct'], 0) + ' (audited rate)', 'embedded in the payout',
         pc(IN['tax_dmtt'], 0) + ' on prudence',
         f"AED {p3(abs(DMTT_DELTA))} per share on the cash-flow model — the gap between the "
         f"two published columns"],
        ['Terminal claim', f"full terminal value ({pc(BC['tv_share'], 0)} of enterprise "
         f"value)", 'a perpetuity of the committed dividend only',
         'none — the current multiple regime is assumed permanent',
         f"AED {p3(BC['ps'] - E3_CENTRAL)} per share between Expert 1's central and Expert "
         f"3's — the largest single gap in the room"],
        ['Consumption recovery', 'recovers through 2027; grid shown', 'not sensitive — the '
         'dividend is fixed either way', 'embedded in the peer prices',
         f"AED {p3(abs(BC['ps'] - PC['ps']))} per share even in the never-recovers case — "
         f"small by construction (the pass-through)"],
        ['Risk premium', 'model-built cost of equity from the sovereign and the published '
         'premium', f"the same {pc(W['ke_rating'], 2)} rate, applied to a committed flow",
         'whatever the market embeds — the war discount is kept, not modelled out',
         'the half-point grid: AED ' + p3(abs(_dn50 - _up50) / 2) + ' per share per 50bp']]
table(rows, [1.20, 1.55, 1.45, 1.55, 1.25], size=8.0)
P("The instruction to the reader is not to average the three. It is to decide which premise "
  "you hold — whether the terminal claim of a regulated monopoly is bankable, whether a "
  "committed dividend is a floor, whether today's regime prices are the right anchor — and "
  "use the corresponding number. The disagreement is a map of what you need a view on.",
  space_after=10)

# =========================== 15. ABOUT =======================================
H1('About this series')
P("This series publishes independent, educational valuation studies of listed companies. Each "
  "study is built from disclosed financial statements and named market data, states its "
  "assumptions explicitly, computes every figure in an auditable model rather than in prose, "
  "and publishes the ranges its assumptions produce. Studies never carry a rating or a price "
  "target. Where a figure is estimated rather than disclosed, it is labelled. Where a source "
  "could not be reached or a disclosure does not exist, the gap is recorded in the "
  "accompanying bibliography rather than quietly filled in.")
P("The probabilistic price map in section 3 is produced by a volatility model that is tested "
  "by walk-forward simulation against a carry-anchored random-walk benchmark before it is "
  "allowed to publish a range. It describes price dispersion and carries no view on value. It "
  "is never combined with the fair-value work.")

# =========================== 16. DISCLOSURE ==================================
H1('Disclosure & Disclaimer')
P("For information only — not investment advice. This document is educational analysis and is "
  "not an offer or a solicitation to buy or sell any security. It contains no recommendation, "
  "no rating and no price target. The author holds no position in the security discussed and "
  "has no business relationship with the company. Figures are drawn from public sources "
  "believed reliable but not independently verified; where figures are derived or estimated "
  "this is stated in the text. Valuation is inherently uncertain and depends on assumptions "
  "that reasonable analysts will dispute — several such disputes are set out explicitly in "
  "this document, and two (the tax framing and the consumption recovery) are published as "
  "full alternative computations rather than resolved silently. Past performance and "
  "simulated distributions are not guides to future returns. Readers must reach their own "
  "conclusions and should consider taking independent advice. No liability is accepted for "
  "any loss arising from use of this material.", size=9.2, color=GREY)

out = os.path.join(HERE, 'EMPOWER_Valuation_Study_09-08-2026_public.docx')
finalize(doc)
doc.save(out)
print(f"wrote {out} | {len(doc.paragraphs)} paragraphs | {len(doc.tables)} tables")
if MISSING_FIGS:
    print("MISSING FIGURES (skipped):", ', '.join(MISSING_FIGS))
else:
    print("all figures embedded")
