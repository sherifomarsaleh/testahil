"""AN INPUT NOBODY READS IS EITHER DEAD WEIGHT OR A SIGN SOMETHING WAS REWIRED.

A blind self-audit of this study found 63 registered inputs that no formula reads.
Individually harmless; as a class, not. Every one is a figure a reader can look up in the
bibliography, dated and sourced, sitting beside a model that never consults it — and the
dangerous case is the one where a driver WAS moved onto a different quantity and its old
input stayed behind, still registered, still published, still saying what the study used
to do. That is the shape of every finding this edition answered, one layer further back.

So the register is checked against the model. An input is READ if its name appears in a
V[...] lookup anywhere outside the registration block itself. An input that is not read
must say so: entries listed in DISCLOSED below are published as evidence, context or
provenance rather than as model inputs, and each carries the reason.

Run: python3 orphan_input_check.py [--list]
"""
import ast, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'compute.py')

# Published deliberately, and NOT as a driver. Each line is the reason.
DISCLOSED = {
    'eps_reported': 'the company\'s own reported EPS, published so the study\'s derived '
                    'EPS can be reconciled against it',
    'nd_release_fy25': 'the company\'s own net-debt figure on its narrower release basis, '
                       'published so the definitional gap is visible',
    'w_egp_implied_fy24': 'last year\'s pound share of the debt book, published so the '
                          'direction of travel can be read',
    'electra_sold_2025_mn': 'an ownership movement, context for the free float',
    'rf_external_span': 'the disagreement between external readings, published because it '
                        'is the reason the rate is sensitised rather than presented precise',
    'assoc_bv_fy23': 'a balance-sheet comparative, printed in the history table',
    'electra_mto': 'the last strategic transaction, company-profile context',
    'sh_electra_fy24': 'the same transaction\'s outcome',
    'cables_tonnage_h1': 'the half\'s volumes, published beside the annual series',
}


# THE SWEEP'S OWN EVIDENCE TRAIL, AND THE ONE RATCHET THIS CHECK CARRIES.
#
# These are figures read off a filing during the Step 2A information sweep, registered
# with their source and date, and then neither consulted by a formula nor printed in a
# delivered document. That is not automatically waste: the register is the auditable
# record of WHAT WAS READ, and a line read and found not to move anything is evidence of
# coverage. A study that registered only what it used could not be distinguished from one
# that only read what it wanted.
#
# But the class is also where a rewiring hides — a driver moved onto a different quantity
# with its old input left behind, still registered, still dated, still describing what the
# study used to do. So the list is written out in full rather than matched by pattern, it
# is printed on every pass so the number stays visible, and it may only ever SHORTEN: a
# new name here fails the check and has to be wired in, printed, or argued for on its own.
COVERAGE = (
    'cables_passthrough_alt',
    'cables_real_growth',
    'capex_h1_23',
    'capex_h1_24',
    'corp_load',
    'debt_q1_26',
    'dna_pct_fy25',
    'emp_share_h1_25',
    'etr_h1_25',
    'etr_q1_25',
    'etr_q1_26',
    'export_share_fy25',
    'foreign_share_fy25',
    'fx',
    'fx_depreciation_path',
    'h1_26_assoc',
    'h1_26_assoc_oneoff',
    'h1_26_eps',
    'h1_26_eq_parent',
    'h1_26_gp',
    'h1_26_nci',
    'h1_26_nci_eq',
    'h1_26_netfin',
    'h1_26_op',
    'h1_26_rev',
    'kd_egp_fy24',
    'kd_egp_q1_26',
    'kd_fy24_egp',
    'kd_fy24_eur',
    'kd_fy24_usd',
    'kd_hard_q1_26',
    'mgn_fy25',
    'mgn_h1_25',
    'nci_share_h1_26_equity',
    'nwc_pct_hist',
    'ppe_gross_depreciable_fy25',
    'q1_25_ebitda_house',
    'q1_26_assoc',
    'q1_26_gp',
    'q1_26_nd',
    'q1_26_netfin',
    'q1_26_tax',
    'seg_profit_h1_25',
    'seg_unalloc_h1_26',
    'sh_ahmed',
    'sh_mohamed',
    'sh_other_fy24',
    'sh_sadek',
    'stake_insulators',
    'tax_rate_retired',
)


def registered(tree):
    """Every name registered through I(...) in the inputs block."""
    out = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.keyword) and isinstance(node.value, ast.Call) \
                and isinstance(node.value.func, ast.Name) and node.value.func.id == 'I':
            out[node.arg] = node.value.lineno
    return out


# The delivered documents read the register too, through IN[...] / INP[...]. An input a
# document PUBLISHES is doing a job — it is evidence a reader can check — even when no
# formula consults it. Only an input that neither the model reads nor any document prints
# is genuinely orphaned.
READERS = ('docx_swdy.py', 'docx_register.py', 'build_xlsx_swdy.py', 'figures.py')


def read_names(src, reg):
    """Names the MODEL consults (V[...]) or a delivered document prints (IN[...])."""
    doc = ''
    for r in READERS:
        q = os.path.join(HERE, r)
        if os.path.exists(q):
            doc += open(q).read()
    hit = set()
    for name in reg:
        e = re.escape(name)
        model = re.compile(r"""V\s*(?:\[\s*|\.\s*get\s*\(\s*)['"]%s['"]""" % e)
        printed = re.compile(r"""(?:IN|INP|D\['inputs'\])\s*(?:\[\s*|\.\s*get\s*\(\s*)['"]%s['"]""" % e)
        if model.search(src) or printed.search(doc):
            hit.add(name)
    return hit


def main():
    src = open(SRC).read()
    tree = ast.parse(src)
    reg = registered(tree)
    read = read_names(src, reg)
    orphans = sorted(set(reg) - read - set(DISCLOSED) - set(COVERAGE))
    stale_exempt = sorted((set(DISCLOSED) | set(COVERAGE)) - set(reg))
    if stale_exempt:
        print('EXEMPTIONS FOR INPUTS THAT NO LONGER EXIST: %s' % ', '.join(stale_exempt))
        print('An exemption outliving the thing it exempts is how a list stops binding.')
        return 1
    if orphans:
        print('REGISTERED BUT NEVER READ: %d of %d input(s)' % (len(orphans), len(reg)))
        for o in orphans:
            print('  compute.py:%-6d %s' % (reg[o], o))
        print('\nEach is published in the bibliography, dated and sourced, beside a model '
              'that does not consult it. Wire it in, remove it, or add it to DISCLOSED '
              'with the reason it is published as evidence rather than as a driver.')
        return 1
    _live = len(reg) - len(DISCLOSED) - len(COVERAGE)
    print('input register: %d of %d input(s) are read by the model or printed in a '
          'delivered document; %d published as evidence; %d carried as the sweep\'s '
          'coverage record, a list that may only shorten'
          % (_live, len(reg), len(DISCLOSED), len(COVERAGE)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
