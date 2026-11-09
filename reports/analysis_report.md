# Stack Overflow Developer Survey 2025: Econometric and Statistical Analysis Report

**Project Name:** Poll Results Visualizer  
**Project Author:** Akash Das  
**Milestone:** Phase 5 of 8 — Analysis (Methodological Review & Statistical Corrections Pass)  
**Status:** Completed, Independently Validated & Empirically Verified  
**Primary Dataset Input:** `data/processed/survey_results_cleaned.parquet` (49,191 rows × 176 columns, Snappy Parquet, SHA-256: `16f5ce8e8f387405fa9635e44074dc468f44b82c0ee23287b2889be238fbbe52`)  
**Supporting Artifacts:** `src/analysis.py`, `tests/test_analysis.py`, `tests/test_statistical_engine_validation.py`, `notebooks/02_analysis_deep_dive.ipynb`, `outputs/analysis_summary_metrics.json`  

---

## 1. Executive Summary & Core Insights Matrix

This report presents a methodologically audited, reproducible statistical and econometric investigation into four central research questions regarding the global software development industry. All models, test statistics, robust standard errors, and multiple testing corrections were estimated using the pure-Python mathematical engine in `src/analysis.py` directly against the canonical cleaned Parquet dataset, and independently validated against closed-form mathematical benchmarks.

### Core Empirical Findings Matrix

| Research Question | Focus & Analytical Sample | Statistical Method & Diagnostics | Key Empirical Estimate (with Uncertainty Interval) | Substantive Observational Interpretation |
| :--- | :--- | :--- | :--- | :--- |
| **RQ1: AI Trust Dynamics** | Reported accuracy trust (`AIAcc`, $N=33,297$) across career seniority & language stacks | Pearson $\chi^2$, crude Odds Ratios (Wald 95% CIs), Benjamini–Hochberg FDR adjustments | **Seniority:** Veteran crude $OR = 1.178$ $[1.053, 1.318]$ ($p = 0.0043$) vs. entry. **Rust Users:** Distrust $63.63\%$ ($OR = 2.196$ $[2.059, 2.343]$, BH FDR $p < 10^{-120}$). | Experienced developers exhibit higher crude odds of distrust. Stated use of strict systems programming languages (Rust, C++, Go) is strongly and positively associated with reported distrust. |
| **RQ2: Tech Compensation** | Specialized tech associations on $\ln(\text{Salary})$ ($N=22,769$ qualified earners) | Multivariable Mincerian OLS, White HC1 robust SEs, Breusch-Pagan test, FDR control | **Docker:** $+13.17\%$ $[+10.31\%, +16.10\%]$ (Robust $t=9.49, p < 10^{-20}$). **Rust:** $+12.79\%$ $[+9.18\%, +16.52\%]$ (Robust $t=7.25, p < 10^{-12}$). **AWS:** $+10.91\%$ $[+8.17\%, +13.72\%]$. **TypeScript:** $+7.50\%$ $[+4.93\%, +10.14\%]$. **Go:** $+7.10\%$ $[+3.86\%, +10.45\%]$. **Python:** $+1.32\%$ $[-1.09\%, +3.79\%]$ (Robust $t=1.07$, n.s.). | Raw salary differences attenuate sharply under controls. Systems assets (Docker, Rust, AWS, TypeScript, Go) retain positive conditional compensation associations; Python shows no statistically significant conditional difference ($p = 0.2857$). |
| **RQ3: AI Agent Outcomes** | 6-tier adoption of AI agents (`AIAgents`, $N=31,919$) vs. sentiment & `JobSat` ($N=23,766$) | One-way ANOVA, $\eta^2$, $\omega^2$, post-hoc Bonferroni tests, $2 \times 2$ sentiment OR audit | **Favorable Sentiment:** Daily users $90.73\%$ ($OR = 21.292$ $[19.114, 23.719]$). **JobSat:** Daily mean $7.401$ vs. Non-planner $7.149$ (Diff $= +0.252$, Bonferroni $p < 10^{-9}$). | Daily agent adoption is strongly associated with favorable sentiment. The $+0.252$-point difference in job satisfaction is statistically significant, but the practical effect size is small ($\eta^2 = 0.0024$, Cohen's $d = 0.128$). |
| **RQ4: Remote Work Dynamics** | Conditional wage differences across `RemoteWork` ($N=20,236$) controlling for OrgSize & Country | Non-response branch audit, three-stage OLS with HC1 robust SEs, sensitivity analysis | **Fully Remote:** $+30.65\%$ $[+25.27\%, +36.26\%]$ (Robust $t=12.46, p < 10^{-34}$) vs. In-person reference category in Model C ($R^2 = 0.4254$). | RemoteWork nonresponse is associated with respondent branch; missingness is not MCAR with respect to MainBranch. In-person developers exhibit an unadjusted and adjusted conditional compensation deficit. |

---

## 2. Research Question 1 (RQ1): AI Trust Dynamics & Developer Characteristics

### 2.1 Reconciled Sample Flow & Active AI-User Accounting
A critical objective of this review pass is formally reconciling historical counts between general AI usage (`AISelect`) and perceived AI output accuracy (`AIAcc`).

In the preliminary Phase 5 briefing, an ad-hoc filter combining autonomous agent adoption (`AIAgents`) and AI education (`LearnCodeAI`) resulted in an undercounted figure of $19,733$ respondents. As established during Phase 4 Exploratory Data Analysis, the canonical survey instrument measuring active AI tool usage is question `AISelect`: *"Do you currently use AI tools in your development process?"*

Active AI tool users are formally defined as respondents selecting:
1. *"Yes, I use AI tools daily"* ($N = 15,883$)
2. *"Yes, I use AI tools weekly"* ($N = 5,958$)
3. *"Yes, I use AI tools monthly or infrequently"* ($N = 4,628$)

#### Table 1.1: Complete Analytical Sample-Flow Accounting

| Stage / Filter | Survey Instrument | Sample Count ($N$) | % of Total Survey | Subpopulation % | Methodological Note |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **1. Total Survey Respondents** | Full microdata | 49,191 | 100.00% | — | Canonical raw CSV & processed Parquet row count |
| **2. AISelect Answered** | `AISelect` non-null | 33,720 | 68.55% | 100.00% | Respondents completing the general AI gateway module |
| *— AISelect Missing* | `AISelect` is null | 15,471 | 31.45% | — | Non-respondents or survey dropouts prior to AI section |
| **3. Active AI Tool Users** | `AISelect` (Daily, Weekly, Monthly) | 26,469 | 53.81% | 78.49% | Active user population established in Phase 4 EDA |
| **4. AIAcc Answered** | `AIAcc` non-null | 33,297 | 67.69% | 100.00% | Primary analytical denominator for AI trust analysis |
| *— AIAcc Missing* | `AIAcc` is null | 15,894 | 32.31% | — | Non-respondents to accuracy trust question |
| **5. Active AI Users Answering AIAcc** | `AISelect` active $\cap$ `AIAcc` non-null | **26,126** | **53.11%** | **78.46%** | **Reconciled Phase 4 subpopulation ($15,662$ daily, $5,901$ weekly, $4,563$ monthly)** |
| *— Active AI Users Skipping AIAcc* | `AISelect` active $\cap$ `AIAcc` is null | 343 | 0.70% | 1.30% | Active AI users who skipped the specific trust question |
| **6. Non-Active AI Users Answering AIAcc** | `AISelect` non-active $\cap$ `AIAcc` non-null | 7,171 | 14.58% | 21.54% | $5,380$ non-planners, $1,754$ planners, $37$ missing `AISelect` |
| **7. Seniority Complete Cases** | `AIAcc` non-null $\cap$ `WorkExp_num` non-null | 30,780 | 62.57% | 92.44% | Complete cases for career experience cross-tabulations |
| **8. Language Complete Cases** | `AIAcc` non-null $\cap$ `LanguageHaveWorkedWith` non-null | 30,681 | 62.37% | 92.14% | Complete cases for programming language cross-tabulations |

### 2.2 Audit of Seniority Brackets & Contingency Structure (5x3 vs. 5x2)
Among the $N = 30,780$ complete cases with valid career experience (`WorkExp_num`) and trust ratings (`AIAcc`), we evaluate career seniority across two distinct statistical formulations:

#### 1. Global 5x3 Contingency Table (Independence Test)
- **Predictor:** 5 standardized career cohorts (`WorkExp_bracket`: Entry <2 yrs, Junior 2–5 yrs, Mid 6–10 yrs, Senior 11–20 yrs, Veteran 21+ yrs).
- **Outcome Variable:** 3-tier trust classification (`AIAcc_tier`: Distrust, Neutral, Trust).
- **Degrees of Freedom:** $df = (r - 1)(c - 1) = (5 - 1)(3 - 1) = 4 \times 2 = \mathbf{8}$.
- **Statistical Test:** Pearson $\chi^2 = \mathbf{38.39}$, $df = 8$, $p = \mathbf{6.38 \times 10^{-6}}$, Cramér's $V = \mathbf{0.025}$.

#### Table 1.2a: Global 5x3 Contingency Table: Observed [Expected] Frequencies ($N = 30,780$)

| Career Seniority Bracket | Distrust ($n$ [Exp]) | Neutral ($n$ [Exp]) | Trust ($n$ [Exp]) | Total Bracket ($n$) | % Distrust |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. <2 years (Entry)** | 654 [678.81] | 313 [322.91] | 522 [487.29] | 1,489 | 43.92% |
| **2. 2 to 5 years (Junior)** | 2,784 [2,920.83] | 1,427 [1,389.43] | 2,196 [2,096.74] | 6,407 | 43.45% |
| **3. 6 to 10 years (Mid)** | 3,096 [3,103.18] | 1,452 [1,476.18] | 2,259 [2,227.64] | 6,807 | 45.48% |
| **4. 11 to 20 years (Senior)** | 4,062 [4,065.09] | 1,930 [1,933.75] | 2,925 [2,918.16] | 8,917 | 45.55% |
| **5. 21+ years (Veteran)** | 3,436 [3,264.10] | 1,553 [1,552.73] | 2,171 [2,343.17] | 7,160 | 47.99% |
| **Total Global Sample** | **14,032 [14,032.0]** | **6,675 [6,675.0]** | **10,073 [10,073.0]** | **30,780** | **45.59%** |

#### 2. Collapsed 5x2 Contingency Table & Crude Odds Ratios
To evaluate binary skepticism, the outcome is collapsed into Distrust (Somewhat distrust + Highly distrust) vs. Not Distrust (Trust + Neutral).
- **Degrees of Freedom:** $df = (r - 1)(c - 1) = (5 - 1)(2 - 1) = 4 \times 1 = \mathbf{4}$.
- **Statistical Test:** Pearson $\chi^2 = \mathbf{30.12}$, $df = 4$, $p = \mathbf{4.63 \times 10^{-6}}$, Cramér's $V = \mathbf{0.031}$.
- **Reference Group:** Entry-level engineers (<2 years experience, $N = 1,489$).
- **Crude Odds Ratio Formula:** For group $j$ with cell counts $a$ (distrust) and $b$ (not distrust) vs. baseline $c$ (distrust) and $d$ (not distrust):
  $$\text{OR} = \frac{a \cdot d}{b \cdot c}, \quad SE(\ln(\text{OR})) = \sqrt{\frac{1}{a} + \frac{1}{b} + \frac{1}{c} + \frac{1}{d}}, \quad 95\%\text{ CI} = \exp(\ln(\text{OR}) \pm 1.95996 \cdot SE)$$

#### Table 1.2b: Collapsed 5x2 Seniority Contingency Table and Crude Odds Ratios ($N = 30,780$)

| Career Seniority Bracket | Total $n$ | Distrust Count ($a$) [Exp] | Not Distrust Count ($b$) [Exp] | % Distrust | Crude Odds Ratio | 95% Wald Confidence Interval | $SE(\ln(\text{OR}))$ | $z$-statistic | Two-Tailed $p$-value |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. <2 years (Entry)** | 1,489 | 654 [678.81] | 835 [810.19] | 43.92% | **1.000** *(Baseline)* | — | — | — | — |
| **2. 2 to 5 years (Junior)** | 6,407 | 2,784 [2,920.83] | 3,623 [3,486.17] | 43.45% | **0.981** | [0.876, 1.099] | 0.0580 | -0.33 | 0.7420 |
| **3. 6 to 10 years (Mid)** | 6,807 | 3,096 [3,103.18] | 3,711 [3,703.82] | 45.48% | **1.065** | [0.951, 1.192] | 0.0576 | 1.10 | 0.2731 |
| **4. 11 to 20 years (Senior)** | 8,917 | 4,062 [4,065.09] | 4,855 [4,851.91] | 45.55% | **1.068** | [0.956, 1.193] | 0.0564 | 1.17 | 0.2418 |
| **5. 21+ years (Veteran)** | 7,160 | 3,436 [3,264.10] | 3,724 [3,895.90] | 47.99% | **1.178** | **[1.053, 1.318]** | 0.0573 | 2.86 | **0.0043** |
| **Total Complete Cases** | **30,780** | **14,032 [14,032.0]** | **16,748 [16,748.0]** | **45.59%** | — | — | — | — | — |

- **Methodological Reconciliation:** The global test ($df = 8, \chi^2 = 38.39, p = 6.38 \times 10^{-6}$) tests the omnibus hypothesis that 3-tier trust distributions vary across the 5 experience cohorts. The collapsed binary test ($df = 4, \chi^2 = 30.12, p = 4.63 \times 10^{-6}$) specifically tests whether binary distrust rates vary across cohorts, providing the analytical basis for the crude odds ratios.
- **Substantive Observational Finding:** Veteran developers with over two decades of professional software engineering tenure exhibit a statistically significant elevation in crude odds of distrusting AI output accuracy relative to entry-level developers ($OR = 1.178, p = 0.0043$). Junior, mid-level, and senior brackets do not differ significantly from the entry baseline.

### 2.3 Programming Language Associations & Multiple Testing Control
We audit the relationship between stated programming language use in `LanguageHaveWorkedWith` and reported AI distrust among $N = 30,681$ complete cases.
To guard against false discoveries across the family of $m = 6$ hypothesis tests, we report:
1. **Raw Two-Tailed $p$-values** from Pearson's $\chi^2$ test ($df = 1$).
2. **Benjamini–Hochberg (BH) False Discovery Rate (FDR) Adjusted $p$-values**.
3. **Bonferroni Family-Wise Adjusted $p$-values**.

#### Table 1.3: Programming Language Distrust Associations with Multiple Testing Corrections

| Language Stack | Stack Users ($n_1$) | User Distrust ($a$) | User % Distrust | Non-Users ($n_0$) | Non-User Distrust ($c$) | Non-User % Distrust | Crude Odds Ratio | 95% Wald Confidence Interval | Pearson $\chi^2$ ($df=1$) | Raw Two-Tailed $p$-value | Benjamini–Hochberg FDR $p$-value | Bonferroni Adjusted $p$-value |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Rust** | 4,614 | 2,936 | **63.63%** | 26,067 | 11,558 | 44.34% | **2.196** | **[2.059, 2.343]** | 585.43 | $2.47 \times 10^{-129}$ | **$1.48 \times 10^{-128}$** | **$1.48 \times 10^{-128}$** |
| **C++** | 7,252 | 3,963 | **54.65%** | 23,429 | 10,531 | 44.95% | **1.476** | **[1.400, 1.556]** | 208.99 | $2.28 \times 10^{-47}$ | **$6.84 \times 10^{-47}$** | **$1.37 \times 10^{-46}$** |
| **Go** | 5,072 | 2,685 | **52.94%** | 25,609 | 11,809 | 46.11% | **1.314** | **[1.237, 1.396]** | 79.12 | $5.84 \times 10^{-19}$ | **$1.17 \times 10^{-18}$** | **$3.51 \times 10^{-18}$** |
| **JavaScript** | 20,427 | 9,376 | **45.90%** | 10,254 | 5,118 | 49.91% | **0.851** | **[0.812, 0.893]** | 44.09 | $3.13 \times 10^{-11}$ | **$4.70 \times 10^{-11}$** | **$1.88 \times 10^{-10}$** |
| **TypeScript** | 13,495 | 6,193 | **45.89%** | 17,186 | 8,301 | 48.30% | **0.908** | **[0.868, 0.950]** | 17.61 | $2.71 \times 10^{-5}$ | **$3.25 \times 10^{-5}$** | **$1.62 \times 10^{-4}$** |
| **Python** | 17,902 | 8,622 | **48.16%** | 12,779 | 5,872 | 45.95% | **1.093** | **[1.044, 1.144]** | 14.64 | $1.30 \times 10^{-4}$ | **$1.30 \times 10^{-4}$** | **$7.82 \times 10^{-4}$** |

- **Descriptive Observational Interpretation:** Stated use of strict systems programming languages (Rust, C++, Go) is strongly and positively associated with reported distrust in AI accuracy, whereas dynamic web languages (JavaScript, TypeScript) exhibit lower crude odds of distrust relative to non-users.
- **Language Correction:** We strictly avoid causal assertions that programming languages "drive" skepticism. Rather, developers in systems engineering environments—where borrow checkers, memory layouts, and strict type constraints reject invalid code at compile time—encounter technical friction when LLMs hallucinate non-existent APIs or syntax, correlating with higher reported distrust.

---

## 3. Research Question 2 (RQ2): Compensation and Technology Associations

### 3.1 Econometric Specification & Complete-Case Filtering
To evaluate conditional compensation differences across specialized technologies, we estimate a Mincerian OLS regression model on natural log annual compensation:

$$\ln(\text{Salary}_i) = \beta_0 + \sum_{k=1}^6 \beta_k \text{Tech}_{ki} + \gamma_1 \text{WorkExp}_i + \gamma_2 \text{WorkExp}_i^2 + \sum_{j=1}^7 \delta_j \text{Country}_{ji} + \sum_{m=1}^5 \lambda_m \text{DevType}_{mi} + \varepsilon_i$$

#### Model Parameters & Complete-Case Rules:
- **Dependent Variable:** Natural log of annual converted compensation in USD ($\ln(\text{ConvertedCompYearly})$).
- **Salary Retention Rate & Tail Trimming:** Among qualified survey respondents with valid positive annual compensation ($N = 23,947$), trimming the extreme tails at $\$1,000$ and $\$1,000,000$ USD removes $724$ low records ($3.02\%$) and $46$ high records ($0.19\%$), totaling $770$ trimmed observations ($3.22\%$) and retaining $N = 23,177$ records (exact retention rate: $96.78\% \approx 96.8\%$). After listwise deletion of missing values across regressors, the estimation sample comprises $N = 22,769$ complete cases.
- **Technology Indicators (6 Binary Variables):** Rust, Go, Python, TypeScript (from `LanguageHaveWorkedWith`), AWS, Docker (from `PlatformHaveWorkedWith`).
- **Human Capital Terms:** Linear professional experience (`WorkExp_num`) and quadratic experience ($\text{WorkExp\_num}^2$) to capture diminishing marginal returns to tenure.
- **Geographic Controls (Top 7 Countries):** United States of America, Germany, United Kingdom, Canada, India, France, Netherlands (Reference category: "Other").
- **Developer Role Controls (Top 5 Roles):** Full-stack developer, Back-end developer, Front-end developer, Engineering manager, DevOps engineer or professional (Reference category: "Other").
- **Design Matrix Dimensions & Degrees of Freedom:** The model comprises $k = 20$ explanatory variables ($6$ technology indicators, $2$ experience terms, $7$ country indicators, $5$ developer role indicators) and $p = k + 1 = 21$ estimated parameters including Intercept. Sample size is $N = 22,769$, yielding $df_{\text{model}} = 20$ and residual degrees of freedom $df_{\text{residual}} = n - p = 22,769 - 21 = 22,748$.
- **Percentage Conversion Formula:** Coefficients are converted to percentage differences using the exact semi-logarithmic formula:
  $$\%\Delta = 100 \times (e^{\hat{\beta}} - 1)$$
- **Methodological Status:** All estimates represent **conditional compensation associations among surveyed respondents, controlling for the specified covariates**. They are **not causal technology premiums or genuine market returns**.

### 3.2 Model Diagnostics, Leverage, Influence & Sensitivity Analysis
- **Goodness-of-Fit:** $R^2 = 0.3846$, Adjusted $R^2 = 0.3840$.
- **Test Statistic Clarification:** The overall model test statistic reported ($F(20, 22748) = 710.77, p < 10^{-300}$) is the **conventional OLS $F$-statistic** ($F = \frac{R^2 / k}{(1 - R^2) / (n - p)}$ with $k = 20, p = 21$), not a robust Wald test.
- **Residual Standard Error ($s_e$):** $0.8396$ log points on $df_{\text{residual}} = 22,748$ residual degrees of freedom.
- **Breusch-Pagan Test for Heteroskedasticity:**
  $$\text{Auxiliary Regression: } e_i^2 = \alpha_0 + X_i \alpha + u_i \implies LM = n \cdot R_{\text{aux}}^2 = 2,269.63, \quad df = 20, \quad p < 10^{-300}$$
  *Diagnostic Implication:* The null hypothesis of homoskedasticity is decisively rejected ($p < 10^{-300}$). Conventional OLS standard errors are biased. Consequently, **White HC1 heteroskedasticity-robust standard errors** (MacKinnon & White 1985) are mandatory:
  $$\text{Var}_{\text{HC1}}(\hat{\beta}) = (X^T X)^{-1} \left[ X^T \text{diag}\left(e_i^2 \cdot \frac{n}{n-p}\right) X \right] (X^T X)^{-1}$$
- **Leverage Diagnostics:** Using the standard threshold $h_{ii} > \frac{2p}{n} = \frac{2(21)}{22,769} = 0.001845$, exactly $1,797$ observations ($7.89\%$) exhibit elevated leverage (min $h_{ii} = 0.000271$, max $h_{ii} = 0.073703$).
- **Cook's Distance Distribution:**
  $$D_i = \frac{e_i^2}{p \cdot s^2} \left[ \frac{h_{ii}}{(1 - h_{ii})^2} \right]$$
  - Cutoff threshold: $4/n = 4 / 22,769 = 0.000175677 \approx 1.76 \times 10^{-4}$ (alternative: $4/(n - p) = 1.758 \times 10^{-4}$).
  - Distribution: Min = $1.08 \times 10^{-14}$, 25th percentile = $1.80 \times 10^{-6}$, Median = $8.35 \times 10^{-6}$, 75th percentile = $2.86 \times 10^{-5}$, Mean = $8.63 \times 10^{-5}$, Max = $0.405230$.
  - Observations exceeding $4/n$: Exactly $1,039$ observations ($4.56\%$).
- **Sensitivity Analysis (Diagnostic Screening Re-estimation):**
  Observations with Cook's distance exceeding $4/n = 4 / 22,769 \approx 1.76 \times 10^{-4}$ ($1,039$ observations, $4.56\%$) exceed a diagnostic screening threshold; they are not characterized as invalid records or errors. Re-estimating Model 3 on the subset within this threshold ($N = 21,730$, $R^2 = 0.4845$, Clean $F = 1,020.2$) is conducted strictly as an exploratory sensitivity analysis, not as a definitive or inherently cleaner model.

#### Table 2.0: Regression Sensitivity Analysis: Full Sample vs. Diagnostic Screened Sample ($D_i \le 4/n$)

| Technology Covariate | Full Model $\hat{\beta}$ ($N=22,769$) | Full HC1 SE | Screened Model $\hat{\beta}$ ($N=21,730$) | Screened HC1 SE | Coefficient $\%\Delta$ | Robust Significance Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Rust** | **+0.1203** | 0.0166 | **+0.1217** | 0.0123 | +1.17% | Preserved ($p < 10^{-22}$) |
| **Docker** | **+0.1237** | 0.0130 | **+0.0950** | 0.0101 | -23.18% | Preserved ($p < 10^{-20}$) |
| **AWS** | **+0.1036** | 0.0128 | **+0.0937** | 0.0095 | -9.50% | Preserved ($p < 10^{-22}$) |
| **Go** | **+0.0686** | 0.0157 | **+0.0942** | 0.0115 | +37.22% | Preserved ($p < 10^{-15}$) |
| **TypeScript** | **+0.0723** | 0.0124 | **+0.0732** | 0.0095 | +1.21% | Preserved ($p < 10^{-14}$) |
| **Python** | **+0.0131** | 0.0123 | **+0.0141** | 0.0094 | +7.16% | Preserved (n.s., $p = 0.134$) |

*Sensitivity Finding & Interpretation:* Across all six evaluated technologies, coefficient signs and significance classifications are preserved. However, coefficient magnitudes and relative rankings change noticeably. Specifically, Docker's coefficient decreases by $23.18\%$ (dropping from $\hat{\beta} = +0.1237$, rank 1 in the full model, to $+0.0950$, rank 2 in the screened refit), while Go's coefficient increases by $37.22\%$ (rising from $\hat{\beta} = +0.0686$, rank 5 in the full model, to $+0.0942$, rank 3 in the screened refit), which elevates Rust to rank 1 ($\hat{\beta} = +0.1217$, $+1.17\%$). This sensitivity analysis demonstrates that point estimates and rankings are sensitive to observations exceeding the diagnostic screening threshold, and does not establish that estimates are unaffected by influential observations.
- **Multicollinearity Assessment:** All technology VIF values are between $1.08$ and $1.34$ (low risk, threshold $<5.0$).
- **Omitted Variable Limitations:** Unobserved variables—including individual cognitive aptitude, elite university education, private equity grants, and local micro-market purchasing power—remain in the disturbance term.

### 3.3 Econometric Results: Technology Associations

#### Table 2.1: Conditional Technology Compensation Associations with HC1 Robust Inference and FDR Control

| Technology Asset | Parameter Estimate ($\hat{\beta}$) | Controlled % Difference | Conventional OLS SE | White HC1 Robust SE | Robust $t$-statistic | Robust 95% Confidence Interval | Raw Robust $p$-value | Benjamini–Hochberg FDR $p$-value | Bonferroni Adjusted $p$-value | VIF |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Docker** | +0.1237 | **+13.17%** | 0.0130 | 0.0130 | 9.49 | [+10.31%, +16.10%] | $2.39 \times 10^{-21}$ | **$1.44 \times 10^{-20}$** | **$1.44 \times 10^{-20}$** | 1.335 |
| **AWS** | +0.1036 | **+10.91%** | 0.0129 | 0.0128 | 8.11 | [+8.17%, +13.72%] | $4.92 \times 10^{-16}$ | **$1.48 \times 10^{-15}$** | **$2.95 \times 10^{-15}$** | 1.226 |
| **Rust** | +0.1203 | **+12.79%** | 0.0172 | 0.0166 | 7.25 | [+9.18%, +16.52%] | $4.32 \times 10^{-13}$ | **$8.64 \times 10^{-13}$** | **$2.59 \times 10^{-12}$** | 1.081 |
| **TypeScript** | +0.0723 | **+7.50%** | 0.0126 | 0.0124 | 5.85 | [+4.93%, +10.14%] | $4.86 \times 10^{-9}$ | **$7.28 \times 10^{-9}$** | **$2.91 \times 10^{-8}$** | 1.263 |
| **Go** | +0.0686 | **+7.10%** | 0.0161 | 0.0157 | 4.37 | [+3.86%, +10.45%] | $1.23 \times 10^{-5}$ | **$1.47 \times 10^{-5}$** | **$7.36 \times 10^{-5}$** | 1.125 |
| **Python** | +0.0131 | **+1.32%** | 0.0120 | 0.0123 | 1.07 | [-1.09%, +3.79%] | 0.2857 | **0.2857 (n.s.)** | **1.0000 (n.s.)** | 1.162 |

- **Substantive Observational Interpretation:**  
  1. **Infrastructure & Cloud:** Stated use of Docker ($+13.17\%$) and AWS ($+10.91\%$) is associated with positive conditional compensation differences relative to non-users holding experience, role, and country constant.
  2. **Modern Systems Specialization:** Stated use of Rust ($+12.79\%$) and Go ($+7.10\%$) retains statistically significant positive conditional associations after multiple testing control.
  3. **The Python Disappearance:** Python's apparent $+11.72\%$ raw compensation advantage completely dissolves to **$+1.32\%$** ($95\%$ CI $[-1.09\%, +3.79\%]$, robust $t = 1.07, p = 0.2857$). Python use does not provide a statistically significant conditional compensation difference once geography and seniority are controlled.

---

## 4. Research Question 3 (RQ3): Autonomous AI Agent Adoption & Workplace Outcomes

### 4.1 Developer Job Satisfaction (`JobSat`) ANOVA & Effect Sizes
We evaluate developer role satisfaction (`JobSat`, 0–10 integer scale) across the 6-tier adoption hierarchy of `AIAgents` among $N = 23,766$ complete cases:

#### Table 3.1: Job Satisfaction Descriptive Statistics across AI Agent Adoption Tiers

| Adoption Hierarchy Tier | Valid $N$ | Mean JobSat | Median | Std Dev ($s$) | Std Error ($SE$) | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Daily Agent Users** | 3,527 | **7.401** | 8.0 | 1.951 | 0.033 | [7.337, 7.465] |
| **2. Weekly Agent Users** | 2,179 | **7.362** | 8.0 | 1.841 | 0.039 | [7.285, 7.439] |
| **3. Copilot-Only Users** | 3,402 | **7.211** | 8.0 | 1.870 | 0.032 | [7.148, 7.274] |
| **4. Monthly / Infrequent Users** | 1,842 | **7.207** | 8.0 | 2.033 | 0.047 | [7.115, 7.300] |
| **5. Non-Planners (Baseline)** | 8,711 | **7.149** | 7.0 | 2.034 | 0.022 | [7.106, 7.191] |
| **6. Planners** | 4,105 | **7.147** | 7.0 | 1.987 | 0.031 | [7.086, 7.207] |
| **Total Analyzed Cohort** | **23,766** | **7.218** | **8.0** | **1.974** | **0.013** | **[7.193, 7.243]** |

#### ANOVA Decomposition & Effect Size Metrics:
- **Sum of Squares:** $SS_{\text{between}} = 226.25$, $df_{\text{between}} = 5$, $MS_{\text{between}} = 45.25$.
- **Residual Sum of Squares:** $SS_{\text{within}} = 92,545.99$, $df_{\text{within}} = 23,760$, $MS_{\text{within}} = 3.90$.
- **$F$-Statistic:** $F = \frac{45.25}{3.90} = 11.6172$, $p = 3.02 \times 10^{-11}$.
- **Eta-Squared ($\eta^2$):**
  $$\eta^2 = \frac{SS_{\text{between}}}{SS_{\text{total}}} = \frac{226.25}{92,772.24} = \mathbf{0.002439} \quad (0.244\%\text{ of total variance})$$
- **Omega-Squared ($\omega^2$):**
  $$\omega^2 = \frac{SS_{\text{between}} - df_{\text{between}} \cdot MS_{\text{within}}}{SS_{\text{total}} + MS_{\text{within}}} = \frac{226.25 - 5(3.8950)}{92,772.24 + 3.8950} = \mathbf{0.002229} \quad (0.223\%\text{ of total variance})$$

#### Table 3.2: Post-Hoc Pairwise Comparisons vs. Non-Planners Baseline (Mean = 7.149)

| Adoption Tier | Analyzed $N$ | Mean JobSat | Difference vs. Non-Planners | Pooled $SE(\text{Diff})$ | 95% Confidence Interval | Standardized Cohen's $d$ | Raw Two-Tailed $p$-value | Bonferroni Adjusted $p$-value |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Daily Agent Users** | 3,527 | 7.401 | **+0.252** | 0.0394 | [+0.175, +0.329] | **0.128** | $1.54 \times 10^{-10}$ | **$7.72 \times 10^{-10}$** |
| **Weekly Agent Users** | 2,179 | 7.362 | **+0.213** | 0.0473 | [+0.121, +0.306] | **0.108** | $6.41 \times 10^{-6}$ | **$3.20 \times 10^{-5}$** |
| **Copilot-Only Users** | 3,402 | 7.211 | +0.062 | 0.0399 | [-0.016, +0.140] | 0.031 | 0.1203 | 0.6017 (n.s.) |
| **Monthly / Infrequent Users** | 1,842 | 7.207 | +0.059 | 0.0506 | [-0.041, +0.158] | 0.030 | 0.2469 | 1.0000 (n.s.) |
| **Planners** | 4,105 | 7.147 | -0.002 | 0.0374 | [-0.075, +0.071] | -0.001 | 0.9546 | 1.0000 (n.s.) |

#### Practical Magnitude Discussion:
While the ANOVA test achieves extreme statistical significance ($p = 3.02 \times 10^{-11}$) driven by the massive sample size ($N = 23,766$), the substantive effect size is **small**:
- An eta-squared of $0.0024$ indicates that autonomous agent adoption explains less than **one-quarter of one percent ($0.24\%$)** of the total variance in developer job satisfaction.
- The difference of $+0.252$ points on an 11-point integer scale ($0$ to $10$) corresponds to a Cohen's $d$ of **$0.128$** (roughly one-eighth of a standard deviation). In practical organizational terms, agent adoption is associated with modest satisfaction differences.

### 4.2 Audit of Favorable Sentiment Odds Ratio ($OR = 21.29$)
We audit the reported Odds Ratio of $21.29$ for favorable AI sentiment (`AISent`) comparing Daily Agent Users vs. Non-Planners:
- **Source Variables:** `AISent` and `AIAgents`.
- **Classification Rules:** Favorable = "Very favorable" or "Favorable" ($1$); Non-Favorable = "Indifferent", "Unfavorable", "Very unfavorable", "Unsure" ($0$).

#### Table 3.3: $2 \times 2$ Contingency Table for Favorable AI Sentiment

| Adoption Cohort | Favorable Sentiment ($a, c$) | Non-Favorable Sentiment ($b, d$) | Total Cohort ($n$) | % Favorable |
| :--- | :---: | :---: | :---: | :---: |
| **Daily AI Agent Users** | **$a = 4,075$** | **$b = 416$** | 4,491 | **90.74%** |
| **Non-Planners (Baseline)** | **$c = 3,801$** | **$d = 8,262$** | 12,063 | **31.51%** |
| **Total Evaluated Respondents** | **7,876** | **8,678** | **16,554** | **47.58%** |

#### Calculation Details:
- **Odds Ratio:**
  $$\text{OR} = \frac{a \cdot d}{b \cdot c} = \frac{4,075 \times 8,262}{416 \times 3,801} = \frac{33,667,650}{1,581,216} = \mathbf{21.292}$$
- **Standard Error:** $SE(\ln(\text{OR})) = \sqrt{\frac{1}{4,075} + \frac{1}{416} + \frac{1}{3,801} + \frac{1}{8,262}} = \sqrt{0.003034} = \mathbf{0.0551}$.
- **Wald 95% Confidence Interval:** $\exp(\ln(21.292) \pm 1.95996 \cdot 0.0551) = \mathbf{[19.114, 23.719]}$.
- **Test Statistic & Significance:** $z = \frac{\ln(21.292)}{0.0551} = 55.53$, two-tailed $p < 10^{-300}$.
- **Sparse-Cell & Separation Audit:** All four contingency cells contain hundreds or thousands of observations (minimum cell $b = 416$). There is **zero evidence of quasi-complete separation or sparse-cell inflation**.
- **Observational Clarification:** This massive odds ratio does not imply that agent usage causes favorable sentiment. Rather, early adopters of autonomous development tools are naturally self-selected enthusiasts who entered the workflow with strong pro-technology dispositions.

---

## 5. Research Question 4 (RQ4): RemoteWork Missingness & Compensation

### 5.1 Missingness Terminology & Contingency Audit
Questionnaire routing audit confirms that the public survey schema (`survey_results_schema.csv`) releases question texts and identifiers (`QID24` for `RemoteWork`, `QID3` for `MainBranch`), but does not publish the underlying survey branching logic script. Therefore, missingness in `RemoteWork` is an **empirically observed pattern in survey response data**, rather than a published branching specification.

Consistent with methodological rigor, we adopt the exact mandated finding:
> **Mandated Methodological Finding:**  
> RemoteWork nonresponse is associated with respondent branch. The observed association suggests that missingness is not MCAR with respect to MainBranch. The available data alone cannot distinguish MAR from MNAR.

#### Table 4.1: Cross-Tabulation of MainBranch by RemoteWork Response Status ($N = 49,191$)

| MainBranch Category | Answered RemoteWork ($n$) | Missing RemoteWork ($n$) | Total Category ($N$) | % Answered | % Missing |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Developer by profession** | 28,286 | 9,181 | 37,467 | 75.50% | 24.50% |
| **Learning to code (Student)** | 552 | 2,033 | 2,585 | 21.35% | **78.65%** |
| **Not primarily a developer, but writes code** | 3,172 | 1,722 | 4,894 | 64.81% | 35.19% |
| **Codes primarily as a hobby** | 530 | 1,394 | 1,924 | 27.55% | **72.45%** |
| **Used to be a developer by profession** | 642 | 683 | 1,325 | 48.45% | 51.55% |
| **Supports developers / Work with devs** | 598 | 398 | 996 | 60.04% | 39.96% |
| **Total Global Sample** | **33,780** | **15,411** | **49,191** | **68.67%** | **31.33%** |

- **Independence Test:** Pearson $\chi^2 = 5,333.84$, $df = 5$, $p < 10^{-300}$, Cramér's $V = 0.329$.
- **Selection Audit Conclusion:** Missingness is heavily concentrated in non-professional branches (students: $78.65\%$ missing; hobbyists: $72.45\%$ missing). The observed association confirms that missingness is not MCAR with respect to MainBranch. Available data alone cannot distinguish MAR from MNAR.

### 5.2 Sensitivity Analysis for Complete-Case Selection
Among all salary earners with valid compensation ($\$1,000$ to $\$1,000,000$ USD, $N = 23,177$), we compare respondents who completed `RemoteWork` ($N = 20,534$, $88.60\%$) against those who skipped `RemoteWork` ($N = 2,643$, $11.40\%$):

#### Table 4.2: Sensitivity Comparison between Answered and Missing RemoteWork Salary Earners

| Demographic / Metric | Answered RemoteWork ($N = 20,534$) | Missing RemoteWork ($N = 2,643$) | Absolute Difference | Selection Bias Assessment |
| :--- | :---: | :---: | :---: | :--- |
| **Median Annual Compensation** | **$77,730** | **$75,000** | +$2,730 (+3.6%) | Highly comparable median wage profile |
| **Mean Professional Experience** | **13.32 years** | **17.44 years** | -4.12 years | Missing respondents are slightly more senior |
| **United States Respondent Share** | **22.98%** | **16.61%** | +6.37% | Answered respondents have higher US representation |
| **Employed Full-Time Share** | **87.21%** | **78.14%** | +9.07% | Missing respondents include more freelancers/part-time |

- **Selection Limitation:** The $N = 20,236$ complete cases in Model C represent active salary earners who completed all covariates. They should not be treated as a randomized sample of all survey participants.

### 5.3 Conditional Compensation Differences Across Working Arrangements
We evaluate conditional compensation differences relative to the in-person reference category across three progressive regression specifications using White HC1 robust standard errors:
- **Model A:** Unadjusted bivariate regression on `RemoteWork` indicators (In-person as baseline).
- **Model B:** Controls for experience (`WorkExp_num`, $\text{WorkExp\_num}^2$) and employer size (`OrgSize_grouped`: Micro $<20$, Small $20-99$, Mid-size $100-999$, Large $1,000-4,999$, Enterprise $5,000+$).
- **Model C:** Fully adjusted model adding country controls (USA, Germany, UK, Canada, India, France, Netherlands; Reference: "Other").

#### Table 4.3: Conditional Compensation Differences Relative to In-Person Baseline

| Working Arrangement | Estimation $N$ | Model A: Raw Diff (%) | Model B: +Exp & OrgSize (%) | Model C: Fully Adjusted (%) | Model C HC1 Robust SE | Model C Robust $t$-stat | Model C Robust 95% Confidence Interval | Model C Robust $p$-value |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **In-person** | 3,124 | **0.00%** *(Baseline)* | **0.00%** *(Baseline)* | **0.00%** *(Baseline)* | — | — | — | — |
| **Remote** | 6,944 | **+78.45%** | **+46.21%** | **+30.65%** | 0.0214 | 12.46 | **[+25.27%, +36.26%]** | **$1.17 \times 10^{-35}$** |
| **Hybrid (leans flexible)** | 3,745 | **+73.00%** | **+36.96%** | **+34.46%** | 0.0213 | 13.87 | **[+28.95%, +40.20%]** | **$9.48 \times 10^{-44}$** |
| **Hybrid (leans in-person)** | 3,846 | **+57.34%** | **+34.37%** | **+33.86%** | 0.0213 | 13.70 | **[+28.39%, +39.56%]** | **$9.79 \times 10^{-43}$** |
| **Your choice / Flexible** | 2,577 | **+63.02%** | **+36.34%** | **+34.07%** | 0.0239 | 12.26 | **[+27.93%, +40.50%]** | **$1.40 \times 10^{-34}$** |

- **Model C Complete Specification & Diagnostics:**
  - **Dependent Variable:** Natural log of annual converted compensation in USD ($y_i = \ln(\text{ConvertedCompYearly}_i)$).
  - **Estimation Sample (Complete Cases):** $N = 20,236$ salary earners within $\$1,000$ to $\$1,000,000$ USD with non-missing values across all model regressors.
  - **Design Matrix Dimensions:** $k = 18$ explanatory variables ($4$ remote work indicators, $2$ experience terms, $5$ organization size indicators, $7$ country indicators) and $p = k + 1 = 19$ estimated parameters including Intercept.
  - **Degrees of Freedom:** $df_{\text{model}} = 18$, $df_{\text{residual}} = n - p = 20,236 - 19 = 20,217$.
  - **Specification Formula:**
    $$\ln(\text{Salary}_i) = \beta_0 + \sum_{k=1}^4 \beta_{\text{Remote}, k} \text{RemoteWork}_{i, k} + \gamma_1 \text{WorkExp}_i + \gamma_2 \text{WorkExp}_i^2 + \sum_{m=1}^5 \delta_m \text{OrgSize}_{i, m} + \sum_{c=1}^7 \lambda_c \text{Country}_{i, c} + \varepsilon_i$$
  - **Predictors and Reference Categories:**
    - Working Arrangement (`RemoteWork`): 4 dummy variables (Remote, Hybrid leans flexible, Hybrid leans in-person, Your choice flexible); Reference category: **"In-person"**.
    - Professional Experience: `WorkExp_num` (linear) and `WorkExp_num_sq` (quadratic).
    - Organization Size (`OrgSize_grouped`): 5 dummy variables (Small 20-99, Mid-size 100-999, Large 1,000-4,999, Enterprise 5,000+, Unknown); Reference category: **"1. Micro (<20)"**.
    - Geographic Country (`Country_grouped`): 7 dummy variables (Canada, France, Germany, India, Netherlands, UK, USA); Reference category: **"Other"**.
  - **Standard Errors:** White HC1 heteroskedasticity-robust standard errors.
  - **Diagnostics:** $R^2 = 0.4254$, Adjusted $R^2 = 0.4249$, Breusch-Pagan test $LM = 2,054.64, df = 18, p < 10^{-300}$, Conventional OLS $F(18, 20217) = 831.44, p < 10^{-300}$ (conventional OLS $F$, not robust Wald $F$). Multicollinearity is absent across all covariates (all VIF $< 3.5$, except between linear and quadratic experience terms).
- **Neutral Interpretation:** In-person developers exhibit a conditional compensation difference of $\approx 30\%$ to $34\%$ relative to remote and hybrid colleagues holding country, experience, and employer size constant. We refrain from loaded phrases such as "wage penalty" or "suffer".

---

## 6. Independent Statistical-Engine Validation

Because environment network restrictions prevented pip installation of external statistical packages (SciPy, Statsmodels), all analytical procedures were implemented in pure Python/NumPy within `src/analysis.py`.
To satisfy scientific review standards, every routine was tested against independently derived, closed-form mathematical benchmarks in `tests/test_statistical_engine_validation.py`:

#### Table 5.1: Mathematical Validation Summary against Analytical Benchmarks

Textbook 5-observation reference dataset: $(x, y) = [(1, 2), (2, 3), (3, 5), (4, 4), (5, 6)]$.
Exact analytical derivations:
- $n = 5, p = 2, df_{\text{res}} = 3, df_{\text{model}} = 1$.
- $X^T X = \begin{bmatrix} 5 & 15 \\ 15 & 55 \end{bmatrix}$, $(X^T X)^{-1} = \begin{bmatrix} 1.1 & -0.3 \\ -0.3 & 0.1 \end{bmatrix}$.
- $\hat{\beta} = [1.3, 0.9]^T$, $\hat{y} = [2.2, 3.1, 4.0, 4.9, 5.8]^T$, $e = [-0.2, -0.1, 1.0, -0.9, 0.2]^T$, $RSS = 1.90, TSS = 10.0, R^2 = 0.81$.
- White HC0 Meat $S_0 = \begin{bmatrix} 1.90 & 6.50 \\ 6.50 & 23.04 \end{bmatrix}$, $V_{\text{HC0}} = \begin{bmatrix} 0.0826 & -0.0182 \\ -0.0182 & 0.0114 \end{bmatrix}$.
- White HC1 Scale $\frac{n}{n-p} = \frac{5}{3} \implies V_{\text{HC1}} = \begin{bmatrix} 0.13766667 & -0.03033333 \\ -0.03033333 & 0.01900000 \end{bmatrix}$.
- $SE_{\text{HC1}}(\hat{\beta}_0) = \sqrt{0.13766667} = 0.37103459$, $SE_{\text{HC1}}(\hat{\beta}_1) = \sqrt{0.019} = 0.13784049$, $t_{\text{HC1}}(\hat{\beta}_1) = 6.529286$.

Independent Multi-Column Predictor Matrix for Variance Inflation Factor (VIF):
To validate `calculate_vif` independently of any outcome regression, we employ a 3-predictor matrix ($n = 5$ observations):
$$x_1 = [3.0, 5.0, 8.0, 9.0, 15.0]^T, \quad x_2 = [1.0, 2.0, 3.0, 4.0, 5.0]^T, \quad x_3 = [0.0, 1.0, 0.0, 1.0, 2.0]^T$$
Exact closed-form auxiliary regression derivations:
- Auxiliary regression of $x_2$ on $(x_1, x_3)$ with intercept: $\hat{x}_{2, i} = \frac{1 + x_{1, i}}{3}$, $RSS_2 = 2/3, TSS_2 = 10 \implies R_2^2 = 1 - \frac{2/3}{10} = \frac{14}{15}$.
  $$\text{Analytical Expected } VIF(x_2) = \frac{1}{1 - 14/15} = \mathbf{15.000000} \quad (\text{Exact Integer!})$$
- Auxiliary regression of $x_1$ on $(x_2, x_3)$ with intercept: $\hat{x}_{1, i} = -\frac{2}{15} + \frac{38}{15} x_{2, i} + \frac{2}{3} x_{3, i}$, $RSS_1 = \frac{76}{15} \approx 5.066667, TSS_1 = 84 \implies R_1^2 = 1 - \frac{76/15}{84} = 1 - \frac{19}{315} = \frac{296}{315}$.
  $$\text{Analytical Expected } VIF(x_1) = \frac{1}{1 - 296/315} = \frac{315}{19} \approx \mathbf{16.578947}$$
- Auxiliary regression of $x_3$ on $(x_1, x_2)$ with intercept: $\hat{x}_{3, i} = -\frac{12}{35} + \frac{5}{35} x_{1, i} + 0 \cdot x_{2, i}$, $RSS_3 = \frac{38}{35} \approx 1.085714, TSS_3 = \frac{14}{5} = 2.8 \implies R_3^2 = 1 - \frac{38/35}{14/5} = 1 - \frac{19}{49} = \frac{30}{49}$.
  $$\text{Analytical Expected } VIF(x_3) = \frac{1}{1 - 30/49} = \frac{49}{19} \approx \mathbf{2.578947}$$

| Procedure / Function | Analytical Benchmark Reference | Tested Parameter | Implemented Value | Benchmark Value | Absolute Error | Validation Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| `fit_ols` | Textbook $5$-point dataset | Slope $\hat{\beta}_1$ | 0.900000 | 0.900000 | $0.00 \times 10^{-7}$ | **Validated** |
| `fit_ols` | Textbook $5$-point dataset | Intercept $\hat{\beta}_0$ | 1.300000 | 1.300000 | $0.00 \times 10^{-7}$ | **Validated** |
| `fit_ols` | Textbook $5$-point dataset | $R^2$ Goodness-of-Fit | 0.810000 | 0.810000 | $0.00 \times 10^{-7}$ | **Validated** |
| `fit_ols` | Textbook $5$-point dataset | Residual Standard Error ($s$) | 0.795822 | 0.795822 | $0.00 \times 10^{-6}$ | **Validated** |
| `fit_ols` | Textbook $5$-point dataset | $F$-statistic | 12.789474 | 12.789474 | $0.00 \times 10^{-6}$ | **Validated** |
| `fit_ols` | Textbook $5$-point dataset | White HC1 Covariance Matrix $V_{11}$ | 0.019000 | 0.019000 | $0.00 \times 10^{-7}$ | **Validated** |
| `fit_ols` | Textbook $5$-point dataset | White HC1 Robust $SE(\hat{\beta}_1)$ | 0.137840 | 0.137840 | $0.00 \times 10^{-7}$ | **Validated** |
| `calculate_vif` | Multi-predictor matrix ($n=5, k=3$) | Analytical $VIF(x_2)$ | 15.000000 | 15.000000 | $0.00 \times 10^{-7}$ | **Validated** |
| `calculate_vif` | Multi-predictor matrix ($n=5, k=3$) | Analytical $VIF(x_1)$ | 16.578947 | $315/19 \approx 16.578947$ | $< 1.00 \times 10^{-6}$ | **Validated** |
| `calculate_vif` | Multi-predictor matrix ($n=5, k=3$) | Analytical $VIF(x_3)$ | 2.578947 | $49/19 \approx 2.578947$ | $< 1.00 \times 10^{-6}$ | **Validated** |
| `calculate_contingency_and_chi2` | Hand-calculated $2 \times 2$ table ($a=40, b=60, c=20, d=80$) | Pearson $\chi^2$ | 9.523810 | 9.523810 | $< 1.00 \times 10^{-6}$ | **Validated** |
| `calculate_contingency_and_chi2` | Hand-calculated $2 \times 2$ table | Cramér's $V$ | 0.218218 | 0.218218 | $< 1.00 \times 10^{-6}$ | **Validated** |
| `calculate_odds_ratios` | Hand-calculated $2 \times 2$ table ($a=40, b=60, c=20, d=80$) | Odds Ratio | 2.666667 | $8/3 \approx 2.666667$ | $< 1.00 \times 10^{-6}$ | **Validated** |
| `calculate_odds_ratios` | Hand-calculated $2 \times 2$ table | 95% Wald CI | [1.4166, 5.0203] | [1.4166, 5.0203] | $< 1.00 \times 10^{-4}$ | **Validated** |
| `compare_groups_continuous` | Hand-calculated $3$-group balanced dataset ($N=9$) | ANOVA $F$-statistic | 27.000000 | 27.000000 | $0.00 \times 10^{-7}$ | **Validated** |
| `compare_groups_continuous` | Hand-calculated $3$-group dataset | Eta-squared ($\eta^2$) | 0.900000 | 0.900000 | $0.00 \times 10^{-7}$ | **Validated** |
| `compare_groups_continuous` | Hand-calculated $3$-group dataset | Omega-squared ($\omega^2$) | 0.852459 | $52/61 \approx 0.852459$ | $< 1.00 \times 10^{-6}$ | **Validated** |
| `adjust_p_values` | Theoretical $4$-test sequence $[0.001, 0.01, 0.03, 0.05]$ | Benjamini–Hochberg | $[0.004, 0.02, 0.04, 0.05]$ | Identical | $0.00 \times 10^{-7}$ | **Validated** |
| `chi2_p_value` | Exact theoretical $\chi^2$ critical limits ($\alpha = 0.05$) | $p$-value at critical $\chi^2$ | 0.050000 | 0.050000 | $< 1.00 \times 10^{-6}$ | **Validated** |

---

## 7. Quality Gate Verification Results

1. **Automated Test Suite:** **70/70 tests passing** in `pytest` ($100\%$ pass rate across Phase 1, Phase 2, Phase 3, Phase 4, Phase 5, and independent statistical engine validation).
2. **Linting Standard:** **0 errors / 0 warnings** across `app/`, `src/`, `tests/` in `flake8` ($100\%$ PEP 8 compliant).
3. **Streamlit Live Health Check:** Verified outside sandbox isolation (`BypassSandbox: true`): started cleanly on port 8506, probed `http://127.0.0.1:8506/_stcore/health`, received HTTP `200 OK` (`ok`), and terminated cleanly.
4. **Dataset Hashes Intact:**
   - `survey_results_public.csv`: `2d1f65308877282edfb4470520eabbc08cb499118432a3dcec6a66c086aa2baa`
   - `survey_results_schema.csv`: `1d24951e04eab46c6f9fecef6ce8e6b32a0a14a3f0eecdcf62f70833a74b3ff8` (30,403 bytes; verified identical byte-for-byte to canonical Git LFS pointer OID and size; earlier transcription mentioning `1d24951eed43...` was an errant copy typo)
   - `survey_results_cleaned.parquet`: `16f5ce8e8f387405fa9635e44074dc468f44b82c0ee23287b2889be238fbbe52`
5. **Git Repository Boundaries:** Working tree untracked, 0 staged changes, 0 commits, 0 pushes, 0 remotes configured.

---
**Report Author:** Akash Das  
**Project Milestone:** Phase 5 — Analysis (Complete, Audited, Independently Validated)  
**Date of Completion:** November 9, 2026  
**Phase Boundary:** Phase 6 (Dashboards & Visualizations) has NOT been started. Awaiting formal Project Lead review and authorization.
