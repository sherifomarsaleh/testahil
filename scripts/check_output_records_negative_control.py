"""A CHECK NOBODY HAS SEEN FAIL IS NOT EVIDENCE.

Reinjects every condition scripts/check_output_records.py claims to catch.

  1. NO REVERSE READ where contested judgements exist, and 2. the reverse.
  3. A REVERSE READ WITH NO IMPLIED QUANTITY — a file that exists and says nothing.
  4. THE DIAGNOSTIC READ BACK INTO THE MODEL — a builder importing diagnostics.json,
     which is a price-derived quantity re-entering the valuation through a side door.
  5. A CONTESTED JUDGEMENT WITH NO REASON — which side was taken, but not why.
  6. A JUDGEMENT MISSING ITS OTHER FRAMING — the dual-framing rule with one framing.
  7. NO CONTESTED JUDGEMENTS AT ALL — a valuation nobody looked at hard enough.
  8. UNPARSEABLE / 9. NO RECORD, NOT LISTED / 10. EMPTY POPULATION.

And the clean cases, including a study whose sign test FLAGS: the flag is
information, not a failure, and a gate that failed on it would push studies to
resolve their judgements inconsistently to stay green.

    python3 scripts/check_output_records_negative_control.py
"""
import json, os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join("scripts", "check_output_records.py")

DIAG = {"ticker": "NCO", "spot": 10.0,
        "implied": {"quantity": "the cash conversion the price is paying for",
                    "value": 0.079, "study_value": 0.087,
                    "solved_on": "this study's own model, varying only conversion"}}
CJ = {"ticker": "NCO", "judgements": [
    {"name": "conversion period", "adopted": "14 years", "alternative": "10 years",
     "value_adopted": 98.0, "value_alternative": 50.0, "why": "the company's own rate"},
    {"name": "minority basis", "adopted": "value share", "alternative": "book",
     "value_adopted": 98.0, "value_alternative": 87.0, "why": "the standing rule"},
    {"name": "premium basis", "adopted": "swap", "alternative": "rating",
     "value_adopted": 90.0, "value_alternative": 98.0, "why": "live market pricing"},
]}


def sandbox():
    tmp = tempfile.mkdtemp(prefix="out_nc_")
    os.makedirs(os.path.join(tmp, "engine", "build_depth_audit"))
    os.makedirs(os.path.join(tmp, "scripts"))
    for f in ("research_protocol.py", "macro_path.py"):
        shutil.copy(os.path.join(ROOT, "engine", f), os.path.join(tmp, "engine", f))
    shutil.copytree(os.path.join(ROOT, "engine", "macro_paths"),
                    os.path.join(tmp, "engine", "macro_paths"))
    shutil.copy(os.path.join(ROOT, "scripts", "check_output_records.py"),
                os.path.join(tmp, "scripts", "check_output_records.py"))
    return tmp


def put(tmp, diag=None, cj=None, builder=None, raw=None):
    d = os.path.join(tmp, "engine", "nco_study")
    os.makedirs(d, exist_ok=True)
    if raw is not None:
        open(os.path.join(d, "diagnostics.json"), "w").write(raw)
    elif diag is not None:
        json.dump(diag, open(os.path.join(d, "diagnostics.json"), "w"), indent=1)
    if cj is not None:
        json.dump(cj, open(os.path.join(d, "contested_judgements.json"), "w"), indent=1)
    if builder:
        open(os.path.join(d, "compute.py"), "w").write(builder)


def put_list(tmp, tickers):
    json.dump({"why": "negative control", "adopted": "2026-09-02",
               "outstanding": sorted(tickers)},
              open(os.path.join(tmp, "engine", "build_depth_audit",
                                "output_outstanding.json"), "w"), indent=1)


def case(name, build, expect_red, results):
    tmp = sandbox()
    try:
        build(tmp)
        r = subprocess.run([sys.executable, GATE], cwd=tmp, capture_output=True, text=True)
        out = (r.stdout + r.stderr).strip()
        red = r.returncode != 0
        ok = red == expect_red
        results.append((name, ok, r.returncode, out.splitlines()[-1] if out else ""))
        if not ok:
            print("\n---- %s ----\n%s" % (name, out))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    R = []
    import copy

    case("1 contested judgements, no reverse read",
         lambda t: (put(t, cj=CJ), put_list(t, [])), True, R)
    case("2 reverse read, no contested judgements",
         lambda t: (put(t, diag=DIAG), put_list(t, [])), True, R)

    d3 = copy.deepcopy(DIAG); d3.pop("implied")
    case("3 reverse read with no implied quantity",
         lambda t: (put(t, diag=d3, cj=CJ), put_list(t, [])), True, R)

    case("4 a builder reads the diagnostic back into the model",
         lambda t: (put(t, diag=DIAG, cj=CJ,
                        builder="import json\nD = json.load(open('diagnostics.json'))\n"
                                "WACC = D['implied']['value']\n"), put_list(t, [])), True, R)

    # THE CASE THE CONTAINMENT CHECK WAS RE-POINTED FOR, and it must stay GREEN.
    # `diagnostics.json` is not a reserved name: every statement walk-forward
    # writes one holding its own per-driver error diagnostics, and a study that
    # consumes THAT is doing what [R-FCAL-01] asks — carrying its calibration into
    # the delivered document. EGCH's compute.py opens
    # ../egch_walkforward/diagnostics.json and was failed for it. A check firing on
    # work that is right is never answered by widening it; it is answered by
    # pointing it at the right file, and this case is what proves the re-pointing
    # did not simply switch it off — case 4 above, the real leak, still goes red.
    case("4b a builder reads the WALK-FORWARD's diagnostics, not the reverse read",
         lambda t: (put(t, diag=DIAG, cj=CJ,
                        builder="import json, os\n"
                                "_WF = os.path.join(HERE, '..', 'nco_walkforward')\n"
                                "D = json.load(open(os.path.join(_WF, "
                                "'diagnostics.json')))\n"
                                "BIAS = D.get('bias')\n"), put_list(t, [])), False, R)

    c5 = copy.deepcopy(CJ); c5["judgements"][1].pop("why")
    case("5 a judgement with no reason", lambda t: (put(t, diag=DIAG, cj=c5), put_list(t, [])),
         True, R)
    c6 = copy.deepcopy(CJ); c6["judgements"][0].pop("value_alternative")
    case("6 a judgement missing its other framing",
         lambda t: (put(t, diag=DIAG, cj=c6), put_list(t, [])), True, R)
    case("7 no contested judgements at all",
         lambda t: (put(t, diag=DIAG, cj={"judgements": []}), put_list(t, [])), True, R)
    case("8 a record will not parse",
         lambda t: (put(t, raw="{nope", cj=CJ), put_list(t, [])), True, R)

    def b9(t):
        d = os.path.join(t, "engine", "nco_study"); os.makedirs(d, exist_ok=True)
        json.dump({"meta": {}}, open(os.path.join(d, "study_numbers.json"), "w"))
        put_list(t, [])
    case("9 new study, no records, not listed", b9, True, R)
    case("10 empty population", lambda t: put_list(t, ["GHOST"]), True, R)

    case("clean: both records present and sound",
         lambda t: (put(t, diag=DIAG, cj=CJ), put_list(t, [])), False, R)

    # THE FLAG IS INFORMATION, NOT A FAILURE. A gate that went red here would push
    # studies to resolve their judgements inconsistently in order to stay green,
    # which is the opposite of what this measures.
    cf = copy.deepcopy(CJ)
    for j in cf["judgements"]:
        j["value_adopted"], j["value_alternative"] = 98.0, 50.0
    cf["judgements"].append({"name": "fourth", "adopted": "a", "alternative": "b",
                             "value_adopted": 98.0, "value_alternative": 50.0,
                             "why": "stated"})
    cf["judgements"].append({"name": "fifth", "adopted": "a", "alternative": "b",
                             "value_adopted": 98.0, "value_alternative": 50.0,
                             "why": "stated"})
    case("clean: every judgement one way — FLAGGED, not failed",
         lambda t: (put(t, diag=DIAG, cj=cf), put_list(t, [])), False, R)

    def b_listed(t):
        put(t, cj=CJ); put_list(t, ["NCO"])
    case("clean: a listed outstanding study", b_listed, False, R)

    print("\nNEGATIVE CONTROL — scripts/check_output_records.py")
    for name, ok, rc, last in R:
        print("  %-48s %-4s exit %d   %s" % (name, "ok" if ok else "MISS", rc, last[:56]))
    bad = [n for n, ok, _, _ in R if not ok]
    if bad:
        print("\nFAILED on: %s" % ", ".join(bad)); return 1
    print("\nAll %d conditions behave as claimed." % len(R))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
