import unittest
from logic import Calculator
from math import isclose


class TestLogic(unittest.TestCase):

    def test_monthly_repayments(self):
        result = Calculator(150000, 70, 4.5, 15, 45100).monthly_repayments()
        self.assertEqual(result, 803.24, 144583.2, 39583.2, 180)

# failure because of comparison of floating points
    def test_min_deposit(self):
        result = Calculator(150000, 70, 4.5, 15,
                            45100).calc_loan_mindeposit()
        self.assertEqual(result, 105000.0/1, 45000.0/1)

# Calculator(150000, 70, 4.5, 15, 45100)


if __name__ == "__main__":
    unittest.main()
