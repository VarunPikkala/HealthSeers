import streamlit as st

BACKGROUND = "#e6f3ff"
CARD = "#0B1624"
CARD_BORDER = "#164E63"

CYAN = "#22D3EE"
GREEN = "#22C55E"
AMBER = "#F59E0B"
RED = "#EF4444"

TEXT = "#F8FAFC"
MUTED = "#94A3B8"

THEMES = {
    "dark": {
        "bg": "#020817",
        "bg_elev": "#071321",
        "card": "#0B1624",
        "card_border": "#164E63",
        "text": "#F8FAFC",
        "muted": "#94A3B8",
        "cyan": "#22D3EE",
        "green": "#22C55E",
        "amber": "#F59E0B",
        "red": "#EF4444",
        "button_grad_1": "#0891B2",
        "button_grad_2": "#06B6D4",
        "sidebar": "#020817",
        "shadow": "rgba(0, 0, 0, 0.25)",
        "pill_bg": "rgba(15, 118, 110, 0.14)",
        "pill_text": "#d7f6ff",
    },
    "light": {
        "bg": "#edf7ff",
        "bg_elev": "#f8fbff",
        "card": "#ffffff",
        "card_border": "#b8dff8",
        "text": "#12304a",
        "muted": "#475569",
        "cyan": "#0b7ea8",
        "green": "#15803d",
        "amber": "#b45309",
        "red": "#b91c1c",
        "button_grad_1": "#0ea5e9",
        "button_grad_2": "#14b8a6",
        "sidebar": "#f5fbff",
        "shadow": "rgba(15, 23, 42, 0.10)",
        "pill_bg": "rgba(14, 165, 233, 0.12)",
        "pill_text": "#0f3b5c",
    },
}


def get_theme():
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"
    return st.session_state.theme


def set_theme(theme_name):
    st.session_state.theme = theme_name


def render_theme_toggle():
    theme = get_theme()
    is_light = theme == "light"

    st.sidebar.markdown(
        """
        <div style="
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: #94A3B8;
            margin-bottom: 0.7rem;
        ">
            Theme
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        f"""
        <style>
        div[data-testid="stCheckbox"] {{
            margin-top: 0.2rem;
        }}
        div[data-testid="stCheckbox"] label {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.7rem;
            font-weight: 700;
            color: {'#12304a' if is_light else '#F8FAFC'};
        }}
        div[data-testid="stCheckbox"] .stCheckbox {{
            width: 52px;
            height: 28px;
            border-radius: 999px;
            background: linear-gradient(90deg, #0ea5e9, #14b8a6);
            position: relative;
            padding: 4px;
            box-shadow: inset 0 0 0 1px rgba(255,255,255,0.25);
        }}
        div[data-testid="stCheckbox"] .stCheckbox input {{
            display: none;
        }}
        div[data-testid="stCheckbox"] .stCheckbox span {{
            display: block;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: white;
            position: absolute;
            left: 4px;
            top: 4px;
            transition: all 0.25s ease;
            box-shadow: 0 2px 10px rgba(15, 23, 42, 0.25);
        }}
        div[data-testid="stCheckbox"] .stCheckbox input:checked + span {{
            left: 28px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    theme_on = st.sidebar.checkbox(
        "☀️ Light mode",
        value=is_light,
        key="theme_toggle_switch",
        help="Toggle between dark and light mode",
    )

    if theme_on:
        set_theme("light")
    else:
        set_theme("dark")