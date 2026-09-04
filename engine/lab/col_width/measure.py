import sys, os, subprocess, re
sys.path.insert(0, '/home/user/testahil/engine/tmgh_study')
os.chdir('/home/user/testahil/engine/tmgh_study')
import docx
from docx_helpers import table, style

TOKENS = ["1,234", "12,345", "102,747", "-110,168", "1,152,921", "-1,152,921",
          "35.79%", "-0.06", "Discount", "Enterprise", "attributable",
          "shareholders", "Depreciation", "Observations", "conversion"]
GRID = [round(1.00 + 0.05*i, 2) for i in range(0, 41)]   # 1.00 .. 3.00

d = docx.Document(); style(d)
for tok in TOKENS:
    for w in GRID:
        d.add_paragraph("MARK|%s|%.2f" % (tok, w))
        table(d, ["x"], [[tok]], [w])
d.save('/tmp/ma.docx')
