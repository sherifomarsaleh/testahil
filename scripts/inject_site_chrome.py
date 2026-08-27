#!/usr/bin/env python3
"""Inject the site favicon links into any served page missing them — and gate on it.

Written 27-Aug-2026, the day after check 6 (tab-chrome) was added, when two
brand-new pages (test/record.html, test/study.html) shipped without the icon
links their five sibling pages carried — and by the time the fix was pushed,
374 more (the per-ticker clean-URL shells under test/{TICKER}/) had shipped
the same way. The gate DETECTED them — after they were live. Detection after
the push is the wrong side of the deploy: the rule is "any page under
testahil.com/ has the favicon", so the deploy path itself must make that
true, not report that it wasn't.

Three modes, the first three steps of deploy-pages.yml BEFORE the artifact
uploads:

  --self-test  negative control on synthetic pages: a chrome-less page must
               FAIL check_tab_chrome before injection and PASS after, at both
               depths; a gate-legal page must come back byte-untouched;
               foreign icon markup preserved; CRLF preserved; the exempt file
               untouched. Runs first in CI so the injector cannot silently rot.
  --write      fix what is mechanical: inject the depth-correct icon pair into
               any served page the gate would flag. Idempotent — a second run
               is a byte-for-byte no-op. NEVER invents a <title>: a page's
               name is a human decision, not chrome.
  --check      import the REAL gate (check_page_integrity.check_tab_chrome
               over check_page_integrity.served_pages) and exit 1 on any
               finding. After --write the only possible findings are missing
               titles — exactly the thing that SHOULD block a deploy loudly.

THE POPULATION AND THE PASS CRITERION ARE IMPORTED, NEVER REIMPLEMENTED
([R-ENF-01]): this script takes served_pages(), TAB_CHROME_EXEMPT and
check_tab_chrome from scripts/check_page_integrity.py by import, so the set
of pages the injector walks and the test the gate applies are the checker's
own, by construction — an injector with its own private notion of "a page"
or "has an icon" would be the scope-drift defect check 6's docstring already
records.
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
REPO = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from check_page_integrity import (  # noqa: E402  (path set above)
    TAB_CHROME_EXEMPT,
    check_tab_chrome,
    served_pages,
)


def gate_icon_re(relname: str) -> re.Pattern:
    """The gate's OWN pass condition, verbatim from check_tab_chrome: an icon
    link whose href is favicon.png with ANY query string, depth-correct.
    The injector acts iff this does not match — so injector and gate agree by
    construction. (First cut used string equality on ?v=2 and 'repaired' a
    gate-legal ?v=20260713f on lulu.html, and rewrote the CAPTURED icon markup
    of a filing-evidence page whose own comment says the capture is untouched.
    The lesson is the [R-ENF-01] one again: the fixer's condition must BE the
    checker's, not a paraphrase of it.)"""
    want = r'href="favicon\.png(\?[^"]*)?"' if "/" not in relname else r'href="/favicon\.png(\?[^"]*)?"'
    return re.compile(r'<link[^>]*rel="icon"[^>]*' + want)


def chrome_lines(relname: str) -> str:
    """The two icon links, depth-correct — same rule check 6 enforces:
    relative at the repo root, root-absolute anywhere deeper."""
    base = "" if "/" not in relname else "/"
    return (
        f'<link rel="icon" type="image/png" href="{base}favicon.png?v=2">\n'
        f'<link rel="apple-touch-icon" href="{base}apple-touch-icon.png?v=2">'
    )


def inject(relname: str, src: str) -> str:
    """Pure text -> text. Idempotent. NEVER rewrites existing markup — a page
    that fails the gate gets the standard pair APPENDED at the head anchor and
    everything already there is preserved byte-for-byte (the savola filing
    captures set this precedent: their own dead icon links stay untouched,
    ours sit beside them). Never touches <title>."""
    if relname in TAB_CHROME_EXEMPT:
        return src
    head, sep, tail = src.partition("</head>")
    scope = head if sep else src

    if gate_icon_re(relname).search(scope):
        return src  # the gate passes this page; nothing to do

    lines = chrome_lines(relname)
    # insertion point, best anchor first — after viewport, else charset, else
    # the <head> open tag, else after a leading <title> (headless fragments),
    # else prepend: head-only elements before any body content are what a
    # browser builds its head from, which is also what check 6 inspects.
    for pat in (
        r'<meta name="viewport"[^>]*>',
        r"<meta charset=[^>]*>",
        r"<head[^>]*>",
        r"</title>",
    ):
        m2 = re.search(pat, scope)
        if m2:
            fixed = scope[: m2.end()] + "\n" + lines + scope[m2.end():]
            return fixed + sep + tail
    return lines + "\n" + scope + sep + tail


def run_write() -> int:
    changed, untitled = [], []
    pages = served_pages()
    for name, path in sorted(pages.items()):
        # newline="" both ways: a CRLF capture stays CRLF — first cut
        # silently rewrote 2,347 lines of a filing capture LF-only.
        with open(path, encoding="utf-8", errors="replace", newline="") as fh:
            src = fh.read()
        out = inject(name, src)
        if out != src:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(out)
            changed.append(name)
        h = out.split("</head>", 1)[0] if "</head>" in out else out[:4000]
        if name not in TAB_CHROME_EXEMPT and not re.search(r"<title>\s*[^<\s]", h):
            untitled.append(name)
    for n in changed:
        print(f"injected: {n}")
    print(f"{len(changed)} page(s) changed, {len(pages)} served pages walked")
    if untitled:
        print("CANNOT FIX (a <title> is authored, not injected) — the --check "
              "gate will fail the deploy on these:")
        for n in untitled:
            print(f"  - {n}")
    return 0


def run_check() -> int:
    findings = check_tab_chrome(served_pages())
    for f in findings:
        print(f"  - {f}")
    print(f"tab-chrome gate: {len(findings)} finding(s)")
    return 1 if findings else 0


def run_self_test() -> int:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        (tmp / "sub").mkdir()
        bare = ('<!doctype html>\n<html><head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                "<title>t</title>\n</head><body>x</body></html>\n")
        foreign = '<link rel="icon" href="/Theme/icons/favicon-32.png">'
        wrong = bare.replace("<title>", foreign + "\n<title>")
        legal = bare.replace("<title>",
                             '<link rel="icon" type="image/png" href="favicon.png?v=20260713f">\n<title>')
        crlf = bare.replace("\n", "\r\n")
        cases = {"root.html": bare, "sub/page.html": bare,
                 "sub/foreign.html": wrong, "legalquery.html": legal,
                 "crlf.html": crlf}
        for rel, sc in cases.items():
            with open(tmp / rel, "w", encoding="utf-8", newline="") as fh:
                fh.write(sc)
        pages = {rel: tmp / rel for rel in cases}

        pre = check_tab_chrome(pages)
        assert len(pre) == 4, f"negative control: expected 4 icon findings pre-injection, got {pre}"
        assert not any("legalquery" in f for f in pre), "gate must accept any ?query — test premise broken"

        for rel in cases:
            with open(tmp / rel, encoding="utf-8", newline="") as fh:
                before = fh.read()
            first = inject(rel, before)
            assert inject(rel, first) == first, f"not idempotent on {rel}"
            with open(tmp / rel, "w", encoding="utf-8", newline="") as fh:
                fh.write(first)

        post = check_tab_chrome(pages)
        assert post == [], f"gate still failing after injection: {post}"
        with open(tmp / "legalquery.html", encoding="utf-8", newline="") as fh:
            assert fh.read() == legal, "a gate-passing page must be byte-untouched"
        with open(tmp / "sub/foreign.html", encoding="utf-8", newline="") as fh:
            ft = fh.read()
        assert foreign in ft and 'href="/favicon.png?v=2"' in ft, \
            "foreign icon markup must be preserved verbatim, ours appended beside it"
        with open(tmp / "crlf.html", encoding="utf-8", newline="") as fh:
            ct = fh.read()
        assert "\r\n</head>" in ct and 'href="favicon.png?v=2"' in ct, "CRLF body must survive injection"
        with open(tmp / "sub/page.html", encoding="utf-8", newline="") as fh:
            assert 'href="/favicon.png?v=2"' in fh.read()

        exempt = next(iter(TAB_CHROME_EXEMPT))
        assert inject(exempt, "google-site-verification: x") == "google-site-verification: x"
    print("self-test: ok (fails pre-injection, passes post, idempotent, gate-legal "
          "pages byte-untouched, foreign markup preserved, CRLF preserved, exempt untouched)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--write", action="store_true")
    g.add_argument("--check", action="store_true")
    g.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return run_self_test()
    if a.write:
        return run_write()
    return run_check()


if __name__ == "__main__":
    raise SystemExit(main())
