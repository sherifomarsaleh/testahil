"""What is ARCC worth if EFG's margin view is right?

Our EBITDA margin is an OUTPUT of the bottom-up build — derived prices minus a per-tonne
cost stack — and it glides DOWN from the audited FY2025 peak of 39.25% to 35.02% by FY2030,
because the cost stack inflates faster than the price path. EFG holds margin essentially
flat at the FY2025 level. That is the single largest open item between the two models.

This file does not argue the question. It overrides the margin path, re-runs the DCF and
the two earnings-based lenses, and prints what falls out.

GATE: scenario 0 rebuilds the published 55.40 / 54.65 from study_numbers.json before any
override is applied. If the harness cannot reproduce the base case it is not entitled to
report a scenario, so it exits instead.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
F, DCF, W, L, H = D['forecast'], D['dcf'], D['wacc'], D['lenses'], D['history']
IN = {k: v['value'] for k, v in D['inputs'].items()}
SH, REM = D['meta']['shares_mn'], DCF['rem']
TAXE = 1 - F['nopat'][0] / F['ebit'][0]
G, WT_ = IN['g_term'], W['wacc_term']
MGN_FY25 = H['margin'][2]                       # 39.25% audited
BASE = list(F['margin'])                        # 36.03 -> 35.02, derived not assumed


def dcf(mgn, rev_mult=None):
    """Revalue on an EBITDA-margin PATH. Capex, working capital, the discount schedule and
    the terminal algebra are untouched. rev_mult optionally scales the revenue path, which
    matters because a margin-only run keeps OUR volume build — the more optimistic of the
    two volume views — and would otherwise read as neutral when it is not."""
    rm = rev_mult or [1.0] * 5
    rev = [F['revenue'][i] * rm[i] for i in range(5)]
    eb = [rev[i] * mgn[i] for i in range(5)]
    ebit = [eb[i] - F['dna'][i] for i in range(5)]
    nop = [ebit[i] * (1 - TAXE) for i in range(5)]
    fc = [nop[i] + F['dna'][i] - F['capex'][i] - F['dwc'][i] * rm[i] for i in range(5)]
    fc[0] *= REM
    pv = sum(fc[i] * F['df'][i] for i in range(5))
    rr = G / (nop[-1] * (1 + G) / DCF['ic_repl'])          # reinvestment = g / ROIC
    tv = nop[-1] * (1 + G) * (1 - rr) / (WT_ - G)
    return (pv + tv * DCF['df_tv'] + DCF['net_cash'] - DCF['nci']) / SH, rr


def lenses(fv_dcf, norm_mgn):
    """The two earnings lenses run off a MID-CYCLE margin, not the forecast path. They only
    move if you also accept that the through-cycle level is higher, so norm_mgn is passed
    in explicitly rather than inherited."""
    ebn = IN['rev_fy25'] * IN['norm_rev_haircut'] * norm_mgn
    rel = (ebn * IN['ev_ebitda_just'] + DCF['net_cash'] - DCF['nci']) / SH
    nopn = (ebn - IN['dna_fy25']) * (1 - TAXE)
    nrm = (nopn * IN['pe_just'] + DCF['net_cash'] - DCF['nci']) / SH
    ast = L['values']['Asset / replacement cost']
    wts = L['weights']
    v = {'DCF (cash flow)': fv_dcf, 'Relative multiples': rel,
         'Normalised earnings': nrm, 'Asset / replacement cost': ast}
    return v, sum(v[k] * wts[k] for k in v)


# ---- GATE: reproduce the published base case --------------------------------
b_dcf, b_rr = dcf(BASE)
b_v, b_c = lenses(b_dcf, IN['norm_mgn'])
bad = [f"DCF {b_dcf:.4f} vs {L['values']['DCF (cash flow)']:.4f}"] if abs(
    b_dcf - L['values']['DCF (cash flow)']) > 0.01 else []
bad += [f"central {b_c:.4f} vs {L['central']:.4f}"] if abs(b_c - L['central']) > 0.01 else []
for k in ('Relative multiples', 'Normalised earnings'):
    if abs(b_v[k] - L['values'][k]) > 0.01:
        bad.append(f"{k} {b_v[k]:.4f} vs {L['values'][k]:.4f}")
print('GATE — harness reproduces the published base case:', 'PASS' if not bad else 'FAIL')
if bad:
    sys.exit('  ' + '; '.join(bad))

# ---- the scenarios ----------------------------------------------------------
FLAT = [MGN_FY25] * 5                                  # EFG: FY2025 margin is durable
HALF = [(BASE[i] + FLAT[i]) / 2 for i in range(5)]     # split the difference

# EFG's FY2028 revenue is 13,792 against our 15,350 — their volumes FALL 3% over the five
# years where ours rise 3.1%. Read off their Figure 1; the intermediate years are not
# tabulated here, so the gap is ramped linearly to that FY2028 anchor and held widening at
# the same annual rate. Labelled a PROXY wherever it is reported.
EFG_FY28 = 13792.0
step = (1.0 - EFG_FY28 / F['revenue'][2]) / 3.0        # per-year erosion to hit FY2028
EFG_REV = [1.0 - step * (i + 1) for i in range(5)]

SC = [('Testahil base — margin glides 39.3% -> 35.0%', BASE, IN['norm_mgn'], None),
      ('Half way — glide only half as far', HALF, IN['norm_mgn'], None),
      ("EFG margin — HELD at the FY2025 39.25%", FLAT, IN['norm_mgn'], None),
      ("EFG margin AND a 39.25% mid-cycle margin", FLAT, MGN_FY25, None),
      ("EFG margin AND EFG volumes (PROXY)", FLAT, IN['norm_mgn'], EFG_REV)]

print(f"\n  effective tax {TAXE:.2%}   terminal rate {WT_:.2%}   g {G:.1%}   "
      f"market {IN['spot']:.2f}\n")
print(f"  {'scenario':44s} {'FY30 mgn':>9s} {'DCF':>8s} {'central':>9s} {'vs mkt':>8s} {'reinv':>7s}")
rows = []
for name, mgn, nm, rm in SC:
    fv, rr = dcf(mgn, rm)
    v, c = lenses(fv, nm)
    rows.append(dict(name=name, mgn_path=[round(m, 4) for m in mgn], norm_mgn=nm,
                     rev_mult=rm and [round(x, 4) for x in rm], dcf=round(fv, 2),
                     central=round(c, 2), reinvest=round(rr, 4),
                     lenses={k: round(x, 2) for k, x in v.items()}))
    print(f"  {name:44s} {mgn[-1]:8.1%} {fv:8.2f} {c:9.2f} {c/IN['spot']-1:+8.1%} {rr:7.1%}")

print(f"\n  sensitivities off the base case:")
up, _ = dcf([m + 0.01 for m in BASE])
dn, _ = dcf(BASE, [0.95] * 5)
print(f"    +1.00pt of EBITDA margin, every year  ->  DCF {up - b_dcf:+.2f}   "
      f"central {lenses(up, IN['norm_mgn'])[1] - b_c:+.2f}")
print(f"    -5.0% on the revenue path, every year ->  DCF {dn - b_dcf:+.2f}   "
      f"central {lenses(dn, IN['norm_mgn'])[1] - b_c:+.2f}")

json.dump(rows, open(os.path.join(HERE, 'scenario_margin.json'), 'w'), indent=1)
print('\n  wrote scenario_margin.json')
