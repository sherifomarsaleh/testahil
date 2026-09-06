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
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OWNER, REPO = "sherifomarsaleh", "testahil"
API = f"https://api.github.com/repos/{OWNER}/{REPO}"


# ---------------------------------------------------------------- plumbing
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import check_publish_block as publish_block      # imported, never re-implemented


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
def sync_main(ticker: str, republish: bool = False) -> None:
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
    # ...AND THE REFUSAL IS ALSO PREVENTABLE, NOT ONLY DIAGNOSABLE. Step 2 of this
    # very script regenerates the derived surfaces INTO the working tree, so the
    # second invocation always arrives here dirty -- which is exactly the run where
    # origin/main has moved and the merge matters most. Committing first is what a
    # human does by hand at this point ("Regenerate the derived surfaces for the ADIB
    # republish"); doing it here is what lets an interrupted publish be re-run without
    # a human in the loop. Stash+pop would collide in assets/data.js for the same
    # reason the merge does, one step later and with a stash still to unwind.
    # A CONFLICTED TREE IS NOT A DIRTY TREE, AND `git add -A` TURNS AN HONEST
    # FAILURE INTO A COMMITTED CORRUPTION (30-Aug-2026). When the merge below
    # hits conflicts this script dies correctly — but it leaves the tree in an
    # unmerged state, and on the NEXT run `git status --porcelain` is non-empty,
    # so this branch used to `git add -A` the conflict markers and commit them.
    # Measured: 106 pages shipped with literal <<<<<<< HEAD in them, the merge
    # concluded itself, and the re-run then printed "branch is current with
    # origin/main" — the failure the previous run reported had been erased by
    # obeying its own instruction to re-run. Refuse instead: unmerged paths are
    # resolved by a human, never swept into a commit.
    unmerged = run(["git", "diff", "--name-only", "--diff-filter=U"]).split()
    if unmerged:
        die("the working tree has UNRESOLVED merge conflicts from an earlier run — "
            "resolve these files, `git add` them, commit, then re-run:\n    "
            + "\n    ".join(unmerged)
            + "\n\n  Resolve ADDITIVELY: keep main's new ticker rows AND this ticker's"
              "\n  row. Keep SITE.latest as main has it unless this is a first publish."
              "\n  This script will NOT `git add -A` over a conflicted tree.")

    if run(["git", "status", "--porcelain"]).strip():
        print("  working tree is dirty — committing it before the merge "
              "(git refuses to start a merge over uncommitted overlapping edits)")
        run(["git", "add", "-A"])
        run(["git", "commit", "-q", "-m",
             f"Regenerate the derived surfaces for the {ticker} "
             f"{'republish' if republish else 'publish'}\n\n"
             f"Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"])

    p = subprocess.run(["git", "merge", "origin/main", "--no-edit"],
                       cwd=ROOT, text=True, capture_output=True)
    if p.returncode != 0:
        # A FAILED MERGE IS NOT ALWAYS A CONFLICT, AND SAYING SO SENDS THE READER
        # TO THE WRONG FILE (24-Aug-2026). This branch used to assume every non-zero
        # exit meant conflicted content and printed `--diff-filter=U`. When git
        # REFUSES TO START the merge -- "Your local changes to the following files
        # would be overwritten" -- there are no unmerged paths, so that list is
        # EMPTY: the script printed "hit conflicts -- resolve by hand" followed by
        # nothing at all, and the actual cause (uncommitted edits overlapping main's)
        # never appeared. The remedies are opposites, which is what makes the
        # misdiagnosis expensive: a real conflict is resolved in the file, a refused
        # merge is resolved by committing first. Distinguish them on the unmerged
        # set, and when there is none, relay git's own words rather than a guess.
        conflicts = run(["git", "diff", "--name-only", "--diff-filter=U"]).split()
        if conflicts:
            die("merge of origin/main hit conflicts — resolve by hand, then re-run:\n    "
                + "\n    ".join(conflicts)
                + "\n\n  Resolve ADDITIVELY: keep main's new ticker rows AND this ticker's"
                  "\n  row. Keep SITE.latest as main has it unless this is a first publish"
                  "\n  (a republish must not hijack the homepage hero).")
        die("git REFUSED to start the merge of origin/main — this is NOT a content "
            "conflict, so there is nothing to resolve in a file. git said:\n\n    "
            + "\n    ".join(((p.stderr or "") + (p.stdout or "")).strip().splitlines()[:12])
            + "\n\n  Almost always: this ticker's edits are still uncommitted and touch "
              "files\n  main also moved. Commit them on this branch first, then re-run — "
              "the\n  merge can then resolve normally, and any real conflict will be "
              "reported\n  by the branch above with the files actually named.")
    print("  merged origin/main cleanly")


def ledger_instrument(key: str) -> str:
    """The LEDGER's name for a published key -- NOT always the key itself.

    Imported from engine/apply_technicals rather than copied: that map is the one
    place these aliases live (metal_backtest and rollforward_one both read it).
    Platinum publishes as METALS.PLATINUM on platinum.html but grades under
    instrument:"Platinum"; gold, silver, Samsung and Kakao differ in case."""
    sys.path.insert(0, os.path.join(ROOT, "engine"))
    from apply_technicals import LEDGER_ALIAS
    return LEDGER_ALIAS.get(key, key)


def market_of(ticker: str) -> str | None:
    """Market for a published key, from the SAME authority the site itself uses.

    RESOLVED THROUGH THE GENERATED REGISTRY (assets/markets.js), not from the
    entry's `code` prefix. Market is decided by FILE PLACEMENT --
    engine/raw_ohlc/{MARKET}/{TICKER}.csv -- which is what
    build_market_registry.py reads and what ledger.html, the picker and every
    other surface group by. Step 2 regenerates that registry immediately before
    this is called, so it is never stale here.

    WHY THIS STOPPED BEING A HAND-LISTED MAP (24-Aug-2026). The map was patched
    once per defect and each patch closed only the instance in front of it:

      - 9-Aug   SWDY/SCEM/EGCH shipped live and invisible on the Ticker Picker.
      - 23-Aug  the three metals live in `const METALS = {...}`, so all three
                resolved to None; fixed by reading both objects and adding
                "XAU/USD"/"XPT/USD".
      - 23-Aug  every Qatari name carries QSE: while the map held only QE:;
                fixed by sourcing the equity half from apply_technicals.
      - 24-Aug  SILVER's code is "XAG/USD", which that metals patch did not
                list -- so SILVER alone of the 93 published keys resolved to
                None. Two things follow silently from that one None: step 2
                SKIPS the fair-value overlay ("no market resolved"), and step 4
                misses the non-equity exemption and instead demands SILVER
                appear on the EQUITY registers, where no metal has ever been --
                i.e. a silver republish is blocked outright by a gate asserting
                something that was never true.

    Four instances, one class: a hand-maintained table standing in for a fact
    the repo already computes from file placement. So the table stops being the
    decision. The `code` prefix survives only as a fallback for a key the
    registry has no row for, which today is none of the 93.

    Loaded in node rather than regexed: markets.js exports marketOf(), which
    already handles the LEDGER-vs-TICKERS spelling split (Gold/Samsung/Kakao),
    and re-implementing that lookup here is how the two would drift apart."""
    js = ("const fs=require('fs'),vm=require('vm');const c={};vm.createContext(c);"
          "vm.runInContext(fs.readFileSync('assets/markets.js','utf8'),c);"
          f"process.stdout.write(String(c.marketOf({json.dumps(ticker)}) || ''));")
    mkt = run(["node", "-e", js]).strip()
    if mkt:
        return mkt

    # Fallback: the published entry's own `code` prefix, read by LOADING data.js
    # (both objects -- the metals are entries of `const METALS = {...}`), never by
    # regex: a regex over a file this size has already mis-parsed it once.
    js = ("const fs=require('fs'),vm=require('vm');const c={};vm.createContext(c);"
          "vm.runInContext(fs.readFileSync('assets/data.js','utf8')"
          "+';globalThis.__T=Object.assign({},typeof METALS!==\"undefined\"?METALS:{},TICKERS);',c);"
          f"process.stdout.write(String((c.__T[{json.dumps(ticker)}]||{{}}).code||''));")
    code = run(["node", "-e", js]).strip()
    sys.path.insert(0, os.path.join(ROOT, "engine"))
    from apply_technicals import EXCHANGE_MARKET
    return {**EXCHANGE_MARKET,
            "XPT/USD": "XPT", "XAU/USD": "XAU"}.get(code.split(":")[0])



def surfaces(ticker: str) -> None:
    """All generated surfaces, in dependency order. Never hand-edit these."""
    step("2/6", "regenerating the derived surfaces")
    print(run(["node", "scripts/generate_seo.js"]).strip()[-300:])
    print(run(["node", "scripts/generate_feed.js"]).strip()[-200:])
    print(run(["python3", "scripts/build_market_registry.py", "--write"]).strip()[-200:])
    # 6. THE PRICES BLOCK — the freshest price this repository HOLDS for each covered
    # name, which is NOT TICKERS[k].spot: spot is the price a cone was struck at, and
    # [R-GAP-01] measures a fair value against the LATEST KNOWN price. A roll-forward
    # moves a library, so it moves the answer this block's own readers give, and the
    # block goes stale in the same pass that made it stale.
    #
    # IT WAS MISSING FROM THIS LIST AND FOUR PUBLISHES IN ONE AFTERNOON WENT RED ON IT
    # — ARCC, PHAR, QNB and SCEM, every one for the identical reason and every one
    # after its surfaces had been "regenerated". That is the surface-4 defect exactly
    # (the Ticker Picker overlay nothing rebuilt, three names live and invisible), and
    # the answer is the same one: a generated surface that is not in this function is a
    # surface somebody has to remember, and the record says nobody does.
    print(run(["python3", "scripts/build_prices_block.py"]).strip()[-200:])
    # The Ticker Picker reads a GENERATED overlay that nothing here used to rebuild, so a
    # published name simply was not on that page — SWDY, SCEM and EGCH all shipped green
    # and invisible. The overlay now covers every fitted market (see step 5 below).
    # these run last: they rewrite the ticker's own data.js block, so the entry must exist.
    print(run(["python3", "engine/ta_chart.py", "--only", ticker, "--write"]).strip()[-200:])
    print(run(["python3", "engine/apply_technicals.py", "--only", ticker,
               "--write"]).strip()[-300:])
    # 5. the fair-value overlay feeds picker.html. It was NOT in this list, so four
    # consecutive EG publishes shipped without ever reaching the Ticker Picker — the
    # page simply read a file nobody had regenerated.
    #
    # It rebuilds EVERY market in one file — fv_overlay resolves each row's market from
    # the registry and prices it with that market's own profile and cash hurdle, so no
    # --market argument is needed or wanted. The page sections by market on top of that,
    # which only holds together if the whole file is rebuilt at once.
    mkt = market_of(ticker)
    if mkt:
        out = run(["python3", "engine/fv_overlay.py",
                   "--js", "assets/fv_overlay.js"])
        blocked = [l for l in out.splitlines() if "BLOCKED" in l]
        # BLOCKED USED TO MEAN "ABSENT FROM THE PICKER". It no longer always does
        # (24-Aug-2026). picker.html now LISTS a name whose fair value is merely in the
        # wrong unit — a corporate action changed the share count after the study was
        # priced, so no honest gap exists — showing its price and dashing every
        # fair-value-derived cell. That name reaches the reader; it just does not claim
        # a gap it cannot compute. Failing the publish on it would be enforcing a
        # premise that is no longer true, and the only way past would be to re-base the
        # study's number from a publish script, which is a research decision.
        #
        # The check stays for every OTHER block reason, because those really do drop
        # the row. And it is no longer the last word either way: check_ticker_surfaces
        # renders the picker in a browser and asserts the ticker is in the DOM, which
        # is the claim this guard was always a proxy for.
        SOFT_BLOCKS = ("share basis changed since the fair value was struck",)
        if blocked:
            hard = [l for l in blocked if not any(s in l for s in SOFT_BLOCKS)]
            soft = [l for l in blocked if l not in hard]
            if hard:
                print("  fv_overlay BLOCKED rows (these names will NOT appear in the picker):")
                for l in hard:
                    print("   ", l.strip()[:150])
            if soft:
                print("  fv_overlay blocked WITHOUT a gap, still listed on the picker:")
                for l in soft:
                    print("   ", l.strip()[:150])
            if any(ticker in l for l in hard):
                die(f"{ticker} is BLOCKED from the fair-value overlay — it would publish "
                    f"without reaching the Ticker Picker. Most often the entry is missing "
                    f"`fairAsof` (the close the FAIR VALUE is struck on); without it the "
                    f"overlay falls back to the publication date in the study filename and "
                    f"reports look-ahead against the cone anchor.")
        print("  fv_overlay regenerated for every fitted market")
    else:
        print(f"  no market resolved for {ticker} — fv_overlay not regenerated")

    mirror_legacy_assets()


def mirror_legacy_assets() -> None:
    """Keep legacy/assets/ in step with assets/ — SIX SURFACES DEPEND ON IT.

    The 30-Aug-2026 cutover snapshotted assets/ into legacy/assets/ and left the
    legacy pages loading it RELATIVELY, so /legacy/ledger.html reads
    /legacy/assets/data.js, not the copy this publish just rewrote. Nothing synced
    the two, and the snapshot had never been updated — this is simply the first
    publish since the cutover, so the divergence had not had a chance to show yet.

    It matters because root ledger.html, picker.html, trade.html and portfolio.html
    are all redirect stubs: the only WORKING copies are the legacy ones. A frozen
    snapshot therefore does not age gracefully, it silently stops the public
    forecast ledger from ever showing another grade, while /EMAARDEV/study/ (new
    IA, absolute /assets/) shows the fresh cone — the same site quoting two prices
    for one stock on the same day.

    Copy only files legacy ALREADY has: legacy/assets is a snapshot of the surfaces
    the old site reads, not a mirror of everything in assets/, and adding test.js or
    editions.json to it would be inventing content the archive never had.
    """
    src = os.path.join(ROOT, "assets")
    dst = os.path.join(ROOT, "legacy", "assets")
    if not os.path.isdir(dst):
        print("  no legacy/assets — nothing to mirror")
        return
    copied = []
    for name in sorted(os.listdir(dst)):
        a, b = os.path.join(src, name), os.path.join(dst, name)
        if not os.path.isfile(a) or not os.path.isfile(b):
            continue
        if open(a, "rb").read() != open(b, "rb").read():
            shutil.copyfile(a, b)
            copied.append(name)
    # [R-ENF-04] Report what was examined, not just what changed.
    print(f"  legacy/assets mirrored — {len(os.listdir(dst))} file(s) checked, "
          + (f"{len(copied)} updated: {', '.join(copied)}" if copied else "0 updated"))


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


def served_page(name: str, marker: str) -> str:
    """Repo-relative path of the page a READER actually gets for `name`.

    Since the 30-Aug-2026 cutover the root slugs are redirect stubs and the
    preserved study pages live under legacy/ (still served). A file:// render of
    the stub executes its location.replace() against a file URL and lands
    nowhere, so the check reported "did not render its valuation gauge" for a
    page that was fine — pointing the reader at the data when the fault was the
    path. Resolve on the MARKER the check is about to look for, exactly as
    check_data_freshness.py resolves HAS_BACKTEST: root wins if it ever carries
    the set again, legacy/ otherwise.
    """
    root_p = os.path.join(ROOT, name)
    if os.path.exists(root_p) and marker in open(root_p, encoding='utf-8').read():
        return name
    legacy_p = os.path.join(ROOT, 'legacy', name)
    if os.path.exists(legacy_p) and marker in open(legacy_p, encoding='utf-8').read():
        return f'legacy/{name}'
    # [R-ENF-04] Neither copy carries the marker: that is a finding, not a default.
    die(f"no served copy of {name} carries {marker!r} — checked {root_p} and "
        f"{legacy_p}. The page layout moved, or the page was never written.")


def render_verify(ticker: str) -> None:
    """Verify by RENDER, not by grep: the markup looks correct either way. Loads the
    ticker page and ledger.html in headless Chromium and reads the DOM."""
    step("4/6", "verifying by render (headless)")
    js = r"""
const { chromium } = require('playwright');
(async () => {
  const TKP  = process.argv[2];   // ticker page   -> repo-relative served path
  const INST = process.argv[3];   // LEDGER name   -> listed in the ledger page
  const LEDP = process.argv[5];   // ledger page   -> repo-relative served path
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium',
                                    args: ['--no-sandbox'] });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(String(e)));
  // Hermetic render: every assertion below reads DOM built by LOCAL scripts
  // (data.js/app.js) off file://. Third-party fonts/analytics are not what is
  // being verified, and on a sandboxed runner one hanging external fetch stalls
  // the 'load' event until the gate times out — so external requests are blocked
  // and navigation waits on the DOM, which is the thing actually asserted on.
  await p.route('**/*', r =>
    r.request().url().startsWith('file://') ? r.continue() : r.abort());
  const base = 'file://' + process.argv[4] + '/';
  await p.goto(base + TKP, { waitUntil: 'domcontentloaded' });
  await p.waitForTimeout(1500);
  const pageOK = (await p.content()).includes('id="gauge"');
  await p.goto(base + LEDP, { waitUntil: 'domcontentloaded' });
  await p.waitForTimeout(1800);
  const body = await p.innerText('body');
  const listed = new RegExp('\\b' + INST + '\\b').test(body);
  console.log(JSON.stringify({ pageOK, listed, errors: errs }));
  await b.close();
})();
"""
    path = os.path.join(ROOT, ".publish_render_check.js")
    open(path, "w").write(js)
    try:
        env = dict(os.environ, NODE_PATH=os.environ.get(
            "NODE_PATH", "/opt/node22/lib/node_modules"))
        # TWO names, not one. The page is {ticker}.html; the ledger lists the
        # LEDGER instrument. For every equity they are the same string, which is
        # why one argument survived this long -- but platinum's page is
        # platinum.html while its rows say Platinum, so the single-arg version
        # failed on a correctly published metal and blamed the market registry.
        tk_page = served_page(f"{ticker.lower()}.html", 'id="gauge"')
        led_page = served_page("ledger.html", "HAS_BACKTEST")
        p = subprocess.run(["node", path, tk_page, ledger_instrument(ticker),
                            ROOT, led_page],
                           cwd=ROOT, text=True,
                           capture_output=True, timeout=300, env=env)
        if p.returncode != 0:
            die(f"render check could not run:\n{(p.stdout + p.stderr)[:1500]}")
        res = json.loads(p.stdout.strip().splitlines()[-1])
    finally:
        os.path.exists(path) and os.remove(path)
    inst = ledger_instrument(ticker)
    if not res["pageOK"]:
        die(f"{tk_page} did not render its valuation gauge")
    if not res["listed"]:
        die(f"{inst} does not appear in {led_page}'s rendered DOM — check the "
            f"market registry (MARKET_OF) and the LEDGER rows")
    if res["errors"]:
        die(f"page errors on render: {res['errors'][:3]}")
    label = ticker if inst == ticker else f"{ticker} (as {inst})"
    print(f"  {tk_page} renders · {label} listed in {led_page} · 0 page errors")

    # The ticker's own page and the ledger were the only two surfaces ever verified here.
    # Everything else was taken on trust and drifted: three publishes in a row went out
    # missing from the Ticker Picker. This checks every page that is supposed to carry
    # every covered name, by rendering it and reading the DOM a reader would see.
    env = dict(os.environ, NODE_PATH=os.environ.get(
        "NODE_PATH", "/opt/node22/lib/node_modules"))
    # NON-EQUITY NAMES ARE EXEMPT, LOUDLY (23-Aug-2026). check_ticker_surfaces.js
    # drives the EQUITY registers -- stocks, Trade, Portfolio and the Ticker Picker.
    # No metal has ever appeared on any of them: gold, silver and platinum are all
    # absent today and fv_overlay emits no metals rows. That script's own header
    # lists metals.html among the surfaces deliberately excluded as "prose and
    # non-equity". So on a metal this gate demanded something that has never been
    # true, failed with "not in TICKERS -- nothing to check", and blocked the
    # publish. Skipping is right; skipping SILENTLY is not, because the day metals
    # do join those registers this line is what has to change.
    if market_of(ticker) in ("XAU", "XPT"):
        print(f"  SKIP — {ticker} is a non-equity name. The register surfaces this "
              f"gate checks (stocks/Trade/Portfolio/Picker) carry equities only; "
              f"metals are published on metals.html and ledger.html, both of which "
              f"step 4 already verified by render.")
        return
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

    # [R-GAP-02] — THE FIRST THING, BEFORE ANY WORK IS DONE. A study more than 30%
    # from the latest known price does not reach the live site until that is sorted
    # or an evidenced market dissent releases it. This runs ahead of the build
    # rather than beside the other gates because a name that may not publish should
    # cost nothing to discover, and because a gate placed later is one somebody
    # eventually reaches for --ship past.
    step("0/6", "publication limit [R-GAP-02]")
    ok, why, rows = publish_block.verdict(tk)
    for label, v, g in rows:
        print(f"    {label:<46} {v:10.2f}  {g*100:+7.1f}%")
    if not ok:
        die(f"{tk} MAY NOT PUBLISH — {why}.\n"
            f"  Either close the gap in the study, or file "
            f"engine/{tk.lower()}_study/MARKET_DISSENT_{{DD-MM-YYYY}}.md carrying "
            f"MECHANISM, REVERSE READ, WHY NOT CREDIBLE, WHAT WE CHECKED and "
            f"FALSIFIER, with a DISSENT_AT_GAP line matching the current gap.\n"
            f"  Run: python3 scripts/check_publish_block.py --ticker {tk}")
    print(f"    {why}")

    print(f"publishing {tk}" + (" (republish)" if a.republish else ""))
    step("1/6", "syncing with origin/main")
    sync_main(tk, a.republish)
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
