"""Unit tests for export module.

Author: Akash Das
"""

import pandas as pd
from src.export import export_dataframe_to_csv, get_csv_download_bytes


def test_export_dataframe_to_csv(tmp_path):
    """Verify DataFrame exports properly to a destination CSV file."""
    df = pd.DataFrame({"col1": [1, 2], "col2": ["A", "B"]})
    out_path = export_dataframe_to_csv(df, "test_export.csv", output_directory=tmp_path)
    assert out_path.exists()
    loaded = pd.read_csv(out_path)
    pd.testing.assert_frame_equal(df, loaded)


def test_get_csv_download_bytes():
    """Verify DataFrame converts into UTF-8 CSV bytes."""
    df = pd.DataFrame({"col1": [1, 2], "col2": ["A", "B"]})
    raw_bytes = get_csv_download_bytes(df)
    assert isinstance(raw_bytes, bytes)
    text = raw_bytes.decode("utf-8")
    assert "col1,col2" in text
    assert "1,A" in text
