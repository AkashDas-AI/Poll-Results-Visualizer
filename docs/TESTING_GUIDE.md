# Testing Guide: Poll Results Visualizer

**Project Name:** Poll Results Visualizer  
**Author:** Akash Das  
**Current Milestone:** Phase 8 - Final Project Polish, GitHub Preparation and Publication  
**Primary Dataset:** Stack Overflow Annual Developer Survey 2025  
**Quality Assurance Stack:** pytest (>= 8.0.0), flake8 (>= 7.0.0), GitHub Actions CI  
**Test Suite Status:** 93 Passed out of 93 Tests (100% Pass Rate) | 0 Flake8 Linting Errors  

---

## 1. Quality Assurance Architecture and Philosophy

The testing architecture of **Poll Results Visualizer** is designed to guarantee high reliability, numerical reproducibility, econometric validity, and sub-second execution speed across heterogeneous environments.

```
+-----------------------------------------------------------------------------------+
|                                  TEST PYRAMID                                     |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|                              / \                                                  |
|                             /   \                                                 |
|                            /  E2E \              Streamlit Live Health Checks    |
|                           / Health \             (HTTP 200, /_stcore/health)      |
|                          /----------\                                             |
|                         / Component  \           Plotly Figures, KPI Metric Cards |
|                        /  & UI Tests  \          Dual-Percentage Visuals, Funnel  |
|                       /----------------\                                          |
|                      / Integration Tests\        Phase 5 Models, Mincer Wage Reg, |
|                     / & Closed-Form Proof\       White HC1 Covariance, ANOVA, VIF |
|                    /----------------------\                                       |
|                   /    Unit Test Suite     \     Data Loaders, Schema Validation, |
|                  / (Cleaning, Parsing, KPIs)\    Experience Classifier, Imputation|
|                 +----------------------------+                                    |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

### Core Testing Principles

1. **Hermetic and Pure-Python Execution:**
   - Numerical calculations (OLS, White HC1 covariance matrix, Pearson chi-square, one-way ANOVA, VIF) are implemented in pure Python and NumPy.
   - Tests execute with zero reliance on external compiled econometric binaries or external network services.

2. **CI/CD Decoupling via Conditional Skips:**
   - The processed Apache Parquet dataset (`data/processed/survey_results_cleaned.parquet`, 9.8 MB) is excluded from the public git repository for size efficiency.
   - Tests that depend on the on-disk Parquet artifact utilize a clean `@require_parquet` decorator:
     ```python
     HAS_CLEANED_PARQUET = Path("data/processed/survey_results_cleaned.parquet").exists()
     require_parquet = pytest.mark.skipif(
         not HAS_CLEANED_PARQUET,
         reason="Cleaned survey dataset not present on disk (expected in fresh git clone)",
     )
     ```
   - All synthetic and mock-based unit tests execute independently, ensuring that GitHub Actions CI runs with a 100% pass rate on fresh repository clones without requiring external data downloads.

3. **Closed-Form Mathematical Verification:**
   - Statistical algorithms are verified not only against expected internal behavior, but against independent closed-form mathematical equations and known statistical benchmark datasets (e.g. standard normal CDF, chi-square upper-tail survival, auxiliary $R^2$ VIF definitions).

4. **Zero-Tolerance Static Analysis:**
   - The codebase enforces strict PEP 8 conformance via `flake8`. Zero errors and zero warnings are permitted across application code, analytical libraries, and test suites.

---

## 2. Test Suite Directory Structure and Inventory

The automated test suite comprises **93 unit and integration tests** organized across 10 specialized test modules in the `tests/` directory:

```
tests/
|-- __init__.py                                 # Package marker
|-- test_analysis.py                            # 14 tests: Statistical engine and KPIs
|-- test_dashboard_components.py                # 22 tests: Plotly figures, filters, and UI logic
|-- test_data_cleaning.py                       #  5 tests: Generic survey data cleaning pipeline
|-- test_data_loader.py                         #  4 tests: CSV loading, encodings, and mappings
|-- test_data_validation.py                     #  5 tests: Schema validation and anomaly detection
|-- test_export.py                              #  2 tests: CSV disk export and in-memory byte serialization
|-- test_insights.py                            #  4 tests: Automated narrative generation and Phase 7 integrity
|-- test_stackoverflow_2025.py                  # 19 tests: SO 2025 adapter, multi-select, and currencies
|-- test_stackoverflow_cleaning.py              # 11 tests: Experience classification, cleaning, and Parquet IO
`-- test_statistical_engine_validation.py       #  7 tests: Independent closed-form mathematical proofs
```

---

## 3. Comprehensive Module Breakdown

### 3.1. `tests/test_analysis.py` (14 Tests)
Validates core exploratory data analysis routines, exploratory cross-tabulations, multivariable linear regressions, collinearity diagnostics, and distribution helpers.

| Test Function | Verification Scope | Assertions / Invariants |
|---|---|---|
| `test_calculate_kpis_distinguishes_unique_respondents` | Evaluates total responses vs unique respondents when multiple questions are answered. | Ensures `total_respondents` matches unique `respondent_id` count, not row count. |
| `test_get_response_distribution` | Validates frequency counts and percentage share calculations for categorical questions. | Sum of percentages equals 100.0% within floating-point tolerance. |
| `test_get_segment_comparison` | Verifies within-segment normalization across demographic cohorts. | Group-level percentage sums equal 100.0% within each demographic slice. |
| `test_get_trend_over_time` | Verifies daily aggregation logic for temporal poll tracking. | Correct daily counts and date formatting. |
| `test_analysis_empty_dataframe_safety` | Edge case validation for empty DataFrame inputs. | Returns structured empty DataFrames/dictionaries without unhandled exceptions. |
| `test_statistical_distributions_exact_prob` | Evaluates standard normal CDF and survival probability implementations. | Matches known values ($z=0 \to p=0.5, z=1.96 \to p \approx 0.025$). |
| `test_calculate_contingency_and_chi2_synthetic` | Tests Pearson Chi-Square test of independence and Cramér's V on synthetic $2 \times 2$ table. | Matches analytical $\chi^2$ and degrees of freedom ($df = 1$). |
| `test_calculate_contingency_errors` | Input validation for contingency analysis (1D data, non-existent columns). | Raises descriptive `ValueError` upon malformed column references. |
| `test_calculate_odds_ratios` | Verifies crude cross-product ratio calculation and Woolf log-standard error confidence intervals. | Exact match to $(ad)/(bc)$ cross-multiplication. |
| `test_fit_ols_linear_model` | Verifies multivariable OLS regression, $R^2$, and White HC1 heteroskedasticity-robust standard errors. | Estimates recover known synthetic regression parameters $(\beta_0, \beta_1)$. |
| `test_fit_ols_with_categorical_predictors` | Validates one-hot dummy variable generation with reference category omission. | Matrix rank matches $k - 1$ degrees of freedom to avoid perfect collinearity. |
| `test_fit_ols_error_cases` | Evaluates collinearity handling, zero variance columns, and singular matrices. | Raises informative errors when $(X^TX)$ is non-invertible. |
| `test_calculate_vif` | Evaluates Variance Inflation Factor calculation using auxiliary regressions. | Correctly identifies collinear variables ($\text{VIF} > 5.0$). |
| `test_compare_groups_continuous` | Tests one-way ANOVA $F$-test and omnibus effect size decomposition ($\eta^2, \omega^2$). | Matches between-group and within-group sum of squares decomposition. |

---

### 3.2. `tests/test_dashboard_components.py` (22 Tests)
Validates Streamlit visual components, Plotly chart generators, input filter logic, and reconciliation against approved Phase 5/6 statistical findings.

| Test Function | Verification Scope | Assertions / Invariants |
|---|---|---|
| `test_plot_distribution_bar` | Generates Plotly vertical bar charts with data labels and annotations. | Returns `go.Figure`, layout contains title, trace type is `bar`. |
| `test_plot_distribution_bar_empty` | Fallback behavior when plotting empty or null distributions. | Returns graceful `go.Figure` with annotation stating "No data available". |
| `test_plot_distribution_pie` | Generates Plotly donut/pie charts with custom slice colors. | Figure contains `pie` trace with percentage values. |
| `test_plot_distribution_pie_empty` | Fallback behavior for empty pie charts. | Returns graceful empty figure placeholder. |
| `test_plot_segment_breakdown_bar` | Generates grouped bar charts for cross-demographic comparisons. | Multi-trace bar chart grouped by segment category. |
| `test_plot_trend_line` | Generates temporal line charts with markers. | Trace type is `scatter` with `mode='lines+markers'`. |
| `test_plot_horizontal_bar_with_denominators` | Verifies dual-percentage multi-select horizontal bar charts. | Formats annotations showing both $\%$ of respondents and $\%$ of selections. |
| `test_plot_technology_comparison_bar` | Generates paired Current vs Desired technology adoption bars. | Contains 2 traces: Current (`#3B82F6`) and Desired (`#22C55E`). |
| `test_plot_compensation_box` | Generates salary distribution box plots with quartile annotations. | Trace type is `box`, y-axis formatted in thousands of USD. |
| `test_plot_missingness_ranking_bar` | Generates survey missingness ranking bars sorted descending. | Bars sorted by missingness percentage; hover displays $N_{\text{missing}}$. |
| `test_plot_sample_flow_funnel` | Generates 4-stage sample flow funnel from raw extract to complete cases. | Stages match $49,191 \to 49,009 \to 23,947 \to 22,769$. |
| `test_experience_brackets_slicing` | Validates standard 5-cohort professional experience bracket categorization. | Assigns correct bracket: `<2 years`, `2-5 years`, `6-10 years`, `11-20 years`, `21+ years`. |
| `test_compensation_trimming_slicing` | Validates trimmed sample boundary filter ($\$1,000 \le \text{Comp} \le \$2,000,000$). | Excludes non-positive records and extreme hyper-outliers. |
| `test_get_survey_dataset_loads_canonical_parquet` | Validates loading and schema conformance of cleaned Parquet. | Rows = $49,191$, columns $\ge 170$, `ResponseId` is primary key. |
| `test_get_survey_overview_kpis` | Verifies executive dashboard KPIs from Parquet dataset. | Raw count = $49,191$, Official base = $49,009$, Countries = $177$, AI adoption $= 78.50\%$. |
| `test_age_distribution_exact_counts_and_percentages` | Validates age distribution counts and percentages against Phase 6 specs. | Complete cases match exact frequency counts across all 8 age bins. |
| `test_technology_exact_respondent_denominators` | Verifies that technology adoption percentages use $N_{\text{answered}}$ as denominator. | Denominator strictly equals respondents answering the question ($N=48,341$). |
| `test_paired_technology_sample_size` | Validates paired Current vs Desired technology sample boundary. | Exact sample size matches $N = 27,079$ complete cases. |
| `test_remotework_missingness_approved_wording` | Audits documentation and UI strings for approved missingness interpretation. | Prohibits unsupported causal claims (e.g. "routed past", "branch rule proof"). |
| `test_cohort_filtering_preserves_valid_denominators` | Verifies that UI filter selections recalculate active $N_{\text{answered}}$ denominators. | Denominators update dynamically without dividing by full sample size. |
| `test_remotework_contingency_table_exact_reconciliation` | Reconciles $6 \times 2$ RemoteWork vs MainBranch contingency table. | Answered sum $= 33,780$, Missing sum $= 15,411$, Grand total $= 49,191$. |
| `test_remotework_compensation_model_c_reconciliation` | Validates Model C remote wage regression coefficients against Phase 5 truth. | Remote coefficient $\hat{\beta} = +0.267353$ ($+30.65\%$, $t = 11.517, p < 10^{-15}$). |

---

### 3.3. `tests/test_data_cleaning.py` (5 Tests)
Validates generic tabular data cleaning, non-mutating transformations, and edge cases.

| Test Function | Verification Scope | Assertions / Invariants |
|---|---|---|
| `test_clean_poll_data_does_not_mutate_original` | Verifies that the cleaning function returns a deep copy without mutating input DataFrame. | Input DataFrame values and column references remain identical before and after call. |
| `test_clean_poll_data_imputes_unknown_segment` | Tests imputation of null demographic segments. | Missing categorical segment values are replaced with `'Unknown'`. |
| `test_clean_poll_data_deduplication_keeps_latest` | Tests deterministic deduplication by `(respondent_id, question_id)` sorting by date. | Retains latest response (`keep='last'`) when multiple records exist. |
| `test_clean_poll_data_drops_empty_mandatory_fields` | Tests removal of records with null or blank mandatory fields. | Drops rows where `respondent_id`, `question_id`, or `response` is null/empty string. |
| `test_clean_poll_data_empty_dataframe` | Verifies safety when passing an empty DataFrame. | Returns an empty DataFrame with identical schema without throwing errors. |

---

### 3.4. `tests/test_data_loader.py` (4 Tests)
Validates file ingestion resilience, fallback character encodings, and column mapping dictionaries.

| Test Function | Verification Scope | Assertions / Invariants |
|---|---|---|
| `test_load_sample_data_success` | Ingests baseline sample poll dataset. | Returns non-empty DataFrame with expected baseline schema. |
| `test_load_nonexistent_file_raises_error` | Error handling when target file path does not exist. | Raises `FileNotFoundError` with clear diagnostic path. |
| `test_load_empty_file_raises_error` | Error handling when target file is zero bytes. | Raises `ValueError` indicating file contains no data. |
| `test_load_column_mapping` | Verifies column renaming dictionary logic for schema normalization. | Maps legacy column names to standardized canonical schema names. |

---

### 3.5. `tests/test_data_validation.py` (5 Tests)
Validates schema enforcement, anomaly auditing, and type safety.

| Test Function | Verification Scope | Assertions / Invariants |
|---|---|---|
| `test_validate_schema_valid` | Validates compliant DataFrame against required schema columns. | Returns `is_valid=True` and empty missing column list. |
| `test_validate_schema_missing_columns` | Detects absence of mandatory schema columns. | Returns `is_valid=False` and lists all missing attribute names. |
| `test_validate_schema_non_dataframe` | Type check enforcement for non-pandas inputs (lists, dicts, strings). | Raises `TypeError` with explicit input type information. |
| `test_validate_poll_data_anomalies` | Audits duplicate keys, future timestamps, and invalid categorical entries. | Returns dictionary reporting anomaly counts and row indices. |
| `test_validate_poll_data_empty_dataframe` | Validates schema conformance of an empty DataFrame. | Conforms to schema if required column headers are present. |

---

### 3.6. `tests/test_export.py` (2 Tests)
Validates data serialization, disk persistence, and UI in-memory byte generation.

| Test Function | Verification Scope | Assertions / Invariants |
|---|---|---|
| `test_export_dataframe_to_csv` | Exports DataFrame to a physical file path on disk. | Creates target file; contents match DataFrame records. |
| `test_get_csv_download_bytes` | Serializes DataFrame into UTF-8 encoded bytes for `st.download_button`. | Returns `bytes` instance readable by `pd.read_csv(io.BytesIO(bytes))`. |

---

### 3.7. `tests/test_insights.py` (4 Tests)
Validates automated descriptive narrative generators and ensures non-causal language and Phase 7 numerical synchronization.

| Test Function | Verification Scope | Assertions / Invariants |
|---|---|---|
| `test_generate_question_insights_content` | Generates descriptive analytical narratives for single-select questions. | Narrative includes top answer, percentage share, and valid sample size. |
| `test_generate_question_insights_empty` | Handles empty response inputs gracefully. | Returns safe fallback narrative without KeyError. |
| `test_generate_segment_insights` | Generates non-causal demographic comparison summaries. | Contains explicit disclaimer that observed cohort differences do not imply causation. |
| `test_phase7_reporting_deliverables_integrity` | Cryptographic and numerical verification of Phase 7 reporting package. | Asserts exact presence of: $N=30,780$, $\chi^2=38.3898$, Rust $+0.1203$ / $+12.79\%$, ANOVA $F=11.6172$, $\eta^2=0.002439$. |

---

### 3.8. `tests/test_stackoverflow_2025.py` (19 Tests)
Validates Stack Overflow 2025 domain adapter routines, multi-select semicolon string normalization, currency conversion, and population accounting.

| Test Function | Verification Scope | Assertions / Invariants |
|---|---|---|
| `test_load_survey_data_missing_file_raises_error` | Ensures survey loader raises `FileNotFoundError` if CSV does not exist. | Correctly triggers file-not-found exception. |
| `test_load_survey_data_missing_id_col` | Audits required `ResponseId` identifier. | Raises `ValueError` if identifier column is missing from CSV header. |
| `test_resolve_file_path_finds_first_existing` | Evaluates file resolution helper across multiple candidate paths. | Returns first valid on-disk path in prioritized search order. |
| `test_get_question_text` | Looks up official survey question phrasing from `survey_results_schema.csv`. | Returns exact question string (e.g. "Which country do you currently reside in?"). |
| `test_analyze_single_select` | Aggregates single-select column distributions. | Returns DataFrame sorted descending by response count; computes exact percentages. |
| `test_analyze_single_select_empty_or_missing_col` | Resilience against missing or all-null survey columns. | Returns structured empty DataFrame with correct column types. |
| `test_analyze_multi_select` | Splits semicolon-delimited multi-select entries (`Python;SQL;Bash`). | Aggregates distinct technology frequencies; calculates dual percentages. |
| `test_analyze_multi_select_empty` | Evaluates multi-select processing on all-null series. | Returns empty DataFrame without raising string splitting exceptions. |
| `test_cross_tabulate_single` | Calculates bivariate cross-tabulation table with row/column totals. | Marginals match independent univariate frequency sums. |
| `test_get_compensation_summary` | Calculates parametric and non-parametric salary summary metrics. | Computes mean, standard deviation, median, IQR, min, max, and sample size. |
| `test_get_survey_kpis` | Verifies high-level survey population KPI dictionary. | Returns correct dictionary keys and positive numeric counts. |
| `test_compensation_summary_distinguishes_answered_and_official` | Verifies reporting of both $N_{\text{answered}}$ and $N_{\text{official}}$ denominators. | Explicitly distinguishes 23,947 compensation respondents from 49,009 official base. |
| `test_population_constants_integrity` | Verifies core survey constants against official published boundaries. | Raw $= 49,191$, Official $= 49,009$, Qualified filter boundary $= 182$ rows. |
| `test_convert_local_compensation_to_usd` | Validates local currency multiplication by Stack Overflow exchange rate factors. | Multiplies `CompTotal` by `CurrencySymbol` exchange rate accurately. |
| `test_convert_local_compensation_unconvertible_or_missing` | Evaluates handling of unconvertible or missing local compensation values. | Assigns `NaN` without corrupting valid numeric conversions. |
| `test_build_poll_adapter_table_has_no_fabricated_dates` | Verifies that adapted survey tabular view does not synthesize artificial dates. | Date column is omitted or marked null to preserve cross-sectional nature. |
| `test_get_compensation_summary_untrimmed` | Calculates summary statistics on raw untrimmed compensation ($N=23,947$). | Preserves full sample distribution including extreme values. |
| `test_country_compensation_reconciliation_exhaustive` | Reconciles compensation distributions across the top 10 respondent countries. | Country-level counts sum to total cross-national compensation sample. |
| `test_load_cleaned_survey_data_parquet` | Validates fast ingestion from `data/processed/survey_results_cleaned.parquet`. | Loads DataFrame with 49,191 rows and verify Parquet metadata. |

---

### 3.9. `tests/test_stackoverflow_cleaning.py` (11 Tests)
Validates data transformation pipelines, professional coding experience parsing, multi-select normalization, and Parquet caching.

| Test Function | Verification Scope | Assertions / Invariants |
|---|---|---|
| `test_classify_experience_value` | Tests experience binning logic for string and numeric inputs. | Categorizes `Less than 1 year` as `<2 years` and `More than 50 years` as `21+ years`. |
| `test_clean_experience_value_scalar` | Parses numeric years of experience from mixed string inputs. | Converts `"5"` $\to 5.0$, `"Less than 1 year"` $\to 0.5$, `"More than 50 years"` $\to 50.0$. |
| `test_clean_experience_series` | Vectorized experience parsing across entire pandas Series. | Produces clean float64 series with identical length; preserves nulls. |
| `test_normalize_multiselect_string` | Standardizes delimiter whitespace and removes duplicate technology tags. | `"Python; Python ; SQL "` $\to$ `"Python;SQL"`. |
| `test_normalize_multiselect_series` | Vectorized multi-select standardization across pandas Series. | Cleans every record in series; handles missing values cleanly. |
| `test_clean_stackoverflow_survey_synthetic` | Tests complete end-to-end cleaning pipeline on synthetic raw survey extract. | Executes deduplication, column type coercion, and derivation cleanly. |
| `test_clean_stackoverflow_survey_with_yearscodepro` | Tests feature engineering of `YearsCodePro` into standardized analytical brackets. | Creates `YearsCodePro_bracket` column matching 5-level taxonomy. |
| `test_clean_stackoverflow_survey_missing_id_and_empty_errors` | Verifies error handling when raw survey lacks `ResponseId` or contains 0 rows. | Raises `ValueError` prior to executing expensive transformation pipelines. |
| `test_clean_stackoverflow_survey_drops_null_ids` | Verifies that respondents with null `ResponseId` are discarded. | Drops unidentifiable records from cleaned output. |
| `test_save_processed_dataset` | Validates writing processed DataFrame to Apache Parquet with Snappy compression. | Verifies file is created on disk and is loadable via `pd.read_parquet`. |
| `test_processed_dataset_integrity_on_disk` | Audits cryptographic hash and schema of canonical Parquet artifact. | SHA-256 matches `16f5ce8e8f387405fa9635e44074dc468f44b82c0ee23287b2889be238fbbe52`. |

---

### 3.10. `tests/test_statistical_engine_validation.py` (7 Tests)
Independent closed-form mathematical benchmark proofs validating our statistical algorithms directly against theoretical formulas from statistical and econometric literature.

| Test Function | Mathematical Scope & Verification | Benchmark Equation / Theoretical Standard |
|---|---|---|
| `test_independent_normal_survival_probabilities` | Closed-form benchmark for standard normal CDF and upper-tail survival $P(Z > z)$. | Verifies rational Chebyshev polynomial approximation matches known Abramowitz and Stegun benchmarks within $10^{-7}$ precision. |
| `test_independent_chi2_survival_probabilities` | Independent survival function $P(\chi^2 > x)$ with $k$ degrees of freedom. | Compares regularized lower and upper incomplete gamma functions $\Gamma(s, x) / \Gamma(s)$ against known survival tables for $df \in \{1, 2, 4, 8\}$. |
| `test_independent_ols_and_white_hc1_closed_form_benchmark` | Multivariable OLS coefficients and White (1980) HC1 heteroskedasticity-robust covariance matrix. | Direct matrix proof: $\hat{\beta} = (X^TX)^{-1} X^T y$ and $\hat{\Sigma}_{\text{HC1}} = \frac{n}{n-k} (X^TX)^{-1} \left( \sum_{i=1}^n e_i^2 x_i x_i^T \right) (X^TX)^{-1}$. Validates standard errors, $t$-statistics, and two-tailed $p$-values. |
| `test_independent_contingency_and_odds_ratio_benchmark` | $2 \times 2$ contingency table, Pearson chi-square, crude odds ratio, and Woolf log-SE confidence intervals. | $\chi^2 = \sum \frac{(O - E)^2}{E}$, $\text{OR} = \frac{n_{11} n_{22}}{n_{12} n_{21}}$, $\text{SE}(\ln \text{OR}) = \sqrt{\frac{1}{n_{11}} + \frac{1}{n_{12}} + \frac{1}{n_{21}} + \frac{1}{n_{22}}}$. Verifies asymptotic normal intervals $[\exp(\ln \text{OR} \pm 1.96 \cdot \text{SE})]$. |
| `test_independent_anova_and_effect_sizes_benchmark` | One-way Analysis of Variance (ANOVA) decomposition and omnibus effect sizes. | Proves exact algebraic equivalence: $\text{SS}_{\text{total}} = \text{SS}_{\text{between}} + \text{SS}_{\text{within}}$, $F = \frac{\text{MS}_{\text{between}}}{\text{MS}_{\text{within}}}$, $\eta^2 = \frac{\text{SS}_{\text{between}}}{\text{SS}_{\text{total}}}$, $\omega^2 = \frac{\text{SS}_{\text{between}} - (k-1)\text{MS}_{\text{within}}}{\text{SS}_{\text{total}} + \text{MS}_{\text{within}}}$, and Cohen's $d = 2\sqrt{\frac{\eta^2}{1 - \eta^2}}$. |
| `test_independent_multiple_testing_adjustments` | False Discovery Rate (FDR) and Family-Wise Error Rate (FWER) multiple comparison corrections. | Verifies Benjamini-Hochberg procedure: $p_{(i)} \le \frac{i}{m} Q$, and conservative Bonferroni correction: $p_{\text{adj}} = \min(1.0, m \cdot p)$. |
| `test_independent_vif_closed_form_benchmark` | Variance Inflation Factor (VIF) collinearity detection via auxiliary regressions. | Proves: $\text{VIF}_j = \frac{1}{1 - R_j^2}$, where $R_j^2$ is coefficient of determination obtained from regressing predictor $x_j$ onto all remaining $k - 1$ predictors. |

---

## 4. Test Execution Instructions

### Prerequisites
Ensure your local environment has the project dependencies installed within `.venv`:
```bash
# Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Verify dependencies
pip install -r requirements-dev.txt
```

### 1. Execute Complete Test Suite
Run all 93 unit tests with default configuration:
```bash
pytest
```
*Expected duration:* $\approx 8 - 12$ seconds.  
*Expected outcome:* `93 passed in XX.XXs`.

### 2. Verbose Output with Execution Durations
Profile the top 10 slowest executing tests to monitor performance:
```bash
pytest -v --durations=10
```

### 3. Targeted Test Execution
Execute specific modules, classes, or individual test functions:

```bash
# Run statistical engine tests only
pytest tests/test_analysis.py

# Run mathematical benchmark validation tests only
pytest tests/test_statistical_engine_validation.py

# Run dashboard visual component tests only
pytest tests/test_dashboard_components.py

# Run a specific test function by name pattern
pytest -k "test_remotework_contingency_table_exact_reconciliation"

# Stop immediately upon first test failure
pytest -x
```

### 4. Flake8 Linting Enforcement
Audit all project code for strict PEP 8 conformance:
```bash
flake8 app src tests
```
*Expected outcome:* Exit code 0 with zero output (no errors, no warnings).

---

## 5. Continuous Integration (CI/CD) Pipeline

Automated testing is orchestrated via GitHub Actions workflows in [`.github/workflows/tests.yml`](file:///d:/Projects/Data%20Science/Poll%20Results%20Visualizer/.github/workflows/tests.yml).

### Workflow Configuration Matrix
- **Triggers:** Push events to `main` and all Pull Requests.
- **Operating System:** `ubuntu-latest`.
- **Python Matrix:** Python `3.10` and `3.11`.
- **Pipeline Stages:**
  1. **Checkout:** Fetches repository code.
  2. **Environment Setup:** Configures Python version with pip dependency caching.
  3. **Dependency Installation:** Upgrades pip and installs `requirements-dev.txt`.
  4. **Linting Gate:** Runs `flake8 app src tests`.
  5. **Test Execution Gate:** Runs `pytest`.

```yaml
name: Tests

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11"]

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt

      - name: Run linting
        run: |
          flake8 app src tests

      - name: Run tests with pytest
        run: |
          pytest
```

---

## 6. Live Application Health Verification Probe

In addition to static unit and integration tests, live application health is verified via loopback socket probes against Streamlit's internal health endpoint:

```python
import urllib.request
import urllib.error

health_url = "http://localhost:8501/_stcore/health"

try:
    with urllib.request.urlopen(health_url, timeout=5) as response:
        if response.status == 200:
            print("Streamlit Health Probe: SUCCESS (HTTP 200 OK)")
except urllib.error.URLError as e:
    print(f"Streamlit Health Probe: FAILED ({e.reason})")
```

---

## 7. Troubleshooting Common Testing Issues

| Symptom | Probable Cause | Corrective Action |
|---|---|---|
| `ModuleNotFoundError: No module named 'app'` or `'src'` | Current working directory is not the project root, or `sys.path` does not include project root. | Ensure commands are executed from the repository root directory (`D:/Projects/Data Science/Poll Results Visualizer`). `pytest.ini` automatically adds the root to `pythonpath`. |
| `Cleaned survey dataset not present on disk` (Skipped tests) | Normal and expected in clean CI clones where `survey_results_cleaned.parquet` is not stored in git. | To run parquet-dependent tests locally, generate the parquet file via: `python -c "from src.datasets.stackoverflow_cleaning import clean_and_save_survey_data; clean_and_save_survey_data()"`. |
| `AssertionError: assert 0.1203 == approx(0.1204)` | Rust coefficient precision mismatch. | The canonical Model 3 Rust coefficient is unrounded $+0.1203419...$, which rounds to $+0.1203$ (not $+0.1204$). Verify using `outputs/analysis_summary_metrics.json`. |
| Flake8 `E501 line too long (> 100 characters)` | Formatting violation in Python source file. | Wrap long strings using implicit string literal concatenation or multi-line tuples. Verify via `.flake8` configuration (`max-line-length = 100`). |
| Flake8 `W291 trailing whitespace` or `W293 blank line contains whitespace` | Editor left trailing spaces. | Remove trailing whitespace or configure your IDE to strip trailing whitespace on file save. |

---

## 8. Summary Checklist for Pull Requests

Before committing and submitting a Pull Request, maintainers must verify:
- [x] Virtual environment `.venv` is active.
- [x] `pytest` passes with 100% pass rate (93/93 tests passing).
- [x] `flake8 app src tests` passes with 0 errors and 0 warnings.
- [x] No sensitive API keys, local credentials, or machine paths are hardcoded.
- [x] Any new analytical function has corresponding unit tests in `tests/`.
- [x] Documentation in `docs/` and `README.md` is updated to reflect any new parameters or behavior.
