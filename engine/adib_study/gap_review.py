#!/usr/bin/env python3
"""ADIB-Egypt — the arithmetic behind GAP_REVIEW. [R-GAP-01]

The central lands materially BELOW the latest known price. The rule does not say the
answer must change; it says the answer is audited before it ships. This computes every
number the review quotes, so no figure in that document is typed.
"""
import sys, os, math, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import compute as C  # noqa: E402


def central_with(**over):
    """Re-strike the central under an override. Restores every global it touches."""
    keep = dict(P=C.P, KE_PATH=C.KE_PATH, KE_TERM=C.KE_TERM, DF=C.DF, G_TERM=C.G_TERM)
    if 'rf' in over:
        d = over['rf'] - C.RF
        C.KE_PATH = [k + d for k in keep['KE_PATH']]
        C.KE_TERM = keep['KE_TERM'] + d
        C.DF = C.discount_factors(C.KE_PATH)
    if 'ke0' in over:
        k0, kt = over['ke0'], C.KE_TERM
        n = len(C.YEARS)
        C.KE_PATH = [k0 + (kt - k0) * (i + 1) / (n + 1) for i in range(n)]
        C.DF = C.discount_factors(C.KE_PATH)
    proj_kw = {k: v for k, v in over.items() if k in ('cor', 'yield_path', 'cof_path',
                                                      'fin_growth')}
    if proj_kw:
        C.P = C.project(**proj_kw)
    v = C.ddm()['per_share']          # the PRIMARY [R-LENS-03], never a blend
    for k, val in keep.items():
        setattr(C, k, val)
    return v


def solve_rf_for_spot():
    lo, hi = 0.05, 0.30
    for _ in range(80):
        mid = (lo + hi) / 2
        if central_with(rf=mid) > C.SPOT:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def solve_ke_for_spot():
    lo, hi = 0.10, 0.45
    for _ in range(80):
        mid = (lo + hi) / 2
        if central_with(ke0=mid) > C.SPOT:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main():
    out = {}
    out['central'] = C.CENTRAL
    out['spot'] = C.SPOT
    out['gap'] = C.CENTRAL / C.SPOT - 1

    # 1. the base-year question: what if the June half's near-nil loss charge holds?
    h1_cor = C.H1OBS['cost_of_risk']
    out['h1_cost_of_risk'] = h1_cor
    out['central_if_h1_cor_holds_2026'] = central_with(
        cor=[h1_cor] + list(C.COST_OF_RISK[1:]))
    out['central_if_h1_cor_holds_throughout'] = central_with(cor=[h1_cor] * 5)

    # 2. the discount-rate question
    out['rf_held'] = C.RF
    out['rf_apr_may_2026_market'] = 0.2129
    out['central_at_rf_2129'] = central_with(rf=0.2129)
    out['central_at_rf_1929'] = central_with(rf=0.1929)   # = -200bp on the held rate
    out['rf_that_reaches_spot'] = solve_rf_for_spot()
    out['ke_that_reaches_spot'] = solve_ke_for_spot()
    bv_jun = C.H1['equity_parent'] / C.SHARES
    out['market_pb_on_jun26_book'] = C.SPOT / bv_jun
    out['market_implied_ke_gordon'] = C.G_TERM + (C.H1OBS['roe'] - C.G_TERM) / (C.SPOT / bv_jun)

    # 3. both together
    out['central_rf2129_and_h1cor'] = central_with(rf=0.2129, cor=[h1_cor] + list(C.COST_OF_RISK[1:]))

    # 4. multiple cross-check
    out['implied_pb_2026'] = C.CENTRAL / C.P[0]['bvps']
    out['implied_pe_2026'] = C.CENTRAL / C.P[0]['eps']
    out['implied_pb_on_jun26_book'] = C.CENTRAL / bv_jun
    out['implied_pe_trailing_fy25'] = C.CENTRAL / (C.FY25['np_parent'] / C.SHARES)
    out['gordon_pb_at_terminal'] = ((C.P[-1]['roe'] - C.G_TERM) / (C.KE_TERM - C.G_TERM))
    out['gordon_pb_at_ke0_on_fy26_roe'] = ((C.P[0]['roe'] - C.G_TERM) / (C.KE_PATH[0] - C.G_TERM))

    # 5. balance-sheet check: is anything counted twice?
    out['ri_book0'] = C.RI['book0']
    out['ri_capital_added'] = C.CAP_INCREASE_26
    out['fy26_fcfe'] = C.P[0]['fcfe']
    out['fy26_dividend'] = C.P[0]['dividend']
    out['equity_assets_path'] = [r['equity_assets'] for r in C.P]

    # 6. terminal coherence
    out['terminal_growth'] = C.G_TERM
    out['terminal_rf'] = C.RF_TERM
    out['terminal_inflation'] = C.EG.terminal_inflation
    out['terminal_ke'] = C.KE_TERM
    out['terminal_roe'] = C.P[-1]['roe']
    out['tv_share_ddm'] = C.DDM['pv_tv'] / C.DDM['equity']
    out['tv_share_fcfe'] = C.FCFE['pv_tv'] / C.FCFE['equity']
    out['tv_share_ri'] = C.RI['pv_tv'] / C.RI['equity']

    # 7. macro coherence: ADIB growth against nominal GDP
    infl = C.INFL
    real_gdp = 0.045
    nom = [(1 + i) * (1 + real_gdp) - 1 for i in infl]
    out['nominal_gdp_growth'] = nom
    out['financing_growth'] = list(C.FIN_GROWTH)
    out['growth_multiple_of_nominal_gdp'] = [g / n for g, n in zip(C.FIN_GROWTH, nom)]
    sysc = C.EG  # for the record only
    import macro as WFM  # the walk-forward's own system-credit series
    sc25 = WFM.SYSTEM_CREDIT[2025]
    share25 = C.FY25['financing'] * 1e6 / sc25
    path = []
    sc = sc25
    for i, y in enumerate(C.YEARS):
        sc *= (1 + nom[i])
        path.append(C.P[i]['financing'] * 1e6 / sc)
    out['share_of_system_credit_fy2025'] = share25
    out['share_of_system_credit_path'] = path

    # WHAT THIS ARTEFACT WAS CURRENT WITH, IN A FIELD NAMED FOR THE PURPOSE. It carried
    # `central` and `spot`, which the currency gate does not read as a declaration — those
    # are figures the review computes, not a statement of the edition it stands on. An
    # artefact that does not say what it was current WITH cannot be told from a stale one,
    # and this one went stale twice today without any gate being able to say so.
    _committed = json.load(open(os.path.join(HERE, 'study_numbers.json')))
    out['published_central'] = _committed['central']
    out['published_spot'] = _committed['spot']

    json.dump(out, open(os.path.join(HERE, 'gap_review_numbers.json'), 'w'), indent=1,
              default=float)
    for k, v in out.items():
        if isinstance(v, list):
            print('%-38s %s' % (k, ' '.join('%.4f' % x for x in v)))
        else:
            print('%-38s %.6f' % (k, v))


if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'adib_walkforward'))
    main()
