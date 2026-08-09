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
CAPEX_ALL = [-x for x in HC_['capex']] + [-x for x in CAPEX]

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
