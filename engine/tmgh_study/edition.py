"""THE EDITION DATE OF THE TMGH STUDY, WRITTEN ONCE.

THIS IS THE STUDY THE WHOLE PATTERN WAS LEARNED ON. TMGH was rebuilt on fresh numbers
on 06-09-2026 and shipped under its 02-09 edition name, because six sites typed that
date independently and nothing compared them. A reader then holds a document whose
masthead agrees with its filename and disagrees with the model beside it — which no
gate can catch by comparing the two, since both are wrong in the same way.

The date lives here now. Changing the edition is one line, and a site that forgets to
import this module is something a grep can find, where six independently typed strings
were not.

Note the register document is called SOURCES here rather than Bibliography, which is
itself why a shared helper cannot guess these names and each study states its own.

THE PREVIOUS EDITIONS ARE NAMED, NOT DELETED.
"""
import datetime as _dt

EDITION = _dt.date(2026, 9, 2)

SUPERSEDES = ()

_D = EDITION.strftime('%d-%m-%Y')
_C = EDITION.strftime('%d%m%Y')

ISO = EDITION.isoformat()
STUDY_DOCX = 'TMGH_Valuation_Study_%s.docx' % _D
MODEL_XLSX = 'TMGH_Valuation_Model_%s.xlsx' % _C
SOURCES_DOCX = 'TMGH_Sources_%s.docx' % _D


# THE PDF IS THE FILE A READER ACTUALLY OPENS, so it is named here too rather than
# spelled out again wherever one is baked or checked.
STUDY_PDF = STUDY_DOCX[:-len('.docx')] + '.pdf'
MODEL_PDF = MODEL_XLSX[:-len('.xlsx')] + '.pdf'
# THIS STUDY'S REGISTER IS CALLED SOURCES, NOT BIBLIOGRAPHY, and a generic helper
# assuming the other name is exactly why each study states its own filenames here.
SOURCES_PDF = SOURCES_DOCX[:-len('.docx')] + '.pdf'

def prior(pattern):
    """The same artefact under a superseded edition, oldest first."""
    return [pattern.replace(_D, d.strftime('%d-%m-%Y')).replace(_C, d.strftime('%d%m%Y'))
            for d in SUPERSEDES]
