"""
This module provides core arithmetic operations, including addition, subtraction, multiplication, and division.
"""

def add(x, y):
    """
    Returns the sum of x and y.
    """
    return x + y

def subtract(x, y):
    """
    Returns the result of subtracting y from x.
    """
    return x - y

def multiply(x, y):
    """
    Returns the product of x and y.
    """
    return x * y

def divide(x, y):
    """
    Divides x by y. Raises ValueError if y is zero.

    Raises:
        ValueError: If the divisor is zero.
    """
    if y == 0:
        raise ValueError("Division by zero is not allowed.")
    return x / y
