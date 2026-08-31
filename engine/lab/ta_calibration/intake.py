"""intake.py — validate a batch of vendor OHLC exports before anything is written.

Run this on an upload directory BEFORE any file goes near engine/raw_ohlc/. It
writes nothing; it decides whether a batch is safe to convert.

WHY EACH CHECK IS HERE

1. THE EXCHANGE COMES FROM THE FILENAME, NOT THE FOLDER. TradingView names its
   exports ADX_FAB_1D.csv / DFM_DLY_EMAAR_1D.csv, and that prefix is the one
   piece of provenance the library layout destroys — raw_ohlc/ groups by MARKET
   (AE spans ADX and DFM), and the protocol is explicit that the exchange is
   read from the code prefix in assets/data.js and never inferred from the
   folder. So the filename is checked AGAINST data.js, and a disagreement is a
   refusal, not a warning.

2. TADAWUL SYMBOLS ARE NUMERIC. data.js carries TADAWUL:2050 for SAVOLA and
   TADAWUL:4142 for RIYADHCABLE, so a vendor file named TADAWUL_2050_1D.csv
   resolves by CODE, not by name — the failure that put ALRAJHI under raw file
   RAJHI once already. Both routes are tried and the resolution is printed.

3. PRICE VS TOTAL-RETURN IS DIAGNOSED, NEVER ASSUMED. Divergence from the held
   library that decays to zero at the right-hand edge in a piecewise-constant
   staircase is dividend back-adjustment. Reported per file, because the two
   bases must never be mixed inside one market panel.

4. THE POPULATION IS COUNTED AGAINST THE LIBRARIES ON DISK. A batch that
   silently covers 26 of 28 names reports 26 of 28, not "clean".
"""
from __future__ import annotations
import os, re, sys, glob, json, subprocess
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
RAW = os.path.join(ROOT, 'engine', 'raw_ohlc')
sys.path.insert(0, os.path.join(ROOT, 'engine'))

EXCHANGE_MARKET = {'ADX': 'AE', 'DFM': 'AE', 'EGX': 'EG', 'TADAWUL': 'SA',
                   'NSE': 'IN', 'NASDAQ': 'US', 'QSE': 'QA', 'KRX': 'KR'}
FNAME = re.compile(r'^(?:[0-9a-f]{8}-)?([A-Z]+)_(?:DLY_)?(.+?)_1D\.csv$')

# A data.js TICKER KEY IS NOT A LIBRARY FILENAME, and every one of the three
# places they diverge is already recorded in the protocol as a defect someone
# found the hard way:
#   2POINTZERO   a JS identifier cannot start with a digit, so data.js quotes
#                the key and the library sidesteps it in the filename. The
#                digest records this name being silently dropped by three
#                separate tools, each of which reported success.
#   ALRAJHI      data.js carries TADAWUL:1120; the library file is RAJHI.csv.
#                Named in the digest as the miss the load-assert caught.
#   ADIBUAE      ADIB is a different bank per market — ledger ADIB is Egyptian,
#                ADIBUAE is the UAE one, and the two libraries are EG/ADIB.csv
#                and AE/ADIB.csv. band_record.py resolves this through an
#                explicit asserted alias rather than inferring from a filename.
# GOLD/SILVER/PLATINUM hold libraries and carry no data.js TICKERS entry at all.
ALIAS = {('AE', '2POINTZERO'): 'TWOPOINTZERO',
         ('SA', 'ALRAJHI'): 'RAJHI',
         ('AE', 'ADIBUAE'): 'ADIB'}
METALS_ONLY = {'XAU/GOLD', 'XAU/SILVER', 'XPT/PLATINUM'}


def library_key(market, ticker):
    """The (market, library filename) a data.js ticker actually lives under."""
    return f'{market}/{ALIAS.get((market, ticker), ticker)}'


def assert_bijection(dmap, libs):
    """Every data.js ticker resolves to a held library, and no library is orphaned.

    Asserted BOTH WAYS, per the band_record rule: a tool reporting '0 skipped'
    is not evidence. Without this the AE batch reads 27 of 28 forever and the
    one missing name is re-sent again and again.
    """
    from collections import defaultdict
    claimed, market_of = defaultdict(list), {}
    for (ex, _), tkr in dmap.items():
        mkt = EXCHANGE_MARKET.get(ex)
        if mkt:
            market_of[tkr] = mkt
    for tkr, mkt in market_of.items():
        k = library_key(mkt, tkr)
        if k not in libs:
            raise AssertionError(f'data.js ticker {tkr} resolves to {k}, which is not held')
        claimed[k].append(tkr)
    orphans = sorted(libs - set(claimed) - METALS_ONLY)
    if orphans:
        raise AssertionError(f'library files claimed by no data.js ticker: {orphans}')
    dupes = {k: v for k, v in claimed.items() if len(v) > 1}
    if dupes:
        raise AssertionError(f'two data.js tickers claim one library: {dupes}')
    return len(market_of), len(libs)


def data_js_map():
    """{(exchange, symbol-or-code): ticker} straight out of the shipped data.js."""
    out = subprocess.run(['node', '-e', f'''
      const fs=require('fs');
      const src=fs.readFileSync({json.dumps(os.path.join(ROOT,"assets","data.js"))},'utf8');
      eval(src.replace(/^\\s*(const|var|let)\\s+/gm,'global.'));
      const T=global.TICKERS||{{}};
      console.log(JSON.stringify(Object.fromEntries(
        Object.entries(T).map(([k,v])=>[k, v.code||'']))));
    '''], capture_output=True, text=True, cwd=ROOT)
    if out.returncode:
        raise RuntimeError(f'could not read data.js: {out.stderr[:300]}')
    codes = json.loads(out.stdout)
    m = {}
    for tkr, code in codes.items():
        if ':' not in code:
            continue
        ex, sym = code.split(':', 1)
        m[(ex, sym.upper())] = tkr          # by code (numeric on TADAWUL)
        m[(ex, tkr.upper())] = tkr          # by name
    return m


def read_export(path):
    u = pd.read_csv(path)
    cols = {c.lower(): c for c in u.columns}
    need = ('time', 'open', 'high', 'low', 'close')
    if not all(k in cols for k in need):
        return None
    df = pd.DataFrame({'Date': pd.to_datetime(u[cols['time']], errors='coerce'),
                       'Price': u[cols['close']], 'Open': u[cols['open']],
                       'High': u[cols['high']], 'Low': u[cols['low']],
                       'Vol.': u[cols['volume']] if 'volume' in cols else np.nan})
    return df.dropna(subset=['Date', 'Price', 'High', 'Low']).sort_values('Date').reset_index(drop=True)


def read_library(market, ticker):
    p = os.path.join(RAW, market, f'{ticker}.csv')
    if not os.path.exists(p):
        return None
    d = pd.read_csv(p)
    d.columns = [c.strip().strip('"').lstrip('﻿') for c in d.columns]
    d['Date'] = pd.to_datetime(d['Date'], format='%m/%d/%Y', errors='coerce')
    d['Price'] = pd.to_numeric(d['Price'].astype(str).str.replace(',', ''), errors='coerce')
    return d.dropna(subset=['Date', 'Price']).sort_values('Date').reset_index(drop=True)


def basis(up, lib):
    """price / total-return / mismatch, from the shape of the divergence."""
    m = up[['Date', 'Price']].merge(lib[['Date', 'Price']], on='Date',
                                    suffixes=('_up', '_lib')).dropna()
    if len(m) < 60:
        return dict(verdict='too little overlap', overlap=len(m))
    rel = (m.Price_up - m.Price_lib).abs() / m.Price_lib
    tail = rel[m.Date >= m.Date.max() - pd.Timedelta(days=30)]
    steps = np.round(rel.to_numpy(), 6)
    n_levels = len(np.unique(steps))
    v = ('price' if rel.median() < 1e-4 else
         'total-return' if (tail.median() < 1e-4 and n_levels < len(m) / 5) else
         'UNRECONCILED')
    return dict(verdict=v, overlap=int(len(m)), median_div=float(rel.median()),
                tail_div=float(tail.median()), distinct_levels=int(n_levels))


def main(updir):
    from data_quality import clean_ohlc
    dmap = data_js_map()
    libs = {f'{m}/{os.path.basename(f)[:-4]}'
            for m in os.listdir(RAW) for f in glob.glob(os.path.join(RAW, m, '*.csv'))}
    n_tickers, n_libs = assert_bijection(dmap, libs)
    print(f'name map reconciled: {n_tickers} data.js tickers -> {n_libs} libraries '
          f'(+{len(METALS_ONLY)} metals with no data.js entry)')
    files = sorted(glob.glob(os.path.join(updir, '*.csv')))
    seen, rows, problems = set(), [], []

    for f in files:
        b = os.path.basename(f)
        mm = FNAME.match(b)
        if not mm:
            problems.append((b, 'filename does not carry EXCHANGE_SYMBOL_1D — cannot '
                                'resolve the exchange, and it must not be guessed'))
            continue
        ex, sym = mm.group(1).upper(), mm.group(2).upper()
        mkt = EXCHANGE_MARKET.get(ex)
        tkr = dmap.get((ex, sym))
        if mkt is None:
            problems.append((b, f'exchange {ex} is not registered'))
            continue
        if tkr is None:
            problems.append((b, f'{ex}:{sym} matches no code in data.js — needs an '
                                f'explicit mapping, never a guess'))
            continue
        key = library_key(mkt, tkr)
        up = read_export(f)
        if up is None:
            problems.append((b, 'missing one of time/open/high/low/close'))
            continue
        lib = read_library(mkt, tkr)
        try:
            cl, rep = clean_ohlc(up.copy(), tkr, verbose=False, market=mkt)
            step0 = f'ok ({len(up)}->{len(cl)}' + (f', {len(list(rep))} repairs)' if rep else ')')
        except Exception as e:
            step0 = f'FAILED: {type(e).__name__}'
        bs = basis(up, lib) if lib is not None else dict(verdict='no library held')
        seen.add(key)
        rows.append(dict(file=b, key=key, exchange=ex, rows=len(up),
                         first=str(up.Date.min().date()), last=str(up.Date.max().date()),
                         step0=step0, **{f'basis_{k}': v for k, v in bs.items()}))

    r = pd.DataFrame(rows)
    print(f'files: {len(files)} | resolved: {len(rows)} | unresolved: {len(problems)}')
    if len(r):
        print(r[['key', 'exchange', 'rows', 'first', 'last', 'step0',
                 'basis_verdict']].to_string(index=False))
        print('\nbasis tally:', dict(r.basis_verdict.value_counts()))
    unrec = r[r.basis_verdict == 'UNRECONCILED'] if len(r) else r
    if len(unrec):
        # A refusal must hand over the evidence to settle it, or it is just a
        # shrug. The staircase is the whole diagnosis: a piecewise-constant
        # divergence with few distinct levels is dividend back-adjustment, and
        # the tail test only failed because an ex-date fell inside the window.
        print('\nUNRECONCILED — classify these by hand before converting:')
        for _, x in unrec.iterrows():
            print(f"  {x.key}: overlap {x.basis_overlap}, median divergence "
                  f"{x.basis_median_div*100:.2f}%, last-30-day {x.basis_tail_div*100:.2f}%, "
                  f"{x.basis_distinct_levels} distinct divergence levels across "
                  f"{x.basis_overlap} rows")
            print(f"     few distinct levels = a dividend staircase (total-return); "
                  f"many = a genuine data disagreement (stop)")
    if problems:
        print('\nUNRESOLVED — nothing is written for these:')
        for b, why in problems:
            print(f'  {b}: {why}')

    # COUNT AGAINST A KNOWN TOTAL, per market.
    print('\ncoverage against the libraries on disk:')
    by_market = {}
    for k in libs:
        by_market.setdefault(k.split('/')[0], set()).add(k)
    complete = []
    for mkt in sorted(by_market):
        have = seen & by_market[mkt]
        flag = 'COMPLETE' if len(have) == len(by_market[mkt]) else \
               ('partial — DO NOT CONVERT' if have else '-')
        if len(have) == len(by_market[mkt]):
            complete.append(mkt)
        print(f'  {mkt:5} {len(have):>3} of {len(by_market[mkt]):>3}   {flag}')
        missing = sorted(x.split("/")[1] for x in by_market[mkt] - have)
        if have and missing:
            print(f'        missing: {", ".join(missing)}')
    print(f'\nmarkets convertible as a unit: {complete or "none"}')
    print('A market is converted whole or not at all — its fit pools the panel, so a '
          'mixed-basis panel is worse than either basis chosen consistently.')
    return r


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else
         '/root/.claude/uploads/972d4834-4b15-5e35-8d2b-653ceed1c887/')
