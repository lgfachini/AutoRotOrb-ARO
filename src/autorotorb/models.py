from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

OrbitalKey = Tuple[str, str, str, int]
OrbitalPopulationMap = Dict[OrbitalKey, float]


@dataclass(frozen=True)
class ElectronSpace:
    """Electron-count-derived orbital-space information."""

    total_electrons: int
    inactive_orbitals_last_index: int
    active_space_start_index: int
    active_space_end_index: int


@dataclass(frozen=True)
class AnalysisResult:
    """Complete output of an AutoRotOrb analysis."""

    electron_space: ElectronSpace
    ranked_populations: OrbitalPopulationMap
    candidate_orbitals: OrbitalPopulationMap
    candidate_indexes: List[int]
    active_space_indexes: List[int]
    swaps: List[Tuple[int, int]]
    rotation_block: str
