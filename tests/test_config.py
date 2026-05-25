from __future__ import annotations

import unittest
from pathlib import Path

from autorotorb.config import AnalysisConfig, OrbitalRequest


class TestAnalysisConfigValidation(unittest.TestCase):
    def test_rejects_empty_orbital_requests(self) -> None:
        with self.assertRaises(ValueError):
            AnalysisConfig(
                output_file=Path("missing.out"),
                orbital_requests=[],
                active_electrons=4,
            )

    def test_rejects_non_positive_active_electrons(self) -> None:
        with self.assertRaises(ValueError):
            AnalysisConfig(
                output_file=Path("missing.out"),
                orbital_requests=[
                    OrbitalRequest("0", "Dy", "f", 1),
                ],
                active_electrons=0,
            )

    def test_rejects_invalid_spin(self) -> None:
        with self.assertRaises(ValueError):
            AnalysisConfig(
                output_file=Path("missing.out"),
                orbital_requests=[
                    OrbitalRequest("0", "Dy", "f", 1),
                ],
                active_electrons=4,
                wanted_spin="INVALID",
            )


class TestOrbitalRequestValidation(unittest.TestCase):
    def test_rejects_non_positive_number(self) -> None:
        with self.assertRaises(ValueError):
            OrbitalRequest("0", "Dy", "f", 0)


if __name__ == "__main__":
    unittest.main()
