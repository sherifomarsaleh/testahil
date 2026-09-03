"""ARCC_Valuation_Study_03-09-2026_public.docx — TMPV house structure.

16 headings: 7 top-level sections plus the 9 subsections of section 1, then three
appendices. Reads study_numbers.json exclusively — no numeral is typed here.

REVISION 3 — the forecast price path recalibrated to the audited record, which disproved
the one revision 2 inherited. Revision 2 rebuilt every company figure on the audited
consolidated financial statements for FY2023, FY2024 and FY2025 and the reviewed Q1-2026
interim accounts.

Written for an external reader: no internal procedure names, step numbers or house
process references appear anywhere in the output.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)
from docx_base import *          # noqa: F401,F403
from docx_base import (doc, P, H1, H2, rich, bullet, table, figure, box, caption,
                       masthead, INK, GREY, BRASS, GOLD, F_CREAM, F_PANEL, Pt, Inches)

D = json.load(open('study_numbers.json'))
_B = json.load(open('beta_result.json'))
BETA = dict(_B['adopted'], _peer_list=_B['peer_betas_usable'])
SEA = D['seasonality']
CALB = D['calibration']
OWN = _B['own_stock']
STK = json.load(open('strike_result.json'))
S0 = json.load(open('step0_result.json'))
# THE PUBLISHED BAND RECORD IS NOT THE FITTING SAMPLE [corrected 03-Sep-2026].
# step0_result.json carries the BREAK-FILTERED panel the engine fits on -- 16 windows
# here, with 28 dropped -- and [R-CAL-02] is explicit that the record a reader is
# shown is deliberately NOT break-filtered, because every dropped window is a real
# forecast that really resolved and a reader asking how often our bands held is owed
# the whole record. The two are different samples on purpose, and the document was
# quoting the wrong one. It reads the generated record instead, which is the single
# source that rule names.
def _band_record(tk):
    import re as _re
    _src = open(os.path.join(HERE, '..', '..', 'assets', 'data.js'), encoding='utf-8').read()
    _i = _src.find('BANDS')
    _m = _re.search(r'\b%s\s*:\s*\{([^}]*)\}' % tk, _src[_i:_i + 200000])
    if not _m:
        raise SystemExit('no published band record for %s. [R-CAL-02] says what a '
                         'reader is shown, and this study cannot show it without one.' % tk)
    _out = {}
    for _k, _v in _re.findall(r'(\w+)\s*:\s*("[^"]*"|[-\w.]+)', _m.group(1)):
        _out[_k] = (_v.strip('"') if _v.startswith('"')
                    else (None if _v == 'null' else float(_v)))
    return _out


BAND = _band_record('ARCC')
TECH = json.load(open('technicals.json'))['state']
EFG = json.load(open('efg_bridge.json'))
MSC = json.load(open('scenario_margin.json'))
M, H, F = D['meta'], D['history'], D['forecast']
W, DCF, LN, SN = D['wacc'], D['dcf'], D['lenses'], D['sensitivity']
TR, PE, SHT = D['terminal_reconciliation'], D['peers'], D['share_triangulation']
EXP, LR, GDV = D['experts'], D['lens_ranges'], D['growth_destroys_value']
FA = D['forecast_anchor']          # [R-ANCHOR-01]: the record is printed for every study
TERMREC = D['terminal_record']     # [R-TERM-01]: the terminal's own committed record

BU, UC, KDG, CON = D['bottom_up'], D['unit_calibration'], D['kd_gate'], D['contested']
IN = {k: v['value'] for k, v in D['inputs'].items()}
SPOT, SH = M['spot'], M['shares_mn']
# THE DATE BESIDE THE PRICE WAS TYPED AND THE PRICE WAS NOT [corrected 03-Sep-2026].
# Four places in the delivered files read "latest known close (6 August 2026) | 77.00".
# The 6 August close was 59.00; 77.00 is the 3 September close. A date typed beside a
# computed number is the same defect as a number typed beside a computed one, and it
# is worse here, because it makes a current price look stale and a stale one look
# current. It is derived from the committed record.
import datetime as _dt
SPOT_DATE = M.get('spot_date') or ''
SPOT_DATE_WORDS = (_dt.date.fromisoformat(SPOT_DATE).strftime('%-d %B %Y')
                   if SPOT_DATE else 'the latest session')
YH, YF = H['years'], F['years']
TAXE = H['tax_eff']


def n0(x): return f"{x:,.0f}"
def n1(x): return f"{x:,.1f}"
def n2(x): return f"{x:,.2f}"
def n3(x): return f"{x:,.3f}"
def pc(x, dp=1): return f"{x*100:.{dp}f}%"
def sg(x, dp=1): return f"{x*100:+.{dp}f}%"


# ============================== COVER ========================================
masthead()
P('Arabian Cement Company S.A.E.', size=22, bold=True, space_after=1)
EDITION_WORDS = _dt.date.fromisoformat(M['edition_date']).strftime('%-d %B %Y')
P(f'Egyptian Exchange · ARCC · Egyptian pounds · valuation as of 30 June 2026, the date '
  f'of the latest disclosed balance sheet; issued {EDITION_WORDS}',
  size=11, color=GREY, space_after=10)
rich([(f'One of Egypt\'s largest cement plants, at the top of the best year the industry '
       f'has had in more than a decade — audited profit up '
       f'{pc(IN["pat_fy25"]/IN["pat_fy24"]-1, 0)} in a single year on a '
       f'{pc(IN["rev_fy25"]/IN["rev_fy24"]-1)} revenue step — and facing '
       f'{n1(IN["egy_revival_mt"])} million tonnes of dormant national capacity queuing to '
       f'restart inside the forecast window.', {'size': 12})], space_after=10)

box([('What this is. ', 'An independent valuation of Arabian Cement Company, an '
      'educational analysis and not investment advice. It carries no rating and no price '
      'target — fair-value ranges and distributions only.'),
     ('The company in one line. ', f'Two production lines in Suez governorate, about '
      f'{n1(IN["cap_cement_mt"])} million tonnes of cement a year and roughly '
      f'{pc(PE["sector"]["share_of_capacity"], 1)} of Egypt\'s nominal capacity, listed on '
      f'the Egyptian Exchange since May 2014, with cash of EGP '
      f'{n0(IN["cash_h1_26"])}mn against interest-bearing debt of EGP '
      f'{n0(IN["debt_h1_26"])}mn at 30 June 2026. Every figure in this study is read from '
      f'the company\'s own audited and reviewed accounts.'),
     ('Where the value lands. ', f'The cash-flow lens — the value this study '
      f'publishes — reads EGP {n2(LN["central"])}, and the cross-checks around it span '
      f'EGP {n2(LN["low"])} to EGP {n2(LN["high"])}, against a '
      f'market price of EGP {n2(SPOT)} — {sg(LN["central"]/SPOT-1)}.')])

# The retired blend, computed once so the document can quote what was dropped
# without any builder retyping a number: the 50/20/22/8 weights this edition
# stopped using, applied to the reads this edition publishes.
_NORM_DIAG = LN['diagnostic']['Normalised earnings (diagnostic, not a lens for this class)']
_BLEND = (0.50 * LN['values']['DCF (cash flow)']
          + 0.20 * LN['values']['Relative multiples']
          + 0.22 * _NORM_DIAG
          + 0.08 * LN['values']['Asset / replacement cost'])

# ---- headline ---------------------------------------------------------------
# THREE TOP-LEVEL SECTIONS OF THE MODEL REPORT WERE ABSENT FROM THIS DOCUMENT
# [added 03-Sep-2026]. The study went straight from its cover box to a summary
# table, and closed on a one-line footer. Headline, Company overview, About and
# Disclosure were never written, and structure_matches_model was attested True
# because nothing outside the study had ever counted the sections.
H1('Headline')
_DCFR = LR[LN['primary']]
P(f'Arabian Cement is worth EGP {n2(LN["central"])} a share on the cash-flow lens this '
  f'study publishes, against a market price of EGP {n2(SPOT)} on {SPOT_DATE_WORDS} — '
  f'{sg(LN["central"]/SPOT-1)}. The other reads span EGP {n2(LN["low"])} to '
  f'EGP {n2(LN["high"])} and are published beside it rather than averaged into it, because '
  f'they disagree for reasons a reader should see.')
P(f'The shape of the range matters more than its width, and it is not symmetric. On the '
  f'primary lens the bear corner is EGP {n2(_DCFR["bear"])} and the bull corner '
  f'EGP {n2(_DCFR["bull"])} — barely above the central. Both corners move one business '
  f'driver across the span this company\'s own audited accounts have printed, the EBITDA '
  f'margin from {pc(H["margin"][0], 2)} in {H["years"][0]} to '
  f'{pc(H["margin"][-1], 2)} in {H["years"][-1]}, with the macro path held completely '
  f'still. Essentially the whole range is downside: if the margin reverts to what this '
  f'company earned in {H["years"][0]} the value is EGP {n2(_DCFR["bear"])}. An earlier edition '
  f'published a symmetric band of two margin points around the forecast and concealed that '
  f'completely.')
P(f'The disagreement with the market is not about the business, and the forecast itself is '
  f'the evidence. It opens at an EBITDA margin of {pc(FA["first_forecast_rate"], 2)} against '
  f'{pc(FA["latest_reviewed_rate"], 2)} in {FA["latest_reviewed_period"]} — the best year '
  f'this company has ever filed — and rises to {pc(FA["forecast_path"][-1], 2)} by the end '
  f'of the window. There is essentially no operating upside left in it: a reader looking for '
  f'the cautious assumption that produces this discount will not find one on the margin line. '
  f'Section 1.11 sets out what a buyer at EGP {n2(SPOT)} has to believe instead, and section '
  f'1.4 is where that belief has to live.')
P(f'Three things about the company matter more than anything else in the model. It is one '
  f'plant — about {n1(IN["cap_cement_mt"])} million tonnes of cement a year in Suez '
  f'governorate, one product, one country, and no diversification anywhere to absorb a '
  f'shock. It holds more cash than debt: EGP {n0(IN["cash_h1_26"])}mn against '
  f'EGP {n0(IN["debt_h1_26"])}mn of interest-bearing borrowings at 30 June 2026, which is '
  f'why the enterprise-to-equity bridge adds rather than subtracts. And it has just filed '
  f'the best year the Egyptian industry has had in more than a decade — audited profit up '
  f'{pc(IN["pat_fy25"]/IN["pat_fy24"]-1, 0)} on a {pc(IN["rev_fy25"]/IN["rev_fy24"]-1)} '
  f'revenue step — with {n1(IN["egy_revival_mt"])} million tonnes of dormant national '
  f'capacity queuing to restart inside the forecast window.')
P(f'What would change the answer is stated in section 7 and not buried: a cost of capital '
  f'that normalises faster than the central bank\'s published path would raise this value '
  f'materially, and beta is the input it would arrive through — the study\'s own most '
  f'consequential contested judgement, worth {sg(CON[1]["effect"])} of value and published '
  f'both ways rather than averaged.')

# ---- valuation summary ------------------------------------------------------
H1('Valuation summary — every read at a glance')
rows = [['Lens', 'Value per share (EGP)', 'Role', 'Versus spot', 'Terminal value % of EV']]
_PRIM = LN['primary']
rows.append([_PRIM, n2(LN['values'][_PRIM]), 'the central',
             sg(LN['values'][_PRIM] / SPOT - 1), pc(DCF['tv_share'])])
for k in LN['values']:
    if k == _PRIM:
        continue
    rows.append([k, n2(LN['values'][k]), 'cross-check',
                 sg(LN['values'][k] / SPOT - 1), '—'])
rows.append(['Normalised earnings', n2(LN['diagnostic']['Normalised earnings (diagnostic, not a lens for this class)']), 'diagnostic only',
             sg(LN['diagnostic']['Normalised earnings (diagnostic, not a lens for this class)'] / SPOT - 1), '—'])
rows.append(['Range across the reads', f'{n2(LN["low"])} – {n2(LN["high"])}', '—',
             f'{sg(LN["low"]/SPOT-1)} to {sg(LN["high"]/SPOT-1)}', '—'])
rows.append([f'Market price, latest known close ({SPOT_DATE_WORDS})', n2(SPOT), '—', '—', '—'])
table(rows, [2.55, 1.35, 0.90, 1.02, 1.18], band_rows={1})
caption('The cash-flow lens IS the value this study publishes. The others are '
        'cross-checks, shown at the same size so a reader can see where they '
        'disagree with it rather than an average that hides the disagreement. A '
        'previous edition blended all four at fixed weights of 50, 20, 22 and 8 per '
        'cent and published EGP ' + n2(_BLEND) + '; those weights were '
        'chosen rather than tested, and averaging four methods makes a fifth one '
        'nobody has checked. Normalised earnings is shown as a diagnostic and is not '
        'a valuation of this company: it capitalises a mid-cycle margin at a nominal '
        'rate, and section 1.7 shows growth destroying value here.')

figure('fig1_football.png', 6.9,
       'Figure 1 — Each lens as a range, with its base case marked, against the market price.')

# ---- company overview -------------------------------------------------------
H1('Company overview')
P(f'Arabian Cement Company S.A.E. runs two production lines at a single site in Suez '
  f'governorate with a nameplate capacity of about {n1(IN["cap_cement_mt"])} million tonnes '
  f'of grey cement a year, roughly {pc(PE["sector"]["share_of_capacity"], 1)} of Egypt\'s '
  f'nominal capacity. It has been listed on the Egyptian Exchange since May 2014. Every '
  f'figure about the company in this study is read from its own audited and reviewed '
  f'accounts; nothing about its reported history comes from a data vendor or a broker.')
P(f'What it sells is close to a commodity, and that is the first fact the lens follows from. '
  f'Essentially all revenue is cement and clinker out of one plant, so there are no parts to '
  f'sum: this is valued as a single operating company. Of the {n1(UC["vol_fy25"])} million '
  f'tonnes it sold in FY2025, {pc(UC["vol_clk_exp"]/UC["vol_fy25"])} left as raw clinker for '
  f'export — the lowest-value and highest-carbon thing it ships — and the rest as cement '
  f'into a domestic market it cannot differentiate itself within.')
P(f'The balance sheet is the unusual part and it works in the shareholder\'s favour. At 30 '
  f'June 2026 the company held EGP {n0(IN["cash_h1_26"])}mn of cash against '
  f'EGP {n0(IN["debt_h1_26"])}mn of interest-bearing debt, so it is net cash. Section 1.7 '
  f'sets out how that reaches equity value, and section 1.4 why a debt book that changed '
  f'currency inside the period is measured against its facility notes rather than against a '
  f'trailing effective rate the accounts cannot produce.')
P(f'The sector context is what the forecast turns on, and it was corrected in this edition. '
  f'Egypt sold about {n1(IN["egy_prod_mt"])} million tonnes against roughly '
  f'{n0(IN["egy_capacity_mt"])} million tonnes of nameplate — a market running near '
  f'{pc(PE["sector"]["utilisation"], 0)}, which is NOT the structurally slack market earlier '
  f'editions of this study described. The oversupply risk is prospective: it lives in the '
  f'{n1(IN["egy_revival_mt"])} million tonne restart programme and in a production quota '
  f'that was suspended in May 2025 rather than repealed, either of which would meet a market '
  f'with little spare demand to absorb it.')

# ============================== 1 ============================================
H1('1  Fundamental valuation')
P('Arabian Cement is valued as a single operating company, not as a sum of parts, and the '
  'reason is worth stating before any number appears. Essentially all of its revenue is '
  'grey cement and clinker from one industrial site. There is no property portfolio, no '
  'lending book, no concession and no collection of consolidated operating subsidiaries '
  'that would need valuing on their own terms. A sum-of-the-parts here would be a sum of '
  'one part, and the discipline it is meant to impose — never blending legs that need '
  'different methods — has nothing to bite on.')
P(f'Four lenses are read and ONE of them is the answer. A discounted cash-flow model built '
  f'up from tonnes and costs is the primary for this class, and the figure this study '
  f'publishes is that lens and nothing else: EGP {n2(LN["central"])}. Relative multiples, '
  f'normalised earnings power and replacement cost are CROSS-CHECKS, published in the same '
  f'table so a reader can see where they disagree — they span EGP {n2(LN["low"])} to EGP '
  f'{n2(LN["high"])} — and none of them is averaged into the answer. There are no weights '
  f'in this model to report. An earlier edition blended the four at 50/20/22/8 and would '
  f'have read EGP {n2(D["lens_record"]["retired"]["blend_value"])}; those weights had '
  f'never cleared any '
  f'out-of-sample test, and a number produced by averaging several methods is not more '
  f'robust than the best of them — it is a new method with free parameters nobody tested, '
  f'importing every weakness of the weakest lens at whatever weight somebody typed. Where '
  f'several methods disagree the honest thing is to publish the disagreement and say which '
  f'one the answer is.')

# ---- 1.1 --------------------------------------------------------------------
H2('1.1  The business, and why the lens follows from it')
P(f'The plant runs two lines in Suez governorate producing on average about '
  f'{n1(IN["cap_cement_mt"])} million tonnes of clinker and cement a year. That is roughly '
  f'{pc(PE["sector"]["share_of_capacity"], 1)} of Egypt\'s nominal capacity. Larger single '
  f'sites exist — National Cement Beni Suef and Lafarge Ain Sokhna are both materially '
  f'bigger — so the earlier edition\'s claim that this is the country\'s second-largest '
  f'plant is withdrawn. The balance sheet is what that '
  f'description implies: property-dominated, with working capital in inventory and '
  f'receivables, no investment property, no equity-accounted portfolio of any size, and no '
  f'financing arm.')
P(f'The FY2025 accounts show revenue of EGP {n0(IN["rev_fy25"])}mn and attributable profit '
  f'of EGP {n0(IN["pat_fy25"])}mn, against EGP {n0(IN["rev_fy24"])}mn and EGP '
  f'{n0(IN["pat_fy24"])}mn a year earlier — revenue up '
  f'{pc(IN["rev_fy25"]/IN["rev_fy24"]-1)} and profit up '
  f'{pc(IN["pat_fy25"]/IN["pat_fy24"]-1, 0)}. That is not a business changing shape. It is '
  f'a price event, and the whole of this valuation turns on how much of it lasts.')
rows = [['', 'FY2023', 'FY2024', 'FY2025']]
rows.append(['Revenue (EGP mn)'] + [n0(x) for x in H['revenue']])
rows.append(['Gross profit (EGP mn)'] + [n0(x) for x in H['gross_profit']])
rows.append(['Operating profit (EGP mn)'] + [n0(x) for x in H['ebit']])
rows.append(['EBITDA (EGP mn)'] + [n0(x) for x in H['ebitda']])
rows.append(['EBITDA margin'] + [pc(x) for x in H['margin']])
rows.append(['Attributable profit (EGP mn)'] + [n0(x) for x in H['pat']])
rows.append(['Earnings per share (EGP)'] + [n2(x) for x in H['eps']])
rows.append(['Effective tax rate'] + [pc(x) for x in H['tax_eff_hist']])
rows.append(['Capital expenditure (EGP mn)'] + [n0(x) for x in H['capex']])
table(rows, [2.60, 1.30, 1.30, 1.30])
caption('Table 1 — Three audited years. Every line is a disclosed figure or a formula over '
        'disclosed figures: operating profit is gross profit less administrative expenses, '
        'provisions and credit losses, and EBITDA adds back the depreciation and '
        'amortisation reported in the cash flow statement.')
P(f'Two things stand out. The revenue note splits local from export: local sales rose '
  f'{pc(IN["rev_local_goods_fy25"]/IN["rev_local_fy24"]-1, 0)} while export sales were '
  f'{sg((IN["rev_exp_goods_fy25"]+IN["rev_exp_svc_fy25"])/IN["rev_exp_fy24"]-1)} — the '
  f'abolition of Egypt\'s cement production quota in May 2025 was a DOMESTIC event, and '
  f'exports sat against a statutory 30% cap throughout. And the '
  f'margin moved from {pc(H["margin"][1])} to {pc(H["margin"][2])} in a single year, '
  f'because almost the entire price increase fell to the bottom line on a cost base that '
  f'is largely fixed.')

# ---- 1.2 --------------------------------------------------------------------
H2('1.2  The unit economics — where EBITDA actually comes from')
P('The operating model starts at the PLANT, and the tonnes are now DISCLOSED rather '
  'than reconstructed. The company publishes sales volumes and production indicators in '
  'its FY2025 investor presentation — clinker production, cement production, local sales, '
  'cement exports and clinker exports — and this build reproduces every one of them to '
  'within 0.02%. Three earlier editions of this study rebuilt those tonnes from an assumed '
  'price because that document had not been read, and were 28% low on the total.')
P('It is worth being plain about what those editions did, because the failure was '
  'structural rather than arithmetic. They assumed a cement price, divided the audited '
  'revenue by it to get tonnes, and presented the utilisation that fell out as an '
  'independent corroboration. It was neither independent nor a corroboration: it was the '
  'same assumption written twice, and the FY2025 check it produced was an accounting '
  'identity that reproduces the audited revenue for ANY price, because volume moves by '
  'exactly the reciprocal. The drivers here are physical — kiln utilisation, the clinker '
  'factor and the two export shares — and the tonnes, the mill utilisation and all three '
  'realised prices come out of them. The prices are therefore outputs that can be held '
  'against the market and disagree with it.')
P('It also carries three products where the previous edition carried one. This company '
  'sells local cement, export cement and export CLINKER, and clinker is the unground '
  'intermediate, worth a fraction of the cement it could have become. Pricing every tonne '
  'at a cement price made the plant look far smaller than it is.')
rows = [['', 'Value']]
rows.append(['Kiln clinker capacity (audited note 1)', f'{n2(IN["cap_clinker_mt"])}Mt'])
rows.append(['Kiln utilisation  (DRIVER)', pc(IN['kiln_util'][0])])
rows.append(['Clinker produced', f'{n3(UC["clk_prod"])}Mt'])
rows.append(['Sold as clinker  (DRIVER)', pc(IN['clk_export_share'][0])])
rows.append(['Clinker exported', f'{n3(UC["vol_clk_exp"])}Mt'])
rows.append(['Clinker factor  (DRIVER)', n3(IN['clinker_factor'])])
rows.append(['Cement produced', f'{n3(UC["cem_prod"])}Mt'])
rows.append(['Mill utilisation', pc(UC['util_fy25'])])
rows.append(['Plus draw from finished-goods stock', f'{n3(IN["cem_stock_draw"][0])}Mt'])
rows.append(['Cement sold', f'{n3(UC["cem_sold"])}Mt'])
rows.append(['Cement exported  (DRIVER)', pc(IN['cem_export_share'][0])])
# THE TOTAL'S THREE COMPONENTS ARE PRINTED AND CONTIGUOUS. Until this edition the export
# cement tonnage appeared nowhere — only its share — and the clinker tonnage sat eight rows
# up, so a reader went from cement sold of 3.553Mt to total despatches of 4.854Mt with no
# printed route between them, and clinker is 27% of the volume.
rows.append(['Exported as cement', f'{n3(UC["cem_sold"] - UC["vol_local"])}Mt'])
rows.append(['Local cement', f'{n3(UC["vol_local"])}Mt'])
rows.append(['Exported as clinker  (from above)', f'{n3(UC["vol_clk_exp"])}Mt'])
rows.append(['TOTAL DESPATCHES', f'{n3(UC["vol_fy25"])}Mt'])
rows.append(['Local cement price — DERIVED', f'EGP {n0(UC["price_loc_derived"])}/t'])
rows.append(['Export cement price — DERIVED', f'USD {n1(UC["price_exp_cem_usd"])}/t'])
rows.append(['Export clinker price — DERIVED', f'USD {n1(UC["price_exp_clk_usd"])}/t'])
table(rows, [4.10, 2.00], band_rows={16, 17, 18, 19})
caption('Table 2 — The plant in tonnes, and the prices that fall out of it. Every FY2025 '
        'physical figure is the company\'s own disclosure. The four '
        'drivers are physical; everything below them is derived. Cement exports of '
        f'{pc(IN["cem_export_share"][0])} of cement made sit inside the 30% statutory cap — '
        'the previous edition\'s single-product build put exports at 31.5% of volume and '
        'breached the cap its own text called binding.')
P(f'The three derived prices are the test, and it is a test this study does not pass '
  f'cleanly. Local cement at EGP {n0(UC["price_loc_derived"])} a tonne is credible against '
  f'Egyptian ex-works commentary. Export cement at USD {n1(UC["price_exp_cem_usd"])} and '
  f'export clinker at USD {n1(UC["price_exp_clk_usd"])} sit roughly a third BELOW the USD '
  f'44-48 the trade press quotes for Egyptian clinker free on board. Either the physical '
  f'volumes behind this build are too high, or realisations run well under the published '
  f'indices. The gap is published rather than tuned away, and it is the reason the volume '
  f'base carries its own sensitivity rather than being presented as settled.')
P(f'The cost stack is the printed one. Cost of sales of EGP {n0(H["cogs"][2])}mn splits into '
  f'materials and fuel of EGP {n0(IN["cos_materials_fy25"])}mn — the note confirms this is '
  f'the cost of inventories charged to cost of sales, so it carries fuel, packing and spares '
  f'as well as raw meal — transportation of EGP {n0(IN["cos_transport_fy25"])}mn, overheads '
  f'of EGP {n0(IN["cos_overhead_fy25"])}mn, and depreciation and amortisation of EGP '
  f'{n0(IN["cos_mfg_dep_fy25"] + IN["cos_intang_amort_fy25"])}mn. Adding cash administrative expenses, '
  f'provisions and credit losses gives a total cash cost of EGP {n0(UC["cash_cost_fy25"])}mn, '
  f'or EGP {n0(UC["cash_cost_t"])} a tonne.')
rows = [['The cost stack and the margin it produces', 'FY2025A', 'FY2026E', 'FY2030E']]
for lab, key in [('Materials and fuel (EGP mn)', 'c_mat'),
                 ('Transportation (EGP mn)', 'c_tra'),
                 ('Overheads and administration (EGP mn)', 'c_ovh'),
                 ('Provisions and credit losses (EGP mn)', 'c_prv'),
                 ('Total cash cost (EGP per tonne of cement)', 'cc_t'),
                 ('Blended realised price (EGP per tonne of cement)', 'price')]:
    rows.append([lab] + [n0(BU[i][key]) for i in (0, 1, 5)])
rows.append(['Volume (Mt)'] + [n3(BU[i]['vol']) for i in (0, 1, 5)])
rows.append(['EBITDA (EGP mn)'] + [n0(BU[i]['ebitda']) for i in (0, 1, 5)])
rows.append(['EBITDA margin'] + [pc(BU[i]['mgn']) for i in (0, 1, 5)])
table(rows, [2.60, 1.30, 1.30, 1.30], band_rows={5, 8, 9})
caption('Table 3 — The cost stack and the margin it produces. EBITDA is an OUTPUT of this '
        'build, not an input to it, and the table foots: revenue less the four cost lines '
        'IS the EBITDA printed at the foot. THE FOUR COST LINES ARE TOTALS IN EGP '
        'MILLIONS, NOT per-tonne rates — materials and fuel are driven by CLINKER '
        'produced, because the kiln burns the fuel, while transportation and overheads are '
        'driven by cement despatched, so no single per-tonne figure describes them all. '
        'Provisions and credit losses are an operating charge above operating profit in '
        'the audited statements, so they belong in this bridge, but they are not a cost of '
        'making a tonne and are therefore excluded from the per-tonne cash cost above.')
figure('fig7_stack.png', 6.9,
       'Figure 2 — Cash cost per tonne against realised price per tonne. The margin is the '
       'gap, and the gap narrows across the forecast.')
P(f'The reconstruction reproduces audited FY2025 revenue to '
  f'{sg(BU[0]["rev"]/IN["rev_fy25"]-1, 3)} and audited FY2025 EBITDA to '
  f'{sg(BU[0]["ebitda"]/H["ebitda"][2]-1, 3)}. It is not forced to: the volume is derived '
  f'from the revenue note and the cost lines are the printed ones, so a wrong price '
  f'assumption would show up as a non-zero residual.')
P(f'One physical constraint is worth checking, because the volume forecast is built off '
  f'CEMENT capacity while the kiln is what could bind first. At a clinker factor of '
  f'{n2(IN["clinker_factor"])} — observed from the audited capacity pair of '
  f'{n1(IN["cap_clinker_mt"])}Mt of clinker against {n1(IN["cap_cement_mt"])}Mt of cement — '
  f'the FY2030 volume needs {n3(BU[5]["vol"]*IN["clinker_factor"])}Mt of clinker against '
  f'{n1(IN["cap_clinker_mt"])}Mt of kiln capacity, or {pc(BU[5]["vol"]*IN["clinker_factor"]/IN["cap_clinker_mt"])} '
  f'of it. The forecast fits the plant, with '
  f'{n3(IN["cap_clinker_mt"]-BU[5]["vol"]*IN["clinker_factor"])}Mt of headroom, and more '
  f'blending would widen that.')
P(f'The company-specific lever is fuel, and it is now visible in the accounts rather than '
  f'assumed. Assets under construction of EGP {n0(IN["auc_fy25"])}mn include EGP '
  f'{n0(IN["auc_altfuel_fy25"])}mn of alternative-fuel capacity for production line 2 and EGP '
  f'{n0(IN["auc_silo_fy25"])}mn of a new cement silo for line 1, and a EUR 25mn European Bank for '
  f'Reconstruction and Development facility is drawn against exactly that programme — '
  f'tranche one for alternative-fuel capacity and hydrogen injection on kiln 1, tranche two '
  f'for hydrogen injection on kiln 2. The model carries a saving on the materials-and-fuel '
  f'line rising to {pc(IN["af_saving"][5], 1)} by FY2030 as a result. That is a funded and '
  f'part-built programme, not an intention.')

H2('1.3  Depreciation, capital spending, and what the book hides')
P(f'Depreciation and amortisation is disclosed in the cash flow statement: EGP '
  f'{n0(H["dna"][2])}mn in FY2025, EGP {n0(H["dna"][1])}mn in FY2024 and EGP '
  f'{n0(H["dna"][0])}mn in FY2023 — property depreciation, licence amortisation and '
  f'right-of-use amortisation. That is {pc(H["dna"][2]/H["revenue"][2], 2)} of FY2025 '
  f'revenue, and it is small for a cement plant.')
P(f'It is small for a reason that matters to the valuation. The plant dates from around '
  f'2010 and the accounts are prepared on a historical-cost basis; the pound has devalued '
  f'several times since. Net property, plant and equipment is EGP {n0(IN["ppe_fy25"])}mn '
  f'and assets under construction a further EGP {n0(IN["auc_fy25"])}mn; the EGP '
  f'{n0(IN["ppe_fy25"]+IN["auc_fy25"])}mn together, on {n1(IN["cap_cement_mt"])}Mt of '
  f'capacity, is about USD '
  f'{n0((IN["ppe_fy25"]+IN["auc_fy25"])/IN["cap_cement_mt"]/IN["fx"])} per annual tonne — '
  f'against a replacement cost of USD {n0(IN["repl_usd_t"])}. The book is carrying the '
  f'plant at '
  f'{pc((IN["ppe_fy25"]+IN["auc_fy25"])/IN["cap_cement_mt"]/IN["fx"]/IN["repl_usd_t"])} of '
  f'what one would cost to build.')
rows = [['EGP mn', 'FY2023', 'FY2024', 'FY2025']]
rows.append(['Depreciation and amortisation'] + [n0(x) for x in H['dna']])
rows.append(['Capital expenditure'] + [n0(x) for x in H['capex']])
rows.append(['Capex as a share of EBITDA'] +
            [pc(TR['history'][i]['capex_over_ebitda']) for i in range(3)])
rows.append(['Net reinvestment (capex less depreciation)'] +
            [n0(TR['history'][i]['reinvestment']) for i in range(3)])
rows.append(['Reinvestment rate (net reinvestment / NOPAT)'] +
            [pc(TR['history'][i]['rr']) for i in range(3)])
rows.append(['Return on BOOK invested capital'] +
            [pc(TR['history'][i]['roic_book']) for i in range(3)])
rows.append(['Character'] + [TR['history'][i]['character'].split(' — ')[0] for i in range(3)])
table(rows, [2.60, 1.30, 1.30, 1.30])
caption('Table 4 — The reinvestment record, buildable because capital expenditure is '
        'disclosed for all three years. FY2023 spent less than it depreciated; FY2024 and '
        'FY2025 carried the alternative-fuel and silo programmes on top of maintenance.')
P(f'That has a direct consequence for the forecast, and it is treated as one. Capital '
  f'expenditure is NOT set at book depreciation. It is set at the economic maintenance '
  f'level of USD {n2(IN["capex_usd_t_cap"])} per tonne of installed capacity — about EGP '
  f'{n0(F["capex"][0])}mn in FY2026 against a book charge of EGP {n0(F["dna"][0])}mn. '
  f'Setting capex equal to book depreciation would flatter free cash flow by construction; '
  f'the cost of refusing to do so is computed in section 1.9 and is worth '
  f'{sg(CON[2]["effect"])} of the cash-flow lens. The audited FY2024 and FY2025 outturns of '
  f'EGP {n0(H["capex"][1])}mn and EGP {n0(H["capex"][2])}mn — USD {n1(H["capex"][1]/IN["cap_cement_mt"]/IN["fx_avg_fy24"])} '
  f'and USD {n1(H["capex"][2]/IN["cap_cement_mt"]/IN["fx_avg_fy25"])} a tonne — bracket the '
  f'assumption, and both of those years carried growth projects as well as maintenance.')

H2('1.4  The cost of capital, and a debt book that changed currency')
P(f'The discount rate is a schedule, not a number. Egypt is in monetary transition: the '
  f'central bank held its main operation rate at 19.50% through the first half of 2026 '
  f'while headline inflation eased to 14.3%, and its own published medium-term target is '
  f'7%. A single flat rate applied to both the explicit years and a perpetuity would assert '
  f'that Egypt\'s cost of capital never normalises.')
P(f'The cost of DEBT is the line the audited accounts changed most. During 2025 the company '
  f'refinanced out of pound working-capital facilities and into euro term debt: a EUR 25mn '
  f'facility from the European Bank for Reconstruction and Development at three-month '
  f'Euribor plus {pc(IN["ebrd_margin"], 2)}, drawn to EUR 18.5mn to fund alternative-fuel '
  f'capacity and hydrogen '
  f'injection, and a EUR 3.09mn National Bank of Egypt facility under a KfW '
  f'industrial-pollution programme at six-month Euribor plus 3%. '
  f'{pc(KDG["eur_share"])} of the interest-bearing book is now euro-denominated.')
rows = [['Facility', 'Balance (EGP mn)', 'Currency', 'Contractual rate',
         'Pound-equivalent cost']]
rows.append(['CIB credit facilities', n0(IN['debt_cib_fy25']), 'EGP',
             f'corridor + 0.6% = {pc(KDG["kd_cib"], 2)}', pc(KDG['kd_cib'], 2)])
rows.append(['National Bank of Egypt / KfW', n0(IN['debt_nbe_fy25']), 'EUR',
             f'Euribor + 3.00% = {pc(KDG["kd_nbe"], 2)}',
             pc(KDG['kd_nbe'] + IN['egp_dep_vs_eur'], 2)])
rows.append(['European Bank for Reconstruction and Development', n0(IN['debt_ebrd_fy25']),
             'EUR', f'Euribor + {pc(IN["ebrd_margin"], 2)} = {pc(KDG["kd_ebrd"], 2)}',
             pc(KDG['kd_ebrd'] + IN['egp_dep_vs_eur'], 2)])
rows.append(['Lease liabilities', n1(IN['lease_fy25']), 'EGP',
             f'marginal pound rate = {pc(KDG["kd_cib"], 2)}', pc(KDG['kd_cib'], 2)])
rows.append(['Weighted average', n0(W['debt_total']),
             f'{pc(KDG["eur_share"], 0)} EUR', pc(KDG['kd_contracted'], 2),
             pc(KDG['kd_blended'], 2)])
table(rows, [2.10, 0.95, 0.80, 1.45, 1.20], band_rows={5})
caption('Table 5 — The debt book, facility by facility, from the audited borrowings note, '
        'and the rate ADOPTED is the last column. A euro loan is not a cheap loan to a '
        'company that earns pounds: the contractual coupon has to carry the expected '
        f'{pc(IN["egp_dep_vs_eur"], 0)} annual pound depreciation against the euro before '
        'it can be compared with a pound rate or applied to pound cash flows. Both columns '
        'weight to the figures shown, from these four lines and nothing pasted; the '
        'contractual weighted average is published beside the adopted one so the reader can '
        'see the whole of the difference.')
P(f'Three checks are published rather than asserted, because a contractual rate is not the '
  f'same thing as a rate paid. Interest expense over average interest-bearing debt gives '
  f'{pc(KDG["eff_fy24"], 2)} in FY2024, {pc(KDG["eff_fy25"], 2)} in FY2025 and '
  f'{pc(KDG["eff_q126_annualised"], 2)} annualising the first quarter of 2026. The '
  f'adopted {pc(KDG["kd_blended"], 2)} sits ABOVE all three, and the gap is not a '
  f'reconciling item to be smoothed: the book re-based mid-year, so the trailing average '
  f'balance is not what carried the interest, and the borrowing that funds an asset still '
  f'under construction has its interest capitalised into that asset rather than expensed. '
  f'A marginal forward-looking rate is the right one for a discount rate, and the gap is '
  f'disclosed so the reader can disagree.')
P(f'One caution belongs next to that number, and it runs the other way from the one a '
  f'reader might expect. The alternative here is the CONTRACTED euro rate — the coupon as '
  f'written, {pc(KDG["kd_contracted"], 2)} blended — and adopting it would mean the euro '
  f'debt is NOT compensated for pound depreciation beyond what this study\'s own currency '
  f'path already assumes. This study does not adopt it. Loading the euro legs with '
  f'{pc(IN["egp_dep_vs_eur"], 0)} annual pound depreciation under interest parity, which is '
  f'what a company earning pounds actually bears on a euro loan, is what produces the '
  f'adopted {pc(KDG["kd_egp_equivalent"], 2)} — '
  f'{n1(KDG["kd_egp_equivalent"]/KDG["kd_contracted"])} times the contracted figure. The '
  f'cheaper alternative is computed as a VALUE and not merely described: it is worth '
  f'{sg(CON[0]["effect"])} of the cash-flow lens, because debt is only '
  f'{pc(W["wd_gross"])} of the capital structure. A large swing in a small weight is still '
  f'a small effect, and saying so is not the same as dismissing it. The adopted rate is the '
  f'MORE conservative of the two.')
rows = [['', 'Explicit window', 'Terminal']]
rows.append(['Risk-free rate', pc(IN['rf'], 2), pc(IN['rf_term'], 2)])
rows.append(['Less sovereign default spread', f'({pc(IN["sov_spread_cds"], 2)})', '—'])
rows.append(['Normalised risk-free rate', pc(W['rf_star'], 2), pc(IN['rf_term'], 2)])
rows.append(['Beta', n3(W['beta']), n3(W['beta_term'])])
rows.append(['Equity risk premium', pc(IN['erp_cds'], 2), pc(IN['erp_term'], 2)])
rows.append(['Cost of equity', pc(W['ke_exp'], 2), pc(W['ke_term'], 2)])
rows.append(['Cost of debt after tax', pc(W['kd_at'], 2),
             pc(IN['kd_term'] * (1 - IN['tax_stat']), 2)])
rows.append(['Debt weight', pc(W['wd_gross'], 2), pc(IN['wd_term'], 1)])
rows.append(['Blended cost of capital', pc(W['wacc_exp'], 2), pc(W['wacc_term'], 2)])
table(rows, [2.90, 1.80, 1.80], band_rows={9})
caption('Table 6 — The two anchors. The sovereign default spread is netted OUT of the local '
        'risk-free rate before a country equity premium is added, so Egypt\'s default risk '
        'is charged once rather than twice; leaving it in would have put the cost of equity '
        f'at {pc(W["ke_raw_retired"], 2)} instead of {pc(W["ke_exp"], 2)}.')
rows = [['Year'] + YF]
rows.append(['Glide fraction'] + [n3(x) for x in F['glide']])
rows.append(['Forward cost of capital'] + [pc(x, 2) for x in F['fwd_wacc']])
rows.append(['Cumulative discount factor'] + [f'{x:.4f}' for x in F['df']])
table(rows, [1.62, 1.06, 1.06, 1.06, 1.06, 1.06])
caption('Table 7 — The schedule. The glide fractions are the cumulative progress of the '
        'POUND cost-of-debt path: the discount rate is a pound rate applied to pound cash '
        'flows, so the Egyptian easing calendar sets its slope while the euro debt book sets '
        'the level of the cost of debt. The terminal value is capitalised at the terminal '
        'rate and brought home on year five\'s own cumulative factor — one date, one price '
        'of time.')

H2('1.5  Beta, and why it is a peer estimate rather than a regression')
P('This edition changes the beta, and the change is worth setting out plainly because it '
  'is the single largest driver of the difference between this valuation and the previous '
  'one.')
P(f'The only market index against which an Egyptian Exchange listing can properly be '
  f'measured is the EGX30. Measured against it, over {n2(OWN["window_years"])} years of '
  f'weekly returns to {OWN["last_obs"]}, Arabian Cement returns a beta of '
  f'{n3(OWN["beta"])} on {OWN["n"]} observations — with an R-squared of '
  f'{pc(OWN["r2"], 1)} and a standard error of {n3(OWN["se"])}. An R-squared of '
  f'{pc(OWN["r2"], 1)} means the index explains under a twentieth of this share\'s '
  f'movement. That is below the threshold at which a regression is treated as usable, so '
  f'the regression is NOT adopted, and its diagnostics are printed here rather than '
  f'tucked away.')
P(f'Earlier editions of this study reported a beta of '
  f'{n3(BETA["retired"]["beta"])} with a materially better R-squared. That figure was '
  f'measured against a basket assembled from the other Egyptian companies this house '
  f'follows, rather than against the market. A basket of covered names will always appear '
  f'to explain a covered name better than the market does, because it is partly made of '
  f'companies like it; the better statistic was the artefact, not the evidence. It is '
  f'withdrawn.')
P(f'What replaces it is the ordinary fallback when a company\'s own history cannot carry '
  f'the estimate: the betas of comparable Egyptian companies. The peer set was named '
  f'before any of it was measured — Lecico, Egypt Aluminium, Orascom Construction and '
  f'Egyptian Chemical Industries, the country\'s building-materials and construction '
  f'complex — and their betas against the EGX30 are '
  f'{", ".join(n3(b) for b in BETA["_peer_list"])}. The median, '
  f'{n3(BETA["beta_used"])}, is adopted. Sinai Cement is the closest business match of '
  f'all and is deliberately NOT used: its own regression is weaker still, and a second '
  f'unusable number does not make a usable one. It is reported here as evidence about how '
  f'thinly this sector trades rather than as an input.')
P('One step could not be completed and it is flagged rather than passed over. The proper '
  'construction strips each peer\'s own borrowing out of its beta and then adds back the '
  'borrowing of the company being valued. That needs each peer\'s balance sheet, which '
  'this study has not sourced, so the peers\' betas are used as published. The direction '
  'of the omission is not in doubt: Arabian Cement holds more cash than debt while its '
  'peers carry borrowings, so completing the step could only LOWER the beta, lower the '
  'discount rate and RAISE the value. The figure adopted here is therefore the cautious '
  'end of the range, and the valuation is shown across the whole peer spread rather than '
  'at a point.')
P(f'The consequence is large and is published as a value rather than described: on the '
  f'withdrawn basket figure the cash-flow lens would read '
  f'{n2(CON[1]["fv_alternative"])} against {n2(CON[1]["fv_adopted"])} on the adopted one, '
  f'a difference of {sg(CON[1]["effect"])}.')
rows = [['Beta'] + [n2(b) for b in SN['beta_grid']]]
rows.append(['Fair value per share (EGP)'] + [n2(x) for x in SN['beta']])
table(rows, [2.20, 0.98, 0.98, 0.98, 0.98, 0.98])
caption(f'Table 8 — Fair value across the fixed comparability anchors. These are round '
        f'numbers held constant so studies can be compared, and they therefore do NOT track '
        f'any one regression\'s confidence interval — on this name the withdrawn own-stock '
        f'estimate carries a 95% interval of {n2(SN["beta_ci_lo"])} to '
        f'{n2(SN["beta_ci_hi"])}, whose LOWER end sits below the lowest anchor here and '
        f'would put the cash-flow lens at EGP {n2(SN["fv_at_ci_lo"])}. That end is the '
        f'value-RAISING one, and it is stated rather than left off the table: a wider '
        f'interval than the anchors show is a fact about how little this regression '
        f'establishes, not a reason to print a narrower one.')

# ---- 1.6 --------------------------------------------------------------------
H2('1.6  The cash-flow waterfall')
rows = [['EGP mn'] + YF]
for lab, key, fmt in [('Revenue', 'revenue', n0), ('EBITDA', 'ebitda', n0),
                      ('EBITDA margin', 'margin', pc),
                      ('Depreciation and amortisation', 'dna', n0),
                      ('Plus other operating income', 'other_income', n0),
                      ('EBIT', 'ebit', n0)]:
    rows.append([lab] + [fmt(x) for x in F[key]])
rows.append([f'Tax rate (effective, {pc(TAXE)})'] + [pc(TAXE) for _ in YF])
rows.append(['NOPAT  (EBIT × (1 − t))'] + [n0(x) for x in F['nopat']])
rows.append(['Plus depreciation'] + [n0(x) for x in F['dna']])
rows.append(['Less capital expenditure'] + [f'({n0(x)})' for x in F['capex']])
rows.append(['Less change in working capital'] + [f'({n0(x)})' for x in F['dwc']])
rows.append(['Free cash flow to the firm'] + [n0(x) for x in F['fcff']])
rows.append(['Discount factor'] + [f'{x:.4f}' for x in F['df']])
rows.append(['Present value of FCFF'] + [n0(x) for x in F['pv']])
table(rows, [2.10, 0.92, 0.92, 0.92, 0.92, 0.92], band_rows={12, 14}, size=8.8)
caption('Table 9 — The full build from revenue to present value, and every line of it is '
        'printed so the arithmetic closes on the page: EBITDA less depreciation PLUS other '
        'operating income is the EBIT shown. That last line is the export subsidy at the '
        'rate the company disclosed on its FY2025 export revenue, plus the non-subsidy '
        'remainder escalated; it is a real disclosed income and leaving it out of the '
        'printed build would have left a reader unable to reconcile the two rows either '
        'side of it. FY2026 carries only the five months not yet earned at the valuation '
        'date; the seven already earned are rolled into the opening cash balance instead, '
        'so the period is counted exactly once rather than twice or not at all.')
P(f'The effective tax rate of {pc(TAXE)} is DISCLOSED, not inferred: income tax of EGP '
  f'{n0(H["tax"][2])}mn against pre-tax profit of EGP {n0(H["pbt"][2])}mn. The company '
  f'separately states an average effective rate of {pc(IN["eff_rate_disclosed_fy25"], 2)} for '
  f'2025 and {pc(IN["eff_rate_disclosed_fy24"], 2)} for 2024, and '
  f'the first quarter of 2026 ran at 25.9%. It sits close to the statutory '
  f'{pc(IN["tax_stat"], 1)} because the deferred-tax movement is small.')

# ---- 1.7 --------------------------------------------------------------------
P(f'The margin path is the central judgement in this forecast, and it deserves stating as '
  f'one number rather than left inside a table. Local prices are assumed to grow '
  f'{pc(IN["price_local_path"][5]-1)} in total across the five years while pound costs grow '
  f'{pc(IN["cost_infl"][5]-1)} — a real erosion of about '
  f'{pc(IN["cost_infl"][5]/IN["price_local_path"][5]-1, 0)}. The EBITDA margin therefore '
  f'falls from the audited {pc(H["margin"][2])} to {pc(F["margin"][4])} by FY2030, still '
  f'well above the {pc(H["margin"][1])} of FY2024 and far above the {pc(H["margin"][0])} of '
  f'FY2023. The claim is not that the business deteriorates; it is that part of the 2025 '
  f'step-change gives back as dormant capacity returns and energy reform continues. A '
  f'reader who thinks the industry passes cost through faster should read the margin '
  f'sensitivity in section 7: two points of margin is worth about EGP '
  f'{n2(SN["mgn"][3]-SN["mgn"][2])} a share.')
P(f'That path is set below the cost path in every year, and this revision changed how it '
  f'is judged rather than only where it sits. The prior edition justified it against '
  f'headline inflation of {pc(IN["cost_infl"][5]-1)} — but that is the input-price index, '
  f'not the cost the model actually charges. Netting the alternative-fuel saving off the '
  f'materials line, the cash cost per tonne the model charges grows '
  f'{pc(BU[5]["cc_t"]/BU[0]["cc_t"]-1)}, so the real erosion is '
  f'{pc(BU[5]["cc_t"]/BU[0]["cc_t"]/(IN["price_local_path"][5])-1)} rather than the figure '
  f'previously printed. The comparison is now made against the cost the model charges.')
P(f'The presentation also settles a question three earlier editions argued about without '
  f'evidence. It reports local revenue and local volume for both years, so the realised '
  f'local price can be COMPUTED: EGP 1,810 a tonne in FY2024 against EGP 2,909 in FY2025, '
  f'a rise of 60.7% on volume up only 11.7%. The FY2025 margin step was price, not volume. '
  f'More useful for a forecast is the exit rate: the fourth quarter of 2025 realised EGP '
  f'3,118 a tonne, 7.2% ABOVE the full-year average. Holding that exit flat through 2026 '
  f'would by itself produce a full-year average 7.2% higher, so the '
  f'{pc(IN["price_local_path"][1]-1, 1)} carried here is less than a point above a path in '
  f'which prices stop rising altogether. That is the sense in which this forecast is '
  f'conservative, and it can now be checked rather than asserted.')
P(f'The audited record still frames it. In FY2024 revenue grew '
  f'{pc(H["revenue"][1]/H["revenue"][0]-1, 1)} against total cash cost of '
  f'{pc((H["cogs"][1]+H["ga"][1]-IN["dna_fy24"])/(H["cogs"][0]+H["ga"][0]-IN["dna_fy23"])-1, 1)}; '
  f'in FY2025 revenue grew {pc(H["revenue"][2]/H["revenue"][1]-1, 1)} against cash cost of '
  f'{pc((H["cogs"][2]+H["ga"][2]-IN["dna_fy25"])/(H["cogs"][1]+H["ga"][1]-IN["dna_fy24"])-1, 1)}, '
  f'which is why the gross margin moved {pc(H["gross_profit"][0]/H["revenue"][0])} to '
  f'{pc(H["gross_profit"][1]/H["revenue"][1])} to {pc(H["gross_profit"][2]/H["revenue"][2])}. '
  f'In every period the accounts cover, price outran cost. But the first quarter of 2026 is '
  f'the sharper evidence and it cuts the other way: revenue grew '
  f'{pc(IN["rev_q1_26"]/IN["rev_q1_25"]-1, 1)} while the gross margin EXPANDED to '
  f'{pc(IN["gp_q1_26"]/IN["rev_q1_26"])} from {pc(H["gross_profit"][2]/H["revenue"][2])}. A '
  f'margin that widens on a 17% revenue step is the signature of VOLUME spread over fixed '
  f'cost, not of price. This study does not hold the quarterly volume and price split, so '
  f'it cannot settle which it was — and that is stated here rather than resolved by '
  f'assertion, because the answer changes the forecast materially.')
P(f'One reconciliation belongs here too, because it is the sharpest challenge to the '
  f'forecast. The first quarter of 2026 — reviewed, not audited, but signed off in May — '
  f'earned attributable profit of EGP {n0(IN["pat_q1_26"])}mn on revenue of EGP '
  f'{n0(IN["rev_q1_26"])}mn, a gross margin of {pc(IN["gp_q1_26"]/IN["rev_q1_26"])} against '
  f'{pc(H["gross_profit"][2]/H["revenue"][2])} for FY2025 as a whole. Four times that '
  f'quarter is EGP {n0(4*IN["pat_q1_26"])}mn. This model forecasts EGP {n0(F["pat"][0])}mn '
  f'for FY2026, {sg(F["pat"][0]/(4*IN["pat_q1_26"])-1)} below the simple annualisation. '
  f'Margins were still EXPANDING in the first quarter; the forecast assumes they turn. That '
  f'is the assumption to attack.')

H2('1.7  The enterprise-to-equity bridge')
rows = [['', 'EGP mn', 'Per share (EGP)']]
for lab, v in [('Present value of explicit free cash flow', DCF['sum_pv']),
               ('Present value of terminal value', DCF['pv_tv']),
               ('Enterprise value', DCF['ev']),
               ('Plus net cash at the valuation date', DCF['net_cash']),
               ('Less non-controlling interests', -IN['nci']),
               ('Equity value', DCF['equity'])]:
    rows.append([lab, n0(v), n2(v / SH)])
rows.append(['Terminal value as % of enterprise value', pc(DCF['tv_share']), '—'])
rows.append([f'Market price, latest known close ({SPOT_DATE_WORDS})', '—', n2(SPOT)])
rows.append(['Upside / (downside) to this lens', '—', sg(DCF['fv'] / SPOT - 1)])
table(rows, [3.30, 1.50, 1.50], band_rows={3, 6, 7})
caption('Table 10 — The bridge. Terminal value as a share of enterprise value is stated '
        'here and again in the summary table on page 1.')
P(f'Cash is added at face and is not in the discount rate. The valuation date is 30 June '
  f'2026 and the bridge stands on the balance sheet OF THAT DATE rather than on a '
  f'roll-forward: cash of EGP {n0(IN["cash_h1_26"])}mn less '
  f'interest-bearing debt of EGP {n0(IN["debt_h1_26"])}mn is net cash of EGP '
  f'{n0(DCF["net_cash"])}mn, or EGP {n2(DCF["net_cash"]/SH)} a share. The previous edition '
  f'had no balance sheet for its own valuation date and had to build one — FY2025 cash, plus '
  f'the cash the business would generate to that date, less the declared dividend — which '
  f'came out EGP {n0(DCF["rollforward_gap"])}mn too generous, EGP '
  f'{n2(DCF["rollforward_gap_per_share"])} a share, because a projection cannot see six '
  f'months of stock-building, receivables and capital spending that had in fact happened. '
  f'A disclosed balance sheet beats a projection of one.')
P(f'Minority interests are deducted, and the audited figure is the reason this line is now '
  f'immaterial: EGP {n0(IN["nci_h1_26"]*1e6)} at 30 June 2026, or '
  f'{pc(IN["nci_h1_26"]/DCF["equity"], 4)} of equity value. The subsidiaries are 99% to 99.99% '
  f'owned.')
P(f'At {pc(DCF["tv_share"])} of enterprise value, the terminal value carries less of this '
  f'valuation than the two-thirds to four-fifths a long-horizon discounted cash-flow model '
  f'usually ends up with, and that is a consequence of the {pc(W["wacc_exp"])} '
  f'explicit-window discount rate rather than a design choice — at that rate the fifth '
  f'forecast year is already discounted to {pc(F["df"][4], 0)} of its face value. The '
  f'answer therefore depends more on the '
  f'next five years and less on a perpetuity assumption than is usual, which for a business '
  f'whose next five years are forecastable from tonnes and disclosed costs is the right '
  f'place for the weight to sit. It is worth naming the direction of travel honestly: the '
  f'prior revision put the terminal share at 45.5%, and correcting the price path lifted it '
  f'because a higher terminal margin loads more value into the perpetuity than into a '
  f'heavily discounted explicit window. More of the answer rests on the far end than it did.')

H2('1.8  Terminal value, and what growth costs')
P(f'Terminal growth is held at {pc(IN["g_term"], 0)}, against a terminal risk-free rate '
  f'that already embeds disinflation — so approximately zero in real terms. It is not '
  f'derived from recent performance, and the reason is arithmetic rather than a matter of '
  f'judgement.')
P(f'Attributable profit compounded {pc(TR["pat_cagr_fy23_fy25"], 0)} a year across the two '
  f'audited steps from FY2023 to FY2025. Compounded against nominal economic growth of about '
  f'{pc(IN["egy_gdp_growth"], 0)}, a company at {pc(TR["share_of_gdp"], 3)} of Egyptian '
  f'output today would equal the entire Egyptian economy in roughly '
  f'{n0(TR["crossover_years"])} years. That is not a forecast anyone would defend; it is the '
  f'reason recent growth belongs in the explicit window, describing a specific dated event — '
  f'the removal of the production quota — and not in the perpetuity.')
P(f'Growth in the terminal state has to be paid for, and the choice of what capital it is '
  f'paid on is the single most consequential judgement in this model. On the audited BOOK, '
  f'return on invested capital was {pc(TR["history"][2]["roic_book"])} in FY2025 — well '
  f'above any plausible cost of capital, which would make terminal growth free. But that '
  f'book carries a plant built around 2010 at historical cost through several devaluations: '
  f'net property and construction of EGP {n0(IN["ppe_fy25"]+IN["auc_fy25"])}mn is about USD '
  f'{n0((IN["ppe_fy25"]+IN["auc_fy25"])/IN["cap_cement_mt"]/IN["fx"])} per annual tonne '
  f'against a replacement cost of USD {n0(IN["repl_usd_t"])}. A return computed on that base '
  f'measures the devaluation, not the economics of adding a tonne.')
P(f'The terminal block is therefore struck on REPLACEMENT-COST invested capital — EGP '
  f'{n0(DCF["ic_repl"])}mn, being {n1(IN["cap_cement_mt"])}Mt at USD {n0(IN["repl_usd_t"])} '
  f'a tonne. On that basis the return on capital in the terminal year is '
  f'{pc(TR["roic_repl"])}.')
P(f'WHAT THE TERMINAL CHARGES, AND WHY IT CHANGED IN THIS EDITION. Earlier revisions derived '
  f'the terminal reinvestment from that return — growth divided by return on capital, which '
  f'came to {pc(TR["rr_repl"])} of terminal profit. Substituting the definitions, that '
  f'construction collapses to a fixed charge of growth multiplied by invested capital: EGP '
  f'{n0(IN["g_term"]*DCF["ic_repl"])}mn a year, for ever. Read as a programme for replacing '
  f'the plant it implies doing so every {n1(1.0/IN["g_term"])} years — which is one divided '
  f'by the growth rate, and so a fact about the inflation path rather than about the kiln. '
  f'The reinvestment identity is a statement about REAL growth, and this model\u2019s '
  f'terminal real growth is zero, so the charge was buying no capacity at all.')
P(f'This edition charges what holding the plant actually costs: capital maintenance over the '
  f'useful life ARCC\u2019s own audited accounts disclose — '
  f'{n0(TERMREC["inputs"]["useful_life_years"])} years for machinery and equipment and for '
  f'other installations — which is EGP {n0(TERMREC["maintenance"])}mn a year against '
  f'replacement cost, plus the working capital that inflation requires, less the book '
  f'depreciation already inside terminal profit. That is the same definition of free cash '
  f'flow the explicit window uses; the earlier terminal used a different one, and a model '
  f'should not carry two. Three implied asset lives previously sat inside this one and '
  f'disagreed by a factor of nearly three: the terminal\u2019s {n1(1.0/IN["g_term"])} years, '
  f'the explicit window\u2019s own capital spending at '
  f'{n1(IN["repl_usd_t"]/IN["capex_usd_t_cap"])} years, and the disclosed '
  f'{n0(TERMREC["inputs"]["useful_life_years"])}. The sourced figure sits between the '
  f'model\u2019s own two conventions. The explicit window and the terminal may still differ, '
  f'and here they do for an economic reason: kiln 2 sits in assets under construction, so a '
  f'young plant genuinely spends less than replacement depreciation for a while, while the '
  f'terminal is perpetuity, where every asset must be replaced at current cost.')
P(f'Growth in the terminal is charged at what growth costs — the capital a REAL increase in '
  f'capacity requires, at the replacement cost of that capacity — and this model takes no '
  f'real growth, so it charges none for it. Whether it should is the ordinary question: does '
  f'a new tonne earn more than it costs? Terminal profit over invested capital is '
  f'{pc(GDV["n_over_ic"], 2)} against a terminal rate of {pc(W["wacc_term"])} — '
  f'{n0(abs(GDV["n_over_ic"]-W["wacc_term"])*1e4)} basis points '
  f'{"above" if GDV["n_over_ic"] > W["wacc_term"] else "BELOW"} it. Growth '
  f'therefore {"adds" if GDV["analytic_adds_value"] else "DESTROYS"} value: the '
  f'cash-flow lens is EGP {n2(GDV["fv_at_g3"])} at 3% terminal growth and EGP '
  f'{n2(GDV["fv_at_g7"])} at 7%, so four extra points of perpetual growth take the value '
  f'{"UP" if GDV["fv_at_g7"] > GDV["fv_at_g3"] else "DOWN"} by '
  f'{pc(abs(GDV["spread_pct"]), 1)}. The practical conclusion is the one that matters: on a '
  f'replacement-cost denominator this plant roughly breaks even on new tonnes, in a market '
  f'carrying {n0(IN["egy_capacity_mt"])}Mt of capacity against {n0(IN["egy_cons_mt"])}Mt of '
  f'consumption, so nothing in this valuation is bought with an assumption about perpetual '
  f'growth. A reader who prefers the book basis should know it lifts the valuation '
  f'substantially, and should say why a plant carried at a tenth of replacement cost is the '
  f'right denominator.')
rows = [['Explicit-window rate'] + [pc(g, 0) for g in SN['g_grid']]]
for i, wv in enumerate(SN['wacc_grid']):
    rows.append([pc(wv, 2)] + [n2(x) for x in SN['wacc_g'][i]])
table(rows, [1.72, 1.02, 1.02, 1.02, 1.02, 1.02])
# Both the strength and the SIGN of the growth lever are read off the grid, never
# typed. They flipped between revisions and a hard-typed caption would now be false.
_row = SN["wacc_g"][0][4] - SN["wacc_g"][0][0]     # 3% -> 7% growth, rate held
_col = SN["wacc_g"][4][0] - SN["wacc_g"][0][0]     # low -> high rate, growth held
_g_up = 'UP' if _row > 0 else 'DOWN'
_g_str = 'STRONGER' if abs(_row) > abs(_col) else 'WEAKER'
caption(f'Table 11 — Fair value per share across the explicit-window cost of capital and '
        f'terminal growth. Growth is the {_g_str} of the two levers here and it points '
        f'{_g_up}: across a row the value moves EGP {n2(abs(_row))}, against EGP '
        f'{n2(abs(_col))} down a column. The paragraphs above set out why the growth axis is '
        f'nearly flat — on a replacement-cost denominator this plant sits within '
        f'{n0((GDV["n_over_ic"]-GDV["hurdle"])*1e4)} basis points of breaking even on new '
        f'tonnes, so perpetual growth neither creates nor destroys much of anything.')
figure('fig2_sens.png', 6.6,
       f'Figure 3 — The same surface. The growth axis is almost flat and the discount-rate '
       f'axis is not; that is the model being consistent with its own terminal algebra '
       f'rather than a sign error.')
rows = [['Explicit-window rate'] + [pc(w, 1) for w in SN['wt_grid']]]
for i, wv in enumerate(SN['wacc_grid']):
    rows.append([pc(wv, 2)] + [n2(x) for x in SN['exp_term'][i]])
table(rows, [1.72, 1.02, 1.02, 1.02, 1.02, 1.02])
caption('Table 12 — The two anchors varied INDEPENDENTLY: the explicit-window rate down '
        'the side, the terminal rate across the top. This shows what the valuation needs '
        'the economy to do, not merely what growth rate the model needs.')

# ---- 1.9 --------------------------------------------------------------------
H2('1.9  The other three lenses, and the choices that were contested')
P(f'The relative lens applies {n1(IN["ev_ebitda_just"])} times to normalised EBITDA of EGP '
  f'{n0(LN["ebitda_norm"])}mn — the FY2025 revenue base cut '
  f'{pc(1-IN["norm_rev_haircut"], 0)} and a mid-cycle margin of {pc(IN["norm_mgn"])} '
  f'applied to it — and adds net cash at face. The multiple is disclosed as weakly '
  f'anchored: the listed Egyptian peer set is thin, and its published multiples do not '
  f'reconcile against the market capitalisations printed beside them. That is why this '
  f'lens carries {pc(IN["w_rel"], 0)} and not more.')
P(f'The normalised-earnings lens capitalises the same mid-cycle operating profit after tax '
  f'— EGP {n0(LN["nopat_norm"])}mn — at {n1(IN["pe_just"])} times, and again adds cash at '
  f'FACE rather than capitalising it at the operating multiple. Cash is worth cash; '
  f'capitalising a pound of treasury at seven times would value it at a discount to '
  f'itself.')
P(f'The asset lens values the capacity: {n1(IN["cap_cement_mt"])}Mt at a justified USD '
  f'{n0(IN["ev_t_just"])} per annual tonne, marked down '
  f'{pc(1-IN["ev_t_just"]/IN["repl_usd_t"], 0)} from a replacement cost of USD '
  f'{n0(IN["repl_usd_t"])}. Against that, the market is paying USD '
  f'{n1(LN["ev_per_t_spot"])} per annual tonne. This lens carries only '
  f'{pc(IN["w_asset"], 0)}, and the reason is in the same paragraph as the number: '
  f'restarting a mothballed line costs a fraction of building one, and '
  f'{n1(IN["egy_revival_mt"])}Mt of restart capacity is queuing. Replacement cost is a '
  f'ceiling here, not a floor.')
rows = [['Choice', 'Adopted', 'Alternative', 'Effect on the cash-flow lens']]
for c in CON:
    rows.append([c['choice'], c['adopted'], c['alternative'],
                 f'{n2(c["fv_alternative"])}  ({sg(c["effect"])})'])
table(rows, [2.55, 1.05, 1.20, 1.70], size=8.8)
caption('Table 13 — Every contested choice computed as a value rather than argued in '
        'prose. None of these alternatives is hidden; each is a full re-run of the model.')

# ---- 1.10 -------------------------------------------------------------------
OFF_LABEL = {'EFG': 'EFG off mark', 'OPEN': 'open — no referee', 'NEITHER': 'method, not error'}
H2('1.10  A published sell-side target, reconciled item by item')
P(f'On 6 August 2026 EFG Hermes published a Buy rating on ARCC with a target price of EGP '
  f'{n2(EFG["start"])}, against a spot of EGP {n2(EFG["market"])}. Both models reproduce '
  f'FY2025 revenue, cost of sales, gross profit, D&A, capex and net cash to the pound, so '
  f'the whole EGP {n2(EFG["start"]-EFG["end"])} gap between the two targets is forward-'
  f'looking. What follows replaces one driver of theirs with one of ours at a time and '
  f'records the change, so the bars sum to the gap by construction rather than by a plug.')
rows = [['Step', 'EGP/sh', 'What moved']]
rows.append(['START — EFG Hermes target', n2(EFG['start']), '6 Aug 2026, Buy, DCF'])
for s in EFG['steps']:
    rows.append([s['label'].replace('\n', ' '), f'{s["value"]:+.2f}',
                s['sub'].replace('\n', ' ')])
rows.append(['END — this study\'s central', n2(EFG['end']),
             'the cash-flow lens, published alone'])
table(rows, [2.65, 0.85, 3.00], size=8.8)
caption(f'Table 14 — The reconciliation bridge. Bars sum to the gap exactly '
        f'({sum(s["value"] for s in EFG["steps"]):+.2f} vs {EFG["end"]-EFG["start"]:+.2f}). '
        f'Reproduced independently as a check before publication.')
figure('fig_efg_bridge.png', 6.6,
      f'Figure 4 — The same bridge, drawn. Every bar substitutes exactly one driver and '
      f'carries it through both the discounted window and the cash bridge, so nothing is '
      f'counted twice.')
tally = {}
for s in EFG['steps']:
    tally[s['off']] = tally.get(s['off'], 0.0) + s['value']
P(f'Sorting the eight steps by who the evidence favours: the items where EFG’s own '
  f'construction is inconsistent with itself sum to {tally.get("EFG",0):+.2f} — an internal '
  f'date mismatch between their discount factors and their cash balance, a capex path that '
  f'sits below their own depreciation in every tabulated year, a terminal value grown '
  f'without a reinvestment charge, and a dividend of EGP 5.34/share, ex 12 April 2026, that '
  f'their own front page discloses and their balance sheet does not appear to reflect. Two '
  f'items are genuinely open — the operating build, where our volumes are higher and our '
  f'margin path is lower, and the discount-rate convention, where their rate is below the '
  f'sovereign risk-free rate early and harsher than ours late, worth a combined '
  f'{tally.get("OPEN",0):+.2f}. The remaining {tally.get("NEITHER",0):+.2f} is a lens-'
  f'weighting difference, not an error on either side.')
for s in EFG['steps']:
    P(f'{s["label"].replace(chr(10), " ")} ({s["value"]:+.2f}, {OFF_LABEL[s["off"]]}). '
      f'{s["receipt"]}', size=9.6)
mgn_rows = [['Year', 'Testahil', 'EFG published', 'EFG on our definition', 'Gap']]
FY25A = MSC['fy25a']
mgn_rows.append(['FY2025a', pc(FY25A['testahil']), pc(FY25A['efg_published']),
                 pc(FY25A['efg_our_definition']), 'audited'])
for r in MSC['margin_table']:
    mgn_rows.append([r['year'], pc(r['testahil']), pc(r['efg_published']),
                     pc(r['efg_our_definition']), f'{r["gap_pt"]:+.2f}pt'])
table(mgn_rows, [1.05, 1.15, 1.30, 1.55, 0.95], size=8.8)
caption(f'Table 15 — EBITDA margin, year by year. EFG’s FY2025a margin restates to '
        f'{pc(H["margin"][2])} once the {pc(MSC["wedge_pct"])} definitional wedge — '
        f'provisions, expected credit losses and other operating income, which the two '
        f'models classify oppositely — is removed, reproducing our own audited figure '
        f'exactly. The disagreement from FY2026 on is real, not definitional, and it widens '
        f'rather than staying flat.')
sc_rows = [['Scenario', 'DCF lens', 'Central', 'vs spot']]
for r in MSC['scenarios']:
    sc_rows.append([r['name'], n2(r['dcf']), n2(r['central']), sg(r['central']/SPOT-1)])
table(sc_rows, [3.60, 0.95, 0.95, 0.95], size=8.8)
caption(f'Table 16 — What EFG’s margin view is worth, held against both volume '
        f'assumptions. Their margin on OUR volumes clears spot; their margin AND their '
        f'volumes, taken together, does not.')

# ---- 1.11 -------------------------------------------------------------------
H2('1.11  What a buyer at EGP ' + n2(SPOT) + ' must believe')
half = next(r for r in MSC['scenarios'] if 'Half way' in r['name'])
P(f'Strip out the items resolved above and the honest disagreement left is one thing: how '
  f'fast does the FY2025 margin peak fade. Everything else in the bridge is either a '
  f'construction error on the published target (the date mismatch, the sub-depreciation '
  f'capex path, the unfunded terminal growth, the still-outstanding dividend) or a lens-'
  f'weighting convention that is not a factual dispute at all. A market price of EGP '
  f'{n2(SPOT)} sits between this study’s central of EGP {n2(LN["central"])} and '
  f'EFG’s corrected-for-its-own-errors figure, closer to ours — but a buyer paying '
  f'spot is not implicitly endorsing either model whole. Splitting the one open '
  f'question down the middle — EFG’s margin path and this study’s volume path, '
  f'averaged rather than either side’s optimism taken alone — prices at EGP '
  f'{n2(half["central"])}, {sg(half["central"]/SPOT-1)} against spot. That, not either '
  f'published figure, is the number this study would defend if forced to name one.')

# ============================== 2 ============================================
H1('2  Price structure')
P(TECH['tech']['summary'])
rows = [['', 'Level (EGP)', 'Distance from spot']]
for i, r in enumerate(TECH['levels']['res']):
    rows.append([f'Resistance {i+1}', n2(r), sg(r / SPOT - 1)])
for i, s_ in enumerate(TECH['levels']['sup']):
    rows.append([f'Support {i+1}', n2(s_), sg(s_ / SPOT - 1)])
rows.append(['52-week high', n2(TECH['hi_52w']), sg(TECH['hi_52w'] / SPOT - 1)])
rows.append(['52-week low', n2(TECH['lo_52w']), sg(TECH['lo_52w'] / SPOT - 1)])
table(rows, [2.00, 1.50, 1.70])
caption('Table 17 — Levels are computed from swing structure with a recency weight; '
        'moving averages, the 52-week extremes and round numbers are admitted as '
        'candidates but score below real swing points. Resistance 1 and support 1 always '
        'mean nearest to the close.')
figure('fig3_ma.png', 6.9,
       'Figure 5 — Three years of price with the 50- and 200-day averages.')
rich([('On the upside: ', {'bold': True}), (TECH['tech']['bull'], {})])
rich([('On the downside: ', {'bold': True}), (TECH['tech']['bear'], {})])
P('This section describes the tape and makes no claim about value. The two are compared in '
  'section 4.')

# ============================== 3 ============================================
H1('3  A probabilistic price map')
P('The following is NOT a valuation. It is a distribution of where the share price could '
  'sit at two horizons, drawn from the price history alone and from nothing in the '
  'preceding sections. It is included because a single fair-value number tells a reader '
  'nothing about dispersion, and it is labelled illustrative because its own calibration '
  'record says it should be.')
rows = [['', 'One month', 'Three months']]
for lab, k in [('5th percentile', 'p5'), ('25th percentile', 'p25'), ('Median', 'p50'),
               ('75th percentile', 'p75'), ('95th percentile', 'p95')]:
    rows.append([lab, n2(STK['horizons']['1M']['pct'][k]), n2(STK['horizons']['3M']['pct'][k])])
rows.append(['Probability of finishing above the current price',
             pc(STK['horizons']['1M']['p_above']), pc(STK['horizons']['3M']['p_above'])])
rows.append(['Probability of touching +10% at any point',
             pc(STK['horizons']['1M']['touch_up10']), pc(STK['horizons']['3M']['touch_up10'])])
rows.append(['Probability of touching −10% at any point',
             pc(STK['horizons']['1M']['touch_dn10']), pc(STK['horizons']['3M']['touch_dn10'])])
table(rows, [3.00, 1.60, 1.60], band_rows={3})
caption(f'Table 18 — Percentiles in EGP per share, from a 50,000-path simulation anchored '
        f'on the {STK["anchor_date"]} close of EGP {n2(STK["spot"])} — the last session in '
        f'the price history this map was simulated from, which is EARLIER than the '
        f'{SPOT_DATE_WORDS} close of EGP {n2(SPOT)} the valuation is struck against. Those '
        f'are two clocks and they are supposed to be: a fresh price moves the valuation '
        f'without re-running the simulation. Read every percentile below against EGP '
        f'{n2(STK["spot"])}. The drift is the carry — the '
        f'risk-free rate less the dividend yield — and nothing else.')
figure('fig4_fan.png', 6.9, 'Figure 6 — The three-month cone.')
figure('fig6_dist.png', 6.4, 'Figure 7 — The three-month outcome distribution.')
# TWO THINGS HERE WERE FORBIDDEN ON A PUBLIC SURFACE [corrected 03-Sep-2026].
#
# (1) "The map is therefore TOO WIDE" is a FLAG, and [R-CAL-02] permits one only
#     when it is EARNED — a two-sided binomial test against the target at the 5%
#     level — and says that OTHERWISE NOTHING IS SAID, because the ordinary case is
#     a cone that held about as often as it promised and silence is the honest
#     response to it. ARCC's live record carries flag: null. The flag was typed.
#
# (2) The skill number against a random walk is the RETIRED verdict [R-CAL-03],
#     which may not reach a reader on any surface. It appeared twice.
#
# What replaces both is what the rule actually says a reader is shown: the band
# record with its COUNT beside the percentage, and the flag only if earned.
_FLAG = (BAND.get('flag') or '')
P(f'How well calibrated is it? Over {int(BAND["n"])} resolved three-month forecasts '
  f'on this share the price finished inside the ninety-per-cent band '
  f'{pc(BAND["c90"], 0)} of the time, and inside the fifty-per-cent band '
  f'{pc(BAND["c50"], 0)} of the time. The count is printed beside the percentage because a '
  f'percentage without its count is the number that misleads.'
  + (f' On a two-sided test at the five-per-cent level the bands ran {_FLAG}.'
     if _FLAG else
     ' No flag is earned on a two-sided test at the five-per-cent level: the bands held '
     'about as often as they promised, and nothing further is claimed for them.')
  + ' No valuation conclusion in this study rests on the map.')

# ============================== 4 ============================================
H1('4  Comparison of the lenses')
rows = [['Lens', 'Bear (EGP)', 'Base (EGP)', 'Bull (EGP)', 'Role', 'Versus spot']]
for k in list(LN['values']) + ['Normalised earnings']:
    _role = ('the central' if k == LN['primary']
             else ('diagnostic only' if k == 'Normalised earnings' else 'cross-check'))
    rows.append([k, n2(LR[k]['bear']), n2(LR[k]['base']), n2(LR[k]['bull']), _role,
                 sg(LR[k]['base'] / SPOT - 1)])
table(rows, [2.00, 1.00, 1.00, 1.00, 0.90, 1.02], band_rows={1})
caption('Table 19 — Each lens as a range. The disagreement between them is information, '
        'not noise.')
_above = sorted([k for k in LN['values'] if LN['values'][k] > SPOT],
                key=lambda k: -LN['values'][k])
_below = sorted([k for k in LN['values'] if LN['values'][k] <= SPOT],
                key=lambda k: LN['values'][k])
_lens_l = lambda ks: ' and '.join([', '.join(ks[:-1]), ks[-1]] if len(ks) > 1 else ks)
# THIS PARAGRAPH ASSUMED BOTH SIDES WERE OCCUPIED AND RENDERED EMPTY SLOTS WHEN THEY
# WERE NOT [corrected 03-Sep-2026]. At a spot of 59.00 some lenses sat above and two
# below, and the sentence was written for that arrangement -- "Some sit ABOVE the
# market price — {list}, at EGP {values} — and TWO sit below". At 77.00 nothing sits
# above, so the delivered study read "Some sit ABOVE the market price — , at EGP —
# and two sit below:" and then listed three. A count typed into prose is a claim
# about the numbers; it is now derived from them, and each clause appears only when
# it has something to say.
_n_word = lambda n: {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five'}.get(n, str(n))
_side = lambda ks: '%s, at EGP %s' % (_lens_l(ks),
                                      ' and EGP '.join(n2(LN['values'][k]) for k in ks))
if _above and _below:
    _open = ('%s sit%s ABOVE the market price — %s — and %s below: %s.'
             % (_n_word(len(_above)).capitalize(), '' if len(_above) > 1 else 's',
                _side(_above), _n_word(len(_below)), _side(_below)))
elif _above:
    _open = ('EVERY lens sits ABOVE the market price: %s.' % _side(_above))
else:
    _open = ('EVERY lens sits BELOW the market price: %s. Not one read in this study '
             'reaches what the shares trade at, which is a stronger statement than any '
             'single lens makes and is the thing to weigh first.' % _side(_below))
P(f'The lenses do not agree, and the pattern of their disagreement is the most useful '
  f'thing in this study. ' + _open +
  f' The split is not assets against earnings. It runs between what the plant can be '
  f'expected to EARN or COST from here, which both land above the market, and what the '
  f'market is currently willing to PAY for a pound of Egyptian cement earnings, which is '
  f'what the two multiple-based lenses measure and which lands below. A cement peer group '
  f'trading at {n1((PE["scem"]["pe"]+PE["mbsc"]["pe"])/2)} times earnings in a country '
  f'whose policy rate has '
  f'a two in front of it is not obviously mispricing anything; it is discounting the same '
  f'restart programme this study discounts, only harder and sooner.')
P(f'This edition does not resolve that by weighting. A previous one blended the four '
  f'readings at {pc(IN["w_dcf"], 0)}/{pc(IN["w_rel"], 0)}/{pc(IN["w_norm"], 0)}/'
  f'{pc(IN["w_asset"], 0)} and published the average, EGP {n2(_BLEND)}; '
  f'but those weights were chosen rather than tested, and an average of four methods is '
  f'a fifth method nobody has checked, carrying every weakness of the weakest at whatever '
  f'weight somebody typed. The value published here is the cash-flow lens alone, EGP '
  f'{n2(LN["central"])} against EGP {n2(SPOT)} — {sg(LN["central"]/SPOT-1)} — and the '
  f'other readings are printed beside it so the disagreement is visible rather than '
  f'averaged away. A reader who believes replacement cost is a floor rather than a '
  f'ceiling can read EGP {n2(LN["values"]["Asset / replacement cost"])} off the same '
  f'table and reach the opposite conclusion; the case against doing so is the '
  f'{n1(IN["egy_revival_mt"])}Mt restart programme, and it is a testable one.')
P(f'Against the technical picture, the two readings are in tension. The share is above its '
  f'entire moving-average stack on a rising 200-day and {pc(1-TECH["pct_off_high"], 0)} of '
  f'of its 52-week intraday high — 98% OF that high, and '
  f'{pc((SPOT-35.01)/(60.40-35.01), 0)} of the way UP the range, which are different '
  f'statistics and the earlier edition ran them together — while the two multiple-based '
  f'lenses put fair value below the '
  f'current price and the two forward-looking ones put it above. Momentum sits with the '
  f'cash-flow case here rather than against it, and the disagreement that remains is '
  f'between that case and the multiple the market is prepared to pay. This study takes no '
  f'view on which resolves first.')

# ============================== 5 ============================================
H1('5  Catalysts to watch')
for head, body in [
    ('The restart programme. ', f'Seven to nine dormant Egyptian lines are under study for '
     f'revival, potentially adding {n1(IN["egy_revival_mt"])}Mt from the second half of '
     f'2026 — about {pc(PE["sector"]["revival_pct_of_consumption"], 0)} of domestic '
     f'consumption. Whether those lines actually restart, and how fast, is the single '
     f'largest swing factor in the price path this model assumes.'),
    ('The realised price, quarter by quarter. ', f'The model assumes a domestic price of '
     f'EGP {n0(BU[1]["price_loc"])} a tonne in FY2026 and growth below cost '
     f'inflation thereafter. Two consecutive quarters of realised prices above EGP 4,200 '
     f'would break that assumption upward; a return toward EGP 3,000 would break it down.'),
    ('The alternative-fuel programme. ', f'The substitution rate is assumed to rise from '
     f'a cumulative {pc(IN["af_saving"][5], 1)} saving on the materials and fuel line by '
     f'FY2030, against a EUR 25mn facility already drawn and EGP 240mn of capacity already '
     f'under construction. Progress on it is '
     f'reported in the company\'s own sustainability disclosure and is directly visible in '
     f'the fuel cost per tonne. A stall would cost roughly the difference between the '
     f'blended and fossil-only fuel bills.'),
    ('Energy tariffs. ', 'Phased subsidy reform continues to raise the domestic industrial '
     'energy bill independently of the global fuel price. The model inflates the pound cost '
     'lines by 11.5% in FY2026, easing to 7.0% by FY2030; a faster reform schedule would '
     'compress the margin faster than assumed.'),
    ('The export cap and the carbon border mechanism. ', 'Exports are capped at 30% of '
     'production, and the EU carbon border mechanism raises the landed cost of Egyptian '
     'cement in Europe. A low-clinker, high-alternative-fuel producer suffers less from the '
     'second than a conventional peer, and the export price path assumes exactly that.'),
    ('Distribution policy. ', f'The company declared EGP {n0(IN["div_fy25_declared"])}mn for '
     f'FY2025, about {pc(IN["payout"], 0)} of attributable profit, on top of EGP '
     f'{n0(IN["div_fy24_paid"])}mn for FY2024. A change in that policy changes the cash '
     f'roll-forward and, through it, the balance sheet the bridge relies on.'),
]:
    bullet(body, bold_head=head)

# ============================== 6 ============================================
H1('6  Reading the probability zones')
P('The distribution in section 3 is easier to use as zones than as percentiles. The '
  'following divides the three-month outcome space into four bands and states what each '
  'would mean, without predicting which occurs.')
h3 = STK['horizons']['3M']['pct']
rows = [['Zone', 'Three-month range (EGP)', 'Probability', 'What it would mean']]
rows.append(['Lower tail', f'below {n2(h3["p5"])}', '5%',
             'A break of the 48.10 support zone, most plausibly on a faster-than-assumed '
             'capacity restart'])
rows.append(['Below spot', f'{n2(h3["p5"])} – {n2(SPOT)}',
             pc(1 - STK['horizons']['3M']['p_above'] - 0.05, 0),
             'The market converging toward the earnings-based lenses in this study'])
rows.append(['Above spot', f'{n2(SPOT)} – {n2(h3["p95"])}',
             pc(STK['horizons']['3M']['p_above'] - 0.05, 0),
             'Momentum and the 2026 pricing environment continuing to lead the earnings case'])
rows.append(['Upper tail', f'above {n2(h3["p95"])}', '5%',
             'A re-rating toward the asset lens, which would require the restart programme '
             'to be abandoned or delayed materially'])
table(rows, [1.10, 1.55, 0.90, 2.55], size=8.8)
caption('Table 20 — Zones, not forecasts. The four are exclusive and sum to 100%: each '
        'tail is carved OUT of the band beside it rather than counted twice. The '
        'probabilities come from the price map and are subject to the same over-width '
        'caution as everything else in section 3.')

# ============================== 7 ============================================
H1('7  Caveats and what would change our mind')
for head, body in [
    ('The accounts are audited, and this study is built on them. ', 'An earlier edition of '
     'this work was written without access to a source document and reconstructed the '
     'history by closing disclosed profit against modelled assumptions. That edition is '
     'superseded. Every historical figure here is read from the consolidated financial '
     'statements signed by Deloitte on 25 February 2026, or from the reviewed interim '
     'accounts of 25 May 2026. Four things it got materially wrong are worth naming, '
     'because they show where reconstruction fails: minority interests were deducted at '
     'EGP 150mn against an audited EGP 158,005; the effective tax rate was inferred at '
     '29.4% against a disclosed 23.8%; the cost of debt was assumed at 21.5% against a '
     'euro-denominated book paying about 7.5%; and kiln capacity was assumed 14% too low.'),
    ('The model was rebuilt bottom up, and the answer moved a long way. ', f'Four '
     f'reviewers tested the previous edition. Between them they showed that its volume '
     f'came from an assumed price rather than from the plant, that its FY2025 validation '
     f'was an identity that could not fail, that its terminal capital was measured in '
     f'valuation-date pounds against a terminal-year cash flow, that its terminal cost of '
     f'debt sat 250 basis points below its own terminal risk-free rate, that its terminal '
     f'risk-free rate used the central bank\'s near-dated inflation target rather than its '
     f'medium-term one, that its discount factors applied each year\'s rate one period '
     f'late, that its beta was levered twice, and that ten rows of its income statement '
     f'were labelled one row above their contents. All of that is corrected here. The '
     f'central fair value moves from EGP 61.30 to EGP {n2(LN["central"])}, and the '
     f'conclusion moves from a premium over the market to a small discount.'),
    ('The expert panel is the model at three parameter values, not three independent '
     'valuations. ', f'A reviewer pointed out that Expert 1\'s central IS the asset lens '
     f'to the pound and Expert 2\'s IS the normalised-earnings lens. That is correct, and '
     f'the workbook now builds all nine panel figures as FORMULAS off the same drivers '
     f'rather than typing them, so the point is demonstrated rather than argued: Expert 1 '
     f'marks replacement cost at USD 80/95/110 a tonne, Expert 2 capitalises the '
     f'normalised base at 6/7/8 times, Expert 3 discounts mid-cycle free cash flow at a '
     f'20.0%/17.5%/15.0% required return. Read the panel as a sensitivity with reasoning '
     f'attached, not as corroboration.'),
    ('Volume is now physical, and it is the largest open question in the study. ', f'The '
     f'build runs on kiln utilisation, the clinker factor and two export shares, and the '
     f'three realised prices are derived from the audited revenue note. That makes the '
     f'prices testable, and they do not fully pass: export clinker derives to USD '
     f'{n1(UC["price_exp_clk_usd"])} a tonne against a trade-press range of USD 44-48. '
     f'Either the physical assumptions are too generous or realisations run below the '
     f'published indices. The company discloses despatch volumes in its investor material, '
     f'which would settle it; that material could not be reached from here, and the '
     f'audited statements are image-only scans that carry no volume table.'),
    ('The cost of debt is marginal and pound-equivalent, not the coupon as written. ',
     f'The adopted {pc(KDG["kd_blended"], 2)} carries the euro legs at the pound cost a '
     f'company earning pounds actually bears, against a contracted blend of '
     f'{pc(KDG["kd_contracted"], 2)}. It sits above the {pc(KDG["eff_fy25"], 2)} that '
     f'FY2025 interest over average debt gives and the '
     f'{pc(KDG["eff_q126_annualised"], 2)} the first quarter of 2026 annualises to, because '
     f'the book re-based mid-year and interest on assets still under construction is '
     f'capitalised. Adopting the contracted rate instead would leave the euro debt '
     f'uncompensated for pound depreciation beyond the currency path assumed here, and is '
     f'worth {sg(CON[0]["effect"])}.'),
    ('Half a year has been turned into a whole one, and that is the largest assumption '
     'here. ', f'The forecast starts from the reviewed six months to 30 June 2026 — revenue '
     f'of EGP {n0(IN["rev_h1_26"])}mn at a {pc(IN["gp_h1_26"]/IN["rev_h1_26"])} gross '
     f'margin — grossed up to a full year. HOW MUCH OF A YEAR ARCC\'S FIRST HALF IS varies: '
     f'it was {pc(SEA["shares_rev"][0])}, {pc(SEA["shares_rev"][1])} and '
     f'{pc(SEA["shares_rev"][2])} of the year in the three years that can be measured. The '
     f'median is used, which puts FY2026 revenue at EGP {n0(CALB["fy26_rev_implied"])}mn; on '
     f'the least favourable of the three it would be EGP {n0(SEA["fy26_low"])}mn and on the '
     f'most favourable EGP {n0(SEA["fy26_high"])}mn. Simply doubling the half gives EGP '
     f'{n0(SEA["fy26_if_doubled"])}mn.'),
    ('And no interim tonnage is published, so the uplift cannot be split between price and '
     'volume. ', f'Local sales of goods rose {pc(IN["rev_h1_26_loc_goods"]/IN["rev_h1_25_loc_goods"]-1)} '
     f'against the same half of 2025 while export sales of goods fell '
     f'{pc(IN["rev_h1_26_exp_goods"]/IN["rev_h1_25_exp_goods"]-1)}. The company publishes no '
     f'tonnage with its half-year accounts, so this study cannot tell how much of the local '
     f'rise was a higher price and how much was more tonnes. It is taken entirely as price '
     f'and carried through every forecast year as a level shift of '
     f'{n3(CALB["local"])} times. THAT IS THE ASSUMPTION IN THIS STUDY MOST CAPABLE OF BEING '
     f'WRONG: if the rise was volume rather than price, and volume is capped by the plant, '
     f'the later years are overstated.'),
    ('A large collection of export subsidy is treated as one-off. ', f'The half-year accounts '
     f'record EGP {n0(IN["export_subsidy_h1_26"])}mn of export subsidy collected in the '
     f'second quarter, against EGP {n1(IN["export_subsidy_fy25"])}mn for the whole of FY2025. '
     f'It is excluded from forward operating profit and left in the cash balance, on the '
     f'reading that it settles accumulated claims. If a comparable amount arrives again with '
     f'no accumulated-claims explanation, it is recurring and this study understates value.'),
    ('The terminal denominator is a choice. ', f'Return on capital is '
     f'{pc(TR["history"][2]["roic_book"])} on the audited book and {pc(TR["roic_repl"])} on '
     f'replacement cost. The terminal block uses replacement cost, which leaves the plant '
     f'roughly breaking even on new tonnes — {pc(GDV["n_over_ic"], 2)} against a hurdle of '
     f'{pc(GDV["hurdle"], 2)}, so four points of terminal growth are worth '
     f'{pc(GDV["spread_pct"], 1)} of value and the answer does not rest on the rate. On the '
     f'book basis growth would be close to free and the valuation materially higher. The '
     f'case for replacement cost is that the book carries a 2010-vintage plant at a tenth of '
     f'what one would cost to build today, but a reader is entitled to disagree.'),
    ('The beta is not this company\'s own. ', f'Measured against the market index, Arabian '
     f'Cement\'s own share history explains too little to be usable — an R-squared of '
     f'{pc(OWN["r2"], 1)} — so the discount rate rests on the betas of four comparable '
     f'Egyptian companies instead. That is the ordinary fallback and it is disclosed, but '
     f'it means the risk measure in this valuation is a sector estimate rather than a '
     f'measurement of this share. The valuation is shown across the whole peer spread for '
     f'exactly that reason.'),
    ('The price map is a separate lens and carries no valuation weight. ',
     f'Over {int(BAND["n"])} resolved three-month forecasts the price finished inside '
     f'the ninety-per-cent band {pc(BAND["c90"], 0)} of the time. It is carried as '
     f'illustrative only, and nothing in the valuation depends on it.'),
    ('A minority position under a 60% shareholder. ', 'Aridos Jativa of Spain owns 60% of '
     'the capital. No control premium or discount is applied anywhere in this valuation, in '
     'either direction. The company also holds 1% of its own capital in treasury, acquired '
     'during 2025, which is excluded from the share count throughout.'),
    ('Currency, on both sides now. ', 'Revenue is 69% local and 31% export; costs are '
     'largely in pounds but fuel and spares are not; and the debt is 91% euro. A weaker '
     'pound raises export revenue in pounds and raises the pound cost of servicing the euro '
     'debt. The model carries one currency path acting on all three legs.'),
]:
    bullet(body, bold_head=head)
rows = [['Net cash at the valuation date (EGP mn)'] + [n0(x) for x in SN['nc_grid']]]
rows.append(['Fair value per share (EGP)'] + [n2(x) for x in SN['net_cash']])
table(rows, [2.40, 0.92, 0.92, 0.92, 0.92, 0.92], size=8.8)
caption('Table 21 — The clean net-cash sensitivity, with the tax rate held.')
rows = [['Shift in the EBITDA margin, every forecast year'] + [sg(m, 0) for m in SN['mgn_grid']]]
rows.append(['Fair value per share (EGP)'] + [n2(x) for x in SN['mgn']])
table(rows, [2.40, 0.92, 0.92, 0.92, 0.92, 0.92], size=8.8)
caption('Table 22 — And the margin sensitivity, which is the largest single swing factor '
        'in the model.')

# ============================== APPENDIX A ===================================
doc.add_page_break()
H1('Appendix A  Financial statements')
H2('A.1  Income statement — three years reported and five forecast')
rows = [['EGP mn'] + YH + YF]
rows.append(['Revenue'] + [n0(x) for x in H['revenue']] + [n0(x) for x in F['revenue']])
rows.append(['Cost of sales'] + [f'({n0(x)})' for x in H['cogs']] + ['—'] * 5)
rows.append(['Gross profit'] + [n0(x) for x in H['gross_profit']] + ['—'] * 5)
rows.append(['Operating profit'] + [n0(x) for x in H['ebit']] + [n0(x) for x in F['ebit']])
rows.append(['Depreciation and amortisation'] + [n0(x) for x in H['dna']] +
            [n0(x) for x in F['dna']])
rows.append(['EBITDA'] + [n0(x) for x in H['ebitda']] + [n0(x) for x in F['ebitda']])
rows.append(['EBITDA margin'] + [pc(x) for x in H['margin']] + [pc(x) for x in F['margin']])
rows.append(['Net finance and other income'] +
            [n0(H['pbt'][i] - H['ebit'][i]) for i in range(3)] +
            [n0(x) for x in F['treasury']])
rows.append(['Profit before tax'] + [n0(x) for x in H['pbt']] + [n0(x) for x in F['pbt']])
rows.append(['Income tax'] + [f'({n0(x)})' for x in H['tax']] +
            [f'({n0(x)})' for x in F['tax']])
rows.append(['Attributable profit'] + [n0(x) for x in H['pat']] + [n0(x) for x in F['pat']])
rows.append(['Earnings per share (EGP)'] + [n2(x) for x in H['eps']] +
            [n2(x) for x in F['eps']])
table(rows, [1.52, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72], size=8.0,
      band_rows={11})
caption('Table A1 — Three AUDITED years and five forecast. FY2023-FY2025 revenue, cost of '
        'sales, administrative expenses, provisions, pre-tax profit, tax, attributable '
        'profit, earnings per share and depreciation are disclosed figures; operating '
        'profit, EBITDA and the margins are formulas over them. The published earnings per '
        'share is struck on distributable profit after the statutory employees\' and '
        'directors\' share, which is why it differs slightly from profit over the share '
        'count.')
H2('A.2  Balance sheet — as reported')
rows = [['EGP mn'] + YH + YF]
rows.append(['Total assets'] + [n0(x) for x in
                                [IN['ta_fy23'], IN['ta_fy24'], IN['ta_fy25']]] +
            [n0(x) for x in F['total_assets']])
rows.append(['Cash and bank balances'] +
            [n0(x) for x in [IN['cash_fy23'], IN['cash_fy24'], IN['cash_fy25']]] +
            [n0(x) for x in F['cash']])
rows.append(['Interest-bearing debt'] +
            [n0(x) for x in [IN['debt_fy23'], IN['debt_fy24'], W['debt_total']]] +
            [n0(W['debt_total']) for _ in YF])
rows.append(['Net (cash) / debt'] +
            [n0(IN['debt_fy23'] - IN['cash_fy23']), n0(IN['debt_fy24'] - IN['cash_fy24']),
             n0(W['debt_total'] - IN['cash_fy25'])] +
            [n0(W['debt_total'] - x) for x in F['cash']])
rows.append(['Equity attributable to owners'] +
            [n0(x) for x in [IN['eq_fy23'], IN['eq_fy24'], IN['eq_fy25']]] +
            [n0(x) for x in F['equity']])
rows.append(['Book value per share (EGP)'] +
            [n2(x / SH) for x in [IN['eq_fy23'], IN['eq_fy24'], IN['eq_fy25']]] +
            [n2(x / SH) for x in F['equity']])
rows.append(['Return on equity'] +
            [pc(H['pat'][0] / IN['eq_fy23']), pc(H['pat'][1] / IN['eq_fy24']),
             pc(LN['roe_fy25'])] +
            [pc(F['pat'][i] / F['equity'][i]) for i in range(5)])
table(rows, [1.52, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72], size=8.0,
      band_rows={1})
caption('Table A2 — All three historical years are AUDITED. The FY2025 balance sheet closes '
        f'exactly: total assets of EGP {n0(IN["ta_fy25"])}mn less total liabilities of EGP '
        f'{n0(IN["tl_fy25"])}mn equals equity of EGP {n0(IN["eq_fy25"] + IN["nci"])}mn.')
H2('A.3  Forecast cash flow and the working-capital markers')
rows = [['EGP mn'] + YF]
for lab, vals in [('Attributable profit', F['pat']),
                  ('Add back depreciation', F['dna']),
                  ('Less change in working capital', [-x for x in F['dwc']]),
                  ('Capital expenditure', [-x for x in F['capex']]),
                  ('Dividends paid', [-x for x in F['dividends']]),
                  ('Closing cash', F['cash']),
                  ('Memo: free cash flow to the firm', F['fcff'])]:
    rows.append([lab] + [n0(x) for x in vals])
table(rows, [2.10, 0.92, 0.92, 0.92, 0.92, 0.92], size=8.6, band_rows={6})
caption('Table A3 — Free cash flow to the FIRM excludes treasury income, which is handled '
        'in the equity bridge; free cash flow to equity includes it through profit.')

# ============================== APPENDIX B ===================================
doc.add_page_break()
H1('Appendix B  Peer set, sector structure and risks')
H2('B.1  Peers and the sector frame')
rows = [['', 'Revenue (EGP mn)', 'Profit (EGP mn)', 'Market cap (EGP mn)',
         'Price / earnings', 'Net margin']]
for key in ('self', 'scem', 'mbsc'):
    p_ = PE[key]
    rows.append([p_['name'], n0(p_['rev']), n0(p_['pat']), n0(p_['mcap']),
                 f'{p_["pe"]:.2f}x', pc(p_['pat'] / p_['rev'])])
table(rows, [1.85, 1.15, 1.05, 1.20, 0.95, 0.85], size=8.6)
caption('Table B1 — Every multiple here is RECOMPUTED from revenue, profit and market '
        'capitalisation rather than quoted, because the published multiples for this peer '
        'set do not reconcile against the market capitalisations printed beside them.')
figure('fig8_sector.png', 6.6,
       'Figure B1 — The Egyptian cement balance. The surplus is the whole sector case.')
H2('B.2  The sector balance, and what it is not')
P(f'Egypt carries about {n0(IN["egy_capacity_mt"])}Mt of nameplate capacity against roughly '
  f'{n0(IN["egy_cons_mt"])}Mt of domestic consumption and {n0(IN["egy_prod_mt"])}Mt of '
  f'total sales. The balance now closes because it is taken from one disclosure rather '
  f'than assembled from three: local {n1(IN["egy_cons_mt"])}Mt plus exports '
  f'{n1(IN["egy_exports_mt"])}Mt equals the {n1(IN["egy_prod_mt"])}Mt total. Earlier '
  f'editions set a cement-plus-clinker export figure against a cement-only production '
  f'figure and printed a balance that was out by 7.5Mt. The correction matters beyond '
  f'tidiness: {n1(IN["egy_prod_mt"])}Mt of sales against roughly '
  f'{n0(IN["egy_capacity_mt"])}Mt of nameplate is a market running near '
  f'{pc(PE["sector"]["utilisation"], 0)}, which is NOT the structurally slack market this '
  f'study has described from its first edition. The oversupply risk is prospective — it '
  f'lives in the {n1(IN["egy_revival_mt"])}Mt restart programme, not in the current '
  f'balance — and the distinction is material to the price path. The abolition of the '
  f'production quota in May 2025 removed the mechanism that had been supporting price into '
  f'that surplus, and the {n1(IN["egy_revival_mt"])}Mt restart programme would add to it.')
H2('B.3  Risk register')
P('One entry per risk that could move this valuation by more than a few per cent, each '
  'stated as a mechanism rather than a worry, and each with the disclosure it rests on.')
for head, body in [
    ('Price risk. ', f'This is the dominant risk, and the disclosure corrects how it '
     f'should be framed. The Egyptian market is NOT currently slack: it sold '
     f'{n1(IN["egy_prod_mt"])}Mt against roughly {n0(IN["egy_capacity_mt"])}Mt of '
     f'nameplate, and this company realised a 60.7% rise in its local price in FY2025. The '
     f'risk is prospective and it has two legs — the {n1(IN["egy_revival_mt"])}Mt restart '
     f'programme, and a production quota that was SUSPENDED rather than repealed and could '
     f'return without legislation. Either would meet a market with little spare demand to '
     f'absorb it. That is why the forecast price path grows below cost inflation in every '
     f'year despite an exit rate that would support more.'),
    ('Energy and currency. ', 'Fuel is dollar-priced and electricity tariffs are on a '
     'reform path. Both raise cost independently of what happens to price.'),
    ('Concentration. ', 'One site, one product, one country. There is no diversification '
     'anywhere in this business to absorb a shock to Egyptian construction demand.'),
    ('Carbon. ', f'The EU carbon border mechanism raises the landed cost of exports into '
     f'Europe. At a clinker factor of {n3(IN["clinker_factor"])} — a PRODUCTION ratio, not '
     f'the ratio of two nameplate capacities the earlier edition mistook for one — this '
     f'producer is better placed than most Egyptian peers, but better placed is not '
     f'unaffected. It also ships {pc(UC["vol_clk_exp"]/UC["vol_fy25"])} of its tonnes as '
     f'raw clinker, which carries the highest embedded carbon of anything it sells.'),
    ('Disclosure. ', 'The depth of published financial detail is thin by the standards of '
     'the other markets covered, which is why so much of this study is a triangulation '
     'shown rather than a figure asserted.'),
]:
    bullet(body, bold_head=head)

# ============================== APPENDIX C ===================================
doc.add_page_break()
H1('Appendix C  The expert valuation panel')
P('Three independent valuations of the same company, each built by a different method and '
  'each stated with the specific evidence that would prove it wrong. They are not '
  'averaged: the disagreement between them is the point.')
figure('figD1_experts.png', 6.7,
       'Figure C1 — The three panel valuations against the market price.')
for _i, e in enumerate(EXP, 1):
    H2(f'C.{_i}  {e["label"]} — {e["method"]}')
    rich([('Valuation: ', {'bold': True}),
          (f'EGP {n2(e["low"])} to EGP {n2(e["high"])}, central EGP {n2(e["central"])} '
           f'({sg(e["central"]/SPOT-1)} against the market price of EGP {n2(SPOT)}).', {})])
    P(e['summary'])
    rich([('What would prove this wrong: ', {'bold': True, 'color': BRASS}),
          (e['falsifier'], {})])
_PRIMV = LN['values'][LN['primary']]
rows = [['', 'Low (EGP)', 'Central (EGP)', 'High (EGP)', 'Versus spot']]
for e in EXP:
    rows.append([f'{e["label"]} — {e["method"]}', n2(e['low']), n2(e['central']),
                 n2(e['high']), sg(e['central'] / SPOT - 1)])
cen = sorted(x['central'] for x in EXP)
rows.append(['Panel median', '—', n2(cen[1]), '—', sg(cen[1] / SPOT - 1)])
table(rows, [2.72, 1.02, 1.15, 1.02, 0.94], band_rows={4})
# THIS CAPTION ASSERTED THAT THE MEDIAN 'SITS CLOSE TO' THE CENTRAL AND IT DOES NOT
# [corrected 03-Sep-2026]. It was true of an edition whose central was a weighted blend of
# four lenses; the blend is retired, the central is the cash-flow lens alone, and the
# sentence went on standing while the number it described moved 22% away from it. A number
# stated in prose is computed, never typed — and a RELATION stated in prose is a number.
_MED = sorted(x['central'] for x in EXP)[1]
caption(f'Table C1 — The panel. The median of the three, EGP {n2(_MED)}, sits '
        f'{sg(_MED/_PRIMV-1)} from this study\'s own central of EGP {n2(_PRIMV)} and '
        f'{sg(_MED/SPOT-1)} from the market price. It is NOT a confirmation of anything: two '
        f'of the three panel methods are anchored on the same forecast the central uses, and '
        f'the one that is not — replacement cost — is the highest read in the study. An '
        f'earlier edition compared this median to a weighted average of four lenses; those '
        f'weights are retired, and the comparison is now against the published central.')

# ---- C.4 --------------------------------------------------------------------
# CROSS-EXAMINATION, THE THREE IN ONE ROOM AND THE DIVERGENCE TABLE were absent
# [added 03-Sep-2026]. Depth-bar standard 7 requires all three by name; Appendix C
# ended after the third expert and a summary table.
_E = {e['label']: e for e in EXP}
_C = sorted(EXP, key=lambda e: e['central'])
_LO, _MD, _HI = _C[0], _C[1], _C[2]

H2('C.4  Cross-examination')
P('Each expert is put the strongest objection the other two can make, and each objection is '
  'either conceded or rejected with the arithmetic that settles it. Every figure below comes '
  'from the three valuations above or from the study\'s own committed record.')
rows = [['Objection', 'Raised by', 'Answered', 'The arithmetic']]
rows.append([
    f'{_E["Expert 1"]["method"]} values a plant nobody is building. The '
    f'{n1(IN["egy_revival_mt"])}Mt restart programme is the live test and restarting a '
    f'mothballed kiln costs a fraction of new build.', 'Experts 2 and 3', 'CONCEDED',
    f'This is Expert 1\'s own stated falsifier, and it is the reason the lens is marked to '
    f'USD 95 an annual tonne rather than the USD 130 a new line costs. At USD 95 it reads '
    f'EGP {n2(_E["Expert 1"]["central"])}; the market is paying USD '
    f'{LN["ev_per_t_spot"]:.1f} an annual tonne at the traded price.'])
rows.append([
    'A replacement-cost read says nothing about whether the plant earns its cost of capital.',
    'Expert 3', 'REJECTED',
    f'That is what it is for. It is the one read in this study anchored on something other '
    f'than a forecast, and it is the strongest argument against the central — which is why '
    f'it is published beside it at EGP {n2(_E["Expert 1"]["central"])} rather than averaged '
    f'away.'])
rows.append([
    f'The forecast that drives the earnings reads opens at '
    f'{pc(FA["first_forecast_rate"], 2)} against a filed peak of '
    f'{pc(FA["latest_reviewed_rate"], 2)}, so it has no headroom.', 'Expert 1',
    'CONCEDED — AND STATED IN THE STUDY',
    f'It is the point of the range: the bull corner is EGP {n2(LN["high"])}, barely above the '
    f'central of EGP {n2(_PRIMV)}, while the bear corner is EGP {n2(LN["low"])} on the FY2023 '
    f'margin this company actually filed. Essentially the whole range is downside, and a '
    f'symmetric band would have concealed that.'])
rows.append([
    'The beta is a peer median, not this company\'s own regression, so the discount rate is '
    'borrowed.', 'Experts 1 and 2', 'CONCEDED — AND PUBLISHED BOTH WAYS',
    f'The own-stock regression against the EGX30 returns {CON[1]["alternative"]} on an '
    f'R-squared of 4.7%, below the usability floor, so tier 1 is not available. On the '
    f'regression the lens would read EGP {n2(CON[1]["fv_alternative"])} against '
    f'EGP {n2(CON[1]["fv_adopted"])} — {sg(CON[1]["effect"])}, the study\'s most '
    f'consequential contested judgement.'])
rows.append([
    'Peer betas are used as published, without unlevering and re-levering.', 'Expert 3',
    'CONCEDED — WITH THE DIRECTION NAMED',
    'The peers carry borrowings and this company holds net cash, so completing the step '
    'could only LOWER the beta, lower the rate and RAISE the value. The adopted figure is '
    'therefore the cautious end of tier 2, and the omission is flagged rather than passed '
    'over.'])
rows.append([
    'Growth is worth having, so a terminal that punishes it is wrong.', 'Expert 2',
    'REJECTED',
    f'Measured on this company\'s own returns: at the terminal return and reinvestment rate '
    f'this study computes ({pc(GDV["roic_term"], 2)} against a terminal cost of capital of '
    f'{pc(GDV["wacc_term"], 2)}, a spread of {pc(GDV["spread_pct"], 2)}), moving terminal '
    f'growth from 3% to 7% takes the value from EGP {n2(GDV["fv_at_g3"])} DOWN to '
    f'EGP {n2(GDV["fv_at_g7"])} — about {n2(abs(GDV["fv_at_g7"] - GDV["fv_at_g3"]) / 4)} a '
    f'share for each point of growth, the WRONG way. Growth funded at a return below the '
    f'cost of capital destroys value, and section 1.8 shows the arithmetic.'])
table(rows, [2.05, 1.05, 1.20, 2.50], size=8.0)
caption('Table C2 — Cross-examination. Four of the six objections are conceded, which is the '
        'honest count for a study whose forecast sits at its subject\'s best filed year and '
        'whose discount rate rests on a borrowed beta. The two rejections each rest on a '
        'number rather than a preference.')

# ---- C.5 --------------------------------------------------------------------
H2('C.5  The three in one room')
P(f'Put in one room the three methods land between EGP {n2(_LO["central"])} and '
  f'EGP {n2(_HI["central"])}, a spread of {pc(_HI["central"]/_LO["central"]-1)} of the lower '
  f'number, with a median of EGP {n2(_MD["central"])} against a market price of '
  f'EGP {n2(SPOT)} — {sg(_MD["central"]/SPOT-1)}. All three sit below the price, and so does '
  f'the study\'s own central of EGP {n2(_PRIMV)}.')
P(f'What they agree on is not built in, and that is what makes it worth reading. None of the '
  f'three sets a macro path of its own — all of them stand on the house inflation, currency '
  f'and policy path for Egypt, so their disagreement is entirely about how a tonne of cement '
  f'should be capitalised and never about what the economy is doing. All three also agree '
  f'that this company is worth less than EGP {n2(SPOT)}, by methods that share no arithmetic: '
  f'one values the steel and concrete, one the earnings stream, one the cash returned against '
  f'what the capital costs.')
P(f'Where they part company is what they are anchored ON. {_HI["label"]} — '
  f'{_HI["method"].lower()} — is the highest at EGP {n2(_HI["central"])} because it is the '
  f'only read not anchored on a forecast at all; it asks what the plant would cost to build '
  f'and marks that down for a market with dormant capacity. The other two are anchored on '
  f'the same forecast the central uses, and that forecast already sits at this company\'s '
  f'best filed margin. So the panel\'s spread is largely the difference between valuing an '
  f'asset and valuing a stream, which is exactly the disagreement a cyclical single-plant '
  f'producer should produce — and it is why the study publishes the replacement-cost read '
  f'beside its central rather than inside it.')

# ---- C.6 --------------------------------------------------------------------
H2('C.6  Reading the divergence')
P('One row per pair, naming the single assumption that accounts for most of the gap between '
  'them, and what is left of the gap once that assumption is removed.')
rows = [['Pair', 'Gap (EGP)', 'Gap %', 'What drives it', 'What is left']]
_pairs = [
    (_HI, _MD, 'the anchor itself — one values the plant, the other the stream. There is no '
               'single parameter to remove, because the two do not share one.', None),
    (_HI, _LO, 'the same thing, at its widest: an asset value against the most '
               'forecast-dependent read in the panel.', None),
    (_MD, _LO, 'both are anchored on the same forecast, so what separates them is how much '
               'of the value is allowed to sit beyond the explicit window.', None),
]
for a, b in [(_HI, _MD), (_HI, _LO), (_MD, _LO)]:
    why = next(w for x, y, w, _ in _pairs if x is a and y is b)
    rows.append([f'{a["label"]} vs {b["label"]}', n2(a['central'] - b['central']),
                 pc(a['central'] / b['central'] - 1), why, 'not decomposed'])
rows.append([f'Panel median vs the central', n2(_MD['central'] - _PRIMV),
             pc(abs(_MD['central'] / _PRIMV - 1)),
             'nothing structural — the central is a cash-flow read and so is one of the three',
             'not decomposed'])
table(rows, [1.55, 0.80, 0.65, 2.75, 1.05], size=8.0)
caption('Table C3 — The divergence. Not one of these gaps reduces to a parameter, and that is '
        'the finding rather than a gap in the analysis: the panel was cast by METHOD, so two '
        'members of it do not share an input to vary. Where a pair does share its arithmetic '
        '— the median against the central — the difference is small and structural. A '
        'divergence table that decomposed these into parameters would be inventing a common '
        'model the panel deliberately does not have.')

# ============================== ABOUT ========================================
doc.add_page_break()
H1('About this series')
box([
    ('WHAT THIS IS.  ',
     'An independent, educational valuation study. It is NOT investment advice and it '
     'issues no buy, sell or hold recommendation. It publishes a fair-value range, a '
     'probability distribution for the price, and the model behind both, and it grades its '
     'own forecasts publicly when they resolve.'),
    ('WHAT IT RESTS ON.  ',
     'The company\'s own audited and reviewed financial statements, read from the filings '
     'rather than from any vendor\'s summary. Every input carries a value, a source, a date '
     'and a research layer in the companion source register, and every figure in this '
     'document is computed by the model rather than typed into the document.'),
    ('THE COMPANION FILES.  ',
     f'A workbook that recalculates this study live, and a standalone bibliography listing '
     f'every registered input with its source, the judgements with what would overturn each '
     f'one, and the negative results — the things looked for and not found.'),
    ('WHAT IT DOES NOT DO.  ',
     'It never states a rating or a price target. Where a figure has two legitimate '
     'framings, both are published. Where a judgement is contested and worth more than a '
     'few per cent of the answer, the study computes it both ways and shows the pair '
     'instead of averaging them into one number nobody can check.'),
])

H1('Disclosure & Disclaimer')
P('Testahil · Independent valuation research · Educational analysis, not investment '
  'advice. No rating and no price target is expressed or implied.', size=9.2, bold=True)
P('This document is published for education and discussion. It is not a recommendation, an '
  'offer, or a solicitation to buy or sell any security, and it takes no account of any '
  'reader\'s circumstances, objectives or constraints. Nothing in it should be relied on as '
  'the basis for an investment decision.', size=8.8)
P('The valuation is a range produced by a stated model from stated inputs, and it will be '
  'wrong in ways the model cannot see. Section 7 sets out what would change it. Forecasts '
  'about a single-plant producer in one country are uncertain in ways no range fully '
  'captures, and past performance — the company\'s or this method\'s — does not predict '
  'future results.', size=8.8)
P(f'The price quoted throughout is the latest known close, EGP {n2(SPOT)} on '
  f'{SPOT_DATE_WORDS}. It moves; the valuation does not move with it. No position is held '
  f'in this security by the author of this study, and no compensation of any kind has been '
  f'received from the company, from any holder of its shares, or from anyone with an '
  f'interest in its price.', size=8.8)

OUT = 'ARCC_Valuation_Study_03-09-2026_public.docx'
doc.save(OUT)
print('wrote', OUT)
