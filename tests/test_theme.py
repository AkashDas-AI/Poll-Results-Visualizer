"""Unit tests for centralized Light/Dark Mode theme architecture.

Validates theme configuration schemas, session-state lifecycle, Plotly figure styling,
defensive null-safety, invalid-input guards, and trace/data immutability.

Author: Akash Das
Project: Poll Results Visualizer
Phase: Phase 3 — Theme Architecture Hardening
"""

import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

from app.components.charts import (
    plot_distribution_bar,
    plot_distribution_pie,
    plot_segment_breakdown_bar,
    plot_trend_line,
    plot_horizontal_bar_with_denominators,
    plot_technology_comparison_bar,
    plot_compensation_box,
    plot_missingness_ranking_bar,
    plot_sample_flow_funnel,
    _empty_figure,
)
from app.components.theme import (
    DARK_THEME,
    LIGHT_THEME,
    THEMES,
    get_current_theme,
    get_theme_config,
    set_theme,
    _on_theme_toggle_change,
    render_theme_toggle,
    apply_custom_theme,
    apply_chart_theme,
    CUSTOM_THEME_CSS_DARK,
    CUSTOM_THEME_CSS_LIGHT,
)


REQUIRED_PALETTE_KEYS = {
    "name",
    "bg_main",
    "bg_sidebar",
    "bg_card",
    "text_primary",
    "text_secondary",
    "accent_primary",
    "indicator_positive",
    "indicator_warning",
    "border",
    "plotly_template",
    "chart_grid",
    "chart_font_color",
    "chart_secondary_color",
    "chart_paper",
    "chart_bg",
    "hover_bg",
    "hover_text",
    "hover_border",
    "font_family",
}


@pytest.fixture(autouse=True)
def clean_session_state():
    """Ensure clean session state for each test run."""
    if hasattr(st, "session_state"):
        st.session_state.clear()
    yield
    if hasattr(st, "session_state"):
        st.session_state.clear()


# -----------------------------------------------------------------------------
# 1. Palette Schema and Consistency Tests
# -----------------------------------------------------------------------------

def test_theme_palette_schema():
    """Verify DARK_THEME and LIGHT_THEME define identical required configuration keys."""
    assert set(DARK_THEME.keys()) >= REQUIRED_PALETTE_KEYS
    assert set(LIGHT_THEME.keys()) >= REQUIRED_PALETTE_KEYS
    assert set(DARK_THEME.keys()) == set(LIGHT_THEME.keys())

    assert DARK_THEME["name"] == "Dark"
    assert LIGHT_THEME["name"] == "Light"
    assert DARK_THEME["plotly_template"] == "plotly_dark"
    assert LIGHT_THEME["plotly_template"] == "plotly_white"
    assert DARK_THEME["font_family"] == "Arial, sans-serif"
    assert LIGHT_THEME["font_family"] == "Arial, sans-serif"


def test_theme_registry_contains_both_themes():
    """Verify THEMES dictionary registers Dark and Light definitions."""
    assert "Dark" in THEMES
    assert "Light" in THEMES
    assert THEMES["Dark"] is DARK_THEME
    assert THEMES["Light"] is LIGHT_THEME


# -----------------------------------------------------------------------------
# 2. Theme State and Retrieval Tests
# -----------------------------------------------------------------------------

def test_get_current_theme_default_headless():
    """Verify default fallback to Dark theme in headless or uninitialized session state."""
    # Ensure session_state does not hold theme_mode
    if hasattr(st, "session_state") and "theme_mode" in st.session_state:
        del st.session_state["theme_mode"]

    assert get_current_theme() == "Dark"


def test_get_current_theme_from_session_state():
    """Verify get_current_theme accurately reflects session_state values."""
    if hasattr(st, "session_state"):
        st.session_state["theme_mode"] = "Light"
        assert get_current_theme() == "Light"

        st.session_state["theme_mode"] = "Dark"
        assert get_current_theme() == "Dark"

        # Invalid mode string should safely fall back to Dark
        st.session_state["theme_mode"] = "HighContrast"
        assert get_current_theme() == "Dark"

        # Cleanup
        del st.session_state["theme_mode"]


def test_get_theme_config():
    """Verify get_theme_config returns correct dictionary or raises on invalid theme."""
    dark_cfg = get_theme_config("Dark")
    assert dark_cfg["name"] == "Dark"
    assert dark_cfg["bg_main"] == "#0E1117"

    light_cfg = get_theme_config("Light")
    assert light_cfg["name"] == "Light"
    assert light_cfg["bg_main"] == "#F8FAFC"

    # None falls back to active theme
    default_cfg = get_theme_config(None)
    assert default_cfg["name"] == "Dark"

    # Invalid theme raises ValueError
    with pytest.raises(ValueError, match="Invalid theme 'UnsupportedTheme'"):
        get_theme_config("UnsupportedTheme")


def test_set_theme():
    """Verify set_theme updates session_state and guards against invalid names."""
    if hasattr(st, "session_state"):
        set_theme("Light")
        assert st.session_state.get("theme_mode") == "Light"
        assert st.session_state.get("theme_mode_selector") == "☀️ Light"

        set_theme("Dark")
        assert st.session_state.get("theme_mode") == "Dark"
        assert st.session_state.get("theme_mode_selector") == "🌙 Dark"

        with pytest.raises(ValueError, match="Invalid theme 'Neon'"):
            set_theme("Neon")


def test_on_theme_toggle_change_callback():
    """Verify _on_theme_toggle_change parses selector label correctly."""
    if hasattr(st, "session_state"):
        st.session_state["theme_mode_selector"] = "☀️ Light"
        _on_theme_toggle_change()
        assert st.session_state["theme_mode"] == "Light"

        st.session_state["theme_mode_selector"] = "🌙 Dark"
        _on_theme_toggle_change()
        assert st.session_state["theme_mode"] == "Dark"


# -----------------------------------------------------------------------------
# 3. User-Facing Toggle Interaction & Lifecycle Tests (Phase 4)
# -----------------------------------------------------------------------------

def test_fresh_session_dark_default():
    """Scenario A: Verify fresh session defaults to Dark mode and initializes selector properly."""
    with patch.object(st, "sidebar", MagicMock()) as mock_sidebar, patch.object(st, "markdown", MagicMock()):
        theme = render_theme_toggle(location="sidebar")
        assert theme == "Dark"
        assert st.session_state["theme_mode"] == "Dark"
        assert st.session_state["theme_mode_selector"] == "🌙 Dark"
        mock_sidebar.radio.assert_called_once()
        _, kwargs = mock_sidebar.radio.call_args
        assert kwargs["key"] == "theme_mode_selector"
        assert kwargs["options"] == ["🌙 Dark", "☀️ Light"]


def test_toggle_switch_to_light():
    """Scenario B: Simulate user selecting Light in sidebar radio toggle."""
    with patch.object(st, "sidebar", MagicMock()), patch.object(st, "markdown", MagicMock()) as mock_markdown:
        # Initial render (defaults to Dark)
        render_theme_toggle(location="sidebar")

        # Simulate user clicking "☀️ Light"
        st.session_state["theme_mode_selector"] = "☀️ Light"
        _on_theme_toggle_change()

        assert st.session_state["theme_mode"] == "Light"
        assert get_current_theme() == "Light"

        # Apply custom theme (as done on rerun)
        active_theme = apply_custom_theme(show_toggle=True)
        assert active_theme == "Light"
        assert st.session_state["theme_mode_selector"] == "☀️ Light"

        # Verify Light theme CSS was injected
        css_injected = mock_markdown.call_args[0][0]
        assert LIGHT_THEME["bg_main"] in css_injected
        assert DARK_THEME["bg_main"] not in css_injected


def test_toggle_switch_back_to_dark():
    """Scenario C: Simulate user switching from Light back to Dark."""
    with patch.object(st, "sidebar", MagicMock()), patch.object(st, "markdown", MagicMock()) as mock_markdown:
        # Start in Light mode
        set_theme("Light")
        assert get_current_theme() == "Light"

        # User selects Dark
        st.session_state["theme_mode_selector"] = "🌙 Dark"
        _on_theme_toggle_change()

        assert st.session_state["theme_mode"] == "Dark"
        assert get_current_theme() == "Dark"

        active_theme = apply_custom_theme(show_toggle=True)
        assert active_theme == "Dark"
        assert st.session_state["theme_mode_selector"] == "🌙 Dark"

        css_injected = mock_markdown.call_args[0][0]
        assert DARK_THEME["bg_main"] in css_injected


def test_cross_page_navigation_persistence():
    """Scenario D: Verify selected theme persists across page navigations without reset."""
    with patch.object(st, "sidebar", MagicMock()), patch.object(st, "markdown", MagicMock()):
        # User on Page 1 switches to Light
        set_theme("Light")
        assert st.session_state["theme_mode"] == "Light"

        # Simulate Page 2 (2_Response_Analysis.py) calling apply_custom_theme()
        theme_p2 = apply_custom_theme(show_toggle=True)
        assert theme_p2 == "Light"
        assert st.session_state["theme_mode"] == "Light"
        assert st.session_state["theme_mode_selector"] == "☀️ Light"

        # Simulate Page 3 (3_Segment_Comparison.py) calling apply_custom_theme()
        theme_p3 = apply_custom_theme(show_toggle=True)
        assert theme_p3 == "Light"
        assert st.session_state["theme_mode"] == "Light"
        assert st.session_state["theme_mode_selector"] == "☀️ Light"

        # Simulate Page 4 (4_Data_Quality.py) calling apply_custom_theme()
        theme_p4 = apply_custom_theme(show_toggle=True)
        assert theme_p4 == "Light"
        assert st.session_state["theme_mode"] == "Light"
        assert st.session_state["theme_mode_selector"] == "☀️ Light"


def test_rerun_session_stability():
    """Scenario E: Verify consecutive Streamlit reruns maintain state with no key collisions."""
    with patch.object(st, "sidebar", MagicMock()) as mock_sidebar, patch.object(st, "markdown", MagicMock()):
        # First execution run
        t1 = render_theme_toggle(location="sidebar")
        assert t1 == "Dark"

        # Second execution run (normal rerun)
        t2 = render_theme_toggle(location="sidebar")
        assert t2 == "Dark"
        assert st.session_state["theme_mode"] == "Dark"
        assert st.session_state["theme_mode_selector"] == "🌙 Dark"

        # Ensure both runs used the identical single key
        for call in mock_sidebar.radio.call_args_list:
            assert call[1]["key"] == "theme_mode_selector"


def test_invalid_state_recovery_and_fallback():
    """Scenario F: Verify recovery when session_state contains unrecognized or corrupted values."""
    with patch.object(st, "sidebar", MagicMock()), patch.object(st, "markdown", MagicMock()):
        # Corrupt theme_mode
        st.session_state["theme_mode"] = "CorruptedHighContrast"
        assert get_current_theme() == "Dark"

        # Corrupt selector
        st.session_state["theme_mode_selector"] = "MalformedOption"

        # render_theme_toggle should heal the state to default Dark
        recovered = render_theme_toggle(location="sidebar")
        assert recovered == "Dark"
        assert st.session_state["theme_mode"] == "Dark"
        assert st.session_state["theme_mode_selector"] == "🌙 Dark"


# -----------------------------------------------------------------------------
# 3. Chart Theme Hardening & Figure Styling Tests
# -----------------------------------------------------------------------------

def test_apply_chart_theme_none_guard():
    """Verify defensive handling of fig=None returns None without error."""
    assert apply_chart_theme(None) is None
    assert apply_chart_theme(None, theme="Light") is None
    assert apply_chart_theme(None, theme="Dark") is None


def test_apply_chart_theme_invalid_theme_raises():
    """Verify applying an invalid theme name raises ValueError."""
    fig = go.Figure(data=[go.Bar(x=[1, 2], y=[10, 20])])
    with pytest.raises(ValueError, match="Invalid theme 'InvalidTheme'"):
        apply_chart_theme(fig, theme="InvalidTheme")


def test_apply_chart_theme_dark_styling():
    """Verify Dark theme visual properties applied to Plotly figure."""
    fig = go.Figure(data=[go.Bar(x=["A", "B"], y=[10, 20])])
    styled = apply_chart_theme(fig, theme="Dark")

    assert styled is fig
    assert styled.layout.template == pio.templates["plotly_dark"]
    assert styled.layout.font.color == DARK_THEME["text_primary"]
    assert styled.layout.font.family == "Arial, sans-serif"
    assert styled.layout.paper_bgcolor == DARK_THEME["chart_paper"]
    assert styled.layout.plot_bgcolor == DARK_THEME["chart_bg"]
    assert styled.layout.hoverlabel.bgcolor == DARK_THEME["bg_card"]
    assert styled.layout.hoverlabel.font.color == DARK_THEME["text_primary"]
    assert styled.layout.hoverlabel.bordercolor == DARK_THEME["border"]
    assert styled.layout.xaxis.gridcolor == DARK_THEME["chart_grid"]
    assert styled.layout.yaxis.gridcolor == DARK_THEME["chart_grid"]
    assert styled.layout.xaxis.tickfont.color == DARK_THEME["text_secondary"]
    assert styled.layout.yaxis.tickfont.color == DARK_THEME["text_secondary"]


def test_apply_chart_theme_light_styling():
    """Verify Light theme visual properties applied to Plotly figure."""
    fig = go.Figure(data=[go.Bar(x=["A", "B"], y=[10, 20])])
    styled = apply_chart_theme(fig, theme="Light")

    assert styled is fig
    assert styled.layout.template == pio.templates["plotly_white"]
    assert styled.layout.font.color == LIGHT_THEME["text_primary"]
    assert styled.layout.font.family == "Arial, sans-serif"
    assert styled.layout.paper_bgcolor == LIGHT_THEME["chart_paper"]
    assert styled.layout.plot_bgcolor == LIGHT_THEME["chart_bg"]
    assert styled.layout.hoverlabel.bgcolor == LIGHT_THEME["bg_card"]
    assert styled.layout.hoverlabel.font.color == LIGHT_THEME["text_primary"]
    assert styled.layout.hoverlabel.bordercolor == LIGHT_THEME["border"]
    assert styled.layout.xaxis.gridcolor == LIGHT_THEME["chart_grid"]
    assert styled.layout.yaxis.gridcolor == LIGHT_THEME["chart_grid"]
    assert styled.layout.xaxis.tickfont.color == LIGHT_THEME["text_secondary"]
    assert styled.layout.yaxis.tickfont.color == LIGHT_THEME["text_secondary"]


def test_apply_chart_theme_preserves_traces_and_data():
    """Verify trace coordinates, series values, and custom metadata are strictly preserved."""
    x_data = ["Rust", "Python", "Go"]
    y_data = [82.5, 78.2, 65.4]
    custom_data = ["n=1200", "n=4500", "n=890"]

    fig = go.Figure(data=[
        go.Bar(
            x=x_data,
            y=y_data,
            customdata=custom_data,
            text=["82.5%", "78.2%", "65.4%"],
            hoverinfo="x+y+text",
        )
    ])

    # Apply Dark
    styled_dark = apply_chart_theme(fig, theme="Dark")
    assert list(styled_dark.data[0].x) == x_data
    assert list(styled_dark.data[0].y) == y_data
    assert list(styled_dark.data[0].customdata) == custom_data
    assert list(styled_dark.data[0].text) == ["82.5%", "78.2%", "65.4%"]

    # Apply Light to same figure
    styled_light = apply_chart_theme(fig, theme="Light")
    assert list(styled_light.data[0].x) == x_data
    assert list(styled_light.data[0].y) == y_data
    assert list(styled_light.data[0].customdata) == custom_data
    assert list(styled_light.data[0].text) == ["82.5%", "78.2%", "65.4%"]


# -----------------------------------------------------------------------------
# 4. Scoped CSS Verification
# -----------------------------------------------------------------------------

def test_scoped_css_definitions():
    """Verify CSS generator templates contain target selectors and distinct background colors."""
    assert DARK_THEME["bg_main"] in CUSTOM_THEME_CSS_DARK
    assert DARK_THEME["bg_card"] in CUSTOM_THEME_CSS_DARK
    assert 'div[data-testid="stMetric"]' in CUSTOM_THEME_CSS_DARK

    assert LIGHT_THEME["bg_main"] in CUSTOM_THEME_CSS_LIGHT
    assert LIGHT_THEME["bg_card"] in CUSTOM_THEME_CSS_LIGHT
    assert 'div[data-testid="stMetric"]' in CUSTOM_THEME_CSS_LIGHT


# -----------------------------------------------------------------------------
# 5. Comprehensive 14-Chart Theming & Mode Adaptation Audit (Phase 5)
# -----------------------------------------------------------------------------

@pytest.fixture
def sample_chart_datasets():
    """Return synthetic sample datasets for all chart generators."""
    return {
        "dist": pd.DataFrame({
            "option": ["Python", "Rust", "JavaScript"],
            "response_count": [300, 150, 450],
            "percentage": [33.3, 16.7, 50.0],
        }),
        "segment": pd.DataFrame({
            "segment": ["0-2 yrs", "0-2 yrs", "3-5 yrs", "3-5 yrs"],
            "option": ["Remote", "In-person", "Remote", "In-person"],
            "percentage": [60.0, 40.0, 70.0, 30.0],
            "response_count": [60, 40, 70, 30],
        }),
        "trend": pd.DataFrame({
            "date": pd.date_range("2025-06-01", periods=5),
            "response_count": [100, 250, 300, 280, 190],
        }),
        "tech": pd.DataFrame({
            "option": ["Rust", "Python", "Go"],
            "pct_of_respondents_current": [12.5, 58.1, 15.0],
            "pct_of_respondents_desired": [31.0, 45.4, 25.6],
        }),
        "comp": pd.DataFrame({
            "DevType": ["DevOps", "DevOps", "Full-Stack", "Full-Stack"],
            "ConvertedCompYearly": [110000.0, 130000.0, 95000.0, 105000.0],
        }),
        "missing": pd.DataFrame({
            "column": ["RemoteWork", "EdLevel", "YearsCode"],
            "missing_count": [15411, 230, 100],
            "missing_pct": [31.3, 0.5, 0.2],
            "non_null_count": [33780, 48961, 49091],
        }),
        "funnel_names": ["Stage 1", "Stage 2", "Stage 3"],
        "funnel_counts": [49191, 23947, 22769],
    }


@pytest.mark.parametrize("theme_name", ["Dark", "Light"])
def test_all_10_shared_chart_generators_under_theme(sample_chart_datasets, theme_name):
    """Verify all 10 shared chart generators correctly apply Dark and Light themes."""
    cfg = DARK_THEME if theme_name == "Dark" else LIGHT_THEME
    expected_tpl = pio.templates[cfg["plotly_template"]]
    ds = sample_chart_datasets

    # 1. plot_distribution_bar
    f1 = plot_distribution_bar(ds["dist"], theme=theme_name)
    assert f1.layout.template == expected_tpl
    assert f1.layout.paper_bgcolor == cfg["chart_paper"]

    # 2. plot_distribution_pie
    f2 = plot_distribution_pie(ds["dist"], theme=theme_name)
    assert f2.layout.template == expected_tpl
    assert f2.layout.paper_bgcolor == cfg["chart_paper"]

    # 3. plot_segment_breakdown_bar
    f3 = plot_segment_breakdown_bar(ds["segment"], theme=theme_name)
    assert f3.layout.template == expected_tpl
    assert f3.layout.paper_bgcolor == cfg["chart_paper"]

    # 4. plot_trend_line
    f4 = plot_trend_line(ds["trend"], theme=theme_name)
    assert f4.layout.template == expected_tpl
    assert f4.layout.paper_bgcolor == cfg["chart_paper"]

    # 5. plot_horizontal_bar_with_denominators
    f5 = plot_horizontal_bar_with_denominators(
        ds["dist"], "option", "response_count", n_answered=900, theme=theme_name
    )
    assert f5.layout.template == expected_tpl
    assert f5.layout.paper_bgcolor == cfg["chart_paper"]

    # 6. plot_technology_comparison_bar
    f6 = plot_technology_comparison_bar(
        ds["tech"], tech_col="option", current_col="pct_of_respondents_current",
        desired_col="pct_of_respondents_desired", theme=theme_name
    )
    assert f6.layout.template == expected_tpl
    assert f6.layout.paper_bgcolor == cfg["chart_paper"]
    assert f6.data[0].marker.color == cfg["accent_primary"]
    assert f6.data[1].marker.color == cfg["indicator_positive"]

    # 7. plot_compensation_box
    f7 = plot_compensation_box(ds["comp"], group_col="DevType", theme=theme_name)
    assert f7.layout.template == expected_tpl
    assert f7.layout.paper_bgcolor == cfg["chart_paper"]

    # 8. plot_missingness_ranking_bar
    f8 = plot_missingness_ranking_bar(ds["missing"], theme=theme_name)
    assert f8.layout.template == expected_tpl
    assert f8.layout.paper_bgcolor == cfg["chart_paper"]

    # 9. plot_sample_flow_funnel
    f9 = plot_sample_flow_funnel(ds["funnel_names"], ds["funnel_counts"], theme=theme_name)
    assert f9.layout.template == expected_tpl
    assert f9.layout.paper_bgcolor == cfg["chart_paper"]

    # 10. _empty_figure
    f10 = _empty_figure("Notice", theme=theme_name)
    assert f10.layout.template == expected_tpl
    assert f10.layout.paper_bgcolor == cfg["chart_paper"]


@pytest.mark.parametrize("theme_name", ["Dark", "Light"])
def test_all_4_page_inline_figures_under_theme(sample_chart_datasets, theme_name):
    """Verify all 4 page-level inline figures correctly apply Dark and Light themes."""
    cfg = DARK_THEME if theme_name == "Dark" else LIGHT_THEME
    expected_tpl = pio.templates[cfg["plotly_template"]]
    ds = sample_chart_datasets

    # 11. Inline fig_age (1_Overview.py)
    fig_age = px.bar(ds["dist"], x="option", y="percentage", title="Age Cohort Distribution")
    apply_chart_theme(fig_age, theme=theme_name)
    assert fig_age.layout.template == expected_tpl
    assert fig_age.layout.paper_bgcolor == cfg["chart_paper"]

    # 12. Inline fig_exp (1_Overview.py)
    fig_exp = go.Figure()
    fig_exp.add_trace(go.Box(x=[5, 10, 15], name="Years Coding", marker_color="#3B82F6"))
    fig_exp.add_trace(go.Box(x=[2, 6, 12], name="Work Exp", marker_color="#22C55E"))
    apply_chart_theme(fig_exp, theme=theme_name)
    assert fig_exp.layout.template == expected_tpl
    assert fig_exp.layout.paper_bgcolor == cfg["chart_paper"]

    # 13. Inline fig_exp_box (3_Segment_Comparison.py)
    fig_exp_box = px.box(ds["comp"], x="DevType", y="ConvertedCompYearly", title="Exp Box")
    apply_chart_theme(fig_exp_box, theme=theme_name)
    assert fig_exp_box.layout.template == expected_tpl
    assert fig_exp_box.layout.paper_bgcolor == cfg["chart_paper"]

    # 14. Inline fig_rw_box (3_Segment_Comparison.py)
    fig_rw_box = px.box(ds["comp"], x="DevType", y="ConvertedCompYearly", title="RW Box")
    apply_chart_theme(fig_rw_box, theme=theme_name)
    assert fig_rw_box.layout.template == expected_tpl
    assert fig_rw_box.layout.paper_bgcolor == cfg["chart_paper"]
