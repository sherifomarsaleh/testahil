"""A dated archive of every fair value this house has published.  [R-VCAL-01]

WHY IT EXISTS. `assets/data.js` carries exactly ONE `fair{bear,base,full}` per
name, with no date and no standard stamp on it. So the question "what did we say
this company was worth in March, and against what price?" has no answer in the
repository — it can only be reconstructed by walking git history, which the value-
gap backtest had to do and which yielded about a month of observations because the
working clone is shallow. A record that has to be excavated is a record the next
question will not bother to ask.

Every published fair value therefore lands here, dated, with the spot it was
struck against and the standard it was built to. The valuation calibration's
series (b) reads vintages from this file, and so does every future backtest.

TWO SOURCES, KEPT APART ON PURPOSE, because they are different evidence:

  RECONSTRUCTED — recovered by walking `assets/data.js` through git history. Each
  entry carries the commit and its date, and the date is WHEN THE VALUE APPEARED
  IN THE REPOSITORY, which is not necessarily when the study was struck. It is the
  best available answer for the past and it is labelled as an inference, never as
  a record.

  RECORDED — written at the moment of publication by the re-issue or the site
  build, carrying the study's own strike date, its own spot and its own standard
  version. From the first entry onward this is the real archive; the
  reconstruction is scaffolding under it.

THE ARCHIVE NEVER INFERS A SPOT IT DOES NOT HOLD. A vintage whose price at the
time is unknown records the fair value and says the spot is unknown, because
log(FV/P) computed against the wrong price is worse than no observation: it is a
plausible number that quietly poisons a pooled mean.
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
from typing import Dict, List, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
ROOT = os.path.dirname(ENGINE)
ARCHIVE = os.path.join(ENGINE, "fv_vintages.json")
DATA_JS = "assets/data.js"
# The published line. A fair value only ever reached a reader through main.
MAIN_REF = "origin/main"

def _git(*args) -> str:
    return subprocess.run(["git", "-C", ROOT] + list(args),
                          capture_output=True, text=True, timeout=600).stdout


NODE_READER = r"""
const fs = require('fs');
// argv[2], NOT argv[1]: node's argv is [node, script, ...args]. Reading argv[1]
// hands this reader its OWN source, which then evaluates `require` inside a
// `new Function` scope and reports "require is not defined" — a perfectly
// self-consistent error message about a file nobody asked to read.
const target = process.argv[2];
if (!target || target === process.argv[1]) {
  process.stdout.write(JSON.stringify({error: 'no target file given (argv[2])'}));
  process.exit(0);
}
const src = fs.readFileSync(target, 'utf8');
// data.js is a series of top-level `const NAME = ...;` declarations with no
// exports. Evaluating it inside a function scope and then reading TICKERS out is
// how app.js sees it, which is the whole point: a checker that models the parser
// is checking a different file from the one that ships.
let T;
try {
  T = new Function(src + "\n;return typeof TICKERS === 'undefined' ? null : TICKERS;")();
} catch (e) {
  process.stdout.write(JSON.stringify({error: String(e && e.message || e)}));
  process.exit(0);
}
if (!T) { process.stdout.write(JSON.stringify({error: 'no TICKERS in this revision'})); process.exit(0); }
const out = {};
for (const k of Object.keys(T)) {
  const e = T[k] || {};
  if (!e.fair) continue;
  out[k] = {fair: {bear: e.fair.bear, base: e.fair.base, full: e.fair.full},
            spot: (e.spot === undefined ? null : e.spot),
            spot_date: (e.spotDate === undefined ? null : e.spotDate),
            code: (e.code === undefined ? null : e.code)};
}
process.stdout.write(JSON.stringify({tickers: out, total: Object.keys(T).length}));
"""


def parse_data_js(text: str) -> dict:
    """Every name's fair value, spot and exchange code out of one data.js.

    THROUGH A REAL JAVASCRIPT LOAD, never a regex. The first version of this
    reader matched entries with a non-greedy pattern and immediately invented a
    ticker called `hz` — a nested horizon object whose closing brace let the match
    run on and swallow a neighbouring `fair:` block — producing sixteen vintages
    for a name that does not exist. That is [R-ENF-03] exactly: a checker that
    models the parser is reading a different file from the one that ships, and
    this repo has already paid for that lesson once on a live ticker page. The
    excuse the first version gave for the regex, that node cannot load a
    historical blob, was simply false: the blob is written to a temp file and
    loaded, the same way app.js sees it.

    Returns {"tickers": {...}, "total": N} where N is EVERY name in the revision,
    fair value or not, so the caller can count what it read against a known total.
    """
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8") as fh:
        fh.write(text)
        blob_path = fh.name
    # .cjs, not .js: node resolves module type from the nearest package.json and
    # an ES-module context makes `require` undefined, which fails as a parse
    # error and would have been recorded as "this revision has no fair values".
    with tempfile.NamedTemporaryFile("w", suffix=".cjs", delete=False,
                                     encoding="utf-8") as fh:
        fh.write(NODE_READER)
        reader_path = fh.name
    try:
        r = subprocess.run(["node", reader_path, blob_path],
                           capture_output=True, text=True, timeout=120)
        if r.returncode != 0 or not r.stdout.strip():
            return {"error": "node exited %d: %s"
                             % (r.returncode, (r.stderr or "").strip()[:200])}
        return json.loads(r.stdout)
    finally:
        for p_ in (blob_path, reader_path):
            try:
                os.unlink(p_)
            except OSError:
                pass


def reconstruct(limit: Optional[int] = None) -> dict:
    """Walk data.js through git history and recover what each name was worth when.

    THE DATE IS THE COMMIT'S, NOT THE STUDY'S. A fair value appears in the
    repository when someone commits it, which may be days after it was struck and
    is certainly not the moment the study was written. Every reconstructed entry
    says so in its own record rather than in a note somewhere else.
    """
    # FIRST-PARENT ON main, and this is not a detail. A plain `git log` walks every
    # reachable commit, so a branch that carried a different fair value for a few
    # hours appears in the archive as a published vintage, and a merge makes the
    # value flip back and forth on one date. AMOC read as TWELVE vintages that way,
    # alternating 5.95 and 8.64 within a single day, none of which the site ever
    # served. A vintage is what MAIN carried, because that is what deploys.
    ref = _git("rev-parse", "--verify", "--quiet", MAIN_REF).strip() or "HEAD"
    revs = [l for l in _git("log", "--first-parent", ref, "--format=%H %aI",
                            "--", DATA_JS).splitlines() if l]
    if limit:
        revs = revs[:limit]
    series: Dict[str, List[dict]] = {}
    parse_failures = []
    seen_names = set()
    total_seen: Dict[str, int] = {}
    for line in revs:
        sha, when = line.split(None, 1)
        blob = _git("show", "%s:%s" % (sha, DATA_JS))
        if not blob:
            parse_failures.append((sha[:8], "data.js not present at this commit"))
            continue
        res = parse_data_js(blob)
        if res.get("error"):
            parse_failures.append((sha[:8], res["error"]))
            continue
        parsed = res.get("tickers") or {}
        if not parsed:
            # An empty parse is not an empty file. [R-ENF-04]
            parse_failures.append((sha[:8], "loaded %d names and none carried a "
                                            "fair value" % res.get("total", 0)))
            continue
        total_seen[sha[:8]] = res.get("total", 0)
        seen_names |= set(parsed)
        for name, rec in parsed.items():
            prev = series.get(name, [])
            if prev and prev[-1]["fair"] == rec["fair"]:
                # Same value, older commit: keep the EARLIER appearance, which is
                # when the house started saying it, and drop the repetition. A
                # vintage archive records changes, not commits.
                prev[-1]["first_seen"] = when[:10]
                prev[-1]["first_seen_commit"] = sha[:8]
                continue
            series.setdefault(name, []).append({
                "source": "reconstructed",
                "fair": rec["fair"],
                "spot": rec["spot"],
                "spot_date": rec["spot_date"],
                "code": rec["code"],
                "first_seen": when[:10],
                "first_seen_commit": sha[:8],
                "date_meaning": ("the commit that introduced this value, NOT the "
                                 "date the study was struck"),
            })
    for name in series:
        series[name] = list(reversed(series[name]))
    return {"series": series, "revisions_walked": len(revs),
            "ref": ref,
            "names_seen": sorted(seen_names), "parse_failures": parse_failures,
            "names_in_latest_revision": (max(total_seen.values())
                                         if total_seen else 0)}


def load() -> dict:
    if os.path.exists(ARCHIVE):
        return json.load(open(ARCHIVE, encoding="utf-8"))
    return {"_": "", "series": {}}


def record(name: str, bear: float, base: float, full: float, *, struck: str,
           spot: Optional[float], spot_date: Optional[str],
           standard: Optional[str] = None, note: str = "") -> dict:
    """Write one PUBLISHED vintage, at the moment it is published.

    This is the half that matters. Everything reconstructed from git history is
    an inference about when a number appeared; this is a record of when it was
    struck, made by the thing that struck it.

    The spot may be None and that is allowed — a vintage whose price at the time
    is genuinely unknown is recorded WITHOUT one rather than with a plausible
    substitute, because log(FV/P) against the wrong price is not a weaker
    observation, it is a wrong one that no later reader can spot.
    """
    if not (bear <= base <= full):
        raise SystemExit("FATAL: %s fair range is not ordered bear <= base <= "
                         "full (%s, %s, %s). A range that crosses itself is an "
                         "input error, not a finding." % (name, bear, base, full))
    d = load()
    entries = d["series"].setdefault(name.upper(), [])
    entry = {
        "source": "recorded",
        "fair": {"bear": float(bear), "base": float(base), "full": float(full)},
        "spot": (float(spot) if spot is not None else None),
        "spot_date": spot_date,
        "struck": struck,
        "standard_version": standard,
        "date_meaning": "the date the study was struck, recorded at publication",
    }
    if note:
        entry["note"] = note
    if any(e.get("source") == "recorded" and e.get("struck") == struck
           and e.get("fair") == entry["fair"] for e in entries):
        return d                                    # idempotent re-run, not a new vintage
    entries.append(entry)
    entries.sort(key=lambda e: (e.get("struck") or e.get("first_seen") or ""))
    json.dump(d, open(ARCHIVE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return d


def build(limit: Optional[int] = None) -> int:
    """Seed or refresh the reconstructed half, leaving every recorded entry alone."""
    rec = reconstruct(limit=limit)
    d = load()
    kept = 0
    for name, entries in rec["series"].items():
        prev = [e for e in d["series"].get(name, []) if e.get("source") == "recorded"]
        kept += len(prev)
        d["series"][name] = sorted(entries + prev,
                                   key=lambda e: (e.get("struck")
                                                  or e.get("first_seen") or ""))
    d["_"] = ("A dated archive of every fair value this house has published. "
              "GENERATED for the reconstructed half by "
              "engine/valuation_calibration/fv_vintages.py; the RECORDED half is "
              "written at publication and is never regenerated. Read this rather "
              "than walking git history: assets/data.js carries one undated "
              "fair{} per name, so the question 'what did we say this was worth "
              "in March' has no other answer.")
    d["reconstruction"] = {
        "ref": rec.get("ref"),
        "ref_meaning": ("first-parent history of the published line. A branch's "
                        "fair value is not a vintage: only what main carried ever "
                        "reached a reader."),
        "revisions_walked": rec["revisions_walked"],
        "names_seen": len(rec["names_seen"]),
        "earliest": min((e["first_seen"] for es in rec["series"].values()
                         for e in es), default=None),
        "latest": max((e["first_seen"] for es in rec["series"].values()
                       for e in es), default=None),
        "parse_failures": rec["parse_failures"],
        "clone_depth_warning": (
            "The reconstruction can only see as far back as this clone's history. "
            "A SHALLOW clone silently yields a shorter archive that looks "
            "complete, so the walked-revision count and the earliest date are "
            "recorded here and any consumer reads them rather than assuming a "
            "span."),
        "shallow_clone": os.path.exists(os.path.join(ROOT, ".git", "shallow")),
    }
    json.dump(d, open(ARCHIVE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    n = sum(len(v) for v in d["series"].values())
    print("wrote %s — %d names, %d vintages (%d recorded, %d reconstructed) "
          "over %d revisions of %s, %s to %s%s"
          % (os.path.relpath(ARCHIVE, ROOT), len(d["series"]), n, kept, n - kept,
             rec["revisions_walked"], DATA_JS,
             d["reconstruction"]["earliest"], d["reconstruction"]["latest"],
             "  [SHALLOW CLONE — the archive is as short as the clone]"
             if d["reconstruction"]["shallow_clone"] else ""))
    if rec["parse_failures"]:
        print("  %d revisions could not be parsed and are listed in the archive "
              "rather than dropped:" % len(rec["parse_failures"]))
        for sha, why in rec["parse_failures"][:5]:
            print("    %s  %s" % (sha, why))
    return 0


def report(name: Optional[str] = None) -> dict:
    d = load()
    if name:
        es = d["series"].get(name.upper(), [])
        print("%s — %d vintages" % (name.upper(), len(es)))
        for e in es:
            f = e["fair"]
            print("  %-10s %-12s bear %-9s base %-9s full %-9s  spot %s"
                  % (e.get("source"), e.get("struck") or e.get("first_seen"),
                     f["bear"], f["base"], f["full"],
                     e.get("spot") if e.get("spot") is not None else "unknown"))
        return d
    moved = {k: v for k, v in d["series"].items() if len(v) > 1}
    print("fair-value vintages — %d names, %d vintages, %d names with more than one"
          % (len(d["series"]), sum(len(v) for v in d["series"].values()), len(moved)))
    r = d.get("reconstruction") or {}
    print("  reconstructed from %s revisions of %s, %s to %s%s"
          % (r.get("revisions_walked"), DATA_JS, r.get("earliest"), r.get("latest"),
             "   [SHALLOW CLONE]" if r.get("shallow_clone") else ""))
    for k, v in sorted(moved.items(), key=lambda kv: -len(kv[1]))[:12]:
        print("     %-12s %d vintages, %s -> %s"
              % (k, len(v), v[0]["fair"]["base"], v[-1]["fair"]["base"]))
    return d


if __name__ == "__main__":
    import sys
    a = sys.argv[1:]
    if a and a[0] == "build":
        raise SystemExit(build())
    report(a[0] if a else None)
