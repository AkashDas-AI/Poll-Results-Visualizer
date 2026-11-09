"""Unit tests for insights module.

Author: Akash Das
"""

import pandas as pd
from src.insights import generate_question_insights, generate_segment_insights


def test_generate_question_insights_content():
    """Verify generated question insights identify leader and avoid causal assertions."""
    dist_df = pd.DataFrame({
        "option": ["Option A", "Option B"],
        "response_count": [60, 40],
        "percentage": [60.0, 40.0],
    })
    insights = generate_question_insights(dist_df, "Sample Question")
    assert len(insights) >= 3
    # Check leading option noted
    assert any("Option A" in text for text in insights)
    # Check margin mentioned
    assert any("20.0" in text for text in insights)
    # Check non-causal disclaimer
    assert any("do not establish causal" in text for text in insights)


def test_generate_question_insights_empty():
    """Verify empty input handling."""
    empty_df = pd.DataFrame(columns=["option", "response_count", "percentage"])
    insights = generate_question_insights(empty_df, "Empty Question")
    assert len(insights) == 1
    assert "No response data" in insights[0]


def test_generate_segment_insights():
    """Verify segment insights identify differences and include disclaimer."""
    seg_df = pd.DataFrame({
        "segment": ["Cohort 1", "Cohort 2"],
        "option": ["Option A", "Option B"],
        "response_count": [10, 15],
        "segment_total": [10, 15],
        "percentage": [100.0, 100.0],
    })
    insights = generate_segment_insights(seg_df)
    assert len(insights) >= 2
    assert any("Cohort 1" in text for text in insights)
    assert any("do not imply demographic causation" in text for text in insights)


def test_phase7_reporting_deliverables_integrity():
    """Verify Phase 7 reports exist, enforce non-causal language, and maintain approved statistical standards."""
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent

    report_files = [
        root / "reports" / "project_report.md",
        root / "reports" / "key_insights_report.md",
        root / "reports" / "recommendations_report.md",
        root / "docs" / "INTERVIEW_PREPARATION.md",
        root / "docs" / "PORTFOLIO_PRESENTATION_GUIDE.md",
    ]

    for rf in report_files:
        assert rf.exists(), f"Missing required Phase 7 deliverable: {rf.name}"
        content = rf.read_text(encoding="utf-8")
        assert len(content) > 1000, f"File {rf.name} is unexpectedly short"

    # Verify approved RemoteWork missingness statement in project_report.md
    proj_report = (root / "reports" / "project_report.md").read_text(encoding="utf-8")
    assert "RemoteWork nonresponse is associated with respondent branch" in proj_report
    assert "The available data alone cannot distinguish MAR from MNAR" in proj_report
    assert "+30.65" in proj_report
    assert "0.2674" in proj_report or "0.267353" in proj_report

    # Verify approved Phase 5 RQ1, RQ2, and RQ3 statistics in project_report.md
    assert "30,780" in proj_report
    assert "38.3898" in proj_report
    assert "30.1175" in proj_report
    assert "1.178" in proj_report
    assert "47.99" in proj_report
    assert "43.92" in proj_report
    assert "13.17" in proj_report
    assert "12.79" in proj_report
    assert "0.1203" in proj_report
    assert "23,766" in proj_report
    assert "11.6172" in proj_report or "11.62" in proj_report
    assert "0.002439" in proj_report or "0.24%" in proj_report

    # Negative assertions for deprecated / unapproved figures
    assert "1.324" not in proj_report
    assert "50.32%" not in proj_report
    assert "13.42%" not in proj_report
    assert "12.98%" not in proj_report
    assert "0.1204" not in proj_report
    assert "14,817" not in proj_report

    # Verify AI agent practical effect size caveat in key_insights_report.md
    key_insights = (root / "reports" / "key_insights_report.md").read_text(encoding="utf-8")
    assert "0.002439" in key_insights or "0.24%" in key_insights
    assert "0.1203" in key_insights
    assert "0.1204" not in key_insights
    assert "negligible" in key_insights.lower()
    assert "0.003777" not in key_insights
    assert "0.38%" not in key_insights
    assert "14,817" not in key_insights
    assert "Systems Renaissance" not in key_insights
    assert "Web Fatigue" not in key_insights

    # Verify recommendations report separates facts from recommendations
    recs_report = (root / "reports" / "recommendations_report.md").read_text(encoding="utf-8")
    assert "Measured Facts" in recs_report
    assert "Strategic Recommendations" in recs_report
