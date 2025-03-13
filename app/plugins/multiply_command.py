# app/plugins/multiply_command.py
"""
This module defines the `MultiplyCommand` class for performing multiplication operations.
"""

from decimal import Decimal
from app.command import Command

class MultiplyCommand(Command):
    """
    Command class for performing multiplication operations.
    Implements the `execute` and `execute_multiprocessing` methods.
    """
    operation_name = "multiply"

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        """
        Multiplies two numbers.

        Args:
            num1 (Decimal): The first number.
            num2 (Decimal): The second number.

        Returns:
            Decimal: The product of num1 and num2.
        """
        return num1 * num2

    def execute_multiprocessing(self, num1: Decimal, num2: Decimal, result_queue):
        """
        Performs the multiplication operation using multiprocessing
        and puts the result into a queue.

        Args:
            num1 (Decimal): The first number.
            num2 (Decimal): The second number.
            result_queue (multiprocessing.Queue): Queue to store the result.
        """
        result = self.execute(num1, num2)
        result_queue.put(result)