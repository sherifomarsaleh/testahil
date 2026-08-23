"""Negative control for [R-DOC-02]'s check_status_claims.

Restores the three status claims EXACTLY as they shipped and asserts each is caught.
A check that has never failed on the defect it was written for is not a check.
"""
import importlib.util
import sys

spec = importlib.util.spec_from_file_location(
    'cpt', '/home/user/testahil/scripts/check_protocol_text.py')
cpt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cpt)

DEFECTS = [
    # verbatim from Standing_Research_Protocol.md before today
    ('adaptive-width branch state',
     'As of this entry the change is committed and pushed to branch '
     'feat/adaptive-width-overlay-eg (open PR, not yet merged to main).'),
    # verbatim from the digest before today
    ('digest branch state',
     'Committed on a feature branch with an open PR - verify whether it is in production.'),
    # the shape the rule generalises to
    ('pending review',
     'The overlay is pending review and will be enabled once someone looks at it.'),
]

CLEAN = [
    ('quoted defect is a citation, not a claim',
     'The sentence that stood here still said "open PR, not yet merged to main", '
     'and it had been wrong for weeks.'),
    ('claim carrying its re-verification',
     'MERGED AND LIVE - re-verified against main 23-Aug-2026.'),
    ('a RULE about branches is not a status claim',
     'Engine and protocol changes go on a feature branch with an open PR, never a '
     'direct push to main.'),
    ('a rule using must',
     'Every engine change must sit on a feature branch before it is reviewed.'),
]

fails_seen = 0
for name, text in DEFECTS:
    f = []
    cpt.check_status_claims(text, 'test', f)
    ok = len(f) > 0
    fails_seen += ok
    print(f"  {'CAUGHT ' if ok else 'MISSED '} {name}")

clean_ok = 0
for name, text in CLEAN:
    f = []
    cpt.check_status_claims(text, 'test', f)
    ok = len(f) == 0
    clean_ok += ok
    print(f"  {'PASSED ' if ok else 'FALSE+ '} {name}")

print()
print(f'defects caught {fails_seen}/{len(DEFECTS)} | clean text passed {clean_ok}/{len(CLEAN)}')
sys.exit(0 if fails_seen == len(DEFECTS) and clean_ok == len(CLEAN) else 1)
