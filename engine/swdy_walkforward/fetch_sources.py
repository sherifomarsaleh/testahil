"""Fetch SWDY's own filings from the company's own investor-relations archive.

SIGCM clause 1: historicals come from the company's own audited statements and its
own IR documents. This script logs EVERY attempt, success or failure, into
fetch_attempts.json — a refusal is a recorded fact of this run's history, not an
absence [R-ENF-04].

Route: ir.elsewedyelectric.com is a JavaScript-rendered results centre whose PDF
list is served by a POST endpoint (api/filter_results_center_sections) guarded by a
per-session CSRF token. The token is read out of the rendered page in the same
session, so the archive is reached without a headless browser.
"""
import json, os, re, html, urllib.parse, subprocess, datetime, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILINGS = os.path.join(HERE, 'filings')
IR = 'https://ir.elsewedyelectric.com'
RC = IR + '/en/results-center'
API = IR + '/api/filter_results_center_sections'
PAGE_ID = '9740'
YEARS = list(range(2007, 2027))

attempts = []


def log(url, outcome, detail='', tier=None, kind=None):
    attempts.append(dict(url=url, outcome=outcome, detail=detail, tier=tier,
                         kind=kind, at=datetime.datetime.utcnow().isoformat(timespec='seconds')))


def curl(args, out=None):
    cmd = ['curl', '-sS', '-L', '--max-time', '180'] + args
    if out:
        cmd += ['-o', out]
    cmd += ['-w', '%{http_code}']
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, (r.stdout or '').strip()[-3:], r.stderr


def discover():
    """Return [(year, quarter, title, url)] from the IR results centre."""
    cj = os.path.join(HERE, '.cookies')
    rc = os.path.join(HERE, '.rc.html')
    rc_, code, err = curl(['-c', cj, RC], rc)
    if code != '200':
        log(RC, 'FAIL', f'http {code} {err[:200]}')
        raise SystemExit('results centre unreachable — STOP AND INFORM')
    log(RC, 'OK', 'results centre rendered; CSRF token and year list read')
    s = open(rc, encoding='utf-8', errors='replace').read()
    tok = re.search(r"_token: '([^']+)'", s).group(1)
    found = []
    for y in YEARS:
        dst = os.path.join(HERE, '.api_%d.json' % y)
        _, code, err = curl(['-b', cj, '-X', 'POST', API,
                             '-H', 'X-Requested-With: XMLHttpRequest',
                             '--data', f'page_id={PAGE_ID}&year={y}&language=en&_token={tok}'], dst)
        if code != '200':
            log(f'{API}?year={y}', 'FAIL', f'http {code}')
            continue
        log(f'{API}?year={y}', 'OK', 'section payload returned')
        d = json.load(open(dst))
        for sec in d.get('sectionsData', []):
            q = sec.get('quarter')
            h = html.unescape(sec['section_html'])
            # each card is an <a href=..> with a <h*> or alt title nearby
            for m in re.finditer(r'href="(https?://[^"]+?\.pdf)"', h):
                url = m.group(1)
                # A LITERAL SPACE IN AN href IS A REAL URL AND curl REFUSES IT (http 000).
                # The FY2018 consolidated annual statement is published at
                # ".../Elsewedy Electric FY-2018 Cons.ENG.pdf" and the first pass recorded a
                # bare failure against it, which reads exactly like the document not being
                # there. It is there. Re-run the probe before believing the absence
                # [R-ENF-04]; only the path is quoted, never the scheme or host.
                if ' ' in url:
                    sch, _, rest = url.partition('://')
                    host, _, path = rest.partition('/')
                    url = sch + '://' + host + '/' + urllib.parse.quote(path)
                title = urllib.parse.unquote(os.path.basename(url))
                found.append((y, q, title, url))
    # de-duplicate, preserve order
    seen, out = set(), []
    for r in found:
        if r[3] in seen:
            continue
        seen.add(r[3])
        out.append(r)
    return out


# What this run needs: the CONSOLIDATED annual statements (the audited historicals),
# the consolidated interims for the current year, the earnings releases (segment and
# KPI anchors no statement carries) and the segment-analysis sheets.
# THE MATCHER IS BUILT FROM WHAT THE ARCHIVE ACTUALLY CONTAINS, NOT FROM WHAT IT OUGHT
# TO CONTAIN [L-355]. A first draft of this list wanted `consolidat` and silently dropped
# SIX annual consolidated filings — FY2016 ("FY-2016-FS.Eng"), FY2018 ("FY-2018 Cons.ENG"),
# FY2020 and FY2021 ("EE-Cons.-English-FY-20xx") among them — and reported a clean run of
# 215 documents while doing it. Nineteen years of filings and no error anywhere: an absent
# answer in a clean answer's clothes [R-ENF-04]. Every spelling below was read off the
# archive's own filenames after listing what the first pass had thrown away.
WANT = re.compile(r'(consolidat|consolidation|consalidat|consolildat|cosolidat|'
                  r'\bcons\b|\bcons[._-]|year-end|earnings-release|earnings|'
                  r'\bER-|\bfs\b|\bfs[._-]|\bcfs|financial|segment|presentation|rap-)', re.I)
# "Seperate" is the archive's own misspelling and must be skipped exactly as "separate" is;
# a skip list built from correct spellings would have admitted a standalone filing as a
# consolidated one, which is worse than dropping it.
SKIP = re.compile(r'(standalone|stanalone|separate|seperate|unconsolidated|غير|القوائم)', re.I)


def classify(title):
    t = title.lower()
    if SKIP.search(t):
        return None
    if re.search(r'segment', t):
        return 'segment_analysis'
    if re.search(r'earnings-presentation|presentation', t):
        return 'ir_presentation'
    if re.search(r'earnings-release|\ber-|press-release|reports.*results|rap-|earnings', t):
        return 'earnings_release'
    if WANT.search(t):
        return 'financial_statements'
    return None


def main():
    items = discover()
    print(f'discovered {len(items)} pdf links across {len(YEARS)} years')
    got = []
    for y, q, title, url in items:
        kind = classify(title)
        if kind is None:
            log(url, 'SKIPPED', 'standalone/separate or non-financial document', kind=None)
            continue
        safe = re.sub(r'[^A-Za-z0-9._-]', '_', f'{y}Q{q}__{title}')
        dst = os.path.join(FILINGS, safe)
        if os.path.exists(dst) and os.path.getsize(dst) > 20000:
            log(url, 'CACHED', dst, tier='A', kind=kind)
            got.append((y, q, kind, safe, url))
            continue
        _, code, err = curl([url], dst)
        if code != '200' or not os.path.exists(dst) or os.path.getsize(dst) < 5000:
            log(url, 'FAIL', f'http {code}; {os.path.getsize(dst) if os.path.exists(dst) else 0} bytes',
                kind=kind)
            if os.path.exists(dst):
                os.remove(dst)
            continue
        log(url, 'OK', f'{os.path.getsize(dst)} bytes', tier='A', kind=kind)
        got.append((y, q, kind, safe, url))
    manifest = [dict(fiscal_year=y, quarter=q, kind=k, file=f, url=u,
                     tier='A', tier_reason="the company's own investor-relations archive")
                for y, q, k, f, u in got]
    json.dump(manifest, open(os.path.join(HERE, 'source_manifest.json'), 'w'), indent=1)
    json.dump(attempts, open(os.path.join(HERE, 'fetch_attempts.json'), 'w'), indent=1)
    print(f'downloaded/cached {len(got)}; attempts logged {len(attempts)}')


if __name__ == '__main__':
    main()
