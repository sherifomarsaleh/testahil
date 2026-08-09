"""EGCH — value per share against a FLAT cost of capital, as whole-model re-runs.

The study reports its answer against a built, glided cost of capital. A reader whose real
disagreement is with that rate needs to see the answer at other rates without re-deriving
the model, and needs to see it as a re-run rather than as an interpolation. Six rates, six
complete revaluations.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE); sys.path.insert(0, HERE)
import alternatives as A

RATES = (0.25, 0.20, 0.18, 0.16, 0.14, 0.12)
OUT = {f"{w:.4f}": A.reprice(wacc_path=[w] * 5, wacc_terminal=w) for w in RATES}
json.dump(OUT, open('flat_rate_ladder.json', 'w'), indent=1)
for k, v in OUT.items():
    print(f"  flat {float(k):.2%}  ->  EGP {v:6.2f}")
print("wrote flat_rate_ladder.json")
