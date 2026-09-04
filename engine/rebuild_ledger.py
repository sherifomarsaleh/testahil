#!/usr/bin/env python3
"""A REBUILD IS A SEQUENCE OF LEVERS AND THE SEQUENCE IS THE THING NOBODY WATCHES.

    from engine import rebuild_ledger as RL

WHY THIS EXISTS. [R-VCAL-01]'s promotion guard governs levers promoted FROM the
valuation calibration: one at a time, in an order fixed before any score exists, halted
the moment the stacked bias would cross zero. It was written against a named failure —
"the guard against stacking five individually-justified moves into an overshoot, the
exact failure that called this reassessment".

NOTHING GOVERNED THE SAME THING IN A REBUILD, and a rebuild applies rules that ALREADY
bind rather than levers seeking promotion, so the guard was never read as covering it.
On 4 September 2026 one study took SIX corrections in an afternoon — a sanctioned
terminal on a disclosed asset life, growth stored as a real rate, the house inflation
ladder, a derived currency path, a derived terminal risk-free rate, a retired lens
blend — and moved from 55% below the market price to 71% below it. Every correction was
required. Every one was right. Nobody looked at the running total until the last one was
in, and by then the answer had passed through +45% and back down through -56%.

WHAT THIS RECORDS, AND THE THIRD FIELD IS THE ONE THAT MATTERS:

  1. THE LEVERS IN THE ORDER APPLIED, each with the answer before and after. A rebuild
     that applies six corrections and reports one number has published a result nobody
     can decompose, including its author a week later.
  2. THE RUNNING TOTAL, so the stack is visible WHILE it is built rather than after.
  3. WHICH RULE EACH LEVER SERVES — because SEVERAL LEVERS SERVING ONE RULE ARE ONE
     PIECE OF EVIDENCE, NOT SEVERAL. Three of that study's six corrections were the
     house macro path applied in three places (the inflation ladder, the currency
     derived from it, and the terminal risk-free derived from it), and between them they
     took 56% off a value the terminal correction had just raised by 45%. Counting them
     as three independent confirmations that the study was too high would have been
     counting one rule three times.

WHAT IT DELIBERATELY DOES NOT DO. It sets no threshold and blocks nothing. A large
cumulative move is not evidence of error — a study wrong in six ways moves a long way
when all six are fixed, and that is the process working. What it forbids is the move
being INVISIBLE. [R-GAP-01] already audits the ANSWER; this records the ROUTE, and the
two answer different questions: whether the destination is credible, and whether anyone
watched the journey.

THE AUDIT POINT IS DECLARED, NOT DERIVED. A rebuild states in advance where it will
stop and look — after the levers serving one rule are complete is the natural place, and
it is the place that would have caught the case above. A number chosen here would be a
free parameter and the promotion rule forbids one.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List, Optional


class RebuildRefused(Exception):
    """A ledger that cannot be read as a sequence. It raises; it never warns."""


@dataclass
class Lever:
    """One correction, with the answer either side of it."""
    name: str
    rule: str                      # the standing rule it serves — the grouping key
    before: float
    after: float
    why: str = ''
    evidence: str = ''

    @property
    def move(self) -> float:
        if not self.before:
            return float('nan')
        return self.after / self.before - 1.0


@dataclass
class Ledger:
    ticker: str
    started_at: str                # the answer this rebuild began from
    start_value: float
    start_spot: float
    audit_after: str = ''          # the lever after which this rebuild will stop and look
    levers: List[Lever] = field(default_factory=list)

    # ---------------------------------------------------------------- building
    def apply(self, name: str, rule: str, after: float, why: str = '',
              evidence: str = '') -> Lever:
        """Record a lever. `after` is the answer once it is in."""
        before = self.levers[-1].after if self.levers else self.start_value
        lv = Lever(name=name, rule=rule, before=before, after=after, why=why,
                   evidence=evidence)
        self.levers.append(lv)
        return lv

    # ---------------------------------------------------------------- reading
    @property
    def value(self) -> float:
        return self.levers[-1].after if self.levers else self.start_value

    @property
    def cumulative(self) -> float:
        if not self.start_value:
            return float('nan')
        return self.value / self.start_value - 1.0

    def by_rule(self) -> dict:
        """The net move each RULE is responsible for, levers of one rule combined.

        THE POINT OF THE WHOLE MODULE. A rule applied in three places moved the answer
        once, not three times, and a decomposition that lists six levers where three
        rules are at work invites reading three coincidences into one correction.
        """
        out = {}
        for lv in self.levers:
            g = out.setdefault(lv.rule, {'levers': [], 'first_before': lv.before,
                                         'last_after': lv.after})
            g['levers'].append(lv.name)
            g['last_after'] = lv.after
        for g in out.values():
            g['move'] = (g['last_after'] / g['first_before'] - 1.0
                         if g['first_before'] else float('nan'))
        return out

    def record(self) -> dict:
        """The committed form. Everything a reader needs to redo the decomposition."""
        rules = self.by_rule()
        return {
            'ticker': self.ticker,
            'started_at': self.started_at,
            'start_value': self.start_value,
            'start_spot': self.start_spot,
            'start_gap': (self.start_value / self.start_spot - 1.0
                          if self.start_spot else None),
            'audit_after': self.audit_after,
            'levers': [asdict(lv) | {'move': lv.move} for lv in self.levers],
            'value': self.value,
            'cumulative_move': self.cumulative,
            'rules': rules,
            'distinct_rules': len(rules),
            'note': ('Several levers serving ONE rule are one piece of evidence, not '
                     'several. `rules` combines them; `levers` keeps the order they were '
                     'applied in so the route can be walked.'),
        }


# ---------------------------------------------------------------------- checking
REQUIRED = ('ticker', 'start_value', 'start_spot', 'levers', 'value', 'cumulative_move',
            'rules', 'audit_after')


def assert_rebuild(record: dict, ticker: str = '?') -> dict:
    """Raise unless a rebuild's own ledger can be walked from start to answer.

    Four refusals, none of them a threshold:

      * a missing field — a ledger that does not say where it started cannot say how
        far it went;
      * a BROKEN CHAIN — each lever's `before` must be the previous one's `after`, or
        the sequence is a list of measurements rather than a route, and the running
        total means nothing;
      * a lever naming no rule, because the rule is the grouping key and an ungrouped
        lever silently becomes its own piece of evidence;
      * NO DECLARED AUDIT POINT on a rebuild carrying more than one lever. One lever
        needs no plan; a sequence does, and the plan is what makes stopping to look a
        decision rather than an afterthought.
    """
    fails = []
    r = record or {}
    for f in REQUIRED:
        if f not in r:
            fails.append('the ledger states no %r' % f)
    if fails:
        raise RebuildRefused('REBUILD LEDGER FAIL — %s:\n  - %s'
                             % (ticker, '\n  - '.join(fails)))

    levers = r.get('levers') or []
    if not levers:
        fails.append('the ledger records no lever at all. A rebuild that changed '
                     'nothing is not a rebuild, and one that changed something without '
                     'recording it is the state this module exists to end.')
    prev = r.get('start_value')
    for i, lv in enumerate(levers):
        for f in ('name', 'rule', 'before', 'after'):
            if lv.get(f) in (None, ''):
                fails.append('lever %d states no %r' % (i + 1, f))
        b = lv.get('before')
        if isinstance(b, (int, float)) and isinstance(prev, (int, float)):
            if abs(b - prev) > max(1e-9, abs(prev) * 1e-9):
                fails.append(
                    'lever %d (%r) starts from %.6f and the one before it ended at '
                    '%.6f. The chain is broken, so the running total is not a running '
                    'total.' % (i + 1, lv.get('name'), b, prev))
        prev = lv.get('after')
    if isinstance(prev, (int, float)) and isinstance(r.get('value'), (int, float)):
        if abs(prev - r['value']) > max(1e-9, abs(prev) * 1e-9):
            fails.append('the last lever ends at %.6f and the ledger publishes %.6f'
                         % (prev, r['value']))
    if len(levers) > 1 and not str(r.get('audit_after') or '').strip():
        fails.append(
            'a rebuild of %d levers declares no audit point. Where the stack is looked '
            'at is a decision, and a decision nobody wrote down was not made.'
            % len(levers))

    if fails:
        raise RebuildRefused('REBUILD LEDGER FAIL — %s:\n  - %s'
                             % (ticker, '\n  - '.join(fails)))
    return r


def render(record: dict) -> str:
    """The table a reader actually wants, levers in order and rules combined."""
    r = record
    out = ['REBUILD LEDGER — %s' % r['ticker'],
           '   started at %.4f against a spot of %.4f (%+.1f%%)'
           % (r['start_value'], r['start_spot'], 100 * (r['start_gap'] or 0)),
           '']
    out.append('  %-52s %10s %10s %8s' % ('lever', 'before', 'after', 'move'))
    out.append('  ' + '-' * 84)
    for lv in r['levers']:
        out.append('  %-52s %10.4f %10.4f %+7.1f%%'
                   % (lv['name'][:52], lv['before'], lv['after'], 100 * lv['move']))
    out.append('  ' + '-' * 84)
    out.append('  %-52s %10.4f %10.4f %+7.1f%%'
               % ('CUMULATIVE', r['start_value'], r['value'],
                  100 * r['cumulative_move']))
    out += ['', '  BY RULE — several levers serving one rule are ONE piece of evidence:']
    for rule, g in sorted(r['rules'].items(), key=lambda kv: -abs(kv[1]['move'])):
        out.append('  %-24s %+7.1f%%   %d lever(s): %s'
                   % (rule, 100 * g['move'], len(g['levers']), ', '.join(g['levers'])))
    out += ['', '  audit point declared: %s' % (r['audit_after'] or '(none)')]
    return '\n'.join(out)
