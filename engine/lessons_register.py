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
    # ADNOCLS earns vessel-days times day rates set in a GLOBAL charter market in US
    # dollars, and owns assets that trade in a liquid international secondhand market at
    # broker-quoted prices. Both halves of that are different from every asset-heavy class
    # above. A cement plant's price is set in a domestic market behind freight protection
    # and its kiln cannot be sold to a buyer in another country; a charter rate can halve
    # in a year and a vessel can. So the two react to the same shock in opposite ways, and
    # the lens that carries the weight is different: replacement cost is an industry rule
    # of thumb for a kiln and an OBSERVABLE PRICE for a ship. Filing a shipping company's
    # lessons under "cement and heavy industrial" because both are capital-intensive would
    # be the superstition this register warns about.
    "marine logistics and shipping, chartered fleet on global day rates",
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
CEM = "cement and heavy industrial"
SHIP = "marine logistics and shipping, chartered fleet on global day rates"

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
      "superseded edition for a check to open."),
    L("L-068", "ALL", None,
      "What a process commits decides what can ever be asked of it "
      "later.",
      "A record answers the question it was built for. Anything else "
      "you later want to know has to have been written down at the "
      "time, and if it was not, it is usually gone rather than merely "
      "inconvenient. When you design what a piece of work leaves "
      "behind, spend a moment asking what a DIFFERENT question would "
      "need from it.",
      "method reassessment WS6, valuation-input census, 03-Sep-2026",
      "self_audit",
      "Five fundamental walk-forwards each scored their drivers "
      "properly and committed an income statement. When the valuation "
      "calibration came to rebuild a fair value at a past origin, a "
      "census of what they actually carry found NOT ONE of 55 name- "
      "origin cells with a complete enterprise-to-equity bridge and a "
      "capital-expenditure figure: cash on 25% of cells, debt on 60%, "
      "working capital on 27%, a footed share count on 16%, capex on "
      "none. Three cells (TMGH 2020-2022) allow capex to be derived "
      "by the identity capex = dPPE + D&A; five more (PHDC 2015-2019) "
      "carry the bridge and no route to capex at all. Every missing "
      "item sits on a balance sheet or cash-flow statement in filings "
      "those runs had already opened and parsed cell by cell, so "
      "carrying them out would have been a copy rather than new "
      "research.",
      "A run that commits the block and then finds nobody ever asks "
      "for it — if several names carry cash, debt, capex and a share "
      "count through a full cycle and no later question needs them, "
      "the cost was real and the benefit was not, and the block "
      "should shrink to what was used."),

    L("L-069", "ALL", None,
      "An instrument whose bias points the same way as the hypothesis "
      "cannot test it.",
      "If the thing you are measuring with leans in the same "
      "direction as the thing you are trying to prove, a confirming "
      "answer means nothing — the instrument would have produced it "
      "whatever the truth was. Worse than a big known bias is one "
      "that changes direction from case to case, because that cannot "
      "be corrected, disclosed as a direction, or reasoned around.",
      "method reassessment WS6, valuation-input census, 03-Sep-2026",
      "self_audit",
      "The reassessment tests whether this house leans pessimistic. "
      "Two mechanical valuation lenses were declared to measure it "
      "and both were shaped by what happened to be committed rather "
      "than by the class rule: omitting cash UNDERSTATES equity "
      "value, omitting capex OVERSTATES it, and omitting working "
      "capital does either depending on growth — so a value assembled "
      "from whatever a cell carries has a bias whose sign is set by "
      "which items that cell is missing. On AMOC, a net-cash company, "
      "the omitted cash is most of the answer. The second declaration "
      "knew it was a floor and said so; what it did not say is that a "
      "floor cannot measure a pessimism lean.",
      "A demonstration that the omissions are small relative to value "
      "on a given name — a company with no debt, no material cash and "
      "no reinvestment — in which case a mechanical value on that "
      "name is honest and this caution is too strict there. The test "
      "is arithmetic and available."),

    L("L-070", "ALL", None,
      "An alternative must go through the same bridge as the number "
      "it is compared with.",
      "When a study prices a choice 'the other way', the two figures "
      "have to be built the same way apart from the choice itself. If "
      "the alternative runs through an older or simpler bridge, the "
      "difference between them measures the bridge as much as the "
      "choice — and it will usually look bigger than it is.",
      "method reassessment WS8, AMOC output records, 03-Sep-2026",
      "self_audit",
      "AMOC's helper for contested choices deducts the minority as a "
      "share of ENTERPRISE value and omits provisions, the dividend "
      "payable and investments; the delivered bridge deducts a share "
      "of EQUITY value and carries all three lines. Same enterprise "
      "value, EGP 10.3528 against the delivered EGP 9.9142. Compared "
      "against the delivered headline, three of four contested "
      "choices clear the 5%-of-value materiality line; compared like "
      "for like, one does. A sign test on the first basis would have "
      "counted three material judgements where there is one.",
      "A case where the simpler construction is the one a reader "
      "receives — then it is the headline that is inconsistent with "
      "the alternatives, not the other way round, and the fix runs in "
      "the opposite direction."),

    L("L-071", "ALL", None,
      "A rule enforced on the record is not enforced on the document.",
      "It is much easier to check a machine-readable record than the "
      "report a reader actually opens, so that is where checks get "
      "written — and the record can be brought into line while the "
      "document goes on saying the old thing. When a rule governs "
      "what a reader is TOLD, the check has to read what the reader "
      "receives.",
      "method reassessment WS8, lens vocabulary in delivered "
      "documents, 03-Sep-2026",
      "self_audit",
      "[R-LENS-03] retired the typed multi-lens blend and is enforced "
      "on each study's committed lens record, which was green "
      "everywhere. Reading the delivered PDFs instead: 6 of 20 "
      "carried no weighted blend and 14 published a weighted central "
      "as the study's own answer. ARCC had been RE-ISSUED after the "
      "rule and its document prints a weighted central of 54.65 "
      "beside a numbers file carrying 53.46. ADNOCLS, the model "
      "report every study is opened beside, carried twenty-two such "
      "assertions — so the exemplar was teaching the retired "
      "architecture to every study that followed.",
      "A rule whose whole content IS the record — a provenance field, "
      "a stamp, an attestation — has nothing in the document to "
      "check, and reading the document for it would find nothing. The "
      "test is whether the rule governs what a reader is told."),

    L("L-072", "ALL", None,
      "A forecast that reverses what the company has just filed is a claim, "
      "and it is named, sourced and measured or it is not made.",
      "A model that quietly walks a rate back toward a longer average looks "
      "prudent and is not: it is a forecast of reversion that nobody wrote "
      "down and nobody can check. Where the forecast opens materially below "
      "the latest reviewed period, the mechanism is named from a closed list, "
      "the disclosure that establishes it is carried from the filings, and "
      "the direction is MEASURED in the company's own like-for-like period "
      "pair.",
      "the AMOC, EGCH and ARCC re-strikes of 03-Sep-2026, on the principal's "
      "lead",
      "build",
      "The rule had been in both governing documents since 07-Aug-2026 and on "
      "one day three studies in one market violated it in three costumes, "
      "every one lowering the value. AMOC forecast a 9.494% gross margin "
      "falling to 8.764% against a filed half of 12.428% — an implied second "
      "half of 6.56% — on an unsourced real cost drift of +2.7 points a year "
      "that contradicted its own registered principle; worth +19.4% when "
      "corrected. EGCH forecast 45.66% falling to 33.02% on one typed array "
      "carrying the dollar export price down 17%, source layer 'Constructed'. "
      "ARCC opened at 39.03% against a filed peak of 39.25% and told no "
      "reader it sat at the top of its own range. [L-048] had been registered "
      "after the first occurrence, was correct, and bound nothing.",
      "A study whose forecast opens materially below its latest reviewed "
      "period, names a mechanism from the closed list, carries the "
      "disclosure, shows the like-for-like direction agreeing — and is still "
      "wrong when the period matures. That would say the mechanism test is "
      "satisfiable without being informative."),

    L("L-073", "ALL", None,
      "A driver out of line with the rest of the book usually means our "
      "method slipped on this one name, not that the company is unusual.",
      "The strongest test of a contested driver is not whether it can be "
      "argued for on its own name — almost any of them can — but whether the "
      "same house builds the same class of input the same way everywhere "
      "else. Where two studies carry opposite conventions for the same kind "
      "of number, one of them is wrong and the disagreement says which "
      "question to ask.",
      "EGCH's dollar export price against AMOC's dollar feedstock price, "
      "03-Sep-2026",
      "build",
      "EGCH carried a typed dollar output price falling 17% over five years "
      "with no marginal cash cost quoted and no institution publishing it, "
      "while AMOC — same house, same market, same week — held its dollar "
      "commodity price FLAT and registered the reason in as many words: 'no "
      "forecast of it is defensible'. Neither study was checked against the "
      "other; the inconsistency was invisible from inside either one, and it "
      "ran the value-destroying way in the study that had it. Separately, "
      "EGCH published the RATING equity-risk-premium basis as its central "
      "where [R-COC-01] names the CDS basis by default and both peer "
      "Egyptian studies use it — a 13.94% premium against 9.41% for the same "
      "sovereign on the same day, again the higher one.",
      "A case where a name genuinely does deserve a different convention "
      "from its book, established from that company's own disclosures rather "
      "than from the analyst's judgement. Then the rule is to name the "
      "difference, not to conform."),

    L("L-074", "ALL", None,
      "A self-attested string is not a check, however carefully it is worded.",
      "Where a gate reads a sentence a study wrote about itself, the study "
      "can write the right sentence and do the wrong thing — and the gate "
      "will pass it, repeatedly, with no sign anything is wrong. Where the "
      "claim can be reduced to arithmetic, reduce it: commit the number and "
      "the ingredients that would reproduce the thing it is claimed not to "
      "be, and divide.",
      "the AMOC relative lens, exposed by the 03-Sep-2026 re-strike",
      "self_audit",
      "AMOC's lens record attested 'enterprise value to EBITDA from the "
      "company's own history and its regional peers, never a multiple read "
      "off the current price' while its code computed (market cap + net "
      "debt) / base-year EBITDA re-rated by zero — the traded multiple "
      "exactly. assert_lens_design searched the prose for phrases meaning "
      "'from the price', found the reassuring words, and passed it three "
      "times. What exposed it was moving the price: the spot rose 48.4% and "
      "the lens rose 51.3%, which a lens built on five years of own history "
      "cannot do. The gate now requires the adopted multiple and the three "
      "numbers that reproduce the traded one, and refuses when they agree to "
      "within half a per cent.",
      "A relative multiple whose circularity ingredients cannot be committed "
      "because the metric genuinely has no traded counterpart. Then the "
      "arithmetic form is unavailable and the prose test is the only one "
      "left — which is an argument for withdrawing the lens, not for "
      "trusting the sentence."),

    L("L-075", "ALL", None,
      "A fix that enumerates the keys it knows about is a fix that expires.",
      "Carry-over lists, allow-lists and key-lists written when they were "
      "complete go stale the moment anything is added, and they fail "
      "silently — the new thing is simply dropped. Invert them wherever the "
      "inversion is expressible: carry everything the module does not itself "
      "produce, rather than everything somebody remembered.",
      "EGCH's build order, 03-Sep-2026",
      "build",
      "compute.py is imported by alternatives.py, which re-runs it and "
      "rewrites study_numbers.json. A carry-over had been written for that "
      "exact hazard and named ('central', 'fair'), which was complete when "
      "written. lenses.py has since added central_two_sided, lens_record, "
      "macro_record and bridge_record — the records [R-LENS-03], "
      "[R-MACRO-01] and [R-BRIDGE-01] are checked from outside on — and all "
      "four were silently dropped on every build. Three repo gates went red "
      "at once and the study read, from outside, like one that had never "
      "committed a record at all.",
      "A module where carrying everything unknown is wrong because a stale "
      "key must be actively cleared. Then the inversion needs an explicit "
      "expiry list, which is the same hazard in the other direction and has "
      "to be checked rather than remembered."),


    L("L-076", "ALL", None,
      "An artefact every builder reads and nothing writes is a number frozen at "
      "the date somebody last typed it.",
      "It will not announce itself, it survives every rebuild, and it wears the "
      "appearance of a computed record while being a memory. Where a file feeds "
      "a document, ask what WRITES it — and if the answer is nothing, that is "
      "the defect, before any question of whether its numbers are right.",
      "AMOC, ARCC, EGCH and PHDC, four outside audits on 03-Sep-2026",
      "critique",
      "Three separate artefacts with no generator anywhere in the repository "
      "were found in one day. AMOC's case_adversarial.json was read by THREE "
      "builders and written by none; it froze at a base central of 5.954 and "
      "drove Table 7, Table 18, Figure 4 and the opening paragraph through two "
      "editions, telling a reader that conceding every contested charge reached "
      "EGP 7.47 — below the published 11.834, which is impossible, because every "
      "charge conceded raises the value. PHDC's diagnostics.json was the same "
      "shape and froze at a spot of 15.20 through a re-strike to 14.40. ARCC's "
      "efg_bridge caption was typed from a superseded model. None was visible to "
      "any gate, because every gate reads study_numbers.json and none of these "
      "files is in it.",
      "An artefact with no generator that nonetheless stays current across "
      "several editions — which would mean something else is keeping it so, and "
      "that thing is the generator by another name."),

    L("L-077", "ALL", None,
      "A default on a key that is never present is not a default. It is a second "
      "answer with no label.",
      "A dict lookup with a fallback reads as defensive, and it is — right up to "
      "the moment the key is absent EVERY time, when it silently becomes the only "
      "code path and nothing says so. Prefer a lookup that raises, or derive the "
      "value from something the same output already publishes so the two cannot "
      "disagree.",
      "PHDC's cash-flow waterfall, 03-Sep-2026",
      "critique",
      "The row headed 'Cost of capital, that year' read "
      "w.get('forward_wacc', wacc) on each waterfall row. forward_wacc sits on "
      "the CASE, not on a row, so the fallback fired in every column and printed "
      "a flat 25.1% above a row of gliding discount factors it cannot produce. "
      "Compounding the printed rate gives 0.639 for 2027 against a published "
      "0.656 and 0.039 for 2040 against 0.090 — 2.3 times out by year fifteen, in "
      "a table headed 'with nothing collapsed'. The workbook was right throughout. "
      "The fix was not a better default: the rate is now DERIVED from the "
      "discount factors the same table publishes.",
      "A case where the fallback is genuinely the intended path for some rows and "
      "the named key for others. Then the two paths need different labels in the "
      "output, not one silent branch."),

    L("L-078", "ALL", None,
      "A guard that cannot fail is worse than no guard, because it is counted as "
      "one.",
      "Before writing an assertion, ask what value of the input would make it "
      "raise. If the answer is none, the assertion is decoration standing where a "
      "check should be — and it will be trusted by everyone who reads the code "
      "afterwards.",
      "AMOC's probability zones, 03-Sep-2026",
      "critique",
      "Five zone probabilities were built as consecutive differences of a "
      "cumulative distribution and guarded by 'assert the zones sum to one'. "
      "CONSECUTIVE DIFFERENCES OF A CUMULATIVE FUNCTION TELESCOPE, so that sum is "
      "1.0 for ANY ordering of the cuts, ascending or not. The cuts were not "
      "ascending, two zones were NEGATIVE, and the table shipped -74.6% and "
      "-16.0% under a caption promising a genuine partition. The guard had been "
      "there the whole time and could never have caught it.",
      "A guard whose failure condition is unreachable in this code path but "
      "reachable in another that shares the function — then it is a real check "
      "for the other caller and should say which."),

    L("L-079", "ALL", None,
      "Write a correction OVER the sentence it corrects, not beneath it.",
      "Adding the new statement under the old one leaves a document asserting "
      "both, and the reader has no way to tell which is current. It happens "
      "because the correction feels safer as an addition — nothing is lost — and "
      "that is exactly what makes it dangerous.",
      "AMOC §1.2, 03-Sep-2026",
      "critique",
      "One paragraph read 'HALF OF THIS BASE YEAR IS A PRESS RELEASE AND NOT A "
      "FILING'; the paragraph four lines below it read 'THE HALF IS FILED, AND "
      "THE RELEASED GROSS PROFIT WAS RIGHT'. Both were true of successive "
      "editions and only one was true of this one. A table cell in between still "
      "gave the basis as 'second half SOLVED' while the model used the filed "
      "figure, and the caveat list still called the base year 'half press "
      "release' — so the same page carried a superseded claim three times over "
      "beside its own correction.",
      "A document that deliberately publishes both the old and the new reading "
      "for a reader of the previous edition — which is legitimate, and is why "
      "the retired blend is published labelled RETIRED rather than deleted. The "
      "test is whether the old statement is marked as superseded."),

    L("L-080", "ALL", None,
      "A check that reads what a process DECLARES is not checking what the process does.",
      "Every exemption in a gate is a place where the gate stops looking. A TRUE "
      "exemption on the WRONG OBJECT is the safest hiding place there is: nobody is "
      "lying, the reason survives review, and the work happens somewhere the check "
      "does not reach. Where a rule governs a quantity, hold the quantity — holding "
      "the study's description of where the quantity lives is one indirection too many.",
      "EGCH cpi_path, 03-Sep-2026",
      "build",
      "EGCH declared its one growth line exempt from the house inflation path on "
      "grounds that were perfectly true — its revenue is built from tonnes and dollar "
      "prices, so no nominal growth rate sat on that line. Meanwhile an input named "
      "nowhere in the record, cpi_path = 10.0 / 7.0 / 6.0 / 5.0 / 5.0 against a house "
      "ladder of 16.0 / 12.0 / 9.0 / 7.5 / 7.0, drove the purchasing-power wedge and "
      "therefore the whole currency path — so both the pound value of dollar revenue "
      "and the gas cost — and escalated other materials, wages, services and the "
      "terminal tonne's conversion cost. It terminated at 5% while the same record "
      "carried the house terminal of 7%. The study's own gap review named it in plain "
      "words, 'the study's own Egyptian inflation path', inside the heading whose "
      "purpose is to catch it, and passed.",
      "A gate that holds the declared object and the used object and finds them "
      "always identical across a large book — which would mean the indirection is "
      "harmless in practice and the extra clause is cost without benefit."),

    L("L-081", "ALL", None,
      "A list of forbidden words cannot be complete; match the shapes that cannot occur innocently.",
      "Where a prohibition can be expressed as a SHAPE rather than a vocabulary, express "
      "it as a shape. A word list is maintained by whoever last thought of a word, so "
      "every copy of it has a different hole, and the holes are invisible until something "
      "falls through one.",
      "EGCH and AMOC bibliographies, 03-Sep-2026",
      "build",
      "Depth-bar standard 4 is implemented by each study as its own list of forbidden "
      "terms — 39 in ARCC, 68 in EGCH, a different set in AMOC. EGCH's delivered "
      "bibliography shipped two standing-rule identifiers and a repository path out of "
      "an input register's source field while its own scrub reported ZERO hits across "
      "68 patterns; AMOC's scrub, which happens to carry both shapes, caught the "
      "identical sentence the same hour. A sweep of the book found three more delivered "
      "documents leaking through three different holes.",
      "A shape that turns out to occur innocently in a document written for an outside "
      "reader — which would mean the shape was the wrong instrument and a word list, "
      "with its judgement about ordinary senses, was right after all."),

    L("L-082", "ALL", None,
      "A correction that moves the answer away from the price is not a reason to reconsider the correction.",
      "The temptation runs the other way from the one everyone guards against. A "
      "correction that closes a gap feels confirmed by the closing, and one that widens "
      "it invites a second look at the correction rather than at the model. Both "
      "instincts are the same error: the price is evidence about where to LOOK, never "
      "evidence about what the answer is.",
      "AMOC inflation ladder, 03-Sep-2026",
      "build",
      "Conforming AMOC's cost ladder to the house path was expected to RAISE the value: "
      "the study's own ladder compounded higher, 1.7385 against 1.6288 over five "
      "forecast years, so the cost side alone said the value would rise. It fell, EGP "
      "11.83 to 11.40, from -12.3% to -15.5% against the price, because the currency "
      "path is derived from the same ladder by purchasing-power parity — a lower ladder "
      "means a stronger pound, and on a dollar-linked slate the translation gain lost "
      "outweighs the pound costs saved. The direction was not predictable from the sign "
      "of the input error.",
      "A case where re-examining a correction that widened a gap uncovers a real defect "
      "in the correction itself — which is why the instinct exists and why the rule is "
      "about not letting the DIRECTION be the trigger, rather than about never looking."),

    L("L-083", "ALL", None,
      "A value patched into a generated artefact is lost at the next generation.",
      "The patch works, the gate goes green, and the obligation to move it into the "
      "generator becomes a thing somebody has to remember. Nobody does, and the loss "
      "surfaces hours or weeks later as a gate failing on work that looked finished.",
      "TMGH range_basis, 03-Sep-2026",
      "build",
      "The commit that adopted the range_basis requirement wrote the block straight into "
      "engine/tmgh_study/study_numbers.json and never into build_numbers.py. The next "
      "honest rebuild of that study — triggered by an unrelated amendment the same day — "
      "dropped it, and the lens-design gate went red on a study that had been conforming "
      "eight hours earlier. This is L-067's cousin: that one was a check pinned to a "
      "filename, this one is a value pinned to a file.",
      "A generated artefact that legitimately cannot be produced by its generator — a "
      "figure only a person can supply — in which case the honest form is an input the "
      "generator READS, not a patch to its output."),

    L("L-084", "ALL", None,
      "A process that validates itself validates the list its author thought of.",
      "Local checks fail by imagination, not by care. A careful author writes careful "
      "assertions about everything they can think of, and the gap is precisely the set of "
      "things they could not — which no amount of further care inside the same process "
      "will supply, because what is missing is a list written somewhere else. This is why "
      "a shared instrument beats a good local one even when the local one is better "
      "written.",
      "ARCC sweep.py, 03-Sep-2026",
      "build",
      "ARCC was the only study in the book that hand-rolled its Step 2A sweep instead of "
      "importing engine/research_sweep.py. Its own assertions checked five things — every "
      "finding has a source, a date and a model impact; the class is one of four; all four "
      "rings appear; ids are unique; driver cross-references resolve — and all five passed. "
      "Replaying the same 26 findings through the shared register's validate() produced "
      "SEVEN errors, and five were facts the study already held: a company website "
      "attempted and refused, an investor presentation cited by page for six drivers, the "
      "reviewed half the bridge stands on, and three top-down drivers whose evidenced "
      "absence sat in prose inside their own justification.",
      "A study whose local checks turn out to be a strict superset of the shared "
      "instrument's — which would mean the shared module is the weaker one and should "
      "adopt the local checks, not the other way round."),

    L("L-085", "ALL", None,
      "A rule that one study implements is a rule that one study obeys.",
      "A correct rule, written down and implemented well in the one place it exists, "
      "binds nothing anywhere else. The instinct is to port the implementation study by "
      "study; the cost of that is one hand-maintained copy per study, each with its own "
      "hole. Make it arithmetic ONCE, in a shared place, and the rule survives everywhere "
      "rather than in the place somebody remembered.",
      "prose_check across the book, 03-Sep-2026",
      "build",
      "\"A number stated in prose must be computed, not typed\" had been standing for four "
      "weeks and exactly one study of twenty-four implemented a check for it. Measured in "
      "one afternoon on three studies that had just been rebuilt and passed every other "
      "gate: AMOC published a 514-basis-point margin range whose own five named periods "
      "span 737, alongside a summary row that summed five values and divided by four; ARCC "
      "shipped a masthead a day stale and a price date a month stale; PHDC carried three "
      "comments above one line, two of them wrong. Across the whole book, 373 of 8,824 "
      "figures in the delivered documents had no computed counterpart. Shared as "
      "engine/prose_figures.py rather than copied twenty-three times, and the first four "
      "ports reached zero unmatched across 1,561 figures.",
      "A rule whose right implementation is genuinely study-specific — where a shared "
      "instrument would have to be so configurable that each study's declaration IS the "
      "implementation, at which point the sharing buys nothing but a common vocabulary."),

    L("L-086", "ALL", None,
      "A system of checks has properties no check in it can see.",
      "Each gate can be individually right, individually negative-controlled, and "
      "collectively unable to answer the one question that matters about the set: can a "
      "new subject walk past all of them? Where a claim about the SYSTEM can be expressed "
      "as a test, write the test — it runs over the system rather than inside it, and it "
      "fails rather than warns.",
      "the new-study gauntlet, 03-Sep-2026",
      "build",
      "Every ratcheted gate in this repository states that the build breaks on a NEW "
      "violation, and every one is negative-controlled. Planting an empty study directory "
      "and running the set found that four of seventeen stayed green — three legitimately, "
      "because they bite on artefacts rather than on the directory, and one on a real hole: "
      "check_artefact_currency skipped every two-sided study behind a comment claiming the "
      "branches were handled when nothing handled them, and EGCH's contested-judgements "
      "artefact sat stale at 1.7854 against a published 2.3109 for a full day.",
      "A system-level property that turns out to be unfalsifiable in practice — where "
      "every way of weakening the system to test the property is so artificial that its "
      "failure teaches nothing about the real risk."),

    L("L-087", "ALL", None,
      "A comment asserting a check that does not exist is worse than no comment.",
      "It stops the next reader looking. An absent check invites the question; a comment "
      "claiming the check is elsewhere answers it wrongly and closes it. This is the "
      "documentation form of a self-attested boolean.",
      "check_artefact_currency, 03-Sep-2026",
      "build",
      "The gate skipped any study whose central was not a scalar, with the inline comment "
      "'a two-sided study; handled by its branches'. Nothing in the file handled branches — "
      "the word appeared exactly once in it, in that comment. EGCH publishes a two-sided "
      "answer and therefore escaped the gate entirely, and its contested_judgements.json "
      "was stale by 29% for the whole day the gate reported clean.",
      "A comment that names the module or function actually performing the check, which is "
      "a pointer rather than an assertion and can be verified by following it."),
    L("L-088", "ALL", None,
      "A formula right in real terms and wrong in nominal terms passes every arithmetic "
      "check that will ever be written.",
      "Nothing in it is arithmetically wrong, so recalculation, provenance, source "
      "discipline and four-field registers all come back clean. Where a quantity carries a "
      "unit — real or nominal, this year's money or that year's — the unit is the thing to "
      "check, and no amount of care inside the arithmetic will supply it.",
      "[R-TERM-01], method reassessment, 03-Sep-2026",
      "build",
      "ARCC's terminal charged the reinvestment identity rr = g/ROIC with a NOMINAL g whose "
      "real component was zero, so it levied g x IC = EGP 3,583.4mn a year for ever, 62.2% "
      "of terminal profit, to buy nothing. It survived four revisions, a cell-by-cell "
      "recalculation with zero disagreements, a conforming beta attestation, all eight "
      "depth-bar standards and a clean external-reader scrub. Correcting it moved the "
      "central from EGP 53.21 to 66.53.",
      "A case where a real/nominal mismatch is caught by an ordinary arithmetic or "
      "provenance check rather than by someone asking what unit a quantity is in."),

    L("L-089", "ALL", None,
      "An inflation rate that has quietly become an asset life will not announce itself, "
      "because both are just numbers.",
      "Read a perpetual capital charge as a replacement programme and ask how many years it "
      "implies. Where the charge is growth times invested capital the answer is one over "
      "the growth rate — a fact about the currency rather than about the plant, and one that "
      "gets worse the higher inflation goes, which is the exact opposite of prudence.",
      "[R-TERM-01], method reassessment, 03-Sep-2026",
      "build",
      "ARCC's terminal implied replacing its entire replacement-cost asset base every 14.3 "
      "years, against 1/g of 14.3 to the decimal. Three implied lives sat inside the one "
      "model and disagreed by 2.8x — the terminal's 14.3, the explicit window's own capex at "
      "40.2, and the DISCLOSED 20 from the audited accounting-policies note. The sourced "
      "figure sat between the model's own two conventions.",
      "A company contractually obliged to spend at that rate — a concession condition, a "
      "licence commitment or a take-or-pay — in which case the charge is real and the "
      "implied life is beside the point."),

    L("L-090", "ALL", None,
      "When a gate fires on work that is right, the answer is almost never to widen it — and "
      "that applies to a gate this desk wrote an hour earlier.",
      "Widening a bound is a free parameter and moving the number to satisfy it corrupts the "
      "thing being measured. The third option — establish that the check is pointed at the "
      "WRONG MEASUREMENT and re-point it — is more work and is the only one that leaves the "
      "check stronger than it found it.",
      "[R-TERM-01] and [R-COC-01], 03-Sep-2026",
      "build",
      "terminal_value.py first refused any terminal below NOPAT/W. ARCC's own beta "
      "sensitivity grid broke it: TV/floor tends to FCFF(1+g)/NOPAT = 0.658, below one by "
      "construction whenever maintenance exceeds book depreciation, so it fired on a sound "
      "terminal. AND IT WAS WRONG IN THE SAME WAY AS THE DEFECT IT WAS BUILT TO CATCH — it "
      "treated book depreciation as the cash cost of replacement. Re-pointed at the claim "
      "that survives: a company is never obliged to spend GROWTH capital.",
      "A case where widening a bound, rather than re-pointing it, left the check "
      "demonstrably stronger."),

    L("L-091", "ALL", None,
      "A hard-coded zero is a defect in mirror image, and it is how a corrected defect comes "
      "back.",
      "Writing a quantity as a literal because it happens to be zero today removes the "
      "mechanism that makes it non-zero tomorrow. The model and the artefact then disagree "
      "about BEHAVIOUR rather than about a value, which no check on levels can see.",
      "[R-TERM-01], ARCC workbook rebuild, 03-Sep-2026",
      "build",
      "The rebuilt workbook wrote terminal REAL growth as a literal 0.0, so bumping the "
      "terminal growth cell raised the value while the model lowered it: the workbook said "
      "growth was FREE. Every level reconciled — 919 of 919 formula cells reproduced the "
      "model — and only the driver test, which perturbs inputs and checks DIRECTIONS, caught "
      "it.",
      "A directional disagreement between a model and its workbook that a level-by-level "
      "reconciliation does catch."),

    L("L-092", "ALL", None,
      "A review that reaches a confident wrong conclusion is more dangerous than no review.",
      "It closes the question. The way it happens is not carelessness: the review looks for "
      "the error everywhere the arithmetic could be wrong, the arithmetic is not wrong, and "
      "it concludes the disagreement must lie outside the model.",
      "[R-GAP-01] and [R-TERM-01], ARCC, 03-Sep-2026",
      "build",
      "ARCC's revision-4 gap review audited a central of 53.21 at -30.9% and concluded in "
      "terms that 'the disagreement with the market is therefore not about the business at "
      "all', locating the whole gap in a cost of capital the market was applying 816bp below "
      "the Egyptian sovereign. The defect was in the terminal, which carried 41% of "
      "enterprise value and which the review did not examine. Its own MULTIPLE CROSS-CHECK "
      "heading would have shown it: 3.1x forward EBITDA and USD 78 per annual tonne against "
      "a replacement cost of USD 130.",
      "A gap review that reaches a wrong conclusion and is caught by the next reader as "
      "quickly as an absent review would have been."),

    L("L-093", "ALL", None,
      "A filing is not read until the notes that bear on the model are read.",
      "Parsing a filing for its statements and treating it as read is the statement-level "
      "form of the unread-filing defect. The accounting policies carry useful lives, "
      "recognition clocks and definitions that decide constructions the numbers alone cannot "
      "settle.",
      "[R-TERM-01], ARCC, 03-Sep-2026",
      "build",
      "ARCC's FY2025 filing had been parsed cell by cell for its statements across four "
      "revisions. Its accounting-policies note discloses machinery and equipment at 20 "
      "years, and that figure is what the terminal turned on — worth EGP 13.32 a share. The "
      "note had never been opened, and the filing carries no text layer at all, so reading "
      "it took OCR off the rendered pixels.",
      "A study where the accounting-policies note bears on no construction in the model — in "
      "which case it is not needed, and the record should say so rather than leave the note "
      "unopened."),
    L("L-094", "ALL", None,
      "EVERY NOMINAL LINE IS UNDER-FORECAST ON EVERY NAME. That is the house bias, and it "
      "is about scale rather than about margin.",
      "Revenue, cost of sales, operating expense, tax, finance income and provisions all "
      "come in ABOVE forecast, with the same sign on all five names measured. Nothing about "
      "any single line looks careless; what is systematic is that the whole nominal scale of "
      "the business is set too low, which is a growth-path error rather than a base-year one.",
      "engine/valuation_calibration/systemic_bias.py, 03-Sep-2026",
      "walk_forward_fundamental",
      "Pooled by-driver bias across all five completed runs: revenue -0.316, cost of sales "
      "-0.335, operating expense -0.272, tax -1.023, finance income -0.818, provisions "
      "-0.656 — every one negative on every name that reports it. At cell level on the two "
      "runs that commit cells the error COMPOUNDS with horizon (revenue -0.023 at one year "
      "to -0.348 at five), with an intercept near zero, which is the signature of a rate "
      "error and not a level error.",
      "A name whose nominal lines are over-forecast, or a horizon profile that is flat "
      "rather than compounding, either of which would move this from a growth-path finding "
      "to a base-year one."),

    L("L-094a", "ALL", None,
      "A finding measured on whichever names happened to have the data is not a sample of "
      "the book, and it will read like one.",
      "The subset was not CHOSEN, which is exactly what makes it feel like a random draw. "
      "It is not: whatever determined which runs committed their raw cells may well "
      "correlate with the thing being measured, and here it did — the two runs holding cells "
      "were both developers.",
      "engine/valuation_calibration/systemic_bias.py, 03-Sep-2026",
      "build",
      "The cell-level pool said PROFIT was forecast at +0.8084, x2.24 of actual, too high in "
      "89% of 867 cells, on both names that commit cells — and it was reported as a HOUSE "
      "finding. Pooled across all five runs' aggregates it is -0.3424 and only 3 of 12 "
      "bottom-line drivers are too high: the two DEVELOPERS forecast profit far too high "
      "(PHDC +1.107, TMGH +0.264) and the three INDUSTRIALS far too LOW (AMOC -0.943, EGCH "
      "-0.774, ARCC -0.422). The claim was true of the subset and false of the book, and it "
      "was corrected within the hour by reading the aggregates the other three DO commit.",
      "A case where the names holding the richer data are demonstrably unrelated to the "
      "quantity under measurement — in which case the subset is a sample and may be treated "
      "as one, once that is shown rather than assumed."),

    L("L-095", "ALL", None,
      "A forecast can under-forecast revenue AND under-forecast cost and still be "
      "optimistic, because the margin is the difference.",
      "Small errors in the same direction on two large lines do not cancel — they compound "
      "into the residual between them. Checking that revenue and cost are each roughly right "
      "is not the same as checking the margin, and the margin is what the value rests on.",
      "engine/valuation_calibration/systemic_bias.py, 03-Sep-2026",
      "walk_forward_fundamental",
      "Revenue pools at -0.2243 (x0.80 of actual) and cost of sales at -0.1309 (x0.88) — "
      "both UNDER-forecast, which reads as conservative on each line taken alone. Because "
      "revenue is under-forecast by MORE, the forecast gross margin comes out too wide and "
      "gross profit pools at +0.2303. Finance cost at -1.1465 then carries the net line to "
      "+0.8084.",
      "A case where two same-signed line biases of unequal size leave the margin unbiased."),

    L("L-096", "ALL", None,
      "The runs recorded their scores and not their observations, so a question about which "
      "LINES are biased could be answered on two names out of five.",
      "This is the amendment about valuation inputs arriving a second time, one layer along. "
      "The cells cost nothing to keep; they were simply not asked for, and nobody noticed "
      "the missing field until the question arrived.",
      "[R-FCAL-01 AMENDED], 03-Sep-2026",
      "build",
      "AMOC, ARCC and EGCH commit bias, MAE, over-share and bootstrap intervals by driver, "
      "horizon and era — and not the per-cell projected-versus-actual pairs those were "
      "computed from. PHDC and TMGH commit 403 and 1,856 cells. So the line-level systemic "
      "bias analysis rests on two names, and the three that would have told us whether it "
      "generalises cannot.",
      "A pooled statistic from which the underlying cells can be recovered exactly, which "
      "would make committing them redundant."),
    L("L-097", "ALL", None,
      "A defect whose direction depends on a market parameter will look like a house bias in "
      "whichever market you happen to be looking at.",
      "The complaint can be entirely true and its attribution entirely wrong. Only a census "
      "across markets separates the two, and correcting from the direction of the complaint "
      "alone gets the sign right on the names that prompted it and wrong everywhere else.",
      "engine/valuation_calibration/terminal_census.py, 03-Sep-2026",
      "build",
      "The retired terminal implied a replacement cycle of 1/g, so it over-charged where "
      "terminal inflation was high and UNDER-charged where it was low. Across the eleven "
      "studies carrying it, the implied life ran from 14.3 years (AMOC, 7% terminal "
      "inflation) to 66.7 (ADNOCDIST, 1.5%). Priced on a 30-year asset life, three names "
      "RISE and eight FALL, median -5.8% of enterprise value: it raises the Egyptian names "
      "the pessimism complaint came from and lowers the Gulf names, whose low terminal "
      "inflations bought them a forty- to sixty-seven-year replacement cycle no "
      "accounting-policies note supports.",
      "A market parameter whose variation across the book is too small for the direction of "
      "a defect to flip — in which case a one-market diagnosis does generalise."),

    L("L-098", "ALL", None,
      "Rule candidates OUT by arithmetic before naming what is left. A gap review that lists "
      "unresolved items without pricing them tells a reader nothing about which one matters.",
      "Every study has open items and their existence is not evidence that they explain "
      "anything. Price each at a generous bound: what survives is the answer, and what does "
      "not is removed from the reader's attention rather than left to worry them.",
      "EGCH gap review, 03-Sep-2026",
      "build",
      "EGCH's review named three unresolved items behind an 88% gap. Priced: the two "
      "book-carried non-operating assets are 77% of the equity value and so the most "
      "leveraged items in the bridge, yet closing the gap on them alone needs them at 7.8x "
      "carrying value — at a generous 2x they move the answer EGP 1.78 against a gap of EGP "
      "12.10. The ANNA programme, which the whole study is architected around as a binary "
      "judgement, carries the answer from 2.31 to only 3.06 as its margin runs from 1.93% to "
      "40%. The terminal charge is near value-neutral. All three ruled out; the gap is the "
      "cost of capital, and the enterprise value stands at 2.25x terminal EBIT against a "
      "market paying 7.13x.",
      "A review where the unresolved items, priced at generous bounds, DO span the gap — in "
      "which case listing them was the right answer and pricing them proves it."),

    L("L-099", "ALL", None,
      "A DELIVERED TABLE MUST FOOT FOR THE READER, NOT ONLY FOR THE MODEL. Where a table "
      "prints components and a total, the total must be reproducible from the rows printed.",
      "A recalculation gate reconciles a model TO ITSELF, so a correct model passes however "
      "wrong the page is. A per-figure check matches each number against the model and "
      "passes when every figure is individually right. The defect lives in the RELATIONSHIP "
      "BETWEEN figures, and nothing that inspects figures one at a time can see it.",
      "ARCC 03-Sep-2026, reading the rendered PDF page by page",
      "build",
      "Three tables in one delivered study, all after 919 of 919 formula cells reconciled "
      "and 533 prose figures matched with none unmatched. Table 3 deducted provisions and "
      "credit losses in the model and did not print the line, so a reader adding the printed "
      "rows came out EGP 82mn above the printed EBITDA. Table 5 printed four CONTRACTUAL "
      "rates and labelled their blend adopted at 13.36% — the printed four weight to 7.89%, "
      "and 13.36% reproduces from a local-equivalent column the table did not carry, under a "
      "caption reading built in the model from these four lines, not pasted. Table 2 went "
      "from cement sold of 3.553Mt to total despatches of 4.854Mt with the export cement "
      "tonnage printed nowhere, and clinker is 27% of this company\'s volume. In all three "
      "the model was right and the page could not be reconciled by the reader it was written "
      "for.",
      "A study where every unreconciled total turns out to be a legitimate exception, which "
      "would mean the arithmetic form of this check earns nothing beyond what a declaration "
      "already states."),

    L("L-100", "ALL", None,
      "MEASURE A PROPOSED GATE ACROSS THE WHOLE BOOK BEFORE SETTING ITS BAR, and let the "
      "measurement decide the ARCHITECTURE and not merely the threshold.",
      "A check that fires on one table in seven is the check everyone learns to ignore, and "
      "the temptation on seeing that number is to loosen the arithmetic until it is quiet — "
      "which destroys the thing being measured. The third option is to keep the arithmetic "
      "exact and change WHO declares the exceptions.",
      "the table-footing gate, 03-Sep-2026",
      "build",
      "Run book-wide with no declarations the instrument flagged 22.3% of all tables. Two of "
      "the three causes were the instrument being WRONG about how tables work — a balance "
      "sheet foots over its subtotals rather than its leaf rows (67 tables), and a row "
      "labelled Total assets heading a summary balance sheet is a disclosed line item with "
      "nothing above it (34 tables) — and both were fixed rather than declared away, taking "
      "the rate to 16.5%. The residue is IRREDUCIBLE: a Total equity row listed AMONG line "
      "items is structurally indistinguishable from a roll-up, and so is a driver named "
      "Blended ARPU in a sensitivity grid. So the arithmetic stayed exact and the study "
      "declares its own exceptions with reasons — the prose_figures architecture, reached by "
      "measurement rather than by preference. ARCC needed three declarations and each names "
      "a real structural fact about its own table.",
      "A rule set that separates a roll-up from a list of line items by shape alone, which "
      "would make the per-study declaration unnecessary rather than merely narrower."),

    L("L-213", "ALL", None,
      "A DIRECTION WORD IS A CLAIM AND IS CHECKED AGAINST THE SIGN BESIDE IT. Compute the "
      "word, not only the number.",
      "Every figure-level gate here reconciles NUMBERS. The words around them are typed, and "
      "a typed word does not look like a figure — so a correctly computed ratio can sit "
      "beside a direction word that says the opposite and no check notices.",
      "ARCC 03-Sep-2026, reading the rendered PDF",
      "build",
      "ARCC shipped \'This model forecasts EGP 3,842mn for FY2026, +1.8% below the simple "
      "annualisation\' — the ratio computed correctly, the word saying the opposite, in the "
      "paragraph the study itself calls the sharpest challenge to its forecast. Measured "
      "across every delivered document in its latest edition, a regular expression matching "
      "a signed percentage against a contradicting direction word within three words finds "
      "ONE further instance and no false positives: MODON publishes \'AED 2.50, -12% above "
      "the market\'. Two innocent constructions fired against the first draft and taught the "
      "pattern — a TEMPORAL \'over\' (fell -2.4% over the same span) and a RANGE DASH "
      "(80-85% above the 2024 average) — so bare \'over\' is not in the upward set and a "
      "sign preceded by a digit is not a minus.",
      "A book where this pattern fires on constructions that are correct more often than on "
      "ones that are wrong, which would make it a check people learn to ignore."),

    L("L-214", "ALL", None,
      "A PART-YEAR STUB MUST SHOW ITS SCALING FACTOR ON THE PAGE. A column whose components "
      "are full-year and whose total is part-year cannot be footed by anyone.",
      "The model is right and the reader is stranded: the arithmetic fails by exactly the "
      "stub fraction, with nothing printed to explain it, and the natural inference is that "
      "the total is wrong.",
      "ARCC 03-Sep-2026, reading the rendered PDF",
      "build",
      "ARCC\'s cash-flow waterfall printed NOPAT 3,745 plus depreciation 344 less capital "
      "expenditure 890 less working capital 108 — which sums to 3,091 — against a printed "
      "free cash flow of 1,545, exactly half, because the valuation date is 30 June and only "
      "the remaining half-year is discounted. Every other column footed to the last unit. "
      "The caption compounded it by stating FIVE months not yet earned and SEVEN already "
      "earned, both typed, against a committed stub of 0.500 — six and six. The remaining "
      "fraction is now a printed row and the months are computed from the stub.",
      "A stub convention where the components are themselves pro-rated, in which case the "
      "column foots without the extra row and printing it would be noise."),

    L("L-215", "ALL", None,
      "WHEN A CONSTRUCTION IS RETIRED, ASSERT ITS INPUTS GONE FROM THE PROSE AS WELL AS FROM "
      "THE MODEL. A retirement that leaves the workbook clean and the sentences talking is a "
      "rule half-applied.",
      "Retiring a construction is a code change, and code changes are checked by code. The "
      "sentences describing it are typed, so they survive the retirement silently and go on "
      "telling a reader the model does something it stopped doing.",
      "ARCC 03-Sep-2026, reading the rendered PDF and then making it arithmetic",
      "build",
      "The typed lens blend was retired and the workbook was asserted clean of its four "
      "weight cells. SIX sentences went on quoting those weights in the present tense — the "
      "cash-flow lens \'carries half the weight\', the relative lens \'carries 20% and not "
      "more\', the asset lens \'carries only 8%\', an expert falsifier ending on \'carries "
      "only 8% of the weight\', and two comparison passages. READING THE PAGES FOUND THREE "
      "OF THE SIX; a five-line assertion driven off the retired inputs\' own committed "
      "values found all six in one run, which is the whole argument for making a lesson "
      "arithmetic. The assertion permits a weight to be NAMED where the sentence places it "
      "in a superseded edition, because saying what a previous edition did and why this one "
      "does not is the legitimate use.",
      "A retirement where the prose genuinely cannot be checked against the retired input, "
      "for instance one whose value is too common a number to match on."),

    L("L-216", "ALL", None,
      "A CHECK THAT OPENS A DELIVERED FILE MUST RESOLVE IT BY DATE, NEVER BY STRING SORT.",
      "Edition filenames carry DD-MM-YYYY, so alphabetical order is not chronological order "
      "and sorted(...)[-1] silently returns whichever name sorts last.",
      "ARCC 03-Sep-2026",
      "build",
      "The first draft of the retired-weight assertion took sorted(glob(...))[-1] and opened "
      "the superseded 08-08-2026 edition, because \'08-08-2026\' sorts above \'03-09-2026\'. "
      "It reported that edition\'s defects as current and would equally have reported a "
      "clean superseded file as proof that a defective delivered one was fine. This is "
      "L-066 and L-067 — a check that opens a delivered file by name moves with the "
      "re-issue — recurring in a new form within a day of being registered, which is "
      "evidence that the lesson needed to be arithmetic rather than remembered.",
      "A repository whose delivered filenames sort chronologically as strings, which would "
      "make the distinction moot."),

    L("L-217", "ALL", None,
      "A GENERATOR THAT CRASHES LEAVES ITS ARTEFACT EXACTLY AS IT WAS, AND THE DOCUMENT GOES "
      "ON PUBLISHING IT. A broken generator is silent in a way a wrong one is not.",
      "Nothing in a build pipeline distinguishes \'this file was not regenerated\' from "
      "\'this file did not need regenerating\'. The artefact keeps its timestamp, keeps its "
      "shape, and keeps the numbers of whichever edition last ran successfully.",
      "ARCC 03-Sep-2026, reading the rendered PDF",
      "build",
      "scenario_margin.py ended on sum(v[k] * L[\'weights\'][k]), and when the typed lens "
      "blend was retired under [R-LENS-03] the weights left the numbers file and the "
      "generator began raising KeyError on every run. The delivered study went on publishing "
      "that file\'s LAST SUCCESSFUL output — a base case of 55.40 / 54.65 against a published "
      "66.53, in a table headed \'Central\', 29% below a spot the same study elsewhere "
      "reports it as 13.6% below. Re-running it then exposed a SECOND defect the crash had "
      "been hiding: the harness re-implemented the discounted cash flow rather than calling "
      "the model, so it still carried the retired rr = g / ROIC terminal and landed 27% "
      "below the study it exists to reproduce, and it dropped other operating income "
      "entirely. Its own G3 gate said so the moment it ran. Now it calls the shared terminal "
      "builder on the study\'s own committed terminal record and reproduces 66.53 exactly.",
      "A build system that fails the whole run when any generator raises, which would make "
      "the silence impossible rather than merely detectable."),

    L("L-218", "ALL", None,
      "TEXT DRAWN INSIDE A FIGURE IS INVISIBLE TO EVERY CHECK THAT READS A DOCUMENT. Compute "
      "it, because nothing else will catch it.",
      "The prose-figure gate reads a document\'s text; a chart\'s annotation is pixels. A "
      "number typed into a figure therefore has NO instrument pointed at it at all, which "
      "inverts the usual intuition that a chart is somehow less load-bearing than a "
      "sentence.",
      "ARCC 03-Sep-2026, reading the rendered PDF",
      "build",
      "Figure 4\'s annotation read \'the whole EGP 15.10 gap is forward-looking\' and \'that "
      "cash is inside the 54.65\' — the superseded edition\'s gap and central — drawn "
      "directly above bars that already ended at 66.53, in a figure whose underlying record "
      "was current and declared its vintage correctly. It also claimed two thirds of the gap "
      "was capex and a dividend when those two steps together are several times the gap. "
      "Every figure in the annotation is now computed from the record the bars are drawn "
      "from, so the text and the picture cannot disagree.",
      "A rendering pipeline that emits figure text into the document\'s text layer, where "
      "the existing prose gate would reach it."),

    L("L-219", "ALL", None,
      "A DISTANCE IS MEASURED FROM THE PRICE ITS SUBJECT WAS COMPUTED ON, NEVER FROM A PRICE "
      "OF ANOTHER DATE. Two clocks in one column produce figures that are individually "
      "correct and jointly impossible.",
      "The technical read is built on the price library; the study\'s spot is the latest "
      "known market price, and the two can be weeks apart. A percentage that divides one by "
      "the other has no meaning and does not announce itself as meaningless.",
      "ARCC 03-Sep-2026, reading the rendered PDF",
      "build",
      "ARCC\'s levels table headed a column \'Distance from spot\' and divided every level by "
      "a spot of 77.00 struck on 3 September, while the levels themselves come from a "
      "library ending 6 August at a close of 59.00 — four weeks and 30.5% earlier. Every "
      "resistance and every support printed as a large NEGATIVE, and the 52-WEEK HIGH "
      "printed 21.6% BELOW the current price, which is impossible on one clock. The read "
      "itself was internally coherent throughout: resistance 1 above its own close, support "
      "1 below it. Distances are now measured from the read\'s own close with that date in "
      "the column heading, and the gap between the two dates is stated in the caption rather "
      "than buried inside a percentage.",
      "A study whose technical read and spot are always struck on the same session, which "
      "would make the distinction unnecessary rather than merely invisible."),

    L("L-220", "ALL", None,
      "A WIDENING MADE TO CLEAR A FALSE POSITIVE CAN HIDE A TRUE ONE. Widening a rendering "
      "set across two CLOCKS is not the same discipline as widening it across two renderings "
      "of one quantity.",
      "The standing rule that a false positive is fixed by widening the set, never by "
      "deleting the figure, is right — and it says nothing about which widenings are "
      "legitimate. Admitting both a correct and an incorrect anchor makes the check pass on "
      "either, which is indistinguishable from not checking.",
      "ARCC 03-Sep-2026",
      "build",
      "prose_check declared PF.relative_to(technicals, (read_close, spot)) — both anchors — "
      "so the levels table\'s wrong-clock distances were IN the rendering set and the gate "
      "reported 0 unmatched on a table showing the 52-week high below the current price. "
      "Narrowed to the read\'s own close, with the single figure that legitimately spans "
      "both clocks — the gap between them, stated in the caption — declared explicitly.",
      "A quantity genuinely quotable against two different anchors in the same document, "
      "where the reader is told which is which at each use."),

    L("L-221", "ALL", None,
      "A CAUTIOUS-SOUNDING VERDICT IS STILL A VERDICT AND IS PUBLISHED ONLY WHERE THE RECORD "
      "EARNS IT. Understating in the wrong direction is not a safe error.",
      "A flag that flatters gets checked; a flag that disparages our own work reads as "
      "conservative disclosure and is waved through. Both are claims about the world.",
      "ARCC 03-Sep-2026, reading the rendered PDF",
      "build",
      "The cone figure was titled \'ILLUSTRATIVE ONLY, this cone is over-wide\' and the body "
      "said the map was labelled illustrative \'because its own calibration record says it "
      "should be\'. That name\'s published record carries NO flag: 41 of 44 resolved "
      "three-month forecasts finished inside the 90% band, 93.2% against a 90% target, "
      "which the two-sided test does not distinguish from the target, and its width of "
      "1.43x a naive random walk is the ordinary figure for its exchange and is disclosed "
      "rather than judged. The study was publishing a flag the record does not earn and "
      "attributing it to that record. Replaced with the record\'s own numbers and a title "
      "saying what the cone IS — anchored on the last session of the price history rather "
      "than on the valuation date.",
      "A record that does earn the flag, in which case publishing it is the rule working."),

    L("L-222", "ALL", None,
      "READ THE SITE\'S DATA THROUGH A REAL JAVASCRIPT PARSE, IN EVERY PLACE THAT READS IT — "
      "not only in the checkers written after the lesson.",
      "A regular expression over a JavaScript object literal returns the FIRST match where "
      "the parser takes the LAST, so a duplicated key means the tool inspects the half no "
      "reader ever sees.",
      "ARCC 03-Sep-2026",
      "build",
      "The standing rule was adopted after a reader — not a check — found a ticker page "
      "publishing a support above its own close while both existing gates reported it "
      "clean, and one study (EGCH) implements it correctly through node. ARCC\'s own "
      "band-record reader was a regex over data.js the whole time. The rule was right, was "
      "written down, and bound in one place, which is the same shape as the prose-figure "
      "and sweep-module findings of the same week.",
      "A data file that is genuinely a flat key-value format with no possibility of a "
      "duplicate key, where a regex and a parser cannot disagree."),

    L("L-223", "ALL", None,
      "COUNT HOW MANY PLACES A RULE ACTUALLY BINDS BEFORE BELIEVING IT BINDS. The number is "
      "usually smaller than the number of places it applies.",
      "A rule written in prose is obeyed where somebody implemented it and nowhere else, and "
      "nothing about the repository shows the difference — every file looks equally "
      "compliant until somebody counts.",
      "the site-data reader, 03-Sep-2026",
      "build",
      "[R-ENF-03] requires assets/data.js to be read through a real JavaScript parse and was "
      "adopted after a reader found a ticker page publishing a support above its own close "
      "while both gates reported it clean. Four weeks later, FORTY-FOUR files read the "
      "site\'s data and THIRTEEN still did it by regular expression, including three engine "
      "modules and four repository-level scripts. This is the fourth finding of identical "
      "shape in one week — the prose-figure check implemented by one study of twenty-four, "
      "the sweep register by sixteen of seventeen, the external-reader scrub as a "
      "hand-maintained word list per study, and now this. The remedy is the same every "
      "time: one shared instrument, and a gate that counts.",
      "A rule whose implementations are structurally impossible to count, where the honest "
      "answer is that it cannot be enforced from outside and must stay prose."),

    L("L-224", "ALL", None,
      "A PROBABILITY AND THE BOUNDARY IT IS MEASURED AGAINST MUST COME FROM THE SAME CLOCK. "
      "This is the two-clock error in the one place where it changes what a reader believes "
      "will happen.",
      "A distribution simulated from one anchor answers questions about that anchor. Splitting "
      "its bands at a different price and keeping its probabilities states the chance of "
      "finishing above one number using the distribution of another — and the result looks "
      "like an ordinary percentage.",
      "ARCC 03-Sep-2026, reading the rendered PDF",
      "build",
      "The probability-zone table drew its boundaries at the latest close of 77.00 and took "
      "its probabilities from the simulation\'s P(above the ANCHOR) of 59.00, so it "
      "published a 51% chance of finishing above 77.00 from a distribution whose median is "
      "60.46 and whose 95th percentile is 83.17 — roughly three times the truth, in the one "
      "table whose entire purpose is to state probabilities. Every other figure on the page "
      "was correct. Boundaries and probabilities now both sit on the anchor, the anchor is "
      "named rather than called spot, and the caption states how far the latest close is "
      "from it.",
      "A study whose cone is re-struck at delivery on the same price the valuation uses, "
      "where the two clocks coincide and the distinction cannot arise."),

    L("L-225", "ALL", None,
      "A SUMMARY SENTENCE IS A CLAIM AND IS RECOMPUTED, NOT REMEMBERED. Counts and directions "
      "in prose go stale exactly like figures, and nothing looks less like a number than a "
      "word.",
      "Figure gates match numerals. A sentence saying which lenses sit above the price "
      "contains no numeral at all, so it survives every re-strike untouched while the "
      "lenses move underneath it.",
      "ARCC 03-Sep-2026, reading the rendered PDF",
      "build",
      "One sentence in section 4 said \'the two multiple-based lenses put fair value below "
      "the current price and the two forward-looking ones put it above\', two paragraphs "
      "after the same page stated that EVERY lens sits below the market. Both could not be "
      "true; the second was. The same sentence carried a typed 98% restating a computed "
      "one, a typed 52-week high and low, a distance computed against spot while the high "
      "and low came from a read four weeks earlier, and a duplicated word. It is now "
      "computed from the lens values, and it says the uncomfortable thing plainly: no "
      "reading in the study supports the price.",
      "A study where the lens set is fixed and cannot move between editions, making a "
      "written count safe."),

    L("L-226", "ALL", None,
      "A CHECK THAT READS A DELIVERED DOCUMENT READS ITS TABLE CELLS TOO. A reader does not "
      "distinguish a paragraph from a cell, so a check that does is checking a different "
      "document.",
      "python-docx exposes paragraphs and tables as separate collections, so the natural "
      "one-line way to get a document\'s text silently omits every table — which is where "
      "the densest and most quotable claims sit.",
      "ARCC 03-Sep-2026",
      "build",
      "The check written that morning to stop a retired diagnostic being quoted as the live "
      "figure read paragraphs only, and reported clean while the cross-examination TABLE "
      "carried \'the terminal return and reinvestment rate this study computes (11.26% ...)\' "
      "— the retired construction\'s own number, in the cell whose job is to reject an "
      "objection on evidence. This is the PHDC precedent in this repository, where a "
      "standing-rule identifier leaked to a reader through a table cell for the same reason. "
      "Widened, it caught the defect on its first run.",
      "A document format where tables are part of the paragraph stream, making the omission "
      "impossible rather than merely easy."),

    L("L-227", "ALL", None,
      "READING THE RENDERED PAGES IS NOT A FORMALITY AND NOTHING CURRENTLY REPLACES IT. "
      "Budget it per re-issue, and mine each finding for the check that would have caught it.",
      "Every automated gate here points from the page back to the model and asks whether "
      "each figure came from it. The defects that survive are the ones that live BETWEEN "
      "figures, in the words around them, inside pictures, or in a relationship between two "
      "tables — none of which a per-figure check can see.",
      "ARCC 03-Sep-2026",
      "build",
      "Reading all 32 pages of one delivered study found roughly forty distinct "
      "claim-level defects, in a study that had just passed the recalculation gate, the "
      "prose-figure check, the external-reader scrub, the column audit and every "
      "repository-level gate. The most serious stated a 51% probability for an outcome the "
      "model puts near 15%; several published a superseded edition\'s numbers; one "
      "contradicted its own page two paragraphs later. SIX of the classes were then made "
      "arithmetic in the same session and are now in CI — table footing, the sign-word "
      "check, the retired-input check, the shared site-data reader, delivered-PDF currency "
      "and artefact currency — so the next study cannot repeat them. The residue is the "
      "argument for keeping the read.",
      "A re-issue where the read finds nothing the gates did not, sustained over several "
      "studies, which would mean the instruments have caught up with the reader."),

    L("L-228", "ALL", None,
      "RUN A NEW INSTRUMENT OVER THE WHOLE BOOK BEFORE BELIEVING ITS FIRST FINDING. Most of "
      "what a fresh check reports is the check being wrong about how the work is shaped.",
      "A gate written from one study\'s defects encodes that study\'s table conventions. The "
      "book carries several more, each of them ordinary, and each looks like a defect until "
      "somebody looks at it.",
      "the table-footing gate, 03-Sep-2026",
      "build",
      "Pointed at the five rebuilt studies the gate reported 38 unreconciled totals. FOUR "
      "were the instrument, not the book, and all four were fixed rather than declared: a "
      "date column parsed as numeric because \'Jan 2026\' yields 2026 under any reader that "
      "tolerates a prefix; a TOTAL row that is a SUM in one column and a WEIGHTED MEAN in "
      "another, which the first draft tried only for labels containing the word "
      "\'weighted\'; a weighted mean whose band ignored the ROUNDING OF ITS OWN WEIGHT "
      "COLUMN, condemning a product table by five units on a band of four; and an \'OF "
      "WHICH\' breakdown, whose indented sub-items were counted alongside the parent line "
      "they decompose, condemning a balance sheet that foots exactly. Each fix made the "
      "instrument more right rather than more permissive, and the negative control held at "
      "14/14 through all four.",
      "A first run whose findings are all real, which would mean the instrument was written "
      "from a wide enough sample to begin with."),

    L("L-229", "ALL", None,
      "A RATCHET ENTRY IS EARNED BY A NAMED FINDING, NOT BY SILENCE. Where a study cannot "
      "clear a check, write down what it failed on and keep it listed.",
      "The temptation on a stubborn red is to declare the exception and move on; a "
      "declaration with a reason that is really \'this one is awkward\' is the rubber stamp "
      "the whole mechanism exists to prevent.",
      "TMGH 03-Sep-2026",
      "build",
      "Four studies were given footing declarations in one pass. Three came off the ratchet "
      "with every exception naming a real structural fact — an input register keyed by "
      "name, a transposed cost-of-capital table, a blend across products whose weights live "
      "in another table, disclosed line items in a summary. The fourth did not: TMGH\'s "
      "as-reported balance sheet is 748 SHORT in its non-current block and 24 short in its "
      "current block against the rows it prints, so either the statement carries lines the "
      "table omits or the totals are wrong. That is the reader\'s problem either way, it was "
      "not resolved, and the study stays listed with that as its recorded reason.",
      "A book where every red resolves to a legitimate structural exception, which would "
      "mean the instrument is measuring nothing."),

    L("L-230", "ALL", None,
      "A STATEMENT THAT CLOSES AT THE TOP CAN STILL FAIL A READER IN EVERY BLOCK BELOW IT. "
      "Check the sub-totals, not only the identity.",
      "Total assets equalling equity plus liabilities is the check every model already runs "
      "on itself, and it passes whether or not the printed components of each block add up "
      "to their own sub-total. The reader adds the column, not the identity.",
      "TMGH 03-Sep-2026",
      "build",
      "TMGH\'s as-reported balance sheet closed PERFECTLY at the top — non-current plus "
      "current is total assets to the pound, and equity plus liabilities is the same figure "
      "— so every check that reconciles a model to itself passed it. Below that, the five "
      "printed non-current lines came out EGP 748mn short of their own sub-total and the "
      "seven current lines EGP 24mn short. The study was not wrong: it HELD every missing "
      "figure as a registered input and simply did not print them — intangibles 84.6 plus "
      "right-of-use 481.4 plus deferred tax 182.0 is 748.0 to the last hundred thousand, "
      "and work in progress is 23.6. A reader adding a column had no way to tell a missing "
      "line from a wrong total.",
      "A presentation that deliberately shows principal lines only and SAYS so, where the "
      "residual is labelled rather than absent."),

    L("L-231", "ALL", None,
      "TRIAGE A GATE'S BACKLOG BY HOW CLOSE THE ARITHMETIC COMES, NOT BY THE LABEL. A block "
      "that ALMOST foots is a missing line; one that is wildly off is a different kind of "
      "row altogether.",
      "Both arrive as the same complaint — a total that does not follow from the rows above "
      "it — and reading eighty-seven of them one at a time is how a backlog becomes "
      "permanent. The distance separates them in a single pass.",
      "the table-footing port, 03-Sep-2026",
      "build",
      "Run across the nineteen studies carrying no footing check, the gate reported 87 "
      "unreconciled totals. Sorting each by how close its nearest printed block comes to the "
      "stated total split them cleanly: 21 land within six per cent, and every one inspected "
      "is the TMGH signature — a summary statement omitting small lines it already holds as "
      "registered inputs, closing perfectly at the top and short by half a point to two "
      "points in each block below (ADNOCDRILL, AMR, EMPOWER, RIYADHCABLE, EIPICO). The other "
      "66 are far off and are structural: a disclosed line item among its peers, a "
      "transposed cost-of-capital table whose weights are a row, a blend across a dimension "
      "the column does not carry. Recorded in footing_findings.json rather than resolved, "
      "because recording a finding is what stops a backlog from silently becoming a "
      "declaration.",
      "A backlog where the two classes overlap in distance, which would mean the triage is "
      "measuring the wrong thing and each case must be read individually."),

    L("L-232", "ALL", None,
      "WHEN A RULE KEEPS BREAKING, SUSPECT THE INSTRUMENT BEFORE THE WILL. Ask what mechanism "
      "is behind it and whether that mechanism can physically do the job.",
      "A rule that has been restated three times and broken three times is not a rule anyone "
      "disagrees with. Restating it a fourth time is the cheapest response and the one least "
      "likely to work; asking what enforces it is the expensive one.",
      "the continuation routine, 03-Sep-2026",
      "build",
      "\"Do not stop\" was adopted, written into the operating protocol, and broken twice in "
      "one afternoon, each time by ending a turn on a progress report. The machinery behind "
      "it was an hourly cron, and a cron has three properties that make it unable to do this "
      "job: it CANNOT FIRE INTO A TURN THAT IS ALREADY RUNNING, so it shortens the gap after "
      "a stop and can never prevent one; its floor is SIXTY MINUTES, tested and refused "
      "below that; and nothing inside a turn forces a next action. Its own prompt admitted "
      "the first — \"so that stopping costs an hour rather than half a day\" — which "
      "describes a backstop. The replacement is SELF-RE-INVOCATION: the last act of a turn "
      "that ends with work remaining launches a background task whose EXIT re-invokes the "
      "session, caused by the stop rather than by a clock, inside the turn\'s own control, "
      "and costing a minute. The cron is demoted to the archived-session case it can "
      "actually serve.",
      "A rule that keeps breaking while its mechanism demonstrably can do the job, which "
      "would mean the diagnosis really is about will and the remedy is elsewhere."),

    L("L-233", "ALL", None,
      "WHERE A TABLE DOES NOT ADD AND THE MISSING LINES ARE NOT HELD, PRINT A LABELLED "
      "RESIDUAL. It is not inventing data — it is arithmetic on two figures the study "
      "already has — and it is strictly better than a column that does not add.",
      "The instinct on finding a gap that cannot be closed from the sources to hand is to "
      "leave it, because naming the missing lines would be an invention. That is right about "
      "the naming and wrong about the leaving: a reader facing a column that does not add "
      "cannot tell a missing line from a wrong total, and the residual tells them which.",
      "the footing port, 03-Sep-2026",
      "build",
      "Five studies came out short against their own disclosed totals. TMGH, ADNOCDRILL and "
      "EMPOWER HELD every missing figure as a registered input and were fixed by printing "
      "the lines — EMPOWER\'s eleven of them, with the builder asserting that each residual "
      "IS the sum of the specific lines it names, because a residual computed as "
      "total-less-printed foots BY CONSTRUCTION and proves nothing. AMR and RIYADHCABLE did "
      "NOT hold them, and were fixed by a row labelled \'Other assets, not broken out in "
      "this table (residual)\' with a caption saying why it is not named. RIYADHCABLE\'s "
      "residual then became a finding in its own right: SAR 146, 147 and 430mn, so something "
      "outside the four broken-out lines grew by SAR 283mn in one year, which that table "
      "cannot explain and the next edition should.",
      "A residual so large that labelling it is a way of not investigating it, where the "
      "honest answer is to obtain the statements instead."),

    L("L-234", "ALL", None,
      "A NEW GATE'S FALSE-POSITIVE RATE IS A PROPERTY OF THE GATE, AND IT FALLS AS THE GATE "
      "LEARNS THE WORK. Measure it, fix the instrument, measure again — never widen a bound "
      "to make a number look better.",
      "The first run of any check over an existing book reports mostly its own ignorance of "
      "how that book is shaped. Treating that number as a defect rate leads to loosening; "
      "treating it as a to-do list of things the instrument does not yet understand leads to "
      "a sharper check.",
      "the table-footing port, 03-Sep-2026",
      "build",
      "The book-wide advisory fell 22.3% -> 10.5% across SEVEN instrument fixes in one "
      "session, and not one of them loosened a tolerance: a balance sheet foots over its "
      "SUBTOTALS; a row labelled Total assets HEADING a summary is a line item with nothing "
      "above it; a date column parses as numeric because \'Jan 2026\' yields 2026; a TOTAL "
      "row is a sum in one column and a WEIGHTED MEAN in another; a weighted mean\'s band "
      "must carry the rounding of its own WEIGHT column; an \'OF WHICH\' row is a breakdown "
      "of the line above and not a peer; a DASH in a total cell is \'not shown\' rather than "
      "a claim of zero, while a dash in a component is zero; a PERCENTAGE is not a component "
      "of a currency total; and an EMPTY cell in a row that carries values elsewhere means "
      "\'does not apply here\' rather than the end of the block. The negative control held at "
      "14/14 through every one, which is what made the fixes safe to make quickly.",
      "A fix that lowers the rate by relaxing what counts as reproducible rather than by "
      "correcting what the instrument believes about tables."),

    L("L-235", "ALL", None,
      "A CHECK'S POPULATION PREDICATE IS PART OF THE CHECK, AND KEYING IT ON A WORD RATHER "
      "THAN ON THE QUANTITY PUTS INNOCENT WORK ON THE RATCHET — WHERE IT WILL LATER EXCUSE "
      "THE REAL THING.",
      "A ratchet entry is an allowance. An allowance standing over a file that never "
      "committed the offence is not merely untidy: it is a standing permission that "
      "activates the day that file does commit it, silently, because the gate will read the "
      "name off the list and move on.",
      "the site-data reader port, 03-Sep-2026",
      "build",
      "The gate for [R-ENF-03] keyed its population on the STRING 'data.js' appearing "
      "anywhere in a file, and three of the thirteen files it ratcheted never open the file "
      "at all: two carry the word inside an external-reader SCRUB WORD LIST — the internal "
      "vocabulary a delivered document may not contain — and one names the path in a prose "
      "comment, while each separately uses a regular expression for something else "
      "entirely. Re-pointed at a PATH CONSTRUCTION per [R-COC-01], the population fell 44 "
      "-> 31 and the ratchet 13 -> 10, and the negative control gained the distinction that "
      "matters: green-because-EXCLUDED is not green-because-compliant, and an exit code "
      "cannot tell them apart, so the population COUNT is compared with and without each "
      "file.",
      "A population predicate that is broader than the rule and where the extra members are "
      "shown to be harmless — which would mean the ratchet's allowances cost nothing."),

    L("L-236", "ALL", None,
      "A SYNTAX CHECK IS NOT A SEMANTIC CHECK, AND THE GAP BETWEEN THEM IS EXACTLY WHERE A "
      "DUPLICATED KEY LIVES.",
      "'It parses' feels like verification and is a much weaker claim than it sounds. A "
      "file can be perfectly well-formed and still not mean what its author wrote, and the "
      "form most likely to survive every check is the one that is legal in the language.",
      "the site-data writer port, 03-Sep-2026",
      "build",
      "Every tool that writes assets/data.js edits it as TEXT — correctly, since a JSON "
      "round-trip would destroy the file's formatting and its prose comments — and each "
      "verified with `node --check`. Demonstrated on a real copy of the file rather than "
      "asserted: plant a second `levels` key on one entry and `node --check` PASSES, the "
      "parser returns the SECOND, and a regular expression returns the FIRST. That is not a "
      "hypothetical shape; it is the exact defect [R-ENF-03] was adopted on, a ticker page "
      "publishing a support ABOVE its own close while both gates read the half the reader "
      "never saw. The write path could have produced that file again and nothing would have "
      "said so.",
      "A writer whose post-write verification is shown to catch a shadowed field without "
      "loading the file — which would mean the syntax check was sufficient after all."),

    L("L-237", "ALL", None,
      "A READER AND A WRITER OWE DIFFERENT THINGS TO THE SAME RULE, AND HOLDING ONE TO THE "
      "OTHER'S OBLIGATION MANUFACTURES A DEBT THAT CAN NEVER BE PAID.",
      "A ratchet entry that cannot in principle be cleared is a permanently-red check "
      "[R-ENF-02] forbids, wearing a different hat — and it is worse than an obviously red "
      "one, because it looks like a backlog somebody will get to.",
      "the site-data writer port, 03-Sep-2026",
      "build",
      "Three files WRITE data.js by string surgery, which is the only sound way to preserve "
      "its formatting, so 'read it through a parse' forbids the job rather than the "
      "defect. Re-pointed at what a writer actually owes — proof that the PARSER agrees "
      "with what it wrote — the clause immediately surfaced FOUR MORE writers the string "
      "predicate had never counted, one of them a CONE writer with no post-write check of "
      "any kind, not even `node --check`; two more counted their records against a known "
      "total and never looked at a VALUE, which a block emitted twice leaves identical "
      "either way. The ratchet went 13 -> 0.",
      "A writer for which no verification is expressible, which would mean the obligation "
      "is unmeetable rather than merely different."),

    L("L-238", "ALL", None,
      "AN EXEMPTION WIDER THAN ITS OWN REASON IS THE SAFEST HIDING PLACE THERE IS.",
      "Nobody is lying, the reason survives review, and the work simply happens where the "
      "check no longer reaches. This is [R-MACRO-01]'s finding — a TRUE exemption on the "
      "WRONG OBJECT — arriving again in a different area within a day, which is what makes "
      "it a house rule rather than an anecdote.",
      "the site-data reader port, 03-Sep-2026",
      "build",
      "A negative control plants a broken data.js on purpose, so requiring it to verify "
      "that the file it deliberately corrupted parses to what it meant is incoherent — a "
      "real exemption with a real reason. The first draft implemented it by skipping "
      "*_negative_control.py ENTIRELY, which also stopped checking whether a control READS "
      "data.js by regular expression, where nothing excuses it, and shrank the population "
      "from 31 to 26 for a reason that had nothing to do with reading. Scoped to the writer "
      "clause it was written for, and asserted in BOTH directions: a control that writes "
      "without verifying passes, a control that reads by regex still fails.",
      "An exemption whose scope cannot be narrowed to its reason without losing the reason "
      "— which would mean the two genuinely coincide."),

    L("L-239", "ALL", None,
      "A RULE OF THE FORM 'AFTER ANY X, ASSERT Y' BINDS NOTHING UNTIL SOMETHING THAT DOES "
      "X CALLS Y.",
      "It is the most convincing kind of dead rule, because it names its own trigger and "
      "therefore reads as though it executes. The place to look is not the rule but the "
      "code that performs X.",
      "the site-data writer port, 03-Sep-2026",
      "build",
      "'After ANY ledger write, assert the lifecycle invariant' has been standing since "
      "29-Jul-2026. NEITHER writer that appends ledger rows checked it; it lived in the "
      "protocol and in whatever the operator remembered. Measured before it was asserted, "
      "per [R-ENF-02]: 0 violations across 187 (instrument, horizon) pairs, so it passes "
      "today rather than arriving red. And the invariant is NOT 'one open row per name' — "
      "steady state is four, because a fresh three-month strike demotes the prior cone to "
      "an aging tail; 114 pairs carry one open row and 73 carry two and every one is "
      "correct. What may never happen is two open rows sharing the LATEST anchor.",
      "A written trigger of this shape that turns out to be executed by every performer of "
      "X without anyone having wired it — which would mean prose triggers do bind."),

    L("L-240", "ALL", None,
      "THE BASE A RATE IS APPLIED TO IS AS MUCH A SPECIFICATION AS THE RATE, AND A BASE "
      "BUILT FROM WHATEVER THE BALANCE SHEET HAPPENS TO CARRY IS NOT A SPECIFICATION AT ALL.",
      "A reinvestment or maintenance charge is rate x base. Every argument this house has "
      "had about terminals has been about the RATE — the implied asset life, the growth "
      "assumption — while the base went unexamined because it looked like arithmetic "
      "somebody had already done.",
      "the ADNOCLS terminal, measured 03-Sep-2026",
      "build",
      "THE MODEL REPORT — the document every other study is written against — computes its "
      "terminal invested capital as NET BOOK property, plant and equipment plus working "
      "capital plus intangibles plus goodwill, and divides the growth rate into it. Two of "
      "those three additions are not replaced by capital expenditure at all: a maintenance "
      "programme does not buy back goodwill, and working capital is charged separately as "
      "inflation x working capital in the corrected construction, so including it in the "
      "base charges for it twice. The first is NET BOOK rather than replacement cost, which "
      "is the very distinction the corrected terminal exists to draw. Measured: the model "
      "levies 228,793 a year for ever; book depreciation on the same assets alone is "
      "612,111, which is 2.7x the charge and is itself struck on historical cost; on the "
      "disclosed 25-year life applied to gross cost the charge should be 3.1x to 3.7x what "
      "is levied. The shared terminal module REFUSES these inputs outright — implied payout "
      "120.2% of terminal profit — and that refusal is the module reporting that the BASE "
      "is wrong rather than the life.",
      "A study whose invested-capital base is demonstrably at replacement cost and still "
      "produces a maintenance charge far below its own book depreciation."),

    L("L-241", "ALL", None,
      "AN IDENTITY IS WRITTEN FOR THE CASE IN FRONT OF YOU AND THEN RUNS ON EVERY CASE "
      "AFTER IT. GUARD IT BY THE CONDITION IT ASSUMES, NOT BY THE MARKET IT WAS WRITTEN FOR.",
      "An identity carries its assumptions silently — that is what makes it an identity — "
      "so when the assumption stops holding there is no error, only a plausible number. It "
      "will not announce itself and no gate about provenance, arithmetic or sourcing can "
      "see it, because nothing about it is unsourced or miscalculated.",
      "sourcing six house macro paths, 03-Sep-2026",
      "build",
      "Relative purchasing-power parity was written for Egypt, the first market sourced, "
      "and ran unconditionally on every market added after. On a HARD PEG it manufactures "
      "exactly the drift the peg forbids: the first UAE print returned a dirham sliding "
      "3.6725 to 3.65 over five years off a 0.5pp inflation differential that a fixed "
      "nominal rate absorbs as a REAL appreciation. A study reading it would have escalated "
      "dollar revenue against a depreciating dirham and called it derived — a claim that "
      "the peg breaks, made silently, by arithmetic. The same relation on the UNITED STATES "
      "path compared the dollar with itself and returned a 0.98% depreciation of the dollar "
      "against the dollar. Both were found by PRINTING a newly sourced path, not by any "
      "gate. Both are now guarded by regime and by numeraire and pinned in the negative "
      "control on all seven markets in both directions.",
      "A currency identity that produces the right answer under a regime it does not assume "
      "— which would mean the guard is unnecessary rather than merely quiet."),

    L("L-242", "ALL", None,
      "A GATE THAT NOTHING RUNS IS A FILE. WIRING IT IN IS PART OF WRITING IT, NOT A "
      "FOLLOW-UP.",
      "A written gate feels finished — it has a docstring, a negative control, a name "
      "somebody can cite — and every property that makes it convincing is present whether "
      "or not anything ever executes it. It is [R-CAL-03]'s decorative test in a sharper "
      "form: not a check that never rejects anything, but a check that never RUNS.",
      "the legacy-assets gate, found unwired 03-Sep-2026",
      "build",
      "scripts/check_legacy_assets_sync.py was written on 30-Aug-2026 for a real shipped "
      "defect and was invoked by NO workflow. Run by hand four days later it went RED, and "
      "what it found was live: on 1 September the AMOC fair value was reverted in "
      "assets/data.js to its pre-calibration figure, because the standing instruction is "
      "that nothing from the calibration campaign goes live one name at a time. The revert "
      "reached assets/ and not the legacy mirror — and legacy/ holds the ONLY working "
      "copies of the ledger, picker, trade and portfolio pages, which read their own "
      "data.js. For two days testahil.com served 5.53/8.64/12.48 on /legacy/ and "
      "4.09/5.95/8.52 on the new information architecture: TWO DIFFERENT FAIR VALUES FOR "
      "ONE COMPANY ON ONE DAY, with the public ledger showing the campaign number that was "
      "not supposed to be there. Confirmed by fetching both URLs from the live site before "
      "fixing it, rather than inferred from the repository. Separately measured the same "
      "hour: TWENTY-ONE of seventy-one gates were in no workflow's TRIGGER list, so "
      "editing a gate ran nothing — the one file whose correctness every other check "
      "depends on was the one file CI did not watch.",
      "A gate whose value does not depend on being run — which would mean it is "
      "documentation, and should be filed as such."),

    L("L-243", "ALL", None,
      "WHEN A MEASUREMENT ON ONE NAME EXPLAINS EVERYTHING, THAT IS THE MOMENT TO POOL IT, "
      "NOT THE MOMENT TO CONCLUDE.",
      "A single name that answers the question cleanly is more persuasive than a pooled "
      "figure that answers it partly, and it is persuasive in the wrong direction: the "
      "cleanliness is what should make it suspect. This is [R-LESSON-01]'s one-observation "
      "rule turned on a finding ABOUT the findings, where it is easiest to forget.",
      "the macro-share measurement, 03-Sep-2026",
      "build",
      "The driver census shows a bias that COMPOUNDS with the horizon — an intercept near "
      "zero with a large slope, the signature of a rate error. [R-FCAL-01] already requires "
      "every origin to be re-run on PERFECT FORESIGHT of the inflation path, so the "
      "explicit window's own escalator can be tested directly. On AMOC it answered "
      "completely: net sales 89.2% macro, raw materials 97.6%, cost of sales 97.3% — the "
      "revenue error collapsing from 0.5701 to 0.0617 and the cost error from 0.6273 to "
      "0.0153 once the model is told the true path. That is a whole diagnosis from one "
      "name, and it is wrong as a general claim. Pooled across five names and 64 drivers "
      "carrying an inflation term the median macro share is 19.9%, the inflation path is "
      "most of the error on 10 of 64, and the total falls only 64.88 to 57.78 — 11%. EGCH "
      "goes the OTHER WAY: perfect foresight of inflation makes its forecast 13% WORSE, "
      "because its revenue is dollar tonnes at dollar prices and its errors are not in the "
      "pound at all. The pooled figure is now printed by the census beside the per-name "
      "ones so the one-name reading cannot be the one that gets read.",
      "A pooled macro share that rises toward AMOC's as more names are run — which would "
      "make the inflation path a general explanation after all."),

    L("L-244", "ALL", None,
      "A RATE ERROR THAT SURVIVES PERFECT FORESIGHT OF THE RATE IS SOMEWHERE ELSE.",
      "Where a bias compounds with the horizon there is usually more than one rate it could "
      "live in, and the candidates are rarely tested against each other — the first "
      "plausible one gets the blame. Ruling one out is worth as much as finding one.",
      "the macro-share measurement, 03-Sep-2026",
      "build",
      "Two rates could carry a compounding scale error: the inflation path the explicit "
      "window escalates on, and the terminal construction. Handing the model the true "
      "inflation path at every origin removes 11% of the pooled driver error and leaves "
      "89% standing, which RULES THE EXPLICIT WINDOW'S ESCALATOR OUT as the general cause "
      "and is evidence FOR the terminal attribution rather than against it. What the "
      "inflation path does explain is concentrated and legible: pound-denominated cost and "
      "revenue lines on names whose currency moved a long way, which is a fact about one "
      "economy and two companies rather than a property of the method.",
      "A third rate — a demand path, a margin glide — that removes more of the residual "
      "than the terminal construction does when it is tested the same way."),

    L("L-245", "ALL", None,
      "TWO CORRECTIONS TO ONE FORMULA ARE NOT TWO INDEPENDENT CORRECTIONS WHEN THEY SIT ON "
      "DIFFERENT BASES. Pricing one with the other left at its old value gives a number "
      "that is neither construction, and it looks perfectly reasonable.",
      "The temptation is strong precisely where one half is cheap and the other is not: "
      "the cheap half gets priced, the expensive half gets deferred, and the interim "
      "figure is quoted as a lower bound when it is not a bound at all.",
      "the terminal census, 03-Sep-2026",
      "build",
      "[R-TERM-01] names two errors in the retired terminal: the charge, whose implied "
      "replacement cycle is 1/g rather than a fact about the asset, and a terminal that "
      "never adds book depreciation back though NOPAT is already net of it. Correcting the "
      "first needs a life sourced from each company's own accounting-policies note — real "
      "research, one name at a time. The second appears to need nothing, so a first draft "
      "priced it alone across thirteen terminals and reported the pooled terminal rising "
      "69.6%. IT IS WRONG. g x IC is a NET investment figure — the new capital needed to "
      "grow at g — so a construction charging it has already netted depreciation, and "
      "adding book D&A on top double-counts; the corrected construction charges maintenance "
      "GROSS at replacement cost, which is exactly why it must add book D&A back first. "
      "Checked against the one worked case rather than reasoned about: on ARCC the "
      "add-back-alone gives 2,445.3 against the module's own 3,310.1, 26% short. What the "
      "census prints instead is the one inference that needs no sourced life AND ONLY RUNS "
      "ONE WAY — a terminal charging less than its own book depreciation cannot be "
      "maintaining the asset base, because book depreciation is struck on historical cost "
      "and replacement costs more.",
      "A decomposition of the terminal into two charges that are on the same basis, where "
      "each half can be priced with the other held."),

    L("L-246", "ALL", None,
      "THE TERMINAL DEFECT IS PESSIMISTIC IN EGYPT AND OPTIMISTIC IN THE GULF, AND THE SIGN "
      "IS SET BY THE CURRENCY RATHER THAN BY THE COMPANY.",
      "A defect with a single name — 'the model is too pessimistic' — invites a correction "
      "with a single sign, and a correction with a single sign applied to a book that "
      "splits both ways makes half of it worse. The evidence for the diagnosis came almost "
      "entirely from Egyptian names, where the sign happens to be negative.",
      "the terminal census, 03-Sep-2026",
      "build",
      "The retired charge is g x IC, so the implied replacement cycle is 1/g — 14.3 years "
      "at a 7% terminal inflation and 66.7 at 1.5%. THE SAME PLANT IS CHARGED FOUR AND A "
      "HALF TIMES AS HARD FOR BEING IN EGYPT RATHER THAN THE EMIRATES. Measured across the "
      "readable book: SEVEN OF THIRTEEN terminals charge LESS than their own book "
      "depreciation — AMR 0.12x, DU 0.14x, SAVOLA 0.21x, AIRARABIA 0.23x, FERTIGLOBE 0.26x, "
      "ADNOCDIST 0.31x, ADNOCLS 0.32x — and every one of them is in a pegged low-inflation "
      "market. Those terminals are OVER-valued, not under. The six charging more than book "
      "depreciation are AMOC, ARCC, MODON, SCEM, RIYADHCABLE and SWDY, and the worked "
      "correction on ARCC raised its value while the measured correction on ADNOCLS would "
      "LOWER it. Since 44 of the 90 covered names are Gulf, the defect is optimistic on "
      "most of the book.",
      "A pegged-market name whose disclosed useful life turns out to exceed 1/g — which "
      "would mean the under-charge is not general to low-inflation markets."),

    L("L-247", "ALL", None,
      "A DATE IS A FIGURE A READER SEES, AND THE RULE THAT A FIGURE MUST BE COMPUTED RATHER "
      "THAN TYPED APPLIES TO IT.",
      "Dates escape the numeric-traceability discipline because they do not look like "
      "numbers: no gate that reconciles figures against a model inspects them, no "
      "recalculation touches them, and a stale one reads as a fact rather than as an error. "
      "They are also typed in several places at once, which guarantees they will disagree.",
      "reading PHDC's rendered pages, 03-Sep-2026",
      "build",
      "ARCC shipped a masthead a day stale and it was recorded as one study's defect. "
      "Reading PHDC's pages the same way found the identical thing — a 3 September edition "
      "whose masthead reads 'edition of 2 September 2026' — which made it a CLASS, and "
      "closing the class rather than the instance is what [R-ENF-01] requires. Measured "
      "across 31 delivered valuation studies, SEVEN do not carry their own edition date in "
      "their masthead, in three shapes: stated and WRONG (PHDC, TMGH, both a day stale), "
      "stated NOWHERE IN THE DOCUMENT AT ALL (ADNOCLS and SAVOLA — and ADNOCLS is THE MODEL "
      "REPORT, so a reader receives the exemplar every other study is written against with "
      "nothing on it saying when it was struck), and buried in the body (DU at paragraph "
      "74 inside a licence sentence, GBCO at 167 in an expert-log note, RIYADHCABLE at 119 "
      "in the disclaimer). THE ROOT CAUSE WAS TYPING: PHDC's builder carried the date in "
      "THREE separate string literals — masthead, disclosure, output filename — and two of "
      "the three said 2 September while the file said 3 September; TMGH's carried two that "
      "disagreed. Both now derive it from the file the document ships as, so they cannot "
      "disagree, and the rebuilds changed two paragraphs and one paragraph respectively — "
      "nothing but the date moved.",
      "A delivered document whose date is derived from one source and is still wrong — "
      "which would mean the derivation, not the typing, is the defect."),

    L("L-248", "ALL", None,
      "A SCRIPT THAT RUNS CLEAN AND WRITES NOTHING IS THE MOST CONVINCING FALSE CONFIRMATION "
      "THERE IS, BECAUSE IT LOOKS EXACTLY LIKE THE WORK SUCCEEDING.",
      "An exit code of zero is not evidence that anything happened. This is [R-ENF-04]'s "
      "empty-result rule pointed at your own hands rather than at a gate: the check that "
      "the fix landed has to be the ARTEFACT, not the command.",
      "correcting a figure label, 03-Sep-2026",
      "build",
      "A study's figure label typed a date beside a computed price and got it eleven days "
      "wrong. The fix went into figures.py, figures.py was run, it exited 0 and printed "
      "nothing — and the fix had not landed, because that module defines drawing functions "
      "and has NO main block, so running it as a script does nothing at all. The images are "
      "built by a separate build_figures.py that calls those functions, and the document "
      "embeds the images by filename without rebuilding them, so a change to the drawing "
      "code reaches a reader through TWO steps that nothing enforces. It was caught only by "
      "rendering the page again and looking at it, where the old date was still printed. "
      "The delivered document had been rebuilt in between and reported CLEAN by its own "
      "scrub and column audit, because both inspect text and the defect was inside a PNG.",
      "A pipeline where the delivered document rebuilds its own figures, so a change to the "
      "drawing code cannot fail to reach the page."),

    L("L-249", "ALL", None,
      "AN INCOME STATEMENT'S SUBTOTALS ARE ROLL-UPS A READER ADDS UP, AND NOT ONE OF THEM "
      "IS LABELLED AS A TOTAL.",
      "A footing check keyed on the word 'total' is blind to the commonest table in this "
      "house. Gross profit, operating profit, profit before tax and profit for the year are "
      "every bit as much sums of the rows above them as a balance-sheet total is, and a "
      "reader adds them up the same way — they just never say so.",
      "reading PHDC's rendered page 4, 03-Sep-2026",
      "build",
      "PHDC's forecast income statement printed Revenue, Cost of revenue, Gross profit, "
      "Overheads and Operating profit, and gross less overheads came out EGP 393mn ABOVE "
      "the printed operating profit in 2026, rising to 1,039mn by 2031. The model computes "
      "EBIT as gross less overheads less DEPRECIATION and the table never printed the "
      "depreciation row. Every figure in it was individually correct and the defect lived "
      "in the RELATIONSHIP between them — the same shape as ARCC's Table 3, which deducted "
      "provisions and credit losses and never printed the line. TWO STUDIES, ONE DEFECT, "
      "FOUND BOTH TIMES BY A PERSON READING. A chain check was built and MEASURED across "
      "1,051 tables and 277 subtotal rows: 53% did not reproduce against revenue, 27% "
      "against the previous subtotal — an income statement is a CHAIN, and re-pointing it "
      "halved the rate without touching a tolerance. It was still one table in four, which "
      "is the permanently-red check [R-ENF-02] forbids, so IT WAS NOT ADOPTED and the "
      "measurement is recorded so the next attempt starts from it.",
      "A discriminator that tells a currency component from a volume or per-unit row "
      "without relying on label words — which is what the residue of that measurement turns "
      "on."),

    L("L-250", "ALL", None,
      "A COMPARATIVE CLAIM IS A CLAIM ABOUT THE TABLE BENEATH IT, AND IT IS THE ONE KIND OF "
      "SENTENCE A READER CAN FALSIFY WITHOUT LEAVING THE PAGE.",
      "\'X moves the answer more than Y\' reads as a summary rather than as an assertion, so "
      "nobody checks it — and every number it depends on is printed directly below. A "
      "figure check reconciles each cell against the model and never asks whether the "
      "sentence above them is true of the cells together.",
      "reading PHDC's rendered page 10, 03-Sep-2026",
      "build",
      "The sensitivity section said \'moving the discount rate by the whole 800 basis "
      "points of the 11 June 2026 edition\'s error changes value by LESS than moving cash "
      "conversion from one observed year to another\', immediately above the grid that "
      "refutes it: 800bp on the three-year-mean row runs 37.40 to 10.24, a move of EGP "
      "27.16 a share, against 11.71 for conversion from 2023-25 to the mean and 22.44 from "
      "the mean to 2024. Wrong in the direction stated. Replaced with a sentence COMPUTED "
      "from the grid, which also says something truer and more useful — the crux is the "
      "conversion rate, but only across its whole observed spread (34.15); one year to the "
      "next moves value less than the discount rate does.",
      "A comparative claim that survives being recomputed from the table it describes — "
      "which is what computing it rather than typing it now guarantees."),

    L("L-251", "ALL", None,
      "A CAPTION THAT NAMES A RULE IS ASSERTING THE PICTURE FOLLOWS IT, AND A PICTURE IS "
      "WHERE A FREE PARAMETER HIDES BEST.",
      "Nothing reconciles a caption against the code that drew the figure. A threshold "
      "chosen to make a chart look right is invisible to every gate this house has, "
      "because no number it produces is ever printed.",
      "reading PHDC's rendered page 10, 03-Sep-2026",
      "build",
      "The heatmap title read \'bold where the cell BRACKETS the EGP 14.40 close\' and the "
      "code marked any cell within EGP 1.20 of it — a different rule, and a free parameter "
      "with nothing behind it. A single cell cannot bracket a value; a PAIR does. The two "
      "rules disagreed visibly on this very grid: the 6.0% row straddles 14.40 between "
      "16.10 and 11.20 and NEITHER cell is within 1.20, so the row a reader most wants "
      "marked was left plain, while the 12.0% row — whose whole span sits above the close "
      "and brackets nothing — carried a bold cell. Same family as the ARCC heatmap whose "
      "title promised bold cells that did not exist. Now the straddling PAIR is bolded, "
      "which is what the word means, needs no threshold, and is checkable.",
      "A figure whose caption names a rule the drawing code does not implement, where the "
      "rule as written cannot be made parameter-free."),

    L("L-252", "ALL", None,
      "A COUNT SPELLED OUT IN WORDS ESCAPES EVERY CHECK THIS HOUSE HAS, AND EVERY STUDY IS "
      "FULL OF THEM.",
      "The numeric-traceability rule matches NUMERALS. \'Five\' is a word, so a count "
      "written that way is invisible to it — and a count is the easiest figure of all to "
      "leave behind, because it changes when a list changes and nothing connects the two.",
      "reading PHDC's rendered page 13, 03-Sep-2026",
      "build",
      "PHDC's section 7 opened \'Five things are not disclosed by the company\' while the "
      "READ FIRST twelve pages earlier COMPUTED the same count from the model and said SIX "
      "— the study contradicting itself in the sentence that introduces the list a reader "
      "is about to count. A sixth gap had been registered and the typed word stayed. Both "
      "now come from one helper. Measured across all 31 delivered studies: 775 spelled-out "
      "counts qualifying a noun, in every study. A general gate was attempted and DECLINED "
      "— of 92 that looked mappable to a committed collection, 74 disagreed and almost "
      "every one was the instrument being wrong (a lenses object holding the central and "
      "two beta-alternates beside the four actual lenses; \'two lenses\' inside a sentence "
      "about a subset). A count word means something only against a collection somebody has "
      "NAMED, so this needs the per-study declaration prose_figures and footing_check "
      "already use.",
      "A rule that maps a count noun in prose to a committed collection without a per-study "
      "declaration — which would make the general gate tractable after all."),

    L("L-253", "ALL", None,
      "A COLUMN AUDIT CANNOT SEE ONE ROW, BECAUSE AN AVERAGE CANNOT: A SINGLE CELL ONE "
      "CHARACTER TOO WIDE WRAPS AFTER ITS MINUS SIGN AND PRINTS A NEGATIVE NUMBER AS A "
      "POSITIVE ONE.",
      "Table-discipline checks measure whether a column is starved or bloated, which is a "
      "property of the column as a whole. The defect here is a property of ONE CELL, and it "
      "changes a figure's SIGN as a reader reads it — the worst possible outcome from a "
      "purely typographic cause.",
      "reading PHDC's rendered appendix, 03-Sep-2026",
      "build",
      "The label column took 4.6cm of 16.2cm, leaving 1.66cm for each of seven years, and "
      "\'-110,168\' is eight characters — one too many. Word breaks a line after a hyphen, "
      "so the 2035 and 2040 cost-of-revenue cells rendered as a BARE DASH with 110,168 on "
      "the line beneath, which a reader takes for a positive number or for a dash meaning "
      "\'not applicable\'. The column audit reported the table CLEAN and was right by its "
      "own lights: the column is not starved on average, and one row is a single character "
      "wider than every other. THE FIRST FIX MADE IT WORSE AND THAT IS THE USEFUL PART — "
      "U+2212 MINUS SIGN is typographically correct and does not offer a break, but it is "
      "WIDER than a hyphen, so every cell in the row then wrapped mid-number. The character "
      "was never the problem. Per [R-COC-01], when a fix makes the thing worse the "
      "diagnosis was wrong: the column was too narrow for its content, and the fix is to "
      "widen it.",
      "A wrapped cell whose cause is genuinely the character rather than the width — which "
      "would mean the substitution was right and the measurement of it was wrong."),

    L("L-254", "ALL", None,
      "WHERE A STUDY COMPUTES A QUANTITY ON SEVERAL BASES AND ADOPTS ONE, EVERY PUBLISHED "
      "FIGURE MUST BE ASSERTED TO COME FROM THE ADOPTED ONE: THE WRONG KEY IS SILENT, "
      "REPRODUCES PERFECTLY, AND READS AS CORRECT.",
      "A study that offers a reader two or three ways of measuring the same thing has to "
      "pick one to answer with. Nothing in the code marks which key is the answer, so a "
      "display that reaches for a neighbouring one produces a number that is individually "
      "right, recalculates to the last cell, and is not the study's answer.",
      "reading TMGH's rendered pages, 03-Sep-2026",
      "build",
      "TMGH deducts the minority at its share of value \u2014 its summary table says so, its "
      "headline range is stated on it, and [R-BRIDGE-01] requires it \u2014 and FIVE separate "
      "displays published the BOOK basis instead: the enterprise-to-equity bridge, whose "
      "lines summed to EGP 244,183mn and whose last row printed 113.24 where 244,183 / "
      "2,060.7 is 118.50; the crux table, whose own caption states 'with the minority "
      "deducted at its share of value' beside numbers that were not; the discount-rate "
      "sensitivity grid, which did not carry the adopted basis at all; the reverse read, "
      "which solved what the traded price implies against a per-share the study does not "
      "publish; and the comparison of the lenses. NOTHING STATED A REASON ANYWHERE \u2014 it "
      "was the key that got written first and copied. Every figure passed the numeric-"
      "traceability gate, the recalculation gate and the prose-figure check, because each "
      "was computed and correct; what was wrong was WHICH of the three it was. The bridge "
      "case is the sharpest: [R-BRIDGE-01] already required the equity to divide to the "
      "stated per share, and the assertion existed in the rule and in no code.",
      "A study where the several bases are genuinely interchangeable for the purpose in "
      "hand, so that reading a neighbouring key changes nothing a reader would act on."),

    L("L-255", "ALL", None,
      "A LOOKUP THAT MATCHES NOTHING BUILDS A TABLE WITH HEADERS AND NO ROWS, AND NOTHING "
      "RAISES, BECAUSE AN EMPTY COLLECTION IS A VALID TABLE.",
      "Code that filters a record into display rows returns an empty list when the "
      "record's keys have moved. The build succeeds, the document is written, and the page "
      "carries a heading, a table frame and a caption with nothing between them.",
      "reading TMGH's rendered pages, 03-Sep-2026",
      "build",
      "TMGH's walk-forward results table asked for keys shaped 'asknown|<driver>|all' "
      "against a scores record whose keys are plain driver names \u2014 a schema borrowed from "
      "another study's file \u2014 matched nothing, and produced an empty list. The delivered "
      "page carried the table's headers and its caption under prose reading 'each driver "
      "scored against what the company actually reported. The results decided which of the "
      "model's habits were corrected'. The record was fine: fifteen drivers, thirty to "
      "forty observations each. The same silence had emptied the record itself one level "
      "up, where the numbers builder iterated the file's TOP-LEVEL keys looking for the "
      "same shape. [R-ENF-04] names this exactly \u2014 an empty result is not a clean result "
      "\u2014 and here the emptiness reached a reader. The fix is an assertion on the row "
      "count, not a corrected key: the corrected key would work until the schema moves "
      "again.",
      "A table legitimately empty on some editions, where a floor on the row count would "
      "be the false claim instead."),

    L("L-256", "ALL", None,
      "A RATIO QUOTED IN PROSE MUST DIVIDE A NUMERATOR BY A DENOMINATOR OF THE SAME PERIOD, "
      "AND A PARAGRAPH CAN MAKE THE MISTAKE IT IS WARNING ABOUT.",
      "Where a sentence gives a reader both operands and the result, the three have to "
      "agree. Where they do not, the sentence refutes itself in front of the reader.",
      "reading TMGH's rendered pages, 03-Sep-2026",
      "build",
      "The paragraph explaining why a finance-cost correction was REFUSED \u2014 on the ground "
      "that the reported charge and the borrowings describe different things \u2014 divided the "
      "FY2025 charge by the borrowings on the 30-JUNE-2026 balance sheet and reported "
      "'about 44%'. That figure reconciles against neither pairing: 3,936.5 over the 16,493 "
      "the same sentence quotes is 23.9%, which is BELOW the policy peak it was being "
      "contrasted with, so the argument as printed refuted itself; and against the "
      "borrowings of the year that BORE the charge it is 33.4%. The correct figure supports "
      "the argument and the printed one destroyed it. This is [R-FCAL-01] trap (i) \u2014 the "
      "interest denominator \u2014 occurring in a paragraph written to explain that very trap.",
      "A ratio whose operands genuinely belong to different periods for a stated reason, "
      "with the mismatch named rather than silent."),

    L("L-257", "ALL", None,
      "A FILE SOMETHING WRITES AND NOTHING READS IS A NUMBER FROZEN AT THE MOMENT SOMEBODY "
      "LAST RAN THE SCRIPT \u2014 THE MIRROR OF [R-ENF-06], AND IT HAS NO VINTAGE TO CHECK.",
      "[R-ENF-06] asks what WRITES a file that a builder reads. The same question the other "
      "way round is worth asking: a file with no consumer has nobody to notice when it goes "
      "stale, and it sits in the study directory looking exactly like a computed record.",
      "reading TMGH's rendered pages, 03-Sep-2026",
      "build",
      "TMGH's statements.json was written by its statements module's main() and read by "
      "nothing \u2014 the numbers builder imports the module and calls build(), so the live "
      "path never touches the file. It sat two days stale, giving 2030 development revenue "
      "of 76,350 against the 102,747 the delivered document prints, a 35% divergence. IT "
      "WAS NOT HARMLESS: sizing a table column needed the widest cell in that row, the "
      "first attempt read this file, got 76,350, concluded the column was wide enough, and "
      "was wrong \u2014 the page had been printing '102,74' with a lone '7' beneath it for two "
      "days. The cheapest fix for a file with no consumer is not to declare its vintage; it "
      "is not to write it.",
      "A written-and-unread file that is genuinely an evidence record rather than a derived "
      "one \u2014 a critique register or a raw download, where freezing is the point."),

    L("L-258", "ALL", None,
      "A COLUMN MUST CLEAR ITS WIDEST TOKEN, HEADER INCLUDED, AND A HEADER IS BOLD, WHICH "
      "IS TWELVE PER CENT WIDER ON THE INK.",
      "L-253 established that a column must clear its widest cell. Two further things were "
      "learned by getting it wrong twice more inside ten minutes: the widest cell is "
      "frequently the HEADER, and the header is set bold, which no plain-text measurement "
      "sees.",
      "reading TMGH's rendered pages, 03-Sep-2026",
      "build",
      "A 'Discount rate' header rendered 'Discou nt rate' at 1.7cm. A hand fix widened that "
      "column and narrowed 'Case' to 3.0cm, which needs 3.61 for 'Credit-default-swap' "
      "\u2014 the same error again, minutes later. The column was then sized from measured "
      "per-character widths and STILL printed 'Discoun', because the measurement had been "
      "taken on plain cells: bold needs 1.077x to 1.121x the ink of the same token plain, "
      "measured on seven tokens. The model was right about the string and wrong about the "
      "FACE IT IS SET IN. The shared width module now holds both measurements and asserts "
      "its constants still clear them at import; a percent sign is 0.30cm, which is why an "
      "entire ten-cell cost-of-capital row printed '32.4' with a bare '%' beneath it while "
      "the orphan detector \u2014 which scans for a stray DIGIT \u2014 reported the document clean.",
      "A renderer whose metrics differ enough from the measured ones that the constants "
      "stop clearing their own experiment, which the module's import assertion would say."),

    L("L-259", "ALL", None,
      "A RELATIVE GLOB RUN FROM THE WRONG DIRECTORY MATCHES NOTHING AND REPORTS CLEAN, AND "
      "IT IS THE COMMONEST WAY [R-ENF-04]'s FAILURE ACTUALLY HAPPENS HERE.",
      "A sweep written as engine/*_study/*.json is correct from the repository root and "
      "matches nothing from anywhere else. The result is not an error: it is a confident "
      "zero, printed in the same words a genuinely clean run would print.",
      "sweeping for stale peer prices, 03-Sep-2026",
      "build",
      "A sweep for artefacts older than the repository's own price libraries reported "
      "'0 stale' and was believed. Counting what it had EXAMINED returned zero rows across "
      "zero studies: the working directory was inside a study, so the glob resolved under "
      "that directory and matched no file at all. Re-run from the root it examined 25 rows "
      "and found the real case. THIS HAPPENED WITHIN THE HOUR OF REGISTERING L-255, which "
      "is the same failure one level up, and twice more in the same session on other "
      "commands. The habit that catches it is cheap and is the only thing that does: "
      "ASSERT THE POPULATION BEFORE READING THE RESULT \u2014 a sweep prints what it "
      "examined, and zero examined is a failure rather than a finding. Absolute paths help "
      "and are not sufficient, because the next probe will be written in a hurry too.",
      "A sweep whose population is genuinely empty for a stated reason, where the assertion "
      "would be the false claim instead."),

    L("L-260", "ALL", None,
      "AN ARTEFACT BUILT FROM A COMMITTED LIBRARY GOES STALE SILENTLY, BECAUSE THE LIBRARY "
      "MOVES BY THE CALENDAR AND THE ARTEFACT MOVES ONLY WHEN SOMEBODY RE-RUNS IT.",
      "A file that reads a price library and writes a summary is correct on the day it is "
      "written and drifts every day after. Nothing about it looks stale: it carries dates, "
      "sources and tiers, and every figure in it was right when it was taken.",
      "reading TMGH's rendered pages, 03-Sep-2026",
      "build",
      "TMGH's delivered peer table published Emaar Misr at 11.53 as at 28 July, SODIC at "
      "27.48 as at 27 July and Orascom at 40.16 as at 27 July, while THIS REPOSITORY'S OWN "
      "committed libraries held 13.70, 31.01 and 41.50 at 1 September \u2014 the first "
      "18.8% higher. The generator does nothing but read the last row of each library and "
      "had simply not been re-run. No valuation number moves, because this study "
      "deliberately tabulates no peer multiples; what moves is a table of prices a reader "
      "takes as current. It is [R-ENF-06]'s shape with the staleness on the INPUT side, and "
      "the standing library-staleness rule's shape too: a fact that moves by the calendar "
      "must not be remembered by something that moves only when edited.",
      "A peer table deliberately frozen at a stated date for a stated reason, which the "
      "document would then have to say."),

    L("L-261", "ALL", None,
      "A FILE SOMETHING WRITES, WHEN NOTHING MAKES IT RUN, IS AS FROZEN AS ONE NOTHING "
      "WRITES AT ALL \u2014 AND HARDER TO SEE, BECAUSE IT HAS A GENERATOR.",
      "[R-ENF-06] asks what writes an artefact a builder reads, and a reassuring answer "
      "closes the question. But a generator that exists and is not run produces exactly "
      "the same stale number, and the study looks better arranged while it happens.",
      "rebuilding TMGH, 03-Sep-2026",
      "build",
      "Four artefacts went stale in one afternoon on a study already conforming to "
      "[R-ENF-06]: statements.json two days behind the model, peers.json five weeks behind "
      "THIS REPOSITORY'S OWN price libraries, experts.json quoting a reverse read that had "
      "since been corrected, and a note added to a generator that never reached the page "
      "because the script writing its file was not re-run after the edit. None was "
      "carelessness about a number; each was the ordinary consequence of a pipeline whose "
      "steps a person has to remember. MEASURED ACROSS THE BOOK, 2 OF 24 STUDIES HAVE A "
      "SINGLE BUILD ENTRY POINT, and the other twenty-two carry 7 to 32 scripts each that "
      "must be run in the right order from memory. The fix is not to remember harder: an "
      "entry point declares the dependency order explicitly and ends with the checks, so a "
      "build that produced a stale artefact cannot also report clean.",
      "A study whose scripts are genuinely independent, where an order does not exist to "
      "be got wrong."),

    L("L-262", "ALL", None,
      "A PRICED ALTERNATIVE THAT RE-RUNS THE BASE CASE SCORES ZERO BY CONSTRUCTION, AND A "
      "ZERO DELTA IS THE ONE ANSWER NOBODY CHECKS.",
      "A table that prices each contested choice by re-running the model with that choice "
      "moved is only as good as the move. Where the alternative is set to what the base "
      "case already uses, the re-run returns the base case, the delta is exactly zero, and "
      "the row reports that the choice does not matter.",
      "reading EGCH's rendered pages, 03-Sep-2026",
      "build",
      "The FIRST row of EGCH's contested-constructions table priced 'country risk off the "
      "sovereign's credit rating' against the traded default swap and scored +0.00. The "
      "study's base case already uses the swap basis \u2014 rf_star_spot IS rf_star_cds and the "
      "published rate IS wacc_cds \u2014 so the alternative re-ran the base case. The labels "
      "were reversed with it: the study CHOOSES the swap basis and the alternative is the "
      "rating basis. Priced correctly the choice is worth EGP 1.26 against a base of 2.31, "
      "a delta of \u22121.05 and the THIRD largest of the ten, in a table whose entire purpose "
      "is to show what each choice is worth. Nothing could catch it: the figure was "
      "computed, the model re-ran, the arithmetic was exact. A NON-ZERO delta invites a "
      "reader to check it; a zero one says there is nothing to look at.",
      "An alternative that genuinely coincides with the base case for a stated reason, "
      "where the row would have to say so rather than print a bare zero."),

    L("L-263", "ALL", None,
      "A TABLE WITH TWO BASIS COLUMNS MUST PRODUCE TWO ANSWERS, AND A DERIVED ROW IDENTICAL "
      "IN BOTH WHILE ITS INPUTS DIFFER IS READING ONE COLUMN TWICE.",
      "Where a table sets out the same construction on two bases side by side, the rows "
      "that are INPUTS may legitimately be identical \u2014 a beta, a cost of debt, a set of "
      "weights \u2014 but a row DERIVED from rows that differ cannot be.",
      "reading EGCH's rendered pages, 03-Sep-2026",
      "build",
      "EGCH's cost-of-capital table set out the rating and swap bases in two columns whose "
      "costs of equity differ (30.99% against 29.28%), and printed 25.76% for the cost of "
      "capital in BOTH \u2014 because the rating cell read wacc_path[0], which IS the published "
      "rate and IS the swap basis. The rating figure reproduces from its own rows as 66.2% "
      "x 30.99% + 33.8% x 18.86% = 26.88%, and the printed one does not. The note beneath "
      "compounded it, saying the rating basis was carried 'as the more conservative' when "
      "the study carries the swap basis and that basis is 113 basis points LOWER. The "
      "table-footing instrument could not see it: the row is a weighted mean whose weights "
      "are a ROW formatted as a combined string, not a column it can read.",
      "A derived row that genuinely coincides across two bases, which would need saying."),

    L("L-264", "ALL", None,
      "A TABLE THAT NAMES ITS OPERATIONS IN WORDS IS GIVING A READER INSTRUCTIONS, AND "
      "FOLLOWING THEM MUST ARRIVE WHERE THE PAGE SAYS.",
      "\"Plus net cash\", \"Less depreciation and amortisation\", \"Add back the "
      "impairment\" are instructions, not labels. A reader will carry them out. Where a "
      "line the model uses is not printed, the reader arrives somewhere the page does "
      "not \u2014 and nothing about the page looks wrong, because every figure on it is "
      "correct.",
      "reading SCEM's rendered pages, 04-Sep-2026",
      "build",
      "Five tables in one study, in a document that had passed table_footing, "
      "prose_figures, the recalculation gate, the scrub and the column audit. The "
      "enterprise-to-equity bridge printed \"Enterprise value 6,617\", \"Plus net cash "
      "4,930\", \"Equity value 11,426\" while deducting EGP 120mn of minority in the "
      "model and printing no line for it. The cash-flow waterfall printed depreciation, "
      "capital expenditure and working capital between NOPAT and free cash flow \u2014 "
      "three lines that feed only the balance-sheet projection \u2014 while the model "
      "builds free cash flow as NOPAT less reinvestment, so a reader adding the column "
      "reached 1,829 in year one against a printed 799. Three lenses jumped from an "
      "enterprise figure straight to value per share: dividing the printed earnings by "
      "the printed share count gives 39.66 against a printed 58.10.",
      "A delivered waterfall whose printed rows reach its printed answer while a line "
      "the model uses is still missing, which would mean the arithmetic closes by "
      "coincidence."),

    L("L-265", "ALL", None,
      "WHERE A PAGE CANNOT SAY ENOUGH FOR A CHECK TO BE SOUND, MOVE THE CHECK TO WHOEVER "
      "KNOWS \u2014 DO NOT WEAKEN IT UNTIL IT PASSES.",
      "A check firing on work that is right has three possible answers and only one is "
      "honest. Widening its tolerance is a free parameter. Changing the work to satisfy "
      "it corrupts what is being measured. The third is to ask what the check is "
      "actually measuring, and point it at something that can be reproduced.",
      "building the waterfall instrument, 04-Sep-2026",
      "build",
      "The page-side reading of a waterfall was built first and measured twice over the "
      "whole book: 42.4% of all 979 tables on the first design, whose matches were "
      "coincidence against a pool of several thousand committed numbers, and 30.7% of "
      "the 127 tables carrying an operator row on the second, after two further "
      "re-pointings that were each the instrument being wrong about how tables work. The "
      "residue is irreducible because a statement mixes labelled and unlabelled steps: "
      "an income statement runs Revenue, EBITDA, margin, depreciation, \"Plus other "
      "operating income\", EBIT, and EBIT is EBITDA LESS that depreciation PLUS that "
      "income \u2014 the page performs the subtraction and never says so. The check "
      "moved to the builder, which knows the anchor because it put it there.",
      "A page-side reading that reaches an honest rate on this book, which would mean "
      "the ambiguity is in the implementation rather than in what a page can state."),

    L("L-266", "ALL", None,
      "AN EXCEPTION TO A CHECK IS DECLARED WITH A REASON OR IT IS THE CHECK SWITCHED "
      "OFF.",
      "Every instrument in this house lets a study declare a legitimate exception. The "
      "reason is not decoration on the declaration \u2014 it IS the declaration, because "
      "an exception with no reason is indistinguishable from a defect somebody waved "
      "through, and nobody can tell the two apart afterwards.",
      "building the waterfall instrument, 04-Sep-2026",
      "build",
      "waterfall() accepts a figure the table does not print and REFUSES when no reason "
      "is supplied with it, which is [R-COC-01 AMENDED]'s closed-mechanism clause and "
      "table_footing's own declaration rule arriving at the same place from three "
      "directions. Its first use is the one line in the study that a reader genuinely "
      "cannot add up \u2014 a first forecast year scaled to the part of the year still "
      "unearned at the valuation date \u2014 which the caption already named and which "
      "is now declared to the instrument in the same words.",
      "An exception class where the reason is genuinely mechanical and stating it adds "
      "nothing, which would need to be shown rather than asserted."),

    L("L-267", "ALL", None,
      "A TABLE USES ONE SIGN CONVENTION FOR ITS DEDUCTIONS, AND A LABEL SAYING \"LESS\" "
      "OVER A FIGURE THE MODEL ADDS IS WRONG WHATEVER THE ARITHMETIC DOES.",
      "A deduction can be printed in parentheses, as a signed negative, or as a bare "
      "magnitude. Any one of the three is clear. Two of them in one table means a reader "
      "does not know whether to take the magnitude off or add the sign \u2014 and the "
      "same row printing 855 in one year and -4,550 in the next, under one label, is "
      "something nobody can read correctly.",
      "measuring the delivered documents, 04-Sep-2026",
      "build",
      "Nine of the 100 tables in the book that carry a deduction row print two "
      "conventions at once, and in every one of the nine the row breaking the convention "
      "is a working-capital line the model ADDS while its label says \"Less\". One "
      "prints \"(2,650)\", \"(360)\", \"(792)\", \"(1,012)\" and then \"440\", so "
      "a reader following the labels reaches 3,488 against a printed 4,368 \u2014 twenty "
      "per cent of that year's cash flow. Three of the nine switch convention between "
      "adjacent years in a single row. The semantic defect beneath it is the real one: "
      "\"Less INCREASE in working capital\" over a release states the opposite of what "
      "happened.",
      "A table whose two conventions are two different quantities rather than two "
      "readings of one \u2014 a rate beside its amount, which the check already "
      "distinguishes and which is why it distinguishes them."),

    L("L-268", "ALL", None,
      "COMPUTE THE WHOLE NEW FILE BEFORE OPENING ANYTHING FOR WRITING \u2014 AN OPEN IN "
      "WRITE MODE TRUNCATES BEFORE THE EXPRESSION BESIDE IT IS EVALUATED.",
      "open(path, 'w').write(f(text)) evaluates the open FIRST. If f() then raises, the "
      "file is already empty and the exception looks like nothing happened. Build the "
      "new text in full, and only then open the file.",
      "truncating a study builder to zero bytes, 04-Sep-2026",
      "build",
      "A patch script applying the same edit to six builders wrote "
      "io.open(p,'w').write(add_import(s)); on the second file add_import raised because "
      "that builder has no sys.path preamble, and the traceback was the only sign that "
      "the file had already been emptied \u2014 1,023 lines gone, recovered from git "
      "because it happened to be committed. Nothing about the error message mentioned "
      "the file.",
      "A write path where the truncation genuinely cannot precede the failure, such as "
      "writing to a temporary file and renaming it, which is the stronger form of this "
      "same discipline."),

    L("L-269", "ALL", None,
      "A TEMPLATE IS AN UNWRITTEN RULE WITH NOBODY CHECKING IT, AND IT TRANSMITS EVERY "
      "PROPERTY IT HAPPENS TO HAVE.",
      "Where a process propagates by imitation \u2014 open this document beside the one "
      "you are writing \u2014 the thing imitated IS the standard, whatever the documents "
      "say. It carries not the rules somebody remembered to write down but everything the "
      "template contains, including the constructions later rules retired.",
      "measuring the model report against the ratchets, 04-Sep-2026",
      "build",
      "The exemplar every study in this house is modelled on was outstanding on EIGHT "
      "ratchets at once \u2014 among them lens design, so it still publishes the typed "
      "four-lens blend that rule retired, and the valuation gap, where it is listed "
      "UNREADABLE, meaning that gate cannot recover a central and a spot from the "
      "document every other study is copied from. Not one of those entries was wrong; "
      "that is what a ratchet is for. Nothing was counting them on THIS study, and a "
      "ratchet entry on the exemplar is a debt every study written afterwards owes "
      "without anybody deciding to take it on.",
      "A house whose studies are written from the rules rather than from a template, "
      "where the exemplar's own state would stop propagating."),

    L("L-270", "ALL", None,
      "THE OLDEST RULES ARE THE LEAST CHECKED, BECAUSE THEY PREDATE THE MACHINERY.",
      "A rule adopted before there was any way to enforce it does not acquire enforcement "
      "by being important. It acquires it when somebody goes back and asks which of the "
      "old rules are still running on trust.",
      "auditing SIGCM clause 1 from outside, 04-Sep-2026",
      "build",
      "SIGCM clause 1 \u2014 historicals from the company's own filings, never a vendor "
      "or press \u2014 predates every enforcement rule in the standing protocol, was "
      "never in doubt, and was checked only by a boolean each study set on itself. Two "
      "delivered studies were in plain breach. One took its revenue, profit and balance "
      "sheet from trade press and an aggregator while its audited statements sat on the "
      "company's own website, six PDFs one click from the homepage: equity EGP 6,020.3mn "
      "filed against 5,240.0mn used, cash 4,762.3mn against 3,850.0mn, depreciation "
      "122.5mn against 418.1mn \u2014 every error understating the company.",
      "An old rule found to have been enforced all along by something nobody had "
      "noticed, which would mean the audit should look for the enforcement before "
      "assuming its absence."),

    L("L-271", "ALL", None,
      "TRY THE COMPANY'S OWN WEBSITE. IT IS USUALLY THERE.",
      "Before any aggregator, before any press report, before concluding a filing cannot "
      "be obtained: fetch the company's own site and list its links. The rule has said so "
      "since August 2026 and the cost of not doing it is measured in whole studies.",
      "fetching SCEM's audited statements, 04-Sep-2026",
      "build",
      "Sinai Cement's homepage carries six audited financial statements as direct PDF "
      "links \u2014 FY2022 through FY2025 and the reviewed Q1-2026 \u2014 with no "
      "authentication and no investor-relations portal to navigate. The study valuing the "
      "company had used trade press and an aggregator for every historical, and its sweep "
      "register logs no attempt on the site either way, which the primary-source rule "
      "requires even when the attempt fails.",
      "A company whose site genuinely carries nothing, where the attempt is logged as a "
      "failure and the escalation ladder runs \u2014 which is the rule working, not a "
      "counter-example to it."),


    L("L-272", "ALL", None,
      "A CONSTRUCTION THAT IS ONLY HARMLESS BECAUSE THE INPUT IS SMALL IS STILL WRONG.",
      "It is tempting to leave a defect alone when it moves the answer by a basis point. "
      "The next study to copy the construction may not have a small input, and it will "
      "copy the defect with the shape rather than with the number.",
      "the SCEM rebuild, 04-Sep-2026",
      "build",
      "Three defects on one study each moved the answer by well under one per cent and "
      "each was a real error of construction: a cost of debt 81 basis points BELOW the "
      "sovereign that taxes the company on a book that is 0.5 per cent of capital; a "
      "Hamada re-levering applied to an already-levered beta; and a terminal beta the "
      "workbook computed one way and the model another. The same cost-of-debt error was "
      "found on AMOC where it was equally immaterial, and the reason given there for "
      "fixing it is the reason here: a rule obeyed only when it is expensive is not a "
      "rule.",
      "A construction whose defect is bounded by arithmetic rather than by the size of "
      "the input \u2014 where the shape itself cannot go wrong at any input."),

    L("L-273", "ALL", None,
      "A SENSITIVITY GRID MUST REPRODUCE THE ANSWER AT ITS OWN CENTRE.",
      "A sensitivity is the base case with one driver moved. If the unmoved cell does "
      "not reproduce the published figure, the grid is answering a different question "
      "from the study, and every cell in it looks perfectly reasonable while it does.",
      "the SCEM rebuild, 04-Sep-2026",
      "build",
      "SCEM's grid ran the explicit window on the RETIRED reinvestment identity while the "
      "base case ran the sanctioned waterfall, so its zero-shift cell read EGP 109.82 "
      "against a published 128.80, fifteen per cent apart. Its own code comment recorded "
      "that the TERMINAL had been re-pointed at the sanctioned module and the explicit "
      "window had been left behind. Nothing noticed because no assertion tied the grid to "
      "its own centre; three one-line asserts now do, and they are the whole fix.",
      "A grid that deliberately answers a different question \u2014 an alternative "
      "construction published as such \u2014 which is then not a sensitivity and is not "
      "labelled as one."),

    L("L-274", "ALL", None,
      "A PROBE THAT READS ZERO IS A PROBE THAT DID NOT RUN.",
      "When a check reads a cell by address and the sheet moves, it does not fail. It "
      "reads blank space as zero, and every comparison against a zero base comes out at "
      "zero difference, which reads as a pass.",
      "the SCEM rebuild, 04-Sep-2026",
      "build",
      "Retiring a typed lens blend moved the central from a SUM of weighted lenses at "
      "D10 to the primary lens at C12. The driver test kept opening D10, read 0.000, and "
      "reported all 51 drivers passing. A recalculation row pointed at a cell that had "
      "become the maintenance charge compared 958.83 against 0.1923 and passed a relative "
      "tolerance in neither direction anybody read. Both are the same shape as L-067 and "
      "both were caught by asserting that no headline probe may read nothing.",
      "A quantity that is legitimately zero, which none of a price, a rate or a cash flow "
      "in a valuation is \u2014 where one exists, the assertion names it rather than "
      "being relaxed."),

    L("L-275", "CLASS", CEM,
      "AN OLD PLANT'S RECENT CAPEX IS NOT ITS MAINTENANCE REQUIREMENT.",
      "A company that has been spending a third of what replacing its plant at today's "
      "prices would cost is deferring, not economising \u2014 and a forecast cannot "
      "spend that little AND run the kilns harder every year. Those are two assumptions "
      "that cannot both be true.",
      "the SCEM rebuild, 04-Sep-2026",
      "build",
      "Sinai Cement's own cash-flow statements average EGP 303.2mn a year of capital "
      "spending against a current-cost maintenance requirement of EGP 958.8mn on the "
      "disclosed life \u2014 3.2x apart, on a plant whose note 4 shows 59.7 per cent of "
      "cost written down, machinery 68.4 per cent, and EGP 379.4mn fully depreciated AND "
      "STILL IN USE. Replacement cost is 7.9x the book cost because the plant was built "
      "in pre-devaluation pounds. Charging the recent run rate flat while utilisation "
      "climbs from 71.0 to 79.1 per cent was worth EGP 5.16 a share, against the value.",
      "A genuinely young plant, where net book value is a large fraction of cost and the "
      "gap between recent spend and replacement maintenance is the ordinary under-spend "
      "of an asset not yet needing renewal."),


    L("L-276", "ALL", None,
      "THE 1/g TERMINAL DEFECT POINTS THE OTHER WAY IN A LOW-INFLATION MARKET.",
      "Building a terminal on the reinvestment identity makes the implied asset life the "
      "reciprocal of the growth rate. Everyone here learned that as a rule that CHARGES "
      "TOO MUCH, because it was found on high-inflation names. In a pegged two per cent "
      "economy the same arithmetic makes every asset last fifty years and charges far too "
      "little. Which way it bites is a fact about the currency, not about the asset.",
      "the ADNOCLS re-issue, 04-Sep-2026",
      "build",
      "The construction charges g x IC every year for ever, so the implied replacement "
      "cycle is 1/g. At Egypt's 7 per cent terminal that is 14.3 years against a "
      "disclosed 25-year cement plant, and the correction RAISED value on ARCC and SCEM. "
      "At the dirham's pegged 2 per cent it is 50 years against a disclosed 25-year ship, "
      "and the correction LOWERS it. Of the thirteen studies carrying the construction, "
      "the implied cycles run from 14.3 years to 66.7 — every one of them the reciprocal "
      "of that market's terminal inflation and none of them a fact about the assets.",
      "A market whose terminal inflation happens to coincide with its assets' disclosed "
      "life, where the defect is invisible because the two agree by accident."),

    L("L-277", "CLASS", SHIP,
      "A FLEET'S DISCLOSED HULL LIFE IS NOT ITS MAINTENANCE LIFE.",
      "Shipping accounts state a hull life of twenty-five years or so, and the company's "
      "own realised depreciation runs far above what that implies. The gap is not an "
      "error: dry-docking is capitalised and written off over two to five years, and "
      "dry-docking IS maintenance. A terminal that charges hull replacement while adding "
      "back all book depreciation adds back the amortisation of a cost it never charged.",
      "the ADNOCLS re-issue, 04-Sep-2026",
      "build",
      "Rebuilding ADNOCLS's terminal on the sanctioned module at the disclosed 25-year "
      "vessel life produced an implied payout of 117 per cent of terminal profit — a "
      "going concern distributing more than it earns for ever — and the module refused "
      "it. The study's own input register already carried the reason, that dry-docking "
      "components are written off over two to five years. The disclosure splits neither "
      "the vessel line by type nor the charge by component, so the life that would "
      "reconcile the two cannot be derived from the filings and none was invented.",
      "A fleet operator whose statements disclose the dry-docking component separately, "
      "where the hull cycle and the maintenance charge can be built apart and the "
      "reconciliation is arithmetic rather than an open question."),


    L("L-278", "ALL", None,
      "A NEGATIVE CONTROL THAT NAMES A LIVE RATCHET ENTRY HAS AN EXPIRY DATE ON IT.",
      "A ratchet may only ever shorten. So a control case built by reaching into a live "
      "ratchet and moving whichever entry it was written around stops being constructible "
      "the day that entry is cleared — and then it fails for a reason that has nothing to "
      "do with the property it tests, which reads exactly like failing for the right one. "
      "Plant the starting state; do not assume it.",
      "clearing the exemplar's last ratchet entries, 04-Sep-2026",
      "build",
      "Three controls broke this way in one day. The delivered-PDF control removed a named "
      "study from a ratchet to prove the gate then fires, and that study had just been "
      "pruned off it. Two cases of the exemplar-debt control did the same: one needed "
      "ADNOCLS on the gap gate's unreadable list to move it, and one needed it on the "
      "macro ratchet to remove it, and the morning's work had cleared both. Each now "
      "either reads the entry off the list at run time or plants its own, and asserts the "
      "mutation landed either way.",
      "A control whose case genuinely requires a specific historical entry — where the "
      "case is about that entry rather than about the property, and should say so."),

    L("L-279", "ALL", None,
      "A GATE SWEEP THAT SKIPS THE NEGATIVE CONTROLS IS A DIFFERENT POPULATION FROM CI.",
      "Running every scripts/check_*.py and excluding the ones ending "
      "_negative_control feels like running the gates, because it is where the gates "
      "live. CI runs both. A sweep built from a pattern the operator chose reports on the "
      "population the operator chose.",
      "the ADNOCLS re-issue, 04-Sep-2026",
      "build",
      "A hand-rolled sweep of 44 gates reported 0 red while the CI step list reported one: "
      "the exemplar-debt negative control, excluded by the sweep's own pattern. This is "
      "the same defect scripts/run_ci_gates.py was written for on 3 September 2026, when a "
      "by-hand sweep reported green against a CI that had been red for a day — anchor the "
      "population somewhere else. The remedy is to run that script rather than a pattern, "
      "and it is cheap.",
      "Nothing. The controls are part of the suite; a sweep that omits them is measuring "
      "something narrower and should say which."),

    L("L-280", "ALL", None,
      "A DEFECT MEASURED ONLY WHERE IT HURTS LOOKS LIKE A BIAS WITH A DIRECTION. "
      "Measure it where it should run the other way before correcting it anywhere.",
      "The retired terminal charges the growth rate against invested capital every "
      "year for ever, so the replacement cycle it implies is one divided by that rate "
      "— a fact about the CURRENCY and not about the asset. In a high-inflation market "
      "that is 14 years and it starves a 25-year plant; in a pegged one it is fifty "
      "years and it buys half the maintenance a 25-year ship needs. Same identity, "
      "opposite sign. Correcting it raises value in one market and LOWERS it in the "
      "other, and a house that had only ever measured the painful side would read a "
      "correction with a single sign as obviously right.",
      "The terminal census across the delivered book, 03/04-Sep-2026",
      "build",
      "Seven of thirteen readable terminals charge LESS than their own book "
      "depreciation, which cannot be maintaining an asset base because book "
      "depreciation is struck on historical cost and replacement costs more — and "
      "every one of the seven is in a pegged low-inflation market. The worked "
      "correction on a high-inflation name RAISED its value; the measured correction "
      "on the exemplar would LOWER it. Three of the eight names held below the price "
      "are also names whose terminal under-charges, so on those the correction moves "
      "the answer AWAY from the price and the pessimism is somewhere else. Read the "
      "current split live from the census; the names move at every rebuild.",
      "A market where the correction runs the same way as in every other, which would "
      "make this a bias rather than a sign change. Or a disclosed asset life that "
      "happens to equal one divided by the terminal inflation rate, which would mean "
      "the identity was measuring the asset after all."),

    L("L-281", "ALL", None,
      "A LOCAL CI RUNNER INHERITS THE DEVELOPER'S ENVIRONMENT AND CI DOES NOT, so "
      "green locally is not evidence about CI.",
      "Running the pipeline's own step list on this machine looks like the strongest "
      "possible pre-flight check, and for logic it is. For anything that depends on a "
      "TOOL being present it is worthless in the reassuring direction: the local "
      "machine has accumulated every tool anybody ever needed, and the build machine "
      "starts from a manifest somebody has to remember to update.",
      "The gate sweep of 04-Sep-2026 against the CI run of the same commit",
      "build",
      "The local sweep reported 89 steps green. CI failed the same commit: "
      "poppler-utils was installed 320 lines below the step that needed it, and "
      "matplotlib was never installed at all, so every one of 27 figure scripts "
      "failed to import. Both tools were present locally, so neither gate could have "
      "gone red here however carefully the sweep was run.",
      "A local runner that builds its own environment from the workflow's manifest "
      "rather than using the machine's, which would make the two comparable again."),

    L("L-282", "ALL", None,
      "A GATE THAT CANNOT RUN HAS REFUSED NOTHING, AND MUST NOT BE COUNTED AS "
      "PERMISSIVE. Give a broken tool its own exit code and its own words.",
      "When a check fails there are two very different repairs: fix the thing being "
      "checked, or fix the machine the check runs on. A runner that lumps them "
      "together sends every reader to the first one, and the second is invisible "
      "until somebody reads the log three times.",
      "The new-study gauntlet in CI, 04-Sep-2026",
      "build",
      "The gauntlet reported 3 gates did not refuse a new study. All three had "
      "refused nothing because a tool they needed was absent, and each said so in its "
      "own output while the summary line said the opposite. That is the gauntlet's own "
      "first-run finding arriving a second time — a gate red for the wrong reason "
      "reads exactly like one red for the right reason. Exit 2 now means the tool is "
      "missing, and the run still fails, under a heading that points at the "
      "environment.",
      "A failure mode where the repair really is the same either way, which would make "
      "the distinction ceremony."),

    L("L-283", "ALL", None,
      "AN ID SCHEME THAT ENCODES A PROPERTY STOPS ENCODING IT AND NOTHING ANNOUNCES "
      "THE MOMENT IT DID.",
      "Numbering a register so the number tells you the kind of entry is convenient "
      "until the blocks fill. Then somebody allocates past the boundary, quite "
      "reasonably, and from that day the number means nothing while every comment "
      "still says it does — and the code that does the allocating is the last thing to "
      "find out.",
      "The lessons register's own id minter, 04-Sep-2026",
      "build",
      "The minter's docstring read 0xx for one scope, 1xx for another, 2xx for the "
      "third, and allocated inside a 99-wide window per scope. The first block had "
      "long since overflowed into the others, so the window arithmetic would have "
      "minted an id already in use. It never got that far: it CRASHED on a suffixed "
      "id — a correction inserted in place in an append-only register, legitimate "
      "under that convention and unreadable by int() — so the sanctioned path for "
      "appending any harvested lesson raised before it reached the register. Now "
      "counted against the whole register, which is the rule this house already holds "
      "for every other population.",
      "A register where the scope really is recoverable from the id, which would make "
      "the blocks load-bearing rather than decorative."),

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
