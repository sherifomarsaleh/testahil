#!/usr/bin/env python3
"""SCEM walk-forward — the POINT-IN-TIME macro conditioning.

WHAT AN ORIGIN KNEW, NOT WHAT WE KNOW. Each origin is given the IMF World Economic
Outlook edition that EXISTED at that year-end and nothing later. A rebuild that
reaches for today's series is not a rebuild; it is the answer wearing a date, and the
house archive has already measured how far that would be off — Egyptian inflation as
published at an origin differs from today's reading of the same year by up to 10.4
percentage points, in both directions.

TWO EXOGENOUS ANCHORS, and neither is the company's own trend:
  ACTIVITY   Egypt real GDP growth (NGDP_RPCH). Cement is an activity-linked
             commodity — the state housing, industrial and transport programmes are
             its marginal buyer — and the issuer discloses no volume of its own, so
             the volume leg has to come from outside the company entirely.
  PRICE      Egypt consumer price inflation (PCPIPCH).

THE BASIS BREAK IS REAL AND IS MAPPED, NOT IGNORED. The IMF publishes Egypt on a
FISCAL year ending 30 June; Sinai Cement reports on a CALENDAR year. A calendar year
is therefore half of each of the two fiscal years that span it — the `fiscal_june`
mapping [R-MACRO-01 AMENDED] runs the other way round — and it is applied to both
series identically and declared here rather than left to be discovered. Using the
fiscal figure as though it were the calendar one would put Egypt's whole 2024
devaluation in the wrong year.

WHAT COULD NOT BE SOURCED, AND SO IS NOT USED: the October 2025 edition, which is the
one an origin standing at 31-Dec-2025 would have had. Four URL patterns were tried and
all four refused (see fetch_attempts.json); origin FY2025 is therefore given the APRIL
2025 edition, which did exist at that origin and is simply not the freshest one that
did. It is labelled, and it changes no scored cell, because FY2025 has no resolved
horizon yet.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WEO = os.path.join(HERE, 'weo')
ARCHIVE = os.path.join(os.path.dirname(HERE), 'macro_history',
                       '_extract_weo_egypt.json')

# The edition each origin actually had. Declared, not inferred.
VINTAGE = {
    'FY2021': 'October 2021',
    'FY2022': 'October 2022',
    'FY2023': 'October 2023',
    'FY2024': 'October 2024',
    'FY2025': 'April 2025',
}
VINTAGE_NOTE = {
    'FY2025': ('the October 2025 edition is the one this origin would have had and it '
               'could not be sourced from any of four URL patterns; the April 2025 '
               'edition DID exist at 31-Dec-2025 and is used, labelled. No scored cell '
               'depends on it — FY2025 has no resolved horizon.'),
}
LOCAL = {'October 2024': 'WEOOct2024all.xls', 'April 2025': 'WEOApr2025all.xls'}
OUTTURN_EDITION = 'April 2025'      # the latest edition held, for the perfect-foresight leg


def _read_local(fname):
    raw = open(os.path.join(WEO, fname), 'rb').read().decode('utf-16')
    lines = raw.splitlines()
    hdr = lines[0].split('\t')
    out = {}
    for ln in lines:
        f = ln.split('\t')
        if len(f) < 10 or f[1] != 'EGY' or f[2] not in ('NGDP_RPCH', 'PCPIPCH'):
            continue
        series = {}
        for i, y in enumerate(hdr):
            if y.isdigit() and i < len(f):
                v = f[i].replace(',', '').strip()
                try:
                    series[y] = float(v)
                except ValueError:
                    pass
        out[f[2]] = series
    return out


def editions():
    """Every WEO edition available to this run, from both places it can come from."""
    out = {}
    arch = json.load(open(ARCHIVE))
    for name, blk in arch.items():
        out[name] = {k: {y: float(v) for y, v in s['values'].items()
                         if _isnum(v)}
                     for k, s in blk['series'].items() if k in ('NGDP_RPCH', 'PCPIPCH')}
    for name, fname in LOCAL.items():
        out[name] = _read_local(fname)
    return out


def _isnum(v):
    try:
        float(v)
        return True
    except (TypeError, ValueError):
        return False


def calendar(series, year):
    """FISCAL-JUNE -> CALENDAR. Half of each of the two fiscal years spanning it.

    The IMF's Egypt year `Y` runs July Y-1 to June Y, so calendar year Y is the
    second half of fiscal Y and the first half of fiscal Y+1.
    """
    a, b = series.get(str(year)), series.get(str(year + 1))
    if a is None or b is None:
        return None
    return 0.5 * a + 0.5 * b


def path(origin, horizons=(1, 2, 3)):
    """What the origin believed about the years it was forecasting."""
    ed = editions()[VINTAGE[origin]]
    y0 = int(origin[2:])
    out = {}
    for h in horizons:
        y = y0 + h
        g = calendar(ed['NGDP_RPCH'], y)
        p = calendar(ed['PCPIPCH'], y)
        out[h] = dict(year=y, real_gdp_growth=None if g is None else g / 100.0,
                      cpi=None if p is None else p / 100.0)
    return out


def outturn(year):
    """The perfect-foresight leg: the latest published reading of that year."""
    ed = editions()[OUTTURN_EDITION]
    g = calendar(ed['NGDP_RPCH'], year)
    p = calendar(ed['PCPIPCH'], year)
    est = year >= 2025
    return dict(year=year, real_gdp_growth=None if g is None else g / 100.0,
                cpi=None if p is None else p / 100.0,
                is_outturn=not est,
                note=('the April 2025 edition PROJECTS this year rather than reporting '
                      'it, so the perfect-foresight leg for it is a projection and is '
                      'labelled; cells landing on it are reported separately'
                      if est else 'an estimate of a completed year'))


if __name__ == '__main__':
    eds = editions()
    print('WEO editions available to this run: %s' % ', '.join(sorted(eds)))
    rec = {'vintage_by_origin': VINTAGE, 'vintage_note': VINTAGE_NOTE,
           'outturn_edition': OUTTURN_EDITION,
           'mapping': 'fiscal_june -> calendar, half of each of the two fiscal years',
           'believed': {}, 'outturn': {}}
    print('\n%-8s %-14s %s' % ('origin', 'edition', 'what it believed, calendar years'))
    for o in sorted(VINTAGE):
        p = path(o)
        rec['believed'][o] = p
        bits = []
        for h, d in sorted(p.items()):
            if d['cpi'] is None:
                bits.append('%d n/a' % d['year'])
            else:
                bits.append('%d g%+.1f%% p%.1f%%'
                            % (d['year'], d['real_gdp_growth'] * 100, d['cpi'] * 100))
        print('%-8s %-14s %s' % (o, VINTAGE[o], '  '.join(bits)))
    print('\n%-6s %s' % ('year', 'outturn (April 2025 edition), calendar'))
    for y in range(2022, 2027):
        d = outturn(y)
        rec['outturn'][y] = d
        if d['cpi'] is not None:
            print('%-6d g%+.2f%%  p%.2f%%   %s'
                  % (y, d['real_gdp_growth'] * 100, d['cpi'] * 100,
                     'OUTTURN' if d['is_outturn'] else 'PROJECTION'))
    json.dump(rec, open(os.path.join(HERE, 'macro.json'), 'w'), indent=1)
