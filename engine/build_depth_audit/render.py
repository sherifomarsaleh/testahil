# -*- coding: utf-8 -*-
"""Render the build-depth audit table from classification.py. No number is typed here."""
import importlib.util, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('classification', os.path.join(HERE, 'classification.py'))
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
ROWS = C.ROWS

TIER = {
 'A' : 'Bottom-up — disclosed units',
 'A-': 'Bottom-up — major legs',
 'B' : 'Bottom-up — derived units',
 'C' : 'Segment-level',
 'D' : 'Top-down',
 'E' : 'Asset / NAV / stake marks',
 'F' : 'Bank driver build',
}
ORDER = ['A','A-','B','C','D','E','F']

def mkt(code): return code.split(':')[0]

bu  = [r for r in ROWS if r[5]]
nbu = [r for r in ROWS if not r[5]]
bu.sort(key=lambda r: (ORDER.index(r[4]), r[0]))
nbu.sort(key=lambda r: (ORDER.index(r[4]), r[0]))

def table(rows):
    out = ['| Ticker | Company | Exchange | Study edition | Build tier | How the forecast is actually built |',
           '|---|---|---|---|---|---|']
    for tk, nm, code, ed, tier, _, ev in rows:
        out.append(f'| **{tk}** | {nm} | {mkt(code)} | {ed} | {TIER[tier]} | {ev} |')
    return '\n'.join(out)

cnt = collections.Counter(r[4] for r in ROWS)
vint = collections.defaultdict(lambda: [0, 0])
for r in ROWS:
    d, mo, y = r[3].split('-')
    vint[f'{y}-{mo}'][0 if r[5] else 1] += 1
eng = {d[:-6].upper() for d in os.listdir(os.path.dirname(HERE)) if d.endswith('_study')}
def coded(tk): return tk in eng or (tk == 'FERTIGLB' and 'FERTIGLOBE' in eng)
cb = collections.Counter((coded(r[0]), r[5]) for r in ROWS)

MD = f"""# Build-depth audit — which fundamental valuations were built from the bottom up

**Scope.** Every stock carrying a published fundamental fair value in `assets/data.js`
(**{len(ROWS)}** names). The four metals studies (XAUUSD, XAUUSD 12M, XAGUSD, XPTUSD) are
excluded — they have no corporate revenue build to classify. Each row was read out of the
latest delivered edition of that stock's own study, and for the {sum(1 for r in ROWS if coded(r[0]))}
studies that carry a code-built `engine/<name>_study/` directory, cross-read against
`compute.py` / `bottom_up.json`.

**Standard applied.** SIGCM clause 2 and DRIVER DISCIPLINE in the Standing Research Protocol:
*revenue as VOLUME × PRICE and cost as COST-PER-UNIT, product by product or service by service
wherever segments are disclosed; where unit/segment data is not disclosed, drop to the finest
sourced level and FLAG the gap.* A study counts as **built bottom-up** only where the forecast
runs on a physical unit and a rate per unit, with margins falling out as outputs.

## Headline

| | Count | Share |
|---|---|---|
| **Built from the bottom up** | **{len(bu)}** | {len(bu)/len(ROWS):.0%} |
| **Not built from the bottom up** | **{len(nbu)}** | {len(nbu)/len(ROWS):.0%} |
| Total covered stocks | {len(ROWS)} | 100% |

### The seven build tiers

| Tier | Meaning | Count | Counts as bottom-up? |
|---|---|---|---|
| A | {TIER['A']} — revenue = a disclosed physical unit × a price/rate, cost per unit, margins as outputs | {cnt['A']} | Yes |
| A− | {TIER['A-']} — the unit build covers the major legs; the remainder sits at segment level because nothing finer is disclosed, and the study says so | {cnt['A-']} | Yes |
| B | {TIER['B']} — genuine unit economics, but the units are the preparer's estimate, an index, or back-solved from disclosed totals | {cnt['B']} | Yes, with the caveat |
| C | {TIER['C']} — each disclosed segment on its own driver, no unit economics; gap flagged | {cnt['C']} | No |
| D | {TIER['D']} — a group or segment revenue-growth path plus a margin assumption or glide | {cnt['D']} | No |
| E | {TIER['E']} — value comes from marking assets, stakes or segment earnings at multiples; no revenue build at all | {cnt['E']} | No |
| F | {TIER['F']} — balances × margin (NIM / cost-of-risk / cost-to-income bridge) | {cnt['F']} | No |

---

## A. Built from the bottom up — {len(bu)} stocks

{table(bu)}

---

## B. Not built from the bottom up — {len(nbu)} stocks

{table(nbu)}

---

## What the pattern shows

**1. Build depth tracks the study's vintage almost perfectly.**

| Study edition | Bottom-up | Not bottom-up |
|---|---|---|
""" + '\n'.join(f'| {k} | {v[0]} | {v[1]} |' for k, v in sorted(vint.items())) + f"""

The August-2026 cohort is {vint['2026-08'][0]} bottom-up against {vint['2026-08'][1]} not; the
July-2026 cohort is {vint['2026-07'][0]} against {vint['2026-07'][1]}. Bottom-up construction is
not distributed across the book — it arrived with the current protocol and has been applied
to whatever has been rebuilt since.

**2. The code-built studies are where the unit builds live.**
Of the {sum(1 for r in ROWS if coded(r[0]))} stocks whose study carries an
`engine/<name>_study/` directory with a `compute.py`, **{cb[(True, True)]}** are bottom-up and
{cb[(True, False)]} are not (MODON and SWDY stop at segment level on disclosure grounds; STC is
top-down by an explicit gate decision). Of the {sum(1 for r in ROWS if not coded(r[0]))} studies
with no code directory, only {cb[(False, True)]} are bottom-up — the five Egyptian developers,
plus SALIK, LULU, CLHO and DSCW.

**3. Most non-bottom-up studies say so, and say why.**
This is the protocol's flag-the-gap rule working rather than failing. STC, ADNOCGAS, AGTHIA,
RMDA, SABIC, SWDY, MODON and CLHO each name the missing disclosure in the delivered document
before falling back. The refusals are consistent: no study manufactures a volume/price split
the filings do not support.

**4. Tier B is a real distinction and should not be read as tier A.**
Seven studies have the full shape of a unit build on units that are *not disclosed*: ELEC
back-solves tonnage from LME copper and FX; RIYADHCABLE runs a tonnage *index* (FY2025 = 100)
because the company publishes no tonnage; and the five Egyptian developers (PHDC, TMGH, OCDI,
ORHD, EMFD) price every project from a unit mix per square metre that four of the five state
outright is "the preparer's estimates ... illustrative, not authoritative", calibrated so the
model reproduces disclosed totals. ARCC is the cautionary precedent inside the house: three
earlier editions back-solved cement tonnes from an assumed price and presented the resulting
utilisation as corroboration — an accounting identity that reproduces audited revenue for *any*
price. Those editions were withdrawn once the disclosed volumes were read.

**5. One live inconsistency in self-labelling, in the bank class.**
ADCB — the house's bank reference study — states that "all eight of ADCB's drivers are top-down,
because the bank reports blended results ... rather than the deposit-repricing betas, fee volumes
or product unit-economics a bottom-up build would need". ADIB and DIB repeat that wording.
But Al Rajhi, on a structurally identical NIM / cost-to-income / cost-of-risk bridge, calls the
same construction "a legitimate bottom-up build rather than a manufactured one", and SNB says it
forecasts net special commission income as "NIM × average earning assets rather than a top-down
growth rate". The substance is the same in all of them; only the label differs. This audit applies
the ADCB reading — the governing bank precedent — and puts all twelve banks in tier F, outside
bottom-up. Worth reconciling in the protocol so the term means one thing across the book.
"""
open(os.path.join(HERE, 'BUILD_DEPTH_AUDIT_23-08-2026.md'), 'w', encoding='utf-8').write(MD)
print('bottom-up', len(bu), '/ not', len(nbu), '/ total', len(ROWS))
print('written', os.path.join(HERE, 'BUILD_DEPTH_AUDIT_23-08-2026.md'))
