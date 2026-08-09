"""EGCH — does a source field actually NAME a source?

NOT YET WIRED INTO run_all.py, and deliberately so. It currently fails on 31 inputs and
those failures are TRUE: the industry-context layer (peer capacities, the EV/EBITDA band,
greenfield build costs, the mid-cycle urea level) and several market quotes cite nothing a
reader could open. The gate is not softened to make the build green, and the build is not
blocked on a debt that can only be cleared by going and finding the sources. Wire it in
when the register can pass it.


inputs.py asserts every input carries a source. It only ever checked the field was
non-empty. Four inputs passed that check with a source that describes a source rather than
citing one -- "Observed Egyptian industrial transaction and trading range", "Industry
capacity survey", "Listed granular urea free-on-board Egypt futures contract, front-month
settle". External critiques found all four, and one of them sets the top of the published
field while another is the single largest value driver in the study.

A source is sufficient if it names something a reader could go and look at: a filing, an
exchange or instrument, a named institution or dataset, a URL, or -- for a constructed
input -- the word "Constructed" followed by the construction.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)
from inputs import REG

NAMES = re.compile(
    r"audited financial statements|interim statements|note \d|auditor|cash-flow statement|"
    r"income statement|balance sheet|comparative column|country risk premium workbook|"
    r"damodaran|central bank|cbe|capmas|egyptian exchange|egx|investing\.com|tradingview|"
    r"cme|cbot|argus|trading economics|reuters|bloomberg|orascom|tecnimont|abu ?qir|"
    r"mubasher|marketscreener|https?://|epc award|prospectus|annual report|"
    r"sustainability report|monetary policy report|press release|constructed|derived",
    re.I)

VAGUE = re.compile(
    r"^(observed|industry|market|standard|typical|estimated|assumed|house|sector)\b|"
    r"\bsurvey\b(?!.*\b(by|from)\b)", re.I)

bad = []
for k, r in sorted(REG.items()):
    src = (r["source"] or "").strip()
    if not NAMES.search(src) or VAGUE.match(src):
        bad.append((k, r["layer"], src[:100]))

print(f"source audit: {len(REG)} inputs")
print(f"  sources that do not name anything a reader could look at: {len(bad)}")
for k, layer, src in bad:
    print(f"   ! {k}  [{layer}]  {src!r}")
if bad:
    sys.exit(f"FAIL: {len(bad)} input(s) carry a source that describes a source rather "
             f"than citing one. A four-field check that only tests for a non-empty string "
             f"is not a provenance check.")
print("PASS: every source names a document, an instrument, an institution or a construction")
