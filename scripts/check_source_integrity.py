#!/usr/bin/env python3
"""[R-ENF-01] SIGCM CLAUSE 1 IS CHECKED FROM OUTSIDE, NOT ATTESTED FROM INSIDE.

SIGCM clause 1 has been a HARD GATE since July 2026 and says it in terms: HISTORICALS =
OFFICIAL SOURCES ONLY, no data vendors, brokers, press-as-a-numbers-source or third-party
estimates for the subject's reported historicals; if the official data cannot be obtained,
STOP AND INFORM. A violation is a hard fail — do not issue.

WHAT WAS CHECKING IT WAS A BOOLEAN THE STUDY SET ON ITSELF. That is the composite-beta
shape [R-ENF-01] closed everywhere else, and it had the predicted result: on 04-Sep-2026 two
delivered studies were found in plain breach, and one was measured against the filings it
should have used.

    SCEM took its revenue, profit and balance-sheet figures from Global Cement, cemnet,
    Daily News Egypt, Arab Finance and an aggregator's carry of S&P Global Market
    Intelligence — WHILE ITS AUDITED STATEMENTS SAT ON THE COMPANY'S OWN WEBSITE, six PDFs
    one click from the homepage and no authentication. Fetched and read against the study:

        shareholders' equity   EGP 6,020.3mn filed   against   5,240.0mn used   (-13.0%)
        cash and bank          EGP 4,762.3mn filed   against   3,850.0mn used   (-19.2%)
        depreciation, FY2025   EGP   122.5mn filed   against     418.1mn used   (+241%)
        operating profit       EGP 3,304.1mn filed   against an EBIT of 2,640.0 (-20.1%)

    Every one of those errors understates the company, which is the direction this
    reassessment exists to find. A reviewed 31-March-2026 balance sheet was on the same
    page, unread, carrying EGP 5,802.0mn of cash and a quarter's profit of EGP 1,114.5mn
    against a full prior year of 2,284.5mn.

THE POPULATION IS ANCHORED BOTH WAYS [R-ENF-04]: a run examining zero registers FAILS, and a
study whose register cannot be read is listed as UNREADABLE rather than skipped — because
unreadability is the cheapest route past any source check.

Ratcheted [R-ENF-02]: the two studies in breach today, and the seven whose register this
gate cannot read, are listed and allowed. The list may only ever SHORTEN.
"""
import argparse
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
import source_integrity as SI                                          # noqa: E402

RATCHET = os.path.join(ROOT, 'engine', 'build_depth_audit', 'source_outstanding.json')


def survey():
    """(breaches, unreadable, registers read)."""
    breaches, unreadable, read = {}, {}, 0
    for d in sorted(glob.glob(os.path.join(ROOT, 'engine', '*_study'))):
        tk = os.path.basename(d).replace('_study', '').upper()
        p = os.path.join(d, 'study_numbers.json')
        if not os.path.exists(p):
            unreadable[tk] = 'no committed numbers file'
            continue
        try:
            I = json.load(open(p)).get('inputs', {})
        except (ValueError, OSError) as exc:
            unreadable[tk] = 'numbers file will not parse: %s' % str(exc)[:50]
            continue
        if not isinstance(I, dict) or not I:
            unreadable[tk] = ('the input register is not in the committed numbers file, so '
                              'no source can be read from it')
            continue
        # A REGISTER CARRYING NO DATED HISTORICAL AT ALL IS UNREADABLE FOR THIS PURPOSE,
        # and the test is exact rather than a minimum count. Every study is built from the
        # company's reported past; one committing none of it has its register somewhere a
        # checker cannot reach, and committing five inputs would otherwise be the cheapest
        # route past a source check — declaration without execution, one level down.
        if not any(SI.is_dated_historical(k) for k in I):
            unreadable[tk] = ('the committed register carries no dated historical at all, '
                              'so there is no reported figure whose source can be read')
            continue
        read += 1
        bad = SI.audit(I)
        if bad:
            breaches[tk] = bad
    return breaches, unreadable, read


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prune', action='store_true',
                    help='rewrite the ratchet; it may only ever SHORTEN')
    a = ap.parse_args()

    breaches, unreadable, read = survey()
    r = json.load(open(RATCHET)) if os.path.exists(RATCHET) else {}
    allow_b = set(r.get('breaching', []))
    allow_u = set(r.get('unreadable', []))

    if read == 0:
        print('FAIL — read zero input registers. An absent answer is not a clean one.')
        return 1
    on_disk = {os.path.basename(d).replace('_study', '').upper()
               for d in glob.glob(os.path.join(ROOT, 'engine', '*_study'))}
    ghosts = sorted((allow_b | allow_u) - on_disk)
    if ghosts:
        print('FAIL — the ratchet names studies that do not exist on disk: %s'
              % ', '.join(ghosts))
        return 1

    print('%d input register(s) read; %d stud%s in breach; %d unreadable'
          % (read, len(breaches), 'y' if len(breaches) == 1 else 'ies', len(unreadable)))
    for tk in sorted(breaches):
        print('%s%-12s %d dated historical(s) sourced outside the filings'
              % ('   ' if tk in allow_b else '>> ', tk, len(breaches[tk])))
        for k, why, src in breaches[tk][:4]:
            print('       %-18s %s' % (k, why))
    for tk in sorted(unreadable):
        print('%s%-12s UNREADABLE — %s'
              % ('   ' if tk in allow_u else '>> ', tk, unreadable[tk]))

    new_b = sorted(set(breaches) - allow_b)
    new_u = sorted(set(unreadable) - allow_u)

    if a.prune:
        if allow_b and (set(breaches) - allow_b or set(unreadable) - allow_u):
            print('REFUSED — --prune may only ever SHORTEN; %s would be added'
                  % ', '.join(new_b + new_u))
            return 1
        json.dump({'rule': 'R-ENF-01 / SIGCM clause 1 checked from outside',
                   'note': "Studies sourcing the company's OWN dated historicals outside "
                           'its filings, and studies whose input register this gate cannot '
                           'read. May only ever SHORTEN. A breach closes by re-issuing the '
                           'study on its own statements; an unreadable one by committing '
                           'its register where a checker can reach it.',
                   'breaching': sorted(breaches),
                   'unreadable': sorted(unreadable)}, open(RATCHET, 'w'), indent=1)
        print('ratchet rewritten: %d breaching, %d unreadable'
              % (len(breaches), len(unreadable)))
        return 0

    if new_b or new_u:
        print('\nFAIL — SIGCM clause 1 is a HARD GATE and these are new:')
        for tk in new_b:
            print('   %-12s sources the company\'s own historicals outside its filings' % tk)
        for tk in new_u:
            print('   %-12s %s' % (tk, unreadable[tk]))
        return 1
    print('\nOK — no new breach and no newly unreadable register. %d breaching and %d '
          'unreadable on the ratchet, which may only SHORTEN.' % (len(allow_b), len(allow_u)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
