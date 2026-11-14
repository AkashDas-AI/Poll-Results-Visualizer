"""Overview Page - Demographics & Fieldwork Telemetry.

Stack Overflow Developer Survey 2025 Visualizer.
Author: Akash Das
Project: Poll Results Visualizer
Phase: Phase 6 — Visualization
"""

import sys
from pathlib import Path
import pandas as pd
import streamlit as st

try:
    import plotly.express as px
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    px = None
    go = None
    HAS_PLOTLY = False

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.data_provider import get_survey_dataset, get_survey_overview_kpis  # noqa: E402
from app.components.kpi_cards import render_survey_executive_kpis  # noqa: E402
from app.components.filters import render_survey_demographic_filters  # noqa: E402
from app.components.theme import apply_custom_theme, apply_chart_theme  # noqa: E402
from app.components.charts import (  # noqa: E402
    plot_horizontal_bar_with_denominators,
    render_plotly_chart,
    CHART_FONT_FAMILY,
    DEFAULT_CHART_TEMPLATE,
)
from src.datasets.stackoverflow_2025 import analyze_multi_select  # noqa: E402

st.set_page_config(
    page_title="Demographics & Fieldwork - SO 2025",
    page_icon="📈",
    layout="wide",
)

AGE_ORDER = [
    "Under 18 years old",
    "18-24 years old",
    "25-34 years old",
    "35-44 years old",
    "45-54 years old",
    "55-64 years old",
    "65 years or older",
    "Prefer not to say",
]


def main():
    apply_custom_theme()
    st.title("📈 Survey Fieldwork & Demographics Overview")
    st.caption("Executive telemetry, demographic composition, and population denominator accounting.")

    # Methodology & Denominator Notice
    st.warning(
        "⚠️ **Survey Methodology & Population Framework:**\n\n"
        "- **Standardized Population Terminology:**\n"
        "  - **N_raw = 49,191**: Total unweighted rows in the downloadable public CSV extract.\n"
        "  - **N_official = 49,009**: Official qualified responses analyzed in Stack Overflow's web report "
        "(182-row qualification filter difference due to time-spent <3 min filters).\n"
        "  - **N_answered**: Question-specific non-missing responses in the raw extract.\n"
        "- **Non-Probability Opt-In Sample:** Sourced via Stack Overflow owned channels; reflects an engaged, "
        "self-selected community. All reported proportions are observational."
    )

    # Load canonical cleaned dataset
    try:
        full_df = get_survey_dataset()
        kpis = get_survey_overview_kpis()
    except Exception as e:
        st.error(f"Failed to load dataset: {e}")
        st.stop()

    # Sidebar Cohort Filtering
    filtered_df, selections = render_survey_demographic_filters(full_df, enable_comp_trim=False, key_prefix="ov_")
    n_filtered = len(filtered_df)
    n_total = len(full_df)

    # Executive Telemetry KPIs
    st.subheader("Official Fieldwork Telemetry")
    render_survey_executive_kpis(kpis, n_current=n_filtered, show_salary=True)

    st.markdown("---")

    # Section 1: Demographics
    st.subheader("1. Demographic Composition")
    col_age, col_ed = st.columns(2)

    with col_age:
        st.markdown("#### Age Distribution")
        age_valid = filtered_df["Age"].dropna()
        n_age_ans = len(age_valid)

        if n_age_ans > 0:
            age_counts = age_valid.value_counts().to_dict()
            # Sort according to natural age order
            ordered_ages = [a for a in AGE_ORDER if a in age_counts]
            other_ages = [a for a in age_counts if a not in AGE_ORDER]
            all_ordered = ordered_ages + other_ages

            age_df = pd.DataFrame({
                "Age Bracket": all_ordered,
                "Count": [age_counts[a] for a in all_ordered],
            })
            age_df["Percentage"] = (age_df["Count"] / n_age_ans) * 100.0

            if HAS_PLOTLY:
                fig_age = px.bar(
                    age_df,
                    x="Age Bracket",
                    y="Percentage",
                    text=age_df["Percentage"].apply(lambda v: f"{v:.1f}%"),
                    title="<b>Respondent Age Cohort Distribution</b>",
                    color="Percentage",
                    color_continuous_scale="Blues",
                )
                fig_age.update_layout(
                    showlegend=False,
                    yaxis_title="Share of Answered Respondents (%)",
                    xaxis_title="",
                    margin=dict(l=20, r=20, t=50, b=30),
                )
                apply_chart_theme(fig_age)
                render_plotly_chart(fig_age)
            else:
                render_plotly_chart(None, "Respondent Age Cohort Distribution requires the 'plotly' package.")
            modal_idx = age_df["Count"].idxmax()
            modal_row = age_df.loc[modal_idx]
            modal_cohort = modal_row["Age Bracket"]
            modal_count = int(modal_row["Count"])
            modal_pct = modal_row["Percentage"]
            filter_note = f" (filtered from {n_total:,})" if n_age_ans < n_total else ""
            st.caption(
                f"Question Answered: N_answered = {n_age_ans:,}{filter_note} | "
                f"Modal Cohort: {modal_cohort} with {modal_count:,} respondents ({modal_pct:.2f}% of answered)."
            )
        else:
            st.info("No age data available for current filter.")

    with col_ed:
        st.markdown("#### Highest Education Level (`EdLevel`)")
        ed_valid = filtered_df["EdLevel"].dropna()
        n_ed_ans = len(ed_valid)

        if n_ed_ans > 0:
            ed_counts = ed_valid.value_counts().reset_index()
            ed_counts.columns = ["Education Level", "Count"]

            # Shorten labels for clean display
            short_labels = {
                "Bachelor’s degree (B.A., B.S., B.Eng., etc.)": "Bachelor's degree",
                "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)": "Master's degree",
                "Some college/university study without earning a degree": "Some college / No degree",
                "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)": (
                    "Secondary school"
                ),
                "Professional degree (JD, MD, Ph.D, Ed.D, etc.)": "Professional degree (PhD/MD)",
                "Associate degree (A.A., A.S., etc.)": "Associate degree",
                "Primary/elementary school": "Primary school",
                "Something else": "Something else",
            }
            ed_counts["Display Label"] = ed_counts["Education Level"].map(lambda x: short_labels.get(x, x))

            fig_ed = plot_horizontal_bar_with_denominators(
                ed_counts,
                category_col="Display Label",
                count_col="Count",
                n_answered=n_ed_ans,
                n_total=n_total,
                title="Education Level Distribution",
                top_n=8,
                color_scale="Blues",
            )
            render_plotly_chart(fig_ed)
            st.caption(
                f"Question Answered: N_answered = {n_ed_ans:,} | "
                "Hover reveals exact counts, % of answered, and % of total survey pool."
            )
        else:
            st.info("No education data available for current filter.")

    # Experience Comparison
    st.markdown("#### Developer Experience: Total Coding (`YearsCode_num`) vs. Professional (`WorkExp_num`)")
    exp_col1, exp_col2 = st.columns([2, 1])

    with exp_col1:
        yc_series = filtered_df["YearsCode_num"].dropna()
        we_series = filtered_df["WorkExp_num"].dropna()

        if not yc_series.empty and not we_series.empty:
            if HAS_PLOTLY:
                fig_exp = go.Figure()
                fig_exp.add_trace(
                    go.Box(
                        x=yc_series,
                        name="Years Coding (YearsCode_num)",
                        marker_color="#3B82F6",
                        boxpoints=False,
                    )
                )
                fig_exp.add_trace(
                    go.Box(
                        x=we_series,
                        name="Professional Work Exp (WorkExp_num)",
                        marker_color="#22C55E",
                        boxpoints=False,
                    )
                )
                fig_exp.update_layout(
                    title="<b>Experience Distributions: Total Coding vs. Professional Work Experience</b>",
                    xaxis_title="Years of Experience",
                    margin=dict(l=20, r=20, t=50, b=30),
                    height=260,
                )
                apply_chart_theme(fig_exp)
                render_plotly_chart(fig_exp)
            else:
                render_plotly_chart(None, "Coding vs. Work Experience boxplot requires the 'plotly' package.")
        else:
            st.info("Insufficient experience data for box plot.")

    with exp_col2:
        st.markdown("**Distribution Moments Summary**")
        moments_df = pd.DataFrame([
            {
                "Metric": "Valid Answered (N)",
                "Total Coding": f"{len(yc_series):,}",
                "Professional Work": f"{len(we_series):,}",
            },
            {
                "Metric": "Mean (Years)",
                "Total Coding": f"{yc_series.mean():.2f}" if not yc_series.empty else "N/A",
                "Professional Work": f"{we_series.mean():.2f}" if not we_series.empty else "N/A",
            },
            {
                "Metric": "Median (Years)",
                "Total Coding": f"{yc_series.median():.1f}" if not yc_series.empty else "N/A",
                "Professional Work": f"{we_series.median():.1f}" if not we_series.empty else "N/A",
            },
            {
                "Metric": "Std Dev (Years)",
                "Total Coding": f"{yc_series.std():.2f}" if not yc_series.empty else "N/A",
                "Professional Work": f"{we_series.std():.2f}" if not we_series.empty else "N/A",
            },
        ])
        st.dataframe(moments_df, hide_index=True, use_container_width=True)
        st.caption(
            "Note: Total coding experience consistently exceeds professional work experience because respondents "
            "often begin coding recreationally or academically prior to professional employment."
        )

    st.markdown("---")

    # Section 2: Employment & Working Arrangements
    st.subheader("2. Employment Status & Working Arrangements")
    col_emp, col_rw = st.columns(2)

    with col_emp:
        st.markdown("#### Primary Employment Status (`Employment`)")
        if "Employment" in filtered_df.columns:
            emp_dist = analyze_multi_select(filtered_df, "Employment", delimiter=";")
            n_emp_ans = len(filtered_df["Employment"].dropna())

            if not emp_dist.empty:
                fig_emp = plot_horizontal_bar_with_denominators(
                    emp_dist,
                    category_col="option",
                    count_col="response_count",
                    n_answered=n_emp_ans,
                    n_total=n_total,
                    title="Employment Status Breakdown (Multi-Select)",
                    top_n=8,
                    color_scale="Blues",
                )
                render_plotly_chart(fig_emp)
                st.caption(
                    f"Multi-select question: Respondents may select multiple statuses. "
                    f"N_answered = {n_emp_ans:,} respondents."
                )

    with col_rw:
        st.markdown("#### Working Arrangement (`RemoteWork`)")
        if "RemoteWork" in filtered_df.columns:
            rw_valid = filtered_df["RemoteWork"].dropna()
            n_rw_ans = len(rw_valid)

            if n_rw_ans > 0:
                rw_counts = rw_valid.value_counts().reset_index()
                rw_counts.columns = ["Arrangement", "Count"]

                fig_rw = plot_horizontal_bar_with_denominators(
                    rw_counts,
                    category_col="Arrangement",
                    count_col="Count",
                    n_answered=n_rw_ans,
                    n_total=n_total,
                    title="Working Arrangement Breakdown",
                    color_scale="Teal",
                )
                render_plotly_chart(fig_rw)
                st.caption(
                    f"N_answered = {n_rw_ans:,} | Non-response: {n_total - n_rw_ans:,} respondents omitted. "
                    "RemoteWork nonresponse is associated with respondent branch. "
                    "The observed association suggests that missingness is not MCAR with respect to MainBranch. "
                    "The available data alone cannot distinguish MAR from MNAR."
                )

    st.markdown("---")

    # Section 3: Geographic Distribution
    st.subheader("3. Geographic Distribution (Top 15 Countries)")
    if "Country" in filtered_df.columns:
        c_valid = filtered_df["Country"].dropna()
        n_c_ans = len(c_valid)

        if n_c_ans > 0:
            c_counts = c_valid.value_counts().reset_index()
            c_counts.columns = ["Country", "Count"]

            fig_country = plot_horizontal_bar_with_denominators(
                c_counts,
                category_col="Country",
                count_col="Count",
                n_answered=n_c_ans,
                n_total=n_total,
                title="Top 15 Respondent Countries",
                top_n=15,
                color_scale="Blues",
                height=450,
            )
            render_plotly_chart(fig_country)

            with st.expander("📋 View Complete Country Distribution Table"):
                c_counts["Pct_Answered"] = (c_counts["Count"] / n_c_ans * 100.0).round(2)
                c_counts["Pct_Total_Survey"] = (c_counts["Count"] / n_total * 100.0).round(2)
                st.dataframe(c_counts, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
