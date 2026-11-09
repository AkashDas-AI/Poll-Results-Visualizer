"""Cached Data Provider for Poll Results Visualizer Streamlit Application.

Provides centralized, cached access to the cleaned Stack Overflow 2025 Parquet dataset,
survey schema dictionary, and Phase 5 analytical summary metrics.

Author: Akash Das
Project: Poll Results Visualizer
Phase: Phase 6 — Visualization
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional
import pandas as pd
import streamlit as st

from src.datasets.stackoverflow_2025 import (
    load_cleaned_survey_data,
    load_survey_schema,
    get_survey_kpis,
    DEFAULT_CLEANED_PARQUET_PATH,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
METRICS_JSON_PATH = PROJECT_ROOT / "outputs" / "analysis_summary_metrics.json"


@st.cache_data(show_spinner=False)
def get_survey_dataset(parquet_path: Optional[str] = None) -> pd.DataFrame:
    """Retrieve the cleaned 49,191-row Stack Overflow 2025 dataset with caching.

    Args:
        parquet_path: Optional custom path to Parquet file.

    Returns:
        pd.DataFrame: Cleaned survey dataset.
    """
    path = parquet_path or str(DEFAULT_CLEANED_PARQUET_PATH)
    return load_cleaned_survey_data(path)


@st.cache_data(show_spinner=False)
def get_survey_schema_dict() -> pd.DataFrame:
    """Retrieve the survey schema questionnaire dictionary with caching."""
    try:
        return load_survey_schema()
    except Exception:
        return pd.DataFrame(columns=["qid", "qname", "question", "type"])


@st.cache_data(show_spinner=False)
def get_survey_overview_kpis() -> Dict[str, Any]:
    """Retrieve executive overview KPIs computed from the canonical dataset."""
    df = get_survey_dataset()
    return get_survey_kpis(df)


@st.cache_data(show_spinner=False)
def get_analysis_summary_metrics() -> Dict[str, Any]:
    """Retrieve Phase 5 statistical model outputs and summary metrics from JSON."""
    if METRICS_JSON_PATH.exists():
        try:
            with open(METRICS_JSON_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}
