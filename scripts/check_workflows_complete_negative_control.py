"""Negative control for check_workflows_complete.  [R-ENF-01]

Every condition the gate refuses, reinjected into a sandbox, and the clean cases it must
not fire on. EVERY MUTATION ASSERTS THAT IT LANDED and the case count is asserted against
a declared constant.

THE CASE THAT MATTERS IS THE SEVENTH. This workflow lists script names in TWO places: a
`paths:` block, so that editing one triggers the job, and a `run:` line, which actually
executes it. A name in the first and not the second reads identical to being covered while
running nothing at all — and that is not hypothetical, it is how a typed list hides an
omission. If this gate ever stops telling the two apart it goes green on a repository that
checks nothing, so the case is kept whatever else changes.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "engine"))
import sandbox_reclaim as SBX       # noqa: E402

TARGET = os.path.join(HERE, "check_workflows_complete.py")
RED_EXPECTED = 7
CLEAN_EXPECTED = 3

WF = """name: t
on: [push]
jobs:
  t:
    runs-on: ubuntu-latest
    steps:
%s
"""


def _sandbox(gate_names, run_names, paths_names=(), excluded=None, wf_dir=True,
             second_workflow=None):
    tmp = SBX.make("wfc_nc_")
    os.makedirs(os.path.join(tmp, "scripts"))
    os.makedirs(os.path.join(tmp, "engine"))
    shutil.copy(os.path.join(ROOT, "engine", "sandbox_reclaim.py"),
                os.path.join(tmp, "engine", "sandbox_reclaim.py"))
    body = open(TARGET, encoding="utf-8").read()
    if excluded is not None:
        old = body[body.index("EXCLUDED = {"):body.index("}\n", body.index("EXCLUDED = {")) + 2]
        body = body.replace(old, "EXCLUDED = %r\n" % (excluded,))
    open(os.path.join(tmp, "scripts", "check_workflows_complete.py"), "w").write(body)
    for n in gate_names:
        open(os.path.join(tmp, "scripts", n), "w").write("# gate\n")
    if wf_dir:
        d = os.path.join(tmp, ".github", "workflows")
        os.makedirs(d)
        # THE SANDBOX CARRIES THE GATE ITSELF, so in a miniature repository the gate is
        # one of the gates — and in the real one it IS invoked. Leaving it out of every
        # fixture made all three clean cases go red on the gate finding itself, which is
        # the fixture being wrong rather than the gate. It is added wherever the case
        # runs anything at all, and left out of the two cases whose whole subject is that
        # nothing runs.
        run_names = list(run_names) + ["check_workflows_complete.py"] if run_names \
            else list(run_names)
        steps = "".join("      - name: %s\n        run: python3 scripts/%s\n" % (n, n)
                        for n in run_names)
        paths = "".join("      - 'scripts/%s'\n" % n for n in paths_names)
        open(os.path.join(d, "a.yml"), "w").write((("    paths:\n" + paths) if paths else "")
                                                  + WF % (steps or "      - run: true\n"))
        if second_workflow:
            s = "".join("      - name: %s\n        run: python3 scripts/%s\n" % (n, n)
                        for n in second_workflow)
            open(os.path.join(d, "b.yml"), "w").write(WF % s)
    return tmp


def case(name, want_red, kw, landed, results):
    tmp = _sandbox(**kw)
    try:
        ok_land, why = landed(tmp)
        if not ok_land:
            print("  MISS  %-58s FIXTURE DID NOT LAND: %s" % (name[:58], why))
            results.append(False)
            return
        r = subprocess.run([sys.executable,
                            os.path.join(tmp, "scripts", "check_workflows_complete.py")],
                           capture_output=True, text=True, timeout=300, cwd=tmp)
        red = r.returncode != 0
        ok = (red == want_red)
        results.append(ok)
        print("  %-5s %-58s %s" % ("ok" if ok else "MISS", name[:58],
                                   "RED" if red else "green"))
        if not ok:
            for l in (r.stdout + r.stderr).strip().splitlines()[-4:]:
                print("        " + l[:140])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    print("NEGATIVE CONTROL - check_workflows_complete  [R-ENF-01]")
    res = []
    G = ["check_one.py", "check_two.py"]

    def files_there(tmp, names):
        for n in names:
            if not os.path.exists(os.path.join(tmp, "scripts", n)):
                return False, "%s absent" % n
        return True, ""

    case("a gate on disk that runs in no workflow", True,
         dict(gate_names=G, run_names=["check_one.py"], excluded={}),
         lambda t: files_there(t, G), res)

    case("ZERO gates on disk [R-ENF-04]", True,
         dict(gate_names=[], run_names=[], excluded={}),
         lambda t: (not os.path.exists(os.path.join(t, "scripts", "check_one.py")),
                    "a gate survived"), res)

    case("no workflow directory at all", True,
         dict(gate_names=G, run_names=[], wf_dir=False, excluded={}),
         lambda t: (not os.path.isdir(os.path.join(t, ".github")),
                    "the workflow directory survived"), res)

    case("ZERO invocations read across the workflows [R-ENF-04]", True,
         dict(gate_names=G, run_names=[], excluded={}),
         lambda t: files_there(t, G), res)

    case("an exclusion naming a file that is not on disk", True,
         dict(gate_names=G, run_names=G, excluded={"check_ghost.py": "a reason"}),
         lambda t: (not os.path.exists(os.path.join(t, "scripts", "check_ghost.py")),
                    "the ghost exists"), res)

    case("an exclusion with an EMPTY reason", True,
         dict(gate_names=G, run_names=G, excluded={"check_two.py": "   "}),
         lambda t: files_there(t, G), res)

    # THE DECISIVE ONE: listed under `paths:` so editing it triggers the job, and never
    # run. Identical to coverage on the page, and it executes nothing.
    case("a gate named only under paths: and never run", True,
         dict(gate_names=G, run_names=["check_one.py"], paths_names=["check_two.py"],
              excluded={}),
         lambda t: files_there(t, G), res)

    case("CLEAN - every gate invoked", False,
         dict(gate_names=G, run_names=G, excluded={}),
         lambda t: files_there(t, G), res)

    case("CLEAN - one excluded with a real reason, and present", False,
         dict(gate_names=G, run_names=["check_one.py"],
              excluded={"check_two.py": "its subject is the run rather than the book"}),
         lambda t: files_there(t, G), res)

    case("CLEAN - invoked from a SECOND workflow file", False,
         dict(gate_names=G, run_names=["check_one.py"],
              second_workflow=["check_two.py"], excluded={}),
         lambda t: (os.path.exists(os.path.join(t, ".github", "workflows", "b.yml")),
                    "the second workflow is absent"), res)

    assert len(res) == RED_EXPECTED + CLEAN_EXPECTED, (
        "cases ran %d, declared %d" % (len(res), RED_EXPECTED + CLEAN_EXPECTED))
    print("\n%d of %d conditions behaved as the gate claims." % (sum(res), len(res)))
    if all(res):
        print("OK - a gate that runs nowhere is refused, and one that runs somewhere is "
              "not.")
        return 0
    print("FAILED - the gate does not behave as the rule says.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
