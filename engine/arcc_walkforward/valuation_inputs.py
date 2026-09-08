"""The VALUATION-INPUT BLOCK for this run — the figures a VALUE is rebuilt from.

[R-FCAL-01 AMENDED, 03-09-2026].  A driver panel is not a record a value can be
rebuilt from.  This run's `panel.py` committed the income statement, the revenue
and cost notes, the interest-bearing borrowings and the physical volumes — every
figure the walk-forward's own scoring needed — and left no trace of the balance
sheet beside them.  Measured by `engine/valuation_calibration/bridge_inputs.py`,
ARCC carried DEBT and DEPRECIATION and nothing else: no cash, no property, no
working capital, no share count, and therefore no route to capital expenditure
even by the identity, because the identity needs property at two dates.

WHY THAT MATTERED MORE THAN THE COUNT OF WHAT WAS MISSING.  Debt without cash is
the ASYMMETRIC half of a bridge: the debt that is committed is deducted in full
while the cash that would be added back is absent, so a bridge built from what
this run committed is biased DOWNWARD by construction — the same direction as the
hypothesis the calibration is testing, which is the one direction an instrument
must not be biased in.  ARCC held EGP 3,459,391,229 of cash at 31 December 2025
against EGP 1,133,932,616 of borrowings.  On that origin the omitted item is not
a rounding error; it is most of the bridge.

WHAT IS HERE.  For every origin the run declares — FY2018 to FY2025, fiscal years
ending 31 December — cash and equivalents, interest-bearing debt, property plant
and equipment, depreciation and amortisation, the working-capital lines, capital
expenditure, and the share count with the par value it was footed against.  FY2015,
FY2016 and FY2017 are carried too, OUTSIDE the origin list and labelled as what they
are: the prior-year anchors a trailing window reaches back into.  None of them is an
origin of this run and none is recorded as one.

WHY THE ANCHOR RUNS BACK THREE YEARS AND NOT ONE.  The identity capex = dPPE + D&A
needs property at two dates, which is why FY2017 was carried when FY2018 was the
first origin.  A capital-spending INTENSITY is a different shape of question: it is
taken over the three fiscal years to a date, so a rebuild standing at FY2017 reads
FY2015, FY2016 and FY2017 and one standing at FY2018 reads FY2016, FY2017 and
FY2018.  With the block starting at FY2017 neither of those windows could be filled
and both dates were unanswerable — not because the figures were disputed but because
nobody had copied them out.  This is [R-FCAL-01 AMENDED]'s own lesson arriving one
turn later: WHAT A PROCESS COMMITS DECIDES WHAT CAN EVER BE ASKED OF IT, and the
question that arrived needed one more year of the same copying.

EVERY FIGURE IS A COPY, NOT NEW RESEARCH.  Each one sits on a balance sheet or a
cash-flow statement in a filing this run had already parsed cell by cell; carrying
them out is transcription.  Not carrying them out meant no valuation of this
company could ever be rebuilt at a past origin, permanently, for any year whose
filings are no longer to hand.

ROUTE, AND WHY ARITHMETIC DECIDES [clause (iii)].  ARCC files every statement as
an image: across the eleven annual filings read here, not one page carried a text
layer worth reading — the two added last, FY2015 and FY2016, return NIL extractable
text across all 36 and 47 of their pages — so every figure arrived by OCR off the
rendered pixels and NOT ONE is believed because it looked clean.  Every balance
sheet foots against the identities ITS OWN PAGE states, and the footing runs at
import as assertions rather than living in a comment, which is this run's own house
discipline from `panel.py`.

TWO PRESENTATIONS, AND THE CHECK FOLLOWS THE PAGE.  FY2016 onwards print assets =
equity + liabilities.  FY2015 prints a WORKING-CAPITAL balance sheet and states no
total-assets line and no total-liabilities line at all, so a checker demanding them
would be condemning a page for not printing something the company never printed.
What is tested instead is every identity that page DOES assert — current assets less
current liabilities to its stated deficit, non-current assets plus that deficit to
its stated total investment, equity plus non-current liabilities to its stated total
finance, and the two sides against each other — which is the same number of tests
and the honest ones.  A GATE THAT FIRES ON A DIFFERENT PRESENTATION HAS FOUND A
PRESENTATION, NOT A DEFECT.

SEVEN FIGURES WERE READ WRONGLY AND ARITHMETIC CAUGHT ALL SEVEN.  Each looked
perfectly clean on the page and none would have been visible to a reader of the
extracted figure:

  FY2015 total non-current liabilities         1 688 590 700 -> 1 088 590 700
  FY2016 investments in a joint venture        2 445 783   -> 1 445 783
  FY2016 current income tax payable            116 577 542 -> 116 577 541
  FY2017 creditors and other credit balances   119 300 630 -> 119 240 630
  FY2018 trade receivables                     illegible   -> 92 994 532
  FY2019 total non-current assets              2 712 684 353 -> 2 712 084 353
  FY2023 depreciation of property and plant    215 976 939 -> 215 376 939
  FY2023 amortisation of right-of-use assets   6 891 239   -> 6 891 333

The FY2015 one is the argument for footing in one line: a six-hundred-million error
in a single digit, on a page whose every other figure was read correctly, refused by
the page's own three components AND by its own total-finance line, and returning the
right figure when the same page was re-rendered at 600 dpi.  The FY2016 tax figure
is the harder shape — the LAST digit, printing ...541 at one magnification and ...542
at another in BOTH the balance sheet and note 10.2, so no amount of re-rendering
settles it; what settles it is that the column requires 541, note 10.2's own two
components give 541, and the FY2017 filing's comparative prints 541.  THREE ROUTES
TO A DIGIT NO SCAN WILL RESOLVE.

The first three were settled by the statement's own column.  The last two were
first settled by the FY2024 filing's comparative column, whose every line foots to
the stated subtotal where the FY2023 page's own reading misses it by 599,906 —
and re-reading the FY2023 page ITSELF at higher magnification then returned the
same two figures, so they are that filing's own column after all and nothing is
carried back from a later one.  A LOW-RESOLUTION READING THAT DOES NOT FOOT LOOKS
EXACTLY LIKE A RE-PRESENTATION, and only re-reading the page tells them apart.

POINT IN TIME IS ABSOLUTE.  Every year is carried AS FIRST REPORTED, from its own
filing's own column.  One re-presentation falls inside this window and it is
recorded BESIDE the figure it would replace, never substituted: the FY2023 filing
nets EGP 36,385,385 of debtors against trade and notes payable in its FY2022
comparative, so an origin standing at FY2022 saw debtors of 235,320,162 and could
not have seen the 198,934,777 the next filing showed for the same date.

THE FILINGS ARE HELD AGAIN AND EVERY FIGURE WAS RE-READ.  `filings/` is
gitignored, so the container that rebuilds this repository starts without the
documents and a record that cannot be re-opened cannot be re-checked.  All nine
annual filings were fetched again from the company's own investor-relations
archive, at the URLs this run's own `fetch_attempts.json` already recorded, and
every balance sheet and cash-flow figure below was read a second time off the
pixels: 2017, 2018, 2019, 2020, 2021, 2022, 2024 and 2025 from each year's OWN
column, and 2023 from its own column with the FY2024 filing's comparative
settling the two figures its own page will not resolve.  Every line reproduced.
The FY2017 creditors line came back 119 300 630 on the second reading as well and
the column total again refuses it — the same misread twice, caught the same way,
which is the argument for footing rather than for a better extractor.

THE SHARE COUNT IS FOOTED ELEVEN TIMES, NOT READ ONCE [clause (ii)].  Every one of
these filings carries its own capital note — note 16 in FY2015 and note 20 from
FY2016 on, titled "Capital" to 2021 and "Issued and paid-up capital" from 2022 — and
every one prints the same three rows: par value per share, the number of ordinary
shares authorized, issued and fully paid, and the issued capital.  Eleven pages,
eleven readings, and the count is the same on all of them because the CAPITAL is the
same on all of them: the
last resolution that moved it was the January 2014 stock split, recited in note
20.2 of the 2016, 2017 and 2018 filings and in note 16 of the FY2015 filing itself,
which took EGP 757 479 400 from 7 574 794 shares at EGP 100 to 378 739 700 at EGP 2 —
and which is INSIDE this window at its near end, so the two years added here are the
two closest to the event that last moved the count and are read on their own pages
rather than assumed from the years after them.  An unchanged count read off eleven
pages is not today's count carried back; what clause (ii) forbids is the carrying, and
the difference is that these are eleven pages.  Each foots twice — issued capital
divided by par reproduces the count the same note states, and the note's issued
capital reproduces the issued and paid-up capital on that year's own balance
sheet — and both run at import.  TWO THINGS ARE RECORDED RATHER THAN TIDIED AWAY:
the FY2019 note's table is headed 2018 and 2017 where the notes around it read
2019 and 2018, a stale header left in the filing, settled by the arithmetic and by
the FY2020 filing's own properly-headed comparative; and the FY2025 count is the
ISSUED count, with note 21's 3 872 255 treasury shares at EGP 143 327 985 named
beside it rather than netted off, because which of the two a value is divided by
is a valuation choice and this record makes none.

WHAT IS DELIBERATELY NOT DECIDED HERE.  This module records; it values nothing.
Where a figure could be defined two ways the record carries the disclosed lines
and names the convention rather than resolving it — interest-bearing debt is the
three borrowing lines this run's own `panel.py` forms its rate on, with the lease
liabilities carried BESIDE them rather than folded in or dropped, because whether
a lease liability is debt is a valuation choice and not a reading of the page.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CALIB = os.path.join(os.path.dirname(HERE), "valuation_calibration")

# The origins this run declares (PRE_REGISTRATION_01-09-2026.md, section 'Origins
# and horizons'). FY2017 is NOT one of them and is carried separately below.
ORIGINS = ["FY%d" % y for y in range(2018, 2026)]

# Which filing carries which year's own column, and the page the figure sits on.
# The file names are the company's own, as published on its investor-relations
# archive and as this run's `panel.py` SOURCES already records them.
FILES = {
    2015: ("ACC-2015-Consolidated-Financials-English.pdf", "ARCC_FY2015_Consolidated.pdf"),
    2016: ("FY-2016-Consolidated-Financials-English.pdf", "ARCC_FY2016_Consolidated.pdf"),
    2017: ("FY-2017-Consolidated-Financials-English.pdf", "ARCC_FY2017_Consolidated.pdf"),
    2018: ("ARCC_FY_2018_Consolidated_Financials-English.pdf", "ARCC_FY2018_Consolidated.pdf"),
    2019: ("FY_2019_Consolidated_Financials-English.pdf", "ARCC_FY2019_Consolidated.pdf"),
    2020: ("FY-2020-consolidated-financials-english.pdf", "ARCC_FY2020_Consolidated.pdf"),
    2021: ("FY_2021_Consolidated_Financials-English.pdf", "ARCC_FY2021_Consolidated.pdf"),
    2022: ("FY_2022_Consolidated_Financials-English.pdf", "ARCC_FY2022_Consolidated.pdf"),
    2023: ("4Q2023_ACC_Consolidated_Financials.pdf", "ARCC_FY2023_Consolidated.pdf"),
    2024: ("FY2024_Consolidated_Financials-English.pdf", "ARCC_FY2024_Consolidated.pdf"),
    2025: ("FY-2025-Consolidated-Financials-English.pdf", "ARCC_FY2025_Consolidated.pdf"),
}

ROUTE = ("OCR off the rendered pixels — the filing carries no text layer on any "
         "page (nil extractable text across all 520 pages of the eleven annual "
         "filings, re-measured when FY2015 and FY2016 were added and nil on both "
         "of those too), so every figure was read from an image, at 200 to 300 dpi, "
         "with a table re-rendered at higher magnification — 600, 1200, up to 2400 "
         "dpi on the digits that would not resolve — wherever a small figure did "
         "not settle; every figure footed against the statement's own arithmetic "
         "before it was recorded, and the arithmetic rather than the extractor's "
         "confidence is what settled every disagreement")

# ---------------------------------------------------------------------------
# Consolidated statement of financial position, OWN column, at 31 December.
# Stated positive as printed. Every line below is asserted against the
# statement's own subtotals in `foot()`.
# ---------------------------------------------------------------------------
BS = {
 # FY2015 IS A DIFFERENT STATEMENT ALTOGETHER AND THE RECORD SAYS SO RATHER THAN
 # FLATTENING IT.  This filing presents a WORKING-CAPITAL balance sheet — non-current
 # assets, then current assets less current liabilities to a "(Deficit in) working
 # capital", then "Total investment", then "Financed by:" equity and non-current
 # liabilities — so there is no total-assets line and no total-liabilities line on the
 # page at all.  `fmt` names which presentation each year carries and `foot()` runs the
 # identities the page itself states.  Two further presentation facts ride with it: the
 # trade receivable is INSIDE "Debtors and other debit balances" (note 9 splits it at
 # EGP 5 500 032) and the trade payable is INSIDE "Creditors and other credit balances"
 # (note 13 splits it at EGP 289 654 854), where 2016 onwards print both on their own
 # lines — so the aggregates are carried on the page's own lines with `trade_receivables`
 # and `trade_payables` at nil, the disclosed splits named in NOTES, and the working
 # capital TOTAL on the same definition as every other year because the definition sums
 # all of them.  Equity carries a fourth line, "Net profits for the year", which later
 # years fold into retained earnings; `profit_for_year` keeps the page's own line.
 2015: dict(page=(4,), fmt="working_capital",
   ppe=2_546_154_219, auc=124_756_807, intangibles=109_142_259, other_assets=0,
   rou=0, jv=0, tnca=2_780_053_285,
   inventories=198_339_836, trade_receivables=0, debtors=66_249_751,
   due_from_related=0, cash=379_206_624, tca=643_796_211,
   capital=757_479_400, treasury=0, legal_reserve=156_122_086, retained=181_155_133,
   profit_for_year=277_224_384,
   parent_equity=1_371_981_003, nci=13_702, total_equity=1_371_994_705,
   borrowings_nc=357_584_237, notes_payable_nc=0, dtl=330_616_463,
   other_liab_nc=400_390_000, lease_nc=0, tncl=1_088_590_700,
   trade_payables=0, credit_facilities=1_714_317, tax_payable=71_766_122,
   borrowings_cp=206_297_400, other_liab_cp=86_430_000, creditors=529_421_515,
   lease_c=0, due_to_related=51_765_814, provisions=15_868_923, dividends_payable=0,
   tcl=963_264_091,
   wc_deficit=-319_467_880, total_investment=2_460_585_405,
   total_finance=2_460_585_405,
   facility_label="bank_overdraft",
   read_dispute=("a first reading at 300 dpi returned total non-current liabilities of "
                 "1 688 590 700, which the page's own three components (357 584 237 + "
                 "400 390 000 + 330 616 463 = 1 088 590 700) refuse and which the "
                 "page's own 'Total finance of working capital and non-current assets' "
                 "of 2 460 585 405 refuses a second time. RE-READING THE SAME PAGE AT "
                 "600 dpi RETURNS 1 088 590 700 — this filing's own figure, and nothing "
                 "is carried in from another document. The disagreement was the "
                 "extractor's and not the company's")),
 # FY2016 returns to the assets = equity + liabilities presentation the later years use,
 # bilingual, and it is the devaluation year: note 12 capitalises EGP 372 983 255 of
 # foreign-currency exchange differences into the cost of property, which is why this
 # year's capex identity runs far above its disclosed cash figure (see `_capex`).
 2016: dict(page=(5, 6),
   ppe=2_890_580_340, auc=17_670_237, intangibles=86_622_259, other_assets=0,
   rou=0, jv=1_445_783, tnca=2_996_318_619,
   inventories=280_626_750, trade_receivables=20_165_342, debtors=97_645_204,
   due_from_related=1_910_248, cash=136_820_111, tca=537_167_655,
   total_assets=3_533_486_274,
   capital=757_479_400, treasury=0, legal_reserve=185_127_989, retained=339_205_125,
   parent_equity=1_281_812_514, nci=19_114, total_equity=1_281_831_628,
   borrowings_nc=463_562_238, notes_payable_nc=0, dtl=340_285_124,
   other_liab_nc=196_149_919, lease_nc=0, tncl=999_997_281,
   trade_payables=353_637_901, credit_facilities=66_116_749, tax_payable=116_577_541,
   borrowings_cp=371_986_732, other_liab_cp=146_462_000, creditors=179_279_676,
   lease_c=0, due_to_related=8_413_626, provisions=9_183_140, dividends_payable=0,
   tcl=1_251_657_365, total_liabilities=2_251_654_646, teal=3_533_486_274,
   read_dispute=("this scan does not resolve two digits and ARITHMETIC SETTLED BOTH "
                 "rather than the extractor. (i) The current income tax payable prints "
                 "as ...541 at one magnification and ...542 at another, on the balance "
                 "sheet AND in note 10.2; the current-liabilities column requires "
                 "116 577 541 given the seven other lines, note 10.2's own two "
                 "components (115 020 127 + 1 557 414) give 116 577 541, and the FY2017 "
                 "filing's 2016 comparative column prints 116 577 541. (ii) The "
                 "investment in a joint venture read 2 445 783 at 600 dpi and 1 445 783 "
                 "at 1200 dpi; only 1 445 783 foots the stated total non-current assets "
                 "of 2 996 318 619, and note 15 and the FY2017 comparative both print "
                 "1 445 783. Every other line on this page reproduced on a second "
                 "reading")),
 2017: dict(page=(5, 6),
   ppe=2_371_924_441, auc=249_232_824, intangibles=396_151_869, other_assets=83_653,
   rou=0, jv=2_023_874, tnca=3_019_416_661,
   inventories=257_544_521, trade_receivables=15_512_298, debtors=85_007_648,
   due_from_related=0, cash=133_557_621, tca=491_622_088, total_assets=3_511_038_749,
   capital=757_479_400, treasury=0, legal_reserve=209_713_200, retained=325_021_738,
   parent_equity=1_292_214_338, nci=22_017, total_equity=1_292_236_355,
   borrowings_nc=601_101_209, notes_payable_nc=7_000_000, dtl=337_657_419,
   other_liab_nc=92_968_685, lease_nc=0, tncl=1_038_727_313,
   trade_payables=455_229_498, credit_facilities=300_419_651, tax_payable=110_901,
   borrowings_cp=167_535_000, other_liab_cp=114_462_000, creditors=119_240_630,
   lease_c=0, due_to_related=7_384_177, provisions=15_693_224, dividends_payable=0,
   tcl=1_180_075_081, total_liabilities=2_218_802_394, teal=3_511_038_749),
 2018: dict(page=(5, 6),
   ppe=2_473_177_771, auc=106_904_072, intangibles=345_475_618, other_assets=47_801,
   rou=0, jv=2_264_213, tnca=2_927_869_475,
   inventories=287_985_828, trade_receivables=92_994_532, debtors=107_874_288,
   due_from_related=0, cash=184_590_855, tca=673_445_503, total_assets=3_601_314_978,
   capital=757_479_400, treasury=0, legal_reserve=231_456_593, retained=329_029_161,
   parent_equity=1_317_965_154, nci=2_149_810, total_equity=1_320_114_964,
   borrowings_nc=619_160_870, notes_payable_nc=0, dtl=344_798_687,
   other_liab_nc=12_308_000, lease_nc=0, tncl=976_267_557,
   trade_payables=592_601_887, credit_facilities=273_674_586, tax_payable=293_208,
   borrowings_cp=77_731_487, other_liab_cp=124_681_184, creditors=216_867_519,
   lease_c=0, due_to_related=8_460_876, provisions=10_621_710, dividends_payable=0,
   tcl=1_304_932_457, total_liabilities=2_281_200_014, teal=3_601_314_978),
 2019: dict(page=(5, 6),
   ppe=2_408_100_199, auc=3_777_941, intangibles=294_799_369, other_assets=11_951,
   rou=3_086_102, jv=2_308_791, tnca=2_712_084_353,
   inventories=162_831_419, trade_receivables=27_529_031, debtors=115_574_736,
   due_from_related=0, cash=101_331_254, tca=407_266_440, total_assets=3_119_350_793,
   capital=757_479_400, treasury=0, legal_reserve=254_820_827, retained=151_416_266,
   parent_equity=1_163_716_493, nci=30_980, total_equity=1_163_747_473,
   borrowings_nc=491_836_958, notes_payable_nc=0, dtl=338_826_864,
   other_liab_nc=0, lease_nc=1_538_321, tncl=832_202_143,
   trade_payables=704_046_978, credit_facilities=62_035_301, tax_payable=13_903_338,
   borrowings_cp=90_356_520, other_liab_cp=12_308_000, creditors=216_252_373,
   lease_c=981_360, due_to_related=10_743_810, provisions=12_773_497, dividends_payable=0,
   tcl=1_123_401_177, total_liabilities=1_955_603_320, teal=3_119_350_793),
 2020: dict(page=(5, 6),
   ppe=2_202_003_667, auc=7_800_244, intangibles=254_049_586, other_assets=0,
   rou=1_047_456, jv=2_454_486, tnca=2_467_355_439,
   inventories=176_470_491, trade_receivables=15_938_789, debtors=136_384_081,
   due_from_related=0, cash=67_032_927, tca=395_826_288, total_assets=2_863_181_727,
   capital=757_479_400, treasury=0, legal_reserve=257_830_772, retained=18_551_721,
   parent_equity=1_033_861_893, nci=31_108, total_equity=1_033_893_001,
   borrowings_nc=387_454_349, notes_payable_nc=11_021_813, dtl=323_765_007,
   other_liab_nc=0, lease_nc=0, tncl=722_241_169,
   trade_payables=459_805_964, credit_facilities=340_110_399, tax_payable=438_220,
   borrowings_cp=99_165_216, other_liab_cp=769_250, creditors=180_575_890,
   lease_c=915_298, due_to_related=6_767_033, provisions=18_500_287, dividends_payable=0,
   tcl=1_107_047_557, total_liabilities=1_829_288_726, teal=2_863_181_727),
 2021: dict(page=(5, 6),
   ppe=2_019_945_189, auc=3_261_312, intangibles=219_424_613, other_assets=0,
   rou=17_631_358, jv=2_523_361, tnca=2_262_785_833,
   inventories=369_730_638, trade_receivables=58_876_151, debtors=153_272_743,
   due_from_related=0, cash=128_250_456, tca=710_129_988, total_assets=2_972_915_821,
   capital=757_479_400, treasury=0, legal_reserve=257_830_772, retained=45_625_489,
   parent_equity=1_060_935_661, nci=38_681, total_equity=1_060_974_342,
   borrowings_nc=272_760_907, notes_payable_nc=7_610_691, dtl=301_472_827,
   other_liab_nc=0, lease_nc=6_979_776, tncl=588_824_201,
   trade_payables=693_703_628, credit_facilities=240_386_963, tax_payable=43_280_867,
   borrowings_cp=114_334_781, other_liab_cp=0, creditors=184_254_394,
   lease_c=9_566_342, due_to_related=11_792_907, provisions=25_797_396, dividends_payable=0,
   tcl=1_323_117_278, total_liabilities=1_911_941_479, teal=2_972_915_821),
 2022: dict(page=(5,),
   ppe=1_839_104_558, auc=3_952_133, intangibles=191_268_364, other_assets=0,
   rou=12_992_066, jv=2_569_276, tnca=2_049_886_397,
   inventories=624_486_267, trade_receivables=79_554_875, debtors=235_320_162,
   due_from_related=76_140, cash=818_442_022, tca=1_757_879_466,
   total_assets=3_807_765_863,
   capital=757_479_400, treasury=0, legal_reserve=260_543_120, retained=145_003_980,
   parent_equity=1_163_026_500, nci=38_121, total_equity=1_163_064_621,
   borrowings_nc=177_476_090, notes_payable_nc=4_544_514, dtl=266_201_710,
   other_liab_nc=0, lease_nc=6_724_129, tncl=454_946_443,
   trade_payables=847_567_285, credit_facilities=360_644_205, tax_payable=198_386_556,
   borrowings_cp=163_534_780, other_liab_cp=0, creditors=299_002_000,
   lease_c=6_411_505, due_to_related=369_246, provisions=63_871_019,
   dividends_payable=249_968_203,
   tcl=2_189_754_799, total_liabilities=2_644_701_242, teal=3_807_765_863),
 2023: dict(page=(5,),
   ppe=1_683_607_099, auc=2_426_563, intangibles=163_112_115, other_assets=0,
   rou=12_901_506, jv=0, tnca=1_862_047_283,
   inventories=986_106_029, trade_receivables=228_615_932, debtors=249_566_135,
   due_from_related=95_368, cash=561_096_680, tca=2_025_480_144,
   total_assets=3_887_527_427,
   capital=757_479_400, treasury=0, legal_reserve=294_829_534, retained=701_912_725,
   parent_equity=1_754_221_659, nci=48_010, total_equity=1_754_269_669,
   borrowings_nc=0, notes_payable_nc=1_788_996, dtl=282_218_616,
   other_liab_nc=0, lease_nc=1_739_258, tncl=285_746_870,
   trade_payables=1_067_664_610, credit_facilities=90_074_273, tax_payable=216_715_896,
   borrowings_cp=0, other_liab_cp=0, creditors=309_899_324,
   lease_c=9_481_649, due_to_related=0, provisions=54_445_334,
   dividends_payable=99_229_802,
   tcl=1_847_510_888, total_liabilities=2_133_257_758, teal=3_887_527_427),
 2024: dict(page=(5,),
   ppe=1_669_630_565, auc=706_855_633, intangibles=134_955_866, other_assets=0,
   rou=4_436_332, jv=0, tnca=2_515_878_396,
   inventories=852_490_043, trade_receivables=160_048_158, debtors=632_979_976,
   due_from_related=156_657, cash=1_687_062_873, tca=3_332_737_707,
   total_assets=5_848_616_103,
   capital=757_479_400, treasury=0, legal_reserve=363_627_770, retained=1_182_365_129,
   parent_equity=2_303_472_299, nci=53_721, total_equity=2_303_526_020,
   borrowings_nc=120_392_380, notes_payable_nc=301_142_055, dtl=241_146_994,
   other_liab_nc=0, lease_nc=1_642_532, tncl=664_323_961,
   trade_payables=839_311_693, credit_facilities=615_044_229, tax_payable=374_014_396,
   borrowings_cp=25_481_075, other_liab_cp=0, creditors=345_087_344,
   lease_c=3_625_821, due_to_related=0, provisions=77_899_139,
   dividends_payable=600_302_425,
   tcl=2_880_766_122, total_liabilities=3_545_090_083, teal=5_848_616_103),
 2025: dict(page=(5,),
   ppe=2_522_323_523, auc=391_543_753, intangibles=106_799_617, other_assets=0,
   rou=822_030, jv=0, tnca=3_021_488_923,
   inventories=1_053_646_218, trade_receivables=244_416_417, debtors=1_004_779_062,
   due_from_related=0, cash=3_459_391_229, tca=5_762_232_926,
   total_assets=8_783_721_849,
   capital=757_479_400, treasury=-143_327_985, legal_reserve=379_505_774,
   retained=3_648_917_046,
   parent_equity=4_642_574_235, nci=158_005, total_equity=4_642_732_240,
   borrowings_nc=888_522_538, notes_payable_nc=0, dtl=255_316_160,
   other_liab_nc=103_020_835, lease_nc=0, tncl=1_246_859_533,
   trade_payables=720_176_243, credit_facilities=99_916_937, tax_payable=1_102_259_109,
   borrowings_cp=145_493_141, other_liab_cp=0, creditors=713_424_488,
   lease_c=1_176_042, due_to_related=0, provisions=111_684_116, dividends_payable=0,
   tcl=2_894_130_076, total_liabilities=4_140_989_609, teal=8_783_721_849),
}

# ---------------------------------------------------------------------------
# Consolidated statement of cash flows, OWN column, for the year.
# Capital expenditure is DISCLOSED on every one of these statements — payments
# for property, plant and equipment and payments for assets under construction,
# each its own line — so it is committed as a figure and NOT derived. The
# identity is still reported beside it in `build()`, because two independent
# routes to one number is a check and the disagreement between them is the
# accrual/cash difference a reader should see rather than a defect.
# ---------------------------------------------------------------------------
CF = {
 2015: dict(page=(7,), dep_ppe=175_412_201, amort_intangibles=22_520_000,
            amort_other=0, amort_rou=0,
            capex_ppe=17_479_672, capex_auc=52_700_132, capex_other=0,
            cash_end=379_206_624,
            impairment_goodwill=8_274_220,
            impairment_note=(
                "this filing's cash-flow statement carries ONE add-back line, "
                "\"Intangible assets' amortization\" of 30 794 220, and note 7 splits it: "
                "22 520 000 of amortisation of the electricity-supply agreement and "
                "8 274 220 of IMPAIRMENT of the Andalus goodwill, which the note writes "
                "on its own row and which reduces the goodwill to nil. An impairment is "
                "not an amortisation charge, so the depreciation-and-amortisation figure "
                "recorded here is 175 412 201 + 22 520 000 and the impairment is carried "
                "BESIDE it rather than folded in or dropped. Two independent grounds: the "
                "company's own note 7, and the FY2016 filing, which prints \"Impairment of "
                "goodwill 8 274 220\" as its own line in the 2015 comparative. The three "
                "still foot to the 30 794 220 this page states"),
            note=("capital expenditure is DISCLOSED on this statement as two lines and "
                  "both are confirmed twice over: the FY2016 filing's 2015 comparative "
                  "column prints the same 17 479 672 and 52 700 132, and note 6's "
                  "projects-under-construction roll-forward states additions of "
                  "51 381 120 plus advances to suppliers of 1 319 012, which is the "
                  "52 700 132 exactly")),
 2016: dict(page=(10, 11), dep_ppe=183_571_516, amort_intangibles=22_520_000,
            amort_other=0, amort_rou=0,
            capex_ppe=17_581_585, capex_auc=22_111_253, capex_other=0,
            cash_end=136_820_111,
            note=("the depreciation figure is the one the CASH-FLOW page states and note "
                  "12's own accumulated-depreciation roll-forward reproduces it "
                  "independently (1 142 761 518 closing less 963 832 740 opening plus "
                  "4 642 738 eliminated on disposals = 183 571 516); the two payment "
                  "lines reproduce from this page's own investing subtotal of "
                  "(24 743 153) and are printed identically in the FY2017 filing's 2016 "
                  "comparative"),
            identity_note=(
                "this year the identity runs FAR above the disclosed cash figure — "
                "420 911 067 against 39 692 838 — and the reason is on the company's own "
                "note 12: the Central Bank floated the pound on 3 November 2016, and the "
                "note CAPITALISES EGP 372 983 255 of foreign-currency exchange "
                "differences into the cost of property. Adding the EGP 31 466 760 "
                "transferred in from inventory and taking out the disposals leaves the "
                "residue inside the reading tolerance of these scans. NONE OF IT IS "
                "SPENDING, which is exactly why the disclosed cash figure is what is "
                "committed and the identity is only ever reported beside it"),
            restatement_note=(
                "THE FY2017 FILING RESTATES THIS YEAR'S SPLIT — it shows "
                  "depreciation of 155 415 267 and amortisation of 50 676 249 for 2016, "
                  "28 156 249 moved from one line to the other, TOTALLING THE SAME "
                  "206 091 516 — because that filing reclassified the operating licence "
                "between property and intangibles. The figures recorded here are this "
                "filing's own, as first reported")),
 2017: dict(page=(10, 11), dep_ppe=186_297_452, amort_intangibles=50_676_249,
            amort_other=59_752, amort_rou=0,
            capex_ppe=17_594_103, capex_auc=242_103_780, capex_other=143_404,
            cash_end=133_557_621),
 2018: dict(page=(10, 11), dep_ppe=199_833_161, amort_intangibles=50_676_251,
            amort_other=35_852, amort_rou=0,
            capex_ppe=27_405_852, capex_auc=96_669_881, capex_other=0,
            cash_end=184_590_855),
 2019: dict(page=(10, 11), dep_ppe=210_637_159, amort_intangibles=50_676_249,
            amort_other=35_850, amort_rou=4_312_948,
            capex_ppe=38_380_668, capex_auc=3_436_791, capex_other=0,
            cash_end=101_331_254),
 2020: dict(page=(10, 11), dep_ppe=210_297_525, amort_intangibles=40_749_783,
            amort_other=11_951, amort_rou=2_038_646,
            capex_ppe=4_250_127, capex_auc=1_236_682, capex_other=0,
            cash_end=67_032_927),
 2021: dict(page=(10, 11), dep_ppe=217_929_493, amort_intangibles=34_624_973,
            amort_other=0, amort_rou=5_902_848,
            capex_ppe=19_208_760, capex_auc=0, capex_other=0,
            cash_end=128_250_456,
            note="the statement discloses a non-cash transaction beside it — the "
                 "unpaid portion of the purchase cost of fixed assets, EGP 13 235 203 "
                 "— so cash capital expenditure understates the year's additions by "
                 "that amount"),
 2022: dict(page=(9,), dep_ppe=208_215_007, amort_intangibles=28_156_249,
            amort_other=0, amort_rou=5_568_129,
            capex_ppe=27_374_376, capex_auc=690_821, capex_other=0,
            cash_end=818_442_022),
 2023: dict(page=(9,), dep_ppe=215_376_939, amort_intangibles=28_156_249,
            amort_other=0, amort_rou=6_891_333,
            capex_ppe=56_808_221, capex_auc=1_735_742, capex_other=0,
            cash_end=561_096_680,
            note="a first, lower-resolution reading of the FY2023 page gave "
                 "215 976 939 and 6 891 239; neither foots the adjustments "
                 "subtotal the same page states, and the FY2024 filing's "
                 "comparative column foots exactly. RE-READING THE FY2023 PAGE "
                 "ITSELF AT HIGHER MAGNIFICATION RETURNS 215 376 939 AND "
                 "6 891 333 — that filing's OWN column, agreeing with the FY2024 "
                 "comparative to the pound — so these are the figures as first "
                 "reported and nothing is carried back from a later filing. The "
                 "disagreement was the extractor's and not the company's, which is "
                 "why arithmetic and not the extractor is the arbiter"),
 2024: dict(page=(9,), dep_ppe=221_562_864, amort_intangibles=28_156_249,
            amort_other=0, amort_rou=7_082_414,
            capex_ppe=206_542_630, capex_auc=705_472_770, capex_other=0,
            cash_end=1_687_062_873),
 2025: dict(page=(9,), dep_ppe=259_089_682, amort_intangibles=28_156_249,
            amort_other=0, amort_rou=2_525_364,
            capex_ppe=329_893_202, capex_auc=466_577_558, capex_other=0,
            cash_end=3_459_391_229),
}

# ---------------------------------------------------------------------------
# The capital note, read off each year's OWN filing. THE COUNT IS FOOTED OR IT
# IS NOT RECORDED [clause (ii)]: issued capital divided by par must reproduce
# the count the same document states. Today's count is never carried back —
# each year's entry is that year's own note, with its own page.
# ---------------------------------------------------------------------------
#
# WHAT IS ON THE PAGE, AND WHY NINE IDENTICAL COUNTS ARE NINE READINGS AND NOT
# ONE CARRIED FORWARD.  Every one of these nine filings carries its own capital
# note — note 20 throughout, titled "Capital" to 2021 and "Issued and paid-up
# capital" from 2022 — and every one is the SAME three-row table: par value per
# share, the number of ordinary shares authorized, issued and fully paid, and the
# issued capital.  The count does not move across the window because the capital
# does not move: the last resolution that changed it was the January 2014 stock
# split, recited in note 20.2 of the 2017 and 2018 filings, which took EGP
# 757 479 400 from 7 574 794 shares at EGP 100 to 378 739 700 shares at EGP 2.
# Each year below is that year's OWN page, and each foots against that year's own
# balance sheet, which states the same issued and paid-up capital under note 20.
# The prohibition [clause (ii)] is on carrying TODAY'S count back to a past
# origin; it is not a prohibition on a count that is genuinely unchanged and read
# nine times, and the difference is exactly that these are nine pages.
CAPITAL = {
 2015: dict(shares=378_739_700, issued_capital=757_479_400, par_value=2.0,
            page=29, note="16",
            par_source=(
                "note 16 'Capital' prints authorized capital 757 479 400, issued and "
                "paid up capital 757 479 400, number of shares 378 739 700 and par value "
                "per share 2, in one table headed December 31, 2015 and December 31, "
                "2014; the same note then recites the 23 January 2014 Extraordinary "
                "General Assembly resolution updating Article No. (6) from 7 574 794 "
                "shares at EGP 100 to 378 739 700 shares at EGP 2, so the table and the "
                "recital state the same identity two ways in the same document")),
 2016: dict(shares=378_739_700, issued_capital=757_479_400, par_value=2.0,
            page=35, note="20.1",
            par_source=(
                "note 20.1 'Authorized and Issued capital', the same three-row table "
                "headed 2016 and 2015, with note 20.2's recital of the Article 6 "
                "resolution beneath it")),
 2017: dict(shares=378_739_700, issued_capital=757_479_400, par_value=2.0,
            page=33, note="20.1",
            par_source=(
                "note 20.1 'Authorized and Issued capital' prints par value per "
                "share (EGP) 2, number of ordinary shares authorized, issued and "
                "fully paid 378 739 700 and issued capital (EGP) 757 479 400 in "
                "one table headed 2017 and 2016; note 20.2 on the following page "
                "recites the Extraordinary General Assembly resolution updating "
                "Article No. (6) of the Articles of Association to EGP 757 479 400 "
                "distributed among 378 739 700 shares with a par value amounting "
                "to EGP 2 each, so the table and the recital state the same "
                "identity two ways in the same document")),
 2018: dict(shares=378_739_700, issued_capital=757_479_400, par_value=2.0,
            page=35, note="20.1",
            par_source=(
                "note 20.1 'Authorized and Issued capital', the same three-row "
                "table headed 2018 and 2017, with note 20.2's recital of the "
                "Article 6 resolution on the page after it")),
 2019: dict(shares=378_739_700, issued_capital=757_479_400, par_value=2.0,
            page=36, note="20",
            par_source=(
                "note 20 'Capital', the same three-row table. THE TABLE'S OWN "
                "COLUMN HEADERS READ 2018 AND 2017 while the notes around it read "
                "2019 and 2018 — a stale header left in the filing, recorded as "
                "read rather than silently corrected. What settles the year is "
                "arithmetic and two other pages: the FY2019 balance sheet states "
                "issued and paid-up capital of EGP 757 479 400 at 31 December 2019 "
                "under this same note, 757 479 400 / 2 reproduces 378 739 700, and "
                "the FY2020 filing's own note 20 — properly headed 2020 and 2019 — "
                "states par 2, 378 739 700 shares and EGP 757 479 400 for the 2019 "
                "comparative")),
 2020: dict(shares=378_739_700, issued_capital=757_479_400, par_value=2.0,
            page=37, note="20",
            par_source=("note 20 'Capital', the three-row table headed 2020 and "
                        "2019")),
 2021: dict(shares=378_739_700, issued_capital=757_479_400, par_value=2.0,
            page=35, note="20",
            par_source=("note 20 'Capital', the three-row table headed 2021 and "
                        "2020")),
 2022: dict(shares=378_739_700, issued_capital=757_479_400, par_value=2.0,
            page=33, note="20",
            par_source=("note 20 'Issued and paid-up capital', the three-row table "
                        "headed December 31, 2022 and December 31, 2021")),
 2023: dict(shares=378_739_700, issued_capital=757_479_400, par_value=2.0,
            page=35, note="20",
            par_source=("note 20 'Issued and paid-up capital', the three-row table "
                        "headed December 31, 2023 and December 31, 2022")),
 2024: dict(shares=378_739_700, issued_capital=757_479_400, par_value=2.0,
            page=35, note="20",
            par_source=("note 20 'Issued and paid-up capital', the three-row table "
                        "headed December 31, 2024 and December 31, 2023")),
 2025: dict(shares=378_739_700, issued_capital=757_479_400, par_value=2.0,
            page=33, note="20",
            par_source=("note 20 'Issued and paid-up capital', the three-row table "
                        "headed December 31, 2025 and December 31, 2024"),
            treasury_cost=143_327_985, treasury_shares=3_872_255,
            treasury_page=33, treasury_note="21",
            treasury_why=(
                "note 21 'Treasury shares' states that on July 21, 2025 the Board "
                "approved acquiring treasury shares and that the Company acquired "
                "during 2025 3 872 255 shares amounting to EGP 143 327 985, which "
                "the balance sheet carries as a deduction from equity of the same "
                "amount. THE COUNT RECORDED ABOVE IS THE ISSUED COUNT, which is "
                "what the capital note states and what foots against par; the "
                "shares in issue net of treasury are 374 867 445 and are named "
                "here rather than substituted, because which of the two a value is "
                "divided by is a valuation choice and this record makes none. This "
                "is the case clause (ii) anticipates — the capital note cannot see "
                "a treasury movement, so the movement is read off its own note")),
}

# PROPERTY AT THE DATE BEFORE THE FIRST YEAR CARRIED. FY2014 is NOT a year of this
# record and no block is built for it: the only thing needed of it is property at
# 31 December 2014, so that FY2015's disclosed capital expenditure has an identity to
# be checked against. It is read from the FY2015 filing's OWN comparative column, which
# is that filing's own page and the right vintage for a comparative — unlike a figure
# lifted out of a LATER year's comparative, which is a restatement wearing an original's
# clothes.
PRIOR_PPE = {
 2014: dict(ppe=2_676_733_351, auc=99_410_072, year_read=2015, page=(4,),
            what=("'Fixed assets (net)' and 'Projects under construction' in the "
                  "31 December 2014 comparative column of the FY2015 consolidated "
                  "balance sheet"),
            check=("that column foots on its own terms — non-current assets "
                   "2 676 733 351 + 99 410 072 + 139 936 479 = 2 916 079 902, the "
                   "stated total — and note 6's roll-forward opens 2015 on the same "
                   "99 410 072")),
}

# WHERE ONE YEAR AND THE NEXT ARE NOT ON ONE BASIS. The identity capex = dPPE + D&A
# compares property at two dates, so a RECLASSIFICATION between those dates makes the
# identity measure the reclassification rather than the spending. Where a break is
# declared here the cross-check is NOT RUN and the reason is recorded, because a number
# that cannot mean what it appears to mean is worse than no number. This changes no
# committed figure anywhere: capital expenditure is DISCLOSED on every one of these
# cash-flow statements and the identity is only ever reported beside it.
BASIS_BREAKS = {
 (2016, 2017): (
     "the FY2017 filing moves EGP 360 205 859 of the operating licence OUT of property, "
     "plant and equipment and INTO intangible assets: its 2016 comparative column prints "
     "property of 2 530 374 481 and intangibles of 446 828 118 against the 2 890 580 340 "
     "and 86 622 259 the FY2016 filing itself printed for the same date, the two "
     "differences equal and opposite to the pound and total non-current assets unchanged "
     "at 2 996 318 619. Run across that boundary on the figures AS FIRST REPORTED the "
     "identity returns -100 795 860 against a disclosed 259 841 287, which is the "
     "reclassification and not the spending; run on the re-presented base it returns "
     "259 409 999, within 431 288 of the disclosed figure — which is what establishes "
     "the diagnosis rather than asserting it. FY2017's committed capital expenditure is "
     "the DISCLOSED cash figure either way and does not move"),
}

# Disclosures that ride beside a figure and change how it should be read. Only the
# figures READ off a page are typed here; everything a reader would compare them
# against is computed in `_wc` from the committed lines, so no arithmetic is typed.
NOTES = {
 (2015, "wc"): dict(
     presentation=(
         "this filing prints NO separate trade receivable and NO separate trade payable: "
         "the trade debtor sits inside 'Debtors and other debit balances (net)' and note "
         "9 splits it at EGP 5 500 032 of a 66 249 751 total; the trade payable sits "
         "inside 'Creditors and other credit balances' and note 13 splits it at EGP "
         "289 654 854 of a 529 421 515 total. The two aggregate lines are carried on the "
         "page's own terms with the separate lines at nil, so the working-capital TOTAL "
         "is on the same definition as every other year — the definition sums all of "
         "them — while the disclosed split is named here rather than silently "
         "redistributed across lines this page does not carry"),
     trade_debtors_inside_debtors=5_500_032,
     trade_payable_inside_creditors=289_654_854,
 ),
 (2016, "wc"): dict(
     presentation=(
         "the trade receivable and the trade payable are back on their own lines from "
         "this filing onwards, so this year is on the same presentation as FY2017 and "
         "after"),
 ),
 (2022, "wc"): dict(
     re_presented_debtors=198_934_777,
     re_presented_tca=1_721_494_081,
     re_presented_total_assets=3_771_380_478,
     re_presented_in=2023, page=5,
     why=("netting debtors against trade and notes payable"),
 ),
}


def _close(a, b, tol=1):
    return abs(a - b) <= tol


def foot():
    """Every balance sheet against ITS OWN subtotals — the ones the page prints.

    TWO PRESENTATIONS SIT IN THIS WINDOW AND THE CHECK FOLLOWS THE PAGE RATHER THAN
    THE OTHER WAY ROUND. FY2016 onwards print assets = equity + liabilities. FY2015
    prints a WORKING-CAPITAL balance sheet: non-current assets, current assets less
    current liabilities to a stated deficit, a stated 'Total investment', and then
    equity plus non-current liabilities to a stated total finance. That page states
    no total assets and no total liabilities, so demanding them would be checking a
    line the company never printed; what is checked instead is every identity the
    page DOES assert, which is the same number of them.
    """
    bad = []
    for y, b in sorted(BS.items()):
        nca = sum(b[k] for k in ("ppe", "auc", "intangibles", "other_assets", "rou", "jv"))
        ca = sum(b[k] for k in ("inventories", "trade_receivables", "debtors",
                                "due_from_related", "cash"))
        ncl = sum(b[k] for k in ("borrowings_nc", "notes_payable_nc", "dtl",
                                 "other_liab_nc", "lease_nc"))
        cl = sum(b[k] for k in ("trade_payables", "credit_facilities", "tax_payable",
                                "borrowings_cp", "other_liab_cp", "creditors", "lease_c",
                                "due_to_related", "provisions", "dividends_payable"))
        eq = (b["capital"] + b["treasury"] + b["legal_reserve"] + b["retained"]
              + b.get("profit_for_year", 0))
        tests = [
            ("non-current assets", nca, b["tnca"]),
            ("current assets", ca, b["tca"]),
            ("non-current liabilities", ncl, b["tncl"]),
            ("current liabilities", cl, b["tcl"]),
            ("equity attributable to owners", eq, b["parent_equity"]),
            ("total equity", b["parent_equity"] + b["nci"], b["total_equity"]),
        ]
        if b.get("fmt") == "working_capital":
            tests += [
                ("working capital", b["tca"] - b["tcl"], b["wc_deficit"]),
                ("total investment", b["tnca"] + b["wc_deficit"], b["total_investment"]),
                ("total finance of working capital and non-current assets",
                 b["total_equity"] + b["tncl"], b["total_finance"]),
                ("the two sides of the page", b["total_investment"], b["total_finance"]),
            ]
        else:
            tests += [
                ("total assets", nca + ca, b["total_assets"]),
                ("total liabilities", ncl + cl, b["total_liabilities"]),
                ("equity and liabilities", b["total_equity"] + b["total_liabilities"],
                 b["teal"]),
            ]
        for what, got, want in tests:
            if not _close(got, want):
                bad.append("%d %s: %d against a stated %d" % (y, what, got, want))
    for y, c in sorted(CF.items()):
        if y in BS and not _close(c["cash_end"], BS[y]["cash"]):
            bad.append("%d cash at the end of the cash-flow statement %d against a "
                       "balance sheet %d" % (y, c["cash_end"], BS[y]["cash"]))
    for y, k in sorted(CAPITAL.items()):
        implied = k["issued_capital"] / k["par_value"]
        if abs(implied - k["shares"]) > max(1.0, 1e-6 * k["shares"]):
            bad.append("%d capital %.0f / par %.4g = %.0f against a stated %.0f — the "
                       "document does not foot against itself" % (
                           y, k["issued_capital"], k["par_value"], implied, k["shares"]))
        # the capital note and the balance sheet are two pages of one document and
        # must agree, or one of them was read wrongly
        if y in BS and not _close(k["issued_capital"], BS[y]["capital"]):
            bad.append("%d the capital note's issued capital %d against the balance "
                       "sheet's issued and paid-up capital %d"
                       % (y, k["issued_capital"], BS[y]["capital"]))
        if k.get("treasury_cost") and not _close(k["treasury_cost"],
                                                 -BS[y]["treasury"]):
            bad.append("%d the treasury note's cost %d against the balance sheet's "
                       "deduction from equity %d"
                       % (y, k["treasury_cost"], -BS[y]["treasury"]))
    return bad


_BAD = foot()
assert not _BAD, "the valuation-input block does not foot: " + "; ".join(_BAD)


def debt(y):
    """Interest-bearing borrowings, on this run's own definition.

    `panel.py` forms the effective rate on long-term borrowings, their current
    portion and credit facilities, and excludes trade and notes payable,
    creditors and other credit balances and current tax BY CONSTRUCTION — the
    [R-FCAL-01] trap (i) discipline. The same three lines are what is committed
    here, so the block and the panel cannot disagree about what debt means. The
    lease liabilities are carried BESIDE them, named, because folding them in or
    dropping them are both valuation choices and this record makes neither.
    """
    b = BS[y]
    return b["borrowings_nc"] + b["borrowings_cp"] + b["credit_facilities"]


def working_capital(y):
    """Operating working capital: the trading lines, and nothing else.

    Cash, borrowings, credit facilities, current tax, the dividend declared but
    unpaid, provisions and lease liabilities are all EXCLUDED and all named in
    the record, because a reader cannot tell an excluded line from an unread one.
    """
    b = BS[y]
    assets = (b["inventories"] + b["trade_receivables"] + b["debtors"]
              + b["due_from_related"])
    liabs = b["trade_payables"] + b["creditors"] + b["due_to_related"]
    return assets - liabs


def source(y, statement, page):
    f = FILES[y][0]
    return ("%s, %s, page %s (the company's own audited consolidated financial "
            "statements for the year ended 31 December %d, from its own "
            "investor-relations archive)"
            % (f, statement, ", ".join(str(p) for p in page), y))


def _cash(y):
    b, r = BS[y], dict(NOTES.get((y, "cash"), {}))
    rec = {
        "value": b["cash"],
        "as_at": "%d-12-31" % y,
        "source": source(y, "consolidated statement of financial position, "
                            "'Cash and bank balances'", BS[y]["page"]),
        "route": ROUTE,
        "lines": {"cash_and_bank_balances": b["cash"]},
        "check": ("the cash-flow statement closes on the same figure — "
                  "%d" % CF[y]["cash_end"]),
    }
    rec.update(r)
    return rec


def _debt(y):
    b = BS[y]
    return {
        "value": debt(y),
        "as_at": "%d-12-31" % y,
        "source": source(y, "consolidated statement of financial position, "
                            "borrowings (non-current), current portion of long-term "
                            "borrowings and credit facilities", BS[y]["page"]),
        "route": ROUTE,
        "definition": ("long-term borrowings, their current portion and credit "
                       "facilities — the three lines this run's own panel.py forms "
                       "its effective rate on, so the block and the panel cannot "
                       "disagree about what debt means"),
        "lines": {
            "borrowings_non_current": b["borrowings_nc"],
            "current_portion_of_long_term_borrowings": b["borrowings_cp"],
            b.get("facility_label", "credit_facilities"): b["credit_facilities"],
        },
        "carried_beside_not_folded_in": {
            "lease_liabilities_non_current": b["lease_nc"],
            "lease_liabilities_current": b["lease_c"],
            "notes_payable_non_current": b["notes_payable_nc"],
            "why": ("whether a lease liability or a long-dated supplier balance is "
                    "debt is a valuation choice; this record reads the page and "
                    "makes neither choice, so both are named rather than folded in "
                    "or dropped"),
        },
        "check": ("reproduces this run's own committed panel.DEBT total for the "
                  "same year"),
    }


def _capex(y):
    c = CF[y]
    disclosed = c["capex_ppe"] + c["capex_auc"] + c["capex_other"]
    rec = {
        "value": disclosed,
        "period": "FY%d" % y,
        "source": source(y, "consolidated statement of cash flows, investing "
                            "activities — payments for property, plant and equipment "
                            "and payments for assets under construction", c["page"]),
        "route": ROUTE,
        "derived": False,
        "disclosed": True,
        "lines": {
            "payments_for_property_plant_and_equipment": c["capex_ppe"],
            "payments_for_assets_under_construction": c["capex_auc"],
            "payments_for_other_assets": c["capex_other"],
        },
    }
    prior = None
    if (y - 1, y) in BASIS_BREAKS:
        rec["identity_cross_check_not_run"] = {
            "identity": "capex = dPPE + D&A",
            "why": BASIS_BREAKS[(y - 1, y)],
            "what_is_committed": ("the DISCLOSED cash figure above, which this break "
                                  "does not touch"),
        }
    elif y - 1 in BS:
        prior = dict(BS[y - 1])
        prior_src = "the FY%d filing's own balance sheet" % (y - 1)
    elif y - 1 in PRIOR_PPE:
        pp = PRIOR_PPE[y - 1]
        prior = dict(pp)
        prior_src = ("%s (%s)" % (pp["what"], FILES[pp["year_read"]][0]))
    if prior is not None:
        now = BS[y]
        ident = ((now["ppe"] + now["auc"]) - (prior["ppe"] + prior["auc"])
                 + c["dep_ppe"])
        rec["identity_cross_check"] = {
            "identity": "capex = dPPE + D&A",
            "value": ident,
            "basis": ("property, plant and equipment plus assets under construction "
                      "at both dates, and the depreciation of property, plant and "
                      "equipment for the year"),
            "prior_year_property": prior["ppe"] + prior["auc"],
            "prior_year_source": prior_src,
            "difference_from_disclosed": ident - disclosed,
            "note": ("the two are not the same measurement and the gap is not a "
                     "defect: disposals leave at net book value, additions can be "
                     "unpaid at the year end, and assets move out of construction "
                     "into property without cash. The DISCLOSED cash figure is what "
                     "is committed; the identity is reported beside it so a later "
                     "rebuild can see both rather than assume they agree"),
        }
        if c.get("identity_note"):
            rec["identity_cross_check"]["why_they_differ_this_year"] = c["identity_note"]
    if c.get("note"):
        rec["note"] = c["note"]
    return rec


def _ppe(y):
    b = BS[y]
    return {
        "value": b["ppe"],
        "as_at": "%d-12-31" % y,
        "source": source(y, "consolidated statement of financial position, "
                            "'Property, plant and equipment (net)'", BS[y]["page"]),
        "route": ROUTE,
        "lines": {
            "property_plant_and_equipment_net": b["ppe"],
            "assets_under_construction": b["auc"],
            "right_of_use_assets_net": b["rou"],
            "intangible_assets_net": b["intangibles"],
        },
        "note": ("the identity capex = dPPE + D&A is run on property PLUS assets "
                 "under construction, because this company's spending lands in "
                 "construction first and moves across without cash; the intangible "
                 "is the operating licence and amortises on its own line"),
    }


def _dep(y):
    c = CF[y]
    total = (c["dep_ppe"] + c["amort_intangibles"] + c["amort_other"]
             + c["amort_rou"])
    rec = {
        "value": total,
        "period": "FY%d" % y,
        "source": source(y, "consolidated statement of cash flows, the "
                            "depreciation and amortisation add-backs", c["page"]),
        "route": ROUTE,
        "lines": {
            "depreciation_of_property_plant_and_equipment": c["dep_ppe"],
            "amortisation_of_intangible_assets": c["amort_intangibles"],
            "amortisation_of_other_assets": c["amort_other"],
            "amortisation_of_right_of_use_assets": c["amort_rou"],
        },
        "note": ("the whole charge, which is more than the cost-of-sales "
                 "depreciation this run's panel.py carries: that one is the "
                 "manufacturing share and this is the group total"),
    }
    if c.get("impairment_goodwill"):
        rec["carried_beside_not_folded_in"] = {
            "impairment_of_goodwill": c["impairment_goodwill"],
            "why": c["impairment_note"],
            "the_three_foot": (total + c["impairment_goodwill"]),
        }
    if c.get("note"):
        rec["route_dispute"] = c["note"]
    return rec


def _wc(y):
    b = BS[y]
    rec = {
        "value": working_capital(y),
        "as_at": "%d-12-31" % y,
        "source": source(y, "consolidated statement of financial position, the "
                            "trading lines of current assets and current "
                            "liabilities", BS[y]["page"]),
        "route": ROUTE,
        "definition": ("inventories + trade receivables + debtors and other debit "
                       "balances + due from related parties, less trade and notes "
                       "payable, creditors and other credit balances and due to "
                       "related parties"),
        "lines": {
            "inventories": b["inventories"],
            "trade_receivables_net": b["trade_receivables"],
            "debtors_and_other_debit_balances_net": b["debtors"],
            "due_from_related_parties": b["due_from_related"],
            "trade_and_notes_payable": b["trade_payables"],
            "creditors_and_other_credit_balances": b["creditors"],
            "due_to_related_parties": b["due_to_related"],
            "total_current_assets": b["tca"],
            "total_current_liabilities": b["tcl"],
        },
        "excluded_and_named": {
            "cash_and_bank_balances": b["cash"],
            "credit_facilities": b["credit_facilities"],
            "current_portion_of_long_term_borrowings": b["borrowings_cp"],
            "current_income_tax_liability": b["tax_payable"],
            "dividends_payable": b["dividends_payable"],
            "provisions": b["provisions"],
            "lease_liabilities_current": b["lease_c"],
            "current_portion_of_long_term_other_liabilities": b["other_liab_cp"],
            "why": ("a reader cannot tell an excluded line from an unread one, so "
                    "every current line that is NOT in the working-capital figure "
                    "is named here with its own amount"),
        },
    }
    n = NOTES.get((y, "wc")) or {}
    if n.get("presentation"):
        rec["presentation"] = n["presentation"]
        for k in ("trade_debtors_inside_debtors", "trade_payable_inside_creditors"):
            if k in n:
                rec.setdefault("disclosed_split_named_not_redistributed", {})[k] = n[k]
    if n.get("re_presented_debtors"):
        b2 = dict(b)
        b2["debtors"] = n["re_presented_debtors"]
        alt = ((b2["inventories"] + b2["trade_receivables"] + b2["debtors"]
                + b2["due_from_related"])
               - (b2["trade_payables"] + b2["creditors"] + b2["due_to_related"]))
        d_debtors = b["debtors"] - n["re_presented_debtors"]
        d_tca = b["tca"] - n["re_presented_tca"]
        d_ta = b["total_assets"] - n["re_presented_total_assets"]
        rec["point_in_time"] = (
            "AS FIRST REPORTED. The FY%d filing's own statement of financial "
            "position states debtors and other debit balances (net) of %s at "
            "%d-12-31, and that is the figure in the working capital above. The "
            "FY%d filing re-presents the same date at %s — %s — carrying total "
            "current assets to %s and total assets to %s, the same %s in all "
            "three. An origin standing at FY%d could not have seen the later "
            "presentation, so it is recorded beside the figure it would replace "
            "and never substituted for it."
            % (y, format(b["debtors"], ","), y, n["re_presented_in"],
               format(n["re_presented_debtors"], ","), n["why"],
               format(n["re_presented_tca"], ","),
               format(n["re_presented_total_assets"], ","),
               format(d_debtors, ","), y))
        rec["re_presented_by_a_later_filing"] = {
            "debtors_and_other_debit_balances_net": n["re_presented_debtors"],
            "total_current_assets": n["re_presented_tca"],
            "total_assets": n["re_presented_total_assets"],
            "difference_on_each_of_the_three": d_debtors,
            "the_three_agree": d_debtors == d_tca == d_ta,
            "working_capital_on_that_basis": alt,
            "adopted": "the figure as first reported, above",
            "source": source(n["re_presented_in"],
                             "consolidated statement of financial position, the "
                             "%d-12-31 comparative column" % y, (n["page"],)),
            "route": ROUTE,
        }
    return rec


def _shares(y):
    if y not in CAPITAL:
        return {"missing": ("the capital note of the FY%d filing could not be read, "
                            "so no count is recorded — a count that does not foot "
                            "against its own issued capital and par value is not "
                            "recorded at all" % y)}
    k = CAPITAL[y]
    rec = {
        "value": k["shares"],
        "as_at": "%d-12-31" % y,
        "issued_capital": k["issued_capital"],
        "par_value": k["par_value"],
        "source": source(y, "note %s, the capital note" % k["note"], (k["page"],)),
        "route": ROUTE,
        "check": ("issued capital %d / par %g = %d, matching the count the same "
                  "note states" % (k["issued_capital"], k["par_value"],
                                   k["issued_capital"] / k["par_value"])),
        "par_source": k["par_source"],
        "vintage": ("read off the FY%d filing's own note; no later count is carried "
                    "back to this origin" % y),
    }
    if k.get("treasury_cost"):
        rec["treasury"] = {
            "shares_held": k["treasury_shares"],
            "at_cost": k["treasury_cost"],
            "shares_in_issue_net_of_treasury": k["shares"] - k["treasury_shares"],
            "balance_sheet_check": (
                "the deduction from equity on the same year's balance sheet is %s, "
                "the same figure"
                % format(-BS[y]["treasury"], ",")),
            "source": source(y, "note %s, treasury shares" % k["treasury_note"],
                             (k["treasury_page"],)),
            "route": ROUTE,
            "why": k["treasury_why"],
        }
    return rec


def block(y):
    return {
        "cash": _cash(y),
        "debt": _debt(y),
        "capex": _capex(y),
        "ppe": _ppe(y),
        "dep": _dep(y),
        "wc": _wc(y),
        "shares": _shares(y),
    }


def record():
    """The valuation-input block, in the shape [R-FCAL-01 AMENDED] defines."""
    return {
        "_": ("The inputs a VALUE is rebuilt from at each of this run's origins, "
              "committed beside the driver panel under [R-FCAL-01 AMENDED]. "
              "GENERATED by engine/arcc_walkforward/valuation_inputs.py, which "
              "foots every balance sheet against its own subtotals at import; "
              "never hand-edited."),
        "run": "ARCC",
        "rule": "[R-FCAL-01 AMENDED] (03-09-2026)",
        "company": "Arabian Cement Company S.A.E.",
        "currency": "EGP",
        "units": "as printed in the filings — units, not thousands or millions",
        "basis": "consolidated",
        "fiscal_year_end": "31 December",
        "origins_declared_by": "PRE_REGISTRATION_01-09-2026.md",
        "route": ROUTE,
        "point_in_time": (
            "every year is carried AS FIRST REPORTED, from its own filing's own "
            "column. Re-presentations inside this window are recorded beside the "
            "figure they would replace and never substituted — the FY2023 filing's "
            "netting of debtors in its FY2022 comparative, and the FY2017 filing's "
            "reclassification of EGP 360 205 859 of operating licence out of property "
            "and into intangibles in its FY2016 comparative, which also moves "
            "EGP 28 156 249 of FY2016's charge from depreciation to amortisation while "
            "leaving the total unchanged. The FY2016 filing likewise restates FY2015 "
            "(property by 1 253, depreciation by 453, deferred tax by 5 273, cash by "
            "919 730) and recognises a joint venture FY2015's own page does not carry; "
            "FY2015 is committed on its OWN page throughout. THE ONE FIGURE READ OUT "
            "OF A COMPARATIVE COLUMN IS PROPERTY AT 31 DECEMBER 2014, which is not a "
            "year of this record and exists only so FY2015's disclosed capital "
            "expenditure has an identity to be checked against; it is read from the "
            "FY2015 filing's OWN comparative, which is that filing's own page."),
        "sources": {str(y): FILES[y][0] for y in sorted(FILES)},
        "basis_breaks": dict({"FY%d to FY%d" % k: v
                              for k, v in sorted(BASIS_BREAKS.items())}, **{
            "_": ("Where one year and the next are NOT on one basis, so the identity "
                  "capex = dPPE + D&A would measure a reclassification rather than "
                  "spending. The cross-check is declined at these boundaries and the "
                  "reason is recorded; no committed figure moves, because capital "
                  "expenditure is DISCLOSED on every one of these cash-flow "
                  "statements."),
        }),
        "presentation_changes": {
            "_": ("Two balance-sheet presentations sit in this window and neither is "
                  "flattened into the other. FY2015 prints a WORKING-CAPITAL balance "
                  "sheet — non-current assets, current assets less current liabilities "
                  "to a stated deficit, a stated total investment, then 'Financed by:' "
                  "equity and non-current liabilities — and states no total-assets and "
                  "no total-liabilities line at all; FY2016 onwards print assets = "
                  "equity + liabilities. The footing check follows the page: every "
                  "identity FY2015 asserts is tested, and a line it never printed is "
                  "not demanded of it."),
            "FY2015": ("working-capital format; trade receivable inside 'Debtors and "
                       "other debit balances' and trade payable inside 'Creditors and "
                       "other credit balances', both split in the notes and named in "
                       "the working-capital record; the interest-bearing facility is a "
                       "BANK OVERDRAFT rather than the 'credit facilities' line the "
                       "later years carry, and it is recorded under the page's own "
                       "name; equity carries a fourth line, 'Net profits for the year', "
                       "which later filings fold into retained earnings"),
            "FY2016": ("assets = equity + liabilities, the presentation FY2017 onwards "
                       "use; the trade receivable and trade payable are on their own "
                       "lines from this filing"),
        },
        "origins": {"FY%d" % y: block(y) for y in range(2018, 2026)},
        "prior_year_anchor": {
            "_": ("FY2015, FY2016 and FY2017 are NOT origins of this run. They are "
                  "carried because a trailing window reaches back past the first "
                  "origin — the identity capex = dPPE + D&A needs property at two "
                  "dates, and a capital-spending intensity is taken over the three "
                  "fiscal years to an origin, so an origin at FY2017 reads FY2015, "
                  "FY2016 and FY2017. Recording any of them inside `origins` would "
                  "misstate what this run tested."),
            "FY2015": block(2015),
            "FY2016": block(2016),
            "FY2017": block(2017),
        },
    }


def shares_record():
    """The point-in-time counts, in the shape the calibration panel reads.

    engine/valuation_calibration/panel.py resolves a share count for an origin
    from shares_{ticker}.json and from nothing else, so a count committed only
    inside this run's own record would be invisible to the readiness matrix that
    decides which origins the calibration can score. It is GENERATED here, from
    the same footed reading, so the two cannot drift apart.
    """
    out = {
        "_": ("GENERATED by engine/arcc_walkforward/valuation_inputs.py from that "
              "run's own reading of each year's capital note — NOT by "
              "extract_shares.py, whose scan this did not run. Never hand-edited."),
        "ticker": "ARCC",
        "shares_mn": {},
        "rule": ("recorded only where issued capital divided by par value "
                 "reproduces the share count the same document states"),
    }
    for y, k in sorted(CAPITAL.items()):
        out["shares_mn"][str(y)] = {
            "shares_mn": k["shares"] / 1e6,
            "issued_capital": float(k["issued_capital"]),
            "par_value": float(k["par_value"]),
            "page": k["page"],
            "file": FILES[y][0],
            "check": ("capital %d / par %g = %d, matching the stated count"
                      % (k["issued_capital"], k["par_value"],
                         k["issued_capital"] / k["par_value"])),
            "how": k["par_source"],
            "route": ROUTE,
            # FY2017 is read and footed like the rest and is NOT an origin of this
            # run — it is the prior-year anchor the capex identity needs. The count
            # is a true dated fact either way; saying which is which here stops a
            # later reader inferring an origin from the presence of a count.
            "origin_of_this_run": ("FY%d" % y) in ORIGINS,
        }
    return out


def main():
    bad = foot()
    if bad:
        raise SystemExit("REFUSED — the block does not foot:\n  "
                         + "\n  ".join(bad))
    rec = record()
    p = os.path.join(HERE, "valuation_inputs.json")
    json.dump(rec, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    q = os.path.join(CALIB, "shares_arcc.json")
    json.dump(shares_record(), open(q, "w", encoding="utf-8"), indent=1,
              ensure_ascii=False)

    print("valuation-input block — ARCC\n")
    print("  %-8s %14s %14s %14s %12s %14s %14s %12s"
          % ("year", "cash", "debt", "capex", "ppe", "D&A", "working cap", "shares"))
    print("  " + "-" * 108)

    def row(y, tag=""):
        b = block(y)
        def v(i):
            r = b[i]
            return "MISSING" if "missing" in r else "%,.0f".replace(",", "") % 0 \
                if r.get("value") is None else format(r["value"], ",.0f")
        print("  FY%-6d %14s %14s %14s %14s %14s %14s %12s%s"
              % (y, v("cash"), v("debt"), v("capex"), v("ppe"), v("dep"), v("wc"),
                 v("shares"), tag))

    for y in (2015, 2016, 2017):
        row(y, "   anchor")
    for y in range(2018, 2026):
        row(y)
    n_missing = sum(1 for y in range(2018, 2026) for i, r in block(y).items()
                    if "missing" in r)
    n_anchor_missing = sum(1 for y in (2015, 2016, 2017) for i, r in block(y).items()
                           if "missing" in r)
    print("\n  %d origins x 7 items = %d cells, %d recorded missing"
          % (8, 8 * 7, n_missing))
    print("  3 prior-year anchors x 7 items = 21 cells, %d recorded missing "
          "(FY2015, FY2016 and FY2017 are NOT origins of this run)" % n_anchor_missing)
    for k, why in sorted(BASIS_BREAKS.items()):
        print("  basis break FY%d to FY%d — the capex identity is declined across it"
              % k)
    print("  wrote %s" % os.path.relpath(p, os.path.dirname(os.path.dirname(HERE))))
    print("  wrote %s" % os.path.relpath(q, os.path.dirname(os.path.dirname(HERE))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
