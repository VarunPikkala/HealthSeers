import streamlit as st

from components.theme import THEMES


def load_styles(theme_name="dark"):
    theme = THEMES.get(theme_name, THEMES["dark"])

    st.markdown(
        f"""
        <style>

        :root {{
            --bg: {theme['bg']};
            --bg-elev: {theme['bg_elev']};
            --card: {theme['card']};
            --card-border: {theme['card_border']};
            --text: {theme['text']};
            --muted: {theme['muted']};
            --cyan: {theme['cyan']};
            --green: {theme['green']};
            --amber: {theme['amber']};
            --red: {theme['red']};
            --button-grad-1: {theme['button_grad_1']};
            --button-grad-2: {theme['button_grad_2']};
            --shadow: {theme['shadow']};
            --sidebar: {theme['sidebar']};
            --pill-bg: {theme['pill_bg']};
            --pill-text: {theme['pill_text']};
        }}

        html, body, .stApp, [data-testid="stAppViewContainer"] {{
            background: var(--bg);
            color: var(--text);
            transition: background 0.45s ease, color 0.35s ease, border-color 0.35s ease;
        }}

        .stSidebar > div:first-child {{
            background: var(--sidebar);
            transition: background 0.45s ease;
        }}

        .stSidebar .stButton > button {{
            border-radius: 12px;
            border: 1px solid transparent;
            padding: 0.7rem 0.8rem;
            font-size: 0.96rem;
            font-weight: 700;
            text-align: left;
            transition: all 0.25s ease;
            background: var(--pill-bg);
            color: var(--text);
        }}

        .stSidebar .stButton > button:hover {{
            transform: translateX(2px);
            border-color: var(--card-border);
        }}

        .stSidebar .stButton > button[kind="primary"] {{
            background: linear-gradient(90deg, var(--button-grad-1), var(--button-grad-2));
            color: #ffffff;
            box-shadow: 0 10px 22px rgba(14, 165, 233, 0.18);
        }}

        .block-container {{
            max-width: 1450px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }}

        .brand {{
            font-size: 32px;
            font-weight: 800;
            letter-spacing: 3px;
            color: var(--text);
            transition: color 0.35s ease;
        }}

        .brand-accent {{
            color: var(--cyan);
        }}

        .subtitle {{
            color: var(--muted);
            font-size: 14px;
            margin-top: -5px;
            transition: color 0.35s ease;
        }}

        .system-status {{
            color: var(--green);
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 1px;
            transition: color 0.35s ease;
        }}

        .glass-card {{
            background: var(--card);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 22px;
            box-shadow: 0 8px 30px var(--shadow);
            backdrop-filter: blur(10px);
            transition: background 0.45s ease, border-color 0.35s ease, box-shadow 0.35s ease;
        }}

        .metric-label {{
            color: var(--muted);
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            transition: color 0.35s ease;
        }}

        .metric-value {{
            color: var(--text);
            font-size: 32px;
            font-weight: 800;
            margin-top: 6px;
            transition: color 0.35s ease;
        }}

        .risk-score {{
            font-size: 58px;
            font-weight: 900;
            line-height: 1;
        }}

        .risk-high {{
            color: var(--red);
            font-weight: 800;
            letter-spacing: 1px;
        }}

        .risk-medium {{
            color: var(--amber);
            font-weight: 800;
        }}

        .risk-low {{
            color: var(--green);
            font-weight: 800;
        }}

        .cyan-glow {{
            box-shadow:
                0 0 20px rgba(34, 211, 238, 0.15),
                inset 0 0 20px rgba(34, 211, 238, 0.03);
        }}

        .fade-in {{
            animation: fadeIn 0.7s ease-out;
        }}

        @keyframes fadeIn {{
            from {{
                opacity: 0;
                transform: translateY(12px);
            }}

            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .pulse {{
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0% {{
                box-shadow: 0 0 0 rgba(239, 68, 68, 0);
            }}

            50% {{
                box-shadow: 0 0 25px rgba(239, 68, 68, 0.25);
            }}

            100% {{
                box-shadow: 0 0 0 rgba(239, 68, 68, 0);
            }}
        }}

        .stButton > button {{
            border: 1px solid var(--card-border);
            border-radius: 12px;
            background: linear-gradient(90deg, var(--button-grad-1), var(--button-grad-2));
            color: white;
            font-weight: 800;
            letter-spacing: 0.5px;
            transition: all 0.35s ease, transform 0.2s ease;
            animation: themePulse 0.6s ease;
        }}

        .stButton > button:hover {{
            box-shadow: 0 0 25px rgba(34, 211, 238, 0.35);
            transform: translateY(-1px) scale(1.01);
        }}

        .stSidebar .stCheckbox label {{
            color: var(--text);
            font-weight: 700;
        }}

        .stSidebar .stCheckbox [data-testid="stMarkdownContainer"] {{
            color: var(--text);
        }}

        @keyframes themePulse {{
            0% {{
                opacity: 0.5;
                transform: scale(0.98);
            }}
            100% {{
                opacity: 1;
                transform: scale(1);
            }}
        }}

        .st-emotion-cache-1a0m5r8, .st-emotion-cache-1wmy9hl {{
            transition: background 0.45s ease, border-color 0.35s ease, color 0.35s ease;
        }}

        hr {{
            border-color: var(--card-border);
            transition: border-color 0.35s ease;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )