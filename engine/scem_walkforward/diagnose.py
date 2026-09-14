#!/usr/bin/env python3
"""SCEM walk-forward — diagnosis: the side-by-side statements, the one-offs, the
decomposition of the revenue and profit errors, and the cut-invariance test.

THE CUT-INVARIANCE TEST IS RUN THROUGH THE SHARED INSTRUMENT [R-ENF-03], never
reimplemented: a checker that models a measurement is checking a different measurement.
"""
import collections
import json
import math
import os
import sys

import bottom_up as BU
import panel as P

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'valuation_calibration'))
import boundary_sensitivity as BSEN     # noqa: E402

ONE_OFFS = {
    "FY2024": [dict(line="gain on sale of investments", value=1_517_386_642,
                    what="the disposal of the 25.40% holding in Sinai White Portland "
                         "Cement to Aalborg Portland Holding, completed 13 August 2024",
                    share_of_pbt=1_517_386_642 / 3_150_036_485,
                    treatment="EXCLUDED from every driver rule and from the profit the "
                              "drivers rebuild. A model that cannot foresee a stake "
                              "sale should not be scored as though it should have.")],
    "FY2025": [dict(line="provisions other than depreciation", value=-28_192_283,
                    what="a NET RELEASE of provisions, the only year in the panel where "
                         "this line is negative",
                    share_of_pbt=-28_192_283 / 3_358_865_272,
                    treatment="left in. It is inside the cost base the drivers rebuild "
                              "and is small (0.8% of pre-tax profit); removing it "
                              "would be a judgement at a historical origin.")],
    "FY2023": [dict(line="change in inventory inside cost of sales", value=138_243_904,
                    what="the coal stock pricing policy changed from first-in-first-out "
                         "to weighted average, which note 3/8 states 'resulted in the "
                         "company incurring losses, and those losses were charged to "
                         "the income statement'",
                    share_of_pbt=None,
                    treatment="left in and RECORDED. It is a genuine change of "
                              "accounting policy inside cost of sales, disclosed by the "
                              "company itself, and it falls in the cost note that foots "
                              "to the face of the profit and loss account.")],
}


def side_by_side():
    lines = ["# SCEM — projected versus actual income statement, EVERY origin",
             "",
             "Internal. EGP millions. The model is the mechanical one pre-registered on "
             "7 September 2026; no judgement driver stands at any origin.",
             ""]
    for o in P.YEARS:
        proj = BU.project(o)
        lines.append("## Origin %s" % o)
        lines.append("")
        d = P.derived()[o]
        lines.append("Standing at %s the model saw revenue of EGP %.1fmn, EBITDA of EGP "
                     "%.1fmn, interest-bearing debt of EGP %.1fmn at a realised rate of "
                     "%s on the borrowings that actually bear it, and cash of EGP "
                     "%.1fmn."
                     % (o, d['revenue'], d['ebitda'], d['interest_bearing_debt'],
                        ('%.2f%%' % (100 * d['kd_on_borrowings']))
                        if d.get('kd_on_borrowings') else 'its own first-year figure',
                        d['cash']))
        lines.append("")
        for h in (1, 2, 3):
            p = proj.get(h)
            if p is None:
                continue
            a = BU.actual(p['year'])
            lines.append("**h=%d → FY%d**%s" % (h, p['year'],
                                                "" if a else "  (not yet matured)"))
            lines.append("")
            lines.append("| line | projected | actual | error |")
            lines.append("|---|---:|---:|---:|")
            rows = [("Revenue", 'revenue'), ("Materials, fuel, power, packing", 'materials'),
                    ("Cost-of-sales wages", 'cogs_wages'),
                    ("Cost-of-sales maintenance", 'cogs_maintenance'),
                    ("Transfer and loading", 'transport'),
                    ("General and administrative", 'ga'),
                    ("EBITDA", 'ebitda'),
                    ("Depreciation and amortisation", 'dna'),
                    ("Finance expense", 'finance_expense'),
                    ("Interest income", 'interest_income'),
                    ("Net profit after tax", 'pat')]
            for label, k in rows:
                pv = p.get(k)
                av = a.get(k) if a else None
                if av is None:
                    lines.append("| %s | %.1f | — | — |" % (label, pv))
                elif pv > 0 and av > 0:
                    lines.append("| %s | %.1f | %.1f | %+.3f log |"
                                 % (label, pv, av, math.log(pv / av)))
                else:
                    lines.append("| %s | %.1f | %.1f | %+.1f%% |"
                                 % (label, pv, av, 100 * (pv - av) / abs(av) if av else 0))
            if a and 'pat_ex_oneoff' in a and abs(a['pat_ex_oneoff'] - a['pat']) > 1:
                lines.append("| *Net profit excluding the FY2024 disposal* | %.1f | %.1f | |"
                             % (p['pat'], a['pat_ex_oneoff']))
            lines.append("")
        lines.append("")
    return "\n".join(lines)


def decompose():
    """Where the revenue and the profit miss actually came from."""
    out = {}
    for o in P.YEARS:
        proj = BU.project(o)
        for h in (1, 2, 3):
            p = proj.get(h)
            if p is None:
                continue
            a = BU.actual(p['year'])
            if a is None:
                continue
            key = "%s h=%d" % (o, h)
            # revenue: the two exogenous legs against the outturn revenue
            vol_leg = math.log(p['V'])
            price_leg = math.log(p['P'])
            total = math.log(p['revenue'] / a['revenue'])
            out[key] = dict(
                revenue_log_error=total,
                from_activity_anchor=vol_leg,
                from_price_anchor=price_leg,
                residual_company=total - vol_leg - price_leg,
                note="the residual is what the company did that the two exogenous "
                     "anchors cannot explain; it is exactly zero by construction only "
                     "if the origin's own base year is the actual base year, which it "
                     "is, so the residual IS the anchors' joint miss",
                ebitda_projected=p['ebitda'], ebitda_actual=a['ebitda'],
                pat_projected=p['pat'], pat_actual=a['pat'])
    return out


def cut_invariance():
    cells = json.load(open(os.path.join(HERE, 'error_cells.json')))
    by = collections.defaultdict(list)
    for c in cells:
        if c.get('scale') == 'log' and c.get('log_error') is not None:
            by[c['driver']].append((c['year'], c['log_error']))
    out = {}
    for k, v in sorted(by.items()):
        cuts, flipped = BSEN.cuts_for(v)
        out[k] = dict(n=len(v), admissible_cuts=len(cuts), flips=len(flipped),
                      cuts=[[b, a, c] for b, a, c in cuts],
                      verdict=("UNTESTABLE — no boundary leaves %d cells on both sides, "
                               "so this driver is too thin to cut and is never counted "
                               "stable: an absence of contrary evidence is not evidence "
                               "[R-ENF-04]" % BSEN.MIN_SIDE) if not cuts else
                              ("STABLE at every admissible cut" if not flipped else
                               "FLIPS at %d of %d cuts — instability, reported and never "
                               "corrected for" % (len(flipped), len(cuts))))
    return out


if __name__ == '__main__':
    P.verify()
    open(os.path.join(HERE, 'scem_IS_projected_vs_actual_all_origins.md'),
         'w').write(side_by_side())
    rec = dict(one_offs=ONE_OFFS, decomposition=decompose(),
               cut_invariance=cut_invariance(), min_side=BSEN.MIN_SIDE)
    json.dump(rec, open(os.path.join(HERE, 'diagnostics.json'), 'w'), indent=1)
    print('side-by-side income statements written for %d origins' % len(P.YEARS))
    print('\nCUT-INVARIANCE [R-FCAL-01 AMENDED 07-09-2026], through the shared '
          'instrument at MIN_SIDE=%d\n' % BSEN.MIN_SIDE)
    for k, v in sorted(rec['cut_invariance'].items()):
        print('  %-18s n=%-3d cuts=%-2d  %s' % (k, v['n'], v['admissible_cuts'],
                                                v['verdict'][:70]))
    print('\nREVENUE ERROR DECOMPOSED\n')
    print('%-14s %10s %10s %10s %12s' % ('cell', 'total', 'activity', 'price', 'residual'))
    for k, v in sorted(rec['decomposition'].items()):
        print('%-14s %+10.3f %+10.3f %+10.3f %+12.3f'
              % (k, v['revenue_log_error'], v['from_activity_anchor'],
                 v['from_price_anchor'], v['residual_company']))
