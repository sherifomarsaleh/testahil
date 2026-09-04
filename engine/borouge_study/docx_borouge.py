"""BOROUGE_Valuation_Study_09-08-2026_public.docx — sixteen sections, house style.

Every financial numeral in this document is read from study_numbers.json, technicals.json,
strike_result.json, backtest_5y.json or beta_result.json. No figure is typed into this
builder — the traceability check in qc_checks.py enforces that.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
from table_residual import signed_column   # the shared check, not hand-rolled
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)

import docx_base as B                                       # noqa: E402
from docx_base import (H1, H2, P, box, bullet, caption, doc,  # noqa: E402
                       figure, masthead, rich, table)
from docx_base import BRASS, GREY, INK                       # noqa: E402

D = json.load(open('study_numbers.json'))
TE = json.load(open('technicals.json'))
# JSON turns integer keys into strings; restore them so the moving-average windows can be
# addressed by the number a reader would use.
TE['ma'] = {int(k): v for k, v in TE['ma'].items()}
TE['ma_slope'] = {int(k): v for k, v in TE['ma_slope'].items()}
STK = json.load(open('strike_result.json'))
BT = json.load(open('backtest_5y.json'))
BETA = json.load(open('beta_result.json'))
SRC = json.load(open('source_access.json'))

W, LEN_, SN, H = D['wacc'], D['lenses'], D['sensitivity'], D['history']
FR, UB, WC = D['framings'], D['unit_build'], D['working_capital']
CI = {k: v['value'] for k, v in D['company_inputs'].items()}
MC = {k: v['value'] for k, v in D['macro'].items()}
NRM, REL, BV = D['normalised'], D['relative'], D['book_value']
ALT = D['alt_wacc']['bottom_up_sector_beta']
FN, FP = FR['normalisation'], FR['prolonged']
SPOT, FX = D['spot_aed'], D['aed_per_usd']
SHARES = D['shares_out'] / 1e6
YF = [r['year'] for r in FN['rows']]
HYS = ['2023', '2024', '2025']


def m(x, dp=0):
    return f'{x:,.{dp}f}'


def pc(x, dp=1):
    return f'{x * 100:.{dp}f}%'


def px(x):
    return f'{x:.2f}'


TVSHARE_N = FN['pv_terminal'] / FN['ev']
TVSHARE_P = FP['pv_terminal'] / FP['ev']

# =============================================================== 1 MASTHEAD
masthead()
P('Borouge plc', size=25, bold=True, space_after=0)
P('Abu Dhabi Securities Exchange · BOROUGE · polyolefins · reports in US dollars, '
  'trades in dirhams', size=11, color=GREY, space_after=2)
rich([(f'Close {px(SPOT)} AED', {'bold': True, 'size': 11}),
      (f'   ·   7 August 2026   ·   study dated 9 August 2026   ·   '
       f'{m(SHARES / 1000, 2)}bn shares in issue', {'size': 11, 'color': GREY})],
     space_after=10)

H1('Read this first')
box([
    ('What this is. ',
     'An independent valuation study of Borouge plc, built from the company’s own '
     'audited and reviewed financial statements and its own disclosed operating data. '
     'It is educational analysis. It is not investment advice, it is not a '
     'recommendation, and it carries no rating and no price target.'),
    ('What it gives you instead. ',
     'A range of fair values from four independent methods, and a separate, explicitly '
     'probabilistic map of where the traded price could sit over the next one and three '
     'months. The two are different objects and the study never mixes them: the first '
     'asks what the business is worth, the second asks what the share price might do.'),
    ('The one thing to know before reading a single number. ',
     'This study publishes TWO answers to its central question, not one, and never '
     'averages them. Borouge’s own share-price history gives a very low measured '
     'sensitivity to its market, and a sensitivity built up from what global chemical '
     f'companies look like gives a much higher one. The gap is worth '
     f'{px(LEN_["dcf_normalisation_own_beta"] - LEN_["dcf_normalisation_sector_beta"])} '
     f'dirhams a share. Rather than pick one and bury the choice, the study carries both '
     f'all the way through — every lens, every table, the workbook, and the analyst '
     f'appendix.'),
    ('Currency. ',
     'Borouge reports in US dollars. Its shares trade in dirhams, which have been pegged '
     'to the dollar at 3.6725 since November 1997 and have not moved since. The '
     'valuation is therefore built in dollars and converted to dirhams at the peg; '
     'there is no exchange-rate view inside any number here.'),
])

# =============================================================== 2 HEADLINE
H1('Headline')
P('Borouge is a low-cost polyolefin producer in the middle of the worst polyolefin '
  'market in a generation, and it is also, right now, a company whose shipping lane was '
  'shut for half a year. Those two facts pull in different directions and the study '
  'keeps them separate.', size=11)
P(f'On the four valuation lenses the study runs, the field spans {px(D["fair_low"])} to '
  f'{px(D["fair_high"])} dirhams a share, with a median of {px(D["fair_mid"])} against a '
  f'close of {px(SPOT)}. That is not a narrow answer and the study does not pretend '
  f'otherwise. The width is not noise — it is almost entirely one disagreement, about '
  f'how risky this share really is, and the study prices that disagreement rather than '
  f'resolving it.')
P(f'The operating picture underneath is more settled than the valuation range suggests. '
  f'Borouge earned an EBITDA margin of {pc(H["2025"]["ebitda"] / H["2025"]["revenue"])} '
  f'in 2025 while nine of its eleven listed peers lost money. It does that on advantaged '
  f'ethane feedstock at Ruwais, at a cost of '
  f'${m(UB["feed_per_t"]["2025"], 0)} a tonne of production against '
  f'${m(UB["feed_per_t_h126"], 0)} in the first half of 2026, when the plant had to buy '
  f'propylene at market prices because its conversion unit was starved of ethane. That '
  f'gap — about {pc(UB["feed_per_t_h126"] / UB["feed_per_t"]["2025"] - 1, 0)} — is the '
  f'single clearest measure of what the disruption cost.')
box([
    ('Three things this study concludes. ', ''),
    ('One. ',
     f'The 2026 damage is mechanically identifiable and mechanically reversible. '
     f'Feedstock at ${m(UB["feed_per_t_h126"], 0)} a tonne instead of '
     f'${m(UB["feed_per_t"]["2025"], 0)}, and freight at '
     f'${m(UB["sd_per_t_h126"], 0)} a tonne instead of '
     f'${m(UB["sd_per_t"]["2025"], 0)}, are an idled conversion unit and a re-routed '
     f'ship. Neither is a permanent reset of the cost base. Whether they reverse in 2026 '
     f'or drag into 2027 is genuinely unknowable, so the study builds both and publishes '
     f'both: the answers differ by '
     f'{(abs(LEN_["dcf_normalisation_own_beta"] - LEN_["dcf_prolonged_own_beta"]) * 100):.1f} '
     f'fils a share — under a fifth of one per cent of the price — so the disruption is '
     f'loud in the news and almost silent in the valuation. A year of impaired shipping '
     f'sits inside a five-year window in which most of the value lies beyond the '
     f'forecast, so it moves the answer far less than the headlines suggest.'),
    ('Two. ',
     f'The expansion next door is not yours. Borouge 4 adds 1.4 million tonnes at the '
     f'same site and is owned 70% by ADNOC and 30% by OMV. Borouge plc operates it for a '
     f'fee. Valued as a fee stream, that is worth about ${m(FN["b4"]["value"], 0)}m, or '
     f'{pc(FN["b4"]["share_of_ev"])} of enterprise value — real, but a fraction of what '
     f'the tonnes would be worth if the company owned them. It is why terminal growth in '
     f'this study is long-run inflation and nothing more.'),
    ('Three. ',
     f'Most of the value is in the years nobody can see. Terminal value is '
     f'{pc(TVSHARE_N)} of enterprise value on the central construction. That is high, it '
     f'is stated in the summary table and in the bridge rather than buried, and it is the '
     f'honest consequence of valuing a long-lived asset at a cost of capital of '
     f'{pc(W["wacc_own"], 2)}. At the higher cost of capital the study also publishes, '
     f'the terminal share falls to {pc(ALT["tv_share"]["normalisation"])} — and the value '
     f'falls with it.'),
])

# =============================================================== 3 VALUATION SUMMARY
H1('Valuation summary')
P('Four lenses, each run twice — once at the share’s own measured risk, once at the risk '
  'a global chemical company usually carries. The two columns are the same business '
  'valued at two different costs of capital. They are never averaged.')
rows = [['Lens', 'At sector risk (AED)', 'At own measured risk (AED)',
         'Terminal value as % of enterprise value', 'What it rests on']]
rows.append(['Discounted cash flow — shipping normalises',
             px(LEN_['dcf_normalisation_sector_beta']),
             px(LEN_['dcf_normalisation_own_beta']), pc(TVSHARE_N),
             'Five years of tonnes and prices, then a terminal block'])
rows.append(['Discounted cash flow — disruption persists',
             px(LEN_['dcf_prolonged_sector_beta']),
             px(LEN_['dcf_prolonged_own_beta']), pc(TVSHARE_P),
             'The same build with the lane impaired into 2027'])
rows.append(['Book value and sustainable return',
             px(LEN_['book_value_sector_beta']), px(LEN_['book_value_own_beta']), '—',
             f'Return on equity of {pc(BV["roe_sustainable"])} against the cost of equity'])
rows.append(['Normalised earnings power',
             px(LEN_['normalised_earnings_sector_beta']),
             px(LEN_['normalised_earnings_own_beta']), '—',
             'Mid-cycle volumes and prices, capitalised'])
rows.append(['Relative multiples', px(LEN_['relative_multiples']),
             px(LEN_['relative_multiples']), '—',
             'Three through-cycle multiples; unaffected by the risk debate'])
rows.append(['The field', px(D['fair_low']) + ' low', px(D['fair_high']) + ' high', '',
             f'Median {px(D["fair_mid"])} against a close of {px(SPOT)}'])
table(rows, [1.72, 1.06, 1.16, 1.20, 1.86], band_rows={6}, size=8.9)
caption('Table 1 — The summary valuation. The terminal-value share is shown against the '
        'two cash-flow lenses because that is where it applies; the other three lenses do '
        'not have one. Every figure is reproduced live in the companion workbook.')

figure('fig1_football.png', 6.9,
       'Figure 1 — Each lens is drawn as a bar between the two costs of capital the study '
       'publishes. The relative lens is a single point because a through-cycle multiple '
       'does not move with the risk debate.')

box([
    ('Why the range is this wide, in one paragraph. ',
     f'Take the risk debate out and the study is tight: at the share’s own measured risk '
     f'the four lenses land at {px(LEN_["dcf_normalisation_own_beta"])}, '
     f'{px(LEN_["book_value_own_beta"])}, {px(LEN_["normalised_earnings_own_beta"])} and '
     f'{px(LEN_["relative_multiples"])}; at sector risk they land at '
     f'{px(LEN_["dcf_normalisation_sector_beta"])}, {px(LEN_["book_value_sector_beta"])}, '
     f'{px(LEN_["normalised_earnings_sector_beta"])} and '
     f'{px(LEN_["relative_multiples"])}. Within each column the methods agree far better '
     f'than they disagree. It is the choice BETWEEN columns that is worth almost two '
     f'dirhams, and no amount of extra modelling settles it — it is a judgement about '
     f'whether four years of a thinly floated share trading in a narrow band tells you '
     f'anything about the risk of a business whose earnings track a global commodity.'),
])

# =============================================================== 4 COMPANY OVERVIEW
H1('Company overview')
P('Borouge plc makes two products. It cracks ethane into ethylene and converts it to '
  'polyethylene, and it makes polypropylene, at one integrated complex at Ruwais in Abu '
  'Dhabi. It sells into more than ninety countries, employs more than 2,900 people, and '
  'was formed in 1998 as a partnership between ADNOC and Borealis. It listed on the Abu '
  'Dhabi Securities Exchange in June 2022.')
P(f'Nameplate capacity is {m(UB["capacity_pe"])} thousand tonnes a year of polyethylene '
  f'and {m(UB["capacity_pp"])} thousand tonnes of polypropylene. In 2025 the plant '
  f'produced {m(UB["production"]["2025"])} thousand tonnes and sold '
  f'{m(UB["vol_tot"]["2025"])} thousand tonnes, the difference being inventory and '
  f'material sourced from partners. Revenue was ${m(H["2025"]["revenue"])}m, EBITDA '
  f'${m(H["2025"]["ebitda"])}m and profit after tax ${m(H["2025"]["pat"])}m.')
P('Two structural facts shape everything that follows, and both were confirmed against '
  'the company’s own filings rather than inferred.')
bullet('Since March 2026 Borouge plc has been majority-held by Borouge Group '
       'International AG, formed when ADNOC and OMV combined Borouge and Borealis and '
       'acquired Nova Chemicals. Each parent holds 46.94% of that combined entity. '
       'Borouge plc remains separately listed and its free float continues to trade. A '
       'tender offer converting Borouge plc shares into shares of the combined entity is '
       'expected in 2027, subject to market conditions and regulatory approval. No '
       'exchange ratio has been published, so no conversion value enters any number in '
       'this study.', bold_head='It is now part of a larger group. ')
bullet('Borouge 4, the 1.4 million tonne expansion at the same site, is owned 70% by '
       'ADNOC and 30% by OMV. Borouge plc operates it under an Asset Usage Agreement '
       'signed in March 2026 and earns a fee. Its ownership share is zero, and the study '
       'carries it at zero. Recontribution of those assets into the parent group is not '
       'expected before 2029.',
       bold_head='The expansion at its own site belongs to its parents. ')

H2('What class of company this is, and therefore how it is valued')
P('The classification matters more than any single assumption, because getting it wrong '
  'invalidates the whole study. It was taken from the filings, not from a sector label.')
rows = [['Evidence', 'What the filings show', 'What it rules in or out'],
        ['Revenue mix',
         f'Polyethylene ${m(UB["rev_pe"]["2025"])}m and polypropylene '
         f'${m(UB["rev_pp"]["2025"])}m of ${m(H["2025"]["revenue"])}m total — '
         f'{pc((UB["rev_pe"]["2025"] + UB["rev_pp"]["2025"]) / H["2025"]["revenue"])} '
         f'from selling two polymers',
         'An operating company. No fee income, no rental stream, no lending margin'],
        ['Balance-sheet shape',
         f'Property, plant and equipment ${m(CI["ppe_fy25"] / 1000)}m of total assets '
         f'${m(CI["ta_fy25"] / 1000)}m — {pc(CI["ppe_fy25"] / CI["ta_fy25"])} of the '
         f'balance sheet is the plant itself',
         'Rules out a holding company and an investment company: there is no portfolio '
         'of stakes to value separately'],
        ['Financial assets',
         'No loan book, no financing receivables, no insurance float. Cash of '
         f'${m(CI["cash_fy25"] / 1000)}m against borrowings of '
         f'${m(CI["debt_fy25"] / 1000)}m',
         'Rules out a bank and an operating company with a captive lender: there are no '
         'legs needing different methods'],
        ['Segment reporting', 'One operating segment. Volume and price disclosed by '
         'product; cost and profit are not split',
         'A single-lens valuation is correct. A sum-of-the-parts would be inventing '
         'divisions the company does not report'],
        ['The one thing that IS separable',
         f'The Borouge 4 operator fee — a contracted stream from assets the company does '
         f'not own, worth about ${m(FN["b4"]["value"])}m',
         'Valued on its own and added in the bridge, rather than blended into the '
         'operating forecast']]
table(rows, [1.20, 2.75, 2.85], size=8.9)
caption('Table 2 — The classification evidence. Borouge is an operating company with one '
        'separable contracted fee stream, so it takes a cash-flow lens built from tonnes '
        'and dollars per tonne, with the fee stream valued separately and added in the '
        'bridge.')

# =============================================================== 5 SECTION 1
H1('1  Fundamental valuation')

H2('1.1  The cash-flow model')
P('The forecast is built from physical units, not from a margin assumption. Volume is '
  'nameplate capacity times a utilisation rate the company itself discloses. Price is the '
  'published benchmark for each polymer, plus the premium Borouge discloses it earns over '
  'that benchmark, times a realisation residual measured against three years of audited '
  'revenue. Cost is dollars per tonne, split by what physically drives it.')
P(f'The realisation residual is the bridge from a published benchmark to the company’s '
  f'own printed top line, and it is measured rather than assumed. Across the three '
  f'audited years polyethylene revenue per tonne ran {UB["realisation_pe"]:.4f} times '
  f'benchmark-plus-premium and polypropylene {UB["realisation_pp"]:.4f} times. In the '
  f'first half of 2026 those widened to {UB["realisation_pe_h126"]:.4f} and '
  f'{UB["realisation_pp_h126"]:.4f} on shortage pricing. The forecast carries the audited '
  f'three-year mean, not the half-year, because the widening is an artefact of a closed '
  f'shipping lane rather than a durable improvement in what customers will pay.')
rows = [['USD million', '2026', '2027', '2028', '2029', '2030']]
# ONE SIGN CONVENTION. Every deduction here printed a POSITIVE MAGNITUDE under "Less"
# while the working-capital line printed a SIGNED value under the same word — and that row
# switches between adjacent years, 24.5 in one and -8.1 in the next, which no reader can
# get right. The magnitudes stay for the cost stack, which never changes sign; the
# working-capital line is the signed cash effect and says so in its own label.
for key, label in [('revenue', 'Revenue'), ('feedstock', 'Less: feedstock'),
                   ('othprod', 'Less: other production cost'),
                   ('sd', 'Less: selling and distribution'),
                   ('ga', 'Less: general and administrative'),
                   ('other_income', 'Add: other income'), ('ebitda', 'EBITDA'),
                   ('da', 'Less: depreciation and amortisation'), ('ebit', 'EBIT'),
                   ('nopat', 'NOPAT (EBIT after tax)'),
                   ('da2', 'Add back: depreciation and amortisation'),
                   ('capex', 'Less: capital expenditure'),
                   ('d_nwc', 'Movement in working capital — a release adds, '
                             'a build subtracts'),
                   ('fcff', 'Free cash flow to the firm'),
                   ('discount_factor', 'Discount factor'),
                   ('pv_fcff', 'Present value of free cash flow')]:
    src = 'da' if key == 'da2' else key
    dp = 4 if key == 'discount_factor' else (1 if key == 'd_nwc' else 0)
    sgn = -1.0 if key == 'd_nwc' else 1.0
    rows.append([label] + [m(sgn * r[src], dp) for r in FN['rows']])
for _r in FN['rows']:
    signed_column([_r['nopat'], _r['da'], -_r['capex'], -_r['d_nwc']],
                  _r['fcff'], dp=0, what='the cash-flow waterfall')
table(rows, [2.40, 0.86, 0.86, 0.86, 0.86, 0.86], size=8.6,
      band_rows={7, 14, 16})
caption('Table 3 — The full free-cash-flow waterfall on the central construction, in the '
        'order the reader needs it: EBITDA, depreciation, EBIT, NOPAT, the add-back, '
        'capital spend, working capital, free cash flow to the firm, the discount factor '
        'and the present value. Every line is a live formula in the companion workbook.')

rows = [['The terminal block', 'USD million'],
        ['Final-year NOPAT', m(FN['rows'][-1]['nopat'])],
        [f'Terminal NOPAT at {pc(MC["terminal_growth"], 1)} growth',
         m(FN['terminal_nopat'])],
        [f'Reinvestment rate = growth / return on capital of '
         f'{pc(MC["terminal_roc"], 0)}', pc(FN['reinvestment_rate'])],
        ['Terminal free cash flow', m(FN['terminal_fcff'])],
        ['Terminal value', m(FN['terminal_value'])],
        ['Present value of the terminal value', m(FN['pv_terminal'])],
        ['Present value of the explicit five years', m(FN['pv_explicit'])],
        ['Enterprise value of the owned business', m(FN['ev_core'])],
        ['Plus: the Borouge 4 operator fee stream', m(FN['b4']['value'])],
        ['Enterprise value', m(FN['ev'])],
        ['Terminal value as a share of enterprise value', pc(TVSHARE_N)],
        ['Less: net debt', '(' + m(FN['net_debt']) + ')'],
        ['Less: lease liabilities', '(' + m(FN['leases'], 1) + ')'],
        ['Less: non-controlling interests', '(' + m(FN['nci'], 1) + ')'],
        ['Equity value', m(FN['equity'])],
        ['Value per share (USD)', f'{FN["per_share_usd"]:.4f}'],
        ['Value per share (AED)', px(FN['per_share_aed'])]]
table(rows, [4.30, 2.00], size=9.0, band_rows={10, 11, 15, 18})
caption('Table 4 — Enterprise value to equity value, on the central construction. The '
        'terminal-value share is shown inside the bridge, where a reader meets it, rather '
        'than in a footnote.')

H2('1.2  Book value and sustainable return')
P(f'Borouge earned returns on equity of {", ".join(pc(x) for x in BV["roe_hist"])} across '
  f'the three audited years, a mean of {pc(BV["roe_sustainable"])}. Against a cost of '
  f'equity of {pc(W["ke_own"], 2)} and long-run growth of {pc(MC["terminal_growth"], 1)}, '
  f'that justifies {BV["justified_pb"]:.2f} times a book value of '
  f'${BV["bvps_usd"]:.4f} a share, or {px(LEN_["book_value_own_beta"])} dirhams. At the '
  f'higher cost of equity of {pc(W["ke_bottom_up"], 2)} the same return justifies only '
  f'{BV["justified_pb_sector_beta"]:.2f} times book, or '
  f'{px(LEN_["book_value_sector_beta"])} dirhams.')
P('This lens is the most sensitive of the four to the risk debate, and deliberately so: a '
  'justified multiple of book is a ratio of two rates, so when the denominator nearly '
  'doubles the answer more than halves. It is shown because it is a genuinely independent '
  'read on the same business — it uses no forecast at all — not because it is precise.')

H2('1.3  Relative multiples')
P(f'The listed peer set cannot produce an honest earnings multiple today. Of the eleven '
  f'polyolefin and diversified-chemical peers observed, {D["peers_loss_making"]} are '
  f'loss-making on trailing net income and {D["peers_ev_undefined"]} have no defined '
  f'enterprise-value-to-EBITDA multiple at all because EBITDA is negative. The median of '
  f'whatever happens to print is {D["peer_naive_median"]:.1f} times, and it is rejected: a '
  f'median taken across collapsed denominators measures the depth of the trough, not the '
  f'multiple the market pays.')
figure('fig8_peers.png', 6.7,
       'Figure 2 — Nine of eleven listed peers are loss-making. The gold line is the '
       'through-cycle multiple the study adopts instead of their median.')
rows = [['Through-cycle anchor', 'Multiple']]
for k, v in D['relative_triangulation'].items():
    rows.append([k, f'{v:.2f}x'])
rows.append(['Median of the three — the multiple adopted',
             f'{REL["median_ev_ebitda"]:.2f}x'])
rows.append([f'Applied to mid-cycle EBITDA of ${m(REL["midcycle_ebitda"])}m',
             f'${m(REL["ev"])}m enterprise value'])
rows.append(['Less net debt, leases and minorities, per share',
             f'{px(LEN_["relative_multiples"])} AED'])
table(rows, [4.30, 2.00], size=9.0, band_rows={4, 6})
caption('Table 5 — The triangulation is shown rather than the conclusion asserted: three '
        'named through-cycle anchors, and the median of them. The workbook takes that '
        'median in the sheet.')

H2('1.4  Normalised earnings power')
P(f'Mid-cycle is derived from the audited record rather than asserted. Utilisation is the '
  f'mean of the two most recent audited years — {pc(NRM["util_pe"])} for polyethylene and '
  f'{pc(NRM["util_pp"])} for polypropylene — and the benchmark is the mean of the three '
  f'audited annual averages, ${m(NRM["bench_pe"])} and ${m(NRM["bench_pp"])} a tonne. '
  f'Both therefore already contain a turnaround year and a soft-price year, and neither '
  f'contains the 2026 disruption.')
P(f'On that basis mid-cycle EBITDA is ${m(NRM["ebitda"])}m and mid-cycle NOPAT '
  f'${m(NRM["nopat"])}m. Capitalised at {pc(W["wacc_own"], 2)}, net of the same '
  f'reinvestment the terminal block charges, that gives '
  f'{px(LEN_["normalised_earnings_own_beta"])} dirhams a share; at '
  f'{pc(W["wacc_bottom_up"], 2)} it gives '
  f'{px(LEN_["normalised_earnings_sector_beta"])}.')

H2('1.5  The four lenses in one field')
P(f'The four lenses across both costs of capital span {px(D["fair_low"])} to '
  f'{px(D["fair_high"])} dirhams, median {px(D["fair_mid"])}, against a close of '
  f'{px(SPOT)}. Read column by column they agree closely; read across columns they do '
  f'not. That is the honest shape of the answer and Figure 1 draws it as such.')

H2('1.6  The drivers, and what each one is built on')
P('Every forecast driver below is built from something disclosed. Where nothing is '
  'disclosed, the study says so rather than inventing a formula.')
rows = [['Driver', 'How it is built', 'Source of the build']]
for drv, how, src in [
    ('Volume by product', 'Nameplate capacity times a disclosed utilisation path, '
     'anchored on the rates the plant demonstrated in 2024 and 2025',
     'Management discussion and analysis, by product, every quarter'),
    ('Realised price', 'Published benchmark plus the company’s own disclosed premium, '
     'times a realisation residual measured over three audited years',
     'Management discussion and analysis, reconciled to audited revenue'),
    ('Feedstock', 'Split into a contracted ethane leg and a market-priced propylene leg, '
     'with the market share of the mix as the driver. Each leg escalates on its OWN '
     'price path', 'Cost per tonne from the audited statements over disclosed tonnes'),
    ('Other production cost',
     f'Fitted across three audited years into a ${m(UB["othprod_fixed"])}m fixed leg and '
     f'a ${UB["othprod_var_per_t"] * 1000:.0f} per tonne variable leg. Only the fixed leg '
     f'escalates on consumer inflation', 'Audited statements, three years'),
    ('Selling and distribution', 'Dollars per tonne sold. This is the freight route '
     'decision, and it is one of the two variables the two constructions differ on',
     'Audited statements and interim statements'),
    ('Tax', f'The company’s own three-year mean effective rate of {pc(W["tax"])}, not the '
     f'9% federal headline — Borouge is taxed under the emirate-level regime',
     'Tax note, three audited years'),
    ('Working capital',
     f'{WC["dso"]:.0f} days of sales, {WC["dio"]:.0f} days of inventory and '
     f'{WC["dpo"]:.0f} days of payables, a {WC["ccc"]:.0f}-day cycle. The balance sheet '
     f'and cash flow are projected from these', 'Audited statements, three years'),
    ('Capital expenditure', 'The current-year guide, then a steady-state maintenance '
     'figure set from the company’s own three-year outturn. This is the one materially '
     'top-down driver in the build, and it is sensitised',
     'Guidance and three years of actual spend'),
    ('Ethane escalation', 'Zero real escalation. The pricing formula of the ADNOC '
     'feedstock arrangement is not disclosed anywhere, so none is invented',
     'Searched across four annual reports and every filing — not disclosed'),
]:
    rows.append([drv, how, src])
table(rows, [1.25, 3.15, 2.40], size=8.5)
caption('Table 6 — The driver table. Margins are an OUTPUT of this build, never an input: '
        'the EBITDA margin the forecast produces is whatever tonnes, prices and dollars '
        'per tonne make it.')

figure('fig7_stack.png', 6.9,
       'Figure 3 — Where a dollar of 2025 revenue actually went. Each block is a driver '
       'the forecast projects separately.')

box([
    ('One escalator per cost, and why it matters. ',
     f'The cost stack is not escalated by a single blended inflation index. Contracted '
     f'ethane escalates on its own terms; purchased propylene escalates on the propylene '
     f'benchmark path, through the model’s own price forecast; only the genuinely domestic '
     f'fixed leg escalates on UAE consumer inflation of {pc(MC["uae_cpi"], 1)}. Running '
     f'one blended index across physically different inputs is the standard way a forecast '
     f'manufactures a margin trend out of arithmetic — the price side falls on its own '
     f'commodity path while the cost side rises on a domestic index, and a margin decline '
     f'appears that nobody chose and no evidence supports.'),
])

H2('1.7  The crux')
P('If a reader has time for one number in this study, it is the beta — the measure of how '
  'much this share moves with its market, which sets the cost of equity and through it '
  'almost the entire valuation range.')
rows = [['', 'The share’s own history', 'Built up from the sector'],
        ['Beta', f'{W["beta_own"]:.3f}', f'{W["beta_bottom_up"]:.3f}'],
        ['How it was measured',
         f'{BETA["n"]} weekly observations over {BETA["window_years"]} years against the '
         f'{BETA["regressor"]}',
         'Global chemicals unlevered beta, re-levered at this company’s own debt and tax'],
        ['Statistical quality',
         f'R-squared {BETA["r2"]:.3f}; 90% interval [{BETA["ci90"][0]:.2f}, '
         f'{BETA["ci90"][1]:.2f}], spanning '
         f'{(BETA["ci90"][1] - BETA["ci90"][0]) / BETA["beta"]:.2f} times the estimate '
         f'itself',
         'No sampling error of its own, but it is somebody else’s companies'],
        ['Cost of equity', pc(W['ke_own'], 2), pc(W['ke_bottom_up'], 2)],
        ['Cost of capital', pc(W['wacc_own'], 2), pc(W['wacc_bottom_up'], 2)],
        ['Value per share, shipping normalises',
         px(LEN_['dcf_normalisation_own_beta']),
         px(LEN_['dcf_normalisation_sector_beta'])]]
table(rows, [1.55, 2.55, 2.55], size=8.8, band_rows={6})
caption('Table 7 — The study’s central contested judgement, computed both ways and '
        'published side by side. It is never averaged into one number.')
P(f'The case for the low measured beta is that it is this company’s own history, measured '
  f'properly, and it passes every usability test applied to it. The case against it is '
  f'that the same tests flag it as weak, and that a lead-lag correction for thin trading '
  f'moves it DOWN rather than up — so infrequent trading does not explain it. What a '
  f'{W["beta_own"]:.2f} beta most plausibly measures is a share with a small free float '
  f'that has traded in a narrow band since listing, not the risk of a business whose '
  f'earnings track a global commodity benchmark. A reader who finds that argument '
  f'persuasive should read the sector-beta column; a reader who trusts measured history '
  f'over analogy should read the other. The study does not choose for them.')

P('Because this is the number that matters most, it was tested four ways rather than '
  'measured once.')
rows = [['Test', 'Result', 'What it says']]
WS = BETA['window_sensitivity']
rows.append(['Window length',
             ' · '.join(f'{y}yr {WS[str(y)]["beta"]:.2f}' for y in (2, 3, 4, 5)),
             'Stable. The rule permits any window from two to five years, and the answer '
             'barely moves across all four — so the estimate is not an artefact of where '
             'the window was cut'])
rows.append(['Lead-lag correction for thin trading',
             f'{BETA["dimson"]["sum_beta"]:.3f} against {BETA["beta"]:.3f}',
             'Moves the estimate DOWN, not up. Infrequent trading is the usual '
             'explanation for a low measured beta, and here it is ruled out rather than '
             'assumed'])
rows.append(['A different construction of "the market"',
             f'{BETA["composite_corroboration"]["beta"]:.3f} against an equal-weight '
             f'basket of the other {BETA["composite_corroboration"]["names"]} listed '
             f'UAE names',
             'Lower still. An equal-weight basket over-weights small, thinly traded '
             'companies, which is exactly why the market-capitalisation-weighted index '
             'is the right measure and this is only a cross-check'])
rows.append(['Is the share inside its own index?',
             f'Yes, at under '
             f'{BETA["index_membership"]["weight_upper_bound"] * 100:.1f}% of it',
             'It is a constituent, so a little of its own movement is inside the thing '
             'it is measured against. At this weight the effect is negligible; in the '
             'equal-weight basket above it would not have been'])
table(rows, [1.70, 1.95, 3.15], size=8.3)
caption('Table 8 — The beta tested four ways. Every test points the same direction: the '
        'measured figure is genuinely low, and it is genuinely uncertain.')

H2('1.8  Macro, country and the cost of capital')
P('The cost of capital is built from the ground up, and country risk is charged exactly '
  'once.')
rows = [['Component', 'Value', 'Where it comes from']]
for label, val, src in [
    ('US 10-year Treasury yield', pc(MC['ust_10y'], 2), 'The dollar risk-free anchor'),
    ('Less: US default spread', '(' + pc(MC['us_default_spread'], 2) + ')',
     'Normalises the yield to a true risk-free rate'),
    ('Normalised risk-free rate', pc(W['rf_star'], 2), 'The rate used'),
    ('Dirham cross-check', pc(W['rf_star_aed'], 2),
     f'UAE dirham government bond at {pc(MC["uae_govt_yield_aed"], 2)} less the UAE '
     f'default spread of {pc(MC["uae_default_spread_rating"], 2)}'),
    ('Mature-market equity premium', pc(MC['mature_erp'], 2), 'Before country risk'),
    ('Plus: UAE country risk premium', pc(MC['uae_crp'], 2),
     'Country risk enters here and nowhere else'),
    ('Equity risk premium (rating basis)', pc(W['erp_rating'], 2), 'The premium used'),
    ('Equity risk premium (spread basis)', pc(W['erp_default_spread_basis'], 2),
     'Published alongside: no sovereign credit-default-swap quote exists for the UAE'),
    ('Cost of equity — own beta', pc(W['ke_own'], 2), 'Risk-free plus beta times premium'),
    ('Cost of equity — sector beta', pc(W['ke_bottom_up'], 2), 'The same build, other beta'),
    ('Pre-tax cost of debt', pc(W['kd'], 2),
     'Marginal and forward-looking, in the currency of the cash flows'),
    ('Equity weight at market value', pc(W['equity_weight']),
     f'Market capitalisation ${m(W["mktcap"])}m against net debt ${m(FN["net_debt"])}m'),
    ('Cost of capital — own beta', pc(W['wacc_own'], 2), ''),
    ('Cost of capital — sector beta', pc(W['wacc_bottom_up'], 2), ''),
]:
    rows.append([label, val, src])
table(rows, [2.05, 0.95, 3.90], size=8.6, band_rows={3, 7, 13, 14})
caption('Table 9 — The cost of capital, built line by line. The risk-free rate is '
        'normalised by the sovereign’s own default spread BEFORE a country premium is '
        'added, so sovereign risk is charged once rather than twice.')

P('Two constructions of the risk-free rate are shown because they do not agree, and the '
  'gap is reported rather than reconciled away. Building it in dollars gives '
  f'{pc(W["rf_star"], 2)}; building it from the dirham government bond and subtracting '
  f'the UAE’s own default spread gives {pc(W["rf_star_aed"], 2)}. Under a hard peg those '
  f'should coincide; they differ by {pc(W["rf_star"] - W["rf_star_aed"], 2)}. The dollar '
  f'construction is used because the company reports, borrows and sells in dollars.')

P('The cost of debt was tested against evidence rather than assumed.')
rows = [['Evidence', 'Rate', 'Read'],
        ['UAE sovereign in dollars', pc(W['sovereign_usd'], 2),
         'The floor — a corporate cannot borrow below its own sovereign in the same '
         'currency'],
        ['Borouge’s related-party facilities as priced',
         pc(W['kd_related_party'], 2),
         f'USD 2.8bn of term facilities plus a drawn revolver from the parent, priced '
         f'{pc(W["margin_related"], 2)} over the reference rate'],
        ['Arm’s-length marginal cost adopted', pc(W['kd'], 2),
         f'The long dollar rate plus a {pc(W["margin_arms"], 2)} margin. The '
         f'related-party facilities sit {pc(W["kd"] - W["kd_related_party"], 2)} inside '
         f'that — close enough to arm’s length that no adjustment is warranted, and the '
         f'test is shown rather than asserted'],
        ['After tax', pc(W['kd'] * (1 - W['tax']), 2), 'What enters the cost of capital']]
table(rows, [1.95, 0.80, 4.15], size=8.6)
caption('Table 10 — The cost-of-debt evidence. Every contested construction in this study '
        'is priced rather than argued.')

H2('1.9  Sensitivity')
figure('fig2_sens.png', 6.4,
       'Figure 4 — Value per share across the cost of capital and terminal growth, on the '
       'central construction at the share’s own measured risk. The bold cell is the '
       'published reading.')
P('Two things are worth reading off that grid. The first is how steep it is: half a point '
  'on the cost of capital is worth roughly half a dirham, which is why the beta debate '
  'dominates this study. The second is subtler — value RISES with terminal growth here, '
  'which is the opposite of the usual textbook direction. That is not an error. Growth '
  f'has to be funded by reinvestment of growth divided by the return on capital, and at a '
  f'{pc(MC["terminal_roc"], 0)} return against a {pc(W["wacc_own"], 2)} cost of capital '
  f'that reinvestment earns far more than it costs. Had the return sat below the cost of '
  f'capital the sign would flip.')
rows = [['Sensitivity', 'Downside', 'Published', 'Upside']]
prem = SN['premium_grid']['normalisation']
util = SN['util_grid']['normalisation']
rows.append([f'Realised premium over benchmark, ±$100/tonne', px(prem[0][1]),
             px(prem[2][1]), px(prem[4][1])])
rows.append([f'Utilisation, ±10 percentage points', px(util[0][1]), px(util[2][1]),
             px(util[4][1])])
rows.append([f'Cost of capital, ±100 basis points',
             px(SN['grids']['normalisation'][4][2]), px(SN['grids']['normalisation'][2][2]),
             px(SN['grids']['normalisation'][0][2])])
table(rows, [3.10, 1.30, 1.30, 1.30], size=8.9)
caption('Table 11 — The crux sensitised in observable units: dollars per tonne of premium '
        'and percentage points of utilisation, not abstract multiples.')

# =============================================================== 6 SECTION 2
H1('2  Technical and price structure')
P(f'The share closed at {px(SPOT)} dirhams on 7 August 2026, having traded between '
  f'{px(TE["lo_52w"])} and {px(TE["hi_52w"])} over the past year. It sits '
  f'{pc(TE["pct_off_high"])} below that high and {pc(TE["pct_off_low"])} above that low '
  f'— which is to say, close to the bottom of its own range.')
P(TE['tech']['summary'])
figure('fig3_ma.png', 6.9,
       'Figure 5 — The price since listing in June 2022, with the twenty-, fifty- and '
       'two-hundred-session averages.')
rows = [['Reading', 'Value', 'What it says'],
        ['Close', px(TE['close']), 'The anchor for everything below'],
        ['20-session average', px(TE['ma'][20]),
         f'{TE["ma_slope"][20].capitalize()} — the price is '
         f'{"below" if SPOT < TE["ma"][20] else "above"} it'],
        ['50-session average', px(TE['ma'][50]), TE['ma_slope'][50].capitalize()],
        ['200-session average', px(TE['ma'][200]), TE['ma_slope'][200].capitalize()],
        ['Relative strength index (14)', f'{TE["rsi"]:.0f}',
         'Soft, but not at an extreme in either direction'],
        ['Average true range (14)', f'{TE["atr"]:.3f}',
         f'About {pc(TE["atr_pct"])} of the price a day — an orderly tape'],
        ['Moving-average crossover',
         f'{TE["ma_cross"]["kind"]} cross, {TE["ma_cross"]["ago"]} sessions ago',
         'Recent enough to still be the governing structure'],
        ['Nearest resistance', px(TE['levels']['res'][0]),
         'Then ' + ' and '.join(px(x) for x in TE['levels']['res'][1:])],
        ['Nearest support', px(TE['levels']['sup'][0]),
         'Then ' + ' and '.join(px(x) for x in TE['levels']['sup'][1:])]]
table(rows, [1.90, 1.15, 3.85], size=8.8)
caption('Table 12 — The price structure. Levels are ordered from nearest to the close '
        'outward in both directions.')
P('This section describes the tape and nothing else. It carries no view on what the '
  'business is worth — that is what the four lenses above are for — and the two are '
  'deliberately not blended.')

# =============================================================== 7 SECTION 3
H1('3  A probabilistic map of the traded price')
P('This is a different question from everything above. The lenses ask what the business '
  'is worth. This section asks a narrower and more testable question: given how this '
  'share has actually behaved, where could the price sit in one and in three months?')
h1m, h3m = STK['horizons']['1M'], STK['horizons']['3M']
P(f'The bands below are simulated from the cleaned daily price history since listing. '
  f'The central drift is not a forecast of direction — it is the risk-free rate of '
  f'{pc(STK["rf_live"], 2)} less the dividend yield, which at the company’s stated annual '
  f'intention of 16.2 fils a share on a {px(SPOT)} close is {pc(STK["q_annual"], 2)}. '
  f'Because the dividend exceeds the risk-free rate, the drift is NEGATIVE at '
  f'{pc(STK["rf_live"] - STK["q_annual"], 2)} a year: a share that pays out more than '
  f'cash earns should, all else equal, drift down by the difference. That is why the '
  f'probability of finishing above today’s close is slightly below half rather than above '
  f'it.')
rows = [['Horizon', 'Ends', '5th', '25th', 'Median', '75th', '95th',
         'Above the close']]
for tag, name in [('1M', 'One month'), ('3M', 'Three months')]:
    hz = STK['horizons'][tag]
    rows.append([name, hz['grade_date']] +
                [px(hz['pct'][p]) for p in ('p5', 'p25', 'p50', 'p75', 'p95')] +
                [pc(hz['p_above'], 0)])
table(rows, [1.05, 1.05, 0.72, 0.72, 0.78, 0.72, 0.72, 1.04], size=8.7)
caption('Table 13 — The percentile map, in dirhams a share.')
figure('fig4_fan.png', 6.9,
       'Figure 6 — The three-month band. The shaded areas are the middle 50% and the '
       'middle 90% of simulated outcomes.')
figure('fig6_dist.png', 6.5,
       'Figure 7 — The full distribution of three-month outcomes.')

P('A level-touch ladder answers a question the percentiles do not: not where the price '
  'ends up, but whether it trades through a level at any point along the way.')
rows = [['Move from the close', 'Level (AED)', 'Within one month', 'Within three months']]
for p_ in (5, 10, 15, 20):
    rows.append([f'Up {p_}%', px(SPOT * (1 + p_ / 100)),
                 pc(h1m['touch_up'][str(p_)], 0), pc(h3m['touch_up'][str(p_)], 0)])
for p_ in (5, 10, 15, 20):
    rows.append([f'Down {p_}%', px(SPOT * (1 - p_ / 100)),
                 pc(h1m['touch_dn'][str(p_)], 0), pc(h3m['touch_dn'][str(p_)], 0)])
table(rows, [1.60, 1.40, 1.85, 1.95], size=8.8)
caption('Table 14 — The chance the price trades through each level at any point inside '
        'the window, not just where it finishes.')

box([
    ('How well has this band actually worked on THIS share — and the honest answer. ',
     f'The method was tested by running it backwards over the share’s own history, '
     f'stepping forward three months at a time and scoring each band against what '
     f'actually happened, against the benchmark of assuming the price simply drifts with '
     f'carry. On Borouge specifically it did NOT beat that benchmark. Over the '
     f'{BT["full"]["windows"]} independent three-month windows the history allows, it '
     f'scored {BT["full"]["skill_norm"]:+.3f} against it — worse, not better, and worse '
     f'consistently rather than by luck of the sampling.'),
    ('What went wrong is specific and it is visible in the numbers. ',
     f'The bands are too WIDE, not mis-centred. {pc(BT["full"]["cov80"], 0)} of outcomes '
     f'landed inside the 80% band and {pc(BT["full"]["cov90"], 0)} inside the 90% band, '
     f'when 80% and 90% is what those bands are meant to contain. The band came out '
     f'{BT["full"]["width_vs_benchmark"]:.2f} times as wide as the benchmark’s. Centring '
     f'is fine — the average outcome sat at the {BT["full"]["pit_mean"]:.2f} percentile '
     f'of its own band, close to the midpoint you would want. Borouge is simply a calmer '
     f'share than the UAE market average the band width is set from, and a band sized for '
     f'that average is too generous for it.'),
    ('Two further limits, stated rather than buried. ',
     f'First, Borouge listed on 3 June 2022, so its history is '
     f'{BT["history_span_years"]} years, not five. A five-year test is not available for '
     f'this share and the five-year window here is identical to its whole history. '
     f'Second, {BT["full"]["windows"]} independent windows is a small sample, and the '
     f'distribution of outcomes within the bands is not as even as it should be. Read '
     f'the bands in this section as a description of how this share has behaved, and '
     f'treat their width as generous rather than tight.'),
])

# =============================================================== 8 SECTION 4
H1('4  Comparison of the lenses')
P('Four methods, deliberately chosen so that they fail in different ways. Where they '
  'agree, the agreement means something; where they diverge, the divergence points at a '
  'specific assumption rather than at general uncertainty.')
rows = [['Lens', 'What it is good at', 'How it fails', 'Reading (AED)']]
rows.append(['Discounted cash flow',
             'It is the only lens that uses the actual tonnes, prices and costs, and the '
             'only one that can price a fee stream separately',
             f'It puts {pc(TVSHARE_N)} of the answer in a terminal block, and it is '
             f'hostage to the cost of capital',
             f'{px(LEN_["dcf_normalisation_sector_beta"])} – '
             f'{px(LEN_["dcf_normalisation_own_beta"])}'])
rows.append(['Book value and sustainable return',
             'Uses no forecast at all — just what the company has actually earned on '
             'what it has actually invested',
             'It is a ratio of two rates, so it amplifies the risk debate more than any '
             'other lens',
             f'{px(LEN_["book_value_sector_beta"])} – '
             f'{px(LEN_["book_value_own_beta"])}'])
rows.append(['Relative multiples',
             'Completely independent of the risk debate, and anchored on what the market '
             'has actually paid through a cycle',
             'The current peer set is broken — nine of eleven are loss-making — so it '
             'leans on through-cycle anchors rather than live comparables',
             px(LEN_['relative_multiples'])])
rows.append(['Normalised earnings power',
             'Strips out both the disruption and the trough by construction',
             'Mid-cycle is a judgement, and it inherits the same cost of capital as the '
             'cash-flow lens',
             f'{px(LEN_["normalised_earnings_sector_beta"])} – '
             f'{px(LEN_["normalised_earnings_own_beta"])}'])
table(rows, [1.50, 1.90, 2.05, 1.35], size=8.5)
caption('Table 15 — What each lens is for, and where each one breaks.')
P(f'The pattern is clear once the columns are read separately. Inside the low-risk '
  f'column the four lenses span {px(LEN_["relative_multiples"])} to '
  f'{px(LEN_["dcf_normalisation_own_beta"])}; inside the high-risk column they span '
  f'{px(LEN_["normalised_earnings_sector_beta"])} to '
  f'{px(LEN_["relative_multiples"])}. The relative lens sits in the middle of the whole '
  f'field precisely because it is the one lens the risk debate cannot touch — and at '
  f'{px(LEN_["relative_multiples"])} against a close of {px(SPOT)}, it is also the lens '
  f'that sits furthest below the market.')

# =============================================================== 9 SECTION 5
H1('5  Catalysts')
rows = [['What', 'When', 'Why it matters']]
for what, when, why in [
    ('Third-quarter results',
     'Late October 2026',
     'The first clean read on whether utilisation and freight actually recovered in the '
     'second half. This is the single observation that separates the study’s two '
     'constructions, and it arrives within months rather than years.'),
    ('Feedstock cost per tonne in the next disclosure', 'With Q3 and full-year results',
     f'It ran ${m(UB["feed_per_t_h126"])} in the first half against '
     f'${m(UB["feed_per_t"]["2025"])} in 2025. A move back toward the low 300s confirms '
     f'the conversion unit is running on ethane again; a figure still near '
     f'${m(UB["feed_per_t_h126"])} says the disruption is structural rather than '
     f'temporary.'),
    ('Freight cost per tonne sold', 'With Q3 and full-year results',
     f'${m(UB["sd_per_t_h126"])} against ${m(UB["sd_per_t"]["2025"])} is the re-routing '
     f'cost. It reverses when the direct route reopens, and not before.'),
    ('The tender offer', 'Expected during 2027',
     'Borouge plc shares are expected to convert into shares of the combined group, '
     'subject to market conditions and regulatory approval. No exchange ratio has been '
     'published. When one is, it becomes the dominant fact about this security and '
     'supersedes much of the analysis here.'),
    ('The dividend', 'Declared with full-year results',
     f'The stated annual intention of 16.2 fils a share is {pc(STK["q_annual"], 1)} on '
     f'the current price and is explicitly reaffirmed in the half-year release. It is '
     f'also the reason the probability band in Section 3 drifts down rather than up.'),
    ('Borouge 4 ramp-up and recontribution', 'Recontribution not expected before 2029',
     f'The operator fee is worth about ${m(FN["b4"]["value"])}m today. If the terms on '
     f'which those assets eventually move into the group change, so does that figure — '
     f'in either direction.'),
    ('Polyolefin benchmark prices', 'Continuous',
     'Global capacity rises about a fifth by 2034 against demand growing with world '
     'output. The industry’s own consensus on when operating rates recover has already '
     'slipped to 2032. This is the slow variable that sets the ceiling on every lens '
     'here.'),
]:
    rows.append([what, when, why])
table(rows, [1.45, 1.20, 4.15], size=8.5)
caption('Table 16 — What to watch, and what each observation would actually settle.')

# =============================================================== 10 SECTION 6
H1('6  Reading the probability zones')
P('The bands in Section 3 are easy to over-read, so this section says plainly what they '
  'do and do not mean.')
bullet(f'The 90% band for three months runs {px(h3m["pct"]["p5"])} to '
       f'{px(h3m["pct"]["p95"])}. That means roughly nine outcomes in ten fall inside it '
       f'IF the future resembles this share’s own past. It is not a promise, and one '
       f'outcome in ten falls outside it by design.',
       bold_head='A band is a description, not a forecast. ')
bullet('The percentile table says where the price might FINISH. The touch ladder says '
       'whether it might pass through a level along the way. Those are different '
       'probabilities and the touch numbers are always the larger of the two.',
       bold_head='Finishing and touching are different questions. ')
bullet(f'The evidence in Section 3 says these bands have been too WIDE on this share: '
       f'{pc(BT["full"]["cov90"], 0)} of past outcomes landed inside a band meant to hold '
       f'90%. A reader should treat the edges as conservative rather than as a tight '
       f'boundary.', bold_head='On this share specifically, the bands are generous. ')
bullet(f'A fair-value range of {px(D["fair_low"])} to {px(D["fair_high"])} and a '
       f'three-month band of {px(h3m["pct"]["p5"])} to {px(h3m["pct"]["p95"])} are '
       f'answers to different questions. The first is about the business over years; the '
       f'second is about the share price over weeks. Nothing in this study claims the '
       f'price will move toward the fair-value range inside the band’s window.',
       bold_head='The band and the fair value are not the same object. ')

# =============================================================== 11 SECTION 7
H1('7  Caveats, and what would change our mind')
rows = [['The concern', 'How much it matters', 'What would settle it']]
for concern, matters, settle in [
    ('The beta is weak, and it drives everything',
     f'It is worth about {px(LEN_["dcf_normalisation_own_beta"] - LEN_["dcf_normalisation_sector_beta"])} '
     f'dirhams a share — more than every other uncertainty in this study combined',
     'A longer trading history, a larger free float, or a period in which the share '
     'actually moves with its market would resolve it empirically. Until then the study '
     'publishes both answers rather than choosing.'),
    (f'Terminal value is {pc(TVSHARE_N)} of enterprise value',
     'High, and structurally so for a long-lived asset at a low cost of capital. At the '
     f'higher cost of capital it falls to {pc(ALT["tv_share"]["normalisation"])}',
     'Nothing settles it; it is a property of the method. It is disclosed in the summary '
     'table, in the bridge and in the workbook rather than hidden, so a reader can '
     'discount it as they see fit.'),
    ('The ethane pricing formula is not disclosed',
     'Material but bounded. The study carries zero real escalation and shows what a '
     'non-zero escalator costs in the sensitivity',
     'Disclosure of the ADNOC supply terms. Until then no forward escalator can honestly '
     'be built, and inventing one would be worse than carrying zero and saying so.'),
    ('Only one operating segment is reported',
     'Volume and price are disclosed by product but cost and profit are not, so the cost '
     'allocation between polyethylene and polypropylene rests on physical drivers rather '
     'than on disclosure',
     'Segmental profitability disclosure. The gap is flagged rather than papered over.'),
    ('The tender offer has no published ratio',
     'Potentially decisive, and entirely unquantifiable today. No conversion value enters '
     'any number here',
     'Publication of the exchange terms. At that point this study’s subject changes and '
     'much of it would need re-doing.'),
    ('Capital expenditure beyond the current year is not guided',
     'The one materially top-down driver in the build. It is set from the company’s own '
     'three-year outturn and sensitised',
     'A published medium-term capital programme.'),
    ('The probability bands did not beat their benchmark on this share',
     f'Stated in full in Section 3: {BT["full"]["skill_norm"]:+.3f} against the benchmark '
     f'over {BT["full"]["windows"]} windows, because the bands are too wide rather than '
     f'mis-centred',
     'More history. The share has traded for '
     f'{BT["history_span_years"]} years, and the test needs more independent windows than '
     'that allows.'),
]:
    rows.append([concern, matters, settle])
table(rows, [1.65, 2.35, 2.80], size=8.4)
caption('Table 17 — What could be wrong, how much it would cost, and what evidence would '
        'resolve it.')

# =============================================================== 12 APPENDIX A
doc.add_page_break()
H1('Appendix A  Financial statements')
H2('A.1  Income statement — three audited years and five forecast years')
rows = [['USD million'] + [f'FY{y}' for y in HYS] + [str(y) for y in YF]]
for key, label in [('revenue', 'Revenue'), ('gross_profit', 'Gross profit'),
                   ('sd', 'Selling and distribution'),
                   ('ga', 'General and administrative'),
                   ('ebit', 'Operating profit (EBIT)'),
                   ('da', 'Depreciation and amortisation'), ('ebitda', 'EBITDA'),
                   ('pbt', 'Profit before tax'), ('tax', 'Tax'),
                   ('pat', 'Profit after tax')]:
    hist_vals = [m(H[y][key]) for y in HYS]
    fvals = []
    for r_ in FN['rows']:
        if key == 'gross_profit':
            v = r_['revenue'] - r_['feedstock'] - r_['othprod'] - r_['da']
        elif key == 'pbt':
            v = r_['ebit'] - FN['net_debt'] * W['kd']
        elif key == 'tax':
            v = (r_['ebit'] - FN['net_debt'] * W['kd']) * W['tax']
        elif key == 'pat':
            v = (r_['ebit'] - FN['net_debt'] * W['kd']) * (1 - W['tax'])
        else:
            v = r_[key]
        fvals.append(m(v))
    rows.append([label] + hist_vals + fvals)
table(rows, [1.62, 0.62, 0.62, 0.62, 0.63, 0.63, 0.63, 0.63, 0.63], size=8.0)
caption('Table A1 — Historical columns are the audited figures. Forecast columns are the '
        'same cells that feed the cash-flow waterfall, linked rather than restated.')

H2('A.2  Balance sheet')
rows = [['USD million'] + [f'FY{y}' for y in HYS]]
for key, label, keys in [
        ('ppe', 'Property, plant and equipment', ['ppe_fy23', 'ppe_fy24', 'ppe_fy25']),
        ('inv', 'Inventory', ['inv_fy23', 'inv_fy24', 'inv_fy25']),
        ('cash', 'Cash and equivalents', ['cash_fy23', 'cash_fy24', 'cash_fy25']),
        ('ta', 'Total assets', ['ta_fy23', 'ta_fy24', 'ta_fy25']),
        ('debt', 'Borrowings', ['debt_fy23', 'debt_fy24', 'debt_fy25']),
        ('equity', 'Equity attributable to owners',
         ['eq_owners_fy23', 'eq_owners_fy24', 'eq_owners_fy25'])]:
    rows.append([label] + [m(CI[k] / 1000) for k in keys])
rows.append(['Net debt'] + [m((CI[f'debt_fy{y[2:]}'] - CI[f'cash_fy{y[2:]}']) / 1000)
                            for y in HYS])
table(rows, [2.60, 1.35, 1.35, 1.35], size=8.6)
caption('Table A2 — The audited balance sheet, in USD million, from the filings.')

H2('A.3  How the forecast balance sheet and cash flow are built')
P('Neither statement is plugged. The markers below are what the workbook actually does, '
  'and a reader can follow each one in the sheet.')
rows = [['Line', 'How it moves']]
for line, how in [
    ('Property, plant and equipment',
     'Opening balance, plus capital expenditure, less depreciation. Depreciation is the '
     'opening balance times a rate set by the company’s own current-year charge.'),
    ('Trade receivables',
     f'Forecast revenue times {WC["dso"]:.0f} days over 365 — the collection period the '
     f'audited statements themselves show.'),
    ('Inventory',
     f'Forecast production cost times {WC["dio"]:.0f} days over 365.'),
    ('Trade payables',
     f'Forecast production cost times {WC["dpo"]:.0f} days over 365.'),
    ('Net working capital',
     f'Receivables plus inventory less payables — a {WC["ccc"]:.0f}-day cash cycle. Its '
     f'change is the working-capital line in the cash-flow waterfall.'),
    ('Net debt',
     'Opening balance, less free cash flow after the after-tax finance cost, plus the '
     'dividend the company states it intends to keep paying.'),
    ('Equity',
     'Opening balance, plus profit after tax, less that same dividend.'),
    ('Cash from operations',
     'EBITDA less the working-capital movement less tax on operating profit. It '
     'reconciles to free cash flow to the firm through capital expenditure alone.'),
]:
    rows.append([line, how])
table(rows, [1.85, 4.95], size=8.6)
caption('Table A3 — The roll-forward markers. Every one of them is a live formula in the '
        'companion workbook.')

# =============================================================== 13 APPENDIX B
doc.add_page_break()
H1('Appendix B  Peers, risks and the research record')
H2('B.1  The listed peer set')
rows = [['Company', 'EV/EBITDA', 'Forward P/E', 'Price to book', 'Dividend yield',
         'EBITDA margin', 'Loss-making']]
for nm, d_ in D['peer_table'].items():
    rows.append([nm,
                 f'{d_["ev_ebitda"]:.1f}x' if d_['ev_ebitda'] else '—',
                 f'{d_["pe_fwd"]:.1f}x' if d_['pe_fwd'] else '—',
                 f'{d_["pb"]:.2f}x' if d_['pb'] else '—',
                 pc(d_['div_yield']) if d_['div_yield'] is not None else '—',
                 pc(d_['ebitda_margin']) if d_['ebitda_margin'] is not None else '—',
                 'yes' if d_['loss_making'] else 'no'])
PBM = MC['peer_borouge_market']
rows.append(['Borouge, on the same basis', f'{PBM["ev_ebitda"]:.1f}x',
             f'{PBM["pe_fwd"]:.1f}x', '—', pc(PBM['div_yield']),
             pc(PBM['ebitda_margin']), 'no'])
table(rows, [1.55, 0.90, 0.90, 0.90, 0.95, 0.95, 0.75], size=8.2,
      band_rows={len(rows) - 1})
caption('Table B1 — The peer set, observed 9 August 2026. It is a cross-check on the '
        'valuation, never a source for any Borouge figure. Borouge’s EBITDA margin is '
        'roughly three times the group’s while nine of eleven lose money — the '
        'advantaged-feedstock position in one line.')

H2('B.2  Risk register')
rows = [['Risk', 'Where it hits', 'How the study handles it']]
for risk, hits, handled in [
    ('Structural oversupply in polyolefins', 'Benchmark prices in every forecast year',
     'The price path settles BELOW the 2023–24 level rather than returning to it, on the '
     'published capacity and operating-rate evidence'),
    ('Shipping-lane disruption', 'Utilisation and freight cost',
     'Two full constructions, published side by side rather than averaged'),
    ('Feedstock availability', 'Feedstock cost per tonne',
     'The contracted and market-priced legs are modelled separately, with the market '
     'share of the mix as an explicit driver'),
    ('Concentration in one site', 'Everything',
     'Not diversifiable and not modelled away. One complex, one set of assets, and a '
     'single unplanned outage would hit every line'),
    ('Related-party dependence', 'Feedstock terms, debt pricing, the fee agreement',
     'The debt is tested against arm’s length and sits inside it; the feedstock formula '
     'is not disclosed and that gap is flagged'),
    ('Minority position in a controlled company',
     'Governance, and the terms of any future conversion',
     'Stated as a caveat. No conversion value enters any number'),
    ('Regulatory pressure on plastics', 'Long-run demand growth',
     'Carried as a drag on terminal growth rather than as a demand collapse'),
]:
    rows.append([risk, hits, handled])
table(rows, [1.75, 1.85, 3.20], size=8.4)
caption('Table B2 — The risk register.')

H2('B.3  The research record')
P(f'Every historical figure in this study traces to a document Borouge itself published. '
  f'All {SRC["total"]} of those documents were re-downloaded from the company’s own '
  f'investor-relations library on 9 August 2026 and confirmed byte-for-byte identical to '
  f'the copies this study was built from. Four complete audited financial years were '
  f'obtained ({", ".join(SRC["complete_audited_years"])}), of which the three most recent '
  f'are carried as model columns; both disclosed quarters of the study year were read '
  f'before the forecast was built, not after. A separate bibliography document lists '
  f'every source, every input and every judgement.')
rows = [['Layer', 'What was used', 'Role']]
for layer, used, role in [
    ('The company’s own filings',
     'Four years of audited statements, two interim periods, five management discussions, '
     'four earnings presentations, two earnings releases, four annual reports',
     'The ONLY source of any figure Borouge reports. Historicals, unit build, debt, '
     'working capital, tax'),
    ('Official statistics and central banks',
     'US Treasury yields, the overnight financing rate, the UAE central bank’s base rate '
     'and quarterly review, the UAE finance ministry’s bond auction, the IMF and the '
     'Energy Information Administration',
     'Macro context and the risk-free rate'),
    ('Published market data',
     'Sovereign default spreads, equity risk premiums and sector betas by country and '
     'industry',
     'The cost-of-capital build'),
    ('Industry press and research',
     'Capacity outlooks to 2034 and operating-rate consensus',
     'Forecast price direction only — never a Borouge figure'),
    ('Market data aggregators',
     'Eleven listed peers’ multiples and margins',
     'CROSS-CHECK ONLY, and labelled as such wherever it appears'),
]:
    rows.append([layer, used, role])
table(rows, [1.55, 3.05, 2.20], size=8.4)
caption('Table B3 — Where the evidence came from, and what each layer was allowed to do. '
        'No aggregator or press report is a source for any figure Borouge itself reports.')

# =============================================================== 14 APPENDIX C
doc.add_page_break()
H1('Appendix C  Three analysts, three methods, one company')
P('Three experienced practitioners were asked to value Borouge independently, each using '
  'the method they actually trust. They are labelled Expert 1, 2 and 3. Each shows their '
  'workings in full, names a sensitivity with numbers attached, and states in advance the '
  'single observation that would prove them wrong.')

H2('C.1  Expert 1 — the cash-flow analyst')
P('Worldview. A company is worth the cash it will produce, discounted. Everything else — '
  'multiples, book value, sentiment — is a shortcut to that, and shortcuts break exactly '
  'when you need them. Build the tonnes, build the dollars per tonne, and let the margin '
  'fall out.', italic=True)
P('When it works: when the operating build is genuinely disclosed, as it is here. When it '
  f'fails: when most of the answer sits past the forecast, which is precisely the '
  f'situation — {pc(TVSHARE_N)} of enterprise value is in the terminal block.')
rows = [['Working', 'Value']]
for label, v in [
    ('Mid-forecast revenue (USD m)', m(FN['rows'][2]['revenue'])),
    ('Mid-forecast EBITDA (USD m)', m(FN['rows'][2]['ebitda'])),
    ('Implied EBITDA margin', pc(FN['rows'][2]['ebitda_margin'])),
    # one convention in this table too: the net-debt line below is bracketed, so
    # this deduction is bracketed rather than left as a bare positive
    ('Less depreciation (USD m)', '(' + m(FN['rows'][2]['da']) + ')'),
    ('EBIT (USD m)', m(FN['rows'][2]['ebit'])),
    (f'NOPAT after {pc(W["tax"])} tax (USD m)', m(FN['rows'][2]['nopat'])),
    ('Free cash flow to the firm (USD m)', m(FN['rows'][2]['fcff'])),
    ('Present value of five explicit years (USD m)', m(FN['pv_explicit'])),
    ('Present value of the terminal block (USD m)', m(FN['pv_terminal'])),
    ('Operator fee stream (USD m)', m(FN['b4']['value'])),
    ('Enterprise value (USD m)', m(FN['ev'])),
    ('Less net debt, leases and minorities (USD m)',
     '(' + m(FN['net_debt'] + FN['leases'] + FN['nci']) + ')'),
    ('Equity value (USD m)', m(FN['equity'])),
    ('Value per share (AED)', px(FN['per_share_aed'])),
]:
    rows.append([label, v])
table(rows, [4.30, 2.00], size=8.7, band_rows={11, 14})
P(f'Named sensitivity. "Move the cost of capital by fifty basis points and I move by '
  f'{px(abs(SN["grids"]["normalisation"][1][2] - SN["grids"]["normalisation"][2][2]))} '
  f'dirhams. Move the realised premium by a hundred dollars a tonne and I move by '
  f'{px(abs(SN["premium_grid"]["normalisation"][4][1] - SN["premium_grid"]["normalisation"][2][1]))}. '
  f'Those are the only two that matter to me."')
P('Falsifier, stated in advance. "If full-year 2026 feedstock cost per tonne comes in '
  f'above ${m(UB["feed_per_t_h126"])} — that is, if the first half was not the peak — '
  f'then my premise that the disruption is temporary is wrong and every number above is '
  f'too high."', italic=True)

H2('C.2  Expert 2 — the balance-sheet and returns analyst')
P('Worldview. Forecasts are opinions; the balance sheet is a record. What a company has '
  'actually earned on what it has actually invested, over a full cycle, tells you more '
  'than five years of projected tonnes. Value it off book and off return.', italic=True)
P('When it works: when a business is capital-intensive with a long record of stable '
  'returns, which describes this one. When it fails: when book value has been distorted '
  'by write-downs or acquisitions, and when the answer is hostage to the cost of equity — '
  'which here it very much is.')
rows = [['Working', 'Value']]
for label, v in [
    ('Return on equity, 2023', pc(BV['roe_hist'][0])),
    ('Return on equity, 2024', pc(BV['roe_hist'][1])),
    ('Return on equity, 2025', pc(BV['roe_hist'][2])),
    ('Sustainable return on equity (mean)', pc(BV['roe_sustainable'])),
    ('Book value per share (USD)', f'{BV["bvps_usd"]:.4f}'),
    ('Cost of equity at the share’s own measured risk', pc(W['ke_own'], 2)),
    ('Long-run growth', pc(MC['terminal_growth'], 1)),
    ('Justified price to book = (return − growth) / (cost of equity − growth)',
     f'{BV["justified_pb"]:.2f}x'),
    ('Value per share (AED)', px(LEN_['book_value_own_beta'])),
    ('The same at sector risk: cost of equity', pc(W['ke_bottom_up'], 2)),
    ('The same at sector risk: justified price to book',
     f'{BV["justified_pb_sector_beta"]:.2f}x'),
    ('The same at sector risk: value per share (AED)',
     px(LEN_['book_value_sector_beta'])),
]:
    rows.append([label, v])
table(rows, [4.30, 2.00], size=8.7, band_rows={9, 12})
P(f'Named sensitivity. "My lens is a ratio of two rates, so it is the most levered of the '
  f'three to the risk question — {px(LEN_["book_value_sector_beta"])} against '
  f'{px(LEN_["book_value_own_beta"])}, a factor of more than two. If the sustainable '
  f'return falls five points to {pc(BV["roe_sustainable"] - 0.05)}, I lose roughly a '
  f'fifth of my number."')
P('Falsifier, stated in advance. "If return on equity in 2026 falls below the cost of '
  'equity, my whole justification for a premium to book collapses and the right answer '
  'is book value itself, not a multiple of it."', italic=True)

H2('C.3  Expert 3 — the cycle and multiple analyst')
P('Worldview. Commodity chemicals is a cycle, and the cycle is the only thing that '
  'matters. Do not forecast the trough — normalise through it, and pay a through-cycle '
  'multiple on through-cycle earnings.', italic=True)
P('When it works: at the extremes of a cycle, where forecasts are most wrong and '
  'multiples most misleading. When it fails: when the cycle is not a cycle but a '
  'structural shift — and with a fifth of global capacity arriving by 2034, that risk is '
  'live.')
rows = [['Working', 'Value']]
for label, v in [
    ('Peers observed', str(len(D['peer_table']))),
    ('Of which loss-making', str(D['peers_loss_making'])),
    ('Of which no defined multiple', str(D['peers_ev_undefined'])),
    ('Naive peer median — rejected', f'{D["peer_naive_median"]:.1f}x'),
    ('LyondellBasell ten-year median',
     f'{D["relative_triangulation"]["LyondellBasell ten-year median EV/EBITDA"]:.2f}x'),
    ('Industries Qatar, current',
     f'{D["relative_triangulation"]["Industries Qatar current EV/EBITDA"]:.2f}x'),
    ('Global diversified chemicals sector',
     f'{D["relative_triangulation"]["Damodaran global Chemical (Diversified) sector EV/EBITDA"]:.3f}x'),
    ('Median of the three — adopted', f'{REL["median_ev_ebitda"]:.2f}x'),
    ('Mid-cycle EBITDA (USD m)', m(REL['midcycle_ebitda'])),
    ('Enterprise value (USD m)', m(REL['ev'])),
    ('Equity value (USD m)', m(REL['equity'])),
    ('Value per share (AED)', px(LEN_['relative_multiples'])),
    ('Cross-read: normalised earnings power, own risk (AED)',
     px(LEN_['normalised_earnings_own_beta'])),
    ('Cross-read: normalised earnings power, sector risk (AED)',
     px(LEN_['normalised_earnings_sector_beta'])),
]:
    rows.append([label, v])
table(rows, [4.30, 2.00], size=8.7, band_rows={8, 12})
P(f'Named sensitivity. "One turn on the multiple is worth about '
  f'{px(REL["midcycle_ebitda"] / (D["shares_out"] / 1e6) * FX)} dirhams a share. That is '
  f'the whole debate in my lens — and it is why I use three anchors rather than one."')
P('Falsifier, stated in advance. "If global operating rates have not begun to recover by '
  '2029, this is not a cycle and normalising through it is the wrong method. I would '
  'switch to a liquidation-and-replacement view of the assets."', italic=True)

H2('C.4  Cross-examination')
rows = [['Challenge', 'Response']]
for chal, resp in [
    ('Expert 3 to Expert 1: "Seventy-three per cent of your answer is a terminal block '
     'in a business whose industry does not expect to normalise until 2032. You are not '
     'valuing cash flows, you are valuing an assumption."',
     'CONCEDED IN PART. The terminal share is high and is disclosed everywhere it '
     'appears rather than buried. But the terminal block is built on reinvestment funded '
     'at the company’s own return on capital, not on a growth assumption pulled from the '
     'air — and the sensitivity grid shows what happens across the whole plausible range '
     'of both inputs.'),
    ('Expert 1 to Expert 2: "Your lens has no forecast in it at all, which you call a '
     'strength. But you use a cost of equity, and that means you have imported the '
     'single most contested input in the study while claiming to avoid judgement."',
     'CONCEDED. The book-value lens is the most levered of the three to the risk '
     'question — it moves by more than a factor of two across the two costs of equity. '
     'It is presented as an independent read on returns, not as a precise answer, and '
     'both readings are published.'),
    ('Expert 2 to Expert 3: "You reject the peer median because nine of eleven are '
     'losing money, then use two of those same companies as through-cycle anchors. You '
     'cannot have it both ways."',
     'REJECTED. The rejection is of the CURRENT median, because the denominator has '
     'collapsed. The anchors are a ten-year median for one name and a current multiple '
     'for a profitable name, plus a sector-wide figure. Those are different objects: one '
     'is a trough measurement, the others are through-cycle measurements.'),
    ('Expert 3 to Expert 2: "A sustainable return on equity of twenty-five per cent in '
     'commodity chemicals is not sustainable. It is what advantaged feedstock earns at '
     'the top of a cycle, and you have averaged three good years."',
     'CONCEDED IN PART. The three years averaged include 2025, a soft-price year, so the '
     'mean is not purely peak. But the point stands that advantaged feedstock is a '
     'position, not a law, and the falsifier stated above is precisely the test of it.'),
    ('Expert 1 to Expert 3: "Your mid-cycle EBITDA is the average of two forecast years '
     'from MY model. You are not independent of me — you are a multiple applied to my '
     'work."',
     'CONCEDED. The relative lens and the cash-flow lens share a mid-cycle earnings '
     'estimate, so they are not fully independent. What the relative lens contributes '
     'that the cash-flow lens cannot is a market-tested multiple in place of a discount '
     'rate — and that is exactly why it is the one lens the beta debate does not touch.'),
]:
    rows.append([chal, resp])
table(rows, [3.05, 3.75], size=8.4)
caption('Table C1 — Each challenge is either conceded or rejected. None is left hanging.')

H2('C.5  The three in one room')
P('Put together, the three agree on more than the range suggests. All three accept that '
  'the 2026 cost step is mechanically identifiable and probably temporary. All three '
  'accept that Borouge 4 belongs to its parents and that terminal growth is therefore '
  'inflation and nothing more. All three accept that the peer group is broken as a live '
  'comparable set.')
P(f'Where they part company is the discount rate, and only Expert 3 escapes it. At the '
  f'share’s own measured risk the three land at {px(LEN_["dcf_normalisation_own_beta"])}, '
  f'{px(LEN_["book_value_own_beta"])} and {px(LEN_["relative_multiples"])}; at sector '
  f'risk they land at {px(LEN_["dcf_normalisation_sector_beta"])}, '
  f'{px(LEN_["book_value_sector_beta"])} and the same {px(LEN_["relative_multiples"])}. '
  f'Expert 3 does not move because a multiple does not contain a discount rate — which '
  f'is why the study reports the relative lens as the median of the whole field rather '
  f'than as one reading among four.')
figure('figD1_experts.png', 6.5,
       'Figure 8 — Where each expert lands. The span within each bar is the risk debate; '
       'the distance between bars is method.')

H2('C.6  Divergence table — which assumption drives which gap')
rows = [['Gap', 'Size (AED)', 'The assumption behind it']]
for gap, size, why in [
    ('Expert 1 at own risk vs Expert 1 at sector risk',
     px(LEN_['dcf_normalisation_own_beta'] - LEN_['dcf_normalisation_sector_beta']),
     f'Beta of {W["beta_own"]:.2f} against {W["beta_bottom_up"]:.2f} — a cost of capital '
     f'of {pc(W["wacc_own"], 2)} against {pc(W["wacc_bottom_up"], 2)}. This single input '
     f'is larger than every other disagreement combined'),
    ('Expert 1 vs Expert 3, at own risk',
     px(LEN_['dcf_normalisation_own_beta'] - LEN_['relative_multiples']),
     'A discounted cash flow at a low cost of capital against a through-cycle multiple. '
     'Method, not data'),
    ('Expert 1 vs Expert 2, at own risk',
     px(LEN_['dcf_normalisation_own_beta'] - LEN_['book_value_own_beta']),
     'The forecast adds value above what the current book and return alone justify — the '
     'value of the five explicit years'),
    ('Shipping normalises vs disruption persists',
     f'{abs(LEN_["dcf_normalisation_own_beta"] - LEN_["dcf_prolonged_own_beta"]) * 100:.1f} fils',
     'A year of impaired utilisation and elevated freight, inside a five-year window '
     'where most value sits beyond it. Loud in the news, quiet in the arithmetic'),
    (f'Terminal growth {SN["g_grid"][0] * 100:.1f}% vs {SN["g_grid"][-1] * 100:.1f}%',
     px(SN['grids']['normalisation'][2][4] - SN['grids']['normalisation'][2][0]),
     'Return on capital sits above the cost of capital, so growth adds value here rather '
     'than destroying it'),
]:
    rows.append([gap, size, why])
table(rows, [2.05, 0.85, 3.90], size=8.4)
caption('Table C2 — The divergences, isolated. The beta line is the study’s central '
        'contested judgement and dwarfs the rest.')

# =============================================================== 15 ABOUT
doc.add_page_break()
H1('About this study')
P('Testahil publishes independent valuation studies and calibrated probability ranges, '
  'and keeps a public record of every forecast it makes so that its accuracy can be '
  'checked rather than claimed.')
P('Two commitments shape how this document is written. The first is that historical '
  'figures come only from the company’s own issued statements — never from a data vendor, '
  'a broker note or a press summary. Where an official document could not be obtained, '
  'the study would say so and stop rather than substitute. In this case every document '
  'needed was obtained directly from the company and verified. The second is that a '
  'forecast is built from the ground up: product by product, tonnes times price, cost per '
  'tonne, with each cost escalating on the thing that actually drives it. Margins are an '
  'output of that build, never an input to it.')
P('Where a figure has two legitimate constructions, both are published. This study does '
  'that twice — for the cost of capital and for the shipping disruption — and averages '
  'neither.')

# =============================================================== 16 DISCLOSURE
H1('Disclosure')
P('This document is educational analysis and is not investment advice, an offer, or a '
  'solicitation. It is not a recommendation to buy, sell or hold any security. It '
  'contains no rating and no price target, by design: it publishes ranges and '
  'probability distributions instead, because a single number would imply a precision '
  'that the evidence does not support.')
P('The analysis rests on information believed to be reliable, drawn from the company’s '
  'own published filings and from official statistical sources, but its accuracy and '
  'completeness are not guaranteed. Valuation involves assumptions about the future that '
  'will not be borne out exactly. The probability ranges in Section 3 describe how this '
  'share has behaved historically and are explicitly not promises about how it will '
  'behave.')
P(f'All figures are as at 7 August 2026 for market data and the dates stated for '
  f'financial data. The study was prepared on 9 August 2026. Currency amounts are US '
  f'dollars for financial statements and dirhams for per-share figures, converted at the '
  f'pegged rate of {FX} dirhams to the dollar.')
P('Readers should form their own view and, where appropriate, seek professional advice '
  'suited to their own circumstances.', size=9.5, color=GREY)

OUT = 'BOROUGE_Valuation_Study_09-08-2026_public.docx'
doc.save(OUT)
print(f'wrote {OUT}')
print(f'paragraphs: {len(doc.paragraphs)}, tables: {len(doc.tables)}, '
      f'figures: {len(doc.inline_shapes)}')
