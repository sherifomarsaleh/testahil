"""SAVOLA beta — tier-1 own-stock weekly regression against the published index
of the exchange the stock is listed on (Tadawul -> TASI), produced by THE ONLY
sanctioned route, engine/beta_regression.own_stock_beta(), and attested by
research_protocol.assert_beta_provenance(). Never a study-local script, never a
constituent composite (see the FERTIGLB precedent: composite understated beta
~40% and overstated fair value 21.6%)."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from beta_regression import own_stock_beta
from research_protocol import assert_beta_provenance

rec = own_stock_beta('SAVOLA', 'SA', 'TADAWUL')
assert_beta_provenance(rec)
with open(os.path.join(HERE, 'beta_result.json'), 'w') as f:
    json.dump(rec, f, indent=1, default=str)
print(f"beta {rec['beta']:.3f} | R2 {rec['r2']:.3f} | n {rec['n']} | SE {rec['se']:.3f} | "
      f"CI90 [{rec['ci90'][0]:.2f},{rec['ci90'][1]:.2f}] | usable={rec['usable']} "
      f"({rec['gate_msg']}) | weak={rec['weak']}")
print(f"window {rec['first_obs']}..{rec['last_obs']} ({rec['window_years']}y) | "
      f"index {rec['index_file']} asof {rec['index_asof']} | conforming={rec['conforming']}")
print(f"Blume cross-check: {rec['blume_crosscheck']:.3f}")
print("stock DQ:", rec['stock_dq'])
print("index DQ:", rec['index_dq'])
