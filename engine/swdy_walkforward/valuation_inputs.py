"""The VALUATION-INPUT BLOCK, per origin [R-FCAL-01 AMENDED 03-Sep-2026].

A driver panel is not a record a value can be rebuilt from, and the difference stays
invisible until something tries. This commits, per origin and under the same
point-in-time discipline as every other figure in this run:

    cash and equivalents · interest-bearing debt · property, plant and equipment ·
    depreciation and amortisation · the working-capital lines · the share count with
    the par value it was footed against · capital expenditure

Capex is committed where the cash-flow statement discloses it and otherwise DERIVED by
`capex = dPP&E + D&A` and LABELLED as derived, because an identity is not an assumption
and the label is what keeps the two apart.

A MISSING ITEM IS RECORDED AS MISSING, named with its reason, never omitted — a block
quietly carrying six of seven reads as complete.

THE SHARE COUNT IS FOOTED OR IT IS NOT RECORDED, and on this name that is not a
formality. SWDY's capital note is a CHRONOLOGY of resolutions rather than one current
sentence, and the count moved four times inside this window while the PAR VALUE ITSELF
CHANGED from EGP 10 to EGP 1 in 2018. Today's 2,140,777,876 shares carried back to
FY2016 would be wrong by a factor of 9.6 - plausible on the page, invisible in the
pooled error afterwards, and fatal to any per-share figure rebuilt at that origin.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from parse_fs import numbers, big, load
import parse_er as E

OUT = os.path.join(HERE, 'valuation_inputs.json')
PANEL = os.path.join(HERE, 'panel.json')

# ---------------------------------------------------------------------------
# THE SHARE COUNT, read out of the capital note's own recital.
#
# Note 29 of the FY2025 audited statements recites every resolution that changed the
# capital, with its date and the count it produced. The recital STOPS at the last
# resolution that changed the capital, so it establishes the par value and the identity
# and each year's count is that year's own committed capital divided by that year's par.
# ---------------------------------------------------------------------------
CAPITAL_RECITAL = [
    dict(effective='2017-01-01', capital_egp=2234180000, shares=223418000, par=10.0,
         event='issued and fully paid-up capital as of 1 January 2017'),
    dict(effective='2017-05-04', capital_egp=2184180000, shares=218418000, par=10.0,
         event='EGM of 4 May 2017 wrote off 5 million treasury shares'),
    dict(effective='2018-05-22', capital_egp=2184180000, shares=2184180000, par=1.0,
         event='EGM of 22 May 2018 split the par value to EGP 1 from EGP 10; annotated '
               'in the commercial register on 8 August 2018'),
    dict(effective='2022-10-17', capital_egp=2170777876, shares=2170777876, par=1.0,
         event='13,402,124 treasury shares purchased Jun-Sep 2020 retired; the '
               'commercial register was annotated on 17 October 2022'),
    dict(effective='2024-04-18', capital_egp=2140777876, shares=2140777876, par=1.0,
         event='30,000,000 treasury shares retired at a par value of EGP 30,000,000'),
]
RECITAL_SOURCE = ("Elsewedy Electric Company, audited consolidated financial statements "
                  "for the year ended 31 December 2025, note 29 (share capital)")


def shares_at(year_end):
    """The count in issue at 31 December of `year_end`, with its par and its footing."""
    d = '%d-12-31' % year_end
    cur = None
    for r in CAPITAL_RECITAL:
        if r['effective'] <= d:
            cur = r
    if cur is None:
        return dict(missing=True,
                    reason='the capital recital in note 29 begins at 1 January 2017 and '
                           'says nothing about the capital at this year end')
    foots = abs(cur['capital_egp'] / cur['par'] - cur['shares']) < 1
    return dict(shares=cur['shares'], par_value_egp=cur['par'],
                issued_capital_egp=cur['capital_egp'],
                footing='issued capital %d / par %.0f = %d, which is the count the same '
                        'note states' % (cur['capital_egp'], cur['par'], cur['shares']),
                foots=foots, established_by=cur['event'], effective=cur['effective'],
                source=RECITAL_SOURCE, tier='A_AUDITED', route='text_layer')


# ---------------------------------------------------------------------------
# Cash-flow capex, out of the audited statements where the filing is to hand.
# ---------------------------------------------------------------------------
AUDITED_CF = {
    2025: ('2025Q4__EE-Consolidated-En-FS-31-December-2025.filled.txt', 0),
    2024: ('2025Q4__EE-Consolidated-En-FS-31-December-2025.filled.txt', 1),
    2023: ('2024Q4__EE-Consalidated-English-FS-31-December-2024.filled.txt', 1),
    2021: ('2021Q4__EE-Cons.-English-FY-2021.txt', 0),
    2020: ('2021Q4__EE-Cons.-English-FY-2021.txt', 1),
    2019: ('2019Q4__Elsewedy-Electric-Consolidated-English-31-12-2019.txt', 0),
    2018: ('2018Q4__Elsewedy_Electric_FY-2018_Cons.ENG.txt', 0),
    2016: ('2016Q4__Elsewedy-Electric-FY-2016-FS.Eng.txt', 0),
}
CAPEX_PATS = [r'acquisition of (fixed assets|property)', r'Paid for.*acquisition of',
              r'purchase of (property|fixed assets)', r'Payments? for.*(property|fixed assets)']
DEP_PATS = [r'^\s*Depreciation of property', r'^\s*Depreciation and amortization',
            r'^\s*Depreciation\b']


def cf_line(fname, col, pats, minabs=1e6):
    txt = load(fname)
    if txt is None:
        return None
    for ln in txt.splitlines():
        if any(re.search(p, ln, re.I) for p in pats):
            v = [x for x, _ in numbers(ln) if abs(x) >= minabs]
            if len(v) > col:
                return dict(value=abs(v[col]), line=ln.strip()[:140], source=fname,
                            tier='A_AUDITED', route='text_layer_or_ocr')
    return None


# The modern audited statement of financial position, for the last three fiscal years.
AUD_BS = {
    2025: ('2025Q4__EE-Consolidated-En-FS-31-December-2025.filled.txt', 0),
    2024: ('2025Q4__EE-Consolidated-En-FS-31-December-2025.filled.txt', 1),
    2023: ('2024Q4__EE-Consalidated-English-FS-31-December-2024.filled.txt', 1),
}
AUD_BS_LABELS = {
    'ppe':          [r'^\s*Property, plant and equipment\b'],
    'inventories':  [r'^\s*Inventories\b'],
    'cash':         [r'^\s*Cash and cash equivalents\b'],
    'total_assets': [r'^\s*Total assets\b'],
    'total_equity': [r'^\s*Total equity\b'],
}
# These two appear TWICE on the modern balance sheet - non-current and current - and both
# halves are working capital. They are summed, exactly as loans and borrowings are.
AUD_BS_SUMMED = {
    'receivables': [r'^\s*Trade and other receivables\b'],
    'payables':    [r'^\s*Trade and other payables\b'],
}


def aud_bs(fname, col):
    """The statement of financial position, SCOPED TO ITS OWN PAGE, then FOOTED.

    Scoping is not tidiness. A first draft searched the whole filing and summed the
    balance sheet's "Trade and other receivables" with the CASH FLOW STATEMENT'S
    working-capital movement of the same name - EGP 117.7bn of assets plus a negative
    EGP 27.4bn of movement, giving 101.3bn, a number in the right units that foots
    against nothing. The same label means two different things in two statements.

    THEN THE PAGE IS FOOTED THREE WAYS, and it has to be, because this page is the one
    that comes off OCR: non-current plus current assets against total assets, total
    equity plus total liabilities against total assets, and cash against the CASH-FLOW
    statement's own closing balance - which sits on a TEXT-LAYER page. That last check
    is what catches the defect this page actually carries: the OCR renders cash as
    "Al 949 208 624", the leading 41 having become the letters A and l, and a reader
    takes EGP 949,208,624 for EGP 41,949,208,624 - out by a factor of 44, sitting in a
    column of otherwise perfect figures.
    """
    txt = load(fname)
    if txt is None:
        return None
    lines_all = txt.splitlines()
    start = None
    for i, ln in enumerate(lines_all):
        if re.search(r'Consolidated Statement of Financial Position', ln, re.I):
            if any(re.match(r'\s*Total assets\b', lines_all[k], re.I)
                   for k in range(i + 1, min(i + 60, len(lines_all)))):
                start = i
                break
    if start is None:
        return None
    stop = len(lines_all)
    for j in range(start + 1, min(start + 70, len(lines_all))):
        if re.match(r'\s*Tota[lt] equity and liabilities\b', lines_all[j], re.I):
            stop = j + 1
            break
    scope = lines_all[start:stop]

    out, borrow = {}, []
    summed = {k: [] for k in AUD_BS_SUMMED}
    agg = {}
    for ln in scope:
        v = [x for x, _ in numbers(ln) if abs(x) >= 1e6]
        if re.match(r'\s*Loans and borrowings\b', ln, re.I) and len(v) > col:
            borrow.append((v[col], ln.strip()[:110]))
        for key, pats in AUD_BS_SUMMED.items():
            if any(re.match(p, ln, re.I) for p in pats) and len(v) > col:
                summed[key].append((v[col], ln.strip()[:110]))
        for key, pats in AUD_BS_LABELS.items():
            if key in out:
                continue
            if any(re.match(p, ln, re.I) for p in pats) and len(v) > col:
                out[key] = dict(value=v[col], line=ln.strip()[:110], source=fname,
                                tier='A_AUDITED', route='ocr_200dpi')
        for key, pat in (('non_current_assets', r'\s*Non-current assets\b'),
                         ('current_assets', r'\s*Current assets\b'),
                         ('total_liabilities', r'\s*Total liabilities\b'),
                         ('total_eq_and_liab', r'\s*Tota[lt] equity and liabilities\b')):
            if key not in agg and re.match(pat, ln, re.I) and len(v) > col:
                agg[key] = v[col]
    for key, rows in summed.items():
        if rows:
            out[key] = dict(value=sum(v for v, _ in rows), lines=[l for _, l in rows],
                            source=fname, tier='A_AUDITED', route='ocr_200dpi',
                            note='non-current and current halves summed')
    if borrow:
        out['interest_bearing_debt'] = dict(
            value=sum(v for v, _ in borrow), lines=[l for _, l in borrow], source=fname,
            tier='A_AUDITED', route='ocr_200dpi',
            note='loans and borrowings, non-current plus current. Trade and other '
                 'payables, contract liabilities, due to related parties and provisions '
                 'are EXCLUDED: none of them bears interest, and dividing the finance '
                 'charge by a total that includes them understates the borrowing rate by '
                 'a multiple and manufactures a bias that looks exactly like evidence.')

    # ---- the three footing tests ------------------------------------------
    ta = (out.get('total_assets') or {}).get('value')
    te = (out.get('total_equity') or {}).get('value')
    checks = []
    if ta and 'non_current_assets' in agg and 'current_assets' in agg:
        r = agg['non_current_assets'] + agg['current_assets'] - ta
        checks.append(dict(test='non-current + current = total assets', residual=r,
                           verdict='PASS' if abs(r) < 1 else 'FAIL'))
    if ta and te and 'total_liabilities' in agg:
        r = te + agg['total_liabilities'] - ta
        checks.append(dict(test='equity + liabilities = total assets', residual=r,
                           verdict='PASS' if abs(r) < 1 else 'FAIL'))
    cf_cash = cf_line(fname, col, [r'^\s*Cash and cash equivalents at 31 December'])
    if cf_cash and out.get('cash'):
        r = out['cash']['value'] - cf_cash['value']
        ok = abs(r) < 1
        checks.append(dict(test="balance-sheet cash = cash-flow statement's closing cash",
                           residual=r, verdict='PASS' if ok else 'FAIL'))
        if not ok:
            out['cash'] = dict(value=cf_cash['value'], line=cf_cash['line'], source=fname,
                               tier='A_AUDITED', route='text_layer',
                               superseded=dict(value=out['cash']['value'],
                                               line=out['cash']['line'], route='ocr_200dpi'),
                               note='THE BALANCE-SHEET FIGURE WAS REFUSED AND REPLACED. The '
                                    'statement of financial position is on an image-only '
                                    'page and its OCR renders the leading digits of cash as '
                                    'letters; the figure carried here is the one the '
                                    'consolidated statement of cash flows states as its '
                                    'closing balance, which sits on a text-layer page and '
                                    'is the same quantity. Arithmetic is the arbiter, not '
                                    'the extractor.')
    out['_footing'] = checks
    return out or None


def build():
    panel = json.load(open(PANEL))['years']
    origins, prior, missing_log = {}, {}, []

    def block_for(y):
        b, miss = {}, []
        # ---- balance sheet -------------------------------------------------
        if y in AUD_BS:
            got = aud_bs(*AUD_BS[y]) or {}
            for k, v in got.items():
                b[k] = v
        er = E.read_year(y, 'bs') if y in E.ANNUAL_ER else None
        if er:
            mapping = dict(cash='cash', inventories='inventories', receivables='receivables',
                           payables='payables', total_assets='total_assets',
                           total_equity='total_equity', capital='issued_capital',
                           fixed_assets='ppe_or_fixed_assets')
            for src, dst in mapping.items():
                if dst in b or src not in er:
                    continue
                b[dst] = dict(value=er[src]['value'], line=er[src]['line'],
                              source=er['_meta']['file'] if '_meta' in er else None,
                              tier='A_IR', route='text_layer')
            if 'interest_bearing_debt' not in b:
                parts = [(k, er[k]['value'], er[k]['line']) for k in ('st_debt', 'lt_debt')
                         if k in er]
                if parts:
                    b['interest_bearing_debt'] = dict(
                        value=sum(v for _, v, _ in parts),
                        lines=[l for _, _, l in parts],
                        components=[k for k, _, _ in parts],
                        source=er.get('_meta', {}).get('file'), tier='A_IR',
                        route='text_layer',
                        note='bank overdraft and short-term loans plus long-term loans. '
                             'Accounts payable, other credit balances, amounts due to '
                             'affiliates and provisions are EXCLUDED - none bears '
                             'interest [R-FCAL-01 trap (i)].')
                    if len(parts) == 1:
                        miss.append(dict(item='long-term borrowings' if parts[0][0] == 'st_debt'
                                         else 'short-term borrowings',
                                         reason='this vintage of the release prints the '
                                                'balance sheet without that line; the debt '
                                                'total is therefore a FLOOR, and it is '
                                                'labelled as one rather than presented as '
                                                'the whole book'))
                        b['interest_bearing_debt']['is_floor'] = True
        # ---- income-statement-derived flows --------------------------------
        row = panel.get(str(y), {})
        for src, dst in (('dna', 'depreciation_and_amortisation'),):
            if src in row:
                b[dst] = dict(value=abs(row[src]['value']), line=row[src].get('line'),
                              source=row[src].get('source'), tier=row[src].get('tier'),
                              route=row[src].get('route'))
        if 'depreciation_and_amortisation' not in b and y in AUDITED_CF:
            got = cf_line(AUDITED_CF[y][0], AUDITED_CF[y][1], DEP_PATS)
            if got:
                b['depreciation_and_amortisation'] = got
        # ---- capex ---------------------------------------------------------
        if y in AUDITED_CF:
            got = cf_line(AUDITED_CF[y][0], AUDITED_CF[y][1], CAPEX_PATS)
            if got:
                got['disclosed'] = True
                b['capex'] = got
        # ---- share count ---------------------------------------------------
        sh = shares_at(y)
        if sh.get('missing') and b.get('issued_capital'):
            # the recital establishes the par in force; the count is THIS year's own
            # committed capital divided by it, never a count carried back
            par = 10.0
            cap = b['issued_capital']['value']
            sh = dict(shares=cap / par, par_value_egp=par, issued_capital_egp=cap,
                      footing='issued capital %d / par %.0f = %d' % (cap, par, cap / par),
                      foots=True, source=b['issued_capital']['source'], tier='A_IR',
                      route='text_layer',
                      established_by='the par value in force at this date is EGP 10, '
                                     'established by note 29 of the FY2025 audited '
                                     'statements, which records the split to EGP 1 as '
                                     'taking effect on 22 May 2018')
        b['share_count'] = sh
        if sh.get('missing'):
            miss.append(dict(item='share count', reason=sh['reason']))
        for item in ('cash', 'interest_bearing_debt', 'ppe', 'ppe_or_fixed_assets',
                     'depreciation_and_amortisation', 'inventories', 'receivables',
                     'payables', 'capex'):
            pass
        return b, miss

    years = sorted(int(y) for y in panel)
    for y in years:
        b, miss = block_for(y)
        if not b:
            continue
        # capex DERIVED where the cash-flow statement is not to hand
        if 'capex' not in b:
            ppe_key = 'ppe' if 'ppe' in b else 'ppe_or_fixed_assets'
            prev = origins.get(y - 1) or prior.get(y - 1)
            prev_ppe = None
            if prev:
                for k in ('ppe', 'ppe_or_fixed_assets'):
                    if k in prev:
                        prev_ppe = prev[k]['value']
                        break
            dna = (b.get('depreciation_and_amortisation') or {}).get('value')
            if prev_ppe is not None and ppe_key in b and dna:
                b['capex'] = dict(value=b[ppe_key]['value'] - prev_ppe + dna,
                                  disclosed=False, derived=True,
                                  formula='capex = dPP&E + D&A',
                                  note='DERIVED. The cash-flow statement for this year is '
                                       'not in the archive as a machine-readable filing; '
                                       'the identity is not an assumption and this label '
                                       'is what keeps the two apart.',
                                  tier='DERIVED')
            else:
                miss.append(dict(item='capital expenditure',
                                 reason='the cash-flow statement is not to hand for this '
                                        'year and the identity capex = dPP&E + D&A cannot '
                                        'be closed either, because ' +
                                        ('the prior year has no PP&E figure'
                                         if prev_ppe is None else
                                         'this year has no PP&E figure' if ppe_key not in b
                                         else 'no depreciation figure is available')))
        for item, label in (('cash', 'cash and equivalents'),
                            ('interest_bearing_debt', 'interest-bearing debt'),
                            ('depreciation_and_amortisation', 'depreciation and amortisation'),
                            ('inventories', 'inventories'),
                            ('receivables', 'trade and other receivables'),
                            ('payables', 'trade and other payables')):
            if item not in b:
                miss.append(dict(item=label, reason='not disclosed in a machine-readable '
                                                    'filing held for this year'))
        if 'ppe' not in b and 'ppe_or_fixed_assets' not in b:
            miss.append(dict(item='property, plant and equipment',
                             reason='not disclosed in a machine-readable filing held for '
                                    'this year'))
        b['_missing'] = miss
        if 2014 <= y <= 2025:
            origins[y] = b
        else:
            prior[y] = b
        if miss:
            missing_log.append(dict(year=y, missing=[m['item'] for m in miss]))

    out = dict(
        _='SWDY valuation-input block per origin [R-FCAL-01 AMENDED 03-Sep-2026]. '
          'INTERNAL. Built as the run went, not retro-fitted.',
        built='2026-09-07', ticker='SWDY', currency='EGP',
        capital_recital=CAPITAL_RECITAL, capital_recital_source=RECITAL_SOURCE,
        origins={str(k): v for k, v in sorted(origins.items())},
        prior_year_anchor={str(k): v for k, v in sorted(prior.items())},
        missing_summary=missing_log)
    json.dump(out, open(OUT, 'w'), indent=1)
    print('valuation inputs: %d origins, %d prior-year anchors' % (len(origins), len(prior)))
    for m in missing_log:
        if 2014 <= m['year'] <= 2025:
            print('  %d missing: %s' % (m['year'], ', '.join(m['missing'])))
    return out


if __name__ == '__main__':
    build()
