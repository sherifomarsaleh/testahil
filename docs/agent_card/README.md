# The agent card

A one-page reference for the committed subagents in `.claude/agents/`: what to say to
reach each one, what it hands back, and where it stops. Page two draws where each agent
sits in the workflow it belongs to.

Written for the operator, not for a reader of the research — nothing here is delivered to
anyone outside the project.

## What is here

| File | What it is |
|---|---|
| `TESTAHIL_Agent_Card.docx` | **GENERATED — never hand-edit.** The deliverable, A4 landscape, two pages. |
| `agent_card.html` | The same card as a web page, and the source of the schematic. Hand-authored. |
| `schematic.png` | **GENERATED** from the `<svg>` inside `agent_card.html`. The figure on page two. |
| `build_card_docx.js` | The generator. Reads `schematic.png`, writes the `.docx` beside itself. |

The Word document states facts that move — how many agents there are, what each one
refuses to do — so it is generated rather than typed, the same discipline the band
records and the as-of stamps obey. Edit the generator, never the `.docx`.

## Rebuilding it

```
node docs/agent_card/build_card_docx.js          # -> TESTAHIL_Agent_Card.docx
```

`docx` (npm) must resolve. From the repo root it does; from elsewhere,
`NODE_PATH=<repo>/node_modules`.

To regenerate the schematic after editing the `<svg>` in `agent_card.html` — it needs a
browser, so it is a separate step and the PNG is committed rather than built in CI:

```
python3 - <<'PY'
import re, pathlib
src = pathlib.Path('docs/agent_card/agent_card.html').read_text(encoding='utf-8')
style = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
svg   = re.search(r'(<svg .*?</svg>)', src, re.S).group(1)
light = ':root, :root[data-theme="dark"] { --ground:#FFF; --surface:#FFF; --sunk:#E8EBF0;' \
        ' --ink:#141C26; --ink2:#3D4855; --muted:#697687; --line:#D8DDE5; --line2:#EBEEF3;' \
        ' --a:#0E6B5E; --a-soft:#E3F0ED; --stop:#A4552F; --stop-soft:#F6E9E1; }' \
        'body{margin:0;background:#fff}#wrap{width:1280px;background:#fff;padding:8px 10px}' \
        '#wrap svg{width:1280px;min-width:0;height:auto;color:#141C26}'
pathlib.Path('/tmp/schematic.html').write_text(
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    'family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">'
    f'<style>{style}{light}</style><div id="wrap">{svg}</div>', encoding='utf-8')
PY
node -e "const {chromium}=require('playwright');(async()=>{
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const p=await b.newPage({viewport:{width:1340,height:980},deviceScaleFactor:2});
  await p.goto('file:///tmp/schematic.html',{waitUntil:'load'}); await p.waitForTimeout(1200);
  await (await p.\$('#wrap')).screenshot({path:'docs/agent_card/schematic.png'}); await b.close();})()"
```

The PNG's aspect ratio is set by the SVG's `viewBox`. If you change it, change
`transformation: { width, height }` in the generator to match, or the figure will be
stretched.

## Keeping it true

**The card counts the agents, so adding or removing one makes it stale.** A ninth agent
(`testahil-answer-challenger`) landed while this card said eight, which is how the count
was caught. When `.claude/agents/` changes, the row goes into the table in BOTH
`agent_card.html` and `build_card_docx.js`, a lane goes into the schematic if the agent
has a workflow of its own, and the "nine subagents" / "all nine" prose moves with it.

**A gate holds it** — `python3 scripts/check_agent_card.py`, which reads the agent list
from `.claude/agents/` rather than from the card [R-ENF-04] and FAILS if a card source
omits an agent, names one that no longer exists, miscounts them in prose, or if the
committed `.docx` is older than the generator that makes it. It runs in CI. The first
draft of this README said the card was kept true by hand; that is the shape [R-ENF-01]
forbids wherever a test is possible, and here the test is a directory listing and a
substring search.

## Rendering it to look at

LibreOffice needs `libreoffice-writer`, not just `libreoffice-core` — without it every
`.docx` fails to load with "source file could not be loaded", the same symptom
`engine/make_pdf.py` hits.

```
apt-get install -y libreoffice-writer poppler-utils
soffice --headless --convert-to pdf TESTAHIL_Agent_Card.docx
pdftoppm -jpeg -r 100 TESTAHIL_Agent_Card.pdf page
```
