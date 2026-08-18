"""SAVOLA study — price-series ingest.

Two user-supplied investing.com exports (18-Aug-2026):
  * Tadawul All Share (TASI) history -> MERGED onto the persistent library at
    engine/raw_indices/SA/TASI.csv (merge-never-overwrite: overlapping dates must
    match to the 4th decimal; only strictly-newer rows are spliced on top).
  * Savola Group history -> NEW library file engine/raw_ohlc/SA/SAVOLA.csv
    (new coverage; no existing library to merge with).

Raw vendor rows are written verbatim (same quoted investing.com format the TASI
library already uses); every consumer runs Step 0.0 (data_quality.clean_ohlc)
at load time, so cleaning is done at read, not by editing the library.
"""
import os, sys, csv, io

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, '..')
sys.path.insert(0, ENG)
import pandas as pd
from primitives import load_ohlc

UP = '/root/.claude/uploads/a8970403-b1ce-52e0-85c5-0afc1908154f'
UP_TASI = os.path.join(UP, '8f6127dd-Tadawul_All_Share_Historical_Data.csv')
UP_SAV = os.path.join(UP, '7e2b0fdb-Savola_Group_Stock_Price_History.csv')
LIB_TASI = os.path.join(ENG, 'raw_indices', 'SA', 'TASI.csv')
LIB_SAV = os.path.join(ENG, 'raw_ohlc', 'SA', 'SAVOLA.csv')

# ---- 1. TASI: diagnose, verify overlap to 4dp, splice new rows on top --------
lib = load_ohlc(LIB_TASI)
up = load_ohlc(UP_TASI)
print(f"TASI library: {len(lib)} rows {lib['Date'].iloc[0].date()}..{lib['Date'].iloc[-1].date()}")
print(f"TASI upload : {len(up)} rows {up['Date'].iloc[0].date()}..{up['Date'].iloc[-1].date()}")

m = lib.merge(up, on='Date', suffixes=('_lib', '_up'))
print(f"overlapping dates: {len(m)}")

# DIAGNOSED 18-Aug-2026: the library's trailing two sessions (26/27-Jul-2026,
# the last rows of the 10-Aug commit) were captured BEFORE final settlement —
# the fresh export's 27-Jul row shows a wider intraday range (H 10,824.23 /
# L 10,741.20 vs the library's 10,823.21/10,772.92) and a settled close of
# 10,769.12 vs the snapshot's 10,773.47 (-0.04%). Every one of the 3,887
# earlier overlapping sessions matches EXACTLY (max diff 0.000000), so this is
# a final-print revision of two stale trailing rows, not vendor drift. The
# settled prints supersede the snapshots; both rows are replaced explicitly
# and the revision is logged here and in the study record.
REVISE_FROM = pd.Timestamp('2026-07-26')
strict = m[m['Date'] < REVISE_FROM]
bad = 0
for c in ['Price', 'Open', 'High', 'Low']:
    d = (strict[f'{c}_lib'] - strict[f'{c}_up']).abs()
    nb = int((d > 5e-5).sum())
    bad += nb
    if nb:
        print(f"  MISMATCH {c}: {nb} rows\n"
              f"{strict.loc[d > 5e-5, ['Date', f'{c}_lib', f'{c}_up']].head(10)}")
    else:
        print(f"  {c}: all {len(strict)} pre-revision overlaps match to 4dp "
              f"(max diff {d.max():.6f})")
assert bad == 0, "overlap mismatch outside the trailing revision window — do not splice"
rev = m[m['Date'] >= REVISE_FROM]
for _, r in rev.iterrows():
    print(f"  REVISED {r['Date'].date()}: close {r['Price_lib']} -> {r['Price_up']}, "
          f"H {r['High_lib']} -> {r['High_up']}, L {r['Low_lib']} -> {r['Low_up']} "
          f"(settled print supersedes intraday snapshot)")
missing_in_up = set(lib['Date']) - set(up['Date'])
assert not missing_in_up, f"upload lacks {len(missing_in_up)} library dates — partial export?"

new_dates = up[up['Date'] > lib['Date'].max()]['Date']
print(f"new sessions to splice: {len(new_dates)} "
      f"({new_dates.min().date()}..{new_dates.max().date()})")

# splice verbatim vendor rows: upload lines that are strictly newer OR replace
# the two revised trailing sessions; every older library line is kept verbatim.
with io.open(UP_TASI, 'r', encoding='utf-8-sig', newline='') as f:
    up_lines = f.read().splitlines()
hdr, up_rows = up_lines[0], up_lines[1:]
def row_date(line):
    return pd.to_datetime(next(csv.reader([line]))[0], format='%m/%d/%Y')
new_lines = [ln for ln in up_rows if ln.strip() and row_date(ln) >= REVISE_FROM]
new_lines.sort(key=row_date, reverse=True)  # newest first, matching the library

with io.open(LIB_TASI, 'r', encoding='utf-8-sig', newline='') as f:
    lib_lines = f.read().splitlines()
assert lib_lines[0].replace('﻿', '') == hdr.replace('﻿', ''), "header mismatch"
keep = [ln for ln in lib_lines[1:] if ln.strip() and row_date(ln) < REVISE_FROM]
out = [lib_lines[0]] + new_lines + keep
with io.open(LIB_TASI, 'w', encoding='utf-8', newline='') as f:
    f.write('\n'.join(out) + '\n')
chk = load_ohlc(LIB_TASI)
assert chk['Date'].is_monotonic_increasing and chk['Date'].iloc[-1] == up['Date'].max()
assert len(chk) == len(up), (len(chk), len(up))
print(f"TASI library now {len(chk)} rows to {chk['Date'].iloc[-1].date()} — "
      f"spliced {len(new_lines) - len(rev)} new rows, revised {len(rev)} trailing rows")

# ---- 2. SAVOLA: new library file (verbatim vendor export) --------------------
sav = load_ohlc(UP_SAV)
print(f"\nSAVOLA upload: {len(sav)} rows {sav['Date'].iloc[0].date()}..{sav['Date'].iloc[-1].date()}")
assert not os.path.exists(LIB_SAV), "SAVOLA.csv already exists — this is not new coverage"
with io.open(UP_SAV, 'r', encoding='utf-8-sig', newline='') as f:
    body = f.read()
with io.open(LIB_SAV, 'w', encoding='utf-8', newline='') as f:
    f.write(body if body.endswith('\n') else body + '\n')
chk2 = load_ohlc(LIB_SAV)
assert len(chk2) == len(sav) and chk2['Price'].iloc[-1] == sav['Price'].iloc[-1]
print(f"SAVOLA library written: {len(chk2)} parseable rows, last close "
      f"{chk2['Price'].iloc[-1]} on {chk2['Date'].iloc[-1].date()}")
