"""ARCC beta — RE-DERIVED against the PUBLISHED INDEX OF THE EXCHANGE, 01-Sep-2026.

WHY THIS FILE WAS REWRITTEN, AND WHAT IT REPLACES.

The retired version (kept beside this one as `beta_reg_composite_retired.py`)
regressed ARCC against an EQUAL-WEIGHT COMPOSITE built from the covered EGX
names. Its own docstring said so. That is a HARD FAIL under SIGCM clause 6 and
under the beta rule: a constituent composite is not a substitute and not a tier.
It changes whenever a stock is posted, and it shares constituents with the panel
it prices.

It is also the failure this repository has already paid for once. On FERTIGLB —
the first name run both ways — the composite gave beta 0.492 against the real
index's 0.931, a ~40% understatement that carried WACC from 11.90% to 8.53% and
overstated the centre by 21.6%. Every beta built on a composite is
non-conforming and must be re-derived before its study is re-issued. This is
that re-derivation, and it is the substantive reason ARCC sat in the campaign's
`reissue` tier.

WHAT THE CORRECT REGRESSION SAYS, AND WHY IT IS NOT ADOPTED.

`beta_regression.own_stock_beta('ARCC','EG','EGX')` — the only sanctioned route,
which resolves the regressor itself to engine/raw_indices/EG/EGX30.csv, runs
Step 0.0 on both series and matches the weekly grid to the EGX trading week —
returns beta 0.6981 on 253 weekly observations with **R-squared 0.047**, against
a usability floor of 0.05. IT FAILS THE GATE. Narrowly, but the gate is not a
suggestion, and the retired composite regression "passed" only because a
composite of the covered names co-moves with a covered name by construction.

So the strict preference order falls to TIER 2: a same-country peer beta. Five
Egyptian heavy-industrial names clear the gate against EGX30; the direct cement
peer, Suez Cement, does not (R-squared 0.025), which is itself worth recording —
neither Egyptian cement name is well explained by EGX30.

THE GAP IS FLAGGED, NOT PAPERED OVER: the peer betas are NOT unlevered and
re-levered, because peer balance sheets were not sourced from primary filings in
this run. The direction is known and it is conservative — ARCC runs net cash
(EGP 1,134mn of debt against EGP 3,459mn of cash), so re-levering to its own
structure would give a beta at or BELOW the peer median, a lower cost of equity
and a HIGHER value. The unadjusted peer median understates value.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))

import beta_regression as BR  # noqa: E402

PEERS = {
    'SCEM': 'Suez Cement — the direct cement peer',
    'EGAL': 'Egypt Aluminium — heavy industrial, energy-intensive',
    'ELEC': 'Electro Cable Egypt — heavy industrial',
    'SWDY': 'Elsewedy Electric — heavy industrial',
    'EGCH': 'Egyptian Chemical Industries — heavy industrial',
    'ABUK': 'Abu Qir Fertilizers — heavy industrial, gas-intensive',
}


def median(xs):
    xs = sorted(xs)
    if not xs:
        return None
    m = len(xs) // 2
    return xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2.0


def main():
    own = BR.own_stock_beta('ARCC', 'EG', 'EGX')

    peers = {}
    for tk, what in PEERS.items():
        r = BR.own_stock_beta(tk, 'EG', 'EGX')
        peers[tk] = dict(beta=r['beta'], r2=r['r2'], se=r['se'], n=r['n'],
                         usable=r['usable'], what=what)

    usable = {k: v for k, v in peers.items() if v['usable']}
    tier2 = median([v['beta'] for v in usable.values()])

    adopted_beta = own['beta'] if own['usable'] else tier2
    tier = 1 if own['usable'] else 2

    rec = dict(own)
    rec.update(
        ticker='ARCC', market='EG', exchange='EGX',
        conforming=True,
        peers=peers,
        tier2_peer_median=tier2,
        adopted=dict(
            beta_used=adopted_beta,
            tier=tier,
            basis=('tier-1 own-stock weekly regression against EGX30'
                   if tier == 1 else
                   'TIER 2 — same-country peer median. The own-stock regression '
                   'against the published EGX30 index FAILS the usability gate '
                   '(R2 %.3f < 0.05), so the strict preference order requires a '
                   'peer beta rather than the failing estimate.' % own['r2']),
            why=('Median of the %d usable Egyptian heavy-industrial regressions '
                 'against EGX30: %s. Suez Cement, the direct cement peer, is '
                 'excluded because it too fails the gate (R2 %.3f) — neither '
                 'Egyptian cement name is well explained by EGX30.'
                 % (len(usable),
                    ', '.join('%s %.4f' % (k, v['beta'])
                              for k, v in sorted(usable.items())),
                    peers['SCEM']['r2'])),
            gap='NOT unlevered and re-levered: peer balance sheets were not '
                'sourced from primary filings in this run. ARCC runs net cash, '
                'so re-levering to its own structure would give a LOWER beta and '
                'a HIGHER value — the unadjusted peer median understates value.',
            sensitivity_required=[0.63, 0.80, 1.0303, 1.15, 1.30],
        ),
        # Dual framing [the contested-judgement rule]: the adopted tier-2 peer
        # beta against the own-stock regression that failed the gate. Both are
        # published; neither is averaged into the other.
        dimson=dict(
            sum_beta=own['beta'],
            note='NOT a Dimson sum-beta. This slot carries the OWN-STOCK '
                 'regression against EGX30 (beta %.4f, R2 %.3f, n=%d), which '
                 'failed the usability gate and is published as the labelled '
                 'alternative framing beside the adopted tier-2 peer median. '
                 'Blume cross-check on the own-stock fit: %.4f.'
                 % (own['beta'], own['r2'], own['n'],
                    own.get('blume_crosscheck') or float('nan')),
        ),
        retired_composite=dict(
            beta=0.6280798261200432,
            note='The beta this study carried until 01-Sep-2026, regressed '
                 'against an equal-weight composite of the covered EGX names. '
                 'A constituent composite is a HARD FAIL, not a tier. Recorded '
                 'so the size of the correction is visible: 0.6281 -> %.4f.'
                 % adopted_beta,
        ),
    )
    out = os.path.join(HERE, 'beta_result.json')
    json.dump(rec, open(out, 'w'), indent=1, default=str)

    print('own-stock vs EGX30 : beta %.4f  R2 %.3f  se %.3f  n=%d  usable=%s'
          % (own['beta'], own['r2'], own['se'], own['n'], own['usable']))
    for k, v in sorted(peers.items()):
        print('  peer %-5s beta %.4f  R2 %.3f  usable=%s' % (k, v['beta'], v['r2'], v['usable']))
    print('ADOPTED tier %d beta %.4f   (retired composite was 0.6281)'
          % (tier, adopted_beta))
    print('index %s as of %s' % (own['index_file'], own['index_asof']))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
