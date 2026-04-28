from __future__ import annotations

from .config import AnalysisConfig
from .io_utils import read_text_lines
from .models import AnalysisResult
from .parser import compute_electron_space, parse_orca_output, parse_total_electrons
from .rotation import build_rotation_block, suggest_swaps
from .selection import (
    rank_populations,
    round_populations,
    select_candidate_orbitals,
    unique_sorted_indexes,
)


def analyze_active_space(config: AnalysisConfig) -> AnalysisResult:
    """Run the complete AutoRotOrb active-space analysis."""
    lines = read_text_lines(config.output_file)

    active_orbitals = sum(request.number for request in config.orbital_requests)
    total_electrons = parse_total_electrons(lines)

    electron_space = compute_electron_space(
        total_electrons=total_electrons,
        active_electrons=config.active_electrons,
        active_orbitals=active_orbitals,
    )

    raw_populations = parse_orca_output(
        lines=lines,
        orbital_requests=config.orbital_requests,
        wanted_spin=config.wanted_spin,
    )

    ranked_populations = rank_populations(
        round_populations(raw_populations, config.population_round_digits)
    )

    max_index = (
        config.max_orbital_index
        if config.max_orbital_index is not None
        else electron_space.active_space_end_index
    )

    candidate_orbitals = select_candidate_orbitals(
        ranked_populations=ranked_populations,
        orbital_requests=config.orbital_requests,
        max_orbital_index=max_index,
    )

    candidate_indexes = unique_sorted_indexes(candidate_orbitals)

    active_space_indexes = list(
        range(
            electron_space.active_space_start_index,
            electron_space.active_space_end_index + 1,
        )
    )

    swaps = suggest_swaps(active_space_indexes, candidate_indexes)
    rotation_block = build_rotation_block(swaps, config.rotation_angle)

    return AnalysisResult(
        electron_space=electron_space,
        ranked_populations=ranked_populations,
        candidate_orbitals=candidate_orbitals,
        candidate_indexes=candidate_indexes,
        active_space_indexes=active_space_indexes,
        swaps=swaps,
        rotation_block=rotation_block,
    )
