#!/usr/bin/env python3
"""Negative control for [R-ENF-01]'s waterfall gate and the instrument beneath it.

A CHECK NOBODY HAS SEEN FAIL IS NOT EVIDENCE. Every condition below is reinjected into a
sandbox copy of the repository and the gate must go RED and must NAME the study; every
clean case must stay GREEN. EVERY MUTATION IS ASSERTED TO HAVE LANDED before the gate runs
— a fixture that silently fails to inject its own condition produces a green run that
proves only that the file was untouched, which is the [R-ENF-04] species and is exactly
how this repository's earlier controls have failed.

The instrument's own conditions are exercised directly, because waterfall() is what
actually refuses at build time and the gate only requires that it be called.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
import table_residual as TR                                            # noqa: E402

GATE = 'scripts/check_waterfall_assertions.py'


# --------------------------------------------------------------------------
# PART ONE — the instrument itself
# --------------------------------------------------------------------------
def instrument_cases():
    """(name, callable, must_raise) — waterfall()'s own refusals and acceptances."""
    def bridge_as_shipped():
        # SCEM's enterprise-to-equity bridge exactly as it was delivered: the minority was
        # deducted in the model and no line was printed for it.
        return TR.waterfall(6616.62, [('Plus net cash', 4929.74)], 11426.36, dp=0,
                            what='bridge as shipped')

    def bridge_corrected():
        return TR.waterfall(6616.62, [('Plus net cash', 4929.74),
                                      ('Less non-controlling interests', 120.0)],
                            11426.36, dp=0, what='bridge corrected')

    def deduction_in_parentheses():
        # "(120)" and "120" under a row saying Less are the same instruction
        return TR.waterfall(6616.62, [('Plus net cash', 4929.74),
                                      ('Less non-controlling interests', -120.0)],
                            11426.36, dp=0, what='bridge, parenthesised deduction')

    def waterfall_as_shipped():
        # the printed cash-flow waterfall: depreciation added back, capital expenditure and
        # working capital deducted, against a model that runs NOPAT less reinvestment
        return TR.waterfall(1915.16, [('Plus depreciation & amortisation', 445.0),
                                      ('Less capital expenditure', 400.0),
                                      ('Less change in working capital', 131.0)],
                            798.62, dp=0, what='waterfall as shipped')

    def step_with_no_operation():
        return TR.waterfall(100.0, [('Depreciation & amortisation', 10.0)], 90.0, dp=0,
                            what='a step that instructs nothing')

    def undeclared_extra():
        return TR.waterfall(1.0, [('Plus one', 1.0)], 5.0, dp=0, extra=3.0,
                            what='an exception with no reason')

    def declared_extra():
        return TR.waterfall(1.0, [('Plus one', 1.0)], 5.0, dp=0, extra=3.0,
                            why='a real, stated reason')

    def rounding_inside_the_band():
        # every row printed to the unit, so the band is (n+2)*0.5 and a half-unit is fine
        return TR.waterfall(6616.0, [('Plus net cash', 4930.0)], 11546.4, dp=0,
                            what='inside the printed rounding')

    def rounding_outside_the_band():
        return TR.waterfall(6616.0, [('Plus net cash', 4930.0)], 11550.0, dp=0,
                            what='outside the printed rounding')

    def per_share_division():
        return TR.waterfall(15154.0, [('Divided by shares in issue', 260.812477)],
                            58.10, dp=2, what='per share')

    return [
        ('1  the bridge exactly as it shipped, minority deducted and unprinted',
         bridge_as_shipped, True),
        ('2  the same bridge with the line printed', bridge_corrected, False),
        ('3  the deduction printed in parentheses is the same instruction',
         deduction_in_parentheses, False),
        ('4  the cash-flow waterfall exactly as it shipped', waterfall_as_shipped, True),
        ('5  a step whose label instructs nothing', step_with_no_operation, True),
        ('6  an undeclared figure the table does not print', undeclared_extra, True),
        ('7  the same figure declared with its reason', declared_extra, False),
        ('8  a half-unit of printed rounding must NOT fire', rounding_inside_the_band,
         False),
        ('9  four units against a band of one and a half must fire',
         rounding_outside_the_band, True),
        ('10 a per-share division reproduces', per_share_division, False),
    ]


# --------------------------------------------------------------------------
# PART TWO — the gate, in a sandbox
# --------------------------------------------------------------------------
def run(cwd):
    p = subprocess.run([sys.executable, GATE], cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def sandbox():
    d = tempfile.mkdtemp(prefix='wf-nc-')
    dst = os.path.join(d, 'repo')
    os.makedirs(dst)
    for item in ('scripts', 'engine'):
        shutil.copytree(os.path.join(ROOT, item), os.path.join(dst, item),
                        ignore=shutil.ignore_patterns('*.pdf', '*.png', '*.xlsx',
                                                      '__pycache__', 'raw_ohlc',
                                                      'raw_indices', 'lab'))
    return d, dst


def gate_cases():
    """(name, mutate(dst) -> assertion that it landed, expect_red, must_name)."""
    def drop_scem_call(dst):
        p = os.path.join(dst, 'engine', 'scem_study', 'docx_scem.py')
        s = open(p, encoding='utf-8').read()
        assert 'waterfall(' in s, 'fixture never injected: SCEM did not call waterfall()'
        s = s.replace('waterfall(', 'no_such_helper_(')
        s = s.replace('from table_residual import no_such_helper_',
                      'from table_residual import waterfall')
        open(p, 'w', encoding='utf-8').write(s)
        assert 'import table_residual' in s
        return 'SCEM'

    def import_but_never_call(dst):
        p = os.path.join(dst, 'engine', 'scem_study', 'docx_scem.py')
        s = open(p, encoding='utf-8').read()
        assert 'waterfall(' in s
        s = s.replace('waterfall(', 'unused_(')
        open(p, 'w', encoding='utf-8').write(s)
        assert 'import table_residual' in s and 'waterfall(' not in s
        return 'SCEM'

    def ratchet_names_a_ghost(dst):
        p = os.path.join(dst, 'engine', 'build_depth_audit', 'waterfall_outstanding.json')
        d = json.load(open(p))
        d['outstanding'].append('NOSUCHCO')
        json.dump(d, open(p, 'w'), indent=1)
        assert 'NOSUCHCO' in json.load(open(p))['outstanding']
        return 'NOSUCHCO'

    def empty_population(dst):
        n = 0
        for root, _, files in os.walk(os.path.join(dst, 'engine')):
            for f in files:
                if f.endswith('.docx'):
                    os.remove(os.path.join(root, f))
                    n += 1
        assert n, 'fixture never injected: no documents were removed'
        return 'zero documents'

    def clean(dst):
        return ''

    return [
        ('11 a study printing a waterfall whose builder does not call the check',
         drop_scem_call, True, 'SCEM'),
        ('12 a builder that imports the module and never runs its assertion',
         import_but_never_call, True, 'SCEM'),
        ('13 a ratchet naming a study that is not on disk', ratchet_names_a_ghost, True,
         'NOSUCHCO'),
        ('14 an emptied population must FAIL, not report clean', empty_population, True,
         'zero'),
        ('15 the repository as it stands must stay GREEN', clean, False, ''),
    ]


def main():
    fails = []
    print('PART ONE — the instrument')
    for name, fn, must_raise in instrument_cases():
        try:
            fn()
            raised = False
        except TR.WaterfallError:
            raised = True
        ok = (raised == must_raise)
        print('  %-4s %s' % ('ok' if ok else 'FAIL', name))
        if not ok:
            fails.append(name)

    print('PART TWO — the gate')
    for name, mutate, expect_red, must_name in gate_cases():
        d, dst = sandbox()
        try:
            marker = mutate(dst)
            rc, out = run(dst)
            red = rc != 0
            ok = (red == expect_red)
            if ok and expect_red and must_name:
                ok = must_name.lower() in out.lower()
            print('  %-4s %s' % ('ok' if ok else 'FAIL', name))
            if not ok:
                fails.append(name)
                print('       rc=%d marker=%r' % (rc, marker))
                print('       ' + '\n       '.join(out.strip().splitlines()[-6:]))
        finally:
            shutil.rmtree(d, ignore_errors=True)

    total = len(instrument_cases()) + len(gate_cases())
    print('\n%d/%d conditions behaved as required' % (total - len(fails), total))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
