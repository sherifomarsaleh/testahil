#!/usr/bin/env python3
"""[R-REPAIR-01] A COMMITTED RECORD MUST SURVIVE ITS OWN REBUILD.

Several studies build study_numbers.json in more than one step: a primary generator
(compute.py, build_numbers.py) writes the valuation, and later steps append records other
gates require — the asset-base vintage [R-ASSET-01], the cost-of-capital reproduction
[R-COC-02], the EV-to-equity bridge, the information-set date.

EVERY ONE OF THOSE PRIMARY GENERATORS ENDED IN json.dump(OUT, f), WHICH IS A WHOLESALE
OVERWRITE. Re-run the primary alone and the later steps' records are gone — silently, with
the generator reporting success, and with the study still passing every gate that reads the
file until something rebuilds it. check_record_survives_rebuild.py found five studies in
exactly that state: AMOC, PHAR, PHDC, SWDY and TMGH, losing between one and two records
each.

Its own message names the remedy: "Write it in the generator; a repair that does not survive
a rebuild is not a repair."

WHY THE CARRIED SET IS CLOSED AND NOT A BLANKET MERGE. Preserving every unknown key would
fix this failure and create a worse one: a record deleted on purpose, or renamed, would live
in the artefact forever with nothing able to remove it, and a stale key would be
indistinguishable from a current one. So the keys carried are named here, each owned by a
step that runs after the primary. A key not on this list is not preserved, which is the
same discipline every ratchet in this repository runs on.
"""
import json
import os

# key -> the step that owns it. Named, never patterned.
DOWNSTREAM_OWNED = {
    'asset_base_record':      'asset_base_record.py — [R-ASSET-01]',
    'information_set_ends':   'asset_base_record.py — [R-ASSET-01]',
    'bridge_record':          'forecast_anchor.py / the bridge step',
    'cost_of_capital_record': 'forecast_anchor.py — [R-COC-02]',
}


def write_preserving(path, out, owned=None):
    """Write `out` to `path`, carrying forward downstream-owned records already there.

    Returns the list of keys carried, so a generator can SAY it carried them rather
    than doing it silently — a preserved record nobody mentions is how the next
    person concludes the primary generator writes it.
    """
    owned = DOWNSTREAM_OWNED if owned is None else owned
    carried = []
    if os.path.exists(path):
        try:
            with open(path) as fh:
                prior = json.load(fh)
        except (OSError, ValueError):
            # [R-ENF-04] — an unreadable prior file is not an absent one. Refuse
            # rather than overwrite a file that may hold records we cannot see.
            raise RuntimeError(
                '%s exists and will not parse. Refusing to overwrite it: an '
                'unreadable file is not an empty one, and a record that cannot be '
                'read is exactly the record most likely to be lost.' % path)
        if isinstance(prior, dict):
            for k in owned:
                if k in prior and k not in out:
                    out[k] = prior[k]
                    carried.append(k)
    with open(path, 'w') as fh:
        json.dump(out, fh, indent=1)
    return carried
