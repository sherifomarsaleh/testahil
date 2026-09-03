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
    "telecom operator",
    "cement and heavy industrial",
    "petrochemical",
    "airline",
    "bank",
    "holding company",
    "commodity and metals",
    # TMGH is off-plan with a large backlog and long payment plans like the
    # class above, but it recognises revenue when the customer takes control of
    # the home, not as construction progresses. [L-102] makes the recognition
    # basis the class-defining question for developers, so filing a
    # point-in-time issuer's lessons under a class whose name asserts
    # percentage-of-completion would be the superstition this register warns
    # about. The two are kept apart.
    "real-estate developer, off-plan, point-in-time on handover",
    # AMOC buys fuel oil and wax distillate from the state oil company and sells
    # refined products drawn from the same barrel, in the same months, at prices
    # set off the same international quotes. Its margin is a ~6.6% SPREAD between
    # two numbers each above EGP 35 billion. That is a different economic animal
    # from a petrochemical producer, whose product prices can and do move
    # independently of its feedstock for long stretches, and filing a spread
    # business's lessons under "petrochemical" would be the superstition this
    # register warns about — the two react to the same shock in opposite ways.
    "refiner, commodity pass-through on a thin spread",
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
    L("L-206", "STOCK", "EGCH",
      "KIMA's urea output falls in the summer gas curtailment, so flat "
      "tonnes over-forecast every year.",
      "The complex is gas-fed and the state cuts industrial gas in the "
      "summer months when power demand peaks. Holding urea tonnes flat at "
      "the last reported year assumes a full year of gas the plant has not "
      "had since it opened. Read the auditor's tonnage table and the "
      "curtailment note before setting volume, and treat flat as the "
      "optimistic case.",
      "EGCH walk-forward, 1 September 2026",
      "walk_forward_fundamental",
      "Urea tonnes held flat at the origin over-forecast by 9.3% in all three "
      "scoreable unit-window cells (output 586kt to 522kt to 513kt); inside "
      "that window the revenue error was entirely realisation (+11%, +49%, "
      "+34%) and not volume (-11%, -12%, -2%). AMOC showed the same "
      "flat-volume lean (+7.6%, 8 of 9 cells) and the two are recorded "
      "separately until a third name shows it.",
      "A year in which reported urea tonnes reach or exceed the prior year "
      "with the curtailment still in force."),
    L("L-207", "STOCK", "EGCH",
      "EGCH: every level driver projects a plant that no longer "
      "exists.",
      "The 1960 electrolytic plant was shut inside the window and "
      "replaced by a gas-fed urea complex with about twelve times its "
      "revenue, with two loss years on either side. A rule that holds "
      "any level flat, or grows it on its own trend, from an origin "
      "before FY2020 is forecasting the old plant into years the new "
      "one reported, so revenue, cost and profit all come out far too "
      "low with a sign that never changes. On this name the record "
      "before and after the replacement must be read as two records.",
      "EGCH walk-forward, date not recorded",
      "walk_forward_fundamental",
      "Bias -0.596 log (about 1.8 times too low), average miss 0.812, "
      "wrong in the same direction in 67% of cases, and the sign "
      "holds across every bootstrap block tested (n=55).",
      "A re-run of the same rules on origins FY2020 onward only, "
      "where the revenue bias no longer holds its sign across "
      "bootstrap blocks."),

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

    # ------------------------------------------------ EMFD, 01-Sep-2026 ---
    # Learned while BUILDING the panel for a fundamental walk-forward that
    # never ran: EMFD's own investor-relations register stops at H1-2021, so
    # the run is blocked at [R-FCAL-01] §1 and no forecast was ever scored.
    # These are therefore NOT walk-forward findings and are not written as
    # any. They are defects found in our own work by the arithmetic that was
    # put there to find them, plus two facts about this company's disclosure
    # that a second name now confirms.
    #
    # NOTE ON SCOPE. Several of these findings are EMFD-specific and would be
    # STOCK lessons, but a STOCK lesson must name a real study directory and
    # engine/emfd_study/ does not exist. They are recorded in
    # engine/emfd_walkforward_pending/ and the Fundamental Driver Ledger
    # instead, and become STOCK entries when that directory does. Inventing a
    # study directory to satisfy the gate would be defeating the check.

    L("L-034", "ALL", None,
      "An extractor can be fluently, confidently wrong, and only arithmetic "
      "will say so.",
      "A tool that cannot read something usually says so. One that reads it "
      "badly hands you clean-looking numbers that are simply not on the page, "
      "and nothing about the output looks broken. Never accept a figure "
      "because the extractor produced it; accept it because it foots.",
      "EMFD source build, 01-Sep-2026",
      "build",
      "Two of EMFD's filings print EASTERN ARABIC NUMERALS. Tesseract's Arabic "
      "model returned well-formed figures such as 51,052,159 that appear "
      "nowhere on the page, at 300 and 400 dpi and at psm 4 and 6, so its "
      "output was not used. The figures used instead were read from the "
      "rendered page and accepted only because three arithmetic identities "
      "closed on each year AND a different document — the FY2015 statement of "
      "changes in equity, extracted independently by OCR in English — prints "
      "the same profit figures, 417,946,327 for FY2014 and 1,026,245 for "
      "FY2013.",
      "An extractor that fails loudly on a script it cannot read instead of "
      "emitting plausible digits."),

    L("L-035", "ALL", None,
      "Tolerance in a number parser is greed.",
      "A separator you accept 'just in case' does not sit quietly. On a "
      "two-column statement it runs straight through the gap between the "
      "columns and welds both years into one number. Accept the separator the "
      "document actually uses.",
      "EMFD balance-sheet build, 01-Sep-2026",
      "build",
      "Allowing a space to stand in for a thousands separator turned 'Fixed "
      "assets under construction 5 974,670,923 958,519,586' into a single "
      "figure of 5,974,670,923,958,519,808 — both years and the note "
      "reference together — where the value is 974,670,923. Found by the "
      "statement's own subtotal, not by reading the output.",
      "A single-column statement, where there is no adjacent column to run "
      "into."),

    L("L-036", "ALL", None,
      "A nil printed as a dash is data, and dropping it shifts every column "
      "left.",
      "Reading a row as 'the first two numbers after the label' works until a "
      "year is nil. Then the comparative slides into the current column and "
      "the row is wrong by a whole year, silently.",
      "EMFD balance-sheet build, 01-Sep-2026",
      "build",
      "EMFD's FY2020 non-current credit facilities print as 'Credit "
      "facilities 13 - 10,255,590' — nil in 2020 against 10,255,590 in 2019. "
      "Read as two numbers it put the 2019 figure into the 2020 column, and "
      "that row is the denominator of the borrowing-rate driver. The same "
      "species as L-033: a suspiciously simple reading of a table is usually a "
      "broken one.",
      "A statement that prints an explicit zero rather than a dash."),

    L("L-037", "ALL", None,
      "The first filing that mentions a year is not the year as first "
      "reported.",
      "Every annual statement prints the prior year again, as the company "
      "chooses to present it a year later. Read filings newest-first and 'keep "
      "the first record of each year' keeps the restated one — the opposite of "
      "what point-in-time discipline requires.",
      "EMFD panel build, 01-Sep-2026",
      "build",
      "EMFD's FY2013 revenue is 1,247,893,152 in its own filing and "
      "1,188,328,131 as restated in the FY2014 accounts, a 4.8% difference. "
      "Cost of revenue and profit before tax are IDENTICAL on both bases, so "
      "nothing watching the bottom line would ever have seen it. The panel now "
      "refuses to let a later filing's comparative overwrite a year's own "
      "filing, and records the restatement beside it.",
      "An issuer that never restates a comparative."),

    L("L-038", "ALL", None,
      "Judge a source by the payload it returns, never by its status code.",
      "A page that refuses you can still answer 200. Ask what the bytes are, "
      "not what the header claims, or a challenge page gets filed as a "
      "financial statement.",
      "EMFD source sweep, 01-Sep-2026",
      "build",
      "The Egyptian Exchange answers every request — including a request for a "
      "named PDF — with HTTP 200 carrying an anti-bot interstitial. Of 79 "
      "logged attempts, the ones against that host all 'succeeded'. The probe "
      "now accepts a document only if its first five bytes are %PDF-. Same "
      "family as L-014 and L-015: the check was looking at something other "
      "than the thing it was judging.",
      "A payload test that wrongly rejects a legitimate document — a filing "
      "served in a format whose magic bytes we did not anticipate."),

    L("L-039", "ALL", None,
      "Reconcile a quoted figure at the quoting document's own precision.",
      "A results release that says 'EGP 3.2 billion' is not disagreeing with "
      "an audited 3,237,263,142 — it is rounder. Score agreement against what "
      "the document actually promised, or invent disagreements and go looking "
      "for causes that are not there.",
      "EMFD KPI build, 01-Sep-2026",
      "build",
      "A fixed percentage band scored the FY2015 release as disagreeing with "
      "the audited statement. At the release's own precision — one decimal of "
      "a billion, so plus or minus 0.05bn — it agrees, and so do the FY2016 "
      "and FY2017 releases against 4,008,925,078 and 4,511,007,479.",
      "A document that quotes to full precision, where the two tests "
      "coincide."),

    L("L-040", "ALL", None,
      "A source document can be incomplete, and 'the filing exists' is not "
      "'the year is sourced'.",
      "A register that lists a year's accounts is not a guarantee that the "
      "accounts are all there. Check that the statement you need is in the "
      "file before counting the year as held.",
      "EMFD source build, 01-Sep-2026",
      "build",
      "The FY2015 year-end PDF on EMFD's own investor-relations register omits "
      "its profit-or-loss page entirely: balance sheet, changes in equity, "
      "cash flows, notes, and no income statement anywhere in 28 pages. The "
      "year was taken from the FY2016 filing's comparative column instead and "
      "flagged as a comparative rather than as first reported.",
      "A register whose files are checked for completeness at publication."),

    L("L-041", "ALL", None,
      "A rate whose denominator is immaterial is not a rate — refuse it "
      "rather than widen it.",
      "When the base that should generate a flow is close to nothing, the "
      "implied rate is nonsense, and the temptation at that moment is to widen "
      "the base until the answer looks sensible. That is how a wrong model "
      "gets a right-looking number. Leave the rate undefined and say so.",
      "EMFD financing-rule check, 01-Sep-2026",
      "build",
      "EMFD's disclosed interest-bearing borrowings imply a borrowing rate of "
      "238% in FY2019 and 69% in FY2020 — the company is effectively "
      "unlevered and the denominator is noise. Dividing the same finance cost "
      "by total liabilities would have produced about 0.04% and looked "
      "perfectly reasonable. This is L-204 seen from the other side: that "
      "lesson is about using too broad a base, this one about what to do when "
      "the correct base is too small to divide by.",
      "A filing disclosing material interest-bearing borrowings, where the "
      "ordinary rate on opening borrowings applies."),

    L("L-042", "ALL", None,
      "A pre-registration may be amended only while no result exists.",
      "Fixing the rules in advance is worth nothing if they can be adjusted "
      "once the numbers are in. Before any error is computed a change is a "
      "choice; afterwards the identical change is tuning. Date the amendment "
      "and say which side of that line it fell on.",
      "EMFD pre-registration, 01-Sep-2026",
      "build",
      "The rule for the finance-income driver formed its rate on the opening "
      "asset base. The balance-sheet extraction then showed EMFD's "
      "earning-asset base roughly doubling across FY2016-FY2017, making an "
      "opening-base rate and an average-base rate materially different "
      "quantities — the opening-base rate ranges from 8.8% to 26.6% on the "
      "extracted window. Both conventions are now computed at every origin and "
      "both reported, neither selected. The amendment was made and dated while "
      "the run was blocked and no forecast error existed.",
      "An amendment shown to be forced by an arithmetic error in the original "
      "rule, which is a correction rather than a choice."),

    # ------------------------------------------------------------- CLASS ---
    L("L-115", "CLASS", DEV,
      "An off-plan developer may be on completed contract, not "
      "percentage-of-completion — the class label can be wrong.",
      "Not every off-plan developer books revenue as it builds. Some book it "
      "only on handover, which puts revenue and cost on the same clock and "
      "makes the classic profit overstatement impossible. Read the issuer's "
      "own words before applying anything learned from another developer.",
      "EMFD source build, 01-Sep-2026",
      "build",
      "EMFD's own results releases state it in terms — 'revenues recognized "
      "according to the Completed Contract (CC) method', in both the FY2016 "
      "and FY2017 releases — so through FY2020 revenue and cost of revenue are "
      "released together at handover and L-001's own stated falsifier is met "
      "for that window. The basis then changed: EAS 48 took effect on 1 "
      "January 2021 and the one period published on both bases restates "
      "revenue by +2.72%, cost of revenue by +8.05% and gross profit by "
      "-8.42%. This is the second name behind L-102, and it widens that "
      "lesson: the basis can differ between issuers of the same class, not "
      "merely change date.",
      "A market where the recognition basis is mandated uniformly, so the "
      "class and the basis always coincide."),

    L("L-116", "CLASS", DEV,
      "A developer's operating KPIs can stop years before its statements do.",
      "Units delivered and contracted sales live in the results release, not "
      "the accounts. An issuer that stops publishing releases still files "
      "statements — so revenue keeps arriving while the drivers that explain "
      "it do not, and the unit-level model simply cannot be scored on those "
      "years.",
      "EMFD KPI build, 01-Sep-2026",
      "build",
      "EMFD's register carries results releases for FY2015, FY2016 and FY2017 "
      "only, giving delivered units of 819, 935 and 1,386. For FY2018-FY2020 "
      "no unit count exists in ANY document it publishes — no release, and the "
      "management annual reports for those years are the board's Arabic "
      "governance report with no operating data in it — while audited "
      "statements for all three years are on the same register. Units "
      "delivered, revenue per unit and cost per unit are therefore unscoreable "
      "on the three most recent years of the obtainable window. This is the "
      "second name behind L-205, which is why it is filed at class scope: "
      "PHDC's drivers lag its accounts by a year or two, EMFD's stop "
      "altogether.",
      "An issuer whose operating KPIs appear in the audited statements "
      "themselves rather than only in a results release."),


    L("L-043", "ALL", None,
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

    L("L-117", "CLASS", "real-estate developer, off-plan, point-in-time on handover",
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

    L("L-044", "ALL", None,
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

    L("L-118", "CLASS", "real-estate developer, off-plan, point-in-time on handover",
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

    L("L-045", "ALL", None,
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

    L("L-046", "ALL", None,
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

    L("L-047", "ALL", None,
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

    L("L-048", "ALL", None,
      "A forecast scenario must be internally consistent, or it "
      "invents its own bias.",
      "If you carry inflation forward at 25% a year, you cannot also "
      "hold the exchange rate still — those are the same event seen "
      "twice. Doing both inflates every cost and freezes every price, "
      "and the profit forecast is then wrong for a reason that has "
      "nothing to do with the company. Check that the macro "
      "assumptions could all be true at once before reading anything "
      "into the errors they produce.",
      "AMOC walk-forward, date not recorded",
      "walk_forward_fundamental",
      "Bias -0.570 log (about 1.8 times too low), average miss 0.570, "
      "wrong in the same direction in 100% of cases, and the sign "
      "holds across every bootstrap block tested (n=9).",
      "A scenario whose macro inputs are mutually inconsistent that "
      "nonetheless produces no directional bias in the lines they "
      "drive."),

    L("L-049", "ALL", None,
      "Test the method against 'assume no change' before trusting its "
      "profit forecast.",
      "The simplest possible forecast is to write down last year's "
      "number and stop. It is surprisingly hard to beat, and a model "
      "that loses to it has not earned the precision it displays. Run "
      "the comparison explicitly — if the model loses, publish a "
      "range and say so, rather than a point that looks more informed "
      "than it is.",
      "AMOC walk-forward, date not recorded",
      "walk_forward_fundamental",
      "Negative skill against the freeze benchmark at horizons 1, 2, "
      "3, worst -1.588.",
      "A run where the model beats the no-change benchmark on the "
      "profit line at every horizon tested."),

    L("L-050", "ALL", None,
      "Setting 'non-recurring' items to zero is a forecast, and "
      "usually a bad one.",
      "Provision releases, disposal gains and currency gains are each "
      "unpredictable, so the tempting rule is to forecast none of "
      "them. But something in that bucket lands almost every year, "
      "and zero is further from the truth than simply carrying last "
      "year's total forward. If the individual items cannot be "
      "forecast, forecast the bucket.",
      "AMOC walk-forward, date not recorded",
      "walk_forward_fundamental",
      "Negative skill against the freeze benchmark at horizons 1, 2, "
      "3, worst -0.785.",
      "An issuer whose other-income line is genuinely empty in most "
      "years, where zero beats carrying the previous year forward."),

    L("L-051", "ALL", None,
      "A number that is zero by construction is not a finding about "
      "the world.",
      "If a driver contains no inflation term, then re-running it "
      "with perfect knowledge of inflation must change nothing, and "
      "the 'macro share' of its error must come back at exactly zero. "
      "That is arithmetic, not evidence. Declare which drivers those "
      "are BEFORE running the split, so a structural zero cannot be "
      "read back as a discovery.",
      "AMOC walk-forward, date not recorded",
      "walk_forward_fundamental",
      "Average miss 0.606 as known, 0.606 with perfect foresight of "
      "inflation — the macro share is only 0.0%.",
      "Nothing. A quantity fixed by construction cannot become "
      "evidence about the world."),

    L("L-119", "CLASS", "refiner, commodity pass-through on a thin spread",
      "On a thin spread, being right about both sides separately is "
      "not enough.",
      "When profit is a small difference between two very large "
      "numbers, an error that looks tiny on each of them is enormous "
      "on the difference. Six per cent out on revenue and almost "
      "exact on cost still left the gross profit forecast wrong by "
      "two thirds. What has to be right is the two sides RELATIVE to "
      "each other, and a model that forecasts them independently will "
      "not deliver that however good each looks alone.",
      "AMOC walk-forward, date not recorded",
      "walk_forward_fundamental",
      "Average miss 0.504 as known, 0.519 with perfect foresight of "
      "inflation — the macro share is only -2.8%.",
      "A pass-through business with a comparably thin margin where "
      "independent revenue and cost forecasts of similar accuracy "
      "produce a proportionate, not amplified, profit error."),

    L("L-052", "ALL", None,
      "Check an annualised half-year base against every full year you "
      "hold.",
      "A base year built by doubling one good half can sit well above "
      "anything the company has actually achieved over twelve months. "
      "Growing from it then compounds a rebound into a trend. Before "
      "forecasting growth off a part-year base, line it up against "
      "the full-year record — and if the base is already the highest "
      "number in that record, flat is the optimistic case, not the "
      "neutral one.",
      "AMOC walk-forward, date not recorded",
      "walk_forward_fundamental",
      "AMOC's base half annualises to 1,616,167 tonnes against a "
      "five-year mean of 1,436,781 and a most recent full year of "
      "1,261,586; audited sales tonnage ran 1,492,273 / 1,547,816 / "
      "1,448,889 / 1,433,341 / 1,261,586 over FY2021-FY2025. Even a "
      "FLAT volume rule over-forecast, bias +7.6% and too high in 8 "
      "of 9 tested cases.",
      "A part-year base that is representative of the full-year "
      "record, where growing from it does not over-forecast."),

    L("L-053", "ALL", None,
      "A coherence test is only as good as the estimate inside it.",
      "Checking a disclosure against your own reconstruction of it is "
      "a good habit, but the reconstruction can be the thing that is "
      "wrong. Before rejecting a company's own figure, ask which line "
      "in your test is estimated and how volatile that line is. If "
      "the answer is the most volatile line in the statement, the "
      "test cannot carry the weight of a rejection.",
      "AMOC walk-forward, date not recorded",
      "build",
      "AMOC's released gross profit for the half to June 2026 was "
      "rejected on a test that estimated the half's other income by "
      "DOUBLING the March quarter's 225,556,509, giving 451mn against "
      "the 196,526,615 the filing later showed. The released figure "
      "was right to 0.03%. Gross profit was then solved from the "
      "profit line at 8.997% against a filed 9.653%, and that base- "
      "year margin ran through all four lenses.",
      "A rejection built on an extrapolated volatile line that a "
      "later filing confirms was correct."),

    L("L-054", "ALL", None,
      "Value the whole firm, or value the operations and add the cash "
      "— never both.",
      "When a company holds more cash than debt, weighting its cost "
      "of capital on NET debt makes the debt weight negative and "
      "pushes the rate used on the OPERATING cash flows above the "
      "cost of equity. If the cash is then added back at face in the "
      "bridge, the same cash has been charged for twice: once by "
      "discounting the business as though owning a deposit made it "
      "riskier, and once by counting the deposit at par.",
      "AMOC walk-forward, date not recorded",
      "build",
      "AMOC's operating cash flows were discounted at 31.19% against "
      "a cost of equity of 27.45% — 374 basis points higher — because "
      "net cash of 3.0bn against a market capitalisation of 11.8bn "
      "gives a debt weight of -26.2%. The bridge then added the 3.0bn "
      "at face. Gross borrowings are 0.14% of the capital structure, "
      "so the unlevered rate is the cost of equity to three decimals.",
      "A construction in which a net-cash-weighted rate is used on "
      "operating cash flows AND the cash is left out of the bridge — "
      "which is the other consistent pair, and equally acceptable."),

    L("L-055", "ALL", None,
      "Terminal growth and the terminal discount rate must agree "
      "about inflation.",
      "The discount rate used past the forecast horizon has an "
      "inflation assumption buried inside it, usually through the "
      "risk-free rate. If terminal growth is set below that number, "
      "the model is quietly assuming the business shrinks in real "
      "terms for ever — a large, permanent claim that nobody wrote "
      "down and no disclosure supports. Read the inflation out of the "
      "terminal rate first, then choose growth against it and state "
      "the real growth you have assumed, even when it is zero.",
      "AMOC walk-forward, date not recorded",
      "build",
      "AMOC's first pass carried terminal growth of 5.0% against a "
      "terminal risk-free of 12.5% embedding the central bank's 7% "
      "target — a perpetual real decline of about 2% a year, never "
      "stated. Set to 7% (inflation only, zero real), the central "
      "moved from 5.53 to 8.64 against a spot of 9.10 together with "
      "the other five corrections.",
      "A study that deliberately assumes real decline in perpetuity, "
      "says so, and shows the disclosure or industry evidence "
      "supporting it — that is a stated assumption, not this defect."),

    L("L-056", "ALL", None,
      "A claim about the record — 'best ever', 'never' — is "
      "recomputed, never typed.",
      "Superlatives are the sentences a reader remembers and the ones "
      "nobody checks, because they read as colour rather than as "
      "arithmetic. They also go stale silently: typed once against an "
      "early version of the model, they survive every later change to "
      "it. Compute the claim from the filings in the same pass that "
      "computes the number it describes, and drive the sentence off "
      "that value rather than retyping it.",
      "AMOC walk-forward, date not recorded",
      "build",
      "AMOC's headline said the market price required a gross margin "
      "'above the best single quarter this company has ever filed' at "
      "12.2%. The figure was typed, never solved, and never revisited "
      "as the model moved. Solved by bisection it is 9.37% — below "
      "the 9.653% just filed for twelve months — and the company had "
      "already printed 13.84% for FY2022 and 13.92% in the quarter to "
      "June 2026, so the claim was false twice over.",
      "A delivered superlative that a reader can verify from the "
      "study's own committed numbers without recomputing it — at "
      "which point it was computed, not typed."),

    L("L-057", "ALL", None,
      "Interest income is a balance times a rate, and holding it flat "
      "cannot track either.",
      "A company that builds a cash pile into rising deposit rates "
      "earns dramatically more interest, and a company that spends "
      "one earns less. Carrying last year's figure forward misses "
      "both moves at once. Drive it off the cash balance at the "
      "deposit rate, the same way the rest of the book does.",
      "ARCC walk-forward, date not recorded",
      "walk_forward_fundamental",
      "Bias -1.641 log (about 5.2 times too low), average miss 2.177, "
      "wrong in the same direction in 76% of cases, and the sign "
      "holds across every bootstrap block tested (n=25).",
      "Nothing. This is arithmetic."),

    L("L-120", "CLASS", "cement and heavy industrial",
      "Haulage cost follows the EXPORT tonne, so a cost per tonne "
      "despatched misprices it.",
      "Cement sold at home moves a short distance to a local "
      "customer; clinker sold abroad moves to a port. Spreading "
      "haulage across every tonne despatched makes the cost look like "
      "a rate that inflation moves, when it is really a mix effect. "
      "When the export share falls, a per-despatched-tonne driver "
      "overstates the cost.",
      "ARCC walk-forward, date not recorded",
      "walk_forward_fundamental",
      "Bias -0.693 log (about 2.0 times too low), average miss 0.791, "
      "wrong in the same direction in 76% of cases, and the sign "
      "holds across every bootstrap block tested (n=25).",
      "A producer whose local and export haulage rates per tonne are "
      "disclosed and turn out to be the same."),

    L("L-058", "ALL", None,
      "An exogenous volume anchor has to be scored against 'no "
      "change' before it is trusted.",
      "The protocol asks for volume to be driven by something outside "
      "the company — population, credit, activity — rather than by "
      "its own trend. That is the right instinct and it is not self- "
      "validating: the anchor can point the wrong way. Score it "
      "against simply carrying last year's volume forward, and if it "
      "loses, the driver is mis-specified and no correction factor "
      "will repair it.",
      "ARCC walk-forward, date not recorded",
      "walk_forward_fundamental",
      "Negative skill against the freeze benchmark at horizons 1, 2, "
      "3, 4, 5, worst -0.260.",
      "A study where the exogenous anchor loses to freeze and the "
      "anchor is still the better forecast out of sample."),

    L("L-059", "ALL", None,
      "If perfect knowledge of the macro path makes a MARGIN forecast "
      "worse, the two legs were cancelling.",
      "A margin is a difference, so its error is the difference of "
      "two errors. When revenue and cost are both wrong in the same "
      "direction the margin can come out nearly right for the wrong "
      "reason. Handing the model the true inflation and currency path "
      "repairs the two legs by different amounts and breaks that "
      "cancellation — which is why the margin forecast can get WORSE "
      "with better information. The practical consequence is the "
      "important part: never recalibrate one leg onto a fresh actual "
      "without recalibrating the other on the same one.",
      "ARCC walk-forward, date not recorded",
      "walk_forward_fundamental",
      "Average miss 1.265 as known, 1.339 with perfect foresight of "
      "inflation — the macro share is only -5.8%.",
      "A run where the macro split is positive on the margin and "
      "negative on both of the legs that make it, which would mean "
      "the cancellation runs the other way."),

    L("L-060", "ALL", None,
      "A bottom-line bias that flips sign between regimes is "
      "instability, and must not be corrected.",
      "Net profit is what is left after everything else, so it "
      "inherits every driver's error and the currency's on top. When "
      "its miss runs one way before a devaluation sequence and the "
      "other way through it, the average is a number that was true in "
      "neither period. Report the instability; do not correct for it.",
      "ARCC walk-forward, date not recorded",
      "walk_forward_fundamental",
      "By era: E1 pre-2022 -0.581; E2 devaluation sequence +0.006.",
      "A record long enough that one sign dominates the bottom line "
      "across every regime it contains."),

    L("L-061", "ALL", None,
      "A correction that makes the out-of-sample error WORSE is a "
      "specification defect, not a bias.",
      "It is tempting to treat any consistent miss as something a "
      "multiplier can fix. Test the multiplier the way you would test "
      "a forecast: estimate it only on data that had already "
      "resolved, then apply it forward. If the error gets worse, the "
      "problem is in how the driver is wired, and a correction would "
      "only hide it.",
      "ARCC walk-forward, date not recorded",
      "walk_forward_fundamental",
      "Applied -0.108 at origin FY2022; average miss changed -0.108.",
      "A driver whose correction degrades out of sample and is "
      "nevertheless shown to be a calibration problem rather than a "
      "specification one."),

    L("L-062", "ALL", None,
      "A sensitivity that does not reproduce the headline when "
      "nothing is changed is a second model.",
      "Every study has a block that re-values the company under a "
      "different assumption. If that block rebuilds the calculation "
      "instead of reusing it, it will drift from the answer it is "
      "supposed to be testing — and it will drift silently, because "
      "nobody compares a sensitivity to the base case. Call the "
      "function with nothing changed and require it to return the "
      "published number.",
      "ARCC walk-forward, date not recorded",
      "self_audit",
      "On ARCC the re-valuation function discounted the terminal "
      "value at the last explicit year's mid-year factor while the "
      "headline used the end-of-window factor. Called with no change "
      "it returned 57.27 against a published 55.21, so every "
      "sensitivity and every contested judgement in the study was "
      "quoted on a basis 3.7% more generous than the number it was "
      "compared against. The assertion that now enforces it caught a "
      "SECOND instance on its first run, when a new income line was "
      "added to the headline and not to the rebuild.",
      "Nothing. A sensitivity that cannot reproduce its own base case "
      "is measuring something else."),

    L("L-063", "ALL", None,
      "If every observation you have includes growth spending, they "
      "are a CEILING on maintenance, not a midpoint.",
      "When the only capital-spending figures available are years "
      "that also carried expansion projects, those figures are the "
      "most maintenance could possibly have been. Setting the "
      "maintenance assumption in the middle of that band puts it "
      "above some of the observations and treats an upper bound as a "
      "central estimate.",
      "ARCC walk-forward, date not recorded",
      "self_audit",
      "ARCC's input note observed that FY2024 (USD 3.70/t) and FY2025 "
      "(USD 3.23/t) 'both carry the alternative-fuel and silo "
      "programmes' and then set maintenance at USD 4.00/t — above "
      "both. The H1-2026 cash-flow statement settled the direction by "
      "splitting the spend: EGP 102.9mn of property, plant and "
      "equipment against EGP 505.5mn of assets under construction, so "
      "83% of it was the growth programme. Resetting the anchor to "
      "the most recent full year's total was worth EGP 0.84 on the "
      "central.",
      "A disclosure that separates maintenance from growth capital "
      "directly, which makes the inference unnecessary."),
    L("L-064", "ALL", None,
      "While a project is under construction, its interest and "
      "currency losses go to the asset, not the income statement.",
      "Under IAS 23 and its Egyptian equivalent, the interest on a "
      "loan that funds a qualifying asset — and the exchange loss on "
      "that loan — is capitalised into the asset until it is ready "
      "for use. So a borrowing rate formed from the income-statement "
      "charge during construction understates what the loan actually "
      "costs, and a currency driver that charges the revaluation to "
      "profit invents a loss the company will never book there. Form "
      "the rate on the loan's own terms, put the construction-period "
      "charge on the balance sheet, and move it to the income "
      "statement only when the asset is commissioned.",
      "EGCH walk-forward, date not recorded",
      "walk_forward_fundamental",
      "Bias -1.276 log (about 3.6 times too low), average miss 1.372, "
      "wrong in the same direction in 86% of cases, and the sign "
      "holds across every bootstrap block tested (n=28).",
      "An issuer that expenses all borrowing costs as incurred, where "
      "the rate formed on the income-statement charge matches the "
      "loan's disclosed cost and the currency revaluation appears in "
      "profit in the year of the devaluation."),
    L("L-065", "ALL", None,
      "A statutory-rate tax driver must first check whether the "
      "company pays current tax at the origin.",
      "Tax by formula at the statutory rate is the right rule for a "
      "regime, but a company carrying forward large losses, or taking "
      "an accelerated first-year deduction on new plant, books no "
      "current tax for years and then a deferred charge or credit "
      "that the formula cannot see. Read the current-tax line and the "
      "deferred-tax note at the origin before applying the rate; "
      "where current tax is nil, say so and carry the zero-tax case "
      "beside the statutory one rather than assuming it away.",
      "EGCH walk-forward, date not recorded",
      "walk_forward_fundamental",
      "Average miss 1.500 as known, 2.028 with perfect foresight of "
      "inflation — the macro share is only -35.2%.",
      "A run on a company whose current tax at every origin equals "
      "the statutory rate on profit before tax, where the formula's "
      "error is inside the other drivers' noise."),

    L("L-066", "ALL", None,
      "A checklist a study fills in about itself measures its opinion "
      "of the work, not the work.",
      "Where a standard can be read off the delivered file, read it "
      "off the delivered file. An attestation is only worth what an "
      "outside reader could not otherwise see; anything a script can "
      "measure directly should be measured directly, and the "
      "attestation kept for the judgements that genuinely cannot be.",
      "AMOC and ARCC delivered-workbook audit, 01-Sep-2026",
      "self_audit",
      "AMOC's compute.py set structure_matches_model=True and "
      "assert_model_study() passed on that boolean, while the "
      "delivered workbook carried SEVEN sheets against the model "
      "report's sixteen. Every other gate that could see the file was "
      "examining its contents: the recalculation reconciled 5,775 "
      "formula cells with zero disagreements, the external-reader "
      "scrub was clean and table discipline reported zero problems "
      "across both documents. None of them was looking at its shape. "
      "Reading the sheet list off the .xlsx from outside found it in "
      "one line.",
      "A standard that cannot be expressed as a test of the delivered "
      "artefact, where the attestation is the only evidence "
      "available."),

    L("L-208", "ALL", None,
      "A check that fails by the calendar is not a check.",
      "If a generated file carries today's date, or an age counted in days, "
      "and something compares that file byte for byte, the comparison starts "
      "failing at midnight with nothing changed. Everyone learns to ignore it, "
      "and then they ignore it on the night it means something. Put the date "
      "the CONTENT was sourced in the file, and leave 'how old is that now' to "
      "a tool someone runs.",
      "Cost-of-capital reference gate, 03-Sep-2026",
      "self_audit",
      "engine/Cost_of_Capital_Reference.md is compared byte for byte against "
      "its generator's output in CI, and the generator stamped it with "
      "date.today() and with the sovereign quote's age in days. It went red "
      "every midnight from 02-Sep-2026, and by the time it was found a red "
      "gate on that branch was already being read as background noise. The "
      "document now carries the date its paths were sourced; rebuilt under a "
      "faked 2027-05-17 clock it is byte-identical to today's output.",
      "A byte-compared artefact whose consumers genuinely need the run date — "
      "in which case the comparison, not the date, is the thing to change."),

    L("L-209", "ALL", None,
      "An observed number and an estimated one need different evidence to be "
      "point-in-time.",
      "A price, a policy rate, an auction result is fixed the day it happens "
      "and nobody revises it, so looking it up today is fine. A price index or "
      "a national account is revised and rebased for years, so today's version "
      "is NOT what anyone had at the time and using it silently rewrites "
      "history. The second kind needs the publication that existed then.",
      "Point-in-time macro archive, 03-Sep-2026",
      "build",
      "Across the six origins where both are held, Egypt's inflation as "
      "published AT the origin and as reported for that same year today differ "
      "by 4.24 percentage points on average and 7.50 at worst, in both "
      "directions (2017 +7.50, 2018 -6.46). At those sizes an escalator, the "
      "currency path derived from it and the terminal all move.",
      "An observed series that turns out to be revised after the fact — a "
      "settled or restated market close is exactly that, and this repository "
      "has already seen one on a metals anchor."),

    L("L-210", "ALL", None,
      "A mean far from its median is a tail, and a tail is a different problem "
      "from a bias.",
      "If the average name is 10% below the market but the middle name is on "
      "it, the house is not pessimistic — it is inconsistent, and a handful of "
      "names carry the whole gap. Moving a rate to fix the average would push "
      "every reasonable name off the market to correct a few that are wrong.",
      "Delivered-book measurement, 03-Sep-2026",
      "self_audit",
      "Across all 90 published fair values against the prices they were struck "
      "at, the mean is -10.6% and the MEDIAN is -0.3%, with 46 of 90 below the "
      "price. Ten names read more than 40% below against three more than 40% "
      "above, and the exchange-clustered interval straddles zero.",
      "A book whose mean and median agree, where a uniform correction is "
      "exactly the right instrument."),

    L("L-211", "ALL", None,
      "A CI step assumes a disposable runner; a working checkout is not one.",
      "Workflow steps are written knowing the machine gets thrown away, so "
      "they rebase, reset and auto-commit freely. Running them where the work "
      "lives does what they say.",
      "run_ci_gates.py incident, 03-Sep-2026",
      "self_audit",
      "A script written to run CI's own steps locally reached a workflow that "
      "rebases and auto-commits: the checkout was left mid-rebase on a "
      "detached HEAD, a directory was emptied on disk, and an uncommitted file "
      "was swept into a commit describing something else. Nothing was lost "
      "only because every commit was already pushed, which is timing rather "
      "than design.",
      "A runner that executes such steps inside a throwaway worktree, where "
      "the assumption they are written under actually holds."),

    L("L-212", "ALL", None,
      "A local check sweep must read the list CI runs, not a list somebody "
      "keeps.",
      "Running the checks you remember is not running the checks. The two "
      "lists drift the moment a step is added straight to the workflow, and "
      "the difference is invisible from the side you are standing on.",
      "Gate-sweep population, 03-Sep-2026",
      "self_audit",
      "'Every gate green' was reported here while CI had been red for a day on "
      "a step that lives inline in the workflow and was never in the "
      "hand-maintained list. The sweep now parses the workflow and runs every "
      "step it declares, so a step added to CI is a step it runs.",
      "Nothing yet. If a workflow ever declares steps that cannot be "
      "meaningfully run outside the runner, they are skipped BY NAME and "
      "counted, never dropped."),

    L("L-067", "ALL", None,
      "A gate pointed at a superseded file reports on something "
      "nobody receives.",
      "When a study is re-issued, every check that opens the "
      "delivered file by name has to move with it. A check left "
      "pointing at the previous edition keeps passing, and its green "
      "says nothing about what was actually shipped.",
      "AMOC and ARCC delivered-workbook audit, 01-Sep-2026",
      "self_audit",
      "Three further instances have been found since, which is why this is "
      "filed at ALL and not as one study's mishap: a valuation-gap review "
      "green-lighted against an answer that had moved from 3.76 to -1.06; the "
      "fair-value register reporting [ok] while it sat two editions behind the "
      "study it records; and a vintage archive that would have done the same "
      "had its gate checked existence. Every one asked whether an artefact "
      "EXISTED. Originally: ARCC's driver_test.py and label_gate.py both opened "
      "ARCC_Valuation_Model_06082026_public.xlsx while the delivered "
      "file was the 01092026 edition, and both reported clean. Re- "
      "pointed at the delivered file, five of the driver assertions "
      "failed at once: revision 4 had moved the valuation date to 30 "
      "June 2026 and put the bridge on that reviewed balance sheet, "
      "so the FY2025 cash, minority and declared-dividend rows no "
      "longer move the headline and the assertions that said they did "
      "had never run against the model that shipped.",
      "A build that writes to one filename per study, so there is no "
      "superseded edition for a check to open."),]


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
