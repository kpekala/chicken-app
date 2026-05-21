import unittest

from osm import merge_rings

class TestMergeRings(unittest.TestCase):

    def test_empty_input(self):
        """Test that empty input returns an empty list."""
        self.assertEqual(merge_rings([]), [])

    def test_already_closed_ring(self):
        """Test a way that is already a perfect closed ring."""
        ways = [[(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]]
        expected = [[(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]]
        self.assertEqual(merge_rings(ways), expected)

    def test_two_segments_in_order(self):
        """Test two segments that seamlessly connect end-to-start."""
        ways = [
            [(0, 0), (0, 1), (1, 1)],
            [(1, 1), (1, 0), (0, 0)]
        ]
        expected = [[(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]]
        self.assertEqual(merge_rings(ways), expected)

    def test_segments_out_of_order(self):
        """Test multiple segments that build a ring but are jumbled in the list."""
        ways = [
            [(1, 1), (1, 0)],
            [(0, 0), (0, 1)],
            [(1, 0), (0, 0)],
            [(0, 1), (1, 1)]
        ]
        # The exact starting point of the result depends on which segment is popped first.
        # It should start at (1, 1) because that is the first in the list.
        expected = [[(1, 1), (1, 0), (0, 0), (0, 1), (1, 1)]]
        self.assertEqual(merge_rings(ways), expected)

    def test_reversed_segments(self):
        """Test segments where the connection is end-to-end or start-to-start (needs reversing)."""
        ways = [
            [(0, 0), (0, 1)],
            [(1, 1), (0, 1)], # End-to-end match with the first segment (needs reversing)
            [(1, 1), (1, 0)],
            [(0, 0), (1, 0)]  # Start-to-start match when it reaches the end
        ]
        expected = [[(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]]
        self.assertEqual(merge_rings(ways), expected)

    def test_multiple_separate_rings(self):
        """Test multipolygons (e.g., two separate islands)."""
        ways = [
            [(0, 0), (0, 1), (1, 1)],
            [(10, 10), (10, 11), (11, 11)], # Start of second ring
            [(1, 1), (1, 0), (0, 0)],       # Completes first ring
            [(11, 11), (11, 10), (10, 10)]  # Completes second ring
        ]
        expected = [
            [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)],
            [(10, 10), (10, 11), (11, 11), (11, 10), (10, 10)]
        ]
        self.assertEqual(merge_rings(ways), expected)


if __name__ == '__main__':
    unittest.main()