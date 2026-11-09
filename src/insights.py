"""Insights module for Poll Results Visualizer.

Generates automated, descriptive summary narratives from analytical outputs.
Maintains objective, observational language; does not assert causal claims.
Author: Akash Das
"""

from typing import List
import pandas as pd

from src.config import COL_OPTION, COL_SEGMENT


def generate_question_insights(dist_df: pd.DataFrame, question_name: str) -> List[str]:
    """Generate descriptive text observations for a single question's distribution.

    Args:
        dist_df: DataFrame returned by `get_response_distribution`.
        question_name: The question title.

    Returns:
        List[str]: List of bulleted analytical insights.
    """
    if dist_df.empty:
        return ["No response data available to generate insights for this question."]

    insights = []
    total_answers = dist_df["response_count"].sum()
    top_row = dist_df.iloc[0]
    top_option = top_row[COL_OPTION]
    top_pct = top_row["percentage"]
    top_count = top_row["response_count"]

    insights.append(
        f"**Leading Choice**: '{top_option}' is the most selected option with "
        f"{top_count} responses ({top_pct}% of total {total_answers} responses)."
    )

    if len(dist_df) > 1:
        second_row = dist_df.iloc[1]
        second_option = second_row[COL_OPTION]
        second_pct = second_row["percentage"]
        margin = round(top_pct - second_pct, 2)
        insights.append(
            f"**Plurality Margin**: '{top_option}' leads over the second choice '{second_option}' "
            f"({second_pct}%) by a descriptive margin of {margin} percentage points."
        )

    # Consensus assessment
    if top_pct > 50.0:
        insights.append(
            f"**Majority Consensus**: A majority ({top_pct}%) of respondents favored '{top_option}'."
        )
    elif top_pct < 35.0:
        insights.append(
            "**Fragmented Distribution**: No single option captured more than 35% of responses, "
            "indicating a distributed or split opinion among respondents."
        )

    insights.append(
        "_Note: These observations describe the sample responses gathered and do not establish causal relationships._"
    )

    return insights


def generate_segment_insights(segment_df: pd.DataFrame) -> List[str]:
    """Generate comparative descriptive insights across demographic segments.

    Args:
        segment_df: DataFrame returned by `get_segment_comparison`.

    Returns:
        List[str]: Observational comparison notes.
    """
    if segment_df.empty:
        return ["No segment comparison data available."]

    insights = []
    # Identify top option per segment
    top_per_segment = (
        segment_df.sort_values(by=[COL_SEGMENT, "percentage"], ascending=[True, False])
        .groupby(COL_SEGMENT, observed=False)
        .first()
        .reset_index()
    )

    for _, row in top_per_segment.iterrows():
        seg_name = row[COL_SEGMENT]
        opt_name = row[COL_OPTION]
        pct = row["percentage"]
        rc = row["response_count"]
        stot = row["segment_total"]
        insights.append(
            f"In segment **{seg_name}**, the most frequent option was **'{opt_name}'** "
            f"accounting for {pct}% of responses within that cohort ({rc}/{stot})."
        )

    # Check for divergence across segments
    distinct_top_choices = top_per_segment[COL_OPTION].nunique()
    if distinct_top_choices > 1:
        insights.append(
            f"**Segment Divergence**: Top preferences differ across demographic cohorts "
            f"({distinct_top_choices} distinct leading options across groups)."
        )
    else:
        insights.append(
            "**Consistent Alignment**: All analyzed segments share the same leading option."
        )

    insights.append(
        "_Note: Segment comparisons reflect observed sample distributions and do not imply demographic causation._"
    )

    return insights
