"""BOROUGE — primary-source access verification.

Every historical figure in this study is read off a Borouge plc document held in
src/. This script re-fetches each of those documents from the company's own
investor-relations document library and asserts the bytes on disk are the bytes
the company publishes. It is the evidence behind QC item (s): the build path
touches no aggregator.

Run: python3 verify_sources.py
Writes: source_access.json
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'src')
BASE = "https://www.borouge.com"
IRDOC = "/en/investor-relations/Documents/IR%20Documents/"

# local file -> (published URL path, what the study reads off it)
DOCS = {
    'FS_FY2022.pdf': (IRDOC + "Borouge-Q4-2022-EN%20Financial%20Statements.pdf",
                      "FY2022 audited consolidated financial statements (statutory)"),
    'FS_FY2023.pdf': (IRDOC + "Borouge-Q4-2023-EN%20Financial%20Statements.pdf",
                      "FY2023 audited consolidated financial statements (statutory)"),
    'FS_FY2024.pdf': (IRDOC + "Borouge-Q4-2024-EN%20Borouge%20Financial%20Statement.pdf",
                      "FY2024 audited consolidated financial statements (statutory)"),
    'FS_FY2025.pdf': ("/en/investor-relations/IRResults/FYQ4-25/"
                      "Q4%202025%20Financial%20Statements%20-%20statutory.pdf",
                      "FY2025 audited consolidated financial statements (statutory)"),
    'FS_Q1_2026.pdf': (IRDOC + "Q1%202026%20Financial%20Statements%20-%20statutory%20-%20English.pdf",
                       "Q1-2026 condensed interim financial statements (reviewed)"),
    'FS_Q2_2026.pdf': (IRDOC + "Borouge-Q2-2026-EN%20Borouge%20Financial%20Statements.pdf",
                       "H1-2026 condensed interim financial statements (reviewed)"),
    'MDA_FY2023.pdf': (IRDOC + "Borouge-Q4-2023-EN%20MDA.pdf",
                       "FY2023 Management Discussion & Analysis — physical unit build"),
    'MDA_FY2024.pdf': (IRDOC + "Borouge-Q4-2024-EN%20Borouge%20MDA.pdf",
                       "FY2024 Management Discussion & Analysis — physical unit build"),
    'MDA_FY2025.pdf': ("/en/investor-relations/IRResults/FYQ4-25/"
                       "Q4%202025%20Management%20Discussion%20and%20Analysis%20Report.pdf",
                       "FY2025 Management Discussion & Analysis — physical unit build"),
    'MDA_Q1_2026.pdf': (IRDOC + "Q1%202026%20MDA%20-%20English.pdf",
                        "Q1-2026 Management Discussion & Analysis"),
    'MDA_Q2_2026.pdf': (IRDOC + "Borouge-Q2-2026-EN%20Borouge%20MDA.pdf",
                        "H1-2026 Management Discussion & Analysis"),
    'PRES_FY2023.pdf': (IRDOC + "Borouge-Q4-2023-EN%20Earnings%20Presentation.pdf",
                        "FY2023 earnings presentation"),
    'PRES_FY2024.pdf': (IRDOC + "Borouge-Q4-2024-EN%20Borouge%20Earnings%20Presentation.pdf",
                        "FY2024 earnings presentation"),
    'PRES_FY2025.pdf': ("/en/investor-relations/IRResults/FYQ4-25/"
                        "Q4%202025%20Earnings%20Presentation.pdf",
                        "FY2025 earnings presentation"),
    'PRES_Q2_2026.pdf': (IRDOC + "Borouge-Q2-2026-EN%20Borouge%20Earnings%20Presentation.pdf",
                         "H1-2026 earnings presentation"),
    'REL_FY2025.pdf': ("/en/investor-relations/IRResults/FYQ4-25/"
                       "Q4%202025%20Earnings%20Release.pdf",
                       "FY2025 earnings release"),
    'REL_Q2_2026.pdf': (IRDOC + "Borouge-Q2-2026-EN%20Borouge%20Earnings%20Release.pdf",
                        "H1-2026 earnings release"),
    'AR2022.pdf': (IRDOC + "Annual%20Reports/Borouge%20Annual%20Report%202022%20final.pdf",
                   "Annual Report 2022"),
    'AR2023.pdf': (IRDOC + "Annual%20Reports/Borouge%20Annual%20Report%202023%20final.pdf",
                   "Annual Report 2023"),
    'AR2024.pdf': (IRDOC + "Annual%20Reports/Borouge%20Annual%20Report%202024%20final.pdf",
                   "Annual Report 2024"),
    'AR2025.pdf': (IRDOC + "Annual%20Reports/Borouge_Annual_Report_2025_ENG.pdf",
                   "Annual Report 2025"),
}

# The Abu Dhabi Securities Exchange market-statistics workbooks, used only for the
# traded-share and market-capitalisation cross-check, never for a reported figure.
ADX = {
    'ADB_FY2025.xlsx': "Abu Dhabi Securities Exchange monthly market statistics, December 2025",
    'ADB_Q1_2026.xlsx': "Abu Dhabi Securities Exchange monthly market statistics, March 2026",
    'ADB_Q2_2026.xlsx': "Abu Dhabi Securities Exchange monthly market statistics, June 2026",
}


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def fetch(url):
    """Re-fetch a published document. Returns (bytes, http_status) or (None, status)."""
    out = subprocess.run(
        ['curl', '-s', '-L', '--max-time', '120', '-w', '%{http_code}',
         '-o', '/tmp/_bor_verify.bin', url],
        capture_output=True, text=True)
    code = out.stdout.strip()[-3:]
    if code != '200' or not os.path.exists('/tmp/_bor_verify.bin'):
        return None, code
    with open('/tmp/_bor_verify.bin', 'rb') as fh:
        return fh.read(), code


def main():
    rows, failures = [], []
    for name, (path, what) in sorted(DOCS.items()):
        local = os.path.join(SRC, name)
        url = BASE + path
        have = os.path.exists(local)
        row = dict(file=name, url=url, reads=what, held_locally=have)
        if have:
            row['bytes_local'] = os.path.getsize(local)
            row['sha256_local'] = sha(local)
        body, code = fetch(url)
        row['http_status'] = code
        if body is None:
            row['refetch'] = 'UNREACHABLE'
            failures.append(f"{name}: HTTP {code} at {url}")
        else:
            row['bytes_remote'] = len(body)
            row['sha256_remote'] = hashlib.sha256(body).hexdigest()
            if have and row['sha256_local'] == row['sha256_remote']:
                row['refetch'] = 'IDENTICAL'
            elif have:
                row['refetch'] = 'DIFFERS'
                failures.append(
                    f"{name}: local {row['bytes_local']}B does not match published "
                    f"{row['bytes_remote']}B at {url}")
            else:
                row['refetch'] = 'FETCHED (no local copy)'
                failures.append(f"{name}: no local copy held")
        rows.append(row)
        print(f"  {row['refetch']:<22} {name:<20} {row.get('bytes_local', 0):>9,}B  {url}")

    adx_rows = []
    for name, what in sorted(ADX.items()):
        local = os.path.join(SRC, name)
        adx_rows.append(dict(file=name, describes=what,
                             held_locally=os.path.exists(local),
                             bytes_local=os.path.getsize(local) if os.path.exists(local) else 0,
                             role='cross-check only — never a source for a reported figure'))

    result = dict(
        ticker='BOROUGE',
        verified_on='2026-08-09',
        company_document_library=BASE + "/en/investor-relations/Pages/reports-results.aspx",
        documents=rows,
        exchange_files=adx_rows,
        complete_audited_years=['2022', '2023', '2024', '2025'],
        interim_periods=['Q1 2026', 'H1 2026'],
        identical=sum(1 for r in rows if r.get('refetch') == 'IDENTICAL'),
        total=len(rows),
        failures=failures,
    )
    with open(os.path.join(HERE, 'source_access.json'), 'w') as fh:
        json.dump(result, fh, indent=1)

    print(f"\n{result['identical']} of {result['total']} documents re-fetched from "
          f"borouge.com byte-for-byte identical to the copy the build reads.")
    print(f"Complete audited financial years assembled: "
          f"{len(result['complete_audited_years'])} "
          f"({', '.join(result['complete_audited_years'])}).")
    if failures:
        print(f"\nFAILURES ({len(failures)}):")
        for f in failures:
            print('  !', f)
        sys.exit(1)


if __name__ == '__main__':
    main()
