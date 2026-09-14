"""What a walk-forward run says about itself, read from ONE place.

A run directory is the subject of at least three gates -- the lessons register, the
fair-value calibration register and the forward-ranges check -- and each of them anchors
on the directory EXISTING. That is right: a run that has finished owes lessons, a
baseline, a delivered fair value and a study to print its far-year ranges in.

It is wrong for a run that has not finished. On 09-09-2026 one committed extraction script
made engine/adib_walkforward/ exist on every checkout, and all three gates reported a
FINISHED run missing its work. RUN_IN_PROGRESS.json is the declaration that fixes that,
on the same principle as ABUK's CALIBRATION_ONLY.json: silence is not a declaration, in
either direction.

THIS MODULE EXISTS SO THE DECLARATION IS READ ONCE. Three gates each testing
os.path.exists on the same filename is three copies of one rule, and copies drift -- the
fourth gate written next month would not know to look. A gate calls in_flight() and gets
the same answer as every other gate.

WHAT THIS MODULE DOES NOT DO: it does not decide whether the marker is HONEST. That test
lives in scripts/check_lessons_register.py, which refuses a marker sitting beside a
lessons draft, scores or projections -- a finished run wearing an unfinished label. The
test is the run's own artefacts rather than a clock, so there is no horizon to argue about
and no way to park a run behind this file.
"""
import json
import os

ENGINE = os.path.dirname(os.path.abspath(__file__))
MARKER = 'RUN_IN_PROGRESS.json'


def run_dir(ticker):
    return os.path.join(ENGINE, '%s_walkforward' % ticker.lower())


def in_flight(ticker=None, path=None):
    """True where the run declares itself unfinished. Pass a ticker or a directory."""
    d = path if path is not None else run_dir(ticker)
    return os.path.exists(os.path.join(d, MARKER))


def declaration(ticker=None, path=None):
    """The marker's contents, or None. Unreadable is NOT absent -- it raises, because a
    declaration nobody can read is not a declaration and must not read as one."""
    d = path if path is not None else run_dir(ticker)
    p = os.path.join(d, MARKER)
    if not os.path.exists(p):
        return None
    with open(p, encoding='utf-8') as fh:
        return json.load(fh)


def all_in_flight():
    """Every ticker whose run declares itself unfinished, upper-cased."""
    out = set()
    for name in os.listdir(ENGINE):
        if not name.endswith('_walkforward'):
            continue
        if in_flight(path=os.path.join(ENGINE, name)):
            out.add(name[:-len('_walkforward')].upper())
    return out
