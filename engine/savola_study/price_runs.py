#!/usr/bin/env python3
"""All critique-finding pricing runs (step 3 of the response procedure).
Each run prices ONE finding against the delivered base. Output feeds the ledger."""
from price_findings import run, price, BASE_CENTRAL, BASE_DCF

R = {}

# --- base sanity ---
ns = run()
assert abs(ns['CENTRAL'] - BASE_CENTRAL) < 1e-9

# CW1/GT1/GR1: settled spot 25.40 (enters WACC weight only in the model)
R['spot 25.40 (WACC weight leg only)'] = price('spot 25.40 (WACC weight leg only)',
                                               run({'spot': 25.40}))

# GT1b: Herfy 15.66 claim (NCI leg + E1)
ns_h = run({'herfy_price': 15.66})
R['herfy 15.66 (GT claim, unverified)'] = price('herfy 15.66 (GT claim, unverified)', ns_h)
print(f"    e1 base moves {ns['e1_base']:.4f} -> {ns_h['e1_base']:.4f}")

# CW3 (accept) / GT2 (mirror, reject): FCFF charges full lease additions
LEASE_PATCH = (
    "FCFF = [n + d - c - r - w for n, d, c, r, w in\n"
    "        zip(NOPAT, DNA, B['capex'], ROU_D, DWC)]",
    "_lb = V['leases_fy25']\n"
    "DLEASE = []\n"
    "for _g in V['rou_growth']:\n"
    "    DLEASE.append(_lb * _g)\n"
    "    _lb += _lb * _g\n"
    "FCFF = [n + d - c - r - dl - w for n, d, c, r, dl, w in\n"
    "        zip(NOPAT, DNA, B['capex'], ROU_D, DLEASE, DWC)]",
)
ns_l = run(patches=[LEASE_PATCH])
R['CW3 charge full lease additions'] = price('CW3 charge full lease additions', ns_l)

# GT2 as proposed: REMOVE the lease charge entirely (the mirror error, priced for the ledger)
GT_PATCH = (
    "FCFF = [n + d - c - r - w for n, d, c, r, w in\n"
    "        zip(NOPAT, DNA, B['capex'], ROU_D, DWC)]",
    "FCFF = [n + d - c - w for n, d, c, w in\n"
    "        zip(NOPAT, DNA, B['capex'], DWC)]",
)
R['GT2 as proposed: no lease charge'] = price('GT2 as proposed: no lease charge',
                                              run(patches=[GT_PATCH]))

# CW12/GR/GT warnings: terminal ROIC at the model's own year-5 (9.66%)
R['CW12 terminal ROIC 9.66%'] = price('CW12 terminal ROIC 9.66%', run({'roic_term': 0.0966}))

# CW13 + Q2 interims: point-in-time ex-treasury divisor 296.682mn
R['CW13 shares 296.682 point-in-time'] = price('CW13 shares 296.682 point-in-time',
                                               run({'shares_wavg_mn': 296.682}))
# Cowork's own version (300mn issued)
R['CW13 as proposed: 300mn'] = price('CW13 as proposed: 300mn', run({'shares_wavg_mn': 300.0}))

# CW18 as proposed: strip the 85bp market spread (rf* = 4.68%)
R['CW18 as proposed rf*=4.68'] = price('CW18 as proposed rf*=4.68',
                                       run({'sov_spread_rating': 0.0085}))
# Second-edition fix: FTSE SAGBI 5.52% observed + July-2026 Damodaran (0.48 / 4.94)
R['fix: rf 5.52 + July Damodaran'] = price('fix: rf 5.52 + July Damodaran',
                                           run({'rf_observed': 0.0552,
                                                'sov_spread_rating': 0.0048,
                                                'erp_rating': 0.0494}))

# CW25/CC15: WACC weights on the 30-Jun-2026 balance sheet (loans 2,664.5 / leases 3,716.8)
W_PATCH1 = ("EV_w = mktcap + V['loans_fy25'] + V['leases_fy25']",
            "EV_w = mktcap + 2664.518 + 3716.808")
W_PATCH2 = ("wl = V['loans_fy25'] / EV_w", "wl = 2664.518 / EV_w")
W_PATCH3 = ("wz = V['leases_fy25'] / EV_w", "wz = 3716.808 / EV_w")
R['CW25 weights on 30-Jun BS'] = price('CW25 weights on 30-Jun BS',
                                       run(patches=[W_PATCH1, W_PATCH2, W_PATCH3]))

# CC2: Tiryaki 274.6 receivable into the bridge (+ WC ratio ex-receivable)
TIR_PATCH = ("NONOP = V['inv_nc_fy25'] + V['inv_c_fy25'] + kinan_capitalized + V['invprop_fy25']",
             "NONOP = V['inv_nc_fy25'] + V['inv_c_fy25'] + kinan_capitalized + V['invprop_fy25'] + 274.619")
R['CC2 Tiryaki 274.6 in bridge'] = price('CC2 Tiryaki 274.6 in bridge', run(patches=[TIR_PATCH]))
R['CC2b + WC ratio ex-receivable 4.11%'] = price(
    'CC2b + WC ratio ex-receivable 4.11%',
    run({'prepay_ratio': 0.0411}, patches=[TIR_PATCH]))

# GT4 (accept; self-audit find): investment property 158.2 out of the bridge
IP_PATCH = ("NONOP = V['inv_nc_fy25'] + V['inv_c_fy25'] + kinan_capitalized + V['invprop_fy25']",
            "NONOP = V['inv_nc_fy25'] + V['inv_c_fy25'] + kinan_capitalized")
R['GT4 drop invprop from bridge'] = price('GT4 drop invprop from bridge', run(patches=[IP_PATCH]))

# GT5 as proposed: Herfy NCI at book 434.6 instead of market 511.3
R['GT5 as proposed NCI at book'] = price('GT5 as proposed NCI at book',
                                         run(patches=[("nci_herfy_mkt = 0.51 * herfy_mktcap",
                                                       "nci_herfy_mkt = V['nci_herfy_book']")]))

# CC3: book lens on the model's own FY2026E recurring (NP[0])
BOOK_PATCH = ("roe_sust = (V['recurring_np_fy25'] * (1 + V['rec_g_fy26'])) / V['equity_att_fy25']",
              "roe_sust = NP[0] / V['equity_att_fy25']")
ns_b = run(patches=[BOOK_PATCH])
R['CC3 book lens on model FY26E'] = price('CC3 book lens on model FY26E', ns_b)
print(f"    NP[0]={ns_b['NP'][0]:.1f} roe_sust={ns_b['roe_sust']*100:.2f}% book {ns['book_base']:.2f}->{ns_b['book_base']:.2f}")

# CW2: Al Othaim n/m -> retail leg = BinDawood alone
pp = dict(ns['V']['peer_pe'])
pp['OTHAIM'] = pp['BINDAWOOD']
R['CW2 Othaim n/m'] = price('CW2 Othaim n/m', run({'peer_pe': pp}))

# CW21/CC9: peers at true 18-Aug closes (BinDawood 20.20, Othaim n/m stays for this run alone)
pp2 = dict(ns['V']['peer_pe']); pp2['BINDAWOOD'] = 20.20; pp2['WILMAR'] = 12.54; pp2['ALMARAI'] = 19.77
R['CW21 peers at 18-Aug closes'] = price('CW21 peers at 18-Aug closes', run({'peer_pe': pp2}))

# CW24: mix weight from the model's own FY26E EBITDA (53.6% FP)
R['CW24 mix weight 53.6%'] = price('CW24 mix weight 53.6%', run({'pe_mix_w_fp': 0.536}))

# CW20: roll every lens to the anchor (their mechanical reading of the caption)
ROLL_PATCH = [
    ("rel_base = pe_applied * eps_f[0]", "rel_base = to_anchor(pe_applied * eps_f[0])[0]"),
    ("norm_base = eps_norm * pe_applied", "norm_base = to_anchor(eps_norm * pe_applied)[0]"),
    ("book_base = bvps * pb_just", "book_base = to_anchor(bvps * pb_just)[0]"),
]
R['CW20 roll all lenses'] = price('CW20 roll all lenses', run(patches=ROLL_PATCH))

# CW22: trailing multiple on trailing recurring EPS (like-for-like variant)
# TTM recurring to 30-Jun-2026 = 539.1 - 372/1.40 + 372 = 645.4; EPS on 298.589 (base divisor)
TTM_PATCH = ("rel_base = pe_applied * eps_f[0]",
             "rel_base = pe_applied * (645.4 / V['shares_wavg_mn'])")
R['CW22 trailing x trailing (rel)'] = price('CW22 trailing x trailing (rel)',
                                            run(patches=[TTM_PATCH]))

# CW22b: normalized lens on FY2026E instead of FY2027E (mismatch variant)
NORM_PATCH = [("rev_mid = B['rev'][1]", "rev_mid = B['rev'][0]"),
              ("np_norm = (((rev_mid * V['norm_ebitda_mgn'] - DNA[1]) + NF[1]) * (1 - T) * (1 - NCI_SHARE)\n"
               "           + KINAN[1])",
               "np_norm = (((rev_mid * V['norm_ebitda_mgn'] - DNA[0]) + NF[0]) * (1 - T) * (1 - NCI_SHARE)\n"
               "           + KINAN[0])")]
R['CW22b normalized on FY26E'] = price('CW22b normalized on FY26E', run(patches=NORM_PATCH))

# CW28: store path at the H1 run-rate (+8/yr)
R['CW28 stores at H1 run-rate'] = price('CW28 stores at H1 run-rate',
                                        run({'stores_path': [235.0, 243.0, 251.0, 259.0, 267.0]}))

# CW29: sps opening density -5.9% instead of -6% (derivation range end)
R['CW29 sps open -5.9%'] = price('CW29 sps open -5.9%',
                                 run({'sps_g_A': [-0.059, -0.03, -0.01, 0.0, 0.0]}))
R['CW29 sps open -7.1%'] = price('CW29 sps open -7.1%',
                                 run({'sps_g_A': [-0.071, -0.03, -0.01, 0.0, 0.0]}))

# CC14a/CW14: Herfy margin at the disclosed 18.7%
R['CW14 herfy margin 18.7%'] = price('CW14 herfy margin 18.7%', run({'herfy_ebitda_mgn': 0.187}))

# CW37: July-2026 Damodaran vintage alone (0.48 / 4.94), rf construction unchanged
R['CW37 July Damodaran alone'] = price('CW37 July Damodaran alone',
                                       run({'sov_spread_rating': 0.0048, 'erp_rating': 0.0494}))

# Mehbaj deferred consideration 6.0 as a bridge liability
MEH_PATCH = ("NONOP = V['inv_nc_fy25'] + V['inv_c_fy25'] + kinan_capitalized + V['invprop_fy25']",
             "NONOP = V['inv_nc_fy25'] + V['inv_c_fy25'] + kinan_capitalized + V['invprop_fy25'] - 6.0")
R['CW9/CC7 Mehbaj deferred -6.0'] = price('CW9/CC7 Mehbaj deferred -6.0', run(patches=[MEH_PATCH]))

# CW26: de-roll the two anchor-dated legs (formula-priced, verified by patch here)
DEROLL = ("EQ = bridge(EV_OP)" if False else None)
ns_dr = run(patches=[(
    "PS, ROLL = to_anchor(PS_DEC)",
    "ROLL = (1 + ke_rating) ** (V['anchor_days'] / 365.0)\n"
    "PS = ((EQ - kinan_capitalized + nci_herfy_mkt) * ROLL + kinan_capitalized - nci_herfy_mkt) \\\n"
    "     / V['shares_wavg_mn'] - V['div_between']",
)])
R['CW26 de-roll Kinan/Herfy legs'] = price('CW26 de-roll Kinan/Herfy legs', ns_dr)

# CC11: Expert 1 - exclude Herfy's own liabilities (728.9) from the group deduction
E1_PATCH = ("e1_eq = (e1_ev + e1_herfy + NONOP + V['cash_fy25'] - V['loans_fy25'] - V['leases_fy25']",
            "e1_eq = (e1_ev + e1_herfy + 728.9 + NONOP + V['cash_fy25'] - V['loans_fy25'] - V['leases_fy25']")
ns_e1 = run(patches=[E1_PATCH])
print(f"CC11 e1 with Herfy liabs excluded: e1 {ns['e1_base']:.2f} -> {ns_e1['e1_base']:.2f} "
      f"(+{ns_e1['e1_base'] - ns['e1_base']:.2f}); central unchanged {ns_e1['CENTRAL']:.4f}")

# E3 rebuilt consistently (CW4/5/6, CC1/12): bridge via the accounting identity,
# IC path includes lease additions, lo/hi carry every bridge term
E3_PATCH = [
    # IC path: include the lease-book growth the model's own BS walk carries
    ("    reinv = B['capex'][i] + ROU_D[i] + DWC[i] - DNA[i]",
     "    reinv = B['capex'][i] + ROU_D[i] + DWC[i] - DNA[i] + V['leases_fy25'] * V['rou_growth'][i] * (1 + 0)"),
    # consistent equity bridge: IC0 identity => add back cash/investments/kinan, deduct debt & NCI only
    ("e3_eq = (e3_ev + NONOP + V['kinan_carry'] + V['cash_fy25'] + V['inv_c_fy25'] * 0.0\n"
     "         - V['loans_fy25'] - V['leases_fy25'] - V['eb_fy25'] - V['restor_fy25'] - V['other_net_liab'] - NCI_VAL)",
     "e3_eq = (e3_ev + V['cash_fy25'] + V['inv_c_fy25'] + V['inv_nc_fy25'] + V['kinan_carry']\n"
     "         - V['loans_fy25'] - V['leases_fy25'] - NCI_VAL)"),
    ("e3_lo = to_anchor((IC0 + e3_pv_ri + NONOP + V['kinan_carry'] + V['cash_fy25']\n"
     "                   - V['loans_fy25'] - V['leases_fy25'] - V['eb_fy25'] - V['restor_fy25']\n"
     "                   - NCI_VAL) / V['shares_wavg_mn'])[0]",
     "e3_lo = to_anchor((e3_eq - e3_fade) / V['shares_wavg_mn'])[0]"),
    ("e3_hi = to_anchor((IC0 + e3_pv_ri + e3_fade + ri5 * 0.4 / (wacc_exp)\n"
     "                   / (1 + wacc_exp) ** 10 + NONOP + V['kinan_carry'] + V['cash_fy25']\n"
     "                   - V['loans_fy25'] - V['leases_fy25'] - V['eb_fy25'] - V['restor_fy25']\n"
     "                   - NCI_VAL) / V['shares_wavg_mn'])[0]",
     "e3_hi = to_anchor((e3_eq + ri5 * 0.4 / (wacc_exp) / (1 + wacc_exp) ** 10)\n"
     "                  / V['shares_wavg_mn'])[0]"),
]
ns_e3 = run(patches=E3_PATCH)
print(f"E3 rebuilt: base {ns['e3_base']:.2f} -> {ns_e3['e3_base']:.2f}; "
      f"rng [{ns_e3['e3_lo']:.2f}, {ns_e3['e3_hi']:.2f}] (was [{ns['e3_lo']:.2f}, {ns['e3_hi']:.2f}]); "
      f"panel median {ns['PANEL_MED']:.2f} -> {ns_e3['PANEL_MED']:.2f}; central {ns_e3['CENTRAL']:.4f}")
print(f"    RI path {[round(x,1) for x in ns_e3['RI_PATH']]} (was {[round(x,1) for x in ns['RI_PATH']]})")

# ---- the implementable correction stack (accepted mechanical fixes together) ----
STACK_OVR = {
    'spot': 25.40, 'shares_wavg_mn': 296.682,
    'rf_observed': 0.0552, 'sov_spread_rating': 0.0048, 'erp_rating': 0.0494,
    'herfy_ebitda_mgn': 0.187, 'pe_mix_w_fp': 0.536, 'peer_pe': pp,  # Othaim n/m
    'prepay_ratio': 0.0411,
}
STACK_PATCHES = [LEASE_PATCH, W_PATCH1, W_PATCH2, W_PATCH3,
                 ("NONOP = V['inv_nc_fy25'] + V['inv_c_fy25'] + kinan_capitalized + V['invprop_fy25']",
                  "NONOP = V['inv_nc_fy25'] + V['inv_c_fy25'] + kinan_capitalized + 274.619 - 6.0")]
ns_stk = run(STACK_OVR, STACK_PATCHES)
price('STACK pre-terminal-fix', ns_stk)
# terminal ROIC at the corrected model's own year-5 (computed inside the stack run)
_ic = ns_stk['IC_PATH']; _np = ns_stk['NOPAT']
roic5 = _np[4] / _ic[3]
print(f"    stack's own year-5 ROIC (NOPAT5/IC4) = {roic5*100:.2f}%")
ns_stk2 = run({**STACK_OVR, 'roic_term': round(roic5, 4)}, STACK_PATCHES)
price('STACK + terminal ROIC = own year-5', ns_stk2)
print(f"    lens detail: dcf {ns_stk2['PS_A']:.2f} rel {ns_stk2['rel_base']:.2f} "
      f"norm {ns_stk2['norm_base']:.2f} book {ns_stk2['book_base']:.2f}")
print(f"    vs settled spot 25.40: {(ns_stk2['CENTRAL']/25.40-1)*100:+.1f}%")

# ============ FINAL second-edition candidate stack ============
NWC0_PATCH = ("nwc0 = (V['inventories_fy25'] + V['tr_fy25'] + V['prepay_fy25'] - V['tp_fy25']",
              "nwc0 = (V['inventories_fy25'] + V['tr_fy25'] + (V['prepay_fy25'] - 274.619) - V['tp_fy25']")
BVPS_PATCH = ("bvps = V['equity_att_fy25'] / V['shares_wavg_mn']",
              "bvps = 5360.505 / V['shares_wavg_mn']")
TTM_FULL = [
    ("rel_base = pe_applied * eps_f[0]", "rel_base = pe_applied * (645.4 / V['shares_wavg_mn'])"),
    ("rel_bear = pe_mix * (1 - 0.30) * eps_f[0]", "rel_bear = pe_mix * (1 - 0.30) * (645.4 / V['shares_wavg_mn'])"),
    ("rel_bull = pe_mix * (1 - 0.10) * eps_f[0]", "rel_bull = pe_mix * (1 - 0.10) * (645.4 / V['shares_wavg_mn'])"),
]
DEROLL_PATCH = (
    "PS, ROLL = to_anchor(PS_DEC)",
    "ROLL = (1 + ke_rating) ** (V['anchor_days'] / 365.0)\n"
    "PS = ((EQ - kinan_capitalized + nci_herfy_mkt) * ROLL + kinan_capitalized - nci_herfy_mkt) \\\n"
    "     / V['shares_wavg_mn'] - V['div_between']",
)
pp3 = dict(ns['V']['peer_pe']); pp3['OTHAIM'] = 20.20; pp3['BINDAWOOD'] = 20.20
pp3['WILMAR'] = 12.54; pp3['ALMARAI'] = 19.77   # Othaim n/m => retail leg = BinDawood 18-Aug
FINAL_OVR = {
    'spot': 25.40, 'shares_wavg_mn': 296.682,
    'rf_observed': 0.0552, 'sov_spread_rating': 0.0048, 'erp_rating': 0.0494,
    'herfy_ebitda_mgn': 0.187, 'pe_mix_w_fp': 0.536, 'peer_pe': pp3,
    'prepay_ratio': 0.0411,
}
TIRBS_PATCH = ("    assets = (PPE_PATH[i] + ROU_P[i] + V['intang_fy25'] + V['invprop_fy25'] + KINAN_BV[i]\n"
               "              + V['inv_nc_fy25'] + V['inv_c_fy25'] + NWC[i] + CASH_P[i])",
               "    assets = (PPE_PATH[i] + ROU_P[i] + V['intang_fy25'] + V['invprop_fy25'] + KINAN_BV[i]\n"
               "              + V['inv_nc_fy25'] + V['inv_c_fy25'] + 274.619 + NWC[i] + CASH_P[i])")
FINAL_PATCHES = [LEASE_PATCH, W_PATCH1, W_PATCH2, W_PATCH3, NWC0_PATCH, TIRBS_PATCH, BVPS_PATCH,
                 BOOK_PATCH, DEROLL_PATCH] + TTM_FULL + NORM_PATCH + E3_PATCH + [E1_PATCH] + [
    ("NONOP = V['inv_nc_fy25'] + V['inv_c_fy25'] + kinan_capitalized + V['invprop_fy25']",
     "NONOP = V['inv_nc_fy25'] + V['inv_c_fy25'] + kinan_capitalized + 274.619 - 6.0")]
ns_f0 = run(FINAL_OVR, FINAL_PATCHES)
price('FINAL pre-terminal', ns_f0)
roic5c = ns_f0['NOPAT'][4] / ns_f0['IC_PATH'][3]
print(f"    corrected-path year-5 ROIC = {roic5c*100:.3f}%")
ns_fin = run({**FINAL_OVR, 'roic_term': round(roic5c, 5)}, FINAL_PATCHES)
price('FINAL second-edition candidate', ns_fin)
print(f"    lenses: dcf {ns_fin['PS_A']:.2f} | rel {ns_fin['rel_base']:.2f} | "
      f"norm {ns_fin['norm_base']:.2f} | book {ns_fin['book_base']:.2f}")
print(f"    wacc {ns_fin['wacc_exp']*100:.3f}% -> term {ns_fin['wacc_term']*100:.3f}% | ke {ns_fin['ke_rating']*100:.3f}%")
print(f"    experts: e1 {ns_fin['e1_base']:.2f} | e2 {ns_fin['e2_base']:.2f} | e3 {ns_fin['e3_base']:.2f} "
      f"| panel median {ns_fin['PANEL_MED']:.2f}")
print(f"    framings: A {ns_fin['PS_A']:.2f} / B {ns_fin['PS_B']:.2f} | bear {ns_fin['PS_BEAR']:.2f} bull {ns_fin['PS_BULL']:.2f}")
print(f"    vs settled spot 25.40: {(ns_fin['CENTRAL']/25.40-1)*100:+.1f}%  (was +11% on 25.30)")
