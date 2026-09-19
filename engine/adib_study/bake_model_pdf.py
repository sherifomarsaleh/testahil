"""Bake this study's delivered workbook to a values-visible PDF.

The builder is SHARED — engine/bake_model_pdf_shared.py. This file is the two facts that are
this study's own: which directory, and which edition module names the files.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import edition as _EDN
import xlcalc as _XL
from bake_model_pdf_shared import bake

if __name__ == '__main__':
    bake(HERE, _EDN, _XL)
