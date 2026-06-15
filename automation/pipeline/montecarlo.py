"""10-factor Monte Carlo for the Testahil studies.
5 continuous factors compound daily; 5 discrete events jump once on a random
session in the window. Idiosyncratic noise tops paths up to realized vol.
Deterministic: seed is fixed so every run reproduces the published numbers."""
import numpy as np

TRADING_DAYS_3M = 60  # calibration window for the 3M drift/vol figures


def run(cfg):
    mc = cfg["montecarlo"]
    anchor = cfg["market"]["anchor"]
    rng = np.random.default_rng(mc["seed"])
    n, max_h = mc["paths"], max(mc["horizons_days"])

    # --- continuous factors: daily GBM-style log returns, summed across factors
    daily_drift = np.zeros(max_h)
    daily_var = np.zeros(max_h)
    for f in mc["continuous"]:
        daily_drift += f["drift"] / TRADING_DAYS_3M
        daily_var += (f["vol"] ** 2) / TRADING_DAYS_3M
    cont = rng.normal(daily_drift, np.sqrt(daily_var), size=(n, max_h))

    # --- idiosyncratic noise to reach realized vol
    target_daily_vol = mc["realized_vol_annual"] / np.sqrt(252)
    resid = max(target_daily_vol ** 2 - daily_var.mean(), 0)
    cont += rng.normal(0, np.sqrt(resid), size=(n, max_h))

    log_paths = np.cumsum(cont, axis=1)

    # --- discrete events: each fires with prob p, on a uniform-random day
    for e in mc["events"]:
        fires = rng.random(n) < e["prob"]
        day = rng.integers(0, max_h, size=n)
        impact = rng.normal(e["impact"], e["spread"], size=n) * fires
        # add the (one-off, permanent) jump from its event day onward
        idx = np.arange(max_h)[None, :] >= day[:, None]
        log_paths += idx * impact[:, None]

    prices = anchor * np.exp(log_paths)

    pct = [5, 25, 50, 75, 95]
    out = {"percentiles": {}, "touch": {}}
    for h in mc["horizons_days"]:
        col = prices[:, h - 1]
        out["percentiles"][h] = {p: round(float(np.percentile(col, p)), 2) for p in pct}
    # touch = path ever reaches level within horizon
    for h in mc["horizons_days"]:
        window = prices[:, :h]
        peak = window.max(axis=1)
        out["touch"][h] = {lvl: round(float((peak >= lvl).mean()), 2)
                           for lvl in cfg["touch_levels"]}
    return out


if __name__ == "__main__":
    import sys, yaml, json
    cfg = yaml.safe_load(open(sys.argv[1]))
    print(json.dumps(run(cfg), indent=2))
