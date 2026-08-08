"""
research_sweep.py — Step 2A Information Sweep: register + enforcement.
Intended repo path: engine/research_sweep.py

House rule (Standing_Research_Protocol.md, Step 2A, adopted 10-Jul-2026):
before any forecast driver is set, run an exhaustive ring-by-ring information
sweep on the ticker. This module does NOT perform the searching — the analyst
does, at study time. It is the evidence-forcing scaffold, in the same mold as
wacc_builder.py's RegressionBetaAttempt gate: it makes the sweep recordable,
classifiable and consequential, and it FAILS the build rather than defaulting
when the record is incomplete.

Enforced invariants
  1. COVERAGE  — every mandatory category of every ring for the asset class is
     closed by >= 1 finding. A dated NEGATIVE search counts as closure; silence
     never does.
  2. PROVENANCE — any finding carrying a financial-statement line item
     (is_fs_data=True) must be sourced COMPANY_OFFICIAL. Aggregators are never
     a financial-statement source (market data only).
  3. CONSEQUENCE — every B / S / D finding must name its model impact (the base
     or driver it touches). B events are modeled explicitly and dual-framed,
     never smoothed into a growth glide.
  4. GATE LINKAGE — the per-driver gate table must exist; every TOP_DOWN driver
     must cite the negative search that justifies it; every BOTTOM_UP driver
     must cite the company-official disclosure or D-finding that unlocked it.
  5. PRIMARY ACCESS [ADDED 07-Aug-2026, per instruction — ARCC study] — at
     least one `record_primary_access` call must exist: an attempt at the
     company's own official website/IR page, logged whether it succeeded or
     was blocked (real case: arabiancementcompany.com returned
     connect_rejected at this environment's proxy). Never silently skipped.
  6. FS DEPTH [ADDED 07-Aug-2026] — findings carrying is_fs_data=True and a
     `fiscal_period` tagged as a full year (e.g. "FY2024") must span >= 2
     distinct fiscal years (hard FAIL below that) with a warning below 4 (the
     target, not the floor) — per Standing_Research_Protocol.md's PRIMARY-
     SOURCE FINANCIAL RESEARCH procedure.
  7. STUDY-YEAR QUARTER COVERAGE [ADDED 07-Aug-2026] — if
     `declare_study_year` was called, every quarter it lists as already
     disclosed must have >= 1 finding tagged with that `fiscal_period` in the
     sweep, so the study year's actuals are swept in BEFORE the build rather
     than discovered after (ARCC's own Q1-2026 actual sat unswept until a
     user asked about it).
  8. IR COVERAGE [ADDED 07-Aug-2026] — at least one finding sourced
     SourceType.COMPANY_IR: an investor-relations presentation or
     investor/earnings-call transcript, kept distinct from COMPANY_OFFICIAL
     (audited statements/annual report/filing portal) so a reviewer can see
     how much of the Company ring rests on the company's own primary IR
     channel specifically, not just "some company source."

Outputs: JSON (ships with the study files), Word-ready Sweep Register rows
(Appendix B), per-driver gate rows (§1.6), and the QC item (m) verdict line.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import date
from enum import Enum


# ----------------------------------------------------------------------------
# Taxonomy
# ----------------------------------------------------------------------------
class AssetClass(Enum):
    STOCK = "STOCK"
    METAL = "METAL"


class Ring(Enum):
    # equity rings (outside-in)
    GLOBAL = "GLOBAL"
    COUNTRY = "COUNTRY"
    INDUSTRY = "INDUSTRY"
    COMPANY = "COMPANY"
    # metal rings
    GLOBAL_MACRO = "GLOBAL_MACRO"
    SUPPLY = "SUPPLY"
    DEMAND = "DEMAND"
    MARKET_STRUCTURE = "MARKET_STRUCTURE"


class FindingClass(Enum):
    B = "BASE_CHANGER"        # resets the roll-forward base; explicit dual-framed event
    S = "STRUCTURAL"          # breaks a forward driver assumption; re-set or sensitize
    D = "DRIVER_UNLOCK"       # new disclosure converts top-down -> bottom-up
    C = "COLOR"               # context only; changes no number
    NEG = "NEGATIVE_SEARCH"   # category searched, nothing found (dated)


class SourceType(Enum):
    COMPANY_OFFICIAL = "COMPANY_OFFICIAL"      # audited FS / annual report / exchange filing portal
    COMPANY_IR = "COMPANY_IR"                  # [ADDED 07-Aug-2026] IR presentations, investor/earnings
                                                # calls, webcast decks — kept distinct from
                                                # COMPANY_OFFICIAL so the register shows how much of the
                                                # Company ring rests on the primary IR channel specifically
                                                # (volumes, per-unit prices, utilisation, segment splits —
                                                # data that never appears in a financial statement at all)
    REGULATOR_OFFICIAL = "REGULATOR_OFFICIAL"  # CB, regulator, ministry, WGC/USGS/LBMA/CFTC etc.
    PRIMARY_MARKET_DATA = "PRIMARY_MARKET_DATA"  # exchange quotes, bond yields, FX
    REPUTABLE_PRESS = "REPUTABLE_PRESS"
    AGGREGATOR = "AGGREGATOR"                  # investing.com, TradingEconomics, ... market data ONLY
    SEARCH = "SEARCH"                          # provenance of a negative search itself


RINGS: dict[AssetClass, list[Ring]] = {
    AssetClass.STOCK: [Ring.GLOBAL, Ring.COUNTRY, Ring.INDUSTRY, Ring.COMPANY],
    AssetClass.METAL: [Ring.GLOBAL_MACRO, Ring.SUPPLY, Ring.DEMAND, Ring.MARKET_STRUCTURE],
}

# Mandatory categories per ring — each must be closed by a finding or a dated
# negative search. Extra findings under free-form categories are welcome; they
# simply don't count toward coverage.
MANDATORY: dict[Ring, list[str]] = {
    Ring.GLOBAL: [
        "rate cycle & USD/FX regime",
        "commodity complex (input/output)",
        "global sector demand",
        "trade / sanctions / supply chains",
    ],
    Ring.COUNTRY: [
        "sovereign macro (inflation, policy rate, FX/deval risk)",
        "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
        "fiscal / political events with sector read-through",
    ],
    Ring.INDUSTRY: [
        "demand drivers & capacity/supply balance",
        "pricing",
        "new entrants (named-competitor level)",
        "technology substitution",
        "competitor capacity / price moves (named)",
    ],
    Ring.COMPANY: [
        "strategic plans & guidance",
        "regular disclosures",
        "IR communications (calls, presentations, releases)",
        "one-off base-resetting transactions",
        "ownership / stake changes (named-transaction rule)",
        "management & capital actions",
        "official financial statements",
    ],
    Ring.GLOBAL_MACRO: [
        "real rates & USD",
        "central-bank policy path",
        "official-sector behavior",
    ],
    Ring.SUPPLY: ["mine production", "recycling", "disruptions"],
    Ring.DEMAND: [
        "industrial demand",
        "jewelry / consumer demand",
        "investment / ETF flows",
        "official-sector purchases",
    ],
    Ring.MARKET_STRUCTURE: [
        "positioning (COT)",
        "forward curve / lease rates",
        "regulatory treatment (e.g. Basel III)",
    ],
}


class DriverMode(Enum):
    BOTTOM_UP = "BOTTOM_UP"
    TOP_DOWN = "TOP_DOWN"


# ----------------------------------------------------------------------------
# Records
# ----------------------------------------------------------------------------
@dataclass
class Finding:
    fid: str
    ring: Ring
    category: str
    klass: FindingClass
    headline: str
    source_name: str
    source_type: SourceType
    source_date: str                 # ISO yyyy-mm-dd — the source's own date
    detail: str = ""
    url: str = ""
    model_impact: str = ""           # REQUIRED for B/S/D: the base/driver touched + direction
    is_fs_data: bool = False         # True if the finding carries a financial-statement line item
    fiscal_period: str = ""          # [ADDED 07-Aug-2026] "FY2024" for a full year, "Q1-2026" for a
                                      # quarter — feeds the FS-depth and quarter-coverage invariants


@dataclass
class DriverGateRow:
    driver: str                      # e.g. "PC volumes (units)", "EBITDA margin glide"
    mode: DriverMode
    justification: str
    sweep_refs: list[str] = field(default_factory=list)   # fids that justify the mode


@dataclass
class PrimaryAccessAttempt:
    """[ADDED 07-Aug-2026] One attempt to reach the company's own official website/IR page,
    logged whether it succeeded or failed. Real case: arabiancementcompany.com returned
    connect_rejected at this environment's proxy — that is exactly what this record exists
    to make visible rather than silently falling back to a weaker secondary source."""
    url: str
    reachable: bool
    attempt_date: str
    note: str = ""


# ----------------------------------------------------------------------------
# Register
# ----------------------------------------------------------------------------
@dataclass
class SweepRegister:
    ticker: str
    asset_class: AssetClass
    sweep_date: str                  # ISO — the day the sweep was run
    findings: list[Finding] = field(default_factory=list)
    drivers: list[DriverGateRow] = field(default_factory=list)
    primary_access: list[PrimaryAccessAttempt] = field(default_factory=list)
    study_year: str = ""
    study_quarters_disclosed: list[str] = field(default_factory=list)
    _n: int = 0

    # ---- recording ----------------------------------------------------------
    def add(self, ring: Ring, category: str, klass: FindingClass, headline: str,
            source_name: str, source_type: SourceType, source_date: str,
            detail: str = "", url: str = "", model_impact: str = "",
            is_fs_data: bool = False, fiscal_period: str = "") -> str:
        self._n += 1
        fid = f"F{self._n:02d}"
        self.findings.append(Finding(fid, ring, category, klass, headline,
                                     source_name, source_type, source_date,
                                     detail, url, model_impact, is_fs_data,
                                     fiscal_period))
        return fid

    def record_primary_access(self, url: str, reachable: bool, attempt_date: str,
                              note: str = "") -> None:
        """[ADDED 07-Aug-2026] Log an attempt at the company's own official website/IR
        page — required before falling back to any aggregator or secondary source. Call
        this even when `reachable` is False; that is the case the invariant exists to
        surface, not to hide."""
        self.primary_access.append(PrimaryAccessAttempt(url, reachable, attempt_date, note))

    def declare_study_year(self, fiscal_year: str, quarters_disclosed: list[str]) -> None:
        """[ADDED 07-Aug-2026] State which quarters of the study's own fiscal year are
        already on the public record as of the sweep date, e.g. declare_study_year(
        "2026", ["Q1-2026"]). Each one then requires >= 1 finding tagged with that
        `fiscal_period` — the study year's own actuals must be swept in BEFORE the build,
        not discovered after."""
        self.study_year = fiscal_year
        self.study_quarters_disclosed = list(quarters_disclosed)

    def add_negative(self, ring: Ring, category: str, searched: str,
                     search_date: str) -> str:
        """Close a category with nothing found. `searched` = what was actually
        queried, so a later SF (sourcing-failure) review can audit the pattern."""
        return self.add(ring, category, FindingClass.NEG,
                        f"Negative search — nothing found ({searched})",
                        "negative search", SourceType.SEARCH, search_date)

    def add_driver(self, driver: str, mode: DriverMode, justification: str,
                   sweep_refs: list[str]) -> None:
        self.drivers.append(DriverGateRow(driver, mode, justification, list(sweep_refs)))

    # ---- enforcement --------------------------------------------------------
    def validate(self) -> tuple[list[str], list[str]]:
        """Return (errors, warnings). Any error = build FAIL (QC item m)."""
        errors: list[str] = []
        warnings: list[str] = []
        by_fid = {f.fid: f for f in self.findings}

        # 1. coverage — every mandatory category closed
        for ring in RINGS[self.asset_class]:
            for cat in MANDATORY[ring]:
                if not any(f.ring is ring and f.category == cat for f in self.findings):
                    errors.append(f"COVERAGE: {ring.value} / '{cat}' unclosed — "
                                  f"needs a finding or a dated negative search")

        # 2. provenance — FS line items company-official only
        for f in self.findings:
            if f.is_fs_data and f.source_type is not SourceType.COMPANY_OFFICIAL:
                errors.append(f"PROVENANCE: {f.fid} '{f.headline}' carries a "
                              f"financial-statement figure sourced {f.source_type.value} — "
                              f"FS data must be COMPANY_OFFICIAL")

        # 3. consequence — B/S/D must name the base/driver touched
        for f in self.findings:
            if f.klass in (FindingClass.B, FindingClass.S, FindingClass.D):
                if not f.model_impact.strip() or f.model_impact.strip().lower() == "none":
                    errors.append(f"CONSEQUENCE: {f.fid} ({f.klass.name}) "
                                  f"'{f.headline}' names no model impact")

        # 4. dating — every record dated
        for f in self.findings:
            if not f.source_date.strip():
                errors.append(f"DATING: {f.fid} '{f.headline}' has no source date")
            if not f.source_name.strip():
                errors.append(f"DATING: {f.fid} '{f.headline}' has no source name")

        # 5. driver gate table — must exist and be properly cited
        if not self.drivers:
            errors.append("GATE: per-driver gate table is empty — every major "
                          "driver needs a BOTTOM_UP/TOP_DOWN row citing the sweep")
        for d in self.drivers:
            refs = [by_fid.get(r) for r in d.sweep_refs]
            if not d.sweep_refs or any(r is None for r in refs):
                errors.append(f"GATE: driver '{d.driver}' cites missing/no sweep findings")
                continue
            if d.mode is DriverMode.TOP_DOWN:
                if not any(r.klass is FindingClass.NEG for r in refs):
                    errors.append(f"GATE: TOP_DOWN driver '{d.driver}' cites no "
                                  f"negative search — top-down must be evidenced "
                                  f"absence, not convenience")
            else:  # BOTTOM_UP
                if not any(r.klass is FindingClass.D or
                           r.source_type is SourceType.COMPANY_OFFICIAL for r in refs):
                    errors.append(f"GATE: BOTTOM_UP driver '{d.driver}' cites no "
                                  f"company-official disclosure or D-finding")

        # 5. primary access — the company's own site must have been attempted
        if not self.primary_access:
            errors.append("PRIMARY ACCESS: no record_primary_access() call — the "
                          "company's own website/IR page must be attempted and logged, "
                          "success or failure, before any secondary source is used")

        # 6. FS depth — >= 2 distinct full fiscal years (hard floor), 4 is the target
        fs_years = sorted({f.fiscal_period for f in self.findings
                           if f.is_fs_data and f.fiscal_period.startswith("FY")})
        if len(fs_years) < 2:
            errors.append(f"FS DEPTH: only {len(fs_years)} distinct fiscal year(s) "
                          f"{fs_years} carry is_fs_data — minimum 2 required "
                          f"(or state the shortfall explicitly if the company genuinely "
                          f"discloses fewer)")
        elif len(fs_years) < 4:
            warnings.append(f"FS DEPTH: {len(fs_years)} distinct fiscal years {fs_years} "
                            f"— target is 4; below target but above the floor")

        # 7. study-year quarter coverage — every declared quarter needs its own finding
        if self.study_quarters_disclosed:
            have = {f.fiscal_period for f in self.findings}
            missing = [q for q in self.study_quarters_disclosed if q not in have]
            if missing:
                errors.append(f"QUARTER COVERAGE: study year {self.study_year} declared "
                              f"{self.study_quarters_disclosed} disclosed but no finding "
                              f"is tagged {missing} — sweep every disclosed quarter "
                              f"BEFORE the build, not after")

        # 8. IR coverage — at least one finding sourced distinctly as investor relations
        if not any(f.source_type is SourceType.COMPANY_IR for f in self.findings):
            errors.append("IR COVERAGE: no finding sourced SourceType.COMPANY_IR — an "
                          "investor-relations presentation or call transcript is "
                          "mandatory, not optional, for volumes/prices/utilisation data "
                          "no financial statement carries")

        # warnings — non-fatal hygiene
        n_color = sum(1 for f in self.findings if f.klass is FindingClass.C)
        if n_color > 12:
            warnings.append(f"COLOR FLOOD: {n_color} C-findings — cap per protocol; "
                            f"trim to the ones worth a reader's minute")
        return errors, warnings

    def check_freshness(self, delivery_date: str, max_days: int = 14) -> str | None:
        """~10 trading days ≈ 14 calendar days. Returns a warning or None."""
        gap = (date.fromisoformat(delivery_date) - date.fromisoformat(self.sweep_date)).days
        if gap > max_days:
            return (f"FRESHNESS: {gap} calendar days between sweep ({self.sweep_date}) "
                    f"and delivery ({delivery_date}) — re-run the company ring")
        return None

    # ---- outputs -------------------------------------------------------------
    def counts(self) -> dict[str, int]:
        c = {k.name: 0 for k in FindingClass}
        for f in self.findings:
            c[f.klass.name] += 1
        return c

    def qc_line(self) -> str:
        errors, warnings = self.validate()
        c = self.counts()
        nbu = sum(1 for d in self.drivers if d.mode is DriverMode.BOTTOM_UP)
        ntd = len(self.drivers) - nbu
        verdict = "PASS" if not errors else f"FAIL ({len(errors)} errors)"
        line = (f"QC(m) — Information Sweep [{self.ticker}, {self.sweep_date}]: {verdict} — "
                f"{len(RINGS[self.asset_class])}/{len(RINGS[self.asset_class])} rings, "
                f"{len(self.findings)} findings "
                f"({c['B']} B · {c['S']} S · {c['D']} D · {c['C']} C · {c['NEG']} NEG), "
                f"driver gate {len(self.drivers)} rows ({nbu} bottom-up / {ntd} top-down)")
        fs_years = sorted({f.fiscal_period for f in self.findings
                           if f.is_fs_data and f.fiscal_period.startswith("FY")})
        n_ir = sum(1 for f in self.findings if f.source_type is SourceType.COMPANY_IR)
        access = ("attempted" if self.primary_access else "NOT ATTEMPTED")
        line += (f" | primary access: {access} ({len(self.primary_access)}) "
                 f"| FS years: {len(fs_years)} {fs_years} | IR findings: {n_ir}")
        if warnings:
            line += f" | warnings: {len(warnings)}"
        return line

    def register_rows(self) -> list[list[str]]:
        """Appendix B Sweep Register — Word-ready rows (header included)."""
        rows = [["#", "Ring", "Category", "Class", "Finding", "Source", "Period", "Date"]]
        order = {r: i for i, r in enumerate(RINGS[self.asset_class])}
        for f in sorted(self.findings, key=lambda x: (order.get(x.ring, 99), x.fid)):
            rows.append([f.fid, f.ring.value.title(), f.category,
                         f.klass.name, f.headline, f.source_name, f.fiscal_period,
                         f.source_date])
        return rows

    def driver_rows(self) -> list[list[str]]:
        """§1.6 per-driver gate table — Word-ready rows (header included)."""
        rows = [["Driver", "Mode", "Justification", "Sweep ref"]]
        for d in self.drivers:
            rows.append([d.driver, d.mode.value.replace("_", "-").lower(),
                         d.justification, ", ".join(d.sweep_refs)])
        return rows

    def to_json(self, path: str) -> None:
        out = dict(ticker=self.ticker, asset_class=self.asset_class.value,
                   sweep_date=self.sweep_date,
                   findings=[{**asdict(f), "ring": f.ring.value,
                              "klass": f.klass.value, "source_type": f.source_type.value}
                             for f in self.findings],
                   drivers=[{**asdict(d), "mode": d.mode.value} for d in self.drivers],
                   primary_access=[asdict(p) for p in self.primary_access],
                   study_year=self.study_year,
                   study_quarters_disclosed=self.study_quarters_disclosed,
                   qc_line=self.qc_line())
        with open(path, "w") as fh:
            json.dump(out, fh, indent=1)


# ----------------------------------------------------------------------------
# Self-test / demo — the two failure modes this module exists to catch
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    reg = SweepRegister("PHDC", AssetClass.STOCK, "2026-07-10")

    # -- deliberately broken register ----------------------------------------
    reg.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
            "Ras-El-Hekma-linked land monetisation resets recognised-revenue base",
            "PHDC IR release", SourceType.COMPANY_OFFICIAL, "2026-05-14",
            model_impact="FY26 revenue base +one-off tranche; model as explicit "
                         "dated event, headline dual-framed with/without")
    reg.add(Ring.COMPANY, "official financial statements", FindingClass.C,
            "FY25 revenue per investing.com",
            "investing.com", SourceType.AGGREGATOR, "2026-07-01",
            is_fs_data=True)   # <- PROVENANCE violation, on purpose
    # INDUSTRY 'technology substitution' left unclosed on purpose -> COVERAGE error
    errs, _ = reg.validate()
    print("== broken register ==")
    for e in [x for x in errs if not x.startswith("COVERAGE")] + errs[:3]:
        print("  ", e)
    print("   ...", len(errs), "errors total |", reg.qc_line(), "\n")

    # -- fixed register --------------------------------------------------------
    reg2 = SweepRegister("PHDC", AssetClass.STOCK, "2026-07-10")
    reg2.record_primary_access("https://phdc.com.eg/investor-relations", True, "2026-07-08")
    fB = reg2.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
                  "Ras-El-Hekma-linked land monetisation resets recognised-revenue base",
                  "PHDC IR release", SourceType.COMPANY_OFFICIAL, "2026-05-14",
                  model_impact="FY26 revenue base: explicit dated event, dual-framed")
    fFS = reg2.add(Ring.COMPANY, "official financial statements", FindingClass.D,
                   "FY25 audited FS disclose launches, deliveries and backlog by project",
                   "PHDC FY25 audited FS", SourceType.COMPANY_OFFICIAL, "2026-03-30",
                   model_impact="unlocks bottom-up collections schedule", is_fs_data=True,
                   fiscal_period="FY2025")
    reg2.add(Ring.COMPANY, "official financial statements", FindingClass.D,
             "FY24 audited FS — prior-year comparative", "PHDC FY24 audited FS",
             SourceType.COMPANY_OFFICIAL, "2025-03-28",
             model_impact="second historical year for the reconciliation table",
             is_fs_data=True, fiscal_period="FY2024")
    fIR = reg2.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
                   FindingClass.D, "Q1-2026 earnings call: delivery pace and pricing by phase",
                   "PHDC Q1-2026 investor call transcript", SourceType.COMPANY_IR,
                   "2026-05-12", model_impact="confirms Q1 delivery volumes against the "
                   "backlog schedule", fiscal_period="Q1-2026")
    reg2.declare_study_year("2026", ["Q1-2026"])
    for ring in RINGS[AssetClass.STOCK]:
        for cat in MANDATORY[ring]:
            if not any(f.ring is ring and f.category == cat for f in reg2.findings):
                reg2.add_negative(ring, cat, f"query set for '{cat}'", "2026-07-10")
    nSGA = [f.fid for f in reg2.findings
            if f.ring is Ring.COMPANY and f.category == "regular disclosures"][0]
    reg2.add_driver("Collections schedule (per-project)", DriverMode.BOTTOM_UP,
                    "backlog + delivery schedule disclosed in FY25 FS", [fFS, fB, fIR])
    reg2.add_driver("SG&A % of revenue", DriverMode.TOP_DOWN,
                    "no cost-line granularity disclosed; normalized glide", [nSGA])
    errs2, warns2 = reg2.validate()
    print("== fixed register ==")
    print("   errors:", errs2, "| warnings:", warns2)
    print("  ", reg2.qc_line())
    fresh = reg2.check_freshness("2026-08-05")
    print("   freshness check (delivery 05-Aug):", fresh)
    reg2.to_json("/tmp/sweep_PHDC.json")
    print("   register rows:", len(reg2.register_rows()) - 1,
          "| driver rows:", len(reg2.driver_rows()) - 1, "| JSON written")
