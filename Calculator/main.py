"""Main application entry point for the Smart Calculator.

This module coordinates the CLI loop, captures user inputs, resolves operations
using the Calculator class, updates the HistoryManager, and outputs styled
results and error reports.
"""

import sys
from calculator import Calculator
from history import HistoryCorruptedError, HistoryManager
from utils import (
    get_integer_input,
    get_menu_choice,
    get_numeric_input,
    print_error,
    print_header,
    print_info,
    print_success,
    print_warning,
    format_number
)


def display_menu() -> None:
    """Print the interactive main menu of the Smart Calculator."""
    print("\n===========================")
    print("      SMART CALCULATOR     ")
    print("===========================")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Modulus")
    print("6. Power")
    print("7. Floor Division")
    print("8. Square Root")
    print("9. Factorial")
    print("10. Percentage")
    print("11. Absolute")
    print("12. Logarithm")
    print("13. Sine")
    print("14. Cosine")
    print("15. Tangent")
    print("16. View History")
    print("17. Delete History")
    print("18. Export History to CSV")
    print("19. Exit")
    print("===========================")


def print_history_table(entries: list) -> None:
    """Print the calculation history list in a beautiful table format.

    Args:
        entries: A list of history entry dictionaries.
    """
    if not entries:
        print_info("No calculation history found.")
        return

    # Print table header
    header = f"{'ID':<5} | {'Operation':<18} | {'First Num':<12} | {'Second Num':<12} | {'Result':<15} | {'Timestamp':<20}"
    print_header(header)
    print("-" * len(header))

    for entry in entries:
        num1_str = format_number(entry["first_number"])
        num2 = entry["second_number"]
        num2_str = format_number(num2) if num2 is not None else "N/A"
        res_str = format_number(entry["result"])
        
        print(
            f"{entry['id']:<5} | "
            f"{entry['operation']:<18} | "
            f"{num1_str:<12} | "
            f"{num2_str:<12} | "
            f"{res_str:<15} | "
            f"{entry['timestamp']:<20}"
        )


def main() -> None:
    """Run the main CLI interactive loop for the Smart Calculator."""
    calc = Calculator()
    history_manager = HistoryManager()

    print_success("Welcome to the Smart Calculator! Choose an option to begin.")

    while True:
        display_menu()
        choice = get_menu_choice("Select an option (1-19): ", 1, 19)

        # 19. Exit
        if choice == 19:
            print_success("Thank you for using Smart Calculator. Goodbye!")
            sys.exit(0)

        # 16. View History
        elif choice == 16:
            try:
                entries = history_manager.get_entries()
                print_history_table(entries)
            except HistoryCorruptedError as e:
                print_error(str(e))
            continue

        # 17. Delete History
        elif choice == 17:
            history_manager.clear_history()
            print_success("Calculation history deleted successfully.")
            continue

        # 18. Export History to CSV
        elif choice == 18:
            try:
                csv_path = input("Enter output CSV path/filename (e.g. history.csv): ").strip()
                if not csv_path:
                    print_error("Filename cannot be empty.")
                    continue
                history_manager.export_to_csv(csv_path)
                print_success(f"History successfully exported to '{csv_path}'.")
            except (ValueError, IOError) as e:
                print_error(str(e))
            except HistoryCorruptedError as e:
                print_error(f"Cannot export history: {str(e)}")
            continue

        # Mathematical operations
        try:
            # Operation category settings
            # Two-operand operations: 1-7, 10
            if choice in (1, 2, 3, 4, 5, 6, 7, 10):
                if choice == 10:
                    num1 = get_numeric_input("Enter value (part): ")
                    num2 = get_numeric_input("Enter total: ")
                else:
                    num1 = get_numeric_input("Enter first number: ")
                    num2 = get_numeric_input("Enter second number: ")

                if choice == 1:
                    result = calc.add(num1, num2)
                    op_name = "Addition"
                elif choice == 2:
                    result = calc.subtract(num1, num2)
                    op_name = "Subtraction"
                elif choice == 3:
                    result = calc.multiply(num1, num2)
                    op_name = "Multiplication"
                elif choice == 4:
                    result = calc.divide(num1, num2)
                    op_name = "Division"
                elif choice == 5:
                    result = calc.modulus(num1, num2)
                    op_name = "Modulus"
                elif choice == 6:
                    result = calc.power(num1, num2)
                    op_name = "Power"
                elif choice == 7:
                    result = calc.floor_division(num1, num2)
                    op_name = "Floor Division"
                elif choice == 10:
                    result = calc.percentage(num1, num2)
                    op_name = "Percentage"

                # Output result
                num1_str = format_number(num1)
                num2_str = format_number(num2)
                res_str = format_number(result)
                print_success(f"Result: {num1_str} {op_name.lower() if choice != 10 else 'is what percent of'} {num2_str} = {res_str}")
                
                # Save to history
                history_manager.add_entry(op_name, num1, num2, result)

            # Single-operand operations: 8, 9, 11, 13, 14, 15
            elif choice in (8, 9, 11, 13, 14, 15):
                num1 = get_numeric_input("Enter number: ")

                if choice == 8:
                    result = calc.square_root(num1)
                    op_name = "Square Root"
                    print_success(f"Result: √{format_number(num1)} = {format_number(result)}")
                elif choice == 9:
                    result = calc.factorial(num1)
                    op_name = "Factorial"
                    print_success(f"Result: {format_number(num1)}! = {format_number(result)}")
                elif choice == 11:
                    result = calc.absolute(num1)
                    op_name = "Absolute"
                    print_success(f"Result: |{format_number(num1)}| = {format_number(result)}")
                elif choice in (13, 14, 15):
                    # Ask user if they are using degrees or radians
                    mode_choice = input("Is the angle in degrees? (y/n, default: y): ").strip().lower()
                    in_degrees = mode_choice not in ("n", "no", "radian", "radians")
                    unit = "deg" if in_degrees else "rad"

                    if choice == 13:
                        result = calc.sine(num1, in_degrees)
                        op_name = f"Sine ({unit})"
                        print_success(f"Result: sin({format_number(num1)} {unit}) = {format_number(result)}")
                    elif choice == 14:
                        result = calc.cosine(num1, in_degrees)
                        op_name = f"Cosine ({unit})"
                        print_success(f"Result: cos({format_number(num1)} {unit}) = {format_number(result)}")
                    elif choice == 15:
                        result = calc.tangent(num1, in_degrees)
                        op_name = f"Tangent ({unit})"
                        print_success(f"Result: tan({format_number(num1)} {unit}) = {format_number(result)}")

                # Save to history
                history_manager.add_entry(op_name, num1, None, result)

            # Logarithm operation (special double-operand with defaults)
            elif choice == 12:
                num1 = get_numeric_input("Enter number: ")
                base_choice = input("Do you want to specify a custom base? (y/n, default: n [natural log]): ").strip().lower()
                
                if base_choice in ("y", "yes"):
                    base = get_numeric_input("Enter base: ")
                    result = calc.logarithm(num1, base)
                    op_name = f"Log (base {format_number(base)})"
                    print_success(f"Result: log_{format_number(base)}({format_number(num1)}) = {format_number(result)}")
                    history_manager.add_entry(op_name, num1, base, result)
                else:
                    result = calc.logarithm(num1)
                    op_name = "Log (base e)"
                    print_success(f"Result: ln({format_number(num1)}) = {format_number(result)}")
                    history_manager.add_entry(op_name, num1, None, result)

        except ZeroDivisionError as e:
            print_error(f"Math Error - {str(e)}")
        except ValueError as e:
            print_error(f"Value Error - {str(e)}")
        except Exception as e:  # pylint: disable=broad-except
            print_error(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_warning("\nProgram interrupted by user. Exiting...")
        sys.exit(0)
