from pathlib import Path

from autorotorb import AnalysisConfig, OrbitalRequest, analyze_active_space
from autorotorb.reporting import print_result


config = AnalysisConfig(
    output_file=Path("data/example.out"),
    orbital_requests=[
        OrbitalRequest(atom_label="0", atom_symbol="Dy", orbital_type="f", number=7),
    ],
    active_electrons=9,
    wanted_spin="SPIN UP",
)

result = analyze_active_space(config)
print_result(result)
