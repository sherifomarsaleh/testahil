"""[R-COC-02] — the cost of equity reproduces from its own committed inputs.

THE DEFECT, IN THE PRINCIPAL'S WORDS: a study that "creates wrong cost or high Ke and Kd".

WHAT WAS AND WAS NOT ALREADY CHECKED. [R-COC-01] and check_cost_of_capital.py enforce a
great deal about the CONSTRUCTION — the sovereign counted exactly once, Kd above its own
sovereign, market-value weights, the glide, WACC_TERM below WACC_EXP, the three-assert Kd
gate, the 150bp bound and its re-pointing. Measured 07-09-2026, NOTHING ANYWHERE
REPRODUCED KE: a search of every file in scripts/ for ke_exp, cost_of_equity, ke_terminal,
capm and "rf_star +" returned no match, and check_cost_of_capital reads rf_star exactly
once, to test the risk-free NORMALISATION identity and never the CAPM one.

SO A COST OF EQUITY TYPED 300 BASIS POINTS HIGH PASSED EVERY CHECK IN THE REPOSITORY.
Priced on ARCC's own committed sensitivity grid, the input with the widest committed
uncertainty in that model was the one input whose arithmetic nothing reproduced: +300bp of
WACC is -3.1% of value, beta 0.80 to 1.15 — both inside the study's own confidence
interval — is -16%, and the study's own 95% beta interval spans a fair value from 59.35 to
102.54 against a published 66.53.

THE FIRST DRAFT OF THIS CHECK WOULD HAVE CONDEMNED TWO STUDIES THAT ARE RIGHT, AND THAT IS
RECORDED HERE RATHER THAN QUIETLY FIXED. Requiring ke_terminal = rf_t + beta x erp_t — the
arithmetic engine/cost_of_capital.py itself performs — reproduces ADNOCLS, PHDC and TMGH to
the basis point and misses ARCC by 102.87bp and SCEM by 132.24bp. Both differences resolve
EXACTLY, to six decimals, as a Hamada RELEVERING of beta from the current capital structure
to the terminal one at a 22.5% tax rate: ARCC's beta of 0.927522 unlevers to 0.900090 and
relevers to 1.074483 against an implied 1.074483; SCEM's 1.000000 unlevers to 0.995949 and
relevers to 1.188914 against an implied 1.188914. That is a correct and ordinary
construction, and per [R-COC-01] the answer to a check firing on work that is right is to
RE-POINT it, never to widen it and never to move the number to satisfy it.

WHAT THE MEASUREMENT ACTUALLY FOUND IS BETTER THAN A WRONG NUMBER AND WORSE THAN NOTHING:
the book runs TWO different terminal cost-of-equity constructions, the sanctioned module
performs only one of them, and NEITHER STUDY'S RECORD SAYS WHICH IT USED — no occurrence of
relever, unlever, Hamada or target structure anywhere in either. So a reader cannot tell
1.074483 from a typo, and neither could any instrument. THE DEFECT IS THE UNDECLARED
CONSTRUCTION, not the arithmetic.

THE RULE: Ke reproduces from the record's own inputs under a construction the record NAMES,
from a CLOSED list. The list is closed for [R-COC-01 AMENDED]'s reason — an open one lets a
study opt out by inventing a construction, and "our terminal is different" is not a
construction.

TOLERANCE IS NOT A FREE PARAMETER HERE, because this is an IDENTITY rather than an
estimate. The records carry full double precision, so a study that computed Ke this way
agrees to float noise; anything above that is a different computation, not a rounding.
A record storing ROUNDED figures is its own failure — a record that does not carry its own
precision — and is reported as that rather than absorbed by widening the bound.
"""
from __future__ import annotations

FLOAT_NOISE = 1e-9

# CLOSED. A construction not on this list is not a construction.
TERMINAL_CONSTRUCTIONS = ("same_beta", "relevered", "split_premium",
                          "beta_to_one_split")

# `beta_to_one_split` WAS ADDED 10-09-2026 BECAUSE THE BOOK RUNS IT, not because a
# study asked to be let through. Two names -- SWDY and EIPICO -- carry a terminal
# beta of exactly 1.00 on the reasoning that a beta reverts to the market over a
# perpetuity, alongside [R-COC-03]'s split premium. Both reproduce to 0.0000bp
# under it. That is the same ground on which `relevered` was added when two studies
# were found doing Hamada and nothing could tell a relevered beta from a typo.
#
# THE LIST STAYS CLOSED AND THE RECORD MUST PUBLISH `beta_terminal`. A study that
# reverts its beta and does not say so is indistinguishable from one that typed the
# wrong beta, which is the whole reason this module exists; and a construction is
# admitted here on evidence that the book performs it, never on the grounds that a
# study would otherwise fail.

# THE EXPLICIT WINDOW HAS A CLOSED LIST TOO, FROM 10-09-2026, and until it did this
# check tested the RETIRED identity and nothing else. That is worse than not testing:
# rf* + beta x ERP_total multiplies the country premium by beta, which is the exact
# double count [R-COC-03] was adopted to stop -- so the gate PASSED the construction
# the standard forbids and FAILED all four studies in the book that had already been
# rebuilt on the right one. A gate that is inverted is not a weak gate.
#
# `total_premium` is kept because a record struck before 10-09-2026 did that, and
# rewriting history to match a later rule is not verification. It is reported as
# SUPERSEDED rather than accepted silently.
EXPLICIT_CONSTRUCTIONS = ("split_premium", "total_premium")


class KeError(Exception):
    pass


def ke_explicit_split(rf_star, beta, erp_mature, crp_effective):
    """Ke under [R-COC-03]: beta on the MATURE premium, the country premium added flat.

    THE SANCTIONED EXPLICIT-WINDOW CONSTRUCTION from 10-Sep-2026. `ke_explicit`
    below reproduces the RETIRED one and is kept only so records struck before that
    date still verify against what they actually did -- rewriting them to match a
    later rule would be rewriting history. A record struck after that date and
    reproducing only under `ke_explicit` is a defect, not an alternative.
    """
    return rf_star + beta * erp_mature + crp_effective


def crp_effective(rec):
    """The country premium a record actually charges, from components it PUBLISHES.

    [R-COC-03] charges country risk once, at the weight of the operations: lambda of it
    where the company operates, and the foreign country's own premium on the rest. Both
    legs must be in the record. Nothing is solved here -- a check that solves lambda out
    of the published answer reproduces whatever it is handed, which is the failure the
    terminal side of this module already names.

    Returns None when the record does not publish the split, which is a failure to be
    REPORTED rather than a licence to fall back on the retired identity.
    """
    crp = rec.get("crp")
    if crp is None:
        return None
    lam = rec.get("lambda_country")
    if lam is None:
        return None
    if not 0.0 <= lam <= 1.0:
        raise KeError("lambda_country %r is outside [0,1]" % lam)
    if lam == 1.0:
        return crp
    foreign = rec.get("crp_foreign")
    if foreign is None:
        raise KeError("lambda_country is %.4f, so %.2f%% of the operations sit outside "
                      "the country whose premium is charged, and the record states no "
                      "crp_foreign for them. A lambda below one without a foreign "
                      "premium charges nothing at all for that share of the business"
                      % (lam, 100 * (1 - lam)))
    return lam * crp + (1.0 - lam) * foreign


def ke_explicit(rf_star, beta, erp):
    """The explicit-window CAPM identity, exactly as engine/cost_of_capital.py performs it.

    The committed `erp` is the figure AFTER any country-premium lambda scaling, because
    that is what the module stores; reproducing from a pre-scaled premium would fail on
    every study that scales one.
    """
    return rf_star + beta * erp


def relevered_beta(beta, weight_debt, weight_equity, weight_debt_terminal, tax_rate):
    """Hamada: unlever at today's structure, relever at the terminal one.

    RAISES rather than returning a plausible number on a structure that cannot support
    the arithmetic — a terminal debt weight of 1.0 has no equity to lever.
    """
    if weight_equity <= 0 or weight_debt_terminal is None:
        raise KeError("no equity weight, or no terminal debt weight, to relever against")
    if not 0 <= weight_debt_terminal < 1:
        raise KeError("terminal debt weight %r is outside [0,1)" % weight_debt_terminal)
    de_now = weight_debt / weight_equity
    beta_u = beta / (1 + (1 - tax_rate) * de_now)
    de_term = weight_debt_terminal / (1 - weight_debt_terminal)
    return beta_u * (1 + (1 - tax_rate) * de_term)


def ke_terminal(rec, construction, tax_rate=None):
    """Reproduce the terminal cost of equity under a NAMED construction."""
    if construction not in TERMINAL_CONSTRUCTIONS:
        raise KeError("terminal construction %r is not on the closed list %s"
                      % (construction, list(TERMINAL_CONSTRUCTIONS)))
    rf_t, erp_t, beta = rec.get("rf_terminal"), rec.get("erp_terminal"), rec.get("beta")
    if None in (rf_t, erp_t, beta):
        raise KeError("record carries no rf_terminal, erp_terminal or beta")
    if construction == "split_premium":
        # [R-COC-03]: the terminal premium is a total and splits the same way. The
        # record must carry the split it used -- solving for it here would make the
        # check reproduce whatever it was handed.
        em, ce = rec.get("erp_mature"), rec.get("crp_effective_terminal")
        if None in (em, ce):
            raise KeError("a split_premium terminal must record erp_mature and "
                          "crp_effective_terminal; neither is derivable from the total "
                          "without assuming the answer")
        return rf_t + beta * em + ce
    if construction == "beta_to_one_split":
        em, ce = rec.get("erp_mature"), rec.get("crp_effective_terminal")
        bt = rec.get("beta_terminal")
        if None in (em, ce):
            raise KeError("a beta_to_one_split terminal must record erp_mature and "
                          "crp_effective_terminal")
        if bt is None:
            raise KeError("a beta_to_one_split terminal must record beta_terminal. A "
                          "beta that reverts and does not say so cannot be told from a "
                          "beta that was typed wrong")
        if abs(bt - 1.0) > FLOAT_NOISE:
            raise KeError("beta_to_one_split names a terminal beta of one and the record "
                          "states %.6f. Reverting to something other than the market is a "
                          "different construction and needs its own name" % bt)
        return rf_t + bt * em + ce
    if construction == "same_beta":
        return rf_t + beta * erp_t
    if tax_rate is None:
        raise KeError("a relevered terminal needs the tax rate it was relevered at, "
                      "named in the record — it cannot be inferred from the answer")
    b = relevered_beta(beta, rec.get("weight_debt"), rec.get("weight_equity"),
                       rec.get("weight_debt_terminal"), tax_rate)
    return rf_t + b * erp_t


def implied_relevering_tax(rec):
    """Solve the tax rate a relevered terminal beta implies, ALGEBRAICALLY.

    DIAGNOSTIC ONLY, and the distinction is the whole point: this exists so a refusal
    tells the author what to declare instead of handing them a puzzle. It is never
    accepted as the declaration — a rate solved out of the answer it is meant to explain
    is the reverse-engineered construction this house prohibits, and accepting it would
    make the check unfalsifiable by construction.

    From ke_t = rf_t + beta_L x erp_t and Hamada,
        k  = (ke_t - rf_t) / erp_t / beta = (1 + (1-t).de_t) / (1 + (1-t).de_now)
        t  = 1 - (1 - k) / (k.de_now - de_t)
    Returns None where the algebra does not close.
    """
    try:
        rf_t, erp_t, beta = rec["rf_terminal"], rec["erp_terminal"], rec["beta"]
        ket, wd, we = rec["ke_terminal"], rec["weight_debt"], rec["weight_equity"]
        wdt = rec["weight_debt_terminal"]
        if not erp_t or not beta or not we or wdt is None or not 0 <= wdt < 1:
            return None
        k = (ket - rf_t) / erp_t / beta
        de_now, de_t = wd / we, wdt / (1 - wdt)
        denom = k * de_now - de_t
        if abs(denom) < 1e-12:
            return None
        t = 1 - (1 - k) / denom
        return t if -0.05 <= t <= 0.60 else None
    except Exception:
        return None


def _check_explicit(rec, rs, b, ke):
    """Reproduce the explicit-window Ke under the construction the record NAMES.

    Same discipline as the terminal side: a closed list, and where the record declares
    nothing the failure message says which construction it actually matches, so the fix
    is one line rather than a puzzle.
    """
    cons = rec.get("ke_construction")
    if cons is not None and cons not in EXPLICIT_CONSTRUCTIONS:
        return ["ke_construction %r is not on the closed list %s"
                % (cons, list(EXPLICIT_CONSTRUCTIONS))]

    try:
        ce = crp_effective(rec)
    except KeError as exc:
        return [str(exc)]
    em = rec.get("erp_mature")
    split = None
    if ce is not None and em is not None:
        split = ke_explicit_split(rs, b, em, ce)

    e = rec.get("erp")
    total = ke_explicit(rs, b, e) if e is not None else None

    if cons == "split_premium":
        if split is None:
            return ["ke_construction says split_premium, so the record must publish "
                    "erp_mature, crp and lambda_country (and crp_foreign where lambda "
                    "is below one). It publishes %s"
                    % ([k for k in ("erp_mature", "crp", "lambda_country", "crp_foreign")
                        if rec.get(k) is not None] or "none of them")]
        if abs(split - ke) > FLOAT_NOISE:
            return ["ke_exp %.10f does not reproduce under its own declared "
                    "split_premium construction = %.10f (%+.2f bp)"
                    % (ke, split, (ke - split) * 1e4)]
        return []

    if cons == "total_premium":
        if total is None:
            return ["ke_construction says total_premium and the record publishes no erp"]
        if abs(total - ke) > FLOAT_NOISE:
            return ["ke_exp %.10f does not reproduce under its own declared "
                    "total_premium construction = %.10f (%+.2f bp)"
                    % (ke, total, (ke - total) * 1e4)]
        return ["ke_construction is total_premium, the SUPERSEDED identity: it multiplies "
                "the country premium by beta, which [R-COC-03] charges once and flat. The "
                "arithmetic reproduces and the construction is retired; a record struck "
                "after 10-09-2026 must be rebuilt on split_premium"]

    # UNDECLARED. Name what it matches.
    if split is not None and abs(split - ke) <= FLOAT_NOISE:
        return ["ke_exp names no construction. It reproduces under 'split_premium' — "
                "declare it, so a reader can tell the sanctioned construction from a "
                "coincidence"]
    if total is not None and abs(total - ke) <= FLOAT_NOISE:
        return ["ke_exp names no construction. It reproduces under the SUPERSEDED "
                "'total_premium' identity, which multiplies the country premium by beta"]
    hint = ""
    if e is not None and rec.get("default_spread") is not None:
        try:
            import cost_of_capital as _coc
            _crp, _em = _coc.split_erp(e, rec["default_spread"])
            if _crp:
                lam = (ke - rs - b * _em) / _crp
                hint = ("; splitting the committed erp gives a mature premium of %.4f and "
                        "a country premium of %.4f, under which the published Ke implies "
                        "lambda = %.4f. PUBLISH the components rather than leaving them to "
                        "be solved out of the answer" % (_em, _crp, lam))
        except Exception:                                            # noqa: BLE001
            pass
    return ["ke_exp %.10f reproduces under no construction on the closed list %s%s"
            % (ke, list(EXPLICIT_CONSTRUCTIONS), hint)]


def check(rec):
    """Return a list of failure strings. Empty means the record's Ke reproduces.

    This makes no claim that a cost of equity of 28% is right for a company. It claims
    only that the number published is the number its own inputs produce, under a
    construction the record names.
    """
    fails = []
    if not isinstance(rec, dict):
        return ["no cost_of_capital_record committed"]

    rs, b, ke = rec.get("rf_star"), rec.get("beta"), rec.get("ke_exp")
    # NAME WHAT IS ACTUALLY MISSING. This said "carries no rf_star, beta or ke_exp" whenever
    # ANY ONE of the three was absent — so it reported two fields as missing that the record
    # plainly carries, and a reader chasing it had to open the file to find out which of the
    # three the gate meant. The wording is also a ratchet SIGNATURE, so a message that names
    # a fixed list changes shape every time the list does: narrowing this check from four
    # fields to three on 10-09-2026 turned a knowingly-outstanding study into a "new breach"
    # without anything about that study changing [R-ENF-08]. Derived from the record, it
    # only changes when the record does.
    # THE LEGS MUST ADD BACK TO THE TOTAL THEY WERE SPLIT FROM. Under the split identity
    # the rate is built from erp_mature and the country premium, so the published TOTAL
    # premium stops being an input to anything a reader checks — and a total quietly raised
    # sails through. The negative control caught it the moment the fixtures moved across:
    # "an ERP quietly raised" went green. The identity is erp = erp_mature + crp, it is
    # Damodaran's own, and it costs one line to hold [R-COC-03].
    _em, _crp, _erp = rec.get("erp_mature"), rec.get("crp"), rec.get("erp")
    if None not in (_em, _crp, _erp) and abs((_em + _crp) - _erp) > FLOAT_NOISE:
        fails.append("the split does not add back: erp_mature %.6f + crp %.6f is %.6f "
                     "against a published total premium of %.6f. A total that no longer "
                     "feeds the rate is a number nothing checks"
                     % (_em, _crp, _em + _crp, _erp))
    _absent = [n for n, v in (("rf_star", rs), ("beta", b), ("ke_exp", ke)) if v is None]
    if _absent:
        fails.append("record carries no %s, so the explicit cost of equity cannot be "
                     "reproduced at all" % " or ".join(_absent))
    else:
        fails.extend(_check_explicit(rec, rs, b, ke))

    fails.extend(check_weights(rec))
    fails.extend(check_beta_source(rec))

    ket = rec.get("ke_terminal")
    if ket is None:
        return fails                      # a record with no terminal is not this test's subject

    cons = rec.get("ke_terminal_construction")
    tax = rec.get("relevering_tax_rate")
    if cons is None:
        # UNDECLARED. Say which construction it actually matches, because naming it is
        # what turns a refusal into a one-line fix rather than a puzzle.
        hint = "; it reproduces under NEITHER, which is the more serious reading"
        try:
            if abs(ke_terminal(rec, "same_beta") - ket) <= FLOAT_NOISE:
                hint = "; it reproduces under 'same_beta'"
        except KeError:
            pass
        if "same_beta" not in hint:
            t = implied_relevering_tax(rec)
            if t is not None:
                try:
                    if abs(ke_terminal(rec, "relevered", t) - ket) <= FLOAT_NOISE:
                        hint = ("; it reproduces under 'relevered' at an implied tax rate "
                                "of %.2f%%, which the record does not state — declare it, "
                                "do not let it be solved out of the answer" % (100 * t))
                except KeError:
                    pass
        fails.append("ke_terminal names no construction. The record must declare one of "
                     "%s%s" % (list(TERMINAL_CONSTRUCTIONS), hint))
        return fails

    try:
        want = ke_terminal(rec, cons, tax)
    except KeError as e:
        fails.append(str(e))
        return fails
    if abs(want - ket) > FLOAT_NOISE:
        fails.append("ke_terminal %.10f does not reproduce under its own declared "
                     "construction %r = %.10f (%+.2f bp)"
                     % (ket, cons, want, (ket - want) * 1e4))
    return fails

# ---------------------------------------------------------------- the weights

# EXTENDED 07-09-2026, on the census's own finding, verified by hand. [R-COC-01] requires
# MARKET-VALUE weights and a WACC built from them, and nothing reproduced the WACC either.
# THE EXEMPLAR IS THE WORKED CASE AND THAT IS WHY IT MATTERS: ADNOCLS's committed weights
# are 0.800444 and 0.071933, WHICH SUM TO 0.872377 RATHER THAN ONE, and its committed
# wacc_exp of 8.5484% does not reproduce from them — we*ke + wd*kd_after_tax gives 7.9230%,
# 62.5bp adrift, and renormalising the weights gives 9.0821%, adrift the other way. Neither
# reading reaches the published figure. This is the document every new study is built by
# copying [R-ENF-01 EXTENDED 04-Sep], so a construction it carries propagates looking
# exactly like the house standard.
#
# THE BETA'S PROVENANCE RIDES WITH IT, and the census was half right about SCEM in a way
# worth recording. Its record carries beta = 1.0 where the own-stock regression measures
# far lower — which reads like a typed number and is NOT one: the study's own input register
# says the regression FAILS the usability gate at R-squared 0.038 against the 0.05 floor,
# that the lead-lag estimate is 0.837 with a 90% interval containing 1.00, and that rounding
# to 1.00 costs 1.84% of the central, "stated rather than left implicit". That is the
# sanctioned tier-3 fallback, done properly. WHAT IS MISSING IS THAT THE RECORD CANNOT SAY
# SO: beta_source is None, the justification lives on a different object, and a reader of
# the cost-of-capital record sees 1.0 with no provenance — so nothing distinguishes a
# priced fallback from a number somebody typed.

BETA_SOURCES = ("own_stock_regression", "peer_relevered", "tier3_fallback", "shrunk")


# RE-POINTED 07-09-2026, ON THE EXEMPLAR, AND THE RE-POINTING IS THE FINDING. The clause
# above was written from the census and was WRONG ABOUT ADNOCLS. Its weights do not sum to
# one over TWO tranches because that company is financed by THREE: equity 0.800444, drawn
# debt 0.071933 AND PERPETUAL CAPITAL SECURITIES AT 0.127635, which sum to 1.000000 exactly
# and reproduce wacc_exp to ZERO — 0.0854836070 against a committed 0.0854836070, and the
# terminal likewise. THE RECORD WAS RIGHT AND THE GATE COULD ONLY COUNT TO TWO. Per
# [R-COC-01]: WHEN A CHECK FIRES ON WORK THAT IS RIGHT, RE-POINT IT — never widen the
# tolerance and never move the number to satisfy it.
#
# WHY A DECLARED TRANCHE IS NOT THE OPEN LIST THIS HOUSE FORBIDS ELSEWHERE. A declared
# MECHANISM (a reason a bound does not apply) is unfalsifiable text, which is why those
# lists are closed. A declared TRANCHE carries a WEIGHT and a RATE, and adding one changes
# the arithmetic the record must then satisfy in two places at once: the weights must still
# sum to one, and the WACC must still reproduce over all of them. A study cannot buy itself
# slack by inventing a tranche — an invented tranche has to be paid for out of the weights
# of the real ones and out of the published WACC. THE ARITHMETIC IS THE CLOSURE.
#
# WHAT IS STILL REFUSED, AND IT IS THE THING THAT WAS ACTUALLY WRONG HERE: a record whose
# weights do not sum to one AND WHICH DECLARES NOTHING TO ACCOUNT FOR THE REMAINDER. The
# exemplar's hybrid weight was committed under `wh` in a different object; a reader of the
# cost-of-capital record saw two weights and a gap, and so did every instrument.

def other_tranches(rec):
    """The tranches beyond equity and debt, as (name, weight, rate) — [] if none.

    A tranche is (weight, rate) or it is not a tranche: a name with no rate cannot be
    priced into a weighted average, and a weight with no name cannot be read by anyone.
    """
    out, bad = [], []
    for i, tr in enumerate(rec.get("other_tranches") or []):
        if not isinstance(tr, dict):
            bad.append("tranche %d is not a record" % (i + 1))
            continue
        nm, w, r = tr.get("name"), tr.get("weight"), tr.get("rate")
        if not str(nm or "").strip():
            bad.append("tranche %d names nothing" % (i + 1))
        if not isinstance(w, (int, float)) or not isinstance(r, (int, float)):
            bad.append("tranche %r carries no weight and rate to be averaged over"
                       % (nm or i + 1))
            continue
        out.append((str(nm), float(w), float(r)))
    return out, bad


#: grounds on which a record legitimately carries NO weights, because there is no
#: weighted rate to build. CLOSED, and the same list and the same "<ground>: <why>"
#: shape as NO_WACC_GROUNDS in scripts/check_cost_of_capital.py — one fact, one place
#: to change it. An open list would let any study opt out of the weights clause by
#: inventing a reason [R-ENF-03].
NO_WEIGHTS_GROUNDS = {
    "bank": ("deposits are raw material rather than financing; their cost is inside the "
             "net interest margin and equity flows are discounted at the cost of equity"),
}


def _no_weights_ground(rec):
    """(exempt, failure) — never exempt on the declared word alone."""
    ground = rec.get("no_wacc_reason")
    if not ground:
        return False, None
    key = str(ground).split(":", 1)[0].strip().lower()
    if key not in NO_WEIGHTS_GROUNDS:
        return False, ("no_wacc_reason names %r, which is not on the closed list %s"
                       % (key, sorted(NO_WEIGHTS_GROUNDS)))
    # THE CLAIM IS THAT THERE IS NO WEIGHTED RATE. A weighted rate says otherwise.
    for f in ("wacc_exp", "wacc_terminal", "weight_debt", "weight_equity"):
        if rec.get(f) is not None:
            return False, ("claims the %r ground and still carries %s. The ground says "
                           "there is nothing to weight" % (key, f))
    return True, None


def check_weights(rec):
    """Failures in the weights and the WACC they are supposed to build."""
    fails = []
    we, wd = rec.get("weight_equity"), rec.get("weight_debt")
    if not isinstance(we, (int, float)) or not isinstance(wd, (int, float)):
        # RE-POINTED, NOT WIDENED [R-COC-01]. The population for this clause is every
        # record that HAS a weighted rate, not every record. A deposit-funded bank has
        # no market-value capital structure to weight — reporting it as "carries no
        # weights" says the check could not find something that is not there.
        exempt, why = _no_weights_ground(rec)
        if exempt:
            return []
        if why:
            return [why]
        return ["record carries no market-value weights"]

    extra, bad = other_tranches(rec)
    fails.extend(bad)

    # NET WEIGHTS ARE A LEGITIMATE CONSTRUCTION on a net-cash company — [R-BRIDGE-01]'s own
    # negative control keeps a clean case for exactly that — so a NEGATIVE debt weight is
    # not the defect. Weights that do not SUM TO ONE are, whatever their signs.
    total = we + wd + sum(w for _, w, _ in extra)
    if abs(total - 1.0) > 1e-6:
        named = "".join(" + %s %.6f" % (n, w) for n, w, _ in extra)
        fails.append("weight_equity %.6f + weight_debt %.6f%s = %.6f, not one — a weighted "
                     "average over weights that do not sum to one is not an average of "
                     "anything%s" % (we, wd, named, total,
                                     "" if extra else ". If this company is financed by a "
                                     "tranche beyond equity and drawn debt, the record has "
                                     "to declare it in other_tranches with its weight and "
                                     "its rate, because a reader cannot price a gap"))

    wacc, ke, kd_at = rec.get("wacc_exp"), rec.get("ke_exp"), rec.get("kd_aftertax")
    if all(isinstance(x, (int, float)) for x in (wacc, ke, kd_at)):
        want = we * ke + wd * kd_at + sum(w * r for _, w, r in extra)
        if abs(want - wacc) > 1e-6:
            fails.append("wacc_exp %.6f does not reproduce from its own weights and rates "
                         "(%.6f, %+.1f bp)" % (wacc, want, (wacc - want) * 1e4))
    return fails


def check_beta_source(rec):
    """The record must say WHERE its beta came from."""
    if rec.get("beta") is None:
        return []
    src = rec.get("beta_source")
    if src is None:
        return ["the record names no beta_source, so nothing distinguishes a measured "
                "regression from a priced tier-3 fallback from a number somebody typed. "
                "One of %s" % list(BETA_SOURCES)]
    if src not in BETA_SOURCES:
        return ["beta_source %r is not on the closed list %s" % (src, list(BETA_SOURCES))]
    return []
