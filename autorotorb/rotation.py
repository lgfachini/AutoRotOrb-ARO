from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple


def suggest_swaps(
    active_space_indexes: Sequence[int],
    candidate_indexes: Sequence[int],
) -> List[Tuple[int, int]]:
    """
    Suggest orbital swaps required to bring candidate orbitals into the active window.

    Returns pairs:
        (active_orbital_to_replace, candidate_orbital_to_add)
    """
    active_set = set(active_space_indexes)
    candidate_set = set(candidate_indexes)

    to_replace = sorted(active_set - candidate_set)
    to_add = sorted(candidate_set - active_set)

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
