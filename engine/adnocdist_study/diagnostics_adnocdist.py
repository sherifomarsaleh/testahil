"""ADNOCDIST — the reverse read and the sign test.  [R-ENF-05]

THE REVERSE READ. This study states what it believes. It has never stated what
the PRICE believes, and the two are the same model read backwards. Solved here:
the SINGLE FLAT DISCOUNT RATE that reproduces the traded price on this study's
own free cash flows, its own terminal cash flow and its own terminal growth,
holding every driver at its published value — against the flat rate that
reproduces THIS STUDY'S OWN enterprise value on the identical construction, so
the two are the same quantity measured twice.

WHY THAT QUANTITY AND WHY A SECOND READING BESIDE IT. Three-quarters of this
enterprise value sits beyond the last explicit year, so the disagreement with the
market is a disagreement about the price of time and about the long run, and the
study's own reverse valuation says so. But the study's own reverse valuation is
solved through revalue(), which returns the CASH-FLOW LENS — and the answer this
study publishes is the weighted centre of four lenses, a different number. A read
solved against a lens the study does not publish overstates the disagreement, so
the cross-reads below solve the same question against the answer a reader
actually receives, by re-running the whole model.

THE PRICE IS THE LATEST KNOWN ONE, NOT THE STRIKE. [R-GAP-01] as amended says a
fair value is put against the latest known close; the study was struck at AED
4.07 on 7 August and the latest known close is AED 4.02 on 3 September. Both are
solved and both are printed, because a reverse read against a month-old price is
a comparison a reader cannot use.

THE CONTAINMENT RULE IS THE POINT, NOT A FORMALITY. A rate solved from a price
and then used anywhere in the valuation is the reverse-engineered rate the
protocol prohibits outright, arriving through a side door. So this module writes
diagnostics.json and NOTHING READS IT BACK; it is named `diagnostics_*` so the
exemption applies to the file that COMPUTES the read rather than to a builder
that consumes it; and it ASSERTS, before writing, that the solved value appears
nowhere in study_numbers.json, which is the file every builder does read.

THE SIGN TEST. Any single contested choice is defensible; what is not is a study
resolving every one of them the same way and never noticing. Every alternative
below is valued by RE-RUNNING THIS STUDY'S OWN compute.py with that one choice
changed and everything else held — so the difference measures the CHOICE and not
the construction — and each source substitution is asserted to have landed
exactly once before the run is believed. Nothing here changes a driver, a
forecast, a rate or a fair value: the alternatives are computed and reported,
never adopted.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
NUM = os.path.join(HERE, "study_numbers.json")
COMPUTE = os.path.join(HERE, "compute.py")

# the price this read is solved at, and where it comes from
PRICE_FILE = os.path.join(ENGINE, "prices", "SUPPLIED_03-09-2026.json")

SRC = open(COMPUTE, encoding="utf-8").read()
ANCHOR = "V = {k: v['value'] for k, v in INP.items()}"
assert SRC.count(ANCHOR) == 1, "compute.py's input dictionary is not where this expects it"


# --------------------------------------------------------------------------
# THE STUDY'S OWN MODEL, RE-RUN WITH ONE THING CHANGED
#
# The alternative framings are not re-implemented here. compute.py is executed
# in a scratch directory with __file__ pointed at it, so the run writes ITS
# study_numbers.json there and cannot touch the committed one; an input override
# is injected at the single line where the input dictionary becomes the value
# dictionary, so everything downstream re-derives through the study's own code;
# and a fork that is a CONSTRUCTION rather than an input is a minimal source
# substitution, asserted to have landed.
# --------------------------------------------------------------------------
def run(overrides=None, patches=(), label=""):
    src = SRC
    for old, new in patches:
        n = src.count(old)
        assert n == 1, ("the substitution %r landed %d times, not once (%s). A fork "
                        "valued through a substitution that did not land is a fixture "
                        "that never injected its condition." % (old[:70], n, label))
        src = src.replace(old, new)
    src = src.replace(ANCHOR, ANCHOR + "\nV.update(_OVR)", 1)
    d = tempfile.mkdtemp(prefix="adnocdist_alt_")
    try:
        for f in ("step0_result.json", "backtest_5y.json", "vol_diagnostic.json",
                  "width_diagnostic.json"):
            p = os.path.join(HERE, f)
            if os.path.exists(p):
                shutil.copy(p, d)
        g = {"__name__": "_alt", "__file__": os.path.join(d, "compute.py"),
             "_OVR": dict(overrides or {})}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src, "compute.py", "exec"), g)
        return g
    finally:
        shutil.rmtree(d, ignore_errors=True)


def bisect(fn, lo, hi, target, n=200):
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        if fn(mid) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# --------------------------------------------------------------------------
# the forks, each as (name, adopted, alternative, overrides, substitutions, why)
# --------------------------------------------------------------------------
GLIDE = [("W['beta_drift_frac'] = 0.0", "W['beta_drift_frac'] = V['beta_drift_frac']"),
         ("W['beta_terminal'] = W['beta']",
          "W['beta_terminal'] = W['beta'] + W['beta_drift_frac'] * (1 - W['beta'])"),
         ("W['wd_terminal'] = W['wd']", "W['wd_terminal'] = V['wd_terminal']")]
WC_TRADE = [("    rec = WC['dso_all'] / 365 * F['revenue'][i]",
             "    rec = WC['dso_trade'] / 365 * F['revenue'][i]"),
            ("    pay = WC['dpo_all'] / 365 * F['direct_costs_A'][i]",
             "    pay = WC['dpo_trade'] / 365 * F['direct_costs_A'][i]"),
            ("_nwc, _prev, _dnwc = [], WC['nwc_fy25'], []",
             "_nwc, _prev, _dnwc = [], (V['tr_fy25'] + V['inv_fy25'] - V['tp_fy25']), []")]
NET_CAPEX = [("    cpx.append(_maint + _growth)", "    cpx.append(_d + _OVR['_net_capex'])")]
THREE_LEG = [("L['just_fwd_pe'] = L['pe_method_justified']",
              "L['just_fwd_pe'] = sum(L['pe_methods']) / 3")]
PAYOUT_FLOOR = [("L['pe_method_justified'] = (L['pe_payout_implied'] * (1 + V['g_terminal'])",
                 "L['pe_method_justified'] = (V['payout_floor'] * (1 + V['g_terminal'])")]
ROE_LATEST = [("L['roe_sust'] = roe_sust", "L['roe_sust'] = roe_hist[-1]"),
              ("just_pb = (roe_sust - V['g_terminal']) / (W['ke'] - V['g_terminal'])",
               "just_pb = (roe_hist[-1] - V['g_terminal']) / (W['ke'] - V['g_terminal'])")]
FY27_EPS = [("    pbt = F[f'ebit_{frame}'][0] + V['intinc_fy25'] - V['fin_fy25']",
             "    pbt = F[f'ebit_{frame}'][1] + V['intinc_fy25'] - V['fin_fy25']")]
BRIDGE_H126 = [("    nd = H['FY2025']['net_debt_company']", "    nd = _OVR['_nd']"),
               ("    lease = V['lease_fy25']", "    lease = _OVR['_lease']"),
               ("    nci_ = V['nciq_fy25']", "    nci_ = _OVR['_nci']")]
MINORITY_VALUE = [("    nci_ = V['nciq_fy25']",
                   "    nci_ = _OVR['_nci_share'] * (ev - nd - lease)")]
MARGIN_NO_STEP = [("m = UB['margin_comm_h126']\nmc = []",
                   "m = UB['margin_comm_h126'] / (1 + V['gp_comm_per_l_g'][0])\nmc = []")]
LEASES_OPERATING = [("_open = V['ppe_fy25'] + V['rou_fy25']", "_open = V['ppe_fy25']"),
                    ("c = H['FY2025']['cash_opex']",
                     "c = H['FY2025']['cash_opex'] + V['leasepay_fy25']"),
                    ("    lease = V['lease_fy25']", "    lease = 0.0")]


def forks(base, fig):
    """Every fork this study resolved that a reader could reasonably resolve the
    other way, with the alternative built from the study's OWN committed record.

    NO MODEL-DERIVED NUMERAL IS TYPED INTO A REASON. Every figure quoted in a `why`
    below is interpolated from `fig`, which this module computed, or is a figure the
    company itself disclosed and this study committed with its source.
    """
    V, H, DCF = base["V"], base["H"], base["DCF"]
    return [
        dict(
            name="the central: the four-lens weighted blend vs the class primary alone",
            adopted="a weighted centre — cash flow 40%, normalised earnings 25%, "
                    "relative multiple 20%, book and sustainable return 15%",
            alternative="the cash-flow lens alone as the central, the others published "
                        "beside it as cross-checks",
            fixed=DCF["frame_A"]["per_share"], fixed_b=DCF["frame_B"]["per_share"],
            why="[R-LENS-03] retires the typed blend: one class primary IS the central, the "
                "other lenses are cross-checks, and book value is a disclosed floor that is "
                "never weighted. Three of the four weighted lenses here value the company on "
                "reported accounting earnings and historical-cost book, and the weights "
                "never cleared an out-of-sample test. This is the study's largest contested "
                "construction and it is on that rule's ratchet until the study is rebuilt; "
                "the alternative is the study's own cash-flow reading, unchanged, not a new "
                "model."),
        dict(
            name="the FY2026 commercial margin per litre: a +17.0% step vs the 2.0% "
                 "escalator the retail leg takes",
            adopted="a 17.0% step in FY2026, described as the realised first-half outcome",
            alternative="the same 2.0% domestic escalator the retail margin per litre takes",
            ovr=dict(gp_comm_per_l_g=[0.020] * 5),
            why="The step is applied TO the realised first half — the commercial margin per "
                "litre is anchored on the disclosed half-year figure and the escalator then "
                "multiplies it — so the realised outcome is the anchor rather than the case "
                "for the step, and that anchor is already 19.2% above the prior-year half on "
                "the company's own disclosure. The company's own quarterly figures have "
                "underlying EBITDA falling from USD 305mn in the first quarter to USD 298mn "
                f"in the second. A harsher reading still, holding the margin flat at the "
                f"realised half with no FY2026 step at all, gives AED {fig['margin_no_step']:.4f}."),
        dict(
            name="terminal growth: a typed nominal 1.50% vs the house AE terminal of 2.00% "
                 "at zero real growth",
            adopted="1.50% nominal, set below the domestic escalator for the "
                    "electric-vehicle drag",
            alternative="2.00% nominal, the house AE terminal inflation at zero real growth",
            ovr=dict(g_terminal=0.020),
            why="[R-MACRO-01] stores a growth rate as (real, inflation path) and recomputes "
                "the nominal. A typed 1.50% against a terminal inflation of "
                f"{100 * fig['pi_term']:.2f}% is a real decline of "
                f"{-100 * fig['study_real_g']:.3f}% a year in perpetuity — which may well be "
                "right for a fuel retailer facing the transition this study models, and "
                "which the study nowhere writes down as the real number it is. The "
                "alternative is the house path's own terminal, not a view."),
        dict(
            name="country risk: a 4bp market default spread stripped against a 64bp rating "
                 "premium added back, vs the rating basis on both sides",
            adopted="strip the 4bp spread the July-2026 dirham auction actually contains, "
                    "add back the 64bp rating-based country premium",
            alternative="the rating basis on both sides — strip the 42bp rating default "
                        "spread, add back the same 64bp premium",
            ovr=dict(sov_spread=0.0042),
            why="Country risk must enter exactly once and the SAME basis must be stripped as "
                "is added back. The study strips a market-observed 4bp and adds back a "
                "rating-based 64bp, and gives its reason in its own record: removing 42bp "
                "from a bond that carries 4bp puts the normalised rate below the "
                "matched-tenor Treasury under a hard peg, which cannot be right. The reason "
                "is good and the bases still do not match, so both are priced. The "
                "consistent-basis reading lowers the normalised risk-free rate by 38bp and "
                "the cost of equity with it."),
        dict(
            name="the justified multiple's payout: derived from the sustainable-growth "
                 "identity vs the company's own 75% policy floor",
            adopted="payout = 1 - g/ROE, so the multiple satisfies g = retention x return",
            alternative="the 75% of net profit the dividend policy actually commits to",
            patch=PAYOUT_FLOOR,
            why="Both are defensible and they are not the same question. The identity keeps "
                "the multiple internally consistent — at a sustainable return on equity of "
                f"{100 * fig['roe_sust']:.1f}% a 75% payout implies growth far above the "
                "1.5% the same multiple capitalises — and it removes the free parameter the "
                "critiques objected to. The company's disclosed commitment is nonetheless "
                "75% of net profit or USD 700mn if higher, and the board paid the floor "
                "rather than a share of the spiked half-year profit. Adopting the identity "
                f"raises the payout the multiple uses to {100 * fig['payout_implied']:.1f}% "
                "and raises the value."),
        dict(
            name="tax: the audited FY2025 effective rate of 10.17% vs the 15% domestic "
                 "minimum top-up",
            adopted="10.17%, the rate the audited FY2025 reconciliation actually shows",
            alternative="15%, the domestic minimum top-up rate in force for groups above "
                        "the revenue threshold",
            ovr=dict(tax_effective=0.15),
            why="The company is plainly within the size threshold and its own audited "
                "reconciliation does not apply the top-up; the reviewed half-year runs "
                "10.09%. Following the filing rather than the reader's expectation of it is "
                "the source rule working. It is a risk rather than a defect, and it is the "
                "largest single identifiable downside construction the study itself names — "
                "the study prices it on its own cash-flow lens and this row carries it "
                "through every lens the rate touches, which is why the figure here is "
                "larger."),
        dict(
            name="inventory movements: normalised to zero from FY2027 vs carried at the "
                 "FY2024-FY2025 average",
            adopted="published BOTH ways and never averaged — Frame A and Frame B",
            alternative="a single central reading",
            fixed=base["L"]["centre_B"], fixed_b=base["L"]["centre_A"],
            why="The study takes no side and the dual framing is the right answer: inventory "
                "movements are not a line in the audited statements, appearing only in "
                "management commentary with no reconciliation to the accounts. The two "
                "branches are recorded here as the two framings so the fork is measured "
                "rather than exempted. The direction below is an artefact of anchoring this "
                "record on Frame A, which is the branch the shared reader resolves; the "
                "difference sits under the materiality bar at the published centre though it "
                f"is {100 * fig['inv_lens_share']:.1f}% on the cash-flow lens alone."),
        dict(
            name="the cost of capital: flat, vs the glide to a drifted beta and a 10% "
                 "terminal debt weight",
            adopted="flat — today is the terminal under a hard peg, so the explicit and "
                    "terminal rates are identical",
            alternative="the glide the delivered document still describes, with beta "
                        "drifting 38.9% of the way to one and a 10% terminal debt weight",
            patch=GLIDE,
            why="Flat is what the cost-of-capital procedure returns for a pegged market and "
                "it is the right construction. The retired glide is priced here because "
                "eight delivered passages still describe it, so a reader has been told the "
                "study does something it does not — a defect already on the study's own "
                "findings list. Adopting flat raises the value, and the alternative is what "
                "the document says is being done."),
        dict(
            name="the relative lens's earnings year: FY2026, the inventory-gain peak, vs "
                 "FY2027",
            adopted="FY2026 forward earnings",
            alternative="FY2027 forward earnings",
            patch=FY27_EPS,
            why="FY2026 carries the AED 762mn realised inventory gain the company itself "
                "excludes from underlying EBITDA, and it is higher than FY2027, FY2028 and "
                "FY2029 operating profit, so a multiple applied to it capitalises the peak "
                "year. The lens was de-circularised when the price-derived legs were "
                "dropped; the year it is applied to was not revisited."),
        dict(
            name="the reference multiple: the fundamentals-derived leg alone vs the "
                 "three-leg average carrying the traded multiples",
            adopted="the justified multiple alone",
            alternative="the average of the justified multiple, today's traded multiple and "
                        "the own three-year mean",
            patch=THREE_LEG,
            why="Two of the three legs are the traded price divided by earnings, so the "
                "three-leg average made a lens presented as independent evidence about value "
                "two-thirds a restatement of the price it was being compared against. "
                "Dropping them is right and it LOWERED the value; the alternative is what "
                "the first edition published."),
        dict(
            name="the impairment and credit-loss charge: normalised down vs held at the "
                 "annualised first half of 2026",
            adopted="FY2026 at the realised first half annualised, then a normalised level "
                    "escalating with inflation",
            alternative="held at the annualised first-half rate for the whole window",
            ovr=dict(impair_norm=[360.0] * 5),
            why="FY2025 carried AED 284.3mn and the first half of 2026 AED 179.9mn, both "
                "described by the company as prudence-based provisioning. Calling the "
                "elevated level temporary is a judgement about a charge that has risen in "
                "each of the last two periods, and it is made in the direction that raises "
                "the value."),
        dict(
            name="the terminal return on capital: faded to 25.0% vs the company's own "
                 "disclosed FY2025 figure",
            adopted="25.0%, fading the disclosed return toward a mature network",
            alternative="the return on capital employed the company itself disclosed for "
                        "FY2025",
            ovr=dict(roic_terminal=0.327),
            why="The company disclosed 32.7% for FY2025 and 40.1% for the first half of "
                "2026 on its own measure, and this study's own committed history computes "
                f"{100 * H['FY2025']['roce']:.1f}% for FY2025 on the study's own definition. "
                "The fade is the conservative side and it costs value, because the terminal "
                "reinvestment charge is growth over return."),
        dict(
            name="the sustainable return in the book lens: the three-year mean vs the "
                 "latest audited year",
            adopted="the three-year mean of the return on equity attributable to "
                    "shareholders",
            alternative="the latest audited year alone",
            patch=ROE_LATEST,
            why="The return rose in each of the three audited years, so the mean "
                f"({100 * fig['roe_sust']:.2f}%) sits below the latest reading "
                f"({100 * fig['roe_latest']:.2f}%) and the mean is the lower of the two. The "
                "expert appendix names this as that lens's most sensitive input and runs it "
                "the other way, to the earliest year; this row runs it to the most recent."),
        dict(
            name="capital spending: maintenance set equal to depreciation vs the realised "
                 "FY2023-25 net rate",
            adopted="maintenance at the depreciation rate on the opening base, plus growth "
                    "capital per station added",
            alternative="the mean realised FY2023-25 excess of capital spending over "
                        "depreciation, held through the window",
            ovr_fn=lambda: dict(_net_capex=None), patch=NET_CAPEX,
            why="The steady-state condition that a network replaces what it consumes is the "
                "standard construction and it reconciles FY2026 to the company's own "
                "guidance. It is nonetheless below what this company has actually spent: "
                "capital spending exceeded depreciation by a mean of AED "
                f"{fig['net_capex']:,.0f}mn a year across the three audited years, against "
                f"AED {fig['model_net_capex']:,.0f}mn in the model's own first forecast "
                "year."),
        dict(
            name="working capital: the related-party-inclusive cycle vs trade balances alone",
            adopted="the cycle as the audited balance sheet presents it, including balances "
                    "with related parties",
            alternative="trade balances alone",
            patch=WC_TRADE,
            why="The study publishes both cycles and says which it uses and why: the "
                "related-party presentation is the balance sheet that exists. A reader who "
                "thinks those terms would not survive an arm's-length renegotiation should "
                "use the other, which the study also says. The adopted reading is the one "
                "that releases cash."),
        dict(
            name="the minority: deducted at book vs at its share of equity value",
            adopted="the book carrying amount",
            alternative="its disclosed profit share of the equity value the model produces",
            ovr_fn=lambda: dict(_nci_share=None), patch=MINORITY_VALUE,
            why="[R-BRIDGE-01] deducts the minority at its share of value rather than at "
                "historical cost, because the model capitalises the whole of subsidiary cash "
                f"flow. On the disclosed profit share of {100 * fig['nci_share']:.4f}% that "
                f"is about AED {fig['nci_at_value']:,.0f}mn against the AED "
                f"{V['nciq_fy25']:,.1f}mn book amount deducted. The book deduction is the "
                "smaller charge and the higher value."),
        dict(
            name="leases: deducted in the bridge with right-of-use depreciation inside the "
                 "charge, vs treated as operating",
            adopted="the lease liability deducted in the bridge, the rent not added back",
            alternative="rent charged in cash operating costs, the right-of-use asset out of "
                        "the depreciable base, no lease deducted in the bridge",
            ovr_fn=lambda: dict(dep_rate=None, maint_capex_rate=None),
            patch=LEASES_OPERATING,
            why="The study names this as contested and prices only the bridge leg, at AED "
                f"{V['lease_fy25']:,.0f}mn or AED "
                f"{V['lease_fy25'] / V['shares_mn']:.2f} a share. The alternative is priced "
                "here in full, which takes three coordinated changes rather than one plus a "
                "depreciation rate re-measured excluding right-of-use assets from the "
                f"study's own committed figures ({100 * fig['dep_ex_rou']:.4f}% against the "
                f"committed {100 * V['dep_rate']:.4f}%); it is reported as a reconstruction "
                "for that reason. Mixing the two treatments would double-count, which is the "
                "study's own point."),
        dict(
            name="the bridge: the audited 31-Dec-2025 sheet vs the reviewed 30-Jun-2026 sheet",
            adopted="the audited FY2025 balance sheet",
            alternative="the reviewed 30-June-2026 balance sheet, whose income statement the "
                        "model already consumes",
            ovr_fn=lambda: dict(_nd=None, _lease=None, _nci=None), patch=BRIDGE_H126,
            why="[R-BRIDGE-01] stands the bridge on the LATEST disclosed sheet. The reviewed "
                "interim is in this study's own source set and its income statement is fully "
                "consumed while its balance sheet is not. Net debt, leases and the minority "
                "all move, and the net effect is against the study's own answer. The three "
                "figures are read from that filing by this study's own gap review of 5 "
                "September and are not committed inputs of the model, which is why this row "
                "is the one alternative below that does not come from the committed "
                "register."),
    ]


# the three the reviewer could NOT value both ways, named rather than dropped:
# an absent answer is not a clean one.
NOT_VALUED = [
    dict(name="the equity risk premium basis",
         adopted="the rating basis",
         why_not="The published country-risk file carries a rating-based row for the UAE "
                 "and no credit-default-swap-based row, so the second framing does not "
                 "exist in the original source. Constructing one from a third-party quote "
                 "that contradicts the original file would be worse than disclosing the "
                 "gap, and the study says so. Reported unvalued rather than guessed.",
         one_sided_price="the study offers a beta of 0.80 as arithmetically equivalent to a "
                         "premium about forty per cent higher, worth AED 4.25 on its own "
                         "cash-flow lens"),
    dict(name="the proposed acquisition of Shell Downstream South Africa",
         adopted="excluded from every number, and disclosed as excluded",
         why_not="Announced on 7 July 2026 at approximately USD 1,000mn of enterprise "
                 "value, after the 30 June sheet and not closed. No consideration "
                 "structure, no funding split and no acquired earnings are disclosed, so "
                 "the including framing cannot be built from the filings without inventing "
                 "its terms. The exclusion is applied consistently on both sides of the "
                 "bridge.",
         one_sided_price="none available from the disclosures"),
    dict(name="the 45 fils per litre minimum margin under the parent supply agreement",
         adopted="not carried as a driver; the retail margin per litre is built from the "
                 "disclosed gross profit and litres",
         why_not="The study's own negative-results record states that this figure — which "
                 "it calls the single most consequential structural input — was sourced "
                 "from secondary reporting of an exchange filing and never confirmed from "
                 "the primary document. The model's own realised retail margin is about 36 "
                 "fils, BELOW the quoted floor, so the two cannot be measuring the same "
                 "thing; applying the floor as a forecast level would be inventing a driver "
                 "on an unconfirmed source. Reported unvalued, and the delivered caption "
                 "that calls 36.0 'comfortably above' 45 is a separate defect already on "
                 "the study's own findings list.",
         one_sided_price="not priced; the primary source was never obtained"),
]


def build():
    live = json.load(open(NUM, encoding="utf-8"))
    base = run()
    # THE HARNESS IS PROVED AGAINST THE COMMITTED ANSWER BEFORE ANY ALTERNATIVE IS
    # BELIEVED. A re-run that does not reproduce the published number exactly is
    # measuring a different model, and every difference below would be a fiction.
    for k, got in (("centre_A", base["L"]["centre_A"]), ("centre_B", base["L"]["centre_B"])):
        assert got == live["lenses"][k], (
            "the re-run does not reproduce the committed %s (%r vs %r)"
            % (k, got, live["lenses"][k]))
    assert base["DCF"]["frame_A"]["per_share"] == live["dcf"]["frame_A"]["per_share"]

    A0 = live["lenses"]["centre_A"]
    B0 = live["lenses"]["centre_B"]
    V, H = base["V"], base["H"]

    # ---------------- the price ----------------
    struck = float(live["spot"])
    prices = json.load(open(PRICE_FILE, encoding="utf-8"))
    spot, spot_date = _latest_close(prices, live["meta"]["ticker"])

    # ---------------- the reverse read ----------------
    sys.path.insert(0, ENGINE)
    import reverse_read as RR

    W, DCF = live["wacc"], live["dcf"]
    shares = float(live["meta"]["shares_mn"])
    reads = {}
    for fr in ("frame_A", "frame_B"):
        x = DCF[fr]
        t_mid, how = RR.resolve_times({}, x["df"], W["disc_rate"])
        reads[fr] = dict(RR.read(x["fcff"], t_mid, x["tv"], W["wacc_terminal"], x["g"],
                                 x["df"][-1], x["df"][-1], x["ev"], x["equity"],
                                 shares, spot),
                         discounting_times=t_mid, times_resolved=how)
        reads[fr + "_at_strike"] = RR.read(x["fcff"], t_mid, x["tv"], W["wacc_terminal"],
                                           x["g"], x["df"][-1], x["df"][-1], x["ev"],
                                           x["equity"], shares, struck)
    r_price = reads["frame_A"]["implied_rate_at_price"]
    r_study = reads["frame_A"]["implied_rate_at_study_value"]

    # ---------------- what the price implies about the PUBLISHED answer ----------------
    # solved by re-running the whole model, because the study's published answer is a
    # weighted centre of four lenses and its own reverse valuation is solved on one of them
    g_pub = bisect(lambda x: run(dict(g_terminal=x))["L"]["centre_A"], -0.08, 0.030, spot)
    g_pub_b = bisect(lambda x: run(dict(g_terminal=x))["L"]["centre_B"], -0.08, 0.030, spot)
    g_pub_strike = bisect(lambda x: run(dict(g_terminal=x))["L"]["centre_A"],
                          -0.08, 0.030, struck)
    macro = json.load(open(os.path.join(ENGINE, "macro_paths", "AE.json"), encoding="utf-8"))
    pi_term = _terminal_inflation(macro)

    # ---------------- what the company itself has disclosed ----------------
    kd = float(W["kd_pretax"])
    kd_usd = float(W["kd_pretax_usd_basis"])
    div_yield = float(V["dps"]) / spot
    vol_retail_g = V["vol_retail_h126"] / V["vol_retail_h125"] - 1
    stations_g = V["stations_h126"] / V["stations_h125"] - 1
    lps_g = ((V["vol_retail_h126"] / V["stations_h126"])
             / (V["vol_retail_h125"] / V["stations_h125"]) - 1)
    vol_retail_g_fy25 = V["vol_retail_fy25"] / V["vol_retail_fy24"] - 1

    diag = {
        "ticker": live["meta"]["ticker"],
        "as_of": "2026-09-05",
        "spot": spot,
        "spot_date": spot_date,
        "published_central": A0,
        "published_spot": struck,
        "why_this_file": (
            "The reverse read — what the traded price must believe — is a DIAGNOSTIC and "
            "lives outside the numbers file every builder reads. A quantity solved from a "
            "price and then used anywhere in the valuation is the reverse-engineered rate "
            "the protocol prohibits outright, arriving through a side door. Nothing in this "
            "file is an input to anything: it is COMPUTED by diagnostics_adnocdist.py, no "
            "builder reads it, and this generator asserts before writing that the solved "
            "value appears nowhere in study_numbers.json."),
        "implied": {
            "quantity": ("the single flat discount rate that reproduces the traded price on "
                         "this study's own free cash flows and terminal"),
            "value": r_price,
            "value_other_framing": reads["frame_B"]["implied_rate_at_price"],
            "study_value": r_study,
            "study_value_range": [float(W["wacc"]), float(W["wacc_terminal"])],
            "study_value_range_note": (
                "the two ends are IDENTICAL because this study's schedule is flat: the "
                "cost-of-capital procedure returns a flat ladder in a pegged market, where "
                "today already is the terminal. It is recorded as a range anyway so the "
                "field means the same thing here as on a study that glides."),
            "solved_on": (
                "engine/reverse_read.py, on this study's own committed free cash flows, its "
                "own terminal cash flow recovered from its own terminal value, its own "
                "terminal growth and its own bridge — holding every driver at its published "
                "value and varying only the discount rate until the model reproduces the "
                "traded price. The discounting convention was %s, and it recovers whole "
                "years because this study discounts to year ends."
                % reads["frame_A"]["times_resolved"]),
            "reading": (
                "At AED %.2f the price is paying for a flat %.2f%% cost of capital on the "
                "same cash flows this study discounts at %.2f%%, so the market and the study "
                "disagree by about %.0f basis points on the price of time and risk rather "
                "than on the business; on the through-cycle frame the implied rate is "
                "%.2f%%. The study's own flat rate reproduces to %.4f%% against a published "
                "%.4f%%, which is the check that the two numbers are one quantity measured "
                "twice. Beside what the company itself discloses: its marginal cost of debt "
                "is %.2f%% on its own disclosed dirham margin and %.2f%% on the dollar one, "
                "and its own committed fixed dividend yields %.2f%% at this price — so the "
                "market is discounting the whole firm about %.0f basis points above the "
                "rate the company itself borrows at, against this study's %.0f."
                % (spot, 100 * r_price, 100 * r_study,
                   10000 * (r_price - r_study),
                   100 * reads["frame_B"]["implied_rate_at_price"],
                   100 * r_study, 100 * float(W["wacc"]),
                   100 * kd, 100 * kd_usd, 100 * div_yield,
                   10000 * (r_price - kd), 10000 * (r_study - kd))),
        },
        "construction": {k: v for k, v in reads["frame_A"].items()},
        "construction_frame_B": {k: v for k, v in reads["frame_B"].items()},
        "at_the_strike": {
            "spot": struck,
            "frame_A": reads["frame_A_at_strike"]["implied_rate_at_price"],
            "frame_B": reads["frame_B_at_strike"]["implied_rate_at_price"],
            "why_both": ("[R-GAP-01] as amended measures against the latest known close, and "
                         "the study was struck a month earlier; both are solved so a reader "
                         "can see how much of the disagreement is the month."),
        },
        "cross_reads": {
            "why": ("The read above is solved on the cash-flow lens, which is the "
                    "comparable construction across this book. The answer THIS study "
                    "publishes is a weighted centre of four lenses, so the same question is "
                    "solved again against the published answer by re-running the whole "
                    "model — the study's own reverse valuation is solved through revalue(), "
                    "which returns the cash-flow lens at AED %.4f rather than the published "
                    "AED %.4f, and therefore overstates the disagreement."
                    % (live["dcf"]["frame_A"]["per_share"], A0)),
            "implied_terminal_growth_on_the_published_central": g_pub,
            "implied_terminal_growth_on_the_published_central_frame_B": g_pub_b,
            "implied_terminal_growth_at_the_strike": g_pub_strike,
            "study_terminal_growth": float(V["g_terminal"]),
            "house_AE_terminal_inflation": pi_term,
            "implied_real_terminal_growth": (1 + g_pub) / (1 + pi_term) - 1,
            "study_real_terminal_growth": (1 + float(V["g_terminal"])) / (1 + pi_term) - 1,
            "the_studys_own_published_reverse_valuation": {
                "terminal_growth": live["crux"]["g_implied"],
                "terminal_discount_rate": live["crux"]["wacc_term_implied"],
                "beta": live["crux"]["beta_implied"],
                "note": ("solved at the 7 August strike of AED %.2f and against the "
                         "cash-flow lens rather than the published centre, which is why "
                         "these differ from the figures above"% struck),
            },
            "reading": (
                "Solved against the answer a reader actually receives, AED %.2f implies "
                "terminal growth of %+.3f%% nominal against this study's %.2f%% — a real "
                "decline of %.3f%% a year against the house terminal inflation of %.2f%%, "
                "where the study's own figure is a real decline of %.3f%%. Beside what the "
                "company has disclosed: retail volume grew %.1f%% in the first half of 2026 "
                "and %.1f%% in FY2025, the network grew %.1f%%, and litres per station "
                "therefore FELL %.1f%%. A market paying for a small real decline in a fuel "
                "retailer whose own throughput per site is falling is not paying for "
                "something implausible, so the disagreement is about the DEGREE of that "
                "decline rather than about whether the market has misread the "
                "business — and a reverse read landing on a believable number is "
                "evidence against a premium rather than for it."
                % (spot, 100 * g_pub, 100 * float(V["g_terminal"]),
                   -100 * ((1 + g_pub) / (1 + pi_term) - 1), 100 * pi_term,
                   -100 * ((1 + float(V["g_terminal"])) / (1 + pi_term) - 1),
                   100 * vol_retail_g, 100 * vol_retail_g_fy25, 100 * stations_g,
                   -100 * lps_g)),
        },
        "company_disclosed": {
            "marginal_cost_of_debt_dirham_margin": kd,
            "marginal_cost_of_debt_dollar_margin": kd_usd,
            "yield_on_the_committed_fixed_dividend_at_this_price": div_yield,
            "retail_volume_growth_h1_2026": vol_retail_g,
            "retail_volume_growth_fy2025": vol_retail_g_fy25,
            "network_growth_h1_2026": stations_g,
            "litres_per_station_growth_h1_2026": lps_g,
            "return_on_capital_fy2025_this_study_definition": float(H["FY2025"]["roce"]),
            "note": ("every figure here is the company's own disclosure, or an identity on "
                     "two of them, taken from this study's own four-field input register — "
                     "except the last, which is this study's own computation on its own "
                     "definition and is labelled as such. The company's own disclosed "
                     "return on capital employed of 32.7% for FY2025 and 40.1% for the "
                     "first half of 2026 sits in the study's record as evidence inside an "
                     "input's source rather than as a committed value of its own, so it is "
                     "quoted in the judgement that turns on it and not recomputed here."),
        },
    }

    # ---------------- the contested judgements ----------------
    # Every figure quoted in a reason is computed here and interpolated, never typed.
    net_capex = sum(H[y]["capex"] - (V["dep_ppe_fy%s" % y[-2:]] + V["dep_rou_fy%s" % y[-2:]]
                                     + V["amort_fy%s" % y[-2:]]) for y in base["HYRS"]) / 3
    nci_share = V["nci_fy25"] / V["np_fy25"]
    dep_ex_rou = (V["dep_ppe_fy25"] + V["amort_fy25"]) / V["ppe_fy24"]
    dA, dB = live["dcf"]["frame_A"], live["dcf"]["frame_B"]
    fig = dict(
        margin_no_step=run({}, MARGIN_NO_STEP, "no FY2026 step")["L"]["centre_A"],
        pi_term=pi_term,
        study_real_g=(1 + float(V["g_terminal"])) / (1 + pi_term) - 1,
        roe_sust=base["L"]["roe_sust"],
        roe_latest=base["L"]["roe_hist"][-1],
        payout_implied=base["L"]["pe_payout_implied"],
        inv_lens_share=abs(dA["per_share"] - dB["per_share"]) / abs(dB["per_share"]),
        net_capex=net_capex,
        model_net_capex=base["F"]["capex"][0] - base["F"]["dna"][0],
        nci_share=nci_share,
        nci_at_value=nci_share * (dA["ev"] - dA["net_debt"] - dA["leases"]),
        dep_ex_rou=dep_ex_rou,
    )
    # the reviewed 30-June-2026 balance sheet, as this study's own gap review reads it
    H126 = dict(_nd=3207.684, _lease=1472.850, _nci=201.770)

    rows = []
    for f in forks(base, fig):
        if "fixed" in f:
            alt_a, alt_b = f["fixed"], f["fixed_b"]
        else:
            ovr = dict(f.get("ovr") or {})
            if f.get("ovr_fn"):
                seed = f["ovr_fn"]()
                for k in seed:
                    ovr[k] = {"_net_capex": net_capex, "_nci_share": nci_share,
                              "dep_rate": dep_ex_rou, "maint_capex_rate": dep_ex_rou,
                              "_nd": H126["_nd"], "_lease": H126["_lease"],
                              "_nci": H126["_nci"]}[k]
            g = run(ovr, f.get("patch") or (), f["name"])
            alt_a, alt_b = g["L"]["centre_A"], g["L"]["centre_B"]
        rows.append(dict(
            name=f["name"], adopted=f["adopted"], alternative=f["alternative"],
            value_adopted=A0, value_alternative=alt_a,
            value_adopted_frame_B=B0, value_alternative_frame_B=alt_b,
            share_of_value=abs(A0 - alt_a) / abs(alt_a),
            direction=("the study adopted the higher-value framing" if A0 > alt_a
                       else "the study adopted the lower-value framing"),
            why=f["why"]))

    cj = {
        "ticker": live["meta"]["ticker"],
        "as_of": "2026-09-05",
        "published_central": A0,
        "published_spot": struck,
        "why_this_file": (
            "Any single contested choice in a valuation is defensible. What is not is a "
            "study that resolves EVERY contested choice the same way and never notices — "
            "which is how a lean survives an audit of its steps. Each is recorded with BOTH "
            "framings' values, the side adopted and why, and the binomial sign test is "
            "printed. A study landing them all one way is FLAGGED, never failed: a company "
            "can genuinely deserve a consistent read, and a gate that failed on it would "
            "push studies to resolve judgements inconsistently to stay green."),
        "both_framings_share_a_bridge": (
            "Every alternative is computed by RE-RUNNING this study's own compute.py with "
            "that one choice changed and everything else held at its published value, "
            "through the same lenses and the same bridge as the adopted figure — so the "
            "difference measures the CHOICE and not the construction. Each source "
            "substitution is asserted to have landed exactly once, and the re-run is proved "
            "against the committed answer before any alternative is believed."),
        "the_answer_this_record_is_anchored_on": (
            "This study publishes TWO branches and no single figure. Every row is valued on "
            "Frame A, the branch the shared reader resolves, with the Frame B pair recorded "
            "beside it; the two move together on every row except the inventory judgement "
            "itself, which IS the difference between the branches."),
        "materiality": (
            "A judgement is material where the two framings differ by more than 5% of "
            "value. Because the published answer is a weighted centre of four lenses, a "
            "driver change moves it LESS than it moves the cash-flow lens alone — which is "
            "a real property of the published construction and not a softening of the test; "
            "the cash-flow-lens effect is larger on every row that touches a driver."),
        "judgements": rows,
        "not_valued": NOT_VALUED,
        "not_treated_as_a_contested_judgement": [
            dict(name="beta",
                 why="It is measured, not chosen: a five-year weekly regression against the "
                     "published index of its own exchange, 257 observations, R-squared "
                     "0.179, usable on the gate, so no lower tier is reached for. The "
                     "sensitivity table shows it is the largest single driver of value, "
                     "which is a fact about the model rather than a fork the study "
                     "resolved. The record's index file is registered under a filename the "
                     "resolver does not carry, and that file is byte-identical to the one "
                     "it does — a provenance defect on the study's own findings list, not a "
                     "second framing of the number."),
            dict(name="the dividend lens, flat versus grown",
                 why="It carries no weight in either published centre, so both framings "
                     "give the identical answer. It sets the bottom of the published range "
                     "of readings and nothing else."),
        ],
    }
    return diag, cj


def _latest_close(prices, ticker):
    """The latest supplied close for this name, read where the file puts it.

    Read explicitly rather than by searching the file for a plausible number: a
    price recovered by a pattern is a price nobody can check, and an absent one
    must raise rather than fall back to the strike [R-ENF-04].
    """
    row = (prices.get("prices") or {}).get(ticker)
    assert row and isinstance(row.get("price"), (int, float)), (
        "no supplied close for %s in %s — an absent price is not a clean one"
        % (ticker, os.path.basename(PRICE_FILE)))
    return float(row["price"]), ("close %s, supplied %s (%s)"
                                 % (row.get("date"), prices.get("supplied"),
                                    os.path.basename(PRICE_FILE)))


def _terminal_inflation(macro):
    """The house AE terminal inflation, read live from the path [R-MACRO-01]."""
    v = ((macro.get("inflation") or {}).get("terminal") or {}).get("value")
    assert isinstance(v, float), ("the AE macro path exposes no terminal inflation — "
                                  "read it live, never assume it")
    return float(v)


def _assert_containment(diag):
    """THE DEVICE, CHECKED HERE AS WELL AS BY THE GATE.

    The reverse read lives outside the numbers file every builder reads. A float
    carried at full precision does not appear there by coincidence, so a hit means
    a quantity solved from the traded price is sitting where the model can reach
    it — which is the prohibition, whether or not anything currently reads it.
    """
    val = diag["implied"]["value"]
    doc = json.load(open(NUM, encoding="utf-8"))

    def hunt(node, trail=""):
        if isinstance(node, dict):
            for k, v in node.items():
                r = hunt(v, trail + "/" + str(k))
                if r:
                    return r
        elif isinstance(node, list):
            for i, v in enumerate(node):
                r = hunt(v, trail + "[%d]" % i)
                if r:
                    return r
        elif isinstance(node, float) and node == val:
            return trail
        return None

    where = hunt(doc)
    assert where is None, (
        "the reverse read's own value is committed in study_numbers.json at %s. A quantity "
        "solved from the traded price must not sit in the numbers file every builder reads."
        % where)


def main():
    diag, cj = build()
    _assert_containment(diag)
    json.dump(diag, open(os.path.join(HERE, "diagnostics.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    json.dump(cj, open(os.path.join(HERE, "contested_judgements.json"), "w",
                       encoding="utf-8"), indent=1, ensure_ascii=False)

    i = diag["implied"]
    print("ADNOCDIST reverse read at AED %.2f (%s)" % (diag["spot"], diag["spot_date"]))
    print("  the price implies a flat %.4f%%; this study discounts at %.4f%%  (%+.0f bp)"
          % (100 * i["value"], 100 * i["study_value"],
             10000 * (i["value"] - i["study_value"])))
    print("  on the published centre the price implies terminal growth of %+.4f%% "
          "against %.2f%%"
          % (100 * diag["cross_reads"]["implied_terminal_growth_on_the_published_central"],
             100 * diag["cross_reads"]["study_terminal_growth"]))
    mat = [j for j in cj["judgements"] if j["share_of_value"] >= 0.05]
    up = len([j for j in mat if j["value_adopted"] > j["value_alternative"]])
    print("  %d contested judgements, %d material at the 5%% bar, %d resolved upward"
          % (len(cj["judgements"]), len(mat), up))
    for j in mat:
        print("     %-6s %5.1f%%  %s" % ("UP" if j["value_adopted"] > j["value_alternative"]
                                         else "DOWN", 100 * j["share_of_value"],
                                         j["name"][:88]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
