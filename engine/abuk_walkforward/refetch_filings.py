"""Rebuild this run's `filings/` directory from the fetch log.

WHY THIS EXISTS AND WHAT HAPPENED. The 40 source PDFs this run parsed totalled
145 MB. `engine/*_walkforward/filings/` is gitignored, so they were never
committed; the container's root filesystem then filled to 100% and they were
deleted to free it. That is recorded here rather than left for a later reader
to discover as an absence.

THE DELETION IS PROVABLY LOSSLESS. `fetch_attempts.json` records, for every
file, the exact URL it came from, its byte count and the first sixteen hex
digits of its SHA-256. This script re-fetches each one and verifies both. A file
that does not come back identical is reported, not silently accepted.

Run it before re-reading any figure sourced to a filing.
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch_sources as fs


def main(only=None):
    log = json.load(open(os.path.join(HERE, "fetch_attempts.json")))
    want = [e for e in log if e.get("result") == "OK"]
    if only:
        want = [e for e in want if e["name"] in only]
    ok = bad = skipped = 0
    for e in want:
        dest = os.path.join(HERE, "filings", e["name"])
        if os.path.exists(dest) and os.path.getsize(dest) == e["bytes"]:
            skipped += 1
            continue
        p = fs.fetch(e["url"], e["name"], e.get("note", ""))
        if not p:
            bad += 1
            print("  FAILED TO REFETCH  %s" % e["name"])
            continue
        blob = open(p, "rb").read()
        h = hashlib.sha256(blob).hexdigest()[:16]
        if len(blob) != e["bytes"] or h != e["sha256"]:
            bad += 1
            print("  MISMATCH %s: %d bytes / %s against a recorded %d / %s"
                  % (e["name"], len(blob), h, e["bytes"], e["sha256"]))
        else:
            ok += 1
    print("refetched %d, already present %d, failed or mismatched %d, of %d "
          "recorded files" % (ok, skipped, bad, len(want)))
    return bad == 0


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1:] or None) else 1)
