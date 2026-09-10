#!/usr/bin/env python3
"""ADIB walk-forward — the exogenous macro ring, with a publication lag that binds.

POINT-IN-TIME. At a 31-December origin the current year's national accounts and CPI
print are NOT yet published. Every rule that reads a macro series therefore reads it
through `o-1` and never through `o`. That is R1 and R15 of the pre-registration and it
is enforced HERE rather than remembered at each call site: `known_through(o)` is the
only accessor the build uses.

Tier C, and deliberately so - these are macro aggregates for the country, not company
figures. Every company figure in this run is tier A.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
_W = json.load(open(os.path.join(HERE, 'macro_eg_wdi.json'), encoding='utf-8'))

SOURCE = ('World Bank World Development Indicators, Egypt Arab Rep., read 2026-09-09: '
          'FP.CPI.TOTL.ZG (CPI inflation), NY.GDP.MKTP.CN (GDP, current LCU), '
          'FS.AST.PRVT.GD.ZS (domestic credit to the private sector, % of GDP), '
          'PA.NUS.FCRF (EGP/USD), FM.LBL.BMNY.CN (broad money).')

CPI_PCT = {int(y): v for y, v in _W['cpi_pct'].items()}
GDP = {int(y): v for y, v in _W['gdp_lcu'].items()}
CREDIT_PCT = {int(y): v for y, v in _W['credit_priv_pct_gdp'].items()}
EGPUSD = {int(y): v for y, v in _W['egp_usd'].items()}
M2 = {int(y): v for y, v in _W['broad_money_lcu'].items()}

# System credit to the private sector, in EGP. The exogenous volume anchor (R1).
SYSTEM_CREDIT = {y: CREDIT_PCT[y] / 100.0 * GDP[y]
                 for y in sorted(set(CREDIT_PCT) & set(GDP))}

# Egyptian statutory corporate income tax rate, by the regime in force at each
# year-end. Law 91/2005 as amended: 25% headline from 2011 (with a 30% top band
# 2014-2015 for large profits), unified at 22.5% by Law 96/2015 from FY2015.
# Used ONLY as R13's reported sensitivity, never as the primary rule.
STATUTORY_TAX = {y: (0.25 if y < 2015 else 0.225) for y in range(2009, 2031)}


def known_through(o):
    """The last macro year an analyst standing at 31-Dec of origin `o` could read."""
    return o - 1


def cpi_index(base, y, path=None):
    """Cumulative CPI index from `base` to `y`, base = 1.0. `path` overrides CPI_PCT."""
    src = path or CPI_PCT
    x = 1.0
    for t in range(base + 1, y + 1):
        if t not in src:
            return None
        x *= (1.0 + src[t] / 100.0)
    return x


def trailing_mean_cpi(o, k=3):
    """R15: mean published inflation over the k years ending at known_through(o)."""
    last = known_through(o)
    ys = [y for y in range(last - k + 1, last + 1) if y in CPI_PCT]
    if not ys:
        return None
    return sum(CPI_PCT[y] for y in ys) / len(ys) / 100.0


def projected_cpi_path(o, hmax=5, k=3):
    """The inflation path the mechanical rule sees at origin o: flat at the trailing mean."""
    g = trailing_mean_cpi(o, k)
    if g is None:
        return None
    return {o + h: g * 100.0 for h in range(0, hmax + 1)}


def system_credit_cagr(o, k=3):
    """R1: trailing k-year CAGR of system credit, on the series published through o-1."""
    last = known_through(o)
    a, b = last - k, last
    if a not in SYSTEM_CREDIT or b not in SYSTEM_CREDIT:
        return None
    return (SYSTEM_CREDIT[b] / SYSTEM_CREDIT[a]) ** (1.0 / k) - 1.0


def projected_system_credit(o, hmax=5, k=3):
    """R1: system credit projected from its last KNOWN level at its trailing CAGR.

    The last known level is o-1, so the o+h projection compounds h+1 years. The
    origin year's own system credit is itself a projection, exactly as it would have
    been for a reader standing at that origin.
    """
    g = system_credit_cagr(o, k)
    last = known_through(o)
    if g is None or last not in SYSTEM_CREDIT:
        return None
    base = SYSTEM_CREDIT[last]
    return {o + h: base * (1.0 + g) ** (h + 1) for h in range(0, hmax + 1)}


if __name__ == '__main__':
    print('%-6s %14s %10s %10s %10s' % ('year', 'system_credit', 'cpi%', 'gdp_lcu', 'egp/usd'))
    for y in sorted(SYSTEM_CREDIT):
        if y >= 2009:
            print('%-6d %14.0f %10.2f %10.3g %10.2f'
                  % (y, SYSTEM_CREDIT[y] / 1e6, CPI_PCT.get(y, float('nan')),
                     GDP[y] / 1e9, EGPUSD.get(y, float('nan'))))
    print('\n(system credit in EGP mn)')
    for o in range(2014, 2025):
        print('origin FY%d  known_through %d  credit CAGR %.1f%%  trailing CPI %.1f%%'
              % (o, known_through(o), 100 * (system_credit_cagr(o) or 0),
                 100 * (trailing_mean_cpi(o) or 0)))
