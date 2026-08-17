#!/usr/bin/env python3
"""MODON beta — TIER 1, produced by the HOUSE module, not a study-local regression.

Revisions 1 and 2 regressed against a study-local equal-weight composite because the
official index could not be obtained. Revision 3 first replaced that with a study-local
regression against the official series — better, but still study-local. This file now
calls engine/beta_regression.own_stock_beta(), which is the shared implementation the
standing rule points at: it resolves the regressor through raw_indices/, screens both
series with the same data-quality gate, applies the Dimson lead-lag correction (which
matters here — 84.75% of the shares sit with one holder, so non-synchronous trading
biases a naive OLS beta DOWNWARD), and returns a provenance record that
research_protocol.assert_beta_provenance() can inspect.

Writes beta_official.json for compute.py to read. No number is typed by hand.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from beta_regression import own_stock_beta                      # noqa: E402
from research_protocol import assert_beta_provenance            # noqa: E402

TICKER, MARKET, EXCHANGE = 'MODON', 'AE', 'ADX'


def main():
    rec = own_stock_beta(TICKER, MARKET, EXCHANGE, years=5)
    assert_beta_provenance(rec)
    print(f'BETA PROVENANCE: PASS — regressor {rec["index_file"]} '
          f'(as of {rec["index_asof"]}), conforming={rec["conforming"]}')

    # The naive (non-Dimson) reading on the same weeks, reported so the thin-trading
    # correction is visible rather than buried inside a default argument.
    naive = own_stock_beta(TICKER, MARKET, EXCHANGE, years=5, dimson=False)

    print(f'\n{"reading":<34}{"beta":>8}{"SE":>8}{"R2":>8}{"n":>6}  gate')
    for label, r in (('Dimson-corrected (adopted)', rec), ('naive OLS, same weeks', naive)):
        print(f'{label:<34}{r["beta"]:>8.3f}{r["se"]:>8.3f}{r["r2"]:>8.3f}{r["n"]:>6d}'
              f'  {"PASS" if r["usable"] else "FAIL"}')
    print(f'\nthin-trading correction is worth {rec["beta"] - naive["beta"]:+.3f} of beta '
          f'({(rec["beta"] - naive["beta"]) / naive["se"]:.2f} standard errors of the naive '
          f'estimate) — MODON\'s free float is thin (84.75% held by one entity), which is '
          f'exactly the condition Dimson corrects')
    print(f'Blume cross-check: {rec["blume_crosscheck"]:.3f}')
    print(f'90% CI on the adopted beta: [{rec["ci90"][0]:.3f}, {rec["ci90"][1]:.3f}]')
    if rec['weak']:
        print('WEAK-INSTRUMENT FLAG is set — the study must label this beta as such '
              'everywhere it supports a conclusion')

    out = dict(adopted_beta=round(rec['beta'], 3),
               record={k: v for k, v in rec.items() if k != 'notes'},
               naive={k: naive[k] for k in ('beta', 'se', 'r2', 'n')},
               index_name='FTSE ADX General Index')
    with open(os.path.join(HERE, 'beta_official.json'), 'w') as fh:
        json.dump(out, fh, indent=1, default=str)
    print('\nwrote beta_official.json')


if __name__ == '__main__':
    main()
