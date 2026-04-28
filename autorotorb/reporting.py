from __future__ import annotations

from pathlib import Path
from typing import Optional

from .models import AnalysisResult


def format_result(result: AnalysisResult) -> str:
    """Format an AnalysisResult as a human-readable report."""
    lines = []

    lines.append("AutoRotOrb (ARO) active-space analysis")
    lines.append("=" * 80)
    lines.append("")
    lines.append("Electron-space summary")
    lines.append("-" * 80)
    lines.append(f"Total electrons: {result.electron_space.total_electrons}")
    lines.append(
        "Last inactive orbital index: "
        f"{result.electron_space.inactive_orbitals_last_index}"
    )
    lines.append(
        "Active-space index range: "
        f"{result.electron_space.active_space_start_index} - "
        f"{result.electron_space.active_space_end_index}"
    )
    lines.append("")

    lines.append("Candidate orbitals")
    lines.append("-" * 80)

    if result.candidate_orbitals:
        for key, value in result.candidate_orbitals.items():
            atom_label, atom_symbol, orbital_type, mo_index = key
            lines.append(
                f"MO {mo_index:5d} | atom {atom_label:>4s} {atom_symbol:<3s} "
                f"{orbital_type:<3s} | contribution = {value}"
            )
    else:
        lines.append("No candidate orbitals were selected.")

    lines.append("")
    lines.append(f"Candidate indexes: {result.candidate_indexes}")
    lines.append(f"Current active-space indexes: {result.active_space_indexes}")
    lines.append("")
    lines.append("Suggested ORCA rotation block")
    lines.append("-" * 80)
    lines.append(result.rotation_block)
    lines.append("")

    return "\n".join(lines)


def print_result(result: AnalysisResult) -> None:
    """Print a formatted analysis result."""
    print(format_result(result))


def save_result(result: AnalysisResult, output_file: Optional[Path]) -> None:
    """Save a formatted report if output_file is provided."""
    if output_file is None:
        return

    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(format_result(result), encoding="utf-8")
