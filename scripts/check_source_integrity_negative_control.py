#!/usr/bin/env python3
"""Negative control for [R-ENF-01]'s SIGCM clause-1 gate.

A CHECK NOBODY HAS SEEN FAIL IS NOT EVIDENCE. The clean cases carry as much weight as the
breaches here, because three earlier drafts of this instrument fired on 156 and then 83
items across sixteen studies — forecast ratios, commodity benchmarks quoted inside a
company's own MD&A, and balance-sheet lines whose source names the line rather than the
document — and every one of those was work that was right. Per [R-COC-01] each was fixed by
re-pointing the check, never by widening it.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
import source_integrity as SI                                          # noqa: E402

CASES = [
    ('1  a dated historical relayed through a trade outlet, exactly as it shipped',
     'rev_fy25', 'EGX filing reported by Global Cement, cemnet/International Cement Review, '
                 'Daily News Egypt and Arab Finance', True),
    ('2  a dated historical carried by an aggregator, exactly as it shipped',
     'eq_fy25', 'FY2025 balance-sheet data from S&P Global Market Intelligence as carried '
                'by two independent aggregators', True),
    ('3  a dated historical sourced to an aggregator and no document',
     'rev_fy24', 'MarketScreener/Mubasher FY2024 consolidated results', True),
    ('4  a dated historical from the audited statements — must NOT fire',
     'rev_fy25', "Audited statement of profit or loss for the year ended 31 December 2025, "
                 'sales (net) EGP 9,089,149,688', False),
    ('5  a vendor named BESIDE the company\'s own release — must NOT fire',
     'rev_h1_26', 'H1-2026 revenue backlog; Modon H1-2026 results announcement, as also '
                  'reported by Reuters', False),
    ('6  a commodity benchmark inside the company\'s own MD&A — must NOT fire',
     'bm_urea_eg_fy24', 'Fertiglobe Q4 2025 Results MD&A Report — urea Egypt FOB '
                        '(source: CRU, MMSA, ICIS)', False),
    ('7  a FORWARD RATIO is not a historical, whatever its source — must NOT fire',
     'dna_pct', 'D&A as a share of revenue, per MarketScreener', False),
    ('8  a balance-sheet line whose source names the line rather than a document',
     'inv_fy23', 'Inventories, 31 Dec 2023 (net of write-downs)', False),
    ('9  a peer figure is not the subject\'s own historical — must NOT fire',
     'peer_mbsc_rev', 'Misr Beni Suef FY2025 net sales, per Argaam', False),
    ('10 a reviewed interim from the company\'s own filing — must NOT fire',
     'cash_mar26', 'Reviewed interim statement of financial position as at 31 March 2026, '
                   'cash on hand and at banks', False),
]


def sandbox():
    d = tempfile.mkdtemp(prefix='si-nc-')
    dst = os.path.join(d, 'repo')
    os.makedirs(dst)
    for item in ('scripts', 'engine'):
        shutil.copytree(os.path.join(ROOT, item), os.path.join(dst, item),
                        ignore=shutil.ignore_patterns('*.pdf', '*.png', '*.xlsx', '*.docx',
                                                      '__pycache__', 'raw_ohlc',
                                                      'raw_indices', 'lab', 'panels'))
    return d, dst


def run(cwd):
    p = subprocess.run([sys.executable, 'scripts/check_source_integrity.py'],
                       cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def gate_cases():
    out = []
    # 11 — a NEW study in breach must FAIL and be named
    d, dst = sandbox()
    try:
        p = os.path.join(dst, 'engine', 'du_study', 'study_numbers.json')
        j = json.load(open(p))
        assert isinstance(j.get('inputs'), dict), 'fixture never injected: no register'
        j['inputs']['rev_fy24'] = {'value': 1.0, 'source': 'Bloomberg terminal, as reported '
                                                           'by MarketScreener',
                                   'date': '2026-01-01', 'ring': 'Company'}
        json.dump(j, open(p, 'w'))
        assert 'Bloomberg' in json.load(open(p))['inputs']['rev_fy24']['source']
        rc, txt = run(dst)
        out.append(('11 a new study in breach must FAIL and be named',
                    rc != 0 and 'DU' in txt))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    # 12 — a study whose register vanishes must FAIL as newly unreadable
    d, dst = sandbox()
    try:
        p = os.path.join(dst, 'engine', 'du_study', 'study_numbers.json')
        j = json.load(open(p))
        j['inputs'] = {}
        json.dump(j, open(p, 'w'))
        assert json.load(open(p))['inputs'] == {}
        rc, txt = run(dst)
        out.append(('12 a register that vanishes must FAIL as newly unreadable',
                    rc != 0 and 'DU' in txt))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    # 13 — a register with inputs but no dated historical is unreadable, not clean
    d, dst = sandbox()
    try:
        p = os.path.join(dst, 'engine', 'du_study', 'study_numbers.json')
        j = json.load(open(p))
        j['inputs'] = {'some_rate': {'value': 1.0, 'source': 'x', 'date': 'y', 'ring': 'z'}}
        json.dump(j, open(p, 'w'))
        assert len(json.load(open(p))['inputs']) == 1
        rc, txt = run(dst)
        out.append(('13 five inputs and no historical is unreadable, not clean',
                    rc != 0 and 'DU' in txt))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    # 14 — the repository as it stands must stay GREEN
    d, dst = sandbox()
    try:
        rc, txt = run(dst)
        out.append(('14 the repository as it stands must stay GREEN', rc == 0))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return out


def main():
    fails = []
    for name, key, src, must in CASES:
        got = bool(SI.violation(key, src))
        ok = (got == must)
        print('  %-4s %s' % ('ok' if ok else 'FAIL', name))
        if not ok:
            fails.append(name)
    for name, ok in gate_cases():
        print('  %-4s %s' % ('ok' if ok else 'FAIL', name))
        if not ok:
            fails.append(name)
    total = len(CASES) + 4
    print('\n%d/%d conditions behaved as required' % (total - len(fails), total))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
