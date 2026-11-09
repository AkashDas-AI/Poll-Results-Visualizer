"""Data Loader module for Poll Results Visualizer.

Handles reading survey polling data safely, bridging official public datasets
and custom survey files with comprehensive error handling.
Author: Akash Das
"""

from pathlib import Path
from typing import Union, Optional
import pandas as pd

from src.config import COLUMN_MAPPINGS, SO_2025_PUBLIC_CSV
from src.datasets.stackoverflow_2025 import (
    load_survey_data,
    build_poll_adapter_table,
    StackOverflowDataError
)


class DataLoaderError(Exception):
    """Custom exception raised when data loading fails."""
    pass


def load_poll_data(
    file_path: Optional[Union[str, Path]] = None,
    apply_column_mappings: bool = True
) -> pd.DataFrame:
    """Load survey polling data.

    If file_path is None, loads the official Stack Overflow 2025 survey dataset
    via the source adapter. If file_path is provided, loads the target CSV file.

    Args:
        file_path: Path to the CSV file. If None, loads official public dataset.
        apply_column_mappings: If True, maps legacy/synonymous column names to
                               standard schema names.

    Returns:
        pd.DataFrame: Loaded data conforming to standard schema.

    Raises:
        DataLoaderError: If file not found, empty, or cannot be parsed.
    """
    if file_path is None:
        if not SO_2025_PUBLIC_CSV.exists():
            raise DataLoaderError(
                f"Official Stack Overflow 2025 dataset not found at {SO_2025_PUBLIC_CSV}.\n"
                f"Please download the official dataset from:\n"
                "https://media.githubusercontent.com/media/StackExchange/Survey/main/"
                "packages/archive/2025/results.csv\n"
                f"and place it at: {SO_2025_PUBLIC_CSV}"
            )
        try:
            so_df = load_survey_data(SO_2025_PUBLIC_CSV, nrows=5000)
            return build_poll_adapter_table(so_df)
        except StackOverflowDataError as e:
            raise DataLoaderError(str(e)) from e

    target_path = Path(file_path)
    if not target_path.exists():
        raise DataLoaderError(f"Poll data file not found at: {target_path}")

    try:
        df = pd.read_csv(target_path, encoding="utf-8")
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(target_path, encoding="latin-1")
        except Exception as e:
            raise DataLoaderError(f"Failed to parse CSV due to encoding error: {e}") from e
    except pd.errors.EmptyDataError:
        raise DataLoaderError(f"CSV file is empty: {target_path}")
    except Exception as e:
        raise DataLoaderError(f"Error reading CSV file at {target_path}: {e}") from e

    if df.empty:
        raise DataLoaderError(f"The loaded dataset contains 0 records: {target_path}")

    df.columns = [str(c).strip() for c in df.columns]

    if apply_column_mappings:
        df = df.rename(columns=COLUMN_MAPPINGS)

    return df
