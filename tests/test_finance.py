"""
Unit tests for Personal Finance Calculator
"""

import unittest
from finance_calculator import calculate_tax


class TestFinanceCalculator(unittest.TestCase):
    """Test cases for finance calculator functions."""

    def test_calculate_tax_normal(self):
        """Test tax calculation with normal values."""
        self.assertEqual(calculate_tax(10000, 10), 1000)

    def test_calculate_tax_zero_salary(self):
        """Tax should be zero if salary is zero."""
        self.assertEqual(calculate_tax(0, 10), 0)

    def test_calculate_tax_zero_rate(self):
        """Tax should be zero if tax rate is zero."""
        self.assertEqual(calculate_tax(10000, 0), 0)

    def test_calculate_tax_float(self):
        """Test with float values."""
        self.assertAlmostEqual(calculate_tax(12345.67, 12.5), 1543.20875)


if __name__ == "__main__":
    unittest.main()