#!/usr/bin/env python3
"""A NEW STUDY MUST CLEAR EVERY GATE, AND THIS PROVES IT RATHER THAN ASSERTING IT.

[R-ENF-07]

WHY THIS EXISTS
    The point of a ratcheted gate is that knowingly-outstanding work is listed and allowed
    to fail while the build breaks on a NEW violation. Every gate in this repository says
    so in its own docstring, and every one is negative-controlled on its own conditions.
    What none of them tests is the claim the whole design rests on:

        A STUDY DIRECTORY CREATED TOMORROW, WITH NOTHING IN IT, GOES RED EVERYWHERE.

    That is a property of the SYSTEM rather than of any gate, so no gate can check it. It
    is also the exact claim the programme was asked to deliver — that a study is produced
    correctly and passes several checks without anyone intervening — and it is the kind of
    claim that is true by construction right up to the day a ratchet is seeded one entry
    too generously, or a gate globs a pattern a new directory happens not to match, or a
    check skips a study whose numbers file will not parse.

    So this walks the whole set: it copies the repository into a sandbox, plants an empty
    study directory called ZZTEST_study, and runs every ratcheted gate. Each one must go
    RED and must NAME the new study. A gate that stays green on a study with no numbers, no
    documents, no workbook, no sweep and no records is a gate a new name can walk past.

WHAT A PASS MEANS, AND WHAT IT DOES NOT
    A pass means every gate in the set REFUSES an unknown study directory. It does not mean
    the gates are individually right — each has its own negative control for that — and it
    does not mean a study cannot be wrong in a way no gate models. It means the guideline
    BINDS on a new name rather than depending on whoever builds it remembering to look.

USAGE
    python3 scripts/check_new_study_gauntlet.py           # gate
    python3 scripts/check_new_study_gauntlet.py --verbose # each gate's own last line
"""
import glob
import json
import os
import shutil
import subprocess
import re
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TICKER = 'ZZTEST'

# THE SET IS SPLIT, AND THE SPLIT IS THE FINDING [measured 03-Sep-2026 on the first run].
# A single list of "study gates" turned out to conflate two different kinds of check, and
# four of the seventeen stayed green on an empty directory for a perfectly good reason:
# they bite on ARTEFACTS, not on the directory. A study with no delivered documents cannot
# leak internal vocabulary and cannot publish a retired blend. Demanding that those gates
# refuse an empty directory would be a false claim about what they check — so they are
# tested the way they actually work, by planting a MINIMAL OFFENDING ARTEFACT and asserting
# they catch it.
#
# a builder that READS the artefact, which is what makes the artefact gate's subject exist
BUILDER_STUB = "import json\nd = json.load(open('diagnostics.json'))\n"

# DIRECTORY GATES: must refuse a study directory that exists and holds nothing. These are
# the checks a new name cannot walk past by simply not producing something.
DIRECTORY_GATES = [
    # An empty study directory commits no numbers file, which this gate reads as
    # having no readable inputs register and refuses unless another list already
    # records it as unreadable — so a new name goes red and is named.
    'check_four_field.py',
    # An empty study directory commits no spot and no date, and this gate reads a
    # study whose answer it cannot resolve as UNREADABLE rather than skipping it —
    # so a planted name goes red and is named. It belongs here rather than among
    # the artefact-conditional gates for the same reason check_four_field does:
    # what it reads is the numbers file, which every real study has and an empty
    # directory does not.
    'check_spot_currency.py',
    'check_study_provenance.py',
    'check_rebuild_ledger.py',
    'check_workbook_structure.py',
    'check_document_structure.py',
    'check_sweep_module.py',
    'check_prose_figures.py',
    'check_valuation_gap.py',
    'check_macro_coherence.py',
    'check_bridge.py',
    'check_lens_design.py',
    'check_cost_of_capital.py',
    'check_output_records.py',
    'check_forecast_anchor.py',
    'check_delivered_pdf_currency.py',
    'check_table_footing.py',
    'check_source_integrity.py',
    # ADDED 05-Sep-2026, and how it got here is the finding beside it. This gate has
    # always run over every study directory — through engine/valuation_calibration/
    # terminal_census.census(), which does the glob — so its own source carried no
    # `_study` and the detector below could not see it. It became visible only when an
    # unrelated comment in it happened to mention a study path. An empty directory has no
    # numbers file, the census reports it unreadable, and the gate refuses it by name.
    'check_terminal_floor.py',
    # ADDED 05-Sep-2026, BY THIS FILE'S OWN REFUSAL rather than by anyone remembering. Both
    # gates were adopted the same day and neither was listed here, so the gauntlet reported
    # 29 of 29 refusing while two study-scoped gates on disk had been tested by nothing — the
    # failure shape this file exists to close, occurring inside it. Both are directory-scoped:
    # an empty study directory declares no walk-forward scope and carries no recalculation
    # instrument, neither has a ratchet entry, and each refuses BY NAME.
    'check_walkforward_scope.py',
    'check_workbook_values.py',
    # ADDED 06-Sep-2026 IN THE COMMIT THAT ADOPTS THE GATE, per [R-ENF-01 EXT 04-Sep] and
    # the precedent this file set on 5 September, when it refused two gates adopted the day
    # before. DIRECTORY-scoped rather than artefact-scoped, and the reason is a clause the
    # gate carries deliberately: it is anchored [R-ENF-04] BOTH ways, so a study directory
    # for which it can find NO writer of the numbers file fails outright — a detector that
    # cannot find a generator has not proved there is none. An empty directory is exactly
    # that case, and the gate refuses it by name.
    'check_numbers_generators.py',
]

# ARTEFACT GATES: bite once the study produces the artefact they read, and are tested by
# planting one that should trip them. `plant` returns the files to create.
ARTEFACT_GATES = {
    'check_ke_reproduction.py': (
        # An empty study commits no cost-of-capital record, so refusing a bare directory
        # would be a false claim about what this gate checks [R-ENF-07]. Planted with a
        # record whose Ke does NOT reproduce from its own inputs.
        'a committed cost of equity that does not reproduce from its own inputs',
        lambda: {'study_numbers.json': ('json', {
            'cost_of_capital_record': {
                'rf_star': 0.1955, 'beta': 0.9275220650537075, 'erp': 0.0941,
                'ke_exp': 0.31277982632155385,
                'rf_terminal': 0.125, 'erp_terminal': 0.07,
                'ke_terminal': 0.189927, 'ke_terminal_construction': 'same_beta',
                'weight_equity': 0.96, 'weight_debt': 0.04,
                'weight_debt_terminal': 0.2}})}),
    'check_terminal_basis.py': (
        # An empty study directory contains no Python file calling TerminalInputs at all,
        # so refusing a bare directory would be a false claim about what this gate checks
        # [R-ENF-07]: it reads CALL SITES in the code rather than any committed record.
        # Planted with the defect exactly as SCEM and PHAR carried it — a flow handed to
        # the terminal already grown by (1+g), which the module's own contract says
        # overstates the terminal by exactly that.
        'a terminal fed a flow already grown by (1+g)',
        lambda: {'compute.py': ('text',
                                'import terminal_value as TV\n'
                                't = TV.build(TV.TerminalInputs(\n'
                                '    nopat=nopat[-1] * (1 + g_term),\n'
                                '    dna_book=dna[-1] * (1 + g_term),\n'
                                '    wacc=wacc_term, inflation=pi_term))\n')}),
    'check_asset_base_wired.py': (
        # An empty study commits no asset-base QUANTITY, so there is nothing that could be
        # registered-but-unread and refusing a bare directory would be a false claim about
        # what this gate checks [R-ENF-07]. Planted with the defect exactly: the quantity
        # committed, and no arithmetic anywhere that reads it.
        'an asset base committed and read by no arithmetic',
        lambda: {'study_numbers.json': ('json', {
            'land_bank_sqm_mn': 33.0,
            'asset_base_record': {'quantity': 'land_bank_sqm_mn', 'as_at': '2024-12-31'}}),
            'compute.py': ('text',
                           'CENTRAL = 17.85\n'
                           '# the land bank is printed in the document and enters nothing\n'
                           'def build():\n    return {"central": CENTRAL}\n')}),
    'check_lens_independence.py': (
        # An empty study has no builder, so no builder can be importing another lens and
        # refusing a bare directory would be a false claim [R-ENF-07]. Planted with the
        # breach: a builder that writes the committed numbers AND imports the price engine,
        # with no declaration.
        'a valuation builder importing the price engine',
        lambda: {'study_numbers.json': ('json', {'central': 17.85}),
                 'compute.py': ('text',
                                'import json\n'
                                'from engine.mc_v3 import simulate_paths_v3\n'
                                'def build():\n'
                                '    json.dump({"central": 17.85}, open("study_numbers.json", "w"))\n')}),
    'check_bridge_reaches_answer.py': (
        # An empty study commits neither figure, so there is no disagreement possible and
        # refusing a bare directory would be a false claim [R-ENF-07]. Planted with the
        # defect as it stands on the exemplar: a bridge arriving somewhere the published
        # answer is not.
        'an equity bridge that does not reach the answer the study publishes',
        lambda: {'study_numbers.json': ('json', {
            'bridge_record': {'per_share': 1.5263},
            'lens_record': {'central': 5.6054}})}),
    'check_ground_up.py': (
        # An empty study commits no driver lines and no summary, so it is in the unreadable
        # group by construction — which IS a refusal, and the right one. Planted with the
        # sharper case anyway: committed lines that fail the assertion when it is run.
        'driver lines that do not cover the revenue they claim to build',
        lambda: {'study_numbers.json': ('json', {
            'driver_lines': [{'name': 'one', 'level': 'unit', 'share_of_revenue': 0.4,
                              'unit': 'tonnes', 'unit_source': 'note 7',
                              'price_basis': 'realised price per tonne'}]})}),
    'check_record_survives_rebuild.py': (
        # An empty study has no generator, so there is no rebuild to attempt and refusing
        # a bare directory would be a false claim [R-ENF-07]. Planted with the defect: a
        # committed record no generator writes.
        'a committed record that its own rebuild removes',
        lambda: {'study_numbers.json': ('json', {'central': 1.23,
                                                 'forecast_anchor': {'x': 1}}),
                 'compute.py': ('text',
                                'import json, os\n'
                                'json.dump({"central": 1.23}, open(os.path.join('
                                'os.path.dirname(__file__), "study_numbers.json"), "w"))\n')}),
    'check_anchor_ordering.py': (
        # An empty study commits neither date, so there is no ordering to violate and
        # refusing a bare directory would be a false claim [R-ENF-07]. Planted with the
        # defect as it stands on the exemplar: a bridge on a later sheet than the profit
        # anchor, out of one filing.
        "a profit anchor behind the study's own balance sheet",
        lambda: {'study_numbers.json': ('json', {
            'bridge_record': {'balance_sheet_date': '2026-06-30'},
            'forecast_anchor': {'latest_reviewed_date': '2025-12-31'}})}),
    'check_terminal_spread.py': (
        # An empty study commits no terminal that reinvests, so there is no spread to earn
        # and refusing a bare directory would be a false claim about what this gate checks
        # [R-ENF-07]. Planted with the defect as it was found on ARCC: a terminal return
        # beneath the terminal cost of capital, reinvesting into it, declared nowhere.
        'a terminal reinvesting below its own cost of capital',
        lambda: {'study_numbers.json': ('json', {
            'roic_term': 0.1126, 'wacc_terminal': 0.1834, 'reinvestment_rate': 0.62})}),
    'check_output_sanity.py': (
        # An empty study commits no lens record, so there is no relationship between its
        # own figures to contradict and refusing a bare directory would be a false claim
        # about what this gate checks [R-ENF-07]. Planted with the defect as it was found:
        # a central published BENEATH a cross-check the study itself calls a floor.
        'a central published beneath the study\'s own disclosed floor',
        lambda: {'study_numbers.json': ('json', {
            'lens_record': {
                'class': 'refiner/petrochemical/cement',
                'primary': {'kind': 'dcf', 'value': 4.7459},
                'central': 4.7459,
                'cross_checks': [{'kind': 'book_value', 'value': 5.2046,
                                  'note': 'a disclosed FLOOR, published as such and '
                                          'never weighted'}]}})}),
    'check_asset_base.py': (
        # A study with NO numbers file commits no class, so it is not in this gate's
        # scope and refusing an empty directory would be a FALSE CLAIM about what it
        # checks [R-ENF-07]. Planted with the minimum that puts it in scope: a class
        # the registry calls asset-based, an information set, and no asset_base_record.
        'a study valued on a physical asset base that never states the vintage of it',
        lambda: {'study_numbers.json': ('json', {
            'meta': {'class': 'real-estate developer, off-plan, '
                              'percentage-of-completion',
                     'information_set_ends': '1Q2026'}})}),
    'check_delivered_vocabulary.py': (
        'a delivered document naming a standing rule',
        lambda: {'%s_Valuation_Study_03-09-2026.docx' % TICKER: ('docx', 'Adopted under '
                                                                 '[R-GAP-01] in September.')}),
    'check_waterfall_assertions.py': (
        'a delivered table instructing a reader whose builder never checks it',
        lambda: {'%s_Valuation_Study_03-09-2026.docx' % TICKER: ('docx', [
            ['EGP million', 'Value'],
            ['Enterprise value', '6,617'],
            ['Plus net cash', '4,930'],
            ['Equity value', '11,426'],
        ]),
            'build_it.py': ('py', BUILDER_STUB)}),
    'check_band_vocabulary.py': (
        'a delivered document carrying the retired verdict vocabulary',
        lambda: {'%s_Valuation_Study_03-09-2026.docx' % TICKER: (
            'docx', 'The cone FAILED CALIBRATION TEST over the resolved windows.')}),
    'check_column_widths.py': (
        'a delivered table whose column is too narrow for the figure it prints',
        lambda: {'%s_Valuation_Study_03-09-2026.docx' % TICKER: ('docx', (
            [['EGP million', 'FY2025'], ['Revenue', '(1,234,567.89)']], [2.0, 0.18]))}),
    'check_edition_date.py': (
        'a delivered document whose masthead disagrees with its own filename',
        lambda: {'%s_Valuation_Study_03-09-2026.docx' % TICKER: (
            'docx', 'Valuation study issued 1 January 2026')}),
    'check_site_data_reader.py': (
        'a study script reading assets/data.js with a regex instead of a real parse',
        lambda: {'read_it.py': ('py', "import re\n"
                                      "src = open('assets/data.js').read()\n"
                                      "m = re.search(r'levels', src)\n")}),
    'check_figure_axes.py': (
        'a figure script drawing a reference line outside its own axes',
        lambda: {'figures.py': ('py', "import matplotlib\n"
                                      "matplotlib.use('Agg')\n"
                                      "import matplotlib.pyplot as plt\n"
                                      "fig, ax = plt.subplots()\n"
                                      "ax.plot([1, 2, 3], [1, 2, 3])\n"
                                      "ax.set_ylim(0, 3)\n"
                                      "ax.axhline(99.0, color='r')\n"
                                      "fig.savefig('fig_out.png')\n")}),
    'check_sign_convention.py': (
        'a delivered table printing deductions in two sign conventions at once',
        lambda: {'%s_Valuation_Study_03-09-2026.docx' % TICKER: ('docx', [
            ['AED million', '2026E'],
            ['Less cash operating expenses', '(2,650)'],
            ['Less capital expenditure', '(1,012)'],
            ['Less increase in working capital', '440'],
            ['Free cash flow to the firm', '4,368'],
        ])}),
    # ARTEFACT-CONDITIONAL, LISTED IN THE COMMIT THAT ADOPTS THE GATE [R-ENF-07].
    # An empty study directory carries no numbers file and so makes no claim about a
    # correction; this gate bites on the CLAIM, which is a study asserting one that
    # no walk-forward run adopted. Demanding it refuse an empty directory would be a
    # false statement about what it checks.
    # ARTEFACT-CONDITIONAL, LISTED IN THE COMMIT THAT ADOPTS THE GATE [R-ENF-07].
    # Eleven of twenty-four studies carry no terminal record at all and every one of
    # them is legitimate, so an empty study directory is not a violation here and
    # demanding that this gate refuse one would be a FALSE CLAIM about what it checks.
    # It bites on a record that EXISTS and is short of the field set the module emits.
    # ARTEFACT-CONDITIONAL, LISTED IN THE COMMIT THAT ADOPTS THE GATE [R-ENF-07].
    # An empty study directory delivers no valuation document, so it has nothing to be
    # missing a bibliography FROM — refusing it would be a FALSE CLAIM about what this
    # gate checks. It bites on a study that DELIVERS a document and ships no
    # bibliography-class artefact beside it.
    # ARTEFACT-CONDITIONAL [R-ENF-07]: an empty study directory delivers no document
    # and so embeds no figure — there is nothing that could be translucent, and
    # refusing it would be a false claim about what this gate checks.
    'check_figure_opacity.py': (
        'a delivered document embedding a translucent figure',
        lambda: {'%s_Valuation_Study_03-09-2026.docx' % TICKER: ('docx_media', None)}),
    'check_bibliography.py': (
        'a delivered study with no standalone bibliography document',
        lambda: {'%s_Valuation_Study_03-09-2026.docx' % TICKER: ('docx', 'A study a '
                 'reader receives, with no bibliography beside it.')}),
    'check_terminal_record_shape.py': (
        'a committed terminal record short of the field set terminal_value.py emits',
        lambda: {'study_numbers.json': ('json', {
            'dcf': {'terminal_record': {
                'rule': 'R-TERM-01', 'fcff': 1.0, 'tv': 10.0,
                'inputs': {'nopat': 1.0, 'wacc': 0.12, 'inflation': 0.05}}}})}),
    'check_corrections_applied.py': (
        'a committed numbers file claiming an adopted correction with no walk-forward '
        'run behind it',
        lambda: {'study_numbers.json': ('json', {
            'adopted_correction': {'driver': 'a_driver_no_run_adopted', 'factor': 1.05}})}),
    'check_artefact_currency.py': (
        'a builder-read JSON carrying a central and declaring no vintage',
        lambda: {'diagnostics.json': ('json', {'central': 12.34, 'note': 'no declaration'}),
                 'build_it.py': ('py', BUILDER_STUB)}),
    'check_eps_reconciliation.py': (
        'a committed numbers file whose profit over shares does not reproduce the '
        'reported earnings per share, with nothing naming the difference',
        lambda: {'study_numbers.json': ('json', {
            'meta': {'shares_mn': 1000.0},
            'inputs': {
                'npa_fy25': {'value': 8000.0, 'source': 'audited FY2025 statements',
                             'date': '2026-02-01', 'ring': 'Company'},
                'eps_fy25': {'value': 7.00, 'source': 'audited FY2025 statements',
                             'date': '2026-02-01', 'ring': 'Company'}}})}),
    'check_harness_outputs.py': (
        'a pricing harness that can write the committed numbers file on the override path',
        lambda: {'compute.py': ('py',
                                'import json, os\n'
                                "BETA_OVERRIDE = os.environ.get('BETA_OVERRIDE')\n"
                                'beta = float(BETA_OVERRIDE) if BETA_OVERRIDE else 0.488\n'
                                "json.dump({'beta': beta}, "
                                "open('study_numbers.json', 'w'))\n")}),
    'check_source_rebinding.py': (
        'a source constant rebound after inputs were registered against it',
        lambda: {'compute.py': ('py',
                                'FS25 = "Consolidated Financial Statements FY2025"\n'
                                "inp('a', 1.0, FS25, '2025-12-31', 'COMPANY')\n"
                                'FS25 = "Annual Report 2025, note 15"\n'
                                "inp('b', 2.0, FS25, '2025-12-31', 'COMPANY')\n")}),
    # ADDED 06-Sep-2026 IN THE COMMIT THAT ADOPTS THE GATE, which is the whole point of
    # [R-ENF-01 EXT 04-Sep]: the two gates adopted on 5 September appeared in none of these
    # lists and this file reported "29 of 29 refuse a new study" while two of the gates it
    # was counting had been tested by nothing. This one is ARTEFACT-conditional rather than
    # directory-conditional: an empty study directory commits no strike date and no
    # currency, so there is nothing to hold against an anchor and refusing it would be a
    # FALSE CLAIM about what this gate checks. It bites once the study commits both.
    'check_macro_anchor_age.py': (
        'a study struck long after the currency anchor its own path derives from',
        lambda: {'study_numbers.json': ('json', {
            'meta': {'spot_date': '2026-09-03', 'currency': 'EGP'}})}),
}

# NOT IN EITHER SET, and each with the reason, because a name in a list that resolves to
# the wrong subject is worse than an absence [R-ENF-04]:
#   check_valuation_inputs.py       anchors on WALK-FORWARD run directories, not on study
#                                   directories — a new study is not its subject
#   check_calibration_deliverables.py  anchors on the campaign queue's calibrated names
#   check_lens_vocabulary.py        reads delivered PDFs; with no PDF there is nothing to
#                                   read, and its own population anchoring covers the case
#                                   where the whole book has none
EXCLUDED = {
    'check_fetch_authenticity.py': 'its population is the TRACKED TREE — git ls-files — '
                                   'because its subject is whether a committed file is the '
                                   'type it claims and whether a stored source is a block '
                                   'page. It reaches into study directories, so the '
                                   'detector is right to see it, but a study planted in '
                                   'this sandbox is UNTRACKED and the gate therefore says '
                                   'nothing about it, correctly. Demanding a nonzero exit '
                                   'would make it claim a new study had committed a WAF '
                                   'page under a filing\'s name when it has committed '
                                   'nothing at all',
    'check_tree_unmodified.py': 'its subject is THE RUN rather than any study — it asks '
                                'whether the checks that ran modified the tracked tree, '
                                'and a planted study directory is untracked, which this '
                                'gate deliberately says nothing about. Demanding a nonzero '
                                'exit would make it claim a check had rewritten a '
                                'committed file when nothing had',
    'check_valuation_inputs.py': 'anchors on walk-forward run directories, not study '
                                 'directories',
    'check_calibration_deliverables.py': "anchors on the campaign queue's calibrated names",
    'check_lens_vocabulary.py': 'reads delivered PDFs; an empty study has none',
    'check_published_lens_vocabulary.py': 'its subject is the reader-facing SITE — the ticker pages and the coverage grid. A study directory planted in a sandbox publishes no page, so demanding a nonzero exit would be a FALSE claim about what this gate checks',
    'check_published_gap.py': 'its subject is the SITE — the gap a READER computes from assets/data.js. A planted study directory publishes no fair value, and the gate takes its population from the published names rather than from the directories',
    'check_error_injection.py': 'its subject is THE SYSTEM\'s detection claim rather than any study: it copies the repository and plants named real errors of its own. Running it inside this sandbox is a harness inside a harness, and its own baseline step would be measuring this run rather than the book',
    'check_standard_claim.py': 'its subject is the RELATION between a study\'s claimed standard version and the ratchets recording who does not meet it. A planted study is on no ratchet, so it conforms by construction — correctly, since a new study owes no debt — and plant() writes only inside the study directory, so the relation cannot be created from here. Refusing an empty directory would assert a debt that does not exist',
    'check_page_integrity.py': "its subject is the site's ticker pages; the only mention "
                               'of a study directory in it is a comment',
    'check_screen_block.py': 'its subject is the SCREEN block in assets/data.js. It reads '
                             'study directories only to ask whether a rebuilt central '
                             'EXISTS — the answer for a new empty directory is no, which '
                             'is the correct reading and not a refusal. Demanding a nonzero '
                             'exit would make it claim a study is superseded on the '
                             'strength of the directory being there',
    'check_published_coverage.py': 'holds PUBLISHED fair values against the studies behind '
                                   'them, so a study directory is its reference set rather '
                                   'than its subject — a new directory publishes nothing '
                                   'and there is correctly nothing to refuse',
    'check_publish_block.py': '[R-GAP-02] deliberately carries NO ratchet because it blocks '
                              'a FUTURE act rather than condemning a past one, and a held '
                              'study is not a red build. It reads the new study as '
                              'unreadable and HOLDS it, which is the rule working; '
                              'demanding a nonzero exit would contradict the rule',
    'check_new_study_gauntlet.py': 'this file',
    'check_exemplar_debt.py': 'its subject is the model report and the ratchets naming '
                              'it; a new empty study directory is not the exemplar and '
                              'there is correctly nothing for it to refuse',
    'check_lessons_register.py': 'anchors on the WALK-FORWARD run directories and the '
                                 'lessons behind them, not on study directories',
    'check_protocol_text.py': 'reads the two governing documents; it names study '
                              'directories only to check that what they claim exists '
                              'does exist',
    'check_walkforward_actuation.py': 'anchors on walk-forward runs, not on study '
                                      'directories',
    # ADDED 07-Sep-2026 IN THE COMMIT THAT ADOPTS THE GATE [R-ENF-07].
    'check_forward_ranges.py': 'anchors on the WALK-FORWARD run directories that '
                               'commit a band, not on study directories. A new '
                               'empty study has no run behind it, so there is '
                               'correctly no band whose absence from a document '
                               'could be refused; it reads study directories only '
                               'to find the document a run already owes',
    # ADDED 09-09-2026 IN THE COMMIT THAT ADOPTS THE GATE [R-ENF-07]. It compares a
    # study's TYPED artefact names against the dates its own committed record states,
    # so its whole subject is a record that already exists. A new empty study
    # directory has no study_numbers.json, therefore no owned dates, therefore
    # nothing a typed name could contradict -- and it is reported as
    # no_dated_record rather than passed over, so the population stays visible.
    # Demanding a nonzero exit here would be asking it to refuse a study for
    # holding no dates, which is not what the rule says.
    'check_typed_dates.py': 'compares typed artefact names against the dates a '
                            'study RECORD already states; a new empty study has no '
                            'record, so there is correctly nothing to contradict',
    # Anchors on recalc.py, not on the study directory: a study with no recalculator has
    # no typed workbook name that could be stale. Its own population guard is stricter
    # than a refusal here would be -- it goes red when the recalculator glob finds
    # NOTHING, so the layout moving cannot read as every study being clean.
    # Anchors on engine/prices/, not on study directories: a new study adds no supplied
    # price, so there is correctly nothing of its to contradict. Its own population guard
    # is stricter than a refusal here -- it goes red when the price file is absent or
    # carries no entries, so the layout moving cannot read as every price agreeing.
    'check_supplied_prices.py':
        'anchors on the supplied price files and the OHLC libraries, not on study '
        'directories; a new empty study supplies no price',
    'check_recalculator_target.py':
        'anchors on each study\'s recalc.py and the workbooks beside it; a new empty '
        'study has no recalculator, so there is correctly no typed target to hold '
        'against an artefact',
}


# THE LISTS ARE HAND-MAINTAINED, WHICH MEANS A GATE ADDED TOMORROW IS SILENTLY UNTESTED
# AND THIS FILE STILL REPORTS CLEAN — the [R-ENF-04] species inside the very check written
# to close it. The completeness clause below reads the gates on disk rather than trusting
# the lists: any script that resolves study directories for itself is study-scoped, and
# must be named in EXACTLY ONE of the three lists. A new gate then fails this run until
# somebody says which kind it is, which is the whole point of the file.
STUDY_SCOPED = re.compile(r"engine['\"/,\s]{0,4}\*_study|_study['\"]?\s*\)|glob\("
                          r"[^)]*_study")


def study_scoped_gates(repo):
    """Every gate on disk that resolves study directories for itself."""
    out = set()
    for path in sorted(glob.glob(os.path.join(repo, 'scripts', 'check_*.py'))):
        name = os.path.basename(path)
        if name.endswith('_negative_control.py'):
            continue                     # a control is evidence about a gate, not a gate
        try:
            src = open(path, encoding='utf-8').read()
        except OSError:
            continue
        # ANY script that RESOLVES a study directory, not only one that globs the literal
        # pattern. Five gates construct the path instead — "engine/%s_study" % ticker —
        # and the first draft of this clause could not see them, which is the same
        # under-detection it exists to close, one level down. A comment about "the study"
        # carries no underscore, so this stays exact rather than becoming a word search.
        #
        # AND A GATE MAY DELEGATE THE RESOLUTION ENTIRELY [widened 05-Sep-2026].
        # check_terminal_floor.py runs over every study directory through
        # terminal_census.census(), which does the glob, so its own source carried no
        # `_study` at all and this detector could not see it — for as long as it has
        # existed. It surfaced only because an unrelated comment added to that gate
        # happened to name a study path, which is luck rather than a check. So the
        # first-party modules a gate imports are read too, one level down: a gate that
        # hands its population to a shared instrument is still a gate over that
        # population.
        if '_study' in src or _imports_a_study_resolver(repo, src):
            out.add(name)
    return out


def _imports_a_study_resolver(repo, src):
    """Does this script import a first-party module that resolves study directories?"""
    # NO REGEX HERE, DELIBERATELY. [R-ENF-03]'s gate refuses a regular-expression call in
    # any file that reads assets/data.js, and this file does — it plants a study script
    # reading data.js as one of its own fixtures. A pattern-scan call added here for an
    # unrelated purpose tripped that gate the first time it ran, which is the right
    # outcome: the rule is about the FILE, not about which line the call sits on. Splitting
    # the line is enough for an import statement and needs no pattern.
    #
    # AND THE COMMENT EXPLAINING THAT TRIPPED IT TOO, because it named the call. Worth
    # leaving recorded rather than tidied away: a shape-matching check cannot tell a call
    # from a description of one, which is the cost of shape-matching and is why it is only
    # used where the shape cannot occur innocently. Here it can, in a comment — so the
    # comment says what happened without writing the call.
    mods = set()
    for line in src.splitlines():
        head = line.strip()
        if head.startswith('import ') or head.startswith('from '):
            parts = head.split()
            if len(parts) >= 2:
                mods.add(parts[1].rstrip(','))
    for m in mods:
        rel = m.replace('.', os.sep)
        for cand in (os.path.join(repo, rel + '.py'),
                     os.path.join(repo, rel, '__init__.py'),
                     os.path.join(repo, 'engine', rel + '.py'),
                     os.path.join(repo, 'scripts', rel + '.py')):
            if os.path.exists(cand):
                try:
                    if '_study' in open(cand, encoding='utf-8').read():
                        return True
                except OSError:
                    continue
    return False


def sandbox():
    """A copy of the repository with one empty study directory planted in it.

    Copied rather than mutated: a gate that rebuilds a ratchet, or a --prune run reached by
    accident, must not be able to touch the real tree. This repository has already paid for
    running repo-mutating steps against a live checkout once.
    """
    tmp = tempfile.mkdtemp(prefix='gauntlet_')
    def ignore(d, names):
        # raw_indices was excluded in the first draft and check_study_provenance CRASHED on
        # its absence — going red for the wrong reason, which reads exactly like going red
        # for the right one. An excluded directory a gate needs is a sandbox defect
        # masquerading as a finding [R-ENF-04].
        # raw_ohlc (16MB) and panels (2.6MB) are COPIED, not excluded, and the cost is
        # accepted deliberately. The first draft excluded raw_indices and a gate crashed
        # on the absence, going red for the WRONG reason — which reads exactly like going
        # red for the right one [R-ENF-07]. Excluding these two reproduced that failure in
        # three more gates the day the lists were completed: page_integrity refused for a
        # missing OHLC population, band_vocabulary for a legacy page whose panel was not
        # there, figure_axes for figure scripts that could not run. A SANDBOX DEFECT
        # MASQUERADING AS A FINDING IS THE MORE DANGEROUS OUTCOME, because it is green-
        # looking evidence that a gate works.
        return [n for n in names
                if n in ('.git', '__pycache__', 'node_modules', 'filings')]
    shutil.copytree(ROOT, os.path.join(tmp, 'repo'), ignore=ignore, symlinks=True)
    repo = os.path.join(tmp, 'repo')
    os.makedirs(os.path.join(repo, 'engine', '%s_study' % TICKER.lower()), exist_ok=True)
    return tmp, repo


# THE TOOL CONTRACT. A gate that cannot run because a TOOL is absent exits 2, never
# 1: both are failures and neither is clean [R-ENF-04], but they send a reader to
# different repairs — one to the gate or the study, the other to the environment.
TOOL_EXIT = 2


def run(repo, gate):
    r = subprocess.run([sys.executable, os.path.join('scripts', gate)],
                       cwd=repo, capture_output=True, text=True, timeout=1800)
    out = (r.stdout or '') + (r.stderr or '')
    lines = [l for l in out.strip().splitlines() if l.strip()]
    return r.returncode, out, (lines[-1] if lines else '')


def plant(sdir, files):
    """Create the artefacts an artefact gate needs as its subject."""
    for name, (kind, payload) in files.items():
        path = os.path.join(sdir, name)
        if kind == 'docx':
            import docx
            d = docx.Document()
            if isinstance(payload, tuple):
                # (rows, widths_in_inches) — a gate whose subject is a COLUMN WIDTH cannot
                # be tested by a table that does not carry one
                rows_, widths = payload
                t = d.add_table(rows=len(rows_), cols=len(rows_[0]))
                t.autofit = False
                for j, w in enumerate(widths):
                    t.columns[j].width = docx.shared.Inches(w)
                for i, row in enumerate(rows_):
                    for j, cell in enumerate(row):
                        t.cell(i, j).text = str(cell)
                        t.cell(i, j).width = docx.shared.Inches(widths[j])
            elif isinstance(payload, list):
                # a TABLE fixture: [[cell, ...], ...]. A gate whose subject is a table
                # cannot be given a paragraph and be said to have been tested.
                t = d.add_table(rows=len(payload), cols=len(payload[0]))
                for i, row in enumerate(payload):
                    for j, cell in enumerate(row):
                        t.cell(i, j).text = str(cell)
            else:
                d.add_paragraph(payload)
            d.save(path)
        elif kind == 'docx_media':
            # A document EMBEDDING A TRANSLUCENT IMAGE. A gate whose subject is the
            # pixel data of a delivered figure cannot be tested by a paragraph.
            import io as _io
            import docx
            from PIL import Image
            im = Image.new('RGBA', (12, 12), (255, 255, 255, 0))   # fully transparent
            buf = _io.BytesIO()
            im.save(buf, format='PNG')
            buf.seek(0)
            d = docx.Document()
            d.add_paragraph('A delivered study with a figure in it.')
            d.add_picture(buf)
            d.save(path)
        elif kind == 'json':
            json.dump(payload, open(path, 'w', encoding='utf-8'))
        else:
            open(path, 'w', encoding='utf-8').write(payload)


def main(argv):
    verbose = '--verbose' in argv
    tmp, repo = sandbox()
    sdir = os.path.join(repo, 'engine', '%s_study' % TICKER.lower())
    try:
        print('NEW-STUDY GAUNTLET — an empty engine/%s_study/ planted in a sandbox copy'
              % TICKER.lower())
        print('%d directory gates, %d artefact gates, %d excluded with a stated reason\n'
              % (len(DIRECTORY_GATES), len(ARTEFACT_GATES), len(EXCLUDED)))

        red, wrong, missing, notool = [], [], [], []

        print('DIRECTORY GATES — must refuse a study directory that holds nothing')
        for gate in DIRECTORY_GATES:
            if not os.path.exists(os.path.join(repo, 'scripts', gate)):
                missing.append(gate)
                continue
            try:
                rc, out, last = run(repo, gate)
            except Exception as e:                                      # noqa: BLE001
                rc, out, last = 1, '', '%s: %s' % (type(e).__name__, e)
            named = TICKER.lower() in out.lower()
            # EXIT 2 IS THE TOOL CONTRACT: the gate could not run, so it has refused
            # nothing and its silence says nothing about the study. Counting that as a
            # permissive gate is the gauntlet's own first-run finding arriving a second
            # time — on 04-Sep-2026 three gates hit it in CI (poppler installed 320 lines
            # below this step, matplotlib never installed at all) and this file reported
            # "3 gate(s) did not refuse the new study". They had refused nothing because
            # they had run nothing, and those are different repairs. It still FAILS the
            # run [R-ENF-04]; what changes is which way it sends the reader.
            if rc == TOOL_EXIT:
                notool.append((gate, rc, named, last))
                print('   %-4s %-40s exit %d   (could not run — broken tool)'
                      % ('TOOL', gate, rc))
                if verbose:
                    print('        %s' % last[:150])
                continue
            ok = rc != 0 and named
            (red if ok else wrong).append((gate, rc, named, last))
            print('   %-4s %-40s exit %d%s' % ('RED ' if ok else 'MISS', gate, rc,
                                               '' if named else '   (does not name it)'))
            if verbose:
                print('        %s' % last[:150])

        print('\nARTEFACT GATES — bite once the study produces what they read')
        for gate, (what, mk) in ARTEFACT_GATES.items():
            if not os.path.exists(os.path.join(repo, 'scripts', gate)):
                missing.append(gate)
                continue
            for f in os.listdir(sdir):
                os.remove(os.path.join(sdir, f))
            try:
                plant(sdir, mk())
                rc, out, last = run(repo, gate)
            except Exception as e:                                      # noqa: BLE001
                rc, out, last = 0, '', '%s: %s' % (type(e).__name__, e)
            named = TICKER.lower() in out.lower()
            if rc == TOOL_EXIT:                       # see the note above
                notool.append((gate, rc, named, last))
                print('   %-4s %-40s exit %d   (could not run — broken tool)'
                      % ('TOOL', gate, rc))
                if verbose:
                    print('        %s' % last[:150])
                continue
            ok = rc != 0 and named
            (red if ok else wrong).append((gate, rc, named, last))
            print('   %-4s %-40s exit %d   %s' % ('RED ' if ok else 'MISS', gate, rc, what))
            if verbose:
                print('        %s' % last[:150])
        for f in os.listdir(sdir):
            os.remove(os.path.join(sdir, f))

        print('\nEXCLUDED, each with its reason')
        for gate, why in EXCLUDED.items():
            print('   %-45s %s' % (gate, why))
            if not os.path.exists(os.path.join(repo, 'scripts', gate)):
                missing.append(gate)

        print('\n%d of %d gates refuse a new study'
              % (len(red), len(red) + len(wrong)))
        rc = 0
        if missing:
            print('\nFAIL — %d gate(s) named in this file do not exist: %s'
                  % (len(missing), ', '.join(sorted(set(missing)))))
            print('The lists ARE the claim; a name resolving to nothing means the claim is '
                  'about a gate that is not there [R-ENF-04].')
            rc = 1
        unlisted = sorted(study_scoped_gates(repo)
                          - set(DIRECTORY_GATES) - set(ARTEFACT_GATES) - set(EXCLUDED))
        if unlisted:
            print('\nFAIL — %d study-scoped gate(s) on disk are named in none of the three '
                  'lists: %s' % (len(unlisted), ', '.join(unlisted)))
            print('A gate nobody listed is a gate this run never tested, and the run still '
                  'reports clean — which is the failure shape this whole file exists to '
                  'close, occurring inside it. Say which kind it is.')
            rc = 1
        if notool:
            print('\nFAIL — %d gate(s) COULD NOT RUN; a tool they need is absent, so they '
                  'refused nothing and their silence is not evidence [R-ENF-04]:'
                  % len(notool))
            for gate, code, _named, last in notool:
                print('   %-40s exit %d' % (gate, code))
                print('        %s' % last[:170])
            print('Fix the ENVIRONMENT, not the gate: every tool a gate needs is installed '
                  'before any gate runs. This is not a finding about the study.')
            rc = 1
        if wrong:
            print('\nFAIL — %d gate(s) did not refuse the new study, or went red without '
                  'naming it:' % len(wrong))
            for gate, code, named, last in wrong:
                print('   %-40s exit %d  names it: %s' % (gate, code, named))
                print('   %-40s   %s' % ('', last[:130]))
            print('\nA gate that does not refuse a study with no numbers, no documents, no '
                  'workbook, no sweep and no records is one a new name can walk past. '
                  'Either it should cover a new study and does not, or it belongs in '
                  'ARTEFACT_GATES or EXCLUDED — and saying WHICH is the whole point of '
                  'this file.')
            rc = 1
        if rc == 0:
            print('\nOK — every directory gate refuses an empty study by name, and every '
                  'artefact gate catches a planted offender. The guideline binds on a new '
                  'study rather than on whoever builds it remembering to look.')
        return rc
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
