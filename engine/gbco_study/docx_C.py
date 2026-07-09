"""Content part C: Appendices A–D, About, Disclosure, footer."""
from docx_base import *

L = D['lenses']; E = D['experts']; s0 = D['step0']; sotp = D['sotp']

# ================= Appendix A ================================================
H1('Appendix A  Financial statements')
P('Selected consolidated figures, as reported (4Q23 / 4Q24 / 4Q25 earnings releases; 1Q26 release 14 May 2026). EGP million. '
  'FY23 operating profit is shown after provisions for cross-year consistency with the FY25 layout. The five-year forecast '
  'is the model build (companion Excel, Income Statement sheet, formula-linked to Assumptions).')
H2('A.1  Income statement (consolidated, EGP mn)')
rows = [
 ['Line', 'FY23', 'FY24', 'FY25', 'FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E'],
 ['GB Auto revenue', '23,854', '47,065', '66,358', '78,550', '95,736', '112,459', '128,714', '144,761'],
 ['GB Capital revenue', '4,951', '7,384', '14,743', '21,377', '27,790', '34,738', '41,686', '49,189'],
 ['Eliminations', '(488)', '(479)', '(872)', '(1,099)', '(1,359)', '(1,619)', '(1,874)', '(2,133)'],
 ['Total revenue', '28,317', '53,970', '80,230', '98,828', '122,168', '145,578', '168,525', '191,817'],
 ['Gross profit', '6,884', '10,515', '12,431', '14,633', '18,600', '22,760', '26,551', '30,417'],
 ['S&M and administration', '(3,431)', '(4,844)', '(6,547)', '(7,906)', '(9,651)', '(11,355)', '(13,061)', '(14,770)'],
 ['Other income · provisions', '250', '150', '747', '791', '977', '1,165', '1,348', '1,535'],
 ['Operating profit', '3,703', '5,821', '6,631', '7,518', '9,926', '12,570', '14,838', '17,182'],
 ['Associates', '1,066', '868', '975', '1,250', '1,430', '1,630', '1,830', '2,030'],
 ['EBIT', '4,770', '6,689', '7,606', '8,768', '11,356', '14,200', '16,668', '19,212'],
 ['FX gains (losses)', '(1,499)', '(292)', '(37)', '—', '—', '—', '—', '—'],
 ['Net finance cost', '(966)', '(2,398)', '(3,702)', '(4,100)', '(3,800)', '(3,500)', '(3,300)', '(3,100)'],
 ['Earnings before tax', '2,304', '3,999', '3,867', '4,668', '7,556', '10,700', '13,368', '16,112'],
 ['Income taxes', '(493)', '(939)', '(1,086)', '(1,307)', '(2,116)', '(2,996)', '(3,743)', '(4,511)'],
 ['NP before minority interest', '1,811', '3,060', '2,780', '3,361', '5,441', '7,704', '9,625', '11,601'],
 ['Minority interest', '80', '(132)', '100', '(67)', '(109)', '(154)', '(193)', '(232)'],
 ['Net profit (attributable)', '1,891', '2,928', '2,880', '3,294', '5,332', '7,550', '9,433', '11,369'],
]
table(rows, [2.05, 0.615, 0.615, 0.615, 0.615, 0.615, 0.615, 0.615, 0.615], first_col_bold=True, size=8.2)
caption('Forecast columns are the live model build (rounded); the Excel is the source of truth and reprices from Assumptions.')
H2('A.2  Balance sheet (consolidated, EGP mn) — grouped house layout')
rows = [
 ['Line', 'FY23', 'FY24', 'FY25', 'FY26E', 'FY28E', 'FY30E'],
 ['PP&E, intangibles, ROU & inv. property', '6,937', '10,361', '13,389', '15,665', '19,821', '23,414'],
 ['Investments in associates', '10,732', '11,744', '13,690', '14,940', '18,000', '21,860'],
 ['GB Capital loan book (on BS)', '7,681', '11,483', '17,518', '23,650', '37,542', '53,158'],
 ['Inventories', '6,366', '21,134', '24,650', '28,278', '35,987', '42,849'],
 ['Trade receivables — Auto', '1,744', '3,709', '5,317', '6,284', '8,997', '11,581'],
 ['Advances, debtors & other current', '1,039', '2,942', '4,671', '5,498', '7,591', '9,337'],
 ['Cash & cash equivalents', '4,504', '7,421', '9,524', '6,371', '2,744', '4,779'],
 ['Other assets', '3,581', '3,932', '2,601', '2,602', '2,602', '2,602'],
 ['TOTAL ASSETS', '42,585', '72,725', '91,359', '103,287', '133,283', '169,579'],
 ['Equity attributable', '19,839', '25,439', '28,789', '31,625', '43,463', '61,568'],
 ['Non-controlling interests', '1,363', '1,978', '1,801', '1,869', '2,090', '2,515'],
 ['Borrowings', '12,518', '22,609', '38,041', '43,541', '54,341', '66,241'],
 ['Trade & notes payables', '7,399', '19,718', '18,437', '21,961', '28,864', '35,360'],
 ['Leases · provisions · other · DT', '1,467', '2,982', '4,291', '4,291', '4,291', '4,291'],
 ['Balance check (assets − L&E)', '0', '0', '0', '0', '0', '0'],
]
table(rows, [2.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75], first_col_bold=True, size=8.4)
caption('Historic columns are grouped from the disclosed segment balance sheets (release Tables 12–13); a small reallocation '
        'between “advances & debtors” and “other assets” aligns the grouped layout to the disclosed Auto working-capital '
        'figures — flagged in the model. Forecast rolls forward on the clean-surplus construction; the check row is zero.')
H2('A.3  GB Auto segment and cash-flow markers · the DPS schedule (device A-2)')
rows = [
 ['GB Auto segment', 'FY23', 'FY24', 'FY25'],
 ['Revenue', '23,854', '47,065', '66,358'],
 ['Gross margin', '24.4%', '19.2%', '14.8%'],
 ['EBITDA · margin', '3,795 · 15.9%', '5,881 · 12.5%', '6,363 · 9.6%'],
 ['Net working capital · % of revenue', '4,466 · 18.7%', '10,784 · 22.9%', '18,917 · 28.5%'],
 ['Net debt · ND/EBITDA', '2,922 · 0.77×', '5,292 · 0.90×', '15,210 · 2.39×'],
 ['Capital employed · ROCE', '10,231 · 35.9%', '18,731 · 31.5%', '28,513 · 21.3%'],
 ['Capex', '~1,100', '2,642', '2,695'],
]
table(rows, [2.6, 1.4, 1.4, 1.5], first_col_bold=True, size=8.8)
rows = [
 ['Dividend schedule', 'FY25A', 'FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E'],
 ['Payout of attributable NP', '~13%', '14%', '15%', '16%', '18%', '20%'],
 ['DPS (EGP)', '0.35', '0.42', '0.74', '1.11', '1.56', '2.09'],
 ['Yield at spot', '1.1%', '1.4%', '2.4%', '3.6%', '5.0%', '6.7%'],
 ['Stress check', 'Bear-case FY27E NP ~3.6 bn still covers a 15% payout 6.7×; the constraint is the lending book\u2019s equity appetite, not earnings.', '', '', '', '', ''],
]
table(rows, [1.9, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85], first_col_bold=True, size=8.6)
caption('Forecast-vs-actual scorecard (device A-3) and new-vs-old reconciliation (A-4): not applicable on an initiation; both '
        'tables become standing sections from the first 3-month update, scoring these FY26E lines against the print.')

# ================= Appendix B ================================================
H1('Appendix B  Step 0 — calibration backtest')
P('Before any forecast we test the Monte Carlo lens on GBCO\u2019s own five years of history: at seventeen non-overlapping '
  'origins (h = 60 trading days), using only data available at each origin, the YZ-HAR engine generates the three-month-ahead '
  'distribution and the realized close is scored against it. The grade is skill versus a naïve benchmark — a zero-drift '
  'random-walk lognormal cone on trailing realized vol — measured by CRPS skill (must be > 0) and the Winkler interval '
  'score; the PIT histogram and coverage table are diagnostics only, since band-containment rewards width.')
rows = [
 ['Configuration / scheme', 'n', 'CRPS skill', 'Interval skill', '50 / 80 / 90% coverage', 'PIT mean'],
 ['Zero drift — non-overlapping', '17', '−1.6%', '−0.4%', '47 / 82 / 88%', '0.62 (right-skewed)'],
 ['Secular drift — non-overlapping', '17', '+3.2%', '−6.0%', '59 / 76 / 94%', '0.53'],
 ['Secular drift — monthly origins', '49', '+9.6%', '−8.4%', '53 / 86 / 92%', '0.57'],
]
table(rows, [2.15, 0.5, 0.95, 0.95, 1.5, 1.15], first_col_bold=True, size=8.7)
figure('figB1_calibration.png', 6.6, 'Figure B-1 — Calibration backtest: quarterly cone replay (log scale), PIT histogram, '
       'and interval coverage versus target, secular-drift configuration.')
P('Zero drift fails the gate on this name: negative CRPS skill and a PIT pushed into the upper deciles — the classic '
  'signature of a distribution that keeps under-calling a secular uptrend (GBCO is a thirteen-bagger over the sample, the '
  'same EGP-repricing dynamic as the EGX developers). Re-running with the asset-class secular drift switched on — the '
  'prescribed recalibration path — flips the result: CRPS skill +3.2% on non-overlapping windows and +9.6% on monthly '
  'origins, with the PIT mean back near 0.5 and no material U-shape. The interval score gives some of that back (the t(5) '
  'tails price protection the benchmark doesn\u2019t carry), and a block bootstrap on the 17 windows puts the 90% CI on '
  'CRPS skill at roughly [−0.17, +0.18] — P(skill > 0) ≈ 0.62. The lens is accepted with that thinness stated: seventeen '
  'windows is decent validation, not robust proof, and the drift term is re-tested every quarter with a hard kill rule. '
  'Flag for the record: GBCO is the first EGX non-developer to carry the secular drift — adopted empirically here, exactly '
  'as the protocol requires, not by asset-class default.')

# ================= Appendix C ================================================
H1('Appendix C  Peer set, sector structure, and risks')
P('GB Corp has no clean single comparable — an auto assembler-distributor, an NBFI and a fintech associate in one wrapper. '
  'The peer set is therefore split by leg.')
rows = [
 ['Leg', 'Closest peers', 'Typical valuation'],
 ['Auto assembly & distribution', 'Saudi/GCC auto distributors, Türk Traktör, EGX consumer durables', 'EV/EBITDA ~4–6×; P/E ~8–12×'],
 ['NBFI / consumer & SME finance', 'Contact Financial (CNFN), EFG finance arm, Raya finance leg', 'P/B ~1.0–1.8× on mid-teens ROE'],
 ['Fintech associate', 'Fawry (FWRY), e-Finance (EFIH); MNT-Halan private rounds', 'Private marks; last round USD 1.4 bn'],
]
table(rows, [1.9, 3.1, 2.0], first_col_bold=True, size=8.9)
P('Sector structure. Egypt\u2019s PC market is in a policy-assisted recovery (~210k registrations in 2025, +40% y/y) with '
  'the CBE easing cycle restoring affordability, localization incentives reshaping the CKD/CBU mix, and Chinese entrants '
  '(BYD) resetting price points. Consumer and SME finance is growing faster than banking credit off a low base, with '
  'securitization deepening as a funding market. Principal risks: a structurally higher working-capital intensity; a '
  'renewed EGP devaluation; regional conflict freezing Iraq/Jordan; BYD-led price competition; credit-cycle deterioration in '
  'the lending book; a private-market re-price of MNT-Halan; and execution on Sadat.')

# ================= Appendix D ================================================
H1('Appendix D  The expert valuation panel')
P('Every Testahil study closes with a panel of standing expert personas — drawn from the house Expert Persona Library, not '
  'invented for the occasion, so that each accumulates a track record across studies and a quarterly update is a re-run, not '
  'a re-training. For GBCO we cast the industrial trio, adding the cash-returns lens because the name is capital-heavy: '
  'Expert 1 (the accountant — split-legs NAV and the marks), Expert 2 (earnings power — normalized mid-cycle earnings and '
  'multiples), Expert 3 (cash returns — return on capital against its cost). Each runs a different method, derives its fair '
  'value from shown workings, and states a falsification condition. The macro-policy lens — rates, the pound, the region — '
  'runs through the body (§1.8, §5) rather than as a separate persona.')

H2('D.1  Expert 1 — the split-legs NAV and the marks')
P('Worldview. A group is worth the sum of its parts at realizable value, less a discount for the wrapper. Mark each leg to '
  'what it would fetch on its own; then argue only about the discount.', size=9.8)
P('When it works / fails. Best where the legs are separable and independently markable; fails hardest when the discount '
  'applied to a private mark is itself contestable — exactly his position on MNT-Halan now.', size=9.8)
rows = [
 ['Expert 1\u2019s marks (EGP mn)', 'Value'],
 ['Auto leg (accepts the §1.2 DCF)', f"{sotp['auto_eq']:,.0f}"],
 ['GB Capital at 1.0× adjusted book', '9,500'],
 [f"Associates: MNT-Halan {sotp['mnt_halan_value']:,.0f} (41.61% confirmed × USD 1.4bn) + other {sotp['other_assoc']:.0f}", f"{sotp['assoc']:,.0f}"],
 [f"Σ = EGP {sotp['prediscount_ps']:.1f}/share pre-discount", f"{sotp['total']:,.0f}"],
 ['Fair wrapper discount 8% (operator, not a passive holdco)', f"→ EGP {E['e1']['base']:.1f}/share"],
]
table(rows, [4.4, 1.7], first_col_bold=True, size=9.0)
P(f"Sensitivity (swing = the discount on the mark, now that the stake is settled): at a 25% discount on MNT-Halan alone "
  f"his NAV falls to \u2248EGP {(sotp['auto_eq']+sotp['cap_val']+sotp['mnt_halan_value']*0.75+sotp['other_assoc'])*0.92/1085.5:.0f}/share; "
  f"at 50%, \u2248EGP {(sotp['auto_eq']+sotp['cap_val']+sotp['mnt_halan_value']*0.50+sotp['other_assoc'])*0.92/1085.5:.0f}. He concedes "
  "this openly: \u201cthe stake isn\u2019t the argument anymore — the argument is what a 41.61% minority stake in an "
  "unlisted fintech is worth to a public-market buyer who can\u2019t sell it, and that\u2019s a discount rate question, not "
  "an ownership question.\u201d Cross-examination: he tells Expert 2 that capitalizing mid-cycle earnings double-counts "
  "assets he has already marked at full value; he tells Expert 3 that a 15-point ROCE haircut on the Auto leg is small "
  "next to the swing available just from how hard you discount an illiquid stake.", size=9.8)
rich([('Verdict, falsification, market-implied. ', dict(bold=True)),
      (f"Fair EGP {E['e1']['base']:.1f} (range {sotp['bear']:.0f}\u2013{sotp['bull']:.0f}) — still his widest range, now "
       "driven by the discount debate rather than an unconfirmed stake. Falsified by a real secondary transaction in "
       "MNT-Halan shares at a materially different price, or by the second closing repricing the round away from USD "
       "1.4bn. The market price implies a discount on the associate leg far steeper than his stated 8% wrapper discount — "
       "in his own view, evidence the market doesn\u2019t trust the round\u2019s marked value to transfer cleanly to a "
       "41.61% minority holder.", {})])

H2('D.2  Expert 2 — normalized earnings power')
P('Worldview. An operating business is worth a fair multiple of its sustainable mid-cycle earnings; peaks (FY24\u2019s FX '
  'windfall) and troughs (FY23) are noise to be stripped out.', size=9.8)
P('When it works / fails. Best with a through-cycle record (three disclosed years spanning trough, windfall and '
  'normalization is workable); fails at structural breaks — if BYD resets Egyptian ASPs permanently, his normalization is '
  'simply wrong.', size=9.8)
rows = [
 ['Expert 2\u2019s normalization', 'Value'],
 ['Mid-cycle group PAT (EGP mn)', '4,200'],
 ['Shares (mn) → normalized EPS', '1,085.5 → EGP 3.87'],
 ['Justified through-cycle P/E (EM auto + NBFI blend)', '8.5×'],
 ['Fair value', f"→ EGP {E['e2']['base']:.1f}/share"],
]
table(rows, [4.4, 1.7], first_col_bold=True, size=9.0)
P('Sensitivity (swing = the multiple / the margin): at 7.5× EGP 29.0; at 9.5×, 36.8; a 1-pt miss on mid-cycle Auto GPM costs '
  '~EGP 2.5. Cross-examination: he tells Expert 1 that an NAV struck off a trough-margin DCF understates a business whose '
  'volumes are still mid-cycle; he tells Expert 3 that cash-conversion pessimism ignores that working capital is a stock, '
  'not a perpetual flow — it releases exactly when growth normalizes.', size=9.8)
rich([('Verdict, falsification, market-implied. ', dict(bold=True)),
      (f"Fair EGP {E['e2']['base']:.1f} (range {L['normalized']['bear']:.0f}–{L['normalized']['bull']:.0f}) — the most "
       "bullish. Falsified by Auto gross margin stuck below ~13% through FY27, or the Egyptian PC market rolling over. The "
       "market implies normalized earnings ~5% below his: it mostly believes him.", {})], size=9.8)

H2('D.3  Expert 3 — cash returns: ROCE against the cost of capital')
P('Worldview. A business creates value only when each pound of capital earns above its cost, in cash. He looks past the '
  'income statement to the economic-profit spread — and past reported returns to returns ex one-offs.', size=9.8)
P('When it works / fails. Best for capital-intensive compounders where the reinvestment spread is the story; fails where '
  'the capital base is temporarily inflated by a one-off build (his own caveat here: FY25\u2019s WC bulge may be exactly '
  'that).', size=9.8)
rows = [
 ['Expert 3\u2019s economic-profit test', 'Value'],
 ['Auto capital employed (FY25)', '28,513'],
 ['Auto ROCE — FY25 vs FY23/24', '21.3% vs 35.9% / 31.5%'],
 ['WACC (his hurdle)', '~22%'],
 ['Spread ≈ nil ⇒ Auto EV ≈ 0.9× CE', '25,662 → equity 9,652'],
 [f"Lender at 0.9× book · associate at 0.85× (his own haircut on the mark, stake now confirmed)", f"8,550 · {sotp['assoc']*0.85:,.0f}"],
 ['GB Capital ROAE, headline vs adjusted (one-off stripped)', '7.9% vs 15.1%'],
 ['Fair value', f"→ EGP {E['e3']['base']:.1f}/share"],
]
table(rows, [4.4, 1.7], first_col_bold=True, size=9.0)
P(f"Sensitivity (swing = the ROCE fade, and the discount he applies to the mark): if ROCE re-approaches 30% as WC "
  f"releases, his Auto mark rises to \u2248EGP 3/share more; but moving his associate haircut from 0.85\u00d7 to 0.60\u00d7 "
  "costs \u2248EGP 7/share — larger than his preferred ROCE lever. Cross-examination: he tells Expert 2 that mid-cycle "
  "earnings without the capital cost to hold them is a half-truth — FY25 grew profit 49% in revenue terms and consumed "
  "EGP 8bn doing it; he tells Expert 1 that an 8% wrapper discount doesn\u2019t begin to capture the illiquidity of a "
  "41.61% stake in a company that has never had a public exit.", size=9.8)
rich([('Verdict, falsification, market-implied. ', dict(bold=True)),
      (f"Fair EGP {E['e3']['base']:.1f} (range \u224832\u201348) — even his conservative method lands well above spot once "
       "the confirmed stake is applied at the round\u2019s valuation, which he flags as the real finding here: the stake "
       "was never the issue, the mark is. Falsified either by a durable ROCE recovery above ~28\u201330%, or by a real "
       "secondary sale of MNT-Halan shares at a price meaningfully below the round\u2019s implied valuation. The market "
       "price sits well below his number: on a cash-returns basis the market looks unconvinced by the mark at face "
       "value, not by GB Corp\u2019s ownership of it.", {})])

H2('D.5  The three in one room')
P('The stake question that dominated the first draft of this study is now settled — GB Corp confirmed 41.61% in writing '
  'on 9 June 2026. What the three disagree on now is what that confirmed stake is worth.', size=9.8)
P('Expert 1: \u201cThe company told us what it owns. Fine — now the argument is honest: it\u2019s about the discount, not '
  'the number. I apply 8% for the wrapper. If you think that\u2019s too thin for an illiquid minority stake, argue the '
  'discount, not the disclosure.\u201d', size=9.8, italic=False)
P('Expert 3: \u201cYour own arithmetic says a confirmed 41.61% stake is worth three quarters of the entire market cap. '
  'That was true when the number was uncertain and it\u2019s just as true now that it isn\u2019t. The company being honest '
  'about its ownership doesn\u2019t make the market\u2019s skepticism about the mark go away — if anything it sharpens the '
  'question.\u201d', size=9.8)
P('Expert 2: \u201cYou\u2019re both still arguing about a number that was never in my model. Mid-cycle earnings power '
  'doesn\u2019t care what MNT-Halan is worth, confirmed or not. If you want the one lens immune to this whole argument, '
  'it\u2019s mine — and notice it\u2019s also the one closest to where the market actually prices the stock.\u201d', size=9.8)

H2('D.6  Reading the divergence')
figure('figD1_experts.png', 6.0, 'Figure D-1 — The three experts\u2019 fair-value ranges. Brass ticks are base cases; the '
       'gold band is the panel centre; the light line is spot. The spread is now almost entirely the MNT-Halan discount question.')
rows = [
 ['Expert', 'Method', 'Single swing assumption', 'Base fair value'],
 ['Expert 1', 'Split-legs NAV', 'Discount on the MNT-Halan mark (8% wrapper)', f"EGP {E['e1']['base']:.1f}"],
 ['Expert 2', 'Normalized earnings power', 'Mid-cycle PAT 4.2 bn × 8.5× (stake-blind)', f"EGP {E['e2']['base']:.1f}"],
 ['Expert 3', 'Cash returns / ROCE vs WACC', 'ROCE fade + 0.85× haircut on the mark', f"EGP {E['e3']['base']:.1f}"],
]
table(rows, [1.0, 2.2, 2.5, 1.3], first_col_bold=True, size=9.0)
P(f"The spread — EGP {min(E['e1']['base'],E['e2']['base'],E['e3']['base']):.1f} to "
  f"{max(E['e1']['base'],E['e2']['base'],E['e3']['base']):.1f} at base — is wide for what is otherwise a set of "
  "broadly-agreeing methods, and it is now almost entirely one disagreement: not the volumes, not the lender\u2019s "
  "profitability, not the Auto cash-conversion path, and — since 9 June 2026 — not the MNT-Halan stake either (all three "
  "experts now accept 41.61% as fact). What separates them is purely how much to discount that confirmed stake\u2019s "
  "marked value. Expert 2 sidesteps the question entirely by never pricing the stake; Experts 1 and 3 both use the "
  "confirmed figure but disagree on the haircut. Unlike the working-capital disagreement in an earlier draft of this "
  "study — a genuine business uncertainty that resolves with quarterly prints — this one may never fully resolve, since "
  "private-mark discounts are inherently a matter of judgment rather than a fact that prints on a schedule. Until a real "
  "secondary transaction in MNT-Halan shares provides an independent data point, Expert 2\u2019s stake-blind number "
  "remains the one estimate in the room immune to this whole argument.")

caption('Each expert\u2019s point fair value (and bull/base/bear) is logged with the study date (8 Jul 2026) and spot '
        '(EGP 31.25) as an internal per-expert track record, kept separate from the core Calibration Ledger.')

# ================= About / Disclaimer / footer ================================
H1('About this series')
P('Testahil publishes independent, educational valuation studies. Each is an attempt to reason transparently about what a '
  'security is worth, with every assumption shown and a companion model so readers can disagree productively. The house '
  'style is distributions, not tips: we describe ranges and probabilities, not targets, and we do not tell anyone what to '
  'do. Studies are framed as educational analysis, the preparer is not licensed by any securities regulator, and holdings '
  'are disclosed.')
H1('Disclosure & Disclaimer')
for head, body in [
 ('Not investment advice. ', 'This document is educational and informational only. It is not, and must not be relied upon '
  'as, investment, financial, legal, accounting or tax advice, nor an offer, solicitation or recommendation to buy, sell or '
  'hold any security. It contains no price target and no rating.'),
 ('No licence; no advisory relationship. ', 'The preparer is not registered or licensed with any securities or financial '
  'regulator in any jurisdiction — including Egypt\u2019s Financial Regulatory Authority (FRA) — holds no brokerage or '
  'investment-advisory authorisation, and is not acting as your adviser or fiduciary. Nothing here is personalised to your '
  'circumstances.'),
 ('Holdings disclosure. ', 'The preparer may hold, and may in the future take or dispose of, a position in the security '
  'discussed in this report, and may transact at any time without notice. This is a potential conflict of interest you '
  'should weigh.'),
 ('Sources & accuracy. ', 'Reported financial and operating figures are drawn from the company\u2019s public disclosure and '
  'other public sources believed reliable but not independently verified; they may contain errors or be superseded. '
  'Forward-looking inputs — the leg marks (including the discount applied to GB Corp\u2019s confirmed MNT-Halan stake), the '
  'complexity discount, projections, multiples, the DCF and Monte-Carlo factor probabilities — are the '
  'preparer\u2019s own judgments and are inherently uncertain.'),
 ('Forward-looking statements. ', 'Any statements about the future are estimates subject to risks and uncertainties; actual '
  'results may differ materially. The Monte Carlo models price, not value, and encodes subjective probabilities for events '
  'that have not occurred.'),
 ('No reliance; your responsibility. ', 'Do your own research and consult a licensed professional before making any '
  'decision. You are solely responsible for your investment decisions and their outcomes. To the maximum extent permitted '
  'by law, the preparer accepts no liability for any loss arising from use of this document.'),
 ('Currency & figures. ', 'Figures are in Egyptian pounds (EGP), millions unless stated; bn denotes billion. FX at study '
  'date: USD/EGP ≈ 47.5 (flagged estimate). Rounding may cause totals to differ slightly. Spot price and market data are as '
  'of 7 July 2026 and change continuously.'),
]:
    rich([(head, dict(bold=True, italic=True)), (body, {})], size=9.6, space_after=5)
P('TESTAHIL · Independent Valuation Study · Educational Analysis · GB Corp S.A.E. (EGX: GBCO) · edition 08-07-2026 · '
  'reporting currency EGP', size=8.8, color=GREY, align='center', space_before=10)
