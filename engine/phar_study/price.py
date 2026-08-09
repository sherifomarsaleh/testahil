"""Price a finding: re-run the whole model with one or more inputs replaced."""
import json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = json.load(open(os.path.join(HERE, 'study_numbers.json')))
B_C, B_A, B_B = (BASE['lenses']['fair_base'], BASE['dcf']['frame_A']['per_share'],
                 BASE['dcf']['frame_B']['per_share'])


def run(over):
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    env = dict(os.environ, PHAR_OVERRIDE=json.dumps(over), PHAR_QUIET='1', PHAR_OUT=path)
    r = subprocess.run([sys.executable, os.path.join(HERE, 'compute.py')], env=env,
                       capture_output=True, text=True)
    if r.returncode:
        os.unlink(path)
        return None, r.stderr.strip().split('\n')[-1]
    d = json.load(open(path)); os.unlink(path)
    return d, None


CASES = [
    ('SA-1  provision at the stated three-year average 6.516%',
     {'prov_pct_permanent': 0.0651609}),
    ('SA-3  terminal ROIC at the model FY2030 ROIC 16.36%', {'roic_term': 0.1636}),
    ('SA-4  FCFF taxed at the effective 23.5%', {'tax_stat': 0.235}),
    ('SA-10 peer leg at the true midpoint of the two observations, 21.35x',
     {'peer_pe_regional': 21.35}),
    ('C-11  risk-free at the 6-Aug observable 23.00%', {'rf': 0.2300}),
    ('C-15  interest charged at the marginal blended rate on flat debt',
     {'int_path': [0.18548 * 8797.7256] * 5}),
    ('C-19  terminal real rate at Egypt real GDP growth (rf_term 9.5%)', {'rf_term': 0.095}),
    ('C-22  associates at the Q1 run-rate, 52.5m', {'assoc_norm': 52.5}),
    ('X     associates dropped to zero (bound test)', {'assoc_norm': 0.0}),
]
print(f"{'finding':62s} {'centre':>9s} {'d/share':>9s} {'% centre':>9s} {'Frame A':>9s}")
print(f"{'BASELINE':62s} {B_C:9.2f} {'—':>9s} {'—':>9s} {B_A:9.2f}")
out = []
for label, over in CASES:
    d, err = run(over)
    if err:
        print(f'{label:62s}   FAILED: {err[:60]}'); continue
    c, a = d['lenses']['fair_base'], d['dcf']['frame_A']['per_share']
    print(f'{label:62s} {c:9.2f} {c - B_C:+9.2f} {(c / B_C - 1) * 100:+8.1f}% {a:9.2f}')
    out.append(dict(label=label, over=over, centre=c, d=c - B_C, pct=c / B_C - 1, frame_a=a))
json.dump(out, open(os.path.join(HERE, 'audit_pricing.json'), 'w'), indent=1)
