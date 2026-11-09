"""Stack Overflow Developer Survey 2025 Dataset Adapter.

Provides ingestion, schema interpretation, question-type detection,
and analytical processing routines for the official 2025 survey release.
Author: Akash Das
"""

from pathlib import Path
from typing import Dict, Any, List, Optional, Union
import pandas as pd
import numpy as np

# Canonical Paths relative to project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_RAW_DIR = PROJECT_ROOT / "data" / "raw" / "stackoverflow_developer_survey_2025"
DEFAULT_PUBLIC_CSV_NAMES = ["survey_results_public.csv", "results.csv"]
DEFAULT_SCHEMA_CSV_NAMES = ["survey_results_schema.csv", "schema.csv"]
DEFAULT_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DEFAULT_CLEANED_PARQUET_PATH = DEFAULT_PROCESSED_DIR / "survey_results_cleaned.parquet"
DEFAULT_CLEANED_CSV_PATH = DEFAULT_PROCESSED_DIR / "survey_results_cleaned.csv"

COL_ID = "ResponseId"

# Official Methodology Benchmarks & Population Counts
N_RAW_EXTRACT = 49191
N_OFFICIAL_QUALIFIED = 49009
OFFICIAL_QUALIFIED_POPULATION = 49009
N_OFFICIAL_SALARY_RESPONSES = 23928
N_ANSWERED_SALARY_RAW = 23947
OFFICIAL_FIELDWORK_PERIOD = "May 29, 2025 – June 23, 2025"

# Reference exchange rates for June 25, 2025 (USD per 1 unit of local currency)
# Sourced from official Stack Overflow 2025 survey conversion methodology
OFFICIAL_EXCHANGE_RATES_JUNE_2025: Dict[str, float] = {
    "USD United States dollar": 1.0,
    "EUR European Euro": 1.16015,
    "GBP Pound sterling": 1.36141,
    "CAD Canadian dollar": 0.72966,
    "AUD\tAustralian dollar": 0.65010,
    "INR Indian rupee": 0.011648,
    "BRL Brazilian real": 0.18202,
    "PLN Polish zloty": 0.27284,
    "CHF\tSwiss franc": 1.23993,
    "SEK\tSwedish krona": 0.10481,
    "UAH Ukrainian hryvnia": 0.02397,
}


class StackOverflowDataError(Exception):
    """Raised when survey data or schema cannot be found or parsed."""
    pass


def resolve_file_path(base_dir: Path, possible_names: List[str]) -> Path:
    """Find the first existing file from a list of candidate filenames."""
    for name in possible_names:
        candidate = base_dir / name
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"None of the candidate files {possible_names} were found in {base_dir}."
    )


def load_survey_data(file_path: Optional[Union[str, Path]] = None, nrows: Optional[int] = None) -> pd.DataFrame:
    """Load the official Stack Overflow 2025 respondent-level CSV.

    Args:
        file_path: Optional direct path to CSV. If omitted, checks default directory.
        nrows: Optional row limit for fast exploration/testing.

    Returns:
        pd.DataFrame: Respondent-level survey responses.

    Raises:
        StackOverflowDataError: If the official dataset file is missing.
    """
    if file_path is not None:
        target_path = Path(file_path)
    else:
        try:
            target_path = resolve_file_path(DEFAULT_RAW_DIR, DEFAULT_PUBLIC_CSV_NAMES)
        except FileNotFoundError as e:
            raise StackOverflowDataError(
                f"Official Stack Overflow 2025 dataset not found in {DEFAULT_RAW_DIR}.\n"
                "To obtain the official data, download 'results.csv' from:\n"
                "https://github.com/StackExchange/Survey/tree/main/packages/archive/2025\n"
                "or via official Git LFS media endpoint:\n"
                "https://media.githubusercontent.com/media/StackExchange/Survey/main/"
                "packages/archive/2025/results.csv\n"
                f"and place it at: {DEFAULT_RAW_DIR / 'survey_results_public.csv'}"
            ) from e

    if not target_path.exists():
        raise StackOverflowDataError(f"Survey dataset file does not exist: {target_path}")

    try:
        df = pd.read_csv(target_path, low_memory=False, nrows=nrows)
    except Exception as e:
        raise StackOverflowDataError(f"Failed to load survey data from {target_path}: {e}") from e

    if COL_ID not in df.columns:
        raise StackOverflowDataError(f"Missing mandatory respondent key '{COL_ID}' in dataset.")

    return df


def load_cleaned_survey_data(file_path: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """Load the cleaned Stack Overflow 2025 processed survey dataset.

    Prefers Apache Parquet for high-performance vectorized I/O, falling back to CSV.

    Args:
        file_path: Optional direct path to parquet or CSV. If omitted, checks default processed directory.

    Returns:
        pd.DataFrame: Cleaned respondent-level survey dataset.

    Raises:
        StackOverflowDataError: If the processed dataset file is missing.
    """
    if file_path is not None:
        target_path = Path(file_path)
    else:
        if DEFAULT_CLEANED_PARQUET_PATH.exists():
            target_path = DEFAULT_CLEANED_PARQUET_PATH
        elif DEFAULT_CLEANED_CSV_PATH.exists():
            target_path = DEFAULT_CLEANED_CSV_PATH
        else:
            raise StackOverflowDataError(
                f"Cleaned dataset not found in {DEFAULT_PROCESSED_DIR}. "
                "Run Phase 3 cleaning pipeline to generate survey_results_cleaned.parquet."
            )

    if not target_path.exists():
        raise StackOverflowDataError(f"Processed dataset file does not exist: {target_path}")

    try:
        if target_path.suffix.lower() == ".parquet":
            df = pd.read_parquet(target_path)
        else:
            df = pd.read_csv(target_path, low_memory=False)
    except Exception as e:
        raise StackOverflowDataError(f"Failed to load cleaned survey data from {target_path}: {e}") from e

    if COL_ID not in df.columns:
        raise StackOverflowDataError(f"Missing mandatory respondent key '{COL_ID}' in cleaned dataset.")

    return df


def load_survey_schema(file_path: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """Load the official Stack Overflow 2025 survey schema questionnaire dictionary.

    Args:
        file_path: Optional direct path to schema CSV.

    Returns:
        pd.DataFrame: Survey question schema dictionary.

    Raises:
        StackOverflowDataError: If schema file is missing.
    """
    if file_path is not None:
        target_path = Path(file_path)
    else:
        try:
            target_path = resolve_file_path(DEFAULT_RAW_DIR, DEFAULT_SCHEMA_CSV_NAMES)
        except FileNotFoundError as e:
            raise StackOverflowDataError(
                f"Official Stack Overflow 2025 schema not found in {DEFAULT_RAW_DIR}.\n"
                "Download 'schema.csv' from:\n"
                "https://media.githubusercontent.com/media/StackExchange/Survey/main/packages/archive/2025/schema.csv\n"
                f"and place it at: {DEFAULT_RAW_DIR / 'survey_results_schema.csv'}"
            ) from e

    if not target_path.exists():
        raise StackOverflowDataError(f"Survey schema file does not exist: {target_path}")

    try:
        schema_df = pd.read_csv(target_path)
    except Exception as e:
        raise StackOverflowDataError(f"Failed to load schema from {target_path}: {e}") from e

    return schema_df


def get_question_text(schema_df: pd.DataFrame, qname: str) -> str:
    """Retrieve official question wording for a given question identifier."""
    if schema_df.empty or "qname" not in schema_df.columns:
        return qname

    matches = schema_df[schema_df["qname"] == qname]
    if matches.empty:
        # Check by qid
        matches = schema_df[schema_df["qid"] == qname]

    if not matches.empty:
        row = matches.iloc[0]
        q_text = str(row.get("question", qname))
        sub = row.get("sub")
        if pd.notnull(sub) and str(sub).strip():
            return f"{q_text} ({sub})"
        return q_text
    return qname


def analyze_single_select(
    df: pd.DataFrame,
    column: str,
    top_n: Optional[int] = None,
    dropna: bool = True
) -> pd.DataFrame:
    """Compute distribution metrics for a single-select categorical survey question.

    Args:
        df: Input survey DataFrame.
        column: Survey column name to analyze.
        top_n: Optional limit to top N categories.
        dropna: Whether to exclude missing values from the base denominator.

    Returns:
        pd.DataFrame: Contains [category, response_count, percentage].
    """
    if column not in df.columns or df.empty:
        return pd.DataFrame(columns=["category", "response_count", "percentage"])

    series = df[column]
    if dropna:
        series = series.dropna()

    valid_respondents = len(series)
    if valid_respondents == 0:
        return pd.DataFrame(columns=["category", "response_count", "percentage"])

    counts = series.value_counts(dropna=dropna).reset_index()
    counts.columns = ["category", "response_count"]

    counts["percentage"] = (counts["response_count"] / valid_respondents) * 100.0
    counts["percentage"] = counts["percentage"].round(2)

    if top_n is not None and top_n > 0:
        counts = counts.head(top_n)

    return counts.reset_index(drop=True)


def analyze_multi_select(
    df: pd.DataFrame,
    column: str,
    delimiter: str = ";",
    top_n: Optional[int] = None
) -> pd.DataFrame:
    """Parse and calculate distributions for multi-select questions.

    Percentages are computed against two distinct baselines:
    1. `pct_of_respondents`: Share of valid respondents who selected this option (sum may exceed 100%).
    2. `pct_of_selections`: Share of total individual checkmark selections.

    Args:
        df: Input survey DataFrame.
        column: Semicolon-delimited multi-select column.
        delimiter: Multi-select separator (default: ';').
        top_n: Optional limit to top N options.

    Returns:
        pd.DataFrame: Contains [option, response_count, pct_of_respondents, pct_of_selections].
    """
    if column not in df.columns or df.empty:
        return pd.DataFrame(columns=["option", "response_count", "pct_of_respondents", "pct_of_selections"])

    valid_series = df[column].dropna()
    total_valid_respondents = len(valid_series)

    if total_valid_respondents == 0:
        return pd.DataFrame(columns=["option", "response_count", "pct_of_respondents", "pct_of_selections"])

    # Explode multi-select responses
    all_selections = (
        valid_series.astype(str)
        .str.split(delimiter)
        .explode()
        .str.strip()
    )
    all_selections = all_selections[all_selections != ""]

    total_selections = len(all_selections)
    if total_selections == 0:
        return pd.DataFrame(columns=["option", "response_count", "pct_of_respondents", "pct_of_selections"])

    counts = all_selections.value_counts().reset_index()
    counts.columns = ["option", "response_count"]

    # Calculate dual percentages
    counts["pct_of_respondents"] = ((counts["response_count"] / total_valid_respondents) * 100.0).round(2)
    counts["pct_of_selections"] = ((counts["response_count"] / total_selections) * 100.0).round(2)

    if top_n is not None and top_n > 0:
        counts = counts.head(top_n)

    return counts.reset_index(drop=True)


def cross_tabulate_single(
    df: pd.DataFrame,
    question_col: str,
    segment_col: str,
    normalize: str = "segment"
) -> pd.DataFrame:
    """Cross-tabulate a single-select question across demographic cohorts.

    Args:
        df: Input survey DataFrame.
        question_col: Survey question column.
        segment_col: Demographic segmentation column (e.g., 'Age', 'Employment').
        normalize: 'segment' for within-cohort shares, or 'all' for total sample share.

    Returns:
        pd.DataFrame: Contains [segment, category, count, percentage].
    """
    if question_col not in df.columns or segment_col not in df.columns or df.empty:
        return pd.DataFrame(columns=[segment_col, "category", "count", "percentage"])

    valid_df = df[[segment_col, question_col]].dropna()
    if valid_df.empty:
        return pd.DataFrame(columns=[segment_col, "category", "count", "percentage"])

    grouped = (
        valid_df.groupby([segment_col, question_col], observed=False)
        .size()
        .reset_index(name="count")
    )
    grouped.columns = [segment_col, "category", "count"]

    if normalize == "segment":
        totals = valid_df.groupby(segment_col, observed=False).size().to_dict()
        grouped["cohort_total"] = grouped[segment_col].map(totals)
        grouped["percentage"] = (
            grouped.apply(
                lambda r: round((r["count"] / r["cohort_total"]) * 100.0, 2)
                if r["cohort_total"] > 0 else 0.0,
                axis=1
            )
        )
    else:
        total_rows = len(valid_df)
        grouped["percentage"] = ((grouped["count"] / total_rows) * 100.0).round(2)

    return grouped.sort_values(by=[segment_col, "count"], ascending=[True, False]).reset_index(drop=True)


def convert_local_compensation_to_usd(
    comp_total: Union[float, int, pd.Series],
    currency: Union[str, pd.Series],
    exchange_rates: Optional[Dict[str, float]] = None
) -> Union[float, pd.Series]:
    """Convert self-reported annual local compensation to USD using reference exchange rates.

    Under official Stack Overflow methodology, respondents report annual compensation
    in their day-to-day currency (`Currency`), which is subsequently converted into USD
    (`ConvertedCompYearly`) based on exchange rates recorded on June 25, 2025.

    Args:
        comp_total: Raw numerical self-reported annual compensation.
        currency: Day-to-day currency label string (e.g., 'EUR European Euro').
        exchange_rates: Optional custom conversion mapping. Defaults to OFFICIAL_EXCHANGE_RATES_JUNE_2025.

    Returns:
        Union[float, pd.Series]: Converted compensation in USD, or NaN if unconvertible.
    """
    rates = exchange_rates or OFFICIAL_EXCHANGE_RATES_JUNE_2025

    if isinstance(comp_total, pd.Series) and isinstance(currency, pd.Series):
        def _convert_row(val, curr):
            if pd.isna(val) or pd.isna(curr):
                return np.nan
            try:
                num = float(val)
                if num <= 0:
                    return np.nan
            except (ValueError, TypeError):
                return np.nan

            curr_clean = str(curr).strip()
            # Match currency in exchange rate table
            rate = rates.get(curr_clean)
            if rate is None:
                # Try prefix lookup (e.g. 'USD', 'EUR')
                for k, v in rates.items():
                    if curr_clean.startswith(k[:3]):
                        rate = v
                        break
            if rate is not None:
                return round(num * rate, 2)
            return np.nan

        return pd.Series(
            [_convert_row(v, c) for v, c in zip(comp_total, currency)],
            index=comp_total.index
        )
    else:
        if pd.isna(comp_total) or pd.isna(currency):
            return np.nan
        try:
            num = float(comp_total)
            if num <= 0:
                return np.nan
        except (ValueError, TypeError):
            return np.nan

        curr_clean = str(currency).strip()
        rate = rates.get(curr_clean)
        if rate is None:
            for k, v in rates.items():
                if curr_clean.startswith(k[:3]):
                    rate = v
                    break
        if rate is not None:
            return round(num * rate, 2)
        return np.nan


def get_compensation_summary(
    df: pd.DataFrame,
    group_by: Optional[str] = None,
    trim_outliers: bool = False
) -> pd.DataFrame:
    """Compute central tendencies and quartiles for annual compensation in USD.

    Methodology Notice:
        - Primary Field: Uses `ConvertedCompYearly`, the official pre-converted annual
          USD compensation column provided in the raw extract (converted by Stack Overflow
          using June 25, 2025 exchange rates).
        - Local Currency Clarification: `CompTotal` in the raw survey was reported across 142
          distinct currencies (`Currency`) and must not be aggregated directly as USD.
        - Population Distinction: In the raw public extract, N_answered = 23,947 respondents
          have non-null ConvertedCompYearly. This project-derived count differs from Stack
          Overflow's published salary report count of N_official = 23,928 by a net difference
          of 19 records (individual qualification flags are omitted from the public microdata).
        - Non-Parametric Metrics: Reports Median, Q1, Q3, and IQR to resist skewness.
        - No Arbitrary Boundaries: Evaluates all positive values without arbitrary cutoffs
          unless trim_outliers is explicitly requested.

    Args:
        df: Input survey DataFrame.
        group_by: Optional grouping column (e.g., 'DevType', 'Age', 'Country').
        trim_outliers: If True, restricts reporting to values between $1,000 and $2,000,000 USD.

    Returns:
        pd.DataFrame: Summary table containing N_answered, median, 25th, and 75th percentiles.
    """
    comp_col = "ConvertedCompYearly"
    if comp_col not in df.columns or df.empty:
        return pd.DataFrame(columns=[
            "group", "n_answered", "valid_respondents", "median_usd", "p25_usd", "p75_usd", "iqr_usd"
        ])

    cols_to_use = [comp_col] + ([group_by] if group_by and group_by in df.columns else [])
    valid = df[cols_to_use].dropna().copy()
    valid[comp_col] = pd.to_numeric(valid[comp_col], errors="coerce")
    valid = valid.dropna(subset=[comp_col])
    valid = valid[valid[comp_col] > 0]

    if trim_outliers:
        valid = valid[(valid[comp_col] >= 1000) & (valid[comp_col] <= 2000000)]

    if valid.empty:
        return pd.DataFrame(columns=[
            "group", "n_answered", "valid_respondents", "median_usd", "p25_usd", "p75_usd", "iqr_usd"
        ])

    if group_by and group_by in valid.columns:
        res = (
            valid.groupby(group_by, observed=False)[comp_col]
            .agg(
                n_answered="count",
                median_usd="median",
                p25_usd=lambda x: np.percentile(x, 25),
                p75_usd=lambda x: np.percentile(x, 75)
            )
            .reset_index()
        )
        res["iqr_usd"] = res["p75_usd"] - res["p25_usd"]
        res["valid_respondents"] = res["n_answered"]  # Backward compatibility alias
        res.columns = ["group", "n_answered", "median_usd", "p25_usd", "p75_usd", "iqr_usd", "valid_respondents"]
        return res.sort_values(by="median_usd", ascending=False).reset_index(drop=True)
    else:
        p25 = float(np.percentile(valid[comp_col], 25))
        p75 = float(np.percentile(valid[comp_col], 75))
        n_count = len(valid)
        return pd.DataFrame([{
            "group": "Overall Sample",
            "n_answered": n_count,
            "valid_respondents": n_count,  # Backward compatibility alias
            "median_usd": float(valid[comp_col].median()),
            "p25_usd": p25,
            "p75_usd": p75,
            "iqr_usd": p75 - p25,
        }])


def build_poll_adapter_table(
    df: pd.DataFrame,
    max_rows: Optional[int] = 10000,
    segment_col: str = "Age"
) -> pd.DataFrame:
    """Transform wide-format survey responses into a tidy poll schema for dashboard integration.

    Extracts core AI and employment questions while preserving links between respondents,
    questions, answers, and demographic cohorts.

    Cross-Sectional Notice:
        The Stack Overflow Annual Developer Survey 2025 is a single cross-sectional study
        fielded from May 29 to June 23, 2025. Individual respondent submission timestamps are
        omitted from public microdata to protect privacy. Accordingly, `response_date` is
        explicitly set to None (no artificial date is fabricated).

    Args:
        df: Input raw Stack Overflow survey DataFrame.
        max_rows: Optional row limit for responsive UI loading.
        segment_col: Column to use for demographic segmentation (default: 'Age').

    Returns:
        pd.DataFrame: Conforms to [respondent_id, question, option, response_date, segment].
    """
    if df.empty:
        return pd.DataFrame(columns=[
            "respondent_id", "question", "option", "response_date", "segment"
        ])

    sample_df = df.head(max_rows) if max_rows else df
    target_questions = {
        "AISelect": "Do you currently use AI tools in your development process?",
        "AISent": "How favorable is your stance on using AI tools?",
        "AIAcc": "How much do you trust the accuracy of AI tools?",
        "AIAgents": "Are you using AI agents in your work?",
        "AIThreat": "Do you believe AI is a threat to your current job?",
        "RemoteWork": "What is your current work arrangement?",
        "Employment": "What is your primary employment status?",
    }

    records = []

    for _, row in sample_df.iterrows():
        r_id = f"SO-{row.get(COL_ID, '')}"
        segment_val = str(row.get(segment_col, "Unknown")) if pd.notnull(row.get(segment_col)) else "Unknown"

        for col_name, q_label in target_questions.items():
            if col_name in row and pd.notnull(row[col_name]):
                val = str(row[col_name]).strip()
                if val:
                    records.append({
                        "respondent_id": r_id,
                        "question": q_label,
                        "option": val,
                        "response_date": None,  # Cross-sectional survey: No fabricated dates
                        "segment": segment_val,
                    })

    if not records:
        return pd.DataFrame(columns=[
            "respondent_id", "question", "option", "response_date", "segment"
        ])

    return pd.DataFrame(records)


def get_survey_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate executive overview metrics for the 2025 survey.

    Standardized Population Terminology:
        - `n_raw`: All rows in the downloaded public CSV (49,191).
        - `n_official`: The official published qualified response base (49,009).
        - `n_answered_ai`: Non-missing responses to AISelect in the raw extract (33,720).
        - `n_answered_comp`: Non-missing converted compensation in raw extract (23,947).
        - `n_official_comp`: Published salary response base on official website (23,928).
        - `comp_discrepancy`: Net difference of 19 records between derived and published counts.
    """
    if df.empty:
        return {
            "n_raw": 0,
            "n_official": N_OFFICIAL_QUALIFIED,
            "total_respondents": 0,
            "raw_records_count": 0,
            "official_published_count": N_OFFICIAL_QUALIFIED,
            "total_variables": 0,
            "countries_count": 0,
            "n_answered_ai": 0,
            "ai_valid_count": 0,
            "ai_users_count": 0,
            "ai_adoption_rate": 0.0,
            "n_answered_comp": 0,
            "comp_valid_count": 0,
            "n_official_comp": N_OFFICIAL_SALARY_RESPONSES,
            "comp_discrepancy": 0,
            "median_comp_usd": None,
            "comp_caveat": "No compensation data available."
        }

    raw_count = len(df)
    total_vars = len(df.columns)
    countries = df["Country"].dropna().nunique() if "Country" in df.columns else 0

    # AI adoption rate (AISelect: 'Yes')
    ai_rate = 0.0
    ai_count = 0
    ai_answered = 0
    if "AISelect" in df.columns:
        valid_ai = df["AISelect"].dropna()
        ai_answered = len(valid_ai)
        if ai_answered > 0:
            ai_yes = valid_ai.str.lower().str.startswith("yes").sum()
            ai_count = int(ai_yes)
            ai_rate = round((ai_yes / ai_answered) * 100.0, 2)

    # Median compensation using official pre-converted USD column (untrimmed)
    med_comp = None
    comp_answered = 0
    if "ConvertedCompYearly" in df.columns:
        valid_comp = pd.to_numeric(df["ConvertedCompYearly"], errors="coerce").dropna()
        valid_comp = valid_comp[valid_comp > 0]
        comp_answered = len(valid_comp)
        if comp_answered > 0:
            med_comp = float(round(valid_comp.median(), 2))

    discrepancy = comp_answered - N_OFFICIAL_SALARY_RESPONSES if raw_count == N_RAW_EXTRACT else 0

    return {
        "n_raw": raw_count,
        "n_official": N_OFFICIAL_QUALIFIED,
        "total_respondents": raw_count,
        "raw_records_count": raw_count,
        "official_published_count": N_OFFICIAL_QUALIFIED,
        "total_variables": total_vars,
        "countries_count": countries,
        "n_answered_ai": ai_answered,
        "ai_valid_count": ai_answered,
        "ai_users_count": ai_count,
        "ai_adoption_rate": ai_rate,
        "n_answered_comp": comp_answered,
        "comp_valid_count": comp_answered,
        "n_official_comp": N_OFFICIAL_SALARY_RESPONSES,
        "comp_discrepancy": discrepancy,
        "median_comp_usd": med_comp,
        "comp_caveat": (
            f"Pre-converted annual USD compensation (N_answered = {comp_answered:,} in raw extract; "
            f"N_official = {N_OFFICIAL_SALARY_RESPONSES:,} published). Net difference of {discrepancy} records "
            "represents a population-count reconciliation limitation, as public microdata does not expose "
            "sufficient qualification-screening information to identify individual excluded records. "
            "Unverified against payroll data."
        )
    }
