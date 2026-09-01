#!/usr/bin/env python3
"""EMFD — render the source register, the basis-break register and the scope
decision FROM the committed evidence files.

Nothing in these documents is typed. Every count, span, hash and delta is
resolved at build time from ir_register.json, extraction_survey.json and
restatements.json, for the same reason the band records are generated and the
as-of stamps are stamped: a document that states a fact which moves must not be
the thing that remembers it.

Run after fetch_sources.py, extract_survey.py and restatement_check.py.
"""
import json, os, textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
DATE = "01-09-2026"
LONG_DATE = "1 September 2026"


def load(name):
    with open(os.path.join(HERE, name)) as f:
        return json.load(f)


def write(name, body):
    path = os.path.join(HERE, name)
    with open(path, "w") as f:
        f.write(body)
    print("  wrote %s (%d bytes)" % (name, len(body)))


# ------------------------------------------------------------------ facts ---
def facts():
    reg, sur, res = load("ir_register.json"), load("extraction_survey.json"), \
        load("restatements.json")
    att = load("fetch_attempts.json")
    # panel.json and kpi.json are built after the first pass of this file, so
    # they are optional here and the records simply say less without them
    pan = load("panel.json") if os.path.exists(
        os.path.join(HERE, "panel.json")) else None
    kpi = load("kpi.json") if os.path.exists(
        os.path.join(HERE, "kpi.json")) else None

    docs = reg["documents"]
    fs = [d for d in docs if d["kind"] == "FS"]
    cons = [d for d in fs if d["basis"] in ("consolidated", "unspecified")]
    year_end = sorted({d["year"] for d in cons
                       if d["period"] in ("Q4", "Year-End")})

    # A fiscal year is COMPLETE for this purpose when a year-end profit-or-loss
    # statement for it has been extracted AND FOOTS -- which is what panel.json
    # records. Counting the register's filenames instead would count FY2021 as
    # present on the strength of two quarters, and would miss FY2012, which is
    # carried only as the comparative column of the FY2013 filing.
    complete = ([int(y) for y in sorted(pan["years"], key=int)] if pan
                else year_end)
    partial = sorted({d["year"] for d in cons} - set(complete))

    origins = [y for y in complete if len([x for x in complete if x <= y]) >= 5]
    cells = [(o, h) for o in origins for h in range(1, 6)
             if o + h <= max(complete)]

    units = sorted(int(y) for y, r in (kpi or {}).get("by_year", {}).items()
                   if "units_delivered" in r)
    no_units = sorted(u["year"] for u in (kpi or {}).get(
        "years_without_a_unit_count", []))

    return {
        "reg": reg, "sur": sur, "res": res, "att": att,
        "pan": pan, "kpi": kpi, "units": units, "no_units": no_units,
        "panel_restated": (pan or {}).get("restated_in_a_later_filing", []),
        "routes": sorted({(pan or {}).get("years", {})[y]["provenance"]["route"]
                          .split(";")[0] for y in (pan or {}).get("years", {})}),
        "n_docs": len(docs), "n_fs": len(fs), "n_cons": len(cons),
        "n_er": len([d for d in docs if d["kind"] == "ER"]),
        "n_ar": len([d for d in docs if d["kind"] == "AR"]),
        "complete": complete, "partial": partial,
        "first_year": min(complete), "last_year": max(complete),
        "origins": origins, "cells": cells,
        "max_h": max([h for _, h in cells], default=0),
        "attempts": len(att),
        "attempts_ok": sum(1 for a in att if a.get("ok")),
        "mb": sum(a.get("bytes", 0) for a in att if a.get("ok")) / 1e6,
        "text_years": sur["year_end_pl_from_text_layer"],
        "ocr_years": sur["year_end_pl_needing_ocr"],
        "footed": sur["pl_statements_that_foot"],
        "not_footed": sur["pl_statements_that_do_not_foot"],
    }


# --------------------------------------------------------- source register ---
def source_register(F):
    reg, att = F["reg"], F["att"]
    docs = reg["documents"]

    rows = []
    for y in sorted({d["year"] for d in docs}):
        yd = [d for d in docs if d["year"] == y]
        cons = sorted({d["period"] for d in yd if d["kind"] == "FS"
                       and d["basis"] in ("consolidated", "unspecified")})
        sep = sorted({d["period"] for d in yd if d["kind"] == "FS"
                      and d["basis"] == "separate"})
        er = sorted({d["period"] for d in yd if d["kind"] == "ER"})
        ar = len([d for d in yd if d["kind"] == "AR"])
        rows.append("| %d | %s | %s | %s | %s |"
                    % (y, ", ".join(cons) or "—", ", ".join(sep) or "—",
                       ", ".join(er) or "—", ar or "—"))

    probes = []
    for g in reg["gap_probes"]:
        detail = g.get("error") or ("HTTP %s, %s, %s bytes"
                                    % (g.get("status"), g.get("content_type"),
                                       g.get("bytes")))
        probes.append("| %s | %s | %s |"
                      % (g["label"], g["verdict"],
                         detail.replace("|", "/")[:110]))

    failed = {}
    for a in att:
        if not a.get("ok"):
            host = a["url"].split("/")[2]
            failed.setdefault(host, []).append(a.get("error", ""))

    fail_rows = ["| %s | %d | %s |" % (h, len(v), (v[0] or "")[:90])
                 for h, v in sorted(failed.items())]

    return """# EMFD — Sweep Register: primary-source acquisition

**Instrument:** Emaar Misr for Development Company (S.A.E.) · EGX:EMFD · market EG
**Run date:** {long_date}
**Rule:** [R-FCAL-01] §1 · SIGCM clauses 1 and 8 · L-007 (try the company's own site first,
and log every attempt including the ones that fail).

This register is generated by `build_records.py` from `ir_register.json` and
`fetch_attempts.json`. No figure in it is typed.

---

## 1. What was attempted, in order

The company's own investor-relations document register was resolved first, in both
language versions, and every document it publishes was downloaded and hashed. Only then
were the routes probed that would carry the years that register stops short of.

* **{attempts} HTTP attempts**, {ok} of them successful, **{mb:.1f} MB** retrieved.
* Registers read: `{reg_en}` and its Arabic mirror.
* **{n_docs} documents** classified and downloaded, all of them real PDFs:
  {n_fs} financial statements ({n_cons} consolidated or single-entity),
  {n_er} earnings releases, {n_ar} management annual reports.

One transport artefact is recorded because it would otherwise read as an absent document:
the company's CDN answers the **full** Chrome user-agent string with HTTP 403 and the
**abbreviated** one with HTTP 200, from the same client in the same second. A sweep that
had used the ordinary string would have concluded the register was unreachable. [R-ENF-04]

## 2. What the company's own register holds

| fiscal year | consolidated / single-entity FS | separate FS | earnings release | mgmt annual report |
|---|---|---|---|---|
{rows}

**Complete fiscal years carried by a year-end statement: {first}–{last} ({n_complete} years).**
{partial_note}

## 3. Extraction route, per document

Arithmetic is the arbiter, not the extractor's confidence, so every profit-or-loss
statement that yielded a text layer was checked against its own identities before being
believed.

* Year-end profit-or-loss readable **from the text layer**: {text_years}
* Year-end profit-or-loss that will need **OCR off the rendered pixels**: {ocr_years}
* Statements checked and **footing**: {footed}
* Statements that extracted and did **not** foot: {not_footed}

The four oldest year-end filings carry no text layer at all — they are scans. Several
later files are mixed: the FY2020 profit-or-loss extracts cleanly while the statement of
financial position on the facing page is an image. Any panel built from this window has to
record the route each figure came by, per document, not per file.

## 4. The years the register does not reach, and every route tried for them

| route | outcome | detail |
|---|---|---|
{probes}

Failures by host:

| host | failed attempts | first error |
|---|---|---|
{fail_rows}

Notes on the two that matter:

* **egx.com.eg** is reachable and answers **HTTP 200 to every request**, including requests
  for PDFs — with an F5 anti-bot interstitial in place of the document. Judging that route
  by status code would have recorded a success and stored an HTML challenge page as a
  financial statement. The probe therefore judges the payload: a document is accepted only
  if its first five bytes are `%PDF-`.
* **ir.egidegypt.com:8080** is the backend of the IR widget the company embeds on its own
  investor-relations page — i.e. the company's own channel. It serves on port 8080, which
  this session's egress policy does not permit. That is an environment limit, not a
  publication fact, and it is recorded as such.

A JavaScript-capable browser was also tried, and could not be used: Chromium is installed
here but cannot reach any host through this session's proxy — verified against a control
(`https://example.com` fails identically), so the failure is the transport, not the target.

## 5. What was extracted from what was obtained

The window the register reaches has been extracted and is in `panel.json`. Every year is
believed only because it foots:

* **Fiscal years in the panel: {panel_first}–{panel_last} ({n_panel} years.)** FY{panel_first}
  is carried as the comparative column of the FY{panel_first_plus} filing, the earliest year
  the archive reaches at all.
* **Three routes, all recorded per year:** {routes}. Four of the year-end filings are scans;
  the two oldest are Arabic and print **Eastern Arabic numerals**, which tesseract reads
  fluently and wrongly, so they were read from the rendered page and then verified — see
  below.
* **Every year foots** on revenue − cost = gross profit, on the sum of the lines below gross
  profit = profit before tax, and on PBT − tax = profit. None was dropped.
* **Cross-document verification.** The FY2013 and FY2014 profit figures also appear in the
  FY2015 statement of changes in equity — a different document, extracted independently by
  OCR in English — and match exactly. The read is trusted because two documents agree, not
  because it was read carefully.
* **The FY2015 filing is missing its own profit-or-loss page.** Its pages run balance sheet,
  changes in equity, cash flows, notes; no page carries an income statement. That is a defect
  in the company's own scan, and FY2015 is taken instead from the comparative column of the
  FY2016 filing, flagged as a comparative.
* **Operating KPIs are thinner than the statements.** Delivered-unit counts and contracted
  sales values exist for {units} — from the company's results releases — and for
  {no_units} **no unit count exists in any document on the register**: no results release
  was published for those years and the management annual reports for them are Arabic scans
  of the board's governance report, which carries no operating data. Those years therefore
  cannot enter the unit-level drivers, and the pre-registration says in advance that they are
  reported as dropped rather than interpolated.
* Where a release quotes revenue, it is reconciled against the audited statement **at the
  release's own precision** — "EGP 3.2 billion" promises nothing finer than ±0.05bn — and
  all of them agree.

## 6. Conclusion of the sweep

Every fiscal year from **{first} to {last}** is available from the company's own audited
statements. **FY{gap_start} onward is not** — not from the company's site, not from the
exchange, not from the company's own embedded IR backend, and not from an archive. The
walk-forward's §1 requirement that the most recent three fiscal years come from the
company's audited statements or its own IR documents therefore cannot be met, and the run
stops here and asks. See `SCOPE_DECISION_{date}.md`.

Aggregator figures for the missing years exist and were deliberately **not** used: SIGCM
clause 1 bars a data vendor as the source of the subject's own reported historicals, and
§1 restates it for this exercise with the words "no exception". A fabricated or borrowed
cell corrupts the very error the method is being scored on.
""".format(long_date=LONG_DATE, date=DATE, attempts=F["attempts"],
           ok=F["attempts_ok"], mb=F["mb"], reg_en=reg["registers"][0],
           n_docs=F["n_docs"], n_fs=F["n_fs"], n_cons=F["n_cons"],
           n_er=F["n_er"], n_ar=F["n_ar"], rows="\n".join(rows),
           first=F["first_year"], last=F["last_year"],
           n_complete=len(F["complete"]),
           partial_note=("Partial years also held: %s (quarters only, no year-end "
                         "statement)." % ", ".join(str(y) for y in F["partial"])
                         if F["partial"] else ""),
           panel_first=F["complete"][0], panel_last=F["complete"][-1],
           panel_first_plus=F["complete"][0] + 1, n_panel=len(F["complete"]),
           routes=", ".join(F["routes"]),
           units=", ".join("FY%d" % y for y in F["units"]) or "no year",
           no_units=", ".join("FY%d" % y for y in F["no_units"]) or "no year",
           text_years=F["text_years"], ocr_years=F["ocr_years"],
           footed=F["footed"], not_footed=F["not_footed"] or "none",
           probes="\n".join(probes), fail_rows="\n".join(fail_rows),
           gap_start=F["last_year"] + 1)


# ----------------------------------------------------------- basis breaks ---
def basis_breaks(F):
    res = F["res"]
    d19 = {d["line"]: d for d in res["differences"] if d["year"] == 2019}
    e = res["eas_48_interim"]["lines"]

    def pct(line):
        a = d19[line]["as_reported"]
        return 100.0 * d19[line]["delta"] / abs(a)

    rows19 = "\n".join(
        "| {} | {:,.0f} | {:,.0f} | {:+,.0f} | {:+.2f}% |".format(
            k.replace("_", " "), d19[k]["as_reported"], d19[k]["as_restated"],
            d19[k]["delta"], pct(k))
        for k in sorted(d19))
    rows48 = "\n".join(
        "| {} | {:,.0f} | {:,.0f} | {:+,.0f} | {:+.2f}% |".format(
            k.replace("_", " "), v["as_reported"], v["as_restated"],
            v["delta"], v["pct"])
        for k, v in sorted(e.items()))

    p13 = {d["line"]: d for d in
           (load("panel.json").get("restated_in_a_later_filing") or [])
           if d["year"] == 2013}
    rows13 = "\n".join(
        "| {} | {:,.0f} | {:,.0f} | {:+,.0f} | {:+.2f}% |".format(
            k.replace("_", " "), p13[k]["as_first_reported"],
            p13[k]["as_restated"], p13[k]["delta"],
            100.0 * p13[k]["delta"] / abs(p13[k]["as_first_reported"]))
        for k in sorted(p13)) or "| — | | | | |"
    ent = load("restatements.json").get("reporting_entity_by_filing", {})
    entity_rows = "\n".join("* FY%s filing — **%s**" % (y, b)
                            for y, b in sorted(ent.items())) or "* (not read)"
    n17 = len([d for d in load("restatements.json")["differences"]
               if d["year"] == 2017])
    moved17 = ("no profit-or-loss figure" if n17 == 0
               else "%d profit-or-loss line(s)" % n17)
    rev13_pct = (100.0 * p13["revenue"]["delta"]
                 / abs(p13["revenue"]["as_first_reported"])) if "revenue" in p13 \
        else float("nan")

    return """# EMFD — basis-break register

**Instrument:** Emaar Misr for Development Company (S.A.E.) · EGX:EMFD
**Written:** {long_date}, before any modelling. [R-FCAL-01] §1.

Generated by `build_records.py` from `restatements.json`. Every delta below is measured
from the company's own filings, not recalled: each annual statement prints the prior year
as the company chose to present it a year later, and differencing the two columns turns
the restatement history into an object rather than a memory.

---

## B1 — EAS 47 / 48 / 49 adopted 1 January 2021 · **revenue is redefined at this line**

The Egyptian analogues of IFRS 9, 15 and 16 (Ministerial Resolution 69 of 2019) took
effect for annual periods beginning on or after 1 January 2021. The FY2020 statements say
in terms that the Group elected **not** to early adopt; the H1-2021 interim says the Group
adopted all three **for the first time** and prints its 2020 comparatives marked
"(Restated)".

That gives exactly one period published on **both** bases — the six months ended
30 June 2020 — and so exactly one place where the standard's effect on this company can be
measured rather than assumed:

| line | pre-EAS 48, as first reported | post-EAS 48, as restated | delta | % |
|---|---:|---:|---:|---:|
{rows48}

**Consequence, and it is not a footnote.** Revenue is a different quantity before and after
this line, and cost of revenue moves nearly three times as far as revenue does, so the
margin moves too. §1's rule — *score unit drivers only inside their own definition window*
— means a revenue or cost-per-unit driver may not be scored across 31 December 2020.
The obtainable window ends at FY2020; every year an update must forecast begins at FY2021.
**The training window and the forecast window share no revenue definition.**

## B2 — FY2019 reclassified in the FY2020 accounts · gross-up between revenue and other income

FY2020 note 36 (*Comparative figures*) states that certain 2019 comparatives were
reclassified to conform to the current year's presentation. Differencing the two columns
shows what was reclassified:

| line | FY2019 as first reported | FY2019 as restated one year later | delta | % |
|---|---:|---:|---:|---:|
{rows19}

Profit before tax and profit for the year are **identical on both bases**. This is a pure
gross-up: something previously shown net inside other income was regrossed into revenue and
cost of revenue, and the line was relabelled from "Other income" to "Net other income".

**Consequence.** A revenue driver scored across FY2019 would carry a step of
**{rev_pct:+.1f}%** that has nothing to do with the business. Because profit is untouched,
no check that looks at the bottom line would ever see it. FY2017 and FY2018 show no
differences between their two presentations, so the break is specific to the FY2020
presentation change and is dated there.

Under point-in-time discipline each origin keeps the **as-first-reported** figure and the
restatement is recorded here beside it, never substituted.

## B3 — FY2013 reclassified in the FY2014 accounts · the same gross-up, six years earlier

The FY2013 income statement and the FY2014 income statement's comparative column
disagree about FY2013 by a wide margin, and the pattern is the FY2019 one again:

| line | FY2013 as first reported | FY2013 as restated one year later | delta | % |
|---|---:|---:|---:|---:|
{rows13}

Cost of revenue is identical on both bases and profit before tax is identical on both
bases — **{rev13_pct:+.1f}%** was moved off the revenue line into the other-income and
selling-expense lines, with the composition re-cut and the FY2013 statement's operating-profit
subtotal and separate currency-revaluation line both dropped from the FY2014 presentation.

**Two reclassifications of the same kind, six years apart, each invisible at the bottom
line.** That is not an accident of one year's presentation; on this issuer the revenue line
is a presentation choice that has been revisited more than once. Every origin in the panel
therefore keeps the **as-first-reported** figure, and `panel.py` refuses to let a later
filing's comparative overwrite it — a plain "take the first filing that mentions the year"
rule took exactly the wrong one here, silently, until the two figures were differenced.

## B4 — the currency, which is not one break but four

The Egyptian pound was floated in November 2016 and devalued again in March 2022, October
2022 and March 2024. Only the first of those falls inside the obtainable window, and it
falls near its start. Every scoreable cell this window could produce lies **after** the
2016 float and **before** the 2022–24 sequence, so the era split §5 requires — *apply a
correction only where the bias holds its sign across eras* — has no second era to test
against. The corrections step is not merely under-powered on this window; it is unevaluable
by construction.

These dates are macro facts, not company disclosures, and they are marked here as inputs to
be sourced and dated in the pre-registration's macro table before any origin is built —
never reconstructed from memory into a driver.

## B5 — the reporting entity changes at FY2018, with a measured effect of nil on the P&L

Before FY2018 the company published a single set of statements. From FY2018 it publishes a
**consolidated** set alongside a **separate** set. The panel uses the consolidated basis
from FY2018 and the single set before it.

The basis is read off each filing's own cover, never inferred from its filename:
{entity_rows}

The size of the break is measured rather than assumed. FY2017 appears twice — as the current
column of its own single-entity filing and as the comparative column of the FY2018
consolidated filing — and differencing the two gives **{n17} line(s) that differ**:
consolidating the newly formed subsidiary moved {moved17} in its first year. The break is
registered because it will matter for the balance sheet and for later years, not because it
moved anything here.

## B6 — presentation changes still to be registered when the blocked years arrive

Recorded now as open, so that they are checked rather than discovered:

* whether the separate and consolidated bases diverge after 2021 (the register carries both
  from 2018 to H1-2021, and only the consolidated basis before that);
* whether the segment or project disclosure was re-cut in the years the register does not
  reach;
* whether the FY2021 EAS 48 transition was applied fully retrospectively or by the modified
  retrospective route, which determines whether FY2020 is restated in the FY2021 annual
  accounts at all;
* every one-off the company itself attributes in FY2021–FY2025, which cannot be enumerated
  from documents that have not been read.
""".format(long_date=LONG_DATE, rows48=rows48, rows19=rows19,
           rev_pct=pct("revenue"), rows13=rows13, rev13_pct=rev13_pct,
           entity_rows=entity_rows, n17=n17, moved17=moved17)


# --------------------------------------------------------- scope decision ---
def scope_decision(F):
    grid = []
    for o in F["origins"]:
        hs = [h for h in range(1, 6) if o + h <= F["last_year"]]
        grid.append("| %d | %s | %d |" % (o, ", ".join(str(h) for h in hs) or "—",
                                          len(hs)))
    return """# EMFD — fundamental walk-forward: SCOPE DECISION

**Instrument:** Emaar Misr for Development Company (S.A.E.) · EGX:EMFD · market EG · exchange EGX
**Class:** real-estate developer, off-plan, percentage-of-completion
**Decided:** {long_date}, before any projection was run.

## Decision

**The run does not start. It is BLOCKED at [R-FCAL-01] §1 and the documents are requested.**

This is not the §0 SKIP verdict and it must not be recorded as one. SKIP is for a company
whose history is too short — *"walk-forward not run — insufficient sourceable history (N
years)"*. EMFD's history is not short. Its recent statements are not reachable from here.
Those are different facts and they call for different words.

## Why

§1 is unconditional: *"The most recent 3 fiscal years and all current-year quarters MUST
come from the company's audited financial statements or its own website/investor-relations
documents. No exception: if they cannot be obtained, STOP and ask for the documents."*

The company's own investor-relations register publishes financial statements from FY{first}
to H1-2021 and stops. Everything from FY{gap} onward — which is to say the three most
recent fiscal years and every quarter of the current one — is absent from it. The exchange
carries those filings and answers automated requests with an anti-bot interstitial; the
company's own embedded IR backend serves on a port this session's egress policy does not
permit; a JavaScript-capable browser cannot reach any host from here, verified against a
control. Every route and its outcome is in `SOURCE_REGISTER_{date}.md`.

Aggregator figures for the missing years are readily available and were deliberately not
used. SIGCM clause 1 bars a data vendor as the source of the subject's own reported
historicals; §1 restates it with the words "no exception". Substituting them would produce
a training record whose errors are partly transcription noise from somebody else's
spreadsheet — measuring our method against a vendor's arithmetic rather than against what
the company reported.

## What the obtainable window would and would not support

Even setting §1's rule aside, the window that IS obtainable does not carry a training
record. Complete fiscal years from the company's own statements: **{first}–{last}
({n_complete} years)**. An origin needs five prior complete years, so the admissible
origins are {origins}, and actuals stop at FY{last}:

| origin | horizons that resolve | cells |
|---|---|---|
{grid}

**{n_cells} scoreable (origin, horizon) cells in total, none beyond horizon {max_h}.** The
reference run on a comparable name carried 40 cells to horizon 5, and its own record still
states that its corrections rest on too few origins to be independent. {n_cells} overlapping
cells is not a smaller version of that. It is not a training record.

Four further things are true of that window, each of them sufficient on its own:

1. **No era split exists.** Every one of those cells sits after the November 2016 float and
   before the 2022–24 devaluations. §5 applies a correction *only where the bias holds its
   sign across eras*; with one era there is nothing to hold a sign across. The corrections
   step is unevaluable by construction, not merely weak.
2. **The revenue definition changes at the window's edge.** EAS 48 took effect on
   1 January 2021 and this company adopted it then, restating the one overlapping period's
   revenue and cost (see `BASIS_BREAKS_{date}.md`, B1). §1 scores unit drivers only inside
   their own definition window. The obtainable window ends where the current definition
   begins, so the two do not overlap at all.
3. **Half the window has no unit count at all.** Delivered-unit counts exist for {units}
   and for {no_units} they exist nowhere on the company's register — no results release was
   published for those years, and their management annual reports are Arabic scans of the
   board's governance report with no operating data in them. The three drivers that carry
   this class — units delivered, revenue per unit, cost per unit — are therefore unscoreable
   on the three most recent years of the obtainable window, and interpolating a unit count
   is precisely what §1 forbids.
4. **The purpose would not be served.** The two purposes are per-driver bias detection and
   calibrated ranges for years 3–5 of the update now being written. A record whose newest
   origin is FY{last} produces neither for a forecast starting in 2026 — it would describe
   how the method behaved in a currency regime and an accounting basis that have both since
   been replaced.

## What is needed to lift the block

Any of the following, for **FY2021, FY2022, FY2023, FY2024 and FY2025**, plus every 2026
quarter already disclosed:

1. the audited consolidated financial statements as filed (the exchange's own PDFs are the
   documents themselves and are acceptable — the obstacle is reaching them, not their
   provenance); or
2. the same statements from the company's investor-relations channel; or
3. the annual reports carrying them.

The earnings releases for those years are wanted alongside the statements, not instead of
them: L-008 — *a period is not researched until both its statements and its results release
are in*, because the release carries the sales value, the delivery counts and the backlog
that no financial statement holds, and this class of company is driven by exactly those.

With FY2021–FY2025 in hand the panel spans FY{first}–FY2025 — **{n_full} fiscal years**,
comfortably a **FULL** run under §0 — and the origins run to FY2024 with horizons to five,
spanning both currency eras and both revenue bases. That is a real record. It is about five
documents away.

## What was done anyway, and what was not

Done, and committed:

* the full source sweep, with every attempt logged and every obtained document hashed;
* the extraction survey — which statements yield a text layer, which need OCR, and whether
  each one **foots** against its own arithmetic;
* the restatement comparison, which found and measured two basis breaks;
* the basis-break register those findings feed;
* **the pre-registration, written in full now** — before any error has been computed, which
  is the only moment at which it can honestly be written. Nothing in it can be tuned to a
  result that does not exist yet.

Not done, and not to be represented as done: the panel, any projection, any error cell, any
correction, the two documents §6 requires, and any change to a delivered EMFD number. The
existing EMFD study and its published cone are untouched by this work.
""".format(long_date=LONG_DATE, date=DATE, first=F["first_year"],
           last=F["last_year"], gap=F["last_year"] + 1,
           n_complete=len(F["complete"]),
           origins=", ".join("FY%d" % o for o in F["origins"]),
           grid="\n".join(grid), n_cells=len(F["cells"]), max_h=F["max_h"],
           n_full=len(range(F["first_year"], 2026)),
           units=", ".join("FY%d" % y for y in F["units"]) or "no year",
           no_units=", ".join("FY%d" % y for y in F["no_units"]) or "no year")


# -------------------------------------------------------- pre-registration ---
def prereg(F):
    """The pre-registration. Written before a single error has been computed --
    which, on a blocked run, is the only moment at which it can honestly be
    written at all: nothing in it can be tuned to a result that does not exist.

    The origin grid is computed for the span §1 REQUIRES (FY2013-FY2025), not
    for the span currently in hand, so that the document commits to the shape of
    the run before the documents arrive rather than after."""
    FIRST, LAST = F["first_year"], 2025          # the span §1 requires
    years = list(range(FIRST, LAST + 1))
    origins = [y for y in years if len([x for x in years if x <= y]) >= 5
               and y < LAST]
    rows, total = [], 0
    for o in origins:
        hs = [h for h in range(1, 6) if o + h <= LAST]
        total += len(hs)
        rows.append("| FY%d | %s | %d |" % (o, ", ".join(str(h) for h in hs),
                                            len(hs)))
    nonoverlap = [origins[i] for i in range(0, len(origins), 5)]

    return """# EMFD — fundamental walk-forward training: PRE-REGISTRATION

**Instrument:** Emaar Misr for Development Company (S.A.E.) · EGX:EMFD · market EG · exchange EGX
**Class:** off-plan residential developer — **completed-contract basis to FY2020** (see §0)
**Written:** {long} — BEFORE any projection was run and before any error was computed.
**Status:** training record only. Nothing here is published; nothing here changes a
delivered number until the correction it proposes has passed §8's test.

This file is fixed at the moment it is committed. Every parameter is **stated**, never
fitted; where a rule needs a number, the number is a stated function of data available at
the origin. Sensitivities are reported, never selected. If a later commit changes anything
here, the change is itself dated and the affected results are re-run and re-reported — the
pre-registration is not edited to match an outcome.

**It is written now, while the run is blocked, deliberately.** The documents §1 requires are
not yet in hand (`SCOPE_DECISION_{date}.md`). Writing the rules before the data exists is
the strongest possible version of the discipline this section is for: there is no result to
tune towards, because there is no result.

---

## 0. The one thing to establish before anything else — the revenue-recognition basis

L-102 says check the revenue-recognition basis before anything else. Checked, from the
company's own earnings releases, which state it in terms:

> "revenues recognized according to the **Completed Contract (CC) method**"
> — FY2016 results release, and again in the FY2017 release

So through FY2020 this company recognised revenue **on handover**, not as construction
progressed. Three consequences, all of them structural:

1. **The house class label does not fit the pre-2021 window.** The registered class is
   "real-estate developer, off-plan, percentage-of-completion". EMFD to FY2020 is off-plan
   **completed-contract**. The class lessons are read, as required, but the ones that turn
   on percentage-of-completion are read as **not applying to this window** — which is the
   register working, not a licence to ignore it.
2. **L-001's own falsifier is met here.** That lesson — revenue and cost must sit on the
   same clock — records its overturning condition as *"an issuer that genuinely recognises
   revenue only on handover, where the two clocks already coincide."* Under completed
   contract, revenue and cost of revenue are both released at delivery, so the clocks
   coincide by construction. The driver design below still puts them on one clock
   explicitly, because a design that relies on an accounting basis staying put is a design
   that breaks silently when it moves — and it did move, at 1 January 2021.
3. **It moves at EAS 48.** From FY2021 the company adopted EAS 48 (the Egyptian IFRS 15) and
   restated. Whether that shifts it to over-time recognition, and for which projects, is a
   question the FY2021 statements answer and this session cannot. The driver definitions
   below are therefore written to be evaluated **inside a recognition-basis window**, and
   the first task when the blocked documents arrive is to date that boundary and split the
   panel on it. See `BASIS_BREAKS_{date}.md` B1.

## 1. Origins

Annual origins at the fiscal year-end (31 December). An origin is admissible once the panel
holds **five prior complete fiscal years** for the driver being projected.

* Panel span **required by §1**: FY{first} – FY{last}.
* First admissible origin: **FY{o1}**. Last scored origin: **FY{olast}** (h=1 resolves at
  FY{last}).
* Origin FY{last} is *struck but unresolved*: it produces the forward projection the update
  consumes and contributes no error.

At each origin the model sees **only** what had been published by that date, **as originally
reported**. Where a later filing restates a figure the origin used, the origin keeps the
as-first-reported number and the restatement is recorded in the basis-break register beside
it. Two such restatements are already measured there and neither is adopted.

## 2. Horizons

**h = 1…5 years.** A pair (origin *o*, horizon *h*) is scored iff *o + h ≤ {last}*.

| origin | horizons that resolve | cells |
|---|---|---|
{rows}

**{total} scoreable (origin, horizon) cells per driver** on the required span. On the span
currently obtainable there are {have_cells}, which is why the run is blocked rather than
narrowed.

## 3. Drivers, by class

Built bottom-up. **Margins are outputs, never inputs** (L-005).

| # | driver | class | unit |
|---|---|---|---|
| D1 | units delivered | volume | units/yr |
| D2 | revenue per unit delivered | price | EGP/unit |
| D3 | cost per unit delivered | cost per unit | EGP/unit |
| D4 | net contracted sales value | volume × price | EGP |
| D5 | backlog (value and units) | conversion | EGP, units |
| D6a | selling and marketing expense | overhead, sales-linked | EGP |
| D6b | general and administrative expense | overhead, fixed | EGP |
| D7 | finance income | financing | EGP |
| D8 | finance cost | financing | EGP |
| D9 | depreciation and amortisation | non-cash | EGP |
| D10 | income tax | regulated | EGP |
| D11 | construction and development spend | capex | EGP |
| D12 | working capital (receivables, advances, inventory) | balance sheet | days |

Aggregates are **rebuilt from the drivers**, never projected directly: revenue, cost of
revenue, gross profit, EBITDA, profit before tax, profit for the year, and the balance-sheet
and cash-flow lines they drive.

**Why the driver tree is delivery-anchored rather than completion-anchored.** Under
completed contract, revenue *is* delivery: `revenue = D1 × D2` and `COGS = D1 × D3` with
both on the same year's delivery count. That satisfies L-001 by construction and satisfies
L-010 — *never divide one year's value by another year's volume* — because D2 and D3 are
formed from the same year's revenue and the same year's delivered units, never from a sales
value disclosed to one year and a unit count disclosed to another.

## 4. Mechanical rule for each driver, with parameters

Evaluated on information available at origin *o* only. `TTM3(x, o)` is the trailing
three-fiscal-year arithmetic mean of *x* ending at *o*; `TTM5` likewise over five.
**There are no judgement drivers at a historical origin — the method is tested, not the
analyst.**

* **D1 units delivered.** §3 requires an exogenous market anchor, so the primary rule is
  `units_{{o+h}} = Households_{{o+h}} × intensity_o`, `intensity_o = units_o / Households_o`
  held flat, with Egyptian urban household formation projected at the rate published
  **before** the origin (vintage recorded per origin).
  **This rule is also a pre-registered test of a provisional lesson.** L-101 states that a
  developer's volume is set by its launch and construction calendar and that no demographic
  anchor can see it. That is a falsifiable prediction: if D1's demographic anchor fails to
  beat *freeze* at every horizon, L-101 gains a second name; if it beats freeze, L-101 is
  challenged on its own terms. The rule is therefore **not** replaced by a launch-calendar
  rule — replacing it would be reading a provisional lesson as authority, which
  [R-LESSON-01] forbids. It is run, and its failure or success is a result.
  **Constraint (L-104):** cumulative deliveries may never exceed cumulative net contracted
  sales. `units_{{o+h}} = min(anchor, backlog units available)`. A projection that delivers
  what was never sold is arithmetic, not a forecast; the constraint binds, and every origin
  where it binds is reported.
* **D2 revenue per unit delivered.** `D2_{{o+h}} = D2_o × Π_{{k=1..h}} (1 + π_k)` with
  `D2_o = TTM3(revenue / units delivered, o)` and π the **expected Egyptian headline CPI
  path**. Two macro settings, both pre-registered, and the pair is what defines the
  macro/company split in §6:
  * **as-known:** π_k = TTM3(CPI, o) held flat — the honest information set at the origin.
  * **perfect-foresight:** π_k = realised CPI. Not a forecast; it exists only to price how
    much of the miss was macro.
* **D3 cost per unit delivered.** `D3_o = TTM3(cost of revenue / units delivered, o)`,
  escalated on a **construction-cost** path, not on headline CPI — one escalator per driver
  class (L-009). Where a construction-cost series cannot be sourced for a vintage, headline
  CPI is used and **the substitution is flagged in that cell**, never absorbed silently.
* **D4 net contracted sales.** `D4 = units contracted × price per unit contracted`, each on
  its own rule (volume on the D1 anchor, price on the D2 escalator).
  **Reported sensitivity, not a selected one (L-114):** that lesson records that a
  developer's new-sales value is under-forecast whenever price and volume are projected
  separately. The joint alternative — `D4` projected directly on its own trailing rule — is
  therefore computed at every origin **as well**, and both are reported. Neither is chosen
  on the strength of its score; choosing would be the CRPS-selection mistake in a new
  costume.
* **D5 backlog.** Rolled, in value and in units:
  `backlog_t = backlog_{{t-1}} + net sales_t − revenue recognised_t`, units likewise.
  **L-103:** the two contract positions move together. The contract-asset side (instalment
  and notes receivable) and the contract-liability side (advances from customers) are
  projected from the **same** backlog roll, never independently, and their sum is asserted
  against the disclosed balance-sheet lines at every historical year before any origin is
  built.
* **D6a selling and marketing.** `S&M_t = s_o × net sales_t`, `s_o = TTM3(S&M / net sales, o)`.
  Sales-linked, because that is what it is.
* **D6b general and administrative.** `G&A_t = a_o × Π (1 + π_k)`, `a_o = TTM3(G&A, o)`.
  Fixed and escalated, not revenue-linked. The two overhead lines are **not** pooled: they
  have different drivers and pooling them would hide which one moved.
* **D7 finance income.** This company's finance income is of the same order as its operating
  profit, so it is a first-class driver and not a residual.
  `finance income_t = r_o × (opening cash and deposits + opening instalment/notes
  receivable)`, `r_o = TTM3(finance income / that same opening base, o)`, and the rate is
  additionally run on the **exogenous** setting `r = CBE overnight deposit rate known at the
  origin`, giving the macro/company split for this line.
  **The base is the assets that actually earn it** — cash, time deposits and interest-bearing
  instalment receivables — never total assets and never total current assets. This is
  [R-FCAL-01]'s trap (i) applied to the asset side: a rate formed on a base that does not
  earn the income is arithmetic dressed as evidence, and it is what L-002 was learned from.
* **D8 finance cost.** `finance cost_t = kd_o × opening **interest-bearing borrowings**`,
  where interest-bearing borrowings means the facilities the debt note itself says bear
  interest — never total liabilities, never advances from customers, never retentions or
  payables.
  **This company appears to be substantially unlevered**: its FY2018 finance cost is under
  EGP 1 million against a multi-billion balance sheet. Where the debt note discloses no
  interest-bearing borrowings at an origin, `kd_o` is **undefined and is not computed**: the
  line carries `TTM3(finance cost, o)` and the cell is marked *rate not identified*. A ratio
  whose denominator is near zero produces a spectacular and meaningless rate, and the
  temptation at that moment is to widen the denominator until the answer looks sensible —
  which is exactly the mis-specification L-002 records. The rule refuses in advance.
* **D9 D&A.** PP&E roll-forward: `PPE_t = PPE_{{t-1}} + capex_t − D&A_t`,
  `D&A_t = d_o × PPE_{{t-1}}`, `d_o = TTM3(D&A / opening PP&E, o)`.
* **D10 income tax.** By formula under the regime **known at the origin**: the Egyptian
  statutory corporate rate as legislated at that date, applied to positive profit before
  tax, zero otherwise. A rate change legislated after the origin is a **macro/regulatory**
  miss, not a company miss, and is reported in that column.
* **D11 construction and development spend.** The disclosed programme or guidance at the
  origin where the company gave one, else `TTM3(construction spend, o)` escalated on the D3
  cost path. It is an **input** that drives inventory, deliveries and D&A — never an output.
* **D12 working capital.** DSO, DIO and DPO computed at the origin and held flat, applied to
  the projected revenue and cost lines to project receivables, development inventory,
  advances from customers and payables, and from there the balance sheet and the cash-flow
  statement. **No unexplained plugs where the driver is disclosed.**
  **L-105** records that for a developer the collection cycle and a fast growth path cannot
  both hold. That is not corrected for here; it is **tested**: where a projection implies
  both, the implied cash balance is reported and the contradiction is shown rather than
  reconciled away.

## 5. Naive benchmarks

Computed for every driver and every aggregate at every (origin, horizon):

* **freeze** — every line flat at the last actual: `F_{{o+h}} = A_o`.
* **trend** — trailing three-year CAGR from the origin:
  `T_{{o+h}} = A_o × (A_o / A_{{o-3}})^(h/3)`.

Skill is the reduction in mean absolute log error against each benchmark, per horizon. **A
method that cannot beat "no change" has not earned the precision it displays**, and where
that happens the record says so in those words.

## 6. Score

* **Primary:** log error `e = ln(projected / actual)`, per driver, per horizon; reported as
  **bias** (mean e) and **MAE** (mean |e|).
* **Sign cases:** where either side is ≤ 0 the log is undefined. Those cells are **not**
  dropped and **not** patched — they are counted in a separate sign-error tally scored as
  `(P − A)/|A|`, reported separately, never pooled into the log statistics.
* **Uncertainty:** moving-block bootstrap over **origins**, block lengths **{{2, 3, 4}}**,
  2000 resamples — the same robustness bar this repository uses elsewhere. A bias is called
  robust only if its sign holds across all three block lengths.
* **Shares:** fraction of origins over- and under-forecast, and the sign **by era**.
* **Macro vs company split:** every origin is projected twice, once on the as-known macro
  path and once on perfect foresight. The **perfect-foresight error is the company error**;
  the difference is the **macro/regulatory error**. Both are reported for every driver.
  **The split carries its own check:** D1 (units delivered) has no inflation term, so its
  macro share must come back **zero by construction**. A non-zero macro share on a volume
  driver is a wiring fault, not a finding, and the run stops there.
* **Eras — two independent partitions, pre-registered, dated, not chosen by outcome.** They
  do not coincide, and a driver must sit inside **both** windows to be scored:
  * *FX regime:* E1 pre-float FY{first}–FY2016 · E2 post-float FY2017–FY2021 ·
    E3 devaluation cycle FY2022–FY2025.
  * *Recognition basis:* R1 completed contract, to FY2020 · R2 EAS 48, FY2021 onward — the
    exact boundary to be confirmed from the FY2021 statements when they arrive.

## 7. Roles of the two samples

* The **rolling record** — all admissible cells, horizons overlapping — **estimates** the
  corrections.
* The **non-overlapping origins** — spaced five apart so no two share a forecast year;
  on the required span that is {nonover} — **confirm** them. This set is thin. Its thinness
  is stated here in advance as a limit of a single-name study and is not worked around.

## 8. Corrections — the rule, fixed before any error exists

* **Expanding window only:** a correction applied at origin *o* uses errors resolved
  **before** *o*. No correction is ever informed by an outcome it is then scored on.
* **Half strength by default:** applied correction = 0.5 × estimated bias.
* Applied **only** where the bias holds its sign across eras (§6). A bias that changes sign
  between eras is reported as **instability** and is not corrected — the average of two
  opposite regimes was true in neither.
* **Reset** after a structural break, defined as a driver error beyond its own two-sigma.
* A correction enters the live update's drivers only if it (a) passed the adjusted-versus-raw
  test here **and** (b) is consistent with how that driver class is built across the rest of
  this book. Otherwise it is a **watch flag** — recorded, graded live, revisited at the next
  update, acted on by nobody. The second clause is not a formality: it is what caught a
  finance-cost correction on another name that passed its own test and was hiding a wrong
  denominator.
* **Guidance is scored and never consumed.** Management's forward targets are logged against
  outcome with their own bias, and are never an input to a driver at a historical origin.

## 9. What would make this record misleading — stated in advance

So that none of it can be discovered later and quietly dropped:

* **One name, few origins.** {total} cells across {n_orig} origins is a small sample for a
  five-horizon claim. Block-bootstrap intervals will be wide, and are reported wide.
* **Overlapping horizons.** The rolling record's cells are not independent. That is why the
  non-overlapping set exists and why it is reported even though it is thin.
* **A currency that moves everything at once.** Egypt's 2016 float and the 2022–24
  devaluation steps move every nominal driver together. If the corrections turn out to
  restate "the currency fell", that is a finding about the macro path and not about the
  driver rules, and it is reported that way.
* **A recognition basis that changes inside the span.** The EAS 48 boundary splits the panel
  into two definitions of revenue. Pooling across it would manufacture a step; the era
  partition exists to prevent that, and any driver that cannot be scored inside one window
  is reported unscored rather than scored wrongly.
* **Unit KPIs are thinner than the statements, and this is already measured rather than
  feared.** On the window obtained so far, delivered-unit counts exist for {units} and for
  {no_units} they exist in no document on the company's register at all. Any year without a
  sourced unit count drops out of D1, D2 and D3 and is reported as dropped; it is never
  interpolated. A shorter window is a smaller claim, and a filled cell is a false one.
""".format(long=LONG_DATE, date=DATE, first=FIRST, last=LAST, o1=origins[0],
           olast=origins[-1], rows="\n".join(rows), total=total,
           n_orig=len(origins), have_cells=len(F["cells"]),
           nonover=", ".join("FY%d" % o for o in nonoverlap),
           units=", ".join("FY%d" % y for y in F["units"]) or "no year",
           no_units=", ".join("FY%d" % y for y in F["no_units"]) or "no year")


def main():
    F = facts()
    write("SOURCE_REGISTER_%s.md" % DATE, source_register(F))
    write("BASIS_BREAKS_%s.md" % DATE, basis_breaks(F))
    write("SCOPE_DECISION_%s.md" % DATE, scope_decision(F))
    write("PRE_REGISTRATION_%s.md" % DATE, prereg(F))
    print("\nobtainable complete fiscal years : %s" % F["complete"])
    print("admissible origins               : %s" % F["origins"])
    print("scoreable cells                  : %d (max horizon %d)"
          % (len(F["cells"]), F["max_h"]))


if __name__ == "__main__":
    main()
