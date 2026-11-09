"""Configuration module for Poll Results Visualizer.

Defines dataset paths, column schemas, and application settings.
Author: Akash Das
"""

from pathlib import Path

# Base Paths (Relative to project root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLE_DATA_DIR = DATA_DIR / "sample"

# Official Stack Overflow 2025 Paths
SO_2025_RAW_DIR = RAW_DATA_DIR / "stackoverflow_developer_survey_2025"
SO_2025_PUBLIC_CSV = SO_2025_RAW_DIR / "survey_results_public.csv"
SO_2025_SCHEMA_CSV = SO_2025_RAW_DIR / "survey_results_schema.csv"

# Legacy / Generic Polling Schema
DEFAULT_SAMPLE_PATH = SO_2025_PUBLIC_CSV

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
CHARTS_DIR = OUTPUTS_DIR / "charts"
EXPORTS_DIR = OUTPUTS_DIR / "exports"
LOGS_DIR = OUTPUTS_DIR / "logs"

# Standard Legacy Schema Columns (Kept for backwards compatibility)
COL_RESPONDENT_ID = "respondent_id"
COL_QUESTION = "question"
COL_OPTION = "option"
COL_RESPONSE_DATE = "response_date"
COL_SEGMENT = "segment"

REQUIRED_COLUMNS = [
    COL_RESPONDENT_ID,
    COL_QUESTION,
    COL_OPTION,
    COL_RESPONSE_DATE,
    COL_SEGMENT,
]

# Backward compatibility column mapping
COLUMN_MAPPINGS = {
    "ResponseId": COL_RESPONDENT_ID,
    "response_id": COL_RESPONDENT_ID,
    "user_id": COL_RESPONDENT_ID,
    "option_selected": COL_OPTION,
    "selected_option": COL_OPTION,
    "date": COL_RESPONSE_DATE,
    "demographic": COL_SEGMENT,
    "group": COL_SEGMENT,
}

# Data Quality Defaults
DEFAULT_UNKNOWN_SEGMENT = "Unknown"
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
