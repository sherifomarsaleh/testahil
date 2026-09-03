#!/usr/bin/env python3
"""Day 0: re-fetch every primary document the walk-forwards registered and verify its sha256.

The registers carry url + sha256 for the documents each run read; the documents themselves
were read from session scratch and are not on disk. This re-fetches each one, hashes it,
compares, and keeps ONLY the statements a study currently stands on (the base-year and the
latest interim) under engine/<x>_walkforward/filings/ — the rest are proven re-fetchable by
url+sha and discarded, because committing hundreds of megabytes of scans would bloat the
repository and the session's disk allowance. Every outcome is written to refetch_log.json.
A failed fetch or a hash mismatch is a STOP-AND-ASK item for MORNING.md, never silently skipped.
"""
import hashlib, json, os, sys, time, urllib.request, ssl
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REGS = {
  'PHDC': 'engine/phdc_walkforward/ir_register.json',
  'TMGH': 'engine/tmgh_walkforward/ir_register.json',
  'AMOC': 'engine/amoc_walkforward/ir_register.json',
  'EGCH': 'engine/egch_walkforward/ir_register.json',
}
KEEP_KINDS = ('financial_statement', 'audited annual statements', 'reviewed interim', 'consolidated')
def walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values(): yield from walk(v)
    elif isinstance(o, list):
        for v in o: yield from walk(v)
ctx = ssl.create_default_context()
log = {'started': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'results': [], 'summary': {}}
for tk, rel in REGS.items():
    d = json.load(open(os.path.join(ROOT, rel)))
    recs = [r for r in walk(d) if isinstance(r, dict) and r.get('sha256') and r.get('url')]
    keep_dir = os.path.join(ROOT, os.path.dirname(rel), 'filings'); os.makedirs(keep_dir, exist_ok=True)
    ok = mism = fail = kept = 0
    for r in recs:
        url = r['url']; want = r['sha256'].lower()
        name = r.get('name') or r.get('file') or url.rsplit('/', 1)[-1]
        h = hashlib.sha256(); size = 0; status = 'ok'; err = ''
        tmp = os.path.join(keep_dir, '.partial')
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=120, context=ctx) as resp, open(tmp, 'wb') as f:
                while True:
                    chunk = resp.read(1 << 16)
                    if not chunk: break
                    h.update(chunk); f.write(chunk); size += len(chunk)
            got = h.hexdigest()
            if got != want: status = 'HASH MISMATCH'; mism += 1
            else: ok += 1
        except Exception as e:
            status = 'FETCH FAILED'; err = '%s: %s' % (type(e).__name__, str(e)[:120]); fail += 1
        keep = status == 'ok' and any(k in (str(r.get('kind', '')) + ' ' + str(r.get('label', ''))).lower() for k in ('financial_statement', 'audited', 'reviewed', 'interim', 'consolidated'))
        if keep and os.path.exists(tmp):
            dest = os.path.join(keep_dir, name.replace('/', '_'))
            os.replace(tmp, dest); kept += 1
        elif os.path.exists(tmp):
            os.remove(tmp)
        log['results'].append({'ticker': tk, 'name': name, 'url': url, 'sha256_expected': want,
                               'status': status, 'bytes': size, 'kept': bool(keep), 'error': err})
        print('%-5s %-14s %9d  %s' % (tk, status, size, name[:70]), flush=True)
    log['summary'][tk] = {'records': len(recs), 'ok': ok, 'hash_mismatch': mism, 'fetch_failed': fail, 'kept_on_disk': kept}
    json.dump(log, open(os.path.join(ROOT, 'engine/method_reassessment/refetch_log.json'), 'w'), indent=1)
log['finished'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
json.dump(log, open(os.path.join(ROOT, 'engine/method_reassessment/refetch_log.json'), 'w'), indent=1)
print('SUMMARY', json.dumps(log['summary']))
