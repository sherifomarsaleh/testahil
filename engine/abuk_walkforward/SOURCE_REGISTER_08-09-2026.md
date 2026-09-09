# ABUK — primary-source index, 08-09-2026

Abu Qir Fertilizers and Chemical Industries Company (S.A.E.), EGX:ABUK.

## The company's own channel, and how it was found

**SIGCM clause 1 requires the company's own site FIRST, and the attempt logged either way.**
It was logged, and the first four attempts were WRONG HOSTNAMES rather than a site that
does not answer — the same shape as the GBCO record, where six recorded failures turned
out to be six wrong hosts.

| host tried | result | what it is |
|---|---|---|
| abuqirfert.com, www.abuqirfert.com, abuqir.com.eg, www.abuqir.com.eg | 000 | do not resolve |
| **abuqirfertilizers.com** | **200** | **THE FOOTBALL CLUB** — `fixtures`, `player-category/players`, `technical-staff`. A live host under a plausible name resolving to the WRONG SUBJECT, which is worse than a dead one |
| **abuqir.net** (abuqir.com redirects here) | **200** | **the company**, with an investor-relations section |

**A CONTROL WAS RUN BEFORE THE 000s WERE BELIEVED** and it is why they were not written
down as "the site is unreachable": github.com returned **400** through this container's
proxy, so a 000 here is evidence about the probe and not about the host [R-ENF-04].

## The fiscal-year break, which comes before any driver

**THE FISCAL YEAR MOVED FROM 30 JUNE TO 31 DECEMBER.** The shelf shows years ended
30-June-2024 and 30-June-2025, a TRANSITIONAL SIX-MONTH PERIOD ended 31-December-2024, and
then a full year ended 31-December-2025. Consequences to carry into the build rather than
discover later:

- a basis-break register precedes modelling [R-FCAL-01], and this is the break;
- the inflation mapping is NOT one of the closed list applied across the whole history —
  `fiscal_june` governs the years to June and `calendar` the years from December
  [R-MACRO-01 AMENDED], and the transitional half belongs to neither by itself;
- any year-on-year growth rate spanning the change compares a twelve-month period with a
  six-month one unless it is stated otherwise.

## Statements and releases held (URLs as published)

| period | statement | earnings release |
|---|---|---|
| 6M ended 30-Jun-2026 | /wp-content/uploads/2026/08/Financial-statements-30-6-2026.pdf | /wp-content/uploads/2026/08/Earnings-release-30-6-2026.pdf |
| 3M ended 31-Mar-2026 | /wp-content/uploads/2026/04/Abu-Qir-english-Q1-2026.pdf | /wp-content/uploads/2026/04/erning-release-march-2026.pdf |
| FY ended 31-Dec-2025 | /wp-content/uploads/2026/03/Abu-Qir-FS-as-of-31-12-2025-English-version.pdf | /wp-content/uploads/2026/02/ernings-release31-12-2025-.pdf |
| 3M ended 30-Sep-2025 | /wp-content/uploads/2025/11/Financial-statements-For-the-Three-Months-Period-Ended-September-30-2025.pdf | /wp-content/uploads/2025/11/Earnings-Release-for-the-financial-period-ended-30-09-2025.pdf |
| FY ended 30-Jun-2025 | /wp-content/uploads/2025/11/Financial-statements-for-the-year-ended-June-30-2025.pdf | /wp-content/uploads/2025/11/Earnings-Release-for-FY-ended-30-06-2025.pdf |
| 9M ended 31-Mar-2025 | /wp-content/uploads/2025/11/Financial-statements-For-the-Nine-Months-Period-Ended-Mars-31-2025.pdf | /wp-content/uploads/2025/11/Earnings-Release-for-the-financial-period-ended-31-03-2025.pdf |
| 6M ended 31-Dec-2024 (transitional) | /wp-content/uploads/2025/11/Financial-statements-For-the-Six-Months-Period-Ended-December-31-2024.pdf | /wp-content/uploads/2025/11/Earnings-Release-for-the-financial-period-ended-31-12-2024.pdf |
| 3M ended 30-Sep-2024 | /wp-content/uploads/2025/11/Financial-statements-for-the-three-months-period-ended-September-30-2024.pdf | /wp-content/uploads/2025/11/Earnings-Release-for-the-financial-period-ended-30-09-2024.pdf |
| FY ended 30-Jun-2024 | /wp-content/uploads/2025/11/Financial-statements-for-the-year-ended-June-30-2024.pdf | /wp-content/uploads/2025/11/Earnings-Release-FY-ended-30-6-2024.pdf |
| 9M ended 31-Mar-2024 | /wp-content/uploads/2025/11/Financial-statements-for-the-Nine-Months-Period-Ended-March-31-2024.pdf | /wp-content/uploads/2025/11/Earnings-Release-for-the-financial-period-ended-31-3-2024.pdf |
| 6M ended 31-Dec-2023 | /wp-content/uploads/2025/11/Financial-statements-For-the-Six-Months-Period-Ended-December-31-2023.pdf | /wp-content/uploads/2025/11/Earnings-Release-for-the-six-months-ended-31-12-2023.pdf |
| 3M ended 30-Sep-2023 | /wp-content/uploads/2025/11/Financial-Statements-for-the-three-months-period-ended-September-30-2023-and-Auditors-Review-Reports.pdf | /wp-content/uploads/2025/11/Earnings-Release-for-the-three-months-ended-September-30-2023.pdf |

All under `https://abuqir.net`. **NOTHING HERE HAS BEEN DOWNLOADED, PARSED OR USED YET** —
this is the located shelf, not the evidence, and every figure still owes its four fields
and its arithmetic check [R-SIGCM-03 clause iv].

## Fair-value baseline

Frozen before any work: **bear 50 / base 60 / full 72 EGP**, built to no current-standard
study, so the movement column at the end measures against a number of unknown provenance
and must say so wherever it is quoted.

## The six-month period, which the company's own website labels as a year

**THE PERIOD ENDED 31 DECEMBER 2025 IS SIX MONTHS, NOT TWELVE.** The statements say so in
terms — *"for the six months from July 1 till December 31, 2025"* and *"period from
01/07/2025 to 31/12/2025"* — while the investor-relations page lists that same file under
**"Q4 (Year ended December 31, 2025)"**.

A build taking the website's label at face value books **EGP 13,131,643,463** as a full
year when it is half of one, understating the base year by about a factor of two and
compounding that through every forecast year and the terminal. This is [R-GAP-01]'s BASE
YEAR heading — anything annualised, scaled or solved is named as such — caught before a
driver was set rather than found in the error afterwards.

## Text layer and route

**The text layer is 50 characters across 50 pages**, i.e. empty — the SCEM and ARCC shape
exactly. Every figure below was read by **OCR off the rendered pixels** (pdftoppm 200dpi,
tesseract 5.3.4 eng, `--psm 6`), and the disputed column re-rendered at 400dpi and re-read.

## Arithmetic, which is the arbiter

Individual statement of financial position, 31-Dec-2025 (EGP):

| total | computed from printed rows | stated | result |
|---|---:|---:|---|
| non-current assets | 8,716,933,927 | 8,716,933,928 | **out by 1** |
| current assets | 23,888,244,441 | 23,888,244,441 | foots |
| total assets | 32,605,178,369 | 32,605,178,370 | out by 1, inherited |
| total equity | 23,241,840,301 | 23,241,840,301 | foots |

**The 1 EGP is the filing's own, not the OCR's.** Both comparative columns — 30-Jun-2025
and 1-Jul-2024 — foot EXACTLY on the same OCR pass, and every line of the December column
re-read identically at 400dpi. Recorded rather than repaired; immaterial to a valuation and
exactly the kind of thing that gets silently absorbed.

## Why this is a PENDING directory and carries no frozen baseline

A baseline was frozen here and **removed as premature**. `fv_movement.py check` anchors on
run directories and refuses a record with no run behind it, symmetrically — which is the
gate correctly saying a name cannot be started halfway. EMFD is the precedent: substantial
work in a `_walkforward_pending` directory and no register entry until the run is real.

**The removal is provably lossless**: `assets/data.js` still carries ABUK at
`bear 50 / base 60 / full 72`, identical to what was frozen, so nothing this campaign could
have moved has moved, and the baseline captured when the run genuinely starts will read the
same three numbers. It carried no editions.
