"""ADNOCLS_Valuation_Model_09082026_public.xlsx — 16 sheets mirroring the house canonical
model (asset-heavy marine logistics operating-company variant). Blue = inputs · black =
formulas · green = cross-sheet links.

The workbook is FORMULA-DRIVEN. Every quantity that is arithmetically derivable from an
input is written as a live Excel formula, not as a pasted number, so the reader can trace
each figure back to the drivers on the Assumptions sheet and change one to see the model
reprice. Only three classes of cell are pasted values:

  1. audited and disclosed history (the primary record) — where a line is both disclosed
     and derivable, the DISCLOSED figure is carried;
  2. the output of a unit build that would be unreadable flattened into a grid — here the
     historical segment revenue and earnings grid, which the disclosed operating-segments
     note gives directly;
  3. whole-model re-runs: the Monte Carlo price map, the sensitivity grids, the DCF
     bear/bull scenario bounds and the expert-panel legs, each cell of which is a complete
     revaluation of the entire model.

The tanker fleet build, the gas-carrier build, the cost of capital (including the three
cost-of-debt constructions and their average), the discount-factor compounding, the
statements roll (property plant and equipment, working capital from the days ratios, equity
and net debt) and every ratio and per-share figure are all live formulas.

Every formula cell also carries the model's own value for that cell into
xlsx_expected.json, and recalc.py evaluates the workbook independently and asserts the two
agree. A formula that computes the right thing the wrong way therefore fails the gate.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
V = {k: v['value'] for k, v in D['inputs'].items()}

BLUE = Font(color='0000FF'); GREEN = Font(color='008000'); BLACK = Font(color='000000')
TITLE = Font(bold=True, size=13, color='F6F1E6'); SUB = Font(size=9, color='6E7B77')
FILL_T = PatternFill('solid', start_color='1C3A36')
FILL_H = PatternFill('solid', start_color='EAF0EE')
FILL_G = PatternFill('solid', start_color='F6F1E6')
NUM0 = '#,##0;(#,##0);"-"'; NUM1 = '#,##0.0;(#,##0.0);"-"'; NUM2 = '#,##0.00;(#,##0.00);"-"'
PCT = '0.0%;(0.0%);"-"'; PCT2 = '0.00%'; PX = '0.00;(0.00);"-"'; PX3 = '0.000;(0.000);"-"'
MULT = '0.00x'; DF4 = '0.0000'; BETA = '0.000'

M = D['meta']
HI, HB, HC_, CCC = D['hist_is'], D['hist_bs'], D['hist_cf'], D['ccc']
SEGH, GRPH = D['seg_hist'], D['grp_hist']
FLEET, DRV = D['fleet'], D['drivers']
FC, FIN, FBS = D['fcst'], D['fin'], D['fcst_bs']
WACC, DCFB, DCFA = D['wacc'], D['dcf'], D['dcf_asset_beta']
LN, LW, REL, NRM, BK = D['lenses'], D['lens_weights'], D['rel'], D['norm'], D['book']
EXP, SN, STK, SOTP = D['experts'], D['sens'], D['strike'], D['sotp']
PEERS, TECH, STEP0 = D['peers'], D['technicals'], D['step0']

SEGS = D['segs']; SEG_GROUP = D['seg_group']; GROUPS = D['groups']
YH = ['FY2023', 'FY2024', 'FY2025']
YF = FC['years']
YFE = [y + 'E' for y in YF]
SPOT = M['spot_aed']; SH = M['shares_mn']; PEG = M['fx']
CLS = ['hs', 'mr', 'lr1', 'lr2', 'vlcc']
CLS_NAME = ['Handysize', 'Medium range', 'Long range 1', 'Long range 2',
            'Very large crude carrier']
CD = ['B', 'C', 'D', 'E', 'F']            # five forecast years, or five tanker classes
HC = ['B', 'C', 'D']                      # three historical years on the statements
FCOL = ['E', 'F', 'G', 'H', 'I']          # five forecast years on the statements
ALL = HC + FCOL

# ============================================================================
# THE MODEL, RECOMPUTED FROM THE COMMITTED INPUTS
# Every expected value written into xlsx_expected.json comes from here, and every line
# below is asserted against the committed study blocks at the foot of this file. No
# financial numeral is typed into this builder.
# ============================================================================
ESC = V['opex_escalation']
H2W = V['h2_2026_reversion']
GROSSUP = V['tnk_grossup_26']
ROLLOFF = [1.0, 0.5, 0.0, 0.0, 0.0]
OWNED = FLEET['owned']; SPOTN = FLEET['spot']; FIXN = FLEET['fixed']
TCOUT = FLEET['tc_out']; TCE25 = FLEET['tce_fy25']; TCEMID = FLEET['tce_mid']
Q1R = FLEET['q1_26']; Q2R = FLEET['q2_26']
OPEX_DAY = FLEET['opex_day']; GAS_VY = FLEET['gas_vessel_years']
GAS_RATE = FLEET['gas_rate_day']; GAS_MGN = V['gas_margin']
VDAYS = sum(OWNED.values()) * 365

TNK_H2 = {c: Q1R[c] * (1 - H2W) + TCE25[c] * H2W for c in CLS}
TNK_Y26 = {c: (Q1R[c] + Q2R[c] + 2 * TNK_H2[c]) / 4.0 for c in CLS}
TNK_PATH = {c: [TNK_Y26[c] + (TCEMID[c] - TNK_Y26[c]) * i / 4.0 for i in range(5)]
            for c in CLS}
TNK_SPOTREV = [sum(SPOTN[c] * TNK_PATH[c][i] for c in CLS) * 365 / 1000.0 for i in range(5)]
TNK_FIXREV = [sum(FIXN[c] * (TCOUT[c] * ROLLOFF[i] + TNK_PATH[c][i] * (1 - ROLLOFF[i]))
                  for c in CLS) * 365 / 1000.0 for i in range(5)]
TNK_TCEREV = [a + b for a, b in zip(TNK_SPOTREV, TNK_FIXREV)]
TNK_OPEXD = [OPEX_DAY * (1 + ESC) ** (i + 1) for i in range(5)]
TNK_OPEX = [VDAYS * TNK_OPEXD[i] / 1000.0 for i in range(5)]
TNK_EBITDA = [TNK_TCEREV[i] - TNK_OPEX[i] for i in range(5)]
TNK_REV = [TNK_TCEREV[i] * GROSSUP for i in range(5)]

GAS_RATED = [GAS_RATE * (1 + ESC) ** (i + 1) for i in range(5)]
GAS_REV = [GAS_VY[i] * 365 * GAS_RATED[i] / 1000.0 for i in range(5)]
GAS_EBITDA = [r * GAS_MGN for r in GAS_REV]

SEG_REV_F, SEG_EB_F = {}, {}
for s in SEGS:
    if s == 'Tankers':
        SEG_REV_F[s], SEG_EB_F[s] = list(TNK_REV), list(TNK_EBITDA)
    elif s == 'Gas Carriers':
        SEG_REV_F[s], SEG_EB_F[s] = list(GAS_REV), list(GAS_EBITDA)
    else:
        SEG_REV_F[s] = list(DRV[s]['rev'])
        SEG_EB_F[s] = [r * m for r, m in zip(DRV[s]['rev'], DRV[s]['mar'])]
REV_F = [sum(SEG_REV_F[s][i] for s in SEGS) for i in range(5)]
EB_F = [sum(SEG_EB_F[s][i] for s in SEGS) for i in range(5)]
GRP_REV_F = {g: [sum(SEG_REV_F[s][i] for s in SEGS if SEG_GROUP[s] == g) for i in range(5)]
             for g in GROUPS}
GRP_EB_F = {g: [sum(SEG_EB_F[s][i] for s in SEGS if SEG_GROUP[s] == g) for i in range(5)]
            for g in GROUPS}

DEP_RATE = V['dep_rate_ppe']; OTHER_DNA = V['other_dna_run_rate']
CAPEX = [V[f'capex_{y[2:]}'] for y in YF]
PPE_OPEN, PPE_CLOSE, DEP1, DEP_PPE = [], [], [], []
_o = V['ppe_fy25']
for i in range(5):
    d1 = DEP_RATE * (_o + (_o + CAPEX[i])) / 2.0
    d = DEP_RATE * (_o + max(_o + CAPEX[i] - d1, 0)) / 2.0
    PPE_OPEN.append(_o); DEP1.append(d1); DEP_PPE.append(d)
    PPE_CLOSE.append(_o + CAPEX[i] - d); _o = PPE_CLOSE[-1]
OTHER_DNA_Y = [OTHER_DNA * (1 + ESC) ** (i + 1) for i in range(5)]
DNA_F = [DEP_PPE[i] + OTHER_DNA_Y[i] for i in range(5)]
EBIT_F = [EB_F[i] - DNA_F[i] for i in range(5)]

SEG_DNA25 = {s: V['seg_dna_' + s.lower().replace(' ', '_').replace('-', '_') + '_fy25']
             for s in SEGS}
SEG_DNA_TOT = sum(SEG_DNA25.values())
GRP_DNA_SHARE = {g: sum(SEG_DNA25[s] for s in SEGS if SEG_GROUP[s] == g) / SEG_DNA_TOT
                 for g in GROUPS}
TAX_G = {'Integrated Logistics': V['tax_integrated_logistics'],
         'Shipping': V['tax_shipping'], 'Services': V['tax_services']}
GRP_DNA_F = {g: [DNA_F[i] * GRP_DNA_SHARE[g] for i in range(5)] for g in GROUPS}
GRP_TAXABLE = {g: [max(GRP_EB_F[g][i] - GRP_DNA_F[g][i], 0) for i in range(5)]
               for g in GROUPS}
GRP_TAX = {g: [GRP_TAXABLE[g][i] * TAX_G[g] for i in range(5)] for g in GROUPS}
TAX_F = [sum(GRP_TAX[g][i] for g in GROUPS) for i in range(5)]
TAXRATE_F = [TAX_F[i] / EBIT_F[i] for i in range(5)]
NOPAT_F = [EBIT_F[i] - TAX_F[i] for i in range(5)]
OPCOST_F = [REV_F[i] - EB_F[i] for i in range(5)]

OPCOST25 = V['rev_fy25'] - HI['ebitda_op'][2]
DSO = CCC['dso'][2]
DIO = V['inv_fy25'] / OPCOST25 * 365
DPO = (V['pay_fy25'] + V['dtr_c_fy25']) / OPCOST25 * 365
NWC25 = HB['nwc'][2]
RECV_F = [REV_F[i] * DSO / 365 for i in range(5)]
INV_F = [OPCOST_F[i] * DIO / 365 for i in range(5)]
PAY_F = [OPCOST_F[i] * DPO / 365 for i in range(5)]
NWC_F = [RECV_F[i] + INV_F[i] - PAY_F[i] for i in range(5)]
DNWC_F = [NWC_F[0] - NWC25] + [NWC_F[i] - NWC_F[i - 1] for i in range(1, 5)]
FCFF_F = [NOPAT_F[i] + DNA_F[i] - CAPEX[i] - DNWC_F[i] for i in range(5)]

# --- cost of capital ---------------------------------------------------------
MKTCAP = SH * SPOT / PEG * 1000.0
RF_STAR = V['rf_observed'] - V['sov_spread']
KE = RF_STAR + V['beta'] * V['erp_total']
KE_A = RF_STAR + 1.0 * V['erp_total']
KD1 = V['sofr'] + V['shldr_margin']
KD_BANK = (V['bank_loan_lo'] + V['bank_loan_hi']) / 2
KD_OTHER = (V['other_borr_lo'] + V['other_borr_hi']) / 2
KD_TP = (KD_BANK + KD_OTHER) / 2
KD_LEASE = V['intpaid_lease_fy25'] / ((V['lease_open_fy25'] + V['lease_close_fy25']) / 2)
DEBT_NOW = V['q1_26_shldr_loan'] + V['q1_26_borrowings'] + V['q1_26_leases']
KD2 = (V['q1_26_shldr_loan'] * KD1 + V['q1_26_borrowings'] * KD_TP
       + V['q1_26_leases'] * KD_LEASE) / DEBT_NOW
KD3 = KD_BANK
KD = (KD1 + KD2 + KD3) / 3
TAXS = V['tax_stat']
KD_AT = KD * (1 - TAXS)
WE = MKTCAP / (MKTCAP + DEBT_NOW); WD = 1 - WE
W_EXP = WE * KE + WD * KD_AT
KE_T = V['rf_terminal'] + V['beta'] * V['erp_total']
KE_T_A = V['rf_terminal'] + 1.0 * V['erp_total']
KD_T = V['rf_terminal'] + (KD - RF_STAR)
KD_T_AT = KD_T * (1 - TAXS)
W_TERM = WE * KE_T + WD * KD_T_AT
W_EXP_A = WE * KE_A + WD * KD_AT
W_TERM_A = WE * KE_T_A + WD * KD_T_AT

STUB = 0.75
G = V['g_terminal']
NDCO = V['q1_26_netdebt']; DEFERRED = V['q1_26_pcp']; HYBRID = V['q1_26_hybrid']
NCI_BV = V['q1_26_nci']; JV_BV = V['jv_bv_q126']; EQP0 = V['q1_26_eqp']
CASH = V['q1_26_cash']; Q1FCF = V['q1_26_fcf']
NETDEBT = NDCO + DEFERRED
INTANG = V['intang_fy25']; GW = V['gw_fy25']
IC_F = [PPE_CLOSE[i] + NWC_F[i] + INTANG + GW for i in range(5)]


def dcf_legs(w, wt):
    glide = [w + (wt - w) * (i + 1) / 5.0 for i in range(5)]
    df, cum = [], 1.0
    for i, rr in enumerate(glide):
        cum *= (1 + rr) ** (STUB if i == 0 else 1.0)
        df.append(1.0 / cum)
    fcffd = list(FCFF_F); fcffd[0] -= Q1FCF
    pv = [c * d for c, d in zip(fcffd, df)]
    pv_expl = sum(pv)
    roic_t = NOPAT_F[4] / IC_F[4]
    reinv = G / roic_t
    nopat_t1 = NOPAT_F[4] * (1 + G)
    tv = nopat_t1 * (1 - reinv) / (wt - G)
    pv_tv = tv * df[4]
    ev_ops = pv_expl + pv_tv
    ev = ev_ops + JV_BV
    eq = ev - NETDEBT - HYBRID - NCI_BV
    return dict(glide=glide, df=df, fcffd=fcffd, pv=pv, pv_expl=pv_expl, roic_t=roic_t,
                reinv=reinv, nopat_t1=nopat_t1, tv=tv, pv_tv=pv_tv,
                tv_share=pv_tv / ev_ops, ev_ops=ev_ops, ev=ev, equity=eq,
                fv_usd=eq / SH / 1000.0, fv_aed=eq / SH / 1000.0 * PEG)


DC = dcf_legs(W_EXP, W_TERM)
DA = dcf_legs(W_EXP_A, W_TERM_A)

# --- the funding roll and the forecast statements -----------------------------
DPS = [V['dps_2026_usd'] * 1000.0 * (1 + V['div_growth']) ** i for i in range(5)]
HYB_CPN = HYBRID * (V['sofr'] + V['hybrid_margin'])
NCI_SHARE = V['nci_share']
ND_OPEN, GROSS_D, INT_F, FININC_F, ND_CLOSE, FCFE_F = [], [], [], [], [], []
_nd = NETDEBT
for i in range(5):
    g_open = _nd + CASH
    it = KD * g_open
    fi = V['sofr'] * CASH
    fcfe = FCFF_F[i] - it * (1 - TAXS) + fi * (1 - TAXS) - HYB_CPN
    ND_OPEN.append(_nd); GROSS_D.append(g_open); INT_F.append(it); FININC_F.append(fi)
    FCFE_F.append(fcfe); ND_CLOSE.append(_nd - fcfe + DPS[i]); _nd = ND_CLOSE[-1]
PBT_F = [EBIT_F[i] - INT_F[i] + FININC_F[i] for i in range(5)]
TAXP_F = [PBT_F[i] * TAXRATE_F[i] for i in range(5)]
PAT_F = [PBT_F[i] - TAXP_F[i] for i in range(5)]
NCI_F = [PAT_F[i] * NCI_SHARE for i in range(5)]
NPA_F = [PAT_F[i] - NCI_F[i] for i in range(5)]
ORD_F = [NPA_F[i] - HYB_CPN for i in range(5)]
EQ_OPEN, EQ_CLOSE = [], []
_e = EQP0
for i in range(5):
    EQ_OPEN.append(_e); _e = _e + NPA_F[i] - DPS[i] - HYB_CPN; EQ_CLOSE.append(_e)
ROE_F = [NPA_F[i] / ((EQ_OPEN[i] + EQ_CLOSE[i]) / 2) for i in range(5)]
ROIC_F = [NOPAT_F[i] / IC_F[i] for i in range(5)]
BVPS_F = [EQ_CLOSE[i] / SH / 1000.0 for i in range(5)]

# --- the lenses ---------------------------------------------------------------
SPOT_W = V['spot_share_ebitda_26']
MULT_CONTR = PEERS[0]['ev_ebitda']
MULT_SPOT = (PEERS[1]['ev_ebitda'] + PEERS[2]['ev_ebitda']) / 2
BLEND_EV = (1 - SPOT_W) * MULT_CONTR + SPOT_W * MULT_SPOT
BLEND_PE = (1 - SPOT_W) * PEERS[0]['pe_fwd'] + SPOT_W * PEERS[1]['pe_fwd']


def eq_from_ev(ev):
    return ev + JV_BV - NETDEBT - HYBRID - NCI_BV


def per_share(eq):
    return eq / SH / 1000.0 * PEG


REL_EV = BLEND_EV * EB_F[0]
REL_V_EV = per_share(eq_from_ev(REL_EV))
REL_V_PE = BLEND_PE * ORD_F[0] / SH / 1000.0 * PEG
W_EVEB = V['rel_weight_ev_ebitda']
REL_BASE = W_EVEB * REL_V_EV + (1 - W_EVEB) * REL_V_PE
REL_BEAR = per_share(eq_from_ev(MULT_SPOT * EB_F[0]))
REL_BULL = per_share(eq_from_ev(MULT_CONTR * EB_F[0]))
NORM_EB = sum(EB_F) / 5.0
NORM_ORD = sum(NPA_F) / 5.0 - HYB_CPN
NORM_V_EV = per_share(eq_from_ev(BLEND_EV * NORM_EB))
NORM_EPS = NORM_ORD / SH / 1000.0
NORM_V_PE = NORM_EPS * BLEND_PE * PEG
NORM_BASE = (NORM_V_EV + NORM_V_PE) / 2
NORM_BEAR = per_share(eq_from_ev(MULT_SPOT * NORM_EB))
NORM_BULL = per_share(eq_from_ev(MULT_CONTR * NORM_EB))
ROE_SUST = sum(ROE_F) / 5.0
BVPS0 = EQP0 / SH / 1000.0
PB_FAIR = (ROE_SUST - G) / (KE - G)
BOOK_BASE = PB_FAIR * BVPS0 * PEG
BOOK_BEAR = ((ROE_SUST * 0.85) - G) / (KE_A - G) * BVPS0 * PEG
BOOK_BULL = ((ROE_SUST * 1.15) - G) / ((RF_STAR + 0.55 * V['erp_total']) - G) * BVPS0 * PEG
VSB_RATIO = V['vessel_sale_price'] / V['vessel_sale_book']

LB = {'dcf': (LN['dcf']['bear'], DC['fv_aed'], LN['dcf']['bull']),
      'relative': (REL_BEAR, REL_BASE, REL_BULL),
      'normalized': (NORM_BEAR, NORM_BASE, NORM_BULL),
      'book': (BOOK_BEAR, BOOK_BASE, BOOK_BULL)}
CENTRAL = sum(LW[k] * LB[k][1] for k in LB)
CENTRAL_A = CENTRAL - LW['dcf'] * DC['fv_aed'] + LW['dcf'] * DA['fv_aed']
CENTRAL_BEAR = sum(LW[k] * LB[k][0] for k in LB)
CENTRAL_BULL = sum(LW[k] * LB[k][2] for k in LB)

# --- the sum-of-the-parts cross-check -----------------------------------------
SOTP_MULT = {'Integrated Logistics': MULT_CONTR, 'Services': MULT_CONTR,
             'Shipping': BLEND_EV}
SOTP_EV = {g: GRP_EB_F[g][0] * SOTP_MULT[g] for g in GROUPS}
SOTP_EVOPS = sum(SOTP_EV.values())
SOTP_EQ = SOTP_EVOPS + JV_BV - NETDEBT - HYBRID - NCI_BV
SOTP_FV = per_share(SOTP_EQ)

# --- the own multiples --------------------------------------------------------
EV_NOW = MKTCAP + NETDEBT
OWN_EVEB_TTM = EV_NOW / HI['ebitda_reported'][2]
OWN_EVEB_26 = EV_NOW / EB_F[0]
OWN_PE_TTM = MKTCAP / (V['npa_fy25'] - V['hybrid_coupon_fy25'])
OWN_PB = MKTCAP / (EQP0 + HYBRID)
OWN_DY = V['dps_2026_usd'] * 1000.0 / MKTCAP

# --- historical statement derivations ----------------------------------------
H_DNA = HI['dna']; H_EBITDA = HI['ebitda_op']; H_REV = HI['revenue']
H_OPCOST = [H_REV[i] - H_EBITDA[i] for i in range(3)]
H_NWC = HB['nwc']; H_ND = HB['net_debt']; H_EQ = HB['equity_parent']
H_NPA = HI['npa']
H_ORD = [H_NPA[0], H_NPA[1], H_NPA[2] - V['hybrid_coupon_fy25']]
H_HYBCPN = [0.0, 0.0, V['hybrid_coupon_fy25']]
H_GROSSD = HB['debt']
H_IC = [HB['ppe'][i] + H_NWC[i] + HB['intangibles'][i] + HB['goodwill'][i] for i in range(3)]

REV_ALL = H_REV + REV_F
EB_ALL = H_EBITDA + EB_F
EBIT_ALL = HI['ebit'] + EBIT_F
DNA_ALL = H_DNA + DNA_F
NPA_ALL = H_NPA + NPA_F
ORD_ALL = H_ORD + ORD_F
HYBCPN_ALL = H_HYBCPN + [HYB_CPN] * 5
ND_ALL = H_ND + ND_CLOSE
EQ_ALL = H_EQ + EQ_CLOSE
NWC_ALL = H_NWC + NWC_F
IC_ALL = H_IC + IC_F
GROSSD_ALL = H_GROSSD + GROSS_D
OPCOST_ALL = H_OPCOST + OPCOST_F
CAPEX_ALL = list(HC_['capex']) + [-x for x in CAPEX]

wb = Workbook()
EXPECT, ANCH = {}, {}


def sheet(n):
    ws = wb.create_sheet(n) if wb.sheetnames != ['Sheet'] else wb.active
    ws.title = n
    return ws


def title(ws, t, s=None, w=10, awidth=48, cwidth=13):
    ws['A1'] = t; ws['A1'].font = TITLE; ws['A1'].fill = FILL_T
    for c in range(2, w + 1):
        ws.cell(row=1, column=c).fill = FILL_T
    if s:
        ws['A2'] = s; ws['A2'].font = SUB
    ws.column_dimensions['A'].width = awidth
    for c in range(2, w + 1):
        ws.column_dimensions[get_column_letter(c)].width = cwidth


def put(ws, ad, v, font=BLACK, fmt=NUM0, bold=False, fill=None, wrap=False):
    c = ws[ad]; c.value = v
    c.font = Font(color=font.color, bold=bold)
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    if wrap: c.alignment = Alignment(wrap_text=True, vertical='top')
    return c


def putf(ws, ad, formula, expect, fmt=NUM0, bold=False, green=False):
    """Write a live formula and record the model's own value for the same cell."""
    put(ws, ad, formula, GREEN if green else BLACK, fmt, bold=bold)
    if expect is None:
        raise ValueError(f'formula at {ws.title}!{ad} carries no expected value')
    EXPECT.setdefault(ws.title, {})[ad] = float(expect)


def hdr(ws, row, labels, start=1):
    for i, l in enumerate(labels):
        c = ws.cell(row=row, column=start + i, value=l)
        c.font = Font(bold=True); c.fill = FILL_H


def band(ws, row, w=10):
    for c in range(1, w + 1):
        ws.cell(row=row, column=c).fill = FILL_G
        ws.cell(row=row, column=c).font = Font(bold=True)


def note(ws, ad, text):
    put(ws, ad, text, fmt=None).font = SUB


# ============ 1 READ FIRST ====================================================
ws = sheet('READ FIRST')
title(ws, 'Testahil — ADNOC Logistics & Services plc (ADX: ADNOCLS)', None, 9)
for i, ln in enumerate([
 'Companion model · Independent Valuation Study · Educational analysis · Not investment advice', '',
 'What this workbook is. A transparent companion to the ADNOC L&S valuation study. Every blue cell is an',
 'input; every black cell is a formula; green cells link across sheets.', '',
 'IT IS FORMULA-DRIVEN. Every figure that can be derived arithmetically from a driver is a live formula, so',
 'you can change a blue cell on Assumptions and watch the model reprice. The cost of equity is built from the',
 'normalised risk-free rate, the beta and the equity risk premium — and the normalised rate is itself a',
 'formula, the observed government bond yield less the sovereign default spread. The cost of debt is built',
 'three separate ways on the sheet — the parent facility at the overnight financing rate plus its margin, a',
 'weighted blend of the instruments the company actually has outstanding, and the disclosed third-party',
 'bank-loan midpoint — and the three are averaged in a cell. The discount factors compound year on year off',
 'the cost-of-capital glide, with a three-quarter stub for 2026 because the valuation date is 31 March 2026.',
 'The tanker fleet is built vessel by vessel from the vessel counts and day rates on Assumptions; the balance',
 'sheet rolls property, plant and equipment, working capital, equity and net debt forward; and every ratio and',
 'per-share figure, including the conversion to dirhams at the fixed parity, is a formula.', '',
 'THREE THINGS ARE PASTED VALUES, and it is worth knowing exactly which.',
 '  (1) AUDITED AND DISCLOSED HISTORY — the primary record, not a calculation. Where a line is both disclosed',
 '      and arithmetically derivable, the DISCLOSED figure is carried, because the filing is the record.',
 '  (2) THE OUTPUT OF A UNIT BUILD that would be unreadable flattened into a grid — the historical segment',
 '      revenue and earnings table, which the operating-segments note gives directly.',
 '  (3) WHOLE-MODEL RE-RUNS, where each figure is a complete revaluation of the entire model and so cannot be',
 '      a single formula: the Monte Carlo price map, the two sensitivity grids, the discounted-cash-flow',
 '      bear and bull bounds (each of which re-runs the fleet build at a different rate anchor, a different',
 '      beta and a different capital-expenditure path) and the three expert-panel legs.',
 '  THE MONTE CARLO AND SENSITIVITY GRIDS DO NOT REDRAW WHEN A DRIVER IS CHANGED. Changing a blue cell',
 '  reprices the whole valuation chain, but those grids are engine outputs and stay as they were run.',
 '  Anything else pasted is a defect.', '',
 'How revenue is built. Not as one growth rate. The tanker fleet is built vessel by vessel: fifty-three owned',
 'vessels split into those trading at spot rates and those on charters out at rates already fixed and',
 'disclosed, each class earning its own time-charter equivalent per day over 365 days, less an all-in running',
 'cost per vessel per day escalated on a services-and-wage escalator. The gas carriers are built from',
 'contracted vessel-years times an implied day rate. The five remaining units are grown on their own revenue',
 'and margin drivers, anchored on what each actually earned in the first quarter of 2026.', '',
 'THE CONTESTED JUDGEMENT, PUBLISHED BOTH WAYS. The stock\'s own weekly regression against its local index',
 f"gives a beta of {V['beta']:.3f}, which passes the usability gate and is the primary reading. An asset-risk",
 'beta of 1.00 — what a listed fleet owner might be expected to carry — gives a materially different cost of',
 'equity. BOTH are carried through the model in full, side by side, on the Summary and Fundamental Valuation',
 'sheets. They are NOT averaged into one number.', '',
 'What it is not. It is not investment advice, a recommendation, or a price target. Values are model outputs',
 'shown as ranges and distributions.', '',
 'Sourcing note, up front. FY2023, FY2024 and FY2025 come from the company\'s own audited consolidated',
 'financial statements; the first quarter of 2026 comes from the reviewed interim statements; the fleet,',
 'rate and contract data come from the company\'s own investor presentations and earnings calls. Every input',
 'is listed with its value, source and date in the companion bibliography document.', '',
 f"Currency. US dollar thousand unless stated — the company reports in US dollars. Per-share figures are in",
 f"dirhams at the fixed parity of {PEG:.4f} dirhams to the dollar. Spot AED {SPOT:.2f} ({M['price_date']} close).",
 'Sheets: READ FIRST · Summary · Fundamental Valuation · Assumptions · SOTP Bridge · Segments · Relative &',
 'Normalized · DCF · Income Statement · Balance Sheet · Cash Flow · Summary Financials · Monte Carlo ·',
 'Sensitivity · Per-Share & Ratios · Peer & Sector.'], start=3):
    ws.cell(row=i, column=1, value=ln).font = Font(size=10)
ws.column_dimensions['A'].width = 114

# ============ 2 SUMMARY =======================================================
ws = sheet('Summary')
title(ws, 'Summary — valuation at a glance', 'All values link live to their source sheets. '
      'AED per share unless stated.', 8, awidth=52, cwidth=15)
hdr(ws, 4, ['Lens', 'Bear', 'Base', 'Bull', 'Weight', 'Contribution', 'vs spot',
            'Terminal value share'])
S_SPOT = 16
LENS_ROWS = {'dcf': 5, 'relative': 6, 'normalized': 7, 'book': 8}
LENS_LABEL = {'dcf': 'Discounted cash flow (own regressed beta)',
              'relative': 'Relative multiples',
              'normalized': 'Normalised earnings power',
              'book': 'Book value and sustainable return'}
LENS_BASE_SRC = {'dcf': '=DCF!$C$%d', 'relative': "='Relative & Normalized'!$C$%d",
                 'normalized': "='Relative & Normalized'!$C$%d",
                 'book': "='Relative & Normalized'!$C$%d"}
SUMMARY_LENS_SRC = {}    # filled once the source sheets know their own row numbers

# ============ 3 FUNDAMENTAL VALUATION =========================================
ws = sheet('Fundamental Valuation')
title(ws, 'Fundamental valuation — the four lenses and the contested judgement', None, 6,
      awidth=58, cwidth=16)

# ============ 4 ASSUMPTIONS ====================================================
ws = sheet('Assumptions')
title(ws, 'Assumptions — every input in the model', 'Blue cells are inputs. Change one and '
      'the model reprices: everything downstream is a formula.', 8, awidth=62, cwidth=14)
r = 4
A = {}


def block(name, items, cols=None):
    global r
    band(ws, r, 8); put(ws, f'A{r}', name, bold=True, fmt=None)
    if cols:
        for i, c in enumerate(cols):
            cc = ws.cell(row=r, column=2 + i, value=c)
            cc.font = Font(bold=True); cc.fill = FILL_G
    r += 1
    for key, lab, val, fmt in items:
        put(ws, f'A{r}', lab, fmt=None)
        if isinstance(val, (list, tuple)):
            for i, v in enumerate(val):
                put(ws, f'{get_column_letter(2+i)}{r}', v, BLUE if isinstance(v, (int, float))
                    else BLACK, fmt)
        else:
            put(ws, f'C{r}', val, BLUE, fmt)
        A[key] = r
        r += 1
    r += 1


def a(key, i=None, col=None):
    """Absolute reference to an Assumptions cell; i or col selects a list column."""
    c = col if col else (get_column_letter(2 + i) if i is not None else 'C')
    return f"Assumptions!${c}${A[key]}"


block('Market and share anchors', [
    ('spot', 'Share price (AED, Abu Dhabi Securities Exchange close)', SPOT, PX),
    ('shares', 'Shares outstanding (mn)', SH, NUM1),
    ('fx', 'Dirhams per US dollar (fixed parity, unchanged since 1997)', PEG, DF4),
    ('stub', 'Stub year fraction — 31 March 2026 valuation date to 31 December 2026',
     STUB, '0.00'),
    ('q1fcf', 'First-quarter 2026 free cash flow, already inside net debt at the valuation '
     'date (USD 000)', Q1FCF, NUM0)])
block('Cost of capital', [
    ('rf_obs', 'Observed government bond yield (dirham tranche maturing January 2031)',
     V['rf_observed'], PCT2),
    ('sov', 'Sovereign default spread (netted out of the risk-free rate)', V['sov_spread'],
     PCT2),
    ('beta', 'Beta — own-stock weekly regression against its local index', V['beta'], BETA),
    ('beta_a', 'Asset-risk beta — the contested alternative', 1.0, BETA),
    ('erp', 'Equity risk premium (mature premium plus country risk)', V['erp_total'], PCT2),
    ('rf_term', 'Terminal risk-free rate', V['rf_terminal'], PCT2),
    ('tax_stat', 'Statutory corporate tax rate', TAXS, PCT)])
block('Cost of debt — the evidence behind the three constructions', [
    ('sofr', 'Secured overnight financing rate', V['sofr'], PCT2),
    ('shldr_m', 'Parent revolving credit facility margin', V['shldr_margin'], PCT2),
    ('bank_lo', 'Third-party bank loans — low end of the disclosed range', V['bank_loan_lo'],
     PCT2),
    ('bank_hi', 'Third-party bank loans — high end of the disclosed range', V['bank_loan_hi'],
     PCT2),
    ('oth_lo', 'Other third-party borrowings — low end of the disclosed range',
     V['other_borr_lo'], PCT2),
    ('oth_hi', 'Other third-party borrowings — high end of the disclosed range',
     V['other_borr_hi'], PCT2),
    ('lease_int', 'Lease interest charged in 2025 (USD 000)', V['intpaid_lease_fy25'], NUM0),
    ('lease_open', 'Lease liabilities, opening balance 2025 (USD 000)', V['lease_open_fy25'],
     NUM0),
    ('lease_close', 'Lease liabilities, closing balance 2025 (USD 000)',
     V['lease_close_fy25'], NUM0),
    ('d_shldr', 'Shareholder loan at 31 March 2026 (USD 000)', V['q1_26_shldr_loan'], NUM0),
    ('d_borr', 'Third-party borrowings at 31 March 2026 (USD 000)', V['q1_26_borrowings'],
     NUM0),
    ('d_lease', 'Lease liabilities at 31 March 2026 (USD 000)', V['q1_26_leases'], NUM0)])
block('Tanker fleet — vessel counts and day rates by class',
      [('tnk_own', 'Vessels owned', [OWNED[c] for c in CLS], NUM0),
       ('tnk_spot', 'Vessels trading at spot rates', [SPOTN[c] for c in CLS], NUM0),
       ('tnk_tcout', 'Fixed charter-out rate (USD per day)',
        ['-' if TCOUT[c] == 0 else TCOUT[c] for c in CLS], NUM0),
       ('tnk_tce25', '2025 average time-charter equivalent (USD per day)',
        [TCE25[c] for c in CLS], NUM0),
       ('tnk_q1', 'First-quarter 2026 time-charter equivalent (USD per day)',
        [Q1R[c] for c in CLS], NUM0),
       ('tnk_q2', 'Second-quarter 2026 time-charter equivalent (USD per day)',
        [Q2R[c] for c in CLS], NUM0),
       ('tnk_mid', 'Mid-cycle rate anchor (USD per day)', [TCEMID[c] for c in CLS], NUM0)],
      cols=CLS_NAME)
block('Tanker fleet — rate path and running cost', [
    ('h2w', 'Weight on the 2025 average rate in setting the second half of 2026', H2W, PCT),
    ('opex_day', 'All-in running cost per vessel per day (USD)', OPEX_DAY, NUM1),
    ('opex_esc', 'Running-cost escalation (services and wages)', ESC, PCT),
    ('grossup', 'Gross-up from time-charter-equivalent revenue to reported revenue',
     GROSSUP, '0.00')])
block('Tanker charter-out roll-off and gas-carrier contracts',
      [('roll', 'Charter-out contracts still running (share of the year)', ROLLOFF, PCT),
       ('gas_vy', 'Gas carriers — contracted vessel-years', GAS_VY, NUM1),
       ('gas_rate', 'Gas carriers — implied revenue per vessel-day (USD)', GAS_RATE, NUM0),
       ('gas_mgn', 'Gas carriers — earnings margin', GAS_MGN, PCT)], cols=YF)
_items = []
for s in SEGS:
    if s in ('Tankers', 'Gas Carriers'):
        continue
    k = s.lower().replace(' ', '_').replace('-', '_')
    _items.append((f'rev_{k}', f'{s} — revenue (USD 000)', DRV[s]['rev'], NUM0))
    _items.append((f'mar_{k}', f'{s} — earnings margin', DRV[s]['mar'], PCT))
block('The remaining five units — revenue and margin drivers', _items, cols=YF)
block('Capital expenditure, depreciation and working capital',
      [('capex', 'Capital expenditure (USD 000)', CAPEX, NUM0),
       ('dep_rate', 'Depreciation rate on property, plant and equipment', DEP_RATE, PCT2),
       ('other_dna', 'Other depreciation and amortisation, 2026 run rate (USD 000)',
        OTHER_DNA, NUM0),
       ('dso', 'Days sales outstanding', DSO, NUM1),
       ('dio', 'Days inventory outstanding', DIO, NUM1),
       ('dpo', 'Days payable outstanding', DPO, NUM1),
       ('nwc25', 'Net working capital at 31 December 2025 (USD 000)', NWC25, NUM0)],
      cols=YF)
block('Tax by business unit and the 2025 depreciation allocation basis', [
    ('tax_il', 'Integrated Logistics — income tax rate', TAX_G['Integrated Logistics'], PCT),
    ('tax_ship', 'Shipping — income tax rate', TAX_G['Shipping'], PCT),
    ('tax_serv', 'Services — income tax rate', TAX_G['Services'], PCT)]
    + [('dna_' + s.lower().replace(' ', '_').replace('-', '_'),
        f'{s} — 2025 depreciation and amortisation (USD 000)', SEG_DNA25[s], NUM0)
       for s in SEGS])
block('Funding, distributions and the bridge', [
    ('nd_co', 'Net debt at 31 March 2026, company basis (USD 000)', NDCO, NUM0),
    ('deferred', 'Deferred consideration on acquisitions (USD 000)', DEFERRED, NUM0),
    ('hybrid', 'Perpetual capital securities at carrying value (USD 000)', HYBRID, NUM0),
    ('hyb_m', 'Perpetual capital securities margin over the overnight rate',
     V['hybrid_margin'], PCT2),
    ('nci_bv', 'Non-controlling interests at carrying value (USD 000)', NCI_BV, NUM0),
    ('nci_sh', 'Non-controlling interests\' share of profit', NCI_SHARE, PCT),
    ('jv', 'Joint ventures and associates at carrying value (USD 000)', JV_BV, NUM0),
    ('eqp0', 'Equity attributable to shareholders at 31 March 2026 (USD 000)', EQP0, NUM0),
    ('cash', 'Cash and cash equivalents held (USD 000)', CASH, NUM0),
    ('intang', 'Intangible assets (USD 000)', INTANG, NUM0),
    ('gw', 'Goodwill (USD 000)', GW, NUM0),
    ('dps26', 'Ordinary dividend declared for 2026 (USD 000)', DPS[0], NUM0),
    ('div_g', 'Ordinary dividend growth', V['div_growth'], PCT),
    ('g_term', 'Terminal growth', G, PCT)])
block('Lens weights and the multiple blend', [
    ('spot_w', 'Share of 2026 earnings exposed to spot rates', SPOT_W, PCT),
    ('w_eveb', 'Weight on the enterprise multiple within the relative lens', W_EVEB, PCT),
    ('w_dcf', 'Weight — discounted cash flow', LW['dcf'], PCT),
    ('w_rel', 'Weight — relative multiples', LW['relative'], PCT),
    ('w_norm', 'Weight — normalised earnings power', LW['normalized'], PCT),
    ('w_book', 'Weight — book value and sustainable return', LW['book'], PCT)])
block('The realised vessel sale — direct evidence on carrying values', [
    ('vs_book', 'Carrying value of the very large crude carrier sold (USD 000)',
     V['vessel_sale_book'], NUM0),
    ('vs_price', 'Realised sale price, January 2026 (USD 000)', V['vessel_sale_price'],
     NUM0),
    ('vs_gain', 'Capital gain recognised on the sale, as disclosed (USD 000)',
     V['vessel_sale_gain'], NUM0)])
ASSUMPTIONS_LAST = r

# ---- fixed row plans, so every sheet can reference every other ---------------
# Segments
SG = dict(revh=4, revh0=5, revht=12, ebh=14, ebh0=15, ebht=22, mgnh=23,
          tband=25, own=26, spotn=27, fix=28, tcout=29, tce25=30, q1=31, q2=32,
          h2=33, y26=34, mid=35, pathb=37, path0=38, buildb=44, spotrev=45,
          fixrev=46, tcerev=47, vdays=48, opexd=49, opex=50, teb=51, gross=52,
          trev=53, gasb=55, gasvy=56, gasrate=57, gasrev=58, gasmgn=59, gaseb=60,
          unitb=62, unit0=63, frevb=74, frev0=75, frevt=82, febb=84, feb0=85,
          febt=92, fmgn=93, grpb=95, grev0=96, geb0=99, gmgn0=102)
# DCF
DF_ = dict(rev=5, ebitda=6, mgn=7, dna=8, ebit=9, tax=10, nopat=11, adddna=12,
           capex=13, dnwc=14, fcff=15, q1=16, fcfd=17, glide=18, df=19, pv=20,
           taxb=22, geb0=23, gdna0=26, gtax0=29, gtaxc0=32, taxtot=35, taxrate=36,
           tvb=38, g=39, ic=40, roic=41, reinv=42, nopat1=43, tv=44, pvex=45,
           pvtv=46, evops=47, tvshare=48, jv=49, ev=50, nd=51, defd=52, hyb=53,
           nci=54, eq=55, fvusd=56, fvaed=57,
           keb=59, rfobs=60, sov=61, rfstar=62, beta=63, erp=64, ke=65,
           kdb=67, sofr=68, shldrm=69, kd1=70, banklo=71, bankhi=72, bankmid=73,
           othlo=74, othhi=75, othmid=76, tp=77, leaseint=78, leaseopen=79,
           leaseclose=80, kdlease=81, dshldr=82, dborr=83, dlease=84, dtot=85,
           kd2=86, kd3=87, kd=88, taxstat=89, kdat=90,
           wb=92, mktcap=93, borr=94, we=95, wd=96, wacc=97, rfterm=98, keterm=99,
           kdterm=100, kdtermat=101, waccterm=102,
           ab=104, betaa=105, kea=106, keta=107, wacca=108, wactermsa=109,
           ahdr=110, glidea=111, dfa=112, pva=113, pvexa=114, tva=115, pvtva=116,
           evopsa=117, tvsharea=118, eva=119, eqa=120, fvaeda=121)
# Income statement
IS = dict(rev=5, dc=6, gp=7, ga=8, ecl=9, oi=10, oe=11, op=12, dna=13, ebitda=14,
          ebjv=15, ebrep=16, opcost=17, mgn=18, assoc=19, bargain=20, prevheld=21,
          fininc=22, fincost=23, pbt=24, tax=25, pat=26, nci=27, npa=28, hybcpn=29,
          ordn=30, eps=31, epsaed=32)
# Balance sheet
BS = dict(ppe=5, rou=6, intang=7, gw=8, invprop=9, jv=10, inv=11, recv=12, cash=13,
          ta=14, pay=15, nwc=16, grossd=17, nd=18, hyb=19, nci=20, eqp=21, teq=22,
          ndeb=23, bvps=24, bvpsaed=25, ic=26, roic=27, roe=28,
          ppeb=30, ppeopen=31, ppecapex=32, ppedeprate=33, ppedep1=34, ppedep=35,
          ppeclose=36, otherdna=37, dnatot=38,
          wcb=40, wcrev=41, wcopcost=42, wcdso=43, wcdio=44, wcdpo=45, wcrecv=46,
          wcinv=47, wcpay=48, wcnwc=49, wcdnwc=50,
          ndb=52, ndopen=53, ndgross=54, ndint=55, ndfcff=56, ndintat=57, ndfi=58,
          ndcpn=59, ndfcfe=60, nddps=61, ndclose=62,
          eqb=64, eqopen=65, eqnpa=66, eqdps=67, eqcpn=68, eqclose=69, dpsps=70)
# Cash flow
CF = dict(ebitda=5, ocf=6, capex=7, fcf=8, wfb=10, nopat=11, dna=12, cap=13, dnwc=14,
          fcff=15, intat=16, fi=17, cpn=18, fcfe=19, dps=20, ndmove=21, conv=22)
# Relative & Normalized
RN = dict(hdr=4, eb26=5, blend=6, ev=7, jv=8, nd=9, defd=10, hyb=11, nci=12, eq=13,
          vev=14, pe=15, ord26=16, vpe=17, w=18, base=19, bear=20,
          ownb=22, spotusd=23, mktcap=24, netdebt=25, evnow=26, eveb_ttm=27,
          eveb_26=28, pe_ttm=29, pb=30, dy=31,
          nhdr=33, neb=34, nev=35, neq=36, nvev=37, nord=38, neps=39, nvpe=40,
          nbase=41, nbear=42,
          bhdr=44, beqp=45, bbvps=46, bbvpsaed=47, broe=48, bke=49, bg=50, bpb=51,
          bbase=52, bbear=53,
          vsb=55, vsbook=56, vsprice=57, vsratio=58, vsgain=59, vsnote=60)
# SOTP bridge
SB = dict(hdr=4, pvex=5, pvtv=6, evops=7, tvshare=8, jv=9, ev=10, nd=11, defd=12,
          hyb=13, nci=14, eq=15, fvusd=16, fvaed=17,
          legb=19, leg0=20, legt=23, mb=25, mcon=26, mspot=27, mw=28, mship=29,
          bb=31, bevops=32, bjv=33, bev=34, bnd=35, bdefd=36, bhyb=37, bnci=38,
          beq=39, bfv=40)
# Summary
SU = dict(hdr=4, dcf=5, rel=6, norm=7, book=8, central=9, cb=11, dcfa=12, centrala=13,
          panel=15, spot=16, keyhdr=18, key0=19)
# Fundamental valuation
FV = dict(hdr=4, dcf=5, dcfbear=6, dcfbull=7, rel=8, norm=9, book=10, central=12,
          cb=14, beta=15, ke=16, wacc=17, fv=18, cen=19, betaa=20, kea=21, wacca=22,
          fva=23, cena=24, note=25, eb=27, ehdr=28, e0=29, epanel=32)
# Per-share & ratios
PS = dict(eps=5, epsaed=6, ordps=7, bvps=8, fcffps=9, dpsps=10, payout=11, gm=12,
          ebm=13, ebitm=14, netm=15, roe=16, roic=17, ndeb=18, cover=19, dso=20,
          dio=21, dpo=22, cycle=23, capexrev=24,
          ab=26, aprice=27, apriceusd=28, amkt=29, aev=30, aeveb=31, aeveb26=32,
          ape=33, apb=34, ady=35)
# Peer & sector
PR = dict(hdr=4, p0=5, mb=9, mcon=10, mspot=11, mw=12, mev=13, pecon=14, pespot=15,
          pe=16, ob=18, o0=19)
# Monte Carlo
MC = dict(hdr=4, h0=5, lhdr=8, l0=9, ehdr=14, e0=15)
# Sensitivity
SE = dict(bgb=4, bghdr=5, bg0=6, ab=12, ahdr=13, a0=14, aswing=15, cb=17, chdr=18,
          c0=19, cswing=20, tb=22, thdr=23, t0=24, tnote=25,
          mb=27, m1y=28, mspot=29, mhdr=30, mpath=31, mvs=32, mob=33, mnote=34)

SEGREF = {s: i for i, s in enumerate(SEGS)}
UNITS = [s for s in SEGS if s not in ('Tankers', 'Gas Carriers')]

# ============ 5 SOTP BRIDGE ====================================================
ws = sheet('SOTP Bridge')
title(ws, 'Enterprise value to equity — the bridge, and the sum-of-the-parts cross-check',
      'USD thousand unless stated. Per-share figures in dirhams at the fixed parity.', 6,
      awidth=58, cwidth=17)
hdr(ws, SB['hdr'], ['Step', '', 'USD 000', 'AED per share'])
_bridge = [
    (SB['pvex'], 'Present value of the five forecast years', f"=DCF!$C${DF_['pvex']}",
     DC['pv_expl'], True),
    (SB['pvtv'], 'Present value of the terminal value', f"=DCF!$C${DF_['pvtv']}",
     DC['pv_tv'], True),
    (SB['evops'], 'Enterprise value of operations', f"=C{SB['pvex']}+C{SB['pvtv']}",
     DC['ev_ops'], False),
    (SB['jv'], 'Plus joint ventures and associates at carrying value', f"={a('jv')}",
     JV_BV, True),
    (SB['ev'], 'Enterprise value', f"=C{SB['evops']}+C{SB['jv']}", DC['ev'], False),
    (SB['nd'], 'Less net debt at 31 March 2026', f"=-{a('nd_co')}", -NDCO, True),
    (SB['defd'], 'Less deferred consideration on acquisitions', f"=-{a('deferred')}",
     -DEFERRED, True),
    (SB['hyb'], 'Less perpetual capital securities at carrying value', f"=-{a('hybrid')}",
     -HYBRID, True),
    (SB['nci'], 'Less non-controlling interests at carrying value', f"=-{a('nci_bv')}",
     -NCI_BV, True),
    (SB['eq'], 'Equity attributable to ordinary shareholders',
     f"=C{SB['ev']}+C{SB['nd']}+C{SB['defd']}+C{SB['hyb']}+C{SB['nci']}", DC['equity'],
     False)]
for rw, lab, fml, xp, gr in _bridge:
    put(ws, f'A{rw}', lab, fmt=None)
    bd = rw in (SB['evops'], SB['ev'], SB['eq'])
    putf(ws, f'C{rw}', fml, xp, NUM0, bold=bd, green=gr)
    putf(ws, f'D{rw}', f"=C{rw}/{a('shares')}/1000*{a('fx')}", xp / SH / 1000.0 * PEG, PX,
         bold=bd)
band(ws, SB['evops'], 4); band(ws, SB['ev'], 4); band(ws, SB['eq'], 4)
put(ws, f"A{SB['tvshare']}", 'Terminal value as a share of enterprise value', fmt=None)
putf(ws, f"C{SB['tvshare']}", f"=C{SB['pvtv']}/C{SB['evops']}", DC['tv_share'], PCT)
put(ws, f"A{SB['fvusd']}", 'Fair value per share (USD)', fmt=None)
putf(ws, f"C{SB['fvusd']}", f"=C{SB['eq']}/{a('shares')}/1000", DC['fv_usd'], PX)
put(ws, f"A{SB['fvaed']}", 'Fair value per share (AED)', bold=True, fmt=None)
putf(ws, f"C{SB['fvaed']}", f"=C{SB['fvusd']}*{a('fx')}", DC['fv_aed'], PX, bold=True)
band(ws, SB['fvaed'], 4)

band(ws, SB['legb'], 6)
put(ws, f"A{SB['legb']}", 'THE SUM-OF-THE-PARTS CROSS-CHECK — EACH LEG ON ITS OWN MULTIPLE',
    bold=True, fmt=None)
hdr(ws, SB['legb'] + 0, ['', '2026E EBITDA', 'Multiple', 'Enterprise value', 'Basis'],
    start=2)
_legmult = {'Integrated Logistics': f"C{SB['mcon']}", 'Shipping': f"C{SB['mship']}",
            'Services': f"C{SB['mcon']}"}
_basis = {l['leg']: l['basis'] for l in SOTP['legs']}
for j, g in enumerate(GROUPS):
    rw = SB['leg0'] + j
    put(ws, f'A{rw}', g, fmt=None)
    putf(ws, f'B{rw}', f"=Segments!B{SG['geb0']+j}", GRP_EB_F[g][0], NUM0, green=True)
    putf(ws, f'C{rw}', f"={_legmult[g]}", SOTP_MULT[g], MULT)
    putf(ws, f'D{rw}', f'=B{rw}*C{rw}', SOTP_EV[g], NUM0)
    put(ws, f'E{rw}', _basis[g], fmt=None, wrap=True)
    ws.row_dimensions[rw].height = 28
band(ws, SB['legt'], 6)
put(ws, f"A{SB['legt']}", 'Enterprise value of the operating legs', bold=True, fmt=None)
putf(ws, f"D{SB['legt']}", f"=SUM(D{SB['leg0']}:D{SB['leg0']+2})", SOTP_EVOPS, NUM0,
     bold=True)
ws.column_dimensions['E'].width = 52

band(ws, SB['mb'], 6)
put(ws, f"A{SB['mb']}", 'THE SHIPPING MULTIPLE, BUILT — NOT PASTED', bold=True, fmt=None)
for rw, lab, fml, xp, fmt in [
        (SB['mcon'], 'Contracted-fleet multiple (long-term contracted gas shipping peer)',
         f"='Peer & Sector'!$C${PR['mcon']}", MULT_CONTR, MULT),
        (SB['mspot'], 'Spot-tanker multiple (average of the two spot-tanker peers)',
         f"='Peer & Sector'!$C${PR['mspot']}", MULT_SPOT, MULT),
        (SB['mw'], "Share of 2026 earnings exposed to spot rates, as disclosed",
         f"={a('spot_w')}", SPOT_W, PCT),
        (SB['mship'], 'Shipping multiple — the two weighted by that share',
         f"=(1-C{SB['mw']})*C{SB['mcon']}+C{SB['mw']}*C{SB['mspot']}", BLEND_EV, MULT)]:
    put(ws, f'A{rw}', lab, fmt=None)
    putf(ws, f'C{rw}', fml, xp, fmt, green=fml.startswith(("='P", '=Assumptions')))

band(ws, SB['bb'], 6)
put(ws, f"A{SB['bb']}", 'THE SUM-OF-THE-PARTS BRIDGE TO EQUITY', bold=True, fmt=None)
_sb = [(SB['bevops'], 'Enterprise value of the operating legs', f"=D{SB['legt']}",
        SOTP_EVOPS, False),
       (SB['bjv'], 'Plus joint ventures and associates at carrying value', f"={a('jv')}",
        JV_BV, True),
       (SB['bev'], 'Enterprise value', f"=C{SB['bevops']}+C{SB['bjv']}",
        SOTP_EVOPS + JV_BV, False),
       (SB['bnd'], 'Less net debt at 31 March 2026', f"=-{a('nd_co')}", -NDCO, True),
       (SB['bdefd'], 'Less deferred consideration on acquisitions', f"=-{a('deferred')}",
        -DEFERRED, True),
       (SB['bhyb'], 'Less perpetual capital securities at carrying value',
        f"=-{a('hybrid')}", -HYBRID, True),
       (SB['bnci'], 'Less non-controlling interests at carrying value', f"=-{a('nci_bv')}",
        -NCI_BV, True),
       (SB['beq'], 'Equity attributable to ordinary shareholders',
        f"=C{SB['bev']}+C{SB['bnd']}+C{SB['bdefd']}+C{SB['bhyb']}+C{SB['bnci']}",
        SOTP_EQ, False)]
for rw, lab, fml, xp, gr in _sb:
    put(ws, f'A{rw}', lab, fmt=None)
    putf(ws, f'C{rw}', fml, xp, NUM0, bold=(rw in (SB['bev'], SB['beq'])), green=gr)
band(ws, SB['beq'], 6)
put(ws, f"A{SB['bfv']}", 'Sum-of-the-parts fair value per share (AED)', bold=True, fmt=None)
putf(ws, f"C{SB['bfv']}", f"=C{SB['beq']}/{a('shares')}/1000*{a('fx')}", SOTP_FV, PX,
     bold=True)
band(ws, SB['bfv'], 6)
note(ws, f"A{SB['bfv']+2}", 'The sum-of-the-parts is a cross-check on the discounted cash '
     'flow, not a fifth lens: it prices each business unit\'s 2026 earnings on the multiple '
     'the market is paying for that kind of earnings stream, and the Shipping leg is the '
     'only one that carries spot exposure, which is why its multiple is a weighted blend '
     'rather than a single peer figure.')

# ============ 6 SEGMENTS =======================================================
ws = sheet('Segments')
title(ws, 'Segments — the disclosed record and the unit build', 'USD thousand unless stated. '
      'The tanker fleet is built vessel by vessel; every forecast figure below is a formula.',
      9, awidth=52, cwidth=14)
hdr(ws, SG['revh'], ['Segment revenue — as disclosed (USD 000)'] + YH)
for j, s in enumerate(SEGS):
    put(ws, f"A{SG['revh0']+j}", s, fmt=None)
    for i in range(3):
        put(ws, f"{HC[i]}{SG['revh0']+j}", SEGH[s]['revenue'][i], BLUE, NUM0)
band(ws, SG['revht'], 4)
put(ws, f"A{SG['revht']}", 'Total revenue', bold=True, fmt=None)
for i in range(3):
    putf(ws, f"{HC[i]}{SG['revht']}",
         f"=SUM({HC[i]}{SG['revh0']}:{HC[i]}{SG['revh0']+6})", HI['revenue'][i], NUM0,
         bold=True)
hdr(ws, SG['ebh'], ['Segment EBITDA — as disclosed (USD 000)'] + YH)
for j, s in enumerate(SEGS):
    put(ws, f"A{SG['ebh0']+j}", s, fmt=None)
    for i in range(3):
        put(ws, f"{HC[i]}{SG['ebh0']+j}", SEGH[s]['ebitda'][i], BLUE, NUM0)
band(ws, SG['ebht'], 4)
put(ws, f"A{SG['ebht']}", 'Total segment EBITDA', bold=True, fmt=None)
_segeb_tot = [sum(SEGH[s]['ebitda'][i] for s in SEGS) for i in range(3)]
for i in range(3):
    putf(ws, f"{HC[i]}{SG['ebht']}", f"=SUM({HC[i]}{SG['ebh0']}:{HC[i]}{SG['ebh0']+6})",
         _segeb_tot[i], NUM0, bold=True)
put(ws, f"A{SG['mgnh']}", 'Segment EBITDA margin', fmt=None)
for i in range(3):
    putf(ws, f"{HC[i]}{SG['mgnh']}", f"={HC[i]}{SG['ebht']}/{HC[i]}{SG['revht']}",
         _segeb_tot[i] / HI['revenue'][i], PCT)

band(ws, SG['tband'], 9)
put(ws, f"A{SG['tband']}", 'TANKERS — THE UNIT BUILD, VESSEL BY VESSEL', bold=True, fmt=None)
for i, c in enumerate(CLS_NAME):
    cc = ws.cell(row=SG['tband'], column=2 + i, value=c)
    cc.font = Font(bold=True); cc.fill = FILL_G
_tnkrows = [(SG['own'], 'Vessels owned', 'tnk_own', [OWNED[c] for c in CLS], NUM0),
            (SG['spotn'], 'Vessels trading at spot rates', 'tnk_spot',
             [SPOTN[c] for c in CLS], NUM0),
            (SG['tcout'], 'Fixed charter-out rate (USD per day)', 'tnk_tcout',
             [TCOUT[c] for c in CLS], NUM0),
            (SG['tce25'], '2025 average time-charter equivalent (USD per day)', 'tnk_tce25',
             [TCE25[c] for c in CLS], NUM0),
            (SG['q1'], 'First-quarter 2026 time-charter equivalent (USD per day)', 'tnk_q1',
             [Q1R[c] for c in CLS], NUM0),
            (SG['q2'], 'Second-quarter 2026 time-charter equivalent (USD per day)', 'tnk_q2',
             [Q2R[c] for c in CLS], NUM0),
            (SG['mid'], 'Mid-cycle rate anchor (USD per day)', 'tnk_mid',
             [TCEMID[c] for c in CLS], NUM0)]
for rw, lab, key, vals, fmt in _tnkrows:
    put(ws, f'A{rw}', lab, fmt=None)
    for j in range(5):
        putf(ws, f'{CD[j]}{rw}', f"={a(key, col=CD[j])}", vals[j], fmt, green=True)
put(ws, f"A{SG['fix']}", 'Vessels on charters out at fixed rates', fmt=None)
for j, c in enumerate(CLS):
    putf(ws, f"{CD[j]}{SG['fix']}", f"={CD[j]}{SG['own']}-{CD[j]}{SG['spotn']}", FIXN[c],
         NUM0)
put(ws, f"A{SG['h2']}", 'Second-half 2026 time-charter equivalent — the first quarter '
    'stepped back toward the 2025 average (USD per day)', fmt=None)
for j, c in enumerate(CLS):
    putf(ws, f"{CD[j]}{SG['h2']}",
         f"={CD[j]}{SG['q1']}*(1-{a('h2w')})+{CD[j]}{SG['tce25']}*{a('h2w')}", TNK_H2[c],
         NUM0)
put(ws, f"A{SG['y26']}", 'FY2026 spot time-charter equivalent — the four quarters averaged '
    '(USD per day)', fmt=None)
for j, c in enumerate(CLS):
    putf(ws, f"{CD[j]}{SG['y26']}",
         f"=({CD[j]}{SG['q1']}+{CD[j]}{SG['q2']}+2*{CD[j]}{SG['h2']})/4", TNK_Y26[c], NUM0)

band(ws, SG['pathb'], 6)
put(ws, f"A{SG['pathb']}", 'Spot time-charter equivalent by class, gliding to the mid-cycle '
    'anchor (USD per day)', bold=True, fmt=None)
for i, y in enumerate(YF):
    cc = ws.cell(row=SG['pathb'], column=2 + i, value=y)
    cc.font = Font(bold=True); cc.fill = FILL_G
for j, c in enumerate(CLS):
    rw = SG['path0'] + j
    put(ws, f'A{rw}', CLS_NAME[j], fmt=None)
    for i in range(5):
        f_ = (f"=${CD[j]}${SG['y26']}" if i == 0 else
              f"=${CD[j]}${SG['y26']}+(${CD[j]}${SG['mid']}-${CD[j]}${SG['y26']})*{i}/4")
        putf(ws, f'{CD[i]}{rw}', f_, TNK_PATH[c][i], NUM0)

band(ws, SG['buildb'], 6)
put(ws, f"A{SG['buildb']}", 'Tanker revenue and running cost (USD 000)', bold=True, fmt=None)
for i, y in enumerate(YF):
    cc = ws.cell(row=SG['buildb'], column=2 + i, value=y)
    cc.font = Font(bold=True); cc.fill = FILL_G
put(ws, f"A{SG['spotrev']}", 'Spot fleet — vessels x rate per day x 365', fmt=None)
for i in range(5):
    f_ = '=(' + '+'.join(f"${CD[j]}${SG['spotn']}*{CD[i]}{SG['path0']+j}"
                         for j in range(5)) + ')*365/1000'
    putf(ws, f"{CD[i]}{SG['spotrev']}", f_, TNK_SPOTREV[i], NUM0)
put(ws, f"A{SG['fixrev']}", 'Chartered-out fleet — vessels at their fixed rates while the '
    'contracts run, at spot thereafter', fmt=None)
for i in range(5):
    roll = a('roll', col=CD[i])
    f_ = '=(' + '+'.join(
        f"${CD[j]}${SG['fix']}*(${CD[j]}${SG['tcout']}*{roll}"
        f"+{CD[i]}{SG['path0']+j}*(1-{roll}))" for j in range(5)) + ')*365/1000'
    putf(ws, f"{CD[i]}{SG['fixrev']}", f_, TNK_FIXREV[i], NUM0)
put(ws, f"A{SG['tcerev']}", 'Time-charter-equivalent revenue', bold=True, fmt=None)
for i in range(5):
    putf(ws, f"{CD[i]}{SG['tcerev']}",
         f"={CD[i]}{SG['spotrev']}+{CD[i]}{SG['fixrev']}", TNK_TCEREV[i], NUM0, bold=True)
put(ws, f"A{SG['vdays']}", 'Vessel-days a year (owned fleet x 365)', fmt=None)
putf(ws, f"B{SG['vdays']}", f"=SUM(B{SG['own']}:F{SG['own']})*365", VDAYS, NUM0)
put(ws, f"A{SG['opexd']}", 'Running cost per vessel-day, escalated (USD)', fmt=None)
for i in range(5):
    putf(ws, f"{CD[i]}{SG['opexd']}", f"={a('opex_day')}*(1+{a('opex_esc')})^{i+1}",
         TNK_OPEXD[i], NUM1)
put(ws, f"A{SG['opex']}", 'Total running cost — cost per day x vessel-days', fmt=None)
for i in range(5):
    putf(ws, f"{CD[i]}{SG['opex']}", f"=$B${SG['vdays']}*{CD[i]}{SG['opexd']}/1000",
         TNK_OPEX[i], NUM0)
put(ws, f"A{SG['teb']}", 'Tankers EBITDA', bold=True, fmt=None)
for i in range(5):
    putf(ws, f"{CD[i]}{SG['teb']}", f"={CD[i]}{SG['tcerev']}-{CD[i]}{SG['opex']}",
         TNK_EBITDA[i], NUM0, bold=True)
put(ws, f"A{SG['gross']}", 'Gross-up from time-charter-equivalent to reported revenue',
    fmt=None)
for i in range(5):
    putf(ws, f"{CD[i]}{SG['gross']}", f"={a('grossup')}", GROSSUP, '0.00', green=True)
put(ws, f"A{SG['trev']}", 'Tankers revenue', bold=True, fmt=None)
for i in range(5):
    putf(ws, f"{CD[i]}{SG['trev']}", f"={CD[i]}{SG['tcerev']}*{CD[i]}{SG['gross']}",
         TNK_REV[i], NUM0, bold=True)

band(ws, SG['gasb'], 6)
put(ws, f"A{SG['gasb']}", 'GAS CARRIERS — CONTRACTED VESSEL-YEARS x IMPLIED DAY RATE',
    bold=True, fmt=None)
for i, y in enumerate(YF):
    cc = ws.cell(row=SG['gasb'], column=2 + i, value=y)
    cc.font = Font(bold=True); cc.fill = FILL_G
put(ws, f"A{SG['gasvy']}", 'Contracted vessel-years', fmt=None)
for i in range(5):
    putf(ws, f"{CD[i]}{SG['gasvy']}", f"={a('gas_vy', col=CD[i])}", GAS_VY[i], NUM1,
         green=True)
put(ws, f"A{SG['gasrate']}", 'Revenue per vessel-day, escalated (USD)', fmt=None)
for i in range(5):
    putf(ws, f"{CD[i]}{SG['gasrate']}", f"={a('gas_rate')}*(1+{a('opex_esc')})^{i+1}",
         GAS_RATED[i], NUM0)
put(ws, f"A{SG['gasrev']}", 'Gas Carriers revenue', fmt=None)
for i in range(5):
    putf(ws, f"{CD[i]}{SG['gasrev']}",
         f"={CD[i]}{SG['gasvy']}*365*{CD[i]}{SG['gasrate']}/1000", GAS_REV[i], NUM0)
put(ws, f"A{SG['gasmgn']}", 'Gas Carriers earnings margin', fmt=None)
for i in range(5):
    putf(ws, f"{CD[i]}{SG['gasmgn']}", f"={a('gas_mgn')}", GAS_MGN, PCT, green=True)
put(ws, f"A{SG['gaseb']}", 'Gas Carriers EBITDA', bold=True, fmt=None)
for i in range(5):
    putf(ws, f"{CD[i]}{SG['gaseb']}", f"={CD[i]}{SG['gasrev']}*{CD[i]}{SG['gasmgn']}",
         GAS_EBITDA[i], NUM0, bold=True)

band(ws, SG['unitb'], 6)
put(ws, f"A{SG['unitb']}", 'THE REMAINING FIVE UNITS — REVENUE DRIVER x MARGIN DRIVER',
    bold=True, fmt=None)
for i, y in enumerate(YF):
    cc = ws.cell(row=SG['unitb'], column=2 + i, value=y)
    cc.font = Font(bold=True); cc.fill = FILL_G
UNIT_ROW = {}
for j, s in enumerate(UNITS):
    k = s.lower().replace(' ', '_').replace('-', '_')
    rr = SG['unit0'] + 2 * j
    UNIT_ROW[s] = rr
    put(ws, f'A{rr}', f'{s} — revenue', fmt=None)
    put(ws, f'A{rr+1}', f'{s} — EBITDA', fmt=None)
    for i in range(5):
        putf(ws, f'{CD[i]}{rr}', f"={a('rev_'+k, col=CD[i])}", DRV[s]['rev'][i], NUM0,
             green=True)
        putf(ws, f'{CD[i]}{rr+1}', f"={CD[i]}{rr}*{a('mar_'+k, col=CD[i])}",
             SEG_EB_F[s][i], NUM0)

_SEG_REV_SRC = {'Tankers': SG['trev'], 'Gas Carriers': SG['gasrev']}
_SEG_EB_SRC = {'Tankers': SG['teb'], 'Gas Carriers': SG['gaseb']}
for s in UNITS:
    _SEG_REV_SRC[s] = UNIT_ROW[s]; _SEG_EB_SRC[s] = UNIT_ROW[s] + 1
band(ws, SG['frevb'], 6)
put(ws, f"A{SG['frevb']}", 'FORECAST REVENUE BY SEGMENT', bold=True, fmt=None)
for i, y in enumerate(YFE):
    cc = ws.cell(row=SG['frevb'], column=2 + i, value=y)
    cc.font = Font(bold=True); cc.fill = FILL_G
for j, s in enumerate(SEGS):
    put(ws, f"A{SG['frev0']+j}", s, fmt=None)
    for i in range(5):
        putf(ws, f"{CD[i]}{SG['frev0']+j}", f"={CD[i]}{_SEG_REV_SRC[s]}", SEG_REV_F[s][i],
             NUM0)
band(ws, SG['frevt'], 6)
put(ws, f"A{SG['frevt']}", 'Total revenue', bold=True, fmt=None)
for i in range(5):
    putf(ws, f"{CD[i]}{SG['frevt']}",
         f"=SUM({CD[i]}{SG['frev0']}:{CD[i]}{SG['frev0']+6})", REV_F[i], NUM0, bold=True)
band(ws, SG['febb'], 6)
put(ws, f"A{SG['febb']}", 'FORECAST EBITDA BY SEGMENT', bold=True, fmt=None)
for i, y in enumerate(YFE):
    cc = ws.cell(row=SG['febb'], column=2 + i, value=y)
    cc.font = Font(bold=True); cc.fill = FILL_G
for j, s in enumerate(SEGS):
    put(ws, f"A{SG['feb0']+j}", s, fmt=None)
    for i in range(5):
        putf(ws, f"{CD[i]}{SG['feb0']+j}", f"={CD[i]}{_SEG_EB_SRC[s]}", SEG_EB_F[s][i],
             NUM0)
band(ws, SG['febt'], 6)
put(ws, f"A{SG['febt']}", 'Total EBITDA', bold=True, fmt=None)
for i in range(5):
    putf(ws, f"{CD[i]}{SG['febt']}", f"=SUM({CD[i]}{SG['feb0']}:{CD[i]}{SG['feb0']+6})",
         EB_F[i], NUM0, bold=True)
put(ws, f"A{SG['fmgn']}", 'Group EBITDA margin', fmt=None)
for i in range(5):
    putf(ws, f"{CD[i]}{SG['fmgn']}", f"={CD[i]}{SG['febt']}/{CD[i]}{SG['frevt']}",
         EB_F[i] / REV_F[i], PCT)
band(ws, SG['grpb'], 6)
put(ws, f"A{SG['grpb']}", 'FORECAST BY BUSINESS UNIT', bold=True, fmt=None)
for i, y in enumerate(YFE):
    cc = ws.cell(row=SG['grpb'], column=2 + i, value=y)
    cc.font = Font(bold=True); cc.fill = FILL_G
for j, g in enumerate(GROUPS):
    mem = [SEGS.index(s) for s in SEGS if SEG_GROUP[s] == g]
    put(ws, f"A{SG['grev0']+j}", f'{g} — revenue', fmt=None)
    put(ws, f"A{SG['geb0']+j}", f'{g} — EBITDA', fmt=None)
    put(ws, f"A{SG['gmgn0']+j}", f'{g} — EBITDA margin', fmt=None)
    for i in range(5):
        putf(ws, f"{CD[i]}{SG['grev0']+j}",
             '=' + '+'.join(f"{CD[i]}{SG['frev0']+m}" for m in mem), GRP_REV_F[g][i], NUM0)
        putf(ws, f"{CD[i]}{SG['geb0']+j}",
             '=' + '+'.join(f"{CD[i]}{SG['feb0']+m}" for m in mem), GRP_EB_F[g][i], NUM0)
        putf(ws, f"{CD[i]}{SG['gmgn0']+j}",
             f"={CD[i]}{SG['geb0']+j}/{CD[i]}{SG['grev0']+j}",
             GRP_EB_F[g][i] / GRP_REV_F[g][i], PCT)
note(ws, f"A{SG['gmgn0']+4}", 'The tanker gross-up moves reported revenue only, never '
     'earnings: earnings are struck on time-charter-equivalent revenue less the running '
     'cost of the same vessels, so the presentation of voyage and relet revenue cannot '
     'change the valuation.')

# ============ 7 RELATIVE & NORMALIZED ==========================================
ws = sheet('Relative & Normalized')
title(ws, 'Relative multiples, normalised earnings power and the book lens', 'USD thousand '
      'unless stated. Per-share figures in dirhams.', 5, awidth=62, cwidth=17)
hdr(ws, RN['hdr'], ['Relative lens', '', 'Value'])
_rel = [
    (RN['eb26'], 'FY2026E group EBITDA', f"=DCF!B{DF_['ebitda']}", EB_F[0], NUM0, True),
    (RN['blend'], 'Blended enterprise multiple',
     f"='Peer & Sector'!$C${PR['mev']}", BLEND_EV, MULT, True),
    (RN['ev'], 'Implied enterprise value', f"=C{RN['eb26']}*C{RN['blend']}", REL_EV, NUM0,
     False),
    (RN['jv'], 'Plus joint ventures and associates at carrying value', f"={a('jv')}", JV_BV,
     NUM0, True),
    (RN['nd'], 'Less net debt at 31 March 2026', f"=-{a('nd_co')}", -NDCO, NUM0, True),
    (RN['defd'], 'Less deferred consideration on acquisitions', f"=-{a('deferred')}",
     -DEFERRED, NUM0, True),
    (RN['hyb'], 'Less perpetual capital securities at carrying value', f"=-{a('hybrid')}",
     -HYBRID, NUM0, True),
    (RN['nci'], 'Less non-controlling interests at carrying value', f"=-{a('nci_bv')}",
     -NCI_BV, NUM0, True),
    (RN['eq'], 'Implied equity attributable to ordinary shareholders',
     f"=C{RN['ev']}+C{RN['jv']}+C{RN['nd']}+C{RN['defd']}+C{RN['hyb']}+C{RN['nci']}",
     eq_from_ev(REL_EV), NUM0, False),
    (RN['vev'], 'Value per share on the enterprise multiple (AED)',
     f"=C{RN['eq']}/{a('shares')}/1000*{a('fx')}", REL_V_EV, PX, False),
    (RN['pe'], 'Blended price/earnings', f"='Peer & Sector'!$C${PR['pe']}", BLEND_PE, MULT,
     True),
    (RN['ord26'], 'FY2026E earnings attributable to ordinary shareholders',
     f"='Income Statement'!E{IS['ordn']}", ORD_F[0], NUM0, True),
    (RN['vpe'], 'Value per share on the earnings multiple (AED)',
     f"=C{RN['ord26']}*C{RN['pe']}/{a('shares')}/1000*{a('fx')}", REL_V_PE, PX, False),
    (RN['w'], 'Weight on the enterprise multiple', f"={a('w_eveb')}", W_EVEB, PCT, True)]
for rw, lab, fml, xp, fmt, gr in _rel:
    put(ws, f'A{rw}', lab, fmt=None)
    putf(ws, f'C{rw}', fml, xp, fmt, green=gr)
band(ws, RN['base'], 5)
put(ws, f"A{RN['base']}", 'RELATIVE LENS — value per share (AED)', bold=True, fmt=None)
putf(ws, f"C{RN['base']}",
     f"=C{RN['w']}*C{RN['vev']}+(1-C{RN['w']})*C{RN['vpe']}", REL_BASE, PX, bold=True)
put(ws, f"A{RN['bear']}", 'Bear on the spot multiple (C) / bull on the contracted multiple '
    '(D), same construction', fmt=None)
_relbridge = (f"+{a('jv')}-{a('nd_co')}-{a('deferred')}-{a('hybrid')}-{a('nci_bv')})"
              f"/{a('shares')}/1000*{a('fx')}")
putf(ws, f"C{RN['bear']}",
     f"=(C{RN['eb26']}*'Peer & Sector'!$C${PR['mspot']}" + _relbridge, REL_BEAR, PX)
putf(ws, f"D{RN['bear']}",
     f"=(C{RN['eb26']}*'Peer & Sector'!$C${PR['mcon']}" + _relbridge, REL_BULL, PX)

band(ws, RN['ownb'], 5)
put(ws, f"A{RN['ownb']}", "THE COMPANY'S OWN MULTIPLES AT THE ANCHOR PRICE", bold=True,
    fmt=None)
for rw, lab, fml, xp, fmt, gr in [
        (RN['spotusd'], 'Share price (USD)', f"={a('spot')}/{a('fx')}", SPOT / PEG, PX,
         True),
        (RN['mktcap'], 'Market capitalisation (USD 000)',
         f"=C{RN['spotusd']}*{a('shares')}*1000", MKTCAP, NUM0, False),
        (RN['netdebt'], 'Net debt including deferred consideration (USD 000)',
         f"={a('nd_co')}+{a('deferred')}", NETDEBT, NUM0, True),
        (RN['evnow'], 'Enterprise value (USD 000)',
         f"=C{RN['mktcap']}+C{RN['netdebt']}", EV_NOW, NUM0, False),
        (RN['eveb_ttm'], 'Enterprise value / 2025 reported EBITDA',
         f"=C{RN['evnow']}/'Income Statement'!D{IS['ebrep']}", OWN_EVEB_TTM, MULT, True),
        (RN['eveb_26'], 'Enterprise value / FY2026E EBITDA',
         f"=C{RN['evnow']}/C{RN['eb26']}", OWN_EVEB_26, MULT, False),
        (RN['pe_ttm'], 'Price / 2025 earnings attributable to ordinary shareholders',
         f"=C{RN['mktcap']}/'Income Statement'!D{IS['ordn']}", OWN_PE_TTM, MULT, True),
        (RN['pb'], 'Price / book at 31 March 2026',
         f"=C{RN['mktcap']}/({a('eqp0')}+{a('hybrid')})", OWN_PB, MULT, False),
        (RN['dy'], 'Dividend yield on the 2026 distribution',
         f"={a('dps26')}/C{RN['mktcap']}", OWN_DY, PCT, True)]:
    put(ws, f'A{rw}', lab, fmt=None)
    putf(ws, f'C{rw}', fml, xp, fmt, green=gr)
hdr(ws, RN['nhdr'], ['Normalised earnings lens — the five-year average of the model\'s own '
                     'forecast', '', 'Value'])
for rw, lab, fml, xp, fmt, gr in [
        (RN['neb'], 'Mid-cycle EBITDA — five-year average',
         f"=AVERAGE(DCF!B{DF_['ebitda']}:F{DF_['ebitda']})", NORM_EB, NUM0, True),
        (RN['nev'], 'Implied enterprise value', f"=C{RN['neb']}*C{RN['blend']}",
         BLEND_EV * NORM_EB, NUM0, False),
        (RN['neq'], 'Implied equity attributable to ordinary shareholders',
         f"=C{RN['nev']}+{a('jv')}-{a('nd_co')}-{a('deferred')}-{a('hybrid')}"
         f"-{a('nci_bv')}", eq_from_ev(BLEND_EV * NORM_EB), NUM0, False),
        (RN['nvev'], 'Value per share on the enterprise multiple (AED)',
         f"=C{RN['neq']}/{a('shares')}/1000*{a('fx')}", NORM_V_EV, PX, False),
        (RN['nord'], 'Mid-cycle earnings attributable to ordinary shareholders — five-year '
         'average', f"=AVERAGE('Income Statement'!E{IS['ordn']}:I{IS['ordn']})", NORM_ORD,
         NUM0, True),
        (RN['neps'], 'Mid-cycle earnings per share (USD)',
         f"=C{RN['nord']}/{a('shares')}/1000", NORM_EPS, PX3, False),
        (RN['nvpe'], 'Value per share on the earnings multiple (AED)',
         f"=C{RN['neps']}*C{RN['pe']}*{a('fx')}", NORM_V_PE, PX, False)]:
    put(ws, f'A{rw}', lab, fmt=None)
    putf(ws, f'C{rw}', fml, xp, fmt, green=gr)
band(ws, RN['nbase'], 5)
put(ws, f"A{RN['nbase']}", 'NORMALISED LENS — value per share (AED)', bold=True, fmt=None)
putf(ws, f"C{RN['nbase']}", f"=(C{RN['nvev']}+C{RN['nvpe']})/2", NORM_BASE, PX, bold=True)
put(ws, f"A{RN['nbear']}", 'Bear on the spot multiple (C) / bull on the contracted multiple '
    '(D), same construction', fmt=None)
putf(ws, f"C{RN['nbear']}",
     f"=(C{RN['neb']}*'Peer & Sector'!$C${PR['mspot']}" + _relbridge, NORM_BEAR, PX)
putf(ws, f"D{RN['nbear']}",
     f"=(C{RN['neb']}*'Peer & Sector'!$C${PR['mcon']}" + _relbridge, NORM_BULL, PX)

hdr(ws, RN['bhdr'], ['Book value and sustainable return', '', 'Value'])
for rw, lab, fml, xp, fmt, gr in [
        (RN['beqp'], 'Equity attributable to shareholders at 31 March 2026 (USD 000)',
         f"={a('eqp0')}", EQP0, NUM0, True),
        (RN['bbvps'], 'Book value per share (USD)',
         f"=C{RN['beqp']}/{a('shares')}/1000", BVPS0, PX3, False),
        (RN['bbvpsaed'], 'Book value per share (AED)', f"=C{RN['bbvps']}*{a('fx')}",
         BVPS0 * PEG, PX, False),
        (RN['broe'], 'Sustainable return on equity — five-year forecast average',
         f"=AVERAGE('Balance Sheet'!E{BS['roe']}:I{BS['roe']})", ROE_SUST, PCT, True),
        (RN['bke'], 'Cost of equity', f"=DCF!$C${DF_['ke']}", KE, PCT2, True),
        (RN['bg'], 'Terminal growth', f"={a('g_term')}", G, PCT, True),
        (RN['bpb'], 'Justified price / book',
         f"=(C{RN['broe']}-C{RN['bg']})/(C{RN['bke']}-C{RN['bg']})", PB_FAIR, MULT, False)]:
    put(ws, f'A{rw}', lab, fmt=None)
    putf(ws, f'C{rw}', fml, xp, fmt, green=gr)
band(ws, RN['bbase'], 5)
put(ws, f"A{RN['bbase']}", 'BOOK LENS — value per share (AED)', bold=True, fmt=None)
putf(ws, f"C{RN['bbase']}", f"=C{RN['bpb']}*C{RN['bbvpsaed']}", BOOK_BASE, PX, bold=True)
put(ws, f"A{RN['bbear']}", 'Bear — return 15% lower against the asset-risk cost of equity '
    '(C) / bull — return 15% higher against a lower premium (D)', fmt=None)
putf(ws, f"C{RN['bbear']}",
     f"=(C{RN['broe']}*0.85-C{RN['bg']})/(DCF!$C${DF_['kea']}-C{RN['bg']})"
     f"*C{RN['bbvpsaed']}", BOOK_BEAR, PX)
putf(ws, f"D{RN['bbear']}",
     f"=(C{RN['broe']}*1.15-C{RN['bg']})/((DCF!$C${DF_['rfstar']}+0.55*{a('erp')})"
     f"-C{RN['bg']})*C{RN['bbvpsaed']}", BOOK_BULL, PX)

band(ws, RN['vsb'], 5)
put(ws, f"A{RN['vsb']}", 'THE REALISED VESSEL SALE — DIRECT EVIDENCE ON CARRYING VALUES',
    bold=True, fmt=None)
put(ws, f"A{RN['vsbook']}", 'Carrying value of the very large crude carrier sold (USD 000)',
    fmt=None)
putf(ws, f"C{RN['vsbook']}", f"={a('vs_book')}", V['vessel_sale_book'], NUM0, green=True)
put(ws, f"A{RN['vsprice']}", 'Realised sale price, January 2026 (USD 000)', fmt=None)
putf(ws, f"C{RN['vsprice']}", f"={a('vs_price')}", V['vessel_sale_price'], NUM0, green=True)
put(ws, f"A{RN['vsratio']}", 'Realised price over carrying value', bold=True, fmt=None)
putf(ws, f"C{RN['vsratio']}", f"=C{RN['vsprice']}/C{RN['vsbook']}", VSB_RATIO, MULT,
     bold=True)
put(ws, f"A{RN['vsgain']}", 'Capital gain recognised on the sale, as disclosed (USD 000)',
    fmt=None)
putf(ws, f"C{RN['vsgain']}", f"={a('vs_gain')}", V['vessel_sale_gain'], NUM0, green=True)
note(ws, f"A{RN['vsnote']}", 'This is the only direct evidence in the study on how far the '
     'balance sheet\'s carrying values sit below what the fleet would actually fetch: one '
     '2017-built very large crude carrier, ninety per cent owned, sold in January 2026 at '
     'about a third above its carrying value. The book lens above values the equity at its '
     'carried book, so a fleet that would realise more than book is a reason that lens '
     'reads low rather than a reason to adjust it.')

# ============ 8 DCF =============================================================
ws = sheet('DCF')
title(ws, 'Discounted cash flow — the full waterfall', 'USD thousand. Every line is a live '
      'formula: the cost of capital is built below from its own components, the discount '
      'factors compound year on year off the glide, and 2026 is a three-quarter stub '
      'because the valuation date is 31 March 2026.', 6, awidth=58, cwidth=15)
hdr(ws, 4, ['USD 000'] + YFE)


def wf(rw, lab, fmls, vals, fmt=NUM0, bd=False, green=False):
    put(ws, f'A{rw}', lab, bold=bd, fmt=None)
    for i in range(5):
        putf(ws, f'{CD[i]}{rw}', fmls(i), vals[i], fmt, bold=bd, green=green)
    if bd:
        band(ws, rw, 6)


wf(DF_['rev'], 'Revenue', lambda i: f"=Segments!{CD[i]}{SG['frevt']}", REV_F, green=True)
wf(DF_['ebitda'], 'EBITDA', lambda i: f"=Segments!{CD[i]}{SG['febt']}", EB_F, green=True)
wf(DF_['mgn'], 'EBITDA margin', lambda i: f"={CD[i]}{DF_['ebitda']}/{CD[i]}{DF_['rev']}",
   [EB_F[i] / REV_F[i] for i in range(5)], PCT)
wf(DF_['dna'], 'Less depreciation and amortisation',
   lambda i: f"=-'Balance Sheet'!{CD[i]}{BS['dnatot']}", [-x for x in DNA_F], green=True)
wf(DF_['ebit'], 'EBIT', lambda i: f"={CD[i]}{DF_['ebitda']}+{CD[i]}{DF_['dna']}", EBIT_F,
   bd=True)
wf(DF_['tax'], 'Less tax on operating profit — the business-unit mix below',
   lambda i: f"=-{CD[i]}{DF_['taxtot']}", [-x for x in TAX_F])
wf(DF_['nopat'], 'NOPAT', lambda i: f"={CD[i]}{DF_['ebit']}+{CD[i]}{DF_['tax']}", NOPAT_F,
   bd=True)
wf(DF_['adddna'], 'Add back depreciation and amortisation',
   lambda i: f"=-{CD[i]}{DF_['dna']}", DNA_F)
wf(DF_['capex'], 'Less capital expenditure', lambda i: f"=-{a('capex', col=CD[i])}",
   [-x for x in CAPEX], green=True)
wf(DF_['dnwc'], 'Less change in working capital',
   lambda i: f"=-'Balance Sheet'!{CD[i]}{BS['wcdnwc']}", [-x for x in DNWC_F], green=True)
wf(DF_['fcff'], 'Free cash flow to the firm',
   lambda i: (f"={CD[i]}{DF_['nopat']}+{CD[i]}{DF_['adddna']}+{CD[i]}{DF_['capex']}"
              f"+{CD[i]}{DF_['dnwc']}"), FCFF_F, bd=True)
put(ws, f"A{DF_['q1']}", 'Less first-quarter 2026 free cash flow, already inside net debt '
    'at the valuation date', fmt=None)
putf(ws, f"B{DF_['q1']}", f"=-{a('q1fcf')}", -Q1FCF, NUM0, green=True)
for i in range(1, 5):
    put(ws, f"{CD[i]}{DF_['q1']}", '-', BLACK, NUM0)
wf(DF_['fcfd'], 'Free cash flow discounted from 31 March 2026',
   lambda i: (f"={CD[i]}{DF_['fcff']}+{CD[i]}{DF_['q1']}" if i == 0
              else f"={CD[i]}{DF_['fcff']}"), DC['fcffd'], bd=True)
wf(DF_['glide'], 'Forward cost of capital — the glide from current to terminal',
   lambda i: (f"=$C${DF_['wacc']}+($C${DF_['waccterm']}-$C${DF_['wacc']})*{i+1}/5"),
   DC['glide'], PCT2)
wf(DF_['df'], 'Discount factor — each year compounded onto the last',
   lambda i: (f"=1/(1+{CD[i]}{DF_['glide']})^{a('stub')}" if i == 0
              else f"={CD[i-1]}{DF_['df']}/(1+{CD[i]}{DF_['glide']})"), DC['df'], DF4)
wf(DF_['pv'], 'Present value of free cash flow',
   lambda i: f"={CD[i]}{DF_['fcfd']}*{CD[i]}{DF_['df']}", DC['pv'], bd=True)

band(ws, DF_['taxb'], 6)
put(ws, f"A{DF_['taxb']}", 'THE TAX MIX — EACH BUSINESS UNIT AT ITS OWN DISCLOSED RATE',
    bold=True, fmt=None)
for i, y in enumerate(YFE):
    cc = ws.cell(row=DF_['taxb'], column=2 + i, value=y)
    cc.font = Font(bold=True); cc.fill = FILL_G
_TAXKEY = {'Integrated Logistics': 'tax_il', 'Shipping': 'tax_ship', 'Services': 'tax_serv'}
_dnakeys = ['dna_' + s.lower().replace(' ', '_').replace('-', '_') for s in SEGS]
for j, g in enumerate(GROUPS):
    mem = [k for k, s in zip(_dnakeys, SEGS) if SEG_GROUP[s] == g]
    put(ws, f"A{DF_['geb0']+j}", f'{g} — EBITDA', fmt=None)
    put(ws, f"A{DF_['gdna0']+j}", f'{g} — share of depreciation and amortisation', fmt=None)
    put(ws, f"A{DF_['gtax0']+j}", f'{g} — taxable profit', fmt=None)
    put(ws, f"A{DF_['gtaxc0']+j}", f'{g} — tax charge at {TAX_G[g]:.0%}', fmt=None)
    _share = '(' + '+'.join(a(k) for k in mem) + ')/(' + '+'.join(a(k) for k in _dnakeys) + ')'
    for i in range(5):
        putf(ws, f"{CD[i]}{DF_['geb0']+j}", f"=Segments!{CD[i]}{SG['geb0']+j}",
             GRP_EB_F[g][i], NUM0, green=True)
        putf(ws, f"{CD[i]}{DF_['gdna0']+j}",
             f"=-{CD[i]}{DF_['dna']}*{_share}", GRP_DNA_F[g][i], NUM0)
        putf(ws, f"{CD[i]}{DF_['gtax0']+j}",
             f"=MAX({CD[i]}{DF_['geb0']+j}-{CD[i]}{DF_['gdna0']+j},0)", GRP_TAXABLE[g][i],
             NUM0)
        putf(ws, f"{CD[i]}{DF_['gtaxc0']+j}",
             f"={CD[i]}{DF_['gtax0']+j}*{a(_TAXKEY[g])}", GRP_TAX[g][i], NUM0)
put(ws, f"A{DF_['taxtot']}", 'Tax on operating profit', bold=True, fmt=None)
put(ws, f"A{DF_['taxrate']}", 'Effective tax rate on operating profit', fmt=None)
for i in range(5):
    putf(ws, f"{CD[i]}{DF_['taxtot']}",
         f"=SUM({CD[i]}{DF_['gtaxc0']}:{CD[i]}{DF_['gtaxc0']+2})", TAX_F[i], NUM0, bold=True)
    putf(ws, f"{CD[i]}{DF_['taxrate']}", f"={CD[i]}{DF_['taxtot']}/{CD[i]}{DF_['ebit']}",
         TAXRATE_F[i], PCT2)
band(ws, DF_['taxtot'], 6)

band(ws, DF_['tvb'], 6)
put(ws, f"A{DF_['tvb']}", 'TERMINAL VALUE AND THE BRIDGE TO EQUITY', bold=True, fmt=None)
_tv = [(DF_['g'], 'Terminal growth', f"={a('g_term')}", G, PCT, True),
       (DF_['ic'], 'Terminal invested capital',
        f"='Balance Sheet'!I{BS['ic']}", IC_F[4], NUM0, True),
       (DF_['roic'], 'Terminal return on invested capital',
        f"=F{DF_['nopat']}/C{DF_['ic']}", DC['roic_t'], PCT, False),
       (DF_['reinv'], 'Required reinvestment rate — terminal growth over the return on '
        'invested capital', f"=C{DF_['g']}/C{DF_['roic']}", DC['reinv'], PCT, False),
       (DF_['nopat1'], 'Terminal-year NOPAT grown one year',
        f"=F{DF_['nopat']}*(1+C{DF_['g']})", DC['nopat_t1'], NUM0, False),
       (DF_['tv'], 'Terminal value — grown NOPAT net of reinvestment, capitalised at the '
        'terminal rate',
        f"=C{DF_['nopat1']}*(1-C{DF_['reinv']})/(C{DF_['waccterm']}-C{DF_['g']})", DC['tv'],
        NUM0, False),
       (DF_['pvex'], 'Present value of the five forecast years',
        f"=SUM(B{DF_['pv']}:F{DF_['pv']})", DC['pv_expl'], NUM0, False),
       (DF_['pvtv'], 'Present value of the terminal value',
        f"=C{DF_['tv']}*F{DF_['df']}", DC['pv_tv'], NUM0, False),
       (DF_['evops'], 'Enterprise value of operations',
        f"=C{DF_['pvex']}+C{DF_['pvtv']}", DC['ev_ops'], NUM0, False),
       (DF_['tvshare'], 'Terminal value as a share of enterprise value',
        f"=C{DF_['pvtv']}/C{DF_['evops']}", DC['tv_share'], PCT, False),
       (DF_['jv'], 'Plus joint ventures and associates at carrying value', f"={a('jv')}",
        JV_BV, NUM0, True),
       (DF_['ev'], 'Enterprise value', f"=C{DF_['evops']}+C{DF_['jv']}", DC['ev'], NUM0,
        False),
       (DF_['nd'], 'Less net debt at 31 March 2026', f"=-{a('nd_co')}", -NDCO, NUM0, True),
       (DF_['defd'], 'Less deferred consideration on acquisitions', f"=-{a('deferred')}",
        -DEFERRED, NUM0, True),
       (DF_['hyb'], 'Less perpetual capital securities at carrying value',
        f"=-{a('hybrid')}", -HYBRID, NUM0, True),
       (DF_['nci'], 'Less non-controlling interests at carrying value', f"=-{a('nci_bv')}",
        -NCI_BV, NUM0, True),
       (DF_['eq'], 'Equity attributable to ordinary shareholders',
        f"=C{DF_['ev']}+C{DF_['nd']}+C{DF_['defd']}+C{DF_['hyb']}+C{DF_['nci']}",
        DC['equity'], NUM0, False),
       (DF_['fvusd'], 'Fair value per share (USD)',
        f"=C{DF_['eq']}/{a('shares')}/1000", DC['fv_usd'], PX, False),
       (DF_['fvaed'], 'Fair value per share (AED)', f"=C{DF_['fvusd']}*{a('fx')}",
        DC['fv_aed'], PX, False)]
for rw, lab, fml, xp, fmt, gr in _tv:
    put(ws, f'A{rw}', lab, bold=(rw == DF_['fvaed']), fmt=None)
    putf(ws, f'C{rw}', fml, xp, fmt, bold=(rw in (DF_['ev'], DF_['eq'], DF_['fvaed'])),
         green=gr)
band(ws, DF_['eq'], 4); band(ws, DF_['fvaed'], 4)

band(ws, DF_['keb'], 6)
put(ws, f"A{DF_['keb']}", 'COST OF EQUITY — BUILT HERE, NOT ASSUMED', bold=True, fmt=None)
_coc = [(DF_['rfobs'], 'Observed government bond yield (dirham tranche, January 2031)',
         f"={a('rf_obs')}", V['rf_observed'], PCT2, True),
        (DF_['sov'], 'Less sovereign default spread — country risk enters once, through the '
         'premium', f"={a('sov')}", V['sov_spread'], PCT2, True),
        (DF_['rfstar'], 'Normalised risk-free rate',
         f"=C{DF_['rfobs']}-C{DF_['sov']}", RF_STAR, PCT2, False),
        (DF_['beta'], 'Beta — own-stock weekly regression against its local index',
         f"={a('beta')}", V['beta'], BETA, True),
        (DF_['erp'], 'Equity risk premium', f"={a('erp')}", V['erp_total'], PCT2, True),
        (DF_['ke'], 'Cost of equity',
         f"=C{DF_['rfstar']}+C{DF_['beta']}*C{DF_['erp']}", KE, PCT2, False)]
for rw, lab, fml, xp, fmt, gr in _coc:
    put(ws, f'A{rw}', lab, fmt=None)
    putf(ws, f'C{rw}', fml, xp, fmt, bold=(rw == DF_['ke']), green=gr)
band(ws, DF_['ke'], 4)

band(ws, DF_['kdb'], 6)
put(ws, f"A{DF_['kdb']}", 'COST OF DEBT — THREE CONSTRUCTIONS, AVERAGED HERE', bold=True,
    fmt=None)
_kd = [(DF_['sofr'], 'Secured overnight financing rate', f"={a('sofr')}", V['sofr'], PCT2,
        True),
       (DF_['shldrm'], 'Parent revolving credit facility margin', f"={a('shldr_m')}",
        V['shldr_margin'], PCT2, True),
       (DF_['kd1'], 'METHOD 1 — parent revolving facility rate drawn January 2026',
        f"=C{DF_['sofr']}+C{DF_['shldrm']}", KD1, PCT2, False),
       (DF_['banklo'], 'Third-party bank loans — low end of the disclosed range',
        f"={a('bank_lo')}", V['bank_loan_lo'], PCT2, True),
       (DF_['bankhi'], 'Third-party bank loans — high end of the disclosed range',
        f"={a('bank_hi')}", V['bank_loan_hi'], PCT2, True),
       (DF_['bankmid'], 'Bank-loan midpoint',
        f"=(C{DF_['banklo']}+C{DF_['bankhi']})/2", KD_BANK, PCT2, False),
       (DF_['othlo'], 'Other third-party borrowings — low end of the disclosed range',
        f"={a('oth_lo')}", V['other_borr_lo'], PCT2, True),
       (DF_['othhi'], 'Other third-party borrowings — high end of the disclosed range',
        f"={a('oth_hi')}", V['other_borr_hi'], PCT2, True),
       (DF_['othmid'], 'Other-borrowings midpoint',
        f"=(C{DF_['othlo']}+C{DF_['othhi']})/2", KD_OTHER, PCT2, False),
       (DF_['tp'], 'Third-party blended rate — the two midpoints averaged',
        f"=(C{DF_['bankmid']}+C{DF_['othmid']})/2", KD_TP, PCT2, False),
       (DF_['leaseint'], 'Lease interest charged in 2025 (USD 000)', f"={a('lease_int')}",
        V['intpaid_lease_fy25'], NUM0, True),
       (DF_['leaseopen'], 'Lease liabilities, opening balance (USD 000)',
        f"={a('lease_open')}", V['lease_open_fy25'], NUM0, True),
       (DF_['leaseclose'], 'Lease liabilities, closing balance (USD 000)',
        f"={a('lease_close')}", V['lease_close_fy25'], NUM0, True),
       (DF_['kdlease'], 'Implied lease borrowing rate — interest over the average balance',
        f"=C{DF_['leaseint']}/((C{DF_['leaseopen']}+C{DF_['leaseclose']})/2)", KD_LEASE,
        PCT2, False),
       (DF_['dshldr'], 'Shareholder loan at 31 March 2026 (USD 000)', f"={a('d_shldr')}",
        V['q1_26_shldr_loan'], NUM0, True),
       (DF_['dborr'], 'Third-party borrowings at 31 March 2026 (USD 000)',
        f"={a('d_borr')}", V['q1_26_borrowings'], NUM0, True),
       (DF_['dlease'], 'Lease liabilities at 31 March 2026 (USD 000)', f"={a('d_lease')}",
        V['q1_26_leases'], NUM0, True),
       (DF_['dtot'], 'Borrowings at 31 March 2026 (USD 000)',
        f"=C{DF_['dshldr']}+C{DF_['dborr']}+C{DF_['dlease']}", DEBT_NOW, NUM0, False),
       (DF_['kd2'], 'METHOD 2 — the instruments actually outstanding, weighted by balance',
        f"=(C{DF_['dshldr']}*C{DF_['kd1']}+C{DF_['dborr']}*C{DF_['tp']}"
        f"+C{DF_['dlease']}*C{DF_['kdlease']})/C{DF_['dtot']}", KD2, PCT2, False),
       (DF_['kd3'], 'METHOD 3 — the disclosed third-party bank-loan midpoint',
        f"=C{DF_['bankmid']}", KD3, PCT2, False),
       (DF_['kd'], 'Cost of debt — the three constructions averaged',
        f"=AVERAGE(C{DF_['kd1']},C{DF_['kd2']},C{DF_['kd3']})", KD, PCT2, False),
       (DF_['taxstat'], 'Statutory corporate tax rate', f"={a('tax_stat')}", TAXS, PCT,
        True),
       (DF_['kdat'], 'Cost of debt after tax',
        f"=C{DF_['kd']}*(1-C{DF_['taxstat']})", KD_AT, PCT2, False)]
for rw, lab, fml, xp, fmt, gr in _kd:
    put(ws, f'A{rw}', lab, fmt=None)
    putf(ws, f'C{rw}', fml, xp, fmt, bold=(rw == DF_['kd']), green=gr)
band(ws, DF_['kd'], 4)

band(ws, DF_['wb'], 6)
put(ws, f"A{DF_['wb']}", 'WEIGHTS AND THE COST OF CAPITAL', bold=True, fmt=None)
_w = [(DF_['mktcap'], 'Market capitalisation (USD 000)',
       f"={a('spot')}/{a('fx')}*{a('shares')}*1000", MKTCAP, NUM0, False),
      (DF_['borr'], 'Borrowings at 31 March 2026 (USD 000)', f"=C{DF_['dtot']}", DEBT_NOW,
       NUM0, False),
      (DF_['we'], 'Equity weight — market capitalisation over the total',
       f"=C{DF_['mktcap']}/(C{DF_['mktcap']}+C{DF_['borr']})", WE, PCT2, False),
      (DF_['wd'], 'Debt weight', f"=1-C{DF_['we']}", WD, PCT2, False),
      (DF_['wacc'], 'Cost of capital — explicit window',
       f"=C{DF_['we']}*C{DF_['ke']}+C{DF_['wd']}*C{DF_['kdat']}", W_EXP, PCT2, False),
      (DF_['rfterm'], 'Terminal risk-free rate', f"={a('rf_term')}", V['rf_terminal'], PCT2,
       True),
      (DF_['keterm'], 'Terminal cost of equity',
       f"=C{DF_['rfterm']}+C{DF_['beta']}*C{DF_['erp']}", KE_T, PCT2, False),
      (DF_['kdterm'], 'Terminal cost of debt — the same spread over the terminal rate',
       f"=C{DF_['rfterm']}+(C{DF_['kd']}-C{DF_['rfstar']})", KD_T, PCT2, False),
      (DF_['kdtermat'], 'Terminal cost of debt after tax',
       f"=C{DF_['kdterm']}*(1-C{DF_['taxstat']})", KD_T_AT, PCT2, False),
      (DF_['waccterm'], 'Terminal cost of capital',
       f"=C{DF_['we']}*C{DF_['keterm']}+C{DF_['wd']}*C{DF_['kdtermat']}", W_TERM, PCT2,
       False)]
for rw, lab, fml, xp, fmt, gr in _w:
    put(ws, f'A{rw}', lab, fmt=None)
    putf(ws, f'C{rw}', fml, xp, fmt,
         bold=(rw in (DF_['wacc'], DF_['waccterm'])), green=gr)
band(ws, DF_['wacc'], 4); band(ws, DF_['waccterm'], 4)

band(ws, DF_['ab'], 6)
put(ws, f"A{DF_['ab']}", 'THE CONTESTED JUDGEMENT — THE SAME MODEL ON AN ASSET-RISK BETA '
    'OF 1.00', bold=True, fmt=None)
for rw, lab, fml, xp, fmt, gr in [
        (DF_['betaa'], 'Asset-risk beta', f"={a('beta_a')}", 1.0, BETA, True),
        (DF_['kea'], 'Cost of equity on the asset-risk beta',
         f"=C{DF_['rfstar']}+C{DF_['betaa']}*C{DF_['erp']}", KE_A, PCT2, False),
        (DF_['keta'], 'Terminal cost of equity on the asset-risk beta',
         f"=C{DF_['rfterm']}+C{DF_['betaa']}*C{DF_['erp']}", KE_T_A, PCT2, False),
        (DF_['wacca'], 'Cost of capital — explicit window, asset-risk beta',
         f"=C{DF_['we']}*C{DF_['kea']}+C{DF_['wd']}*C{DF_['kdat']}", W_EXP_A, PCT2, False),
        (DF_['wactermsa'], 'Terminal cost of capital, asset-risk beta',
         f"=C{DF_['we']}*C{DF_['keta']}+C{DF_['wd']}*C{DF_['kdtermat']}", W_TERM_A, PCT2,
         False)]:
    put(ws, f'A{rw}', lab, fmt=None)
    putf(ws, f'C{rw}', fml, xp, fmt, green=gr)
hdr(ws, DF_['ahdr'], ['The same cash flows, discounted at the asset-risk cost of capital']
    + YFE)
wf(DF_['glidea'], 'Forward cost of capital — the glide',
   lambda i: (f"=$C${DF_['wacca']}+($C${DF_['wactermsa']}-$C${DF_['wacca']})*{i+1}/5"),
   DA['glide'], PCT2)
wf(DF_['dfa'], 'Discount factor',
   lambda i: (f"=1/(1+{CD[i]}{DF_['glidea']})^{a('stub')}" if i == 0
              else f"={CD[i-1]}{DF_['dfa']}/(1+{CD[i]}{DF_['glidea']})"), DA['df'], DF4)
wf(DF_['pva'], 'Present value of free cash flow',
   lambda i: f"={CD[i]}{DF_['fcfd']}*{CD[i]}{DF_['dfa']}", DA['pv'])
for rw, lab, fml, xp, fmt in [
        (DF_['pvexa'], 'Present value of the five forecast years',
         f"=SUM(B{DF_['pva']}:F{DF_['pva']})", DA['pv_expl'], NUM0),
        (DF_['tva'], 'Terminal value',
         f"=C{DF_['nopat1']}*(1-C{DF_['reinv']})/(C{DF_['wactermsa']}-C{DF_['g']})",
         DA['tv'], NUM0),
        (DF_['pvtva'], 'Present value of the terminal value',
         f"=C{DF_['tva']}*F{DF_['dfa']}", DA['pv_tv'], NUM0),
        (DF_['evopsa'], 'Enterprise value of operations',
         f"=C{DF_['pvexa']}+C{DF_['pvtva']}", DA['ev_ops'], NUM0),
        (DF_['tvsharea'], 'Terminal value as a share of enterprise value',
         f"=C{DF_['pvtva']}/C{DF_['evopsa']}", DA['tv_share'], PCT),
        (DF_['eva'], 'Enterprise value', f"=C{DF_['evopsa']}+C{DF_['jv']}", DA['ev'], NUM0),
        (DF_['eqa'], 'Equity attributable to ordinary shareholders',
         f"=C{DF_['eva']}+C{DF_['nd']}+C{DF_['defd']}+C{DF_['hyb']}+C{DF_['nci']}",
         DA['equity'], NUM0),
        (DF_['fvaeda'], 'Fair value per share (AED) — asset-risk beta',
         f"=C{DF_['eqa']}/{a('shares')}/1000*{a('fx')}", DA['fv_aed'], PX)]:
    put(ws, f'A{rw}', lab, bold=(rw == DF_['fvaeda']), fmt=None)
    putf(ws, f'C{rw}', fml, xp, fmt, bold=(rw == DF_['fvaeda']))
band(ws, DF_['fvaeda'], 4)
note(ws, f"A{DF_['fvaeda']+2}", 'The two readings above are carried side by side and are '
     'never averaged. The regressed beta is the primary reading because it passes the '
     'usability gate on the stock\'s own history; the asset-risk beta is what a listed '
     'fleet owner might instead be expected to carry, and the gap between the two is the '
     'single most consequential judgement in this study.')

# ============ 9 INCOME STATEMENT =================================================
ws = sheet('Income Statement')
title(ws, 'Income statement — three years audited, five years forecast', 'USD thousand, '
      'consolidated. History is the audited record; every forecast line is a formula.', 9,
      awidth=52, cwidth=13)
hdr(ws, 4, ['USD 000'] + YH + YFE)


def line(rw, lab, hist_v, hist_f, fc_f, fc_v, fmt=NUM0, bd=False, green=False):
    put(ws, f'A{rw}', lab, bold=bd, fmt=None)
    for i in range(3):
        if hist_f is not None:
            putf(ws, f'{HC[i]}{rw}', hist_f(i), hist_v[i], fmt, bold=bd)
        else:
            put(ws, f'{HC[i]}{rw}', hist_v[i], BLUE, fmt, bold=bd)
    for i in range(5):
        if fc_f is None:
            put(ws, f'{FCOL[i]}{rw}', '-', BLACK, fmt, bold=bd)
        else:
            putf(ws, f'{FCOL[i]}{rw}', fc_f(i), fc_v[i], fmt, bold=bd, green=green)
    if bd:
        band(ws, rw, 9)


line(IS['rev'], 'Revenue', HI['revenue'], None,
     lambda i: f"=DCF!{CD[i]}{DF_['rev']}", REV_F, bd=True, green=True)
line(IS['dc'], 'Direct costs', HI['direct_costs'], None, None, None)
line(IS['gp'], 'Gross profit', HI['gross_profit'],
     lambda i: f"={HC[i]}{IS['rev']}+{HC[i]}{IS['dc']}", None, None)
line(IS['ga'], 'General and administrative expenses', HI['ga'], None, None, None)
line(IS['ecl'], 'Expected credit losses', HI['ecl'], None, None, None)
line(IS['oi'], 'Other income', HI['other_income'], None, None, None)
line(IS['oe'], 'Other expenses', HI['other_expenses'], None, None, None)
line(IS['op'], 'Operating profit', HI['ebit'],
     lambda i: (f"={HC[i]}{IS['gp']}+{HC[i]}{IS['ga']}+{HC[i]}{IS['ecl']}"
                f"+{HC[i]}{IS['oi']}+{HC[i]}{IS['oe']}"),
     lambda i: f"={FCOL[i]}{IS['ebitda']}-{FCOL[i]}{IS['dna']}", EBIT_F, bd=True)
line(IS['dna'], 'Depreciation and amortisation', H_DNA, None,
     lambda i: f"='Balance Sheet'!{CD[i]}{BS['dnatot']}", DNA_F, green=True)
line(IS['ebitda'], 'EBITDA (operating)', H_EBITDA,
     lambda i: f"={HC[i]}{IS['op']}+{HC[i]}{IS['dna']}",
     lambda i: f"=DCF!{CD[i]}{DF_['ebitda']}", EB_F, bd=True, green=True)
_ebjv = [HI['ebitda_bridge']['share_of_jv'][i] + HI['ebitda_bridge']['one_offs'][i]
         for i in range(3)]
line(IS['ebjv'], 'Add share of joint ventures and one-off gains carried in reported EBITDA',
     _ebjv, None, None, None)
line(IS['ebrep'], 'EBITDA as reported', HI['ebitda_reported'],
     lambda i: f"={HC[i]}{IS['ebitda']}+{HC[i]}{IS['ebjv']}",
     lambda i: f"={FCOL[i]}{IS['ebitda']}", EB_F)
line(IS['opcost'], 'Total operating costs', H_OPCOST,
     lambda i: f"={HC[i]}{IS['rev']}-{HC[i]}{IS['ebitda']}",
     lambda i: f"={FCOL[i]}{IS['rev']}-{FCOL[i]}{IS['ebitda']}", OPCOST_F)
line(IS['mgn'], 'EBITDA margin (operating)',
     [H_EBITDA[i] / H_REV[i] for i in range(3)],
     lambda i: f"={HC[i]}{IS['ebitda']}/{HC[i]}{IS['rev']}",
     lambda i: f"={FCOL[i]}{IS['ebitda']}/{FCOL[i]}{IS['rev']}",
     [EB_F[i] / REV_F[i] for i in range(5)], PCT)
line(IS['assoc'], 'Share of joint ventures and associates', HI['assoc'], None, None, None)
line(IS['bargain'], 'Gain on bargain purchase',
     [0, 0, V['bargain_fy25']], None, None, None)
line(IS['prevheld'], 'Loss on the previously held interest',
     [0, 0, V['prevheld_fy25']], None, None, None)
line(IS['fininc'], 'Finance income', HI['fin_income'], None,
     lambda i: f"={a('sofr')}*{a('cash')}", FININC_F, green=True)
line(IS['fincost'], 'Finance costs', HI['fin_costs'], None,
     lambda i: f"=-DCF!$C${DF_['kd']}*'Balance Sheet'!{CD[i]}{BS['ndgross']}",
     [-x for x in INT_F], green=True)
line(IS['pbt'], 'Profit before tax', HI['pbt'],
     lambda i: (f"={HC[i]}{IS['op']}+{HC[i]}{IS['assoc']}+{HC[i]}{IS['bargain']}"
                f"+{HC[i]}{IS['prevheld']}+{HC[i]}{IS['fininc']}+{HC[i]}{IS['fincost']}"),
     lambda i: f"={FCOL[i]}{IS['op']}+{FCOL[i]}{IS['fininc']}+{FCOL[i]}{IS['fincost']}",
     PBT_F, bd=True)
line(IS['tax'], 'Income tax', HI['tax'], None,
     lambda i: f"=-{FCOL[i]}{IS['pbt']}*DCF!{CD[i]}{DF_['taxrate']}", [-x for x in TAXP_F])
line(IS['pat'], 'Profit for the year', HI['pat'],
     lambda i: f"={HC[i]}{IS['pbt']}+{HC[i]}{IS['tax']}",
     lambda i: f"={FCOL[i]}{IS['pbt']}+{FCOL[i]}{IS['tax']}", PAT_F)
line(IS['nci'], 'Non-controlling interests', [0, 0, -V['nci_pl_fy25']], None,
     lambda i: f"=-{FCOL[i]}{IS['pat']}*{a('nci_sh')}", [-x for x in NCI_F])
line(IS['npa'], 'Profit attributable to shareholders', H_NPA,
     lambda i: f"={HC[i]}{IS['pat']}+{HC[i]}{IS['nci']}",
     lambda i: f"={FCOL[i]}{IS['pat']}+{FCOL[i]}{IS['nci']}", NPA_F, bd=True)
line(IS['hybcpn'], 'Perpetual capital securities coupon',
     [0, 0, -V['hybrid_coupon_fy25']], None,
     lambda i: f"=-{a('hybrid')}*({a('sofr')}+{a('hyb_m')})", [-HYB_CPN] * 5)
line(IS['ordn'], 'Earnings attributable to ordinary shareholders', H_ORD,
     lambda i: f"={HC[i]}{IS['npa']}+{HC[i]}{IS['hybcpn']}",
     lambda i: f"={FCOL[i]}{IS['npa']}+{FCOL[i]}{IS['hybcpn']}", ORD_F, bd=True)
put(ws, f"A{IS['eps']}", 'Earnings per ordinary share (USD)', fmt=None)
put(ws, f"A{IS['epsaed']}", 'Earnings per ordinary share (AED)', fmt=None)
for i in range(8):
    putf(ws, f"{ALL[i]}{IS['eps']}", f"={ALL[i]}{IS['ordn']}/{a('shares')}/1000",
         ORD_ALL[i] / SH / 1000.0, PX3)
    putf(ws, f"{ALL[i]}{IS['epsaed']}", f"={ALL[i]}{IS['eps']}*{a('fx')}",
         ORD_ALL[i] / SH / 1000.0 * PEG, PX3)
note(ws, f"A{IS['epsaed']+2}", 'Every FY2023-25 line above is the audited figure. In the '
     'forecast the company\'s own disclosure-only lines — direct costs, gross profit, the '
     'general and administrative split, the share of joint ventures and the two 2025 '
     'acquisition items — are not projected, because the forecast is built at the business-'
     'unit level on earnings before depreciation rather than on a cost-line split the '
     'filings do not support forward. The finance charge is computed on gross borrowings, '
     'which move with the net-debt roll, so profit is struck after interest and differs '
     'from the pre-financing discounted-cash-flow waterfall by construction.')

# ============ 10 BALANCE SHEET ====================================================
ws = sheet('Balance Sheet')
title(ws, 'Balance sheet — condensed, and the rolls that drive it', 'USD thousand, '
      'consolidated. Every FY2023-25 line is the audited closing figure; every forecast '
      'line is rolled forward from a driver.', 9, awidth=52, cwidth=13)
hdr(ws, 4, ['USD 000'] + YH + YFE)


def bline(rw, lab, hist_v, fc_f, fc_v, fmt=NUM0, bd=False, hist_f=None, green=False):
    put(ws, f'A{rw}', lab, bold=bd, fmt=None)
    for i in range(3):
        if hist_f is not None:
            putf(ws, f'{HC[i]}{rw}', hist_f(i), hist_v[i], fmt, bold=bd)
        else:
            put(ws, f'{HC[i]}{rw}', hist_v[i], BLUE, fmt, bold=bd)
    for i in range(5):
        if fc_f is None:
            put(ws, f'{FCOL[i]}{rw}', '-', BLACK, fmt, bold=bd)
        else:
            putf(ws, f'{FCOL[i]}{rw}', fc_f(i), fc_v[i], fmt, bold=bd, green=green)
    if bd:
        band(ws, rw, 9)


bline(BS['ppe'], 'Property, plant and equipment', HB['ppe'],
      lambda i: f"={CD[i]}{BS['ppeclose']}", PPE_CLOSE)
bline(BS['rou'], 'Right-of-use assets', HB['rou'], None, None)
bline(BS['intang'], 'Intangible assets', HB['intangibles'], lambda i: f"={a('intang')}",
      [INTANG] * 5, green=True)
bline(BS['gw'], 'Goodwill', HB['goodwill'], lambda i: f"={a('gw')}", [GW] * 5, green=True)
bline(BS['invprop'], 'Investment properties', HB['inv_prop'], None, None)
bline(BS['jv'], 'Investments in joint ventures and associates', HB['jv'],
      lambda i: f"={a('jv')}", [JV_BV] * 5, green=True)
bline(BS['inv'], 'Inventories', HB['inventories'], lambda i: f"={CD[i]}{BS['wcinv']}",
      INV_F)
bline(BS['recv'], 'Trade and other receivables, including amounts due from related parties',
      [HB['receivables'][i] + HB['due_from_related'][i] for i in range(3)],
      lambda i: f"={CD[i]}{BS['wcrecv']}", RECV_F)
bline(BS['cash'], 'Cash and cash equivalents', HB['cash'], lambda i: f"={a('cash')}",
      [CASH] * 5, green=True)
bline(BS['ta'], 'Total assets', HB['total_assets'], None, None, bd=True)
bline(BS['pay'], 'Trade and other payables, including amounts due to related parties',
      [HB['payables'][i] + HB['due_to_related'][i] for i in range(3)],
      lambda i: f"={CD[i]}{BS['wcpay']}", PAY_F)
put(ws, f"A{BS['nwc']}", 'Net working capital', fmt=None)
for i in range(8):
    putf(ws, f"{ALL[i]}{BS['nwc']}",
         f"={ALL[i]}{BS['recv']}+{ALL[i]}{BS['inv']}-{ALL[i]}{BS['pay']}", NWC_ALL[i], NUM0)
bline(BS['grossd'], 'Gross borrowings', HB['debt'],
      lambda i: f"={CD[i]}{BS['ndgross']}", GROSS_D)
bline(BS['nd'], 'Net debt', HB['net_debt'], lambda i: f"={CD[i]}{BS['ndclose']}",
      ND_CLOSE, bd=True)
bline(BS['hyb'], 'Perpetual capital securities', HB['hybrid'], lambda i: f"={a('hybrid')}",
      [HYBRID] * 5, green=True)
bline(BS['nci'], 'Non-controlling interests', HB['nci'], lambda i: f"={a('nci_bv')}",
      [NCI_BV] * 5, green=True)
bline(BS['eqp'], 'Equity attributable to shareholders', HB['equity_parent'],
      lambda i: f"={CD[i]}{BS['eqclose']}", EQ_CLOSE, bd=True)
put(ws, f"A{BS['teq']}", 'Total equity', bold=True, fmt=None)
_teq = [HB['total_equity'][i] for i in range(3)] + [EQ_CLOSE[i] + HYBRID + NCI_BV
                                                   for i in range(5)]
for i in range(8):
    putf(ws, f"{ALL[i]}{BS['teq']}",
         f"={ALL[i]}{BS['eqp']}+{ALL[i]}{BS['hyb']}+{ALL[i]}{BS['nci']}", _teq[i], NUM0,
         bold=True)
band(ws, BS['teq'], 9)
put(ws, f"A{BS['ndeb']}", 'Net debt / EBITDA', fmt=None)
put(ws, f"A{BS['bvps']}", 'Book value per share (USD)', fmt=None)
put(ws, f"A{BS['bvpsaed']}", 'Book value per share (AED)', fmt=None)
put(ws, f"A{BS['ic']}", 'Invested capital', fmt=None)
for i in range(8):
    putf(ws, f"{ALL[i]}{BS['ndeb']}",
         f"={ALL[i]}{BS['nd']}/'Income Statement'!{ALL[i]}{IS['ebitda']}",
         ND_ALL[i] / EB_ALL[i], MULT)
    putf(ws, f"{ALL[i]}{BS['bvps']}", f"={ALL[i]}{BS['eqp']}/{a('shares')}/1000",
         EQ_ALL[i] / SH / 1000.0, PX3)
    putf(ws, f"{ALL[i]}{BS['bvpsaed']}", f"={ALL[i]}{BS['bvps']}*{a('fx')}",
         EQ_ALL[i] / SH / 1000.0 * PEG, PX)
    putf(ws, f"{ALL[i]}{BS['ic']}",
         f"={ALL[i]}{BS['ppe']}+{ALL[i]}{BS['nwc']}+{ALL[i]}{BS['intang']}"
         f"+{ALL[i]}{BS['gw']}", IC_ALL[i], NUM0)
put(ws, f"A{BS['roic']}", 'Return on invested capital', fmt=None)
put(ws, f"A{BS['roe']}", 'Return on equity (profit over average equity)', fmt=None)
for i in range(3):
    put(ws, f"{HC[i]}{BS['roic']}", '-', BLACK, PCT)
for i in range(5):
    putf(ws, f"{FCOL[i]}{BS['roic']}",
         f"=DCF!{CD[i]}{DF_['nopat']}/{FCOL[i]}{BS['ic']}", ROIC_F[i], PCT)
put(ws, f"B{BS['roe']}", '-', BLACK, PCT)
_hroe = [None] + [H_NPA[i] / ((H_EQ[i - 1] + H_EQ[i]) / 2) for i in (1, 2)]
for i in (1, 2):
    putf(ws, f"{HC[i]}{BS['roe']}",
         f"='Income Statement'!{HC[i]}{IS['npa']}/(({HC[i-1]}{BS['eqp']}"
         f"+{HC[i]}{BS['eqp']})/2)", _hroe[i], PCT)
for i in range(5):
    prev = f"{a('eqp0')}" if i == 0 else f"{FCOL[i-1]}{BS['eqp']}"
    putf(ws, f"{FCOL[i]}{BS['roe']}",
         f"='Income Statement'!{FCOL[i]}{IS['npa']}/(({prev}+{FCOL[i]}{BS['eqp']})/2)",
         ROE_F[i], PCT)

band(ws, BS['ppeb'], 6)
put(ws, f"A{BS['ppeb']}", 'THE PROPERTY, PLANT AND EQUIPMENT ROLL', bold=True, fmt=None)
for i, y in enumerate(YFE):
    cc = ws.cell(row=BS['ppeb'], column=2 + i, value=y); cc.font = Font(bold=True)
    cc.fill = FILL_G
put(ws, f"A{BS['ppeopen']}", 'Opening property, plant and equipment', fmt=None)
put(ws, f"A{BS['ppecapex']}", 'Capital expenditure', fmt=None)
put(ws, f"A{BS['ppedeprate']}", 'Depreciation rate on property, plant and equipment',
    fmt=None)
put(ws, f"A{BS['ppedep1']}", 'First-pass depreciation, on the opening balance plus the full '
    'additions', fmt=None)
put(ws, f"A{BS['ppedep']}", 'Depreciation on property, plant and equipment — on the average '
    'of opening and closing', fmt=None)
put(ws, f"A{BS['ppeclose']}", 'Closing property, plant and equipment', bold=True, fmt=None)
put(ws, f"A{BS['otherdna']}", 'Other depreciation and amortisation, escalated', fmt=None)
put(ws, f"A{BS['dnatot']}", 'Total depreciation and amortisation', bold=True, fmt=None)
for i in range(5):
    c = CD[i]
    f_open = (f"={a('ppe_dummy')}" if False else
              (f"=D{BS['ppe']}" if i == 0 else f"={CD[i-1]}{BS['ppeclose']}"))
    putf(ws, f"{c}{BS['ppeopen']}", f_open, PPE_OPEN[i], NUM0, green=(i == 0))
    putf(ws, f"{c}{BS['ppecapex']}", f"={a('capex', col=c)}", CAPEX[i], NUM0, green=True)
    putf(ws, f"{c}{BS['ppedeprate']}", f"={a('dep_rate')}", DEP_RATE, PCT2, green=True)
    putf(ws, f"{c}{BS['ppedep1']}",
         f"={c}{BS['ppedeprate']}*({c}{BS['ppeopen']}+({c}{BS['ppeopen']}"
         f"+{c}{BS['ppecapex']}))/2", DEP1[i], NUM0)
    putf(ws, f"{c}{BS['ppedep']}",
         f"={c}{BS['ppedeprate']}*({c}{BS['ppeopen']}+({c}{BS['ppeopen']}"
         f"+{c}{BS['ppecapex']}-{c}{BS['ppedep1']}))/2", DEP_PPE[i], NUM0)
    putf(ws, f"{c}{BS['ppeclose']}",
         f"={c}{BS['ppeopen']}+{c}{BS['ppecapex']}-{c}{BS['ppedep']}", PPE_CLOSE[i], NUM0,
         bold=True)
    putf(ws, f"{c}{BS['otherdna']}", f"={a('other_dna')}*(1+{a('opex_esc')})^{i+1}",
         OTHER_DNA_Y[i], NUM0)
    putf(ws, f"{c}{BS['dnatot']}", f"={c}{BS['ppedep']}+{c}{BS['otherdna']}", DNA_F[i],
         NUM0, bold=True)
band(ws, BS['dnatot'], 6)

band(ws, BS['wcb'], 6)
put(ws, f"A{BS['wcb']}", 'THE WORKING-CAPITAL ROLL FROM THE DAYS RATIOS', bold=True,
    fmt=None)
for i, y in enumerate(YFE):
    cc = ws.cell(row=BS['wcb'], column=2 + i, value=y); cc.font = Font(bold=True)
    cc.fill = FILL_G
for rw, lab in [(BS['wcrev'], 'Revenue'), (BS['wcopcost'], 'Total operating costs'),
                (BS['wcdso'], 'Days sales outstanding'),
                (BS['wcdio'], 'Days inventory outstanding'),
                (BS['wcdpo'], 'Days payable outstanding'),
                (BS['wcrecv'], 'Trade and other receivables — revenue x days / 365'),
                (BS['wcinv'], 'Inventories — operating cost x days / 365'),
                (BS['wcpay'], 'Trade and other payables — operating cost x days / 365'),
                (BS['wcnwc'], 'Net working capital'),
                (BS['wcdnwc'], 'Change in net working capital')]:
    put(ws, f'A{rw}', lab, bold=(rw in (BS['wcnwc'], BS['wcdnwc'])), fmt=None)
for i in range(5):
    c = CD[i]
    putf(ws, f"{c}{BS['wcrev']}", f"=DCF!{c}{DF_['rev']}", REV_F[i], NUM0, green=True)
    putf(ws, f"{c}{BS['wcopcost']}", f"={c}{BS['wcrev']}-DCF!{c}{DF_['ebitda']}",
         OPCOST_F[i], NUM0)
    putf(ws, f"{c}{BS['wcdso']}", f"={a('dso')}", DSO, NUM1, green=True)
    putf(ws, f"{c}{BS['wcdio']}", f"={a('dio')}", DIO, NUM1, green=True)
    putf(ws, f"{c}{BS['wcdpo']}", f"={a('dpo')}", DPO, NUM1, green=True)
    putf(ws, f"{c}{BS['wcrecv']}", f"={c}{BS['wcrev']}*{c}{BS['wcdso']}/365", RECV_F[i],
         NUM0)
    putf(ws, f"{c}{BS['wcinv']}", f"={c}{BS['wcopcost']}*{c}{BS['wcdio']}/365", INV_F[i],
         NUM0)
    putf(ws, f"{c}{BS['wcpay']}", f"={c}{BS['wcopcost']}*{c}{BS['wcdpo']}/365", PAY_F[i],
         NUM0)
    putf(ws, f"{c}{BS['wcnwc']}",
         f"={c}{BS['wcrecv']}+{c}{BS['wcinv']}-{c}{BS['wcpay']}", NWC_F[i], NUM0, bold=True)
    prev = a('nwc25') if i == 0 else f"{CD[i-1]}{BS['wcnwc']}"
    putf(ws, f"{c}{BS['wcdnwc']}", f"={c}{BS['wcnwc']}-{prev}", DNWC_F[i], NUM0, bold=True)
band(ws, BS['wcnwc'], 6)

band(ws, BS['ndb'], 6)
put(ws, f"A{BS['ndb']}", 'THE NET-DEBT ROLL', bold=True, fmt=None)
for i, y in enumerate(YFE):
    cc = ws.cell(row=BS['ndb'], column=2 + i, value=y); cc.font = Font(bold=True)
    cc.fill = FILL_G
for rw, lab in [(BS['ndopen'], 'Opening net debt'),
                (BS['ndgross'], 'Gross borrowings — opening net debt plus the cash held'),
                (BS['ndint'], 'Interest charge on gross borrowings'),
                (BS['ndfcff'], 'Free cash flow to the firm'),
                (BS['ndintat'], 'Less interest after tax'),
                (BS['ndfi'], 'Plus finance income after tax'),
                (BS['ndcpn'], 'Less perpetual capital securities coupon'),
                (BS['ndfcfe'], 'Free cash flow to equity'),
                (BS['nddps'], 'Less ordinary dividends'),
                (BS['ndclose'], 'Closing net debt')]:
    put(ws, f'A{rw}', lab, bold=(rw in (BS['ndfcfe'], BS['ndclose'])), fmt=None)
for i in range(5):
    c = CD[i]
    f_open = f"={a('nd_co')}+{a('deferred')}" if i == 0 else f"={CD[i-1]}{BS['ndclose']}"
    putf(ws, f"{c}{BS['ndopen']}", f_open, ND_OPEN[i], NUM0, green=(i == 0))
    putf(ws, f"{c}{BS['ndgross']}", f"={c}{BS['ndopen']}+{a('cash')}", GROSS_D[i], NUM0)
    putf(ws, f"{c}{BS['ndint']}", f"=DCF!$C${DF_['kd']}*{c}{BS['ndgross']}", INT_F[i], NUM0)
    putf(ws, f"{c}{BS['ndfcff']}", f"=DCF!{c}{DF_['fcff']}", FCFF_F[i], NUM0, green=True)
    putf(ws, f"{c}{BS['ndintat']}", f"=-{c}{BS['ndint']}*(1-{a('tax_stat')})",
         -INT_F[i] * (1 - TAXS), NUM0)
    putf(ws, f"{c}{BS['ndfi']}",
         f"={a('sofr')}*{a('cash')}*(1-{a('tax_stat')})", FININC_F[i] * (1 - TAXS), NUM0)
    putf(ws, f"{c}{BS['ndcpn']}", f"=-{a('hybrid')}*({a('sofr')}+{a('hyb_m')})", -HYB_CPN,
         NUM0)
    putf(ws, f"{c}{BS['ndfcfe']}",
         f"={c}{BS['ndfcff']}+{c}{BS['ndintat']}+{c}{BS['ndfi']}+{c}{BS['ndcpn']}",
         FCFE_F[i], NUM0, bold=True)
    putf(ws, f"{c}{BS['nddps']}", f"=-{a('dps26')}*(1+{a('div_g')})^{i}", -DPS[i], NUM0)
    putf(ws, f"{c}{BS['ndclose']}",
         f"={c}{BS['ndopen']}-{c}{BS['ndfcfe']}-{c}{BS['nddps']}", ND_CLOSE[i], NUM0,
         bold=True)
band(ws, BS['ndclose'], 6)

band(ws, BS['eqb'], 6)
put(ws, f"A{BS['eqb']}", 'THE EQUITY ROLL', bold=True, fmt=None)
for i, y in enumerate(YFE):
    cc = ws.cell(row=BS['eqb'], column=2 + i, value=y); cc.font = Font(bold=True)
    cc.fill = FILL_G
for rw, lab in [(BS['eqopen'], 'Opening equity attributable to shareholders'),
                (BS['eqnpa'], 'Add profit attributable to shareholders'),
                (BS['eqdps'], 'Less ordinary dividends'),
                (BS['eqcpn'], 'Less perpetual capital securities coupon'),
                (BS['eqclose'], 'Closing equity attributable to shareholders'),
                (BS['dpsps'], 'Ordinary dividend per share (USD)')]:
    put(ws, f'A{rw}', lab, bold=(rw == BS['eqclose']), fmt=None)
for i in range(5):
    c = CD[i]
    f_open = f"={a('eqp0')}" if i == 0 else f"={CD[i-1]}{BS['eqclose']}"
    putf(ws, f"{c}{BS['eqopen']}", f_open, EQ_OPEN[i], NUM0, green=(i == 0))
    putf(ws, f"{c}{BS['eqnpa']}", f"='Income Statement'!{FCOL[i]}{IS['npa']}", NPA_F[i],
         NUM0, green=True)
    putf(ws, f"{c}{BS['eqdps']}", f"={c}{BS['nddps']}", -DPS[i], NUM0)
    putf(ws, f"{c}{BS['eqcpn']}", f"={c}{BS['ndcpn']}", -HYB_CPN, NUM0)
    putf(ws, f"{c}{BS['eqclose']}",
         f"={c}{BS['eqopen']}+{c}{BS['eqnpa']}+{c}{BS['eqdps']}+{c}{BS['eqcpn']}",
         EQ_CLOSE[i], NUM0, bold=True)
    putf(ws, f"{c}{BS['dpsps']}", f"=-{c}{BS['eqdps']}/{a('shares')}/1000",
         DPS[i] / SH / 1000.0, PX3)
band(ws, BS['eqclose'], 6)
note(ws, f"A{BS['dpsps']+2}", 'The condensed layout above does not foot to zero: right-of-'
     'use assets, investment properties, provisions, deferred tax and the other liabilities '
     'not shown separately are omitted from the forecast columns because they are not '
     'driven by anything in this model. The audited FY2023-25 columns carry every line as '
     'reported.')

# ============ 11 CASH FLOW =========================================================
ws = sheet('Cash Flow')
title(ws, 'Cash flow — the audited record and the forecast waterfall', 'USD thousand.', 9,
      awidth=52, cwidth=13)
hdr(ws, 4, ['USD 000'] + YH + YFE)
put(ws, f"A{CF['ebitda']}", 'EBITDA (operating)', fmt=None)
put(ws, f"A{CF['ocf']}", 'Operating cash flow, as reported', fmt=None)
put(ws, f"A{CF['capex']}", 'Capital expenditure', fmt=None)
put(ws, f"A{CF['fcf']}", 'Free cash flow, as reported', bold=True, fmt=None)
for i in range(8):
    putf(ws, f"{ALL[i]}{CF['ebitda']}", f"='Income Statement'!{ALL[i]}{IS['ebitda']}",
         EB_ALL[i], NUM0, green=True)
for i in range(3):
    put(ws, f"{HC[i]}{CF['ocf']}", HC_['ocf'][i], BLUE, NUM0)
    put(ws, f"{HC[i]}{CF['capex']}", HC_['capex'][i], BLUE, NUM0)
    putf(ws, f"{HC[i]}{CF['fcf']}", f"={HC[i]}{CF['ocf']}+{HC[i]}{CF['capex']}",
         HC_['fcf'][i], NUM0, bold=True)
for i in range(5):
    put(ws, f"{FCOL[i]}{CF['ocf']}", '-', BLACK, NUM0)
    putf(ws, f"{FCOL[i]}{CF['capex']}", f"=DCF!{CD[i]}{DF_['capex']}", -CAPEX[i], NUM0,
         green=True)
    put(ws, f"{FCOL[i]}{CF['fcf']}", '-', BLACK, NUM0, bold=True)
band(ws, CF['fcf'], 9)
band(ws, CF['wfb'], 9)
put(ws, f"A{CF['wfb']}", 'THE FORECAST WATERFALL — LINKED TO THE DISCOUNTED-CASH-FLOW SHEET',
    bold=True, fmt=None)
for i, y in enumerate(YFE):
    cc = ws.cell(row=CF['wfb'], column=5 + i, value=y); cc.font = Font(bold=True)
    cc.fill = FILL_G
_cfrows = [(CF['nopat'], 'NOPAT', lambda i: f"=DCF!{CD[i]}{DF_['nopat']}", NOPAT_F, True),
           (CF['dna'], 'Add back depreciation and amortisation',
            lambda i: f"=DCF!{CD[i]}{DF_['adddna']}", DNA_F, True),
           (CF['cap'], 'Less capital expenditure',
            lambda i: f"=DCF!{CD[i]}{DF_['capex']}", [-x for x in CAPEX], True),
           (CF['dnwc'], 'Less change in working capital',
            lambda i: f"=DCF!{CD[i]}{DF_['dnwc']}", [-x for x in DNWC_F], True),
           (CF['fcff'], 'Free cash flow to the firm',
            lambda i: (f"={FCOL[i]}{CF['nopat']}+{FCOL[i]}{CF['dna']}+{FCOL[i]}{CF['cap']}"
                       f"+{FCOL[i]}{CF['dnwc']}"), FCFF_F, False),
           (CF['intat'], 'Less interest after tax',
            lambda i: f"='Balance Sheet'!{CD[i]}{BS['ndintat']}",
            [-x * (1 - TAXS) for x in INT_F], True),
           (CF['fi'], 'Plus finance income after tax',
            lambda i: f"='Balance Sheet'!{CD[i]}{BS['ndfi']}",
            [x * (1 - TAXS) for x in FININC_F], True),
           (CF['cpn'], 'Less perpetual capital securities coupon',
            lambda i: f"='Balance Sheet'!{CD[i]}{BS['ndcpn']}", [-HYB_CPN] * 5, True),
           (CF['fcfe'], 'Free cash flow to equity',
            lambda i: (f"={FCOL[i]}{CF['fcff']}+{FCOL[i]}{CF['intat']}+{FCOL[i]}{CF['fi']}"
                       f"+{FCOL[i]}{CF['cpn']}"), FCFE_F, False),
           (CF['dps'], 'Less ordinary dividends',
            lambda i: f"='Balance Sheet'!{CD[i]}{BS['nddps']}", [-x for x in DPS], True),
           (CF['ndmove'], 'Movement in net debt (a fall is a negative)',
            lambda i: f"=-{FCOL[i]}{CF['fcfe']}-{FCOL[i]}{CF['dps']}",
            [ND_CLOSE[i] - ND_OPEN[i] for i in range(5)], False)]
for rw, lab, fml, vals, gr in _cfrows:
    bd = rw in (CF['fcff'], CF['fcfe'])
    put(ws, f'A{rw}', lab, bold=bd, fmt=None)
    for i in range(3):
        put(ws, f'{HC[i]}{rw}', '-', BLACK, NUM0)
    for i in range(5):
        putf(ws, f'{FCOL[i]}{rw}', fml(i), vals[i], NUM0, bold=bd, green=gr)
    if bd:
        band(ws, rw, 9)
put(ws, f"A{CF['conv']}", 'Cash conversion — free cash flow to the firm over EBITDA',
    fmt=None)
for i in range(3):
    put(ws, f'{HC[i]}{CF["conv"]}', '-', BLACK, PCT)
for i in range(5):
    putf(ws, f"{FCOL[i]}{CF['conv']}", f"={FCOL[i]}{CF['fcff']}/{FCOL[i]}{CF['ebitda']}",
         FCFF_F[i] / EB_F[i], PCT)
note(ws, f"A{CF['conv']+2}", 'Cash conversion is the crux of an asset-heavy fleet owner: in '
     '2026 the newbuild programme absorbs more than the whole of the operating cash the '
     'business generates, and only as that programme delivers does free cash flow to the '
     'firm turn materially positive.')

# ============ 12 SUMMARY FINANCIALS =================================================
ws = sheet('Summary Financials')
title(ws, 'Summary financials — the eight-year picture', 'USD thousand unless stated. Every '
      'cell on this sheet is a link or a ratio; nothing is typed twice.', 9, awidth=52,
      cwidth=13)
hdr(ws, 4, ['USD 000'] + YH + YFE)
r = 5


def sf(lab, fml, vals, fmt=NUM0, skip=()):
    global r
    put(ws, f'A{r}', lab, fmt=None)
    for i in range(8):
        if i in skip or vals[i] is None:
            put(ws, f'{ALL[i]}{r}', '-', BLACK, fmt)
        else:
            f_ = fml(i)
            putf(ws, f'{ALL[i]}{r}', f_, vals[i], fmt,
                 green=f_.startswith(("='I", "='B", '=DCF', "='C", "='S")))
    r += 1


sf('Revenue', lambda i: f"='Income Statement'!{ALL[i]}{IS['rev']}", REV_ALL)
sf('Revenue growth', lambda i: f'={ALL[i]}5/{ALL[i-1]}5-1',
   [None] + [REV_ALL[i] / REV_ALL[i - 1] - 1 for i in range(1, 8)], PCT, skip=(0,))
sf('EBITDA (operating)', lambda i: f"='Income Statement'!{ALL[i]}{IS['ebitda']}", EB_ALL)
sf('EBITDA margin', lambda i: f"='Income Statement'!{ALL[i]}{IS['mgn']}",
   [EB_ALL[i] / REV_ALL[i] for i in range(8)], PCT)
sf('EBIT', lambda i: f"='Income Statement'!{ALL[i]}{IS['op']}", EBIT_ALL)
sf('Depreciation and amortisation', lambda i: f"='Income Statement'!{ALL[i]}{IS['dna']}",
   DNA_ALL)
sf('Profit attributable to shareholders', lambda i: f"='Income Statement'!{ALL[i]}{IS['npa']}",
   NPA_ALL)
sf('Earnings attributable to ordinary shareholders',
   lambda i: f"='Income Statement'!{ALL[i]}{IS['ordn']}", ORD_ALL)
sf('Earnings per ordinary share (AED)',
   lambda i: f"='Income Statement'!{ALL[i]}{IS['epsaed']}",
   [ORD_ALL[i] / SH / 1000.0 * PEG for i in range(8)], PX3)
sf('Free cash flow to the firm', lambda i: f"='Cash Flow'!{ALL[i]}{CF['fcff']}",
   [None] * 3 + FCFF_F, skip=(0, 1, 2))
sf('Capital expenditure', lambda i: f"='Cash Flow'!{ALL[i]}{CF['capex']}", CAPEX_ALL)
sf('Capital expenditure / revenue', lambda i: f'=-{ALL[i]}{r-1}/{ALL[i]}5',
   [-CAPEX_ALL[i] / REV_ALL[i] for i in range(8)], PCT)
sf('Net working capital', lambda i: f"='Balance Sheet'!{ALL[i]}{BS['nwc']}", NWC_ALL)
sf('Net working capital / revenue', lambda i: f'={ALL[i]}{r-1}/{ALL[i]}5',
   [NWC_ALL[i] / REV_ALL[i] for i in range(8)], PCT)
sf('Net debt', lambda i: f"='Balance Sheet'!{ALL[i]}{BS['nd']}", ND_ALL)
sf('Net debt / EBITDA', lambda i: f"='Balance Sheet'!{ALL[i]}{BS['ndeb']}",
   [ND_ALL[i] / EB_ALL[i] for i in range(8)], MULT)
sf('Equity attributable to shareholders', lambda i: f"='Balance Sheet'!{ALL[i]}{BS['eqp']}",
   EQ_ALL)
sf('Invested capital', lambda i: f"='Balance Sheet'!{ALL[i]}{BS['ic']}", IC_ALL)
sf('Return on invested capital', lambda i: f"='Balance Sheet'!{ALL[i]}{BS['roic']}",
   [None] * 3 + ROIC_F, PCT, skip=(0, 1, 2))
sf('Return on equity', lambda i: f"='Balance Sheet'!{ALL[i]}{BS['roe']}",
   [None] + _hroe[1:] + ROE_F, PCT, skip=(0,))
note(ws, f'A{r+1}', 'Return on invested capital is the discounted-cash-flow sheet\'s NOPAT '
     'over the same year\'s invested capital, which is why the audited years carry capital '
     'but no return: their tax charge is struck on a post-financing basis and is not '
     'comparable with the pre-financing NOPAT the forecast uses.')

# ============ 13 MONTE CARLO ==========================================================
ws = sheet('Monte Carlo')
title(ws, 'Probabilistic price map', 'A map of price dispersion over the next one and three '
      'months. It carries no view on value and is never blended with the valuation. Each '
      'figure is a complete engine re-run, so it is a pasted value and does NOT redraw when '
      'a driver is changed.', 8, awidth=48, cwidth=14)
hdr(ws, MC['hdr'], ['Horizon (AED)', '5th', '25th', 'Median', '75th', '95th',
                    'Probability above spot'])
for j, tag in enumerate(('1M', '3M')):
    h = STK['horizons'][tag]
    rw = MC['h0'] + j
    put(ws, f'A{rw}', f"{'One month' if tag == '1M' else 'Three months'} — graded "
        f"{h['grade_date']}", fmt=None)
    for i, k in enumerate(('p5', 'p25', 'p50', 'p75', 'p95')):
        put(ws, f'{get_column_letter(2+i)}{rw}', h['pct'][k], BLUE, PX)
    put(ws, f'G{rw}', h['p_above'], BLUE, PCT)
hdr(ws, MC['lhdr'], ['Level event', 'One month', 'Three months'])
for j, (lab, k) in enumerate([('Finishes 10% or more above spot', 'p_up10'),
                              ('Finishes 10% or more below spot', 'p_dn10'),
                              ('Touches 10% above spot at any point', 'touch_up10'),
                              ('Touches 10% below spot at any point', 'touch_dn10')]):
    rw = MC['l0'] + j
    put(ws, f'A{rw}', lab, fmt=None)
    put(ws, f'B{rw}', STK['horizons']['1M'][k], BLUE, PCT)
    put(ws, f'C{rw}', STK['horizons']['3M'][k], BLUE, PCT)
hdr(ws, MC['ehdr'], ['Engine setting', '', 'Value'])
for j, (lab, v, fmt, gr) in enumerate([
        ('Simulated paths', 50000, NUM0, False),
        ('Annualised volatility (three-month anchor)',
         STK['horizons']['3M']['anchor_vol_ann'], PCT, False),
        ('Spot price (AED)', f"=Summary!$C${SU['spot']}", PX, True),
        ('Anchor date', STK['anchor_date'], None, False),
        ('Calibration verdict on the five-year walk-forward', STEP0['verdict'], None,
         False)]):
    rw = MC['e0'] + j
    put(ws, f'A{rw}', lab, fmt=None)
    if gr:
        putf(ws, f'C{rw}', v, SPOT, fmt, green=True)
    else:
        put(ws, f'C{rw}', v, BLUE, fmt)
note(ws, f"A{MC['e0']+6}", 'The price map is a dispersion forecast from the price series '
     'alone. It is deliberately not reconciled to the valuation lenses: one is a statement '
     'about what a price could do over weeks, the other about what a business is worth.')

# ============ 14 SENSITIVITY ============================================================
ws = sheet('Sensitivity')
title(ws, 'Sensitivity — what the valuation needs the world to do', 'AED per share. Each '
      'cell is a complete re-run of the whole model, including the fleet build, so these '
      'grids are engine outputs rather than formulas and do NOT redraw when a driver is '
      'changed.', 8, awidth=52, cwidth=14)
band(ws, SE['bgb'], 8)
put(ws, f"A{SE['bgb']}", 'Beta (rows) x terminal growth (columns)', bold=True, fmt=None)
hdr(ws, SE['bghdr'], ['Beta'] + [f'{g:.1%}' for g in SN['gs']])
for i, b in enumerate(SN['betas']):
    rw = SE['bg0'] + i
    put(ws, f'A{rw}', f'{b:.3f}', fmt=None)
    for j in range(len(SN['gs'])):
        put(ws, f'{get_column_letter(2+j)}{rw}', SN['grid_beta_g'][i][j], BLUE, PX)
band(ws, SE['ab'], 8)
put(ws, f"A{SE['ab']}", 'Mid-cycle tanker rate anchor, as a multiple of the base anchor',
    bold=True, fmt=None)
_am = ['0.8', '0.9', '1.0', '1.1', '1.2']
hdr(ws, SE['ahdr'], [''] + [f'{float(m):.2f}x' for m in _am])
put(ws, f"A{SE['a0']}", 'Fair value per share (AED)', fmt=None)
for j, m in enumerate(_am):
    put(ws, f'{get_column_letter(2+j)}{SE["a0"]}', SN['anchor'][m], BLUE, PX)
put(ws, f"A{SE['aswing']}", 'Swing across the grid', fmt=None)
putf(ws, f"C{SE['aswing']}", f"=MAX(B{SE['a0']}:F{SE['a0']})-MIN(B{SE['a0']}:F{SE['a0']})",
     max(SN['anchor'].values()) - min(SN['anchor'].values()), PX)
band(ws, SE['cb'], 8)
put(ws, f"A{SE['cb']}", 'Capital expenditure, as a multiple of the guided path', bold=True,
    fmt=None)
_cm = ['0.9', '1.0', '1.1', '1.2']
hdr(ws, SE['chdr'], [''] + [f'{float(m):.2f}x' for m in _cm])
put(ws, f"A{SE['c0']}", 'Fair value per share (AED)', fmt=None)
for j, m in enumerate(_cm):
    put(ws, f'{get_column_letter(2+j)}{SE["c0"]}', SN['capex'][m], BLUE, PX)
put(ws, f"A{SE['cswing']}", 'Swing across the grid', fmt=None)
putf(ws, f"C{SE['cswing']}", f"=MAX(B{SE['c0']}:E{SE['c0']})-MIN(B{SE['c0']}:E{SE['c0']})",
     max(SN['capex'].values()) - min(SN['capex'].values()), PX)
band(ws, SE['tb'], 8)
put(ws, f"A{SE['tb']}", 'A uniform group tax rate — the global-minimum-tax case', bold=True,
    fmt=None)
_tk = ['0.05', '0.09', '0.15']
hdr(ws, SE['thdr'], [''] + [f'{float(t):.0%}' for t in _tk])
put(ws, f"A{SE['t0']}", 'Fair value per share (AED)', fmt=None)
for j, t in enumerate(_tk):
    put(ws, f'{get_column_letter(2+j)}{SE["t0"]}', SN['tax'][t], BLUE, PX)
note(ws, f"A{SE['tnote']}", 'The shipping units currently bear under one per cent, because '
     'international shipping income is relieved under the corporate tax law; the group\'s '
     'blended charge on operating profit is therefore only a few per cent. A fifteen per '
     'cent rate reaching that income — a global minimum tax applied without the shipping '
     'relief — is the downside case, and it is a whole-model re-run rather than a formula '
     'because the mix itself changes.')
band(ws, SE['mb'], 8)
put(ws, f"A{SE['mb']}", 'THE RATE PATH AGAINST WHAT THE FORWARD MARKET WAS ACTUALLY PAYING',
    bold=True, fmt=None)
MCC = SN['market_cross_check']
put(ws, f"A{SE['m1y']}", 'One-year time charter fixed in early 2026, very large crude '
    'carrier (USD per day)', fmt=None)
put(ws, f"C{SE['m1y']}", MCC['vlcc_1y_tc'], BLUE, NUM0)
put(ws, f"A{SE['mspot']}", 'Broker spot print for the same vessel class (USD per day)',
    fmt=None)
put(ws, f"C{SE['mspot']}", MCC['vlcc_spot_broker'], BLUE, NUM0)
hdr(ws, SE['mhdr'], ["This study's own path for the same vessel class (USD per day)"] + YFE)
put(ws, f"A{SE['mpath']}", 'Very large crude carrier — spot time-charter equivalent',
    fmt=None)
for i in range(5):
    putf(ws, f'{CD[i]}{SE["mpath"]}', f"=Segments!{CD[i]}{SG['path0']+4}",
         TNK_PATH['vlcc'][i], NUM0, green=True)
put(ws, f"A{SE['mvs']}", 'The study\'s 2027 path over the one-year time charter', fmt=None)
putf(ws, f"C{SE['mvs']}", f"=C{SE['mpath']}/C{SE['m1y']}",
     TNK_PATH['vlcc'][1] / MCC['vlcc_1y_tc'], MULT)
put(ws, f"A{SE['mob']}", 'Crude tanker order book as a share of the trading fleet', fmt=None)
put(ws, f"C{SE['mob']}", MCC['orderbook_pct'], BLUE, PCT)
note(ws, f"A{SE['mnote']}", MCC['note'])
ws.column_dimensions['A'].width = 58

# ============ 15 PER-SHARE & RATIOS =========================================================
ws = sheet('Per-Share & Ratios')
title(ws, 'Per-share and ratio analysis', 'The indicator set for an asset-heavy marine '
      'logistics operator. Every ratio is a formula off the statements; per-share figures '
      'convert to dirhams at the fixed parity.', 9, awidth=52, cwidth=13)
hdr(ws, 4, ['Measure'] + YH + YFE)


def ratio(rw, lab, fml, vals, fmt, skip=()):
    put(ws, f'A{rw}', lab, fmt=None)
    for i in range(8):
        if i in skip or vals[i] is None:
            put(ws, f'{ALL[i]}{rw}', '-', BLACK, fmt)
        else:
            putf(ws, f'{ALL[i]}{rw}', fml(i), vals[i], fmt)


ratio(PS['eps'], 'Earnings per ordinary share (USD)',
      lambda i: f"='Income Statement'!{ALL[i]}{IS['eps']}",
      [ORD_ALL[i] / SH / 1000.0 for i in range(8)], PX3)
ratio(PS['epsaed'], 'Earnings per ordinary share (AED)',
      lambda i: f"='Income Statement'!{ALL[i]}{IS['epsaed']}",
      [ORD_ALL[i] / SH / 1000.0 * PEG for i in range(8)], PX3)
ratio(PS['ordps'], 'Attributable profit per share (AED, before the perpetual coupon)',
      lambda i: f"='Income Statement'!{ALL[i]}{IS['npa']}/{a('shares')}/1000*{a('fx')}",
      [NPA_ALL[i] / SH / 1000.0 * PEG for i in range(8)], PX3)
ratio(PS['bvps'], 'Book value per share (AED)',
      lambda i: f"='Balance Sheet'!{ALL[i]}{BS['bvpsaed']}",
      [EQ_ALL[i] / SH / 1000.0 * PEG for i in range(8)], PX)
ratio(PS['fcffps'], 'Free cash flow to the firm per share (AED)',
      lambda i: f"='Cash Flow'!{ALL[i]}{CF['fcff']}/{a('shares')}/1000*{a('fx')}",
      [None] * 3 + [x / SH / 1000.0 * PEG for x in FCFF_F], PX3, skip=(0, 1, 2))
ratio(PS['dpsps'], 'Ordinary dividend per share (AED)',
      lambda i: f"='Balance Sheet'!{CD[i-3]}{BS['dpsps']}*{a('fx')}",
      [None] * 3 + [x / SH / 1000.0 * PEG for x in DPS], PX3, skip=(0, 1, 2))
ratio(PS['payout'], 'Ordinary dividend payout ratio',
      lambda i: f"=-'Balance Sheet'!{CD[i-3]}{BS['eqdps']}/'Income Statement'!"
                f"{ALL[i]}{IS['npa']}",
      [None] * 3 + [DPS[i] / NPA_F[i] for i in range(5)], PCT, skip=(0, 1, 2))
ratio(PS['gm'], 'Gross margin',
      lambda i: f"='Income Statement'!{ALL[i]}{IS['gp']}/'Income Statement'!"
                f"{ALL[i]}{IS['rev']}",
      [HI['gross_profit'][i] / H_REV[i] for i in range(3)] + [None] * 5,
      PCT, skip=(3, 4, 5, 6, 7))
ratio(PS['ebm'], 'EBITDA margin', lambda i: f"='Income Statement'!{ALL[i]}{IS['mgn']}",
      [EB_ALL[i] / REV_ALL[i] for i in range(8)], PCT)
ratio(PS['ebitm'], 'EBIT margin',
      lambda i: f"='Income Statement'!{ALL[i]}{IS['op']}/'Income Statement'!"
                f"{ALL[i]}{IS['rev']}", [EBIT_ALL[i] / REV_ALL[i] for i in range(8)], PCT)
ratio(PS['netm'], 'Net margin (attributable)',
      lambda i: f"='Income Statement'!{ALL[i]}{IS['npa']}/'Income Statement'!"
                f"{ALL[i]}{IS['rev']}", [NPA_ALL[i] / REV_ALL[i] for i in range(8)], PCT)
ratio(PS['roe'], 'Return on equity', lambda i: f"='Balance Sheet'!{ALL[i]}{BS['roe']}",
      [None] + _hroe[1:] + ROE_F, PCT, skip=(0,))
ratio(PS['roic'], 'Return on invested capital',
      lambda i: f"='Balance Sheet'!{ALL[i]}{BS['roic']}", [None] * 3 + ROIC_F, PCT,
      skip=(0, 1, 2))
ratio(PS['ndeb'], 'Net debt / EBITDA', lambda i: f"='Balance Sheet'!{ALL[i]}{BS['ndeb']}",
      [ND_ALL[i] / EB_ALL[i] for i in range(8)], MULT)
ratio(PS['cover'], 'Interest cover (EBIT over finance costs)',
      lambda i: f"=-'Income Statement'!{ALL[i]}{IS['op']}/'Income Statement'!"
                f"{ALL[i]}{IS['fincost']}",
      [HI['ebit'][i] / abs(HI['fin_costs'][i]) for i in range(3)]
      + [EBIT_F[i] / INT_F[i] for i in range(5)], MULT)
ratio(PS['dso'], 'Days sales outstanding',
      lambda i: f"='Balance Sheet'!{ALL[i]}{BS['recv']}/'Income Statement'!"
                f"{ALL[i]}{IS['rev']}*365",
      [(HB['receivables'][i] + HB['due_from_related'][i]) / H_REV[i] * 365
       for i in range(3)] + [DSO] * 5, NUM1)
ratio(PS['dio'], 'Days inventory outstanding',
      lambda i: f"='Balance Sheet'!{ALL[i]}{BS['inv']}/'Income Statement'!"
                f"{ALL[i]}{IS['opcost']}*365",
      [HB['inventories'][i] / H_OPCOST[i] * 365 for i in range(3)] + [DIO] * 5, NUM1)
ratio(PS['dpo'], 'Days payable outstanding',
      lambda i: f"='Balance Sheet'!{ALL[i]}{BS['pay']}/'Income Statement'!"
                f"{ALL[i]}{IS['opcost']}*365",
      [(HB['payables'][i] + HB['due_to_related'][i]) / H_OPCOST[i] * 365
       for i in range(3)] + [DPO] * 5, NUM1)
ratio(PS['cycle'], 'Cash conversion cycle (days)',
      lambda i: f"={ALL[i]}{PS['dso']}+{ALL[i]}{PS['dio']}-{ALL[i]}{PS['dpo']}",
      [(HB['receivables'][i] + HB['due_from_related'][i]) / H_REV[i] * 365
       + HB['inventories'][i] / H_OPCOST[i] * 365
       - (HB['payables'][i] + HB['due_to_related'][i]) / H_OPCOST[i] * 365
       for i in range(3)] + [DSO + DIO - DPO] * 5, NUM1)
ratio(PS['capexrev'], 'Capital expenditure / revenue',
      lambda i: f"=-'Cash Flow'!{ALL[i]}{CF['capex']}/'Income Statement'!"
                f"{ALL[i]}{IS['rev']}",
      [-CAPEX_ALL[i] / REV_ALL[i] for i in range(8)], PCT)
band(ws, PS['ab'], 9)
put(ws, f"A{PS['ab']}", 'MULTIPLES AT THE ANCHOR PRICE', bold=True, fmt=None)
for rw, lab, fml, xp, fmt in [
        (PS['aprice'], 'Share price (AED)', f"=Summary!$C${SU['spot']}", SPOT, PX),
        (PS['apriceusd'], 'Share price (USD)',
         f"='Relative & Normalized'!$C${RN['spotusd']}", SPOT / PEG, PX),
        (PS['amkt'], 'Market capitalisation (USD 000)',
         f"='Relative & Normalized'!$C${RN['mktcap']}", MKTCAP, NUM0),
        (PS['aev'], 'Enterprise value (USD 000)',
         f"='Relative & Normalized'!$C${RN['evnow']}", EV_NOW, NUM0),
        (PS['aeveb'], 'Enterprise value / 2025 reported EBITDA',
         f"='Relative & Normalized'!$C${RN['eveb_ttm']}", OWN_EVEB_TTM, MULT),
        (PS['aeveb26'], 'Enterprise value / FY2026E EBITDA',
         f"='Relative & Normalized'!$C${RN['eveb_26']}", OWN_EVEB_26, MULT),
        (PS['ape'], 'Price / 2025 ordinary earnings',
         f"='Relative & Normalized'!$C${RN['pe_ttm']}", OWN_PE_TTM, MULT),
        (PS['apb'], 'Price / book at 31 March 2026',
         f"='Relative & Normalized'!$C${RN['pb']}", OWN_PB, MULT),
        (PS['ady'], 'Dividend yield on the 2026 distribution',
         f"='Relative & Normalized'!$C${RN['dy']}", OWN_DY, PCT)]:
    put(ws, f'A{rw}', lab, fmt=None)
    putf(ws, f'C{rw}', fml, xp, fmt, green=True)

# ============ 16 PEER & SECTOR ===============================================================
ws = sheet('Peer & Sector')
title(ws, 'Peer frame and sector context', 'No single clean comparable exists: the company '
      'is part contracted marine logistics and part spot tanker owner, so the frame is '
      'built from both ends and blended on the company\'s own disclosed exposure.', 10,
      awidth=34, cwidth=15)
hdr(ws, PR['hdr'], ['Company', 'Market', 'Business model', 'EV/EBITDA', 'Forward P/E',
                    'Trailing P/E', 'Price / book', 'Dividend yield', 'Source', 'As at'])
for j, p in enumerate(PEERS):
    rw = PR['p0'] + j
    put(ws, f'A{rw}', p['name'], fmt=None)
    put(ws, f'B{rw}', p['market'], fmt=None)
    put(ws, f'C{rw}', p['model'], fmt=None, wrap=True)
    put(ws, f'D{rw}', p['ev_ebitda'], BLUE, MULT)
    put(ws, f'E{rw}', p['pe_fwd'] if p['pe_fwd'] is not None else 'n/a', BLUE, MULT)
    put(ws, f'F{rw}', p['pe_ttm'] if p['pe_ttm'] is not None else 'n/a', BLUE, MULT)
    put(ws, f'G{rw}', p['pb'] if p['pb'] is not None else 'n/a', BLUE, MULT)
    put(ws, f'H{rw}', p['dy'] if p['dy'] is not None else 'n/a', BLUE, PCT)
    put(ws, f'I{rw}', p['src'], fmt=None, wrap=True)
    put(ws, f'J{rw}', p['asof'], fmt=None)
    ws.row_dimensions[rw].height = 28
ws.column_dimensions['C'].width = 30; ws.column_dimensions['I'].width = 34
ws.column_dimensions['A'].width = 30
band(ws, PR['mb'], 10)
put(ws, f"A{PR['mb']}", 'THE MULTIPLES USED IN THE RELATIVE LENS', bold=True, fmt=None)
for rw, lab, fml, xp, fmt in [
        (PR['mcon'], 'Contracted-shipping multiple', f"=D{PR['p0']}", MULT_CONTR, MULT),
        (PR['mspot'], 'Spot-tanker multiple — the two spot owners averaged',
         f"=(D{PR['p0']+1}+D{PR['p0']+2})/2", MULT_SPOT, MULT),
        (PR['mw'], 'Share of 2026 earnings exposed to spot rates, as disclosed',
         f"={a('spot_w')}", SPOT_W, PCT),
        (PR['mev'], 'Blended enterprise multiple',
         f"=(1-C{PR['mw']})*C{PR['mcon']}+C{PR['mw']}*C{PR['mspot']}", BLEND_EV, MULT),
        (PR['pecon'], 'Contracted-shipping forward price/earnings', f"=E{PR['p0']}",
         PEERS[0]['pe_fwd'], MULT),
        (PR['pespot'], 'Spot-tanker forward price/earnings', f"=E{PR['p0']+1}",
         PEERS[1]['pe_fwd'], MULT),
        (PR['pe'], 'Blended price/earnings',
         f"=(1-C{PR['mw']})*C{PR['pecon']}+C{PR['mw']}*C{PR['pespot']}", BLEND_PE, MULT)]:
    put(ws, f'A{rw}', lab, fmt=None)
    putf(ws, f'C{rw}', fml, xp, fmt, green=fml.startswith('=Assumptions'))
band(ws, PR['ob'], 10)
put(ws, f"A{PR['ob']}", "THE COMPANY'S OWN MULTIPLES AT THE ANCHOR PRICE", bold=True,
    fmt=None)
for j, (lab, src, xp, fmt) in enumerate([
        ('Enterprise value / 2025 reported EBITDA', RN['eveb_ttm'], OWN_EVEB_TTM, MULT),
        ('Enterprise value / FY2026E EBITDA', RN['eveb_26'], OWN_EVEB_26, MULT),
        ('Price / 2025 ordinary earnings', RN['pe_ttm'], OWN_PE_TTM, MULT),
        ('Price / book at 31 March 2026', RN['pb'], OWN_PB, MULT),
        ('Dividend yield on the 2026 distribution', RN['dy'], OWN_DY, PCT)]):
    rw = PR['o0'] + j
    put(ws, f'A{rw}', lab, fmt=None)
    putf(ws, f'C{rw}', f"='Relative & Normalized'!$C${src}", xp, fmt, green=True)
note(ws, f"A{PR['o0']+6}", 'The contracted peer is a long-term contracted gas shipping '
     'company whose earnings look nothing like a spot tanker owner\'s; the two spot owners '
     'carry the opposite exposure. Neither is a comparable on its own, which is why the '
     'multiple applied is a blend weighted by the share of earnings the company itself '
     'discloses as spot-exposed, and why the relative lens is a cross-check rather than an '
     'independent valuation.')

# ============ 2 SUMMARY (filled now the source rows are known) ==================
ws = wb['Summary']
_LSRC = {'dcf': (f"='Fundamental Valuation'!$C${FV['dcfbear']}", f"=DCF!$C${DF_['fvaed']}",
                 f"='Fundamental Valuation'!$C${FV['dcfbull']}"),
         'relative': (f"='Relative & Normalized'!$C${RN['bear']}",
                      f"='Relative & Normalized'!$C${RN['base']}",
                      f"='Relative & Normalized'!$D${RN['bear']}"),
         'normalized': (f"='Relative & Normalized'!$C${RN['nbear']}",
                        f"='Relative & Normalized'!$C${RN['nbase']}",
                        f"='Relative & Normalized'!$D${RN['nbear']}"),
         'book': (f"='Relative & Normalized'!$C${RN['bbear']}",
                  f"='Relative & Normalized'!$C${RN['bbase']}",
                  f"='Relative & Normalized'!$D${RN['bbear']}")}
_WKEY = {'dcf': 'w_dcf', 'relative': 'w_rel', 'normalized': 'w_norm', 'book': 'w_book'}
_SUKEY = {'dcf': 'dcf', 'relative': 'rel', 'normalized': 'norm', 'book': 'book'}
for k in ('dcf', 'relative', 'normalized', 'book'):
    rw = SU[_SUKEY[k]]
    put(ws, f'A{rw}', LENS_LABEL[k], fmt=None)
    for col, idx in (('B', 0), ('C', 1), ('D', 2)):
        putf(ws, f'{col}{rw}', _LSRC[k][idx], LB[k][idx], PX, green=True)
    putf(ws, f'E{rw}', f"={a(_WKEY[k])}", LW[k], PCT, green=True)
    putf(ws, f'F{rw}', f'=C{rw}*E{rw}', LB[k][1] * LW[k], PX)
    putf(ws, f'G{rw}', f"=C{rw}/$C${SU['spot']}-1", LB[k][1] / SPOT - 1, PCT)
putf(ws, f"H{SU['dcf']}", f"=DCF!$C${DF_['tvshare']}", DC['tv_share'], PCT, green=True)
band(ws, SU['central'], 8)
put(ws, f"A{SU['central']}", 'WEIGHTED CENTRAL', bold=True, fmt=None)
_LK = ['dcf', 'rel', 'norm', 'book']
for col, idx, xp in (('B', 0, CENTRAL_BEAR), ('D', 2, CENTRAL_BULL)):
    putf(ws, f"{col}{SU['central']}",
         '=' + '+'.join(f'{col}{SU[k]}*E{SU[k]}' for k in _LK), xp, PX, bold=True)
putf(ws, f"C{SU['central']}",
     f"=SUM(F{SU['dcf']}:F{SU['book']})", CENTRAL, PX, bold=True)
putf(ws, f"E{SU['central']}", f"=SUM(E{SU['dcf']}:E{SU['book']})", 1.0, PCT, bold=True)
putf(ws, f"G{SU['central']}", f"=C{SU['central']}/$C${SU['spot']}-1", CENTRAL / SPOT - 1,
     PCT, bold=True)
band(ws, SU['cb'], 8)
put(ws, f"A{SU['cb']}", 'THE CONTESTED JUDGEMENT — PUBLISHED BOTH WAYS, NEVER AVERAGED',
    bold=True, fmt=None)
put(ws, f"A{SU['dcfa']}", 'Discounted cash flow (asset-risk beta of 1.00)', fmt=None)
putf(ws, f"B{SU['dcfa']}", f"=B{SU['dcf']}", LN['dcf']['bear'], PX)
putf(ws, f"C{SU['dcfa']}", f"=DCF!$C${DF_['fvaeda']}", DA['fv_aed'], PX, green=True)
putf(ws, f"D{SU['dcfa']}", f"=D{SU['dcf']}", LN['dcf']['bull'], PX)
putf(ws, f"E{SU['dcfa']}", f"=E{SU['dcf']}", LW['dcf'], PCT)
putf(ws, f"F{SU['dcfa']}", f"=C{SU['dcfa']}*E{SU['dcfa']}", DA['fv_aed'] * LW['dcf'], PX)
putf(ws, f"G{SU['dcfa']}", f"=C{SU['dcfa']}/$C${SU['spot']}-1", DA['fv_aed'] / SPOT - 1, PCT)
putf(ws, f"H{SU['dcfa']}", f"=DCF!$C${DF_['tvsharea']}", DA['tv_share'], PCT, green=True)
put(ws, f"A{SU['centrala']}", 'Weighted central on the asset-risk beta', bold=True, fmt=None)
putf(ws, f"C{SU['centrala']}",
     f"=F{SU['dcfa']}+F{SU['rel']}+F{SU['norm']}+F{SU['book']}", CENTRAL_A, PX, bold=True)
putf(ws, f"G{SU['centrala']}", f"=C{SU['centrala']}/$C${SU['spot']}-1", CENTRAL_A / SPOT - 1,
     PCT, bold=True)
band(ws, SU['centrala'], 8)
put(ws, f"A{SU['panel']}", 'Expert panel average', fmt=None)
putf(ws, f"C{SU['panel']}", f"='Fundamental Valuation'!$C${FV['epanel']}",
     D['panel_centre'], PX, green=True)
putf(ws, f"G{SU['panel']}", f"=C{SU['panel']}/$C${SU['spot']}-1",
     D['panel_centre'] / SPOT - 1, PCT)
put(ws, f"A{SU['spot']}", 'Market price (AED, anchor)', bold=True, fmt=None)
put(ws, f"C{SU['spot']}", SPOT, BLUE, PX, bold=True)
band(ws, SU['spot'], 8)
hdr(ws, SU['keyhdr'], ['Key figure', '', 'Value'])
_KEY = [('Shares outstanding (mn)', f"={a('shares')}", SH, NUM1),
        ('Market capitalisation (USD 000)', f"=DCF!$C${DF_['mktcap']}", MKTCAP, NUM0),
        ('Enterprise value at the anchor price (USD 000)',
         f"='Relative & Normalized'!$C${RN['evnow']}", EV_NOW, NUM0),
        ('Net debt including deferred consideration, 31 March 2026 (USD 000)',
         f"='Relative & Normalized'!$C${RN['netdebt']}", NETDEBT, NUM0),
        ('FY2025 revenue (USD 000)', f"='Income Statement'!D{IS['rev']}", H_REV[2], NUM0),
        ('FY2025 EBITDA as reported (USD 000)', f"='Income Statement'!D{IS['ebrep']}",
         HI['ebitda_reported'][2], NUM0),
        ('FY2025 profit attributable to shareholders (USD 000)',
         f"='Income Statement'!D{IS['npa']}", H_NPA[2], NUM0),
        ('Cost of equity — regressed beta', f"=DCF!$C${DF_['ke']}", KE, PCT2),
        ('Cost of equity — asset-risk beta', f"=DCF!$C${DF_['kea']}", KE_A, PCT2),
        ('Cost of debt — the three constructions averaged', f"=DCF!$C${DF_['kd']}", KD,
         PCT2),
        ('Cost of capital — explicit window', f"=DCF!$C${DF_['wacc']}", W_EXP, PCT2),
        ('Cost of capital — terminal', f"=DCF!$C${DF_['waccterm']}", W_TERM, PCT2),
        ('Terminal growth', f"=DCF!$C${DF_['g']}", G, PCT),
        ('Sum-of-the-parts cross-check (AED per share)',
         f"='SOTP Bridge'!$C${SB['bfv']}", SOTP_FV, PX)]
for j, (lab, fml, xp, fmt) in enumerate(_KEY):
    rw = SU['key0'] + j
    put(ws, f'A{rw}', lab, fmt=None)
    putf(ws, f'C{rw}', fml, xp, fmt, green=True)
note(ws, f"A{SU['key0']+len(_KEY)+1}", 'The terminal value share beside the discounted-cash-'
     'flow row is a live formula — the present value of the terminal value over the '
     'enterprise value of operations — and it is shown again in the equity bridge on the '
     'SOTP Bridge sheet. It is high, as it is for any long-lived asset owner whose fleet '
     'outlives the forecast window, and it is the reason the terminal cost of capital and '
     'the terminal growth rate carry more of this valuation than any single trading year.')
ANCH.update(summary_central=f"C{SU['central']}", summary_spot=f"C{SU['spot']}",
            dcf_fv=f"C{DF_['fvaed']}", dcf_fv_asset=f"C{DF_['fvaeda']}",
            summary_central_asset=f"C{SU['centrala']}")

# ============ 3 FUNDAMENTAL VALUATION (filled) ==================================
ws = wb['Fundamental Valuation']
hdr(ws, FV['hdr'], ['Lens / step', 'Basis', 'AED per share'])
_fv = [(FV['dcf'], 'Discounted cash flow (own regressed beta)',
        'links to the DCF sheet — five explicit years plus a capitalised terminal value',
        f"=DCF!$C${DF_['fvaed']}", DC['fv_aed'], True),
       (FV['dcfbear'], '  bear', 'beta 1.10, rate anchor 0.85x, capital expenditure 1.10x '
        '— a whole-model re-run', LN['dcf']['bear'], LN['dcf']['bear'], False),
       (FV['dcfbull'], '  bull', 'beta 0.55, rate anchor 1.15x, capital expenditure 0.95x '
        '— a whole-model re-run', LN['dcf']['bull'], LN['dcf']['bull'], False),
       (FV['rel'], 'Relative multiples',
        'blended enterprise and earnings multiples on 2026 earnings',
        f"='Relative & Normalized'!$C${RN['base']}", REL_BASE, True),
       (FV['norm'], 'Normalised earnings power',
        'the same multiples on the five-year average of the forecast',
        f"='Relative & Normalized'!$C${RN['nbase']}", NORM_BASE, True),
       (FV['book'], 'Book value and sustainable return',
        'justified price-to-book on the sustainable return on equity',
        f"='Relative & Normalized'!$C${RN['bbase']}", BOOK_BASE, True)]
for rw, lab, basis, val, xp, isf in _fv:
    put(ws, f'A{rw}', lab, fmt=None)
    put(ws, f'B{rw}', basis, fmt=None, wrap=True)
    ws.row_dimensions[rw].height = 28
    if isf:
        putf(ws, f'C{rw}', val, xp, PX, green=True)
    else:
        put(ws, f'C{rw}', val, BLUE, PX)
band(ws, FV['central'], 3)
put(ws, f"A{FV['central']}", 'Weighted central', bold=True, fmt=None)
putf(ws, f"C{FV['central']}", f"=Summary!$C${SU['central']}", CENTRAL, PX, bold=True,
     green=True)
band(ws, FV['cb'], 3)
put(ws, f"A{FV['cb']}", 'THE CONTESTED JUDGEMENT — TWO BETAS, BOTH CARRIED THROUGH IN FULL',
    bold=True, fmt=None)
for rw, lab, basis, fml, xp, fmt in [
        (FV['beta'], 'Beta — own-stock weekly regression',
         f"{D['beta']['n']} weekly observations, R-squared {D['beta']['r2']:.1%}, standard "
         f"error {D['beta']['se']:.3f} — the usability gate is passed",
         f"={a('beta')}", V['beta'], BETA),
        (FV['ke'], 'Cost of equity on the regressed beta',
         'normalised risk-free rate plus beta times the equity risk premium',
         f"=DCF!$C${DF_['ke']}", KE, PCT2),
        (FV['wacc'], 'Cost of capital on the regressed beta',
         'explicit window, market-value weights', f"=DCF!$C${DF_['wacc']}", W_EXP, PCT2),
        (FV['fv'], 'Fair value per share — regressed beta (AED)', 'the primary reading',
         f"=DCF!$C${DF_['fvaed']}", DC['fv_aed'], PX),
        (FV['cen'], 'Weighted central — regressed beta (AED)', 'all four lenses',
         f"=Summary!$C${SU['central']}", CENTRAL, PX),
        (FV['betaa'], 'Asset-risk beta', 'what a listed fleet owner might be expected to '
         'carry; the sector prior for a spot tanker owner is 0.9 to 1.4',
         f"={a('beta_a')}", 1.0, BETA),
        (FV['kea'], 'Cost of equity on the asset-risk beta',
         'the same construction at a beta of 1.00', f"=DCF!$C${DF_['kea']}", KE_A, PCT2),
        (FV['wacca'], 'Cost of capital on the asset-risk beta',
         'explicit window, market-value weights', f"=DCF!$C${DF_['wacca']}", W_EXP_A, PCT2),
        (FV['fva'], 'Fair value per share — asset-risk beta (AED)',
         'the alternative reading', f"=DCF!$C${DF_['fvaeda']}", DA['fv_aed'], PX),
        (FV['cena'], 'Weighted central — asset-risk beta (AED)',
         'all four lenses, the discounted-cash-flow leg swapped',
         f"=Summary!$C${SU['centrala']}", CENTRAL_A, PX)]:
    put(ws, f'A{rw}', lab, fmt=None)
    put(ws, f'B{rw}', basis, fmt=None, wrap=True)
    ws.row_dimensions[rw].height = 26
    putf(ws, f'C{rw}', fml, xp, fmt, green=True)
note(ws, f"A{FV['note']}", 'These two readings are published side by side and are never '
     'averaged into a single number. The regression passes its usability gate on the '
     'stock\'s own history, but that history is only three years long and the beta\'s own '
     'confidence interval spans more than half the point estimate, so the asset-risk '
     'reading is not a stress case — it is a second legitimate answer to the same question.')
band(ws, FV['eb'], 5)
put(ws, f"A{FV['eb']}", 'EXPERT PANEL — THREE METHODS, WORKED INDEPENDENTLY', bold=True,
    fmt=None)
hdr(ws, FV['ehdr'], ['Expert', 'Method', 'Base (AED per share)', 'Low', 'High'])
for j, k in enumerate(['e1', 'e2', 'e3']):
    e = EXP[k]
    rw = FV['e0'] + j
    put(ws, f'A{rw}', f'Expert {j+1}', fmt=None)
    put(ws, f'B{rw}', e['method_short'], fmt=None)
    put(ws, f'C{rw}', e['base'], BLUE, PX)
    put(ws, f'D{rw}', e['rng'][0], BLUE, PX)
    put(ws, f'E{rw}', e['rng'][1], BLUE, PX)
band(ws, FV['epanel'], 5)
put(ws, f"A{FV['epanel']}", 'Panel average', bold=True, fmt=None)
putf(ws, f"C{FV['epanel']}", f"=AVERAGE(C{FV['e0']}:C{FV['e0']+2})", D['panel_centre'], PX,
     bold=True)
ws.column_dimensions['B'].width = 56

# ============ notes on the Assumptions sheet ====================================
ws = wb['Assumptions']
put(ws, f"H{A['erp']}", 'No sovereign credit-default-swap entry exists for the United Arab '
    'Emirates in the country risk file, so the alternative rating-versus-swap premium basis '
    'cannot be built for this country; one basis is published rather than two.',
    fmt=None).font = SUB
put(ws, f"H{A['sofr']}", 'The Central Bank base rate of 3.65% was maintained at the 29 July '
    '2026 decision; the last change was a 25 basis point cut from 3.90% on 10 December '
    '2025.', fmt=None).font = SUB
put(ws, f"H{A['tnk_tcout']}", 'The smallest two classes have no vessels on charters out, so '
    'no fixed rate applies to them.', fmt=None).font = SUB
put(ws, f'A{ASSUMPTIONS_LAST}', 'Every figure on this sheet is an input. Nothing here is '
    'computed; everything computed from these cells lives on the sheets that follow.',
    fmt=None).font = SUB

# ============ save and verify against the committed study numbers ================
def close(x, y, tol):
    assert abs(float(x) - float(y)) <= tol, f'{x} vs {y}'


for i in range(5):
    close(REV_F[i], FC['revenue'][i], 1e-6)
    close(EB_F[i], FC['ebitda'][i], 1e-6)
    close(DNA_F[i], FC['dna'][i], 1e-6)
    close(EBIT_F[i], FC['ebit'][i], 1e-6)
    close(TAX_F[i], FC['tax'][i], 1e-6)
    close(NOPAT_F[i], FC['nopat'][i], 1e-6)
    close(NWC_F[i], FC['nwc'][i], 1e-6)
    close(DNWC_F[i], FC['dnwc'][i], 1e-6)
    close(FCFF_F[i], FC['fcff'][i], 1e-6)
    close(PPE_CLOSE[i], FC['ppe'][i], 1e-6)
    close(ND_CLOSE[i], FIN['net_debt'][i], 1e-6)
    close(GROSS_D[i], FIN['gross_debt'][i], 1e-6)
    close(INT_F[i], FIN['interest'][i], 1e-6)
    close(NPA_F[i], FIN['npa'][i], 1e-6)
    close(EQ_CLOSE[i], FBS[i]['equity_parent'], 1e-6)
    close(ROE_F[i], FBS[i]['roe'], 1e-12)
    close(ROIC_F[i], FBS[i]['roic'], 1e-12)
    close(IC_F[i], FBS[i]['invested_capital'], 1e-6)
    close(DC['df'][i], DCFB['df'][i], 1e-12)
    close(DC['pv'][i], DCFB['pv'][i], 1e-6)
    close(DA['pv'][i], DCFA['pv'][i], 1e-6)
    close(TNK_PATH['vlcc'][i], SN['market_cross_check']['vlcc_path'][i], 1e-6)
for k in ('pv_expl', 'ev_ops', 'ev', 'equity', 'fv_aed', 'tv', 'pv_tv'):
    kk = {'pv_expl': 'pv_explicit', 'ev_ops': 'ev_ops', 'ev': 'ev', 'equity': 'equity',
          'fv_aed': 'fv_aed', 'tv': 'tv', 'pv_tv': 'pv_tv'}[k]
    close(DC[k], DCFB[kk], 1e-6)
    close(DA[k], DCFA[kk], 1e-6)
close(DC['tv_share'], DCFB['tv_share'], 1e-12)
close(DA['tv_share'], DCFA['tv_share'], 1e-12)
close(W_EXP, WACC['wacc'], 1e-12); close(W_TERM, WACC['wacc_term'], 1e-12)
close(KE, WACC['ke'], 1e-12); close(KE_A, WACC['ke_beta1'], 1e-12)
close(KD, WACC['kd'], 1e-12); close(KD1, WACC['kd_method1'], 1e-12)
close(KD2, WACC['kd_method2'], 1e-12); close(KD3, WACC['kd_method3'], 1e-12)
close(WE, WACC['we'], 1e-12); close(MKTCAP, WACC['mktcap'], 1e-6)
close(REL_BASE, LN['relative']['base'], 1e-9)
close(REL_BEAR, LN['relative']['bear'], 1e-9)
close(REL_BULL, LN['relative']['bull'], 1e-9)
close(NORM_BASE, LN['normalized']['base'], 1e-9)
close(NORM_BEAR, LN['normalized']['bear'], 1e-9)
close(NORM_BULL, LN['normalized']['bull'], 1e-9)
close(BOOK_BASE, LN['book']['base'], 1e-9)
close(BOOK_BEAR, LN['book']['bear'], 1e-9)
close(BOOK_BULL, LN['book']['bull'], 1e-9)
close(ROE_SUST, BK['roe_sustainable'], 1e-12)
close(PB_FAIR, BK['pb_fair'], 1e-12)
close(BVPS0, BK['bvps_usd'], 1e-12)
close(VSB_RATIO, BK['vessel_value_to_book'], 1e-12)
close(CENTRAL, D['central'], 1e-9)
close(CENTRAL_A, D['central_asset_beta'], 1e-9)
close(CENTRAL_BEAR, LN['central']['bear'], 1e-9)
close(CENTRAL_BULL, LN['central']['bull'], 1e-9)
close(BLEND_EV, REL['blend_ev_ebitda'], 1e-12)
close(BLEND_PE, REL['blend_pe'], 1e-12)
close(OWN_EVEB_TTM, REL['own_ev_ebitda_ttm'], 1e-9)
close(OWN_EVEB_26, REL['own_ev_ebitda_26'], 1e-9)
close(OWN_PE_TTM, REL['own_pe_ttm'], 1e-9)
close(OWN_PB, REL['own_pb'], 1e-9)
close(OWN_DY, REL['own_dy'], 1e-12)
close(SOTP_EVOPS, SOTP['ev_ops'], 1e-6)
close(SOTP_EQ, SOTP['equity'], 1e-6)
close(SOTP_FV, SOTP['fv_aed'], 1e-9)
for j, g in enumerate(GROUPS):
    close(SOTP_EV[g], SOTP['legs'][j]['ev'], 1e-6)
    close(GRP_EB_F[g][0], SOTP['legs'][j]['ebitda_26'], 1e-6)
for i in range(5):
    for s in SEGS:
        close(SEG_REV_F[s][i], D['fcst_seg'][s]['rev'][i], 1e-6)
        close(SEG_EB_F[s][i], D['fcst_seg'][s]['ebitda'][i], 1e-6)

out = os.path.join(HERE, 'ADNOCLS_Valuation_Model_09082026_public.xlsx')
wb.save(out)
json.dump({'expected': EXPECT, 'anchors': ANCH},
          open(os.path.join(HERE, 'xlsx_expected.json'), 'w'), indent=1)
nchk = sum(len(v) for v in EXPECT.values())
nform = nlit = 0
per = {}
for s in wb.worksheets:
    f_ = l_ = 0
    for row in s.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith('='):
                f_ += 1
            elif isinstance(c.value, (int, float)):
                l_ += 1
    per[s.title] = (f_, l_); nform += f_; nlit += l_
print(f'wrote {out} | {len(wb.sheetnames)} sheets: {wb.sheetnames}')
for k, (f_, l_) in per.items():
    print(f'  {k:24s} formulas {f_:5d}   pasted numeric {l_:5d}')
print(f'formulas: {nform} (of which {nchk} carry a checked expected value) | '
      f'numeric literals: {nlit}')
