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

    label = "☀️ Light" if is_light else "🌙 Dark"

    if st.sidebar.button(
        f"{label}",
        key="theme_toggle_switch",
        use_container_width=True,
        help="Toggle between dark and light mode",
    ):
        set_theme("light" if not is_light else "dark")

    st.sidebar.markdown(
        """
        <style>
        div[data-testid="stSidebar"] .stButton > button {
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 44px;
            border: 1px solid rgba(148, 163, 184, 0.35);
            border-radius: 999px;
            background: linear-gradient(90deg, #0f172a, #1e293b);
            color: #f8fafc;
            font-weight: 800;
            letter-spacing: 0.5px;
            box-shadow: inset 0 0 0 1px rgba(255,255,255,0.08);
            transition: all 0.25s ease;
        }
        div[data-testid="stSidebar"] .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 18px rgba(14, 165, 233, 0.18);
        }
        div[data-testid="stSidebar"] .stButton > button::before {
            content: "";
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: white;
            position: absolute;
            left: 8px;
            top: 50%;
            transform: translateY(-50%);
            box-shadow: 0 1px 8px rgba(15, 23, 42, 0.28);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )