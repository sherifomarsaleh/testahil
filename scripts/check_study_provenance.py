#!/usr/bin/env python3
"""Repo-level provenance gate — the check a study cannot skip by not calling it.

WHY THIS EXISTS
    engine/research_protocol.py already holds assert_beta_provenance(), assert_sigcm()
    and assert_model_study(), and they work. But each study decides whether to CALL
    them, and most do not: a study passes by not checking itself. That is the exact
    shape of the failure being corrected — every study in the repo regressed against a
    composite of the covered names WHILE THE RULE AGAINST IT WAS ALREADY WRITTEN DOWN,
    because writing a rule down does not execute it.

    This script runs from OUTSIDE the studies, over all of them, in CI. A study cannot
    opt out of it, and adding a new study directory with no gate is itself a failure.

WHAT IT CHECKS, per study directory under engine/*_study/
    1. a beta artefact exists at all
    2. the artefact records a regressor FILE, not just a name in prose  [R-BETA-04]
    3. that file resolves to an index registered in wacc_builder.EXCHANGE_INDEX  [R-IDX-01]
       (a byte-identical copy under an unregistered filename FAILS — the number may be
       right but assert_beta_provenance() cannot attest it)
    4. the study calls at least one of the three gates in its own code  [R-ENF-02]
    5. no study-local beta script survives  [R-ENF-02] — hand-rolling one is what the standing rule
       forbids, and it is how the composite spread

THE RATCHET
    83 studies are knowingly outstanding, tracked in the rebuild queue. Failing the
    build for all of them on day one produces a permanently red check that everyone
    learns to ignore, which is worse than no check. So a study named in
    OUTSTANDING is allowed to fail, and the gate fails only on:
      - a study NOT on the list that violates            -> regression, hard fail
      - a study directory with no entry either way       -> new work, hard fail
    A study on the list that now PASSES is reported so the list can shrink. The list is
    only ever allowed to get shorter; scripts/check_study_provenance.py --prune rewrites
    it, and a shorter list is the measure of progress through the queue.

USAGE
    python3 scripts/check_study_provenance.py          # gate; exit 1 on any hard fail
    python3 scripts/check_study_provenance.py --prune  # drop the now-passing entries
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
OUTSTANDING_FILE = os.path.join(ENGINE, 'build_depth_audit', 'outstanding.json')
sys.path.insert(0, ENGINE)

GATE_CALLS = ('assert_beta_provenance', 'assert_sigcm', 'assert_model_study')
BETA_FILES = ('beta_sanctioned.json', 'beta_result.json', 'beta_official.json')
# A study-local regression script. beta_record.py / beta_run.py are the SANCTIONED
# shape - they call beta_regression.own_stock_beta() and record the result - so they
# are only a violation if they do their own regression instead.
LOCAL_BETA_HINT = re.compile(r'\bnp\.linalg\.lstsq|polyfit|\bcov\(|composite', re.I)


def registered_stems():
    from wacc_builder import EXCHANGE_INDEX
    return set(EXCHANGE_INDEX.values())


def read_beta(sdir):
    for f in BETA_FILES:
        p = os.path.join(sdir, f)
        if os.path.exists(p):
            try:
                return f, json.load(open(p, encoding='utf-8'))
            except Exception:
                return f, None
    return None, None


def audit(sdir, stems):
    """Return (ok, [reasons]) for one study directory."""
    bad = []
    fname, rec = read_beta(sdir)
    if rec is None:
        bad.append('no readable beta artefact' if fname is None
                   else f'{fname} is not valid JSON')
    else:
        path = str(rec.get('index_file') or rec.get('regressor_file') or '')
        named = str(rec.get('regressor') or rec.get('index') or rec.get('index_name') or '')
        if not path:
            bad.append(f'{fname} records no regressor FILE'
                       + (f' (only the name {named!r})' if named else ''))
        else:
            stem = os.path.basename(path)[:-4] if path.endswith('.csv') else os.path.basename(path)
            if 'raw_indices' not in path.replace('\\', '/'):
                bad.append(f'regressor {path!r} is not under raw_indices/')
            elif stem not in stems:
                bad.append(f'regressor {stem!r} is not registered in EXCHANGE_INDEX '
                           f'(registered: {", ".join(sorted(stems))})')

    pys = [f for f in os.listdir(sdir) if f.endswith('.py')]
    src = {}
    for f in pys:
        try:
            src[f] = open(os.path.join(sdir, f), encoding='utf-8', errors='ignore').read()
        except Exception:
            src[f] = ''
    if not any(any(g in t for g in GATE_CALLS) for t in src.values()):
        bad.append('no code in the study calls any of '
                   + ', '.join(g + '()' for g in GATE_CALLS))
    for f, t in src.items():
        if f.startswith('beta_') and 'own_stock_beta' not in t and LOCAL_BETA_HINT.search(t):
            bad.append(f'{f} looks like a study-local regression '
                       '(does not call beta_regression.own_stock_beta)')
    return (not bad), bad


def check_index_registry():
    """Every .csv under raw_indices/ is registered, or documented as deliberately held.

    [R-IDX-01, 23-Aug-2026] ADXGENERAL.csv sat beside FADGI.csv, byte-identical, under a
    filename the resolver does not register. Two studies regressed against it: the right
    number with provenance that cannot resolve. Nothing objected, because no rule said a
    file in this directory must be either registered or gone.
    """
    from wacc_builder import EXCHANGE_INDEX
    root = os.path.join(ENGINE, 'raw_indices')
    registered = set(EXCHANGE_INDEX.values())
    held = json.load(open(OUTSTANDING_FILE, encoding='utf-8')).get('held_unregistered', {})
    bad = []
    for mkt in sorted(os.listdir(root)):
        d = os.path.join(root, mkt)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if not f.endswith('.csv'):
                continue
            stem = f[:-4]
            if stem in registered or stem in held:
                continue
            bad.append(f'{mkt}/{f} is neither registered in EXCHANGE_INDEX nor listed as '
                       f'deliberately held')
    return bad


def check_standard_version():
    """Report the standard each study was built to.  [R-STD-01, 23-Aug-2026]"""
    from research_protocol import STANDARD_VERSION
    stamped, unstamped = {}, []
    for d in sorted(os.listdir(ENGINE)):
        if not d.endswith('_study'):
            continue
        v = None
        for f in os.listdir(os.path.join(ENGINE, d)):
            if f.endswith('.json'):
                try:
                    j = json.load(open(os.path.join(ENGINE, d, f), encoding='utf-8'))
                except Exception:
                    continue
                if isinstance(j, dict) and 'standard_version' in j:
                    v = j['standard_version']
                    break
        (stamped.setdefault(v, []).append(d[:-6].upper()) if v
         else unstamped.append(d[:-6].upper()))
    return STANDARD_VERSION, stamped, unstamped


def main():
    prune = '--prune' in sys.argv
    stems = registered_stems()
    outstanding = json.load(open(OUTSTANDING_FILE, encoding='utf-8'))
    known = set(outstanding['outstanding'])

    dirs = sorted(d for d in os.listdir(ENGINE)
                  if d.endswith('_study') and os.path.isdir(os.path.join(ENGINE, d)))
    hard, fixed, still, unknown = [], [], [], []

    for d in dirs:
        tk = d[:-6].upper()
        ok, why = audit(os.path.join(ENGINE, d), stems)
        listed = tk in known or tk in outstanding.get('aliases', {})
        if ok and listed:
            fixed.append(tk)
        elif ok:
            pass
        elif listed:
            still.append((tk, why))
        elif tk in outstanding.get('exempt', {}):
            pass
        else:
            (hard if tk in {x[:-6].upper() for x in dirs} else unknown).append((tk, why))

    idx_bad = check_index_registry()
    cur, stamped, unstamped = check_standard_version()

    print(f'study directories: {len(dirs)}   registered indices: {len(stems)}')
    print(f'current study standard: {cur}   stamped: {sum(len(v) for v in stamped.values())}'
          f'   unstamped: {len(unstamped)}')
    print(f'known outstanding: {len(known)}   exempt: {len(outstanding.get("exempt", {}))}')
    print()
    if fixed:
        print(f'NOW PASSING — remove from the outstanding list ({len(fixed)}):')
        for tk in fixed:
            print(f'   {tk}')
        print()
    if still:
        print(f'still outstanding, allowed for now ({len(still)}):')
        for tk, why in still:
            print(f'   {tk}: {why[0]}')
        print()
    if hard:
        print(f'FAIL — not on the outstanding list and not conforming ({len(hard)}):')
        for tk, why in hard:
            for w in why:
                print(f'   {tk}: {w}')
        print()

    if prune and fixed:
        outstanding['outstanding'] = sorted(known - set(fixed))
        json.dump(outstanding, open(OUTSTANDING_FILE, 'w', encoding='utf-8'), indent=1)
        print(f'pruned {len(fixed)} now-passing entries; '
              f'{len(outstanding["outstanding"])} remain')
        return 0

    if idx_bad:
        print(f'FAIL — index registry ({len(idx_bad)}):')
        for b in idx_bad:
            print(f'   {b}')
        print()

    if hard or idx_bad:
        print('The gate fails. Either fix the study or, if this is knowingly deferred '
              'work, add it to engine/build_depth_audit/outstanding.json WITH A REASON.')
        return 1
    print('OK — no new violations.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
