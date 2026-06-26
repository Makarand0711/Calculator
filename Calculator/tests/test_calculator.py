"""Unit tests for the Smart Calculator project.

This module tests the Calculator class operations (Addition, Division,
Square Root, Factorial, Percentage) and tests HistoryManager saving, loading,
clearing, and corruption recovery.
"""

import os
import unittest
import json
from calculator import Calculator
from history import HistoryManager, HistoryCorruptedError


class TestCalculator(unittest.TestCase):
    """Test suite for the core mathematical operations in Calculator class."""

    def setUp(self) -> None:
        """Set up test calculator instance."""
        self.calc = Calculator()

    def test_addition(self) -> None:
        """Test addition operation with integers, floats, zero, and negative numbers."""
        self.assertEqual(self.calc.add(3, 5), 8)
        self.assertEqual(self.calc.add(-1, -1), -2)
        self.assertEqual(self.calc.add(-5, 5), 0)
        self.assertAlmostEqual(self.calc.add(1.5, 2.7), 4.2)
        self.assertEqual(self.calc.add(0, 0), 0)

    def test_division(self) -> None:
        """Test division operation and division-by-zero check."""
        self.assertAlmostEqual(self.calc.divide(6, 3), 2.0)
        self.assertAlmostEqual(self.calc.divide(-6, 3), -2.0)
        self.assertAlmostEqual(self.calc.divide(5, 2), 2.5)
        
        # Test division by zero raises ZeroDivisionError
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(5, 0)

    def test_square_root(self) -> None:
        """Test square root operation and negative-value check."""
        self.assertAlmostEqual(self.calc.square_root(9), 3.0)
        self.assertAlmostEqual(self.calc.square_root(0), 0.0)
        self.assertAlmostEqual(self.calc.square_root(2), 1.41421356, places=7)

        # Test square root of a negative number raises ValueError
        with self.assertRaises(ValueError):
            self.calc.square_root(-4)

    def test_factorial(self) -> None:
        """Test factorial operation with normal integers, float integers, and validation errors."""
        self.assertEqual(self.calc.factorial(5), 120)
        self.assertEqual(self.calc.factorial(0), 1)
        self.assertEqual(self.calc.factorial(1), 1)
        
        # Whole floats representing integers should succeed
        self.assertEqual(self.calc.factorial(5.0), 120)

        # Test negative integer factorial raises ValueError
        with self.assertRaises(ValueError):
            self.calc.factorial(-5)

        # Test float with fractional part factorial raises ValueError
        with self.assertRaises(ValueError):
            self.calc.factorial(5.5)

    def test_percentage(self) -> None:
        """Test percentage calculation and divide-by-zero total check."""
        self.assertAlmostEqual(self.calc.percentage(20, 100), 20.0)
        self.assertAlmostEqual(self.calc.percentage(5, 20), 25.0)
        self.assertAlmostEqual(self.calc.percentage(1.5, 3), 50.0)

        # Test division by zero total percentage raises ZeroDivisionError
        with self.assertRaises(ZeroDivisionError):
            self.calc.percentage(10, 0)


class TestHistoryManager(unittest.TestCase):
    """Test suite for the HistoryManager class including JSON storage and recovery."""

    def setUp(self) -> None:
        """Set up temporary test history file."""
        self.test_filename = "test_history.json"
        self.manager = HistoryManager(self.test_filename)

    def tearDown(self) -> None:
        """Clean up the temporary history file and any backups created during testing."""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
        
        # Clean up any test backups
        for filename in os.listdir("."):
            if filename.startswith(self.test_filename + ".corrupt_"):
                try:
                    os.remove(filename)
                except OSError:
                    pass

    def test_history_saving_and_loading(self) -> None:
        """Test that operations are saved correctly to history and loaded back."""
        # History should start empty
        entries = self.manager.get_entries()
        self.assertEqual(len(entries), 0)

        # Add some entries
        self.manager.add_entry("Addition", 5, 10, 15)
        self.manager.add_entry("Square Root", 16, None, 4)

        # Read back and verify values
        entries = self.manager.get_entries()
        self.assertEqual(len(entries), 2)

        # Verify entry 1
        self.assertEqual(entries[0]["id"], 1)
        self.assertEqual(entries[0]["operation"], "Addition")
        self.assertEqual(entries[0]["first_number"], 5)
        self.assertEqual(entries[0]["second_number"], 10)
        self.assertEqual(entries[0]["result"], 15)
        self.assertIn("timestamp", entries[0])

        # Verify entry 2
        self.assertEqual(entries[1]["id"], 2)
        self.assertEqual(entries[1]["operation"], "Square Root")
        self.assertEqual(entries[1]["first_number"], 16)
        self.assertIsNone(entries[1]["second_number"])
        self.assertEqual(entries[1]["result"], 4)

    def test_clear_history(self) -> None:
        """Test clearing the saved history entries."""
        self.manager.add_entry("Addition", 1, 2, 3)
        self.assertEqual(len(self.manager.get_entries()), 1)

        self.manager.clear_history()
        self.assertEqual(len(self.manager.get_entries()), 0)

    def test_corrupted_history_file(self) -> None:
        """Test that a corrupted JSON file raises HistoryCorruptedError and backs up."""
        # Write corrupted JSON to the file
        with open(self.test_filename, "w", encoding="utf-8") as f:
            f.write("{invalid_json: true")

        # Loading history should raise HistoryCorruptedError
        with self.assertRaises(HistoryCorruptedError) as context:
            self.manager.get_entries()

        # Check that error message mentions reset and backup
        self.assertIn("corrupted", str(context.exception))
        
        # Verify that a backup path was created and is valid
        backup_path = context.exception.backup_path
        self.assertIsNotNone(backup_path)
        self.assertTrue(os.path.exists(backup_path))
        
        # Check that original file was reset and is now clean
        self.assertEqual(len(self.manager.get_entries()), 0)


if __name__ == "__main__":
    unittest.main()
