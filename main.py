from __future__ import annotations

from pathlib import Path

from autorotorb import AnalysisConfig, OrbitalRequest, analyze_active_space
from autorotorb.reporting import print_result, save_result


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

DEFAULT_OUTPUT = Path("data/minimal_orca.out")


def main() -> None:
    config = AnalysisConfig(
        output_file=DEFAULT_OUTPUT,
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

    result = analyze_active_space(config)
    print_result(result)
    save_result(result, Path("data/aro_report.txt"))


if __name__ == "__main__":
    main()
