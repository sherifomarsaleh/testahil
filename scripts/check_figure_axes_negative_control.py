#!/usr/bin/env python3
"""The figure-axis gate must fire on every shape it claims to catch, and on nothing else.

The two failing cases are the constructions that shipped. The clean cases include the two
the detector got wrong twice before it got them right: a VERTICAL bar chart, whose x is a
category index and not a value, and a football-field SPAN bar drawn with left=, whose
container datavalue is a width and not a coordinate. Each of those fired on a majority of
the book's figure scripts in an earlier draft.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join('scripts', 'check_figure_axes.py')

HEAD = """import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import figure_guard
HERE = os.path.dirname(os.path.abspath(__file__))
"""

CASES = [
    ("AMOC's figure 4 as it shipped — seven bars clipped to the same length and the "
     "price line thrown away",
     HEAD + """
fig, ax = plt.subplots()
ax.barh([0, 1, 2], [11.40, 12.17, 12.74])
ax.axvline(13.50, color='r', ls='--')
ax.set_xlim(0, 10.4)
fig.savefig(os.path.join(HERE, 'f.png'))
""", True, 'reference line'),
    ("AMOC's figure 1 as it shipped — a hardcoded 2 to 11 against a spot of 13.50",
     HEAD + """
fig, ax = plt.subplots()
ax.barh([0, 1], [4.0, 6.0], left=[2.0, 3.0])
ax.axvline(13.50, color='r', ls='--')
ax.set_xlim(2, 11)
fig.savefig(os.path.join(HERE, 'f.png'))
""", True, 'reference line'),
    ("a bar clipped at the axis edge, with no reference line at all",
     HEAD + """
fig, ax = plt.subplots()
ax.bar([0, 1], [3.0, 9.9])
ax.set_ylim(0, 5)
fig.savefig(os.path.join(HERE, 'f.png'))
""", True, 'a bar'),
    # ---- and the ones that must NOT fire ---------------------------------------------
    ("CLEAN — limits derived from what is drawn, price line included",
     HEAD + """
fig, ax = plt.subplots()
ax.barh([0, 1, 2], [11.40, 12.17, 12.74])
ax.axvline(13.50, color='r', ls='--')
ax.set_xlim(0, 13.50 * 1.1)
fig.savefig(os.path.join(HERE, 'f.png'))
""", False, None),
    ("CLEAN — a VERTICAL bar chart, whose x is a category index and not a value; an "
     "earlier detector read it as a coordinate and fired on ten scripts of twenty-six",
     HEAD + """
fig, ax = plt.subplots()
ax.bar([0, 1, 2], [3.0, 4.0, 5.0])
ax.set_xlim(-0.6, 2.6)
ax.set_ylim(0, 6)
fig.savefig(os.path.join(HERE, 'f.png'))
""", False, None),
    ("CLEAN — a football-field SPAN bar drawn with left=, whose container datavalue is a "
     "WIDTH and not a coordinate; the second detector read it as one and fired on sixteen",
     HEAD + """
fig, ax = plt.subplots()
ax.barh([0, 1], [66.0, 20.0], left=[22.2, 30.0])
ax.set_xlim(20, 90)
fig.savefig(os.path.join(HERE, 'f.png'))
""", False, None),
    ("CLEAN — a deliberate crop, DECLARED with its reason",
     HEAD + """
fig, ax = plt.subplots()
ax.bar([0, 1], [3.0, 9.9])
ax.set_ylim(0, 5)
figure_guard.allow(ax, 'the tail is cropped on purpose to keep the body legible')
fig.savefig(os.path.join(HERE, 'f.png'))
""", False, None),
]


def build(tmp, ratchet=None, unrunnable=None):
    os.makedirs(os.path.join(tmp, 'scripts'), exist_ok=True)
    os.makedirs(os.path.join(tmp, 'engine', 'build_depth_audit'), exist_ok=True)
    shutil.copy(os.path.join(ROOT, GATE), os.path.join(tmp, GATE))
    shutil.copy(os.path.join(ROOT, 'engine', 'figure_guard.py'),
                os.path.join(tmp, 'engine', 'figure_guard.py'))
    json.dump({'outstanding': ratchet or {}, 'unrunnable': unrunnable or []},
              open(os.path.join(tmp, 'engine', 'build_depth_audit',
                                'figaxes_outstanding.json'), 'w'), indent=1)


def plant(tmp, src, study='zzz', name='figures.py'):
    d = os.path.join(tmp, 'engine', '%s_study' % study)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, name), 'w').write(src)


def run(tmp):
    r = subprocess.run([sys.executable, GATE], cwd=tmp, capture_output=True, text=True,
                       timeout=600)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


def main():
    bad = 0
    for name, src, must_fail, expect in CASES:
        tmp = tempfile.mkdtemp(prefix='ncfa')
        try:
            build(tmp)
            plant(tmp, src)
            rc, out = run(tmp)
            ok = ((rc != 0) == must_fail) and (expect is None or expect in out)
            print('%-4s %s' % ('PASS' if ok else 'FAIL', name[:98]))
            if not ok:
                bad += 1
                print('      rc=%d wanted %s' % (rc, 'RED' if must_fail else 'GREEN'))
                print('      ' + '\n      '.join(out.strip().splitlines()[-4:]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # A SCRIPT THAT WILL NOT RUN IS NOT A CLEAN SCRIPT. Its figures are unchecked, which
    # is the state this gate exists to stop passing quietly.
    tmp = tempfile.mkdtemp(prefix='ncfau')
    try:
        build(tmp)
        # THE FIXTURE MUST BE IN THE POPULATION BEFORE IT CAN TEST THE GATE. A first
        # version raised before any savefig call, so the script was not a figure script
        # at all and the gate refused on an empty population — the fixture failing to
        # inject its own condition, which is the shape [R-ENF-04] names and which this
        # control's own earlier sibling caught once already.
        plant(tmp, HEAD + "\nraise RuntimeError('missing data')\n"
                          "fig, ax = plt.subplots()\n"
                          "fig.savefig(os.path.join(HERE, 'f.png'))\n")
        # A RUNNABLE SIBLING IS PART OF THE CONDITION. With only the broken script in
        # the sandbox the population anchor fires first and says "NONE of them ran",
        # which is correct and is a DIFFERENT refusal; the case under test is one
        # unrunnable script among scripts that do run.
        plant(tmp, CASES[3][1], name='figures_ok.py')
        rc, out = run(tmp)
        ok = rc != 0 and 'will not run' in out and 'NONE of them ran' not in out
        print('%-4s a figure script that will not run FAILS among scripts that do'
              % ('PASS' if ok else 'FAIL'))
        bad += 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # the ratchet excuses, and only what it names
    tmp = tempfile.mkdtemp(prefix='ncfar')
    try:
        build(tmp, ratchet={'engine/zzz_study/figures.py': ['known']})
        plant(tmp, CASES[0][1])
        rc, out = run(tmp)
        ok = rc == 0 and 'ratcheted' in out
        print('%-4s a ratcheted figure stays GREEN' % ('PASS' if ok else 'FAIL'))
        bad += 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # no figure scripts at all must FAIL
    tmp = tempfile.mkdtemp(prefix='ncfaz')
    try:
        build(tmp)
        rc, out = run(tmp)
        ok = rc != 0 and 'zero figure scripts' in out
        print('%-4s a run with no figure scripts FAILS [R-ENF-04]'
              % ('PASS' if ok else 'FAIL'))
        bad += 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # EVERY script unrunnable is the absence the count would hide behind
    tmp = tempfile.mkdtemp(prefix='ncfan')
    try:
        build(tmp, unrunnable=['engine/zzz_study/figures.py'])
        plant(tmp, HEAD + "\nraise RuntimeError('nope')\n"
                          "fig, ax = plt.subplots()\n"
                          "fig.savefig(os.path.join(HERE, 'f.png'))\n")
        rc, out = run(tmp)
        ok = rc != 0 and 'NONE of them ran' in out
        print('%-4s a run where every script refused to execute FAILS, even when they are '
              'all on the ratchet [R-ENF-04]' % ('PASS' if ok else 'FAIL'))
        bad += 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # AND THE GUARD MUST NOT WRITE. A gate that rewrites the work it checks is worse than
    # no gate: it would silently regenerate every study's committed figures.
    tmp = tempfile.mkdtemp(prefix='ncfaw')
    try:
        build(tmp)
        plant(tmp, CASES[3][1])
        run(tmp)
        wrote = os.path.exists(os.path.join(tmp, 'engine', 'zzz_study', 'f.png'))
        print('%-4s the gate writes no figure while checking' % ('PASS' if not wrote else 'FAIL'))
        bad += 0 if not wrote else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    total = len(CASES) + 5
    print('\n%d/%d conditions behaved as specified' % (total - bad, total))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
