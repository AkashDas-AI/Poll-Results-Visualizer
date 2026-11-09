"""Poll Results Visualizer - Main Application Entry Point.

Phase 6: Interactive Data Visualization Experience.
Dataset: Stack Overflow Developer Survey 2025 (Cleaned Parquet, 49,191 Respondents).
Author: Akash Das
Project: Poll Results Visualizer
Phase: Phase 6 — Visualization
"""

import sys
from pathlib import Path
import streamlit as st

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.data_provider import get_survey_dataset, get_survey_overview_kpis  # noqa: E402
from app.components.kpi_cards import render_survey_executive_kpis  # noqa: E402
from app.components.theme import apply_custom_theme  # noqa: E402

st.set_page_config(
    page_title="Poll Results Visualizer - SO 2025",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    apply_custom_theme()
    st.title("📊 Stack Overflow Developer Survey 2025 Visualizer")
    st.caption("A modular, interactive analytics platform for public opinion and survey research.")

    # Authorship Banner
    st.info("👤 **Project Author:** Akash Das | **Phase 6:** Production Interactive Visualization Suite")

    # Survey Methodology & Population Notice
    st.warning(
        "⚠️ **Survey Methodology & Population Framework:**\n\n"
        "- **Standardized Population Terminology:**\n"
        "  - **N_raw = 49,191**: All unweighted rows in the downloadable public CSV extract.\n"
        "  - **N_official = 49,009**: Official qualified respondents reported in Stack Overflow's web report.\n"
        "  - **N_answered**: Question-specific non-missing responses in the raw extract.\n"
        "- **Public Extract Limitation:** The public CSV does not flag the 182 unqualified rows dropped by Stack "
        "Overflow's internal time-spent (<3 min) and screening filters. All project-derived percentages use "
        "N_answered from the raw extract.\n"
        "- **Non-Probability Opt-In Sample:** Sourced via Stack Overflow owned media; over-represents engaged "
        "community members. No population weighting is applied. Findings reflect observational associations without "
        "causal claims."
    )

    # Load dataset via cached provider
    try:
        df = get_survey_dataset()
        kpis = get_survey_overview_kpis()
    except Exception as e:
        st.error(f"### ⚠️ Failed to load cleaned survey dataset\n\n{e}")
        st.info("Ensure `data/processed/survey_results_cleaned.parquet` is present in the project workspace.")
        st.stop()

    # High-level KPIs
    st.subheader("Official Survey Telemetry (2025)")
    render_survey_executive_kpis(kpis, show_salary=True)

    st.markdown("---")

    # Navigation Directory Cards
    st.subheader("🧭 Application Analytical Modules")
    st.caption("Select a dedicated analytical section from the sidebar or click below to explore:")

    col_nav1, col_nav2 = st.columns(2)

    with col_nav1:
        st.markdown(
            """
            #### [📈 Page 1: Demographics & Fieldwork](Overview)
            - **Demographic Composition:** Age cohorts, Education (`EdLevel`), and Experience distributions.
            - **Employment & Working Arrangements:** Full-time, Contractor, and Remote work breakdown.
            - **Geographic Footprint:** Top 15 respondent countries with dual-percentage accounting.
            - **Population Framework:** Systematic explanation of $N_{\\text{raw}}$, $N_{\\text{official}}$,
              and $N_{\\text{answered}}$.
            """
        )
        st.markdown("---")
        st.markdown(
            """
            #### [👥 Page 3: Segment Comparison & Compensation](Segment_Comparison)
            - **Developer Role Analysis:** Median compensation and distributions across 20+ roles (including DevOps).
            - **Geographic Compensation:** Cross-country earnings comparisons and experience gradients.
            - **Experience vs. Earnings:** Quadratic Mincerian return profiles and quartile breakdowns.
            - **Remote Work Dynamics:** Neutral observational framing explaining why raw ~50-70% differences
              attenuate to ~30-34% under econometric controls.
            """
        )

    with col_nav2:
        st.markdown(
            """
            #### [💻 Page 2: Technology & AI Adoption](Response_Analysis)
            - **Programming Languages:** Top 20 languages worked with and dual-percentage respondent shares.
            - **Technology Migration:** Current vs. Desired languages with net momentum and retention metrics.
            - **Databases & Cloud Platforms:** Top 15 database technologies and leading cloud providers.
            - **AI Adoption Hierarchy:** 6-tier AI agent adoption matrix, trust sentiment, and perceived accuracy.
            """
        )
        st.markdown("---")
        st.markdown(
            """
            #### [🛡️ Page 4: Data Quality, Missingness & Governance](Data_Quality)
            - **Missingness Rankings:** Ranked audit of top 20 questions by non-response rate.
            - **Nonresponse Association Audit:** Demonstration that `RemoteWork` nonresponse is associated with
              `MainBranch` (not MCAR).
            - **Sample Flow Accounting:** Funnel tracking $N=49,191 \\to N=23,947 \\to N=23,177 \\to N=22,769$.
            - **Methodological Limitations & Exports:** Opt-in boundaries, exchange-rate caveats, and JSON export.
            """
        )

    st.markdown("---")

    col_about, col_preview = st.columns([3, 2])

    with col_about:
        st.markdown("### 📌 Survey Specifications & Technical Architecture")
        st.markdown(
            """
            - **Dataset Source:** Stack Overflow Annual Developer Survey 2025 (Open Database License v1.0).
            - **Canonical Dimensions:** 49,191 respondent rows $\\times$ 176 attributes in processed Parquet format.
            - **Fielding Window:** May 29, 2025 – June 23, 2025. Timestamps omitted from public release for privacy.
            - **Analytical Rigor:** All statistical estimates, VIF diagnostics, and heteroskedasticity-robust White HC1
              standard errors are computed using validated algorithms in `src.analysis`.
            - **Interactive Filtering:** Interactive sidebar filtering dynamically updates respondent counts
              ($N_{\\text{filtered}}$) across all pages while preserving full population denominators.
            """
        )

    with col_preview:
        st.markdown("### 📋 Respondent Data Preview")
        preview_cols = [
            "ResponseId", "Age", "Employment", "Country", "DevType",
            "YearsCode_num", "WorkExp_num", "ConvertedCompYearly"
        ]
        available_preview = [c for c in preview_cols if c in df.columns]
        st.dataframe(df[available_preview].head(6), use_container_width=True)
        st.caption(f"Showing first 6 respondent profiles from {len(df):,} total cleaned survey records.")


if __name__ == "__main__":
    main()
