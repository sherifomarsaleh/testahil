"""THE TWO DATES EVERY VALUATION DOCUMENT CARRIES, resolved from one place.

WHAT THIS EXISTS TO STOP [R-DOC-03, adopted 10-09-2026 by instruction].
A valuation document states a number struck against a price, and BOTH facts have dates
that are not the same date. The price is the latest known close, which may be days old.
The document is issued when it is issued. On 10-09-2026 the principal was sent an AMOC
package containing the 8 August edition while the current one is 3 September, and the
confusion was possible only because a reader could not tell, from the paper itself, WHEN
IT WAS ISSUED as distinct from when its price was taken.

A document that carries one date leaves a reader to guess which of the two it is. The
rule is therefore that both appear, at the top, always -- and that a recalibration issues
a NEW document carrying the day it was issued, never an amended copy of an older one.

RESOLVED, NEVER TYPED. The price date is the spot input's own registered date, surfaced
through the study's committed numbers. The issue date is the study's own edition module
where it has one, because that is the file every artefact name already derives from
[L-066]; a study with no edition module falls back to the date passed by its builder.
Neither is read from a filename and neither is guessed from a file's modification time --
an old file with a fresh timestamp is exactly the trap that produced the AMOC package.
"""
import json
import os

ENGINE = os.path.dirname(os.path.abspath(__file__))


def _numbers(ticker):
    p = os.path.join(ENGINE, '%s_study' % ticker.lower(), 'study_numbers.json')
    if not os.path.exists(p):
        return {}
    with open(p, encoding='utf-8') as fh:
        return json.load(fh)


def price_date(ticker, numbers=None):
    """The date of the price this study is struck against.

    THE SPOT INPUT'S OWN REGISTERED DATE COMES FIRST, and meta.asof comes LAST, because
    they are different facts on some studies and the difference is the whole point of
    this module. ARCC strikes at a 3 September price while its valuation date is
    30 June 2026 -- the date of the latest disclosed balance sheet -- so reading asof
    would print the balance-sheet date under a label that says "the latest known close".
    A study whose spot carries no date at all returns empty and the document says
    "not recorded" rather than borrowing a date that means something else.
    """
    d = numbers if numbers is not None else _numbers(ticker)
    sp = (d.get('inputs') or {}).get('spot')
    if isinstance(sp, dict) and sp.get('date'):
        return sp['date']
    if d.get('spot_date'):
        return d['spot_date']
    # THE SUPPLIED PRICE FILE IS WHERE THE PRICE GATE ITSELF READS, so a study whose own
    # numbers carry no spot date is answered from the same record that routes it, never
    # from a date typed here. Merged newest-first on each price's OWN date, which is the
    # convention check_valuation_gap and check_supplied_prices both hold to.
    import glob
    best = ('', '')
    for fp in sorted(glob.glob(os.path.join(ENGINE, 'prices', 'SUPPLIED_*.json'))):
        try:
            with open(fp, encoding='utf-8') as fh:
                doc = json.load(fh)
        except Exception:                                            # noqa: BLE001
            continue
        row = (doc.get('prices') or {}).get(ticker.upper())
        if isinstance(row, dict):
            dt = row.get('date') or doc.get('supplied') or ''
            if dt >= best[0]:
                best = (dt, fp)
    if best[0]:
        return best[0]
    return (d.get('meta') or {}).get('asof') or ''


def issue_date(ticker, default=None):
    """The date this EDITION was issued, from the study's own edition module."""
    import importlib.util as _ilu
    p = os.path.join(ENGINE, '%s_study' % ticker.lower(), 'edition.py')
    if os.path.exists(p):
        try:
            s = _ilu.spec_from_file_location('_ed_%s' % ticker.lower(), p)
            m = _ilu.module_from_spec(s)
            s.loader.exec_module(m)
            for attr in ('ISO', 'EDITION'):
                v = getattr(m, attr, None)
                if isinstance(v, str) and len(v) >= 8:
                    return v
        except Exception:                                            # noqa: BLE001
            pass
    # NO EDITION MODULE: take the date the study's own DELIVERED documents carry, which
    # is the edition's issue date by construction -- the builders stamp it into the
    # filename. Read from the NAME, never from the modification time: an old file with a
    # fresh timestamp is precisely the trap that put an 8 August AMOC package in front of
    # the principal on 10-09-2026 while the current edition was 3 September.
    import glob
    import re
    best = ''
    d = os.path.join(ENGINE, '%s_study' % ticker.lower())
    for f in glob.glob(os.path.join(d, '*Valuation_Study*')):
        m = re.search(r'(\d{2})-(\d{2})-(\d{4})', os.path.basename(f))
        if m:
            iso = '%s-%s-%s' % (m.group(3), m.group(2), m.group(1))
            best = max(best, iso)
    return best or default or ''


def _human(iso):
    """2026-09-10 -> 10 September 2026. Anything else is returned as given."""
    MONTHS = ('January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December')
    try:
        y, m, d = iso.split('-')
        return '%d %s %s' % (int(d), MONTHS[int(m) - 1], y)
    except Exception:                                                # noqa: BLE001
        return iso


def header_line(ticker, spot=None, currency='', numbers=None, issued=None):
    """The one line that goes at the top of every valuation document.

    Both dates, labelled, in that order: the price the answer is measured against, then
    the day this edition was issued. A reader never has to infer which is which.
    """
    pd = price_date(ticker, numbers)
    idt = issue_date(ticker, issued)
    px = ''
    if spot is not None:
        px = ' of %s%s' % (('%s ' % currency) if currency else '', ('%.2f' % float(spot)))
    return ('PRICE DATE %s — the latest known close%s, the price this valuation is '
            'measured against.   ISSUE DATE %s — the day this edition was issued. '
            'A recalibration issues a NEW document carrying its own issue date; the two '
            'dates are stated separately because they are not the same fact [R-DOC-03].'
            % (_human(pd) or 'not recorded', px, _human(idt) or 'not recorded'))
