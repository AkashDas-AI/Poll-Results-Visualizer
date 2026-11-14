"""Unit tests for centralized Light/Dark Mode theme architecture.

Validates theme configuration schemas, session-state lifecycle, Plotly figure styling,
defensive null-safety, invalid-input guards, and trace/data immutability.

Author: Akash Das
Project: Poll Results Visualizer
Phase: Phase 3 — Theme Architecture Hardening
"""

import pytest
import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio

from app.components.theme import (
    DARK_THEME,
    LIGHT_THEME,
    THEMES,
    get_current_theme,
    get_theme_config,
    set_theme,
    _on_theme_toggle_change,
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
