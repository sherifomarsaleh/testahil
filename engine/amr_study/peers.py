"""AMR — peer frame for the relative-multiples lens and the operating-KPI cross-check.

Peers are a CROSS-CHECK ONLY. Nothing here is a source for Americana's own reported
historicals; those come exclusively from the audited consolidated financial statements.
The peer set spans (a) the region — Saudi-listed restaurant operators — and (b) outside
the region — global franchisors and large franchisee/operator platforms in emerging
markets, which is the closer structural analogue for a master-franchisee operator.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))

PEERS = [
    ('6013.SR',      'Alamar Foods',            'Saudi Arabia',  'Regional franchisee operator (Domino’s, Wendy’s MENA)'),
    ('6002.SR',      'Herfy Food Services',     'Saudi Arabia',  'Saudi QSR operator and food manufacturer'),
    ('6001.SR',      'Halwani Bros',            'Saudi Arabia',  'Saudi packaged-food peer (consumer cross-check)'),
    ('ALSEA.MX',     'Alsea',                   'Mexico',        'Largest Latin-American franchisee operator (Starbucks, Domino’s, BK)'),
    ('JUBLFOOD.NS',  'Jubilant FoodWorks',      'India',         'Master franchisee, Domino’s India'),
    ('DEVYANI.NS',   'Devyani International',   'India',         'Master franchisee, KFC/Pizza Hut India — closest structural analogue'),
    ('SAPPHIRE.NS',  'Sapphire Foods',          'India',         'Master franchisee, KFC/Pizza Hut India'),
    ('YUM',          'Yum! Brands',             'United States', 'Franchisor of KFC, Pizza Hut, Taco Bell'),
    ('YUMC',         'Yum China',               'China',         'Licensee-operator of KFC/Pizza Hut in China'),
    ('QSR',          'Restaurant Brands Intl.', 'Canada',        'Franchisor of Burger King, Tim Hortons, Popeyes'),
    ('DPZ',          "Domino's Pizza",          'United States', 'Franchisor, delivery-led QSR'),
]

MODULES = 'defaultKeyStatistics,financialData,summaryDetail,price'


def crumb():
    subprocess.run(['curl', '-sS', '--max-time', '30', '-c', '/tmp/yc.txt',
                    'https://fc.yahoo.com', '-o', '/dev/null'], check=False)
    c = subprocess.run(['curl', '-sS', '--max-time', '30', '-b', '/tmp/yc.txt', '-c', '/tmp/yc.txt',
                        'https://query1.finance.yahoo.com/v1/test/getcrumb',
                        '-H', 'User-Agent: Mozilla/5.0'], capture_output=True, text=True).stdout.strip()
    return c


def get(sym, c):
    u = (f'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{sym}'
         f'?modules={MODULES}&crumb={c}')
    raw = subprocess.run(['curl', '-sS', '--max-time', '40', '-b', '/tmp/yc.txt', u,
                          '-H', 'User-Agent: Mozilla/5.0'], capture_output=True, text=True).stdout
    d = json.loads(raw)
    r = d.get('quoteSummary', {}).get('result')
    return r[0] if r else None


def raw(node, key):
    v = (node or {}).get(key)
    if isinstance(v, dict):
        return v.get('raw')
    return v


def main():
    c = crumb()
    out = {}
    for sym, name, country, why in PEERS:
        r = get(sym, c)
        if not r:
            out[sym] = dict(name=name, country=country, rationale=why, error='no data returned')
            print(f'{sym:14s} NO DATA')
            continue
        ks, fd, sd, pr = (r.get('defaultKeyStatistics', {}), r.get('financialData', {}),
                          r.get('summaryDetail', {}), r.get('price', {}))
        ev = raw(ks, 'enterpriseValue')
        ebitda = raw(fd, 'ebitda')
        rev = raw(fd, 'totalRevenue')
        mc = raw(pr, 'marketCap') or raw(sd, 'marketCap')
        rec = dict(
            name=name, country=country, rationale=why,
            currency=raw(pr, 'currency') or pr.get('currency'),
            price=raw(pr, 'regularMarketPrice'), market_cap=mc,
            enterprise_value=ev, revenue_ttm=rev, ebitda_ttm=ebitda,
            ebitda_margin=(ebitda / rev) if (ebitda and rev) else None,
            ev_ebitda=(ev / ebitda) if (ev and ebitda) else None,
            ev_sales=(ev / rev) if (ev and rev) else None,
            pe_trailing=raw(sd, 'trailingPE'), pe_forward=raw(sd, 'forwardPE') or raw(ks, 'forwardPE'),
            price_to_book=raw(ks, 'priceToBook'),
            dividend_yield=raw(sd, 'dividendYield'),
            roe=raw(fd, 'returnOnEquity'), operating_margin=raw(fd, 'operatingMargins'),
            revenue_growth=raw(fd, 'revenueGrowth'),
            net_debt=(ev - mc) if (ev and mc) else None,
        )
        out[sym] = rec
        print(f"{sym:14s} {name:26s} EV/EBITDA {rec['ev_ebitda'] and round(rec['ev_ebitda'],1)}  "
              f"P/E {rec['pe_trailing'] and round(rec['pe_trailing'],1)}  "
              f"EBITDA mgn {rec['ebitda_margin'] and round(100*rec['ebitda_margin'],1)}%")
    payload = dict(
        retrieved='2026-08-09',
        source=('Yahoo Finance quoteSummary API (query2.finance.yahoo.com/v10/finance/quoteSummary), '
                'trailing-twelve-month figures as published, retrieved 9 August 2026. '
                'CROSS-CHECK ONLY — no figure here enters the Americana build; Americana’s own '
                'historicals come exclusively from its audited consolidated financial statements.'),
        peers=out)
    with open(os.path.join(HERE, 'peers.json'), 'w') as f:
        json.dump(payload, f, indent=1)
    print('\nwrote peers.json')


if __name__ == '__main__':
    main()
