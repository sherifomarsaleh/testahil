"""Find the pages that matter in a scanned AMOC filing, cheaply.

Full-quality OCR of the whole archive is hours of work for pages nobody reads.
This pass renders each page at 150 dpi and asks only ONE question — which
statement or note is this? — using the headings, which survive a coarse render
even where the digits do not.

NOTHING NUMERIC IS TAKEN FROM THIS PASS.  It locates; the figures are then read
from the rendered page at full resolution and footed against their own
arithmetic.  Keeping the two apart is deliberate: a coarse OCR that is good
enough to find a heading is NOT good enough to read a nine-digit figure, and
letting one pass do both is how a misread digit enters a panel looking clean.
"""
import os, re, json, subprocess, tempfile, sys
import pymupdf

SRC = os.environ.get("AMOC_SCRATCH",
    "/tmp/claude-0/-home-user-testahil/50e83873-11d1-59bd-8752-622f52dccf21/scratchpad/amoc_src")
OUT = os.path.join(SRC, "locate")

# Headings, English and Arabic, as these filings actually print them.
MARKS = [
    ("income_statement", r"income statement|statement of (profit|income)|profit or loss|"
                         r"قائمة الدخل|الارباح والخسائر|الأرباح والخسائر"),
    ("balance_sheet",    r"balance sheet|statement of financial position|"
                         r"قائمة المركز المالي|الميزانية"),
    ("cash_flow",        r"cash flow|قائمة التدفقات النقدية|التدفقات النقدية"),
    ("equity",           r"changes in equity|قائمة التغير في حقوق|التغير فى حقوق"),
    ("sales_by_product", r"net sales|sales by product|صافى المبيعات|صافي المبيعات|"
                         r"المبيعات حسب|كميه|كمية"),
    ("cost_of_sales",    r"cost of sales|تكلفة المبيعات|تكلفه المبيعات"),
    ("fixed_assets",     r"fixed assets|property, plant|الاصول الثابتة|الأصول الثابتة"),
    ("loans",            r"loans|borrowing|قروض|التسهيلات"),
    ("provisions",       r"provisions|المخصصات"),
]


def page_text(page, dpi=150, lang="eng+ara"):
    t = page.get_text()
    if len(t.strip()) > 250:
        return t, "text"
    pix = page.get_pixmap(dpi=dpi)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        f.write(pix.tobytes("png")); png = f.name
    try:
        r = subprocess.run(["tesseract", png, "stdout", "-l", lang, "--psm", "6"],
                           capture_output=True, timeout=180)
        return r.stdout.decode("utf-8", "replace"), "ocr150"
    finally:
        os.unlink(png)


def locate(pdf, lang="eng+ara"):
    os.makedirs(OUT, exist_ok=True)
    dest = os.path.join(OUT, os.path.basename(pdf)[:-4] + ".hits.json")
    if os.path.exists(dest):
        return json.load(open(dest))
    doc = pymupdf.open(os.path.join(SRC, pdf))
    hits = {}
    for pno, page in enumerate(doc, 1):
        txt, route = page_text(page, lang=lang)
        low = txt.lower()
        for name, pat in MARKS:
            if re.search(pat, low):
                hits.setdefault(name, []).append({"page": pno, "route": route})
    json.dump({"pdf": pdf, "pages": len(doc), "hits": hits}, open(dest, "w"), indent=1)
    return {"pdf": pdf, "pages": len(doc), "hits": hits}


if __name__ == "__main__":
    for pdf in sys.argv[1:]:
        r = locate(pdf)
        print("%s (%d pages)" % (r["pdf"][:36], r["pages"]))
        for k, v in sorted(r["hits"].items()):
            print("   %-18s %s" % (k, [x["page"] for x in v][:14]))
