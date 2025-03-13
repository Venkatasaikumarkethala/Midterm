# app/plugins/add_command.py
"""
This module defines the `AddCommand` class for performing addition operations.
"""

from decimal import Decimal
from app.command import Command

class AddCommand(Command):
    """
    Command class for performing addition operations.
    Implements the `execute` and `execute_multiprocessing` methods.
    """
    operation_name = "add"

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        """
        Adds two numbers.

        Args:
            num1 (Decimal): The first number.
            num2 (Decimal): The second number.

        Returns:
            Decimal: The result of the addition.
        """
        return num1 + num2

    def execute_multiprocessing(self, num1: Decimal, num2: Decimal, result_queue):
        """
        Performs the addition operation using multiprocessing
        and puts the result into a queue.

        Args:
            num1 (Decimal): The first number.
            num2 (Decimal): The second number.
            result_queue (multiprocessing.Queue): Queue to store the result.
        """
        result = self.execute(num1, num2)
        result_queue.put(result)