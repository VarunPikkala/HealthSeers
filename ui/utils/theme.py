import streamlit as st

LIGHT_THEME = {
    "background": "#F7F7F2", "background_secondary": "#FFFFFF", "background_dark": "#EFEFE8",
    "glass": "#FFFFFF", "glass_featured": "#FFFFFF", "glass_active": "#FFFFFF",
    "accent": "#00AFC1", "accent_hover": "#008B9A", "accent_soft": "#EAF9FA", "accent_border": "rgba(0,175,193,0.28)", "accent_glow": "rgba(0,175,193,0.12)",
    "text_primary": "#10252B", "text_secondary": "#52636A", "text_muted": "#7B8A8F", "structure": "#10252B", "border": "#DDE4E3", "divider": "#E4E7E1",
    "ai": "#7957D5", "ai_soft": "#F3F0FF", "data": "#3277C8", "data_soft": "#EDF4FC",
    "low": "#16A66A", "medium": "#D99A00", "high": "#E23B45", "low_rgb": [22, 166, 106, 210], "medium_rgb": [217, 154, 0, 210], "high_rgb": [226, 59, 69, 210], "sidebar": "#FFFFFF", "chart_grid": "#E6ECEC", "map_style": "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
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
    common_overrides = """
    .stApp,[data-testid='stAppViewContainer'],[data-testid='stMain'],.main,[data-testid='stSidebar']{color:var(--text-primary)!important;}
    .stApp p,.stApp label,.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp h5,.stApp h6,.stApp [data-testid='stMetricLabel'],.stApp [data-testid='stMetricValue']{color:var(--text-primary)!important;}
    """ if theme is LIGHT_THEME else ""
    light_overrides = """
    html,body,#root,.stApp,[class*='stApp'],[data-testid='stAppViewContainer'],[data-testid='stMain'],.main,.main .block-container{background-color:var(--background)!important;background:var(--background)!important;color:var(--text-primary)!important;}
    [data-testid='stHeader']{background:var(--background)!important;}
    .main p,.main label,.main h1,.main h2,.main h3,.main h4,.main h5,.main h6,.main [data-testid='stMetricLabel'],.main [data-testid='stMetricValue']{color:var(--text-primary)!important;}
    .top-header,.kpi-card,.panel,.architecture,.method-step,footer{background:#FFFFFF;backdrop-filter:none;-webkit-backdrop-filter:none;}
    [data-testid='stSidebar']{background:#FFFFFF!important;backdrop-filter:none;-webkit-backdrop-filter:none;box-shadow:2px 0 12px rgba(16,37,43,.04);}
    .stButton button{background:#FFFFFF!important;}
    .stButton button:hover,.stButton button[kind='primary']{background:#EAF9FA!important;}
    [data-testid='stSelectbox']>div>div,[data-testid='stMultiSelect']>div>div,[data-testid='stTextInput'] input{background:#FFFFFF!important;backdrop-filter:none;color:#10252B!important;}
    [data-testid='stSelectbox'] *,[data-testid='stMultiSelect'] *,[data-baseweb='select'] *{color:#10252B!important;}
    [data-baseweb='popover'],[data-baseweb='menu'],[role='listbox']{background:#FFFFFF!important;color:#10252B!important;}
    [data-baseweb='popover'] *,[data-baseweb='menu'] *,[role='listbox'] *{color:#10252B!important;}
    .alert-panel{background:#FFF1F2;}
    .architecture-flow span{background:#EAF9FA;}
    """ if theme is LIGHT_THEME else ""
    return f"<style>:root{{{variables};--theme-transition:background-color 200ms ease,color 200ms ease,border-color 200ms ease,box-shadow 200ms ease;}}{common_overrides}{light_overrides}</style>"
