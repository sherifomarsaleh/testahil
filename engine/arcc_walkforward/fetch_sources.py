"""Fetch ARCC's own filings from arabiancementcompany.com and log every attempt.

SIGCM clause 1 and [R-FCAL-01] §1: the most recent three fiscal years and every
disclosed current-year quarter come from the COMPANY'S OWN audited statements or
its own IR documents.  ARCC publishes its whole archive on its own site, so every
number in this panel is tier A -- there is no aggregator anywhere in the chain.

EVERY ATTEMPT IS LOGGED WITH ITS OUTCOME [R-CAMP-01, L-007], successes and
failures alike, and each file is recorded with its sha256 so a later session can
tell a re-download from a re-read.
"""
import concurrent.futures as cf
import hashlib
import json
import os
import subprocess
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, 'filings')
BASE = 'https://arabiancementcompany.com/wp-content/uploads'

# (local name, url path, what it is, tier)
DOCS_WANTED = [
    # --- fiscal-year consolidated financials, the panel's spine -------------
    ('FY2015_cons', '2025/06/ACC-2015-Consolidated-Financials-English.pdf', 'FY2015 consolidated FS (carries FY2014 comparative)', 'A'),
    ('FY2016_cons', '2025/06/FY-2016-Consolidated-Financials-English.pdf', 'FY2016 consolidated FS', 'A'),
    ('FY2017_cons', '2025/06/FY-2017-Consolidated-Financials-English.pdf', 'FY2017 consolidated FS', 'A'),
    ('FY2018_cons', '2025/06/ARCC_FY_2018_Consolidated_Financials-English.pdf', 'FY2018 consolidated FS', 'A'),
    ('FY2019_cons', '2025/06/FY_2019_Consolidated_Financials-English.pdf', 'FY2019 consolidated FS', 'A'),
    ('FY2020_cons', '2025/06/FY-2020-consolidated-financials-english.pdf', 'FY2020 consolidated FS', 'A'),
    ('FY2021_cons', '2025/06/FY_2021_Consolidated_Financials-English.pdf', 'FY2021 consolidated FS', 'A'),
    ('FY2022_cons', '2025/06/FY_2022_Consolidated_Financials-English.pdf', 'FY2022 consolidated FS', 'A'),
    ('FY2023_cons', '2025/06/4Q2023_ACC_Consolidated_Financials.pdf', 'FY2023 consolidated FS', 'A'),
    ('FY2024_cons', '2025/06/FY2024_Consolidated_Financials-English.pdf', 'FY2024 consolidated FS', 'A'),
    ('FY2025_cons', '2026/02/FY-2025-Consolidated-Financials-English.pdf', 'FY2025 consolidated FS', 'A'),
    # --- the current study year: EVERY disclosed quarter, before the build --
    ('Q1_2026_cons', '2026/06/Q1-2026-Consolidated-Financials-English.pdf', 'Q1-2026 consolidated FS', 'A'),
    ('Q2_2026_cons', '2026/08/2Q2026-Consolidated-Financials-English.pdf', 'Q2-2026 consolidated FS', 'A'),
    # --- results releases and IR decks: the operating anchors no FS carries --
    ('IR_FY2025', '2026/02/FY-2025-Investor-Presentation.pdf', 'FY2025 investor presentation', 'A'),
    ('IR_Q1_2026', '2026/06/Q1-2026-Investor-Presentation.pdf', 'Q1-2026 investor presentation', 'A'),
    ('ER_FY2024', '2025/06/ACC_FY2024_Earnings_Release.pdf', 'FY2024 earnings release', 'A'),
    ('IR_FY2024', '2025/06/FY2024_ACC_Investor_Presentation.pdf', 'FY2024 investor presentation', 'A'),
    ('IR_FY2022', '2025/06/ACC_FY_2022_Investor_presentation.pdf', 'FY2022 investor presentation', 'A'),
    ('IR_FY2021', '2025/06/ACC_FY_2021_Investor_presentation.pdf', 'FY2021 investor presentation', 'A'),
    ('IR_FY2020', '2025/06/ACC_FY_20_INVESTOR_PRESENTATION.pdf', 'FY2020 investor presentation', 'A'),
    ('IR_FY2019', '2025/06/ACC_FY2019_Investor_Presentation.pdf', 'FY2019 investor presentation', 'A'),
    ('IR_FY2018', '2025/06/ACC_FY18_Investor_presentation.pdf', 'FY2018 investor presentation', 'A'),
    ('IR_FY2017', '2025/06/ACC-FY-2017-Investors-presentation.pdf', 'FY2017 investor presentation', 'A'),
    ('IR_FY2016', '2025/06/ACC-FY-2016-Investors-presentation.pdf', 'FY2016 investor presentation', 'A'),
    ('IR_FY2015', '2025/06/ACC-FY-2015-Investors-presentation.pdf', 'FY2015 investor presentation', 'A'),
    ('ER_FY2021', '2025/06/FY_2021_Earnings_Release.pdf', 'FY2021 earnings release', 'A'),
    ('ER_FY2022', '2025/06/FY_2022_Earnings_Release.pdf', 'FY2022 earnings release', 'A'),
    ('ER_FY2023', '2025/06/ACC_4Q_2023_Earnings_Release.pdf', 'FY2023 earnings release', 'A'),
    ('ER_FY2020', '2025/06/4Q_2020_Earnings_Release.pdf', 'FY2020 earnings release', 'A'),
    ('ER_FY2019', '2025/06/4Q_2019_EARNINGS_RELEASEPDF.pdf', 'FY2019 earnings release', 'A'),
    ('ER_FY2018', '2025/06/4Q_2018_Earnings_Release.pdf', 'FY2018 earnings release', 'A'),
    ('ER_FY2017', '2025/06/4Q-2017-Earnings-Release.pdf', 'FY2017 earnings release', 'A'),
    ('ER_FY2016', '2025/06/FY-2016-Earnings-Release.pdf', 'FY2016 earnings release', 'A'),
    ('ER_FY2015', '2025/06/FY-2015-Earnings-Release.pdf', 'FY2015 earnings release', 'A'),
]


def get(item):
    name, path, what, tier = item
    url = '%s/%s' % (BASE, path)
    dest = os.path.join(DOCS, name + '.pdf')
    t0 = time.time()
    r = subprocess.run(['curl', '-s', '-L', '--max-time', '120', '-w', '%{http_code}',
                        '-o', dest, url], capture_output=True, text=True)
    code = r.stdout.strip()
    ok = code == '200' and os.path.exists(dest) and os.path.getsize(dest) > 20000
    rec = {'name': name, 'url': url, 'what': what, 'tier': tier,
           'ts': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
           'status': code, 'ok': ok, 'secs': round(time.time() - t0, 2)}
    if ok:
        rec['bytes'] = os.path.getsize(dest)
        rec['sha256'] = hashlib.sha256(open(dest, 'rb').read()).hexdigest()
        rec['outcome'] = 'HTTP %s, %d bytes downloaded' % (code, rec['bytes'])
    else:
        rec['outcome'] = 'HTTP %s — not retrieved' % code
        if os.path.exists(dest):
            os.remove(dest)
    return rec


def main():
    os.makedirs(DOCS, exist_ok=True)
    out = []
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        for rec in ex.map(get, DOCS_WANTED):
            out.append(rec)
            print('%-4s %-14s %s' % (rec['status'], rec['name'], rec['what']))
    out.sort(key=lambda x: x['name'])
    json.dump(out, open(os.path.join(HERE, 'fetch_attempts.json'), 'w'), indent=1)
    got = sum(1 for x in out if x['ok'])
    print('\n%d of %d retrieved from the company\'s own site' % (got, len(out)))
    return 0 if got == len(out) else 1


if __name__ == '__main__':
    raise SystemExit(main())
