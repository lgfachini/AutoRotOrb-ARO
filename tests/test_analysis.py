from __future__ import annotations

from pathlib import Path
import unittest

from autorotorb import AnalysisConfig, OrbitalRequest, analyze_active_space
from autorotorb.rotation import build_rotation_block, suggest_swaps


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "minimal_orca.out"


class AnalysisTests(unittest.TestCase):
    def test_analyze_active_space_with_minimal_fixture(self) -> None:
        config = AnalysisConfig(
            output_file=FIXTURE,
            orbital_requests=[OrbitalRequest("0", "Dy", "f", 3)],
            active_electrons=8,
            wanted_spin="SPIN UP",
        )

        result = analyze_active_space(config)

        self.assertEqual(result.active_space_indexes, [6, 7, 8])
        self.assertEqual(result.candidate_indexes, [6, 7, 8])
        self.assertEqual(result.swaps, [])
        self.assertEqual(
            result.rotation_block,
            "# The active space does not need further rotations.",
        )

    def test_suggest_swaps_pairs_indexes_in_order(self) -> None:
        self.assertEqual(suggest_swaps([6, 7, 8], [5, 7, 9]), [(6, 5), (8, 9)])

    def test_suggest_swaps_rejects_unbalanced_candidates(self) -> None:
        with self.assertRaisesRegex(ValueError, "Cannot pair"):
            suggest_swaps([6, 7, 8], [6, 7])

    def test_build_rotation_block_formats_orca_block(self) -> None:
        self.assertEqual(
            build_rotation_block([(6, 5)], angle=90),
            "%scf\nrotate{ 6, 5, 90 } end\nend",
        )


if __name__ == "__main__":
    unittest.main()
