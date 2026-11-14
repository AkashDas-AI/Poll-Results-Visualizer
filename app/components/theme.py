"""Professional Theme & Visual Styling Components for Poll Results Visualizer.

Provides centralized Light Mode and Dark Mode theme management, enterprise design palettes,
scoped CSS injection, and Plotly figure styling.

Author: Akash Das
Project: Poll Results Visualizer
Phase: Feature Enhancement - Theme Management (Light / Dark Mode)
"""

from typing import Any, Dict, Optional
import streamlit as st

# -----------------------------------------------------------------------------
# Enterprise Business Intelligence Design Palettes
# -----------------------------------------------------------------------------

DARK_THEME: Dict[str, Any] = {
    "name": "Dark",
    "bg_main": "#0E1117",
    "bg_sidebar": "#161B26",
    "bg_card": "#1C2433",
    "text_primary": "#F1F5F9",
    "text_secondary": "#A0AEC0",
    "accent_primary": "#3B82F6",
    "indicator_positive": "#22C55E",
    "indicator_warning": "#F59E0B",
    "border": "#30394A",
    "plotly_template": "plotly_dark",
    "chart_grid": "rgba(128, 128, 128, 0.15)",
    "chart_font_color": "#F1F5F9",
    "chart_secondary_color": "#A0AEC0",
}

LIGHT_THEME: Dict[str, Any] = {
    "name": "Light",
    "bg_main": "#F8FAFC",
    "bg_sidebar": "#F1F5F9",
    "bg_card": "#FFFFFF",
    "text_primary": "#0F172A",
    "text_secondary": "#475569",
    "accent_primary": "#2563EB",
    "indicator_positive": "#16A34A",
    "indicator_warning": "#D97706",
    "border": "#CBD5E1",
    "plotly_template": "plotly_white",
    "chart_grid": "rgba(0, 0, 0, 0.08)",
    "chart_font_color": "#0F172A",
    "chart_secondary_color": "#475569",
}

THEMES: Dict[str, Dict[str, Any]] = {
    "Dark": DARK_THEME,
    "Light": LIGHT_THEME,
}

# Backward-compatible constant aliases (Dark baseline)
COLOR_BG_MAIN = DARK_THEME["bg_main"]
COLOR_BG_SIDEBAR = DARK_THEME["bg_sidebar"]
COLOR_BG_CARD = DARK_THEME["bg_card"]
COLOR_TEXT_PRIMARY = DARK_THEME["text_primary"]
COLOR_TEXT_SECONDARY = DARK_THEME["text_secondary"]
COLOR_ACCENT_PRIMARY = DARK_THEME["accent_primary"]
COLOR_INDICATOR_POSITIVE = DARK_THEME["indicator_positive"]
COLOR_INDICATOR_WARNING = DARK_THEME["indicator_warning"]
COLOR_BORDER = DARK_THEME["border"]

# -----------------------------------------------------------------------------
# Scoped CSS Generators
# -----------------------------------------------------------------------------

CUSTOM_THEME_CSS_DARK = f"""
<style>
/* Enterprise BI Dark Theme */
.stApp {{
    background-color: {DARK_THEME["bg_main"]};
    color: {DARK_THEME["text_primary"]};
}}

section[data-testid="stSidebar"] {{
    background-color: {DARK_THEME["bg_sidebar"]} !important;
    border-right: 1px solid {DARK_THEME["border"]} !important;
}}

section[data-testid="stSidebar"] .stMarkdown p {{
    color: {DARK_THEME["text_primary"]} !important;
}}

/* Enterprise Card Styling for KPI Metrics */
div[data-testid="stMetric"] {{
    background-color: {DARK_THEME["bg_card"]} !important;
    border: 1px solid {DARK_THEME["border"]} !important;
    border-radius: 8px !important;
    padding: 14px 18px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}}

div[data-testid="stMetric"]:hover {{
    border-color: {DARK_THEME["accent_primary"]} !important;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2) !important;
}}

div[data-testid="stMetricLabel"] p {{
    color: {DARK_THEME["text_secondary"]} !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}}

div[data-testid="stMetricValue"] div {{
    color: {DARK_THEME["text_primary"]} !important;
    font-weight: 700 !important;
}}

/* Captions and Secondary Text */
.stCaption, [data-testid="stCaptionContainer"] p {{
    color: {DARK_THEME["text_secondary"]} !important;
}}

/* Clean Separators and Dividers */
hr {{
    border-color: {DARK_THEME["border"]} !important;
    opacity: 0.7 !important;
    margin: 1.5rem 0 !important;
}}

/* Dataframe Container Borders */
div[data-testid="stDataFrame"] {{
    border: 1px solid {DARK_THEME["border"]} !important;
    border-radius: 8px !important;
}}

/* Expanders */
div[data-testid="stExpander"] {{
    border: 1px solid {DARK_THEME["border"]} !important;
    border-radius: 8px !important;
    background-color: {DARK_THEME["bg_sidebar"]} !important;
}}

div[data-testid="stExpander"] summary {{
    color: {DARK_THEME["text_primary"]} !important;
}}

/* Tab Navigation Active State */
button[data-baseweb="tab"][aria-selected="true"] {{
    color: {DARK_THEME["accent_primary"]} !important;
    border-bottom-color: {DARK_THEME["accent_primary"]} !important;
}}

/* Sidebar Radio Pills */
div[data-testid="stRadio"] > div {{
    gap: 8px;
}}
</style>
"""

CUSTOM_THEME_CSS_LIGHT = f"""
<style>
/* Enterprise BI Light Theme */
.stApp {{
    background-color: {LIGHT_THEME["bg_main"]} !important;
    color: {LIGHT_THEME["text_primary"]} !important;
}}

section[data-testid="stSidebar"] {{
    background-color: {LIGHT_THEME["bg_sidebar"]} !important;
    border-right: 1px solid {LIGHT_THEME["border"]} !important;
}}

section[data-testid="stSidebar"] .stMarkdown p {{
    color: {LIGHT_THEME["text_primary"]} !important;
}}

/* Headings and Main Text */
h1, h2, h3, h4, h5, h6 {{
    color: {LIGHT_THEME["text_primary"]} !important;
}}

.stApp p, .stApp span, .stApp label, .stApp li {{
    color: #334155;
}}

/* Enterprise Card Styling for KPI Metrics */
div[data-testid="stMetric"] {{
    background-color: {LIGHT_THEME["bg_card"]} !important;
    border: 1px solid {LIGHT_THEME["border"]} !important;
    border-radius: 8px !important;
    padding: 14px 18px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}}

div[data-testid="stMetric"]:hover {{
    border-color: {LIGHT_THEME["accent_primary"]} !important;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.15) !important;
}}

div[data-testid="stMetricLabel"] p {{
    color: {LIGHT_THEME["text_secondary"]} !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}}

div[data-testid="stMetricValue"] div {{
    color: {LIGHT_THEME["text_primary"]} !important;
    font-weight: 700 !important;
}}

/* Captions and Secondary Text */
.stCaption, [data-testid="stCaptionContainer"] p {{
    color: {LIGHT_THEME["text_secondary"]} !important;
}}

/* Clean Separators and Dividers */
hr {{
    border-color: {LIGHT_THEME["border"]} !important;
    opacity: 1 !important;
    margin: 1.5rem 0 !important;
}}

/* Dataframe Container Borders & Surface */
div[data-testid="stDataFrame"] {{
    border: 1px solid {LIGHT_THEME["border"]} !important;
    border-radius: 8px !important;
    background-color: {LIGHT_THEME["bg_card"]} !important;
}}

/* Expanders */
div[data-testid="stExpander"] {{
    border: 1px solid {LIGHT_THEME["border"]} !important;
    border-radius: 8px !important;
    background-color: {LIGHT_THEME["bg_card"]} !important;
}}

div[data-testid="stExpander"] summary {{
    color: {LIGHT_THEME["text_primary"]} !important;
    font-weight: 600 !important;
}}

/* Tab Navigation Active State */
button[data-baseweb="tab"] {{
    color: {LIGHT_THEME["text_secondary"]} !important;
}}

button[data-baseweb="tab"][aria-selected="true"] {{
    color: {LIGHT_THEME["accent_primary"]} !important;
    border-bottom-color: {LIGHT_THEME["accent_primary"]} !important;
    font-weight: 600 !important;
}}

/* Header Bar */
header[data-testid="stHeader"] {{
    background-color: rgba(248, 250, 252, 0.85) !important;
}}

/* Inputs & Selectboxes */
div[data-baseweb="select"] > div {{
    background-color: #FFFFFF !important;
    border-color: #CBD5E1 !important;
    color: #0F172A !important;
}}

div[data-baseweb="tag"] {{
    background-color: #E2E8F0 !important;
    color: #0F172A !important;
}}

/* Sidebar Radio Pills */
div[data-testid="stRadio"] > div {{
    gap: 8px;
}}
</style>
"""

# Backward-compatible CSS alias
CUSTOM_THEME_CSS = CUSTOM_THEME_CSS_DARK

# -----------------------------------------------------------------------------
# Theme Management Functions
# -----------------------------------------------------------------------------


def get_current_theme() -> str:
    """Return the currently selected theme ('Dark' or 'Light'). Default: 'Dark'.

    Safely handles headless environments (e.g., pytest or standalone script execution)
    where Streamlit session_state is uninitialized.
    """
    try:
        if hasattr(st, "session_state") and "theme_mode" in st.session_state:
            mode = st.session_state["theme_mode"]
            if mode in THEMES:
                return mode
    except Exception:
        pass
    return "Dark"


def get_theme_config(theme: Optional[str] = None) -> Dict[str, Any]:
    """Retrieve color palette and template configuration for the specified or active theme."""
    if theme is None:
        theme = get_current_theme()
    return THEMES.get(theme, DARK_THEME)


def set_theme(theme_name: str) -> None:
    """Explicitly set the active theme in session state."""
    if theme_name in THEMES and hasattr(st, "session_state"):
        st.session_state["theme_mode"] = theme_name
        st.session_state["theme_mode_selector"] = "🌙 Dark" if theme_name == "Dark" else "☀️ Light"


def _on_theme_toggle_change() -> None:
    """Callback triggered upon theme radio interaction."""
    selected_label = st.session_state.get("theme_mode_selector", "🌙 Dark")
    new_theme = "Light" if "Light" in selected_label else "Dark"
    st.session_state["theme_mode"] = new_theme


def render_theme_toggle(location: str = "sidebar") -> str:
    """Render a clear Light Mode / Dark Mode toggle in the sidebar or main page.

    Synchronizes state across page navigation and Streamlit reruns.

    Args:
        location: 'sidebar' to render in st.sidebar, or 'main' for st.

    Returns:
        str: Active theme name ('Dark' or 'Light').
    """
    target = st.sidebar if location == "sidebar" else st

    if "theme_mode" not in st.session_state:
        st.session_state["theme_mode"] = "Dark"

    current = st.session_state["theme_mode"]
    expected_selector_val = "🌙 Dark" if current == "Dark" else "☀️ Light"
    if "theme_mode_selector" not in st.session_state:
        st.session_state["theme_mode_selector"] = expected_selector_val

    target.markdown("### 🎨 Display Theme")
    target.radio(
        label="Display Theme",
        options=["🌙 Dark", "☀️ Light"],
        key="theme_mode_selector",
        on_change=_on_theme_toggle_change,
        horizontal=True,
        label_visibility="collapsed",
    )
    target.markdown("---")

    return get_current_theme()


def apply_custom_theme(show_toggle: bool = True) -> str:
    """Apply active theme styles and optionally render the sidebar toggle.

    Args:
        show_toggle: Whether to render the sidebar theme toggle. Default True.

    Returns:
        str: Active theme name ('Dark' or 'Light').
    """
    theme = get_current_theme()
    if show_toggle:
        render_theme_toggle(location="sidebar")
        theme = get_current_theme()

    css = CUSTOM_THEME_CSS_DARK if theme == "Dark" else CUSTOM_THEME_CSS_LIGHT
    st.markdown(css, unsafe_allow_html=True)
    return theme


def apply_chart_theme(fig: Any, theme: Optional[str] = None) -> Any:
    """Apply the active theme's template, colors, and transparent canvas to a Plotly figure.

    Args:
        fig: A Plotly Figure object (go.Figure).
        theme: Optional explicit theme override ('Dark' or 'Light').

    Returns:
        The styled Plotly Figure.
    """
    cfg = get_theme_config(theme)
    fig.update_layout(
        template=cfg["plotly_template"],
        font=dict(color=cfg["text_primary"]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_xaxes(
        gridcolor=cfg["chart_grid"],
        zerolinecolor=cfg["chart_grid"],
        tickfont=dict(color=cfg["text_secondary"]),
        title_font=dict(color=cfg["text_primary"]),
    )
    fig.update_yaxes(
        gridcolor=cfg["chart_grid"],
        zerolinecolor=cfg["chart_grid"],
        tickfont=dict(color=cfg["text_secondary"]),
        title_font=dict(color=cfg["text_primary"]),
    )
    return fig
