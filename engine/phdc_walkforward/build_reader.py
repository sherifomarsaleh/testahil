"""Render the PHDC walk-forward documents as one self-contained HTML reader.

The markdown files are the source of record; this only presents them. It is
written narrow-first because it is read in a side panel, not a browser tab:
one column, a sticky document switcher instead of a side rail, and every table
in its own horizontal scroller so the page body never scrolls sideways.

Nothing here restates a number. The renderer converts the committed markdown
and adds no content of its own beyond navigation.
"""
import os, re, html, json
import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = [
    ("record", "Training record", "TRAINING_RECORD_30-08-2026.md",
     "What the method would have done on this company's own history"),
    ("prereg", "Pre-registration", "PRE_REGISTRATION_30-08-2026.md",
     "Fixed before any error was computed"),
    ("breaks", "Basis breaks", "BASIS_BREAKS_30-08-2026.md",
     "Which years are comparable, and why"),
    ("origins", "Projected vs actual", "phdc_IS_projected_vs_actual_all_origins.md",
     "Ten origins, line by line"),
]

MD = markdown.Markdown(extensions=["tables", "fenced_code", "attr_list", "sane_lists"])


def convert(path):
    MD.reset()
    body = MD.convert(open(os.path.join(HERE, path), encoding="utf-8").read())
    # every table gets its own scroller — several run far wider than a side panel
    body = re.sub(r"<table>", '<div class="tw"><table>', body)
    body = re.sub(r"</table>", "</table></div>", body)
    # drop the H1 — the switcher already names the document
    body = re.sub(r"<h1>.*?</h1>", "", body, count=1, flags=re.S)
    return body


def toc(body):
    out = []
    for m in re.finditer(r"<h2>(.*?)</h2>", body, flags=re.S):
        text = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        out.append(text)
    return out


def slug(s):
    # prefixed because these headings start with a section number, and an id
    # beginning with a digit is legal HTML but not a legal CSS selector
    return "s-" + re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:58]


def anchor(body):
    def rep(m):
        text = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        return '<h2 id="%s">%s</h2>' % (slug(text), m.group(1))
    return re.sub(r"<h2>(.*?)</h2>", rep, body, flags=re.S)


CSS = """
:root{
  /* ledger paper, faintly green-grey — a picked neutral, not a default */
  --paper:#F4F6F3; --surface:#FFFFFF; --sunk:#EDF0EC;
  --ink:#171B18; --body:#2C3330; --muted:#657069; --faint:#8A948E;
  --rule:#D8DED8; --rule-soft:#E6EAE5;
  /* the subject is the SIGN and SIZE of an error, so the scale has two poles */
  --over:#9A3B26;      /* over-forecast, warm */
  --under:#1F6461;     /* under-forecast, cool */
  --flag:#8A6A18;      /* watch flag, ochre */
  --marker:#8A3324;    /* the one bold colour: a red pencil on a ledger */
  --marker-wash:#F6E9E4;
  --shadow:0 1px 2px rgba(23,27,24,.05),0 8px 24px -16px rgba(23,27,24,.22);
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --paper:#12150F; --surface:#191D17; --sunk:#20251E;
    --ink:#EEF1EA; --body:#D2D8CE; --muted:#98A296; --faint:#75806F;
    --rule:#2E352B; --rule-soft:#242A21;
    --over:#E0876A; --under:#6FB8B0; --flag:#D2AC55;
    --marker:#E39273; --marker-wash:#2A1D17;
    --shadow:0 1px 2px rgba(0,0,0,.4),0 10px 28px -18px rgba(0,0,0,.7);
  }
}
:root[data-theme="dark"]{
  --paper:#12150F; --surface:#191D17; --sunk:#20251E;
  --ink:#EEF1EA; --body:#D2D8CE; --muted:#98A296; --faint:#75806F;
  --rule:#2E352B; --rule-soft:#242A21;
  --over:#E0876A; --under:#6FB8B0; --flag:#D2AC55;
  --marker:#E39273; --marker-wash:#2A1D17;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 10px 28px -18px rgba(0,0,0,.7);
}

*{box-sizing:border-box}
body{
  margin:0; background:var(--paper); color:var(--body);
  font-family:"Source Serif 4",Iowan Old Style,Georgia,serif;
  font-size:16px; line-height:1.62;
  -webkit-font-smoothing:antialiased;
}
.wrap{max-width:74ch; margin:0 auto; padding:0 20px 80px}

/* ---- masthead ---------------------------------------------------------- */
header.mast{
  padding:26px 20px 18px; border-bottom:1px solid var(--rule);
  background:var(--surface);
}
.mast-in{max-width:74ch; margin:0 auto}
.eyebrow{
  font-family:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
  font-size:11px; letter-spacing:.13em; text-transform:uppercase;
  color:var(--muted); margin:0 0 8px;
}
h1.title{
  font-family:"IBM Plex Sans",system-ui,-apple-system,Segoe UI,sans-serif;
  font-weight:600; font-size:clamp(22px,5.2vw,30px); line-height:1.15;
  letter-spacing:-.015em; color:var(--ink); margin:0 0 10px; text-wrap:balance;
}
.standfirst{font-size:15px; color:var(--muted); margin:0; max-width:62ch}

/* facts strip — orientation, drawn straight from the record */
.facts{
  display:grid; grid-template-columns:repeat(auto-fit,minmax(88px,1fr));
  gap:1px; margin:18px 0 0; padding:1px;
  border-radius:3px; overflow:hidden; background:var(--rule);
}
.fact{padding:9px 12px; background:var(--sunk)}
.fact dt{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:10px;
  letter-spacing:.1em; text-transform:uppercase; color:var(--faint); margin:0 0 3px;
}
.fact dd{
  margin:0; font-family:"IBM Plex Mono",ui-monospace,monospace;
  font-size:16px; font-weight:500; color:var(--ink); font-variant-numeric:tabular-nums;
}

/* ---- document switcher ------------------------------------------------- */
nav.switch{
  position:sticky; top:0; z-index:20; background:var(--surface);
  border-bottom:1px solid var(--rule); box-shadow:var(--shadow);
}
/* the strip scrolls in a side panel — fade the right edge so it reads as more */
nav.switch::after{
  content:""; position:absolute; top:0; right:0; width:26px; height:100%;
  pointer-events:none;
  background:linear-gradient(to right,transparent,var(--surface));
}
.switch-in{
  max-width:74ch; margin:0 auto; display:flex; gap:2px; padding:0 12px;
  overflow-x:auto; scrollbar-width:none;
}
.switch-in::-webkit-scrollbar{display:none}
nav.switch button{
  appearance:none; border:0; background:none; cursor:pointer; white-space:nowrap;
  font-family:"IBM Plex Sans",system-ui,sans-serif; font-size:13px; font-weight:500;
  color:var(--muted); padding:13px 12px 11px; border-bottom:2px solid transparent;
  letter-spacing:-.005em;
}
nav.switch button:hover{color:var(--ink)}
nav.switch button[aria-selected="true"]{color:var(--marker); border-bottom-color:var(--marker)}
nav.switch button:focus-visible{outline:2px solid var(--marker); outline-offset:-3px; border-radius:2px}

.doc-note{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:11px;
  letter-spacing:.04em; color:var(--faint); padding:14px 0 0; margin:0;
}

/* ---- prose ------------------------------------------------------------- */
article h2{
  font-family:"IBM Plex Sans",system-ui,sans-serif; font-weight:600;
  font-size:clamp(17px,4vw,21px); line-height:1.25; letter-spacing:-.012em;
  color:var(--ink); margin:44px 0 4px; padding-top:18px;
  border-top:1px solid var(--rule); text-wrap:balance;
}
article h2:first-of-type{border-top:0; padding-top:0; margin-top:26px}
article h3{
  font-family:"IBM Plex Sans",system-ui,sans-serif; font-weight:600;
  font-size:15px; color:var(--ink); margin:30px 0 2px; letter-spacing:-.005em;
}
article p{margin:14px 0}
article strong{color:var(--ink); font-weight:600}
article em{color:var(--body)}
article ul,article ol{margin:14px 0; padding-left:22px}
article li{margin:7px 0}
article li::marker{color:var(--faint)}
article hr{border:0; border-top:1px solid var(--rule); margin:38px 0}
article a{color:var(--marker); text-underline-offset:2px}

blockquote{
  margin:18px 0; padding:2px 0 2px 16px; border-left:2px solid var(--marker);
  color:var(--body); font-style:italic;
}
blockquote p{margin:8px 0}

code{
  font-family:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
  font-size:.86em; background:var(--sunk); padding:1px 5px; border-radius:3px;
  color:var(--ink); font-variant-numeric:tabular-nums;
}
pre{
  background:var(--sunk); border:1px solid var(--rule-soft); border-radius:4px;
  padding:14px 16px; overflow-x:auto; margin:18px 0;
}
pre code{background:none; padding:0; font-size:12.5px; line-height:1.65}

/* ---- tables ------------------------------------------------------------ */
.tw{
  overflow-x:auto; margin:20px 0; border:1px solid var(--rule);
  border-radius:4px; background:var(--surface);
  -webkit-overflow-scrolling:touch;
}
table{border-collapse:collapse; width:100%; min-width:max-content}
th,td{
  padding:8px 12px; text-align:left; border-bottom:1px solid var(--rule-soft);
  font-size:13px; line-height:1.45; white-space:nowrap;
}
th{
  font-family:"IBM Plex Sans",system-ui,sans-serif; font-weight:600; font-size:11px;
  letter-spacing:.06em; text-transform:uppercase; color:var(--muted);
  background:var(--sunk); position:sticky; top:0;
  border-bottom:1px solid var(--rule);
}
td{
  font-family:"IBM Plex Mono",ui-monospace,monospace;
  font-variant-numeric:tabular-nums; color:var(--body);
}
td:first-child{
  font-family:"Source Serif 4",Georgia,serif; color:var(--ink);
  white-space:normal; min-width:13ch;
}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover td{background:var(--sunk)}
/* colour only what the document itself already emphasised */
td strong{color:var(--marker); font-weight:600}

footer.end{
  margin-top:52px; padding-top:18px; border-top:1px solid var(--rule);
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:11px;
  color:var(--faint); letter-spacing:.03em; line-height:1.7;
}
[hidden]{display:none !important}
@media (prefers-reduced-motion:no-preference){
  article{animation:fade .18s ease-out}
  @keyframes fade{from{opacity:0}to{opacity:1}}
}
"""

JS = """
const tabs=[...document.querySelectorAll('nav.switch button')];
const docs=[...document.querySelectorAll('article')];
function show(id){
  tabs.forEach(t=>t.setAttribute('aria-selected',String(t.dataset.doc===id)));
  docs.forEach(d=>{d.hidden=(d.id!==id)});
  window.scrollTo({top:0,behavior:'instant'});
  try{localStorage.setItem('phdc-doc',id)}catch(e){}
}
tabs.forEach(t=>t.addEventListener('click',()=>show(t.dataset.doc)));
let start='record';
try{const s=localStorage.getItem('phdc-doc'); if(s&&document.getElementById(s))start=s}catch(e){}
show(start);
"""


def build(out_path):
    parts = []
    for key, label, path, note in DOCS:
        body = anchor(convert(path))
        parts.append('<article id="%s" hidden><p class="doc-note">%s</p>%s'
                     '<footer class="end">engine/phdc_walkforward/%s<br>'
                     'training record only · nothing published · '
                     'no rating, target or recommendation</footer></article>'
                     % (key, html.escape(note), body, html.escape(path)))
    tabs = "".join(
        '<button data-doc="%s" role="tab" aria-selected="false">%s</button>'
        % (k, html.escape(l)) for k, l, _, _ in DOCS)
    facts = [("origins", "10"), ("horizons", "1–5y"), ("panel span", "FY11–25"),
             ("documents", "88"), ("records", "551")]
    factstrip = "".join('<div class="fact"><dt>%s</dt><dd>%s</dd></div>' % (k, v)
                        for k, v in facts)
    doc = """<title>PHDC Walk-Forward Record</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<style>%s</style>
<header class="mast"><div class="mast-in">
  <p class="eyebrow">Palm Hills Developments · EGX:PHDC · 30 August 2026</p>
  <h1 class="title">Fundamental walk-forward training</h1>
  <p class="standfirst">Training the fundamental method on this company's own
  history before the update's build is finalised. Nothing here is published.</p>
  <dl class="facts">%s</dl>
</div></header>
<nav class="switch"><div class="switch-in" role="tablist">%s</div></nav>
<div class="wrap">%s</div>
<script>%s</script>""" % (CSS, factstrip, tabs, "".join(parts), JS)
    open(out_path, "w", encoding="utf-8").write(doc)
    return len(doc)


if __name__ == "__main__":
    out = os.environ.get("PHDC_READER", os.path.join(
        "/tmp/claude-0/-home-user-testahil/2283e95e-66db-5f22-bba6-0db833f32495"
        "/scratchpad/render", "PHDC_walkforward_record.html"))
    n = build(out)
    print("%s  (%.1f KB)" % (out, n / 1024.0))
