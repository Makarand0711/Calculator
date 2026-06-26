"""Utility functions module for the Smart Calculator.

This module provides input validation helpers, text formatting utilities,
and styled CLI outputs to ensure a premium user experience and clear error
messages.
"""

from typing import Union

# ANSI escape sequences for text styling
COLOR_HEADER = "\033[95m"  # Light Magenta
COLOR_BLUE = "\033[94m"    # Light Blue
COLOR_CYAN = "\033[96m"    # Light Cyan
COLOR_GREEN = "\033[92m"   # Light Green
COLOR_WARNING = "\033[93m" # Light Yellow
COLOR_FAIL = "\033[91m"    # Light Red
COLOR_RESET = "\033[0m"    # Reset
STYLE_BOLD = "\033[1m"     # Bold
STYLE_UNDERLINE = "\033[4m" # Underline


def print_header(text: str) -> None:
    """Print text styled as a section header.

    Args:
        text: The text to print.
    """
    print(f"\n{COLOR_HEADER}{STYLE_BOLD}{text}{COLOR_RESET}")


def print_success(text: str) -> None:
    """Print text styled as a success message.

    Args:
        text: The text to print.
    """
    print(f"{COLOR_GREEN}✔ {text}{COLOR_RESET}")


def print_error(text: str) -> None:
    """Print text styled as an error message.

    Args:
        text: The text to print.
    """
    print(f"{COLOR_FAIL}✘ Error: {text}{COLOR_RESET}")


def print_info(text: str) -> None:
    """Print text styled as info.

    Args:
        text: The text to print.
    """
    print(f"{COLOR_CYAN}{text}{COLOR_RESET}")


def print_warning(text: str) -> None:
    """Print text styled as a warning message.

    Args:
        text: The text to print.
    """
    print(f"{COLOR_WARNING}⚠ Warning: {text}{COLOR_RESET}")


def format_number(val: Union[int, float]) -> str:
    """Format a number to be user-friendly.

    Removes unnecessary trailing zeros for float values and formats integers.

    Args:
        val: The number to format.

    Returns:
        A clean string representation of the number.
    """
    if isinstance(val, float):
        # Check if the float is actually a whole number (e.g. 5.0)
        if val.is_integer():
            return str(int(val))
        
        # Round to 10 decimal places to eliminate float representation issues (e.g. 0.1 + 0.2)
        rounded = round(val, 10)
        
        # Format and strip trailing zeros and the decimal point if it ends up as a whole number
        s = f"{rounded:.10f}".rstrip("0").rstrip(".")
        return s
    
    return str(val)


def get_numeric_input(prompt: str) -> float:
    """Prompt the user for a numeric input and validate it.

    This function loops until the user provides a valid integer or float.

    Args:
        prompt: The text prompt to display to the user.

    Returns:
        The validated float value.
    """
    while True:
        try:
            user_input = input(f"{COLOR_BLUE}{prompt}{COLOR_RESET}").strip()
            if not user_input:
                raise ValueError("Input cannot be empty.")
            
            # Try to convert to float
            val = float(user_input)
            return val
        except ValueError:
            print_error("Invalid number. Please enter a valid integer or decimal.")


def get_integer_input(prompt: str) -> int:
    """Prompt the user for an integer input and validate it.

    This function loops until the user provides a valid integer.

    Args:
        prompt: The text prompt to display to the user.

    Returns:
        The validated integer value.
    """
    while True:
        try:
            user_input = input(f"{COLOR_BLUE}{prompt}{COLOR_RESET}").strip()
            if not user_input:
                raise ValueError("Input cannot be empty.")
            
            # Convert to float first to handle cases like '5.0', then convert to int if it's integer
            f_val = float(user_input)
            if not f_val.is_integer():
                raise ValueError("Value must be an integer.")
            return int(f_val)
        except ValueError:
            print_error("Invalid input. Please enter a valid integer.")


def get_menu_choice(prompt: str, min_val: int, max_val: int) -> int:
    """Prompt the user for a menu choice and validate it's within range.

    Args:
        prompt: The text prompt to display to the user.
        min_val: The minimum allowable integer choice.
        max_val: The maximum allowable integer choice.

    Returns:
        The validated menu choice.
    """
    while True:
        try:
            choice = get_integer_input(prompt)
            if min_val <= choice <= max_val:
                return choice
            print_error(f"Please select a number between {min_val} and {max_val}.")
        except ValueError:
            print_error("Invalid menu option.")
