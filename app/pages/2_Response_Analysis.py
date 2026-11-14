"""Technology Analysis Page - Poll Results Visualizer.

Explores programming languages, current vs. desired technology migration,
database and platform adoption, and the 6-tier AI tool/agent hierarchy.

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

from app.data_provider import get_survey_dataset  # noqa: E402
from app.components.filters import render_survey_demographic_filters  # noqa: E402
from app.components.theme import apply_custom_theme  # noqa: E402
from app.components.charts import (  # noqa: E402
    plot_horizontal_bar_with_denominators,
    plot_technology_comparison_bar,
    render_plotly_chart,
)
from src.datasets.stackoverflow_2025 import (  # noqa: E402
    analyze_single_select,
    analyze_multi_select,
)

st.set_page_config(
    page_title="Technology & AI Adoption - SO 2025",
    page_icon="💻",
    layout="wide",
)


def main():
    apply_custom_theme()
    st.title("💻 Technology & AI Adoption Deep Dive")
    st.caption("Granular multi-select technology breakdowns, migration patterns, and autonomous agent adoption.")

    # Observational boundary notice
    st.info(
        "ℹ️ **Multi-Select & AI Telemetry Note:** Multi-select technology columns are semicolon-delimited. "
        "Percentages are reported as **% of answered respondents** (shares may sum to >100% due to multiple "
        "selections). Tooltips display exact counts alongside % of total survey pool (N_raw = 49,191)."
    )

    try:
        full_df = get_survey_dataset()
    except Exception as e:
        st.error(f"Failed to load dataset: {e}")
        st.stop()

    # Sidebar Cohort Filtering
    filtered_df, selections = render_survey_demographic_filters(full_df, enable_comp_trim=False, key_prefix="ta_")
    n_total = len(full_df)

    # Section 1: Programming Languages
    st.subheader("1. Programming Languages Landscape")
    if "LanguageHaveWorkedWith" in filtered_df.columns:
        lang_valid = filtered_df["LanguageHaveWorkedWith"].dropna()
        n_lang_ans = len(lang_valid)

        if n_lang_ans > 0:
            lang_dist = analyze_multi_select(filtered_df, "LanguageHaveWorkedWith", top_n=20)
            fig_lang = plot_horizontal_bar_with_denominators(
                lang_dist,
                category_col="option",
                count_col="response_count",
                n_answered=n_lang_ans,
                n_total=n_total,
                title="Top 20 Programming Languages Currently Worked With",
                top_n=20,
                color_scale="Blues",
                height=520,
            )
            render_plotly_chart(fig_lang)
            st.caption(
                f"Question Answered: N_answered = {n_lang_ans:,} respondents "
                f"({n_lang_ans / n_total * 100.0:.1f}% of survey pool). "
                "Adoption shares among answered respondents: JavaScript (66.32%), HTML/CSS (62.20%), "
                "SQL (58.83%), Python (58.13%), and TypeScript (43.76%)."
            )
        else:
            st.info("No programming language data available for current filter.")

    st.markdown("---")

    # Section 2: Current vs. Desired Migration
    st.subheader("2. Current vs. Desired Technology Migration")
    st.markdown(
        "Comparing languages developers **currently use** (`LanguageHaveWorkedWith`) versus "
        "languages they **want to work with** next year (`LanguageWantToWorkWith`). "
        "Evaluated on the paired respondent cohort to ensure symmetric denominators."
    )

    if "LanguageHaveWorkedWith" in filtered_df.columns and "LanguageWantToWorkWith" in filtered_df.columns:
        paired_df = filtered_df.dropna(subset=["LanguageHaveWorkedWith", "LanguageWantToWorkWith"])
        n_paired = len(paired_df)

        if n_paired > 0:
            curr_df = analyze_multi_select(paired_df, "LanguageHaveWorkedWith", top_n=30)
            des_df = analyze_multi_select(paired_df, "LanguageWantToWorkWith", top_n=30)

            if not curr_df.empty and not des_df.empty:
                merged_lang = pd.merge(
                    curr_df[["option", "response_count", "pct_of_respondents"]],
                    des_df[["option", "response_count", "pct_of_respondents"]],
                    on="option",
                    suffixes=("_current", "_desired"),
                )
                merged_lang["net_desire_ratio"] = (
                    merged_lang["response_count_desired"] / merged_lang["response_count_current"].replace(0, 1)
                ).round(2)
                merged_lang["delta_pct"] = (
                    merged_lang["pct_of_respondents_desired"] - merged_lang["pct_of_respondents_current"]
                ).round(2)

                col_comp_chart, col_comp_table = st.columns([3, 2])

                with col_comp_chart:
                    fig_comp = plot_technology_comparison_bar(
                        merged_lang,
                        tech_col="option",
                        current_col="pct_of_respondents_current",
                        desired_col="pct_of_respondents_desired",
                        title=f"Top 15 Languages: Current vs. Desired Adoption (N_paired = {n_paired:,})",
                        top_n=15,
                    )
                    render_plotly_chart(fig_comp)

                with col_comp_table:
                    st.markdown("#### Migration & Desire Momentum")
                    st.caption(
                        f"Paired sample (N_paired = {n_paired:,}). "
                        "Ratio > 1.0 indicates expanding forward demand; < 1.0 indicates contracting interest."
                    )
                    disp_table = merged_lang.rename(
                        columns={
                            "option": "Language",
                            "pct_of_respondents_current": "Current %",
                            "pct_of_respondents_desired": "Desired %",
                            "delta_pct": "Net Gap (pp)",
                            "net_desire_ratio": "Desire Ratio",
                        }
                    )[["Language", "Current %", "Desired %", "Net Gap (pp)", "Desire Ratio"]].head(12)

                    st.dataframe(disp_table, hide_index=True, use_container_width=True)
                    st.caption(
                        "Positive stated preference gaps observed in modern systems and typed languages "
                        "(e.g., Rust +18.45 pp, Go +10.56 pp), contrasting with negative preference gaps in "
                        "JavaScript (-27.02 pp) and Python (-12.74 pp) among paired respondents."
                    )
        else:
            st.info("No paired language responses available for current filter.")

    st.markdown("---")

    # Section 3: Databases & Cloud Platforms
    st.subheader("3. Databases & Cloud Infrastructure Platforms")
    col_db, col_plat = st.columns(2)

    with col_db:
        st.markdown("#### Top 15 Databases (`DatabaseHaveWorkedWith`)")
        if "DatabaseHaveWorkedWith" in filtered_df.columns:
            db_valid = filtered_df["DatabaseHaveWorkedWith"].dropna()
            n_db_ans = len(db_valid)
            if n_db_ans > 0:
                db_dist = analyze_multi_select(filtered_df, "DatabaseHaveWorkedWith", top_n=15)
                fig_db = plot_horizontal_bar_with_denominators(
                    db_dist,
                    category_col="option",
                    count_col="response_count",
                    n_answered=n_db_ans,
                    n_total=n_total,
                    title="Database Adoption (% of Answered)",
                    top_n=15,
                    color_scale="Blues",
                    height=450,
                )
                render_plotly_chart(fig_db)
                st.caption(
                    f"Question Answered: N_answered = {n_db_ans:,} respondents. "
                    "Dominant database engines: PostgreSQL (56.86%), MySQL (41.41%), and SQLite (38.35%)."
                )

    with col_plat:
        st.markdown("#### Top 10 Cloud Platforms (`PlatformHaveWorkedWith`)")
        if "PlatformHaveWorkedWith" in filtered_df.columns:
            plat_valid = filtered_df["PlatformHaveWorkedWith"].dropna()
            n_plat_ans = len(plat_valid)
            if n_plat_ans > 0:
                plat_dist = analyze_multi_select(filtered_df, "PlatformHaveWorkedWith", top_n=10)
                fig_plat = plot_horizontal_bar_with_denominators(
                    plat_dist,
                    category_col="option",
                    count_col="response_count",
                    n_answered=n_plat_ans,
                    n_total=n_total,
                    title="Cloud & Platform Adoption (% of Answered)",
                    top_n=10,
                    color_scale="Teal",
                    height=450,
                )
                render_plotly_chart(fig_plat)
                st.caption(
                    f"Question Answered: N_answered = {n_plat_ans:,} respondents. "
                    "Leading infrastructure platforms: Docker (71.79%), AWS (43.77%), "
                    "Microsoft Azure (26.58%), and Google Cloud (24.80%)."
                )

    st.markdown("---")

    # Section 4: AI Tools & Autonomous Agents
    st.subheader("4. AI Tool Adoption & Autonomous Agent Hierarchy")
    st.markdown(
        "Evaluating developer stance across **tool usage** (`AISelect`), **sentiment** (`AISent`), "
        "**trust in accuracy** (`AIAcc`), and the emerging **autonomous agents hierarchy** (`AIAgents`)."
    )

    ai_tab1, ai_tab2, ai_tab3, ai_tab4 = st.tabs([
        "🤖 AI Tool Usage (AISelect)",
        "🎯 Trust in Accuracy (AIAcc)",
        "💭 Developer Sentiment (AISent)",
        "⚡ Autonomous Agents (AIAgents)",
    ])

    with ai_tab1:
        if "AISelect" in filtered_df.columns:
            ai_sel_df = analyze_single_select(filtered_df, "AISelect")
            n_ai_ans = len(filtered_df["AISelect"].dropna())
            if not ai_sel_df.empty:
                fig_ai_sel = plot_horizontal_bar_with_denominators(
                    ai_sel_df,
                    category_col="category",
                    count_col="response_count",
                    n_answered=n_ai_ans,
                    n_total=n_total,
                    title="AI Tool Usage Frequency (AISelect)",
                    color_scale="Blues",
                )
                render_plotly_chart(fig_ai_sel)
                st.caption(
                    f"N_answered = {n_ai_ans:,} | "
                    f"Daily and weekly users account for the majority of respondents adopting AI tools."
                )

    with ai_tab2:
        if "AIAcc" in filtered_df.columns:
            acc_df = analyze_single_select(filtered_df, "AIAcc")
            n_acc_ans = len(filtered_df["AIAcc"].dropna())
            if not acc_df.empty:
                fig_acc = plot_horizontal_bar_with_denominators(
                    acc_df,
                    category_col="category",
                    count_col="response_count",
                    n_answered=n_acc_ans,
                    n_total=n_total,
                    title="Perceived Accuracy of AI Tools (AIAcc)",
                    color_scale="Teal",
                )
                render_plotly_chart(fig_acc)
                st.caption(
                    f"N_answered = {n_acc_ans:,} | "
                    "Note: Only ~3% 'Highly trust' AI output, while 'Distrust' (Somewhat + Highly) exceeds 45%."
                )

    with ai_tab3:
        if "AISent" in filtered_df.columns:
            sent_df = analyze_single_select(filtered_df, "AISent")
            n_sent_ans = len(filtered_df["AISent"].dropna())
            if not sent_df.empty:
                fig_sent = plot_horizontal_bar_with_denominators(
                    sent_df,
                    category_col="category",
                    count_col="response_count",
                    n_answered=n_sent_ans,
                    n_total=n_total,
                    title="General Sentiment Towards AI Tools (AISent)",
                    color_scale="Blues",
                )
                render_plotly_chart(fig_sent)
                st.caption(f"N_answered = {n_sent_ans:,} | Majority of developers view AI tooling favorably.")

    with ai_tab4:
        if "AIAgents" in filtered_df.columns:
            agents_df = analyze_single_select(filtered_df, "AIAgents")
            n_agents_ans = len(filtered_df["AIAgents"].dropna())
            if not agents_df.empty:
                fig_agents = plot_horizontal_bar_with_denominators(
                    agents_df,
                    category_col="category",
                    count_col="response_count",
                    n_answered=n_agents_ans,
                    n_total=n_total,
                    title="Autonomous AI Agent Adoption Hierarchy (AIAgents)",
                    color_scale="Teal",
                )
                render_plotly_chart(fig_agents)
                st.caption(
                    f"N_answered = {n_agents_ans:,} | "
                    "The 6-tier hierarchy illustrates that while copilot/autocomplete mode is widespread, "
                    "autonomous multi-step agents in production remain in early exploratory phases (~9.2% daily)."
                )


if __name__ == "__main__":
    main()
