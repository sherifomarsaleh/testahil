"""SCEM beta — THE SANCTIONED ROUTE, replacing this study's composite regression.

WHAT WAS HERE AND WHY IT WAS WRONG. This file hand-rolled a five-year weekly
regression of SCEM against an EQUAL-WEIGHT COMPOSITE of the 31 names that happen to
sit in engine/raw_ohlc/EG/ — and it said so in its own docstring, calling the
composite "the house pattern". It was the house pattern: every study in this
repository once did it, each copying the last. SIGCM clause 6 calls a constituent
composite a HARD FAIL and not a fallback, for reasons that are facts about the object
rather than preferences — a basket of the names this engine happens to cover changes
whenever a stock is posted, mixes exchanges inside one market code, and shares
constituents with the panel it prices. It is a coverage artefact, not a market.

WHAT IT COST HERE IS NOT THE NUMBER, AND THAT IS THE INTERESTING PART. This study
already adopts a beta of 1.00 and says why: the own-stock regression FAILS the usability
gate, so tier 1 is unavailable and the fallback is taken. That conclusion was right. It
was reached on the WRONG MEASUREMENT — the composite regression's R-squared of 0.038 —
and the conforming regression against the exchange's own published index gives 0.024,
which fails the same gate harder. A fallback justified by the wrong statistic is a
fallback nobody can check, even when the fallback is correct.

SO THE VALUE DOES NOT MOVE AND THE RECORD DOES. Against EGX30 this stock's beta is 0.5910
with an R-squared of 0.024 over 255 weekly observations and a 90% interval of [0.134,
1.048] — an interval that contains 1.00, which is what makes the fallback defensible
rather than merely conservative. Against the composite it was 0.4852 at 0.038. Both fail;
only one of them is a regression against a market.

NOTHING HERE HAND-ROLLS A REGRESSION. beta_regression.own_stock_beta() resolves the
regressor itself from the exchange the stock is listed on (EGX -> EGX30, read from the
registered series under engine/raw_indices/), runs the data-quality gate on BOTH
series, matches the weekly grid to that exchange's real trading week, applies the
Dimson correction for thin trading, and returns the provenance WITH the number — the
index file, its as-of date, the market, the exchange and the conforming flag — so
assert_beta_provenance() can inspect the record rather than trust a boolean the study
set on itself.

THE WITHDRAWN NUMBER IS KEPT, NOT DELETED, because a correction whose size nobody can
see is a correction nobody can check.

    python3 beta_reg.py        writes beta_result.json
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from beta_regression import own_stock_beta                      # noqa: E402

WITHDRAWN = {
    "beta": 0.4852,
    "r2": 0.038,
    "n": 256,
    "se": 0.153,
    "regressor": "32-name equal-weight composite of the covered EGX library, SCEM excluded from its own index",
    "why_withdrawn": (
        "A constituent composite is a coverage artefact rather than a market: it "
        "changes whenever a stock is posted, it mixes exchanges inside one market "
        "code, and it shares constituents with the panel it prices. SIGCM clause 6 "
        "calls it a hard fail, not a fallback, and the published index of the "
        "exchange the stock is listed on is held in this repository, so there was "
        "never a sourcing obstacle — only an inherited pattern."),
}

res = own_stock_beta('SCEM', 'EG', 'EGX')
res = dict(res)
res['withdrawn_composite'] = WITHDRAWN
res['delta_vs_withdrawn'] = float(res['beta'] / WITHDRAWN['beta'] - 1.0)

# THE CONFORMING ROUTE IS THE ONLY ROUTE, AND THE ANSWER IT RETURNS HERE IS "NOT USABLE".
# That is a result rather than an obstacle: the hierarchy names what happens next, and
# what may not happen is keeping a composite number because the conforming one failed.
assert res.get('conforming'), (
    'own_stock_beta returned a NON-CONFORMING record for SCEM: %r. Stop and inform '
    'rather than proceed — an interim or composite regressor is not a tier.'
    % (res.get('interim_note') or res.get('index_file')))
res['tier'] = 1 if res.get('usable') else 3
res['adopted_beta'] = float(res['beta']) if res.get('usable') else 1.00
res['tier_reason'] = (
    "TIER 1 UNAVAILABLE: %s. Tier 2 is a same-country peer beta, and the only other "
    "Egyptian cement issuer this repository holds a price library for is ARCC, whose own "
    "conforming regression fails the SAME gate (R-squared 0.047) — a peer beta built on an "
    "unusable regression is the same unusable number wearing another company's name, so "
    "tier 2 cannot be assembled from what is held rather than being skipped. TIER 3 is "
    "taken: beta = 1.00, which the conforming regression's own 90%% interval [%.3f, %.3f] "
    "contains. The point estimate of %.4f is published beside it and is NOT used."
    % (res.get('gate_msg'), res['ci90'][0], res['ci90'][1], res['beta'])) \
    if not res.get('usable') else "TIER 1: the own-stock regression clears the gate."
assert str(res.get('index_file', '')).startswith('raw_indices/'), (
    'the regressor is not a registered published index: %r' % res.get('index_file'))

json.dump(res, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1, default=str)

print('regression beta {0:.4f} | R2 {1:.3f} | n {2} | SE {3:.4f} | CI90 [{4:.3f}, {5:.3f}]'
      .format(res['beta'], res['r2'], res['n'], res['se'], res['ci90'][0], res['ci90'][1]))
print('   ADOPTED beta {0:.2f} at tier {1}'.format(res['adopted_beta'], res['tier']))
print('   ' + res['tier_reason'])
print('   regressor {0} as at {1}; conforming={2}; usable={3} ({4})'
      .format(res['index_file'], res['index_asof'], res['conforming'], res['usable'],
              res['gate_msg']))
print('   WITHDRAWN composite beta {0:.4f} (R2 {1:.3f}) — the conforming regressor is '
      '{2:+.1%} against it and explains {3:+.3f} more of the stock'
      .format(WITHDRAWN['beta'], WITHDRAWN['r2'], res['delta_vs_withdrawn'],
              res['r2'] - WITHDRAWN['r2']))
