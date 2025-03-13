
# app/plugins/subtract_command.py
"""
This module defines the `SubtractCommand` class for performing subtraction operations.
"""

from decimal import Decimal
from app.command import Command

class SubtractCommand(Command):
    """
    Command class for performing subtraction operations.
    Implements the `execute` and `execute_multiprocessing` methods.
    """
    operation_name = "subtract"

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        """
        Subtracts the second number from the first number.

        Args:
            num1 (Decimal): The first number.
            num2 (Decimal): The second number.

        Returns:
            Decimal: The result of the subtraction (num1 - num2).
        """
        return num1 - num2

    def execute_multiprocessing(self, num1: Decimal, num2: Decimal, result_queue):
        """
        Performs the subtraction operation using multiprocessing
        and puts the result into a queue.

        Args:
            num1 (Decimal): The first number.
            num2 (Decimal): The second number.
            result_queue (multiprocessing.Queue): Queue to store the result.
        """
        result = self.execute(num1, num2)
        result_queue.put(result)
