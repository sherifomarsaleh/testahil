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
import shutil
import subprocess
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


# ---- THE AMENDMENT-DAY half [R-DOC-01 AMENDED 07-09-2026]. The witness is OUTSIDE
# ---- the document, so these run against a real little repository rather than a
# ---- string: the defect was two fields agreeing with each other and not with the
# ---- world, and no fixture made of text alone can reproduce that.

DAY_RED_EXPECTED, DAY_CLEAN_EXPECTED = 3, 3


def _repo(commit_at=None, dirty=False):
    """A repository whose governing documents were committed at a chosen instant."""
    tmp = tempfile.mkdtemp(prefix='sync-nc-')
    eng = os.path.join(tmp, 'engine')
    os.makedirs(eng)
    d = os.path.join(eng, 'PROJECT_INSTRUCTIONS_06-09-2026.md')
    f = os.path.join(eng, 'Standing_Research_Protocol.md')
    open(d, 'w').write(OPEN_D + BODY)
    open(f, 'w').write('PROTOCOL REVISION 2026-09-06d — ' + BODY)
    env = dict(os.environ)
    subprocess.run(['git', 'init', '-q'], cwd=tmp, check=True)
    subprocess.run(['git', 'config', 'user.email', 't@t'], cwd=tmp, check=True)
    subprocess.run(['git', 'config', 'user.name', 't'], cwd=tmp, check=True)
    subprocess.run(['git', 'add', '-A'], cwd=tmp, check=True)
    if commit_at:
        env['GIT_AUTHOR_DATE'] = env['GIT_COMMITTER_DATE'] = commit_at
    subprocess.run(['git', 'commit', '-qm', 'amend'], cwd=tmp, check=True, env=env)
    st = subprocess.run(['git', 'status', '--porcelain'], cwd=tmp,
                        capture_output=True, text=True).stdout
    assert st.strip() == '', 'fixture: the repository did not start clean'
    if dirty:
        open(d, 'a').write(' one more sentence, uncommitted.')
        st = subprocess.run(['git', 'status', '--porcelain'], cwd=tmp,
                            capture_output=True, text=True).stdout
        assert st.strip(), 'MUTATION DID NOT LAND: git does not see the edit'
    return tmp, d, f


def _days(tmp, d, f):
    return cps.amendment_days(root=tmp, paths=[d, f])


def day_cases():
    """(name, run) pairs; each returns (ok, detail)."""
    out = []

    def stamp_names_another_day():
        """THE DEFECT AS IT HAPPENED: committed on the 7th, stamped the 6th."""
        tmp, d, f = _repo(commit_at='2026-09-07T01:25:08+00:00')
        try:
            days, _ = _days(tmp, d, f)
            assert '2026-09-07' in days, 'MUTATION DID NOT LAND: %r' % days
            return ('2026-09-06' not in days,
                    'stamped 2026-09-06f, amended on %s' % ' or '.join(days))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def not_a_repository():
        """An unanswerable check is not a clean one [R-ENF-04]."""
        tmp, d, f = _repo(commit_at='2026-09-07T01:25:08+00:00')
        try:
            shutil.rmtree(os.path.join(tmp, '.git'))
            assert not os.path.exists(os.path.join(tmp, '.git')), 'MUTATION DID NOT LAND'
            try:
                _days(tmp, d, f)
                return (False, 'it answered anyway')
            except RuntimeError as exc:
                return (True, str(exc)[:60])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def no_commit_touching_them():
        """A shallow clone, where the honest answer is a refusal."""
        tmp = tempfile.mkdtemp(prefix='sync-nc-')
        try:
            subprocess.run(['git', 'init', '-q'], cwd=tmp, check=True)
            subprocess.run(['git', 'config', 'user.email', 't@t'], cwd=tmp, check=True)
            subprocess.run(['git', 'config', 'user.name', 't'], cwd=tmp, check=True)
            open(os.path.join(tmp, 'README'), 'w').write('x')
            subprocess.run(['git', 'add', '-A'], cwd=tmp, check=True)
            subprocess.run(['git', 'commit', '-qm', 'root'], cwd=tmp, check=True)
            miss = os.path.join(tmp, 'engine', 'nothing.md')
            assert not os.path.exists(miss), 'MUTATION DID NOT LAND'
            try:
                _days(tmp, [miss], )
                return (False, 'it answered anyway')
            except TypeError:
                pass
            try:
                cps.amendment_days(root=tmp, paths=[miss])
                return (False, 'it answered anyway')
            except RuntimeError as exc:
                return (True, str(exc)[:60])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def matches_utc():
        tmp, d, f = _repo(commit_at='2026-09-07T01:25:08+00:00')
        try:
            days, _ = _days(tmp, d, f)
            return ('2026-09-07' in days, ' or '.join(days))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def matches_cairo_across_midnight():
        """22:30 UTC is the NEXT day in Cairo. BOTH readings must be accepted.

        Choosing one zone here would be a free parameter, and this is the band where
        the two disagree — the only place the choice would ever show.
        """
        tmp, d, f = _repo(commit_at='2026-09-06T22:30:00+00:00')
        try:
            days, _ = _days(tmp, d, f)
            return (days == ['2026-09-06', '2026-09-07'], ' or '.join(days))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def amended_in_the_working_tree():
        """An amendment happening NOW is dated now, not by the last commit."""
        tmp, d, f = _repo(commit_at='2020-01-01T00:00:00+00:00', dirty=True)
        try:
            days, when = _days(tmp, d, f)
            return ('2020-01-01' not in days and 'working tree' in when,
                    '%s (%s)' % (' or '.join(days), when))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    out.append(('a stamp naming a day the documents were not amended on',
                stamp_names_another_day))
    out.append(('not a git repository', not_a_repository))
    out.append(('no commit touching the documents', no_commit_touching_them))
    out.append(('a stamp matching the commit day in UTC', matches_utc))
    out.append(('a commit at 22:30 UTC — both zone readings accepted',
                matches_cairo_across_midnight))
    out.append(('amended in the working tree', amended_in_the_working_tree))
    return out


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

d_cases = day_cases()
assert len(d_cases) == DAY_RED_EXPECTED + DAY_CLEAN_EXPECTED, (
    'AMENDMENT-DAY CASE COUNT CHANGED — update the declared constants deliberately.')
d_red = d_clean = 0
for i, (name, run) in enumerate(d_cases):
    ok, detail = run()
    is_red_case = i < DAY_RED_EXPECTED
    if is_red_case:
        d_red += ok
        print(f"  {'CAUGHT ' if ok else 'MISSED '} {name}  ({detail})")
    else:
        d_clean += ok
        print(f"  {'PASSED ' if ok else 'FALSE+ '} {name}  ({detail})")
print(f'{d_red}/{DAY_RED_EXPECTED} amendment-day defects caught, '
      f'{d_clean}/{DAY_CLEAN_EXPECTED} clean cases passed')

if (caught != EXPECTED_RED or passed != EXPECTED_CLEAN
        or s_caught != EXPECTED_SPLICE_RED or s_passed != EXPECTED_SPLICE_CLEAN
        or d_red != DAY_RED_EXPECTED or d_clean != DAY_CLEAN_EXPECTED):
    print('FAIL — the stamp, splice or amendment-day refusal does not do what '
          '[R-DOC-01] claims.')
    sys.exit(1)
print('OK — a document stating two revisions is refused, so is one repeating a '
      'passage it was spliced with, and so is a stamp naming a day the documents '
      'were not amended on; one stamp, ordinary phrasing and both zone readings '
      'are not.')
