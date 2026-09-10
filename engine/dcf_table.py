"""THE DCF VALUATION TABLE, THE WAY A SELL-SIDE READER EXPECTS TO SEE IT  [R-DCF-01]

The failure, 10-Sep-2026. The principal put an EFG Hermes valuation page for Edita
beside one of our studies and asked where our equivalent was. It did not exist. Our
studies carried every one of these numbers -- the forecast waterfall, the discount
factors, the terminal, the enterprise-to-equity bridge -- spread across a cash-flow
section, a terminal section, a bridge paragraph and an appendix, each correct and
none of them the ONE TABLE a reader opens the document to find. A number that is
present in four places and assembled in none is, to the person reading, absent.

WHAT THIS IS NOT. It is not a new calculation and it must never become one. Every
line here is read from the study's own committed numbers file; this module owns no
arithmetic beyond summing what it was handed and asserting that the sum reproduces
the study's own published value per share. If it disagrees with the study, the study
is right and this table is broken -- which is why the reconciliation is an assert
rather than a note.

    from dcf_table import dcf_table
    rows, rec = dcf_table(numbers)      # rows: list[list[str]], rec: the audit trail
"""
from __future__ import annotations


class DCFTableError(RuntimeError):
    """The numbers file does not carry what a valuation table needs."""


# The line order a reader expects, and the key each line is read from. NOTHING is
# computed here that the study did not already publish.
WATERFALL = (
    ("Revenue",                      "rev",     1),
    ("EBITDA",                       "ebitda",  1),
    ("Less: cash taxes",             "tax",    -1),
    ("Less: capital expenditure",    "capex",  -1),
    ("Less: investment in working capital", "dnwc", -1),
    ("Add: depreciation & amortisation", "dna", 1),
)


def _years(f):
    y = f.get("years")
    if not y:
        raise DCFTableError("the forecast block carries no year labels")
    return [str(v) for v in y]


def _series(f, key, n):
    v = f.get(key)
    if v is None:
        return None
    if not isinstance(v, (list, tuple)) or len(v) < n:
        raise DCFTableError("forecast series %r is not a %d-year list" % (key, n))
    return list(v)[:n]


# THE CONTRACT. A study supplies these, and where its own numbers file names them
# differently it SAYS SO by passing `blocks`/`fields` from its own builder. The
# mapping is declared by the study, never guessed here: a shared module that
# pattern-matches nine private shapes is nine silent assumptions wearing one name,
# and the first time a study renames a key the table would quietly print a
# different company's kind of number.
CONTRACT = dict(
    blocks=("fcst", "dcf"),
    forecast_required=("years", "rev", "ebitda", "capex", "dnwc", "dna", "fcff"),
    forecast_optional=("tax", "df", "pv", "fwd_wacc"),
    bridge_required=("pv_explicit", "tv", "pv_tv", "ev", "nd", "eq_attr", "ps"),
    bridge_optional=("tv_share", "assoc", "nci_val", "emp_val", "shares", "ps_dec"),
)


def probe(numbers, blocks=None):
    """What this study already carries against the contract, and what it is missing.

    A study that cannot render the table is not a study without a valuation — it is
    a study whose valuation is spread across privately-named keys. This makes that
    difference COUNTABLE rather than a vague backlog: it returns the list of keys a
    person has to publish, per study, so the remaining work is a number.

    NOT EVERY CLASS OWES THIS TABLE. The contract describes a cash-flow lens, and
    the class primary is not a cash-flow lens everywhere — a bank is valued on
    equity flows and a holdco on a sum of its parts [R-LENS-03]. A bank probing as
    "missing a forecast block" is not a defect in the bank; it is this probe being
    asked a question about a lens the study does not run. Read the missing list
    against LENS_REGISTRY before calling any of it work.
    """
    fb, db = blocks or CONTRACT["blocks"]
    f, d = numbers.get(fb) or {}, numbers.get(db) or {}
    miss_f = [k for k in CONTRACT["forecast_required"] if k not in f]
    miss_d = [k for k in CONTRACT["bridge_required"] if k not in d]
    return dict(forecast_block=fb, bridge_block=db,
                forecast_present=bool(f), bridge_present=bool(d),
                missing_forecast=miss_f, missing_bridge=miss_d,
                renders=not (miss_f or miss_d),
                missing_total=len(miss_f) + len(miss_d))


def dcf_table(numbers, currency="EGP", unit="mn", per_share_dp=2, blocks=None,
              fields=None):
    """(rows, record) -- the valuation table, read from a study's numbers file.

    `numbers` is the parsed study_numbers.json. Returns rows ready for a document
    table (first row is the header) and a record carrying the reconciliation so a
    gate can check the table against the study without re-reading the document.
    """
    fb, db = blocks or CONTRACT["blocks"]
    alias = dict(fields or {})

    def K(name):
        """The key THIS study uses for a contract field."""
        return alias.get(name, name)

    f = numbers.get(fb) or {}
    d = numbers.get(db) or {}
    w = numbers.get("wacc") or numbers.get("cost_of_capital_record") or {}
    f = {k: f[K(k)] for k in set(list(CONTRACT["forecast_required"])
                                 + list(CONTRACT["forecast_optional"]))
         if K(k) in f}
    d = {k: d[K(k)] for k in set(list(CONTRACT["bridge_required"])
                                 + list(CONTRACT["bridge_optional"]))
         if K(k) in d}
    if not f or not d:
        raise DCFTableError("the numbers file carries no fcst/dcf block; this table is "
                            "read from the study, never recomputed")
    yrs = _years(f)
    n = len(yrs)

    def fmt(x, dp=0):
        return ("{:,.%df}" % dp).format(x)

    rows = [["%s %s" % (currency, unit)] + yrs]
    for label, key, sign in WATERFALL:
        s = _series(f, key, n)
        if s is None:
            continue
        rows.append([label] + [fmt(sign * v) for v in s])

    fcff = _series(f, "fcff", n)
    if fcff is None:
        raise DCFTableError("no fcff series: a DCF table without free cash flow is not one")
    rows.append(["Free cash flow to the firm"] + [fmt(v) for v in fcff])

    fwd = _series(f, "fwd_wacc", n)
    if fwd is not None:
        rows.append(["Discount rate for the year"] + ["{:.2%}".format(v) for v in fwd])
    df = _series(f, "df", n)
    if df is not None:
        rows.append(["Discount factor"] + ["{:.4f}".format(v) for v in df])
    pv = _series(f, "pv", n)
    if pv is not None:
        rows.append(["Present value of free cash flow"] + [fmt(v) for v in pv])

    # ---- the bridge, one line at a time -----------------------------------
    blank = [""] * n

    def one(label, value, dp=0, pct=False):
        cell = "{:.2%}".format(value) if pct else fmt(value, dp)
        rows.append([label] + blank[:-1] + [cell])

    one("Sum of present values, explicit window", d["pv_explicit"])
    one("Terminal value, undiscounted", d["tv"])
    one("Present value of the terminal value", d["pv_tv"])
    if d.get("tv_share") is not None:
        one("Terminal value as a share of enterprise value", d["tv_share"], pct=True)
    if w.get("wacc_exp") is not None:
        one("Cost of capital, first explicit year", w["wacc_exp"], pct=True)
    if w.get("wacc_term") is not None:
        one("Cost of capital, terminal", w["wacc_term"], pct=True)
    g = (numbers.get("inputs", {}).get("g_term") or {}).get("value")
    if g is not None:
        one("Terminal growth", g, pct=True)
    one("ENTERPRISE VALUE", d["ev"])
    one("Less: net debt", -d["nd"])
    if d.get("assoc"):
        one("Add: investments in associates", d["assoc"])
    if d.get("nci_val") is not None:
        one("Less: minority interests", -d["nci_val"])
    emp = d.get("emp_val")
    if emp:
        one("Less: employees' statutory share of profit", -emp)
    one("EQUITY VALUE", d["eq_attr"])
    sh = numbers.get("meta", {}).get("shares") or d.get("shares")
    if sh:
        one("Shares in issue (mn)", sh)
    ps_dec = d.get("ps_dec")
    if ps_dec is not None:
        one("Value per share at the model date", ps_dec, dp=per_share_dp)
    one("VALUE PER SHARE", d["ps"], dp=per_share_dp)

    # ---- the reconciliation, as an assert and not a footnote ---------------
    rec = dict(rule="R-DCF-01", years=yrs,
               pv_explicit_published=d["pv_explicit"], ev_published=d["ev"],
               ps_published=d["ps"])
    if pv is not None:
        s = sum(pv)
        rec["pv_explicit_summed"] = s
        if abs(s - d["pv_explicit"]) > max(1.0, 1e-6 * abs(d["pv_explicit"])):
            raise DCFTableError(
                "the present values in this table sum to %.1f against the study's published "
                "%.1f. The table is read from the study and may not disagree with it."
                % (s, d["pv_explicit"]))
        ev_chk = s + d["pv_tv"]
        rec["ev_summed"] = ev_chk
        if abs(ev_chk - d["ev"]) > max(1.0, 1e-6 * abs(d["ev"])):
            raise DCFTableError(
                "explicit PV %.1f + terminal PV %.1f = %.1f against a published enterprise "
                "value of %.1f" % (s, d["pv_tv"], ev_chk, d["ev"]))
    return rows, rec


def sensitivity_grid(numbers, currency="EGP"):
    """(rows, record) -- terminal cost of capital DOWN, terminal growth ACROSS.

    The adopted case MUST be the centre cell. A grid whose axes do not contain the
    number the study struck is a grid the reader cannot locate the answer on, and
    that is what every study in this book shipped until 10-Sep-2026 [R-SENS-01].
    """
    s = numbers.get("sens_wg")
    if not s:
        raise DCFTableError("the numbers file carries no sens_wg grid")
    g, wg, tab = s["g_grid"], s["wacc_grid"], s["table"]
    if len(g) % 2 == 0 or len(wg) % 2 == 0:
        raise DCFTableError("a grid with an even axis has no centre cell to reconcile")
    gi, wi = len(g) // 2, len(wg) // 2
    central = numbers.get("central")
    centre = tab[wi][gi]
    if central is not None and abs(centre - central) > 0.01:
        raise DCFTableError(
            "the centre cell reads %.2f and the study's central is %.2f. The grid must be "
            "CENTRED on the adopted case: axes step around the struck values, they are not "
            "a typed ladder that happens to sit near them." % (centre, central))
    rows = [["%s / share — terminal cost of capital (down) vs terminal growth (across)"
             % currency] + ["{:.2%}".format(x) for x in g]]
    for i, wv in enumerate(wg):
        rows.append(["{:.2%}".format(wv)] + ["{:,.2f}".format(v) for v in tab[i]])
    return rows, dict(rule="R-SENS-01", centre_cell=centre, central=central,
                      g_grid=g, wacc_grid=wg)
