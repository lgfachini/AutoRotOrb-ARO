from __future__ import annotations

import unittest

from autorotorb.config import OrbitalRequest
from autorotorb.parser import (
    compute_electron_space,
    normalize_spin_label,
    parse_orca_output,
    parse_total_electrons,
)


class ParserTests(unittest.TestCase):
    def test_parse_total_electrons_accepts_variable_spacing(self) -> None:
        lines = ["Number   of   Electrons   NEL   ....      20\n"]

        self.assertEqual(parse_total_electrons(lines), 20)

    def test_compute_electron_space_uses_zero_based_orbital_indexes(self) -> None:
        space = compute_electron_space(
            total_electrons=20,
            active_electrons=8,
            active_orbitals=3,
        )

        self.assertEqual(space.inactive_orbitals_last_index, 5)
        self.assertEqual(space.active_space_start_index, 6)
        self.assertEqual(space.active_space_end_index, 8)

    def test_compute_electron_space_rejects_odd_inactive_electron_count(self) -> None:
        with self.assertRaisesRegex(ValueError, "must be even"):
            compute_electron_space(
                total_electrons=20,
                active_electrons=7,
                active_orbitals=3,
            )

    def test_normalize_spin_label_accepts_aliases(self) -> None:
        self.assertEqual(normalize_spin_label("alpha"), "SPIN UP")
        self.assertEqual(normalize_spin_label("beta"), "SPIN DOWN")
        self.assertIsNone(normalize_spin_label(None))

    def test_parse_orca_output_reads_requested_spin_block(self) -> None:
        request = OrbitalRequest("0", "Dy", "f", 2)
        lines = [
            "LOEWDIN REDUCED ORBITAL POPULATIONS PER MO\n",
            "SPIN UP\n",
            " -------- -------- -------- -------- -------- --------\n",
            "     0 Dy f 1.0 2.0 3.0 4.0 5.0 6.0\n",
            "SPIN DOWN\n",
            " -------- -------- -------- -------- -------- --------\n",
            "     0 Dy f 10.0 20.0 30.0 40.0 50.0 60.0\n",
        ]

        populations = parse_orca_output(lines, [request], wanted_spin="SPIN DOWN")

        self.assertEqual(populations[("0", "Dy", "f", 0)], 10.0)
        self.assertEqual(populations[("0", "Dy", "f", 5)], 60.0)

    def test_parse_orca_output_reads_restricted_table_without_spin_header(self) -> None:
        request = OrbitalRequest("0", "Dy", "f", 2)
        lines = [
            "LOEWDIN REDUCED ORBITAL POPULATIONS PER MO\n",
            " -------- -------- -------- -------- -------- --------\n",
            "     0 Dy f 1.0 2.0 3.0 4.0 5.0 6.0\n",
        ]

        populations = parse_orca_output(lines, [request], wanted_spin="SPIN UP")

        self.assertEqual(populations[("0", "Dy", "f", 0)], 1.0)
        self.assertEqual(populations[("0", "Dy", "f", 5)], 6.0)

    def test_parse_orca_output_uses_last_loewdin_table(self) -> None:
        request = OrbitalRequest("0", "Dy", "f", 2)
        lines = [
            "LOEWDIN REDUCED ORBITAL POPULATIONS PER MO\n",
            " -------- -------- -------- -------- -------- --------\n",
            "     0 Dy f 1.0 2.0 3.0 4.0 5.0 6.0\n",
            "LOEWDIN REDUCED ORBITAL POPULATIONS PER MO\n",
            " -------- -------- -------- -------- -------- --------\n",
            "     0 Dy f 10.0 20.0 30.0 40.0 50.0 60.0\n",
        ]

        populations = parse_orca_output(lines, [request], wanted_spin=None)

        self.assertEqual(populations[("0", "Dy", "f", 0)], 10.0)


if __name__ == "__main__":
    unittest.main()
