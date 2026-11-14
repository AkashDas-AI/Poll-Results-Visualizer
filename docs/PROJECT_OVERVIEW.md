# Project Overview: Poll Results Visualizer

**Project Name:** Poll Results Visualizer  
**Author:** Akash Das  
**Version:** 1.0.0 (Phase 8 Production Release)  
**Primary Dataset:** Stack Overflow Annual Developer Survey 2025  
**License:** MIT License (Source Code) / Open Database License v1.0 (Survey Microdata)  
**Status:** Complete & Verified Across All 8 Phases  

---

## 1. Executive Summary & Problem Statement

Public opinion polls, developer sentiment studies, and labor market surveys generate high-dimensional, complex datasets characterized by:
- Wide respondent tables ($170+$ attributes per individual).
- High item nonresponse and conditional branching logic.
- Semicolon-delimited multi-select questions that distort standard percentage totals.
- Heavy right-skewness and currency heterogeneity in self-reported compensation.
- Uncritical conflation of cross-sectional survey associations with causal mechanisms in popular reporting.

**Poll Results Visualizer** is an enterprise-grade survey analytics platform, econometric engine, and interactive dashboard built in Python. Fielded against 49,191 raw microdata records from the official **Stack Overflow Annual Developer Survey 2025**, the project demonstrates how data science pipelines must unite rigorous statistical theory with clean, decoupled software engineering.

The application eliminates black-box shortcuts by implementing an independent econometric engine from first principles in pure Python and NumPy, decoupling business logic from presentation, and enforcing mathematically disciplined dual-denominator reporting.

---

## 2. Core Project Objectives

1. **Authentic Public Data Engineering:** Ingest, audit, and clean authentic public survey microdata without synthetic shortcuts or lossy in-place mutations.
2. **First-Principles Statistical & Econometric Rigor:** Implement Ordinary Least Squares (OLS) with White HC1 heteroskedasticity-robust covariance, auxiliary Variance Inflation Factor (VIF) collinearity diagnostics, Breusch-Pagan tests, Chi-Square tests of independence, and One-Way ANOVA with effect size decomposition ($\eta^2$, $\omega^2$, Cohen's $d$).
3. **Optimized High-Performance Storage:** Convert raw 140.8 MB CSV data into an Apache Parquet format using Snappy compression, cutting storage footprint by $92.6\%$ (down to $9.8$ MB) and accelerating cold-load times tenfold.
4. **Decoupled Software Architecture:** Enforce strict architectural boundaries between data ingestion, econometric modeling, chart generation, and UI views, ensuring the analytical engine is 100% testable via standard `pytest` runners.
5. **Interactive Executive Visualization:** Deliver a responsive, multi-page Streamlit and Plotly dashboard featuring dynamic demographic cohort slicing, sub-second caching (`@st.cache_data`), sample flow funnels, and in-memory CSV export streams.
6. **Centralized Light/Dark Theme Architecture:** Implement an enterprise design system in `app/components/theme.py` featuring a persistent sidebar radio toggle (`theme_mode_selector`), session state persistence (`theme_mode`: `"Dark"` / `"Light"`), scoped CSS injection, and dynamic Plotly figure theming (`apply_chart_theme`) across all 14 dashboard charts.
7. **Non-Causal Analytical Governance:** Uphold strict observational framing across all automated narratives, reminding stakeholders that cross-sectional survey comparisons reflect sample associations rather than causal effects.
8. **Production Code Quality:** Maintain an exhaustive test suite (116 unit tests: 115 passed, 1 skipped), zero Flake8 linting errors across all modules, immutable cryptographic dataset hashes (SHA-256), and an automated pre-publication security scan confirming 0 leaked credentials.

---

## 3. Technology Stack

| Layer | Technology | Version | Purpose & Rationale |
| :--- | :--- | :--- | :--- |
| **Runtime** | Python | 3.11.0 | High-performance base runtime for enterprise data science. |
| **Data Processing** | Pandas, NumPy | 2.2.3, 2.1.3 | Vectorized array operations and structured tabular data manipulation. |
| **Storage & Serialization** | PyArrow / Parquet | 18.1.0 | Fast columnar storage with Snappy compression for 9.8 MB footprint. |
| **Econometric Engine** | Pure Python / NumPy | - | Closed-form OLS, White HC1, VIF, Chi-Square, and ANOVA from scratch. |
| **Data Visualization** | Plotly | 5.24.1 | Interactive, accessible charts with shared themes and hover templates. |
| **Application UI** | Streamlit | 1.40.2 | Reactive multi-page web dashboard with `@st.cache_data` memory caching. |
| **Testing Framework** | Pytest | 8.3.4 | Automated unit test suite with 116 tests (115 passed, 1 skipped) and CI skip guards. |
| **Code Style & Linting** | Flake8 | 7.1.1 | PEP 8 style guide enforcement with zero warnings and zero errors across app, src, tests, tools. |
| **CI / CD Automation** | GitHub Actions | - | Automated linting and test execution matrix on Python 3.10 and 3.11. |

---

## 4. Eight-Phase Development Roadmap Ledger

The project was executed through an eight-phase software development lifecycle:

- **Phase 1 - Foundation Setup & Modularization:** Established directory structure, local virtual environment (`.venv`), configuration constants (`src/config.py`), base data loaders, deduplication logic, and initial 4-page Streamlit shell.
- **Phase 2 - Official Public Data Integration:** Acquired and audited the official Stack Overflow Developer Survey 2025 (49,191 rows $\times$ 172 columns), implemented the domain adapter (`src/datasets/stackoverflow_2025.py`), authored 10-section exploratory data analysis notebook (`notebooks/01_data_exploration.ipynb`), and eliminated synthetic mock artifacts.
- **Phase 3 - Wide-Format Data Hygiene & Feature Derivation:** Implemented non-destructive experience parsing (`YearsCode_num`, `WorkExp_num`), standardized 78 semicolon-delimited multi-select questions, categorized compensation reporting taxonomy, established zero-date fabrication policy, and serialized the dataset to Apache Parquet.
- **Phase 4 - Exploratory Data Analysis & Quality Reporting:** Completed comprehensive data quality audits, generated missingness heatmaps, documented item nonresponse, produced `reports/data_quality_report.md` and `reports/eda_report.md`, and validated population constants ($N_{\text{raw}} = 49,191, N_{\text{official}} = 49,009$).
- **Phase 5 - Statistical Modeling & Econometric Engine:** Implemented from first principles in `src/analysis.py`: OLS with White HC1 robust covariance, Breusch-Pagan tests, auxiliary VIF routines, Chi-Square contingency tests with Cramér's V, odds ratios with Wald CIs, ANOVA with effect sizes ($\eta^2, \omega^2, d$), Bonferroni-Holm familywise error adjustments, and Cook's distance sensitivity analysis ($4/n$). Verified against textbook closed-form benchmarks.
- **Phase 6 - Interactive Visualization Implementation:** Deployed full multi-page dashboard in `app/` featuring Plotly charts with dual-denominator normalization, paired language migration analysis across 27,079 symmetric respondents, interactive compensation boxplots, sample flow funnels, and verified RemoteWork missingness contingency reconciliation.
- **Phase 7 - Insights & Professional Reporting:** Authored comprehensive reporting deliverables (`reports/project_report.md`, `reports/key_insights_report.md`, `reports/recommendations_report.md`, `docs/INTERVIEW_PREPARATION.md`, `docs/PORTFOLIO_PRESENTATION_GUIDE.md`). Reconciled Rust regression coefficient precision ($\hat{\beta} = +0.1203, +12.79\%$).
- **Phase 8 - Final Project Polish, GitHub Preparation, and Publication:** Conducted automated pre-publication security audit (73 files scanned, 0 secrets), rewrote `README.md` (0 emojis, 0 em dashes, 26 required domains), decoupled CI testing via `@require_parquet`, confirmed 93 passing unit tests and 0 Flake8 errors, staged 73 approved files, and created initial commit on `main`.

---

## 5. Key Research Questions & Empirical Findings

### RQ1: Generative AI Trust Paradox
- **Empirical Finding:** While $78.50\%$ of respondents actively use AI developer tools, $45.69\%$ actively distrust tool output accuracy, with only $3.09\%$ expressing high trust.
- **Seniority Trust Gap:** Distrust escalates with professional experience. Entry-level developers (<2 years) exhibit $43.92\%$ distrust, while veteran developers (21+ years) exhibit $47.99\%$ distrust (Crude Odds Ratio $\text{OR} = 1.178, p = 0.0043, N = 30,780$).
- **Statistical Integrity:** 3-category global chi-square test: $\chi^2 = 38.3898, df = 8, p = 6.38 \times 10^{-6}$, Cramér's $V = 0.02497$. Collapsed binary test: $\chi^2 = 30.1175, df = 4, p = 4.63 \times 10^{-6}$.

### RQ2: Technology Stack Compensation Premiums
- **Extended Mincerian Model (Model 3, $N = 22,769, R^2 = 0.3846, \text{RMSE} = 0.6979$):**
  - **Docker:** $+13.17\%$ premium ($\hat{\beta} = +0.1237, t = 9.49, p = 2.39 \times 10^{-21}$, robust 95% CI: $[+10.31\%, +16.10\%]$).
  - **Rust:** $+12.79\%$ premium ($\hat{\beta} = +0.1203, t = 7.25, p = 4.32 \times 10^{-13}$, robust 95% CI: $[+9.18\%, +16.52\%]$).
  - **AWS:** $+10.91\%$ premium ($\hat{\beta} = +0.1036, t = 8.11, p = 4.92 \times 10^{-16}$, robust 95% CI: $[+8.17\%, +13.72\%]$).
  - **TypeScript:** $+7.50\%$ premium ($\hat{\beta} = +0.0723, t = 5.85, p = 4.86 \times 10^{-9}$, robust 95% CI: $[+4.93\%, +10.14\%]$).
  - **Go:** $+7.10\%$ premium ($\hat{\beta} = +0.0686, t = 4.37, p = 1.23 \times 10^{-5}$, robust 95% CI: $[+3.86\%, +10.45\%]$).
  - **Python:** $+1.32\%$ premium ($\hat{\beta} = +0.0131, t = 1.07, p = 0.2857$ [not statistically significant], robust 95% CI: $[-1.09\%, +3.79\%]$).
- **Exact Percentage Rule:** All differentials calculated via Halvorsen and Palmquist's exact formula $100 \times (e^\beta - 1)$.
- **Multicollinearity:** All predictor VIFs $< 1.50$, safely below the $5.0$ concern threshold.

### RQ3: Autonomous AI Agents vs. Job Satisfaction
- **Statistical vs. Practical Significance:** One-way ANOVA evaluating job satisfaction across 6 AI agent adoption tiers on complete cases ($N = 23,766$) yielded extreme statistical significance:
  $$F(5, 23760) = 11.6172, \quad p = 3.019 \times 10^{-11}$$
- **Effect Size Decomposition:** Despite extreme statistical significance, the practical effect size is negligible:
  $$\eta^2 = 0.002439 \quad (\approx 0.24\% \text{ variance explained}), \quad \omega^2 = 0.002229 \quad (\approx 0.22\%)$$
- **Pairwise Contrast:** Daily agent users report a mean job satisfaction of $7.401$ vs $7.149$ for non-planners—a difference of only $+0.252$ points on a 10-point scale (Cohen's $d = 0.128$).

### RQ4: Remote Work Compensation Dynamics
- **Confounded Raw Differential:** In raw data, remote workers report an apparent $+88.6\%$ median salary gap over in-person peers.
- **Econometric Model C ($N = 20,236, R^2 = 0.4254$):** Controlling for country, experience, and organization size attenuates the conditional remote differential to **$+30.65\%$** ($\hat{\beta} = +0.267353, t = 12.35, p = 6.44 \times 10^{-35}$), proving the raw gap is primarily driven by geographic clustering in high-wage economies.

---

## 6. Governance, Licensing, and Attribution

- **Project Author:** Akash Das
- **Source Code License:** MIT License (permissive open-source license covering all source code and documentation).
- **Dataset License:** Open Database License (ODbL) v1.0, © Stack Exchange, Inc. Database Contents License (DbCL) applies to microdata contents.
- **Attribution Notice:** Stack Overflow Developer Survey 2025 microdata is utilized under ODbL terms. The project is an independent analytical study and is not affiliated with or endorsed by Stack Exchange, Inc.
