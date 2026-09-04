import sys, os
sys.path.insert(0,'/home/user/testahil/engine/tmgh_study'); os.chdir('/home/user/testahil/engine/tmgh_study')
import docx
from docx_helpers import table, style
d=docx.Document(); style(d)
for sz in (7.5, 8.5):
    for t in ["2026-07-28","(16,493)","102,747","35.79%"]:
        for w in [round(1.0+0.05*i,2) for i in range(41)]:
            d.add_paragraph("MARK|%s|%.1f|%.2f"%(t,sz,w)); table(d,["x"],[[t]],[w],size=sz)
d.save('/tmp/ms.docx')
