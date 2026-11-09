# Statistical & Econometric Methodology

**Project Name:** Poll Results Visualizer  
**Author:** Akash Das  
**Current Milestone:** Phase 8 - Final Project Polish, GitHub Preparation and Publication  
**Primary Dataset:** Stack Overflow Annual Developer Survey 2025  

---

## 1. Survey Sampling Framework & Data Governance

### 1.1 Non-Probabilistic Convenience Sampling
The Stack Overflow Annual Developer Survey is a voluntary, self-administered web survey fielded via banner links, social media, and developer newsletters between **May 29, 2025**, and **June 23, 2025**.
- **Sampling Mechanism:** Opt-in convenience sample. Participants are self-selected Stack Overflow community members and web visitors.
- **Absence of Population Weights:** The public microdata release does not provide post-stratification or demographic sampling weights.
- **Methodological Mandate:** The visualizer strictly refuses to fabricate or apply synthetic sampling weights. All reported metrics reflect unweighted sample counts and sample proportions.
- **Scope of Inference:** Findings describe empirical relationships within the participating sample and cannot be generalized to the entire global population of software engineers.

### 1.2 Target Populations & Denominator Taxonomy
To prevent denominator confusion across questions with varying nonresponse rates, the project enforces four distinct population constants:

| Population Identifier | Sample Size ($N$) | Definition & Inclusion Criteria |
| :--- | :--- | :--- |
| **Raw Microdata ($N_{\text{raw}}$)** | $49,191$ | Total unweighted records in `survey_results_public.csv`. |
| **Official Published Base ($N_{\text{official}}$)** | $49,009$ | Officially qualified responses reported on the Stack Overflow public website (182 records excluded due to qualification filters). |
| **Question Answered Base ($N_{\text{answered}}$)** | Variable per item | Total respondents providing a non-null answer to a specific question (e.g. $N = 30,780$ for `AIAcc`; $N = 23,947$ for `ConvertedCompYearly`). |
| **Paired Migration Cohort ($N_{\text{paired}}$)** | $27,079$ | Symmetric respondents answering both `LanguageHaveWorkedWith` and `LanguageWantToWorkWith`. |

### 1.3 Non-Causal Cross-Sectional Inference Policy
The survey employs a cross-sectional observational design. All variables are captured simultaneously at a single point in time. Completion timestamps are omitted to protect participant privacy.
- **Core Principle:** Cross-sectional regression coefficients and contingency table associations establish empirical correlations, **not causation**.
- **Language Standards:** Automated narratives strictly avoid causal verbs ("causes", "drives", "impacts", "leads to", "boosts"). Descriptions use neutral observational terms ("associated with", "conditional differential", "stated preference gap").

---

## 2. Descriptive Survey Mathematics

### 2.1 Single-Select Categorical Normalization
For questions where respondents choose exactly one mutually exclusive option:
$$\text{Percentage}(O_i) = \left( \frac{\text{Count}(O_i)}{N_{\text{answered}}} \right) \times 100$$
The sum of percentages across all options evaluates to exactly $100.0\%$.

### 2.2 Multi-Select Dual-Denominator Normalization
In semicolon-delimited multi-select questions (e.g. `LanguageHaveWorkedWith`), respondents may select multiple options. Presenting percentages relative to total selections distorts prevalence. The system computes dual metrics:
1. **Respondent Prevalence Share (%):**
   $$\text{Pct of Respondents}(O_i) = \left( \frac{\text{Count}(O_i)}{N_{\text{answered}}} \right) \times 100$$
   *Because respondents select multiple technologies, the sum across options exceeds $100\%$.*
2. **Total Selection Share (%):**
   $$\text{Pct of Selections}(O_i) = \left( \frac{\text{Count}(O_i)}{\sum_j \text{Count}(O_j)} \right) \times 100$$
   *Represents the fraction of all checkmarks attributed to option $O_i$. Sums to $100.0\%$.*

### 2.3 Within-Cohort Normalization
When comparing across demographic segments with unequal sample sizes, raw counts create misleading impressions. Percentages are normalized within each cohort:
$$P(O_i \mid S_k) = \left( \frac{\text{Count}(O_i \text{ in cohort } S_k)}{\text{Total answered responses in cohort } S_k} \right) \times 100$$

---

## 3. Inferential Categorical Testing

### 3.1 Pearson Chi-Square Test of Independence ($\chi^2$)
To evaluate whether categorical outcomes differ significantly across demographic cohorts:
$$\chi^2 = \sum_{i=1}^r \sum_{j=1}^c \frac{\left(O_{ij} - E_{ij}\right)^2}{E_{ij}}, \quad E_{ij} = \frac{R_i \times C_j}{N}$$
- **Degrees of Freedom:** $df = (r - 1)(c - 1)$.
- **$p$-Value Evaluation:** Evaluated via regularized upper incomplete gamma function $Q(df/2, \chi^2/2)$.
- **Cramér's $V$ Effect Size:**
  $$V = \sqrt{\frac{\chi^2}{N \min(r - 1, c - 1)}}$$
  - $V \approx 0.10$: Small association
  - $V \approx 0.30$: Medium association
  - $V \ge 0.50$: Large association

### 3.2 Binary Odds Ratios & Wald Confidence Intervals
For $2 \times 2$ contingency tables comparing exposure/seniority against a binary outcome:
$$\text{OR} = \frac{a \times d}{b \times c}$$
- **Asymptotic Standard Error of $\ln(\text{OR})$:**
  $$SE_{\ln(\text{OR})} = \sqrt{\frac{1}{a} + \frac{1}{b} + \frac{1}{c} + \frac{1}{d}}$$
- **Wald 95% Confidence Interval:**
  $$\text{CI}_{95\%} = \left[ \exp\left(\ln(\text{OR}) - 1.96 \times SE\right), \quad \exp\left(\ln(\text{OR}) + 1.96 \times SE\right) \right]$$
- **Wald $z$-Statistic:** $z = \frac{\ln(\text{OR})}{SE}, \quad p = 2 \left(1 - \Phi(|z|)\right)$.

---

## 4. Econometric Modeling & Wage Regressions

### 4.1 Extended Mincerian Log-Linear Wage Specification
To estimate technology compensation premiums while controlling for human capital and structural confounders, we specify a semi-logarithmic Ordinary Least Squares (OLS) model:
$$\ln(\text{Wage}_i) = \beta_0 + \beta_1 \text{Exp}_i + \beta_2 \text{Exp}_i^2 + \sum_{j} \gamma_j \text{Tech}_{ij} + \sum_{k} \delta_k \text{Demog}_{ik} + \epsilon_i$$
- **Dependent Variable:** $\ln(\text{ConvertedCompYearly})$ in USD.
- **Experience Controls:** Linear and quadratic professional experience ($\text{WorkExp\_num}$).
- **Quadratic Experience Inflection Point:**
  $$\text{Exp}_{\text{peak}} = -\frac{\hat{\beta}_1}{2 \hat{\beta}_2}$$
  In Model 3 ($\hat{\beta}_1 = +0.06734, \hat{\beta}_2 = -0.001149$), empirical earnings peak at $\approx 29.3$ years of experience.

### 4.2 Exact Exponential Percentage Conversion
In semi-logarithmic regressions, naive linear interpretation ($\% \Delta y \approx 100 \times \hat{\beta}$) produces substantial errors for coefficients exceeding $0.10$. All reporting utilizes **Halvorsen and Palmquist's exact formula**:
$$\% \Delta y = 100 \times \left(e^{\hat{\beta}} - 1\right)$$
- **Confidence Intervals:** Upper and lower bounds of $\hat{\beta}$ are similarly converted:
  $$\text{CI}_{95\%} = \left[ 100 \times \left(e^{\hat{\beta} - 1.96 \times SE} - 1\right), \quad 100 \times \left(e^{\hat{\beta} + 1.96 \times SE} - 1\right) \right]$$

### 4.3 White's Heteroskedasticity-Consistent (HC1) Standard Errors
Cross-sectional wage data inherently violates the Gauss-Markov homoskedasticity assumption. Constant variance is rejected via the Breusch-Pagan test ($LM = 2,269.63, df = 20, p = 0.0$ in Model 3). To prevent inflated $t$-statistics and spurious significance, all standard errors use White's HC1 estimator:
$$\text{Var}_{\text{HC1}}(\hat{\beta}) = \frac{n}{n - p} \left(X^T X\right)^{-1} X^T \text{diag}\left(e_i^2\right) X \left(X^T X\right)^{-1}$$
where $e_i = y_i - \hat{y}_i$ are OLS residuals, $n$ is sample size, and $p$ is the number of estimated parameters.

### 4.4 Closed-Form Multicollinearity Diagnostics (VIF)
Collinearity between technology predictors is evaluated using auxiliary regressions:
$$\text{VIF}_j = \frac{1}{1 - R_j^2} = \frac{\text{TSS}_j}{\text{RSS}_j}$$
- **Threshold:** $\text{VIF} < 5.0$ indicates no problematic collinearity.
- **Empirical Results:** In Model 3, all predictor VIFs were $< 1.50$ (Docker: 1.15, Rust: 1.05, AWS: 1.19, TypeScript: 1.25, Go: 1.12, Python: 1.20).
- **Independent Closed-Form Verification Benchmark:**
  To guarantee engine precision, the implementation is validated against an exact $5 \times 3$ predictor matrix:
  - $x_1$ on $x_2, x_3$: $\text{RSS} = 76/15, \text{TSS} = 84, R^2 = 296/315 \implies \text{VIF} = 315/19 \approx 16.578947$.
  - $x_2$ on $x_1, x_3$: $\text{RSS} = 2/3, \text{TSS} = 10, R^2 = 14/15 \implies \text{VIF} = 15.0$.
  - $x_3$ on $x_1, x_2$: $\text{RSS} = 38/35, \text{TSS} = 2.8, R^2 = 30/49 \implies \text{VIF} = 49/19 \approx 2.578947$.

### 4.5 Regression Performance Scores & Model Comparison

| Specification | Sample Size ($N$) | Predictors ($p$) | $R^2$ | Adjusted $R^2$ | RMSE | $F$-Statistic ($p$-value) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Model 1: Baseline Human Capital** | $22,769$ | $3$ | $0.2831$ | $0.2830$ | $0.7529$ | $359.1$ ($p < 10^{-300}$) |
| **Model 2: Demographics & Roles** | $22,769$ | $15$ | $0.3533$ | $0.3529$ | $0.7153$ | $250.7$ ($p < 10^{-300}$) |
| **Model 3: Full Specification + Tech** | $22,769$ | $21$ | $0.3846$ | $0.3840$ | $0.6979$ | $186.7$ ($p < 10^{-300}$) |
| **Model C: Remote Work Dynamics** | $20,236$ | $18$ | $0.4254$ | $0.4249$ | $0.6720$ | $373.1$ ($p < 10^{-300}$) |

### 4.6 Sensitivity Analysis & Influential Observation Screening
To evaluate model stability, observations are screened using Cook's distance ($D_i$) and leverage ($h_{ii}$):
$$D_i = \frac{e_i^2}{p \times s^2} \left( \frac{h_{ii}}{(1 - h_{ii})^2} \right), \quad h_{ii} = x_i (X^T X)^{-1} x_i^T$$
- **Diagnostic Screening Threshold:** $D_i > \frac{4}{n}$. Exceeding this threshold indicates potential influence, **not** data corruption or justification for deletion.
- **Sensitivity Model ($N = 21,730$, $1,039$ points screened):**
  - **100% Stability:** All coefficient signs and statistical significance classifications are fully preserved.
  - **Point Estimate Shifts:** Point estimates and relative rankings adjust (Docker shifts from $+13.17\%$ to $+9.97\%$; Go shifts from $+7.10\%$ to $+9.88\%$). This formally demonstrates that while sign and significance are robust, exact magnitudes are sensitive to influential observations.

---

## 5. Analysis of Variance (ANOVA) & Effect Sizes

### 5.1 One-Way ANOVA Decomposition
Evaluating continuous outcomes across $k$ categorical groups:
$$SS_{\text{between}} = \sum_{j=1}^k n_j (\bar{y}_j - \bar{y})^2, \quad SS_{\text{within}} = \sum_{j=1}^k \sum_{i=1}^{n_j} (y_{ij} - \bar{y}_j)^2, \quad SS_{\text{total}} = SS_b + SS_w$$
$$F = \frac{SS_{\text{between}} / (k - 1)}{SS_{\text{within}} / (N - k)}$$

### 5.2 Effect Size Decompositions ($\eta^2$, $\omega^2$, Cohen's $d$)
Large sample sizes yield tiny $p$-values even when real-world group differences are trivial. We decompose effect magnitude:
1. **Eta-Squared ($\eta^2$):** $\eta^2 = \frac{SS_{\text{between}}}{SS_{\text{total}}}$.
2. **Omega-Squared ($\omega^2$):** Less biased population variance estimator:
   $$\omega^2 = \frac{SS_{\text{between}} - (k - 1) MS_{\text{within}}}{SS_{\text{total}} + MS_{\text{within}}}$$
3. **Pairwise Cohen's $d$:**
   $$d = \frac{\bar{y}_1 - \bar{y}_2}{s_{\text{pooled}}}, \quad s_{\text{pooled}} = \sqrt{\frac{(n_1 - 1)s_1^2 + (n_2 - 1)s_2^2}{n_1 + n_2 - 2}}$$
4. **Multiple Testing Control:** Pairwise post-hoc $p$-values are adjusted using the **Bonferroni-Holm step-down procedure** to control the familywise error rate (FWER) without excessive conservatism.

---

## 6. Missing Data Analysis (Rubin's Taxonomy)

Under Donald Rubin's missing data taxonomy:
- **MCAR (Missing Completely at Random):** Missingness is independent of both observed and unobserved data.
- **MAR (Missing at Random):** Missingness depends on observed covariates but is conditionally independent of unobserved values.
- **MNAR (Missing Not at Random):** Missingness depends directly on unobserved values.

### RemoteWork Nonresponse Case Study
- **Observed Pattern:** $15,411$ out of $49,191$ respondents ($31.33\%$) omitted `RemoteWork`.
- **Contingency Analysis:** A $6 \times 2$ contingency table against `MainBranch` yields $\chi^2 = 5,333.84, df = 5, p < 10^{-300}$, Cramér's $V = 0.3293$. Professional developers exhibited $24.50\%$ nonresponse, while students ($78.65\%$) and hobbyists ($72.45\%$) skipped the item at massive rates.
- **Methodological Boundary:** Because the public survey schema does not release internal questionnaire skip logic, we cannot prove whether students were structurally routed past employment questions. The finding is stated strictly as:
  > *"RemoteWork nonresponse is strongly associated with respondent branch ($\chi^2 = 5,333.84, df = 5, p < 10^{-300}$). The observed association indicates that missingness is not MCAR with respect to MainBranch. The available public microdata alone cannot distinguish MAR from MNAR."*
