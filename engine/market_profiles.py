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
    signal_type="rev_1m", signal_sign=-1, ic=0.08, signal_active=True,
    nu=4.0, width_cal=0.965,
    fit_meta=("Fitted 10-Jul-2026 on the 7-name EG panel (EMFD/GBCO/KABO/OCDI/ORHD/"
              "PHDC/TMGH, 115 windows), LONO-stable (per-name nu=4, cal 0.92-0.99). "
              "Panel verdict under this fit: PASS +0.062 CI[+0.036,+0.078]."),
    breaks=["2016-11-03", "2022-03-21", "2023-01-11"],
    notes=("Literature: no EGX momentum; overreaction/short-term reversal supported "
           "(EGX event studies; Kuwait 1m reversal ~3.1%/mo t≈4.4 as GCC analogue). "
           "Signal sign/IC re-estimated on the 6-name pooled panel each cycle."),
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
    signal_type="mom_12_1", signal_sign=-1, ic=0.06, signal_active=False,
    nu=5.0, width_cal=1.28,
    fit_meta=("Fitted 10-Jul-2026 on the 2-name SA panel (ALINMA/MAADEN, 36 windows). "
              "MLE scale wanted 1.40; shrink_cal CAP (1.30) binding at 1.28 -> Saudi "
              "HAR structurally a touch narrow; revisit the cap as the panel passes "
              "~5 names. Panel verdict: PASS +0.022 CI[+0.001,+0.041]. ALINMA is "
              "BOUNDARY (skill -0.010; CI edge flips sign with bootstrap block size "
              "2 vs 3/4) -> per the robust-verdict rule it stays PARITY-flagged, not "
              "FAIL; review at its first live grade (T+20 2026-08-04). LONO with n=2 "
              "is unstable (single-name fits) - the pooled fit is the production config."),
    breaks=["2015-06-15"],
    notes=("Signal OFF (fallback rule): 1-name panel cannot establish IC; literature "
           "sign-unstable (contrarian post-2015 opening). Runs carry-only until the "
           "Saudi panel reaches ~5 covered names."),
)

# ---- Approved-design stubs (priors from the two profile tables signed off 09/10-Jul) ----
USA = MarketProfile("US", "United States", FED_SCHEDULE, 0.0363,
    "UST 10Y 4.58% (tradingeconomics 8-Jul-2026, cached CoC-Reference); use 3M bill 3.71% "
    "(investing.com 10-Jul-2026) for the 60d carry at publish.",
    "mom_12_1", +1, 0.05, False, nu=12.0, width_cal=1.014,
    fit_meta=("Fitted 10-Jul-2026 on the 3-name US panel (AAPL/NVDA/TSLA, 54 windows, "
              "2021-2026): nu=12, cal=1.014 - thin tails like metals, far from EGX. "
              "SIGNAL ABLATION on this panel: carry-only (+0.012 CI[-0.006,+0.017]) "
              "marginally beats the mom_12_1 prior ON (+0.010 CI[-0.013,+0.019]) -> "
              "fallback rule applies, signal_active=False; the JT prior is retained "
              "for re-estimation at ~5 names. Panel verdict PARITY. Per-name "
              "(carry-only LONO, robust blocks): AAPL PARITY -0.002 (was BOUNDARY "
              "with the signal ON - the momentum prior was hurting it), NVDA PARITY "
              "+0.002, TSLA PARITY +0.015."),
    notes="Mature-market momentum prior (JT 12-1) - ablated OFF on the first panel; "
          "re-estimate as the panel grows.")
UK = MarketProfile("GB", "United Kingdom", [("2020-01-01", 0.0400)], 0.0400,
    "PLACEHOLDER — source gilt/3M at first UK study.", "mom_12_1", +1, 0.05, True,
    notes="Strong UK momentum literature.")
BRAZIL = MarketProfile("BR", "Brazil", [("2020-01-01", 0.1300)], 0.1300,
    "PLACEHOLDER — source Selic/DI at first BR study.", "mom_12_1", +1, 0.07, True,
    notes="EM momentum prior (Rouwenhorst).")
KOREA = MarketProfile("KR", "South Korea", [("2020-01-01", 0.0300)], 0.0300,
    "PLACEHOLDER — source KTB at first KR study.", None, +1, 0.03, False,
    nu=6.0, width_cal=1.070,
    fit_meta=("Fitted 10-Jul-2026 on the 3-name KR panel (SAMSUNG/KAKAO/LGES, 55 "
              "windows, 2021-2026): nu=6, cal=1.070. DATA REPAIR: the KAKAO "
              "investing.com export interleaved pre/post-split price scales through "
              "Mar-Apr 2021 (13 rows at ~5x); repaired exactly (rows with Price>"
              "200,000 KRW / 5, the corporate 5:1 ratio) - before the repair a "
              "single poisoned trailing-vol window fabricated +0.33 'skill'. Panel "
              "verdict PARITY +0.006 CI[-0.006,+0.008]. Per-name (LONO, robust "
              "blocks): SAMSUNG PARITY -0.022, KAKAO PARITY +0.006, LGES PARITY "
              "+0.005. Supersedes the legacy per-instrument Samsung KVOL=1.30 "
              "uplift from the v1-era site config."),
    notes="Asia momentum-failure pattern: carry-only.")
UAE = MarketProfile("AE", "UAE (ADX/DFM)", [("2020-01-01", 0.0450), ("2026-07-01", 0.0393)], 0.0393,
    "3M EIBOR (CBUAE fixings; Fed-mirror via the peg) — never UST. Long rf for CoC: AED federal T-bond.",
    "rev_1m", -1, 0.06, False,
    nu=250.0, width_cal=1.042,
    fit_meta=("PROVISIONAL 1-NAME FIT 10-Jul-2026 on ALPHADHABI (14 non-overlapping 60d "
              "windows, post-2022 ADX-workweek panel, 2023-2026): MLE selected the "
              "Gaussian limit (nu=250 encodes normal), cal=1.042 (shrink 0.7). Backtest "
              "carry = CBUAE mirror of the Fed schedule. Name verdict PARITY +0.006 "
              "CI[-0.008,+0.016], P(skill>0)=0.80, robust blocks {2,3,4}. QGTS-precedent "
              "rule applies: single-name AE fit is provisional — no AE name-level FAIL "
              "is real, and this fit is re-estimated, once a >=3-name panel exists "
              "(FAB/ENBD/EMAAR/ADNOCGAS/ALDAR/IHC candidates; IHC needs a liquidity "
              "screen). Panel frame: engine/panels/AE_ALPHADHABI_60d.csv."),
    breaks=["2022-01-01"], notes="Workweek switch Jan-2022: vol pool post-2022 only. "
    "Signal off until 5-name panel estimated (FAB/ENBD/EMAAR/ADNOCGAS/IHC available). "
    "IHC needs liquidity screen.")
INDIA = MarketProfile("IN", "India (NSE)", [("2020-01-01", 0.0650)], 0.0650,
    "PLACEHOLDER — source 10Y G-Sec at first IN study.", "mom_12_1", +1, 0.07, False,
    nu=250.0, width_cal=0.930,
    fit_meta=("Fitted 10-Jul-2026 on the 3-name IN panel (TMPV/RELIANCE/INFY, 51 "
              "windows, 2021-2026): MLE selected the Gaussian limit (nu=250 encodes "
              "normal), cal=0.930 - thin tails, cone ~7% wide. SIGNAL ABLATION is "
              "DECISIVE: the mom_12_1 prior HURTS (panel -0.018 ON vs +0.002 "
              "carry-only) despite India's strong momentum literature -> fallback "
              "rule, signal_active=False; re-estimate at ~5 names. Panel verdict "
              "PARITY +0.002 CI[-0.007,+0.016]. Per-name (carry-only LONO, robust "
              "blocks): TMPV PARITY -0.009, RELIANCE PARITY +0.006, INFY PARITY "
              "+0.004 - all robust. NB the backtest carry schedule is a flat 6.50% "
              "placeholder (RBI repo actually 4.00->6.50->~5.50 over the window) - "
              "gate-neutral for skill, but source the real schedule + live G-Sec "
              "before any IN publish."),
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
    nu=12.0, width_cal=0.972,
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
              "banner decision = separately-initiated publish step)."),
    notes="Thin literature: carry-only until a ~5-name Qatar panel exists.")

METALS = MarketProfile("XAU", "Metals (Gold/Silver, USD)", FED_SCHEDULE, 0.0363,
    "USD cost-of-carry anchor: Fed funds midpoint schedule (q=0, no dividend). "
    "Documented assumption: the carry-anchored null for a zero-yield USD store of "
    "value is spot x exp(rf) — the futures-contango-consistent center; gate-neutral "
    "(same anchor both sides).",
    None, +1, 0.0, False,
    nu=12.0, width_cal=1.014,
    fit_meta=("PROVISIONAL single-instrument self-fit 10-Jul-2026 (GOLD, 67 windows "
              "2009-2026): nu=12, cal=1.014 - near-Gaussian, tails far thinner than "
              "EGX (nu=4); the old borrowed t5 was too fat for metals. Verdict "
              "PARITY +0.009 CI[-0.003,+0.028] (near-PASS). Silver shares this fit, "
              "flagged, until its own OHLC panel exists."),
    notes="Carry-only. Shape/width fitted on the gold panel; silver SHARES the "
          "metals fit until its own OHLC panel exists (flagged).")

PROFILES = {p.code: p for p in [EGYPT, SAUDI, USA, UK, BRAZIL, KOREA, UAE, INDIA, QATAR, METALS]}
