#!/usr/bin/env python3
"""Assemble GBCO_Valuation_Study_{edition}_public.docx from the three content parts.

There was no runner. The three parts share one `doc` through docx_base and nothing saved
it, so the delivered edition was produced by an ad-hoc command that is not in the
repository — which means the document a reader receives could not be rebuilt from the
study's own code. It can now.

Every path resolves against HERE, so the file lands beside this script whatever directory
the run is invoked from.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..'))
os.chdir(HERE)

import docx_base                                                    # noqa: E402
import docx_A                                                       # noqa: E402,F401
import docx_B                                                       # noqa: E402,F401
import docx_C                                                       # noqa: E402,F401

EDITION = docx_A.EDITION_STAMP
OUT = os.path.join(HERE, 'GBCO_Valuation_Study_%s_public.docx' % EDITION)
docx_base.doc.save(OUT)
print('wrote', os.path.relpath(OUT, os.path.dirname(HERE)))
