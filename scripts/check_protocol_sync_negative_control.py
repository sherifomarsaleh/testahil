"""Negative control for check_protocol_sync's SECOND-STAMP refusal.  [R-DOC-01]

Reinjects the defect EXACTLY as it shipped on 07-09-2026 — a union merge of the
single-line digest that kept both sides' opening sentences, so the file carried
two DIGEST REVISION stamps and every check in the repository read the first one
and passed.

EVERY MUTATION ASSERTS THAT IT LANDED before the gate is run. Three negative
controls in this repository have been caught passing a fixture that never
injected its condition, so a case that cannot prove it changed the file is not
evidence of anything, and the case COUNT is asserted against a declared constant
so a later edit cannot delete a case and leave the file reporting clean.

The clean half is the half that matters: a stamp is a real sentence in a real
document, and a gate that fires on the ORDINARY shape would be the permanently
red check [R-ENF-02] forbids.
"""
import importlib.util
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, 'check_protocol_sync.py')

spec = importlib.util.spec_from_file_location('cps', TARGET)
cps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cps)

OPEN_D = ('DIGEST REVISION 2026-09-06d — [R-DOC-01] every copy of this block '
          'carries this line as its FIRST characters. ')
OPEN_C = ('DIGEST REVISION 2026-09-06c — [R-DOC-01] every copy of this block '
          'carries this line as its FIRST characters. ')
BODY = ('If the copy you are holding does not, it is STALE. TESTAHIL — Standing '
        'Research Protocol (condensed). THIS BLOCK CONTAINS RULES, NOT NUMBERS.')

RED = [
    # exactly as it shipped: the union merge kept both opening sentences
    ('the 07-09 merge artefact, both stamps on one line',
     OPEN_D + OPEN_C + BODY),
    # the same defect with the stale stamp far down the document
    ('a superseded stamp buried mid-document',
     OPEN_D + BODY + ' ... ' + OPEN_C + ' ... ' + BODY),
    # the other document's prefix is no more allowed than its own
    ('a PROTOCOL stamp inside the digest',
     OPEN_D + BODY + ' PROTOCOL REVISION 2026-09-05a — see the full account.'),
    # three stamps: the count must not be what makes it pass
    ('three stamps',
     OPEN_D + OPEN_C + BODY + ' DIGEST REVISION 2026-09-05a — older still.'),
]

CLEAN = [
    ('one stamp, single-line document', OPEN_D + BODY),
    ('one stamp, multi-line document', OPEN_D + '\n\n' + BODY + '\n' + BODY),
    # the rule ABOUT stamps is prose, not a stamp — it names no date
    ('prose describing the rule',
     OPEN_D + BODY + ' Bump the DIGEST REVISION on every edit, however small.'),
    # a rev. number in the full protocol's own history is a different shape
    ('the full protocol edition history',
     OPEN_D + BODY + ' (rev. 10, 1 September 2026 — CAMPAIGN WORK IS MERGED ON GREEN)'),
    # a DATE beside the word revision, with no stamp prefix
    ('a dated amendment note',
     OPEN_D + BODY + ' [R-MACRO-01 AMENDED 06-09-2026] A PATH\'S ANCHOR CARRIES A DATE.'),
]

EXPECTED_RED, EXPECTED_CLEAN = 4, 5
assert len(RED) == EXPECTED_RED and len(CLEAN) == EXPECTED_CLEAN, (
    'CASE COUNT CHANGED — a case was added or deleted. Update the declared '
    'constants deliberately; a control that silently shrinks reports clean.')


def _run(text):
    fd, path = tempfile.mkstemp(suffix='.md')
    with os.fdopen(fd, 'w', encoding='utf-8') as fh:
        fh.write(text)
    try:
        return cps.extra_stamps(path), cps.revision(path)
    finally:
        os.unlink(path)


caught = 0
for name, text in RED:
    # ASSERT THE MUTATION LANDED: the fixture must actually carry a second stamp,
    # or a green result proves only that nothing was injected.
    assert len(cps.REV_ANY.findall(text)) > 1, 'MUTATION DID NOT LAND: ' + name
    extra, first = _run(text)
    ok = bool(extra)
    caught += ok
    print(f"  {'CAUGHT ' if ok else 'MISSED '} {name}"
          + (f"  (second stamp {extra[0][0]})" if extra else ''))

passed = 0
for name, text in CLEAN:
    assert len(cps.REV_ANY.findall(text)) == 1, 'CLEAN FIXTURE IS NOT CLEAN: ' + name
    extra, first = _run(text)
    ok = not extra and first is not None
    passed += ok
    print(f"  {'PASSED ' if ok else 'FALSE+ '} {name}")

print(f"\n{caught}/{EXPECTED_RED} defects caught, {passed}/{EXPECTED_CLEAN} clean cases passed")
if caught != EXPECTED_RED or passed != EXPECTED_CLEAN:
    print('FAIL — the second-stamp refusal does not do what [R-DOC-01] claims.')
    sys.exit(1)
print('OK — a document stating two revisions is refused; one stamp is not.')
