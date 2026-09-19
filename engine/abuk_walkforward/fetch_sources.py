"""ABUK fundamental walk-forward — source fetcher.

Every attempt is logged, success or failure, into fetch_attempts.json
(§1 of engine/Fundamental_Walkforward_Prompt.md: "Log every source attempt,
including failures, in the Sweep Register").

The container's egress proxy truncates a single response at 1 MiB, so files are
pulled with byte-range requests and re-assembled.  The assembled length is
checked against the server's Content-Length before the file is accepted.
"""
import json, os, subprocess, sys, hashlib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
FILINGS = os.path.join(HERE, "filings")
LOG = os.path.join(HERE, "fetch_attempts.json")
CHUNK = 1 << 20


def _curl(args, timeout=300):
    p = subprocess.run(["curl", "-sS", "-L", "--max-time", str(timeout)] + args,
                       capture_output=True)
    return p.returncode, p.stdout, p.stderr.decode("utf8", "replace")


def head(url):
    rc, out, err = _curl(["-I", "-o", "/dev/null",
                          "-w", "%{http_code} %{size_download} %{content_type}", url])
    return out.decode("utf8", "replace").strip(), err


def fetch(url, name, note=""):
    os.makedirs(FILINGS, exist_ok=True)
    dest = os.path.join(FILINGS, name)
    entry = {"url": url, "name": name, "note": note,
             "attempted": datetime.date.today().isoformat()}
    # length first
    rc, out, err = _curl(["-r", "0-0", "-D", "-", "-o", "/dev/null", url])
    total = None
    for line in out.decode("utf8", "replace").splitlines():
        if line.lower().startswith("content-range:"):
            try:
                total = int(line.split("/")[-1].strip())
            except ValueError:
                total = None
    if total is None:
        rc, out, err = _curl(["-I", "-o", "/dev/null", "-w", "%{size_download}", url])
        entry.update(result="FAIL", reason="no content-range; server would not report length",
                     stderr=err[:400])
        _log(entry)
        return None
    buf = bytearray()
    off = 0
    while off < total:
        end = min(off + CHUNK - 1, total - 1)
        rc, out, err = _curl(["-H", f"Range: bytes={off}-{end}", "--output", "-", url])
        if rc != 0 or not out:
            entry.update(result="FAIL", reason=f"range {off}-{end} failed rc={rc}",
                         stderr=err[:400])
            _log(entry)
            return None
        buf += out
        off += len(out)
    if len(buf) != total:
        entry.update(result="FAIL", reason=f"assembled {len(buf)} of {total} bytes")
        _log(entry)
        return None
    with open(dest, "wb") as fh:
        fh.write(buf)
    entry.update(result="OK", bytes=total,
                 sha256=hashlib.sha256(buf).hexdigest()[:16],
                 magic=buf[:5].decode("latin1"))
    _log(entry)
    return dest


def _log(entry):
    data = []
    if os.path.exists(LOG):
        data = json.load(open(LOG))
    data = [d for d in data if not (d.get("url") == entry["url"]
                                    and d.get("name") == entry["name"])]
    data.append(entry)
    json.dump(data, open(LOG, "w"), indent=1, sort_keys=True)
    print(f"  {entry['result']:5s} {entry['name']:34s} "
          f"{entry.get('bytes', entry.get('reason',''))}")


if __name__ == "__main__":
    for spec in json.load(open(sys.argv[1])):
        fetch(spec["url"], spec["name"], spec.get("note", ""))
