#!/usr/bin/env python3
"""Put the invite gate and a noindex on every served page — and gate on it.

Written 14-09-2026, when the site became invitation-only. The same lesson
[R-ENF-01] that produced inject_site_chrome.py applies here and for the same
reason: "every page under testahil.com/ is behind the rope" is a property of
the deploy, so the deploy path makes it true rather than reporting afterwards
that a new page shipped open. The population and the exempt set are IMPORTED
from scripts/check_page_integrity.py, never reimplemented.

Two marks per page, both in <head>, both idempotent:

  <meta name="robots" content="noindex,nofollow">   — keep it out of search
  <script src="/assets/gate.js"></script>           — the rope itself

A page that already carries a robots meta containing "noindex" is left alone
(the archived ticker pages carry their own). One that carries a robots meta
WITHOUT noindex is rewritten, because an index directive on an invite-only
site is the defect, not the exemption.

Modes:
  --self-test  negative control: an open page must FAIL the check before
               injection and PASS after, at both depths; an already-gated page
               comes back byte-untouched; CRLF is preserved; the exempt file
               is untouched.
  --write      inject into any served page missing either mark.
  --check      exit 1 on any served page still missing either mark.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
REPO = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from check_page_integrity import (  # noqa: E402  (path set above)
    TAB_CHROME_EXEMPT,
    served_pages,
)

GATE_SRC = "/assets/gate.js"
GATE_TAG = f'<script src="{GATE_SRC}"></script>'
NOINDEX = '<meta name="robots" content="noindex,nofollow">'

GATE_RE = re.compile(r'<script[^>]*src="/assets/gate\.js"', re.I)
ROBOTS_RE = re.compile(r'<meta\s+name="robots"[^>]*>', re.I)


def head_of(src: str) -> str:
    return src.split("</head>", 1)[0] if "</head>" in src else src[:4000]


def findings_for(relname: str, src: str) -> list[str]:
    """The pass condition, in one place, used by --write and --check alike."""
    if relname in TAB_CHROME_EXEMPT:
        return []
    head = head_of(src)
    out = []
    if not GATE_RE.search(head):
        out.append("no invite gate")
    m = ROBOTS_RE.search(head)
    if not m or "noindex" not in m.group(0).lower():
        out.append("not noindex")
    return out


def inject(relname: str, src: str) -> str:
    """Pure text -> text, idempotent. Never rewrites anything but a robots
    meta that asks to be indexed."""
    if relname in TAB_CHROME_EXEMPT:
        return src

    head, sep, tail = src.partition("</head>")
    scope = head if sep else src

    m = ROBOTS_RE.search(scope)
    if m and "noindex" not in m.group(0).lower():
        scope = scope[: m.start()] + NOINDEX + scope[m.end():]
        m = ROBOTS_RE.search(scope)

    add = []
    if not m:
        add.append(NOINDEX)
    if not GATE_RE.search(scope):
        add.append(GATE_TAG)
    if not add:
        return scope + sep + tail

    lines = "\n".join(add)
    # As early in the head as possible — the gate hides the document at parse
    # time, so anything it sits behind is markup the visitor could see flash.
    for pat in (r"<meta charset=[^>]*>", r"<head\b[^>]*>", r"</title>"):
        hit = re.search(pat, scope, re.I)
        if hit:
            return scope[: hit.end()] + "\n" + lines + scope[hit.end():] + sep + tail
    return lines + "\n" + scope + sep + tail


def run_write() -> int:
    changed = []
    pages = served_pages()
    for name, path in sorted(pages.items()):
        with open(path, encoding="utf-8", errors="replace", newline="") as fh:
            src = fh.read()
        out = inject(name, src)
        if out != src:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(out)
            changed.append(name)
    for n in changed:
        print(f"gated: {n}")
    print(f"{len(changed)} page(s) changed, {len(pages)} served pages walked")
    return 0


def run_check() -> int:
    findings = []
    for name, path in sorted(served_pages().items()):
        src = path.read_text(encoding="utf-8", errors="replace")
        for what in findings_for(name, src):
            findings.append(f"{name}: {what}")
    if findings:
        print(f"INVITE GATE: {len(findings)} finding(s) — the deploy is blocked")
        for f in findings[:40]:
            print(f"  - {f}")
        if len(findings) > 40:
            print(f"  ... and {len(findings) - 40} more")
        return 1
    print("invite gate: every served page carries the gate and a noindex")
    return 0


OPEN_PAGE = (
    "<!doctype html><html><head><meta charset=\"utf-8\">"
    "<title>x</title></head><body>hi</body></html>"
)


def run_self_test() -> int:
    fails = []

    # 1. an open page fails before, passes after, at both depths
    for rel in ("open.html", "deep/open.html"):
        if not findings_for(rel, OPEN_PAGE):
            fails.append(f"{rel}: an open page was not flagged")
        fixed = inject(rel, OPEN_PAGE)
        if findings_for(rel, fixed):
            fails.append(f"{rel}: still flagged after injection")
        if inject(rel, fixed) != fixed:
            fails.append(f"{rel}: injection is not idempotent")

    # 2. a page that already carries its own noindex keeps it, and is not
    #    given a second robots meta
    own = OPEN_PAGE.replace("<title>", '<meta name="robots" content="noindex"><title>')
    fixed = inject("own.html", own)
    if len(ROBOTS_RE.findall(fixed)) != 1:
        fails.append("own.html: a second robots meta was added")

    # 3. an indexing directive is REPLACED, not appended to
    idx = OPEN_PAGE.replace("<title>", '<meta name="robots" content="index,follow"><title>')
    fixed = inject("idx.html", idx)
    if "index,follow" in fixed or len(ROBOTS_RE.findall(fixed)) != 1:
        fails.append("idx.html: an index directive survived")

    # 4. CRLF is preserved
    crlf = OPEN_PAGE.replace("><", ">\r\n<")
    fixed = inject("crlf.html", crlf)
    if "\r\n" not in fixed:
        fails.append("crlf.html: CRLF was not preserved")

    # 5. the exempt file is untouched
    ex = sorted(TAB_CHROME_EXEMPT)[0]
    if inject(ex, OPEN_PAGE) != OPEN_PAGE:
        fails.append(f"{ex}: the exempt file was rewritten")

    if fails:
        print("SELF-TEST FAILED:")
        for f in fails:
            print(f"  - {f}")
        return 1
    print("invite-gate injector self-test: all cases pass")
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
    return run_write() if a.write else run_check()


if __name__ == "__main__":
    raise SystemExit(main())
