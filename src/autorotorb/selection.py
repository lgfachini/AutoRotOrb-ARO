from __future__ import annotations

from typing import Iterable, List

from .config import OrbitalRequest
from .models import OrbitalPopulationMap


def round_populations(
    populations: OrbitalPopulationMap,
    digits: int = 1,
) -> OrbitalPopulationMap:
    """Round orbital population values for reporting and ranking."""
    return {key: round(value, digits) for key, value in populations.items()}


def rank_populations(populations: OrbitalPopulationMap) -> OrbitalPopulationMap:
    """Sort orbital populations from highest to lowest contribution."""
    return dict(sorted(populations.items(), key=lambda item: item[1], reverse=True))


def select_candidate_orbitals(
    ranked_populations: OrbitalPopulationMap,
    orbital_requests: Iterable[OrbitalRequest],
    max_orbital_index: int,
) -> OrbitalPopulationMap:
    """Select top candidate orbitals according to requested atom/orbital types."""
    candidates: OrbitalPopulationMap = {}

    for request in orbital_requests:
        matching = {
            key: value
            for key, value in ranked_populations.items()
            if key[0] == request.atom_label
            and key[1] == request.atom_symbol
            and key[2] == request.orbital_type
            and key[3] <= max_orbital_index
        }

        top = dict(
            sorted(matching.items(), key=lambda item: item[1], reverse=True)[
                : request.number
            ]
        )
        candidates.update(top)

    return candidates


def unique_sorted_indexes(populations: OrbitalPopulationMap) -> List[int]:
    """Extract unique molecular-orbital indices from a population map."""
    return sorted({key[3] for key in populations})
