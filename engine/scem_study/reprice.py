"""Price every critique finding BEFORE judging it.

A compact re-implementation of the delivered model, parameterised so each proposed
correction can be applied in isolation and in combination. Every number quoted in the
critique-response table comes from here.
"""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
IN = {k: v['value'] for k, v in D['inputs'].items()}

BASE = dict(
    rf=0.2231, sov=0.0340, erp=0.0941, beta=1.00, kd=0.2150, tax=0.225,
    debt=36.8, shares=260.812477, spot=79.00,
    rf_term=0.105, erp_term=0.070, kd_term=0.150, wd_term=0.20, g=0.05,
    kd_path=[0.2150, 0.1950, 0.1800, 0.1680, 0.1600],
    rev=list(D['forecast']['revenue']),
    mgn=[0.305, 0.285, 0.270, 0.265, 0.260],
    dnap=[0.046, 0.045, 0.044, 0.043, 0.042],
    cxp=[0.050, 0.048, 0.047, 0.046, 0.045],
    wcp=0.080, rev25=9090.0,
    cap_mt=3.80, repl=130.0, fx=49.8, ev_t=95.0,
    net_cash=5307.05, nci=0.0,
    ev_ebitda=5.0, pe=7.0, norm_mgn=0.265, dna25=418.14,
    cash_yield_norm=0.15,
    w=(0.45, 0.20, 0.20, 0.15),
    relever=False, midyear=False, stub=0.0,
    reinv_consistent=False, norm_cash_at_face=False,
)


def run(**kw):
    p = dict(BASE); p.update(kw)
    tax = p['tax']
    # ---- cost of capital, built exactly as the workbook builds it -----------
    rf_star = p['rf'] - p['sov']
    ke = rf_star + p['beta'] * p['erp']
    kd_at = p['kd'] * (1 - tax)
    mcap = p['spot'] * p['shares']
    wd = p['debt'] / (p['debt'] + mcap)
    wacc_e = (1 - wd) * ke + wd * kd_at
    beta_t = p['beta']
    if p['relever']:                       # Hamada re-lever to the terminal structure
        de = p['wd_term'] / (1 - p['wd_term'])
        beta_t = p['beta'] * (1 + (1 - tax) * de)
    ke_t = p['rf_term'] + beta_t * p['erp_term']
    wacc_t = (1 - p['wd_term']) * ke_t + p['wd_term'] * p['kd_term'] * (1 - tax)
    kdp = p['kd_path']
    glide = [(kdp[0] - kdp[i]) / (kdp[0] - kdp[-1]) for i in range(5)]
    fwd = [wacc_e - (wacc_e - wacc_t) * g for g in glide]
    df, acc = [], 1.0
    for i in range(5):
        if p['midyear']:
            half = acc / (1 + fwd[i]) ** 0.5
            acc /= (1 + fwd[i])
            df.append(half * (1 + fwd[i]) ** p['stub'])
        else:
            acc /= (1 + fwd[i])
            df.append(acc * (1 + fwd[i]) ** p['stub'])
    # ---- waterfall ----------------------------------------------------------
    rev = p['rev']
    ebitda = [rev[i] * p['mgn'][i] for i in range(5)]
    dna = [rev[i] * p['dnap'][i] for i in range(5)]
    ebit = [ebitda[i] - dna[i] for i in range(5)]
    nopat = [ebit[i] * (1 - tax) for i in range(5)]
    capex = [rev[i] * p['cxp'][i] for i in range(5)]
    prev = [p['rev25']] + rev[:-1]
    dwc = [(rev[i] - prev[i]) * p['wcp'] for i in range(5)]
    ic_repl = p['cap_mt'] * 1e6 * p['repl'] * p['fx'] / 1e6
    if p['reinv_consistent']:
        # Growth in the explicit window must be bought at the SAME return the terminal
        # pays for it: net reinvestment = growth in NOPAT / ROIC_replacement.
        roic_r = nopat[-1] * (1 + p['g']) / ic_repl
        prev_n = nopat[0] / (1 + (rev[0] / p['rev25'] - 1))
        fcff = []
        for i in range(5):
            base_n = prev_n if i == 0 else nopat[i - 1]
            dnopat = max(nopat[i] - base_n, 0.0)
            net_reinv = dnopat / roic_r
            fcff.append(nopat[i] - net_reinv)
    else:
        fcff = [nopat[i] + dna[i] - capex[i] - dwc[i] for i in range(5)]
    pv = [fcff[i] * df[i] for i in range(5)]
    sum_pv = float(np.sum(pv))
    roic_t = nopat[-1] * (1 + p['g']) / ic_repl
    rr = p['g'] / roic_t
    tv = nopat[-1] * (1 + p['g']) * (1 - rr) / (wacc_t - p['g'])
    pv_tv = tv * df[-1]
    ev = sum_pv + pv_tv
    eq = ev + p['net_cash'] - p['nci']
    fv_dcf = eq / p['shares']
    # ---- other lenses -------------------------------------------------------
    eb_norm = p['rev25'] * p['norm_mgn']
    fv_rel = (eb_norm * p['ev_ebitda'] + p['net_cash'] - p['nci']) / p['shares']
    nopat_norm = (eb_norm - p['dna25']) * (1 - tax)
    if p['norm_cash_at_face']:
        fv_norm = (nopat_norm * p['pe'] + p['net_cash'] - p['nci']) / p['shares']
    else:
        earn = nopat_norm + p['net_cash'] * p['cash_yield_norm'] * (1 - tax)
        fv_norm = (earn * p['pe'] - p['nci']) / p['shares']
    ev_asset = p['ev_t'] * p['cap_mt'] * 1e6 * p['fx'] / 1e6
    fv_asset = (ev_asset + p['net_cash'] - p['nci']) / p['shares']
    w = p['w']
    central = w[0] * fv_dcf + w[1] * fv_rel + w[2] * fv_norm + w[3] * fv_asset
    return dict(dcf=fv_dcf, rel=fv_rel, norm=fv_norm, asset=fv_asset, central=central,
                ev=ev, tv_share=pv_tv / ev, wacc_e=wacc_e, wacc_t=wacc_t, ke=ke,
                sum_pv=sum_pv, pv_tv=pv_tv, roic_t=roic_t, rr=rr, spot=p['spot'])


B = run()
C0 = B['central']


def price(label, **kw):
    r = run(**kw)
    d = r['central'] - C0
    return dict(label=label, central=r['central'], dcf=r['dcf'], delta_egp=d,
                delta_pct=d / C0, r=r)


if __name__ == '__main__':
    print(f"BASE central {C0:.2f} | dcf {B['dcf']:.2f} | rel {B['rel']:.2f} | "
          f"norm {B['norm']:.2f} | asset {B['asset']:.2f} | wacc_e {B['wacc_e']:.4f} "
          f"| wacc_t {B['wacc_t']:.4f} | tv% {B['tv_share']:.3f}")
    CASES = [
        ('C1  net cash 5,307 -> 3,813 (reported FY2025)', dict(net_cash=3813.0)),
        ('C2  net cash on the implied distribution (-1,865)', dict(net_cash=3442.0)),
        ('C3  net cash 5,802 (Q1-2026 filing)', dict(net_cash=5765.2)),
        ('C4  spot 79.00 -> 81.10', dict(spot=81.10)),
        ('C5  effective tax 32% on the P&L closure only', dict()),
        ('C6  consistent reinvestment rule across both windows', dict(reinv_consistent=True)),
        ('C7  beta 1.00 -> 0.837 (lead-lag point estimate)', dict(beta=0.837)),
        ('C8  beta 1.00 -> 0.485 (raw regression)', dict(beta=0.485)),
        ('C9  Hamada re-lever terminal beta', dict(relever=True)),
        ('C10 ERP rating basis 13.94% + sov 6.37%', dict(erp=0.1394, sov=0.0637)),
        ('C11 ERP 14.87% (Jul-2026 vintage), sov unchanged', dict(erp=0.1487)),
        ('C12 no netting: Ke = rf + ERP (Gemini research)', dict(sov=0.0)),
        ('C13 rf 22.31% -> 22.98%', dict(rf=0.2298)),
        ('C14 rf 22.31% -> 21.29% (Apr-26 observed)', dict(rf=0.2129)),
        ('C15 terminal rf on the 7% operative target (12.5%), g 7%',
         dict(rf_term=0.125, g=0.07)),
        ('C16 terminal rf 12.5%, g unchanged at 5%', dict(rf_term=0.125)),
        ('C17 replacement cost on CLINKER capacity 2.57Mt',
         dict(cap_mt=2.57)),
        ('C18 capacity 2.9Mt (company website figure)', dict(cap_mt=2.9)),
        ('C19 NCI deduction 2,008 (Gemini research 15%)', dict(nci=2008.0)),
        ('C20 NCI deduction 120 (profit-share evidence)', dict(nci=120.0)),
        ('C21 normalised lens: cash at FACE, not capitalised',
         dict(norm_cash_at_face=True)),
        ('C22 mid-year discounting', dict(midyear=True)),
        ('C23 mid-year + 7-month stub', dict(midyear=True, stub=7 / 12)),
        ('C24 FY2026 margin capped at the FY2025 peak (28.0%)',
         dict(mgn=[0.280, 0.275, 0.270, 0.265, 0.260])),
        ('C25 peer multiple 3.48x instead of 5.0x', dict(ev_ebitda=3.48)),
        ('C26 asset lens dropped, reweighted 53/23/24',
         dict(w=(0.529, 0.235, 0.236, 0.0))),
        ('C27 normalised revenue base -15% (peak price stripped)',
         dict(rev25=9090.0 * 0.85)),
    ]
    print(f"\n{'finding':56s}{'central':>9s}{'EGP':>9s}{'%':>9s}")
    for lab, kw in CASES:
        p = price(lab, **kw)
        print(f"{lab:56s}{p['central']:9.2f}{p['delta_egp']:+9.2f}{p['delta_pct']:+9.2%}")
