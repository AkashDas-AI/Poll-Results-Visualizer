"""Independent mathematical validation suite for pure-Python statistical engine.

Validates parameter estimates, standard errors, degrees of freedom, confidence
intervals, test statistics, p-values, and effect sizes against independently derived
hand-calculated closed-form analytical benchmarks.

Author: Akash Das
Project: Poll Results Visualizer - Phase 5 Review Corrections
"""

import math
import pandas as pd
import pytest

from src.analysis import (
    normal_cdf,
    normal_p_value,
    chi2_p_value,
    f_distribution_p_value,
    calculate_contingency_and_chi2,
    calculate_odds_ratios,
    fit_ols,
    calculate_vif,
    compare_groups_continuous,
    adjust_p_values,
)


def approx(val, tol=1e-5):
    return pytest.approx(val, abs=tol)


# ---------------------------------------------------------------------------
# 1. Exact Distribution Survival Probabilities
# ---------------------------------------------------------------------------


def test_independent_normal_survival_probabilities():
    """Validate standard normal CDF and two-tailed p-values across central and tail points.

    Analytical benchmark reference values:
    - z = 0.0: CDF = 0.5000000, two-tailed p = 1.0000000
    - z = 1.959964: CDF = 0.9750000, two-tailed p = 0.0500000 (alpha = 0.05)
    - z = 2.575829: CDF = 0.9950000, two-tailed p = 0.0100000 (alpha = 0.01)
    - z = 3.290527: CDF = 0.9995000, two-tailed p = 0.0010000 (alpha = 0.001)
    - z = 3.890592: CDF = 0.9999500, two-tailed p = 0.0001000 (alpha = 0.0001)
    - z = 4.000000: CDF = 0.9999683, two-tailed p = 6.33425e-5
    - z = 5.000000: CDF = 0.9999997, two-tailed p = 5.73303e-7
    """
    assert approx(normal_cdf(0.0), 1e-7) == 0.5
    assert approx(normal_p_value(0.0), 1e-7) == 1.0

    # Alpha critical points
    assert approx(normal_cdf(1.959964), 1e-5) == 0.975
    assert approx(normal_p_value(1.959964), 1e-5) == 0.05

    assert approx(normal_cdf(2.575829), 1e-5) == 0.995
    assert approx(normal_p_value(2.575829), 1e-5) == 0.01

    assert approx(normal_cdf(3.290527), 1e-5) == 0.9995
    assert approx(normal_p_value(3.290527), 1e-5) == 0.001

    assert approx(normal_cdf(3.890592), 1e-5) == 0.99995
    assert approx(normal_p_value(3.890592), 1e-5) == 0.0001

    # Extreme tail points
    assert approx(normal_cdf(4.0), 1e-6) == 0.9999683
    assert approx(normal_p_value(4.0), 1e-6) == 6.33425e-5

    assert approx(normal_cdf(5.0), 1e-7) == 0.9999997
    assert approx(normal_p_value(5.0), 1e-7) == 5.73303e-7


def test_independent_chi2_survival_probabilities():
    """Validate Chi-squared survival probabilities across multiple df and extreme tails.

    Tests df = 1, 2, 4, 8, 19 against analytical critical values:
    - df = 1: 3.841459 (p = 0.05), 6.634897 (p = 0.01), 10.827566 (p = 0.001)
    - df = 2: exact survival function S(x; 2) = exp(-x/2)
      x = -2 * ln(p) -> exact p for 0.05, 0.01, 0.001, 0.0001
    - df = 4: 9.487729 (p = 0.05), 13.276704 (p = 0.01), 18.466827 (p = 0.001), 23.51269 (p = 0.0001)
      and chi2 = 30.1175 (RQ1 collapsed 5x2 table -> p = 4.632e-6)
    - df = 8: 15.507313 (p = 0.05), 20.090235 (p = 0.01), 26.124482 (p = 0.001), 31.82761 (p = 0.0001)
      and chi2 = 38.3898 (RQ1 global 5x3 table -> p = 6.377e-6)
    - df = 19: 30.143527 (p = 0.05), 36.190869 (p = 0.01), 43.820197 (p = 0.001), 50.84097 (p = 0.0001)
    """
    # df = 1
    assert approx(chi2_p_value(3.8414588, 1), 1e-5) == 0.05
    assert approx(chi2_p_value(6.634897, 1), 1e-5) == 0.01
    assert approx(chi2_p_value(10.827566, 1), 1e-5) == 0.001

    # df = 2 (exact analytical closed-form: S(x) = exp(-x/2))
    for target_p in [0.05, 0.01, 0.001, 0.0001]:
        x_val = -2.0 * math.log(target_p)
        assert approx(chi2_p_value(x_val, 2), 1e-6) == target_p

    # df = 4
    assert approx(chi2_p_value(9.487729, 4), 1e-5) == 0.05
    assert approx(chi2_p_value(13.276704, 4), 1e-5) == 0.01
    assert approx(chi2_p_value(18.466827, 4), 1e-5) == 0.001
    assert approx(chi2_p_value(23.512690, 4), 1e-5) == 0.0001
    # Collapsed Seniority 5x2 contingency test statistic
    assert approx(chi2_p_value(30.11753, 4), 1e-7) == 4.63212e-06

    # df = 8
    assert approx(chi2_p_value(15.507313, 8), 1e-5) == 0.05
    assert approx(chi2_p_value(20.090235, 8), 1e-5) == 0.01
    assert approx(chi2_p_value(26.124482, 8), 1e-5) == 0.001
    assert approx(chi2_p_value(31.827610, 8), 1e-5) == 0.0001
    # Global Seniority 5x3 contingency test statistic
    assert approx(chi2_p_value(38.38980, 8), 1e-7) == 6.37709e-06

    # df = 19
    assert approx(chi2_p_value(30.143527, 19), 1e-5) == 0.05
    assert approx(chi2_p_value(36.190869, 19), 1e-5) == 0.01
    assert approx(chi2_p_value(43.820197, 19), 1e-5) == 0.001
    assert approx(chi2_p_value(50.840970, 19), 1e-4) == 0.0001

    # Boundary conditions
    assert chi2_p_value(0.0, 1) == 1.0
    assert chi2_p_value(-5.0, 2) == 1.0


# ---------------------------------------------------------------------------
# 2. Linear OLS Regression & White HC1 Closed-Form Benchmark
# ---------------------------------------------------------------------------


def test_independent_ols_and_white_hc1_closed_form_benchmark():
    """Validate fit_ols and White HC1 covariance matrix against hand calculations.

    Textbook 5-point dataset:
    (x, y) = [(1, 2), (2, 3), (3, 5), (4, 4), (5, 6)]

    Exact analytical derivation:
    Design matrix X = [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5]], y = [2, 3, 5, 4, 6]
    n = 5, p = 2, df_residual = 3, df_model = 1
    X^T X = [[5, 15], [15, 55]]
    det(X^T X) = 5(55) - 15(15) = 275 - 225 = 50
    (X^T X)^(-1) = (1/50) * [[55, -15], [-15, 5]] = [[1.1, -0.3], [-0.3, 0.1]]

    X^T y = [20, 69]^T
    beta_hat = [[1.1, -0.3], [-0.3, 0.1]] * [20, 69]^T = [1.3, 0.9]^T
    y_hat = [2.2, 3.1, 4.0, 4.9, 5.8]^T
    residuals e = [-0.2, -0.1, 1.0, -0.9, 0.2]^T
    e^2 = [0.04, 0.01, 1.00, 0.81, 0.04]^T
    RSS = sum(e_i^2) = 1.90
    TSS = sum((y - y_bar)^2) = 10.00
    R^2 = 1 - 1.9/10.0 = 0.81
    s^2 = 1.9 / 3 = 0.6333333333
    s = sqrt(s^2) = 0.79582243
    Conventional SE(beta_1) = sqrt(0.63333333 * 0.1) = sqrt(0.06333333) = 0.25166115
    Conventional SE(beta_0) = sqrt(0.63333333 * 1.1) = sqrt(0.69666667) = 0.83466560
    t(beta_1) = 0.9 / 0.25166115 = 3.576237
    F = (8.1 / 1) / (1.9 / 3) = 12.78947368

    White HC0 Meat Matrix:
    S_0 = X^T diag(e^2) X = [[1.90, 6.50], [6.50, 23.04]]
    V_HC0 = (X^T X)^(-1) S_0 (X^T X)^(-1) = [[0.0826, -0.0182], [-0.0182, 0.0114]]

    White HC1 Degrees-of-Freedom Correction:
    Scale factor = n / (n - p) = 5 / 3
    V_HC1 = (5/3) * V_HC0 = [[0.13766667, -0.03033333], [-0.03033333, 0.01900000]]
    SE_HC1(beta_0) = sqrt(0.13766667) = 0.37103459
    SE_HC1(beta_1) = sqrt(0.01900000) = 0.13784049
    t_HC1(beta_1) = 0.9 / 0.13784049 = 6.529286
    """
    df_toy = pd.DataFrame({
        "x": [1.0, 2.0, 3.0, 4.0, 5.0],
        "y": [2.0, 3.0, 5.0, 4.0, 6.0],
    })

    model = fit_ols(df_toy, y_col="y", x_num_cols=["x"], add_intercept=True)

    assert model["n_obs"] == 5
    assert model["df_model"] == 1
    assert model["df_residual"] == 3
    assert approx(model["r_squared"], 1e-6) == 0.81
    assert approx(model["residual_std_err"], 1e-6) == 0.7958224
    assert approx(model["f_statistic"], 1e-4) == 12.78947

    coefs = model["coefficients"].set_index("term")

    # Point estimates
    assert approx(coefs.loc["x", "coef"], 1e-6) == 0.9
    assert approx(coefs.loc["Intercept", "coef"], 1e-6) == 1.3

    # Conventional OLS standard errors and t-stats
    assert approx(coefs.loc["x", "std_error"], 1e-6) == 0.25166115
    assert approx(coefs.loc["Intercept", "std_error"], 1e-6) == 0.83466560
    assert approx(coefs.loc["x", "t_stat"], 1e-4) == 3.576237

    # White HC1 robust covariance matrix matching
    cov_hc1 = model["cov_hc1"]
    assert approx(cov_hc1[0, 0], 1e-6) == 0.13766667
    assert approx(cov_hc1[0, 1], 1e-6) == -0.03033333
    assert approx(cov_hc1[1, 0], 1e-6) == -0.03033333
    assert approx(cov_hc1[1, 1], 1e-6) == 0.01900000

    # White HC1 robust standard errors and t-stats
    assert approx(coefs.loc["Intercept", "robust_se"], 1e-6) == 0.37103459
    assert approx(coefs.loc["x", "robust_se"], 1e-6) == 0.13784049
    assert approx(coefs.loc["x", "robust_t_stat"], 1e-4) == 6.529286

    # Breusch-Pagan diagnostic
    assert "breusch_pagan_stat" in model
    assert model["breusch_pagan_df"] == 1


# ---------------------------------------------------------------------------
# 3. 2x2 Contingency Table and Odds Ratio Closed-Form Benchmark
# ---------------------------------------------------------------------------


def test_independent_contingency_and_odds_ratio_benchmark():
    """Validate 2x2 contingency table, Chi2, and Odds Ratio against exact hand calculations.

    Table:
                   Case (Outcome=1)    Non-Case (Outcome=0)    Total
    Exposed (E=1)         40                    60              100
    Unexposed (E=0)       20                    80              100
    Total                 60                   140              200

    Exact closed-form values:
    - Expected: E_11 = 30.0, E_12 = 70.0, E_21 = 30.0, E_22 = 70.0
    - Chi2 = (10)^2/30 + (-10)^2/70 + (-10)^2/30 + (10)^2/70 = 200/30 + 200/70 = 9.52381
    - df = (2-1)*(2-1) = 1
    - Cramer's V = sqrt(9.52381 / 200) = 0.218218
    - OR = (40 * 80) / (60 * 20) = 3200 / 1200 = 8/3 = 2.666667
    - SE(ln OR) = sqrt(1/40 + 1/60 + 1/20 + 1/80) = sqrt(0.10416667) = 0.3227486
    - ln(OR) = ln(8/3) = 0.9808293
    - 95% Wald CI: exp(0.9808293 +- 1.959964 * 0.3227486) = [1.4150, 5.0257]
    - z-score = 0.9808293 / 0.3227486 = 3.039
    """
    data = (
        [{"Exposure": "Exposed", "Outcome": 1}] * 40
        + [{"Exposure": "Exposed", "Outcome": 0}] * 60
        + [{"Exposure": "Unexposed", "Outcome": 1}] * 20
        + [{"Exposure": "Unexposed", "Outcome": 0}] * 80
    )
    df_ct = pd.DataFrame(data)

    c2_res = calculate_contingency_and_chi2(df_ct, "Exposure", "Outcome")

    assert c2_res["total_n"] == 200
    assert c2_res["df"] == 1
    assert approx(c2_res["expected"].loc["Exposed", 1], 1e-6) == 30.0
    assert approx(c2_res["expected"].loc["Exposed", 0], 1e-6) == 70.0
    assert approx(c2_res["chi2"], 1e-4) == 9.5238
    assert approx(c2_res["cramers_v"], 1e-4) == 0.2182
    assert c2_res["p_value"] < 0.005

    or_res = calculate_odds_ratios(df_ct, "Exposure", "Outcome", positive_outcome=1, reference_exposure="Unexposed")
    exposed_row = or_res[or_res["category"] == "Exposed"].iloc[0]

    assert approx(exposed_row["odds_ratio"], 1e-4) == 2.6667
    assert approx(exposed_row["ci_lower"], 1e-3) == 1.4166
    assert approx(exposed_row["ci_upper"], 1e-3) == 5.020
    assert approx(exposed_row["z_score"], 1e-2) == 3.04
    assert exposed_row["p_value"] < 0.005


# ---------------------------------------------------------------------------
# 4. One-Way ANOVA and Effect Sizes (eta^2, omega^2) Benchmark
# ---------------------------------------------------------------------------


def test_independent_anova_and_effect_sizes_benchmark():
    """Validate one-way ANOVA, eta^2, and omega^2 against exact hand calculations.

    Groups:
    - Group 1: [4, 5, 6] (mean = 5, n = 3)
    - Group 2: [7, 8, 9] (mean = 8, n = 3)
    - Group 3: [10, 11, 12] (mean = 11, n = 3)
    Total N = 9, k = 3, Grand mean = 8.0

    Analytical values:
    - SS_between = 3(5-8)^2 + 3(8-8)^2 + 3(11-8)^2 = 3(9) + 0 + 3(9) = 54.0
    - SS_within = (1+0+1) + (1+0+1) + (1+0+1) = 6.0
    - SS_total = 54.0 + 6.0 = 60.0
    - df_between = 2, df_within = 6
    - MS_between = 54 / 2 = 27.0
    - MS_within = 6 / 6 = 1.0
    - F = 27.0 / 1.0 = 27.0
    - eta^2 = 54 / 60 = 0.90
    - omega^2 = (54 - 2(1)) / (60 + 1) = 52 / 61 = 0.852459
    """
    df_anova = pd.DataFrame({
        "group": ["G1"] * 3 + ["G2"] * 3 + ["G3"] * 3,
        "score": [4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0],
    })

    res = compare_groups_continuous(df_anova, "group", "score")

    assert res["total_n"] == 9
    assert res["df_between"] == 2
    assert res["df_within"] == 6
    assert approx(res["ss_between"], 1e-6) == 54.0
    assert approx(res["ss_within"], 1e-6) == 6.0
    assert approx(res["ss_total"], 1e-6) == 60.0
    assert approx(res["anova_f_stat"], 1e-6) == 27.0
    assert approx(res["eta_squared"], 1e-6) == 0.90
    assert approx(res["omega_squared"], 1e-5) == 52.0 / 61.0
    assert res["anova_p_value"] < 0.005


# ---------------------------------------------------------------------------
# 5. Multiple Testing Adjustment (Benjamini-Hochberg & Bonferroni) Benchmark
# ---------------------------------------------------------------------------


def test_independent_multiple_testing_adjustments():
    """Validate adjust_p_values against theoretical step-up adjustments.

    Given raw p-values: [0.001, 0.01, 0.03, 0.05] (m = 4)
    - Bonferroni: [0.004, 0.04, 0.12, 0.20]
    - Benjamini-Hochberg (BH):
      - Rank 4: 0.05 * 4 / 4 = 0.05
      - Rank 3: 0.03 * 4 / 3 = 0.04
      - Rank 2: 0.01 * 4 / 2 = 0.02
      - Rank 1: 0.001 * 4 / 1 = 0.004
      Monotonic adjustments: [0.004, 0.02, 0.04, 0.05]
    """
    raw_p = [0.001, 0.01, 0.03, 0.05]

    bonf = adjust_p_values(raw_p, method="bonferroni")
    assert approx(bonf[0], 1e-6) == 0.004
    assert approx(bonf[1], 1e-6) == 0.04
    assert approx(bonf[2], 1e-6) == 0.12
    assert approx(bonf[3], 1e-6) == 0.20

    bh = adjust_p_values(raw_p, method="fdr_bh")
    assert approx(bh[0], 1e-6) == 0.004
    assert approx(bh[1], 1e-6) == 0.02
    assert approx(bh[2], 1e-6) == 0.04
    assert approx(bh[3], 1e-6) == 0.05


# ---------------------------------------------------------------------------
# 6. Variance Inflation Factor (VIF) Closed-Form Benchmark
# ---------------------------------------------------------------------------


def test_independent_vif_closed_form_benchmark():
    """Validate calculate_vif against an independent multi-column predictor matrix.

    Predictor Matrix (3 explanatory predictors, n = 5 observations):
      x1 = [3.0, 5.0, 8.0, 9.0, 15.0]
      x2 = [1.0, 2.0, 3.0, 4.0, 5.0]
      x3 = [0.0, 1.0, 0.0, 1.0, 2.0]

    This is completely independent of any outcome-on-predictor regression.

    Independent Mathematical Derivation of Auxiliary Regressions:

    1. Auxiliary Regression for x2 regressed on (x1, x3) with intercept:
       x_{2, i} = alpha_0 + alpha_1 * x_{1, i} + alpha_3 * x_{3, i} + u_{2, i}
       Normal equations yield exact coefficients:
         alpha_0 = 1/3, alpha_1 = 1/3, alpha_3 = 0.0
       Fitted values:
         hat{x}_{2, i} = (1 + x_{1, i}) / 3 = [4/3, 2, 3, 10/3, 16/3]^T
       Residuals:
         e_i = x_{2, i} - hat{x}_{2, i} = [-1/3, 0, 0, 2/3, -1/3]^T
       Residual Sum of Squares (RSS):
         RSS = (-1/3)^2 + 0^2 + 0^2 + (2/3)^2 + (-1/3)^2 = 1/9 + 4/9 + 1/9 = 6/9 = 2/3
       Mean of x2 = 3.0. Total Sum of Squares (TSS):
         TSS = sum((x_{2, i} - 3)^2) = (-2)^2 + (-1)^2 + 0^2 + 1^2 + 2^2 = 10
       Auxiliary R^2:
         R_2^2 = 1 - (RSS / TSS) = 1 - ((2/3) / 10) = 1 - 1/15 = 14/15 approx 0.9333333333
       Analytical Expected VIF:
         VIF(x_2) = 1 / (1 - R_2^2) = 1 / (1/15) = 15.00000000 (Exact Integer!)

    2. Auxiliary Regression for x1 regressed on (x2, x3) with intercept:
       Normal equations yield: hat{x}_1 = -2/15 + (38/15) * x2 + (2/3) * x3
       RSS = 76/15 approx 5.066667, TSS = 84.0
       Auxiliary R_1^2 = 1 - ((76 / 15) / 84) = 1 - (19 / 315) = 296 / 315 approx 0.93968254
       Analytical Expected VIF:
         VIF(x_1) = 1 / (19 / 315) = 315 / 19 approx 16.57894737

    3. Auxiliary Regression for x3 regressed on (x1, x2) with intercept:
       Normal equations yield: hat{x}_3 = -12/35 + (5/35) * x1 + 0 * x2
       RSS = 38/35 approx 1.085714, TSS = 14/5 = 2.8
       Auxiliary R_3^2 = 1 - ((38 / 35) / (14 / 5)) = 1 - (19 / 49) = 30 / 49 approx 0.61224490
       Analytical Expected VIF:
         VIF(x_3) = 1 / (19 / 49) = 49 / 19 approx 2.57894737
    """
    df_vif = pd.DataFrame({
        "x1": [3.0, 5.0, 8.0, 9.0, 15.0],
        "x2": [1.0, 2.0, 3.0, 4.0, 5.0],
        "x3": [0.0, 1.0, 0.0, 1.0, 2.0],
    })

    vif_res = calculate_vif(df_vif, x_num_cols=["x1", "x2", "x3"]).set_index("variable")

    # Assert exact analytical values
    assert approx(vif_res.loc["x2", "vif"], 1e-6) == 15.0
    assert approx(vif_res.loc["x1", "vif"], 1e-6) == 315.0 / 19.0
    assert approx(vif_res.loc["x3", "vif"], 1e-6) == 49.0 / 19.0

    # Risk level classification verification
    assert vif_res.loc["x2", "risk_level"] == "Severe (>10)"
    assert vif_res.loc["x1", "risk_level"] == "Severe (>10)"
    assert vif_res.loc["x3", "risk_level"] == "Low (<5)"

    # F-distribution p-value for large df
    f_p = f_distribution_p_value(27.0, 2, 600)
    assert f_p < 1e-5
    assert f_distribution_p_value(-1.0, 2, 10) == 1.0
