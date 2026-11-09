"""Professional Theme & Visual Styling Components for Poll Results Visualizer.

Provides dark-mode-first styling, design palette constants, and CSS injection.

Author: Akash Das
Project: Poll Results Visualizer
Phase: Feature Enhancement - Professional Dark Mode
"""

import streamlit as st

# Enterprise Business Intelligence Dark Theme Color Palette
COLOR_BG_MAIN = "#0E1117"
COLOR_BG_SIDEBAR = "#161B26"
COLOR_BG_CARD = "#1C2433"
COLOR_TEXT_PRIMARY = "#F1F5F9"
COLOR_TEXT_SECONDARY = "#A0AEC0"
COLOR_ACCENT_PRIMARY = "#3B82F6"
COLOR_INDICATOR_POSITIVE = "#22C55E"
COLOR_INDICATOR_WARNING = "#F59E0B"
COLOR_BORDER = "#30394A"

# Scoped CSS enhancement for metrics, cards, borders, and typography
CUSTOM_THEME_CSS = f"""
<style>
/* Enterprise Card Styling for KPI Metrics */
div[data-testid="stMetric"] {{
    background-color: {COLOR_BG_CARD};
    border: 1px solid {COLOR_BORDER};
    border-radius: 8px;
    padding: 14px 18px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}}

div[data-testid="stMetric"]:hover {{
    border-color: {COLOR_ACCENT_PRIMARY};
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
}}

div[data-testid="stMetricLabel"] p {{
    color: {COLOR_TEXT_SECONDARY} !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}}

div[data-testid="stMetricValue"] div {{
    color: {COLOR_TEXT_PRIMARY} !important;
    font-weight: 700 !important;
}}

/* Captions and Secondary Text */
.stCaption, [data-testid="stCaptionContainer"] p {{
    color: {COLOR_TEXT_SECONDARY} !important;
}}

/* Clean Separators and Dividers */
hr {{
    border-color: {COLOR_BORDER} !important;
    opacity: 0.7 !important;
    margin: 1.5rem 0 !important;
}}

/* Dataframe Container Borders */
div[data-testid="stDataFrame"] {{
    border: 1px solid {COLOR_BORDER};
    border-radius: 8px;
}}

/* Expanders */
div[data-testid="stExpander"] {{
    border: 1px solid {COLOR_BORDER} !important;
    border-radius: 8px !important;
    background-color: {COLOR_BG_SIDEBAR} !important;
}}

/* Tab Navigation Active State */
button[data-baseweb="tab"][aria-selected="true"] {{
    color: {COLOR_ACCENT_PRIMARY} !important;
    border-bottom-color: {COLOR_ACCENT_PRIMARY} !important;
}}
</style>
"""


def apply_custom_theme() -> None:
    """Inject scoped custom CSS to enhance dashboard visual hierarchy."""
    st.markdown(CUSTOM_THEME_CSS, unsafe_allow_html=True)
