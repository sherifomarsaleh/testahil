#!/usr/bin/env python3
"""A PUBLISHED FAIR VALUE WITH NO STUDY BEHIND IT IS EXAMINED BY NOTHING.  [R-ENF-01]

WHY THIS EXISTS
    Every construction gate in this repository — the bridge, the lens design, the macro
    path, the cost-of-capital schedule, the forecast anchor, the valuation-input block, the
    document and workbook shape, the prose figures, the sweep — takes a STUDY DIRECTORY as
    its subject. `engine/*_study/`. That is the right subject for each of them and it is why
    each of them works.

    It also means that a name with no study directory is examined by NONE of them. Measured
    on 3 September 2026, through a real JavaScript load of the site's own data file:

        90 names carry a published fair value
        22 have a study directory
        68 DO NOT

    So the construction gates are silent about 76% of what this house publishes. Not
    passing it — silent about it. The 22 examined names average a much larger discount to
    price than the 68 unexamined ones, which is a fact about which names got studied and
    not evidence about the rest.

    That gap was known: it was measured during the valuation calibration and written into
    the programme state. What it did not have was an instrument, so it could not go red, it
    could not shorten, and nothing would notice if it grew. A number in a status note is a
    number that rots [R-DOC-02]; a ratchet that may only shorten is a commitment.

WHAT IT CHECKS
    1. every ticker the site publishes a fair value for either HAS a study directory or is
       listed on the ratchet
    2. no NEW name may be published without one — a fair value that reaches a reader with
       no study behind it is the one thing this whole design cannot examine
    3. the list may only ever get SHORTER: each name that gains a study comes off it

    The fair values are read through a real `node` load of assets/data.js rather than a
    regex [R-ENF-03], for the reason that rule records: a regex returns the FIRST match and
    a JavaScript object literal takes the LAST, so a duplicated key means every regex tool
    inspects the half the reader never sees.

WHAT IT DELIBERATELY DOES NOT DO
    It does not require the 68 to be studied today — that is Phase 2 of the programme and
    68 studies is not a thing a gate can demand. It requires the number to be VISIBLE, to
    be counted somewhere other than a note, and to move in one direction only.

USAGE
    python3 scripts/check_published_coverage.py          # gate
    python3 scripts/check_published_coverage.py --prune  # drop names that gained a study
"""
import glob
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
OUTSTANDING = os.path.join(ENGINE, 'build_depth_audit', 'coverage_outstanding.json')

READ_JS = r'''
const fs=require('fs'),vm=require('vm'),ctx={};vm.createContext(ctx);
vm.runInContext(fs.readFileSync(process.argv[1],'utf8')+';globalThis.__X={TICKERS};',ctx);
const T=ctx.__X.TICKERS, out={};
for (const k of Object.keys(T)) {
  const t=T[k];
  if (t && t.fair && (t.fair.base!==undefined || t.fair.bear!==undefined)) {
    out[k]=(t.code||'');
  }
}
console.log(JSON.stringify(out));
'''


def published():
    """Every name the site publishes a fair value for, through a real JS load [R-ENF-03]."""
    data = os.path.join(ROOT, 'assets', 'data.js')
    if not os.path.exists(data):
        raise SystemExit('FAIL — assets/data.js is not present. An absent site file is not '
                         'an empty one [R-ENF-04].')
    r = subprocess.run(['node', '-e', READ_JS, data],
                       capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        raise SystemExit('FAIL — assets/data.js would not LOAD in node: %s\nA file that '
                         'parses is not a file that loads, and a regex reader would have '
                         'inspected the half the reader never sees [R-ENF-03].'
                         % (r.stderr or '').strip()[:300])
    return json.loads(r.stdout)


def main(argv):
    pub = published()
    if not pub:
        print('FAIL — the site publishes no fair value at all. An empty result is not a '
              'clean result [R-ENF-04]: either data.js changed shape or this reader is '
              'looking at the wrong key.')
        return 1
    studies = {os.path.basename(d)[:-len('_study')].upper()
               for d in glob.glob(os.path.join(ENGINE, '*_study'))}
    if not studies:
        print('FAIL — no study directories found. The comparison has no second population '
              '[R-ENF-04].')
        return 1

    known = {}
    if os.path.exists(OUTSTANDING):
        known = json.load(open(OUTSTANDING, encoding='utf-8')).get('entries', {})

    have = sorted(k for k in pub if k.upper() in studies)
    lack = sorted(k for k in pub if k.upper() not in studies)

    print('PUBLISHED FAIR VALUES AND THE STUDIES BEHIND THEM')
    print('   read through a real node load of assets/data.js [R-ENF-03]')
    print('   %d published · %d with a study · %d without\n'
          % (len(pub), len(have), len(lack)))
    from collections import Counter
    ex = Counter((pub[k].split(':')[0] if ':' in pub[k] else '?') for k in lack)
    if ex:
        print('WITHOUT A STUDY, by exchange: '
              + ' · '.join('%s %d' % (e, n) for e, n in ex.most_common()))

    now_have = sorted(k for k in known if k in have or k.upper() in studies)
    if now_have:
        print('\nNOW STUDIED — remove from the list (%d): %s'
              % (len(now_have), ', '.join(now_have)))

    stranded = sorted(k for k in known if k not in pub)
    if '--prune' in argv:
        keep = {k: v for k, v in known.items() if k not in now_have and k in pub}
        for k in lack:
            keep.setdefault(k, 'published fair value, no study directory — Phase 2 of the '
                               'method reassessment')
        json.dump({'note': ('Names whose fair value the site publishes with no study '
                            'directory behind it, as at the adoption of this gate '
                            '(03-Sep-2026). Every construction gate in this repository '
                            'takes a study directory as its subject, so each of these is '
                            'examined by NONE of them. Allowed to fail; the list may only '
                            'ever get SHORTER. --prune rewrites it.'),
                   'entries': keep},
                  open(OUTSTANDING, 'w', encoding='utf-8'), indent=1, sort_keys=True)
        open(OUTSTANDING, 'a', encoding='utf-8').write('\n')
        print('\npruned; %d entry/entries remain' % len(keep))
        return 0

    rc = 0
    if stranded:
        print('\nFAIL — %d listed name(s) no longer carry a published fair value: %s'
              % (len(stranded), ', '.join(stranded)))
        print('The population this list is held against must exist [R-ENF-04]. A name that '
              'stopped being published comes off the list.')
        rc = 1
    new = [k for k in lack if k not in known]
    if new:
        print('\nFAIL — %d name(s) publish a fair value with no study directory and no '
              'entry either way: %s' % (len(new), ', '.join(new)))
        print('\nEvery construction gate here takes a study directory as its subject, so a '
              'published fair value without one is examined by NOTHING — not passed, '
              'silent. Build the study, or list the name and accept that it is unexamined; '
              'what may not happen is a new fair value reaching a reader with neither.')
        rc = 1
    if rc == 0:
        print('\nOK — no newly published fair value lacks a study, and the list has not '
              'grown.')
    return rc


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
