import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from autorotorb import AnalysisConfig, OrbitalRequest, analyze_active_space
from autorotorb.reporting import print_result

FIXTURE = PROJECT_ROOT / "data" / "minimal_orca.out"

config = AnalysisConfig(
    output_file=FIXTURE,
    orbital_requests=[
        OrbitalRequest(atom_label="0", atom_symbol="Dy", orbital_type="f", number=3),
    ],
    active_electrons=8,
    wanted_spin="SPIN UP",
)

result = analyze_active_space(config)
print_result(result)
