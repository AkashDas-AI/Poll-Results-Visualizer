"""Analysis module for Poll Results Visualizer.

Provides deterministic statistical aggregations, response distributions,
cross-tabulations by demographic segment, temporal volume trends (Phases 1-2),
as well as advanced econometric modeling, Ordinary Least Squares (OLS) multivariable
regression, Variance Inflation Factors (VIF), contingency tables with Pearson's
chi-squared test and Cramér's V, pairwise Odds Ratios, and continuous group
comparisons for deep survey analysis (Phase 5).

Author: Akash Das
Project: Poll Results Visualizer - Phase 5 (Analysis)
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from src.config import (
    COL_OPTION,
    COL_QUESTION,
    COL_RESPONDENT_ID,
    COL_RESPONSE_DATE,
    COL_SEGMENT,
)


# ---------------------------------------------------------------------------
# Phase 1 & 2 Core Aggregations (Preserved)
# ---------------------------------------------------------------------------


def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Compute high-level Key Performance Indicators for the dataset.

    Distinguishes total response records from unique respondent counts.

    Args:
        df: Input polling DataFrame.

    Returns:
        Dict[str, Any]: High-level metrics.
    """
    if df.empty:
        return {
            "total_responses": 0,
            "unique_respondents": 0,
            "total_questions": 0,
            "total_segments": 0,
            "date_min": None,
            "date_max": None,
        }

    valid_dates = pd.to_datetime(df[COL_RESPONSE_DATE], errors="coerce").dropna()

    return {
        "total_responses": int(len(df)),
        "unique_respondents": int(df[COL_RESPONDENT_ID].nunique()),
        "total_questions": int(df[COL_QUESTION].nunique()),
        "total_segments": int(df[COL_SEGMENT].nunique()),
        "date_min": valid_dates.min().strftime("%Y-%m-%d") if not valid_dates.empty else None,
        "date_max": valid_dates.max().strftime("%Y-%m-%d") if not valid_dates.empty else None,
    }


def get_response_distribution(df: pd.DataFrame, question: str) -> pd.DataFrame:
    """Calculate option response counts and percentage distribution for a question.

    Protects against division by zero and normalizes within the question.

    Args:
        df: Input polling DataFrame.
        question: Specific question string to filter by.

    Returns:
        pd.DataFrame: Contains [option, response_count, percentage].
    """
    sub_df = df[df[COL_QUESTION] == question]
    total_answers = len(sub_df)

    if total_answers == 0:
        return pd.DataFrame(columns=[COL_OPTION, "response_count", "percentage"])

    counts = sub_df[COL_OPTION].value_counts(dropna=False).reset_index()
    counts.columns = [COL_OPTION, "response_count"]

    # Safe percentage calculation
    counts["percentage"] = (counts["response_count"] / total_answers) * 100.0
    counts["percentage"] = counts["percentage"].round(2)

    return counts.sort_values(by="response_count", ascending=False).reset_index(drop=True)


def get_segment_comparison(df: pd.DataFrame, question: str) -> pd.DataFrame:
    """Calculate option breakdown partitioned by demographic segment.

    Computes within-segment percentages (row percentage per segment)
    to allow fair comparison across cohorts of differing sample sizes.

    Args:
        df: Input polling DataFrame.
        question: Target question string.

    Returns:
        pd.DataFrame: Contains [segment, option, response_count, segment_total, percentage].
    """
    sub_df = df[df[COL_QUESTION] == question]
    if sub_df.empty:
        return pd.DataFrame(
            columns=[COL_SEGMENT, COL_OPTION, "response_count", "segment_total", "percentage"]
        )

    # Group by segment and option
    grouped = (
        sub_df.groupby([COL_SEGMENT, COL_OPTION], observed=False)
        .size()
        .reset_index(name="response_count")
    )

    # Compute segment totals
    segment_totals = sub_df.groupby(COL_SEGMENT, observed=False).size().to_dict()

    grouped["segment_total"] = grouped[COL_SEGMENT].map(segment_totals)

    # Safe percentage within segment
    grouped["percentage"] = grouped.apply(
        lambda row: round((row["response_count"] / row["segment_total"]) * 100.0, 2)
        if row["segment_total"] > 0
        else 0.0,
        axis=1,
    )

    return grouped.sort_values(
        by=[COL_SEGMENT, "response_count"], ascending=[True, False]
    ).reset_index(drop=True)


def get_trend_over_time(df: pd.DataFrame, question: Optional[str] = None) -> pd.DataFrame:
    """Aggregate response volume or option breakdown over calendar dates.

    Args:
        df: Input polling DataFrame.
        question: Optional question filter.

    Returns:
        pd.DataFrame: Contains dates and response volumes.
    """
    sub_df = df.copy()
    if question:
        sub_df = sub_df[sub_df[COL_QUESTION] == question]

    sub_df[COL_RESPONSE_DATE] = pd.to_datetime(sub_df[COL_RESPONSE_DATE], errors="coerce")
    valid_records = sub_df.dropna(subset=[COL_RESPONSE_DATE])

    if valid_records.empty:
        return pd.DataFrame(columns=["date", "response_count"])

    trend = (
        valid_records.groupby(valid_records[COL_RESPONSE_DATE].dt.date)
        .size()
        .reset_index(name="response_count")
    )
    trend.columns = ["date", "response_count"]
    trend["date"] = pd.to_datetime(trend["date"])
    return trend.sort_values(by="date").reset_index(drop=True)


# ---------------------------------------------------------------------------
# Phase 5 Advanced Analytical & Econometric Routines
# ---------------------------------------------------------------------------


def normal_cdf(z: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def normal_p_value(z: float) -> float:
    """Two-tailed p-value for a standard normal z-statistic."""
    return math.erfc(abs(z) / math.sqrt(2.0))


def gamma_inc_q(a: float, x: float) -> float:
    """Upper regularized incomplete gamma function Q(a, x) = Gamma(a, x) / Gamma(a).

    Evaluated via series expansion for x < a + 1 and Lentz continued fraction for x >= a + 1.
    Provides machine-precision survival probabilities without external C libraries.
    """
    if x <= 0.0:
        return 1.0
    if a <= 0.0:
        return 0.0

    if x < a + 1.0:
        ap = a
        sum_val = 1.0 / a
        del_val = sum_val
        for _ in range(250):
            ap += 1.0
            del_val = del_val * x / ap
            sum_val += del_val
            if abs(del_val) < abs(sum_val) * 1e-15:
                break
        gam_val = math.lgamma(a)
        p = sum_val * math.exp(-x + a * math.log(x) - gam_val)
        return max(0.0, min(1.0, 1.0 - p))
    else:
        b = x + 1.0 - a
        c = 1.0 / 1e-30
        d = 1.0 / b
        h = d
        for i in range(1, 251):
            an = -i * (i - a)
            b += 2.0
            d = an * d + b
            if abs(d) < 1e-30:
                d = 1e-30
            c = b + an / c
            if abs(c) < 1e-30:
                c = 1e-30
            d = 1.0 / d
            del_val = d * c
            h *= del_val
            if abs(del_val - 1.0) < 1e-15:
                break
        gam_val = math.lgamma(a)
        q = math.exp(-x + a * math.log(x) - gam_val) * h
        return max(0.0, min(1.0, q))


def chi2_p_value(chi2: float, df: int) -> float:
    """Exact upper-tail survival probability (p-value) for Chi-squared distribution."""
    if chi2 <= 0.0 or df <= 0:
        return 1.0
    return gamma_inc_q(df / 2.0, chi2 / 2.0)


def f_distribution_p_value(f_stat: float, df1: int, df2: int) -> float:
    """Upper-tail survival probability (p-value) for F-distribution."""
    if f_stat <= 0.0 or df1 <= 0 or df2 <= 0:
        return 1.0
    if df2 > 500:
        chi2_approx = df1 * f_stat
        return chi2_p_value(chi2_approx, df1)

    term1 = 2.0 / (9.0 * df1)
    term2 = 2.0 / (9.0 * df2)
    y = abs((1.0 - term2) * (f_stat ** (1.0 / 3.0)) - (1.0 - term1))
    den = math.sqrt(term2 * (f_stat ** (2.0 / 3.0)) + term1)
    z = y / den
    return 0.5 * math.erfc(z / math.sqrt(2.0))


def calculate_contingency_and_chi2(
    df: pd.DataFrame,
    row_col: str,
    col_col: str,
    min_count: int = 0,
) -> Dict[str, Any]:
    """Computes two-way cross-tabulation, Pearson Chi-squared test, and Cramér's V.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset.
    row_col : str
        Column name for row categories.
    col_col : str
        Column name for column categories.
    min_count : int, default 0
        Minimum cell count threshold (for filtering sparse tables if desired).

    Returns
    -------
    Dict[str, Any]
        Dictionary with observed table, expected table, chi2, df, p_value, cramers_v, total_n.
    """
    sub_df = df[[row_col, col_col]].dropna()
    total_n = len(sub_df)
    if total_n == 0:
        raise ValueError(f"No non-null overlapping records found for '{row_col}' and '{col_col}'.")

    observed = pd.crosstab(sub_df[row_col], sub_df[col_col])
    if min_count > 0:
        observed = observed[(observed.sum(axis=1) >= min_count)]
        observed = observed.loc[:, (observed.sum(axis=0) >= min_count)]

    r, c = observed.shape
    if r < 2 or c < 2:
        raise ValueError("Contingency table must have at least 2 rows and 2 columns after filtering.")

    row_totals = observed.sum(axis=1).values.astype(float)
    col_totals = observed.sum(axis=0).values.astype(float)
    grand_total = float(observed.values.sum())

    expected_mat = np.outer(row_totals, col_totals) / grand_total
    expected = pd.DataFrame(expected_mat, index=observed.index, columns=observed.columns)

    obs_mat = observed.values.astype(float)
    chi2_stat = float(
        np.sum((obs_mat - expected_mat) ** 2 / np.where(expected_mat == 0, 1e-12, expected_mat))
    )
    dof = (r - 1) * (c - 1)
    p_val = chi2_p_value(chi2_stat, dof)

    min_dim = min(r - 1, c - 1)
    cramers_v = (
        math.sqrt(chi2_stat / (grand_total * min_dim))
        if min_dim > 0 and grand_total > 0
        else 0.0
    )

    row_sums = observed.sum(axis=1)
    proportions = observed.div(row_sums, axis=0) * 100.0

    observed_with_margins = observed.copy()
    observed_with_margins["Total"] = observed_with_margins.sum(axis=1)
    col_sum_row = observed_with_margins.sum(axis=0)
    col_sum_row.name = "Total"
    observed_with_margins = pd.concat([observed_with_margins, col_sum_row.to_frame().T])

    return {
        "observed": observed,
        "observed_with_margins": observed_with_margins,
        "proportions": proportions,
        "expected": expected,
        "chi2": chi2_stat,
        "df": dof,
        "p_value": p_val,
        "cramers_v": cramers_v,
        "total_n": int(grand_total),
    }


def calculate_odds_ratios(
    df: pd.DataFrame,
    exposure_col: str,
    outcome_col: str,
    positive_outcome: Any,
    reference_exposure: Any,
) -> pd.DataFrame:
    """Calculates unadjusted pairwise Odds Ratios with 95% Wald confidence intervals.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset.
    exposure_col : str
        Categorical predictor/exposure column.
    outcome_col : str
        Outcome column.
    positive_outcome : Any
        Value in outcome_col considered the event/case.
    reference_exposure : Any
        Category in exposure_col used as the baseline comparison.

    Returns
    -------
    pd.DataFrame
        Table with exposure categories, counts, Odds Ratio, 95% CI, Z-score, and p-value.
    """
    sub_df = df[[exposure_col, outcome_col]].dropna()
    categories = [cat for cat in sub_df[exposure_col].unique() if cat != reference_exposure]

    ref_mask = sub_df[exposure_col] == reference_exposure
    ref_pos = int((ref_mask & (sub_df[outcome_col] == positive_outcome)).sum())
    ref_neg = int((ref_mask & (sub_df[outcome_col] != positive_outcome)).sum())

    results = [
        {
            "category": f"{reference_exposure} (Reference)",
            "n_positive": ref_pos,
            "n_negative": ref_neg,
            "total": ref_pos + ref_neg,
            "pct_positive": (ref_pos / (ref_pos + ref_neg) * 100.0)
            if (ref_pos + ref_neg) > 0
            else 0.0,
            "odds_ratio": 1.0,
            "ci_lower": 1.0,
            "ci_upper": 1.0,
            "z_score": 0.0,
            "p_value": 1.0,
        }
    ]

    for cat in categories:
        cat_mask = sub_df[exposure_col] == cat
        cat_pos = int((cat_mask & (sub_df[outcome_col] == positive_outcome)).sum())
        cat_neg = int((cat_mask & (sub_df[outcome_col] != positive_outcome)).sum())
        tot = cat_pos + cat_neg

        if cat_pos == 0 or cat_neg == 0 or ref_pos == 0 or ref_neg == 0:
            or_val = ((cat_pos + 0.5) * (ref_neg + 0.5)) / ((cat_neg + 0.5) * (ref_pos + 0.5))
            se_ln = math.sqrt(
                1.0 / (cat_pos + 0.5)
                + 1.0 / (cat_neg + 0.5)
                + 1.0 / (ref_pos + 0.5)
                + 1.0 / (ref_neg + 0.5)
            )
        else:
            or_val = (cat_pos * ref_neg) / (cat_neg * ref_pos)
            se_ln = math.sqrt(1.0 / cat_pos + 1.0 / cat_neg + 1.0 / ref_pos + 1.0 / ref_neg)

        ln_or = math.log(or_val)
        ci_lower = math.exp(ln_or - 1.959964 * se_ln)
        ci_upper = math.exp(ln_or + 1.959964 * se_ln)
        z = ln_or / se_ln
        p = normal_p_value(z)

        results.append(
            {
                "category": str(cat),
                "n_positive": cat_pos,
                "n_negative": cat_neg,
                "total": tot,
                "pct_positive": (cat_pos / tot * 100.0) if tot > 0 else 0.0,
                "odds_ratio": or_val,
                "ci_lower": ci_lower,
                "ci_upper": ci_upper,
                "z_score": z,
                "p_value": p,
            }
        )

    return pd.DataFrame(results)


def fit_ols(
    df: pd.DataFrame,
    y_col: str,
    x_num_cols: Optional[List[str]] = None,
    x_cat_cols: Optional[List[str]] = None,
    reference_categories: Optional[Dict[str, str]] = None,
    add_intercept: bool = True,
) -> Dict[str, Any]:
    """Fits multivariable Ordinary Least Squares (OLS) regression with robust diagnostics.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset.
    y_col : str
        Continuous dependent variable column name.
    x_num_cols : Optional[List[str]], default None
        List of continuous/numeric predictor column names.
    x_cat_cols : Optional[List[str]], default None
        List of categorical predictor column names (converted to dummy variables).
    reference_categories : Optional[Dict[str, str]], default None
        Mapping of categorical column names to desired baseline reference categories.
    add_intercept : bool, default True
        Whether to include a constant term (intercept).

    Returns
    -------
    Dict[str, Any]
        Structured dictionary containing coefficients, diagnostics, residuals, fitted values.
    """
    x_num = list(x_num_cols) if x_num_cols else []
    x_cat = list(x_cat_cols) if x_cat_cols else []
    ref_map = reference_categories or {}

    all_req = [y_col] + x_num + x_cat
    clean_df = df[all_req].dropna().copy()
    n_obs = len(clean_df)
    if n_obs == 0:
        raise ValueError("No complete cases available for regression model.")

    y = clean_df[y_col].values.astype(float)

    design_parts = []
    col_names = []

    if add_intercept:
        design_parts.append(np.ones((n_obs, 1), dtype=float))
        col_names.append("Intercept")

    for num_col in x_num:
        vals = clean_df[num_col].values.astype(float).reshape(-1, 1)
        design_parts.append(vals)
        col_names.append(num_col)

    for cat_col in x_cat:
        series = clean_df[cat_col].astype(str)
        unique_cats = sorted(series.unique())
        ref = ref_map.get(cat_col)
        if ref is not None and ref in unique_cats:
            ref_category = ref
        else:
            ref_category = series.value_counts().index[0]

        for cat in unique_cats:
            if cat == ref_category:
                continue
            dummy_vals = (series == cat).astype(float).values.reshape(-1, 1)
            design_parts.append(dummy_vals)
            col_names.append(f"{cat_col}_{cat}")

    X = np.hstack(design_parts)
    p = X.shape[1]
    df_residual = n_obs - p
    df_model = p - 1 if add_intercept else p

    if df_residual <= 0:
        raise ValueError(f"Insufficient degrees of freedom: n={n_obs}, predictors={p}.")

    beta = np.linalg.pinv(X) @ y
    fitted_vals = X @ beta
    residuals = y - fitted_vals

    rss = float(np.sum(residuals ** 2))
    tss = float(np.sum((y - np.mean(y)) ** 2)) if add_intercept else float(np.sum(y ** 2))
    mss = max(0.0, tss - rss)

    r_squared = float(1.0 - (rss / tss)) if tss > 0 else 0.0
    adj_r_squared = (
        float(1.0 - ((rss / df_residual) / (tss / (n_obs - 1))))
        if tss > 0 and n_obs > 1
        else 0.0
    )

    s2 = rss / df_residual
    residual_se = math.sqrt(s2)

    xtx_inv = np.linalg.pinv(X.T @ X)
    cov_matrix = s2 * xtx_inv
    se_beta = np.sqrt(np.maximum(0.0, np.diag(cov_matrix)))

    t_stats = np.where(se_beta > 1e-12, beta / se_beta, 0.0)
    p_values = [normal_p_value(t) for t in t_stats]

    ci_lower = beta - 1.959964 * se_beta
    ci_upper = beta + 1.959964 * se_beta

    pct_effect = (np.exp(beta) - 1.0) * 100.0
    pct_lower = (np.exp(ci_lower) - 1.0) * 100.0
    pct_upper = (np.exp(ci_upper) - 1.0) * 100.0

    # Heteroskedasticity-Robust Standard Errors (White HC1: MacKinnon & White 1985)
    hc1_scale = n_obs / df_residual
    u2_weighted = (residuals ** 2) * hc1_scale
    meat = X.T @ (X * u2_weighted[:, None])
    cov_hc1 = xtx_inv @ meat @ xtx_inv
    se_robust = np.sqrt(np.maximum(0.0, np.diag(cov_hc1)))
    t_robust = np.where(se_robust > 1e-12, beta / se_robust, 0.0)
    p_robust = [normal_p_value(t) for t in t_robust]

    ci_lower_robust = beta - 1.959964 * se_robust
    ci_upper_robust = beta + 1.959964 * se_robust
    pct_lower_robust = (np.exp(ci_lower_robust) - 1.0) * 100.0
    pct_upper_robust = (np.exp(ci_upper_robust) - 1.0) * 100.0

    # Breusch-Pagan Test for Heteroskedasticity (Auxiliary regression of e_i^2 on X)
    e2 = residuals ** 2
    b_aux = xtx_inv @ (X.T @ e2)
    e2_fitted = X @ b_aux
    rss_bp = float(np.sum((e2 - e2_fitted) ** 2))
    tss_bp = float(np.sum((e2 - np.mean(e2)) ** 2))
    r2_bp = max(0.0, 1.0 - (rss_bp / tss_bp)) if tss_bp > 1e-12 else 0.0
    bp_lm_stat = float(n_obs * r2_bp)
    bp_df = p - 1 if add_intercept else p
    bp_p_value = chi2_p_value(bp_lm_stat, bp_df)

    if df_model > 0 and df_residual > 0 and s2 > 0:
        f_stat = float((mss / df_model) / s2)
        f_pval = f_distribution_p_value(f_stat, df_model, df_residual)
    else:
        f_stat = 0.0
        f_pval = 1.0

    coeff_df = pd.DataFrame(
        {
            "term": col_names,
            "coef": beta,
            "std_error": se_beta,
            "t_stat": t_stats,
            "p_value": p_values,
            "ci_lower_95": ci_lower,
            "ci_upper_95": ci_upper,
            "pct_effect": pct_effect,
            "pct_ci_lower": pct_lower,
            "pct_ci_upper": pct_upper,
            "robust_se": se_robust,
            "robust_t_stat": t_robust,
            "robust_p_value": p_robust,
            "robust_ci_lower_95": ci_lower_robust,
            "robust_ci_upper_95": ci_upper_robust,
            "pct_robust_ci_lower": pct_lower_robust,
            "pct_robust_ci_upper": pct_upper_robust,
        }
    )

    return {
        "coefficients": coeff_df,
        "r_squared": r_squared,
        "adj_r_squared": adj_r_squared,
        "f_statistic": f_stat,
        "f_p_value": f_pval,
        "residual_std_err": residual_se,
        "n_obs": n_obs,
        "df_model": df_model,
        "df_residual": df_residual,
        "residuals": residuals,
        "fitted_values": fitted_vals,
        "design_matrix_cols": col_names,
        "cov_hc1": cov_hc1,
        "breusch_pagan_stat": bp_lm_stat,
        "breusch_pagan_df": bp_df,
        "breusch_pagan_p_value": bp_p_value,
    }


def calculate_vif(
    df: pd.DataFrame,
    x_num_cols: Optional[List[str]] = None,
    x_cat_cols: Optional[List[str]] = None,
    reference_categories: Optional[Dict[str, str]] = None,
) -> pd.DataFrame:
    """Calculates Variance Inflation Factors (VIF) to detect multicollinearity.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset.
    x_num_cols : Optional[List[str]], default None
        Numeric predictors.
    x_cat_cols : Optional[List[str]], default None
        Categorical predictors.
    reference_categories : Optional[Dict[str, str]], default None
        Mapping of categorical variables to reference baseline categories.

    Returns
    -------
    pd.DataFrame
        Table with predictor column names and corresponding VIF values.
    """
    x_num = list(x_num_cols) if x_num_cols else []
    x_cat = list(x_cat_cols) if x_cat_cols else []
    ref_map = reference_categories or {}

    all_req = x_num + x_cat
    clean_df = df[all_req].dropna().copy()
    n_obs = len(clean_df)
    if n_obs == 0:
        raise ValueError("No complete cases available for VIF calculation.")

    design_parts = []
    col_names = []

    for num_col in x_num:
        vals = clean_df[num_col].values.astype(float).reshape(-1, 1)
        design_parts.append(vals)
        col_names.append(num_col)

    for cat_col in x_cat:
        series = clean_df[cat_col].astype(str)
        unique_cats = sorted(series.unique())
        ref = ref_map.get(cat_col)
        ref_cat = (
            ref if (ref is not None and ref in unique_cats) else series.value_counts().index[0]
        )

        for cat in unique_cats:
            if cat == ref_cat:
                continue
            dummy_vals = (series == cat).astype(float).values.reshape(-1, 1)
            design_parts.append(dummy_vals)
            col_names.append(f"{cat_col}_{cat}")

    if not design_parts:
        return pd.DataFrame(columns=["variable", "vif", "risk_level"])

    X = np.hstack(design_parts)
    k = X.shape[1]

    vifs = []
    for j in range(k):
        y_j = X[:, j]
        X_not_j = np.delete(X, j, axis=1)
        X_design = np.hstack([np.ones((n_obs, 1)), X_not_j])

        beta = np.linalg.pinv(X_design) @ y_j
        y_hat = X_design @ beta
        rss = float(np.sum((y_j - y_hat) ** 2))
        tss = float(np.sum((y_j - np.mean(y_j)) ** 2))

        r2 = 1.0 - (rss / tss) if tss > 1e-12 else 0.0
        r2 = max(0.0, min(0.999999, r2))
        vif = 1.0 / (1.0 - r2)
        vifs.append(vif)

    return pd.DataFrame(
        {
            "variable": col_names,
            "vif": vifs,
            "risk_level": [
                "Severe (>10)" if v > 10 else ("Moderate (5-10)" if v > 5 else "Low (<5)")
                for v in vifs
            ],
        }
    )


def compare_groups_continuous(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
) -> Dict[str, Any]:
    """Computes descriptive statistics, one-way ANOVA, and pairwise differences across groups.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset.
    group_col : str
        Categorical grouping column.
    value_col : str
        Continuous measurement column.

    Returns
    -------
    Dict[str, Any]
        Dictionary with group summary statistics, ANOVA F-test, and effect sizes.
    """
    sub_df = df[[group_col, value_col]].dropna().copy()
    sub_df[value_col] = sub_df[value_col].astype(float)
    groups = sorted(sub_df[group_col].unique())

    stats_list = []
    group_arrays = []

    for g in groups:
        vals = sub_df[sub_df[group_col] == g][value_col].values
        n = len(vals)
        if n == 0:
            continue
        mean_val = float(np.mean(vals))
        median_val = float(np.median(vals))
        std_val = float(np.std(vals, ddof=1)) if n > 1 else 0.0
        se_val = std_val / math.sqrt(n) if n > 0 else 0.0
        ci_lower = mean_val - 1.959964 * se_val
        ci_upper = mean_val + 1.959964 * se_val

        group_arrays.append(vals)
        stats_list.append(
            {
                "group": str(g),
                "count": n,
                "mean": mean_val,
                "median": median_val,
                "std": std_val,
                "se": se_val,
                "ci_lower_95": ci_lower,
                "ci_upper_95": ci_upper,
            }
        )

    summary_df = pd.DataFrame(stats_list)

    k = len(group_arrays)
    total_n = sum(len(arr) for arr in group_arrays)
    if k > 1 and total_n > k:
        grand_mean = float(np.mean(np.concatenate(group_arrays)))
        ss_between = float(
            sum(len(arr) * ((np.mean(arr) - grand_mean) ** 2) for arr in group_arrays)
        )
        ss_within = float(sum(np.sum((arr - np.mean(arr)) ** 2) for arr in group_arrays))
        ss_total = ss_between + ss_within
        df_between = k - 1
        df_within = total_n - k
        ms_between = ss_between / df_between
        ms_within = ss_within / df_within if df_within > 0 else 0.0
        if ms_within > 1e-12:
            f_stat = ms_between / ms_within
            p_val = f_distribution_p_value(f_stat, df_between, df_within)
        elif ss_between > 1e-12:
            f_stat = float("inf")
            p_val = 0.0
        else:
            f_stat = 0.0
            p_val = 1.0

        eta_squared = ss_between / ss_total if ss_total > 0 else 0.0
        denom_omega = ss_total + ms_within
        omega_squared = (
            (ss_between - df_between * ms_within) / denom_omega
            if denom_omega > 0 and (ss_between - df_between * ms_within) > 0
            else 0.0
        )
    else:
        f_stat = 0.0
        p_val = 1.0
        df_between = 0
        df_within = 0
        ss_between = 0.0
        ss_within = 0.0
        ss_total = 0.0
        eta_squared = 0.0
        omega_squared = 0.0

    return {
        "summary": summary_df,
        "anova_f_stat": f_stat,
        "anova_p_value": p_val,
        "df_between": df_between,
        "df_within": df_within,
        "ss_between": ss_between,
        "ss_within": ss_within,
        "ss_total": ss_total,
        "eta_squared": eta_squared,
        "omega_squared": omega_squared,
        "total_n": total_n,
    }


# ---------------------------------------------------------------------------
# Multiple Testing Adjustments
# ---------------------------------------------------------------------------


def adjust_p_values(p_values: List[float], method: str = "fdr_bh") -> List[float]:
    """Adjusts p-values for multiple hypothesis testing.

    Parameters
    ----------
    p_values : List[float]
        Unadjusted raw p-values.
    method : str, default 'fdr_bh'
        Adjustment method: 'fdr_bh' (Benjamini-Hochberg) or 'bonferroni'.

    Returns
    -------
    List[float]
        Adjusted p-values, capped at 1.0.
    """
    m = len(p_values)
    if m == 0:
        return []
    if m == 1:
        return [min(1.0, max(0.0, float(p_values[0])))]

    if method.lower() == "bonferroni":
        return [min(1.0, max(0.0, float(p) * m)) for p in p_values]
    elif method.lower() in ["fdr_bh", "bh"]:
        # Benjamini-Hochberg procedure
        indexed = sorted(enumerate(p_values), key=lambda x: x[1])
        adj = [0.0] * m
        # Step-up adjustment
        cum_min = 1.0
        for rank_from_end, (orig_idx, p_val) in enumerate(reversed(indexed)):
            rank = m - rank_from_end
            raw_adj = float(p_val) * m / rank
            cum_min = min(cum_min, raw_adj)
            adj[orig_idx] = min(1.0, max(0.0, cum_min))
        return adj
    else:
        raise ValueError(f"Unknown multiple testing adjustment method: '{method}'.")
