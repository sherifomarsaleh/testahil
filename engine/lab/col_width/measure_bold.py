import sys, os
sys.path.insert(0,'/home/user/testahil/engine/tmgh_study'); os.chdir('/home/user/testahil/engine/tmgh_study')
import docx
from docx_helpers import table, style
d=docx.Document(); style(d)
TOK=["Discount","Enterprise","Observations","102,747","-110,168","35.79%","conversion"]
for t in TOK:
    for w in [round(1.0+0.05*i,2) for i in range(41)]:
        d.add_paragraph("MARK|%s|%.2f" % (t,w))
        table(d,[t],[["x"]],[w])          # the TOKEN AS THE HEADER, i.e. bold
d.save('/tmp/mb.docx')
