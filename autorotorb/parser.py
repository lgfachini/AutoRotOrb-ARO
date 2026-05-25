from __future__ import annotations

import re
from typing import Iterable, Optional

from .config import OrbitalRequest
from .models import ElectronSpace, OrbitalPopulationMap

NEL_PATTERN = "Number of Electrons    NEL             ...."
LOEWDIN_HEADER = "LOEWDIN REDUCED ORBITAL POPULATIONS PER MO"
SPIN_UP = "SPIN UP"
SPIN_DOWN = "SPIN DOWN"

# ORCA prints six MO columns per row. The first data row uses MO indices 0–5,
# the next row block 6–11, and so on. The dashed separator advances the base
# index by six; the initial base is -6 so the first separator yields base 0.
ORCA_COLUMNS_PER_ROW = 6
ORCA_INITIAL_MO_OFFSET = -ORCA_COLUMNS_PER_ROW


def normalize_spin_label(spin: Optional[str]) -> Optional[str]:
    """Normalize a spin label to ORCA's printed convention."""
    if spin is None:
        return None

    value = spin.strip().upper()

    if value in {"SPIN UP", "UP", "ALPHA"}:
        return SPIN_UP

    if value in {"SPIN DOWN", "DOWN", "BETA"}:
        return SPIN_DOWN

    raise ValueError("wanted_spin must be 'SPIN UP', 'SPIN DOWN', or None.")


def parse_total_electrons(lines: Iterable[str]) -> int:
    """Extract the total number of electrons from an ORCA output file."""
    for line in lines:
        if NEL_PATTERN in line:
            return int(line.split()[-1])

    raise ValueError("Could not find total number of electrons (NEL).")


def compute_electron_space(
    total_electrons: int,
    active_electrons: int,
    active_orbitals: int,
) -> ElectronSpace:
    """
    Infer inactive and active orbital index limits.

    The indexing follows the logic of the original ARO script:
    inactive_last = ((NEL - active_electrons) / 2) - 1
    active_start  = inactive_last + 1
    active_end    = inactive_last + active_orbitals
    """
    if active_orbitals <= 0:
        raise ValueError("active_orbitals must be a positive integer.")

    inactive_electrons = total_electrons - active_electrons

    if inactive_electrons < 0:
        raise ValueError("active_electrons cannot exceed total_electrons.")

    if inactive_electrons % 2 != 0:
        raise ValueError("NEL - active_electrons must be even.")

    inactive_last = int(inactive_electrons / 2) - 1
    active_start = inactive_last + 1
    active_end = inactive_last + active_orbitals

    return ElectronSpace(
        total_electrons=total_electrons,
        inactive_orbitals_last_index=inactive_last,
        active_space_start_index=active_start,
        active_space_end_index=active_end,
    )


def orbital_line_pattern(request: OrbitalRequest) -> re.Pattern[str]:
    """Build a regular expression matching one Loewdin population row."""
    return re.compile(
        rf"\s*{re.escape(request.atom_label)}\s+"
        rf"{re.escape(request.atom_symbol)}\s+"
        rf"{re.escape(request.orbital_type)}[-\d]*\s*"
    )


def parse_orca_output(
    lines: Iterable[str],
    orbital_requests: Iterable[OrbitalRequest],
    wanted_spin: Optional[str] = "SPIN UP",
) -> OrbitalPopulationMap:
    """
    Parse ORCA Loewdin reduced orbital populations per molecular orbital.

    When the output contains multiple Loewdin tables, only the last table is
    used. Contributions are accumulated across spin blocks when wanted_spin
    is None.
    """
    wanted_spin = normalize_spin_label(wanted_spin)
    requests = tuple(orbital_requests)
    patterns = {request: orbital_line_pattern(request) for request in requests}

    loewdin_section = False
    current_spin: Optional[str] = None
    orbital_index_offset = ORCA_INITIAL_MO_OFFSET
    populations: OrbitalPopulationMap = {}

    for line in lines:
        if LOEWDIN_HEADER in line:
            if loewdin_section:
                populations.clear()
            loewdin_section = True
            current_spin = None
            orbital_index_offset = ORCA_INITIAL_MO_OFFSET
            continue

        if not loewdin_section:
            continue

        if SPIN_UP in line:
            current_spin = SPIN_UP
            orbital_index_offset = ORCA_INITIAL_MO_OFFSET
            continue

        if SPIN_DOWN in line:
            current_spin = SPIN_DOWN
            orbital_index_offset = ORCA_INITIAL_MO_OFFSET
            continue

        if wanted_spin is not None and current_spin != wanted_spin:
            continue

        if " -------- " in line:
            orbital_index_offset += ORCA_COLUMNS_PER_ROW
            continue

        for request in requests:
            if not patterns[request].match(line):
                continue

            parts = line.split()
            if len(parts) <= 3:
                continue

            try:
                values = [float(value) for value in parts[3:]]
            except ValueError:
                continue

            for column_index, value in enumerate(values):
                mo_index = orbital_index_offset + column_index
                key = (
                    request.atom_label,
                    request.atom_symbol,
                    request.orbital_type,
                    mo_index,
                )
                populations[key] = populations.get(key, 0.0) + value

    return populations
