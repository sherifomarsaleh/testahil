#!/usr/bin/env python3
"""Negative control for scripts/check_frozen_escalator.py.

A check nobody has seen fail is not evidence. Every case below copies the
repository into a sandbox, injects one condition, runs the gate there and asserts
the colour it comes back.

EVERY MUTATION ASSERTS THAT IT LANDED. That clause is not decoration: this
repository has caught a negative control passing a fixture that never injected
its condition four times, and one of this session's own measurements did it again
(a cost-line mutation that negated a value, produced non-positive cells the log
score dropped, and reported "no change"). A case whose mutation did not land is a
case that proves the gate is UNCHANGED, which is the opposite of what a control
is for.

THE CLEAN CASES ARE THE HALF THAT MATTERS HERE, and one of them is the gate's own
history: the FIRST draft doubled a named function and flagged EGCH's revenue as
frozen, when EGCH's revenue moves through a currency path derived from the CPI
differential read straight off its own table. That case is kept as a clean case
precisely because an earlier draft failed it.

    python3 scripts/check_frozen_escalator_negative_control.py
"""
import json, os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join("scripts", "check_frozen_escalator.py")
RATCHET = os.path.join("engine", "build_depth_audit", "frozen_outstanding.json")
EXPECTED_CASES = 14        # asserted against the declared constant


def sandbox():
    d = tempfile.mkdtemp(prefix="frozen-nc-")
    for sub in ("scripts", "engine"):
        shutil.copytree(os.path.join(ROOT, sub), os.path.join(d, sub),
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc",
                                                      "*.docx", "*.xlsx", "*.pdf"))
    return d


def run(d):
    r = subprocess.run([sys.executable, GATE], cwd=d, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)


def _read(path):
    with open(path) as f:
        return f.read()


def _write(path, text):
    with open(path, "w") as f:
        f.write(text)


# ---------------------------------------------------------------- mutations
def m_none(d):
    return True


def m_empty_ratchet(d):
    p = os.path.join(d, RATCHET)
    before = _read(p)
    j = json.loads(before)
    j["outstanding"] = []
    _write(p, json.dumps(j, indent=1))
    return _read(p) != before


def m_ratchet_keyed_by_ticker(d):
    """The ratchet re-keyed by TICKER instead of TICKER:LINE — a one-line edit
    anybody could make in good faith, and the one that matters: it would forgive
    AMOC on every line it ever acquires, not just the one it was seeded for. The
    gate must still refuse AMOC's frozen net_sales, because a bare ticker no
    longer matches any key."""
    p = os.path.join(d, RATCHET)
    j = json.loads(_read(p))
    j["outstanding"] = sorted({k.split(":")[0] for k in j["outstanding"]})
    _write(p, json.dumps(j, indent=1))
    return all(":" not in k for k in json.loads(_read(p))["outstanding"])


def m_declare_empty_reason(d):
    m_empty_ratchet(d)
    p = os.path.join(d, "engine", "amoc_walkforward", "frozen_escalators.json")
    _write(p, json.dumps({"frozen": {"net_sales": ""}}, indent=1))
    return os.path.exists(p)


def m_declare_bad_reason(d):
    m_empty_ratchet(d)
    p = os.path.join(d, "engine", "amoc_walkforward", "frozen_escalators.json")
    _write(p, json.dumps({"frozen": {"net_sales": "we could not forecast it"}}, indent=1))
    return os.path.exists(p)


def m_declare_good_reason(d):
    m_empty_ratchet(d)
    # every OTHER seeded line must still be declared, or this case goes red for
    # a reason that is not the one it is testing.
    for tk, fn, ln in (("arcc", "finance_escalators", "finance_costs"),
                       ("tmgh", "finance_escalators", "finance_cost"),
                       ("phdc", "finance_escalators", "is.finance_cost")):
        q = os.path.join(d, "engine", "%s_walkforward" % tk, "frozen_escalators.json")
        _write(q, json.dumps({"frozen": {ln: "contractually_fixed"}}, indent=1))
    p = os.path.join(d, "engine", "amoc_walkforward", "frozen_escalators.json")
    _write(p, json.dumps({"frozen": {"net_sales": "contractually_fixed"}}, indent=1))
    return os.path.exists(p)


def m_freeze_arcc(d):
    """ARCC's revenue cut off from every inflation path. A NEW frozen line on a
    run that is not on the ratchet must go red even though AMOC's is allowed."""
    p = os.path.join(d, "engine", "arcc_walkforward", "bottom_up.py")
    s = _read(p)
    old = "    return (1 + cpi(o)) ** h, (1 + fx_dep(o)) ** h, 1.0"
    if old not in s:
        return False
    _write(p, s.replace(old, "    return 1.0, 1.0, 1.0", 1))
    return "return 1.0, 1.0, 1.0" in _read(p)


def m_unprobeable(d):
    """A run whose projector will not import. Must be RED, never skipped."""
    p = os.path.join(d, "engine", "egch_walkforward", "bottom_up.py")
    s = _read(p)
    _write(p, "raise RuntimeError('injected: this module does not import')\n" + s)
    return _read(p).startswith("raise RuntimeError")


def m_freeze_phdc(d):
    """PHDC's cost line cut off from the panel inflation it reads. A run driven
    through an ADAPTER must be caught exactly as one driven directly -- otherwise
    the adapters are a hole rather than a coverage extension."""
    p = os.path.join(d, "engine", "phdc_walkforward", "bottom_up.py")
    s = _read(p)
    old = "            cogs = cpu0 * infl * deliveries"
    if old not in s:
        return False
    _write(p, s.replace(old, "            cogs = cpu0 * deliveries", 1))
    return "cogs = cpu0 * deliveries" in _read(p)


def m_freeze_tmgh(d):
    """TMGH's development cost cut off from the inflation it is handed."""
    p = os.path.join(d, "engine", "tmgh_walkforward", "bottom_up.py")
    s = _read(p)
    old = "def project(A, cpi, urb, o, horizons=HORIZONS, foresight=False):"
    if old not in s:
        return False
    _write(p, s.replace(old, old + "\n    cpi = {y: 0.0 for y in cpi}", 1))
    return "cpi = {y: 0.0 for y in cpi}" in _read(p)


def m_no_directories(d):
    moved = 0
    for n in ("amoc", "egch", "arcc", "tmgh", "phdc"):
        src = os.path.join(d, "engine", "%s_walkforward" % n)
        if os.path.isdir(src):
            shutil.move(src, src + "_moved")
            moved += 1
    return moved == 5


def m_no_lines_probed(d):
    """Directories present, every probed line renamed so nothing can be probed.
    The distinction an absent answer hides behind [R-ENF-04].

    THE MUTATION IS BY SHAPE, NOT BY LITERAL. An earlier version matched each
    RUNS tuple as an exact string and stopped landing the moment a line was added
    to those tuples — it reported MUTATION DID NOT LAND, which is the control
    working, and it would have reported a false green had the landing assertion
    not been there."""
    p = os.path.join(d, GATE)
    s = _read(p)
    head = s.index("RUNS = [")
    tail = s.index("]", s.index("\"phdc\")", head)) + 1
    block = s[head:tail]
    out, n = [], 0
    for line in block.splitlines():
        i, j = line.find("["), line.rfind("]")
        if i != -1 and j > i and '"' in line[i:j]:
            line = line[:i] + '["no_such_line"]' + line[j + 1:]
            n += 1
        out.append(line)
    if n < 5:
        return False
    _write(p, s[:head] + "\n".join(out) + s[tail:])
    return _read(p).count("no_such_line") >= 5


def m_index_only(d):
    """A run wired ONLY to a cpi INDEX, not a rate. Scaling every year of an index
    by the same constant leaves every RATIO unchanged, so a gate bumping by a flat
    factor would call this frozen when it is wired. The gate's rising factor is
    what closes it; this case is what proves the closure."""
    p = os.path.join(d, "engine", "arcc_walkforward", "bottom_up.py")
    s = _read(p)
    old = "def cpi(fy):"
    if old not in s:
        return False
    inject = ('def cpi(fy):\n'
              '    a = _m("cpi_index", "FY%d" % (_y(fy) - 1))\n'
              '    b = _m("cpi_index", fy)\n'
              '    if a and b:\n'
              '        return b / a - 1.0\n')
    s = s.replace(old + '\n    """Egyptian annual consumer price inflation, as a rate."""\n',
                  inject, 1)
    _write(p, s)
    return "cpi_index" in _read(p).split("def fx_dep")[0]


CASES = [
    # (name, mutation, expect_red)
    ("AMOC as it stands, ratchet emptied", m_empty_ratchet, True),
    ("a ratchet re-keyed by ticker, not ticker:line", m_ratchet_keyed_by_ticker, True),
    ("a declaration with an EMPTY reason", m_declare_empty_reason, True),
    ("a reason not on the closed list", m_declare_bad_reason, True),
    ("a NEW frozen run beside a ratcheted one", m_freeze_arcc, True),
    ("a frozen line on a run driven by an ADAPTER (PHDC)", m_freeze_phdc, True),
    ("a frozen line on a run driven by an ADAPTER (TMGH)", m_freeze_tmgh, True),
    ("a run whose projector will not import", m_unprobeable, True),
    ("no run directories at all", m_no_directories, True),
    ("directories present, zero lines probed", m_no_lines_probed, True),
    ("the repository as it stands", m_none, False),
    ("a frozen line with a reason on the list", m_declare_good_reason, False),
    ("EGCH, wired through the currency path", m_none, False),
    ("a run wired only to a cpi INDEX", m_index_only, False),
]


def main():
    if len(CASES) != EXPECTED_CASES:
        print("FAIL: %d cases against a declared %d — a case was added or deleted "
              "without the constant moving." % (len(CASES), EXPECTED_CASES))
        return 1
    bad = 0
    for name, mut, expect_red in CASES:
        d = sandbox()
        try:
            landed = mut(d)
            if not landed:
                print("FAIL  %-45s MUTATION DID NOT LAND" % name)
                bad += 1
                continue
            code, out = run(d)
            red = code != 0
            ok = (red == expect_red)
            print("%-5s %-45s expected %-5s got %s"
                  % ("ok" if ok else "FAIL", name,
                     "RED" if expect_red else "green", "RED" if red else "green"))
            if not ok:
                bad += 1
                print("      %s" % out.strip().replace("\n", "\n      ")[:600])
        finally:
            shutil.rmtree(d, ignore_errors=True)
    print()
    if bad:
        print("NEGATIVE CONTROL FAILED — %d of %d case(s)" % (bad, len(CASES)))
        return 1
    print("negative control OK — %d cases, %d red and %d clean"
          % (len(CASES), sum(1 for _, _, r in CASES if r),
             sum(1 for _, _, r in CASES if not r)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
