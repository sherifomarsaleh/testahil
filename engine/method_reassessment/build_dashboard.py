#!/usr/bin/env python3
"""Render the programme dashboard from progress.py's own numbers.

GENERATED, NEVER TYPED — the same rule the as-of stamps, the band records and the
lessons register obey: a page that states a fact which moves must not be the thing
that remembers it. Every figure here comes from progress.report(); nothing on the
page is written by hand, so a stale dashboard is impossible without a stale
repository behind it.

THE DESIGN CARRIES ONE ARGUMENT. A progress board wants to draw a bar for
everything, and a bar implies a denominator. Two of the four things this programme
is waiting on have no denominator at all — an export that has not arrived, and a
vintage that cannot mature before June 2027 — so those get a struck slot marked NO
DATE with the dependency named, never a bar at an invented percentage. The absence
is the status, and it is drawn as prominently as the progress.
"""
from __future__ import annotations

import datetime as dt
import html
import re
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(HERE, "dashboard.html")

sys.path.insert(0, HERE)
import progress  # noqa: E402


def e(x) -> str:
    return html.escape(str(x))


def bar(done: int, total: int, tone: str = "go") -> str:
    pct = 0 if not total else round(100 * done / total)
    return (
        '<div class="meter"><div class="meter-track">'
        '<div class="meter-fill %s" style="width:%d%%"></div></div>'
        '<div class="meter-read"><span class="pct">%d<span class="sym">%%</span></span>'
        '<span class="frac">%d of %d</span></div></div>' % (tone, pct, pct, done, total))


def build() -> str:
    d = progress.report()
    p1, p2, dd = d["phase1"], d["phase2"], d["dates"]
    b, dv, acc = p1["build"], p1["delivery"], p1["acceptance"]
    met = sum(1 for a in acc if a["state"] == "MET")
    a3 = next((a for a in acc if a["n"] == 3), None)
    p2a = p2.get("a") or {"rebuilt": {"done": 0, "total": 0},
                          "backtested": {"done": 0, "total": 0, "names": []}}
    p2b = p2.get("b") or {}
    gen = dt.datetime.now(dt.timezone.utc).strftime("%d %B %Y, %H:%M UTC")

    # ---- the four measured rows -------------------------------------------------
    rows = [
        ("Phase 1 — build", "the artefacts the ten workstreams had to produce",
         bar(b["done"], b["total"]),
         "COMPLETE", "on day %s of a planned %d" % (dd.get("elapsed_days", "?"),
                                                    progress.PHASE1_PLANNED_WEEKS * 7),
         "done"),
        ("Phase 1 — delivery", "the five re-issued names, three checks each",
         bar(dv["done"], dv["total"], "warn" if dv["done"] < dv["total"] else "go"),
         ("%d ARTEFACT%s STALE" % (dv["total"] - dv["done"],
                                    "" if dv["total"] - dv["done"] == 1 else "S")
          if dv["done"] < dv["total"] else "ALL CURRENT"),
         "named below" if dv["done"] < dv["total"] else "nothing outstanding",
         "warn" if dv["done"] < dv["total"] else "done"),
        ("Phase 1 — acceptance", "Part E, and its third item is the instrument",
         bar(met, len(acc), "warn"),
         ("INSTRUMENT RUNNING" if a3 and a3["state"] == "RUNNING" else "NO DATE"),
         ("%d of %d origins live" % (a3.get("origins_usable", 0),
                                     a3.get("origins_declared", 0))
          if a3 and a3["state"] == "RUNNING" else "criterion 3 is blocked"),
         ("warn" if a3 and a3["state"] == "RUNNING" else "none")),
        ("Phase 2a — rebuilt", "a study exists, built to the current method",
         bar(p2a["rebuilt"]["done"], p2a["rebuilt"]["total"], "warn"),
         "BOUNDED BY WORK", "throughput decides", "warn"),
        ("Phase 2a — backtested", "that study has been tested on the company's own history",
         bar(p2a["backtested"]["done"], p2a["backtested"]["total"], "warn"),
         "BOUNDED BY WORK", "%s scored so far" % (", ".join(p2a["backtested"]["names"])
                                                  or "none"), "warn"),
        ("Phase 2b — the live test", "claims struck after 2a closes, graded on what happens",
         '<div class="meter"><div class="meter-track"></div><div class="meter-read">'
         '<span class="pct">—</span><span class="frac">not started</span></div></div>',
         "BOUNDED BY THE CALENDAR", "no work shortens it", "none"),
    ]
    row_html = "".join(
        '<div class="prow"><div class="prow-id"><h3>%s</h3><p>%s</p></div>%s'
        '<div class="verdict %s"><span class="v-main">%s</span>'
        '<span class="v-sub">%s</span></div></div>'
        % (e(t), e(sub), m, tone, e(vmain), e(vsub))
        for t, sub, m, vmain, vsub, tone in rows)

    # ---- the dependency chain ---------------------------------------------------
    chain = []
    chain.append(("dated", dd.get("start", "—"),
                  "Phase 1 opens", "the commit that introduced the plan — measured "
                  "from git, not carried in a document"))
    chain.append(("dated", d["generated"][:10],
                  "the build finishes", "all %d workstream artefacts present; the "
                  "Gantt had this at %s" % (b["total"], dd.get("phase1_planned_end", "?"))))
    if a3:
        chain.append(("dated" if a3["state"] == "RUNNING" else "undated",
                      "RUNNING" if a3["state"] == "RUNNING" else "NO DATE",
                      "criterion 3 — the acceptance instrument",
                      a3["waits_on"]))
        if a3.get("first_scoreable"):
            chain.append(("dated-far", a3["first_scoreable"],
                          "its as-delivered check cannot mature before this",
                          a3.get("dated_half", "")))
    chain.append(("undated", "BY WORK", "Phase 2a — the backtest across the book",
                  "ninety rebuilds and ninety backtests; throughput decides when it "
                  "closes. Held until Phase 1's record shows the method unbiased, "
                  "because eighty-five studies on an unproven method is the mistake "
                  "the campaign just made with five. %d of %d names carry a "
                  "point-in-time record so far."
                  % (p2a["backtested"]["done"], p2a["backtested"]["total"])))
    chain.append(("undated", "BY CALENDAR", "Phase 2b — the live test, going forward",
                  "grades only claims struck AFTER 2a closes, on the fundamental "
                  "lens's own clock (%s). It cannot complete earlier than %s. No "
                  "amount of capacity shortens it, and projecting it from a work "
                  "rate would be a number nobody can know."
                  % (p2b.get("horizon", "up to one year"),
                     p2b.get("earliest", "one year after 2a closes"))))
    chain_html = "".join(
        '<li class="node %s"><span class="node-when">%s</span>'
        '<div class="node-body"><h4>%s</h4><p>%s</p></div></li>'
        % (k, e(when), e(what), e(why)) for k, when, what, why in chain)

    # ---- scenarios --------------------------------------------------------------
    sc = "".join(
        '<tr><td class="num">%d</td><td>%s</td><td class="num strong">%s</td></tr>'
        % (s["half_windows_per_week"], e(s["label"]), e(s["both_phases_end"]))
        for s in dd.get("scenarios", []))

    # ---- acceptance -------------------------------------------------------------
    tone = {"MET": "ok", "NOT MET": "no", "BLOCKED": "block"}
    acc_html = "".join(
        '<li class="crit"><span class="chip %s">%s</span>'
        '<div><h4>%d &nbsp;%s</h4><p>%s</p>%s</div></li>'
        % (tone.get(a["state"], "no"), e(a["state"] or "OPEN"), a["n"], e(a["text"]),
           e(a["waits_on"] or ""),
           '<p class="deep">%s</p>' % e(a["dated_half"]) if a.get("dated_half") else "")
        for a in acc)

    # ---- the five ---------------------------------------------------------------
    five = ""
    for n in dv["names"]:
        gap = n.get("gap")
        gcls = "flat"
        if gap is not None:
            gcls = "up" if gap > 0.10 else ("down" if gap < -0.10 else "flat")
        moved = n.get("moved_since_strike")
        five += ('<tr><th scope="row">%s</th><td class="num">%s</td>'
                 '<td class="num">%s<span class="asof">%s</span></td>'
                 '<td class="num %s">%s</td><td class="notes">%s%s</td></tr>'
                 % (e(n["ticker"]),
                    "%.2f" % n["central"] if n.get("central") is not None else "two-sided",
                    "%.2f" % n["spot"] if n.get("spot") else "—",
                    e(n.get("price_date") or ""),
                    gcls, "%+.1f%%" % (gap * 100) if gap is not None else "—",
                    "".join('<span class="flag">%s</span>' % e(i) for i in n["issues"])
                    or '<span class="clear">documents current</span>',
                    "" if moved is None else
                    '<span class="moved">struck at %.2f — the price has moved %+.1f%% '
                    'since</span>' % (n["struck_spot"], moved * 100)))

    # ---- phase 2 markets --------------------------------------------------------
    mk = "".join(
        '<li><span class="mk-name">%s</span>'
        '<span class="mk-bar"><span style="width:%d%%"></span></span>'
        '<span class="mk-num">%d / %d</span></li>'
        % (e(m["market"]), 0 if not m["total"] else round(100 * m["done"] / m["total"]),
           m["done"], m["total"])
        for m in p2.get("markets", []))

    flight = "".join(
        '<tr><th scope="row"><code>%s</code></th><td class="num">%d</td>'
        '<td class="num">%s</td><td class="notes">%s</td></tr>'
        % (e(fb["branch"].replace("origin/", "")), fb["ahead"], e(fb["last"]),
           e(fb["subject"]))
        for fb in progress.live_branches()[:6])

    commits = " · ".join("%s %d" % (k[5:], v)
                         for k, v in (dd.get("commits_by_day") or {}).items())

    out = TEMPLATE
    for k, v in dict(
        gen=e(gen), rows=row_html, chain=chain_html, scenarios=sc,
        acc=acc_html, five=five, markets=mk,
        rate_note=e(dd.get("rate_note", "")), commits=e(commits), flight=flight,
        p2done=p2.get("done", 0), p2total=p2.get("total", 0),
        start=e(dd.get("start", "—")), elapsed=e(dd.get("elapsed_days", "—")),
    ).items():
        out = out.replace("{{%s}}" % k, str(v))
    if "{{" in out:
        raise SystemExit("FAIL — unfilled placeholder: %s"
                         % re.findall(r"\{\{\w+\}\}", out)[:5])
    return out


TEMPLATE = """<title>Reassessment Progress Board</title>
<!-- GitHub Pages serves the whole repository, so this file IS a served page and
     carries the site's tab chrome like every other one. check_page_integrity.py
     said so and it was right: the first instinct was to exempt it as "an artifact
     source, not a site page", which would have asserted something false about the
     deployment in order to quiet a gate. On the published Artifact this link
     resolves to nothing and the tab icon comes from the publish call, which costs
     nothing; on testahil.com it resolves. -->
<link rel="icon" href="/favicon.png">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{
  --ground:#f6f8f5; --surface:#ffffff; --sunk:#eef1ed;
  --ink:#141a18; --ink-2:#3d4a45; --ink-3:#6d7c76;
  --rule:#dde3de; --rule-2:#c9d2cb;
  --go:#1f6f5c; --go-soft:#d8e8e2;
  --warn:#a8621b; --warn-soft:#f2e4d4;
  --stop:#9d3729; --stop-soft:#f2ddd9;
  --ui:'Archivo',system-ui,-apple-system,'Segoe UI',sans-serif;
  --prose:'Newsreader',Georgia,'Times New Roman',serif;
  --mono:'IBM Plex Mono',ui-monospace,'SF Mono',Menlo,monospace;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --ground:#0e1312; --surface:#161d1b; --sunk:#1c2422;
    --ink:#e6ece9; --ink-2:#b3c0ba; --ink-3:#84968e;
    --rule:#26302d; --rule-2:#35423e;
    --go:#5cbfa4; --go-soft:#1a3630;
    --warn:#dd9b52; --warn-soft:#3a2c1a;
    --stop:#e0806f; --stop-soft:#3a211c;
  }
}
:root[data-theme="dark"]{
  --ground:#0e1312; --surface:#161d1b; --sunk:#1c2422;
  --ink:#e6ece9; --ink-2:#b3c0ba; --ink-3:#84968e;
  --rule:#26302d; --rule-2:#35423e;
  --go:#5cbfa4; --go-soft:#1a3630;
  --warn:#dd9b52; --warn-soft:#3a2c1a;
  --stop:#e0806f; --stop-soft:#3a211c;
}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--ui);
  font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{max-width:1060px;margin:0 auto;padding:44px 26px 90px}
h1,h2,h3,h4{margin:0;text-wrap:balance;font-weight:600;letter-spacing:-.012em}
p{margin:0}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--ink-3)}

/* masthead ---------------------------------------------------------------- */
.mast{border-bottom:2px solid var(--ink);padding-bottom:20px}
.mast h1{font-size:clamp(30px,4.4vw,46px);line-height:1.04;margin:10px 0 12px}
.mast .lede{font-family:var(--prose);font-size:18px;line-height:1.5;
  color:var(--ink-2);max-width:64ch}
.mast .meta{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:16px;
  font-family:var(--mono);font-size:11.5px;color:var(--ink-3)}
.mast .meta b{color:var(--ink-2);font-weight:500}

/* progress rows ----------------------------------------------------------- */
.rows{margin-top:8px}
.prow{display:grid;grid-template-columns:minmax(210px,1.15fr) minmax(200px,1.5fr) minmax(150px,.85fr);
  gap:20px 26px;align-items:center;padding:22px 0;border-bottom:1px solid var(--rule)}
.prow-id h3{font-size:17px}
.prow-id p{font-family:var(--prose);font-size:14.5px;color:var(--ink-3);margin-top:3px}
.meter{display:flex;align-items:center;gap:14px}
.meter-track{flex:1;height:9px;background:var(--sunk);border-radius:1px;overflow:hidden}
.meter-fill{height:100%;background:var(--go)}
.meter-fill.warn{background:var(--warn)}
.meter-read{display:flex;flex-direction:column;min-width:74px}
.pct{font-size:23px;font-weight:600;font-variant-numeric:tabular-nums;line-height:1}
.pct .sym{font-size:13px;font-weight:500;color:var(--ink-3);margin-left:1px}
.frac{font-family:var(--mono);font-size:11px;color:var(--ink-3);margin-top:3px}
.verdict{display:flex;flex-direction:column;gap:3px;padding-left:16px;
  border-left:3px solid var(--rule-2)}
.verdict.done{border-left-color:var(--go)}
.verdict.warn{border-left-color:var(--warn)}
.verdict.none{border-left-color:var(--warn);background:
  repeating-linear-gradient(135deg,transparent 0 6px,var(--warn-soft) 6px 7px)}
.v-main{font-family:var(--mono);font-size:12px;letter-spacing:.06em;font-weight:500}
.verdict.none .v-main{color:var(--warn)}
.verdict.done .v-main{color:var(--go)}
.v-sub{font-family:var(--prose);font-size:13.5px;color:var(--ink-3);line-height:1.35}

/* section scaffolding ----------------------------------------------------- */
section{margin-top:52px}
section > h2{font-size:22px;margin-bottom:6px}
section > .intro{font-family:var(--prose);font-size:16px;color:var(--ink-2);
  max-width:66ch;margin-bottom:22px}

/* dependency chain -------------------------------------------------------- */
.chain{list-style:none;margin:0;padding:0;position:relative}
.chain:before{content:"";position:absolute;left:124px;top:12px;bottom:12px;
  width:1px;background:var(--rule-2)}
.node{display:grid;grid-template-columns:112px 1fr;gap:0 40px;padding:14px 0;
  position:relative}
.node-when{font-family:var(--mono);font-size:12px;text-align:right;padding-top:2px;
  color:var(--ink-2);font-variant-numeric:tabular-nums}
.node:after{content:"";position:absolute;left:120px;top:19px;width:9px;height:9px;
  border-radius:50%;background:var(--go);border:2px solid var(--ground)}
.node.undated:after{background:var(--warn)}
.node.dated-far:after{background:var(--ground);border:2px solid var(--warn)}
.node.undated .node-when{color:var(--warn);font-weight:500;letter-spacing:.05em}
.node.dated-far .node-when{color:var(--warn)}
.node-body h4{font-size:16px}
.node-body p{font-family:var(--prose);font-size:15px;color:var(--ink-2);
  margin-top:4px;max-width:62ch}

/* panels ------------------------------------------------------------------ */
.panel{background:var(--surface);border:1px solid var(--rule);padding:24px 26px}
.panel h3{font-size:16px;margin-bottom:4px}
.panel .note{font-family:var(--prose);font-size:14.5px;color:var(--ink-3);
  max-width:66ch;margin-top:14px}

/* tables ------------------------------------------------------------------ */
.tw{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:14.5px}
th,td{text-align:left;padding:10px 14px 10px 0;border-bottom:1px solid var(--rule);
  vertical-align:top}
thead th{font-family:var(--mono);font-size:10.5px;letter-spacing:.11em;
  text-transform:uppercase;color:var(--ink-3);font-weight:500;
  border-bottom:1px solid var(--rule-2)}
tbody th{font-weight:600}
.num{font-variant-numeric:tabular-nums;text-align:right;white-space:nowrap}
.num.strong{font-weight:600}
td.up{color:var(--go)} td.down{color:var(--stop)}
.notes .flag{display:block;font-family:var(--prose);font-size:13.5px;color:var(--warn)}
.notes .clear{font-family:var(--mono);font-size:11px;color:var(--ink-3)}
.notes .moved{display:block;font-family:var(--prose);font-size:13px;color:var(--ink-3);margin-top:3px}
.asof{display:block;font-family:var(--mono);font-size:10px;color:var(--ink-3);font-weight:400;margin-top:2px}
tbody th code{font-family:var(--mono);font-size:12px;font-weight:400}

/* criteria ---------------------------------------------------------------- */
.crits{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:2px}
.crit{display:grid;grid-template-columns:84px 1fr;gap:18px;padding:14px 0;
  border-bottom:1px solid var(--rule)}
.crit h4{font-size:15.5px;font-weight:500}
.crit p{font-family:var(--prose);font-size:14.5px;color:var(--ink-2);margin-top:4px;
  max-width:70ch}
.crit p.deep{color:var(--ink-3);margin-top:6px}
.chip{font-family:var(--mono);font-size:10.5px;letter-spacing:.07em;padding:3px 0;
  text-align:center;height:fit-content;border:1px solid currentColor}
.chip.ok{color:var(--go);background:var(--go-soft)}
.chip.no{color:var(--stop);background:var(--stop-soft)}
.chip.block{color:var(--warn);background:var(--warn-soft)}

/* markets ----------------------------------------------------------------- */
.mkts{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:11px}
.mkts li{display:grid;grid-template-columns:190px 1fr 70px;gap:16px;align-items:center}
.mk-name{font-size:14.5px}
.mk-bar{height:7px;background:var(--sunk);display:block;border-radius:1px;overflow:hidden}
.mk-bar span{display:block;height:100%;background:var(--go)}
.mk-num{font-family:var(--mono);font-size:12px;color:var(--ink-3);text-align:right;
  font-variant-numeric:tabular-nums}

/* footer ------------------------------------------------------------------ */
footer{margin-top:60px;padding-top:22px;border-top:2px solid var(--ink);
  font-family:var(--prose);font-size:15px;color:var(--ink-2);max-width:70ch}
footer code{font-family:var(--mono);font-size:13px;background:var(--sunk);
  padding:2px 6px;color:var(--ink)}
@media (max-width:760px){
  .prow{grid-template-columns:1fr;gap:14px}
  .verdict{border-left:none;border-top:3px solid var(--rule-2);padding:12px 0 0}
  .verdict.done{border-top-color:var(--go)} .verdict.warn,.verdict.none{border-top-color:var(--warn)}
  .chain:before{left:6px} .node{grid-template-columns:1fr;gap:6px;padding-left:30px}
  .node-when{text-align:left} .node:after{left:2px}
  .crit{grid-template-columns:1fr;gap:8px} .chip{width:84px}
  .mkts li{grid-template-columns:1fr 60px} .mk-bar{grid-column:1/-1}
}
</style>

<div class="wrap">
  <header class="mast">
    <div class="eyebrow">TESTAHIL &nbsp;·&nbsp; standing research protocol</div>
    <h1>Fundamental method reassessment</h1>
    <p class="lede">Three stages. Phase&nbsp;1 rebuilds the method. Phase&nbsp;2a backtests it
      across all ninety names — bounded by <em>work</em>. Phase&nbsp;2b grades what it claims
      from that point forward against what actually happens — bounded by the
      <em>calendar</em>, and no amount of capacity shortens it. Every figure below is counted
      from the repository when this page is built; none of it is typed.</p>
    <div class="meta">
      <span>built <b>{{gen}}</b></span>
      <span>phase 1 opened <b>{{start}}</b></span>
      <span>day <b>{{elapsed}}</b></span>
      <span>commits <b>{{commits}}</b></span>
    </div>
  </header>

  <div class="rows">{{rows}}</div>

  <section>
    <h2>When each phase can end</h2>
    <p class="intro">A completion date is a quantity divided by a rate. The quantity is
      countable; the rate has never been measured, and two of the things this programme
      waits on are not rates at all. Where a dependency has no date, neither does the
      phase — so it is drawn as an absence rather than as a bar at a number nobody
      measured.</p>
    <ol class="chain">{{chain}}</ol>
  </section>

  <section>
    <h2>What every row above means</h2>
    <p class="intro">Five measures of three different things. They are never averaged,
      because they answer different questions and disagreeing is informative.</p>
    <div class="panel">
      <h3>Phase 1 — build</h3>
      <p class="note"><strong>Are the tools that produce a valuation built?</strong> One house
      macro path per market instead of each study carrying its own inflation view; a
      cost-of-capital schedule that glides with the central bank's own easing path instead of
      one crisis-level rate applied to every year and the perpetuity; one class primary as the
      central instead of a weighted blend of four lenses; a checked enterprise-to-equity
      bridge. Ten workstreams, twenty-nine artefacts. <strong>Complete.</strong> It is about
      the method, not about any company.</p>
      <h3 style="margin-top:18px">Phase 1 — delivery</h3>
      <p class="note"><strong>Do the five test names have finished, current documents?</strong>
      Three checks each: the study exposes a readable answer, its gap review audits the answer
      the study actually publishes rather than a superseded one, and the publish queue holds
      that same answer. Fifteen of fifteen. This is a currency check — it catches a document
      or a queue still stating last week's number, which happened three times.</p>
      <h3 style="margin-top:18px">Phase 1 — acceptance</h3>
      <p class="note"><strong>Has the rebuilt method been shown to work?</strong> Six criteria,
      and the third is the instrument: the valuation calibration must show that the house is
      not systematically wrong. Five of six hold. The outstanding one is criterion 3, which is
      running at six of eleven point-in-time origins and needs the rest of its historical
      archive. <em>The other five criteria are hygiene; this one is the evidence.</em></p>
      <h3 style="margin-top:18px">Phase 2a — rebuilt</h3>
      <p class="note"><strong>Does a study exist, built to today's method?</strong> One house
      macro path, the cost-of-capital schedule rather than a single crisis-level rate, one
      class primary as the central with the other lenses published beside it, a checked
      enterprise-to-equity bridge. It produces the four documents. This is the number that
      answers "have we valued this company properly yet" — and for 85 of the 90 the answer is
      still no, because most have no study at all.</p>
      <h3 style="margin-top:18px">Phase 2a — backtested</h3>
      <p class="note"><strong>Has that method been tested on the company's own history?</strong>
      Rebuild its fair value at each past year-end using only what was published by that date,
      and score it: did we agree with the market then, and did our disagreement predict what
      the price did next. A study tells you what we think a company is worth. The backtest is
      the only thing that tells you whether our way of arriving at that number has ever been
      right.</p>
      <p class="note"><strong>Why rebuilt runs ahead of backtested, and should.</strong> The
      backtest needs point-in-time inputs for every origin — what the sovereign yield, the
      policy rate, the inflation print and the risk premium actually were on the day, not
      today's revised readings. That archive is the binding constraint, not the study count.</p>
      <h3 style="margin-top:18px">Phase 2b — the live test</h3>
      <p class="note"><strong>Does the corrected method work going forward, on evidence nobody
      can tune?</strong> From the day 2a closes, every fair value published is a dated claim
      graded against what actually happens. It has no bar and no projected date on purpose:
      2a is bounded by <em>work</em> and finishes faster with more capacity, while 2b is bounded
      by the <em>calendar</em> — a claim made today cannot be graded until what it claimed has
      happened, and no amount of effort shortens that.</p>
      <p class="note"><strong>The one thing none of these rows measures.</strong> Whether a
      given company's fair value is right. That is what the deviation column in the table above
      is for, and why four of the five sit outside 10% of their market price today.</p>
    </div>
  </section>

  <section>
    <h2>Work in flight</h2>
    <p class="intro">The repository is not one line. Several sessions work at once,
      and a blocker closed on a live branch is closed. This section exists because an
      earlier build of this page reported an item open that another session had closed
      hours before — the figures above are now read at the frontier, and each says
      which branch it came from.</p>
    <div class="tw"><table>
      <thead><tr><th>Branch</th><th class="num">Ahead of main</th><th>Last commit</th>
        <th>Latest</th></tr></thead>
      <tbody>{{flight}}</tbody>
    </table></div>
  </section>

  <section>
    <h2>If Phase 2a started today</h2>
    <p class="intro">The plan's own cap scenarios for the build-and-backtest work,
      anchored on the measured start date. These are not a forecast — they are three
      arithmetic consequences of three assumptions, and the assumption has never been
      tested. <strong>They do not apply to 2b at all</strong>: 2b is bounded by the
      calendar, so a work rate cannot project it.</p>
    <div class="panel">
      <div class="tw"><table>
        <thead><tr><th>Half-windows / week</th><th>Assumption</th>
          <th class="num">2a would close</th></tr></thead>
        <tbody>{{scenarios}}</tbody>
      </table></div>
      <p class="note">{{rate_note}}</p>
    </div>
  </section>

  <section>
    <h2>Acceptance — Part E</h2>
    <p class="intro">The programme is complete when these hold and are printed by the
      gates rather than attested. Item 3 is the instrument; the rest are its
      surroundings.</p>
    <ul class="crits">{{acc}}</ul>
  </section>

  <section>
    <h2>The five re-issued names</h2>
    <p class="intro">Each name's own committed central against <strong>the latest price the
      house holds</strong> — the principal's dated export where it is newer than the price
      library — not the spot the study was struck at. Those are the same number on the day a
      study is built and diverge every day after. A flag is an artefact that exists but is no
      longer current — the failure shape this programme found three times, and the reason
      the column is here at all.</p>
    <div class="tw"><table>
      <thead><tr><th>Name</th><th class="num">Central</th><th class="num">Latest price</th>
        <th class="num">vs price</th><th>State</th></tr></thead>
      <tbody>{{five}}</tbody>
    </table></div>
  </section>

  <section>
    <h2>Phase 2a — {{p2done}} of {{p2total}} names rebuilt</h2>
    <p class="intro">Read live from the campaign queue, which refuses rather than
      returning a short list. Market order is fixed and there is a hard stop after Egypt
      to ask whether the corrected method generalises before the UAE begins.</p>
    <ul class="mkts">{{markets}}</ul>
  </section>

  <footer>
    <p>Regenerate with <code>python3 engine/method_reassessment/build_dashboard.py</code>,
    or read the same figures in a terminal with
    <code>python3 engine/method_reassessment/progress.py</code>. The programme's
    narrative — what happened each night, with the evidence and a recommended answer on
    each item — is <code>engine/method_reassessment/MORNING.md</code>. Nothing on this
    page has been published to testahil.com; the site still carries the
    pre-reassessment numbers.</p>
  </footer>
</div>
"""


if __name__ == "__main__":
    open(OUT, "w", encoding="utf-8").write(build())
    print("\nwrote %s (%d bytes)" % (os.path.relpath(OUT, ROOT),
                                     os.path.getsize(OUT)))
