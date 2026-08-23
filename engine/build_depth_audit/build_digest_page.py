# -*- coding: utf-8 -*-
"""Publish the digest as a page with a copy button.

WHY. Four rounds of "is this the right one?" all pasted back the same stale text.
The cause was not the reader: a .md attachment gives no practical way to select
55,000 characters, so each round pasted whatever was already in the project. The
fix is a page with one button, not a fifth identical file.
"""
import html, os, hashlib, re
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'PROJECT_INSTRUCTIONS_11-07-2026.md')
raw = open(SRC, encoding='utf-8').read()
rev = re.match(r'DIGEST REVISION (\S+)', raw).group(1)
sha = hashlib.sha256(raw.encode()).hexdigest()[:12]
body = html.escape(raw)

HTML = f"""<title>The Project Instructions</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,600&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
:root{{--ground:#F2F4F7;--surface:#FFFFFF;--sunk:#E8EBF0;--ink:#141C26;--ink2:#3D4855;
 --muted:#697687;--line:#D8DDE5;--line2:#EBEEF3;--a:#0E6B5E;--on-a:#FFFFFF;
 --shadow:0 1px 2px rgba(20,28,38,.05),0 8px 24px -14px rgba(20,28,38,.18);}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--ground:#0F141A;--surface:#161D25;
 --sunk:#1E262F;--ink:#E9EDF2;--ink2:#C2CAD4;--muted:#8D99A8;--line:#2A343F;--line2:#212A34;
 --a:#5CC9B4;--on-a:#0F141A;--shadow:0 1px 2px rgba(0,0,0,.4),0 8px 28px -16px rgba(0,0,0,.7);}}}}
:root[data-theme="dark"]{{--ground:#0F141A;--surface:#161D25;--sunk:#1E262F;--ink:#E9EDF2;
 --ink2:#C2CAD4;--muted:#8D99A8;--line:#2A343F;--line2:#212A34;--a:#5CC9B4;--on-a:#0F141A;
 --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 28px -16px rgba(0,0,0,.7);}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--ground);color:var(--ink);
 font-family:"IBM Plex Sans",ui-sans-serif,system-ui,sans-serif;font-size:15.5px;line-height:1.6}}
.wrap{{max-width:900px;margin:0 auto;padding:clamp(20px,4vw,48px) clamp(14px,3vw,28px) 70px}}
h1{{font-family:Newsreader,ui-serif,Georgia,serif;font-weight:600;margin:0;
 font-size:clamp(28px,4.4vw,44px);line-height:1.06;letter-spacing:-.015em}}
p{{margin:0}}
.eyebrow{{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11px;letter-spacing:.15em;
 text-transform:uppercase;color:var(--muted)}}
header{{display:flex;flex-direction:column;gap:13px;padding-bottom:22px;border-bottom:1px solid var(--line)}}
.lede{{color:var(--ink2);max-width:62ch}}
.bar{{position:sticky;top:0;z-index:5;background:var(--ground);padding:16px 0 14px;
 display:flex;flex-wrap:wrap;gap:12px;align-items:center;border-bottom:1px solid var(--line2)}}
button{{font:inherit;font-weight:600;font-size:15px;background:var(--a);color:var(--on-a);
 border:0;border-radius:4px;padding:11px 22px;cursor:pointer;box-shadow:var(--shadow)}}
button:hover{{filter:brightness(1.07)}}
button:focus-visible{{outline:2px solid var(--a);outline-offset:3px}}
.meta{{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--muted);
 display:flex;flex-direction:column;gap:2px}}
.meta b{{color:var(--ink);font-weight:600}}
#said{{color:var(--a);font-weight:600;font-size:14px}}
.note{{background:var(--surface);border:1px solid var(--line2);border-left:3px solid var(--a);
 border-radius:3px;padding:14px 17px;margin-top:18px}}
.note p{{color:var(--ink2);font-size:14.5px;max-width:70ch}}
pre{{background:var(--surface);border:1px solid var(--line);border-radius:3px;
 padding:18px 20px;margin-top:16px;max-height:62vh;overflow:auto;white-space:pre-wrap;
 word-wrap:break-word;font-family:"IBM Plex Mono",monospace;font-size:12.5px;
 line-height:1.62;color:var(--ink2);box-shadow:var(--shadow)}}
pre::selection,pre *::selection{{background:var(--a);color:var(--on-a)}}
footer{{margin-top:26px;font-size:12.5px;color:var(--muted);max-width:74ch}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
</style>

<div class="wrap">
<header>
  <p class="eyebrow">TESTAHIL &middot; project instructions &middot; the block to paste</p>
  <h1>Revision {rev}</h1>
  <p class="lede">The whole condensed protocol, current as of this revision. Press the button,
  then paste over whatever is in your project instructions now. Nothing else needs doing.</p>
</header>

<div class="bar">
  <button id="copy" type="button">Copy all {len(raw):,} characters</button>
  <span id="said"></span>
  <span class="meta"><span>revision <b>{rev}</b></span><span>sha256 <b>{sha}</b></span></span>
</div>

<div class="note">
  <p><strong>How to tell it worked.</strong> What you paste must begin
  <code>DIGEST REVISION {rev}</code>. If the block in your project starts with
  &ldquo;TESTAHIL &mdash; Standing Research Protocol&rdquo; instead, it is the old one and the
  paste did not land.</p>
</div>

<pre id="text">{body}</pre>

<footer>
  Generated from <code>engine/PROJECT_INSTRUCTIONS_11-07-2026.md</code> on the
  <code>claude/stock-valuation-analysis-fkbnmg</code> branch. Regenerated by
  <code>build_digest_page.py</code> whenever the digest changes, so this page and the file
  cannot disagree.
</footer>
</div>

<script>
(function(){{
  var btn=document.getElementById('copy'), said=document.getElementById('said'),
      pre=document.getElementById('text');
  function tell(m){{ said.textContent=m; setTimeout(function(){{said.textContent='';}},4000); }}
  function fallback(){{
    var r=document.createRange(); r.selectNodeContents(pre);
    var s=window.getSelection(); s.removeAllRanges(); s.addRange(r);
    try{{ document.execCommand('copy'); tell('Copied.'); }}
    catch(e){{ tell('Selected — press Ctrl+C (Cmd+C) to copy.'); }}
  }}
  btn.addEventListener('click',function(){{
    var t=pre.textContent;
    if(navigator.clipboard && navigator.clipboard.writeText){{
      navigator.clipboard.writeText(t).then(function(){{tell('Copied.');}},fallback);
    }} else {{ fallback(); }}
  }});
}})();
</script>
"""
p = os.path.join(HERE, 'digest_page.html')
open(p, 'w', encoding='utf-8').write(HTML)
print('wrote', p, '|', len(raw), 'chars of digest | rev', rev, '| sha', sha)
