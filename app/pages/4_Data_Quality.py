"""Data Quality Page - Poll Results Visualizer.

Provides comprehensive missingness rankings, structural non-response audits,
compensation sample flow accounting, experience moments comparison,
and dataset/metrics export capabilities.

Author: Akash Das
Project: Poll Results Visualizer
Phase: Phase 6 — Visualization
"""

import sys
from pathlib import Path
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.data_provider import (  # noqa: E402
    get_survey_dataset,
    METRICS_JSON_PATH,
)
from app.components.theme import apply_custom_theme  # noqa: E402
from app.components.charts import (  # noqa: E402
    plot_missingness_ranking_bar,
    plot_sample_flow_funnel,
)
from src.export import get_csv_download_bytes  # noqa: E402

st.set_page_config(
    page_title="Data Quality & Audit Trail - SO 2025",
    page_icon="🛡️",
    layout="wide",
)


def main():
    apply_custom_theme()
    st.title("🛡️ Data Quality, Missingness & Governance")
    st.caption("Missingness rankings, sample flow accounting, experience moments audit, and governance.")

    # Quality and Governance Framework Notice
    st.warning(
        "⚠️ **Data Governance & Methodological Standards:**\n\n"
        "- **Preservation of Raw Truth:** All raw categorical codes and original survey values are preserved "
        "intact. Hygiene logic derives clean numeric features (`YearsCode_num`, `WorkExp_num`) without destructive "
        "overwrites.\n"
        "- **Nonresponse Association & Missingness Mechanisms:** RemoteWork nonresponse is associated with "
        "respondent branch. The observed association suggests that missingness is not MCAR with respect to MainBranch. "
        "The available data alone cannot distinguish MAR from MNAR.\n"
        "- **Population Boundaries:** Project metrics use N_raw = 49,191 unweighted records. The 182-row gap with "
        "the official published qualified sample (N_official = 49,009) is formally accounted for across all "
        "deliverables."
    )

    try:
        full_df = get_survey_dataset()
    except Exception as e:
        st.error(f"Failed to load dataset: {e}")
        st.stop()

    n_total = len(full_df)

    # Section 1: Missingness Audit
    st.subheader("1. Survey Missingness & Non-Response Ranking")
    st.markdown(
        "Evaluating non-response rates across all 176 survey variables. Questions with the highest missingness "
        "typically represent conditional branch questions (e.g., questions asked only to managers or job seekers)."
    )

    # Compute missingness across all columns
    missing_series = full_df.isna().sum()
    missing_df = pd.DataFrame({
        "column": missing_series.index,
        "missing_count": missing_series.values,
        "missing_pct": (missing_series.values / n_total * 100.0).round(2),
        "non_null_count": n_total - missing_series.values,
    }).sort_values(by="missing_pct", ascending=False)

    col_miss_bar, col_miss_branch = st.columns([3, 2])

    with col_miss_bar:
        fig_miss = plot_missingness_ranking_bar(
            missing_df,
            title="Top 20 Questions by Non-Response / Missingness Rate",
            top_n=20,
        )
        st.plotly_chart(fig_miss, use_container_width=True)

    with col_miss_branch:
        st.markdown("#### Nonresponse Association in `RemoteWork`")
        st.caption("Evaluating nonresponse across professional branches (`MainBranch`).")

        ct = pd.crosstab(full_df["MainBranch"], full_df["RemoteWork"].isna(), margins=True, margins_name="Total")
        ct.columns = ["Answered", "Missing", "Total"]
        ct["Missing Rate (%)"] = (ct["Missing"] / ct["Total"] * 100.0).round(2)

        # Simplify index for clean display
        short_branches = {
            "I am a developer by profession": "Professional Developer",
            "I am learning to code": "Learning to Code",
            "I am not primarily a developer, but I write code sometimes as part of my work/studies": (
                "Occasional Coder / Studies"
            ),
            "I code primarily as a hobby": "Hobbyist Coder",
            "I used to be a developer by profession, but no longer am": "Former Developer",
            "I work with developers or my work supports developers but am not a developer by profession": (
                "Dev Support / Adjacent"
            ),
            "Total": "Total Sample",
        }
        disp_ct = ct.reset_index()
        disp_ct["MainBranch"] = disp_ct["MainBranch"].map(lambda x: short_branches.get(x, x))
        disp_ct = disp_ct.rename(columns={"MainBranch": "Respondent Branch"})

        st.dataframe(disp_ct, hide_index=True, use_container_width=True)
        st.caption(
            "Independence Test: Pearson χ² = 5,333.84, df = 5, p < 0.0001, Cramér's V = 0.3293 | "
            "Total N = 49,191 (Answered: 33,780, Missing: 15,411). "
            "RemoteWork nonresponse is associated with respondent branch. The observed association suggests that "
            "missingness is not MCAR with respect to MainBranch. The available data alone cannot distinguish "
            "MAR from MNAR."
        )

    st.markdown("---")

    # Section 2: Compensation Sample Flow
    st.subheader("2. Compensation Sample Flow & Complete-Case Accounting")
    st.markdown(
        "Tracing the sequential sample reduction from raw unweighted respondents to the final complete-case "
        "econometric estimation sample (Phase 5 Model 3)."
    )

    stage_names = [
        "1. Raw Survey Extract (N_raw)",
        "2. Answered Converted Comp (USD)",
        "3. Trimmed Analytical Sample ($1k–$1M)",
        "4. Model 3 Econometric Complete Cases",
    ]
    stage_counts = [49191, 23947, 23177, 22769]

    col_funnel, col_flow_memo = st.columns([3, 2])

    with col_funnel:
        fig_funnel = plot_sample_flow_funnel(stage_names, stage_counts, title="Compensation Analytical Sample Flow")
        st.plotly_chart(fig_funnel, use_container_width=True)

    with col_flow_memo:
        st.markdown("#### Sample Flow Ledger")
        ledger_data = [
            {
                "Stage": "1. Raw Public Extract",
                "Count": "49,191",
                "Retention": "100.0%",
                "Exclusion Reason": "Baseline unweighted population.",
            },
            {
                "Stage": "2. Reported Converted USD",
                "Count": "23,947",
                "Retention": "48.7%",
                "Exclusion Reason": "25,244 omitted (voluntary non-response, students, hobbyists, unconverted local).",
            },
            {
                "Stage": "3. Trimmed Analytical Sample",
                "Count": "23,177",
                "Retention": "47.1%",
                "Exclusion Reason": "770 excluded (< $1,000 or > $1,000,000 USD extreme self-reporting noise).",
            },
            {
                "Stage": "4. Model 3 Complete Cases",
                "Count": "22,769",
                "Retention": "46.3%",
                "Exclusion Reason": (
                    "408 missing complete covariates across Country, Role, Experience, Remote, and Tech."
                ),
            },
        ]
        st.dataframe(pd.DataFrame(ledger_data), hide_index=True, use_container_width=True)
        st.caption(
            "Every step of sample reduction is transparently accounted for to prevent attrition bias."
        )

    st.markdown("---")

    # Section 3: Experience Distributions Moments Comparison
    st.subheader("3. Experience Distributions Moments Comparison")
    st.markdown(
        "Auditing distribution moments between total coding experience (`YearsCode_num`) and "
        "professional work experience (`WorkExp_num`)."
    )

    yc = full_df["YearsCode_num"].dropna()
    we = full_df["WorkExp_num"].dropna()

    exp_table = pd.DataFrame([
        {
            "Metric": "Column Name",
            "Total Coding Experience": "YearsCode_num",
            "Professional Work Experience": "WorkExp_num",
        },
        {
            "Metric": "Storage Data Type",
            "Total Coding Experience": str(yc.dtype),
            "Professional Work Experience": str(we.dtype),
        },
        {
            "Metric": "Total Rows in Dataset",
            "Total Coding Experience": f"{n_total:,}",
            "Professional Work Experience": f"{n_total:,}",
        },
        {
            "Metric": "Valid Non-Null Count (N)",
            "Total Coding Experience": f"{len(yc):,}",
            "Professional Work Experience": f"{len(we):,}",
        },
        {
            "Metric": "Missing Count",
            "Total Coding Experience": f"{full_df['YearsCode_num'].isna().sum():,}",
            "Professional Work Experience": f"{full_df['WorkExp_num'].isna().sum():,}",
        },
        {
            "Metric": "Mean (Years)",
            "Total Coding Experience": f"{yc.mean():.2f}",
            "Professional Work Experience": f"{we.mean():.2f}",
        },
        {
            "Metric": "Median (Years)",
            "Total Coding Experience": f"{yc.median():.1f}",
            "Professional Work Experience": f"{we.median():.1f}",
        },
        {
            "Metric": "Standard Deviation",
            "Total Coding Experience": f"{yc.std():.2f}",
            "Professional Work Experience": f"{we.std():.2f}",
        },
        {
            "Metric": "Minimum",
            "Total Coding Experience": f"{yc.min():.1f}",
            "Professional Work Experience": f"{we.min():.1f}",
        },
        {
            "Metric": "25th Percentile (Q1)",
            "Total Coding Experience": f"{yc.quantile(0.25):.1f}",
            "Professional Work Experience": f"{we.quantile(0.25):.1f}",
        },
        {
            "Metric": "75th Percentile (Q3)",
            "Total Coding Experience": f"{yc.quantile(0.75):.1f}",
            "Professional Work Experience": f"{we.quantile(0.75):.1f}",
        },
        {
            "Metric": "Maximum",
            "Total Coding Experience": f"{yc.max():.1f}",
            "Professional Work Experience": f"{we.max():.1f}",
        },
    ])

    st.dataframe(exp_table, hide_index=True, use_container_width=True)
    st.info(
        "💡 **Key Insight:** `YearsCode_num` mean (16.57 years) consistently exceeds `WorkExp_num` mean (13.37 years) "
        "because developers frequently explore programming for multiple years academically, informally, or as "
        "hobbyists before entering full-time professional software employment."
    )

    st.markdown("---")

    # Section 4: Methodological Caveats & Governance
    st.subheader("4. Methodological Limitations & Quality Governance")
    col_gov1, col_gov2 = st.columns(2)

    with col_gov1:
        st.markdown(
            """
            #### 1. Non-Probability Opt-In Sampling
            - Sourced through Stack Overflow owned media and banner promotions.
            - Over-represents active, engaged community members relative to the global software population.
            - No post-stratification survey weighting is supplied with the public microdata.
            - All estimates represent observational sample associations.

            #### 2. The 182-Row Qualification Gap
            - **N_raw = 49,191** in downloadable public extract.
            - **N_official = 49,009** in official web report.
            - Net difference of 182 rows stems from internal screening filters (<3 min completion time)
              whose flags are omitted from public microdata.
            """
        )

    with col_gov2:
        st.markdown(
            """
            #### 3. Self-Reported Currency & Exchange Rates
            - Pre-converted annual USD compensation (`ConvertedCompYearly`) uses fixed exchange rates
              from June 25, 2025.
            - Values are self-reported and unverified against tax filings or payroll systems.
            - Figures do not adjust for local purchasing power parity (PPP), exaggerating cross-national real wage gaps.

            #### 4. Observational & Non-Causal Boundaries
            - Cross-sectional study fielded May 29 – June 23, 2025.
            - Regression coefficients indicate conditional correlations, not causal mechanisms or guaranteed returns.
            - Technologies with high premiums (e.g., Rust, Go) reflect specialization premiums and employer selectivity.
            """
        )

    st.markdown("---")

    # Section 5: Data & Artifacts Export
    st.subheader("5. Processed Dataset & Artifacts Export")
    col_exp1, col_exp2 = st.columns(2)

    with col_exp1:
        st.markdown("#### Cleaned Dataset Sample Export")
        st.caption("Download a representative CSV sample of the cleaned Stack Overflow 2025 dataset.")
        sample_export_df = full_df.head(1000)
        csv_bytes = get_csv_download_bytes(sample_export_df)
        st.download_button(
            label="📥 Download Cleaned Sample CSV (1,000 Rows)",
            data=csv_bytes,
            file_name="survey_results_cleaned_sample.csv",
            mime="text/csv",
        )

    with col_exp2:
        st.markdown("#### Phase 5 Statistical Metrics JSON")
        st.caption("Download the complete verified Phase 5 regression coefficients and test metrics.")
        if METRICS_JSON_PATH.exists():
            with open(METRICS_JSON_PATH, "r", encoding="utf-8") as f:
                metrics_str = f.read()
            st.download_button(
                label="📥 Download Analysis Summary Metrics JSON",
                data=metrics_str,
                file_name="analysis_summary_metrics.json",
                mime="application/json",
            )
        else:
            st.info("Metrics JSON file not available.")


if __name__ == "__main__":
    main()
