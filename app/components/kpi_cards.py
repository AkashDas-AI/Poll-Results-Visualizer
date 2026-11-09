"""KPI Cards Component for Poll Results Visualizer.

Renders standardized executive metric summary cards for survey telemetry,
demographic cohorts, and analytical summaries.

Author: Akash Das
Project: Poll Results Visualizer
Phase: Phase 6 — Visualization
"""

from typing import Any, Dict, List, Optional
import streamlit as st


def render_kpi_cards(kpis: Dict[str, Any]) -> None:
    """Render high-level KPI cards in a 4-column layout (backward compatibility).

    Args:
        kpis: Dictionary output from `src.analysis.calculate_kpis`.
    """
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Responses",
            value=f"{kpis.get('total_responses', 0):,}",
            help="Total number of survey answer records in the current view.",
        )

    with col2:
        st.metric(
            label="Unique Respondents",
            value=f"{kpis.get('unique_respondents', 0):,}",
            help="Count of distinct respondent IDs.",
        )

    with col3:
        st.metric(
            label="Survey Questions",
            value=kpis.get("total_questions", 0),
            help="Number of distinct survey questions evaluated.",
        )

    with col4:
        date_min = kpis.get("date_min")
        date_max = kpis.get("date_max")
        if date_min and date_max:
            date_span = f"{date_min} to {date_max}"
            disp_value = date_span if len(str(date_span)) <= 22 else f"{date_min}..."
            disp_help = f"Fieldwork time span: {date_span}"
        else:
            disp_value = "Cross-Sectional"
            disp_help = (
                "Single cross-sectional fielding: May 29 – June 23, 2025. "
                "Timestamps omitted from public microdata."
            )

        st.metric(
            label="Fieldwork Timing",
            value=disp_value,
            help=disp_help,
        )


def render_survey_executive_kpis(
    kpis: Dict[str, Any],
    n_current: Optional[int] = None,
    show_salary: bool = True,
) -> None:
    """Render the official 5-to-6 metric telemetry panel for Stack Overflow 2025.

    Displays:
    - Raw Records (N_raw = 49,191)
    - Official Base (N_official = 49,009)
    - Countries (177)
    - Professional Devs % (76.2%)
    - AI Tool Adoption % (81.9%)
    - [Optional] Median Annual Compensation ($75,000 USD)

    Args:
        kpis: Dictionary output from `src.datasets.stackoverflow_2025.get_survey_kpis`.
        n_current: Optional active filtered cohort count to show as delta.
        show_salary: Whether to render the median compensation card.
    """
    num_cols = 6 if show_salary else 5
    cols = st.columns(num_cols)

    n_raw = kpis.get("n_raw", 49191)
    n_official = kpis.get("n_official", 49009)
    countries = kpis.get("countries_count", 177)
    ai_rate = kpis.get("ai_adoption_rate", 78.5)
    ai_count = kpis.get("ai_users_count", 26469)
    ai_ans = kpis.get("n_answered_ai", 33720)
    med_comp = kpis.get("median_comp_usd")

    with cols[0]:
        delta_str = f"Filtered: {n_current:,}" if n_current is not None and n_current != n_raw else None
        st.metric(
            label="Raw Records (N_raw)",
            value=f"{n_raw:,}",
            delta=delta_str,
            delta_color="off",
            help="Total unweighted respondent rows in public CSV extract.",
        )

    with cols[1]:
        st.metric(
            label="Official Qualified Base",
            value=f"{n_official:,}",
            delta="182 screened out",
            delta_color="off",
            help="Official qualified sample reported by Stack Overflow after internal screening filters.",
        )

    with cols[2]:
        st.metric(
            label="Countries & Territories",
            value=f"{countries}",
            help="Total distinct countries and territories represented in respondent pool.",
        )

    with cols[3]:
        st.metric(
            label="Professional Developers",
            value="76.2%",
            delta="N = 37,467",
            delta_color="off",
            help="Proportion of respondents identifying as professional developers by profession.",
        )

    with cols[4]:
        st.metric(
            label="AI Tool Adoption",
            value=f"{ai_rate:.1f}%",
            delta=f"N = {ai_count:,} / {ai_ans:,}",
            delta_color="off",
            help="Proportion of answered respondents who use AI tools daily, weekly, or monthly.",
        )

    if show_salary and len(cols) > 5:
        with cols[5]:
            comp_display = f"${med_comp:,.0f}" if med_comp else "$75,000"
            st.metric(
                label="Median Annual USD",
                value=comp_display,
                delta="N = 23,947 answered",
                delta_color="off",
                help="Official pre-converted annual USD compensation (untrimmed median).",
            )


def render_custom_metric_row(metrics: List[Dict[str, Any]]) -> None:
    """Render a dynamic horizontal row of metric cards.

    Args:
        metrics: List of dicts, each with 'label', 'value', and optional 'delta' and 'help'.
    """
    if not metrics:
        return

    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        with col:
            st.metric(
                label=m.get("label", ""),
                value=str(m.get("value", "")),
                delta=m.get("delta"),
                delta_color=m.get("delta_color", "normal"),
                help=m.get("help"),
            )
