"""EGCH — the build, in the ONE order its dependencies allow.

Running these by hand in the wrong order is how a document ends up quoting a lens value
that its own workbook no longer holds: alternatives.py reads lenses.json, figures.py
reads alternatives.json, and both documents read all three. The order is the contract.

AND A STAGE LEFT OUT OF THIS LIST NEVER RUNS AT ALL. diagnostics_egch.py, which writes
contested_judgements.json and diagnostics.json, was missing until 5 September 2026, so
those two artefacts went on declaring a central three corrections old while every stage
listed here rebuilt cleanly. check_artefact_currency caught it, which is what that gate is
for [R-ENF-06]: an artefact every builder reads and this list does not write is a number
frozen at the date somebody last ran it by hand.
"""
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
STAGES = ["beta_record.py", "inputs.py", "compute.py", "lenses.py", "experts.py", "alternatives.py",
          "sensitivity.py", "diagnostics_egch.py", "flat_rate_ladder.py", "band_record.py", "figures.py", "build_xlsx.py", "docx_egch.py",
          "docx_biblio.py", "recalc.py", "formula_audit.py", "cross_check.py", "prose_check.py", "driver_test.py", "qc_checks.py", "attest.py"]
only = sys.argv[1:] or STAGES
for stage in only:
    print(f"\n=== {stage} " + "=" * (66 - len(stage)))
    r = subprocess.run([sys.executable, os.path.join(HERE, stage)], cwd=HERE)
    if r.returncode:
        sys.exit(f"BUILD STOPPED AT {stage} (exit {r.returncode})")
print("\nall stages completed")
