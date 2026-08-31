"""density_screen.py — trading-day density against each exchange's real calendar.

The protocol carries this as a STANDING RULE — "screen a market's trading-day
density against that exchange's REAL calendar before trusting any fit built on
it" — and nothing in the repo executes it. Step 0.0 strips only a LEADING block
of placeholder rows, so a name whose sparse years are INTERLEAVED with real ones
passes cleanly: IHC has 27 sessions in 2011 (88.9% of them flat bars) and 252 in
2024, and every gate reports it clean.

THE REFERENCE CALENDAR IS MEASURED, NOT ASSUMED. For each market and year the
denominator is the union of dates across every library in that market — the
exchange's real sessions as this repo actually observed them, so a market-wide
holiday is not counted against a name. Markets with a single library have no
independent denominator and are reported as such rather than scored against
themselves.

TWO READINGS, AND THEY ARE NOT THE SAME DEFECT — the first cut of this screen
combined them with an OR and flagged 37 names, most of them for nothing:

  density  — sessions present / market sessions that year. LOW DENSITY IS
             USUALLY BENIGN. A name that listed in October has a first year at
             0.12 and there is nothing wrong with it; ADNOCDIST 2017, SALIK
             2022 and LULU 2024 all read 0.05-0.25 with every bar trading. So
             density is scored ONLY on a name's INTERIOR years — never its
             first or last, which are partial by construction.
  liveness — share of present bars that actually traded (High > Low). THIS is
             the reading that matters: a bar with no range is a non-trading day
             wearing a session's clothes, and unlike a missing bar it enters
             every window, every pivot and every volatility estimate as a real
             observation of zero movement.

A screen that fires on every IPO is one everybody learns to ignore, which is the
failure mode this repository has already recorded twice.

No threshold here is a gate. This is a diagnostic that says which names carry
years a fit should not rest on; turning any cut into a gate needs the promotion
rule and its own evidence.
"""
import os, sys, glob, json
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.abspath(os.path.join(HERE, '..', '..', 'raw_ohlc'))

THIN_DENSITY = 0.60      # reported, not enforced
THIN_LIVENESS = 0.70


def load(path):
    d = pd.read_csv(path)
    d.columns = [c.strip().strip('"').lstrip('﻿') for c in d.columns]
    d['dt'] = pd.to_datetime(d['Date'], format='%m/%d/%Y', errors='coerce')
    for c in ('Price', 'High', 'Low'):
        d[c] = pd.to_numeric(d[c].astype(str).str.replace(',', ''), errors='coerce')
    return d.dropna(subset=['dt']).sort_values('dt').reset_index(drop=True)


def main():
    books, rows = {}, []
    for mkt in sorted(os.listdir(RAW)):
        files = sorted(glob.glob(os.path.join(RAW, mkt, '*.csv')))
        if not files:
            continue
        books[mkt] = {os.path.basename(f)[:-4]: load(f) for f in files}

    total = sum(len(v) for v in books.values())
    for mkt, names in books.items():
        # the market's real calendar: the union of every library's dates
        cal = pd.Series(sorted(set().union(*[set(d.dt) for d in names.values()])))
        cal_year = cal.groupby(cal.dt.year).size()
        solo = len(names) == 1
        for tkr, d in names.items():
            yrs = sorted(d.dt.dt.year.unique())
            edge = {yrs[0], yrs[-1]}          # partial by construction, not by defect
            for yr, g in d.groupby(d.dt.dt.year):
                denom = int(cal_year.get(yr, 0))
                if not denom:
                    continue
                rows.append(dict(market=mkt, ticker=tkr, year=int(yr), n=int(len(g)),
                                 market_sessions=denom,
                                 density=float(len(g) / denom),
                                 liveness=float((g.High > g.Low).mean()),
                                 median_px=float(g.Price.median()), solo_market=solo,
                                 edge_year=bool(yr in edge)))
    r = pd.DataFrame(rows)
    r.to_csv(os.path.join(HERE, 'density_screen.csv'), index=False)

    scored = r[~r.solo_market]
    interior = scored[~scored.edge_year]
    print(f"libraries screened: {total} | markets: {len(books)} | name-years: {len(r)}")
    print(f"single-library markets, no independent denominator: "
          f"{sorted(r[r.solo_market].market.unique())}")
    print(f"interior name-years (first/last excluded as partial): {len(interior)}\n")

    dead = interior[interior.liveness < THIN_LIVENESS]
    gappy = interior[interior.density < THIN_DENSITY]
    print(f"=== DEAD BARS — liveness < {THIN_LIVENESS:.0%} (the reading that matters) ===")
    print(f"{len(dead)} interior name-years across "
          f"{len(dead.groupby(['market','ticker']))} names\n")
    span = interior.groupby(['market', 'ticker']).year.nunique().rename('interior_years')
    a = dead.groupby(['market', 'ticker']).agg(
        bad_years=('year', 'size'), first=('year', 'min'), last=('year', 'max'),
        worst_liveness=('liveness', 'min'), worst_density=('density', 'min')).join(span)
    a['share'] = a.bad_years / a.interior_years
    print(a.sort_values('share', ascending=False).to_string(float_format=lambda x: f'{x:.3f}'))

    print(f"\n=== MISSING BARS — interior density < {THIN_DENSITY:.0%} ===")
    if len(gappy):
        print(gappy[['market', 'ticker', 'year', 'n', 'market_sessions', 'density',
                     'liveness']].sort_values('density')
              .to_string(index=False, float_format=lambda x: f'{x:.3f}'))
    else:
        print("none — every interior year carries a full complement of sessions.")

    json.dump({'screened': total, 'name_years': len(r), 'interior_name_years': len(interior),
               'dead_bar_name_years': int(len(dead)),
               'names_with_dead_bars': int(len(a)),
               'names': {f'{m}/{t}': dict(bad_years=int(v.bad_years), first=int(v.first),
                                          last=int(v.last),
                                          worst_liveness=float(v.worst_liveness),
                                          share_of_interior=float(v.share))
                         for (m, t), v in a.iterrows()}},
              open(os.path.join(HERE, 'density_screen.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
