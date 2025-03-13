# app/plugins/divide_command.py
"""
This module defines the `DivideCommand` class for performing division operations.
"""

from decimal import Decimal, DivisionByZero
from app.command import Command

class DivideCommand(Command):
    """
    Command class for performing division operations.
    Implements the `execute` and `execute_multiprocessing` methods.
    """
    operation_name = "divide"

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        """
        Divides the first number by the second number.

        Args:
            num1 (Decimal): The numerator.
            num2 (Decimal): The denominator.

        Returns:
            Decimal: The result of the division.

        Raises:
            DivisionByZero: If the second number is zero.
        """
        if num2 == 0:
            raise DivisionByZero("Division by zero is not allowed.")
        return num1 / num2

    def execute_multiprocessing(self, num1: Decimal, num2: Decimal, result_queue):
        """
        Performs the division operation using multiprocessing
        and puts the result into a queue.

        Args:
            num1 (Decimal): The numerator.
            num2 (Decimal): The denominator.
            result_queue (multiprocessing.Queue): Queue to store the result.
        """
        try:
            result = self.execute(num1, num2)
            result_queue.put(result)
        except DivisionByZero as e:
            result_queue.put(e)