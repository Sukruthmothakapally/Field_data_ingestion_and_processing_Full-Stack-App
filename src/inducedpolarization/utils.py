# src/inducedpolarization/utils.py

import pandas as pd
import re

def read_file(filepath: str) -> pd.DataFrame:
    """
    Reads a dataset file in various formats (CSV, DAT, BIN).

    Args:
        filepath (str): Path to the dataset file.

    Returns:
        pd.DataFrame: Parsed dataset.

    Raises:
        ValueError: If format is unsupported.
    """
    if filepath.endswith(".csv"):
        return pd.read_csv(filepath)
    elif filepath.endswith(".dat") or filepath.endswith(".txt"):
        return parse_dat_file(filepath)
    elif filepath.endswith(".bin"):
        import pickle
        with open(filepath, "rb") as f:
            return pickle.load(f)
    else:
        raise ValueError("Unsupported file format")

def parse_dat_file(filepath: str) -> pd.DataFrame:
    """
    Parses a .dat file which includes metadata, column headers, and tabular data.

    The parser assumes that:
    - Column headers start with 'T1X ...'
    - Data rows start with numbers
    - Lines are space-separated

    Args:
        filepath (str): Path to the .dat file.

    Returns:
        pd.DataFrame: Parsed dataset.
    """
    with open(filepath, "r") as f:
        lines = f.readlines()

    headers = []
    data_rows = []

    for i, line in enumerate(lines):
        if line.startswith("T1X"):
            headers = re.split(r"\s+", line.strip())
        elif re.match(r"^\d", line.strip()):
            row = re.split(r"\s+", line.strip())
            data_rows.append(row)

    return pd.DataFrame(data_rows, columns=headers)
