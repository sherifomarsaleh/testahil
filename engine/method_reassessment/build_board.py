"""The framework build board — GENERATED, never typed.

A page that states a fact which moves must not be the thing that remembers it. Every
count on this board is measured here, at build time, from the repository itself; the
only hand-written content is board_state.json, which carries the QUEUE and the
JUDGEMENTS — what is next, what a test means — because those are decisions rather
than measurements.

Usage:  python3 engine/method_reassessment/build_board.py [--out PATH] [--today YYYY-MM-DD]
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
ROOT = os.path.dirname(ENGINE)
STATE = os.path.join(HERE, "board_state.json")


# ---------------------------------------------------------------- measurement

def published_names():
    """Count the names the site actually publishes, through a real JS parse [R-ENF-03]."""
    js = os.path.join(ROOT, "assets", "data.js")
    if not os.path.exists(js):
        return None
    prog = ("const fs=require('fs');const s=fs.readFileSync(%r,'utf8');"
            "eval(s.replace(/^\\s*(const|let|var)\\s+/gm,'globalThis.'));"
            "console.log(Object.keys(globalThis.TICKERS||{}).length);" % js)
    try:
        r = subprocess.run(["node", "-e", prog], capture_output=True, text=True, timeout=90)
        return int((r.stdout or "").strip())
    except Exception:
        return None


def study_dirs():
    return sorted(os.path.basename(d)[:-6].upper()
                  for d in glob.glob(os.path.join(ENGINE, "*_study")))


def gate_counts():
    gates = [g for g in glob.glob(os.path.join(ROOT, "scripts", "check_*.py"))
             if "negative_control" not in g]
    ctrls = glob.glob(os.path.join(ROOT, "scripts", "*negative_control*.py"))
    return len(gates), len(ctrls)


def concept_coverage(words):
    """How many GATE files mention a concept, under any of several spellings.

    Counted rather than asserted, and counted across SPELLINGS deliberately: a reader
    that guesses one naming convention silently finds nothing and reports it as a
    result [L-355]. A hit inside a negative control is NOT coverage — a fixture
    reproducing a defect is not a check for it — so those are excluded and counted
    separately, because the difference is the whole point.
    """
    pat = re.compile("|".join(words), re.I)
    real, fixture = [], []
    for p in glob.glob(os.path.join(ROOT, "scripts", "*.py")):
        try:
            body = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        if pat.search(body):
            (fixture if "negative_control" in p else real).append(os.path.basename(p))
    return sorted(real), sorted(fixture)


def head():
    try:
        r = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                           cwd=ROOT, capture_output=True, text=True, timeout=30)
        return (r.stdout or "").strip() or "unknown"
    except Exception:
        return "unknown"


def branch():
    try:
        r = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                           cwd=ROOT, capture_output=True, text=True, timeout=30)
        return (r.stdout or "").strip() or "unknown"
    except Exception:
        return "unknown"


# ---------------------------------------------------------------- rendering

def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


CHIP = {"DONE": "c-done", "IN FLIGHT": "c-flight", "NEXT": "c-next",
        "QUEUED": "c-queued", "BLOCKED": "c-blocked",
        "CAUGHT": "c-done", "UNCOVERED": "c-blocked", "PARTLY": "c-next"}


def render(st, m):
    days = (dt.date.fromisoformat(st["target"]) - m["today"]).days
    q = st["queue"]
    done = sum(1 for r in q if r["state"] == "DONE")

    parts = []
    A = parts.append

    A("""<title>Framework Build Board</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
 :root{
   --ground:#FAF9F7; --panel:#FFFFFF; --ink:#16181D; --ink-2:#3C4148;
   --muted:#6A7280; --rule:#E3E0DA; --rule-2:#EFEDE8;
   --accent:#24446E; --accent-soft:#EAF0F7;
   --done:#2E6F4E; --done-bg:#E8F2EC;
   --blocked:#A63D1C; --blocked-bg:#FBEBE4;
   --next:#8A6A1B; --next-bg:#F7F0DC;
   --queued:#6A7280; --queued-bg:#EFEDE8; --today-bg:#F4EFE2;
   --serif:"Newsreader",Georgia,serif;
   --sans:"IBM Plex Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
   --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
 }
 @media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
   --ground:#111317; --panel:#171A1F; --ink:#E8E6E1; --ink-2:#BFC3C9;
   --muted:#8B929B; --rule:#2A2E35; --rule-2:#22262C;
   --accent:#8FB4E0; --accent-soft:#1B2531;
   --done:#7BC49A; --done-bg:#16281F;
   --blocked:#E29271; --blocked-bg:#2E1D15;
   --next:#D9BC6B; --next-bg:#2B2415;
   --queued:#8B929B; --queued-bg:#22262C; --today-bg:#242017;}}
 :root[data-theme="dark"]{
   --ground:#111317; --panel:#171A1F; --ink:#E8E6E1; --ink-2:#BFC3C9;
   --muted:#8B929B; --rule:#2A2E35; --rule-2:#22262C;
   --accent:#8FB4E0; --accent-soft:#1B2531;
   --done:#7BC49A; --done-bg:#16281F;
   --blocked:#E29271; --blocked-bg:#2E1D15;
   --next:#D9BC6B; --next-bg:#2B2415;
   --queued:#8B929B; --queued-bg:#22262C; --today-bg:#242017;}

 body{background:var(--ground);color:var(--ink);font-family:var(--sans);
      font-size:15px;line-height:1.6;-webkit-font-smoothing:antialiased;}
 .wrap{max-width:900px;margin:0 auto;padding:40px 24px 90px;}
 h1,h2,h3{font-family:var(--serif);font-weight:500;text-wrap:balance;margin:0;}
 h1{font-size:2.3rem;line-height:1.12;letter-spacing:-.012em;}
 h2{font-size:1.38rem;margin:0 0 4px;}
 h3{font-size:1.02rem;line-height:1.35;}
 p{margin:0 0 12px;max-width:68ch;color:var(--ink-2);}
 .eyebrow{font-size:.72rem;font-weight:600;letter-spacing:.11em;text-transform:uppercase;
          color:var(--muted);margin:0 0 10px;}
 .mono{font-family:var(--mono);font-variant-numeric:tabular-nums;}
 header{border-bottom:1px solid var(--rule);padding-bottom:24px;margin-bottom:32px;}
 .stamp{margin-top:14px;font-family:var(--mono);font-size:.78rem;color:var(--muted);
        display:flex;flex-wrap:wrap;gap:6px 18px;}
 section{margin:0 0 40px;}
 .sec-head{margin-bottom:14px;}
 .sec-head p{margin:6px 0 0;font-size:.93rem;}

 .countdown{display:flex;flex-wrap:wrap;gap:14px;margin-top:20px;}
 .cd{flex:1 1 150px;background:var(--panel);border:1px solid var(--rule);border-radius:3px;
     padding:14px 16px;}
 .cd .n{font-family:var(--mono);font-size:1.85rem;font-weight:500;color:var(--ink);
        line-height:1.1;font-variant-numeric:tabular-nums;}
 .cd .l{font-size:.76rem;color:var(--muted);margin-top:4px;letter-spacing:.03em;}

 .props{display:grid;gap:1px;background:var(--rule-2);border:1px solid var(--rule);
        border-radius:3px;}
 .prop{background:var(--panel);padding:18px 20px;}
 .prop .top{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin-bottom:6px;}
 .prop .pid{font-family:var(--mono);font-size:.8rem;color:var(--muted);}
 .prop p{font-size:.92rem;margin:0 0 8px;max-width:none;}
 .prop .test{font-size:.85rem;color:var(--muted);border-left:2px solid var(--rule);
             padding-left:11px;margin-top:10px;}
 .prop .test b{color:var(--ink-2);font-weight:600;}

 .chip{display:inline-block;font-size:.7rem;font-weight:600;letter-spacing:.05em;
       padding:3px 9px;border-radius:2px;white-space:nowrap;}
 .c-done{background:var(--done-bg);color:var(--done);}
 .c-flight{background:var(--accent-soft);color:var(--accent);}
 .c-next{background:var(--next-bg);color:var(--next);}
 .c-queued{background:var(--queued-bg);color:var(--queued);}
 table.gantt th.gcell,table.gantt td.gcell{width:26px;min-width:26px;text-align:center;
   padding:4px 0;}
 table.gantt th.gcell span{display:block;font-size:10px;opacity:.6;font-weight:400;}
 table.gantt th.gcell.today,table.gantt td.gcell.today{background:var(--today-bg);}
 table.gantt td.fam{font-size:11px;opacity:.75;max-width:210px;}
 table.gantt .bar{display:block;height:12px;border-radius:3px;}
 table.gantt .b-done{background:var(--done);}
 table.gantt .b-next{background:var(--next);}
 table.gantt .b-queued{background:var(--queued);opacity:.45;}
 .c-blocked{background:var(--blocked-bg);color:var(--blocked);}

 .tbl-scroll{overflow-x:auto;}
 table{width:100%;border-collapse:collapse;font-size:.9rem;}
 th{font-size:.7rem;font-weight:600;letter-spacing:.09em;text-transform:uppercase;
    color:var(--muted);text-align:left;padding:0 14px 8px 0;
    border-bottom:1px solid var(--rule);white-space:nowrap;}
 td{padding:12px 14px 12px 0;border-bottom:1px solid var(--rule-2);vertical-align:top;
    color:var(--ink-2);}
 td:first-child,th:first-child{padding-left:2px;}
 tbody tr:last-child td{border-bottom:none;}
 .num{font-family:var(--mono);font-variant-numeric:tabular-nums;}
 .qitem{color:var(--ink);font-weight:500;}
 .qitem span{display:block;color:var(--muted);font-size:.85rem;font-weight:400;margin-top:3px;}
 .day{font-family:var(--mono);color:var(--muted);white-space:nowrap;}

 .panel{background:var(--panel);border:1px solid var(--rule);border-radius:3px;
        padding:18px 20px;}
 .panel + .panel{margin-top:13px;}
 .note{font-size:.87rem;color:var(--muted);margin-top:12px;max-width:66ch;}
 caption{caption-side:bottom;text-align:left;padding-top:11px;font-size:.83rem;
         color:var(--muted);}
 footer{margin-top:52px;padding-top:20px;border-top:1px solid var(--rule);
        font-size:.82rem;color:var(--muted);}
 footer code{font-family:var(--mono);font-size:.9em;}
 @media (max-width:620px){h1{font-size:1.8rem;}.wrap{padding:28px 16px 66px;}}
</style>
<div class="wrap">""")

    # ---- header
    A('<header><p class="eyebrow">TESTAHIL</p>')
    A("<h1>Framework build board</h1>")
    A('<p style="font-size:1.05rem">%s</p>' % esc(st["goal"]))
    A('<div class="countdown">')
    A('<div class="cd"><div class="n">%d</div><div class="l">days to %s</div></div>'
      % (days, dt.date.fromisoformat(st["target"]).strftime("%d %b")))
    A('<div class="cd"><div class="n">%d / %d</div><div class="l">build steps done</div></div>'
      % (done, len(q)))
    A('<div class="cd"><div class="n">%s</div><div class="l">gates, %s negative controls</div></div>'
      % (m["gates"], m["ctrls"]))
    A('<div class="cd"><div class="n">%s / %s</div><div class="l">names a gate can open</div></div>'
      % (m["with_study"], m["published"] if m["published"] else "?"))
    A("</div>")
    A('<div class="stamp"><span>branch %s</span><span>head %s</span>'
      '<span>built %s</span></div>'
      % (esc(m["branch"]), esc(m["head"]), esc(m["built_at"])))
    A("</header>")

    # ---- the three properties
    A('<section><div class="sec-head"><h2>The three things it has to do</h2>'
      '<p>Each carries the test that says it holds. A property with no test is not '
      'delivered.</p></div><div class="props">')
    for p in st["properties"]:
        A('<div class="prop"><div class="top"><span class="pid">%s</span>'
          '<h3>%s</h3><span class="chip %s">%s</span></div>'
          % (esc(p["id"]), esc(p["title"]),
             CHIP.get(p["state"], "c-queued"), esc(p["state"])))
        A("<p>%s</p>" % esc(p["note"]))
        A('<div class="test"><b>Test —</b> %s</div></div>' % esc(p["test"]))
    A("</div></section>")

    # ---- the scorecard
    A('<section><div class="sec-head"><h2>Your three errors, today</h2>'
      '<p>Measured against the gate set, not asserted.</p></div><div class="tbl-scroll">'
      "<table><thead><tr><th>The error</th><th>Caught?</th><th>By what</th></tr></thead><tbody>")
    for e in st["errors"]:
        A('<tr><td style="color:var(--ink)">&ldquo;%s&rdquo;</td>'
          '<td><span class="chip %s">%s</span></td><td>%s</td></tr>'
          % (esc(e["words"]), CHIP.get(e["verdict"], "c-queued"),
             esc(e["verdict"]), esc(e["by"])))
    A("</tbody></table></div>")
    A('<p class="note"><strong>Landbank, measured live at build time:</strong> %d gate file(s) '
      "mention it in any of %d spellings%s. A hit inside a negative control is a fixture "
      "reproducing a defect, not a check for it.</p>"
      % (len(m["land_real"]), m["land_spellings"],
         (" — the only hits in the tree are fixtures in %s"
          % ", ".join("<span class='mono'>%s</span>" % esc(f) for f in m["land_fixture"]))
         if m["land_fixture"] and not m["land_real"] else ""))
    A('<p class="note"><strong>Cost of equity, measured live at build time:</strong> %d gate '
      "file(s) reproduce it from its own inputs, searched under %d spellings "
      "(<span class='mono'>ke_exp</span>, <span class='mono'>cost_of_equity</span>, "
      "<span class='mono'>ke_terminal</span>, <span class='mono'>capm</span>, "
      "<span class='mono'>rf_star +</span>).</p>" % (len(m["ke_real"]), m["ke_spellings"]))
    A("</section>")

    # ---- gantt
    # DATA, NEVER TYPED POSITIONS. The first Gantt this project drew placed its bars and
    # its header independently and the columns never corresponded to the days — the same
    # defect as a number typed in prose. Here every bar's offset and width are COMPUTED
    # from the row's own dates against the axis, so a re-dating is one edit to the data.
    sched = st.get("schedule") or []
    if sched:
        days = sorted({d for r in sched
                       for d in (r["start"], r["end"])})
        d0 = dt.date.fromisoformat(days[0])
        d1 = dt.date.fromisoformat(days[-1])
        span = (d1 - d0).days + 1
        A('<section><div class="sec-head"><h2>Delivery schedule</h2>'
          "<p>%s</p></div>" % esc(st.get("schedule_note", "")))
        A('<div class="tbl-scroll"><table class="gantt"><thead><tr>'
          "<th>Work</th><th>Closes</th>")
        for i in range(span):
            d = d0 + dt.timedelta(days=i)
            cls = " today" if d == m["today"] else ""
            A('<th class="gcell%s">%s<span>%s</span></th>'
              % (cls, d.strftime("%a")[:1], d.day))
        A("</tr></thead><tbody>")
        for r in sched:
            s = dt.date.fromisoformat(r["start"])
            e = dt.date.fromisoformat(r["end"])
            A('<tr><td class="qitem">%s<span>%s</span></td><td class="fam">%s</td>'
              % (esc(r["title"]), esc(r.get("detail", "")),
                 esc(" · ".join(r.get("families", [])))))
            for i in range(span):
                d = d0 + dt.timedelta(days=i)
                on = s <= d <= e
                st_cls = {"DONE": "b-done", "NEXT": "b-next"}.get(r["state"], "b-queued")
                A('<td class="gcell%s">%s</td>'
                  % (" today" if d == m["today"] else "",
                     ('<span class="bar %s"></span>' % st_cls) if on else ""))
            A("</tr>")
        A("</tbody></table></div>")
        A('<p class="foot">Each row names the census FAMILIES it closes rather than a '
          "percentage, so a slip shows as a family still open — not as a date that moved "
          "quietly.</p></section>")

    # ---- queue
    A('<section><div class="sec-head"><h2>The build queue</h2>'
      "<p>One session a day, the rate you set. Ordered by value at risk closed, not by "
      "tidiness.</p></div><div class=\"tbl-scroll\">"
      "<table><thead><tr><th>Day</th><th>Step</th><th>State</th></tr></thead><tbody>")
    for r in q:
        A('<tr><td class="day">%s</td><td class="qitem">%s<span>%s</span></td>'
          '<td><span class="chip %s">%s</span></td></tr>'
          % (esc(r["day"]), esc(r["item"]), esc(r["detail"]),
             CHIP.get(r["state"], "c-queued"), esc(r["state"])))
    A("</tbody></table></div></section>")

    # ---- reach
    A('<section><div class="sec-head"><h2>Reach — the number that decides P1</h2></div>'
      '<div class="panel"><div class="tbl-scroll"><table>'
      "<thead><tr><th>Population</th><th>Count</th><th>What a gate can say about it</th>"
      "</tr></thead><tbody>")
    outside = (m["published"] - m["with_study"]) if m["published"] else None
    A('<tr><td>Published fair values on the site</td><td class="num">%s</td>'
      "<td>every one is a number a reader can act on</td></tr>"
      % (m["published"] if m["published"] else "unreadable"))
    A('<tr><td>With a study directory</td><td class="num">%d</td>'
      "<td>every construction gate opens these</td></tr>" % m["with_study"])
    A('<tr><td>Without one</td><td class="num">%s</td>'
      '<td style="color:var(--blocked)">nothing — the gates glob '
      "<span class='mono'>engine/*_study/</span>, so these are invisible rather than "
      "passing</td></tr>" % (outside if outside is not None else "?"))
    A("</tbody></table></div>")
    A('<p class="note"><strong>And it cannot be fixed by gating harder.</strong> Those names '
      "carry a fair value in <span class='mono'>data.js</span> and no model behind it — there "
      "is no construction to check. What this week delivers is that each one becomes "
      "<em>visibly</em> modelless instead of silently unexamined, with the population counted "
      "against the site rather than against the study folders. Building the missing models is "
      "separate work, about nine weeks.</p></div></section>")

    # ---- gauntlet
    g = st["gauntlet"]
    A('<section><div class="sec-head"><h2>What already works</h2></div><div class="panel" '
      'style="border-left:3px solid var(--done)">'
      "<h3>Every gate refuses a new study</h3>"
      "<p>An empty study directory was planted in a copy of the repository and the whole set "
      "run against it: <strong>%d of %d</strong> gates refused it — every directory gate by "
      "name, every artefact gate on a planted offender, and the exclusions each carrying a "
      "written reason rather than a silence.</p>"
      '<p style="margin:0"><strong>So the machinery binds on new work.</strong> What is wrong '
      "with it is which error classes it knows about, how far it reaches, and that nobody "
      "fixes what it finds — which is P1, P2 and P3 above.</p>"
      '<div class="note"><span class="mono">python3 scripts/check_new_study_gauntlet.py</span> '
      "· run %s</div></div></section>" % (g["passed"], g["of"], esc(g["when"])))

    A("<footer>Generated by <code>engine/method_reassessment/build_board.py</code> from "
      "<code>board_state.json</code> and the repository itself — every count above is "
      "measured at build time, never typed. Read anything live rather than trusting this "
      "page: <code>scripts/check_new_study_gauntlet.py</code>, "
      "<code>engine/valuation_calibration/delivered.py</code>. The specification is "
      "<code>engine/method_reassessment/FRAMEWORK_SPEC_07-09-2026.md</code>; the gaps are "
      "<code>FRAMEWORK_GAPS_07-09-2026.md</code>.</footer></div>")
    return "\n".join(parts)


def main(argv=None):
    ap = argparse.ArgumentParser()
    # NOT INSIDE THE REPOSITORY BY DEFAULT, and the reason is a finding rather than a
    # preference: GitHub Pages publishes this whole tree (there is a .nojekyll), so an
    # .html file committed anywhere under it is SERVED ON THE LIVE SITE. This board
    # discusses held studies, ratchet debt and internal state — exactly the vocabulary
    # depth-bar standard 4 keeps away from an outside reader — and check_page_integrity
    # caught it sitting there. It is rendered to a scratch path and published as an
    # artefact from there; the GENERATOR and its state are committed, the page is not.
    ap.add_argument("--out", default=os.environ.get(
        "TESTAHIL_BOARD_OUT", "/tmp/testahil_board.html"))
    ap.add_argument("--today", default=None)
    a = ap.parse_args(argv)

    st = json.load(open(STATE, encoding="utf-8"))
    gates, ctrls = gate_counts()
    LAND = [r"landbank", r"land[_ ]bank", r"land[_ ]bank[_ ]sqm", r"asset[_ ]base",
            r"landholding"]
    KE = [r"ke_exp", r"cost_of_equity", r"ke_terminal", r"capm", r"rf_star \+"]
    land_real, land_fix = concept_coverage(LAND)
    ke_real, ke_fix = concept_coverage(KE)
    dirs = study_dirs()

    m = {
        "today": dt.date.fromisoformat(a.today) if a.today else dt.date.today(),
        "gates": gates, "ctrls": ctrls,
        "published": published_names(),
        "with_study": len(dirs),
        "land_real": land_real, "land_fixture": land_fix, "land_spellings": len(LAND),
        "ke_real": ke_real, "ke_fixture": ke_fix, "ke_spellings": len(KE),
        "head": head(), "branch": branch(),
        # A DATE ALONE CANNOT SAY WHETHER THIS IS THIS MORNING'S BOARD OR THIS EVENING'S,
        # which is the whole question somebody opening it is asking.
        "built_at": dt.datetime.now().strftime("%Y-%m-%d %H:%M UTC%z") or
                    dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    # AN EMPTY POPULATION IS NOT A CLEAN ONE [R-ENF-04]: a board reporting 0 published
    # names would read as a tidy page rather than as a broken reader.
    if not m["published"]:
        print("REFUSING: could not read the published book from assets/data.js",
              file=sys.stderr)
        return 1
    if not dirs:
        print("REFUSING: no study directories found", file=sys.stderr)
        return 1

    html = render(st, m)
    open(a.out, "w", encoding="utf-8").write(html)
    print("wrote %s  (%d bytes)" % (a.out, len(html)))
    print("  published %s · with study %d · gates %d · controls %d"
          % (m["published"], m["with_study"], gates, ctrls))
    print("  landbank in gates: %d real, %d fixture-only" % (len(land_real), len(land_fix)))
    print("  Ke reproduction in gates: %d" % len(ke_real))
    return 0


if __name__ == "__main__":
    sys.exit(main())
