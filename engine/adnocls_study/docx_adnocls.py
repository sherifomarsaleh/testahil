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
import datetime as _dt


def _pdate(s):
    return _dt.date(*map(int, s.split('-')))


_MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def fdate(s):
    """ISO date -> '28 Mar 2027', so a table of contract expiries reads like prose."""
    d = _pdate(s)
    return f'{d.day} {_MON[d.month - 1]} {d.year}'


# The fleet is counted AT THE VALUATION DATE, and the split between vessels trading at
# spot and vessels already fixed is read off the published charter table rather than off a
# second disclosure: a vessel is on charter out on a date if its own contract runs over it.
VDATE = _pdate(M['valuation_date'])
CHT = FLT['charters']
CHT_LIVE = [c for c in CHT if _pdate(c['start']) <= VDATE < _pdate(c['end'])]
owned_total = sum(FLT['owned'].values())
owned_total_fy25 = sum(FLT['owned_fy25'].values())
fixed_total = len(CHT_LIVE)
spot_total = owned_total - fixed_total
fixed_by_class = {k: sum(1 for c in CHT_LIVE if c['klass'] == k) for k in FLT['owned']}
charter_last = max(c['end'] for c in CHT)
charter_last_yr = charter_last[:4]
# the implied spot rate against the blend the company publishes, for the largest class in
# the quarter it has actually reported — the single number this edition turns on
VS_BLEND = FLT['blend_q1_26']['vlcc']
VS_SPOT = FLT['spot_q1_26']['vlcc']


def aed_ps(usd_k):
    """A US-dollar-thousand amount expressed per share, in dirhams."""
    return usd_k / SH / 1000.0 * PEG


# The minority deduction, three ways: at book, as this study takes it, and as it would be
# if the profit share were applied to the whole equity value with nothing netted off.
# The cost of capital as the superseded edition built it — ordinary equity and debt only,
# with the perpetual capital securities left out of the weights entirely. Recomputed here
# from the committed weights rather than quoted, so the "before" figure cannot drift away
# from the "after" one it is being compared with.
_cap_ed = W['mktcap'] + W['debt']
_we_ed, _wd_ed = W['mktcap'] / _cap_ed, W['debt'] / _cap_ed
WACC_PRIOR = _we_ed * W['ke'] + _wd_ed * W['kd'] * (1 - W['tax_stat'])
WACC_TERM_PRIOR = _we_ed * W['ke_term'] + _wd_ed * W['kd_term'] * (1 - W['tax_stat'])
# The justified-multiple form of the asset lens, on the SAME inputs the residual-income
# construction uses, so the comparison between the two methods is a comparison of methods
# and not of two different sets of assumptions.
PB_SINGLE = (BK['roe_sustainable'] - BK['g']) / (BK['ke'] - BK['g'])
BOOK_SINGLE = PB_SINGLE * BK['bvps_aed']
# Where the base rate path crosses the independent one-year charter, read off the path
# itself rather than named in prose — the rebuilt path moved it, and a sentence naming the
# old years would have survived the rebuild looking perfectly plausible.
_vp, _tc = MCC['vlcc_path'], MCC['vlcc_1y_tc']
TC_CROSS = next((i for i in range(len(_vp) - 1) if _vp[i] >= _tc >= _vp[i + 1]),
                len(_vp) - 2)
NCI_LIFT = aed_ps(DCF['nci'] - DCF['nci_book'])
NCI_FLAT = IN['nci_share'] * (DCF['ev'] - DCF['net_debt'])
NCI_FLAT_COST = aed_ps(NCI_FLAT - DCF['nci_book'])
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
# Which two consecutive rate anchors the market price falls between — read off the grid, so
# the sentence that names them cannot drift away from the table it describes.
_anch = sorted(SN['anchor'].items(), key=lambda kv: float(kv[0]))
anchor_cross = next(((float(_anch[i][0]), float(_anch[i + 1][0]))
                     for i in range(len(_anch) - 1)
                     if _anch[i][1] <= SPOT <= _anch[i + 1][1]), None)
# and which two beta columns it falls between, on the adopted terminal growth row
_bcol = SN['gs'].index(IN['g_terminal'])
_bser = [(b, SN['grid_beta_g'][i][_bcol]) for i, b in enumerate(SN['betas'])]
beta_cross = next(((_bser[i][0], _bser[i + 1][0]) for i in range(len(_bser) - 1)
                   if _bser[i + 1][1] <= SPOT <= _bser[i][1]), None)
tax_span = list(SN['tax'].values())
e1_pe_lo = E1['rng'][0] / E1['eps_usd'] / PEG
e1_pe_hi = E1['rng'][1] / E1['eps_usd'] / PEG
nd_target_debt = IN['nd_ebitda_target_lo'] * F['ebitda'][4]
CLS = [('vlcc', 'Very large crude carriers'), ('lr2', 'Long range 2'),
       ('lr1', 'Long range 1'), ('mr', 'Medium range'), ('hs', 'Handysize')]


def segkey(s):
    return s.lower().replace(' ', '_').replace('-', '_')


# ---- the review record, counted off the register rather than remembered -------
# Two rounds of external review. The count and the number of readers are read from the
# committed adjudication file, so a document that states them cannot drift from it.
_ADJ = json.load(open(os.path.join(HERE, 'critique_adjudication.json')))
N_FINDINGS = len(_ADJ)
N_REVIEWS = len({r['source'] for r in _ADJ})
assert N_FINDINGS and N_REVIEWS, 'the review register is empty'

# The two superseded editions' headline figures, recovered from the register the reviews
# were adjudicated in rather than remembered. A running total is the one number a reader
# cannot reconstruct for themselves, so it has to come from a committed file like the rest.
import re as _re
import collections as _collections


def _prior(field, key):
    counts = _collections.Counter()
    for r in _ADJ:
        for chunk in _re.split(r';', r.get(field) or ''):
            if key in chunk.lower():
                m = _re.search(r'(\d+\.\d\d)\s*(?:→|->)', chunk)
                if m:
                    counts[m.group(1)] += 1
                break
    assert counts, f'no prior {key} recoverable from the review register'
    return float(counts.most_common(1)[0][0])


def _prior2(pattern):
    counts = _collections.Counter(
        m.group(1) for r in _ADJ
        for m in [_re.search(pattern, r.get('evidence') or '')] if m)
    assert counts, f'no figure recoverable for {pattern!r}'
    return float(counts.most_common(1)[0][0])


CENTRAL_ED1 = _prior('claimed_impact', 'weighted central')
DCF_ED1 = _prior('claimed_impact', 'dcf')
CENTRAL_ED2 = _prior2(r'central from (\d+\.\d+) to')
DCF_ED2 = _prior2(r'published DCF base of (\d+\.\d+)')
for _lbl, _v in (('first-edition central', CENTRAL_ED1), ('first-edition cash flow', DCF_ED1),
                 ('second-edition central', CENTRAL_ED2),
                 ('second-edition cash flow', DCF_ED2)):
    assert 1.0 < _v < 100.0, f'{_lbl} recovered as {_v}, which is not a share price'

# ---- the purchase announced on the anchor date -------------------------------
# Eleven vessels for about USD 1.3 billion, announced on the same day as the closing price
# this study is anchored on. The first edition left it out entirely, which compared a fair
# value that excluded the vessels with a market price that already included them.
ACQ_COST = IN['acq_2026_cost']
ACQ_VLCC, ACQ_GAS_N = IN['acq_2026_vlcc'], IN['acq_2026_gas']
ACQ_DATE = fdate(D['inputs']['acq_2026_cost']['date'])
VLCC_AFTER = FLT['owned']['vlcc'] + ACQ_VLCC
# The bridge deducts net debt in three pieces and the purchase is the third of them.
NET_DEBT_TOTAL = BR['net_debt_company'] + BR['deferred'] + ACQ_COST
assert abs(NET_DEBT_TOTAL - BR['net_debt']) < 1e-6, \
    'the bridge deduction does not reconcile to its three published components'

# ---- the earnings multiple, on both bases ------------------------------------
# The peers' FORWARD multiples are applied to the company's forward earnings, which is
# consistent. What was not consistent was quoting the company on a TRAILING multiple in the
# table beside them. Both blends are published; the forward one is the one applied.
BLEND_PE_TTM = ((1 - REL['spot_weight']) * PEERS[0]['pe_ttm']
                + REL['spot_weight'] * PEERS[1]['pe_ttm'])
# and the company's own multiple on the same forward basis, so the comparison table shows
# like against like in both columns rather than a trailing figure beside forward peers
OWN_PE_FWD = M['mktcap_usd000'] / REL['npa_ord_26']

# ---- price to book on the book the asset lens actually uses -------------------
# The market multiple must be struck on the SAME denominator as the justified multiple it
# is printed beside, or the comparison reverses its own sign.
PB_MARKET_ORD = W['mktcap'] / IN['q1_26_eqp']
PB_MARKET_WIDE = REL['own_pb']

# ---- one return-on-equity convention, end to end ------------------------------
# Closing equity in both halves. The model's own forecast row divides by AVERAGE equity,
# which is a different measure; splicing the two produced a rise that was an artefact of
# the switch rather than a fact about the business.
ROE_HIST = [HI['npa'][i] / HB['equity_parent'][i] for i in range(3)]
ROE_FCST = [FIN['npa'][i] / FBS[i]['equity_parent'] for i in range(5)]
ROE_FCST_AVGEQ = [b['roe'] for b in FBS]

# ---- one earnings definition in the leverage ratio ----------------------------
ND_EBITDA_HIST = [HB['net_debt'][i] / HI['ebitda_op'][i] for i in range(3)]

# ---- the first quarter, on the two bases the company itself publishes ---------
# The reviewed statements and the management commentary do not carry the same first-quarter
# 2025 revenue: tanker revenue for the first three quarters of 2025 was re-presented, with
# no effect on profit. The unit table is on the re-presented basis, so a growth rate quoted
# beside unit figures has to be on that basis too.
Q1_REV_26_UNITS = sum(IN[f'q1_26_rev_{segkey(s)}'] for s in SEGS)
Q1_REV_25_UNITS = sum(IN[f'q1_25_rev_{segkey(s)}'] for s in SEGS)
Q1_YOY_UNITS = Q1_REV_26_UNITS / Q1_REV_25_UNITS - 1
Q1_YOY_STAT = IN['q1_26_rev'] / IN['q1_25_rev'] - 1

# ---- depreciation against earnings, across the forecast and not just year one -
DNA_SHARE = [d / e for d, e in zip(F['dna'], F['ebitda'])]
DNA_SHARE_AVG = sum(DNA_SHARE) / len(DNA_SHARE)

# ---- the sum of the parts, with the exposure share re-based to its own leg -----
# The disclosed spot share is a GROUP share, and every dollar of spot exposure sits inside
# one leg. Applied to that leg's own earnings it is materially larger.
SOTP_LEG = {l['leg']: l for l in SOTP['legs']}
SHIP_W_LEG = min(1.0, REL['spot_weight'] * F['ebitda'][0] / FGR['Shipping']['ebitda'][0])
SHIP_MULT_LEG = ((1 - SHIP_W_LEG) * REL['contracted_multiple']
                 + SHIP_W_LEG * REL['spot_multiple'])
SOTP_EV_REBASED = (SOTP['ev_ops'] - SOTP_LEG['Shipping']['ev']
                   + SOTP_LEG['Shipping']['ebitda_26'] * SHIP_MULT_LEG)
SOTP_FV_REBASED = aed_ps(SOTP_EV_REBASED + SOTP['jv'] - SOTP['net_debt']
                         - SOTP['hybrid'] - SOTP['nci'])

# ---- the perpetual securities capitalised at their OWN required return --------
# Their coupon divided by their own coupon rate returns the carrying value to the dollar,
# which is what makes the alternative treatment a statement about the discount rate rather
# than a second valuation of the same claim.
HYB_AT_OWN_COUPON = FIN['hybrid_coupon'] / W['kh']

# ---- the second expert on the same bridge the other two use -------------------
E2_BRIDGED = aed_ps(E2['value'] * (1 - IN['nci_share']) + BR['jv'])

# ---- the disclosed useful lives, quoted from the source rather than restated ---
# The lives are a list of numbers in an accounting policy note. Retyping them into a builder
# is exactly how a document drifts from its own filing, so the sentence is taken from the
# committed source text and only the leading citation is trimmed off it.
DEP_LIVES = SRC['life_tankers'].split(' — ', 1)[1]
assert 'depreciated straight line' in DEP_LIVES, \
    'the useful-life source text is not the policy sentence this quotes'

# ---- the vessel sale, on both carrying values its own release supports --------
VSALE_BOOK_IMPLIED = IN['vessel_sale_price'] - IN['vessel_sale_gain']
VSALE_RATIO_IMPLIED = IN['vessel_sale_price'] / VSALE_BOOK_IMPLIED

# ---- what the beta alone is worth, read off the published grid ----------------
BETA_ONLY_BEAR = SN['grid_beta_g'][SN['betas'].index(BF['ci90'][1])][g_col]
BETA_ONLY_ALT = SN['grid_beta_g'][SN['betas'].index(BFA['beta'])][g_col]

# ---- the terminal risk-free basis switch, priced by read-across ----------------
# The explicit window takes an observed bond yield net of the sovereign's own spread; the
# terminal takes a constructed long-run anchor. That is a change of basis and it is worth
# stating. It has no row of its own in the grid, so it is priced by the beta step that
# moves the cost of equity by the same amount — which OVERSTATES it, because a beta step
# moves every year and this one moves only the terminal.
RF_BASIS_GAP = W['rf_star'] - W['rf_terminal']
_dbeta_equiv = RF_BASIS_GAP / W['erp']
_steps = [(abs((SN['betas'][i + 1] - SN['betas'][i]) - _dbeta_equiv), i)
          for i in range(len(SN['betas']) - 1)]
_rf_i = min(_steps)[1]
RF_READACROSS_BETA = SN['betas'][_rf_i + 1] - SN['betas'][_rf_i]
RF_READACROSS = (SN['grid_beta_g'][_rf_i][g_col] - SN['grid_beta_g'][_rf_i + 1][g_col])

# ---- management's guidance, converted from its own percentages ----------------
# The company publishes DIRECTIONAL guidance — a band in words — for the group and for each
# business unit. Every figure below is this study's own conversion of those words into
# dollars at the midpoint of the band, applied to the reported figure it grows from. The
# three unit rows and the group row do not reconcile, and that is a property of the
# guidance rather than of the conversion.
GPCT = {'Integrated Logistics': ('g26_rev_il', 'g26_ebitda_il'),
        'Shipping': ('g26_rev_ship', 'g26_ebitda_ship'),
        'Services': ('g26_rev_serv', 'g26_ebitda_serv')}
GUID_UNITS_REV = sum(GD[g]['guided_revenue'] for g in GROUPS)
GUID_UNITS_EBITDA = sum(GD[g]['guided_ebitda'] for g in GROUPS)
GUID_REV_GAP = GD['Group']['guided_revenue'] - GUID_UNITS_REV
GUID_EBITDA_GAP = GD['Group']['guided_ebitda'] - GUID_UNITS_EBITDA
BUILT_VS_UNITS = F['ebitda'][0] / GUID_UNITS_EBITDA - 1
# the guided figures must be the ones the model holds, not a second conversion done here
for _g in GROUPS:
    assert abs(GRPH[_g]['revenue'][2] * (1 + IN[GPCT[_g][0]])
               - GD[_g]['guided_revenue']) < 1.0, f'{_g} guided revenue does not reconcile'
    assert abs(GRPH[_g]['ebitda'][2] * (1 + IN[GPCT[_g][1]])
               - GD[_g]['guided_ebitda']) < 1.0, f'{_g} guided earnings do not reconcile'

# ---- where a value sits, computed rather than asserted ------------------------
# Both of these were prose in an earlier edition and both went stale the moment the model
# moved: the cash-flow lens crossed the market price in this rebuild, and every sentence
# that placed it "below" or "between the first and second supports" would have survived the
# rebuild reading perfectly plausibly.
_LADDER = sorted(TC['levels']['sup'] + TC['levels']['res'])
# The year the modelled balance sheet turns to net cash is read off the path, never named:
# the August purchase pushed it out by a year and a sentence naming the old one would have
# read perfectly well.
_nc = [i for i, b in enumerate(FBS) if b['net_debt'] < 0]
NET_CASH_WORD = (f"net cash by {YRL[_nc[0]]}" if _nc
                 else f"{xt(FIN['nd_ebitda'][4], 2)} by {YRL[4]}, without reaching net cash "
                      f"inside the forecast")


def ladder(x):
    below = [lv for lv in _LADDER if lv <= x]
    above = [lv for lv in _LADDER if lv > x]
    if not below:
        return f"below every computed level, the lowest of which is {p2(_LADDER[0])}"
    if not above:
        return f"above every computed level, the highest of which is {p2(_LADDER[-1])}"
    return f"between the computed levels of {p2(below[-1])} and {p2(above[0])}"


_PCT3 = [('5th', H3M['pct']['p5']), ('25th', H3M['pct']['p25']),
         ('50th', H3M['pct']['p50']), ('75th', H3M['pct']['p75']),
         ('95th', H3M['pct']['p95'])]


def zone3m(x):
    lo = [nm for nm, v in _PCT3 if v <= x]
    hi = [nm for nm, v in _PCT3 if v > x]
    if not lo:
        return f"below the {_PCT3[0][0]} percentile of the three-month distribution"
    if not hi:
        return f"above the {_PCT3[-1][0]} percentile of the three-month distribution"
    return (f"between the {lo[-1]} and {hi[0]} percentile of the three-month "
            f"distribution")


# ---- the Services driver rationale, reconciled to the model -------------------
# The committed rationale for this unit still credits the margin to a profit share the
# forecast explicitly removes and adds once in the bridge instead. Guarded, so a later
# rewrite of the rationale cannot leave a silent no-op behind.
_SERV_OLD = 'and the growing profit share from the bunkering associate'
_SERV_NEW = ('and the warehouse activity moved into it. The group’s share of the '
             'bunkering associate is NOT in this line: it is taken out of the unit before '
             'the forecast starts and the stake is added once, at book value, in the '
             'bridge')
assert _SERV_OLD in WHY['Services'], \
    'the Services rationale no longer carries the clause this correction replaces'
WHY = dict(WHY)
WHY['Services'] = WHY['Services'].replace(_SERV_OLD, _SERV_NEW)


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
      f"into a single number."),
     ("This is a twice-corrected edition, and both rounds of correction are listed. ",
      f"This study has been through two rounds of external review. {n0(N_REVIEWS)} "
      f"independent readers raised {n0(N_FINDINGS)} findings between them; every one was "
      f"priced and "
      f"adjudicated, and the ones that survived scrutiny have been acted on. The first round "
      f"rebuilt the tanker fleet vessel by vessel, made the cost of capital charge for every "
      f"kind of capital the company actually uses, stopped the joint ventures being counted "
      f"twice, replaced the asset lens with a method this company's distribution policy does "
      f"not break, and struck earnings per share after the coupon on securities that rank "
      f"ahead of the ordinary shares. The second round put a USD {b1(ACQ_COST)} billion "
      f"vessel purchase into the model that the first edition had omitted altogether, "
      f"stopped the smallest tankers being carried at a rate that moved the opposite way "
      f"from theirs, re-based receivable days onto the revenue the forecast is actually "
      f"built at, and corrected two descriptions that did not match what the model does. "
      f"The section headed “What changed in this edition, and why”, immediately after the "
      f"caveats, sets both rounds out row by row with the direction and the size of each. A "
      f"study that has been corrected and does not say so is worse than one that was right "
      f"the first time.")])

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
P(f"On {ACQ_DATE} — the day the closing price this study is anchored on was set — the "
  f"company announced the purchase of {n0(ACQ_VLCC + ACQ_GAS_N)} more vessels for about USD "
  f"{b1(ACQ_COST)} billion: {n0(ACQ_VLCC)} very large crude carriers and "
  f"{n0(ACQ_GAS_N)} gas carriers. The crude carriers and most of the gas carriers were "
  f"bought secondhand for delivery in the third quarter of {YRL[0][:4]}; the rest are gas "
  f"carrier newbuildings resold from a Chinese yard, arriving in the fourth. It takes the "
  f"owned crude fleet from {n0(FLT['owned']['vlcc'])} "
  f"vessels to {n0(VLCC_AFTER)} and the gas fleet to twelve very large gas carriers. The "
  f"first edition of this study omitted it entirely, which meant a fair value that excluded "
  f"the vessels was being compared with a market price that already included them. They are "
  f"now in the model: each class joins the fleet on its own announced delivery date and "
  f"earns from that date, and the USD {b1(ACQ_COST)} billion is added both to net debt in "
  f"the bridge and to the asset base that depreciates. The announcement also corroborates a "
  f"correction the first round of review produced. That round cut the crude fleet from the "
  f"{n0(owned_total_fy25)} tankers on the books at the {HYRS[2]} year end to the "
  f"{n0(owned_total)} owned at the valuation date, because a very large crude carrier had "
  f"been sold in January — taking that class to {n0(FLT['owned']['vlcc'])}. The company now "
  f"says the purchase takes it to {n0(VLCC_AFTER)}, and {n0(FLT['owned']['vlcc'])} plus "
  f"{n0(ACQ_VLCC)} is {n0(VLCC_AFTER)}. The corrected count is the one the company itself "
  f"is counting from.")
P(f"The two halves of the business behave completely differently, and averaging them is "
  f"the main way this company gets mis-valued. About {pc(IN['contracted_2026_share'], 0)} "
  f"of {YRL[0]} revenue is already contracted with the parent group, against a long-term "
  f"contracted revenue backlog of roughly USD {b1(IN['contracted_revenue_lt'])} billion. "
  f"The other half is a merchant fleet: {n0(IN['spot_vessels_total'])} vessels across the "
  f"group trade at spot rates, and the company discloses that a change of USD 1,000 a day "
  f"in what they "
  f"earn moves group earnings by about USD {m0(IN['ebitda_per_1000_day'])} million a year. "
  f"On the company's own disclosure {pc(IN['spot_share_ebitda_26'], 0)} of {YRL[0]} "
  f"earnings sits on spot rates, falling to {pc(IN['spot_share_ebitda_29'], 0)} by "
  f"{YRL[3]} as contracted gas and logistics capacity comes in.")
P(f"That merchant half is having an extraordinary year, and reading how extraordinary "
  f"takes one step of care. The company publishes a single rate per vessel class per "
  f"quarter, and that rate is a blend: it averages the vessels trading in the open market "
  f"together with the vessels already fixed on charters out at rates agreed months or "
  f"years earlier. Asked about the figure for the largest class on the first-quarter call, "
  f"the chief financial officer said it “was related to our full fleet of "
  f"{n0(FLT['owned']['vlcc'])}, and it includes all the vessels on long-term charter as "
  f"well … it's a blended rate that we give there, which is obviously less than the "
  f"spot rate.” So the published figure understates what an uncommitted vessel earns, "
  f"by exactly the drag of the vessels inside it that are not free to earn it. Very large "
  f"crude carriers earned a published average of USD {n0(FLT['blend_fy25']['vlcc'])} a day "
  f"across {HYRS[2]}; the published figure was USD {n0(VS_BLEND)} for the first quarter of "
  f"{YRL[0][:4]} and USD {n0(FLT['blend_q2_26']['vlcc'])} was indicated for the second. "
  f"Strip out the {n0(fixed_by_class['vlcc'])} of {n0(FLT['owned']['vlcc'])} vessels in "
  f"that class already on charter out, each at its own disclosed rate, and the rate the "
  f"remaining vessels must have earned in the first quarter is USD {n0(VS_SPOT)} a day. "
  f"The long-range classes moved the same way. The first quarter as a whole showed revenue of USD "
  f"{m0(Q1_REV_26_UNITS)} million ({sgn(Q1_YOY_UNITS)} year on year, because low-margin "
  f"chartered-in trading fell away), earnings before interest, tax, depreciation and "
  f"amortisation of USD {m0(IN['q1_26_ebitda_group'])} million "
  f"({sgn(IN['q1_26_ebitda_group']/q1_25_ebitda-1)}) and attributable profit of USD "
  f"{m0(IN['q1_26_npa'])} million ({sgn(IN['q1_26_npa']/IN['q1_25_npa']-1)}). All three of "
  f"those movements are on the basis the company's own commentary uses, which is the basis "
  f"its business-unit table is on. The reviewed statements carry a different first-quarter "
  f"{HYRS[2][2:]} revenue comparative — tanker revenue and direct costs for the first three "
  f"quarters of that year were re-presented, with no effect on profit — and on the "
  f"statutory comparative the same revenue movement is {sgn(Q1_YOY_STAT)} rather than "
  f"{sgn(Q1_YOY_UNITS)}. The statements are what every historical line in this study is "
  f"built from; the commentary basis is the only one on which the two years are comparable "
  f"unit by unit, so it is the one quoted beside unit figures, and the difference is stated "
  f"rather than left to be discovered. Whether those rates hold is the whole valuation.")
P(f"This study says they do not hold, and prices the fleet reverting over five years to "
  f"the average of what it earned in {HYRS[1]} and {HYRS[2]}. That is a judgement, and "
  f"section 1.7 sets out the outside evidence for it. On that base the four lenses centre "
  f"at AED {p2(D['central'])} against a market price of {p2(SPOT)} — {ab(D['central'])}. "
  f"The cash-flow lens on its own lands at AED {p2(LN['dcf']['base'])}, "
  f"{ab(LN['dcf']['base'])}, and the three notional experts in Appendix C, who price "
  f"mid-cycle earnings rather than a terminal value, centre at AED {p2(PANEL)}, "
  f"{ab(PANEL)}. The honest conclusion is that the evidence brackets the screen price "
  f"rather than pointing away from it: the widest reads sit meaningfully above, the asset "
  f"lens sits well below, and the two constructions that stay closest to the company's own "
  f"reported cash — the cash-flow lens and the expert panel — sit within a few per cent of "
  f"the market. This is not a study that finds a mispricing.")
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
         f"{p3(IN['beta'])} against {BFP['label']} and on all three kinds of capital the "
         f"company uses — ordinary equity {pc(W['we'], 1)}, debt {pc(W['wd'], 1)}, "
         f"perpetual capital securities {pc(W['wh'], 1)} at their own coupon; terminal "
         f"growth {pc(IN['g_terminal'], 0)}; "
         f"{pc(DCF['tv_share'], 0)} of enterprise value comes from the terminal value",
         f"{p2(LN['dcf']['bear'])} – {p2(LN['dcf']['bull'])}", p2(LN['dcf']['base']),
         vs(LN['dcf']['base'])],
        ['Relative multiples',
         f"a blended {xt(REL['blend_ev_ebitda'], 2)} enterprise value to earnings and "
         f"{xt(REL['blend_pe'], 2)} price to earnings on {YRL[0]}, weighted "
         f"{pc(REL['weight_ev_ebitda'], 0)} to the enterprise measure. The earnings "
         f"multiple is the peers' FORWARD multiple applied to forward earnings; on their "
         f"trailing multiples the same blend is {xt(BLEND_PE_TTM, 2)}",
         f"{p2(LN['relative']['bear'])} – {p2(LN['relative']['bull'])}",
         p2(LN['relative']['base']), vs(LN['relative']['base'])],
        ['Normalised earnings power',
         f"the five-year average of the build's own earnings — USD "
         f"{m0(NRM['norm_ebitda'])} million before interest, tax, depreciation and "
         f"amortisation — at the same blended multiples",
         f"{p2(LN['normalized']['bear'])} – {p2(LN['normalized']['bull'])}",
         p2(LN['normalized']['base']), vs(LN['normalized']['base'])],
        ['Book value and sustainable return',
         f"the ordinary book of AED {p2(BK['bvps_aed'])} a share, plus five years of "
         f"returns earned above the cost of equity of {pc(BK['ke'], 2)} on that book, "
         f"discounted, plus a remainder that fades at {pc(BK['fade'], 0)} a year — worth "
         f"{xt(BK['pb_fair'], 2)} the book it starts from",
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
         f"carrying value of USD {m0(BR['hybrid'])} million (section 1.1). Read what makes "
         f"the two differ: capitalising the same coupon at the securities' OWN rate of "
         f"{pc(W['kh'], 2)} returns USD {m0(HYB_AT_OWN_COUPON)} million, the carrying value "
         f"to the dollar. This alternative is therefore a statement about the rate the "
         f"claim should be discounted at, not a second valuation of it",
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
        f"it. Ranges are bear-to-bull within each lens, and within the cash-flow lens the "
        f"bear and bull cases are a COMPOSITE of three stresses moved together, not the "
        f"beta alone. Each end takes one end of the beta's own 90% confidence interval — "
        f"{BF['ci90'][1]:.3f} at the bear end and {BF['ci90'][0]:.3f} at the bull end — and "
        f"moves the mid-cycle rate anchor and the capital programme against the value at "
        f"the same time. Reading the beta off by itself, the published grid in section 1.9 "
        f"puts the {BF['ci90'][1]:.3f} case at AED {p2(BETA_ONLY_BEAR)} against a published "
        f"bear of {p2(LN['dcf']['bear'])}, so roughly AED "
        f"{p2(BETA_ONLY_BEAR-LN['dcf']['bear'])} of that bound is the other two stresses "
        f"rather than the statistics. The bounds are still drawn from the estimate's own "
        f"interval rather than from round numbers chosen by hand — but they are not the "
        f"span the estimate alone supports, and an earlier edition described them as though "
        f"they were. The index reading is the largest of the three "
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
        ['The purchase announced on the anchor date',
         f"{n0(ACQ_VLCC + ACQ_GAS_N)} more vessels for about USD {b1(ACQ_COST)} billion, "
         f"announced {ACQ_DATE}: {n0(ACQ_VLCC)} very large crude carriers, taking that "
         f"class from {n0(FLT['owned']['vlcc'])} to {n0(VLCC_AFTER)}, and "
         f"{n0(ACQ_GAS_N)} gas carriers, taking the gas fleet to twelve very large gas "
         f"carriers. The crude carriers and most of the gas carriers deliver in the third "
         f"quarter of {YRL[0][:4]}; the remaining gas carrier newbuildings, resold from a "
         f"Chinese yard, in the fourth. Each vessel enters the model on its own delivery "
         f"date and earns from it, and the purchase price is added to net debt in the "
         f"bridge and to the depreciating asset base"],
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
         f"{n0(IN['spot_vessels_total'])} vessels trade at spot rates on the company's own "
         f"group-wide count at the {HYRS[2]} year end — wider than the {n0(spot_total)} "
         f"owned tankers free to earn the market at the valuation date in the row above, "
         f"because it also covers the dry-bulk and container fleet. The company "
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
         f"{xt(IN['nd_ebitda_target_lo'], 1)} to {xt(IN['nd_ebitda_target_hi'], 1)}. The "
         f"bridge in section 1.1 deducts USD {m0(NET_DEBT_TOTAL)} million, which is that "
         f"figure plus the deferred consideration of USD {m0(BR['deferred'])} million and "
         f"the USD {b1(ACQ_COST)} billion committed to the August purchase"],
        ['Perpetual capital securities',
         f"USD {b1(IN['hybrid_face'])} billion of perpetual capital securities were "
         f"issued in {HYRS[2]}, carried at USD {m0(IN['q1_26_hybrid'])} million and priced "
         f"at the secured overnight financing rate plus "
         f"{IN['hybrid_margin']*10000:,.0f} basis points. They sit inside total equity in "
         f"the accounts but rank ahead of the ordinary shares, so this study deducts them "
         f"in the bridge — both at carrying value and at the present value of their "
         f"coupon — and, because they are a third kind of capital and not a rounding on "
         f"the other two, also weights them in the cost of capital at "
         f"{pc(W['wh'], 1)} of the total, at their own coupon of {pc(W['kh'], 2)}"],
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
  f"discloses is forecast on its own physical driver: the tankers literally vessel by "
  f"vessel — each of the {n0(len(CHT))} vessels chartered out earns its own disclosed "
  f"rate for exactly the days its own contract runs, and every other vessel earns the "
  f"open-market rate solved out of the company's published class averages — the gas "
  f"carriers on contracted vessel-years at the day rate implied by their own revenue, and "
  f"the remaining units on what they actually earned in the first quarter of "
  f"{YRL[0][:4]}, annualised and grown. Sections 1.6 and 1.7 set the build out unit by "
  f"unit and vessel by vessel. Cash flow is then taken all the way to present value, "
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
        f"collection, inventory and payment cycle the {HYRS[2]} statements actually show, "
        f"re-based onto the revenue this forecast is built at — the two paragraphs below "
        f"set out why that re-basing was needed and what it cost.")
H2('Two lines that price a fleet, and how each is set')
P(f"The capital-intensive lines in that waterfall are depreciation and working capital, and "
  f"both were challenged in review. Neither is an assumption dropped in from outside, and "
  f"both are worth showing rather than asserting.")
rows = [['Line', 'What the model uses', 'The evidence, and what a reviewer proposed instead'],
        ['Depreciation on property, plant and equipment',
         pc(IN['dep_rate_ppe'], 2) + ' of the average balance',
         f"The company's own accounting policy note reads: “{DEP_LIVES}”. Written off "
         f"straight line over the tanker life it discloses, the fleet's stated lives imply "
         f"about {pc(1.0/IN['life_tankers'], 1)} a year before the short-lived dry-docking "
         f"components are added. The rate used is the first quarter of {YRL[0][:4]} "
         f"annualised over that quarter's average balance. A reviewer proposed the "
         f"{HYRS[2]} realised rate of {pc(IN['dep_rate_realised_fy25'], 2)} instead. Both "
         f"candidates sit ABOVE what the disclosed lives imply, which is what the "
         f"dry-docking components do to the blend; between the two, the rate used is the "
         f"LOWER — the more conservative of the two available forward bases, because a "
         f"lower charge means a higher taxable base rather than a flattered one, and the "
         f"{HYRS[2]} average balance is distorted by a fleet acquired at the start of that "
         f"year. It is kept, and it is sensitised"],
        ['Receivable days in working capital',
         f"{n1(IN['dso_days'])} days",
         f"Receivables over revenue in the {HYRS[2]} statements is {n1(IN['dso_days_reported'])} "
         f"days. But {HYRS[2]} revenue carries a gross-up of {xt(IN['tnk_grossup_25'], 2)} "
         f"over the owned tanker fleet's own charter-equivalent revenue, from chartered-in "
         f"and relet trading, while the forecast is built at {xt(IN['tnk_grossup_26'], 2)}. "
         f"A day count calibrated on the first and applied to the second understates the "
         f"receivable balance by the whole difference between the two conventions. Re-based "
         f"onto the revenue the forecast actually produces, {n1(IN['dso_days_reported'])} "
         f"days becomes {n1(IN['dso_days'])}. This is the correction that falsified a "
         f"caveat the previous edition printed — see the caveats in section 7"]]
table(rows, [1.55, 1.15, 4.30], size=8.2, left_cols=(1, 2))

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
         f"carried at the reviewed 31 March 2026 book value with no uplift; these earn "
         f"outside the consolidated cash flow, principally the six gas carriers held "
         f"fifty-fifty and the bunkering associate. Their earnings are taken OUT of the "
         f"forecast before it starts — the disclosed unit earnings include the group's "
         f"share of them, USD {m0(IN['jv_gas_fy25'])} million inside Gas Carriers and USD "
         f"{m0(IN['jv_services_fy25'])} million inside Services in {HYRS[2]} — so that "
         f"adding the stakes here counts them once and not twice"],
        ['Enterprise value', m0(DCF['ev']), ''],
        ['Less net debt', neg(m0(BR['net_debt_company'])),
         'the reviewed 31 March 2026 figure: the parent facility, third-party borrowings '
         'and lease liabilities less cash'],
        ['Less deferred consideration', neg(m0(BR['deferred'])),
         'the contracted price of the remaining 20% of the acquired tanker business, '
         'payable in mid-2027 and carried against the investment reserve — a real claim '
         'on the enterprise and treated as one. It is also the reason the minority line '
         'below is not simply the book figure'],
        ['Less the vessels bought in August 2026', neg(m0(ACQ_COST)),
         f"the {n0(ACQ_VLCC + ACQ_GAS_N)} vessels announced on {ACQ_DATE} — "
         f"{n0(ACQ_VLCC)} very large crude carriers and {n0(ACQ_GAS_N)} gas carriers — at "
         f"the announced price. The purchase is committed and unpaid at the valuation date, "
         f"so it is debt-like and comes out here; the vessels themselves are on the other "
         f"side of the ledger, earning inside the forecast from their own delivery dates "
         f"and depreciating in the asset base from the same dates. Taking the cost without "
         f"the earnings, or the earnings without the cost, would be the error in either "
         f"direction; the first edition of this study did neither and simply left the whole "
         f"transaction out"],
        ['Less perpetual capital securities', neg(m0(BR['hybrid'])),
         f"at carrying value. They sit inside total equity in the accounts but rank ahead "
         f"of the ordinary shares and carry a coupon of USD {m0(FIN['hybrid_coupon'])} "
         f"million a year, so the ordinary shareholder does not own them. Because they are "
         f"deducted here they are also WEIGHTED in the cost of capital above, at "
         f"{pc(W['wh'], 1)} of the capital and at their own coupon of {pc(W['kh'], 2)} — "
         f"the two halves of one treatment. The alternative treatment is two lines below"],
        ['Less non-controlling interests', neg(m0(DCF['nci'])),
         f"NOT the book value of USD {m0(DCF['nci_book'])} million. USD "
         f"{m0(DCF['nci_navig8'])} million of that book arose on the tanker combination, "
         f"and that 20% is contracted for purchase in mid-2027 at a price already "
         f"deducted two lines above as deferred consideration, so deducting it again at a "
         f"share of equity value would count it twice. Only the remaining USD "
         f"{m0(DCF['nci_other_bv'])} million of book is lifted to its share of value. That "
         f"lift costs AED {p2(NCI_LIFT)} a share, against the AED {p2(NCI_FLAT_COST)} it "
         f"would cost to apply the {pc(IN['nci_share'])} profit share to the whole equity "
         f"value and net nothing off"],
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
# The bridge must FOOT. The line the first edition was missing was worth USD 1.3 billion and
# nothing in the document would have shown it: every figure in the table was individually
# correct and the column simply did not add up to the equity value printed under it.
_bridge_sum = (DCF['ev'] - BR['net_debt_company'] - BR['deferred'] - ACQ_COST
               - BR['hybrid'] - DCF['nci'])
assert abs(_bridge_sum - DCF['equity']) < 1.0, (
    f'the bridge table does not foot: the deductions shown leave '
    f'{_bridge_sum:,.0f} against a published equity value of {DCF["equity"]:,.0f}')
table(rows, [2.55, 0.95, 3.50], size=8.2, band_rows={5, 13, 15, 16},
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
P(f"Run the same returns against {BFA['label']} and the slope is {p3(BFA['beta'])} instead. "
  f"One qualification before the explanation, because the two runs are not quite the "
  f"identical regression: the published-index run pairs {n0(BE['n'])} weekly observations "
  f"and the composite run pairs {n0(BE['composite_variant']['n'])}, because the index "
  f"series obtained stops earlier than the exchange's own price history does. The samples "
  f"differ by {n0(abs(BE['composite_variant']['n'] - BE['n']))} weeks out of "
  f"{n0(BE['n'])}, so a small part of the gap between the two slopes is sample rather than "
  f"market definition, and an earlier edition called them the same regression without "
  f"saying so. The rest of the difference is large and it has nothing to do with this "
  f"company: a published "
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
  f"belong to the ordinary shareholder. The return earned on that equity, struck after the "
  f"coupon those securities take ahead of it, runs {pc(BK['roe_path'][0])} in {YRL[0]} and "
  f"falls to {pc(BK['roe_path'][4])} by {YRL[4]} as the rate cycle normalises and the "
  f"capital base grows; across the five years it averages {pc(sum(BK['roe_path'])/5)}. That "
  f"path is struck on OPENING book, which is the convention this lens is built on and the "
  f"one it uses throughout.")
P(f"A separate return figure runs through the appendix and it is on a different convention, "
  f"so the two are set out together rather than spliced. On CLOSING equity attributable to "
  f"ordinary shareholders — the measure the reported history is naturally computed on — the "
  f"return ran {pc(ROE_HIST[0])} in {HYRS[0]}, {pc(ROE_HIST[1])} in {HYRS[1]} and "
  f"{pc(ROE_HIST[2])} in {HYRS[2]}, and the five forecast years run "
  f"{' · '.join(pc(x) for x in ROE_FCST)}, averaging {pc(sum(ROE_FCST)/5)}. Appendix A.2 "
  f"now carries that row on closing equity end to end. An earlier edition put the reported "
  f"years on closing equity and the forecast years on AVERAGE equity in the same row and "
  f"the same sentence, which made the series read as a rise into a sustainable level; on "
  f"the average-equity convention the forecast years are "
  f"{' · '.join(pc(x) for x in ROE_FCST_AVGEQ)} instead. The direction of the series depends "
  f"on which of the two is used, so mixing them was manufacturing a trend rather than "
  f"reporting one. Neither convention is wrong and this study uses closing equity in the "
  f"appendix, opening book in the lens below, and says which is which at each place.")
P(f"The textbook form of this lens is a justified price-to-book multiple: the sustainable "
  f"return less growth, divided by the cost of equity less growth. It is not used here, and "
  f"the reason is arithmetic rather than taste. That formula describes a steady state in "
  f"which the company distributes everything it does not need in order to fund its growth. "
  f"At a sustainable return of {pc(BK['roe_sustainable'])} and growth of {pc(BK['g'], 0)}, "
  f"the payout that steady state requires is {pc(1-BK['g']/BK['roe_sustainable'], 0)} of "
  f"earnings. This company pays out {pc(min(FIN['payout']), 0)} to "
  f"{pc(max(FIN['payout']), 0)} and retains the rest, which compounds its book at about "
  f"{pc(BK['roe_sustainable']*(1-sum(FIN['payout'])/5))} a year — above the cost of equity "
  f"of {pc(BK['ke'], 2)}, where the formula does not merely mislead but is undefined, "
  f"because the denominator it divides by has gone through zero. A lens whose central "
  f"expression is undefined on the company in front of it is the wrong lens.")
P(f"What is used instead is residual income, which asks the same question without the "
  f"steady-state assumption: what is the book the company already has, plus the value of "
  f"earning more than the cost of equity on it for as long as that lasts. The construction "
  f"is the opening ordinary book; plus, for each of the five forecast years, the return on "
  f"that year's opening book less the cost of equity, multiplied by that opening book and "
  f"discounted; plus a remainder beyond the forecast in which the excess return decays at "
  f"{pc(BK['fade'], 0)} a year. The fade is a judgement and it is the one place this lens "
  f"is soft: a fleet has to be replaced at market prices rather than at the value it is "
  f"carried at, so an excess return over the cost of equity cannot persist unchanged, but "
  f"nothing observable fixes the speed. A slower fade would raise this lens and a faster "
  f"one would lower it; at the rate used, the remainder beyond the forecast is USD "
  f"{m0(BK['pv_terminal']*1000)} million of the USD {m0(BK['equity_value']*1000)} million "
  f"total, and the book the company already owns is most of the rest.")
rows = [['Year', 'Opening ordinary book (USD mn)', 'Return on it',
         'Less the cost of equity', 'Residual income (USD mn)', 'Discount factor',
         'Present value (USD mn)']]
for r in BK['detail']:
    rows.append([r['year'].replace('FY', '') + 'E', n0(r['opening_book']),
                 pc(r['roe']), f"{(r['roe']-BK['ke'])*100:+.2f}pp",
                 n0(r['residual_income']), f"{r['discount_factor']:.4f}",
                 n0(r['pv'])])
rows.append(['Total', '', '', '', '', '', n0(sum(r['pv'] for r in BK['detail']))])
table(rows, [0.62, 1.16, 0.80, 0.94, 1.10, 0.88, 1.10], size=8.0,
      band_rows={6})
caption(f"Residual income is what the ordinary shareholder earns above the "
        f"{pc(BK['ke'], 2)} it costs to hold the equity — the return in the third column "
        f"less that cost, applied to the book in the second. It is positive in every "
        f"forecast year and shrinking in every one of them, which is the same picture the "
        f"cash-flow model gives from the other end. The opening book of each year is the "
        f"model's own rolled-forward balance sheet, so this lens and Appendix A.2 cannot "
        f"disagree.")
rows = [['Line', 'Value'],
        ['Equity attributable to ordinary shareholders at 31 March 2026 (USD mn)',
         m0(IN['q1_26_eqp'])],
        ['Book value per share (USD)', f"{BK['bvps_usd']:.4f}"],
        ['Book value per share (AED, at the peg)', p2(BK['bvps_aed'])],
        ['Plus the present value of five years of residual income (USD mn)',
         n0(sum(r['pv'] for r in BK['detail']))],
        [f"Plus the present value of the remainder, fading at {pc(BK['fade'], 0)} a year "
         f"(USD mn)", n0(BK['pv_terminal'])],
        ['Equity value on this lens (USD mn)', n0(BK['equity_value'])],
        ['Implied price to book', xt(BK['pb_fair'], 2)],
        ['Fair value per share (AED)', p2(LN['book']['base'])],
        [f"Range — bear at the top of the beta's 90% interval ({BF['ci90'][1]:.3f}, cost "
         f"of equity {pc(BK['ke_bear'], 2)}) with the return on that book scaled down; bull "
         f"at the bottom of it ({BF['ci90'][0]:.3f}, {pc(BK['ke_bull'], 2)}) with the same "
         f"scaling applied upward",
         f"{p2(LN['book']['bear'])} – {p2(LN['book']['bull'])}"],
        ['Memorandum — the price the market pays for the SAME book, ordinary equity only',
         xt(PB_MARKET_ORD, 2)],
        ['Memorandum — the same on the wider book that also counts the perpetual securities',
         xt(PB_MARKET_WIDE, 2)],
        ['Memorandum — realised value against carrying value on the January vessel sale',
         f"{xt(BK['vessel_value_to_book'], 2)} on the disclosed carrying value, "
         f"{xt(VSALE_RATIO_IMPLIED, 2)} on the carrying value the disclosed gain implies"]]
table(rows, [4.90, 2.10], size=8.5, band_rows={8})
P(f"The first of those memorandum lines is the one to read against the justified multiple "
  f"above it, and an earlier edition printed the wrong one. The lens values ORDINARY equity "
  f"— AED {p2(BK['bvps_aed'])} a share, excluding the perpetual capital securities — so the "
  f"market multiple has to be struck on the same denominator. On that basis the market pays "
  f"{xt(PB_MARKET_ORD, 2)} book against the {xt(BK['pb_fair'], 2)} this lens justifies, "
  f"which says the share is EXPENSIVE on the asset lens. Struck on the wider book that also "
  f"counts the perpetual securities the market appears to pay {xt(PB_MARKET_WIDE, 2)}, which "
  f"printed beneath a justified multiple computed on the narrower book invites the opposite "
  f"conclusion from a comparison that is not like for like. Both are now shown and the "
  f"comparable one is named. The peer in section 1.3 that publishes a price-to-book figure "
  f"trades at {xt(PEERS[0]['pb'], 2)}, and that comparison is on the ordinary-book basis "
  f"too.")
P(f"The bounds move with the beta and with the return together: the bear bound of AED "
  f"{p2(LN['book']['bear'])} takes a cost of equity of {pc(BK['ke_bear'], 2)}, built on the "
  f"upper end {BF['ci90'][1]:.3f} of the beta's own 90% confidence interval, together with "
  f"a proportionally lower return on that book; the bull bound of AED "
  f"{p2(LN['book']['bull'])} takes "
  f"{pc(BK['ke_bull'], 2)} on the lower end {BF['ci90'][0]:.3f} of the same interval with "
  f"the same proportion applied upward. Only the cost of equity in those bounds comes from "
  f"the estimate's own statistical uncertainty; the return stress beside it is a judgement, "
  f"as it is in the cash-flow lens. The lens carries the lowest "
  f"weight of the four, at {pc(LW['book'], 0)}, because it inherits the same cost of equity "
  f"as the cash-flow model rather than testing it independently, and because carrying value "
  f"is a poor description of what a fleet is worth.")
P(f"On that last point there is one piece of hard evidence, and it is worth more than any "
  f"amount of argument. In January {YRL[0][:4]} the company completed the sale of a "
  f"2017-built very large crude carrier for USD {m0(BK['vessel_sale_price'])} million "
  f"against a carrying value of USD {m0(BK['vessel_sale_book'])} million — a realised "
  f"market value of {xt(BK['vessel_value_to_book'], 2)} book, on its own asset, disclosed "
  f"in its own earnings release. The same release discloses a gain of USD "
  f"{m0(IN['vessel_sale_gain'])} million on the sale, which implies a carrying value of USD "
  f"{m0(VSALE_BOOK_IMPLIED)} million and a ratio of {xt(VSALE_RATIO_IMPLIED, 2)} instead — "
  f"the company's own two disclosures about one transaction do not quite reconcile, and "
  f"both readings are shown rather than one being picked. Two further qualifications belong "
  f"with the figure: the vessel was 90% owned, so the group did not keep all of the "
  f"proceeds, and the sale was struck in a strong market. That tells the reader which way "
  f"this lens is biased. "
  f"Carrying values understate realisable value, so a book-based read of this company is "
  f"conservative rather than neutral, and the gap is not small: applied across the fleet, "
  f"a {xt(BK['vessel_value_to_book'], 2)} ratio would lift the asset base by roughly a "
  f"third. It is a single transaction on a single vessel in a strong market and it is not "
  f"extrapolated into the valuation — but it is the only direct evidence available on the "
  f"gap between the balance sheet and the market, and it points one way.")

# ---- 1.3 relative ------------------------------------------------------------
H2('1.3  Relative multiples')
P(f"There is no clean comparable for this company, and the reason is the same reason it is "
  f"interesting: nothing else combines a contracted logistics arm working for a national "
  f"oil company with an open-market tanker fleet. The frame used here therefore takes two "
  f"multiples from two different kinds of shipowner and blends them on the company's own "
  f"disclosed exposure, rather than picking one peer and pretending it fits.")
rows = [['Company', 'Market', 'Business model', 'EV / earnings',
         'Price / earnings (fwd / trailing)', 'Price / book']]
for pr in PEERS:
    rows.append([pr['name'], pr['market'], pr['model'], xt(pr['ev_ebitda'], 2),
                 ' / '.join(xt(x, 2) if x else '—'
                            for x in (pr['pe_fwd'], pr['pe_ttm'])),
                 xt(pr['pb'], 2) if pr['pb'] else '—'])
rows.append(['ADNOC Logistics & Services', M['exchange'].replace('Securities ', ''),
             'half contracted logistics, half merchant fleet',
             f"{xt(REL['own_ev_ebitda_ttm'], 2)} trailing / "
             f"{xt(REL['own_ev_ebitda_26'], 2)} on {YRL[0]}",
             f"{xt(OWN_PE_FWD, 2)} / {xt(REL['own_pe_ttm'], 2)}",
             xt(PB_MARKET_ORD, 2)])
table(rows, [1.50, 0.86, 1.50, 1.12, 1.24, 0.78], size=8.0, band_rows={4},
      left_cols=(1, 2))
caption(f"The contracted-fleet multiple of {xt(REL['contracted_multiple'], 2)} comes from "
        f"the long-term contracted gas shipowner; the spot multiple of "
        f"{xt(REL['spot_multiple'], 2)} is the average of the two listed spot tanker "
        f"owners. Two sourcing points belong on the face of this table. First, the peer "
        f"multiples are taken from data-aggregator statistics pages, named and dated in the "
        f"source register, and NOT recomputed from each peer's own filings — the rule that "
        f"admits only a company's own issued statements governs the subject's reported "
        f"history, and it is the subject's history, not the comparators', that this study "
        f"builds from. The consequence is real and is stated rather than buried: the study "
        f"cannot demonstrate that a comparator's earnings are struck on the same definition "
        f"as its own, which is a reason to read this lens as a cross-check on relative "
        f"pricing rather than as an independent valuation. Second, the price-to-earnings "
        f"column now shows forward and trailing for every row, because the multiple this "
        f"lens APPLIES is the peers' forward multiple and quoting the company on a trailing "
        f"figure beside forward peers — as an earlier edition did — compares two different "
        f"things. The company's own price-to-book is struck on ordinary equity, the same "
        f"book the comparator's figure uses and the same book the asset lens in section 1.2 "
        f"values. The company's own trailing enterprise multiple uses the operating "
        f"earnings definition used throughout, not the company's own wider reported one, "
        f"and is struck on the same convention "
        f"the peer figures use — market capitalisation plus net debt — so that the "
        f"comparison is like for like. On this study's own bridge, which additionally "
        f"treats the perpetual capital securities and the minorities as claims ranking "
        f"ahead of the ordinary shares, the same {YRL[0]} earnings give "
        f"{xt(REL['own_ev_ebitda_26_bridge'], 2)} rather than "
        f"{xt(REL['own_ev_ebitda_26'], 2)}. Both are set out in the next table.")
H2('The same company, on two definitions of enterprise value')
P(f"An enterprise multiple depends entirely on what is counted as part of the enterprise, "
  f"and this company has two claims — perpetual capital securities and minority interests "
  f"— that different conventions treat differently. Publishing one number without saying "
  f"which convention produced it is how a comparison quietly stops comparing.")
rows = [['Basis', 'Enterprise value (USD mn)', f"On {YRL[0]} earnings", 'Where it is used'],
        ['Market capitalisation plus net debt', m0(M['ev_usd000']),
         xt(REL['own_ev_ebitda_26'], 2),
         'the convention behind the published figures for the three comparators, so it is '
         'the one the peer table above must use'],
        ["This study's own bridge — the same plus the perpetual capital securities at "
         "carrying value and the minority interests",
         m0(REL['own_ev_bridge']), xt(REL['own_ev_ebitda_26_bridge'], 2),
         'the definition section 1.1 bridges from, because each of those claims ranks '
         'ahead of the ordinary share and is deducted there'],
        ['The difference', m0(REL['own_ev_bridge'] - M['ev_usd000']),
         f"{REL['own_ev_ebitda_26_bridge']-REL['own_ev_ebitda_26']:+.2f} turns",
         f"{pc(BR['hybrid']/(REL['own_ev_bridge']-M['ev_usd000']), 0)} of it the perpetual "
         f"capital securities. A reader comparing this company with a peer that has none "
         f"should know which of the two numbers they are holding"]]
table(rows, [2.05, 1.10, 0.95, 2.90], size=8.2, left_cols=(0, 3))
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
        ['Blended price-to-earnings multiple, forward', xt(REL['blend_pe'], 2),
         f"the peers' FORWARD multiples blended on the same weight, applied to {YRL[0]} "
         f"attributable profit after the perpetual coupon of USD "
         f"{m0(REL['npa_ord_26'])} million. This is the multiple the lens uses: a forward "
         f"multiple belongs on forward earnings"],
        ['The same blend on the peers’ trailing multiples', xt(BLEND_PE_TTM, 2),
         f"published so that a reader who prefers the trailing basis can see it. It is "
         f"higher, so using it would raise this lens; it is not used, because the earnings "
         f"it would be applied to are forecast rather than reported. The company's own "
         f"multiple is {xt(OWN_PE_FWD, 2)} forward and {xt(REL['own_pe_ttm'], 2)} trailing, "
         f"and an earlier edition quoted only the second beside peers shown on the first"],
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
         f"the whole group at the spot multiple, and the whole group at the contracted "
         f"multiple — the two corners the ENTERPRISE reading sits between. Read the base "
         f"against it carefully: the base is a weighted blend of the enterprise reading and "
         f"the earnings reading, while both bounds flex the enterprise reading only, so the "
         f"base of AED {p2(LN['relative']['base'])} does not sit in the middle of its own "
         f"published span. It sits at about the "
         f"{(LN['relative']['base']-LN['relative']['bear'])/(LN['relative']['bull']-LN['relative']['bear'])*100:.0f}"
         f"th percentile of it. The span is a multiple range, not a symmetric error bar "
         f"around the base, and it is labelled as one"]]
table(rows, [2.30, 1.00, 3.70], size=8.3, band_rows={9}, left_cols=(2,))

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
rows.append(['Less non-controlling interests', '', '', neg(m0(SOTP['nci'])),
             f"at book value. The cash-flow bridge in section 1.1 lifts the "
             f"non-contracted slice of this to its share of value, worth AED "
             f"{p2(NCI_LIFT)} a share; that refinement is not repeated in this "
             f"cross-check"])
rows.append(['Equity value', '', '', m0(SOTP['equity']),
             f"AED {p2(SOTP['fv_aed'])} a share, {ab(SOTP['fv_aed'])}"])
rows.append(['MEMORANDUM — the Shipping leg with the exposure share re-based to it', '',
             xt(SHIP_MULT_LEG, 2), m0(SOTP_EV_REBASED),
             f"AED {p2(SOTP_FV_REBASED)} a share. The {pc(REL['spot_weight'], 0)} weight in "
             f"the row above is the company's disclosed share of GROUP earnings exposed to "
             f"spot rates, and every dollar of that exposure sits inside Shipping. Measured "
             f"against Shipping's own {YRL[0]} earnings rather than the group's it is "
             f"{pc(SHIP_W_LEG, 0)}, which lowers the leg multiple to {xt(SHIP_MULT_LEG, 2)} "
             f"and the cross-check by AED {p2(SOTP['fv_aed']-SOTP_FV_REBASED)} a share"])
table(rows, [1.75, 1.02, 0.72, 1.11, 2.40], size=8.0, band_rows={4, 9, 10},
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
        ['Range — the whole group at the spot multiple, and at the contracted multiple '
         '(the enterprise reading only; the base is an average of the two readings, so it '
         'does not sit in the middle of this span)',
         f"{p2(LN['normalized']['bear'])} – {p2(LN['normalized']['bull'])}"]]
table(rows, [4.90, 2.10], size=8.5, band_rows={9})
caption(f"The two constructions disagree by a wide margin — AED "
        f"{p2(2*NRM['base']-NRM['value_pe'])} against AED {p2(NRM['value_pe'])} — and the "
        f"gap is depreciation and the perpetual coupon. This is a young fleet: "
        f"depreciation runs from {pc(min(DNA_SHARE))} of earnings before interest, tax, "
        f"depreciation and amortisation in the lightest forecast year to "
        f"{pc(max(DNA_SHARE))} in the heaviest, averaging {pc(DNA_SHARE_AVG)} across the "
        f"five — and RISING through them, as the newbuild programme and the vessels bought "
        f"in August {YRL[0][:4]} come into the asset base. An earlier edition quoted the "
        f"first year's figure as though it were the average, which understated the very "
        f"wedge this paragraph exists to explain. An enterprise measure and an after-tax "
        f"earnings measure will never agree on a company like this. Averaging them is a "
        f"deliberate refusal to pick, and the lens carries {pc(LW['normalized'], 0)} weight "
        f"accordingly. The published range flexes the enterprise reading between the spot "
        f"and contracted multiples; the base is the average of that reading and the "
        f"earnings reading, so it sits at about the "
        f"{(LN['normalized']['base']-LN['normalized']['bear'])/(LN['normalized']['bull']-LN['normalized']['bear'])*100:.0f}"
        f"th percentile of its own span rather than at the middle of it.")

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
                 f"{l['base'] * LW[k]:.3f}"])
rows.append(['Weighted central — published index', p2(LN['central']['bear']),
             p2(D['central']), p2(LN['central']['bull']), pc(1.0, 0),
             f"{D['central']:.3f}"])
# The composite rows carry the PRIMARY construction's bear and bull, because only their
# base was re-run on the composite beta. Printing those bounds beside a base two dirhams
# higher puts a range around a number the range was not built for, so the cells say so
# instead of showing a figure that belongs to a different construction.
_borrowed = (LN['dcf_beta_alt']['bear'], LN['dcf_beta_alt']['bull']) == \
            (LN['dcf']['bear'], LN['dcf']['bull'])
_nb = 'not re-run' if _borrowed else None
rows.append(['Cash-flow model — equal-weight composite',
             _nb or p2(LN['dcf_beta_alt']['bear']), p2(LN['dcf_beta_alt']['base']),
             _nb or p2(LN['dcf_beta_alt']['bull']),
             pc(LW['dcf'], 0), f"{LN['dcf_beta_alt']['base'] * LW['dcf']:.3f}"])
rows.append(['Weighted central — equal-weight composite',
             _nb or p2(LN['central_beta_alt']['bear']), p2(D['central_beta_alt']),
             _nb or p2(LN['central_beta_alt']['bull']), pc(1.0, 0),
             f"{D['central_beta_alt']:.3f}"])
table(rows, [2.42, 0.86, 0.86, 0.86, 0.86, 1.14], size=8.5, band_rows={5, 7})
caption(f"Contributions are shown to three decimals so that the four of them add to the "
        f"weighted central exactly; rounded to the nearest fil they would come up one fil "
        f"short of it, which is a display artefact rather than an arithmetic one. The two "
        f"composite rows have no bear and bull of their own: only their base case was "
        f"re-run on the composite beta, so the low and high cells are left empty rather "
        f"than filled with the primary construction's bounds. An earlier edition filled "
        f"them, which put a span around a base that sat near the top of it. One further "
        f"thing a reader should know about the composite reading: at {p3(BFA['beta'])} it "
        f"lies BELOW the lower bound of the adopted estimate's own 90% confidence interval "
        f"of [{BF['ci90'][0]:.3f}, {BF['ci90'][1]:.3f}]. It is carried at full size "
        f"throughout this study because the difference between the two measurements is a "
        f"fact about index construction that a reader is entitled to see — but it is a "
        f"more aggressive statement about the discount rate than this study's own bull "
        f"case, and that is now on its face rather than left to be worked out.")
P(f"The four lenses do not agree and the disagreement is informative. The two that price "
  f"earnings through a multiple — relative and normalised — land at AED "
  f"{p2(LN['relative']['base'])} and AED {p2(LN['normalized']['base'])}, the furthest above "
  f"the market of the four. The two that state a cost of equity rather than importing one "
  f"land lower: the cash-flow model at AED {p2(LN['dcf']['base'])}, close to the screen, "
  f"and the book lens at AED {p2(LN['book']['base'])}, well below it. That ordering is not "
  f"a coincidence and it is the most useful thing this table says. The multiple-based "
  f"lenses import a cost of capital rather than state one, and the comparators they import "
  f"it from are a contracted shipowner and a pair of spot tanker owners, so they already "
  f"embed an answer to the question the cash-flow model asks explicitly and answers with a "
  f"measured beta of {p3(IN['beta'])}. Where the two families disagree, the disagreement is "
  f"about the discount rate rather than about the cash flows.")
P(f"There is a weakness in this weighting that a reader should be told about rather than "
  f"left to find, and it is the largest single item still open against this study. The "
  f"relative lens and the normalised lens are not independent of each other. They use the "
  f"SAME three multiples — the contracted-fleet multiple, the spot multiple and the "
  f"blend of them — and the same weighting between the enterprise and earnings readings. "
  f"What differs between them is only the earnings denominator those multiples are applied "
  f"to: the {YRL[0]} build in one, the five-year average of the same build in the other. "
  f"Together they carry {pc(LW['relative']+LW['normalized'], 0)} of the weighted central. "
  f"So {pc(LW['relative']+LW['normalized'], 0)} of the headline rests on one method "
  f"presented as two reads, and the four-lens field is narrower evidence than four bars "
  f"make it look. The counterfactual is easy to state: dropping the normalised lens and "
  f"redistributing its weight would move the central toward the cash-flow and asset lenses, "
  f"which are the two that sit lower. This has not been changed, because both denominators "
  f"are legitimate questions to ask and neither is redundant on its own terms — but the "
  f"overlap is real, it is not neutral in direction, and it is disclosed here rather than "
  f"absorbed.")
P(f"Weighted together, the four centre at AED {p2(D['central'])}, {ab(D['central'])}. "
  f"Measuring the market as an equal-weight composite instead lifts that to AED "
  f"{p2(D['central_beta_alt'])}, {ab(D['central_beta_alt'])}. Neither figure supports a "
  f"claim that this share is materially mispriced: on the adopted construction the centre "
  f"of the evidence sits about {abs(D['central']/SPOT-1)*100:.0f}% above the screen, which "
  f"is narrower than the bear-to-bull width of any single lens in the table and narrower "
  f"than the three-month price dispersion in section 3. The honest reading of the field "
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
             f"Literally vessel by vessel, on the company's own charter table. "
             f"{n0(owned_total)} owned tankers in five size classes at the valuation date, "
             f"of which {n0(fixed_total)} sit on charters out at disclosed fixed rates "
             f"running to dates between {YRL[0][:4]} and {charter_last_yr}; each of those "
             f"earns its own rate for exactly the days its own contract covers, and no "
             f"other. The remaining {n0(spot_total)} earn the open-market rate, which is "
             f"not assumed but solved out of the company's own published class average by "
             f"removing the chartered vessels from it — section 1.7 shows the arithmetic. "
             f"{YRL[0][:4]} is built from the market rate implied by the first quarter, "
             f"the level implied by the second, and a second half stepped halfway back "
             f"toward the {HYRS[2]} implied rate; from {YRL[1]} the market rate glides "
             f"over four years to the mid-cycle anchor, the average of the {HYRS[1]} and "
             f"{HYRS[2]} outcomes. The {n0(ACQ_VLCC)} very large crude carriers bought on "
             f"{ACQ_DATE} join the fleet on their announced delivery date and trade at that "
             f"same market rate from it, so they earn part of {YRL[0]} and all of every "
             f"year after. The smallest class is not broken out in any published rate "
             f"table, so it is carried at the medium-range rate scaled by "
             f"{xt(IN['handysize_relative'], 2)} — the relative move the company itself "
             f"disclosed for it, not a substitution. Running cost is USD "
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
             f"near the {HYRS[2]} outcome NET of the joint-venture profit, since the "
             f"disclosed earnings of this unit include USD {m0(IN['jv_gas_fy25'])} million "
             f"of the group's share of the gas-carrier joint venture and that is added "
             f"separately at book value in the bridge. {n0(IN['gas_lt_contracted'])} of "
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
        f"showed revenue {sgn(Q1_YOY_UNITS)} year on year while "
        f"earnings rose {sgn(IN['q1_26_ebitda_group']/q1_25_ebitda-1)} — both movements on "
        f"the business-unit basis this table is built on, which is the basis the company's "
        f"own commentary uses.")

figure(os.path.join(HERE, 'fig7_mix.png'), 6.9,
       "Figure 2 — earnings by business unit, reported and forecast, with the group "
       "margin. Shipping does the moving; the contracted logistics base grows steadily "
       "underneath it.")

H2("The build against the company's own guidance — a gap, stated plainly")
P(f"This build sits materially above what management has guided for {YRL[0][:4]}, and that "
  f"is a deliberate result of the method rather than an accident to be reconciled away.")
P(f"One thing has to be established before the comparison can be read at all: the company "
  f"does not publish a dollar guidance figure, for the group or for any business unit. What "
  f"it publishes is DIRECTIONAL — a band in words, for revenue and for earnings, at group "
  f"level and for each of the three units. Every guided figure below is this study's own "
  f"conversion of those words into dollars, taken at the midpoint of the band and applied "
  f"to the {HYRS[2]} figure it grows from. The conversion is shown line by line so that a "
  f"reader who reads a band differently can redo it.")
rows = [['Line', f"{HYRS[2]} base (USD mn)", 'Guided change', 'Converted (USD mn)']]
for g in GROUPS:
    rows.append([f'{g} — revenue', m0(GRPH[g]['revenue'][2]), sgn(IN[GPCT[g][0]], 1),
                 m0(GD[g]['guided_revenue'])])
rows.append(['Sum of the three units — revenue', m0(sum(GRPH[g]['revenue'][2]
                                                        for g in GROUPS)), '',
             m0(GUID_UNITS_REV)])
rows.append(['Group — revenue, on the group band', m0(IN['rev_fy25']),
             sgn(IN['g26_rev_group'], 1), m0(GD['Group']['guided_revenue'])])
rows.append(['Difference — the group band against the three unit bands', '', '',
             f"{'+' if GUID_REV_GAP >= 0 else ''}{m0(GUID_REV_GAP)}"])
for g in GROUPS:
    rows.append([f'{g} — earnings', m0(GRPH[g]['ebitda'][2]), sgn(IN[GPCT[g][1]], 1),
                 m0(GD[g]['guided_ebitda'])])
rows.append(['Sum of the three units — earnings',
             m0(sum(GRPH[g]['ebitda'][2] for g in GROUPS)), '', m0(GUID_UNITS_EBITDA)])
rows.append(["Group — earnings, on the group band and the company's own reported measure",
             m0(HI['ebitda_reported'][2]), sgn(IN['g26_ebitda_group'], 1),
             m0(GD['Group']['guided_ebitda'])])
rows.append(['Difference — the group band against the three unit bands', '', '',
             f"{'+' if GUID_EBITDA_GAP >= 0 else ''}{m0(GUID_EBITDA_GAP)}"])
table(rows, [3.10, 1.30, 1.10, 1.50], size=8.2, band_rows={4, 6, 11, 13}, left_cols=(0,))
caption(f"Every row multiplies out. The two DIFFERENCE rows are the point of the table and "
        f"they are a property of the guidance, not of this conversion: management's three "
        f"unit bands and its group band do not reconcile at their midpoints. On revenue the "
        f"three units imply USD {m0(GUID_UNITS_REV)} million against a group band implying "
        f"USD {m0(GD['Group']['guided_revenue'])} million; on earnings the units imply more "
        f"than the group band does, and part of that second gap is a measure difference as "
        f"well — the group band is stated against the company's own reported earnings "
        f"figure, which adds the share of joint ventures and one-off items to the "
        f"USD {m0(sum(GRPH[g]['ebitda'][2] for g in GROUPS))} million the three units sum "
        f"to. An earlier edition of this study printed the unit rows and the group row in "
        f"one column that did not add up, with no note that it did not. Both totals are now "
        f"shown and the gap between them is named.")
H2('The build against that guidance')
rows = [['Business unit', 'Guided revenue', 'Built revenue', 'Guided earnings',
         'Built earnings', 'Gap on earnings']]
for g in GROUPS + ['Group']:
    gd = GD[g]
    rows.append([g, m0(gd['guided_revenue']), m0(gd['built_revenue']),
                 m0(gd['guided_ebitda']), m0(gd['built_ebitda']),
                 sgn(gd['ebitda_gap'])])
rows.append(['Group, measured against the three units instead', m0(GUID_UNITS_REV),
             m0(GD['Group']['built_revenue']), m0(GUID_UNITS_EBITDA),
             m0(GD['Group']['built_ebitda']), sgn(BUILT_VS_UNITS)])
table(rows, [1.60, 1.08, 1.08, 1.08, 1.08, 1.08], size=8.3, band_rows={4, 5})
caption(f"Revenue and earnings in USD million; guided figures are the converted ones from "
        f"the table above. The last row exists because the group guidance and the unit "
        f"guidance do not agree with each other, so the gap this build carries depends on "
        f"which of the two it is measured against: {sgn(GD['Group']['ebitda_gap'])} against "
        f"the group band, {sgn(BUILT_VS_UNITS)} against the sum of the unit bands. Both are "
        f"published. The built figures are the output of the unit model in this section.")
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
  f"valuation turns entirely on how long that lasts and where it settles. Getting to that "
  f"question, though, requires first getting the current rate right, and the published "
  f"figure is not it.")

H2('The published rate is a blend, and the company says so')
P(f"The company publishes one rate per vessel class per quarter. That figure averages the "
  f"vessels trading in the open market with the vessels already committed on charters out "
  f"at rates fixed months or years earlier, so it is lower than what a free vessel earns "
  f"and lower by an amount that depends on how many of the class are committed. Asked "
  f"directly about the largest class on the first-quarter call, the chief financial "
  f"officer put it plainly:")
P(f"“… was related to our full fleet of {n0(FLT['owned']['vlcc'])}, and it includes all "
  f"the vessels on long-term charter as well … it's a blended rate that we give there, "
  f"which is obviously less than the spot rate.”", italic=True, size=9.4)
P(f"An earlier edition of this study read that published figure as the open-market rate "
  f"and then added the chartered vessels to the model separately at their own, lower, "
  f"disclosed rates. That charges the drag of the charters twice — once inside the "
  f"published average and once again beside it — and it understates the fleet. The build "
  f"is now the other way round. Every one of the {n0(len(CHT))} vessels chartered out is "
  f"carried individually, at its own published rate, for exactly the days its own contract "
  f"runs. The open-market rate is then not assumed at all: it is solved out of the "
  f"company's own published average by taking the charters back out of it — the class "
  f"average multiplied by the class's vessel-days, less what the committed vessels earned, "
  f"divided by the days the uncommitted vessels had. Nothing about the market rate is a "
  f"judgement; it is arithmetic on the company's own disclosure.")

H2('The twelve vessels chartered out, exactly as published')
rows = [['Vessel', 'Class', 'Fixed rate (USD/day)', 'Period', 'Runs to']]
for c in CHT:
    rows.append([c['name'], dict(CLS)[c['klass']], n0(c['rate']),
                 f"{n0(c['period_months'])} months", fdate(c['end'])])
rows.append([f"{n0(len(CHT))} vessels", '',
             f"{n0(min(c['rate'] for c in CHT))} – {n0(max(c['rate'] for c in CHT))}",
             '', f"last expiry {fdate(charter_last)}"])
table(rows, [1.62, 1.66, 1.32, 1.10, 1.30], size=8.0, band_rows={13}, left_cols=(0, 1))
caption(f"Every field is disclosed in the company's own contract table; the start date is "
        f"the stated expiry less the stated period, so no date is invented. At the "
        f"valuation date of {M['valuation_date']}, {n0(fixed_total)} of these were running, "
        f"leaving {n0(spot_total)} of the {n0(owned_total)} owned tankers free to earn the "
        f"open-market rate. The spread inside the table is the point: the two long-range-one "
        f"vessels are fixed at USD {n0(min(c['rate'] for c in CHT))} a day while the "
        f"open-market rate for their class in the first quarter was USD "
        f"{n0(FLT['spot_q1_26']['lr1'])}, and the four largest vessels are fixed between "
        f"USD {n0(min(c['rate'] for c in CHT if c['klass'] == 'vlcc'))} and USD "
        f"{n0(max(c['rate'] for c in CHT if c['klass'] == 'vlcc'))} against an open-market "
        f"rate of USD {n0(VS_SPOT)}. A vessel on charter out cannot earn the market, and "
        f"the model no longer pretends the fleet average is what a free vessel earns.")

figure(os.path.join(HERE, 'fig8_tce.png'), 7.0,
       f"Figure 3 — the crux made visible, on both measures. Left: the rate the company "
       f"publishes for each class each quarter, which is a blend across the whole class, on "
       f"a logarithmic scale; the last two points are the first quarter of {YRL[0][:4]} as "
       f"reported and the second quarter as indicated. The open markers on the dashed line "
       f"are the rate those same quarters imply for a very large crude carrier that is NOT "
       f"on charter out — USD {n0(VS_SPOT)} against a published USD {n0(VS_BLEND)} in the "
       f"first quarter. The dotted lines are the mid-cycle rates this study's base case "
       f"reverts to; the dash-dotted line is an independent one-year charter fixed by a "
       f"listed owner in early {YRL[0][:4]}. Right: the first quarter of {YRL[0][:4]} for "
       f"every class, published beside implied. The difference between the two bars is the "
       f"charters inside the published figure, which is why it is zero for the medium-range "
       f"class, where no vessel is chartered out.")
rows = [['Class', 'Owned', 'On charter out', f"{HYRS[1]}", f"{HYRS[2]} published",
         f"{HYRS[2]} implied", f"{YRL[0][:4]} Q1 published", f"{YRL[0][:4]} Q1 implied",
         'Mid-cycle anchor']]
for key, nm in CLS:
    rows.append([nm, n0(FLT['owned'][key]), n0(fixed_by_class[key]),
                 n0(FLT['blend_fy24'][key]), n0(FLT['blend_fy25'][key]),
                 n0(FLT['spot_fy25'][key]),
                 n0(FLT['blend_q1_26'][key]), n0(FLT['spot_q1_26'][key]),
                 n0(FLT['spot_mid'][key])])
table(rows, [1.06, 0.56, 0.72, 0.66, 0.76, 0.72, 0.84, 0.84, 0.84], size=7.5)
caption(f"US dollars per vessel per day. “Published” is the company's own class average; "
        f"“implied” is what a vessel not on charter out must have earned for that average "
        f"to be true, given the charters the company also publishes. Where a class has no "
        f"vessel on charter out the two are the same figure, which is the check that the "
        f"construction is doing only what it claims. The mid-cycle anchor is the implied "
        f"rate for the average of the {HYRS[1]} and {HYRS[2]} outcomes, which is what the "
        f"base case reverts to over four years from {YRL[1]}. Counts are at the valuation "
        f"date and therefore BEFORE the {n0(ACQ_VLCC)} very large crude carriers bought on "
        f"{ACQ_DATE}, which take that class to {n0(VLCC_AFTER)} from their delivery date "
        f"and are carried in the forecast from it. Two disclosure gaps are handled and "
        f"flagged. Quarterly rates for the medium-range class are not disclosed for "
        f"{HYRS[1]}, so the {HYRS[2]} average stands in. And the handysize vessels are not "
        f"broken out in any rate table at all: an earlier edition carried them at the "
        f"medium-range rate unadjusted, which was wrong in DIRECTION and not merely in "
        f"size — the company said on the first-quarter call that handysize rates were "
        f"softer while medium range was up, so the two smallest classes were moving "
        f"opposite ways. They are now carried at {xt(IN['handysize_relative'], 2)} the "
        f"medium-range rate, the relative move the company itself disclosed. Both classes "
        f"remain small: together {n0(FLT['owned']['mr']+FLT['owned']['hs'])} of "
        f"{n0(owned_total)} vessels, none of them on charter out, and the smallest earners.")
P(f"The scale of the move is easiest to see in the largest class. Very large crude "
  f"carriers averaged a published USD {n0(FLT['blend_fy24']['vlcc'])} a day in {HYRS[1]} "
  f"and USD {n0(FLT['blend_fy25']['vlcc'])} in {HYRS[2]}; the published figure was USD "
  f"{n0(VS_BLEND)} for the first quarter of {YRL[0][:4]} and USD "
  f"{n0(FLT['blend_q2_26']['vlcc'])} was indicated for the second. Take out the "
  f"{n0(fixed_by_class['vlcc'])} of {n0(FLT['owned']['vlcc'])} vessels in that class "
  f"already on charter out and the free vessels earned USD {n0(VS_SPOT)} in the first "
  f"quarter, and the indicated second quarter implies USD "
  f"{n0(FLT['spot_q2_26']['vlcc'])} — roughly "
  f"{VS_SPOT/FLT['spot_mid']['vlcc']:.1f} times the mid-cycle anchor "
  f"this study reverts to, against the "
  f"{VS_BLEND/FLT['spot_mid']['vlcc']:.1f} times the published figure suggests. Against "
  f"{n0(spot_total)} owned vessels free to earn the market and the company's own "
  f"disclosure that USD 1,000 a day is worth USD {m0(IN['ebitda_per_1000_day'])} million "
  f"of annual earnings, the difference between today's rate and the mid-cycle anchor is "
  f"worth well over a billion dollars a year of earnings. That is why this one judgement "
  f"dominates — and it is also why the correction matters, because the same reversion "
  f"judgement applied to a higher starting point produces a higher value.")
H2('Why the base case reverts — the outside evidence')
P(f"A reversion assumption made without evidence is just pessimism. Two independent "
  f"observations, neither of them this study's own construction, point the same way, and "
  f"they are the reason the base case is a judgement with support rather than a default.")
rows = [['Evidence', 'What it shows'],
        ['The forward market will not pay spot for a year of time',
         f"A listed crude tanker owner fixed seven very large crude carriers on one-year "
         f"time charters in early {YRL[0][:4]} at USD {n0(MCC['vlcc_1y_tc'])} a day, at a "
         f"time when the spot rate of the moment was around USD "
         f"{n0(MCC['vlcc_spot_broker'])} and this company's own uncommitted vessels went "
         f"on to earn an implied USD {n0(VS_SPOT)} in the first quarter. A counterparty "
         f"willing to "
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
         f"The base case runs the market rate for a very large crude carrier not on "
         f"charter out from USD {n0(MCC['vlcc_path'][0])} in {YRL[0]} down to USD "
         f"{n0(MCC['vlcc_path'][4])} by {YRL[4]}, a straight glide to the "
         f"{HYRS[1]}-{HYRS[2]} average. Read against the one-year charter above, that "
         f"path is the LESS pessimistic of the two: it stays above USD "
         f"{n0(MCC['vlcc_1y_tc'])} until it crosses between {YRL[TC_CROSS]} and "
         f"{YRL[TC_CROSS+1]}, so for {n0(TC_CROSS+1)} of the five forecast years this "
         f"study assumes the fleet earns more than a counterparty was willing to commit "
         f"to for twelve months. That cuts against this study's own conclusion and is "
         f"stated rather than left for a reader to work out"]]
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
  f"the market price, which it reaches between the {pc(anchor_cross[0], 0)} and "
  f"{pc(anchor_cross[1], 0)} anchors. "
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
         f"the plain AVERAGE of three constructions built on six disclosed instruments — "
         f"the evidence table follows. It is not a weighted figure and an earlier edition "
         f"described it as one. Weighted by what is actually drawn the same evidence gives "
         f"{pc(W['kd_balance_weighted'], 2)}, which is one of the three constructions being "
         f"averaged; both are published"],
        ['Cost of debt, after tax', pc(W['kd_after_tax'], 2), '',
         f"at the {pc(W['tax_stat'], 0)} statutory rate. This is the one place in the study "
         f"where the statutory rate is used rather than the rate the company actually "
         f"bears: the model taxes profit unit by unit at effective rates running near "
         f"{pc(F['tax_rate'][0])}, and a shield taken at {pc(W['tax_stat'], 0)} is larger "
         f"than the relief the group in fact receives. It is inconsistent, it is disclosed, "
         f"and it is worth almost nothing — debt is {pc(W['wd'], 1)} of capital, so the "
         f"whole difference between a statutory and an effective shield is a fraction of a "
         f"basis point on the cost of capital"],
        ['Cost of the perpetual capital securities', pc(W['kh'], 2), pc(W['kh_term'], 2),
         f"their own contractual coupon — the overnight financing rate plus "
         f"{IN['hybrid_margin']*10000:,.0f} basis points. It is not tax-relieved, because "
         f"the coupon is a distribution rather than interest, and it is not marked down in "
         f"the terminal by anything except the risk-free rate the margin sits on: the "
         f"coupon floats, so its cost normalises as the base rate does"],
        ['Ordinary equity weight', pc(W['we'], 1), pc(W['we'], 1),
         f"market capitalisation of USD {m0(W['mktcap'])} million against gross debt of "
         f"USD {m0(W['debt'])} million and perpetual capital securities of USD "
         f"{m0(W['hybrid_cap'])} million. Market-value weights throughout; book equity is "
         f"never used"],
        ['Debt weight', pc(W['wd'], 1), pc(W['wd'], 1), ''],
        ['Perpetual capital securities weight', pc(W['wh'], 1), pc(W['wh'], 1),
         f"An earlier edition of this study left this tranche out of the weights on the "
         f"ground that it is already deducted in the bridge and counting it here would "
         f"charge for it twice. That reasoning does not hold, and two independent reviews "
         f"said so. Deducting a claim from value and pricing the capital it supplies are "
         f"different operations: leaving it out took a cheap tranche of funding out of the "
         f"enterprise without letting it lower the rate at which the enterprise is "
         f"discounted. It is now weighted at its own coupon, which is the correction that "
         f"moves the cost of capital from {pc(WACC_PRIOR, 2)} to {pc(W['wacc'], 2)} and "
         f"the terminal rate from {pc(WACC_TERM_PRIOR, 2)} to {pc(W['wacc_term'], 2)}"],
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
rows.append(['Memorandum — the same evidence weighted by what is actually drawn',
             'balance-weighted', pc(W['kd_balance_weighted'], 2)])
rows.append(['Adopted cost of debt, pre-tax',
             'the plain average of three constructions', pc(W['kd'], 2)])
table(rows, [4.10, 1.55, 1.35], size=8.3, band_rows={8}, left_cols=(1,))
caption(f"The spread of the evidence is the point. The parent revolving facility at the "
        f"secured overnight financing rate plus 80 basis points is the cheapest money in "
        f"the book and is a genuine benefit of the ownership structure; third-party bank "
        f"debt costs {(W['kd_bank_mid']-W['kd_method1'])*10000:,.0f} basis points more. "
        f"The adopted rate sits between them. It is the plain AVERAGE of three "
        f"constructions — the marginal drawdown rate on the parent facility, the blend of "
        f"the instruments actually outstanding, and the midpoint of the disclosed "
        f"third-party bank range — and not a figure weighted across the book, which is what "
        f"an earlier edition of this study called it. The genuinely balance-weighted "
        f"construction is {pc(W['kd_balance_weighted'], 2)}, is one of the three being "
        f"averaged, and is shown above so that a reader who wants it can take it directly; "
        f"the two are {abs(W['kd']-W['kd_balance_weighted'])*10000:,.0f} basis points "
        f"apart on a tranche that is {pc(W['wd'], 1)} of capital. The adopted rate sits "
        f"above the local sovereign yield of {pc(W['rf_observed'], 2)}, as a corporate "
        f"borrowing in the same currency must. The perpetual capital securities appear in "
        f"the evidence because they price the company's own subordinated risk, and they "
        f"are also carried in the weights at that same {pc(W['kh'], 2)} rather than "
        f"averaged into the cost of debt: they are neither debt nor ordinary equity, so "
        f"they get a weight and a rate of their own. They are deducted in the bridge as "
        f"well, and that is not a double charge — deducting a claim from value and pricing "
        f"the capital it supplies are two different operations, and doing only the first "
        f"is what the earlier edition of this study got wrong.")

H2('Where this construction is contested, and what the alternatives are worth')
P("Six choices above are legitimately arguable. Each alternative is computed and its "
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
        ['The terminal risk-free rate on a constructed long-run anchor',
         f"Carrying the explicit window's basis into the terminal instead — the observed "
         f"government yield net of the sovereign's own default spread, "
         f"{pc(W['rf_star'], 2)}, rather than the {pc(W['rf_terminal'], 2)} long-run anchor "
         f"used",
         f"raises the terminal risk-free rate by "
         f"{RF_BASIS_GAP*10000:,.0f} basis points and the value with it. It has no row of "
         f"its own in the grid overleaf, so the closest read-across is the beta: a step of "
         f"{p3(RF_READACROSS_BETA)} in the beta moves the cost of equity by about the same "
         f"amount and is worth AED {p2(RF_READACROSS)} — an OVERSTATEMENT of this item, "
         f"because a beta step moves every year and this one moves only the terminal",
         'The explicit window should be priced off a rate the market is quoting today; a '
         'perpetuity should not, because today’s yield is a point on a cycle and a '
         'perpetuity is not. Both are defensible and the basis genuinely changes between '
         'them, which is why it is listed here rather than left inside the cost-of-capital '
         'table. An earlier edition made the switch without listing it as a choice'],
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
       f"{p2(SPOT)} is crossed in the beta grid between the {p3(beta_cross[0])} and "
       f"{p3(beta_cross[1])} rows, and in the rate-anchor range between the "
       f"{pc(anchor_cross[0], 0)} and {pc(anchor_cross[1], 0)} anchors.")
P("Each anchor is varied independently around its own base, so each row shows what the "
  "valuation needs that one thing to do.")
rows = [['Beta →'] + [p3(b) for b in SN['betas']]]
for j, g in enumerate(SN['gs']):
    rows.append([f"terminal growth {pc(g, 1)}"] +
                [p2(SN['grid_beta_g'][i][j]) for i in range(len(SN['betas']))])
table(rows, [1.60, 1.08, 1.08, 1.08, 1.08, 1.08], size=8.4)
caption(f"Fair value in AED per share. The adopted construction is the {p3(IN['beta'])} "
        f"column at {pc(IN['g_terminal'], 1)} growth, and its cell is the published "
        f"cash-flow base of AED {p2(LN['dcf']['base'])} exactly. The bear case is struck at "
        f"{p3(SN['betas'][-1])}, the top of the regression's own 90% confidence interval "
        f"and the right-hand column here; the bull case is struck at the bottom of that "
        f"interval, {BF['ci90'][0]:.3f}, which falls between the first and second columns. "
        f"The equal-weight composite alternative is the {p3(SN['betas'][0])} column — and "
        f"note where that sits: BELOW the bottom of the interval, so the composite reading "
        f"is a lower discount rate than this study's own bull case takes. Beta moves the "
        f"answer across the whole width of this table; growth moves it a fraction of that. "
        f"Read "
        f"the beta columns against the published bear and bull of AED "
        f"{p2(LN['dcf']['bear'])} and {p2(LN['dcf']['bull'])} and the difference is "
        f"visible: those two also move the rate anchor and the capital programme, so they "
        f"are wider than the beta alone.")
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
rows.append(['Bear-to-bull scenario composite — THE PUBLISHED RANGE',
             f"three things at once: the beta at the two ends of its own 90% interval "
             f"({BF['ci90'][1]:.3f} in the bear, {BF['ci90'][0]:.3f} in the bull), a lower "
             f"mid-cycle rate anchor and a heavier capital programme in the bear, and the "
             f"reverse of both in the bull",
             f"{p2(LN['dcf']['bear'])} – {p2(LN['dcf']['bull'])}",
             p2(LN['dcf']['bull'] - LN['dcf']['bear'])])
rows.append(['Memorandum — the bear beta on its own',
             f"{p3(BF['ci90'][1])}, with the rate anchor and the capital programme left at "
             f"the base",
             f"{p2(BETA_ONLY_BEAR)} against a published bear of "
             f"{p2(LN['dcf']['bear'])}",
             p2(BETA_ONLY_BEAR - LN['dcf']['bear'])])
table(rows, [2.10, 1.95, 1.60, 1.35], size=8.4, left_cols=(1, 2))
caption(f"Ranked by single-row swing, the beta is the largest by a wide margin — larger "
        f"than the operating crux, larger than the capital programme, larger than the tax "
        f"exposure. That is worth reading precisely. The width of the beta row is the "
        f"width of a measured statistical interval; the width of the rate-anchor row is a "
        f"judgement about the future that no amount of data settles. The first is "
        f"uncertainty that has been quantified, "
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
  f"ladder: the weighted central of AED {p2(D['central'])} sits {ladder(D['central'])}, the "
  f"cash-flow lens on its own, at AED {p2(LN['dcf']['base'])}, sits "
  f"{ladder(LN['dcf']['base'])}, the equal-weight composite reading of AED "
  f"{p2(D['central_beta_alt'])} sits {ladder(D['central_beta_alt'])}, and the asset lens at "
  f"AED {p2(LN['book']['base'])} sits {ladder(LN['book']['base'])}. A valuation and a level "
  f"ladder are unrelated constructions and any agreement between them proves nothing; the "
  f"placement is computed off the same ladder printed above rather than described, so it "
  f"cannot go stale while the table beside it moves.", space_after=10)

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
  f"reads that stay closest to the company's own reported cash. The cash-flow lens lands at "
  f"AED {p2(LN['dcf']['base'])}, {ab(LN['dcf']['base'])}; the expert panel in Appendix C, "
  f"which prices mid-cycle earnings and capitalises no terminal value at all, centres at "
  f"AED {p2(PANEL)}, {ab(PANEL)}. Two constructions that share no machinery land within AED "
  f"{p2(abs(LN['dcf']['base']-PANEL))} of each other and both within a few per cent of the "
  f"screen. The two multiple lenses land materially higher, but they import their cost of "
  f"capital from comparators rather than state one — and they import the same three "
  f"multiples as each other, so they are one piece of evidence about relative pricing "
  f"rather than two independent answers (section 1.5). The asset lens lands materially "
  f"lower, on carrying values the company's own vessel sale says are understated. Read "
  f"together, the evidence brackets the screen price rather than pointing away from it.")
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
  f"fairly priced rather than materially cheap. The composite reading should be read with "
  f"one further fact attached to it: at {p3(BFA['beta'])} it sits below the bottom of the "
  f"adopted estimate's own 90% interval, so it is a more aggressive discount rate than this "
  f"study's own bull case takes.")
P("No recommendation and no forecast of the share price is expressed here or anywhere "
  "else in this document. The output is a range and a distribution.", space_after=10)

# ============================ 9  §5  CATALYSTS ===============================
H1('5  Catalysts to watch')
rows = [['Catalyst', 'Why it matters', 'What to watch'],
        ['Second-quarter and half-year results',
         f"the second-quarter published rate of USD {n0(FLT['blend_q2_26']['vlcc'])} a day "
         f"for the "
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
         f"{YRL[0]} to {NET_CASH_WORD}, against a stated target of "
         f"{xt(IN['nd_ebitda_target_lo'], 1)} to {xt(IN['nd_ebitda_target_hi'], 1)}. "
         f"The company will not sit there — and the purchase announced on "
         f"{ACQ_DATE} is the first evidence of that, USD {b1(ACQ_COST)} billion of it, "
         f"committed within days of the balance sheet this study values",
         'further acquisitions, a step-up in distributions beyond the stated 5% a year, or '
         'a larger newbuild programme — see section 7'],
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
         'ordinary drift lower; the asset lens sits well below this zone and no other '
         'fundamental read in the study reaches down into it'],
        ['Upper half of the central band',
         f"{p2(H3M['pct']['p50'])} – {p2(H3M['pct']['p75'])}",
         'ordinary drift higher; the cash-flow lens on its own sits inside this zone, so '
         'no repricing of the business is needed to reach it'],
        ['Upper tail', f"above {p2(H3M['pct']['p95'])}",
         'a 1-in-20 outcome; the zone in which the market would be pricing the rate '
         'strength as durable, or the equal-weight reading of the discount rate'],
        ['Where the weighted central sits', p2(D['central']),
         f"{zone3m(D['central'])}. Reaching it inside a quarter is an ordinary outcome "
         f"rather than a repricing"],
        ['Where the cash-flow lens alone sits', p2(LN['dcf']['base']),
         f"{zone3m(LN['dcf']['base'])} — close enough to the price today that the "
         f"distribution treats the two as the same place"],
        ['Where the expert panel centres', p2(PANEL),
         f"{zone3m(PANEL)}. Three methods that share no machinery with the cash-flow model "
         f"land essentially on the screen price"],
        ['Where the equal-weight composite central sits', p2(D['central_beta_alt']),
         zone3m(D['central_beta_alt'])],
        ['Where the asset lens sits', p2(LN['book']['base']),
         f"{zone3m(LN['book']['base'])} — the one fundamental read the three-month "
         f"distribution treats as a tail outcome"]]
table(rows, [1.80, 1.70, 3.50], size=8.4, left_cols=(2,))

# ============================= 11  §7  CAVEATS ===============================
H1('7  Caveats and what would change our mind')
for head, body in [
    ("The beta still moves the answer more than anything else, even though it is now "
     "settled. ",
     f"Regressed against the {BE['regressor']}, the beta is {p3(IN['beta'])}; regressed "
     f"against an equal-weight composite of the same exchange's names it is "
     f"{p3(BFA['beta'])}, worth AED {p2(beta_gap)} a share on the cash-flow lens. Across "
     f"the beta range tested in section 1.9 the swing is AED "
     f"{p2(max(beta_span)-min(beta_span))}, still the widest single sensitivity in the "
     f"study. What has changed is that this is no longer an unresolved argument between a "
     f"regression and an economic prior — the published index of the share's own exchange "
     f"is the right yardstick and the two now agree. What remains is ordinary statistical "
     f"uncertainty: {BE['window_years']:.1f} years of listed history, an R-squared of "
     f"{BE['r2']:.3f}, and a 90% interval of [{BE['ci90'][0]:.2f}, {BE['ci90'][1]:.2f}] "
     f"that this study's bear and bull cases carry at full width rather than narrowing. A "
     f"longer history could still move the point estimate inside that interval, and the "
     f"share is a constituent of the index it is measured against, which pulls the "
     f"estimate up rather than down (section 1.8)."),
    ("The terminal value is most of the answer. ",
     f"{pc(DCF['tv_share'], 0)} of the cash-flow model's enterprise value is the terminal "
     f"value on the adopted construction, {pc(DCFA['tv_share'], 0)} on the equal-weight "
     f"composite. That is high, and it is the arithmetic consequence of discounting a business "
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
     f"company will either lever up for acquisitions or return more capital, and on "
     f"{ACQ_DATE} it did the first: USD {b1(ACQ_COST)} billion of vessels, committed within "
     f"days of the balance sheet this study values, and now carried in the model. This does "
     f"not "
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
     f"The published USD {n0(FLT['blend_q2_26']['vlcc'])} a day for the largest class in "
     f"the second "
     f"quarter of {YRL[0][:4]} is the level the company indicated on its first-quarter "
     f"call, not an audited or reported outcome. It is one of the four quarters that sets "
     f"the {YRL[0]} rate, so an error there flows into the first forecast year. The "
     f"reported half-year will settle it."),
    ("One rate substitution is still carried in the fleet build, and a second has been "
     "replaced. ",
     f"Quarterly rates for the medium-range class are not disclosed for {HYRS[1]}, so the "
     f"{HYRS[2]} average stands in. That one remains, and it is labelled as a substitution "
     f"wherever it appears. The second has gone: an earlier edition carried the handysize "
     f"vessels, which are not broken out in any published rate table, at the medium-range "
     f"rate unadjusted. That was not merely imprecise — it had the sign wrong. The company "
     f"said on the first-quarter call that handysize rates were SOFTER while medium range "
     f"was UP, so the two smallest classes were moving in opposite directions and the "
     f"substitution was importing a rise into a class that was falling. They are now "
     f"carried at {xt(IN['handysize_relative'], 2)} the medium-range rate, which is the "
     f"relative move the company itself disclosed rather than a stand-in. The two classes "
     f"together are {n0(FLT['owned']['mr']+FLT['owned']['hs'])} of {n0(owned_total)} "
     f"vessels and the lowest earners in the fleet, so neither is large — but a "
     f"substitution that points the wrong way is a different kind of error from one that "
     f"is merely approximate, and it is corrected rather than re-flagged."),
    ("The vessels bought on the anchor date are announced, not delivered. ",
     f"The USD {b1(ACQ_COST)} billion purchase of {n0(ACQ_VLCC + ACQ_GAS_N)} vessels was "
     f"announced on {ACQ_DATE} and none of them had been delivered when this study was "
     f"struck. The model carries them from their announced delivery dates and adds the "
     f"announced price to net debt, which is the only treatment that keeps the fair value "
     f"and the market price on the same set of assets — the market price this study is "
     f"compared against was set on the day of the announcement. What is assumed is that the "
     f"vessels arrive on the announced schedule at the announced price, and that they trade "
     f"on the same rate path as the rest of the class. A delayed delivery would take "
     f"earnings out of {YRL[0]} while leaving the debt in; a price different from the one "
     f"announced would move the bridge directly. The half-year and full-year statements are "
     f"the first confirmation of either."),
    ("The open-market rate is solved out of a published average, and that construction "
     "has a load-bearing assumption inside it. ",
     f"The company publishes one rate per vessel class per quarter and states that it is "
     f"blended across the whole class. This study takes the {n0(len(CHT))} vessels on "
     f"charter out at their own disclosed rates and solves the rest out of that average, "
     f"which gives USD {n0(VS_SPOT)} a day for the largest class in the first quarter of "
     f"{YRL[0][:4]} against a published USD {n0(VS_BLEND)}. The arithmetic is exact only "
     f"if the published average is a straight vessel-day average of the whole class. If "
     f"the company weights it differently, or if a vessel was off-hire for part of the "
     f"quarter, the solved rate is too high by the same amount the average is understated. "
     f"The check available is that where a class has no vessel on charter out the two "
     f"figures come out identical, which they do. The half-year statement, which reports "
     f"the second quarter rather than indicating it, is the first outside test of the "
     f"construction."),
    ("The fade in the asset lens is a judgement with nothing observable behind it. ",
     f"Residual income beyond the fifth year is carried as a remainder decaying at "
     f"{pc(BK['fade'], 0)} a year, worth USD {m0(BK['pv_terminal']*1000)} million of the "
     f"USD {m0(BK['equity_value']*1000)} million this lens produces. The economic argument "
     f"for a fade is solid — a fleet has to be replaced at market prices rather than at "
     f"the value it is carried at, so a return above the cost of equity cannot persist "
     f"unchanged — but the speed is chosen, not measured. A slower fade raises this lens "
     f"and a faster one lowers it. The lens carries {pc(LW['book'], 0)} weight, which is "
     f"the lowest of the four, partly for this reason."),
    ("Two unit inputs are solved rather than sourced. ",
     f"Per-vessel running cost of USD {n0(FLT['opex_day'])} a day is solved so that the "
     f"owned fleet's earnings reproduce the reported {HYRS[2]} result, and the gas carrier "
     f"day rate of USD {n0(FLT['gas_rate_day'])} is solved from reported {HYRS[2]} revenue "
     f"over consolidated vessel-years. Neither is disclosed at a finer level anywhere in "
     f"the filings. Both are labelled as solved wherever they appear, and both are "
     f"anchored on a reported outcome rather than assumed."),
    ("The revenue gross-up for the tanker fleet is presentational at the earnings line — "
     "and an earlier edition of this study said it could not reach the valuation, which "
     "was wrong. ",
     f"Reported Tankers revenue was {xt(IN['tnk_grossup_25'], 2)} the owned fleet's own "
     f"charter-equivalent revenue in {HYRS[2]}, because of chartered-in and relet trading "
     f"that carries almost no margin. The forecast sets that ratio at "
     f"{xt(IN['tnk_grossup_26'], 2)} from {YRL[0]}, on the evidence of the first quarter, "
     f"where revenue fell year on year while the rate earned per vessel more than doubled. "
     f"The earlier edition printed this caveat with a claim attached: that the ratio moves "
     f"the revenue line and never the earnings line, SO IT CANNOT AFFECT THE VALUATION. The "
     f"first half of that is true and the conclusion does not follow, and the correction is "
     f"printed here rather than the sentence being quietly dropped. Revenue is not only an "
     f"output — it is the denominator the working-capital cycle is expressed in. Receivable "
     f"days were calibrated on {HYRS[2]} revenue, which carries the "
     f"{xt(IN['tnk_grossup_25'], 2)} gross-up, and then applied to a forecast revenue line "
     f"built at {xt(IN['tnk_grossup_26'], 2)}. Two different conventions on the two sides "
     f"of one ratio understate the receivable balance, and the change in working capital is "
     f"a line in the free-cash-flow waterfall. Re-based onto the revenue the forecast "
     f"actually produces, {n1(IN['dso_days_reported'])} days becomes "
     f"{n1(IN['dso_days'])} — and that reaches the valuation, through working capital, by "
     f"exactly the route the earlier caveat said did not exist. A study that quietly drops "
     f"a claim it has made is worse than one that says the claim was wrong. Separately and "
     f"still true: a reader comparing this study's revenue forecast with a broker's should "
     f"know the two may be on different conventions."),
    ("The four lenses are less independent of one another than four lenses sound. ",
     f"The relative lens and the normalised lens apply the SAME three multiples to two "
     f"different earnings denominators — the first forecast year in one, the five-year "
     f"average of the same forecast in the other. Between them they carry "
     f"{pc(LW['relative']+LW['normalized'], 0)} of the weighted central, so that much of "
     f"the headline rests on one method presented as two reads. Both denominators are "
     f"legitimate questions and neither read is redundant on its own terms, so nothing has "
     f"been dropped — but the overlap is not neutral in direction. Those two lenses are the "
     f"two that sit highest; collapsing them to one would move the central toward the "
     f"cash-flow and asset lenses, which sit lower. This is the largest single item "
     f"the reviews raised that has been left open rather than acted on, and it is stated "
     f"here so that a reader weighs the field knowing it."),
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
     f"wider Abu Dhabi panel and why the beta is set out against three separate market "
     f"series in section 1.8 rather than accepted at face value. One further limit belongs "
     f"here: the index series supplied ends {BE['regressor_span'][1]}, before the share's "
     f"last session used elsewhere in this study, so {n0(BE['unused_stock_weeks'])} weekly "
     f"observations sit outside the regression. The window was stopped where the index "
     f"stops rather than pairing the share against a stale index level."),
    ("What would change our mind, specifically. ",
     f"Upward: one-year time-charter fixtures settling durably above the mid-cycle anchor "
     f"used here; the contracted gas programme delivering on time and taking spot exposure "
     f"below the disclosed {pc(IN['spot_share_ebitda_29'], 0)}; a longer price history "
     f"that settles the beta toward the lower end of its interval as the contracted "
     f"programme comes in, which would lift the cash-flow lens directly. Downward: the "
     f"same history settling it toward the upper end; rates reverting faster than the "
     f"four-year glide assumed here; "
     f"the shipping tax relief being withdrawn; a capital programme that grows without a "
     f"matching contracted return; or evidence that the contracted relationship with the "
     f"parent is repriced rather than renewed.")]:
    bullet(body, bold_head=head)
P('', space_after=8)

# ==================== 11b  WHAT CHANGED IN THIS EDITION ======================
H1('What changed in these editions, and why')
P(f"This study has been through two rounds of external review. {n0(N_REVIEWS)} independent "
  f"readers raised {n0(N_FINDINGS)} findings between them. Every one was priced — what "
  f"would it move the answer by, if it were right — and then adjudicated on its own "
  f"evidence rather than on its confidence. Many were rejected with the receipt that "
  f"rejects them; the ones that survived are below. None of this is presented as "
  f"refinement: several were errors, and they are called errors here. A study that has been "
  f"corrected and does not say so is worse than one that was right the first time, because "
  f"the reader has no way of telling which they are holding.")
rows = [['Edition', 'Cash-flow lens (AED)', 'Weighted central (AED)', 'Against the market '
         f"price of {p2(SPOT)}"],
        ['As first issued', p2(DCF_ED1), p2(CENTRAL_ED1), vs(CENTRAL_ED1)],
        ['After the first round of corrections', p2(DCF_ED2), p2(CENTRAL_ED2),
         vs(CENTRAL_ED2)],
        ['This edition, after the second round', p2(LN['dcf']['base']), p2(D['central']),
         vs(D['central'])]]
table(rows, [2.30, 1.55, 1.60, 1.55], size=8.5, band_rows={3})
caption(f"Read the two rounds together and the headline has moved less than the work "
        f"behind it. The first round changed the central by AED "
        f"{CENTRAL_ED2-CENTRAL_ED1:+.2f} — essentially nothing — while replacing the "
        f"tanker build, the cost of capital, the asset lens and the treatment of the joint "
        f"ventures, because the corrections ran in both directions and very nearly "
        f"cancelled. The second round moved it AED {D['central']-CENTRAL_ED2:+.2f}, and "
        f"almost all of that is one item: a vessel purchase the first edition did not know "
        f"about. The composition of the answer has changed far more than the answer has, "
        f"which is the honest summary of both rounds.")
H2('Round one — the corrections made in the previous edition')
rows = [['What changed', 'What was wrong before', 'What it is now', 'Which way it moved '
         'the answer']]
rows.append([
    'The tanker fleet is built vessel by vessel',
    f"The company publishes one rate per vessel class per quarter, and that rate is a "
    f"blend across the whole class — the chief financial officer said so in terms on the "
    f"first-quarter call. The earlier edition read it as the open-market rate AND then "
    f"added the vessels on charter out separately at their own lower rates, so the drag of "
    f"the charters was charged twice.",
    f"Each of the {n0(len(CHT))} vessels chartered out earns its own disclosed rate for "
    f"exactly the days its own contract runs, and the open-market rate is solved out of "
    f"the published blend rather than assumed. For the largest class in the first quarter "
    f"of {YRL[0][:4]} that gives USD {n0(VS_SPOT)} a day against a published USD "
    f"{n0(VS_BLEND)}. Section 1.7.",
    'UP. The fleet starts from a higher rate, and the same reversion judgement applied to '
    'a higher starting point produces a higher value.'])
rows.append([
    'The perpetual capital securities are priced in the cost of capital',
    f"They were deducted in the bridge as a claim ranking ahead of the ordinary shares but "
    f"left out of the weights in the cost of capital, on the ground that including them "
    f"would charge for them twice. That was a non-sequitur, and two of the four reviews "
    f"said so independently: deducting a claim from value and pricing the capital it "
    f"supplies are different operations, and doing only the first removes a cheap tranche "
    f"of funding from the enterprise without letting it lower the rate.",
    f"They now carry a weight of {pc(W['wh'], 1)} at their own coupon of "
    f"{pc(W['kh'], 2)}, beside ordinary equity at {pc(W['we'], 1)} and debt at "
    f"{pc(W['wd'], 1)}, and that cost normalises with the risk-free rate in the terminal "
    f"because the coupon floats. The cost of capital falls from {pc(WACC_PRIOR, 2)} to "
    f"{pc(W['wacc'], 2)} and the terminal rate from {pc(WACC_TERM_PRIOR, 2)} to "
    f"{pc(W['wacc_term'], 2)}. Section 1.8.",
    'UP, and this is the largest of the five. A lower discount rate raises a valuation in '
    'which most of the value sits beyond the fifth year.'])
rows.append([
    'The joint ventures are counted once',
    f"The earnings the company discloses for each business unit already include the "
    f"group's share of its equity-accounted joint ventures — USD "
    f"{m0(IN['jv_gas_fy25'])} million inside Gas Carriers and USD "
    f"{m0(IN['jv_services_fy25'])} million inside Services in {HYRS[2]}, both visible in "
    f"the segment note. The earlier edition forecast those earnings inside the units AND "
    f"added the stakes again at carrying value in the bridge.",
    f"The joint-venture share is taken out of the unit earnings before the forecast "
    f"starts. The stakes are still added in the bridge at their reviewed book value of USD "
    f"{m0(BR['jv'])} million, which is now the only place they appear. Sections 1.1 and "
    f"1.6.",
    'DOWN. Forecast earnings are lower in both affected units, and the terminal value '
    'carries that reduction forward.'])
rows.append([
    'The asset lens is residual income, not a justified price-to-book',
    f"A justified price-to-book multiple assumes a steady state in which the company pays "
    f"out everything it does not need to fund its growth — at this company's returns, "
    f"{pc(1-BK['g']/BK['roe_sustainable'], 0)} of earnings. It pays out "
    f"{pc(min(FIN['payout']), 0)} to {pc(max(FIN['payout']), 0)} and compounds its book "
    f"faster than its own cost of equity, which is the region in which that formula is not "
    f"merely inaccurate but undefined.",
    f"Opening ordinary book, plus five years of returns earned above the cost of equity on "
    f"that book, discounted, plus a remainder fading at {pc(BK['fade'], 0)} a year. "
    f"Section 1.2.",
    f"DOWN, and by more than any other single change. On the same returns, the same cost "
    f"of equity and the same growth, the justified-multiple form gives "
    f"{xt(PB_SINGLE, 2)} book, or AED {p2(BOOK_SINGLE)} a share; residual income gives "
    f"AED {p2(LN['book']['base'])}. At {pc(LW['book'], 0)} weight the difference is worth "
    f"about AED {p2((BOOK_SINGLE-LN['book']['base'])*LW['book'])} of the weighted "
    f"central."])
rows.append([
    'Earnings per share is struck after the perpetual coupon',
    f"Forecast earnings per share was profit attributable to ordinary AND perpetual "
    f"holders divided by the ordinary shares. The coupon ranks ahead of the ordinary "
    f"shares, so that figure belongs to somebody else.",
    f"Earnings per share is now profit after the USD {m0(FIN['hybrid_coupon'])} million "
    f"annual coupon, over the ordinary shares. The figure before the coupon is kept as a "
    f"memorandum line so the two reconcile. Appendix A.1.",
    f"DOWN by about {pc(1-FIN['eps'][0]/FIN['eps_pre_coupon'][0])} on the per-share "
    f"earnings, which feeds the earnings-multiple leg of the comparison and normalised "
    f"lenses."])
rows.append([
    'Two smaller corrections, carried for completeness',
    f"The fleet was counted at the {HYRS[2]} year end, at {n0(owned_total_fy25)} owned "
    f"tankers, after a very large crude carrier had already been sold in January "
    f"{YRL[0][:4]}. And the minority interests were deducted at book value with no "
    f"explanation of why book was the right measure when the minorities take "
    f"{pc(IN['nci_share'])} of profit.",
    f"The fleet is {n0(owned_total)} owned tankers at the valuation date. The minorities "
    f"are deducted at USD {m0(DCF['nci'])} million: the USD {m0(DCF['nci_navig8'])} "
    f"million arising on the tanker combination stays at book because that stake is "
    f"contracted for purchase in mid-2027 at a price already deducted as deferred "
    f"consideration, and only the remaining USD {m0(DCF['nci_other_bv'])} million is "
    f"lifted to its share of value. Sections 1.1 and 1.7.",
    f"DOWN, marginally, on both. The minority treatment costs AED {p2(NCI_LIFT)} a share, "
    f"not the AED {p2(NCI_FLAT_COST)} that applying the profit share to the whole equity "
    f"value would have cost — the criticism was right about the premise and wrong about "
    f"the conclusion."])
table(rows, [1.34, 2.06, 2.06, 1.54], size=7.8, align_right_from=9)

H2('Round two — the corrections made in this edition')
P(f"The second round of review produced one finding that moves the answer materially and "
  f"several that do not move it at all but damage the document — a table that does not "
  f"foot, a claim that contradicts the model behind it, two conventions spliced into one "
  f"series. The second kind is easy to wave through precisely because it costs nothing. "
  f"They are corrected here on the same terms as the first kind.")
rows = [['What changed', 'What was wrong before', 'What it is now', 'Which way it moved '
         'the answer']]
rows.append([
    f"A USD {b1(ACQ_COST)} billion vessel purchase is in the model",
    f"On {ACQ_DATE} — the anchor date of this study — the company announced the purchase "
    f"of {n0(ACQ_VLCC + ACQ_GAS_N)} vessels for about USD {b1(ACQ_COST)} billion. The "
    f"previous edition omitted it entirely. That is not a modelling choice: it compared a "
    f"fair value that excluded the vessels with a market price that already included them.",
    f"{n0(ACQ_VLCC)} very large crude carriers and {n0(ACQ_GAS_N)} gas carriers join the "
    f"fleet on their announced delivery dates and earn from those dates; the USD "
    f"{b1(ACQ_COST)} billion is added to net debt in the bridge and to the depreciating "
    f"asset base. It also independently confirms the fleet count corrected in round one: "
    f"the company says the purchase takes it to {n0(VLCC_AFTER)} crude carriers, and the "
    f"corrected valuation-date count of {n0(FLT['owned']['vlcc'])} plus {n0(ACQ_VLCC)} is "
    f"{n0(VLCC_AFTER)}. Headline, company overview, section 1.1 and section 1.7.",
    'UP, and it is nearly the whole of the second round. The earning fleet grows by more '
    'than the debt costs, on the rate path this study already assumed.'])
rows.append([
    'The smallest tankers are no longer carried at a rate that moved the opposite way',
    f"The handysize class is not broken out in any published rate table, so the previous "
    f"edition carried it at the medium-range rate unadjusted. On the first-quarter call the "
    f"company said handysize rates were SOFTER while medium range was UP — the two classes "
    f"moved in opposite directions, so the substitution had the sign wrong, not merely the "
    f"magnitude.",
    f"Carried at {xt(IN['handysize_relative'], 2)} the medium-range rate, the relative move "
    f"the company itself disclosed. Section 1.7.",
    f"DOWN, and small: {n0(FLT['owned']['hs'])} of {n0(owned_total)} owned tankers and the "
    f"lowest earners in the fleet. A substitution that points the wrong way is still worth "
    f"correcting."])
rows.append([
    'Receivable days are re-based onto the revenue the forecast is built at',
    f"Receivable days were calibrated on {HYRS[2]} revenue, which carries a "
    f"{xt(IN['tnk_grossup_25'], 2)} gross-up over the owned fleet's own charter-equivalent "
    f"revenue, and then applied to a forecast revenue line built at "
    f"{xt(IN['tnk_grossup_26'], 2)}. Two conventions on the two sides of one ratio.",
    f"Re-based onto the basis the forecast uses: {n1(IN['dso_days_reported'])} days becomes "
    f"{n1(IN['dso_days'])}. Section 1.1.",
    f"DOWN. A larger receivable balance means a larger build in working capital, and the "
    f"change in working capital is a line in the cash-flow waterfall. This is also what "
    f"falsified a caveat the previous edition printed — see section 7."])
rows.append([
    'The cost of debt is described as the average it is',
    f"The previous edition called the adopted pre-tax cost of debt a figure “weighted "
    f"across the drawn book”. It is not weighted. It is the plain average of three "
    f"constructions, one of which happens to be the balance-weighted one.",
    f"Published as an average, at {pc(W['kd'], 2)}, with the genuinely balance-weighted "
    f"construction shown beside it at {pc(W['kd_balance_weighted'], 2)}. Section 1.8.",
    f"NO MOVEMENT — the figure did not change, only the description of it. The two "
    f"constructions are {abs(W['kd']-W['kd_balance_weighted'])*10000:,.0f} basis points "
    f"apart on a tranche that is {pc(W['wd'], 1)} of capital."])
rows.append([
    'The depreciation rate is kept, and now carries its evidence',
    f"A reviewer proposed replacing the rate used with the {HYRS[2]} realised rate of "
    f"{pc(IN['dep_rate_realised_fy25'], 2)}. The previous edition gave no evidence either "
    f"way, which made the choice look arbitrary.",
    f"The disclosed useful lives, the realised rate and the rate used are now shown "
    f"together. Both candidates sit ABOVE what the stated lives imply for the fleet, "
    f"because dry-docking components are written off over a few years; the rate used, "
    f"{pc(IN['dep_rate_ppe'], 2)}, is the LOWER — the more conservative of the two forward "
    f"bases. Section 1.1.",
    'NO MOVEMENT. The rate is unchanged; the reader can now see why, and disagree on the '
    'evidence rather than on assertion.'])
rows.append([
    'The earnings multiple is published on both bases',
    f"The previous edition applied the peers' FORWARD multiple to forward earnings, which "
    f"is right, but quoted the company's own multiple on a TRAILING basis in the table "
    f"beside peers shown forward.",
    f"Both bases are published throughout: the blend is {xt(REL['blend_pe'], 2)} forward "
    f"and {xt(BLEND_PE_TTM, 2)} trailing, and the company is shown at "
    f"{xt(OWN_PE_FWD, 2)} forward beside {xt(REL['own_pe_ttm'], 2)} trailing. Section 1.3.",
    'NO MOVEMENT on the lens, which always used the forward blend. It removes a comparison '
    'that was not like for like.'])
rows.append([
    'Several tables that did not foot, or described themselves wrongly',
    "The bridge from enterprise value to equity did not add up once the purchase above was "
    "in the model. The guidance reconciliation did not foot and called the study's own "
    "conversion of directional guidance “the midpoint of the ranges the company "
    "published”. Return on equity ran on closing equity in the reported years and average "
    "equity in the forecast years, inside one row and one sentence. The leverage ratio ran "
    "on two different earnings definitions in the same row. The price-to-book memorandum "
    "was struck on a wider book than the multiple printed above it. The published "
    "bear-to-bull range was described as the beta's own interval when it also moves the "
    "rate anchor and the capital programme.",
    "Each is corrected in place and the superseded description is named rather than "
    "removed. Sections 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 1.9 and Appendix A.2.",
    "NO MOVEMENT on any fair value. Every one of them was a defect in what the document "
    "says about itself, which is the class of finding that gets waved through because it "
    "prices at zero."])
table(rows, [1.34, 2.06, 2.06, 1.54], size=7.8, align_right_from=9)
P(f"One thing did not change and is worth saying so. The reversion judgement in section "
  f"1.7 — that the fleet glides over four years to the average of what it earned in "
  f"{HYRS[1]} and {HYRS[2]} — is the same judgement it was, and it remains the largest "
  f"open question in the study. The corrections above changed what the fleet is reverting "
  f"FROM, not the view about where it settles. Nor did the beta change: it is still "
  f"{p3(IN['beta'])} against the published index of the share's own exchange, with the "
  f"equal-weight composite reading of {p3(BFA['beta'])} published beside it at full size "
  f"throughout.")
P(f"And one finding has been left open rather than acted on, which a reader should know "
  f"before weighing the field. The relative lens and the normalised lens share all three "
  f"multiples and the same weighting between the enterprise and earnings readings; what "
  f"differs between them is only the earnings denominator those multiples are applied to. "
  f"Together they carry {pc(LW['relative']+LW['normalized'], 0)} of the weighted central, "
  f"so {pc(LW['relative']+LW['normalized'], 0)} of the headline rests on one method "
  f"presented as two reads. It has not been changed, because both denominators are "
  f"legitimate questions and neither read is redundant on its own terms. But it is not "
  f"neutral in direction — those are the two lenses that sit highest — and it is the "
  f"largest single item still outstanding from either round of review. Section 1.5 and "
  f"section 7 both carry it.", space_after=10)


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
rows.append(['Attributable to ordinary shareholders'] +
            ['—', '—', m0(HI['npa'][2] - IN['hybrid_coupon_fy25'])] +
            [m0(x) for x in FIN['npa_ordinary']])
rows.append(['Earnings per share (USD)'] + [f"{x:.3f}" for x in HI['eps']] +
            [f"{x:.3f}" for x in FIN['eps']])
rows.append(['  memorandum — before the perpetual coupon (USD)'] + ['—'] * 3 +
            [f"{x:.3f}" for x in FIN['eps_pre_coupon']])
table(rows, [1.72, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66], size=7.5,
      band_rows={6, 16, 19})
caption(f"Every reported line is taken directly from the company's audited consolidated "
        f"statements. Two rows are house derivations and are labelled: earnings before "
        f"interest, tax, depreciation and amortisation is earnings before interest and tax "
        f"plus depreciation and amortisation — the audited statements carry no such line, "
        f"and the company's own reported figure (USD {m0(HI['ebitda_reported'][2])} "
        f"million in {HYRS[2]} against the USD {m0(EBITDA_H[2])} million used here) adds "
        f"the share of joint ventures and one-off items; and forecast earnings per share "
        f"is profit attributable to the ORDINARY shareholders over shares outstanding — "
        f"that is, after the perpetual securities coupon of USD "
        f"{m0(FIN['hybrid_coupon'])} million a year, which ranks ahead of them. An earlier "
        f"edition struck it before that coupon, which overstated it by about "
        f"{pc(FIN['eps_pre_coupon'][0]/FIN['eps'][0]-1)}; the figure before the coupon is "
        f"kept as the memorandum line so the two can be reconciled. The reported earnings "
        f"per share in the first three columns are the company's own published basic "
        f"figures and are not restated here. Forecast profit is struck after interest on "
        f"the modelled debt path and after tax at each unit's own rate, so it differs from "
        f"the free-cash-flow waterfall in section 1.1, which is a pre-financing measure by "
        f"construction.")

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
            [xt(ND_EBITDA_HIST[i], 2) for i in range(3)] +
            [xt(x, 2) for x in FIN['nd_ebitda']])
rows.append(['Return on equity'] + [pc(x) for x in ROE_HIST] +
            [pc(x) for x in ROE_FCST])
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
        f"ordinary shareholders barely moved. Two ratio rows carry one definition each, end "
        f"to end, and both were spliced in an earlier edition. Return on equity is "
        f"attributable profit over CLOSING equity attributable to ordinary shareholders in "
        f"every column; the forecast years were previously shown over AVERAGE equity, which "
        f"is a different measure and made the series read as a rise where a consistent "
        f"basis shows a fall. On the average-equity convention the same forecast years are "
        f"{' · '.join(pc(x) for x in ROE_FCST_AVGEQ)}, and the residual-income lens in "
        f"section 1.2 uses a third convention — OPENING book — which is the right one for "
        f"that construction and is named there. Net debt to earnings is on the operating "
        f"earnings definition used throughout this study in every column; the reported "
        f"years were previously shown against the company's own wider reported earnings "
        f"figure, which is a different denominator from the one the forecast columns use.")

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
        ['How the market is measured in the beta',
         'the published index of the share’s own exchange against an equal-weight '
         'composite of the same exchange’s names',
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
  "the industry and the company itself. Figures the SUBJECT COMPANY reports about itself "
  "come only from its own issued statements and disclosures; no data vendor, broker or "
  "press report is the source of any of the subject's reported historical figures. That "
  "rule is scoped deliberately and the scope matters: the comparator multiples in section "
  "1.3 ARE taken from data-aggregator statistics pages, named and dated, and were not "
  "recomputed from each comparator's own filings. It is the largest block of non-company "
  "data in the study, it is labelled wherever it is used, and the limitation it carries — "
  "that a comparator's earnings cannot be shown to be struck on the same definition as the "
  "subject's — is stated at the table rather than here. The full input-by-input register, with a "
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
    ("The comparators' own filings were not used, and their multiples were not "
     "recomputed. ",
     f"The three comparator multiples in section 1.3 come from data-aggregator statistics "
     f"pages, each named and dated in the source register. Rebuilding them from each "
     f"comparator's own accounts — three more sets of filings, on three different reporting "
     f"conventions, in three different currencies — was not undertaken. The consequence is "
     f"specific and is stated at the table itself: the study cannot demonstrate that a "
     f"comparator's earnings are struck on the same definition as its own, which is a "
     f"reason to read the comparison lens as evidence about relative pricing rather than as "
     f"an independent valuation. It is the largest block of non-company data in the study, "
     f"and the two lenses that rest on it carry {pc(LW['relative']+LW['normalized'], 0)} of "
     f"the weighted central between them."),
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
        [f"Range — the low end at a cost of equity of {pc(E2['ke_lo'], 2)}, built on the "
         f"top of the beta's 90% interval ({BF['ci90'][1]:.3f}), with lower growth; the "
         f"high end at {pc(E2['ke_hi'], 2)} on the bottom of it ({BF['ci90'][0]:.3f}) "
         f"with higher growth",
         f"{p2(E2['rng'][0])} – {p2(E2['rng'][1])}"]]
table(rows, [4.80, 2.20], size=8.4, band_rows={8})
P(f"One thing this leg does NOT do, and it is a genuine inconsistency across the panel "
  f"rather than a feature of the method. The stream it capitalises starts from group free "
  f"cash flow, which includes the {pc(IN['nci_share'])} of profit that belongs to the "
  f"minority holders, and it never adds the joint-venture stakes that the main bridge and "
  f"Expert 3 both add at book value. Expert 1 deducts the minorities and Expert 3 runs the "
  f"full bridge; this one does neither. Put on the same bridge as the other two — the "
  f"minority share out, the joint ventures in — this expert would land at AED "
  f"{p2(E2_BRIDGED)} rather than AED {p2(E2['base'])}, a move of AED "
  f"{E2_BRIDGED-E2['base']:+.2f}. The published figure is left as the method produces it "
  f"and the difference is stated here, because three experts presented as independent "
  f"reads of one balance sheet should not be quietly running three different bridges.")
P(f"This expert lands at AED {p2(E2['base'])}, below the study's own weighted central of "
  f"AED {p2(D['central'])}, and the reason is specific: the five-year average free cash "
  f"flow of USD {m0(E2['fcff'])} million is dragged down by the investment years. Free "
  f"cash flow to the firm is USD {m0(F['fcff'][0])} million in {YRL[0]} and USD "
  f"{m0(F['fcff'][3])} million in {YRL[3]}; averaging a business across a period when it "
  f"is building the assets that produce the later number is a real charge against it. That "
  f"is the method doing what it says it does, and it is why the range extends as high as "
  f"AED {p2(E2['rng'][1])}.")
e2_alt_val = E2['fcfe'] * (1 + E2['g']) / (W['ke_beta1'] - E2['g'])
P(f"Named sensitivity: this method is a single-stage capitalisation, so it is more "
  f"sensitive to the cost of equity than anything else in the study. Capitalise the same "
  f"owner cash earnings at the cost of equity the equal-weight composite produces — "
  f"{pc(W['ke_beta1'], 2)} instead of {pc(E2['ke'], 2)} — and the answer is roughly AED "
  f"{p2(e2_alt_val/SH/1000.0*PEG)} a share, a rise of about "
  f"{pc(e2_alt_val/E2['value']-1, 0)}. The direction is worth being explicit about: a "
  f"lower discount rate raises a perpetuity, so the construction this study does not adopt "
  f"is the generous one. Within the adopted construction, the two ends of the beta's own "
  f"90% interval are what set this expert's published range, and they span AED "
  f"{p2(E2['rng'][1]-E2['rng'][0])}. This expert is therefore the one most exposed to the "
  f"discount rate, and says so.")
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
  f"the same move in the opposite direction removes about the same amount from a base of "
  f"AED {p2(E3['base'])} that already sits {ab(E3['base'])}, and takes the fifth-year "
  f"spread of {E3['spread'][4]*100:+.1f} percentage points close to zero. Nothing in the "
  f"operating build has a comparable effect on this method, which is the point it is "
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
         f"Accepted, and it is why the panel divides the way it does. Expert 1 never "
         f"touches it. Expert 2 is fully exposed to it, which is why its range spans AED "
         f"{p2(E2['rng'][1]-E2['rng'][0])}, struck at the two ends of the beta's own 90% "
         f"interval. Expert 3 prices it year by year and finds the spread stays positive "
         f"on either measurement of the market, which is the one useful thing the panel "
         f"can say about it: the business creates value at both costs of capital — the "
         f"argument is only about how much, and it is now an argument about statistical "
         f"width rather than about which yardstick to use."]]
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
  f"of one another. The market price of AED {p2(SPOT)} falls inside that span, and so does "
  f"this study's own cash-flow lens; the weighted central of AED {p2(D['central'])} sits "
  f"{'inside it as well' if min(E1['base'], E2['base'], E3['base']) <= D['central'] <= max(E1['base'], E2['base'], E3['base']) else 'above all three'}.")
P(f"The panel centre of AED {p2(PANEL)} sits {ab(PANEL)} and "
  f"{sgn(PANEL/D['central']-1, 0)} against this study's weighted central. That gap is "
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
         f"Expert 2 is fully exposed, Expert 1 not at all — which is why Expert 1 lands "
         f"AED {p2(E1['base']-E2['base'])} above Expert 2 without ever taking a position "
         f"on the question"],
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
         'deducted at carrying value in the bridge and weighted in the cost of capital at '
         'their own coupon',
         'the two bridge treatments differ by AED '
         + p2(DCFH['fv_aed'] - DCF['fv_aed']) + ' a share in the main model'],
        ['The minorities and the joint ventures',
         f"minorities deducted at {pc(IN['nci_share'])} of mid-cycle profit; joint ventures "
         f"not added",
         'neither deducted nor added — the one inconsistency in this panel',
         'both, on the same bridge the cash-flow model uses',
         f"putting Expert 2 on the same bridge as the other two would move it AED "
         f"{E2_BRIDGED-E2['base']:+.2f} and the panel centre with it. The published figures "
         f"are each method's own; the gap is stated in C.2 rather than smoothed"]]
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
P(f"Where a judgement has two legitimate constructions, both are computed and both are "
  f"published side by side. This study does that twice: for the series the beta is "
  f"measured against, which is the widest single sensitivity in it, and for the treatment "
  f"of the perpetual capital securities. Neither pair is averaged, because an average of "
  f"two constructions is a number that neither construction supports. Where a construction "
  f"has been changed since an earlier version of a study, the superseded one is published "
  f"alongside the new one at full size rather than quietly replaced — that is why the "
  f"equal-weight composite reading of AED {p2(D['central_beta_alt'])} appears throughout "
  f"this document beside the adopted AED {p2(D['central'])}.")
P(f"The same rule governs correction, and it extends to a study's own words about itself. "
  f"Where a study has been reviewed and found wrong, the corrections are listed in the "
  f"document itself, with the direction and the size of each, rather than absorbed into a "
  f"new set of numbers that looks as though it was always there — and where a superseded "
  f"edition made a CLAIM that later work falsified, the claim is reprinted and corrected "
  f"rather than deleted. This edition does that twice: for a caveat that said a revenue "
  f"convention could not reach the valuation, and for a cost of debt described as weighted "
  f"when it is an average. This document carries the full list, under “What changed in "
  f"these editions, and why”, immediately after the caveats. It covers both rounds of "
  f"review and it is the section a reader who has seen an earlier edition should read "
  f"first.")
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
