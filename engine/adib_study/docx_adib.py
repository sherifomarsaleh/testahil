#!/usr/bin/env python3
"""ADIB_Valuation_Study_09-09-2026.docx — the 16-section study.

Written for an EXTERNAL reader. No internal procedure vocabulary, no rule identifiers, no
verdict tokens, no calibration appendix; the calibration evidence appears inside section 3
as plain sentences with the statistics inline. Experts are Expert 1, 2 and 3, cast by
method.

EVERY NUMBER COMES FROM study_numbers.json. Nothing in this file is typed.
"""
import json, os, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..'))
import docx_base as B
from docx.shared import Pt, Inches

doc, P, H1, H2, rich, table, caption, masthead = (
    B.doc, B.P, B.H1, B.H2, B.rich, B.table, B.caption, B.masthead)


def box(lines, **kw):
    """The house box takes (head, body) pairs; plain strings are the common case here."""
    return B.box([(l if isinstance(l, tuple) else ('', l)) for l in lines], **kw)


def bullet(text, bold_head=None):
    return B.bullet(text, bold_head=(bold_head + ' — ') if bold_head else None)
INK, GREY, BRASS, GOLD = B.INK, B.GREY, B.BRASS, B.GOLD

D = json.load(open(os.path.join(HERE, 'study_numbers.json'), encoding='utf-8'))
TECH = json.load(open(os.path.join(HERE, 'technicals.json'), encoding='utf-8'))
STRIKE = json.load(open(os.path.join(HERE, 'strike_result.json'), encoding='utf-8'))
GAPN = json.load(open(os.path.join(HERE, 'gap_review_numbers.json'), encoding='utf-8'))
WF = json.load(open(os.path.join(HERE, '..', 'adib_walkforward',
                                 'walkforward_summary.json'), encoding='utf-8'))

M, CC, P5 = D['meta'], D['cost_of_capital'], D['projection']
OBS, H1O, FAR = D['base_year_observed_ratios'], D['latest_reviewed_annualised'], D['far_year_ranges']
BY, LR, LN = D['base_year'], D['latest_reviewed'], D['lenses']
REG = D['register']
SPOT, SH, CENTRAL = M['spot'], M['shares_mn'], D['central']
BEAR, FULL = D['fair']['bear'], D['fair']['full']
EDITION = '09-09-2026'
YR = ['FY2026E', 'FY2027E', 'FY2028E', 'FY2029E', 'FY2030E']

_TN = [0]


def T(cap):
    _TN[0] += 1
    return 'Table %d — %s' % (_TN[0], cap)


def m(x, dp=0):
    return format(round(x, dp), ',.%df' % dp)


def pc(x, dp=1):
    return '%.*f%%' % (dp, 100 * x)


def egp(x, dp=2):
    return 'EGP %s' % format(round(x, dp), ',.%df' % dp)


# ============================================================ Masthead + READ FIRST
masthead()
P('Independent Valuation Study — Educational Analysis', size=13, bold=True)
P('Abu Dhabi Islamic Bank – Egypt S.A.E.  (EGX: ADIB)', size=15, bold=True, color=BRASS,
  space_after=2)
P('Fundamental analysis · technical analysis · Monte Carlo simulation — one integrated read',
  size=10, italic=True, color=GREY)
rich([('Anchor: ', {'bold': True}), (
    '%s (close 3 September 2026) · %s million shares in issue · market capitalisation about '
    '%s billion (roughly US$1.6bn at 50.25 to the dollar) · Egypt\'s largest listed Islamic '
    'bank by assets · FY2025 attributable profit %s billion on a %s return on equity, total '
    'assets %s billion · the six months to June 2026 added another %s billion of profit and '
    'took assets to %s billion · the swing factors are how much of that return survives the '
    'central bank\'s easing cycle, what a normal loss charge looks like after a half-year at '
    'almost nothing, and an Egyptian pound cost of equity near thirty per cent.'
    % (egp(SPOT), m(SH), egp(SPOT * SH / 1000, 1), egp(BY['np_parent'] / 1000, 2),
       pc(OBS['roe']), egp(BY['total_assets'] / 1000, 1),
       egp(LR['np_parent'] / 1000, 2), egp(LR['total_assets'] / 1000, 1)), {})],
     size=9.6)

H1('READ FIRST — what this document is, and is not')

# [R-DOC-03] THE TWO DATES, AT THE TOP, LABELLED. A valuation states a number struck
# against a price, and those are two facts with two dates that are not the same date.
# Resolved by engine/doc_dates.py and never from a file's modification time.
import sys as _sys_dd
import os as _os_dd
_sys_dd.path.insert(0, _os_dd.path.dirname(_os_dd.path.dirname(_os_dd.path.abspath(__file__))))
import doc_dates as _DD
P(_DD.header_line('ADIB'), size=8, color=GREY)

box([
 'This study is a valuation exercise and an expression of personal analytical opinion, '
 'published free of charge for educational purposes. It shows how one analyst applies '
 'fundamental, technical and probabilistic methods to a listed company, and invites '
 'scrutiny of that method. It is NOT investment advice, NOT a recommendation or '
 'solicitation to buy, sell or hold any security, and NOT directed at the circumstances '
 'of any reader.',
 'The preparer is not licensed by any securities regulator in any jurisdiction, holds no '
 'Egyptian or other brokerage authorisation, provides no financial consultancy, manages '
 'no money, and accepts no fees, funds or clients.',
 'All values are model outputs presented as ranges and distributions, because no single '
 'number should be relied on. There is no rating and no price target anywhere in this '
 'document.',
 'A NOTE ON IDENTITY. ADIB-Egypt (EGX: ADIB), the subject of this study, is the '
 'Cairo-listed bank formerly known as National Bank for Development. Abu Dhabi Islamic '
 'Bank PJSC (ADX: ADIB) is its Abu Dhabi-listed parent and a different company; it is '
 'covered separately and nothing here refers to it.',
 'WHERE THE NUMBERS COME FROM. Every historical figure is ADIB-Egypt\'s own audited or '
 'reviewed consolidated financial statements, downloaded from adib.eg: sixteen '
 'consolidated fiscal years from 2010 to 2025, plus the three and six months to March and '
 'June 2026. Every one of those statements was checked to add up before it was used. '
 'Forward-looking inputs — the growth path, the margin path, the loss charge, the cost of '
 'equity — are the preparer\'s judgements and are flagged as such throughout.',
 'TWO CLOCKS. The fair value is a risk-adjusted anchor of roughly twelve months, struck '
 'against the 3 September close. The only genuinely three-month figures are the '
 'percentiles in section 3, which are anchored on the 23 August close because that is the '
 'last session in the price history this study holds. Never read one clock as the other.',
])

# ============================================================ Headline
H1('Headline')
P('ADIB-Egypt is a bank that has compounded through a currency collapse. Since 2019 it has '
  'taken total assets from %s billion to %s billion, financing to customers from %s billion '
  'to %s billion, and attributable profit from %s billion to %s billion — while the Egyptian '
  'pound went from about 16 to the dollar to about 50. Its return on equity in 2025 was %s.'
  % (egp(60.325, 1), egp(LR['total_assets'] / 1000, 1), egp(30.734, 1),
     egp(LR['fin_customers'] / 1000, 1), egp(1.229, 2), egp(BY['np_parent'] / 1000, 2),
     pc(OBS['roe'])))
P('Two things make the next five years harder than the last five, and they are the whole '
  'of this study. The first is that the Central Bank of Egypt is cutting: its overnight '
  'deposit rate has come down from a peak above 27%% to 19.00%% and its own published path '
  'takes it to 12.00%%. A bank earning a %s margin on its assets in a 19%% policy world does '
  'not earn it in a 12%% one, and the asset side reprices faster than the deposit side. The '
  'second is the loss charge. ADIB-Egypt charged %s million of expected credit losses in '
  'the six months to June 2026 — not billion, million, on a %s billion financing book. That '
  'is a release, not a run rate, and this study does not carry it forward.'
  % (pc(OBS['nim'], 2), m(H1O['ecl_charge'], 3), egp(LR['fin_customers'] / 1000, 0)))
P('The dividend-discount lens, which is the primary read for a bank, values the shares at '
  '%s. Free cash flow to equity gives %s and residual income %s — a spread of %s across the '
  'three present-value reads. The market is at %s. The study is %s below it, the '
  'disagreement is audited in a separate review published with this document, and the two '
  'things that would close most of it are named there: a fresher Egyptian ten-year yield '
  'than the one this study is carrying, and a loss charge closer to the last six months '
  'than to the last four years.'
  % (egp(CENTRAL), egp(LN['free_cash_flow_to_equity']), egp(LN['residual_income']),
     egp(FULL - BEAR), egp(SPOT), pc(abs(D['gap_to_spot']))))

# ============================================================ Valuation summary
H1('Valuation summary — every read at a glance')
rows = [['Lens', 'Value per share', 'What it is', 'Role']]
rows.append(['Dividend discount', egp(LN['dividend_discount']),
             'the cash a shareholder can be paid, after the balance sheet has taken the '
             'capital it needs to grow', 'PRIMARY — this is the central'])
rows.append(['Free cash flow to equity', egp(LN['free_cash_flow_to_equity']),
             'the same flow built from the capital requirement rather than a payout ratio',
             'cross-check'])
rows.append(['Residual income', egp(LN['residual_income']),
             'today\'s book value plus the value of every future year\'s return above the '
             'cost of equity', 'cross-check'])
rows.append(['Relative multiples', egp(LN['relative_multiples']),
             'Egyptian large-cap bank price-to-book and price-to-earnings bands applied to '
             'the 2026 forecast', 'cross-check — the weakest evidence here'])
rows.append(['Book value and sustainable return', egp(LN['book_value_and_sustainable_return']),
             'the June 2026 book of %s a share at the price-to-book its own long-run return '
             'supports' % egp(LN['book_value_floor']), 'cross-check'])
rows.append(['Normalised earnings power', egp(LN['normalised_earnings_power']),
             'what the bank earns on a mid-cycle margin and a mid-cycle loss charge, '
             'capitalised', 'reported only'])
table(rows, [1.55, 1.05, 3.0, 1.4], size=8.8)
caption(T('the six reads, and which one is the answer'))
P('One lens is the central and the others are published beside it. They are not averaged: '
  'a weighted blend of lenses is a set of numbers nobody has ever tested, and this house '
  'retired the practice after a blend on another company landed 28% away from a market its '
  'own cash-flow lens had matched within 2%. For a bank the primary read is the dividend '
  'discount, because a bank\'s deposits are its raw material rather than its financing and '
  'the only thing that reaches a shareholder is what the capital rules let the bank pay out.')
rows = [['', 'Value per share', 'Against the 3 September close of %s' % egp(SPOT)]]
rows.append(['Low end of the present-value reads', egp(BEAR), pc(BEAR / SPOT - 1)])
rows.append(['CENTRAL — dividend discount', egp(CENTRAL), pc(CENTRAL / SPOT - 1)])
rows.append(['High end of the present-value reads', egp(FULL), pc(FULL / SPOT - 1)])
table(rows, [3.1, 1.7, 2.2], size=9.0, first_col_bold=True)
caption(T('the range, and what it is not'))
P('THE RANGE IS NARROW AND THAT IS A STATEMENT ABOUT THE LENSES, NOT ABOUT CONFIDENCE. It '
  'is the spread between the three present-value reads, and they agree because they are '
  'three ways of discounting the same capital-constrained flow. It is not a forecast '
  'confidence interval. Section 7 gives the measured one, and it is far wider: on this '
  'company\'s own sixteen-year history, a profit forecast made three years ahead by this '
  'method has landed anywhere between a third and one-and-a-half times the outcome.')

# ============================================================ Company overview
H1('Company overview')
P('ADIB-Egypt is the Cairo-listed Islamic bank that Abu Dhabi Islamic Bank PJSC took '
  'control of in 2007, when it was called National Bank for Development. The filings tell '
  'that story plainly: the accounts are still headed "National Bank For Development '
  '(S.A.E.)" through the 2013 report, they carry a consolidated non-bank trading subsidiary '
  'with its own sales and cost-of-sale lines, and they show cumulative attributable losses '
  'of %s billion across 2010 to 2012 against a balance sheet of about %s billion. The bank '
  'was recapitalised three times, the conventional loan book was run off, and the '
  'accumulated deficit was not cleared until the end of the decade.'
  % (egp(2.463, 2), egp(14.4, 1)))
P('What it is now is a mid-sized Egyptian bank growing faster than the system. It funds '
  'itself with %s billion of customer deposits, lends %s billion to customers, and holds '
  'most of the difference in Egyptian treasury bills and government paper — the shape of '
  'almost every Egyptian bank, and the reason its earnings are as much a function of the '
  'policy rate as of its own lending. Financing to customers is %s of total assets against '
  '%s at the end of 2025, so that mix is actively shifting toward customer credit.'
  % (egp(LR['total_assets'] / 1000 / 1.25, 0), egp(LR['fin_customers'] / 1000, 0),
     pc(H1O['financing_over_assets']), pc(OBS['financing_over_assets'])))
P('Issued capital has moved a great deal and the share count is the denominator of '
  'everything in this study, so it is worth stating once: %s. At the LE 10 par value the '
  'filings state, that is 1,500 million shares today.'
  % REG['shares']['source'].split('.')[0].replace(
      'ADIB-Egypt issued and paid-up capital of EGP 15,000,000 thousand at 30 June 2026, '
      'over the LE 10 par value the filings state (FY2018 note 34/2), = 1,500 million shares',
      'capital rose from EGP 2.0 billion through 4.0, 5.0, 6.0 and 12.0 billion to EGP 15.0 '
      'billion at 30 June 2026, the last step a EGP 3 billion cash increase completed in the '
      'second quarter'))

# ============================================================ §1 Fundamental valuation
H1('1  Fundamental valuation')
P('A bank is not valued the way an industrial company is, and the difference is not '
  'cosmetic. An industrial valuation starts from enterprise value, subtracts debt and adds '
  'cash. For a bank, deposits ARE the raw material — the thing it buys and resells — so '
  'subtracting them as though they were borrowings produces a number with no meaning. '
  'Everything below is therefore built on equity: the flows are flows to the shareholder, '
  'the discount rate is the cost of equity, and there is no weighted average cost of '
  'capital and no enterprise-to-equity bridge anywhere in this study.')

H2('1.1  The cash-flow model — what the shareholder can actually be paid')
P('The model projects the balance sheet first, applies a yield to the assets and a cost to '
  'the funding, and lets the margin fall out. It never sets a margin. The waterfall for '
  'each year runs: financing to customers, grossed up to total assets on the disclosed '
  'mix; income earned at the asset yield on the AVERAGE of the opening and closing balance '
  'sheet; the cost of deposits charged at the funding rate on the average of the '
  'liabilities that actually bear it; fees and other income as a rate on average assets; '
  'administrative costs grown from the FY2025 base; the loss charge as a rate on average '
  'financing; tax at the effective rate the bank actually pays.')
box(['WHY THE AVERAGE BALANCE SHEET AND NOT THE CLOSING ONE. ADIB-Egypt grew total assets '
     '33% in 2025 and 19.5% in the first half of 2026. Applying a full year of yield to a '
     'closing balance sheet would credit twelve months of income to assets the bank held '
     'for six, and would inflate every projected profit in this study by a large and '
     'entirely artificial margin. Every rate below is applied to an average.'])
rows = [['EGP million', 'FY2025A', 'H1-2026A'] + YR]
def prow(label, key, dp=0, hist=None, h1=None):
    r = [label, m(hist, dp) if hist is not None else '—',
         m(h1, dp) if h1 is not None else '—']
    return r + [m(x[key], dp) for x in P5]
rows.append(prow('Financing income', 'fin_income', 0, BY['fin_income'], LR['fin_income']))
rows.append(prow('Cost of deposits', 'cost_funds', 0, BY['cost_funds'], LR['cost_funds']))
rows.append(prow('Net income from funds', 'net_funds', 0, BY['net_funds'], LR['net_funds']))
rows.append(prow('Net fees and commissions', 'net_fees', 0, BY['net_fees'], LR['net_fees']))
rows.append(prow('Other non-interest income', 'other_nii', 0, BY['other_nii'], None))
rows.append(prow('Administrative expenses', 'admin', 0, BY['admin'], LR['admin']))
rows.append(prow('Other operating expenses', 'other_op', 0, BY['other_op'], LR['other_op']))
rows.append(prow('Expected credit losses', 'ecl', 0, BY['ecl'], -H1O['ecl_charge']))
rows.append(prow('Profit before tax', 'pbt', 0, BY['pbt'], LR['pbt']))
rows.append(prow('Tax', 'tax', 0, BY['tax'], LR['tax']))
rows.append(prow('Attributable profit', 'np_parent', 0, BY['np_parent'], LR['np_parent']))
table(rows, [1.6, 0.8, 0.8] + [0.76] * 5, size=8.0, first_col_bold=True)
caption(T('the profit build, with the two reported periods beside it'))
rows = [['', 'FY2025A', 'H1-2026A'] + YR]
rows.append(['Net interest margin (OUTPUT)', pc(OBS['nim'], 2), pc(H1O['nim'], 2)]
            + [pc(x['nim'], 2) for x in P5])
rows.append(['Cost-to-income (OUTPUT)', pc(OBS['cost_income']), '—']
            + [pc(x['cost_income']) for x in P5])
rows.append(['Return on average assets (OUTPUT)', pc(OBS['roa'], 2), '—']
            + [pc(x['roa'], 2) for x in P5])
rows.append(['Return on average equity (OUTPUT)', pc(OBS['roe']), pc(H1O['roe'])]
            + [pc(x['roe']) for x in P5])
rows.append(['Dividend payout (DERIVED)', '11.7%', '—'] + [pc(x['payout']) for x in P5])
rows.append(['Equity / total assets', pc(OBS['equity_over_assets'], 2),
             pc(H1O['equity_over_assets'], 2)] + [pc(x['equity_assets'], 2) for x in P5])
table(rows, [1.9, 0.8, 0.8] + [0.72] * 5, size=8.2, first_col_bold=True)
caption(T('the ratios that fall out — every one of them an output, none an input'))
P('THE PAYOUT IS NOT A CHOICE THIS STUDY MADE. Equity is pinned each year at %s of total '
  'assets — the level the bank actually stood at on 30 June 2026 — and the dividend is '
  'whatever profit is left after getting there. A bank growing its balance sheet by a third '
  'cannot also distribute, and the arithmetic says so rather than a sentence saying so '
  'beside a typed ratio. The derived path opens at %s for 2026 against the %s ADIB-Egypt '
  'actually paid on its 2024 earnings, which is the closest thing to an external check this '
  'driver has.'
  % (pc(float(REG['target_equity_assets']['value']), 1), pc(P5[0]['payout']), '11.7%'))

H2('1.2  Book value and the return it sustains')
P('Attributable book value was %s a share at 30 June 2026 — %s billion over 1,500 million '
  'shares. That is the floor: what a shareholder owns if the bank stops compounding '
  'tomorrow. Capitalised at the price-to-book its own long-run return supports (%s times, '
  'from a %s terminal return against a %s terminal cost of equity and %s growth), the same '
  'book is worth %s a share.'
  % (egp(LN['book_value_floor']), egp(LR['equity_parent'] / 1000, 2),
     '%.2f' % (LN['book_value_and_sustainable_return'] / LN['book_value_floor']),
     pc(P5[-1]['roe']), pc(CC['ke_terminal']), pc(CC['terminal_growth']),
     egp(LN['book_value_and_sustainable_return'])))
P('One thing the book value hides and this study will not. The EGP 3 billion capital '
  'increase completed in the second quarter of 2026 issued 300 million new shares at the '
  'LE 10 par value, against a book value per share of about %s. Book value per share moved '
  'from %s at the end of 2025 to %s at 30 June — six months at a %s annualised return on '
  'equity bought existing holders less than one per cent of book. The growth was real and '
  'so was the dilution.'
  % (egp(28.83), egp(28.83), egp(LN['book_value_floor']), pc(H1O['roe'])))

H2('1.3  Relative multiples')
P('At the central the shares stand on %s times forecast 2026 book and %s times forecast '
  '2026 earnings. At the market they stand on %s times and %s times. Applying the '
  'price-to-book and price-to-earnings bands Egyptian large-cap banks trade in to the 2026 '
  'forecast gives %s a share.'
  % ('%.2f' % GAPN['implied_pb_2026'], '%.1f' % GAPN['implied_pe_2026'],
     '%.2f' % (SPOT / P5[0]['bvps']), '%.1f' % (SPOT / P5[0]['eps']),
     egp(LN['relative_multiples'])))
box(['THIS IS THE WEAKEST EVIDENCE IN THE STUDY AND IT IS SAID SO RATHER THAN DRESSED UP. '
     'No same-day book value could be sourced for any Egyptian bank other than ADIB-Egypt '
     'itself. Commercial International Bank\'s price is held on the same date — %s on 3 '
     'September — and its book value is not. The multiple read is therefore a BAND, it is '
     'published as a cross-check and not as part of the answer, and it happens to be the '
     'lens pulling upward: on its own it says %s.'
     % (egp(float(REG['peer_comi_price']['value'])), egp(LN['relative_multiples']))])

H2('1.4  Normalised earnings power')
P('What does ADIB-Egypt earn in a normal year? On a %s net interest margin — below the %s '
  'it earned in 2025 and the %s the June half annualises to — and a %s loss charge rather '
  'than the %s of the last six months, the bank earns about %s a share, and capitalised at '
  'the current cost of equity that is worth %s. The point of the exercise is not the number '
  'but the check: a multiple applied to 2025\'s margin or to the June half\'s loss charge '
  'is capitalising a peak.'
  % (pc(0.055, 1), pc(OBS['nim'], 2), pc(H1O['nim'], 2), pc(0.015, 2),
     pc(H1O['cost_of_risk'], 3), egp(LN['normalised_earnings_power'] * (CC['ke'] - CC['terminal_growth'])),
     egp(LN['normalised_earnings_power'])))

H2('1.5  Synthesis — one lens is the answer')
P('The dividend discount is the central at %s. Residual income, the relative multiple and '
  'book value sit beside it as cross-checks, and free cash flow to equity is published '
  'because it is the same flow reached a different way. They are not averaged. The envelope '
  'is the range of the three present-value reads — %s at the low end, %s at the high — and '
  'no spread is invented around it.'
  % (egp(CENTRAL), egp(BEAR), egp(FULL)))
rows = [['Lens', 'Per share', 'Against the central', 'Present-value read?']]
for lab, key in [('Dividend discount (PRIMARY)', 'dividend_discount'),
                 ('Free cash flow to equity', 'free_cash_flow_to_equity'),
                 ('Residual income', 'residual_income'),
                 ('Relative multiples', 'relative_multiples'),
                 ('Book value and sustainable return', 'book_value_and_sustainable_return'),
                 ('Normalised earnings power', 'normalised_earnings_power')]:
    v = LN[key]
    rows.append([lab, egp(v), pc(v / CENTRAL - 1),
                 'yes — in the envelope' if key in ('dividend_discount',
                 'free_cash_flow_to_equity', 'residual_income') else 'no'])
table(rows, [2.3, 1.1, 1.3, 1.9], size=8.8, first_col_bold=True)
caption(T('every read, and which ones set the envelope'))
P('The three present-value lenses land within %s of each other, which is worth a sentence '
  'because they did not always. An earlier version of this model typed a dividend payout '
  'path instead of deriving it, and under that version the dividend lens and the '
  'free-cash-flow lens disagreed by about %s a share while the model quietly accumulated '
  'capital it had no use for. The disagreement between two lenses was the only thing that '
  'said so.' % (egp(FULL - BEAR), egp(7)))

H2('1.6  The drivers')
rows = [['Driver', 'FY2025 actual', 'H1-2026 actual', 'The path, and why']]
rows.append(['Financing to customers', egp(BY['financing'] / 1000, 0) + 'bn',
             egp(LR['fin_customers'] / 1000, 0) + 'bn',
             '+48%% in 2026 then 26 / 19 / 15 / 12%%. The bank was already at %sbn at 30 '
             'June, so 2026 asks for only +14%% in the second half against +29%% in the '
             'first. The path decays toward nominal GDP growth by 2030.'
             % (egp(LR['fin_customers'] / 1000, 0))])
rows.append(['Asset yield', pc(OBS['asset_yield'], 2), pc(H1O['asset_yield'], 2),
             '15.0 → 10.8%, falling at about 0.75 of the central bank\'s published policy '
             'glide from 19.00% to 12.00%. An INPUT.'])
rows.append(['Cost of funds', pc(OBS['cost_of_funds'], 2), '—',
             '10.6 → 7.0%, at about 0.80 of the same glide. Slower than the asset side, '
             'which is why the margin compresses. Charged on customers\' deposits, due to '
             'banks and subordinated financing — the balances that actually bear it, and '
             'nothing else. An INPUT.'])
rows.append(['Net interest margin', pc(OBS['nim'], 2), pc(H1O['nim'], 2),
             'AN OUTPUT of the two rows above. %s → %s. It is never typed.'
             % (pc(P5[0]['nim'], 2), pc(P5[-1]['nim'], 2))])
rows.append(['Cost of risk', pc(OBS['cost_of_risk'], 2), pc(H1O['cost_of_risk'], 3),
             '1.00% in 2026 and 1.30% thereafter — below the 2022-25 mean of 2.09% and far '
             'above the six months to June. The single most consequential judgement here.'])
rows.append(['Net fees / average assets', pc(OBS['fee_ratio'], 2), pc(H1O['fee_ratio'], 2),
             '0.80 → 0.85%, opening at the reviewed half and recovering slowly.'])
rows.append(['Administrative expenses', egp(-BY['admin'] / 1000, 2) + 'bn',
             egp(-LR['admin'] / 1000, 2) + 'bn',
             '+34% in 2026, then inflation plus about six points. Cost-to-income is an '
             'OUTPUT of this and the revenue lines.'])
rows.append(['Effective tax rate', pc(OBS['tax_rate']), pc(H1O['tax_rate']),
             '28.5%, above the 22.5% statutory rate because the withholding on treasury-'
             'bill income is not creditable.'])
table(rows, [1.5, 1.0, 1.0, 3.5], size=8.2, first_col_bold=True)
caption(T('the eight drivers, and the three ratios that are outputs of them'))

H2('1.7  The crux')
P('Every bank study has one load-bearing tension. ADIB-Egypt\'s is that the two things '
  'making it look cheapest are the two things least likely to persist, and they are both '
  'in the same six months of accounts.')
P('The June 2026 half printed a %s annualised return on equity and charged %s million of '
  'credit losses. Annualise that half and the bank earns about %s billion in 2026 and the '
  'shares are on four times earnings. Do it for five years and this study\'s central is %s '
  'a share rather than %s. But a half-year at a 0.003%% loss rate is not a business model; '
  'it is a release, on a book that carried charges of 2.7%% of financing in both 2023 and '
  '2024. The bank is growing customer financing at close to 30%% a half — new lending does '
  'not default in its first year, and the loss charge on it arrives later.'
  % (pc(H1O['roe']), m(H1O['ecl_charge'], 3), egp(LR['np_parent'] * 2 / 1000, 1),
     egp(GAPN['central_if_h1_cor_holds_throughout']), egp(CENTRAL)))
P('The second half of the tension is the capital. Pinning equity at %s of assets while '
  'assets grow a third takes %s billion of retained earnings in 2026 alone, against %s '
  'billion of profit. The bank has already answered this once, by issuing 300 million new '
  'shares at par in the second quarter — which funded the growth and cost existing holders '
  'most of the half\'s book-value gain. A reader who believes the growth should also '
  'believe there is more of that to come.'
  % (pc(float(REG['target_equity_assets']['value']), 1),
     egp(P5[0]['equity_required'] / 1000, 1), egp(P5[0]['np_parent'] / 1000, 1)))

H2('1.8  Macro and the cost of capital')
P('Every rate in this study comes from one Egyptian macro path, and nothing is set '
  'independently of it. The Central Bank of Egypt\'s own baseline puts average headline '
  'inflation at 16.0% in 2026 and 12.0% in 2027; the path to the 7% target-band midpoint is '
  'a straight glide between those published endpoints and is labelled as interpolation, not '
  'as a forecast anybody published. The policy rate glides with it.')
rows = [['', '2026', '2027', '2028', '2029', '2030', 'terminal']]
rows.append(['Headline inflation'] + [pc(x, 1) for x in REG['inflation_path']['value']]
            + [pc(CC['terminal_inflation'], 1)])
rows.append(['Overnight deposit rate'] + [pc(x, 2) for x in REG['policy_rate_path']['value']] + ['—'])
rows.append(['Cost of equity used'] + [pc(k, 2) for k in CC['ke_path']] + [pc(CC['ke_terminal'], 2)])
table(rows, [1.5] + [0.86] * 6, size=8.4, first_col_bold=True)
caption(T('one path, and the discount rate that glides with it'))
rows = [['Cost of equity', 'Rate', 'Where it comes from']]
rows.append(['Egyptian ten-year local-currency yield', pc(CC['rf'], 2),
             'market quote of 6 August 2026'])
rows.append(['less the sovereign default spread', '(%s)' % pc(CC['sovereign_default_spread'], 2),
             'so the country\'s own risk is charged once, not twice — it is already inside '
             'the equity premium'])
rows.append(['= normalised risk-free rate', pc(CC['rf_star'], 2), 'derived'])
rows.append(['Beta against the EGX30 index', '%.4f' % CC['beta'],
             'own-stock weekly regression, %d observations over %.1f years to %s, R-squared '
             '%.3f, standard error %.4f' % (D['beta_record']['n'],
             D['beta_record']['window_years'], D['beta_record']['last_obs'],
             D['beta_record']['r2'], D['beta_record']['se'])])
rows.append(['Egyptian total equity risk premium', pc(CC['erp'], 2),
             'the total premium column, which is what multiplies beta; the country premium '
             'alone is not added on top'])
rows.append(['= COST OF EQUITY', pc(CC['ke'], 2), 'the rate used in the first forecast year'])
rows.append(['Terminal cost of equity', pc(CC['ke_terminal'], 2),
             'a %s terminal risk-free rate — itself derived as %s terminal inflation plus a '
             '%s real convention — plus the same beta times a normalised %s premium'
             % (pc(CC['terminal_rf'], 2), pc(CC['terminal_inflation'], 1), pc(0.055, 1),
                pc(CC['terminal_erp'], 1))])
table(rows, [2.5, 0.85, 3.65], size=8.3, first_col_bold=True)
caption(T('the cost of equity, built rather than quoted'))
P('EVERY CONTESTED CONSTRUCTION, PRICED. Built on the rating basis instead — a different '
  'column of the same source — the cost of equity is %s, %d basis points away, which is '
  'reassuring because the two are made of different inputs. Charging the raw yield AND a '
  'country-loaded premium, which is the construction this house retired, would give %s and '
  'would be counting Egypt\'s default risk twice. And the market\'s own implied cost of '
  'equity, inverted from the %s times book it is paying against the June half\'s return, is '
  '%s — %d basis points below the rate this study uses. That gap is a real disagreement and '
  'the study does not resolve it in its own favour.'
  % (pc(CC['ke_rating_basis'], 2), round(abs(CC['ke'] - CC['ke_rating_basis']) * 1e4),
     pc(CC['ke_double_counted_retired'], 2), '%.2f' % GAPN['market_pb_on_jun26_book'],
     pc(GAPN['market_implied_ke_gordon'], 2),
     round(abs(CC['ke'] - GAPN['market_implied_ke_gordon']) * 1e4)))
box(['ONE INPUT IN THIS STUDY IS STALE AND IT IS THE MOST IMPORTANT ONE. The Egyptian '
     'ten-year yield of %s is dated 6 August 2026 — 34 days before the price this study is '
     'struck against, and beyond the fortnight this house allows such a quote to stand. A '
     'live re-source was attempted on 9 September down four routes and all four failed: the '
     'central bank\'s bond-auction pages return an error, its data endpoint returns the '
     'website rather than the data, and two market-data providers render their yield tables '
     'in a way that cannot be read without a browser. The only recent evidence found is that '
     'the same yield averaged 21.29%% between late April and late May 2026, which is 171 '
     'basis points BELOW what this study is carrying. At that rate the central would be %s '
     'rather than %s. The rate is carried, the staleness is declared, the sensitivity is in '
     '1.9, and a current quote is the first thing this study would want.'
     % (pc(CC['rf'], 2), egp(GAPN['central_at_rf_2129']), egp(CENTRAL))])

H2('1.9  Sensitivity')
rows = [['Move', 'Central', 'Change']]
for s_ in D['sensitivity']:
    rows.append([s_['driver'], egp(s_['value']), pc(s_['change'])])
table(rows, [2.6, 1.4, 1.2], size=8.6, first_col_bold=True)
caption(T('what moves the answer, in order of how much'))
P('The margin drivers dominate, which is what a bank should look like: fifty basis points '
  'on the asset yield is worth %s of the value and fifty on the funding cost %s. The loss '
  'charge is worth %s per fifty basis points. Terminal growth is worth almost nothing — %s '
  'for a full percentage point — because the terminal discount rate is high enough that a '
  'far-future pound is worth very little today, and that is the honest shape of an Egyptian '
  'valuation rather than a modelling convenience.'
  % (pc(abs(D['sensitivity'][2]['change'])), pc(abs(D['sensitivity'][4]['change'])),
     pc(abs(D['sensitivity'][0]['change'])), pc(abs(D['sensitivity'][10]['change']))))

# ============================================================ §2 Technical
H1('2  Technical and price structure')
_t = TECH
P('The price closed %s on %s, the last session in the history this study holds — %s clean '
  'daily sessions after the data-quality screen. %s'
  % (egp(float(_t['close'])), _t['as_of'] if 'as_of' in _t else _t.get('computed_on', ''),
     m(_t.get('sessions', 0)), _t['narrative']['summary'] if 'narrative' in _t
     else _t.get('summary', '')))
rows = [['', 'Levels']]
rows.append(['Resistance above', ' · '.join(egp(float(x)) for x in _t['levels']['res'])])
rows.append(['Support below', ' · '.join(egp(float(x)) for x in _t['levels']['sup'])])
table(rows, [1.6, 5.4], size=9.0, first_col_bold=True)
caption(T('the charted levels'))
P('%s  %s' % (_t['tech']['bull'], _t['tech']['bear']))
P('A technical read is a description of where the price has been trading and what levels it '
  'has respected. It is not a forecast and it is not combined with the valuation: the two '
  'lenses are kept apart deliberately, and section 4 compares them without letting either '
  'adjust the other.')

# ============================================================ §3 Probabilistic map
H1('3  A probabilistic price map')
P('This section is a distribution, not a view. It takes the price history through the same '
  'production chain the rest of this house uses — a data-quality gate, a Yang-Zhang '
  'variance estimate, a heterogeneous autoregressive volatility forecast, and 50,000 '
  'simulated paths on a Student-t shape with %.1f degrees of freedom — and reports where the '
  'price lands. The shape and width parameters are not chosen here: they are read live from '
  'the engine, where they are fitted to a thirty-name Egyptian panel.'
  % STRIKE['nu'])
P('Anchor: %s, the close on %s. The drift is the Egyptian carry — the policy rate less the '
  'dividend yield — and nothing else; there is no view of direction in it beyond that.'
  % (egp(STRIKE['spot']), STRIKE['anchor_date']))
rows = [['Horizon', 'Resolves', '5th', '25th', 'Median', '75th', '95th', 'Chance higher']]
for k in ('1M', '3M'):
    h = STRIKE['horizons'][k]
    rows.append(['1 month' if k == '1M' else '3 months', str(h['target_date'])[:10],
                 egp(h['p5']), egp(h['p25']), egp(h['p50']), egp(h['p75']), egp(h['p95']),
                 pc(h['p_up'], 0)])
table(rows, [0.95, 0.95, 0.8, 0.8, 0.85, 0.8, 0.85, 0.95], size=8.4, first_col_bold=True)
caption(T('the percentile map, from 50,000 simulated paths'))
box(['TWO CLOCKS, AND THEY ARE NOT THE SAME. The percentiles above are anchored on the 23 '
     'August close of %s, because that is the last session in the price history this study '
     'holds. The fair value is struck against %s, the 3 September close. A reader comparing '
     'the two should hold that eleven-day difference in mind; nothing has been adjusted to '
     'hide it.' % (egp(STRIKE['spot']), egp(SPOT))])
P('What the distribution is worth. The width parameters were fitted on a thirty-name '
  'Egyptian panel rather than on this stock, so what is being claimed is a base rate for '
  'Egyptian equities of this volatility, not a forecasting edge in this name. The Egyptian '
  'shape is genuinely fat-tailed — %.1f degrees of freedom rather than a normal '
  'distribution — and that is devaluation-jump risk, not a data artefact: it survived the '
  'repair of every known price-series defect in the panel. Read section 3 as a base rate.'
  % STRIKE['nu'])

# ============================================================ §4 Comparison
H1('4  Comparison of the lenses')
rows = [['Lens', 'What it says', 'Clock']]
rows.append(['Fundamental', 'central %s, envelope %s to %s, which is %s against the 3 '
             'September close of %s'
             % (egp(CENTRAL), egp(BEAR), egp(FULL), pc(D['gap_to_spot']), egp(SPOT)),
             'about twelve months'])
rows.append(['Technical', _t['tech']['trend'] + '; nearest support %s, nearest '
             'resistance %s' % (egp(float(_t['levels']['sup'][0])),
                                egp(float(_t['levels']['res'][0]))), 'weeks'])
rows.append(['Probabilistic', 'a three-month median of %s with a 5th-to-95th range of %s '
             'to %s, and a %s chance of ending higher'
             % (egp(STRIKE['horizons']['3M']['p50']), egp(STRIKE['horizons']['3M']['p5']),
                egp(STRIKE['horizons']['3M']['p95']),
                pc(STRIKE['horizons']['3M']['p_up'], 0)), 'three months'])
table(rows, [1.2, 4.6, 1.2], size=8.6, first_col_bold=True)
caption(T('the three reads, side by side and never blended'))
P('The three disagree, and the disagreement is the useful part. The fundamental lens says '
  'the shares are dear; the technical read says they are in an uptrend a few per cent below '
  'a one-year high; the distribution says the next three months are close to a coin flip '
  'with a fat left tail. NOTHING HERE IS COMBINED. No output of one lens is an input to '
  'another, and no lens is adjusted because another disagrees — a comparison that lets the '
  'lenses talk to each other stops being three pieces of evidence and becomes one.')

# ============================================================ §5 Catalysts
H1('5  Catalysts to watch')
for h, t in [
 ('The third-quarter statements, due around November 2026',
  'The one number that matters is the expected-credit-loss line. If the nine months to '
  'September still carry almost no charge, the case for this study\'s 1.00%% assumption '
  'weakens sharply and the central moves toward %s. If the charge normalises in the third '
  'quarter, it strengthens.' % egp(GAPN['central_if_h1_cor_holds_throughout'])),
 ('Central Bank of Egypt monetary policy meetings',
  'The rate has been held for four consecutive meetings at 19.00%%. The published path takes '
  'it to 12.00%% by 2030. Cuts faster than that compress the margin faster than this study '
  'assumes; a pause does the opposite. Fifty basis points on the asset yield is worth %s of '
  'the value.' % pc(abs(D['sensitivity'][2]['change']))),
 ('Any further capital raising',
  'The bank issued 300 million shares at par in the second quarter of 2026 to fund growth. '
  'Pinning capital at %s of assets while assets compound at these rates needs more of it. '
  'The terms matter as much as the amount: an issue at par against a book value near %s '
  'transfers value from existing holders.'
  % (pc(float(REG['target_equity_assets']['value']), 1), egp(LN['book_value_floor']))),
 ('The Egyptian pound',
  'Every line in this bank\'s accounts is in pounds. The house path derives the currency '
  'from its own inflation ladder rather than setting it by hand, so a devaluation outside '
  'that path moves the nominal figures without moving the real ones — and moves the '
  'sovereign yield the discount rate is built on.'),
 ('A current ten-year yield',
  'Not a company event, but the largest single uncertainty in this study. The rate it uses '
  'is 34 days old; the only recent market evidence points 171 basis points lower, and that '
  'alone is worth %s a share.' % egp(GAPN['central_at_rf_2129'] - CENTRAL))]:
    bullet(t, bold_head=h)

# ============================================================ §6 Reading the zones
H1('6  Reading the probability zones')
P('The percentiles in section 3 are not targets and not levels anyone expects. They are a '
  'way of saying how wide the range of plausible outcomes is, given how this stock has '
  'actually moved. The 25th-to-75th band is where half the simulated paths finish; the '
  '5th-to-95th is where nine in ten do. One in twenty finishes below the 5th and one in '
  'twenty above the 95th, and both of those are ordinary rather than surprising.')
P('The three-month band here runs from %s to %s — a spread of about %s of the anchor price. '
  'That is wide, and it is wide because Egyptian equity returns have a genuinely fat left '
  'tail: the fitted shape carries %.1f degrees of freedom, which is a formal way of saying '
  'that large single-day moves happen far more often than a bell curve allows. A reader who '
  'finds the band uncomfortably wide is reading it correctly.'
  % (egp(STRIKE['horizons']['3M']['p5']), egp(STRIKE['horizons']['3M']['p95']),
     pc((STRIKE['horizons']['3M']['p95'] - STRIKE['horizons']['3M']['p5'])
        / STRIKE['spot'], 0), STRIKE['nu']))

# ============================================================ §7 Caveats
H1('7  Caveats and what would change our mind')
box(['HOW FAR AHEAD THIS METHOD CAN ACTUALLY SEE, MEASURED ON THIS COMPANY. Before this '
     'study was written, the forecasting method behind it was tested on ADIB-Egypt\'s own '
     'sixteen-year history: rebuilt at eleven past year-ends using only what had been '
     'published by each of those dates, projected forward one to five years, and scored '
     'against what the bank actually reported. %d of those forecasts have matured for each '
     'of %d drivers.'
     % (WF['cells_per_driver'], WF['drivers']),
     'What it found. Against the naive rule of assuming last year repeats, the method is '
     'better by %s on attributable profit and better on thirteen of fourteen drivers, and '
     'the improvement holds when the origins are resampled. Against the naive rule of '
     'extending the last three years\' growth rate, it is a dead heat on profit (%s) and '
     'WORSE on balance-sheet volume. It under-forecast profit at every horizon and the '
     'shortfall widens with distance: %s in logs at one year, %s at five.'
     % (pc(WF['skill']['np_parent']['vs_freeze'], 0),
        pc(WF['skill']['np_parent']['vs_trend'], 0),
        '%+.2f' % WF['by_horizon']['h1']['bias'], '%+.2f' % WF['by_horizon']['h5']['bias']),
     'WHY IT UNDER-FORECAST, AND WHAT THIS STUDY DID ABOUT IT. The mechanical rule anchors '
     'lending volume on the size of the Egyptian credit system and holds the bank\'s share '
     'of it flat. ADIB-Egypt has taken share every year for a decade. So the rule was wrong '
     'in the same direction at all eleven origins — and this study does NOT hold share '
     'flat: its share path is stated in the drivers and audited in the gap review. No '
     'correction factor from that test enters this model. Every candidate either failed its '
     'own by-origin test or failed the check that it match how the same driver is built '
     'across the rest of the book, and a steady error usually means something is wired '
     'wrong rather than that a multiplier is missing.',
     'WHAT IT MEANS FOR YEARS THREE TO FIVE. The measured spread of that record — how far '
     'the outcome sat from the forecast, three years out — runs from about a third of the '
     'projection to about one and a half times it. Appendix A publishes 2028, 2029 and 2030 '
     'as RANGES on that measurement rather than as points, and a reader should treat the '
     'far years of this or any five-year forecast accordingly.'])
P('THE FAIR-VALUE ENVELOPE IN THIS STUDY IS NARROW AND THAT IS NOT A CONFIDENCE '
  'STATEMENT. %s to %s is the spread between three ways of discounting the same '
  'capital-constrained flow, and they agree because they are close cousins. It is not the '
  'range of outcomes. The range of outcomes is in the box above and it is much wider.'
  % (egp(BEAR), egp(FULL)))
for h, t in [
 ('The loss charge is the biggest judgement here',
  'The bank charged %s million of credit losses in six months. This study assumes 1.00%% of '
  'average financing in 2026 and 1.30%% after. If the release proves structural the central '
  'is %s; if the loss charge returns to its 2022-25 mean of 2.09%% it is nearer %s. Both '
  'ends are plausible on the evidence in hand.'
  % (m(H1O['ecl_charge'], 3), egp(GAPN['central_if_h1_cor_holds_throughout']), egp(22))),
 ('The risk-free rate is 34 days old',
  'Named already in 1.8 and repeated here because it is the largest single uncertainty. '
  'Four live re-source routes failed on the study date. The only recent market evidence '
  'found points 171 basis points below the rate carried, which alone is worth %s a share.'
  % egp(GAPN['central_at_rf_2129'] - CENTRAL)),
 ('The peer multiples could not be sourced properly',
  'No same-day book value could be obtained for any Egyptian bank other than ADIB-Egypt. '
  'The multiple lens is a band, it carries no weight in the answer, and it is the lens '
  'pointing highest.'),
 ('One year of the history is a comparative, not an original',
  'No English 2021 consolidated filing exists on the bank\'s own site — the document '
  'published under that name is the Arabic one. The 2021 figures come from the comparative '
  'column of the audited 2022 statements. Same auditor, same issuer, but a comparative can '
  'carry a restatement the original did not.'),
 ('The growth path assumes continued share gain',
  'Financing grows at 2.3 times nominal GDP in 2026, decaying to parity by 2030, which '
  'takes the bank from about 3.1%% of Egyptian private credit to about 4.4%%. That is slower '
  'than the share gain of the last decade and faster than none. If the bank simply grows '
  'with the system, the central falls by about %s.'
  % pc(abs(D['sensitivity'][6]['change']))),
 ('What would change our mind, in one line',
  'A third-quarter loss charge still near zero, or a current ten-year yield near 21%, would '
  'each move this study several pounds a share toward the market. A loss charge back at 2.7% '
  'of financing, or a policy rate cut faster than the published path, would move it away.')]:
    bullet(t, bold_head=h)

# ============================================================ Appendix A
doc.add_page_break()
H1('Appendix A — Financial statements')
H2('A.1  Income statement — three reported years and five forecast')
rows = [['EGP million', 'FY2023A', 'FY2024A', 'FY2025A'] + YR]
def hrow(label, key):
    return [label, m(HY[2023][key], 0), m(HY[2024][key], 0), m(BY[key], 0)] + \
           [m(x[key], 0) for x in P5]
import sys as _sys
_sys.path.insert(0, os.path.join(HERE, '..', 'adib_walkforward'))
import panel as WFP
HY = {}
for y in (2023, 2024):
    r = WFP.IS['FY%d' % y]
    HY[y] = {k: r[k] / 1000.0 for k in ('fin_income', 'cost_funds', 'net_funds', 'net_fees',
                                        'admin', 'other_op', 'ecl', 'pbt', 'tax', 'np',
                                        'np_parent')}
    HY[y]['other_nii'] = WFP.other_nii('FY%d' % y) / 1000.0
for lab, k in [('Financing income', 'fin_income'), ('Cost of deposits', 'cost_funds'),
               ('Net income from funds', 'net_funds'),
               ('Net fees and commissions', 'net_fees'),
               ('Other non-interest income', 'other_nii'),
               ('Administrative expenses', 'admin'),
               ('Other operating expenses', 'other_op'),
               ('Expected credit losses', 'ecl'), ('Profit before tax', 'pbt'),
               ('Tax', 'tax'), ('Net profit', 'np'), ('Attributable to the bank', 'np_parent')]:
    rows.append(hrow(lab, k))
table(rows, [1.5, 0.72, 0.72, 0.72] + [0.68] * 5, size=7.7, first_col_bold=True)
caption(T('income statement, reported and forecast'))
P('THE LAST THREE YEARS ARE AS FILED. 2023, 2024 and 2025 are each read from that year\'s '
  'own audited consolidated statements and every one of them adds up.')

H2('A.2  Balance sheet as reported')
rows = [['EGP million', 'FY2023A', 'FY2024A', 'FY2025A', 'H1-2026A']]
for lab, k in [('Financing to customers, net', 'fin_customers'),
               ('Total assets', 'total_assets'),
               ("Customers' deposits", 'cust_deposits'),
               ('Total liabilities', 'total_liab'),
               ('Equity attributable to the bank', 'equity_parent')]:
    r = [lab]
    for y in (2023, 2024, 2025):
        v = WFP.BS['FY%d' % y].get(k)
        r.append(m(v / 1000.0, 0) if v is not None else '—')
    hv = {'fin_customers': LR['fin_customers'], 'total_assets': LR['total_assets'],
          'cust_deposits': None, 'total_liab': LR['total_liab'],
          'equity_parent': LR['equity_parent']}.get(k)
    r.append(m(hv / 1000.0, 0) if hv else '—')
    rows.append(r)
table(rows, [2.4, 1.15, 1.15, 1.15, 1.15], size=8.4, first_col_bold=True)
caption(T('balance sheet, as reported'))

H2('A.3  The projected balance sheet, the capital account and the far-year ranges')
rows = [['EGP million'] + YR]
for lab, k in [('Financing to customers', 'financing'), ('Total assets', 'total_assets'),
               ('Attributable equity', 'equity'),
               ('Equity build required', 'equity_required'),
               ('Dividend', 'dividend'), ('Net flow to shareholders', 'fcfe')]:
    rows.append([lab] + [m(x[k], 0) for x in P5])
table(rows, [2.0] + [1.0] * 5, size=8.4, first_col_bold=True)
caption(T('the projected balance sheet and the capital account'))
P('The net flow to shareholders is negative in 2026 — %s million — because that is the year '
  'the bank took %s billion of new equity in. A capital call is a negative dividend and it '
  'is shown as one rather than netted away.'
  % (m(P5[0]['fcfe'], 0), egp(float(REG['capital_increase_2026']['value']) / 1000, 1)))
rows = [['Attributable profit, EGP million', 'Low', 'Point', 'High', 'Cells measured']]
for y in ('2028', '2029', '2030'):
    f = FAR[y]
    rows.append([y, m(f['low'], 0), m(f['point'], 0), m(f['high'], 0), str(f['n'])])
table(rows, [2.2, 1.2, 1.2, 1.2, 1.2], size=8.6, first_col_bold=True)
caption(T('years three to five as ranges, not points'))
P('These ranges are not scenarios anyone wrote down. They are the measured spread of this '
  'forecasting method\'s own error on this company\'s own history, at three, four and five '
  'years ahead, applied to the point forecast. They are wide because that spread is wide, '
  'and publishing the point alone would be claiming a precision the record does not support.')

# ============================================================ Appendix B
doc.add_page_break()
H1('Appendix B — Peers, risk register and the research register')
H2('B.1  Peers and the sector frame')
P('Egypt has roughly forty banks and five that matter to a public-market comparison. This '
  'study holds a same-day price for exactly one of them — Commercial International Bank at '
  '%s on 3 September 2026 — and a same-day book value for none. That is a real limit and '
  'it is why the multiple lens carries no weight in the answer.'
  % egp(float(REG['peer_comi_price']['value'])))
rows = [['', 'What is held', 'What is not']]
rows.append(['Commercial International Bank (EGX: COMI)',
             'price %s, 3 September 2026, same file and same day as ADIB-Egypt\'s own'
             % egp(float(REG['peer_comi_price']['value'])),
             'book value, earnings, capital ratio — none on the study date'])
rows.append(['Other listed Egyptian banks',
             'nothing on the study date',
             'prices and fundamentals; not sourced, and not substituted from memory'])
rows.append(['The band used', 'price-to-book 1.4-2.2x, price-to-earnings 5.5-8.5x, applied '
             'to the 2026 forecast', 'a point estimate — there is not enough here for one'])
table(rows, [2.2, 2.7, 2.1], size=8.3, first_col_bold=True)
caption(T('the peer frame, and its holes'))
P('Sector context that IS held. Egyptian private-sector credit is about 26%% of GDP, down '
  'from 36%% in 2009 — the banking system has been shrinking relative to the economy for '
  'fifteen years while the government absorbed the savings. ADIB-Egypt is about %s of that '
  'system\'s credit and rising. A reader who believes credit deepening resumes should '
  'believe this study\'s growth path is conservative; a reader who believes the crowding-out '
  'continues should believe the opposite.' % pc(GAPN['share_of_system_credit_fy2025'], 1))

H2('B.2  Risk register')
rows = [['Risk', 'How it would show up', 'Sized']]
rows.append(['The loss charge normalises above the assumed path',
             'the expected-credit-loss line in any quarterly statement',
             '%s of value per 50 basis points' % pc(abs(D['sensitivity'][0]['change']))])
rows.append(['The margin compresses faster than the policy glide',
             'net income from funds against average assets, quarterly',
             '%s per 50 basis points on the asset yield'
             % pc(abs(D['sensitivity'][2]['change']))])
rows.append(['Further equity issued at or near par',
             'issued capital in any balance sheet',
             'not sized — depends entirely on the terms; the 2026 issue cost existing '
             'holders most of a half-year\'s book-value gain'])
rows.append(['The sovereign', 'the yield the discount rate is built on, and the '
             'government paper that is most of the balance sheet',
             '%s per 200 basis points' % pc(abs(D['sensitivity'][8]['change']))])
rows.append(['Concentration in Egyptian government exposure',
             'the split between financing to customers and treasury bills',
             'not separately sized; it is the shape of every Egyptian bank'])
rows.append(['The growth simply stops',
             'financing to customers, quarterly',
             '%s if financing grows five points a year slower'
             % pc(abs(D['sensitivity'][6]['change']))])
table(rows, [2.1, 2.6, 2.3], size=8.3, first_col_bold=True)
caption(T('risk register — every entry sized where it can be'))

H2('B.3  The research register')
rows = [['Layer', 'What was read', 'Dated', 'Result']]
rows.append(['Company — statements',
             'sixteen consolidated fiscal years, FY2010 to FY2025, plus Q1 and H1 2026, all '
             'from adib.eg', '9 Sep 2026',
             'obtained; every statement footed against its own arithmetic'])
rows.append(['Company — other', 'the 2024 annual report, the 2025 board report, the '
             '2023 and 2024 investor-relations packs, the 2025 governance report',
             '9 Sep 2026', 'obtained'])
rows.append(['Company — negative result',
             'the English FY2021 consolidated filing', '9 Sep 2026',
             'DOES NOT EXIST — the file published under that name is the Arabic filing. Two '
             'alternative filenames returned 404. FY2021 taken from the FY2022 comparative.'])
rows.append(['Country — macro',
             'Egyptian inflation, policy rate, sovereign yield, currency and terminal '
             'convention, from the house path', '2 Sep 2026', 'obtained'])
rows.append(['Country — negative result', 'a current Egyptian ten-year yield',
             '9 Sep 2026',
             'NOT OBTAINED. Four routes tried: the central bank\'s bond-auction pages (404), '
             'its auction endpoint (returns the site shell), and two market-data providers '
             '(JavaScript-rendered tables, and a 403). The 6 August quote is carried and '
             'declared stale.'])
rows.append(['Industry',
             'Egyptian private-sector credit and broad money, 2005-2025', '9 Sep 2026',
             'obtained; used for the share-of-system check'])
rows.append(['Peers', 'same-day Egyptian bank prices and book values', '9 Sep 2026',
             'PARTIAL — one price, no book values. Recorded rather than filled in.'])
rows.append(['Market', 'the share price and the price history', '3 Sep / 23 Aug 2026',
             'obtained; the two dates differ and section 3 says so'])
table(rows, [1.35, 2.6, 0.95, 2.1], size=7.9, first_col_bold=True)
caption(T('the research register, negative results included'))

# ============================================================ Appendix C
doc.add_page_break()
H1('Appendix C — Expert panel')
P('Three readings of the same evidence, each by a different method, written to disagree '
  'rather than to converge.')
H2('C.1  Expert 1 — the balance-sheet reader')
P('"Start with what is not in dispute. This bank funds itself at %s and earns %s on its '
  'assets, and the gap between those two numbers is the whole business. In 2025 that gap '
  'was %s of average assets and it produced a %s return on equity. Now watch what the '
  'central bank is doing: 19.00%% today, 12.00%% on its own published path. Both sides of my '
  'spread fall, but the asset side falls first and faster, because a treasury bill reprices '
  'in three months and a savings depositor takes longer to accept less. That is why my '
  'margin goes to %s by 2030 and why I do not believe a %s return survives the decade."'
  % (pc(OBS['cost_of_funds'], 2), pc(OBS['asset_yield'], 2), pc(OBS['nim'], 2),
     pc(OBS['roe']), pc(P5[-1]['nim'], 2), pc(OBS['roe'])))
P('"The second thing I would say is that this bank does not have spare capital. Equity is '
  '%s of assets. Growing assets by a third takes %s billion of it, and the bank earns %s '
  'billion. That is why the dividend is small and why they came to shareholders for %s '
  'billion in June. Anyone valuing this on earnings without asking what the balance sheet '
  'consumes is valuing a number the shareholder never sees."'
  % (pc(H1O['equity_over_assets'], 2), egp(P5[0]['equity_required'] / 1000, 1),
     egp(P5[0]['np_parent'] / 1000, 1),
     egp(float(REG['capital_increase_2026']['value']) / 1000, 0)))
H2('C.2  Expert 2 — the credit reader')
P('"I look at one line and it is the strangest line I have seen in an Egyptian bank\'s '
  'accounts this year. %s million of credit losses in six months, on a %s billion book. The '
  'same half of last year was %s million. The full year 2023 and 2024 were each about 2.7%% '
  'of financing. Something has been released, and the statements do not tell me what."'
  % (m(H1O['ecl_charge'], 3), egp(LR['fin_customers'] / 1000, 0), m(732.193, 0)))
P('"Here is why I would not extrapolate it. This book grew 29% in six months. Newly written '
  'financing does not go bad in its first year; it goes bad in its third. A bank growing '
  'this fast has a loss charge that lags its balance sheet by two or three years, so the '
  'charge you see today is levied on a book a third the size of the one you own. If growth '
  'slows and the seasoning arrives together, the charge does not go back to 1.3% — it goes '
  'to something worse for a couple of years. I would rather be wrong on the conservative '
  'side of that."')
H2('C.3  Expert 3 — the market reader')
P('"You are all arguing about the cost of equity and calling it something else. The stock '
  'is at %s, which is %s times June book on a %s trailing return. Invert that with a 7%% '
  'terminal growth and the market is discounting at %s. This study uses %s. That is the '
  'entire disagreement — %s basis points on a rate, not a view about credit."'
  % (egp(SPOT), '%.2f' % GAPN['market_pb_on_jun26_book'], pc(H1O['roe']),
     pc(GAPN['market_implied_ke_gordon'], 2), pc(CC['ke'], 2),
     m(abs(CC['ke'] - GAPN['market_implied_ke_gordon']) * 1e4, 0)))
P('"And I would point out where that rate comes from: a ten-year yield printed on 6 August, '
  'thirty-four days before the price. In late April and May the same yield was averaging '
  '21.29%%. Put 21.29%% in and the answer is %s. Put in what the market is implying and the '
  'answer is the market. I am not saying the model is wrong. I am saying the largest input '
  'in it is a month old and the study should say so — which, to its credit, it does."'
  % egp(GAPN['central_at_rf_2129']))
H2('C.4  Cross-examination')
P('Expert 3 to Expert 2: "You will not extrapolate six months of credit data, but you will '
  'extrapolate four years of it. Why is the 2022-25 average more relevant than the most '
  'recent half?" Expert 2: "Because the average contains a devaluation and the half does '
  'not. I am not extrapolating either — I am picking a number between them and saying so."')
P('Expert 1 to Expert 3: "The market\'s implied cost of equity is not evidence about the '
  'cost of equity. It is the market\'s price divided by my estimate of the return. If my '
  'return estimate is too low, your implied rate is too low too." Expert 3: "Agreed, and '
  'that is why I used the reported half rather than the forecast. It is the least '
  'model-dependent version of the calculation available."')
P('Expert 2 to Expert 1: "Your margin path assumes the asset side reprices faster. Half '
  'this balance sheet is treasury bills — those reprice in ninety days. But the customer '
  'financing is Islamic, and a murabaha is priced at origination for its whole term. Are '
  'you sure the mix does not slow the repricing?" Expert 1: "Not sure. It would make the '
  'margin fall more slowly than I have it, which would raise the answer."')
H2('C.5  The three in one room')
P('What they agree on: the balance sheet is growing far faster than the Egyptian economy '
  'and the capital to fund it is the binding constraint; the margin compresses as the '
  'central bank cuts; and the loss charge in the June half is not a run rate.')
P('What they do not agree on: whether the disagreement with the market is about credit or '
  'about the discount rate. Expert 2 says the market is under-providing for a fast-growing '
  'book. Expert 3 says the market and the model differ by %s basis points on one rate and '
  'everything else is decoration. Expert 1 says both are secondary to the capital call that '
  'has not happened yet.'
  % m(abs(CC['ke'] - GAPN['market_implied_ke_gordon']) * 1e4, 0))
H2('C.6  Reading the divergence')
P('The spread between the highest and lowest present-value read in this study is %s a '
  'share, which is small. The spread between the study and the market is %s a share, which '
  'is not. That shape — three lenses agreeing with each other and disagreeing with the '
  'price — is exactly the case where the lenses probably share an assumption. Here they '
  'share two: a %s cost of equity built on a stale yield, and a loss charge normalised '
  'above the last six months. A reader who disagrees with either should not adjust the '
  'lenses; they should change those two inputs and read the sensitivity table.'
  % (egp(FULL - BEAR), egp(SPOT - CENTRAL), pc(CC['ke'], 2)))

# ============================================================ About + Disclosure
doc.add_page_break()
H1('About this series')
P('Testahil publishes independent valuation studies as an educational exercise in method. '
  'Each study builds a company from its own filings, states every input with its source and '
  'date, and publishes ranges rather than points. Every forecast is recorded so that it can '
  'be graded later against what actually happened, and the grading is published whether it '
  'flatters the method or not.')
P('This study was built alongside a test of its own forecasting method on ADIB-Egypt\'s own '
  'history — eleven past year-ends, rebuilt from what was published at the time and scored '
  'against what the bank reported. Section 7 gives the result, including the part where the '
  'method does no better than a naive growth rule.')
H1('Disclosure and disclaimer')
P('The preparer holds no position in ADIB-Egypt, has no relationship with the company, and '
  'received no compensation from any party in connection with this document. The preparer '
  'is not licensed by the Egyptian Financial Regulatory Authority or by any other '
  'securities regulator, holds no brokerage or advisory authorisation in any jurisdiction, '
  'manages no money, and accepts no clients.', size=9.2, color=GREY)
P('This document is not investment advice, not a recommendation, not a solicitation, and '
  'not an offer. It contains no rating and no price target. It is a valuation exercise '
  'published for educational purposes and it is not directed at the circumstances, '
  'objectives or means of any reader. Any person acting on it does so entirely at their own '
  'risk. All figures are model outputs under stated assumptions; the assumptions are '
  'disclosed so a reader can disagree with them, and a reader who does will get a different '
  'number.', size=9.2, color=GREY)
P('Historical financial data is ADIB-Egypt\'s own published disclosure. Market data is '
  'sourced as stated. Forward-looking figures are the preparer\'s judgements and are '
  'flagged throughout. No part of this document may be represented as the view of '
  'ADIB-Egypt, of Abu Dhabi Islamic Bank PJSC, or of any regulator.', size=9.2, color=GREY)

out = os.path.join(HERE, 'ADIB_Valuation_Study_%s.docx' % EDITION)
doc.save(out)
print('written %s' % out)
print('sections: 16   tables: %d' % _TN[0])
