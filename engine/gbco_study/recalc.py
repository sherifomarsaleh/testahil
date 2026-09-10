#!/usr/bin/env python3
"""Recalculate the DELIVERED GBCO workbook and reconcile it, cell by cell, against the study.

WHY THIS EXISTS AND WHY IT IS NEW. Until this rebuild GBCO carried no recalculation at all
and was listed on the workbook-values ratchet for exactly that: "no recalculation script in
the study directory". A clean-looking workbook is not evidence, and the workbook it would
have been checking was publishing a superseded construction — a four-lens weighted blend, a
conglomerate discount and one side of a two-sided answer — while the study beside it had
moved on. Nothing compared them, because nothing could.

THE FILE IS RESOLVED BY THE DATE IN ITS NAME, NEVER BY A STRING SORT AND NEVER BY A NAME
TYPED HERE [L-066/L-067]. A check that opens a delivered file by name moves with the
re-issue; two of another study's gates once opened a superseded workbook and reported clean.

FOUR GATES, IN INCREASING STRENGTH.

  1. EVERY formula in the workbook must evaluate, through the explicit evaluator in
     xlcalc.py rather than through the library that wrote the file. Anything unparseable is
     a FAILURE, never a skip: a permissive verifier is worse than no verifier.

  2. EVERY formula cell must reproduce a value computed HERE, from the study's committed
     drivers, by an independent reimplementation that never reads the workbook's own
     formulas — and NO formula cell may be left unchecked. The historical columns are the
     one place this reads the workbook, and it reads its INPUT cells only: the disclosed
     FY2023-FY2025 figures are the givens, and what is under test is the arithmetic the
     workbook performs on them.

  3. The balance sheet's check row must be CONSTANT across the forecast rather than zero.
     The company's own grouped segment balance sheets carry a 0.1 rounding at FY2024 and
     FY2025, and a forecast that closes carries an opening difference forward unchanged.
     Asserting zero would have forced a disclosed figure to be edited to make a check pass.

  4. A hand-written set of headline reconciliations against study_numbers.json — both
     branches of the two-sided answer, every leg behind them, the envelope, the cross-checks
     and the cost-of-capital chain — as an independent read on gate 2's own expectations.
"""
import glob
import json
import os
import re
import sys

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import xlcalc                                                         # noqa: E402

_DATE = re.compile(r'_(\d{2})(\d{2})(\d{4})_')


def delivered():
    """The LATEST edition by the DATE inside the filename, never by sorting the string."""
    cands = [f for f in glob.glob(os.path.join(HERE, 'GBCO_Valuation_Model_*_public.xlsx'))
             if not os.path.basename(f).startswith('~$')]
    if not cands:
        raise SystemExit('no delivered workbook on disk — nothing to check')
    def key(f):
        m = _DATE.search(os.path.basename(f))
        if not m:
            raise SystemExit('a delivered workbook whose name carries no date: %s' % f)
        d, mo, y = m.groups()
        return (y, mo, d)
    return max(cands, key=key)


XLSX = delivered()
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
ASM = json.load(open(os.path.join(HERE, '_asm_rows.json')))
SEG = json.load(open(os.path.join(HERE, '_seg_rows.json')))
ISR = json.load(open(os.path.join(HERE, '_is_rows.json')))
BSJ = json.load(open(os.path.join(HERE, '_bs_rows.json')))
CFJ = json.load(open(os.path.join(HERE, '_cf_rows.json')))
DCJ = json.load(open(os.path.join(HERE, '_dcf_rows.json')))
ANS = json.load(open(os.path.join(HERE, '_ans_rows.json')))
BS = BSJ['BS']; CF = CFJ['CF']; DC = DCJ['DC']

wb = openpyxl.load_workbook(XLSX)
BK = xlcalc.Book(wb)
cv = BK.cell_value
HCOLS = ['B', 'C', 'D']
FCOLS = ['E', 'F', 'G', 'H', 'I']
DCOLS = ['B', 'C', 'D', 'E', 'F']          # the DCF sheet's five forecast columns


def raw(sheet, coord):
    """A DISCLOSED input cell, read as it stands. Never a formula — if it is one, the
    caller has asked this checker to take an answer from the thing it is checking."""
    v = wb[sheet][coord].value
    if isinstance(v, str) and v.startswith('='):
        raise SystemExit('%s!%s is a formula and was read as an input' % (sheet, coord))
    return float(v) if v is not None else 0.0


# =====================================================================================
# THE INDEPENDENT MODEL — built from the study's committed drivers, never from the sheet
# =====================================================================================
SH = D['shares']; TAX = D['disclosed_drivers']['cost_stack']['tax_rate']
SPOT = D['spot']
DD = D['disclosed_drivers']; CS = DD['cost_stack']; GD = D['group_forecast']['drivers']
COC = D['cost_of_capital_record']; RB = D['cost_of_capital_rating_basis']
CAPI = D['lens_inputs']['capital']; REL = D['lens_inputs']['relative']
G = DD['growth']

# ---- the auto leg, units x average selling price -----------------------------------
pc_vol, pc_asp, pc_rev = [], [], []
v = raw('Segments', 'D%d' % SEG['PC volume (units)'])
a = (raw('Segments', 'D%d' % SEG['PC revenue']) / v)
for i in range(5):
    v *= 1 + G['pc_volume'][i]; a *= 1 + G['pc_asp'][i]
    pc_vol.append(v); pc_asp.append(a); pc_rev.append(v * a)
cv_vol, cv_rev = [], []
v = raw('Segments', 'D%d' % SEG['CV&CE volume (units)'])
x = raw('Segments', 'D%d' % SEG['CV&CE revenue'])
for i in range(5):
    v *= 1 + G['cv_volume'][i]
    x *= (1 + G['cv_volume'][i]) * (1 + G['cv_asp'][i])
    cv_vol.append(v); cv_rev.append(x)
lm_vol, lm_rev = [], []
v = raw('Segments', 'D%d' % SEG['Light-Mobility volume (units)'])
x = raw('Segments', 'D%d' % SEG['Light-Mobility revenue'])
for i in range(5):
    v *= 1 + G['lm_volume'][i]
    x *= (1 + G['lm_volume'][i]) * (1 + G['lm_asp'][i])
    lm_vol.append(v); lm_rev.append(x)
tr_rev = []
x = raw('Segments', 'D%d' % SEG['Trading revenue (tires + parts)'])
for i in range(5):
    x *= 1 + G['trading'][i]
    tr_rev.append(x)
auto_rev = [pc_rev[i] + cv_rev[i] + lm_rev[i] + tr_rev[i] for i in range(5)]
auto_gp = [auto_rev[i] * CS['gross_margin'][i] for i in range(5)]
auto_ebit = [auto_gp[i] - auto_rev[i] * CS['gsa_pct'][i]
             + auto_rev[i] * CS['other_income_pct']
             + auto_rev[i] * CS['provisions_pct'] for i in range(5)]
auto_dna = [auto_rev[i] * CS['dna_pct'][i] for i in range(5)]
auto_ebitda = [auto_ebit[i] + auto_dna[i] for i in range(5)]

cap_rev = []
x = GD['capital_revenue_fy2025']
for i in range(5):
    x *= 1 + GD['capital_growth'][i]
    cap_rev.append(x)
elim = [-(auto_rev[i] + cap_rev[i]) * GD['eliminations_pct'][i] for i in range(5)]
grp_rev = [auto_rev[i] + cap_rev[i] + elim[i] for i in range(5)]
grp_gp = [auto_gp[i] + cap_rev[i] * GD['capital_gross_margin'][i] + elim[i] * 0.2
          for i in range(5)]
grp_sga = [-grp_rev[i] * GD['group_opex_pct'][i] for i in range(5)]
grp_oth = [grp_rev[i] * GD['group_other_income_pct'][i] for i in range(5)]
grp_prov = [grp_rev[i] * GD['group_provisions_pct'][i] for i in range(5)]
grp_op = [grp_gp[i] + grp_sga[i] + grp_oth[i] + grp_prov[i] for i in range(5)]
grp_assoc = list(GD['associates_income'])
grp_ebit = [grp_op[i] + grp_assoc[i] for i in range(5)]
grp_dna = [auto_dna[i] + GD['capital_dna'][i] for i in range(5)]
grp_ebitda = [grp_ebit[i] + grp_dna[i] for i in range(5)]
grp_fx = [0.0] * 5
grp_fin = list(GD['net_finance_cost'])
grp_ebt = [grp_ebit[i] + grp_fx[i] + grp_fin[i] for i in range(5)]
grp_tax = [-grp_ebt[i] * TAX for i in range(5)]
grp_npbmi = [grp_ebt[i] + grp_tax[i] for i in range(5)]
grp_mi = [grp_npbmi[i] * GD['minority_pct'][i] for i in range(5)]
grp_np = [grp_npbmi[i] + grp_mi[i] for i in range(5)]

# ---- the balance sheet roll-forward and the cash flow -------------------------------
# EIGHT COLUMNS THROUGHOUT: FY2023, FY2024 and FY2025 as disclosed, then five forecast
# years. The three historical columns are read as INPUTS; every forecast column is
# recomputed here from the committed drivers.
B_ = 'Balance Sheet'
NONAUTO = raw(B_, 'B%d' % BSJ['NONAUTO'])


def hist3(row):
    return [raw(B_, '%s%d' % (c, row)) for c in HCOLS]


ppe = hist3(BS['PP&E, intangibles, right-of-use & investment property'])
assoc_bs = hist3(BS['Investments in associates (MNT-Halan, Bedaya, Kaf)'])
loan = hist3(BS['GB Capital loan book (on balance sheet)'])
inv = hist3(BS['Inventories'])
rec = hist3(BS['Trade receivables — Auto'])
adv = hist3(BS['Advances, debtors & other current'])
cash = hist3(BSJ['CASH'])
othassets = hist3(BS['Other assets (deferred tax, held-for-sale, miscellaneous)'])
eq = hist3(BSJ['EQ'])
nci = hist3(BS['Non-controlling interests'])
borrow = hist3(BS['Borrowings (loans, overdrafts & bonds)'])
pay = hist3(BSJ['PAY'])
lease = hist3(BS['Lease obligations'])
prov_bs = hist3(BS['Provisions'])
othliab = hist3(BS['Other liabilities'])
dtl = hist3(BS['Deferred tax liabilities'])

for i in range(5):
    inv.append(auto_rev[i] * GD['auto_inventory_pct'][i])
    rec.append(auto_rev[i] * GD['auto_receivables_pct'][i])
    adv.append(auto_rev[i] * GD['auto_advances_pct'][i])
    pay.append(auto_rev[i] * GD['auto_payables_pct'][i] + NONAUTO)
    lease.append(lease[-1]); prov_bs.append(prov_bs[-1])
    othliab.append(othliab[-1]); dtl.append(dtl[-1]); othassets.append(othassets[-1])
    ppe.append(ppe[-1] + CS['capex'][i] + GD['rental_and_other_capex'][i] - grp_dna[i])
    assoc_bs.append(assoc_bs[-1] + grp_assoc[i])
    loan.append(loan[-1] * (1 + GD['capital_loanbook_growth'][i]))
    nci.append(nci[-1] - grp_mi[i])
    borrow.append(borrow[-1] + GD['net_new_borrowings'][i])
nwc = [inv[i] + rec[i] + adv[i] - (pay[i] - NONAUTO) for i in range(8)]
dnwc = [nwc[3 + i] - nwc[2 + i] for i in range(5)]

cf_np = list(grp_npbmi); cf_dna = list(grp_dna)
cf_assoc = [-grp_assoc[i] for i in range(5)]
cf_dnwc = [-dnwc[i] for i in range(5)]
cf_dloan = [-(loan[3 + i] - loan[2 + i]) for i in range(5)]
cf_ocf = [cf_np[i] + cf_dna[i] + cf_assoc[i] + cf_dnwc[i] + cf_dloan[i] for i in range(5)]
cf_capex = [-(CS['capex'][i] + GD['rental_and_other_capex'][i]) for i in range(5)]
cf_fcf = [cf_ocf[i] + cf_capex[i] for i in range(5)]
cf_borrow = list(GD['net_new_borrowings'])
cf_div = [-grp_np[i] * GD['dividend_payout'][i] for i in range(5)]
cf_delta = [cf_fcf[i] + cf_borrow[i] + cf_div[i] for i in range(5)]
cf_open, cf_close = [], []
c0 = cash[2]
for i in range(5):
    cf_open.append(c0); c0 += cf_delta[i]; cf_close.append(c0); cash.append(c0)
for i in range(5):
    eq.append(eq[-1] + grp_np[i] + cf_div[i])
tot_eq = [eq[i] + nci[i] for i in range(8)]
ta = [ppe[i] + assoc_bs[i] + loan[i] + inv[i] + rec[i] + adv[i] + cash[i] + othassets[i]
      for i in range(8)]
tle = [tot_eq[i] + borrow[i] + pay[i] + lease[i] + prov_bs[i] + othliab[i] + dtl[i]
       for i in range(8)]
chk = [ta[i] - tle[i] for i in range(8)]
netdebt = [borrow[i] - cash[i] for i in range(8)]

# ---- the cost of capital, the DCF and the three legs --------------------------------
# THE FIFTH PLACE THIS IDENTITY WAS WRITTEN OUT BY HAND, and the fourth to be
# left behind when the construction changed. rf* + beta x ERP_total multiplies
# the country premium by beta; [R-COC-03] charges it once, flat, at the weight of
# the operations. This gate is supposed to prove the workbook reproduces the
# model, so a private re-derivation here proves only that two wrong things agree.
# The record publishes its own components; read them.
ke = (COC['rf_star'] + COC['beta'] * COC['erp_mature'] + COC['crp_effective'])
kd_at = COC['kd_pretax'] * (1 - TAX)
wacc1 = (1 - COC['weight_debt']) * ke + COC['weight_debt'] * kd_at
# The alternative basis splits the same way; it was the sixth hand-written copy of
# the retired identity in this study alone.
ke_alt = (RB['rf_star'] + COC['beta'] * RB['erp_mature'] + RB['crp_effective'])
wacc_alt = (1 - COC['weight_debt']) * ke_alt + COC['weight_debt'] * kd_at
TG = D['macro']['terminal_growth_nominal']
fwd = COC['forward_wacc']; wacc_T = COC['wacc_terminal']
df = []
c = 1.0
for i in range(5):
    c /= (1 + fwd[i]); df.append(c)
nopat = [auto_ebit[i] * (1 - TAX) for i in range(5)]
fcff = [nopat[i] + auto_dna[i] - CS['capex'][i] - dnwc[i] for i in range(5)]
pv = [fcff[i] * df[i] for i in range(5)]
pv_sum = sum(pv)
tv = fcff[4] * (1 + TG) / (wacc_T - TG)
pv_tv = tv * df[4]
ev = pv_sum + pv_tv
auto_nd = D['dcf']['auto_nd']; auto_nci = D['dcf']['auto_nci']
auto_eq = ev - auto_nd - auto_nci
evpp = 0.01 * (1 - TAX) * (sum(auto_rev[i] * df[i] for i in range(5))
                           + auto_rev[4] * (1 + TG) / (wacc_T - TG) * df[4])

cap_opeq = CAPI['segment_equity_before_nci'] - CAPI['associates_carried_within']
cap_opeq_d25 = 18312.6 - 15732.426
roe_h1 = (649.6 - 426.2) * 2 / ((cap_opeq_d25 + cap_opeq) / 2)
roe_fy25 = (1365.9 - 986.4) / cap_opeq_d25
ke_T = (COC['rf_terminal'] + COC['beta'] * COC['erp_mature']
        + COC['crp_effective_terminal'])
pb = (roe_h1 - TG) / (ke_T - TG)
capleg = cap_opeq * pb
capleg_fy25 = cap_opeq * ((roe_fy25 - TG) / (ke_T - TG))

mnt_a = (D['sotp']['mnt_halan_round_usd'] * D['sotp']['mnt_halan_stake']
         * D['sotp']['egp_usd'])
mnt_b = D['lens_record']['primary']['range_basis']['low']
oth_assoc = CAPI['associates_carried_within'] - mnt_b
assoc_a = mnt_a + oth_assoc
assoc_b = mnt_b + oth_assoc
sotp_a = auto_eq + capleg + assoc_a
sotp_b = auto_eq + capleg + assoc_b
ps_a = sotp_a / SH
ps_b = sotp_b / SH

eps_hist = {y: REL['history'][y][1] / SH for y in ('2023', '2024', '2025')}
pe_hist = {y: REL['history'][y][0] / eps_hist[y] for y in ('2023', '2024', '2025')}
pe_med = sorted(pe_hist.values())[1]
eps26 = grp_np[0] / SH
rel_ps = eps26 * pe_med
traded_pe = SPOT * SH / grp_np[0]
book = D['experts']['e2']['book']
bvps = book / SH
env_lo = min(ps_b, ps_a, rel_ps)
env_hi = max(ps_b, ps_a, rel_ps)

# ---- the two sensitivity grids ------------------------------------------------------
SHIFTS = ANS['SENS']['shifts']; TGS = ANS['SENS']['tgs']
# THE MARK LEVELS ARE THE ONES SOMEBODY ARGUED FOR, in the order the builder writes them:
# the two haircuts this study's own expert panel puts on a private mark, then the two
# branches. They are deliberately NOT equal steps between the branches, because an equal
# step would land on the average of two disclosures only one of which can be right.
marks = sorted([mnt_a * h for h in ANS['SENS']['haircuts']] + [mnt_b, mnt_a])
grid1 = [[(ev + s * 100 * evpp - auto_nd - auto_nci + capleg + marks[k] + oth_assoc) / SH
          for k in range(len(marks))] for s in D['sens']['grid_margin']]
help_df, help_wt, grid2 = [], [], []
for s in SHIFTS:
    f, c = [], 1.0
    for i in range(5):
        c /= (1 + fwd[i] + s); f.append(c)
    help_df.append(f); help_wt.append(wacc_T + s)
for i, s in enumerate(SHIFTS):
    row = []
    for t in TGS:
        g = TG + t
        p = sum(fcff[k] * help_df[i][k] for k in range(5))
        tvx = fcff[4] * (1 + g) / (help_wt[i] - g) * help_df[i][4]
        row.append((p + tvx - auto_nd - auto_nci + capleg + assoc_a) / SH)
    grid2.append(row)

# =====================================================================================
# THE EXPECTED MAP — every formula cell in the workbook, addressed by the row the builder
# recorded and valued by the model above
# =====================================================================================
E = {}


def setrow(sheet, row, cols, vals):
    for c, v in zip(cols, vals):
        if v is not None:
            E[(sheet, '%s%d' % (c, row))] = float(v)


def one(sheet, coord, v):
    E[(sheet, coord)] = float(v)


A = ASM
one('Assumptions', 'B%d' % A['Cost of equity Ke = rf* + beta x mature premium + country premium'], ke)
one('Assumptions', 'B%d' % A['After-tax cost of debt'], kd_at)
one('Assumptions', 'B%d' % A['WACC — first forecast year'], wacc1)
one('Assumptions', 'B%d' % A['GB Capital operating equity'], cap_opeq)
one('Assumptions', 'B%d' % A['GB Capital operating equity, 31 December 2025'], cap_opeq_d25)
one('Assumptions', 'B%d' % A['Return on operating equity — 1H2026 annualised (ADOPTED)'], roe_h1)
one('Assumptions', 'B%d' % A['Return on operating equity — FY2025 framing'], roe_fy25)
one('Assumptions', 'B%d' % A['Terminal cost of equity Ke(T) = rf(T) + beta x mature premium + country premium'], ke_T)
one('Assumptions', 'B%d' % A['Justified price-to-book = (ROE - g) / (Ke(T) - g)'], pb)
one('Assumptions', 'B%d' % A['GB Capital lending leg (EGP mn)'], capleg)
one('Assumptions', 'B%d' % A['memo: the same leg on the FY2025 return framing'], capleg_fy25)
one('Assumptions', 'B%d' % A['memo: GB Capital operating equity per share — a DISCLOSED FLOOR, '
                             'never weighted'], cap_opeq / SH)
one('Assumptions', 'B%d' % A['BRANCH A — MNT-Halan at the June-2026 round price'], mnt_a)
one('Assumptions', 'B%d' % A["Other associates (Bedaya, Kaf) — by identity off the note's own total"],
    oth_assoc)
one('Assumptions', 'B%d' % A['Associates — branch A (round price)'], assoc_a)
one('Assumptions', 'B%d' % A['Associates — branch B (reviewed carrying value)'], assoc_b)
one('Assumptions', 'B%d' % A['Cost of equity, alternative (rating-basis premium)'], ke_alt)
one('Assumptions', 'B%d' % A['Weighted cost of capital, alternative (rating-basis premium)'], wacc_alt)

S = 'Segments'
hpcv = [raw(S, '%s%d' % (c, SEG['PC volume (units)'])) for c in HCOLS]
hpcr = [raw(S, '%s%d' % (c, SEG['PC revenue'])) for c in HCOLS]
hcvr = [raw(S, '%s%d' % (c, SEG['CV&CE revenue'])) for c in HCOLS]
hlmr = [raw(S, '%s%d' % (c, SEG['Light-Mobility revenue'])) for c in HCOLS]
htrr = [raw(S, '%s%d' % (c, SEG['Trading revenue (tires + parts)'])) for c in HCOLS]
hautor = [raw(S, '%s%d' % (c, SEG['GB Auto total revenue'])) for c in HCOLS]
hcapr = [raw(S, '%s%d' % (c, SEG['GB Capital revenue'])) for c in HCOLS]
hgrpr = [raw(S, '%s%d' % (c, SEG['Group revenue'])) for c in HCOLS]
hagp = [raw(S, '%s%d' % (c, SEG['Auto gross profit'])) for c in HCOLS]
haebit = [raw(S, '%s%d' % (c, SEG['Auto EBIT (operating profit)'])) for c in HCOLS]
hadna = [raw(S, '%s%d' % (c, SEG['Auto D&A'])) for c in HCOLS]
setrow(S, SEG['PC volume (units)'], FCOLS, pc_vol)
setrow(S, SEG['PC revenue'], FCOLS, pc_rev)
setrow(S, SEG['PC ASP (EGP mn/unit)'], HCOLS, [hpcr[i] / hpcv[i] for i in range(3)])
setrow(S, SEG['PC ASP (EGP mn/unit)'], FCOLS, pc_asp)
setrow(S, SEG['CV&CE volume (units)'], FCOLS, cv_vol)
setrow(S, SEG['CV&CE revenue'], FCOLS, cv_rev)
setrow(S, SEG['Light-Mobility volume (units)'], FCOLS, lm_vol)
setrow(S, SEG['Light-Mobility revenue'], FCOLS, lm_rev)
setrow(S, SEG['Trading revenue (tires + parts)'], FCOLS, tr_rev)
setrow(S, SEG['Other Auto / after-sales & regional adj.'], HCOLS,
       [hautor[i] - hpcr[i] - hcvr[i] - hlmr[i] - htrr[i] for i in range(3)])
setrow(S, SEG['Other Auto / after-sales & regional adj.'], FCOLS, [0.0] * 5)
setrow(S, SEG['GB Auto total revenue'], FCOLS, auto_rev)
setrow(S, SEG['GB Capital revenue'], FCOLS, cap_rev)
setrow(S, SEG['Intercompany eliminations'], HCOLS,
       [hgrpr[i] - hautor[i] - hcapr[i] for i in range(3)])
setrow(S, SEG['Intercompany eliminations'], FCOLS, elim)
setrow(S, SEG['Group revenue'], FCOLS, grp_rev)
setrow(S, SEG['Auto gross profit'], FCOLS, auto_gp)
setrow(S, SEG['Auto gross margin'], HCOLS, [hagp[i] / hautor[i] for i in range(3)])
setrow(S, SEG['Auto gross margin'], FCOLS, [auto_gp[i] / auto_rev[i] for i in range(5)])
setrow(S, SEG['Auto EBIT (operating profit)'], FCOLS, auto_ebit)
setrow(S, SEG['Auto D&A'], FCOLS, auto_dna)
setrow(S, SEG['Auto EBITDA'], HCOLS, [haebit[i] + hadna[i] for i in range(3)])
setrow(S, SEG['Auto EBITDA'], FCOLS, auto_ebitda)
setrow(S, SEG['Auto EBITDA margin'], HCOLS,
       [(haebit[i] + hadna[i]) / hautor[i] for i in range(3)])
setrow(S, SEG['Auto EBITDA margin'], FCOLS,
       [auto_ebitda[i] / auto_rev[i] for i in range(5)])

S = 'DCF'
setrow(S, DC['Auto revenue'], DCOLS, auto_rev)
setrow(S, DC['EBITDA'], DCOLS, auto_ebitda)
setrow(S, DC['D&A'], DCOLS, [-x for x in auto_dna])
setrow(S, DC['EBIT'], DCOLS, auto_ebit)
setrow(S, DC['NOPAT = EBIT x (1 - tax)'], DCOLS, nopat)
setrow(S, DC['+ D&A'], DCOLS, auto_dna)
setrow(S, DC['- Capex'], DCOLS, [-x for x in CS['capex']])
setrow(S, DC['- Increase in net working capital'], DCOLS, [-x for x in dnwc])
setrow(S, DC['FCFF'], DCOLS, fcff)
setrow(S, DC['Discount factor (cumulative on the schedule)'], DCOLS, df)
setrow(S, DC['PV of FCFF'], DCOLS, pv)
one(S, 'B%d' % DCJ['SPV'], pv_sum)
one(S, 'B%d' % DCJ['TVR'], tv)
one(S, 'B%d' % DCJ['PVT'], pv_tv)
one(S, 'B%d' % DCJ['EVR'], ev)
one(S, 'B%d' % DC['Terminal share of enterprise value'], pv_tv / ev)
one(S, 'B%d' % DC['less: GB Auto net debt (30 June 2026)'], -auto_nd)
one(S, 'B%d' % DC['less: GB Auto non-controlling interests'], -auto_nci)
one(S, 'B%d' % DCJ['AEQ'], auto_eq)
one(S, 'B%d' % DC['check: year-1 forward rate less the WACC built on Assumptions'],
    fwd[0] - wacc1)
one(S, 'B%d' % DCJ['EVPP'], evpp)

S = 'Income Statement'
I = ISR
hrev = [raw(S, '%s%d' % (c, I['Gross profit'])) for c in HCOLS]
setrow(S, I['GB Auto revenue'], HCOLS, hautor); setrow(S, I['GB Auto revenue'], FCOLS, auto_rev)
setrow(S, I['GB Capital revenue'], HCOLS, hcapr); setrow(S, I['GB Capital revenue'], FCOLS, cap_rev)
setrow(S, I['Intercompany eliminations'], HCOLS,
       [hgrpr[i] - hautor[i] - hcapr[i] for i in range(3)])
setrow(S, I['Intercompany eliminations'], FCOLS, elim)
setrow(S, I['Total revenue'], HCOLS, hgrpr); setrow(S, I['Total revenue'], FCOLS, grp_rev)
setrow(S, I['Gross profit'], FCOLS, grp_gp)
setrow(S, I['Gross profit margin'], HCOLS, [hrev[i] / hgrpr[i] for i in range(3)])
setrow(S, I['Gross profit margin'], FCOLS, [grp_gp[i] / grp_rev[i] for i in range(5)])
setrow(S, I['Selling, marketing & administration'], FCOLS, grp_sga)
setrow(S, I['Other operating income'], FCOLS, grp_oth)
setrow(S, I['Provisions (net)'], FCOLS, grp_prov)
hsga = [raw(S, '%s%d' % (c, I['Selling, marketing & administration'])) for c in HCOLS]
hoth = [raw(S, '%s%d' % (c, I['Other operating income'])) for c in HCOLS]
hprv = [raw(S, '%s%d' % (c, I['Provisions (net)'])) for c in HCOLS]
hop = [hrev[i] + hsga[i] + hoth[i] + hprv[i] for i in range(3)]
setrow(S, I['Operating profit'], HCOLS, hop); setrow(S, I['Operating profit'], FCOLS, grp_op)
hass = [raw(S, '%s%d' % (c, I['Investment gains from associates'])) for c in HCOLS]
setrow(S, I['Investment gains from associates'], FCOLS, grp_assoc)
hebit = [hop[i] + hass[i] for i in range(3)]
setrow(S, I['EBIT'], HCOLS, hebit); setrow(S, I['EBIT'], FCOLS, grp_ebit)
setrow(S, I['Group D&A'], FCOLS, grp_dna)
hdna25 = raw(S, 'D%d' % I['Group D&A'])
one(S, 'D%d' % I['EBITDA (EBIT + D&A)'], hebit[2] + hdna25)
setrow(S, I['EBITDA (EBIT + D&A)'], FCOLS, grp_ebitda)
setrow(S, I['Foreign exchange gains (losses)'], FCOLS, grp_fx)
setrow(S, I['Net finance cost'], FCOLS, grp_fin)
hfx = [raw(S, '%s%d' % (c, I['Foreign exchange gains (losses)'])) for c in HCOLS]
hfin = [raw(S, '%s%d' % (c, I['Net finance cost'])) for c in HCOLS]
hebt = [hebit[i] + hfx[i] + hfin[i] for i in range(3)]
setrow(S, I['Earnings before tax'], HCOLS, hebt); setrow(S, I['Earnings before tax'], FCOLS, grp_ebt)
setrow(S, I['Income taxes'], FCOLS, grp_tax)
htax = [raw(S, '%s%d' % (c, I['Income taxes'])) for c in HCOLS]
hnpbmi = [hebt[i] + htax[i] for i in range(3)]
setrow(S, I['Net profit before minority interest'], HCOLS, hnpbmi)
setrow(S, I['Net profit before minority interest'], FCOLS, grp_npbmi)
setrow(S, I['Minority interest'], FCOLS, grp_mi)
hmi = [raw(S, '%s%d' % (c, I['Minority interest'])) for c in HCOLS]
hnp = [hnpbmi[i] + hmi[i] for i in range(3)]
setrow(S, I['Net profit (attributable)'], HCOLS, hnp)
setrow(S, I['Net profit (attributable)'], FCOLS, grp_np)
setrow(S, I['Net profit margin'], HCOLS, [hnp[i] / hgrpr[i] for i in range(3)])
setrow(S, I['Net profit margin'], FCOLS, [grp_np[i] / grp_rev[i] for i in range(5)])

S = 'Balance Sheet'
setrow(S, BS['PP&E, intangibles, right-of-use & investment property'], FCOLS, ppe[3:])
setrow(S, BS['Investments in associates (MNT-Halan, Bedaya, Kaf)'], FCOLS, assoc_bs[3:])
setrow(S, BS['GB Capital loan book (on balance sheet)'], FCOLS, loan[3:])
setrow(S, BS['Inventories'], FCOLS, inv[3:])
setrow(S, BS['Trade receivables — Auto'], FCOLS, rec[3:])
setrow(S, BS['Advances, debtors & other current'], FCOLS, adv[3:])
setrow(S, BSJ['CASH'], FCOLS, cash[3:])
setrow(S, BS['Other assets (deferred tax, held-for-sale, miscellaneous)'], FCOLS, othassets[3:])
setrow(S, BSJ['TA'], HCOLS + FCOLS, ta)
setrow(S, BSJ['EQ'], FCOLS, eq[3:])
setrow(S, BS['Non-controlling interests'], FCOLS, nci[3:])
setrow(S, BS['Total equity'], HCOLS + FCOLS, tot_eq)
setrow(S, BS['Borrowings (loans, overdrafts & bonds)'], FCOLS, borrow[3:])
setrow(S, BSJ['PAY'], FCOLS, pay[3:])
setrow(S, BS['Lease obligations'], FCOLS, lease[3:])
setrow(S, BS['Provisions'], FCOLS, prov_bs[3:])
setrow(S, BS['Other liabilities'], FCOLS, othliab[3:])
setrow(S, BS['Deferred tax liabilities'], FCOLS, dtl[3:])
setrow(S, BSJ['TLE'], HCOLS + FCOLS, tle)
setrow(S, BSJ['CHK'], HCOLS + FCOLS, chk)
setrow(S, BSJ['ND'], HCOLS + FCOLS, netdebt)
setrow(S, BSJ['NWC'], HCOLS + FCOLS, nwc)
setrow(S, BSJ['DNWC'], FCOLS, dnwc)

S = 'Cash Flow'
setrow(S, CF['Net profit before minority interest'], FCOLS, cf_np)
setrow(S, CF['+ D&A'], FCOLS, cf_dna)
setrow(S, CF['- Associates income (non-cash)'], FCOLS, cf_assoc)
setrow(S, CF['- Increase in net Auto working capital'], FCOLS, cf_dnwc)
setrow(S, CF['- Increase in the GB Capital loan book'], FCOLS, cf_dloan)
setrow(S, CF['Operating cash flow'], FCOLS, cf_ocf)
setrow(S, CF['- Capex (Auto + rental fleet)'], FCOLS, cf_capex)
setrow(S, CF['Free cash flow'], FCOLS, cf_fcf)
setrow(S, CF['+ Increase in borrowings (net)'], FCOLS, cf_borrow)
setrow(S, CF['- Dividends paid'], FCOLS, cf_div)
setrow(S, CF['Net change in cash'], FCOLS, cf_delta)
setrow(S, CFJ['OPEN'], FCOLS, cf_open)
setrow(S, CFJ['CLOSE'], FCOLS, cf_close)

S = 'SOTP Bridge'
for col, leg, ass, tot in (('C', auto_eq, assoc_b, sotp_b), ('D', auto_eq, assoc_a, sotp_a)):
    one(S, '%s6' % col, leg); one(S, '%s7' % col, capleg); one(S, '%s8' % col, ass)
    one(S, '%s9' % col, tot); one(S, '%s10' % col, SH); one(S, '%s11' % col, tot / SH)
    one(S, '%s12' % col, SPOT); one(S, '%s13' % col, tot / SH / SPOT - 1)
mrow = ANS['SOTP']['mnt']
one(S, 'C%d' % mrow, mnt_b); one(S, 'D%d' % mrow, mnt_a)
one(S, 'C%d' % (mrow + 1), mnt_b / SH); one(S, 'D%d' % (mrow + 1), mnt_a / SH)
one(S, 'C%d' % (mrow + 2), mnt_b / sotp_b); one(S, 'D%d' % (mrow + 2), mnt_a / sotp_a)
one(S, 'D%d' % (mrow + 3), ps_a - ps_b)
assert ANS['SOTP']['ladder1'] - ANS['SOTP']['ladder0'] + 1 == len(marks), 'ladder length'
for k, rr in enumerate(range(ANS['SOTP']['ladder0'], ANS['SOTP']['ladder1'] + 1)):
    one(S, 'A%d' % rr, marks[k])
    one(S, 'B%d' % rr, marks[k] / mnt_b)
    one(S, 'C%d' % rr, (auto_eq + capleg + marks[k] + oth_assoc) / SH)

S = 'Relative & Normalized'
for i, y in enumerate(('2023', '2024', '2025')):
    rr = ANS['REL']['pe0'] + i
    one(S, 'B%d' % rr, REL['history'][y][0]); one(S, 'C%d' % rr, REL['history'][y][1])
    one(S, 'D%d' % rr, eps_hist[y]); one(S, 'E%d' % rr, pe_hist[y])
one(S, 'E%d' % ANS['REL']['pe'], pe_med)
one(S, 'B%d' % ANS['REL']['np26'], grp_np[0])
one(S, 'B%d' % ANS['REL']['eps26'], eps26)
one(S, 'B%d' % ANS['REL']['value'], rel_ps)
one(S, 'B%d' % (ANS['REL']['value'] + 1), rel_ps / SPOT - 1)
one(S, 'B%d' % ANS['REL']['traded'], traded_pe)
one(S, 'B%d' % ANS['REL']['book'], book)
one(S, 'B%d' % ANS['REL']['bvps'], bvps)
one(S, 'B%d' % (ANS['REL']['bvps'] + 1), SPOT / bvps)

S = 'Summary'
r0 = ANS['SUM']['read0']
for i, v in enumerate((ps_b, ps_a, rel_ps)):
    one(S, 'C%d' % (r0 + i), v); one(S, 'D%d' % (r0 + i), v / SPOT - 1)
one(S, 'C%d' % (ANS['SUM']['read1'] + 1), bvps)
one(S, 'D%d' % (ANS['SUM']['read1'] + 1), bvps / SPOT - 1)
one(S, 'C%d' % ANS['SUM']['envlo'], env_lo); one(S, 'D%d' % ANS['SUM']['envlo'], env_lo / SPOT - 1)
one(S, 'C%d' % ANS['SUM']['envhi'], env_hi); one(S, 'D%d' % ANS['SUM']['envhi'], env_hi / SPOT - 1)
one(S, 'C%d' % (ANS['SUM']['envhi'] + 2), SPOT)

S = 'Fundamental Valuation'
one(S, 'C6', ps_b); one(S, 'C7', ps_a); one(S, 'C8', rel_ps); one(S, 'C9', bvps)
one(S, 'B10', env_lo); one(S, 'D10', env_hi); one(S, 'C11', SPOT)
one(S, 'C12', cap_opeq / SH)

S = 'Summary Financials'
setrow(S, 6, HCOLS + FCOLS, hgrpr + grp_rev)
one(S, 'D7', hebit[2] + hdna25)
setrow(S, 7, FCOLS, grp_ebitda)
setrow(S, 8, HCOLS + FCOLS, hebit + grp_ebit)
setrow(S, 9, HCOLS + FCOLS, hnp + grp_np)
setrow(S, 10, HCOLS + FCOLS, ta)
setrow(S, 11, HCOLS + FCOLS, tot_eq)
setrow(S, 12, HCOLS + FCOLS, netdebt)
setrow(S, 13, FCOLS, cf_fcf)
setrow(S, 14, FCOLS, fcff)

S = 'Monte Carlo'
for coord, v in (('B%d' % (ANS.get('MC', {}) or 0), None),):
    pass
for ws_row in wb['Monte Carlo'].iter_rows():
    for c in ws_row:
        if isinstance(c.value, str) and c.value.startswith('=Assumptions!'):
            lbl = c.value.split('$')[-1]
            E[('Monte Carlo', c.coordinate)] = float(
                wb['Assumptions']['B%s' % lbl].value)

S = 'Sensitivity'
g1 = ANS['SENS']['g1']
for k in range(len(marks)):
    one(S, '%s5' % chr(ord('B') + k), marks[k])
for i in range(len(D['sens']['grid_margin'])):
    for k in range(len(marks)):
        one(S, '%s%d' % (chr(ord('B') + k), g1 + i), grid1[i][k])
g2h = ANS['SENS']['g2hdr']; g2 = ANS['SENS']['g2']
for j, t in enumerate(TGS):
    one(S, '%s%d' % (chr(ord('B') + j), g2h), TG + t)
for i in range(len(SHIFTS)):
    for j in range(len(TGS)):
        one(S, '%s%d' % (chr(ord('B') + j), g2 + i), grid2[i][j])
h0 = ANS['SENS']['help0']
for i in range(len(SHIFTS)):
    for k in range(5):
        one(S, '%s%d' % (chr(ord('B') + k), h0 + i), help_df[i][k])
    one(S, 'G%d' % (h0 + i), help_wt[i])
one(S, 'B%d' % ANS['SENS']['offset'], ps_a - ps_b)

S = 'Per-Share & Ratios'
ALLC = HCOLS + FCOLS
np_all = hnp + grp_np
rev_all = hgrpr + grp_rev
eq_all = eq
ebitda_all = [None, None, hebit[2] + hdna25] + grp_ebitda
dps = [grp_np[i] * GD['dividend_payout'][i] / SH for i in range(5)]
r = 6
setrow(S, r, ALLC, [x / SH for x in np_all])
setrow(S, r + 1, FCOLS, dps)
setrow(S, r + 2, ALLC, [x / SH for x in eq_all])
setrow(S, r + 3, ALLC, [SPOT / (x / SH) for x in np_all])
setrow(S, r + 4, ALLC, [SPOT / (x / SH) for x in eq_all])
setrow(S, r + 5, FCOLS, [d / SPOT for d in dps])
setrow(S, r + 6, ['D'] + FCOLS,
       [ebitda_all[2] / rev_all[2]] + [grp_ebitda[i] / grp_rev[i] for i in range(5)])
setrow(S, r + 7, ALLC, [np_all[i] / rev_all[i] for i in range(8)])
setrow(S, r + 8, ALLC, [np_all[i] / eq_all[i] for i in range(8)])
setrow(S, r + 9, ['D'] + FCOLS,
       [netdebt[2] / ebitda_all[2]] + [netdebt[3 + i] / grp_ebitda[i] for i in range(5)])
setrow(S, r + 10, ALLC[1:], [rev_all[i] / rev_all[i - 1] - 1 for i in range(1, 8)])
setrow(S, r + 11, ALLC[1:], [np_all[i] / np_all[i - 1] - 1 for i in range(1, 8)])

# =====================================================================================
# THE GATES
# =====================================================================================
print('delivered workbook: %s' % os.path.basename(XLSX))

nform, errors = 0, []
cells = list(BK.formula_cells())
for sh, coord in cells:
    nform += 1
    try:
        cv(sh, coord)
    except Exception as ex:                                           # noqa: BLE001
        errors.append('%s!%s: %s' % (sh, coord, ex))
print('gate 1 — formulas: %d, unresolvable: %d' % (nform, len(errors)))
for e in errors[:25]:
    print('   ', e)


def tol_for(v):
    return max(2e-4, abs(v) * 5e-6)


nchk, drift = 0, []
for (sh, coord), want in E.items():
    nchk += 1
    try:
        got = cv(sh, coord)
    except Exception:                                                 # noqa: BLE001
        got = None
    if not isinstance(got, (int, float)) or abs(float(got) - want) > tol_for(want):
        drift.append((sh, coord, got, want))
print('gate 2 — formula cells reconciled against the model: %d, disagreements: %d'
      % (nchk, len(drift)))
for sh, coord, got, want in drift[:40]:
    # '%,.6f' IS NOT A PYTHON FORMAT and never was: %-formatting has no comma flag,
    # so this line raises ValueError. It sits inside the loop that runs ONLY when a
    # cell disagrees, so it had never executed -- the reporting path crashed at
    # exactly the moment it was needed and printed nothing about the drift it found.
    g = format(got, ',.6f') if isinstance(got, (int, float)) else repr(got)
    print('    %s!%s: workbook=%s  model=%.6f' % (sh, coord, g, want))

uncovered = ['%s!%s' % (sh, coord) for sh, coord in cells if (sh, coord) not in E]
print('gate 2 — formula cells with no expected value: %d' % len(uncovered))
for u in uncovered[:40]:
    print('   ', u)

chk_cells = [cv('Balance Sheet', '%s%d' % (c, BSJ['CHK'])) for c in HCOLS + FCOLS]
moved = [i for i in range(3, 8) if abs(chk_cells[i] - chk_cells[2]) > 1e-6]
print('gate 3 — the balance check is constant from FY2025 forward: %s (it stands at %.4f, '
      'the rounding inside the disclosed grouping)'
      % ('yes' if not moved else 'NO — ' + str(moved), chk_cells[2]))

BRANCH = D['central_two_sided']['branches']
checks = [
    ('Branch B — ' + BRANCH[0]['label'], ('SOTP Bridge', 'C11'), BRANCH[0]['value'], 0.0005),
    ('Branch A — ' + BRANCH[1]['label'], ('SOTP Bridge', 'D11'), BRANCH[1]['value'], 0.0005),
    ('there is no central, and no cell between the branches',
     ('SOTP Bridge', 'D%d' % (ANS['SOTP']['mnt'] + 3)),
     BRANCH[1]['value'] - BRANCH[0]['value'], 0.0005),
    ('GB Auto equity value', ('DCF', 'B%d' % DCJ['AEQ']), D['sotp']['auto_eq'], 0.5),
    ('GB Auto enterprise value', ('DCF', 'B%d' % DCJ['EVR']), D['dcf']['ev'], 0.5),
    ('sum of the present values, FY26-30E', ('DCF', 'B%d' % DCJ['SPV']), D['dcf']['pv_sum'], 0.5),
    ('terminal value', ('DCF', 'B%d' % DCJ['TVR']), D['dcf']['tv'], 1.0),
    ('present value of the terminal', ('DCF', 'B%d' % DCJ['PVT']), D['dcf']['pv_tv'], 1.0),
    ('terminal share of enterprise value',
     ('DCF', 'B%d' % DC['Terminal share of enterprise value']), D['dcf']['tv_pct'], 0.0005),
    ('GB Capital lending leg', ('Assumptions', 'B%d' % ASM['GB Capital lending leg (EGP mn)']),
     D['lens_inputs']['capital']['value'], 0.5),
    ('GB Capital justified price-to-book',
     ('Assumptions', 'B%d' % ASM['Justified price-to-book = (ROE - g) / (Ke(T) - g)']),
     D['lens_inputs']['capital']['justified_pb'], 1e-6),
    ('GB Capital return on operating equity, 1H2026',
     ('Assumptions', 'B%d' % ASM['Return on operating equity — 1H2026 annualised (ADOPTED)']),
     D['lens_inputs']['capital']['roe_h126'], 1e-6),
    ('GB Capital return on operating equity, FY2025 framing',
     ('Assumptions', 'B%d' % ASM['Return on operating equity — FY2025 framing']),
     D['lens_inputs']['capital']['roe_fy25'], 1e-6),
    ('GB Capital operating equity', ('Assumptions', 'B%d' % ASM['GB Capital operating equity']),
     D['lens_inputs']['capital']['operating_equity'], 0.01),
    ('terminal cost of equity',
     ('Assumptions', 'B%d' % ASM['Terminal cost of equity Ke(T) = rf(T) + beta x mature premium + country premium']),
     D['cost_of_capital_record']['ke_terminal'], 1e-8),
    ('cost of equity, explicit window',
     ('Assumptions', 'B%d' % ASM['Cost of equity Ke = rf* + beta x mature premium + country premium']),
     D['cost_of_capital_record']['ke_exp'], 1e-8),
    ('WACC, first forecast year', ('Assumptions', 'B%d' % ASM['WACC — first forecast year']),
     D['cost_of_capital_record']['wacc_exp'], 1e-8),
    ('cost of equity on the rating basis',
     ('Assumptions', 'B%d' % ASM['Cost of equity, alternative (rating-basis premium)']),
     D['cost_of_capital_rating_basis']['ke_exp'], 1e-8),
    ('MNT-Halan at the round price',
     ('Assumptions', 'B%d' % ASM['BRANCH A — MNT-Halan at the June-2026 round price']),
     D['sotp']['mnt_halan_value'], 0.01),
    ('other associates, by identity',
     ('Assumptions', 'B%d' % ASM["Other associates (Bedaya, Kaf) — by identity off the "
                                 "note's own total"]),
     D['sotp']['other_assoc'], 0.01),
    ('the relative multiple — the MEDIAN of three own-history observations',
     ('Relative & Normalized', 'E%d' % ANS['REL']['pe']), REL['pe'], 1e-9),
    ('the relative read', ('Relative & Normalized', 'B%d' % ANS['REL']['value']),
     D['lenses']['relative']['base'], 0.0005),
    ('the multiple the shares already trade at',
     ('Relative & Normalized', 'B%d' % ANS['REL']['traded']), REL['traded_pe'], 1e-6),
    ('FY2026E group net profit, read from the model',
     ('Relative & Normalized', 'B%d' % ANS['REL']['np26']),
     D['group_forecast']['rows'][0]['net_profit'], 0.01),
    ('book value per share, the disclosed floor',
     ('Relative & Normalized', 'B%d' % ANS['REL']['bvps']),
     D['lens_record']['cross_checks'][1]['value'], 0.0005),
    ('envelope — low', ('Summary', 'C%d' % ANS['SUM']['envlo']), D['central_bear'], 0.0005),
    ('envelope — high', ('Summary', 'C%d' % ANS['SUM']['envhi']), D['central_full'], 0.0005),
    ('the price the answer is measured against', ('SOTP Bridge', 'C12'), D['spot'], 1e-9),
    ('gap on branch B', ('SOTP Bridge', 'C13'),
     D['valuation_gap']['branch_gaps'][0]['gap'], 1e-6),
    ('gap on branch A', ('SOTP Bridge', 'D13'),
     D['valuation_gap']['branch_gaps'][1]['gap'], 1e-6),
    ('the sensitivity grid reaches branch B on its own branch column',
     ('Sensitivity', '%s%d' % (ANS['SENS']['branch_cols']['B'], ANS['SENS']['g1'] + 2)),
     BRANCH[0]['value'], 0.0005),
    ('the sensitivity grid reaches branch A on its own branch column',
     ('Sensitivity', '%s%d' % (ANS['SENS']['branch_cols']['A'], ANS['SENS']['g1'] + 2)),
     BRANCH[1]['value'], 0.0005),
    ('the second grid returns branch A at no shift and no growth change',
     ('Sensitivity', 'D%d' % (ANS['SENS']['g2'] + 2)), BRANCH[1]['value'], 0.0005),
    ('the schedule and the Assumptions WACC are one rate',
     ('DCF', 'B%d' % DC['check: year-1 forward rate less the WACC built on Assumptions']),
     0.0, 1e-12),
    ('FY2030E group net profit', ('Income Statement', 'I%d' % ISR['Net profit (attributable)']),
     D['group_forecast']['rows'][4]['net_profit'], 0.01),
    ('FY2026E free cash flow to the firm, the auto leg',
     ('DCF', 'B%d' % DCJ['FCFF']), D['dcf']['rows'][0]['fcff'], 0.01),
    ('FY2030E free cash flow to the firm, the auto leg',
     ('DCF', 'F%d' % DCJ['FCFF']), D['dcf']['rows'][4]['fcff'], 0.01),
]
bad = 0
for name, (sh, cd), want, tol in checks:
    try:
        got = cv(sh, cd)
    except Exception:                                                 # noqa: BLE001
        got = None
    ok = isinstance(got, (int, float)) and abs(float(got) - float(want)) <= tol
    if not ok:
        bad += 1
    gs = ('%.6f' % got) if isinstance(got, (int, float)) else repr(got)
    print("  [%s] %s: workbook=%s  study=%.6f"
          % ('OK ' if ok else 'BAD', name, gs, float(want)))

# THE ANSWER IS TWO-SIDED, AND A WORKBOOK THAT QUIETLY AVERAGED THE BRANCHES WOULD PASS
# EVERY CHECK ABOVE. This gate refuses that, and it is pointed at the CLAIM rather than at
# every cell in the file. A first draft flagged any cell within half a piastre of the
# midpoint and caught two — the middle rung of an interpolated mark ladder and the middle
# column of the sensitivity grid built on the same interpolation. Both were real: an equal
# step between two disclosures puts their average on the page while calling it a
# sensitivity, and both were removed rather than tolerated. But a grid cell that happens to
# land near the midpoint at some margin shift and some discount rate is arithmetic about a
# stress, not an answer, and a gate that condemned it would be firing on correct work.
# So the test is: (i) the sheets a reader takes an ANSWER from carry nothing strictly
# between the branches except the branches; and (ii) no formula anywhere averages them.
ANSWER_CELLS = ([('Summary', 'C%d' % rr) for rr in range(ANS['SUM']['read0'],
                                                         ANS['SUM']['read1'] + 2)]
                + [('Summary', 'C%d' % ANS['SUM']['envlo']),
                   ('Summary', 'C%d' % ANS['SUM']['envhi'])]
                + [('Fundamental Valuation', c) for c in
                   ('C6', 'C7', 'C8', 'C9', 'B10', 'D10', 'C11', 'C12')]
                + [('SOTP Bridge', 'C11'), ('SOTP Bridge', 'D11')])
lo, hi = BRANCH[0]['value'], BRANCH[1]['value']
between = ['%s!%s' % (sh, cd) for sh, cd in ANSWER_CELLS
           if lo + 1e-6 < float(cv(sh, cd)) < hi - 1e-6]
print('gate 4 — answer cells lying strictly between the two branches (EGP %.4f to %.4f): %d'
      % (lo, hi, len(between)))
for b in between:
    print('   ', b)
BR_B, BR_A = "C11", "D11"
averaged = []
for sh, coord in cells:
    f = str(wb[sh][coord].value)
    if 'AVERAGE(' in f.upper():
        averaged.append('%s!%s (an average)' % (sh, coord))
    elif BR_B in f and BR_A in f and 'SOTP Bridge' in f and '/2' in f:
        averaged.append('%s!%s (the two branches, halved)' % (sh, coord))
print('gate 4 — formulas averaging the two branches: %d' % len(averaged))
for a_ in averaged:
    print('   ', a_)

assert not errors, '%d unresolvable formulas' % len(errors)
assert not drift, '%d formula cells disagree with the model' % len(drift)
assert not uncovered, '%d formula cells are not checked against the model' % len(uncovered)
assert not moved, 'the balance check moves across the forecast'
assert bad == 0, '%d reconciliation mismatches' % bad
assert not between, 'an answer cell lies between the two branches'
assert not averaged, 'a formula averages the two branches'
print('\nRECALC OK — %d of %d formula cells reproduce the model, 0 unresolvable, 0 '
      'unchecked; %d headline reconciliations passed; the two branches are published side '
      'by side and no answer between them is published anywhere.'
      % (nchk, nform, len(checks)))
