#!/usr/bin/env python3
"""CI gate for the campaign's parked names.  [R-CAMP-01]

A park is the campaign's fourth outcome, beside FULL / LIGHT / SKIP: the
company published the years and this container cannot reach them.  It exists so
that an unreachable host does not become the sentence "walk-forward not run --
insufficient sourceable history", which would be a fact about the network
wearing the costume of a fact about the company [R-ENF-04].

Being an outcome that no other gate can see, it needs one of its own.  The two
campaign gates anchor on engine/*_walkforward/ directories, and a parked name
deliberately has none -- so without this check a park is invisible to every
automated job in the repository, and "we are waiting on documents" would decay
into "nobody looked" with nothing able to tell the difference.

What it enforces, none of it self-attested:
  * every parked name is really in the queue, and is not also excluded;
  * every logged attempt carries its OUTCOME, not just a URL -- the rule is log
    the attempt AND its outcome, and a bare URL list is an assertion;
  * every park names the exact documents needed and the condition that releases
    it, so the block is actionable by someone other than its author;
  * no parked name carries a run directory or a frozen fair-value baseline,
    either of which would turn the two campaign gates red for a run that is not
    happening -- and a permanently red check is one everyone learns to ignore.

Negative-controlled by scripts/check_campaign_parked_negative_control.py.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))

import campaign_parked  # noqa: E402

if __name__ == '__main__':
    print('campaign parked-names gate [R-CAMP-01]')
    rc = campaign_parked.check()
    print('parked register OK' if rc == 0 else 'parked register FAILED')
    raise SystemExit(rc)
