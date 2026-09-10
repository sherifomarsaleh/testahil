#!/usr/bin/env python3
"""ADIB-Egypt — the beta, written out where a gate outside the study can read it.

THIS FILE RUNS NO REGRESSION. It calls beta_regression.own_stock_beta(), which resolves
the regressor itself, runs the data-quality gate on both series, matches the weekly grid
to the exchange's real trading week and returns the provenance with the number. Every
study in this repository once hand-rolled its own regression against an equal-weight
composite of the covered names; on one name that understated beta by about 40% and
overstated the fair value by 21.6%.

The record lands in beta_sanctioned.json, which is what
scripts/check_study_provenance.py reads. study_numbers.json carries the same record under
`beta_record`, from the same call in the same session — one measurement, written twice
because two readers need it, never computed twice.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from beta_regression import own_stock_beta

rec = own_stock_beta('ADIB', 'EG', 'EGX')
out = {k: (list(v) if isinstance(v, tuple) else v) for k, v in rec.items()}
out['_'] = ('Own-stock first-tier weekly regression against the PUBLISHED INDEX OF THE '
            'EXCHANGE THIS STOCK IS LISTED ON, produced by '
            'beta_regression.own_stock_beta("ADIB","EG","EGX"). Never a study-local '
            'composite. The regressor file is index_file below and it is under '
            'raw_indices/, which is deliberately outside raw_ohlc/ so an index can never '
            'enter a calibration panel as a covered name.')
out['company'] = ('Abu Dhabi Islamic Bank – Egypt S.A.E., EGX: ADIB — the Cairo listing. '
                  'NOT ADIB Group PJSC (ADX: ADIB), which is the covered name ADIBUAE and '
                  'would regress against a different index on a different exchange.')
json.dump(out, open(os.path.join(HERE, 'beta_sanctioned.json'), 'w'), indent=1, default=str)
print('beta %.4f  R2 %.3f  n %d  se %.4f  index %s as at %s  conforming %s'
      % (rec['beta'], rec['r2'], rec['n'], rec['se'], rec['index_file'],
         rec['index_asof'], rec['conforming']))
