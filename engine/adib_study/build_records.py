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
    _MP = json.load(open(os.path.join(HERE, '..', 'macro_paths', 'EG.json'),
                        encoding='utf-8'))
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

    # THE MECHANISM, NAMED FROM THE CLOSED LIST [R-ANCHOR-01 AMENDED 13-09-2026].
    # The note above has said since 10-09-2026 what is happening and the gate could not
    # read it: the six mechanisms on the list were all industrial and none of them
    # describes a policy cycle turning, so this study's forecast was undeclared in the
    # only sense the rule cares about. NOTHING HERE IS NEW ARITHMETIC — the disclosure is
    # the sweep's own F05 and the like-for-like is this file's own two committed margins.
    _F05 = next(f for f in json.load(open(os.path.join(HERE, 'sweep_register.json'),
                                          encoding='utf-8'))['findings']
                if f['fid'] == 'F05')
    _nim_fy25 = d['base_year_observed_ratios']['nim']
    d['forecast_anchor']['mechanism'] = dict(
        name='administered_rate_cycle_down',
        disclosure=('%s — %s. The published overnight deposit rate glides 19.00%% to '
                    '12.00%% over the forecast window and the house Egyptian macro path '
                    'engine/macro_paths/EG.json carries it; the asset side reprices at a '
                    'beta of about 0.75 and the deposit side at about 0.80 of a slower '
                    'clock, which is what compresses the spread. Registered in this '
                    "study's own sweep as %s, %s, %s."
                    % (_F05['source_name'], _F05['headline'], _F05['fid'],
                       _F05['source_type'], _F05['source_date'])),
        like_for_like=dict(
            measures=('net interest margin on average total assets — the realised spread '
                      'itself, which is what the mechanism claims moves, computed by this '
                      "study's own code from the bank's own filed statements in both "
                      'periods'),
            period_a='FY2025, audited',
            value_a=_nim_fy25,
            period_b='H1-2026, reviewed, annualised',
            value_b=_nim0,
            # a LOWER margin is the direction that makes the forecast rate fall, so a
            # higher value is NOT the bad direction here
            higher_is_worse=False,
            note=('the turn has already reached this bank: the spread ran %.3f%% across '
                  'the audited year and %.3f%% in the reviewed half, a fall of %.2f '
                  'points BEFORE any of the forecast cuts. Had it widened into the latest '
                  'half the mechanism would be contradicted by the filings and this record '
                  'would be refused.'
                  % (100 * _nim_fy25, 100 * _nim0, 100 * (_nim_fy25 - _nim0))),
        ))

    # ---- 5. THE NO-BRIDGE DECLARATION [R-BRIDGE-01 CLAUSE FIVE, 13-09-2026].
    # check_bridge.py refused this study for carrying no bridge_record, and it was RIGHT
    # to refuse it: an absent record and a breaching one read identically [R-ENF-04]. The
    # study owes no bridge — every lens below lands on equity per share directly and there
    # is no enterprise value anywhere in this file — but SILENCE IS NOT A DECLARATION, so
    # the fact is committed in a shape a gate can read and be held to.
    _F16 = next(f for f in json.load(open(os.path.join(HERE, 'sweep_register.json'),
                                          encoding='utf-8'))['findings']
                if f['fid'] == 'F16')
    d['equity_direct_declaration'] = dict(
        declared_on='2026-09-13',
        no_enterprise_value=True,
        why=('a bank is valued on what reaches the shareholder [L-111]. Deposits are this '
             'business\'s raw material, not its financing, so there is no enterprise value '
             'to bridge from: subtracting a deposit book as though it were debt is '
             'meaningless. This study computes no enterprise value, no net debt and no '
             'WACC at any point, and its cost-of-capital record says so in terms '
             '(no_wacc_reason).'),
        lenses=sorted(d['lenses']),
        primary_lens='dividend_discount',
        lenses_note=('all seven produce a figure PER SHARE directly: the three '
                     'present-value reads discount a flow to equity and divide by shares, '
                     'the relative read multiplies book value and earnings per share, and '
                     'the book, book-floor and normalised reads are per-share by '
                     'construction. None of them passes through an enterprise value.'),
        balance_sheet_date='2026-06-30',
        latest_disclosed_date='2026-06-30',
        latest_disclosed_source=('%s (%s, %s, %s) — the latest disclosure in existence at '
                                 'the sweep date, established by this study\'s own Step 2A '
                                 'register rather than asserted. %s'
                                 % (_F16['source_name'], _F16['fid'], _F16['source_type'],
                                    _F16['source_date'], _F16['headline'])),
        equity_value=C.DDM['equity'],
        shares_mn=C.SHARES,
        per_share=d['central'],
        arithmetic=('EGP %.3f million of equity value over %.0f million shares = EGP %.4f '
                    'a share, which is the figure this study publishes. The sheet, the '
                    'register and this division are the three parts of [R-BRIDGE-01] that '
                    'do NOT fall away with the enterprise value.'
                    % (C.DDM['equity'], C.SHARES, d['central'])),
    )

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

    # ---- 5. THE MACRO RECORD, WHICH IS COMMITTED IN ORDER TO FAIL HONESTLY ----------
    # Added 13-09-2026. check_macro_coherence has been RED on this study reading "ADIB
    # carries no macro record" -- an ABSENCE, which [R-ENF-04] holds exactly as a breach and
    # which tells a reader nothing about what is actually wrong. Writing the record does not
    # make the gate green and is not meant to: it makes it fail for the REASON THE PRINCIPAL
    # RULED ON rather than for a missing file.
    #
    # WHAT THE RECORD SAYS ABOUT ITSELF. The explicit window ends FY2030 with net financing
    # to customers growing 12.0% and hands to a 7.00% terminal -- five points apart where
    # [R-MACRO-01] allows two, "or the terminal capitalises a growth rate the model never
    # reached and takes most of the value with it". That is a real breach and it is declared
    # here rather than argued away.
    #
    # AND IT IS OPEN BY DECISION, NOT BY OVERSIGHT. Modelling the taper explicitly was built,
    # measured and reverted: it moves the central from EGP 44.4610 to EGP 41.8291 and the gap
    # to the latest known price from -14.6% to -19.6%. The principal was shown the number, the
    # direction and the reason the gate exists, and ruled "do not extend horizon beyond 5
    # years". Recorded in adib_study/HORIZON_RULING_10-09-2026.md; the attribution was later
    # questioned and has been confirmed from the session record. THE FAILURE STANDS IN THE
    # OPEN: it cannot go on the outstanding ratchet, because that list may only ever shorten.
    _infl = d['inputs']['inflation_path']['value']
    _fin = d['inputs']['financing_growth']['value']
    _adm = d['inputs']['admin_growth']['value']
    d['macro_record'] = dict(
        market='EG',
        path_as_of=_MP.get('as_of') if isinstance(_MP, dict) else None,
        explicit_years=[x['year'] for x in _P],
        inflation_inputs=[
            dict(key='inflation_path (forecast years)', mapping='calendar',
                 first_year=_P[0]['year'], values=list(_infl),
                 note='the house calendar ladder, read live from engine/macro_paths/EG.json '
                      'rather than typed.'),
        ],
        growth_lines=[
            # ADMIN COST GROWTH IS NOT AN INFLATION VIEW, AND DECLARING IT AS ONE WAS MY
            # ERROR [corrected 13-09-2026]. It was first written into inflation_inputs on
            # a 'calendar' mapping, which asserts the array IS the house ladder -- and the
            # gate correctly refused it: 34.0% against a ladder of 16.0% in year one. The
            # gate's own words are the right ones: if the mapping is right the array was
            # typed, and if the array is right the mapping is not what the study does.
            #
            # The array is right. This is a cost-to-income path on a bank still adding
            # branches, systems and people, running ABOVE prices in every forecast year
            # and converging toward them; it is a business decision about operating
            # leverage, not a claim about Egyptian inflation.
            dict(name='administrative cost growth', years=[x['year'] for x in _P],
                 nominal=list(_adm),
                 real=float((1.0 + _adm[-1]) / (1.0 + _infl[-1]) - 1.0),
                 exempt_reason=(
                     'an operating-cost path, not a price-linked line. It runs above the '
                     'house ladder in every year (%s against %s) and converges toward it, '
                     'which is a statement about this bank\'s build-out and its operating '
                     'leverage rather than about inflation. Registered so a reader can see '
                     'the excess and disagree with it, rather than finding it inside a '
                     'cost line.'
                     % (', '.join('%.1f%%' % (100 * x) for x in _adm),
                        ', '.join('%.1f%%' % (100 * x) for x in _infl)))),
            dict(name='net financing to customers', years=[x['year'] for x in _P],
                 nominal=list(_fin[-len(_P):]) if len(_fin) >= len(_P) else list(_fin),
                 # THE REAL RATE IS COMPUTED FROM THE LINE'S OWN HORIZON YEAR, not defaulted
                 # to zero. Zero would be a claim -- that this book grows with prices and
                 # nothing else -- and it is the opposite of what this study argues.
                 real=float((1.0 + _fin[-1]) / (1.0 + _infl[-1]) - 1.0),
                 # EXEMPT BY NAME, AND THE EXEMPTION DOES NOT COVER THE THING THAT IS WRONG.
                 # GrowthLine stores ONE real rate, and this line's real growth is not one
                 # number: it falls from 27.6% in 2026 to 4.7% in 2030 as deepening and share
                 # gain run out. That is a balance-sheet trajectory, not a price-linked line,
                 # and forcing it to a constant would make the record say something false in
                 # order to be checkable.
                 #
                 # WHAT THIS DOES NOT BUY. The exemption reaches clause 1 only -- whether each
                 # nominal rate recomputes from inflation and a stated real. It does NOT reach
                 # the horizon-to-terminal window, which is the clause the principal ruled on
                 # and which this record still declares broken: 12.0% into 7.00%, five points
                 # where two are allowed. An exemption used to silence that would be the
                 # widening this book forbids.
                 exempt_reason=(
                     'a balance-sheet trajectory rather than a price-linked line. Real growth '
                     'is not constant across the window -- %s -- because it is credit '
                     'deepening plus share gain, both of which run out; a single stated real '
                     'rate cannot describe it without asserting something the model does not '
                     'do. The horizon-to-terminal window is NOT exempted and is declared '
                     'broken in this record\'s own note.'
                     % ', '.join('%d %.1f%%' % (y, 100 * ((1 + n) / (1 + i) - 1))
                                 for y, n, i in zip([x['year'] for x in _P], _fin, _infl))),
                 basis='credit deepening plus share gain, in an economy whose private credit '
                       'is about a quarter of GDP. The study\'s own note has share drift '
                       'reaching zero by FY2030, so what remains at the horizon is deepening: '
                       'nominal %.1f%% against a ladder of %.1f%% is %.2f%% REAL, and that '
                       'real growth is precisely what the 7.00%% terminal switches off in one '
                       'step.'
                       % (100 * _fin[-1], 100 * _infl[-1],
                          100 * ((1.0 + _fin[-1]) / (1.0 + _infl[-1]) - 1.0))),
        ],
        growth_at_horizon_end=float(_fin[-1]),
        terminal=dict(g_nominal=float(d['inputs']['terminal_growth']['value']),
                      real=0.0,
                      rf=float(d['inputs']['rf_terminal']['value']),
                      inflation_in_rf=float(d['inputs']['terminal_growth']['value'])),
        note=('THIS RECORD DECLARES A BREACH RATHER THAN CLEARING ONE. Growth at the horizon '
              'end is %.2f%% against a terminal of %.2f%% -- %.2f points, where the rule '
              'allows two. It is open BY THE PRINCIPAL\'S RULING of 10-09-2026 ("do not '
              'extend horizon beyond 5 years"), given after being shown that closing it moves '
              'the central from EGP 44.4610 to EGP 41.8291. WHAT WOULD SETTLE IT PROPERLY is '
              'the terminal itself: 7.00%% is terminal inflation at ZERO real growth, i.e. the '
              'bank stops taking share AND stops participating in credit deepening the moment '
              'the window closes, in an economy growing about 4.5%% real. A terminal real '
              'growth near 3%% would put nominal growth at about 10.2%% and clear the window '
              'with no extension at all -- and would RAISE the answer rather than lower it, '
              'which is exactly why it must be argued from evidence about this bank and this '
              'credit market or not at all. It is NOT a route back to 44.46.'
              % (100 * _fin[-1],
                 100 * d['inputs']['terminal_growth']['value'],
                 100 * (_fin[-1] - d['inputs']['terminal_growth']['value']))),
    )

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
