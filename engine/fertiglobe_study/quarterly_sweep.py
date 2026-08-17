"""Extend the cost pass-through sample from 3 annual periods to 10 quarterly ones.

WHY THIS EXISTS. The published study fitted the pass-through slope on THREE disclosed
periods (FY2024, FY2025, H1-2026). With two fitted parameters that leaves one degree of
freedom, so the 90% interval on the slope was [-0.14, +1.10] -- the whole economically
possible range. R-squared of 0.96 on three points is near-guaranteed by construction and
overstates what the data supports.

WHY NOT SIMPLY ADD FY2022 AND FY2023. They were fetched and tested (see the regime test
in the study): Algeria's ten-year gas price-stability agreement was still in force until
the end of 2023, so gas was effectively FIXED while urea spiked. FY2022's realised cash
cost sits ~107 $/t BELOW the post-2023 relationship. Pooling the two regimes drags the
slope from 0.481 to 0.286 -- which would RAISE the valuation. That is a regime break, not
extra evidence, and using it would flatter the answer.

WHAT THIS DOES INSTEAD. Every quarter from Q1-2024 (the first fully post-agreement
quarter) to Q2-2026 is read from the company's own quarterly MD&A reports -- segment
revenue and adjusted EBITDA for the own-produced segment, own-produced urea and ammonia
volumes, and the CRU/MMSA benchmark prices. Ten observations inside ONE cost regime,
df=8 instead of df=1.

SOURCE: fertiglobe.com investor-relations results archive, quarterly MD&A reports.
Primary documents only -- no aggregator, no broker.
"""
import json
import os
import re
import sys

QDIR = sys.argv[1] if len(sys.argv) > 1 else 'q'
HERE = os.path.dirname(os.path.abspath(__file__))
NUM = r'\(?-?[\d,]+\.?\d*\)?'

ORDER = ['q1_24', 'q2_24', 'q3_24', 'q4_24', 'q1_25',
         'q2_25', 'q3_25', 'q4_25', 'q1_26', 'q2_26']
LABEL = {k: f"Q{k[1]}-20{k[3:]}" for k in ORDER}


def num(s):
    s = s.strip().replace(',', '')
    neg = s.startswith('(') and s.endswith(')')
    s = s.strip('()')
    try:
        v = float(s)
    except ValueError:
        return None
    return -v if neg else v


def first_num(line, skip=0):
    """First numeric token on a line, after skipping `skip` of them."""
    out = [num(m) for m in re.findall(NUM, line)]
    out = [v for v in out if v is not None]
    return out[skip] if len(out) > skip else None


def grab(txt, key, want, skip=0):
    """First line containing `key` inside the block starting at `want`."""
    i = txt.find(want)
    if i < 0:
        return None
    for line in txt[i:i + 1400].split('\n'):
        if key.lower() in line.lower():
            return first_num(line, skip)
    return None


def parse(tag, txt):
    q, yy = tag[1], tag[3:]
    head = f'Segment overview Q{q} 20{yy}'
    rev = grab(txt, 'Total revenues', head)
    adj = grab(txt, 'Adjusted EBITDA', head)
    if adj is None:
        adj = grab(txt, 'EBITDA', head)
    # volume block: the current quarter is the first numeric column
    vu = vn = None
    m = re.search(r'Own Product\b', txt)
    if m:
        blk = txt[m.start():m.start() + 900].split('\n')
        for line in blk:
            s = line.strip()
            if re.match(r'^Urea\b', s) and vu is None:
                vu = first_num(s)
            elif re.match(r'^Ammonia\b', s) and vn is None:
                vn = first_num(s)
    bu = bn = None
    for line in txt.split('\n'):
        if 'Granular Urea' in line and 'Egypt' in line and bu is None:
            bu = first_num(line)
        if line.strip().startswith('Ammonia') and 'Middle East' in line and bn is None:
            bn = first_num(line)
    return dict(period=LABEL[tag], rev_own=rev, ebitda_own=adj,
                vol_urea=vu, vol_nh3=vn, bm_urea=bu, bm_nh3=bn)


rows = []
for tag in ORDER:
    p = os.path.join(QDIR, f'{tag}.txt')
    if not os.path.exists(p):
        print(f'  MISSING {p}')
        continue
    r = parse(tag, open(p, errors='ignore').read())
    rows.append(r)

print(f"{'period':9s}{'rev_own':>9s}{'ebitda':>9s}{'urea kt':>9s}{'nh3 kt':>8s}"
      f"{'bm_urea':>9s}{'bm_nh3':>8s}{'px $/t':>9s}{'cost $/t':>10s}")
clean = []
for r in rows:
    miss = [k for k, v in r.items() if v is None]
    if miss:
        print(f"{r['period']:9s}  INCOMPLETE -> missing {miss}")
        continue
    vol = r['vol_urea'] + r['vol_nh3']
    r['vol_own'] = vol
    r['px'] = r['rev_own'] / vol * 1000
    r['cost_t'] = (r['rev_own'] - r['ebitda_own']) / vol * 1000
    r['bm_blend'] = (r['vol_urea'] * r['bm_urea'] + r['vol_nh3'] * r['bm_nh3']) / vol
    r['realisation'] = r['px'] / r['bm_blend']
    clean.append(r)
    print(f"{r['period']:9s}{r['rev_own']:9.1f}{r['ebitda_own']:9.1f}{r['vol_urea']:9.0f}"
          f"{r['vol_nh3']:8.0f}{r['bm_urea']:9.0f}{r['bm_nh3']:8.0f}{r['px']:9.1f}{r['cost_t']:10.1f}")

json.dump(clean, open(os.path.join(HERE, 'quarterly_units.json'), 'w'), indent=1)
print(f'\n{len(clean)} complete quarters -> quarterly_units.json')
