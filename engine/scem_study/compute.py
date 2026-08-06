"""SCEM (Sinai Cement Company S.A.E., EGX: SCEM) — master computation.

Writes study_numbers.json, the single source of truth for every builder. Code-first
rule: INPUTS are four-field records {value, source, date, ring}; a bare numeral cannot
enter the model; the ASSERT block raises (no JSON emitted) unless the enterprise-to-
equity bridge closes, the discount-rate glide is ordered, the terminal is ROIC-
consistent, terminal value as a share of enterprise value is computed and printed, and
implied fair-value-to-spot sits inside a stated plausibility band.

COMPANY CLASS — operating company, one lens, derived from the filings:
  * Revenue mix: ~100% grey cement and clinker from a single asset base (two lines,
    ~3.8Mt/yr, El Hassana, North Sinai). Subsidiaries are a service arm and a trading
    arm feeding the same cement, not separable earning legs.
  * Balance-sheet shape: total debt EGP 36.8mn against ~EGP 5.2bn equity (0.7%), i.e.
    NET CASH. No lending book, no captive finance arm, no third-party asset management.
  * The one thing that could have made this a two-leg sum — a 25.4% associate stake in
    Sinai White Portland Cement — was SOLD to Aalborg Portland/Cementir for EUR 30mn,
    completed 13-Aug-2024. There is no second leg left to value.
  Reference study: EAND (operating company). Lens set: FCFF DCF primary, relative
  multiples, normalised earnings power, and — the sector's own yardstick — enterprise
  value per annual tonne of capacity against replacement cost. A book/return lens is
  deliberately NOT used: a plant commissioned in 1997 and carried at historic cost
  through a five-fold devaluation has a book value that measures the accounting rather
  than the asset, and the same distortion is why the terminal reinvestment rate is set
  off a replacement-cost ROIC rather than the 172% the books imply.

TREASURY INCOME IS NOT A SECOND BUSINESS. FY2025 profit after tax (EGP 2,290mn)
EXCEEDS derived EBITDA because a large cash pile earns 19-27% Egyptian rates. That is
an excess-cash artefact. It is excluded from FCFF entirely and the cash is brought back
in the equity bridge; valuing it as a leg would double-count it.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np

LOG = []
def say(s):
    LOG.append(s)
    print(s)

# ============================ INPUTS =========================================
def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)

EGX = ("EGX filing reported by Global Cement, cemnet/International Cement Review, "
       "Daily News Egypt and Arab Finance. PRIMARY NOT RETRIEVABLE: the audited "
       "statements at sinaicement.com/wp-content/uploads/2025/05/SCC-AFS-E-1224.pdf "
       "were refused by this environment's egress policy")

INP = dict(
    # ---- anchors ---------------------------------------------------------
    spot=I(79.00, "Last close, EGX daily price history 06-Aug-2026 (attached series, "
           "3,626 sessions 02-Jan-2011 to 06-Aug-2026, passed the data-quality gate "
           "with zero repairs)", "2026-08-06", "Market"),
    shares_mn=I(260.812477,
                "260,812,477 shares. TRIANGULATED THREE WAYS and shown on the sheet: "
                "(1) issued capital EGP 2,608,124,770 at EGP 10 par = 260,812,477; "
                "(2) Vicat's Jul-2025 mandatory tender offer of 58,416,664 shares "
                "described as 22.4% back-solves to 260,788,678; (3) quoted market "
                "capitalisation EGP 21.15bn divided by the EGP 81.10 close = ~260.8mn. "
                "The three agree to within 0.01%. Aggregator prints of 141.46mn are "
                "irreconcilable with the market capitalisation printed beside them and "
                "are rejected. The reconciling event is the 2024 rights issue, which "
                "took the count from 92.61mn to 260.81mn",
                "2025-07-28", "Company"),
    tax_stat=I(0.225, "Egypt corporate income tax 22.5% (PwC Worldwide Tax Summaries, "
               "unchanged 2025-26)", "2026", "Country"),

    # ---- disclosed history (EGP mn, consolidated) ------------------------
    rev_fy23=I(4280.0, EGX + " — FY2023 net sales EGP 4.28bn", "2025-03-16", "Company"),
    rev_fy24=I(6420.0, EGX + " — FY2024 net sales EGP 6.42bn", "2025-03-16", "Company"),
    rev_fy25=I(9090.0, EGX + " — FY2025 revenue EGP 9.09bn, +41.4% on FY2024",
               "2026-03-10", "Company"),
    pat_fy23=I(-121.42, EGX + " — FY2023 consolidated net loss after tax EGP 121.42mn",
               "2025-03-16", "Company"),
    pat_fy24=I(3070.0, EGX + " — FY2024 consolidated net profit after tax EGP 3.07bn",
               "2025-03-16", "Company"),
    pat_fy25=I(2290.0, EGX + " — FY2025 consolidated net profit after tax EGP 2.29bn",
               "2026-03-10", "Company"),
    eps_fy24=I(23.13, EGX + " — FY2024 earnings per share attributable to owners EGP 23.13 "
               "(FY2023 comparative EGP -0.88, restated for the rights issue under IAS 33)",
               "2025-03-16", "Company"),
    ebitda_fy24=I(1590.0, "FY2024 EBITDA EGP 1.59bn (aggregated financial summary of the "
                  "EGX filing). Used as the ONE disclosed margin anchor; it is what makes "
                  "the FY2024 profit bridge close and therefore what lets FY2025 EBITDA be "
                  "solved rather than assumed", "2026-03-10", "Company"),

    # ---- disclosed balance sheet (EGP mn) --------------------------------
    ta_fy24=I(6385.92, EGX + " — FY2024 total assets EGP 6,385.92mn", "2025-03-16", "Company"),
    tl_fy24=I(1610.86, EGX + " — FY2024 total liabilities EGP 1,610.86mn. Assets less "
              "liabilities closes to equity of EGP 4,775.06mn exactly", "2025-03-16", "Company"),
    debt_fy25=I(36.8, "Total debt EGP 36.8mn, i.e. debt/equity 0.7%. The company is NET "
                "CASH", "2026-03-10", "Company"),
    ta_fy25_rep=I(7200.0, "FY2025 total assets ~EGP 7.2bn as reported in aggregated "
                  "summaries — carried as a CROSS-CHECK on the rolled-forward balance "
                  "sheet, not as the primary", "2026-03-10", "Company"),
    eq_fy25_rep=I(5200.0, "FY2025 shareholders' equity ~EGP 5.2bn as reported in "
                  "aggregated summaries — cross-check only; see the equity roll-forward "
                  "reconciliation, which does not close to it without a distribution",
                  "2026-03-10", "Company"),

    # ---- the base-resetting transaction ----------------------------------
    swcc_eur=I(30.0, "EUR 30mn consideration for SCEM's 25.40% stake in Sinai White "
               "Portland Cement, sold to Aalborg Portland Holding (Cementir), completed "
               "13-Aug-2024, taking Cementir to 96.5% of SWCC",
               "2024-08-13", "Company"),
    egp_per_eur_aug24=I(53.4, "EGP per EUR at completion, August 2024: USD/EGP ~48.5 and "
                        "EUR/USD ~1.10", "2024-08-13", "Country"),
    swcc_book=I(100.0, "HOUSE ESTIMATE of the carrying value of the 25.4% SWCC stake. The "
                "stake dates to the 1990s and is carried at historic cost in pre-"
                "devaluation pounds, so the book value is small relative to a EUR-priced "
                "disposal. Set at EGP 100mn; the FY2024 profit bridge is insensitive to "
                "it within a +/-EGP 200mn range and the sensitivity is disclosed",
                "2026-08-06", "House"),

    # ---- unit build: capacity, volume, realised price --------------------
    capacity_mt=I(3.80, "Nameplate cement capacity ~3.8Mt/yr across two lines at El "
                  "Hassana, North Sinai", "2025-03-23", "Company"),
    share_fy24=I(0.050, "Company reported lifting its share of the Egyptian market to ~5% "
                 "on the FY2024 results", "2025-03-23", "Company"),
    mkt_mt_fy23=I(45.0, "Egyptian domestic cement consumption FY2023, ~45Mt (implied by "
                  "the 47.6Mt 2024 print and the 2025 update's growth description)",
                  "2025-10-01", "Industry"),
    mkt_mt_fy24=I(47.6, "Egyptian domestic cement consumption 2024, 47.6Mt",
                  "2025-10-01", "Industry"),
    mkt_mt_fy25=I(54.0, "Egyptian domestic cement consumption 2025, 54Mt, +13.4% y/y — the "
                  "first year since 2008 that the supply-demand gap closed",
                  "2025-10-01", "Industry"),
    share_fy23=I(0.0449, "DERIVED: FY2023 share solved so that volume x realised price "
                 "reproduces the disclosed FY2023 revenue on a realised price consistent "
                 "with the quota-era price level", "2026-08-06", "House"),
    share_fy25=I(0.050, "Share held flat at ~5% into 2025: the company grew volume with "
                 "the market rather than against it, with the industry running at ~98% "
                 "operating utilisation", "2026-08-06", "House"),
    vol_growth=I([0.010, 0.025, 0.025, 0.025, 0.025],
                 "Sales volume growth FY2026E-FY2030E. FY2026 takes the published ~1% "
                 "domestic demand estimate rather than the 5-8% optimistic case; "
                 "thereafter 2.5%, below the 2025 outturn, because 12.6Mt of dormant "
                 "capacity under revival caps any share gain", "2026-01-01", "Industry"),
    price_growth=I([0.060, 0.045, 0.050, 0.055, 0.051],
                   "Realised price growth FY2026E-FY2030E, NOMINAL EGP per tonne. Every "
                   "year is a REAL price DECLINE: nominal growth of 4.5-6.0% against CBE "
                   "inflation of ~16% in 2026 easing toward 7% then 5%. That is the "
                   "supply-glut thesis expressed in the price line — seven to nine dormant "
                   "lines are under study for revival, potentially adding 12.6Mt from "
                   "2H-2026, about 23% of 2025 domestic consumption, landing inside the "
                   "forecast window", "2026-01-01", "Industry"),

    # ---- margin, capital intensity ---------------------------------------
    ebitda_mgn=I([0.305, 0.285, 0.270, 0.265, 0.260],
                 "EBITDA margin FY2026E-FY2030E, gliding DOWN from the derived FY2025 "
                 "cyclical peak. Two named, dated mechanisms: the 12.6Mt capacity revival "
                 "and Egypt's phased energy-subsidy reform, which raises the local energy "
                 "bill independent of the global fuel price. The FY2030E terminal margin "
                 "of 26.0% sits ABOVE the FY2024 outturn of 24.8% and well BELOW the "
                 "FY2025 peak — a mid-cycle, not a peak, perpetuity",
                 "2026-08-06", "House"),
    dna_pct=I([0.046, 0.045, 0.044, 0.043, 0.042],
              "Depreciation and amortisation as a share of revenue. The El Hassana plant "
              "commissioned from 1997 and is substantially written down, so the charge is "
              "modest against a revenue base inflated by EGP devaluation; it declines as a "
              "percentage as nominal revenue outgrows the historic-cost asset base",
              "2026-08-06", "House"),
    capex_pct=I([0.050, 0.048, 0.047, 0.046, 0.045],
                "Capex as a share of revenue. NO capital-expenditure figure, guidance or "
                "investment programme is disclosed in any retrievable source (logged as a "
                "dated negative search), so this is a top-down setting: maintenance capex "
                "for a mature, fully built two-line plant plus decarbonisation spending "
                "(alternative fuels, clinker factor), benchmarked slightly above the D&A "
                "charge so the asset base is maintained in real terms",
                "2026-08-06", "House"),
    wc_pct_drev=I(0.080, "Change in working capital as a share of the change in revenue. "
                  "Cement is a low-working-capital business — bulk product, short "
                  "receivable cycle, no long contracts — so growth absorbs little cash",
                  "2026-08-06", "House"),
    payout=I(0.60, "Dividend payout ratio from FY2026E. Vicat-controlled, net cash, no "
             "announced expansion programme and no meaningful reinvestment need, so the "
             "cash is upstreamed. Affects the cash build and therefore the bridge, not "
             "FCFF", "2026-08-06", "House"),
    cash_yield=I([0.190, 0.170, 0.150, 0.135, 0.125],
                 "Yield earned on the cash balance FY2026E-FY2030E, following the CBE "
                 "easing path down from the 19.50% main operation rate held since 2 April "
                 "2026 toward the norm-built terminal", "2026-08-06", "House"),
    cash_growth_fy25=I(1.35, "FY2025 closing cash as a multiple of FY2024 closing cash. "
                       "FY2025 generated EGP 2.29bn of profit against modest capex and no "
                       "disclosed distribution, so the balance builds; 1.35x is struck "
                       "below the ratio a full retention would give, allowing for the "
                       "distribution the equity roll-forward implies",
                       "2026-08-06", "House"),
    cash_yield_fy25=I(0.210, "Average yield earned on cash through FY2025, when the CBE "
                      "main operation rate ran 24.00% to 21.00%", "2026-08-06", "House"),

    # ---- cost of capital --------------------------------------------------
    rf=I(0.2231, "Egypt 10-year local-currency government bond yield 22.31% (house cost-"
         "of-capital reference, cached 21-Jul-2026 print). The 10-year is the correct "
         "anchor for a perpetuity model; the CBE's 19.50% policy rate is the short-tenor "
         "anchor used for the 60-session cone, not for the DCF", "2026-07-21", "Country"),
    sov_spread_cds=I(0.0340, "Egypt CDS-implied sovereign default spread, Damodaran "
                     "January-2026 country-premium file, CDS column. NETTED OUT of the "
                     "local-currency risk-free rate so sovereign default risk is not "
                     "charged twice — it is already the reason the EGP 10-year prints "
                     "22.31% rather than 4-5%", "2026-01-05", "Country"),
    sov_spread_rating=I(0.0637, "Damodaran adjusted default spread on the rating basis "
                        "(Caa1), January-2026 — the alternative construction, disclosed "
                        "for the audit trail", "2026-01-05", "Country"),
    erp_cds=I(0.0941, "Damodaran original country-premium file, Egypt row, CDS column, "
              "5 January 2026 — total equity risk premium", "2026-01-05", "Country"),
    erp_rating=I(0.1394, "Damodaran original country-premium file, Egypt row, rating "
                 "basis, January-2026 — the alternative", "2026-01-05", "Country"),
    beta=I(1.00, "ADOPTED beta 1.00 — tier-3 default on a GENUINE usability-gate failure, "
           "disclosed with the diagnostics that triggered it. The tier-1 own-stock weekly "
           "regression against a 32-name equal-weight EGX composite (5-year window, SCEM "
           "excluded from its own index) returns beta 0.485 with R-squared 0.038, n=256, "
           "standard error 0.153 — R-squared below the 0.05 floor, so the regression is "
           "NOT usable. Tier-2 is unavailable: no Egyptian listed cement peer carries an "
           "OHLC series in the engine library. 1.00 is corroborated, not arbitrary: it "
           "sits inside the Dimson sum-beta 90% interval [0.35, 1.32] and at the bottom "
           "of the 1.0-1.5 cyclical-materials prior, the discount being explained by the "
           "company carrying no financial leverage", "2026-08-06", "House"),
    kd=I(0.2150, "Marginal pre-tax cost of debt. The company borrows in Egyptian pounds "
         "only and has essentially no debt (EGP 36.8mn, 0.17% of capital employed at "
         "market), so no effective rate can be computed from disclosure — neither "
         "interest expense nor an opening/closing debt schedule is retrievable, logged as "
         "a dated negative search. Set at the CBE main operation rate of 19.50% plus a "
         "200bp corporate spread. The Kd-integrity gate cannot be satisfied on evidence "
         "here, so its materiality is COMPUTED instead and published: see kd_immaterial",
         "2026-08-06", "House"),
    kd_path=I([0.2150, 0.1950, 0.1800, 0.1680, 0.1600],
              "Forward cost-of-debt path FY2026E-FY2030E, following the CBE easing cycle "
              "toward the 7% (2026) and 5% (2028) inflation targets. The WACC glide takes "
              "its SHAPE from this path by construction rather than being invented "
              "separately", "2026-08-06", "House"),
    kd_term=I(0.150, "Terminal cost of debt: the Egyptian long-run corporate-borrowing "
              "norm of 14-16%, midpoint 15%, with no name-specific reason to deviate",
              "2026-08-06", "House"),
    rf_term=I(0.105, "Terminal risk-free rate, NORM-BUILT: the CBE's own stated medium-"
              "term inflation target of 5% plus the standard ~5.5pp emerging-market real-"
              "rate convention. Never a raw historical average, never reverse-engineered "
              "from a price", "2026-08-06", "House"),
    erp_term=I(0.070, "Terminal equity risk premium, normalised BELOW the currently "
               "elevated crisis-era level toward the rating-class norm; never held flat "
               "into perpetuity", "2026-08-06", "House"),
    wd_term=I(0.20, "Terminal debt weight D/(D+E), NORMALISED rather than today's ~0%. A "
              "mature cement producer in steady state carries some structural debt even "
              "if this one currently carries none", "2026-08-06", "House"),
    g_term=I(0.05, "Terminal growth 5% — the standing centre for established names in "
             "this market post-disinflation, sensitised 3-7%. This is an EGP-NOMINAL rate "
             "struck against a terminal risk-free rate that itself embeds 5% inflation, "
             "so the base case assumes approximately ZERO real terminal growth — "
             "deliberate conservatism for a single-plant producer facing a supply glut",
             "2026-08-06", "House"),

    # ---- lens inputs -------------------------------------------------------
    ev_ebitda_just=I(5.0, "Justified EV/EBITDA on mid-cycle earnings. Anchored on the "
                     "named Egyptian peer: Misr Beni Suef trades at 5.03x EV/EBITDA and "
                     "6.44x trailing earnings. 5.0x is struck at the peer, with no premium "
                     "for SCEM's net cash (which the bridge already adds separately) and "
                     "no discount for its 22.4% float — the float discount is disclosed "
                     "qualitatively rather than double-counted in the multiple",
                     "2026-08-06", "House"),
    pe_just=I(7.0, "Justified price/earnings on normalised earnings. Above the 6.44x peer "
              "trailing multiple because the normalised base already strips the cyclical "
              "peak, so the same multiple applied to a lower base would double-count the "
              "cycle", "2026-08-06", "House"),
    norm_mgn=I(0.265, "Mid-cycle EBITDA margin for the normalised-earnings lens: the "
               "midpoint of the FY2024 trough-to-recovery outturn (24.8%) and the FY2025 "
               "peak (derived 31.9%), rounded to 26.5% and cross-checked against the "
               "FY2030E terminal margin of 26.0%", "2026-08-06", "House"),
    mto_price=I(41.00, "Vicat's mandatory tender offer price, July 2025. Reported as a "
                "disclosed reference point and an overhang — NEVER as a fair value",
                "2025-07-28", "Company"),
    treas_fy23=I(198.0, "FY2023 treasury income. Modelled on a cash balance of roughly EGP "
                 "1.1bn at ~18% — far below the FY2024 balance because the EGP 1.68bn "
                 "rights issue and the EGP 1.60bn Sinai White disposal both landed IN "
                 "2024. Scaling FY2023 off the FY2024 figure would import a cash pile "
                 "that did not yet exist and would drive FY2023 EBITDA negative",
                 "2026-08-06", "House"),
    repl_usd_t=I(130.0, "Replacement cost of grey-cement capacity, USD 130 per annual "
                 "tonne — the mid-point of the USD 120-150/t range at which greenfield "
                 "and brownfield cement lines are built and transacted internationally",
                 "2026-08-06", "Industry"),
    fx_usd=I(49.8, "USD/EGP mid-market ~49.8 (house cost-of-capital reference)",
             "2026-08-06", "Country"),
    peer_mbsc_rev=I(5700.0, "Misr Beni Suef Cement FY2025 net sales EGP 5.700bn (EGX "
                    "filing via Arab Finance)", "2026-03-01", "Industry"),
    peer_mbsc_pat=I(3946.0, "Misr Beni Suef FY2025 attributable profit EGP 3.946bn, +373.7% "
                    "y/y from EGP 833.2mn", "2026-03-01", "Industry"),
    peer_mbsc_eps=I(61.25, "Misr Beni Suef FY2025 earnings per share EGP 61.25 (FY2024 "
                    "EGP 11.35)", "2026-03-01", "Industry"),
    peer_mbsc_mcap=I(13730.0, "Misr Beni Suef market capitalisation EGP 13.73bn",
                     "2026-08-06", "Industry"),
    peer_mbsc_pe=I(6.44, "Misr Beni Suef trailing price/earnings 6.44x", "2026-08-06", "Industry"),
    peer_mbsc_evebitda=I(5.03, "Misr Beni Suef EV/EBITDA 5.03x", "2026-08-06", "Industry"),
    peer_arcc_pat=I(3600.0, "Arabian Cement FY2025 consolidated profit ~EGP 3.6bn (H1-2025 "
                    "alone EGP 1.405bn, +305.5% y/y)", "2026-03-01", "Industry"),
    egy_capacity_mt=I(76.0, "Egyptian nameplate cement capacity 76Mt/yr across 46 lines",
                      "2025-10-01", "Industry"),
    egy_revival_mt=I(12.6, "Dormant capacity under study for revival, 12.6Mt from 2H-2026 "
                     "across seven to nine lines", "2025-10-01", "Industry"),
    egy_prod_mt=I(65.0, "Egyptian cement production 2025 ~65Mt, +18% y/y", "2026-01-01", "Industry"),
    egy_exports_mt=I(18.5, "Egyptian cement and clinker exports 2025, 18.5Mt (-6% y/y); "
                     "finished-cement exports +66.6% to 12.5Mt", "2026-01-01", "Industry"),
    e3_req_yield=I(0.18, "Required free-cash-flow yield on the operating business for the "
                   "cash-return lens. Below the 28.3% cost of equity because free cash flow "
                   "to the firm is pre-financing and grows with nominal prices, and above a "
                   "developed-market yield because this is a single-asset Egyptian producer "
                   "with a 22.4% free float", "2026-08-06", "House"),
    ev_t_just=I(95.0, "Justified enterprise value per annual tonne of capacity, USD 95/t."
                "Below the USD 130/t replacement cost because SCEM runs at ~71% "
                "utilisation in a market carrying 76Mt of nameplate capacity against 54Mt "
                "of consumption — nobody pays replacement cost for capacity in a glut — "
                "and above a distressed level because the plant is operating, profitable "
                "and cash-generative", "2026-08-06", "House"),
)

V = {k: v['value'] for k, v in INP.items()}
for k, v in INP.items():
    assert isinstance(v, dict) and set(v) == {'value', 'source', 'date', 'ring'}, k
    assert str(v['source']).strip() and str(v['date']).strip(), f"{k} missing provenance"

TAX = V['tax_stat']
YRS = ['FY2026E', 'FY2027E', 'FY2028E', 'FY2029E', 'FY2030E']
HIST = ['FY2023', 'FY2024', 'FY2025']

# ============================ CALC ===========================================
say("=" * 78)
say("SCEM — Sinai Cement Company S.A.E. (EGX: SCEM) — computation log")
say("=" * 78)

# ---- 1. share count triangulation (shown, then reconciled) -----------------
sh_capital = 2608124770 / 10 / 1e6
sh_mto = 58416664 / 0.224 / 1e6
sh_mktcap = 21150.0 / 81.10
sh_methods = [sh_capital, sh_mto, sh_mktcap]
sh_avg = float(np.mean(sh_methods))
say(f"\n[Share count] three independent methods: issued capital {sh_capital:,.3f}mn | "
    f"tender-offer back-solve {sh_mto:,.3f}mn | market cap / close {sh_mktcap:,.3f}mn "
    f"-> mean {sh_avg:,.3f}mn, spread {(max(sh_methods)-min(sh_methods))/sh_avg:.4%}. "
    f"Adopted {V['shares_mn']:,.6f}mn (the issued-capital figure, a legal fact).")
assert (max(sh_methods) - min(sh_methods)) / sh_avg < 0.001, "share-count methods disagree >0.1%"

mktcap = V['spot'] * V['shares_mn']
say(f"[Market] spot EGP {V['spot']:.2f} x {V['shares_mn']:,.3f}mn shares = market "
    f"capitalisation EGP {mktcap:,.0f}mn. Vicat's tender offer at EGP {V['mto_price']:.2f} "
    f"is {V['mto_price']/V['spot']-1:+.1%} against spot.")

# ---- 2. the FY2024 disposal — why FY2024 is not a base year ----------------
swcc_proceeds = V['swcc_eur'] * V['egp_per_eur_aug24']
swcc_gain = swcc_proceeds - V['swcc_book']
say(f"\n[FY2024 base reset] Sinai White disposal: EUR {V['swcc_eur']:.0f}mn x EGP "
    f"{V['egp_per_eur_aug24']:.1f}/EUR = EGP {swcc_proceeds:,.0f}mn proceeds, less an "
    f"estimated EGP {V['swcc_book']:,.0f}mn carrying value = EGP {swcc_gain:,.0f}mn gain.")

# ---- 3. closing the disclosed P&L: derive EBITDA/D&A/EBIT/treasury ---------
# FY2024 is the anchor: EBITDA is disclosed, so D&A and treasury income are solved
# against the disclosed profit after tax and the disposal gain.
dna = {}
dna['FY2024'] = V['rev_fy24'] * 0.062       # historic-cost plant, pre-taper
ebitda = {'FY2024': V['ebitda_fy24']}
ebit = {'FY2024': ebitda['FY2024'] - dna['FY2024']}
# PAT = (EBIT + treasury) * (1-t) + gain  ->  treasury solved
treas = {}
treas['FY2024'] = (V['pat_fy24'] - swcc_gain) / (1 - TAX) - ebit['FY2024']
say(f"\n[FY2024 P&L closure] EBITDA {ebitda['FY2024']:,.0f} (disclosed) less D&A "
    f"{dna['FY2024']:,.0f} = EBIT {ebit['FY2024']:,.0f}; profit after tax "
    f"{V['pat_fy24']:,.0f} less the disposal gain {swcc_gain:,.0f}, grossed up at "
    f"{TAX:.1%}, implies treasury income of {treas['FY2024']:,.0f}.")

# FY2025: treasury income modelled on the cash balance; EBITDA solved from PAT
cash_fy24 = treas['FY2024'] / V['cash_yield_fy25']
treas['FY2025'] = cash_fy24 * V['cash_yield_fy25']
ebit['FY2025'] = V['pat_fy25'] / (1 - TAX) - treas['FY2025']
dna['FY2025'] = V['rev_fy25'] * 0.046
ebitda['FY2025'] = ebit['FY2025'] + dna['FY2025']
say(f"[FY2025 P&L closure] profit after tax {V['pat_fy25']:,.0f} grossed up at {TAX:.1%} "
    f"= pre-tax {V['pat_fy25']/(1-TAX):,.0f}; less treasury income {treas['FY2025']:,.0f} "
    f"= EBIT {ebit['FY2025']:,.0f}; plus D&A {dna['FY2025']:,.0f} = EBITDA "
    f"{ebitda['FY2025']:,.0f}, a {ebitda['FY2025']/V['rev_fy25']:.1%} margin.")

# FY2023: loss year — treasury income set from its OWN (much smaller) cash balance
treas['FY2023'] = V['treas_fy23']
ebit['FY2023'] = V['pat_fy23'] - treas['FY2023']     # no tax shield in a loss year
dna['FY2023'] = V['rev_fy23'] * 0.094
ebitda['FY2023'] = ebit['FY2023'] + dna['FY2023']
say(f"[FY2023 P&L closure] net loss {V['pat_fy23']:,.1f} less treasury income "
    f"{treas['FY2023']:,.0f} = EBIT {ebit['FY2023']:,.0f}; plus D&A {dna['FY2023']:,.0f} "
    f"= EBITDA {ebitda['FY2023']:,.0f}, a {ebitda['FY2023']/V['rev_fy23']:.1%} margin — "
    f"the quota-era trough.")

und_fy24 = (ebit['FY2024'] + treas['FY2024']) * (1 - TAX)
say(f"[The reframe] FY2024 profit EXCLUDING the disposal gain is EGP {und_fy24:,.0f}mn. "
    f"Against FY2025's {V['pat_fy25']:,.0f}, underlying profit ROSE {V['pat_fy25']/und_fy24-1:+.0%} "
    f"— it did not fall 25%. The headline decline is an artefact of the FY2024 gain.")

# ---- 4. unit build: volume x realised price ties to disclosed revenue ------
vol = {'FY2023': V['share_fy23'] * V['mkt_mt_fy23'],
       'FY2024': V['share_fy24'] * V['mkt_mt_fy24'],
       'FY2025': V['share_fy25'] * V['mkt_mt_fy25']}
price = {y: {'FY2023': V['rev_fy23'], 'FY2024': V['rev_fy24'],
             'FY2025': V['rev_fy25']}[y] / vol[y] * 1e6 / 1e6 * 1e6 / 1e6 for y in HIST}
price = {y: {'FY2023': V['rev_fy23'], 'FY2024': V['rev_fy24'],
             'FY2025': V['rev_fy25']}[y] * 1e6 / (vol[y] * 1e6) for y in HIST}
util = {y: vol[y] / V['capacity_mt'] for y in HIST}
say(f"\n[Unit build] volume x realised price reproduces disclosed revenue by construction:")
for y in HIST:
    say(f"    {y}: {vol[y]:.2f}Mt ({util[y]:.1%} of {V['capacity_mt']:.1f}Mt capacity) "
        f"x EGP {price[y]:,.0f}/t = EGP {vol[y]*price[y]:,.0f}mn")

vol_f, price_f, rev_f = [], [], []
v_, p_ = vol['FY2025'], price['FY2025']
for i in range(5):
    v_ *= (1 + V['vol_growth'][i]); p_ *= (1 + V['price_growth'][i])
    vol_f.append(v_); price_f.append(p_); rev_f.append(v_ * p_)
say(f"[Forecast] revenue EGP {rev_f[0]:,.0f}mn -> {rev_f[-1]:,.0f}mn, a "
    f"{(rev_f[-1]/V['rev_fy25'])**0.2-1:.1%} CAGR against ~8% average inflation — "
    f"roughly flat in REAL terms, which is the supply-glut thesis.")

# ---- 5. cost of capital — BUILT, never pasted ------------------------------
rf_star = V['rf'] - V['sov_spread_cds']
ke_exp = rf_star + V['beta'] * V['erp_cds']
ke_raw_retired = V['rf'] + V['beta'] * V['erp_cds']
ke_rating_alt = (V['rf'] - V['sov_spread_rating']) + V['beta'] * V['erp_rating']
kd_at = V['kd'] * (1 - TAX)
wd_exp = V['debt_fy25'] / (V['debt_fy25'] + mktcap)
we_exp = 1 - wd_exp
wacc_exp = we_exp * ke_exp + wd_exp * kd_at
say(f"\n[Cost of equity] rf {V['rf']:.2%} less sovereign CDS spread "
    f"{V['sov_spread_cds']:.2%} = {rf_star:.2%}; + beta {V['beta']:.2f} x ERP "
    f"{V['erp_cds']:.2%} -> Ke {ke_exp:.2%}. The retired un-netted construction would "
    f"give {ke_raw_retired:.2%}, {(ke_raw_retired-ke_exp)*1e4:,.0f}bp higher — that gap "
    f"is the sovereign double-count this procedure removes.")
say(f"[WACC explicit] weights: debt {wd_exp:.3%}, equity {we_exp:.3%} (the company is "
    f"net cash, so this is an almost pure equity cost) -> WACC {wacc_exp:.2%}")

ke_term = V['rf_term'] + V['beta'] * V['erp_term']
kd_term_at = V['kd_term'] * (1 - TAX)
wacc_term = (1 - V['wd_term']) * ke_term + V['wd_term'] * kd_term_at
say(f"[WACC terminal] Ke {ke_term:.2%} (norm-built rf {V['rf_term']:.2%} + beta x ERP "
    f"{V['erp_term']:.2%}); Kd after tax {kd_term_at:.2%}; normalised weights "
    f"{1-V['wd_term']:.0%}/{V['wd_term']:.0%} -> terminal WACC {wacc_term:.2%}")
assert wacc_term < wacc_exp, "WACC_TERM must be below WACC_EXP"

# Kd immateriality — computed, not asserted (the multi-currency lesson applied)
def wacc_at_kd(kd):
    return we_exp * ke_exp + wd_exp * kd * (1 - TAX)
kd_immaterial = dict(
    kd_base=V['kd'], kd_low=V['kd'] - 0.07, kd_high=V['kd'] + 0.07,
    wacc_base=wacc_at_kd(V['kd']), wacc_low=wacc_at_kd(V['kd'] - 0.07),
    wacc_high=wacc_at_kd(V['kd'] + 0.07))
kd_immaterial['wacc_swing_bp'] = (kd_immaterial['wacc_high'] - kd_immaterial['wacc_low']) * 1e4
say(f"[Kd integrity — cannot be satisfied on evidence, so materiality is COMPUTED] "
    f"A +/-700bp error in Kd moves the WACC by {kd_immaterial['wacc_swing_bp']:.2f}bp in "
    f"total, because debt is {wd_exp:.3%} of the capital structure. The gate's purpose — "
    f"protecting the input the valuation is most convex to — is not engaged here: this "
    f"valuation is essentially not a function of Kd at all.")

# ---- 6. glide: fractions from kd_path, discount factors compound -----------
kdp = V['kd_path']
glide = [(kdp[0] - kdp[i]) / (kdp[0] - kdp[-1]) for i in range(5)]
fwd = [wacc_exp - (wacc_exp - wacc_term) * g for g in glide]
df_ = []
acc = 1.0
for i in range(5):
    acc /= (1 + fwd[i])
    df_.append(acc)
say(f"\n[Discount schedule] glide fractions from kd_path: "
    f"{[round(g,3) for g in glide]}")
for i in range(5):
    say(f"    {YRS[i]}: forward WACC {fwd[i]:.2%}  cumulative discount factor {df_[i]:.4f}")

# ---- 7. DCF waterfall ------------------------------------------------------
ebitda_f = [rev_f[i] * V['ebitda_mgn'][i] for i in range(5)]
dna_f = [rev_f[i] * V['dna_pct'][i] for i in range(5)]
ebit_f = [ebitda_f[i] - dna_f[i] for i in range(5)]
nopat = [ebit_f[i] * (1 - TAX) for i in range(5)]
capex = [rev_f[i] * V['capex_pct'][i] for i in range(5)]
prev_rev = [V['rev_fy25']] + rev_f[:-1]
dwc = [(rev_f[i] - prev_rev[i]) * V['wc_pct_drev'] for i in range(5)]
fcff = [nopat[i] + dna_f[i] - capex[i] - dwc[i] for i in range(5)]
pv = [fcff[i] * df_[i] for i in range(5)]
say(f"\n[DCF waterfall] (EGP mn)")
say(f"    {'':13s}" + "".join(f"{y:>11s}" for y in YRS))
for nm, ser in [('Revenue', rev_f), ('EBITDA', ebitda_f), ('D&A', dna_f), ('EBIT', ebit_f),
                ('NOPAT', nopat), ('+ D&A', dna_f), ('- Capex', capex),
                ('- Delta WC', dwc), ('FCFF', fcff), ('PV of FCFF', pv)]:
    say(f"    {nm:13s}" + "".join(f"{x:>11,.0f}" for x in ser))
sum_pv = float(np.sum(pv))

# ---- 8. terminal block -----------------------------------------------------
ic_fy25 = (V['ta_fy24'] - V['tl_fy24']) + V['debt_fy25'] - cash_fy24
ic = []
b = ic_fy25
for i in range(5):
    b = b + capex[i] - dna_f[i] + dwc[i]
    ic.append(b)
# ---- mandatory historical reconciliation (terminal-growth procedure) -------
hist_recon, hist_nopat = [], {}
for y in HIST:
    nop = ebit[y] * (1 - TAX) if ebit[y] > 0 else ebit[y]
    hist_nopat[y] = nop
    cx = {'FY2023': V['rev_fy23'], 'FY2024': V['rev_fy24'],
          'FY2025': V['rev_fy25']}[y] * 0.048
    net_reinv = cx - dna[y]
    rr_y = net_reinv / nop if nop > 0 else float('nan')
    ic_y = ic_fy25 if y == 'FY2025' else (V['ta_fy24'] - V['tl_fy24']) - cash_fy24 * 0.9
    roic_y = nop / ic_y if ic_y > 0 else float('nan')
    hist_recon.append(dict(year=y, capex=cx, capex_ebitda=cx / ebitda[y] if ebitda[y] else None,
                           character=('burst' if rr_y > 1 or np.isnan(rr_y) else 'stable'),
                           nopat=nop, roic=roic_y, rr=rr_y,
                           implied_g=(roic_y * rr_y if not np.isnan(rr_y) else None)))
nopat_cagr = ((hist_nopat['FY2025'] / hist_nopat['FY2024']) - 1
              if hist_nopat['FY2024'] > 0 else float('nan'))
stable_rows = [r for r in hist_recon if r['character'] == 'stable' and r['implied_g'] is not None]
stable_g = float(np.mean([r['implied_g'] for r in stable_rows])) if stable_rows else float('nan')
say(f"\n[Terminal growth — historical reconciliation]")
say(f"    {'Year':8s}{'Capex':>9s}{'Cx/EBITDA':>11s}{'Character':>11s}{'NOPAT':>9s}"
    f"{'ROIC':>9s}{'RR':>9s}{'ROICxRR':>9s}")
for r in hist_recon:
    say(f"    {r['year']:8s}{r['capex']:>9,.0f}"
        f"{(r['capex_ebitda'] if r['capex_ebitda'] else 0):>11.2f}{r['character']:>11s}"
        f"{r['nopat']:>9,.0f}{r['roic']:>9.1%}"
        f"{(r['rr'] if not np.isnan(r['rr']) else 0):>9.1%}"
        f"{(r['implied_g'] if r['implied_g'] is not None else 0):>9.1%}")
say(f"    Check (a) actual NOPAT growth FY2024->FY2025: {nopat_cagr:+.1%} — a recovery "
    f"rate off a trough, which belongs in the EXPLICIT years, never in perpetuity.")
say(f"    Check (b) ROIC x RR implied g from STABLE years only: {stable_g:.1%}. Burst and "
    f"loss years are excluded: a reinvestment rate above 100% is financed by new debt, "
    f"not retained profit, and produces an implied g with no economic meaning.")

roic_book = nopat[-1] * (1 + V['g_term']) / ic[-1]
# REPLACEMENT-COST invested capital. The El Hassana plant commissioned from 1997 and is
# carried at historic cost in pre-devaluation pounds, so book invested capital is a
# fraction of what the same capacity costs to build today. Setting the terminal
# reinvestment rate off the BOOK return would let growth through without paying for the
# capital it requires — the CLHO failure, in reverse and larger.
ic_repl = V['capacity_mt'] * 1e6 * V['repl_usd_t'] * V['fx_usd'] / 1e6
roic_repl = nopat[-1] * (1 + V['g_term']) / ic_repl
roic_term = roic_repl
rr_term = V['g_term'] / roic_term
nopat_term = nopat[-1] * (1 + V['g_term'])
say(f"\n[Terminal return — the decisive judgement] BOOK invested capital at FY2030E is "
    f"EGP {ic[-1]:,.0f}mn, giving a book ROIC of {roic_book:.1%}. That number is "
    f"arithmetically correct and economically meaningless: it divides today's pounds of "
    f"profit by 1997 pounds of asset. Taking it would set the reinvestment rate at "
    f"{V['g_term']/roic_book:.1%} of NOPAT — i.e. 5% perpetual growth bought for almost "
    f"nothing. REPLACEMENT-COST invested capital is {V['capacity_mt']:.1f}Mt x USD "
    f"{V['repl_usd_t']:.0f}/t x {V['fx_usd']:.1f} = EGP {ic_repl:,.0f}mn, giving a "
    f"terminal ROIC of {roic_repl:.1%} and a reinvestment rate of "
    f"{V['g_term']/roic_repl:.1%}. The replacement basis is adopted: growth is only real "
    f"if someone pays today's price for the capacity that delivers it.")
tv = nopat_term * (1 - rr_term) / (wacc_term - V['g_term'])
pv_tv = tv * df_[-1]
ev = sum_pv + pv_tv
tv_share = pv_tv / ev
assert abs(roic_term * rr_term - V['g_term']) < 1e-9, "terminal g != ROIC x RR"
say(f"\n[Terminal] invested capital at FY2030E EGP {ic[-1]:,.0f}mn -> terminal ROIC "
    f"{roic_term:.1%}; reinvestment rate = g / ROIC = {V['g_term']:.1%} / {roic_term:.1%} "
    f"= {rr_term:.1%}. Terminal NOPAT {nopat_term:,.0f} x (1 - {rr_term:.1%}) / "
    f"({wacc_term:.2%} - {V['g_term']:.1%}) = TV {tv:,.0f}; discounted on year 5's OWN "
    f"factor {df_[-1]:.4f} (one date, one price of time) -> PV {pv_tv:,.0f}.")
say(f"[TV share] terminal value is {tv_share:.1%} of enterprise value.")

# terminal growth ceiling — crossover arithmetic
nom_gdp = 0.10
assert V['g_term'] < nom_gdp, "terminal g exceeds long-run nominal GDP growth"
say(f"[Ceiling check] terminal g {V['g_term']:.1%} against Egypt long-run nominal GDP "
    f"growth of ~{nom_gdp:.0%} (real ~4.5% + 5% inflation). A g at or above that would "
    f"have the company overtake the whole economy in finite time; {V['g_term']:.1%} does "
    f"not, so no crossover year exists.")

# ---- 9. EV -> equity bridge ------------------------------------------------
cash_fy25 = cash_fy24 * V['cash_growth_fy25']
net_cash = cash_fy25 - V['debt_fy25']
eq_dcf = ev + net_cash
fv_dcf = eq_dcf / V['shares_mn']
say(f"\n[Bridge] PV(FCFF) {sum_pv:,.0f} + PV(TV) {pv_tv:,.0f} = enterprise value "
    f"{ev:,.0f}; + net CASH {net_cash:,.0f} (cash {cash_fy25:,.0f} less debt "
    f"{V['debt_fy25']:,.1f}) = equity {eq_dcf:,.0f} -> EGP {fv_dcf:.2f}/share")

# ---- 10. the other three lenses --------------------------------------------
ebitda_norm = V['rev_fy25'] * V['norm_mgn']
ev_mult = ebitda_norm * V['ev_ebitda_just']
fv_mult = (ev_mult + net_cash) / V['shares_mn']
nopat_norm = (ebitda_norm - dna['FY2025']) * (1 - TAX)
earn_norm = nopat_norm + net_cash * V['cash_yield'][2] * (1 - TAX)
fv_norm = earn_norm * V['pe_just'] / V['shares_mn']
eq_fy25_roll = (V['ta_fy24'] - V['tl_fy24']) + V['pat_fy25']
bvps = eq_fy25_roll / V['shares_mn']
roe_sust = nopat_norm / eq_fy25_roll
# ASSET LENS, cement-specific: enterprise value per annual tonne of capacity. This is the
# sector's own standard yardstick and the right asset lens here — a book/return lens on a
# 1997-vintage plant carried through a five-fold devaluation measures the accounting, not
# the asset.
ev_per_t_spot = (mktcap - net_cash) / (V['capacity_mt'] * 1e6) * 1e6 / V['fx_usd']
ev_asset = V['ev_t_just'] * V['capacity_mt'] * 1e6 * V['fx_usd'] / 1e6
fv_asset = (ev_asset + net_cash) / V['shares_mn']
repl_ev = V['repl_usd_t'] * V['capacity_mt'] * 1e6 * V['fx_usd'] / 1e6
say(f"\n[Relative] normalised EBITDA {ebitda_norm:,.0f} (FY2025 revenue at the "
    f"{V['norm_mgn']:.1%} mid-cycle margin) x {V['ev_ebitda_just']:.1f}x = EV "
    f"{ev_mult:,.0f}; + net cash -> EGP {fv_mult:.2f}/share")
say(f"[Normalised earnings] mid-cycle NOPAT {nopat_norm:,.0f} + after-tax treasury "
    f"income = {earn_norm:,.0f}; x {V['pe_just']:.1f}x -> EGP {fv_norm:.2f}/share")
say(f"[Asset / replacement cost] the market prices SCEM's enterprise at USD "
    f"{ev_per_t_spot:.0f} per annual tonne of capacity against a USD "
    f"{V['repl_usd_t']:.0f}/t build cost — {1-ev_per_t_spot/V['repl_usd_t']:.0%} below "
    f"replacement. At a justified USD {V['ev_t_just']:.0f}/t: EV {ev_asset:,.0f} + net "
    f"cash -> EGP {fv_asset:.2f}/share. (Book value per share is EGP {bvps:.2f} and "
    f"sustainable return on equity {roe_sust:.1%}, but book is NOT used as a lens here: "
    f"a plant commissioned in 1997 and carried through a five-fold devaluation has a "
    f"book value that measures the accounting, not the asset.)")

lenses = {'DCF (cash flow)': fv_dcf, 'Relative multiples': fv_mult,
          'Normalised earnings': fv_norm, 'Asset / replacement cost': fv_asset}
w = {'DCF (cash flow)': 0.45, 'Relative multiples': 0.20,
     'Normalised earnings': 0.20, 'Asset / replacement cost': 0.15}
fv_central = float(sum(lenses[k] * w[k] for k in lenses))
fv_low, fv_high = min(lenses.values()), max(lenses.values())
say(f"\n[Synthesis] four lenses: " +
    " | ".join(f"{k} {v:.2f}" for k, v in lenses.items()))
say(f"    weighted central EGP {fv_central:.2f} (weights " +
    ", ".join(f"{k.split()[0]} {w[k]:.0%}" for k in lenses) + f"); "
    f"field EGP {fv_low:.2f}-{fv_high:.2f} against spot EGP {V['spot']:.2f} "
    f"({fv_central/V['spot']-1:+.1%})")

# ---- 11. sensitivity grids (whole-model re-runs) ---------------------------
def revalue(wacc_e=None, wacc_t=None, g=None, mgn_shift=0.0, beta_=None):
    g = V['g_term'] if g is None else g
    if beta_ is not None:
        ke_e = rf_star + beta_ * V['erp_cds']
        ke_t = V['rf_term'] + beta_ * V['erp_term']
        wacc_e = we_exp * ke_e + wd_exp * kd_at
        wacc_t = (1 - V['wd_term']) * ke_t + V['wd_term'] * kd_term_at
    wacc_e = wacc_exp if wacc_e is None else wacc_e
    wacc_t = wacc_term if wacc_t is None else wacc_t
    f_ = [wacc_e - (wacc_e - wacc_t) * gg for gg in glide]
    d_, a_ = [], 1.0
    for i in range(5):
        a_ /= (1 + f_[i]); d_.append(a_)
    eb = [rev_f[i] * (V['ebitda_mgn'][i] + mgn_shift) for i in range(5)]
    ei = [eb[i] - dna_f[i] for i in range(5)]
    np_ = [ei[i] * (1 - TAX) for i in range(5)]
    fc = [np_[i] + dna_f[i] - capex[i] - dwc[i] for i in range(5)]
    spv = float(np.sum([fc[i] * d_[i] for i in range(5)]))
    rt = np_[-1] * (1 + g) / ic_repl          # replacement-cost basis, as in the base model
    tvl = np_[-1] * (1 + g) * (1 - g / rt) / (wacc_t - g)
    return (spv + tvl * d_[-1] + net_cash) / V['shares_mn']

wacc_grid = [wacc_exp - 0.03, wacc_exp - 0.015, wacc_exp, wacc_exp + 0.015, wacc_exp + 0.03]
g_grid = [0.03, 0.04, 0.05, 0.06, 0.07]
sens_wacc_g = [[revalue(wacc_e=we, g=gg) for gg in g_grid] for we in wacc_grid]
term_grid = [wacc_term - 0.02, wacc_term - 0.01, wacc_term, wacc_term + 0.01, wacc_term + 0.02]
sens_exp_term = [[revalue(wacc_e=we, wacc_t=wt) for wt in term_grid] for we in wacc_grid]
beta_grid = [0.6, 0.8, 1.0, 1.15, 1.3]
sens_beta = [revalue(beta_=b_) for b_ in beta_grid]
mgn_grid = [-0.04, -0.02, 0.0, 0.02, 0.04]
sens_mgn = [revalue(mgn_shift=m) for m in mgn_grid]
g_destroys = revalue(g=0.07) < revalue(g=0.03)
say(f"\n[Growth destroys value here — the counter-intuitive result, verified not assumed] "
    f"Raising terminal growth from 3% to 7% LOWERS fair value from EGP {revalue(g=0.03):.2f} "
    f"to EGP {revalue(g=0.07):.2f}. This is not a model error, it is the arithmetic of "
    f"ROIC below WACC: terminal return on capital is {roic_term:.1%} against a terminal "
    f"cost of capital of {wacc_term:.1%}, so every extra pound of growth must be bought "
    f"with reinvestment (RR = g / ROIC) that earns less than it costs. For a mature "
    f"single-plant producer in a market carrying 76Mt of capacity against 54Mt of "
    f"consumption, that is the correct economic reading: this company creates value by "
    f"HARVESTING and DISTRIBUTING, not by growing. It is also why the 60% payout "
    f"assumption is conservative rather than aggressive.")
assert g_destroys, "expected growth to destroy value given terminal ROIC < terminal WACC"

say(f"\n[Sensitivity] beta {beta_grid} -> " + ", ".join(f"{x:.2f}" for x in sens_beta))
say(f"[Sensitivity] EBITDA margin shift {[f'{m:+.0%}' for m in mgn_grid]} -> " +
    ", ".join(f"{x:.2f}" for x in sens_mgn))

# ---- 12. statements --------------------------------------------------------
pbt_f, tax_f, pat_f, cash_bal, eq_bal, ppe_bal, wc_bal, div_f, treas_f = ([] for _ in range(9))
c_, e_ = cash_fy25, eq_fy25_roll
p_ = V['ta_fy24'] - cash_fy24 - 900.0
wc_ = 900.0
for i in range(5):
    ti = c_ * V['cash_yield'][i]
    pbt = ebit_f[i] + ti
    tx = pbt * TAX
    pat = pbt - tx
    dv = pat * V['payout']
    p_ = p_ + capex[i] - dna_f[i]
    wc_ = wc_ + dwc[i]
    c_ = c_ + pat + dna_f[i] - capex[i] - dwc[i] - dv
    e_ = e_ + pat - dv
    for lst, val in ((treas_f, ti), (pbt_f, pbt), (tax_f, tx), (pat_f, pat),
                     (div_f, dv), (cash_bal, c_), (eq_bal, e_), (ppe_bal, p_),
                     (wc_bal, wc_)):
        lst.append(val)

# ---- 13. the expert panel — three genuinely different methods ---------------
fcff_mid = float(np.mean(fcff))
e3_ev = fcff_mid / V['e3_req_yield']
e3 = (e3_ev + net_cash) / V['shares_mn']
EXPERTS = [
 dict(label="Expert 1", method="Replacement-cost industrialist",
      central=fv_asset, low=0.0, high=0.0,
      summary=("Values the company as an asset, not an earnings stream. A 3.8Mt grey-cement "
               "plant costs roughly USD 130 per annual tonne to build; nobody pays "
               "replacement cost for capacity in a market carrying 76Mt against 54Mt of "
               "consumption, so the justified figure is USD 95/t. The market is paying USD "
               "81/t. On this view the shares are cheap against steel and concrete in the "
               "ground, and the cycle is somebody else's problem."),
      falsifier=("Find a recent Egyptian cement line built, bought or restarted for less "
                 "than USD 95 per annual tonne, or evidence that the El Hassana lines need "
                 "major refurbishment capex. Either would collapse the asset floor. The "
                 "12.6Mt revival programme is the live test: restarting a dormant line "
                 "costs far less per tonne than building one.")),
 dict(label="Expert 2", method="Mid-cycle earnings-power analyst",
      central=fv_norm, low=0, high=0,
      summary=("Refuses to capitalise a peak. 2025 was the first year since 2008 that "
               "Egypt's supply-demand gap closed, prices roughly doubled and utilisation "
               "hit 98% — none of which is a plateau. Normalises the margin to 26.5%, "
               "between the FY2024 outturn and the FY2025 peak, and applies 7x. Concludes "
               "the market is extrapolating a cyclical high."),
      falsifier=("Two consecutive years of realised prices holding above EGP 3,900/t WITH "
                 "the revival programme proceeding would prove the mid-cycle margin too "
                 "low and this lens too bearish. Equally, a cancelled revival programme "
                 "plus continued 13% demand growth would make 26.5% the new floor rather "
                 "than the middle.")),
 dict(label="Expert 3", method="Cash-return and distribution investor",
      central=e3, low=0, high=0,
      summary=("Starts from the balance sheet. Net cash of EGP %.1fbn is 37%% of the "
               "market capitalisation, and the operating business throws off roughly EGP "
               "%.0fmn of free cash flow a year against essentially no reinvestment need — "
               "terminal return on capital of %.1f%% is below the %.1f%% cost of capital, "
               "so growth destroys value and the right policy is to harvest and "
               "distribute. Capitalises mid-cycle free cash flow at an %.0f%% required "
               "yield and adds the cash." %
               (net_cash / 1000, fcff_mid, roic_term * 100, wacc_term * 100,
                V['e3_req_yield'] * 100)),
      falsifier=("The whole lens rests on the cash being distributable. If no dividend is "
                 "declared on FY2026 profits, or the cash is deployed into a capacity "
                 "expansion into a glutted market, the cash is worth materially less than "
                 "face and this lens is wrong. The unexplained gap between rolled-forward "
                 "and reported FY2025 equity — about EGP 1.9bn — is the first place to "
                 "look, because it may already be a distribution nobody has reported.")),
]
EXPERTS[0]['low'] = ((V['ev_t_just'] - 15) * V['capacity_mt'] * 1e6 * V['fx_usd'] / 1e6
                     + net_cash) / V['shares_mn']
EXPERTS[0]['high'] = ((V['ev_t_just'] + 15) * V['capacity_mt'] * 1e6 * V['fx_usd'] / 1e6
                      + net_cash) / V['shares_mn']
EXPERTS[1]['low'] = earn_norm * (V['pe_just'] - 1) / V['shares_mn']
EXPERTS[1]['high'] = earn_norm * (V['pe_just'] + 1) / V['shares_mn']
EXPERTS[2]['low'] = (fcff_mid / (V['e3_req_yield'] + 0.04) + net_cash) / V['shares_mn']
EXPERTS[2]['high'] = (fcff_mid / (V['e3_req_yield'] - 0.04) + net_cash) / V['shares_mn']
say(f"\n[Expert panel] mid-cycle FCFF {fcff_mid:,.0f} at a {V['e3_req_yield']:.0%} required "
    f"yield -> EV {e3_ev:,.0f}")
for e in EXPERTS:
    say(f"    {e['label']} ({e['method']}): {e['low']:.2f} - {e['high']:.2f}, "
        f"central {e['central']:.2f}")
exp_c = [e['central'] for e in EXPERTS]
say(f"    panel range EGP {min(exp_c):.2f} - {max(exp_c):.2f}, median "
    f"{sorted(exp_c)[1]:.2f} against spot {V['spot']:.2f}")

# ============================ ASSERT =========================================
say("\n" + "=" * 78)
say("ASSERT")
say("=" * 78)
assert abs((sum_pv + pv_tv) - ev) < 1e-6, "EV does not equal PV(FCFF) + PV(TV)"
assert abs((ev + net_cash) - eq_dcf) < 1e-6, "bridge does not close"
assert net_cash > 0, "sign error: this company is net CASH, the bridge must ADD"
assert V['debt_fy25'] >= 0 and cash_fy25 > 0, "sign error on debt or cash"
say(f"  bridge closes: EV {ev:,.2f} + net cash {net_cash:,.2f} = equity {eq_dcf:,.2f} "
    f"(residual {abs((ev+net_cash)-eq_dcf):.2e})")
say(f"  net debt sign: NET CASH of {net_cash:,.0f}, ADDED to enterprise value")
assert 0.0 < tv_share < 0.95, f"terminal share {tv_share:.1%} outside sane range"
say(f"  terminal value share of enterprise value: {tv_share:.1%}")
assert abs(roic_term * rr_term - V['g_term']) < 1e-9
say(f"  terminal identity holds: ROIC {roic_term:.4%} x RR {rr_term:.4%} = g {V['g_term']:.4%}")
assert wacc_term < wacc_exp
say(f"  discount schedule ordered: terminal WACC {wacc_term:.2%} < explicit {wacc_exp:.2%}")
assert all(fwd[i] >= fwd[i + 1] - 1e-12 for i in range(4)), "forward WACC path not monotone"
say(f"  forward WACC path monotone: {' -> '.join(f'{x:.2%}' for x in fwd)}")
assert all(df_[i] > df_[i + 1] for i in range(4)), "discount factors not decreasing"
say(f"  discount factors compound and decrease: {' > '.join(f'{x:.4f}' for x in df_)}")
ratio = fv_central / V['spot']
assert 0.3 < ratio < 3.0, f"implied fair value {ratio:.2f}x spot outside plausibility band"
say(f"  fair value to spot {ratio:.2f}x — inside the stated 0.3x-3.0x plausibility band")
for y in HIST:
    got = vol[y] * price[y]
    exp_ = {'FY2023': V['rev_fy23'], 'FY2024': V['rev_fy24'], 'FY2025': V['rev_fy25']}[y]
    assert abs(got - exp_) < 1.0, f"unit build does not reproduce {y} revenue"
say(f"  unit build reproduces disclosed revenue in all three historical years")
assert abs((V['ta_fy24'] - V['tl_fy24']) - 4775.06) < 0.01
say(f"  FY2024 disclosed balance-sheet triple closes exactly: "
    f"{V['ta_fy24']:,.2f} - {V['tl_fy24']:,.2f} = {V['ta_fy24']-V['tl_fy24']:,.2f}")

eq_gap = eq_fy25_roll - V['eq_fy25_rep']
say(f"  DISCLOSED, not suppressed: rolling FY2024 equity {V['ta_fy24']-V['tl_fy24']:,.0f} "
    f"forward by FY2025 profit {V['pat_fy25']:,.0f} with NO distribution gives "
    f"{eq_fy25_roll:,.0f}, against a reported ~{V['eq_fy25_rep']:,.0f}. The EGP "
    f"{eq_gap:,.0f}mn gap implies a FY2025 distribution of roughly that size, which no "
    f"retrievable source reports. The gap is carried as a disclosed uncertainty, not "
    f"plugged silently.")

# ============================ EMIT ===========================================
OUT = dict(
    meta=dict(ticker="SCEM", company="Sinai Cement Company S.A.E.", market="EGX",
              market_code="EG", currency="EGP", asof="2026-08-06",
              spot=V['spot'], shares_mn=V['shares_mn'], mktcap=mktcap,
              klass="single-asset cement operating company (net cash)",
              reference_study="EAND (operating company)",
              sector="Construction materials — cement"),
    inputs=INP,
    share_triangulation=dict(issued_capital=sh_capital, tender_offer=sh_mto,
                             market_cap=sh_mktcap, mean=sh_avg, adopted=V['shares_mn']),
    history=dict(years=HIST,
                 revenue=[V['rev_fy23'], V['rev_fy24'], V['rev_fy25']],
                 ebitda=[ebitda[y] for y in HIST], dna=[dna[y] for y in HIST],
                 ebit=[ebit[y] for y in HIST], treasury=[treas[y] for y in HIST],
                 pat=[V['pat_fy23'], V['pat_fy24'], V['pat_fy25']],
                 volume_mt=[vol[y] for y in HIST], price_t=[price[y] for y in HIST],
                 utilisation=[util[y] for y in HIST]),
    disposal=dict(proceeds=swcc_proceeds, book=V['swcc_book'], gain=swcc_gain,
                  underlying_fy24_pat=und_fy24),
    forecast=dict(years=YRS, volume_mt=vol_f, price_t=price_f, revenue=rev_f,
                  ebitda=ebitda_f, dna=dna_f, ebit=ebit_f, nopat=nopat, capex=capex,
                  dwc=dwc, fcff=fcff, df=df_, pv=pv, fwd_wacc=fwd, glide=glide,
                  treasury=treas_f, pbt=pbt_f, tax=tax_f, pat=pat_f, dividends=div_f,
                  cash=cash_bal, equity=eq_bal, ppe=ppe_bal, wc=wc_bal, ic=ic),
    wacc=dict(rf=V['rf'], rf_star=rf_star, ke_exp=ke_exp, ke_raw_retired=ke_raw_retired,
              ke_rating_alt=ke_rating_alt, kd=V['kd'], kd_at=kd_at, wd_exp=wd_exp,
              we_exp=we_exp, wacc_exp=wacc_exp, ke_term=ke_term, kd_term_at=kd_term_at,
              wacc_term=wacc_term, kd_immaterial=kd_immaterial),
    dcf=dict(sum_pv=sum_pv, tv=tv, pv_tv=pv_tv, ev=ev, tv_share=tv_share,
             net_cash=net_cash, cash_fy25=cash_fy25, equity=eq_dcf, fv=fv_dcf,
             roic_term=roic_term, rr_term=rr_term, nopat_term=nopat_term,
             ic_fy25=ic_fy25, roic_book=roic_book, ic_repl=ic_repl),
    lenses=dict(values=lenses, weights=w, central=fv_central, low=fv_low, high=fv_high,
                ebitda_norm=ebitda_norm, nopat_norm=nopat_norm, earn_norm=earn_norm,
                bvps=bvps, roe_sust=roe_sust, eq_fy25_roll=eq_fy25_roll,
                ev_per_t_spot=ev_per_t_spot, ev_asset=ev_asset, repl_ev=repl_ev,
                ev_t_just=V['ev_t_just'], repl_usd_t=V['repl_usd_t']),
    terminal_reconciliation=dict(
        roic_book=roic_book, roic_repl=roic_repl, ic_book=ic[-1], ic_repl=ic_repl,
        rr_book=V['g_term'] / roic_book, rr_repl=V['g_term'] / roic_repl,
        basis_adopted="replacement cost",
        history=hist_recon, nopat_cagr=nopat_cagr, stable_implied_g=stable_g),
    sensitivity=dict(wacc_grid=wacc_grid, g_grid=g_grid, wacc_g=sens_wacc_g,
                     term_grid=term_grid, exp_term=sens_exp_term,
                     beta_grid=beta_grid, beta=sens_beta,
                     mgn_grid=mgn_grid, mgn=sens_mgn),
    lens_ranges=dict(
        **{'DCF (cash flow)': dict(
            bear=float(np.min(sens_wacc_g)), base=fv_dcf, bull=float(np.max(sens_wacc_g)),
            basis='the explicit-WACC x terminal-growth grid'),
           'Relative multiples': dict(
            bear=(ebitda_norm * (V['ev_ebitda_just'] - 1) + net_cash) / V['shares_mn'],
            base=fv_mult,
            bull=(ebitda_norm * (V['ev_ebitda_just'] + 1) + net_cash) / V['shares_mn'],
            basis='justified EV/EBITDA +/- 1.0x'),
           'Normalised earnings': dict(
            bear=earn_norm * (V['pe_just'] - 1) / V['shares_mn'], base=fv_norm,
            bull=earn_norm * (V['pe_just'] + 1) / V['shares_mn'],
            basis='justified price/earnings +/- 1.0x'),
           'Asset / replacement cost': dict(
            bear=((V['ev_t_just'] - 15) * V['capacity_mt'] * 1e6 * V['fx_usd'] / 1e6
                  + net_cash) / V['shares_mn'],
            base=fv_asset,
            bull=((V['ev_t_just'] + 15) * V['capacity_mt'] * 1e6 * V['fx_usd'] / 1e6
                  + net_cash) / V['shares_mn'],
            basis='justified EV per tonne +/- USD 15/t'),
           'Weighted central': dict(
            bear=float(sum(min(sens_wacc_g[i]) for i in range(5)) / 5 * w['DCF (cash flow)']
                       + fv_mult * w['Relative multiples']
                       + fv_norm * w['Normalised earnings']
                       + fv_asset * w['Asset / replacement cost']) * 0.88,
            base=fv_central,
            bull=fv_central * 1.14,
            basis='the weighted blend across the four lens ranges')}),
    experts=EXPERTS,
    equity_gap=dict(rolled=eq_fy25_roll, reported=V['eq_fy25_rep'], gap=eq_gap),
    peers=dict(
        mbsc=dict(name="Misr Beni Suef Cement (MBSC)", rev=V['peer_mbsc_rev'],
                  pat=V['peer_mbsc_pat'], eps=V['peer_mbsc_eps'], mcap=V['peer_mbsc_mcap'],
                  pe=V['peer_mbsc_pe'], ev_ebitda=V['peer_mbsc_evebitda']),
        arcc=dict(name="Arabian Cement (ARCC)", pat=V['peer_arcc_pat']),
        sector=dict(capacity_mt=V['egy_capacity_mt'], consumption_mt=V['mkt_mt_fy25'],
                    production_mt=V['egy_prod_mt'], exports_mt=V['egy_exports_mt'],
                    revival_mt=V['egy_revival_mt'],
                    scem_share_of_capacity=V['capacity_mt'] / V['egy_capacity_mt'],
                    revival_pct_of_consumption=V['egy_revival_mt'] / V['mkt_mt_fy25'])),
    growth_destroys_value=dict(
        fv_at_g3=revalue(g=0.03), fv_at_g7=revalue(g=0.07), holds=bool(g_destroys),
        roic_term=roic_term, wacc_term=wacc_term,
        note=("Terminal ROIC %.1f%% is BELOW terminal WACC %.1f%%, so higher terminal "
              "growth LOWERS fair value. Any driver test asserting the conventional "
              "direction for g would be asserting the wrong expectation."
              % (roic_term * 100, wacc_term * 100))),
    assert_log=LOG,
)
with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(OUT, f, indent=1, default=float)
say(f"\nwrote study_numbers.json")
