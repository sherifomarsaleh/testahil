#!/usr/bin/env python3
"""adopt_calibration.py — the sanctioned way to say YES to a material calibration change.

WHY THIS EXISTS (23-Aug-2026). auto_refresh.py's materiality gate could say STOP but
there was no documented way to say GO. The gate opened a review PR whose own closing
line reads "either merge this PR to accept, or re-run with a corrected raw_ohlc/ input"
— except merging accepts NOTHING: the workflow stages only engine/PENDING_REVIEW and
engine/panels, and market_profiles.py is deliberately never written for a material
market. So the instruction was not executable, adopting meant hand-editing production,
and nobody did. 66 review PRs accumulated between 6-Aug and 23-Aug-2026, every one
re-reporting the same standing finding, and 18 names across EG/AE/SA sat outside any
applied fit — ADNOCLS, DU, MODON, FERTIGLB and SAVOLA among them, all with live pages.

A gate with no release is not a gate, it is a stall. This is the release.

WHAT IT DOES NOT DO. It does not re-decide materiality, soften a verdict, or pick a
config. It re-runs the SAME production chain auto_refresh.py runs, prints the incumbent
against the proposal including the move in the published 90% cone, and — only when a
human passes --yes — writes it through auto_refresh.write_production(), which is
import-verified (the nu=Gaussian precedent: a bare identifier parses and dies only at
import, and that bug once reached main). No second code path, no hand-edit.

Usage:
  python3 scripts/adopt_calibration.py                    # show every market, change nothing
  python3 scripts/adopt_calibration.py --markets EG,AE    # show just these
  python3 scripts/adopt_calibration.py --markets EG --yes # adopt EG
  python3 scripts/adopt_calibration.py --all --yes        # adopt everything proposed
"""
import argparse
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(os.path.dirname(HERE), 'engine')
sys.path.insert(0, ENGINE)

import auto_refresh as ar                                            # noqa: E402
from market_profiles import PROFILES                                 # noqa: E402
from panel_refresh import refresh_market                             # noqa: E402


def _fmt(v):
    return '—' if v is None else (f"{v:.4f}" if isinstance(v, float) else str(v))


def report(market, result, incumbent, registry):
    """Print the incumbent against the proposal. Returns the reasons list."""
    material, reasons, added = ar.assess_materiality(market, result, incumbent, registry)

    old_bw = ar.band_halfwidth(incumbent.nu, incumbent.width_cal)
    new_bw = ar.band_halfwidth(result['nu'], result['width_cal'])
    move = (new_bw - old_bw) / old_bw if (old_bw and new_bw) else None

    print(f"\n=== {market} ===")
    print(f"  {'':22} {'IN PRODUCTION':>22} {'PROPOSED':>22}")
    print(f"  {'nu':22} {_fmt(incumbent.nu):>22} {_fmt(result['nu']):>22}")
    print(f"  {'width_cal':22} {_fmt(incumbent.width_cal):>22} {_fmt(result['width_cal']):>22}")
    print(f"  {'panel names':22} {len(registry.get('panel_names', [])):>22} "
          f"{len(result['panel_names']):>22}")
    print(f"  {'windows':22} {registry.get('windows', '—'):>22} {result['windows']:>22}")
    print(f"  {'market verdict':22} {str(registry.get('market_verdict', '—')):>22} "
          f"{result['market_verdict']:>22}")
    print(f"  {'90% cone half-width':22} {_fmt(old_bw):>22} {_fmt(new_bw):>22}"
          + (f"   ({move:+.2%})" if move is not None else ""))
    if added:
        print(f"  entering the fit for the first time: {', '.join(added)}")
    if material:
        print("  MATERIAL — a human must decide:")
        for r in reasons:
            print(f"    - {r}")
    else:
        print("  not material")
    return material, reasons


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--markets', default='', help='comma-separated market codes')
    ap.add_argument('--all', action='store_true', help='every market with raw files')
    ap.add_argument('--yes', action='store_true',
                    help='actually write market_profiles.py + fitted_configs.json')
    args = ap.parse_args()

    touched = ar.discover_touched_markets()
    if args.markets:
        want = [m.strip().upper() for m in args.markets.split(',') if m.strip()]
        unknown = [m for m in want if m not in touched]
        if unknown:
            sys.exit(f"no raw files for: {', '.join(unknown)}")
    elif args.all:
        want = sorted(touched)
    else:
        want = sorted(touched)

    registry = json.load(open(ar.REGISTRY_PATH)) if os.path.exists(ar.REGISTRY_PATH) else {}
    adopted, skipped = [], []

    for market in want:
        try:
            result = refresh_market(market, touched[market], touched[market],
                                    update_registry=False, tag=ar.HORIZON_TAG)
        except Exception as exc:
            print(f"\n=== {market} ===\n  PIPELINE ERROR — not adopted: {exc}")
            skipped.append(market)
            continue

        material, reasons = report(market, result, PROFILES[market],
                                   registry.get(market, {}))

        if not args.yes:
            continue

        ar.write_production(market, result)
        adopted.append(market)
        print(f"  -> ADOPTED: written to market_profiles.py + fitted_configs.json")

        # The evidence for a material adoption is committed alongside it, not just
        # printed. A config that moved for a reason nobody can read later is a config
        # nobody can audit.
        if material:
            path = ar.write_pending_review(market, result, reasons, PROFILES[market])
            adopted_note = (
                f"\n---\n\n## ADOPTED {datetime.date.today().isoformat()}\n\n"
                f"Reviewed and accepted by a human via scripts/adopt_calibration.py. "
                f"market_profiles.py and fitted_configs.json now carry this fit; the "
                f"table above is the evidence it was adopted on.\n")
            with open(path, 'a') as f:
                f.write(adopted_note)
            print(f"  -> evidence retained at {os.path.relpath(path, os.path.dirname(HERE))}")

    print()
    if not args.yes:
        print("DRY RUN — nothing written. Re-run with --yes to adopt.")
    else:
        print(f"adopted: {', '.join(adopted) if adopted else 'none'}"
              + (f" | skipped: {', '.join(skipped)}" if skipped else ""))
    return 0


if __name__ == '__main__':
    sys.exit(main())
