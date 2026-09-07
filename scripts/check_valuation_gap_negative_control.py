#!/usr/bin/env python3
"""Negative control for the valuation-gap gate.  [R-GAP-01]

A CHECK NOBODY HAS SEEN FAIL IS NOT EVIDENCE. This reinjects every condition the gate
claims to catch and fails if any of them is reported clean, plus a clean control that
must PASS — because a control proving only that things go red would also pass if the
gate had become unconditionally red.

The conditions are the ones that actually cost something:

  1. a central fair value far below the traded price with NO review — the AMOC case of
     1-Sep-2026, where six independent modelling defects sat behind a 39% discount and
     every existing gate passed the study
  2. a review that EXISTS but skips a required heading — the rubber stamp, which is the
     way a review requirement normally dies
  3. a study whose committed numbers do not resolve to a central/spot pair — an answer
     nobody can read is not an answer that passed  [R-ENF-04]
  4. an EMPTIED population — zero studies examined must FAIL, never read as zero
     problems found  [R-ENF-04]
  5. a study on the outstanding list that no longer resolves on disk — the gate's own
     glob having silently stopped matching
  6. [AMENDED 02-Sep-2026] a gap on the other side (central far ABOVE spot) MUST now fire:
     the rule is two-sided, and the case that used to prove the one-sidedness is inverted
     here rather than deleted, because the same construction going from green to red is the
     sharpest evidence the extension took effect. What used to read: the rule is
     one-sided by instruction, and a check that fires where no rule exists is the
     permanently-red check [R-ENF-02] forbids

Nothing here touches the real studies: every case runs against a temporary ENGINE
directory built from scratch.
"""
import io
import json
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

import check_valuation_gap as gate  # noqa: E402

REAL_ENGINE, REAL_OUTSTANDING = gate.ENGINE, gate.OUTSTANDING

FULL_REVIEW = '\n'.join('## %s\ncovered.\n' % k for k in gate.REQUIRED_SECTIONS)


def review_auditing(central):
    """A complete review that states the central it audited — what a current
    review looks like once a review has to say which answer it examined."""
    return FULL_REVIEW + '\nAUDITED CENTRAL: %.4f\n' % central


def make_study(engine, tk, central=None, spot=None, review=None, numbers=True):
    d = os.path.join(engine, '%s_study' % tk.lower())
    os.makedirs(d, exist_ok=True)
    if numbers:
        j = {}
        if central is not None:
            j['central'] = central
        if spot is not None:
            j['spot'] = spot
        json.dump(j, io.open(os.path.join(d, 'study_numbers.json'), 'w', encoding='utf-8'))
    if review is not None:
        io.open(os.path.join(d, 'GAP_REVIEW_01-09-2026.md'), 'w',
                encoding='utf-8').write(review)
    return d


def run_case(name, build, outstanding, expect_fail, extra_names=()):
    tmp = tempfile.mkdtemp()
    try:
        build(tmp)
        os.makedirs(os.path.join(tmp, 'build_depth_audit'), exist_ok=True)
        op = os.path.join(tmp, 'build_depth_audit', 'gap_outstanding.json')
        json.dump(outstanding, io.open(op, 'w', encoding='utf-8'))
        gate.ENGINE, gate.OUTSTANDING = tmp, op

        # THE GATE NO LONGER GLOBS FOR ITS POPULATION [re-pointed 06-09-2026], so
        # the sandbox has to supply one. It is built FROM THE SANDBOX'S OWN
        # DIRECTORIES, never hand-written, so a case cannot accidentally test a
        # population that does not match the fixture it planted; `extra_names`
        # adds delivered studies that commit NO record, which is the condition
        # the re-pointing exists to make visible and which no directory can
        # express. study_population.py is negative-controlled separately on its
        # own eight conditions -- each instrument tested on what it decides.
        def _fixture_population(_tmp=tmp, _extra=extra_names):
            out = {}
            for d in sorted(os.listdir(_tmp)):
                if d.endswith('_study') and os.path.isdir(os.path.join(_tmp, d)):
                    out[d[:-len('_study')].upper()] = {
                        'delivered': ['%s_Valuation_Study_01-09-2026_public.pdf'
                                      % d[:-len('_study')].upper()],
                        'record_dir': os.path.join(_tmp, d), 'readable': True}
            for tk in (_extra or ()):
                out[tk] = {'delivered': ['%s_Valuation_Study_01-09-2026_public.pdf' % tk],
                           'record_dir': None, 'readable': False}
            return out
        gate.resolve_population = _fixture_population

        # THE SHARED NO-RECORD RATCHET IS SUBSTITUTED BY POINTING THE RESOLVER AT A
        # FIXTURE FILE, not by re-implementing its logic here: a control that reasons
        # about the ratchet in its own words tests its own reasoning. The cases keep
        # declaring their allowance under the key they always used.
        _nrp = os.path.join(tmp, 'coverage_outstanding.json')
        json.dump({'entries': {t: 'fixture' for t in
                               sorted(outstanding.get('no_record_dir') or [])}},
                  io.open(_nrp, 'w', encoding='utf-8'))
        _sp.NO_RECORD_RATCHET = _nrp

        buf, real = [], sys.stdout

        class Tee:
            def write(self, s):
                buf.append(s)

            def flush(self):
                pass

        sys.stdout = Tee()
        try:
            rc = gate.main([])
        finally:
            sys.stdout = real

        failed = rc != 0
        ok = failed == expect_fail
        print('  %-4s %-62s %s' % ('[ok]' if ok else 'MISS', name,
                                   'went red' if failed else 'reported clean'))
        if not ok:
            print('        ---- what the gate printed ----')
            for line in ''.join(buf).splitlines():
                print('        %s' % line)
        return ok
    finally:
        gate.ENGINE, gate.OUTSTANDING = REAL_ENGINE, REAL_OUTSTANDING
        gate.resolve_population = REAL_POPULATION
        _sp.NO_RECORD_RATCHET = REAL_NO_RECORD
        shutil.rmtree(tmp, ignore_errors=True)


REAL_POPULATION = gate.resolve_population
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                'engine'))
import study_population as _sp                                          # noqa: E402
REAL_NO_RECORD = _sp.NO_RECORD_RATCHET

EMPTY = {'breach_no_review': [], 'unreadable': [], 'exempt': {}}


DECLARED_CASES = 27


def main():
    print('valuation-gap gate — negative control')
    cases = [
        ('central 39% below spot, no gap review',
         lambda e: make_study(e, 'AMOC', 5.53, 9.10), EMPTY, True),
        ('review exists but skips a required heading',
         lambda e: make_study(e, 'AMOC', 5.53, 9.10,
                              review=FULL_REVIEW.replace('## DISCOUNT RATE', '## SOMETHING ELSE')),
         EMPTY, True),
        ('committed numbers carry no central/spot pair',
         lambda e: make_study(e, 'AMOC'), EMPTY, True),
        ('emptied population — zero studies is not zero problems',
         lambda e: None, EMPTY, True),
        ('listed study no longer resolves on disk',
         lambda e: make_study(e, 'AMOC', 9.00, 9.10),
         {'breach_no_review': ['SWDY'], 'unreadable': [], 'exempt': {}}, True),
        ('CLEAN — central 1% below spot, must PASS',
         lambda e: make_study(e, 'AMOC', 9.00, 9.10), EMPTY, False),
        # [R-GAP-01 amended, 02-Sep-2026] the gate is TWO-SIDED. This case tested the
        # one-sidedness and is INVERTED here rather than deleted: the same construction
        # that had to stay green under the old rule must go red under the new one, which
        # is the sharpest possible evidence that the extension actually took effect.
        ('central far ABOVE spot, unreviewed — the two-sided extension',
         lambda e: make_study(e, 'AMOC', 18.00, 9.10), EMPTY, True),
        ('central 13% above spot, unreviewed — the DU case the one-sided rule could not see',
         lambda e: make_study(e, 'AMOC', 10.28, 9.10), EMPTY, True),
        ('CLEAN — central above spot WITH a complete review, must PASS',
         lambda e: make_study(e, 'AMOC', 18.00, 9.10, review=review_auditing(18.00)),
         EMPTY, False),
        ('CLEAN — central 8% above spot, inside the band, must PASS',
         lambda e: make_study(e, 'AMOC', 9.83, 9.10), EMPTY, False),
        ('CLEAN — breach WITH a complete review, must PASS',
         lambda e: make_study(e, 'AMOC', 5.53, 9.10, review=review_auditing(5.53)),
         EMPTY, False),
        # A REVIEW AUDITS AN ANSWER, AND THE ANSWER MOVES. EGCH's central went from
        # 3.76 to -1.06 on 02-Sep-2026 while its review, written for 3.76, sat in the
        # directory unchanged and this gate passed the study. These three cases are
        # that incident, seeded.
        ('review audits a central the study no longer publishes — the EGCH case',
         lambda e: make_study(e, 'AMOC', 5.53, 9.10, review=review_auditing(3.76)),
         EMPTY, True),
        ('review complete but states no audited central at all',
         lambda e: make_study(e, 'AMOC', 5.53, 9.10, review=FULL_REVIEW),
         {'breach_no_review': [], 'unreadable': [], 'review_central_unstated': [],
          'exempt': {}}, True),
        ('CLEAN — review audits the central the study publishes, must PASS',
         lambda e: make_study(e, 'AMOC', 5.53, 9.10, review=review_auditing(5.53)),
         EMPTY, False),
        ('CLEAN — review audits it to the last decimal that matters, must PASS',
         lambda e: make_study(e, 'AMOC', 5.53, 9.10, review=review_auditing(5.5301)),
         EMPTY, False),
        # A REVIEW AUDITS A DISAGREEMENT, AND THE DISAGREEMENT MOVES EVEN WHEN THE
        # ANSWER DOES NOT [added 03-Sep-2026, per the principal: "the gate checks a
        # review audits the current answer, not the current gap — that's why all
        # four pass while every one was written for a much smaller disagreement"].
        # PHDC's own case, seeded: its review audited 17.1517, exactly what the
        # study published, so the central test passed it — while the review was
        # written at +12.8% against a strike of 15.20 and the day's price of 14.40
        # made the gap +19.1%.
        ('review audits the right central but a much smaller gap — the PHDC case',
         lambda e: make_study(e, 'PHDC', 17.1517, 14.40,
                              review=review_auditing(17.1517) + '\nAUDITED GAP: +12.8%\n'),
         EMPTY, True),
        ('CLEAN — review states the gap it actually audited, must PASS',
         lambda e: make_study(e, 'PHDC', 17.1517, 14.40,
                              review=review_auditing(17.1517) + '\nAUDITED GAP: +19.1%\n'),
         EMPTY, False),
        ('CLEAN — a gap that moved less than half the trigger, must PASS',
         lambda e: make_study(e, 'PHDC', 17.1517, 14.40,
                              review=review_auditing(17.1517) + '\nAUDITED GAP: +16.0%\n'),
         EMPTY, False),

        # --- the exemption, added 05-Sep-2026 with the clause it enforces --------------
        # gap_outstanding.json carried an `exempt` block from the day the rule was seeded
        # and NOTHING READ IT, so the one exempt name sat in `unreadable` as well, as a
        # defect that could never be cleared. These three cases are what makes the
        # enforcement evidence rather than an assertion.
        ('an exempt study that DOES expose a central — the exemption or the study is wrong',
         lambda e: make_study(e, 'XPT', 1608.37, 1600.00),
         {'breach_no_review': [], 'unreadable': [],
          'exempt': {'XPT': 'metals study - no issuer, no equity fair value of this shape'}},
         True),
        ('an exemption with an empty reason is a name switched off, not excused',
         lambda e: make_study(e, 'XPT', None, None),
         {'breach_no_review': [], 'unreadable': [], 'exempt': {'XPT': '   '}},
         True),
        ('CLEAN — an exempt study exposing no central, with its reason, must PASS',
         lambda e: (make_study(e, 'XPT', None, None),
                    make_study(e, 'AMOC', 9.00, 9.10)),
         {'breach_no_review': [], 'unreadable': [],
          'exempt': {'XPT': 'metals study - no issuer, no equity fair value of this shape'}},
         False),

        # ---- THE POPULATION RE-POINTING [06-09-2026]. Until this date the gate
        # globbed engine/*_study and audited 23 of 90 delivered studies while
        # reporting itself population-anchored. These six cases are the conditions
        # that re-pointing creates, and the two CLEAN ones matter most: a ratchet
        # that cannot stay green is the permanently-red check [R-ENF-02] forbids.
        ('a delivered study committing no record, not on the ratchet',
         lambda e: make_study(e, 'AMOC', 9.00, 9.10), EMPTY, True, ('COMI',)),
        ('CLEAN — the same study, ratcheted on no_record_dir, must PASS',
         lambda e: make_study(e, 'AMOC', 9.00, 9.10),
         {'breach_no_review': [], 'unreadable': [], 'exempt': {},
          'no_record_dir': ['COMI']}, False, ('COMI',)),
        ('a name excused on no_record_dir that DOES commit a record',
         lambda e: make_study(e, 'AMOC', 9.00, 9.10),
         {'breach_no_review': [], 'unreadable': [], 'exempt': {},
          'no_record_dir': ['AMOC']}, True),
        ('a name carrying BOTH allowances — the two are not interchangeable',
         lambda e: make_study(e, 'AMOC', 9.00, 9.10),
         {'breach_no_review': [], 'unreadable': ['COMI'], 'exempt': {},
          'no_record_dir': ['COMI']}, True, ('COMI',)),
        ('a ratcheted name that resolves to no covered name at all',
         lambda e: make_study(e, 'AMOC', 9.00, 9.10),
         {'breach_no_review': [], 'unreadable': [], 'exempt': {},
          'no_record_dir': ['ZZNOTABOOKNAME']}, True),
        ('names present and ZERO answers read — anchored the second way',
         lambda e: None,
         {'breach_no_review': [], 'unreadable': [], 'exempt': {},
          'no_record_dir': ['COMI']}, True, ('COMI',)),
    ]
    results = [run_case(*(c if len(c) == 5 else c + ((),))) for c in cases]
    assert len(results) == DECLARED_CASES, (
        'declared %d cases, ran %d — a control that quietly loses a case reports '
        'clean for the wrong reason.' % (DECLARED_CASES, len(results)))
    print()
    if all(results):
        print('negative control OK — the gate goes red on every injected defect, on both '
              'sides of the price, and stays green on every clean case')
        return 0
    print('NEGATIVE CONTROL FAILED — %d of %d cases came back wrong. A gate that cannot be '
          'shown to fail is not evidence.' % (sum(1 for r in results if not r), len(results)))
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
