from __future__ import annotations

import unittest

from autorotorb.models import AnalysisResult, ElectronSpace
from autorotorb.reporting import format_result, sorted_candidate_items


class TestReporting(unittest.TestCase):
    def test_sorted_candidate_items_orders_by_contribution(self) -> None:
        candidates = {
            ("0", "Dy", "f", 6): 70.0,
            ("0", "Dy", "f", 8): 90.0,
            ("0", "Dy", "f", 7): 80.0,
        }
        ordered = list(sorted_candidate_items(candidates))
        self.assertEqual([key[3] for key, _ in ordered], [8, 7, 6])

    def test_format_result_lists_candidates_by_contribution(self) -> None:
        result = AnalysisResult(
            electron_space=ElectronSpace(20, 7, 8, 10),
            ranked_populations={},
            candidate_orbitals={
                ("0", "Dy", "f", 6): 70.0,
                ("0", "Dy", "f", 8): 90.0,
                ("0", "Dy", "f", 7): 80.0,
            },
            candidate_indexes=[6, 7, 8],
            active_space_indexes=[8, 9, 10],
            swaps=[(9, 6), (10, 7)],
            rotation_block="%scf",
        )
        report = format_result(result)
        self.assertLess(report.index("MO     8"), report.index("MO     7"))
        self.assertLess(report.index("MO     7"), report.index("MO     6"))


if __name__ == "__main__":
    unittest.main()
