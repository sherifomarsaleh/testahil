"""Negative control for check_figure_opacity.  [R-ENF-01]

Reinjects every condition the gate refuses and the clean cases it must not fire on.
EVERY MUTATION ASSERTS THAT IT LANDED, and the case COUNT is asserted against a declared
constant.

THE CLEAN CASE THAT MATTERS IS THE OPAQUE RGBA IMAGE. Matplotlib writes an alpha channel
that is fully opaque, so 160 of the book's 176 images carry one — and a gate reading the
colour MODE rather than the minimum alpha would condemn twenty-two compliant studies. The
author's first pass did exactly that, reporting twenty times the real figure, which is why
that case is here rather than assumed.
"""
import glob
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TARGET = os.path.join(HERE, "check_figure_opacity.py")
SRC_ENGINE = os.path.join(ROOT, "engine")

CASES_EXPECTED = 9
RED_EXPECTED = 5
CLEAN_EXPECTED = 4


def _png(mode, alpha=None):
    from PIL import Image
    im = Image.new(mode, (8, 8), color=(240, 240, 240, 255)[:len(mode)])
    if alpha is not None and mode in ("RGBA", "LA"):
        a = Image.new("L", (8, 8), color=alpha)
        im.putalpha(a)
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    return buf.getvalue()


def _docx(path, images):
    """A minimal zip carrying word/media entries — all this gate reads."""
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("word/document.xml", "<w:document/>")
        for i, blob in enumerate(images, 1):
            z.writestr("word/media/image%d.png" % i, blob)


def _sandbox(studies=None):
    """Synthetic documents: the gate reads embedded images and nothing else."""
    tmp = tempfile.mkdtemp(prefix="opa-nc-")
    eng = os.path.join(tmp, "engine")
    os.makedirs(os.path.join(eng, "build_depth_audit"))
    spec = studies if studies is not None else {
        "clean": [_png("RGB"), _png("RGBA", 255)],
        "alsoclean": [_png("RGBA", 255)],
        "ratcheted": [_png("RGBA", 0)],
    }
    for tk, imgs in spec.items():
        d = os.path.join(eng, "%s_study" % tk.lower())
        os.makedirs(d)
        _docx(os.path.join(d, "%s_Valuation_Study_03-09-2026.docx" % tk.upper()), imgs)
    # THE RATCHET NAMES ONLY STUDIES THIS SANDBOX ACTUALLY CONTAINS. Writing a fixed
    # entry made two CLEAN cases go red on the anchored-on-nothing refusal — the gate
    # was right and the fixture was wrong, which is the fourth time today a control's
    # own scaffolding, not its subject, produced the failure.
    json.dump({"rule": "t",
               "outstanding": ["RATCHETED"] if "ratcheted" in spec else []},
              open(os.path.join(eng, "build_depth_audit",
                                "figure_opacity_outstanding.json"), "w"))
    os.makedirs(os.path.join(tmp, "scripts"))
    shutil.copy(TARGET, os.path.join(tmp, "scripts", "check_figure_opacity.py"))
    return tmp


def _run(tmp):
    r = subprocess.run([sys.executable,
                        os.path.join(tmp, "scripts", "check_figure_opacity.py")],
                       capture_output=True, text=True, timeout=300)
    return r.returncode, r.stdout + r.stderr


# ------------------------------------------------------------------ red cases

def translucent_new(tmp_unused):
    tmp = _sandbox({"newname": [_png("RGBA", 0)], "clean": [_png("RGB")]})
    return tmp, "translucent image"


def partially_translucent(tmp_unused):
    """Not fully transparent — a soft edge is still transparency by the bar's words."""
    tmp = _sandbox({"newname": [_png("RGBA", 128)], "clean": [_png("RGB")]})
    return tmp, "translucent image"


def phantom_ratchet(tmp_unused):
    tmp = _sandbox()
    p = os.path.join(tmp, "engine", "build_depth_audit",
                     "figure_opacity_outstanding.json")
    json.dump({"outstanding": ["NOSUCHNAME"]}, open(p, "w"))
    assert json.load(open(p))["outstanding"] == ["NOSUCHNAME"], "MUTATION DID NOT LAND"
    return tmp, "anchored on nothing"


def no_images(tmp_unused):
    """A document reader that stopped finding media reads like a clean book."""
    tmp = _sandbox({"clean": [], "alsoclean": []})
    got = 0
    for p in glob.glob(os.path.join(tmp, "engine", "*_study", "*.docx")):
        with zipfile.ZipFile(p) as z:
            got += sum(1 for n in z.namelist() if n.startswith("word/media/"))
    assert got == 0, "MUTATION DID NOT LAND: media survived"
    return tmp, "ZERO images"


def emptied_population(tmp_unused):
    tmp = _sandbox()
    dirs = glob.glob(os.path.join(tmp, "engine", "*_study"))
    assert dirs, "MUTATION DID NOT LAND"
    for d in dirs:
        shutil.rmtree(d)
    return tmp, "ZERO study directories"


# ---------------------------------------------------------------- clean cases

def opaque_rgba(tmp_unused):
    """THE CASE THAT DECIDES THIS GATE. An RGBA image that is fully opaque.

    160 of the book's 176 images are exactly this. A gate reading the MODE would
    condemn twenty-two compliant studies; the author's first pass did.
    """
    tmp = _sandbox({"clean": [_png("RGBA", 255), _png("RGBA", 255)]})
    with zipfile.ZipFile(glob.glob(os.path.join(tmp, "engine", "*_study",
                                                "*.docx"))[0]) as z:
        from PIL import Image
        im = Image.open(io.BytesIO(z.read("word/media/image1.png")))
        assert im.mode == "RGBA", "fixture: the image is not RGBA, so it proves nothing"
        assert im.getchannel("A").getextrema()[0] == 255, "fixture: it is not opaque"
    return tmp, None


def plain_rgb(tmp_unused):
    tmp = _sandbox({"clean": [_png("RGB")]})
    return tmp, None


def ratcheted_offender(tmp_unused):
    """The known breach is on the list and must not turn the build red."""
    tmp = _sandbox()
    p = os.path.join(tmp, "engine", "build_depth_audit",
                     "figure_opacity_outstanding.json")
    assert "RATCHETED" in json.load(open(p))["outstanding"], "fixture: not ratcheted"
    return tmp, None


def study_with_no_document(tmp_unused):
    """A metals directory delivers no study; it is out of scope, not a breach."""
    tmp = _sandbox()
    d = os.path.join(tmp, "engine", "metal_study")
    os.makedirs(d)
    assert not glob.glob(os.path.join(d, "*.docx")), "MUTATION DID NOT LAND"
    return tmp, None


RED = [
    ("a fully transparent figure in a new study", translucent_new),
    ("a partly translucent figure", partially_translucent),
    ("a ratchet naming a study not on disk", phantom_ratchet),
    ("no images found at all", no_images),
    ("an emptied population", emptied_population),
]
CLEAN = [
    ("an OPAQUE RGBA image — the mode is not the measurement", opaque_rgba),
    ("a plain RGB image", plain_rgb),
    ("the known breach, on the ratchet", ratcheted_offender),
    ("a directory delivering no study document", study_with_no_document),
]


def main():
    assert len(RED) == RED_EXPECTED, "a red case was deleted"
    assert len(CLEAN) == CLEAN_EXPECTED, "a clean case was deleted"
    assert len(RED) + len(CLEAN) == CASES_EXPECTED, "the case count moved"

    print("NEGATIVE CONTROL — check_figure_opacity  [R-ENF-01]")
    print("   %d conditions: %d that must go RED, %d that must stay GREEN"
          % (CASES_EXPECTED, RED_EXPECTED, CLEAN_EXPECTED))
    bad = []
    for name, fn in RED:
        tmp, want = fn(None)
        try:
            rc, out = _run(tmp)
            ok = rc != 0 and (want is None or want in out)
            print("   %-52s %s" % (name, "RED" if ok else "*** STAYED GREEN ***"))
            if not ok:
                bad.append("%s: rc=%d, expected %r\n%s" % (name, rc, want, out[-400:]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    for name, fn in CLEAN:
        tmp, _ = fn(None)
        try:
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
