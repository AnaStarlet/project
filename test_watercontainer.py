import unittest
from main import maxArea

class TestMaxArea(unittest.TestCase):
    def test_add_1(self):
        self.assertEqual(maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]), 49)

    def test_add_2(self):
        self.assertEqual(maxArea([1, 2, 4, 6, 8, 3, 2]), 10)

    def test_add_3(self):
        self.assertEqual(maxArea([0, 0, 5, 0, 0]), 0)

    def test_add_4(self):
        self.assertEqual(maxArea([10, 1]), 1)

    def test_add_5(self):
        self.assertEqual(maxArea([1, 1]), 1)

if __name__ == '__main__':
    unittest.main()