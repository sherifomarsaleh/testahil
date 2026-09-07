"""The inputs a VALUE is rebuilt from at each of this run's origins.

Committed beside the driver panel under [R-FCAL-01 AMENDED] (03-09-2026). GENERATED
from this run's OWN committed artefacts — balance_sheet.json, panel.json and
extraction_survey.json — and never hand-edited: an artefact every reader consumes
and nothing writes is a number frozen at the date somebody typed it [R-ENF-06].

WHAT THIS RUN IS, AND WHY THE BLOCK IS WRITTEN ANYWAY. The run is BLOCKED at
[R-FCAL-01] section 1 — the three most recent fiscal years cannot be obtained from
the company's own audited statements or its own investor-relations documents — and
no forecast has been made, no error computed and no delivered number moved. The
amendment binds forward, and this directory is where the forward binding lands: the
statements FY2016-FY2020 have already been parsed cell by cell, so carrying the six
items out of them is a COPY rather than new research, and a figure not written down
at the time is not merely inconvenient afterwards, it is gone. Nothing here is a
driver, a score or a value.

THE TWO REFUSALS THIS FILE MAKES, AND THEY ARE THE POINT OF IT

  capex and depreciation are MISSING AT EVERY ORIGIN, and the reason is one fact
  rather than five: this run extracted the profit-or-loss page and the statement of
  financial position and NOT the cash-flow statement — its own panel says so in its
  own words — and the extraction survey could not even LOCATE a cash-flow page in
  any of the five filings. The identity capex = change in PPE + D&A cannot supply
  it either: the change in PPE is available from FY2017 onward and the D&A term is
  not available at all, so the identity is short one of its two operands at every
  origin. An identity missing an operand is not a derivation, and filling it would
  corrupt the very error a later rebuild is scored on.

  THE SHARE COUNT IS NOT RECORDED AT ANY ORIGIN, and the paid-in capital IS. Those
  are two different rows on purpose. This run read the FACE of the balance sheet,
  where issued capital is printed in pounds; the par value and the count the same
  document states live in the capital NOTE, which was never parsed. Clause (ii) is
  unconditional — issued capital divided by par must reproduce the stated count, or
  the count is not recorded — and no par value may be supplied from anywhere else.
  The capital sits unchanged at EGP 4,529,338,000 across all five origins, which
  says there was no capital increase on the face of the statements in this window
  and still does not say how many shares there are.

WHAT IT FOOTS BEFORE IT WRITES, and it refuses rather than emits on a break:

  * interest-bearing debt reproduces, to the pound, from its own named component
    lines, against the base this run had already committed for its financing rule;
  * PPE plus deferred tax reproduces the printed total non-current assets exactly at
    FY2017-FY2020; at FY2016 it does not, a residual of EGP 143,345,677 sits in a
    line the extraction did not capture, and that is RECORDED rather than smoothed;
  * the balance-sheet identity current liabilities = total assets less equity less
    non-current liabilities reproduces the PRINTED current liabilities exactly at
    FY2017, FY2018 and FY2019, which is what licenses its use at FY2020, where the
    extraction captured no current-liabilities subtotal. That one figure is LABELLED
    derived, on the same footing the amendment gives derived capex: an identity is
    not an assumption and the label is what keeps the two apart.

POINT-IN-TIME. Every figure is that year's OWN column in that year's OWN filing —
no comparative column is used anywhere here, and no later filing is substituted.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

RULE = "[R-FCAL-01 AMENDED] (03-09-2026)"

# The origins this run's own pre-registration declares (section 1): first
# admissible FY2016, last scored FY2024, FY2025 struck but unresolved. The five
# beyond FY2020 are the blocked ones and they are written out as missing rather
# than left off the record — a block quietly carrying five of ten reads as a
# shorter run rather than a stopped one.
ORIGINS = list(range(2016, 2026))
HELD = list(range(2016, 2021))

BLOCK = (
    "no statements exist for this origin in this run. The company's own "
    "investor-relations register publishes financial statements from FY2012 to "
    "H1-2021 and stops; everything FY2021 onward is absent from it, the exchange "
    "answers automated requests with an anti-bot interstitial, and the company's "
    "own embedded investor-relations backend serves on a port this environment's "
    "egress does not carry. Aggregator figures for these years were available and "
    "were deliberately not used, because a data vendor may not be the source of a "
    "company's own reported historicals (SIGCM clause 1). The run is BLOCKED at "
    "[R-FCAL-01] section 1 and the documents are requested; every route attempted "
    "and its outcome is logged in SOURCE_REGISTER_01-09-2026.md and in "
    "fetch_attempts.json. This is not a reading that failed — it is a document "
    "that was never obtained, and the two are different facts."
)

NO_CASHFLOW_HEAD = (
    "this run extracted the profit-or-loss page and the statement of financial "
    "position and NOT the cash-flow statement — panel.json says so in its own "
    "words, 'profit or loss only; the balance sheet and cash flow are extracted "
    "when the blocked years arrive and the whole panel is built in one pass on one "
    "definition of each line'. "
)

NO_CASHFLOW_TAIL = (
    " The source documents themselves are held outside the repository by design — "
    "fetch_sources.py writes about 92 MB of PDFs to a scratch directory and commits "
    "only the register, the sha256 hashes and the extracted numbers — so this item "
    "cannot be copied out of anything committed here. It is one document-fetch "
    "away and it is not a guess away."
)


def no_cashflow(survey):
    """The cash-flow reason for ONE filing, from that filing's own survey row.

    Written per origin rather than once, because the two failures are different
    facts: a file with no text layer anywhere and a file whose text layer covers
    every statement EXCEPT this one are not the same obstacle, and a reader who
    cannot tell them apart cannot tell which is cheap to fix.
    """
    row = ((survey.get("statements") or {}).get("cash_flows") or {})
    return (NO_CASHFLOW_HEAD
            + "The extraction survey went further and could not LOCATE a cash-flow "
              "statement page in this filing at all: against %d pages it records "
              "route '%s', page %s, '%s'."
              % (survey.get("pages") or 0, row.get("route"),
                 row.get("page") if row.get("page") is not None else "not found",
                 row.get("note") or "no note")
            + NO_CASHFLOW_TAIL)


def dep_why(survey, pl_lines):
    """`pl_lines` is that year's OWN profit-or-loss line count, counted from the
    panel rather than typed — the count differs by year in this panel (15 at
    FY2012, 13 from FY2015) and a typed one would be right by luck."""
    return (
        "no depreciation or amortisation charge is committed anywhere in this run. "
        "The profit-or-loss panel carries %d lines at this origin and none of them "
        "is D&A — " % pl_lines +
        "on this company's face presentation the charge sits inside cost of "
        "revenue and general and administrative expenses — and the fixed-asset "
        "movement note, which is where the charge is disclosed, was never parsed. "
        + no_cashflow(survey))


SHARES_WHY = (
    "NOT FOOTED, THEREFORE NOT RECORDED, per clause (ii). This run read the FACE of "
    "the statement of financial position, where issued and paid-up capital is "
    "printed in pounds; it did not parse the capital note, which is the only place "
    "carrying the par value and the share count the same document states. Issued "
    "capital divided by par must reproduce that stated count before a count may be "
    "written down, and neither operand of that check is held. The paid-in capital "
    "IS committed, as its own item, because capital in pounds is not a share count "
    "and crediting this cell with one it does not have is the fabrication this "
    "record exists to refuse. TODAY'S COUNT IS NOT CARRIED BACK and neither is any "
    "neighbour's: a carried count is fabricated in vintage, plausible on the page "
    "and invisible in the pooled error afterwards."
)


def _load(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return json.load(fh)


def _survey_row(docs, filename):
    for d in docs:
        if d.get("file") == filename:
            return d
    return {}


def _route(prov, survey):
    """Clause (iii): the route, the page and the file, on the same footing as the
    four-field rule. Recorded as this run itself recorded it — text layer or OCR,
    with the resolution the reading survived at — never re-described."""
    return {
        "route": prov.get("route"),
        "page_index": prov.get("page_index"),
        "page_rotation": prov.get("page_rotation"),
        "ocr_dpi": prov.get("ocr_dpi"),
        "file": prov.get("source_document"),
        "url": prov.get("source_url"),
        "file_sha256": survey.get("sha256"),
        "file_pages": survey.get("pages"),
        "file_has_text_layer": survey.get("file_has_text_layer"),
        "column": prov.get("column"),
        "tier": prov.get("tier"),
        "arbiter": ("arithmetic, not the extractor's confidence — this year's "
                    "statement was accepted only where its own subtotals "
                    "re-derive, and the identities that were tested are recorded "
                    "in balance_sheet.json's identity_checks"),
    }


DEBT_COMPONENTS = ("credit_facilities_cl", "credit_facilities_ncl",
                   "borrowings_related", "current_portion_ltl",
                   "long_term_liabilities")
PPE_COMPONENTS = ("fixed_assets", "fixed_assets_under_constr",
                  "investment_properties")
TRADE_LINES = ("accounts_notes_receivable", "development_properties",
               "prepayments_other_recv", "due_from_related",
               "advances_from_customers", "trade_payables", "retentions_payable",
               "due_to_related", "income_tax_payable", "provisions_liab_cl")


def build():
    bs = _load("balance_sheet.json")
    panel = _load("panel.json")
    docs = _load("extraction_survey.json")["documents"]
    years, bases = bs["years"], bs["driver_bases"]

    origins, checks = {}, []
    for y in ORIGINS:
        key = "FY%d" % y
        if y not in HELD:
            origins[key] = {
                item: {"missing": True, "reason": BLOCK}
                for item in ("cash", "debt", "capex", "ppe", "dep", "wc",
                             "shares", "cap")
            }
            origins[key]["_origin"] = (
                "declared by PRE_REGISTRATION_01-09-2026.md section 1; blocked at "
                "[R-FCAL-01] section 1, no statement obtained")
            continue

        sy = str(y)
        lines = years[sy]["lines"]
        prov = years[sy]["provenance"]
        survey = _survey_row(docs, prov.get("source_document"))
        route = _route(prov, survey)
        asat = "%d-12-31" % y
        src = "%s, statement of financial position, own column" % route["file"]

        # ---- debt: footed against the base this run already committed -------
        comp = {k: lines[k] for k in DEBT_COMPONENTS if k in lines}
        debt = sum(comp.values())
        base = bases[sy]["interest_bearing_borrowings"]
        assert abs(debt - base["value"]) < 0.5, (y, debt, base["value"])
        checks.append({"origin": key, "check": "interest-bearing debt",
                       "derived": debt, "against": base["value"], "foots": True})

        # ---- ppe: tested against the printed non-current subtotal -----------
        ppe_lines = {k: lines[k] for k in PPE_COMPONENTS if k in lines}
        ppe = sum(ppe_lines.values())
        dta = lines.get("deferred_tax_assets", 0.0)
        tnca = lines.get("total_non_current_assets")
        residual = None if tnca is None else tnca - ppe - dta
        checks.append({"origin": key,
                       "check": "PPE + deferred tax vs printed total non-current assets",
                       "derived": ppe + dta, "against": tnca,
                       "foots": residual is not None and abs(residual) < 0.5,
                       "residual": residual})

        # ---- current liabilities: printed, or by the identity, labelled -----
        cl = lines.get("total_current_liabilities")
        ncl = lines.get("total_non_current_liab")
        ta, te = lines["total_assets"], lines["total_equity"]
        cl_derived = None if ncl is None else ta - te - ncl
        if cl is not None and cl_derived is not None:
            checks.append({"origin": key,
                           "check": "current liabilities = total assets - equity"
                                    " - non-current liabilities",
                           "derived": cl_derived, "against": cl,
                           "foots": abs(cl_derived - cl) < 0.5})
        cl_is_derived = cl is None
        if cl_is_derived:
            assert cl_derived is not None, y
            cl = cl_derived

        tca = lines["total_current_assets"]
        wc = tca - cl

        origins[key] = {
            "_origin": ("declared by PRE_REGISTRATION_01-09-2026.md section 1; "
                        "statements held, this run parsed the profit-or-loss page "
                        "and the statement of financial position"),
            "cash": {
                "value": lines["cash"], "as_at": asat, "unit": "EGP",
                "precision": "exact — whole pounds as printed",
                "source": src + ", cash and cash equivalents",
                "route": route,
                "definition": ("the balance sheet's own cash and cash equivalents "
                               "line, exactly as printed"),
                "excluded_and_named": {
                    "investments": lines.get("investments"),
                    "why": ("the statement presents investments as a separate line "
                            "from cash and this record makes no valuation choice "
                            "about whether they are equivalents, so the figure is "
                            "NAMED here rather than folded in or dropped. This "
                            "run's own financing rule treats them as part of the "
                            "interest-EARNING asset base, which is a different "
                            "question from whether they are cash"),
                },
            },
            "debt": {
                "value": debt, "as_at": asat, "unit": "EGP",
                "precision": "exact — whole pounds as printed",
                "source": src + ", the borrowing lines named below",
                "route": route,
                "definition": base["DERIVED"],
                "why": base["why"],
                "lines": comp,
                "check": ("reproduces to the pound the interest-bearing borrowings "
                          "base this run had already committed for its financing "
                          "rule: %.0f" % base["value"]),
                "excluded_and_named": {
                    "advances_from_customers": lines.get("advances_from_customers"),
                    "trade_payables": lines.get("trade_payables"),
                    "retentions_payable": lines.get("retentions_payable"),
                    "eosb_provision": lines.get("eosb_provision"),
                    "why": ("none of these bears interest. Excluding them is the "
                            "whole point of the rule: dividing a finance charge by "
                            "a broader liabilities total understates the rate by a "
                            "multiple and manufactures a bias that looks exactly "
                            "like evidence. They are named so a reader can tell an "
                            "excluded line from an unread one"),
                },
            },
            "capex": {
                "missing": True,
                "reason": (
                    no_cashflow(survey)
                    + " THE IDENTITY CANNOT SUPPLY IT EITHER: capex = change in PPE "
                      "+ D&A needs both of its operands, and the D&A term is missing "
                      "at every origin of this run for the reason recorded under "
                      "that item. "
                    + ("The change in PPE IS available here — this origin's PPE and "
                       "the prior origin's are both committed — so this cell is one "
                       "disclosed depreciation charge away from a derivation."
                       if y > HELD[0] else
                       "The change in PPE is not available here either: FY2016 is "
                       "the first year of this run's balance-sheet panel, no FY2015 "
                       "balance sheet is held, and the identity has no opening term "
                       "at this origin. This cell is two figures away, not one.")
                    + " An identity short an operand is not a derivation, and "
                      "filling it would corrupt the very error a later rebuild is "
                      "scored on."),
            },
            "ppe": {
                "value": ppe, "as_at": asat, "unit": "EGP",
                "precision": "exact — whole pounds as printed",
                "source": src + ", the non-current asset lines named below",
                "route": route,
                "definition": ("fixed assets, fixed assets under construction and "
                               "investment properties — the long-lived asset base. "
                               "Development properties are NOT in it and are named "
                               "beside: for an off-plan developer they are "
                               "inventory carried at cost and consumed through "
                               "cost of revenue, not a depreciating asset, and "
                               "folding them in would put the largest number on "
                               "the balance sheet into a capex identity it has no "
                               "business in"),
                "lines": ppe_lines,
                "carried_beside_not_folded_in": {
                    "development_properties": lines.get("development_properties"),
                    "why": ("inventory for this class of company, and by an order "
                            "of magnitude the largest asset here; a rebuild that "
                            "wants operating assets and one that wants the "
                            "development pipeline need different answers, so the "
                            "figure is named and the choice is left open"),
                },
                "check": (("PPE %.0f plus deferred tax assets %.0f reproduces the "
                           "printed total non-current assets of %.0f exactly"
                           % (ppe, dta, tnca)) if residual is not None
                          and abs(residual) < 0.5 else
                          ("PPE %.0f plus deferred tax assets %.0f leaves a "
                           "residual of %.0f against the printed total non-current "
                           "assets of %.0f. The residual sits in a non-current line "
                           "this run's extraction did not capture; it is RECORDED "
                           "rather than smoothed, and no figure here is adjusted to "
                           "close it" % (ppe, dta, residual, tnca))),
            },
            "dep": {"missing": True,
                    "reason": dep_why(survey,
                                      len(panel["years"][sy]["lines"]))},
            "wc": {
                "value": wc, "as_at": asat, "unit": "EGP",
                "precision": "exact — whole pounds as printed"
                             if not cl_is_derived else
                             "exact on the printed operands; the current-liability "
                             "operand is derived by the balance-sheet identity",
                "source": src + ", the current sections",
                "route": route,
                "definition": ("total current assets less total current "
                               "liabilities, the statement's own current "
                               "subtotals. This company prints no working-capital "
                               "line of its own"),
                "derived": cl_is_derived,
                "derivation": (
                    ("total current liabilities are not captured on this year's "
                     "parse, and are derived by the balance-sheet identity: total "
                     "assets %.0f less total equity %.0f less total non-current "
                     "liabilities %.0f = %.0f. LABELLED DERIVED. The identity "
                     "reproduces the PRINTED current liabilities to the pound at "
                     "FY2017, FY2018 and FY2019, which is what licenses it here; "
                     "an identity is not an assumption and the label is what keeps "
                     "the two apart" % (ta, te, ncl, cl)) if cl_is_derived else None),
                "lines": {
                    "total_current_assets": tca,
                    "total_current_liabilities": cl,
                    **{k: lines[k] for k in TRADE_LINES if k in lines},
                },
                "also_inside_this_figure_and_committed_separately": {
                    "cash": lines["cash"],
                    "investments": lines.get("investments"),
                    "current_borrowings": {k: comp[k] for k in
                                           ("credit_facilities_cl",
                                            "current_portion_ltl") if k in comp},
                    "why": ("this is the GROSS difference of the two printed "
                            "subtotals, so cash, investments and the current "
                            "borrowing lines sit inside it AND are committed as "
                            "their own items above. A rebuild netting them a "
                            "second time would double-count, and the trading lines "
                            "are listed above so any narrower definition can be "
                            "built from the page rather than assumed"),
                },
            },
            "shares": {"missing": True, "reason": SHARES_WHY},
            "cap": {
                "value": lines["share_capital"], "as_at": asat, "unit": "EGP",
                "precision": "exact — whole pounds as printed",
                "source": src + ", issued and paid-up capital",
                "route": route,
                "definition": ("issued and paid-up capital in pounds, off the face "
                               "of the statement of financial position"),
                "not_a_share_count": ("this is capital in currency and it becomes a "
                                      "count only when divided by the par value in "
                                      "the capital note, which this run has not "
                                      "parsed. See the shares item above"),
                "vintage": ("this year's own column in this year's own filing. The "
                            "figure is unchanged across all five held origins, "
                            "which says the face of the statements shows no capital "
                            "increase in this window and still says nothing about "
                            "the number of shares"),
            },
        }

    for c in checks:
        assert c["foots"] or c["check"].startswith("PPE"), c

    return {
        "_": __doc__.strip(),
        "run": "EMFD",
        "rule": RULE,
        "company": "Emaar Misr for Development Company (S.A.E.)",
        "ticker": "EMFD",
        "market": "EG",
        "exchange": "EGX",
        "currency": "EGP",
        "units": "as printed in the filings — whole pounds, not thousands",
        "basis": "consolidated from FY2018; the FY2016 and FY2017 year-end filings "
                 "are the editions this run obtained and are recorded as they were "
                 "published",
        "fiscal_year_end": "31 December",
        "run_status": ("BLOCKED at [R-FCAL-01] section 1 — no projection has been "
                       "run, no error computed, no lesson written and no delivered "
                       "number moved. This block is the amendment binding forward "
                       "on the statements the run HAS already parsed"),
        "origins_declared_by": "PRE_REGISTRATION_01-09-2026.md, section 1",
        "origins_held": ["FY%d" % y for y in HELD],
        "origins_blocked": ["FY%d" % y for y in ORIGINS if y not in HELD],
        "point_in_time": ("every figure is that year's OWN column in that year's "
                          "OWN filing. No comparative column is used anywhere in "
                          "this block and no later filing is substituted for an "
                          "earlier one. Two restatements inside the wider window "
                          "are measured in restatements.json and BASIS_BREAKS_"
                          "01-09-2026.md and neither is adopted here"),
        "source_documents": {
            "FY%d" % y: {
                "file": years[str(y)]["provenance"]["source_document"],
                "url": years[str(y)]["provenance"]["source_url"],
                "sha256": _survey_row(
                    docs, years[str(y)]["provenance"]["source_document"]
                ).get("sha256"),
                "tier": years[str(y)]["provenance"]["tier"],
            } for y in HELD
        },
        "arithmetic_checks": checks,
        "origins": origins,
    }


if __name__ == "__main__":
    doc = build()
    out = os.path.join(HERE, "valuation_inputs.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    held = doc["origins_held"]
    print("wrote %s" % out)
    print("  origins: %d held, %d blocked"
          % (len(held), len(doc["origins_blocked"])))
    for c in doc["arithmetic_checks"]:
        print("  %-8s %-58s %s" % (c["origin"], c["check"],
                                   "foots" if c["foots"] else
                                   "residual %.0f" % (c.get("residual") or 0)))
