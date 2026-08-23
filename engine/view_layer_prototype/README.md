# View-Layer Prototype — 23-Aug-2026

**STATUS: PROTOTYPE. Not live, not published, no site file touched.** A
self-contained HTML mock of the proposed ticker-card redesign, built after the
23-Aug-2026 client critique ("the cone is very wide and has no direction").

**Revised same day under THREE-LENS INDEPENDENCE (Sherif, 23-Aug-2026, see
`Standing_Research_Protocol.md`):** the first cut drew direction as a fan
toward the fundamental fair values — retired, because the MC card's direction
must come from the MC's own price data, never from another lens. The card now
shows:

1. **The typical range leads.** The middle-half band of the published cone is
   the visual object; the 9-in-10 band demotes to a faint whisker. Same
   information, honest hierarchy. The drawn band is asserted at build time to
   reproduce the published p5/p25/p50/p75/p95 at both struck horizons (worst
   deviation this build: 0.15%) — the build fails rather than drift from the
   live site.
2. **The engine's own lean (illustrative).** An orange leaned center:
   alpha = IC × sigma_h × clip(z, ±2) — the exact Grinold form of the engine's
   existing signal socket — with IC from the tournament's surviving
   12-month-momentum cell for that market/horizon (zero lean where no cell
   survived) and z the stock's own momentum vs its own strictly-prior history.
   Labelled illustrative everywhere: it goes live only through the standing
   promotion gate. Momentum family only — technical-family survivors
   (200-day trend, 52-week-high) are excluded to keep MC ⊥ technical.
3. **Three lenses side by side, never blended.** A strip under each chart
   quotes the fundamental study's verdict and the computed technical trend as
   *separate* opinions beside the engine's lean. None feeds another;
   agreement is information.

Demo names: ETEL (engine leans up; fundamental independently agrees),
ADNOCDRILL (engine leans down; fundamental independently agrees), EMFD
(mild lean; the big fundamental upside stays in its own lens).

## Files

- `build_prototype.py` — generator (reads assets/data.js via node, the
  fv_overlay JSON for the published cone's shape parameters, the cleaned
  raw_ohlc history, and the tournament RESULTS; writes the HTML)
- `PROTOTYPE_23-08-2026.html` — the show piece (open in a browser; hover any
  chart)

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

The card layout into `assets/app.js` for all ticker pages needs only
published data plus the technical trend already stamped on each page. The
LEAN is separate: it ships only after the momentum candidate passes the
standing promotion gate (pre-registered forward shadow cohort recommended),
at which point it flows through `market_profiles` signal_active/ic like any
engine signal — no new machinery. Colors validated for color-vision safety
(teal #178A76 vs orange #D06A2C on the site paper, all six checks pass).
