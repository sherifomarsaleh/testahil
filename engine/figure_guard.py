#!/usr/bin/env python3
"""A figure may not draw something outside its own axis and say nothing.

WHY THIS EXISTS. A study figure hardcoded its x-axis at 0 to 10.4 while the values it drew
ran 10.86 to 12.74 against a traded price of 13.50. Every bar was clipped at the axis edge
and they ALL RENDERED THE SAME LENGTH — 11.40 indistinguishable from 12.74 — and the price
line the caption's whole argument rested on ("not all of them together reaches the price")
was drawn outside the axis and thrown away, leaving a red label floating over no line. A
second figure in the same study hardcoded 2 to 11 against the same 13.50 and lost its price
line the same way.

NOTHING RAISED IN EITHER CASE. The code ran, the picture rendered, and it was wrong in a way
only a reader looking at it could see. That is the same defect the ticker-page overlay gate
was written for — "COMI's axis topped out at 148 against a freshly computed resistance of
160 and injectLevels drew a line at y=-21, outside the viewBox, silently" — arriving in a
study figure, where nothing was watching.

A HARDCODED AXIS LIMIT IS A NUMBER THAT STOPS BEING TRUE THE MOMENT THE MODEL MOVES. It is
not forbidden here: a percentage axis pinned to 0-100 is right, and so is a zoom that
deliberately crops. What is forbidden is cropping something the figure DREW, because the
figure then shows a reader less than it claims to.

HOW TO USE IT: `import figure_guard` at the top of a figures script, once. It wraps
Figure.savefig, so every figure that script saves is checked with no further change. Pass
figure_guard.allow(ax, 'why') to declare a deliberate crop; the reason is required, on the
same discipline as every other declared exception in this repository.
"""
import os

import matplotlib.figure
from matplotlib.transforms import BlendedGenericTransform

_ALLOWED = {}
_ORIG = matplotlib.figure.Figure.savefig
TOL = 1e-9

# A GATE MUST NOT REWRITE THE WORK IT IS CHECKING. Running a study's figure script to
# inspect what it draws would otherwise overwrite that study's committed PNGs, so the
# gate sets this and savefig checks the figure and returns without writing it.
DRY_RUN = os.environ.get('FIGURE_GUARD_DRY_RUN') == '1'
FINDINGS = []


def allow(ax, why):
    """Declare that this axes deliberately crops what it draws, and say why."""
    assert str(why).strip(), 'a declared crop with no reason is not a declaration'
    _ALLOWED[id(ax)] = why


def _refs(ax):
    """(axis, value) for every axvline/axhline on this axes.

    An axvline is a Line2D whose transform is BLENDED — data in x, axes fraction in y —
    which is exactly what distinguishes it from an ordinary two-point series.
    """
    out = []
    for ln in ax.lines:
        if not isinstance(ln.get_transform(), BlendedGenericTransform):
            continue
        xs, ys = list(ln.get_xdata()), list(ln.get_ydata())
        if len(xs) == 2 and xs[0] == xs[1] and ys == [0, 1]:
            out.append(('x', float(xs[0])))
        elif len(ys) == 2 and ys[0] == ys[1] and xs == [0, 1]:
            out.append(('y', float(ys[0])))
    return out


def _bars(ax):
    """(axis, value) for every bar's VALUE, on the axis that value is measured against.

    RE-POINTED [R-COC-01]. The first draft walked ax.patches and emitted BOTH the x and
    the y extent of every rectangle, letting the limit comparison decide which mattered.
    That is not a decision the comparison can make: a VERTICAL bar's x is a category
    index and has nothing to do with the value axis, so the check fired on ten scripts
    of twenty-six and most of those hits were the detector, not the figure. A check that
    cries wolf is one everybody learns to ignore.

    matplotlib records what the first draft was guessing: a BarContainer carries its
    ORIENTATION and its DATAVALUES. Read those instead of reverse-engineering rectangles,
    and a bar is compared only against the axis its value is drawn on. Bars outside a
    container (a hand-built patch) are not checked, which is honest: nothing says what
    axis they measure.
    """
    out = []
    for c in getattr(ax, 'containers', []):
        o = getattr(c, 'orientation', None)
        if o not in ('vertical', 'horizontal'):
            continue
        for p in getattr(c, 'patches', []):
            try:
                if o == 'horizontal':
                    a, b = float(p.get_x()), float(p.get_x() + p.get_width())
                    axis = 'x'
                else:
                    a, b = float(p.get_y()), float(p.get_y() + p.get_height())
                    axis = 'y'
            except (TypeError, ValueError):
                continue
            # BOTH EDGES, because a span bar drawn with left= can be clipped at either.
            # A second re-pointing: the first version of this compared the container's
            # DATAVALUES against the axis limits, and a datavalue is a MAGNITUDE measured
            # from the bar's base, not a position — so every football-field span bar,
            # drawn as barh(y, hi - lo, left=lo), was compared as though its width were a
            # coordinate. It fired on sixteen scripts of twenty-six.
            out.append((axis, a))
            out.append((axis, b))
    return out


def problems(fig):
    """Every reference line or bar edge this figure draws outside its own limits."""
    bad = []
    for i, ax in enumerate(fig.axes):
        if id(ax) in _ALLOWED:
            continue
        xlo, xhi = sorted(ax.get_xlim())
        ylo, yhi = sorted(ax.get_ylim())
        lim = {'x': (xlo, xhi), 'y': (ylo, yhi)}
        for kind, items in (('reference line', _refs(ax)), ('bar', _bars(ax))):
            for axis, v in items:
                lo, hi = lim[axis]
                if v < lo - TOL or v > hi + TOL:
                    bad.append('axes %d: a %s at %s=%.4g is outside the %s limits '
                               '(%.4g, %.4g)' % (i, kind, axis, v, axis, lo, hi))
    return bad


def _guarded(self, fname, *a, **k):
    bad = problems(self)
    if DRY_RUN:
        for b in bad:
            FINDINGS.append('%s: %s' % (os.path.basename(str(fname)), b))
        return None
    if bad:
        raise AssertionError(
            'FIGURE DRAWS OUTSIDE ITS OWN AXIS — %s:\n  - %s\n'
            'A clipped bar renders the same length as every other clipped bar, and a '
            'clipped reference line is simply not there while the caption says it is. '
            'Derive the limits from what is drawn, or declare the crop with '
            'figure_guard.allow(ax, why).'
            % (os.path.basename(str(fname)), '\n  - '.join(bad)))
    return _ORIG(self, fname, *a, **k)


matplotlib.figure.Figure.savefig = _guarded


def check_script(path):
    """Run a figures script under the guard and report what it drew outside its axes.

    Used by scripts/check_figure_axes.py so the guard can be applied from outside a study
    that has not yet imported it — the gate runs the instrument rather than counting the
    import, which is the difference between a green tick and a green result.
    """
    import runpy
    import sys
    d = os.path.dirname(os.path.abspath(path))
    sys.path.insert(0, d)
    cwd = os.getcwd()
    try:
        os.chdir(d)
        runpy.run_path(path, run_name='__figure_guard__')
    finally:
        os.chdir(cwd)
        if sys.path and sys.path[0] == d:
            sys.path.pop(0)
