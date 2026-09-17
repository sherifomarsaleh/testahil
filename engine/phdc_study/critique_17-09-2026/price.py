from phdc import *

B = value(); BASE = B['ps']
def rep(tag, ps, note=''):
    d = ps - BASE
    print(f'{tag:<58s} {ps:9.4f}   {d:+8.4f}  {d/BASE:+8.2%}   {note}')

print(f'{"COUNTERFACTUAL":<58s} {"EGP/sh":>9s}   {"Δ EGP":>8s}  {"Δ %":>8s}')
print(f'{"BASE — as delivered":<58s} {BASE:9.4f}   {0:+8.4f}  {0:+8.2%}')
print('-'*110)

# --- row 1: the published single rate, applied flat -----------------------
for r,lab in [(0.2511,'25.11% (adopted, swap basis)'),(0.260967,'26.0967% (Assumptions!B12)')]:
    rep(f'1  flat {lab}', value(path=[r]*15, term_g=TERM_G, term_pv=None)['ps'])

# MY FINDING: the 10-Sep house terminal of 14.9751% instead of 16.1547%
p = WACC_PATH[:4] + [0.1497514171621503]*11
rep('SA-1  terminal at the 10-Sep house rate 14.9751%', value(path=p, term_pv=None)['ps'])

# --- row 2: the bridge on the sheet it names ------------------------------
rep('2  bridge on the TRUE 31-Mar sheet (8-line def.)',
    value(net_debt=23244.719, assoc=3838.697211, invprop=1020.474869)['ps'])
rep("2b  same, on the critique's 6-line net debt 23,076.3",
    value(net_debt=23076.311, assoc=3838.697211, invprop=1020.474869)['ps'])

# --- row 4: conversion at the stated three-year mean ----------------------
mean3 = (0.0433340+0.1787001+0.0393759)/3
rep(f'4  conversion at the stated 3-yr mean {mean3:.4%}', value(conv=mean3)['ps'])

# --- row 9: a genuine five-year window ------------------------------------
rep('9  five explicit years, as the text declares', value(n_years=5)['ps'])

# --- row 15: what conversion does 45.11 require? --------------------------
lo,hi=0.0,1.0
for _ in range(200):
    m=(lo+hi)/2
    if value(conv=m)['ps'] < 45.11: lo=m
    else: hi=m
print(f'{"15  conversion required for the published 45.11 high":<58s} {45.11:9.4f}   '
      f'{"":>8s}  {"":>8s}   needs conv = {(lo+hi)/2:.4%}')
rep('15b DCF high at the adopted rate (conv 17.870%)', value(conv=CONV_STRONG)['ps'])
rep('15c DCF low  at the adopted rate (conv 3.938%)',  value(conv=CONV_WEAK)['ps'])

# --- row 20: weights on the June debt book -------------------------------
mktcap = 14.40*SHARES
for debt,lab in [(33552.7,'31-Dec-2025 book (as used)'),(35275.5,'30-Jun-2026 book (the bridge)')]:
    we = mktcap/(mktcap+debt); wacc = we*0.294639 + (1-we)*0.1976250
    print(f'   20  weights on {lab:<34s} We={we:.4%} WACC={wacc:.4%}')
we = mktcap/(mktcap+35275.5); wacc0 = 0.2511
scale = (we*0.294639+(1-we)*0.1976250)/wacc0
rep('20  path rescaled to the June-book WACC 24.99%',
    value(path=[w*scale for w in WACC_PATH], term_pv=None)['ps'])

# --- row 22: half-year stub ----------------------------------------------
rep('22  half-year stub from the 30-Jun bridge date', value(stub=0.5, term_pv=None)['ps'])

# --- row 23: the flat 15% the text declares ------------------------------
rep('23  units grow a flat 15%, as the text declares',
    value(growth=[0]+[0.15]*14, term_pv=None)['ps'])

# --- row 24: the other two minority bases --------------------------------
for m,lab in [(0.0594,'3-year mean profit share 5.94%'),(0.0835,'book share of equity 8.35%')]:
    rep(f'24  minority at the {lab}', value(mi=m)['ps'])

# --- row 25: the outstanding share count ---------------------------------
rep('25  divided by the outstanding count 2,839.98mn', value(shares=2839.980164)['ps'])

# --- row 41: no after-tax finance add-back -------------------------------
rep('41  no finance-cost add-back at all', value(fin=0.0, term_pv=None)['ps'])
rep('41b add-back escalating with the price path',
    value(fin=0.0, term_pv=None, capex=CAPEX)['ps'], '(see below)')

# --- row 32: the revenue anchor on the statement figure ------------------
rep('32  anchor on 9,346.1 not the rounded 9,300',
    value(units0=UNITS_26*9346.133744/9300.0)['ps'])

# --- row 5: beta on the regressor TMGH's row implies ---------------------
for b,lab in [(1.41,'1.41 (row 5)'),(1.0329,'1.0329 Blume-adjusted (row 24 of contested)')]:
    ke = 0.1959 + b*0.0941
    wacc = 0.551*ke + 0.449*0.1976250
    sc = wacc/0.2511
    rep(f'5  beta {lab} -> WACC {wacc:.4%}',
        value(path=[w*sc for w in WACC_PATH], term_pv=None)['ps'])

# --- row 39: capex on the disclosed 9.1% of the asset base ---------------
rep('39  maintenance capex at 0 (upper bound of the fix)', value(capex=0.0, term_pv=None)['ps'])

# --- the reverse read: implied conversion at each rate -------------------
print('-'*110)
for r,lab in [(None,'the undisclosed falling path'),(0.2511,'a flat 25.11%')]:
    p = WACC_PATH if r is None else [r]*15
    lo,hi=0.0,1.0
    for _ in range(200):
        m=(lo+hi)/2
        if value(conv=m,path=p,term_pv=None)['ps'] < 14.40: lo=m
        else: hi=m
    print(f'   implied conversion at EGP 14.40 on {lab:<32s} = {(lo+hi)/2:.4%}')
