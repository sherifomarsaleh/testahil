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
            erp=C.ERP, beta=C.BETA, ke=C.KE0, ke_rating_basis=C.KE_RATING,
            ke_double_counted_retired=C.KE_DOUBLE,
            ke_terminal=C.KE_TERM, ke_terminal_construction='same_beta',
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
        register={k: dict(value=(v.value if not isinstance(v.value, (list, dict)) else v.value),
                          source=v.source, date=v.date, tier=v.tier)
                  for k, v in C.REG.items()},
    )
    p = os.path.join(HERE, 'study_numbers.json')
    json.dump(d, open(p, 'w'), indent=1, default=float)
    print('written %s' % p)
    print('central %.4f  spot %.2f  gap %+.1f%%  bear %.4f  full %.4f'
          % (C.CENTRAL, C.SPOT, 100 * (C.CENTRAL / C.SPOT - 1), C.BEAR, C.FULL))


if __name__ == '__main__':
    main()
