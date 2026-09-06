"""WHICH SCRIPTS WRITE A STUDY'S NUMBERS FILE, AND IN WHAT ORDER.

Adding one line to SWDY's lens record and rebuilding it produced an EIGHTEEN-LINE
diff, and the sixteen deleted lines were that study's entire [R-ANCHOR-01]
forecast_anchor record. `study_numbers.json` there is written WHOLE by compute.py
and that block is appended AFTERWARDS by a second script; nothing in either file,
or anywhere else, said so.

It was caught by reading a diffstat. No gate could have caught it: a gate reads the
file that is there and cannot know what a rebuild removed.

THREE STUDIES ARE IN THAT STATE and one of them is severe:

    SWDY    compute.py + forecast_anchor.py   -> forecast_anchor
    SAVOLA  compute.py + forecast_anchor.py   -> forecast_anchor
    EGCH    compute.py + lenses.py            -> central, central_two_sided, spot,
                                                fair, lens_record, bridge_record,
                                                macro_record, forecast_anchor

A rebuild running only EGCH's compute.py removes THE STUDY'S OWN CENTRAL AND SPOT —
the two fields the valuation-gap gate reads — plus three standing-rule records. Every
gate downstream would then report on a file that had quietly lost them, and would
report it as an UNREADABLE STUDY rather than as a rebuild that deleted the answer.

THE INSTRUMENT ALREADY EXISTED IN THREE STUDIES OF TWENTY-FOUR — borouge, du and
empower each read the numbers file, import the model, and restore-and-refuse if the
bytes moved — and it bound nowhere else, which is the prose-figures finding verbatim:
a rule that one study implements is a rule that one study obeys. `guard()` below is
that instrument, shared, so a study calls it in one line instead of copying it.

DETECTION IS PARSED, NOT GREPPED, AND IT HAD TO BE RE-POINTED TWICE. Both directions
are recorded because both were wrong in an instructive way:

  * It UNDER-detected. A first pass resolved only `X = <literal mentioning
    study_numbers>` and reported DU as having NO writer at all — DU builds the
    filename through a ternary and then a join, two hops. An absent answer wearing
    the costume of a clean one [R-ENF-04].
  * It then OVER-detected. Following the chain to a fixpoint tainted
    `doc = json.load(open(NUMBERS))` and everything built from it, so EMPOWER and
    FERTIGLOBE were flagged — both of which write diagnostics.json. A path is not
    what a file said.
  * And one of those false positives WAS EMPOWER'S OWN GUARD: the second draft was
    pointing at the one study that had already solved the problem.
"""

import ast
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')

# A call whose result is FILE CONTENT rather than a PATH. Taint must not follow
# these or every write in the file matches -- see the over-detection note above.
_READERS = {'load', 'loads', 'read', 'readlines'}


def _is_content(value):
    for n in ast.walk(value):
        if isinstance(n, ast.Call):
            f = n.func
            nm = (f.attr if isinstance(f, ast.Attribute)
                  else f.id if isinstance(f, ast.Name) else '')
            if nm in _READERS or nm == 'open':
                return True
    return False


def writes_numbers(path):
    """True if this script opens study_numbers.json in a write mode."""
    try:
        tree = ast.parse(open(path, encoding='utf-8').read())
    except Exception:
        return False
    tainted = set()
    for _ in range(6):                       # fixpoint, cheaply bounded
        before = set(tainted)
        for n in ast.walk(tree):
            if (isinstance(n, ast.Assign) and len(n.targets) == 1
                    and isinstance(n.targets[0], ast.Name)):
                if _is_content(n.value):
                    continue
                src = ast.dump(n.value)
                names = {x.id for x in ast.walk(n.value) if isinstance(x, ast.Name)}
                if 'study_numbers' in src or (names & tainted):
                    tainted.add(n.targets[0].id)
        if tainted == before:
            break
    for n in ast.walk(tree):
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id == 'open' and n.args):
            mode = ''
            if len(n.args) > 1 and isinstance(n.args[1], ast.Constant):
                mode = str(n.args[1].value)
            for kw in n.keywords:
                if kw.arg == 'mode' and isinstance(kw.value, ast.Constant):
                    mode = str(kw.value.value)
            tgt = ast.dump(n.args[0])
            names = {x.id for x in ast.walk(n.args[0]) if isinstance(x, ast.Name)}
            if ('study_numbers' in tgt or (names & tainted)) and 'w' in mode:
                return True
    return False


def writers(study_dir):
    """The scripts in one study directory that write its numbers file."""
    return [os.path.basename(f) for f in sorted(glob.glob(os.path.join(study_dir, '*.py')))
            if not f.endswith('_backup.py') and writes_numbers(f)]


def census():
    """ticker -> [writers], for every study directory on disk."""
    out = {}
    for d in sorted(glob.glob(os.path.join(ENGINE, '*_study'))):
        if not os.path.isdir(d):
            continue
        out[os.path.basename(d)[:-len('_study')].upper()] = writers(d)
    if not out:
        raise SystemExit('FATAL: no study directories. An empty result is not a clean '
                         'result [R-ENF-04].')
    return out


def guard(numbers_path, before=None):
    """Restore-and-refuse: the instrument borouge, du and empower already carried.

    Call it with the bytes read BEFORE importing the model. If importing moved the
    committed numbers file, the original is restored and the process refuses — a
    diagnostic may not move the valuation it is measuring, and a rebuild may not
    silently drop what another generator appended.
    """
    if before is None:
        return open(numbers_path, 'rb').read()
    if open(numbers_path, 'rb').read() != before:
        open(numbers_path, 'wb').write(before)
        raise SystemExit(
            'REFUSED: running this moved %s. The original bytes are restored.\n'
            'If that file is written by more than one generator, running one of them '
            'alone DELETES what the others appended, and no gate can see it: a gate '
            'reads the file that is there and cannot know what a rebuild removed.'
            % os.path.basename(numbers_path))
    return before


def restorers(study_dir):
    """Writers whose write is a RESTORE rather than an append.

    EMPOWER and FERTIGLOBE were called false positives twice and they are not:
    `open(NUMBERS, "wb").write(_BEFORE)` really does write the numbers file. What
    it writes is the ORIGINAL BYTES, to put back what importing the model moved —
    the guard, not a generator. The detector was right and the classification was
    wrong, which is worth recording because the same mistake would have been made
    again by the next person reading its output.

    Detection is mechanical; CLASSIFICATION IS DECLARED. A script that calls
    guard() has said what its write is. A script that writes and neither calls
    guard() nor appears in the study's declared generator order is the violation.
    THE TEST IS STRUCTURAL, NOT A MESSAGE MATCH. A first draft looked for
    guard()'s own wording and missed FERTIGLOBE, which carries the identical
    construction with an assert instead of a raise — the forbidden-word-list
    mistake in miniature: a list of phrases cannot be complete, and the shape can.
    A restore is a write whose VALUE was read from the same file earlier in the
    same script; nothing else has that shape and no generator can acquire it by
    accident.
    """
    out = []
    for f in sorted(glob.glob(os.path.join(study_dir, '*.py'))):
        if f.endswith('_backup.py') or not writes_numbers(f):
            continue
        src = open(f, encoding='utf-8').read()
        if 'numbers_generators.guard' in src:
            out.append(os.path.basename(f))
            continue
        try:
            tree = ast.parse(src)
        except Exception:
            continue
        # names holding bytes READ from the numbers file
        held = set()
        for n in ast.walk(tree):
            if (isinstance(n, ast.Assign) and len(n.targets) == 1
                    and isinstance(n.targets[0], ast.Name)):
                d = ast.dump(n.value)
                if 'study_numbers' in d or ('read' in d and 'NUM' in d):
                    if "'rb'" in d or '"rb"' in d or 'read' in d:
                        held.add(n.targets[0].id)
        # a write whose argument is one of those names is a RESTORE
        for n in ast.walk(tree):
            if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                    and n.func.attr == 'write' and n.args):
                arg = n.args[0]
                if isinstance(arg, ast.Name) and arg.id in held:
                    out.append(os.path.basename(f))
                    break
    return out


if __name__ == '__main__':
    c = census()
    multi = {k: v for k, v in c.items() if len(v) > 1}
    print('study directories: %d   with a writer found: %d'
          % (len(c), sum(1 for v in c.values() if v)))
    missing = sorted(k for k, v in c.items() if not v)
    if missing:
        print('NO WRITER FOUND for %s — the detector under-detects and an absent '
              'answer is not a clean one [R-ENF-04]' % ', '.join(missing))
    print('\nWRITTEN BY MORE THAN ONE SCRIPT — a rebuild running only one drops what')
    print('the others appended, and nothing in the file says so unless it declares it:')
    for k, v in sorted(multi.items()):
        d = os.path.join(ENGINE, '%s_study' % k.lower())
        r = set(restorers(d))
        gen = [x for x in v if x not in r]
        print('   %-12s generators: %-42s restore-guard: %s'
              % (k, ', '.join(gen), ', '.join(sorted(r)) or '-'))
    print('\nA study with more than one GENERATOR must declare their order; a writer')
    print('that is a restore-guard is not a generator and says so by calling guard().')
