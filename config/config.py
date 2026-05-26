from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from autorotorb import AnalysisConfig, OrbitalRequest


# =============================================================================
# USER SETTINGS
# =============================================================================
# Edit this file to run AutoRotOrb (ARO) on an ORCA output file.
#
# ARO reads the Loewdin reduced orbital population table printed by ORCA,
# ranks molecular orbitals by selected atomic-orbital contributions, and
# suggests ORCA rotate commands when the current active-space window does not
# match the highest-ranked candidate orbitals.
#
# Atom labels must match the labels printed in the ORCA Loewdin table.
#
# You can also run from the command line:
#   python -m autorotorb -i data/your_job.out --active-electrons 11 \
#       --orbital-request 0 Er f 7
# =============================================================================

ANALYSIS_CONFIG = AnalysisConfig(
    output_file=PROJECT_ROOT / "data" / "minimal_orca.out",
    orbital_requests=[
        OrbitalRequest(
            atom_label="0",
            atom_symbol="Dy",
            orbital_type="f",
            number=3,
        ),
    ],
    active_electrons=8,
    wanted_spin="SPIN UP",
    population_round_digits=1,
    rotation_angle=90,
)

# Set to None to skip saving a text report.
REPORT_FILE = PROJECT_ROOT / "data" / "aro_report.txt"
