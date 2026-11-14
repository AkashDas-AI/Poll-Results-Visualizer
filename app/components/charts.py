"""Reusable Plotly Chart Components for Poll Results Visualizer.

Generates interactive figures for distribution, cross-tabulations, trends,
technology comparisons, compensation distributions, and data quality audits.
Supports dynamic Enterprise Light Mode and Dark Mode theme adaptation.

Author: Akash Das
Project: Poll Results Visualizer
Phase: Phase 6 — Visualization (Theme Enhancement)
"""

from typing import List, Optional
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.config import COL_OPTION, COL_SEGMENT
from app.components.theme import (
    apply_chart_theme,
    get_theme_config,
)

CHART_FONT_FAMILY = "Arial, sans-serif"
DEFAULT_CHART_TEMPLATE = "plotly_dark"
CHART_BG_TRANSPARENT = "rgba(0, 0, 0, 0)"
CHART_GRID_COLOR = "rgba(128, 128, 128, 0.15)"


def _empty_figure(
    message: str = "No data available matching active criteria",
    theme: Optional[str] = None,
) -> go.Figure:
    """Create a standardized empty Plotly figure with a clear notice message."""
    cfg = get_theme_config(theme)
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=14, color=cfg["text_secondary"], family=CHART_FONT_FAMILY),
    )
    fig.update_layout(
        template=cfg["plotly_template"],
        paper_bgcolor=CHART_BG_TRANSPARENT,
        plot_bgcolor=CHART_BG_TRANSPARENT,
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        margin=dict(l=20, r=20, t=50, b=30),
    )
    apply_chart_theme(fig, theme=theme)
    return fig


def plot_distribution_bar(
    dist_df: pd.DataFrame,
    title: str = "Response Distribution",
    theme: Optional[str] = None,
) -> go.Figure:
    """Generate a horizontal bar chart displaying option percentages.

    Args:
        dist_df: DataFrame with [option, response_count, percentage].
        title: Chart title.
        theme: Optional explicit theme override ('Dark' or 'Light').

    Returns:
        go.Figure: Configured Plotly figure.
    """
    cfg = get_theme_config(theme)
    if dist_df.empty or COL_OPTION not in dist_df.columns or "percentage" not in dist_df.columns:
        return _empty_figure("No response data available", theme=theme)

    sorted_df = dist_df.sort_values(by="percentage", ascending=True)

    fig = px.bar(
        sorted_df,
        x="percentage",
        y=COL_OPTION,
        orientation="h",
        text=sorted_df["percentage"].apply(lambda v: f"{v:.1f}%"),
        labels={"percentage": "Share of Responses (%)", COL_OPTION: "Option"},
        title=f"<b>{title}</b>",
        color="percentage",
        color_continuous_scale="Blues",
        template=cfg["plotly_template"],
    )
    fig.update_layout(
        showlegend=False,
        font=dict(family=CHART_FONT_FAMILY, color=cfg["text_primary"]),
        paper_bgcolor=CHART_BG_TRANSPARENT,
        plot_bgcolor=CHART_BG_TRANSPARENT,
        xaxis_title="Share of Responses (%)",
        yaxis_title="",
        margin=dict(l=20, r=20, t=50, b=30),
        xaxis=dict(
            range=[0, max(sorted_df["percentage"].max() * 1.15, 10)],
            gridcolor=cfg["chart_grid"],
        ),
        yaxis=dict(gridcolor=cfg["chart_grid"]),
    )
    apply_chart_theme(fig, theme=theme)
    return fig


def plot_distribution_pie(
    dist_df: pd.DataFrame,
    title: str = "Share Breakdown",
    theme: Optional[str] = None,
) -> go.Figure:
    """Generate a donut chart for option share breakdown.

    Args:
        dist_df: DataFrame with [option, response_count, percentage].
        title: Chart title.
        theme: Optional explicit theme override ('Dark' or 'Light').

    Returns:
        go.Figure: Plotly figure.
    """
    cfg = get_theme_config(theme)
    if dist_df.empty or COL_OPTION not in dist_df.columns or "response_count" not in dist_df.columns:
        return _empty_figure("No breakdown data available", theme=theme)

    fig = px.pie(
        dist_df,
        names=COL_OPTION,
        values="response_count",
        hole=0.45,
        title=f"<b>{title}</b>",
        color_discrete_sequence=px.colors.qualitative.Safe,
        template=cfg["plotly_template"],
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(
        font=dict(family=CHART_FONT_FAMILY, color=cfg["text_primary"]),
        paper_bgcolor=CHART_BG_TRANSPARENT,
        plot_bgcolor=CHART_BG_TRANSPARENT,
        margin=dict(l=20, r=20, t=50, b=30),
    )
    apply_chart_theme(fig, theme=theme)
    return fig


def plot_segment_breakdown_bar(
    segment_df: pd.DataFrame,
    title: str = "Segment Breakdown",
    theme: Optional[str] = None,
) -> go.Figure:
    """Generate a grouped bar chart comparing option percentages across demographic segments.

    Args:
        segment_df: DataFrame with [segment, option, percentage, response_count].
        title: Chart title.
        theme: Optional explicit theme override ('Dark' or 'Light').

    Returns:
        go.Figure: Plotly figure.
    """
    cfg = get_theme_config(theme)
    if segment_df.empty or COL_SEGMENT not in segment_df.columns:
        return _empty_figure("No segment comparison data available", theme=theme)

    fig = px.bar(
        segment_df,
        x=COL_SEGMENT,
        y="percentage",
        color=COL_OPTION,
        barmode="group",
        text=segment_df["percentage"].apply(lambda v: f"{v:.1f}%"),
        labels={"percentage": "Within-Segment Share (%)", COL_SEGMENT: "Demographic Segment"},
        title=f"<b>{title}</b>",
        color_discrete_sequence=px.colors.qualitative.Plotly,
        template=cfg["plotly_template"],
    )
    fig.update_layout(
        font=dict(family=CHART_FONT_FAMILY, color=cfg["text_primary"]),
        paper_bgcolor=CHART_BG_TRANSPARENT,
        plot_bgcolor=CHART_BG_TRANSPARENT,
        xaxis_title="Demographic Segment",
        yaxis_title="Share within Cohort (%)",
        margin=dict(l=20, r=20, t=50, b=30),
        legend_title="Selected Option",
        xaxis=dict(gridcolor=cfg["chart_grid"]),
        yaxis=dict(gridcolor=cfg["chart_grid"]),
    )
    apply_chart_theme(fig, theme=theme)
    return fig


def plot_trend_line(
    trend_df: pd.DataFrame,
    title: str = "Response Volume Over Time",
    theme: Optional[str] = None,
) -> go.Figure:
    """Generate a line chart tracking response volume across dates.

    Args:
        trend_df: DataFrame with [date, response_count].
        title: Chart title.
        theme: Optional explicit theme override ('Dark' or 'Light').

    Returns:
        go.Figure: Plotly figure.
    """
    cfg = get_theme_config(theme)
    if trend_df.empty or "date" not in trend_df.columns or "response_count" not in trend_df.columns:
        return _empty_figure("No trend data available", theme=theme)

    fig = px.line(
        trend_df,
        x="date",
        y="response_count",
        markers=True,
        title=f"<b>{title}</b>",
        labels={"date": "Survey Date", "response_count": "Responses Logged"},
        template=cfg["plotly_template"],
    )
    fig.update_layout(
        font=dict(family=CHART_FONT_FAMILY, color=cfg["text_primary"]),
        paper_bgcolor=CHART_BG_TRANSPARENT,
        plot_bgcolor=CHART_BG_TRANSPARENT,
        xaxis_title="Date",
        yaxis_title="Response Count",
        margin=dict(l=20, r=20, t=50, b=30),
        xaxis=dict(gridcolor=cfg["chart_grid"]),
        yaxis=dict(gridcolor=cfg["chart_grid"]),
    )
    apply_chart_theme(fig, theme=theme)
    return fig


def plot_horizontal_bar_with_denominators(
    df: pd.DataFrame,
    category_col: str,
    count_col: str,
    n_answered: int,
    n_total: int = 49191,
    title: str = "Response Distribution",
    top_n: Optional[int] = None,
    color_scale: str = "Blues",
    height: Optional[int] = None,
    theme: Optional[str] = None,
) -> go.Figure:
    """Generate a horizontal bar chart displaying dual percentages and counts in hover.

    Reports:
    - Percentage of valid answered respondents (n / n_answered * 100).
    - Percentage of total survey respondents (n / n_total * 100).

    Args:
        df: Input DataFrame containing category and count columns.
        category_col: Column containing category labels.
        count_col: Column containing raw counts.
        n_answered: Denominator for answered responses.
        n_total: Total survey respondent count (default: 49,191).
        title: Chart title.
        top_n: Optional limit to top N categories.
        color_scale: Plotly continuous color scale.
        height: Optional fixed figure height in pixels.
        theme: Optional explicit theme override ('Dark' or 'Light').

    Returns:
        go.Figure: Formatted Plotly figure.
    """
    cfg = get_theme_config(theme)
    if df.empty or category_col not in df.columns or count_col not in df.columns:
        return _empty_figure("No data available for distribution", theme=theme)

    plot_df = df.copy()
    plot_df[count_col] = pd.to_numeric(plot_df[count_col], errors="coerce").fillna(0)
    plot_df = plot_df.sort_values(by=count_col, ascending=False)

    if top_n is not None and top_n > 0:
        plot_df = plot_df.head(top_n)

    # Sort ascending for horizontal bar display (highest at top)
    plot_df = plot_df.sort_values(by=count_col, ascending=True)

    pct_answered = (plot_df[count_col] / max(n_answered, 1)) * 100.0
    pct_total = (plot_df[count_col] / max(n_total, 1)) * 100.0
    plot_df["pct_answered"] = pct_answered
    plot_df["pct_total"] = pct_total

    # Text label on bar
    bar_texts = [f"{pct:.1f}% ({int(cnt):,})" for pct, cnt in zip(pct_answered, plot_df[count_col])]

    # Customdata array for hovertemplate: [count, n_answered, pct_total, n_total]
    customdata = np.stack(
        (
            plot_df[count_col].values,
            np.full(len(plot_df), n_answered),
            plot_df["pct_total"].values,
            np.full(len(plot_df), n_total),
        ),
        axis=-1,
    )

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=plot_df[category_col],
            x=plot_df["pct_answered"],
            orientation="h",
            text=bar_texts,
            textposition="auto",
            marker=dict(
                color=plot_df["pct_answered"],
                colorscale=color_scale,
                line=dict(color="rgba(0,0,0,0.15)", width=1),
            ),
            customdata=customdata,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Respondents: %{customdata[0]:,}<br>"
                "Share of Answered: %{x:.1f}% (N = %{customdata[1]:,})<br>"
                "Share of Total Survey: %{customdata[2]:.1f}% (N = %{customdata[3]:,})"
                "<extra></extra>"
            ),
        )
    )

    max_pct = plot_df["pct_answered"].max() if not plot_df.empty else 10
    fig.update_layout(
        title=f"<b>{title}</b>",
        template=cfg["plotly_template"],
        font=dict(family=CHART_FONT_FAMILY, color=cfg["text_primary"]),
        paper_bgcolor=CHART_BG_TRANSPARENT,
        plot_bgcolor=CHART_BG_TRANSPARENT,
        xaxis_title="Share of Answered Respondents (%)",
        yaxis_title="",
        xaxis=dict(
            range=[0, max(max_pct * 1.18, 5)],
            gridcolor=cfg["chart_grid"],
        ),
        yaxis=dict(gridcolor=cfg["chart_grid"]),
        margin=dict(l=20, r=20, t=50, b=30),
        height=height or max(350, len(plot_df) * 28),
    )
    apply_chart_theme(fig, theme=theme)
    return fig


def plot_technology_comparison_bar(
    comparison_df: pd.DataFrame,
    tech_col: str = "technology",
    current_col: str = "current_pct",
    desired_col: str = "desired_pct",
    title: str = "Current vs. Desired Technology Adoption",
    top_n: int = 15,
    theme: Optional[str] = None,
) -> go.Figure:
    """Generate a paired grouped horizontal bar chart comparing current vs. desired usage.

    Args:
        comparison_df: DataFrame with [technology, current_pct, desired_pct, ...].
        tech_col: Column with technology names.
        current_col: Column with % currently using.
        desired_col: Column with % desiring to work with.
        title: Chart title.
        top_n: Limit to top N technologies by current adoption.
        theme: Optional explicit theme override ('Dark' or 'Light').

    Returns:
        go.Figure: Configured paired bar chart.
    """
    cfg = get_theme_config(theme)
    if comparison_df.empty or tech_col not in comparison_df.columns:
        return _empty_figure("No technology comparison data available", theme=theme)

    plot_df = comparison_df.head(top_n).copy()
    plot_df = plot_df.sort_values(by=current_col, ascending=True)

    fig = go.Figure()

    # Current Worked With - Primary Accent
    fig.add_trace(
        go.Bar(
            y=plot_df[tech_col],
            x=plot_df[current_col],
            name="Currently Worked With",
            orientation="h",
            marker=dict(color=cfg["accent_primary"]),
            text=plot_df[current_col].apply(lambda v: f"{v:.1f}%"),
            textposition="auto",
            hovertemplate="<b>%{y}</b><br>Currently Used: %{x:.1f}%<extra></extra>",
        )
    )

    # Desired - Positive Indicator
    fig.add_trace(
        go.Bar(
            y=plot_df[tech_col],
            x=plot_df[desired_col],
            name="Want to Work With",
            orientation="h",
            marker=dict(color=cfg["indicator_positive"]),
            text=plot_df[desired_col].apply(lambda v: f"{v:.1f}%"),
            textposition="auto",
            hovertemplate="<b>%{y}</b><br>Want to Work With: %{x:.1f}%<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"<b>{title}</b>",
        barmode="group",
        template=cfg["plotly_template"],
        font=dict(family=CHART_FONT_FAMILY, color=cfg["text_primary"]),
        paper_bgcolor=CHART_BG_TRANSPARENT,
        plot_bgcolor=CHART_BG_TRANSPARENT,
        xaxis_title="Proportion of Respondents (%)",
        yaxis_title="",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(gridcolor=cfg["chart_grid"]),
        yaxis=dict(gridcolor=cfg["chart_grid"]),
        margin=dict(l=20, r=20, t=60, b=30),
        height=max(400, len(plot_df) * 35),
    )
    apply_chart_theme(fig, theme=theme)
    return fig


def plot_compensation_box(
    df: pd.DataFrame,
    group_col: str,
    comp_col: str = "ConvertedCompYearly",
    title: str = "Annual Converted Compensation Distribution (USD)",
    max_groups: int = 12,
    show_points: bool = False,
    theme: Optional[str] = None,
) -> go.Figure:
    """Generate an interactive box plot comparing annual compensation across cohorts.

    Args:
        df: Input DataFrame containing grouping and compensation columns.
        group_col: Categorical cohort column (e.g., 'DevType', 'RemoteWork', 'Country').
        comp_col: Converted annual compensation column in USD.
        title: Chart title.
        max_groups: Maximum number of cohorts to display (ranked by respondent volume).
        show_points: Whether to render raw outlier scatter points.
        theme: Optional explicit theme override ('Dark' or 'Light').

    Returns:
        go.Figure: Configured box plot.
    """
    cfg = get_theme_config(theme)
    if df.empty or group_col not in df.columns or comp_col not in df.columns:
        return _empty_figure("No compensation data available for comparison", theme=theme)

    valid_df = df[[group_col, comp_col]].dropna().copy()
    valid_df[comp_col] = pd.to_numeric(valid_df[comp_col], errors="coerce")
    valid_df = valid_df.dropna(subset=[comp_col])
    valid_df = valid_df[valid_df[comp_col] > 0]

    if valid_df.empty:
        return _empty_figure("No positive compensation records found", theme=theme)

    # Select top cohorts by volume
    top_cohorts = valid_df[group_col].value_counts().head(max_groups).index.tolist()
    plot_df = valid_df[valid_df[group_col].isin(top_cohorts)].copy()

    # Calculate medians for ordering
    medians = plot_df.groupby(group_col, observed=False)[comp_col].median()
    ordered_groups = medians.sort_values(ascending=False).index.tolist()

    fig = go.Figure()
    palette = px.colors.qualitative.Safe

    for i, grp in enumerate(ordered_groups):
        grp_data = plot_df[plot_df[group_col] == grp][comp_col]
        fig.add_trace(
            go.Box(
                y=grp_data,
                name=str(grp),
                boxpoints="outliers" if show_points else False,
                marker=dict(color=palette[i % len(palette)]),
                line=dict(width=1.5),
            )
        )

    fig.update_layout(
        title=f"<b>{title}</b>",
        template=cfg["plotly_template"],
        font=dict(family=CHART_FONT_FAMILY, color=cfg["text_primary"]),
        paper_bgcolor=CHART_BG_TRANSPARENT,
        plot_bgcolor=CHART_BG_TRANSPARENT,
        yaxis_title="Annual Compensation (USD)",
        xaxis_title="",
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=40),
        yaxis=dict(
            tickprefix="$",
            tickformat=",.0f",
            gridcolor=cfg["chart_grid"],
        ),
        xaxis=dict(gridcolor=cfg["chart_grid"]),
    )
    apply_chart_theme(fig, theme=theme)
    return fig


def plot_missingness_ranking_bar(
    missing_df: pd.DataFrame,
    title: str = "Top 20 Survey Questions by Non-Response / Missingness Rate",
    top_n: int = 20,
    theme: Optional[str] = None,
) -> go.Figure:
    """Generate a horizontal bar chart displaying ranked non-response rates.

    Args:
        missing_df: DataFrame with [column, missing_count, missing_pct, non_null_count].
        title: Chart title.
        top_n: Number of questions to present.
        theme: Optional explicit theme override ('Dark' or 'Light').

    Returns:
        go.Figure: Ranked missingness bar chart.
    """
    cfg = get_theme_config(theme)
    if missing_df.empty or "column" not in missing_df.columns or "missing_pct" not in missing_df.columns:
        return _empty_figure("No missingness data available", theme=theme)

    plot_df = missing_df.head(top_n).sort_values(by="missing_pct", ascending=True)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=plot_df["column"],
            x=plot_df["missing_pct"],
            orientation="h",
            text=plot_df["missing_pct"].apply(lambda v: f"{v:.1f}%"),
            textposition="auto",
            marker=dict(
                color=plot_df["missing_pct"],
                colorscale="Reds",
                line=dict(color="rgba(255,255,255,0.15)", width=1),
            ),
            customdata=plot_df[["missing_count", "non_null_count"]].values,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Missing Rate: %{x:.1f}%<br>"
                "Missing Count: %{customdata[0]:,}<br>"
                "Valid Answered: %{customdata[1]:,}"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title=f"<b>{title}</b>",
        template=cfg["plotly_template"],
        font=dict(family=CHART_FONT_FAMILY, color=cfg["text_primary"]),
        paper_bgcolor=CHART_BG_TRANSPARENT,
        plot_bgcolor=CHART_BG_TRANSPARENT,
        xaxis_title="Non-Response / Missingness Rate (%)",
        yaxis_title="",
        xaxis=dict(
            range=[0, 105],
            gridcolor=cfg["chart_grid"],
        ),
        yaxis=dict(gridcolor=cfg["chart_grid"]),
        margin=dict(l=20, r=20, t=50, b=30),
        height=max(400, len(plot_df) * 26),
    )
    apply_chart_theme(fig, theme=theme)
    return fig


def plot_sample_flow_funnel(
    stage_names: List[str],
    stage_counts: List[int],
    title: str = "Sample Qualification & Complete-Case Filtering Flow",
    theme: Optional[str] = None,
) -> go.Figure:
    """Generate a funnel chart visualizing sample flow drops across analytical stages.

    Args:
        stage_names: List of stage description labels.
        stage_counts: List of respondent counts at each stage.
        title: Chart title.
        theme: Optional explicit theme override ('Dark' or 'Light').

    Returns:
        go.Figure: Funnel figure.
    """
    cfg = get_theme_config(theme)
    if not stage_names or not stage_counts or len(stage_names) != len(stage_counts):
        return _empty_figure("No sample flow data available", theme=theme)

    fig = go.Figure(
        go.Funnel(
            y=stage_names,
            x=stage_counts,
            textinfo="value+percent initial",
            marker=dict(
                color=["#1E3A8A", "#2563EB", "#3B82F6", "#60A5FA"][: len(stage_names)],
                line=dict(width=1, color="rgba(255,255,255,0.2)"),
            ),
            connector=dict(line=dict(color="#64748B", width=1, dash="dot")),
        )
    )

    fig.update_layout(
        title=f"<b>{title}</b>",
        template=cfg["plotly_template"],
        font=dict(family=CHART_FONT_FAMILY, color=cfg["text_primary"]),
        paper_bgcolor=CHART_BG_TRANSPARENT,
        plot_bgcolor=CHART_BG_TRANSPARENT,
        margin=dict(l=20, r=20, t=50, b=30),
        height=360,
    )
    apply_chart_theme(fig, theme=theme)
    return fig
