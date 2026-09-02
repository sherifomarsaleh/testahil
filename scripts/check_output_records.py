"""THE STUDY AUDITS ITS OWN ANSWER, AND THE AUDIT IS CHECKED FROM OUTSIDE.

[R-ENF-05], enforced per [R-ENF-01].

Two instruments, both aimed at the same failure: a house that leans in one
direction and cannot see it.

THE REVERSE READ. Every study states what it believes; almost none states what
the PRICE believes, and the two are the same model read backwards. A reverse
DCF — the growth, margin, conversion rate or discount rate the traded price
implies under the study's own drivers — turns a disagreement into a measurable
one: not "we are 28% below" but "the price is paying for a conversion rate of
7.9% and we forecast 8.7%". The hard part is keeping it OUT of the model, so it
lives in its own file and this gate refuses any study whose builders read that
file back in — a rate solved from a price and re-entering the valuation is the
reverse-engineered terminal the protocol prohibits, arriving through a side door.

THE SIGN TEST. Any single contested choice in a valuation is defensible; what is
not defensible is a study that resolves EVERY one of them in the same direction
and never notices. Each is recorded with both framings' values and the side
adopted, and a binomial sign test is printed. A study landing them all one way
at p < 0.05 is FLAGGED, not failed: a company can genuinely deserve a consistent
read. What it may not do is go unmeasured.

Population-anchored [R-ENF-04], ratcheted [R-ENF-02].

    python3 scripts/check_output_records.py
    python3 scripts/check_output_records.py --prune
"""
import glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
sys.path.insert(0, ENGINE)

OUTSTANDING_FILE = os.path.join(ENGINE, "build_depth_audit", "output_outstanding.json")


def studies():
    return sorted(glob.glob(os.path.join(ENGINE, "*_study")))


def ticker_of(sdir):
    return os.path.basename(sdir)[: -len("_study")].upper()


def audit(sdir):
    import research_protocol as RP

    tk = ticker_of(sdir)
    dp = os.path.join(sdir, "diagnostics.json")
    cp = os.path.join(sdir, "contested_judgements.json")
    if not os.path.exists(dp) and not os.path.exists(cp):
        return "no_record", "carries neither a reverse read nor a contested-judgement record"
    if not os.path.exists(dp):
        return "fail", "carries contested judgements but no reverse read"
    if not os.path.exists(cp):
        return "fail", "carries a reverse read but no contested-judgement record"
    try:
        diag = json.load(open(dp, encoding="utf-8"))
        cj = json.load(open(cp, encoding="utf-8"))
    except Exception as e:                                   # noqa: BLE001
        return "fail", "a record will not parse: %s" % e
    try:
        r = RP.assert_reverse_dcf(diag, sdir, ticker=tk)
        c = RP.assert_contested_judgements(cj, ticker=tk)
    except AssertionError as e:
        return "fail", str(e).replace("\n", " ")
    except Exception as e:                                   # noqa: BLE001
        return "fail", "%s: %s" % (type(e).__name__, e)
    flag = "   FLAGGED: every material judgement resolved one way" if c["flag"] else ""
    return "ok", ("price implies %s of %s against the study's %s; %d judgements, "
                  "%d material, sign test p=%s%s"
                  % (r["quantity"][:40], _fmt(r["implied"]), _fmt(r["study"]),
                     c["judgements"], c["material"],
                     "n/a" if c["sign_test_p"] is None else "%.2f" % c["sign_test_p"], flag))


def _fmt(x):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return str(x)
    return "%.2f%%" % (100 * x) if abs(x) < 1 else "%.2f" % x


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
        print("FAIL — examined zero studies. An empty result is not a clean result "
              "[R-ENF-04].")
        return 1
    missing = sorted(known - {ticker_of(d) for d in sdirs})
    if missing:
        print("FAIL — the outstanding list names studies that do not exist on disk: %s"
              % ", ".join(missing))
        return 1

    ok, fixed, still, hard = [], [], [], []
    for d in sdirs:
        tk = ticker_of(d)
        state, detail = audit(d)
        listed = tk in known
        if state == "ok":
            (fixed if listed else ok).append((tk, detail))
        else:
            (still if listed else hard).append((tk, detail))

    print("studies examined: %d   conforming: %d   outstanding (allowed): %d"
          % (len(sdirs), len(ok) + len(fixed), len(still)))
    for tk, detail in sorted(ok) + sorted(fixed):
        print("   %-12s %s" % (tk, detail))
    if still:
        print("\nstill outstanding, allowed for now (%d)" % len(still))
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
