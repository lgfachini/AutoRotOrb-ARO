from pathlib import Path

from autorotorb import AnalysisConfig, OrbitalRequest, analyze_active_space
from autorotorb.reporting import print_result

FIXTURE = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "minimal_orca.out"

config = AnalysisConfig(
    output_file=FIXTURE,
    orbital_requests=[
        OrbitalRequest(atom_label="0", atom_symbol="Dy", orbital_type="f", number=3),
    ],
    active_electrons=4,
    wanted_spin="SPIN UP",
)

result = analyze_active_space(config)
print_result(result)
