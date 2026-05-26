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

    def __post_init__(self) -> None:
        if not str(self.atom_label).strip():
            raise ValueError("atom_label must be non-empty.")
        if not str(self.atom_symbol).strip():
            raise ValueError("atom_symbol must be non-empty.")
        if not str(self.orbital_type).strip():
            raise ValueError("orbital_type must be non-empty.")
        if self.number <= 0:
            raise ValueError("number must be a positive integer.")


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

    def __post_init__(self) -> None:
        object.__setattr__(self, "output_file", Path(self.output_file))

        requests = tuple(self.orbital_requests)
        if not requests:
            raise ValueError("orbital_requests must contain at least one OrbitalRequest.")
        object.__setattr__(self, "orbital_requests", requests)

        if self.active_electrons <= 0:
            raise ValueError("active_electrons must be a positive integer.")

        if self.population_round_digits < 0:
            raise ValueError("population_round_digits must be zero or greater.")

        if self.max_orbital_index is not None and self.max_orbital_index < 0:
            raise ValueError("max_orbital_index must be zero or greater when set.")

        if self.rotation_angle == 0:
            raise ValueError("rotation_angle must be non-zero.")

        from .parser import normalize_spin_label

        normalize_spin_label(self.wanted_spin)
