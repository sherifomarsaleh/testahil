"""Price every critique finding. Input-level findings re-run the whole model through
compute.py's audit hook; structural findings are re-derived closed-form from the model's
own committed numbers. Nothing here is typed by hand except the alternative the critic asks for."""
import json, os, subprocess, sys, tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, 'study_numbers.json')))
L, D, W, F = S['lenses'], S['dcf'], S['wacc'], S['forecast']
B_C, B_A, B_B = L['fair_base'], D['frame_A']['per_share'], D['frame_B']['per_share']
SH = S['inputs']['shares_mn']['value']
WT = {l['name']: l['weight'] for l in L['items']}
w_A, w_B, w_bk, w_rel, w_nrm = 0.25, 0.25, 0.20, 0.15, 0.15


def run(over):
    fd, path = tempfile.mkstemp(suffix='.json'); os.close(fd)
    env = dict(os.environ, PHAR_OVERRIDE=json.dumps(over), PHAR_QUIET='1', PHAR_OUT=path)
    r = subprocess.run([sys.executable, os.path.join(HERE, 'compute.py')], env=env,
                       capture_output=True, text=True)
    if r.returncode:
        os.unlink(path); return None, r.stderr.strip().split('\n')[-1]
    d = json.load(open(path)); os.unlink(path)
    return d, None


def centre(a=B_A, b=B_B, bk=L['book_ps'], rel=L['rel_ps'], nrm=L['norm_ps']):
    return w_A * a + w_B * b + w_bk * bk + w_rel * rel + w_nrm * nrm


def bridge(ev_core, assoc=D['frame_A']['assoc_value'], afs=S['inputs']['afs_fy25']['value'],
           nd=W['net_debt'], nci=D['frame_A']['nci']):
    return (ev_core + assoc + afs - nd - nci) / SH


def dcf(nopat, fcff, nopat_term=None, reinv=None, extra_term_cf=0.0):
    """Rebuild a frame from a cash-flow path, using the model's own factors."""
    df, wt, g = np.array(W['df']), W['wacc_term'], S['inputs']['g_term']['value']
    pv = float(np.dot(np.array(fcff), df))
    nt = nopat[-1] * (1 + g) if nopat_term is None else nopat_term
    rr = (g / S['inputs']['roic_term']['value']) if reinv is None else reinv
    tfcff = nt * (1 - rr) + extra_term_cf
    tv = tfcff / (wt - g)
    return pv + tv * df[-1]


ROWS = []


def rec(tag, what, val, frame_a=None, note=''):
    ROWS.append(dict(tag=tag, what=what, centre=val, d=val - B_C, pct=(val / B_C - 1),
                     frame_a=frame_a, note=note))


# ---------------------------------------------------------------- input-level re-runs
OVERRIDES = [
    ('A6/B-', 'provision at the stated three-year average 6.5161%', {'prov_pct_permanent': 0.0651609}),
    ('A18/B2', 'terminal ROIC at the model FY2030 ROIC 16.36%', {'roic_term': 0.1636}),
    ('A17/B-', 'FCFF taxed at the model effective rate 23.5%', {'tax_stat': 0.235}),
    ('A11/B10', 'risk-free at the 6-Aug observable print 23.00%', {'rf': 0.2300}),
    ('D5', 'risk-free at the CBE May-26 auction weighted average 23.407%', {'rf': 0.23407}),
    ('A19/B-', 'terminal risk-free at 9.5% (5% inflation + real GDP 4.5%)', {'rf_term': 0.095}),
    ('B3a', 'terminal debt weight at the market-value reading 25.1%', {'wd_term': 0.251}),
    ('B3b', 'terminal debt weight at the book reading 39.5%', {'wd_term': 0.395}),
    ('A15/B26', 'interest charged at the blended marginal rate on flat debt',
     {'int_path': [W['kd_blend'] * W['gross_debt']] * 5}),
    ('A22/B-', 'associate contribution at the Q1-2026 run-rate (13.118 x 4)',
     {'assoc_norm': S['inputs']['q1_assoc']['value'] * 4}),
    ('A5/B9a', 'sustainable return at the model FY2030 ROE', {}),   # filled below
    ('B22/A7', 'peer leg at the true midpoint of the two observations 21.35x',
     {'peer_pe_regional': 21.35}),
    ('D19', 'associate multiple at the listed associate MUP trailing 9.33x',
     {'assoc_multiple': 9.33}),
]
base_roe30 = F['roe'][-1]
for tag, what, over in OVERRIDES:
    if tag == 'A5/B9a':
        continue
    d, err = run(over)
    if err:
        rec(tag, what + '  [FAILED: ' + err[:40] + ']', float('nan')); continue
    rec(tag, what, d['lenses']['fair_base'], d['dcf']['frame_A']['per_share'])

# A5 — sustainable return: roe_sust is computed in the model, so price it by substitution
# in the three places it lands (book multiple, justified multiple, implied payout).
ke_t, g = W['ke_term'], S['inputs']['g_term']['value']
for lbl, roe in [('the model FY2030 ROE %.2f%%' % (base_roe30 * 100), base_roe30),
                 ('the model 5-year mean ROE %.2f%%' % (float(np.mean(F['roe'])) * 100),
                  float(np.mean(F['roe'])))]:
    bk = ((roe - g) / (ke_t - g)) * L['bv_ps']
    jm = (1 - g / roe) / (ke_t - g)
    rel = float(np.mean([jm, L['own_pe_mean'], L['peer_adj_pe']])) * L['eps_fwd']
    nrm = L['norm_pat_ps'] * (1 - g / roe) / (ke_t - g)
    rec('A5/B9', 'sustainable return set to ' + lbl, centre(bk=bk, rel=rel, nrm=nrm))

# ------------------------------------------------------------------- structural re-derivations
# A3/B1 — de-average the two frames: publish two centres, each with its own frame-consistent EPS
for nm, fr, eps in [('Frame A only', B_A, L['eps_26_A']), ('Frame B only', B_B, L['eps_26_B'])]:
    rel = float(np.mean([L['just_fwd_pe'], L['own_pe_mean'], L['peer_adj_pe']])) * eps
    v = 0.50 * fr + w_bk * L['book_ps'] + w_rel * rel + w_nrm * L['norm_ps']
    rec('A3/B1', 'de-averaged headline — ' + nm, v, fr)

# A7/B22 — drop the peer leg entirely
rel = float(np.mean([L['just_fwd_pe'], L['own_pe_mean']])) * L['eps_fwd']
rec('A7/B22', 'relative lens with the unsourced peer leg deleted', centre(rel=rel))
# D2 — drop the model-derived justified multiple from the relative lens
rel = float(np.mean([L['own_pe_mean'], L['peer_adj_pe']])) * L['eps_fwd']
rec('D2', 'relative lens with the model-derived justified multiple deleted', centre(rel=rel))
# both intrinsic-contaminated legs out: own history only
rec('D2b', 'relative lens on the own four-year mean alone',
    centre(rel=L['own_pe_mean'] * L['eps_fwd']))

# A14 — period-match: trailing multiples on trailing EPS, forward multiple on forward EPS
rel = float(np.mean([L['just_fwd_pe'] * L['eps_fwd'],
                     L['own_pe_mean'] * L['eps_ttm'],
                     L['peer_adj_pe'] * L['eps_ttm']]))
rec('A14', 'trailing multiples applied to trailing EPS (period-matched)', centre(rel=rel))

# B4 — terminal NOPAT charged depreciation on the parked construction balance
cip_end, dep_rate, tax = F['cip'][-1], S['inputs']['dep_rate']['value'], S['inputs']['tax_stat']['value']
extra_dep = cip_end * dep_rate
for nm, fr, key in [('Frame A', B_A, 'frame_A'), ('Frame B', B_B, 'frame_B')]:
    fd = D[key]
    nt = fd['nopat_term'] - extra_dep * (1 - tax)
    ev = dcf(fd['nopat'], fd['fcff'], nopat_term=nt)
    if key == 'frame_A':
        a = bridge(ev)
    else:
        b = bridge(ev)
rec('B4', 'terminal NOPAT charged D&A on the parked construction balance (%.0fm)' % cip_end,
    centre(a=a, b=b), a)

# C1 — add the non-cash credit-loss provision back into FCFF and the terminal block
for key in ('frame_A', 'frame_B'):
    fd, prov = D[key], F['prov_A' if key == 'frame_A' else 'prov_B']
    fcff = [f + p for f, p in zip(fd['fcff'], prov)]
    ev = dcf(fd['nopat'], fcff, extra_term_cf=prov[-1] * (1 + g))
    if key == 'frame_A':
        a = bridge(ev)
    else:
        b = bridge(ev)
rec('C1', 'credit-loss provision added back to FCFF as a non-cash charge', centre(a=a, b=b), a)

# C2 / D1 — the consolidation-perimeter and stale-anchor bridge variants
nd_q1 = S['inputs']['q1_debt']['value'] - S['inputs']['q1_cash']['value']
nci_dec = S['inputs']['nci_fy25']['value']
VARIANTS = [
    ('C2', 'Dec-25 net debt held, NCI restored to the Dec-25 audited 288.7m',
     dict(nd=W['net_debt'], nci=nci_dec)),
    ('C2b', 'Dec-25 NCI 288.7m and the associate add-back at cost removed',
     dict(nd=W['net_debt'], nci=nci_dec, assoc=D['frame_A']['assoc_earnings_value'])),
    ('D1', 'bridge anchored on the 31-Mar-2026 net debt (%.0fm)' % nd_q1, dict(nd=nd_q1)),
    ('D1b', 'Mar-26 net debt AND the first year discounted three quarters', None),
]
for tag, what, kw in VARIANTS:
    if kw is None:
        continue
    a = bridge(D['frame_A']['ev_core'], **{**dict(assoc=D['frame_A']['assoc_value']), **kw})
    b = bridge(D['frame_B']['ev_core'], **{**dict(assoc=D['frame_B']['assoc_value']), **kw})
    rec(tag, what, centre(a=a, b=b), a)

# D1b — roll the DCF forward one quarter as the critic prescribes, then bridge on Mar-26 debt
df = np.array(W['df']) ** 0.0
for key in ('frame_A', 'frame_B'):
    fd = D[key]
    dfq = np.array(W['df']) * (1 + np.array(W['disc_rate'])) ** 0.25
    pv = float(np.dot(np.array(fd['fcff']), dfq))
    tv = fd['tv'] * dfq[-1]
    ev = pv + tv
    v = bridge(ev, assoc=fd['assoc_value'], nd=nd_q1)
    if key == 'frame_A':
        a = v
    else:
        b = v
rec('D1b', 'Mar-26 net debt with the explicit period rolled forward one quarter',
    centre(a=a, b=b), a)

# C3 — normalised earnings lens carrying the model's own FY2027 finance cost
norm_ebit = L['norm_margin'] * F['revenue'][1]
int27 = S['inputs']['int_path']['value'][1]
nrm_pat = (norm_ebit - int27) * (1 - S['inputs']['tax_eff_fwd']['value']) + \
    S['inputs']['assoc_norm']['value'] - F['nci_fwd']
nrm_ps = (nrm_pat / SH) * L['payout_implied'] / (ke_t - g)
rec('C3', 'normalised lens charged the model FY2027 finance cost (EPS %.2f)' % (nrm_pat / SH),
    centre(nrm=nrm_ps))

# ----------------------------------------------------------------------------- report
print(f"BASELINE  centre {B_C:.4f}  Frame A {B_A:.4f}  Frame B {B_B:.4f}\n")
print(f"{'tag':9s} {'finding priced':70s} {'centre':>8s} {'d/sh':>8s} {'% centre':>9s} {'Frame A':>8s}")
for r in sorted(ROWS, key=lambda x: -abs(x['pct'])):
    fa = f"{r['frame_a']:8.2f}" if r['frame_a'] is not None else f"{'—':>8s}"
    print(f"{r['tag']:9s} {r['what'][:70]:70s} {r['centre']:8.2f} {r['d']:+8.2f} "
          f"{r['pct'] * 100:+8.2f}% {fa}")
json.dump(ROWS, open(os.path.join(HERE, 'audit_pricing_2.json'), 'w'), indent=1)
