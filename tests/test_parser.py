from __future__ import annotations

import unittest
from pathlib import Path

from autorotorb.config import OrbitalRequest
from autorotorb.parser import (
    ORCA_COLUMNS_PER_ROW,
    ORCA_INITIAL_MO_OFFSET,
    compute_electron_space,
    parse_orca_output,
    parse_total_electrons,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"
REQUEST = OrbitalRequest(atom_label="0", atom_symbol="Dy", orbital_type="f", number=3)


class TestParseTotalElectrons(unittest.TestCase):
    def test_reads_nel_from_fixture(self) -> None:
        lines = (FIXTURES / "minimal_orca.out").read_text(encoding="utf-8").splitlines(
            keepends=True
        )
        self.assertEqual(parse_total_electrons(lines), 20)


class TestComputeElectronSpace(unittest.TestCase):
    def test_active_window(self) -> None:
        space = compute_electron_space(
            total_electrons=20,
            active_electrons=4,
            active_orbitals=3,
        )
        self.assertEqual(space.inactive_orbitals_last_index, 7)
        self.assertEqual(space.active_space_start_index, 8)
        self.assertEqual(space.active_space_end_index, 10)

    def test_rejects_odd_inactive_electron_count(self) -> None:
        with self.assertRaises(ValueError):
            compute_electron_space(
                total_electrons=21,
                active_electrons=4,
                active_orbitals=3,
            )


class TestParseOrcaOutput(unittest.TestCase):
    def test_maps_mo_indices_from_orca_columns(self) -> None:
        lines = [
            "LOEWDIN REDUCED ORBITAL POPULATIONS PER MO\n",
            "SPIN UP\n",
            " -------- -------- -------- -------- -------- --------\n",
            "         0    Dy    f       0.0    0.0    0.0    0.0    0.0    0.0\n",
            " -------- -------- -------- -------- -------- --------\n",
            "         0    Dy    f       0.0    0.0    5.5    0.0    0.0    0.0\n",
        ]
        populations = parse_orca_output(lines, [REQUEST], wanted_spin="SPIN UP")
        self.assertEqual(populations[("0", "Dy", "f", 8)], 5.5)

    def test_uses_last_loewdin_block_only(self) -> None:
        lines = (FIXTURES / "multi_loewdin_orca.out").read_text(
            encoding="utf-8"
        ).splitlines(keepends=True)
        populations = parse_orca_output(lines, [REQUEST], wanted_spin="SPIN UP")
        self.assertEqual(populations[("0", "Dy", "f", 8)], 1.0)
        self.assertEqual(populations.get(("0", "Dy", "f", 6), 0.0), 0.0)

    def test_orca_index_constants(self) -> None:
        self.assertEqual(ORCA_INITIAL_MO_OFFSET, -6)
        self.assertEqual(ORCA_COLUMNS_PER_ROW, 6)


if __name__ == "__main__":
    unittest.main()
