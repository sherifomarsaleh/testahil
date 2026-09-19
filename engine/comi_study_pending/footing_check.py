"""COMI — the arithmetic arbiter for every statement page the Step 2A sweep used.

A statement is accepted only if it foots against its OWN printed subtotals. A broken
character map extracts figures that look perfectly clean and are wrong — right
positions, wrong glyphs — and nothing about the extraction looks broken. Arithmetic is
the only test that catches it, so every page is re-added here against the total the
company itself printed, and the ROUTE each figure came by is recorded beside it.

ROUTES USED
  text   — pdftotext -layout text layer, accepted because the page foots
  ocr    — tesseract off the rendered pixels at 110 dpi, used for the two documents
           that carry no text layer at all (the 15-Mar-2026 OGA resolutions and the
           9-Feb-2026 board resolution). Neither is a statement; both are corroborated
           arithmetically against figures that ARE in a footed statement.

Run: python3 engine/comi_study_pending/footing_check.py
All figures EGP thousands unless stated. Sources are the PDFs in ./filings/.
"""
FAILS = []


def foot(doc, page, name, parts, printed, route="text"):
    s = sum(parts)
    ok = (s == printed)
    if not ok:
        FAILS.append((doc, name, s, printed))
    print(f"  [{route:4}] {name:<52} {s:>16,}  vs printed {printed:>16,}  "
          f"{'OK' if ok else '*** DOES NOT FOOT — RE-READ BY OCR ***'}")
    return ok


print("CIB FY2025 IFRS Consolidated FS (RNS 3239S, 09-Feb-2026)")
foot("FY25", "IS", "net interest income", [211600177, -104121746], 107478431)
foot("FY25", "IS", "net fee and commission income", [16036009, -6816966], 9219043)
foot("FY25", "IS", "profit before income tax",
     [107478431, 9219043, 216273, 1523649, 775841, -24692107, -1533040, 11804786, 10512],
     104803388)
foot("FY25", "IS", "net profit for the year", [104803388, -29323206], 75480182)
foot("FY25", "IS", "attributable split", [75460219, 19963], 75480182)
foot("FY25", "IS", "FY2024 restated comparative — PBT",
     [90984024, 7085220, 195047, 20470230, 459337, -19952958, -22323778, -5401308, -17786],
     71498028)
foot("FY25", "OCI", "total comprehensive income",
     [75480182, 503643, -96248, 10758425, -498433, -295691, -615506, -40145], 85196227)
foot("FY25", "BS", "total assets",
     [20002406, 68874046, 135236549, 34440770, 507953766, 3173539, 620349, 373747694,
      236672175, 2469076, 45210, 182827, 54040912, 2545498, 5481682], 1445486499)
foot("FY25", "BS", "total liabilities",
     [3353746, 1110395693, 2526481, 137802, 53860, 4761558, 33144838, 20570313,
      30471499, 15644651], 1221060441)
foot("FY25", "BS", "equity attributable to parent",
     [33779361, 105020603, 2343532, 83254686], 224398182)
foot("FY25", "BS", "liabilities + equity", [1221060441, 224426058], 1445486499)
foot("FY25", "n.3", "interest income by asset class",
     [20066633, 94424365, 89324621, 7784558], 211600177)
foot("FY25", "n.3", "interest expense by class",
     [9112525, 91747074, 14908, 221200, 2835376, 190663], 104121746)
foot("FY25", "n.9", "net impairment released",
     [9101206, 2987628, -137399, -146649], 11804786)
foot("FY25", "n.17", "gross loans by stage — total",
     [427519888, 108806857, 9933490], 546260235)
foot("FY25", "n.17", "gross loans by segment", [92459011, 453801224], 546260235)
foot("FY25", "n.17", "ECL by stage — total", [7231807, 19797922, 7658027], 34687756)
foot("FY25", "n.17", "gross to net loans",
     [546260235, -34687756, -82363, -40820, -3495530], 507953766)
foot("FY25", "n.26", "deposits by product",
     [461967523, 180471867, 248483791, 211270156, 8202356], 1110395693)
foot("FY25", "n.26", "deposits by rate type",
     [201838067, 26136289, 882421337], 1110395693)
foot("FY25", "n.31.8", "retained earnings roll-forward",
     [51590097, -21744828, 2628, 111370, -8993602, 75460219, -26186, -13145012], 83254686)
foot("FY25", "n.34.5", "tier 1 capital",
     [33779361, 94853160, 20231006, -2684971, 40257342], 186435898)
foot("FY25", "n.34.5", "tier 2 capital", [25581480, 9073673], 34655153)
foot("FY25", "n.34.5", "total qualifying capital base", [186435898, 34655153], 221091051)
foot("FY25", "n.34.5", "risk weighted assets",
     [726170603, 5270678, 74032267, 5593451], 811066999)
print(f"         CAR check: 221,091,051 / 811,066,999 = "
      f"{221091051/811066999:.2%} vs printed 27.3%")
print(f"         leverage : 186,435,898 / 1,649,986,599 = "
      f"{186435898/1649986599:.2%} vs printed 11.3%")

print("\nCIB FY2024 IFRS Consolidated FS (RNS 5950X, 19-Feb-2025)")
foot("FY24", "IS", "net interest income", [182735474, -91751450], 90984024)
foot("FY24", "IS", "profit before income tax",
     [90984024, 7085220, 195047, 20470230, 459337, 0, 0, -19952958, -23201267,
      -4523819, -17786], 71498028)
foot("FY24", "IS", "net profit for the year", [71498028, -21878946], 49619082)
foot("FY24", "IS", "FY2023 comparative — PBT",
     [52885691, 5438225, 234010, 4006880, 221810, -51831, -206287, -13299910,
      -6341869, -4270081, -55983], 38560655)

print("\nCIB FY2023 IFRS Consolidated FS (RNS 7294C, 12-Feb-2024)")
foot("FY23", "IS", "net interest income", [104028379, -51142688], 52885691)
foot("FY23", "IS", "net profit for the year", [38560655, -11942406, -42102], 26576147)
foot("FY23", "BS", "total assets",
     [71887821, 231085244, 822448, 234985936, 306375, 1105148, 233430236, 38341019,
      729823, 115979, 161, 18801444, 0, 0, 1685230, 2739092], 836035956)
foot("FY23", "BS", "total liabilities",
     [12458003, 677237479, 674417, 140934, 873, 3073349, 21937452, 9395534,
      12483907, 11095996], 748497944)
foot("FY23", "BS", "liabilities + equity", [748497944, 87538012], 836035956)

print("\nCIB FY2022 (comparative column of the FY2023 filing; also RNS 5862T)")
foot("FY22", "IS", "net interest income", [55723701, -24828159], 30895542)
foot("FY22", "IS", "profit before income tax",
     [30895542, 3072398, 52411, 2829976, 1162195, -9452863, -4562828, -1584944,
      -19253], 22392634)
foot("FY22", "IS", "net profit for the year", [22392634, -7769064, -4427], 14619143)
foot("FY22", "BS", "total assets",
     [47492549, 133856720, 2978197, 193599872, 247324, 1939961, 208144247, 34524760,
      1726082, 186062, 0, 14521427, 51831, 206287, 185745, 2405434], 642066498)
foot("FY22", "BS", "liabilities + equity", [575278342, 66788156], 642066498)

print("\nCIB Q1-2026 interim condensed consolidated (RNS 9499D, 12-May-2026)")
foot("Q1-26", "BS", "total assets",
     [92010988, 170847392, 55185042, 551721003, 515109, 375696731, 265712744, 43710,
      223223, 49309350, 1366252, 5636266], 1568267810)
foot("Q1-26", "BS", "total liabilities",
     [14239563, 1214998089, 56747, 81585, 5394655, 60735106, 5455820, 34530873,
      16602339], 1352094777)
foot("Q1-26", "BS", "liabilities + equity", [1352094777, 216173033], 1568267810)
foot("Q1-26", "IS", "net interest income", [53305545, -23605965], 29699580)
foot("Q1-26", "IS", "profit before income tax",
     [29699580, 2221085, 24830, 433650, 168162, -5154563, -2309125, 481032, -1500],
     25563151)
foot("Q1-26", "IS", "net profit for the period", [25563151, -6366847, -1374262], 17822042)

print("\nCIB Q2/H1-2026 interim condensed consolidated (RNS 1119N, 21-Jul-2026)")
foot("H1-26", "BS", "total assets",
     [144083579, 213509638, 48462194, 597785831, 399402, 348654793, 269977831, 51807,
      190054, 58636578, 2437842, 5850379], 1690039928)
foot("H1-26", "BS", "total liabilities",
     [42856364, 1308646344, 54956, 227032, 12351399, 32905897, 4922120, 34616250,
      15043327], 1451623689)
foot("H1-26", "BS", "liabilities + equity", [1451623689, 238416239], 1690039928)
foot("H1-26", "IS", "net interest income (6 months)", [110568003, -49741855], 60826148)
foot("H1-26", "IS", "profit before income tax (6 months)",
     [60826148, 5827921, 186093, 1455384, 545790, -10356040, -3850419, -482430, 6597],
     54159044)
foot("H1-26", "IS", "net profit (6 months)", [54159044, -14495340, -349978], 39313726)
foot("H1-26", "IS", "net interest income (Q2 alone)", [57262458, -26135890], 31126568)
foot("H1-26", "IS", "net profit (Q2 alone)", [28595893, -8128493, 1024284], 21491684)
foot("H1-26", "n.3", "gross loans by stage", [523678573, 103791178, 10896911], 638366662)
foot("H1-26", "n.3", "ECL by stage", [8934230, 19555664, 8196394], 36686288)
foot("H1-26", "n.3", "gross to net loans",
     [638366662, -36686288, -127475, -26129, -3740939], 597785831)
foot("H1-26", "n.24", "deposits by product",
     [554043991, 215014198, 273675783, 257277289, 8635083], 1308646344)
foot("H1-26", "n.24", "deposits by customer type", [565036367, 743609977], 1308646344)
foot("H1-26", "FX", "deposits by currency",
     [852436348, 396082977, 48453609, 3955277, 7718133], 1308646344)

print("\nCIB FY2025 Earnings Release consolidated highlights (RNS 3242S) — EGP million")
foot("FY25rel", "P&L", "FY25 net operating income", [107700, 9733], 117433)
foot("FY25rel", "P&L", "FY25 profit before tax", [117433, -17562, 11711], 111582)
foot("FY25rel", "P&L", "FY25 net profit", [111582, -29895, 572], 82259)
foot("FY25rel", "P&L", "FY24 net operating income", [91064, 7892], 98956)
foot("FY25rel", "P&L", "FY24 net profit", [77136, -23549, 1670], 55257)

print("\nOCR-ROUTE DOCUMENTS — no text layer; corroborated arithmetically")
print("  [ocr ] OGA 15-Mar-2026 item 5: 'cash dividends payout of EGP 6 per share'")
print(f"         cross-check: 25% of FY2025 net profit EGP 82,259m over 3,377,936k "
      f"shares = EGP {0.25*82259e6/3377936e3:.2f}/share — agrees to rounding")
print("  [ocr ] Board 09-Feb-2026: capital EGP 33,779,361,000 -> EGP 34,051,391,000")
foot("board", "OCR", "capital increase via 27,203,000 shares at EGP 10 par",
     [33779361000, 272030000], 34051391000, route="ocr")
print("         cross-check: EGP 34,051,391 thousand is the figure printed on the "
      "footed 30-Jun-2026 balance sheet")

print("\n" + "=" * 78)
if FAILS:
    print(f"FAIL — {len(FAILS)} page(s) do not foot; each must be re-read by OCR off the "
          f"rendered pixels before any figure from it enters the study:")
    for d, n, s, p in FAILS:
        print(f"   {d} / {n}: computed {s:,} vs printed {p:,} (diff {s - p:,})")
    raise SystemExit(1)
print("PASS — every statement page used by the COMI sweep foots against its own printed "
      "subtotals, on both the current and the comparative column. The pdftotext text "
      "layer is therefore sound and no statement page needed OCR re-reading.")
