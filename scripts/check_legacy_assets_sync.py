#!/usr/bin/env python3
"""check_legacy_assets_sync.py — legacy/assets must not drift from assets/.

WHY THIS EXISTS (30-Aug-2026). The cutover moved the new IA to root and
byte-preserved the old site under legacy/, snapshotting assets/ into
legacy/assets/. The legacy pages load their scripts RELATIVELY, so
/legacy/ledger.html reads /legacy/assets/data.js while /EMAARDEV/study/ reads
/assets/data.js. Nothing synced them and nothing checked them.

That is not a cosmetic split. Root ledger.html, picker.html, trade.html and
portfolio.html are ALL redirect stubs — the only working copies are the legacy
ones — so a frozen legacy/assets/data.js means the public forecast ledger never
shows another grade, while the new IA shows a fresh cone for the same name on
the same day. The first roll-forward after the cutover (EMAARDEV, 30-Aug-2026)
is what surfaced it; before that nothing had changed data.js, so the two copies
were still byte-identical and the hazard was invisible.

[R-ENF-01] A rule that can be checked must be checked FROM OUTSIDE the thing it
governs. publish_site.py now mirrors the two; this asserts the result rather
than trusting that it ran.

[R-ENF-04] An empty result is not a clean result: a missing or empty
legacy/assets is a FINDING, not a pass. The population is counted and printed.

Scope: only files legacy ALREADY carries. legacy/assets is a snapshot of the
surfaces the old site reads, not a mirror of everything under assets/ — root-only
files (test.js, editions.json, prose/) are correctly absent and are not flagged.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets")
DST = os.path.join(ROOT, "legacy", "assets")


def main() -> int:
    if not os.path.isdir(DST):
        print("legacy/assets does not exist — nothing served under /legacy/ reads a "
              "snapshot, so this check does not apply. If the cutover is still in "
              "place this is itself the finding.")
        return 0
    names = sorted(n for n in os.listdir(DST) if os.path.isfile(os.path.join(DST, n)))
    if not names:
        print("FAIL — legacy/assets exists but is EMPTY. Refusing to report clean "
              "having compared nothing.")
        return 1

    drifted, missing = [], []
    for n in names:
        a, b = os.path.join(SRC, n), os.path.join(DST, n)
        if not os.path.isfile(a):
            missing.append(n)
            continue
        if open(a, "rb").read() != open(b, "rb").read():
            drifted.append(n)

    print(f"compared {len(names)} file(s) in legacy/assets against assets/")
    if missing:
        print(f"  note: {len(missing)} legacy-only file(s), no root counterpart to "
              f"compare: {', '.join(missing)}")
    if drifted:
        print(f"\nFAIL — {len(drifted)} file(s) drifted from assets/:")
        for n in drifted:
            print(f"    legacy/assets/{n}")
        print("\n  The legacy pages are SERVED and read these relatively, so a reader "
              "on /legacy/ gets\n  these bytes, not assets/. Re-run "
              "`python3 scripts/publish_site.py --ticker TK --republish`,\n  which "
              "mirrors them, or copy them across deliberately.")
        return 1
    print("OK — every snapshotted surface matches assets/; /legacy/ and the new IA "
          "read the same data.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
