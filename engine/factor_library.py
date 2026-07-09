"""
Testahil — Factor Library (code form of Appendix A + the calibrated developer numbers).

Three tiers (the universal machinery):
  C  continuous       -> contributes a forward DRIFT to price; diffusion vol comes from the
                         instrument's realized vol (calibrated from OHLC), so C vol here is
                         informational / for stress modes, NOT double-counted in the base run.
  M  macro base-rate  -> discrete jump: probability over the window + impact (mean, spread).
  E  idiosyncratic    -> discrete jump: probability + impact (mean, spread).

All drift/prob/impact numbers are EDITABLE JUDGMENTS (the table IS the model). The EGX-developer
class is calibrated from the published TMGH study (real). Every other class carries the Appendix-A
factor STRUCTURE with starting magnitudes flagged calibrated=False — these are red-pen defaults to
tune at the new-asset sign-off touchpoint, never finals to publish blind.
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Factor:
    name: str
    tier: str                 # 'C' | 'M' | 'E'
    sign: str                 # '+', '-', '--', 'mixed'
    channel: str = ""
    # continuous (C):
    drift_3m: Optional[float] = None   # price-space 3-month drift contribution
    vol_3m: Optional[float] = None     # price-space 3-month vol (informational in base run)
    # discrete (M/E):
    prob: Optional[float] = None       # probability of occurring within the window
    impact_mean: Optional[float] = None
    impact_spread: Optional[float] = None
    calibrated: bool = False


# ----------------------------------------------------------------------------- ticker -> class
_TICKER_CLASS = {
    "PHDC": "egx_developer", "TMGH": "egx_developer", "HELI": "egx_developer", "EMFD": "egx_developer",
    "ORAS": "egx_contractor",
    "COMI": "egx_bank", "HRHO": "egx_bank", "BTFH": "egx_bank",
    "CCAP": "egx_holdco",
    "FWRY": "egx_payments",
    "ABUK": "egx_fertilizer", "MFPC": "egx_fertilizer",
    "EFID": "egx_staples",
    "XAGUSD": "metals", "XAUUSD": "metals", "SILVER": "metals", "GOLD": "metals",
}

def classify(ticker: str) -> str:
    """Generation rule, step 1: ticker -> asset class. Unknown -> raises (sign off a new set first)."""
    t = ticker.upper().strip()
    if t not in _TICKER_CLASS:
        raise KeyError(
            f"{ticker!r} is not in any existing class. Generate a new factor set into the three-tier "
            f"structure and sign it off (the new-asset touchpoint) before running."
        )
    return _TICKER_CLASS[t]


# ----------------------------------------------------------------------------- 1. EGX developer
# Calibrated from the published TMGH study (§3.1). Real numbers.
_DEVELOPER = [
    Factor("CBE policy-rate path", "C", "-", "discounting; softened if net-cash", drift_3m=+0.020, vol_3m=0.04, calibrated=True),
    Factor("EGP/USD rate", "C", "-", "build-cost, translation, USD revenue", drift_3m=-0.025, vol_3m=0.07, calibrated=True),
    Factor("Inflation (CPI)", "C", "mixed", "real-asset hedge vs construction cost", drift_3m=+0.015, vol_3m=0.04, calibrated=True),
    Factor("EGX30 & foreign flows", "C", "+", "market beta, liquidity", drift_3m=+0.015, vol_3m=0.07, calibrated=True),
    Factor("Brent / Gulf liquidity", "C", "+", "GCC buyer purchasing power", drift_3m=+0.005, vol_3m=0.05, calibrated=True),
    Factor("Geopolitical / regional security", "M", "-", "risk-premium shock", prob=0.30, impact_mean=-0.12, impact_spread=0.05, calibrated=True),
    Factor("Cross-border JV inflows (KSA/Oman/Iraq)", "E", "+", "Banan/Oman/Baghdad funding & sentiment", prob=0.30, impact_mean=+0.06, impact_spread=0.04, calibrated=True),
    Factor("Project launch & sales execution", "E", "+", "SouthMED / Spine / Noor", prob=0.55, impact_mean=+0.08, impact_spread=0.04, calibrated=True),
    Factor("Tourism & hospitality demand", "E", "+", "owned hotels", prob=0.45, impact_mean=+0.04, impact_spread=0.06, calibrated=True),
    Factor("Mortgage finance & credit", "E", "+", "affordability, velocity", prob=0.35, impact_mean=+0.02, impact_spread=0.05, calibrated=True),
]

# ------------------------------------------------------- helper to build to-calibrate default sets
def _C(name, sign, channel, drift, vol):
    return Factor(name, "C", sign, channel, drift_3m=drift, vol_3m=vol, calibrated=False)

def _ev(name, tier, sign, channel, p, mean, spread):
    return Factor(name, tier, sign, channel, prob=p, impact_mean=mean, impact_spread=spread, calibrated=False)

# ----------------------------------------------------------------------------- other EGX classes
# Structure from Appendix A; magnitudes are starting judgments (calibrated=False) to red-pen.
_CONTRACTOR = [
    _C("EGP/USD rate", "mixed", "USD reporting; EGP contract translation", +0.000, 0.06),
    _C("CBE rate / working-capital cost", "-", "funding long-cycle projects", -0.010, 0.04),
    _C("EGX30 & foreign flows", "+", "beta, liquidity", +0.015, 0.07),
    _C("Oil & regional infra-capex cycle", "+", "project pipeline (Egypt+Gulf)", +0.010, 0.06),
    _C("Input cost (steel/cement/labour)", "-", "margin channel", -0.010, 0.05),
    _ev("Geopolitical / regional security", "M", "-", "project-country risk", 0.30, -0.10, 0.05),
    _ev("Public-sector payment & receivables", "M", "-", "arrears / cash conversion", 0.30, -0.05, 0.04),
    _ev("Fiscal / infrastructure-spend program", "M", "+", "award pipeline", 0.30, +0.05, 0.04),
    _ev("Major contract award or loss", "E", "mixed", "per named tender", 0.45, +0.04, 0.07),
    _ev("Backlog burn / completion milestone", "E", "+", "revenue recognition", 0.40, +0.04, 0.04),
    _ev("Claim / dispute / impairment", "E", "-", "one-off P&L", 0.25, -0.06, 0.05),
]
_BANK = [  # note the rate SIGN FLIP
    _C("CBE policy-rate path", "+", "NIM vs funding cost", +0.020, 0.04),
    _C("EGP/USD rate", "+", "treasury FX gains, dollarization", +0.010, 0.06),
    _C("Inflation (CPI)", "+", "nominal loan growth, fee income", +0.010, 0.04),
    _C("EGX30 & foreign flows", "+", "beta; brokerage/IB (HRHO/BTFH)", +0.015, 0.07),
    _C("Private-sector credit growth", "+", "loan-book expansion", +0.010, 0.04),
    _ev("Geopolitical / regional security", "M", "-", "risk premium, deposit-flight tail", 0.30, -0.10, 0.05),
    _ev("Asset-quality / NPL-cycle shift", "M", "-", "ECL provisioning regime", 0.30, -0.06, 0.04),
    _ev("Capital / dividend-payout change", "M", "mixed", "distributable earnings", 0.25, +0.02, 0.05),
    _ev("Sovereign rating / T-bill yield regime", "M", "mixed", "large gov-securities book", 0.30, +0.02, 0.05),
    _ev("Earnings surprise (NIM/ECL/fees)", "E", "mixed", "quarterly print", 0.50, +0.02, 0.06),
    _ev("M&A / capital action", "E", "mixed", "deal flow / capital raise", 0.30, +0.03, 0.06),
    _ev("Non-recurring ECL release / one-off", "E", "mixed", "normalize per COMI rule", 0.30, 0.00, 0.05),
]
_HOLDCO = [
    _C("EGP/USD rate", "-", "USD sub-debt servicing, FX on portfolio", -0.030, 0.08),
    _C("CBE rate", "-", "cost of debt across levered portfolio", -0.015, 0.05),
    _C("EGX30 & foreign flows", "+", "holdco-discount narrows w/ sentiment", +0.020, 0.08),
    _C("Energy / commodity complex", "+", "largest assets energy/refining", +0.015, 0.07),
    _C("Inflation (CPI)", "mixed", "portfolio nominal revenue", +0.005, 0.05),
    _ev("Geopolitical / regional security", "M", "-", "risk premium", 0.30, -0.12, 0.05),
    _ev("Holdco-discount regime shift", "M", "mixed", "sentiment toward conglomerates", 0.30, +0.04, 0.06),
    _ev("Sovereign / credit event (refinancing)", "M", "-", "USD-debt rollover risk", 0.25, -0.08, 0.06),
    _ev("Subsidiary catalyst", "E", "+", "per named platform", 0.40, +0.06, 0.05),
    _ev("Debt restructuring / refinancing", "E", "mixed", "USD sub-debt event", 0.30, +0.04, 0.07),
    _ev("Portfolio monetization / exit", "E", "+", "asset sale crystallizes NAV", 0.30, +0.06, 0.05),
]
_PAYMENTS = [
    _C("CBE policy-rate path", "mixed", "float income vs multiple compression", +0.000, 0.05),
    _C("Inflation (CPI)", "mixed", "nominal txn value vs real consumption", +0.005, 0.04),
    _C("Consumer spending / digitization", "+", "transaction volume & velocity", +0.020, 0.06),
    _C("EGX30 & foreign flows", "+", "high-beta growth name", +0.020, 0.08),
    _C("EGP/USD rate", "-", "USD tech / platform costs", -0.005, 0.05),
    _ev("Geopolitical / regional security", "M", "-", "risk premium, beta drawdown", 0.30, -0.10, 0.05),
    _ev("Regulatory / instant-payments (IPN, fees)", "M", "mixed", "tailwind vs fee caps / InstaPay", 0.30, +0.02, 0.06),
    _ev("Consumer-credit cycle", "M", "mixed", "BNPL / lending-arm exposure", 0.30, +0.02, 0.05),
    _ev("New vertical launch", "E", "+", "per named product", 0.45, +0.06, 0.05),
    _ev("Major biller / merchant partnership or loss", "E", "mixed", "network reach", 0.40, +0.04, 0.06),
    _ev("Earnings surprise (throughput, take rate)", "E", "mixed", "quarterly print", 0.50, +0.03, 0.06),
    _ev("Competitive disruption (InstaPay / new entrant)", "E", "-", "volume / take-rate erosion", 0.30, -0.06, 0.05),
]
_FERTILIZER = [  # FX flip: exports USD-priced -> devaluation positive
    _C("Global urea / ammonia price", "+", "dominant revenue driver", +0.020, 0.08),
    _C("Natural-gas feedstock cost", "-", "main input (regulated gas price)", -0.010, 0.05),
    _C("EGP/USD rate", "+", "exports priced USD; devaluation lifts EGP rev", +0.015, 0.06),
    _C("Brent / energy complex", "mixed", "co-moves w/ gas, ammonia, freight", +0.005, 0.06),
    _C("Global agricultural / crop demand", "+", "fertilizer demand", +0.010, 0.05),
    _C("EGX30 & foreign flows", "+", "beta, liquidity", +0.015, 0.07),
    _ev("Geopolitical / regional security", "M", "mixed", "Suez/Red Sea freight, gas supply", 0.30, -0.04, 0.06),
    _ev("Egypt gas-price / subsidy reset", "M", "-", "step change in feedstock cost", 0.30, -0.06, 0.05),
    _ev("Export quota / domestic-allocation policy", "M", "-", "caps exportable volume", 0.25, -0.05, 0.04),
    _ev("Global gas / energy shock", "M", "+", "spikes product prices (tail)", 0.20, +0.08, 0.06),
    _ev("Plant turnaround / outage / expansion", "E", "mixed", "utilization", 0.35, +0.02, 0.06),
    _ev("Gas-supply curtailment to the plant", "E", "-", "Egypt cuts gas in shortages", 0.30, -0.07, 0.05),
    _ev("Earnings surprise / dividend", "E", "mixed", "high-payout names", 0.45, +0.03, 0.05),
]
_STAPLES = [  # FX is a margin NEGATIVE (imported inputs)
    _C("Inflation (CPI)", "mixed", "input-cost pressure vs pricing power", +0.005, 0.04),
    _C("EGP/USD rate", "-", "imported wheat/oils/packaging", -0.010, 0.05),
    _C("Soft-commodity inputs (wheat/sugar/oils/resin)", "-", "COGS", -0.010, 0.05),
    _C("Consumer disposable income / real wages", "+", "volume; down-trading risk", +0.010, 0.04),
    _C("EGX30 & foreign flows", "+", "beta (defensive, lower)", +0.010, 0.05),
    _ev("Geopolitical / regional security", "M", "-", "wheat supply (Black Sea) & risk premium", 0.30, -0.05, 0.04),
    _ev("Subsidy / staple-price policy", "M", "mixed", "government food-price intervention", 0.30, +0.02, 0.05),
    _ev("Global soft-commodity shock", "M", "-", "wheat / sugar spike", 0.25, -0.05, 0.05),
    _ev("Consumer purchasing-power cycle", "M", "+", "volume", 0.30, +0.03, 0.04),
    _ev("New product / SKU / capacity expansion", "E", "+", "per named launch", 0.40, +0.04, 0.04),
    _ev("Pricing pass-through (success/failure)", "E", "mixed", "margin recovery", 0.40, +0.03, 0.05),
    _ev("Earnings surprise (volume, margin)", "E", "mixed", "quarterly print", 0.50, +0.02, 0.05),
    _ev("Market-share / competitive move", "E", "mixed", "per event", 0.35, +0.02, 0.05),
]
_METALS = [  # cost-curve / real-rate model (silver/gold)
    _C("Real US 10-year yield", "-", "opportunity cost of non-yielding metal", -0.020, 0.06),
    _C("DXY (US dollar index)", "-", "priced in USD", -0.010, 0.05),
    _C("Industrial demand / global PMI", "+", "silver industrial leg", +0.010, 0.06),
    _C("Cross-metal beta (gold; G/S ratio)", "+", "silver tracks gold, higher beta", +0.015, 0.08),
    _C("Fed-path / real-rate expectations", "-", "forward discounting of carry", -0.010, 0.05),
    _ev("Geopolitical / safe-haven shock", "M", "+", "haven bid", 0.30, +0.06, 0.05),
    _ev("Central-bank buying regime", "M", "+", "structural demand shift", 0.25, +0.04, 0.04),
    _ev("Monetary-policy regime change (Fed pivot)", "M", "+", "re-rating of the complex", 0.25, +0.06, 0.05),
    _ev("Inventory / supply shock", "E", "+", "COMEX/LBMA draw, mine disruption", 0.30, +0.05, 0.05),
    _ev("Large COT positioning unwind", "E", "-", "spec-long liquidation", 0.30, -0.06, 0.05),
    _ev("ETF physical-flow surge", "E", "+", "SLV/GLD demand", 0.30, +0.04, 0.04),
]

_LIBRARY = {
    "egx_developer": _DEVELOPER,
    "egx_contractor": _CONTRACTOR,
    "egx_bank": _BANK,
    "egx_holdco": _HOLDCO,
    "egx_payments": _PAYMENTS,
    "egx_fertilizer": _FERTILIZER,
    "egx_staples": _STAPLES,
    "metals": _METALS,
}


def get_factors(asset_class: str):
    if asset_class not in _LIBRARY:
        raise KeyError(f"No factor set for class {asset_class!r}. Classes: {sorted(_LIBRARY)}")
    return list(_LIBRARY[asset_class])


def for_ticker(ticker: str):
    """Convenience: ticker -> (asset_class, factors)."""
    cls = classify(ticker)
    return cls, get_factors(cls)


def split(factors):
    """Return (continuous, events) for the engine."""
    cont = [f for f in factors if f.tier == "C"]
    events = [f for f in factors if f.tier in ("M", "E")]
    return cont, events


def is_calibrated(factors) -> bool:
    return all(f.calibrated for f in factors)
