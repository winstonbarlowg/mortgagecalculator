import unittest
from logic import Calculator


class TestLogic(unittest.TestCase):

    def test_monthly_repayments(self):
        result = Calculator(15000, 70, 4.5, 15, 45100).monthly_repayments(self)
        self.assertEqual(result, 803.24, 144583.2, 39583.2, 180)

    def test_min_deposit(self):
        result = Calculator(15000, 70, 4.5, 15,
                            45100).calc_loan_mindeposit(self)
        self.assertEqual(result, 105000.0, 45000.0)

# Calculator(150000, 70, 4.5, 15, 45100)


if __name__ == "__main__":
    unittest.main()
