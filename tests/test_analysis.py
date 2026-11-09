"""Unit tests for analysis module.

Author: Akash Das
"""

import numpy as np
import pytest
import pandas as pd
from src.analysis import (
    calculate_kpis,
    get_response_distribution,
    get_segment_comparison,
    get_trend_over_time,
    calculate_contingency_and_chi2,
    calculate_odds_ratios,
    fit_ols,
    calculate_vif,
    compare_groups_continuous,
    normal_cdf,
    normal_p_value,
    chi2_p_value,
)


def test_calculate_kpis_distinguishes_unique_respondents():
    """Verify total responses vs unique respondents distinction."""
    df = pd.DataFrame({
        "respondent_id": ["R1", "R1", "R2"],
        "question": ["Q1", "Q2", "Q1"],
        "option": ["Yes", "No", "Yes"],
        "response_date": ["2024-01-01", "2024-01-02", "2024-01-02"],
        "segment": ["Cohort 1", "Cohort 1", "Cohort 2"],
    })
    kpis = calculate_kpis(df)
    assert kpis["total_responses"] == 3
    assert kpis["unique_respondents"] == 2
    assert kpis["total_questions"] == 2
    assert kpis["total_segments"] == 2
    assert kpis["date_min"] == "2024-01-01"
    assert kpis["date_max"] == "2024-01-02"


def test_get_response_distribution():
    """Verify option distribution and percentage calculations."""
    df = pd.DataFrame({
        "respondent_id": ["R1", "R2", "R3", "R4"],
        "question": ["Q1", "Q1", "Q1", "Q2"],
        "option": ["Option A", "Option A", "Option B", "Option A"],
        "response_date": ["2024-01-01"] * 4,
        "segment": ["S1"] * 4,
    })
    dist = get_response_distribution(df, "Q1")
    assert len(dist) == 2
    assert dist.iloc[0]["option"] == "Option A"
    assert dist.iloc[0]["response_count"] == 2
    assert dist.iloc[0]["percentage"] == pytest_approx(66.67, 0.01)
    assert dist.iloc[1]["option"] == "Option B"
    assert dist.iloc[1]["response_count"] == 1
    assert dist.iloc[1]["percentage"] == pytest_approx(33.33, 0.01)


def pytest_approx(val, tol):
    import pytest
    return pytest.approx(val, abs=tol)


def test_get_segment_comparison():
    """Verify within-segment percentage calculations."""
    df = pd.DataFrame({
        "respondent_id": ["R1", "R2", "R3"],
        "question": ["Q1", "Q1", "Q1"],
        "option": ["Yes", "No", "Yes"],
        "response_date": ["2024-01-01"] * 3,
        "segment": ["Cohort A", "Cohort A", "Cohort B"],
    })
    seg = get_segment_comparison(df, "Q1")
    cohort_a = seg[seg["segment"] == "Cohort A"]
    assert cohort_a[cohort_a["option"] == "Yes"]["percentage"].iloc[0] == 50.0
    assert cohort_a[cohort_a["option"] == "No"]["percentage"].iloc[0] == 50.0

    cohort_b = seg[seg["segment"] == "Cohort B"]
    assert cohort_b[cohort_b["option"] == "Yes"]["percentage"].iloc[0] == 100.0


def test_get_trend_over_time():
    """Verify time series volume aggregation."""
    df = pd.DataFrame({
        "respondent_id": ["R1", "R2", "R3"],
        "question": ["Q1", "Q1", "Q1"],
        "option": ["Yes", "No", "Yes"],
        "response_date": ["2024-01-01", "2024-01-01", "2024-01-02"],
        "segment": ["S1"] * 3,
    })
    trend = get_trend_over_time(df)
    assert len(trend) == 2
    assert trend.iloc[0]["response_count"] == 2
    assert trend.iloc[1]["response_count"] == 1


def test_analysis_empty_dataframe_safety():
    """Verify all analysis functions handle empty DataFrames safely without errors."""
    empty_df = pd.DataFrame(columns=["respondent_id", "question", "option", "response_date", "segment"])

    # 1. KPIs on empty DataFrame
    kpis = calculate_kpis(empty_df)
    assert kpis["total_responses"] == 0
    assert kpis["unique_respondents"] == 0
    assert kpis["total_questions"] == 0
    assert kpis["total_segments"] == 0
    assert kpis["date_min"] is None
    assert kpis["date_max"] is None

    # 2. Distribution on empty DataFrame
    dist = get_response_distribution(empty_df, "Nonexistent Question")
    assert dist.empty
    assert list(dist.columns) == ["option", "response_count", "percentage"]

    # 3. Segment comparison on empty DataFrame
    seg = get_segment_comparison(empty_df, "Nonexistent Question")
    assert seg.empty
    assert list(seg.columns) == ["segment", "option", "response_count", "segment_total", "percentage"]

    # 4. Trend on empty DataFrame
    trend = get_trend_over_time(empty_df)
    assert trend.empty
    assert list(trend.columns) == ["date", "response_count"]


# ---------------------------------------------------------------------------
# Phase 5 Advanced Analytical Tests
# ---------------------------------------------------------------------------


def test_statistical_distributions_exact_prob():
    """Verify standard normal and chi-squared survival probabilities."""
    assert pytest_approx(normal_cdf(0.0), 1e-4) == 0.5
    assert pytest_approx(normal_p_value(0.0), 1e-4) == 1.0
    assert pytest_approx(normal_p_value(1.959964), 1e-3) == 0.05
    assert pytest_approx(normal_p_value(2.575829), 1e-3) == 0.01

    # Chi-squared critical values
    assert pytest_approx(chi2_p_value(3.84146, 1), 1e-3) == 0.05
    assert pytest_approx(chi2_p_value(5.99146, 2), 1e-3) == 0.05
    assert pytest_approx(chi2_p_value(9.48773, 4), 1e-3) == 0.05
    assert chi2_p_value(-1.0, 1) == 1.0
    assert chi2_p_value(10.0, 0) == 1.0


def test_calculate_contingency_and_chi2_synthetic():
    """Verify contingency matrix, Pearson Chi-squared, and Cramer's V."""
    # Construct synthetic data with known association
    data = (
        [{"Group": "A", "Outcome": "Yes"}] * 60
        + [{"Group": "A", "Outcome": "No"}] * 40
        + [{"Group": "B", "Outcome": "Yes"}] * 20
        + [{"Group": "B", "Outcome": "No"}] * 80
    )
    df = pd.DataFrame(data)
    res = calculate_contingency_and_chi2(df, "Group", "Outcome")

    assert res["total_n"] == 200
    assert res["df"] == 1
    assert res["observed"].loc["A", "Yes"] == 60
    assert res["observed"].loc["A", "No"] == 40
    assert res["observed"].loc["B", "Yes"] == 20
    assert res["observed"].loc["B", "No"] == 80

    # Expected frequencies
    assert res["expected"].loc["A", "Yes"] == 40.0
    assert res["expected"].loc["A", "No"] == 60.0

    # Chi2 = (20)^2 / 40 + (-20)^2 / 60 + (-20)^2 / 40 + (20)^2 / 60 = 10 + 6.667 + 10 + 6.667 = 33.333
    assert pytest_approx(res["chi2"], 0.05) == 33.333
    assert res["p_value"] < 0.0001
    # Cramer's V = sqrt(33.333 / 200) = sqrt(0.16667) ~ 0.408
    assert pytest_approx(res["cramers_v"], 0.01) == 0.408
    assert "Total" in res["observed_with_margins"].columns


def test_calculate_contingency_errors():
    """Verify contingency calculation handles invalid dimensions gracefully."""
    empty_df = pd.DataFrame(columns=["A", "B"])
    with pytest.raises(ValueError, match="No non-null overlapping records"):
        calculate_contingency_and_chi2(empty_df, "A", "B")

    single_val_df = pd.DataFrame({"A": ["X", "X"], "B": ["Y", "Y"]})
    with pytest.raises(ValueError, match="at least 2 rows and 2 columns"):
        calculate_contingency_and_chi2(single_val_df, "A", "B")


def test_calculate_odds_ratios():
    """Verify pairwise Odds Ratios and Wald 95% confidence intervals."""
    # Reference: Group 0 (pos: 10, neg: 90) -> odds = 10/90 = 1/9
    # Exposed: Group 1 (pos: 20, neg: 80) -> odds = 20/80 = 2/8 = 1/4
    # OR = (1/4) / (1/9) = 9/4 = 2.25
    data = (
        [{"Group": "Baseline", "Outcome": "Success"}] * 10
        + [{"Group": "Baseline", "Outcome": "Failure"}] * 90
        + [{"Group": "Treatment", "Outcome": "Success"}] * 20
        + [{"Group": "Treatment", "Outcome": "Failure"}] * 80
    )
    df = pd.DataFrame(data)
    or_df = calculate_odds_ratios(df, "Group", "Outcome", "Success", "Baseline")

    assert len(or_df) == 2
    ref_row = or_df[or_df["category"] == "Baseline (Reference)"].iloc[0]
    assert ref_row["odds_ratio"] == 1.0
    assert ref_row["pct_positive"] == 10.0

    treat_row = or_df[or_df["category"] == "Treatment"].iloc[0]
    assert pytest_approx(treat_row["odds_ratio"], 0.01) == 2.25
    assert treat_row["ci_lower"] < 2.25 < treat_row["ci_upper"]
    assert treat_row["pct_positive"] == 20.0
    assert treat_row["p_value"] < 0.10


def test_fit_ols_linear_model():
    """Verify OLS regression parameter estimates and diagnostics on known DGP."""
    np.random.seed(42)
    n = 1000
    x1 = np.random.normal(10, 2, n)
    x2 = np.random.normal(5, 1, n)
    noise = np.random.normal(0, 0.5, n)
    y = 5.0 + 2.0 * x1 - 3.0 * x2 + noise

    df = pd.DataFrame({"y": y, "x1": x1, "x2": x2})
    model = fit_ols(df, y_col="y", x_num_cols=["x1", "x2"], add_intercept=True)

    assert model["n_obs"] == 1000
    assert model["df_model"] == 2
    assert model["df_residual"] == 997
    assert model["r_squared"] > 0.95

    coefs = model["coefficients"].set_index("term")
    assert pytest_approx(coefs.loc["Intercept", "coef"], 0.2) == 5.0
    assert pytest_approx(coefs.loc["x1", "coef"], 0.05) == 2.0
    assert pytest_approx(coefs.loc["x2", "coef"], 0.05) == -3.0

    assert coefs.loc["x1", "p_value"] < 0.001
    assert coefs.loc["x2", "p_value"] < 0.001
    assert model["f_p_value"] < 0.001


def test_fit_ols_with_categorical_predictors():
    """Verify OLS dummy variable expansion and baseline category omission."""
    np.random.seed(123)
    n = 600
    roles = np.random.choice(["Developer", "Manager", "Analyst"], size=n)
    experience = np.random.uniform(1, 20, size=n)
    salary_log = 10.0 + 0.05 * experience + (roles == "Manager") * 0.4 - (roles == "Analyst") * 0.2
    salary_log += np.random.normal(0, 0.1, n)

    df = pd.DataFrame({"log_salary": salary_log, "exp": experience, "role": roles})
    model = fit_ols(
        df,
        y_col="log_salary",
        x_num_cols=["exp"],
        x_cat_cols=["role"],
        reference_categories={"role": "Developer"},
    )

    terms = model["coefficients"]["term"].tolist()
    assert "Intercept" in terms
    assert "exp" in terms
    assert "role_Manager" in terms
    assert "role_Analyst" in terms
    assert "role_Developer" not in terms  # Omitted reference baseline

    coefs = model["coefficients"].set_index("term")
    assert coefs.loc["role_Manager", "coef"] > 0.35
    assert coefs.loc["role_Analyst", "coef"] < -0.15


def test_fit_ols_error_cases():
    """Verify OLS handles invalid degrees of freedom and empty inputs."""
    df_empty = pd.DataFrame(columns=["y", "x"])
    with pytest.raises(ValueError, match="No complete cases"):
        fit_ols(df_empty, "y", ["x"])

    df_under = pd.DataFrame({"y": [1.0, 2.0], "x1": [1.0, 2.0], "x2": [3.0, 4.0]})
    with pytest.raises(ValueError, match="Insufficient degrees of freedom"):
        fit_ols(df_under, "y", ["x1", "x2"], add_intercept=True)


def test_calculate_vif():
    """Verify Variance Inflation Factor detects collinearity."""
    np.random.seed(42)
    n = 500
    x1 = np.random.normal(0, 1, n)
    x2 = np.random.normal(0, 1, n)
    # x3 strongly collinear with x1
    x3 = x1 * 0.99 + np.random.normal(0, 0.05, n)

    df = pd.DataFrame({"x1": x1, "x2": x2, "x3": x3})
    vif_df = calculate_vif(df, x_num_cols=["x1", "x2", "x3"])

    assert len(vif_df) == 3
    x2_vif = vif_df[vif_df["variable"] == "x2"]["vif"].iloc[0]
    x1_vif = vif_df[vif_df["variable"] == "x1"]["vif"].iloc[0]
    x3_vif = vif_df[vif_df["variable"] == "x3"]["vif"].iloc[0]

    assert x2_vif < 2.0  # Orthogonal
    assert x1_vif > 10.0  # High collinearity
    assert x3_vif > 10.0


def test_compare_groups_continuous():
    """Verify group-wise descriptive statistics and ANOVA calculation."""
    df = pd.DataFrame({
        "group": ["A"] * 50 + ["B"] * 50 + ["C"] * 50,
        "score": [10.0] * 50 + [15.0] * 50 + [20.0] * 50,
    })
    res = compare_groups_continuous(df, "group", "score")

    assert res["total_n"] == 150
    assert res["df_between"] == 2
    assert res["df_within"] == 147
    assert res["anova_p_value"] < 0.0001

    summary = res["summary"].set_index("group")
    assert summary.loc["A", "mean"] == 10.0
    assert summary.loc["B", "mean"] == 15.0
    assert summary.loc["C", "mean"] == 20.0
