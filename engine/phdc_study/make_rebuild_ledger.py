"""The route this rebuild took, in the order the levers were applied [R-REBUILD-01]."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rebuild_ledger import Ledger, Lever, assert_rebuild, render
from dataclasses import asdict

HERE = os.path.dirname(os.path.abspath(__file__))
L = Ledger(
    ticker="PHDC", started_at="2026-09-17", start_value=17.847764793737, start_spot=14.40,
    audit_after=("DECLARED BEFORE ANY FIGURE WAS RECOMPUTED, and published in the commit that "
                 "committed the extraction: the running total is read AFTER EVERY LEVER, and "
                 "the sequence stops for an eight-heading review if the cumulative move passes "
                 "20 per cent or if the central crosses the traded price. BOTH CONDITIONS FIRED "
                 "at lever 3 and the review is GAP_REVIEW_17-09-2026.md."),
    levers=[
        Lever(name="the bridge onto the reviewed 30-June-2026 balance sheet",
              rule="R-BRIDGE-01", before=17.847764793737, after=16.455050200744573,
              why=("The bridge stood on 31 March 2026 while the company's reviewed 30 June "
                   "2026 statements existed. That is the stale-sheet defect the rule was "
                   "adopted on, and the document arrived during this pass."),
              evidence=("Net debt 23,244.719 -> 27,471.220 on the study's OWN eight-line "
                        "gross-debt definition, verified by reproducing its committed "
                        "31-March figure of 32,369.847 from those same eight lines before "
                        "applying them to June. Associates 3,838.697 -> 3,898.478, investment "
                        "property 1,020.475 -> 1,008.420, minority book 1,432.671 -> "
                        "1,723.049. Every subtotal footed: A = L + E exactly, current assets "
                        "exactly, non-current liabilities exactly, parent + minority exactly.")),
        Lever(name="the gross-margin anchor onto the reviewed half",
              rule="R-ANCHOR-01", before=16.455050200744573, after=16.455050200744573,
              why=("The forecast margin was anchored on the 1Q2026 earnings release; a "
                   "reviewed half to 30 June 2026 now exists and a near-term reviewed actual "
                   "outranks anything earlier."),
              evidence=("35.4839 per cent -> 35.4670, seventeen hundredths of a point, and "
                        "THE ANSWER DOES NOT MOVE AT FOUR DECIMAL PLACES. Recorded as a lever "
                        "rather than dropped because the anchor's QUALITY changed even though "
                        "its level did not: a reviewed half replaces a release that rounded "
                        "its gross profit to the nearest hundred million. A lever worth zero "
                        "is evidence about the rebuild, and leaving it out would overstate "
                        "how much of the move the other two explain.")),
        Lever(name="the cash-conversion rate onto the reviewed half",
              rule="R-ANCHOR-01", before=16.455050200744573, after=13.912894753552722,
              why=("The base case was the MEAN of three full-year conversion rates -- 4.333, "
                   "17.870 and 3.938 per cent -- a three-year average standing in for a rate "
                   "the company has since reported, and an average of a quantity that swings "
                   "by a factor of four. This is the study's own crux."),
              evidence=("Operating cash flow 1,499.068 over revenue 19,528.118 = 7.676 per "
                        "cent, against the 8.714 the mean produced. THE DIRECTION IS MEASURED "
                        "LIKE FOR LIKE IN THE COMPANY'S OWN PERIOD PAIR, from the same "
                        "reviewed statement's own prior-year column: the SAME half a year "
                        "earlier converted at 3.114 per cent, so 3.114 -> 7.676 half against "
                        "half, and the adopted level is not a seasonal artefact of using six "
                        "months where the old rate used twelve. The envelope is unchanged and "
                        "is still the range of filed full-year outcomes.")),
    ])

if __name__ == "__main__":
    rec = asdict(L)
    nums = json.load(open(os.path.join(HERE, "study_numbers.json"), encoding="utf-8"))
    rec["value"] = nums["lens_weighted"]["base"]
    rec["cumulative_move"] = rec["value"] / rec["start_value"] - 1.0
    # SEVERAL LEVERS SERVING ONE RULE ARE ONE PIECE OF EVIDENCE, NOT SEVERAL
    # [R-REBUILD-01] -- read as three corrections this is a landslide, and read as
    # TWO RULES it is a bridge worth -7.8 per cent and an anchoring rule worth -15.4.
    groups = {}
    for lv in rec["levers"]:
        g = groups.setdefault(lv["rule"], {"levers": [], "first_before": lv["before"],
                                           "last_after": lv["after"], "move": 0.0})
        g["levers"].append(lv["name"]); g["last_after"] = lv["after"]
        g["move"] = g["last_after"] / g["first_before"] - 1.0
    rec["rules"] = groups
    rec["distinct_rules"] = sorted(groups)
    for lv in rec["levers"]:
        lv["move"] = lv["after"] / lv["before"] - 1.0
    rec["start_gap"] = rec["start_value"] / rec["start_spot"] - 1.0
    rec["gap"] = rec["value"] / rec["start_spot"] - 1.0
    assert_rebuild(rec, "PHDC")
    json.dump(rec, open(os.path.join(HERE, "rebuild_ledger.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    print(render(rec) if callable(render) else "")
    print("cumulative move: %+.2f%%  (%.4f -> %.4f against a spot of %.2f)"
          % (rec["cumulative_move"] * 100, rec["start_value"], rec["value"], rec["start_spot"]))
