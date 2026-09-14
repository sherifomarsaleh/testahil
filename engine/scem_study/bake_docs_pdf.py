"""Render this study's delivered documents to PDF. Builder: engine/bake_docs_pdf_shared.py.

This file is the one fact that is this study's own: which edition module names the files.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import edition as _EDN
from bake_docs_pdf_shared import bake

if __name__ == '__main__':
    raise SystemExit(bake(HERE, _EDN))
