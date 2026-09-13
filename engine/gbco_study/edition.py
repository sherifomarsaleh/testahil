"""THE EDITION DATE OF THE GB CORP STUDY, WRITTEN ONCE.

WHY THIS FILE ARRIVED LATE. This study's build declared two PDF-baking steps and both
import an edition module — which did not exist, so the build died on them and the three
delivered PDFs had never been rendered by a build at all. They were made by hand, and a
file made by hand is a file that goes stale the moment nobody remembers to remake it:
check_artefact_freshness reported all three behind the documents they are rendered from.

The date lives here now. Changing the edition is one line, and a site that forgets to
import this module is something a grep can find, where independently typed strings are
not.

THE PREVIOUS EDITIONS ARE NAMED, NOT DELETED. A delivered document is what a reader
received on that day; rebuilding over its filename destroys the only record of what was
said.
"""
import datetime as _dt

EDITION = _dt.date(2026, 9, 10)

SUPERSEDES = (_dt.date(2026, 7, 8), _dt.date(2026, 9, 7))

_D = EDITION.strftime('%d-%m-%Y')
_C = EDITION.strftime('%d%m%Y')

ISO = EDITION.isoformat()
WORDS = '%d %s %d' % (EDITION.day, EDITION.strftime('%B'), EDITION.year)
PRIOR_WORDS = '%d %s %d' % (SUPERSEDES[-1].day, SUPERSEDES[-1].strftime('%B'),
                            SUPERSEDES[-1].year)

# THIS STUDY'S DELIVERED FILES CARRY THE _public SUFFIX on the study and the workbook and
# NOT on the bibliography, which is exactly why a generic helper cannot guess these names
# and each study states its own.
STUDY_DOCX = 'GBCO_Valuation_Study_%s_public.docx' % _D
BIBLIO_DOCX = 'GBCO_Bibliography_%s.docx' % _D
MODEL_XLSX = 'GBCO_Valuation_Model_%s_public.xlsx' % _C

STUDY_PDF = STUDY_DOCX[:-len('.docx')] + '.pdf'
BIBLIO_PDF = BIBLIO_DOCX[:-len('.docx')] + '.pdf'
MODEL_PDF = MODEL_XLSX[:-len('.xlsx')] + '.pdf'


def prior(pattern):
    """The same artefact under a superseded edition, oldest first."""
    return [pattern.replace(_D, d.strftime('%d-%m-%Y')).replace(_C, d.strftime('%d%m%Y'))
            for d in SUPERSEDES]
