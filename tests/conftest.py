'''
This module is designed to provide test configuration and data generation
for arithmetic operations using the pytest framework. It utilizes the Faker
library to generate random test data for the following operations: addition,
subtraction, multiplication, and division. The generated data is used to
create dynamic tests for validating the behavior of arithmetic operations.
'''
from decimal import Decimal
from faker import Faker
from app.operations import add, subtract, multiply, divide

fake = Faker()

def generate_test_data(num_records):
    """
    Generates test data for arithmetic operations.
    """
    # Define operation mappings for both Calculator and Calculation tests
    operation_mappings = {
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }
    # Generate test data
    for index in range(num_records):
        operand1 = Decimal(fake.random_number(digits=2))
        operand2 = Decimal(fake.random_number(digits=2)) if index % 4 != 3 else Decimal(fake.random_number(digits=1))
        operation_name = fake.random_element(elements=list(operation_mappings.keys()))
        operation_function = operation_mappings[operation_name]
        if operation_function == divide:
            operand2 = Decimal('1') if operand2 == Decimal('0') else operand2
        try:
            if operation_function == divide and operand2 == Decimal('0'):
                expected_result = "ZeroDivisionError"
            else:
                expected_result = operation_function(operand1, operand2)
        except ZeroDivisionError:
            expected_result = "ZeroDivisionError"
        yield operand1, operand2, operation_name, operation_function, expected_result

def pytest_addoption(parser):
    """
    Adds command line options for pytest.
    """
    parser.addoption("--num_records", action="store", default=5, type=int, help="Number of test records to generate")

def pytest_generate_tests(metafunc):
    """
    Generates dynamic tests based on the provided function parameters.
    """
    if {"operand1", "operand2", "expected_result"}.intersection(set(metafunc.fixturenames)):
        num_records = metafunc.config.getoption("num_records")
        parameters = list(generate_test_data(num_records))
        modified_parameters = [
            (op1, op2, op_name if 'operation_name' in metafunc.fixturenames else op_func, expected)
            for op1, op2, op_name, op_func, expected in parameters
        ]
        metafunc.parametrize("operand1,operand2,operation,expected_result", modified_parameters)