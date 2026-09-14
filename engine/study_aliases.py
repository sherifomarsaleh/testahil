"""THE ONE TABLE SAYING WHICH STUDY DIRECTORY BELONGS TO WHICH TICKER.

Dependency-free ON PURPOSE. This is imported by engine/study_population.py, by
engine/campaign_queue.py and by scripts/check_published_coverage.py, and the last
of those runs inside a negative-control sandbox that builds a minimal tree — so a
module that pulls in node, assets/data.js or files/ cannot live here. Nothing in
this file imports anything.

WHY IT EXISTS AS A FILE RATHER THAN A CONSTANT IN ONE OF THEM. The fact was
written down in study_population.py and COPIED into campaign_queue.py, and the two
were compared only when study_population ran as a script. A consumer that imported
it got no check; a consumer that never imported it got no alias at all. That
consumer was check_published_coverage, which for three days listed FERTIGLB as
having no study while engine/fertiglobe_study sat on disk — and nothing could see
the staleness until a second measurement of the same fact disagreed.

A FACT HARDCODED IN ONE PLACE AND COPIED IN ANOTHER IS NOT HARDCODED, IT IS
DUPLICATED, and the copy is only as good as whatever compares them. So the copy is
removed rather than checked: there is one table, every consumer imports it, and
there is nothing left to drift.
"""

# study directory stem (upper-cased) -> the ticker the site carries
DIR_ALIAS = {
    'FERTIGLOBE': 'FERTIGLB',
}

# study directories that deliberately resolve to no covered equity, with reasons
NOT_AN_EQUITY = {
    'XPT': 'metals study — no issuer, no statements, no drivers',
}


def ticker_for(dir_stem):
    """The ticker a study directory stem belongs to."""
    t = dir_stem.upper()
    return DIR_ALIAS.get(t, t)
