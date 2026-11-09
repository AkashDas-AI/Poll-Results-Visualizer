"""Data Validation module for Poll Results Visualizer.

Validates schema compliance, required columns, and flags data anomalies.
Author: Akash Das
"""

from typing import Dict, Any, List
import pandas as pd

from src.config import (
    REQUIRED_COLUMNS,
    COL_RESPONDENT_ID,
    COL_QUESTION,
    COL_OPTION,
    COL_RESPONSE_DATE,
)


class DataValidationError(Exception):
    """Custom exception raised when data validation fails critical checks."""
    pass


def validate_schema(df: pd.DataFrame, required_columns: List[str] = REQUIRED_COLUMNS) -> Dict[str, Any]:
    """Validate that the DataFrame contains all required columns.

    Args:
        df: Input DataFrame to check.
        required_columns: List of columns required for downstream operations.

    Returns:
        Dict[str, Any]: Validation summary containing status and missing columns.
    """
    if not isinstance(df, pd.DataFrame):
        raise DataValidationError("Input must be a pandas DataFrame.")

    current_cols = set(df.columns)
    missing = [c for c in required_columns if c not in current_cols]

    return {
        "is_valid": len(missing) == 0,
        "missing_columns": missing,
        "existing_columns": list(df.columns),
    }


def validate_poll_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Perform comprehensive data quality inspection on the polling dataset.

    Args:
        df: Input DataFrame.

    Returns:
        Dict[str, Any]: Detailed validation report.
    """
    schema_res = validate_schema(df)
    if not schema_res["is_valid"]:
        return {
            "is_valid": False,
            "errors": [f"Missing required columns: {', '.join(schema_res['missing_columns'])}"],
            "schema_check": schema_res,
            "row_count": len(df),
            "null_counts": {},
            "duplicate_count": 0,
            "invalid_dates": 0,
        }

    total_rows = len(df)
    null_counts = df[REQUIRED_COLUMNS].isnull().sum().to_dict()

    # Identify duplicates: same respondent answering same question
    duplicate_rows = df.duplicated(subset=[COL_RESPONDENT_ID, COL_QUESTION], keep=False).sum()

    # Inspect date column parseability
    parsed_dates = pd.to_datetime(df[COL_RESPONSE_DATE], errors="coerce")
    invalid_dates = parsed_dates.isnull().sum()

    errors = []
    warnings = []

    if total_rows == 0:
        errors.append("Dataset has zero records.")
    if null_counts.get(COL_RESPONDENT_ID, 0) > 0:
        warnings.append(f"{null_counts[COL_RESPONDENT_ID]} records have null respondent_id.")
    if null_counts.get(COL_QUESTION, 0) > 0:
        warnings.append(f"{null_counts[COL_QUESTION]} records have null question.")
    if null_counts.get(COL_OPTION, 0) > 0:
        warnings.append(f"{null_counts[COL_OPTION]} records have null option.")
    if invalid_dates > 0:
        warnings.append(f"{invalid_dates} records have invalid or missing dates.")
    if duplicate_rows > 0:
        warnings.append(f"{duplicate_rows} duplicate responses detected (same respondent and question).")

    is_valid = len(errors) == 0

    return {
        "is_valid": is_valid,
        "errors": errors,
        "warnings": warnings,
        "schema_check": schema_res,
        "row_count": total_rows,
        "null_counts": null_counts,
        "duplicate_count": int(duplicate_rows),
        "invalid_dates": int(invalid_dates),
    }
