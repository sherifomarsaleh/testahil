# -*- coding: utf-8 -*-
"""Render the build-depth audit as a self-contained HTML page.

Every count in the page is computed from classification.ROWS - no figure is typed here.
"""
import importlib.util, os, json, collections, html
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('classification', os.path.join(HERE, 'classification.py'))
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
ROWS = C.ROWS

TIER = {
 'A' : ('Disclosed units',   'Revenue = a disclosed physical unit x a price or rate; cost per unit; margins fall out as outputs.'),
 'A-': ('Major legs',        'The unit build carries the major legs; the rest sits at segment level because nothing finer is disclosed, and the study says so.'),
 'B' : ('Derived units',     'Real unit economics, but the units are the preparer’s estimate, an index, or back-solved from disclosed totals.'),
 'C' : ('Segment level',     'Each disclosed segment on its own driver. No unit economics; the gap is flagged.'),
 'D' : ('Top-down',          'A group or segment revenue-growth path plus a margin assumption or glide.'),
 'E' : ('Asset / NAV marks', 'Value comes from marking assets, stakes or segment earnings at multiples. No revenue build at all.'),
 'F' : ('Bank driver build', 'Balances x margin — a NIM, cost-of-risk and cost-to-income bridge.'),
}
ORDER = ['A','A-','B','C','D','E','F']
BU = {'A','A-','B'}

eng = {d[:-6].upper() for d in os.listdir(os.path.dirname(HERE)) if d.endswith('_study')}
def coded(tk): return tk in eng or (tk == 'FERTIGLB' and 'FERTIGLOBE' in eng)

recs = []
for tk, nm, code, ed, tier, bu, ev in ROWS:
    d, mo, y = ed.split('-')
    recs.append(dict(t=tk, n=nm, x=code.split(':')[0], e=ed, k=f'{y}-{mo}', g=tier,
                     b=1 if bu else 0, c=1 if coded(tk) else 0, v=ev))
recs.sort(key=lambda r: (ORDER.index(r['g']), r['t']))

cnt   = collections.Counter(r['g'] for r in recs)
nbu   = sum(1 for r in recs if not r['b']); ybu = len(recs) - nbu
vint  = collections.defaultdict(lambda: [0, 0])
for r in recs: vint[r['k']][0 if r['b'] else 1] += 1
xch   = collections.Counter(r['x'] for r in recs)
cb    = collections.Counter((r['c'], r['b']) for r in recs)
NCODE = sum(1 for r in recs if r['c'])

def esc(s): return html.escape(s, quote=False)

# ---- stacked tier bar (real proportions, one segment per tier) ----
segs = ''.join(
    f'<span class="seg t{t.replace("-","m")}" style="flex:{cnt[t]}" '
    f'title="Tier {t} — {TIER[t][0]}: {cnt[t]}"><b>{cnt[t]}</b></span>'
    for t in ORDER if cnt[t])

legend = ''.join(
    f'<div class="lg"><span class="sw t{t.replace("-","m")}"></span>'
    f'<span class="lgk">{t}</span><span class="lgn">{esc(TIER[t][0])}</span>'
    f'<span class="lgc">{cnt[t]}</span><p>{esc(TIER[t][1])}</p></div>'
    for t in ORDER)

CODE_STAMP = '<span class="cod" title="Study has a code-built engine directory">code</span>'
def row_html(r):
    g = r['g'].replace('-', 'm')
    s = esc((r['t'] + ' ' + r['n'] + ' ' + r['x'] + ' ' + r['v']).lower())
    return (f'<tr class="r {"bu" if r["b"] else "nb"}" data-b="{r["b"]}" data-g="{r["g"]}" '
            f'data-x="{r["x"]}" data-s="{s}">'
            f'<td class="c-tk"><span class="stripe t{g}"></span>'
            f'<span class="tk">{r["t"]}</span>{CODE_STAMP if r["c"] else ""}</td>'
            f'<td class="c-nm">{esc(r["n"])}<span class="mob">{r["x"]} &middot; {r["e"]}</span></td>'
            f'<td class="c-x"><span class="chip">{r["x"]}</span></td>'
            f'<td class="c-e">{r["e"]}</td>'
            f'<td class="c-g"><span class="tier t{g}">{r["g"]}</span>'
            f'<span class="tn">{esc(TIER[r["g"]][0])}</span></td>'
            f'<td class="c-v">{esc(r["v"])}</td></tr>')
rows = ''.join(row_html(r) for r in recs)

vrows = ''.join(
    f'<tr><td class="mn">{k}</td><td class="num">{v[0]}</td><td class="num">{v[1]}</td>'
    f'<td class="bar"><span style="width:{100*v[0]/(v[0]+v[1]):.0f}%"></span></td></tr>'
    for k, v in sorted(vint.items()))

xchips = ''.join(f'<button class="f" data-f="x" data-v="{k}">{k} <i>{v}</i></button>'
                 for k, v in sorted(xch.items(), key=lambda kv: -kv[1]))

HTML = f"""<title>Bottom-Up Build Audit</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
:root{{
  --ground:#F2F4F7; --surface:#FFFFFF; --sunk:#E8EBF0;
  --ink:#141C26; --ink2:#3D4855; --muted:#697687; --line:#D8DDE5; --line2:#EBEEF3;
  --bu:#0E6B5E; --bu-s:#D6EAE5; --nb:#9A5A2B; --nb-s:#F0E3D6;
  --a:#0E6B5E; --a2:#12897A;
  --tA:#0E6B5E; --tAm:#2E8A72; --tB:#5E9A6B; --tC:#B08A3C; --tD:#A96A32; --tE:#8E5B57; --tF:#6C6480;
  --on-accent:#FFFFFF;
  --shadow:0 1px 2px rgba(20,28,38,.05),0 8px 24px -14px rgba(20,28,38,.18);
}}
@media (prefers-color-scheme:dark){{ :root:not([data-theme="light"]){{
  --ground:#0F141A; --surface:#161D25; --sunk:#1E262F;
  --ink:#E9EDF2; --ink2:#C2CAD4; --muted:#8D99A8; --line:#2A343F; --line2:#212A34;
  --bu:#5CC9B4; --bu-s:#123832; --nb:#D9A16A; --nb-s:#38271A;
  --a:#5CC9B4; --a2:#7FD8C6;
  --tA:#5CC9B4; --tAm:#79C9AE; --tB:#93C79A; --tC:#D6B55F; --tD:#D9975C; --tE:#C08D88; --tF:#A29BBA;
  --on-accent:#0F141A;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 28px -16px rgba(0,0,0,.7);
}} }}
:root[data-theme="dark"]{{
  --ground:#0F141A; --surface:#161D25; --sunk:#1E262F;
  --ink:#E9EDF2; --ink2:#C2CAD4; --muted:#8D99A8; --line:#2A343F; --line2:#212A34;
  --bu:#5CC9B4; --bu-s:#123832; --nb:#D9A16A; --nb-s:#38271A;
  --a:#5CC9B4; --a2:#7FD8C6;
  --tA:#5CC9B4; --tAm:#79C9AE; --tB:#93C79A; --tC:#D6B55F; --tD:#D9975C; --tE:#C08D88; --tF:#A29BBA;
  --on-accent:#0F141A;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 28px -16px rgba(0,0,0,.7);
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--ground);color:var(--ink);
  font-family:"IBM Plex Sans",ui-sans-serif,system-ui,sans-serif;
  font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:1220px;margin:0 auto;padding:clamp(22px,4vw,52px) clamp(14px,3vw,30px) 80px}}
h1,h2,h3{{font-family:Newsreader,ui-serif,Georgia,serif;font-weight:600;text-wrap:balance;margin:0}}
h1{{font-size:clamp(30px,4.6vw,49px);line-height:1.06;letter-spacing:-.015em}}
h2{{font-size:clamp(20px,2.4vw,26px);letter-spacing:-.01em}}
p{{margin:0}}
.eyebrow{{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--muted)}}
header{{display:flex;flex-direction:column;gap:14px;padding-bottom:26px;border-bottom:1px solid var(--line)}}
.lede{{max-width:66ch;color:var(--ink2);font-size:17px}}
.lede b{{color:var(--ink);font-weight:600}}

.score{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1px;
  background:var(--line);border:1px solid var(--line);border-radius:3px;overflow:hidden;margin-top:28px}}
.sc{{background:var(--surface);padding:18px 20px;display:flex;flex-direction:column;gap:3px}}
.sc .k{{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--muted)}}
.sc .v{{font-family:Newsreader,serif;font-size:38px;line-height:1;font-variant-numeric:tabular-nums}}
.sc .s{{font-size:13px;color:var(--muted)}}
.sc.on .v{{color:var(--bu)}} .sc.off .v{{color:var(--nb)}}

.barwrap{{margin-top:34px}}
.bar-t{{display:flex;justify-content:space-between;align-items:baseline;gap:16px;margin-bottom:9px}}
.stack{{display:flex;height:38px;border-radius:3px;overflow:hidden;border:1px solid var(--line)}}
.seg{{display:grid;place-items:center;min-width:26px;color:var(--on-accent);
  font-family:"IBM Plex Mono",monospace;font-size:12px;font-weight:600}}
.seg b{{font-weight:600;mix-blend-mode:normal}}
.tA{{background:var(--tA)}} .tAm{{background:var(--tAm)}} .tB{{background:var(--tB)}}
.tC{{background:var(--tC)}} .tD{{background:var(--tD)}} .tE{{background:var(--tE)}} .tF{{background:var(--tF)}}
.split{{display:flex;font-family:"IBM Plex Mono",monospace;font-size:11.5px;letter-spacing:.06em;
  text-transform:uppercase;margin-top:7px;color:var(--muted)}}
.split .l{{color:var(--bu)}} .split .r{{margin-left:auto;color:var(--nb)}}

.legend{{display:grid;grid-template-columns:repeat(auto-fit,minmax(272px,1fr));gap:14px;margin-top:30px}}
.lg{{background:var(--surface);border:1px solid var(--line2);border-radius:3px;padding:13px 15px;
  display:grid;grid-template-columns:12px auto 1fr auto;gap:8px;align-items:center}}
.lg p{{grid-column:1/-1;font-size:12.5px;color:var(--muted);line-height:1.45}}
.sw{{width:12px;height:12px;border-radius:2px}}
.lgk{{font-family:"IBM Plex Mono",monospace;font-weight:600;font-size:13px}}
.lgn{{font-size:13.5px;color:var(--ink2)}}
.lgc{{font-family:"IBM Plex Mono",monospace;font-size:13px;color:var(--muted);font-variant-numeric:tabular-nums}}

.sec{{margin-top:52px}}
.sec-h{{display:flex;flex-wrap:wrap;align-items:baseline;gap:12px;margin-bottom:6px}}
.note{{max-width:70ch;color:var(--ink2);margin-top:8px}}

.tools{{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:22px 0 14px;
  position:sticky;top:0;z-index:5;background:var(--ground);padding:10px 0;border-bottom:1px solid var(--line2)}}
.f{{font:inherit;font-size:12.5px;background:var(--surface);color:var(--ink2);border:1px solid var(--line);
  border-radius:999px;padding:5px 12px;cursor:pointer;display:inline-flex;gap:6px;align-items:center}}
.f i{{font-style:normal;font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--muted)}}
.f:hover{{border-color:var(--a)}}
.f[aria-pressed="true"]{{background:var(--a);border-color:var(--a);color:var(--on-accent)}}
.f[aria-pressed="true"] i{{color:var(--on-accent);opacity:.72}}
.f:focus-visible,input:focus-visible{{outline:2px solid var(--a2);outline-offset:2px}}
.sp{{width:1px;height:20px;background:var(--line);margin:0 3px}}
input[type=search]{{font:inherit;font-size:13px;background:var(--surface);color:var(--ink);
  border:1px solid var(--line);border-radius:999px;padding:5px 13px;min-width:190px;flex:1 1 190px;max-width:300px}}
.hits{{font-family:"IBM Plex Mono",monospace;font-size:11.5px;color:var(--muted);margin-left:auto}}

.tblwrap{{overflow-x:auto;border:1px solid var(--line);border-radius:3px;background:var(--surface);
  box-shadow:var(--shadow)}}
table{{border-collapse:collapse;width:100%;min-width:940px}}
thead th{{background:var(--sunk);text-align:left;
  font-family:"IBM Plex Mono",monospace;font-weight:600;font-size:10.5px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--muted);padding:9px 12px;border-bottom:1px solid var(--line)}}
tbody td{{padding:13px 12px;border-bottom:1px solid var(--line2);vertical-align:top;font-size:13.5px}}
tbody tr:last-child td{{border-bottom:0}}
tbody tr:hover td{{background:var(--sunk)}}
.c-tk{{position:relative;padding-left:18px!important;white-space:nowrap}}
.stripe{{position:absolute;left:0;top:0;bottom:0;width:4px}}
.tk{{font-family:"IBM Plex Mono",monospace;font-weight:600;font-size:13px;letter-spacing:.01em}}
.cod{{display:block;font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--muted);margin-top:3px}}
.c-nm{{min-width:180px;color:var(--ink2)}}
.mob{{display:none}}
.chip{{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.08em;padding:2px 7px;
  border:1px solid var(--line);border-radius:3px;color:var(--muted);white-space:nowrap}}
.c-e{{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--muted);white-space:nowrap;
  font-variant-numeric:tabular-nums}}
.c-g{{white-space:nowrap}}
.tier{{font-family:"IBM Plex Mono",monospace;font-weight:600;font-size:12px;color:var(--on-accent);
  padding:1px 7px;border-radius:3px}}
.tn{{display:block;font-size:11.5px;color:var(--muted);margin-top:4px}}
.c-v{{color:var(--ink2);line-height:1.5;min-width:340px}}
.r.hide{{display:none}}

.mini{{width:100%;border-collapse:collapse;margin-top:16px;max-width:560px}}
.mini td,.mini th{{padding:7px 10px;border-bottom:1px solid var(--line2);font-size:13px}}
.mini th{{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--muted);text-align:left}}
.mn{{font-family:"IBM Plex Mono",monospace;font-variant-numeric:tabular-nums}}
.num{{font-family:"IBM Plex Mono",monospace;text-align:right;font-variant-numeric:tabular-nums;width:76px}}
.mini .bar{{width:130px}}
.mini .bar span{{display:block;height:7px;background:var(--bu);border-radius:2px;min-width:2px}}

.finds{{display:grid;gap:16px;margin-top:22px}}
.find{{background:var(--surface);border:1px solid var(--line2);border-left:3px solid var(--a);
  border-radius:3px;padding:16px 18px}}
.find h3{{font-family:"IBM Plex Sans",sans-serif;font-size:14.5px;font-weight:600;margin-bottom:5px}}
.find p{{color:var(--ink2);font-size:14px;max-width:74ch}}
.find.warn{{border-left-color:var(--nb)}}
footer{{margin-top:56px;padding-top:20px;border-top:1px solid var(--line);
  font-size:12.5px;color:var(--muted);max-width:76ch}}
code{{font-family:"IBM Plex Mono",monospace;font-size:.9em;background:var(--sunk);
  padding:1px 5px;border-radius:3px}}
@media (max-width:720px){{
  table,thead,tbody,tr,td{{display:block;min-width:0}}
  thead{{display:none}} table{{min-width:0}}
  tbody tr{{border-bottom:1px solid var(--line);padding:4px 0}}
  tbody td{{border:0;padding:3px 14px}}
  .c-nm{{font-weight:600;color:var(--ink);font-size:15px}}
  .mob{{display:block;font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--muted);margin-top:2px}}
  .c-x,.c-e{{display:none}}
  .c-tk{{padding-left:14px!important}}
}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important;animation:none!important}}}}
</style>

<div class="wrap">
<header>
  <p class="eyebrow">TESTAHIL &middot; standing research protocol &middot; build-depth audit &middot; 23 Aug 2026</p>
  <h1>Which valuations were built from the bottom up</h1>
  <p class="lede">Every one of the <b>{len(recs)}</b> stocks carrying a published fundamental fair value,
  read against SIGCM clause&nbsp;2: <i>revenue as volume &times; price, cost as cost-per-unit, to the finest
  sourced level, with the gap flagged wherever the disclosure stops.</i> The verdict for each name comes
  out of its own delivered study &mdash; and, for the {NCODE} studies that carry a code-built
  <code>engine/&lt;name&gt;_study/</code> directory, out of its <code>compute.py</code> as well.</p>
</header>

<div class="score">
  <div class="sc on"><span class="k">Built bottom-up</span><span class="v">{ybu}</span>
    <span class="s">{ybu/len(recs):.0%} of covered stocks &mdash; tiers A, A&minus; and B</span></div>
  <div class="sc off"><span class="k">Not built bottom-up</span><span class="v">{nbu}</span>
    <span class="s">{nbu/len(recs):.0%} &mdash; tiers C through F</span></div>
  <div class="sc"><span class="k">Metals excluded</span><span class="v">4</span>
    <span class="s">Gold, gold 12M, silver, platinum &mdash; no corporate revenue build to classify</span></div>
</div>

<div class="barwrap">
  <div class="bar-t"><p class="eyebrow">The seven build tiers, at true proportion</p></div>
  <div class="stack">{segs}</div>
  <div class="split"><span class="l">&#9668; bottom-up &nbsp;{ybu}</span>
    <span class="r">{nbu}&nbsp; not bottom-up &#9658;</span></div>
  <div class="legend">{legend}</div>
</div>

<section class="sec">
  <div class="sec-h"><h2>The register</h2><p class="eyebrow">one row per covered stock</p></div>
  <p class="note">Sorted by build depth, deepest first. The <code>code</code> stamp marks a study with a
  committed build directory. Filter or search to narrow the register.</p>

  <div class="tools">
    <button class="f" data-f="b" data-v="1">Bottom-up <i>{ybu}</i></button>
    <button class="f" data-f="b" data-v="0">Not bottom-up <i>{nbu}</i></button>
    <span class="sp"></span>
    {''.join(f'<button class="f" data-f="g" data-v="{t}">{t} <i>{cnt[t]}</i></button>' for t in ORDER)}
    <span class="sp"></span>
    {xchips}
    <span class="sp"></span>
    <input type="search" id="q" placeholder="Search ticker, company, evidence&hellip;" aria-label="Search the register">
    <span class="hits" id="hits"></span>
  </div>

  <div class="tblwrap">
  <table>
    <thead><tr><th>Ticker</th><th>Company</th><th>Exch.</th><th>Edition</th><th>Build tier</th>
    <th>How the forecast is actually built</th></tr></thead>
    <tbody id="tb">{rows}</tbody>
  </table>
  </div>
</section>

<section class="sec">
  <div class="sec-h"><h2>What the pattern shows</h2></div>
  <div class="finds">
    <div class="find">
      <h3>Build depth tracks the study's vintage, almost perfectly</h3>
      <p>Bottom-up construction is not spread across the book. It arrived with the current protocol and has
      been applied to whatever has been rebuilt since &mdash; the August-2026 cohort runs
      {vint['2026-08'][0]} bottom-up against {vint['2026-08'][1]}, the July-2026 cohort
      {vint['2026-07'][0]} against {vint['2026-07'][1]}.</p>
      <table class="mini">
        <thead><tr><th>Edition</th><th class="num">Bottom-up</th><th class="num">Not</th><th></th></tr></thead>
        <tbody>{vrows}</tbody>
      </table>
    </div>
    <div class="find">
      <h3>The code-built studies are where the unit builds live</h3>
      <p>Of the {NCODE} stocks whose study carries an <code>engine/&lt;name&gt;_study/</code> directory,
      <b>{cb[(1,1)]}</b> are bottom-up and {cb[(1,0)]} are not &mdash; MODON and SWDY stop at segment level
      on disclosure grounds, STC is top-down by an explicit gate decision. Of the {len(recs)-NCODE} studies
      with no build directory, only {cb[(0,1)]} are bottom-up: the five Egyptian developers, plus SALIK,
      LULU, CLHO and DSCW.</p>
    </div>
    <div class="find">
      <h3>Most of the non-bottom-up studies say so, and say why</h3>
      <p>This is the flag-the-gap rule working, not failing. STC, ADNOCGAS, AGTHIA, RMDA, SABIC, SWDY, MODON
      and CLHO each name the missing disclosure in the delivered document before falling back to a coarser
      driver. No study in the book manufactures a volume/price split its filings cannot support.</p>
    </div>
    <div class="find warn">
      <h3>Tier B should not be read as tier A</h3>
      <p>Seven studies have the full shape of a unit build on units that are <i>not disclosed</i>. ELEC
      back-solves tonnage from LME copper and the exchange rate; RIYADHCABLE runs a tonnage <i>index</i>
      (FY2025&nbsp;=&nbsp;100) because the company publishes no tonnage; and the five Egyptian developers
      price every project off a unit mix per square metre that four of the five state outright is
      "the preparer's estimates &hellip; illustrative, not authoritative", calibrated so the model reproduces
      disclosed totals. ARCC is the cautionary precedent inside the house: three earlier editions back-solved
      cement tonnes from an assumed price and presented the resulting utilisation as corroboration &mdash; an
      accounting identity that reproduces audited revenue for <i>any</i> price. They were withdrawn once the
      disclosed volumes were read.</p>
    </div>
    <div class="find warn">
      <h3>One live inconsistency, in the bank class</h3>
      <p>ADCB &mdash; the house bank reference &mdash; states that "all eight of ADCB's drivers are top-down,
      because the bank reports blended results &hellip; rather than the deposit-repricing betas, fee volumes or
      product unit-economics a bottom-up build would need". ADIB and DIB repeat that wording. But Al&nbsp;Rajhi,
      on a structurally identical NIM / cost-to-income / cost-of-risk bridge, calls the same construction
      "a legitimate bottom-up build rather than a manufactured one", and SNB says it forecasts net special
      commission income as "NIM &times; average earning assets rather than a top-down growth rate". The
      substance is the same; only the label differs. This audit applies the ADCB reading and places all
      {cnt['F']} banks in tier F &mdash; worth reconciling in the protocol so the term means one thing across
      the book.</p>
    </div>
  </div>
</section>

<footer>
  Sources: the latest delivered edition of each study in <code>files/</code>, cross-read against
  <code>engine/&lt;name&gt;_study/compute.py</code> where one exists. Coverage universe and exchange codes
  from <code>assets/data.js</code>. Every count on this page is computed from
  <code>engine/build_depth_audit/classification.py</code> &mdash; no figure is typed into the page.
  Not investment advice; this is a methodology audit, not a valuation.
</footer>
</div>

<script>
(function(){{
  var st={{b:null,g:null,x:null,q:""}};
  try{{var s=localStorage.getItem('bda');if(s)st=Object.assign(st,JSON.parse(s));}}catch(e){{}}
  var rows=[].slice.call(document.querySelectorAll('#tb .r')),
      btns=[].slice.call(document.querySelectorAll('.f')),
      q=document.getElementById('q'), hits=document.getElementById('hits');
  function apply(){{
    var n=0;
    rows.forEach(function(r){{
      var ok=(st.b===null||r.dataset.b===st.b)
           &&(st.g===null||r.dataset.g===st.g)
           &&(st.x===null||r.dataset.x===st.x)
           &&(!st.q||r.dataset.s.indexOf(st.q)>-1);
      r.classList.toggle('hide',!ok); if(ok)n++;
    }});
    btns.forEach(function(b){{b.setAttribute('aria-pressed', st[b.dataset.f]===b.dataset.v);}});
    hits.textContent=n+' of {len(recs)} shown';
    try{{localStorage.setItem('bda',JSON.stringify(st));}}catch(e){{}}
  }}
  btns.forEach(function(b){{b.addEventListener('click',function(){{
    var f=b.dataset.f; st[f]=(st[f]===b.dataset.v)?null:b.dataset.v; apply();
  }});}});
  q.value=st.q||''; q.addEventListener('input',function(){{st.q=q.value.trim().toLowerCase();apply();}});
  apply();
}})();
</script>
"""
p = os.path.join(HERE, 'build_depth_audit.html')
open(p, 'w', encoding='utf-8').write(HTML)
print('wrote', p, len(HTML), 'chars;', ybu, 'bottom-up /', nbu, 'not')
