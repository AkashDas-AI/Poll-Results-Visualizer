"""Unit tests for data cleaning module.

Author: Akash Das
"""

import pandas as pd
from src.data_cleaning import clean_poll_data
from src.config import COL_SEGMENT, DEFAULT_UNKNOWN_SEGMENT


def test_clean_poll_data_does_not_mutate_original():
    """Verify raw input DataFrame is preserved immutably."""
    raw = pd.DataFrame({
        "respondent_id": ["R1", "R2"],
        "question": ["Q1", "Q1"],
        "option": ["A", "B"],
        "response_date": ["2024-01-01", "2024-01-02"],
        "segment": [None, "Adults"],
    })
    raw_copy = raw.copy(deep=True)
    cleaned, _ = clean_poll_data(raw)
    pd.testing.assert_frame_equal(raw, raw_copy)
    assert cleaned is not raw


def test_clean_poll_data_imputes_unknown_segment():
    """Verify missing segments are assigned the default 'Unknown' label."""
    raw = pd.DataFrame({
        "respondent_id": ["R1", "R2"],
        "question": ["Q1", "Q1"],
        "option": ["A", "B"],
        "response_date": ["2024-01-01", "2024-01-02"],
        "segment": [None, ""],
    })
    cleaned, meta = clean_poll_data(raw)
    assert (cleaned[COL_SEGMENT] == DEFAULT_UNKNOWN_SEGMENT).all()
    assert meta["unknown_segments_assigned"] == 2


def test_clean_poll_data_deduplication_keeps_latest():
    """Verify duplicate responses for the same respondent and question keep the latest date."""
    raw = pd.DataFrame({
        "respondent_id": ["R1", "R1"],
        "question": ["Q1", "Q1"],
        "option": ["Initial Answer", "Updated Answer"],
        "response_date": ["2024-01-01", "2024-01-10"],  # Later date has Updated Answer
        "segment": ["Cohort A", "Cohort A"],
    })
    # Pass unordered deliberately
    raw_reversed = raw.iloc[::-1]

    cleaned, meta = clean_poll_data(raw_reversed, deduplicate_policy="latest")
    assert len(cleaned) == 1
    assert cleaned.iloc[0]["option"] == "Updated Answer"
    assert meta["duplicates_removed"] == 1


def test_clean_poll_data_drops_empty_mandatory_fields():
    """Verify records with missing respondent_id or question or option are excluded."""
    raw = pd.DataFrame({
        "respondent_id": ["R1", None, "R3"],
        "question": ["Q1", "Q1", ""],
        "option": ["A", "B", "C"],
        "response_date": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "segment": ["S1", "S2", "S3"],
    })
    cleaned, meta = clean_poll_data(raw)
    assert len(cleaned) == 1
    assert cleaned.iloc[0]["respondent_id"] == "R1"
    assert meta["dropped_empty_mandatory"] == 2


def test_clean_poll_data_empty_dataframe():
    """Verify clean_poll_data processes an empty DataFrame with schema without error."""
    raw = pd.DataFrame(columns=["respondent_id", "question", "option", "response_date", "segment"])
    cleaned, meta = clean_poll_data(raw)
    assert cleaned.empty
    assert meta["initial_rows"] == 0
    assert meta["final_rows"] == 0
