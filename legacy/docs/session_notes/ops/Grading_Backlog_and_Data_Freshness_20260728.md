# Grading backlog — why 6 cohorts read "due" and none can be graded — 28-Jul-2026

Written after a request to "grade COMI as of today," then extended to EMAAR. Neither could be graded, and checking *why* surfaced that five of the six overdue cohorts are blocked on stale libraries rather than on the calendar. The ledger page cannot tell those two cases apart — both render the same `due — grading {date}` chip.

## The six open rows past their stored grade_date

Counted by actual trading rows from `anchor_date` in each library, per the standing grading rule — never off the stored date.

| Name | Mkt | Anchor | Library ends | Sessions elapsed | Needs | Blocked on |
|---|---|---|---|---|---|---|
| COMI | EG | 29-Jun | **28-Jul** | 19 | 20 | **the calendar** — 20th session is 29-Jul, not yet traded |
| EMAAR | AE (DFM) | 29-Jun | 24-Jul | 19 | 20 | **stale library — it matured 27-Jul, one row away** |
| CCAP | EG | 30-Jun | 22-Jul | 15 | 20 | stale library (needs through ~30-Jul) |
| ORAS | EG | 30-Jun | 22-Jul | 15 | 20 | stale library (needs through ~30-Jul) |
| TMPV | IN | 30-Jun | **30-Jun** | 0 | 20 | **zero post-anchor rows** |
| TSLA | US | 30-Jun | **30-Jun** | 0 | 20 | **zero post-anchor rows** |

Only COMI is genuinely waiting on the market. The other five clear the moment fresh OHLC is posted — TSLA and TMPV have a full month missing and have never had a single post-anchor row.

**Standing point: "due" on the ledger page means the projected date has passed, not that the cohort is gradeable.** When triaging, count sessions against the library first; the chip is not evidence. The inverse trap is just as real — COMI's date had passed while the cohort was still immature, because the projection is holiday-blind.

## COMI

19 of 20 EGX sessions since the 29-Jun anchor. Two Sun–Thu weekdays are absent from the library in that window — **2-Jul and 23-Jul** — and both are genuine EGX closures, not gaps: `clean_ohlc` dropped nothing (empty log), and the concurrent market-wide re-strike session independently reported the same two closures from its own pass.

Both horizon conventions agree the cohort matures on **29-Jul**: 29-Jun + 20 sessions = 29-Jul, and 29-Jun + 1 calendar month = 29-Jul. The calendar-vs-session distinction is moot here.

## EMAAR

Anchor 29-Jun at 12.14 — **the library agrees with the published anchor exactly**, unlike COMI. DFM's Mon–Fri calendar in this window is perfectly dense: zero absent weekdays, empty clean log. So 19 sessions to 24-Jul means the 20th session is **Monday 27-Jul, which has already traded**. The cohort matured yesterday; only the library is behind.

One row of DFM data (27-Jul close, high, low) completes the grade. Its cycle-2 cone was already re-struck to the 24-Jul close by the concurrent market-wide pass, so the ticker page is current as of its own last clean close — nothing else to update there.

## Pre-grade: everything except the missing bar

Both cohorts are 19/20. Computed from the known window, so only the final bar can change these.

**EMAAR** — window so far high 12.26 / low 10.86, last known close 11.08.
Locked: touch −5% (11.53) HIT, −10% (10.93) HIT. Still open: +5% needs a 27-Jul high ≥ 12.75, +10% ≥ 13.35, +15% ≥ 13.96, +20% ≥ 14.57 — all far above the 11.08 area, so realistically all miss.
`in_90` holds for any close in [9.98, 14.86]; `in_50` needs [11.22, 13.22]. At the last known close the cohort grades **in_90 true, in_50 false, median_err −9.0%** — a pass on the band with a clear downside miss on the centre.

**COMI** — window so far high 141.70 / low 126.89, last known close 141.50.
Locked: touch +5% (135.71) HIT. Still open: +10% needs a 29-Jul high ≥ 142.18, +15% ≥ 148.64, +20% ≥ 155.10, −5% low ≤ 122.79, −10% ≤ 116.33.
`in_90` holds for [103.44, 159.92]; `in_50` needs [117.89, 140.85]. At the last known close: **in_90 true, in_50 false, median_err +9.8%** — a pass with an upside miss on the centre.

## The COMI anchor-price discrepancy has teeth

COMI cycle-1 carries `anchor_price: 129.25`. The library's 29-Jun close is **126.89** — a 1.86% gap.

**129.25 appears nowhere in the entire 15-year COMI library** — not as a close, open, high or low, on any day. Not an off-by-one date, not an intraday print, not a rounding artifact. Neighbouring closes are 28-Jun 129.82, 29-Jun 126.89, 5-Jul 129.71; none is a plausible transcription source. Most likely a different vendor's 29-Jun close (EGX auction vs last-trade) or a publish-time error in the original study. Unresolved from the repo alone — needs the original study source.

It is not cosmetic, because the touch ladder is struck relative to the anchor:

| Level | vs published 129.25 | vs library 126.89 |
|---|---|---|
| +5% | 135.71 → HIT | 133.23 → HIT |
| **+10%** | 142.18 → **miss** | 139.58 → **HIT** |
| +15% | 148.64 → miss | 145.92 → miss |
| +20% | 155.10 → miss | 152.27 → miss |
| −5% | 122.79 → miss | 120.55 → miss |
| −10% | 116.33 → miss | 114.20 → miss |

Window high through 28-Jul is 141.70, which sits between the two +10% levels — **the discrepancy flips a graded touch outcome.** Resolve before the 29-Jul grade; grade the ladder as published (129.25) per append-only unless the published anchor is affirmatively established as wrong.

Separately, the cone was struck off 129.25 (p50 128.87 ≈ spot × 0.9971). If the true close was 126.89 the whole distribution was born ~1.9% high, shifting recorded `median_err` by roughly 2pp without changing the in-band verdict.

EMAAR is the useful contrast: same vintage, same workflow, anchor ties exactly. So the COMI gap is a one-off, not a systemic anchor-capture bug.

## No grading utility exists in the engine

`engine/strike_cohorts.py` and `engine/apply_rollforward.py` (added 28-Jul) cover striking and applying cohorts, but **nothing in `engine/` grades one**. Every grade so far has been ad-hoc script work re-derived per session, which is how the holiday-blind `grade_date` kept nearly being trusted. A small `engine/grade_cohorts.py` — count sessions from anchor, resolve the true grade session, emit realized/in_90/in_50/quantile/median_err/touch_hit — would make this a one-command step and remove the recurring re-derivation risk. Engine change, so feature branch + PR.

## Unmerged branch backlog

`git ls-remote` shows **23 unmerged `calibration-review-*` branches** dating back to 13-Jul, plus `calibration-review-20260728-103715` opened by today's push (the materiality gate firing correctly on the `raw_ohlc/` change). The gate is working; nothing is being reviewed or merged, so the queue only grows.

`feat/adaptive-width-overlay-eg` is also still unmerged — confirming the TOP OPEN ITEM's own caveat: the EG adaptive-width overlay is **not in production**, and every live EG cone uses the flat market-level `width_cal`.

## Suggested order of work

1. Post one row of DFM data for EMAAR (27-Jul) — it matured yesterday and grades immediately.
2. Resolve the COMI 129.25 vs 126.89 anchor before 29-Jul, since it flips a touch outcome.
3. Grade COMI on 29-Jul once the session lands.
4. Post fresh OHLC for TSLA and TMPV — zero post-anchor data, longest-stale.
5. Post fresh OHLC for CCAP and ORAS (EG, need through ~30-Jul).
6. Build `engine/grade_cohorts.py` so grading stops being re-derived by hand.
7. Triage the 24-branch review queue; decide whether the materiality threshold is too tight if near-identical refits keep opening PRs.
8. Still open from earlier: EMFD/PHDC/HELI touch ladders need a human re-pick; GBCO + STC WACCs predate the v2 cost-of-capital method; metals remains a gold self-fit with silver borrowing it.
