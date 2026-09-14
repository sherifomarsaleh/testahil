#!/usr/bin/env python3
"""SCEM walk-forward — the forward ranges the delivered study publishes.

[R-FCAL-01] YEARS 3-5 ARE PUBLISHED AS RANGES FROM THIS RECORD'S OWN DRIVER-ERROR
DISTRIBUTION, NEVER AS POINTS.

[R-FCAL-01 AMENDED 07-09-2026] A PUBLISHED BAND DECLARES ITS BASIS, ITS COUNT AND ITS
ORIENTATION, in the file rather than in a note. Five runs published bands in five
incompatible shapes and one of them ran the other way up from the other two with no
declaration anywhere; a reciprocal is the most dangerous kind of unit error, because
0.4 and 2.5 are each an ordinary thing to read in a band.

  BASIS        `span` — the range of the observations themselves. NOT a percentile:
               with four, three and two observations at horizons one, two and three, a
               p10-p90 would be a free parameter dressed as a statistic.
  COUNT        stated per driver per horizon, always.
  ORIENTATION  `actual_over_forecast`. MULTIPLY a point projection by the band to get
               the range this record supports for the outturn. A band above 1.0 means
               this method forecast BELOW what the company reported.

WHAT THIS RECORD CANNOT SUPPORT, stated rather than left to be assumed: horizons FOUR
and FIVE. Five sourceable fiscal years give a longest resolved horizon of three, so the
study's FY2029 and FY2030 have NO BAND from this record and must say so in those words
rather than borrowing the three-year band and calling it five.
"""
import collections
import json
import math
import os

import panel as P

HERE = os.path.dirname(os.path.abspath(__file__))

BASIS = "span"
ORIENTATION = "actual_over_forecast"
PUBLISHABLE = ("revenue", "materials", "cogs_wages", "cogs_maintenance", "transport",
               "ga", "dna", "capex")


def build():
    cells = json.load(open(os.path.join(HERE, 'error_cells.json')))
    by = collections.defaultdict(list)
    for c in cells:
        if c.get('scale') == 'log' and c.get('log_error') is not None:
            by[(c['driver'], c['h'])].append(c)
    out = {}
    for (k, h), rows in sorted(by.items()):
        # actual/forecast = exp(-log_error)
        mult = sorted(math.exp(-r['log_error']) for r in rows)
        out.setdefault(k, {})[str(h)] = dict(
            low=mult[0], high=mult[-1], central=math.exp(-sum(
                r['log_error'] for r in rows) / len(rows)),
            n=len(mult), basis=BASIS, orientation=ORIENTATION,
            observations=[dict(origin=r['origin'], target='FY%d' % r['year'],
                               multiplier=math.exp(-r['log_error'])) for r in rows],
            publishable=k in PUBLISHABLE)
    return out


if __name__ == '__main__':
    P.verify()
    bands = build()
    rec = {
        "_rule": "[R-FCAL-01] years 3-5 as RANGES from this record's own driver-error "
                 "distribution, never as points. [AMENDED 07-09-2026] the band declares "
                 "its basis, its count and its orientation.",
        "basis": BASIS,
        "basis_reason": "four, three and two observations at horizons one, two and "
                        "three. A percentile on two observations is not a percentile, "
                        "and calling a span one would be the free parameter the "
                        "promotion rule forbids.",
        "orientation": ORIENTATION,
        "orientation_reason": "MULTIPLY a point projection by the band. A band above "
                              "1.0 means the method forecast BELOW the outturn, which "
                              "is the direction every driver in this record ran except "
                              "finance expense.",
        "horizons_available": [1, 2, 3],
        "horizons_not_available": {
            "4": "NO BAND. Five sourceable fiscal years give a longest resolved horizon "
                 "of three; the study's FY2029 must say so rather than borrow the "
                 "three-year band.",
            "5": "NO BAND, same reason, for FY2030."},
        "bands": bands,
        "caveat": "Every band here rests on between two and four observations of a "
                  "company that went from a loss of EGP 345mn to a profit of EGP 3.07bn "
                  "in three years while its currency lost most of its value. The bands "
                  "are wide because the record is thin and the period was extreme, and "
                  "narrowing them would be inventing precision this panel cannot carry.",
    }
    json.dump(rec, open(os.path.join(HERE, 'forward_ranges.json'), 'w'), indent=1)
    print('FORWARD BANDS — basis %s, orientation %s (multiply a point projection)\n'
          % (BASIS, ORIENTATION))
    print('%-18s %-4s %3s %9s %9s %9s' % ('driver', 'h', 'n', 'low', 'central', 'high'))
    for k in sorted(bands):
        for h in ('1', '2', '3'):
            if h not in bands[k]:
                continue
            b = bands[k][h]
            print('%-18s h=%-2s %3d %9.3f %9.3f %9.3f%s'
                  % (k, h, b['n'], b['low'], b['central'], b['high'],
                     '' if b['publishable'] else '   (aggregate — rebuilt, not banded)'))
