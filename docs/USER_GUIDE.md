# User Guide: Poll Results Visualizer

**Project Name:** Poll Results Visualizer  
**Author:** Akash Das  
**Current Milestone:** Phase 8 - Final Project Polish, GitHub Preparation and Publication  
**Primary Dataset:** Stack Overflow Annual Developer Survey 2025  

---

## 1. Quick Start & Execution

### Prerequisites
- Python 3.10 or 3.11 installed.
- Git installed.
- Terminal / PowerShell.

### Step 1: Open Terminal in Project Root
```bash
cd "D:\Projects\Data Science\Poll Results Visualizer"
```

### Step 2: Activate the Virtual Environment
- **Windows PowerShell:**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **Windows Command Prompt (cmd.exe):**
  ```cmd
  .\.venv\Scripts\activate.bat
  ```
- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

### Step 3: Verify the Processed Dataset
The application loads the optimized Apache Parquet dataset from:
`data/processed/survey_results_cleaned.parquet` (9.8 MB, 49,191 rows $\times$ 176 attributes).

If building from scratch from the raw 140.8 MB CSV:
```bash
python -c "from src.datasets.stackoverflow_cleaning import clean_and_save_survey_data; clean_and_save_survey_data()"
```

### Step 4: Launch the Dashboard Application
Launch via the convenience entry point:
```bash
python run.py
```
Or directly via Streamlit:
```bash
python -m streamlit run app/streamlit_app.py
```
Open your web browser and navigate to:
`http://localhost:8501`

---

## 2. Multi-Page Application Walkthrough

The visualizer provides an interactive, 4-page analytical portal with sub-second responsive filtering powered by Streamlit caching (`@st.cache_data`).

### 1. Home / Landing Page (`app/streamlit_app.py`)
- **Survey Telemetry:** Displays core survey constants: Raw records ($49,191$), Official published base ($49,009$), Countries represented ($177$), Overall AI tool adoption rate ($78.50\%$), and Median converted compensation ($\$75,320$ USD).
- **Survey Methodology Notice:** Clear notification explaining that the dataset represents an unweighted, voluntary opt-in convenience sample.
- **Dataset Navigator:** Quick overview of the 4 dedicated analysis pages and recent data engineering hygiene metrics.

### 2. Page 1: Overview (`app/pages/1_Overview.py`)
- **Sample Flow Funnel:** Interactive visualization tracking sample attrition from total raw records ($49,191$) to official published base ($49,009$), valid compensation respondents ($23,947$), and econometric regression complete cases ($22,769$).
- **Question Inventory Table:** Itemized breakdown of all survey questions with explicit $N_{\text{answered}}$ counts, percentage completeness, and missingness counts.
- **Demographic Benchmarking:** Comparison of survey respondent distributions against official labor statistics (e.g. US Bureau of Labor Statistics) highlighting sample selection characteristics.
- **Cross-Sectional Notice:** Explicit statement confirming that daily fieldwork velocity tracking is disabled to avoid fabricating artificial temporal trends.

### 3. Page 2: Response Analysis (`app/pages/2_Response_Analysis.py`)
Features deep-dive empirical evaluations of the core research questions:
- **RQ1 - Generative AI Trust vs. Seniority:**
  - Distribution of AI accuracy trust (`AIAcc`) across professional experience cohorts.
  - Global 3-category Chi-Square test ($\chi^2 = 38.3898, df = 8, p = 6.38 \times 10^{-6}$) and collapsed binary test ($\chi^2 = 30.1175, df = 4, p = 4.63 \times 10^{-6}$).
  - Crude Odds Ratio ($\text{OR} = 1.178, p = 0.0043$) quantifying the $+4.07$ percentage point trust gap between veteran and entry-level developers.
- **RQ2 - Technology Stack Compensation Premiums:**
  - Paired current-versus-desired technology preference analysis across $27,079$ symmetric respondents.
  - Multi-select dual-denominator bar charts (% of respondents vs % of selections).
  - Extended Mincerian wage regression results (Model 3, $N = 22,769, R^2 = 0.3846$) reporting exact Halvorsen-Palmquist exponential premiums for Docker ($+13.17\%$), Rust ($+12.79\%$), AWS ($+10.91\%$), TypeScript ($+7.50\%$), Go ($+7.10\%$), and Python ($+1.32\%$).
- **RQ3 - Autonomous AI Agents vs. Job Satisfaction:**
  - One-Way ANOVA comparing job satisfaction across 6 AI agent adoption tiers ($N = 23,766, F = 11.6172, p = 3.02 \times 10^{-11}$).
  - Effect size breakdown demonstrating negligible practical variance explained ($\eta^2 = 0.002439, \omega^2 = 0.002229$, Cohen's $d = 0.128$).

### 4. Page 3: Segment Comparison (`app/pages/3_Segment_Comparison.py`)
- **Demographic Cohort Slicing:** Dynamic filtering across 5 experience brackets (<2 years, 2-5 years, 6-10 years, 11-20 years, 21+ years) and 7 primary developer roles.
- **Within-Cohort Normalization:** Grouped horizontal and vertical bar charts normalized within segment totals to avoid sample size distortion.
- **Remote Work Dynamics:** Interactive salary distribution boxplots comparing Remote, Hybrid, and In-Person arrangements.

### 5. Page 4: Data Quality & Methodological Audit (`app/pages/4_Data_Quality.py`)
- **Missingness Heatmaps & Ranking Bars:** Visual breakdown of missing data across all 172 survey attributes.
- **RemoteWork Missingness Contingency Table:** Audited $6 \times 2$ contingency table against `MainBranch` ($\chi^2 = 5,333.84, df = 5, p < 10^{-300}$, Cramér's $V = 0.3293$) with explicit Rubin missingness classification (non-MCAR).
- **Remote Work Econometric Wage Models:** Side-by-side comparison of Models A, B, and C demonstrating how controlling for country and experience attenuates the apparent remote salary gap from $+88.6\%$ to $+30.65\%$.
- **On-Demand Data Export:** In-memory CSV serialization button allowing instant download of cleaned, filtered respondent records.

---

## 3. Automated Testing & Code Quality Gates

### Running the Pytest Suite
Execute all 93 unit tests covering data loading, cleaning, validation, statistical algorithms, and dashboard components:
```bash
pytest
```
Expected output:
```
============================= 93 passed in 7.00s ==============================
```

### Running PEP 8 Linting
Verify complete style compliance across the entire codebase:
```bash
flake8 app src tests
```
Expected output: `0 errors, 0 warnings` (command exits silently with return code 0).

---

## 4. Troubleshooting & Common Questions

1. **Missing Parquet Error:**
   - *Symptom:* Dashboard warns that `data/processed/survey_results_cleaned.parquet` is not found.
   - *Fix:* Ensure the parquet file exists. If cloned without large data files, run the cleaning pipeline from `data/raw/` or download the prepared parquet file.
2. **Streamlit Port In Use:**
   - *Symptom:* `Port 8501 is already in use`.
   - *Fix:* Launch on a different port:
     ```bash
     streamlit run app/streamlit_app.py --server.port 8502
     ```
3. **Encoding Errors on Custom CSV:**
   - *Symptom:* `UnicodeDecodeError` when reading alternative survey CSVs.
   - *Fix:* The built-in loader (`src/data_loader.py`) automatically falls back to `latin-1` if `utf-8` fails.
