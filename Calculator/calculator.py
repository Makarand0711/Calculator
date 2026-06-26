"""Core mathematical operations module for the Smart Calculator.

This module contains the Calculator class which implements various basic and
advanced mathematical functions, with robust error handling for mathematical
domain errors.
"""

import math
from typing import Union

# Define a type alias for numeric inputs
Numeric = Union[int, float]


class Calculator:
    """A calculator class that provides standard and scientific mathematical operations."""

    def add(self, a: Numeric, b: Numeric) -> Numeric:
        """Return the sum of two numbers.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The sum of a and b.
        """
        return a + b

    def subtract(self, a: Numeric, b: Numeric) -> Numeric:
        """Return the difference between two numbers.

        Args:
            a: The first number (minuend).
            b: The second number (subtrahend).

        Returns:
            The difference of a and b.
        """
        return a - b

    def multiply(self, a: Numeric, b: Numeric) -> Numeric:
        """Return the product of two numbers.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The product of a and b.
        """
        return a * b

    def divide(self, a: Numeric, b: Numeric) -> float:
        """Return the division of a by b.

        Args:
            a: The dividend.
            b: The divisor.

        Returns:
            The quotient as a float.

        Raises:
            ZeroDivisionError: If the divisor b is zero.
        """
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return float(a / b)

    def modulus(self, a: Numeric, b: Numeric) -> Numeric:
        """Return the modulus of a by b.

        Args:
            a: The dividend.
            b: The divisor.

        Returns:
            The remainder of division.

        Raises:
            ZeroDivisionError: If the divisor b is zero.
        """
        if b == 0:
            raise ZeroDivisionError("Modulo by zero is undefined.")
        return a % b

    def power(self, base: Numeric, exponent: Numeric) -> Numeric:
        """Return the base raised to the power of exponent.

        Args:
            base: The base number.
            exponent: The exponent number.

        Returns:
            The result of base raised to exponent.

        Raises:
            ValueError: If attempting to raise a negative base to a fractional power,
                        resulting in a complex number.
        """
        try:
            return math.pow(base, exponent)
        except ValueError as e:
            # math.pow raises ValueError for negative base and fractional exponent
            raise ValueError("Negative base raised to a fractional power results in a complex number.") from e
        except OverflowError as e:
            raise ValueError("Result is too large (overflow error).") from e

    def floor_division(self, a: Numeric, b: Numeric) -> int:
        """Return the floor division of a by b.

        Args:
            a: The dividend.
            b: The divisor.

        Returns:
            The largest integer less than or equal to a/b.

        Raises:
            ZeroDivisionError: If the divisor b is zero.
        """
        if b == 0:
            raise ZeroDivisionError("Floor division by zero is undefined.")
        return a // b

    def square_root(self, x: Numeric) -> float:
        """Return the square root of x.

        Args:
            x: The input number.

        Returns:
            The square root of x.

        Raises:
            ValueError: If x is a negative number.
        """
        if x < 0:
            raise ValueError("Cannot calculate the square root of a negative number.")
        return math.sqrt(x)

    def factorial(self, x: Numeric) -> int:
        """Return the factorial of x.

        Args:
            x: A non-negative integer (can be represented as float like 5.0).

        Returns:
            The factorial of x.

        Raises:
            ValueError: If x is negative or not an integer.
        """
        # Check if x is a whole number
        if isinstance(x, float) and not x.is_integer():
            raise ValueError("Factorial is only defined for non-negative integers.")
        
        val = int(x)
        if val < 0:
            raise ValueError("Factorial is only defined for non-negative integers.")
            
        try:
            return math.factorial(val)
        except OverflowError as e:
            raise ValueError("Factorial value is too large to calculate.") from e

    def percentage(self, part: Numeric, total: Numeric) -> float:
        """Return the percentage of part relative to total.

        Formula: (part / total) * 100

        Args:
            part: The partial amount.
            total: The total amount.

        Returns:
            The percentage as a float.

        Raises:
            ZeroDivisionError: If the total is zero.
        """
        if total == 0:
            raise ZeroDivisionError("Cannot calculate percentage when total is zero.")
        return float((part / total) * 100)

    def absolute(self, x: Numeric) -> Numeric:
        """Return the absolute value of x.

        Args:
            x: The input number.

        Returns:
            The absolute value of x.
        """
        return abs(x)

    def logarithm(self, x: Numeric, base: Numeric = math.e) -> float:
        """Return the logarithm of x to the given base.

        Defaults to the natural logarithm (base e).

        Args:
            x: The input number.
            base: The base of the logarithm. Defaults to e.

        Returns:
            The logarithm of x to base.

        Raises:
            ValueError: If x <= 0, or base <= 0, or base == 1.
        """
        if x <= 0:
            raise ValueError("Logarithm is only defined for positive numbers.")
        if base <= 0 or base == 1:
            raise ValueError("Logarithm base must be positive and not equal to 1.")
        
        return math.log(x, base)

    def sine(self, angle: Numeric, in_degrees: bool = True) -> float:
        """Return the sine of an angle.

        Args:
            angle: The angle value.
            in_degrees: True if angle is in degrees, False if in radians.

        Returns:
            The sine of the angle.
        """
        if in_degrees:
            angle = math.radians(angle)
        result = math.sin(angle)
        # Avoid float precision issues like sin(180) != 0
        return round(result, 15) if abs(result) < 1e-14 else result

    def cosine(self, angle: Numeric, in_degrees: bool = True) -> float:
        """Return the cosine of an angle.

        Args:
            angle: The angle value.
            in_degrees: True if angle is in degrees, False if in radians.

        Returns:
            The cosine of the angle.
        """
        if in_degrees:
            angle = math.radians(angle)
        result = math.cos(angle)
        # Avoid float precision issues like cos(90) != 0
        return round(result, 15) if abs(result) < 1e-14 else result

    def tangent(self, angle: Numeric, in_degrees: bool = True) -> float:
        """Return the tangent of an angle.

        Args:
            angle: The angle value.
            in_degrees: True if angle is in degrees, False if in radians.

        Returns:
            The tangent of the angle.

        Raises:
            ValueError: If the tangent is undefined for the given angle (e.g., 90, 270 degrees).
        """
        cos_val = self.cosine(angle, in_degrees)
        if abs(cos_val) < 1e-14:
            raise ValueError("Tangent is undefined for this angle (cosine is zero).")
        
        sin_val = self.sine(angle, in_degrees)
        return sin_val / cos_val
