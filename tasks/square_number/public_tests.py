import unittest
from solution import solve

class TestPublicSquareNumber(unittest.TestCase):

    def test_small_numbers(self):
        self.assertEqual(solve(2), 4)
        self.assertEqual(solve(3), 9)

    def test_medium_numbers(self):
        self.assertEqual(solve(10), 100)
        self.assertEqual(solve(12), 144)

    def test_negative_numbers(self):
        self.assertEqual(solve(-4), 16)
        self.assertEqual(solve(-7), 49)

if __name__ == "__main__":
    unittest.main()