"""SWDY — isolate the valuation effect of the cost of DEBT.

Question: the blended cost of debt is 13% and will fall further as Egyptian
policy rates come down. What does that do to the DCF?

The base model already embeds a declining path (13.0% -> 10.5% terminal). This
script decomposes the effect: it re-runs the DCF holding the free cash flows
fixed (they are pre-financing by construction, so the cost of debt cannot touch
them) and moving only the cost-of-debt schedule, then contrasts that with the
same move applied to the cost of EQUITY, which carries the other ~92% of the
capital weight.
"""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
W, DCF, F = D['wacc'], D['dcf'], D['fcst']
IN = {k: v['value'] for k, v in D['inputs'].items()}
SH, SPOT = D['meta']['shares_mn'], D['meta']['spot']
TAX = IN['tax_eff']
FCFF = F['fcff']
NOPAT5 = F['nopat'][-1]
ROIC_T = DCF['roic_term']
ND, ASSOC, NCI_SH = DCF['nd'], DCF['assoc'], DCF['nci_share']
G = IN['g_term']
KE_EXP, KE_TERM = W['ke_exp'], W['ke_term']
WD_EXP, WD_TERM = W['wd_exp'], IN['wd_term']
BASE_PATH = list(IN['kd_path'])
BASE_TERM = IN['kd_term']


def value(kd_path, kd_term, ke_exp=KE_EXP, ke_term=KE_TERM,
          wd_exp=WD_EXP, wd_term=WD_TERM):
    """Full DCF -> equity per share for a given rate schedule."""
    wacc_exp = (1 - wd_exp) * ke_exp + wd_exp * kd_path[0] * (1 - TAX)
    wacc_term = (1 - wd_term) * ke_term + wd_term * kd_term * (1 - TAX)
    span = kd_path[0] - kd_path[-1]
    if abs(span) < 1e-9:                      # a flat cost-of-debt path carries no
        frac = [(i + 1) / len(kd_path)        # shape information; glide linearly
                for i in range(len(kd_path))]
    else:
        frac = [(kd_path[0] - k) / span for k in kd_path]
    fwd = [wacc_exp - (wacc_exp - wacc_term) * f for f in frac]
    df, c = [], 1.0
    for w in fwd:
        c /= (1 + w); df.append(c)
    rr = min(G / ROIC_T, 0.95)
    tv = NOPAT5 * (1 + G) * (1 - rr) / (wacc_term - G)
    ev = sum(FCFF[i] * df[i] for i in range(5)) + tv * df[-1]
    ps = ((ev - ND + ASSOC) * (1 - NCI_SH)) / SH
    return dict(ps=ps, ev=ev, wacc_exp=wacc_exp, wacc_term=wacc_term,
                tv_share=(tv * df[-1]) / ev)


base = value(BASE_PATH, BASE_TERM)
assert abs(base['ps'] - DCF['ps']) < 0.01, f"base does not reproduce: {base['ps']} vs {DCF['ps']}"
print('=' * 96)
print(f"BASE reproduces the published DCF exactly: EGP {base['ps']:.2f}  "
      f"(cost of capital {base['wacc_exp']:.2%} -> {base['wacc_term']:.2%})")
print('=' * 96)

# ---- 1. what the ALREADY-EMBEDDED decline is worth ---------------------------
flat = value([BASE_PATH[0]] * 5, BASE_PATH[0])
print("\n1. WHAT THE DECLINE ALREADY IN THE MODEL IS WORTH")
print(f"   Cost of debt held FLAT at {BASE_PATH[0]:.1%} forever : EGP {flat['ps']:6.2f}  "
      f"(terminal cost of capital {flat['wacc_term']:.2%})")
print(f"   Cost of debt declining {BASE_PATH[0]:.1%} -> {BASE_TERM:.1%} (base): EGP {base['ps']:6.2f}  "
      f"(terminal cost of capital {base['wacc_term']:.2%})")
print(f"   -> the entire embedded decline is worth EGP {base['ps'] - flat['ps']:+.2f} per share "
      f"({(base['ps']/flat['ps']-1):+.1%})")

# ---- 2. taking it further -----------------------------------------------------
print("\n2. TAKING THE COST OF DEBT FURTHER DOWN (path and terminal shifted together)")
print(f"   {'shift':>8} {'terminal Kd':>12} {'WACC exp':>10} {'WACC term':>10} {'EGP/share':>10} "
      f"{'vs base':>9}")
rows = []
for shift in (0.02, 0.01, 0.0, -0.01, -0.02, -0.03, -0.04):
    p = [max(k + shift, 0.02) for k in BASE_PATH]
    t = max(BASE_TERM + shift, 0.02)
    v = value(p, t)
    rows.append((shift, t, v))
    print(f"   {shift:+8.1%} {t:12.1%} {v['wacc_exp']:10.2%} {v['wacc_term']:10.2%} "
          f"{v['ps']:10.2f} {v['ps']-base['ps']:+9.2f}")
swing = max(r[2]['ps'] for r in rows) - min(r[2]['ps'] for r in rows)
print(f"   -> a 600bp span in the cost of debt moves the valuation EGP {swing:.2f} in total")

# ---- 3. why: the weight ---------------------------------------------------------
print("\n3. WHY THE EFFECT IS SMALL — THE DEBT WEIGHT")
print(f"   Net bank debt {ND:,.0f} against market capitalisation {D['meta']['mktcap']:,.0f}")
print(f"   -> debt carries {WD_EXP:.1%} of the capital weight in the explicit window, "
      f"equity {1-WD_EXP:.1%}")
print(f"   A 100bp fall in the cost of debt moves the explicit cost of capital by only "
      f"{WD_EXP * 0.01 * (1-TAX) * 10000:.0f}bp")
print(f"   A 100bp fall in the cost of EQUITY moves it by "
      f"{(1-WD_EXP) * 0.01 * 10000:.0f}bp — {(1-WD_EXP)/(WD_EXP*(1-TAX)):.0f}x more")

# ---- 4. the same 100bp applied to the whole rate complex --------------------------
print("\n4. THE SAME EASING APPLIED TO THE WHOLE RATE COMPLEX (equity and debt together)")
print("   Egyptian disinflation lowers the government bond yield, which is the risk-free")
print("   rate inside the cost of equity as well as the anchor for corporate borrowing.")
print(f"   {'shift':>8} {'Ke exp':>9} {'Ke term':>9} {'WACC exp':>10} {'WACC term':>10} "
      f"{'EGP/share':>10} {'vs base':>9}")
for shift in (0.01, 0.0, -0.01, -0.02, -0.03):
    p = [max(k + shift, 0.02) for k in BASE_PATH]
    t = max(BASE_TERM + shift, 0.02)
    v = value(p, t, ke_exp=KE_EXP + shift, ke_term=KE_TERM + shift)
    print(f"   {shift:+8.1%} {KE_EXP+shift:9.2%} {KE_TERM+shift:9.2%} {v['wacc_exp']:10.2%} "
          f"{v['wacc_term']:10.2%} {v['ps']:10.2f} {v['ps']-base['ps']:+9.2f}")

# ---- 5. the gross-debt-weight variant ----------------------------------------------
print("\n5. IF GROSS RATHER THAN NET DEBT WEIGHTS WERE USED")
print(f"   The study weights on NET debt ({WD_EXP:.1%}) because that is what the bridge")
print(f"   subtracts. On GROSS debt the weight would be {W['wd_gross']:.1%}, which both lowers")
print( "   the cost of capital and triples the sensitivity to the cost of debt.")
gb = value(BASE_PATH, BASE_TERM, wd_exp=W['wd_gross'])
gf = value([BASE_PATH[0]] * 5, BASE_PATH[0], wd_exp=W['wd_gross'])
gd = value([k - 0.02 for k in BASE_PATH], BASE_TERM - 0.02, wd_exp=W['wd_gross'])
print(f"   Gross-weight base                        : EGP {gb['ps']:6.2f} "
      f"({gb['ps']-base['ps']:+.2f} vs the published DCF)")
print(f"   Gross weights, cost of debt held flat    : EGP {gf['ps']:6.2f}")
print(f"   Gross weights, cost of debt 200bp lower  : EGP {gd['ps']:6.2f} "
      f"({gd['ps']-gb['ps']:+.2f})")

out = dict(base=base['ps'], kd_flat=flat['ps'],
           embedded_decline_worth=base['ps'] - flat['ps'],
           shifts={f"{s:+.2%}": v['ps'] for s, t, v in rows},
           span_600bp=swing, wd_exp=WD_EXP, wd_gross=W['wd_gross'],
           gross_weight_base=gb['ps'])
json.dump(out, open(os.path.join(HERE, 'kd_sensitivity.json'), 'w'), indent=1)
print("\nwrote kd_sensitivity.json")
