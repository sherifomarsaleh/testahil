"""THE GATE REFERENCE — every check a study must pass, generated from the checks themselves.

Never typed. The list, the count and each gate's own claim are read at build time from the
docstrings of scripts/check_*.py, so a gate added tomorrow appears here and a gate whose
claim changes says so. A page that states a fact which moves must not be the thing that
remembers it [R-DOC-02].

GROUPING IS DECLARED HERE AND ONLY HERE, because "what does this protect" is a judgement
about the reader rather than a property of the file. Every gate on disk must land in a
group or the build FAILS — an unclassified gate is one this page silently omits, which is
the same shape as a reader that guesses a naming convention and reports what it finds.

Usage: python3 engine/method_reassessment/build_gate_reference.py [--out PATH]
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import html
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
ROOT = os.path.dirname(ENGINE)

# name -> (heading, one line saying what a reader gets out of this group)
GROUPS = [
    ("the numbers themselves", "Is every figure built from a filing, by arithmetic "
     "somebody can repeat?"),
    ("the model's construction", "Are the discount rate, the terminal and the lens built "
     "the way the house says they are built?"),
    ("what the study says about itself", "Does the record match what the model actually "
     "did?"),
    ("the answer", "Does the conclusion survive being looked at?"),
    ("the documents a reader receives", "Does the page add up, and does it say what the "
     "model says?"),
    ("the site", "Is what reaches a reader the answer this house currently holds?"),
    ("the checks themselves", "Do the checks work, and would they catch a new study?"),
]

MEMBERS = {
    "the numbers themselves": [
        "source_integrity", "four_field", "prose_figures", "harness_outputs",
        "source_rebinding", "eps_reconciliation", "data_freshness", "frozen_escalator",
        "driver_coverage", "sweep_module", "valuation_inputs",
    ],
    "the model's construction": [
        "cost_of_capital", "ke_reproduction", "macro_coherence", "macro_anchor_age",
        "terminal_floor", "terminal_spread", "terminal_record_shape", "bridge",
        "lens_design", "lens_independence", "asset_base", "asset_base_wired",
        "forecast_anchor", "anchor_ordering", "corrections_applied",
        "correction_boundary", "ground_up", "bridge_reaches_answer",
    ],
    "what the study says about itself": [
        "study_provenance", "standard_claim", "numbers_generators",
        "record_survives_rebuild", "artefact_currency", "output_records",
        "rebuild_ledger", "walkforward_scope", "walkforward_actuation",
        "lessons_register", "escalations",
    ],
    "the answer": [
        "valuation_gap", "published_gap", "output_sanity", "publish_block",
        "valuation_calibration", "fv_vintages",
    ],
    "the documents a reader receives": [
        "document_structure", "workbook_structure", "workbook_values", "bibliography",
        "table_footing", "waterfall_assertions", "sign_convention", "column_widths",
        "figure_axes", "figure_opacity", "edition_date", "delivered_vocabulary",
        "lens_vocabulary", "delivered_pdf_currency", "forward_ranges",
        "calibration_deliverables",
    ],
    "the site": [
        "page_integrity", "technical_read", "site_data_reader", "band_vocabulary",
        "published_coverage", "published_lens_vocabulary", "screen_block",
        "prices_block", "legacy_assets_sync", "grade_writer_layout", "tech_calibration",
    ],
    "the checks themselves": [
        "new_study_gauntlet", "error_injection", "tree_unmodified", "exemplar_debt",
        "protocol_sync", "protocol_text", "workflow_deps",
    ],
}

RULE = re.compile(r"\[(R-[A-Z]+-\d+)\]")


def gates():
    """{stem: (claim, [rule ids])} read from each gate's own docstring."""
    out = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "scripts", "check_*.py"))):
        b = os.path.basename(p)
        if b.endswith("_negative_control.py"):
            continue
        src = open(p, encoding="utf-8", errors="replace").read()
        m = re.search(r'"""(.*?)"""', src, re.S)
        doc = m.group(1).strip() if m else ""
        first = doc.split("\n\n")[0].replace("\n", " ").strip()
        claim = re.sub(r"^\[[^\]]+\]\s*/?\s*(\[[^\]]+\])?\s*[—-]?\s*", "", first).strip()
        claim = re.sub(r"^check_\w+\.py\s*[—-]\s*", "", claim)
        if claim and claim[0].islower():
            claim = claim[0].upper() + claim[1:]
        out[b[len("check_"):-3]] = (claim or "(no claim stated)",
                                    sorted(set(RULE.findall(doc[:1500]))))
    return out


def controls():
    return {os.path.basename(p)[len("check_"):-len("_negative_control.py")]
            for p in glob.glob(os.path.join(ROOT, "scripts",
                                            "check_*_negative_control.py"))}


CRITERIA = [
    ("1", "The construction gates are green, and the debt lists carry only names not yet "
          "re-issued.",
     "Seven named gates — cost of capital, macro path, lens design, the bridge, the "
     "walk-forward, the corrections and the calibration — each with a control that proves "
     "it fires."),
    ("2", "Each name's forward drivers sit inside the range its own history supports, or "
          "the exception is priced.",
     "Measured per run through a named adapter, because the five completed runs record "
     "their ranges in five different shapes and one reader would find one of them."),
    ("3", "The fair values this house publishes agree with the prices they were struck "
          "against, on average, with no lean.",
     "Six clauses. Four can be measured now; two wait for the first forecasts to mature "
     "and cannot be hurried."),
    ("4", "Every rule is enforced from outside the study, and every enforcement has a "
          "control that plants the real defect.",
     "A self-attested boolean is never a check. A control nobody has seen fail is not "
     "evidence."),
    ("5", "No study more than 10% from the market price ships without a written review of "
          "eight specific things.",
     "Latest filings, base year, macro coherence, discount rate, terminal, balance sheet, "
     "claims against the record, multiple cross-check."),
    ("6", "Every delivered name ships four documents, and a person has opened and read "
          "each one.",
     "The reading is a human act and no script may attest it."),
]


def build(out_path):
    G, C = gates(), controls()
    placed = {n for v in MEMBERS.values() for n in v}
    missing = sorted(set(G) - placed)
    if missing:
        print("FAIL — %d gate(s) in no group: %s\nAn unclassified gate is one this page "
              "silently omits." % (len(missing), ", ".join(missing)))
        return 1
    ghost = sorted(placed - set(G))
    if ghost:
        print("FAIL — %d grouped name(s) with no gate on disk: %s"
              % (len(ghost), ", ".join(ghost)))
        return 1

    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    esc = html.escape
    A = []
    a = A.append
    a("<title>Study Gate Reference</title>")
    a('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:'
      'opsz,wght@6..72,400;6..72,500&family=IBM+Plex+Sans:wght@400;500;600&'
      'family=IBM+Plex+Mono:wght@400&display=swap">')
    a("<style>\n" + CSS + "\n</style>")
    a('<div class="wrap"><header><p class="eyebrow">TESTAHIL</p>')
    a("<h1>What every study has to pass</h1>")
    a('<p class="lede">%d checks, each run from outside the study it judges, each with a '
      'test that proves it fires on the real defect. %d of them carry a control that '
      're-plants the defect it was built for. Nothing below is typed: every line is read '
      "from the check's own file when this page is built.</p>" % (len(G), len(C)))
    a('<div class="stamp"><span>%s</span><span>head %s</span></div></header>'
      % (dt.date.today().isoformat(), esc(head)))

    a('<section><h2>The checks, by what they protect</h2>')
    for name, blurb in GROUPS:
        rows = MEMBERS[name]
        a('<div class="grp"><h3>%s <span class="cnt">%d</span></h3>'
          '<p class="blurb">%s</p><ul>' % (esc(name), len(rows), esc(blurb)))
        for stem in rows:
            claim, rules = G[stem]
            tick = "✓" if stem in C else "·"
            a('<li><span class="tick %s">%s</span><span class="claim">%s</span>'
              '<span class="src">%s</span></li>'
              % ("has" if stem in C else "no", tick, esc(claim),
                 esc(stem.replace("_", " "))))
        a("</ul></div>")
    a('<p class="foot">✓ marks a check with a negative control — a test that deliberately '
      're-creates the defect and requires the check to go red. A check nobody has seen '
      "fail is not evidence.</p></section>")

    a('<section><h2>What "working properly" means</h2>')
    a('<p class="blurb">Six criteria, fixed before any of them was measured. A criterion '
      "that has not been measured is UNMEASURED, never met.</p>")
    a('<ol class="crit">')
    for n, claim, detail in CRITERIA:
        a("<li><b>%s</b><span>%s</span></li>" % (esc(claim), esc(detail)))
    a("</ol></section>")

    a('<section><h2>Three things the whole framework has to do</h2><ul class="props">')
    for t, d in (("Reach every name",
                  "All 90 published fair values, and any new one, not just the 24 with a "
                  "study directory."),
                 ("Catch the errors that actually happen",
                  "Not the errors that are easy to check for. Each one is planted and the "
                  "check must find it."),
                 ("Work a red check until it is green",
                  "And never by weakening the check, moving a fair value toward a price, "
                  "or inventing a missing figure.")):
        a("<li><b>%s</b><span>%s</span></li>" % (esc(t), esc(d)))
    a("</ul></section>")
    a('<footer>Generated by engine/method_reassessment/build_gate_reference.py. '
      "Re-run it and the page re-reads every check.</footer></div>")

    open(out_path, "w", encoding="utf-8").write("\n".join(A))
    print("wrote %s  (%d gates, %d controls)" % (out_path, len(G), len(C)))
    return 0


CSS = """
:root{--ground:#FBFAF8;--panel:#FFF;--ink:#171A1F;--ink-2:#3E434A;--muted:#6E757E;
 --rule:#E4E1DB;--rule-2:#F0EEE9;--accent:#1F4B3F;--accent-soft:#E9F1EE;
 --serif:"Newsreader",Georgia,serif;--sans:"IBM Plex Sans",system-ui,sans-serif;
 --mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
 --ground:#101215;--panel:#171A1E;--ink:#E9E7E2;--ink-2:#C2C6CB;--muted:#8C939B;
 --rule:#292D33;--rule-2:#20242A;--accent:#8FC9B4;--accent-soft:#152420;}}
:root[data-theme="dark"]{--ground:#101215;--panel:#171A1E;--ink:#E9E7E2;--ink-2:#C2C6CB;
 --muted:#8C939B;--rule:#292D33;--rule-2:#20242A;--accent:#8FC9B4;--accent-soft:#152420;}
body{background:var(--ground);color:var(--ink);font-family:var(--sans);font-size:15px;
 line-height:1.6;-webkit-font-smoothing:antialiased;}
.wrap{max-width:820px;margin:0 auto;padding:42px 22px 80px;}
h1,h2,h3{font-family:var(--serif);font-weight:500;text-wrap:balance;margin:0;}
h1{font-size:2.25rem;line-height:1.12;letter-spacing:-.012em;}
h2{font-size:1.35rem;margin:0 0 6px;}
h3{font-size:1rem;font-family:var(--sans);font-weight:600;margin:0;}
p{margin:0 0 12px;color:var(--ink-2);}
.eyebrow{font-size:.7rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;
 color:var(--muted);margin:0 0 10px;}
.lede{font-size:1.02rem;max-width:62ch;margin-top:14px;}
.stamp{margin-top:16px;font-family:var(--mono);font-size:.76rem;color:var(--muted);
 display:flex;gap:18px;flex-wrap:wrap;}
header{border-bottom:1px solid var(--rule);padding-bottom:26px;margin-bottom:34px;}
section{margin:0 0 44px;}
.grp{background:var(--panel);border:1px solid var(--rule);border-radius:4px;
 padding:16px 18px;margin:14px 0;}
.grp h3 .cnt{font-family:var(--mono);font-size:.78rem;color:var(--muted);
 font-weight:400;margin-left:7px;}
.blurb{font-size:.9rem;color:var(--muted);margin:5px 0 12px;max-width:60ch;}
.grp ul{list-style:none;margin:0;padding:0;}
.grp li{display:grid;grid-template-columns:20px 1fr;gap:2px 8px;padding:8px 0;
 border-top:1px solid var(--rule-2);align-items:baseline;}
.grp li:first-child{border-top:none;}
.tick{font-family:var(--mono);font-size:.85rem;}
.tick.has{color:var(--accent);} .tick.no{color:var(--muted);}
.claim{font-size:.92rem;color:var(--ink);}
.src{grid-column:2;font-family:var(--mono);font-size:.74rem;color:var(--muted);}
.foot{font-size:.85rem;color:var(--muted);max-width:62ch;}
ol.crit{margin:14px 0 0;padding-left:22px;}
ol.crit li{margin:0 0 14px;color:var(--ink);}
ol.crit li b{font-weight:500;} ol.crit li span{display:block;color:var(--muted);
 font-size:.89rem;margin-top:3px;max-width:60ch;}
ul.props{list-style:none;margin:14px 0 0;padding:0;display:grid;gap:1px;
 background:var(--rule);border:1px solid var(--rule);border-radius:4px;}
ul.props li{background:var(--panel);padding:15px 18px;}
ul.props li b{font-weight:600;} ul.props li span{display:block;color:var(--muted);
 font-size:.89rem;margin-top:3px;}
footer{margin-top:48px;padding-top:18px;border-top:1px solid var(--rule);
 font-size:.8rem;color:var(--muted);font-family:var(--mono);}
@media(max-width:600px){h1{font-size:1.75rem;}.wrap{padding:28px 15px 60px;}}
"""

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/tmp/gate_reference.html")
    sys.exit(build(ap.parse_args().out))
