"""ARCC margin: our path against EFG Hermes', year by year — and what theirs is worth.

Our EBITDA margin is an OUTPUT of the bottom-up build (derived prices less a per-tonne cost
stack). It glides DOWN from the audited FY2025 peak because the cost stack inflates faster
than the price path. EFG hold c40%. That is the one item in the reconciliation bridge
marked "open — no referee".

THE CENTRAL HERE IS THE PRIMARY LENS ALONE. The typed four-lens blend is retired
[R-LENS-03]; the other readings are computed and printed beside it, never averaged in.

THE TRAP THIS FILE EXISTS TO AVOID. EFG's FY2025a EBITDA is 5,017; the audited figure we
use is 4,886. The EGP 131 difference is DEFINITIONAL, not a forecast disagreement:

    provisions 74.506 + expected credit losses 3.604 + other operating income 53.340
        = 131.449  =  1.0560% of FY2025 revenue

We charge provisions and ECL above EBITDA (they are operating charges in the audited
statements) and we exclude other operating income. EFG do the reverse. Comparing their
40.3% to our 39.25% therefore overstates the disagreement by a full point in every year.
Restating their published margins onto our definition MUST reproduce our audited 39.25% in
FY2025a, and that is asserted below before any forecast year is quoted.

GATES
  G1  the definitional bridge reconciles FY2025a to within 0.1 of EFG's printed EBITDA
  G2  restating EFG's FY2025a onto our definition reproduces our audited margin
  G3  the harness rebuilds the study's OWN published DCF lens and central before any
      override is applied — read from study_numbers.json, never typed, because the
      typed pair went stale the moment the study was re-issued

SOURCES. EFG Hermes, "Arabian Cement (Egypt)", 6 August 2026, page 2 "Data Miner" —
revenue, EBITDA, EBIT, capex and margins for FY2025a to FY2028e. FY2029e and FY2030e are
NOT tabulated in that report; they are extended here from the report's own text ("we expect
the company to sustain an EBITDA margin of c40% on average") and its decelerating revenue
growth. Every extended figure is flagged EXT in the output and in the JSON.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import terminal_value
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
F, DCF, W, L, H = D['forecast'], D['dcf'], D['wacc'], D['lenses'], D['history']
TR = D['terminal_record']
IN = {k: v['value'] for k, v in D['inputs'].items()}
SH, REM = D['meta']['shares_mn'], DCF['rem']
TAXE = 1 - F['nopat'][0] / F['ebit'][0]
G, WT_ = IN['g_term'], W['wacc_term']
YRS = ['FY2026e', 'FY2027e', 'FY2028e', 'FY2029e', 'FY2030e']

# ---- EFG, page 2 "Data Miner" -----------------------------------------------
E_REV_PUB = [12447.0, 13144.0, 13528.0, 13792.0]        # FY2025a .. FY2028e
E_EBITDA_PUB = [5017.0, 5132.0, 5485.0, 5620.0]
E_EBIT_PUB = [4727.0, 4814.0, 5138.0, 5242.0]
E_GROWTH_EXT = 0.02                                     # EXT: their own 5.6/2.9/2.0 trend

# ---- G1: the definitional bridge --------------------------------------------
WEDGE = IN['prov_fy25'] + IN['ecl_fy25'] + IN['othinc_fy25']
WEDGE_PCT = WEDGE / IN['rev_fy25']
g1 = abs((H['ebitda'][2] + WEDGE) - E_EBITDA_PUB[0]) < 0.1
print(f"G1  definitional bridge: our {H['ebitda'][2]:,.0f} + prov {IN['prov_fy25']:.1f} "
      f"+ ECL {IN['ecl_fy25']:.1f} + other income {IN['othinc_fy25']:.1f} = "
      f"{H['ebitda'][2] + WEDGE:,.0f} vs EFG {E_EBITDA_PUB[0]:,.0f}   "
      f"{'PASS' if g1 else 'FAIL'}   wedge = {WEDGE_PCT:.4%} of revenue")

# EFG margins as published, and restated onto our definition
E_MGN_PUB = [E_EBITDA_PUB[i] / E_REV_PUB[i] for i in range(4)]
E_MGN_OURS = [m - WEDGE_PCT for m in E_MGN_PUB]
g2 = abs(E_MGN_OURS[0] - H['margin'][2]) < 0.0001
print(f"G2  EFG FY2025a restated onto our definition: {E_MGN_OURS[0]:.4%} vs our audited "
      f"{H['margin'][2]:.4%}   {'PASS' if g2 else 'FAIL'}")

# extend FY2029e / FY2030e — flagged, not published
E_REV = list(E_REV_PUB) + [E_REV_PUB[-1] * (1 + E_GROWTH_EXT),
                           E_REV_PUB[-1] * (1 + E_GROWTH_EXT) ** 2]
E_MGN_PUB = E_MGN_PUB + [E_MGN_PUB[-1], E_MGN_PUB[-1]]
E_MGN_OURS = E_MGN_OURS + [E_MGN_OURS[-1], E_MGN_OURS[-1]]
EXT = [False, False, False, False, True, True]          # index 0 = FY2025a

BASE = list(F['margin'])


def dcf(mgn, rev_mult=None):
    """Revalue on an EBITDA-margin PATH. Capex, the discount schedule and the terminal
    algebra are untouched. rev_mult scales the revenue path — a margin-only run keeps OUR
    volume build, the more optimistic of the two, and would read as neutral when it is not."""
    rm = rev_mult or [1.0] * 5
    rev = [F['revenue'][i] * rm[i] for i in range(5)]
    eb = [rev[i] * mgn[i] for i in range(5)]
    # OTHER OPERATING INCOME is part of EBIT in the model and was dropped here, which
    # is what remained of the harness's 27% divergence once the terminal was fixed.
    ebit = [eb[i] - F['dna'][i] + F['other_income'][i] for i in range(5)]
    nop = [ebit[i] * (1 - TAXE) for i in range(5)]
    fc = [nop[i] + F['dna'][i] - F['capex'][i] - F['dwc'][i] * rm[i] for i in range(5)]
    fc[0] *= REM
    pv = sum(fc[i] * F['df'][i] for i in range(5))
    # THE TERMINAL IS BUILT BY THE SHARED BUILDER, NOT RE-IMPLEMENTED HERE. Until
    # 03-Sep-2026 these two lines carried rr = g / ROIC and the substituted terminal it
    # implies, which [R-TERM-01] retired for charging g x IC for ever — an asset life of
    # one over the inflation rate. That left this harness 27% below the study it was
    # supposed to reproduce, and its G3 gate said so the moment it was next run. A
    # re-implementation grades something other than what ships [R-ENF-03]: the inputs come
    # from the study's OWN committed terminal record, and only the two that this scenario
    # actually moves are substituted.
    _ti = dict(TR['inputs'])
    _ti['nopat'] = float(nop[-1])
    _ti['dna_book'] = float(F['dna'][-1])
    tv = terminal_value.build(terminal_value.TerminalInputs(**_ti)).tv
    rr = 0.0 if abs(nop[-1]) < 1e-12 else 1.0 - (tv * (WT_ - G) / (1 + G)) / nop[-1]
    return (pv + tv * DCF['df_tv'] + DCF['net_cash'] - DCF['nci']) / SH, rr


def lenses(fv_dcf, norm_mgn):
    """The cross-check lenses beside the primary. THE BLEND IS RETIRED [R-LENS-03], so this
    returns the primary as the answer and the others beside it — it does NOT average them.

    Until 03-Sep-2026 this function ended on sum(v[k] * L['weights'][k]), and when the
    weights were retired from the numbers file it began raising KeyError. Nothing noticed,
    because a generator that crashes leaves the artefact it writes exactly as it was: the
    delivered study went on publishing this file's LAST SUCCESSFUL run, a base central of
    54.65 against a published 66.53, in a table headed 'Central'. That is [R-ENF-06]
    exactly — an artefact a builder reads, frozen at the date its generator last worked.
    """
    ebn = IN['rev_fy25'] * IN['norm_rev_haircut'] * norm_mgn
    rel = (ebn * IN['ev_ebitda_just'] + DCF['net_cash'] - DCF['nci']) / SH
    nopn = (ebn - IN['dna_fy25']) * (1 - TAXE)
    nrm = (nopn * IN['pe_just'] + DCF['net_cash'] - DCF['nci']) / SH
    v = {'DCF (cash flow)': fv_dcf, 'Relative multiples': rel, 'Normalised earnings': nrm,
         'Asset / replacement cost': L['values']['Asset / replacement cost']}
    return v, fv_dcf


# ---- G3: reproduce the published base case ----------------------------------
b_dcf, b_rr = dcf(BASE)
b_v, b_c = lenses(b_dcf, IN['norm_mgn'])
g3 = abs(b_dcf - L['values']['DCF (cash flow)']) < 0.01 and abs(b_c - L['central']) < 0.01
print(f"G3  harness rebuilds the published base case: DCF {b_dcf:.2f} / central {b_c:.2f}"
      f"   against the published {L['values']['DCF (cash flow)']:.2f} / {L['central']:.2f}"
      f"   {'PASS' if g3 else 'FAIL'}")
if not (g1 and g2 and g3):
    sys.exit('GATES FAILED — not entitled to report a scenario')

# ---- the table --------------------------------------------------------------
print(f"\n  EBITDA MARGIN, YEAR BY YEAR  (EFG wedge removed: {WEDGE_PCT:.2%} of revenue)\n")
print(f"  {'':10s} {'Testahil':>10s} {'EFG pub':>10s} {'EFG on our':>11s} {'gap':>8s}   "
      f"{'Testahil rev':>13s} {'EFG rev':>9s}")
print(f"  {'FY2025a':10s} {H['margin'][2]:9.2%} {E_MGN_PUB[0]:10.2%} {E_MGN_OURS[0]:11.2%} "
      f"{'audited':>8s}   {IN['rev_fy25']:13,.0f} {E_REV[0]:9,.0f}")
tbl = []
for i, y in enumerate(YRS):
    gap = E_MGN_OURS[i + 1] - BASE[i]
    tag = ' EXT' if EXT[i + 1] else ''
    # NO PRE-ROUNDING IN THE RECORD, ONLY AT THE RENDER. Rounding a margin to four places
    # here put FY2025a at exactly 0.3925, a half-way value that then rounded DOWN to 39.2%
    # in the table while the unrounded 0.392502 rounded UP to 39.3% in the caption beside
    # it — the same number printed two ways on one page, caused entirely by rounding twice.
    tbl.append(dict(year=y, testahil=float(BASE[i]), efg_published=float(E_MGN_PUB[i + 1]),
                    efg_our_definition=float(E_MGN_OURS[i + 1]), gap_pt=float(gap * 100),
                    testahil_revenue=float(F['revenue'][i]), efg_revenue=float(E_REV[i + 1]),
                    extended=EXT[i + 1]))
    print(f"  {y:10s} {BASE[i]:9.2%} {E_MGN_PUB[i+1]:10.2%} {E_MGN_OURS[i+1]:11.2%} "
          f"{gap*100:+7.2f}pt   {F['revenue'][i]:13,.0f} {E_REV[i+1]:9,.0f}{tag}")

# ---- the scenarios ----------------------------------------------------------
E_MGN_F = E_MGN_OURS[1:]                                 # their margin, our definition
E_REV_MULT = [E_REV[i + 1] / F['revenue'][i] for i in range(5)]
HALF = [(BASE[i] + E_MGN_F[i]) / 2 for i in range(5)]

SC = [("Testahil base — our margin, our volumes", BASE, IN['norm_mgn'], None),
      ("Half way between the two margin paths", HALF, IN['norm_mgn'], None),
      ("EFG margin, OUR volumes", E_MGN_F, IN['norm_mgn'], None),
      ("EFG margin, EFG volumes — their view whole", E_MGN_F, IN['norm_mgn'], E_REV_MULT),
      ("EFG margin, our volumes, mid-cycle lifted too", E_MGN_F, H['margin'][2], None)]

print(f"\n  {'scenario':46s} {'DCF':>8s} {'central':>9s} {'vs mkt':>8s} {'reinv':>7s}")
rows = []
for name, mgn, nm, rm in SC:
    fv, rr = dcf(mgn, rm)
    v, c = lenses(fv, nm)
    rows.append(dict(name=name, dcf=float(fv), central=float(c), reinvest=float(rr),
                     mgn_path=[float(m) for m in mgn],
                     rev_mult=rm and [float(x) for x in rm], norm_mgn=float(nm)))
    print(f"  {name:46s} {fv:8.2f} {c:9.2f} {c/IN['spot']-1:+8.1%} {rr:7.1%}")

up, _ = dcf([m + 0.01 for m in BASE])
dn, _ = dcf(BASE, [0.95] * 5)
print(f"\n  sensitivities off the base case:")
print(f"    +1.00pt of EBITDA margin, every year   DCF {up-b_dcf:+.2f}   "
      f"central {lenses(up, IN['norm_mgn'])[1]-b_c:+.2f}")
print(f"    -5.0% on the revenue path, every year  DCF {dn-b_dcf:+.2f}   "
      f"central {lenses(dn, IN['norm_mgn'])[1]-b_c:+.2f}")

json.dump(dict(published_central=float(L['central']), published_spot=float(IN['spot']),
               wedge_pct=WEDGE_PCT, wedge_egp=WEDGE, margin_table=tbl, scenarios=rows,
               fy25a=dict(testahil=float(H['margin'][2]), efg_published=float(E_MGN_PUB[0]),
                         efg_our_definition=float(E_MGN_OURS[0]))),
          open(os.path.join(HERE, 'scenario_margin.json'), 'w'), indent=1)
print('\n  wrote scenario_margin.json')
