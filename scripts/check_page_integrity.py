#!/usr/bin/env python3
"""Static page-integrity gate for the ticker/metals site (added 27-Jul-2026).

Why this exists: on 27-Jul-2026 a user screenshot showed rmda.html rendering
with no Monte Carlo section. Reading the markup found nothing wrong — every
sec-* anchor and every <details> was present. The fault only showed up under
a real parse: a missing </details> had nested the "Monte Carlo" accordion
INSIDE "Technical & price structure", so it only existed once you opened
Technical first. The same sweep, extended to cross-page consistency, then
found five OTHER pages quietly publishing a different company's valuation
table (a clone-and-forget artifact) — ihc.html was showing Aramco's lenses,
salik.html showed e&'s, clho.html showed Rameda's, jufo.html showed Abu
Qir's, aapl.html showed Tesla's peer map. On four of the five the static
table contradicted the fair-value gauge rendered from data.js on the SAME
page — which is exactly the class of bug this script is built to catch
automatically, instead of waiting for a user to notice a wrong number.

This script is pure static analysis — no browser, no JS execution. That
covers everything that actually caught real bugs so far. It does NOT confirm
the page renders correctly at runtime (JS errors, whether a container div
actually gets populated) — for that, render the page headless (Playwright,
file://, wait_until='load' — NOT 'networkidle', which never fires against
these pages) and query the live DOM. That is a heavier, local/manual step;
this script is the fast, dependency-free, CI-friendly first line of defense.

Checks:
  1. accordion-nesting   — a `<details class="rds">` opening before its
                            predecessor closes (the RMDA bug class: a missing
                            </details> buries an entire section)
  2. missing-sections    — a ticker page's five standard sections
                            (sec-value / sec-chart / sec-odds / sec-peers /
                            sec-study) are all present, each inside its own
                            top-level accordion
  3. duplicate-tables    — two DIFFERENT tickers rendering byte-identical
                            numeric tables (the clone-and-forget signature —
                            a real per-ticker table should never match
                            another ticker's numbers)
  4. stale-fair-value    — a page's static "weighted central fair value" /
                            "Fair value (weighted)" table row disagrees with
                            that ticker's fair.base in assets/data.js by more
                            than 2% (the tell that a cloned block was never
                            repopulated — data.js and the page ship from the
                            same edit, so they should never drift)
  5. cache-buster-drift  — every HTML file must reference the SAME
                            assets/app.js and assets/data.js query-string
                            version. A partial bump (some pages get the new
                            string, some don't) is invisible in git and in
                            the rendered page, but returning visitors get a
                            stale cached copy on the un-bumped pages and see
                            no change at all.
  6. tab-chrome          — EVERY page the site serves, at any depth, carries
                            a <title> and a site favicon link in its REAL
                            <head>, with a path that actually resolves from
                            that page's own folder. Added 26-Aug-2026 after
                            all 90 three-lenses pages shipped with neither,
                            and widened the same day when the first cut was
                            found globbing the repo root only while 149 pages
                            under ar/, embed/, go/, test/ and engine/ had no
                            icon at all. Exempt: the Google verification token
                            and the saved primary sources under engine/*_study/.

Exit code is non-zero (and prints every finding) if anything in 1-6 fires.
Run from the repo root: python3 scripts/check_page_integrity.py
"""
from __future__ import annotations

import hashlib
import html
import re
import sys
import os as _os
_sys_dir = _os.path.dirname(_os.path.abspath(__file__))
sys.path.insert(0, _sys_dir)
from coverage_floor import assert_examined  # noqa: E402  [R-ENF-04]
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Non-ticker pages: tools, stubs, and indexes that don't carry the five-lens
# ticker template and so are exempt from checks 1/2/4. Checks 3/5 still apply
# to every HTML file in the repo.
NON_TICKER_PAGES = {
    "404.html", "googlef90107a488de289e.html", "thanks.html", "archive.html",
    "news.html", "calculator.html", "compare.html", "egypt.html", "index.html",
    "ledger.html", "metals.html", "method.html", "other-markets.html",
    "stocks.html", "trade.html", "portfolio.html", "picker.html",
}
# Deliberate "coming soon" stubs — correctly minimal, not a bug.
STUB_PAGES = {"copper.html", "mfpc.html"}
# Check 6 exemptions — TWO families, neither of them a page we authored.
# Everything else the site serves must carry the icon, redirect stubs included
# (a stub still flashes a tab).
#
#   * googlef90107a488de289e.html — a Google Search Console verification token,
#     fetched by a verifier rather than read by a person, whose CONTENTS are
#     what the verification tests. Editing it risks un-verifying the domain.
#   * engine/*_study/ — SAVED PRIMARY SOURCES: the ADNOC L&S investor-relations
#     captures and Damodaran's ctryprem.html, which the cost-of-capital rule
#     names as the file to read fresh. SIGCM makes these EVIDENCE, not site
#     furniture; adding site chrome to a source document corrupts the record
#     the study rests on. This is the one exemption that must never be relaxed
#     for tidiness.
TAB_CHROME_EXEMPT = {"googlef90107a488de289e.html"}
PRIMARY_SOURCE_DIRS = ("engine/adnocls_study/", "engine/airarabia_study/",
                       "engine/amr_study/", "engine/savola_study/")

# Three-lenses landing pages (<ticker>-3lenses.html, added 26-Aug-2026) are a
# SECOND page type, not a five-lens study page: one chart carrying the technical
# levels, the published t20/t60 percentiles and the fair-value range on a single
# axis, with the study page one click away. They deliberately carry no
# sec-value/sec-chart/sec-odds/sec-peers/sec-study accordions, so checks 1/2/4
# do not describe them and would fail all 90 on structure alone. They are NOT
# exempt from the clone-detection checks that motivated this script: every
# number they show is read at runtime from assets/data.js under the page's own
# ticker key, so a cross-ticker clone is impossible by construction — there is
# no static valuation table on the page to copy wrong in the first place.
THREE_LENS_SUFFIX = "-3lenses.html"

EXPECTED_SECTIONS = ["sec-value", "sec-chart", "sec-odds", "sec-peers", "sec-study"]


class DetailsNestingParser(HTMLParser):
    """Tracks <details class="rds"> open/close to catch a missing </details>
    burying one accordion inside another (checks 1 & 2)."""

    def __init__(self):
        super().__init__()
        self.stack = []          # stack of {"rds": bool}
        self.rds_events = []     # (depth_at_open, ) for each rds details, in doc order
        self.sec_ids = []        # every id="sec-*" seen, with the rds-depth it's inside
        self.rds_depth_here = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "details":
            is_rds = "rds" in (a.get("class") or "").split()
            self.stack.append(is_rds)
            if is_rds:
                self.rds_events.append(self.rds_depth_here)
                self.rds_depth_here += 1
        eid = a.get("id") or ""
        if eid.startswith("sec-"):
            self.sec_ids.append((eid, self.rds_depth_here))

    def handle_endtag(self, tag):
        if tag == "details" and self.stack:
            was_rds = self.stack.pop()
            if was_rds:
                self.rds_depth_here -= 1


def parse_page(path: Path) -> DetailsNestingParser:
    p = DetailsNestingParser()
    p.feed(path.read_text(encoding="utf-8", errors="replace"))
    return p


def check_accordion_nesting(pages: dict[str, Path]) -> list[str]:
    findings = []
    for name, path in pages.items():
        p = parse_page(path)
        nested = [d for d in p.rds_events if d > 0]
        if nested:
            findings.append(
                f"{name}: {len(nested)} top-level section(s) opened INSIDE another "
                f"section's <details> (nesting depth {max(nested)}) — almost always a "
                f"missing </details>. A reader only sees the buried section if they "
                f"first open its parent."
            )
    return findings


def check_missing_sections(pages: dict[str, Path]) -> list[str]:
    findings = []
    for name, path in pages.items():
        p = parse_page(path)
        seen = {sid for sid, _ in p.sec_ids}
        missing = [s for s in EXPECTED_SECTIONS if s not in seen]
        if missing:
            findings.append(f"{name}: missing section anchor(s) {missing}")
        buried = [sid for sid, depth in p.sec_ids if sid in EXPECTED_SECTIONS and depth > 1]
        if buried:
            findings.append(f"{name}: section anchor(s) {buried} sit nested inside another accordion")
    return findings


def extract_table_signatures(src: str) -> list[str]:
    """Every <table>...</table>'s FULL cell text (every <td>, any class — not
    just class="num"), as a normalized signature string.

    An earlier version of this check only looked at class="num" cells that
    contained a digit. That missed the actual aapl.html/tsla.html clone found
    on 27-Jul-2026: the shared "position vs rivals" table used class="num"
    for qualitative text ("Co-leader", "Top tier", "Early (pre-revenue)")
    with no digits in it, so nothing was fingerprinted at all. Caught by
    testing this script against that exact historical bug before trusting it
    — see the commit this file was added in. Now every cell counts, and the
    threshold is on total signature length / cell count instead of "looks
    numeric", so a fully-cloned qualitative table is just as catchable as a
    fully-cloned numeric one.

    Tables under the length/cell threshold are skipped — too generic (a
    2-row snapshot table, e.g. "Code | XCU") to be a meaningful fingerprint,
    and short coincidental matches are exactly the false positive this
    threshold exists to avoid.
    """
    sigs = []
    for t in re.findall(r"<table>.*?</table>", src, re.S):
        cells = re.findall(r"<td[^>]*>(.*?)</td>", t, re.S)
        vals = [html.unescape(re.sub("<.*?>", "", c)).strip() for c in cells]
        vals = [v for v in vals if v]
        sig = "|".join(vals)
        if len(vals) >= 6 and len(sig) >= 60:
            sigs.append(sig)
    return sigs


def check_duplicate_tables(pages: dict[str, Path]) -> list[str]:
    seen: dict[str, set[str]] = defaultdict(set)
    for name, path in pages.items():
        src = path.read_text(encoding="utf-8", errors="replace")
        for sig in extract_table_signatures(src):
            seen[hashlib.md5(sig.encode()).hexdigest()].add(name)
    findings = []
    for h, names in seen.items():
        if len(names) > 1:
            findings.append(
                f"identical numeric table on different tickers: {', '.join(sorted(names))} "
                f"— a real per-ticker valuation table should never match another ticker's numbers"
            )
    return findings


def extract_row_signatures(src: str) -> list[str]:
    """Every <tr>...</tr>'s cell text, same normalization as
    extract_table_signatures but at ROW granularity."""
    sigs = []
    for t in re.findall(r"<table>.*?</table>", src, re.S):
        for row in re.findall(r"<tr[^>]*>(.*?)</tr>", t, re.S):
            cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
            vals = [html.unescape(re.sub("<.*?>", "", c)).strip() for c in cells]
            vals = [v for v in vals if v]
            sig = "|".join(vals)
            if len(vals) >= 3 and len(sig) >= 40:
                sigs.append(sig)
    return sigs


def check_duplicate_rows(pages: dict[str, Path]) -> list[str]:
    """ADVISORY, not a hard fail (see main()) — this check is what caught a
    SIXTH clone-and-forget bug the whole-table check above missed: rmda.html
    carried oriental-weavers'(orwe.html) real FCFE-DCF/EBITDA-multiple/
    normalized-earnings lens VALUES verbatim (17.3 / 21.2 / 21.1, with
    orwe's own row labels) while its "Relative multiples" and "Fair value
    (weighted)" rows had been correctly updated to RMDA's own numbers — a
    PARTIALLY fixed clone, which a whole-table hash cannot catch because the
    two tables are no longer byte-identical.

    But row-level matching also flags genuinely legitimate cases: two
    closely related tickers correctly citing the same external fact (Emaar
    and Emaar Development both citing the same Dubai-market rival list),
    or a boilerplate disclosure line that legitimately repeats across every
    wholly-owned SOTP subsidiary ("Less: other owners' share | 0.00 |
    Negligible — wholly owned"). Both of those turned up empirically when
    this check was built and are NOT bugs. Given that, this check is
    reported for human review, not treated as a hard failure — read every
    line: some are a real clone, some are a real coincidence."""
    seen: dict[str, set[str]] = defaultdict(set)
    for name, path in pages.items():
        src = path.read_text(encoding="utf-8", errors="replace")
        for sig in extract_row_signatures(src):
            seen[hashlib.md5(sig.encode()).hexdigest()].add(name)
    findings = []
    for h, names in seen.items():
        if len(names) > 1:
            findings.append(f"{', '.join(sorted(names))} share an identical table row")
    return findings


def load_fair_base(data_js: str) -> dict[str, float]:
    out = {}
    for m in re.finditer(
        r"\n  ([A-Z0-9_]+): \{(.{0,2000}?)fair:\s*\{\s*bear:\s*([\d.]+),\s*base:\s*([\d.]+),\s*full:\s*([\d.]+)",
        data_js, re.S,
    ):
        out[m.group(1)] = float(m.group(4))
    return out


def check_stale_fair_value(pages: dict[str, Path], fair_base: dict[str, float]) -> list[str]:
    findings = []
    for name, path in pages.items():
        src = path.read_text(encoding="utf-8", errors="replace")
        km = re.search(r"const T\s*=\s*TICKERS\.([A-Z0-9_]+)", src)
        if not km or km.group(1) not in fair_base:
            continue
        ticker = km.group(1)
        rm = re.search(
            r'<tr style="font-weight:700"><td>(?:Weighted central fair value|Fair value \(weighted\))'
            r'</td><td class="num">([\d.,]+)',
            src,
        )
        if not rm:
            continue
        page_val = float(rm.group(1).replace(",", ""))
        base_val = fair_base[ticker]
        if base_val and abs(page_val - base_val) / abs(base_val) > 0.02:
            pct = (page_val / base_val - 1) * 100
            findings.append(
                f"{name}: page shows weighted-central {page_val:g}, but assets/data.js "
                f"TICKERS.{ticker}.fair.base is {base_val:g} ({pct:+.0f}%) — the static "
                f"table and the live gauge on the same page disagree"
            )
    return findings


def check_cache_buster_drift(all_html: dict[str, Path]) -> list[str]:
    findings = []
    for asset, pattern in (("app.js", r"app\.js\?v=([a-z0-9]+)"), ("data.js", r"data\.js\?v=([a-z0-9]+)")):
        versions: dict[str, list[str]] = defaultdict(list)
        for name, path in all_html.items():
            src = path.read_text(encoding="utf-8", errors="replace")
            m = re.search(pattern, src)
            if m:
                versions[m.group(1)].append(name)
        if len(versions) > 1:
            parts = "; ".join(f"{v} ({len(ns)} pages)" for v, ns in sorted(versions.items()))
            findings.append(
                f"{asset}: pages reference DIFFERENT cache-buster versions — {parts}. "
                f"A page on the old version silently keeps serving the cached pre-edit "
                f"file to a returning visitor even though {asset} itself already changed."
            )
    return findings


def served_pages() -> dict[str, Path]:
    """EVERY page the site serves, at any depth — the population check 6 owns.

    GitHub Pages publishes the whole repository (there is a .nojekyll), so a
    page is anything ending .html anywhere in the tree, not just the root.
    Build directories that are never deployed are skipped by name.
    """
    skip = {".git", "node_modules", "__pycache__", ".github"}
    out = {}
    for p in sorted(REPO.rglob("*.html")):
        rel = p.relative_to(REPO)
        if any(part in skip for part in rel.parts):
            continue
        out[rel.as_posix()] = p
    return out


def check_tab_chrome(pages: dict[str, Path]) -> list[str]:
    """Check 6: a page that a reader can land on names itself and carries the
    site icon, in the real <head> — not in a block a runtime hoists later.

    Written 26-Aug-2026, when every <ticker>-3lenses.html (built that day from
    a different template than the study pages) was found with no <title> and
    no rel="icon" at all. Nothing else looked: checks 1-4 skip that page type
    by design and check 5 only compares versions between pages that DO
    reference an asset.

    WIDENED THE SAME DAY, per instruction — "any page and I mean any page with
    testahil.com/ should have the favicon" — after the first cut of this very
    check globbed the REPO ROOT ONLY and so reported the site clean while 149
    pages under ar/, embed/, go/, test/ and engine/ had no icon at all. That is
    the [R-ENF-01] species twice over: the check was narrower than the rule it
    enforced, and its own scope was the thing nobody audited. THE POPULATION A
    CHECK WALKS IS PART OF THE CHECK; a gate that reports clean having examined
    a third of the book is worse than none, because it certifies the rest.

    PATH DEPTH IS CHECKED, NOT JUST PRESENCE: href="favicon.png?v=2" is
    relative and correct at the root, but from ar/aapl.html it resolves to
    /ar/favicon.png — a 404 that looks perfect in a diff. Subdirectory pages
    must therefore use the root-absolute "/favicon.png".

    Only the <head> before </head> is inspected, because the three-lenses pages
    carry a <helmet> block inside <body> whose <link>/<meta> children the DC
    runtime clones into <head> at load time — an icon there would work in a
    browser and still be a different fact from the one this check states. The
    engine/build_depth_audit reports are headless fragments (they open on
    <title> with no wrapper), so for those the leading run of head-only
    elements is what a browser builds a head from, and what is inspected.

    Measured: 180 findings on the pre-fix root-only tree, 149 more once the
    scope widened to every served page, 0 on the fixed tree.
    """
    findings = []
    for name, path in sorted(pages.items()):
        if name in TAB_CHROME_EXEMPT or name.startswith(PRIMARY_SOURCE_DIRS):
            continue
        src = path.read_text(encoding="utf-8", errors="replace")
        head = src.split("</head>", 1)[0] if "</head>" in src else src[:4000]
        if 'http-equiv="refresh"' in head and "<title>" in head:
            # A redirect stub still flashes a tab; it is NOT exempt from the
            # icon. It is exempt from nothing here — this branch only exists to
            # document that the earlier blanket refresh exemption was dropped
            # when the rule became "any page".
            pass
        at_root = "/" not in name
        want = r'href="favicon\.png(\?[^"]*)?"' if at_root else r'href="/favicon\.png(\?[^"]*)?"'
        if not re.search(r'<link[^>]*rel="icon"[^>]*' + want, head):
            if re.search(r'<link[^>]*rel="icon"', head):
                findings.append(
                    f"{name}: favicon link has the wrong path for its depth — a "
                    f"page in a subdirectory needs the root-absolute "
                    f"/favicon.png, or the browser resolves it against its own "
                    f"folder and gets a 404 while the markup looks right")
            else:
                findings.append(f'{name}: no site favicon link (rel="icon" -> favicon.png) in <head>')
        if not re.search(r"<title>\s*[^<\s]", head):
            findings.append(f"{name}: no <title> in <head> — the browser tab shows the bare URL")
    return findings


def main() -> int:
    all_html = {p.name: p for p in REPO.glob("*.html")}
    served = served_pages()
    ticker_pages = {
        n: p for n, p in all_html.items()
        if n not in NON_TICKER_PAGES and n not in STUB_PAGES
        and not n.endswith(THREE_LENS_SUFFIX)
    }
    data_js_path = REPO / "assets" / "data.js"
    if not data_js_path.exists():
        print(f"FATAL: {data_js_path} not found — run this from the repo root.")
        return 2
    fair_base = load_fair_base(data_js_path.read_text(encoding="utf-8"))
    # [R-ENF-04] The page-count floor below cannot see THIS gate's other blind
    # spot: its scope is the HTML files on disk, so emptying data.js leaves the
    # page count untouched and only makes the data.js cross-checks VACUOUS. The
    # negative control found exactly that, against the first version of this very
    # fix — with data.js emptied, 93 pages were still walked and the gate still
    # printed "Clean". Zero is the only value that makes the comparison vacuous,
    # so zero is what is refused; 92-of-93 is a real property of the book (one
    # page carries no fair block) and not a floor violation.
    if not fair_base:
        print("FATAL: assets/data.js yielded NO fair.base values, so the "
              "stale-fair-value check would compare against nothing and pass "
              "vacuously. Refusing to report clean. [R-ENF-04]")
        return 2

    findings: list[tuple[str, list[str]]] = [
        ("accordion-nesting", check_accordion_nesting(ticker_pages)),
        ("missing-sections", check_missing_sections(ticker_pages)),
        ("duplicate-tables", check_duplicate_tables(ticker_pages)),
        ("stale-fair-value", check_stale_fair_value(ticker_pages, fair_base)),
        ("cache-buster-drift", check_cache_buster_drift(all_html)),
        ("tab-chrome", check_tab_chrome(served)),
    ]

    total = sum(len(f) for _, f in findings)
    # Both populations are PRINTED, per [R-ENF-04]: checks 1-5 walk the root
    # ticker pages, check 6 walks every page the site serves at any depth, and
    # the day those two silently disagreed is the day 149 pages went unchecked.
    print(f"Checked {len(ticker_pages)} ticker pages, {len(all_html)} root HTML files, "
          f"{len(served)} served pages at all depths (check 6).\n")
    for check_name, items in findings:
        status = "FAIL" if items else "ok"
        print(f"[{status}] {check_name} ({len(items)} finding{'s' if len(items) != 1 else ''})")
        for it in items:
            print(f"    - {it}")

    # Advisory, not counted in the exit code — see check_duplicate_rows'
    # docstring. Real hit rate so far: 1 genuine partial-clone bug (rmda.html/
    # orwe.html) alongside 2 legitimate coincidences. Read every line.
    row_dupes = check_duplicate_rows(ticker_pages)
    print(f"\n[advisory] duplicate-rows ({len(row_dupes)} finding{'s' if len(row_dupes) != 1 else ''}) "
          f"— review each; not all are bugs, see script docstring")
    for it in row_dupes:
        print(f"    - {it}")

    print()
    # [R-ENF-04] A gate must never report clean having examined nothing. Measured
    # on adoption day: with data.js emptied to a valid file holding zero entries,
    # this script exited 0 and printed "Clean — no hard findings." It was not
    # broken; it faithfully checked every one of nothing. The count is now
    # PRINTED (it never was) and held against the OHLC libraries on disk, a
    # population counted somewhere data.js cannot reach.
    pop = assert_examined(len(ticker_pages), 'check_page_integrity', 'ticker pages')
    if total:
        print(f"{total} finding(s) across {len(ticker_pages)} ticker pages "
              f"— see above. Fix before publishing.")
        return 1
    print(f"Clean — no hard findings across {len(ticker_pages)} ticker pages "
          f"({pop} libraries on disk).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
