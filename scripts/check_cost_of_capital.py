"""THE COST-OF-CAPITAL SCHEDULE, CHECKED FROM OUTSIDE THE STUDY.

[R-COC-01], enforced per [R-ENF-01].

The protocol has carried the sliding-schedule procedure since 13 July 2026 — each
explicit year discounted at its own forward rate, the glide's shape taken from
the cost-of-debt path, a norm-built terminal, and a three-part integrity gate on
the cost of debt. It is written down in both governing documents. On 2 September
2026 exactly ONE study implemented it. PHDC and TMGH discount every explicit year
and the terminal alike at 26.25% and 32.37%, which asserts that Egypt's cost of
capital never normalises while the central bank publishes a disinflation path and
the studies' own cost-of-debt assumptions contradict them.

What this gate reads is each study's own committed cost-of-capital record and
what it asserts is that the schedule is a schedule: a declining ladder in a
market in transition, the terminal below the explicit window, the terminal value
brought home on the SAME cumulative factor as the last explicit year, country
risk counted exactly once, the cost of debt above its own sovereign and inside
the three-assert gate, and market-value equity weights.

Population-anchored [R-ENF-04], ratcheted [R-ENF-02].

    python3 scripts/check_cost_of_capital.py
    python3 scripts/check_cost_of_capital.py --prune
"""
import glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
sys.path.insert(0, ENGINE)

OUTSTANDING_FILE = os.path.join(ENGINE, "build_depth_audit", "coc_outstanding.json")
RECORD_KEYS = ("cost_of_capital_record", "coc_record", "schedule_record")
TOL = 1e-6


def studies():
    return sorted(glob.glob(os.path.join(ENGINE, "*_study")))


def ticker_of(sdir):
    return os.path.basename(sdir)[: -len("_study")].upper()


def numbers_file(sdir):
    for name in ("study_numbers.json", "numbers.json"):
        p = os.path.join(sdir, name)
        if os.path.exists(p):
            return p
    c = [p for p in glob.glob(os.path.join(sdir, "*.json"))
         if "numbers" in os.path.basename(p).lower()]
    return c[0] if c else None


def find_record(doc):
    for k in RECORD_KEYS:
        if isinstance(doc.get(k), dict):
            return doc[k]
    meta = doc.get("meta")
    if isinstance(meta, dict):
        for k in RECORD_KEYS:
            if isinstance(meta.get(k), dict):
                return meta[k]
    return None


def check_record(rec, ticker):
    """Every clause, on the study's own committed numbers."""
    import macro_path as MP
    fails = []

    mkt = (rec.get("market") or "").upper()
    try:
        path = MP.load(mkt)
    except Exception as e:                                   # noqa: BLE001
        return ["the record's market %r has no house macro path: %s" % (mkt, e)]

    # 1. country risk counted once
    rf, sp, rfs = rec.get("rf_observed"), rec.get("default_spread"), rec.get("rf_star")
    if None in (rf, sp, rfs):
        fails.append("the record does not carry the observed risk-free rate, the sovereign's "
                     "own default spread and the normalised rate; country risk cannot be "
                     "shown to be counted once")
    elif abs((rf - sp) - rfs) > TOL:
        fails.append("the normalised risk-free rate %.6f is not the observed %.6f less this "
                     "sovereign's own default spread %.6f. Using the raw local yield beside a "
                     "premium that already carries country risk double-counts it."
                     % (rfs, rf, sp))

    # 2. the terminal is derived, not quoted
    rf_t = rec.get("rf_terminal")
    if rf_t is None:
        fails.append("no terminal risk-free rate recorded")
    elif abs(rf_t - path.terminal_rf) > TOL:
        fails.append("the terminal risk-free rate %.6f is not the derived %.6f (the inflation "
                     "target in force plus the real-rate convention). A terminal rate "
                     "reverse-engineered from a price is the quietest lever there is."
                     % (rf_t, path.terminal_rf))

    # 3. the schedule declines, and only where a glide belongs
    we, wt = rec.get("wacc_exp"), rec.get("wacc_terminal")
    fwd = rec.get("forward_wacc") or []
    if we is None or wt is None:
        fails.append("no explicit-window or terminal cost of capital recorded")
    elif path.regime == "transition":
        if wt >= we - TOL:
            fails.append("the terminal cost of capital %.4f is not below the explicit-window "
                         "rate %.4f in a market the house path calls a transition. A flat rate "
                         "asserts the economy never normalises, against the central bank's own "
                         "published path." % (wt, we))
        if not fwd:
            fails.append("no forward cost-of-capital ladder recorded: the record shows a single "
                         "rate where the procedure requires one rate per explicit year")
    if fwd:
        for i in range(len(fwd) - 1):
            if fwd[i] < fwd[i + 1] - TOL:
                fails.append("the ladder is not monotone at year %d: %s"
                             % (i + 1, ["%.4f" % x for x in fwd]))
                break
        fr = rec.get("glide_fractions")
        if fr and we is not None and wt is not None:
            for i, (f, w) in enumerate(zip(fr, fwd)):
                if abs(w - (we - (we - wt) * f)) > 1e-8:
                    fails.append("year %d's forward rate does not sit on the glide the "
                                 "fractions describe" % (i + 1))
                    break

    # 4. ONE DATE, ONE PRICE OF TIME
    df = rec.get("discount_factors") or []
    tdf = rec.get("terminal_discount_factor")
    if df and tdf is not None and abs(tdf - df[-1]) > 1e-9:
        fails.append("the terminal value is brought home on a factor of %.6f while the last "
                     "explicit year's cash flow uses %.6f — a %.0f%% premium for relabelling "
                     "the same pound arriving on the same day."
                     % (tdf, df[-1], 100 * (tdf / df[-1] - 1)))
    if df:
        cum = 1.0
        for i, w in enumerate(fwd):
            cum /= (1 + w)
            if i < len(df) and abs(cum - df[i]) > 1e-9:
                fails.append("the discount factors are not the compounded forward rates at "
                             "year %d" % (i + 1))
                break

    # 5. the cost of debt: above its sovereign, and inside the gate
    kd = rec.get("kd_pretax")
    ki = rec.get("kd_integrity") or {}
    if kd is None:
        fails.append("no cost of debt recorded")
    else:
        if ki.get("pct_local_currency", 1.0) >= 0.999 and rf is not None and kd < rf - TOL:
            fails.append("the cost of debt %.4f sits BELOW the sovereign yield %.4f on an "
                         "all-local-currency book. A same-currency corporate cannot borrow "
                         "below its own sovereign." % (kd, rf))
        # THE SHAPE IS CHECKED BEFORE THE VALUES. A record carrying effective_rates
        # as a MAPPING of period to rate — which is the natural thing to write and
        # which the ARCC re-issue of 02-Sep-2026 wrote — used to reach eff[-1] and
        # die with a bare KeyError, and because this gate defers all printing until
        # its loop finishes, the crash produced NO OUTPUT AT ALL: not a failure
        # line, not even the count of studies examined. A CI log showed a traceback
        # and nothing else, and a run of this gate against a working tree read as
        # "no ARCC failures" when it had in fact examined nothing. That is the
        # empty-result-is-not-a-clean-result failure inside a gate written to
        # prevent it.
        #
        # A mapping is now ACCEPTED and ordered by its own keys, because a record
        # that names its periods is better evidence than a bare list, not worse.
        # Anything else REFUSES with a message naming the shape.
        eff_raw = ki.get("effective_rates")
        if isinstance(eff_raw, dict):
            eff = [eff_raw[k] for k in sorted(eff_raw)]
        elif isinstance(eff_raw, (list, tuple)):
            eff = list(eff_raw)
        elif eff_raw is None:
            eff = []
        else:
            eff = []
            fails.append("effective_rates is a %s; it must be a sequence of rates in "
                         "period order, or a mapping of period to rate."
                         % type(eff_raw).__name__)
        if any(not isinstance(x, (int, float)) for x in eff):
            fails.append("effective_rates carries a non-numeric entry: %r" % (eff,))
            eff = [x for x in eff if isinstance(x, (int, float))]
        why = (ki.get("effective_rate_unavailable") or "").strip()
        if len(eff) < 2 and not (len(why) >= 60 and "disclos" in why.lower()):
            fails.append("the cost-of-debt gate needs an independently computed effective rate "
                         "over at least two periods; %d recorded, and no adequate reason. A "
                         "disclosed contractual range's midpoint is not evidence, and 'not "
                         "available' is not a reason — name the disclosure that is missing."
                         % len(eff))
        elif len(eff) < 2:
            # stop-and-inform, honoured: the limitation is recorded and reported here so a
            # reader of the gate's output can see which studies carry it
            pass
        else:
            if abs(kd - eff[-1]) > 0.015 + TOL:
                fails.append("the adopted cost of debt is %.0fbp from the latest independently "
                             "computed effective rate, beyond the 150bp bound"
                             % (10000 * abs(kd - eff[-1])))
            if kd > max(eff) + 0.005 + TOL:
                fails.append("the adopted cost of debt exceeds the peak effective rate by more "
                             "than 50bp")
        if not ki.get("currency_source"):
            fails.append("the currency composition of the debt book is not sourced")
        if not ki.get("interest_bearing_note"):
            fails.append("the effective rate's denominator is not described. Dividing the "
                         "finance charge by a broader liabilities total understates the rate "
                         "by a multiple and manufactures a bias that looks like evidence.")

    # 6. both premium bases visible, one named central
    if rec.get("erp_basis") not in ("cds", "rating"):
        fails.append("no equity-risk-premium basis named as central; both are published and "
                     "one is named")
    if not (rec.get("sensitivity") or {}).get("other_basis"):
        fails.append("the alternative premium basis is not published beside the adopted one")

    return fails


def audit(sdir):
    tk = ticker_of(sdir)
    nf = numbers_file(sdir)
    if not nf:
        return "unreadable", "no committed numbers file"
    try:
        doc = json.load(open(nf, encoding="utf-8"))
    except Exception as e:                                   # noqa: BLE001
        return "unreadable", "%s will not parse: %s" % (os.path.basename(nf), e)
    rec = find_record(doc)
    if rec is None:
        return "no_record", "carries no cost-of-capital schedule record"
    fails = check_record(rec, tk)
    if fails:
        return "fail", "; ".join(fails)
    note = ""
    if (rec.get("kd_integrity") or {}).get("effective_rate_unavailable"):
        note = "   [cost-of-debt check unavailable on this disclosure, stated]"
    return "ok", ("%s, %.2f%% gliding to %.2f%%%s"
                  % (rec.get("market"), 100 * rec["wacc_exp"], 100 * rec["wacc_terminal"], note))


def main():
    prune = "--prune" in sys.argv
    if not os.path.exists(OUTSTANDING_FILE):
        print("FAIL — the ratchet list %s does not exist."
              % os.path.relpath(OUTSTANDING_FILE, ROOT))
        return 1
    out = json.load(open(OUTSTANDING_FILE, encoding="utf-8"))
    known = set(out["outstanding"])
    sdirs = studies()
    if not sdirs:
        print("FAIL — examined zero studies. An empty result is not a clean result [R-ENF-04].")
        return 1
    on_disk = {ticker_of(d) for d in sdirs}
    missing = sorted(known - on_disk)
    if missing:
        print("FAIL — the outstanding list names studies that do not exist on disk: %s"
              % ", ".join(missing))
        return 1

    ok, fixed, still, hard = [], [], [], []
    for d in sdirs:
        tk = ticker_of(d)
        try:
            state, detail = audit(d)
        except Exception as exc:
            # A GATE THAT CRASHES REPORTS NOTHING, AND NOTHING READS AS CLEAN.
            # Whatever is malformed in one study's record, the other twenty-three
            # are still owed an answer and the operator is owed a line naming the
            # study that broke.
            state, detail = 'ERROR', ('%s while auditing this record: %s'
                                      % (type(exc).__name__, exc))
        listed = tk in known
        if state == "ERROR":
            # A CRASH IS NEVER "ALLOWED FOR NOW". The ratchet forgives a study that
            # does not yet CONFORM; it cannot forgive a record this gate could not
            # read, because that is not a known shortfall, it is an unknown one.
            hard.append((tk, detail))
        elif state == "ok":
            (fixed if listed else ok).append((tk, detail))
        else:
            (still if listed else hard).append((tk, detail))

    print("studies examined: %d   conforming: %d   outstanding (allowed): %d"
          % (len(sdirs), len(ok) + len(fixed), len(still)))
    for tk, detail in sorted(ok):
        print("   %-12s %s" % (tk, detail))
    if fixed:
        print("\nNOW PASSING — remove from the outstanding list (%d):" % len(fixed))
        for tk, detail in fixed:
            print("   %-12s %s" % (tk, detail))
    if still:
        print("\nstill outstanding, allowed for now (%d):" % len(still))
        for tk, detail in still[:40]:
            print("   %-12s %s" % (tk, detail[:150]))
    if hard:
        print("\nFAIL — not on the outstanding list and not conforming (%d):" % len(hard))
        for tk, detail in hard:
            print("   %-12s %s" % (tk, detail[:400]))
    if prune:
        out["outstanding"] = sorted(known - {tk for tk, _ in fixed})
        json.dump(out, open(OUTSTANDING_FILE, "w", encoding="utf-8"), indent=1)
        print("\npruned — now %d entries" % len(out["outstanding"]))
        return 0
    if hard:
        return 1
    print("\nOK — no new violations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
