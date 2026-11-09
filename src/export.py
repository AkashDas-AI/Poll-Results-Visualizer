"""Export module for Poll Results Visualizer.

Provides utilities for persisting cleaned datasets and analytical summaries
to local project outputs or preparing downloadable file buffers for the UI.
Author: Akash Das
"""

from pathlib import Path
from typing import Union, Optional
import io
import pandas as pd

from src.config import EXPORTS_DIR


def export_dataframe_to_csv(
    df: pd.DataFrame,
    filename: str,
    output_directory: Optional[Union[str, Path]] = None
) -> Path:
    """Save a DataFrame as a CSV file within the project outputs directory.

    Args:
        df: DataFrame to save.
        filename: Destination filename (e.g., 'cleaned_polls.csv').
        output_directory: Directory path. Defaults to `outputs/exports/`.

    Returns:
        Path: Absolute path to the saved file.
    """
    target_dir = Path(output_directory) if output_directory else EXPORTS_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    dest_file = target_dir / filename
    df.to_csv(dest_file, index=False, encoding="utf-8")
    return dest_file


def get_csv_download_bytes(df: pd.DataFrame) -> bytes:
    """Encode a DataFrame into UTF-8 CSV bytes for Streamlit download buttons.

    Args:
        df: DataFrame to serialize.

    Returns:
        bytes: Encoded CSV byte payload.
    """
    buffer = io.StringIO()
    df.to_csv(buffer, index=False, encoding="utf-8")
    return buffer.getvalue().encode("utf-8")
