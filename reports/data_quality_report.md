# Data Quality & Ingestion Audit Report: Stack Overflow Developer Survey 2025

**Author:** Akash Das  
**Phase:** Phase 2 — Public Dataset Integration & Quality Audit (Analytical Corrections Applied)  
**Date:** 2026-11-09  
**Source Dataset:** Official Stack Overflow Annual Developer Survey 2025  

---

## 1. Dataset Source & Provenance
- **Publisher:** Stack Exchange, Inc.
- **Survey Year:** 2025
- **Fieldwork Period:** May 29, 2025 – June 23, 2025
- **Official Source Endpoints:**
  - Official Survey Results: [https://survey.stackoverflow.co/2025/](https://survey.stackoverflow.co/2025/)
  - Official Survey Methodology: [https://survey.stackoverflow.co/2025/methodology](https://survey.stackoverflow.co/2025/methodology)
  - Official Survey Repository: [https://github.com/StackExchange/Survey](https://github.com/StackExchange/Survey)
  - Release Archive: `https://github.com/StackExchange/Survey/tree/main/packages/archive/2025`
  - Git LFS Media Endpoints:
    - Results: `https://media.githubusercontent.com/media/StackExchange/Survey/main/packages/archive/2025/results.csv`
    - Schema: `https://media.githubusercontent.com/media/StackExchange/Survey/main/packages/archive/2025/schema.csv`
- **License:** Open Database License (ODbL) v1.0 (Database) and Database Contents License (DbCL) v1.0 (Cell contents).
- **Application Code License:** MIT License, Copyright (c) 2026 Akash Das.

---

## 2. Dataset Inventory & Standardized Population Framework
The downloaded dataset contains respondent-level, wide-format records capturing developer characteristics and questionnaire responses.

| Population Concept | Row Count | Standard Definition & Methodological Context |
| :--- | :--- | :--- |
| **Raw Public Records ($N_{\text{raw}}$)** | **49,191** | Total unweighted respondent rows in `survey_results_public.csv` (`ResponseId` 1 to 49,191). |
| **Official Web Published Base ($N_{\text{official}}$)** | **49,009** | Validated respondents reported in Stack Overflow's online methodology after internal speed/consent screening. |
| **Qualification Filter Discrepancy** | **182** | Difference ($49,191 - 49,009 = 182$) reflects internal qualification rules (e.g. <3 min completion) not flagged in public CSV. |
| **Question-Specific Answered Counts ($N_{\text{answered}}$)** | **Varies** | Question-specific non-missing answers in raw extract (e.g. `AISelect`: 33,720; `ConvertedCompYearly`: 23,947; `Country`: 35,437). |

> [!IMPORTANT]
> **Denominator Governance**: All project-derived percentages use $N_{\text{answered}}$ from the raw public extract as the denominator. We do not synthesize an artificial qualification filter to force raw row counts to match $N_{\text{official}}$.

### Physical File Inventory
- **Results Microdata (`survey_results_public.csv`):** 140,893,245 bytes (~134.4 MB), Content SHA-256: `2d1f65308877282edfb4470520eabbc08cb499118432a3dcec6a66c086aa2baa`.
- **Question Schema (`survey_results_schema.csv`):** 30,403 bytes (~29.7 KB), Content SHA-256: `1d24951e04eab46c6f9fecef6ce8e6b32a0a14a3f0eecdcf62f70833a74b3ff8`.
- **Duplicate Removal:** Identical files `results.csv` and `schema.csv` were verified byte-for-byte and removed to eliminate redundant storage.

---

## 3. Respondent Identifier & Duplicate Audit
- **Primary Key:** `ResponseId` (Integer, 1 to 49,191).
- **Duplicate Records:** **0 duplicates**. Every row represents an authenticated unique response event.
- **Completeness of ID:** 100% complete (0 nulls in `ResponseId`).

---

## 4. Question Structure & Questionnaire Topologies
Based on the official survey schema (`survey_results_schema.csv`), the 139 modeled items fall into 4 primary questionnaire types:

1. **Rank Order / Rating (`RO`)** (49 items): Priority rankings and importance ratings (e.g., `TechEndorse_1` through `TechEndorse_9`).
2. **Multiple Choice (`MC`)** (48 items): Categorical variables, subdivided into:
   - *Single-Select*: Mutually exclusive choices (e.g., `Age`, `Employment`, `AISelect`, `AISent`, `AIAcc`, `RemoteWork`).
   - *Multi-Select*: Semicolon-delimited checkbox selections (e.g., `LanguageHaveWorkedWith`, `DatabaseHaveWorkedWith`, `PlatformHaveWorkedWith`).
3. **Text Entry (`TE`)** (29 items): Free-form text fields and compensation entries (e.g., `CompTotal`, `AIExplain`).
4. **Matrix (`Matrix`)** (13 items): Likert agreement grids and multi-dimensional matrices (e.g., `AITool`, `AIAgentImpact`, `AIAgentChallenges`).

---

## 5. Missing-Value (Sparsity) Analysis
Survey participation is voluntary, and respondents were permitted to skip non-mandatory questions or exit early.

### 5.1 High-Completeness Demographic Variables
- `Age`: **0 nulls (100.0% complete)** across all 49,191 respondents.
- `MainBranch`: **0 nulls (100.0% complete)** across all 49,191 respondents.
- `Employment`: 852 nulls (**98.3% complete**).
- `EdLevel`: 1,042 nulls (**97.9% complete**).
- `DevType`: 5,511 nulls (**88.8% complete**).
- `YearsCode`: 6,149 nulls (**87.5% complete**).
- `WorkExp`: 6,298 nulls (**87.2% complete**).
- `Country`: 13,754 nulls (**72.0% complete**).

### 5.2 High-Missingness Columns (>80% Null)
**36 of the 172 columns** exhibit greater than 80% missingness. These correspond to:
- Optional free-text specifications (e.g., `TechEndorse_13_TEXT` is 95.9% null; `JobSatPoints_15_TEXT` is 98.7% null).
- Specialized "other" write-in tools (e.g., `LanguagesHaveEntry` 91.9% null; `DatabaseHaveEntry` 95.6% null).
- Advanced AI agent framework sub-questions shown only to developers who answered affirmatively to developing autonomous agents.

---

## 6. Compensation Reconciliation & Conversion Auditing

### 6.1 Primary Field & Official Currency Conversion
- **Official Converted Column (`ConvertedCompYearly`):** Exists natively in the raw CSV extract. It is used as the **primary source** for all USD compensation analyses. Stack Overflow converted self-reported local currencies into USD using market exchange rates recorded on **June 25, 2025**. Reconstructing conversion from raw local currency is therefore unnecessary for primary benchmarking.
- **Raw Variable (`CompTotal`):** Collected in **142 local currencies** (`Currency`). Raw `CompTotal` must **never** be aggregated directly as USD.
- **Currency Field (`Currency`):** Populated for 35,437 respondents.
- **Conversion Coverage:** In the raw extract, 24,866 respondents answered `CompTotal`, of which **23,947** were converted into `ConvertedCompYearly` by Stack Overflow (919 entries with unconvertible currencies or missing rates were left null).

### 6.2 Reconciliation with Official Published Results
Stack Overflow's official published salary report on `survey.stackoverflow.co/2025/work` analyzes **23,928 salary responses**, compared to **23,947 non-missing responses** in our raw extract:

| Analysis Scope | Raw Public Extract ($N_{\text{answered}}$) | Official Published ($N_{\text{official}}$) | Net Difference ($\Delta$) | Project-Derived Median (USD) | Published Official Median (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **All Respondents** | **23,947** | **23,928** | **+19** | **$75,320** | **~$75,000** |
| **United States** | 5,243 | 5,239 | +4 | $150,000 | $150,000 |
| **Germany** | 2,141 | 2,141 | 0 | $81,210 | $81,210 |
| **United Kingdom** | 1,486 | 1,485 | +1 | $94,618 | $94,618 |
| **France** | 1,027 | 1,026 | +1 | $63,228 | $63,228 |
| **India** | 1,096 | 1,093 | +3 | $17,029 | $17,029 |
| **All Other Countries (Residual)** | **12,954** | **12,944** | **+10** | Varies | Varies |

*Arithmetic Verification:*
- Raw extract: $5,243 + 2,141 + 1,486 + 1,027 + 1,096 + 12,954 = 23,947$ (mutually exclusive and exhaustive across all 164 countries with compensation).
- Official published: $5,239 + 2,141 + 1,485 + 1,026 + 1,093 + 12,944 = 23,928$ (mutually exclusive and exhaustive).
- If Canada ($N_{\text{answered}} = 915$, median $87,550 USD) is broken out separately from the raw extract, the remaining 158 other countries total **12,039** ($11,908 + 12,039 = 23,947$).

**Reconciliation of Derived vs. Published Counts:** The 19-record difference represents the net variance between the project-derived count ($N_{\text{answered}} = 23,947$) and Stack Overflow's published qualified salary count ($N_{\text{official}} = 23,928$). Because individual qualification flags and completion duration timestamps are omitted from the public microdata release, individual excluded records cannot be isolated or identified. Furthermore, while the project-derived medians match the published numbers across several top countries, these matching medians reflect robust central tendencies in large samples and do not imply identical respondent populations given the slight differences in sample sizes.

### 6.3 Non-Parametric Statistics ($N_{\text{answered}} = 23,947$, Untrimmed)
- **Median:** **$75,320 USD**
- **25th Percentile ($Q_1$):** **$38,171 USD**
- **75th Percentile ($Q_3$):** **$120,596 USD**
- **Interquartile Range (IQR):** **$82,425 USD**

> [!WARNING]
> **Reporting Caveats:** Figures represent project-derived estimates from the raw public extract ($N_{\text{answered}}$), not exact reproductions of Stack Overflow's internal filtered statistics ($N_{\text{official}}$). All figures are self-reported, voluntary, unverified against tax/payroll records, and unadjusted for local purchasing power parity (PPP).

---

## 7. Multi-Select Encoding Quality
Questions such as `LanguageHaveWorkedWith` and `DatabaseHaveWorkedWith` use semicolon delimiters (`;`).
- **Parsing Verification:** No malformed or escaped delimiter artifacts were observed.
- **Dual Percentage Baselines:**
  - `pct_of_respondents`: $\frac{\text{selection\_count}}{N_{\text{answered}}} \times 100$ (sums to $>100\%$).
  - `pct_of_selections`: $\frac{\text{selection\_count}}{\sum \text{all\_selections}} \times 100$ (sums to $100\%$).

---

## 8. Data Quality Recommendations & Methodological Constraints
1. **Never Impute Arbitrary Answers:** Missing answers indicate question skipping; do not synthesize artificial values for categorical questions.
2. **Explicit Denominators:** Always state that project-derived calculations use question-specific answered respondents ($N_{\text{answered}}$) from the raw public extract, and never generalize blindly to the global developer population.
3. **Temporal Discipline:** Fielded May 29 – June 23, 2025. Because individual respondent completion timestamps are omitted from public microdata to protect privacy, daily velocity tracking is intentionally disabled to avoid fabricating artificial temporal trends.
4. **Non-Causal Language:** All analyses represent observational correlations within a self-selected sample; causal inferences are strictly prohibited.
5. **Raw Data Immutability:** Keep `data/raw/` strictly read-only and excluded from version control.
