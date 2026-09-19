"""The currency of borrowing, and what [R-COC-01] does with it.  [R-COC-01 AMENDED 08-09-2026]

[R-COC-01] has always said two things about a cost of debt and only one of them was
ever evaluated. It refuses a rate below its own sovereign **on an all-local-currency
book**, and it requires foreign-currency debt to be carried at **local-equivalent
cost** -- the foreign coupon plus the expected local depreciation. Nothing anywhere
established which kind of book a name had, so the floor was applied unconditionally:
the qualifier was doing load-bearing work in a sentence nobody was made to evaluate.

WHAT THIS MODULE DOES NOT DO IS DELETE OR WIDEN THE FLOOR. Where a run commits a
currency composition read from the company's own filings, the book is split and each
half is priced exactly as the rule already directs -- the local tranche keeps the full
floor, and the foreign tranche is carried at local-equivalent cost. Where nothing is
committed, or where the disclosure does not foot, NOTHING CHANGES and the floor stands
on the whole book.

A currency with no disclosed rate is treated as LOCAL, which never understates the
cost. That is SIGCM clause 8 -- the gap named rather than filled -- and it is
deliberately the conservative direction.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)


def committed(tk):
    """The run's own committed record, or None with the reason."""
    p = os.path.join(ENGINE, "%s_walkforward" % tk.lower(), "debt_currency.json")
    if not os.path.exists(p):
        return None, "this run commits no currency of borrowing"
    try:
        return json.load(open(p, encoding="utf-8")), None
    except Exception as exc:
        # An unreadable record is not an absent one and is not a clean one either
        # [R-ENF-04]: it is reported, never skipped into the unchanged branch.
        return None, "the committed record will not parse: %s" % type(exc).__name__


def split(tk, origin):
    """The quoted-foreign share of the book and its amount-weighted disclosed rate.

    Returns (record, None) or (None, reason). The reason is carried so a cell that
    keeps the floor says WHY it kept it rather than looking as though nobody asked.
    """
    doc, why = committed(tk)
    if doc is None:
        return None, why
    r = (doc.get("origins") or {}).get(str(origin))
    if r is None:
        return None, "the committed record carries no entry at this origin"
    if r.get("refused"):
        return None, "the disclosure does not foot and was refused: %s" % r["reason"][:80]
    total = r.get("total_debt_egp_mn")
    quoted = r.get("quoted_fx_egp_mn")
    rates = r.get("disclosed_rates") or {}
    by = r.get("by_currency_egp_mn") or {}
    if not total or quoted is None:
        return None, "the entry carries no total or no quoted foreign amount"
    amts = {c: by[c] for c in by if c in rates and c != "EGP"}
    if not amts or sum(amts.values()) <= 0:
        return None, "no foreign currency at this origin carries a disclosed rate"
    tot_q = sum(amts.values())
    r_fx = sum(amts[c] * rates[c] for c in amts) / tot_q
    r_local = rates.get("EGP")
    if r_local is None:
        return None, "the entry carries no disclosed local rate"
    w_fx = tot_q / total
    if not (0.0 < w_fx <= 1.0):
        return None, "the quoted foreign share does not lie in (0, 1]"
    return {"w_fx": w_fx, "r_fx": r_fx, "r_local": r_local,
            "quoted_egp_mn": tot_q, "total_egp_mn": total,
            "currencies": sorted(amts)}, None


def kd(rec, sovereign, depreciation):
    """kd = w_local x max(r_local, sovereign) + w_foreign x (r_foreign + depreciation).

    The local tranche keeps the full floor because on a local tranche the floor's
    premise holds -- a same-currency corporate cannot borrow below its sovereign. The
    foreign tranche is carried at local-equivalent cost, the depreciation taken from
    the SAME purchasing-power relation this lens builds every currency path on, never
    a second one.
    """
    w = rec["w_fx"]
    local = max(rec["r_local"], sovereign)
    foreign = rec["r_fx"] + depreciation
    return (1.0 - w) * local + w * foreign
