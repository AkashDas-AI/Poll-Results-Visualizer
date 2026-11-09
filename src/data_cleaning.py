"""Data Cleaning module for Poll Results Visualizer.

Performs deterministic data hygiene: date parsing, segment imputation,
and documented duplicate resolution. Never modifies raw inputs in place.
Author: Akash Das
"""

from typing import Tuple, Dict, Any, Optional
import pandas as pd

from src.config import (
    COL_RESPONDENT_ID,
    COL_QUESTION,
    COL_OPTION,
    COL_RESPONSE_DATE,
    COL_SEGMENT,
    DEFAULT_UNKNOWN_SEGMENT,
    REQUIRED_COLUMNS,
)
from src.data_validation import validate_schema, DataValidationError


def clean_poll_data(
    df: pd.DataFrame,
    deduplicate_policy: Optional[str] = "latest",
    unknown_segment_label: str = DEFAULT_UNKNOWN_SEGMENT,
    drop_unparseable_dates: bool = False,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Clean and standardize survey polling data.

    Duplicate Handling Policy:
        - "latest": Sorts by response_date ascending, then keeps the last record
                    per (respondent_id, question).
        - "first": Keeps the earliest record per (respondent_id, question).
        - "none": Retains all duplicate responses without filtering.

    Missing Values Policy:
        - Missing segments are filled with `unknown_segment_label` (default: 'Unknown').
        - Rows missing mandatory identifiers (`respondent_id`, `question`, `option`) are dropped.
        - Dates are coerced to datetime64. Unparseable dates become NaT or are optionally dropped.

    Args:
        df: Input raw DataFrame.
        deduplicate_policy: Policy for resolving duplicate responses ("latest", "first", or "none").
        unknown_segment_label: Label to assign missing segment values.
        drop_unparseable_dates: Whether to drop rows where date parsing failed.

    Returns:
        Tuple[pd.DataFrame, Dict[str, Any]]: Cleaned DataFrame copy and metadata report.
    """
    # 1. Schema check
    schema_res = validate_schema(df, REQUIRED_COLUMNS)
    if not schema_res["is_valid"]:
        raise DataValidationError(
            f"Cannot clean data due to missing columns: {schema_res['missing_columns']}"
        )

    # 2. Work strictly on a fresh copy
    cleaned = df.copy()
    initial_rows = len(cleaned)

    # 3. Work on string representations while safely identifying null/empty values
    invalid_null_literals = {"", "nan", "none", "null", "<na>", "nat"}

    def is_valid_text(series: pd.Series) -> pd.Series:
        return series.notnull() & (~series.astype(str).str.strip().str.lower().isin(invalid_null_literals))

    # Drop rows with null or empty mandatory fields
    valid_mask = (
        is_valid_text(cleaned[COL_RESPONDENT_ID]) &
        is_valid_text(cleaned[COL_QUESTION]) &
        is_valid_text(cleaned[COL_OPTION])
    )
    cleaned = cleaned[valid_mask].copy()
    rows_after_mandatory = len(cleaned)
    dropped_empty_mandatory = initial_rows - rows_after_mandatory

    # Strip whitespace from string columns
    str_cols = [COL_RESPONDENT_ID, COL_QUESTION, COL_OPTION, COL_SEGMENT]
    for col in str_cols:
        if col in cleaned.columns:
            cleaned[col] = cleaned[col].astype(str).str.strip()

    # 4. Handle missing/blank segments
    invalid_seg_mask = ~is_valid_text(cleaned[COL_SEGMENT])
    cleaned.loc[invalid_seg_mask, COL_SEGMENT] = unknown_segment_label
    cleaned[COL_SEGMENT] = cleaned[COL_SEGMENT].fillna(unknown_segment_label)

    # 6. Date parsing and validation
    cleaned[COL_RESPONSE_DATE] = pd.to_datetime(cleaned[COL_RESPONSE_DATE], errors="coerce")
    invalid_dates_count = int(cleaned[COL_RESPONSE_DATE].isnull().sum())

    if drop_unparseable_dates and invalid_dates_count > 0:
        cleaned = cleaned[cleaned[COL_RESPONSE_DATE].notnull()]

    # 7. Deduplication
    duplicates_removed = 0
    if deduplicate_policy in ("latest", "first"):
        pre_dedup_count = len(cleaned)
        # CRITICAL: If keeping latest, sort by response_date first
        cleaned = cleaned.sort_values(
            by=[COL_RESPONSE_DATE],
            na_position="first"
        )
        keep_arg = "last" if deduplicate_policy == "latest" else "first"
        cleaned = cleaned.drop_duplicates(
            subset=[COL_RESPONDENT_ID, COL_QUESTION],
            keep=keep_arg
        )
        duplicates_removed = pre_dedup_count - len(cleaned)

    # Reset index for downstream clean access
    cleaned = cleaned.reset_index(drop=True)

    metadata = {
        "initial_rows": initial_rows,
        "final_rows": len(cleaned),
        "dropped_empty_mandatory": dropped_empty_mandatory,
        "invalid_dates_count": invalid_dates_count,
        "duplicates_removed": duplicates_removed,
        "deduplicate_policy": deduplicate_policy,
        "unknown_segments_assigned": int((cleaned[COL_SEGMENT] == unknown_segment_label).sum()),
    }

    return cleaned, metadata
