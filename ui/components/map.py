import pydeck as pdk
import streamlit as st
from utils.theme import get_theme


def render_risk_map(df, title="COMMUNITY RISK MAP"):
    theme = get_theme()
    st.markdown(f'<div class="panel map-panel"><div class="panel-heading"><span>{title}</span><small>District-level predicted outbreak risk</small></div>', unsafe_allow_html=True)
    colors = {"HIGH": theme["high_rgb"], "MEDIUM": theme["medium_rgb"], "LOW": theme["low_rgb"]}
    map_df = df.copy()
    map_df["color"] = map_df["risk_level"].map(colors)
    map_df["radius"] = map_df["risk_level"].map({"HIGH": 30000, "MEDIUM": 22000, "LOW": 15000})
    map_df = map_df.sort_values("predicted_cases", ascending=False).drop_duplicates("district")
    layer = pdk.Layer("ScatterplotLayer", data=map_df, get_position="[longitude, latitude]", get_fill_color="color", get_radius="radius", pickable=True, auto_highlight=True)
    deck = pdk.Deck(layers=[layer], initial_view_state=pdk.ViewState(latitude=25.3, longitude=92.5, zoom=5.1), tooltip={"html": "<b>{district}</b><br/>{state_ut}<br/>Current: {current_cases}<br/>Predicted: {predicted_cases}<br/>Risk: {risk_level}", "style": {"backgroundColor": theme["structure"], "color": theme["text_primary"]}}, map_style=theme["map_style"])
    st.pydeck_chart(deck, use_container_width=True)
    st.markdown('<div class="legend"><span><i class="dot high-dot"></i>HIGH</span><span><i class="dot medium-dot"></i>MEDIUM</span><span><i class="dot low-dot"></i>LOW</span></div></div>', unsafe_allow_html=True)
