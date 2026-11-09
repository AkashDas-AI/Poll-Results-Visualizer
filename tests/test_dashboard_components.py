"""Unit tests for Dashboard Components (Charts, Filters, KPI Cards, Data Provider).

Validates chart creation, empty DataFrame resilience, dual percentage arithmetic,
cohort filtering logic, and executive telemetry metrics.

Author: Akash Das
Project: Poll Results Visualizer
Phase: Phase 6 — Visualization
"""

import pandas as pd
import plotly.graph_objects as go
import pytest
from pathlib import Path

from app.components.charts import (
    plot_distribution_bar,
    plot_distribution_pie,
    plot_segment_breakdown_bar,
    plot_trend_line,
    plot_horizontal_bar_with_denominators,
    plot_technology_comparison_bar,
    plot_compensation_box,
    plot_missingness_ranking_bar,
    plot_sample_flow_funnel,
)
from app.components.filters import EXPERIENCE_BRACKETS
from app.data_provider import get_survey_dataset, get_survey_overview_kpis
from src.datasets.stackoverflow_2025 import analyze_multi_select
from src.analysis import calculate_contingency_and_chi2

HAS_CLEANED_PARQUET = Path("data/processed/survey_results_cleaned.parquet").exists()
require_parquet = pytest.mark.skipif(
    not HAS_CLEANED_PARQUET,
    reason="Cleaned survey dataset not present on disk (expected in fresh git clone)",
)


@pytest.fixture
def sample_distribution_df():
    return pd.DataFrame({
        "option": ["Python", "JavaScript", "Rust"],
        "response_count": [150, 200, 50],
        "percentage": [37.5, 50.0, 12.5],
    })


@pytest.fixture
def sample_survey_slice():
    return pd.DataFrame({
        "ResponseId": [1, 2, 3, 4, 5],
        "Country": ["United States", "Germany", "United States", "India", "Canada"],
        "DevType": [
            "Developer, full-stack",
            "DevOps engineer or professional",
            "Developer, back-end",
            "Developer, full-stack",
            "Engineering manager",
        ],
        "WorkExp_num": [2.0, 5.0, 12.0, 0.5, 25.0],
        "RemoteWork": ["Remote", "Hybrid", "In-person", "Remote", "In-person"],
        "ConvertedCompYearly": [120000.0, 95000.0, 500.0, 45000.0, 2500000.0],
    })


# --- Chart Tests ---

def test_plot_distribution_bar(sample_distribution_df):
    fig = plot_distribution_bar(sample_distribution_df, title="Language Distribution")
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1
    assert fig.data[0].orientation == "h"


def test_plot_distribution_bar_empty():
    fig = plot_distribution_bar(pd.DataFrame(), title="Empty")
    assert isinstance(fig, go.Figure)
    # Returns standardized empty figure
    assert len(fig.data) == 0 or (len(fig.layout.annotations) > 0)


def test_plot_distribution_pie(sample_distribution_df):
    fig = plot_distribution_pie(sample_distribution_df, title="Share")
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1
    assert fig.data[0].type == "pie"


def test_plot_distribution_pie_empty():
    fig = plot_distribution_pie(pd.DataFrame(), title="Empty")
    assert isinstance(fig, go.Figure)


def test_plot_segment_breakdown_bar():
    seg_df = pd.DataFrame({
        "segment": ["Junior", "Junior", "Senior", "Senior"],
        "option": ["Python", "Rust", "Python", "Rust"],
        "percentage": [60.0, 40.0, 30.0, 70.0],
        "response_count": [60, 40, 30, 70],
    })
    fig = plot_segment_breakdown_bar(seg_df, title="Segment Comparison")
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 2  # Python, Rust


def test_plot_trend_line():
    trend_df = pd.DataFrame({
        "date": ["2025-06-01", "2025-06-02"],
        "response_count": [100, 150],
    })
    fig = plot_trend_line(trend_df, title="Velocity")
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1
    assert fig.data[0].type == "scatter"


def test_plot_horizontal_bar_with_denominators(sample_distribution_df):
    n_answered = 400
    n_total = 1000
    fig = plot_horizontal_bar_with_denominators(
        sample_distribution_df,
        category_col="option",
        count_col="response_count",
        n_answered=n_answered,
        n_total=n_total,
        title="Languages with Dual Denominators",
    )
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1
    trace = fig.data[0]
    # Check that highest count (JavaScript: 200) has x = 200 / 400 * 100 = 50.0%
    assert 50.0 in trace.x
    # Customdata checks: [count, n_answered, pct_total, n_total]
    cd = trace.customdata
    assert cd.shape[1] == 4
    # For count 200, pct_total should be 200 / 1000 * 100 = 20.0%
    js_idx = list(trace.y).index("JavaScript")
    assert cd[js_idx][0] == 200
    assert cd[js_idx][1] == 400
    assert pytest.approx(cd[js_idx][2], 0.01) == 20.0
    assert cd[js_idx][3] == 1000


def test_plot_technology_comparison_bar():
    comp_df = pd.DataFrame({
        "technology": ["Python", "Rust", "Go"],
        "current_pct": [60.0, 15.0, 18.0],
        "desired_pct": [55.0, 35.0, 30.0],
    })
    fig = plot_technology_comparison_bar(
        comp_df,
        tech_col="technology",
        current_col="current_pct",
        desired_col="desired_pct",
        title="Migration",
    )
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 2  # Current and Desired traces
    assert fig.data[0].name == "Currently Worked With"
    assert fig.data[1].name == "Want to Work With"


def test_plot_compensation_box(sample_survey_slice):
    fig = plot_compensation_box(
        sample_survey_slice,
        group_col="DevType",
        comp_col="ConvertedCompYearly",
        title="Role Compensation",
    )
    assert isinstance(fig, go.Figure)
    assert len(fig.data) > 0
    assert fig.data[0].type == "box"


def test_plot_missingness_ranking_bar():
    missing_df = pd.DataFrame({
        "column": ["RemoteWork", "WorkExp", "ConvertedCompYearly"],
        "missing_count": [15000, 6000, 25000],
        "missing_pct": [30.5, 12.2, 50.8],
        "non_null_count": [34191, 43191, 24191],
    })
    fig = plot_missingness_ranking_bar(missing_df, title="Missingness")
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1
    # Check that highest missing percentage (50.8) is plotted
    assert 50.8 in fig.data[0].x


def test_plot_sample_flow_funnel():
    stages = ["Stage 1", "Stage 2", "Stage 3"]
    counts = [1000, 500, 250]
    fig = plot_sample_flow_funnel(stages, counts, title="Flow Funnel")
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1
    assert fig.data[0].type == "funnel"


# --- Filtering Logic Unit Tests ---

def test_experience_brackets_slicing(sample_survey_slice):
    # Test Entry-level (0-2 yrs)
    low, high = EXPERIENCE_BRACKETS["Entry-level (0–2 years)"]
    entry_df = sample_survey_slice[
        (sample_survey_slice["WorkExp_num"] >= low) & (sample_survey_slice["WorkExp_num"] <= high)
    ]
    assert len(entry_df) == 2  # 2.0 and 0.5
    assert set(entry_df["ResponseId"]) == {1, 4}

    # Test Veteran (21+ yrs)
    v_low, v_high = EXPERIENCE_BRACKETS["Veteran (21+ years)"]
    vet_df = sample_survey_slice[
        (sample_survey_slice["WorkExp_num"] >= v_low) & (sample_survey_slice["WorkExp_num"] <= v_high)
    ]
    assert len(vet_df) == 1
    assert vet_df.iloc[0]["ResponseId"] == 5


def test_compensation_trimming_slicing(sample_survey_slice):
    comp = sample_survey_slice["ConvertedCompYearly"]
    # Trim <1000 and >1000000
    valid_mask = comp.notna() & (comp > 0)
    in_range_mask = (comp >= 1000) & (comp <= 1000000)
    trimmed = sample_survey_slice[~valid_mask | in_range_mask]
    # ResponseId 3 ($500) and ResponseId 5 ($2.5M) should be excluded
    assert len(trimmed) == 3
    assert set(trimmed["ResponseId"]) == {1, 2, 4}


# --- Data Provider Caching & Telemetry Tests ---

@require_parquet
def test_get_survey_dataset_loads_canonical_parquet():
    df = get_survey_dataset()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 49191
    assert "ResponseId" in df.columns
    assert "YearsCode_num" in df.columns
    assert "WorkExp_num" in df.columns
    assert "ConvertedCompYearly" in df.columns


@require_parquet
def test_get_survey_overview_kpis():
    kpis = get_survey_overview_kpis()
    assert kpis["n_raw"] == 49191
    assert kpis["n_official"] == 49009
    assert kpis["countries_count"] == 177
    assert kpis["ai_adoption_rate"] == 78.5
    assert kpis["ai_users_count"] == 26469
    assert kpis["n_answered_ai"] == 33720
    assert kpis["n_answered_comp"] == 23947
    assert kpis["median_comp_usd"] == 75320.0


# --- Phase 6 Reconciliation & Verification Unit Tests ---

@require_parquet
def test_age_distribution_exact_counts_and_percentages():
    df = get_survey_dataset()
    age_valid = df["Age"].dropna()
    assert len(age_valid) == 49191
    counts = age_valid.value_counts().to_dict()

    expected_counts = {
        "25-34 years old": 16519,
        "35-44 years old": 13241,
        "18-24 years old": 9210,
        "45-54 years old": 6275,
        "55-64 years old": 2626,
        "65 years or older": 942,
        "Prefer not to say": 378,
    }

    assert len(counts) == 7
    for cat, exp_cnt in expected_counts.items():
        assert counts[cat] == exp_cnt
        exp_pct = round(exp_cnt / 49191 * 100.0, 2)
        act_pct = round(counts[cat] / 49191 * 100.0, 2)
        assert act_pct == exp_pct

    # Validate modal bracket: 25-34 years old at 33.58%
    assert counts["25-34 years old"] == 16519
    modal_pct = round(16519 / 49191 * 100.0, 2)
    assert modal_pct == 33.58


@require_parquet
def test_technology_exact_respondent_denominators():
    df = get_survey_dataset()

    # Languages: N_answered = 31,671
    lang_dist = analyze_multi_select(df, "LanguageHaveWorkedWith")
    n_lang_ans = len(df["LanguageHaveWorkedWith"].dropna())
    assert n_lang_ans == 31671
    lang_map = dict(zip(lang_dist["option"], zip(lang_dist["response_count"], lang_dist["pct_of_respondents"])))

    # Python: 18,410 / 31,671 = 58.13%
    py_cnt, py_pct = lang_map["Python"]
    assert py_cnt == 18410
    assert py_pct == 58.13

    # TypeScript: 13,859 / 31,671 = 43.76%
    ts_cnt, ts_pct = lang_map["TypeScript"]
    assert ts_cnt == 13859
    assert ts_pct == 43.76

    # Databases: N_answered = 25,550
    db_dist = analyze_multi_select(df, "DatabaseHaveWorkedWith")
    n_db_ans = len(df["DatabaseHaveWorkedWith"].dropna())
    assert n_db_ans == 25550
    db_map = dict(zip(db_dist["option"], zip(db_dist["response_count"], db_dist["pct_of_respondents"])))

    # SQLite: 9,798 / 25,550 = 38.35%
    sqlite_cnt, sqlite_pct = db_map["SQLite"]
    assert sqlite_cnt == 9798
    assert sqlite_pct == 38.35

    # Platforms: N_answered = 24,258
    plat_dist = analyze_multi_select(df, "PlatformHaveWorkedWith")
    n_plat_ans = len(df["PlatformHaveWorkedWith"].dropna())
    assert n_plat_ans == 24258
    plat_map = dict(zip(plat_dist["option"], zip(plat_dist["response_count"], plat_dist["pct_of_respondents"])))

    # Microsoft Azure: 6,447 / 24,258 = 26.58%
    azure_cnt, azure_pct = plat_map["Microsoft Azure"]
    assert azure_cnt == 6447
    assert azure_pct == 26.58

    # Google Cloud: 6,015 / 24,258 = 24.80%
    gcp_cnt, gcp_pct = plat_map["Google Cloud"]
    assert gcp_cnt == 6015
    assert gcp_pct == 24.80


@require_parquet
def test_paired_technology_sample_size():
    df = get_survey_dataset()
    paired_df = df.dropna(subset=["LanguageHaveWorkedWith", "LanguageWantToWorkWith"])
    n_paired = len(paired_df)
    assert n_paired == 27079

    curr_dist = analyze_multi_select(paired_df, "LanguageHaveWorkedWith")
    des_dist = analyze_multi_select(paired_df, "LanguageWantToWorkWith")
    curr_map = dict(zip(curr_dist["option"], curr_dist["pct_of_respondents"]))
    des_map = dict(zip(des_dist["option"], des_dist["pct_of_respondents"]))

    # JavaScript: 66.09% worked, 39.07% desired -> gap -27.02 pp
    assert curr_map["JavaScript"] == 66.09
    assert des_map["JavaScript"] == 39.07
    assert round(des_map["JavaScript"] - curr_map["JavaScript"], 2) == -27.02

    # Rust: 15.75% worked, 34.20% desired -> gap +18.45 pp
    assert curr_map["Rust"] == 15.75
    assert des_map["Rust"] == 34.20
    assert round(des_map["Rust"] - curr_map["Rust"], 2) == 18.45


def test_remotework_missingness_approved_wording():
    approved_sentence = (
        "RemoteWork nonresponse is associated with respondent branch. "
        "The observed association suggests that missingness is not MCAR with respect to MainBranch. "
        "The available data alone cannot distinguish MAR from MNAR."
    )
    import re
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent

    # Test presence in 1_Overview.py and 4_Data_Quality.py
    for file_rel in ["app/pages/1_Overview.py", "app/pages/4_Data_Quality.py"]:
        file_path = root / file_rel
        content = file_path.read_text(encoding="utf-8")
        # Collapse multi-line python string literals by stripping quotes and collapsing whitespace
        normalized = re.sub(r'["\']\s*["\']', '', content)
        normalized = " ".join(normalized.split())
        assert approved_sentence in normalized, f"Approved sentence missing in {file_rel}"

    # Test absence of unsupported causal routing claims
    overview_text = (root / "app" / "pages" / "1_Overview.py").read_text(encoding="utf-8")
    dq_text = (root / "app" / "pages" / "4_Data_Quality.py").read_text(encoding="utf-8")
    forbidden_phrases = [
        "systematically routed around employment questions",
        "systematically routed around this question",
        "Structural Non-Response in `RemoteWork`",
    ]
    for phrase in forbidden_phrases:
        assert phrase not in overview_text, f"Found '{phrase}' in 1_Overview.py"
        assert phrase not in dq_text, f"Found '{phrase}' in 4_Data_Quality.py"


@require_parquet
def test_cohort_filtering_preserves_valid_denominators():
    df = get_survey_dataset()
    # Filter to United States respondents
    us_df = df[df["Country"] == "United States of America"]
    assert len(us_df) > 0
    us_lang = analyze_multi_select(us_df, "LanguageHaveWorkedWith")
    assert not us_lang.empty
    # Sum of respondent percentages can exceed 100% due to multi-select
    assert us_lang["pct_of_respondents"].max() <= 100.0

    # Filter to empty DataFrame
    empty_df = df[df["Country"] == "NonExistentCountry"]
    assert len(empty_df) == 0
    fig_empty = plot_horizontal_bar_with_denominators(
        empty_df,
        category_col="Language",
        count_col="Count",
        n_answered=0,
        n_total=0,
        title="Empty Slice",
    )
    assert isinstance(fig_empty, go.Figure)


@require_parquet
def test_remotework_contingency_table_exact_reconciliation():
    df = get_survey_dataset()
    df["RemoteWork_missing"] = df["RemoteWork"].isna().map({True: "Missing", False: "Answered"})

    res = calculate_contingency_and_chi2(df, "MainBranch", "RemoteWork_missing")
    obs = res["observed"]

    # Verify column and row totals
    assert res["total_n"] == 49191
    assert obs["Answered"].sum() == 33780
    assert obs["Missing"].sum() == 15411

    # Verify exact cell counts
    expected_cells = {
        "I am a developer by profession": (28286, 9181, 37467),
        "I am learning to code": (552, 2033, 2585),
        "I am not primarily a developer, but I write code sometimes as part of my work/studies": (3172, 1722, 4894),
        "I code primarily as a hobby": (530, 1394, 1924),
        "I used to be a developer by profession, but no longer am": (642, 683, 1325),
        "I work with developers or my work supports developers but am not a developer by profession": (598, 398, 996),
    }

    for branch, (exp_ans, exp_miss, exp_tot) in expected_cells.items():
        ans_val = obs.loc[branch, "Answered"]
        miss_val = obs.loc[branch, "Missing"]
        assert ans_val == exp_ans
        assert miss_val == exp_miss
        assert ans_val + miss_val == exp_tot

    # Recalculated independence test metrics
    assert round(res["chi2"], 2) == 5333.84
    assert res["df"] == 5
    assert res["p_value"] < 1e-300
    assert round(res["cramers_v"], 4) == 0.3293


def test_remotework_compensation_model_c_reconciliation():
    import json
    import math
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent

    metrics_path = root / "outputs" / "analysis_summary_metrics.json"
    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    rq4 = metrics["rq4_remote_work"]
    assert rq4["complete_cases_model_c"] == 20236
    assert round(rq4["model_c_r_squared"], 4) == 0.4254
    assert rq4["df_model"] == 18
    assert rq4["df_residual"] == 20217

    cond_diffs = {item["arrangement"]: item for item in rq4["conditional_compensation_differences"]}

    # Fully Remote: beta = +0.2674, exact exponential percentage = 100 * (exp(beta) - 1) = +30.65%
    remote_item = cond_diffs["Remote"]
    beta_remote = remote_item["beta"]
    assert round(beta_remote, 4) == 0.2674
    exact_pct_remote = 100.0 * (math.exp(beta_remote) - 1.0)
    assert round(exact_pct_remote, 2) == 30.65
    assert round(remote_item["pct_difference_vs_inperson"], 2) == 30.65

    # Check that dashboard page 3 does not contain deprecated +0.339 or role claim
    page3_text = (root / "app" / "pages" / "3_Segment_Comparison.py").read_text(encoding="utf-8")
    assert "0.339" not in page3_text
    assert "+30.65% for Remote" in page3_text
    assert "role reduces" not in page3_text
