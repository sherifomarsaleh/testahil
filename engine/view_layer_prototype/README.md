# View-Layer Prototype — 23-Aug-2026

**STATUS: PROTOTYPE. Not live, not published, no site file touched.** This
folder holds a self-contained HTML mock of the proposed ticker-card redesign,
built for review after the 23-Aug-2026 client critique ("the cone is very
wide and has no direction").

## What it shows

Three real covered names (ETEL — view up and playable; ADNOCDRILL — view
down; EMFD — worth far more but not on a 3-month clock), each drawn ONLY from
numbers already published on the live site today:

1. **The typical range leads.** The middle-half band of the published cone is
   the visual object; the 9-in-10 band demotes to a faint whisker. Same
   information, honest hierarchy — the live pages currently lead with the
   widest band on the page.
2. **Direction is a second object, not a wider first one.** The orange path
   runs from today's price to the study's bear/base/full values over 12
   months. Teal = the market's odds; orange = our view. The calibrated cone
   is untouched — the view is drawn beside it, never into it.
3. **A plain-English verdict line** whose every number is computed from the
   published data (gap, odds of touching the base value within 3M from
   `fv_overlay`, and the reachability wording for names whose value case
   cannot play out in a quarter).

The drawn market band is asserted at build time to reproduce the published
p5/p25/p50/p75/p95 at both struck horizons (worst deviation on this build:
0.15%); the build fails rather than show a band that drifts from the site.

## Files

- `build_prototype.py` — generator (reads assets/data.js via node, the
  fv_overlay JSON, and the cleaned raw_ohlc history; writes the HTML)
- `PROTOTYPE_23-08-2026.html` — the show piece (open in any browser; hover
  any chart for the numbers at that date)

## Reproduce

    python3 engine/fv_overlay.py --json /tmp/overlay.json
    python3 engine/direction_tournament/tournament.py --generated 2026-08-23 \
        --json engine/direction_tournament/RESULTS_23-08-2026.json \
        --md engine/direction_tournament/RESULTS_23-08-2026.md
    python3 engine/view_layer_prototype/build_prototype.py \
        --overlay /tmp/overlay.json \
        --tournament engine/direction_tournament/RESULTS_23-08-2026.json \
        --out engine/view_layer_prototype/PROTOTYPE_23-08-2026.html

## What adoption would involve (deliberately out of scope here)

Wiring the card into `assets/app.js` for all ~90 ticker pages (the fan data
is already on every page; the fv_overlay odds would need a small generated
include), a pass through the standing site-verification gates, and Sherif's
publish instruction. The orange path is a display of the study's existing
fair values — it is not a forecast object, carries no new fitted parameter,
and would be labelled as the house view distinct from the calibrated cone.
Colors validated for color-vision safety (teal #178A76 vs orange #D06A2C,
all six checks pass on the site's paper surface).
