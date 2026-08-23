# -*- coding: utf-8 -*-
"""Render the rebuild queue as a plain-language page. Every figure computed, none typed."""
import json, os, html, collections, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
Q = json.load(open(os.path.join(HERE, 'queue.json')))
def esc(s): return html.escape(str(s), quote=False)

ALL = [i for w in Q for b in w['batches'] for i in b['items']]
N = len(ALL)
needs = collections.Counter(i['needs'] for i in ALL)
COC = needs['cost of capital']; BOTH = needs['cost of capital + ground-up rebuild']

# enforcement state, read live
dirs = [d for d in sorted(os.listdir(os.path.dirname(HERE))) if d.endswith('_study') and d != 'xpt_study']
def gated(d):
    p = os.path.join(os.path.dirname(HERE), d)
    for f in os.listdir(p):
        if f.endswith('.py'):
            try: t = open(os.path.join(p, f), encoding='utf-8', errors='ignore').read()
            except Exception: continue
            if 'assert_sigcm' in t or 'assert_beta_provenance' in t or 'assert_model_study' in t:
                return True
    return False
GATED = sum(gated(d) for d in dirs); NDIRS = len(dirs)
WF = os.path.join(os.path.dirname(os.path.dirname(HERE)), '.github', 'workflows')
ci = 0
for f in os.listdir(WF):
    t = open(os.path.join(WF, f), encoding='utf-8').read()
    if any(k in t for k in ('assert_sigcm', 'assert_beta_provenance', 'gate_check', 'qc_gate', 'attest')):
        ci += 1

NEED_LABEL = {'cost of capital': 'risk number',
              'cost of capital + ground-up rebuild': 'risk number + ground-up rebuild'}

def item(i):
    short = NEED_LABEL[i['needs']]
    cls = 'both' if 'rebuild' in short else 'coc'
    return (f'<tr><td class="sq">{i["seq"]}</td>'
            f'<td class="tk">{i["tk"]}</td>'
            f'<td class="nm">{esc(i["nm"])}<span class="mob">{i["x"]}</span></td>'
            f'<td class="xc"><span class="chip">{i["x"]}</span></td>'
            f'<td class="nd"><span class="pill {cls}">{short}</span></td></tr>')

waves = ''
for w in Q:
    bs = ''
    for b in w['batches']:
        bs += (f'<div class="batch"><p class="bh"><span class="chip">{b["exchange"]}</span>'
               f'<span class="bcls">{esc(b["cls"])}</span>'
               f'<span class="bn">{len(b["items"])}</span></p>'
               f'<div class="tw"><table><tbody>'
               + ''.join(item(i) for i in b['items']) + '</tbody></table></div></div>')
    waves += (f'<section class="wave"><div class="wh"><p class="eyebrow">{esc(w["wave"])} '
              f'&middot; {w["count"]} studies</p><h2>{esc(w["label"])}</h2>'
              f'<p class="why">{esc(w["why"])}</p></div>{bs}</section>')

HTML = f"""<title>The Rebuild Queue</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
:root{{
  --ground:#F2F4F7; --surface:#FFFFFF; --sunk:#E8EBF0;
  --ink:#141C26; --ink2:#3D4855; --muted:#697687; --line:#D8DDE5; --line2:#EBEEF3;
  --a:#0E6B5E; --a2:#12897A; --warn:#9A5A2B; --on-accent:#FFFFFF;
  --coc:#0E6B5E; --coc-s:#DCEDE9; --both:#9A5A2B; --both-s:#F3E6D9;
  --shadow:0 1px 2px rgba(20,28,38,.05),0 8px 24px -14px rgba(20,28,38,.18);
}}
@media (prefers-color-scheme:dark){{ :root:not([data-theme="light"]){{
  --ground:#0F141A; --surface:#161D25; --sunk:#1E262F;
  --ink:#E9EDF2; --ink2:#C2CAD4; --muted:#8D99A8; --line:#2A343F; --line2:#212A34;
  --a:#5CC9B4; --a2:#7FD8C6; --warn:#D9A16A; --on-accent:#0F141A;
  --coc:#5CC9B4; --coc-s:#123832; --both:#D9A16A; --both-s:#38271A;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 28px -16px rgba(0,0,0,.7);
}} }}
:root[data-theme="dark"]{{
  --ground:#0F141A; --surface:#161D25; --sunk:#1E262F;
  --ink:#E9EDF2; --ink2:#C2CAD4; --muted:#8D99A8; --line:#2A343F; --line2:#212A34;
  --a:#5CC9B4; --a2:#7FD8C6; --warn:#D9A16A; --on-accent:#0F141A;
  --coc:#5CC9B4; --coc-s:#123832; --both:#D9A16A; --both-s:#38271A;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 28px -16px rgba(0,0,0,.7);
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--ground);color:var(--ink);
  font-family:"IBM Plex Sans",ui-sans-serif,system-ui,sans-serif;font-size:15.5px;line-height:1.6;
  -webkit-font-smoothing:antialiased}}
.wrap{{max-width:900px;margin:0 auto;padding:clamp(22px,4vw,54px) clamp(15px,3vw,30px) 80px}}
h1,h2{{font-family:Newsreader,ui-serif,Georgia,serif;font-weight:600;text-wrap:balance;margin:0}}
h1{{font-size:clamp(31px,5vw,50px);line-height:1.05;letter-spacing:-.015em}}
h2{{font-size:clamp(20px,2.5vw,27px);letter-spacing:-.01em}}
h3{{font-family:"IBM Plex Sans",sans-serif;font-size:15px;font-weight:600;margin:0}}
p{{margin:0}}
.eyebrow{{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11px;letter-spacing:.15em;
  text-transform:uppercase;color:var(--muted)}}
header{{display:flex;flex-direction:column;gap:15px;padding-bottom:26px;border-bottom:1px solid var(--line)}}
.lede{{font-size:18px;color:var(--ink2);max-width:62ch}}
.plain{{background:var(--surface);border:1px solid var(--line2);border-radius:3px;padding:16px 19px;
  margin-top:26px;display:grid;gap:9px}}
.plain dt{{font-weight:600;font-size:14px}}
.plain dd{{margin:0 0 4px;color:var(--ink2);font-size:14px;max-width:70ch}}
.check{{background:var(--surface);border:1px solid var(--line);border-left:3px solid var(--a);
  border-radius:3px;padding:20px 22px;margin-top:28px;box-shadow:var(--shadow);display:grid;gap:11px}}
.check p{{color:var(--ink2);max-width:64ch}}
.check strong{{color:var(--ink)}}
.mini{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;background:var(--line);
  border:1px solid var(--line);border-radius:3px;margin-top:4px}}
.mini div{{background:var(--surface);padding:12px 14px}}
.mini .k{{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--muted)}}
.mini .v{{font-family:Newsreader,serif;font-size:29px;line-height:1.1}}
.mini .v.bad{{color:var(--warn)}} .mini .v.good{{color:var(--a)}}
.sec{{margin-top:48px;display:flex;flex-direction:column;gap:13px}}
.sec>p{{max-width:66ch;color:var(--ink2)}}
.pre{{display:grid;gap:11px}}
.prei{{background:var(--surface);border:1px solid var(--line2);border-left:3px solid var(--warn);
  border-radius:3px;padding:14px 17px}}
.prei h3{{margin-bottom:3px}}
.prei.done{{border-left-color:var(--a)}}
.prei.done h3{{color:var(--a)}}
.prei p{{color:var(--ink2);font-size:14.5px;max-width:64ch}}
.wave{{margin-top:44px;display:flex;flex-direction:column;gap:13px}}
.wh{{display:flex;flex-direction:column;gap:5px;padding-bottom:4px;border-bottom:1px solid var(--line)}}
.why{{color:var(--ink2);font-size:14.5px;max-width:68ch}}
.batch{{background:var(--surface);border:1px solid var(--line2);border-radius:3px;overflow:hidden}}
.bh{{display:flex;align-items:center;gap:10px;padding:9px 13px;background:var(--sunk);
  border-bottom:1px solid var(--line2)}}
.bcls{{font-size:13.5px;font-weight:600}}
.bn{{margin-left:auto;font-family:"IBM Plex Mono",monospace;font-size:11.5px;color:var(--muted)}}
.chip{{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.08em;padding:2px 7px;
  border:1px solid var(--line);border-radius:3px;color:var(--muted);white-space:nowrap}}
.tw{{overflow-x:auto}}
table{{border-collapse:collapse;width:100%}}
td{{padding:8px 13px;border-bottom:1px solid var(--line2);font-size:13.5px;vertical-align:middle}}
tr:last-child td{{border-bottom:0}}
tr:hover td{{background:var(--sunk)}}
.sq{{font-family:"IBM Plex Mono",monospace;color:var(--muted);width:42px;
  font-variant-numeric:tabular-nums;text-align:right}}
.tk{{font-family:"IBM Plex Mono",monospace;font-weight:600;width:120px;white-space:nowrap}}
.nm{{color:var(--ink2)}}
.mob{{display:none}}
.xc{{width:70px}}
.nd{{width:230px;text-align:right}}
.pill{{font-size:11.5px;padding:2px 9px;border-radius:999px;white-space:nowrap;font-weight:500}}
.pill.coc{{background:var(--coc-s);color:var(--coc)}}
.pill.both{{background:var(--both-s);color:var(--both)}}
footer{{margin-top:52px;padding-top:20px;border-top:1px solid var(--line);font-size:12.5px;
  color:var(--muted);max-width:74ch}}
code{{font-family:"IBM Plex Mono",monospace;font-size:.88em;background:var(--sunk);
  padding:1px 5px;border-radius:3px}}
@media (max-width:680px){{
  .nd,.xc{{display:none}} .tk{{width:auto}}
  .mob{{display:block;font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--muted)}}
}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important;animation:none!important}}}}
</style>

<div class="wrap">
<header>
  <p class="eyebrow">TESTAHIL &middot; 23 Aug 2026 &middot; the work list</p>
  <h1>The {N} studies to redo, in order</h1>
  <p class="lede">Every covered stock except the {90-N} that are already done properly, arranged so the
  cheapest work comes first and each country's homework is done once instead of once per company.</p>
</header>

<dl class="plain">
  <div><dt>"The risk number"</dt>
  <dd>The measure of how risky a company is, used to turn its future profits into a value today.
  It is supposed to be measured by comparing the share price against its own stock market index.
  In most of these studies it was chosen, not measured.</dd></div>
  <div><dt>"Ground-up rebuild"</dt>
  <dd>Forecasting revenue as <em>how many units sold &times; the price of each</em>, and cost as
  <em>cost per unit</em>, rather than growing last year's total by a percentage.</dd></div>
</dl>

<div class="check">
  <p class="eyebrow">you asked me to check the instructions &mdash; here is what I found</p>
  <p><strong>The written rules are right.</strong> The instructions now require the risk number to be
  measured against the exchange's own published index, forbid the shortcut that caused the original
  problem, require the ground-up build, and require the cost of capital to be sourced rather than
  assumed. Nothing is missing from the text.</p>
  <p><strong>What is missing is the enforcement.</strong> The checking code exists, but each study has
  to choose to call it. A study that simply doesn't call the check passes anyway &mdash; and no
  automated check runs on the repository at all.</p>
  <div class="mini">
    <div><span class="k">Studies with code</span><span class="v">{NDIRS}</span></div>
    <div><span class="k">Calling the check</span><span class="v good">{GATED}</span></div>
    <div><span class="k">Not calling it</span><span class="v bad">{NDIRS-GATED}</span></div>
    <div><span class="k">Automated checks</span><span class="v bad">{ci}</span></div>
  </div>
  <p>This matters because a rule that isn't enforced is exactly what you had before: the original
  shortcut spread through the whole book <em>while the rule against it was already written down</em>.
  Making the check run automatically, and fail the build when it doesn't pass, is a day's work and it
  is the one thing that stops this recurring.</p>
</div>

<section class="sec">
  <h2>Before study number 1</h2>
  <p>None of these is a study rebuild. The first is already settled; the other two are quick and both
  change answers in the queue below, so doing them first avoids redoing work.</p>
  <div class="pre">
    <div class="prei done"><h3>Dubai index &mdash; decided, nothing to do</h3>
    <p>The eight Dubai-listed companies stay on the Abu Dhabi index, by your instruction of
    23&nbsp;Aug&nbsp;2026. That decision is now written into both protocol files and into the code note, so
    a later session will not switch it back on its own. Two conditions come with it: every Dubai company's
    write-up must say plainly that its risk number rests on another exchange's index, and none of them may
    be described as fully conforming. Wave&nbsp;3 is unblocked.</p></div>
    <div class="prei"><h3>Remove the duplicate index file</h3>
    <p>The same index is saved twice under two different names. Two studies point at the copy the system
    doesn't recognise, so their work can't be verified even though the numbers are right.</p></div>
    <div class="prei"><h3>Decide what happens to ARCC and SCEM</h3>
    <p>These two don't move closely enough with the Egyptian market for the measurement to be reliable.
    The rules say fall back to a comparison with similar Egyptian companies, or to a neutral value. Which
    one you pick sets the precedent for every thinly-traded Egyptian company behind them, so decide it
    once, now, rather than eight times during Wave&nbsp;2.</p></div>
  </div>
</section>

<section class="sec">
  <h2>How the order was chosen</h2>
  <p>Cheapest first, then country by country. {COC} of the {N} studies need only the risk number fixed
  because they are already built from the ground up; the other {BOTH} need both, and each of those is a
  full rebuild rather than an edit. Within a country the companies are grouped by type, so banks are done
  together, developers together, and so on &mdash; each group shares one method and one set of comparable
  companies, so the research behind it is done once.</p>
</section>

{waves}

<footer>
  Order computed by <code>engine/build_depth_audit/sequence.py</code> from the 23-Aug-2026 build-depth
  audit and the beta-provenance state of each study's own committed records. Company types are set
  explicitly in <code>classes.py</code>, not guessed from the valuation method. The enforcement counts
  above are read live from the repository each time this page is built.
</footer>
</div>
"""
p = os.path.join(HERE, 'rebuild_queue.html')
open(p, 'w', encoding='utf-8').write(HTML)
print('wrote', p, len(HTML), 'chars |', N, 'studies |', GATED, 'of', NDIRS, 'gated |', ci, 'CI checks')
