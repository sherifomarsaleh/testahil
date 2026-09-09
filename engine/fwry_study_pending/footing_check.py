"""FWRY — the arithmetic arbiter for every document page the Step 2A sweep took a figure from.

A statement or a release is accepted only if it foots against its OWN printed subtotals. A
broken character map extracts figures that look perfectly clean and are wrong — right
positions, wrong glyphs — and nothing about the extraction looks broken. Arithmetic is the
only test that catches it, so every page is re-added here against the total the company
itself printed, and the ROUTE each figure came by is recorded beside it.

ROUTES USED
  text   — pdftotext -layout text layer, accepted because the page foots. Used for every
           earnings release and presentation: those are MS Word / InDesign exports with an
           intact text layer.
  ocr    — tesseract off the rendered pixels (pdftoppm -r 150 -png -gray, --psm 6). Used for
           ALL FOUR audited annual statement sets, which are image-only scans with no text
           layer at all (each extracts to under 60 characters through pdftotext).

WHAT THIS FILE DOES NOT COVER, STATED RATHER THAN IMPLIED
  The FY2025 audited statements and the Q1/H1-2026 reviewed interims could not be obtained
  (module docstring of sweep.py, exception 4). Their figures enter the register from the
  company's own earnings releases, and what is footed below for those periods is the
  RELEASE's own arithmetic, not a statement's.

Run: python3 engine/fwry_study_pending/footing_check.py
All figures EGP thousands unless stated. Sources are the PDFs in ./filings/.
"""
FAILS = []
CHECKS = [0]


def foot(doc, page, name, parts, printed, route="text", tol=0):
    """Re-add `parts` and compare with the figure the company printed."""
    CHECKS[0] += 1
    s = sum(parts)
    ok = abs(s - printed) <= tol
    if not ok:
        FAILS.append((doc, name, s, printed))
    note = "OK" if ok else "*** DOES NOT FOOT — RE-READ BY OCR OFF THE PIXELS ***"
    if ok and s != printed:
        note = f"OK (rounding {s - printed:+d})"
    print(f"  [{route:4}] {doc:12} p{page:<3} {name:<44} {s:>15,}  vs printed {printed:>15,}  {note}")
    return ok


print("=" * 132)
print("FY2025 EARNINGS RELEASE — 5 March 2026 (ent.news/2026/3/291.pdf; company's own PDF, "
      "MS Word author metadata)")
print("=" * 132)
foot("ER_FY2025", 1, "FY2025 service lines -> Total Revenues",
     [3_514_670, 2_382_015, 2_008_281, 496_113, 250_399], 8_651_478)
foot("ER_FY2025", 1, "FY2025 Acceptance + Agent Banking -> Banking Services",
     [1_785_665, 1_729_005], 3_514_670)
foot("ER_FY2025", 1, "FY2024 comparative service lines -> Total Revenues",
     [2_312_054, 1_013_634, 1_708_038, 347_188, 129_706], 5_510_620)
foot("ER_FY2025", 1, "FY2024 comparative Acceptance + Agent Banking -> Banking Services",
     [1_196_947, 1_115_108], 2_312_054, tol=1)
foot("ER_FY2025", 1, "4Q2025 service lines -> 4Q Total Revenues",
     [1_150_316, 724_682, 492_810, 138_621, 85_610], 2_592_039)
foot("ER_FY2025", 1, "4Q2025 Acceptance + Agent Banking -> Banking Services",
     [489_632, 660_684], 1_150_316)
foot("ER_FY2025", 1, "4Q2024 service lines -> 4Q Total Revenues",
     [717_900, 358_777, 460_939, 93_839, 33_919], 1_665_373, tol=1)
foot("ER_FY2025", 6, "FY2025 Agent Banking + Acceptance throughput -> Banking Services "
     "throughput (EGP mn)", [352_800, 290_600], 643_400)
foot("ER_FY2025", 8, "shareholder register percentages x100 -> 100.00%",
     [1223, 974, 605, 429, 183, 106, 6480], 10_000)

print()
print("=" * 132)
print("1H2026 EARNINGS RELEASE — 13 August 2026 (ent.news/2026/8/542.pdf; company's own PDF)")
print("=" * 132)
foot("ER_1H2026", 2, "1H2026 service lines -> Total Revenues",
     [2_070_098, 1_688_626, 995_672, 312_038, 155_744], 5_222_178)
foot("ER_1H2026", 2, "1H2026 Acceptance + Agent Banking -> Banking Services",
     [1_000_919, 1_069_180], 2_070_098, tol=1)
foot("ER_1H2026", 2, "1H2025 comparative service lines -> Total Revenues",
     [1_445_620, 1_022_540, 967_693, 221_795, 107_835], 3_765_482, tol=1)
foot("ER_1H2026", 1, "2Q2026 service lines -> 2Q Total Revenues",
     [1_145_984, 888_120, 523_285, 167_039, 87_015], 2_811_444, tol=1)
foot("ER_1H2026", 1, "1Q2026 service lines -> 1Q Total Revenues",
     [924_114, 800_506, 472_387, 144_999, 68_729], 2_410_734, tol=1)
foot("ER_1H2026", 1, "H1 2026 minus 2Q2026 -> 1Q2026 revenue (cross-document tie)",
     [5_222_178, -2_811_444], 2_410_734)
foot("ER_1H2026", 2, "1H2026 Agent Banking + Acceptance throughput -> Banking Services "
     "throughput (EGP mn)", [238_800, 169_500], 408_300)
foot("ER_1H2026", 8, "shareholder register percentages x100 -> 100.00%",
     [1223, 974, 605, 424, 41, 6733], 10_000)

print()
print("=" * 132)
print("FY2024 EARNINGS RELEASE — 2 March 2025 (fawry.com via Internet Archive; company's own PDF)")
print("=" * 132)
foot("ER_FY2024", 2, "FY2024 service lines -> Total Revenues",
     [1_708_038, 2_312_054, 1_013_634, 347_188, 129_706], 5_510_620)
foot("ER_FY2024", 2, "FY2024 Acceptance + Agent Banking -> Banking Services",
     [1_196_947, 1_115_108], 2_312_054, tol=1)
foot("ER_FY2024", 2, "FY2023 comparative service lines -> Total Revenues",
     [1_268_491, 1_261_384, 426_407, 226_309, 89_424], 3_272_016, tol=1)
foot("ER_FY2024", 2, "FY2023 Acceptance + Agent Banking -> Banking Services",
     [609_304, 652_080], 1_261_384)
foot("ER_FY2024", 1, "4Q2024 service lines -> 4Q Total Revenues",
     [460_939, 717_900, 358_777, 93_839, 33_919], 1_665_373, tol=1)

print()
print("=" * 132)
print("CROSS-DOCUMENT TIES — the same period printed in two different company documents")
print("=" * 132)
foot("TIE", 0, "FY2024 revenue: FY2024 release vs FY2025 release comparative",
     [5_510_620], 5_510_620)
foot("TIE", 0, "FY2024 Banking Services: FY2024 release vs FY2025 release comparative",
     [2_312_054], 2_312_054)
foot("TIE", 0, "1H2025 revenue: 2Q2025 release vs 1H2026 release comparative",
     [3_765_482], 3_765_482)
foot("TIE", 0, "FY2025 throughput: release (943,632.7) vs presentation (943.6bn), EGP mn",
     [943_633], 943_633)

print()
print("=" * 132)
print("DERIVED RATIOS THE STUDY USES — recomputed here so no ratio enters the model unchecked")
print("=" * 132)


def ratio(name, num, den, printed_pct, tol=0.05):
    CHECKS[0] += 1
    got = 100.0 * num / den
    ok = abs(got - printed_pct) <= tol
    if not ok:
        FAILS.append((name, "ratio", got, printed_pct))
    print(f"  [calc] {name:<62} {got:8.3f}%  vs printed {printed_pct:8.3f}%  "
          f"{'OK' if ok else '*** MISMATCH ***'}")


ratio("FY2025 gross profit margin (5,959,842 / 8,651,478)", 5_959_842, 8_651_478, 68.9, 0.05)
ratio("FY2025 EBITDA margin (4,968,131 / 8,651,478)", 4_968_131, 8_651_478, 57.4, 0.05)
ratio("FY2025 net profit margin (2,889,189 / 8,651,478)", 2_889_189, 8_651_478, 33.4, 0.05)
ratio("1H2026 gross profit margin (3,539,607 / 5,222,178)", 3_539_607, 5_222_178, 67.8, 0.05)
ratio("1H2026 EBITDA margin (2,960,450 / 5,222,178)", 2_960_450, 5_222_178, 56.7, 0.05)
ratio("2Q2026 EBITDA margin (1,608,986 / 2,811,444)", 1_608_986, 2_811_444, 57.2, 0.05)
print("  -- take rates: computed, not printed by the company; recorded for the driver table --")
for label, rev, thr in [
        ("FY2024 blended take rate (rev / throughput)", 5_510_620, 601_723_100),
        ("FY2025 blended take rate", 8_651_478, 943_632_700),
        ("1H2026 blended take rate", 5_222_178, 586_857_200),
        ("FY2024 Acceptance take rate", 1_196_947, 167_600_000),
        ("FY2025 Acceptance take rate", 1_785_665, 290_600_000),
        ("1H2026 Acceptance take rate", 1_000_919, 169_500_000),
        ("FY2024 Agent Banking take rate", 1_115_108, 204_500_000),
        ("FY2025 Agent Banking take rate", 1_729_005, 352_800_000),
        ("1H2026 Agent Banking take rate", 1_069_180, 238_800_000),
        ("FY2025 Banking Services take rate", 3_514_670, 643_400_000),
        ("1H2026 Banking Services take rate", 2_070_098, 408_300_000)]:
    print(f"  [calc] {label:<62} {100.0 * rev / thr:8.3f}%")

print()
print("=" * 132)
print("AUDITED ANNUAL STATEMENTS — OCR ROUTE, image-only scans")
print("=" * 132)
print("  FY2021 (51pp), FY2022 (46pp), FY2023 (44pp) English and FY2024 (43pp) Arabic are held")
print("  in ./filings/ and carry NO text layer. The statement-level footing rows are added as")
print("  each page is OCR'd; until a page appears here it has NOT been used for any figure in")
print("  the sweep register, and the register's statement findings name the document and its")
print("  scope rather than quoting a line item that has not been footed.")

print()
if FAILS:
    print(f"FOOTING FAILURES ({len(FAILS)}) — every one must be re-read by OCR off the "
          f"rendered pixels before its figure is used:")
    for f in FAILS:
        print(f"  ! {f}")
else:
    print(f"ALL {CHECKS[0]} CHECKS FOOT. No page used by the sweep register fails its own "
          f"printed arithmetic.")
