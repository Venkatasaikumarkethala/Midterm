import os
import sys
import importlib
import multiprocessing
import logging
import logging.config
from decimal import Decimal, InvalidOperation
from collections import OrderedDict
from dotenv import load_dotenv
from app.calculations import Calculations
from app.calculation import Calculation
from logger_config import configure_logging

def initialize_environment():
    """
    Loads environment variables from .env and returns them as a dictionary.
    """
    load_dotenv()
    env_vars = {key: value for key, value in os.environ.items()}
    logging.info("Environment variables successfully loaded.")
    return env_vars

def discover_plugins():
    """
    Scans the plugins directory and loads command plugins dynamically.
    
    Returns:
        OrderedDict: A dictionary mapping command names to command instances.
    """
    commands_registry = OrderedDict()
    plugin_path = os.path.join('app', 'plugins')

    if not os.path.exists(plugin_path):
        logging.warning(f"Plugin directory missing: {plugin_path}")
        return commands_registry

    for file in os.listdir(plugin_path):
        if file.endswith('_command.py'):
            try:
                module_name = file[:-3]
                module = importlib.import_module(f'app.plugins.{module_name}')
                class_name = module_name[:-8].capitalize() + 'Command'
                command_class = getattr(module, class_name)
                commands_registry[module_name[:-8]] = command_class()
                logging.info(f"Plugin loaded: {module_name}")
            except (ImportError, AttributeError) as e:
                logging.error(f"Error loading plugin {module_name}: {e}")

    return commands_registry

def execution_logger(func):
    """
    Decorator to log execution of the decorated function.
    """
    def wrapper(*args, **kwargs):
        logging.info(f"Running: {func.__name__}")
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            logging.error(f"Error during {func.__name__}: {ex}")
            raise
    return wrapper

@execution_logger
def process_calculation_and_output(operand1, operand2, operation_key, commands, parallel=False):
    """
    Executes the selected operation and displays the result.

    Args:
        operand1 (str): First operand as string.
        operand2 (str): Second operand as string.
        operation_key (str): Name of the operation.
        commands (dict): Registered command objects.
        parallel (bool): Use multiprocessing if True.
    """
    try:
        num1, num2 = map(Decimal, [operand1, operand2])
        operation = commands.get(operation_key)

        if not operation:
            logging.warning(f"Unknown operation: {operation_key}")
            print(f"Error: Unknown operation '{operation_key}'")
            return

        if parallel:
            result_queue = multiprocessing.Queue()
            process = multiprocessing.Process(
                target=operation.execute_multiprocessing,
                args=(num1, num2, result_queue)
            )
            process.start()
            process.join()

            if not result_queue.empty():
                result = result_queue.get()
                logging.info(f"Multiprocessing result for {operation_key}: {result}")
                print(f"{operand1} {operation_key} {operand2} (multiprocessing) = {result}")
            else:
                logging.error("Failed to fetch result from multiprocessing queue.")
                print("Multiprocessing calculation failed.")
        else:
            result = operation.execute(num1, num2)
            logging.info(f"Result for {operation_key}: {result}")
            print(f"{operand1} {operation_key} {operand2} = {result}")

        # Save the calculation
        calc = Calculation(num1, num2, operation)
        calc_result = calc.operate()
        Calculations.add_calculation(calc)
        logging.debug("Calculation added to history.")

    except InvalidOperation:
        logging.error(f"Invalid input values: {operand1}, {operand2}")
        print("Error: One or both inputs are not valid numbers.")
    except Exception as error:
        logging.error(f"Unexpected error: {error}")
        print(f"Unexpected error occurred: {error}")

@execution_logger
def start_repl(commands):
    """
    Starts the REPL loop for interactive calculations.
    """
    print("Calculator REPL started. Type 'exit' to quit.")
    print("Append 'mp' at the end of a command to use multiprocessing.")

    while True:
        user_input = input(">> ").strip()

        if user_input.lower() == 'exit':
            print("Exiting REPL mode.")
            break

        if user_input == 'menu':
            print("Available Commands:")
            for cmd in commands:
                print(f"- {cmd}")
            continue

        if user_input == 'history':
            history = Calculations.get_all_calculations()
            if history.empty:
                print("No calculations recorded.")
            else:
                print(history)
            continue

        if user_input == 'clear_history':
            Calculations.clear_history()
            print("Calculation history cleared.")
            continue

        if user_input.startswith('save_history'):
            _, filename = user_input.split(maxsplit=1)
            Calculations.save_history(filename)
            print(f"History saved to {filename}")
            continue

        if user_input.startswith('load_history'):
            _, filename = user_input.split(maxsplit=1)
            if os.path.exists(filename):
                Calculations.load_history(filename)
                print(f"History loaded from {filename}")
            else:
                print(f"File '{filename}' not found.")
            continue

        if user_input == 'latest':
            latest = Calculations.get_latest()
            print(f"Latest calculation: {latest}" if latest else "No history available.")
            continue

        if user_input.startswith('delete_history'):
            try:
                _, index = user_input.split(maxsplit=1)
                Calculations.delete_history(int(index))
            except (ValueError, IndexError):
                print("Usage: delete_history <index>")
            continue

        if user_input.startswith('filter_with_operation'):
            try:
                _, operation = user_input.split(maxsplit=1)
                filtered = Calculations.filter_with_operation(operation)
                if filtered.empty:
                    print(f"No records found for operation '{operation}'.")
                else:
                    print(filtered)
            except ValueError:
                print("Usage: filter_with_operation <operation>")
            continue

        parts = user_input.split()
        if len(parts) not in [3, 4]:
            print("Usage: <command> <num1> <num2> [mp]")
            continue

        cmd_name, num1, num2 = parts[:3]
        multiprocessing_flag = len(parts) == 4 and parts[3].lower() == 'mp'

        if cmd_name not in commands:
            print(f"Unknown command '{cmd_name}'. Type 'menu' to list commands.")
            continue

        process_calculation_and_output(num1, num2, cmd_name, commands, multiprocessing_flag)

@execution_logger
def main():
    """
    Main function for CLI arguments and REPL initialization.
    """
    commands = discover_plugins()

    if len(sys.argv) == 2 and sys.argv[1].lower() == 'repl':
        start_repl(commands)
        return

    if len(sys.argv) == 4:
        _, num1, num2, operation_type = sys.argv
        process_calculation_and_output(num1, num2, operation_type, commands)
        return

    if len(sys.argv) == 5:
        _, num1, num2, operation_type, flag = sys.argv
        use_parallel = flag.lower() == "mp"
        process_calculation_and_output(num1, num2, operation_type, commands, use_parallel)
        return

    print("Usage:")
    print("  python main.py repl")
    print("  python main.py <number1> <number2> <operation> [mp]")

if __name__ == '__main__':
    # Setup environment variables and logging configuration
    env_settings = initialize_environment()
    log_level = env_settings.get("LOG_LEVEL", "INFO").upper()
    configure_logging(log_level=log_level)

    logging.info(f"Environment mode: {env_settings.get('ENVIRONMENT', 'Unknown')}")
    logging.info("Calculator Application Launched.")

    main()