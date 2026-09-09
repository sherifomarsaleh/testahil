#!/usr/bin/env python3
"""[R-FCAL-01 §6 AMENDED 09-09-2026] — a run that struck nothing has to SAY SO.

The rule as written required every walk-forward to deliver "the UPDATED fundamental
analysis". You cannot update what does not exist, and it was written assuming every run
has a study behind it. ABUK is the first name where that is false and it will not be the
last: the campaign runs the walk-forward across the whole book, and most covered names
carry no current-standard study.

So a campaign run on such a name may be CALIBRATION-ONLY: it still owes its lessons
register, its run records, the study document and the Excel model — the principal's own
condition, "we need a study in docx and the model in excel format as well" — but it need
not STRIKE A FAIR VALUE.

WHAT IS OPTIONAL IS THE STRUCK VALUE, NEVER THE WORK.

THE DECLARATION IS THE WHOLE OF THE EXEMPTION. A run that simply omits a fair value and
says nothing is unfinished exactly as it was before; five gates were red on ABUK for that
and they were RIGHT, which is why the rule was amended rather than the gates widened
[R-COC-01]. Silence is not a claim, and this module exists so that a claim has to be made
in a form a gate can read.

THE SECOND CONDITION IS KEYED ON THE STRUCK VALUE, NOT ON A DIRECTORY, and the difference
matters here. The obvious test — "no study directory exists" — breaks the moment ABUK's
docx and workbook are built, because the directory then exists while the run still,
correctly, strikes nothing. So the test is whether a CENTRAL is published: a name whose
study already asserts a fair value may not quietly drop it behind this exemption.
"""
import json
import os

ENGINE = os.path.dirname(os.path.abspath(__file__))
FILENAME = 'CALIBRATION_ONLY.json'

REQUIRED = ('ticker', 'declared_on', 'struck_no_fair_value', 'why', 'produced')


def path_for(ticker):
    return os.path.join(ENGINE, '%s_walkforward' % ticker.lower(), FILENAME)


def _published_central(ticker):
    """The central the study asserts, or None. Reads the file, never a boolean."""
    p = os.path.join(ENGINE, '%s_study' % ticker.lower(), 'study_numbers.json')
    if not os.path.exists(p):
        return None
    try:
        j = json.load(open(p, encoding='utf-8'))
    except (OSError, ValueError):
        # [R-ENF-04] — unreadable is not absent. Refuse the exemption rather than
        # granting it on a file nobody could read.
        return 'UNREADABLE'
    c = j.get('central')
    if isinstance(c, dict):
        c = c.get('value')
    return c if isinstance(c, (int, float)) else None


def declared(ticker):
    """(ok, why_not) — is this run properly declared calibration-only?

    Returns a PAIR, and it is always truthy if tested bare. Unpack it. Two gates in
    this repository were bitten by exactly that on ratchet_shape.excused() in one day.
    """
    p = path_for(ticker)
    if not os.path.exists(p):
        return False, 'no %s in the run directory — silence is not a declaration' % FILENAME
    try:
        d = json.load(open(p, encoding='utf-8'))
    except (OSError, ValueError) as exc:
        return False, 'the declaration will not parse (%s)' % type(exc).__name__
    missing = [k for k in REQUIRED if k not in d]
    if missing:
        return False, 'the declaration is missing %s' % ', '.join(missing)
    if d.get('struck_no_fair_value') is not True:
        return False, 'the declaration does not assert struck_no_fair_value'
    cen = _published_central(ticker)
    if cen == 'UNREADABLE':
        return False, ('%s_study carries a numbers file that will not parse, so whether '
                       'it asserts a central cannot be established' % ticker.lower())
    if cen is not None:
        return False, ('%s already publishes a central of %s — the exemption is not '
                       'available to a name that strikes a fair value' % (ticker, cen))
    return True, ''


def all_declared():
    """{ticker: why_not} for every run directory that is NOT properly declared."""
    import glob
    out = {}
    for d in sorted(glob.glob(os.path.join(ENGINE, '*_walkforward'))):
        tk = os.path.basename(d)[:-len('_walkforward')].upper()
        ok, why = declared(tk)
        if not ok:
            out[tk] = why
    return out
