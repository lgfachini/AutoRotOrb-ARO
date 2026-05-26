from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple


def suggest_swaps(
    active_space_indexes: Sequence[int],
    candidate_indexes: Sequence[int],
) -> List[Tuple[int, int]]:
    """
    Suggest orbital swaps required to bring candidate orbitals into the active window.

    Pairing is by ascending MO index: the lowest active orbital to replace is
    matched with the lowest candidate orbital to add.

    Returns pairs:
        (active_orbital_to_replace, candidate_orbital_to_add)
    """
    active_set = set(active_space_indexes)
    candidate_set = set(candidate_indexes)

    to_replace = sorted(active_set - candidate_set)
    to_add = sorted(candidate_set - active_set)

    if len(to_replace) != len(to_add):
        raise ValueError(
            "Cannot pair active-space and candidate orbitals for rotation: "
            f"{len(to_replace)} orbital(s) to replace "
            f"{to_replace}, but {len(to_add)} candidate orbital(s) to add "
            f"{to_add}. Check active_electrons, orbital request counts, and "
            "max_orbital_index."
        )

    return list(zip(to_replace, to_add))


def build_rotation_block(
    swaps: Iterable[Tuple[int, int]],
    angle: int = 90,
) -> str:
    """Build an ORCA %scf rotate block from suggested swaps."""
    swaps = list(swaps)

    if not swaps:
        return "# The active space does not need further rotations."

    lines = ["%scf"]
    for active_index, candidate_index in swaps:
        lines.append(f"rotate{{ {active_index}, {candidate_index}, {angle} }} end")
    lines.append("end")

    return "\n".join(lines)
