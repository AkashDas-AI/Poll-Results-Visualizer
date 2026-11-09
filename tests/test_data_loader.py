"""Unit tests for data loader module.

Author: Akash Das
"""

import pytest
import pandas as pd

from src.data_loader import load_poll_data, DataLoaderError
from src.config import REQUIRED_COLUMNS, COL_OPTION


def test_load_sample_data_success(tmp_path):
    """Verify that sample poll data loads successfully from a fixture CSV."""
    fixture_path = tmp_path / "test_poll.csv"
    fixture_path.write_text(
        "respondent_id,question,option,response_date,segment\n"
        "R1,Q1,Yes,2024-01-01,Age 18-34\n"
        "R2,Q1,No,2024-01-02,Age 35-54\n",
        encoding="utf-8"
    )
    df = load_poll_data(fixture_path)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) == 2
    for col in REQUIRED_COLUMNS:
        assert col in df.columns


def test_load_nonexistent_file_raises_error(tmp_path):
    """Verify that attempting to load a non-existent file raises DataLoaderError."""
    fake_path = tmp_path / "nonexistent.csv"
    with pytest.raises(DataLoaderError, match="not found"):
        load_poll_data(fake_path)


def test_load_empty_file_raises_error(tmp_path):
    """Verify that loading an empty file raises DataLoaderError."""
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("")
    with pytest.raises(DataLoaderError):
        load_poll_data(empty_file)


def test_load_column_mapping(tmp_path):
    """Verify legacy column names like option_selected are safely remapped to option."""
    csv_file = tmp_path / "legacy.csv"
    csv_file.write_text(
        "respondent_id,question,option_selected,response_date,segment\n"
        "R1,Q1,Yes,2024-01-01,Age 18-34\n"
    )
    df = load_poll_data(csv_file, apply_column_mappings=True)
    assert COL_OPTION in df.columns
    assert "option_selected" not in df.columns
