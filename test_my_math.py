import unittest
from my_math import add, subtract, multiply, divide

class TestMathFunctions(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(subtract(10, 5), 5)

    def test_multiply(self):
        self.assertEqual(multiply(3, 4), 12)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)

        with self.assertRaises(ValueError):
            divide(10, 0)

if __name__ == '__main__':
    unittest.main()