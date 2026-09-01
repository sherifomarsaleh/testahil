"""What TMG's own documents disclose, and whether this model uses it.

The standing rule says to ask, before declaring a self-audit complete, WHAT THE
FILINGS DISCLOSE THAT THE MODEL DOES NOT CONSUME. Nothing enforced it, so on
this study it was never asked, and two of the biggest items on the company's own
summary page went straight past: a 20mn sqm landbank valued at zero, and a hotel
estate going from c.3,500 keys to c.5,000 by 2028 that earned nothing because
hospitality grew at inflation. Both were on ONE PAGE of ONE document this study
had already downloaded, read and cited.

Every disclosed operating fact is listed here and is either CONSUMED, naming the
driver that uses it, or DECLINED, with a reason. Silence is not available,
because silence is exactly what happened.
"""

DISCLOSED = {
    # ---- consumed -------------------------------------------------------
    "contracted order book, EGP 491.0bn at 30 Jun 2026": {
        "consumed": "model.project() — the opening backlog the deliveries work off"},
    "contracted sales by year, FY2011-FY2025": {
        "consumed": "the balancing item that holds the book at cover, and the "
                    "walk-forward's D1 driver"},
    "development revenue and cost, by period": {
        "consumed": "gross margin gm_dev_h1_26, anchored on the reviewed half-year"},
    "hospitality revenue and cost, by period": {
        "consumed": "gm_hosp_h1_26 and the hospitality leg"},
    "other recurring revenue and cost, by period": {
        "consumed": "gm_other_h1_26 and the other recurring leg"},
    "hotel keys: c.3,500 operating, c.1,500 under construction, "
    "c.5,000 by 2028": {
        "consumed": "HOSP_KEYS_NOW / HOSP_KEYS_TARGET / HOSP_KEYS_COMPLETE_BY — "
                    "revenue per key flat in real terms, the keys carry the "
                    "growth. ADDED 01-Sep-2026 after this register was written; "
                    "before that hospitality grew at inflation only and the "
                    "expansion earned nothing."},
    "landbank 20mn sqm": {
        "consumed": "rnav.py — the asset lens the class requires. ADDED "
                    "01-Sep-2026; before that the DCF credited land at zero "
                    "beyond its own window."},
    "customer advances, EGP 133,993.1mn at 30 Jun 2026": {
        "consumed": "ADV_COVER_ON_PUD, against work in progress"},
    "properties under development, EGP 148,315.4mn": {
        "consumed": "PUD_COVER_YEARS and the build-spend stock adjustment"},
    "borrowings, leases, cash and deposits": {
        "consumed": "the EV-to-equity bridge and the finance charge"},
    "non-controlling interests, 45.2% of equity": {
        "consumed": "the bridge, deducted at book AND proportionally"},
    "investment property, associates, FVOCI": {
        "consumed": "added at book in the bridge"},
    "post-dated cheques, EGP 210,448.8mn off balance sheet": {
        "consumed": "quoted in the collections discussion as evidence that "
                    "off-plan growth is self-funding"},
    "shares outstanding": {"consumed": "per-share arithmetic"},
    "delivery history FY2019-FY2025": {
        "consumed": "DELIVERY_REAL_RECOVERY, the company's own 28.5% nominal / "
                    "7.1% real compound rate"},

    # ---- declined, with the reason --------------------------------------
    "units sold and units delivered, by year": {
        "declined": "the two series are not on one basis across the window and "
                    "the unit counts stop before the statements do; the model "
                    "runs on value, not counts, and says so [L-118]"},
    "Saudi (Banan) project": {
        "declined": "no separate revenue, cost, land or schedule is disclosed "
                    "for it; it sits inside the consolidated development leg "
                    "and is registered as a gap rather than modelled"},
    "hotel keys by property and by brand": {
        "declined": "the release gives the group total only; a per-property "
                    "build would need occupancy and rate by asset, which is "
                    "not published"},
    "42.4 feddan Sharm expansion": {
        "declined": "an area with no capital cost, opening economics or key "
                    "count of its own; it is inside the c.1,500 under "
                    "construction already consumed above"},
    "land carrying value, and landbank by project": {
        "declined": "NOT DISCLOSED AT ALL — the release's project pages are "
                    "scanned graphics carrying no land figures. This is why "
                    "the RNAV publishes a stated upper bound and reverse-solves "
                    "the market rather than a value"},
    "finance cost split between interest and other charges": {
        "declined": "the note gives one figure; registered as a gap, and the "
                    "reason the finance-cost correction was blocked [L-044]"},
    "capital expenditure by segment": {
        "declined": "disclosed in total only; hospitality and other recurring "
                    "carry stated capex ratios with the gap noted"},
    "unit areas, price per sqm, cost per sqm": {
        "declined": "no continuous series is published, which is why the build "
                    "is at SEGMENT level and not unit level, flagged on every "
                    "line under [R-SIGCM-02]"},
}
