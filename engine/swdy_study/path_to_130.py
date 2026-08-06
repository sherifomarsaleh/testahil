"""SWDY — what does it take to reach EGP 130 per share?

Two distinct questions, both answered from the same model:

A. TIME. If the base forecast simply plays out, intrinsic value compounds as the
   remaining cash flows are discounted over a shorter distance and net debt is
   paid down. The model is re-anchored at each future year-end to read the value
   off it, and the implied return from today's price is computed.

B. CONDITIONS. If instead the question is what would have to be TRUE for the
   valuation to be 130 TODAY, each driver is solved by bisection, holding the
   others at base — and the ones that cannot reach 130 within any defensible
   range are reported as unreachable rather than extrapolated.
"""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
W, DCF, F = D['wacc'], D['dcf'], D['fcst']
IN = {k: v['value'] for k, v in D['inputs'].items()}
SH, SPOT = D['meta']['shares_mn'], D['meta']['spot']
TAX = IN['tax_eff']
TARGET = 130.0
ND0, ASSOC, NCI_SH = DCF['nd'], DCF['assoc'], DCF['nci_share']
G, ROIC_T = IN['g_term'], DCF['roic_term']
KE_EXP, KE_TERM = W['ke_exp'], W['ke_term']
WD_EXP, WD_TERM = W['wd_exp'], IN['wd_term']
NWC_FY25 = IN['nwc_pct'] * IN['rev_fy25']
GLIDE = W['glide_frac']
FCFF, DF, TV = F['fcff'], F['df'], DCF['tv']

print('=' * 94)
print(f"Base DCF EGP {DCF['ps']:.2f} · market price EGP {SPOT:.2f} · target EGP {TARGET:.2f}")
print('=' * 94)

# ============================ A. TIME =========================================
# Value at year-end k = the remaining cash flows and the terminal value, each
# discounted only the distance from k, less net debt as it then stands.
ND = [ND0] + F['net_debt']
print("\nA. IF THE BASE FORECAST SIMPLY PLAYS OUT — value re-anchored each year-end")
print(f"   {'as at':>10} {'EV':>10} {'net debt':>10} {'equity/sh':>10} {'cum. divs':>10} "
      f"{'total value':>12}")
rows = []
cum_div = 0.0
for k in range(0, 6):
    dfk = DF[k - 1] if k > 0 else 1.0
    ev = sum(FCFF[i] * DF[i] / dfk for i in range(k, 5)) + TV * DF[4] / dfk
    eq = ((ev - ND[k] + ASSOC) * (1 - NCI_SH)) / SH
    if k > 0:
        cum_div += 0.25 * F['np_attr'][k - 1] * (1 - 0) / SH   # 25% payout, as modelled
    rows.append((k, ev, ND[k], eq, cum_div, eq + cum_div))
    lbl = 'today' if k == 0 else f'+{k}y (FY{25+k})'
    print(f"   {lbl:>10} {ev:10,.0f} {ND[k]:10,.0f} {eq:10.2f} {cum_div:10.2f} "
          f"{eq + cum_div:12.2f}")

# when does equity value alone cross the target?
cross = None
for k in range(1, 6):
    a, b = rows[k - 1][3], rows[k][3]
    if a < TARGET <= b:
        frac = (TARGET - a) / (b - a)
        cross = (k - 1) + frac
        break
cross_tot = None
for k in range(1, 6):
    a, b = rows[k - 1][5], rows[k][5]
    if a < TARGET <= b:
        cross_tot = (k - 1) + (TARGET - a) / (b - a)
        break
print(f"\n   Intrinsic value alone reaches EGP {TARGET:.0f} after "
      f"{cross:.1f} years" if cross else "\n   Intrinsic value does not reach the target within the forecast")
if cross_tot:
    print(f"   Including dividends received along the way, after {cross_tot:.1f} years")

# implied return from TODAY'S PRICE if the model is right
for k in (3, 5):
    tot = rows[k][3] + rows[k][4]
    irr = (tot / SPOT) ** (1 / k) - 1
    print(f"   Buying at the market price of {SPOT:.2f} and holding {k} years to a value of "
          f"{tot:.2f} is a {irr:.1%} annual return")

# ============================ B. CONDITIONS ===================================
def value(margin_shift=0.0, fx_mult=1.0, rate_shift=0.0, g=G, nwc=IN['nwc_pct'],
          fgn_boost=0.0):
    """Re-run the DCF from the drivers. Reproduces base when all defaults hold."""
    rev = [F['rev'][i] * fx_mult * (1 + fgn_boost) ** (i + 1) for i in range(5)]
    ebitda = [(F['ebitda_margin'][i] + margin_shift) * rev[i] for i in range(5)]
    dna = [IN['dna_pct'] * r for r in rev]
    ebit = [ebitda[i] - dna[i] for i in range(5)]
    nopat = [e * (1 - TAX) for e in ebit]
    capex = [IN['capex_pct'][i] * rev[i] for i in range(5)]
    nwc_l = [nwc * r for r in rev]
    dnwc = [nwc_l[0] - nwc * IN['rev_fy25']] + [nwc_l[i] - nwc_l[i - 1] for i in range(1, 5)]
    fcff = [nopat[i] + dna[i] - capex[i] - dnwc[i] for i in range(5)]
    we = (1 - WD_EXP) * (KE_EXP + rate_shift) + WD_EXP * (IN['kd_path'][0] + rate_shift) * (1 - TAX)
    wt = (1 - WD_TERM) * (KE_TERM + rate_shift) + WD_TERM * (IN['kd_term'] + rate_shift) * (1 - TAX)
    fwd = [we - (we - wt) * f for f in GLIDE]
    df, c = [], 1.0
    for w in fwd:
        c /= (1 + w); df.append(c)
    ppe, p = [], F['ppe'][0] - (F['capex'][0] - F['dna'][0])
    for i in range(5):
        p += capex[i] - dna[i]; ppe.append(p)
    roic = nopat[-1] / (nwc_l[-1] + ppe[-1] + IN['intang_fy24'])
    rr = min(g / roic, 0.95)
    tv = nopat[-1] * (1 + g) * (1 - rr) / max(wt - g, 0.015)
    ev = sum(fcff[i] * df[i] for i in range(5)) + tv * df[-1]
    return ((ev - ND0 + ASSOC) * (1 - NCI_SH)) / SH

chk = value()
assert abs(chk - DCF['ps']) < 0.60, f'driver rebuild does not reproduce base: {chk} vs {DCF["ps"]}'
print(f"\nB. WHAT WOULD HAVE TO BE TRUE FOR 130 TODAY  (driver rebuild reproduces base "
      f"at {chk:.2f} vs published {DCF['ps']:.2f})")

def solve(fn, lo, hi, label, unit, plausible):
    """Bisect for the driver level that reaches the target."""
    flo, fhi = fn(lo), fn(hi)
    if not (min(flo, fhi) <= TARGET <= max(flo, fhi)):
        print(f"   {label:<42} UNREACHABLE across [{lo}{unit}, {hi}{unit}] "
              f"-> value spans {min(flo,fhi):.0f}–{max(flo,fhi):.0f}")
        return None
    for _ in range(80):
        mid = (lo + hi) / 2
        if (fn(mid) - TARGET) * (flo - TARGET) > 0:
            lo, flo = mid, fn(mid)
        else:
            hi = mid
    ans = (lo + hi) / 2
    verdict = 'within a defensible range' if plausible(ans) else 'OUTSIDE any defensible range'
    print(f"   {label:<42} needs {ans:+.2%}{unit}  ({verdict})" if unit == ''
          else f"   {label:<42} needs {ans:.3f}{unit}  ({verdict})")
    return ans

solve(lambda x: value(rate_shift=x), 0.02, -0.12, 'Parallel fall in the cost of capital', '',
      lambda a: a > -0.06)
solve(lambda x: value(margin_shift=x), -0.02, 0.12, 'EBITDA margin uplift (all years)', '',
      lambda a: a < 0.03)
solve(lambda x: value(fx_mult=x), 0.9, 2.2, 'Exchange-rate path multiplier', 'x',
      lambda a: a < 1.35)
solve(lambda x: value(g=x), 0.02, 0.12, 'Terminal growth', '',
      lambda a: a < 0.075)
solve(lambda x: value(nwc=x), 0.26, 0.02, 'Working capital as a share of revenue', '',
      lambda a: a > 0.14)
solve(lambda x: value(fgn_boost=x), 0.0, 0.15, 'Extra annual foreign revenue growth', '',
      lambda a: a < 0.05)

# combination: the plausible-but-good case
print("\n   A COMBINATION, each leg individually defensible:")
combo = value(rate_shift=-0.02, margin_shift=0.005, fx_mult=1.06)
print(f"     cost of capital -200bp, EBITDA margin +0.5pp, currency path 6% weaker "
      f"-> EGP {combo:.2f}")
combo2 = value(rate_shift=-0.025, margin_shift=0.0075, fx_mult=1.08, g=0.055)
print(f"     -250bp, +0.75pp, 8% weaker currency, terminal growth 5.5% "
      f"-> EGP {combo2:.2f}")

out = dict(target=TARGET, base=DCF['ps'], spot=SPOT,
           rollforward=[dict(year=k, ev=e, nd=n, equity_ps=q, cum_div=d, total=t)
                        for k, e, n, q, d, t in rows],
           years_to_target=cross, years_to_target_incl_div=cross_tot,
           combo_200bp=combo, combo_250bp=combo2)
json.dump(out, open(os.path.join(HERE, 'path_to_130.json'), 'w'), indent=1, default=float)
print("\nwrote path_to_130.json")
