"""ADNOC Drilling — did each accepted finding actually reach the model?

critique_pricing.py answered a different question: what would each finding be
WORTH if it were applied. It answered it against an uncorrected baseline, and it
is kept unchanged as the record of that pass. It must not be re-run against this
edition — every correction is now inside the baseline, so applying one again
applies it twice, and the file would report nonsense such as 'gross-debt weights
(8.01% not 8.01%)'.

This file answers the question that comes after: is the finding IN the model? Each
check reads the delivered state and asserts the property the finding demanded, so
a later edit that quietly undoes one of them fails here rather than shipping.

Run: python3 implementation_check.py
"""
import os, sys, json, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('adnoc_compute', os.path.join(HERE, 'compute.py'))
C = importlib.util.module_from_spec(spec)
sys.stdout = open(os.devnull, 'w')
spec.loader.exec_module(C)
sys.stdout = sys.__stdout__

V, IN = C.V, C.INP
A, B = C.CASE['A'], C.CASE['B']
rows = A['rows']
PRIOR_CENTRAL = 5.032139158938172        # the first edition, for the reconciliation below
CHECKS, FAILED = [], []


def check(tag, source, what, ok, evidence):
    CHECKS.append(dict(tag=tag, source=source, what=what, implemented=bool(ok),
                       evidence=evidence))
    if not ok:
        FAILED.append(tag)


# --------------------------------------------------------------- the lenses --
check('CC1a', 'Claude Cowork', 'normalised lens capitalised with NO growth in the denominator',
      abs(C.NORMALISED['capitalisation_rate'] - C.WACC) < 1e-12,
      f'capitalisation rate {C.NORMALISED["capitalisation_rate"]*100:.4f}% equals the weighted '
      f'cost of capital of {C.WACC*100:.4f}% exactly; no growth rate is subtracted')
check('CC1b', 'Claude Cowork', 'normalised lens prices the fleet REPORTED at 30 June 2026',
      (C.NORMALISED['units']['island'] == V('rigs_island_2q26')
       and C.NORMALISED['units']['ids'] == V('ids_2q26') + V('discrete_2q26')),
      f'island {C.NORMALISED["units"]["island"]:.0f} (reported at 30-Jun-2026), rigs served '
      f'{C.NORMALISED["units"]["ids"]:.0f}; the end-2026 target of {V("ids_target_fy26"):.0f} '
      f'integrated rigs is not used')
check('CC1c', 'self-audit', 'normalised depreciation is the charge the priced fleet carries',
      abs(C.NORMALISED['dna'] - V('dna_1h26') * 2) < 1e-9,
      f'{C.NORMALISED["dna"]/1e3:,.0f}m — the 1H-2026 reported charge annualised, against a 2030 '
      f'reference of {C.NORMALISED["dna_2030_reference"]/1e3:,.0f}m on a larger fleet')
check('CC2a', 'Claude Cowork', 'book lens uses the return the model itself forecasts',
      abs(C.BOOK['roe_sustainable'] - C.BOOK['roe_forecast_2030']) < 1e-12,
      f'{C.BOOK["roe_sustainable"]*100:.1f}% (the model\'s own FY2030 return on average equity) '
      f'in place of the realised {C.BOOK["roe_historical"]*100:.1f}%')
check('CC8', 'Claude Cowork', 'relative lens applies a trailing multiple to trailing earnings',
      abs(C.RELATIVE['applied_ebitda']
          - (C.ltm_ebitda - C.ltm_jv)) < 1e-6,
      f'last-twelve-month EBITDA {C.RELATIVE["ltm_ebitda"]/1e3:,.0f}m in place of the guided '
      f'FY2026 midpoint of {C.RELATIVE["guided_ebitda_fy26"]/1e3:,.0f}m')
check('CC9', 'Cowork / Think / Research', 'joint ventures counted once, not twice',
      abs(C.RELATIVE['applied_ebitda']
          - (C.RELATIVE['ltm_ebitda'] - C.RELATIVE['ltm_jv_share'])) < 1e-6,
      f'the {C.RELATIVE["ltm_jv_share"]/1e3:,.0f}m share of joint-venture results is stripped '
      f'from the multiplied earnings; the carrying value stays in the bridge')

# --------------------------------------------------------------- the bridge --
_b = A['bridge']
check('GT1', 'Gemini Think', 'the minority is deducted ONCE, through the put',
      'nci' not in _b and abs(_b['put_liability'] + V('finliab_1h26')) < 1e-9,
      f'the bridge deducts the put of {V("finliab_1h26")/1e3:,.0f}m and does not also deduct the '
      f'{V("nci_1h26")/1e3:,.0f}m of minority interests')
check('CC15', 'Claude Cowork', 'capital-structure weights struck on GROSS debt',
      abs(C.w_e - C.mkt_cap / (C.mkt_cap + C.gross_debt_now)) < 1e-12,
      f'equity weight {C.w_e*100:.2f}% on gross debt of {C.gross_debt_now/1e3:,.0f}m, not net '
      f'debt of {C.net_debt_now/1e3:,.0f}m')
check('DATE', 'self-audit', 'enterprise value and the bridge are dated the same day',
      abs(A['enterprise_value']
          - C.roll_ev_to_jun26(A['enterprise_value_dec25'])) < 1e-6,
      f'{A["enterprise_value_dec25"]/1e6:.2f}bn at 31-Dec-2025 carried to '
      f'{A["enterprise_value"]/1e6:.2f}bn at 30-Jun-2026, less the {C.FCFF_1H26/1e3:,.0f}m of '
      f'free cash flow actually generated, then accreted '
      f'{V("days_jun26_to_anchor"):.0f} days to the price anchor')

# ------------------------------------------------------------ the unit build --
check('CC16', 'Cowork / self-audit', 'the regional book opens at the consolidated count',
      C.OPEN_FLEET['regional'] == V('rigs_regional_2q26'),
      f'opens at {C.OPEN_FLEET["regional"]:.0f} rigs, giving {rows[0]["avg_regional"]:.1f} '
      f'FY2026 rig-years in place of the 15 the first edition booked')
check('CC23', 'Claude Cowork', 'the build reconciles to guidance BY SEGMENT, not at group',
      all(abs(C.CALIB[k] - 1) > 1e-9 for k in ('onshore', 'offshore', 'ofs'))
      and abs(rows[0]['revenue'] - V('g26_revenue')) < 1.0,
      'segment corrections ' + ', '.join(f'{k} {(C.CALIB[k]-1)*100:+.1f}%' for k in C.CALIB)
      + f'; FY2026 revenue ties to the guided {V("g26_revenue")/1e6:.2f}bn exactly')
check('OFS2', 'self-audit', 'oilfield services is built on BOTH disclosed rig populations',
      abs(rows[0]['avg_served'] - (rows[0]['avg_ids'] + rows[0]['avg_discrete'])) < 1e-9,
      f'integrated rigs plus rigs given at least one discrete service; the one-driver model is '
      f'refuted by the company\'s own numbers, which imply an integrated rate of '
      f'{C.OFS_SOLVE_INFEASIBLE["implied_ids_rate"]/1e3:,.1f}m a rig')
check('ACQ', 'self-audit', 'the two 2026 business combinations are consolidated in full',
      abs(sum(v for _, v in C.ACQ_ENTRY)) < 1.0
      and rows[0]['balance_sheet']['nci'] == V('acq_nci'),
      f'the entry closes to {sum(v for _, v in C.ACQ_ENTRY):+.2f} against owners equity; goodwill '
      f'and minority interests each tie to the face of the accounts')
check('SELF-A', 'self-audit', 'working capital set on the post-acquisition balance sheet',
      abs(C.WC_PCT_REVENUE - C.WC_1H26 / C.REV_1H26_ANNUALISED) < 1e-12,
      f'{C.WC_PCT_REVENUE*100:.2f}% of revenue, from the 30-Jun-2026 balance sheet, in place of '
      f'the {C.WC_PCT_REVENUE_HIST*100:.2f}% three-year average of pre-acquisition year ends')

# ---------------------------------------------------------------- REVERSALS --
check('SELF-B', 'self-audit', 'REVERSED — terminal block stays at the weighted cost of capital',
      abs(A['terminal_rate'] - C.WACC) < 1e-12 and A['terminal_is_net_cash'],
      'accepted in the pricing pass, implemented, then reversed on a coherence test against '
      'CC15: weights struck on gross debt cannot be read off net debt in the terminal. The 2030 '
      f'firm does hold net cash ({A["terminal_net_debt"]/1e3:,.0f}m) and that is published; it '
      'does not set the rate')

# ------------------------------------------------- the reconciliation, plainly -
print('IMPLEMENTATION CHECK — is each accepted finding actually in the model?\n')
for c in CHECKS:
    print(f'  [{"IN " if c["implemented"] else "OUT"}] {c["tag"]:<7} {c["what"]}')
    print(f'          {c["evidence"]}')
print()
print(f'  first edition, weighted central                 AED {PRIOR_CENTRAL:.2f}')
print(f'  this edition, weighted central                  AED {C.central:.2f}   '
      f'({C.central/PRIOR_CENTRAL-1:+.1%})')
print(f'  market price                                    AED {V("spot_aed"):.2f}')
print(f'  by lens: ' + '  '.join(f'{k} {v:.2f}' for k, v in C.FAIR.items()))
print()
print(f'{len(CHECKS)} findings checked, {len(CHECKS)-len(FAILED)} implemented, '
      f'{len(FAILED)} not' + (f': {FAILED}' if FAILED else ''))

# [R-ENF-06] THE ANSWER THIS ARTEFACT WAS BUILT AGAINST, read from the study's own
# committed numbers rather than typed, so it cannot drift from them. A builder reads
# this file and nothing said what it was current WITH, so a stale copy would have had
# the shape of a computed record — which is worse than a typed numeral, because a typed
# numeral is what the numeric-traceability gate already catches.
_PUB = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   'study_numbers.json'), encoding='utf-8'))
_PUB_C, _PUB_S = _PUB['central'], _PUB['spot']

json.dump(dict(prior_central=PRIOR_CENTRAL, central=C.central, spot=V('spot_aed'),
               published_central=_PUB_C, published_spot=_PUB_S,
               by_lens=C.FAIR, checks=CHECKS),
          open(os.path.join(HERE, 'implementation_check.json'), 'w'), indent=1)
assert not FAILED, f'accepted findings missing from the model: {FAILED}'
