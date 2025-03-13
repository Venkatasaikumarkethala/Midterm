"""
This module defines the MeanCommand class to compute the mean of two numbers.
"""

from decimal import Decimal
from app.command import Command

class MeanCommand(Command):
    """
    Command to calculate the arithmetic mean (average) of two decimal numbers.
    """
    operation_name = "mean"

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        """
        Calculates the mean of two numbers.

        Args:
            num1 (Decimal): First number.
            num2 (Decimal): Second number.

        Returns:
            Decimal: The calculated mean value.
        """
        return (num1 + num2) / Decimal(2)

    def execute_multiprocessing(self, num1: Decimal, num2: Decimal, result_queue):
        """
        Executes the mean calculation in a multiprocessing context.

        Args:
            num1 (Decimal): First number.
            num2 (Decimal): Second number.
            result_queue (multiprocessing.Queue): Queue to store the result.
        """
        result = self.execute(num1, num2)
        result_queue.put(result)
