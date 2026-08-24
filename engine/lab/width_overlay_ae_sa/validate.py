"""Per-name width overlay — AE/SA promotion gate (24-Aug-2026, per instruction:
"we need to stop looking at stocks in a country as a bulk").

Replays the EXACT adopted EG mechanism (adaptive_width constants imported, never
restated) walk-forward on every AE and SA name's own library, and applies the same
promotion gate the EG adoption cleared on 23-Jul-2026:

  1. proper score  — pooled crps/spot with the overlay vs baseline must be PARITY
                     (not robustly worse) across bootstrap blocks {2,3,4};
  2. calibration   — pooled |std_u - 1| must IMPROVE;
  3. breadth       — a majority of gated names must move CLOSER to std_u = 1;
  4. coverage      — pooled cov90 must stay in-band (not leave [0.85, 0.95]).

Walk-forward safe: the multiplier applied at window k is computed from windows
< k only, with the MIN_WINDOWS history gate forcing 1.0 exactly as production
does. Names that never clear the gate contribute mult == 1 throughout (they
dilute the improvement honestly, as in the EG record).
"""
import json
import os
import sys
import warnings
from multiprocessing import Pool

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ENGINE)

import adaptive_width as AW                                      # noqa: E402
import market_profiles as MP                                     # noqa: E402
from data_quality import clean_ohlc                              # noqa: E402
from mc_v3 import (fit_har_v3, har_forecast_v3, carry_log_h,     # noqa: E402
                   simulate_terminal_v3, crps_sample)
from panel_refresh import verdict_ci                             # noqa: E402

N_PATHS = 4000
SEED = 42


def load(mkt, name):
    df = pd.read_csv(f"{ENGINE}/raw_ohlc/{mkt}/{name}.csv")
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
    for c in ("Price", "Open", "High", "Low"):
        df[c] = df[c].astype(str).str.replace(",", "", regex=False).astype(float)
    df = df.sort_values("Date").reset_index(drop=True)
    df, _ = clean_ohlc(df, ticker=name, verbose=False, market=mkt)
    return df


def walk(job):
    """One name: resolved windows with the walk-forward multiplier and paired CRPS."""
    mkt, name = job
    prof = MP.PROFILES[mkt]
    cal = float(prof.width_cal)
    nu = float(prof.nu)
    try:
        df = load(mkt, name)
    except Exception as e:
        return dict(name=name, error=str(e))
    from primitives import yz_variance_proxy
    v = yz_variance_proxy(df)
    close = df["Price"].values
    rows = []
    u2_hist = []
    o = AW.MIN_HIST
    n = len(df)
    while o + AW.H < n:
        beta, s2 = fit_har_v3(v, o, horizon=AW.H)
        dv = har_forecast_v3(v, o, beta, s2, horizon=AW.H)
        sig = float(np.sqrt(dv * AW.H) * cal)
        if sig > 0:
            # multiplier from the RESOLVED past only, gated exactly like production
            if len(u2_hist) >= AW.MIN_WINDOWS:
                w = np.array([AW.EWMA_LAM ** k for k in range(len(u2_hist))][::-1])
                m_raw = float(np.clip(np.sqrt(np.sum(w * np.array(u2_hist)) / np.sum(w)),
                                      *AW.CLIP))
                mult = AW.gentle(m_raw)
            else:
                mult = 1.0
            drift = float(carry_log_h(prof, df["Date"].iloc[o], 0.0, AW.H))
            y = close[o + AW.H]
            u = (np.log(y / close[o]) - drift) / sig
            spot = close[o]
            samp_b = simulate_terminal_v3(spot, sig, drift, nu=nu,
                                          n_paths=N_PATHS, seed=SEED)
            samp_o = simulate_terminal_v3(spot, sig * mult, drift, nu=nu,
                                          n_paths=N_PATHS, seed=SEED)
            q_b = np.percentile(samp_b, [5, 95])
            q_o = np.percentile(samp_o, [5, 95])
            rows.append(dict(
                u=float(u), mult=float(mult), gated=len(u2_hist) >= AW.MIN_WINDOWS,
                crps_b=float(crps_sample(samp_b, y) / spot),
                crps_o=float(crps_sample(samp_o, y) / spot),
                in90_b=bool(q_b[0] <= y <= q_b[1]),
                in90_o=bool(q_o[0] <= y <= q_o[1]),
            ))
            u2_hist.append(u * u)
        o += AW.H
    return dict(name=name, rows=rows)


def market_gate(mkt, results):
    per, pooled_b, pooled_o = [], [], []
    allc_b, allc_o = [], []
    cov_b, cov_o = [], []
    for r in results:
        if "error" in r or not r["rows"]:
            continue
        rr = pd.DataFrame(r["rows"])
        std_b = float(rr["u"].std(ddof=0))
        std_o = float((rr["u"] / rr["mult"]).std(ddof=0))
        n_gated = int(rr["gated"].sum())
        per.append(dict(name=r["name"], windows=len(rr), gated_windows=n_gated,
                        std_u_base=round(std_b, 3), std_u_overlay=round(std_o, 3),
                        closer=abs(std_o - 1) < abs(std_b - 1),
                        moved=bool((rr["mult"] != 1.0).any()),
                        final_mult=round(float(rr["mult"].iloc[-1]), 3)))
        pooled_b += list(rr["u"])
        pooled_o += list(rr["u"] / rr["mult"])
        allc_b += list(rr["crps_b"])
        allc_o += list(rr["crps_o"])
        cov_b += list(rr["in90_b"])
        cov_o += list(rr["in90_o"])
    pb = abs(float(np.std(pooled_b)) - 1)
    po = abs(float(np.std(pooled_o)) - 1)
    moved = [p for p in per if p["moved"]]
    closer = sum(p["closer"] for p in moved)
    cb, co = np.array(allc_o), np.array(allc_b)          # skill of overlay vs baseline
    cis = {b: verdict_ci(cb, co, b) for b in (2, 3, 4)}
    crps_worse_robust = all(ci[2] == "FAIL" for ci in cis.values())
    g = dict(
        market=mkt, names=len(per),
        names_that_moved=len(moved), moved_closer=closer,
        pooled_abs_stdu_base=round(pb, 4), pooled_abs_stdu_overlay=round(po, 4),
        cov90_base=round(float(np.mean(cov_b)), 4),
        cov90_overlay=round(float(np.mean(cov_o)), 4),
        crps_parity_ci={b: [round(float(c[0]), 4), round(float(c[1]), 4), c[2]]
                        for b, c in cis.items()},
        gate=dict(
            crps_parity=not crps_worse_robust,
            stdu_improves=po < pb,
            breadth=(closer > len(moved) / 2) if moved else False,
            cov90_in_band=0.85 <= float(np.mean(cov_o)) <= 0.95,
        ),
    )
    g["PASS"] = all(g["gate"].values())
    return g, per


if __name__ == "__main__":
    cfg = json.load(open(f"{ENGINE}/fitted_configs.json"))
    out = {}
    for mkt in ("AE", "SA"):
        names = cfg[mkt]["panel_names"]
        with Pool(6) as p:
            results = p.map(walk, [(mkt, n) for n in names])
        gate, per = market_gate(mkt, results)
        out[mkt] = dict(gate=gate, per_name=per)
        print(json.dumps(gate, indent=1))
        for q in per:
            print(f"  {q['name']:12s} w={q['windows']:>3} gated={q['gated_windows']:>3} "
                  f"std_u {q['std_u_base']:.3f}->{q['std_u_overlay']:.3f} "
                  f"{'closer' if q['closer'] else ('  --  ' if not q['moved'] else 'FARTHER')} "
                  f"final_mult={q['final_mult']}")
    json.dump(out, open(f"{HERE}/RESULTS_24-08-2026.json", "w"), indent=1)
    print("\nwritten:", f"{HERE}/RESULTS_24-08-2026.json")
