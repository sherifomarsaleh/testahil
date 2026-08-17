"""Peer set for the relative-multiples lens.

SOURCE DISCIPLINE. Every figure for ADNOC Drilling itself comes from its own
audited/reviewed filings. NOTHING in this file feeds the subject's historicals.
What this file collects is PEER data — other listed drillers' and oilfield-service
companies' own reported revenue, EBITDA, debt, cash and share counts, plus their
live share prices — which is market-observable third-party data used for
cross-check and for the relative-multiples lens ONLY. The lens applies a peer
multiple to ADNOC Drilling's OWN audited EBITDA and earnings, so no peer figure
ever enters the subject's income statement, balance sheet or cash flow.

Peer set: the listed contract-drilling and oilfield-service universe, split into
the three groups that actually price differently —

  MENA NOC-CONTRACTED DRILLERS  ADES Holding (2382.SR), Arabian Drilling (2381.SR)
    The closest read: same customer archetype (a national oil company), same
    region, same mix of land and offshore rigs on multi-year contracts.
  GLOBAL LAND DRILLERS          Helmerich & Payne, Nabors, Patterson-UTI, Precision
    Same asset (land rigs) but exposed to the US shale spot market, so their
    multiples carry cycle risk ADNOC Drilling's contracted book does not.
  GLOBAL OFFSHORE DRILLERS      Valaris, Noble, Borr Drilling
    Jackup/floater economics, the read for the Offshore segment.
  DIVERSIFIED OILFIELD SERVICES SLB, Halliburton, Baker Hughes, Weatherford
    The read for the OFS segment, which is an integrated-services business.
"""
import json, os, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'Mozilla/5.0'}

PEERS = [
    ('2382.SR', 'ADES Holding',        'MENA NOC-contracted driller', 'SAR'),
    ('2381.SR', 'Arabian Drilling',    'MENA NOC-contracted driller', 'SAR'),
    ('HP',      'Helmerich & Payne',   'Global land driller',         'USD'),
    ('NBR',     'Nabors Industries',   'Global land driller',         'USD'),
    ('PTEN',    'Patterson-UTI',       'Global land driller',         'USD'),
    ('PDS',     'Precision Drilling',  'Global land driller',         'USD'),
    ('VAL',     'Valaris',             'Global offshore driller',     'USD'),
    ('NE',      'Noble Corporation',   'Global offshore driller',     'USD'),
    ('BORR',    'Borr Drilling',       'Global offshore driller',     'USD'),
    ('SLB',     'SLB',                 'Diversified oilfield services', 'USD'),
    ('HAL',     'Halliburton',         'Diversified oilfield services', 'USD'),
    ('BKR',     'Baker Hughes',        'Diversified oilfield services', 'USD'),
    ('WFRD',    'Weatherford Intl',    'Diversified oilfield services', 'USD'),
]

TS_TYPES = ('quarterlyEBITDA,quarterlyTotalRevenue,quarterlyNetIncome,'
            'quarterlyTotalDebt,quarterlyCashAndCashEquivalents,'
            'quarterlyOrdinarySharesNumber,quarterlyStockholdersEquity')


def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))


def price(sym):
    d = get(f"https://query2.finance.yahoo.com/v8/finance/chart/{sym}?range=5d&interval=1d")
    m = d['chart']['result'][0]['meta']
    return float(m['regularMarketPrice']), m.get('currency')


def series(sym):
    u = (f"https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/"
         f"{sym}?symbol={sym}&type={TS_TYPES}&period1=1580000000&period2=1800000000")
    out = {}
    for blk in get(u)['timeseries']['result']:
        t = blk['meta']['type'][0]
        pts = [(p['asOfDate'], p['reportedValue']['raw']) for p in blk.get(t, []) if p]
        if pts:
            out[t] = sorted(pts)
    return out


def main():
    rows = []
    for sym, name, grp, ccy in PEERS:
        try:
            px, pccy = price(sym)
            s = series(sym)
            eb = s.get('quarterlyEBITDA', [])
            rev = s.get('quarterlyTotalRevenue', [])
            ni = s.get('quarterlyNetIncome', [])
            ltm_ebitda = sum(v for _, v in eb[-4:]) if len(eb) >= 4 else None
            ltm_rev = sum(v for _, v in rev[-4:]) if len(rev) >= 4 else None
            ltm_ni = sum(v for _, v in ni[-4:]) if len(ni) >= 4 else None
            debt = s.get('quarterlyTotalDebt', [(None, None)])[-1][1]
            cash = s.get('quarterlyCashAndCashEquivalents', [(None, None)])[-1][1]
            sh = s.get('quarterlyOrdinarySharesNumber', [(None, None)])[-1][1]
            eqty = s.get('quarterlyStockholdersEquity', [(None, None)])[-1][1]
            asof = eb[-1][0] if eb else None
            rows.append(dict(symbol=sym, name=name, group=grp, price=px, currency=pccy,
                             ltm_ebitda=ltm_ebitda, ltm_revenue=ltm_rev, ltm_net_income=ltm_ni,
                             total_debt=debt, cash=cash, shares=sh, book_equity=eqty,
                             latest_period=asof,
                             ebitda_quarters=[list(q) for q in eb[-4:]]))
            print(f"{sym:9s} px {px:8.2f} {pccy}  LTM EBITDA {ltm_ebitda}  "
                  f"debt {debt}  cash {cash}  sh {sh}  asof {asof}", flush=True)
        except Exception as e:
            print(f"{sym:9s} ERR {e}", flush=True)
            rows.append(dict(symbol=sym, name=name, group=grp, error=str(e)))
        time.sleep(1.2)
    json.dump(rows, open(os.path.join(HERE, 'peers_raw.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
