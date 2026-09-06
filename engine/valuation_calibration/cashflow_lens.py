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
HORIZONS = (1, 2, 3, 4, 5)   # the sealed explicit window
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


def project_arcc(origin):
    d = os.path.join(ENGINE, "arcc_walkforward")
    B = _in(d)
    out = {}
    for h in HORIZONS:
        if h not in B.HORIZONS:
            continue
        p = _run(d, B.project, "FY%d" % origin, h)
        ebit = (p["gross_profit"] - p["ga"] - p["provisions"] + p["reversals"]
                - p["impairments"])
        out[h] = {"revenue": p.get("revenue"), "ebit": ebit,
                  "dna": (p.get("mfg_dep") or 0.0) + (p.get("amort") or 0.0)}
    return out


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


PROJECTORS = {"AMOC": project_amoc, "ARCC": project_arcc, "EGCH": project_egch,
              "PHDC": project_phdc, "TMGH": project_tmgh}


# --------------------------------------------------- the as-reported actuals
REVENUE = {"AMOC": ["is.net_sales"], "ARCC": ["is.revenue"], "EGCH": ["is.revenue"],
           "PHDC": ["is.revenue"], "TMGH": ["total_revenue"]}
FINANCE = {"AMOC": ["is.finance_expenses"], "ARCC": ["other.finance_costs"],
           "EGCH": ["is.debit_interest"], "PHDC": ["is.finance_cost"],
           "TMGH": ["finance_cost"]}
MINORITY = {"AMOC": ["is.nci"], "ARCC": ["is.nci"], "EGCH": [], "PHDC": ["is.nci"],
            "TMGH": ["nci_equity"]}


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
SCALE_PAIR = {
    # AMOC's panel is an income statement and a cost stack; its run exports no
    # balance-sheet line, so NO quantity appears in both records and the unit
    # cannot be measured. Declared unavailable rather than guessed. AMOC drops on
    # the horizon clause first — its run projects three years against a declared
    # window of five — so this costs no cell, and recording it is what keeps the
    # second reason from disappearing behind the first.
    "AMOC": None,
    "ARCC": (["debt.total"], "debt"),
    "EGCH": (["borrowings.bank", "borrowings.holdco", "borrowings.current"], "debt"),
    "PHDC": (["bs.cash"], "cash"),
    "TMGH": (["cash"], "cash"),
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
    for key, b in (doc.get("origins") or {}).items():
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
    keys, item = pair
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
    # 2% either side, because the two records read the same figure off the same
    # statement and any real difference is rounding in the panel's own printing.
    if not (0.98 * scale <= lo and hi <= 1.02 * scale):
        return None, ("the unit ratio is not a clean power of ten across the years "
                      "both records cover — %.6g to %.6g against 1e%d" % (lo, hi, power))
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
    """
    b = blk.get(year) or {}
    if isinstance(b.get("capex"), float):
        route[year] = "disclosed"
        return b["capex"]
    prev = blk.get(year - 1) or {}
    ppe, ppe0, dep = b.get("ppe"), prev.get("ppe"), b.get("dep")
    if all(isinstance(x, float) for x in (ppe, ppe0, dep)):
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
def wacc_at(tk, origin, market, panel, blk, price, shares):
    v = MH.origin(market, origin)
    need = v.require("sovereign_10y", "default_spread", "erp")
    rf = need["sovereign_10y"] - need["default_spread"]
    ke = rf + BETA * need["erp"]
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
    return ({"wacc": w, "ke": ke, "kd": kd, "kd_bound": bound, "tau": tau,
             "we": e / (e + d), "wd": d / (e + d), "rf_star": rf,
             "erp": need["erp"], "sovereign": sov, "equity_mv": e, "debt": d}, None)


def terminal_inflation(market, origin):
    v = MH.origin(market, origin)
    fwd = (v.extras.get("cpi_annual") or {}).get("forward_path") or {}
    last = str(origin + max(HORIZONS))
    x = fwd.get(last)
    if x is None and fwd:
        x = fwd[max(fwd, key=lambda k: int(k))]
    return None if x is None else float(x)


# --------------------------------------------------------------- one cell
def cell(tk, origin, market, cellinfo, horizons=HORIZONS, maintenance="amount"):
    panel, _src = P._panel(os.path.join(ENGINE, "%s_walkforward" % tk.lower()))
    blk = block(tk)
    shares, price = cellinfo["shares"], cellinfo["price"]

    proj = PROJECTORS[tk](origin)
    hs = [h for h in horizons if h in proj]
    if len(hs) < len(horizons):
        return None, ("the projection runs to horizon %d; the declared window is %d"
                      % (max(proj) if proj else 0, max(horizons)))
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

    coc, why = wacc_at(tk, origin, market, panel, blk, price, shares)
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
        df = 1.0 / (1 + coc["wacc"]) ** h
        pv += fcff * df
        rows.append({"h": h, "revenue": rev, "ebit": ebit, "nopat": nopat,
                     "dna": dna, "capex": capex, "wc": wc_h, "dwc": dwc,
                     "fcff": fcff, "df": df})
        last = rows[-1]

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
    try:
        t = TV.build(TV.TerminalInputs(
            nopat=last["nopat"], wacc=coc["wacc"], inflation=infl, real_growth=0.0,
            dna_book=last["dna"],
            maintenance_basis="disclosed_capex",
            maintenance_capex=maint,
            working_capital=last["wc"]))
    except TV.TerminalRefused as exc:
        return None, "terminal refused: %s" % str(exc)[:120]

    pv_tv = t.tv / (1 + coc["wacc"]) ** max(hs)
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
             "maintenance": maint, "maintenance_basis_reading": maintenance,
             "capex_route": it["capex_route"],
             "minority_book": actual(panel, origin, MINORITY[tk]),
             "horizons": hs}, None)


def run(market="EG", horizons=HORIZONS, maintenance="amount"):
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
                          maintenance=maintenance)
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
