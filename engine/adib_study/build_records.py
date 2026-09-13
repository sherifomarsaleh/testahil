#!/usr/bin/env python3
"""ADIB-Egypt — the study's committed numbers. GENERATED; never hand-edited.

Every gate outside this study reads THIS file, not the document.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'adib_walkforward'))
import compute as C  # noqa: E402
import gates         # noqa: E402  — the four standing assertions


def main():
    # THE STUDY'S OWN CODE CALLS THE FOUR ASSERTIONS, and they RAISE rather than warn.
    # A record written by a study that has not cleared them is a record of nothing.
    gates.run()
    d = dict(
        meta=dict(ticker='ADIB',
                  company='Abu Dhabi Islamic Bank (ADIB) – Egypt S.A.E.',
                  not_to_be_confused_with='ADIB Group PJSC (ADX: ADIB), the Abu Dhabi '
                                          'parent, which is the separate covered name ADIBUAE',
                  market='EGX', currency='EGP', asof=C.STUDY_DATE,
                  spot=C.SPOT, spot_date='2026-09-03',
                  spot_source='the committed price file for 3 September 2026 — the latest known '
                              'price. The published site carries 54.40 at the 23 August close, '
                              'which is older.',
                  shares_mn=C.SHARES, mktcap=C.SPOT * C.SHARES,
                  klass='bank', sector='Islamic commercial banking — Egypt',
                  fy_note='financial year ends 31 December',
                  standard='2026.09.07'),
        central=C.CENTRAL, spot=C.SPOT,
        fair=dict(bear=C.BEAR, base=C.CENTRAL, full=C.FULL),
        gap_to_spot=C.CENTRAL / C.SPOT - 1,
        primary=C.PRIMARY,
        lens_architecture=('One class primary IS the central; the others are '
                           'cross-checks. bank -> ddm primary, with residual income, a '
                           'relative multiple and book value beside it. No typed weights.'),
        lenses=dict(dividend_discount=C.DDM['per_share'],
                    free_cash_flow_to_equity=C.FCFE['per_share'],
                    residual_income=C.RI['per_share'],
                    relative_multiples=C.REL['per_share'],
                    book_value_and_sustainable_return=C.BOOK['per_share'],
                    book_value_floor=C.BOOK['floor'],
                    normalised_earnings_power=C.NORM['per_share']),
        present_value_reads=C.PV_READS,
        envelope=dict(bear=C.BEAR, full=C.FULL,
                      construction='the range of the present-value reads on one clock'),
        cost_of_capital=dict(
            rf=C.RF, rf_date='2026-08-06',
            rf_staleness_days=34,
            rf_staleness_note='the house path\'s own 14-day rule flags this as stale; four '
                              'live re-source routes were attempted on 2026-09-09 and all '
                              'four failed. Declared, sensitised, and named as an open data '
                              'request.',
            sovereign_default_spread=C.SOV_SPREAD, rf_star=C.RF - C.SOV_SPREAD,
            # THE BIBLIOGRAPHY COMPARES THIS STUDY'S SPREAD WITH THE HOUSE PATH'S, AND THE
            # SECOND FIGURE WAS TYPED. A number a document prints and the study does not
            # commit is a number the prose check cannot match and nothing can verify — so
            # the comparison went red the moment the checker looked at it, on a sentence
            # that was true. Read from engine/macro_paths/EG.json at build time.
            sov_default_spread_house_path=C.EG_PATH_SPREAD,
            erp=C.ERP, beta=C.BETA, ke=C.KE0, ke_rating_basis=C.KE_RATING,
            # [R-ENF-03] ONE FACT, TWO NAMES — AND THE SECOND ONE WENT STALE. This study
            # publishes its cost of capital twice: here, and again in
            # cost_of_capital_record. The split premium was added to the record and not to
            # this block, and the workbook reads THIS one — so its three lens values and
            # their Summary copies all recomputed the old rate while the study published the
            # new one. The negative control found the same duplication in the terminal an
            # hour earlier. Both blocks now carry the legs, from the same variables, so they
            # cannot disagree about what the rate is made of.
            erp_mature=C.ERP_MATURE, crp=C.CRP, crp_effective=C.CRP,
            crp_terminal=C.CRP_TERM, crp_effective_terminal=C.CRP_TERM,
            lambda_country=1.0, crp_foreign=0.0, ke_construction='split_premium',
            ke_double_counted_retired=C.KE_DOUBLE,
            ke_terminal=C.KE_TERM, ke_terminal_construction='split_premium',
            ke_path=list(C.KE_PATH),
            terminal_growth=C.G_TERM, terminal_rf=C.RF_TERM,
            terminal_inflation=C.EG.terminal_inflation,
            terminal_erp=C.ERP_TERM),
        beta_record={k: (list(v) if isinstance(v, tuple) else v)
                     for k, v in C._BETA.items() if k != 'warnings'},
        base_year=dict(year='FY2025', **{k: v for k, v in C.FY25.items()}),
        base_year_observed_ratios=C.OBS,
        latest_reviewed=dict(period='H1-2026', **C.H1),
        latest_reviewed_annualised=C.H1OBS,
        projection=[{k: v for k, v in r.items()} for r in C.P],
        far_year_ranges=C.FAR,
        far_year_range_source=('engine/adib_walkforward/forward_ranges.json — the '
                               'FUNDAMENTAL walk-forward\'s own attributable-profit error '
                               'dispersion, centred on its own median. Not the price-engine '
                               'walk-forward and not the technical one.'),
        sensitivity=[dict(driver=a, value=b, change=c) for a, b, c in C.SENS],
        walkforward=dict(
            which='the FUNDAMENTAL walk-forward [R-FCAL-01]',
            scope='full', origins='FY2014..FY2024, horizons 1-5, 45 cells per driver',
            corrections_promoted=0,
            note='no correction from that record enters these drivers; every candidate '
                 'either failed the by-origin test, failed the second clause, or is an '
                 'aggregate of drivers already corrected. What the run DID put here is the '
                 'years 3-5 ranges and the knowledge that a flat-share volume rule '
                 'under-forecasts this name.'),
        # THE REGISTER IS COMMITTED UNDER THE NAME EVERY GATE READS [10-09-2026].
        # It was emitted as `register` while scripts/check_source_integrity.py and the
        # rest of the shared checks read `inputs`, so a study that HAD a full
        # four-field register was reported as having none -- "the input register is not
        # in the committed numbers file", of a file that contained it. One fact, two
        # names, and the checker looking under the other one. `register` is kept as an
        # alias to the same object so this study's own three builders keep working;
        # they read one dict, not two.
        inputs={k: dict(value=(v.value if not isinstance(v.value, (list, dict)) else v.value),
                        source=v.source, date=v.date, ring=v.ring)
                for k, v in C.REG.items()},
    )
    d['register'] = d['inputs']          # the same object, under the study's own older name
    # AND THE COST-OF-CAPITAL RECORD UNDER ITS CANONICAL NAME, for the same reason:
    # check_cost_of_capital.py reads a CLOSED list of three key names and this study
    # used a fourth. The list is closed on purpose -- an open one lets a study opt out
    # of the check by inventing a name -- so the study moves, not the list.
    # THE RECORD DECLARES ITS MARKET. The block carried rates and no country, so the
    # gate could not resolve a house macro path for it and refused -- correctly: a
    # cost of capital that does not say which economy it is built on cannot be
    # checked against that economy's own path.
    # THE RECORD UNDER THE CANONICAL FIELD NAMES the shared gate reads. This study
    # named the same quantities differently -- `rf` for the observed yield,
    # `sovereign_default_spread` for the spread, `ke` for the explicit cost of equity,
    # `terminal_rf` for the terminal risk-free -- so a record that carried every one of
    # them was reported as carrying none. One fact, two names, again.
    _cc = d['cost_of_capital']
    d['cost_of_capital_record'] = dict(
        _cc,
        market='EG',
        rf_observed=_cc['rf'],
        default_spread=_cc['sovereign_default_spread'],
        rf_star=_cc['rf_star'],
        erp=_cc['erp'],
        # THE RATING-BASIS PREMIUM IS READ, NOT SOLVED OUT OF THE RATE. This line used to
        # invert the cost of equity — (ke_rating - rf_star) / beta — which worked only while
        # the identity was rf* + beta x the whole premium, and quietly used the CDS-netted
        # rf* against a rating-basis Ke besides. Under the split it would have back-solved a
        # premium that is not the premium, so it now reads the registered figure. Solving an
        # input out of the answer it explains is the reverse-engineered construction this
        # house prohibits, and it survived here because the arithmetic happened to close.
        erp_rating=C.ERP_R,
        erp_basis='market',
        beta=_cc['beta'],
        beta_source='own_stock_regression',
        beta_source_note=(
            'engine/beta_regression.own_stock_beta("ADIB", "EG", "EGX") — a weekly Dimson '
            'regression against the published EGX30 over 256 observations to 20-Aug-2026, '
            'attested by assert_beta_provenance(). Named from the closed list so that a '
            'measured regression cannot be mistaken for a priced fallback or a typed number.'),
        # [R-COC-03] the split, published leg by leg
        erp_mature=C.ERP_MATURE, crp=C.CRP, crp_effective=C.CRP,
        crp_terminal=C.CRP_TERM, crp_effective_terminal=C.CRP_TERM,
        lambda_country=1.0, crp_foreign=0.0,
        ke_construction='split_premium',
        ke_construction_note=(
            'rf* + beta x the MATURE premium + the country premium charged FLAT and once. '
            'Every branch, deposit and financing of this bank is in Egypt, so lambda is '
            '1.00 and the whole country premium is the Egyptian one. The terminal splits '
            'the same way and against the SAME mature leg: what normalises over a '
            'perpetuity is the country premium, not the mature one.'),
        ke_exp=_cc['ke'],
        rf_terminal=_cc['terminal_rf'],
        erp_terminal=_cc['terminal_erp'],
        ke_terminal=_cc['ke_terminal'],
        terminal_growth=_cc['terminal_growth'],
        # A BANK HAS NO WEIGHTED AVERAGE COST OF CAPITAL AND THIS RECORD SAYS SO RATHER
        # THAN INVENTING ONE. Deposits are the raw material of the business and sit
        # inside the margin, not in the discount rate; a "cost of debt" for a bank is
        # its cost of funding, which is a REVENUE-side input here and is already in the
        # forecast at 11.22%. Supplying a debt weight and a blended rate to satisfy a
        # field would be the exact error this study's own gap review names under its
        # discount-rate heading, and a number typed to pass a check is worse than a
        # check that fails.
        # THE ALTERNATIVE PREMIUM BASIS, PUBLISHED BESIDE THE ADOPTED ONE rather than
        # only inside a Ke this record already carries. The rating-basis default spread
        # is registered; the normalised rate on that basis follows from it.
        sensitivity=dict(
            other_basis='rating',
            other_default_spread=C.REG['sov_default_spread_rating'].value,
            rf_star_other_basis=(_cc['rf'] - C.REG['sov_default_spread_rating'].value),
            ke_other_basis=_cc['ke_rating_basis'],
        ),
        no_wacc_reason=('bank: equity flows are discounted at the cost of equity and '
                        'there is no weighted average. Deposits are raw material, not '
                        'financing, and their cost is inside the net interest margin.'),
        # THE SAME FACT, SAID TO THE OTHER GATE. With no enterprise value there is no
        # invested capital to replace and no reinvestment rate, so this study publishes no
        # enterprise terminal value and the 1/g construction test has nothing to bite on.
        # Declared rather than left absent: a study that simply exposes no terminal reads
        # as one that will not show its own [R-ENF-04], and the terminal gate corroborates
        # the claim against the terminal cost of equity and growth published beside it.
        no_terminal_value_reason=('bank: deposits are raw material rather than financing, '
                                  'so there is no enterprise value and no invested capital '
                                  'to replace. The terminal is an equity-side one — a '
                                  'terminal cost of equity and a terminal growth rate, both '
                                  'published in the cost-of-capital record.'),
    )
        # [R-FCAL-01] THE SCOPE DECISION WAS MADE AND WAS NOT WHERE THE GATE READS IT.
    # It has been stated since 09-09-2026 in engine/adib_walkforward/PRE_REGISTRATION,
    # the run exists on disk with its 11 origins and 45 cells, and the study's committed
    # numbers said nothing — so check_walkforward_scope read a study that had decided
    # nothing. A decision recorded only in the document that acts on it is a decision no
    # gate can see, which is the same shape as a line computed and not published.
    # [R-EPS-01] WHAT STANDS BETWEEN THE FILED EARNINGS PER SHARE AND THIS STUDY'S OWN
    # ARITHMETIC, NAMED. Dividing FY2025 attributable profit by the share count this study
    # carries gives EGP 8.39 against a filed 11.25 — a 25% gap, and it is entirely the
    # SHARE COUNT rather than the profit. The filed figure is struck on the weighted
    # average over a capital-increase year, about 1,119mn; the year ENDED at 1,200mn and
    # the count today is 1,500mn after the increase to EGP 15bn completed in 2026. A study
    # valuing the bank as it stands must divide by the count as it stands, and the filed
    # per-share figure is not comparable to it. Named rather than reconciled away: an
    # unnamed difference is indistinguishable from an error.
    _cc_np = C.NP_FY25
    _naive = _cc_np / C.SHARES
    d['eps_reconciliation'] = dict(
        reported_eps=C.EPS_FY25,
        attributable_profit=_cc_np,
        shares_issued=C.SHARES,
        naive_eps=_naive,
        what='the share count alone: the filed figure is struck on the weighted average '
             'over a capital-increase year, this study divides by the count in issue today',
        difference=C.EPS_FY25 - _naive,
        components=[dict(
            item='weighted-average versus current share count',
            amount=0.0,
            per_share=C.EPS_FY25 - _naive,
            source='ADIB-Egypt audited consolidated financial statements FY2025, '
                   'earnings-per-share note, read with the paid-up capital note',
            note='12,588,572 / 11.25 implies about 1,119mn shares — the weighted average '
                 'across a year in which paid-up capital rose. The year ended at 1,200mn '
                 'and 1,500mn are in issue now. NO PROFIT IS IN DISPUTE: the numerator is '
                 'the same figure in both, and nothing is added to or taken from it.')],
        charges_it=False,
        charged_at=0.0,
        note='This bank has raised capital in most years of its recent history, so the '
             'weighted-average count trails the closing count structurally rather than '
             'occasionally. The valuation divides by the current count because it values '
             'the bank as it stands; the filed per-share figure is reported beside it so a '
             'reader can see the two are not the same measure.')

    d['walkforward_scope'] = dict(
        scope='FULL',
        sourceable_fiscal_years=16,
        status='run',
        basis=('Sixteen sourceable consolidated fiscal years, FY2010-FY2025, every one '
               'from the issuer\'s own audited consolidated statements on adib.eg and '
               'every one footing against its own arithmetic. Sixteen is at or above the '
               'eight a FULL scope needs, so the run takes all origins from the first '
               'year with a five-year history behind it, at horizons 1 to 5.'),
        note=('Run 09-09-2026. Origins FY2014-FY2024, eleven of them, 45 origin-horizon '
              'cells, truncated at FY2025 as the last reported year. Pre-registered in '
              'engine/adib_walkforward/PRE_REGISTRATION_09-09-2026.md before any origin '
              'was built.'),
    )

    # ================= THE FOUR STANDARD RECORDS THIS STUDY DID NOT COMMIT =========
    # Added 13-09-2026. ADIB is the newest study in the book and it committed none of
    # them, so FIVE standing gates were red on this one name: check_bridge,
    # check_forecast_anchor, check_ground_up, check_lens_design and
    # check_corrections_applied. Every one of them reported the same underlying fact --
    # that it could not read a record -- and an absent record reads exactly like a
    # breaching one [R-ENF-04], which is the point. NOTHING BELOW MOVES A NUMBER: every
    # figure is read out of this study's own committed arithmetic, above.

    # ---- 1. WHAT THE WALK-FORWARD ADOPTED. Silence and 'none adopted' are the same file
    # to a reader and different facts about the work.
    _cl = json.load(open(os.path.join(HERE, '..', 'adib_walkforward',
                                      'corrections_log.json'), encoding='utf-8'))
    d['adopted_corrections'] = []
    d['adopted_corrections_note'] = (
        'the walk-forward on this name tested %d correction candidates under the two-clause '
        'test and adopted NONE. Four drivers (%s) carry a watch flag rather than a '
        'correction, and the aggregates (%s) were refused as aggregates, which corrections '
        'may not be applied to. Recorded in engine/adib_walkforward/corrections_log.json; '
        'EMPTY RATHER THAN ABSENT.'
        % (_cl['candidates'], ', '.join(_cl['watch_flags']),
           ', '.join(_cl.get('refused_as_aggregates', []))))

    # ---- 2. THE LENS RECORD. The architecture was committed as a SENTENCE and the six
    # answers as a bare dict, so a gate reading this book could see neither which lens is
    # primary nor what its range is built from. Both facts already existed in this file;
    # neither was in a shape anything could read.
    _L = d['lenses']
    d['lens_record'] = {
        # THE CLASS IS THE REGISTERED KEY, NOT A DESCRIPTION OF IT. This said
        # 'bank - deposit-funded, valued on equity directly', which is true and is
        # not a class: LENS_REGISTRY keys the lens architecture AND the lesson
        # taxonomy, so an unregistered string has no primary and carries no lessons.
        'class': 'bank',
        'central': d['central'],
        'primary': dict(
            kind='ddm',
            value=_L['dividend_discount'],
            range=dict(low=d['envelope']['bear'], high=d['envelope']['full']),
            range_note=('the span of the three PRESENT-VALUE reads on one clock — free cash '
                        'flow to equity below, residual income above — rather than a driver '
                        'flexed across a range. On a bank the three are one model entered '
                        'through three doors, so their spread measures the construction and '
                        'not the business.'),
            range_basis=dict(
                driver='the present-value construction itself, across its three entries',
                low=d['envelope']['bear'], high=d['envelope']['full'], macro_held=True,
                evidence=('dividend discount %.4f, free cash flow to equity %.4f, residual '
                          'income %.4f, all on the same five-year window, the same cost of '
                          'equity schedule and the same house macro path. The cost of '
                          'capital and terminal growth do not move between them.'
                          % (_L['dividend_discount'], _L['free_cash_flow_to_equity'],
                             _L['residual_income']))),
        ),
        'note': ('one class primary IS the central and the others are cross-checks, with no '
                 'typed weights [R-LENS-03]. The cross-checks are a relative multiple at '
                 '%.2f, book value and a sustainable return at %.2f, a book floor at %.2f '
                 'and normalised earning power at %.2f. THE RELATIVE READ IS THE HIGHEST '
                 'OF ALL SEVEN and is not blended in.'
                 % (_L['relative_multiples'], _L['book_value_and_sustainable_return'],
                    _L['book_value_floor'], _L['normalised_earnings_power'])),
    }

    # ---- 3. THE FORECAST ANCHOR. On a bank the rate that matters is the net interest
    # margin, and this forecast OPENS BELOW the latest reviewed half — which is the
    # direction that owes a mechanism, and it has one.
    _P = d['projection']
    _nim0 = d['latest_reviewed_annualised']['nim']
    _path = [x['nim'] for x in _P]
    d['forecast_anchor'] = dict(
        rate_name='net interest margin',
        latest_reviewed_period='H1-2026, reviewed, annualised',
        latest_reviewed_date='2026-06-30',
        latest_reviewed_rate=_nim0,
        first_forecast_rate=_path[0],
        forecast_path=_path,
        note=('the forecast opens at %.3f%% against a latest reviewed %.3f%% — %.2f points '
              'BELOW it, %.1f%% relative — and then falls further, to %.3f%% by FY2030. '
              'THE MECHANISM IS DISCLOSED MONETARY POLICY AND IT IS NAMED RATHER THAN '
              'ASSUMED: the reviewed half was earned at the top of an Egyptian tightening '
              'cycle, and the central bank is easing. A deposit-funded bank re-prices its '
              'assets faster than its funding on the way down, so a margin struck at the '
              'peak is not a margin that can be held; carrying %.3f%% flat for five years '
              'would be forecasting that the easing cycle does not happen. The study says '
              'in terms that this compression, a normalised loss charge after a half-year '
              'at almost nothing, and an Egyptian-pound cost of equity near thirty per '
              'cent are the three swing factors.'
              % (100 * _path[0], 100 * _nim0, 100 * (_nim0 - _path[0]),
                 100 * (_path[0] / _nim0 - 1), 100 * _path[-1], 100 * _nim0)))

    # ---- 4. THE DRIVER LINES. The ground-up gate wants the LINES, not the summary an
    # assertion returns: a top line that is one growth rate on the whole company with no
    # unit behind it is the defect it exists to catch. A bank's unit is the balance sheet.
    _y0 = _P[0]
    _avg = _y0['avg_total_assets']
    # OPERATING INCOME IS THE BASE, and the shares foot to it. A bank has no tonnes, so
    # the "unit" is the balance sheet and every income line is a RATE ON A STOCK.
    _opinc = _y0['net_funds'] + _y0['net_fees'] + _y0['other_nii']
    d['driver_lines'] = [
        dict(name='Net funds income', level='unit',
             share_of_revenue=_y0['net_funds'] / _opinc,
             unit='average total assets, EGP %.0fmn in the first forecast year' % _avg,
             unit_source='the reviewed consolidated balance sheet at 30 June 2026, averaged '
                         'with the audited sheet at 31 December 2025',
             price_basis='net interest margin, %.3f%% in the first forecast year, struck on '
                         'average total assets and falling to %.3f%% by FY2030 as the easing '
                         'cycle repricesncome faster than funding'
                         % (100 * _y0['nim'], 100 * _P[-1]['nim']),
             cost_basis='the cost of funds is INSIDE this line, not beside it: the margin is '
                        'financing income less cost of funds, and both legs are filed '
                        'separately in the reviewed statements'),
        dict(name='Net fee income', level='unit',
             share_of_revenue=_y0['net_fees'] / _opinc,
             unit='average total assets, the same stock',
             unit_source='as above',
             price_basis='fee ratio, %.4f%% of average assets, held at the reviewed '
                         'half\'s own annualised rate'
                         % (100 * d['latest_reviewed_annualised']['fee_ratio']),
             cost_basis='fee EXPENSE is netted here and is filed separately; the gross and '
                        'the net are both in the reviewed statements'),
        dict(name='Other operating income — dividends and trading', level='derived',
             share_of_revenue=_y0['other_nii'] / _opinc,
             unit=None, unit_source=None,
             price_basis='carried at the reviewed half\'s annualised level, escalated on '
                         'nothing',
             # THE GATE IS RIGHT TO DEMAND THIS AND None WAS THE WRONG ANSWER. A margin is
             # an output, so a line that says how revenue was built and nothing about cost
             # is a line whose margin is an assumption. Here the honest cost basis is that
             # there is no direct cost, and saying so is a fact about the line rather than
             # a blank.
             cost_basis='NO DIRECT COST, and that is a statement rather than an omission: '
                        'dividend and trading income arrive gross in the filed statements '
                        'and carry no cost of sales. The cost of running the bank sits in '
                        'administrative expense, which is forecast as one base against the '
                        'whole institution and is not allocated across income lines -- so '
                        'this line has no margin of its own, and none is claimed for it.',
             gap_note='THE GAP IS STATED RATHER THAN DRESSED UP. Dividend and trading income '
                      'are not a rate on a stock and there is no unit behind them: they are '
                      'carried at the level the reviewed half earned. At %.1f%% of operating '
                      'income the line cannot carry the answer, and if it could this would '
                      'be the wrong way to build it.'
                      % (100 * _y0['other_nii'] / _opinc)),
    ]
    d['ground_up'] = dict(
        unit='the balance sheet — average total assets for income, financing to customers '
             'for the loss charge',
        lines=len(d['driver_lines']),
        note=('a bank has no tonnes and no units shipped, so the ground-up unit is the '
              'balance sheet itself and every income line is a RATE ON A STOCK. The top '
              'line is not one growth rate on the whole company: it is the margin on '
              'average assets, and the margin and the assets move separately and for '
              'different reasons.'))

    # the 10-09-2026 research pass: what it corroborated and what it left unchanged
    d['research_pass'] = C.RESEARCH_PASS_10_09_2026

    # THE STANDARD STAMP IS READ, NOT TYPED [added 13-09-2026]. engine/campaign_queue.py
    # reads `standard_version` to decide whether a study is built to the LIVE standard, and a
    # study that carries none reads as needing a reissue however recently it was rebuilt.
    # Measured on 13-09-2026: of 24 studies, TWO were stamped at the live 2026.09.10, four at
    # a superseded standard and EIGHTEEN carried no stamp at all -- so the campaign queue
    # listed eight names as outstanding that had just been reissued. Read from the protocol
    # rather than typed, so running a study is what stamps it.
    import research_protocol as _RP_STD
    d['standard_version'] = _RP_STD.STANDARD_VERSION

    p = os.path.join(HERE, 'study_numbers.json')
    json.dump(d, open(p, 'w'), indent=1, default=float)
    print('written %s' % p)
    print('central %.4f  spot %.2f  gap %+.1f%%  bear %.4f  full %.4f'
          % (C.CENTRAL, C.SPOT, 100 * (C.CENTRAL / C.SPOT - 1), C.BEAR, C.FULL))


if __name__ == '__main__':
    main()
