"""Unit tests for the wide-format Stack Overflow 2025 cleaning pipeline.

Author: Akash Das
Project: Poll Results Visualizer
Phase: Phase 3 — Cleaning
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from src.data_validation import DataValidationError
from src.datasets.stackoverflow_cleaning import (
    clean_experience_value,
    classify_experience_value,
    clean_experience_series,
    normalize_multiselect_string,
    normalize_multiselect_series,
    clean_stackoverflow_survey,
    save_processed_dataset,
    compute_file_sha256,
)


def test_classify_experience_value():
    """Verify classification tags distinguish observed numbers from boundary assumptions."""
    num, tag = classify_experience_value(15)
    assert num == 15.0 and tag == "observed_numeric"

    num, tag = classify_experience_value("7.5")
    assert num == 7.5 and tag == "observed_numeric"

    num, tag = classify_experience_value("Less than 1 year")
    assert num == 0.5 and tag == "boundary_less_than_one"

    num, tag = classify_experience_value("More than 50 years")
    assert num == 51.0 and tag == "boundary_more_than_fifty"

    num, tag = classify_experience_value(None)
    assert np.isnan(num) and tag == "missing"

    num, tag = classify_experience_value("invalid_str")
    assert np.isnan(num) and tag == "unparseable"


def test_clean_experience_value_scalar():
    """Verify scalar conversion of numeric and text-boundary experience values."""
    # Standard numbers
    assert clean_experience_value(10) == 10.0
    assert clean_experience_value(14.5) == 14.5
    assert clean_experience_value("7") == 7.0
    assert clean_experience_value("25.0") == 25.0

    # Boundary text values (with default assumptions: <1 -> 0.5, >50 -> 51.0)
    assert clean_experience_value("Less than 1 year") == 0.5
    assert clean_experience_value("less than 1 year") == 0.5
    assert clean_experience_value("  Less than 1 year  ") == 0.5
    assert clean_experience_value("<1") == 0.5
    assert clean_experience_value("< 1") == 0.5

    assert clean_experience_value("More than 50 years") == 51.0
    assert clean_experience_value("more than 50 years") == 51.0
    assert clean_experience_value(">50") == 51.0
    assert clean_experience_value("> 50") == 51.0
    assert clean_experience_value("50+") == 51.0

    # Custom mapping parameters
    assert clean_experience_value("Less than 1 year", less_than_one_val=0.0) == 0.0
    assert clean_experience_value("More than 50 years", more_than_fifty_val=55.0) == 55.0

    # Null, empty, negative, and invalid text
    assert np.isnan(clean_experience_value(None))
    assert np.isnan(clean_experience_value(np.nan))
    assert np.isnan(clean_experience_value(""))
    assert np.isnan(clean_experience_value("   "))
    assert np.isnan(clean_experience_value(-5))
    assert np.isnan(clean_experience_value("invalid_experience"))


def test_clean_experience_series():
    """Verify Series conversion with mixed numeric, text, and null inputs."""
    s = pd.Series(["Less than 1 year", "5", "More than 50 years", None, "20", "invalid"])
    res = clean_experience_series(s)
    assert len(res) == 6
    assert res.iloc[0] == 0.5
    assert res.iloc[1] == 5.0
    assert res.iloc[2] == 51.0
    assert np.isnan(res.iloc[3])
    assert res.iloc[4] == 20.0
    assert np.isnan(res.iloc[5])


def test_normalize_multiselect_string():
    """Verify semicolon delimiter hygiene while preserving legitimate technology labels."""
    # Standard multi-select with whitespace and redundant semicolons
    raw_str = ";Python; ; JavaScript;; HTML/CSS ; "
    expected = "Python;JavaScript;HTML/CSS"
    assert normalize_multiselect_string(raw_str) == expected

    # Preserves tokens with special symbols (.NET, C++, C#)
    c_str = " C++ ; C# ; .NET ; Bash/Shell (all shells) "
    assert normalize_multiselect_string(c_str) == "C++;C#;.NET;Bash/Shell (all shells)"

    # Empty or null strings
    assert pd.isna(normalize_multiselect_string(None))
    assert pd.isna(normalize_multiselect_string(""))
    assert pd.isna(normalize_multiselect_string("   ; ;   "))


def test_normalize_multiselect_series():
    """Verify multi-select normalization across a Series."""
    s = pd.Series(["Python; JavaScript", ";;Rust;;", None, "Docker ; Kubernetes "])
    res = normalize_multiselect_series(s)
    assert res.iloc[0] == "Python;JavaScript"
    assert res.iloc[1] == "Rust"
    assert pd.isna(res.iloc[2])
    assert res.iloc[3] == "Docker;Kubernetes"


def test_clean_stackoverflow_survey_synthetic():
    """Verify wide survey cleaning pipeline on synthetic multi-column survey data."""
    df = pd.DataFrame({
        "ResponseId": [1, 2, 3, 4],
        "Age": [" 25-34 years old ", "18-24 years old", "35-44 years old", "25-34 years old"],
        "YearsCode": ["Less than 1 year", "5", "More than 50 years", None],
        "WorkExp": [0, "3", "12", None],
        "CompTotal": [100000.0, None, 85000.0, 50000.0],
        "Currency": ["USD United States dollar", None, "EUR European Euro", "INR Indian rupee"],
        "ConvertedCompYearly": [100000.0, None, 92000.0, 0.0],
        "LanguageHaveWorkedWith": ["; Python ; JavaScript ;", "Rust; Go", None, " C++ ; C# "],
    })

    cleaned, meta = clean_stackoverflow_survey(df)

    # 1. Output dimensions and metadata check
    assert meta["initial_rows"] == 4
    assert meta["final_rows"] == 4
    assert meta["dropped_missing_id"] == 0
    assert meta["duplicates_removed"] == 0
    assert "YearsCode_num" in meta["derived_columns_added"]
    assert "WorkExp_num" in meta["derived_columns_added"]
    assert "Comp_valid_usd" in meta["derived_columns_added"]

    # 2. Original columns are preserved untouched
    assert cleaned["YearsCode"].iloc[0] == "Less than 1 year"
    assert cleaned["LanguageHaveWorkedWith"].iloc[0] == "Python;JavaScript"

    # 3. Derived numeric columns are correctly calculated
    assert cleaned["YearsCode_num"].iloc[0] == 0.5
    assert cleaned["YearsCode_num"].iloc[1] == 5.0
    assert cleaned["YearsCode_num"].iloc[2] == 51.0
    assert np.isnan(cleaned["YearsCode_num"].iloc[3])

    # 4. Compensation validation flag (non-null and > 0)
    assert cleaned["Comp_valid_usd"].iloc[0] is True or cleaned["Comp_valid_usd"].iloc[0] == 1
    assert cleaned["Comp_valid_usd"].iloc[1] is False or cleaned["Comp_valid_usd"].iloc[1] == 0
    assert cleaned["Comp_valid_usd"].iloc[2] is True or cleaned["Comp_valid_usd"].iloc[2] == 1
    assert cleaned["Comp_valid_usd"].iloc[3] is False or cleaned["Comp_valid_usd"].iloc[3] == 0  # 0.0 is not > 0

    # 5. Compensation status categorization
    assert "Comp_status" in meta["derived_columns_added"]
    assert cleaned["Comp_status"].iloc[0] == "reported_usd"
    assert cleaned["Comp_status"].iloc[1] == "omitted"
    assert cleaned["Comp_status"].iloc[2] == "reported_usd"
    assert cleaned["Comp_status"].iloc[3] == "non_positive_usd"

    # 6. String whitespace stripped
    assert cleaned["Age"].iloc[0] == "25-34 years old"


def test_clean_stackoverflow_survey_with_yearscodepro():
    """Verify YearsCodePro is parsed into YearsCodePro_num when present in dataset."""
    df = pd.DataFrame({
        "ResponseId": [101, 102, 103],
        "YearsCodePro": ["Less than 1 year", "8", "More than 50 years"],
    })
    cleaned, meta = clean_stackoverflow_survey(df)
    assert "YearsCodePro_num" in meta["derived_columns_added"]
    assert cleaned["YearsCodePro_num"].iloc[0] == 0.5
    assert cleaned["YearsCodePro_num"].iloc[1] == 8.0
    assert cleaned["YearsCodePro_num"].iloc[2] == 51.0
    assert meta["experience_conversion_stats"]["YearsCodePro"]["derived_valid_count"] == 3


def test_clean_stackoverflow_survey_missing_id_and_empty_errors():
    """Verify error handling on empty DataFrames or missing ResponseId column."""
    with pytest.raises(DataValidationError, match="Cannot clean an empty DataFrame"):
        clean_stackoverflow_survey(pd.DataFrame())

    df_no_id = pd.DataFrame({"Age": ["25-34"], "YearsCode": [5]})
    with pytest.raises(DataValidationError, match="Missing mandatory primary key"):
        clean_stackoverflow_survey(df_no_id)


def test_clean_stackoverflow_survey_drops_null_ids():
    """Verify rows missing primary identifier are excluded."""
    df = pd.DataFrame({
        "ResponseId": [1, None, 3],
        "Age": ["25-34", "18-24", "35-44"],
    })
    cleaned, meta = clean_stackoverflow_survey(df)
    assert len(cleaned) == 2
    assert meta["dropped_missing_id"] == 1
    assert list(cleaned["ResponseId"]) == [1.0, 3.0]


def test_save_processed_dataset(tmp_path):
    """Verify export to Parquet and CSV with SHA-256 hash generation."""
    df = pd.DataFrame({
        "ResponseId": [1, 2],
        "Age": ["25-34 years old", "35-44 years old"],
        "YearsCode_num": [5.0, 10.0],
    })
    results = save_processed_dataset(
        df,
        output_dir=tmp_path,
        basename="test_cleaned",
        formats=("parquet", "csv"),
    )
    assert "parquet" in results
    assert "csv" in results

    p_file = Path(results["parquet"]["path"])
    c_file = Path(results["csv"]["path"])

    assert p_file.exists()
    assert c_file.exists()
    assert results["parquet"]["rows"] == 2
    assert results["csv"]["rows"] == 2

    # Verify SHA-256 re-computation matches
    assert compute_file_sha256(p_file) == results["parquet"]["sha256"]
    assert compute_file_sha256(c_file) == results["csv"]["sha256"]


def test_processed_dataset_integrity_on_disk():
    """Verify the canonical processed dataset generated in data/processed/."""
    parquet_path = Path("data/processed/survey_results_cleaned.parquet")
    csv_path = Path("data/processed/survey_results_cleaned.csv")

    if not parquet_path.exists() or not csv_path.exists():
        pytest.skip("Processed dataset files not present on disk (expected in fresh git clone)")

    df_p = pd.read_parquet(parquet_path)
    assert len(df_p) == 49191
    assert len(df_p.columns) == 176
    assert "ResponseId" in df_p.columns
    assert "YearsCode_num" in df_p.columns
    assert "WorkExp_num" in df_p.columns
    assert "Comp_valid_usd" in df_p.columns
    assert "Comp_status" in df_p.columns

    # Verify deterministic hash matches
    expected_parquet_hash = "16f5ce8e8f387405fa9635e44074dc468f44b82c0ee23287b2889be238fbbe52"
    assert compute_file_sha256(parquet_path) == expected_parquet_hash
