from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence


@dataclass(frozen=True)
class OrbitalRequest:
    """
    Atom/orbital contribution to track in the ORCA Loewdin table.

    atom_label:
        Atom label/index exactly as printed by ORCA.
    atom_symbol:
        Chemical symbol exactly as printed by ORCA.
    orbital_type:
        Orbital shell/type, such as "d" or "f".
    number:
        Number of orbitals of this atom/shell type to select.
    """

    atom_label: str
    atom_symbol: str
    orbital_type: str
    number: int


@dataclass(frozen=True)
class AnalysisConfig:
    """
    User-facing configuration for one AutoRotOrb analysis.

    output_file:
        ORCA output file.
    orbital_requests:
        Atom/orbital contributions to rank.
    active_electrons:
        Number of active electrons in the intended active space.
    wanted_spin:
        "SPIN UP", "SPIN DOWN", or None to accumulate all spin blocks.
    max_orbital_index:
        Optional upper index for candidate orbitals.
    population_round_digits:
        Decimal places used when ranking contributions.
    rotation_angle:
        Angle used in generated ORCA rotate commands.
    """

    output_file: Path
    orbital_requests: Sequence[OrbitalRequest]
    active_electrons: int
    wanted_spin: Optional[str] = "SPIN UP"
    max_orbital_index: Optional[int] = None
    population_round_digits: int = 1
    rotation_angle: int = 90
