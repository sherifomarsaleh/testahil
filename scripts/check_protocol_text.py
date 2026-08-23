#!/usr/bin/env python3
"""Read the governing documents the way a reader would, and fail on what breaks.

WHY THIS EXISTS
    On 23-Aug-2026 four consecutive rounds of "is this the version to adopt?" each
    turned up a real defect in the protocol text: a clause that contradicted itself
    four sentences apart, a stock count that had gone false, a second count that would
    go false on the next posting, and a stale copy indistinguishable from a current one.

    Every one was found by a HUMAN pasting 55,000 characters back and asking. That is
    the wrong place for the check to live. The reader was doing the author's quality
    pass, one round at a time, and each round cost a full re-read.

    This runs the same four checks mechanically, before anything is sent. It does not
    replace reading the text -- [R-ENF-01] is explicit that some rules can only be prose
    and only a reader can judge them -- it removes the four failures that are mechanical.

WHAT IT CHECKS
    1. every file path the documents name actually exists
    2. every module symbol they name actually imports
    3. no live/volatile count is stated as a current fact (dated findings are fine:
       the block's own opening rule says stock counts go stale the moment a stock posts)
    4. the DFM interim clause does not both hold the interim open and promise to
       replace it -- the specific contradiction that shipped
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
DOCS = {'digest': os.path.join(ENGINE, 'PROJECT_INSTRUCTIONS_11-07-2026.md'),
        'full protocol': os.path.join(ENGINE, 'Standing_Research_Protocol.md')}
sys.path.insert(0, ENGINE)

SYMBOLS = {
    'wacc_builder':      ['EXCHANGE_INDEX', 'INTERIM_INDEX', 'index_interim_note', 'market_index_path'],
    'research_protocol': ['assert_sigcm', 'assert_beta_provenance', 'assert_model_study',
                          'assert_ground_up', 'STANDARD_VERSION', 'REFERENCE_SET'],
    'beta_regression':   ['own_stock_beta'],
    'adaptive_width':    ['live_width_mult'],
    'horizons':          ['resolve'],
}

PATH = re.compile(r'\b(?:engine|scripts|assets|\.github)/[A-Za-z0-9_./{}-]+')
# A count of the CURRENT book is a defect: it goes false silently on the next posting, and
# the block's own opening rule forbids it. A count describing a MEASUREMENT that was taken
# is evidence, and the protocol is built on exactly that -- the 27-name CLHO composite, the
# 30-name LONO panel, the 17-name UAE library. Both look like "N names" to a regex.
#
# A first attempt flagged both and fired 19 times on correct text. Under [R-ENF-02] that is
# the permanently-red check everyone learns to ignore, so this is now narrowed to the two
# shapes that ACTUALLY shipped a false statement -- a present-tense claim about what the
# book holds. Narrow and always right beats broad and ignored.
COUNT = re.compile(
    r'(?:\b(?:holds|covers|carries|contains)\s+(?:\*\*)?\d{1,3}\s+(?:ADX|DFM|EGX|TADAWUL|QSE|KRX|NSE|NASDAQ|covered)\b'
    r'|\b\d{1,3}-name\s+covered\s+panel\b'
    r'|\bagainst\s+a\s+\d{1,3}-name\s+(?:covered\s+)?panel\b)', re.I)
DATED = re.compile(r'\b(?:on \d{1,2}-[A-Za-z]{3}-\d{4}|at that date|then-covered|at the time|'
                   r'\d{1,2} [A-Z][a-z]{2} \d{4}|the test was run against|the measurement is)\b')


def check_paths(text, label, fails):
    named = {p.rstrip('.,;:)') for p in PATH.findall(text) if '{' not in p}
    # a dotted module reference (engine/beta_regression.own_stock_beta) is a symbol, not a path
    named = {p for p in named if not re.search(r'\.py\.\w|\.\w+$', p) or p.endswith(('.py', '.js', '.md', '.json', '.csv', '.yml'))}
    missing = sorted(p for p in named if not os.path.exists(os.path.join(ROOT, p)))
    print(f'  paths named {len(named):3d}   missing {len(missing)}')
    for m in missing:
        print(f'      MISSING PATH  {m}')
        fails.append(f'{label}: names a file that does not exist ({m})')


def check_symbols(fails):
    missing = []
    for mod, names in SYMBOLS.items():
        try:
            m = __import__(mod)
        except Exception as e:
            missing.append(f'{mod} (import failed: {e})')
            continue
        missing += [f'{mod}.{n}' for n in names if not hasattr(m, n)]
    print(f'  symbols named {sum(len(v) for v in SYMBOLS.values()):3d}   missing {len(missing)}')
    for m in missing:
        print(f'      MISSING SYMBOL  {m}')
        fails.append(f'names a symbol that does not exist ({m})')


def _sentence_around(text, i):
    """The sentence the match sits in — NOT a character window.

    A window let a legitimate "at the time" in the NEXT sentence exempt a false count in
    this one, and the negative control caught it. An exemption must belong to the claim it
    exempts.
    """
    start = max(text.rfind('. ', 0, i), text.rfind('\n', 0, i), 0)
    end = text.find('. ', i)
    return text[start:end if end > i else min(len(text), i + 400)]


def check_live_counts(text, label, fails):
    bad = []
    for m in COUNT.finditer(text):
        if DATED.search(_sentence_around(text, m.start())):
            continue
        bad.append(re.sub(r'\s+', ' ', text[max(0, m.start() - 70): m.end() + 70]).strip())
    print(f'  undated live counts {len(bad)}')
    for b in bad:
        print(f'      LIVE COUNT  …{b}…')
        fails.append(f'{label}: states a volatile count as a current fact')


def check_dfm_contradiction(text, label, fails):
    i = text.find('AE/DFM RUNS AN INTERIM')
    if i < 0:
        i = text.find('The DFM interim')
    if i < 0:
        return
    # Stop at the END of the DFM clause. A first cut read 6,000 characters and ran on into
    # "no conforming beta is possible there until one is supplied" -- which is about BR and
    # GB, is correct, and is none of this check's business.
    end = text.find('STILL NOT REGISTERED', i)
    if end < 0:
        end = text.find('Where the exchange comes from', i)
    clause = text[i:end if end > i else i + 4000]
    if 'until one is supplied' in clause and ('DECLINED' in clause or 'declined' in clause):
        print('      CONTRADICTION  the DFM clause both holds the interim open and promises to replace it')
        fails.append(f'{label}: DFM clause contradicts itself')
    else:
        print('  DFM clause coherent')


def main():
    fails = []
    check_symbols(fails)
    for label, path in DOCS.items():
        print(f'\n{label}:')
        text = open(path, encoding='utf-8').read()
        check_paths(text, label, fails)
        check_live_counts(text, label, fails)
        check_dfm_contradiction(text, label, fails)
    print()
    if fails:
        print(f'FAIL ({len(fails)}):')
        for f in fails:
            print('   ', f)
        return 1
    print('OK — the governing documents name nothing that does not exist, carry no undated '
          'live count, and do not contradict themselves where they did before.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
