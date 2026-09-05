"""Write this study's rebuild ledger [R-REBUILD-01] — every figure READ, none typed.

The route is walked on the LOWER of the two branches this study publishes. That is the
branch [R-GAP-02] turns on: a two-sided answer is held only if EVERY branch sits more
than the limit below the price, so the low branch is the one that has to clear the block
on its own, and walking the conservative branch is the reading that cannot flatter the
rebuild. Both branches are recorded on every lever, so the other route can be walked too.

  BEFORE  the study as delivered on 09-08-2026 (git HEAD~ of this directory's
          study_numbers.json), read out of the committed file rather than remembered.
  AFTER   this rebuild's own study_numbers.json.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
REPO = os.path.dirname(ENGINE)
sys.path.insert(0, ENGINE)
import rebuild_ledger as RL  # noqa: E402

REL = 'engine/borouge_study/study_numbers.json'


def committed(rev):
    """The delivered study's own numbers, off the commit rather than off memory."""
    raw = subprocess.run(['git', 'show', f'{rev}:{REL}'], cwd=REPO,
                         capture_output=True, text=True, check=True).stdout
    return json.loads(raw)


BEFORE = committed('HEAD')
AFTER = json.load(open(os.path.join(HERE, 'study_numbers.json')))

# The delivered answer was the MEDIAN of nine readings across two betas and two crux
# framings. Its low branch, in the sense used here, is that single published number:
# a blend has one value and no branches, which is the defect the first lever removes.
START = BEFORE['fair_mid']
START_SPOT = BEFORE['spot_aed']

# The two cash-flow readings on the ADOPTED tier-1 own-stock beta, at the OLD spot —
# the study's own committed lens table carries both, so the intermediate state is read
# and not reconstructed.
MID_LOW = BEFORE['lenses']['dcf_prolonged_own_beta']
MID_HIGH = BEFORE['lenses']['dcf_normalisation_own_beta']

END_LOW, END_HIGH = AFTER['fair_low'], AFTER['fair_high']
END_SPOT = AFTER['spot_aed']

led = RL.Ledger(
    ticker='BOROUGE',
    started_at=AFTER.get('rebuild_started_at', '2026-09-05'),
    start_value=START,
    start_spot=START_SPOT,
    audit_after=json.load(open(os.path.join(HERE, 'rebuild_ledger.json')))['audit_after'],
)

led.apply(
    'the nine-reading median retired for the class primary, published two-sided',
    'R-LENS-03',
    MID_LOW,
    why=(
        'the delivered central was the MEDIAN of nine readings spanning two costs of '
        'capital and two answers to the crux, which is a blend at equal weights nobody '
        'chose and nobody tested. Two defects rode inside it and each is worth more than '
        'the other. (i) FIVE of the nine were struck on a SECTOR bottom-up beta the study '
        'itself does not adopt — its own committed beta record carries a conforming '
        'tier-1 own-stock regression against the exchange index, so the median was half '
        'built on a cost of capital this study rejects, and every one of those five sits '
        'below every one of the four on the adopted beta. (ii) The remaining spread is '
        'the CRUX — whether navigation through the Strait of Hormuz is restored during '
        '2026 — and a median across a question with two answers publishes a number true '
        'under neither. [R-LENS-03] settles both: ONE class primary is the central, the '
        'other lenses are cross-checks published beside it, and where the answer turns on '
        'a judgement the reader is shown the judgement. The cash-flow lens on the adopted '
        'beta is the primary for this class; the book-value and relative-multiple reads '
        'stay as cross-checks; the normalised-earnings read and every sector-beta read '
        'come out of the answer entirely.'
    ),
    evidence=(
        'at the delivered spot the two branches on the adopted beta are '
        f'AED {MID_HIGH:.4f} if navigation normalises and AED {MID_LOW:.4f} if the '
        f'disruption persists, against the retired median of AED {START:.4f}; the '
        f'branch-to-branch spread is AED {MID_HIGH - MID_LOW:.4f} per share, and the '
        'median sat BELOW BOTH of them because the five sector-beta readings dragged it '
        'there. Both branches are carried in study_numbers.json under central_two_sided '
        'with the condition each one holds under, and the retired median is published '
        'beside them as what it was.'
    ),
)

led.apply(
    'the answer re-struck on the latest known price',
    'R-GAP-01',
    END_LOW,
    why=(
        'the study was struck against a close of AED '
        f'{START_SPOT:.2f} from 7 August 2026 and delivered against it a month later. '
        '[R-GAP-01] requires the central to be put against the LATEST KNOWN price before '
        'any delivery, and the price it publishes to be that same price with its date. '
        'The spot is not a decoration here: market-value equity weights are what '
        '[R-COC-01] requires, so the close feeds the capital structure and therefore the '
        'discount rate and therefore the answer. This lever moves the value only through '
        'that route — no driver, no path and no lens changed with it.'
    ),
    evidence=(
        f'AED {END_SPOT:.2f} at 3 September 2026, from the supplied close register. A '
        f'lower close lowers the market value of equity, raises the debt weight and '
        f'therefore lowers the cost of capital, which raises the value: the persistent '
        f'branch moves {MID_LOW:.4f} to {END_LOW:.4f} and the normalisation branch '
        f'{MID_HIGH:.4f} to {END_HIGH:.4f}, '
        f'{100 * (END_LOW / MID_LOW - 1):+.2f}% and '
        f'{100 * (END_HIGH / MID_HIGH - 1):+.2f}%. Both branches now sit at or above the '
        f'price ({100 * (END_LOW / END_SPOT - 1):+.1f}% and '
        f'{100 * (END_HIGH / END_SPOT - 1):+.1f}%), which is the side of '
        '[R-GAP-02] that releases rather than holds — and the release was not the reason '
        'for either lever, which is why the audit point was declared before the first one '
        'was touched.'
    ),
)

rec = led.record()
rec['branches'] = {
    'walked': 'the LOWER branch — disruption persists',
    'why': ('[R-GAP-02] holds a two-sided answer only if EVERY branch breaches, so the '
            'low branch is the one that must clear the block on its own. Walking it '
            'cannot flatter the rebuild.'),
    'start': {'value': START, 'note': 'a blend has one value and no branches'},
    'after_lens_lever': {'low': MID_LOW, 'high': MID_HIGH, 'spot': START_SPOT},
    'after_price_lever': {'low': END_LOW, 'high': END_HIGH, 'spot': END_SPOT},
    'high_branch_cumulative_move': END_HIGH / START - 1.0,
}
RL.assert_rebuild(rec, 'BOROUGE')
with open(os.path.join(HERE, 'rebuild_ledger.json'), 'w') as f:
    json.dump(rec, f, indent=1)
print(RL.render(rec))
print()
print('  high branch: %.4f -> %.4f (%+.1f%%)'
      % (START, END_HIGH, 100 * rec['branches']['high_branch_cumulative_move']))
