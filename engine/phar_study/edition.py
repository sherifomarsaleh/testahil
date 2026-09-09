"""THE EDITION DATE OF THE EIPICO (PHAR) STUDY, WRITTEN ONCE.

Same instrument as engine/swdy_study/edition.py and adopted for the same reason.
PHAR is the clearer case of the two. Its documents were rebuilt on 8 September on
numbers anchored to the 3 September close, and shipped under the edition name
09-08-2026 — the ninth of August — because that string was typed into ten places
across six files and nothing compared any of them with the price the model had
actually used. Its meta block said price_date 2026-08-06 while its own registered
spot input said "Egyptian Exchange close, 3 September 2026".

So a reader held a study dated a month before the price inside it, and every
instrument in this repository reported the study complete. Neither date is typed
any more: the edition comes from here and the price date is read off the spot
input's own registered date, so a document cannot state an anchor its model did
not use.

THE PREVIOUS EDITIONS ARE NAMED, NOT DELETED — a delivered document is what a
reader received on that day.
"""
import datetime as _dt

EDITION = _dt.date(2026, 9, 9)

SUPERSEDES = (_dt.date(2026, 8, 9),)

_D = EDITION.strftime('%d-%m-%Y')
_C = EDITION.strftime('%d%m%Y')

STUDY_DOCX = 'EIPICO_Valuation_Study_%s.docx' % _D
MODEL_XLSX = 'EIPICO_Valuation_Model_%s.xlsx' % _C
BIBLIO_DOCX = 'EIPICO_Bibliography_%s.docx' % _D


def prior(pattern):
    """The same artefact under a superseded edition, oldest first."""
    return [pattern.replace(_D, d.strftime('%d-%m-%Y')).replace(_C, d.strftime('%d%m%Y'))
            for d in SUPERSEDES]
