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
    breaks: List[str] = field(default_factory=list)
    notes: str = ""

    def carry_rate(self, date) -> float:
        d = pd.Timestamp(date)
        r = self.carry_schedule[0][1]
        for eff, rate in self.carry_schedule:
            if d >= pd.Timestamp(eff):
                r = rate
        return r


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
    breaks=["2015-06-15"],
    notes=("Signal OFF (fallback rule): 1-name panel cannot establish IC; literature "
           "sign-unstable (contrarian post-2015 opening). Runs carry-only until the "
           "Saudi panel reaches ~5 covered names."),
)

# ---- Approved-design stubs (priors from the two profile tables signed off 09/10-Jul) ----
USA = MarketProfile("US", "United States", [("2020-01-01", 0.0458)], 0.0458,
    "UST 10Y 4.58% (tradingeconomics 8-Jul-2026, cached CoC-Reference); use 3M bill 3.71% "
    "(investing.com 10-Jul-2026) for the 60d carry at publish.",
    "mom_12_1", +1, 0.05, True, nu=None,
    notes="Mature-market momentum prior (JT 12-1).")
UK = MarketProfile("GB", "United Kingdom", [("2020-01-01", 0.0400)], 0.0400,
    "PLACEHOLDER — source gilt/3M at first UK study.", "mom_12_1", +1, 0.05, True,
    notes="Strong UK momentum literature.")
BRAZIL = MarketProfile("BR", "Brazil", [("2020-01-01", 0.1300)], 0.1300,
    "PLACEHOLDER — source Selic/DI at first BR study.", "mom_12_1", +1, 0.07, True,
    notes="EM momentum prior (Rouwenhorst).")
KOREA = MarketProfile("KR", "South Korea", [("2020-01-01", 0.0300)], 0.0300,
    "PLACEHOLDER — source KTB at first KR study.", None, +1, 0.03, False,
    notes="Asia momentum-failure pattern: carry-only.")
UAE = MarketProfile("AE", "UAE (ADX/DFM)", [("2020-01-01", 0.0450)], 0.0450,
    "PLACEHOLDER — source AED federal bond; never UST (peg rule).", "rev_1m", -1, 0.06, False,
    breaks=["2022-01-01"], notes="Workweek switch Jan-2022: vol pool post-2022 only. "
    "Signal off until 5-name panel estimated (FAB/ENBD/EMAAR/ADNOCGAS/IHC available). "
    "IHC needs liquidity screen.")
INDIA = MarketProfile("IN", "India (NSE)", [("2020-01-01", 0.0650)], 0.0650,
    "PLACEHOLDER — source 10Y G-Sec at first IN study.", "mom_12_1", +1, 0.07, True,
    notes="Robust Indian momentum evidence.")
QATAR = MarketProfile("QA", "Qatar (QE)", [("2020-01-01", 0.0450)], 0.0450,
    "PLACEHOLDER — source QAR sovereign; never UST (peg rule).", "rev_1m", -1, 0.06, False,
    notes="Thin literature: carry-only until panel.")

PROFILES = {p.code: p for p in [EGYPT, SAUDI, USA, UK, BRAZIL, KOREA, UAE, INDIA, QATAR]}
