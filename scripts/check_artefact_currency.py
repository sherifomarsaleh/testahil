#!/usr/bin/env python3
"""[R-ENF-06] AN ARTEFACT A BUILDER READS DECLARES THE ANSWER IT WAS BUILT AGAINST.

    python3 scripts/check_artefact_currency.py [--prune]

WHY THIS EXISTS. On 3 September 2026 three studies were re-struck on fresh prices
and three independent outside audits returned the same verdict for the same
reason, in the auditor's own words: **the re-strike reached the valuation and not
the paper.**

Every one of those documents was built from a numbers file that had moved, beside
a SECOND artefact that had not:

  AMOC   case_adversarial.json, base central 5.954 against a published 11.834 --
         and it was READ by three builders and WRITTEN BY NOTHING. No generator
         existed anywhere in the repository. It drove Table 7, Table 18, Figure 4
         and the opening paragraph, which told a reader that surrendering every
         contested judgement reached EGP 7.47, BELOW the published central, which
         is impossible because every charge conceded raises the value.
  ARCC   efg_bridge.json, a weighted central of 54.65 against a market of 59.00,
         printing a FALLING margin path against Appendix A's rising one.
  EGCH   diagnostics.json and contested_judgements.json, a full edition behind --
         spot 13.98, answer -1.06/2.82, the rating-basis glide -- while the
         document published the re-solved figures beside them.

NONE of these was visible to any existing gate, and the reason is exact: every
gate in this repository reads study_numbers.json, and none of these files is in
it. A stale artefact is worse than a typed numeral in a builder, which the
numeric-traceability gate catches, because IT HAS THE SHAPE OF A COMPUTED RECORD.

THE RULE. Any JSON in a study directory that a builder reads and that carries a
valuation figure must declare, in a field named for the purpose, the study central
and spot it was generated against. The gate compares that declaration with what
the study publishes NOW. It is the same instrument as [R-GAP-01]'s AUDITED CENTRAL
marker on a review, applied to generated artefacts, and for the same reason: an
artefact cannot be checked for currency unless it says what it was current WITH.

WHAT IT DELIBERATELY DOES NOT DO. It does not require every figure in an artefact
to equal the study's -- an adversarial case, an alternative construction and a
price-cone anchor all legitimately differ, and a gate that could not tell those
apart would push studies to stop committing them. It requires the artefact to
state its own vintage. A file whose declared vintage matches is current whatever
else it holds; a file that declares nothing cannot be told from a stale one, and
that is the failure this closes.

Ratcheted [R-ENF-02], population-anchored [R-ENF-04].
"""
import glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
OUTSTANDING = os.path.join(ENGINE, 'build_depth_audit', 'artefact_outstanding.json')

# half a per cent, matching [R-GAP-01]'s AUDITED CENTRAL tolerance: an artefact is
# stale when the answer has MOVED, not when it has been re-rounded
TOL = 0.005

# keys that read as a valuation figure. `end` is here because ARCC's efg_bridge.json
# -- one of the three stale artefacts this rule was adopted on -- carries its answer
# under that name and nothing else.
VALUE_KEYS = ('central', 'per_share', 'value_adopted', 'fair', 'end',
              'value_per_share', 'weighted_central')

# the field an artefact declares its vintage in
DECL = ('published_central', 'study_central', 'built_against_central')
DECL_SPOT = ('published_spot', 'study_spot', 'built_against_spot', 'spot_at_build')

# Files that are INPUTS to the study rather than outputs of it, or that carry no
# valuation figure at all. Named individually rather than pattern-matched, because
# a pattern is how a real artefact slips through.
NOT_OUTPUTS = {
    'sweep_register.json', 'peers.json', 'wacc_result.json', 'beta_result.json',
    'step0_result.json', 'panel_export.json', 'fs_parsed.json', 'macro.json',
    'ir_register.json', 'fetch_attempts.json', 'bs_1q2026.json', 'scores.json',
    'forward_ranges.json', 'lessons_draft.json', 'corrections_log.json',
    'sources.json', 'filings.json', 'technicals.json', 'band_record.json',
    'workbook_census.json', 'formula_count.json', 'xlsx_expected.json',
    'xlsx_expected_v5.json', 'driver_test_result.json', 'scrub_result.json',
    'recalc_result.json', 'prose_check_result.json', 'backtest_5y.json',
    'sensitivity_grid.json', 'flat_rate_ladder.json', 'strike_result.json',
    'lenses.json', 'alternatives.json', 'extract_9m_fy2526.json',
}


def carries_valuation(obj, depth=0):
    """Does this artefact hold a figure that would read as a valuation?"""
    if depth > 6:
        return False
    if isinstance(obj, dict):
        # A FILE THAT DECLARES ITS VINTAGE IS ALWAYS CHECKED, whatever else it holds.
        # Without this the gate could only find artefacts whose value key it already
        # knew, and one of the three that motivated it -- ARCC's efg_bridge.json,
        # which carries its figure under `end` -- was invisible to the first draft.
        # A GATE THAT DOES NOT CATCH ITS OWN MOTIVATING CASE IS NOT EVIDENCE.
        if any(k in obj for k in DECL) or any(k in obj for k in DECL_SPOT):
            return True
        for k, v in obj.items():
            if k in VALUE_KEYS and isinstance(v, (int, float)) and not isinstance(v, bool):
                return True
            if carries_valuation(v, depth + 1):
                return True
    elif isinstance(obj, list):
        return any(carries_valuation(v, depth + 1) for v in obj[:20])
    return False


def declared(obj, keys):
    if not isinstance(obj, dict):
        return None
    for k in keys:
        v = obj.get(k)
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            return float(v)
    return None


def main(argv):
    prune = '--prune' in argv
    d = json.load(open(OUTSTANDING, encoding='utf-8'))
    known = set(d.get('outstanding', []))

    dirs = sorted(glob.glob(os.path.join(ENGINE, '*_study')))
    if not dirs:
        print('FAIL - examined zero studies. An empty result is not a clean result.')
        return 1
    on_disk = {os.path.basename(p)[:-6].upper() for p in dirs}
    ghosts = sorted(known - on_disk)
    if ghosts:
        print('FAIL - the outstanding list names studies that are not on disk: %s'
              % ', '.join(ghosts))
        return 1

    checked = stale = undeclared = 0
    bad, ok_rows, conform = [], [], []
    for sdir in dirs:
        tk = os.path.basename(sdir)[:-6].upper()
        sn = os.path.join(sdir, 'study_numbers.json')
        if not os.path.exists(sn):
            continue
        try:
            doc = json.load(open(sn, encoding='utf-8'))
        except Exception:
            continue
        central, spot = doc.get('central'), doc.get('spot')
        if not isinstance(central, (int, float)):
            continue                       # a two-sided study; handled by its branches
        clean_here = True
        for f in sorted(glob.glob(os.path.join(sdir, '*.json'))):
            base = os.path.basename(f)
            if base == 'study_numbers.json' or base in NOT_OUTPUTS:
                continue
            try:
                j = json.load(open(f, encoding='utf-8'))
            except Exception:
                continue
            if not carries_valuation(j):
                continue
            checked += 1
            dc = declared(j, DECL)
            if dc is None:
                undeclared += 1
                clean_here = False
                bad.append((tk, base, 'declares no central it was built against. An '
                                      'artefact that does not say what it was current '
                                      'WITH cannot be told from a stale one.'))
                continue
            if abs(dc - central) > max(TOL * abs(central), 0.005):
                stale += 1
                clean_here = False
                bad.append((tk, base, 'was built against a central of %.4f and the study '
                                      'now publishes %.4f' % (dc, central)))
                continue
            ds = declared(j, DECL_SPOT)
            if ds is not None and spot and abs(ds - spot) > max(TOL * abs(spot), 0.005):
                stale += 1
                clean_here = False
                bad.append((tk, base, 'was built against a spot of %.4f and the study is '
                                      'struck at %.4f' % (ds, spot)))
                continue
            ok_rows.append((tk, base, dc))
        if clean_here:
            conform.append(tk)

    print('[R-ENF-06] artefact currency: what a builder reads, against what the study '
          'publishes\n')
    print('  examined %d study directories, %d artefacts carrying a valuation figure\n'
          % (len(dirs), checked))
    if ok_rows:
        print('  CURRENT (%d):' % len(ok_rows))
        for tk, base, dc in ok_rows:
            print('   %-10s %-32s built against %.4f' % (tk, base, dc))
        print()
    newbad = [(t, b, w) for t, b, w in bad if t not in known]
    if bad:
        print('  NOT CURRENT OR NOT DECLARED (%d stale, %d undeclared):' % (stale, undeclared))
        for tk, base, why in bad:
            print('   %-10s %-32s %s%s' % (tk, base, why,
                                           '' if tk not in known else '   [outstanding]'))
        print()
    if newbad:
        print('FAIL - %d new violation(s).' % len(newbad))
        print('\nThree outside audits on 3 September 2026 reached the same verdict for the '
              'same reason: the re-strike reached the valuation and not the paper. A second '
              'artefact that no gate reads is where that hides.')
        return 1
    if prune:
        keep = sorted(known - set(conform))
        d['outstanding'] = keep
        json.dump(d, open(OUTSTANDING, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
        print('pruned - now %d entries' % len(keep))
    print('OK - no new violations.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
