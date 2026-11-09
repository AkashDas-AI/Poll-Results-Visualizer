# Exploratory Data Analysis Report: Stack Overflow Developer Survey 2025

**Project Name:** Poll Results Visualizer  
**Project Author:** Akash Das  
**Milestone:** Phase 4 of 8 — Exploratory Data Analysis (EDA)  
**Date:** 2026-11-09  
**Primary Dataset Input:** `data/processed/survey_results_cleaned.parquet` (49,191 rows × 176 columns)  
**Survey Fieldwork:** May 29, 2025 – June 23, 2025  
**Data Rights & License:** Open Database License (ODbL) v1.0, © Stack Exchange, Inc.  

---

## 1. Executive Summary

This report delivers a comprehensive, reproducible exploratory data analysis (EDA) of the cleaned **Stack Overflow Annual Developer Survey 2025** dataset. Building upon the verified wide-format cleaning pipeline established in Phase 3, this analysis investigates six core analytical workstreams:
1. **Dataset Profiling & Telemetry**
2. **Demographics & Experience**
3. **Technology Landscape & Dual-Percentage Multi-Selects**
4. **AI Tool Adoption, Trust & Autonomous Agents**
5. **Work Arrangements & Annual USD Compensation**
6. **Missingness Patterns & Questionnaire Drop-Off Dynamics**

### Key Empirical Findings:
- **Mainstream AI Developer Tool Utilization (`AISelect`):** **78.50%** of answered respondents ($26,469 / 33,720$) report actively utilizing AI developer tools, with nearly half (**47.10%**, $15,883$ respondents) using them daily.
- **The AI Trust-Capability Paradox (`AIAcc`, `AIComplex`):** Developer adoption dramatically outpaces epistemic trust. Among all respondents answering `AIAcc` ($N = 33,297$), only **3.15%** ($1,048$) report "highly trusting" AI outputs, while **45.71%** ($15,218$) express distrust (26.08% somewhat, 19.62% highly). Among active AI users answering `AIAcc` ($N = 26,126$), high trust is merely **3.82%** ($999$). Furthermore, **47.60%** of all answering respondents ($15,842 / 33,283$) rate AI tools as very poor or bad at handling complex engineering tasks.
- **Rapid Transition to Autonomous AI Agents (`AIAgents`):** Over **30.94%** of answered respondents ($9,875 / 31,919$) have adopted autonomous AI agents into their workflows (14.13% daily, 8.99% weekly, 7.83% monthly), indicating rapid enterprise migration from inline autocomplete copilots toward multi-step autonomous execution.
- **Programming Language Cross-Sectional Gap & Rust Stated Interest:** While core technologies JavaScript (66.32%), HTML/CSS (62.20%), SQL (58.83%), and Python (58.13%) maintain the highest current reported utilization, **Rust** exhibits the highest positive current-versus-desired respondent-share gap (**+19.29 percentage points**; 14.92% current use vs. 34.20% desired use; paired matched sample size $N = 27,079$).
- **Relational Database Leadership:** **PostgreSQL** commands industry preference at **56.86%** adoption among answered respondents ($14,529 / 25,550$), leading MySQL (41.41%) and SQLite (38.35%).
- **Work Arrangement Flexibility (`RemoteWork`):** Remote (32.36%) and hybrid (37.19%) configurations account for **69.55%** of answered software professionals ($N_{\text{answered}} = 33,780$).
- **Annual USD Compensation Benchmarks (`ConvertedCompYearly`):** Across all valid converted salary observations ($N_{\text{answered}} = 23,947$), the global median is **$75,320 USD** (IQR: $38,171–$120,596 USD). National medians match Phase 2 official benchmarks exactly: **$150,000 USD** in the United States ($N=5,243$), **$94,618 USD** in the United Kingdom ($N=1,486$), **$87,550 USD** in Canada ($N=915$), **$81,210 USD** in Germany ($N=2,141$), **$63,228 USD** in France ($N=1,027$), and **$17,029 USD** in India ($N=1,096$).
- **Non-Random Survey Missingness:** Item non-response increases systematically across survey modules, reflecting questionnaire fatigue and structured skip routing rather than random omission.

---

## 2. Dataset Overview & Profiling

### 2.1 Standardized Population Terminology
To maintain analytical transparency, three distinct population concepts are strictly differentiated throughout this report:
1. **Raw Extract Records ($N_{\text{raw}} = 49,191$):** Total respondent rows present in the canonical public survey release.
2. **Official Web Published Base ($N_{\text{official}} = 49,009$):** Qualified respondents evaluated on Stack Overflow's online published report after internal screening (e.g. completion speed < 3 minutes, consent criteria). The 182-row difference reflects internal qualification tags omitted from the public microdata.
3. **Question-Specific Answered Count ($N_{\text{answered}}$):** Because question participation is voluntary, all project-derived percentages are calculated against non-missing question respondents (e.g., $N_{\text{answered}} = 33,720$ for `AISelect`; $N_{\text{answered}} = 23,947$ for `ConvertedCompYearly`).

### 2.2 Numerical Variable Profiling Summary
The cleaned dataset contains three primary numerical analytical fields derived or validated during Phase 3:
- `YearsCode_num`: Derived continuous total coding experience in years (including education).
- `WorkExp_num`: Derived continuous professional work experience in years.
- `ConvertedCompYearly`: Official annual USD compensation converted by Stack Overflow at June 25, 2025 exchange rates.

| Variable | Answered ($N$) | Missing ($N$) | Answered (%) | Min | 25th Pct ($Q_1$) | Median | 75th Pct ($Q_3$) | Mean | Max | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`YearsCode_num`** | 43,042 | 6,149 | 87.50% | 1.0 | 8.0 | 14.0 | 24.0 | 16.57 | 100.0 | 11.79 |
| **`WorkExp_num`** | 42,893 | 6,298 | 87.20% | 1.0 | 5.0 | 10.0 | 20.0 | 13.37 | 100.0 | 10.80 |
| **`ConvertedCompYearly`** | 23,947 | 25,244 | 48.68% | 1.0 | 38,171.0 | 75,320.0 | 120,596.0 | 101,761.54 | 50,000,000.0 | 461,756.90 |

#### Analytical Profiling Observations:
1. **Experience Distribution:** Both coding experience (`YearsCode_num`, median 14.0 yrs) and professional experience (`WorkExp_num`, median 10.0 yrs) exhibit right-skewed distributions. The observed minimum of 1.0 is explained by survey questionnaire routing instructing respondents to leave the field blank if their answer was 0. The ceiling of 100.0 represents the maximum numeric constraint enforced by the web instrument.
2. **Reconciliation of Experience Field Statistics with Phase 3:** The empirical means of **16.57** for `YearsCode_num` and **13.37** for `WorkExp_num` reflect the true, unchanged dataset values calculated directly from `data/processed/survey_results_cleaned.parquet`. These values precisely match the authoritative Phase 3 cleaning report (`reports/data_cleaning_report.md`, lines 111-112). The alternative figures (15.65 and 11.83) that appeared in the Step 1291 review briefing table were human typographical errata during manual briefing text drafting; the parquet data on disk, cleaning pipeline, and statistical calculations have remained 100% stable and identical across both phases.
3. **Compensation Skew & Outliers:** `ConvertedCompYearly` demonstrates severe positive skewness, with maximum values reaching $50,000,000 USD (unverified self-reported entries). The mean ($101,762 USD) is heavily distorted by extreme values, whereas the median ($75,320 USD) and interquartile range ($38,171 to $120,596 USD) provide robust non-parametric metrics. Outliers are preserved without silent deletion in accordance with Phase 4 exploratory boundaries.

---

## 3. Demographic & Experience Exploration

### 3.1 Age Cohort Distribution ($N = 49,191$, 100% Complete)
The age distribution covers the full professional lifecycle, centered predominantly on early-to-mid career professionals:

| Age Cohort | Respondent Count ($N$) | Percentage (%) | Cumulative (%) |
| :--- | :---: | :---: | :---: |
| **25–34 years old** | 16,519 | 33.58% | 33.58% |
| **35–44 years old** | 13,241 | 26.92% | 60.50% |
| **18–24 years old** | 9,210 | 18.72% | 79.22% |
| **45–54 years old** | 6,275 | 12.76% | 91.98% |
| **55–64 years old** | 2,626 | 5.34% | 97.32% |
| **65 years or older** | 942 | 1.91% | 99.23% |
| **Prefer not to say** | 378 | 0.77% | 100.00% |

### 3.2 Geographic Concentration (Top 10 Countries, $N_{\text{answered}} = 35,437$)
The survey encompasses developers across 177 sovereign nations, with strong representation across North America and Europe:

| Rank | Country | Answered Count ($N$) | % of Answered ($N=35,437$) | % of Total ($N=49,191$) |
| :---: | :--- | :---: | :---: | :---: |
| 1 | **United States of America** | 7,233 | 20.41% | 14.70% |
| 2 | **Germany** | 3,025 | 8.54% | 6.15% |
| 3 | **India** | 2,547 | 7.19% | 5.18% |
| 4 | **United Kingdom** | 2,042 | 5.76% | 4.15% |
| 5 | **France** | 1,409 | 3.98% | 2.86% |
| 6 | **Canada** | 1,305 | 3.68% | 2.65% |
| 7 | **Ukraine** | 964 | 2.72% | 1.96% |
| 8 | **Poland** | 888 | 2.51% | 1.81% |
| 9 | **Netherlands** | 867 | 2.45% | 1.76% |
| 10 | **Italy** | 835 | 2.36% | 1.70% |
| — | *All Other 167 Countries* | 14,322 | 40.42% | 29.12% |

### 3.3 Educational Attainment ($N_{\text{answered}} = 48,149$, Missing = 1,042)
Over 73% of respondents hold a formal higher-education degree:
- **Bachelor’s degree (B.A., B.S., B.Eng.):** 20,278 (42.12%)
- **Master’s degree (M.A., M.S., M.Eng., MBA):** 12,589 (26.15%)
- **Some college without degree:** 6,182 (12.84%)
- **Secondary school:** 3,631 (7.54%)
- **Professional doctorate (Ph.D., JD, MD):** 2,624 (5.45%)
- **Associate degree:** 1,562 (3.24%)
- **Other / Primary school:** 1,283 (2.67%)

### 3.4 Developer Roles (`DevType`, Single-Select Verification, $N_{\text{answered}} = 43,680$)
As established in Phase 3, `DevType` was administered as a single-select question in 2025. Exactly 32 distinct developer roles were captured with zero delimiter semicolons. The top 10 roles are:

| Developer Role | Count ($N$) | % of Answered ($N=43,680$) | % of Total ($N=49,191$) |
| :--- | :---: | :---: | :---: |
| **Developer, full-stack** | 12,351 | 28.28% | 25.11% |
| **Developer, back-end** | 6,453 | 14.77% | 13.12% |
| **Student** | 3,008 | 6.89% | 6.11% |
| **Architect, software or solutions** | 2,684 | 6.14% | 5.46% |
| **Developer, front-end** | 1,974 | 4.52% | 4.01% |
| **Developer, desktop or enterprise applications** | 1,919 | 4.39% | 3.90% |
| **Other (please specify):** | 1,825 | 4.18% | 3.71% |
| **Developer, mobile** | 1,391 | 3.18% | 2.83% |
| **Developer, embedded applications or devices** | 1,274 | 2.92% | 2.59% |
| **Academic researcher** | 1,131 | 2.59% | 2.30% |

---

## 4. Technology Landscape & Multi-Select Exploration

### 4.1 Multi-Select Denominator Methodology
In multi-select questions, developers select all applicable technologies from a standardized list. We report two complementary metrics:
1. **Respondent-Level %:** $\frac{\text{Selections for Technology}}{N_{\text{answered}}} \times 100$ (Adoption reach).
2. **Selection-Level %:** $\frac{\text{Selections for Technology}}{\text{Total Selections Made across All Options}} \times 100$ (Share of ecosystem volume).

### 4.2 Programming Languages: Current Use vs. Future Desire

> [!NOTE]
> **Population & Denominator Accounting for Technology Comparisons:**
> - Current technology use (`LanguageHaveWorkedWith`) and future technology interest (`LanguageWantToWorkWith`) are distinct optional survey questions with different non-missing populations: $N_{\text{answered}} = 31,671$ for `LanguageHaveWorkedWith` and $N_{\text{answered}} = 27,079$ for `LanguageWantToWorkWith`.
> - The difference between these marginal proportions is formally designated as the **Current-versus-desired respondent-share gap (percentage points)** rather than a causal or longitudinal transition probability.
> - **Paired Analysis:** Exactly $N = 27,079$ respondents answered *both* questions (i.e. every respondent answering `LanguageWantToWorkWith` also answered `LanguageHaveWorkedWith`).

| Programming Language | Worked With ($N$) | Worked With (%) | Want to Work ($N$) | Want to Work (%) | Current-vs-Desired Share Gap (pp) | Paired Matched Gap (pp, $N=27,079$) | Stated Preference Profile |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **JavaScript** | 21,005 | 66.32% | 10,581 | 39.07% | -27.25 pp | -27.01 pp | Widespread core; lower stated interest than current usage |
| **HTML/CSS** | 19,698 | 62.20% | 10,661 | 39.37% | -22.83 pp | -23.00 pp | Web presentation baseline; lower stated interest than current usage |
| **SQL** | 18,633 | 58.83% | 11,257 | 41.57% | -17.26 pp | -17.28 pp | Data query standard; lower stated interest than current usage |
| **Python** | 18,410 | 58.13% | 12,419 | 45.86% | -12.27 pp | -12.74 pp | High current use; highest absolute stated future interest |
| **Bash/Shell** | 15,503 | 48.95% | 8,662 | 31.99% | -16.96 pp | -17.70 pp | Scripting utility; lower stated interest than current usage |
| **TypeScript** | 13,859 | 43.76% | 10,099 | 37.29% | -6.46 pp | -6.95 pp | Resilient enterprise full-stack retention |
| **Java** | 9,358 | 29.55% | 4,981 | 18.39% | -11.15 pp | -11.17 pp | Enterprise legacy persistence; lower stated interest |
| **C#** | 8,852 | 27.95% | 6,117 | 22.59% | -5.36 pp | -4.90 pp | Stable .NET ecosystem |
| **C++** | 7,485 | 23.63% | 5,243 | 19.36% | -4.27 pp | -4.34 pp | High-performance and systems staple |
| **C** | 6,987 | 22.06% | 4,548 | 16.80% | -5.27 pp | -5.57 pp | Low-level embedded and systems core |
| **Go** | 5,219 | 16.48% | 7,414 | 27.38% | **+10.90 pp** | **+10.66 pp** | Substantially higher stated interest than current usage |
| **Rust** | 4,724 | 14.92% | 9,262 | 34.20% | **+19.29 pp** | **+18.86 pp** | **Highest positive current-vs-desired respondent-share gap** |

### 4.3 Relational & Non-Relational Databases ($N_{\text{answered}} = 25,550$)
- **PostgreSQL:** 14,529 (56.86% of respondents; 18.66% of selections) — Primary open-source standard.
- **MySQL:** 10,581 (41.41% of respondents; 13.59% of selections)
- **SQLite:** 9,798 (38.35% of respondents; 12.58% of selections)
- **Microsoft SQL Server:** 7,871 (30.81% of respondents)
- **Redis:** 6,862 (26.86% of respondents)
- **MongoDB:** 6,389 (25.01% of respondents)

### 4.4 Cloud & Infrastructure Platforms ($N_{\text{answered}} = 24,258$)
- **Docker:** 17,414 (71.79% of respondents) — Standard container runtime.
- **npm:** 13,906 (57.33% of respondents)
- **Amazon Web Services (AWS):** 10,618 (43.77% of respondents) — Leading public cloud provider.
- **Pip:** 10,025 (41.33% of respondents)
- **Kubernetes:** 6,993 (28.83% of respondents)
- **Microsoft Azure:** 6,447 (26.58% of respondents)
- **Google Cloud:** 6,015 (24.80% of respondents)

---

## 5. AI Tool Adoption, Trust & Autonomous Agents

### 5.1 Multi-Level Population & Denominator Accounting
Because subsequent AI questions were presented to all respondents continuing through the AI module rather than being strictly restricted to active AI users, denominators must be explicitly distinguished:

| Survey Variable | Concept Measured | Total Survey ($N$) | Item Answered ($N$) | Item Answered (%) | Active AI Users Answering ($N$) | Non-Users Answering ($N$) | Missing `AISelect` Answering ($N$) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`AISelect`** | AI Tool Adoption & Frequency | 49,191 | 33,720 | 68.55% | 26,469 (78.49%) | 7,251 (21.51%) | 0 (0.00%) |
| **`AIAcc`** | Trust in Accuracy of AI Outputs | 49,191 | 33,297 | 67.69% | 26,126 (78.46%) | 7,134 (21.43%) | 37 (0.11%) |
| **`AIComplex`** | Capability on Complex Tasks | 49,191 | 33,283 | 67.66% | 26,128 (78.50%) | 7,116 (21.38%) | 39 (0.12%) |
| **`AIAgents`** | Autonomous AI Agent Adoption | 49,191 | 31,919 | 64.89% | 24,996 (78.31%) | 6,885 (21.57%) | 38 (0.12%) |

### 5.2 AI Developer Tool Usage (`AISelect`, $N_{\text{answered}} = 33,720$)
- **Yes, I use AI tools daily:** 15,883 (**47.10%** of answered; 32.29% of total sample)
- **Yes, I use AI tools weekly:** 5,958 (**17.67%** of answered; 12.11% of total sample)
- **Yes, I use AI tools monthly or infrequently:** 4,628 (**13.72%** of answered; 9.41% of total sample)
- **Total Active AI Users:** **26,469** (**78.49%** of answered; **53.81%** of total survey population)
- **No, and I don't plan to:** 5,454 (**16.17%** of answered)
- **No, but I plan to soon:** 1,797 (**5.33%** of answered)

### 5.3 The Trust-Capability Paradox (`AIAcc` vs. `AIComplex`)
Developer adoption is tempered by pronounced skepticism regarding epistemic accuracy and complex engineering competence:
- **Trust in AI Output Accuracy (`AIAcc`):**
  - *Across all answered respondents ($N_{\text{answered}} = 33,297$):*
    - **Somewhat trust:** 9,869 (29.64%)
    - **Somewhat distrust:** 8,685 (26.08%)
    - **Neither trust nor distrust:** 7,162 (21.51%)
    - **Highly distrust:** 6,533 (19.62%)
    - **Highly trust:** 1,048 (3.15%)
    - *Combined Distrust (Somewhat + Highly):* **15,218** (**45.71%**)
  - *Among active AI users answering `AIAcc` ($N = 26,126$):*
    - **Somewhat trust:** 9,300 (35.60%)
    - **Somewhat distrust:** 6,705 (25.66%)
    - **Neither trust nor distrust:** 6,113 (23.40%)
    - **Highly distrust:** 3,028 (11.59%)
    - **Highly trust:** 980 (3.75%)
    - *Combined Distrust (Somewhat + Highly):* **9,733** (**37.25%**)
- **Handling Complex Tasks (`AIComplex`, $N_{\text{answered}} = 33,283$):**
  - **Good, but not great:** 8,384 (25.19%)
  - **Bad at handling complex tasks:** 7,328 (22.02%)
  - **Very poor at handling complex tasks:** 5,844 (17.56%)
  - **I don't use AI tools for complex tasks / I don't know:** 5,582 (16.77%)
  - **Neither good nor bad:** 4,688 (14.09%)
  - **Very well at handling complex tasks:** 1,457 (4.38%)
  - *Combined Negative Capability Rating (Bad + Very Poor):* **13,172** (**39.58%** of all answered; **51.46%** among active users)

### 5.4 Emergence of Autonomous AI Agents (`AIAgents`, $N_{\text{answered}} = 31,919$)
The 2025 survey tracks adoption of autonomous multi-step AI agents:
- **Active Agent Adopters:** **9,875** (**30.94%** of answered respondents)
  - Daily active agent use: 4,509 (14.13%)
  - Weekly active agent use: 2,868 (8.99%)
  - Monthly or infrequent agent use: 2,498 (7.83%)
- **Copilot / Autocomplete Only (No Agents):** 4,401 (13.79%)
- **Plan to use agents:** 5,561 (17.42%)
- **Do not plan to use agents:** 12,082 (37.85%)

---

## 6. Work Arrangements & Annual Compensation Exploration

### 6.1 Work Arrangements (`RemoteWork`, $N_{\text{answered}} = 33,780$)
- **Fully Remote:** 10,931 (**32.36%**)
- **Hybrid (heavy in-person):** 6,732 (**19.93%**)
- **In-Person:** 6,042 (**17.89%**)
- **Hybrid (heavy flexibility):** 5,831 (**17.26%**)
- **Your Choice / Highly Flexible:** 4,244 (**12.56%**)
- *Total Remote / Hybrid Flexibility:* **27,738** (**82.11%** of answered responses).

### 6.2 Annual Converted Compensation (`ConvertedCompYearly` in USD)

> [!WARNING]
> **Methodological & Conversion Limitations on Compensation:**
> - `CompTotal` was collected across **142 local currencies** and must never be aggregated directly as USD.
> - `ConvertedCompYearly` represents official annualized USD conversions calculated by Stack Overflow using June 25, 2025 exchange rates.
> - Data represents self-reported, voluntary disclosure unverified against payroll records.
> - Exchange rates reflect market conversions and are **not adjusted for local purchasing power parity (PPP)**.

#### Global Non-Parametric Salary Benchmarks ($N_{\text{answered}} = 23,947$):
- **Overall Global Median:** **$75,320 USD**
- **25th Percentile ($Q_1$):** **$38,171 USD**
- **75th Percentile ($Q_3$):** **$120,596 USD**
- **Interquartile Range (IQR):** **$82,425 USD**

#### Median Converted Compensation by Top Countries ($N \ge 100$ responses):
The empirical country-level medians match the official Phase 2 benchmarks to the exact dollar:

| Country | Project Valid Salary ($N$) | Project Median USD ($) | Official 2025 Benchmark Median ($) | Benchmark Match ($\Delta$) | 25th Pct ($Q_1$) | 75th Pct ($Q_3$) | Interquartile Range (IQR) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **United States of America** | 5,243 | **$150,000** | $150,000 ($N=5,239$) | $0.00 | $101,000 | $200,000 | $99,000 |
| **Switzerland** | 418 | **$142,592** | *(In residual)* | — | $109,256 | $173,280 | $64,024 |
| **Australia** | 569 | **$97,514** | *(In residual)* | — | $74,761 | $126,768 | $52,007 |
| **United Kingdom** | 1,486 | **$94,618** | $94,618 ($N=1,485$) | $0.00 | $65,348 | $132,057 | $66,709 |
| **Canada** | 915 | **$87,550** | *(In residual)* | — | $65,663 | $120,381 | $54,718 |
| **Germany** | 2,141 | **$81,210** | $81,210 ($N=2,141$) | $0.00 | $60,328 | $104,413 | $44,085 |
| **Netherlands** | 619 | **$81,210** | *(In residual)* | — | $58,800 | $106,733 | $47,934 |
| **France** | 1,027 | **$63,228** | $63,228 ($N=1,026$) | $0.00 | $46,406 | $87,011 | $40,605 |
| **India** | 1,096 | **$17,029** | $17,029 ($N=1,093$) | $0.00 | $6,974 | $39,521 | $32,547 |

> [!NOTE]
> **Salary Population Reconciliation & Methodological Accounting:**
> - **Analyzed Observations:** The project analyzes all **23,947** raw-extract salary observations present with non-null `ConvertedCompYearly` values.
> - **Official Published Benchmark:** The official published Stack Overflow salary report evaluates **23,928** qualified salary respondents.
> - **Reconciliation Limitation:** The public microdata does not expose sufficient qualification-screening information (such as internal timing flags or speed thresholds) to identify the individual records responsible for the 19-record difference.
> - **Analytical Status:** The difference of 19 records is therefore a population-count reconciliation limitation between the raw public extract and the official published qualified respondent population, not a confirmed record-level screening result. Individual excluded respondents cannot be identified from the released microdata. Reconciled country medians match published benchmarks to the exact dollar ($0.00 variance across all benchmark countries).

#### Median Compensation by Professional Experience Bracket (`WorkExp_num`):
Brackets are standardized using mutually exclusive and collectively exhaustive intervals over all non-null professional experience responses ($[a, b)$ half-open intervals):

| Experience Bracket | Valid Salary ($N$) | % of Answered ($N=23,469$) | Median Annual USD ($) | 25th Pct ($Q_1$) | 75th Pct ($Q_3$) | Interquartile Range (IQR) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **< 2 years** ($0 \le x < 2$) | 860 | 3.66% | **$20,348** | $5,616 | $46,406 | $40,790 |
| **2 to under 6 years** ($2 \le x < 6$) | 4,793 | 20.42% | **$39,445** | $13,922 | $69,609 | $55,687 |
| **6 to under 11 years** ($6 \le x < 11$) | 5,585 | 23.80% | **$72,000** | $41,868 | $110,214 | $68,346 |
| **11 to under 16 years** ($11 \le x < 16$) | 4,224 | 18.00% | **$90,641** | $58,007 | $136,141 | $78,134 |
| **16 to under 20 years** ($16 \le x < 20$) | 1,814 | 7.73% | **$98,612** | $63,808 | $150,000 | $86,192 |
| **20 years and above** ($x \ge 20$) | 6,193 | 26.39% | **$106,733** | $68,331 | $160,000 | $91,669 |
| *Missing `WorkExp_num`* | 478 | — | $47,687 | $17,029 | $96,500 | $79,471 |
| **Total Valid Salary** | **23,947** | **100.00%** | **$75,320** | **$38,171** | **$120,596** | **$82,425** |

#### Median Compensation by Developer Role (`DevType`, Roles with $N \ge 50$):
1. **Senior executive (C-suite, VP, etc.):** $139,218 USD ($N = 316$, IQR: $81,210–$200,000)
2. **Engineering manager:** $130,000 USD ($N = 717$, IQR: $89,951–$175,000)
3. **Product manager:** $104,413 USD ($N = 115$, IQR: $60,000–$151,800)
4. **Cloud infrastructure engineer:** $103,113 USD ($N = 266$, IQR: $60,328–$145,000)
5. **Architect, software or solutions:** $100,962 USD ($N = 1,626$, IQR: $60,328–$149,698)
6. **Cybersecurity or InfoSec professional:** $98,827 USD ($N = 193$, IQR: $47,330–$153,000)
7. **Applied scientist:** $98,612 USD ($N = 162$, IQR: $61,620–$154,998)
8. **Founder, technology or otherwise:** $92,786 USD ($N = 193$, IQR: $47,423–$165,000)
9. **AI/ML engineer:** $87,281 USD ($N = 352$, IQR: $37,685–$150,819)
10. **DevOps engineer or professional:** $87,011 USD ($N = 697$, IQR: $52,207–$133,417)

---

## 7. Missingness Patterns & Survey Quality Exploration

### 7.1 Missingness Rates Across Survey Modules
Evaluation of item non-response across functional modules reveals clear structural attrition patterns:

| Survey Module | Variable | Answered ($N$) | Answered (%) | Missing ($N$) | Missing (%) | Routing / Skip Logic Context |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Demographics** | `Age` | 49,191 | 100.00% | 0 | 0.00% | Mandatory opening demographic question. |
| **Demographics** | `Employment` | 48,339 | 98.27% | 852 | 1.73% | High completion rate; basic screener. |
| **Demographics** | `EdLevel` | 48,149 | 97.88% | 1,042 | 2.12% | Early single-select education question. |
| **Demographics** | `DevType` | 43,680 | 88.80% | 5,511 | 11.20% | Single-select role question; skipped by some students/retired. |
| **Demographics** | `Country` | 35,437 | 72.04% | 13,754 | 27.96% | Mid-survey demographic placement. |
| **Demographics** | `RemoteWork` | 33,780 | 68.67% | 15,411 | 31.33% | Skipped by non-employed and freelance respondents. |
| **Experience** | `YearsCode_num` | 43,042 | 87.50% | 6,149 | 12.50% | Numeric whole years; 0 entered as blank. |
| **Experience** | `WorkExp_num` | 42,893 | 87.20% | 6,298 | 12.80% | Professional work years; 0 entered as blank. |
| **Technology** | `LanguageHaveWorkedWith` | 31,671 | 64.38% | 17,520 | 35.62% | Beginning of technology matrix section. |
| **Technology** | `DatabaseHaveWorkedWith` | 25,550 | 51.94% | 23,641 | 48.06% | Mid-technology module drop-off. |
| **Technology** | `PlatformHaveWorkedWith` | 24,258 | 49.31% | 24,933 | 50.69% | Platform infrastructure matrix. |
| **Technology** | `WebframeHaveWorkedWith` | 22,992 | 46.74% | 26,199 | 53.26% | Framework matrix; specialized relevance. |
| **AI Module** | `AISelect` | 33,720 | 68.55% | 15,471 | 31.45% | Primary gateway to AI section. |
| **AI Module** | `AIAcc` | 33,297 | 67.69% | 15,894 | 32.31% | Trust in accuracy; presented to all section continuers. |
| **AI Module** | `AIComplex` | 33,283 | 67.66% | 15,908 | 32.34% | Handling complex tasks; presented to all continuers. |
| **AI Module** | `AIAgents` | 31,919 | 64.89% | 17,272 | 35.11% | Autonomous agent adoption; end of AI section. |
| **Compensation**| `Comp_status` | 49,191 | 100.00% | 0 | 0.00% | Exhaustive 4-way classification. |
| **Compensation**| `ConvertedCompYearly` | 23,947 | 48.68% | 25,244 | 51.32% | Voluntary income disclosure. |

### 7.2 Empirical Cross-Tabulation: `RemoteWork` Missingness by `Employment`
As resolved in Phase 3, missingness in `RemoteWork` is NOT attributable solely to students or unemployed respondents:

| Employment Category | Answered `RemoteWork` | Missing `RemoteWork` | Total in Category | Missingness Rate (%) | Contribution to Total Missing ($N=15,411$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `Employed` (full-time / part-time) | 30,126 | 3,624 | 33,750 | 10.74% | 23.52% |
| `Independent contractor / self-employed` | 2,327 | 4,381 | 6,708 | 65.31% | 28.43% |
| `Student` | 1,041 | 3,387 | 4,428 | 76.49% | 21.98% |
| `Not employed` (looking / not looking) | 208 | 2,019 | 2,227 | 90.66% | 13.10% |
| `Missing Employment` (omitted both) | 0 | 852 | 852 | 100.00% | 5.53% |
| `Retired` | 78 | 630 | 708 | 88.98% | 4.09% |
| `I prefer not to say` | 0 | 518 | 518 | 100.00% | 3.36% |
| **Total** | **33,780** | **15,411** | **49,191** | **31.33%** | **100.00%** |

---

## 8. Preliminary Visual Observations & Output Catalog

Fourteen standalone interactive visualizations were generated and saved in [`outputs/charts/`](file:///D:/Projects/Data%20Science/Poll%20Results%20Visualizer/outputs/charts/):

1. [`01_age_distribution.html`](file:///D:/Projects/Data%20Science/Poll%20Results%20Visualizer/outputs/charts/01_age_distribution.html): Age cohort frequencies ($N=49,191$).
2. [`02_top_countries.html`](file:///D:/Projects/Data%20Science/Poll%20Results%20Visualizer/outputs/charts/02_top_countries.html): Horizontal bar chart of top 10 respondent countries ($N_{\text{answered}}=35,437$).
3. [`03_developer_roles.html`](file:///D:/Projects/Data%20Science/Poll%20Results%20Visualizer/outputs/charts/03_developer_roles.html): Top 15 single-select developer roles ($N_{\text{answered}}=43,680$).
4. [`04_experience_distributions.html`](file:///D:/Projects/Data%20Science/Poll%20Results%20Visualizer/outputs/charts/04_experience_distributions.html): Dual overlaid histograms of total coding experience vs professional work experience.
5. [`05_top_languages_have_vs_want.html`](file:///D:/Projects/Data%20Science/Poll%20Results%20Visualizer/outputs/charts/05_top_languages_have_vs_want.html): Grouped bar chart comparing current language use with future stated interest (Paired matched $N=27,079$).
6. [`06_top_databases.html`](file:///D:/Projects/Data%20Science/Poll%20Results%20Visualizer/outputs/charts/06_top_databases.html): Top 10 databases worked with (% of answered respondents).
7. [`07_top_cloud_platforms.html`](file:///D:/Projects/Data%20Science/Poll%20Results%20Visualizer/outputs/charts/07_top_cloud_platforms.html): Top 10 cloud and infrastructure platforms.
8. [`08_ai_tool_usage.html`](file:///D:/Projects/Data%20Science/Poll%20Results%20Visualizer/outputs/charts/08_ai_tool_usage.html): Pie chart of AI tool usage frequency ($N_{\text{answered}}=33,720$).
9. [`09_ai_trust_accuracy.html`](file:///D:/Projects/Data%20Science/Poll%20Results%20Visualizer/outputs/charts/09_ai_trust_accuracy.html): Bar chart of output accuracy trust (Total $N_{\text{answered}}=33,297$; Active users $N=26,126$).
10. [`10_ai_agents_adoption.html`](file:///D:/Projects/Data%20Science/Poll%20Results%20Visualizer/outputs/charts/10_ai_agents_adoption.html): Autonomous AI agent adoption frequency (Total $N_{\text{answered}}=31,919$; Active users $N=24,996$).
11. [`11_compensation_by_country.html`](file:///D:/Projects/Data%20Science/Poll%20Results%20Visualizer/outputs/charts/11_compensation_by_country.html): Median annual USD compensation across top nations ($N \ge 100$).
12. [`12_compensation_by_experience.html`](file:///D:/Projects/Data%20Science/Poll%20Results%20Visualizer/outputs/charts/12_compensation_by_experience.html): Median annual compensation by standardized professional experience bracket ($N_{\text{answered}}=23,469$).
13. [`13_compensation_by_role.html`](file:///D:/Projects/Data%20Science/Poll%20Results%20Visualizer/outputs/charts/13_compensation_by_role.html): Top 12 developer roles by median annual USD compensation ($N \ge 50$).
14. [`14_missingness_by_survey_section.html`](file:///D:/Projects/Data%20Science/Poll%20Results%20Visualizer/outputs/charts/14_missingness_by_survey_section.html): Comparative missingness rates across key survey sections.

---

## 9. Methodological Boundaries & Limitations

1. **Non-Probability Convenience Sampling:** The survey is an opt-in web instrument fielded primarily through Stack Overflow owned media. Results reflect the attitudes of self-selected participants and must not be interpreted as statistically representative of the global developer population.
2. **Absence of Longitudinal Timestamps:** The survey represents a cross-sectional snapshot captured between May 29 and June 23, 2025. Individual respondent completion timestamps are omitted to protect privacy; temporal velocity tracking is not possible.
3. **Unverified Compensation Self-Reporting:** Compensation figures reflect voluntary self-reporting without verification against payroll or tax documentation. Market currency conversions do not incorporate local purchasing power parity (PPP).
4. **Descriptive, Non-Causal Boundaries:** All observed associations (e.g. AI adoption across age groups, experience vs. salary) represent descriptive correlations in this sample. Causal inference is strictly out of scope for Phase 4.

---

## 10. Research Questions for Phase 5 (Analysis)

The exploratory findings in Phase 4 identify five high-priority hypotheses to investigate formally in Phase 5:
1. **Determinants of AI Accuracy Trust:** What combination of professional experience, role seniority, and technology stack is most strongly associated with skepticism toward AI tool accuracy?
2. **Specialized Technology Compensation Premiums:** After controlling for years of experience and geographic location, what is the residual compensation premium associated with emerging systems languages (Rust, Go) versus traditional enterprise languages (Java, C#)?
3. **The Agentic Work Experience Divide:** Does autonomous AI agent adoption correlate with higher job satisfaction, or does it correlate with developer friction in code review and maintenance?
4. **Remote Work Wage Dynamics:** Does the salary premium for remote workers persist across emerging developer hubs (e.g., India, Poland) when controlling for multinational employer presence?
5. **Survey Drop-Off Modeling:** Can respondent attrition across technology matrix questions be modeled as a function of early questionnaire fatigue versus technical specialization?

---
**End of Report — Phase 4 Exploratory Data Analysis Complete.**
