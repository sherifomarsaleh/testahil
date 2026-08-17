"""AMR — beta record, produced by the SANCTIONED resolver and nothing else.

This file used to be a study-local regression script. That is exactly what the
standing rule forbids: "NEVER hand-roll a study-local beta script — every study in
this repo once did and every one regressed on a composite." Its own history proves
the point. Its first version regressed the company's SAUDI line against the Tadawul
index (0.894) because no Abu Dhabi index could be reached; its second regressed the
Abu Dhabi line against a constructed composite of covered UAE names (0.586) and
against a US-listed UAE index fund (0.469) — a composite and a differently-timed
proxy, both non-conforming, and both wrong by roughly half.

There is now one path: engine/beta_regression.own_stock_beta(), which resolves the
regressor through wacc_builder.market_index_path(market, exchange), reads the
published index out of engine/raw_indices/, screens both series through the
data-quality gate, applies the Dimson lead-lag correction, and returns a record
carrying its own provenance. engine/research_protocol.assert_beta_provenance()
then refuses any record that did not come from a published index under
raw_indices/ — which a hand-rolled composite never can.

The exchange comes from the code prefix in assets/data.js (ADX:AMR), not from the
raw_ohlc/AE/ folder, which groups by MARKET and holds both ADX and DFM names.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))

from beta_regression import own_stock_beta                 # noqa: E402
from research_protocol import assert_beta_provenance       # noqa: E402

REC = own_stock_beta('AMR', market='AE', exchange='ADX')
assert_beta_provenance(REC)                                 # hard gate, not a warning

with open(os.path.join(HERE, 'beta_result.json'), 'w') as fh:
    json.dump(REC, fh, indent=1, default=str)

print(f"beta {REC['beta']:.4f}  SE {REC['se']:.4f}  R2 {REC['r2']:.4f}  n={REC['n']}  "
      f"window {REC['first_obs']}..{REC['last_obs']} ({REC['window_years']}y)")
print(f"regressor {REC['index_file']} as of {REC['index_asof']}  "
      f"exchange {REC['exchange']}  conforming={REC['conforming']}  "
      f"dimson={REC['dimson']}  weak={REC['weak']}")
print(f"CI90 [{REC['ci90'][0]:.3f}, {REC['ci90'][1]:.3f}]  "
      f"Blume cross-check {REC['blume_crosscheck']:.3f}")
if REC.get('interim_note'):
    print('INTERIM REGRESSOR:', REC['interim_note'])
