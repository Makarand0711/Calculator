"""History management module for the Smart Calculator.

This module handles loading, saving, clearing, and exporting the calculation
history to JSON and CSV formats. It includes error handling for file operations
and corrupted data.
"""

import csv
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

# Define type alias for numeric values
Numeric = Union[int, float]


class HistoryCorruptedError(Exception):
    """Custom exception raised when the history JSON file is corrupted."""

    def __init__(self, message: str, backup_path: Optional[str] = None):
        super().__init__(message)
        self.backup_path = backup_path


class HistoryManager:
    """Manages the lifecycle of calculation history stored in JSON format."""

    def __init__(self, filepath: str = "history.json"):
        """Initialize the HistoryManager with a file path.

        Args:
            filepath: Path to the JSON file where history is stored.
        """
        self.filepath = filepath

    def _load_history(self) -> List[Dict[str, Any]]:
        """Load history from the JSON file.

        Returns:
            A list of dictionary records containing history entries.

        Raises:
            HistoryCorruptedError: If the history file contains invalid JSON or structure.
        """
        if not os.path.exists(self.filepath):
            return []

        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    raise ValueError("History data must be a list of entries.")
                
                # Validate the structure of each entry
                required_keys = {"id", "operation", "first_number", "result", "timestamp"}
                for entry in data:
                    if not isinstance(entry, dict) or not required_keys.issubset(entry.keys()):
                        raise ValueError("Invalid entry structure in history file.")
                
                return data
        except (json.JSONDecodeError, ValueError) as e:
            # Create a backup of the corrupted file to prevent data loss
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{self.filepath}.corrupt_{timestamp}"
            try:
                if os.path.exists(self.filepath):
                    os.rename(self.filepath, backup_path)
            except OSError:
                backup_path = None
                
            raise HistoryCorruptedError(
                f"History file was corrupted and has been reset. "
                f"Original file saved to {backup_path if backup_path else 'could not backup'}.",
                backup_path=backup_path
            ) from e

    def _save_history(self, history: List[Dict[str, Any]]) -> None:
        """Save history back to the JSON file.

        Args:
            history: The complete list of history entries to save.
        """
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=4)

    def add_entry(
        self,
        operation: str,
        first_number: Numeric,
        second_number: Optional[Numeric],
        result: Numeric
    ) -> None:
        """Add a calculation entry to the history.

        Args:
            operation: Name of the operation performed (e.g. 'Addition').
            first_number: The first input number.
            second_number: The second input number, or None if not applicable.
            result: The result of the calculation.
        """
        try:
            history = self._load_history()
        except HistoryCorruptedError:
            # If load fails due to corruption, a new empty history list is created
            history = []

        # Find the next sequential ID
        next_id = 1
        if history:
            next_id = max(entry["id"] for entry in history) + 1

        entry = {
            "id": next_id,
            "operation": operation,
            "first_number": first_number,
            "second_number": second_number,
            "result": result,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        history.append(entry)
        self._save_history(history)

    def get_entries(self) -> List[Dict[str, Any]]:
        """Retrieve all calculation history entries.

        Returns:
            A list of dictionary records containing history entries.
        """
        return self._load_history()

    def clear_history(self) -> None:
        """Clear all calculation history entries."""
        # We can either delete the file or write an empty list. Writing [] is cleaner.
        self._save_history([])

    def export_to_csv(self, csv_filepath: str) -> None:
        """Export history entries to a CSV file.

        Args:
            csv_filepath: The path to the CSV file to write.

        Raises:
            ValueError: If there are no history entries to export.
            IOError: If writing to the CSV file fails.
        """
        entries = self.get_entries()
        if not entries:
            raise ValueError("No history entries found to export.")

        # Ensure the filename ends with .csv
        if not csv_filepath.lower().endswith('.csv'):
            csv_filepath += '.csv'

        fieldnames = ["id", "operation", "first_number", "second_number", "result", "timestamp"]
        
        try:
            with open(csv_filepath, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for entry in entries:
                    # Replace None values with empty string or 'N/A' for readability in CSV
                    row = {k: (v if v is not None else "N/A") for k, v in entry.items()}
                    writer.writerow(row)
        except OSError as e:
            raise IOError(f"Failed to write CSV file to {csv_filepath}: {str(e)}") from e
