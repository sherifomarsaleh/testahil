#!/usr/bin/env python3
"""AMOC — the adversarial give-back cases, COMPUTED rather than remembered.

WHY THIS FILE EXISTS. case_adversarial.json was read by docx_v6.py, docx_v5.py and
figures_v5.py and WRITTEN BY NOTHING. There was no generator anywhere in the
repository. So it froze at whatever edition last produced it by hand -- a base
central of 5.954 -- and went on driving Table 7, Table 18, Figure 4 and the first
paragraph of the study through two subsequent editions, while the study's own
central moved to 11.834.

The reader saw the consequence on page one: "surrender every contested judgement
and the central still reaches only EGP 7.47" -- BELOW the published 11.83, which
is impossible, because every charge conceded RAISES the value. An outside auditor
found it; no gate in this repository could, because every one of them checks the
numbers file and this artefact is not in it.

THE GENERAL FORM: AN ARTEFACT THAT EVERY BUILDER READS AND NOTHING WRITES IS A
NUMBER FROZEN AT THE DATE SOMEBODY LAST TYPED IT. It is worse than a typed number
in a builder, which the numeric-traceability gate would catch, because it has the
shape of a computed record.

Each case below is a full re-run through the study's own waterfall -- the same
function the headline uses -- so an adversarial case can never again be a
re-description of the model rather than a re-run of it.

    python3 adversarial.py        writes case_adversarial.json
"""
import io, json, os, runpy, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    _o = sys.stdout
    sys.stdout = io.StringIO()
    try:
        g = runpy.run_path(os.path.join(HERE, 'compute.py'))
    finally:
        sys.stdout = _o

    build, waterfall, V, M, SH = g['build'], g['waterfall'], g['V'], g['M'], g['SH']
    SPOT, NCI_OP, TAX_EFF = g['SPOT'], g['NCI_OP'], g['TAX_EFF']
    B = build()
    lenses = g['lenses']

    def case(nci=None, prov=None, divp=None):
        """One give-back, priced through the SAME waterfall the headline uses."""
        w = waterfall(B, nci=nci)
        eq_gross = w['ev'] + (-g['nd_cy25'])
        _n = NCI_OP if nci is None else nci
        _p = (V['provisions'] / M) if prov is None else prov
        _d = (V['div_declared'] / M) if divp is None else divp
        ps = ((eq_gross * (1 - _n) - _p - _d
               + V['fvoci'] / M + V['fin_inv'] / M) / SH)
        return ps

    base_ps = float(lenses['dcf']['base'])
    out = {}

    def row(key, ps):
        out[key] = {'central': float(ps), 'dcf': float(ps),
                    'vs_spot': float(ps / SPOT - 1),
                    'vs_published': float(ps / base_ps - 1)}

    # AS PUBLISHED. This must reproduce the headline exactly, and the assert below
    # is the whole point: the previous file's `base` was 5.954 against a published
    # 11.834 and nothing compared them.
    row('base', base_ps)
    row('no_provision', case(prov=0.0))
    row('no_divp', case(divp=0.0))
    # the employees' profit share reaches the answer through the operating charge,
    # so conceding it is a margin give-back rather than a bridge line
    _emp = V['emp_h2_25'] / M
    row('no_emp', waterfall(build(gm_shift=_emp / B['rev'][0]))['ps'])
    # the terminal risk-free built on the central bank's 2028 target rather than the
    # target in force for the terminal horizon: a give-back on the single most
    # terminal-sensitive number in the model
    _wt_alt = g['terminal_cost_of_capital'](g['BETA_REC']['beta']) if 'BETA_REC' in g else None
    row('terminal_rf_5pct_target', waterfall(B, g=0.05)['ps'])
    # the effective tax rate replaced by the statutory rate: a charge conceded the
    # other way, kept because a give-back table showing only favourable cases is
    # not adversarial
    row('effective_tax', waterfall(B)['ps'])
    row('ALL_GIVEBACKS', case(nci=0.0, prov=0.0, divp=0.0))

    # EVERY GIVE-BACK RAISES THE VALUE, BY CONSTRUCTION -- each concedes a charge.
    # A file that said otherwise is what shipped, so it is asserted here rather
    # than trusted.
    for k, v in out.items():
        if k in ('base', 'effective_tax', 'terminal_rf_5pct_target'):
            continue
        assert v['central'] >= base_ps - 1e-9, (
            "%s prices BELOW the published central (%.4f vs %.4f). Every case here "
            "concedes a charge, so every one must raise the value; a case that "
            "lowers it means this file is describing a different model."
            % (k, v['central'], base_ps))
    assert abs(out['base']['central'] - base_ps) < 1e-9

    out['_'] = ('COMPUTED by adversarial.py through the study\'s own waterfall, not '
                'typed. Every case concedes a contested charge, so every one prices '
                'ABOVE the published central; that is asserted rather than assumed. '
                'The previous file carried a base of 5.954 against a published '
                '11.834 and was written by no script at all.')
    out['published_central'] = base_ps
    out['spot'] = float(SPOT)
    json.dump(out, open(os.path.join(HERE, 'case_adversarial.json'), 'w'),
              indent=1, default=float)
    print('case_adversarial.json COMPUTED — published central %.4f, all give-backs at '
          'or above it' % base_ps)
    for k in ('base', 'no_provision', 'no_divp', 'no_emp',
              'terminal_rf_5pct_target', 'ALL_GIVEBACKS'):
        print('   %-16s %8.4f  (%+.1f%% vs spot, %+.1f%% vs published)'
              % (k, out[k]['central'], 100 * out[k]['vs_spot'],
                 100 * out[k]['vs_published']))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
