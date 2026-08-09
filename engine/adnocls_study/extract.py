import pdfplumber, sys, os
for f in sys.argv[1:]:
    out = os.path.splitext(f)[0] + ".txt"
    with pdfplumber.open(f) as pdf:
        parts=[]
        for i,p in enumerate(pdf.pages):
            parts.append(f"\n===== PAGE {i+1} =====\n" + (p.extract_text() or ""))
    open(out,"w").write("\n".join(parts))
    print(f, len(pdf.pages), "pages ->", out)
