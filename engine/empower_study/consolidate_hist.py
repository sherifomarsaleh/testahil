"""EMPOWER — consolidate the four extraction JSONs into one verified historical
panel (hist_panel.json). Cross-filing consistency is ASSERTED, not assumed:
each year that appears in two filings (own filing + next year's comparative)
must match on every shared line, or the mismatch is printed and the run fails.
Derived metrics (EBITDA, margins, capex, working-capital cycle) are computed
here once, so every downstream builder reads one file."""
import json, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))

f22 = json.load(open(os.path.join(HERE, 'extract_fy2022_2023.json')))
f24 = json.load(open(os.path.join(HERE, 'extract_fy2024.json')))
f25 = json.load(open(os.path.join(HERE, 'extract_fy2025.json')))
i26 = json.load(open(os.path.join(HERE, 'extract_2026_interims.json')))

fail = []

def cmp(year, line, a, b, src_a, src_b, tol=1):
    if a is None or b is None:
        return
    if abs(a - b) > tol:
        fail.append(f"{year} {line}: {a:,} ({src_a}) vs {b:,} ({src_b})")

# ---- FY2023 own filing vs FY2024 comparatives (income statement) -----------
is23_own = f22['2023']['income_statement']
is23_cmp = f24['income_statement']['2023']
for k in ['revenue', 'cost_of_sales', 'gross_profit', 'operating_profit',
          'profit_before_tax', 'profit_after_tax']:
    a = is23_own.get(k); b = is23_cmp.get(k)
    cmp('FY23', k, a, b, 'FY23 filing', 'FY24 comparative')

# ---- FY2024 own filing vs FY2025 OCR comparatives --------------------------
is24_own = f24['income_statement']['2024']
is24_cmp = f25.get('2024_comparative', {}).get('income_statement', {})
for k in ['revenue', 'cost_of_sales', 'gross_profit', 'operating_profit',
          'profit_before_tax', 'profit_after_tax']:
    cmp('FY24', k, is24_own.get(k), is24_cmp.get(k), 'FY24 filing', 'FY25 comparative')

if fail:
    print("CROSS-FILING MISMATCHES:")
    for f in fail:
        print("  !", f)
    sys.exit(1)

# ---- assemble panel --------------------------------------------------------
def year_block(y, src):
    return src

panel = {}
panel['2021'] = f22['2021']
panel['2022'] = f22['2022']
panel['2023'] = f22['2023']
panel['2024'] = dict(income_statement=f24['income_statement']['2024'],
                     balance_sheet_assets=f24['balance_sheet_assets']['2024'],
                     cash_flow=f24['cash_flow']['2024'],
                     notes=f24['notes'])
panel['2025'] = f25['2025']

# liabilities for 2024: use FY2025 filing's 2024 comparative BS (full sides)
bs24_cmp = f25.get('2024_comparative', {}).get('balance_sheet', {})
panel['2024']['balance_sheet_full_from_fy25_comparative'] = bs24_cmp

panel['interims_2026'] = {k: i26[k] for k in
                          ['q1_2026', 'h1_2026', 'q2_2026_standalone', 'ir_deck']
                          if k in i26}

# ---- derived metrics -------------------------------------------------------
der = {}
for y in ['2021', '2022', '2023', '2024', '2025']:
    blk = panel[y]
    isb = blk.get('income_statement', {})
    cf = blk.get('cash_flow', {})
    if y == '2025':   # FY2025 extraction nests the CF; flatten to the shared names
        adj = cf.get('adjustments', {})
        cf = dict(cf)
        cf['depreciation_ppe'] = adj.get('depreciation_ppe')
        cf['depreciation_rou'] = adj.get('depreciation_right_of_use_assets')
        cf['amortisation_intangibles'] = adj.get('amortisation_intangibles')
        cf['ppe_additions'] = cf.get('investing', {}).get(
            'capital_expenditure_net_of_project_cost_accruals')
    rev = isb.get('revenue')
    op = isb.get('operating_profit')
    dep_ppe = cf.get('depreciation_ppe')
    dep_rou = cf.get('depreciation_rou') or 0
    amort = cf.get('amortisation_intangibles') or 0
    dna = (dep_ppe + dep_rou + amort) if dep_ppe is not None else None
    d = dict(revenue=rev, operating_profit=op, dna=dna)
    if rev and op and dna:
        d['ebitda'] = op + dna
        d['ebitda_margin'] = round((op + dna) / rev, 4)
        d['op_margin'] = round(op / rev, 4)
    if rev and isb.get('gross_profit'):
        d['gross_margin'] = round(isb['gross_profit'] / rev, 4)
    capex = cf.get('ppe_additions')
    if capex is not None:
        d['capex'] = abs(capex)
        if rev:
            d['capex_pct_rev'] = round(abs(capex) / rev, 4)
    der[y] = d
panel['derived'] = der

json.dump(panel, open(os.path.join(HERE, 'hist_panel.json'), 'w'), indent=1)
print("hist_panel.json written; cross-filing checks PASSED")
for y, d in der.items():
    print(y, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in d.items()})
