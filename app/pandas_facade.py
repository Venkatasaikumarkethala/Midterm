"""
This module provides PandasFacade, a utility class for handling
calculation history stored in a pandas DataFrame.
"""

import pandas as pd

class PandasFacade:
    """
    A wrapper for managing calculation records in a pandas DataFrame.
    """

    def __init__(self):
        """
        Initialize the DataFrame with predefined columns.
        """
        self.dataframe = pd.DataFrame(columns=["operation", "operand1", "operand2", "result"])

    def add_record(self, record: dict):
        """
        Append a new calculation record.

        Args:
            record (dict): A dictionary containing operation details.
        """
        new_row = pd.DataFrame([record])
        self.dataframe = pd.concat([self.dataframe, new_row], ignore_index=True)

    def clear(self):
        """
        Remove all entries from the calculation history.
        """
        self.dataframe = pd.DataFrame(columns=self.dataframe.columns)

    def filter_by_operation(self, operation: str) -> pd.DataFrame:
        """
        Retrieve records filtered by operation type.

        Args:
            operation (str): The operation name.

        Returns:
            pd.DataFrame: Filtered records.
        """
        return self.dataframe[self.dataframe["operation"] == operation]

    def save_to_file(self, path: str):
        """
        Save the DataFrame contents to a CSV file.

        Args:
            path (str): Destination file path.
        """
        self.dataframe.to_csv(path, index=False)

    def load_from_file(self, path: str):
        """
        Load records into the DataFrame from a CSV file.

        Args:
            path (str): Source CSV file path.
        """
        self.dataframe = pd.read_csv(path)

    def delete_record(self, index: int):
        """
        Delete a calculation record by index.

        Args:
            index (int): Row index to delete.
        """
        if 0 <= index < len(self.dataframe):
            self.dataframe.drop(index, inplace=True)
            self.dataframe.reset_index(drop=True, inplace=True)
            print(f"Deleted calculation at index {index}.")
        else:
            print(f"Invalid index: {index}. No record deleted.")
