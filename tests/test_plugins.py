import pytest
import multiprocessing
from decimal import Decimal, DivisionByZero
from multiprocessing import Queue

from app.plugins.add_command import AddCommand
from app.plugins.subtract_command import SubtractCommand
from app.plugins.multiply_command import MultiplyCommand
from app.plugins.divide_command import DivideCommand
from app.plugins.mean_command import MeanCommand
from app.plugins.standard_deviation_command import StandardDeviationCommand

# ---------- AddCommand Tests ----------

def test_add_command():
    command = AddCommand()
    result = command.execute(Decimal(2), Decimal(3))
    assert result == Decimal(5)

def test_add_command_multiprocessing():
    command = AddCommand()
    result_queue = Queue()
    command.execute_multiprocessing(Decimal(2), Decimal(3), result_queue)
    assert result_queue.get() == Decimal(5)

# ---------- SubtractCommand Tests ----------

def test_subtract_command():
    command = SubtractCommand()
    result = command.execute(Decimal(5), Decimal(3))
    assert result == Decimal(2)

def test_subtract_command_multiprocessing():
    command = SubtractCommand()
    result_queue = Queue()
    command.execute_multiprocessing(Decimal(5), Decimal(3), result_queue)
    assert result_queue.get() == Decimal(2)

# ---------- MultiplyCommand Tests ----------

def test_multiply_command():
    command = MultiplyCommand()
    result = command.execute(Decimal(2), Decimal(3))
    assert result == Decimal(6)

def test_multiply_command_multiprocessing():
    command = MultiplyCommand()
    result_queue = Queue()
    command.execute_multiprocessing(Decimal(2), Decimal(3), result_queue)
    assert result_queue.get() == Decimal(6)

# ---------- DivideCommand Tests ----------

def test_divide_command():
    command = DivideCommand()
    result = command.execute(Decimal(6), Decimal(3))
    assert result == Decimal(2)

def test_divide_command_multiprocessing():
    command = DivideCommand()
    result_queue = Queue()
    command.execute_multiprocessing(Decimal(6), Decimal(3), result_queue)
    assert result_queue.get() == Decimal(2)

def test_divide_by_zero():
    command = DivideCommand()
    with pytest.raises(ZeroDivisionError):
        command.execute(Decimal(6), Decimal(0))

def test_divide_command_execute():
    command = DivideCommand()
    
    # Valid divisions
    assert command.execute(Decimal(6), Decimal(3)) == Decimal(2)
    assert command.execute(Decimal(-6), Decimal(3)) == Decimal(-2)
    assert command.execute(Decimal(0), Decimal(3)) == Decimal(0)
    
    # Division by zero
    with pytest.raises(DivisionByZero, match="Division by zero is not allowed."):
        command.execute(Decimal(6), Decimal(0))

def test_divide_command_execute_multiprocessing():
    command = DivideCommand()
    result_queue = Queue()

    # Normal case
    command.execute_multiprocessing(Decimal(6), Decimal(3), result_queue)
    assert result_queue.get() == Decimal(2)

    # Division by zero
    command.execute_multiprocessing(Decimal(6), Decimal(0), result_queue)
    result = result_queue.get()
    assert isinstance(result, DivisionByZero)
    assert str(result) == "Division by zero is not allowed."

# ---------- MeanCommand Tests ----------

def test_mean_command():
    command = MeanCommand()
    result = command.execute(Decimal(10), Decimal(20))
    assert result == Decimal(15)

def test_mean_command_negative_numbers():
    command = MeanCommand()
    result = command.execute(Decimal(-10), Decimal(20))
    assert result == Decimal(5)

def test_mean_command_multiprocessing():
    command = MeanCommand()
    result_queue = Queue()
    command.execute_multiprocessing(Decimal(10), Decimal(20), result_queue)
    assert result_queue.get() == Decimal(15)

# ---------- StandardDeviationCommand Tests ----------

def test_standard_deviation_command():
    command = StandardDeviationCommand()
    result = command.execute(Decimal(10), Decimal(20))

    # Manual calculation
    # Mean = 15, variance = ((10-15)^2 + (20-15)^2)/2 = (25+25)/2 = 25
    # Std Dev = sqrt(25) = 5
    assert result == Decimal(5)

def test_standard_deviation_command_identical_numbers():
    command = StandardDeviationCommand()
    result = command.execute(Decimal(10), Decimal(10))
    assert result == Decimal(0)

def test_standard_deviation_command_multiprocessing():
    command = StandardDeviationCommand()
    result_queue = Queue()
    command.execute_multiprocessing(Decimal(10), Decimal(20), result_queue)
    assert result_queue.get() == Decimal(5)

def test_standard_deviation_command_multiprocessing_with_identical_numbers():
    command = StandardDeviationCommand()
    result_queue = Queue()
    command.execute_multiprocessing(Decimal(7), Decimal(7), result_queue)
    assert result_queue.get() == Decimal(0)

# ---------- Additional MeanCommand Tests ----------

def test_mean_command_with_large_numbers():
    command = MeanCommand()
    result = command.execute(Decimal('1000000000000000000'), Decimal('2000000000000000000'))
    assert result == Decimal('1500000000000000000')

def test_mean_command_with_zero_and_number():
    command = MeanCommand()
    result = command.execute(Decimal(0), Decimal(50))
    assert result == Decimal(25)

def test_mean_command_with_extremely_small_numbers():
    command = MeanCommand()
    result = command.execute(Decimal('0.0000000001'), Decimal('0.0000000003'))
    assert result == Decimal('0.0000000002')

def test_mean_command_with_negative_numbers():
    command = MeanCommand()
    result = command.execute(Decimal(-50), Decimal(-30))
    assert result == Decimal(-40)

def test_mean_command_with_one_negative_one_positive():
    command = MeanCommand()
    result = command.execute(Decimal(-50), Decimal(50))
    assert result == Decimal(0)

def test_mean_command_multiprocessing_with_large_numbers():
    command = MeanCommand()
    result_queue = Queue()
    command.execute_multiprocessing(Decimal('1000000000000000000'), Decimal('2000000000000000000'), result_queue)
    assert result_queue.get() == Decimal('1500000000000000000')

# ---------- Additional StandardDeviationCommand Tests ----------

def test_standard_deviation_command_with_large_numbers():
    command = StandardDeviationCommand()
    result = command.execute(Decimal('1000000000000000000'), Decimal('2000000000000000000'))
    
    # mean = 1.5e+18, variance = ((1e+18 - 1.5e+18)^2 + (2e+18 - 1.5e+18)^2) / 2
    # variance = (0.25e+36 + 0.25e+36)/2 = 0.25e+36
    # std_dev = sqrt(0.25e+36) = 0.5e+18
    assert result == Decimal('500000000000000000')

def test_standard_deviation_command_with_negative_numbers():
    command = StandardDeviationCommand()
    result = command.execute(Decimal(-10), Decimal(-30))
    
    # mean = -20, variance = ((-10 + 20)^2 + (-30 + 20)^2)/2 = (100 + 100)/2 = 100
    # std_dev = sqrt(100) = 10
    assert result == Decimal(10)

def test_standard_deviation_command_with_zero_and_number():
    command = StandardDeviationCommand()
    result = command.execute(Decimal(0), Decimal(50))
    
    # mean = 25, variance = ((0 - 25)^2 + (50 - 25)^2)/2 = (625 + 625)/2 = 625
    # std_dev = sqrt(625) = 25
    assert result == Decimal(25)


def test_standard_deviation_command_multiprocessing_with_large_numbers():
    command = StandardDeviationCommand()
    result_queue = Queue()
    command.execute_multiprocessing(Decimal('1000000000000000000'), Decimal('2000000000000000000'), result_queue)
    assert result_queue.get() == Decimal('500000000000000000')

def test_standard_deviation_command_multiprocessing_with_zero_and_number():
    command = StandardDeviationCommand()
    result_queue = Queue()
    command.execute_multiprocessing(Decimal(0), Decimal(50), result_queue)
    assert result_queue.get() == Decimal(25)

def test_standard_deviation_command_with_opposite_numbers():
    command = StandardDeviationCommand()
    result = command.execute(Decimal(-100), Decimal(100))
    
    # mean = 0
    # variance = ((-100 - 0)^2 + (100 - 0)^2)/2 = (10000 + 10000)/2 = 10000
    # std_dev = sqrt(10000) = 100
    assert result == Decimal(100)

def test_standard_deviation_command_multiprocessing_with_opposite_numbers():
    command = StandardDeviationCommand()
    result_queue = Queue()
    command.execute_multiprocessing(Decimal(-100), Decimal(100), result_queue)
    assert result_queue.get() == Decimal(100)
