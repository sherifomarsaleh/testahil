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

Exit code is non-zero (and prints every finding) if anything in 1-5 fires.
Run from the repo root: python3 scripts/check_page_integrity.py
"""
from __future__ import annotations

import hashlib
import html
import re
import sys
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


def main() -> int:
    all_html = {p.name: p for p in REPO.glob("*.html")}
    ticker_pages = {
        n: p for n, p in all_html.items()
        if n not in NON_TICKER_PAGES and n not in STUB_PAGES
    }
    data_js_path = REPO / "assets" / "data.js"
    if not data_js_path.exists():
        print(f"FATAL: {data_js_path} not found — run this from the repo root.")
        return 2
    fair_base = load_fair_base(data_js_path.read_text(encoding="utf-8"))

    findings: list[tuple[str, list[str]]] = [
        ("accordion-nesting", check_accordion_nesting(ticker_pages)),
        ("missing-sections", check_missing_sections(ticker_pages)),
        ("duplicate-tables", check_duplicate_tables(ticker_pages)),
        ("stale-fair-value", check_stale_fair_value(ticker_pages, fair_base)),
        ("cache-buster-drift", check_cache_buster_drift(all_html)),
    ]

    total = sum(len(f) for _, f in findings)
    print(f"Checked {len(ticker_pages)} ticker pages, {len(all_html)} HTML files total.\n")
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
    if total:
        print(f"{total} finding(s) — see above. Fix before publishing.")
        return 1
    print("Clean — no hard findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
