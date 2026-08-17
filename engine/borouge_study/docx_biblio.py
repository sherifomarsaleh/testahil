"""BOROUGE_Bibliography_09-08-2026.docx — the standalone source and input register.

Four tables, and they are the point of the document rather than an appendix to it:
  1. the primary documents, each with the address it was read from and what it was read
     for, plus the verification that the copy used is the copy the company publishes;
  2. the FULL input register — every input in the model with its value, its date, its
     source and how it was constructed, grouped by research layer;
  3. the judgements, each with what would overturn it;
  4. the negative results — what was searched for and NOT found, and what the study did
     instead.
Plus a short note on where an aggregator was used and where it was not.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)

import docx_base as B                                        # noqa: E402
from docx_base import (H1, H2, P, box, caption, doc, masthead,  # noqa: E402
                       rich, table)
from docx_base import GREY                                    # noqa: E402

D = json.load(open('study_numbers.json'))
SRC = json.load(open('source_access.json'))
SW = json.load(open('sweep_register.json'))
BETA = json.load(open('beta_result.json'))
BT = json.load(open('backtest_5y.json'))

W = D['wacc']
CIN = D['company_inputs']
MIN_ = D['macro']
FN = D['framings']['normalisation']
ALT = D['alt_wacc']['bottom_up_sector_beta']
LEN_ = D['lenses']


def fmt(v):
    if isinstance(v, bool):
        return 'yes' if v else 'no'
    if isinstance(v, float):
        if v == 0:
            return '0'
        if abs(v) < 1:
            return f'{v:,.4f}'
        if abs(v) >= 1e6:
            return f'{v:,.0f}'
        return f'{v:,.3f}'.rstrip('0').rstrip('.')
    if isinstance(v, int):
        return f'{v:,}'
    if isinstance(v, dict):
        return '(table — see the study)'
    return str(v)


masthead()
P('Borouge plc', size=25, bold=True, space_after=0)
P('Bibliography, input register and judgement record', size=13, color=GREY,
  space_after=2)
P('Companion to the Borouge plc valuation study dated 9 August 2026', size=10.5,
  color=GREY, space_after=12)

box([
    ('What this document is for. ',
     'A valuation is only as good as what it is built from. This document lists every '
     'source the study used, every input it carries, every judgement it made and every '
     'search that came back empty — so that a reader can check the study rather than '
     'take it on trust.'),
    ('The rule the study works to. ',
     'Any figure Borouge itself reports comes ONLY from a document Borouge itself '
     'published. Data vendors, broker notes and press coverage appear in this study in '
     'exactly one place — as a cross-check on peer valuations — and they are labelled as '
     'such wherever they appear. If an official document could not be obtained, the '
     'study would stop and say so rather than substitute a weaker source.'),
])

# ============================================================ 1 PRIMARY DOCUMENTS
H1('1  Primary documents')
P(f'All {SRC["total"]} documents below were downloaded from Borouge plc’s own '
  f'investor-relations library. On 9 August 2026 every one of them was downloaded again '
  f'and compared byte-for-byte against the copy this study was built from: '
  f'{SRC["identical"]} of {SRC["total"]} matched exactly. That check is what allows the '
  f'study to state that no figure has passed through an intermediary.')
rows = [['Document', 'What the study reads off it', 'Verified']]
ORDER = ['FS_FY2025.pdf', 'FS_FY2024.pdf', 'FS_FY2023.pdf', 'FS_FY2022.pdf',
         'FS_Q1_2026.pdf', 'FS_Q2_2026.pdf', 'MDA_FY2025.pdf', 'MDA_FY2024.pdf',
         'MDA_FY2023.pdf', 'MDA_Q1_2026.pdf', 'MDA_Q2_2026.pdf', 'PRES_FY2025.pdf',
         'PRES_FY2024.pdf', 'PRES_FY2023.pdf', 'PRES_Q2_2026.pdf', 'REL_FY2025.pdf',
         'REL_Q2_2026.pdf', 'AR2025.pdf', 'AR2024.pdf', 'AR2023.pdf', 'AR2022.pdf']
BY_FILE = {d['file']: d for d in SRC['documents']}
for f in ORDER:
    d = BY_FILE[f]
    rows.append([d['reads'], d['url'].replace('https://www.borouge.com', '')
                 .replace('%20', ' '),
                 'identical' if d['refetch'] == 'IDENTICAL' else d['refetch']])
table(rows, [2.05, 3.90, 0.85], size=7.6)
caption('Table 1 — The primary documents. Paths are relative to www.borouge.com. The '
        'index they were all taken from is at '
        '/en/investor-relations/Pages/reports-results.aspx.')

P('Four complete audited financial years were obtained — 2022, 2023, 2024 and 2025 — each '
  'a full statutory set with an auditor’s report, a statement of financial position, a '
  'statement of profit or loss, a statement of changes in equity, a statement of cash '
  'flows and notes. The study carries 2023, 2024 and 2025 as model columns and holds 2022 '
  'as a check: 2022 was the post-listing peak-price year, and including it would flatter '
  'every through-cycle average the study takes. That exclusion is a stated judgement, not '
  'a gap in the record.')
P('Both quarters of the study year already disclosed — the first quarter and the first '
  'half of 2026 — were read before the forecast was built, not after. They are where the '
  'feedstock step-up and the freight increase come from.')

rows = [['Also used, and what for', 'Role']]
for src_, role in [
    ('Abu Dhabi Securities Exchange monthly market-statistics workbooks, December 2025, '
     'March 2026 and June 2026',
     'Cross-check on traded shares and market capitalisation only. Never a source for a '
     'reported figure'),
    (f'Daily price history for Borouge from listing on 3 June 2022 to 7 August 2026, '
     f'{json.load(open("technicals.json"))["sessions"]:,} sessions',
     'The technical section, the probability bands, and the measured beta'),
]:
    rows.append([src_, role])
table(rows, [3.40, 3.40], size=8.4)

# ============================================================ 2 INPUT REGISTER
doc.add_page_break()
H1('2  The full input register')
P('Every input the model carries, with its value, the date it refers to, and the source '
  'and construction behind it. Nothing in the model is outside this register.')

H2('2.1  Company inputs — read off Borouge’s own documents')
P(f'{len(CIN)} inputs. Every one of them comes from an audited or reviewed financial '
  f'statement, a management discussion and analysis, an earnings presentation or an '
  f'earnings release published by Borouge plc.')
rows = [['Input', 'Value', 'As at', 'Source and construction']]
for k in sorted(CIN):
    v = CIN[k]
    rows.append([k.replace('_', ' '), fmt(v['value']), v['date'], v['source']])
table(rows, [1.30, 0.85, 0.70, 3.95], size=6.4)
caption('Table 2 — The company input register. Values in USD thousand unless the source '
        'text says otherwise.')

H2('2.2  Market, country and industry inputs')
P(f'{len(MIN_)} inputs. These set the cost of capital, the macro backdrop and the '
  f'forecast price direction. None of them is a source for a figure Borouge reports.')
rows = [['Input', 'Value', 'As at', 'Source and construction']]
for k in sorted(MIN_):
    v = MIN_[k]
    rows.append([k.replace('_', ' '), fmt(v['value']), v['date'], v['source']])
table(rows, [1.30, 0.85, 0.70, 3.95], size=6.4)
caption('Table 3 — The market, country and industry input register.')

H2('2.3  Forecast drivers')
P('The drivers below are the study’s own forward assumptions. Each is anchored on '
  'something disclosed, and the anchor is named.')
rows = [['Driver', 'Path 2026–2030', 'Construction', 'Anchor']]
FD = D['framing_drivers']
LABELS = {
    'util_pe': ('Polyethylene utilisation',
                'The rates the plant demonstrated in 2024 and 2025'),
    'util_pp': ('Polypropylene utilisation',
                'The rates the plant demonstrated in 2024 and 2025'),
    'bench_pe': ('Polyethylene benchmark, USD/t',
                 f'Published capacity growth of '
                 f'{MIN_["pe_capacity_growth"]["value"] * 100:.0f}% to 2034 against '
                 f'demand growing with world output'),
    'bench_pp': ('Polypropylene benchmark, USD/t',
                 f'Published capacity growth of '
                 f'{MIN_["pp_capacity_growth"]["value"] * 100:.0f}% to 2034'),
    'prem_pe': ('Polyethylene premium, USD/t',
                'The company’s own through-the-cycle premium guidance'),
    'prem_pp': ('Polypropylene premium, USD/t',
                'The company’s own through-the-cycle premium guidance'),
    'sd_per_t': ('Selling and distribution, USD/t sold',
                 'H1-2026 actual on the re-routed lane, against the audited three-year '
                 'level on the direct route'),
    'feed_market_share': ('Share of feedstock bought at market price',
                          'H1-2026 disclosure that propylene was bought at market prices '
                          'while the conversion unit was idled'),
}
for key, (lab, anchor) in LABELS.items():
    for fk, fname in [('normalisation', 'Shipping normalises'),
                      ('prolonged', 'Disruption persists')]:
        vals = FD[fk][key]
        rows.append([lab if fk == 'normalisation' else '',
                     ' · '.join(fmt(x) for x in vals), fname,
                     anchor if fk == 'normalisation' else ''])
table(rows, [1.55, 1.95, 1.25, 2.05], size=7.2)
caption('Table 4 — The forecast drivers, both constructions. The two differ only in '
        'utilisation, benchmark prices, premia, freight and the feedstock mix — that is, '
        'only in how long the shipping lane stays impaired.')

# ============================================================ 3 JUDGEMENTS
doc.add_page_break()
H1('3  Judgements, and what would overturn each one')
P('These are the places where the study chose. Each is stated with the reasoning and with '
  'the specific observation that would prove it wrong.')
rows = [['Judgement', 'What the study did', 'What would overturn it']]
for j, did, over in [
    ('Which beta to use',
     f'Neither. Both are published: the share’s own five-year weekly regression against '
     f'the {BETA["regressor"]}, giving {BETA["beta"]:.3f}, and a sector bottom-up beta '
     f're-levered to {W["beta_bottom_up"]:.3f}. The two are carried side by side to a '
     f'value per share everywhere they appear',
     'A longer trading history or a wider free float that let the share’s own regression '
     'pass a strong-instrument test rather than a minimum one. A rising R-squared would '
     'settle it empirically'),
    ('Which index to regress against',
     f'The {BETA["regressor"]}, the company’s own local market index. An earlier revision '
     f'of this study used an equal-weight basket of the other listed UAE names, adopted '
     f'only because no index series was available; that basket gives '
     f'{BETA["composite_corroboration"]["beta"]:.3f} against the index’s '
     f'{BETA["beta"]:.3f}. An equal-weight basket over-weights small, thinly traded '
     f'constituents and understates covariance with a large name, so the '
     f'capitalisation-weighted index is the correct measure and the basket is retained '
     f'as a cross-check',
     'A free-float-weighted index series that excluded the subject, which would remove '
     'even the sub-one-per-cent self-covariance the current regressor carries'),
    ('Whether thin trading explains the low beta',
     'No. A lead-lag correction for infrequent trading was run and moves the estimate '
     f'DOWN to {BETA["dimson"]["sum_beta"]:.3f}, not up. So the low reading is not a '
     f'stale-price artefact',
     'A different correction method giving a materially higher estimate'),
    ('Whether the 2026 cost step is permanent',
     'Not decided. Two full constructions are built and published side by side, '
     'differing only in how long the shipping lane stays impaired',
     'Full-year 2026 results. Feedstock back toward the low 300s per tonne confirms the '
     f'temporary reading; a figure still near '
     f'${D["unit_build"]["feed_per_t_h126"]:,.0f} confirms the other'),
    ('Whether to carry the H1-2026 realisation residual',
     'No. The forecast carries the audited three-year mean rather than the wider '
     'half-year figure, on the ground that the widening is shortage pricing rather than '
     'a durable improvement in what customers pay',
     'A second and third consecutive half-year at the wider residual'),
    ('Whether to include FY2022 in the historical averages',
     'No. It is the post-listing peak-price year and would flatter every through-cycle '
     'average. It was obtained and read, and is held as a check',
     'Evidence that 2022 pricing represented a durable level rather than a peak'),
    ('How to value Borouge 4',
     f'As an operator fee stream worth about ${FN["b4"]["value"]:,.0f}m, never as owned '
     f'capacity. The sponsors quantify the fee two ways — a cumulative three-year figure '
     f'and a percentage accretion — and they do not agree, so the LOWER is carried and '
     f'the gap disclosed',
     'Publication of the recontribution terms, or an ownership interest actually '
     'transferring to Borouge plc'),
    ('What terminal growth to use',
     f'{MIN_["terminal_growth"]["value"] * 100:.1f}%, long-run dollar inflation, on the '
     f'specific ground that the company’s OWN capacity is fixed — the expansion at its '
     f'site belongs to its parents',
     'An announced expansion that Borouge plc would actually own'),
    ('Which tax rate to use',
     f'The company’s own three-year mean effective rate of {W["tax"] * 100:.2f}%, not the '
     f'9% federal headline. Borouge is taxed under the emirate-level regime that '
     f'pre-dates the federal tax',
     'A change in the fiscal regime applying to the group, or a sustained effective rate '
     'at a different level'),
    ('Whether to use the peer median multiple',
     f'No. Nine of eleven peers are loss-making and two have no defined multiple, so the '
     f'median of {D["peer_naive_median"]:.1f}x measures a collapsed denominator. Three '
     f'named through-cycle anchors are used instead',
     'A recovery that restores peer profitability, at which point a live median becomes '
     'meaningful again'),
    ('Which risk-free rate construction to use',
     f'The dollar construction at {W["rf_star"] * 100:.2f}%, because the company reports, '
     f'borrows and sells in dollars. The dirham construction gives '
     f'{W["rf_star_aed"] * 100:.2f}% and the gap is reported rather than reconciled away',
     'A change in the peg, which would make the two constructions genuinely different '
     'questions rather than two routes to the same one'),
    ('Whether the related-party debt is at arm’s length',
     f'Yes, and it was tested rather than assumed. The parent facilities price at '
     f'{W["kd_related_party"] * 100:.2f}% against an arm’s-length marginal cost of '
     f'{W["kd"] * 100:.2f}% and a sovereign floor of {W["sovereign_usd"] * 100:.2f}%. '
     f'The gap is {abs(W["kd"] - W["kd_related_party"]) * 100:.2f}%',
     'A refinancing at a materially different margin, or disclosure that the facilities '
     'carry terms a third party would not offer'),
    ('How much weight the probability bands deserve on this share',
     f'Less than usual, and the study says so. Tested over the '
     f'{BT["full"]["windows"]} independent windows the history allows, the bands scored '
     f'{BT["full"]["skill_norm"]:+.3f} against their benchmark — worse, because they are '
     f'too wide for a share this calm',
     'More trading history. The share has traded for '
     f'{BT["history_span_years"]} years and the test needs more windows than that allows'),
]:
    rows.append([j, did, over])
table(rows, [1.35, 2.95, 2.50], size=7.6)
caption('Table 5 — The judgement record.')

# ============================================================ 4 NEGATIVE RESULTS
doc.add_page_break()
H1('4  What was searched for and not found')
P('A study is shaped as much by what is missing as by what is there. Each search below '
  'came back empty, and each row says what the study did instead of filling the gap.')
rows = [['Searched for', 'Where', 'What the study did instead']]
for what, where, did in [
    ('The pricing formula of the ADNOC ethane supply arrangement, and any contracted '
     'escalation',
     'All four annual reports, all four sets of audited statements, both interim sets '
     'and every management discussion',
     'Carried zero real escalation on the contracted leg and flagged it. Inventing a '
     'formula would be worse than carrying zero and saying so; the sensitivity shows what '
     'a non-zero escalator costs'),
    ('Segmental profitability — polyethylene against polypropylene operating profit, '
     'segment assets, segment capital employed',
     'The same documents. Borouge reports as one operating segment',
     'Allocated cost across products on the disclosed physical drivers, and stated the '
     'gap in the study rather than presenting an allocation as a disclosure'),
    ('A published exchange ratio, valuation or prospectus for the expected tender offer',
     'Borouge, ADNOC and OMV investor relations',
     'Carried the offer as a catalyst and a caveat. No conversion value enters any number '
     'in the study'),
    ('A multi-year capital-expenditure programme',
     'Annual reports and every results disclosure. The company guides the year ahead only',
     'Set steady-state maintenance capital spend from the company’s own three-year '
     'outturn against its current-year guide, flagged it as the one materially top-down '
     'driver, and sensitised it'),
    ('A sovereign credit-default-swap quote for the United Arab Emirates',
     'The published country risk file, which carries CDS-based spreads for many '
     'sovereigns but not this one',
     'Published both equity risk premium bases on the rating basis and stated the absence '
     'rather than borrowing a neighbouring sovereign’s quote'),
    ('Direct access to the exchange’s own web portal',
     'adx.ae — refused with an HTTP 403 at the network layer on every attempt',
     'Not needed. Every statement was obtained from the company’s own library, and the '
     'exchange’s monthly statistics workbooks were obtained separately for the market-'
     'capitalisation cross-check'),
]:
    rows.append([what, where, did])
table(rows, [2.05, 2.25, 2.50], size=7.8)
caption('Table 6 — The negative results.')

H1('5  Where the numbers disagree between sources')
P('Two places, and both are reported rather than reconciled.')
rows = [['Disagreement', 'The two figures', 'How the study handles it']]
rows.append([
    'The risk-free rate under a hard currency peg',
    f'{W["rf_star"] * 100:.2f}% built in dollars against {W["rf_star_aed"] * 100:.2f}% '
    f'built from the dirham government bond',
    'Uses the dollar construction, because the company reports and borrows in dollars, '
    'and reports the gap in the study rather than averaging it away'])
rows.append([
    'The two quantifications of the Borouge 4 fee',
    f'${FN["b4"]["steady_from_cumulative"]:,.0f}m a year implied by the disclosed '
    f'three-year cumulative profit, against ${FN["b4"]["steady_from_accretion"]:,.0f}m '
    f'implied by the disclosed percentage accretion',
    'Carries the LOWER and shows both in the workbook. They come from the same press '
    'release and cannot both be right'])
rows.append([
    'UAE growth forecasts',
    f'{MIN_["uae_gdp_growth_cbuae"]["value"] * 100:.1f}% from the central bank against '
    f'{MIN_["uae_gdp_growth_imf"]["value"] * 100:.1f}% from the IMF for the same year',
    'Neither drives a driver. Borouge sells into more than ninety countries, so domestic '
    'growth is context rather than an input. UAE inflation IS used, and only for the '
    'domestic fixed cost leg'])
table(rows, [1.75, 2.35, 2.70], size=8.0)
caption('Table 7 — Where sources disagree.')

H1('6  Where an aggregator was used, and where it was not')
box([
    ('Used, in exactly one place. ',
     'The eleven listed peers’ multiples and margins in the study’s peer table come from '
     'market-data aggregators, observed on 9 August 2026. They are used to demonstrate '
     'that the peer set cannot produce an honest live multiple — nine of eleven are '
     'loss-making — and to cross-check the through-cycle anchors. They are labelled as a '
     'cross-check everywhere they appear.'),
    ('Not used, anywhere. ',
     'No aggregator, broker note, press summary or search-result extract is the source of '
     'any figure Borouge itself reports. Revenue, volumes, prices, costs, the balance '
     'sheet, the cash flow, the tax rate, the debt book and the share count all come from '
     'the company’s own published documents listed in Table 1 — every one of which was '
     're-downloaded and verified byte-for-byte identical before this document was '
     'written.'),
])

OUT = 'BOROUGE_Bibliography_09-08-2026.docx'
doc.save(OUT)
print(f'wrote {OUT}')
print(f'paragraphs: {len(doc.paragraphs)}, tables: {len(doc.tables)}')
print(f'company inputs registered: {len(CIN)}, macro inputs registered: {len(MIN_)}')
