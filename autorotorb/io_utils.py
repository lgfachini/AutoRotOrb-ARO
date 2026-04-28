from __future__ import annotations

from pathlib import Path
from typing import List


def read_text_lines(file_path: Path) -> List[str]:
    """Read a text file and return its lines."""
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path.is_file():
        raise IsADirectoryError(f"Expected a file, got directory: {file_path}")

    with file_path.open("r", encoding="utf-8", errors="replace") as handle:
        return handle.readlines()
