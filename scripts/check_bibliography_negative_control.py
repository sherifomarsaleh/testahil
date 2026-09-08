"""Negative control for check_bibliography.  [R-ENF-01]

Reinjects every condition the gate refuses and the clean cases it must not fire on.
EVERY MUTATION ASSERTS THAT IT LANDED, and the case COUNT is asserted against a declared
constant.

THE CLEAN HALF IS THE WHOLE ARGUMENT HERE. The bibliography artefact ships under THREE
names in this book, and one study's file carries the company's other name rather than
its ticker. A control testing only the obvious convention would prove the gate works on
the twenty-one studies that never needed checking and say nothing about the three that
would have been wrongly condemned — which is exactly what the author's first probe did,
reporting two breaches where there is one.
"""
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TARGET = os.path.join(HERE, "check_bibliography.py")
SRC_ENGINE = os.path.join(ROOT, "engine")

CASES_EXPECTED = 10
RED_EXPECTED = 5
CLEAN_EXPECTED = 5


def _sandbox():
    """Filenames are all this gate reads, so the fixtures are empty files by design."""
    tmp = tempfile.mkdtemp(prefix="bib-nc-")
    eng = os.path.join(tmp, "engine")
    os.makedirs(os.path.join(eng, "build_depth_audit"))
    rat = os.path.join(SRC_ENGINE, "build_depth_audit",
                       "bibliography_outstanding.json")
    if os.path.exists(rat):
        shutil.copy(rat, os.path.join(eng, "build_depth_audit"))
    for d in sorted(glob.glob(os.path.join(SRC_ENGINE, "*_study"))):
        dst = os.path.join(eng, os.path.basename(d))
        os.makedirs(dst)
        for n in os.listdir(d):
            if n.lower().endswith(".docx"):
                open(os.path.join(dst, n), "w").close()
    os.makedirs(os.path.join(tmp, "scripts"))
    shutil.copy(TARGET, os.path.join(tmp, "scripts", "check_bibliography.py"))
    return tmp


def _run(tmp):
    r = subprocess.run([sys.executable,
                        os.path.join(tmp, "scripts", "check_bibliography.py")],
                       capture_output=True, text=True, timeout=300)
    return r.returncode, r.stdout + r.stderr


def _dir(tmp, study):
    return os.path.join(tmp, "engine", study)


def _biblio_of(tmp, study):
    import re
    B = re.compile(r'(bibliograph|source[_ ]register|_sources_)', re.I)
    return [n for n in os.listdir(_dir(tmp, study)) if B.search(n)]


# ------------------------------------------------------------------ red cases

def biblio_removed(tmp):
    """A compliant study loses its bibliography — the defect the gate exists for."""
    b = _biblio_of(tmp, "adnocls_study")
    assert b, "MUTATION DID NOT LAND: nothing to remove"
    for n in b:
        os.remove(os.path.join(_dir(tmp, "adnocls_study"), n))
    assert not _biblio_of(tmp, "adnocls_study"), "MUTATION DID NOT LAND"
    return "no standalone bibliography"


def biblio_removed_alt_name(tmp):
    """The SAME defect on a study whose artefact uses one of the other two names."""
    b = _biblio_of(tmp, "elec_study")
    assert b and 'ource' in b[0], "fixture: elec does not carry the alternate name"
    for n in b:
        os.remove(os.path.join(_dir(tmp, "elec_study"), n))
    assert not _biblio_of(tmp, "elec_study"), "MUTATION DID NOT LAND"
    return "no standalone bibliography"


def phantom_ratchet(tmp):
    p = os.path.join(tmp, "engine", "build_depth_audit",
                     "bibliography_outstanding.json")
    o = json.load(open(p)) if os.path.exists(p) else {"outstanding": []}
    o["outstanding"] = list(o.get("outstanding", [])) + ["NOSUCHNAME"]
    json.dump(o, open(p, "w"))
    assert "NOSUCHNAME" in json.load(open(p))["outstanding"], "MUTATION DID NOT LAND"
    return "anchored on nothing"


def no_study_documents(tmp):
    """The study-document matcher stops matching. Reads exactly like a clean book."""
    hit = 0
    for d in glob.glob(os.path.join(tmp, "engine", "*_study")):
        for n in os.listdir(d):
            if 'valuation_study' in n.lower():
                os.rename(os.path.join(d, n),
                          os.path.join(d, n.replace('Valuation_Study', 'Renamed')))
                hit += 1
    assert hit > 0, "MUTATION DID NOT LAND: no study documents were renamed"
    return "ZERO delivered study documents"


def emptied_population(tmp):
    dirs = glob.glob(os.path.join(tmp, "engine", "*_study"))
    assert dirs, "MUTATION DID NOT LAND"
    for d in dirs:
        shutil.rmtree(d)
    return "ZERO study directories"


# ---------------------------------------------------------------- clean cases

def as_it_stands(tmp):
    return None


def alternate_name_source_register(tmp):
    """ELEC ships a Source_Register. It is compliant and must NOT fire."""
    b = _biblio_of(tmp, "elec_study")
    assert b and 'ource_register' in b[0].lower(), "fixture: not the Source_Register case"
    return None


def alternate_name_sources(tmp):
    """TMGH ships a _Sources_ file. Also compliant."""
    b = _biblio_of(tmp, "tmgh_study")
    assert b and '_sources_' in b[0].lower(), "fixture: not the Sources case"
    return None


def company_named_not_ticker_named(tmp):
    """PHAR's bibliography carries the COMPANY's other name, not the ticker.

    A gate keyed on the ticker prefix would condemn a compliant study, which is the
    second way the author's own probes got this wrong.
    """
    b = _biblio_of(tmp, "phar_study")
    assert b, "fixture: phar carries no bibliography"
    assert not b[0].upper().startswith("PHAR"), \
        "fixture: this file IS ticker-prefixed, so it proves nothing"
    return None


def ratcheted_breach_stays_green(tmp):
    """The known breach is on the list and must not turn the build red."""
    p = os.path.join(tmp, "engine", "build_depth_audit",
                     "bibliography_outstanding.json")
    o = json.load(open(p))
    assert o.get("outstanding"), "fixture: the ratchet is empty, so this proves nothing"
    tk = o["outstanding"][0]
    assert not _biblio_of(tmp, tk.lower() + "_study"), \
        "fixture: the ratcheted study is not actually breaching"
    return None


RED = [
    ("a compliant study loses its bibliography", biblio_removed),
    ("the same defect under an alternate artefact name", biblio_removed_alt_name),
    ("a ratchet naming a study not on disk", phantom_ratchet),
    ("the study-document matcher stops matching", no_study_documents),
    ("an emptied population", emptied_population),
]
CLEAN = [
    ("the repository as it stands", as_it_stands),
    ("an artefact named Source_Register", alternate_name_source_register),
    ("an artefact named Sources", alternate_name_sources),
    ("an artefact named for the company, not the ticker", company_named_not_ticker_named),
    ("the known breach, on the ratchet", ratcheted_breach_stays_green),
]


def main():
    assert len(RED) == RED_EXPECTED, "a red case was deleted"
    assert len(CLEAN) == CLEAN_EXPECTED, "a clean case was deleted"
    assert len(RED) + len(CLEAN) == CASES_EXPECTED, "the case count moved"

    print("NEGATIVE CONTROL — check_bibliography  [R-ENF-01]")
    print("   %d conditions: %d that must go RED, %d that must stay GREEN"
          % (CASES_EXPECTED, RED_EXPECTED, CLEAN_EXPECTED))
    bad = []
    for name, fn in RED:
        tmp = _sandbox()
        try:
            want = fn(tmp)
            rc, out = _run(tmp)
            ok = rc != 0 and (want is None or want in out)
            print("   %-52s %s" % (name, "RED" if ok else "*** STAYED GREEN ***"))
            if not ok:
                bad.append("%s: rc=%d, expected %r\n%s" % (name, rc, want, out[-400:]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    for name, fn in CLEAN:
        tmp = _sandbox()
        try:
            fn(tmp)
            rc, out = _run(tmp)
            print("   %-52s %s" % (name, "green" if rc == 0 else "*** WENT RED ***"))
            if rc != 0:
                bad.append("%s: went red\n%s" % (name, out[-500:]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    if bad:
        print("\nFAIL")
        for b in bad:
            print("  - " + b)
        return 1
    print("\nOK — %d of %d conditions behaved as the gate claims."
          % (CASES_EXPECTED, CASES_EXPECTED))
    return 0


if __name__ == "__main__":
    sys.exit(main())
