# ORAS — two rulings taken before the build, 8 September 2026

marker: ruled_08_09_2026

Both questions below were put to the principal after the Step 2A sweep closed and BEFORE
any number depended on the answer. That order is the point: a sweep that closes without a
regressor and without a share count can ask, and a study that has already struck a beta
can only revise. Both were answered the same day and both answers are recorded here rather
than remembered.

## 1. Which exchange ORAS strikes on

**RULED: the EGX, against `engine/raw_indices/EG/EGX30.csv`.**

Orascom Construction is listed twice — ADX primary in AED (ISIN AEE01702O253) and EGX
secondary in EGP (ISIN EGS95001C011), the same ticker on both. On the sweep date the
company's own page header quoted both at once: EGP 855.85 and AED 60.30, 14.19x apart.

The series this repository holds, `engine/raw_ohlc/EG/ORAS.csv`, closes at 782.25 on
23 August 2026 — the EGP magnitude. So it is the EGX line, it is correctly filed under
EG, and EGX30 is its conforming regressor under SIGCM clause 6. No ADX series is
obtainable: `www.adx.ae` returns HTTP 403 and `api.adx.ae` fails the CONNECT tunnel at
502, both logged in the sweep.

**What the study must disclose, because the ruling does not make the awkwardness go away:**
ADX is the PRIMARY listing and the beta is measured on the secondary line. Two further
complications sit inside the regression window and the build carries both:

- **The ADX listing replaced Nasdaq Dubai inside the window.** The January-2025
  shareholding disclosure still names AEDFXA14NUL7. A window that spans the move spans two
  different secondary-market structures.
- **The pound itself moved**, from about 47.6 to about 52 to the dollar across the same
  window. A beta measured on an EGP series against an EGP index is internally consistent —
  but the company reports in dollars, and that is worth saying rather than leaving for a
  reader to notice.

## 2. How the OCI combination is framed

**RULED: DUAL-FRAME. Standalone and combined, side by side, neither blended into the other.**

The combination has NOT completed. The shareholders' circular of 8 January 2026 sets out
97,201,359 new shares at USD 1 plus USD 12.79 premium, taking issued capital from
110,243,935 to 207,445,294 — an increase of 88.2%. The ratio is 0.4634, ORAS equity value
USD 1,520.0mn against OCI USD 1,347.9mn, consideration about 47%. The long stop is
30 December 2026, the OCI vote is pending, and a rival all-cash NNS offer at EUR 4.10 is
outstanding.

So the terms are established and the outcome is not. The study is built on the standalone
company, and the combined case is carried as a fully separate valuation with its own share
count and its own drivers.

**NO PROBABILITY IS APPLIED TO THE OUTCOME.** A single number weighted between the two
share counts would be a view on a shareholder vote, and this house publishes fair-value
ranges and distributions rather than views on binary corporate events. A reader who holds
a view on the vote can take the frame that matches it; a reader who does not gets both.

## What is not settled by either ruling

The sweep left four things open and neither ruling touches them: FY2022 and FY2023
statement-of-financial-position pages are image-only and not yet read (FY2024's balance
sheet IS carried, as the FY2025 statement's comparative column); there is no cost of sales
by segment, so the one top-down margin allocation is flagged as such in the driver gate;
there are no project-level backlog values, no forward capex plan and no numeric FY2026
guidance, each closed by a dated negative search; and the FY2025 EBITDA carries a
USD 29.0mn legal-settlement gain that the normalisation base excludes.
