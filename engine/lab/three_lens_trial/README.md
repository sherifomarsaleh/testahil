# three_lens_trial — the three-clocks canvas (PHDC + GBCO), 26-Aug-2026

A display-layer trial requested 26-Aug-2026: bring the three lenses together **visually** —
technical analysis for immediate entry/exit reference, the MC cone for the 1–3-month price
range, and the fundamental fair-value range for the ~12-month horizon — on one price axis
per name. PHDC and GBCO are the trial pair.

**What it is:** one generated, standalone page (`three_lens_trial.html`) with, per name, a
zoned canvas (6 months of history → the forecast window with the S/R ladder over the cone →
a fair-value bracket on its own 12-month shelf, behind an explicit clock break), an
alignment strip (spot → MC 3M median → fair base, with computed gaps), and the three lens
cards. Hover/focus reads out only published points — nothing is interpolated.

**What it deliberately is not:**
- Not an integration. [R-LENS-01] holds by construction — the builder reads each lens's
  *published output* and draws them side by side; nothing feeds anything. Same standing as
  fv_overlay: a comparison surface.
- Not hand-typed. Every numeral is machine-read from `assets/data.js` (through a real JS
  parse, per R-ENF-03), the LEDGER strike rows, and the raw libraries — cross-asserted
  (ledger row ⇄ page dist ⇄ library close) before anything renders. The calibration
  sentence renders through `engine/band_record.BandRecord.record_clause()`, the one
  sanctioned phrasing. CALIB is deliberately absent (internal diagnostic).
- Not on the live site. Nothing links here; publishing would be its own explicitly
  requested step under Publish_Protocol.md.

**Regenerate (never hand-edit the HTML):**

    python3 engine/lab/three_lens_trial/build_three_lens_trial.py

The build fails loudly if any cross-assertion breaks — a re-strike, a refit, or a library
update means regenerating, same staleness discipline as the technical read.

Lab code is NOT production. Nothing here is imported by the engine.
