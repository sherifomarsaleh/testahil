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
import datetime as dt
import json, sys, os
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
_XP = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))
XP, ROWS = _XP['expected'], _XP['rows']
SG, RN, DF_ = ROWS['Segments'], ROWS['Relative & Normalized'], ROWS['DCF']
IS, BS, CF = ROWS['Income Statement'], ROWS['Balance Sheet'], ROWS['Cash Flow']
SB, SU, FV, PR = (ROWS['SOTP Bridge'], ROWS['Summary'], ROWS['Fundamental Valuation'],
                  ROWS['Peer & Sector'])
AS = ROWS['Assumptions']
wb = openpyxl.load_workbook(
    os.path.join(HERE, 'ADNOCLS_Valuation_Model_09082026_public.xlsx'))
V = {k: v['value'] for k, v in D['inputs'].items()}
HI, HB, FC, FIN, FBS = D['hist_is'], D['hist_bs'], D['fcst'], D['fin'], D['fcst_bs']
DCF, DCFA, WACC = D['dcf'], D['dcf_beta_alt'], D['wacc']
LN, REL, NRM, BK, SOTP = D['lenses'], D['rel'], D['norm'], D['book'], D['sotp']
FL, SEGF = D['fleet'], D['fcst_seg']


def _charter_window(klass, a, b):
    """Vessel-days and revenue the class's charters out earn over [a, b) — recomputed here
    from the committed charter table, independently of the workbook."""
    lo, hi = dt.date(*map(int, a.split('-'))), dt.date(*map(int, b.split('-')))
    days = rev = 0.0
    for c in FL['charters']:
        if c['klass'] != klass:
            continue
        s_ = dt.date(*map(int, c['start'].split('-')))
        e_ = dt.date(*map(int, c['end'].split('-')))
        n = (min(hi, e_) - max(lo, s_)).days
        if n > 0:
            days += n; rev += n * c['rate']
    return days, rev


CHD_VLCC_Q1, CHR_VLCC_Q1 = _charter_window('vlcc', '2026-01-01', '2026-04-01')
CHD_VLCC_26, CHR_VLCC_26 = _charter_window('vlcc', '2026-01-01', '2027-01-01')
# the crude carriers bought on 7 August 2026 trade spot from their delivery date, so the
# spot vessel-days of that class in 2026 are the owned fleet's days, less the charter days,
# plus theirs — recomputed here from the committed count and that date
ACQ_VLCC_DAYS_26 = V['acq_2026_vlcc'] * (dt.date(2027, 1, 1) - dt.date(2026, 9, 1)).days
# the receivable ratio the forecast uses: the reported one re-based onto the revenue basis
# the forecast is built at, recomputed here from the committed parts
DSO_REBASED = (D['ccc']['dso'][2] * V['rev_fy25']
               / (V['rev_fy25'] - V['seg_rev_tankers_fy25']
                  + FL['tce_rev_25'] * V['tnk_grossup_26']))
BLEND_PE_TTM = ((1 - D['rel']['spot_weight']) * D['peers'][0]['pe_ttm']
                + D['rel']['spot_weight'] * D['peers'][1]['pe_ttm'])
SH, PEG = D['meta']['shares_mn'], D['meta']['fx']


def val(sheet, addr):
    """The model's own value for a cell: the recorded expectation for a formula, or the
    pasted figure itself for a disclosed-history cell."""
    v = XP.get(sheet, {}).get(addr)
    if v is not None:
        return v
    raw = wb[sheet][addr].value
    return float(raw) if isinstance(raw, (int, float)) else None


# sheet, label cell, value cell, words the label must contain, the independent figure
CASES = [
    # --- Summary -------------------------------------------------------------
    ('Summary', f"A{SU['dcf']}", f"C{SU['dcf']}", ['discounted cash flow', 'regressed beta'],
     DCF['fv_aed']),
    ('Summary', f"A{SU['rel']}", f"C{SU['rel']}", ['relative'], LN['relative']['base']),
    ('Summary', f"A{SU['norm']}", f"C{SU['norm']}", ['normalised'], LN['normalized']['base']),
    ('Summary', f"A{SU['book']}", f"C{SU['book']}", ['book value'], LN['book']['base']),
    ('Summary', f"A{SU['central']}", f"C{SU['central']}", ['weighted central'], D['central']),
    ('Summary', f"A{SU['dcfa']}", f"C{SU['dcfa']}", ['composite-index beta'], DCFA['fv_aed']),
    ('Summary', f"A{SU['centrala']}", f"C{SU['centrala']}",
     ['weighted central', 'composite-index beta'], D['central_beta_alt']),
    ('Summary', f"A{SU['dcf']}", f"H{SU['dcf']}", ['discounted cash flow'], DCF['tv_share']),
    ('Summary', f"A{SU['panel']}", f"C{SU['panel']}", ['expert panel'], D['panel_centre']),
    # --- SOTP Bridge ---------------------------------------------------------
    ('SOTP Bridge', f"A{SB['pvex']}", f"C{SB['pvex']}",
     ['present value', 'five forecast years'], DCF['pv_explicit']),
    ('SOTP Bridge', f"A{SB['pvtv']}", f"C{SB['pvtv']}", ['present value', 'terminal value'],
     DCF['pv_tv']),
    ('SOTP Bridge', f"A{SB['evops']}", f"C{SB['evops']}",
     ['enterprise value', 'operations'], DCF['ev_ops']),
    ('SOTP Bridge', f"A{SB['tvshare']}", f"C{SB['tvshare']}",
     ['terminal value', 'share', 'enterprise value'], DCF['tv_share']),
    ('SOTP Bridge', f"A{SB['ev']}", f"C{SB['ev']}", ['enterprise value'], DCF['ev']),
    ('SOTP Bridge', f"A{SB['prenci']}", f"C{SB['prenci']}",
     ['before the minorities'], DCF['ev'] - DCF['net_debt']),
    ('SOTP Bridge', f"A{SB['nci']}", f"C{SB['nci']}",
     ['non-controlling interests', 'contracted price'], -DCF['nci']),
    ('SOTP Bridge', f"A{SB['eq']}", f"C{SB['eq']}", ['equity attributable'], DCF['equity']),
    ('SOTP Bridge', f"A{SB['fvaed']}", f"C{SB['fvaed']}", ['fair value per share', 'aed'],
     DCF['fv_aed']),
    ('SOTP Bridge', f"A{SB['leg0']+1}", f"D{SB['leg0']+1}", ['shipping'],
     SOTP['legs'][1]['ev']),
    ('SOTP Bridge', f"A{SB['mship']}", f"C{SB['mship']}", ['shipping multiple'],
     REL['blend_ev_ebitda']),
    ('SOTP Bridge', f"A{SB['bfv']}", f"C{SB['bfv']}",
     ['sum-of-the-parts', 'fair value per share'], SOTP['fv_aed']),
    # --- Segments: the fleet build, vessel by vessel -------------------------
    ('Segments', f"A{SG['revht']}", f"D{SG['revht']}", ['total revenue'], HI['revenue'][2]),
    ('Segments', f"A{SG['own25']}", f"F{SG['own25']}", ['owned', '31 december 2025'],
     FL['owned_fy25']['vlcc']),
    ('Segments', f"A{SG['own']}", f"F{SG['own']}", ['owned', 'valuation date'],
     FL['owned']['vlcc']),
    # the class vessel-days, the charter days taken out of them, and the spot rate that
    # falls out — the three cells the whole derivation turns on, in the same window
    ('Segments', f"A{SG['cd0']+4}", f"F{SG['cd0']+4}", ['very large crude carrier'],
     FL['owned']['vlcc'] * 90),
    ('Segments', f"A{SG['chd0']+4}", f"F{SG['chd0']+4}", ['very large crude carrier'],
     CHD_VLCC_Q1),
    ('Segments', f"A{SG['sd0']+4}", f"F{SG['sd0']+4}", ['very large crude carrier'],
     FL['owned']['vlcc'] * 90 - CHD_VLCC_Q1),
    ('Segments', f"A{SG['chr0']+4}", f"F{SG['chr0']+4}", ['very large crude carrier'],
     CHR_VLCC_Q1),
    ('Segments', f"A{SG['blend0']+4}", f"F{SG['blend0']+4}", ['very large crude carrier'],
     FL['blend_q1_26']['vlcc']),
    ('Segments', f"A{SG['sp0']+4}", f"F{SG['sp0']+4}", ['very large crude carrier'],
     FL['spot_q1_26']['vlcc']),
    ('Segments', f"A{SG['spb']}", f"F{SG['sp0']+4}", ['implied spot rate', 'removed'],
     FL['spot_q1_26']['vlcc']),
    ('Segments', f"A{SG['sp25']}", f"F{SG['sp25']}", ['2025 implied spot', 'averaged'],
     FL['spot_fy25']['vlcc']),
    ('Segments', f"A{SG['spmid']}", f"F{SG['spmid']}", ['mid-cycle implied spot'],
     FL['spot_mid']['vlcc']),
    ('Segments', f"A{SG['spq1']}", f"F{SG['spq1']}", ['first-quarter 2026', 'implied spot'],
     FL['spot_q1_26']['vlcc']),
    ('Segments', f"A{SG['spq2']}", f"F{SG['spq2']}", ['second-quarter 2026', 'implied spot'],
     FL['spot_q2_26']['vlcc']),
    ('Segments', f"A{SG['ycd0']+4}", f"B{SG['ycd0']+4}", ['very large crude carrier'],
     CHD_VLCC_26),
    ('Segments', f"A{SG['ycrb']}", f"B{SG['ycr0']+4}", ['charter revenue', 'class'],
     CHR_VLCC_26 / 1000.0),
    ('Segments', f"A{SG['ysdb']}", f"B{SG['ysd0']+4}",
     ['spot vessel-days', 'acquired'],
     FL['owned']['vlcc'] * 365 - CHD_VLCC_26 + ACQ_VLCC_DAYS_26),
    # the purchase announced on the anchor date, wherever it lands
    ('Segments', f"A{SG['yacd0']+4}", f"B{SG['yacd0']+4}", ['very large crude carrier'],
     ACQ_VLCC_DAYS_26),
    ('Segments', f"A{SG['acqn']}", f"F{SG['acqn']}", ['bought', '7 august 2026'],
     V['acq_2026_vlcc']),
    ('Segments', f"A{SG['gasvya']}", f"C{SG['gasvya']}",
     ['vessel-years', 'bought on 7 august 2026'], float(V['acq_2026_gas'])),
    ('Segments', f"A{SG['gasvy']}", f"C{SG['gasvy']}", ['contracted vessel-years'],
     FL['gas_vessel_years'][1]),
    ('Segments', f"A{SG['vdays25']}", f"B{SG['vdays25']}", ['vessel-days in 2025'],
     FL['vessel_days_25']),
    ('Segments', f"A{SG['tcerev25']}", f"B{SG['tcerev25']}",
     ['2025 charter-equivalent revenue'], FL['tce_rev_25']),
    ('Segments', f"A{SG['opexd0']}", f"B{SG['opexd0']}", ['running cost per vessel-day'],
     FL['opex_day']),
    ('Segments', f"A{SG['gasrate0']}", f"B{SG['gasrate0']}",
     ['revenue per gas vessel-day'], FL['gas_rate_day']),
    ('Segments', f"A{SG['teb']}", f"B{SG['teb']}", ['tankers', 'ebitda'],
     SEGF['Tankers']['ebitda'][0]),
    ('Segments', f"A{SG['trev']}", f"B{SG['trev']}", ['tankers', 'revenue'],
     SEGF['Tankers']['rev'][0]),
    ('Segments', f"A{SG['gaseb']}", f"B{SG['gaseb']}", ['gas carriers', 'ebitda'],
     SEGF['Gas Carriers']['ebitda'][0]),
    ('Segments', f"A{SG['gasjv']}", f"B{SG['gasjv']}", ['joint-venture profit'],
     -V['jv_gas_fy25'] * (1 + V['opex_escalation'])),
    ('Segments', f"A{SG['frevt']}", f"B{SG['frevt']}", ['total revenue'], FC['revenue'][0]),
    ('Segments', f"A{SG['febt']}", f"B{SG['febt']}", ['total ebitda'], FC['ebitda'][0]),
    ('Segments', f"A{SG['fmgn']}", f"B{SG['fmgn']}", ['ebitda margin'],
     FC['ebitda'][0] / FC['revenue'][0]),
    # --- DCF waterfall -------------------------------------------------------
    ('DCF', f"A{DF_['ebitda']}", f"B{DF_['ebitda']}", ['ebitda'], FC['ebitda'][0]),
    ('DCF', f"A{DF_['ebit']}", f"B{DF_['ebit']}", ['ebit'], FC['ebit'][0]),
    ('DCF', f"A{DF_['nopat']}", f"B{DF_['nopat']}", ['nopat'], FC['nopat'][0]),
    ('DCF', f"A{DF_['fcff']}", f"B{DF_['fcff']}", ['free cash flow to the firm'],
     FC['fcff'][0]),
    ('DCF', f"A{DF_['df']}", f"B{DF_['df']}", ['discount factor'], DCF['df'][0]),
    ('DCF', f"A{DF_['pv']}", f"B{DF_['pv']}", ['present value'], DCF['pv'][0]),
    ('DCF', f"A{DF_['roic']}", f"C{DF_['roic']}",
     ['terminal', 'return on invested capital'], DCF['roic_terminal']),
    ('DCF', f"A{DF_['reinv']}", f"C{DF_['reinv']}", ['reinvestment'], DCF['reinvest']),
    ('DCF', f"A{DF_['tv']}", f"C{DF_['tv']}", ['terminal value'], DCF['tv']),
    ('DCF', f"A{DF_['tvshare']}", f"C{DF_['tvshare']}",
     ['terminal value', 'share', 'enterprise value'], DCF['tv_share']),
    ('DCF', f"A{DF_['ev']}", f"C{DF_['ev']}", ['enterprise value'], DCF['ev']),
    ('DCF', f"A{DF_['prenci']}", f"C{DF_['prenci']}", ['before the minorities'],
     DCF['ev'] - DCF['net_debt']),
    ('DCF', f"A{DF_['ncinav']}", f"C{DF_['ncinav']}",
     ['tanker combination', 'contracted'], V['nci_navig8']),
    ('DCF', f"A{DF_['nciother']}", f"C{DF_['nciother']}",
     ['remaining minorities', 'carrying value'], V['q1_26_nci'] - V['nci_navig8']),
    ('DCF', f"A{DF_['nci']}", f"C{DF_['nci']}",
     ['non-controlling interests', 'contracted price', 'greater of book and value'],
     -DCF['nci']),
    ('DCF', f"A{DF_['eq']}", f"C{DF_['eq']}", ['equity attributable'], DCF['equity']),
    ('DCF', f"A{DF_['fvusd']}", f"C{DF_['fvusd']}", ['fair value per share', 'usd'],
     DCF['fv_usd']),
    ('DCF', f"A{DF_['fvaed']}", f"C{DF_['fvaed']}", ['fair value per share', 'aed'],
     DCF['fv_aed']),
    ('DCF', f"A{DF_['rfstar']}", f"C{DF_['rfstar']}", ['normalised risk-free rate'],
     WACC['rf_star']),
    ('DCF', f"A{DF_['ke']}", f"C{DF_['ke']}", ['cost of equity'], WACC['ke']),
    ('DCF', f"A{DF_['kd1']}", f"C{DF_['kd1']}", ['method 1'], WACC['kd_method1']),
    ('DCF', f"A{DF_['kd2']}", f"C{DF_['kd2']}", ['method 2'], WACC['kd_method2']),
    ('DCF', f"A{DF_['kd3']}", f"C{DF_['kd3']}", ['method 3'], WACC['kd_method3']),
    ('DCF', f"A{DF_['kd']}", f"C{DF_['kd']}", ['cost of debt', 'averaged'], WACC['kd']),
    ('DCF', f"A{DF_['kdat']}", f"C{DF_['kdat']}", ['cost of debt after tax'],
     WACC['kd_after_tax']),
    # the three weights and the two costs of the perpetual leg
    ('DCF', f"A{DF_['hybcap']}", f"C{DF_['hybcap']}",
     ['perpetual capital securities', 'carrying value'], WACC['hybrid_cap']),
    ('DCF', f"A{DF_['captot']}", f"C{DF_['captot']}", ['total capital'],
     WACC['mktcap'] + WACC['debt'] + WACC['hybrid_cap']),
    ('DCF', f"A{DF_['we']}", f"C{DF_['we']}", ['equity weight'], WACC['we']),
    ('DCF', f"A{DF_['wd']}", f"C{DF_['wd']}", ['debt weight'], WACC['wd']),
    ('DCF', f"A{DF_['whyb']}", f"C{DF_['whyb']}",
     ['perpetual capital securities weight'], WACC['wh']),
    ('DCF', f"A{DF_['kh']}", f"C{DF_['kh']}",
     ['cost of the perpetual capital securities', 'own coupon'], WACC['kh']),
    ('DCF', f"A{DF_['khterm']}", f"C{DF_['khterm']}",
     ['terminal cost of the perpetual securities'], WACC['kh_term']),
    ('DCF', f"A{DF_['wacc']}", f"C{DF_['wacc']}", ['cost of capital', 'explicit'],
     WACC['wacc']),
    ('DCF', f"A{DF_['waccterm']}", f"C{DF_['waccterm']}", ['terminal cost of capital'],
     WACC['wacc_term']),
    ('DCF', f"A{DF_['betaa']}", f"C{DF_['betaa']}", ['equal-weight composite', 'alternative'],
     V['beta_composite']),
    ('DCF', f"A{DF_['kea']}", f"C{DF_['kea']}", ['cost of equity', 'composite-index beta'],
     WACC['ke_beta1']),
    ('DCF', f"A{DF_['cilo']}", f"C{DF_['cilo']}", ['lower bound', '90% confidence interval'],
     V['beta_ci_lo']),
    ('DCF', f"A{DF_['cihi']}", f"C{DF_['cihi']}", ['upper bound', '90% confidence interval'],
     V['beta_ci_hi']),
    ('DCF', f"A{DF_['kecilo']}", f"C{DF_['kecilo']}",
     ['cost of equity', 'lower confidence bound'],
     WACC['rf_star'] + V['beta_ci_lo'] * WACC['erp']),
    ('DCF', f"A{DF_['kecihi']}", f"C{DF_['kecihi']}",
     ['cost of equity', 'upper confidence bound'],
     WACC['rf_star'] + V['beta_ci_hi'] * WACC['erp']),
    ('DCF', f"A{DF_['dims']}", f"C{DF_['dims']}", ['lead-lag sum beta'], V['beta_dimson']),
    ('DCF', f"A{DF_['kedims']}", f"C{DF_['kedims']}",
     ['cost of equity', 'lead-lag sum beta'], WACC['ke_dimson']),
    ('DCF', f"A{DF_['fvaeda']}", f"C{DF_['fvaeda']}",
     ['fair value per share', 'composite-index beta'], DCFA['fv_aed']),
    # --- Fundamental Valuation: the two constructions and the interval beside them ----
    ('Fundamental Valuation', f"A{FV['beta']}", f"C{FV['beta']}",
     ['beta', 'published index', 'primary'], D['beta_framing']['primary']['beta']),
    ('Fundamental Valuation', f"A{FV['fv']}", f"C{FV['fv']}",
     ['fair value per share', 'published-index beta'], D['beta_framing']['primary']['fv']),
    ('Fundamental Valuation', f"A{FV['betaa']}", f"C{FV['betaa']}",
     ['beta', 'equal-weight composite', 'alternative'],
     D['beta_framing']['alternative']['beta']),
    ('Fundamental Valuation', f"A{FV['fva']}", f"C{FV['fva']}",
     ['fair value per share', 'composite-index beta'],
     D['beta_framing']['alternative']['fv']),
    ('Fundamental Valuation', f"A{FV['cilo']}", f"C{FV['cilo']}",
     ['lower bound', '90% confidence interval'], D['beta_framing']['ci90'][0]),
    ('Fundamental Valuation', f"A{FV['cihi']}", f"C{FV['cihi']}",
     ['upper bound', '90% confidence interval'], D['beta_framing']['ci90'][1]),
    # --- Income statement ----------------------------------------------------
    ('Income Statement', f"A{IS['rev']}", f"D{IS['rev']}", ['revenue'], HI['revenue'][2]),
    ('Income Statement', f"A{IS['op']}", f"D{IS['op']}", ['operating profit'], HI['ebit'][2]),
    ('Income Statement', f"A{IS['ebitda']}", f"D{IS['ebitda']}", ['ebitda'],
     HI['ebitda_op'][2]),
    ('Income Statement', f"A{IS['ebrep']}", f"D{IS['ebrep']}", ['ebitda', 'reported'],
     HI['ebitda_reported'][2]),
    ('Income Statement', f"A{IS['pbt']}", f"D{IS['pbt']}", ['profit before tax'],
     HI['pbt'][2]),
    ('Income Statement', f"A{IS['npa']}", f"D{IS['npa']}", ['attributable to shareholders'],
     HI['npa'][2]),
    # the two earnings-per-share rows must say WHICH they are: the coupon ranks ahead of
    # the ordinary shares, and a row that does not say so is the ambiguity this gate exists
    # to catch
    ('Income Statement', f"A{IS['ordn']}", f"D{IS['ordn']}",
     ['ordinary shareholders', 'after the perpetual'],
     HI['npa'][2] - V['hybrid_coupon_fy25']),
    ('Income Statement', f"A{IS['npa']}", f"I{IS['npa']}", ['attributable to shareholders'],
     FIN['npa'][4]),
    ('Income Statement', f"A{IS['eps']}", f"E{IS['eps']}",
     ['earnings per ordinary share', 'after the perpetual coupon', 'usd'], FIN['eps'][0]),
    ('Income Statement', f"A{IS['epspre']}", f"E{IS['epspre']}",
     ['before the perpetual coupon'], FIN['eps_pre_coupon'][0]),
    # --- Balance sheet -------------------------------------------------------
    ('Balance Sheet', f"A{BS['nwc']}", f"D{BS['nwc']}", ['net working capital'],
     HB['nwc'][2]),
    ('Balance Sheet', f"A{BS['nd']}", f"I{BS['nd']}", ['net debt'], FIN['net_debt'][4]),
    ('Balance Sheet', f"A{BS['eqp']}", f"I{BS['eqp']}", ['equity attributable'],
     FBS[4]['equity_parent']),
    ('Balance Sheet', f"A{BS['ic']}", f"I{BS['ic']}", ['invested capital'],
     FBS[4]['invested_capital']),
    ('Balance Sheet', f"A{BS['roic']}", f"I{BS['roic']}", ['return on invested capital'],
     FBS[4]['roic']),
    ('Balance Sheet', f"A{BS['roe']}", f"E{BS['roe']}", ['return on equity'], FBS[0]['roe']),
    ('Balance Sheet', f"A{BS['ppeclose']}", f"F{BS['ppeclose']}",
     ['closing property, plant and equipment'], FC['ppe'][4]),
    ('Balance Sheet', f"A{BS['dnatot']}", f"B{BS['dnatot']}",
     ['depreciation and amortisation'], FC['dna'][0]),
    ('Balance Sheet', f"A{BS['wcnwc']}", f"B{BS['wcnwc']}", ['net working capital'],
     FC['nwc'][0]),
    ('Balance Sheet', f"A{BS['wcdnwc']}", f"B{BS['wcdnwc']}",
     ['change in net working capital'], FC['dnwc'][0]),
    ('Balance Sheet', f"A{BS['ndgross']}", f"B{BS['ndgross']}", ['gross borrowings'],
     FIN['gross_debt'][0]),
    ('Balance Sheet', f"A{BS['ndclose']}", f"F{BS['ndclose']}", ['closing net debt'],
     FIN['net_debt'][4]),
    ('Balance Sheet', f"A{BS['eqclose']}", f"F{BS['eqclose']}", ['closing equity'],
     FBS[4]['equity_parent']),
    # --- Cash flow -----------------------------------------------------------
    ('Cash Flow', f"A{CF['fcff']}", f"E{CF['fcff']}", ['free cash flow to the firm'],
     FC['fcff'][0]),
    ('Cash Flow', f"A{CF['fcfe']}", f"E{CF['fcfe']}", ['free cash flow to equity'],
     FC['fcff'][0] - FIN['interest'][0] * (1 - V['tax_stat'])
     + FIN['fin_income'][0] * (1 - V['tax_stat']) - FIN['hybrid_coupon']),
    # --- Relative & Normalized ----------------------------------------------
    ('Relative & Normalized', f"A{RN['base']}", f"C{RN['base']}", ['relative lens'],
     LN['relative']['base']),
    ('Relative & Normalized', f"A{RN['nbase']}", f"C{RN['nbase']}", ['normalised lens'],
     LN['normalized']['base']),
    ('Relative & Normalized', f"A{RN['broe']}", f"C{RN['broe']}",
     ['sustainable return on equity'], BK['roe_sustainable']),
    # the book lens is a RESIDUAL INCOME build now, and every rung of the ladder is checked
    # against the committed detail table rather than the headline alone
    ('Relative & Normalized', f"A{RN['bhdr']}", f"C{RN['beq']}", ['residual income'],
     BK['equity_value']),
    ('Relative & Normalized', f"A{RN['bopen']}", f"C{RN['bopen']}", ['opening ordinary book'],
     BK['detail'][1]['opening_book']),
    ('Relative & Normalized', f"A{RN['broey']}", f"B{RN['broey']}",
     ['return on ordinary equity', 'after the perpetual coupon'], BK['roe_path'][0]),
    ('Relative & Normalized', f"A{RN['bri']}", f"B{RN['bri']}", ['residual income'],
     BK['detail'][0]['residual_income']),
    ('Relative & Normalized', f"A{RN['bdf']}", f"B{RN['bdf']}", ['discount factor'],
     BK['detail'][0]['discount_factor']),
    ('Relative & Normalized', f"A{RN['bpv']}", f"B{RN['bpv']}", ['present value'],
     BK['detail'][0]['pv']),
    ('Relative & Normalized', f"A{RN['btv']}", f"C{RN['btv']}", ['terminal value', 'fading'],
     BK['pv_terminal'] * (1 + BK['ke']) ** 5),
    ('Relative & Normalized', f"A{RN['bpvtv']}", f"C{RN['bpvtv']}",
     ['present value', 'terminal value'], BK['pv_terminal']),
    ('Relative & Normalized', f"A{RN['beq']}", f"C{RN['beq']}",
     ['equity value', 'residual income'], BK['equity_value']),
    ('Relative & Normalized', f"A{RN['bpb']}", f"C{RN['bpb']}", ['price / book'],
     BK['pb_fair']),
    ('Relative & Normalized', f"A{RN['bbase']}", f"C{RN['bbase']}", ['book lens'],
     LN['book']['base']),
    ('Relative & Normalized', f"A{RN['bbear']}", f"C{RN['bbear']}",
     ['bear', 'top', 'confidence interval'], LN['book']['bear']),
    ('Relative & Normalized', f"A{RN['bbear']}", f"D{RN['bbear']}", ['bull', 'bottom'],
     LN['book']['bull']),
    ('Relative & Normalized', f"A{RN['eveb_ttm']}", f"C{RN['eveb_ttm']}",
     ['enterprise value', 'ebitda'], REL['own_ev_ebitda_ttm']),
    # both enterprise-value conventions, each labelled for which it is
    ('Relative & Normalized', f"A{RN['evbr']}", f"C{RN['evbr']}",
     ['bridge', 'perpetual capital securities', 'minorities'], REL['own_ev_bridge']),
    ('Relative & Normalized', f"A{RN['ebbr_26']}", f"C{RN['ebbr_26']}",
     ['fy2026e ebitda', 'bridge convention'], REL['own_ev_ebitda_26_bridge']),
    ('Relative & Normalized', f"A{RN['pe_ttm']}", f"C{RN['pe_ttm']}",
     ['price /', 'ordinary shareholders'], REL['own_pe_ttm']),
    ('Relative & Normalized', f"A{RN['vsratio']}", f"C{RN['vsratio']}",
     ['realised price', 'carrying value'], BK['vessel_value_to_book']),
    # --- Peer & Sector -------------------------------------------------------
    ('Peer & Sector', f"A{PR['mev']}", f"C{PR['mev']}", ['blended enterprise multiple'],
     REL['blend_ev_ebitda']),
    ('Peer & Sector', f"A{PR['pe']}", f"C{PR['pe']}",
     ['blended forward price/earnings'], REL['blend_pe']),
    # the earnings multiple on BOTH bases, each labelled for which it is: the first edition
    # quoted the company trailing against peers shown forward
    ('Peer & Sector', f"A{PR['pe_t']}", f"C{PR['pe_t']}",
     ['blended trailing price/earnings'], BLEND_PE_TTM),
    ('Relative & Normalized', f"A{RN['pe_fwd']}", f"C{RN['pe_fwd']}",
     ['price /', 'forward'], D['wacc']['mktcap'] / D['fin']['npa_ordinary'][0]),
    # --- the cost of debt, labelled for what each construction is ------------
    ('DCF', f"A{DF_['kdbal']}", f"C{DF_['kdbal']}",
     ['balance-weighted', 'method 2'], D['wacc']['kd_balance_weighted']),
    # --- the fleet purchase, in the bridge and on the driver sheet -----------
    ('DCF', f"A{DF_['acq']}", f"C{DF_['acq']}", ['bought on 7 august 2026'],
     -V['acq_2026_cost']),
    ('SOTP Bridge', f"A{SB['acq']}", f"C{SB['acq']}", ['bought on 7 august 2026'],
     -V['acq_2026_cost']),
    ('Assumptions', f"A{AS['acq_cost']}", f"C{AS['acq_cost']}",
     ['purchase price', 'net debt', 'asset base'], V['acq_2026_cost']),
    ('Assumptions', f"A{AS['acq_vlcc']}", f"B{AS['acq_vlcc']}",
     ['very large crude carriers', 'secondhand'], V['acq_2026_vlcc']),
    ('Assumptions', f"A{AS['acq_gas']}", f"B{AS['acq_gas']}",
     ['gas carriers acquired in total'], V['acq_2026_gas']),
    ('Assumptions', f"A{AS['acq_total']}", f"B{AS['acq_total']}", ['vessels acquired'],
     V['acq_2026_vlcc'] + V['acq_2026_gas']),
    ('Balance Sheet', f"A{BS['ppeacq']}", f"B{BS['ppeacq']}",
     ['acquired', '7 august 2026'], V['acq_2026_cost']),
    # --- the receivable ratio, re-based rather than carried across ----------
    ('Assumptions', f"A{AS['dso_rep']}", f"C{AS['dso_rep']}",
     ['days sales outstanding', 'reported'], D['ccc']['dso'][2]),
    ('Assumptions', f"A{AS['dso']}", f"C{AS['dso']}",
     ['days sales outstanding', 're-based'], DSO_REBASED),
    ('Assumptions', f"A{AS['gu25']}", f"C{AS['gu25']}", ['gross-up', '2025'],
     V['seg_rev_tankers_fy25'] / FL['tce_rev_25']),
    ('Assumptions', f"A{AS['gu26']}", f"C{AS['gu26']}", ['gross-up', '2026'],
     V['tnk_grossup_26']),
    # --- depreciation: the rate used, the rate realised, the disclosed lives -
    ('Assumptions', f"A{AS['dep_used']}", f"B{AS['dep_used']}", ['the rate used'],
     V['dep_ppe'] if 'dep_ppe' in V else V['dep_rate_ppe']),
    ('Assumptions', f"A{AS['dep_realised']}", f"B{AS['dep_realised']}",
     ['realised in 2025'], V['dep_rate_realised_fy25']),
    ('Assumptions', f"A{AS['dep_life']}", f"B{AS['dep_life']}",
     ['useful life', 'tankers'], V['life_tankers']),
    # --- the smallest tankers, scaled rather than substituted ---------------
    ('Assumptions', f"A{AS['hs_rel']}", f"C{AS['hs_rel']}",
     ['handysize', 'proportion of the medium-range rate'], V['handysize_relative']),
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
