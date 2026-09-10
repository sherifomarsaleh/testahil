"""THE EDITION DATE OF THE SCEM STUDY, WRITTEN ONCE.

Adopted 09-09-2026 with [R-ENF-06]. The date was typed in 3 places in this directory:
in the builders that NAME the delivered files and in the checkers that OPEN them. Both
halves agreed today, which is exactly why nothing had caught it -- they agree until an
edition changes, and that is the moment they matter.

TMGH is the worked example. It was rebuilt on fresh numbers and shipped under its old
edition name because six sites typed that date independently; a reader then holds a
document whose masthead agrees with its filename and disagrees with the model beside
it, which no comparison of those two can catch. And a CHECKER left on an old name is
worse than a stale document: it opens a file nobody receives and reports that file's
defects as current [L-066/L-067].

THE PREVIOUS EDITIONS ARE NAMED, NOT DELETED.
"""
import datetime as _dt

EDITION = _dt.date(2026, 9, 10)

# RECALIBRATION EDITION. The terminal risk-free rate was TYPED into this study's
# input register at 12.5%, and its own note flagged the alternative as a
# 'REVIEWABLE CHOICE' worth about 1.8% -- a defect recorded rather than fixed. It
# reads the house Egyptian macro path now. Fair value EGP 111.62 -> 122.67.
SUPERSEDES = (_dt.date(2026, 8, 6), _dt.date(2026, 9, 4), _dt.date(2026, 9, 7))

_D = EDITION.strftime('%d-%m-%Y')
_C = EDITION.strftime('%d%m%Y')

ISO = EDITION.isoformat()
WORDS = '%d %s %d' % (EDITION.day, EDITION.strftime('%B'), EDITION.year)
STUDY_DOCX = 'SCEM_Valuation_Study_' + _D + '_public.docx'
MODEL_XLSX = 'SCEM_Valuation_Model_' + _C + '_public.xlsx'
BIBLIO_DOCX = 'SCEM_Bibliography_' + _D + '.docx'


# THE PDF IS THE FILE A READER ACTUALLY OPENS, so it is named here too rather than
# spelled out again wherever one is baked or checked.
STUDY_PDF = STUDY_DOCX[:-len('.docx')] + '.pdf'
MODEL_PDF = MODEL_XLSX[:-len('.xlsx')] + '.pdf'
BIBLIO_PDF = BIBLIO_DOCX[:-len('.docx')] + '.pdf'

def prior(pattern):
    """The same artefact under a superseded edition, oldest first."""
    return [pattern.replace(_D, d.strftime('%d-%m-%Y')).replace(_C, d.strftime('%d%m%Y'))
            for d in SUPERSEDES]
