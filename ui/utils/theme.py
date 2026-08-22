import streamlit as st

LIGHT_THEME = {
    "background": "#F4F1E8", "background_secondary": "#FAF8F2", "background_dark": "#EAE5D8",
    "glass": "rgba(255,255,255,0.42)", "glass_featured": "rgba(255,255,255,0.55)", "glass_active": "rgba(255,255,255,0.62)",
    "accent": "#00AFC1", "accent_hover": "#008B9A", "accent_soft": "rgba(0,175,193,0.08)", "accent_border": "rgba(0,175,193,0.28)", "accent_glow": "rgba(0,175,193,0.12)",
    "text_primary": "#17252B", "text_secondary": "#52636A", "text_muted": "#819096", "structure": "#102B35", "border": "#D9E1DE", "divider": "#E4E7E1",
    "ai": "#7957D5", "ai_soft": "rgba(121,87,213,0.07)", "data": "#3277C8", "data_soft": "rgba(50,119,200,0.07)",
    "low": "#16A66A", "medium": "#D99A00", "high": "#E23B45", "low_rgb": [22, 166, 106, 210], "medium_rgb": [217, 154, 0, 210], "high_rgb": [226, 59, 69, 210], "sidebar": "rgba(255,255,255,0.45)", "chart_grid": "#E4E7E1", "map_style": None,
}

DARK_THEME = {
    "background": "#05080D", "background_secondary": "#080D14", "background_dark": "#030509",
    "glass": "rgba(12,24,34,0.58)", "glass_featured": "rgba(15,31,42,0.68)", "glass_active": "rgba(10,35,44,0.72)",
    "accent": "#00E5FF", "accent_hover": "#33EBFF", "accent_soft": "rgba(0,229,255,0.08)", "accent_border": "rgba(0,229,255,0.22)", "accent_glow": "rgba(0,229,255,0.12)",
    "text_primary": "#F2F7FA", "text_secondary": "#A7B8C4", "text_muted": "#647887", "structure": "#F2F7FA", "border": "#17303B", "divider": "#17303B",
    "ai": "#A855F7", "ai_soft": "rgba(168,85,247,0.10)", "data": "#3B82F6", "data_soft": "rgba(59,130,246,0.10)",
    "low": "#22C55E", "medium": "#F59E0B", "high": "#FF3B4D", "low_rgb": [34, 197, 94, 210], "medium_rgb": [245, 158, 11, 210], "high_rgb": [255, 59, 77, 210], "sidebar": "rgba(5,8,13,0.78)", "chart_grid": "#17303B", "map_style": None,
}


def get_theme(mode=None):
    mode = mode or st.session_state.get("theme", "light")
    return DARK_THEME if mode == "dark" else LIGHT_THEME


def initialize_theme():
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    return st.session_state.theme


def theme_css(theme):
    variables = ";".join(f"--{key.replace('_', '-')}: {value}" for key, value in theme.items() if key not in {"map_style"})
    return f"<style>:root{{{variables};--theme-transition:background-color 200ms ease,color 200ms ease,border-color 200ms ease,box-shadow 200ms ease;}}</style>"
