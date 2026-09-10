# EGCH — valuation gap review, 10 September 2026  [R-GAP-01]

**The answer is TWO-SIDED and both branches breach the ten per cent trigger below the
price. Both are audited.**

- AUDITED CENTRAL: 5.0224  (EGP per share — cash-flow lens, ANNA capital programme carried through)
- AUDITED CENTRAL: 9.1288  (EGP per share — cash-flow lens, ANNA capital programme stopped)
- AUDITED SPOT: **EGP 14.23**, the close of 6 September 2026, the latest price this
  repository holds. The study is struck at EGP 14.41, the supplied close of 3 September;
  both are published and no heading answers differently against one than the other.
- AUDITED GAP: −64.7%   (carried through; the stopped branch is −35.8%)

**A TWO-SIDED ANSWER IS AUDITED ON EVERY BRANCH.** Publishing two numbers instead of one is
not a way to publish two unaudited numbers.

## THIS STUDY IS HELD, AND THIS REVIEW IS WHY

**The hunt for our own error [R-GAP-04] was run on 10 September 2026 and it did not come
back empty.** Four corrections were found against the company's own filings, priced, and
NOT applied:

| what the hunt found | EGP/share |
|---|---:|
| the ANNA nameplate, read against KIMA-2's own disclosed capital intensity | **4.874** |
| inventory carried GROSS of the documentary credits note 11 discloses inside it | 0.604 |
| ammonium nitrate priced at a typed USD 280 against the company's own disclosed EGP 20,000/t realisation (note 20) | 0.564 |
| listed investments marked to 31 March rather than to the strike date (note 8-1) | 0.064 |
| **total, against a gap of 9.21** | **6.106** |

**Every one of them is ours.** Two thirds of the disagreement with the market on the
carried-through branch is accounted for by defects in this study that its own hunt located.
The study therefore fails its own northern-star case on that branch and is HELD.

**AND THE LARGEST IS NOT MERELY UNAPPLIED — IT IS UNRESOLVED.** The company discloses the
ANNA programme at USD 278.4mn **plus** EGP 6,422mn for 600 t/d of nitric acid and 800 t/d of
ammonium nitrate, and discloses KIMA-2 — a whole 1,200 t/d ammonia and 1,575 t/d urea
complex — at USD 292.3mn plus EGP 1.92bn. **The same money buys 264kt of nitrate as bought
575kt of urea.** The auditor's own interim report calls the project **the KIMA ammonia
plant** and names an ammonia licensor on it; note 18-3 calls it acid and nitrates; note 7
calls it acid and fertiliser. **This model sells nothing out of it but ammonium nitrate.**
Picking the flattering reading of a document set that disagrees with itself is not a
correction, it is a preference, so it has not been taken.

## WHAT MOVED SINCE THE 05-09-2026 REVIEW

|  | carried through | stopped |
|---|---:|---:|
| the 05-09-2026 edition | 4.0396 | 8.0388 |
| the terminal risk-free rate off the house path, and the country premium charged once | | |
| **this edition** | **5.0224** | **9.1288** |

**AND THE PUBLISHED ANSWER WAS 21% BELOW ITS OWN MODEL BEFORE THAT.** The study reads the
house macro path for its terminal rate, so when the house structural real rate moved this
morning the model moved with it — and only part of the numbers file was regenerated. The
delivered document, the workbook and the lens record went on carrying 4.0396 while the model
said 4.8990, and the study's own reconciliation gate FAILED ten of its sixteen headline
checks and said so in as many words. **A study's own red gate is not a warning to be
carried; it is the study saying it cannot be issued.**

---

## 1. LATEST FILINGS

Every disclosed period is read. The audited annual report for FY2024/25 and the reviewed
nine months to **31 March 2026** — the latest disclosure, and the balance sheet every bridge
line stands on. **Nothing has been disclosed since**; the FY2025/26 annual report is due late
September 2026 and is the document that settles the ANNA question above.

**ONE SOURCE ROUTE HAS GONE DEAD AND IT IS RECORDED RATHER THAN LEFT.** The 30 June 2026
board disclosure URL registered in `filings/SOURCES.md` now returns 404. It is worth a live
re-fetch before the next edition.

## 2. BASE YEAR

FY2025/26E revenue of **EGP 10,378.7mn** is built on nine reviewed months of EGP 7,314.9mn
with the fourth quarter run-rated **below** the third (3,064 against 3,158.6) — the forecast
does not extrapolate the best quarter it holds.

**ONE COSMETIC FLAW, STATED:** the FY2025/26E "net" of 531.31 is the NINE-MONTH figure
printed in a full-year row. It does not enter the valuation.

## 3. MACRO COHERENCE

The terminal risk-free is read from `engine/macro_paths/EG.json` — `_HOUSE.terminal_rf` —
and terminal growth from the same file's `terminal_growth()`, so one inflation sits in both.
**A DEFECT IN THIS HEADING WAS CORRECTED ON 5 SEPTEMBER AND IS RESTATED:** the terminal
risk-free line once COMPOUNDED inflation with the real rate where the house path adds them,
worth 38.5 basis points on the rate and several per cent on the answer through the terminal
block.

## 4. DISCOUNT RATE

Explicit cost of equity **29.08%** at a beta of 1.0198; explicit weighted cost of capital
**25.63%**; terminal cost of equity **19.99%**; terminal weighted rate **16.88%**.

**THE COUNTRY PREMIUM IS NOW CHARGED ONCE AND FLAT,** which it was not in the 5 September
edition: mature equity premium 4.23%, Egypt's country premium 5.18%, and beta applies only
to the first. The retired construction multiplied both by beta, so at 1.0198 it over-charged
this company for the sovereign by about 10 basis points relative to an identical business at
a beta of one. Small here, and it is fixed because it is wrong rather than because it is
large.

**THE IDENTITY WAS WRITTEN OUT BY HAND IN SEVEN PLACES IN THIS STUDY** — the glide builder,
the record, four workbook cells and the terminal label — and all seven were left behind when
the construction changed. They now go through the sanctioned module.

## 5. TERMINAL

| | carried through | stopped |
|---|---:|---:|
| present value, explicit window | 3,881.5 | 11,125.6 |
| present value of the terminal | 12,590.5 | 13,504.0 |
| **terminal as a share of enterprise value** | **76.4%** | **54.8%** |

**THE TERMINAL CARRIES THREE QUARTERS OF THE CARRIED-THROUGH BRANCH,** and that branch is
the one whose nameplate is in question. The two facts compound: if the ANNA plant's output
slate is wrong, it is wrong in the part of the model that carries most of the weight.

Terminal growth 7.00% nominal at a stated zero real, against a terminal rate embedding the
same 7.00% inflation.

## 6. BALANCE SHEET

The bridge stands on the reviewed sheet of **31 March 2026** and is identical on both
branches except for the enterprise value above it:

| | EGP mn |
|---|---:|
| cash and equivalents | 4,606.5 |
| less interest-bearing debt | −14,639.0 |
| **net debt** | **10,032.5** |
| plus investments at fair value through other comprehensive income | +1,382.9 |
| plus investment property | +2,155.1 |

**THE BORROWINGS WERE VERIFIED LINE BY LINE AGAINST THE FILED SHEET** in the 10 September
hunt: bank loans 14,386.1 + holding-company loans 46.0 + current portion 207.0 = 14,639.0,
and cash 4,606.5. Both match to the thousand. About EGP 3.0bn of it is the first draw on the
ANNA facility — an asset not yet earning — and the model charges only the REMAINING spend,
so the sunk drawdown is not re-charged against the debt that funded it. **No double count.**

**AND ONE BRIDGE LINE IS KNOWN TO BE WRONG AND IS IN THE TABLE ABOVE.** The listed
investments are marked at 31 March (Abu Qir at 81.70) while the committed price file has
94.00 at the strike date. Worth +0.064 a share, unapplied, and listed in the hunt.

## 7. CLAIMS AGAINST THE RECORD

**A CLAIM THAT WAS FALSE IS CORRECTED.** A note in this study said no legal instrument for
the nitrogen-fertiliser export duty had been located. The instrument is real: **Decree No.
258 of 2026**, Official Gazette 25 June 2026, 10% ad valorem on the FOB value of
nitrogen-fertiliser exports, replacing a temporary USD 90/t duty and carrying no stated
expiry. Pure ammonium nitrate above 34.2% nitrogen is exempt, and the model already charges
the duty on urea alone. **The note was written without anybody looking.**

**AND THE DUTY IS NOT A CANDIDATE FOR CLOSING THE GAP, WHICH IS WORTH SAYING BECAUSE IT
LOOKS LIKE ONE.** Removing it is worth +2.940 a share — but this study also holds urea flat
at **USD 530/t for ever**, the war-tightened level the duty was imposed against. Take the war
price away with the duty (USD 400/t, no duty) and the pair is **−5.128**. The duty is the
price of a generous price path, and the two are one judgement.

**DIRECTION COUNT [R-ENF-05]:** re-priced at the frontier, this study resolved **5 of 12**
contested judgements to the lower value and **7 to the higher**. No systematic lean, and the
single largest sensitivity in the model — whether the subsidised gas quota is actually
enforced, worth **−8.24** a share — is resolved GENEROUSLY.

## 8. MULTIPLE CROSS-CHECK

| lens | EGP/share | vs spot 14.23 |
|---|---:|---:|
| relative multiples | 15.99 | +12.4% |
| **cash flow — programme stopped** | **9.13** | **−35.8%** |
| **cash flow — programme carried through** | **5.02** | **−64.7%** |
| normalised earnings power | 4.29 | −69.9% |
| book value, disclosed floor | 0.00 | — |

**THE RELATIVE LENS IS THE ONLY ONE ABOVE THE PRICE, AND IT IS THE LENS THAT DOES NOT SEE
THE CAPITAL PROGRAMME.** It values the company on trailing multiples of a business that has
not yet spent EGP 20.3bn — 71% of its market capitalisation — of which 27.8% is spent. That
is precisely the disagreement: the cash-flow lens charges the remaining spend and the
multiple lens does not.

**THE REVERSE READ.** To reach EGP 14.23 this model needs a **flat nominal EGP discount rate
of 13.06%** on the carried-through branch and **14.35%** on the stopped one — against an
Egyptian sovereign ten-year at **23.00%**. A buyer at this price is discounting an Egyptian
industrial equity at well below what the government that taxes it pays to borrow. **That is
outside the feasible set**, which is why the disagreement cannot be resolved on the rate and
must be resolved on the plant.

---

## Verdict

**AN ERROR WAS FOUND IN THE COMPANY'S FAVOUR — FOUR OF THEM — AND THEY ARE OURS, NOT THE
MARKET'S.** They are priced above and unapplied, and this study does not issue until they
are worked through the filings one at a time.

**What would have to happen for this study to be the one that is wrong:** KIMA's FY2025/26
annual report, due late September 2026, discloses the ANNA project's output slate and its
commissioning timetable. If it names ammonia, this model's nameplate is wrong by roughly the
factor the KIMA-2 capital-intensity comparison implies, the carried-through branch rises
toward the stopped one, and most of the disagreement with the market closes without anything
in the market's behaviour needing to have been a mistake.

**A SECOND, INDEPENDENT FALSIFIER:** on the corrected model the price still needs a flat urea
price of about **USD 616/t in perpetuity**, against USD 530 held, USD 545 front-month FOB
Egypt on 7 August 2026, and **USD 385 realised in FY2024/25**. If urea prints above 616 and
stays there, the market's number is the one the world agreed with.

**AND ONE THING THE MARKET MAY BE SEEING THAT THIS STUDY DOES NOT PRICE AT ALL.** In November
2025 KIMA sold 23,747,036 Abu Qir shares to its 69.8% parent at **EGP 48.72**; those shares
closed at 81.70 four months later and 94.00 on 3 September. **EGP 1,075mn — 0.54 a share —
of value left the listed company in a related-party transaction.** That argues the market
should discount KIMA, not that it should pay 2.8× this study.
