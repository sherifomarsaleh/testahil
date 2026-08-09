#!/usr/bin/env python3
"""Take a prepared ticker from the working tree to LIVE on testahil.com.

WHY THIS EXISTS. "Publish" used to mean "build everything, then stop and ask for a
token" — so a publish reliably ended one step short of being published, and the
person who asked for it had to notice and say "merge". It also regenerated the four
derived surfaces by hand, which is the failure mode that has recurred most often in
this repo (ELEC shipped outside its own exchange group because one of the four was
skipped; nothing threw).

This script owns the MECHANICAL half of publishing, end to end:

    surfaces -> gates -> render-verify -> commit -> push -> PR -> merge -> deploy check

It does NOT own the judgment half. Writing the TICKERS entry, the page, the coverage
rows, the LEDGER cohort and the ledger sweep stay with the analyst/agent, because they
are decisions, not steps. Run this once those edits are sitting in the working tree.

USAGE
    python3 scripts/publish_site.py --ticker SWDY                 # build + verify only
    python3 scripts/publish_site.py --ticker SWDY --ship          # ...+ commit, push, PR, merge
    python3 scripts/publish_site.py --ticker SWDY --ship --republish
                                          # skip first-publish-only steps (calibration
                                          # artifacts, HAS_BACKTEST, cycle-1 rows)

--ship needs a GitHub token with `repo` scope in GITHUB_TOKEN or GH_TOKEN. Without one
it stops after the push and prints exactly what is left to do — it never pretends to
have merged.

EVERY STEP FAILS LOUDLY. A publish that half-works is worse than one that stops.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OWNER, REPO = "sherifomarsaleh", "testahil"
API = f"https://api.github.com/repos/{OWNER}/{REPO}"


# ---------------------------------------------------------------- plumbing
def run(cmd: list[str], *, capture: bool = True, check: bool = True) -> str:
    """Run a command in the repo root. Non-zero exit is fatal unless check=False."""
    p = subprocess.run(cmd, cwd=ROOT, text=True,
                       capture_output=capture, timeout=900)
    if check and p.returncode != 0:
        out = (p.stdout or "") + (p.stderr or "")
        die(f"command failed: {' '.join(cmd)}\n{out.strip()[:4000]}")
    return (p.stdout or "") if capture else ""


def die(msg: str) -> "NoReturn":  # type: ignore[valid-type]
    print(f"\n  FAIL  {msg}\n", file=sys.stderr)
    sys.exit(1)


def step(n: str, msg: str) -> None:
    print(f"\n[{n}] {msg}")


def api(method: str, path: str, token: str, body: dict | None = None) -> dict:
    req = urllib.request.Request(
        f"{API}{path}", method=method,
        data=json.dumps(body).encode() if body else None,
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json",
                 "User-Agent": "testahil-publish"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:1500]
        raise RuntimeError(f"{method} {path} -> {e.code}: {detail}") from None


# ---------------------------------------------------------------- steps
def sync_main(ticker: str) -> None:
    """Merge origin/main first. Other publishes land while a branch is open, and they
    always collide in the same two shared files. Resolving AFTER the surfaces are
    regenerated would ship a feed and a market registry built against the wrong set of
    tickers — which is exactly what happened on the SWDY republish (76 vs 79 names)."""
    run(["git", "fetch", "origin", "main", "-q"])
    behind = run(["git", "rev-list", "--count", "HEAD..origin/main"]).strip()
    if behind == "0":
        print("  branch is current with origin/main")
        return
    print(f"  origin/main is {behind} commit(s) ahead — merging before regenerating")
    p = subprocess.run(["git", "merge", "origin/main", "--no-edit"],
                       cwd=ROOT, text=True, capture_output=True)
    if p.returncode != 0:
        conflicts = run(["git", "diff", "--name-only", "--diff-filter=U"]).split()
        die("merge of origin/main hit conflicts — resolve by hand, then re-run:\n    "
            + "\n    ".join(conflicts)
            + "\n\n  Resolve ADDITIVELY: keep main's new ticker rows AND this ticker's"
              "\n  row. Keep SITE.latest as main has it unless this is a first publish"
              "\n  (a republish must not hijack the homepage hero).")
    print("  merged origin/main cleanly")


def market_of(ticker: str) -> str | None:
    """Market prefix from the ticker's own TICKERS entry ("EGX:PHAR" -> "EG").

    Parsed by LOADING data.js, not by regex: the entry is the authority on the
    market, and a regex over a file this size has already mis-parsed it once."""
    js = ("const fs=require('fs'),vm=require('vm');const c={};vm.createContext(c);"
          "vm.runInContext(fs.readFileSync('assets/data.js','utf8')+';globalThis.__T=TICKERS;',c);"
          f"process.stdout.write(String((c.__T[{json.dumps(ticker)}]||{{}}).code||''));")
    code = run(["node", "-e", js]).strip()
    return {"EGX": "EG", "ADX": "AE", "DFM": "AE", "TADAWUL": "SA",
            "QE": "QA"}.get(code.split(":")[0])


def surfaces(ticker: str) -> None:
    """All generated surfaces, in dependency order. Never hand-edit these."""
    step("2/6", "regenerating the derived surfaces")
    print(run(["node", "scripts/generate_seo.js"]).strip()[-300:])
    print(run(["node", "scripts/generate_feed.js"]).strip()[-200:])
    print(run(["python3", "scripts/build_market_registry.py", "--write"]).strip()[-200:])
    # The Ticker Picker reads a GENERATED overlay that nothing here used to rebuild, so a
    # published name simply was not on that page — SWDY, SCEM and EGCH all shipped green
    # and invisible. The overlay is fitted per market and only EG has a fit today.
    # these run last: they rewrite the ticker's own data.js block, so the entry must exist.
    print(run(["python3", "engine/ta_chart.py", "--only", ticker, "--write"]).strip()[-200:])
    print(run(["python3", "engine/apply_technicals.py", "--only", ticker,
               "--write"]).strip()[-300:])
    # 5. the fair-value overlay feeds picker.html. It was NOT in this list, so four
    # consecutive EG publishes shipped without ever reaching the Ticker Picker — the
    # page simply read a file nobody had regenerated. It is a per-MARKET file, so it is
    # rebuilt for the ticker's own market.
    mkt = market_of(ticker)
    if mkt:
        out = run(["python3", "engine/fv_overlay.py", "--market", mkt,
                   "--js", "assets/fv_overlay.js"])
        blocked = [l for l in out.splitlines() if "BLOCKED" in l]
        if blocked:
            print("  fv_overlay BLOCKED rows (these names will NOT appear in the picker):")
            for l in blocked:
                print("   ", l.strip()[:150])
            if any(ticker in l for l in blocked):
                die(f"{ticker} is BLOCKED from the fair-value overlay — it would publish "
                    f"without reaching the Ticker Picker. Most often the entry is missing "
                    f"`fairAsof` (the close the FAIR VALUE is struck on); without it the "
                    f"overlay falls back to the publication date in the study filename and "
                    f"reports look-ahead against the cone anchor.")
        print(f"  fv_overlay regenerated for {mkt}")
    else:
        print(f"  no market resolved for {ticker} — fv_overlay not regenerated")


def gates() -> None:
    step("3/6", "running the two gates")
    fresh = run(["python3", "scripts/check_data_freshness.py"])
    print(fresh.strip()[-400:])
    if "0 failure" not in fresh:
        die("check_data_freshness reported failures — see above")
    integ = run(["python3", "scripts/check_page_integrity.py"], check=False)
    print(integ.strip()[-400:])
    if "Clean" not in integ:
        die("check_page_integrity reported hard findings — see above")


def render_verify(ticker: str) -> None:
    """Verify by RENDER, not by grep: the markup looks correct either way. Loads the
    ticker page and ledger.html in headless Chromium and reads the DOM."""
    step("4/6", "verifying by render (headless)")
    js = r"""
const { chromium } = require('playwright');
(async () => {
  const TK = process.argv[2];
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium',
                                    args: ['--no-sandbox'] });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(String(e)));
  const base = 'file://' + process.argv[3] + '/';
  await p.goto(base + TK.toLowerCase() + '.html');
  await p.waitForTimeout(1500);
  const pageOK = (await p.content()).includes('id="gauge"');
  await p.goto(base + 'ledger.html');
  await p.waitForTimeout(1800);
  const body = await p.innerText('body');
  const listed = new RegExp('\\b' + TK + '\\b').test(body);
  console.log(JSON.stringify({ pageOK, listed, errors: errs }));
  await b.close();
})();
"""
    path = os.path.join(ROOT, ".publish_render_check.js")
    open(path, "w").write(js)
    try:
        env = dict(os.environ, NODE_PATH=os.environ.get(
            "NODE_PATH", "/opt/node22/lib/node_modules"))
        p = subprocess.run(["node", path, ticker, ROOT], cwd=ROOT, text=True,
                           capture_output=True, timeout=300, env=env)
        if p.returncode != 0:
            die(f"render check could not run:\n{(p.stdout + p.stderr)[:1500]}")
        res = json.loads(p.stdout.strip().splitlines()[-1])
    finally:
        os.path.exists(path) and os.remove(path)
    if not res["pageOK"]:
        die(f"{ticker.lower()}.html did not render its valuation gauge")
    if not res["listed"]:
        die(f"{ticker} does not appear in ledger.html's rendered DOM — check the "
            f"market registry (MARKET_OF) and the LEDGER rows")
    if res["errors"]:
        die(f"page errors on render: {res['errors'][:3]}")
    print(f"  {ticker.lower()}.html renders · {ticker} listed in ledger.html · 0 page errors")

    # The ticker's own page and the ledger were the only two surfaces ever verified here.
    # Everything else was taken on trust and drifted: three publishes in a row went out
    # missing from the Ticker Picker. This checks every page that is supposed to carry
    # every covered name, by rendering it and reading the DOM a reader would see.
    env = dict(os.environ, NODE_PATH=os.environ.get(
        "NODE_PATH", "/opt/node22/lib/node_modules"))
    p = subprocess.run(["node", "scripts/check_ticker_surfaces.js", ticker, ROOT],
                       cwd=ROOT, text=True, capture_output=True, timeout=300, env=env)
    print((p.stdout + p.stderr).strip())
    if p.returncode != 0:
        die(f"{ticker} is missing from a register surface — see above")


def commit_and_push(ticker: str, republish: bool) -> str:
    step("5/6", "committing and pushing")
    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip()
    if branch == "main":
        die("refusing to commit directly to main — publish from a working branch")
    if not run(["git", "status", "--porcelain"]).strip():
        print("  nothing to commit (working tree already clean)")
    else:
        run(["git", "add", "-A"])
        verb = "Republish" if republish else "Publish"
        run(["git", "commit", "-q", "-m",
             f"{verb} {ticker} to the website\n\n"
             f"Surfaces regenerated (sitemap/footer, feed, market registry, chart + "
             f"technicals); freshness and page-integrity gates clean; verified by "
             f"headless render.\n\n"
             f"Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"])
    run(["git", "push", "-u", "origin", branch, "-q"])
    print(f"  pushed {branch}")
    return branch


def ship(ticker: str, branch: str, token: str, republish: bool) -> None:
    """Open the PR, merge it, and confirm the Pages deploy actually ran green.
    A merge without a deploy check is not a publish."""
    step("6/6", "opening the PR, merging, confirming the deploy")
    prs = api("GET", f"/pulls?head={OWNER}:{branch}&state=open", token)
    if prs:
        pr = prs[0]
        print(f"  reusing open PR #{pr['number']}")
    else:
        verb = "Republish" if republish else "Publish"
        pr = api("POST", "/pulls", token, {
            "title": f"{verb} {ticker} to the website",
            "head": branch, "base": "main",
            "body": (f"{verb} **{ticker}** — surfaces regenerated, both gates clean, "
                     f"verified by headless render.\n\nShipped by "
                     f"`scripts/publish_site.py`.\n\n🤖 Generated with "
                     f"[Claude Code](https://claude.com/claude-code)")})
        print(f"  opened PR #{pr['number']}")

    try:
        api("PUT", f"/pulls/{pr['number']}/merge", token,
            {"merge_method": "squash",
             "commit_title": f"{'Republish' if republish else 'Publish'} {ticker} "
                             f"(#{pr['number']})"})
    except RuntimeError as e:
        if "merge conflicts" in str(e).lower():
            die("PR has merge conflicts — origin/main moved during the run. "
                "Re-run the script; it merges main first.")
        raise
    print(f"  merged PR #{pr['number']}")

    sha = api("GET", "/commits/main", token)["sha"]
    print(f"  main is now {sha[:8]} — waiting for the Pages deploy")
    for attempt in range(40):                       # ~10 min
        time.sleep(15)
        runs = api("GET", f"/actions/workflows/deploy-pages.yml/runs?per_page=5",
                   token).get("workflow_runs", [])
        mine = [r for r in runs if r["head_sha"] == sha]
        if not mine:
            continue
        r = mine[0]
        if r["status"] != "completed":
            print(f"    deploy {r['status']}…")
            continue
        if r["conclusion"] == "success":
            print(f"\n  LIVE — deploy succeeded on {sha[:8]}")
            print(f"  https://testahil.com/{ticker.lower()}.html")
            return
        die(f"Pages deploy CONCLUDED '{r['conclusion']}' on {sha[:8]} — the merge "
            f"landed but the site did not update: {r['html_url']}")
    print(f"\n  merged, but the deploy had not finished after 10 minutes.\n"
          f"  Check: https://github.com/{OWNER}/{REPO}/actions/workflows/deploy-pages.yml")


# ---------------------------------------------------------------- entry
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ticker", required=True, help="TICKERS key, e.g. SWDY")
    ap.add_argument("--ship", action="store_true",
                    help="commit, push, PR, merge and confirm the deploy")
    ap.add_argument("--republish", action="store_true",
                    help="an already-covered name: skip first-publish-only steps")
    a = ap.parse_args()
    tk = a.ticker.upper()

    if not os.path.exists(os.path.join(ROOT, f"{tk.lower()}.html")):
        die(f"{tk.lower()}.html does not exist — write the page before publishing")

    print(f"publishing {tk}" + (" (republish)" if a.republish else ""))
    step("1/6", "syncing with origin/main")
    sync_main(tk)
    surfaces(tk)
    gates()
    render_verify(tk)

    if not a.ship:
        print(f"\n  BUILT AND VERIFIED — not shipped (no --ship).\n"
              f"  Re-run with --ship to commit, push, merge and deploy.")
        return

    branch = commit_and_push(tk, a.republish)
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        print(f"\n  PUSHED but NOT MERGED — no GITHUB_TOKEN/GH_TOKEN in the environment.\n"
              f"  The site is unchanged until '{branch}' is merged into main.\n"
              f"  Merge it (PR against main, squash); Pages deploys automatically.")
        return
    ship(tk, branch, token, a.republish)


if __name__ == "__main__":
    main()
