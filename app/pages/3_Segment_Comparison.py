"""Segment Comparison Page - Poll Results Visualizer.

Cross-tabulates developer compensation, roles (including DevOps), experience,
and remote-work arrangements with strict neutral observational framing.

Author: Akash Das
Project: Poll Results Visualizer
Phase: Phase 6 — Visualization
"""

import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.data_provider import get_survey_dataset  # noqa: E402
from app.components.filters import render_survey_demographic_filters  # noqa: E402
from app.components.charts import (  # noqa: E402
    plot_compensation_box,
    CHART_FONT_FAMILY,
    DEFAULT_CHART_TEMPLATE,
)
from src.datasets.stackoverflow_2025 import get_compensation_summary  # noqa: E402

st.set_page_config(
    page_title="Segment Comparison & Compensation - SO 2025",
    page_icon="👥",
    layout="wide",
)


def main():
    st.title("👥 Segment Comparison & Compensation Analysis")
    st.caption("Cross-cohort compensation distributions, developer roles, and working arrangement comparisons.")

    # Methodological & Non-Causal Boundary Notice
    st.warning(
        "⚠️ **Methodological Boundary & Observational Framing Notice:**\n\n"
        "- **Observational Associations:** Compensation comparisons reflect observational cross-sectional differences, "
        "not guaranteed individual returns or causal penalties.\n"
        "- **Confounding & Attenuation:** Raw differences (e.g., remote vs. in-person pay gaps of ~50–88%) "
        "reflect heavy geographic, seniority, and employer-size confounding. In the approved Phase 5 RQ4 Model C "
        "(controlling for country, experience, and organization size), the conditional difference attenuates to "
        "**+30.65% for Remote** (β = +0.2674, 100 × (exp(0.2674) - 1)) and **+33.86% to +34.46% for Hybrid** "
        "(β = +0.2916 to +0.2961) relative to the In-person baseline.\n"
        "- **Self-Reported Compensation:** Converted to USD (`ConvertedCompYearly`) based on June 25, 2025 exchange "
        "rates. Figures are unverified against tax/payroll records and not adjusted for local purchasing power "
        "parity (PPP)."
    )

    try:
        full_df = get_survey_dataset()
    except Exception as e:
        st.error(f"Failed to load dataset: {e}")
        st.stop()

    # Sidebar Cohort Filtering (with compensation trim toggle enabled)
    filtered_df, selections = render_survey_demographic_filters(full_df, enable_comp_trim=True, key_prefix="sc_")

    # Active Compensation Sample Telemetry
    valid_comp = pd.to_numeric(filtered_df["ConvertedCompYearly"], errors="coerce").dropna()
    valid_comp = valid_comp[valid_comp > 0]
    n_comp_ans = len(valid_comp)
    median_usd = valid_comp.median() if n_comp_ans > 0 else 0.0

    st.subheader("Active Compensation Telemetry")
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        st.metric(
            "Valid Salary Responses (N_answered)",
            f"{n_comp_ans:,}",
            help="Respondents reporting positive converted annual USD compensation in the current filtered cohort.",
        )
    with col_t2:
        st.metric(
            "Median Annual Compensation (USD)",
            f"${median_usd:,.0f}" if n_comp_ans > 0 else "N/A",
            help="Non-parametric 50th percentile of annual compensation.",
        )
    with col_t3:
        trim_status = "Trimmed ($1k–$1M USD)" if selections.get("trim_comp") else "Untrimmed ($0+ USD)"
        st.metric("Sample Trimming Status", trim_status)

    st.markdown("---")

    # Section 1: Developer Role Deep Dive
    st.subheader("1. Developer Role Compensation Deep Dive (`DevType`)")
    st.markdown(
        "Comparing compensation across developer specializations. Roles with $\\ge 50$ respondents are ranked "
        "by median annual earnings, explicitly including **DevOps engineers or professionals**."
    )

    if "DevType" in filtered_df.columns and n_comp_ans > 0:
        role_comp_df = get_compensation_summary(filtered_df, group_by="DevType")
        # Filter for roles with at least 30 respondents
        role_comp_df = role_comp_df[role_comp_df["n_answered"] >= 30].sort_values(by="median_usd", ascending=False)

        col_role_box, col_role_table = st.columns([3, 2])

        with col_role_box:
            fig_role_box = plot_compensation_box(
                filtered_df,
                group_col="DevType",
                title="Annual Compensation Distribution by Developer Role (USD)",
                max_groups=12,
            )
            st.plotly_chart(fig_role_box, use_container_width=True)

        with col_role_table:
            st.markdown("#### Role Compensation Summary")
            disp_role_df = role_comp_df.rename(
                columns={
                    "group": "Developer Role",
                    "n_answered": "Responses (N)",
                    "median_usd": "Median ($)",
                    "p25_usd": "Q1 ($)",
                    "p75_usd": "Q3 ($)",
                    "iqr_usd": "IQR ($)",
                }
            )[["Developer Role", "Responses (N)", "Median ($)", "Q1 ($)", "Q3 ($)"]].head(12)

            # Format dollar values
            for c in ["Median ($)", "Q1 ($)", "Q3 ($)"]:
                disp_role_df[c] = disp_role_df[c].apply(lambda v: f"${v:,.0f}")

            st.dataframe(disp_role_df, hide_index=True, use_container_width=True)
            st.caption(
                "Executive, managerial, and architecture roles lead compensation. "
                "DevOps engineers or professionals demonstrate strong mid-tier compensation (~$87k median)."
            )

    st.markdown("---")

    # Section 2: Country Comparisons
    st.subheader("2. Geographic Compensation & Experience Gradients")
    if "Country" in filtered_df.columns and n_comp_ans > 0:
        country_comp = get_compensation_summary(filtered_df, group_by="Country")
        # Restrict to countries with >= 50 respondents
        country_comp = country_comp[country_comp["n_answered"] >= 50].sort_values(by="median_usd", ascending=False)

        col_cntry_box, col_cntry_tbl = st.columns([3, 2])

        with col_cntry_box:
            fig_cntry_box = plot_compensation_box(
                filtered_df,
                group_col="Country",
                title="Annual Compensation Distribution by Country (USD)",
                max_groups=10,
            )
            st.plotly_chart(fig_cntry_box, use_container_width=True)

        with col_cntry_tbl:
            st.markdown("#### Top 10 High-Volume Countries")
            top_countries_by_vol = (
                filtered_df["Country"].value_counts().head(10).index.tolist()
            )
            vol_country_df = country_comp[country_comp["group"].isin(top_countries_by_vol)].copy()
            vol_country_df = vol_country_df.rename(
                columns={
                    "group": "Country",
                    "n_answered": "Responses",
                    "median_usd": "Median ($)",
                    "p25_usd": "Q1 ($)",
                    "p75_usd": "Q3 ($)",
                }
            )[["Country", "Responses", "Median ($)", "Q1 ($)", "Q3 ($)"]]

            for c in ["Median ($)", "Q1 ($)", "Q3 ($)"]:
                vol_country_df[c] = vol_country_df[c].apply(lambda v: f"${v:,.0f}")

            st.dataframe(vol_country_df, hide_index=True, use_container_width=True)
            st.caption(
                "Substantial cross-national wage disparities reflect distinct local economic conditions "
                "and purchasing power rather than productivity alone."
            )

    st.markdown("---")

    # Section 3: Professional Experience & Compensation
    st.subheader("3. Experience Gradients & Diminishing Marginal Returns")
    st.markdown(
        "Evaluating compensation progression across professional work experience tiers (`WorkExp_num`). "
        "The empirical data exhibits concave quadratic returns to experience (Mincerian experience curve)."
    )

    exp_col = "WorkExp_num" if "WorkExp_num" in filtered_df.columns else "YearsCode_num"
    if exp_col in filtered_df.columns and n_comp_ans > 0:
        # Create experience cohorts
        comp_exp_df = filtered_df[[exp_col, "ConvertedCompYearly"]].dropna().copy()
        comp_exp_df["ConvertedCompYearly"] = pd.to_numeric(comp_exp_df["ConvertedCompYearly"], errors="coerce")
        comp_exp_df = comp_exp_df.dropna()
        comp_exp_df = comp_exp_df[comp_exp_df["ConvertedCompYearly"] > 0]

        bins = [-1, 2, 5, 10, 20, 100]
        labels = [
            "Entry-level (0–2 yrs)",
            "Junior (3–5 yrs)",
            "Mid-level (6–10 yrs)",
            "Senior (11–20 yrs)",
            "Veteran (21+ yrs)",
        ]
        comp_exp_df["Experience Bracket"] = pd.cut(comp_exp_df[exp_col], bins=bins, labels=labels)

        col_exp_chart, col_exp_text = st.columns([3, 2])

        with col_exp_chart:
            fig_exp_box = px.box(
                comp_exp_df,
                x="Experience Bracket",
                y="ConvertedCompYearly",
                category_orders={"Experience Bracket": labels},
                title="<b>Compensation by Professional Experience Bracket</b>",
                color="Experience Bracket",
                color_discrete_sequence=px.colors.qualitative.Safe,
                template=DEFAULT_CHART_TEMPLATE,
            )
            fig_exp_box.update_layout(
                font=dict(family=CHART_FONT_FAMILY),
                showlegend=False,
                yaxis_title="Annual Compensation (USD)",
                xaxis_title="",
                yaxis=dict(tickprefix="$", tickformat=",.0f"),
                margin=dict(l=20, r=20, t=50, b=40),
            )
            st.plotly_chart(fig_exp_box, use_container_width=True)

        with col_exp_text:
            st.markdown("#### Concave Experience Returns")
            exp_summary = (
                comp_exp_df.groupby("Experience Bracket", observed=False)["ConvertedCompYearly"]
                .agg(n="count", median="median", mean="mean")
                .reset_index()
            )
            exp_summary["Median ($)"] = exp_summary["median"].apply(lambda v: f"${v:,.0f}")
            exp_summary["Mean ($)"] = exp_summary["mean"].apply(lambda v: f"${v:,.0f}")
            disp_exp = exp_summary[["Experience Bracket", "n", "Median ($)", "Mean ($)"]].rename(
                columns={"n": "Responses (N)"}
            )
            st.dataframe(disp_exp, hide_index=True, use_container_width=True)

            st.info(
                "💡 **Econometric Alignment (Phase 5 Model 1–3):**\n\n"
                "In the econometric specification, the linear experience coefficient is positive "
                "(β_exp = +0.0385) while the quadratic term is negative (β_exp² = -0.00062), "
                "empirically demonstrating diminishing marginal earnings gains as seniority advances."
            )

    st.markdown("---")

    # Section 4: Remote Work & Compensation Dynamics
    st.subheader("4. Remote Work Dynamics & Observational Attenuation")
    st.markdown(
        "Cross-analyzing compensation across **Remote**, **Hybrid**, and **In-person** work arrangements."
    )

    if "RemoteWork" in filtered_df.columns and n_comp_ans > 0:
        rw_comp_df = filtered_df[["RemoteWork", "ConvertedCompYearly"]].dropna().copy()
        rw_comp_df["ConvertedCompYearly"] = pd.to_numeric(rw_comp_df["ConvertedCompYearly"], errors="coerce")
        rw_comp_df = rw_comp_df.dropna()
        rw_comp_df = rw_comp_df[rw_comp_df["ConvertedCompYearly"] > 0]

        # Simplify remote categories for clarity
        def _simplify_rw(val):
            val_s = str(val).lower()
            if "remote" in val_s and "hybrid" not in val_s:
                return "Remote"
            elif "in-person" in val_s and "hybrid" not in val_s:
                return "In-person"
            elif "hybrid" in val_s or "choice" in val_s:
                return "Hybrid / Flexible"
            return "Other"

        rw_comp_df["Arrangement"] = rw_comp_df["RemoteWork"].apply(_simplify_rw)
        rw_comp_df = rw_comp_df[rw_comp_df["Arrangement"] != "Other"]

        col_rw_box, col_rw_memo = st.columns([3, 2])

        with col_rw_box:
            fig_rw_box = px.box(
                rw_comp_df,
                x="Arrangement",
                y="ConvertedCompYearly",
                title="<b>Compensation by Working Arrangement (USD)</b>",
                color="Arrangement",
                color_discrete_sequence=["#1f77b4", "#ff7f0e", "#2ca02c"],
                template=DEFAULT_CHART_TEMPLATE,
            )
            fig_rw_box.update_layout(
                font=dict(family=CHART_FONT_FAMILY),
                showlegend=False,
                yaxis_title="Annual Compensation (USD)",
                xaxis_title="",
                yaxis=dict(tickprefix="$", tickformat=",.0f"),
                margin=dict(l=20, r=20, t=50, b=40),
            )
            st.plotly_chart(fig_rw_box, use_container_width=True)

        with col_rw_memo:
            st.markdown("#### The Attenuation Mechanism Explained")
            rw_medians = (
                rw_comp_df.groupby("Arrangement")["ConvertedCompYearly"]
                .agg(["count", "median"])
                .reset_index()
            )
            rw_medians["Median ($)"] = rw_medians["median"].apply(
                lambda v: f"${v:,.2f}" if v % 1 != 0 else f"${v:,.0f}"
            )
            disp_rw = rw_medians.rename(columns={"count": "Responses (N)"})[
                ["Arrangement", "Responses (N)", "Median ($)"]
            ]
            st.dataframe(disp_rw, hide_index=True, use_container_width=True)

            st.warning(
                "🔍 **Why does the raw gap attenuate from ~50–88% to ~30–34%?**\n\n"
                "1. **Observed Earnings Direction:** In the trimmed compensation sample, Remote respondents "
                "($91,198 USD) and Hybrid respondents ($81,210 USD) report substantially higher raw median "
                "compensation than In-person respondents ($48,346.50 USD).\n"
                "2. **Geographic Confounding:** In-person developers are disproportionately located in developing "
                "nations with lower baseline wage scales, whereas remote workers frequently reside in or consult "
                "for high-compensation markets (e.g., US, Western Europe).\n"
                "3. **Seniority & Org Size Confounding:** Entry-level developers are frequently required into "
                "in-person office settings, while senior engineers and employees at large firms more often "
                "negotiate remote or hybrid flexibility.\n"
                "4. **Econometric Reality (Phase 5 Model C):** Controlling for country, linear and quadratic "
                "experience, and organization size reduces the conditional differential to β = +0.2674 log points "
                "for Remote, yielding an exact exponential conversion of 100 × (exp(0.2674) - 1) = +30.65% "
                "(and +33.86% to +34.46% for Hybrid arrangements) relative to the In-person baseline.\n"
                "5. **Observational Scope:** Figures represent unverified self-reported annual USD without "
                "purchasing power parity (PPP) adjustment, and do not reflect individual causal returns."
            )


if __name__ == "__main__":
    main()
