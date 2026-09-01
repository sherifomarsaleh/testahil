"""EGCH beta — the sanctioned route, replacing this study's composite regression.

WHAT THIS REPLACES AND WHY IT MATTERS. The 08-08-2026 edition regressed EGCH's weekly
returns against a 35-name EQUAL-WEIGHT COMPOSITE of the Egyptian names this engine
happens to cover and recorded beta 1.0527 with `usable: true`. That is a hard SIGCM
clause-6 failure: a composite of covered names is a coverage artefact, not a market. The
rule against it was already written down while the study did it anyway, which is why the
check now runs from outside the study (scripts/check_study_provenance.py).

Nothing here hand-rolls a regression. `beta_regression.own_stock_beta()` resolves the
regressor itself — the PUBLISHED index of the exchange the stock is listed on (EGX30,
engine/raw_indices/EG/EGX30.csv) — runs Step 0.0 on both series, matches the weekly grid
to the EGX's real trading week, and returns provenance with the number.
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import beta_regression
import research_protocol as rp

SUPERSEDED = {"beta": 1.0526645903529388, "r2": 0.2830573279012374, "n": 257,
              "se": 0.10491194482570484, "regressor": "35-name equal-weight EGX composite",
              "why_withdrawn": ("A constituent composite is a coverage artefact, not a market. "
                                "SIGCM clause 6 hard fail; never a fallback and never a tier.")}


def main():
    rec = beta_regression.own_stock_beta("EGCH", "EG", "EGX")
    rp.assert_beta_provenance(rec)
    rec["superseded_composite"] = SUPERSEDED
    rec["standard_version"] = rp.STANDARD_VERSION
    with open(os.path.join(HERE, "beta_result.json"), "w") as f:
        json.dump(rec, f, indent=1, default=str)
    print("EGCH beta %.4f vs %s (as of %s)" % (rec["beta"], rec["index_file"], rec["index_asof"]))
    print("  R2 %.4f  n=%d  SE %.4f  usable=%s  conforming=%s"
          % (rec["r2"], rec["n"], rec["se"], rec["usable"], rec["conforming"]))
    print("  superseded composite %.4f -> published index %.4f (%+.1f%%)"
          % (SUPERSEDED["beta"], rec["beta"], 100 * (rec["beta"] / SUPERSEDED["beta"] - 1)))
    return rec


if __name__ == "__main__":
    main()
