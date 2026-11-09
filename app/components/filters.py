"""Dashboard Filter Components.

Provides sidebar controls for question selection, demographic segmentation,
and wide-format survey cohort filtering.

Author: Akash Das
Project: Poll Results Visualizer
Phase: Phase 6 — Visualization
"""

from typing import Any, Dict, List, Tuple
import pandas as pd
import streamlit as st

from src.config import COL_QUESTION, COL_RESPONSE_DATE, COL_SEGMENT

EXPERIENCE_BRACKETS = {
    "Entry-level (0–2 years)": (0.0, 2.0),
    "Junior (3–5 years)": (3.0, 5.0),
    "Mid-level (6–10 years)": (6.0, 10.0),
    "Senior (11–20 years)": (11.0, 20.0),
    "Veteran (21+ years)": (21.0, 100.0),
}


def render_sidebar_filters(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Render interactive sidebar filters for tidy-format poll tables (backward compatibility).

    Args:
        df: Input cleaned tidy DataFrame.

    Returns:
        Tuple[pd.DataFrame, Dict[str, Any]]: Filtered DataFrame and filter selections.
    """
    st.sidebar.header("🔍 Filters & Controls")

    if df.empty or COL_QUESTION not in df.columns:
        st.sidebar.warning("No data available to filter.")
        return df, {}

    # 1. Question selector
    questions = sorted(df[COL_QUESTION].dropna().unique())
    selected_question = st.sidebar.selectbox(
        "Select Survey Question",
        options=questions,
        index=0 if len(questions) > 0 else None,
    )

    # 2. Segment filter
    all_segments = sorted(df[COL_SEGMENT].dropna().unique()) if COL_SEGMENT in df.columns else []
    selected_segments = st.sidebar.multiselect(
        "Filter by Demographic Segment",
        options=all_segments,
        default=all_segments,
    )

    # 3. Date range filter
    selected_date_range = None
    if COL_RESPONSE_DATE in df.columns:
        dates = pd.to_datetime(df[COL_RESPONSE_DATE], errors="coerce").dropna()
        if not dates.empty:
            min_date = dates.min().date()
            max_date = dates.max().date()
            if min_date < max_date:
                selected_date_range = st.sidebar.date_input(
                    "Response Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                )
            else:
                st.sidebar.caption(f"Single Date Sample: {min_date}")

    # Apply filters
    filtered_df = df.copy()

    if selected_segments and COL_SEGMENT in filtered_df.columns:
        filtered_df = filtered_df[filtered_df[COL_SEGMENT].isin(selected_segments)]
    elif COL_SEGMENT in filtered_df.columns:
        filtered_df = filtered_df.iloc[0:0]

    if (
        selected_date_range
        and isinstance(selected_date_range, tuple)
        and len(selected_date_range) == 2
        and COL_RESPONSE_DATE in filtered_df.columns
    ):
        start_d, end_d = selected_date_range
        dates_s = pd.to_datetime(filtered_df[COL_RESPONSE_DATE]).dt.date
        filtered_df = filtered_df[(dates_s >= start_d) & (dates_s <= end_d)]

    selections = {
        "selected_question": selected_question,
        "selected_segments": selected_segments,
        "selected_date_range": selected_date_range,
    }

    return filtered_df, selections


def render_survey_demographic_filters(
    df: pd.DataFrame,
    enable_comp_trim: bool = True,
    key_prefix: str = "filter_",
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Render interactive sidebar cohort controls for wide-format survey dataset.

    Enables multi-dimensional filtering across:
    - Country (Top 10 default with optional all countries)
    - Developer Role / DevType
    - Professional Experience Brackets (WorkExp_num)
    - Working Arrangement (RemoteWork)
    - Compensation Trimming ($1,000 to $1,000,000 USD)

    Args:
        df: Input cleaned survey DataFrame (49,191 rows).
        enable_comp_trim: Whether to display compensation trim toggle.
        key_prefix: Unique key prefix for Streamlit state widgets.

    Returns:
        Tuple[pd.DataFrame, Dict[str, Any]]: Filtered DataFrame and selections dict.
    """
    st.sidebar.header("🔍 Cohort Slicing Controls")

    if df.empty:
        st.sidebar.warning("No survey records available to filter.")
        return df, {}

    n_total = len(df)
    filtered = df.copy()

    # 1. Country Filter
    selected_countries: List[str] = []
    if "Country" in df.columns:
        top_countries = df["Country"].value_counts().head(10).index.tolist()
        all_countries = sorted([str(c) for c in df["Country"].dropna().unique()])

        country_scope = st.sidebar.radio(
            "Country Scope",
            options=["All Countries", "Top 10 Countries Only", "Custom Selection"],
            index=0,
            key=f"{key_prefix}country_scope",
        )

        if country_scope == "Top 10 Countries Only":
            selected_countries = top_countries
            filtered = filtered[filtered["Country"].isin(top_countries)]
        elif country_scope == "Custom Selection":
            selected_countries = st.sidebar.multiselect(
                "Select Countries",
                options=all_countries,
                default=top_countries[:5],
                key=f"{key_prefix}custom_countries",
            )
            if selected_countries:
                filtered = filtered[filtered["Country"].isin(selected_countries)]
            else:
                filtered = filtered.iloc[0:0]
        else:
            selected_countries = all_countries

    # 2. Developer Role (DevType) Filter
    selected_roles: List[str] = []
    if "DevType" in df.columns:
        # Extract top distinct roles
        role_counts = df["DevType"].dropna().value_counts()
        top_roles = role_counts.head(10).index.tolist()
        all_roles = sorted([str(r) for r in role_counts.index])

        role_filter_active = st.sidebar.checkbox(
            "Filter by Developer Role (DevType)",
            value=False,
            key=f"{key_prefix}enable_role_filter",
        )
        if role_filter_active:
            selected_roles = st.sidebar.multiselect(
                "Select Developer Roles",
                options=all_roles,
                default=top_roles[:5],
                key=f"{key_prefix}selected_roles",
            )
            if selected_roles:
                filtered = filtered[filtered["DevType"].isin(selected_roles)]
            else:
                filtered = filtered.iloc[0:0]

    # 3. Professional Experience Brackets (WorkExp_num)
    selected_exp_brackets: List[str] = []
    exp_col = "WorkExp_num" if "WorkExp_num" in df.columns else "YearsCode_num"
    if exp_col in df.columns:
        exp_filter_active = st.sidebar.checkbox(
            "Filter by Professional Experience",
            value=False,
            key=f"{key_prefix}enable_exp_filter",
        )
        if exp_filter_active:
            bracket_names = list(EXPERIENCE_BRACKETS.keys()) + ["Unspecified / Missing"]
            selected_exp_brackets = st.sidebar.multiselect(
                "Select Experience Brackets",
                options=bracket_names,
                default=bracket_names[:3],
                key=f"{key_prefix}selected_exp",
            )
            if selected_exp_brackets:
                masks = []
                for b_name in selected_exp_brackets:
                    if b_name == "Unspecified / Missing":
                        masks.append(filtered[exp_col].isna())
                    elif b_name in EXPERIENCE_BRACKETS:
                        low, high = EXPERIENCE_BRACKETS[b_name]
                        masks.append((filtered[exp_col] >= low) & (filtered[exp_col] <= high))
                if masks:
                    combined_mask = pd.concat(masks, axis=1).any(axis=1)
                    filtered = filtered[combined_mask]
            else:
                filtered = filtered.iloc[0:0]

    # 4. Working Arrangement (RemoteWork)
    selected_remote: List[str] = []
    if "RemoteWork" in df.columns:
        remote_options = sorted([str(r) for r in df["RemoteWork"].dropna().unique()])
        remote_filter_active = st.sidebar.checkbox(
            "Filter by Work Arrangement",
            value=False,
            key=f"{key_prefix}enable_remote_filter",
        )
        if remote_filter_active:
            selected_remote = st.sidebar.multiselect(
                "Select Work Arrangements",
                options=remote_options,
                default=remote_options,
                key=f"{key_prefix}selected_remote",
            )
            if selected_remote:
                filtered = filtered[filtered["RemoteWork"].isin(selected_remote)]
            else:
                filtered = filtered.iloc[0:0]

    # 5. Compensation Outlier Trim
    trim_comp = False
    if enable_comp_trim and "ConvertedCompYearly" in df.columns:
        trim_comp = st.sidebar.checkbox(
            "Trim Compensation Outliers ($1k–$1M USD)",
            value=False,
            help="Restricts compensation to positive values between $1,000 and $1,000,000 USD to prevent skewness.",
            key=f"{key_prefix}trim_comp",
        )
        if trim_comp:
            comp_series = pd.to_numeric(filtered["ConvertedCompYearly"], errors="coerce")
            # Only trim rows where compensation was reported
            valid_comp_mask = comp_series.notna() & (comp_series > 0)
            in_range_mask = (comp_series >= 1000) & (comp_series <= 1000000)
            # Keep unstated comp rows unless user is specifically looking at comp
            filtered = filtered[~valid_comp_mask | in_range_mask]

    n_filtered = len(filtered)
    filter_pct = (n_filtered / max(n_total, 1)) * 100.0

    st.sidebar.markdown("---")
    st.sidebar.metric(
        label="Active Cohort Sample",
        value=f"{n_filtered:,}",
        delta=f"{filter_pct:.1f}% of total ({n_total:,})",
        delta_color="off",
    )

    if n_filtered == 0:
        st.sidebar.warning("⚠️ No records match current filter criteria.")

    selections = {
        "n_filtered": n_filtered,
        "n_total": n_total,
        "filter_pct": filter_pct,
        "selected_countries": selected_countries,
        "selected_roles": selected_roles,
        "selected_exp_brackets": selected_exp_brackets,
        "selected_remote": selected_remote,
        "trim_comp": trim_comp,
    }

    return filtered, selections
