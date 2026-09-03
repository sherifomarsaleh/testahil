"""The terminal-value census — [R-TERM-01]'s measurement, and it runs before any treatment.

WHY THIS EXISTS. Every study in this book discounts an explicit window and then
capitalises a terminal, and most of them build that terminal from the reinvestment
identity g = rr x ROIC:

    rr = g / ROIC,   ROIC = NOPAT / IC,   TV = NOPAT (1 - rr) / (W - g)

Substitute and the reinvestment charge collapses to a constant that does not depend on
ROIC at all:

    TV = [ NOPAT - g . IC ] / (W - g)

So the construction charges g x IC every year for ever. THE IDENTITY IS A STATEMENT
ABOUT REAL GROWTH. Where g is a nominal rate whose real component is zero — which is
what the house macro path returns for every terminal it builds [R-MACRO-01] — the charge
buys no capacity at all, and the model is paying for what inflation supplies free.

THE DIAGNOSTIC THAT MAKES IT VISIBLE. Read the charge as a capital-maintenance
programme and ask how long it takes to replace the asset base:

    implied replacement cycle  =  IC / charge  =  IC / (g . IC)  =  1 / g

The implied asset life is THE RECIPROCAL OF THE INFLATION RATE. It has nothing to do
with the asset. At 7% terminal inflation it is 14.3 years; at 15% it is 6.7. A cement
kiln does not get younger because the currency got worse. That single number is what this
census computes, name by name, and it is why the defect is a class and not an accident:
the higher a market's inflation, the more brutal the charge, which is the exact opposite
of prudence.

THE FLOOR, which needs no opinion at all. A company can always decline to invest beyond
maintenance and pay the rest out. So a terminal can never be worth less than a no-growth
perpetuity on the same profit:

    TV  >=  NOPAT_last / W

That is a dominance argument, not a judgement: it has no parameters, so there is nothing
in it to tune. A terminal below its own floor is dominated by a policy the company can
choose unilaterally, and the study has published the worse of two worlds.

READING THIS OUTPUT. It measures; it does not correct. Every figure is resolved from each
study's OWN committed numbers file and the census RECORDS THE KEY THAT ANSWERED, so a
study whose terminal cannot be read comes back UNREADABLE rather than clean — an empty
result is not a clean result [R-ENF-04]. Nothing here is an input to any study.
"""
from __future__ import annotations

import json
import math
import os
from glob import glob

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Candidate keys, in preference order. A study is read through the FIRST one present and
# the census reports which — a resolver that silently guesses is the species of defect
# [R-ENF-04] exists to close.
CAND = {
    'tv':        ('tv', 'terminal_value', 'tv_value'),
    'pv_tv':     ('pv_tv', 'pv_terminal'),
    'tv_share':  ('tv_share', 'tv_pct'),
    'wacc_term': ('wacc_term', 'wacc_terminal', 'wacc_T'),
    # 'g' is where studies diverge most: some name it in the DCF, some only in the macro
    # record, some only in a case's inputs. Every route is listed and the census reports
    # WHICH answered, because a resolver that guesses is the defect [R-ENF-04] closes.
    'g':         ('g_term', 'g_terminal', 'terminal_g', 'terminal_growth',
                  'growth_at_horizon_end', 'TERMINAL_GROWTH', 'tg', 'g'),
    'nopat_term':('nopat_term', 'nopat_t1', 'nopat_next', 'terminal_nopat'),
    'ic':        ('ic_repl', 'ic_replacement', 'ic_terminal', 'ic_T', 'invested_capital',
                  'ic_replacement_cost'),
    'rr_term':   ('rr_term', 'rr_T', 'rr_repl', 'reinvest'),
    'df_tv':     ('df_tv', 'dftv'),
    'equity':    ('equity', 'eq_val', 'eq_attr', 'eq'),
    'fv':        ('fv', 'ps', 'per_share', 'fv_aed'),
}
# Where a study nests its DCF under a case or framing rather than a bare 'dcf'.
DCF_HOLDERS = ('dcf', 'dcf_A', 'dcf_B', 'dcf.frame_A', 'dcf.base_ct', 'cases.base',
               'framings.normalisation', 'wacc', 'macro_record',
               'cost_of_capital_record', 'model_parameters')


def _flat(o, path='', out=None):
    """Every numeric leaf, keyed by dotted path. Lists are indexed."""
    out = {} if out is None else out
    if isinstance(o, dict):
        for k, v in o.items():
            p = f'{path}.{k}' if path else k
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                out[p] = float(v)
            elif isinstance(v, (dict, list)):
                _flat(v, p, out)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            p = f'{path}[{i}]'
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                out[p] = float(v)
            elif isinstance(v, (dict, list)):
                _flat(v, p, out)
    return out


def _resolve(flat, names, prefer=DCF_HOLDERS):
    """First candidate present, preferring a DCF-ish container. Returns (value, key)."""
    for n in names:
        # a container-qualified hit first, so dcf.tv beats sensitivity.rows[3].tv
        for pre in prefer:
            k = f'{pre}.{n}'
            if k in flat:
                return flat[k], k
        # then any leaf whose FINAL segment is exactly this name
        hits = [k for k in flat if k.split('.')[-1] == n]
        if len(hits) == 1:
            return flat[hits[0]], hits[0]
        if hits:
            # deterministic: shortest path wins, ties broken lexically
            hits.sort(key=lambda k: (k.count('.'), len(k), k))
            return flat[hits[0]], hits[0]
    return None, None


def _last_explicit(flat, field):
    """The last explicit-window value of a forecast row (forecast.nopat[-1] and kin)."""
    idx = [(int(k.split('[')[-1].rstrip(']')), k) for k in flat
           if k.split('[')[0].split('.')[-1] == field and k.endswith(']')]
    if not idx:
        return None, None
    idx.sort()
    return flat[idx[-1][1]], idx[-1][1]


def read_study(d):
    """One study's terminal, or a stated reason it cannot be read."""
    tk = os.path.basename(d)[:-6].upper()
    f = os.path.join(d, 'study_numbers.json')
    rec = {'ticker': tk, 'dir': os.path.relpath(d, REPO), 'routes': {}}
    if not os.path.exists(f):
        rec['unreadable'] = 'no committed numbers file'
        return rec
    try:
        n = json.load(open(f))
    except Exception as e:
        rec['unreadable'] = f'numbers file will not parse: {e}'
        return rec
    flat = _flat(n)
    for name, cands in CAND.items():
        v, k = _resolve(flat, cands)
        if v is not None:
            rec[name] = v
            rec['routes'][name] = k
    for field in ('nopat', 'dna', 'capex', 'dwc', 'fcff'):
        v, k = _last_explicit(flat, field)
        if v is not None:
            rec[f'{field}_last'] = v
            rec['routes'][f'{field}_last'] = k
    # the terminal WACC often lives only in a forecast row of forward rates
    if 'wacc_term' not in rec:
        v, k = _last_explicit(flat, 'fwd_wacc')
        if v is not None:
            rec['wacc_term'], rec['routes']['wacc_term'] = v, k

    missing = [x for x in ('tv', 'wacc_term', 'g') if x not in rec]
    if missing:
        rec['unreadable'] = 'the terminal exposes no ' + ', '.join(missing)
        return rec
    W, g, tv = rec['wacc_term'], rec['g'], rec['tv']
    if not (0.0 < W < 1.0):
        rec['unreadable'] = f'terminal rate {W} is not a rate'
        return rec
    if g >= W:
        rec['unreadable'] = f'terminal growth {g:.4f} is not below the terminal rate {W:.4f}'
        return rec

    # The numerator the published terminal actually capitalises.
    rec['fcff_term_implied'] = tv * (W - g)
    N = rec.get('nopat_term')
    if N is None and 'nopat_last' in rec:
        N = rec['nopat_last'] * (1.0 + g)
        rec['nopat_term'] = N
        rec['routes']['nopat_term'] = rec['routes']['nopat_last'] + f' x (1+g)  [derived]'
    if N is not None and N > 0:
        rec['charge'] = N - rec['fcff_term_implied']
        rec['charge_share_of_nopat'] = rec['charge'] / N
        if rec.get('ic') and rec['charge'] > 0:
            rec['implied_cycle_years'] = rec['ic'] / rec['charge']
        rec['one_over_g'] = 1.0 / g if g > 0 else math.inf
        # the floor: zero nominal growth, maintenance at book D&A, full payout
        base = rec.get('nopat_last', N / (1.0 + g))
        rec['floor'] = base / W
        rec['tv_vs_floor'] = tv / rec['floor'] - 1.0
        rec['below_floor'] = tv < rec['floor']
    return rec


def census():
    return [read_study(d) for d in sorted(glob(os.path.join(REPO, 'engine', '*_study')))]


def _fv_at(rec, tv_new):
    """What the study's own fair value becomes at a different terminal, all else equal."""
    if not all(k in rec for k in ('df_tv', 'equity', 'fv')) or not rec['fv']:
        return None
    sh = rec['equity'] / rec['fv']
    return (rec['equity'] + (tv_new - rec['tv']) * rec['df_tv']) / sh


def report():
    rows = census()
    read = [r for r in rows if 'unreadable' not in r]
    dark = [r for r in rows if 'unreadable' in r]
    print('THE TERMINAL-VALUE CENSUS  [R-TERM-01]')
    print('   every study\'s own committed terminal, re-expressed as the charge it levies')
    print(f'   {len(rows)} study directories · {len(read)} readable · {len(dark)} not\n')

    scored = [r for r in read if 'charge' in r]
    print(f"  {'ticker':<12}{'g':>7}{'W':>8}{'charge/NOPAT':>13}{'cycle yrs':>11}{'1/g':>7}"
          f"{'TV vs floor':>13}")
    print('  ' + '-' * 71)
    for r in sorted(scored, key=lambda r: r.get('tv_vs_floor', 9e9)):
        cyc = r.get('implied_cycle_years')
        print(f"  {r['ticker']:<12}{r['g']:>6.1%}{r['wacc_term']:>8.2%}"
              f"{r['charge_share_of_nopat']:>12.1%}"
              f"{(f'{cyc:.1f}' if cyc else '—'):>11}{r['one_over_g']:>7.1f}"
              f"{r['tv_vs_floor']:>+12.1%}"
              f"{'  BELOW ITS OWN FLOOR' if r.get('below_floor') else ''}")

    below = [r for r in scored if r.get('below_floor')]
    print(f'\n  BELOW THE FLOOR — a terminal worth less than not investing at all: '
          f'{len(below)} of {len(scored)}')
    for r in sorted(below, key=lambda r: r['tv_vs_floor']):
        fv0, fv1 = r.get('fv'), _fv_at(r, r['floor'])
        px = f'   {fv0:.2f} -> {fv1:.2f} at the floor' if (fv0 and fv1) else ''
        print(f"    {r['ticker']:<12}{r['tv_vs_floor']:>+8.1%}{px}")

    cyc = [r for r in scored if r.get('implied_cycle_years')]
    print(f'\n  THE IMPLIED REPLACEMENT CYCLE IS 1/g, NOT AN ASSET FACT — '
          f'{len(cyc)} studies expose both:')
    for r in sorted(cyc, key=lambda r: r['implied_cycle_years']):
        d = r['implied_cycle_years'] / r['one_over_g'] - 1.0
        print(f"    {r['ticker']:<12}{r['implied_cycle_years']:>7.1f} years against 1/g of "
              f"{r['one_over_g']:>5.1f}   ({d:+.1%})")

    if dark:
        print(f'\n  NOT READABLE ({len(dark)}) — tracked, because an unreadable answer is '
              f'not a clean one [R-ENF-04]:')
        for r in dark:
            print(f"    {r['ticker']:<12}{r['unreadable']}")
    return rows


if __name__ == '__main__':
    report()
