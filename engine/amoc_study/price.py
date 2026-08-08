"""Pricing harness for the critique register.

Step 3 of the critique procedure requires a currency-per-share price on EVERY finding
before any of them is judged. A finding that cannot be priced cannot be called
immaterial. This runs the FULL model — every lens, every weight — with one or more
registered inputs overridden, and reports the weighted central against the published
one, so each row in the register carries a number that came out of the same engine that
produced the published figure rather than out of a back-of-envelope.

    python3 price.py '{"g_term": 0.04}'
    python3 price.py '{"beta": 1.15, "erp": 0.07}' --label "critic beta and ERP"

Overrides are applied to INP *values* after the registry is built and before V is taken,
so every downstream derivation sees them. Anything the model derives rather than reads
(the audited effective tax rate, the base-year revenue) is not overridable here by
design: those are consequences, not inputs, and moving them is a model change, not a
sensitivity.
"""
import io
import json
import os
import re
import sys
import contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_CENTRAL = 5.954021840093423           # published weighted central, 08-Aug-2026

_SRC = open(os.path.join(HERE, 'compute.py')).read()
_ANCHOR = "V = {k: v['value'] for k, v in INP.items()}"
assert _SRC.count(_ANCHOR) >= 1, "compute.py no longer exposes the override point"

_PATCH = (
    "\nimport json as _pj, os as _po\n"
    "_ov = _pj.loads(_po.environ.get('AMOC_OVERRIDE', '{}'))\n"
    "for _k, _v in _ov.items():\n"
    "    assert _k in INP, 'override names an input that does not exist: ' + _k\n"
    "    INP[_k]['value'] = _v\n"
)
_i = _SRC.index(_ANCHOR)
_SRC = _SRC[:_i] + _PATCH + _SRC[_i:]

# the bridge sign gate requires a positive provision; an adversarial run that zeroes it
# is deliberate, so soften ONLY that gate inside the pricing sandbox
_SRC = _SRC.replace("and prov_val > 0", "and prov_val >= 0")

# never let a pricing run overwrite the published artefacts
_SRC = re.sub(r"with open\(os\.path\.join\(HERE, 'study_numbers\.json'\), 'w'\).*?indent=1\)",
              "pass", _SRC, flags=re.S)


def price(overrides):
    os.environ['AMOC_OVERRIDE'] = json.dumps(overrides)
    ns = {'__name__': '__amoc_priced__', '__file__': os.path.join(HERE, 'compute.py')}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(_SRC, 'compute.py', 'exec'), ns)
    return ns['central'], ns


if __name__ == '__main__':
    ov = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    label = sys.argv[sys.argv.index('--label') + 1] if '--label' in sys.argv else json.dumps(ov)
    c, ns = price(ov)
    d = c - BASE_CENTRAL
    print(f"{label}: central EGP {c:.4f} vs {BASE_CENTRAL:.4f} — "
          f"{d:+.4f} ({d / BASE_CENTRAL:+.2%}) — DCF lens EGP {ns['dcf_ps']:.4f}")
