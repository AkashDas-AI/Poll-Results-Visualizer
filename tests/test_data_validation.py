"""Unit tests for data validation module.

Author: Akash Das
"""

import pytest
import pandas as pd

from src.data_validation import (
    validate_schema,
    validate_poll_data,
    DataValidationError,
)
from src.config import REQUIRED_COLUMNS


def test_validate_schema_valid():
    """Verify schema check passes when all required columns are present."""
    df = pd.DataFrame(columns=REQUIRED_COLUMNS)
    res = validate_schema(df)
    assert res["is_valid"] is True
    assert len(res["missing_columns"]) == 0


def test_validate_schema_missing_columns():
    """Verify schema check flags missing required columns."""
    df = pd.DataFrame(columns=["respondent_id", "question"])
    res = validate_schema(df)
    assert res["is_valid"] is False
    assert "option" in res["missing_columns"]
    assert "response_date" in res["missing_columns"]
    assert "segment" in res["missing_columns"]


def test_validate_schema_non_dataframe():
    """Verify passing a non-DataFrame object raises DataValidationError."""
    with pytest.raises(DataValidationError):
        validate_schema({"col": 1})


def test_validate_poll_data_anomalies():
    """Verify validate_poll_data correctly flags duplicates, nulls, and bad dates."""
    data = {
        "respondent_id": ["R1", "R1", "R2"],
        "question": ["Q1", "Q1", "Q1"],
        "option": ["Opt A", "Opt B", "Opt A"],
        "response_date": ["2024-01-01", "not-a-date", "2024-01-03"],
        "segment": ["Cohort 1", None, "Cohort 2"],
    }
    df = pd.DataFrame(data)
    report = validate_poll_data(df)
    assert report["is_valid"] is True  # Schema is valid even with data warnings
    assert report["duplicate_count"] == 2  # R1-Q1 appears twice
    assert report["invalid_dates"] == 1
    assert report["null_counts"]["segment"] == 1


def test_validate_poll_data_empty_dataframe():
    """Verify validate_poll_data flags an empty DataFrame with zero records error."""
    df = pd.DataFrame(columns=["respondent_id", "question", "option", "response_date", "segment"])
    report = validate_poll_data(df)
    assert report["is_valid"] is False
    assert any("zero records" in err for err in report["errors"])
