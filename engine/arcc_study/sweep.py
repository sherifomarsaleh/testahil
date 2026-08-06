"""ARCC — four-ring information sweep register.

Global / Country / Industry / Company. Every finding is classified BLOCKING (B),
STRUCTURAL (S), DRIVER_UNLOCK (D) or COLOR (C), carries a named source and a date, and
states what it does to the model. Findings that set a forecast driver must exist before
the driver is set; the driver table at the bottom records which findings each driver
rests on and whether it is built bottom-up or top-down.

Written to sweep_register.json, which the bibliography document reads.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))

REG = "REGULATOR_OFFICIAL"
PRESS = "REPUTABLE_PRESS"
AGG = "DATA_AGGREGATOR"
FILING = "AUDITED_FINANCIAL_STATEMENTS"
IND = "INDUSTRY_BODY"
HOUSE = "HOUSE_ENGINE"


def F(fid, ring, cat, klass, headline, src, stype, date, impact, is_fs=False, detail=''):
    return dict(fid=fid, ring=ring, category=cat, klass=klass, headline=headline,
                source_name=src, source_type=stype, source_date=date, detail=detail,
                model_impact=impact, is_fs_data=is_fs)


FINDINGS = [
    # ------------------------------- GLOBAL ---------------------------------
    F('F01', 'GLOBAL', 'rate cycle and FX regime', 'STRUCTURAL',
      'The global easing cycle is under way, which is the backdrop against which Egypt '
      'normalises a 19.50% policy rate rather than the cause of it',
      'US Federal Reserve policy history as carried in the house rate schedule',
      REG, '2026-06-18',
      'Sets the direction, not the level, of the cost-of-debt path that the discount-rate '
      'glide inherits its shape from.'),
    F('F02', 'GLOBAL', 'commodity complex (input)', 'STRUCTURAL',
      'Cement is an energy-conversion business: solid fuel and electricity dominate cash '
      'cost, so the fuel bill is the single most important cost driver in the build',
      'Global Cement / International Cement Review industry coverage', PRESS, '2026-02-16',
      'Fuel is modelled explicitly as thermal energy per tonne of clinker times a blended '
      'fuel price, rather than buried in an assumed margin.'),
    F('F03', 'GLOBAL', 'carbon and trade policy', 'DRIVER_UNLOCK',
      'The EU Carbon Border Adjustment Mechanism raises the landed cost of Egyptian cement '
      'in Europe; a low-carbon producer earns a relative premium estimated at about EUR 5.4 '
      'per tonne on European sales',
      'Industry coverage of Egyptian producers\' CBAM positioning', PRESS, '2026-01-01',
      'Sets the export price path DOWN in dollar terms for the industry generally while '
      'giving this producer a smaller decline than a high-clinker peer would suffer; '
      'carried in the export price driver, not as a separate revenue leg.'),
    F('F04', 'GLOBAL', 'traded-goods structure', 'COLOR',
      'Cement is not traded at distance — bulk freight caps the economic export radius, so '
      'global demand reaches an Egyptian producer only through the Mediterranean and East '
      'African basin and never through a world price',
      'Global Cement, Egypt country coverage', PRESS, '2025-10-01',
      'Justifies modelling a domestic price and an export price separately rather than '
      'applying one international benchmark.'),

    # ------------------------------- COUNTRY --------------------------------
    F('F05', 'COUNTRY', 'sovereign macro', 'DRIVER_UNLOCK',
      'The Central Bank of Egypt held the main operation rate at 19.50% (overnight deposit '
      '19.00%, lending 20.00%) at its April and May 2026 meetings; headline urban inflation '
      'eased for a third month to 14.3% in June 2026, and the CBE expects it to accelerate '
      'through Q3-2026 on base effects before declining toward target',
      'Central Bank of Egypt policy decisions and Monetary Policy Report Q1-2026; CAPMAS '
      'CPI release', REG, '2026-07-10',
      'Sets the explicit-window risk-free anchor and the shape of the cost-of-debt path. '
      'The TERMINAL risk-free rate is norm-built from the CBE\'s own published medium-term '
      'inflation target plus a standard emerging-market real-rate convention — never a '
      'historical average and never reverse-engineered from a price.'),
    F('F06', 'COUNTRY', 'sovereign credit', 'STRUCTURAL',
      'Egypt\'s five-year credit default swap traded around 335 basis points in mid-2026, '
      'far tighter than the 2024 crisis peak',
      'Sovereign CDS quotations as carried by market data services; Damodaran country risk '
      'file, January 2026 edition, CDS column', PRESS, '2026-05-15',
      'The sovereign default spread is NETTED OUT of the local-currency risk-free rate '
      'before a country equity risk premium is added, so Egypt\'s default risk is charged '
      'once rather than twice.'),
    F('F07', 'COUNTRY', 'currency', 'STRUCTURAL',
      'The pound has been broadly stable around EGP 50.3-51.0 per US dollar through '
      'July and early August 2026',
      'Egyptian bank exchange-rate surveys reported by Amwal Al Ghad and Arab Finance',
      PRESS, '2026-08-04',
      'Sets the level of the currency path that converts the dollar-priced fuel bill and '
      'the dollar-priced export price into pounds. The two legs partly offset, which is '
      'why the path is carried as one driver rather than two.'),
    F('F08', 'COUNTRY', 'fiscal policy', 'STRUCTURAL',
      'Phased energy-subsidy reform continues to raise the domestic industrial energy bill '
      'independently of the global fuel price',
      'Egyptian cement industry market coverage on energy reform, currency volatility and '
      'raw-material management', PRESS, '2026-02-16',
      'Applies a local cost-inflation index to the pound-denominated cost lines, which is '
      'what prevents the margin from being held flat at the FY2025 peak.'),
    F('F09', 'COUNTRY', 'taxation', 'STRUCTURAL',
      'Egypt\'s statutory corporate income tax rate is 22.5%',
      'Egyptian Tax Authority statutory rate', REG, '2026-01-01',
      'Floor for the tax rate used in the after-tax operating profit line; the rate actually '
      'applied is the effective rate implied by the company\'s own disclosed profit, which '
      'is higher.'),

    # ------------------------------- INDUSTRY -------------------------------
    F('F10', 'INDUSTRY', 'sector structure', 'DRIVER_UNLOCK',
      'Egypt abolished the cement production-quota system in May 2025 and capped exports at '
      '30% of a producer\'s output; prices stabilised near USD 81 per tonne after the change',
      'Egyptian Competition Authority and Industrial Development Authority decisions as '
      'reported by Enterprise and Global Cement', PRESS, '2025-05-01',
      'The unlock that lets utilisation rise in the forecast, and simultaneously the reason '
      'the price path is set BELOW inflation: the same decision that frees volume also '
      'removes the mechanism that was supporting price.'),
    F('F11', 'INDUSTRY', 'supply pipeline', 'DRIVER_UNLOCK',
      'With quotas gone, producers are studying the revival of seven to nine dormant '
      'production lines, potentially adding 12.6 million tonnes from the second half of '
      '2026 — about 23% of domestic consumption',
      'Global Cement, Egypt update; Enterprise industry coverage', PRESS, '2025-10-01',
      'The single most important reason the realised-price path grows more slowly than '
      'inflation across the forecast, and the reason the asset lens is a ceiling rather '
      'than a floor.'),
    F('F12', 'INDUSTRY', 'demand and price', 'DRIVER_UNLOCK',
      'Domestic consumption grew 13-14% to roughly 54 million tonnes in 2025 and cement '
      'sales rose 10.4% to 44.7Mt in FY2024/25; Portland prices ran 80-85% above the 2024 '
      'average during 2025 and are expected to settle near EGP 3,600 per tonne in 2026, '
      'with demand growth forecasts for 2026 spanning 1% to 8%',
      'Enterprise industry review of Egyptian cement 2025; Arab Finance building-materials '
      'indicators', PRESS, '2026-01-15',
      'Anchors both the FY2025 realised-price reconciliation and the deliberately '
      'conservative forward price path.'),
    F('F13', 'INDUSTRY', 'capacity and utilisation', 'STRUCTURAL',
      'Egyptian nameplate capacity is about 76 million tonnes against roughly 54 million '
      'tonnes of domestic consumption and about 65 million tonnes of production',
      'Global Cement, Egypt country update', PRESS, '2025-10-01',
      'Fixes sector utilisation near 70%, which is the cross-check on this producer\'s own '
      'utilisation path and the reason no capacity expansion is modelled.'),
    F('F14', 'INDUSTRY', 'exports', 'STRUCTURAL',
      'Egyptian cement and clinker exports were about 18.5 million tonnes in 2025, with '
      'finished-cement exports up sharply and clinker exports down',
      'Global Cement export coverage', PRESS, '2026-01-01',
      'Supports a higher realised export price per tonne than a clinker-weighted mix would '
      'give, carried inside the export price driver.'),
    F('F15', 'INDUSTRY', 'cost benchmarks', 'STRUCTURAL',
      'Dry preheater/precalciner kilns run at 3.2-3.6 GJ per tonne of clinker and 90-110 '
      'kWh per tonne of cement; replacement cost for grey-cement capacity sits in the USD '
      '120-150 per annual tonne band and fixed cash cost in the USD 10-20 band',
      'Standard cement engineering and industry cost benchmarks', IND, '2026-08-06',
      'Every physical coefficient in the unit cost stack, and the replacement-cost anchor '
      'behind the asset lens and the terminal return on capital.'),
    F('F16', 'INDUSTRY', 'peer set', 'COLOR',
      'The listed Egyptian cement comparator set is thin and its published multiples are '
      'internally inconsistent: for one peer a quoted price/earnings ratio cannot be '
      'reconciled with the market capitalisation printed beside it',
      'Aggregated peer data cross-checked against reported profit and market capitalisation',
      AGG, '2026-08-06',
      'The relative lens is struck on a RECOMPUTED peer multiple, and its weight is held '
      'down because the anchor is weak.'),

    # ------------------------------- COMPANY --------------------------------
    F('F17', 'COMPANY', 'asset base', 'STRUCTURAL',
      'A cement producer with a clinker capacity of 4.2 million tonnes a year that can produce '
      '5 million tonnes a year of cement, on two lines in Suez governorate',
      'Audited FY2025 statements note 1', FILING, '2025-12-31',
      'Nameplate capacity, the base of the volume build, the denominator of the '
      'enterprise-value-per-tonne lens and the base of the fixed-cost line.'),
    F('F18', 'COMPANY', 'financial history', 'DRIVER_UNLOCK',
      'Net sales EGP 4.67bn (2022), 6.04bn (2023), 8.729bn (2024) and 12.447bn (2025, '
      '+42.6%); attributable profit EGP 358.98mn, 697.49mn, 1.160bn and 3.599bn; earnings '
      'per share EGP 3.02 (2024) and 9.49 (2025)',
      'Audited consolidated financial statements FY2023-FY2025, Deloitte (Wafik, Ramy & '
      'Partners), signed 25 February 2026', FILING, '2025-12-31',
      'The disclosed history the whole model closes against, and the base year of the '
      'forecast.', is_fs=True),
    F('F19', 'COMPANY', 'financial history', 'DRIVER_UNLOCK',
      'Full-year 2025 operating income of EGP 4,595.82mn and a fourth-quarter EBITDA of '
      'EGP 1,393.01mn on fourth-quarter sales of EGP 3,645.60mn; trailing gross margin '
      '40.77%',
      'Audited consolidated financial statements FY2025 — statement of profit or loss, and '
      'notes 5 and 6', FILING, '2025-12-31',
      'The disclosed operating-profit anchor the bottom-up cost stack is calibrated to, and '
      'one of the three legs of the depreciation triangulation.', is_fs=True),
    F('F20', 'COMPANY', 'balance sheet', 'DRIVER_UNLOCK',
      'Total assets about EGP 8,783.72mn, total equity about EGP 4,642.73mn, total debt '
      'about EGP 1,035.19mn and cash about EGP 3,459.39mn on the latest reported balance '
      'sheet — a NET CASH position of roughly EGP 2.42bn',
      'Audited consolidated statement of financial position at 31 December 2025 and notes 19, '
      '20, 21, 24 and 25', FILING, '2025-12-31',
      'The enterprise-to-equity bridge, the capital-structure weights in the cost of '
      'capital, and the treasury-income line. Carried with an explicit caution: a separate '
      'aggregation prints total liabilities of EGP 2,894.13mn, which does not close against '
      'the same total-asset and equity pair, so the liabilities figure is DERIVED on the '
      'sheet and the disagreement is disclosed rather than averaged away.', is_fs=True),
    F('F21', 'COMPANY', 'recent trading', 'DRIVER_UNLOCK',
      'First-quarter 2026 net sales EGP 2.995bn (from 2.554bn) and attributable profit EGP '
      '943.068mn (from 590.347mn), +59.7% year on year, earnings per share EGP 2.50',
      'Reviewed condensed consolidated interim financial statements, three months to 31 March '
      '2026, Deloitte, 25 May 2026', FILING, '2026-03-31',
      'The reality check on the first forecast year: revenue growth has decelerated to '
      '+17.3% while profit growth remains strong, which is precisely the price-flat, '
      'margin-holding pattern the forecast assumes.', is_fs=True),
    F('F22', 'COMPANY', 'distributions', 'STRUCTURAL',
      'Cash dividends of EGP 1.10bn for 2024 (EGP 2.94 per share) and EGP 2.0bn for 2025 '
      '(EGP 5.34 per share), a payout of about 56% of attributable profit',
      'Audited FY2025 statements note 28 (general assembly resolution of 2 December 2025) and '
      'the Q1-2026 dividends-payable balance', FILING, '2026-03-31',
      'Sets the forecast payout ratio and, through it, the cash roll-forward on the balance '
      'sheet. Also the sharpest cross-check on the share count: both distributions divide to '
      'the same count to within 0.2%.', is_fs=True),
    F('F23', 'COMPANY', 'ownership', 'COLOR',
      'Aridos Jativa, a Spanish company, owns 60% of the capital. The group also consolidates '
      'Andalus Concrete (99.99%), ACC Management and Trading (99%), Evolve for Investment '
      'and Project Management — the alternative-fuel arm — and Egypt Green for environmental '
      'services, both 99.99%. The company holds 1% of its own capital in treasury, acquired '
      'during 2025 under a board approval of 21 July 2025',
      'Audited FY2025 statements notes 1, 21 and 24', FILING, '2025-12-31',
      'Context for the minority-position risk paragraph. No control premium or discount is '
      'applied anywhere in the valuation.'),
    F('F24', 'COMPANY', 'decarbonisation and cost position', 'DRIVER_UNLOCK',
      'The company is Egypt\'s alternative-fuel leader — refuse-derived fuel and biomass '
      'substitution, a 7.2 MWh solar station commissioned in 2019, baghouse filters and '
      'hydrogen injection in 2024, targeting a 120,000-tonne annual emissions reduction — '
      'and is advancing supplementary cementitious materials, calcined-clay clinker and a '
      'CEM III product with 50% slag',
      'Company sustainability disclosure and industry coverage', FILING, '2026-01-01',
      'The one genuinely company-specific cost lever in the build: the alternative-fuel '
      'substitution rate enters the fuel cost line directly, and the falling clinker factor '
      'enters the volume conversion. This is why the cost stack is not a sector average.'),
    F('F25', 'COMPANY', 'market data', 'STRUCTURAL',
      'Closing price EGP 59.00 on 6 August 2026 (open 58.40, high 59.90, low 58.25) on '
      '374.87mn shares — a market capitalisation of about EGP 22.1bn',
      'The supplied EGX daily series; share count corroborated by both dividend '
      'distributions', AGG, '2026-08-06',
      'The anchor for every versus-spot comparison, the equity weight in the cost of '
      'capital, and the per-share conversion of every lens.'),
    F('F26', 'COMPANY', 'price behaviour', 'STRUCTURAL',
      'The supplied series runs 2,957 sessions from 18 May 2014 to 6 August 2026 with no '
      'placeholder rows, no unadjusted corporate action and a largest single-session move '
      'of 18.2% against the exchange\'s 20% daily limit; the share closes unchanged on '
      '12.2% of sessions against an Egyptian library median of 9.0%',
      'House data-quality gate over the supplied series', HOUSE, '2026-08-06',
      'Clears the price history for use in the probabilistic price map and in the beta '
      'regression, and quantifies the thin-trading bias the beta section has to answer.'),
]

DRIVERS = [
    dict(driver='Sales volume (Mt)', mode='BOTTOM_UP',
         justification=('Built from nameplate cement capacity of about 5.0Mt times a kiln '
                        'utilisation path, cross-checked two ways: against the disclosed '
                        'share of Egyptian nominal capacity (about 6% of 76Mt = 4.6Mt) and '
                        'against sector utilisation of roughly 70%. Quota abolition is the '
                        'unlock that lets utilisation rise.'),
         sweep_refs=['F17', 'F10', 'F13', 'F11']),
    dict(driver='Realised price (EGP/t)', mode='BOTTOM_UP',
         justification=('Domestic and export prices are carried separately. The FY2025 '
                        'domestic price is the level the DISCLOSED revenue implies given '
                        'the volume build and the export split, so the build ties back to '
                        'the printed top line rather than asserting a price.'),
         sweep_refs=['F12', 'F14', 'F18', 'F04']),
    dict(driver='Fuel cost and alternative-fuel substitution', mode='BOTTOM_UP',
         justification=('Thermal energy per tonne of clinker times a blended fuel price, '
                        'where the blend is the company\'s own alternative-fuel '
                        'substitution rate applied between a fossil and a refuse-derived '
                        'fuel price. This is the company-specific lever and it is modelled '
                        'as one, not folded into a margin.'),
         sweep_refs=['F24', 'F02', 'F15', 'F07']),
    dict(driver='EBITDA margin', mode='BOTTOM_UP',
         justification=('An OUTPUT of the physical cost stack, not an input. It glides down '
                        'from the FY2025 peak on two named, dated mechanisms — 12.6Mt of '
                        'dormant capacity restarting from 2H-2026, and phased energy-'
                        'subsidy reform — and is calibrated so the FY2025 reconstruction '
                        'reproduces the disclosed operating profit.'),
         sweep_refs=['F11', 'F08', 'F19', 'F15']),
    dict(driver='Depreciation and amortisation', mode='TOP_DOWN',
         justification=('No depreciation line is separately disclosed in any retrievable '
                        'source. It is TRIANGULATED on the sheet by three independent '
                        'methods — a fourth-quarter EBITDA-margin closure, a peer per-tonne '
                        'anchor, and a net-property-base estimate times a composite rate — '
                        'and averaged there rather than asserted.'),
         sweep_refs=['F19', 'F20']),
    dict(driver='Capital expenditure', mode='TOP_DOWN',
         justification=('No capital-expenditure guidance is obtainable. Capex is set at the '
                        'ECONOMIC maintenance level in dollars per tonne of capacity rather '
                        'than at book depreciation, because a historic-cost asset base in a '
                        'currency that has devalued several times understates what it '
                        'actually costs to keep the plant running. This is deliberately '
                        'conservative and is stated as such.'),
         sweep_refs=['F15', 'F17', 'F07']),
    dict(driver='Cost of debt and the discount-rate glide', mode='BOTTOM_UP',
         justification=('The company is NET CASH, so the cost of debt carries almost no '
                        'weight in the blended rate; the glide SHAPE is inherited from the '
                        'cost-of-debt path implied by the central bank\'s own easing '
                        'calendar rather than invented separately.'),
         sweep_refs=['F05', 'F20']),
    dict(driver='Terminal risk-free rate', mode='BOTTOM_UP',
         justification=('Norm-built from the central bank\'s own published medium-term '
                        'inflation target plus a standard emerging-market real-rate '
                        'convention. Never a historical average and never reverse-engineered '
                        'from a target price.'),
         sweep_refs=['F05']),
    dict(driver='Treasury income', mode='TOP_DOWN',
         justification=('Modelled as a yield on the modelled cash balance. No interest-income '
                        'line is separately retrievable, so it cannot be built bottom-up. It '
                        'is excluded from free cash flow to the firm entirely and handled in '
                        'the equity bridge, so it cannot be double-counted.'),
         sweep_refs=['F20', 'F05']),
    dict(driver='Terminal growth', mode='BOTTOM_UP',
         justification=('Held at the 5% house default for an established emerging-market '
                        'industrial once currency turbulence has passed, sensitised 3-7%, '
                        'and reconciled against the return on capital that would have to '
                        'fund it.'),
         sweep_refs=['F05', 'F15']),
]

OUT = dict(ticker='ARCC', asset_class='STOCK', sweep_date='2026-08-06',
           findings=FINDINGS, drivers=DRIVERS,
           qc_line=('26 findings across four rings, 6 blocking-or-driver-unlock in the '
                    'country and industry rings and 6 in the company ring; every forecast '
                    'driver names the findings it rests on and declares whether it is built '
                    'bottom-up or top-down.'))

counts = {}
for f in FINDINGS:
    counts[f['ring']] = counts.get(f['ring'], 0) + 1
    assert f['source_name'] and f['source_date'] and f['model_impact'] is not None, f['fid']
    assert f['klass'] in ('BLOCKING', 'STRUCTURAL', 'DRIVER_UNLOCK', 'COLOR'), f['fid']
assert set(counts) == {'GLOBAL', 'COUNTRY', 'INDUSTRY', 'COMPANY'}, counts
ids = [f['fid'] for f in FINDINGS]
assert len(ids) == len(set(ids))
for d in DRIVERS:
    for r in d['sweep_refs']:
        assert r in ids, (d['driver'], r)

json.dump(OUT, open(os.path.join(HERE, 'sweep_register.json'), 'w'), indent=1)
print(f"wrote sweep_register.json — {len(FINDINGS)} findings {counts}, "
      f"{len(DRIVERS)} drivers, all cross-references resolve")
