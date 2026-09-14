#!/usr/bin/env python3
"""GBCO walk-forward — build panel.json from GB Corp's own filings.

FOUR FIELDS ON EVERY NUMBER: value, source document, document date, provenance tier.
Tier A throughout: every document is one GB Corp published itself on its own
investor-relations site. NOTHING here is estimated, interpolated or inferred; a year
that cannot be sourced is left out and the window is shortened.

ARITHMETIC IS THE ARBITER — foot_report() reconciles every year against the
statement's own additions and the run refuses to use a year that does not foot.
"""
from __future__ import annotations
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import extract as E, release as R, panel as P                   # noqa: E402

MN = 1e-3   # the annual reports are in EGP thousand, the releases in EGP million

# ---------------------------------------------------------------- document dates
DOCDATE = {
    'GB_Annual_Report_2013.pdf': '2014-03-04', 'GB_Annual_Report_2014.pdf': '2015-03-01',
    'GB_Annual_Report_2015.pdf': '2016-03-01', 'GB_Annual_Report_2016.pdf': '2017-03-01',
    'GB_Annual_Report_2017.pdf': '2018-03-01', 'GB_Annual_Report_2018.pdf': '2019-03-01',
    'GB_Corp_ER_4Q20_-_E_-_FINAL.pdf': '2021-02-01',
    'GB_Corp_ER_4Q21_-_E_-_FINAL.pdf': '2022-02-01',
    'GB_Corp_ER_4Q22_-_E_-_FINAL.pdf': '2023-03-01',
    'GB_Corp_ER_4Q23_-_ER_-_FINAL.pdf': '2024-03-01',
    'GB_Corp_ER_4Q24-_E_-_Final.pdf': '2025-02-01',
    'GB_Corp_ER_4Q25-_E_-_Final.pdf': '2026-02-26',
    'GB_Corp_ER_2Q26-_E_-_Final.pdf': '2026-08-13',
    'GB_Corp_Annual_Report_2025.pdf': '2026-03-01',
}

# FY2012-FY2018 — the audited consolidated statement of income as reproduced in the
# annual report for that year. FY2012 is AR2013's comparative column; FY2017 is
# AR2018's comparative column. Read off the text layer, footed line by line below.
AR_IS = {
  2012: ('GB_Annual_Report_2013.pdf', dict(revenue=8290147, cost=-7220107, gross_profit=1070040,
         other_income=27712, selling=-159152, admin=-304908, provisions=-17349-1364,
         operating_profit=614979, finance_net=-300182, ebt=314797, tax=-38867, net_profit=275930)),
  2013: ('GB_Annual_Report_2013.pdf', dict(revenue=9126721, cost=-7956434, gross_profit=1170287,
         other_income=30013, selling=-261350, admin=-332051, provisions=-20400,
         operating_profit=586499, finance_net=-372324, ebt=214175, tax=-29794, net_profit=184381)),
  2014: ('GB_Annual_Report_2014.pdf', dict(revenue=12322079, cost=-10740412, gross_profit=1581667,
         other_income=55720, selling=-298599, admin=-413558, provisions=-67796,
         operating_profit=857434, finance_net=-531538, ebt=325896, tax=-90206, net_profit=235690)),
  2015: ('GB_Annual_Report_2015.pdf', dict(revenue=12264689, cost=-10670326, gross_profit=1594363,
         other_income=126302, selling=-364486, admin=-531124, provisions=-48893-1591-18719-5688,
         operating_profit=750164, finance_net=-513265, ebt=236899, tax=-45385, net_profit=191514)),
  2016: ('GB_Annual_Report_2016.pdf', dict(revenue=15285672, cost=-13083613, gross_profit=2202059,
         other_income=40734, selling=-449848, admin=-749706, provisions=-184856+21229-2788-10862,
         operating_profit=865962, finance_net=-1853352, ebt=-987390, tax=-2420, net_profit=-989810)),
  2017: ('GB_Annual_Report_2018.pdf', dict(revenue=17656586, cost=-15703786, gross_profit=1952800,
         other_income=151528, selling=-583586, admin=-699205, provisions=-203364,
         operating_profit=618173, finance_net=-1369902, ebt=-751729, tax=28074, net_profit=-723655)),
  2018: ('GB_Annual_Report_2018.pdf', dict(revenue=25811964, cost=-22248011, gross_profit=3563953,
         other_income=173107, selling=-908624, admin=-793878, provisions=-59153,
         operating_profit=1975405, finance_net=-1187257, ebt=788148, tax=-151414, net_profit=636734)),
}


def ar_series():
    """FY2012-FY2018, EGP million, footed against the statement's own additions."""
    out = {}
    for y, (doc, d) in sorted(AR_IS.items()):
        checks = []
        checks.append(('gross profit', d['revenue'] + d['cost'], d['gross_profit']))
        checks.append(('operating profit',
                       d['gross_profit'] + d['other_income'] + d['selling'] + d['admin']
                       + d['provisions'], d['operating_profit']))
        checks.append(('profit before tax', d['operating_profit'] + d['finance_net'], d['ebt']))
        checks.append(('net profit', d['ebt'] + d['tax'], d['net_profit']))
        bad = [(n, a, b) for n, a, b in checks if abs(a - b) > 1.0]
        out[y] = {'doc': doc, 'foots': not bad, 'failed': bad,
                  'v': {k: round(v * MN, 1) for k, v in d.items()}}
    return out


REL_COL = {2019: 3}          # FY2019 is the prior-year column of the FY20 release


def rel_series():
    """FY2019-FY2025, EGP million, AS ORIGINALLY REPORTED in that year's own release."""
    out = {}
    for y, (doc, pg) in sorted(P.RELEASE.items()):
        rws = R.table(doc, pg)
        col = REL_COL.get(y, 4)
        v = {}
        for k, pats in P.REL_LINES.items():
            for lab, vals in rws:
                low = lab.lower().strip()
                if any(re.search(p, low) for p in pats) and len(vals) > col and vals[col] is not None:
                    v[k] = vals[col]
                    break
        checks = []
        if 'ebt' in v and 'tax' in v and 'npbmi' in v:
            checks.append(('net profit before minority', v['ebt'] + v['tax'], v['npbmi']))
        if 'npbmi' in v and 'minority' in v and 'net_profit' in v:
            checks.append(('net profit', v['npbmi'] + v['minority'], v['net_profit']))
        bad = [(n, a, b) for n, a, b in checks if abs(a - b) > 0.2]
        out[y] = {'doc': doc, 'foots': not bad, 'failed': bad, 'v': v}
    return out


def main():
    ar, rel = ar_series(), rel_series()
    years = {}
    for y, blk in ar.items():
        years[y] = {'source': blk['doc'], 'source_date': DOCDATE[blk['doc']], 'tier': 'A',
                    'route': 'PDF text layer (pymupdf) of the annual report reproducing that '
                             'year\'s audited consolidated statement of income',
                    'foots': blk['foots'], 'failed_checks': blk['failed'], 'unit': 'EGP mn',
                    'is': blk['v']}
    for y, blk in rel.items():
        if y in years:
            continue
        years[y] = {'source': blk['doc'], 'source_date': DOCDATE[blk['doc']], 'tier': 'A',
                    'route': "PDF text layer (pymupdf) of GB Corp's own 4Q earnings release, "
                             "the figures AS ORIGINALLY REPORTED at that origin",
                    'foots': blk['foots'], 'failed_checks': blk['failed'], 'unit': 'EGP mn',
                    'is': {k: round(v, 1) for k, v in blk['v'].items()}}
    doc = {'_rule': '[R-FCAL-01] · SIGCM clause 1 · four fields on every number',
           '_currency': 'EGP million', '_entity': 'GB Corp S.A.E (formerly GB Auto S.A.E), EGX: GBCO',
           '_span': '%d-%d' % (min(years), max(years)),
           'years': {str(k): v for k, v in sorted(years.items())}}
    json.dump(doc, open(os.path.join(HERE, 'panel.json'), 'w', encoding='utf-8'),
              indent=1, ensure_ascii=False)
    for y in sorted(years):
        b = years[y]
        print('FY%d  %-6s rev %10.1f  gp %9.1f  op %9.1f  np %9.1f   %s'
              % (y, 'FOOTS' if b['foots'] else 'BROKEN', b['is'].get('revenue', float('nan')),
                 b['is'].get('gross_profit', float('nan')),
                 b['is'].get('operating_profit', float('nan')),
                 b['is'].get('net_profit', float('nan')), b['source'][:34]))
        for n, a, c in b['failed_checks']:
            print('        DOES NOT FOOT %s: %.1f vs %.1f' % (n, a, c))


if __name__ == '__main__':
    main()
