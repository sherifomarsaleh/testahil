"""PHDC peer frame — the Egyptian listed developers, studied on sourced data.

The SIGCM competitors clause asks that peers be studied for operating KPIs and
valuation multiples, as a CROSS-CHECK only — never as a source for the subject's
own historicals. What is sourceable here, and what is not, is stated rather than
papered over:

  SOURCED (tier B, this repository's own price libraries and index):
    market risk — own-stock beta against EGX30 through the same sanctioned
    module PHDC's beta comes from, realised volatility, five-year return,
    maximum drawdown. Every peer runs through the identical procedure, so the
    comparison is like-for-like by construction.

  NOT SOURCED, and therefore ABSENT:
    per-peer earnings and book multiples. No peer publishes a machine-readable
    filing this study can reach, and the aggregator pages carry no financial
    tables. Inventing a P/E to fill the column would be exactly the substitution
    SIGCM forbids, so the column does not exist.
"""
import json, os, sys, math

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, ENGINE)

import numpy as np
import pandas as pd
import beta_regression as BR
from primitives import load_ohlc
from data_quality import clean_ohlc

PEERS = [
    ("PHDC", "Palm Hills Developments"),
    ("TMGH", "Talaat Moustafa Group Holding"),
    ("ORHD", "Orascom Development Egypt"),
    ("EMFD", "Emaar Misr for Development"),
    ("OCDI", "Sixth of October Development & Investment (SODIC)"),
    ("HELI", "Heliopolis Housing and Development"),
    ("PRDC", "Pioneers Properties for Urban Development"),
]


def stats(ticker):
    """Every peer through the SAME Step 0.0 data-quality gate as the subject.

    A peer frame assembled on uncleaned series is not a comparison: the EG
    libraries carry real unadjusted corporate actions (OCDI's 14-Aug-2025 action
    showed as a fake -73% crash and was inside a production fit), and one
    uncleaned peer would dominate every volatility and drawdown column.
    """
    path = os.path.join(ENGINE, "raw_ohlc", "EG", ticker + ".csv")
    df, _dq = clean_ohlc(load_ohlc(path), ticker, verbose=False, market="EG")
    df = df.set_index("Date")
    px = df["Price"].dropna()
    last5 = px[px.index >= px.index.max() - pd.Timedelta(days=365 * 5)]
    r5 = np.log(last5).diff().dropna()
    dd = (last5 / last5.cummax() - 1.0).min()
    return {
        "obs": int(len(px)),
        "first": str(px.index.min().date()),
        "last": str(px.index.max().date()),
        "ann_vol_5y": float(r5.std() * math.sqrt(252)),
        "return_5y": float(last5.iloc[-1] / last5.iloc[0] - 1.0),
        "max_drawdown_5y": float(dd),
        "last_close": float(px.iloc[-1]),
    }


def build():
    out = []
    for tk, name in PEERS:
        row = {"ticker": tk, "name": name}
        try:
            row.update(stats(tk))
        except Exception as e:
            row["price_error"] = "%s: %s" % (type(e).__name__, e)
        try:
            b = BR.own_stock_beta(tk, "EG", "EGX")
            row.update({"beta": b["beta"], "r2": b["r2"], "se": b["se"],
                        "n_weekly": b["n"], "usable": b["usable"],
                        "index_file": b["index_file"], "index_asof": b["index_asof"]})
        except Exception as e:
            row["beta_error"] = "%s: %s" % (type(e).__name__, e)
        out.append(row)
    return out


if __name__ == "__main__":
    rows = build()
    json.dump(rows, open(os.path.join(HERE, "peers.json"), "w"), indent=1, default=str)
    print("EGYPTIAN LISTED DEVELOPERS — market-risk frame")
    print("all betas from beta_regression.own_stock_beta() vs EGX30, identical procedure\n")
    print("%-6s %-34s %7s %6s %6s %8s %9s %9s" %
          ("ticker", "name", "beta", "R2", "SE", "vol 5y", "ret 5y", "max DD"))
    for r in rows:
        if "beta" not in r:
            print("%-6s %-34s   %s" % (r["ticker"], r["name"][:34],
                                       r.get("beta_error", "")[:40]))
            continue
        print("%-6s %-34s %7.4f %5.1f%% %6.3f %7.1f%% %8.1f%% %8.1f%%" %
              (r["ticker"], r["name"][:34], r["beta"], r["r2"] * 100, r["se"],
               r["ann_vol_5y"] * 100, r["return_5y"] * 100, r["max_drawdown_5y"] * 100))
