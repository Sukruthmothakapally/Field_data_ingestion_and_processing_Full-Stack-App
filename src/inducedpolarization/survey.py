# src/inducedpolarization/survey.py

import os
import pandas as pd
from .utils import read_file
import pickle

MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024  # 1GB


class InducedPolarizationSurvey:
    """Represents an Induced Polarization survey dataset with utilities for reading,
    filtering, and converting IP data from various formats.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initializes the survey with provided data.

        Args:
            data (pd.DataFrame): The IP dataset.
        """
        self.data = data

    @classmethod
    def from_file(cls, filepath: str):
        """
        Loads and validates a dataset from a given file path. Supports CSV, DAT, BIN.

        Args:
            filepath (str): Path to the dataset file.

        Returns:
            InducedPolarizationSurvey: An initialized survey instance.

        Raises:
            ValueError: If the file exceeds 1GB or is unsupported.
        """
        if os.path.getsize(filepath) > MAX_FILE_SIZE:
            raise ValueError("File exceeds 1GB limit.")

        data = read_file(filepath)
        return cls(data)

    def filter_by_line(self, line_number: int) -> pd.DataFrame:
        """
        Filters the dataset for a specific Line number.

        Args:
            line_number (int): The line to filter on.

        Returns:
            pd.DataFrame: Filtered rows matching the line number.
        """
        return self.data[self.data["Line"] == line_number]

    def filter_by_column(self, column: str, value) -> pd.DataFrame:
        """
        Filters the dataset where a specific column matches the provided value.

        Args:
            column (str): Column name.
            value (Any): Value to match.

        Returns:
            pd.DataFrame: Filtered dataset.
        """
        return self.data[self.data[column] == value]

    def filter_by_spatial(self, tx_east_range, tx_north_range, rx_east_range, rx_north_range) -> pd.DataFrame:
        """
        Filters dataset spatially based on transmitter and receiver east/north coordinate ranges.

        Args:
            tx_east_range (tuple): (min, max) for TxEast1.
            tx_north_range (tuple): (min, max) for TxNorth1.
            rx_east_range (tuple): (min, max) for RxEast1.
            rx_north_range (tuple): (min, max) for RxNorth1.

        Returns:
            pd.DataFrame: Spatially filtered dataset.
        """
        df = self.data
        return df[
            (df["TxEast1"].between(*tx_east_range)) &
            (df["TxNorth1"].between(*tx_north_range)) &
            (df["RxEast1"].between(*rx_east_range)) &
            (df["RxNorth1"].between(*rx_north_range))
        ]

    def to_format(self, fmt: str, output_path: str):
        """
        Converts the dataset to a specified format and saves it to disk.

        Args:
            fmt (str): Format to convert to — one of 'csv', 'dat', or 'bin'.
            output_path (str): Destination file path.

        Raises:
            ValueError: If the requested format is unsupported.
        """
        if fmt == "csv":
            self.data.to_csv(output_path, index=False)
        elif fmt == "dat":
            self.data.to_csv(output_path, sep="\t", index=False)
        elif fmt == "bin":
            with open(output_path, "wb") as f:
                pickle.dump(self.data, f)
        else:
            raise ValueError("Unsupported format")
