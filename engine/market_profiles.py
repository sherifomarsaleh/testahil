"""market_profiles.py — Testahil universal-engine Market Profile registry (v3).

One engine, markets as data. Each profile supplies:
  carry anchor (local risk-free schedule, annual, decimal),
  signal spec (type/sign/IC — literature prior, re-estimated on pooled panels),
  tail nu (None -> fit on pooled panel, LONO cross-fitted),
  calendar + limit notes, regime-break dates (vol estimated post-break only).

Carry convention: price-forecast drift = ln(1+rf) - ln(1+q), i.e. the
forward-consistent carry for a PRICE (not total-return) series. q = dividend
yield per name (continuous approximation).

Backtest carry schedules are piecewise policy-rate-derived approximations,
GATE-NEUTRAL by construction (engine and benchmark carry the same anchor, so
the CRPS/pinball/interval skill difference is unaffected by the level).
Live-forecast anchors must be freshly sourced per Cost_of_Capital_Reference.md
staleness rules before any publish.

STANDING PER-MARKET FIT RULE (user, 10-Jul-2026 — "every market is different"):
every market Testahil operates in carries its OWN fitted (nu, width_cal) from
its OWN pooled panel — never a borrowed archetype presented as final. A new
market's FIRST action is fitting its own shape/width on its first covered
names' panel; until that fit exists, any borrowed config is FLAGGED and no
name-level FAIL under a borrowed config is treated as real (borrowed configs
fabricate FAILs — QGTS under Egypt's devaluation-fat nu=4 is the canonical
case; PARITY under its own Gaussian/0.92 fit). Single-name fits are
PROVISIONAL until the panel reaches 2+ names; refits follow the panel-growth
cadence (~2+ new names or ~1yr new windows) with the outlier-triggered
immediate-review exception. backtest_v3 resolves nu/width_cal from the
profile automatically when not passed explicitly.

ROBUST-VERDICT RULE (10-Jul-2026): a name-level FAIL requires the bootstrap
CI to sit entirely below zero ROBUSTLY across block sizes {2,3,4} (10k draws,
50k paths). A verdict that flips sign with the block choice is BOUNDARY ->
recorded as PARITY with a flag, reviewed at the name's next live grade.
(ALINMA is the current boundary case.)
"""
from dataclasses import dataclass, field
from typing import Optional, List, Tuple
import pandas as pd

Sched = List[Tuple[str, float]]  # [(effective_date_iso, annual_rate_decimal)]


@dataclass
class MarketProfile:
    code: str
    name: str
    carry_schedule: Sched            # policy-derived, backtest use (gate-neutral)
    rf_live: float                   # current sourced/estimated anchor for live forecasts
    rf_live_source: str
    signal_type: Optional[str]       # 'mom_12_1' | 'rev_1m' | None
    signal_sign: int                 # +1 momentum, -1 contrarian/reversal
    ic: float                        # information-coefficient prior
    signal_active: bool              # False -> carry-only (fallback rule)
    nu: Optional[float] = None       # None -> fit from pooled panel
    width_cal: float = 1.0           # per-market cone multiplier from the panel shape fit
    fit_meta: str = ""               # provenance of the (nu, width_cal) fit
    breaks: List[str] = field(default_factory=list)
    notes: str = ""
    width_overlay_active: bool = False   # EG-only per-name adaptive width overlay (adaptive_width.py)
    ic_by_h: Optional[dict] = None       # per-horizon IC {"1M": x, "3M": y}; None -> flat ic

    def carry_rate(self, date) -> float:
        d = pd.Timestamp(date)
        r = self.carry_schedule[0][1]
        for eff, rate in self.carry_schedule:
            if d >= pd.Timestamp(eff):
                r = rate
        return r


FED_SCHEDULE = [
    ("2009-01-01", 0.0013), ("2015-12-17", 0.0038), ("2016-12-15", 0.0063),
    ("2017-03-16", 0.0088), ("2017-06-15", 0.0113), ("2017-12-14", 0.0138),
    ("2018-03-22", 0.0163), ("2018-06-14", 0.0188), ("2018-09-27", 0.0213),
    ("2018-12-20", 0.0238), ("2019-08-01", 0.0213), ("2019-09-19", 0.0188),
    ("2019-10-31", 0.0163), ("2020-03-16", 0.0013), ("2022-03-17", 0.0038),
    ("2022-05-05", 0.0088), ("2022-06-16", 0.0163), ("2022-07-28", 0.0238),
    ("2022-09-22", 0.0313), ("2022-11-03", 0.0388), ("2022-12-15", 0.0438),
    ("2023-02-02", 0.0463), ("2023-03-23", 0.0488), ("2023-05-04", 0.0513),
    ("2023-07-27", 0.0538), ("2024-09-19", 0.0488), ("2024-11-08", 0.0463),
    ("2024-12-19", 0.0438), ("2025-09-18", 0.0413), ("2025-10-30", 0.0388),
    ("2025-12-11", 0.0363), ("2026-06-18", 0.0363),
]  # Fed funds target midpoints (policy history; Jun-2026 3.50-3.75% per cached note)

EGYPT = MarketProfile(
    code="EG", name="Egypt (EGX)",
    carry_schedule=[
        ("2020-01-01", 0.0825), ("2022-03-21", 0.0925), ("2022-05-19", 0.1125),
        ("2022-10-27", 0.1325), ("2022-12-22", 0.1625), ("2023-03-30", 0.1825),
        ("2023-08-03", 0.1925), ("2024-02-01", 0.2125), ("2024-03-06", 0.2725),
        ("2025-04-17", 0.2500), ("2025-05-22", 0.2400), ("2025-08-28", 0.2200),
        ("2025-10-02", 0.2100), ("2026-02-20", 0.2000), ("2026-04-02", 0.1950),
    ],
    rf_live=0.1950,
    rf_live_source=("CBE main operation rate 19.50% (corridor 19.00/20.00), held since "
                    "2 Apr 2026 [CBE Q1-2026 MPR, cached Cost_of_Capital_Reference.md]. "
                    "Short-tenor anchor for a 60-trading-day horizon; 10Y alt = 22.55% "
                    "(investing.com 3-Jul-2026). FLAG: source a fresh 3M T-bill auction "
                    "yield before first EGX publish under v3 — bills have traded above "
                    "the corridor; 19.50% is the conservative sourced floor."),
    signal_type="mom_combo", signal_sign=+1, ic=0.062, signal_active=True,
    ic_by_h={"1M": 0.062, "3M": 0.068},
    nu=5.0, width_cal=0.958,
    fit_meta=(
        "REFIT 11-Jul-2026 on the FULL 27-name EG panel (351 post-break windows) - "
        "supersedes the 7-name/115-window fit (nu=4, cal=0.965, signal ON). The fit "
        "is CONVERGED: going 25 -> 27 names (adding COMI and ORAS) left nu=4 and "
        "cal=0.909 completely unchanged. Three changes, each tested: (1) "
        "DATA-QUALITY GATE (data_quality.py) cleans every series first, with a "
        "PER-MARKET artifact threshold derived from the exchange's daily price "
        "limit (EGX +/-20% -> every clean name tops out at |log move| <= 0.223, so "
        "anything past 0.29 cannot be trading). Two artifacts found: EFIH carried "
        "flat 0.50 pre-IPO placeholder rows (a fake +333% log jump) and an "
        "unadjusted 3:2 split on 26-May-2025; OCDI/SODIC carried an unadjusted "
        "corporate action on 14-Aug-2025 showing as a fake -73% crash. OCDI was IN "
        "the production 7-name fit - but repairing it does NOT move nu (still 4; "
        "cal 0.979 -> 0.958), so Egypt's fat tail is GENUINE devaluation-jump risk, "
        "not a data bug. (2) BREAK FILTERING ADOPTED: calibrating on "
        "post-2023-01-11 origins only beats calibrating on all windows "
        "out-of-sample (LONO +0.0211 vs +0.0198, both scored on the same post-break "
        "windows) AND narrows the cone from cal=0.972 to 0.909. (3) SIGNAL ABLATED "
        "OFF - this was the LAST active signal in the system. On the panel the "
        "empirical IC of rev_1m is +0.018: the house prior's contrarian sign=-1 is "
        "REFUTED and the magnitude is ~0. Ablation: carry-only +0.0252 beats "
        "signal-ON +0.0211; the signal helps in only 13/25 names; paired bootstrap "
        "P(signal helps)=0.31. Fallback rule applies. The rev_1m/IC-0.08 prior is "
        "retained for re-estimation, but signal_active=False. EVERY market in the "
        "system is now carry-only. RESULT: panel PASS +0.0270 CI[+0.018,+0.038] on "
        "the scale-normalized gate; top-name weight 8.9% (vs 42% under the old "
        "price-weighted gate). ZERO name-level FAILs. PASS: CCAP +0.090, EMFD "
        "+0.078, HELI +0.070, PHDC +0.066, LCSW +0.051, OCDI +0.048, PRDC +0.037. "
        "BOUNDARY(PARITY-flagged): FWRY, ETEL, EFIH, GBCO, ABUK. 15 PARITY (incl. "
        "the two names added last: COMI +0.023, ORAS +0.021). NB PHDC moved to PASS "
        "on refreshed OHLC (1328 rows to 28-Jun-2026, vs a stale 1223-row project "
        "copy) - relevant, since PHDC carries the live ledger cohorts. The old "
        "7-name panel was sector-concentrated (5 of 7 were RE developers); the "
        "27-name panel is cross-sector and its lower headline skill is the more "
        "honest number. UPDATE 13-Jul-2026: CLHO added (28 -> 29 names, 351 -> 377 windows), reviewed "
        "in PR #4 and merged by Sherif. nu=4.0 and cal=0.909 UNCHANGED. CLHO itself: skill -0.0199, "
        "PARITY -- unremarkable, inside the existing PARITY range (ISPH -0.044, OIH -0.011). The one "
        "side-effect: CCAP's OWN verdict moved PASS -> BOUNDARY(PARITY-flagged) (skill +0.0906, still "
        "positive, CI[0.006,0.207] -- straddles the boundary, not a sign flip), which is why the "
        "materiality gate correctly stopped for review rather than auto-committing. Market panel: "
        "PASS +0.0259 CI[0.017,0.036], materially the same as pre-CLHO. "
        "UPDATE 22-Jul-2026: DSCW added (29 -> 30 names, 462 -> 478 windows under the "
        "adopted 2022-03-21 break cut below). NOT material by itself - nu and cal "
        "UNCHANGED at 4.0/0.972. DSCW itself: skill +0.0117, BOUNDARY(PARITY-flagged) "
        "CI[-0.007,+0.027] - unremarkable, inside the existing PARITY/BOUNDARY range. "
        "26-Jul-2026 -- 15-YEAR CALIBRATION SAMPLE: TESTED, NOT ADOPTED (decision, "
        "Sherif). A 15-year EG library (32 series, 97,756 cleaned sessions, median 15.6 "
        "yrs) was ingested and the calibration-sample comparison re-run on it. NOTE the "
        "first run of that comparison was INVALID: data_quality.clean_ohlc corrupted 9 "
        "of 30 names via non-positive prices (see the step-1b fix in data_quality.py). "
        "On PATCHED data, identical scoring windows (492, 30 names, post-2022-03-21), "
        "LONO-cross-fitted: LONG(2011+) nu=6.0/cal=0.909 skill +0.0157; MID(2016+) "
        "nu=6.0/cal=0.923 +0.0155; CURRENT(2022-03-21+) nu=5.0/cal=0.930 +0.0153. "
        "LONG beats CURRENT ROBUSTLY across bootstrap blocks {2,3,4} AND survives a "
        "drop-one-name jackknife (0 flips in 30; top contributor ISPH 18.1%, no name "
        ">25%) -- i.e. it passes both robustness checks, separately. NOT ADOPTED anyway: "
        "the published 90% cone (width_cal x q95(t(nu))) moves only -0.65%, an order of "
        "magnitude inside the 5% materiality gate. A result that is real but immaterial "
        "does not justify moving a live cone. Do not re-litigate on skill alone; skill "
        "did not decide the break cut originally (devaluation-window coverage did) and "
        "that column has NOT been re-run on patched data. nu and cal UNCHANGED at "
        "4.0/0.972; the 2022-03-21 cut STANDS. "
        "26-Jul-2026 -- ROUTINE REFIT APPLIED (PR #27, decision Sherif): this is a "
        "DIFFERENT change from the LONG-sample question above -- same adopted "
        "2022-03-21+ CURRENT window, just re-fit on the patched, library-extended "
        "panel (30 names, 492 windows, up from 478). auto_refresh.py flagged it "
        "material (market verdict PARITY -> PASS) and stopped for review per the "
        "materiality gate; PR #24 (stale, pre-DQ-patch) was closed unmerged and "
        "superseded by PR #27, run after the fix/dq-nonpositive-prices patch "
        "landed on main. nu 4.0 -> 5.0, width_cal 0.972 -> 0.93. Market panel: "
        "PASS skill +0.0158 CI[0.009,0.023] (does not cross zero). Verdict shifts: "
        "ABUK/ADIB BOUNDARY->PARITY, CCAP/EFIH/ORWE/PHDC/TMGH ->PASS, "
        "GBCO/ORHD BOUNDARY-flagged, LCSW/OCDI/ORAS PASS->PARITY, ISPH "
        "BOUNDARY->FAIL. ISPH is the one name-level FAIL: skill -0.0332, checked "
        "robust across bootstrap blocks {2,3,4} (reported as a plain FAIL, not "
        "BOUNDARY, i.e. no block-dependent sign flip) -- a genuine finding, not a "
        "data artifact of the non-positive-price bug (same FAIL was already present "
        "on the stale pre-patch run). XAU was unaffected by the DQ bug and its "
        "PENDING_REVIEW numbers were identical pre- and post-patch, confirming the "
        "fix was correctly scoped to EG only. "
        "UPDATE 27-Jul-2026 (calendar-horizon 3m adoption, PR #32 site-wide switch): "
        "re-fit on the calendar 3-month window. nu 5 -> 6, cal 0.93 -> 0.951 -- "
        "-1.39% band move (narrows), non-material on the market-level band alone. "
        "Market panel stays PASS +0.0158 CI[0.009,0.022] (was CI[0.009,0.023]). BUT "
        "15 of 30 names change verdict category, FIVE of them WORSENING -- CCAP, "
        "EFIH, EMFD, PHDC, PRDC all lose PASS -> PARITY. Three improve to PASS from "
        "PARITY (ABUK, EGAL, ORAS); ISPH partially un-fails (FAIL -> "
        "BOUNDARY(PARITY-flagged)); the rest shuffle between PARITY/BOUNDARY. "
        "Adopted on EXPLICIT user override of the standing 'no worsening' rule "
        "(instruction: 'switch all to one month and 3 months') -- the five PASS "
        "losses above are real and were surfaced before this shipped, not missed. "
        "Source: engine/PENDING_REVIEW/reverify_post_merge.json (EG.3m). "
        "SIGNAL ADOPTED 23-Aug-2026 (per instruction — committed drift): "
        "mom_12_1/sign +1/ic 0.061 ACTIVE, replacing the refuted rev_1m prior. "
        "Evidence: engine/direction_tournament/RESULTS_23-08-2026 — pooled "
        "direction IC +0.061 (1M, n=4763) and +0.068 (3M, n=1134), robust "
        "blocks {2,3,4}, LONO sign-stable, split-half consistent; ic set to "
        "the SMALLER of the two horizons' readings (conservative). Cross-name "
        "ranking power in EG is weak (XS IC ~+0.02 at 1M) — this is a "
        "which-way-is-this-one signal here, not a stock picker, and the "
        "document-techniques backtest (engine/doc_techniques_backtest/) found "
        "no alternative that beat carry. Every strike now records "
        "signal_z/signal_alpha (strike_cohorts already logs both); a sustained "
        "failed-direction grade record triggers the standing out-of-cycle "
        "review, and the next panel refit under signal-ON routes through the "
        "materiality gate as usual. UPGRADED same day (per instruction — "
        "'the tilt is still very conservative'): signal_type -> mom_combo "
        "(equal-weight 12-1 + 6-1, measured COMBO_MOMENTUM_23-08-2026: 1M "
        "+0.062 / 3M +0.068, both PASS/LONO-stable/split-half-stable), "
        "per-horizon ic_by_h replaces the min-horizon shrink, and the socket "
        "knobs softened dead 0.5->0.25 / clip 2.0->2.5 / cap 0.5->0.75 sigma "
        "— the ICs were measured on raw z, so the knobs now track the "
        "evidence, not a conservatism choice."),
    # EGYPT BREAKS RE-DERIVED, 13-Jul-2026 (Sherif: "devaluation is a way of life in
    # Egypt, even sharp ones") -- and he is right, which changes the answer.
    #
    # THE OLD LIST WAS WRONG ON ITS FACE: it ended at 2023-01-11 and MISSED the largest
    # devaluation in the series, 6-Mar-2024 (EGP ~30.9 -> ~50.2). apply_breaks cuts at
    # MAX(breaks), so the live filter only worked BY ACCIDENT -- it happened to leave the
    # Mar-2024 float INSIDE the sample. Had the list been "complete", the filter would have
    # excised the very jump the fat tail (nu=4) exists to price.
    #
    # THE DEEPER POINT: a devaluation is not a one-off regime change here, it is the
    # process -- Mar-2022, Oct-2022, Jan-2023, Mar-2024. Filtering them out filters out
    # the risk. Cutting at the TRUE last break (2024-03-06) leaves a devaluation-free
    # sample, and the fit obediently thins the tail (nu 4 -> 5) and narrows the cone
    # (cal 0.909 -> 0.850). It then WINS the skill test -- because it is scored on a calm
    # period. That is the trap, and the original adoption test walked into it: it compared
    # configs "both scored on the same post-break windows", which is circular by construction.
    #
    # MEASURED on the committed 29-name panel. The column that matters is coverage during
    # the windows that actually CONTAIN the Mar-2024 float:
    #   cut          nu    cal   windows  panel skill  FAILs   dev-window 90% coverage
    #   none/2016   4.0  0.958      508     +0.0169      1            86.2%
    #   2022-03-21  4.0  0.972      462     +0.0204      0            86.2%   <-- ADOPTED
    #   2023-01-11  4.0  0.909      377     +0.0259      0            82.8%   (retired)
    #   2024-03-06  5.0  0.850      237     +0.0376      1            82.8%   (the trap)
    #
    # 2022-03-21 is where Egypt's SERIAL-devaluation regime begins: the pound sat flat at
    # ~15.7 for years, then stepped Mar-22 -> Oct-22 -> Jan-23 -> Mar-24. Cutting there keeps
    # THREE devaluations in the calibration sample -- so the cone is the widest of any config
    # (0.972), devaluation coverage is the best available (86.2%), and there are ZERO
    # name-level FAILs. Going further back to 2016 drags in the stable, managed post-float
    # years -- a genuinely different regime -- and it HURTS (skill falls, CLHO turns FAIL)
    # without improving jump coverage at all.
    #
    # Cost, stated honestly: headline panel skill falls +0.0259 -> +0.0204. We accept that.
    # A cone that is too narrow during a devaluation is the failure mode that loses money,
    # and the lower headline number is the more honest one.
    breaks=["2016-11-03", "2022-03-21"],
    notes=("Literature: no EGX momentum; overreaction/short-term reversal supported "
           "(EGX event studies; Kuwait 1m reversal ~3.1%/mo t≈4.4 as GCC analogue). "
           "Signal sign/IC re-estimated on the 6-name pooled panel each cycle."),
    width_overlay_active=True,  # EG-only, MIN_WINDOWS=28 history-gated (adaptive_width.py)
)

SAUDI = MarketProfile(
    code="SA", name="Saudi Arabia (Tadawul)",
    carry_schedule=[
        ("2020-01-01", 0.0100), ("2022-03-17", 0.0125), ("2022-05-05", 0.0175),
        ("2022-06-16", 0.0225), ("2022-07-28", 0.0300), ("2022-09-22", 0.0375),
        ("2022-11-03", 0.0450), ("2022-12-15", 0.0500), ("2023-02-02", 0.0525),
        ("2023-03-23", 0.0550), ("2023-05-04", 0.0575), ("2023-07-27", 0.0600),
        ("2024-09-19", 0.0550), ("2024-11-08", 0.0525), ("2024-12-19", 0.0500),
        ("2025-09-18", 0.0475), ("2025-10-30", 0.0450), ("2025-12-11", 0.0425),
        ("2026-06-18", 0.0400),
    ],
    rf_live=0.0425,
    rf_live_source=("SAMA repo-anchored ESTIMATE ~4.25% (Fed 3.50-3.75% post Jun-2026 "
                    "FOMC + historical SAMA +50bp spread). FLAG per house no-UST-shortcut "
                    "rule: a direct SAR govt sukuk quote was inaccessible via available "
                    "tools this session (investing.com/WGB tables JS-walled) — replace "
                    "with FTSE SAGBI or iBoxx Tadawul SAR sukuk yield before publish. "
                    "Sensitivity: ±50bp = ±0.12% on the 60d median — immaterial vs band."),
    signal_type="mom_12_1", signal_sign=+1, ic=0.093, signal_active=True,
    ic_by_h={"1M": 0.093, "3M": 0.093},
    nu=12.0, width_cal=1.056,
    fit_meta=(
        "REFIT 11-Jul-2026 on the 11-name SA panel "
        "(ACWA/ALINMA/ARAMCO/ELM/EXTRA/MAADEN/RAJHI/RIBL/SABIC/SNB/STC, 190 windows) "
        "— supersedes the 2-name fit (nu=5, cal=1.28). The old cal=1.28 was CAP-BOUND "
        "thin-panel conservatism, not real Tadawul vol: on an 11-name panel the MLE "
        "lands at scale=1.09 -> cal=1.063, a ~17% narrower cone. LONO out-of-sample "
        "check of the SELECTION PROCEDURE: MLE +0.0008 beats both a direct CRPS-skill "
        "grid search (-0.0011, overfits) and the old incumbent (-0.0000) — "
        "MLE-on-residuals retained as the house method. Panel PARITY +0.0023 "
        "CI[-0.004,+0.008] on the corrected scale-normalized gate. Per-name (LONO, "
        "robust blocks): RAJHI PASS +0.0151 (clean: PIT 0.495, width ratio 0.991); "
        "ELM robust FAIL -0.0142 across blocks {2,3,4}; all others PARITY. Signal "
        "still OFF — 11 names clears the ~5-name threshold, so the mom_12_1 IC is now "
        "estimable and should be ablated at the next refit. "
        "UPDATE 27-Jul-2026: re-verified after main's long-history ingest re-pulled "
        "full price series for all 11 SA names. No break filter excludes it here "
        "(breaks=2015-06-15 only), so the fuller history fully enters the calibration "
        "sample; windows 190 -> 410. nu 6 -> 8, cal 1.063 -> 1.021 -- -8.08% band move "
        "(width_cal x q95(t(nu))), MATERIAL under the standing 5% gate, routed through "
        "a PR rather than auto-committed. Panel PARITY +0.0004 CI[-0.005,+0.006] (was "
        "+0.0023). Per-name verdict changes (4 of 11): EXTRA PARITY -> robust FAIL "
        "-0.0308 CI[-0.047,-0.016] -- confirmed on 2x+ the data, this is not a fresh "
        "signal, the prior short-library fit already read PARITY -0.0140 in the same "
        "direction; ALINMA PARITY -> BOUNDARY(PARITY-flagged) +0.0143; MAADEN PARITY "
        "-> PASS +0.0223; RAJHI PASS -> PARITY +0.0048 (loses PASS, not a FAIL). ELM "
        "stays a robust FAIL -0.0131 (unchanged, pre-existing). Signal still OFF. "
        "Source: engine/reverify_post_merge.py, "
        "engine/PENDING_REVIEW/reverify_post_merge.json. "
        "UPDATE 27-Jul-2026 (calendar-horizon 3m adoption, PR #32 site-wide switch): "
        "re-fit on the calendar 3-month window. nu 8 -> 12, cal 1.021 -> 1.07 -- "
        "+0.45% band move vs the just-adopted 60d incumbent above, non-material on "
        "the band alone. Market panel PARITY -0.002 CI[-0.009,0.004] (was +0.0004). "
        "EXTRA stays a robust FAIL both ways (-0.0308 -> -0.0372) -- confirmed again, "
        "not sensitive to window convention. MAADEN WORSENS: PASS -> PARITY "
        "(+0.0223 -> +0.0073, loses PASS). ELM IMPROVES: FAIL -> PARITY (-0.0131 -> "
        "+0.0056, un-fails). ALINMA BOUNDARY(PARITY-flagged) -> PARITY (resolves). "
        "Adopted on EXPLICIT user override of the standing 'no worsening' rule "
        "(instruction: 'switch all to one month and 3 months') -- MAADEN's PASS "
        "loss is real and was surfaced before this shipped, not missed. Source: "
        "engine/PENDING_REVIEW/reverify_post_merge.json (SA.3m). "
        "SIGNAL ADOPTED 23-Aug-2026 (per instruction — committed drift): "
        "mom_12_1 ic 0.093 ACTIVE, sign corrected -1 -> +1 (the old "
        "contrarian prior is refuted by measurement). Evidence: "
        "engine/direction_tournament/RESULTS_23-08-2026 — 1M pooled IC "
        "+0.093 (n=1437) robust/LONO-stable/split-half-consistent with "
        "cross-name IC +0.089; the 3M pooled read is PARITY on n=318 "
        "(underpowered) while the cross-name 3M read is strongly positive — "
        "the 1M-measured ic is carried to 3M through the socket's sigma "
        "scaling and DISCLOSED as unproven at 3M. Grading discipline as per "
        "the EG adoption note. UPGRADE CHECK same day: the mom_combo variant "
        "was measured and NOT adopted for SA — combo 1M +0.082 underperforms "
        "mom_12_1's +0.093 and combo 3M is PARITY, so SA keeps mom_12_1 with "
        "ic_by_h flat at the 1M reading (3M still carried, still disclosed); "
        "socket knobs softened per the EG note."),
    breaks=["2015-06-15"],
    notes=("Signal OFF (fallback rule): 1-name panel cannot establish IC; literature "
           "sign-unstable (contrarian post-2015 opening). Runs carry-only until the "
           "Saudi panel reaches ~5 covered names."),
)

# ---- Approved-design stubs (priors from the two profile tables signed off 09/10-Jul) ----
USA = MarketProfile("US", "United States", FED_SCHEDULE, 0.0363,
    "UST 10Y 4.58% (tradingeconomics 8-Jul-2026, cached CoC-Reference); use 3M bill 3.71% "
    "(investing.com 10-Jul-2026) for the 60d carry at publish.",
    "mom_12_1", +1, 0.05, False, nu=12.0, width_cal=1.084,
    fit_meta=("Fitted 10-Jul-2026 on the 3-name US panel (AAPL/NVDA/TSLA, 54 windows, "
              "2021-2026): nu=12, cal=1.014 - thin tails like metals, far from EGX. "
              "SIGNAL ABLATION on this panel: carry-only (+0.012 CI[-0.006,+0.017]) "
              "marginally beats the mom_12_1 prior ON (+0.010 CI[-0.013,+0.019]) -> "
              "fallback rule applies, signal_active=False; the JT prior is retained "
              "for re-estimation at ~5 names. Panel verdict PARITY. Per-name "
              "(carry-only LONO, robust blocks): AAPL PARITY -0.002 (was BOUNDARY "
              "with the signal ON - the momentum prior was hurting it), NVDA PARITY "
              "+0.002, TSLA PARITY +0.015. "
              "UPDATE 27-Jul-2026 (calendar-horizon 3m adoption, PR #32 site-wide "
              "switch): re-fit fresh on the calendar 3-month window, freshly recomputed "
              "via refresh_market (not read from the older calendar_horizon_refit_3m.json "
              "snapshot, cross-checked and it agreed). nu Gaussian, cal 1.014 -> 1.077 -- "
              "-1.98% band move (width_cal x q95(t(nu))) vs the live 60d incumbent -- "
              "counterintuitive sign: cal widens but the Gaussian tail is thinner than "
              "t(12), so the cone narrows net. NON-MATERIAL. All three names unchanged: "
              "AAPL/NVDA/TSLA stay PARITY. Market panel PARITY +0.0085 CI[-0.003,+0.018] "
              "(was -0.0056). Windows 51 (vs 54 at 60d). Source: "
              "engine/PENDING_REVIEW/reverify_usa_qatar_india.json (US.3m). Auto-adopted "
              "per the standing non-material gate."),
    notes="Mature-market momentum prior (JT 12-1) - ablated OFF on the first panel; "
          "re-estimate as the panel grows.")
UK = MarketProfile("GB", "United Kingdom", [("2020-01-01", 0.0400)], 0.0400,
    "PLACEHOLDER — source gilt/3M at first UK study.", "mom_12_1", +1, 0.05, False,
    notes="Strong UK momentum literature. signal_active corrected to False "
          "23-Aug-2026: a placeholder stub may not run a live signal — only "
          "AE/EG/SA are adopted (committed drift), each on measured evidence.")
BRAZIL = MarketProfile("BR", "Brazil", [("2020-01-01", 0.1300)], 0.1300,
    "PLACEHOLDER — source Selic/DI at first BR study.", "mom_12_1", +1, 0.07, False,
    notes="EM momentum prior (Rouwenhorst). signal_active corrected to False "
          "23-Aug-2026: a placeholder stub may not run a live signal — only "
          "AE/EG/SA are adopted (committed drift), each on measured evidence.")
KOREA = MarketProfile("KR", "South Korea", [("2020-01-01", 0.0300)], 0.0300,
    "PLACEHOLDER — source KTB at first KR study.", None, +1, 0.03, False,
    nu=8.0, width_cal=1.07,
    fit_meta=(
        "REFIT 27-Jul-2026 on the 3-name KR panel after a 15-YEAR SAMSUNG INGEST - "
        "supersedes nu=Gaussian/cal=1.154. Samsung's library goes 1,515 -> 3,709 "
        "sessions (2011-08-23 onward), which triples the panel's dominant name and "
        "is the first KR fit with a pre-2021 sample. Tail goes Gaussian -> 12 and "
        "the cone NARROWS 1.154 -> 1.105: the published 90% cone (width_cal x "
        "q95(t(nu))) moves -5.3%, tripping the >5% materiality gate, so this went "
        "to PR rather than auto-commit. LGES moves FAIL -> PARITY; all three names "
        "now PARITY; market panel stays PARITY (+0.0004). LONO per-name fits: "
        "KAKAO nu=10/1.098, LGES nu=15/1.147, SAMSUNG nu=Gaussian/1.021. "
        "DATA REPAIR THAT MADE IT POSSIBLE (27-Jul-2026): the Samsung export carried "
        "41 PHANTOM PRE-SPLIT PRINTS - Change % literally '4,900.00%' (= 50x-1, the "
        "May-2018 50:1 split), O=H=L=C, volume '0.00K'..'0.09K' or NaN - every one "
        "on a NON-TRADING day (33 Sundays + 8 confirmed KRX closures incl. Memorial "
        "Day, Seollal, Buddha's Birthday, the 2017 presidential election and Hangul "
        "Day). Same class as the 10-Jul KAKAO 5:1 finding, at 41 rows and 50:1. They "
        "survive step 1 of the gate ONLY because their volume string is non-NaN. "
        "Dropped, not rescaled. What remains is a single genuine unadjusted segment "
        "before 2016-04-14, back-adjusted x0.0204 by the gate. Post-break history "
        "reproduces the previous library EXACTLY (max abs diff 0.000000 over 1,365 "
        "shared sessions) - i.e. this is purely ADDITIVE history, not a restatement. "
        "NOTE the panel is now badly unbalanced: Samsung carries 15 years while "
        "KAKAO and LGES still carry ~5. Backfilling those two is the next upgrade. "
        "UPDATE 27-Jul-2026 (calendar-horizon 3m adoption, PR #32 site-wide switch): "
        "re-fit on the calendar 3-month window. nu 12 -> 10, cal 1.105 -> 1.063 -- "
        "-2.17% band move (width_cal x q95(t(nu))) vs the just-adopted 60d incumbent "
        "above, NON-MATERIAL under the 5% gate. All three names unchanged: "
        "KAKAO/LGES/SAMSUNG stay PARITY. Market panel PARITY +0.0008 CI[-0.003,+0.009] "
        "(was +0.0004). Windows 85 (vs 88 at 60d). Source: "
        "engine/PENDING_REVIEW/reverify_post_merge.json (KR.3m). Auto-adopted per the "
        "standing non-material gate — no per-name verdict changed, no market-verdict "
        "changed, band move under 5%. "
        "SUPERSEDED TEXT (11-Jul-2026) FOLLOWS - "
        "supersedes nu=6/cal=1.070. THE INVESTING.COM KOREAN EXPORT CONTAINS "
        "PHANTOM NON-TRADING ROWS: ~160 rows per name carrying NaN volume and "
        "O=H=L=C, of which 144 of SAMSUNG's 170 fall on a SUNDAY (KOSPI is closed). "
        "Raw density is 276.8 rows/yr; after removing them it is 245.8/yr - exactly "
        "the KOSPI calendar. These phantom rows inject fake zero-return, "
        "zero-intraday-range days straight into the Yang-Zhang variance proxy, "
        "DEPRESSING the volatility estimate. The 10-Jul repair caught only the 13 "
        "pre/post-split price-scale rows (fixed by dividing by 5, which SYNTHESIZES "
        "a price on a day the market never opened); it never saw the ~160 phantom "
        "rows. They are now DROPPED, not rescaled. EFFECT: the tail goes 6 -> "
        "Gaussian and the cone WIDENS 1.070 -> 1.154 - the old fit was "
        "simultaneously too narrow AND falsely fat-tailed, an artifact of the "
        "depressed vol. Skill nevertheless IMPROVES: panel PARITY +0.0144 "
        "CI[-0.005,+0.017] (was +0.006). Per-name (LONO, robust blocks): SAMSUNG "
        "PARITY +0.0094, KAKAO PARITY +0.0022, LGES robust FAIL -0.0268 across "
        "blocks {2,3,4} - and its signature is OVER-COVERAGE: cov80=1.00 and "
        "cov90=1.00 (every outcome inside the 80% band), cone 1.112x the benchmark, "
        "PIT 0.471 (well centred). LGES is not mis-centred, it is simply too wide: "
        "it IPO'd Jan-2022, has the shortest history and only 13 windows, and the "
        "market-level width_cal over-widens a name whose own vol is below the panel "
        "average. This is the clearest case in the whole system for a NAME-LEVEL "
        "width_cal shrunk toward the market fit - proposed, NOT implemented, "
        "pending an out-of-sample test."),
    notes="Asia momentum-failure pattern: carry-only.")
UAE = MarketProfile("AE", "UAE (ADX/DFM)", FED_SCHEDULE, 0.0365,
    "Carry = USD/Fed policy path (AED hard-pegged); rf_live 3.65% = CBUAE Base Rate held "
    "17-Jun-2026. NB the peg 'never-UST' rule governs the VALUATION rf (AED govt bond) -- "
    "the MC carry correctly tracks the Fed for a pegged currency.", "mom_combo", +1, 0.108, True,
    ic_by_h={"1M": 0.108, "3M": 0.185},
    nu=4.5, width_cal=0.965,
    fit_meta=(
        "UPDATE 24-Aug-2026 [R-SHAPE-01]: mid-band reshape ADOPTED per instruction "
        "(investor session) via scripts/adopt_calibration.py -- (nu 10, cal 0.916) -> "
        "(nu 4.5, cal 0.965) along the iso-90% ridge: 90% halfwidth 1.4849 -> 1.4857 "
        "sigma (+0.05%, rounding only), 25-75 band ~8% narrower, pooled cov50 53.8% -> "
        "50.6% on 409 post-break windows (LONO held-out 50.6%), dlogL 2.21 inside the "
        "95% likelihood region, CRPS parity CIs straddle 0 on blocks {2,3,4}. All five "
        "R-SHAPE-01 guards passed; EG and SA were checked the same day and DECLINED "
        "(G-split / G-improve) -- the guards are the release. Reshape provenance lives "
        "in fitted_configs.json mid_band_reshape; superseded pair recorded there too. "
        "UPDATE 09-Aug-2026: AIRARABIA added (18 -> 19 names, 261 -> 279 pooled "
        "windows; DFM low-cost carrier, new coverage for the Air Arabia study). "
        "Pooled MLE moves nu 10 -> 8 with cal unchanged at 0.979 -- the published "
        "90% cone halfwidth moves 0.66%, well inside the 5% materiality band (nu "
        "remains weakly identified; the (nu,cal) pair is the fitted object). "
        "Market panel PARITY +0.0068 CI[-0.000,+0.014], unchanged. AIRARABIA "
        "arrives PARITY +0.0013 CI_b2[-0.026,+0.013] under its LONO fit (nu=10/"
        "0.979) -- not a FAIL. MATERIALITY ITEM reviewed via this study's PR: "
        "ENBD BOUNDARY(PARITY-flagged) -> PARITY (-0.0116, CI_b2[-0.053,+0.009]; "
        "an improvement -- the flag clears, no verdict worsens, no new FAIL, no "
        "lost PASS; ADCB/ADIB/ALDAR/DIB/EMAAR keep PASS). LULU still "
        "PROVISIONAL(insufficient-windows). "
        "REFIT 11-Jul-2026 on the 14-name AE panel (237 post-break windows), RE-RUN "
        "through the data-quality gate - supersedes nu=4/cal=1.070. Adds "
        "ADIB/DIB/TWOPOINTZERO/EAND to the prior 10. Tail moves 4 -> 10: the old "
        "fat tail was carried by IHC/EMAAR idiosyncratic swings on a smaller panel; "
        "four more well-behaved names dilute it. HONESTY NOTE: nu is only WEAKLY "
        "IDENTIFIED - every nu from 5 to Gaussian sits inside the 95% likelihood "
        "interval (nu=4 is only dlogL=2.23 away), and nu trades off against cal. "
        "The (nu,cal) PAIR is fitted; neither coordinate is individually precise. "
        "LONO OOS: this MLE config scores +0.0032 vs the incumbent's -0.0017. "
        "Data-quality gate dropped 3-5 stale no-trade rows each from EAND/ADCB/ADIB "
        "- immaterial (cal 1.056 -> 1.049, nu unchanged). BREAK FILTERING APPLIED: "
        "EAND's OHLC starts 2016, so 21 of its 39 windows predate the Jan-2022 "
        "workweek switch and are excluded from the calibration sample; unfiltered "
        "they pulled the fit to nu=6/cal=1.084. Panel PARITY +0.0049 "
        "CI[-0.004,+0.015]. Per-name: ALPHADHABI robust FAIL -0.0122 (cone 1.136x "
        "benchmark, cov90=0.94 vs a 0.90 target - over-wide, same signature as "
        "KR/LGES); all 13 others PARITY. Signal OFF; 14 names now clears the "
        "threshold for a rev_1m ablation. "
        "UPDATE 22-Jul-2026: BURJEEL/DEWA/LULU/SALIK added (14 -> 18 names, 237 -> 274 "
        "windows); ADIBUAE removed as a byte-identical duplicate of ADIB that was "
        "double-weighting ADIB's windows in every pooled and LONO fit (cmp-verified, "
        "not a data change). nu unchanged at 10; cal 1.049 -> 1.028 (narrower - the "
        "four new names are well-behaved). Panel PARITY +0.0033 CI[-0.005,+0.013]. "
        "MATERIALITY: two verdicts changed, both reviewed before merge (PR #13). "
        "ALPHADHABI: robust FAIL -0.0122 -> PARITY -0.0094 CI[-0.022,0.0] - removing "
        "the double-counted ADIB windows and adding four well-behaved names both moved "
        "the panel-average vol enough to bring ALPHADHABI's own cone back to a "
        "defensible width; no longer a robust FAIL under blocks {2,3,4}. ADCB: PARITY "
        "-> BOUNDARY(PARITY-flagged), skill +0.0259 CI[0.001,0.067] - straddles the "
        "boundary, not a sign flip; flagged for the next grade (ADCB is the bank "
        "reference-study exemplar, worth watching). New names: BURJEEL PARITY +0.0099, "
        "SALIK PARITY -0.0139, DEWA BOUNDARY(PARITY-flagged) -0.0056. LULU: only 2 "
        "non-overlapping windows since its Nov-2024 IPO - too thin for the robust "
        "{2,3,4}-block standard (block=3 has no valid start); verdict is "
        "PROVISIONAL(insufficient-windows) under the now-fixed verdict_ci (previously "
        "this crashed the entire daily AE run; see panel_refresh.py NOBLOCK fix, same "
        "PR). Re-resolves automatically once LULU accrues >=4 windows. "
        "UPDATE 27-Jul-2026: re-verified after main's long-history ingest re-pulled "
        "full price series for all 18 AE names. Break filter (post-2022-01-01) still "
        "applies, so the added deeper history mostly falls outside the calibration "
        "sample; windows 274 -> 275, just new trailing sessions. nu 10 -> 8, cal "
        "1.028 -> 0.895 -- -10.68% band move (width_cal x q95(t(nu))), MATERIAL under "
        "the standing 5% gate, routed through a PR rather than auto-committed. Panel "
        "PARITY +0.008 CI[-0.0,+0.015] (was +0.0033). Per-name verdict changes (4 of "
        "18): ADCB BOUNDARY(PARITY-flagged) -> PARITY +0.0097; ADIB PARITY -> PASS "
        "+0.0395; DEWA BOUNDARY(PARITY-flagged) -> PARITY +0.0012; ADNOCGAS PARITY -> "
        "BOUNDARY(PARITY-flagged) +0.044 CI[0.002,0.114]; EAND PARITY -> "
        "BOUNDARY(PARITY-flagged) +0.0325. No new FAIL, no lost PASS. LULU remains "
        "PROVISIONAL(insufficient-windows). Signal still OFF. Source: "
        "engine/reverify_post_merge.py, engine/PENDING_REVIEW/reverify_post_merge.json. "
        "UPDATE 27-Jul-2026 (calendar-horizon 3m adoption, PR #32 site-wide switch): "
        "re-fit on the calendar 3-month window. nu 8 -> 10, cal 0.895 -> 0.979 -- "
        "+6.62% band move vs the just-adopted 60d incumbent above, MATERIAL (widens, "
        "over the 5% gate). Market panel PARITY +0.0068 CI[-0.001,0.014] (was "
        "+0.008). Per-name: ADCB, ALDAR, DIB, EMAAR all move PARITY -> PASS "
        "(improvements); ADNOCGAS BOUNDARY(PARITY-flagged) -> PARITY (improvement); "
        "AGTHIA PARITY -> BOUNDARY(PARITY-flagged) and ENBD PARITY -> "
        "BOUNDARY(PARITY-flagged) (both WORSEN, flagged not failed). No new FAIL, "
        "no lost PASS. LULU still PROVISIONAL. Adopted on EXPLICIT user override of "
        "the standing 'no worsening' rule (instruction: 'switch all to one month and "
        "3 months') -- the market-level widening and the AGTHIA/ENBD flags above are "
        "real and were surfaced before this shipped. Source: "
        "engine/PENDING_REVIEW/reverify_post_merge.json (AE.3m). "
        "SIGNAL ADOPTED 23-Aug-2026 (per instruction — committed drift): "
        "mom_12_1/sign +1/ic 0.109 ACTIVE, replacing the never-confirmed "
        "rev_1m prior. Evidence: engine/direction_tournament/"
        "RESULTS_23-08-2026 — the strongest direction result in the system: "
        "pooled IC +0.109 (1M, n=2283) and +0.142 (3M, n=492), hit rates "
        "55%, top-vs-bottom-third spread ~+3%/quarter, robust blocks {2,3,4}, "
        "LONO sign-stable, split-half consistent, cross-sectional framing "
        "agrees. UPGRADED same day (per instruction): signal_type -> "
        "mom_combo (COMBO_MOMENTUM_23-08-2026: 1M +0.108 / 3M +0.185, both "
        "PASS/LONO-stable/split-half-stable — the 3M combo is the strongest "
        "direction result in the system), per-horizon ic_by_h replaces the "
        "min-horizon shrink, socket knobs softened per the EG note. Grading "
        "discipline as per the EG adoption note."),
    breaks=["2022-01-01"], notes=("Workweek switch Jan-2022: vol pool post-2022 only. "
    "CORRECTION 11-Jul-2026: re-run through the data_quality gate (EAND/ADCB/ADIB carried "
    "10 trading-halt rows with O=H=L=C and no volume, which flatten the YZ intraday range "
    "and bias the variance proxy DOWN). Immaterial as expected -- width_cal 1.056 -> 1.049, "
    "nu unchanged at 10, panel skill +0.0039 -> +0.0049, ALPHADHABI still a robust FAIL -- "
    "but the fit now conforms to the house cleaning gate."))
INDIA = MarketProfile("IN", "India (NSE)", [("2020-01-01", 0.0650)], 0.0650,
    "PLACEHOLDER — source 10Y G-Sec at first IN study.", "mom_12_1", +1, 0.07, False,
    nu=6.0, width_cal=1.021,
    fit_meta=(
        "REFIT 11-Jul-2026 on the 3-name IN panel (TMPV/RELIANCE/INFY, 51 windows, "
        "2021-2026), RE-RUN through the market-aware data-quality gate and the "
        "scale-normalized gate - EXACT REPRODUCTION of the 10-Jul fit: nu stays at "
        "the Gaussian limit, cal stays 0.930. Screened for the same phantom-row "
        "corruption found in the Korean export (144/170 of one Korean name's "
        "dropped rows fell on a Sunday, when the KOSPI is closed): India's export "
        "is CLEAN - 247.6 rows/yr across all three names, exactly the NSE calendar, "
        "zero phantom rows, no price-limit artifacts. Panel PARITY +0.0046 "
        "CI[-0.006,+0.016] on the corrected gate (was +0.002 on the old "
        "price-weighted one); top-name weight TMPV 43.7% (no single name dominates "
        "as badly as UAE's old IHC problem, but still the largest share of any "
        "3-name panel in the system - worth a 4th name). All three PARITY, zero "
        "FAILs: INFY +0.0070, RELIANCE +0.0090, TMPV -0.0001. SIGNAL RE-CONFIRMED "
        "OFF: empirical IC of mom_12_1 is -0.0933 against the house prior's sign=+1 "
        "- WRONG SIGN, same pattern as Egypt's now-retired rev_1m signal. LONO "
        "ablation shows ZERO difference between signal-ON and carry-only at this "
        "panel size (the dead-zone/cap machinery absorbs it either way) - not "
        "enough data to safely re-estimate the sign, so the mom_12_1/IC-0.07 prior "
        "is RETAINED unchanged for later re-estimation, signal_active stays False. "
        "The backtest carry schedule is still a flat 6.50% placeholder (RBI repo "
        "actually ranged 4.00->6.50->~5.50 over the window) - gate-neutral for "
        "skill scoring but MUST be sourced properly (live G-Sec / real RBI "
        "schedule) before any IN publish. "
        "UPDATE 27-Jul-2026 (calendar-horizon 3m adoption, PR #32 site-wide switch): "
        "re-fit fresh on the calendar 3-month window via refresh_market. nu stays "
        "Gaussian, cal 0.930 -> 0.986 -- +6.02% band move (WIDENS), MATERIAL on its "
        "own, no per-name churn (INFY/RELIANCE/TMPV all stay PARITY). Market panel "
        "PARITY +0.0042 CI[-0.002,0.011] (was +0.0046). Adopted on EXPLICIT user "
        "override of the standing 'no worsening' rule (instruction: 'switch all to "
        "one month and 3 months') -- the 6% widening is real and was surfaced "
        "before this shipped, not missed. Source: "
        "engine/PENDING_REVIEW/reverify_usa_qatar_india.json (IN.3m)."),
    notes="Robust Indian momentum evidence in the literature - but ablated OFF on "
          "the first panel; re-estimate as the panel grows.")
QATAR = MarketProfile("QA", "Qatar (QE)",
    carry_schedule=[
        ("2020-01-01", 0.0100), ("2022-03-17", 0.0125), ("2022-05-05", 0.0175),
        ("2022-06-16", 0.0225), ("2022-07-28", 0.0300), ("2022-09-22", 0.0375),
        ("2022-11-03", 0.0450), ("2022-12-15", 0.0500), ("2023-02-02", 0.0525),
        ("2023-03-23", 0.0550), ("2023-05-04", 0.0575), ("2023-07-27", 0.0600),
        ("2024-09-19", 0.0550), ("2024-11-08", 0.0525), ("2024-12-19", 0.0500),
        ("2025-09-18", 0.0475), ("2025-10-30", 0.0450), ("2025-12-11", 0.0425),
        ("2026-06-18", 0.0400),
    ],
    rf_live=0.0425,
    rf_live_source=("QCB-tracking ESTIMATE: Qatar's peg means QCB moved with the Fed on "
                    "essentially the SAMA dates/levels; schedule cloned from the Saudi "
                    "SAMA-repo schedule as the backtest carry (gate-neutral by "
                    "construction). FLAG per no-UST-shortcut rule: source a real QAR "
                    "sovereign/T-bill yield before any Qatar publish."),
    signal_type="rev_1m", signal_sign=-1, ic=0.06, signal_active=False,
    nu=6.0, width_cal=0.951,
    fit_meta=("Fitted 10-Jul-2026 on the 3-name QA panel (QGTS/QNB/IQCD, 54 windows, "
              "2021-2026) - REPLACES the provisional QGTS-only self-fit (Gaussian/"
              "0.916). nu=12, cal=0.972: thin-tailed pegged market, cone near-"
              "unbiased. Panel verdict PARITY -0.010 CI[-0.017,+0.001] - on low-vol "
              "Qatari mega-caps the HAR cascade adds ~nothing over trailing vol. "
              "Per-name (LONO, robust-verdict blocks {2,3,4}): QGTS PARITY -0.012 "
              "(robust; its old FAIL confirmed as the borrowed-config artifact), "
              "QNB PARITY -0.005 (robust), IQCD FAIL -0.018 (ROBUST across all "
              "blocks - a genuine name-level FAIL under own-market config, the "
              "first; HAR width underperforms plain trailing vol on this name; "
              "banner decision = separately-initiated publish step). "
              "UPDATE 27-Jul-2026 (calendar-horizon 3m adoption, PR #32 site-wide "
              "switch): re-fit fresh on the calendar 3-month window via refresh_market. "
              "nu 12 -> 10, cal 0.972 -> 0.937 -- -1.97% band move vs the live 60d "
              "incumbent, NON-MATERIAL, market panel narrows PARITY -0.0091 -> -0.0028. "
              "IQCD FAIL -> PARITY, the one per-name change -- but read this carefully "
              "before treating it as a clean improvement: IQCD's point skill is "
              "UNCHANGED to marginally worse (-0.0179 -> -0.0183); what moved is the "
              "CI, [-0.032,-0.004] -> [-0.035,+0.006], now crossing zero on fewer, "
              "noisier quarterly windows (51 vs 54). This is a LOSS OF STATISTICAL "
              "POWER under coarser windowing, not evidence IQCD got better -- adopted "
              "per the standing 'no worsening' rule on the letter (no name's verdict "
              "moves to a WORSE category, market narrows) while flagging that the "
              "mechanism here is reduced precision, not improved performance. QGTS/QNB "
              "unchanged PARITY. Windows 51 (vs 54 at 60d). Source: "
              "engine/PENDING_REVIEW/reverify_usa_qatar_india.json (QA.3m)."),
    notes="Thin literature: carry-only until a ~5-name Qatar panel exists.")

METALS = MarketProfile("XAU", "Metals (Gold/Silver, USD)", FED_SCHEDULE, 0.0363,
    "USD cost-of-carry anchor: Fed funds midpoint schedule (q=0, no dividend). "
    "Documented assumption: the carry-anchored null for a zero-yield USD store of "
    "value is spot x exp(rf) — the futures-contango-consistent center; gate-neutral "
    "(same anchor both sides).",
    None, +1, 0.0, False,
    nu=12.0, width_cal=0.958,
    fit_meta=("PROVISIONAL single-instrument self-fit 10-Jul-2026 (GOLD, 67 windows "
              "2009-2026): nu=12, cal=1.014 - near-Gaussian, tails far thinner than "
              "EGX (nu=4); the old borrowed t5 was too fat for metals. Verdict "
              "PARITY +0.009 CI[-0.003,+0.028] (near-PASS). Silver shares this fit, "
              "flagged, until its own OHLC panel exists. "
              "UPDATE 22-Jul-2026 (PR #13, de-circularization): raw_ohlc/XAG/SILVER.csv "
              "sat unused under a profile code ('XAG') the unattended loop never reads; "
              "moved to raw_ohlc/XAU/ so it pools natively under this profile - the FIRST "
              "time XAU has been a real multi-name panel. Panel: 2 names, 86 windows, "
              "nu 12->20 / cal 1.014->1.035. MARKET VERDICT PARITY -> PASS +0.0099 "
              "CI[0.001,0.015]. Per-name via LONO (fit excluding that name's own "
              "contribution, score it OOS - each metal's FIRST non-circular verdict): "
              "GOLD PARITY +0.0011, SILVER PASS +0.0181. A cross-code 3-metal pool "
              "(with platinum: nu=20, cal=0.965, 148w, all PARITY/PASS) was analyzed and "
              "NOT adopted - hard-coding pooled numbers across profile codes fights the "
              "per-market refit loop (every future run would flag materiality drift "
              "against a number that isn't really this profile's own fit). Per the "
              "standing per-market fit rule, XAU fits its own panel; XPT stays a "
              "flagged single-name provisional until copper history or an approved "
              "fit-group mechanism exists. "
              "UPDATE 27-Jul-2026 (calendar-horizon 3m adoption, PR #32 site-wide "
              "switch): re-fit on the calendar 3-month window. nu 20 -> 12, cal "
              "1.035 -> 1.0 -- -0.16% band move (essentially flat). BUT the MARKET "
              "VERDICT WORSENS: PASS -> PARITY (+0.0099 -> +0.0073 CI[-0.004,0.014]) "
              "even though neither name individually changes category -- GOLD stays "
              "PARITY (+0.0011 -> -0.0028), SILVER stays PASS (+0.0181 -> +0.0189). "
              "This is a pooled-panel effect, not a per-name one. Adopted on "
              "EXPLICIT user override of the standing 'no worsening' rule "
              "(instruction: 'switch all to one month and 3 months') -- the lost "
              "market-level PASS is real and was surfaced before this shipped, not "
              "missed. Metals remains the weakest calibration in the system either "
              "way -- read this cone with correspondingly less confidence than an "
              "EGX/GCC name regardless of which convention it's fitted on. Source: "
              "engine/PENDING_REVIEW/reverify_post_merge.json (XAU.3m)."),
    notes="Carry-only. Shape/width fitted on the pooled GOLD+SILVER panel (2 names, "
          "de-circularized via LONO as of 22-Jul-2026) - the first non-circular metals "
          "fit in the system. Still the weakest panel by name-count in Testahil.")

PLATINUM = MarketProfile("XPT", "Platinum (USD)", FED_SCHEDULE, 0.0363,
    "USD cost-of-carry anchor: Fed funds midpoint schedule (q=0, no yield). Same "
    "documented assumption as METALS: the carry-anchored null for a zero-yield USD "
    "store of value is spot x exp(rf); gate-neutral (same anchor both sides).",
    None, +1, 0.0, False,
    nu=8.0, width_cal=0.86,
    fit_meta=("PROVISIONAL single-instrument self-fit 20-Jul-2026 (PLATINUM, 62 windows "
              "2012-2026, production chain, reproduction check vs live gold registry EXACT: "
              "67 windows, +0.0035, CI[-0.005,+0.013]): nu=Gaussian (MLE scale 0.790 -> "
              "width_cal 0.853, clip floor 0.85 active). Verdict PARITY -0.0004 "
              "CI[-0.009,+0.009] robust {2,3,4}. De-circularized cross-check (fit "
              "gold+silver, score platinum OOS): PARITY -0.0114 CI[-0.032,+0.009]. "
              "Borrowed live METALS (Gaussian/1.0): PARITY -0.0094. Pooled 3-metal fit "
              "(nu=20, cal=0.965, 148 windows) is the likely future config once metals "
              "pool - NOT adopted (per-market fit rule). Platinum does NOT arrive "
              "failing. Step-0.0 gate: 4041->4032 rows, 260.0 rows/yr = metals Mon-Fri "
              "calendar, zero corporate-action repairs. "
              "UPDATE 27-Jul-2026 (calendar-horizon 3m adoption, PR #32 site-wide "
              "switch): re-fit on the calendar 3-month window. nu Gaussian -> 8, cal "
              "0.853 -> 0.86 -- +13.98% band move, the LARGEST widening of any market "
              "checked in this pass -- driven mainly by the tail thickening from the "
              "Gaussian limit to t(8), not the small width_cal change. Verdict stays "
              "PARITY (+0.0078, unchanged). Single-name panel, so this IS the market. "
              "Adopted on EXPLICIT user override of the standing 'no worsening' rule "
              "(instruction: 'switch all to one month and 3 months') -- this is the "
              "single biggest cone widening shipped in this batch and was surfaced "
              "plainly before it went out, not buried. Metals remains the weakest "
              "calibration in the system regardless of horizon convention. Source: "
              "engine/PENDING_REVIEW/calendar_horizon_refit_3m.json (XPT.3m, "
              "cross-checked: incumbent in that file matches live production exactly, "
              "unlike the KR entry there which was stale)."),
    notes="Carry-only. Single-name PROVISIONAL self-fit, flagged circular like gold's "
          "first fit; metals remain the weakest calibration in the system.")

PROFILES = {p.code: p for p in [EGYPT, SAUDI, USA, UK, BRAZIL, KOREA, UAE, INDIA, QATAR, METALS, PLATINUM]}
