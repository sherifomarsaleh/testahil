#!/usr/bin/env python3
"""A study far from the price is a FAIL and does not publish.  [R-GAP-02]

WHY THIS EXISTS, IN THE PRINCIPAL'S OWN WORDS
    "A DIFFERENCE OF 30% LET ALONE 70% FROM THE ACTUAL PRICE IS A FAIL AND THE STUDY
    SHOULD NOT BE PUBLISHED UNTIL IT IS SORTED" (3 September 2026), following
    "DO NOT ISSUE A STUDY THAT DOES NOT SATISFY THE CRITERIA WE SET EARLIER".

WHAT CHANGED, AND IT IS A REAL CHANGE
    [R-GAP-01] audits a large gap and says so explicitly: it "does NOT say the answer
    must change — a genuine 39% discount is a legitimate conclusion". That remains true
    of the AUDIT. It is no longer true of PUBLICATION. A study may reach a large-gap
    conclusion, record it, and be held; what it may not do is reach the live site while
    it disagrees with the market by a third.

    The tension is stated rather than smoothed over, because somebody will read both
    rules together: [R-GAP-01] governs whether the answer was AUDITED, this governs
    whether it is ISSUED. An audited answer that still sits 88% from the price has been
    audited and is still not fit to publish. The five-name programme is the evidence —
    every gate passed on EGCH and ARCC, both reviews are thorough and honest, and both
    answers are ones this house would not defend in front of the person who owns them.

THE THRESHOLD IS THE INSTRUCTION'S AND IS NOT DRESSED UP AS A DERIVATION
    Thirty per cent, either side, on the LATEST KNOWN price — the same price
    [R-GAP-01] reads, so the two rules cannot disagree about what the gap is.
    Inventing a justification for a number somebody chose is the free-parameter
    offence in better clothes. What is defensible is the SHAPE: the audit trigger sits
    at 10% because a review is cheap, and the publication block sits higher because
    holding a study has a real cost and the band has to leave room for a genuine
    disagreement that survived its audit.

TWO-SIDED ANSWERS ARE HELD ON THEIR NEAREST BRANCH
    A study publishing two branches is blocked if EVERY branch breaches — its nearest
    reading is still too far. One branch inside the band is a study whose answer
    depends on a decision, which is a legitimate thing to publish.

WHAT IT DOES NOT DO
    It does not touch the studies, move a number, or decide how a gap gets closed. It
    refuses to let one out of the door, and names what is holding it.

USAGE
    python3 scripts/check_publish_block.py              # report every study
    python3 scripts/check_publish_block.py --ticker TK  # exit 1 if TK may not publish
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import check_valuation_gap as gap          # one reader, never a second copy [R-ENF-03]

BLOCK_AT = 0.10        # the instruction's number
BLOCK_BELOW_ONLY = True
# ONE-SIDED ON PURPOSE, per instruction 3 September 2026: "If fair value is above
# the current price then OK. Hold and challenge if the fair value is ONLY below
# the current price by more than 10%."
#
# THE ASYMMETRY IS EVIDENTIAL, NOT DEFERENTIAL. Errors in a discounted cash flow
# are not symmetric: a stale base year, an over-charged discount rate, a missed
# revenue line, a real-terms terminal decline, an unread filing, a terminal
# charging a capital intensity the company has never operated at — every one of
# them pushes value DOWN. A central far BELOW the price is therefore a
# high-prior-of-defect region and the price is the only instrument in the room
# that measures it. A central ABOVE the price is the ordinary shape of finding
# something cheap, which is what this work is for.
#
# WHAT THIS DOES NOT DO, AND THE COST IS STATED RATHER THAN DISCOVERED LATER:
# an over-optimistic study is no longer HELD. It is still AUDITED — [R-GAP-01]
# stays two-sided, so a central more than 10% above the price still owes its
# eight-heading review before the files are staged, and a study that skips it
# still goes red in CI. The split is deliberate: audit both ways, hold only
# where the errors run. If a study is ever found badly wrong on the high side,
# that is the evidence to revisit this clause, and it is written down here so
# the revisit does not depend on anyone remembering.
                       # TIGHTENED FROM 0.30 TO 0.10 on 3 September 2026, per
                       # instruction: "HOLD every document; blocks anything past
                       # 10% from price". The block now sits ON [R-GAP-01]'s audit
                       # trigger rather than above it, which collapses the two-tier
                       # design deliberately: a gap large enough to be worth
                       # auditing is a gap large enough to hold the study while the
                       # audit is written. The cost is stated rather than
                       # discovered — most of the book is held at this level, and
                       # that is the intended reading of "HOLD every document".

# THE RELEASE, IN THE PRINCIPAL'S OWN WORDS: a study may publish past the limit
# "UNLESS YOU HAVE AN IRREFUTABLE EVIDENCE THAT EVERYONE IN THE MARKET IS
# HALLUCINATING AND THAT YOUR FAIR PRICE IS RIGHT AND ALL OTHER PEOPLE ARE WRONG"
# (3 September 2026).
#
# A GATE WITH NO RELEASE IS A STALL [R-CAL-01], and this one would be the worst
# kind — a rule that can only ever be satisfied by moving the answer toward the
# price, which is the fitting this house forbids everywhere else. The release is
# therefore real, and it is deliberately harder than the thing it releases.
#
# WHAT A DISSENT MUST DO, and none of it is a formality:
#   MECHANISM       — the specific thing the market is getting wrong, named from
#                     the filings. "The market is over-optimistic" is not a
#                     mechanism; "the market is capitalising a plant whose
#                     bank-approved cost and nameplate do not earn their capital,
#                     disclosed at note N" is.
#   REVERSE READ    — what the price must believe under this study's OWN drivers,
#                     solved and stated, so the disagreement is measured rather
#                     than asserted. This is what turns "we disagree" into a
#                     number a reader can check.
#   WHY NOT CREDIBLE— why that belief cannot be held, on evidence outside this
#                     model. A reverse read that lands on a believable number is
#                     evidence AGAINST the dissent and the study is still held.
#   WHAT WE CHECKED — the places the error would be if it were ours, each looked
#                     at and named. A dissent written without looking for our own
#                     defect first is the self-audit that only re-checks the work
#                     it did.
#   FALSIFIER       — what would overturn the dissent. A claim with no falsifier
#                     is a habit [R-LESSON-01], and a habit is not evidence.
#
# It carries DISSENT_AT_GAP so it goes stale the moment the answer or the price
# moves past a point — the [R-GAP-01] lesson that a review of a different answer
# is not a review.
DISSENT_GLOB = "MARKET_DISSENT_*.md"
DISSENT_SECTIONS = ("MECHANISM", "REVERSE READ", "WHY NOT CREDIBLE",
                    "WHAT WE CHECKED", "FALSIFIER")
DISSENT_RX = __import__("re").compile(
    r"DISSENT[ _]AT[ _]GAP\s*[:=]\s*(-?[0-9]+\.?[0-9]*)\s*%", __import__("re").I)
DISSENT_TOL = 3.0      # percentage points; a dissent argued at -31% still stands
                       # at -33%, and does not stand at -55%


def read_dissent(sdir):
    """(filename, covered headings, the gap it was argued at) or (None, [], None)."""
    hits = sorted(glob.glob(os.path.join(sdir, DISSENT_GLOB)))
    if not hits:
        return None, [], None
    raw = open(hits[-1], encoding="utf-8").read()
    up = raw.upper()
    m = DISSENT_RX.search(raw)
    return (os.path.basename(hits[-1]),
            [h for h in DISSENT_SECTIONS if h in up],
            float(m.group(1)) if m else None)


def _gap_rows(sdir, ticker):
    """Every readable (label, value, gap) this study publishes against the live price."""
    px, pxdate, pxsrc = gap.latest_known_price(ticker)
    if not px:
        return None, None, None, []
    central, spot, route = gap.read_answer(sdir)
    rows = []
    if central is not None:
        rows.append(("central", central, central / px - 1.0))
    else:
        for b in gap.read_branches(sdir):
            v = gap._num(b.get("value"))
            if v is not None:
                rows.append((str(b.get("label") or "branch")[:44], v, v / px - 1.0))
    return px, pxdate, pxsrc, rows


def phase1_proven():
    """(proven, why) — has the method itself been shown to work yet?  [R-GAP-02 clause 3]

    THE SECOND CONDITION, per instruction 3 September 2026: "do not issue the reports
    before the deviation is sorted AND phase 1 proof the methods is done." Two gates,
    both binding, and the second one is about the METHOD rather than the name.

    WHY IT IS SEPARATE FROM THE GAP. A study can be brought inside 10% of the price by
    fixing the one defect that name happened to carry, and that says nothing about
    whether the method behind it is sound — it is the difference between a passed exam
    and a marked one. The reassessment's Part E acceptance criteria are the marking, and
    until they are met a study inside the band is a study that has not been contradicted
    yet, which is a weaker claim than it looks.

    THE COST IS STATED RATHER THAN DISCOVERED LATER, and it is large: criterion 3 — the
    valuation calibration's pooled bias interval covering zero — cannot mature before the
    first vintages resolve, so ON ADOPTION THIS HOLDS EVERY STUDY IN THE BOOK, including
    the ones already inside the band. That is the instruction read literally and it is
    not softened here. What it does NOT hold is internal work: rebuilding, auditing,
    re-issuing to the principal and merging to main all continue. This gate governs
    ISSUING A REPORT and publishing to the live site, which is what the instruction names.

    Read from the programme's own acceptance record rather than a second copy of it.
    """
    sys.path.insert(0, os.path.join(ROOT, "engine", "method_reassessment"))
    try:
        import progress
        items = progress.acceptance()
    except Exception as e:
        # AN UNREADABLE ACCEPTANCE RECORD IS NOT A PASSED ONE [R-ENF-04]. If the
        # programme's own record cannot be read, nothing is proven and nothing issues.
        return False, "the Phase 1 acceptance record could not be read (%s)" % e
    open_items = [i for i in items if i.get("state") != "MET"]
    if not open_items:
        return True, "Phase 1 acceptance met on all %d criteria" % len(items)
    return False, ("Phase 1 is not proven — %d of %d acceptance criteria open (%s)"
                   % (len(open_items), len(items),
                      "; ".join("#%s %s" % (i["n"], i["text"][:44]) for i in open_items)))


# THIS RULE'S POPULATION IS STUDIES, AND A METAL IS NOT ONE — NAMED, NOT SKIPPED.
#
# [R-GAP-02] holds a STUDY whose fair value sits more than 10% below the price, and
# clause three holds every study until the fundamental method is proven. Both halves
# are statements about the fundamental valuation method: the deviation test compares a
# DCF central against a quote, and the acceptance criteria clause three waits on are
# the valuation calibration's pooled bias and the median |central/price - 1| of that
# same method. The gate's own book-wide population says so in one line — it globs
# engine/*_study and there has never been a metal in it.
#
# A metal has no study by construction and that is not an oversight anywhere: the
# campaign prompt excludes metals "by construction (no issuer, no statements, no
# drivers)", and there is no issuer to file, no statement to foot and no driver to
# build, so there is no discounted cash flow for the method under test to have been
# wrong about. What a metals page publishes is a price cone, a graded ledger row and a
# technical read — governed by [R-CAL-01..03] and [R-TCAL-01], each with its own
# calibration and its own evidence, none of which is the method clause three awaits.
#
# WHAT MADE THIS LOOK LIKE A HOLD RATHER THAN A NON-MEMBERSHIP is the --ticker path.
# Run book-wide the gate takes its population from the study directories and a metal
# never appears; --ticker FORCES a name into that population, and a name outside it
# resolved to "no study directory on disk" — the same sentence an equity that lost its
# study produces. Two different states wearing one message, which is the shape
# [R-ENF-04] names: an absent answer in the costume of a measured one.
#
# THE EXCLUSION IS A CLOSED LIST RESOLVED FROM THE SITE ITSELF, NEVER A RULE OF THUMB.
# "Any name with no study directory is out of scope" would make DELETING a directory
# the cheapest way past this gate, which is precisely what the unreadable branch below
# exists to stop. So membership is read from the METALS object in assets/data.js — the
# keys that are not in TICKERS and carry no study — and an equity with no study
# directory still FAILS as unreadable, unchanged.
def _metal_keys():
    """The registered METALS keys, read from the site rather than typed here.

    Read live for the reason every population in this repo is read live: a typed list
    goes stale the moment a metal is added or removed, and it would go stale silently
    and in the PERMISSIVE direction. If the object cannot be read, NOTHING is excluded
    — an unreadable roster excludes nobody, so the failure falls to the strict side.
    """
    try:
        sys.path.insert(0, os.path.join(ROOT, "engine"))
        import site_data
        return {k.upper() for k in site_data.read_object(
            "METALS", os.path.join(ROOT, "assets", "data.js"))}
    except Exception:
        return set()


def verdict(ticker):
    """(may_publish, reason, rows). An UNREADABLE study may not publish either.

    [R-ENF-04]: a study whose answer this gate cannot read is not a study that
    passed — it is one that was never examined, and letting it through would make
    "unreadable" the cheapest way past the block.
    """
    sdir = os.path.join(ENGINE, "%s_study" % ticker.lower())
    if not os.path.isdir(sdir):
        if ticker.upper() in _metal_keys():
            return True, ("outside this rule's population — a metal publishes no "
                          "fundamental valuation, so there is no central for the "
                          "deviation test and no study for the method hold; its cone "
                          "is governed by [R-CAL-01..03] and its read by "
                          "[R-TCAL-01]"), []
        return False, "no study directory on disk", []
    px, pxdate, pxsrc, rows = _gap_rows(sdir, ticker)
    if px is None:
        return False, "no latest known price — the gap cannot be measured", []
    if not rows:
        return False, "no readable answer to compare against the price", []
    # THE NEAREST READING DECIDES, and "nearest" means nearest to the price from
    # the side that is blocked. A two-sided study with one branch at or above the
    # price is a study whose answer depends on a decision, not one that is too
    # low: it publishes both branches and the reader sees the decision.
    # BOTH CONDITIONS BIND, AND THE METHOD ONE IS CHECKED FIRST because it is the
    # same answer for every name: a book-wide hold is reported once as a book-wide
    # hold rather than as ninety separate coincidences.
    proven, why_p = phase1_proven()
    nearest = max(rows, key=lambda r: r[2]) if BLOCK_BELOW_ONLY else min(
        rows, key=lambda r: abs(r[2]))
    breach = (nearest[2] < -BLOCK_AT) if BLOCK_BELOW_ONLY else abs(nearest[2]) > BLOCK_AT
    if breach:
        if len(rows) > 1:
            why = ("every branch is more than %.0f%% BELOW the price (highest %s at "
                   "%+.1f%%)" % (BLOCK_AT * 100, nearest[0], nearest[2] * 100))
        else:
            why = ("the central is %+.1f%% below the price of %.2f (%s), past the "
                   "%.0f%% publication limit" % (nearest[2] * 100, px, pxdate,
                                                 BLOCK_AT * 100))
        fn, covered, at = read_dissent(sdir)
        if fn is None:
            return False, why + " — and no market dissent is filed", rows
        missing = [h for h in DISSENT_SECTIONS if h not in covered]
        if missing:
            return False, ("%s — %s skips %s, which is not a dissent"
                           % (why, fn, ", ".join(missing))), rows
        if at is None:
            return False, ("%s — %s states no DISSENT_AT_GAP, so nothing says whether "
                           "it argues this gap or an older one" % (why, fn)), rows
        if abs(at - nearest[2] * 100) > DISSENT_TOL:
            return False, ("%s — %s argues a gap of %+.1f%%, and the gap is now %+.1f%%"
                           % (why, fn, at, nearest[2] * 100)), rows
        if not proven:
            return False, ("%s — and %s" % (why_p, fn)), rows
        return True, ("%+.1f%% from the price, released by %s — an evidenced dissent, "
                      "not an assertion" % (nearest[2] * 100, fn)), rows
    if not proven:
        return False, ("inside the band at %+.1f%% of %.2f (%s), but %s"
                       % (nearest[2] * 100, px, pxdate, why_p)), rows
    return True, "%s at %+.1f%% of %.2f (%s)" % (
        nearest[0], nearest[2] * 100, px, pxdate), rows


def main(argv):
    want = None
    if "--ticker" in argv:
        want = argv[argv.index("--ticker") + 1].upper()
    dirs = sorted(glob.glob(os.path.join(ENGINE, "*_study")))
    if not dirs:
        print("FAIL: examined zero study directories [R-ENF-04]")
        return 1
    names = [os.path.basename(d)[:-6].upper() for d in dirs]
    if want:
        names = [want]
    blocked, clean, unread, method = [], [], [], []
    for tk in names:
        ok, why, rows = verdict(tk)
        mark = "PUBLISH" if ok else "HELD   "
        print("%s %-6s %s" % (mark, tk, why))
        for label, v, g in rows:
            print("           %-46s %10.2f  %+7.1f%%" % (label, v, g * 100))
        # THREE STATES, NOT TWO, AND THEY ARE COUNTED SEPARATELY. A study whose
        # answer cannot be read has not passed and has not been measured either;
        # folding it into "blocked" would report a parsing gap as a valuation
        # finding, and folding it into "clean" would make unreadability the
        # cheapest way past this gate [R-ENF-04].
        if ok:
            clean.append(tk)
        elif "Phase 1 is not proven" in why or "acceptance record could not" in why:
            method.append(tk)
        elif "publication limit" in why or "every branch" in why:
            blocked.append(tk)
        else:
            unread.append(tk)
    print("\n%d may publish, %d HELD on the gap (more than %.0f%% BELOW the price), "
          "%d HELD on the method, %d unreadable"
          % (len(clean), len(blocked), BLOCK_AT * 100, len(method), len(unread)))
    if method:
        print("  " + phase1_proven()[1])
    if want:
        return 0 if verdict(want)[0] else 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
