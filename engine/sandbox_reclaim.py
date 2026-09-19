"""Reclaim sandbox copies left behind by a harness that did not finish.

ADOPTED 18-09-2026 ON A MEASURED FAILURE. Two harnesses copy the whole repository
into a temporary directory — the new-study gauntlet and the error-injection
catalogue — and each removes its copy in a `finally`. That is correct exactly as
often as the process completes, which is this book's own general lesson about an
undo that runs last: a kill, a timeout, or an out-of-space error skips it.

WHAT IT COST, measured rather than argued: twenty-five abandoned copies at 1.4 to
1.6 GB each filled the session's whole disk allowance, and EVERY GATE IN THE
REPOSITORY THEN WENT RED WITH AN EMPTY MESSAGE, because each one's output could not
be written. A sweep of 172 checks reported a catastrophe that did not exist. An
infrastructure failure wearing a repository failure's clothes is worse than either,
because the first thing it costs is the reader's belief that anything is working.

THE FIX IS TO RECLAIM AT THE START RATHER THAN ONLY AT THE END. A process that died
cannot clean up after itself; the next one can. The test is EXACT and carries no
threshold: each sandbox records the process that made it, and a sandbox whose
process is gone is finished with, whatever its age. An age cutoff would be the free
parameter the PROMOTION RULE forbids and would be wrong in both directions — it
would delete a long run's live sandbox and keep a short run's dead one.

IT NEVER TOUCHES A LIVE SANDBOX, including its own: a directory whose recorded
process is still running is left alone, and one with no stamp at all is left alone
too, because an unstamped directory is one this module did not make and guessing
about it is how a cleanup deletes somebody's work.
"""
from __future__ import annotations

import glob
import os
import shutil
import tempfile

STAMP = ".sandbox_owner"


def stamp(path: str) -> None:
    """Record the making process inside a sandbox, so a later run can tell."""
    try:
        with open(os.path.join(path, STAMP), "w", encoding="utf-8") as fh:
            fh.write("%d\n" % os.getpid())
    except OSError:
        # A sandbox that cannot be stamped is simply not reclaimable by this route.
        # It is NOT an error: the harness's own `finally` still removes it on a
        # normal exit, and refusing to run over a stamp is a worse failure than
        # leaving one directory behind.
        pass


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True          # it exists and belongs to somebody else
    except OSError:
        return True          # unreadable is not the same as absent [R-ENF-04]
    return True


def reclaim(prefix: str, root: str = None) -> list:
    """Remove sandboxes with this prefix whose making process is gone.

    Returns the paths removed, so a caller can SAY what it reclaimed rather than
    doing it silently — a cleanup nobody can see is one nobody can audit.
    """
    root = root or tempfile.gettempdir()
    gone = []
    for p in sorted(glob.glob(os.path.join(root, prefix + "*"))):
        if not os.path.isdir(p):
            continue
        s = os.path.join(p, STAMP)
        if not os.path.exists(s):
            continue                      # not ours to judge
        try:
            pid = int(open(s, encoding="utf-8").read().strip() or "0")
        except (OSError, ValueError):
            continue
        if pid <= 0 or _alive(pid):
            continue
        shutil.rmtree(p, ignore_errors=True)
        gone.append(p)
    return gone


def make(prefix: str) -> str:
    """Reclaim first, then make a stamped sandbox. The order is the whole point."""
    reclaim(prefix)
    d = tempfile.mkdtemp(prefix=prefix)
    stamp(d)
    return d


if __name__ == "__main__":
    import sys
    pre = sys.argv[1] if len(sys.argv) > 1 else "gauntlet_"
    got = reclaim(pre)
    print("reclaimed %d abandoned sandbox(es) with prefix %r" % (len(got), pre))
    for p in got:
        print("  " + p)
    if not got:
        print("  none — every sandbox with that prefix either has a live process "
              "or carries no owner stamp, and neither is this module's to remove.")
