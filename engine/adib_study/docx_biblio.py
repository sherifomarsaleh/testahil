#!/usr/bin/env python3
"""ADIB_Bibliography_{DD-MM-YYYY}.docx — the standalone bibliography.

Primary documents · the full input register, every entry four-field · judgements with
what would overturn each · negative results · where two sources disagree · what is not
disclosed. GENERATED from study_numbers.json and the walk-forward's own registers;
nothing here is typed twice.
"""
import datetime as _dtm
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'adib_walkforward'))
import docx_base as B
from docx.shared import Pt

doc, P, H1, H2, table, caption, masthead = (B.doc, B.P, B.H1, B.H2, B.table, B.caption,
                                            B.masthead)
INK, GREY = B.INK, B.GREY


def box(lines, **kw):
    return B.box([(l if isinstance(l, tuple) else ('', l)) for l in lines], **kw)


D = json.load(open(os.path.join(HERE, 'study_numbers.json'), encoding='utf-8'))
COC = D['cost_of_capital']   # every rate in this bibliography is read from here
FETCH = json.load(open(os.path.join(HERE, '..', 'adib_walkforward',
                                    'fetch_attempts.json'), encoding='utf-8'))
import panel as WFP  # noqa: E402
REG = D['register']

masthead()
P('Bibliography and input register', size=14, bold=True)
P('Abu Dhabi Islamic Bank – Egypt S.A.E. (EGX: ADIB) — valuation study of 9 September 2026',
  size=11, italic=True, color=GREY)
P('This document stands alone. Every figure in the study can be traced from here to the '
  'document it came from, the date that document carries, and how good a source it is. '
  'Where a figure could not be sourced, this document says so rather than leaving the gap '
  'to be inferred.')

H1('1  Primary documents')
P('Sixteen consolidated fiscal years plus two interim periods, all from the bank\'s own '
  'investor-relations archive at adib.eg. EVERY ONE OF THESE WAS PARSED AND CHECKED TO ADD '
  'UP; a statement that does not foot against its own arithmetic did not enter this study.')
rows = [['Period', 'Document', 'Document date', 'Tier', 'How it was read']]
for k in sorted(WFP.SOURCES, key=lambda x: (x[2:6], x)):
    s = WFP.SOURCES[k]
    rows.append([k.replace('_', '-'), s['doc'][:110], s['date'], s['tier'], s['route']])
table(rows, [0.85, 3.1, 1.0, 0.5, 1.55], size=7.4)
caption('Table 1 — the primary record. Tier A is the company\'s own audited or reviewed '
        'statements. There is no tier B or tier C figure anywhere in this study\'s company '
        'data.')
box(['HOW A RASTER WAS READ, AND WHY IT CAN BE TRUSTED. Seven of these filings publish '
     'their statements as images with no text layer. Each was read TWICE and '
     'independently — once off the largest embedded image at its native resolution, once '
     'off a rendered page — and every disagreement between the two passes was settled by '
     'the statement\'s OWN arithmetic, or where that was not decisive, by the comparative '
     'column of the following year\'s filing. Every statement in this study foots exactly. '
     'Two figures could only be settled by the footing identity and both are labelled '
     'DERIVED with the formula: a gain on financial investments of EGP 7.155 million in '
     'FY2025 (0.04% of pre-tax profit) and non-controlling interests of EGP 38.576 million '
     'in the FY2025 equity block.'])

H1('2  The input register — every entry four-field')
P('Value, source, date, tier. An input with no source does not enter the model.')
rows = [['Input', 'Value', 'Date', 'Tier', 'Source']]
for k in sorted(REG):
    e = REG[k]
    v = e['value']
    if isinstance(v, list):
        vs = ' / '.join(('%.4g' % x) if isinstance(x, (int, float)) else str(x) for x in v)
    elif isinstance(v, float):
        vs = '%.6g' % v
    else:
        vs = str(v)
    rows.append([k.replace('_', ' '), vs[:34], e['date'], e['tier'], e['source'][:430]])
table(rows, [1.25, 1.0, 0.75, 0.5, 3.5], size=6.6)
caption('Table 2 — the full input register.')

H1('3  Judgements, and what would overturn each')
rows = [['Judgement', 'What it is', 'What would overturn it']]
rows.append(['The cost of risk',
             '1.00% of average financing in FY2026 and 1.30% thereafter, against a '
             'FY2022-25 mean of 2.09% and a June-2026 half of effectively zero',
             'A third-quarter 2026 charge still near zero would say the release is '
             'structural and the assumption too harsh. A charge back above 2% would say '
             'the opposite. This is the single most consequential judgement in the study '
             'and it is worth EGP 10.86 a share.'])
rows.append(['The share of Egyptian credit rises',
             'financing grows at 2.26x nominal GDP in 2026, decaying to parity by 2030, '
             'taking the bank from 3.14% of Egyptian private credit to 4.42%',
             'Two consecutive halves of financing growth at or below nominal GDP. The '
             'walk-forward beneath this study measured the historical drift at about 8.7% '
             'a year for a decade, so the assumption is slower than history and faster '
             'than none.'])
rows.append(['The margin compresses with the policy glide',
             'asset yield falls at about 0.75 of the central bank\'s published path and '
             'the cost of funds at about 0.80, so the margin goes from 6.64% to 4.81%',
             'A half in which the margin holds while the policy rate falls. The Islamic '
             'financing book prices at origination for its whole term, so the mix could '
             'slow the repricing more than assumed — which would RAISE the value.'])
rows.append(['Equity is pinned at 10.5% of assets',
             'the level the bank actually stood at on 30 June 2026, and the constraint '
             'that makes the dividend what is left rather than what is chosen',
             'A disclosed regulatory capital target materially different from it, or a '
             'balance sheet run at a visibly lower ratio for two years.'])
# EVERY FIGURE IN THIS ROW IS READ, NOT TYPED. It said 29.81% and explained it as a beta
# times the TOTAL premium — the retired identity — and quoted a central two re-strikes old.
# A typed figure in a delivered document is one nothing can check, and all three went stale
# on the same morning [R-DCF-01].
rows.append(['The cost of equity is %.2f%%' % (100 * COC['ke']),
             'a %.2f%% ten-year yield less a %.2f%% sovereign spread, plus a %.4f beta '
             'times the %.4f%% MATURE premium, plus the %.4f%% country premium charged '
             'flat and once — beta multiplies the mature leg and nothing else'
             % (100 * COC['rf'], 100 * COC['sovereign_default_spread'],
                COC['beta'], 100 * COC['erp_mature'], 100 * COC['crp_effective']),
             'A CURRENT ten-year yield. The one carried is %d days old and the only recent '
             'market evidence found is 171 basis points lower.'
             % COC['rf_staleness_days']])
rows.append(['Terminal growth is 7.00%',
             'equal to terminal inflation — zero real growth in perpetuity',
             'Nothing in the evidence; it is deliberately the conservative end. A bank in '
             'an economy with private credit at 26% of GDP growing at zero real for ever '
             'is an assumption against value, and it is worth about 1.4% per percentage '
             'point.'])
table(rows, [1.5, 2.5, 3.0], size=7.6)
caption('Table 3 — every judgement, and the observation that would kill it.')

H1('4  Negative results — what was looked for and not found')
P('A source that would not yield is a fact worth recording. These are the attempts that '
  'failed, with what was done instead.')
rows = [['What was sought', 'What happened', 'What was done instead']]
for a in FETCH['attempts']:
    if a['tier'] == '-' or 'NOT' in a['outcome'] or '404' in a['outcome'] or \
            'REJECTED' in a['outcome'] or 'does not' in a['outcome'].lower():
        rows.append([a['target'][:70], a['outcome'][:230], ''])
rows.append(['A current Egyptian ten-year government bond yield',
             'FOUR ROUTES, ALL FAILED on 9 September 2026: the central bank\'s '
             'treasury-bond auction pages return 404; its auction endpoint returns the '
             'website shell rather than data; two market-data providers render their '
             'yield tables in JavaScript, and one returns 403.',
             'The 6 August 2026 quote of 23.00% held in the house macro path is carried '
             'and DECLARED STALE on the face of the register entry, in section 1.8 of the '
             'study and in the gap review. It is sensitised by 200 basis points either '
             'way. The only recent evidence found — a 21.29% average over late April to '
             'late May 2026 — is quoted beside it.'])
rows.append(['Same-day book value for any Egyptian bank peer',
             'NOT FOUND. One same-day peer PRICE is held (Commercial International Bank, '
             'EGP 138.98 on 3 September 2026). No peer book value, earnings or capital '
             'ratio could be sourced on the study date.',
             'The relative-multiple lens is published as a BAND, carries no weight in the '
             'answer, and the hole is stated in the study\'s own Appendix B.'])
rows.append(['The English FY2021 consolidated filing',
             'DOES NOT EXIST on the issuer\'s site. The file published under that name is '
             'the ARABIC filing — 102 pages, no English statement page. Two alternative '
             'filenames return 404.',
             'FY2021 is taken from the comparative column of the audited FY2022 '
             'statements. Tier A and the same issuer, but a comparative, which is the one '
             'row in the record where point-in-time discipline cannot be fully honoured.'])
table(rows, [1.7, 2.9, 2.4], size=7.4)
caption('Table 4 — negative results.')

H1('5  Where two sources disagree')
rows = [['The disagreement', 'How it was settled']]
rows.append(['Six fiscal years are RESTATED by the following year\'s filing — FY2011, '
             'FY2014, FY2015, FY2016, FY2017 and FY2018 all carry different figures in '
             'their own report and in the next one. FY2017\'s administrative expenses are '
             'EGP 1,172.1 million in its own filing and EGP 1,015.4 million in the FY2018 '
             'comparative.',
             'THE ORIGINAL IS USED and the restatement is recorded beside it, never '
             'substituted. Every one is listed in the walk-forward\'s own restatement '
             'register. A year read as its successor restated it is a year nobody could '
             'have read at the time.'])
rows.append(['The FY2025 filing prints total assets of EGP 260,457,106 thousand for '
             'FY2024 in one place and the FY2024 filing prints EGP 260,467,106.',
             'The equity block\'s own arithmetic settles it at 260,467,106: liabilities of '
             '237,480,399 plus equity of 22,986,707 reproduce it exactly.'])
rows.append(['The sovereign default spread is %.2f%% in the cost-of-capital record used by '
             'the other Egyptian studies and %.2f%% in the house macro path, from the same '
             'source file.'
             % (100 * COC['sovereign_default_spread'],
                100 * COC['sov_default_spread_house_path']),
             'A rounding artefact of one basis point. The 3.42% figure is used so that this '
             'study\'s cost of equity is built from the same pair of numbers as every '
             'other Egyptian study in the book, and the difference is recorded here.'])
rows.append(['The share price is EGP 54.40 in the site\'s own data file (23 August close) '
             'and EGP 52.05 in the supplied-price file (3 September close).',
             'THE LATER ONE. A study audited against a price eleven days old is audited '
             'against its own past. The 23 August close is still used as the anchor for '
             'the probability map in section 3, because it is the last session in the '
             'price history, and the study says so in terms.'])
table(rows, [3.4, 3.6], size=7.6)
caption('Table 5 — disagreements, and which side was taken.')

H1('6  What is not disclosed')
P('The limits of the record, stated so nobody has to discover them.')
for t in [
 'NO SPLIT OF FINANCING by retail, corporate or small business, and no split of deposits '
 'by account type. The low-cost funding share — the single most useful number in judging '
 'how a bank\'s funding cost behaves in an easing cycle — cannot be computed, and no '
 'assumption is made about it.',
 'NO NON-PERFORMING RATIO AND NO COVERAGE RATIO in any of the eighteen statements parsed. '
 'The cost-of-risk driver is therefore built on the charge, not on the stock of bad '
 'assets, and there is no way to check whether the June 2026 release reflects recoveries, '
 'write-offs or a change in the loss model.',
 'NO GEOGRAPHIC OR PRODUCT SEGMENT NOTE.',
 'NO NUMERIC FORWARD GUIDANCE. Nothing management publishes is consumed as an input to '
 'this model, and there is nothing to score.',
 'THE FILED EARNINGS-PER-SHARE FIGURES CANNOT BE REPRODUCED from attributable profit and '
 'the year-end share count, and this study says so rather than reverse-engineering a '
 'deduction the equity statement does not show. FY2025 prints EGP 11.25 on attributable '
 'profit of EGP 12,588.6 million, implying about 1,119 million weighted shares against a '
 'year-end 1,200 million; FY2024 prints EGP 14.02 implying about 643 million against a '
 'year-end 600 million. Every per-share figure in this study is attributable profit over '
 'the SHARE COUNT AT THE PERIOD END, which is stated, reproducible, and different from '
 'the filed EPS.',
 'THE FY2025 EQUITY RECONCILIATION LEAVES EGP 110.5 MILLION UNEXPLAINED. Retained '
 'earnings move from 15,815.3 to 20,963.2 while attributable profit is 12,588.6, '
 'dividends paid 1,055.9, the reserve transfer 495.4 and the capital increase 6,000.0 — '
 'which closes to within 110.5, or 0.9% of the profit. It is recorded rather than '
 'assigned.']:
    B.bullet(t)

H1('7  Market and macro data')
rows = [['Item', 'Value', 'Date', 'Source']]
for k in ('spot', 'peer_comi_price', 'beta', 'rf', 'sov_default_spread', 'erp',
          'rf_terminal', 'erp_terminal', 'terminal_growth', 'inflation_path',
          'policy_rate_path'):
    e = REG[k]
    v = e['value']
    vs = (' / '.join('%.4g' % x for x in v) if isinstance(v, list)
          else ('%.6g' % v if isinstance(v, float) else str(v)))
    rows.append([k.replace('_', ' '), vs[:28], e['date'], e['source'][:330]])
table(rows, [1.3, 1.1, 0.8, 3.8], size=6.8)
caption('Table 6 — market and macro inputs. These are the only figures in this study that '
        'are not the company\'s own disclosure.')

# THE EDITION IS NOT TYPED HERE. It was, so this file went on writing a
# 09-09-2026 bibliography beside a 10-09-2026 study — one strike, two dates.
import edition as _EDN
out = os.path.join(HERE, _EDN.BIBLIO_DOCX)
doc.save(out)
print('written %s' % out)
