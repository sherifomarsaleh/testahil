"""Price every audit finding on the REAL compute chain (override hook), before judging it."""
import json, os, subprocess, sys
BASE = None
def run(label, inputs=None, flags=None):
    env = dict(os.environ, DU_OVERRIDE=json.dumps({'inputs': inputs or {}, 'flags': flags or {}}))
    subprocess.run([sys.executable, 'compute.py'], env=env, capture_output=True, check=True)
    d = json.load(open('study_numbers.json'))
    return dict(label=label, dcf=d['dcf']['ps'], central=d['central'], rel=d['lenses']['relative']['base'],
                nrm=d['lenses']['normalized']['base'], book=d['lenses']['book']['base'],
                fb=d['dcf']['ps_framing_b'], grid=d['sens']['grid_beta'],
                span=d['span'], m26=d['fcst']['ebitda_margin'][0], ev=d['dcf']['ev'],
                tv_share=d['dcf']['tv_share'])
BASE = run('BASE (as published)')
CEN = BASE['central']
rows=[]
def price(label, **kw):
    r = run(label, **kw)
    dd, dc = r['dcf']-BASE['dcf'], r['central']-CEN
    rows.append((label, r['dcf'], dd, r['central'], dc, dc/CEN))
    print(f"{label:<58} DCF {r['dcf']:6.2f} ({dd:+5.2f})  central {r['central']:6.2f} ({dc:+5.2f}, {dc/CEN:+6.2%})")
    return r
print(f"{'BASE':<58} DCF {BASE['dcf']:6.2f}          central {CEN:6.2f}\n")
# --- the peer multiple (CW#1, CC#4/5) : above 5% -> re-derivation pending, price all candidates
for lab, v in [('P/E 15.5 -> 14.0 (median of my own stated set, CC#4)', 14.0),
               ('P/E 15.5 -> 12.9 (CW#1 Mobily filing-derived)', 12.9),
               ('P/E 15.5 -> 13.0 (median incl. corrected e& 15.3)', 13.0)]:
    price(lab, inputs={'pe_just': v})
# --- sovereign netting / rf basis (CC#2, CW#4, GT#2)
price('same-basis market spread 25bp + ERP 4.66 (my published basis 2)',
      inputs={'sov_spread_rating':0.0025,'erp_rating':0.0466,'erp_term':0.0466})
price('same-basis market spread 4bp + ERP 4.29 (CC#2 fix)',
      inputs={'sov_spread_rating':0.0004,'erp_rating':0.0429,'erp_term':0.0429})
price('rf* floored at matched-tenor UST 4.32% (no-arb floor)',
      inputs={'sov_spread_rating':0.0016})
price('GT#2 fix: rf 4.69% UN-netted + full 4.87 ERP (double-counts CRP)',
      inputs={'rf':0.0469,'sov_spread_rating':0.0,'rf_term':0.0469})
price('CW#6: longest AED tenor Feb-2033 3.779% (terminal rf pulled to 3.70)',
      inputs={'rf':0.03779,'rf_term':0.037,'rf_path':[0.03779,0.0376,0.0374,0.0372,0.037]})
# --- staff cost (CC#11) : my own arithmetic error
price('staff FY26 985 -> 1035.2 (true H2/H1 seasonal ratio 1.196)', inputs={'staff_fy26':1035.16})
price('CC#11 own fix: staff ~1090 (escalated residual)', inputs={'staff_fy26':1090.0})
# --- lease treatment (CC#12, GT#1 vs GR)
price('drop lease-replacement charge (leases-as-debt, CC#12/GT#1)', flags={'no_lease_repl':True})
# --- ex-dividend (GT#3)
price('strip the AED 0.26 interim from every lens (GT#3)', inputs={'div_between':0.66})
# --- book bear single g (CC#13, CW#15)
price('book-lens bear on a single g=2% (CC#13)', flags={'single_g_book':True})
# --- Framing B own reinvestment rate (MY finding, all four missed)
price('Framing B computes its own reinvestment rate (mine)', flags={'framingB_own_rr':True})
# --- beta grid netted (CC#1, CW#3)
r = price('beta grid re-run on the netted basis (CC#1/CW#3)', flags={'beta_grid_netted':True})
print(f"   -> grid now {[round(x,2) for x in r['grid']]} vs published {[round(x,2) for x in BASE['grid']]}")
print(f"   -> base cell {r['grid'][1]:.2f} vs headline DCF {BASE['dcf']:.2f} (gap {r['grid'][1]-BASE['dcf']:+.3f})")
# --- mid-year discounting (CC#24)
price('mid-year discounting on the explicit window (CC#24)', flags={'midyear':True})
# --- combinations
price('ALL accepted-so-far combined (staff+lease+grid+bookg+FramB)',
      inputs={'staff_fy26':1035.16}, flags={'no_lease_repl':True,'beta_grid_netted':True,
      'single_g_book':True,'framingB_own_rr':True})
json.dump(rows, open('finding_prices.json','w'), indent=1)
print('\nwrote finding_prices.json')
