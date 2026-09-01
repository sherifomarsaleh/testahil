"""EGCH — the build, in the ONE order its dependencies allow.

Running these by hand in the wrong order is how a document ends up quoting a lens value
that its own workbook no longer holds: alternatives.py reads lenses.json, figures.py
reads alternatives.json, and both documents read all three. The order is the contract.
"""
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
STAGES = ["beta_record.py", "wacc.py", "inputs.py", "compute.py", "lenses.py", "experts.py", "alternatives.py",
          "sensitivity.py", "flat_rate_ladder.py", "figures.py", "build_xlsx.py", "docx_egch.py",
          "docx_biblio.py", "recalc.py", "formula_audit.py", "cross_check.py", "driver_test.py", "qc_checks.py", "attest.py"]
only = sys.argv[1:] or STAGES
for stage in only:
    print(f"\n=== {stage} " + "=" * (66 - len(stage)))
    r = subprocess.run([sys.executable, os.path.join(HERE, stage)], cwd=HERE)
    if r.returncode:
        sys.exit(f"BUILD STOPPED AT {stage} (exit {r.returncode})")
print("\nall stages completed")
