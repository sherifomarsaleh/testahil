"""Corrections, under BOTH clauses, and the adjusted-versus-raw test by origin.

Expanding window only: a correction applied at origin o is estimated from the cells that
had RESOLVED before o, never from the cell it is about to score. Half strength by
default. Applied only where the bias holds its sign AT EVERY CUT THE DATA ADMITS
[R-FCAL-01 AMENDED 07-09-2026] — the era boundary alone is not the test — and only where
the block-bootstrap interval excludes zero.

THE SECOND CLAUSE IS NOT A FORMALITY. A correction enters the live drivers only if it
passes its own test AND is consistent with how that driver class is built across this
market's book. Where the first test passes and the second does not, the finding is a
SPECIFICATION defect and no multiplier may hide it — that clause has already done its
job once in this book, on a finance-cost correction that was arithmetic wearing the
costume of evidence.
"""
import json, os, sys, math, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bottom_up as B
import score as S

OUT = os.path.join(HERE, 'corrections_log.json')
STRENGTH = 0.5


def main():
    cells = json.load(open(os.path.join(HERE, 'error_cells.json')))['cells']
    diag = json.load(open(os.path.join(HERE, 'diagnostics.json')))
    scores = json.load(open(os.path.join(HERE, 'scores.json')))['drivers']
    stab = diag['stability']

    candidates, declined = [], []
    for k, sc in scores.items():
        if not sc.get('n'):
            continue
        st = stab.get(k, {})
        ci = sc.get('ci')
        reasons = []
        if st.get('flips'):
            reasons.append('the sign flips at %d of %d admissible cuts — an instability, '
                           'not a bias [R-FCAL-01 AMENDED 07-09-2026]'
                           % (len(st['flips']), st['n_cuts']))
        if not st.get('n_cuts'):
            reasons.append('UNTESTABLE — no cut leaves five cells each side, and an '
                           'absence of contrary evidence is not evidence [R-ENF-04]')
        if ci and ci['lo'] <= 0 <= ci['hi']:
            reasons.append('the block-bootstrap interval [%.3f, %.3f] covers zero'
                           % (ci['lo'], ci['hi']))
        if abs(sc['bias']) < 0.05:
            reasons.append('the bias is under 5 log points and is not worth correcting')
        (declined if reasons else candidates).append(
            dict(driver=k, bias=sc['bias'], ci=ci, cuts=st.get('n_cuts'),
                 flips=len(st.get('flips', [])), reasons=reasons))

    # ---- the expanding-window test, adjusted against raw, BY ORIGIN --------
    results = []
    for cand in candidates:
        k = cand['driver']
        ks = sorted([c for c in cells if c['driver'] == k], key=lambda c: c['origin'])
        by_origin = []
        for o in sorted({c['origin'] for c in ks}):
            prior = [c['e'] for c in ks if c['target'] < o]      # RESOLVED before o
            if len(prior) < 3:
                continue
            adj = -STRENGTH * (sum(prior) / len(prior))
            here = [c for c in ks if c['origin'] == o]
            raw_mae = sum(abs(c['e']) for c in here) / len(here)
            adj_mae = sum(abs(c['e'] + adj) for c in here) / len(here)
            by_origin.append(dict(origin=o, n=len(here), prior_cells=len(prior),
                                  adjustment_log=adj, raw_mae=raw_mae, adj_mae=adj_mae,
                                  improved=adj_mae < raw_mae))
        if by_origin:
            imp = sum(1 for r in by_origin if r['improved'])
            results.append(dict(driver=k, bias=cand['bias'], ci=cand['ci'],
                                cuts=cand['cuts'], strength=STRENGTH,
                                by_origin=by_origin, origins=len(by_origin),
                                improved_origins=imp,
                                mean_raw_mae=sum(r['raw_mae'] for r in by_origin) / len(by_origin),
                                mean_adj_mae=sum(r['adj_mae'] for r in by_origin) / len(by_origin),
                                # CLAUSE 1 REQUIRES BOTH, and the first draft required
                                # only the count. A majority of origins can improve while
                                # the MEAN error RISES, because the origins that get worse
                                # get worse by more - which is exactly what the contracting
                                # legs do here (5 of 8 origins improve and mean MAE goes
                                # 0.256 to 0.282). A correction that raises the average
                                # error has not passed anything, and a test that calls it
                                # a pass is the wrong test [R-COC-01].
                                clause_1=('PASS' if (imp > len(by_origin) / 2 and
                                                     sum(r['adj_mae'] for r in by_origin)
                                                     < sum(r['raw_mae'] for r in by_origin))
                                          else 'FAIL')))

    # ---- CLAUSE 2, the one that is not a formality -------------------------
    CLAUSE_2 = {
     'D1_cable_volume_t': dict(
        verdict='WATCH FLAG',
        why='Clause 1 passes and the sample does not support acting on it. The '
            'expanding window leaves THREE origins with three or more resolved cells, '
            'because the investor sheets that publish cable tonnage stop in 2022 and '
            'the unit window closes at FY2020. Three origins of one issuer is not a '
            'population, and an absence of contrary evidence is not evidence [R-ENF-04]. '
            'Recorded, graded live, acted on by nobody.'),
     'D5_contracting_revenue': dict(
        verdict='DECLINED',
        why='Clause 1 fails on the measurement that matters: five of eight origins '
            'improve while the MEAN absolute error RISES from 0.256 to 0.282. A '
            'correction that raises the average error has not passed anything.'),
     'D8_contracting_cost': dict(
        verdict='DECLINED',
        why='As D5, and for the same arithmetic: five of eight origins improve while '
            'the mean absolute error rises from 0.268 to 0.272.'),
     'D11_depreciation': dict(
        verdict='DECLINED — SPECIFICATION DEFECT, NOT A BIAS',
        why='Clause 1 passes emphatically: five origins of five improve and mean MAE '
            'falls from 0.820 to 0.373, which is the single largest improvement any '
            'candidate offers. IT MUST NOT BE ADOPTED, because the driver is wired '
            'wrong and the multiplier would hide it. The rule rolls PP&E forward at '
            'historical cost plus capex less cost over the disclosed life, and the '
            'reported charge is struck on a base that ALSO carries the translation of '
            'foreign subsidiaries: note 17 of the FY2025 statements adds EGP 9,941,876,468 '
            'to the cost of machinery in FY2024 as an "effect of movement in exchange '
            'rates" alone, against additions of EGP 2,061,542,102. A roll-forward that '
            'models the additions and not the translation must under-forecast on a '
            'currency that halved, and it will do so in a NEW way next year rather than '
            'the way the correction was fitted to. The house builds depreciation off a '
            'PP&E roll-forward everywhere in this book and none of those roll-forwards '
            'carries a translation term either, so this fails the second clause on its '
            'own terms. [R-FCAL-01]: a specification error is not a calibration one and '
            'no correction factor may hide it.'),
     'D12_capex': dict(verdict='DECLINED', why='clause 1 fails: four of eight origins.'),
     'D13_other_operating_income': dict(
        verdict='WATCH FLAG',
        why='The rule holds this line flat and was DECLARED equal to FREEZE in advance, '
            'so a correction here changes the RULE rather than calibrating it. Other '
            'operating income is not a driver class this book builds consistently '
            'anywhere - it is a residual of disposals, grants and reversals - so the '
            'second clause has nothing to be consistent WITH. Recorded, graded live.'),
     'D15_finance_costs': dict(
        verdict='DECLINED — SPECIFICATION DEFECT, NOT A BIAS',
        why='Clause 1 passes on seven origins of eight. IT MUST NOT BE ADOPTED, and this '
            'is [L-002] arriving in a new costume. The rule holds the finance charge flat '
            'at the origin, which is a flat DEBT BOOK; SWDY\'s interest-bearing '
            'borrowings went from EGP 6.6bn at FY2014 to EGP 62.5bn at FY2025, nine and a '
            'half times, while the borrowing rate on the borrowings that actually bear it '
            'went from 5.79% to 9.37%. The 88 log points of "bias" are the growth of the '
            'debt book, which the rule does not model. ACROSS THIS MARKET\'S BOOK the '
            'house builds finance cost as rate x interest-bearing borrowings - it is the '
            'first trap [R-FCAL-01] names - so a multiplier on a flat charge is '
            'inconsistent with every other name here. A correction factor is honest when '
            'the model is right and reality is awkward; when the model is wrong it hides '
            'the model.'),
     'D16_finance_income': dict(verdict='DECLINED', why='clause 1 fails: four of eight origins.'),
    }
    for r in results:
        c2 = CLAUSE_2.get(r['driver'], dict(verdict='DECLINED', why='no clause-2 ruling recorded'))
        r['clause_2'] = c2['verdict']
        r['clause_2_reason'] = c2['why']
        r['adopted'] = (r['clause_1'] == 'PASS' and c2['verdict'] == 'ADOPTED')

    out = dict(_='SWDY corrections, both clauses. INTERNAL.', built='2026-09-07',
               strength=STRENGTH, candidates=results, declined=declined,
               adopted=[r['driver'] for r in results if r['adopted']],
               watch_flags=[r['driver'] for r in results
                            if r['clause_2'] == 'WATCH FLAG'])
    json.dump(out, open(OUT, 'w'), indent=1)

    print('DECLINED BEFORE ANY TEST (%d):' % len(declined))
    for d in declined:
        print('  %-28s bias %+.3f — %s' % (d['driver'], d['bias'], d['reasons'][0]))
    print('\nCLAUSE 1 — expanding-window, half strength, adjusted vs raw BY ORIGIN (%d):'
          % len(results))
    for r in results:
        print('  %-28s bias %+.3f  %d origins, improved %d, MAE %.3f -> %.3f   %s'
              % (r['driver'], r['bias'], r['origins'], r['improved_origins'],
                 r['mean_raw_mae'], r['mean_adj_mae'], r['clause_1']))
    print('\nCLAUSE 2 — consistency with how the class is built across this market\'s book:')
    for r in results:
        print('  %-28s %s' % (r['driver'], r['clause_2']))
    print('\nADOPTED: %s' % (out['adopted'] or 'NONE'))
    print('WATCH FLAGS: %s' % (out['watch_flags'] or 'none'))
    return out


if __name__ == '__main__':
    main()
