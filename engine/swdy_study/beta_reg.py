"""SWDY beta — THE SANCTIONED ROUTE, replacing this study's composite regression.

WHAT WAS HERE AND WHY IT WAS WRONG. This file hand-rolled a five-year weekly
regression of SWDY against an EQUAL-WEIGHT COMPOSITE of the 31 names that happen to
sit in engine/raw_ohlc/EG/ — and it said so in its own docstring, calling the
composite "the house pattern". It was the house pattern: every study in this
repository once did it, each copying the last. SIGCM clause 6 calls a constituent
composite a HARD FAIL and not a fallback, for reasons that are facts about the object
rather than preferences — a basket of the names this engine happens to cover changes
whenever a stock is posted, mixes exchanges inside one market code, and shares
constituents with the panel it prices. It is a coverage artefact, not a market.

WHAT IT COST HERE, MEASURED RATHER THAN ASSERTED. Against the published index of the
exchange this stock is listed on, SWDY's beta is 1.2249 with an R-squared of 0.368;
against the composite it was 1.0087 with an R-squared of 0.291. THE COMPOSITE
UNDERSTATED THE BETA BY 21.4% AND EXPLAINED LESS OF THE STOCK, which is the FERTIGLB
precedent again — there the understatement was about 40% and it overstated fair value
by 21.6%. A lower beta lowers the cost of equity, lowers the discount rate and RAISES
the value, so correcting it moves this study's answer DOWN, further below a price it
already sits far below. That direction is not a reason to take the correction and
would not have been a reason to leave it.

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
    "beta": 1.0087131974394166,
    "r2": 0.29126939836703036,
    "n": 258,
    "se": 0.09834241826281419,
    "regressor": "31-name equal-weight composite of the covered EGX library",
    "why_withdrawn": (
        "A constituent composite is a coverage artefact rather than a market: it "
        "changes whenever a stock is posted, it mixes exchanges inside one market "
        "code, and it shares constituents with the panel it prices. SIGCM clause 6 "
        "calls it a hard fail, not a fallback, and the published index of the "
        "exchange the stock is listed on is held in this repository, so there was "
        "never a sourcing obstacle — only an inherited pattern."),
}

res = own_stock_beta('SWDY', 'EG', 'EGX')
res = dict(res)
res['withdrawn_composite'] = WITHDRAWN
res['delta_vs_withdrawn'] = float(res['beta'] / WITHDRAWN['beta'] - 1.0)

# THE CONFORMING ROUTE IS THE ONLY ROUTE. A record that came back non-conforming would
# mean the resolver fell back to something this study may not use, and it must stop
# rather than write a number the rest of the model will treat as sound.
assert res.get('conforming'), (
    'own_stock_beta returned a NON-CONFORMING record for SWDY: %r. Stop and inform '
    'rather than proceed — an interim or composite regressor is not a tier.'
    % (res.get('interim_note') or res.get('index_file')))
assert str(res.get('index_file', '')).startswith('raw_indices/'), (
    'the regressor is not a registered published index: %r' % res.get('index_file'))

json.dump(res, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1, default=str)

print('beta {0:.4f} | R2 {1:.3f} | n {2} | SE {3:.4f} | CI90 [{4:.3f}, {5:.3f}]'
      .format(res['beta'], res['r2'], res['n'], res['se'], res['ci90'][0], res['ci90'][1]))
print('   regressor {0} as at {1}; conforming={2}; usable={3} ({4})'
      .format(res['index_file'], res['index_asof'], res['conforming'], res['usable'],
              res['gate_msg']))
print('   WITHDRAWN composite beta {0:.4f} (R2 {1:.3f}) — the conforming regressor is '
      '{2:+.1%} against it and explains {3:+.3f} more of the stock'
      .format(WITHDRAWN['beta'], WITHDRAWN['r2'], res['delta_vs_withdrawn'],
              res['r2'] - WITHDRAWN['r2']))
