"""SAVOLA -- the [R-ANCHOR-01] forecast anchor, measured rather than asserted.

Adds `forecast_anchor` to study_numbers.json. It CHANGES NO DRIVER, NO RATE AND
NO VALUE: every figure here is either read back out of the committed numbers file
or read off a filing this study already holds, and the record's only job is to
say what the forecast claims against what the company has just filed.

WHAT THE RATE IS. The forecast is built bottom-up -- category volume x GP/tonne
for Food Processing, sales-per-store for Panda, a held margin for Food Services
and Frozen -- so there is no single typed margin driving it. The rate the anchor
governs is the GROUP EBITDA MARGIN, which is what those drivers sum to, what the
committed path publishes, and what the study's own gap review quotes.

WHY THE ANCHOR IS THE REVIEWED HALF AND NOT THE AUDITED YEAR. That is the whole
rule: a near-term reviewed actual outranks a stale full-year rate. The study holds
the reviewed interim condensed consolidated statements for the six months ended
30 June 2026, and they are the latest reviewed period. Against the FY2025 audited
year the forecast opens 1.96% relatively below and nothing fires; against the
reviewed half it opens 6.15% relatively below and the rule fires. The audited year
is the comparison that flatters, which is precisely why the rule names the other.

THE BASIS IS MADE LIKE FOR LIKE BEFORE ANYTHING IS COMPARED. The company's own H1
release quotes EBITDA of SAR 1,316mn on a basis that INCLUDES the SAR 34.241mn
share of equity-accounted investees; this model's EBITDA excludes associates (they
are carried separately, and the associate itself is capitalised in the bridge) and
does not deduct the net impairment loss on financial assets, exactly as the filed
years are built. So the half is rebuilt line by line on the model's own definition
straight off the reviewed statement. Doing so makes the measured gap SMALLER, not
larger -- 6.15% instead of 8.76% -- so the basis correction cannot be accused of
manufacturing the breach it reports.

ARITHMETIC IS THE ARBITER. Each half is asserted to reproduce the "Results from
operating activities" line the same statement prints, from its own components,
before either is used for anything.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json'), encoding='utf-8'))


def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)


Q226 = ("Reviewed interim condensed consolidated FS, three and six months ended "
        "30-Jun-2026, savola.com/en/investors/financial-statements, interim "
        "condensed consolidated statement of profit or loss (page 4) and statement "
        "of cash flows (page 8)")
IRQ2 = "Company Q2-2026 investor presentation, savola.com, Aug-2026 (COMPANY_IR)"
_D = "2026-08-05"          # the date this study already registers for this filing

# ---- the reviewed half, and its own comparative half, SAR '000 as filed -------
# The comparative column is on the face of the SAME statement, which is what makes
# the period pair like-for-like: same basis, same six-month season, both reviewed.
H1_26 = dict(
    rev=I(13587592, Q226 + ": revenues, six months ended 30-Jun-2026", _D, "Company"),
    cogs=I(10962120, Q226 + ": cost of revenues", _D, "Company"),
    sda=I(1586123, Q226 + ": selling and distribution expenses", _D, "Company"),
    adm=I(394059, Q226 + ": administrative expenses", _D, "Company"),
    oth=I(26420, Q226 + ": other operating income, net", _D, "Company"),
    dna=I(607672, Q226 + ": depreciation and amortisation, cash-flow statement "
          "(segment note 14 foots to the same figure)", _D, "Company"),
    imp=I(9914, Q226 + ": net impairment loss on financial assets -- excluded, as "
          "in the filed years", _D, "Company"),
    assoc=I(34241, Q226 + ": share of results in equity-accounted investees, net of "
            "zakat and tax -- excluded, as in the filed years", _D, "Company"),
    rfo=I(696037, Q226 + ": results from operating activities (the footing target)",
          _D, "Company"),
)
H1_25 = dict(
    rev=I(13080036, Q226 + ": revenues, comparative six months ended 30-Jun-2025",
          _D, "Company"),
    cogs=I(10511555, Q226 + ": cost of revenues, comparative", _D, "Company"),
    sda=I(1604014, Q226 + ": selling and distribution expenses, comparative", _D, "Company"),
    adm=I(411835, Q226 + ": administrative expenses, comparative", _D, "Company"),
    oth=I(42242, Q226 + ": other operating income, net, comparative", _D, "Company"),
    dna=I(592479, Q226 + ": depreciation and amortisation, comparative", _D, "Company"),
    imp=I(12776, Q226 + ": net impairment loss on financial assets, comparative",
          _D, "Company"),
    assoc=I(18394, Q226 + ": share of results in equity-accounted investees, "
            "comparative", _D, "Company"),
    rfo=I(600492, Q226 + ": results from operating activities, comparative", _D, "Company"),
)


def v(block):
    return {k: float(x['value']) for k, x in block.items()}


def foots(block, label):
    """The statement must reproduce its own operating line from its own components."""
    h = v(block)
    calc = h['rev'] - h['cogs'] - h['sda'] - h['adm'] + h['oth'] - h['imp'] + h['assoc']
    assert abs(calc - h['rfo']) < 1.0, (label, calc, h['rfo'])
    return h


def op_ebitda(h):
    """The model's own definition: ex-associates, ex-impairment, D&A added back.
    Identical in shape to compute.py's op_ebitda for the filed years."""
    return h['rev'] - h['cogs'] - h['sda'] - h['adm'] + h['oth'] + h['dna']


h26, h25 = foots(H1_26, 'H1-2026'), foots(H1_25, 'H1-2025')
EB26, EB25 = op_ebitda(h26), op_ebitda(h25)
M26, M25 = EB26 / h26['rev'], EB25 / h25['rev']

# the mechanism's measure, on the same pair, from the same statement
CUR25, CUR26 = h25['cogs'] / h25['rev'], h26['cogs'] / h26['rev']

# ---- the forecast, read back out of the committed numbers file ----------------
PATH = [float(x) for x in D['fcst']['ebitda_margin']]
FIRST = PATH[0]
FY25 = D['hist_is']['FY25']
M_FY25 = float(FY25['ebitda']) / float(FY25['rev'])
COMPANY_BASIS = float(D['h1_2026']['ebitda_company']) / float(D['h1_2026']['rev'])

GAP_REL = (FIRST - M26) / abs(M26)
PATH_DROP_REL = (min(PATH) - PATH[0]) / abs(PATH[0])

# the implied second half, which is where the claim actually lives
H2_26_REV = float(D['fcst']['rev'][0]) - h26['rev'] / 1000.0
H2_26_EB = float(D['fcst']['ebitda'][0]) - EB26 / 1000.0
H2_26_M = H2_26_EB / H2_26_REV
H2_25_REV = float(FY25['rev']) - h25['rev'] / 1000.0
H2_25_EB = float(FY25['ebitda']) - EB25 / 1000.0
H2_25_M = H2_25_EB / H2_25_REV
H2_REL = (H2_26_M - H2_25_M) / abs(H2_25_M)

D['forecast_anchor'] = dict(
    rate_name='EBITDA margin',
    latest_reviewed_period='H1-2026, six months ended 30 June 2026, reviewed interim',
    latest_reviewed_date='2026-06-30',
    latest_reviewed_rate=M26,
    first_forecast_rate=FIRST,
    forecast_path=PATH,
    # ---- the mechanism, named from the closed list, sourced and measured -------
    # The forecast opens 6.15% relatively below the reviewed half. What carries the
    # step is the Food Processing GP/tonne path, which sets FY2026E below the level
    # the half realised on all three registered categories -- oil 740 against an
    # H1 762, sugar 215 against 218, pasta 520 against 525 -- and the study's own
    # driver justification names the reason: a replacement-cost squeezed second
    # half, on the company's own Q3/Q4 statement.
    #
    # The measurement is the clause that does the work, and here it agrees. Cost of
    # revenues per unit of revenue, taken off the two columns of the SAME reviewed
    # statement -- same basis, same six-month season, both reviewed -- ROSE from
    # 80.363% to 80.677%. Input cost did outpace realised price in the company's own
    # like-for-like pair, which is the direction the mechanism claims. This is the
    # test AMOC failed and EGCH passed on the identical measure.
    mechanism=dict(
        name='input_cost_outpacing_price',
        disclosure="the Q2-2026 investor presentation states under Operating "
                   "Environment: \"Despite supply-chain disruptions, timely sourcing "
                   "and commercial actions supported a stronger-than-expected Q2 "
                   "performance. Some replacement-cost pressure is expected to "
                   "continue through Q3 and Q4, but remains manageable within the "
                   "Group's ongoing pricing, procurement and cost-efficiency "
                   "measures.\" The same disclosure is what the study's oil GP/tonne "
                   "driver cites for setting FY2026E at 740 against an H1-2026 "
                   "realised 762, and the FAO vegetable-oil index reading it names "
                   "beside it. The company is an edible-oil and sugar refiner buying "
                   "globally-priced soft commodities and selling into administered "
                   "and competitive domestic retail, so the replacement cost of the "
                   "input moves ahead of the realised output price by construction "
                   "of the working-capital cycle.",
        like_for_like=dict(
            measures='cost of revenues per unit of revenue, six months ended 30 June, '
                     'both columns of the reviewed interim statement',
            period_a='H1-2025', value_a=CUR25,
            period_b='H1-2026', value_b=CUR26,
            higher_is_worse=True),
        source=IRQ2 + '; ' + Q226,
    ),
    note=(
        "MEASURED, NOT ASSERTED, AND THE QUALIFICATIONS ARE PART OF THE RECORD. "
        "The rate is the group EBITDA margin on this model's own definition -- ex "
        "share of associates, ex net impairment on financial assets, D&A added back "
        "-- rebuilt for the reviewed half line by line off the interim statement, "
        "which reproduces its own results-from-operating-activities line to the "
        "riyal in both columns. On that basis the half ran %.4f%%. The company's own "
        "release quotes %.4f%% for the same half on a basis that includes the SAR "
        "34.241mn associate share; the like-for-like figure is used because it is "
        "the one the forecast is comparable to, and because it makes the gap smaller "
        "rather than larger. The audited FY2025 year ran %.4f%%, against which the "
        "forecast opens only %.2f%% relatively low and nothing would fire -- the "
        "stale full-year rate is the flattering comparison, which is the reason this "
        "rule names the reviewed one. "
        "WHERE THE CLAIM ACTUALLY SITS: the first forecast year already contains the "
        "filed half, so the step is entirely in the half not yet filed. The implied "
        "second half is %.4f%% against the company's own filed second half of "
        "%.4f%% a year earlier -- %.2f%% relatively below -- while the half the study "
        "does hold came in ABOVE its own prior-year half, %.4f%% against %.4f%%. "
        "SIZE IS NOT DIRECTION AND THE RECORD SAYS SO: the measured input-cost drift "
        "is %.4f points of revenue over the year pair, and the forecast asks %.4f "
        "points off the annual margin relative to the reviewed half. The mechanism "
        "carries the sign and part of the magnitude, not all of it. "
        "AND THE MEASURE IS THE MECHANISM'S, NOT THE RATE'S: gross margin did fall "
        "year on year in the half (%.4f%% to %.4f%%), which is what the mechanism "
        "claims, while the EBITDA margin ROSE over the same pair because selling and "
        "administrative costs fell on higher revenue. A reader is owed both. "
        "The disclosure is management's own forward statement and this house scores "
        "guidance rather than consuming it; it is admitted here because it warns of "
        "cost pressure rather than promising performance, and because the filings "
        "measure the same direction independently -- but the same sentence calls the "
        "pressure \"manageable\", and an implied second half %.2f%% below the "
        "company's own prior second half is a stronger claim than that word supports. "
        "The path clause does not fire: the forecast falls only %.2f%% relative from "
        "its opening year across the explicit window (%.4f%% to %.4f%%), so the "
        "opening step is the whole of it."
        % (100 * M26, 100 * COMPANY_BASIS, 100 * M_FY25, -100 * (FIRST - M_FY25) / M_FY25,
           100 * H2_26_M, 100 * H2_25_M, -100 * H2_REL, 100 * M26, 100 * M25,
           100 * (CUR26 - CUR25), 100 * (M26 - FIRST),
           100 * (1 - CUR25), 100 * (1 - CUR26),
           -100 * H2_REL, -100 * PATH_DROP_REL, 100 * PATH[0], 100 * min(PATH))),
    basis_inputs=dict(
        definition='rev - cogs - selling and distribution - administrative + other '
                   'operating income, net + depreciation and amortisation; associates '
                   'and the net impairment on financial assets excluded, matching the '
                   'construction the study uses for FY2023-FY2025',
        h1_2026=H1_26, h1_2025=H1_25,
        derived=dict(
            ebitda_h1_2026_sar000=EB26, ebitda_h1_2025_sar000=EB25,
            margin_h1_2026=M26, margin_h1_2025=M25,
            margin_fy2025_audited=M_FY25, margin_h1_2026_company_basis=COMPANY_BASIS,
            cost_per_unit_revenue_h1_2025=CUR25, cost_per_unit_revenue_h1_2026=CUR26,
            implied_h2_2026_margin=H2_26_M, filed_h2_2025_margin=H2_25_M,
            gap_relative=GAP_REL, path_drop_relative=PATH_DROP_REL)),
)

with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(D, f, indent=1, default=float)

print('SAVOLA [R-ANCHOR-01] forecast anchor')
print('  rate                       EBITDA margin (model basis, ex-associates)')
print('  latest reviewed  H1-2026   %.4f%%   (company basis %.4f%%; FY2025 audited %.4f%%)'
      % (100 * M26, 100 * COMPANY_BASIS, 100 * M_FY25))
print('  first forecast   FY2026E   %.4f%%' % (100 * FIRST))
print('  gap                        %+.4f pp   %+.2f%% RELATIVE   -> FIRES'
      % (100 * (FIRST - M26), 100 * GAP_REL) if GAP_REL < -0.05 else
      '  gap                        %+.4f pp   %+.2f%% relative   -> inside tolerance'
      % (100 * (FIRST - M26), 100 * GAP_REL))
print('  path                       %s' % ' '.join('%.3f%%' % (100 * x) for x in PATH))
print('  path drop from opening     %+.2f%% relative -> clause two does not fire'
      % (100 * PATH_DROP_REL))
print('  implied H2-2026E           %.4f%%  against filed H2-2025 %.4f%%  (%+.2f%% rel)'
      % (100 * H2_26_M, 100 * H2_25_M, 100 * H2_REL))
print('  mechanism                  input_cost_outpacing_price')
print('  like-for-like              cost/unit revenue %.4f%% (H1-2025) -> %.4f%% (H1-2026)'
      % (100 * CUR25, 100 * CUR26))
print('  direction                  measured RISE of %.4f pp -- agrees with the mechanism'
      % (100 * (CUR26 - CUR25)))
print('study_numbers.json updated')
