"""Assemble engine/macro_history/EG.json from the two extraction records.

WHY THIS IS A SCRIPT AND NOT A HAND-EDITED FILE. Every figure in the archive was
read off a document, and the reading is recorded in `_extract_damodaran_egypt.json`
and `_extract_weo_egypt.json`, each carrying the sha256 of the file it was read
from. This script does the clerical half — mapping a vintage to the origin it
serves, attaching the four fields, and writing the refusals — so that the clerical
half cannot drift from the reading, and so a later session can see exactly which
document every number came from without trusting a note.

THE VINTAGE-TO-ORIGIN CONVENTION IS DECLARED HERE RATHER THAN ASSUMED, because it
is the one judgement in the whole file and getting it wrong is invisible.

  A study struck AT year-end YYYY is written in the weeks after it, and it uses the
  annual country-risk vintage computed on data THROUGH 31-Dec-YYYY — published
  within days of the origin. That is what this house does today and it is what the
  archive does at every past origin. The alternative strict reading (an origin may
  use only what was on the web at 23:59 on 31 December) would push every origin
  onto a vintage describing the PREVIOUS year, which is not what any analyst does
  and not what our own delivered studies did.

  The exception is recorded rather than smoothed: the 2015 vintage held in the
  archive carries "Updated July 1, 2016" — a MID-YEAR RE-PUBLICATION, six months
  after its origin, and the January-2016 original is not held. That file may embed
  first-half-2016 information, which an analyst at 31-Dec-2015 did not have, so the
  2015 origin is marked point_in_time_compromised and the calibration can exclude
  it or sensitivity-test it. It is not quietly used as though it were clean.

The inflation vintages are the IMF World Economic Outlook editions PUBLISHED BEFORE
each origin — October of the origin year where it is held, April of the same year
otherwise (also point-in-time valid, merely staler, and labelled). What they carry
is not only the origin year's inflation as then estimated but the FORWARD PATH an
analyst standing there actually had, which is what [R-MACRO-01] needs at a
historical origin and which today's series cannot supply at any price.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DAM = json.load(open(os.path.join(HERE, "_extract_damodaran_egypt.json"), encoding="utf-8"))
WEO = json.load(open(os.path.join(HERE, "_extract_weo_egypt.json"), encoding="utf-8"))
SUP = json.load(open(os.path.join(HERE, "_supplied_EG_rates.json"), encoding="utf-8"))

ORIGINS = list(range(2013, 2024))

# origin -> the WEO edition that existed at its year-end. October of the origin
# year wherever it is held; April of the same year otherwise, which is still
# published before the origin and is labelled as the staler read it is.
WEO_FOR_ORIGIN = {
    2013: "October 2013",
    2014: "October 2014",
    2015: "October 2015",
    2016: "October 2016",
    2017: "April 2017",
    2018: "October 2018",
    2019: "October 2019",
    # April of the origin year, under the convention stated above, and labelled as
    # the staler read it is. October 2020 is not published at the media blob path
    # that serves every other edition; April 2020 is, it existed well before this
    # origin's year-end, and 2017 is the standing precedent for the fallback.
    2020: "April 2020",
    2021: "October 2021",
    2022: "October 2022",
    2023: "October 2023",
}

# WHY FIVE EDITIONS ARRIVED LATE, AND IT WAS NOT THAT THEY COULD NOT BE OBTAINED.
# This archive recorded on 03-Sep-2026 that the October 2014 and 2020-2023 editions
# "could not be retrieved from here — the October 2014 file returns an interstitial
# page and the 2020-2023 editions sit behind a path this environment cannot
# resolve." Both halves were true of the routes tried and false of the source: the
# /en/Publications/ section does return 403 here and the /external/ path does serve
# a JavaScript redirect, but the media blob path serves every edition, under a
# pattern with NO month folder — .../WEO-Database/{year}/WEOOct{year}all.xls.
# Found by re-running the probe through a headless browser's request context, which
# is the tool this environment provides for exactly that.
#
# AN OBSTACLE IS WORK, NOT NEWS, and a written outcome is a fact about the past
# [R-IND-01]: five origins sat unusable for a day behind a recorded failure that
# one more probe would have cleared. A probe that came back empty is first evidence
# the probe did not run.

# The "Updated" line each Damodaran vintage carries, turned into a publication
# date. Read off the file itself, never inferred from the filename.
PUBLISHED = {
    2013: "2014-01-01", 2014: "2015-01-01", 2015: "2016-07-01", 2016: "2017-01-05",
    2017: "2018-01-01", 2018: "2019-01-01", 2019: "2020-01-01", 2020: "2021-01-01",
    2021: "2022-01-01", 2022: "2023-01-01", 2023: "2024-01-01",
}

ORDINARY_LAG = (
    "Published %s, computed on data through this origin's own year-end. A study "
    "struck at %d is written in the weeks after it and uses this vintage; that is "
    "the convention declared in build_eg.py and it is what this house does today.")

COMPROMISED_2015 = (
    "Published 2016-07-01 — a MID-YEAR RE-PUBLICATION of the 2015 vintage, six "
    "months after this origin, and the January-2016 original is not held. It may "
    "embed first-half-2016 information that an analyst at 31-Dec-2015 did not "
    "have. The origin is marked point_in_time_compromised so the calibration can "
    "exclude it or sensitivity-test it rather than use it as though it were clean.")

DAM_SRC = (
    "Damodaran, NYU Stern, 'Risk Premiums for Other Markets', archived vintage %s "
    "(%s), sheet 'ERPs by country', Egypt row. Downloaded 03-Sep-2026 from "
    "pages.stern.nyu.edu/~adamodar/pc/archives/. THE VINTAGE IS THE POINT: this is "
    "the premium computed on the data available at the origin, not today's reading "
    "of that year.%s")

WEO_SRC = (
    "IMF World Economic Outlook database, %s edition, Egypt, series %s (%s). "
    "Downloaded 03-Sep-2026 from imf.org; sha256 %s. THE VINTAGE IS THE POINT: "
    "this is the inflation an analyst standing at the origin actually had, "
    "estimates and projections included. The figure for the origin year is itself "
    "an %s in this edition, which is correct — nobody at 31-Dec-%d had the final "
    "print either.")


def figure(value, source, date, tier, revision_class, vintage=None,
           published=None, lag_note=None, **extra):
    rec = {"value": value, "source": source, "date": date, "tier": tier,
           "revision_class": revision_class}
    if vintage:
        rec["vintage"] = vintage
    if published:
        rec["published"] = published
    if lag_note:
        rec["publication_lag_note"] = lag_note
    rec.update(extra)
    return rec


def build():
    origins = []
    for y in ORIGINS:
        d = DAM[str(y)]
        figs = {}
        pub = PUBLISHED[y]
        compromised = (y == 2015)
        lag = COMPROMISED_2015 if compromised else (ORDINARY_LAG % (pub, y))
        vint = "%s (%s)" % (d["file"], d["stamp_updated_text"])

        # ---- equity risk premium, both bases; CDS central per [R-COC-01] -----
        has_cds = d.get("erp_cds") is not None
        basis = "cds" if has_cds else "rating"
        erp = d["erp_cds"] if has_cds else d["erp_rating"]
        spread = d["cds_spread_net_of_us"] if has_cds else d["default_spread_rating"]
        note = "" if has_cds else (
            " RATING BASIS: this vintage publishes no credit-default-swap figure "
            "for Egypt, so the central basis at this origin is the rating one and "
            "is labelled as such rather than silently substituted.")
        figs["erp"] = figure(
            round(float(erp), 6), DAM_SRC % (d["file"], d["stamp_updated_text"], note),
            "%d-12-31" % y, "Global", "estimated", vintage=vint, published=pub,
            lag_note=lag, basis=basis,
            erp_rating_basis=round(float(d["erp_rating"]), 6),
            erp_cds_basis=(round(float(d["erp_cds"]), 6) if has_cds else None),
            moody_rating_at_vintage=d["moody_rating"],
            stamp_date_of_update_cell=d.get("stamp_date_of_update_cell"))
        figs["default_spread"] = figure(
            round(float(spread), 6),
            DAM_SRC % (d["file"], d["stamp_updated_text"],
                       " %s-basis default spread." % basis.upper()),
            "%d-12-31" % y, "Global", "estimated", vintage=vint, published=pub,
            lag_note=lag, basis=basis,
            default_spread_rating_basis=round(float(d["default_spread_rating"]), 6),
            default_spread_cds_basis=(round(float(d["cds_spread_net_of_us"]), 6)
                                      if has_cds else None))

        # ---- inflation, from the WEO edition that existed at the origin ------
        ed = WEO_FOR_ORIGIN.get(y)
        if ed:
            w = WEO[ed]
            s = w["series"]["PCPIPCH"]["values"]
            est_after = int(w["estimates_start_after"])
            kind = "actual" if y <= est_after else ("estimate" if y == est_after + 1
                                                    else "projection")
            # what the vintage still calls an actual, and the forward path it gave
            last_actual = max((int(k) for k in s if int(k) <= est_after), default=None)
            fwd = {str(h): float(s[str(h)]) for h in range(y + 1, y + 6) if str(h) in s}
            eop = w["series"].get("PCPIEPCH", {}).get("values", {})
            figs["cpi_annual"] = figure(
                round(float(s[str(y)]) / 100.0, 6),
                WEO_SRC % (ed, "PCPIPCH", "CPI inflation, period average, % change",
                           w["sha256"][:16], kind, y),
                "%d-12-31" % y, "Global", "estimated",
                vintage="IMF WEO %s (sha256 %s)" % (ed, w["sha256"][:16]),
                actual_or_estimate=kind,
                edition_note=("The October edition of the origin year is not held; "
                              "the April edition of the same year is used, which is "
                              "also published before the origin and is merely "
                              "staler." if ed.startswith("April") else None),
                last_actual_year=last_actual,
                last_actual_value=(round(float(s[str(last_actual)]) / 100.0, 6)
                                   if last_actual is not None else None),
                forward_path={k: round(v / 100.0, 6) for k, v in fwd.items()},
                end_of_period_same_vintage=(round(float(eop[str(y)]) / 100.0, 6)
                                            if str(y) in eop else None))
        # ---- policy rate: supplied as a lead, recorded as verified ----------
        pr = (SUP["policy_rate"]["origins"] or {}).get(str(y))
        if pr:
            figs["policy_rate"] = figure(
                float(pr["value"]),
                "%s  [Supplied by the principal 03-Sep-2026 as a lead and CHECKED "
                "against the decision record before recording; the value here is "
                "the verified one.%s]"
                % (pr["source"],
                   "  THE SUPPLIED VALUE WAS WRONG and is corrected: " +
                   pr["why_the_supplied_value_is_wrong"]
                   if pr.get("supplied_was_wrong") else ""),
                "%d-12-31" % y, "Country", "observed",
                verified=pr["verified"],
                supplied_value=pr.get("supplied"),
                corroborated=True,
                instrument=SUP["policy_rate"]["instrument"])

        # ---- the ten-year yield: recorded, and its weakness recorded with it --
        yv = (SUP["sovereign_10y"]["origins"] or {}).get(str(y))
        if yv is not None:
            figs["sovereign_10y"] = figure(
                float(yv),
                "Supplied by the principal 03-Sep-2026, from an AI-generated "
                "summary table with no per-figure publisher. UNCORROBORATED: no "
                "second source for an Egyptian ten-year yield is reachable from "
                "here, and the policy-rate column of the SAME table was wrong on "
                "one origin in eleven in a way that looked entirely plausible. "
                "Recorded because the principal instructed it; flagged because "
                "recording it as equal evidence to a checked figure would hide "
                "the one weakness this archive exists to make visible.",
                "%d-12-31" % y, "Market", "observed",
                corroborated=False,
                corroboration_note=(
                    "the market series the principal pointed to "
                    "(worldgovernmentbonds.com) begins 11-Sep-2016, so this "
                    "origin predates any series that could check it"
                    if y <= 2015 else
                    "a market series covering this origin exists but could not be "
                    "read from here — the page renders client-side and the host "
                    "resets a headless browser through this proxy"),
                instrument=SUP["sovereign_10y"]["instrument"])

        origins.append({
            "year": y,
            "point_in_time_compromised": compromised or None,
            "uncorroborated_figures": sorted(
                k for k, v in figs.items() if v.get("corroborated") is False) or None,
            "figures": figs,
        })
    return origins


# The World Bank series already read into the archive, kept as a LABELLED
# cross-check on each vintage print rather than deleted. It is the current
# reporting of those years and it is not a substitute for the vintage: the
# comparison is the point, and it is one of the few direct measurements this
# project has of how far a revised series drifts from what the origin saw.
def carry_current_vintage_cpi(prev_path):
    if not os.path.exists(prev_path):
        return {}
    prev = json.load(open(prev_path, encoding="utf-8"))
    out = {}
    for o in prev.get("origins", []):
        rec = (o.get("figures") or {}).get("cpi_annual_current_vintage")
        if rec:
            out[int(o["year"])] = rec
    return out


UNSOURCED = {
    "fields": [],
    "resolved_03_09_2026": (
        "policy_rate and sovereign_10y, both supplied by the principal on "
        "03-Sep-2026 — see _supplied_EG_rates.json for what was supplied, what "
        "was verified against the CBE decision record, and the one supplied "
        "figure that was WRONG and is corrected here. The policy rate is "
        "corroborated origin by origin; the ten-year yield is NOT, and every "
        "origin says so."),
    "resolved_04_09_2026": (
        "cpi_annual for 2014 and 2020-2023, the last five origins, sourced from "
        "the IMF World Economic Outlook edition that existed at each — October "
        "2014, April 2020, October 2021, October 2022 and October 2023 — each "
        "recorded with its own sha256, its URL and the route it came by. All "
        "eleven declared origins are now usable, up from six.\n\n"
        "THIS WAS NOT NEW DATA BECOMING AVAILABLE. This record said on 03-Sep "
        "that those editions 'could not be retrieved from here — the October "
        "2014 file returns an interstitial page and the 2020-2023 editions sit "
        "behind a path this environment cannot resolve.' Both halves were true "
        "of the routes tried and FALSE OF THE SOURCE: /en/Publications/ does "
        "return 403 here and /external/ does serve a JavaScript redirect, but "
        "the media blob path serves every edition, under a pattern with NO "
        "month folder. One more probe, through the headless browser this "
        "environment provides, cleared five origins. AN OBSTACLE IS WORK, NOT "
        "NEWS [R-IND-01], and a written outcome is a fact about the past: five "
        "origins sat unusable for a day behind a recorded failure."),
    "what_the_re_source_also_verified": (
        "All six editions already in this archive were re-downloaded by the same "
        "route and every sha256 MATCHED, which independently confirms both the "
        "archive's provenance and the new route. It also settled a live question "
        "rather than assuming it: 'Estimates Start After' is a property of the "
        "SERIES and not of the edition — October 2014 marks GDP from 2013 and "
        "CPI from 2014, October 2022 marks GDP from 2021 and CPI from 2022 — and "
        "this archive keeps one value per edition. Checked against the files, all "
        "six carry the CPI series' own flag, so the existing record is right; the "
        "new entries store the per-series flags too, and name any series that "
        "disagrees rather than losing it."),
    "what_remains": (
        "Nothing on cpi_annual. The uncorroborated ten-year yield stands as "
        "recorded: usable, single-sourced, and said so at every origin."),
    "what_would_close_it": (
        "A second independent source for the sovereign ten-year yield at each "
        "origin, which would corroborate the one field this archive still carries "
        "on a single source."),
}


def main():
    path = os.path.join(HERE, "EG.json")
    prev_cpi = carry_current_vintage_cpi(path)
    origins = build()
    for o in origins:
        rec = prev_cpi.get(o["year"])
        if rec:
            rec.setdefault("revision_class", "estimated")
            rec.setdefault("vintage", "World Bank WDI as retrieved 03-Sep-2026 — "
                                      "THE CURRENT REPORTING, not the origin's")
            o["figures"]["cpi_annual_current_vintage"] = rec
        o["figures"] = {k: v for k, v in o["figures"].items()}
        if o.get("point_in_time_compromised") is None:
            o.pop("point_in_time_compromised", None)

    # ---- what the archive itself measures, computed here and never typed -----
    # This is the direct evidence for why an estimated figure needs its vintage.
    # It is generated from the two extraction records at every rebuild, so it
    # cannot drift from them, and it is stated in pp because that is the unit the
    # error enters a discounted cash flow in.
    drifts, paths = {}, {}
    for o in origins:
        f = o["figures"]
        if "cpi_annual" not in f:
            continue
        pit = f["cpi_annual"]["value"]
        paths[str(o["year"])] = f["cpi_annual"].get("forward_path") or {}
        cur = f.get("cpi_annual_current_vintage")
        if cur:
            drifts[str(o["year"])] = round((float(cur["value"]) / 100.0 - pit) * 100, 2)
    measured = {}
    if drifts:
        mags = [abs(v) for v in drifts.values()]
        measured = {
            "cpi_vintage_drift_pp": drifts,
            "mean_abs_drift_pp": round(sum(mags) / len(mags), 2),
            "max_abs_drift_pp": round(max(mags), 2),
            "n_origins": len(drifts),
            "what_it_shows": (
                "The gap, in percentage points, between the inflation figure "
                "PUBLISHED at each origin and the figure today's series reports "
                "for the same year. It runs in BOTH directions and it is large: a "
                "rebuild that quietly used the modern series would be feeding a "
                "discounted cash flow an inflation rate several points away from "
                "the one the origin actually had, in escalators, in the currency "
                "path derived from them and in the terminal. This is the whole "
                "argument for the estimated/observed split, measured rather than "
                "asserted, on this archive's own numbers."),
            "forward_paths_at_each_origin": paths,
            "what_the_forward_paths_show": (
                "Every vintage's own five-year path converges toward roughly 7 "
                "per cent, from wherever it starts — 12.3% by 2018 seen from "
                "2013, 7.0% by 2020 seen from 2015, 7.1% by 2021 seen from 2016. "
                "The house macro path [R-MACRO-01] is built the same way, from "
                "the same class of institutional forecast, and these are the only "
                "out-of-sample readings this project holds of how such a path "
                "actually performed. NOTHING IS CONCLUDED FROM SIX ORIGINS HERE: "
                "the paths are recorded so the calibration can score them, and a "
                "finding is a finding only once it has been scored."),
        }

    blob = {
        "_": ("POINT-IN-TIME macro vintages for Egypt: what was KNOWN at each "
              "year-end, for the valuation calibration [R-VCAL-01] to rebuild a "
              "fair value at that origin. NOT the forward path in "
              "engine/macro_paths/EG.json, which is what the house believes "
              "today. A rebuild that reaches for today's numbers is not a "
              "rebuild; it is the answer wearing a date."),
        "GENERATED": ("by engine/macro_history/build_eg.py from "
                      "_extract_damodaran_egypt.json and _extract_weo_egypt.json, "
                      "each carrying the sha256 of the file it was read from. "
                      "NEVER hand-edit this file: a record that states where every "
                      "number came from must not be the thing that remembers it."),
        "market": "EG",
        "currency": "EGP",
        "target_span": "2013-2023 year-ends, the span the pre-registration of 03-Sep-2026 fixes",
        "rule": ("A VINTAGE IS SOURCED OR IT DOES NOT EXIST. Four fields on every "
                 "figure plus its revision class. No interpolation between years, "
                 "no carrying a neighbouring year forward, no 'approximately'. An "
                 "origin whose required figures are not all sourced is DROPPED by "
                 "the calibration and its window shortened, which the "
                 "pre-registration fixes in advance precisely so that a thin "
                 "archive shows up as fewer origins rather than as a fuller-"
                 "looking record built on filled-in cells."),
        "revision_class": ("OBSERVED figures (a market close, an administered "
                           "rate) are fixed at their date and need no vintage; "
                           "ESTIMATED figures (a price index, a computed premium) "
                           "are revised and rebased for years afterwards and are "
                           "REFUSED without one. Egypt's 2013 inflation as "
                           "reported today is not the figure anyone had in 2013, "
                           "and a figure filed in the wrong class is right in "
                           "value, wrong in date, and invisible afterwards."),
        "vintage_to_origin_convention": (
            "Origin YYYY uses the annual country-risk vintage computed on data "
            "THROUGH 31-Dec-YYYY and published within days of it, because that is "
            "what a study struck at that origin actually uses and what this house "
            "does today. Declared in build_eg.py rather than assumed. Every figure "
            "published after its origin carries a publication_lag_note saying why "
            "the origin could have had it; there is deliberately no grace period "
            "in days, since a cutoff would be a free parameter nobody measured."),
        "measured": measured,
        "unsourced": UNSOURCED,
        "origins": origins,
    }
    json.dump(blob, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("wrote %s — %d origins" % (os.path.relpath(path), len(origins)))


if __name__ == "__main__":
    main()
