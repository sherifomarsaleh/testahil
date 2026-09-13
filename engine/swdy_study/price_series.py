"""THE PRICE FRAME OF THIS STUDY, READ IN ONE PLACE.

Four files read the price series independently -- strike_swdy.py, figures.py,
docx_swdy.py's section 2 and backtest_5y.py -- and all four read the study-local
SWDY_Stock_Price_History.csv. That file ends 5 August 2026 at 105.20, and this
study's own compute.py records why it cannot be trusted: the supplied spot arrived
as 90.50 and was CORRECTED to 130.00 on 6 September 2026 after it disagreed with
this name's price library on all 35 overlapping sessions after 14 June 2026,
including that 5 August close. The study acted on the finding for its SPOT and left
every price picture reading the discredited file.

So section 2 printed moving averages of 93.77 / 90.04 / 86.07 / 81.88 and a 52-week
closing high of 109.02 under a row reading "Last close 130.00", the cone opened at
105.20 under a line labelled "spot 130.00", and a printed "probability above spot"
of 56% was the probability above 105.20 -- against the 130.00 the study publishes it
is 5.7%.

Two rules, enforced here rather than remembered in four places:

  THE LIBRARY IS THE SOURCE. engine/raw_ohlc/EG/SWDY.csv is what every other name in
  this book strikes on, and a study-local copy of a price series is exactly the
  divergence SIGCM exists to stop.

  THE SERIES STOPS ON THE VALUATION DATE. Not on whatever row the library happens to
  end on. The fair value is measured against one price on one day; a cone struck
  three sessions later, or a moving-average stack running a week past the anchor,
  describes a different price and the page gives the reader no way to see it.

And it REFUSES rather than returning something plausible: if the library holds no
row for the study's valuation date, or its close on that date is not the spot the
study publishes, one of the two is wrong and neither may be assumed.
"""
import json as _json
import os as _os
import sys as _sys

_HERE = _os.path.dirname(_os.path.abspath(__file__))
if _os.path.join(_HERE, '..') not in _sys.path:
    _sys.path.insert(0, _os.path.join(_HERE, '..'))

LIBRARY = _os.path.join(_HERE, '..', 'raw_ohlc', 'EG', 'SWDY.csv')


def asof_and_spot():
    """The study's own valuation date and the price it is measured against."""
    with open(_os.path.join(_HERE, 'study_numbers.json')) as f:
        m = _json.load(f)['meta']
    return m['asof'], float(m['spot'])


def raw():
    """The library as loaded, cut at the valuation date. Pre-clean, for Step 0.0's
    own raw-row count -- a gate that counts rows after a clean it has not run yet
    is counting the wrong thing."""
    import pandas as pd
    from primitives import load_ohlc
    df = load_ohlc(LIBRARY).reset_index(drop=True)
    a, _ = asof_and_spot()
    return df[pd.to_datetime(df['Date']) <= pd.Timestamp(a)].reset_index(drop=True)


def frame(verbose=False):
    """The cleaned series, cut at the valuation date, with its last close ASSERTED
    against the spot the study publishes. Returns (df, clean_report)."""
    import pandas as pd
    from primitives import load_ohlc
    from data_quality import clean_ohlc
    df, rep = clean_ohlc(load_ohlc(LIBRARY), 'SWDY', verbose=verbose, market='EG')
    df = df.reset_index(drop=True)
    a, spot = asof_and_spot()
    df = df[pd.to_datetime(df['Date']) <= pd.Timestamp(a)].reset_index(drop=True)
    if not len(df):
        raise SystemExit('the price library carries no session at or before the '
                         "study's valuation date of %s" % a)
    last = pd.Timestamp(df['Date'].iloc[-1])
    if last != pd.Timestamp(a):
        raise SystemExit('the price library has no row for %s (its last session at '
                         'or before it is %s); the price picture cannot be drawn on '
                         'the day the value is measured'
                         % (a, last.date()))
    close = float(df['Price'].iloc[-1])
    if abs(close - spot) > 0.005:
        raise SystemExit('the library closes at %.4f on %s and the study publishes a '
                         'spot of %.4f; one of the two is wrong and neither may be '
                         'assumed' % (close, a, spot))
    return df, rep
