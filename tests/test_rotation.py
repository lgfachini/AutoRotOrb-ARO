from __future__ import annotations

import unittest

from autorotorb.rotation import build_rotation_block, suggest_swaps


class TestSuggestSwaps(unittest.TestCase):
    def test_pairs_sorted_active_and_candidate_indexes(self) -> None:
        swaps = suggest_swaps([8, 9, 10], [6, 7, 8])
        self.assertEqual(swaps, [(9, 6), (10, 7)])

    def test_no_swaps_when_sets_match(self) -> None:
        self.assertEqual(suggest_swaps([8, 9, 10], [8, 9, 10]), [])

    def test_raises_when_replace_and_add_counts_differ(self) -> None:
        with self.assertRaises(ValueError):
            suggest_swaps([8, 9, 10], [6, 7, 8, 11])


class TestBuildRotationBlock(unittest.TestCase):
    def test_empty_swaps_message(self) -> None:
        block = build_rotation_block([])
        self.assertIn("does not need further rotations", block)

    def test_formats_orca_rotate_commands(self) -> None:
        block = build_rotation_block([(9, 6), (10, 7)], angle=90)
        self.assertIn("rotate{ 9, 6, 90 } end", block)
        self.assertTrue(block.endswith("end"))


if __name__ == "__main__":
    unittest.main()
