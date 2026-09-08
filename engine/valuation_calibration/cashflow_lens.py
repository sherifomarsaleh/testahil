"""The mechanical fair value as a CASH-FLOW lens.  [R-VCAL-01] series (a), score (i).

The construction is fixed in MECHANICAL_LENS_3_06-09-2026.md, sealed and committed
BEFORE any figure under it was computed. It supersedes the order-book floor of
declaration 2, which was a floor on one class and could never measure a lean in
either direction; that declaration barred a third SHAPE on the same inputs and in
the same paragraph instructed the calibration to WAIT FOR THE PROJECTION TO CARRY
THE MISSING ITEMS. Capex and working capital are what it named. The valuation-input
blocks [R-FCAL-01 AMENDED] now carry them, and this is that release.

NOTHING IN THIS MODULE CHOOSES ANYTHING. It reads each run's own projection at each
origin, that name's own trailing intensities from its own committed block, the
point-in-time macro archive, the footed share count for that year, and the close on
or before that year end, and does the arithmetic the sealed declaration describes.

THREE CONSTRUCTION BIASES ARE NAMED IN THE DECLARATION AND ALL THREE RUN THE SAME
WAY AS THE HYPOTHESIS UNDER TEST — a flat crisis-level discount rate, maintenance
charged at total trailing capex, and no minority deducted (this one runs the other
way). A pooled bias is therefore NOT by itself evidence of a house lean, and
report() prices what they could account for rather than leaving it to a reader.

VERIFY BY IMPORT, NOT BY PARSE.
"""
from __future__ import annotations

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, ENGINE)
sys.path.insert(0, HERE)

import macro_history as MH       # noqa: E402
import panel as P                # noqa: E402
import terminal_value as TV      # noqa: E402

BETA = 1.00              # declaration 2, carried forward unchanged
HORIZONS = (1, 2, 3, 4, 5)
# The shortest explicit window a terminal may be built on. THREE is not chosen here: it is
# [R-FCAL-01]'s own LIGHT scope, the shortest window this house pre-registers for any run,
# so a scorer refusing it would be refusing work the method licenses. Anything shorter and
# the terminal carries the whole answer.
MIN_EXPLICIT = 3   # the sealed explicit window

# Declaration 4. Terminal growth is REAL growth on the house inflation path; a typed
# nominal rate is prohibited because nobody can tell whether it meant inflation plus a
# point or inflation minus three. Zero is the conservative standard reading and is what
# the house macro path returns for every terminal it builds. Changing it is an amendment
# to the declaration, made before the figures it affects are computed.
TERMINAL_REAL_GROWTH = 0.0
CONVERGE_PP = 0.02      # [R-MACRO-01]'s own 2pp, borrowed and never minted
STUB_CAP = 10           # a ladder that has not converged in fifteen years
                        # total is one this lens refuses, not extrapolates
INTENSITY_YEARS = 3      # median over the three fiscal years to the origin


# --------------------------------------------------------------- the tax regime
def tax_rate(tk, origin):
    """The statutory rate AS EACH RUN COMMITTED IT — never as this module decided.

    PHDC's own bottom_up.py carries the regime rule (0.225 from 2015, 0.25 before)
    and it is sourced there; EGCH's panel carries a company-specific TAX_REGIME for
    KIMA and that governs at EGCH origins, because a rate that differs is a fact
    about the company rather than a disagreement to average away.
    """
    if tk == "EGCH":
        try:
            sys.path.insert(0, os.path.join(ENGINE, "egch_walkforward"))
            import panel as EP  # noqa: F401
            r = EP.TAX_REGIME.get("FY%d" % origin)
            if isinstance(r, float):
                return r
        except Exception:
            pass
        finally:
            sys.path[:] = [p for p in sys.path
                           if p != os.path.join(ENGINE, "egch_walkforward")]
    return 0.225 if origin >= 2015 else 0.25


# --------------------------------------------------------------- the projections
# EVERY RUN IMPORTS A MODULE CALLED `panel` AND SO DOES THIS DIRECTORY. Loading a
# run's bottom_up with the calibration's own panel already in sys.modules hands it
# the wrong one, and it does not fail loudly — it fails as a missing attribute five
# frames down, which is how the first run of this module dropped all 33 cells with
# three different AttributeErrors. So the shadowed names are EVICTED around every
# load and every call, and restored afterwards.
_SHADOWED = ("panel", "macro", "corrections", "bottom_up", "labels", "parse_fs",
             "parse_kpi", "kpi_panel", "forward")
_CACHE = {}


class _Isolated:
    def __init__(self, rundir):
        self.rundir = rundir
        self.saved = {}

    def __enter__(self):
        self.cwd = os.getcwd()
        for n in _SHADOWED:
            if n in sys.modules:
                self.saved[n] = sys.modules.pop(n)
        sys.path.insert(0, self.rundir)
        os.chdir(self.rundir)
        return self

    def __exit__(self, *exc):
        os.chdir(self.cwd)
        sys.path[:] = [x for x in sys.path if x != self.rundir]
        for n in _SHADOWED:
            sys.modules.pop(n, None)
        sys.modules.update(self.saved)
        return False


def _in(rundir):
    """Import a run's bottom_up with its own directory as cwd, as its score.py does."""
    if rundir in _CACHE:
        return _CACHE[rundir]
    import importlib.util
    p = os.path.join(rundir, "bottom_up.py")
    with _Isolated(rundir):
        spec = importlib.util.spec_from_file_location(
            "bu_%s" % os.path.basename(rundir), p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
    _CACHE[rundir] = m
    return m


def _run(rundir, fn, *a, **kw):
    with _Isolated(rundir):
        return fn(*a, **kw)


def project_amoc(origin):
    d = os.path.join(ENGINE, "amoc_walkforward")
    B = _in(d)
    out = {}
    for h in HORIZONS:
        if h not in B.HORIZONS:
            continue
        p = _run(d, B.project, "FY%d" % origin, h)
        out[h] = {"revenue": p.get("net_sales"),
                  "ebit": p.get("operating_profit"),
                  "dna": p.get("depreciation")}
    return out


def project_arcc(origin, unit_fix=False):   # unit_fix in (False, True, "coherent")
    """ARCC's own projection, exactly as its run computes it.

    unit_fix IS A LABELLED SENSITIVITY AND IS NEVER THE DECLARED RUN. It exists
    because this lens INHERITS each run's projection by construction, so a unit
    error inside one run's cost path arrives here looking like a property of the
    valuation method. What it varies is named, is arithmetic rather than judgement,
    and uses NO information the origin did not have:

      (i) COAL IS A DOLLAR COMMODITY AND THE RUN HOLDS IT FLAT IN POUNDS. That
          run's own docstring states the intent correctly -- "a commodity price
          has no drift and assuming one would be a forecast, not a rule" -- and
          then applies it to coal_egp(), which is the South African dollar price
          MULTIPLIED BY the exchange rate. Holding that level flat through a
          window in which the pound fell 10.434x asserts that the dollar coal
          price fell about ninety per cent, which is not a rule about a commodity;
          it is a forecast, and an impossible one. The sensitivity holds coal flat
          IN DOLLARS and converts at the model's OWN knowable currency path -- the
          same (1 + fx_dep(o)) ** h it already applies to export prices.
      (ii) DEPRECIATION, AMORTISATION AND RIGHT-OF-USE are held at their nominal
          origin values for five years while revenue escalates at the full
          inflation ladder. The sensitivity escalates them on that same ladder.

    THIS IS NOT A PROMOTED LEVER AND MAY NOT BECOME ONE HERE. The pre-registration
    fixes six levers in order before any score existed and an input run's
    projection is not among them; adding a seventh after seeing the scores is the
    fitting this method forbids. What this measures is ATTRIBUTION -- how much of
    the pooled bias is a property of one input rather than of the valuation
    construction -- which is what the acceptance criterion's residual clause asks
    for. The remedy for a unit error is to fix the unit in the run that carries
    it, which re-scores that run's own drivers and is its own pass.
    """
    d = os.path.join(ENGINE, "arcc_walkforward")
    B = _in(d)
    out = {}
    for h in HORIZONS:
        if h not in B.HORIZONS:
            continue
        if unit_fix:
            p = _run(d, _arcc_unit_fixed, B, "FY%d" % origin, h,
                     fx_level=(unit_fix == "coherent"),
                     fx_mode=("fisher" if unit_fix == "fisher" else None))
        else:
            p = _run(d, B.project, "FY%d" % origin, h)
        ebit = (p["gross_profit"] - p["ga"] - p["provisions"] + p["reversals"]
                - p["impairments"])
        out[h] = {"revenue": p.get("revenue"), "ebit": ebit,
                  "dna": (p.get("mfg_dep") or 0.0) + (p.get("amort") or 0.0)}
    return out


US_INFLATION_LT = 0.025    # the house path's own foreign leg for the PPP relation


def _fwd_cpi(o):
    """The origin's OWN published forward inflation path, as a function of horizon.

    Point-in-time: at origin 2021 this returns 6-7% for ever because nobody then
    published anything else, and that is the honest input rather than a defect.
    Beyond the published path the last published year is held, never extrapolated.
    """
    year = int(str(o)[2:]) if str(o).startswith("FY") else int(o)
    v = MH.origin("EG", year)
    fwd = (v.extras.get("cpi_annual") or {}).get("forward_path") or {}
    if not fwd:
        raise ValueError("no published forward inflation path at origin %s" % o)
    last = float(fwd[max(fwd, key=lambda k: int(k))])

    def at(h):
        return float(fwd.get(str(year + h), last))
    return at


def _arcc_unit_fixed(B, o, h, fx_level=False, fx_mode=None):
    """ARCC's projection with the two unit errors named above corrected.

    Every line not named there is B.project()'s own arithmetic, reproduced rather
    than re-derived so the two runs differ ONLY in what this function claims to
    change. It calls B's own paths, drivers and tax rule.

    fx_level ADDS THE THIRD ERROR, WHICH IS THE SAME ERROR AS THE FIRST FACING THE
    OTHER WAY. The run's knowable path takes the origin's last realised annual
    currency move and COMPOUNDS IT for five years. Inflation is a rate and
    compounding it is right; A DEVALUATION IS A STEP. Measured against what the
    currency actually did over the same five years:

        origin FY2016   compounds x3.763    realised x1.560
        origin FY2017   compounds x17.557   realised x1.077     <- the float year
        origin FY2018   compounds x0.996    realised x1.724
        origin FY2019   compounds x0.749    realised x2.701
        origin FY2020   compounds x0.733    realised x3.124
        origin FY2023   compounds x10.434   not yet resolved

    Wrong by a factor of sixteen at FY2017 and wrong in the OPPOSITE direction at
    three consecutive origins, so it is not a bias a reader could correct for. It
    reaches the declared run through export prices, and reaches the corrected one
    through coal as well, which is why the intermediate reading over-corrects at
    exactly the two devaluation origins.

    THE TWO ERRORS ARE ONE ERROR: the level rule and the rate rule applied to the
    wrong quantities. This run's own words are "a commodity price has no drift and
    assuming one would be a forecast, not a rule" -- true, and true of a currency
    on the same reasoning, and true of a dollar commodity only IN DOLLARS. The
    coherent specification is that sentence applied consistently, and it is chosen
    on THAT argument rather than on its score. The score agrees with it, which is
    evidence and is not the reason.
    """
    a = B.actual(o)
    pi, fxm, _coal = B._paths(o, h, False, False)

    # (iv) INFLATION IS A LADDER, NOT A LEVEL — the same error a third time.
    # The run takes the origin's own realised calendar-year inflation and
    # COMPOUNDS IT FLAT for five years, so a crisis year becomes a permanent
    # rate. Measured against the ladder the archive says was PUBLISHED at that
    # very origin:
    #
    #   origin FY2017   cpi(o) 29.5% held flat -> x3.643   published ladder x1.607
    #   origin FY2023   cpi(o) 33.9% held flat -> x4.302   published ladder x2.200
    #   origin FY2019   cpi(o)  9.2% held flat -> x1.549   published ladder x1.446
    #   origin FY2021   cpi(o)  5.2% held flat -> x1.289   published ladder x1.399
    #
    # Wrong by 2.27x and 1.96x at the two crisis origins — which are this name's
    # two worst cells — and wrong the OTHER way at a calm one, so it is not a
    # bias a reader could correct for. [R-MACRO-01] is explicit that the house
    # carries a LADDER TO A TERMINAL and that a study may not carry an inflation
    # number of its own; this run carries its own, flat. The ladder used here is
    # the origin's OWN published forward path, point-in-time, read rather than
    # chosen — the same archive, the same discipline as the currency above.
    #
    # IT IS A SCALE ERROR RATHER THAN A MARGIN ONE: revenue and costs both
    # escalate on it, so the margin barely moves and the whole business is
    # over-sized, which is exactly what this book's own pooled driver census
    # already said — "the margin is roughly right and THE SCALE IS
    # SYSTEMATICALLY TOO LOW" — arriving here with the sign the other way up
    # because a walk-forward under-forecasts what a valuation over-sizes.
    if fx_mode in ("fisher", "ladder"):
        fwd = _fwd_cpi(o)
        pi = 1.0
        for k in range(1, h + 1):
            pi *= (1 + fwd(k))

    # (iii) THE CURRENCY. Three constructions, and the run's own is none of them.
    #
    # A LARGE DEVALUATION IS AN EVENT, NOT AN ANNUAL RATE. The run takes the
    # origin's last realised annual move and compounds it, which at FY2017 turns
    # the float year's 77.4% into x17.557 over five years against a realised
    # x1.077, and at three consecutive calm origins runs the OPPOSITE way. Nobody
    # forecasts a devaluation; what a house can honestly do is one of two things,
    # and BOTH are sanctioned here rather than one being picked:
    #
    #   "level"  — hold the rate where it is and re-value when a devaluation
    #              lands. This is what a great many research houses do, and it
    #              makes no claim it cannot support.
    #   "fisher" — relative purchasing-power parity: the currency drifts at the
    #              INFLATION DIFFERENTIAL, this origin's own published local path
    #              against long-run foreign inflation.
    #
    # FISHER IS THE HOUSE'S OWN RULE AND THE RUN DOES NOT FOLLOW IT. [R-MACRO-01]
    # states in the macro path's own derivation field that the forward currency
    # path is derived by relative PPP against long-run United States inflation and
    # is NEVER SET BY HAND — so the house carries one construction for its studies
    # and another inside a walk-forward, and nothing had compared them.
    if fx_mode == "fisher":
        fwd = _fwd_cpi(o)
        m = 1.0
        for k in range(1, h + 1):
            m *= (1 + fwd(k)) / (1 + US_INFLATION_LT)
        fxm = m
    elif fx_level or fx_mode == "level":
        fxm = 1.0
    pop = (1 + B.pop_growth(o)) ** h
    w = B.W_DEFAULT

    vol_local = a["vol_local"] * pop
    vol_export = a["vol_export"]
    vol_total = vol_local + vol_export
    price_local = a["price_local"] * pi
    price_export = a["price_export"] * fxm
    services = a["services"] * pi
    # (i) coal flat in DOLLARS, carried into pounds on the model's own FX path
    raw_t = a["raw_per_t"] * (w * fxm + (1 - w) * pi)
    tr_t = a["transport_per_t"] * pi
    ov_t = a["overhead_per_t"] * pi
    # (ii) the nominal capital-charge lines escalate with everything else
    mfg_dep, amort, rou = a["mfg_dep"] * pi, a["amort"] * pi, a["rou"] * pi
    ga = a["ga"] * pi

    revenue = (price_local * vol_local * 1000.0
               + price_export * vol_export * 1000.0 + services)
    raw = raw_t * vol_total * 1000.0
    transport = tr_t * vol_total * 1000.0
    overhead = ov_t * vol_total * 1000.0
    cogs = raw + transport + overhead + mfg_dep + amort + rou
    gross_profit = revenue - cogs

    pbt = (gross_profit - ga - a["provisions"] + a["reversals"] - a["impairments"]
           + a["interest_income"] + a["other_income"] - a["finance_costs"]
           + 0.0 + a["disposals"] + a["jv"])
    tax = B.TAX_RATE * pbt if pbt > 0 else 0.0
    return {"revenue": revenue, "cogs": cogs, "gross_profit": gross_profit, "ga": ga,
            "provisions": a["provisions"], "reversals": a["reversals"],
            "impairments": a["impairments"], "mfg_dep": mfg_dep, "amort": amort,
            "rou": rou, "pbt": pbt, "tax": tax, "pat": pbt - tax}


def project_egch(origin):
    d = os.path.join(ENGINE, "egch_walkforward")
    B = _in(d)
    out = {}
    for h in HORIZONS:
        if h not in B.HORIZONS:
            continue
        p = _run(d, B.project, "FY%d" % origin, h)
        need = ("cost_of_sales", "selling", "admin", "provisions", "other_bucket")
        if any(p.get(k) is None for k in need):
            out[h] = {"revenue": p.get("revenue"), "ebit": None, "dna": None}
            continue
        ebit = (p["revenue"] - p["cost_of_sales"] - p["selling"] - p["admin"]
                - p["provisions"] + p["other_bucket"])
        # EGCH is the ONE run whose projection carries no separate D&A line — its
        # depreciation sits inside cost of sales — so it takes the intensity rule,
        # named in the declaration as a per-name exception rather than a fallback.
        out[h] = {"revenue": p["revenue"], "ebit": ebit, "dna": None}
    return out


def project_phdc(origin):
    d = os.path.join(ENGINE, "phdc_walkforward")
    B = _in(d)

    def go():
        pan = B.load()
        return B.project(pan, origin, macro="as_known")
    r = _run(d, go)
    out = {}
    for h in HORIZONS:
        f = r.get(h) or {}
        gp, sga, da = f.get("is.gross_profit"), f.get("is.sga"), f.get("is.admin_depr")
        ebit = None if (gp is None or sga is None) else gp - sga - (da or 0.0)
        out[h] = {"revenue": f.get("is.revenue"), "ebit": ebit, "dna": da}
    return out


def project_tmgh(origin):
    d = os.path.join(ENGINE, "tmgh_walkforward")
    B = _in(d)

    def go():
        A, M = B.load()
        cpi, urb = B.macro_paths(M)
        return B.project(A, cpi, urb, origin, horizons=list(HORIZONS))
    res, _notes = _run(d, go)
    out = {}
    for h in HORIZONS:
        f = (res.get("projection") or {}).get(h) or {}
        gp, sga, da = f.get("gross_profit"), f.get("sga"), f.get("da")
        # THIS RUN'S PROJECTED DEPRECIATION CARRIES THE WRONG SIGN AND ITS OWN
        # SCORER HIDES IT. bottom_up fits d_rate off the panel's `da`, which is
        # stored NEGATIVE (the company's own convention), so `da = d_rate * ppe`
        # is negative and `f["da"] = -da` comes out POSITIVE — and the line below
        # it, `pbt = gross_profit + sga + da + finance_cost`, then ADDS
        # depreciation to profit instead of deducting it. The run's own score.py
        # lists `da` in MAGNITUDE and scores it on |x|, so the depreciation cells
        # are unaffected; `net_profit` is NOT in that set and is overstated by
        # twice the charge at every cell. Recorded in this run's directory and
        # fixed there as its own unit; here the MAGNITUDE is taken, which is the
        # panel's own convention and the run's own scoring convention both.
        ebit = None if gp is None else gp + (sga or 0.0) - abs(da or 0.0)
        rev = f.get("total_revenue")
        if rev is None:
            rev = sum(v for k, v in f.items()
                      if k in ("dev_revenue", "hosp_revenue", "other_revenue")
                      and isinstance(v, (int, float))) or None
        out[h] = {"revenue": rev, "ebit": ebit,
                  "dna": None if da is None else abs(da),
                  "capex": f.get("capex")}
    return out


def project_swdy(origin):
    """SWDY's own projection — the deepest statement history in the book.

    WIRED 08-09-2026 per instruction, on the principal's own reading of the
    blocked years: "Either live with it or chose another stock that has further
    back financial statements to test the framework on." AMOC is blocked at two
    revenue years the principal does not hold and no amount of work here produces
    them; SWDY commits SEVENTEEN statement years back to 2009 against AMOC's six,
    so widening the sample is a WIRING job rather than a research one — a name
    already carried through a full walk-forward and already committing the
    valuation-input block, and simply never connected to this lens.
    """
    d = os.path.join(ENGINE, "swdy_walkforward")
    B = _in(d)
    out = {}
    for h in HORIZONS:
        if h not in B.HORIZONS:
            continue
        r, _macro = _run(d, B.project, origin, h)
        rev = r.get("A_revenue")
        ebit = (r.get("A_gross_profit") - r.get("D10_sga")
                + r.get("D13_other_operating_income") - r.get("D14_other_operating_expense"))
        out[h] = {"revenue": rev, "ebit": ebit, "dna": r.get("D11_depreciation")}
    return out


PROJECTORS = {"AMOC": project_amoc, "ARCC": project_arcc, "EGCH": project_egch,
              "PHDC": project_phdc, "TMGH": project_tmgh, "SWDY": project_swdy}


# --------------------------------------------------- the as-reported actuals
REVENUE = {"AMOC": ["is.net_sales"], "ARCC": ["is.revenue"], "EGCH": ["is.revenue"],
           "PHDC": ["is.revenue"], "TMGH": ["total_revenue"],
           "SWDY": ["revenue"]}
FINANCE = {"AMOC": ["is.finance_expenses"], "ARCC": ["other.finance_costs"],
           "EGCH": ["is.debit_interest"], "PHDC": ["is.finance_cost"],
           "TMGH": ["finance_cost"],
           # SWDY's panel names this line TWO ways across its seventeen years —
           # interest_exp in the earlier ones, finance_cost in the later — and a
           # reader taking either alone finds the other half empty and reports it
           # as a run with no finance charge [L-355]. Both are named.
           "SWDY": ["finance_cost", "interest_exp"]}
MINORITY = {"AMOC": ["is.nci"], "ARCC": ["is.nci"], "EGCH": [], "PHDC": ["is.nci"],
            "TMGH": ["nci_equity"], "SWDY": ["nci", "minority"]}


# THE PANELS AND THE BLOCKS DO NOT SHARE A UNIT AND NOTHING SAID SO. Measured
# 6 September 2026: AMOC and ARCC report in EGP, EGCH in THOUSANDS, PHDC and TMGH
# in MILLIONS, while every valuation-input block is in EGP because it is copied
# off the face of the statement. A cost of debt built from a charge in millions
# over borrowings in units is wrong by a factor of a million and looks like a
# rate; it is exactly the shape [R-TERM-01]'s general lesson names — a quantity
# carrying a UNIT, where no amount of care inside the arithmetic supplies it.
#
# So the scale is MEASURED per name against a figure both records carry, NAMED
# rather than guessed for export_panels.SOURCES's reason, asserted to be a clean
# power of ten across every year where both are present, and the name is REFUSED
# where it is not. A hardcoded scale would go stale the first time a run re-exports
# its panel.
# The pair must be THE SAME QUANTITY in both records or the test measures a
# definitional difference and calls it a unit. Its first draft paired AMOC's
# cost-of-sales depreciation with the block's GROUP charge (ratio 1.05-1.17) and
# EGCH's bank borrowings alone with the block's TOTAL debt (1000-1299), and it
# REFUSED both — correctly, and the fix was to re-point it rather than widen the
# tolerance [R-COC-01].
# THE PAIR SAYS WHAT KIND OF EVIDENCE IT IS, because two different things are being asked
# of it and only one of them is about units. (keys, block_item, kind):
#
#   "identical"  — both records read THE SAME FIGURE off the same statement, so they must
#                  agree to the printing rounding as well as in scale. The tight band is
#                  real evidence here and stays exactly as it was.
#   "related"    — the two are the same QUANTITY IN THE SAME UNITS but not the same line
#                  (a total against one of its components). The scale is still measurable
#                  and the agreement is not, so requiring agreement would be testing a
#                  claim the pair never made.
#
# CORRECTED 07-09-2026 ON A MEASUREMENT. AMOC was declared to share no quantity at all, on
# the reasoning that its run exports no balance-sheet line — TRUE, and the wrong place to
# look: its panel carries cost_stack.depreciation and its block carries dep, the same
# quantity in the same units. Measured across the five shared years the ratio runs 1.0477
# to 1.1664, so the unit is unambiguously 1e0 (the next power of ten is an order away) and
# the two figures plainly differ, by 5 to 17 per cent, growing — which is exactly what a
# cost-of-sales depreciation against a total depreciation looks like. [L-355] again: the
# map was written looking for a balance-sheet line, and the answer was in a cost stack.
SCALE_PAIR = {
    "AMOC": (["cost_stack.depreciation"], "dep", "related"),
    "ARCC": (["debt.total"], "debt", "identical"),
    "EGCH": (["borrowings.bank", "borrowings.holdco", "borrowings.current"], "debt",
             "identical"),
    "PHDC": (["bs.cash"], "cash", "identical"),
    "TMGH": (["cash"], "cash", "identical"),
    # SWDY's panel is an INCOME STATEMENT and its block a BALANCE SHEET, so no
    # quantity appears in both and the identical test has nothing to compare.
    # Revenue against total assets is a RELATED pair and it pins the unit tightly:
    # 0.9887 to 1.5638 across ten shared years, nowhere near the midpoint to
    # another power of ten. A cables manufacturer turning its asset base about
    # once a year is the ordinary shape of that ratio, which is why it is stable
    # enough to measure a unit with.
    "SWDY": (["revenue"], "total_assets", "related"),
}


def _cells(rec):
    if not isinstance(rec, dict):
        return {}
    return rec.get("cells") if isinstance(rec.get("cells"), dict) else rec


def _sum_actual(panel, year, keys):
    """The SUM of named keys — a total the block carries as one line and the panel
    as several. Any key missing makes the sum unusable, never a partial total."""
    src = _cells(panel.get(year) or {})
    tot = 0.0
    for k in keys:
        v = src.get(k)
        v = v.get("value") if isinstance(v, dict) else v
        if not isinstance(v, (int, float)):
            return None
        tot += float(v)
    return tot


def actual(panel, year, keys):
    src = _cells(panel.get(year) or {})
    for k in keys:
        v = src.get(k)
        v = v.get("value") if isinstance(v, dict) else v
        if isinstance(v, (int, float)):
            return float(v)
    return None


def block(tk):
    p = os.path.join(ENGINE, "%s_walkforward" % tk.lower(), "valuation_inputs.json")
    if not os.path.exists(p):
        return {}
    try:
        doc = json.load(open(p, encoding="utf-8"))
    except Exception:
        return {}
    out = {}
    # TWO KEYS, AND READING ONLY THE FIRST WAS A READER DEFECT RATHER THAN A
    # CONSTRUCTION CHOICE [L-355]. A run's `origins` are the years it TESTED;
    # `prior_year_anchor` is a year it committed for the express purpose of
    # feeding a window that reaches back past the first origin. ARCC's own record
    # says so in its own words -- "FY2017 is NOT an origin of this run. It is
    # carried because the identity capex = dPPE + D&A needs property at two dates
    # and FY2018 is the first origin; recording it inside `origins` would misstate
    # what this run tested." The instrument read `origins` alone, found nothing
    # under the other key, and reported that as a dropped cell.
    #
    # THIS ADDS NO ORIGIN AND CANNOT: origins come from panel.build(), never from
    # this block, so an anchor year supplies trailing-window figures and is never
    # itself scored. `origins` WINS on any collision, because what a run tested is
    # what it tested.
    for source in ("prior_year_anchor", "origins"):
        for key, b in (doc.get(source) or {}).items():
            digits = "".join(c for c in str(key) if c.isdigit())
            if len(digits) != 4 or not isinstance(b, dict):
                continue
            row = {}
            for item, rec in b.items():
                if not isinstance(rec, dict) or "missing" in rec:
                    continue
                v = rec.get("value")
                if isinstance(v, (int, float)):
                    row[item] = float(v)
            out[int(digits)] = row
    return out


def panel_scale(tk, panel, blk):
    """How many panel units make one block unit. Measured, asserted, or refused."""
    pair = SCALE_PAIR.get(tk)
    if pair is None:
        return None, ("no quantity appears in both this run's panel and its "
                      "valuation-input block, so the unit cannot be measured")
    keys, item, kind = pair
    ratios = []
    for y in sorted(set(panel) & set(blk)):
        a = _sum_actual(panel, y, keys)
        b = (blk.get(y) or {}).get(item)
        if a and b and a != 0:
            ratios.append(abs(b / a))
    if not ratios:
        return None, ("no year carries both %s and the block's %s, so the unit "
                      "cannot be measured [R-ENF-04]" % (keys[0], item))
    lo, hi = min(ratios), max(ratios)
    mid = _median(ratios)
    power = round(math.log10(mid)) if mid > 0 else None
    if power is None:
        return None, "the measured unit ratio is not positive"
    scale = 10.0 ** power
    if kind == "identical":
        # 2% either side, because the two records read the same figure off the same
        # statement and any real difference is rounding in the panel's own printing.
        if not (0.98 * scale <= lo and hi <= 1.02 * scale):
            return None, ("the unit ratio is not a clean power of ten across the years "
                          "both records cover — %.6g to %.6g against 1e%d"
                          % (lo, hi, power))
        return scale, None
    # A RELATED PAIR ANSWERS THE UNIT AND NOT THE AGREEMENT, and the band for the unit is
    # DERIVED rather than chosen: sqrt(10) is the exact midpoint in log space between two
    # adjacent powers of ten, so inside it no other power is closer and the unit is
    # unambiguous, while outside it the reading is genuinely contested. That is arithmetic
    # about the question rather than a tolerance somebody picked, which is the only kind of
    # bound this house accepts. A pair that would need a wider band than this has not
    # measured a unit at all — it has found two quantities that are not comparable.
    root10 = 10.0 ** 0.5
    if not (scale / root10 < lo and hi < scale * root10):
        return None, ("a RELATED pair must still pin the unit: the ratio runs %.6g to "
                      "%.6g, which straddles the midpoint between 1e%d and its "
                      "neighbour, so no power of ten is unambiguous"
                      % (lo, hi, power))
    return scale, None


def _median(xs):
    xs = sorted(xs)
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2.0


def capex_at(blk, year, route):
    """The year's capex, disclosed or DERIVED, with the route it came by.

    [R-FCAL-01 AMENDED] states the rule this follows in its own words: capex is
    committed where the cash-flow statement discloses it and OTHERWISE DERIVED by
    the identity capex = dPPE + D&A and LABELLED as derived, because an identity is
    not an assumption and the label is what keeps the two apart. So the label is
    carried out of here beside the figure and counted in the report; a run whose
    capex is mostly derived is a different evidence base from one whose capex is
    mostly disclosed, and a reader is owed the difference.

    THE IDENTITY RUNS ON THE BASE THE DISCLOSED LINE COVERS, AND ON THIS BOOK THAT
    IS MEASURABLE RATHER THAN ARGUABLE. Where a company carries assets under
    construction as a SEPARATE balance-sheet line and its cash-flow capex line pays
    for both, an identity on property alone misses everything still being built —
    which for a developer is most of the spend. Measured on TMGH, the only run whose
    blocks carry `cip` and which carries a DISCLOSED capex at the same origin, so
    both routes can be scored against the company's own cash-flow statement: at
    FY2020 the disclosed figure is EGP 2,379.9mn, the identity on property alone
    gives 712.1 (-70.1%) and the identity on property plus construction gives 2,443.4
    (+2.7%). SO THE BASE IS TAKEN FROM THE BLOCK RATHER THAN ASSUMED: where a block
    records `cip`, it joins the property base on BOTH dates; where it does not — every
    other run in the book — nothing changes and the identity is exactly as it was.
    The label stays "derived" either way, because it is derived either way.
    """
    b = blk.get(year) or {}
    if isinstance(b.get("capex"), float):
        route[year] = "disclosed"
        return b["capex"]
    prev = blk.get(year - 1) or {}
    ppe, ppe0, dep = b.get("ppe"), prev.get("ppe"), b.get("dep")
    if all(isinstance(x, float) for x in (ppe, ppe0, dep)):
        cip, cip0 = b.get("cip"), prev.get("cip")
        if isinstance(cip, float) and isinstance(cip0, float):
            ppe, ppe0 = ppe + cip, ppe0 + cip0
        route[year] = "derived"
        return ppe - ppe0 + dep
    return None


def intensities(tk, origin, panel, blk):
    """Median capex / WC / D&A over revenue, across the three fiscal years to t.

    THREE YEARS, MEDIAN, FIXED IN THE DECLARATION. Median rather than mean because
    one exceptional year — TMGH's FY2024 capex at twenty-three times the prior
    year — would otherwise set the whole forward path. Fewer than three years of a
    required ratio DROPS the origin; it is never filled from a neighbour.

    Revenue comes from the as-reported panel and is scaled to the block's own unit
    before the ratio is taken, because the two records do not share one.
    """
    years = [origin - k for k in range(INTENSITY_YEARS)]
    cap, wc, dep = [], [], []
    amounts, route = [], {}
    scale, _why = panel_scale(tk, panel, blk)
    for y in years:
        rev = actual(panel, y, REVENUE[tk])
        b = blk.get(y) or {}
        if not rev or rev <= 0 or scale is None:
            continue
        rev *= scale
        cx = capex_at(blk, y, route)
        if cx is not None:
            cap.append(cx / rev)
            amounts.append(cx)
        if isinstance(b.get("wc"), float):
            wc.append(b["wc"] / rev)
        if isinstance(b.get("dep"), float):
            dep.append(b["dep"] / rev)
    return ({"capex": _median(cap) if len(cap) >= INTENSITY_YEARS else None,
             "wc": _median(wc) if len(wc) >= INTENSITY_YEARS else None,
             "dep": _median(dep) if len(dep) >= INTENSITY_YEARS else None,
             "capex_amount": _median(amounts) if len(amounts) >= INTENSITY_YEARS else None,
             "capex_route": dict(route)},
            {"capex": len(cap), "wc": len(wc), "dep": len(dep)})


# --------------------------------------------------------------- the discount rate
# ---------------------------------------------------------------- LEVER 1
# THE COST-OF-CAPITAL GLIDE. First of the six levers the pre-registration fixed in
# order before any score existed, and it is evaluated here as that list requires:
# ONE AT A TIME, on the current stack, promoted only while the pooled bias moves
# toward zero. Off by default, so the declared run is unchanged by its existence.
#
# The construction is [R-COC-01]'s and nothing here chooses any of it. A transition
# market does not hold a crisis rate for ever, so a single flat rate applied to five
# explicit years AND a perpetuity asserts that it does -- which that rule forbids
# outright in a delivered study, and which this lens has been doing since it was
# built. What replaces it:
#
#   rf_terminal   = terminal inflation + the real-rate convention   [R-MACRO-01]
#   ERP_terminal  = the house terminal premium
#   the glide     = the origin's OWN forward inflation path's cumulative progress
#                   from its first forecast year toward its terminal, so the
#                   front-loading is inherited from the disinflation the origin
#                   could actually see rather than being a second free parameter
#   the terminal is brought home on the SAME cumulative factor as the last explicit
#   year -- one date, one price of time
#
# POINT-IN-TIME IS PRESERVED AND THE ONE EXCEPTION IS NAMED: every rate, spread,
# premium and inflation figure comes from the archive's own record of what was
# published at that origin -- at origin 2021 that path expects 6-7% for ever,
# because nobody saw 2022 coming, and that is the honest input. The real-rate
# convention and the terminal ERP are CONVENTIONS rather than data: they are not
# forecasts of anything and no vintage of them exists to read, so the house figures
# are used at every origin and that is stated rather than left to be discovered.
GLIDE_REAL_RATE = 0.055        # the house emerging-market terminal real convention
GLIDE_ERP_TERMINAL = 0.07      # the house terminal equity risk premium


def _glide_fractions(v, origin, hs):
    """Cumulative progress of the origin's own forward inflation path, in [0, 1].

    Returns None where the path cannot support one, which is a refusal rather than
    a fallback: a glide invented where no disinflation was published would be this
    lens forecasting the recovery instead of reading it.
    """
    fwd = (v.extras.get("cpi_annual") or {}).get("forward_path") or {}
    if len(fwd) < 2:
        return None
    years = sorted(fwd, key=int)
    p0, pT = float(fwd[years[0]]), float(fwd[years[-1]])
    if abs(p0 - pT) < 1e-9:
        return {h: 1.0 for h in hs}          # already at its terminal: flat, by the path
    out = {}
    for h in hs:
        y = str(origin + h)
        x = float(fwd[y]) if y in fwd else pT
        f = (p0 - x) / (p0 - pT)
        out[h] = min(1.0, max(0.0, f))
    return out


def _dfactor(coc, h):
    """The CUMULATIVE discount factor to year h.

    [R-COC-01]: one forward rate per explicit year, compounded, and the terminal
    brought home on the SAME factor as the last explicit year -- one date, one price
    of time. Without a schedule this is the flat rate compounded, which is exactly
    what the declared run has always done, so the declared numbers do not move.
    """
    sched = coc.get("schedule")
    if not sched:
        return 1.0 / (1 + coc["wacc"]) ** h
    f = 1.0
    for k in range(1, h + 1):
        f *= (1 + sched[k])
    return 1.0 / f


def wacc_at(tk, origin, market, panel, blk, price, shares, glide=False,
            terminal_anchor=False, erp_basis=None, pit_beta=False,
            crp_lambda=None):
    v = MH.origin(market, origin)
    need = v.require("sovereign_10y", "default_spread", "erp")
    rf = need["sovereign_10y"] - need["default_spread"]

    # ---------------------------------------------------------------- LEVER 5
    # BETA SHRINKAGE. The declared run carries 1.00 everywhere, which is the FULL
    # shrinkage limit -- all prior, no own history. This moves to the name's own
    # point-in-time regression, Vasicek-shrunk toward that same prior on a weight
    # measured from the market's own cross-sectional dispersion at that origin.
    # Nothing about the strength of the pull is typed. See pit_betas.py.
    beta, beta_rec = BETA, None
    if pit_beta:
        import pit_betas as PB
        beta, beta_rec = PB.shrunk(tk, market, origin)
    ke = rf + beta * need["erp"]

    # ---------------------------------------------------------------- LEVER 3
    # THE EQUITY-RISK-PREMIUM BASIS. The archive carries both at every origin and the
    # declared run takes whichever the vintage names central — on this market, the
    # swap basis. [R-COC-01] requires BOTH to be published and one named central, and
    # it requires the OTHER half of the switch that is easy to forget: the risk-free
    # is normalised by the sovereign's own default spread, so moving to the rating
    # basis means STRIPPING THE RATING SPREAD TOO. Rating-to-rating, CDS-to-CDS —
    # mixing them counts the sovereign on two different measuring sticks, which is
    # the double-count that rule exists to stop, arriving through the side door.
    if erp_basis:
        e_alt = (v.extras.get("erp") or {}).get("erp_%s_basis" % erp_basis)
        d_alt = (v.extras.get("default_spread") or {}).get(
            "default_spread_%s_basis" % erp_basis)
        if e_alt is None or d_alt is None:
            return None, ("this origin publishes no %s-basis pair, and half a basis is "
                          "the sovereign counted on two measuring sticks" % erp_basis)
        rf = need["sovereign_10y"] - float(d_alt)
        ke = rf + beta * float(e_alt)      # `beta`, never BETA: a stacked lever must
        #                                    carry the one beneath it, and this line
        #                                    silently reset it to the constant on the
        #                                    first stacked run, which read as lever 5
        #                                    doing nothing rather than as a bug.
        need = dict(need, erp=float(e_alt), default_spread=float(d_alt))

    # ---------------------------------------------------------------- LEVER 4
    # THE COUNTRY-PREMIUM LAMBDA. [R-COC-01] states the default as 1.00 and requires
    # any other value to be a STATED judgement. The declared run does not state one
    # and is not at 1.00: it consumes a total premium that already carries the
    # source's own scaling, 1.10 to 1.50 across these vintages, silently. So this
    # rebuilds the premium at a stated lambda from the split crp_split.py recovers
    # — same basis in and out, rating-to-rating or CDS-to-CDS, so the sovereign is
    # never measured on two sticks.
    if crp_lambda is not None:
        import crp_split as CRP
        basis = erp_basis or (v.extras.get("erp") or {}).get("basis") or "cds"
        e_new, spread = CRP.erp_at(origin, crp_lambda, basis)
        if e_new is None:
            return None, ("this vintage publishes only one premium basis, so the country "
                          "premium cannot be split — one equation, two unknowns")
        rf = need["sovereign_10y"] - spread
        ke = rf + beta * e_new
        need = dict(need, erp=e_new, default_spread=spread)
    b = blk.get(origin) or {}
    debt = b.get("debt")
    if debt is None:
        return None, "the block commits no interest-bearing debt at this origin"
    fin = actual(panel, origin, FINANCE[tk])
    if fin is None:
        return None, "no finance charge in the as-reported panel at this origin"
    scale, why = panel_scale(tk, panel, blk)
    if scale is None:
        return None, why
    fin *= scale
    # [R-FCAL-01] trap (i): the charge over THE BORROWINGS THAT ACTUALLY BEAR IT.
    eff = abs(fin) / debt if debt > 0 else None
    sov = need["sovereign_10y"]
    if eff is None:
        kd, bound = sov, "no debt to bear a charge — the sovereign stands in"
    elif eff < sov:
        kd, bound = sov, "FLOORED at the sovereign (effective %.2f%%)" % (eff * 100)
    else:
        kd, bound = eff, "the company's own effective rate"
    tau = tax_rate(tk, origin)
    e = price * shares
    d = debt
    if e + d <= 0:
        return None, "no market-value weights at this origin"
    w = (e * ke + d * kd * (1 - tau)) / (e + d)
    out = {"wacc": w, "ke": ke, "kd": kd, "kd_bound": bound, "tau": tau,
           "beta": beta, "beta_record": beta_rec,
           "we": e / (e + d), "wd": d / (e + d), "rf_star": rf,
           "erp": need["erp"], "sovereign": sov, "equity_mv": e, "debt": d}

    # ---------------------------------------------------------------- LEVER 2
    # THE TERMINAL ANCHORS. Distinct from lever 1 and evaluated separately because
    # they are separate claims: the glide is about the EXPLICIT WINDOW sliding, this
    # is about what the PERPETUITY's rate is anchored to. The declared run capitalises
    # a perpetuity at the origin's own rate, so a name struck in a crisis year
    # discounts cash flows in 2040 at a 2023 emergency rate — which is the defect
    # [R-COC-01] exists to make inexpressible in a delivered study, present here.
    #
    # Anchored: rf_terminal = terminal inflation + the real-rate convention, and the
    # terminal premium is the house terminal ERP. The explicit window is UNTOUCHED,
    # which is what keeps this from being lever 1 in another costume. Where the
    # origin's own published path gives a HIGHER terminal rate than its present one,
    # the anchor is used anyway: this lever does not choose a direction, and refusing
    # the cells where it points the inconvenient way would be selecting the answer.
    if terminal_anchor and not glide:
        infl_t = terminal_inflation(market, origin)
        if infl_t is None:
            out["terminal_anchor_flat"] = "no forward inflation path published here"
        else:
            rf_t = infl_t + GLIDE_REAL_RATE
            ke_t = rf_t + beta * GLIDE_ERP_TERMINAL
            sov_t = rf_t + need["default_spread"]
            kd_t = max(kd + (sov_t - sov), sov_t)
            out["wacc_terminal"] = (e * ke_t + d * kd_t * (1 - tau)) / (e + d)
            out["rf_terminal"], out["ke_terminal"], out["kd_terminal"] = rf_t, ke_t, kd_t

    if glide:
        # A CELL THE GLIDE CANNOT BUILD IS FLAT, NOT DROPPED, AND THAT IS THE RULE'S
        # OWN LANGUAGE RATHER THAN A CONVENIENCE. [R-COC-01]: a market already at its
        # terminal "returns a FLAT schedule there and says so rather than
        # manufacturing movement the peg forbids". An origin whose own published
        # forward path shows no disinflation toward a lower terminal is, as far as
        # that origin could see, already there -- Egypt in 2019 and 2021 expected
        # 7% for ever, and nothing published then licensed a glide.
        #
        # IT IS ALSO THE ONLY HONEST WAY TO EVALUATE A LEVER: dropping the cells a
        # lever cannot build would compare a 15-cell mean against a 9-cell mean and
        # call the difference the lever, when most of it would be the sample. Every
        # flat cell carries its reason and the count is printed.
        out["glide_flat_reason"] = None
        infl_t = terminal_inflation(market, origin)
        fr = _glide_fractions(v, origin, HORIZONS) if infl_t is not None else None
        if infl_t is None:
            out["glide_flat_reason"] = "no forward inflation path published at this origin"
            return (out, None)
        if fr is None:
            out["glide_flat_reason"] = ("the origin's published forward inflation path "
                                        "carries fewer than two years")
            return (out, None)
        rf_t = infl_t + GLIDE_REAL_RATE
        ke_t = rf_t + beta * GLIDE_ERP_TERMINAL
        # THE TERMINAL SOVEREIGN, AND ITS SPREAD IS HELD RATHER THAN GLIDED. rf_t is
        # a NORMALISED rate, so the quoted terminal sovereign is rf_t plus a default
        # spread -- and a default spread is a credit judgement, not an inflation
        # quantity, so nothing in the disinflation path licenses moving it. Holding
        # it is the reading that assumes least.
        sov_t = rf_t + need["default_spread"]
        # Kd carries its own margin over the sovereign to the terminal and keeps the
        # floor [R-COC-01] states outright: a same-currency corporate cannot borrow
        # below its sovereign.
        kd_t = max(kd + (sov_t - sov), sov_t)
        sched = {h: (e * (ke + fr[h] * (ke_t - ke))
                     + d * (kd + fr[h] * (kd_t - kd)) * (1 - tau)) / (e + d)
                 for h in HORIZONS}
        w_term = (e * ke_t + d * kd_t * (1 - tau)) / (e + d)
        # [R-COC-01]'s refusal, raised as a drop rather than a warning: in a
        # TRANSITION market the terminal rate may not exceed the explicit-window
        # rate, because that asserts the economy ends worse than it starts and the
        # disinflation path this glide is built from says the opposite.
        if w_term > w:
            out["glide_flat_reason"] = (
                "the origin's own published path puts the terminal rate at %.4f against "
                "an origin rate of %.4f, so it saw no normalisation to glide toward and "
                "the schedule is flat, as it is for a market already at its terminal"
                % (w_term, w))
            return (out, None)
        out["schedule"] = sched
        out["wacc_terminal"] = w_term
        out["glide_fractions"] = fr
        out["ke_terminal"], out["kd_terminal"], out["rf_terminal"] = ke_t, kd_t, rf_t
    return (out, None)


def terminal_inflation(market, origin):
    v = MH.origin(market, origin)
    fwd = (v.extras.get("cpi_annual") or {}).get("forward_path") or {}
    last = str(origin + max(HORIZONS))
    x = fwd.get(last)
    if x is None and fwd:
        x = fwd[max(fwd, key=lambda k: int(k))]
    return None if x is None else float(x)


# --------------------------------------------------------------- one cell
def study_life(tk):
    """The useful life the name's OWN DELIVERED STUDY committed, with its source.

    NOT A LIFE THIS MODULE CHOSE, and the distinction is the whole point [R-TERM-01]:
    a life this desk picked is not a disclosed life. What is read here is the scalar
    a study already committed to its own terminal_record, sourced to an
    accounting-policies note and audited by that study's own gates. A name whose
    record carries no scalar — because its note gives a BAND, and collapsing a band
    is a judgement — returns None and is skipped, with the reason.
    """
    p = os.path.join(ENGINE, "%s_study" % tk.lower(), "study_numbers.json")
    if not os.path.exists(p):
        return None, "no delivered study to read a committed life from"
    try:
        doc = json.load(open(p, encoding="utf-8"))
    except Exception:
        return None, "the study's numbers file will not parse"
    # A study's terminal record sits at the top level on some names and under each
    # scenario on others (EGCH publishes a two-sided answer, so its record is per
    # case). Search by SHAPE and require every occurrence to agree — a name whose
    # cases disagree about the LIFE has not disclosed one thing, and taking the
    # first would be picking.
    found = {}

    def walk(o):
        if isinstance(o, dict):
            if "useful_life_years" in o and "useful_life_source" in o:
                v, sc = o.get("useful_life_years"), o.get("useful_life_source")
                if isinstance(v, (int, float)):
                    found[round(float(v), 6)] = sc or ""
                return
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(doc)
    if len(found) > 1:
        return None, ("the study commits %d different lives across its cases (%s) — "
                      "taking one would be picking"
                      % (len(found), ", ".join("%.4g" % k for k in sorted(found))))
    rec = {}
    if found:
        k = next(iter(found))
        rec = {"useful_life_years": k, "useful_life_source": found[k]}
    life, src = rec.get("useful_life_years"), rec.get("useful_life_source") or ""
    if not isinstance(life, (int, float)) or life <= 0:
        return None, "the study commits no scalar useful life"
    if not src:
        return None, ("the study commits a life with no source — SIGCM clause 1, and "
                      "a life with no note behind it is one somebody chose")
    return float(life), src


def cell(tk, origin, market, cellinfo, horizons=HORIZONS, maintenance="amount",
         arcc_unit_fix=False, glide=False, terminal_anchor=False, erp_basis=None,
         pit_beta=False, crp_lambda=None):
    panel, _src = P._panel(os.path.join(ENGINE, "%s_walkforward" % tk.lower()))
    blk = block(tk)
    shares, price = cellinfo["shares"], cellinfo["price"]

    # A RUN IS SCORED OVER THE WINDOW ITS OWN PRE-REGISTRATION DECLARES, NOT OVER ONE THIS
    # SCORER IMPOSES. Corrected 07-09-2026 on a measurement, and the correction is the
    # opposite of the obvious one: AMOC dropped ALL THREE of its origins because "the
    # projection runs to horizon 3; the declared window is 5", which reads like a defect
    # in AMOC and is not. [R-FCAL-01] sets scope BY SOURCEABLE HISTORY — FULL at eight or
    # more fiscal years with horizons 1-5, LIGHT at five to seven with horizons 1-3 — and
    # AMOC's run declares HORIZONS = [1, 2, 3] because it is a LIGHT-scope name. Extending
    # its projector to five would be overriding a pre-registered scope to make a cell
    # score, which is the selection this method forbids everywhere else.
    #
    # SO THE WINDOW IS THE INTERSECTION, AND ITS LENGTH IS RECORDED ON EVERY CELL. A cell
    # built on three explicit years is not like-for-like with one built on five, and the
    # honest handling is the one [R-FCAL-01] already uses for the driver scores: carry the
    # scope with the figure so a pooled result can be read BY WINDOW rather than silently
    # mixing two of them. A run whose projection reaches fewer than MIN_EXPLICIT years is
    # still refused, because a terminal capitalising a one- or two-year path is a terminal
    # doing all the work.
    # arcc_unit_fix reaches ONE projector and defaults off, so the declared run
    # is byte-identical to what it was before this sensitivity existed.
    proj = (PROJECTORS[tk](origin, unit_fix=arcc_unit_fix)
            if (arcc_unit_fix and tk == "ARCC") else PROJECTORS[tk](origin))
    hs = [h for h in horizons if h in proj]
    if len(hs) < MIN_EXPLICIT:
        return None, ("the projection runs to horizon %d and %d explicit years is the "
                      "floor for a terminal to stand on"
                      % (max(proj) if proj else 0, MIN_EXPLICIT))
    for h in hs:
        if proj[h].get("revenue") is None or proj[h].get("ebit") is None:
            return None, "the projection has no revenue or operating profit at h=%d" % h

    scale, why = panel_scale(tk, panel, blk)
    if scale is None:
        return None, why

    it, counts = intensities(tk, origin, panel, blk)
    if it["capex"] is None:
        return None, ("capex intensity needs %d years and the block carries %d"
                      % (INTENSITY_YEARS, counts["capex"]))
    if it["wc"] is None:
        return None, ("working-capital intensity needs %d years and the block "
                      "carries %d" % (INTENSITY_YEARS, counts["wc"]))
    need_dep = any(proj[h].get("dna") is None for h in hs)
    if need_dep and it["dep"] is None:
        return None, ("this run projects no D&A and the block carries %d of %d "
                      "years for the intensity rule" % (counts["dep"], INTENSITY_YEARS))

    coc, why = wacc_at(tk, origin, market, panel, blk, price, shares, glide=glide,
                       terminal_anchor=terminal_anchor, erp_basis=erp_basis,
                       pit_beta=pit_beta, crp_lambda=crp_lambda)
    if coc is None:
        return None, why
    infl = terminal_inflation(market, origin)
    if infl is None:
        return None, "the archive carries no forward inflation at this origin"

    b0 = blk.get(origin) or {}
    wc_prev = b0.get("wc")
    if wc_prev is None:
        return None, "the block commits no working capital at the origin itself"
    cash, debt = b0.get("cash"), b0.get("debt")
    if cash is None:
        return None, "the block commits no cash at the origin itself"

    tau = coc["tau"]
    rows, pv = [], 0.0
    last = None
    for h in hs:
        # THE PROJECTION SPEAKS ITS RUN'S UNIT AND THE BLOCK SPEAKS EGP. Every
        # forward figure is converted once, here, before it meets a block figure.
        rev = proj[h]["revenue"] * scale
        ebit = proj[h]["ebit"] * scale
        dna = proj[h].get("dna")
        dna = it["dep"] * rev if dna is None else dna * scale
        capex = proj[h].get("capex")
        capex = it["capex"] * rev if capex is None else capex * scale
        wc_h = it["wc"] * rev
        dwc = wc_h - wc_prev
        wc_prev = wc_h
        nopat = ebit * (1 - tau)
        fcff = nopat + dna - capex - dwc
        df = _dfactor(coc, h)
        pv += fcff * df
        rows.append({"h": h, "revenue": rev, "ebit": ebit, "nopat": nopat,
                     "dna": dna, "capex": capex, "wc": wc_h, "dwc": dwc,
                     "fcff": fcff, "df": df})
        last = rows[-1]

    # ---- DECLARATION 4: the terminal is a growing perpetuity on the last explicit
    # year's free cash flow. MECHANICAL_LENS_4_08-09-2026.md, sealed and committed
    # before this code path produced a single figure.
    #
    #     TV = FCF_N x (1 + g) / (WACC_term - g),   g = terminal inflation + real
    #
    # FCF_N is `last["fcff"]` — the same figure the explicit window discounts, taken
    # without adjustment. It already contains that year's capital spending and
    # working-capital movement, which is why no separate maintenance, growth-capital
    # or working-capital charge appears here and why no useful life is read.
    #
    # REAL GROWTH IS ZERO AND STATED, never a typed nominal rate: against a sourced
    # terminal inflation of 7% a typed 5% is a permanent real decline of about 1.9%
    # a year, and the growth rate and the discount rate must answer to the same
    # sourced path or they drift apart. Changing it is an amendment to the
    # declaration, made before the figures it affects exist.
    if maintenance == "gordon":
        g = infl + TERMINAL_REAL_GROWTH
        w_term = coc.get("wacc_terminal") or coc["wacc"]
        if g >= w_term:
            return None, ("terminal refused: growth %.4f is not below the terminal "
                          "rate %.4f, so the perpetuity does not converge" % (g, w_term))
        if last["fcff"] <= 0:
            return None, ("terminal refused: the last explicit year's free cash flow "
                          "is %s, not positive: a company consuming cash in its final "
                          "forecast year is not capitalised as a growing perpetuity"
                          % f"{last['fcff']:,.1f}")
        # DECLARATION 5 — THE TERMINAL CONVERGES BEFORE IT CAPITALISES.
        # [R-MACRO-01]: the explicit window runs until growth is within 2pp of
        # terminal, and eleven of seventeen scoring cells broke it, two by more
        # than twenty points. The window is NOT lengthened — every run declares
        # its own horizons and extending a projector to make a cell score is the
        # selection this method forbids — so the convergence happens here, on the
        # ORIGIN'S OWN PUBLISHED inflation ladder, read rather than chosen.
        # Where that ladder already sits at terminal the stub is EMPTY and this
        # collapses to declaration 4 exactly.
        cf, N = last["fcff"], max(hs)
        pv_stub, k = 0.0, 0
        try:
            fwd = _fwd_cpi(origin)
        except Exception:
            fwd = None
        if fwd is not None:
            while k < STUB_CAP:
                gk = fwd(N + k + 1)
                if gk - g <= CONVERGE_PP:
                    break
                k += 1
                cf = cf * (1 + gk)
                pv_stub += cf * _dfactor(coc, N + k)
            else:
                return None, ("terminal refused: the origin's own published inflation "
                              "path has not converged to within %.0fpp of terminal "
                              "after %d further years, and this lens extrapolates no "
                              "path it was not given" % (100 * CONVERGE_PP, STUB_CAP))
        if cf <= 0:
            return None, ("terminal refused: the converged year's free cash flow is "
                          "%s, not positive" % f"{cf:,.1f}")
        tv = cf * (1 + g) / (w_term - g)
        pv_tv = tv * _dfactor(coc, N + k)
        ev = pv + pv_stub + pv_tv
        equity = ev + cash - (debt or 0.0)
        per_share = equity / shares
        # A NEGATIVE EQUITY VALUE IS A REAL OUTPUT AND IS NOT A SCOREABLE ONE, and the
        # difference matters because of how it fails: this series is scored on
        # log(FV/P), which does not exist below zero, so the cell arrived carrying a
        # null that the scorer rendered as +0.0000 — A COMPANY VALUED AT MINUS 0.557
        # ENTERING THE POOLED MEAN AS PERFECT AGREEMENT WITH ITS PRICE. That is the
        # absent answer in a clean answer's clothes, and it is refused at the source
        # rather than filtered downstream, because a downstream filter is one somebody
        # later forgets. Declaration 4 is amended to carry this refusal; the amendment
        # EXCLUDES a cell rather than admitting one and is forced by arithmetic rather
        # than chosen after seeing a result.
        if per_share <= 0:
            return None, ("terminal refused: equity value is %s per share, not "
                          "positive: a log ratio against the price does not exist "
                          "below zero and this series is scored on one"
                          % f"{per_share:,.3f}")
        # THE EXPLICIT WINDOW MUST CARRY A POSITIVE PRESENT VALUE, and this
        # refusal is added 08-09-2026 knowing exactly what it costs, which is
        # the only reason it can be trusted.
        #
        # A cell whose five discounted forecast years sum to a NEGATIVE present
        # value larger than the terminal is not a cheap company; it is a
        # construction that has broken. Its terminal share prints as a negative
        # percentage — on the cell that provoked this, MINUS 280% — which is not
        # a share of anything, and the value it lands on (0.077 against a traded
        # 9.81) is arithmetic rather than a reading.
        #
        # WHY IT IS NOT RESULTS-SHOPPING, STATED SO A READER CAN CHECK RATHER
        # THAN TRUST: this refusal makes the answer WORSE. With that one cell in,
        # the pooled bias is +0.3692 and every bootstrap interval INCLUDES ZERO,
        # which is criterion 3's clause A passing; with it refused the bias is
        # +0.6175 and every interval EXCLUDES zero, which is clause A failing.
        # A test that passes only because one cell of twenty-two returned a
        # figure its own construction cannot support has not been passed, and
        # reporting it as passed is the exact failure this whole programme was
        # called to prevent. The refusal is placed at the SOURCE for the reason
        # the one above it is: a downstream filter is one somebody later forgets.
        if pv <= 0:
            return None, ("terminal refused: the explicit window's present value "
                          "is %s, not positive — the discounted forecast years "
                          "destroy more than the whole enterprise is worth, so the "
                          "terminal is carrying more than all of the value and its "
                          "share prints negative. That is a broken construction "
                          "rather than a cheap company." % f"{pv:,.0f}")
        return ({"ticker": tk, "origin": origin, "fv": per_share, "price": price,
                 "log": math.log(per_share / price) if per_share > 0 and price > 0 else None,
                 "equity": equity, "ev": ev, "pv_explicit": pv, "pv_terminal": pv_tv,
                 "terminal_share": (pv_tv / ev) if ev else None,
                 "cash": cash, "debt": debt, "shares": shares,
                 "wacc": coc["wacc"], "wacc_terminal": w_term,
                 "terminal_growth": g, "terminal_real_growth": TERMINAL_REAL_GROWTH,
                 "terminal_basis": "gordon_on_last_fcff",
                 "declaration": "MECHANICAL_LENS_4_08-09-2026",
                 "ke": coc["ke"], "kd": coc["kd"], "kd_bound": coc["kd_bound"],
                 "we": coc["we"], "tau": tau, "inflation": infl, "rows": rows,
                 "price_date": cellinfo["price_date"], "scale": scale,
                 "maintenance": None, "maintenance_basis_reading": maintenance,
                 "useful_life_years": None,
                 "intensities": it, "capex_route": it["capex_route"],
                 "minority_book": actual(panel, origin, MINORITY[tk]),
                 "horizons": hs}, None)

    # THE TERMINAL, only through the sanctioned module.
    #
    # "the trailing median capex of section 2 escalated to the last explicit year
    # on that same known inflation path" reads two ways and BOTH ARE PUBLISHED
    # rather than one being chosen: the median trailing capex AMOUNT escalated
    # (`amount`), which is the literal reading and the module's own last-explicit-
    # year basis; and the intensity applied to the ORIGIN's revenue and escalated
    # (`intensity`), which is what section 2's rule produces at h=0. They differ
    # under inflation because the older years in the window are smaller in nominal
    # terms. The declared run is `amount`; the other is reported beside it.
    esc = (1 + infl) ** max(hs)
    maint_amount = (it["capex_amount"] or 0.0) * esc
    maint_intensity = it["capex"] * actual(panel, origin, REVENUE[tk]) * scale * esc
    maint = maint_intensity if maintenance == "intensity" else maint_amount
    life, life_src = (None, "")
    if maintenance == "disclosed_life":
        life, life_src = study_life(tk)
        if life is None:
            return None, "disclosed-life sensitivity: %s" % life_src
    ti = dict(nopat=last["nopat"], wacc=coc["wacc"], inflation=infl, real_growth=0.0,
              dna_book=last["dna"], working_capital=last["wc"])
    if maintenance == "disclosed_life":
        # The module's own CROSS-CHECK basis: the book charge escalated to current cost
        # over half the disclosed life, which is the age of the base under straight-line
        # when the measured age is not to hand. It needs no replacement-cost capital, so
        # it is computable from what these runs commit — which the disclosed_life basis
        # proper is not, since ic_replacement exists at no past origin.
        ti.update(maintenance_basis="book_dna_escalated", useful_life_years=life,
                  useful_life_source=life_src)
    else:
        ti.update(maintenance_basis="disclosed_capex", maintenance_capex=maint)
    try:
        # TERMINAL-BASIS-EXCEPTION: ti is assembled above with nopat=last["nopat"],
        # the LAST EXPLICIT YEAR and not grown. The splat is why no expression is
        # visible at this line; the basis is set where the mapping is built.
        t = TV.build(TV.TerminalInputs(**ti))
    except TV.TerminalRefused as exc:
        return None, "terminal refused: %s" % str(exc)[:120]

    pv_tv = t.tv * _dfactor(coc, max(hs))
    ev = pv + pv_tv
    equity = ev + cash - (debt or 0.0)
    per_share = equity / shares
    return ({"ticker": tk, "origin": origin, "fv": per_share, "price": price,
             "log": math.log(per_share / price) if per_share > 0 and price > 0 else None,
             "equity": equity, "ev": ev, "pv_explicit": pv, "pv_terminal": pv_tv,
             "terminal_share": pv_tv / ev if ev else None,
             "cash": cash, "debt": debt or 0.0, "shares": shares,
             "wacc": coc["wacc"], "ke": coc["ke"], "kd": coc["kd"],
             "kd_bound": coc["kd_bound"], "we": coc["we"], "tau": tau,
             "inflation": infl, "intensities": it, "rows": rows,
             "price_date": cellinfo["price_date"], "scale": scale,
             "maintenance": t.maintenance, "maintenance_basis_reading": maintenance,
             "useful_life_years": life,
             "capex_route": it["capex_route"],
             "minority_book": actual(panel, origin, MINORITY[tk]),
             "horizons": hs}, None)


def run(market="EG", horizons=HORIZONS, maintenance="amount",
        arcc_unit_fix=False, glide=False, terminal_anchor=False, erp_basis=None,
        pit_beta=False, crp_lambda=None):
    cells, names, declared, usable = P.build(market)
    rows, dropped = [], []
    for (tk, y), c in sorted(cells.items()):
        if not c["ready"]:
            continue
        if tk not in PROJECTORS:
            dropped.append((tk, y, "no projector wired for this name"))
            continue
        try:
            r, why = cell(tk, y, market, c, horizons=horizons,
                          maintenance=maintenance, arcc_unit_fix=arcc_unit_fix,
                          glide=glide, terminal_anchor=terminal_anchor,
                          erp_basis=erp_basis, pit_beta=pit_beta,
                          crp_lambda=crp_lambda)
        except MH.VintageMissing as exc:
            r, why = None, str(exc)[:100]
        except Exception as exc:
            r, why = None, "%s: %s" % (type(exc).__name__, str(exc)[:90])
        if r is None:
            dropped.append((tk, y, why))
        else:
            rows.append(r)
    return rows, dropped


if __name__ == "__main__":
    hs = HORIZONS
    if "--own-horizons" in sys.argv:
        hs = None
    rows, dropped = run(horizons=hs or HORIZONS)
    print("cash-flow lens — %d cell(s), %d dropped" % (len(rows), len(dropped)))
    for r in rows:
        print("  %-6s %d  fv %10.3f  px %9.3f  %+7.1f%%  wacc %5.2f%%  tv %4.0f%%"
              % (r["ticker"], r["origin"], r["fv"], r["price"],
                 (r["fv"] / r["price"] - 1) * 100, r["wacc"] * 100,
                 100 * (r["terminal_share"] or 0)))
    for tk, y, why in dropped:
        print("  DROP %-6s %d  %s" % (tk, y, why))
