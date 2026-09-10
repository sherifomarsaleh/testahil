#!/usr/bin/env python3
"""ADIB-Egypt (EGX: ADIB) — the valuation model. Every number the study prints starts here.

WHICH ADIB. Abu Dhabi Islamic Bank – Egypt S.A.E., EGX: ADIB, Cairo-listed, EGP,
formerly National Bank for Development. NOT ADIB Group PJSC (ADX: ADIB), which is the
separate covered name ADIBUAE with its own study.

A BANK IS VALUED ON WHAT REACHES THE SHAREHOLDER [L-111]. There is no enterprise value
here, no WACC and no FCFF: a bank's deposits are its raw material, not its financing, and
subtracting them as though they were debt is meaningless. Three equity lenses — a
dividend discount on the payout path, free cash flow to equity after the capital the
balance sheet actually consumes, and residual income over the cost of equity — plus
relative multiples and normalised earnings power.

MARGINS ARE OUTPUTS [L-005]. The asset yield and the cost of funds are the inputs; net
interest margin, cost-to-income, return on assets and return on equity fall out of them
and are never typed.

WHAT THE WALK-FORWARD PUT IN HERE. Two things and only two, per [R-FCAL-01]:
  * the years 3-5 RANGES, taken from engine/adib_walkforward/forward_ranges.json — this
    record's own driver-error distribution and nothing else;
  * the knowledge that a flat-share volume rule under-forecasts this name at every
    origin, which is why the share path below is explicit and disclosed rather than held
    flat. NO CORRECTION FACTOR ENTERS THESE DRIVERS. Every candidate failed the second
    clause or was an aggregate; the record says so and this model carries none.
"""
from __future__ import annotations
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, ENGINE)
sys.path.insert(0, os.path.join(ENGINE, 'adib_walkforward'))

import macro_path                                    # noqa: E402
from beta_regression import own_stock_beta           # noqa: E402
import panel as WF                                   # noqa: E402

EG = macro_path.load('EG')
STUDY_DATE = '2026-09-10'   # RECALIBRATION EDITION: the terminal risk-free
# rate was refreshed from the house macro path and the answer moved, so this is a
# NEW document rather than a re-print of the old one [R-DOC-03]. Supersedes
# 09-09-2026 (EGP 37.18) and 07-09-2026.
YEARS = [2026, 2027, 2028, 2029, 2030]
MN = 1000.0        # the walk-forward panel is EGP '000; this study works in EGP millions


# ----------------------------------------------------------------------------------
# The input register. value / source / date / tier on every entry.
# ----------------------------------------------------------------------------------
class I:
    def __init__(self, value, source, date, tier):
        self.value, self.source, self.date, self.tier = value, source, date, tier


_BETA = own_stock_beta('ADIB', 'EG', 'EGX')

REG = {}


def reg(name, value, source, date, tier):
    REG[name] = I(value, source, date, tier)
    return value


# ---- price -----------------------------------------------------------------------
SPOT = reg('spot', 52.05,
           'EGP 52.05, the close on 3 September 2026, supplied by the principal and '
           'committed to the house price file for that date. THIS IS THE LATEST '
           'KNOWN PRICE and it is the one the gap is measured against. The published site '
           'still carries 54.40 at the 23 August close, which is 11 days older; a study '
           'audited against its own past is audited against nothing.',
           '2026-09-03', 'Market')
SHARES = reg('shares', 1500.0,
             'ADIB-Egypt issued and paid-up capital of EGP 15,000,000 thousand at 30 June '
             '2026, over the LE 10 par value the filings state (FY2018 note 34/2), = 1,500 '
             'million shares. THE CAPITAL FIGURE IS PROVED BY THE EQUITY BLOCK\'S OWN '
             'ARITHMETIC RATHER THAN BY THE OCR: attributable equity of 43,557,932 less '
             'the subordinated-financing difference of 16,454 leaves 43,541,478 for capital '
             'plus reserves plus retained earnings; retained earnings cannot exceed the '
             'FY2025 closing 20,963,164 plus the half-year attributable profit of 7,536,797 '
             '= 28,499,961, so a capital of 12,000,000 is arithmetically impossible and '
             '15,000,000 is the only reading that closes. It matches the EGP 12bn->15bn '
             'cash increase the delivered 03-07-2026 study reported as approved.',
             '2026-06-30', 'A')

# ---- the base year and the latest reviewed period --------------------------------
def _p(y, f):
    return WF.IS['FY%d' % y][f] / MN


def _b(y, f):
    return WF.BS['FY%d' % y][f] / MN


FY25 = dict(fin_income=_p(2025, 'fin_income'), cost_funds=_p(2025, 'cost_funds'),
            net_funds=_p(2025, 'net_funds'), net_fees=_p(2025, 'net_fees'),
            other_nii=WF.other_nii('FY2025') / MN, admin=_p(2025, 'admin'),
            other_op=_p(2025, 'other_op'), ecl=_p(2025, 'ecl'), pbt=_p(2025, 'pbt'),
            tax=_p(2025, 'tax'), np=_p(2025, 'np'), np_parent=_p(2025, 'np_parent'),
            total_assets=_b(2025, 'total_assets'), deposits=_b(2025, 'cust_deposits'),
            financing=_b(2025, 'fin_customers'), equity=_b(2025, 'equity_parent'))
FY24 = dict(total_assets=_b(2024, 'total_assets'), financing=_b(2024, 'fin_customers'),
            equity=_b(2024, 'equity_parent'), np_parent=_p(2024, 'np_parent'))

H1 = {k: v / MN for k, v in WF.INTERIM['H1_2026'].items() if isinstance(v, (int, float))}
H1['eps'] = WF.INTERIM['H1_2026']['eps']

reg('base_year', 'FY2025',
    'The audited consolidated financial statements for the year ended 31 December 2025, '
    'signed in Cairo on 5 February 2026. Attributable profit EGP 12,588.6 million, total '
    'assets EGP 346,711.2 million, attributable equity EGP 34,596.3 million. Every figure '
    'is read from the filing itself and the statement foots.', '2026-02-05', 'A')
reg('latest_reviewed', 'H1-2026',
    'The condensed consolidated interim statements for the six months ended 30 June 2026, '
    'signed 30 July 2026. Attributable profit EGP 7,536.8 million, total assets EGP '
    '414,302.1 million, financing to customers EGP 190,427.1 million, attributable equity '
    'EGP 43,557.9 million. This is the period the forecast is anchored on.',
    '2026-07-30', 'A')

# ---- observed ratios: OUTPUTS of the base year, computed, never typed -------------
avg_ta_25 = (FY25['total_assets'] + FY24['total_assets']) / 2
avg_fin_25 = (FY25['financing'] + FY24['financing']) / 2
avg_eq_25 = (FY25['equity'] + FY24['equity']) / 2
ibl_25 = (_b(2025, 'cust_deposits') + _b(2025, 'due_to_banks') + _b(2025, 'subordinated'))
ibl_24 = (_b(2024, 'cust_deposits') + _b(2024, 'due_to_banks') + _b(2024, 'subordinated'))
avg_ibl_25 = (ibl_25 + ibl_24) / 2

OBS = dict(
    asset_yield=FY25['fin_income'] / avg_ta_25,
    cost_of_funds=-FY25['cost_funds'] / avg_ibl_25,
    ibl_over_assets=avg_ibl_25 / avg_ta_25,
    nim=FY25['net_funds'] / avg_ta_25,
    fee_ratio=FY25['net_fees'] / avg_ta_25,
    onii_ratio=FY25['other_nii'] / avg_ta_25,
    otherop_ratio=FY25['other_op'] / avg_ta_25,
    cost_of_risk=-FY25['ecl'] / avg_fin_25,
    cost_income=-FY25['admin'] / (FY25['net_funds'] + FY25['net_fees'] + FY25['other_nii']),
    tax_rate=-FY25['tax'] / FY25['pbt'],
    roe=FY25['np_parent'] / avg_eq_25,
    roa=FY25['np'] / avg_ta_25,
    financing_over_assets=FY25['financing'] / FY25['total_assets'],
    equity_over_assets=FY25['equity'] / FY25['total_assets'])

avg_ta_h1 = (H1['total_assets'] + FY25['total_assets']) / 2
avg_eq_h1 = (H1['equity_parent'] + FY25['equity']) / 2
H1OBS = dict(nim=H1['net_funds'] * 2 / avg_ta_h1,
             asset_yield=H1['fin_income'] * 2 / avg_ta_h1,
             fee_ratio=H1['net_fees'] * 2 / avg_ta_h1,
             roe=H1['np_parent'] * 2 / avg_eq_h1,
             tax_rate=-H1['tax'] / H1['pbt'],
             financing_over_assets=H1['fin_customers'] / H1['total_assets'],
             equity_over_assets=H1['equity_parent'] / H1['total_assets'],
             ecl_charge=2.176,          # EGP million, filed; see the register entry below
             cost_of_risk=2.176 * 2 / ((H1['fin_customers'] + FY25['financing']) / 2))

reg('h1_2026_ecl', 2.176,
    'THE SINGLE MOST IMPORTANT FACT IN THE BASE YEAR. ADIB-Egypt charged EGP 2.176 million '
    'of expected credit losses in the six months to 30 June 2026 — an annualised 0.003% of '
    'average financing — against EGP 732.193 million in the same half of 2025 and EGP '
    '1,514.062 million for the whole of FY2025. The line is filed as "Release / (Charge) '
    'Expected credit losses", note 11, and the income statement foots on it: every other '
    'line on the page plus this one reproduces the printed profit before tax of 10,721,790 '
    'exactly. A half-year at a near-nil loss charge is a release, not a run rate, and the '
    'forecast below normalises it rather than annualising it — which is the conservative '
    'direction and is named as a mechanism rather than assumed.',
    '2026-07-30', 'A')

# ---- macro -----------------------------------------------------------------------
INFL = reg('inflation_path', [0.16, 0.12, 0.09, 0.075, 0.07],
           'Central Bank of Egypt baseline average annual headline inflation, 16.0% in 2026 '
           'and 12.0% in 2027 (Q1-2026 Monetary Policy Report as reported 11 May 2026); '
           '2028-2030 interpolated on the bank\'s own glide between the published 2027 '
           'baseline and the 7% target-band midpoint, labelled as interpolation and never '
           'presented as a central-bank forecast. Held in the house macroeconomic path, the '
           'path every Egyptian study runs on.', EG.as_of, 'Country')
POLICY = reg('policy_rate_path', list(EG.raw['policy_rate']['path']),
             'Overnight deposit rate 19.00% now, gliding 19.00 -> 16.50 -> 14.50 -> 13.00 '
             '-> 12.00 with the published inflation path at an approximately constant real '
             'policy rate. Held for a fourth consecutive meeting on 20 August 2026. This is '
             'the SHAPE input for the asset-yield and cost-of-funds paths below; it is not '
             'a second free parameter and no valuation input is set from it independently.',
             EG.raw['policy_rate']['current']['date'], 'Country')

RF = reg('rf', 0.2300,
         'Egypt ten-year EGP government bond yield, 23.00%, the quote of 6 August 2026 held '
         'in the house macroeconomic path and already used by the PHDC, EGCH and PHAR '
         'cost-of-capital records. IT IS 34 DAYS OLD AGAINST THIS STUDY\'S PRICING DATE AND '
         'THE HOUSE PATH\'S OWN 14-DAY STALENESS RULE FLAGS IT AS STALE. A live re-source '
         'was attempted on 9 September 2026 down four routes and all four failed: the '
         'central bank\'s treasury-bond auction pages return 404, its auction API returns '
         'the site shell, the market-data pages render their yield tables in JavaScript, '
         'and the investing.com bond page returns 403. The level is carried, the staleness '
         'is declared here rather than buried, and the rate is sensitised by +/-200 basis '
         'points in section 1.9.', '2026-08-06', 'Country')
SOV_SPREAD = reg('sov_default_spread', 0.0342,
                 'Egypt sovereign credit-default-swap spread, 3.42%, mid-year (July 2026) '
                 'vintage of the country default-spread dataset, Egypt row, "Sovereign CDS '
                 'net of Swiss CDS". Netted out of the local-currency risk-free rate so '
                 'that sovereign default risk is charged ONCE, inside the equity risk '
                 'premium, and not twice. The house macroeconomic path carries 3.41% for '
                 'the same field from the same file; the one-basis-point difference is a '
                 'rounding artefact and is immaterial.', '2026-07-02', 'Country')
ERP = reg('erp', 0.095164,
          'Egypt TOTAL equity risk premium on the sovereign-CDS basis, 9.5164%, same '
          'mid-year vintage. This is the dataset\'s TOTAL premium column, not its country '
          'premium column — the total is what multiplies beta. The country risk premium '
          'alone on this basis is 5.3164% and is NOT added on top.', '2026-07-02', 'Country')
SOV_SPREAD_R = reg('sov_default_spread_rating', 0.059702,
                   'Egypt adjusted default spread on the rating basis (Moody\'s Caa1), '
                   '5.9702%, same vintage — the alternative construction, published for the '
                   'audit trail and never mixed with the CDS basis.', '2026-07-02', 'Country')
ERP_R = reg('erp_rating', 0.134806,
            'Egypt TOTAL equity risk premium on the rating basis, 13.4806%, same vintage.',
            '2026-07-02', 'Country')
BETA = reg('beta', float(_BETA['beta']),
           'Own-stock first-tier weekly regression against EGX30 — THE PUBLISHED INDEX OF '
           'THE EXCHANGE THIS STOCK IS LISTED ON — resolved by '
           'beta_regression.own_stock_beta() rather than hand-rolled. Beta %.4f, R-squared '
           '%.3f, n = %d weekly observations over %.2f years to %s, standard error %.4f, '
           '90%% confidence interval [%.3f, %.3f], Dimson-corrected and matched to the '
           'exchange\'s own trading week (%s). The coefficient is 6.6 times its own '
           'standard error. Blume cross-check %.4f.'
           % (_BETA['beta'], _BETA['r2'], _BETA['n'], _BETA['window_years'],
              _BETA['last_obs'], _BETA['se'], _BETA['ci90'][0], _BETA['ci90'][1],
              _BETA['week_rule'], _BETA['blume_crosscheck']),
           _BETA['index_asof'], 'Market')
RF_TERM = reg('rf_terminal', EG.terminal_rf,
              'Terminal risk-free rate, DERIVED and never quoted: terminal inflation of '
              '7.00% (the CBE target-band midpoint in force) plus the 5.50% emerging-market '
              'terminal real convention. It cannot disagree with the inflation the rest of '
              'the model runs on because it is computed from it.', EG.as_of, 'House')
ERP_TERM = reg('erp_terminal', EG.erp_terminal,
               'Terminal equity risk premium, 7.00%, normalised below today\'s crisis-era '
               'level toward the rating-class norm; never held flat into perpetuity.',
               EG.as_of, 'House')
G_TERM = reg('terminal_growth', EG.terminal_inflation,
             'Terminal growth 7.00% = terminal inflation, ZERO REAL. For a bank in an '
             'economy whose private credit is 26% of GDP that is deliberately conservative: '
             'it assumes ADIB-Egypt stops taking share and stops participating in credit '
             'deepening the moment the explicit window closes. It sits BELOW the 12.50% '
             'terminal risk-free rate and equals the inflation inside it, so the terminal '
             'cannot grow faster than the money it is discounted in.', EG.as_of, 'House')

rf_star = RF - SOV_SPREAD
KE0 = rf_star + BETA * ERP
KE_RATING = (RF - SOV_SPREAD_R) + BETA * ERP_R
KE_DOUBLE = RF + BETA * ERP                      # the retired construction, for contrast
KE_TERM = RF_TERM + BETA * ERP_TERM
KE_PATH = [KE0 + (KE_TERM - KE0) * (i + 1) / (len(YEARS) + 1) for i in range(len(YEARS))]

reg('ke_construction', 'same_beta',
    'The terminal cost of equity uses the SAME regression beta as the explicit window. '
    'ADIB-Egypt is a deposit-funded bank whose capital structure is its business, so there '
    'is no leverage to relever: the beta already embeds the balance sheet it is measured '
    'on. The record names the construction from a closed list so that two '
    'right answers a hundred basis points apart are not indistinguishable from a typo.',
    STUDY_DATE, 'House')

# ---- the drivers -----------------------------------------------------------------
FIN_GROWTH = reg('financing_growth', [0.48, 0.26, 0.19, 0.15, 0.12],
                 'Net financing to customers, year-on-year. FY2026 +48% takes the FY2025 '
                 'close of EGP 147,226 million to EGP 217,895 million — and the bank was '
                 'ALREADY at EGP 190,427 million on 30 June, so this asks for only +14.4% '
                 'in the second half against +29.3% in the first. The path then decays '
                 'toward nominal GDP. IT IS NOT A FLAT SHARE OF SYSTEM CREDIT, and that is '
                 'the walk-forward\'s doing: a flat-share rule under-forecast this name at '
                 'every one of eleven origins, by a median 0.29 in logs at three years, '
                 'because ADIB has taken share at about 8.7% a year for a decade. The share '
                 'path this implies is disclosed in the macro-coherence table and it '
                 'decelerates to zero drift by FY2030.', STUDY_DATE, 'House')
FIN_OVER_ASSETS = reg('financing_over_assets', [0.470, 0.485, 0.500, 0.510, 0.520],
                      'Financing to customers over total assets. FY2025 actual 42.46%; 30 '
                      'June 2026 actual 45.96%. The bank is rotating out of treasury bills '
                      'into customer financing as policy rates fall and bill yields '
                      'compress, and the path continues that observed rotation at a '
                      'decelerating pace. Every point is above both observations, which is '
                      'the assumption, and it is sensitised.', STUDY_DATE, 'House')
ASSET_YIELD = reg('asset_yield', [0.150, 0.134, 0.121, 0.113, 0.108],
                  'Income from Murabaha, Musharaka, Mudaraba and similar income over '
                  'AVERAGE total assets. FY2025 actual 16.23%; the six months to June 2026 '
                  'annualise to 15.30%. The path falls with the CBE\'s published policy '
                  'glide (19.00 -> 12.00) at an asset beta of about 0.75, which is what an '
                  'Egyptian bank holding treasury bills and floating-rate corporate paper '
                  'reprices at. IT IS AN INPUT; net interest margin is not.',
                  STUDY_DATE, 'House')
COST_OF_FUNDS = reg('cost_of_funds', [0.106, 0.092, 0.081, 0.074, 0.070],
                    'Cost of deposits and similar costs over AVERAGE INTEREST-BEARING '
                    'LIABILITIES — customers\' deposits plus due to banks plus subordinated '
                    'financing, and nothing else. FY2025 actual 11.22%. Total liabilities is '
                    'NOT the denominator: at FY2025 it would add EGP 17.9 billion of other '
                    'liabilities, current tax and provisions that pay nothing, and understate '
                    'the funding rate by about a sixth of itself. The path falls at a deposit '
                    'beta of about 0.80 to the policy glide, slower than the asset side, '
                    'which is why the margin compresses.', STUDY_DATE, 'House')
IBL_OVER_ASSETS = reg('ibl_over_assets', 0.855,
                      'Average interest-bearing liabilities over average total assets, held '
                      'at the FY2025 observed 85.5%. The bank funds itself with deposits and '
                      'that ratio has moved within two points across the whole panel.',
                      STUDY_DATE, 'House')
FEE_RATIO = reg('fee_ratio', [0.0080, 0.0082, 0.0084, 0.0085, 0.0085],
                'Net fees and commissions over average total assets. FY2025 actual 0.899%; '
                'the June 2026 half annualises to 0.797%. The path opens at the reviewed '
                'half\'s level and recovers slowly as trade finance and card income grow '
                'with the branch network.', STUDY_DATE, 'House')
ONII_RATIO = reg('other_nii_ratio', [0.0028, 0.0026, 0.0024, 0.0023, 0.0022],
                 'Dividends, net trading, share of associates and gains on investments, as '
                 'one block, over average total assets. FY2025 actual 0.238%; the June 2026 '
                 'half annualises to 0.372%, flattered by trading gains on a moving '
                 'currency. The path normalises DOWN toward the FY2022-FY2024 average as '
                 'the pound settles.', STUDY_DATE, 'House')
OTHEROP_RATIO = reg('other_op_ratio', [-0.0075, -0.0070, -0.0065, -0.0060, -0.0055],
                    'Other operating expenses over average total assets — deposit insurance, '
                    'central-bank charges and the operating-provision line. FY2025 actual '
                    '-0.387%; the June 2026 half annualises to -0.797%, more than double. '
                    'The path opens at the reviewed level and decays, which is the '
                    'conservative reading of a line that has doubled.', STUDY_DATE, 'House')
ADMIN_GROWTH = reg('admin_growth', [0.34, 0.18, 0.15, 0.135, 0.13],
                   'Administrative expenses, year-on-year. FY2026 +34% on FY2025 takes EGP '
                   '3,431 million to EGP 4,598 million; the June half already spent EGP '
                   '2,239 million, so this asks for EGP 2,359 million in the second. '
                   'Thereafter inflation plus about six points, because a bank adding '
                   'branches and systems does not hold headcount flat. Cost-to-income is an '
                   'OUTPUT of this and of the revenue lines; it is not typed anywhere.',
                   STUDY_DATE, 'House')
COST_OF_RISK = reg('cost_of_risk', [0.0100, 0.0130, 0.0130, 0.0130, 0.0130],
                   'Expected credit losses over AVERAGE net financing to customers. The '
                   'observed series is 1.64% (FY2022), 2.73% (FY2023), 2.73% (FY2024), 1.25% '
                   '(FY2025) and effectively ZERO in the June 2026 half — EGP 2.176 million '
                   'on a EGP 190 billion book. FY2026 is set at 1.00%, above the half-year '
                   'run rate and below the four-year mean of 2.09%; the outer years at 1.30% '
                   'sit between the two. ANNUALISING THE JUNE HALF WOULD HAVE ADDED ABOUT '
                   'EGP 1.8 BILLION TO FY2026 PRE-TAX PROFIT and it is not done. Sensitised '
                   '+/-50 basis points in 1.9.', STUDY_DATE, 'House')
TAX_RATE = reg('tax_rate', 0.285,
               'Effective tax rate. FY2025 actual 27.92%, FY2024 26.64%, the June 2026 half '
               '29.58%. The Egyptian statutory corporate rate is 22.5%; an Egyptian bank pays '
               'materially more because the 20% withholding on treasury-bill income is not '
               'creditable and part of its cost base is disallowed. 28.5% sits inside the '
               'observed range and above the statutory rate for that reason.',
               STUDY_DATE, 'House')
NCI_SHARE = reg('nci_share', 0.001,
                'Non-controlling interests take 0.10% of net profit — EGP 12.4 million of '
                'EGP 12,601.0 million in FY2025. Held at that level; it is immaterial and is '
                'carried rather than dropped so the bridge to attributable profit closes.',
                STUDY_DATE, 'A')
PAYOUT = reg('payout', 'DERIVED — see below',
             'THE PAYOUT IS NOT TYPED. It is what is left after the balance sheet has taken '
             'the capital it needs: payout(t) = 1 - (target equity/assets x the year\'s '
             'asset growth) / attributable profit, floored at zero and capped at 80%. A '
             'typed payout path is an assumption about the single thing a growing bank has '
             'least discretion over, and typing one made this model\'s dividend and '
             'free-cash-flow lenses disagree by EGP 7 a share while its equity-to-assets '
             'ratio drifted from 10.0% to 12.4% — the model was retaining capital it had no '
             'use for and calling the result conservatism. THE DERIVED PATH REPRODUCES WHAT '
             'THE BANK ACTUALLY DOES: it gives 13.7% for FY2026 against the 11.7% ADIB-Egypt '
             'actually paid on FY2024 earnings, which is the closest thing to an external '
             'check this driver has. Terminal payout is 1 - g/ROE, derived the same way.',
             STUDY_DATE, 'House')
TARGET_EQ_ASSETS = reg('target_equity_assets', 0.105,
                       'Attributable equity to total assets, held at 10.5% — the level '
                       'ADIB-Egypt actually stood at on 30 June 2026 after its EGP 3 billion '
                       'cash increase, against 9.98% at the FY2025 year end. THIS IS THE '
                       'BINDING CONSTRAINT ON A GROWING BANK and the model pins the RATIO, '
                       'not the increment: equity each year is 10.5% of that year\'s assets '
                       'and the dividend is whatever profit is left after getting there. A '
                       'bank growing its balance sheet 34% cannot also distribute, and the '
                       'arithmetic says so rather than a sentence saying so beside a typed '
                       'payout.', STUDY_DATE, 'House')
CAP_INCREASE_26 = reg('capital_increase_2026', 3000.0,
                      'The EGP 3,000 million cash capital increase completed in the first '
                      'half of 2026, taking issued capital from EGP 12 billion to EGP 15 '
                      'billion — 300 million new shares at the LE 10 par. IT WAS ISSUED AT '
                      'PAR, far below book: attributable book value per share was EGP 28.83 '
                      'at 31 December 2025 on 1,200 million shares and EGP 29.04 at 30 June '
                      '2026 on 1,500 million, so a half-year at a 38.6% return on equity '
                      'bought existing holders 0.7% of book value per share and the rest '
                      'went to the new shares. This is the study\'s crux and it is in 1.7.',
                      '2026-06-30', 'A')

# ---- peers -----------------------------------------------------------------------
PEER_COMI = reg('peer_comi_price', 138.98,
                'Commercial International Bank (EGX: COMI), EGP 138.98, the close on 3 '
                'September 2026 from the committed price file — the same '
                'file, the same date and the same supplier as ADIB\'s own price, so the '
                'two are struck on one day.', '2026-09-03', 'Market')
PEER_PB = reg('peer_pb_band', [1.4, 2.2],
              'The price-to-book band Egyptian large-cap banks trade in. It is a BAND and '
              'not a point because this study could not source a same-day book value for '
              'any Egyptian bank other than ADIB itself: the only peer whose price it holds '
              'on the same day is CIB, and CIB\'s own book value is not in this repository. '
              'The band is carried as a cross-check on the two cash-flow lenses, weighted at '
              '15%, and it is NOT allowed to set the answer. Where a multiple cannot be '
              'sourced it is said so rather than filled in.', STUDY_DATE, 'House')
PEER_PE = reg('peer_pe_band', [5.5, 8.5],
              'The trailing price-to-earnings band for the same group, on the same caveat.',
              STUDY_DATE, 'House')


# ----------------------------------------------------------------------------------
# The projection. Every margin below is an OUTPUT.
# ----------------------------------------------------------------------------------
def project(cor=None, yield_path=None, cof_path=None, fin_growth=None):
    cor = cor or COST_OF_RISK
    yp = yield_path or ASSET_YIELD
    cp = cof_path or COST_OF_FUNDS
    fg = fin_growth or FIN_GROWTH

    rows = []
    fin_prev, ta_prev, eq_prev = FY25['financing'], FY25['total_assets'], FY25['equity']
    for i, y in enumerate(YEARS):
        fin = fin_prev * (1 + fg[i])
        ta = fin / FIN_OVER_ASSETS[i]
        avg_ta = (ta_prev + ta) / 2
        avg_fin = (fin_prev + fin) / 2
        avg_ibl = avg_ta * IBL_OVER_ASSETS

        fin_income = yp[i] * avg_ta
        cost_funds = -cp[i] * avg_ibl
        net_funds = fin_income + cost_funds
        net_fees = FEE_RATIO[i] * avg_ta
        other_nii = ONII_RATIO[i] * avg_ta
        other_op = OTHEROP_RATIO[i] * avg_ta
        admin = -(-FY25['admin'] * math.prod([(1 + ADMIN_GROWTH[j]) for j in range(i + 1)]))
        ecl = -cor[i] * avg_fin
        pbt = net_funds + net_fees + other_nii + other_op + admin + ecl
        tax = -TAX_RATE * pbt
        np_ = pbt + tax
        np_parent = np_ * (1 - NCI_SHARE)

        # THE CAPITAL RATIO IS PINNED AND THE DIVIDEND IS WHAT IS LEFT.
        # equity(t) = target x assets(t); dividend(t) = profit + shares issued - the
        # equity build that gets there. Nothing here is typed.
        issue = CAP_INCREASE_26 if y == 2026 else 0.0
        eq = TARGET_EQ_ASSETS * ta
        div = np_parent + issue - (eq - eq_prev)
        payout = div / np_parent if np_parent else 0.0

        rows.append(dict(
            year=y, financing=fin, total_assets=ta, deposits=ta / (FY25['total_assets'] /
                                                                   FY25['deposits']),
            avg_total_assets=avg_ta, fin_income=fin_income, cost_funds=cost_funds,
            net_funds=net_funds, net_fees=net_fees, other_nii=other_nii,
            other_op=other_op, admin=admin, ecl=ecl, pbt=pbt, tax=tax, np=np_,
            np_parent=np_parent, dividend=div, equity=eq, equity_open=eq_prev,
            payout=payout, equity_required=eq - eq_prev, issue=issue,
            # OUTPUTS
            nim=net_funds / avg_ta,
            cost_income=-admin / (net_funds + net_fees + other_nii),
            roa=np_ / avg_ta,
            roe=np_parent / ((eq_prev + eq) / 2),
            eps=np_parent / SHARES, dps=div / SHARES, bvps=eq / SHARES,
            equity_assets=eq / ta,
            # FCFE is the NET flow to shareholders: the dividend LESS what they
            # subscribed. In FY2026 that is negative — a capital call, which is what
            # actually happened.
            fcfe=div - issue))
        fin_prev, ta_prev, eq_prev = fin, ta, eq
    return rows


P = project()


# ----------------------------------------------------------------------------------
# Lens 1 — dividend discount on the payout path
# ----------------------------------------------------------------------------------
def discount_factors(ke_path):
    df, acc = [], 1.0
    for k in ke_path:
        acc *= (1 + k)
        df.append(1.0 / acc)
    return df


DF = discount_factors(KE_PATH)


def ddm():
    pv = sum(P[i]['dividend'] * DF[i] for i in range(len(YEARS)))
    # Terminal: the payout a bank can sustain at its terminal return and growth is
    # DERIVED (1 - g/ROE), never typed.
    roe_term = P[-1]['roe']
    payout_term = max(0.0, min(1.0, 1 - G_TERM / roe_term))
    d_next = P[-1]['np_parent'] * (1 + G_TERM) * payout_term
    tv = d_next / (KE_TERM - G_TERM)
    return dict(pv_explicit=pv, tv=tv, pv_tv=tv * DF[-1],
                equity=pv + tv * DF[-1], payout_term=payout_term, roe_term=roe_term,
                per_share=(pv + tv * DF[-1]) / SHARES)


# ----------------------------------------------------------------------------------
# Lens 2 — free cash flow to equity, after the capital the balance sheet consumes
# ----------------------------------------------------------------------------------
def fcfe():
    pv = sum(P[i]['fcfe'] * DF[i] for i in range(len(YEARS)))
    ta_last = P[-1]['total_assets']
    f_next = (P[-1]['np_parent'] * (1 + G_TERM)
              - TARGET_EQ_ASSETS * ta_last * G_TERM)
    tv = f_next / (KE_TERM - G_TERM)
    return dict(pv_explicit=pv, tv=tv, pv_tv=tv * DF[-1],
                equity=pv + tv * DF[-1], per_share=(pv + tv * DF[-1]) / SHARES,
                fcfe_next=f_next)


# ----------------------------------------------------------------------------------
# Lens 3 — residual income over the cost of equity
# ----------------------------------------------------------------------------------
def residual_income():
    b0 = FY25['equity']
    pv = 0.0
    for i in range(len(YEARS)):
        ri = P[i]['np_parent'] - KE_PATH[i] * P[i]['equity_open']
        pv += ri * DF[i]
    ri_last = P[-1]['np_parent'] - KE_TERM * P[-1]['equity_open']
    tv = ri_last * (1 + G_TERM) / (KE_TERM - G_TERM)
    # The FY2026 cash increase is equity the shareholder PUT IN, not value created.
    eq = b0 + CAP_INCREASE_26 + pv + tv * DF[-1]
    return dict(book0=b0, pv_ri=pv, tv=tv, pv_tv=tv * DF[-1], equity=eq,
                per_share=eq / SHARES)


# ----------------------------------------------------------------------------------
# Lens 4 — relative multiples (a cross-check, weighted 15%, never the answer)
# ----------------------------------------------------------------------------------
def relative():
    bv26 = P[0]['bvps']
    e26 = P[0]['eps']
    pb = [PEER_PB[0] * bv26, PEER_PB[1] * bv26]
    pe = [PEER_PE[0] * e26, PEER_PE[1] * e26]
    mid = (sum(pb) / 2 + sum(pe) / 2) / 2
    return dict(bvps_2026=bv26, eps_2026=e26, pb_range=pb, pe_range=pe, per_share=mid)


# ----------------------------------------------------------------------------------
# Lens 5 — normalised earnings power
# ----------------------------------------------------------------------------------
def normalised():
    """What the bank earns on a mid-cycle margin and a mid-cycle loss charge, capitalised.

    The normalisation is the point: FY2025's 6.64% margin and the June half's near-nil
    loss charge are both cycle-high, and a multiple applied to either capitalises a peak.
    """
    avg_ta = P[0]['avg_total_assets']
    nim_n = 0.055
    net_funds = nim_n * avg_ta
    fees = FEE_RATIO[0] * avg_ta
    onii = ONII_RATIO[0] * avg_ta
    oop = OTHEROP_RATIO[0] * avg_ta
    admin = P[0]['admin']
    ecl = -0.0150 * ((FY25['financing'] + P[0]['financing']) / 2)
    pbt = net_funds + fees + onii + oop + admin + ecl
    np_ = pbt * (1 - TAX_RATE) * (1 - NCI_SHARE)
    cap = np_ / (KE_TERM - G_TERM) * (KE_TERM - G_TERM) / (KE0 - G_TERM)
    return dict(nim_normal=nim_n, cor_normal=0.0150, pbt=pbt, np_parent=np_,
                eps=np_ / SHARES, equity=np_ / (KE0 - G_TERM),
                per_share=np_ / (KE0 - G_TERM) / SHARES)


def book_value():
    """Lens 6 — book value and the return it sustains. The bank class's third named
    cross-check in research_protocol.LENS_REGISTRY.

    Two reads. The FLOOR is attributable book value per share as filed at 30 June 2026 —
    what the shareholder owns if the bank stops compounding tomorrow. The
    SUSTAINABLE-RETURN read capitalises that same book at the price-to-book a Gordon
    inversion supports on the terminal return and the terminal cost of equity, which is
    the most a book-based lens can honestly say about a compounder.
    """
    bvps_filed = H1['equity_parent'] / SHARES
    pb_sustainable = (P[-1]['roe'] - G_TERM) / (KE_TERM - G_TERM)
    return dict(bvps_filed=bvps_filed, pb_sustainable=pb_sustainable,
                floor=bvps_filed, per_share=bvps_filed * pb_sustainable)


DDM, FCFE, RI, REL, NORM = ddm(), fcfe(), residual_income(), relative(), normalised()
BOOK = book_value()

# ----------------------------------------------------------------------------------
# [R-LENS-03] ONE CLASS PRIMARY IS THE CENTRAL. THERE IS NO TYPED BLEND HERE.
#
# research_protocol.LENS_REGISTRY['bank'] = ('ddm', ['residual_income',
# 'relative_multiple', 'book_value']). The dividend discount IS the central; the others
# are cross-checks published beside it in one table. The typed blend is RETIRED: PHDC's
# four-lens weighted answer landed 28% below a market its own cash-flow lens matched
# within 2.2%, and the weights had never cleared any out-of-sample test.
#
# THE ENVELOPE IS THE RANGE OF THE PRESENT-VALUE READS ON ONE CLOCK, and nothing is
# invented around it. Three of the six lenses discount a flow; the relative multiple, the
# book-value read and normalised earnings power are not present-value reads, are
# published, and do not enter the envelope.
# ----------------------------------------------------------------------------------
PRIMARY = 'ddm'
PV_READS = dict(ddm=DDM['per_share'], fcfe=FCFE['per_share'],
                residual_income=RI['per_share'])
CENTRAL = PV_READS[PRIMARY]
BEAR = min(PV_READS.values())
FULL = max(PV_READS.values())

reg('lens_architecture', 'class primary = dividend discount; no typed blend',
    'The bank class is keyed to a dividend-discount PRIMARY with residual income, a '
    'relative multiple and book value beside it. The central IS the primary. The envelope '
    'is the range of the three present-value reads and no spread is invented around '
    'it.', STUDY_DATE, 'House')


# ----------------------------------------------------------------------------------
# The band — from the walk-forward's own error distribution, and from nowhere else
# ----------------------------------------------------------------------------------
_FR = json.load(open(os.path.join(ENGINE, 'adib_walkforward', 'forward_ranges.json'),
                     encoding='utf-8'))


def far_year_band():
    """Years 3-5 as ranges, from this record's own driver-error distribution.

    THE BAND IS CENTRED, NOT LEVELLED. The measured distribution has a large negative
    median — the mechanical rule under-forecast attributable profit by 0.9 in logs at
    three years — because it holds ADIB's share of system credit FLAT and ADIB has taken
    share every year for a decade. THIS STUDY DOES NOT HOLD SHARE FLAT, so carrying the
    mechanical rule's LEVEL error into a forecast that does not contain it would
    double-count the very bias the study corrected by construction. What carries over is
    the DISPERSION around the distribution's own median, which is the irreducible
    uncertainty of a three-to-five-year bank forecast in Egypt across a devaluation
    cycle. It is wide, it is measured, and it is not narrowed by choosing the tighter of
    the two samples: the FULL record is used.
    """
    out = {}
    for h, y in ((3, 2028), (4, 2029), (5, 2030)):
        d = _FR['lines']['np_parent']['h%d' % h]['all_origins']
        lo = math.exp(-(d['p90'] - d['p50']))
        hi = math.exp(-(d['p10'] - d['p50']))
        pt = P[h - 1]['np_parent']
        out[y] = dict(n=d['n'], low=pt * lo, point=pt, high=pt * hi,
                      low_mult=lo, high_mult=hi,
                      low_eps=pt * lo / SHARES, eps=pt / SHARES, high_eps=pt * hi / SHARES)
    return out


FAR = far_year_band()

_b3 = FAR[2028]

reg('band_construction', 'the range of the present-value reads [R-LENS-03]',
    'Bear is the free-cash-flow-to-equity read, full the residual-income read, and the '
    'central the dividend-discount primary between them. THE ENVELOPE IS NARROW BECAUSE '
    'THE THREE LENSES AGREE, AND THAT IS A STATEMENT ABOUT LENS AGREEMENT RATHER THAN '
    'ABOUT FORECAST CONFIDENCE. The fundamental walk-forward beneath this study measured a '
    'three-year attributable-profit dispersion of x{lo:.2f} to x{hi:.2f} on eight cells; '
    'that distribution sets the YEARS 3-5 PROFIT RANGES in Appendix A and nothing else, '
    'and section 7 says so in terms rather than letting a tight envelope imply a precision '
    'this record does not have.'.format(lo=_b3['low_mult'], hi=_b3['high_mult']),
    STUDY_DATE, 'House')


# ----------------------------------------------------------------------------------
# Sensitivity
# ----------------------------------------------------------------------------------
def sensitivity():
    out = []
    base = CENTRAL

    def recentral(**kw):
        global P, DDM, FCFE, RI, REL, NORM
        keep = P
        P = project(**kw)
        d, f, r, rl = ddm(), fcfe(), residual_income(), relative()
        P = keep
        return d['per_share']            # the PRIMARY [R-LENS-03], never a blend

    for lab, kw in [
        ('cost of risk +50bp', dict(cor=[c + 0.005 for c in COST_OF_RISK])),
        ('cost of risk -50bp', dict(cor=[max(0, c - 0.005) for c in COST_OF_RISK])),
        ('asset yield -50bp', dict(yield_path=[y - 0.005 for y in ASSET_YIELD])),
        ('asset yield +50bp', dict(yield_path=[y + 0.005 for y in ASSET_YIELD])),
        ('cost of funds +50bp', dict(cof_path=[c + 0.005 for c in COST_OF_FUNDS])),
        ('cost of funds -50bp', dict(cof_path=[c - 0.005 for c in COST_OF_FUNDS])),
        ('financing growth -5pp/yr', dict(fin_growth=[g - 0.05 for g in FIN_GROWTH])),
        ('financing growth +5pp/yr', dict(fin_growth=[g + 0.05 for g in FIN_GROWTH])),
    ]:
        v = recentral(**kw)
        out.append((lab, v, v / base - 1))

    # cost-of-capital sensitivities act on the discount rate, not on the projection
    for lab, dke in [('risk-free +200bp', 0.02), ('risk-free -200bp', -0.02)]:
        global KE_PATH, KE_TERM, DF
        k0, kt, df = KE_PATH, KE_TERM, DF
        KE_TERM = kt + dke
        KE_PATH = [k + dke for k in k0]
        DF = discount_factors(KE_PATH)
        v = ddm()['per_share']
        KE_PATH, KE_TERM, DF = k0, kt, df
        out.append((lab, v, v / base - 1))

    for lab, dg in [('terminal growth +100bp', 0.01), ('terminal growth -100bp', -0.01)]:
        global G_TERM
        g0 = G_TERM
        G_TERM = g0 + dg
        v = ddm()['per_share']
        G_TERM = g0
        out.append((lab, v, v / base - 1))
    return out


SENS = sensitivity()


def summary():
    return dict(ticker='ADIB', company='Abu Dhabi Islamic Bank (ADIB) – Egypt S.A.E.',
                exchange='EGX', currency='EGP', study_date=STUDY_DATE,
                spot=SPOT, spot_date='2026-09-03', shares=SHARES,
                central=CENTRAL, bear=BEAR, full=FULL,
                gap_to_spot=CENTRAL / SPOT - 1,
                ke=KE0, ke_rating=KE_RATING, ke_terminal=KE_TERM, beta=BETA,
                primary=PRIMARY,
                lenses=dict(ddm=DDM['per_share'], fcfe=FCFE['per_share'],
                            ri=RI['per_share'], relative=REL['per_share'],
                            book=BOOK['per_share'], normalised=NORM['per_share']))


if __name__ == '__main__':
    s = summary()
    print('ADIB-Egypt (EGX: ADIB) — %s' % STUDY_DATE)
    print('spot EGP %.2f (%s)   shares %.0fmn' % (s['spot'], s['spot_date'], SHARES))
    print()
    print('BASE YEAR FY2025, observed (all OUTPUTS):')
    for k in ('asset_yield', 'cost_of_funds', 'nim', 'fee_ratio', 'cost_of_risk',
              'cost_income', 'tax_rate', 'roe', 'roa', 'financing_over_assets',
              'equity_over_assets'):
        print('   %-22s %8.3f%%' % (k, 100 * OBS[k]))
    print('H1-2026 annualised: NIM %.3f%%  ROE %.2f%%  cost of risk %.4f%%'
          % (100 * H1OBS['nim'], 100 * H1OBS['roe'], 100 * H1OBS['cost_of_risk']))
    print()
    print('COST OF EQUITY: rf %.2f%% - sovereign spread %.2f%% = rf* %.2f%%; + beta %.4f x '
          'ERP %.4f%% = %.2f%%' % (100 * RF, 100 * SOV_SPREAD, 100 * rf_star, BETA,
                                   100 * ERP, 100 * KE0))
    print('   rating basis %.2f%% (%.0fbp apart) | double-counted construction %.2f%% '
          '(retired) | terminal %.2f%%'
          % (100 * KE_RATING, abs(KE0 - KE_RATING) * 1e4, 100 * KE_DOUBLE, 100 * KE_TERM))
    print('   glide: ' + ' -> '.join('%.2f%%' % (100 * k) for k in KE_PATH)
          + ' -> %.2f%%' % (100 * KE_TERM))
    print()
    print('PROJECTION (EGP mn)')
    print('%-6s %11s %11s %9s %9s %9s %8s %8s %8s %8s %8s'
          % ('year', 'financing', 'assets', 'net funds', 'PBT', 'attrib', 'NIM', 'C/I',
             'ROE', 'EPS', 'BVPS'))
    for r in P:
        print('%-6d %11.0f %11.0f %9.0f %9.0f %9.0f %7.2f%% %7.1f%% %7.1f%% %8.2f %8.2f'
              % (r['year'], r['financing'], r['total_assets'], r['net_funds'], r['pbt'],
                 r['np_parent'], 100 * r['nim'], 100 * r['cost_income'], 100 * r['roe'],
                 r['eps'], r['bvps']))
    print()
    print('LENSES (EGP per share)')
    print('   dividend discount      %8.2f   (terminal payout %.0f%% DERIVED from a %.1f%% '
          'terminal return)' % (DDM['per_share'], 100 * DDM['payout_term'],
                                100 * DDM['roe_term']))
    print('   free cash to equity    %8.2f' % FCFE['per_share'])
    print('   residual income        %8.2f' % RI['per_share'])
    print('   relative multiples     %8.2f   (P/B %.1f-%.1f x BVPS %.2f; P/E %.1f-%.1f x '
          'EPS %.2f)' % (REL['per_share'], PEER_PB[0], PEER_PB[1], REL['bvps_2026'],
                         PEER_PE[0], PEER_PE[1], REL['eps_2026']))
    print('   book value + sustainable return %8.2f   (filed BVPS %.2f x sustainable '
          'P/B %.2fx)' % (BOOK['per_share'], BOOK['bvps_filed'], BOOK['pb_sustainable']))
    print('   normalised earnings power %8.2f' % NORM['per_share'])
    print('   PRIMARY = %s [R-LENS-03]; every other lens is a cross-check' % PRIMARY)
    print()
    print('CENTRAL %.2f   BEAR %.2f   FULL %.2f   against spot %.2f -> %+.1f%%'
          % (CENTRAL, BEAR, FULL, SPOT, 100 * (CENTRAL / SPOT - 1)))
    print()
    print('YEARS 3-5 AS RANGES, from the walk-forward\'s own error dispersion:')
    for y in sorted(FAR):
        f = FAR[y]
        print('   %d attributable  EGP %,.0f .. %,.0f mn (point %,.0f)  EPS %.2f .. %.2f '
              '(point %.2f)  n=%d'.replace(',', '')
              % (y, f['low'], f['high'], f['point'], f['low_eps'], f['high_eps'],
                 f['eps'], f['n']))
    print()
    print('SENSITIVITY')
    for lab, v, d in SENS:
        print('   %-26s %8.2f  %+7.1f%%' % (lab, v, 100 * d))
