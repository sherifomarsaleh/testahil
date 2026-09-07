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

# ---- the SPLICE half: a passage repeated verbatim, which is what the union merge
# ---- of the single-line digest actually produced in the body the day after the
# ---- stamp defect. Every fixture is built from the real shapes, not invented.
LONG_A = ('[R-EXAMPLE-01] A RULE HEADER OF REALISTIC LENGTH, ADOPTED SOMEWHEN, per '
          'instruction, whose sentence runs on for a while because every rule in this '
          'document does, and which therefore comfortably exceeds the window this '
          'check uses to decide that a passage did not recur by accident at all, at '
          'something over four hundred characters rather than something just over the '
          'window, because a fixture sitting on a boundary tests the boundary and not '
          'the thing the boundary is for. ')
LONG_B = ('The neighbouring rule says something else entirely, at similar length, so '
          'that a fixture splicing one into the other reproduces the exact shape the '
          'merge produced rather than a shorter thing that only resembles it, which '
          'is what the first draft of this control did and proved nothing by. ')
# THREE DIFFERENT SENTENCES, NOT ONE REPEATED THREE TIMES. The first draft wrote
# this as a single sentence multiplied by three, which is itself a repeated passage
# — so the CLEAN fixtures carried the very defect they were built to prove absent,
# and the check flagged them. It was right to; the fixture was wrong.
FILLER = ('Ordinary prose fills the gap between the two so a repeat is not merely '
          'adjacent text. '
          'A second sentence of unrelated wording carries the fixture past the '
          'window without ever saying the same thing twice. '
          'A third runs on differently again, at enough length that nothing in this '
          'padding lands inside the window by accident. ')

SPLICE_RED = [
    # the shape of site A: a header duplicated with a neighbour's sentence between
    ('a rule header repeated with text between the copies',
     OPEN_D + BODY + LONG_A + LONG_B + LONG_A + BODY),
    # the shape of site B: a whole lesson inserted into a different rule, far away
    ('a passage spliced in far from its own home',
     OPEN_D + LONG_A + FILLER + BODY + FILLER + LONG_A + BODY),
    # immediately adjacent, the cheapest splice of all
    ('a passage duplicated back to back',
     OPEN_D + BODY + LONG_A + LONG_A + BODY),
]

SPLICE_CLEAN = [
    ('no repeat at all', OPEN_D + LONG_A + FILLER + LONG_B + BODY),
    # SHORTER than the window: house phrasing recurs and must not fire
    ('a short recurring house phrase',
     OPEN_D + 'READ THE POPULATION LIVE — never from this block. ' + LONG_A
     + 'READ THE POPULATION LIVE — never from this block. ' + LONG_B),
    # a named deliberate restatement must NOT fire even at full length
    ('a named deliberate restatement',
     OPEN_D + LONG_A + FILLER
     + 'that is the evidence to revisit this clause, and it is written down so the '
       'revisit does not depend on anyone remembering, which two rules in this '
       'document both say in these words on purpose because each records the '
       'evidence that would reopen it and neither points at the other. ' + FILLER
     + 'that is the evidence to revisit this clause, and it is written down so the '
       'revisit does not depend on anyone remembering, which two rules in this '
       'document both say in these words on purpose because each records the '
       'evidence that would reopen it and neither points at the other. '),
]

EXPECTED_SPLICE_RED, EXPECTED_SPLICE_CLEAN = 3, 3
assert len(SPLICE_RED) == EXPECTED_SPLICE_RED and len(SPLICE_CLEAN) == EXPECTED_SPLICE_CLEAN, (
    'SPLICE CASE COUNT CHANGED — update the declared constants deliberately.')

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


def _splice(text):
    fd, path = tempfile.mkstemp(suffix='.md')
    with os.fdopen(fd, 'w', encoding='utf-8') as fh:
        fh.write(text)
    try:
        return cps.duplicated_passages(path)
    finally:
        os.unlink(path)


s_caught = s_passed = 0
for name, text in SPLICE_RED:
    # ASSERT THE MUTATION LANDED: the fixture must actually repeat a passage
    # longer than the window, or a red result proves nothing about this check.
    # EVERY offset, never a sample. A sampled scan only compares windows whose
    # offsets share a remainder, so two copies at offsets differing by a
    # non-multiple of the step are never both seen — which is exactly how the
    # first measurement of this defect reported three splices where there were
    # five, and it is not a bug this file may repeat while asserting a landing.
    W = cps.DUP_WINDOW
    seen = set()
    landed = False
    for i in range(len(text) - W + 1):
        w = text[i:i + W]
        if w in seen:
            landed = True
            break
        seen.add(w)
    assert landed, ('MUTATION DID NOT LAND: ' + name
                    + f' — no {W}-character passage repeats in this fixture')
    hits = _splice(text)
    ok = bool(hits)
    s_caught += ok
    print(f"  {'CAUGHT ' if ok else 'MISSED '} {name}"
          + (f'  ({hits[0][2]} chars)' if hits else ''))
for name, text in SPLICE_CLEAN:
    hits = _splice(text)
    ok = not hits
    s_passed += ok
    print(f"  {'PASSED ' if ok else 'FALSE+ '} {name}"
          + ('' if ok else f'  (flagged {hits[0][2]} chars: {hits[0][3]!r})'))

print(f"{s_caught}/{EXPECTED_SPLICE_RED} splices caught, "
      f"{s_passed}/{EXPECTED_SPLICE_CLEAN} clean cases passed")

if (caught != EXPECTED_RED or passed != EXPECTED_CLEAN
        or s_caught != EXPECTED_SPLICE_RED or s_passed != EXPECTED_SPLICE_CLEAN):
    print('FAIL — the stamp or splice refusal does not do what [R-DOC-01] claims.')
    sys.exit(1)
print('OK — a document stating two revisions is refused, and so is one repeating '
      'a passage it was spliced with; one stamp and ordinary phrasing are not.')
