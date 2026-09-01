"""THE LESSONS REGISTER — what every study taught us, and how far it travels.

[R-LESSON-01] is the standing rule this module implements.

is the standing rule this module implements.

This is the single source of truth. `Lessons_Register.md` is GENERATED from it
and is never hand-edited, so the two cannot drift apart the way this project's
two protocol documents once did.

WHY A SCOPE FIELD IS THE WHOLE POINT. A lesson is useless until you know how
far it carries. Three scopes, and the difference between them is not a matter
of taste:

  STOCK  true of this company and nothing else. A quirk of its disclosure, its
         history, its accounting. Applying it to another name is superstition.

  CLASS  true of every company that works the same way — every off-plan
         developer, every telecom operator. The next study of that class should
         start by reading these; the next study of a DIFFERENT class should not.

  ALL    true of every study we will ever run, because it is about method, or
         arithmetic, or how a document gets checked. These are the expensive
         ones and they are usually learned by getting something wrong.

EVERY LESSON CARRIES WHAT WOULD OVERTURN IT. A lesson with no falsifier is a
habit, not a finding, and habits are how a house method quietly stops being
tested. `overturned_by` is required and may not be empty.

WHAT COUNTS AS A SOURCE. `origin` records HOW the lesson was learned, because
the strength of the evidence differs enormously:

  walk_forward  measured against out-of-sample outcomes across many origins.
                The strongest evidence this project produces.
  critique      found by an external reviewer of a delivered study.
  self_audit    found by re-examining our own build before anyone else read it.
  build         found while building or rendering, usually because a check
                reported clean on something it was not actually looking at.

A walk-forward lesson outranks a self-audit lesson when the two disagree, and
the register says which is which rather than presenting them as equals.
"""

SCOPES = ("STOCK", "CLASS", "ALL")
# TWO DIFFERENT THINGS ARE BOTH CALLED A WALK-FORWARD HERE, and conflating them
# is an error this register made in its first edition. They test different
# machinery, on different evidence, and a lesson from one is not a lesson from
# the other:
#
#   walk_forward_fundamental  the FUNDAMENTAL method — project each driver from
#                             a past origin, score revenue, cost and profit
#                             against what happened, decompose macro from
#                             company, test corrections. One name so far.
#   walk_forward_price        the PRICE ENGINE — strike the Monte Carlo cone at
#                             a past origin and score the outcome against it:
#                             band coverage, the probability-integral transform,
#                             and a proper score against a carry-anchored random
#                             walk. Nineteen names, 317 resolved forecasts.
ORIGINS = ("walk_forward_fundamental", "walk_forward_price", "critique",
           "self_audit", "build")
STATUSES = ("provisional", "adopted", "watch", "outstanding")

# NOTHING IN THIS REGISTER BINDS ANY STUDY. It is a RECORD, not a gate. No
# standing rule refers to it and no QC gate consults it, deliberately: the
# walk-forward method itself has not been validated. As at 31-Aug-2026 exactly
# one company had been through a run, and that run's own training record states
# that its corrections rest on two origins, that the bootstrap intervals are
# wide with several straddling zero, and that the cells are not independent.
#
# The house promotion rule says nothing enters the method — from a human or
# from the pipeline — without surviving the same out-of-sample test the
# forecasts must survive. A finding measured on one name has not survived that
# test, so every lesson learned from a walk-forward run is marked PROVISIONAL
# and stays that way until the method is validated across more names.
#
# Lessons from critiques, self-audits and build failures are a different case:
# each is a defect that was actually found in delivered work, not an inference
# from a fitted record. They are marked adopted. They still bind nothing here —
# the ones that genuinely became house rules live in the standing protocol, and
# reached it through their own route, not through this file.

# Classes are named here once so a typo cannot silently create a new class that
# no study will ever match.
CLASSES = (
    "real-estate developer, off-plan, percentage-of-completion",
    # TMGH is off-plan with a large backlog and long payment plans like the
    # class above, but it recognises revenue when the customer takes control of
    # the home, not as construction progresses. [L-102] makes the recognition
    # basis the class-defining question for developers, so filing a
    # point-in-time issuer's lessons under a class whose name asserts
    # percentage-of-completion would be the superstition this register warns
    # about. The two are kept apart.
    "real-estate developer, off-plan, point-in-time on handover",
    "telecom operator",
    "cement and heavy industrial",
    "petrochemical",
    "airline",
    "bank",
    "holding company",
    "commodity and metals",
)


def L(id, scope, applies_to, headline, plain, source, origin, evidence,
      overturned_by, status=None):
    # A walk-forward finding is PROVISIONAL by construction — it cannot be
    # written in as adopted, whatever the caller passes, until the method that
    # produced it has been validated on more than one name.
    if status is None:
        # A FUNDAMENTAL walk-forward finding is provisional by construction —
        # one name is not a validated method. A PRICE-ENGINE finding rests on
        # nineteen names and 317 resolved forecasts, so it is not.
        status = ("provisional" if origin == "walk_forward_fundamental"
                  else "adopted")
    if origin == "walk_forward_fundamental" and status == "adopted":
        raise ValueError("%s: a fundamental walk-forward lesson may not be "
                         "adopted while the method rests on one name" % id)
    return {"id": id, "scope": scope, "applies_to": applies_to,
            "headline": headline, "plain": plain, "source": source,
            "origin": origin, "evidence": evidence,
            "overturned_by": overturned_by, "status": status}


DEV = "real-estate developer, off-plan, percentage-of-completion"

LESSONS = [

    # ---------------------------------------------------------------- ALL ---
    L("L-001", "ALL", None,
      "Revenue and cost must be recognised on the same clock.",
      "If you count the money coming in as the building goes up, you must count "
      "the money going out the same way. Book revenue as you build but costs "
      "only when you hand over the keys, and the costs arrive late — so every "
      "year looks more profitable than it is.",
      "PHDC walk-forward, 30-Aug-2026",
      "walk_forward_fundamental",
      "Gross profit came out about 72% too high, in 86% of tested cases, and "
      "that fed through into a net profit about 3x too high in 97% of cases — "
      "worse than simply assuming last year's profit repeats.",
      "An issuer that genuinely recognises revenue only on handover, where the "
      "two clocks already coincide."),

    L("L-002", "ALL", None,
      "A correction factor is only honest when the model is right.",
      "When a forecast is consistently wrong in the same direction, it is "
      "tempting to add a fudge factor. But a steady error usually means "
      "something is wired wrong, and a fudge factor hides the wiring instead "
      "of fixing it. Fix the wiring.",
      "PHDC walk-forward, 30-Aug-2026",
      "walk_forward_fundamental",
      "Interest was being divided by total current liabilities (EGP 105.1bn) "
      "instead of by debt that actually pays interest (EGP 24.1bn) — a "
      "denominator 4.4x too big, implying a 3.19% borrowing rate for a company "
      "that borrows at 13.91%. The resulting 'bias' looked real and a "
      "half-strength correction 'worked', cutting the error from 0.85 to 0.40.",
      "Nothing. A mis-specification is never fixed by a multiplier."),

    L("L-003", "ALL", None,
      "Before adopting any correction, ask whether it matches how we treat that "
      "driver everywhere else.",
      "A number that is out of line with the rest of the book usually means our "
      "own method slipped on this one name — not that the company is unusual. "
      "That second question is what tells the two apart.",
      "PHDC walk-forward, 30-Aug-2026",
      "walk_forward_fundamental",
      "The finance-cost correction passed its own test and was blocked by this "
      "one, which is how the wrong denominator in L-002 was found. Every other "
      "Egyptian study builds interest from named facilities, each at its own "
      "rate.",
      "Nothing yet. If a correction ever fails this test for a reason that "
      "turns out to be a genuine company difference, record it here."),

    L("L-004", "ALL", None,
      "Country risk must be counted once, not twice.",
      "A local government bond yield already contains the country's own risk. "
      "Add a country-risk premium on top of it and you have charged for the "
      "same danger twice, which makes every company look worth far less than "
      "it is.",
      "GBCO study; corrected across the book",
      "self_audit",
      "The error reached a delivered study and forced a re-issue of every "
      "affected valuation. The fix: normalise the risk-free rate by subtracting "
      "that sovereign's own default spread before adding the premium back.",
      "A market where the quoted government yield genuinely carries no default "
      "component."),

    L("L-005", "ALL", None,
      "Margins are an output, never an input.",
      "If the filings tell you what things cost per unit, build the cost from "
      "those units and let the margin fall out. Typing in a margin means you "
      "have assumed the answer to the most important question in the model.",
      "DU study, 17-Aug-2026",
      "critique",
      "Edition 3 held one contribution margin per segment as an input at the "
      "audited rate, discarding six months of reviewed data. Rebuilding it "
      "bottom-up surfaced a downside nobody had found: a flat blended ARPU was "
      "a mix tailwind masking per-leg erosion, worth -17.3% on the cash-flow "
      "lens.",
      "An issuer whose filings genuinely disclose no unit or per-segment cost "
      "detail — in which case say so, and flag the gap."),

    L("L-006", "ALL", None,
      "A self-audit that only re-checks what you did will keep missing what you "
      "never did.",
      "Checking your own sums proves the sums are right. It does not tell you "
      "about the whole disclosure you never opened. Ask what the filings "
      "contain that the model does not use.",
      "DU study, 17-Aug-2026",
      "critique",
      "DU's self-audit found seven defects no critique had raised, and still "
      "missed the largest one — that the cost side had not been built from the "
      "bottom up at all. It surfaced only when a rebuild was forced.",
      "Nothing. This is a rule about how to audit, not about any company."),

    L("L-007", "ALL", None,
      "Try the company's own website before any data provider.",
      "The company's own investor-relations page is the source. A data "
      "provider's summary is somebody else's transcription of it, and "
      "transcriptions drift.",
      "ARCC study, 07-Aug-2026",
      "critique",
      "Adopted after a study leaned on aggregator figures while the company's "
      "own quarterly filing sat unread. Log every attempt, including the ones "
      "that fail — a site that will not load is a fact worth recording.",
      "Nothing. Where the primary source is unreachable, stop and say so rather "
      "than substituting a weaker one."),

    L("L-008", "ALL", None,
      "A period is not researched until both its statements AND its results "
      "release are in.",
      "The financial statements give you the numbers. The results release gives "
      "you what they mean — the order book, the volumes, the sales. Reading one "
      "without the other leaves the model running on stale drivers.",
      "MODON study, 09-Aug-2026, found by an outside critique",
      "critique",
      "MODON's first edition read the half-year statements but not the release "
      "published the same month, whose AED 65.4bn order book and AED 26bn "
      "half-year sales superseded the study's core drivers. Caught externally, "
      "restruck the same day.",
      "An issuer that publishes no results release at all — record the absence."),

    L("L-009", "ALL", None,
      "One escalator per cost driver, never one blended rate across all of them.",
      "Coal, imported fuel, local wages and transport do not all rise at the "
      "same speed. Escalating them together with a single inflation number "
      "invents a margin trend that is an artefact of the shortcut.",
      "ARCC study, 07-Aug-2026",
      "critique",
      "The whole of one study's forecast margin decline turned out to be a "
      "mechanical consequence of setting the price path below a single blended "
      "cost index every year — and was already contradicted by a realised "
      "quarterly margin above the prior full year.",
      "A cost base genuinely made of one input."),

    L("L-010", "ALL", None,
      "Never divide one year's value by another year's volume.",
      "If sales are disclosed to 2024 and unit counts only to 2023, dividing "
      "one by the other does not give you a price. It gives you a number with "
      "no meaning.",
      "PHDC walk-forward, 30-Aug-2026",
      "walk_forward_fundamental",
      "Taking each series' latest available year separately produced a price "
      "per unit of 28.5 against a true figure of 11.2 — off by a factor of "
      "two and a half.",
      "Nothing. This is arithmetic."),

    L("L-011", "ALL", None,
      "Publish long-horizon forecasts as ranges, never as points.",
      "A five-year forecast is not one number. Show the spread the method has "
      "actually produced in testing, so a reader can see how much is known.",
      "PHDC walk-forward, 30-Aug-2026",
      "walk_forward_fundamental",
      "At five years the measured spread on revenue ran from 83,620 to 214,090 "
      "EGP mn, and rested on five resolved observations. Publishing a single "
      "figure would have implied precision that ten origins cannot support.",
      "A record long enough and tight enough that the range collapses — which "
      "would itself be the evidence."),

    L("L-012", "ALL", None,
      "Company guidance is scored, never used as an input.",
      "Management's forward targets lean the same way an optimistic model does. "
      "Feeding them in imports the bias instead of correcting for it. Grade "
      "them against outcomes instead.",
      "PHDC walk-forward, 30-Aug-2026",
      "walk_forward_fundamental",
      "Every target quoted retrospectively had been beaten; both targets that "
      "could be graded BEFORE the outcome were missed, over-forecasting "
      "handovers by about 25%. The model's own delivery bias leaned the same "
      "way.",
      "An issuer with a long record of forward targets graded in its own "
      "disclosures."),

    L("L-013", "ALL", None,
      "A recent reviewed actual beats a stale full-year rate.",
      "Anchor unit costs and rates on the most recent reviewed period. Only let "
      "them drift where a named mechanism has a measured direction in the "
      "company's own figures — and hold everything else flat, including "
      "improvements you would like to believe.",
      "DU study, 17-Aug-2026",
      "critique",
      "Carrying a first-half rate into the second half was proved to OVERSTATE "
      "cost, using the prior year's own actual halves.",
      "A structural mechanism with a measured like-for-like direction in the "
      "issuer's own period pair."),

    L("L-014", "ALL", None,
      "A check must look at the thing that actually ships.",
      "It is easy to build a check that inspects a slightly different object "
      "from the one the reader sees — and it will report clean forever.",
      "PHDC study build, 30-Aug-2026",
      "build",
      "The table-width audit read cell widths back and reported clean, while "
      "the renderer reads a separate column grid that nothing had set. "
      "MEASURED ACROSS THE BOOK RATHER THAN ASSUMED: 39 of 984 tables in 44 "
      "delivered documents have a grid disagreeing with their stated widths, "
      "concentrated in two (31 of 33, and 8 of 10). Most builders escape it "
      "only because they happen to set COLUMN widths, which the library "
      "propagates into the grid — an accident of which call was used, not "
      "something any check was testing. The same species had already appeared "
      "twice: a beta check that trusted a self-set flag, and page checks that "
      "parsed with a regex where the browser reads the last value.",
      "Nothing. When this species appears again, close the class, not the "
      "instance."),

    L("L-015", "ALL", None,
      "An empty result is not a clean result.",
      "A check that examined nothing looks exactly like a check that found "
      "nothing wrong. Always count what was examined against a total held "
      "somewhere else.",
      "Repo-wide, 25-Aug-2026; recurred in the PHDC build",
      "build",
      "Four instances in one session, then a fifth: the study's four figures "
      "had no committed code that built them at all. They were produced once by "
      "hand and thereafter only checked, so one figure was drawing a grid the "
      "model had stopped producing and another could not be rebuilt at all.",
      "Nothing. When a probe comes back empty, first assume the probe did not "
      "run."),

    L("L-016", "ALL", None,
      "One document, one model.",
      "If two different models feed one report, it will publish two different "
      "answers and nobody will notice, because each one looks right beside its "
      "own neighbours.",
      "PHDC study build, 30-Aug-2026",
      "build",
      "The headline range, the sensitivity grid and the entire workbook came "
      "from a ten-year capacity model while the summary tables and the bridge "
      "came from the bottom-up model — EGP 9.17-38.74 in the headline against "
      "EGP 2.85-38.75 two pages later. Found by independently recalculating the "
      "delivered workbook, not by reading it.",
      "Nothing. A deliberately published second model must be labelled as a "
      "cross-check, never as the answer."),

    L("L-017", "ALL", None,
      "Never resolve a spreadsheet row by its position.",
      "Row numbers move the moment anyone inserts a line. A check pointed at "
      "the wrong row still computes, and still reports a number. Look rows up "
      "by their label.",
      "PHDC study build, 30-Aug-2026",
      "build",
      "After one driver was added to the workbook, the recalculation read "
      "'revenue per delivered unit' where it expected revenue and reported a "
      "mismatch four orders of magnitude wide.",
      "Nothing."),

    L("L-018", "ALL", None,
      "A registered input that no line of the model consumes is a defect.",
      "Putting a number in the register is not the same as using it. A cost the "
      "company really pays, sitting in the register and consumed by nothing, is "
      "money the valuation has quietly ignored.",
      "AMOC study self-audit, 06-Aug-2026",
      "self_audit",
      "Employees' profit share and board bonuses — about EGP 135mn a year, a "
      "real cash distribution — were registered, quoted in the delivered "
      "documents, and consumed by no line of the model. Worth about -7.7% of "
      "the central value.",
      "An input registered deliberately as context, explicitly marked as not "
      "consumed."),

    L("L-019", "ALL", None,
      "A balance sheet that closes on a residual is not a balance sheet.",
      "If total liabilities are computed as whatever makes the sheet balance, "
      "then every mistake anywhere else disappears into that one line and the "
      "sheet balances no matter how wrong it is.",
      "SCEM study self-audit, 06-Aug-2026",
      "self_audit",
      "One study wrote total liabilities as assets minus equity. The residual "
      "fell to about 706 against a disclosed prior-year figure of 1,611, and "
      "nothing in the model objected.",
      "Nothing. Where a residual is genuinely unavoidable it must be a named "
      "line with a stated meaning, not a silent plug."),

    L("L-020", "ALL", None,
      "Bear and bull cases must come from the model, not from multipliers.",
      "A 'bear case' produced by multiplying the central figure by 0.88 is not "
      "a scenario. It is decoration, and presenting it in a table of weighted "
      "outcomes misrepresents how it was made.",
      "SCEM study self-audit, 06-Aug-2026",
      "self_audit",
      "The published bull case was literally the central value times 1.14 and "
      "the bear times 0.88, presented as a weighted range that no weighting "
      "could produce. A separate study's published range turned out to be the "
      "minimum and maximum of one lens's extremes.",
      "Nothing."),

    L("L-021", "ALL", None,
      "Never fit an input to get the output you wanted.",
      "Introducing a number specifically to stop a line going negative is not "
      "an estimate. It is the answer working backwards into the assumptions.",
      "SCEM study self-audit, 06-Aug-2026",
      "self_audit",
      "A house estimate was introduced specifically to keep one year's EBITDA "
      "from going negative under an earlier scaling, and then carried as though "
      "it were sourced.",
      "Nothing."),

    L("L-022", "ALL", None,
      "A recognised provision is a probable outflow and belongs in the bridge.",
      "If the company has formally recognised that it probably owes something, "
      "the valuation cannot leave it out on the grounds that it is disputed.",
      "AMOC study self-audit, 06-Aug-2026",
      "self_audit",
      "A recognised tax-disputes provision of EGP 904.6mn was excluded on the "
      "reasoning that the discounted earnings were struck after tax — which "
      "confuses a forward tax rate on current profits with settling past "
      "assessments. Worth -9.8% of the central value.",
      "A provision the issuer has explicitly reversed or settled."),

    L("L-023", "ALL", None,
      "A beta must be regressed against the exchange's published index.",
      "Comparing a share against a basket of the other shares you happen to "
      "cover is not comparing it against the market. The basket changes every "
      "time you add a company.",
      "Repo-wide; measured on FERTIGLB, 10-Aug-2026",
      "build",
      "Every study in the repository had regressed against an equal-weighted "
      "composite of covered names, because the first one did and each copied "
      "the last. On the first name run both ways the composite gave a beta of "
      "0.492 against the real index's 0.931 — a 40% understatement that carried "
      "the cost of capital from 11.90% to 8.53% and overstated value by 21.6%.",
      "Nothing. Where the exchange's index is not held, stop and ask for it "
      "rather than building a substitute."),

    L("L-024", "ALL", None,
      "A cautious-sounding label is still a claim, and gets audited like one.",
      "Understating in the wrong direction is not a safe error. Conservative "
      "language slips through review precisely because it does not sound like "
      "a boast.",
      "Repo-wide, 24-Aug-2026",
      "build",
      "Pages carried the label 'failed calibration test' on names whose "
      "forecast bands had actually been too WIDE — over-covering at 97% against "
      "a 90% target — while every name whose bands genuinely ran narrow carried "
      "no flag at all. The label pointed at the wrong names for weeks.",
      "Nothing."),

    L("L-025", "ALL", None,
      "A test that has never changed an outcome is decorative.",
      "Before keeping a check, ask what it has ever rejected. If the answer is "
      "nothing, it is measuring the wrong thing or sitting at the wrong "
      "threshold — and it is occupying the place a working check should hold.",
      "Repo-wide, 25-Aug-2026",
      "build",
      "One standing gate had never excluded anything: across every verdict ever "
      "recorded the tally was 213 / 94 / 12, with no market ever blocked, while "
      "both governing documents described it as the standing gate. It was "
      "retired.",
      "Nothing."),

    L("L-026", "ALL", None,
      "Two figures for the same thing must both be published, never averaged.",
      "Where a number has two legitimate readings, showing the midpoint hides "
      "that there was a disagreement at all. Show both and say which one the "
      "answer rests on.",
      "Repo-wide; applied to PHDC's cash-flow wedge, 30-Aug-2026",
      "build",
      "PHDC's audited balance sheet and audited cash-flow statement disagree "
      "about one year by 46.8% of revenue, and the gap cannot be split from "
      "what is disclosed. The forecast is published both ways rather than "
      "reconciled by an invented plug.",
      "Disclosure that resolves the disagreement."),


    L("L-027", "ALL", None,
      "Never blend two legs that need different methods.",
      "A company with a manufacturing arm and a lending arm is two businesses. "
      "Forcing them into one model produces a number that describes neither.",
      "House method, standing protocol",
      "build",
      "Each class has a method that fits it: a developer on sum-of-the-parts, a "
      "bank on dividends and returns on equity, a holdco piece by piece, a "
      "contractor on cash flow plus parts. Where a company spans two, the legs "
      "are valued separately and added.",
      "Legs so similar that one method genuinely fits both — stated, not "
      "assumed."),


    L("L-031", "ALL", None,
      "Band coverage and a skill score answer different questions, and can "
      "disagree.",
      "A forecast range can hold exactly as often as promised while still "
      "being no better than a simple rule of thumb. Both facts are true at "
      "once. Ask which question you are answering before you quote either "
      "number.",
      "Price-engine walk-forward, 19 names",
      "walk_forward_price",
      "Across 317 resolved three-month forecasts on 19 companies, the 90% band "
      "caught the outcome 94% of the time and the 80% band 86% — close to what "
      "was promised — while the same forecasts beat a carry-anchored random "
      "walk on a proper score only 44% of the time. Coverage said the cone was "
      "honest; the score said it was no better than the naive rule.",
      "A book where the two measures agree closely across most names, which "
      "would mean one of them had stopped being informative."),

    L("L-032", "ALL", None,
      "A book-level average hides how differently individual names behave.",
      "Averaging a measure across every company can look reassuring while "
      "individual names are far off in both directions. Report the spread, not "
      "just the average.",
      "Price-engine walk-forward, 19 names",
      "walk_forward_price",
      "The middle band caught the outcome half the time on average, as "
      "designed — but per name it ran from 20% to 92% against the same 50% "
      "target. The average was right and told you almost nothing about any "
      "particular company.",
      "A book whose per-name spread narrows enough that the average is "
      "representative — which would itself have to be measured, not assumed."),

    L("L-033", "ALL", None,
      "Check the column name before believing a column of zeros.",
      "A measurement that comes back the same for everything is more often a "
      "broken query than a real finding. Look at the actual field names before "
      "you conclude anything from a suspiciously uniform answer.",
      "Price-engine walk-forward, 19 names",
      "build",
      "Scoring the whole book against its benchmark returned 0% for 18 of 19 "
      "names and 53% for the nineteenth. The 18 files name the column crps_b "
      "and the one name crps_bench; the query asked for crps_bench. The real "
      "answer is 44%. This is the same species as L-015 and it recurred inside "
      "the very session that recorded it.",
      "Nothing. When a probe comes back uniform or empty, the first hypothesis "
      "is that the probe did not run."),

    # -------------------------------------------------------------- CLASS ---
    L("L-101", "CLASS", DEV,
      "Volume is set by the launch calendar, and no demographic anchor can see "
      "it.",
      "How many units a developer sells next year depends on which projects it "
      "chooses to launch. Population growth cannot predict that. Use a "
      "population anchor to keep the driver honest, but say out loud that it "
      "runs low.",
      "PHDC walk-forward, 30-Aug-2026",
      "walk_forward_fundamental",
      "Units sold were under-forecast by about 19%, consistently, and the miss "
      "widened sharply during the devaluation years. One region's annual unit "
      "count ran 726, 1,552, 800, 1,231, 4,192 — not a trend, a launch "
      "schedule.",
      "A developer that discloses a firm forward launch pipeline, where volume "
      "can be built from the pipeline instead."),

    L("L-102", "CLASS", DEV,
      "Check the revenue-recognition basis before anything else.",
      "Developers differ in when they book a sale. Get this wrong and every "
      "profit line in the model is wrong, no matter how carefully the rest is "
      "built.",
      "PHDC walk-forward, 30-Aug-2026",
      "walk_forward_fundamental",
      "This is the class-specific form of L-001. Palm Hills moved to "
      "percentage-of-completion in January 2016; a model built without noticing "
      "produced a net-profit forecast three times too high.",
      "Nothing for this class — but confirm the basis per issuer rather than "
      "assuming it."),

    L("L-103", "CLASS", DEV,
      "A developer holds two contract positions at once, and they must move "
      "together.",
      "Buyers who have paid ahead sit as a liability; buyers still paying "
      "instalments sit as an asset. Both grow out of the same order book, so "
      "modelling one against revenue and the other against the order book "
      "makes them drift apart and the cash forecast falls apart.",
      "PHDC study, 30-Aug-2026",
      "build",
      "Driving receivables off revenue and customer advances off the order book "
      "produced a projection with cash at minus EGP 171bn and a negative "
      "present value for the forecast period. Both legs are contract-linked and "
      "must be driven consistently.",
      "A developer that sells for cash on completion, where only one leg "
      "exists."),

    L("L-104", "CLASS", DEV,
      "Deliveries must be constrained by what has actually been sold.",
      "A developer cannot hand over more homes than it has contracted. A "
      "delivery path that compounds on its own can quietly outrun the order "
      "book.",
      "PHDC study, 30-Aug-2026",
      "build",
      "The delivery driver compounds at 15% a year with nothing linking it to "
      "the order book. It happens not to bind on the current path, but it is "
      "unguarded.",
      "Nothing.",
      "outstanding"),

    L("L-105", "CLASS", DEV,
      "For a developer, the collection cycle and a fast growth path cannot both "
      "hold.",
      "If buyers pay over three years and revenue is growing 40% a year, the "
      "money going out runs far ahead of the money coming in. Something has to "
      "give, and the study should say which.",
      "PHDC study, 30-Aug-2026",
      "build",
      "Holding the collection cycle produces free cash flow negative in all "
      "five years and needs EGP 168.5bn of new borrowing by 2030, whose "
      "interest alone exceeds operating profit. Holding cash conversion "
      "instead requires the collection period to fall from 948 days to 299.",
      "A developer collecting substantially at or before handover."),

    L("L-106", "CLASS", "telecom operator",
      "A flat blended revenue-per-user can hide two opposite movements.",
      "An average that does not move can be a growing share of expensive "
      "customers cancelling a falling price on each one. It looks stable right "
      "up until the mix stops shifting.",
      "DU study, 17-Aug-2026",
      "critique",
      "A flat blended ARPU turned out to be a +2.6% mix tailwind against -2.4% "
      "per-leg erosion — worth -17.3% on the cash-flow lens once the tailwind "
      "exhausts, and invisible until the average was taken apart.",
      "An operator with a stable customer mix, demonstrated rather than "
      "assumed."),

    L("L-107", "CLASS", "telecom operator",
      "Where a company discloses one total two different ways, recover the "
      "cross-tabulation and test it.",
      "If costs are disclosed both by type and by division, those two views "
      "together often pin down the split the company never publishes — but the "
      "recovered figures must add up exactly to the disclosed lines in every "
      "period, or the assumptions behind them are wrong.",
      "DU study, 17-Aug-2026",
      "critique",
      "Direct costs disclosed three ways by nature and four by segment let the "
      "joint be recovered exactly. The test is that every residual is "
      "economically possible and foots to the disclosed line in every disclosed "
      "period, asserted in code.",
      "A recovered residual that comes out negative or fails to foot — in which "
      "case the assumption set is wrong and the joint must not be used."),

    L("L-108", "CLASS", "airline",
      "Leased aircraft must carry a liability, a rental and a cash cost.",
      "Adding leased planes to the asset side without the obligation that comes "
      "with them makes the airline look like it got them free.",
      "AIRARABIA study self-audit, 10-Aug-2026",
      "self_audit",
      "AED 300mn a year of leased-fleet additions entered invested capital with "
      "no incremental lease liability in the bridge, no rental in the cost "
      "stack and no cash outflow in free cash flow. Direction: overstates.",
      "An issuer that owns its fleet outright."),

    L("L-109", "CLASS", "petrochemical",
      "A forecast year must be producible from the disclosed half-year.",
      "If hitting your full-year number requires a second half better than any "
      "full year the company has ever had, the forecast is not a forecast.",
      "BOROUGE study, 17-Aug-2026",
      "critique",
      "The 2026 forecast needed a second-half margin of 43.2% against a "
      "best-ever full year of 41.0%, and a feedstock cost below the model's own "
      "floor. Two independent critiques reached this separately.",
      "Disclosed evidence of a genuine step-change in the second half."),

    L("L-110", "CLASS", "cement and heavy industrial",
      "Fuel and imported inputs escalate on their own commodity path, not on "
      "domestic inflation.",
      "A globally traded input like coal follows the world price and the "
      "exchange rate. Escalating it with the local cost of living invents a "
      "margin story.",
      "ARCC study, 07-Aug-2026",
      "critique",
      "The class-specific form of L-009, and the case it was adopted from: a "
      "reconciliation against an outside broker's model showed the entire "
      "forecast margin decline was an artefact of one blended index.",
      "An input genuinely priced domestically."),


    L("L-111", "CLASS", "bank",
      "A bank is valued on what reaches the shareholder, not on enterprise "
      "value.",
      "For a bank, debt is raw material rather than financing, so the usual "
      "enterprise-value approach is meaningless. Value it on dividends, on "
      "free cash flow to equity, and on returns above the cost of equity.",
      "House method, ADCB pattern",
      "build",
      "The reference bank study runs a dividend-discount model alongside free "
      "cash flow to equity and residual income. An enterprise-value discounted "
      "cash flow on a bank subtracts its own deposits as though they were "
      "borrowings.",
      "Nothing for a deposit-taking institution."),

    L("L-112", "CLASS", "holding company",
      "A holding company is valued piece by piece, never as one consolidated "
      "business.",
      "A holdco is a collection of stakes in different businesses, each worth "
      "what it is worth on its own terms. Merging them into one cash-flow "
      "forecast averages away exactly the information you need.",
      "House method, ALPHADHABI pattern",
      "build",
      "The reference holdco study values each holding separately and sums them, "
      "with the discount to that sum stated rather than assumed. Ownership "
      "stakes are sourced to the named transaction, never estimated.",
      "A holdco whose subsidiaries are so alike that one method genuinely fits "
      "them all — in which case say why."),

    L("L-113", "CLASS", "commodity and metals",
      "Say plainly when a commodity's forecast rests on borrowed calibration.",
      "Some metals have no history of their own in this system and borrow "
      "another metal's settings. That is a real limitation, and a reader is "
      "owed it in plain words rather than a footnote.",
      "House method, standing protocol",
      "build",
      "Gold is calibrated on its own data alone, so testing it against that "
      "same data proves nothing. Silver is published with no fit of its own at "
      "all — it borrows gold's. Neither may be presented with the confidence of "
      "a name that has a proper panel behind it.",
      "Enough silver, copper and platinum history to fit each on its own."),

    # -------------------------------------------------------------- STOCK ---
    L("L-201", "STOCK", "PHDC",
      "Palm Hills' units-sold figure does not affect its valuation.",
      "Revenue comes from homes handed over, not homes sold. New sales only "
      "move the reported order book. Worth knowing before spending time "
      "refining the sales forecast.",
      "PHDC study, 30-Aug-2026",
      "build",
      "Raising units sold by 50% moves value per share by exactly zero. The "
      "driver that does move it is the delivery growth rate.",
      "A model where the order book constrains deliveries — which is exactly "
      "what L-104 asks for."),

    L("L-202", "STOCK", "PHDC",
      "Palm Hills' regional unit charts overlap and must be reconciled before "
      "use.",
      "Adding up the regional figures does not necessarily give the company "
      "total, because the charts double-count. Check each release against its "
      "own printed total before trusting the sum.",
      "PHDC study and walk-forward, 30-Aug-2026",
      "build",
      "Only releases whose regional blocks reconcile to their own group total "
      "within 2% are accepted. Where they do reconcile, the regional sum runs "
      "0.8% to 1.5% above the printed total — rounding, not a different "
      "measure.",
      "Nothing; re-check on each new release."),

    L("L-203", "STOCK", "PHDC",
      "Palm Hills' 2025 balance sheet and cash-flow statement disagree by 47% of "
      "revenue.",
      "The two audited statements tell different stories about how much cash "
      "the year absorbed, and the published cash-flow statement is too summary "
      "to explain the difference.",
      "PHDC study, 30-Aug-2026",
      "build",
      "The balance sheet says working capital rose EGP 20,084.7mn; the cash "
      "flow implies EGP 3,146.2mn. The gap of EGP 16,938.5mn cannot be split "
      "from three published totals, so the forecast is published both ways.",
      "The full 2025 cash-flow statement, line by line.",
      "outstanding"),

    L("L-204", "STOCK", "PHDC",
      "Palm Hills' interest rate must be measured on the borrowings that "
      "actually bear interest.",
      "Most of what the company owes — customer deposits, suppliers, cheques — "
      "pays no interest at all. Measuring the borrowing rate against everything "
      "it owes makes it look four times cheaper than it is.",
      "PHDC walk-forward and study, 30-Aug-2026",
      "walk_forward_fundamental",
      "Total current liabilities of EGP 105,099mn against EGP 24,069mn that "
      "bears interest. The correct rate is 13.91%, not 3.19%. Part of the "
      "charge is also capitalised into work in progress rather than expensed.",
      "A change in the disclosed debt structure."),

    L("L-205", "STOCK", "PHDC",
      "Palm Hills' operating drivers stop a year before its financial "
      "statements do.",
      "The company files accounts for a year before it publishes the results "
      "release that carries units and sales — so the volume anchor is always "
      "one to two years behind the revenue figure.",
      "PHDC walk-forward, 30-Aug-2026",
      "walk_forward_fundamental",
      "Units sold stop at FY2023 and new sales at FY2024 while revenue runs to "
      "FY2025. Every affected cell records the lag rather than filling it.",
      "The company publishing a full-year results release for the latest filed "
      "year."),

    L("L-028", "ALL", None,
      "Depreciation forecast from an asset base that is itself "
      "forecast compounds its own error.",
      "Depreciation is usually projected as a rate on a fixed-asset "
      "balance that the model has also projected. Two forecasts "
      "stacked on each other drift much further than either one "
      "alone.",
      "PHDC walk-forward, 30-Aug-2026",
      "walk_forward_fundamental",
      "Bias +0.586 log (about 1.8 times too high), average miss "
      "1.112, wrong in the same direction in 77% of cases, and the "
      "sign holds across every bootstrap block tested (n=39).",
      "A build where depreciation is taken from a disclosed schedule "
      "rather than from a projected asset base, and the error stays "
      "large."),

    L("L-114", "CLASS", "real-estate developer, off-plan, percentage-of-completion",
      "A developer's new-sales value is under-forecast whenever price "
      "and volume are projected separately.",
      "Sales value is units times price. Project each one "
      "conservatively and the two shortfalls multiply, so the value "
      "comes out much lower than it should. Check the product, not "
      "just the parts.",
      "PHDC walk-forward, 30-Aug-2026",
      "walk_forward_fundamental",
      "Bias -0.369 log (about 45% too low), average miss 0.480, wrong "
      "in the same direction in 66% of cases, and the sign holds "
      "across every bootstrap block tested (n=35).",
      "A developer where price and volume are projected jointly and "
      "the value forecast is still biased low."),

    L("L-029", "ALL", None,
      "A bias that changes direction between regimes must never be "
      "corrected for.",
      "If a driver runs high in one period and low in the next, the "
      "average is a number that was never true. Record the "
      "instability and leave the driver alone.",
      "PHDC walk-forward, 30-Aug-2026",
      "walk_forward_fundamental",
      "By era: E1 pre-float -0.315; E2 post-float +0.089; E3 "
      "devaluation -0.015.",
      "A record long enough that one sign dominates across every "
      "regime tested."),

    L("L-030", "ALL", None,
      "Test every measured bias for stability across regimes before "
      "acting on it.",
      "A bias measured over a whole history can hide two opposite "
      "halves. Split the record by regime and check the sign holds in "
      "both before you treat it as a fact.",
      "PHDC walk-forward, 30-Aug-2026",
      "walk_forward_fundamental",
      "By era: E2 post-float +0.507; E3 devaluation -0.196.",
      "Nothing. This is a rule about how to read a measured bias."),

    L("L-034", "ALL", None,
      "A depreciation forecast built on a projected asset base cannot "
      "see an acquisition.",
      "Depreciation is usually projected as a rate on a fixed-asset "
      "balance the model has also projected. That works until the "
      "company buys something. An acquisition multiplies the asset "
      "base overnight and the forecast has no way to know, so the "
      "error is not noise — it is the deal.",
      "TMGH walk-forward, 1 September 2026",
      "walk_forward_fundamental",
      "Bias -0.253 log (about 29% too low), average miss 0.435, wrong "
      "in the same direction in 80% of cases, and the sign holds "
      "across every bootstrap block tested (n=30).",
      "A name with no acquisition inside the tested window whose "
      "depreciation forecast still misses in the same direction and "
      "by the same size.",
      "provisional"),

    L("L-115", "CLASS", "real-estate developer, off-plan, point-in-time on handover",
      "A developer's work in progress runs ahead of its revenue, not "
      "with it.",
      "Half-built homes are an investment made years before the "
      "revenue they produce. Driving work in progress off revenue "
      "makes the model spend when the company has already spent, and "
      "it will understate the balance every time the company is "
      "building for a growing order book.",
      "TMGH walk-forward, 1 September 2026",
      "walk_forward_fundamental",
      "Bias -0.528 log (about 1.7 times too low), average miss 0.528, "
      "wrong in the same direction in 100% of cases, and the sign "
      "holds across every bootstrap block tested (n=25).",
      "A developer whose work in progress tracks its revenue closely "
      "over a full cycle.",
      "provisional"),

    L("L-035", "ALL", None,
      "A reported finance charge is not always interest on "
      "borrowings.",
      "Before dividing a finance charge by debt to get a borrowing "
      "rate, check that the charge is actually interest on that debt. "
      "Where a company recognises a financing component on its "
      "customer contracts, the reported charge includes something no "
      "lender is being paid, and the implied rate is not a rate at "
      "all.",
      "TMGH walk-forward, 1 September 2026",
      "walk_forward_fundamental",
      "Bias -1.224 log (about 3.4 times too low), average miss 1.224, "
      "wrong in the same direction in 100% of cases, and the sign "
      "holds across every bootstrap block tested (n=30).",
      "An issuer whose finance-cost note splits interest on "
      "borrowings from every other financing charge, where the "
      "implied rate then matches its disclosed borrowing cost.",
      "provisional"),

    L("L-116", "CLASS", "real-estate developer, off-plan, point-in-time on handover",
      "The size of a demographic anchor's miss on a developer is set "
      "by the launch calendar, not by the method.",
      "A population-based volume driver runs low for every developer, "
      "but not by a fixed amount. How far low depends entirely on "
      "what the company launched, which means the miss cannot be "
      "corrected with a multiplier fitted on one name and carried to "
      "another.",
      "TMGH walk-forward, 1 September 2026",
      "walk_forward_fundamental",
      "Bias -0.877 log (about 2.4 times too low), average miss 1.022, "
      "wrong in the same direction in 76% of cases, and the sign "
      "holds across every bootstrap block tested (n=33).",
      "A third developer whose miss lands close to one of the first "
      "two, which would suggest a stable offset after all.",
      "provisional"),

    L("L-036", "ALL", None,
      "For a balance-sheet stock, assuming no change is a strong "
      "benchmark.",
      "Stocks move slowly. A model that forecasts one has to beat "
      "simply carrying last year's balance forward, and it often does "
      "not. Check that explicitly before presenting a projected "
      "balance as if it added information.",
      "TMGH walk-forward, 1 September 2026",
      "walk_forward_fundamental",
      "Negative skill against the freeze benchmark at horizons 1, 2, "
      "3, 5, worst -0.555.",
      "A stock series volatile enough that carrying it forward is "
      "clearly worse than modelling it, at most horizons.",
      "provisional"),

    L("L-037", "ALL", None,
      "Perfect foresight of inflation removes almost none of a "
      "forecast error, even across a devaluation.",
      "It is tempting to blame a bad forecast on the currency. Re-run "
      "every forecast knowing the inflation path in advance and see "
      "how much improves. Usually almost nothing does, which means "
      "the error is in how the business was modelled and looking for "
      "a macro fix wastes the effort.",
      "TMGH walk-forward, 1 September 2026",
      "walk_forward_fundamental",
      "Average miss 0.677 as known, 0.623 with perfect foresight of "
      "inflation — the macro share is only 8.1%.",
      "A market or period where the same re-run removes most of the "
      "error.",
      "provisional"),

    L("L-038", "ALL", None,
      "In a high-inflation market, a driver bias that changes "
      "direction between regimes is the normal case, not the "
      "exception.",
      "A bias measured over a whole history can hide two opposite "
      "halves, and in a market with several currency regimes that is "
      "what usually happens. Split the record by regime before "
      "treating any measured bias as a fact — on this company a third "
      "of the drivers changed sign.",
      "TMGH walk-forward, 1 September 2026",
      "walk_forward_fundamental",
      "By era: E2 post-float +0.325; E3 devaluation -0.169.",
      "A market or period where fewer than one driver in ten changes "
      "sign between regimes.",
      "provisional"),
]


def assert_lessons_register():
    """Every rule this register states about itself, enforced on itself."""
    seen, problems = set(), []
    for x in LESSONS:
        for f in ("id", "scope", "headline", "plain", "source", "origin",
                  "evidence", "overturned_by", "status"):
            if not x.get(f):
                problems.append("%s: %s is empty" % (x.get("id", "?"), f))
        if x["id"] in seen:
            problems.append("%s: duplicate id" % x["id"])
        seen.add(x["id"])
        if x["scope"] not in SCOPES:
            problems.append("%s: scope %r is not one of %s"
                            % (x["id"], x["scope"], SCOPES))
        if x["origin"] not in ORIGINS:
            problems.append("%s: origin %r is not one of %s"
                            % (x["id"], x["origin"], ORIGINS))
        if x["status"] not in STATUSES:
            problems.append("%s: status %r is not one of %s"
                            % (x["id"], x["status"], STATUSES))
        # A scoped lesson must say WHAT it is scoped to, and an ALL lesson must
        # not pretend to be scoped. Getting this wrong is how a company quirk
        # ends up applied to the whole book.
        if x["scope"] == "ALL" and x["applies_to"] is not None:
            problems.append("%s: an ALL lesson may not name a subject" % x["id"])
        if x["scope"] != "ALL" and not x["applies_to"]:
            problems.append("%s: a %s lesson must name its subject"
                            % (x["id"], x["scope"]))
        if x["scope"] == "CLASS" and x["applies_to"] not in CLASSES:
            problems.append("%s: class %r is not a registered class"
                            % (x["id"], x["applies_to"]))
    if problems:
        raise AssertionError("lessons register invalid:\n  "
                             + "\n  ".join(problems))
    return len(LESSONS)


def lessons_for(ticker=None, klass=None):
    """What a new study must read before it starts.

    Always returns every ALL lesson. Adds the CLASS lessons for the class given,
    and the STOCK lessons for the ticker given. Passing neither returns only the
    lessons that bind on every study, which is the honest default.
    """
    out = [x for x in LESSONS if x["scope"] == "ALL"]
    if klass:
        if klass not in CLASSES:
            raise KeyError("%r is not a registered class; have %s"
                           % (klass, list(CLASSES)))
        out += [x for x in LESSONS
                if x["scope"] == "CLASS" and x["applies_to"] == klass]
    if ticker:
        out += [x for x in LESSONS
                if x["scope"] == "STOCK" and x["applies_to"] == ticker.upper()]
    return sorted(out, key=lambda x: x["id"])


def counts():
    c = {s: sum(1 for x in LESSONS if x["scope"] == s) for s in SCOPES}
    c["by_origin"] = {o: sum(1 for x in LESSONS if x["origin"] == o)
                      for o in ORIGINS}
    c["by_status"] = {s: sum(1 for x in LESSONS if x["status"] == s)
                      for s in STATUSES}
    c["total"] = len(LESSONS)
    return c


if __name__ == "__main__":
    n = assert_lessons_register()
    c = counts()
    print("lessons register valid — %d lessons" % n)
    print("  by scope   : " + ", ".join("%s %d" % (s, c[s]) for s in SCOPES))
    print("  by origin  : " + ", ".join("%s %d" % (k, v)
                                        for k, v in c["by_origin"].items()))
    print("  by status  : " + ", ".join("%s %d" % (k, v)
                                        for k, v in c["by_status"].items()))
    print("\n  a new off-plan developer study must read %d lessons"
          % len(lessons_for(klass=DEV)))
    print("  a PHDC update must read %d" % len(lessons_for("PHDC", DEV)))
