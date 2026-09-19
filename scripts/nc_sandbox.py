"""Which engine modules does a gate import? Read off the gate, never typed.

WHY THIS EXISTS. A negative control builds a sandbox carrying only what the gate it
exercises reads, and three controls each kept that list as typed filenames. A gate then
grew an import the list did not know about, and each of the three failed the same way:
the gate died on ModuleNotFoundError inside the sandbox before a single injected defect
reached it.

THE HALF THAT MAKES IT DANGEROUS. A control reads a dying gate as RED. So every case
that was supposed to go red went on reporting ok -- for the wrong reason -- while only
the CLEAN cases showed the failure. On check_forward_ranges that was nine cases passing
by crashing and three failing honestly. A control must never be able to pass by crashing
[R-ENF-04]; an empty result is not a clean result.

So the list is derived. A gate that grows an import gets it in its sandbox without
anyone remembering to add it.

WHAT THIS DOES NOT DO: it does not follow imports transitively, and it does not look
inside function bodies for conditional imports of engine modules. Both are deliberate --
the first because no engine module a gate imports currently has an engine dependency of
its own, and the second because a conditional import is a fixture decision the control
should make on purpose. If either stops being true the caller's own assertion catches
it, which is why every caller still asserts that the module it was BUILT around came
through.
"""
import io
import os
import re

_IMPORT = re.compile(r'^[ \t]*import[ \t]+([A-Za-z_][A-Za-z0-9_]*)', re.M)
_FROM = re.compile(r'^[ \t]*from[ \t]+([A-Za-z_][A-Za-z0-9_.]*)[ \t]+import[ \t]+(.+)$', re.M)


def engine_modules_imported_by(gate_path, engine_dir):
    """Every name in `engine_dir` that `gate_path` imports, by any of the three spellings.

    `import run_state`, `from engine import range_disclosure as RD`, and
    `from range_disclosure import X` all resolve to the same file on disk.
    """
    src = io.open(gate_path, encoding='utf-8').read()
    names = set(_IMPORT.findall(src))
    for mod, imported in _FROM.findall(src):
        if mod == 'engine':
            # `from engine import a, b as c` -- each name is its own module file
            for piece in imported.split('#')[0].split(','):
                piece = piece.strip().split(' as ')[0].strip().strip('()')
                if piece:
                    names.add(piece)
        else:
            names.add(mod.split('.')[0])
    return sorted(n for n in names
                  if os.path.exists(os.path.join(engine_dir, n + '.py')))


def copy_engine_modules(gate_path, engine_dir, dest, required=()):
    """Copy them into `dest` and assert the ones this control was built around arrived."""
    import shutil
    copied = engine_modules_imported_by(gate_path, engine_dir)
    for name in copied:
        shutil.copy(os.path.join(engine_dir, name + '.py'), dest)
    for need in required:
        assert need in copied, (
            'the gate no longer imports engine/%s.py, which this control was built '
            'around -- check the gate rather than widening this assertion. It imports: '
            '%s' % (need, ', '.join(copied) or 'nothing from engine'))
    return copied
