"""Bake every formula's evaluated value into a copy of the workbook, then render the
copy to PDF via LibreOffice (landscape, fit-to-width) so the reader's PDF carries
numbers, not formula strings. The delivered .xlsx stays formula-first; only the PDF
is baked. Values come from the same xlcalc evaluation recalc.py gates on."""
import os, subprocess, sys
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
SRCX = os.path.join(HERE, 'RIYADHCABLE_Valuation_Model_18082026_public.xlsx')
wb = openpyxl.load_workbook(SRCX)
bk = xlcalc.Book(wb)
n = 0
vals = {}
for sh, coord in bk.formula_cells():
    vals[(sh, coord)] = bk.cell_value(sh, coord)
    n += 1
for (sh, coord), v in vals.items():
    wb[sh][coord].value = v
for ws in wb.worksheets:
    ws.page_setup.orientation = 'landscape'
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr = openpyxl.worksheet.properties.PageSetupProperties(fitToPage=True)
BAKED = os.path.join(HERE, '_model_baked.xlsx')
wb.save(BAKED)
subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', HERE, BAKED],
               check=True, capture_output=True, timeout=300)
os.replace(os.path.join(HERE, '_model_baked.pdf'),
           os.path.join(HERE, 'RIYADHCABLE_Valuation_Model_18082026_public.pdf'))
os.remove(BAKED)
print(f'baked {n} formula values -> RIYADHCABLE_Valuation_Model_18082026_public.pdf')
