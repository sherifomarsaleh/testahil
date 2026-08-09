"""Gate (s) — every label must describe its own row.

recalc.py and driver_test.py are both value-oriented: one checks that each formula
reproduces the model, the other that each driver propagates. Neither looks at column A, so a
workbook can pass both with a run of rows labelled one row above their contents — which is
exactly the defect this gate exists to catch.

The test: for each labelled row below, the value the workbook computes in that row must
agree with what the label SAYS it is, computed independently from study_numbers.json. The
label text is also checked for the key words it promises, so a row cannot be silently
relabelled into agreement.
"""
import json, sys, os
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
XP = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))['expected']
wb = openpyxl.load_workbook(
    os.path.join(HERE, 'ADNOCLS_Valuation_Model_09082026_public.xlsx'))
V = {k: v['value'] for k, v in D['inputs'].items()}
HI, HB, FC, FIN, FBS = D['hist_is'], D['hist_bs'], D['fcst'], D['fin'], D['fcst_bs']
DCF, DCFA, WACC = D['dcf'], D['dcf_asset_beta'], D['wacc']
LN, REL, NRM, BK, SOTP = D['lenses'], D['rel'], D['norm'], D['book'], D['sotp']
FL, SEGF = D['fleet'], D['fcst_seg']
SH, PEG = D['meta']['shares_mn'], D['meta']['fx']


def val(sheet, addr):
    return XP.get(sheet, {}).get(addr)


# sheet, label cell, value cell, words the label must contain, the independent figure
CASES = [
    # --- Summary -------------------------------------------------------------
    ('Summary', 'A5', 'C5', ['discounted cash flow', 'regressed beta'], DCF['fv_aed']),
    ('Summary', 'A6', 'C6', ['relative'], LN['relative']['base']),
    ('Summary', 'A7', 'C7', ['normalised'], LN['normalized']['base']),
    ('Summary', 'A8', 'C8', ['book value'], LN['book']['base']),
    ('Summary', 'A9', 'C9', ['weighted central'], D['central']),
    ('Summary', 'A12', 'C12', ['asset-risk beta'], DCFA['fv_aed']),
    ('Summary', 'A13', 'C13', ['weighted central', 'asset-risk beta'],
     D['central_asset_beta']),
    ('Summary', 'A5', 'H5', ['discounted cash flow'], DCF['tv_share']),
    ('Summary', 'A15', 'C15', ['expert panel'], D['panel_centre']),
    # --- SOTP Bridge ---------------------------------------------------------
    ('SOTP Bridge', 'A5', 'C5', ['present value', 'five forecast years'],
     DCF['pv_explicit']),
    ('SOTP Bridge', 'A6', 'C6', ['present value', 'terminal value'], DCF['pv_tv']),
    ('SOTP Bridge', 'A7', 'C7', ['enterprise value', 'operations'], DCF['ev_ops']),
    ('SOTP Bridge', 'A8', 'C8', ['terminal value', 'share', 'enterprise value'],
     DCF['tv_share']),
    ('SOTP Bridge', 'A10', 'C10', ['enterprise value'], DCF['ev']),
    ('SOTP Bridge', 'A15', 'C15', ['equity attributable'], DCF['equity']),
    ('SOTP Bridge', 'A17', 'C17', ['fair value per share', 'aed'], DCF['fv_aed']),
    ('SOTP Bridge', 'A21', 'D21', ['shipping'], SOTP['legs'][1]['ev']),
    ('SOTP Bridge', 'A29', 'C29', ['shipping multiple'], REL['blend_ev_ebitda']),
    ('SOTP Bridge', 'A40', 'C40', ['sum-of-the-parts', 'fair value per share'],
     SOTP['fv_aed']),
    # --- Segments: the unit build -------------------------------------------
    ('Segments', 'A12', 'D12', ['total revenue'], HI['revenue'][2]),
    ('Segments', 'A28', 'F28', ['charters out', 'fixed'], FL['fixed']['vlcc']),
    ('Segments', 'A34', 'F34', ['fy2026', 'time-charter equivalent'],
     (FL['q1_26']['vlcc'] + FL['q2_26']['vlcc']
      + 2 * (FL['q1_26']['vlcc'] * 0.5 + FL['tce_fy25']['vlcc'] * 0.5)) / 4),
    ('Segments', 'A42', 'F42', ['very large crude carrier'], FL['tce_mid']['vlcc']),
    ('Segments', 'A48', 'B48', ['vessel-days'], sum(FL['owned'].values()) * 365),
    ('Segments', 'A51', 'B51', ['tankers', 'ebitda'], SEGF['Tankers']['ebitda'][0]),
    ('Segments', 'A53', 'B53', ['tankers', 'revenue'], SEGF['Tankers']['rev'][0]),
    ('Segments', 'A60', 'B60', ['gas carriers', 'ebitda'],
     SEGF['Gas Carriers']['ebitda'][0]),
    ('Segments', 'A82', 'B82', ['total revenue'], FC['revenue'][0]),
    ('Segments', 'A92', 'B92', ['total ebitda'], FC['ebitda'][0]),
    ('Segments', 'A93', 'B93', ['ebitda margin'], FC['ebitda'][0] / FC['revenue'][0]),
    # --- DCF waterfall -------------------------------------------------------
    ('DCF', 'A6', 'B6', ['ebitda'], FC['ebitda'][0]),
    ('DCF', 'A9', 'B9', ['ebit'], FC['ebit'][0]),
    ('DCF', 'A11', 'B11', ['nopat'], FC['nopat'][0]),
    ('DCF', 'A15', 'B15', ['free cash flow to the firm'], FC['fcff'][0]),
    ('DCF', 'A19', 'B19', ['discount factor'], DCF['df'][0]),
    ('DCF', 'A20', 'B20', ['present value'], DCF['pv'][0]),
    ('DCF', 'A41', 'C41', ['terminal', 'return on invested capital'],
     DCF['roic_terminal']),
    ('DCF', 'A42', 'C42', ['reinvestment'], DCF['reinvest']),
    ('DCF', 'A44', 'C44', ['terminal value'], DCF['tv']),
    ('DCF', 'A48', 'C48', ['terminal value', 'share', 'enterprise value'],
     DCF['tv_share']),
    ('DCF', 'A50', 'C50', ['enterprise value'], DCF['ev']),
    ('DCF', 'A55', 'C55', ['equity attributable'], DCF['equity']),
    ('DCF', 'A56', 'C56', ['fair value per share', 'usd'], DCF['fv_usd']),
    ('DCF', 'A57', 'C57', ['fair value per share', 'aed'], DCF['fv_aed']),
    ('DCF', 'A62', 'C62', ['normalised risk-free rate'], WACC['rf_star']),
    ('DCF', 'A65', 'C65', ['cost of equity'], WACC['ke']),
    ('DCF', 'A70', 'C70', ['method 1'], WACC['kd_method1']),
    ('DCF', 'A86', 'C86', ['method 2'], WACC['kd_method2']),
    ('DCF', 'A87', 'C87', ['method 3'], WACC['kd_method3']),
    ('DCF', 'A88', 'C88', ['cost of debt', 'averaged'], WACC['kd']),
    ('DCF', 'A90', 'C90', ['cost of debt after tax'], WACC['kd_after_tax']),
    ('DCF', 'A95', 'C95', ['equity weight'], WACC['we']),
    ('DCF', 'A96', 'C96', ['debt weight'], WACC['wd']),
    ('DCF', 'A97', 'C97', ['cost of capital', 'explicit'], WACC['wacc']),
    ('DCF', 'A102', 'C102', ['terminal cost of capital'], WACC['wacc_term']),
    ('DCF', 'A106', 'C106', ['cost of equity', 'asset-risk beta'], WACC['ke_beta1']),
    ('DCF', 'A121', 'C121', ['fair value per share', 'asset-risk beta'], DCFA['fv_aed']),
    # --- Income statement ----------------------------------------------------
    ('Income Statement', 'A5', 'D5', ['revenue'], HI['revenue'][2]),
    ('Income Statement', 'A12', 'D12', ['operating profit'], HI['ebit'][2]),
    ('Income Statement', 'A14', 'D14', ['ebitda'], HI['ebitda_op'][2]),
    ('Income Statement', 'A16', 'D16', ['ebitda', 'reported'], HI['ebitda_reported'][2]),
    ('Income Statement', 'A24', 'D24', ['profit before tax'], HI['pbt'][2]),
    ('Income Statement', 'A28', 'D28', ['attributable to shareholders'], HI['npa'][2]),
    ('Income Statement', 'A30', 'D30', ['ordinary shareholders'],
     HI['npa'][2] - V['hybrid_coupon_fy25']),
    ('Income Statement', 'A28', 'I28', ['attributable to shareholders'], FIN['npa'][4]),
    # --- Balance sheet -------------------------------------------------------
    ('Balance Sheet', 'A16', 'D16', ['net working capital'], HB['nwc'][2]),
    ('Balance Sheet', 'A18', 'I18', ['net debt'], FIN['net_debt'][4]),
    ('Balance Sheet', 'A21', 'I21', ['equity attributable'], FBS[4]['equity_parent']),
    ('Balance Sheet', 'A26', 'I26', ['invested capital'], FBS[4]['invested_capital']),
    ('Balance Sheet', 'A27', 'I27', ['return on invested capital'], FBS[4]['roic']),
    ('Balance Sheet', 'A28', 'E28', ['return on equity'], FBS[0]['roe']),
    ('Balance Sheet', 'A36', 'F36', ['closing property, plant and equipment'],
     FC['ppe'][4]),
    ('Balance Sheet', 'A38', 'B38', ['depreciation and amortisation'], FC['dna'][0]),
    ('Balance Sheet', 'A49', 'B49', ['net working capital'], FC['nwc'][0]),
    ('Balance Sheet', 'A50', 'B50', ['change in net working capital'], FC['dnwc'][0]),
    ('Balance Sheet', 'A54', 'B54', ['gross borrowings'], FIN['gross_debt'][0]),
    ('Balance Sheet', 'A62', 'F62', ['closing net debt'], FIN['net_debt'][4]),
    ('Balance Sheet', 'A69', 'F69', ['closing equity'], FBS[4]['equity_parent']),
    # --- Cash flow -----------------------------------------------------------
    ('Cash Flow', 'A15', 'E15', ['free cash flow to the firm'], FC['fcff'][0]),
    ('Cash Flow', 'A19', 'E19', ['free cash flow to equity'],
     FC['fcff'][0] - FIN['interest'][0] * (1 - V['tax_stat'])
     + FIN['fin_income'][0] * (1 - V['tax_stat']) - FIN['hybrid_coupon']),
    # --- Relative & Normalized ----------------------------------------------
    ('Relative & Normalized', 'A19', 'C19', ['relative lens'], LN['relative']['base']),
    ('Relative & Normalized', 'A41', 'C41', ['normalised lens'], LN['normalized']['base']),
    ('Relative & Normalized', 'A48', 'C48', ['sustainable return on equity'],
     BK['roe_sustainable']),
    ('Relative & Normalized', 'A51', 'C51', ['justified price / book'], BK['pb_fair']),
    ('Relative & Normalized', 'A52', 'C52', ['book lens'], LN['book']['base']),
    ('Relative & Normalized', 'A27', 'C27', ['enterprise value', 'ebitda'],
     REL['own_ev_ebitda_ttm']),
    ('Relative & Normalized', 'A29', 'C29', ['price / 2025 ordinary earnings'],
     REL['own_pe_ttm']),
    ('Relative & Normalized', 'A58', 'C58', ['realised price', 'carrying value'],
     BK['vessel_value_to_book']),
    # --- Peer & Sector -------------------------------------------------------
    ('Peer & Sector', 'A13', 'C13', ['blended enterprise multiple'],
     REL['blend_ev_ebitda']),
    ('Peer & Sector', 'A16', 'C16', ['blended price/earnings'], REL['blend_pe']),
]

fails, checked = [], 0
print('LABEL GATE — does each label describe its own row?\n')
for sh, lab_ad, val_ad, words, truth in CASES:
    ws = wb[sh]
    label = str(ws[lab_ad].value or '')
    got = val(sh, val_ad)
    checked += 1
    num_ok = got is not None and abs(got - truth) <= max(1e-6, abs(truth) * 1e-5)
    missing = [w for w in words if w.lower() not in label.lower()]
    ok = num_ok and not missing
    tag = 'OK ' if ok else 'FAIL'
    if not ok:
        fails.append((sh, lab_ad, label, words, got, truth, missing))
    print(f"  [{tag}] {sh:22s} {lab_ad:5s} '{label[:44]:46s}' -> {val_ad:5s} "
          f"{got if got is not None else 'MISSING'} vs {truth:,.4f}"
          + (f'   MISSING WORDS {missing}' if missing else ''))
print()
if fails:
    for f in fails:
        print('  MISLABELLED:', f)
    sys.exit(f'LABEL GATE FAILED — {len(fails)} of {checked} labels do not describe their '
             f'row')
print(f'LABEL GATE OK — {checked} labels checked, every one describes its own row')
