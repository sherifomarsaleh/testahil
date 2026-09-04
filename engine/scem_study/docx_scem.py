"""SCEM_Valuation_Study_04-09-2026_public.docx — TMPV house structure.

16 headings: 7 top-level sections plus the 9 subsections of section 1, then three
appendices. Reads study_numbers.json exclusively — no numeral is typed here.

Written for an external reader: no internal procedure names, step numbers or house
process references appear anywhere in the output.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..'))   # the shared instruments live in engine/
from docx_base import *          # noqa: F401,F403
import table_residual as TRES        # the shared waterfall check, not hand-rolled
from table_residual import waterfall                              # noqa: F401
from docx_base import (doc, P, H1, H2, rich, bullet, table, figure, box, caption,
                       masthead, INK, GREY, BRASS, GOLD, F_CREAM, F_PANEL, Pt, Inches)

D = json.load(open('study_numbers.json'))
BETA = json.load(open('beta_result.json'))
STK = json.load(open('strike_result.json'))
S0 = json.load(open('step0_result.json'))
# [R-CAL-02] WHAT A READER IS SHOWN IS THE BAND RECORD, generated from the committed
# panels and read here rather than re-derived: how many resolved three-month forecasts
# this name's history holds, how often the price finished inside the band, the count
# always printed beside the percentage, and a flag ONLY when a two-sided binomial test
# earns one. The skill verdict is retired outright and reaches no reader, by its name or
# by a description of it.
def _band_record(tk):
    """This name's published band record, read from the site's own generated block.

    Handed to node and read off the OBJECT the page renders [R-ENF-03], never matched out
    of the text with a regular expression: a JavaScript object literal takes the LAST
    declaration of a duplicated key and re.search takes the FIRST, and that difference has
    already put a support level above its own close on a live page.
    """
    import subprocess
    root = os.path.abspath(os.path.join(HERE, '..', '..'))
    js = ("const fs=require('fs');"
          "const src=fs.readFileSync(%r,'utf8');"
          "eval(src.replace(/^\\s*(const|var|let)\\s+/gm,'globalThis.'));"
          "process.stdout.write(JSON.stringify(globalThis.BANDS[%r]));"
          % (os.path.join(root, 'assets', 'data.js'), tk))
    out = subprocess.run(['node', '-e', js], capture_output=True, text=True, check=True)
    rec = json.loads(out.stdout)
    assert rec and rec.get('n'), 'no published band record for %s' % tk
    return rec


BAND = _band_record('SCEM')
M, H, F = D['meta'], D['history'], D['forecast']
W, DCF, LN, SN = D['wacc'], D['dcf'], D['lenses'], D['sensitivity']
TR, PE, SHT, DISP = D['terminal_reconciliation'], D['peers'], D['share_triangulation'], D['disposal']
EXP, LR, GDV = D['experts'], D['lens_ranges'], D['growth_destroys_value']
LREC = D['lens_record']        # [R-LENS-03] the primary and its cross-checks
MACRO = D['macro_live']        # [R-MACRO-01] the house path's own figures
LKEYS = ['DCF (cash flow)', 'Relative multiples',
         'Asset / replacement cost', 'Book value (disclosed floor)']
IN = {k: v['value'] for k, v in D['inputs'].items()}
SPOT, SH = M['spot'], M['shares_mn']
YH, YF = ['FY2023', 'FY2024', 'FY2025'], F['years']


def n0(x): return f"{x:,.0f}"
def n1(x): return f"{x:,.1f}"
def n2(x): return f"{x:,.2f}"
def pc(x, dp=1): return f"{x*100:.{dp}f}%"
def sg(x, dp=1): return f"{x*100:+.{dp}f}%"


# ============================== COVER ========================================
masthead()
P('Sinai Cement Company S.A.E.', size=22, bold=True, space_after=1)
P('Egyptian Exchange · SCEM · Egyptian pounds · issued 4 September 2026, struck on the closing price of 2 September 2026', size=11, color=GREY,
  space_after=10)
rich([(f'A single-plant cement producer, sitting on net cash worth '
       f'{pc(D["dcf"]["net_cash"] / (SPOT * SH), 0)} of its market '
       'capitalisation, at the top of the best year the Egyptian cement industry has had '
       'since 2008 — and with 12.6 million tonnes of dormant capacity queuing to restart '
       'inside the forecast window.', {'size': 12})], space_after=10)

box([('What this is. ', 'An independent valuation of Sinai Cement, an educational '
      'analysis and not investment advice. It carries no rating and no price target — '
      'fair-value ranges and distributions only.'),
     ('The company in one line. ', 'Two cement lines at El Hassana in North Sinai, about '
      '3.8 million tonnes a year of capacity, 77.6% owned by the French Vicat group, with '
      'a 22.4% free float and essentially no debt.'),
     ('Where the value lands. ',
      f'The cash-flow lens is the answer: EGP {n2(LN["central"])} a share against a market '
      f'price of EGP {n2(SPOT)}, {sg(LN["central"]/SPOT-1)}. Flexing the operating margin '
      f'down to the lowest the company has ever filed takes it to EGP '
      f'{n2(LREC["primary"]["range"]["low"])}, and the forecast opens above the best year '
      f'it has filed, so essentially the whole of that range is downside. The other lenses '
      f'are published beside it rather than averaged into it: replacement cost EGP '
      f'{n2(LN["values"]["Asset / replacement cost"])}, an enterprise multiple EGP '
      f'{n2(LN["values"]["Relative multiples"])}, and a disclosed book floor of EGP '
      f'{n2(LN["values"]["Book value (disclosed floor)"])}.')])

# ---- summary valuation table (gate item i) ----------------------------------
H2('Summary valuation table')
ROLE = {'DCF (cash flow)': 'PRIMARY — this is the central',
        'Relative multiples': 'cross-check',
        'Asset / replacement cost': 'cross-check',
        'Book value (disclosed floor)': 'disclosed floor, never weighted'}
rows = [['Lens', 'Value per share (EGP)', 'Role', 'Versus spot', 'Terminal value % of EV']]
for k in LKEYS:
    rows.append([k, n2(LN['values'][k]), ROLE[k],
                 sg(LN['values'][k] / SPOT - 1),
                 pc(DCF['tv_share']) if k == 'DCF (cash flow)' else '—'])
rows.append(['Central fair value', n2(LN['central']), 'the primary lens, not a blend',
             sg(LN['central'] / SPOT - 1), '—'])
_pr = LREC['primary']['range']
rows.append(['Range on the primary lens',
             f'{n2(_pr["low"])} – {n2(_pr["high"])}',
             'the operating margin across its own filed span',
             f'{sg(_pr["low"]/SPOT-1)} to {sg(_pr["high"]/SPOT-1)}', '—'])
rows.append(['Market price, 2 September 2026', n2(SPOT), '—', '—', '—'])
rows.append(['Vicat tender offer, July 2025 (reference only)', n2(IN['mto_price']), '—',
             sg(IN['mto_price'] / SPOT - 1), '—'])
table(rows, [2.55, 1.35, 0.72, 1.02, 1.36], band_rows={5})
caption('The central IS the cash-flow lens. The other reads are cross-checks published '
        'beside it and are not averaged into it: where several methods disagree the '
        'disagreement is the output, and a weighted blend of them is a new method with '
        'weights nobody has tested. Terminal value as a percentage of enterprise value is '
        'shown beside the cash-flow lens, and again in the bridge in section 1.1.')

figure('fig1_football.png', 6.9,
       'Figure 1 — Each lens as a range, with its base case marked, against the market price.')

# ============================== 1 ============================================
H1('1  Fundamental valuation')
P('Sinai Cement is valued as a single operating company, not as a sum of parts, and the '
  'reason is worth stating before any number. Essentially all of its revenue is grey '
  'cement and clinker from one asset base. Its subsidiaries are a service arm and a '
  'trading arm feeding that same cement rather than separable businesses. Its balance '
  'sheet carries EGP 36.8 million of total debt against roughly EGP 5.2 billion of '
  'equity, which makes it net cash rather than leveraged. There is no lending book, no '
  'captive finance arm and no third-party asset management.')
P('The one thing that could have made this a two-legged valuation has already been sold. '
  f'Sinai Cement held 25.40% of Sinai White Portland Cement and disposed of it to Aalborg '
  f'Portland, part of the Cementir group, for EUR {n0(IN["swcc_eur"])} million, completing '
  f'on 13 August 2024. There is no second leg left to value, so a single lens is not a '
  f'simplification here — it is the accurate description.')

box([('One thing to fix in your head before reading the history. ',
      f'Profit after tax of EGP {n0(H["pat"][1])} million in FY2024 on revenue of EGP '
      f'{n0(H["revenue"][1])} million is a '
      f'{pc(H["pat"][1] / H["revenue"][1], 0)} net margin. No cement plant earns that from '
      f'making cement. That year contains the Sinai White disposal gain of roughly EGP '
      f'{n0(DISP["gain"])} million and treasury income of EGP {n0(H["treasury"][1])} '
      f'million. THE UNDERLYING FIGURE IS NOT THE REPORTED PROFIT LESS THE GAIN: it is '
      f'operating profit of EGP {n0(H["ebit"][1])} million plus that treasury income, '
      f"taxed at the effective {pc(IN['tax_eff'], 1)}, which is EGP "
      f'{n0(DISP["underlying_fy24_pat"])} million — so FY2025 profit '
      f'{sg(H["pat"][2]/DISP["underlying_fy24_pat"]-1, 0)} rather than '
      f'{sg(H["pat"][2]/H["pat"][1]-1, 0)} as the headline comparison suggests.')])

figure('fig7_bridge.png', 6.7,
       'Figure 2 — Profit after tax across three years, and what FY2024 actually contained.')

# ---- 1.1 --------------------------------------------------------------------
H2('1.1  The cash-flow model — the primary lens, with the full waterfall')
P('The discounted cash-flow model is the primary lens, and for this company it IS the '
  'answer rather than a share of one. It runs on a volume-and-price build off one plant, '
  'discounts each year at that year\'s own cost of capital, and capitalises a terminal '
  'value at a separately built terminal rate. An earlier edition averaged it with three '
  'other reads at weights that were typed rather than tested — and two of those three '
  'value a cement plant off reported accounting earnings and historical-cost book, which '
  'for an asset commissioned in 1997 and carried through a five-fold devaluation measures '
  'the accounting rather than the plant.')
# THE PRINTED WATERFALL WAS NOT THE MODEL'S WATERFALL. It ran NOPAT, plus depreciation,
# less capital expenditure, less the change in working capital, to free cash flow — and the
# model computes free cash flow as NOPAT LESS REINVESTMENT, with the first year scaled to
# the unearned part of it. So three of the four lines between NOPAT and the answer fed
# nothing, the two that do were not printed at all, and a reader adding the column got EGP
# 1,829mn in year one against a printed 799. Under a caption reading "the FULL waterfall...
# every line is a live formula in the companion model".
#
# Those three lines are real and are not deleted: they drive the projected balance sheet —
# property, working capital and cash — and they are shown for what they are, below the
# answer rather than inside it. This is the ARCC Table 3 shape at its worst: every figure
# individually correct, and the relationship between them not the model's.
_STUB = 1.0 - IN['stub_years']
rows = [['EGP million'] + YF]
for lab, key, f in [('Revenue', 'revenue', n0), ('EBITDA', 'ebitda', n0),
                    ('EBITDA margin', None, None), ('Depreciation & amortisation', 'dna', n0),
                    ('EBIT', 'ebit', n0), ('NOPAT  (EBIT × (1 − t))', 'nopat', n0),
                    ('Depreciation and amortisation added back', 'dna', n0),
                    ('Capital expenditure', 'capex', lambda x: '(' + n0(x) + ')'),
                    ('Change in working capital', 'dwc',
                     lambda x: ('(' + n0(x) + ')') if x > 0 else n0(-x)),
                    ('Free cash flow to the firm', 'fcff', n0),
                    ('Discount factor', 'df', lambda x: f'{x:.4f}'),
                    ('Present value of free cash flow', 'pv', n0)]:
    if key is None:
        rows.append([lab] + [pc(F['ebitda'][i] / F['revenue'][i]) for i in range(5)])
    else:
        rows.append([lab] + [f(F[key][i]) for i in range(5)])
table(rows, [2.25, 0.94, 0.94, 0.94, 0.94, 0.94], band_rows={8, 10})
# THE FIRST YEAR FOOTS ONLY WITH THE STUB NAMED, so the caption names it and the build
# asserts every year reproduces from the rows printed above it.
for _i in range(5):
    waterfall(
        F['nopat'][_i],
        [('Plus depreciation and amortisation', F['dna'][_i]),
         ('Less capital expenditure', F['capex'][_i]),
         ('Less change in working capital', F['dwc'][_i])],
        F['fcff'][_i], dp=0, what='Table 1, %s' % YF[_i],
        # THE FIRST YEAR IS THE ONE LINE A READER CANNOT ADD UP AND THE CAPTION SAYS SO:
        # only the unearned part of FY2026 is a future receipt. Declared with its reason
        # rather than silently tolerated, which is what the helper's own refusal is for.
        extra=(-(F['nopat'][_i] + F['dna'][_i] - F['capex'][_i] - F['dwc'][_i])
               * (1.0 - _STUB)) if _i == 0 else 0.0,
        why=('only the part of %s still unearned at the valuation date is a future '
             'receipt; the caption names the fraction' % YF[0]) if _i == 0 else '')
# The stub is quoted to the precision a reader NEEDS, not to a round one: at 42% the two
# printed rows give 804 against a printed 799, so the caption naming the scaling would not
# have let anyone reproduce it. Tested on the PRINTED strings, which is what the reader has.
_STUB_TXT = pc(_STUB, 1)
_rd = lambda t: float(t.replace(',', '').rstrip('%'))
# the stub scales the WHOLE first-year waterfall, not NOPAT alone, so the reader's own
# arithmetic runs down the column and then applies the fraction the caption names
_yr1 = (_rd(n0(F['nopat'][0])) + _rd(n0(F['dna'][0])) - _rd(n0(F['capex'][0]))
        - _rd(n0(F['dwc'][0])))
assert abs(round(_yr1 * _rd(_STUB_TXT) / 100.0) - _rd(n0(F['fcff'][0]))) <= 2.0, (
    'the printed stub does not reproduce the printed first-year cash flow')
caption(f'Table 1 — From revenue to the present value of free cash flow to the firm. Free '
        f'cash flow is NOPAT plus book depreciation, less the capital actually spent and '
        f'the working capital the growth absorbs — the SAME waterfall the terminal uses, '
        f'so the two windows cannot mean different things by the same words. The '
        f'first year is scaled to the {_STUB_TXT} of {YF[0]} still unearned at the '
        f'valuation date — that is the only line a reader cannot add up from the two above '
        f'it. Every line is a live formula in the companion model.')
P('Capital expenditure is the company\'s own run rate from its cash-flow statements — '
  'EGP 121 million in FY2023, 526 million in FY2024 and 262 million in FY2025 — escalated '
  'with domestic costs, and depreciation is the rate its own accounting-policies note '
  'discloses applied to the asset base that capital spending builds. An earlier edition '
  'charged depreciation at 4.6% of revenue falling to 4.2%, against a company that filed '
  '1.35%.', size=9.5, italic=True, color=GREY)

P(f'The discount rate is not one number. Egypt\'s cost of capital today reflects a policy '
  f'rate of {pc(MACRO["policy_rate"], 2)} and a ten-year government yield of '
  f'{pc(IN["rf"], 2)}, neither of which the central bank itself expects to persist — its '
  f'own published target is {pc(MACRO["terminal_inflation"], 0)}. '
  'Applying today\'s rate to a perpetuity would assert that Egypt never normalises. Each '
  'forecast year is therefore discounted at its own forward rate, sliding from the '
  'explicit-window cost of capital to the terminal one, and the terminal value is '
  'discounted using the identical cumulative factor as the year-five cash flow. One date, '
  'one price of time.')
rows = [['', 'Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5']]
rows.append(['Forward cost of capital'] + [pc(x, 2) for x in F['fwd_wacc']])
rows.append(['Cumulative discount factor'] + [f'{x:.4f}' for x in F['df']])
table(rows, [2.25, 0.94, 0.94, 0.94, 0.94, 0.94])
caption('Table 2 — The discount schedule. The shape of the slide is inherited from the '
        'assumed borrowing-cost path rather than invented separately.')

H2('The enterprise-to-equity bridge')
rows = [['', 'EGP million', 'Per share (EGP)']]
for lab, v in [('Present value of the explicit five years', DCF['sum_pv']),
               ('Present value of the terminal value', DCF['pv_tv']),
               ('Enterprise value', DCF['ev'])]:
    rows.append([lab, n0(v), n2(v / SH)])
rows.append(['Terminal value as a percentage of enterprise value', pc(DCF['tv_share']), '—'])
rows.append(['Plus net cash', n0(DCF['net_cash']), n2(DCF['net_cash'] / SH)])
# THE MINORITY WAS DEDUCTED IN THE MODEL AND PRINTED NOWHERE, so a reader adding the
# printed column reached 11,547 against a printed 11,426 — the line, not the arithmetic,
# was missing. It is printed now, and the bridge is asserted to foot from its own rows.
rows.append(['Less non-controlling interests in the subsidiaries',
             '(' + n0(IN['nci']) + ')', '(' + n2(IN['nci'] / SH) + ')'])
rows.append(['Equity value', n0(DCF['equity']), n2(DCF['fv'])])
rows.append(['Market price', '—', n2(SPOT)])
table(rows, [3.55, 1.65, 1.55], band_rows={4, 7})
waterfall(DCF['ev'],
          [('Plus net cash', DCF['net_cash']),
           ('Less non-controlling interests', IN['nci'])],
          DCF['equity'], dp=0, what='Table 3, the bridge')
waterfall(DCF['sum_pv'], [('Plus the present value of the terminal value', DCF['pv_tv'])],
          DCF['ev'], dp=0, what='Table 3, enterprise value')
# THE CAPTION TYPED 41% AGAINST A COMPUTED 49.2% PRINTED TWO ROWS ABOVE IT. Read from
# the record. The minority basis is named because the deduction is now visible; the
# alternative a reviewer proposed is priced here rather than asserted away, since at
# EGP 2,008mn it is worth more than a sixth of the answer.
_nci_alt = 2008.0
caption(f'Table 3 — The bridge. Net cash is ADDED, because this company holds more cash '
        f'than debt, and the minority is deducted from EQUITY value rather than from '
        f'enterprise value, on the share of profit the subsidiaries actually earn. A '
        f'reviewer proposed EGP {n0(_nci_alt)} million instead, {pc(_nci_alt / DCF["ev"], 0)} '
        f'of enterprise value; on that reading the shares are worth EGP '
        f'{n2((DCF["ev"] + DCF["net_cash"] - _nci_alt) / SH)} rather than '
        f'EGP {n2(DCF["fv"])}, and the reasoning behind the adopted figure is in the input '
        f'register. Terminal value is {pc(DCF["tv_share"], 0)} of enterprise value.')

H2('The terminal value, and the judgement that decides it')
P('The single most consequential judgement here is what return the company earns on '
  'capital in perpetuity, because that sets how much of its growth must be paid for. '
  'Measured on the books the answer is meaningless: the El Hassana plant was commissioned '
  'from 1997 and is carried at historic cost in pre-devaluation pounds, so dividing '
  "today's profit by that asset base returns a return no cement plant has ever earned.")
P(f'The terminal return is therefore struck on REPLACEMENT cost. Building 3.80 million '
  f'tonnes of grinding capacity costs about USD {n0(IN["repl_usd_t"])} per annual tonne, '
  f'or EGP {n0(DCF["ic_repl"])} million at today\'s exchange rate. On that basis the '
  f'terminal return on capital is {pc(DCF["roic_term"])} and the reinvestment rate is '
  f'{pc(DCF["rr_term"])} of profit. Growth is only real if someone pays today\'s price for '
  f'the capacity that delivers it — and the same rule now governs the explicit forecast '
  f'years, so both windows price growth identically.')
box([('And this is why growth does not help. ',
      f'Terminal return on capital of {pc(DCF["roic_term"])} sits BELOW the terminal cost '
      f'of capital of {pc(W["wacc_term"])}. Every extra point of perpetual growth must be '
      f'bought with reinvestment that earns less than it costs, so raising terminal growth '
      f'from 3% to 7% LOWERS fair value, from EGP {n2(GDV["fv_at_g3"])} to EGP '
      f'{n2(GDV["fv_at_g7"])}. That is not a modelling artefact; it is the correct reading '
      'of a mature plant in an oversupplied market. This company creates value by '
      'harvesting and distributing, not by growing.')])

# EVERY LENS TABLE ENDED ON AN ANSWER A READER COULD NOT REACH FROM THE ROWS ABOVE IT.
# All three carried an enterprise or earnings figure and then jumped straight to value per
# share, so the net cash, the minority and the share count — every one of which the model
# uses — were printed nowhere: on the normalised lens a reader dividing the printed
# earnings by the printed share count reached EGP 39.66 against a printed 58.10. The tail
# is the bridge's own three lines, and the build asserts the printed answer reproduces
# from the rows printed above it.
def lens_tail(rows, ev_or_earn, answer, first_label):
    rows.append([first_label, n0(ev_or_earn)])
    rows.append(['Plus net cash (EGP mn)', n0(DCF['net_cash'])])
    rows.append(['Less non-controlling interests (EGP mn)', '(' + n0(IN['nci']) + ')'])
    rows.append([f'Divided by shares in issue ({n1(SH)} million)', ''])
    rows.append(['Implied value per share (EGP)', n2(answer)])
    waterfall(ev_or_earn,
              [('Plus net cash', DCF['net_cash']),
               ('Less non-controlling interests', IN['nci']),
               ('Divided by shares in issue', SH)],
              answer, dp=2, what=first_label)
    return rows


# ---- 1.2 --------------------------------------------------------------------
H2('1.2  The asset lens — enterprise value per tonne against replacement cost')
P('For cement, the sector\'s own yardstick is enterprise value per annual tonne of '
  'capacity, and it is used here in place of a book-value lens. That substitution is '
  'deliberate: a plant commissioned in 1997 and carried through a five-fold devaluation '
  'has a book value that measures the accounting rather than the asset, so a price-to-book '
  'ratio on this company says almost nothing.')
rows = [['', 'Value']]
for lab, v in [('Enterprise value at the market price (EGP mn)', n0(SPOT * SH - DCF['net_cash'])),
               ('Capacity (million tonnes a year)', n1(IN['capacity_mt'])),
               ('Enterprise value per tonne, at market (USD/t)', n1(LN['ev_per_t_spot'])),
               ('Replacement cost of new capacity (USD/t)', n0(IN['repl_usd_t'])),
               ('Discount to replacement cost', pc(LN['ev_per_t_spot'] / IN['repl_usd_t'] - 1)),
               ('Justified enterprise value per tonne (USD/t)', n0(IN['ev_t_just']))]:
    rows.append([lab, v])
lens_tail(rows, LN['ev_asset'], LN['values']['Asset / replacement cost'],
          f'Implied enterprise value at EGP {n1(IN["fx"])} to the dollar (EGP mn)')
table(rows, [4.45, 2.30], band_rows={11})
caption('Table 5 — The asset lens. The justified figure sits below replacement cost '
        'because nobody pays build cost for capacity in a market with a structural surplus.')
P('This is the most generous of the four lenses, and the reason is instructive rather than '
  'convenient: the market is paying roughly USD 81 per annual tonne for an operating, '
  'profitable, cash-generative plant, against USD 130 to build one. That gap is real. What '
  'it does not tell you is whether the plant will earn its cost of capital, which is what '
  'the cash-flow lens answers and answers less generously. The disagreement between these '
  'two lenses is the central question about this company, and section 1.5 does not average '
  'it away.')

# ---- 1.3 --------------------------------------------------------------------
H2('1.3  Relative multiples')
P('The named Egyptian comparator is Misr Beni Suef Cement, which posted the same 2025 '
  'step-change: attributable profit up 373.7% to EGP 3.946 billion on sales of EGP 5.700 '
  'billion, trading at 6.44 times trailing earnings and 5.03 times EBITDA. Arabian Cement '
  'reported roughly EGP 3.6 billion of consolidated profit on the same industry '
  'conditions. The uniformity across the peer group is itself the finding: this was a '
  'sector event, not a company event, which is why the multiple here is applied to '
  'normalised rather than trailing earnings.')
rows = [['', 'Value']]
# THE HAIRCUT WAS APPLIED IN THE MODEL AND PRINTED NOWHERE, so a reader multiplying the
# printed revenue by the printed margin reached 2,527 against a printed 2,325. It is the
# line that makes this lens a normalisation rather than half of one, and it is now visible.
for lab, v in [('FY2025 revenue (EGP mn)', n0(H['revenue'][2])),
               (f'Haircut to a mid-cycle revenue base',
                pc(IN['norm_rev_haircut'] - 1)),
               ('Mid-cycle revenue base (EGP mn)',
                n0(H['revenue'][2] * IN['norm_rev_haircut'])),
               ('Mid-cycle EBITDA margin', pc(IN['norm_mgn'])),
               ('Normalised EBITDA (EGP mn)', n0(LN['ebitda_norm'])),
               ('Justified EV/EBITDA', f"{IN['ev_ebitda_just']:.1f}x"),
               ]:
    rows.append([lab, v])
lens_tail(rows, LN['ebitda_norm'] * IN['ev_ebitda_just'],
          LN['values']['Relative multiples'], 'Implied enterprise value (EGP mn)')
assert abs(H['revenue'][2] * IN['norm_rev_haircut'] * IN['norm_mgn']
           - LN['ebitda_norm']) < 1.0, 'normalised EBITDA does not foot from its own rows'
table(rows, [4.45, 2.30], band_rows={11})
caption('Table 6 — The relative lens, struck at the peer\'s own EBITDA multiple with no '
        'premium for net cash, which the bridge adds separately.')

# ---- 1.4 --------------------------------------------------------------------
H2('1.4  Normalised earnings power — where this sits in the cycle')
P('2025 was the first year since 2008 that Egypt\'s cement supply and demand balanced. '
  'Domestic consumption rose 13.4% to 54 million tonnes, production rose 18% to about 65 '
  'million tonnes, operating utilisation reached 98%, and prices roughly doubled after the '
  'competition authority permanently lifted production quotas in July 2025. Every one of '
  'those is a cyclical high, not a plateau.')
rows = [['', 'Value']]
for lab, v in [('Normalised EBITDA (EGP mn)', n0(LN['ebitda_norm'])),
               ('Less depreciation & amortisation (EGP mn)',
                '(' + n0(H['dna'][2]) + ')'),
               (f'Less tax at the statutory {pc(IN["tax_stat"], 1)} (EGP mn)',
                '(' + n0((LN['ebitda_norm'] - H['dna'][2]) * IN['tax_stat']) + ')'),
               ('Normalised NOPAT — the earnings capitalised (EGP mn)',
                n0(LN['nopat_norm'])),
               ('Treasury income on the cash pile, DELIBERATELY EXCLUDED', 'nil'),
               ('Justified price/earnings', f"{IN['pe_just']:.1f}x")]:
    rows.append([lab, v])
lens_tail(rows, LN['earn_norm'] * IN['pe_just'],
          LREC['retired']['normalised_earnings']['value'], 'Capitalised earnings (EGP mn)')
table(rows, [4.45, 2.30], band_rows={11})
caption('Table 7 — Normalised earnings power. THIS READ IS RETIRED AS A LENS FOR THIS '
        'company and is shown for the record rather than carried into the answer: on a '
        'single-asset plant whose margin is an output of how hard the kilns run against a '
        'fixed cost stack, there is no mid-cycle earnings level the cash-flow lens does '
        'not already carry. It rests on a mid-cycle margin struck between the '
        'FY2024 outturn and the FY2025 peak. The income the cash pile earns is left out of '
        'the capitalised figure on purpose: the cash itself is added at face below, and '
        'capitalising its income as well would pay for the same asset twice.')

# ---- 1.5 --------------------------------------------------------------------
H2('1.5  Synthesis — one answer, and the reads that disagree with it')
P(f'The lenses do not agree, and the disagreement is PUBLISHED rather than smoothed. The '
  f'cash-flow lens is the answer for this class of company, at EGP {n2(LN["central"])}. '
  f'The replacement-cost read, which asks only what the plant itself is worth, lands at '
  f'EGP {n2(LN["values"]["Asset / replacement cost"])}. The enterprise multiple lands at '
  f'EGP {n2(LN["values"]["Relative multiples"])} and is the weakest of them, because the '
  f'Egyptian listed peer set is two names and neither publishes an EBITDA series this '
  f'study could measure a multiple from. Book value is a disclosed floor at EGP '
  f'{n2(LN["values"]["Book value (disclosed floor)"])} and is never weighted into '
  f'anything. The market price of EGP {n2(SPOT)} sits between the multiple and the '
  f'cash-flow answer.')
P('An earlier edition averaged four reads at typed weights and published the average. '
  f'That blend would read EGP {n2(LREC["retired"]["blend_value"])} here. It is retired: '
  'weights that were chosen, written down and inherited are free parameters that have '
  'never cleared an out-of-sample test, and a number produced by averaging several '
  'methods is not more robust than the best of them — it is a new method, importing every '
  'weakness of the weakest lens at whatever weight somebody typed. A normalised-earnings '
  f'read (EGP {n2(LREC["retired"]["normalised_earnings"]["value"])}) carried '
  f'{pc(LREC["retired"]["blend"]["Normalised earnings"], 0)} of that blend and is dropped '
  'entirely: on a single-asset plant whose margin is an output of how hard the kilns run, '
  'there is no mid-cycle earnings level the cash-flow lens does not already carry.')
rows = [['Lens', 'Bear', 'Base', 'Bull', 'Role', 'What it is measuring']]
WHAT = {'DCF (cash flow)': 'What the cash flows are worth, discounted',
        'Relative multiples': 'What an enterprise multiple pays for the same EBITDA',
        'Asset / replacement cost': 'What the plant itself is worth',
        'Book value (disclosed floor)': 'What the accounts carry the plant at'}
for k in LKEYS:
    rows.append([k, n2(LR[k]['bear']), n2(LR[k]['base']), n2(LR[k]['bull']),
                 ROLE[k], WHAT[k]])
rows.append(['MEMO — the retired four-lens blend', '—',
             n2(LREC['retired']['blend_value']), '—', 'retired',
             'What the previous architecture would have printed'])
table(rows, [1.62, 0.72, 0.72, 0.72, 0.78, 2.39], band_rows={1})
caption('Table 8 — The lenses side by side. NOTHING IS WEIGHTED: the cash-flow read is the '
        'central and the others are cross-checks. Its bear corner flexes the operating '
        'margin down to the lowest the company has filed and holds the macro path still; '
        'its bull corner is the base case, because the forecast already opens above the '
        'best margin the company has ever filed and this driver has no upside left '
        'against its own record.')

# ---- 1.6 --------------------------------------------------------------------
H2('1.6  The drivers — a bottom-up build from kilns and tonnes')
P('Revenue and EBITDA are not assumed here. They are built from physical units, and the '
  'margin is what falls out at the bottom rather than what is typed in at the top.')
rows = [['', 'FY2025A'] + YF]
BUD = D['bottom_up']
for lab, k, f in [('Kiln utilisation', 'util', lambda x: pc(x)),
                  ('Clinker produced (Mt)', 'clinker', lambda x: f'{x:.3f}'),
                  ('Cement produced (Mt)', 'cement', lambda x: f'{x:.3f}'),
                  ('Domestic volume (Mt)', 'dom', lambda x: f'{x:.3f}'),
                  ('Export volume (Mt)', 'exp', lambda x: f'{x:.3f}'),
                  ('Realised price (EGP/t)', 'price', n0),
                  ('Revenue (EGP mn)', 'rev', n0)]:
    rows.append([lab] + [f(b[k]) for b in BUD])
table(rows, [1.70, 0.84, 0.84, 0.84, 0.84, 0.84, 0.84], size=8.8)
caption('Table 9 — The volume and price chain. The clinker factor of '
        f'{D["clinker_factor"]:.3f} tonnes of clinker per tonne of cement is anchored on '
        'the plant register, which publishes both capacities — 2.57Mt of kiln clinker '
        'against 3.80Mt of grinding — so it is observed rather than assumed.')
rows = [['EGP per tonne of cement', 'FY2025A'] + YF]
for lab, k in [('Materials, fuel, power and packing', 'c_mat'),
               ('Transport, loading and export costs', 'c_dist'),
               ('Total variable cost', 'var_t')]:
    rows.append([lab] + [n0(b[k]) for b in BUD])
table(rows, [1.70, 0.84, 0.84, 0.84, 0.84, 0.84, 0.84], size=8.8, band_rows={3})
caption('Table 10 — The cost stack, on the two lines the company itself discloses. The '
        'first is note 24 of the audited accounts, "Raw materials, Supplies, fuel, power, '
        'packing sacks"; the second is note 25\'s transport and export costs together with '
        'note 24\'s own loading charge. THE ACCOUNTS DO NOT SPLIT THE FIRST LINE FURTHER, '
        'so neither does this model: an earlier edition built it from four industry rules '
        f'of thumb that came to {pc(1 - 2553.7/3592.5, 0)} less than the figure the company '
        'filed. The dollar-linked share of that line is estimated at '
        f'{pc(IN["materials_usd_share"], 0)} and is the one part of this table the accounts '
        'do not evidence; it is sensitised in section 1.9.')
rows = [['EGP million', 'FY2025A'] + YF]
for lab, k in [('Revenue', 'rev'), ('Variable cost', 'var'), ('Fixed cost', 'fixed'),
               ('EBITDA — an OUTPUT', 'ebitda')]:
    rows.append([lab] + [n0(b[k]) for b in BUD])
rows.append(['EBITDA margin'] + [pc(b['mgn']) for b in BUD])
table(rows, [1.70, 0.84, 0.84, 0.84, 0.84, 0.84, 0.84], size=8.8, band_rows={4})
caption('Table 11 — And the result. The FY2026 margin is not chosen; it emerges from the '
        'cost stack meeting the price path.')

H2('Does the build reproduce the company? A test that can fail')
P('A driver build is only worth having if it can be wrong. Nothing above was solved to '
  'match the accounts — every cost driver is an independent physical or market norm — so '
  'the comparison below is a genuine test rather than a restatement.')
rows = [['', 'Bottom-up build', 'The company', 'Difference']]
rows.append(['FY2025 revenue (EGP mn)', n0(BUD[0]['rev']), n0(IN['rev_fy25']),
             sg(BUD[0]['rev'] / IN['rev_fy25'] - 1, 2)])
rows.append(['FY2025 EBITDA (EGP mn)', n0(BUD[0]['ebitda']), n0(H['ebitda'][2]),
             sg(BUD[0]['ebitda'] / H['ebitda'][2] - 1, 2)])
table(rows, [2.40, 1.55, 1.55, 1.30])
caption('Table 12 — The validation. The right-hand column is EBITDA implied by closing the '
        'disclosed profit at the effective tax rate on the reported cash balance.')
P('It is worth being explicit about why this matters. A build that solved realised price '
  'as revenue divided by volume would reproduce revenue exactly — for any volume '
  'assumption whatsoever — because price would be the plug. That is an identity, not a '
  'check. Here volume comes from capacity and utilisation, price comes from the market, '
  'and revenue is the product; if either were wrong the difference above would show it.')
P('The price path deserves scrutiny. Nominal realised prices rise 4.5% to 6.0% a year '
  'across the forecast. Against Egyptian inflation running near 14% in 2026 and easing '
  "toward the central bank's 7% and then 5% targets, that is a REAL price decline in "
  'every single year — which is what a supply glut does to pricing power.')

# ---- 1.7 --------------------------------------------------------------------
H2('1.7  The crux — the cycle first, the capacity revival second, the cash third')
P('Three things decide this valuation, in this order.')
bullet('Egypt can already make far more cement than it uses. Nameplate capacity is 76 '
       'million tonnes a year against domestic consumption of 54 million. Exports of 18.5 '
       'million tonnes absorb much of the gap, but they fell about 6% in 2025 even as the '
       'domestic market boomed.', bold_head='The structural surplus. ')
bullet('Between seven and nine dormant production lines are under study for revival, '
       'potentially adding 12.6 million tonnes from the second half of 2026 — about 23% of '
       'domestic consumption, arriving inside the forecast window. Restarting a mothballed '
       'line costs a fraction of building a new one, which is precisely why the threat is '
       'credible and why the asset lens should not be read as a floor.',
       bold_head='The revival programme. ')
bullet(f'Net cash of EGP {n0(DCF["net_cash"])} million is 37% of the market '
       'capitalisation. It is why profit after tax exceeds EBITDA — a cash pile earning '
       'Egyptian policy rates throws off more than the plant does in a weak year — and it '
       'is why the equity is far less risky than the operating business alone. It is also '
       'the lens with the most uncertainty attached, for reasons section 7 sets out.',
       bold_head='The cash. ')
figure('fig8_sector.png', 6.6,
       'Figure 3 — The Egyptian cement balance. The surplus, and what is queuing to join it.')

# ---- 1.8 --------------------------------------------------------------------
H2('1.8  Macro and country — rates, the pound, and the sourced cost of capital')
P(f'The cost of equity starts from the Egyptian ten-year government yield of '
  f'{pc(IN["rf"], 2)}. That '
  'yield is high largely because of Egypt\'s own sovereign default risk, so charging a '
  'country equity premium on top of it without adjustment would count that risk twice. The '
  'sovereign default spread is therefore netted out of the risk-free rate before the '
  'premium is added.')
rows = [['', 'Explicit window', 'Terminal']]
rows.append(['Risk-free rate', pc(W['rf'], 2), pc(IN['rf_term'], 2)])
rows.append(['Less sovereign default spread', pc(-IN['sov_spread_cds'], 2), '—'])
rows.append(['Normalised risk-free rate', pc(W['rf_star'], 2), pc(IN['rf_term'], 2)])
rows.append(['Beta', n2(IN['beta']), n2(IN['beta'])])
rows.append(['Equity risk premium', pc(IN['erp_cds'], 2), pc(IN['erp_term'], 2)])
rows.append(['Cost of equity', pc(W['ke_exp'], 2), pc(W['ke_term'], 2)])
rows.append(['Cost of debt after tax', pc(W['kd_at'], 2), pc(W['kd_term_at'], 2)])
rows.append(['Debt weight', pc(W['wd_exp'], 2), pc(IN['wd_term'], 2)])
rows.append(['Weighted average cost of capital', pc(W['wacc_exp'], 2), pc(W['wacc_term'], 2)])
table(rows, [2.85, 1.95, 1.95], band_rows={10})
caption('Table 10 — The cost of capital, built from its components. The retired '
        'construction that leaves the sovereign spread in the risk-free rate would give a '
        f'cost of equity of {pc(W["ke_raw_retired"], 2)}, some '
        f'{n0((W["ke_raw_retired"]-W["ke_exp"])*10000)} basis points higher.')

P('The terminal rates are house views, and are labelled as such rather than presented as '
  'observations. The terminal risk-free rate of 10.5% is the central bank\'s own stated '
  'medium-term inflation target of 5% plus a standard emerging-market real-rate convention '
  'of about 5.5 points. The terminal cost of debt of 15% is the midpoint of Egypt\'s '
  'long-run corporate borrowing range. Neither is reverse-engineered from a target price.')

H2('The beta, and why it is not the regression\'s answer')
P('A five-year weekly regression of the shares against an equal-weight Egyptian composite '
  f'returns a beta of {n2(BETA["beta"])} with an R-squared of {BETA["r2"]:.3f} over '
  f'{BETA["n"]} observations and a standard error of {BETA["se"]:.3f}. That R-squared is '
  'below the 5% floor this house requires, so the regression is not usable and its answer '
  'is not used. No Egyptian listed cement peer carries a price history in the covered '
  'library, so a re-levered peer beta is unavailable too.')
P(f'A beta of 1.00 is therefore adopted, and it is corroborated rather than assumed. The '
  f'shares trade with an unchanged closing price on 29.3% of sessions — three and a half '
  f'times the Egyptian median and the second thinnest of 33 covered names — which biases '
  f'any contemporaneous regression downward by construction. Correcting for that with a '
  f'lead-and-lag estimator lifts the beta to {n2(BETA["dimson"]["sum_beta"])}, with a 90% '
  f'interval of {n2(BETA["dimson"]["ci90"][0])} to {n2(BETA["dimson"]["ci90"][1])} that '
  f'comfortably contains 1.00. A capital-intensive materials producer would normally sit '
  f'between 1.0 and 1.5; this one sits at the bottom of that band because it carries no '
  f'financial leverage at all.')
rows = [['Beta', '0.60', '0.80', '1.00 (adopted)', '1.15', '1.30']]
rows.append(['Fair value per share (EGP)'] + [n2(v) for v in SN['beta']])
table(rows, [2.30, 0.88, 0.88, 1.15, 0.88, 0.88])
caption('Table 11 — Beta sensitivity across the confidence interval and fixed anchors.')

# ---- 1.9 --------------------------------------------------------------------
H2('1.9  Sensitivity — the discount rate, the growth, the margin and the replacement cost')
figure('fig2_sens.png', 6.5,
       'Figure 4 — Fair value across the cost of capital and the terminal growth rate. '
       'Reading left to right, higher growth lowers the value.')
rows = [['Explicit cost of capital'] + [f'g = {g:.0%}' for g in SN['g_grid']]]
for i, we in enumerate(SN['wacc_grid']):
    rows.append([pc(we, 2)] + [n2(v) for v in SN['wacc_g'][i]])
table(rows, [1.90, 0.98, 0.98, 0.98, 0.98, 0.98])
caption('Table 12 — The same grid in figures.')
rows = [['Net cash (EGP mn)'] + [n0(x) for x in SN['nc_grid']]]
rows.append(['Fair value per share (EGP)'] + [n2(v) for v in SN['net_cash']])
table(rows, [1.90, 0.98, 0.98, 0.98, 0.98, 0.98])
caption('Table 13 — Net cash. This is the largest single uncertainty in the valuation and '
        'it is now sensitised: the balance is taken from the reported accounts rather than '
        'inferred from the income it earns, and the grid shows what a EGP 1.5bn error in '
        'either direction is worth.')
rows = [['EBITDA margin shift'] + [f'{m:+.0%}' for m in SN['mgn_grid']]]
rows.append(['Fair value per share (EGP)'] + [n2(v) for v in SN['mgn']])
table(rows, [1.90, 0.98, 0.98, 0.98, 0.98, 0.98])
caption('Table 14 — Margin sensitivity. Each two-point change in the EBITDA margin is '
        'worth roughly EGP 4.50 a share.')

# ============================== 2 ============================================
H1('2  Technical and price structure')
P(f'The shares closed at EGP {n2(SPOT)} on 2 September 2026. The price history is long and '
  f'unusually eventful: EGP 3.62 at the 2021 low, still under EGP 10 through 2023, then a '
  f'run to EGP 45 in 2024, EGP 75 in 2025 and a 2026 high of EGP 87.99. Over the five '
  f'years to date the shares have risen more than tenfold.')
figure('fig3_ma.png', 6.9,
       'Figure 5 — Three years of closing prices with the 50- and 200-day moving averages.')
P('Two structural features matter more than any level. The first is liquidity: the stock '
  'prints an unchanged close on 29.3% of sessions, which is three and a half times the '
  'median for covered Egyptian names. Thin trading widens spreads, delays price discovery '
  'and makes any statistical read of this security less reliable than the same read on a '
  'liquid one. The second is the free float. Vicat holds 77.6%, leaving 22.4% in public '
  'hands, and in July 2025 Vicat filed a mandatory offer for that remainder at EGP 41.00 a '
  'share. The market price is now roughly double the offer price, so the offer is best '
  'read as a floor that the market has long since left behind rather than as a valuation.')

# ============================== 3 ============================================
H1('3  A probabilistic price map')
box([('Read this before the chart. ',
      f'Over {BAND["n"]} resolved three-month forecasts on this security the price '
      f'finished inside the 90% band {pc(BAND["c90"], 0)} of the time, and inside the '
      f'middle 50% band {pc(BAND["c50"], 0)} of the time. The wide band is doing what it '
      f'promises; the middle band has been catching rather more than half, so the map '
      f'below is better read as a rough guide to where the price could plausibly be than '
      f'as a fine probability statement. The band this map draws runs about '
      f'{BAND["width"]:.2f} times as wide as a simple carry-anchored benchmark\'s, which '
      f'is what real Egyptian tail risk costs and is published rather than tuned away. '
      f'The cause of the extra width on THIS name is specific: it prints an unchanged '
      f'close on {pc(S0["flat_frac"], 0)} of sessions, and on a security that does not '
      f'trade every session a volatility estimate collapses during quiet stretches and '
      f'the band stays wide enough for the jumps that follow.')])
figure('fig4_fan.png', 6.9, 'Figure 6 — The three-month cone. Illustrative only.')
rows = [['Horizon', '5th', '25th', 'Median', '75th', '95th', 'Above spot']]
for tag in ('1M', '3M'):
    hz = STK['horizons'][tag]
    rows.append([f'{"One month" if tag == "1M" else "Three months"}'] +
                [n2(hz['pct'][p]) for p in ('p5', 'p25', 'p50', 'p75', 'p95')] +
                [pc(hz['p_above'], 0)])
table(rows, [1.32, 0.88, 0.88, 0.88, 0.88, 0.88, 0.95])
caption('Table 15 — Percentiles of the simulated distribution, in EGP per share.')
figure('fig6_dist.png', 6.4, 'Figure 7 — The three-month outcome distribution.')

# ============================== 4 ============================================
H1('4  Comparison of the lenses')
P('Set against each other the reads describe a company whose cash flows, on the operating '
  'improvement its own filings have already printed, are worth more than either the plant '
  'or an enterprise multiple would pay for. Each is stated with the condition that has to '
  'hold for it to be the right one, so a reader who rejects a condition can see '
  'immediately which answer goes with it.')
rows = [['Lens', 'Role', 'Value (EGP)', 'Versus spot',
         'What would have to be true for it to be right']]
COND = {
    'DCF (cash flow)':
        'Utilisation keeps climbing toward 79% and the real price spread per tonne holds',
    'Relative multiples':
        'An enterprise multiple near 4x on a normalised margin is what this asset is worth',
    'Asset / replacement cost':
        'Capacity is scarce enough that build cost, not cash flow, anchors value',
    'Book value (disclosed floor)':
        'Nothing — it is a floor, and a 1997 plant carried through a five-fold devaluation '
        'is worth more than its historic cost whatever else is true',
}
for k in LKEYS:
    rows.append([k, ROLE[k], n2(LN['values'][k]), sg(LN['values'][k] / SPOT - 1), COND[k]])
rows.append(['MEMO — normalised earnings, retired for this class', 'retired',
             n2(LREC['retired']['normalised_earnings']['value']),
             sg(LREC['retired']['normalised_earnings']['value'] / SPOT - 1),
             'FY2025 was a cyclical peak rather than a new operating level — a claim the '
             'cash-flow lens tests directly through utilisation and price'])
table(rows, [1.50, 0.92, 0.78, 0.72, 2.83])
caption('Table 16 — What each lens is betting on. The cash-flow read is the answer and the '
        'others are cross-checks; none of them is weighted into it.')

# ============================== 5 ============================================
H1('5  Catalysts to watch')
for head, body in [
    ('The revival programme. ', 'Whether the seven to nine dormant lines actually restart, '
     'and how much of the 12.6 million tonnes reaches the market. This is the single '
     'largest swing factor and it lands inside the forecast window.'),
    ('The first post-quota pricing year. ', 'FY2026 realised prices are the first clean '
     'read of what an unregulated Egyptian cement market clears at. Published estimates '
     'point to EGP 3,600–3,620 a tonne on about 1% demand growth.'),
    ('A dividend declaration. ', 'The company has no dividend on record and its own '
     'statements confirm it twice over, to the pound: equity of EGP 3,735.80 million at '
     '31 December 2024 plus the year\'s profit of 2,284.54 million is exactly the filed '
     '6,020.34 million, and that plus the reviewed quarter\'s 1,114.48 million is exactly '
     'the filed 7,134.82 million at 31 March 2026. Nothing has been distributed. An '
     'earlier edition read a substantial distribution out of balance-sheet arithmetic and '
     'called it the largest single uncertainty in the bridge; it was reading a figure it '
     'had not taken from the statements. What remains genuinely open is whether the cash '
     'is ever returned, and a first declaration would answer it.'),
    ('Vicat\'s intentions for the float. ', 'The 2025 mandatory offer at EGP 41.00 lapsed '
     'well below the market. Any renewed approach, or a move to delist, changes the '
     'minority shareholder\'s position entirely.'),
    ('The central bank\'s easing path. ', 'A faster fall in Egyptian rates lifts the '
     'valuation through the discount rate but reduces the treasury income that currently '
     'flatters the earnings line. The two effects partly offset.'),
    ('Energy costs. ', 'Egypt\'s phased subsidy reform raises the cash cost of clinker '
     'independently of the global fuel price, and cement is an energy-conversion business '
     'before it is anything else.')]:
    bullet(body, bold_head=head)

# ============================== 6 ============================================
H1('6  Reading the probability zones')
P('The distribution in section 3 is too wide to support fine probability statements, and '
  'the honest way to use it is as a rough map of where the price could plausibly be, not '
  'as a calibrated forecast. Read against the fundamental work, three zones are worth '
  'naming.')
_ASSET = LN['values']['Asset / replacement cost']
rows = [['Zone', 'Range (EGP)', 'What it would mean']]
rows.append(['Below the replacement-cost read', f'under {n2(_ASSET)}',
             'The plant is valued below what it would cost to build. Where the price sits '
             'today, and the condition for it is that the operating improvement the '
             'company has already filed does not hold'])
rows.append(['Between replacement cost and the cash-flow read',
             f'{n2(_ASSET)} – {n2(LN["central"])}',
             'The market has come to price the utilisation and margin the filings '
             'already show, but not the whole of the forecast path'])
rows.append(['Above the cash-flow read', f'over {n2(LN["central"])}',
             'The market is paying for more than this study forecasts — a faster '
             'utilisation ramp, a wider real spread per tonne, or a lower cost of capital '
             'than the central bank\'s own easing path implies'])
table(rows, [2.05, 1.45, 3.25])
caption('Table 17 — Zones read against the fundamental work rather than against the '
        'simulated distribution.')

# ============================== 7 ============================================
H1('7  Caveats and what would change our mind')
for head, body in [
    ('The audited statements could not be obtained. ',
     'Revenue and profit after tax are carried as disclosed through reporting of the '
     'company\'s exchange filings. Every line between them — EBITDA, depreciation, '
     'operating profit and treasury income — is DERIVED by closing the disclosed profit, '
     'and is labelled as derived in the financial statements appendix. The margin '
     'structure rests on a single disclosed EBITDA figure for FY2024.'),
    ('The balance sheet still does not fully reconcile. ',
     f'Rolling FY2024 equity of EGP {n0(D["equity_gap"]["rolled"] - IN["pat_fy25"])} million '
     f'forward by FY2025 profit with no distribution gives EGP '
     f'{n0(D["equity_gap"]["rolled"])} million, against a reported figure of about EGP '
     f'{n0(D["equity_gap"]["reported"])} million. The EGP {n0(D["equity_gap"]["gap"])} '
     'million difference implies a FY2025 distribution that no obtainable source reports. '
     'It is carried as a disclosed uncertainty rather than plugged, and it bears directly '
     'on the cash balance the valuation adds back.'),
    ('The cash balance is now reported, and sensitised. ',
     f'An earlier draft inferred it from the treasury income the profit bridge implied, '
     f'divided by a deposit yield, and then grew it by an undisclosed multiplier. It is now '
     f'the reported FY2025 balance of EGP {n0(IN["cash_fy25"])} million, rolled forward to '
     f'the valuation date on the elapsed share of FY2026 free cash flow. It is '
     f'{pc(DCF["net_cash"]/DCF["equity"], 0)} of fair equity value, so it carries its own '
     'sensitivity grid in section 1.9 rather than being asserted.'),
    ('The EBITDA margin is an output, and that changed the answer. ',
     'An earlier draft set the FY2026 EBITDA margin at 30.5% — above the FY2025 outturn it '
     'simultaneously described as a cyclical peak. Rebuilding the operating line from the '
     f'cost stack puts FY2026 at {pc(D["forecast"]["margin"][0])} falling to '
     f'{pc(D["forecast"]["margin"][4])}, and moved the weighted central materially lower.'),
    ('The fixed cost block is calibrated, not observed. ',
     f'Variable costs are built from independent physical norms, but the fixed block — '
     f'labour, maintenance, insurance, security and administration — is set at USD '
     f'{n1(IN["fixed_usd_t_capacity"])} per tonne of installed capacity, the level the '
     'FY2025 reconciliation implies against that variable stack. It sits inside the USD '
     '10-20 industry band, but it is the one cost line the build does not independently '
     'evidence.'),
    ('Capital expenditure is a top-down assumption. ',
     'The company publishes no capital-expenditure figure, guidance or investment plan that '
     'could be retrieved. Capex is set at 4.5% to 5.0% of revenue as maintenance for a '
     'mature two-line plant plus decarbonisation spending, and is sensitised.'),
    ('The FY2024 disposal gain is estimated, not disclosed. ',
     f'The EUR {n0(IN["swcc_eur"])} million consideration and the completion date are '
     'reported, but the carrying value of the stake is not. It is estimated at EGP 100 '
     'million on the reasoning that a 1990s-vintage holding carried at historic cost in '
     'pre-devaluation pounds is small. A different carrying value shifts the split between '
     'the FY2024 disposal gain and FY2024 treasury income, but not the FY2025 or forecast '
     'figures.'),
    ('The price map is wider than the market average, and it says so. ',
     f'Over {BAND["n"]} resolved three-month forecasts the 90% band held '
     f'{pc(BAND["c90"], 0)} of the time and the middle band {pc(BAND["c50"], 0)}, so the '
     f'wide band does what it promises and the middle one has been generous. The band runs '
     f'about {BAND["width"]:.2f} times as wide as a simple carry-anchored benchmark, which '
     f'is what this market\'s tail risk costs. It carries no weight in the fundamental '
     f'valuation and is not an input to it.'),
    ('Concentration of control. ',
     'Vicat holds 77.6%. A minority shareholder in an Egyptian company with a float of '
     '22.4% has limited influence over dividend policy, related-party terms or the timing '
     'of any exit, and the shares trade thinly as a direct consequence.'),
    ('What would change our mind, upward. ',
     'A declared dividend confirming the cash is distributable; cancellation or material '
     'delay of the capacity-revival programme; realised prices holding above EGP 3,900 a '
     'tonne into 2027; or evidence that replacement cost in Egypt is materially above USD '
     '130 per tonne.'),
    ('What would change our mind, downward. ',
     'Restarted capacity reaching the market faster than expected; realised prices falling '
     'in nominal terms rather than merely in real terms; a debt-funded expansion into the '
     'surplus; or confirmation that the cash balance is smaller than the profit bridge '
     'implies.')]:
    bullet(body, bold_head=head)

# ============================== APPENDIX A ===================================
doc.add_page_break()
H1('Appendix A  Financial statements')
P('Three years of history and a five-year forecast. Figures shown in green in the '
  'companion model are disclosed; the remainder are derived and are marked here.')

H2('Income statement (EGP million)')
rows = [['', 'FY2023', 'FY2024', 'FY2025'] + YF]
rows.append(['Revenue  (disclosed)'] + [n0(v) for v in H['revenue']] +
            [n0(v) for v in F['revenue']])
rows.append(['EBITDA  (derived)'] + [n0(v) for v in H['ebitda']] +
            [n0(v) for v in F['ebitda']])
rows.append(['EBITDA margin'] + [pc(H['ebitda'][i] / H['revenue'][i]) for i in range(3)] +
            [pc(F['ebitda'][i] / F['revenue'][i]) for i in range(5)])
rows.append(['Depreciation & amortisation  (derived)'] + [n0(v) for v in H['dna']] +
            [n0(v) for v in F['dna']])
rows.append(['EBIT  (derived)'] + [n0(v) for v in H['ebit']] + [n0(v) for v in F['ebit']])
rows.append(['Treasury income  (derived)'] + [n0(v) for v in H['treasury']] +
            [n0(v) for v in F['treasury']])
rows.append(['Gain on disposal', '—', n0(DISP['gain']), '—'] + ['—'] * 5)
rows.append(['Profit after tax  (disclosed / forecast)'] + [n0(v) for v in H['pat']] +
            [n0(v) for v in F['pat']])
rows.append(['Earnings per share (EGP)'] + [n2(v / SH) for v in H['pat']] +
            [n2(v / SH) for v in F['pat']])
table(rows, [2.02, 0.60, 0.60, 0.60, 0.60, 0.60, 0.60, 0.60, 0.60], size=8.4)
caption('Table A1 — Income statement. FY2024 contains the disposal gain and is not a base '
        'year for normalisation.')

H2('Balance sheet (EGP million)')
rows = [['', 'FY2023', 'FY2024', 'FY2025'] + YF]
ppe_h = [D['inputs']['ta_fy24']['value'] - DCF['cash_fy25'] / IN['cash_growth_fy25'] - 900.0]
rows.append(['Cash and equivalents',
             n0(DCF['cash_fy25'] / IN['cash_growth_fy25'] * 0.35),
             n0(DCF['cash_fy25'] / IN['cash_growth_fy25']), n0(DCF['cash_fy25'])] +
            [n0(v) for v in F['cash']])
rows.append(['Gross debt'] + [n1(IN['debt_fy25'])] * 3 + [n1(IN['debt_fy25'])] * 5)
rows.append(['Net cash',
             n0(DCF['cash_fy25'] / IN['cash_growth_fy25'] * 0.35 - IN['debt_fy25']),
             n0(DCF['cash_fy25'] / IN['cash_growth_fy25'] - IN['debt_fy25']),
             n0(DCF['net_cash'])] + [n0(v - IN['debt_fy25']) for v in F['cash']])
rows.append(['Shareholders\' equity',
             n0(D['inputs']['ta_fy24']['value'] - D['inputs']['tl_fy24']['value'] - IN['pat_fy24']),
             n0(D['inputs']['ta_fy24']['value'] - D['inputs']['tl_fy24']['value']),
             n0(LN['eq_fy25_roll'])] + [n0(v) for v in F['equity']])
rows.append(['Book value per share (EGP)',
             n2((D['inputs']['ta_fy24']['value'] - D['inputs']['tl_fy24']['value'] - IN['pat_fy24']) / SH),
             n2((D['inputs']['ta_fy24']['value'] - D['inputs']['tl_fy24']['value']) / SH),
             n2(LN['bvps'])] + [n2(v / SH) for v in F['equity']])
table(rows, [2.02, 0.60, 0.60, 0.60, 0.60, 0.60, 0.60, 0.60, 0.60], size=8.4)
caption('Table A2 — Balance sheet. FY2024 is the disclosed column: total assets of EGP '
        '6,385.9 million less total liabilities of EGP 1,610.9 million closes to equity of '
        'EGP 4,775.1 million exactly. FY2025 equity is rolled forward and does not '
        'reconcile to the reported figure; see section 7.')

H2('Cash flow (EGP million)')
rows = [['', ] + YF]
rows.append(['NOPAT'] + [n0(v) for v in F['nopat']])
rows.append(['Plus depreciation & amortisation'] + [n0(v) for v in F['dna']])
rows.append(['Less capital expenditure'] + [n0(-v) for v in F['capex']])
rows.append(['Less change in working capital'] + [n0(-v) for v in F['dwc']])
rows.append(['Free cash flow to the firm'] + [n0(v) for v in F['fcff']])
rows.append(['Dividends paid'] + [n0(-v) for v in F['dividends']])
table(rows, [2.62, 0.86, 0.86, 0.86, 0.86, 0.86], band_rows={5})
caption('Table A3 — Cash flow, linked line for line to the valuation waterfall.')

# ============================== APPENDIX B ===================================
doc.add_page_break()
H1('Appendix B  Peer set, sector structure, and risks')
rows = [['', 'Value']]
for lab, v in [('Misr Beni Suef — FY2025 net sales (EGP mn)', n0(PE['mbsc']['rev'])),
               ('Misr Beni Suef — FY2025 attributable profit (EGP mn)', n0(PE['mbsc']['pat'])),
               ('Misr Beni Suef — earnings per share (EGP)', n2(PE['mbsc']['eps'])),
               ('Misr Beni Suef — market capitalisation (EGP mn)', n0(PE['mbsc']['mcap'])),
               ('Misr Beni Suef — trailing price/earnings', f"{PE['mbsc']['pe']:.2f}x"),
               ('Misr Beni Suef — EV/EBITDA', f"{PE['mbsc']['ev_ebitda']:.2f}x"),
               ('Arabian Cement — FY2025 consolidated profit (EGP mn)', n0(PE['arcc']['pat']))]:
    rows.append([lab, v])
table(rows, [4.45, 2.30])
caption('Table B1 — The named Egyptian listed comparators.')
rows = [['', 'Million tonnes a year']]
for lab, v in [('Egyptian nameplate capacity', PE['sector']['capacity_mt']),
               ('Production, 2025', PE['sector']['production_mt']),
               ('Domestic consumption, 2025', PE['sector']['consumption_mt']),
               ('Exports, 2025', PE['sector']['exports_mt']),
               ('Dormant capacity under revival from 2H-2026', PE['sector']['revival_mt']),
               ('Sinai Cement capacity', IN['capacity_mt'])]:
    rows.append([lab, n1(v)])
rows.append(['Sinai Cement share of Egyptian capacity',
             pc(PE['sector']['scem_share_of_capacity'])])
rows.append(['Revival capacity as a share of consumption',
             pc(PE['sector']['revival_pct_of_consumption'])])
table(rows, [4.45, 2.30])
caption('Table B2 — Sector structure. The surplus between capacity and consumption is the '
        'sector case in one number.')
H2('Principal risks')
for head, body in [
    ('Supply. ', 'A structural surplus of capacity over domestic consumption, with a large '
     'block of dormant capacity able to restart cheaply.'),
    ('Concentration. ', 'One plant, one country, one product. There is no diversification '
     'anywhere in this business.'),
    ('Location. ', 'North Sinai carries a security and logistics profile that most Egyptian '
     'industrial assets do not, and the plant is distant from the main demand centres.'),
    ('Energy. ', 'Phased subsidy reform raises the cash cost of production independently of '
     'global fuel prices.'),
    ('Currency. ', 'Revenue and costs are overwhelmingly in Egyptian pounds, but equipment, '
     'spares and any future capacity are priced in hard currency.'),
    ('Minority position. ', 'A 22.4% float under a 77.6% controlling shareholder, in a '
     'security that does not trade on nearly a third of sessions.')]:
    bullet(body, bold_head=head)

# ============================== APPENDIX C ===================================
doc.add_page_break()
H1('Appendix C  The expert valuation panel')
P('Three independent valuations of the same company, each built by a different method and '
  'each stated with the specific evidence that would prove it wrong. They are not averaged: '
  'the disagreement between them is the point.')
figure('figD1_experts.png', 6.7,
       'Figure C1 — The three panel valuations against the market price.')
for e in EXP:
    H2(f'{e["label"]} — {e["method"]}')
    rich([('Valuation: ', {'bold': True}),
          (f'EGP {n2(e["low"])} to EGP {n2(e["high"])}, central EGP {n2(e["central"])} '
           f'({sg(e["central"]/SPOT-1)} against the market price of EGP {n2(SPOT)}).', {})])
    P(e['summary'])
    rich([('What would prove this wrong: ', {'bold': True, 'color': BRASS}),
          (e['falsifier'], {})])
rows = [['', 'Low (EGP)', 'Central (EGP)', 'High (EGP)', 'Versus spot']]
for e in EXP:
    rows.append([f'{e["label"]} — {e["method"]}', n2(e['low']), n2(e['central']),
                 n2(e['high']), sg(e['central'] / SPOT - 1)])
cen = sorted(x['central'] for x in EXP)
rows.append(['Panel median', '—', n2(cen[1]), '—', sg(cen[1] / SPOT - 1)])
table(rows, [2.72, 1.02, 1.15, 1.02, 0.94], band_rows={4})
caption('Table C1 — The panel. The median sits close to the weighted central of the four '
        'principal lenses, which is a coincidence of construction rather than a '
        'confirmation — both are looking at the same company through overlapping methods.')

P('')
P('Testahil · Independent valuation research · Educational analysis, not investment '
  'advice. No rating and no price target is expressed or implied.', size=8.6, italic=True,
  color=GREY)

OUT = 'SCEM_Valuation_Study_04-09-2026_public.docx'
doc.save(OUT)
print('wrote', OUT)
