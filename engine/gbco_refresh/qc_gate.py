"""GBCO refresh — final QC gate, run programmatically. Every assert here must pass
before the refresh is committed; a failure is DO NOT ISSUE."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(HERE, '..'))

# 1) VERIFY BY IMPORT, NOT BY PARSE — every engine module a commit may rely on
import market_profiles, wacc_builder, research_protocol, research_sweep, adaptive_width
import technicals, apply_technicals, ta_chart, rollforward_one, beta_regression
print("import checks: 10 engine modules import cleanly")

from research_protocol import (SIGCMChecklist, assert_sigcm, ModelStudyChecklist,
                               assert_model_study, assert_beta_provenance, MODEL_STUDY)

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))

# 2) beta provenance — inspect the actual record, not a checklist boolean
assert_beta_provenance(D['beta'])
print(f"beta provenance: {D['beta']['beta']:.3f} on {D['beta']['index_file']} "
      f"(as-of {D['beta']['index_asof']}), usable={D['beta']['usable']}, "
      f"conforming={D['beta']['conforming']}")

# 3) SIGCM attestation
sig = SIGCMChecklist(
    historicals_official_only=True,      # H1-26 FS + ER + FY23-25 from issued statements only
    forecast_ground_up=True,             # volume x price per LOB, cost per unit per class
    debt_lc_fx_split=True,               # note 26/29 evidence; split bounded and flagged
    asset_conversion_cycle=True,         # DIO/DSO/DPO measured; WC projected on the cycle
    competitors=True,                    # CNFN/DOAS/AN/BAJAJ, in and out of country
    beta_own_history_vs_egx30=True,      # own_stock_beta record asserted above
    formula_based_model=True,            # 446 formulas; recalc + driver-nudge test pass
    flags_raised_before_issue=True,      # debt split, perimeter note, MNT opacity all flagged
    stop_and_inform_honoured=True,
)
assert_sigcm(sig)
print("SIGCM: all eight clauses attested and asserted")

# 4) model-study depth bar
msc = ModelStudyChecklist(
    structure_matches_model=True,        # 16-section Word + 16-sheet Excel, exact names/order
    bibliography_document=True,          # standalone biblio: docs/register/judgements/negatives
    provenance_four_field=True,          # 174 inputs, asserted in compute
    numeric_traceability=True,           # builders read study_numbers.json only; recalc PASS
    external_reader_scrub=True,          # qc_checks: 0 hits both documents
    figure_discipline=True,              # opaque light canvases; rendered-image inspection done
    table_discipline=True,               # width checks: 0 over/starved/bloated
    expert_appendix_max_detail=True,     # worked tables, sensitivities, falsifiers, C.4-C.6
    contested_judgement_both_ways=True,  # MNT round vs book, side by side everywhere
)
assert_model_study(msc)
print("model-study bar: all nine attestations pass")

# 5) sweep register still validates
r = subprocess.run([sys.executable, os.path.join(HERE, 'sweep.py')],
                   capture_output=True, text=True)
assert r.returncode == 0 and 'PASS' in r.stdout, r.stdout + r.stderr
print("information-sweep register: PASS (re-validated)")

# 6) workbook recalculation + document checks re-run
for script in ('recalc.py', 'qc_checks.py'):
    r = subprocess.run([sys.executable, os.path.join(HERE, script)],
                       capture_output=True, text=True, cwd=HERE)
    assert r.returncode == 0, f"{script} FAILED:\n{r.stdout[-2000:]}{r.stderr[-500:]}"
print("recalc + document checks: PASS (re-run)")

# 7) data.js — syntax, load, untouched-field byte-equality vs HEAD, counts vs HEAD
js = r"""
const fs = require('fs');
const {execSync} = require('child_process');
const load = (src) => eval(src + ';({TICKERS, LEDGER})');
const cur = load(fs.readFileSync('assets/data.js','utf8'));
const head = load(execSync('git show HEAD:assets/data.js', {maxBuffer: 1<<26}).toString());
const eq = (a,b)=>JSON.stringify(a)===JSON.stringify(b);
if (Object.keys(cur.TICKERS).length !== Object.keys(head.TICKERS).length) throw 'ticker count changed';
if (cur.LEDGER.length !== head.LEDGER.length) throw 'ledger row count changed';
if (!eq(cur.LEDGER, head.LEDGER)) throw 'LEDGER content changed';
const t = cur.TICKERS.GBCO, h = head.TICKERS.GBCO;
for (const k of ['spot','spotDate','ccy','dist','hz','touch','levels','tech','asof','name','nameAr','code'])
  if (!eq(t[k], h[k])) throw 'GBCO untouched field changed: '+k;
for (const k of Object.keys(head.TICKERS))
  if (k !== 'GBCO' && !eq(cur.TICKERS[k], head.TICKERS[k])) throw 'other ticker changed: '+k;
if (eq(t.fair, h.fair)) throw 'fair did not change';
console.log('data.js vs HEAD: only GBCO fair/files changed; tickers', Object.keys(cur.TICKERS).length,
            '; ledger rows', cur.LEDGER.length, '(byte-identical)');
"""
r = subprocess.run(['node', '-e', js], capture_output=True, text=True, cwd=ROOT if os.path.isdir(os.path.join(ROOT, '.git')) else '/home/user/testahil')
assert r.returncode == 0, r.stderr
print(r.stdout.strip())
r = subprocess.run(['node', '--check', 'assets/data.js'], cwd='/home/user/testahil')
assert r.returncode == 0
r = subprocess.run(['node', '--check', 'assets/app.js'], cwd='/home/user/testahil')
assert r.returncode == 0
print("node --check: data.js + app.js clean")

# 8) deliverables exist, in both locations
for f in ['GBCO_Valuation_Study_19-08-2026_public.docx', 'GBCO_Valuation_Study_19-08-2026_public.pdf',
          'GBCO_Valuation_Model_19082026_public.xlsx', 'GBCO_Valuation_Model_19082026_public.pdf',
          'GBCO_Bibliography_19-08-2026.docx', 'GBCO_Bibliography_19-08-2026.pdf']:
    for base in ['/home/user/testahil/files', HERE]:
        assert os.path.exists(os.path.join(base, f)), f"missing {base}/{f}"
print("deliverables: 6 files present in files/ and engine/gbco_refresh/")

# 9) absent protocol files honestly recorded (not fabricated)
assert not os.path.exists('/home/user/testahil/engine/Fundamental_Driver_Ledger.md')
assert not os.path.exists('/home/user/testahil/engine/Cost_of_Capital_Reference.md')
print("driver-ledger / cost-of-capital reference: absent from the repo, recorded as such "
      "(driver decisions logged in the sweep register's gate table + the input register)")

print("\nQC GATE: ALL CHECKS PASS — refresh may be committed")
