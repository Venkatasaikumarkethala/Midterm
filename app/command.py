"""
Declares an abstract base class for all command operations. Each command executes an operation.
"""

from decimal import Decimal
from abc import ABC, abstractmethod

class Command(ABC):
    """
    Defines a standard interface for commands, including synchronous and multiprocessing execution.
    """

    operation_name: str

    @abstractmethod
    def execute(self, operand1: Decimal, operand2: Decimal) -> Decimal:
        """
        Executes the command on the two provided operands.

        Args:
            operand1 (Decimal): The first number.
            operand2 (Decimal): The second number.

        Returns:
            Decimal: Result of the operation.
        """
        pass

    @abstractmethod
    def execute_multiprocessing(self, operand1: Decimal, operand2: Decimal, result_queue):
        """
        Executes the command using multiprocessing and stores the result in a queue.

        Args:
            operand1 (Decimal): The first number.
            operand2 (Decimal): The second number.
            result_queue: A multiprocessing.Queue to capture the result.
        """
        pass
