#!/usr/bin/env python3
"""SCEM walk-forward — the corrections, under BOTH clauses.

CLAUSE ONE  the bias holds its sign AT EVERY CUT THE DATA ADMITS
            [R-FCAL-01 AMENDED 07-09-2026], every boundary leaving at least five
            cells on each side.
CLAUSE TWO  the correction is consistent with how that driver class is built across
            the market's book.

THIS RUN PROMOTES NOTHING, AND THAT WAS PRE-REGISTERED BEFORE ANY ERROR WAS COMPUTED.
Nine resolved cells spread over four target years admit NO boundary leaving five cells
each side, so every driver here is UNTESTABLE for stability rather than stable — an
absence of contrary evidence is not evidence [R-ENF-04]. Every candidate below is
therefore a WATCH FLAG: recorded, graded live, revisited at the next update, acted on
by nobody.

The candidates are still measured and still tested adjusted-versus-raw, because the
point of recording them is that the FY2026 filing adds an origin and the question can
be asked again on a thicker panel.
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

HALF_STRENGTH = 0.5


def expanding_corrections(cells, driver):
    """Expanding window only: at each origin the correction uses ONLY errors that had
    already resolved by then. Half strength by default."""
    rows = sorted([c for c in cells
                   if c['driver'] == driver and c.get('scale') == 'log'],
                  key=lambda c: (c['origin'], c['h']))
    out = {}
    for o in P.YEARS:
        prior = [c['log_error'] for c in rows
                 if c['year'] <= int(o[2:])]      # resolved BEFORE standing at o
        if len(prior) < 2:
            out[o] = dict(n_prior=len(prior), factor=None,
                          why="fewer than two resolved errors existed at this origin, "
                              "so no expanding-window correction is computable")
            continue
        bias = sum(prior) / len(prior)
        out[o] = dict(n_prior=len(prior), bias=bias,
                      factor=math.exp(-HALF_STRENGTH * bias),
                      strength=HALF_STRENGTH)
    return out


def adjusted_vs_raw(cells, driver):
    """Apply each origin's own expanding-window factor and see whether the error falls."""
    corr = expanding_corrections(cells, driver)
    rows = [c for c in cells if c['driver'] == driver and c.get('scale') == 'log']
    raw, adj, by_origin = [], [], {}
    for c in rows:
        f = corr.get(c['origin'], {}).get('factor')
        if f is None:
            continue
        e_raw = c['log_error']
        e_adj = e_raw + math.log(f)
        raw.append(abs(e_raw))
        adj.append(abs(e_adj))
        by_origin.setdefault(c['origin'], {'raw': [], 'adj': []})
        by_origin[c['origin']]['raw'].append(abs(e_raw))
        by_origin[c['origin']]['adj'].append(abs(e_adj))
    if not raw:
        return None
    return dict(n=len(raw), mae_raw=sum(raw) / len(raw), mae_adjusted=sum(adj) / len(adj),
                improves=sum(adj) < sum(raw),
                by_origin={o: dict(mae_raw=sum(v['raw']) / len(v['raw']),
                                   mae_adjusted=sum(v['adj']) / len(v['adj']),
                                   improves=sum(v['adj']) < sum(v['raw']))
                           for o, v in by_origin.items()},
                factors={o: v.get('factor') for o, v in corr.items()})


CLAUSE_TWO = {
    "revenue": "The house builds revenue as volume x price from an exogenous anchor. A "
               "multiplier on revenue is not how that driver is built anywhere in this "
               "book, and on this name the residual is the ACTIVITY ANCHOR ITSELF "
               "missing — Egyptian real GDP growth is not Egyptian cement demand, which "
               "rose 13.4% in 2025 while GDP grew about 4%. That is a specification "
               "question, not a calibration one, and no correction factor may hide it.",
    "materials": "One escalator per driver class is the house rule (L-009, L-110): fuel "
                 "and imported inputs follow their own commodity path, not domestic "
                 "inflation. This issuer does not split the line, so the right answer is "
                 "the disclosure gap, not a multiplier on the blend.",
    "ga": "Overheads are built fixed-plus-variable everywhere in the book. A blanket "
          "uplift on G&A would be consistent with nothing.",
    "capex": "L-063 and L-275 both say the recent capital-spending run rate is a "
             "CEILING or a deferral rather than a central estimate on an old plant. A "
             "multiplier on the run rate points the other way from the class finding.",
    "cogs_wages": "Consistent in shape with how wages are built elsewhere (fixed in "
                  "real terms), so a level correction here would be admissible IF it "
                  "ever passed clause one.",
    "cogs_maintenance": "Same as wages in shape. Admissible on clause two, and it is "
                        "clause one that refuses it here.",
    "finance_expense": "The house builds interest from named facilities at their own "
                       "rates. The miss here is that DEBT WAS REPAID, not that the rate "
                       "was wrong — a correction would be calibrating away a financing "
                       "decision the model held flat by design.",
    "interest_income": "L-057 already says interest income is a balance times a rate "
                       "and holding either flat cannot track it. The fix is the balance "
                       "path, which is a specification, not a factor.",
    "transport": "L-120, a CLASS lesson, says haulage follows the EXPORT tonne and a "
                 "cost per despatched tonne misprices it. This issuer discloses no "
                 "tonne at all, so the class fix is not even expressible here.",
    "working_capital": "Working capital is built from the disclosed cycle everywhere. A "
                       "multiplier is not that.",
    "dna": "Built off a disclosed rate and a roll-forward, and its bias is -0.025 log, "
           "which is nothing.",
    "ebitda": "An AGGREGATE. Corrections are applied to drivers and aggregates are "
              "rebuilt from them; correcting an aggregate directly is forbidden.",
    "pat": "An AGGREGATE, and the same refusal.",
}


if __name__ == '__main__':
    P.verify()
    cells = json.load(open(os.path.join(HERE, 'error_cells.json')))
    by = collections.defaultdict(list)
    for c in cells:
        if c.get('scale') == 'log' and c.get('log_error') is not None:
            by[c['driver']].append((c['year'], c['log_error']))

    log = {"_rule": "[R-FCAL-01] expanding window only, half strength by default, "
                    "applied only where the bias holds its sign at EVERY cut the data "
                    "admits, and consistent with how the driver class is built across "
                    "the market's book.",
           "_pre_registered_expectation": "PRE_REGISTRATION_07-09-2026.md section 6 "
                                          "states, before any error was computed, that "
                                          "nine cells admit no cut leaving five each "
                                          "side, so nothing can be promoted from this "
                                          "run whatever the biases turn out to be.",
           "half_strength": HALF_STRENGTH, "candidates": {}}

    print('%-18s %3s %7s %6s %10s %10s %9s  %s'
          % ('driver', 'n', 'bias', 'cuts', 'MAE raw', 'MAE adj', 'better?', 'verdict'))
    for k in sorted(by):
        v = by[k]
        bias = sum(e for _, e in v) / len(v)
        cuts, flipped = BSEN.cuts_for(v)
        av = adjusted_vs_raw(cells, k)
        clause_one = bool(cuts) and not flipped
        aggregate = k in ('ebitda', 'pat')
        verdict = ('REFUSED — an aggregate; corrections apply to drivers'
                   if aggregate else
                   'WATCH FLAG — clause one UNTESTABLE at %d cells' % len(v)
                   if not cuts else
                   'WATCH FLAG — the sign flips at %d of %d cuts' % (len(flipped), len(cuts))
                   if flipped else 'clause one PASSES')
        log['candidates'][k] = dict(
            n=len(v), bias=bias, admissible_cuts=len(cuts), flips=len(flipped),
            clause_one=clause_one,
            clause_one_reason=("no boundary leaves %d cells on both sides — UNTESTABLE, "
                               "never counted stable" % BSEN.MIN_SIDE) if not cuts
            else ("stable at every admissible cut" if not flipped
                  else "the sign depends on where the line is drawn"),
            clause_two=CLAUSE_TWO.get(k, ''),
            adjusted_vs_raw=av,
            promoted=False,
            disposition='watch_flag' if not aggregate else 'refused',
            verdict=verdict)
        print('%-18s %3d %+7.3f %6d %10s %10s %9s  %s'
              % (k, len(v), bias, len(cuts),
                 '%.3f' % av['mae_raw'] if av else '-',
                 '%.3f' % av['mae_adjusted'] if av else '-',
                 ('yes' if av['improves'] else 'no') if av else '-',
                 verdict[:44]))
    log['promoted'] = []
    log['summary'] = ("%d candidates measured, 0 promoted, %d recorded as watch flags, "
                      "%d refused as aggregates. Nothing from this run enters the live "
                      "drivers."
                      % (len(log['candidates']),
                         sum(1 for v in log['candidates'].values()
                             if v['disposition'] == 'watch_flag'),
                         sum(1 for v in log['candidates'].values()
                             if v['disposition'] == 'refused')))
    log['guidance_ledger'] = {
        "entries": [],
        "note": "EMPTY, and that is a finding rather than an omission. Sinai Cement "
                "publishes no forward guidance, no results presentation and no earnings "
                "call in any of its six filings or on its own website — the prior "
                "study's sweep logged that as a negative search and this run confirms "
                "it. So the guidance-is-scored-never-consumed clause has nothing to "
                "score here, and no driver in this model can have inherited a "
                "management lean, because there is no management forward number to "
                "inherit."}
    json.dump(log, open(os.path.join(HERE, 'corrections_log.json'), 'w'), indent=1)
    print('\n' + log['summary'])
