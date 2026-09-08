"""Negative control for [R-DOC-02]'s check_status_claims.

Restores the three status claims EXACTLY as they shipped and asserts each is caught.
A check that has never failed on the defect it was written for is not a check.
"""
import importlib.util
import os
import sys

# Resolved from THIS file, never hardcoded. The first version carried the absolute path it
# was drafted at (/home/user/...), passed locally, and died on the CI runner where that path
# does not exist — the check meant to stop a stale claim about the repo shipped with one.
HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, 'check_protocol_text.py')

spec = importlib.util.spec_from_file_location('cpt', TARGET)
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

# ---- [R-DOC-02 EXTENDED 07-09-2026] the BARE-FILENAME half -------------------------
# The defect exactly as it shipped, plus the cases that decide whether the check is
# honest rather than merely strict. EVERY FIXTURE ASSERTS ITS OWN CONDITION FIRST: a
# case that cannot prove the name it names is absent (or present) from the tree is
# evidence about nothing.
_HAVE = cpt._repo_basenames()
assert 'mc_v3.py' in _HAVE, 'fixture: the tree index did not find a file that exists'
assert 'mc_v2.py' not in _HAVE, 'fixture: mc_v2.py is present, so its case proves nothing'

BARE_RED = [
    # verbatim from the digest before 07-09-2026
    ('the retired engine module named as available',
     'mc_v2.py is legacy reference only, never the production default.'),
    # the same shape on a file that never existed
    ('a module invented in prose',
     'The schedule is built by cost_of_capital_v9.py and nothing else.'),
    # a document, not a module — the class is files, not python
    ('a delivered document that is not there',
     'The worked precedent is Nonexistent_Study_01-01-2020.docx in that directory.'),
]

BARE_CLEAN = [
    # a real file with no directory prefix must NOT fire
    ('a bare filename that resolves',
     'The production engine is mc_v3.py and the profiles beside it.'),
    # a prefixed path is check_paths' subject and must not be double-counted here
    ('a prefixed path is not this check\'s subject',
     'Read engine/market_profiles.py live before quoting any fit.'),
    # DECLARED ABSENT, with its reason held in the gate
    ('a cache the documents say is never committed',
     'the harvest cache (claims_short.pkl) is a regenerable convenience, never committed'),
    # a braced template names a shape, not a file
    ('a template name',
     'a PENDING_REVIEW/{MARKET}_{date}-ERROR.md carries the traceback'),
]

bare_caught = 0
for name, text in BARE_RED:
    f = []
    cpt.check_bare_filenames(text, 'test', f, _HAVE)
    ok = len(f) > 0
    bare_caught += ok
    print(f"  {'CAUGHT ' if ok else 'MISSED '} {name}")

bare_clean_ok = 0
for name, text in BARE_CLEAN:
    f = []
    cpt.check_bare_filenames(text, 'test', f, _HAVE)
    ok = len(f) == 0
    bare_clean_ok += ok
    print(f"  {'PASSED ' if ok else 'FALSE+ '} {name}")
print()

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
print(f'bare-filename defects caught {bare_caught}/{len(BARE_RED)} | '
      f'clean passed {bare_clean_ok}/{len(BARE_CLEAN)}')
sys.exit(0 if (fails_seen == len(DEFECTS) and clean_ok == len(CLEAN)
               and bare_caught == len(BARE_RED)
               and bare_clean_ok == len(BARE_CLEAN)) else 1)
