from __future__ import annotations

import unittest
import warnings
from pathlib import Path

from autorotorb import AnalysisConfig, OrbitalRequest, analyze_active_space

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "minimal_orca.out"


class TestAnalyzeActiveSpace(unittest.TestCase):
    def test_end_to_end_on_minimal_fixture(self) -> None:
        config = AnalysisConfig(
            output_file=FIXTURE,
            orbital_requests=[
                OrbitalRequest(atom_label="0", atom_symbol="Dy", orbital_type="f", number=3),
            ],
            active_electrons=4,
            wanted_spin="SPIN UP",
        )
        result = analyze_active_space(config)

        self.assertEqual(result.electron_space.total_electrons, 20)
        self.assertEqual(result.candidate_indexes, [6, 7, 8])
        self.assertEqual(result.active_space_indexes, [8, 9, 10])
        self.assertEqual(result.swaps, [(9, 6), (10, 7)])
        self.assertIn("rotate{ 9, 6, 90 } end", result.rotation_block)

    def test_warns_when_candidate_count_differs_from_active_space(self) -> None:
        config = AnalysisConfig(
            output_file=FIXTURE,
            orbital_requests=[
                OrbitalRequest(atom_label="0", atom_symbol="Dy", orbital_type="f", number=1),
                OrbitalRequest(atom_label="0", atom_symbol="Dy", orbital_type="f", number=1),
            ],
            active_electrons=4,
            wanted_spin="SPIN UP",
        )
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            with self.assertRaises(ValueError):
                analyze_active_space(config)

        self.assertTrue(
            any("differs from the active-space size" in str(item.message) for item in caught)
        )


if __name__ == "__main__":
    unittest.main()
