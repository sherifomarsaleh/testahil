# Testahil automation

The idea: **you edit one file of numbers, everything else regenerates and publishes itself.**

## How it works (plain English)
1. Every stock has one config file in `data/` (e.g. `data/PHDC.yaml`). It holds
   the SOTP table, net debt, and the 10 Monte Carlo factors. **This is the only
   file you touch.** It's the "the table IS the model" idea, in a file.
2. `pipeline/run.py` reads that config, runs the 50,000-path Monte Carlo
   (seed 42, so it's reproducible), and renders a finished study into `studies/`.
3. The disclaimer / READ FIRST / RSI-reminder blocks live in the template
   (`templates/study.md.j2`) and never change — only the numbers get swapped in.
   No risk of accidentally editing the disclosure.
4. `.github/workflows/publish.yml` runs the whole thing **automatically** on a
   quarterly schedule (and whenever you change a config), then commits the new
   studies. Point GitHub Pages at `studies/` and the site updates itself.

## To run it yourself
```bash
pip install pyyaml numpy jinja2
python pipeline/run.py data/PHDC.yaml   # writes studies/PHDC.md
```

## To add a new stock
Copy `data/PHDC.yaml` to `data/ORAS.yaml`, change the numbers, push. Done.

## What's still manual (on purpose, for now)
- The narrative paragraphs (technical read, catalyst calendar) — these need your
  judgment. Next step is to template the parts that are mechanical and leave
  prose slots for you.
- Charts (football field, fan chart) — the matplotlib EFG-teal versions can be
  wired into the same pipeline as a next step.
- Pulling EGX/CBE numbers automatically into the config — next step is a fetch
  layer that fills the anchor price and flags audited vs vendor data.
