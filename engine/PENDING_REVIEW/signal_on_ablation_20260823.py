"""Mini-ablation for the 23-Aug-2026 committed-drift adoption: signal ON vs OFF
on a representative subset, engine's own backtest_v3 + pooled_scores, both
calendar horizons. RESEARCH RECORD for the adoption commit — the full-panel
refit under signal-ON runs at the next unattended refresh through the standing
materiality gate."""
import sys
import json
import warnings

warnings.filterwarnings("ignore")
sys.path.insert(0, "engine")
import numpy as np                      # noqa: E402
import pandas as pd                     # noqa: E402
from data_quality import clean_ohlc     # noqa: E402
import market_profiles as MP            # noqa: E402
from mc_v3 import backtest_v3, pooled_scores  # noqa: E402

NAMES = {"AE": ["EMAAR", "ADCB", "ALDAR", "DIB", "FAB"],
         "EG": ["COMI", "HRHO", "ETEL", "ABUK"],
         "SA": ["SABIC", "RAJHI", "RIBL"]}


def load(mkt, tk):
    df = pd.read_csv(f"engine/raw_ohlc/{mkt}/{tk}.csv")
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
    for c in ("Price", "Open", "High", "Low"):
        df[c] = df[c].astype(str).str.replace(",", "", regex=False).astype(float)
    df = df.sort_values("Date").reset_index(drop=True)
    df, _ = clean_ohlc(df, ticker=tk, verbose=False, market=mkt)
    return df


out = {}
for mkt, names in NAMES.items():
    prof = MP.PROFILES[mkt]
    out[mkt] = {}
    for hm in (1, 3):
        fr_on, fr_off = [], []
        for tk in names:
            df = load(mkt, tk)
            for use, bucket in ((True, fr_on), (False, fr_off)):
                r = backtest_v3(df, prof, horizon_months=hm, use_signal=use,
                                n_paths=8000)
                if len(r):
                    r["name"] = tk
                    bucket.append(r)
        s_on, r_on = pooled_scores(fr_on)
        s_off, r_off = pooled_scores(fr_off)
        act = r_on[r_on["alpha"] != 0]
        hit = float((np.sign(act["alpha"]) ==
                     np.sign(np.log(act["realized"] / act["spot"])
                             - (act["drift"] - act["alpha"]))).mean()) \
            if len(act) else None
        out[mkt][f"{hm}M"] = {
            "n": s_on["n"],
            "tilted_share": float(len(act)) / max(s_on["n"], 1),
            "crps_skill_ON": round(s_on["crps_skill"], 4),
            "crps_skill_OFF": round(s_off["crps_skill"], 4),
            "pin50_ON": round(s_on["pin50_skill"], 4),
            "pin50_OFF": round(s_off["pin50_skill"], 4),
            "cov90_ON": round(s_on["cov90"], 3),
            "cov90_OFF": round(s_off["cov90"], 3),
            "tilt_direction_hit_rate": round(hit, 3) if hit is not None else None}
        print(mkt, hm, out[mkt][f"{hm}M"], flush=True)

with open("engine/PENDING_REVIEW/signal_on_ablation_20260823.json", "w") as f:
    json.dump(out, f, indent=1)
print("wrote engine/PENDING_REVIEW/signal_on_ablation_20260823.json")
