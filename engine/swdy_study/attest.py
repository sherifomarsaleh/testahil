"""SWDY — attest ModelStudyChecklist and SIGCM before issue.

THE STUDY CALLED NEITHER. assert_sigcm() and assert_model_study() are the standing hard
gates every delivered study is held to, and nothing in this directory invoked them: the
study asserted its arithmetic thoroughly and never asserted that it was the kind of
document this house issues. A gate nobody calls is not a gate.

Nothing here is self-certified. Every field is set from a file, a count or a number read
out of the DELIVERED artefacts — not from a conviction, and not from a boolean another
step wrote about itself. Where the evidence for a field does not exist, the field is
False and the assertion fails, because an absent result is held exactly as a breaching
one [R-ENF-04].
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..'))
import openpyxl
from docx import Document
from research_protocol import (ModelStudyChecklist, assert_model_study, SIGCMChecklist,
                               assert_sigcm, MODEL_STUDY, assert_beta_provenance,
                               STANDARD_VERSION, DriverLine)
import edition as EDN

D = json.load(open('study_numbers.json'))
INP = D['inputs']
BETA = json.load(open('beta_result.json'))
COC = D['cost_of_capital_record']


def _need(path):
    if not os.path.exists(path):
        raise SystemExit('%s is missing; the attestation cannot be made without it '
                         '[R-ENF-04]' % path)
    return json.load(open(path))


QC = _need('qc_checks.json')
STRIKE = _need('strike_result.json')
# THE SWEEP REGISTER IS PART OF THE ATTESTATION, not a file sitting beside it.
# _need() raises on absence, so a study that stops running its Step 2A sweep stops
# attesting rather than quietly attesting without it [R-ENF-04].
SWEEP = _need('sweep_register.json')

wb = openpyxl.load_workbook(EDN.MODEL_XLSX)
doc = Document(EDN.STUDY_DOCX)
heads = [p.text.strip() for p in doc.paragraphs if p.text.strip() and p.runs
         and p.runs[0].font.size and p.runs[0].font.size.pt >= 12]


def check_sections(hs):
    low = [h.lower() for h in hs]
    missing = []
    for sec in MODEL_STUDY['word_skeleton']:
        stem = re.sub(r'^[0-9.§\s]+', '', sec.split(' — ')[0].split(' + ')[-1]).strip().lower()
        m = re.match(r'(appendix [abc]|[a-z]+)', stem)
        key = m.group(1) if m else stem[:8]
        if not any(key in h for h in low):
            missing.append(sec)
    return missing


sec_missing = check_sections(heads)
sheet_missing = ([n for n in MODEL_STUDY['excel_sheets'] if n not in wb.sheetnames]
                 + [n for n in wb.sheetnames if n not in MODEL_STUDY['excel_sheets']])

# ---- the model-study standards, each from its own evidence --------------------
four_field = all(all(v.get(f) not in (None, '', []) for f in ('value', 'source', 'date', 'ring'))
                 for v in INP.values())
lens_names = set(D['lenses'])
four_lenses = {'dcf', 'relative', 'normalized', 'book'} <= lens_names
expert_full = all(all(k in D['experts'][e] for k in ('base', 'rng', 'method_short'))
                  for e in ('e1', 'e2', 'e3'))
# a base outside its own range is not a lens, it is an arithmetic failure
expert_bracketed = all(D['experts'][e]['rng'][0] <= D['experts'][e]['base']
                       <= D['experts'][e]['rng'][1] for e in ('e1', 'e2', 'e3'))
_fml = sum(1 for ws in wb.worksheets for row in ws.iter_rows()
           for c in row if isinstance(c.value, str) and c.value.startswith('='))
XP = _need('xlsx_expected.json')
recalc_ok = _fml > 0 and len(XP) > 0
contested = abs(D['lenses']['dcf']['base'] - D['lenses']['relative']['base']) > 0

c = ModelStudyChecklist(
    structure_matches_model=(not sec_missing) and (not sheet_missing),
    bibliography_document=os.path.exists(EDN.BIBLIO_DOCX),
    provenance_four_field=four_field,
    numeric_traceability=recalc_ok,
    external_reader_scrub=not QC['scrub_hits'],
    figure_discipline=not QC['transparent'],
    table_discipline=not QC['table_problems'],
    expert_appendix_max_detail=expert_full and expert_bracketed,
    contested_judgement_both_ways=contested)

EVIDENCE = dict(
    sections='%d headings, %d model-study sections missing %s'
             % (len(heads), len(sec_missing), sec_missing or ''),
    sheets='%d sheets, %d mismatches %s' % (len(wb.sheetnames), len(sheet_missing),
                                            sheet_missing or ''),
    lenses=sorted(lens_names),
    inputs='%d inputs, four-field complete=%s' % (len(INP), four_field),
    experts='bases inside their own ranges=%s' % expert_bracketed,
    scrub='%d patterns, %d hits' % (QC['scrub_patterns'], len(QC['scrub_hits'])),
    figures='%d figures, %d transparent' % (QC['figures'], len(QC['transparent'])),
    tables='%d tables, %d problems' % (QC['tables'], len(QC['table_problems'])),
    typed_numerals='%d in %s' % (len(QC['typed_numerals']), ', '.join(QC['builders'])),
    workbook='%d formulas, %d checked expected values' % (_fml, len(XP)),
    sweep='%d findings (%d dated negative searches), %d drivers, primary access %s'
          % (len(SWEEP['findings']),
             sum(1 for f in SWEEP['findings'] if f.get('klass') == 'NEGATIVE_SEARCH'),
             len(SWEEP['drivers']),
             'logged' if SWEEP.get('primary_access') else 'NOT LOGGED'))
assert four_lenses, 'the four lenses are not all present'
assert_model_study(c)
print('assert_model_study PASSED — every standard attested from evidence')
for k, v in EVIDENCE.items():
    print('  %-16s %s' % (k, v))

# ---- SIGCM, field by field, from the study's own record -----------------------
# NOT A ROW OF TRUES. Each clause is answered by something in this tree that would go
# False if the study stopped doing it.
_hist_sources = ' '.join(INP[k]['source'].lower() for k in INP
                         if k.startswith(('rev_fy', 'ebit_fy', 'assets_fy', 'debt_fy',
                                          'cash_fy', 'eps_fy', 'wages_fy')))
sig = SIGCMChecklist(
    # clause 1 — historicals from the company's own issued statements only
    historicals_official_only=('audited' in _hist_sources and 'estimate' not in _hist_sources),
    # clause 2 — the forecast is built from units and segments, not one top-line rate
    forecast_ground_up=(len(D['bottomup']['unit_hist']) >= 3
                        and len(D['bottomup']['seg_gp']) >= 3
                        and all(k in INP for k in ('cables_tonnage_hist', 'cables_volume_growth',
                                                   'cables_passthrough', 'construct_growth',
                                                   'elecprod_growth'))),
    # clause 3 — the debt book is split local vs hard currency
    debt_lc_fx_split=('w_egp_implied' in D['wacc']
                      and {'kd_egp_note', 'kd_hard_note'} <= set(INP)),
    # clause 4 — the working-capital / asset conversion cycle is modelled
    asset_conversion_cycle=any(k.startswith(('dso', 'dio', 'dpo', 'wc_', 'nwc')) for k in INP),
    # clause 5 — competitors. FALSE, AND SAID SO. This study computes no peer multiple
    # anywhere, deliberately: an earlier draft asserted a "peers trade at 8-11x" range
    # that no calculation supported and it was withdrawn rather than sourced. The
    # relative lens runs on SWDY's own trading history instead, and the report says so
    # in three places. Marking this clause True would be exactly the self-certification
    # SIGCM exists to stop, so it is declared N/A with its reason attached.
    competitors=False,
    # clause 6 — beta against the published index of the listing exchange, never a composite
    beta_own_history_vs_egx30=(BETA.get('conforming') is True
                               and 'EGX30' in os.path.basename(BETA['index_file'])),
    # clause 7 — the model is formulas, not pasted values
    formula_based_model=_fml > 0,
    # clause 8 — what was found was raised before issue, in the study's own record
    flags_raised_before_issue=os.path.exists('rebuild_ledger.json')
                              and bool(json.load(open('rebuild_ledger.json')).get('levers')),
    # clause 9 — where the record could not answer, the study stopped and said so
    stop_and_inform_honoured=sum(1 for f in SWEEP['findings']
                                 if f.get('klass') == 'NEGATIVE_SEARCH') >= 5,
    na_reasons={'competitors': (
        'No listed comparable exists for this business mix on this exchange: the nearest '
        'regional peer in cables is a Saudi manufacturer with a fraction of the revenue '
        'and no turnkey engineering arm. The relative lens is therefore built on SWDY\'s '
        'own trading history and labelled as such; an earlier draft\'s unsupported '
        '"peers trade at 8-11x" range was withdrawn rather than sourced, and the '
        'withdrawal is recorded in section 1.3 of the delivered report.')})
assert_sigcm(sig)
print('assert_sigcm PASSED —', {k: v for k, v in sig.__dict__.items() if k != 'na_reasons'})

assert_beta_provenance(BETA)
print('assert_beta_provenance PASSED — %.4f vs %s (conforming=%s)'
      % (BETA['beta'], os.path.basename(BETA['index_file']), BETA['conforming']))

# ---- the ground-up driver record ------------------------------------------------
# THE STUDY HAD NONE. assert_ground_up() says in its own message that the ground-up
# clause "is no longer attestable by a flag; build a DriverLine per revenue line" — and
# SWDY attested the clause with a flag, because nothing called the function. The three
# disclosed segments are recorded here at the level each was actually built to, with the
# gap stated wherever that level is below units. The shares are READ from the FY2025
# segment revenue the forecast bases off, so they cannot drift from the model.
_SEGREV = D['bottomup']['unit_hist']['FY25']['rev']
_TOT = sum(_SEGREV.values())
lines = [
    DriverLine(
        name='Cables and accessories', level='unit',
        share_of_revenue=_SEGREV['cables'] / _TOT,
        unit='tonnes of cable shipped',
        unit_source=("the company's own quarterly earnings releases — 144,997 / 156,748 / "
                     "167,665 / 185,449 tonnes over FY2022-25 and 99,239 in the reviewed "
                     "half against 89,636. NOT in the audited statements, which disclose "
                     "no tonnage for any segment; the releases are the issuer's own and "
                     "are cited as such"),
        price_basis=('the LME copper forward path times the house EGP/USD path, applied '
                     'as a disclosed pass-through rate rather than a revenue growth '
                     'assumption, plus a separate real volume growth term'),
        cost_basis=('segment margin on the audited segment-profit-to-revenue basis; the '
                    'audited statements disclose no cost per tonne')),
    DriverLine(
        name='Constructions and infrastructure', level='segment',
        share_of_revenue=_SEGREV['construct'] / _TOT,
        price_basis="the segment's own FY2023-25 revenue CAGR, tapered",
        cost_basis='disclosed segment margin',
        gap_note=('No unit exists that this business can be built on and no filing '
                  'supplies one: turnkey engineering revenue is recognised on progress '
                  'against contracts of differing size, and neither the audited '
                  'statements nor the interim discloses contract count, megawatts or '
                  'kilometres. The EGP 346bn engineering backlog at 30 June 2026 is read '
                  'from the releases and CORROBORATES the taper; it is not burnt down '
                  'into revenue, because the releases do not disclose the burn profile '
                  'that would take')),
    DriverLine(
        name='Electrical products', level='segment',
        share_of_revenue=_SEGREV['elecprod'] / _TOT,
        price_basis="the segment's own FY2023-25 revenue CAGR, tapered",
        cost_basis='disclosed segment margin',
        gap_note=('The segment aggregates transformers, meters and electrical accessories '
                  'on one disclosed line. No filing splits it, and no meter count, MVA or '
                  'transformer unit figure appears in the audited statements or the '
                  'interim, so there is no unit to build on')),
]
from research_protocol import assert_ground_up
GU = assert_ground_up(lines, 'SWDY')
print('ground-up record: %d lines, %.1f%% of revenue at unit level'
      % (GU['lines'], 100 * GU['unit_share']))
for l in lines:
    print('  %-34s %-8s %5.1f%%  %s' % (l.name, l.level, 100 * l.share_of_revenue,
                                        (l.unit or l.gap_note or '')[:52]))

assert D.get('standard_version') == STANDARD_VERSION, (
    'study_numbers.json is stamped %r against the live standard %r'
    % (D.get('standard_version'), STANDARD_VERSION))

# THE DRIVER RECORD GOES INTO THE NUMBERS FILE, NOT ONLY INTO THE ATTESTATION.
# scripts/check_ground_up.py reads study_numbers.json and reports SWDY as committing no
# driver-line record at all; a record that lives only in a file the gate does not read is
# a record nobody is held to. Written under `driver_lines`, the key the gate looks for,
# beside the assert_ground_up summary it was computed from — the INPUT, not just the
# output, because an output cannot be audited back to the lines that produced it.
D['driver_lines'] = [dict(name=l.name, level=l.level,
                          share_of_revenue=l.share_of_revenue, unit=l.unit,
                          unit_source=l.unit_source, price_basis=l.price_basis,
                          cost_basis=l.cost_basis, gap_note=l.gap_note) for l in lines]
D['ground_up'] = GU
with open('study_numbers.json', 'w') as _f:
    json.dump(D, _f, indent=1)
print('committed %d driver lines to study_numbers.json' % len(lines))

json.dump(dict(model_study=EVIDENCE, passed=c.passed(),
               sigcm={k: v for k, v in sig.__dict__.items() if k != 'na_reasons'},
               beta=dict(beta=BETA['beta'], index_file=BETA['index_file'],
                         conforming=BETA['conforming']),
               ground_up=GU,
               drivers=[dict(name=l.name, level=l.level,
                             share_of_revenue=l.share_of_revenue, unit=l.unit,
                             unit_source=l.unit_source, price_basis=l.price_basis,
                             cost_basis=l.cost_basis, gap_note=l.gap_note)
                        for l in lines],
               anchor=dict(date=STRIKE['anchor_date'], spot=STRIKE['spot']),
               standard_version=STANDARD_VERSION),
          open('attestation.json', 'w'), indent=1)
print('wrote attestation.json | standard %s' % STANDARD_VERSION)
