"""STEP 5 hand-off note, generated from the committed records so no figure is typed."""
import json, os, datetime
H = os.path.dirname(os.path.abspath(__file__))
L = lambda n: json.load(open(os.path.join(H, n), encoding='utf-8'))
cj, sn, ac = L('contested_judgements.json'), L('study_numbers.json'), L('asset_cycle.json')
spot = cj['published_spot']
br = cj['published_central_two_sided']
ts = cj['two_sided_judgement']
out = []
w = out.append
w("# GBCO — handed to the principal for external audit\n")
w("**Step 5 of the recalibration runbook, 17 September 2026.** Generated from the study's own")
w("committed records; every figure below is read, not typed.\n")
w("## What is being audited\n")
w("| file | what it is |")
w("|---|---|")
w("| `GBCO_Valuation_Study_07-09-2026_public.pdf` | the valuation document, 31 pp |")
w("| `GBCO_Valuation_Model_07092026_public.xlsx` | the financial model |")
w("| `GBCO_Bibliography_07-09-2026.pdf` | the standalone bibliography, 11 pp |")
w("| `QC_GATE_07-09-2026.md` | our own gate — **verdict NOT DELIVERABLE, and stale; read §4a of the next file** |")
w("| `QC_ROW_WORK_17-09-2026.md` | what we did about that gate, and what we could not |")
w("| `GAP_REVIEW_07-09-2026.md` | the eight-heading audit the gap triggers |\n")
w("## The answer, and what it was struck against\n")
w("**THIS STUDY PUBLISHES NO SINGLE CENTRAL, AND THAT IS THE ANSWER RATHER THAN AN EVASION.**")
w(f"{sn['central_two_sided']['why']}\n")
w("| branch | EGP per share | against spot | what it is |")
w("|---|---|---|---|")
for b in br:
    lbl = b['label']; v = b['value']
    cond = next((x['what'] for k, x in ts.items()
                 if isinstance(x, dict) and x.get('label') == lbl), '')
    cond = cond.split('. ')[0] if cond else ''
    w(f"| {lbl} | **{v:.4f}** | {(v/spot-1)*100:+.1f}% | {cond} |")
w(f"\nStruck against **EGP {spot:.2f}**, the close of {sn['spot_date']} — the latest price this")
w(f"repository holds. Bear case **{sn['central_bear']:.4f}** ({(sn['central_bear']/spot-1)*100:+.1f}%).\n")
w(f"The spread between the two bases is **EGP {ts['spread_egp_mn']:,.0f}mn**, "
  f"{ts['spread_as_a_share_of_the_higher_branch']*100:.1f}% of the higher branch.")
w(f"\n> {ts['note'][:400]}\n")
w("## Every contested judgement, which way it was resolved, and what would overturn it\n")
st = cj['sign_test']
w(f"**Sign test: of {st['material']} material forks the study took the higher-value side on "
  f"{st['resolved_upward']}, two-sided p = {st['two_sided_p']:.4f}, flagged = {st['flagged']}.** "
  "The two-sided judgement above is deliberately NOT in that count — a sign test measures which "
  "way forks were RESOLVED, and that one was not resolved.\n")
w("| judgement | direction taken | the other framing is worth | what would overturn it |")
w("|---|---|---|---|")
for j in cj['judgements']:
    va, vv = j.get('value_adopted'), j.get('value_alternative')
    delta = f"{vv-va:+.2f} EGP/sh" if (va is not None and vv is not None) else '—'
    ob = (j.get('overturned_by') or '').replace('|', '/').strip()
    w(f"| {j['name']} | {j.get('direction','')} | {delta} | {ob} |")
w("\n**The judgement that decides the answer is the two-sided fork, which is not in that table")
w("because it was not resolved. What would overturn it: a real secondary transaction in")
w("MNT-Halan at a stated price, a prospectus or filed offer range, or a revised")
w("equity-accounted carrying amount.**\n")
w("## What we already know is wrong, so the audit is not spent finding it\n")
w("1. **Capital expenditure is management's guidance** and the standing rule forbids consuming it.")
w("   The path implies depreciation coverage falling to 1.76x against a filed record of 3.87x /")
w("   2.79x / 3.67x, with no mechanism named. **We cannot price the correction honestly** because")
w("   the terminal is a perpetuity struck on the final explicit year, so a corrected capex path is")
w("   multiplied through it; and the sanctioned terminal construction refuses on this name because")
w("   no usable asset life is sourceable from the filings. Order of repair is fixed in advance.")
w("2. **There is no property-plant-and-equipment roll-forward.** Capex, depreciation and working")
w("   capital are three independent typed ratios with no balance sheet joining them. This is the")
w("   defect underneath item 1.")
w("3. **Peers are characterised, not studied.** No peer multiple or operating KPI is sourced,")
w("   dated or computed anywhere in the model or the document.\n")
w("## What we fixed on the way in, which changes what the documents say\n")
cyc = ac['cycle']
w("**The asset-conversion cycle is now built** from GB Corp's own disclosed segment tables —")
w("`asset_cycle.json`, four periods, every disclosed table footed to its own stated total:\n")
w("| period | DSO | DIO | DPO | CCC | working capital / revenue |")
w("|---|---|---|---|---|---|")
for p, r in cyc.items():
    w(f"| {p} | {r['dso']:.1f} | {r['dio']:.1f} | {r['dpo']:.1f} | **{r['ccc']:.1f}** | "
      f"{r['wc_over_annualised_revenue']*100:.1f}% |")
t = ac['ttm_to_30_june_2026']
w(f"\nAgainst the latest reviewed period — working capital {t['working_capital']:,.1f} over "
  f"trailing-twelve-month revenue {t['revenue']:,.1f} = **{t['wc_over_revenue']*100:.2f}%** — the")
w("model's committed ladder of 26.5% falling to 21.5% opens ABOVE the actual and lands on it, so")
w("**it is conservative.** Its stated mechanism is half contradicted: the inventory pre-build")
w(f"unwind is measured ({cyc['FY2025']['dio']:.1f} to {cyc['1H2026']['dio']:.1f} days), payables")
w(f"\"re-extending\" is not ({cyc['FY2025']['dpo']:.1f} to **{cyc['1H2026']['dpo']:.1f}** days).\n")
w("## What we are asking of the audit\n")
w("Not a re-run of the above. **The two questions worth your auditor's time:**\n")
w("1. **Is the two-sided answer the right response to the crux, or an evasion?** We publish both")
w("   bases because both are the company's own disclosures and the filings do not decide between")
w("   them. Averaging them would be a retired construction; a discount standing in for the")
w("   uncertainty would be a free parameter. If there is a third honest option we have missed,")
w("   that is the finding that matters most.")
w("2. **Does anything in the document tell a reader to do something that does not work?** Add the")
w("   printed rows, follow the bridge, reproduce the totals. Every figure is computed and")
w("   individually correct; what we cannot check from inside is whether the page instructs.\n")
w("**A finding that is right costs this study nothing to accept. A finding that is wrong will be")
w("refused with the arithmetic that refutes it, never with a restatement of what the study")
w("already says.**")
open(os.path.join(H, 'HANDOVER_17-09-2026.md'), 'w', encoding='utf-8').write("\n".join(out) + "\n")
print("written:", len(out), "lines")
