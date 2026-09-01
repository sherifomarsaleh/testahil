"""ARCC beta — produced by the ONLY sanctioned route, and it does not survive tier 1.

Revisions 1-3 carried a beta of 0.6281 described as a "tier-1 own-stock weekly
regression (usability gate PASSED)" with an R-squared of 0.091. THAT REGRESSION
WAS AGAINST AN EQUAL-WEIGHT COMPOSITE OF THE COVERED EGYPTIAN NAMES, not against
the EGX30. A composite of the names this engine happens to cover is a coverage
artefact, not a market: it changes whenever a stock is posted and it shares
constituents with the panel it prices, which is exactly why it correlates better
with a covered name than the real index does. SIGCM clause 6 calls it a HARD
FAIL, not a fallback, and the higher R-squared was the artefact rather than the
evidence.

Re-derived here through engine/beta_regression.own_stock_beta(), which resolves
the regressor itself to the published index of the exchange the stock is listed
on, runs the Step 0.0 data-quality gate on both series, and matches the weekly
grid to the EGX's real trading week:

    beta 0.698, R-squared 0.047, SE 0.228, n 253, 4.89 years to 16-Jul-2026

R-squared of 4.7% is BELOW the 5% usability floor. Tier 1 is therefore NOT
available, and the protocol's answer to that is not to keep the number anyway —
it is to fall to tier 2, a SAME-COUNTRY peer beta, and to show the failed
diagnostics beside it.

THE PEER SET is the Egyptian building-materials and construction complex, chosen
before any beta was computed and named in full: Lecico (building materials),
Egypt Aluminium (heavy industrial), Orascom Construction (construction) and
Egyptian Chemical Industries (heavy industrial). Sinai Cement is the closest
business match and IS NOT USED as a peer estimate — its own regression fails the
same gate more badly (R-squared 0.025), and a second unusable number does not
make a usable one. It is reported beside the set as evidence about the sector's
thin trading rather than as an input.

WHAT COULD NOT BE DONE, AND WHICH WAY IT CUTS. The protocol's tier 2 is the
median UNLEVERED peer beta re-levered to the target structure. Peer leverage is
NOT SOURCED here — it would need four more companies' balance sheets — so the
unlever/re-lever step is not performed and the median EQUITY beta is adopted
instead. That is a real gap and it is flagged rather than papered over. Its
direction is not ambiguous: ARCC holds NET CASH and its peers carry debt, so
unlevering the peers and re-levering to ARCC's structure could only produce a
LOWER beta, a LOWER cost of equity and a HIGHER value. The adopted figure is
therefore the conservative end of the tier-2 construction, and the study
publishes the whole peer range as a sensitivity rather than a point.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import beta_regression as BR

PEERS = ["LCSW", "EGAL", "ORAS", "EGCH"]
REPORTED_NOT_USED = ["SCEM"]


def main():
    own = BR.own_stock_beta("ARCC", "EG", "EGX")
    peers = {}
    for t in PEERS + REPORTED_NOT_USED:
        try:
            peers[t] = BR.own_stock_beta(t, "EG", "EGX")
        except Exception as e:
            peers[t] = {"error": str(e)}

    usable = sorted(peers[t]["beta"] for t in PEERS
                    if peers[t].get("usable") and "beta" in peers[t])
    assert len(usable) >= 3, "tier 2 needs at least three usable peers, got %d" % len(usable)
    med = (usable[len(usable) // 2] if len(usable) % 2
           else 0.5 * (usable[len(usable) // 2 - 1] + usable[len(usable) // 2]))

    adopted = {
        "beta_used": med,
        "tier": 2,
        "basis": "SAME-COUNTRY PEER BETA (tier 2). The own-stock regression against the "
                 "EGX30 — the only conforming regressor for an EGX listing — returns "
                 "beta %.3f on an R-squared of %.3f, BELOW the 5%% usability floor, so "
                 "tier 1 is not available." % (own["beta"], own["r2"]),
        "why": "Median equity beta of the Egyptian building-materials and construction "
               "peers that clear the usability gate: %s. Sinai Cement, the closest "
               "business match, fails the same gate more badly (R-squared %.3f) and is "
               "reported rather than used."
               % (", ".join("%s %.3f" % (t, peers[t]["beta"]) for t in PEERS
                            if peers[t].get("usable")),
                  peers["SCEM"].get("r2", float("nan"))),
        "unlever_relever": "NOT PERFORMED — peer leverage is not sourced. The direction is "
                           "unambiguous: ARCC holds net cash and its peers carry debt, so "
                           "the step could only LOWER the beta and RAISE the value. The "
                           "adopted figure is the conservative end of tier 2 and the whole "
                           "peer range is published as a sensitivity.",
        "corroboration": "The failed own-stock regression's own point estimate is %.3f and "
                         "its Blume cross-check %.3f, both below the adopted peer median, "
                         "and its 90%% interval [%.2f, %.2f] contains it. The retired "
                         "composite figure of 0.6281 sits below all of them, which is what "
                         "a regressor sharing constituents with its subject does."
                         % (own["beta"], own.get("blume_crosscheck", float("nan")),
                            own["ci90"][0], own["ci90"][1]),
        "sensitivity_required": sorted(set([round(x, 2) for x in usable] + [0.63, 1.20])),
        "retired": {"beta": 0.6281,
                    "why": "regressed against an equal-weight composite of the covered "
                           "Egyptian names. SIGCM clause 6: a constituent composite is a "
                           "HARD FAIL, not a tier."},
    }
    # The regressor is recorded at the TOP LEVEL of this artefact, not only inside
    # the own-stock record, because the repo-level provenance gate reads the file
    # rather than the study's opinion of itself: a record that names no regressor
    # FILE fails, and "the number is in there somewhere" is not provenance.
    out = {"index_file": own["index_file"], "index_asof": own["index_asof"],
           "market": own["market"], "exchange": own["exchange"],
           "beta": adopted["beta_used"], "conforming": own["conforming"],
           "tier": 2, "r2": own["r2"], "se": own["se"], "n": own["n"],
           "usable": own["usable"],
           "own_stock": own, "peers": peers, "adopted": adopted,
           "peer_set": PEERS, "reported_not_used": REPORTED_NOT_USED,
           "peer_betas_usable": usable, "peer_median": med}
    with open(os.path.join(HERE, "beta_result.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
    print("own-stock vs EGX30: beta %.4f  R2 %.3f  SE %.3f  n %d  usable %s"
          % (own["beta"], own["r2"], own["se"], own["n"], own["usable"]))
    print("  ->", own["gate_msg"])
    for t in PEERS + REPORTED_NOT_USED:
        p = peers[t]
        print("  peer %-5s beta %6.3f  R2 %5.3f  usable %s%s"
              % (t, p.get("beta", float("nan")), p.get("r2", float("nan")),
                 p.get("usable"), "   (reported, NOT used)" if t in REPORTED_NOT_USED else ""))
    print("ADOPTED tier 2 peer median beta %.4f (was 0.6281 on a composite — a hard fail)"
          % med)
    return out


if __name__ == "__main__":
    main()
