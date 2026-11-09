"""Unit tests for Stack Overflow 2025 Dataset Adapter.

Author: Akash Das
"""

import pytest
from pathlib import Path
import pandas as pd

from src.datasets.stackoverflow_2025 import (
    load_survey_data,
    load_cleaned_survey_data,
    get_question_text,
    analyze_single_select,
    analyze_multi_select,
    cross_tabulate_single,
    get_compensation_summary,
    get_survey_kpis,
    convert_local_compensation_to_usd,
    build_poll_adapter_table,
    StackOverflowDataError,
    resolve_file_path,
    OFFICIAL_QUALIFIED_POPULATION,
    N_RAW_EXTRACT,
    N_OFFICIAL_QUALIFIED,
    N_OFFICIAL_SALARY_RESPONSES,
    N_ANSWERED_SALARY_RAW,
)
from src.analysis import get_trend_over_time


@pytest.fixture
def sample_survey_df():
    """Create a small deterministic respondent-level survey DataFrame."""
    return pd.DataFrame({
        "ResponseId": [1, 2, 3, 4, 5],
        "Age": ["18-24 years old", "25-34 years old", "25-34 years old", "35-44 years old", None],
        "Employment": ["Employed", "Employed", "Student", "Employed", "Not employed"],
        "LanguageHaveWorkedWith": [
            "Python;SQL",
            "JavaScript;TypeScript;Python",
            "Python",
            "Java;C#",
            None
        ],
        "AISelect": [
            "Yes, I use AI tools daily",
            "Yes, I use AI tools daily",
            "No, and I don't plan to",
            "Yes, I use AI tools weekly",
            None
        ],
        "ConvertedCompYearly": [60000.0, 120000.0, None, 95000.0, None],
        "Country": ["United States of America", "Germany", "India", "United States of America", "Canada"],
    })


@pytest.fixture
def sample_schema_df():
    """Create a small deterministic schema DataFrame."""
    return pd.DataFrame({
        "qid": ["QID1", "QID2", "QID3"],
        "qname": ["Age", "LanguageHaveWorkedWith", "AISelect"],
        "question": [
            "What is your age?",
            "Which programming languages have you worked with?",
            "Do you currently use AI tools in your development process?"
        ],
        "type": ["MC", "MC", "MC"],
        "sub": [None, None, None],
        "sq_id": [None, None, None]
    })


def test_load_survey_data_missing_file_raises_error(tmp_path):
    """Verify loading from nonexistent path raises StackOverflowDataError."""
    fake_path = tmp_path / "missing_survey.csv"
    with pytest.raises(StackOverflowDataError, match="does not exist"):
        load_survey_data(fake_path)


def test_load_survey_data_missing_id_col(tmp_path):
    """Verify loading dataset without ResponseId raises StackOverflowDataError."""
    bad_csv = tmp_path / "bad_survey.csv"
    bad_csv.write_text("ColA,ColB\n1,2\n", encoding="utf-8")
    with pytest.raises(StackOverflowDataError, match="Missing mandatory respondent key"):
        load_survey_data(bad_csv)


def test_resolve_file_path_finds_first_existing(tmp_path):
    """Verify resolve_file_path selects the first matching candidate file."""
    f2 = tmp_path / "candidate_two.csv"
    f2.write_text("data", encoding="utf-8")
    resolved = resolve_file_path(tmp_path, ["candidate_one.csv", "candidate_two.csv"])
    assert resolved.name == "candidate_two.csv"


def test_get_question_text(sample_schema_df):
    """Verify question text lookup retrieves exact text from schema."""
    text = get_question_text(sample_schema_df, "Age")
    assert text == "What is your age?"

    fallback = get_question_text(sample_schema_df, "UnknownQuestion")
    assert fallback == "UnknownQuestion"


def test_analyze_single_select(sample_survey_df):
    """Verify single-select frequency and percentage calculations."""
    res = analyze_single_select(sample_survey_df, "Age")
    assert len(res) == 3
    # 4 non-null respondents: 2 are '25-34 years old' (50.0%)
    top_row = res.iloc[0]
    assert top_row["category"] == "25-34 years old"
    assert top_row["response_count"] == 2
    assert top_row["percentage"] == 50.0


def test_analyze_single_select_empty_or_missing_col(sample_survey_df):
    """Verify single-select returns empty schema on missing columns or empty df."""
    res = analyze_single_select(sample_survey_df, "NonexistentCol")
    assert res.empty
    assert list(res.columns) == ["category", "response_count", "percentage"]

    empty_df = pd.DataFrame(columns=["Age"])
    res2 = analyze_single_select(empty_df, "Age")
    assert res2.empty


def test_analyze_multi_select(sample_survey_df):
    """Verify multi-select semicolon parsing and dual percentage baselines."""
    res = analyze_multi_select(sample_survey_df, "LanguageHaveWorkedWith")
    # 4 valid respondents, options: Python (3), SQL (1), JavaScript (1), TypeScript (1), Java (1), C# (1)
    # Total selections = 8
    py_row = res[res["option"] == "Python"].iloc[0]
    assert py_row["response_count"] == 3
    # 3 / 4 respondents = 75.0%
    assert py_row["pct_of_respondents"] == 75.0
    # 3 / 8 selections = 37.5%
    assert py_row["pct_of_selections"] == 37.5


def test_analyze_multi_select_empty(sample_survey_df):
    """Verify multi-select handles missing or empty columns gracefully."""
    res = analyze_multi_select(sample_survey_df, "MissingCol")
    assert res.empty
    assert list(res.columns) == ["option", "response_count", "pct_of_respondents", "pct_of_selections"]


def test_cross_tabulate_single(sample_survey_df):
    """Verify demographic cross-tabulation within-cohort percentages."""
    res = cross_tabulate_single(sample_survey_df, "AISelect", "Country")
    assert not res.empty
    us_rows = res[res["Country"] == "United States of America"]
    assert len(us_rows) == 2
    # Both US respondents selected a form of Yes
    assert us_rows["count"].sum() == 2
    assert us_rows["percentage"].sum() == 100.0


def test_get_compensation_summary(sample_survey_df):
    """Verify compensation statistics (median, p25, p75) calculation."""
    summary = get_compensation_summary(sample_survey_df)
    assert len(summary) == 1
    # Valid salaries: [60000.0, 95000.0, 120000.0] -> Median = 95000.0
    assert summary.iloc[0]["valid_respondents"] == 3
    assert summary.iloc[0]["median_usd"] == 95000.0


def test_get_survey_kpis(sample_survey_df):
    """Verify executive KPI summary computation with standardized population terms."""
    kpis = get_survey_kpis(sample_survey_df)
    assert kpis["n_raw"] == 5
    assert kpis["n_official"] == N_OFFICIAL_QUALIFIED
    assert kpis["total_respondents"] == 5
    assert kpis["raw_records_count"] == 5
    assert kpis["official_published_count"] == OFFICIAL_QUALIFIED_POPULATION
    assert kpis["countries_count"] == 4
    assert kpis["n_answered_ai"] == 4  # 4 non-null AISelect
    assert kpis["ai_users_count"] == 3  # 3 'Yes' respondents
    assert kpis["ai_adoption_rate"] == 75.0  # 3 of 4 non-null
    assert kpis["n_answered_comp"] == 3  # 3 non-null ConvertedCompYearly
    assert kpis["n_official_comp"] == N_OFFICIAL_SALARY_RESPONSES
    assert kpis["median_comp_usd"] == 95000.0


def test_compensation_summary_distinguishes_answered_and_official(sample_survey_df):
    """Verify compensation summary includes N_answered distinct from official counts."""
    summary = get_compensation_summary(sample_survey_df)
    assert "n_answered" in summary.columns
    assert summary.iloc[0]["n_answered"] == 3
    assert summary.iloc[0]["median_usd"] == 95000.0


def test_population_constants_integrity():
    """Verify official population and salary benchmarks."""
    assert N_RAW_EXTRACT == 49191
    assert N_OFFICIAL_QUALIFIED == 49009
    assert N_OFFICIAL_SALARY_RESPONSES == 23928
    assert N_ANSWERED_SALARY_RAW == 23947
    # Verify the exact 19-record discrepancy
    assert N_ANSWERED_SALARY_RAW - N_OFFICIAL_SALARY_RESPONSES == 19
    # Verify the exact 182-record qualification discrepancy
    assert N_RAW_EXTRACT - N_OFFICIAL_QUALIFIED == 182


def test_convert_local_compensation_to_usd():
    """Verify documented currency conversion to annual USD."""
    # Test scalar conversion
    eur_usd = convert_local_compensation_to_usd(50000, "EUR European Euro")
    assert eur_usd == round(50000 * 1.16015, 2)

    usd_usd = convert_local_compensation_to_usd(100000, "USD United States dollar")
    assert usd_usd == 100000.0

    gbp_usd = convert_local_compensation_to_usd(70000, "GBP Pound sterling")
    assert gbp_usd == round(70000 * 1.36141, 2)

    # Test Series conversion
    comp_series = pd.Series([50000, 100000, 2000000])
    curr_series = pd.Series(["EUR European Euro", "USD United States dollar", "INR Indian rupee"])
    res_series = convert_local_compensation_to_usd(comp_series, curr_series)
    assert len(res_series) == 3
    assert res_series.iloc[1] == 100000.0
    assert res_series.iloc[2] == round(2000000 * 0.011648, 2)


def test_convert_local_compensation_unconvertible_or_missing():
    """Verify missing, invalid, or unrecognized currencies return NaN."""
    import numpy as np

    assert np.isnan(convert_local_compensation_to_usd(None, "USD United States dollar"))
    assert np.isnan(convert_local_compensation_to_usd(50000, None))
    assert np.isnan(convert_local_compensation_to_usd(50000, "XYZ Unrecognized Currency"))
    assert np.isnan(convert_local_compensation_to_usd(-500, "EUR European Euro"))
    assert np.isnan(convert_local_compensation_to_usd("invalid_number", "USD United States dollar"))


def test_build_poll_adapter_table_has_no_fabricated_dates(sample_survey_df):
    """Verify adapter sets response_date to None and presents no false temporal trends."""
    adapter_df = build_poll_adapter_table(sample_survey_df)
    assert not adapter_df.empty
    assert "response_date" in adapter_df.columns
    # Ensure no fabricated dates are assigned
    assert adapter_df["response_date"].isna().all()

    # Ensure temporal trend calculation returns empty DataFrame
    trend_df = get_trend_over_time(adapter_df)
    assert trend_df.empty
    assert list(trend_df.columns) == ["date", "response_count"]


def test_get_compensation_summary_untrimmed():
    """Verify compensation summary does not drop valid salaries by arbitrary boundary."""
    # Test dataset with values under $1,000 and above $2,000,000
    df = pd.DataFrame({
        "ConvertedCompYearly": [500.0, 50000.0, 100000.0, 3000000.0]
    })
    # Untrimmed should retain all 4 values: [500, 50000, 100000, 3000000]
    # Median of [500, 50000, 100000, 3000000] = (50000 + 100000) / 2 = 75000
    summary = get_compensation_summary(df, trim_outliers=False)
    assert summary.iloc[0]["valid_respondents"] == 4
    assert summary.iloc[0]["median_usd"] == 75000.0


def test_country_compensation_reconciliation_exhaustive():
    """Verify country groups are mutually exclusive and sum exactly to total compensation."""
    # Test on synthetic data
    df = pd.DataFrame({
        "Country": ["United States of America", "Germany", "France", "India", "Canada", "Otherland"],
        "ConvertedCompYearly": [100000.0, 80000.0, 60000.0, 20000.0, 90000.0, 50000.0]
    })
    named_countries = [
        "United States of America", "Germany", "France", "India", "Canada"
    ]
    comp_df = df[df["ConvertedCompYearly"].notna()]
    named_count = int(comp_df["Country"].isin(named_countries).sum())
    residual_count = int((~comp_df["Country"].isin(named_countries)).sum())
    assert named_count + residual_count == len(comp_df)

    # If canonical raw extract exists on disk, verify actual raw data exhaustiveness and exact counts
    from pathlib import Path
    raw_path = Path("data/raw/stackoverflow_developer_survey_2025/survey_results_public.csv")
    if raw_path.exists():
        raw_df = pd.read_csv(raw_path, usecols=["Country", "ConvertedCompYearly"], low_memory=False)
        valid_comp = raw_df[raw_df["ConvertedCompYearly"].notna()]
        total_comp = len(valid_comp)
        assert total_comp == 23947

        # 6-country grouping (US, Germany, UK, Canada, France, India)
        six_countries = [
            "United States of America",
            "Germany",
            "United Kingdom of Great Britain and Northern Ireland",
            "Canada",
            "France",
            "India"
        ]
        six_counts = {c: int((valid_comp["Country"] == c).sum()) for c in six_countries}
        assert six_counts["United States of America"] == 5243
        assert six_counts["Germany"] == 2141
        assert six_counts["United Kingdom of Great Britain and Northern Ireland"] == 1486
        assert six_counts["Canada"] == 915
        assert six_counts["France"] == 1027
        assert six_counts["India"] == 1096

        residual_six = int((~valid_comp["Country"].isin(six_countries)).sum())
        assert residual_six == 12039
        assert sum(six_counts.values()) + residual_six == total_comp

        # 5 official published countries (US, Germany, UK, France, India)
        five_countries = [
            "United States of America",
            "Germany",
            "United Kingdom of Great Britain and Northern Ireland",
            "France",
            "India"
        ]
        five_counts = {c: int((valid_comp["Country"] == c).sum()) for c in five_countries}
        residual_five = int((~valid_comp["Country"].isin(five_countries)).sum())
        assert residual_five == 12954
        assert sum(five_counts.values()) + residual_five == total_comp


def test_load_cleaned_survey_data_parquet():
    """Verify loading cleaned survey dataset from processed parquet."""
    pq_path = Path("data/processed/survey_results_cleaned.parquet")
    if pq_path.exists():
        df = load_cleaned_survey_data(pq_path)
        assert len(df) == 49191
        assert len(df.columns) == 176
        assert "YearsCode_num" in df.columns
        assert "WorkExp_num" in df.columns
        assert "Comp_valid_usd" in df.columns
        assert "Comp_status" in df.columns
