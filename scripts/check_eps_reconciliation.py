#!/usr/bin/env python3
"""WHAT STANDS BETWEEN PROFIT AND SHAREHOLDERS, WHICH APPEARS IN NO LINE OF THE
INCOME STATEMENT [L-294].

    python3 scripts/check_eps_reconciliation.py [--prune]

WHY THIS EXISTS. A valuation ends by dividing an equity value by a share count. Every
gate in this repository checks how that equity value was BUILT — the bridge, the lenses,
the terminal, the cost of capital — and not one asks whether the number being divided is
the number shareholders actually receive.

WHAT WAS FOUND. Egyptian company law gives employees a share of distributable profits.
El Sewedy discloses it in its earnings-per-share note, BELOW profit attributable to
owners, because it is an appropriation of profit rather than an operating cost — so it
appears in no line of the income statement and no cost driver can capture it. It ran
11.6%, 12.0% and 13.0% of attributable profit in FY2024, FY2025 and H1-2026.

That study registered attributable profit of EGP 17,330.245mn AND the company's own
reported EPS of 7.13, both correctly sourced to the audited statements. 17,330.245 /
2,140.778 shares = 8.095. The two figures disagreed by exactly the employees' share, and
the valuation divided by the full count, handing shareholders about 12% of value the
statute gives to somebody else. NOTHING RECONCILED THEM, and the word "employee" occurred
nowhere in the study's committed numbers.

THE MECHANISM IS NOT EGYPTIAN AND NOT UNUSUAL. Anywhere the EPS numerator differs from
attributable profit there is a claim ahead of ordinary shareholders: a statutory profit
share, a preference dividend, a participating instrument, an ESOP allocation, a
weighted-average count against a period-end count.

WHAT THIS CHECKS. Exactly one arithmetic identity, on figures a study already holds:

    committed attributable profit / committed share count  ==  committed reported EPS

within the rounding of the EPS as printed. Where it does not reconcile, the study must
NAME the difference in an `eps_reconciliation` record — what it is, what it is worth, and
whether the valuation charges it. A named difference passes; an unnamed one fails.

WHAT IT DELIBERATELY DOES NOT CHECK. Whether the study is right to charge or not charge
the item — a company that retains rather than distributes may face a smaller statutory
share, and a cap on the charge is a real modelling question. This gate asks only that the
gap be SEEN. A study may declare the difference and value it at zero with a reason.

THE POPULATION IS ANCHORED ON THE STUDY DIRECTORIES [R-ENF-04], and a study registering
no reported EPS is UNREADABLE rather than clean: it is the state that made the original
defect invisible, so it is counted and listed rather than skipped. A run that read zero
studies FAILS.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENGINE = os.path.join(ROOT, 'engine')
OUTSTANDING = os.path.join(ENGINE, 'build_depth_audit', 'eps_outstanding.json')

# Key SHAPES rather than a fixed list: registers across this book name the same quantity
# four ways, which is [R-BETA-04]'s finding, and a list of names cannot be complete.
EPS_KEY = re.compile(r'^eps(_|$)|(_|^)eps_fy\d{2,4}$|reported_eps', re.I)
NPA_KEY = re.compile(r'^np(a)?_fy\d{2,4}$|^net_profit_fy\d{2,4}$|attrib.*profit', re.I)
YEAR = re.compile(r'(\d{2,4})\s*$')


def _year(key):
    m = YEAR.search(key)
    if not m:
        return None
    y = m.group(1)
    return int(y) if len(y) == 4 else 2000 + int(y)


def read(path):
    """(reported eps, attributable profit, shares, year) for the LATEST year both exist."""
    D = json.load(open(path, encoding='utf-8'))
    I = D.get('inputs') or {}
    sh = (D.get('meta') or {}).get('shares_mn')
    eps, npa = {}, {}
    for k, v in I.items():
        val = v.get('value') if isinstance(v, dict) else None
        if not isinstance(val, (int, float)):
            continue
        y = _year(k)
        if y is None:
            continue
        if EPS_KEY.search(k):
            eps[y] = (val, k)
        elif NPA_KEY.search(k):
            npa[y] = (val, k)
    common = sorted(set(eps) & set(npa))
    if not common or not sh:
        return None, None, sh, None, D
    y = common[-1]
    return eps[y], npa[y], sh, y, D


def main(argv):
    prune = '--prune' in argv
    d, known = {}, set()
    if os.path.exists(OUTSTANDING):
        d = json.load(open(OUTSTANDING, encoding='utf-8'))
        known = set(d.get('outstanding', []))

    dirs = sorted(glob.glob(os.path.join(ENGINE, '*_study')))
    if not dirs:
        print('FAIL - the population is empty: no engine/*_study directories found '
              '[R-ENF-04].')
        return 1

    read_n, bad, clean, unreadable = 0, {}, [], []
    for dd in dirs:
        tk = os.path.basename(dd)[:-6].upper()
        nf = os.path.join(dd, 'study_numbers.json')
        if not os.path.exists(nf):
            unreadable.append((tk, 'no committed numbers file'))
            continue
        try:
            eps, npa, sh, y, D = read(nf)
        except Exception as e:
            unreadable.append((tk, 'numbers file will not parse: %s' % e))
            continue
        read_n += 1
        if eps is None:
            unreadable.append((tk, 'registers no reported earnings per share beside its '
                                   'attributable profit, so the gap cannot be seen'))
            continue
        eps_v, eps_k = eps
        npa_v, npa_k = npa
        if not eps_v:
            unreadable.append((tk, 'reported earnings per share is zero'))
            continue
        computed = npa_v / sh
        # tolerance from the PRINTED rounding of the EPS, never chosen: half a unit in the
        # last decimal it is stated to, plus a share-count rounding allowance.
        dec = len((('%r' % eps_v).split('.') + [''])[1])
        tol = max(0.5 * 10 ** -dec, abs(eps_v) * 1e-3)
        gap = computed - eps_v
        rec = (D.get('eps_reconciliation') or {})
        # A RATIO IN THE HUNDREDS IS NOT A PROFIT SHARE, IT IS A UNIT MISMATCH, and
        # conflating the two makes the gate useless for both. Re-pointed rather than
        # widened [R-COC-01]: the first run fired at +102,936% on a study registering
        # profit in local-currency THOUSANDS against an EPS quoted in dollars. That is a
        # real defect — two figures on different bases with nothing saying so, which is
        # exactly the state that hides the thing this gate looks for — but it is a
        # different finding and it is reported as one.
        ratio = abs(computed / eps_v) if eps_v else float('inf')
        if ratio > 3.0 or ratio < 1 / 3.0:
            unreadable.append((tk, 'attributable profit %s (%.4f) over %.4f shares gives '
                                   '%.4f against a reported %s of %.4f — a factor of %.0f. '
                                   'These are not on the same basis (units, currency or '
                                   'scale) and nothing in the register says so, so the '
                                   'reconciliation cannot be read at all.'
                               % (npa_k, npa_v, sh, computed, eps_k, eps_v,
                                  max(ratio, 1 / ratio))))
            continue
        if abs(gap) <= tol:
            clean.append('%-12s FY%s  %.4f computed against %.4f reported'
                         % (tk, y, computed, eps_v))
        elif rec.get('difference') and rec.get('what'):
            clean.append('%-12s FY%s  %+.1f%% gap, NAMED: %s'
                         % (tk, y, 100 * gap / eps_v, str(rec['what'])[:60]))
        else:
            bad.setdefault(tk, []).append(
                'attributable profit %s (%.4f) over %.4f shares gives %.4f against a '
                'reported %s of %.4f - a gap of %+.1f%%, and no eps_reconciliation record '
                'names what stands between them.'
                % (npa_k, npa_v, sh, computed, eps_k, eps_v, 100 * gap / eps_v))

    if read_n == 0:
        print('FAIL - %d study directories and not one committed numbers file was read '
              '[R-ENF-04].' % len(dirs))
        return 1

    print('study directories: %d   numbers files read: %d   reconciled or named: %d   '
          'unreadable: %d' % (len(dirs), read_n, len(clean), len(unreadable)))
    for line in clean:
        print('   ok   ' + line)
    if unreadable:
        print('\nUNREADABLE (%d) - an absent answer is not a clean one:' % len(unreadable))
        for tk, why in unreadable:
            print('   %-12s %s' % (tk, why))

    if prune:
        still = sorted(t for t in known if t in bad)
        json.dump({'outstanding': still, 'note': d.get('note', '')},
                  open(OUTSTANDING, 'w', encoding='utf-8'), indent=1)
        print('\npruned: %d -> %d' % (len(known), len(still)))
        return 0

    new = {t: v for t, v in bad.items() if t not in known}
    if bad:
        print()
    for t in sorted(bad):
        for line in bad[t]:
            print('   %-12s %s   %s' % (t, line, '[outstanding]' if t in known else '[NEW]'))
    if new:
        print('\nFAIL - %d study/studies newly unreconciled: %s'
              % (len(new), ', '.join(sorted(new))))
        return 1
    print('\nOK - no new violations. %d on the ratchet, which may only SHORTEN.' % len(known))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
