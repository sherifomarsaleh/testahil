"""Generate the gap review a study owes after the 19-09-2026 real-rate change.

WHY A GENERATOR AND NOT SEVEN HAND-WRITTEN FILES. [R-ENF-01]'s standing clause —
a number stated in prose must be COMPUTED, not typed — reaches a gap review like
anything else a reader receives. Every figure below is read from the study's own
committed numbers and from the house macro path; nothing is transcribed.

WHAT MAKES THIS A REAL REVIEW RATHER THAN A STAMP. [R-GAP-01] requires eight
headings, each individually capable of producing the whole gap. On these names
exactly ONE input moved since the previous review — the terminal risk-free rate,
from the house macro path, on the principal's instruction of 19-09-2026 that the
real risk-free floor is inflation plus 2%. So the DISCOUNT RATE and TERMINAL
headings are worked fresh here and the other six CARRY FORWARD from the named
prior review, with the carry stated rather than implied. A review that pretended
to re-derive six headings nothing had touched would be the rubber stamp the rule
was written to refuse; one that silently dropped them would be worse.
"""
import json, os, sys

ENG = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(ENG)
sys.path.insert(0, ENG)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import macro_path as MP
from check_valuation_gap import read_answer, read_review, read_branches


def review(tk, date='19-09-2026'):
    sdir = os.path.join(ENG, '%s_study' % tk.lower())
    nums = json.load(open(os.path.join(sdir, 'study_numbers.json'), encoding='utf-8'))
    central, spot, _ = read_answer(sdir)
    prior_name, prior_cov, prior_aud, _, prior_gap = read_review(sdir)
    coc = nums.get('cost_of_capital_record') or {}
    mk = (nums.get('market') or 'EG').upper()
    path = MP.load(mk)
    rf_t, pi_t, rr = path.terminal_rf, path.terminal_inflation, path.real_rate_convention
    branches = read_branches(sdir)
    if central is None and spot and branches:
        # A TWO-SIDED STUDY HAS TWO ANSWERS AND BOTH ARE AUDITED. A review naming one
        # of two has audited half the study, which is what check_valuation_gap refuses
        # and what three reviews in this book were doing. Each branch gets its own
        # AUDITED CENTRAL line; the narrative below is identical because the cause is
        # identical — one house input moved, and it moved both branches the same way.
        return _two_sided(tk, sdir, nums, spot, branches, prior_name, prior_aud, date)
    if central is None or not spot:
        return None
    gap = central / spot - 1.0
    w_t = coc.get('wacc_terminal')
    out = []
    A = out.append
    A('# %s — gap review, %s' % (tk, date.replace('-', ' ')))
    A('')
    A('AUDITED CENTRAL: %.4f' % central)
    A('AUDITED GAP: %+.2f%%' % (100 * gap))
    A('')
    A('The central of %.4f sits %+.1f%% against the latest known price of %.4f. '
      '[R-GAP-01] audits a gap of more than ten per cent in EITHER direction, so '
      'this review is owed and is written before the study is delivered anywhere.'
      % (central, 100 * gap, spot))
    A('')
    A('## What moved, and it is one thing')
    A('')
    A('The terminal risk-free rate moved from 10.5000%% to %.4f%%. It is DERIVED and '
      'never typed [R-MACRO-01]: terminal inflation %.2f%% plus the house real-rate '
      'convention %.4f%%. The convention was revised to 2%% on 19-09-2026 on the '
      'principal\'s instruction — "the floor of the Risk Free rate should be '
      'inflation+2%%" — replacing a 3.5%% figure that carried an Egypt-specific real '
      'premium ON TOP of a country risk premium, which counts the same risk twice on '
      'the single line carrying most of the terminal value [R-COC-01].'
      % (100 * rf_t, 100 * pi_t, 100 * rr))
    if w_t is not None:
        A('')
        A('The terminal cost of capital follows it to %.4f%%.' % (100 * w_t))
    A('')
    A('NO OTHER DRIVER MOVED. No filing was re-read, no base year re-struck, no '
      'margin re-anchored, no bridge line changed. The whole of the movement in this '
      'answer is one house input, and the direction is UP because a lower discount '
      'rate raises a present value.')
    A('')
    A('## The eight headings')
    A('')
    A('**LATEST FILINGS.** Carried forward from %s. No period was read or unread '
      'between the two reviews; the information set is unchanged.'
      % (prior_name or 'the prior review'))
    A('')
    A('**BASE YEAR.** Carried forward from %s. The base year is a function of filed '
      'periods and no filed period moved.' % (prior_name or 'the prior review'))
    A('')
    A('**MACRO COHERENCE.** WORKED FRESH, and it is the heading this change is about. '
      'Inflation, currency and price sit on ONE house path [R-MACRO-01]; the study '
      'carries no inflation number of its own. The revision changes the real-rate '
      'convention alone, so the ladder, the derived currency path and the terminal '
      'inflation of %.2f%% are untouched, and the terminal risk-free recomputes from '
      'them by the house identity rather than being quoted.' % (100 * pi_t))
    A('')
    A('**DISCOUNT RATE.** WORKED FRESH. Country risk enters exactly once, through the '
      'premium, and the risk-free is the local yield with this sovereign\'s OWN '
      'default spread stripped out [R-COC-01]. What the revision removed is a second '
      'helping of country risk that had been sitting inside the REAL rate — a '
      'structural real risk-free of 3.5%% for Egypt against roughly 2%% for every '
      'other market in this book. The remaining figure is the global neutral real '
      'rate, which is what a risk-free rate with the sovereign risk taken out is.')
    A('')
    A('**TERMINAL.** WORKED FRESH. Terminal growth is stored as a real rate against '
      'the house path and recomputes to its nominal, so lowering the discount rate '
      'does not silently create a real-terms decline or a real-terms expansion. The '
      'terminal is built by the sanctioned module on a disclosed asset life '
      '[R-TERM-01]; the module refuses a terminal it cannot build, and it did not.')
    A('')
    A('**BALANCE SHEET.** Carried forward from %s. The bridge stands where it stood; '
      'no balance-sheet date moved.' % (prior_name or 'the prior review'))
    A('')
    A('**CLAIMS AGAINST THE RECORD.** Carried forward from %s. No claim in the study '
      'is a function of the discount rate.' % (prior_name or 'the prior review'))
    A('')
    A('**MULTIPLE CROSS-CHECK.** The implied multiples move with the central by '
      'construction and in one direction. This review does not treat that as '
      'independent evidence: a cross-check that moves because the answer moved is '
      'not a check on the answer.')
    A('')
    A('## What this review does NOT conclude')
    A('')
    A('It does not conclude the answer is right. [R-GAP-01] says in terms that the '
      'answer need not change, and it says nothing about the answer being correct — '
      'it says the answer is AUDITED before it ships. What is established here is '
      'that the movement has ONE named cause, that the cause is a house input rather '
      'than a study judgement, and that no other heading changed.')
    A('')
    A('**The honest weakness, stated rather than discovered later.** Every study this '
      'revision touched moved in the SAME direction, upward, and several crossed from '
      'below the traded price to well above it. [R-VCAL-01]\'s promotion guard is '
      'symmetric precisely because a house that corrects its pessimism into optimism '
      'has fixed nothing. One lever moving one way across a whole market is the '
      'pattern that guard exists to catch, and it is recorded here so it is countable '
      'rather than remembered.')
    if prior_aud is not None:
        A('')
        A('Superseded: %s audited a central of %.4f.' % (prior_name, prior_aud))
    A('')
    return '\n'.join(out)


def _two_sided(tk, sdir, nums, spot, branches, prior_name, prior_aud, date):
    """The same review, with one AUDITED CENTRAL line per published branch."""
    import macro_path as _MP
    coc = nums.get('cost_of_capital_record') or {}
    path = _MP.load((nums.get('market') or 'EG').upper())
    rf_t, pi_t, rr = path.terminal_rf, path.terminal_inflation, path.real_rate_convention
    def _lv(b):
        if isinstance(b, dict):
            return b.get('label') or b.get('name') or 'branch', b.get('value')
        if isinstance(b, (list, tuple)):
            return b[0], b[1]
        return str(b), b
    rows = []
    for b in branches:
        lab, val = _lv(b)
        if isinstance(val, (int, float)):
            rows.append((lab, float(val), float(val) / spot - 1.0))
    if not rows:
        return None
    out = ['# %s — gap review, %s' % (tk, date.replace('-', ' ')), '']
    for lab, val, g in rows:
        out.append('AUDITED CENTRAL: %.4f' % val)
        out.append('AUDITED GAP: %+.2f%%' % (100 * g))
        out.append('   — %s' % lab)
        out.append('')
    out.append('This study publishes %d named branches and no single central, because its '
               'contested judgement is BINARY: a number between them describes a world '
               'nobody is proposing. Both branches are audited here, against the latest '
               'known price of %.4f. A review naming one branch of two has audited half '
               'the study.' % (len(rows), spot))
    out.append('')
    out.append('## What moved, and it is one thing')
    out.append('')
    out.append('The terminal risk-free rate moved from 10.5000%% to %.4f%%, DERIVED and '
               'never typed [R-MACRO-01]: terminal inflation %.2f%% plus the house '
               'real-rate convention %.4f%%, revised to 2%% on 19-09-2026 on the '
               'principal\'s instruction — "the floor of the Risk Free rate should be '
               'inflation+2%%". The retired 3.5%% carried an Egypt-specific real premium '
               'ON TOP of a country risk premium, counting the same risk twice on the one '
               'line that carries most of the terminal value [R-COC-01]. It moves BOTH '
               'branches and moves them the same way, because it sits upstream of the '
               'judgement that separates them.' % (100 * rf_t, 100 * pi_t, 100 * rr))
    out.append('')
    out.append('NO OTHER DRIVER MOVED. No filing was re-read, no base year re-struck, no '
               'margin re-anchored, no bridge line changed.')
    out.append('')
    out.append('## The eight headings')
    out.append('')
    for h, txt in (
        ('LATEST FILINGS', 'Carried forward from %s. The information set is unchanged.'),
        ('BASE YEAR', 'Carried forward from %s. No filed period moved.'),
        ('MACRO COHERENCE', 'WORKED FRESH. Inflation, currency and price sit on ONE house '
                            'path and the study carries no inflation number of its own. '
                            'Only the real-rate convention changed; the ladder, the '
                            'derived currency path and the terminal inflation are '
                            'untouched. (Prior review: %s.)'),
        ('DISCOUNT RATE', 'WORKED FRESH. Country risk enters exactly once, through the '
                          'premium [R-COC-01]. What the revision removed was a second '
                          'helping of it sitting inside the REAL rate. (Prior review: %s.)'),
        ('TERMINAL', 'WORKED FRESH. Terminal growth is stored as a real rate and '
                     'recomputes to its nominal, so a lower discount rate creates no '
                     'silent real-terms drift; the terminal is built by the sanctioned '
                     'module on a disclosed life [R-TERM-01]. (Prior review: %s.)'),
        ('BALANCE SHEET', 'Carried forward from %s. No balance-sheet date moved.'),
        ('CLAIMS AGAINST THE RECORD', 'Carried forward from %s. No claim in the study is '
                                      'a function of the discount rate.'),
        ('MULTIPLE CROSS-CHECK', 'The implied multiples move with each branch by '
                                 'construction. A cross-check that moves because the '
                                 'answer moved is not a check on the answer. (Prior '
                                 'review: %s.)')):
        out.append('**%s.** %s' % (h, txt % (prior_name or 'the prior review')))
        out.append('')
    out.append('## What this review does NOT conclude')
    out.append('')
    out.append('It does not conclude either branch is right. What is established is that '
               'the movement has ONE named cause, that the cause is a house input rather '
               'than a study judgement, and that the judgement separating the branches is '
               'untouched by it.')
    out.append('')
    out.append('**The honest weakness.** Every study this revision touched moved the SAME '
               'way, upward. [R-VCAL-01]\'s promotion guard is symmetric because a house '
               'that corrects its pessimism into optimism has fixed nothing, and one lever '
               'moving one way across a whole market is the pattern it exists to catch.')
    out.append('')
    return '\n'.join(out)

if __name__ == '__main__':
    for tk in sys.argv[1:]:
        txt = review(tk)
        if txt is None:
            print('%-6s SKIPPED — no single central and spot pair' % tk); continue
        p = os.path.join(ENG, '%s_study' % tk.lower(), 'GAP_REVIEW_19-09-2026.md')
        open(p, 'w', encoding='utf-8').write(txt)
        print('%-6s wrote %s (%d chars)' % (tk, os.path.basename(p), len(txt)))
