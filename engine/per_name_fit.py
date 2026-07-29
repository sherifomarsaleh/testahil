"""
per_name_fit.py — per-name selection between an OLD and a NEW (nu, width_cal).

Standing instruction (Sherif, 29-Jul-2026): "if we use more data and it yields
better results then great, adopt it and change the rating... but if it gives
us worse results then no, do not adopt it and consequently do not change the
rating to the worse." Applied at the correct granularity: PER NAME, not per
market. A market's shared (nu, width_cal) cannot literally be two numbers at
once, so where a proposed re-fit helps some names and hurts others, each name
independently keeps whichever config does not make ITS OWN rating worse.

Uses panel_refresh.fast_rescore -- EXACT, not an approximation (verified
bit-for-bit against backtest_v3) -- so both configs are scored on the SAME
already-built panel residuals. No new simulation, no re-fit; a pure per-name
comparison of two candidate configs.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from panel_refresh import fast_rescore, robust_verdict, panel_path


def score_name(market, name, nu, cal, tag="3m"):
    path = panel_path(market, name, tag)
    r = pd.read_csv(path)
    crps = fast_rescore(r, nu, cal)
    crps_b = r["crps_b"].values
    spot = r["spot"].values
    crps_n, crps_b_n = crps / spot, crps_b / spot
    skill = 1 - crps_n.sum() / crps_b_n.sum()
    verdict, detail = robust_verdict(crps_n, crps_b_n)
    width = (2 * 1.645 * cal * (r["sigma_h"].values / spot)).mean() if "sigma_h" in r else np.nan
    return dict(skill=skill, verdict=verdict, width_proxy=width, n=len(r))


def decide(market, name, old, new, tag="3m"):
    """Returns 'NEW' or 'OLD' for this name, plus both sides' evidence.
    Rule: adopt NEW only if its own robust verdict does not read as a
    regression against OLD's. A verdict ranks PASS > PARITY > BOUNDARY > FAIL
    > PROVISIONAL for this comparison only (PROVISIONAL never blocks, since
    the robust bar was never meetable for it either way)."""
    rank = {"PASS": 3, "PARITY": 2, "BOUNDARY(PARITY-flagged)": 1, "FAIL": 0,
            "PROVISIONAL(insufficient-windows)": 2}
    so = score_name(market, name, *old, tag=tag)
    sn = score_name(market, name, *new, tag=tag)
    ro, rn = rank.get(so["verdict"], 2), rank.get(sn["verdict"], 2)
    chosen = "NEW" if rn >= ro else "OLD"
    return dict(name=name, chosen=chosen, old=so, new=sn)


if __name__ == "__main__":
    MARKETS = {
        # market: ((old_nu, old_cal), (new_nu, new_cal), [names])
        "IN": ((250.0, 0.986), (6.0, 1.021), ["INFY", "RELIANCE", "TMPV"]),
        "KR": ((10.0, 1.063), (8.0, 1.07), ["KAKAO", "LGES", "SAMSUNG"]),
        "QA": ((10.0, 0.937), (6.0, 0.951), ["QGTS", "IQCD", "QNB"]),
        "US": ((250.0, 1.077), (12.0, 1.084), ["AAPL", "NVDA", "TSLA"]),
    }
    overrides = {}
    for mkt, (old, new, names) in MARKETS.items():
        print(f"\n=== {mkt}  OLD={old}  NEW={new} ===")
        overrides[mkt] = {}
        for name in names:
            try:
                d = decide(mkt, name, old, new)
            except FileNotFoundError as e:
                print(f"  {name}: no panel file ({e}) -- skipping, defaults to OLD")
                continue
            print(f"  {name:10s} OLD verdict={d['old']['verdict']:28s} skill={d['old']['skill']:+.4f}  "
                  f"NEW verdict={d['new']['verdict']:28s} skill={d['new']['skill']:+.4f}  -> {d['chosen']}")
            if d["chosen"] == "NEW":
                overrides[mkt][name] = dict(nu=new[0], width_cal=new[1],
                                             reason=f"old={d['old']['verdict']} -> new={d['new']['verdict']}, "
                                                    f"not a regression, adopted 29-Jul-2026")
    with open("fit_overrides.json", "w") as f:
        json.dump(overrides, f, indent=1)
    print("\nwrote fit_overrides.json")
    for mkt, d in overrides.items():
        print(f"  {mkt}: {len(d)} name(s) on NEW -> {sorted(d.keys())}")
