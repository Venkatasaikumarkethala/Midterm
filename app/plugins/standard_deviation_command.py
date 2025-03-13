"""
This module defines the StandardDeviationCommand class to compute the standard deviation of two numbers.
"""

from decimal import Decimal
from app.command import Command
import math

class StandardDeviationCommand(Command):
    """
    Command to calculate the standard deviation of two decimal numbers.
    """
    operation_name = "standard_deviation"

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        """
        Computes the sample standard deviation of two numbers.

        Args:
            num1 (Decimal): First number.
            num2 (Decimal): Second number.

        Returns:
            Decimal: The computed standard deviation.
        """
        # Convert Decimal to float for math.sqrt
        mean_value = (num1 + num2) / Decimal(2)
        variance = ((num1 - mean_value) ** 2 + (num2 - mean_value) ** 2) / Decimal(2)
        std_dev = Decimal(math.sqrt(float(variance)))
        return std_dev

    def execute_multiprocessing(self, num1: Decimal, num2: Decimal, result_queue):
        """
        Executes the standard deviation calculation using multiprocessing.

        Args:
            num1 (Decimal): First number.
            num2 (Decimal): Second number.
            result_queue (multiprocessing.Queue): Queue to store the result.
        """
        result = self.execute(num1, num2)
        result_queue.put(result)
