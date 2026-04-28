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
# =============================================================================


def main() -> None:
    config = AnalysisConfig(
        # ORCA output file to analyze.
        output_file=Path("data/Er1Ti9.out"),

        # Atom/orbital contributions to track.
        orbital_requests=[
            OrbitalRequest(
                atom_label="0",
                atom_symbol="Er",
                orbital_type="f",
                number=7,
            ),
        ],

        # Number of active electrons in the intended active space.
        active_electrons=11,

        # Spin block to analyze: "SPIN UP", "SPIN DOWN", or None.
        wanted_spin="SPIN UP",

        # Optional upper index for candidate orbitals. None uses the active-space upper limit.
        max_orbital_index=None,

        # Decimal places used when ranking reported populations.
        population_round_digits=1,

        # Rotation angle used in generated ORCA rotate commands.
        rotation_angle=90,
    )

    result = analyze_active_space(config)
    print_result(result)

    # Optional text report.
    save_result(result, Path("data/aro_report.txt"))


if __name__ == "__main__":
    main()
