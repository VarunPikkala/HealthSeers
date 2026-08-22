import folium
import streamlit as st
from streamlit_folium import st_folium


def render_map():

    st.markdown("### Geographic Risk Intelligence")

    m = folium.Map(
        location=[26.2, 92.9],
        zoom_start=7,
        tiles="CartoDB dark_matter",
    )

    villages = [

        {
            "name": "Village A",
            "lat": 26.20,
            "lon": 92.90,
            "risk": "HIGH",
        },

        {
            "name": "Village B",
            "lat": 26.50,
            "lon": 93.20,
            "risk": "LOW",
        },

        {
            "name": "Village C",
            "lat": 25.90,
            "lon": 93.10,
            "risk": "MEDIUM",
        },
    ]

    colors = {
        "HIGH": "red",
        "MEDIUM": "orange",
        "LOW": "green",
    }

    for village in villages:

        folium.Marker(
            location=[
                village["lat"],
                village["lon"],
            ],

            popup=(
                f"{village['name']} — "
                f"{village['risk']} RISK"
            ),

            tooltip=village["name"],

            icon=folium.Icon(
                color=colors[village["risk"]],
                icon="info-sign",
            ),
        ).add_to(m)

    st_folium(
        m,
        width=None,
        height=520,
    )