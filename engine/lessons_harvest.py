"""Harvest candidate lessons from a walk-forward run's own committed outputs.

WHAT IS AUTOMATED, AND WHAT DELIBERATELY IS NOT.

Automated: finding which of a run's results are worth a lesson, and filling in
the measured evidence from the run's own files. Nothing here is typed by hand,
so a lesson's "what it cost" clause cannot drift from what the run actually
measured. The rules below are fixed in advance, not chosen after seeing the
numbers.

NOT automated, on purpose: THE SCOPE. Deciding whether a finding binds on one
company, on its class, or on every study is a judgement, and the register itself
records that getting it wrong is costly in both directions — too narrow and the
next study repeats the mistake, too broad and one company's quirk becomes a
house rule nobody can dislodge. A machine cannot make that call from a bias
figure. So this module PROPOSES a scope with a stated reason and marks every
draft `confirmed: false`; `lessons_add.py` refuses to append anything still
unconfirmed. The last step is one explicit act by whoever ran the study.

That boundary is the honest one, and it is what makes the loop trustworthy: the
evidence is mechanical, the judgement is signed.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# The thresholds below are stated before any run is read, so they cannot be
# tuned to produce a pleasing number of lessons out of a particular run.
ROBUST_BIAS = 0.20        # a robust bias this large is worth recording
BEATEN_BY_NAIVE = 3       # losing to "no change" at this many horizons matters
COMPANY_NOT_MACRO = 0.10  # macro share below this, with a large error, is us
BIG_MAE = 0.50
ERA_FLIP = True           # a bias that changes sign between eras is not a bias

PRETTY = {
    "is.revenue": "revenue", "is.cogs": "cost of revenue",
    "is.gross_profit": "gross profit", "is.sga": "overheads",
    "is.admin_depr": "depreciation and amortisation",
    "is.finance_cost": "finance cost", "is.npbt": "profit before tax",
    "is.npat_mi": "net profit", "units_sold": "units sold",
    "units_delivered": "units delivered", "asp": "price per unit",
    "new_sales": "new sales",
}


def _name(k):
    return PRETTY.get(k, k.replace("is.", "").replace("_", " "))


def _times(bias):
    """A log bias, said the way a reader would say it."""
    import math
    m = math.exp(abs(bias))
    side = "too high" if bias > 0 else "too low"
    if m >= 1.6:
        return "about %.1f times %s" % (m, side)
    return "about %.0f%% %s" % (100 * (m - 1), side)


def load(run_dir):
    out = {}
    for f in ("scores.json", "diagnostics.json", "corrections_log.json"):
        p = os.path.join(run_dir, f)
        out[f[:-5]] = json.load(open(p)) if os.path.exists(p) else None
    if out["scores"] is None:
        raise FileNotFoundError(
            "%s holds no scores.json — a walk-forward run that produced no "
            "score file has nothing to harvest, and an empty harvest must not "
            "read as a clean one" % run_dir)
    return out


def _draft(key, ticker, headline, plain, evidence, scope, why_scope,
           overturned_by, origin="walk_forward_fundamental"):
    return {"proposed_id": None, "ticker": ticker, "headline": headline,
            "plain": plain, "evidence": evidence, "scope": scope,
            "why_scope": why_scope, "overturned_by": overturned_by,
            "origin": origin, "rule": key, "confirmed": False}


def harvest(run_dir, ticker):
    """Every candidate lesson this run's own numbers support."""
    d = load(run_dir)
    S = d["scores"]
    drafts = []

    by_driver = S.get("by_driver", {})
    by_horizon = S.get("by_horizon", {})
    macro = S.get("macro_split", {})
    eras = S.get("by_era", {})

    # 1 — a robust, material bias in any driver
    for k, r in sorted(by_driver.items()):
        if r.get("robust_sign") and abs(r.get("bias", 0)) >= ROBUST_BIAS:
            drafts.append(_draft(
                "robust_bias", ticker,
                "%s forecasts run %s for %s."
                % (_name(k).capitalize(), _times(r["bias"]), ticker),
                "The method misses this driver in the same direction almost "
                "every time, not at random. That is a fixable defect rather "
                "than noise — find what is wired wrong before adding any "
                "correction factor.",
                "Bias %+.3f log (%s), average miss %.3f, wrong in the same "
                "direction in %.0f%% of cases, and the sign holds across every "
                "bootstrap block tested (n=%d)."
                % (r["bias"], _times(r["bias"]), r["mae"],
                   100 * (r["over"] if r["bias"] > 0 else 1 - r["over"]),
                   r["n"]),
                "UNSCOPED",
                "A robust bias in one driver may be this company's disclosure, "
                "its whole class's economics, or our method. Decide which "
                "before filing.",
                "A later run of the same name where the sign no longer holds "
                "across bootstrap blocks."))

    # 2 — beaten by the naive benchmark at enough horizons to matter
    for k, hs in sorted(by_horizon.items()):
        lost = [h for h, v in hs.items()
                if isinstance(v, dict)
                and v.get("skill_freeze", {}).get("skill", 0) < 0]
        if len(lost) >= BEATEN_BY_NAIVE:
            worst = min((hs[h]["skill_freeze"]["skill"] for h in lost))
            drafts.append(_draft(
                "beaten_by_naive", ticker,
                "The %s forecast loses to assuming no change." % _name(k),
                "At %d of %d horizons, simply carrying last year's number "
                "forward beat the model. A method that cannot beat 'no change' "
                "has not earned the precision it displays, and should be "
                "published as a range or not at all."
                % (len(lost), len(hs)),
                "Negative skill against the freeze benchmark at horizons %s, "
                "worst %.3f." % (", ".join(sorted(lost)), worst),
                "UNSCOPED",
                "Losing to a naive benchmark usually points at the method, "
                "which would make it ALL — but confirm it is not this "
                "company's series being unusually persistent.",
                "A later run where the model beats the freeze benchmark at a "
                "majority of horizons."))

    # 3 — a large error that the currency does not explain
    for k, m in sorted(macro.items()):
        if (m.get("macro_share", 1) <= COMPANY_NOT_MACRO
                and m.get("as_known_mae", 0) >= BIG_MAE):
            drafts.append(_draft(
                "company_not_macro", ticker,
                "The %s error is the company, not the currency." % _name(k),
                "Re-running every forecast with perfect foresight of inflation "
                "barely improves it. So devaluation is not the explanation, "
                "and looking for a macro fix would waste the effort.",
                "Average miss %.3f as known, %.3f with perfect foresight of "
                "inflation — the macro share is only %.1f%%."
                % (m["as_known_mae"], m["perfect_mae"],
                   100 * m["macro_share"]),
                "UNSCOPED",
                "Almost always ALL — 'check whether the macro explains it "
                "before assuming it does' is a method rule — but the specific "
                "finding may be about this market.",
                "A market or period where the same decomposition puts most of "
                "the error on the macro path."))

    # 4 — a bias that changes sign between eras is not a bias
    for k, e in sorted(eras.items()):
        vals = [(nm, v["bias"]) for nm, v in e.items()
                if isinstance(v, dict) and "bias" in v]
        signs = {1 if b > 0 else -1 for _, b in vals}
        if ERA_FLIP and len(vals) >= 2 and len(signs) > 1:
            drafts.append(_draft(
                "era_flip", ticker,
                "The %s bias changes direction between regimes." % _name(k),
                "It runs one way in one period and the other way in the next. "
                "Averaging them produces a correction that is wrong in both. "
                "Record it, do not correct for it.",
                "By era: " + "; ".join("%s %+.3f" % (nm, b) for nm, b in vals)
                + ".",
                "UNSCOPED",
                "A sign that flips with the regime is usually about the market "
                "or the period, not the company — but say which.",
                "A longer record in which one sign dominates across all "
                "regimes."))

    # 5 — a correction that passed its own test and was not promoted
    log = (d["corrections_log"] or {}).get("log", [])
    for entry in log:
        for drv, c in (entry.get("corrections") or {}).items():
            if c.get("applied") and c.get("outcome_mae_change", 0) < 0:
                drafts.append(_draft(
                    "correction_not_promoted", ticker,
                    "A correction to %s worked and must still be checked "
                    "against the rest of the book." % _name(drv),
                    "A fudge factor that improves this one name can be hiding "
                    "a defect in how we set the model up. Before adopting it, "
                    "check it matches how that driver is built everywhere "
                    "else.",
                    "Applied %+.3f at origin %s; average miss changed %+.3f."
                    % (c["applied"], entry.get("origin"),
                       c.get("outcome_mae_change", 0)),
                    "UNSCOPED",
                    "If the correction turns out to be fixing our own "
                    "mis-specification, the lesson is ALL and is about "
                    "specification. If the company is genuinely unusual, it is "
                    "STOCK.",
                    "Evidence that the driver is built the same way across the "
                    "book and this name still needs the correction."))

    # 6 — the guidance record, where one exists
    g = (d["diagnostics"] or {}).get("guidance") or []
    forward = [x for x in g if x.get("kind") == "forward"
               and x.get("log_error") is not None]
    if len(forward) >= 2:
        mean = sum(x["log_error"] for x in forward) / len(forward)
        drafts.append(_draft(
            "guidance_lean", ticker,
            "%s's own forward targets lean %s." % (ticker,
                                                   "high" if mean > 0 else "low"),
            "Management's forward guidance misses in a consistent direction. "
            "A driver that takes guidance as an input inherits that lean "
            "instead of correcting for it, so guidance is graded and never "
            "consumed.",
            "%d forward targets gradable before the outcome, mean log error "
            "%+.3f (%s)." % (len(forward), mean, _times(mean)),
            "UNSCOPED",
            "Guidance behaviour is usually a company habit (STOCK) but the "
            "rule 'score guidance, never consume it' is ALL — file the rule "
            "once and the company's own record separately.",
            "A longer guidance record in which the lean disappears."))

    for i, x in enumerate(drafts, start=1):
        x["proposed_id"] = "DRAFT-%s-%02d" % (ticker.upper(), i)
    return drafts


def main(argv):
    if len(argv) < 2:
        runs = sorted(d for d in os.listdir(HERE) if d.endswith("_walkforward"))
        print("usage: python3 engine/lessons_harvest.py <TICKER> [run_dir]")
        print("walk-forward runs on disk: %s"
              % ", ".join(d[:-len("_walkforward")].upper() for d in runs))
        return 2
    ticker = argv[1].upper()
    run_dir = argv[2] if len(argv) > 2 else os.path.join(
        HERE, "%s_walkforward" % ticker.lower())
    drafts = harvest(run_dir, ticker)
    out = os.path.join(run_dir, "lessons_draft.json")
    json.dump({"ticker": ticker, "run_dir": os.path.relpath(run_dir, HERE),
               "drafts": drafts}, open(out, "w"), indent=1)
    print("%d candidate lesson(s) harvested from %s"
          % (len(drafts), os.path.basename(run_dir)))
    for x in drafts:
        print("\n  %s  [%s]" % (x["proposed_id"], x["rule"]))
        print("    %s" % x["headline"])
        print("    evidence : %s" % x["evidence"])
        print("    scope    : %s — %s" % (x["scope"], x["why_scope"]))
    print("\nwritten to %s" % os.path.relpath(out, os.path.dirname(HERE)))
    print("NEXT: set each draft's scope (ALL / CLASS / STOCK), its subject, and")
    print("      confirmed:true — then run  python3 engine/lessons_add.py %s"
          % ticker)
    print("      Nothing enters the register until the scope is decided; that")
    print("      judgement is not automated and must not be.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
