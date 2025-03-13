"""
Calculations module: Manages a collection of arithmetic calculation records.
Leverages the PandasFacade for simplified data operations.
"""

import pandas as pd
from app.calculation import Calculation
from app.pandas_facade import PandasFacade

class Calculations:
    """
    Acts as a centralized handler for managing calculation records.
    """

    _history_facade = PandasFacade()

    @classmethod
    def add_calculation(cls, calculation: Calculation):
        """
        Records a completed calculation into the history.

        Args:
            calculation (Calculation): The calculation to be stored.
        """
        record = {
            "operation": calculation.operation.operation_name,
            "operand1": calculation.operand1,
            "operand2": calculation.operand2,
            "result": calculation.result
        }
        cls._history_facade.add_record(record)

    @classmethod
    def clear_history(cls):
        """
        Removes all stored calculation records.
        """
        cls._history_facade.clear()

    @classmethod
    def get_all_calculations(cls) -> pd.DataFrame:
        """
        Retrieves all stored calculations.

        Returns:
            pd.DataFrame: DataFrame containing the history of calculations.
        """
        return cls._history_facade.dataframe

    @classmethod
    def filter_by_operation(cls, operation_name: str) -> pd.DataFrame:
        """
        Filters calculation records by a specific operation type.

        Args:
            operation_name (str): The name of the operation to filter.

        Returns:
            pd.DataFrame: Filtered records matching the operation.
        """
        return cls._history_facade.filter_by_operation(operation_name)

    @classmethod
    def save_history(cls, file_path: str):
        """
        Persists the current history into a CSV file.

        Args:
            file_path (str): The output file path.
        """
        cls._history_facade.save_to_file(file_path)

    @classmethod
    def load_history(cls, file_path: str):
        """
        Imports calculation records from a CSV file.

        Args:
            file_path (str): The source CSV file path.
        """
        cls._history_facade.load_from_file(file_path)

    @classmethod
    def delete_history(cls, index: int):
        """
        Deletes a record at the specified index.

        Args:
            index (int): The index of the record to delete.
        """
        cls._history_facade.delete_record(index)
