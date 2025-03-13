from decimal import Decimal

class Calculation:
    """
    Represents a single calculation between two operands using a specified operation.
    """
    def __init__(self, operand1: Decimal, operand2: Decimal, operation):
        self.operand1 = operand1
        self.operand2 = operand2
        self.operation = operation
        self.result = None

    def operate(self) -> Decimal:
        """
        Executes the assigned operation and stores the result.
        """
        self.result = self.operation.execute(self.operand1, self.operand2)
        return self.result

    def __str__(self):
        return f"Calculation({self.operand1}, {self.operand2}, {self.operation.operation_name})"
