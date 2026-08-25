# [R-SHAPE-01] MID-BAND RESHAPE ADOPTED — AE (UAE) — 2026-08-24

Adopted per instruction (investor session: "Reshape UAE and Egypt to make it less
conservative"), applied via `scripts/adopt_calibration.py --markets AE --yes` through
`auto_refresh.write_production()`. Formally NOT material under R-CAL-01's cone-move
metric — by construction: the reshape moves along the iso-90% ridge, so the published
90% edge is unchanged (+0.05%, rounding of cal to 3dp). This file exists because a
shape adoption per instruction gets a dated record whether or not the gate fires.

## What changed

|              | in production | adopted |
|--------------|--------------|---------|
| nu           | 10.0         | 4.5     |
| width_cal    | 0.916        | 0.965   |
| 90% halfwidth (sigma) | 1.4849 | 1.4857 (+0.05%) |
| 25–75 band   | —            | ~8% narrower |
| pooled cov50 (409 post-break windows) | 53.8% | 50.6% |
| market verdict | PASS       | PASS (unchanged) |

nu is weakly identified; the MLE on the current panel reproduces (10, 0.916) and the
adopted point sits dlogL = 2.21 from it — inside the 95% joint likelihood region. The
two shapes publish the same 90% band; they differ in how much of the middle the 25–75
band claims. Picking the ridge point whose 50% band catches half is calibration.

## The five guards (all passed for AE)

1. **G-flat** — dlogL 2.21 ≤ 3.0; cal 0.965 inside the legality clip [0.85, 1.30].
   (nu=4.0 scored cov50 marginally closer but sat at dlogL 3.26 — excluded by this
   guard; the selection moved to 4.5. The guard is doing its job.)
2. **G-improve** — |cov50−50%| closes 3.8pt → 0.6pt, over the 1pt floor.
3. **G-split** — both calendar halves move toward 50%.
4. **G-lono** — pooled held-out cov50 50.6% under shapes selected without each name.
5. **G-crps** — proper-score parity: CI on blocks {2,3,4} = [-0.0017,+0.0020],
   [-0.0016,+0.0021], [-0.0017,+0.0022] — all straddle zero; not robustly worse.

## Same-day declines (the guards are the release)

- **EG** — DECLINED by G-split: mid-band over-coverage (52.3% pooled) lives entirely in
  the late half (58.1%) while the early half already under-covers (46.7%); any single
  shape helps one half by hurting the other. Declined although EG was NAMED in the
  instruction — the promotion rule binds instructions and pipeline alike. If EG's two
  halves converge in future refits, the pipeline reshapes it automatically.
- **SA** — DECLINED by G-improve: production cov50 50.4%, 0.4pt from target. Nothing to
  fix.

## Where the rule lives

`panel_refresh.reshape_mid_band()` inside `refresh_market()` — every future refit,
unattended or deliberate, reproduces the selection under the same guards and records
the outcome (applied or declined, with the failing guard) in `fitted_configs.json`'s
`mid_band_reshape`. Reverting the commit that carried this file restores
market_profiles.py and fitted_configs.json together (superseded pair recorded).
Governing text: [R-SHAPE-01] in `engine/PROJECT_INSTRUCTIONS_11-07-2026.md` (rev
2026-08-24b) and `engine/Standing_Research_Protocol.md` (rev. 8).

Live-site effect: none until the next strike — published cones re-strike at the
monthly roll-forward under whatever shape production carries then.
