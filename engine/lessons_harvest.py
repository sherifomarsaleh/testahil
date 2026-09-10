"""Harvest candidate lessons from a fundamental walk-forward run.  [R-FCAL-01]

Reads the run's own committed outputs.

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

# A SKIP run scores nothing, and it is still a run. [R-FCAL-01] makes SKIP one of the
# three scopes and calls it a completed queue position, so a SKIP that harvested
# nothing would read as a clean result rather than as the finding it usually is: the
# reason a walk-forward cannot run is almost always a fact about the archive or about
# the study's own panel, and both are worth a lesson.
#
# THREE OF THE FOUR THRESHOLDS BELOW WERE STATED AHEAD OF ANY RUN. PANEL_WEDGE WAS NOT,
# AND SAYING SO IS THE POINT — this comment read "the thresholds below are stated here,
# ahead of any run" until 7 September 2026, which was true of the others and false of
# that one: it was set with ELEC's measured 1.5130 already in view. A comment asserting
# a discipline that was not followed is worse than no comment, because it stops the next
# reader looking.
#
# WHAT IT COSTS, MEASURED RATHER THAN ASSERTED: exactly ONE run in the book computes
# profit_beyond_wedge_by at all, so ANY cutoff between 1.0 and 1.5130 classifies every
# run in the book identically and no cutoff classifies a second run either way. THE
# THRESHOLD DOES NO WORK — which is [R-ANCHOR-01]'s own test of whether a cutoff does
# work or merely exists, applied here and failed. It is left at 1.30 rather than quietly
# re-derived, because inventing a justification for a number somebody chose is the
# free-parameter offence in better clothes, and moving it would change nothing while
# looking like a correction. Registered for a ruling; revisit when a second run measures
# the quantity, which is the first moment the choice can be tested at all.
SKIP_SHORTFALL = 1        # sourceable years at least this far below the LIGHT bar
UNSERVED_ARCHIVE = True   # an issuer that lists statements and serves none of them
PANEL_WEDGE = 1.0         # PANEL_WEDGE_RULED_2026-09-07, by the principal: re-pointed at
                          # the MEASURED consolidation wedge itself rather than a chosen
                          # multiple of it. The wedge is computed from the company's own
                          # overlap year, so "beyond what consolidation explains" is a
                          # measured line; "1.30 times what consolidation explains" was a
                          # number somebody picked, with one run's figure already in view.
                          # Nothing in the book is classified differently by the change —
                          # one run measures the quantity and it reads 1.5130 — which is
                          # the point: the bound now rests on an arithmetic fact rather
                          # than on a choice nobody could test.
KD_BELOW_SOVEREIGN = 1    # trap (i)'s broad denominator landing under the sovereign
                          # in at least this many years

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
    p = os.path.join(run_dir, "skip_record.json")
    out["skip"] = json.load(open(p)) if os.path.exists(p) else None
    if out["scores"] is None and out["skip"] is None:
        raise FileNotFoundError(
            "%s holds no scores.json and no skip_record.json — a walk-forward run "
            "that produced neither a score file nor a recorded reason for not "
            "scoring has nothing to harvest, and an empty harvest must not read as "
            "a clean one" % run_dir)
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
    if d["scores"] is None:
        return harvest_skip(d["skip"], ticker)
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


def harvest_skip(K, ticker):
    """Candidates a SKIP run's OWN measurements support. Rules fixed above.

    A run that scores nothing still measures the archive it could not use and the
    panel it could not reconcile to. Each rule below fires off a committed number,
    never off a reading of the run's prose.
    """
    drafts = []
    src = K.get("sourceable_years", {})
    arch = K.get("issuer_archive", {})
    panel = K.get("study_panel_vs_filed_FY2023", {})
    claim = K.get("claimed_filed_record", {})
    ul = K.get("useful_life", {})

    # S1 — the archive is short, so the method could not be tested here at all
    best = max(src.get("consolidated", 0), src.get("standalone", 0))
    bar = src.get("required_for_light", 5)
    if best <= bar - SKIP_SHORTFALL:
        drafts.append(_draft(
            "skip_insufficient_history", ticker,
            "The forecasting method could not be tested on %s at all." % ticker,
            "A walk-forward needs an origin to project from and a later actual to "
            "score against. Where the archive is too short there is no test to run, "
            "and saying so is the result — not a gap to be filled by stretching the "
            "window.",
            "%d sourceable fiscal years on the best available basis against a bar of "
            "%d, and %d scoreable origins: %s."
            % (best, bar, src.get("scoreable_origins", 0),
               src.get("why_zero_origins", "")),
            "STOCK",
            "A short archive is a fact about one issuer, not about a class or a "
            "method. File narrow and widen only if a second name shows the same "
            "thing for the same reason.",
            "A filing archive that becomes reachable, or filings supplied directly, "
            "taking the sourceable span to five years or more on one basis."))

    # S2 — an issuer that lists what it does not serve
    if UNSERVED_ARCHIVE and arch.get("statement_files_listed", 0) > 0 \
            and arch.get("fetchable_on_live_host", -1) == 0:
        drafts.append(_draft(
            "unserved_archive", ticker,
            "An index of filings is not an archive of filings.",
            "A company can list its statements on its own website and serve none of "
            "them. The list looks like evidence the documents exist and are "
            "obtainable; only fetching each one tells you which. Record the outcome "
            "per file, not per page.",
            "%d statement files listed; %d on the live host and %d of those fetchable; "
            "%d on a host whose DNS does not resolve; the index's last period is %s "
            "while the last statement on the basis the study models is %s."
            % (arch.get("statement_files_listed"), arch.get("on_live_host"),
               arch.get("fetchable_on_live_host"), arch.get("on_dead_host"),
               arch.get("index_last_period"),
               arch.get("last_consolidated_statement_issued")),
            "ALL",
            "This is about how a source is checked rather than about any company: "
            "the same wrong inference — a listing read as an obtainable document — is "
            "available on every name in the book.",
            "An index whose listings are shown to be reliably fetchable, making the "
            "per-file probe redundant."))

    # S3 — the study's own panel does not reconcile to the filings
    if panel.get("profit_beyond_wedge_by", 1.0) >= PANEL_WEDGE:
        drafts.append(_draft(
            "panel_unreconciled", ticker,
            "A study's historicals can be unverifiable and still pass every gate.",
            "Where a company stops publishing on the basis a study models, the "
            "study's history quietly becomes a vendor's account of it. Every "
            "arithmetic check still passes, because the numbers are internally "
            "consistent — they are simply nobody's filed numbers. The test is to "
            "measure the study's panel against the filings that DO exist and against "
            "the wedge between the two bases, rather than to assume the difference is "
            "the consolidation.",
            "At the one year existing on both bases the group is %.2fx the parent on "
            "revenue and %.2fx on net profit. The study's FY2023 revenue is %.2fx the "
            "parent — consistent with a consolidated figure — while its net profit is "
            "%.2fx, %.2f times beyond what the measured wedge delivers."
            % (K["consolidation_wedge_at_overlap"]["revenue"],
               K["consolidation_wedge_at_overlap"]["net_profit"],
               panel.get("revenue"), panel.get("net_profit"),
               panel.get("profit_beyond_wedge_by")),
            "ALL",
            "The failure is in how a panel is checked, not in what industry it "
            "belongs to. Any issuer can change reporting basis or stop publishing.",
            "A study whose vendor panel is later reconciled line by line to filings "
            "on the same basis, showing the check adds nothing."))

    # S4 — a "filed record" that was not filed
    if claim.get("premise_withdrawn"):
        lo, hi = claim.get("true_filed_range_standalone", [0, 0])
        clo, chi = claim.get("claimed_range", [0, 0])
        drafts.append(_draft(
            "filed_record_that_was_not_filed", ticker,
            "Check that a \"filed record\" was filed before reasoning from it.",
            "A review can reach the right conclusion about a study and still take its "
            "benchmark from the study's own inputs. Calling a number the company's "
            "own record makes it read as external evidence when it is the thing under "
            "test, and the argument then runs in a circle nobody can see.",
            "A review described a terminal-margin range of %.2f%%-%.2f%% as the "
            "company's own filed record; it is the study's committed hist_is, and two "
            "of its three years have no filing at all. The filed range on the basis "
            "that can be checked is %.2f%%-%.2f%%, which puts the forecast of %.2f%% "
            "INSIDE it rather than at half the lowest filed year, and puts the price's "
            "reverse read at %.1f times the highest filed margin."
            % (100 * clo, 100 * chi, 100 * lo, 100 * hi,
               100 * claim.get("study_terminal_forecast", 0),
               claim.get("reverse_read_over_highest_filed", 0)),
            "ALL",
            "It is a rule about where a benchmark comes from, and it binds on every "
            "review this house writes.",
            "A house convention that tags every committed historical with whether it "
            "came from a filing, making the confusion impossible to make."))

    # S5 — the disclosed-life route that keeps failing
    if ul and not ul.get("route_1_succeeded"):
        band = ul.get("route_2_years_band", [0, 0])
        drafts.append(_draft(
            "useful_life_route_one_fails", ticker,
            "The accounting-policies note usually gives a range, not a life.",
            "[R-TERM-01] needs one disclosed useful life and the policy note rarely "
            "supplies one. Reading a span and picking a point inside it is the choice "
            "the rule exists to forbid, so the honest output is the derived identity "
            "and a band.",
            "Route (1) gave %s. Route (2) — depreciable gross cost over "
            "the annual charge — gives %.2f years on the full base and %.2f excluding "
            "the %.1f%% of that base the note itself discloses as fully depreciated "
            "and still in use, with a prior-year control at %.2f."
            % (ul.get("route_1_outcome", ""), band[1], band[0],
               100 * ul.get("fully_depreciated_share_of_base", 0),
               ul.get("route_2_prior_year_control", 0)),
            "ALL",
            "It is about how a disclosure is read and it has now recurred across "
            "several unrelated names and industries.",
            "A run of filings that do disclose a scalar or a dominant class, making "
            "route (1) the normal case rather than the exception."))

    # S6 — trap (i), where the broad denominator is not merely wrong but impossible
    if K.get("trap_i_broad_denominator_below_sovereign_years", 0) >= KD_BELOW_SOVEREIGN:
        t = K.get("trap_i", {})
        yrs = sorted(t)
        drafts.append(_draft(
            "trap_i_below_sovereign", ticker,
            "A borrowing rate below the sovereign is the arithmetic failing, not the "
            "company borrowing cheaply.",
            "Dividing the finance charge by a liabilities total that includes trade "
            "payables, related-party balances, tax and provisions understates the "
            "rate. The useful part is that the error announces itself: a corporate "
            "cannot fund below its own government, so a rate under the sovereign is a "
            "denominator problem and can be caught without knowing the right answer.",
            "On the borrowings that actually bear interest the rate runs %s; on total "
            "liabilities %s — understated by %.2f to %.2f points, and below the "
            "Egyptian sovereign in %d of %d years."
            % (", ".join("%.2f%%" % (100 * t[y]["rate_on_bearing_debt"]) for y in yrs),
               ", ".join("%.2f%%" % (100 * t[y]["rate_on_total_liabilities"]) for y in yrs),
               min(t[y]["understatement_pp"] for y in yrs),
               max(t[y]["understatement_pp"] for y in yrs),
               K.get("trap_i_broad_denominator_below_sovereign_years"), len(yrs)),
            "ALL",
            "[R-COC-01] already refuses a cost of debt below its own sovereign; this "
            "adds that the same test catches the trap-(i) denominator, which is a "
            "method point rather than a company one.",
            "A jurisdiction where a corporate genuinely funds below its sovereign, "
            "which would make the check fire on work that is right."))

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
