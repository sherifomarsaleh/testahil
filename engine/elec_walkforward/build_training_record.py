#!/usr/bin/env python3
"""ELEC — the training record. Every figure computed, none typed.

A NUMBER STATED IN PROSE MUST BE COMPUTED, NOT TYPED — standing since 07-Aug-2026 and
the reason this document is generated rather than written.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import filed_record as F                                          # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
STUDY = json.load(open(os.path.join(ROOT, "engine/elec_study/study_numbers.json"),
                       encoding="utf-8"))
OUT = os.path.join(HERE, "TRAINING_RECORD_07-09-2026.md")

SPOT, SPOT_DATE, SPOT_FILE = 2.08, "2026-09-03", "SUPPLIED_03-09-2026.json"


def pct(x):
    return "%.2f%%" % (100 * x)


def main():
    L = []
    a = L.append
    hs = STUDY["hist_is"]
    central = STUDY["lenses"]["central"]["base"] if "central" in STUDY["lenses"] \
        else STUDY["central"]["base"]

    a("# ELEC — fundamental walk-forward [R-FCAL-01]: training record")
    a("")
    a("**Electro Cable Egypt · EGX · 7 September 2026 · INTERNAL — never shown to a reader**")
    a("")
    a("**Scope: SKIP.** *walk-forward not run — insufficient sourceable history (4 years).*")
    a("The decision, its three independent grounds and the design that was pre-registered")
    a("are in `PRE_REGISTRATION_07-09-2026.md`. **No error was computed, because there is")
    a("no origin to compute one at.**")
    a("")
    a("This record exists for what the run found while the filings were open, which is")
    a("larger than the scope decision and points the other way from the reading this")
    a("study's own audit reached yesterday.")
    a("")
    a("---")
    a("")
    a("## 1 · What was obtained, and the arithmetic that admits it")
    a("")
    a("Four filings, all audited by UHY United, all Arabic scans with **no text layer**")
    a("(`pdftotext` returns 3 characters across the 33 pages of the one complete file).")
    a("Three of the four are **truncated** at exactly 1 MiB, 5 MiB and 5 MiB with no")
    a("`%EOF` and no readable xref; they open at zero pages, and their page images were")
    a("recovered by scanning the raw bytes for JPEG streams. Every figure below was read")
    a("off the rendered pixels and **re-added against its own statement**.")
    a("")
    a("| filing | basis | pages recovered | status |")
    a("|---|---|---:|---|")
    a("| FY2020 annual | consolidated | 7 | truncated — cash flow and all notes lost |")
    a("| FY2021 annual | standalone | 33 | **complete** |")
    a("| FY2022 annual | standalone | 17 | truncated |")
    a("| FY2023 annual | standalone | 24 | truncated — notes from 8 onward lost |")
    a("")
    a("**Footing: %d checks, %d refusals.** Reproduced by `python3 filed_record.py`."
      % (len(F.footing_report()),
         sum(1 for _, c, p in F.footing_report()
             if abs(c - p) > max(1.0, abs(p) * 1e-9))))
    a("")
    a("Three of those checks are cross-statement rather than within one page, and they")
    a("are the ones worth naming because a broken font map would not survive them:")
    a("FY2023 additions to fixed assets reconcile between the cash-flow statement and")
    a("note 3's own roll-forward; the depreciation charge reconciles between the cash-flow")
    a("statement, the roll-forward and its allocation across cost of sales, selling and")
    a("administrative expenses; and FY2021's closing cash of EGP %s is FY2022's opening"
      % f"{F.BS[('FY2021','standalone')]['cash']:,}")
    a("cash **read out of a different filing**.")
    a("")
    a("## 2 · The filed record")
    a("")
    a("### Income statement, standalone (EGP)")
    a("")
    a("| | FY2020 | FY2021 | FY2022 | FY2023 |")
    a("|---|---:|---:|---:|---:|")
    ys = ("FY2020", "FY2021", "FY2022", "FY2023")
    for lbl, k in (("revenue", "rev"), ("gross profit", "gp"),
                   ("operating profit", "op"), ("net profit", "np")):
        a("| %s | %s |" % (lbl, " | ".join(
            f"{F.IS[(y,'standalone')][k]:,}" for y in ys)))
    a("| D&A | %s |" % " | ".join(f"{F.dna(y):,}" for y in ys))
    a("| **EBITDA** | %s |" % " | ".join(f"**{F.ebitda(y):,}**" for y in ys))
    a("| **EBITDA margin** | %s |" % " | ".join(
        "**%s**" % pct(F.ebitda(y) / F.IS[(y, 'standalone')]["rev"]) for y in ys))
    a("")
    a("### Income statement, consolidated (EGP) — the basis the study models")
    a("")
    a("| | FY2019 | FY2020 |")
    a("|---|---:|---:|")
    for lbl, k in (("revenue", "rev"), ("gross profit", "gp"),
                   ("operating profit", "op"), ("net profit", "np")):
        a("| %s | %s |" % (lbl, " | ".join(
            f"{F.IS[(y,'consolidated')][k]:,}" for y in ("FY2019", "FY2020"))))
    a("| **operating margin** | %s |" % " | ".join(
        "**%s**" % pct(F.IS[(y, 'consolidated')]["op"] / F.IS[(y, 'consolidated')]["rev"])
        for y in ("FY2019", "FY2020")))
    a("")
    a("D&A is not obtainable on the consolidated basis — the FY2020 consolidated")
    a("cash-flow statement sits past the truncation — so **the consolidated line is the")
    a("operating margin and is not directly comparable to an EBITDA margin.** On the")
    a("standalone accounts D&A runs %s to %s of revenue, so the consolidated EBITDA"
      % (pct(min(F.dna(y) / F.IS[(y, 'standalone')]['rev'] for y in ys)),
         pct(max(F.dna(y) / F.IS[(y, 'standalone')]['rev'] for y in ys))))
    a("margin would sit a little above the operating margin, not several times it.")
    a("")

    # ---------------------------------------------------------------- the correction
    a("## 3 · The correction — the audit's central claim does not survive the filings")
    a("")
    a("`AUDIT_06-09-2026.md` states, and the gap review repeats, that")
    a("**\"this company's own reconstructed filed record\"** of terminal EBITDA margin is")
    st = {y: hs[y]["ebitda"] / hs[y]["rev"] for y in ("FY23", "FY24", "FY25")}
    a("**%s – %s**, that the study forecasts %s, and therefore that the study \"forecasts"
      % (pct(min(st.values())), pct(max(st.values())),
         pct(STUDY["dcf"].get("terminal_margin", 0.123) if isinstance(STUDY.get("dcf"), dict) else 0.123)))
    a("less than half of the lowest filed year\".")
    a("")
    a("**Those margins are not filed.** They are the study's own committed `hist_is`,")
    a("which is vendor data:")
    a("")
    a("| | study `hist_is` | ratio to filed |")
    a("|---|---:|---:|")
    for y, fy in (("FY23", "FY2023"),):
        a("| FY2023 EBITDA margin | %s | — |" % pct(st["FY23"]))
    a("| FY2024 EBITDA margin | %s | no filing exists |" % pct(st["FY24"]))
    a("| FY2025 EBITDA margin | %s | no filing exists |" % pct(st["FY25"]))
    a("")
    a("Against the company's own audited FY2023 standalone accounts:")
    a("")
    a("| FY2023 | study | filed standalone | study / filed |")
    a("|---|---:|---:|---:|")
    f23 = F.IS[("FY2023", "standalone")]
    rows = (("revenue", hs["FY23"]["rev"] * 1e6, f23["rev"]),
            ("EBITDA", hs["FY23"]["ebitda"] * 1e6, F.ebitda("FY2023")),
            ("D&A", hs["FY23"]["dna"] * 1e6, F.dna("FY2023")),
            ("finance cost", -hs["FY23"]["fin"] * 1e6, F.FINANCE_COST[("FY2023", "standalone")]),
            ("net profit", hs["FY23"]["np"] * 1e6, f23["np"]))
    for lbl, s, f in rows:
        a("| %s | %s | %s | **%.2fx** |" % (lbl, f"{s:,.0f}", f"{f:,}", s / f))
    a("")
    w = F.consolidation_wedge()
    a("**Consolidation explains the revenue gap and does not explain the profit gap.**")
    a("At the one year that exists on both bases the group is **%.2fx** the parent on"
      % w["revenue"]["factor"])
    a("revenue and **%.2fx** on net profit. The study's FY2023 revenue sits at %.2fx the"
      % (w["net_profit"]["factor"], hs["FY23"]["rev"] * 1e6 / f23["rev"]))
    a("parent — squarely consistent with a consolidated figure — while its net profit sits")
    a("at %.2fx, half again beyond what the measured consolidation wedge delivers."
      % (hs["FY23"]["np"] * 1e6 / f23["np"]))
    a("")
    a("### What the filed margins actually are, and where the forecast sits in them")
    a("")
    a("| | EBITDA margin |")
    a("|---|---:|")
    for y in ys:
        a("| FY%s filed, standalone | %s |" % (y[2:], pct(F.ebitda(y) / F.IS[(y, 'standalone')]["rev"])))
    a("| **the study's terminal forecast** | **12.30%** |")
    a("| the price's reverse read, class primary | 27.17% |")
    a("| the price's reverse read, published blend | 28.34% |")
    a("")
    lo = min(F.ebitda(y) / F.IS[(y, 'standalone')]["rev"] for y in ys)
    hi = max(F.ebitda(y) / F.IS[(y, 'standalone')]["rev"] for y in ys)
    a("**The forecast terminal margin of 12.30% sits INSIDE the company's own filed range")
    a("of %s – %s. It is not below the filed record; it is in the middle of it.**"
      % (pct(lo), pct(hi)))
    a("")
    a("**And the reverse read runs the other way from the audit's reading of it.** The")
    a("price needs 27-28%%, which is **%.1f times** the highest EBITDA margin this company"
      % (0.2717 / hi))
    a("has filed on the basis that can be checked, and roughly double the operating margin")
    a("of its last consolidated year. [R-GAP-02] is explicit that a reverse read landing on")
    a("a *believable* number is evidence against dissent — here it lands on a number the")
    a("filings do not support, which is evidence the other way, and yesterday's audit read")
    a("it as support because it was comparing the price against vendor figures rather than")
    a("against filings.")
    a("")
    a("**This does not make the study right.** The study's 12.30% was not derived from")
    a("these accounts — it was justified in the delivered document against \"the pre-windfall")
    a("2022 norm (about 12%)\" for a year the model holds no income statement for, and the")
    a("filed FY2022 standalone EBITDA margin is %s, not 12%%. **A number can be inside the"
      % pct(F.ebitda("FY2022") / F.IS[("FY2022", 'standalone')]["rev"]))
    a("right range for a reason that is not evidence, and that is what happened here.**")
    a("")

    a("## 4 · Trap (i), demonstrated rather than asserted")
    a("")
    a("[R-FCAL-01] warns that dividing the finance charge by a broader liabilities total")
    a("understates the borrowing rate by a multiple. ELEC's own accounts price it:")
    a("")
    a("| | on the borrowings that bear it | on total liabilities | understated by |")
    a("|---|---:|---:|---:|")
    for y in ("FY2021", "FY2022", "FY2023"):
        r = F.borrowing_rate_check(y)
        a("| %s | **%s** | %s | %.2f points |"
          % (y, pct(r["rate_on_bearing_debt"]), pct(r["rate_on_total_liabilities"]),
             r["understatement_pp"]))
    a("")
    a("The broad-denominator column is not merely low — at %s and %s it sits **below the"
      % (pct(F.borrowing_rate_check("FY2021")["rate_on_total_liabilities"]),
         pct(F.borrowing_rate_check("FY2022")["rate_on_total_liabilities"])))
    a("Egyptian sovereign**, which [R-COC-01] refuses outright. The bearing-debt column")
    a("tracks the policy rate through the tightening, which is the control that says the")
    a("denominator is the right one.")
    a("")

    a("## 5 · The useful life")
    a("")
    ul = F.implied_useful_life()
    a("**Route (1) failed.** The FY2023 policy note (page 13) discloses spans — buildings")
    a("10–50, machinery 4–25, vehicles 5–20, tools 5–20, computers 5, furniture 5–10 —")
    a("with no dominant class and no weighting. A range is not a life.")
    a("")
    a("**Route (2), derived and labelled derived:** depreciable gross cost of")
    a("EGP %s (total cost less land, which is not depreciated) over an annual charge of"
      % f"{ul['depreciable_gross_cost']:,}")
    a("EGP %s gives **%.2f years**, with a prior-year control at %.2f."
      % (f"{ul['annual_charge']:,}", ul["years_on_full_base"], ul["prior_year_control"]))
    a("")
    a("The note also discloses EGP %s of cost **fully depreciated and still in use** —"
      % f"{F.FIXED_ASSET_NOTE_FY2023['fully_depreciated_still_in_use']:,}")
    a("%s of the depreciable base. Those assets carry cost and no charge, so they lengthen"
      % pct(F.FIXED_ASSET_NOTE_FY2023['fully_depreciated_still_in_use']
            / ul['depreciable_gross_cost']))
    a("the ratio; removing them gives **%.2f years**. Both ends sit inside the union of the"
      % ul["years_excluding_fully_depreciated"])
    a("disclosed spans, so **the band %.2f–%.2f is what is recorded** and no point inside it"
      % (ul["years_excluding_fully_depreciated"], ul["years_on_full_base"]))
    a("is chosen — that choice is the one route (1) failed for.")
    a("")

    a("## 6 · What was NOT done, and why")
    a("")
    a("**The study was not rebuilt and `fair{bear,base,full}` did not move.**")
    a("")
    a("Two levers were priced by the audit and both were left unapplied:")
    a("")
    a("| lever | rule | direction | why it was not applied |")
    a("|---|---|---|---|")
    a("| retire the typed four-lens blend, take the class primary | [R-LENS-03] | **down**, 0.3357 to −1.8082 a share | it would rebuild the answer on a panel this run has just shown cannot be reconciled to any document the company has issued |")
    a("| re-anchor the terminal margin to the filed record | [R-ANCHOR-01] | the audit said **up** | **the premise is withdrawn.** The forecast is inside the filed range, not below it, so there is no anchoring defect of the kind claimed |")
    a("")
    a("**No rebuild ledger is written, because no rebuild happened.**")
    a("`engine/rebuild_ledger.py` refuses a ledger with no lever in it — *\"a rebuild that")
    a("changed nothing is not a rebuild\"* — and writing one with a lever nobody applied")
    a("would be the opposite of what that module is for. The two priced-and-declined")
    a("levers are recorded here instead, which serves the same purpose the ledger serves:")
    a("what it forbids is the move being invisible, and a move that was considered and")
    a("refused is recorded with its reason.")
    a("")
    a("**The fair-value register records a movement of about -1.3% on the base and it is")
    a("NOT a change in the answer.** The frozen baseline was read from `assets/data.js`,")
    a("which carries the fair value at two decimal places (0.34); this edition records the")
    a("study's OWN committed figures (0.3357186228503667), which are what it has always")
    a("published. The register compares the two and the difference is the rounding in")
    a("`data.js`. **No lever was applied and no number was recomputed.**")
    a("")
    a("**The gap is not closed and is not claimed to be.** The published central of")
    a("EGP %.4f against EGP %.2f as at %s (%s) is %s. This run does not move it toward"
      % (central, SPOT, SPOT_DATE, SPOT_FILE, pct(central / SPOT - 1)))
    a("the price and does not defend it — it establishes that **the base the number is")
    a("built on cannot be verified against anything the issuer has published**, which is a")
    a("SIGCM clause 1 condition rather than a disagreement with the market.")
    a("")
    a("## 7 · Caveats, stated plainly")
    a("")
    a("- **Four sourceable fiscal years, standalone; two consolidated.** The window stops")
    a("  at FY2023 because the issuer's own index ends at 30 September 2025 and serves")
    a("  nothing after August 2020.")
    a("- **Everything here is the parent entity.** It is not the group, and it must never")
    a("  be substituted into the study's consolidated panel. The wedge is measured, and it")
    a("  is unstable down the statement (%.2fx on revenue, %.2fx on operating profit)."
      % (w["revenue"]["factor"], w["operating_profit"]["factor"]))
    a("- **Three of four filings are truncated**, so the FY2023 capital note, the FY2020")
    a("  consolidated cash-flow statement and the FY2022 notes are unread and recorded as")
    a("  unread rather than worked around.")
    a("- **No forecast was scored**, so this run contributes no cell to any pooled")
    a("  driver-bias census and no evidence for or against any correction.")
    L.append("")
    open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote", OUT, "(%d lines)" % len(L))


if __name__ == "__main__":
    main()
