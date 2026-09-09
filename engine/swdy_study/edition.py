"""THE EDITION DATE OF THE SWDY STUDY, WRITTEN ONCE.

It was written in thirteen places across eight files. That is not a tidiness
complaint: TMGH was rebuilt on fresh numbers on 06-09-2026 and shipped under its
02-09 edition name, because six of its own sites still said 02-09 and nothing
compared them. A reader then holds a document whose masthead disagrees with the
model beside it, and no gate in this repository can tell the difference between a
stale name and a stale number.

So the date lives here and every filename is derived from it. Changing the edition
is one line, and a site that forgets to import this module is the only way to get
the two out of step again — which is a thing a grep can find, where thirteen
independently typed strings were not.

THE PREVIOUS EDITIONS ARE NAMED, NOT DELETED. A delivered document is a historical
artefact: it is what a reader received on that day, and rebuilding over its filename
destroys the only record of what was said. New edition, new file, the old one stays.
"""
import datetime as _dt

EDITION = _dt.date(2026, 9, 9)

SUPERSEDES = (_dt.date(2026, 8, 5),)      # the delivered public edition

_D = EDITION.strftime('%d-%m-%Y')
_C = EDITION.strftime('%d%m%Y')           # the workbook drops the separators

STUDY_DOCX = 'SWDY_Valuation_Study_%s_public.docx' % _D
STUDY_PDF = 'SWDY_Valuation_Study_%s_public.pdf' % _D
MODEL_XLSX = 'SWDY_Valuation_Model_%s_public.xlsx' % _C
MODEL_PDF = 'SWDY_Valuation_Model_%s_public.pdf' % _C
BIBLIO_DOCX = 'SWDY_Bibliography_%s.docx' % _D
BIBLIO_PDF = 'SWDY_Bibliography_%s.pdf' % _D


def prior(pattern):
    """The same artefact under a superseded edition, oldest first — for a build that
    needs to read what it replaces rather than guess at its name."""
    out = []
    for d in SUPERSEDES:
        out.append(pattern.replace(_D, d.strftime('%d-%m-%Y'))
                          .replace(_C, d.strftime('%d%m%Y')))
    return out
