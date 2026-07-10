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
    COMPANY_OFFICIAL = "COMPANY_OFFICIAL"      # audited FS / annual report / company IR / exchange filing portal
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


@dataclass
class DriverGateRow:
    driver: str                      # e.g. "PC volumes (units)", "EBITDA margin glide"
    mode: DriverMode
    justification: str
    sweep_refs: list[str] = field(default_factory=list)   # fids that justify the mode


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
    _n: int = 0

    # ---- recording ----------------------------------------------------------
    def add(self, ring: Ring, category: str, klass: FindingClass, headline: str,
            source_name: str, source_type: SourceType, source_date: str,
            detail: str = "", url: str = "", model_impact: str = "",
            is_fs_data: bool = False) -> str:
        self._n += 1
        fid = f"F{self._n:02d}"
        self.findings.append(Finding(fid, ring, category, klass, headline,
                                     source_name, source_type, source_date,
                                     detail, url, model_impact, is_fs_data))
        return fid

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
        if warnings:
            line += f" | warnings: {len(warnings)}"
        return line

    def register_rows(self) -> list[list[str]]:
        """Appendix B Sweep Register — Word-ready rows (header included)."""
        rows = [["#", "Ring", "Category", "Class", "Finding", "Source", "Date"]]
        order = {r: i for i, r in enumerate(RINGS[self.asset_class])}
        for f in sorted(self.findings, key=lambda x: (order.get(x.ring, 99), x.fid)):
            rows.append([f.fid, f.ring.value.title(), f.category,
                         f.klass.name, f.headline, f.source_name, f.source_date])
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
    fB = reg2.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
                  "Ras-El-Hekma-linked land monetisation resets recognised-revenue base",
                  "PHDC IR release", SourceType.COMPANY_OFFICIAL, "2026-05-14",
                  model_impact="FY26 revenue base: explicit dated event, dual-framed")
    fFS = reg2.add(Ring.COMPANY, "official financial statements", FindingClass.D,
                   "FY25 audited FS disclose launches, deliveries and backlog by project",
                   "PHDC FY25 audited FS", SourceType.COMPANY_OFFICIAL, "2026-03-30",
                   model_impact="unlocks bottom-up collections schedule", is_fs_data=True)
    for ring in RINGS[AssetClass.STOCK]:
        for cat in MANDATORY[ring]:
            if not any(f.ring is ring and f.category == cat for f in reg2.findings):
                reg2.add_negative(ring, cat, f"query set for '{cat}'", "2026-07-10")
    nSGA = [f.fid for f in reg2.findings
            if f.ring is Ring.COMPANY and f.category == "regular disclosures"][0]
    reg2.add_driver("Collections schedule (per-project)", DriverMode.BOTTOM_UP,
                    "backlog + delivery schedule disclosed in FY25 FS", [fFS, fB])
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
