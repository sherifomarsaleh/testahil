#!/usr/bin/env python3
"""PHAR walk-forward — the exogenous (macro) series, with four fields on every figure.

THESE ARE COUNTRY-RING FIGURES, NOT COMPANY HISTORICALS.  SIGCM clause 1 binds
the company's own reported numbers to its own filings and leaves the
Global/Country/Industry rings to credible institutional sources, which is what
these are.  Nothing here is a company figure.

TWO INFLATION LEGS, AND THEY ARE NOT THE SAME SERIES:

  KNOWABLE AT THE ORIGIN — the vintage print the origin could actually have
  read, carried out of engine/macro_history/EG.json, which this repository
  built for [R-VCAL-01] precisely so a rebuild does not reach for today's
  numbers.  THE ARCHIVE STOPS AT 2023.  The FY2024 origin therefore has NO
  knowable-inflation leg and is REPORTED AS UNMEASURED rather than filled from
  a later vintage — a figure right in value and wrong in date is invisible
  afterwards.

  REALISED (perfect foresight) — World Bank WDI FP.CPI.TOTL.ZG, calendar-year
  annual %, the same series and the same vintage macro_history already carries
  under `cpi_annual_current_vintage`, extended to 2024 and 2025.
"""
from __future__ import annotations

WDI_SOURCE = ("World Bank World Development Indicators, series FP.CPI.TOTL.ZG "
              "'Inflation, consumer prices (annual %)', Egypt, api.worldbank.org, "
              "series last updated 2026-07-13, retrieved 07-Sep-2026. Calendar year. "
              "THIS IS THE SERIES AS CURRENTLY REPORTED — a revised figure, right in "
              "value and wrong in vintage, which is why it is used ONLY for the "
              "perfect-foresight leg and never for the knowable-at-origin one.")

REALISED_CPI = {   # calendar year -> annual %, tier B (institutional), revision class ESTIMATED
    2016: 0.13813606, 2017: 0.29506608, 2018: 0.14401466, 2019: 0.09152800,
    2020: 0.05044933, 2021: 0.05214049, 2022: 0.13895661, 2023: 0.33884776,
    2024: 0.28270590, 2025: 0.14073514,
}

VINTAGE_CPI_SOURCE = ("engine/macro_history/EG.json, field `cpi_annual` — the print available "
                      "AT that origin, four-field and revision-classed by that archive's own "
                      "build. The archive's span is 2013-2023 and it stops there.")

VINTAGE_CPI = {    # origin year -> the annual inflation print knowable at that origin
    2019: 0.1387, 2020: 0.0586, 2021: 0.0450, 2022: 0.0850, 2023: 0.2352,
}
VINTAGE_CPI_UNAVAILABLE = {
    2024: "engine/macro_history/EG.json stops at the 2023 origin, so no point-in-time "
          "inflation print exists for a forecast struck at 31-Dec-2024. The leg is reported "
          "as UNMEASURED at this origin. It is NOT filled from a later vintage."
}

POP_SOURCE = ("World Bank World Development Indicators, series SP.POP.TOTL, Egypt, "
              "api.worldbank.org, series last updated 2026-07-13, retrieved 07-Sep-2026.")

POPULATION = {
    2014: 97528654, 2015: 99597342, 2016: 101644589, 2017: 103696057, 2018: 105682094,
    2019: 107553158, 2020: 109315124, 2021: 110957008, 2022: 112618250, 2023: 114535772,
    2024: 116538258, 2025: 118365995,
}


def population_growth(origin_year, k=3):
    """Trailing k-year compound population growth to the origin. EXOGENOUS ANCHOR.

    [R-FCAL-01] §3: volume is anchored on an exogenous market driver dated at the
    origin, never on the company's own trend alone. For a domestic generic
    manufacturer selling packs of medicine, the population it sells to is that
    driver; the company's own trend then supplies the share drift, inside a band.
    """
    a = POPULATION[origin_year - k]
    b = POPULATION[origin_year]
    return (b / a) ** (1.0 / k) - 1.0


def cpi_leg(leg, origin_year, forecast_year):
    """The escalator for one of the three pre-registered legs."""
    if leg == "knowable":
        v = VINTAGE_CPI.get(origin_year)
        return v            # None means UNMEASURED at this origin, by construction
    if leg == "foresight":
        return REALISED_CPI[forecast_year]
    raise ValueError("cpi_leg takes 'knowable' or 'foresight'; the baseline leg carries "
                     "no inflation term at all, which is what makes the split's own check "
                     "possible")


if __name__ == "__main__":
    print("Egypt, trailing 3-year population growth at each origin:")
    for y in range(2020, 2025):
        print("  %d  %.3f%%" % (y, 100 * population_growth(y)))
    print("\nknowable-at-origin CPI print:")
    for y in range(2020, 2025):
        v = VINTAGE_CPI.get(y)
        print("  %d  %s" % (y, ("%.2f%%" % (100 * v)) if v else "UNMEASURED — " +
                            VINTAGE_CPI_UNAVAILABLE[y][:60] + "..."))
    print("\nrealised calendar CPI:")
    for y in range(2020, 2026):
        print("  %d  %.2f%%" % (y, 100 * REALISED_CPI[y]))
