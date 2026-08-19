#!/usr/bin/env python3
"""RIYADHCABLE beta — the sanctioned route, reproducibly.

Runs engine/beta_regression.own_stock_beta against the exchange's published index
(TASI, engine/raw_indices/SA/TASI.csv) and asserts provenance with
research_protocol.assert_beta_provenance. Added at the critique response: the first
edition produced the identical record ad hoc without a committed runner.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
ROOT = os.path.dirname(ENGINE)
sys.path.insert(0, ROOT)
sys.path.insert(0, ENGINE)

from engine.beta_regression import own_stock_beta          # noqa: E402
from engine.research_protocol import assert_beta_provenance  # noqa: E402

rec = own_stock_beta('RIYADHCABLE', 'SA', 'TADAWUL')
rec_ols = own_stock_beta('RIYADHCABLE', 'SA', 'TADAWUL', dimson=False)
rec['ols_crosscheck'] = rec_ols['beta']
assert_beta_provenance(rec)
assert rec['conforming'] and rec['usable'], rec['gate_msg']

with open(os.path.join(HERE, 'beta_result.json'), 'w') as f:
    json.dump(rec, f, indent=1, default=float)

print(f"BETA OK — {rec['ticker']} {rec['beta']:.4f} (R2 {rec['r2']:.3f}, SE {rec['se']:.3f}, "
      f"n {rec['n']}, CI90 [{rec['ci90'][0]:.2f}, {rec['ci90'][1]:.2f}]) vs {rec['index_file']} "
      f"as of {rec['index_asof']}; Dimson={rec['dimson']}, Blume {rec['blume_crosscheck']:.3f}")
