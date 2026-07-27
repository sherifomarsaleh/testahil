"""refit_calendar_horizon.py — Step 0 gate re-run at the calendar 3-month horizon.

One-off adoption script for the 27-Jul-2026 horizon change. Runs the SAME
machinery as the unattended pipeline (panel_refresh.refresh_market) but with
tag='3m', so every window ends on the first session on or after
origin + 3 calendar months instead of on a fixed 60th session.

It writes nothing to production: update_registry=False, panels land in the
'3m' namespace, and the incumbent '60d' panels/fit are untouched. Output is a
comparison table for review — the standing PROMOTION RULE applies, so nothing
here enters the engine until a human reviews the PR.

  python3 refit_calendar_horizon.py            # every market with a library
  python3 refit_calendar_horizon.py EG SA      # named markets only
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auto_refresh import band_halfwidth, discover_touched_markets  # noqa: E402
from market_profiles import PROFILES                              # noqa: E402
from panel_refresh import refresh_market                          # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'PENDING_REVIEW', 'calendar_horizon_refit_3m.json')


def main(argv):
    libs = discover_touched_markets()
    want = [m for m in (argv or sorted(libs)) if m in libs]
    results = {}
    for m in want:
        files = libs[m]
        t0 = time.time()
        print(f"[{m}] {len(files)} names — refitting at calendar 3M ...",
              flush=True)
        try:
            r = refresh_market(m, files, files, update_registry=False, tag='3m')
        except Exception as e:                        # keep the sweep going
            print(f"[{m}] FAILED: {type(e).__name__}: {e}", flush=True)
            results[m] = dict(error=f"{type(e).__name__}: {e}")
            continue
        prof = PROFILES[m]
        old_bw = band_halfwidth(prof.nu, prof.width_cal)
        new_nu = 250.0 if isinstance(r['nu'], str) else r['nu']
        new_bw = band_halfwidth(new_nu, r['width_cal'])
        r['_incumbent'] = dict(nu=prof.nu, width_cal=prof.width_cal)
        r['_band_move_pct'] = round((new_bw / old_bw - 1) * 100, 3)
        r['_elapsed_s'] = round(time.time() - t0, 1)
        results[m] = r
        print(f"[{m}] nu {prof.nu} -> {r['nu']} | width_cal {prof.width_cal} "
              f"-> {r['width_cal']} | 90% band {r['_band_move_pct']:+.2f}% | "
              f"{r['market_verdict']} {r['market_skill']:+.4f} "
              f"CI{r['market_ci90']} | {r['windows']}w/{len(r['panel_names'])}n "
              f"| {r['_elapsed_s']}s", flush=True)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nwrote {OUT}")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
