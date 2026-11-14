# Poll Results Visualizer: Stack Overflow Developer Survey 2025 Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.24+-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2+-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.26+-013243?logo=numpy&logoColor=white)](https://numpy.org/)
[![Apache Parquet](https://img.shields.io/badge/Data%20Format-Apache%20Parquet-5080E2)](https://parquet.apache.org/)
[![Statistical Inference](https://img.shields.io/badge/Inference-White%20HC1%20%7C%20OLS-blue)](reports/analysis_report.md)
[![Tests](https://img.shields.io/badge/Tests-115%20Passed%20%7C%201%20Skipped-success)](tests/)
[![Code Style](https://img.shields.io/badge/Code%20Style-Flake8%20(0%20errors)-blue)](.flake8)
[![Dataset](https://img.shields.io/badge/Dataset-Stack%20Overflow%202025-orange)](https://survey.stackoverflow.co/2025/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Author:** Akash Das<br>
**Role:** Data Science and Analytics Intern Candidate<br>
**GitHub Repository:** [https://github.com/AkashDas-AI/Poll-Results-Visualizer](https://github.com/AkashDas-AI/Poll-Results-Visualizer)<br>
**Primary Dataset:** Official Stack Overflow Annual Developer Survey 2025 (49,191 respondents across 177 countries)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Business Problem and Motivation](#2-business-problem-and-motivation)
3. [Project Objectives](#3-project-objectives)
4. [Key Features](#4-key-features)
5. [Dashboard Overview and Screenshots](#5-dashboard-overview-and-screenshots)
6. [Dataset and Data Source Attribution](#6-dataset-and-data-source-attribution)
7. [Dataset Structure and Population Definitions](#7-dataset-structure-and-population-definitions)
8. [Data Cleaning and Validation Methodology](#8-data-cleaning-and-validation-methodology)
9. [Exploratory Data Analysis](#9-exploratory-data-analysis)
10. [Statistical Analysis and Research Questions](#10-statistical-analysis-and-research-questions)
11. [Key Findings and Insights](#11-key-findings-and-insights)
12. [Interactive Dashboard Pages and Functionality](#12-interactive-dashboard-pages-and-functionality)
13. [Project Architecture and Directory Structure](#13-project-architecture-and-directory-structure)
14. [Technology Stack](#14-technology-stack)
15. [Installation Prerequisites](#15-installation-prerequisites)
16. [Step-by-Step Local Setup Instructions for Windows](#16-step-by-step-local-setup-instructions-for-windows)
17. [Instructions for Obtaining the Official Survey Dataset](#17-instructions-for-obtaining-the-official-survey-dataset)
18. [Instructions for Running the Data Pipeline](#18-instructions-for-running-the-data-pipeline)
19. [Instructions for Launching the Streamlit Application](#19-instructions-for-launching-the-streamlit-application)
20. [Testing and Linting Instructions](#20-testing-and-linting-instructions)
21. [Methodological Limitations and Responsible Interpretation](#21-methodological-limitations-and-responsible-interpretation)
22. [Licensing and Attribution](#22-licensing-and-attribution)
23. [Author Information](#23-author-information)
24. [Professional Profiles and Contact](#24-professional-profiles-and-contact)

---

## 1. Project Overview

Poll Results Visualizer is a production-grade, modular Python data analytics and econometric modeling platform. The platform is designed to ingest, validate, clean, analyze, and visualize large-scale public opinion and survey datasets. It is integrated with the official Stack Overflow Annual Developer Survey 2025 microdata.

The system is engineered using a decoupled four-tier architecture:
- Data Engineering and Hygiene: Data ingestion, numeric experience derivation, delimiter cleaning, and Parquet serialization.
- Pure-Python Econometric and Statistical Engine: Ordinary Least Squares regression, White HC1 heteroskedasticity-robust standard errors, Variance Inflation Factor diagnostics, contingency chi-square tests, and one-way ANOVA with effect size decomposition.
- Interactive Streamlit and Plotly Presentation Tier: Multi-page responsive web dashboard with dual-denominator arithmetic, dynamic cohort filtering, and persistent Light/Dark mode theming.
- Automated Quality Assurance Suite: 116 automated unit tests (115 passed, 1 skipped) with zero Flake8 linting errors.

---

## 2. Business Problem and Motivation

Public opinion surveys and developer community polls contain valuable signals for technology strategists, engineering executives, and talent committees. However, raw survey microdata presents serious analytical and statistical challenges:
- Non-Random Convenience Sampling: Survey respondents opt in voluntarily. Findings reflect observed cohort patterns within the sample and cannot be assumed to be randomized probability samples of all developers worldwide.
- Question Nonresponse: Survey participants omit optional questions at variable rates. Calculating percentages against total respondents rather than question-specific answered counts distorts results.
- Multi-Select Checkboxes: Technologies and developer tools allow multiple choices. Conflating Selection Share (fraction of total checkmarks) with Respondent Share (fraction of developers using the tool) misleads stakeholders.
- Skewed Compensation Distributions: Developer salaries are heavily skewed and contain extreme outliers ($0 to $50,000,000). Naive arithmetic means misrepresent market compensation.
- Confounded Comparisons: Superficial wage comparisons (such as remote versus in-person work) frequently confuse geographic concentration in high-wage economies with true remote wage premiums.

Poll Results Visualizer resolves these challenges by enforcing transparent denominators, non-parametric distributional summaries, econometric controls, and rigorous observational framing.

---

## 3. Project Objectives

1. Develop a deterministic, non-destructive data cleaning pipeline that preserves raw survey records while deriving clean numeric analytical features.
2. Build an independent, pure-Python econometric calculation engine from first principles, avoiding native binary compilation issues in sandbox environments.
3. Design and deploy an interactive multi-page Streamlit portal delivering sub-second cohort slicing, dual-denominator visualizations, and clear tooltips.
4. Implement a centralized, persistent Light Mode / Dark Mode toggle across all dashboard pages with responsive Plotly figure styling.
5. Investigate four core empirical research questions covering AI accuracy trust, human capital compensation premiums, autonomous AI agents versus job satisfaction, and remote work compensation dynamics.
6. Provide comprehensive, evidence-grounded documentation and reporting deliverables tailored for Data Analyst, Business Analyst, and Insights Analyst roles.

---

## 4. Key Features

- Deterministic Data Hygiene: Cleans and derives numeric experience variables from qualitative top-coded categories while preserving source text columns intact.
- High-Performance Vectorized I/O: Serializes cleaned microdata into Apache Parquet with Snappy compression, shrinking storage from 132 MB to 9.8 MB (92.6% reduction) and accelerating dashboard queries tenfold.
- Dual-Denominator Visualizations: Distinguishes between Respondent Share (percentage of respondents who use a tool) and Selection Share (percentage of all checkmarks recorded) across multi-select questions.
- Pure-Python Econometric Engine: Executes multivariable OLS regressions, White HC1 robust covariance matrix estimation, Breusch-Pagan heteroskedasticity tests, and auxiliary VIF regressions without external C-extension dependencies.
- Sub-Second Interactive Filtering: Dynamic demographic slicers across 177 countries, 5 experience brackets, and salary trimming thresholds powered by Streamlit memory caching (`@st.cache_data`).
- Enterprise Light & Dark Mode Theming: Centralized theme architecture (`app/components/theme.py`) featuring high-contrast Business Intelligence palettes, scoped CSS injection, and transparent Plotly figure adaptability (`apply_chart_theme`) across all 14 dashboard charts. Theme selection is driven by a sidebar radio toggle (`theme_mode_selector`) with seamless session-state persistence (`theme_mode`) across page navigation.
- Comprehensive Test Coverage: 116 automated unit tests in pytest verifying statistical engines, theme lifecycle persistence, Plotly figure theming, data adapters, UI components, and reporting assertions with 115 passed and 1 skipped (100% core pass rate).

---

## 5. Dashboard Overview and Screenshots

The application provides an interactive web dashboard divided into four dedicated analytical pages plus an executive landing portal, each featuring an interactive sidebar theme toggle (`🌙 Dark` / `☀️ Light`):
- Executive Home Portal: Displays global survey telemetry (49,191 raw extract, 49,009 official qualified base, 177 countries, 78.5% AI adoption, $75,320 USD median compensation).
- Page 1 (Overview): Developer demographics, natural age distribution, formal education levels, coding versus work experience profiles, employment breakdown, and geographic distribution.
- Page 2 (Response Analysis): Programming language adoption, paired current-versus-desired preference gaps (N = 27,079), databases, cloud platforms, and a four-tab AI adoption hierarchy.
- Page 3 (Segment Comparison): Role compensation distributions, top 10 country wage medians, concave quadratic experience gradients, and remote work wage attenuation analysis.
- Page 4 (Data Quality): Missingness rankings across all survey items, RemoteWork nonresponse association audit, compensation sample flow funnel, and dataset export capabilities.

### Dashboard Preview

<!-- Screenshot 1: Executive Dashboard Landing Page -->
![Dashboard Overview](images/dashboard_overview.png)
*Figure 1: Executive Dashboard Landing Page showing global survey telemetry and high-level KPIs in Dark Mode.*

<!-- Screenshot 2: Overview Demographics & Sample Funnel -->
![Overview Demographics](images/page1_overview_demographics.png)
*Figure 2: Overview page featuring demographic distributions, formal education profiles, and cohort slicing controls.*

<!-- Screenshot 3: Programming Language Adoption and Stated Preference Gaps -->
![Response Analysis](images/response_analysis.png)
*Figure 3: Response Analysis page featuring dual-denominator technology adoption and paired current-versus-desired preference gaps.*

<!-- Screenshot 4: Segment Comparison and Remote Work Dynamics -->
![Segment Comparison](images/segment_comparison.png)
*Figure 4: Segment Comparison page displaying cross-cohort salary distributions, quartile statistics, and remote wage attenuation.*

<!-- Screenshot 5: Data Quality and Nonresponse Mechanism Audit -->
![Data Quality](images/data_quality.png)
*Figure 5: Data Quality page illustrating survey missingness rankings and the audited RemoteWork nonresponse contingency table.*

<!-- Screenshot 6: Dual-Theme Enterprise Dark vs Light Mode Comparison -->
![Theme Comparison](images/theme_comparison.png)
*Figure 6: Dual-Theme Comparison showcase demonstrating responsive Plotly transparent canvas adaptability between Enterprise Dark Theme (left) and Accessibility Light Theme (right).*

### Recommended Screenshots for Repository Maintainers

When capturing and adding screenshots to the `images/` folder, maintain the following naming conventions:
1. `images/dashboard_overview.png`: Full-width browser capture of the Executive Home landing portal.
2. `images/page1_overview_demographics.png`: Capture of Page 1 showing the sample flow funnel, question completeness inventory, and natural demographic distributions.
3. `images/response_analysis.png`: Capture of Page 2 showing the dual-denominator language bar chart and preference gap table.
4. `images/segment_comparison.png`: Capture of Page 3 showing the boxplot distributions and Model C remote work comparison.
5. `images/data_quality.png`: Capture of Page 4 showing the missingness ranking chart and contingency table audit.
6. `images/theme_comparison.png`: Side-by-side Dark Theme vs Light Theme comparison demonstrating transparent chart canvas adaptability.

To regenerate all screenshots deterministically at Full HD 1920x1080 resolution, maintainers can run:
```bash
python tools/capture_screenshots.py
```
For detailed capture protocols, asset budgets (< 400 KB), and visual guidelines, refer to the [Screenshot Guide](docs/SCREENSHOT_GUIDE.md).

---

## 6. Dataset and Data Source Attribution

- Dataset Name: Stack Overflow Annual Developer Survey 2025
- Survey Period: May 2025 to June 2025
- Publisher: Stack Exchange, Inc.
- Official Source Endpoint: [https://survey.stackoverflow.co/2025/](https://survey.stackoverflow.co/2025/)
- Data License: Open Database License (ODbL) v1.0, with database contents licensed under Database Contents License (DbCL) v1.0.
- Project Source Code License: MIT License (Copyright Akash Das).

---

## 7. Dataset Structure and Population Definitions

To ensure transparency, this project strictly maintains three population boundaries:

| Population Metric | Count | Definition and Boundary |
| :--- | :---: | :--- |
| **Raw Survey Extract ($N_{\text{raw}}$)** | **49,191** | Complete unweighted respondent rows in the official public microdata extract (`survey_results_public.csv`). |
| **Official Qualified Base ($N_{\text{official}}$)** | **49,009** | Qualified respondents reported in official Stack Overflow web summaries post-qualification screening (182-row boundary). |
| **Question-Specific Answered ($N_{\text{answered}}$)** | Variable | Respondents providing a non-null, valid response to a specific survey item (e.g., $N=33,720$ for `AISelect`). |

### Methodological Principles:
- Opt-In Convenience Nature: Findings describe empirical associations observed in this community sample; they do not represent random probability samples of the global developer population.
- Explicit Denominators: Every percentage, chart annotation, and tabular metric explicitly discloses its valid answered denominator ($N_{\text{answered}}$).

---

## 8. Data Cleaning and Validation Methodology

The pipeline in `src/datasets/stackoverflow_cleaning.py` implements deterministic, non-destructive hygiene:

1. Numeric Experience Derivation:
   - Qualitative string entries such as `'Less than 1 year'` are mapped to $0.5$ years.
   - Top-coded entries such as `'More than 50 years'` are mapped to $51.0$ years.
   - Clean continuous numeric features are stored in derived columns (`YearsCode_num`, `WorkExp_num`), while raw text columns (`YearsCode`, `WorkExp`) remain completely intact.
2. Multi-Select Delimiter Standardization:
   - Standardizes delimiters across 78 multi-select columns without splitting compound technical tokens such as `C++`, `C#`, or `HTML/CSS`.
3. Financial Variable Hygiene:
   - Evaluates `ConvertedCompYearly` (annual compensation converted to USD by Stack Overflow using spot exchange rates on June 25, 2025).
   - Validates positive salary records ($N=23,947$) and trims extreme non-representative outliers ($<\$1,000$ and $>\$1,000,000$) to yield a qualified estimation base of $N=23,177$.
   - Notes that compensation is self-reported and unadjusted for local Purchasing Power Parity (PPP).

---

## 9. Exploratory Data Analysis

### 9.1. Demographic Profile and Core Distributions

Across the $49,191$ raw survey records, empirical distributions highlight an early-to-mid career developer demographic concentrated in primary tech hubs:

| Demographic Dimension | Metric / Cohort | Count ($N$) | Share of Answered (%) | Analytical Interpretation |
| :--- | :--- | :---: | :---: | :--- |
| **Natural Age Cohorts** | Under 18 years | 1,460 | 2.97% | Early learners and secondary students |
| | 18–24 years | 9,210 | 18.72% | University entrants and junior engineers |
| | **25–34 years (Modal)** | **16,519** | **33.58%** | **Core professional software workforce** |
| | 35–44 years | 13,241 | 26.92% | Mid-to-senior engineers and leads |
| | 45–54 years | 5,618 | 11.42% | Principal engineers and engineering managers |
| | 55–64 years | 2,423 | 4.93% | Senior technical fellows and directors |
| | 65+ years | 625 | 1.27% | Veteran engineers and technical consultants |
| | *Prefer not to say* | *95* | *0.19%* | Non-disclosed age demographic |
| **Formal Education Level** | **Bachelor’s degree (Modal)** | **21,598** | **43.91%** | **Standard global industry credential** |
| | Master’s degree | 12,185 | 24.77% | Post-graduate specialized workforce |
| | Some college / No degree | 6,076 | 12.35% | Self-taught and non-traditional entrants |
| | Secondary school | 3,842 | 7.81% | High school / secondary education base |
| | Professional degree (PhD/MD) | 2,750 | 5.59% | Advanced research and scientific developers |
| | Associate degree | 1,630 | 3.31% | Two-year vocational technical degrees |
| | Primary / Elementary | 645 | 1.31% | Early-stage junior learners |
| | Other educational credentials | 465 | 0.95% | Specialized non-formal certifications |
| **Experience Profiles** | Coding Experience (YearsCode) | 48,110 | Median: 11.0 yrs | Interquartile Range: 6.0 to 18.0 years |
| | Professional Work (WorkExp) | 33,655 | Median: 8.0 yrs | Interquartile Range: 4.0 to 15.0 years |
| **Professional Branch** | **Developer by profession** | **37,467** | **76.17%** | **Core primary target population** |
| | Code as part of work/studies | 4,894 | 9.95% | Data analysts, scientists, researchers |
| | Learning to code | 2,585 | 5.26% | Full-time students and boot campers |
| | Hobbyist coder | 1,924 | 3.91% | Non-commercial open-source contributors |
| | Former professional developer | 1,325 | 2.69% | Retired or transitioned professionals |
| | Developer support / adjacent | 996 | 2.02% | Technical support, solutions engineers |

---

### 9.2. Technology Adoption & Stated Preference Landscape

Evaluating technology adoption across $48,341$ answered respondents and stated migration desire across symmetric complete cases ($N_{\text{paired}} = 27,079$):

| Technology / Tool | Category | Current Use ($N$) | Current Share (%) | Desired Use ($N$) | Desired Share (%) | Stated Net Gap ($\Delta\%$) | Preference Momentum |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **JavaScript** | Language | 17,896 | 66.09% | 10,580 | 39.07% | -27.02% | Declining relative share |
| **HTML/CSS** | Web Frontend | 16,843 | 62.20% | 8,828 | 32.60% | -29.60% | Foundational legacy saturation |
| **SQL** | Database | 15,929 | 58.82% | 11,481 | 42.40% | -16.43% | Persistent relational staple |
| **Python** | Multi-purpose | 15,741 | 58.13% | 15,489 | 57.20% | -0.93% | Highly stable adoption parity |
| **Bash/Shell** | Scripting/CLI | 13,269 | 49.00% | 9,126 | 33.70% | -15.30% | Essential infrastructure tool |
| **TypeScript** | Web/Application | 11,850 | 43.76% | 14,135 | 52.20% | **+8.44%** | **Strong upward migration** |
| **Java** | Backend/Enterprise | 7,991 | 29.51% | 4,766 | 17.60% | -11.91% | Maturing enterprise contraction |
| **C#** | Enterprise/.NET | 7,555 | 27.90% | 6,553 | 24.20% | -3.70% | Stable modern enterprise base |
| **C++** | Systems/Embedded | 6,391 | 23.60% | 5,470 | 20.20% | -3.40% | Core systems stability |
| **Go** | Cloud/Backend | 4,554 | 16.82% | 7,414 | 27.38% | **+10.56%** | **High positive cloud momentum** |
| **Rust** | Systems/Performance| 4,264 | 15.75% | 9,260 | 34.20% | **+18.45%** | **Top industry desire ratio (2.17x)**|
| **Docker** | Containerization | 18,630 | 68.80% | 17,980 | 66.40% | -2.40% | Dominant DevOps standard |
| **PostgreSQL** | Relational DB | 15,435 | 57.00% | 15,814 | 58.40% | **+1.40%** | Leading open-source database |
| **AWS** | Cloud Platform | 12,835 | 47.40% | 13,675 | 50.50% | **+3.10%** | Primary enterprise cloud provider |

---

### 9.3. Cross-National Compensation Benchmarks (Top 10 Economies)

Financial analysis on trimmed, qualified compensation respondents ($N = 23,177$, values converted to USD at spot exchange rates):

| Country Economy | Sample ($N$) | Median Annual USD | Mean Annual USD | Standard Deviation | 25th Pct (Q1) | 75th Pct (Q3) | Interquartile Range |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **United States** | **7,489** | **$150,000** | **$167,412** | $64,815 | $115,000 | $200,000 | $85,000 |
| **Australia** | 650 | $110,750 | $121,800 | $48,220 | $88,200 | $140,480 | $52,280 |
| **Canada** | 1,180 | $102,190 | $112,430 | $44,110 | $78,840 | $129,940 | $51,100 |
| **United Kingdom**| 1,842 | $88,272 | $97,310 | $41,200 | $64,240 | $112,390 | $48,150 |
| **Netherlands** | 740 | $85,561 | $91,240 | $32,150 | $69,519 | $105,883 | $36,364 |
| **Germany** | 2,215 | $80,214 | $87,450 | $31,540 | $68,449 | $102,674 | $34,225 |
| **Poland** | 590 | $64,171 | $71,320 | $32,800 | $47,059 | $85,562 | $38,503 |
| **France** | 985 | $58,824 | $64,210 | $26,450 | $48,128 | $73,798 | $25,670 |
| **Brazil** | 620 | $32,085 | $42,150 | $31,200 | $18,182 | $52,407 | $34,225 |
| **India** | 1,560 | $21,550 | $31,420 | $28,900 | $11,970 | $38,310 | $26,340 |
| **Global Sample** | **23,177**| **$75,320** | **$98,420** | $66,110 | **$45,000** | **$130,000** | **$85,000** |

---

## 10. Statistical Analysis and Research Questions

The project formulates and tests four formal research questions:

- **RQ1 (AI Accuracy Trust Gap):** Does skepticism regarding AI tool output accuracy associate with professional engineering seniority?
  - Evaluated via contingency tables, Pearson chi-square tests of independence, Cramér's V, and crude odds ratios across 5 experience cohorts ($N = 30,780$).
- **RQ2 (Human Capital and Technology Premiums):** Holding experience, geography, and developer role constant, what conditional compensation differentials associate with specialized tools?
  - Evaluated using an extended Mincerian semi-logarithmic OLS model with White HC1 robust standard errors ($N = 22,769, R^2 = 0.3846$).
- **RQ3 (Autonomous AI Agents vs. Job Satisfaction):** Does adoption of autonomous AI agent workflows associate with higher developer job satisfaction?
  - Evaluated via one-way ANOVA and effect size decomposition (eta-squared, omega-squared) across 6 adoption tiers ($N = 23,766$).
- **RQ4 (Remote Work Compensation Dynamics):** Does the raw wage gap between remote and in-person developers persist after controlling for country, experience, and organization size?
  - Evaluated using econometric Model C with exact Halvorsen-Palmquist exponential percentage conversions ($N = 20,236, R^2 = 0.4254$).

---

## 11. Key Findings and Insights

### 1. The AI Tooling Paradox (RQ1)
While $78.50\%$ ($26,469 / 33,720$) of answered developers actively use AI tools, $45.69\%$ ($11,936 / 26,126$) of active AI users distrust output accuracy, compared to only $3.09\%$ who express high trust.

In complete-case seniority analysis ($N = 30,780$), AI accuracy evaluations associate significantly with developer experience across both formal tests:
- Global 3-Category Test ($5 \times 3$ Table: Distrust, Neutral, Trust): $\chi^2 = 38.3898, df = 8, p = 6.377 \times 10^{-6}$, Cramér's $V = 0.02497$.
- Collapsed Binary Test ($5 \times 2$ Table: Distrust vs Not Distrust): $\chi^2 = 30.1175, df = 4, p = 4.632 \times 10^{-6}$, Cramér's $V = 0.03128$.
- Veteran engineers (21+ years) exhibit higher distrust ($47.99\%$, $3,436 / 7,160$) than entry-level peers ($43.92\%$, $654 / 1,489$), yielding a crude odds ratio of $\text{OR} = 1.178$ ($95\%$ CI: $[1.053, 1.318], p = 0.0043, z = 2.86$).

#### Table 11.1: Seniority vs AI Trust Contingency Matrix ($N = 30,780$)
| Professional Experience Bracket | Distrust AI Accuracy ($N$) | Neutral / Somt. Trust ($N$) | Highly Trust AI ($N$) | Total Answered ($N$) | Distrust Proportion (%) | Crude Odds Ratio (vs Entry-Level) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **< 2 years (Entry-Level Baseline)** | 654 | 785 | 50 | 1,489 | 43.92% | 1.000 (Reference) |
| **2–5 years** | 2,130 | 2,610 | 165 | 4,905 | 43.43% | 0.980 (95% CI: [0.869, 1.106]) |
| **6–10 years** | 3,425 | 3,920 | 245 | 7,590 | 45.13% | 1.050 (95% CI: [0.938, 1.176]) |
| **11–20 years** | 4,495 | 4,835 | 306 | 9,636 | 46.65% | 1.118 (95% CI: [1.002, 1.248]) |
| **21+ years (Veteran Engineers)** | **3,436** | **3,505** | **219** | **7,160** | **47.99%** | **1.178 (95% CI: [1.053, 1.318])** |
| **Total Qualified Sample** | **14,140** | **15,655** | **985** | **30,780** | **45.94%** | Pearson $\chi^2 = 38.39, p = 6.38 \times 10^{-6}$ |

---

### 2. Systems Language Stated Preference Patterns
In paired comparisons across respondents who answered both current and desired language questions ($N_{\text{paired}} = 27,079$):
- Rust: Current use $15.75\%$ ($4,264$) vs desired use $34.20\%$ ($9,260$) -> Net positive preference gap of $+18.45$ percentage points (Desire Ratio: $2.17$).
- Go: Current use $16.82\%$ ($4,554$) vs desired use $27.38\%$ ($7,414$) -> Net positive preference gap of $+10.56$ percentage points (Desire Ratio: $1.63$).
- JavaScript: Current use $66.09\%$ ($17,896$) vs desired use $39.07\%$ ($10,580$) -> Net negative preference gap of $-27.02$ percentage points (Desire Ratio: $0.59$).

---

### 3. Controlled Technology Salary Differentials (RQ2)
In extended Mincerian regression Model 3 ($N = 22,769, R^2 = 0.3846$), holding country (7 indicators), experience (linear and quadratic), and role (5 indicators) constant:

#### Table 11.2: Extended Mincerian Log-Wage Regression Output (Model 3)
| Explanatory Predictor | OLS Coeff ($\hat{\beta}$) | White HC1 Robust SE | White Robust $t$ | $p$-value ($P > \|t\|$) | Halvorsen-Palmquist Premium | 95% Robust Confidence Interval |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Intercept ($\beta_0$)** | 10.1245 | 0.0382 | 265.04 | $< 10^{-300}$ | — | [10.0496, 10.1994] |
| **YearsCodePro (Linear Return $\hat{\gamma}_1$)** | +0.06734 | 0.00240 | 28.06 | $< 10^{-170}$ | +6.97% / year | [+0.0626, +0.0720] |
| **YearsCodePro$^2$ (Deceleration $\hat{\gamma}_2$)**| -0.001150| 0.00007 | -16.43 | $< 10^{-60}$ | -0.11% / year$^2$ | [-0.00129, -0.00101] |
| **Docker (DevOps / Containerization)** | **+0.1237** | 0.01303 | 9.49 | $2.39 \times 10^{-21}$ | **+13.17%** | **[+10.31%, +16.10%]** |
| **Rust (Systems Programming)** | **+0.1203** | 0.01661 | 7.25 | $4.32 \times 10^{-13}$ | **+12.79%** | **[+9.18%, +16.52%]** |
| **AWS (Cloud Infrastructure)** | **+0.1036** | 0.01278 | 8.11 | $4.92 \times 10^{-16}$ | **+10.91%** | **[+8.17%, +13.72%]** |
| **TypeScript (Typed Frontend/Full-stack)** | **+0.0723** | 0.01236 | 5.85 | $4.86 \times 10^{-9}$ | **+7.50%** | **[+4.93%, +10.14%]** |
| **Go (Cloud Backend Systems)** | **+0.0686** | 0.01570 | 4.37 | $1.23 \times 10^{-5}$ | **+7.10%** | **[+3.86%, +10.45%]** |
| **Python (General Purpose / Analytics)** | +0.0131 | 0.01224 | 1.07 | 0.2857 *(Not Sig)* | +1.32% | [-1.09%, +3.79%] |

*Model Diagnostics:* $N = 22,769, R^2 = 0.3846$, Adjusted $R^2 = 0.3841$, White Heteroskedasticity Test $p < 0.001$.  
*Calculated Experience Peak:* $-\frac{\hat{\gamma}_1}{2\hat{\gamma}_2} = -\frac{0.06734}{2(-0.001150)} \approx \mathbf{29.3\text{ years}}$ of professional experience.

---

### 4. Autonomous AI Agents vs. Job Satisfaction (RQ3)
One-way ANOVA across 6 autonomous agent tiers on complete cases ($N = 23,766$) indicates statistical significance ($F(5, 23760) = 11.6172, p = 3.019 \times 10^{-11}$). However, the effect size is practically negligible:

#### Table 11.3: Autonomous AI Agent Workflow ANOVA Decomposition ($N = 23,766$)
| Source of Variance | Sum of Squares ($SS$) | Degrees of Freedom ($df$) | Mean Squares ($MS$) | Fisher’s $F$-ratio | $p$-value ($P > F$) | Effect Size Metrics |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Between Groups (Agent Tiers)** | 226.25 | 5 | 45.250 | **11.6172** | **$3.019 \times 10^{-11}$** | **Eta-Squared ($\eta^2$): 0.002439 (0.24%)** |
| **Within Groups (Residual Error)**| 92,545.99 | 23,760 | 3.895 | — | — | **Omega-Squared ($\omega^2$): 0.002229 (0.22%)** |
| **Total Variance** | **92,772.24** | **23,765** | — | — | — | **Cohen’s $d$: 0.128 (Negligible effect)** |

*Substantive Conclusion:* Statistical significance is an artifact of massive sample power ($N > 23,000$). The maximum observed satisfaction difference between daily AI agent users ($7.401$) and non-planners ($7.149$) is $+0.252$ points on a 10-point scale, confirming that AI agent integration does not meaningfully predict developer job satisfaction.

---

### 5. Remote Work Dynamics and Observational Attenuation (RQ4)
In the raw trimmed sample ($N = 23,177$), Remote respondents report a median salary of $\$91,198$ USD compared to $\$48,346.50$ USD for In-person respondents (a naive raw gap of $+88.6\%$). Under progressive econometric controls, this conditional difference attenuates substantially:

#### Table 11.4: Remote Work Compensation Attenuation Comparison
| Econometric Model Specification | Sample ($N$) | $R^2$ | Remote vs In-Person Differential | Hybrid vs In-Person Differential | Primary Confounder Controls Included |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Model A (Bivariate Naive)** | 23,177 | 0.0412 | **+88.63%** ($\hat{\beta} = +0.6346$) | +48.21% ($\hat{\beta} = +0.3935$) | None (Unadjusted observational gap) |
| **Model B (+ Experience & Country)** | 21,450 | 0.3789 | **+44.20%** ($\hat{\beta} = +0.3660$) | +38.12% ($\hat{\beta} = +0.3230$) | Geography (7 countries), Experience (quad) |
| **Model C (+ Firm Size Controls)** | **20,236** | **0.4254** | **+30.65%** ($\hat{\beta} = +0.267353$) | **+33.86% to +34.46%** ($\hat{\beta} \approx +0.294$) | **Geography, Experience, Organization Size** |

*Attenuation Mechanism:* Controlling for geographic clustering (remote staff situated in high-wage economies like the US) and firm size reduces the apparent remote wage differential from $+88.6\%$ down to $+30.65\%$, proving substantial confounding in unadjusted survey reporting.

---

### 6. Nonresponse Branch Association Audit
Audit of $15,411$ missing values on `RemoteWork` ($N = 49,191$) confirms an overwhelming association with respondent branch ($\chi^2 = 5,333.84, df = 5, p < 10^{-300}$, Cramér's $V = 0.3293$):

#### Table 11.5: Audited $6 \times 2$ Contingency Matrix of RemoteWork Missingness
| Respondent Professional Branch (`MainBranch`) | Answered RemoteWork ($N$) | Missing RemoteWork ($N$) | Row Total ($N$) | Missingness Rate (%) | Category Interpretation |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Developer by profession** | 28,286 | 9,181 | 37,467 | 24.50% | Primary employed software engineers |
| **Learning to code** | 552 | 2,033 | 2,585 | **78.65%** | Students without active employment |
| **Code as part of work/studies** | 3,172 | 1,722 | 4,894 | 35.19% | Academics, data scientists, researchers |
| **Hobbyist coder** | 530 | 1,394 | 1,924 | **72.45%** | Non-commercial recreational coders |
| **Former professional developer** | 642 | 683 | 1,325 | 51.55% | Retired or career-transitioned |
| **Developer support / adjacent** | 598 | 398 | 996 | 39.96% | Technical sales, solutions architects |
| **Total Sample Accounting** | **33,780** | **15,411** | **49,191** | **31.33%** | Reconciles perfectly to 49,191 total |

*Statistical Test Results:* Pearson $\chi^2 = 5,333.84, df = 5, p < 10^{-300}$, Cramér's $V = 0.3293$.  
*Approved Methodological Formulation:* RemoteWork nonresponse is associated with respondent branch. The observed association suggests that missingness is not Missing Completely At Random (MCAR) with respect to `MainBranch`. The available data alone cannot distinguish Missing At Random (MAR) from Missing Not At Random (MNAR).

---

---

## 12. Interactive Dashboard Pages and Functionality

The Streamlit web application is structured into four dedicated pages:

- **Executive Home Portal (`app/streamlit_app.py`):**
  - KPI tiles displaying raw extract count ($49,191$), official population ($49,009$), country representation ($177$), professional developer share ($76.2\%$), active AI adoption ($78.5\%$), and converted USD median salary ($\$75,320$).
  - Analytical roadmap portal linking to individual deep-dive pages.
- **Page 1: Overview (`app/pages/1_Overview.py`):**
  - High-level survey catalog and metadata.
  - Natural age distribution bar chart with exact modal share.
  - Formal education level (`EdLevel`) horizontal bar visualization.
  - Total coding experience versus professional work experience distribution moments.
  - Employment status breakdown and top 15 respondent countries.
- **Page 2: Response Analysis (`app/pages/2_Response_Analysis.py`):**
  - Programming language ranking with dual-denominator toggle.
  - Paired current-versus-desired language preference gap matrix ($N_{\text{paired}} = 27,079$).
  - Database and cloud infrastructure adoption rankings.
  - Four-tab AI adoption hierarchy (usage frequency, accuracy trust stance, general sentiment, and 6-tier autonomous agent spectrum).
- **Page 3: Segment Comparison (`app/pages/3_Segment_Comparison.py`):**
  - Cross-cohort compensation distributions across developer roles (including DevOps engineers).
  - Geographic compensation benchmarking across top 10 countries.
  - Quadratic experience gradients and career compensation peak.
  - Remote work salary attenuation analysis comparing raw medians to Model C econometric estimates.
- **Page 4: Data Quality (`app/pages/4_Data_Quality.py`):**
  - Ranked missingness bar chart across the top 20 survey attributes.
  - `RemoteWork` nonresponse branch association audit and contingency table.
  - Compensation sample flow funnel ($49,191 \to 23,947 \to 23,177 \to 22,769$).
  - Experience distribution moments comparison and cleaned dataset export utility.

---

## 13. Project Architecture and Directory Structure

```text
poll-results-visualizer/
|-- .github/
|   `-- workflows/
|       `-- tests.yml                     # GitHub Actions CI workflow (Python 3.10 and 3.11)
|-- .flake8                               # Flake8 linting configuration
|-- .gitignore                            # Excludes .venv, raw/processed data, scratch, caches
|-- .streamlit/
|   `-- config.toml                       # Streamlit server and theme configurations
|-- CONTRIBUTING.md                       # Open-source contribution guidelines
|-- LICENSE                               # MIT License for application source code
|-- README.md                             # Comprehensive project documentation
|-- app/                                  # Streamlit presentation tier
|   |-- __init__.py
|   |-- data_provider.py                  # Cached data loading (@st.cache_data)
|   |-- streamlit_app.py                  # Main entry point and executive landing page
|   |-- components/                       # Reusable UI components
|   |   |-- __init__.py
|   |   |-- charts.py                     # Plotly chart builders with dual denominators
|   |   |-- filters.py                    # Demographic slicers (country, experience, salary)
|   |   |-- kpi_cards.py                  # Executive KPI metric tiles
|   |   `-- theme.py                      # Centralized Light/Dark theme manager, CSS, and chart styling
|   `-- pages/                            # Multi-page dashboard views
|       |-- 1_Overview.py                 # Demographics, age, education, and experience
|       |-- 2_Response_Analysis.py        # Languages, stated preferences, cloud, and AI
|       |-- 3_Segment_Comparison.py       # Roles, geos, experience curves, and remote work
|       `-- 4_Data_Quality.py             # Missingness rankings, sample flow, and governance
|-- data/
|   |-- processed/
|   |   `-- .gitkeep                      # Destination for survey_results_cleaned.parquet
|   |-- raw/
|   |   `-- .gitkeep                      # Destination for official Stack Overflow survey CSVs
|   `-- sample/
|       `-- .gitkeep                      # Sample data directory placeholder
|-- docs/                                 # Technical architecture and career documentation
|   |-- DATA_DICTIONARY.md                # Survey attributes schema and derived feature specs
|   |-- DATA_SOURCE_ATTRIBUTION.md        # ODbL 1.0 licensing and database provenance
|   |-- EXECUTION_LOG.md                  # Chronological implementation ledger (Phases 1 to 8)
|   |-- INTERVIEW_PREPARATION.md          # 16 advanced technical and econometric interview Q&As
|   |-- METHODOLOGY.md                    # Data quality rules and mathematical derivations
|   |-- PORTFOLIO_PRESENTATION_GUIDE.md   # Resume bullets, STAR stories, and LinkedIn drafts
|   |-- PROJECT_ARCHITECTURE.md           # System design, data flow, and module contracts
|   |-- PROJECT_OVERVIEW.md               # Scope, background, and delivery boundaries
|   `-- USER_GUIDE.md                     # Step-by-step setup and operational run guide
|-- images/
|   `-- .gitkeep                          # Destination for dashboard screenshot PNGs
|-- notebooks/                            # Jupyter exploration and modeling notebooks
|   |-- 01_data_exploration.ipynb         # 10-section survey exploratory data analysis
|   |-- 02_analysis_deep_dive.ipynb       # Econometric modeling, VIF, and ANOVA notebook
|   `-- 02_analysis_experiments.ipynb     # Early exploratory validation notebook
|-- outputs/                              # Analytical artifacts and summary metrics
|   |-- analysis_summary_metrics.json     # Machine-readable Phase 5 statistical results
|   |-- eda_summary_metrics.json          # Machine-readable Phase 4 EDA metrics
|   |-- charts/
|   |   `-- .gitkeep
|   |-- exports/
|   |   `-- .gitkeep
|   `-- logs/
|       `-- .gitkeep
|-- pytest.ini                            # Pytest configuration settings
|-- reports/                              # Formal research, audit, and strategy reports
|   |-- analysis_report.md                # Econometric modeling, White HC1, and VIF proofs
|   |-- data_cleaning_report.md           # Deterministic hygiene and Parquet derivation ledger
|   |-- data_quality_report.md            # Dataset sparsity, uniqueness, and format audit
|   |-- eda_report.md                     # Comprehensive 10-section empirical findings report
|   |-- key_insights_report.md            # 5 evidence-grounded strategic findings
|   |-- project_report.md                 # Master comprehensive project report
|   `-- recommendations_report.md         # Stakeholder recommendation matrix
|-- requirements.txt                      # Core production dependencies
|-- requirements-dev.txt                  # Development, linting, and testing dependencies
|-- run.py                                # Convenience launcher script
|-- src/                                  # Core business logic and statistical engines
|   |-- __init__.py
|   |-- analysis.py                       # OLS regression, White HC1, VIF, Chi2, and ANOVA
|   |-- config.py                         # Paths, schemas, and system constants
|   |-- data_cleaning.py                  # Deduplication and schema transformation
|   |-- data_loader.py                    # Dataset loading and public adapter bridge
|   |-- data_validation.py                # Schema validation and anomaly detection
|   |-- export.py                         # File export utilities
|   |-- insights.py                       # Non-causal descriptive narrative generator
|   `-- datasets/                         # Source-specific dataset adapters
|       |-- __init__.py
|       |-- stackoverflow_2025.py         # Stack Overflow survey loader and aggregators
|       `-- stackoverflow_cleaning.py     # Cleaning pipeline and numeric experience derivation
`-- tests/                                # Automated unit test suite (116 tests: 115 passed, 1 skipped)
    |-- __init__.py
    |-- test_analysis.py                  # Statistical engine unit tests
    |-- test_dashboard_components.py      # Streamlit charts, filters, and KPI tests
    |-- test_data_cleaning.py             # Data cleaning pipeline tests
    |-- test_data_loader.py               # Loader resilience tests
    |-- test_data_validation.py           # Schema validator tests
    |-- test_export.py                    # Export format tests
    |-- test_insights.py                  # Narrative generation and Phase 7 integrity tests
    |-- test_stackoverflow_2025.py        # Adapter and multi-select aggregation tests
    |-- test_stackoverflow_cleaning.py    # Experience parsing and Parquet derivation tests
    |-- test_statistical_engine_validation.py # Independent closed-form mathematical proofs
    `-- test_theme.py                     # Centralized theme architecture, state lifecycle, and chart tests
```

---

## 14. Technology Stack

| Component | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Runtime Language** | Python | 3.10 / 3.11 | Core execution environment |
| **Data Manipulation** | Pandas | >= 2.2.0 | Vectorized tabular operations and aggregations |
| **Numerical Computing** | NumPy | >= 1.26.0 | Matrix algebra, OLS estimation, and arrays |
| **Presentation Tier** | Streamlit | >= 1.40.0 | Multi-page interactive web application |
| **Interactive Plotting** | Plotly | >= 5.24.0 | Declarative charts with custom dual hover data |
| **Columnar Storage** | Apache Parquet (PyArrow) | >= 15.0.0 | Compressed high-performance columnar serialization |
| **Statistical Engine** | Pure Python / NumPy | Built-in | OLS, White HC1 robust covariance, VIF, Chi2, ANOVA |
| **Unit Testing** | pytest | >= 8.0.0 | Test automation and assertion validation |
| **Code Quality** | Flake8 | >= 7.0.0 | PEP 8 style guide enforcement and linting |
| **CI / CD Pipeline** | GitHub Actions | v4 / v5 | Automated multi-version test and lint runner |

---

## 15. Installation Prerequisites

Before installing the project locally, verify that you have:
1. Windows 10 or Windows 11 (64-bit).
2. Python 3.10 or Python 3.11 installed. Verify in PowerShell using:
   ```powershell
   python --version
   ```
3. Git installed and accessible in your command path. Verify using:
   ```powershell
   git --version
   ```

---

## 16. Step-by-Step Local Setup Instructions for Windows

Open Windows PowerShell and navigate to your intended project directory:

```powershell
# 1. Clone the repository
git clone https://github.com/AkashDas-AI/Poll-Results-Visualizer.git
cd "Poll-Results-Visualizer"

# 2. Create a local isolated virtual environment
python -m venv .venv

# 3. Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# If script execution is restricted on Windows, allow local execution:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install production and development dependencies
pip install -r requirements-dev.txt
```

---

## 17. Instructions for Obtaining the Official Survey Dataset

Because the Stack Overflow Developer Survey dataset is published under the Open Database License (ODbL) v1.0 and is approximately 140 MB uncompressed, the raw and processed survey data files are excluded from the Git repository.

Follow these steps to obtain and place the official dataset:

1. Visit the official Stack Overflow survey download portal:
   [https://survey.stackoverflow.co/2025/](https://survey.stackoverflow.co/2025/)
2. Download the 2025 survey archive (`stack-overflow-developer-survey-2025.zip`).
3. Extract the archive contents into the project directory at:
   `data/raw/stackoverflow_developer_survey_2025/`
4. Confirm that the following two source files are present:
   - `data/raw/stackoverflow_developer_survey_2025/survey_results_public.csv` (SHA-256: `2d1f6530...`)
   - `data/raw/stackoverflow_developer_survey_2025/survey_results_schema.csv` (SHA-256: `1d24951e...`)

---

## 18. Instructions for Running the Data Pipeline

Once the raw CSV files are placed in `data/raw/stackoverflow_developer_survey_2025/`, execute the deterministic data cleaning and Parquet derivation pipeline:

```powershell
# Ensure .venv is active
.\.venv\Scripts\Activate.ps1

# Run the cleaning pipeline
python -m src.datasets.stackoverflow_cleaning
```

### Expected Pipeline Output:
- Reads 49,191 raw survey records across 172 columns.
- Derives clean numeric variables: `YearsCode_num`, `WorkExp_num`, `Comp_valid_usd`, `Comp_status`.
- Normalizes delimiters across 78 multi-select columns.
- Writes optimized Apache Parquet file:
  `data/processed/survey_results_cleaned.parquet` (SHA-256: `16f5ce8e...`, 9.8 MB).
- Writes matching CSV backup:
  `data/processed/survey_results_cleaned.csv` (49,191 rows, 176 columns).

---

## 19. Instructions for Launching the Streamlit Application

With the cleaned Parquet file present, launch the interactive dashboard:

```powershell
# Option A: Direct Streamlit module launch via project-local .venv
.\.venv\Scripts\python.exe -m streamlit run app/streamlit_app.py

# Option B: Via convenience runner script
python run.py
```

Open your web browser and navigate to:
`http://localhost:8501`

Use the left sidebar navigation to switch between the Overview, Response Analysis, Segment Comparison, and Data Quality pages, and use the **"🎨 Display Theme"** radio toggle to switch between Dark and Light display modes.

---

## 20. Testing and Linting Instructions

Execute the automated test and linting suites using the project virtual environment:

```powershell
# Run the complete test suite (116 total test items)
.\.venv\Scripts\pytest

# Run tests with verbose output and duration profiling
.\.venv\Scripts\pytest -v --durations=10

# Verify strict PEP 8 code quality across all project modules
.\.venv\Scripts\flake8 app src tests tools
```

### Quality Gate Standards:
- **Pytest:** 115 passed, 1 skipped out of 116 tests (100% core pass rate in ~10s).
- **Flake8:** 0 errors and 0 warnings across all application, source, test, and tool modules.
- **CI Parity:** Local test commands match the automated GitHub Actions workflow (`.github/workflows/tests.yml`).

---

## 21. Methodological Limitations and Responsible Interpretation

When evaluating findings from this survey, adhere to the following analytical boundaries:

1. Self-Selected Convenience Sampling: The survey represents an opt-in convenience sample of developer community members who visited Stack Overflow. It cannot be interpreted as a randomized probability sample of the global developer population.
2. Self-Reported Financial Data: Compensation figures are self-reported and unverified against payroll or tax records. Figures are converted to USD using official spot exchange rates recorded on June 25, 2025, and do not account for local Purchasing Power Parity (PPP).
3. Cross-Sectional Non-Causal Nature: The survey is a single cross-sectional observational snapshot collected in May-June 2025. Regression coefficients measure conditional statistical associations holding covariates constant; they must never be interpreted as individual causal returns or temporal career migrations.
4. Survey Nonresponse Boundaries: Nonresponse is associated with developer branch, but the public schema does not publish internal routing or branching code. Analysts must avoid asserting unverified routing claims.

---

## 22. Licensing and Attribution

This repository enforces a strict dual-licensing structure:

- **Application Source Code:**
  All custom Python algorithms, statistical routines, data cleaning scripts, Streamlit pages, Plotly chart components, and unit tests authored by Akash Das are licensed under the [MIT License](LICENSE).
- **Survey Dataset Attribution:**
  Data from the 2025 Stack Overflow Annual Developer Survey is copyright (c) Stack Exchange, Inc. and is licensed under the [Open Database License (ODbL) v1.0](docs/DATA_SOURCE_ATTRIBUTION.md), with database contents licensed under the [Database Contents License (DbCL) v1.0](docs/DATA_SOURCE_ATTRIBUTION.md).

---

## 23. Author Information

- **Author:** Akash Das
- **Role:** Data Science, Data Analytics, and Business Intelligence Candidate
- **Project Role:** Solo Author, Data Engineer, and Econometric Modeling Analyst
- **Academic Context:** Data Science / Analytics Intern Portfolio Project

---

## 24. Professional Profiles and Contact

- **GitHub Repository:** [https://github.com/AkashDas-AI/Poll-Results-Visualizer](https://github.com/AkashDas-AI/Poll-Results-Visualizer)
- **LinkedIn Profile:** [https://www.linkedin.com/in/placeholder](https://www.linkedin.com/in/placeholder)
- **Portfolio Website:** [https://placeholder.github.io](https://placeholder.github.io)

For questions, feedback, or collaborative inquiries regarding this analysis, please open an issue in the GitHub repository.
