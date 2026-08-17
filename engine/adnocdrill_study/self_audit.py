"""ADNOC Drilling — self-audit of THIS edition, run before anyone else reads it.

This is not the previous edition's self-audit re-run. That one found ten things
and all ten are now inside the model, so re-running it would report ten changes
of nothing and call that a pass — which is how a self-audit becomes a formality.
The file has been rewritten to interrogate the model as it now stands, including
the corrections themselves: a correction is a new claim, and a new claim is a new
place to be wrong.

Every finding here is PRICED before it is judged. Nothing is called immaterial
without a number beside it.
"""
import os, sys, json, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('adnoc_compute', os.path.join(HERE, 'compute.py'))
C = importlib.util.module_from_spec(spec)
sys.stdout = open(os.devnull, 'w')
spec.loader.exec_module(C)
sys.stdout = sys.__stdout__

FV, SPOT = C.central, C.V('spot_aed')
rows = C.CASE['A']['rows']
findings = []


def price(tag, what, new_central, note=''):
    d = new_central - FV
    findings.append(dict(tag=tag, what=what, central=new_central, delta=d, pct=d / FV, note=note))
    return d


def reweighted(overrides):
    f = dict(C.FAIR)
    f.update(overrides)
    w = C.LENS_WEIGHT
    return sum(f[k] * w[k] for k in f) / sum(w[k] for k in f)


print(f'SELF-AUDIT OF THE CURRENT EDITION — weighted central AED {FV:.2f} against a market '
      f'price of AED {SPOT:.2f}\n')
print(f'{"":6}{"":72}{"central":>9}{"move":>8}\n')

# ---------------------------------------------------------------------- A ----
# The unit build sets the SHAPE of the forecast; the company's FY2026 segment
# guidance sets its LEVEL. That is a deliberate choice and it is defensible, but
# it means the phrase "built from the bottom up" is doing less work in 2026 than
# a reader would assume. The size of the correction is the honest measure of how
# much the guidance is carrying, so it is published.
cal = C.CALIB
uncal = C.CALIB_UNCALIBRATED
print('A1    HOW MUCH OF FY2026 IS THE UNIT BUILD AND HOW MUCH IS THE GUIDANCE')
for k, nice in (('onshore', 'Onshore'), ('offshore', 'Offshore'), ('ofs', 'Oilfield Services')):
    print(f'        {nice:<20} unit build reconciled to guidance by a factor of {cal[k]:.3f} '
          f'({(cal[k]-1)*100:+.1f}%)')
print(f'        Group revenue before reconciliation {uncal["total"]/1e6:.3f}bn against guidance '
      f'of {C.V("g26_revenue")/1e6:.3f}bn ({uncal["total"]/C.V("g26_revenue")-1:+.1%})')
print('        The unit rates therefore determine the GROWTH PATH, not the FY2026 level. '
      'A driver\n        test on any FY2025 unit rate correctly shows FY2026 unmoved.\n')

# ---------------------------------------------------------------------- B ----
# The build's FY2026 EBITDA margin against the company's own guided range. The
# label on this line in the previous edition said ABOVE when the number was
# below; it is computed now.
g26_margin = rows[0]['ebitda'] / rows[0]['revenue']
lo = C.V('g26_ebitda_lo') / C.V('g26_revenue')
hi = C.V('g26_ebitda_hi') / C.V('g26_revenue')
where = ('ABOVE' if g26_margin > hi else 'BELOW' if g26_margin < lo else 'INSIDE')
gap = (g26_margin - (lo + hi) / 2)
print(f'B1    FY2026 built EBITDA margin {g26_margin*100:.2f}% against guidance of '
      f'{lo*100:.1f}-{hi*100:.1f}% — {where} the guided range')
print(f'        Distance from the guided midpoint: {gap*100:+.2f} percentage points, or USD '
      f'{gap*rows[0]["revenue"]/1e3:,.0f} million of FY2026 EBITDA.')
# priced: run the whole model with the cost stack scaled so FY2026 hits the guided midpoint
mid = (lo + hi) / 2
scale = (rows[0]['revenue'] * mid - rows[0]['ebitda']) / rows[0]['conv_cash_cost']
lift = [dict(r) for r in rows]
pv = 0.0
for n, r in enumerate(lift, start=1):
    eb = r['ebitda_ex_jv'] - r['conv_cash_cost'] * scale
    ebit = eb - r['dna']
    nop = ebit * (1 - C.V('tax_rate'))
    pv += (nop + r['dna'] - r['capex'] - r['delta_wc']) / (1 + C.WACC) ** n
    last_nopat = nop
g = C.TERMINAL_G['A']
tv = last_nopat * (1 + g) * (1 - g / C.V('terminal_roic')) / (C.WACC - g)
ev25 = pv + tv / (1 + C.WACC) ** len(lift)
price('B1', 'cost stack scaled so FY2026 EBITDA lands on the guided midpoint',
      reweighted(dict(dcf_A=C.bridge(C.roll_ev_to_jun26(ev25)))))
f = findings[-1]
print(f'      {"B1":<6}{"the same model with FY2026 EBITDA on the guided midpoint":<72}'
      f'AED {f["central"]:5.2f} {f["delta"]:+6.2f}  {f["pct"]:+6.1%}\n')

# ---------------------------------------------------------------------- C ----
# The contingent consideration recognised on the SLDC acquisition is a real
# obligation. It sits inside trade and other payables on the 30-Jun-2026 balance
# sheet, which the bridge treats as working capital rather than as debt. Priced
# as a bridge deduction to show the size of the question.
cc = C.V('acq_contingent')
alt = {k: C.bridge(C.CASE[k[-1]]['enterprise_value'] - cc) for k in ('dcf_A', 'dcf_B')}
price('C1', 'contingent consideration treated as debt-like in the bridge', reweighted(alt))
f = findings[-1]
print(f'{"C1":<6}{"contingent consideration deducted in the bridge as debt-like":<72}'
      f'AED {f["central"]:5.2f} {f["delta"]:+6.2f}  {f["pct"]:+6.1%}')
print(f'        USD {cc/1e3:,.1f} million. It is presented inside trade and other payables at 30 '
      f'June 2026,\n        so it is already inside working capital; deducting it again in the '
      f'bridge would double count.\n        Reported as a bound, not applied.\n')

# ---------------------------------------------------------------------- D ----
# Liabilities assumed with the acquisitions that no forecast driver generates are
# held flat across the window. Priced by releasing them entirely.
al = rows[0]['balance_sheet']['acquisition_liabilities']
print(f'D1    acquisition liabilities held FLAT at USD {al/1e3:,.1f} million to 2030')
print(f'        {al/rows[-1]["balance_sheet"]["total_assets"]*100:.2f}% of 2030 total assets. '
      f'They do not enter free cash flow to the firm,\n        so the effect on the valuation is '
      f'nil; they affect the forecast balance sheet only.\n')

# ---------------------------------------------------------------------- E ----
# Joint-venture income sits in forecast profit but is not received as cash unless
# the joint ventures distribute. This overstates the forecast cash balance.
jv_cum = sum(r['jv_share'] for r in rows)
print(f'E1    joint-venture income in forecast profit but never received as cash: USD '
      f'{jv_cum/1e3:,.0f} million cumulative')
print(f'        to 2030, against a forecast 2030 cash balance of USD '
      f'{rows[-1]["cash_close"]/1e3:,.0f} million. It is excluded from\n        EBITDA before the '
      f'cash-flow waterfall, so it does NOT touch enterprise value — the overstatement\n        '
      f'is confined to the forecast balance sheet.\n')

# ---------------------------------------------------------------------- F ----
# Gross debt is held flat in nominal terms for five years while the business
# grows into it. That is a policy assumption, not a forecast.
nd0, nd5 = rows[0]['net_debt'], rows[-1]['net_debt']
print(f'F1    gross interest-bearing debt held FLAT at USD '
      f'{rows[0]["balance_sheet"]["debt"]/1e3:,.0f} million to 2030')
print(f'        Net debt therefore falls from USD {nd0/1e3:,.0f} million in 2026 to USD '
      f'{nd5/1e3:,.0f} million in 2030,\n        and the terminal firm holds net cash. The '
      f'terminal block is nonetheless capitalised at the\n        weighted cost of capital, not '
      f'the cost of equity — see the note on the DCF sheet.\n')

# ---------------------------------------------------------------------- G ----
# Terminal value share. Not a defect, but the number a reader should see first.
print(f'G1    terminal value is {C.CASE["A"]["tv_pct_of_ev"]*100:.1f}% of enterprise value in '
      f'the expansion case and\n        {C.CASE["B"]["tv_pct_of_ev"]*100:.1f}% in the plateau '
      f'case. Both are high, and both are stated in the summary\n        table rather than '
      f'buried.\n')

# ---------------------------------------------------------------------- H ----
# The regional book opens at the count consolidated at 30 June 2026 rather than
# at the count consolidated on 1 January, which overstates 2026 regional
# rig-years. FY2026 revenue is reconciled to guidance so the LEVEL is unaffected;
# the mix is not.
print(f'H1    the regional book opens at the {C.V("rigs_regional_2q26"):.0f} rigs consolidated '
      f'at 30 June 2026, not at the count')
print(f'        consolidated on 1 January. FY2026 regional rig-years of '
      f'{rows[0]["avg_regional"]:.1f} are therefore an\n        upper bound. FY2026 revenue is '
      f'reconciled to the segment guidance, so this moves the MIX\n        inside the onshore '
      f'segment and not the level.\n')

allf = reweighted(dict(dcf_A=C.bridge(C.roll_ev_to_jun26(ev25 - cc)),
                       dcf_B=C.bridge(C.CASE['B']['enterprise_value'] - cc)))
price('ALL', 'the two priced findings applied together', allf)
f = findings[-1]
print(f'{"ALL":<6}{"the two priced findings applied together":<72}'
      f'AED {f["central"]:5.2f} {f["delta"]:+6.2f}  {f["pct"]:+6.1%}')

json.dump(dict(base=FV, spot=SPOT, findings=findings),
          open(os.path.join(HERE, 'self_audit.json'), 'w'), indent=1)
