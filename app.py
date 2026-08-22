import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from components.header import render_header
from components.styles import load_styles
from components.theme import render_theme_toggle
from model.anomaly_detection import detect_anomalies, load_dataset
from utils.risk_engine import build_risk_table


st.set_page_config(
    page_title="HealthSeers",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

load_styles(st.session_state.theme)


@st.cache_data
def get_dataset():
    return load_dataset()


@st.cache_data
def get_anomaly_report(df, z_threshold=2.0, ratio_threshold=1.35):
    return detect_anomalies(
        df,
        z_threshold=z_threshold,
        ratio_threshold=ratio_threshold,
    )


@st.cache_data
def get_risk_table(df, limit=10):
    return build_risk_table(df, limit=limit)


render_header()

st.sidebar.markdown(
    """
    <div style="
        font-size:20px;
        font-weight:800;
        letter-spacing:2px;
    ">
        HEALTHSEERS
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.caption("Community Health Intelligence")
render_theme_toggle()
st.sidebar.markdown("---")

nav_options = [
    ("Overview", "🏠"),
    ("Risk Map", "🗺️"),
    ("Community Analysis", "📊"),
    ("Alerts", "🚨"),
]

if "current_page" not in st.session_state:
    st.session_state.current_page = "Overview"

st.sidebar.markdown(
    """
    <div style="
        font-size:12px;
        font-weight:700;
        letter-spacing:1.2px;
        text-transform:uppercase;
        color:#94A3B8;
        margin-bottom:0.7rem;
    ">
        Navigation
    </div>
    """,
    unsafe_allow_html=True,
)

for option, icon in nav_options:
    is_active = st.session_state.current_page == option
    if st.sidebar.button(
        f"{icon} {option}",
        key=f"nav_{option}",
        use_container_width=True,
        type="primary" if is_active else "secondary",
    ):
        st.session_state.current_page = option

page = st.session_state.current_page

st.sidebar.markdown("---")
st.sidebar.subheader("Detection settings")
z_threshold = st.sidebar.slider("Z-score threshold", 0.5, 5.0, 2.0, step=0.1)
ratio_threshold = st.sidebar.slider("Baseline ratio threshold", 1.05, 5.0, 1.35, step=0.05)
top_n = st.sidebar.number_input("Number of top records to show", min_value=5, max_value=50, value=10)


def render_overview():
    dataset = get_dataset()
    if dataset.empty:
        st.warning("No dataset rows were loaded. Please check the data folder.")
        return

    anomalies = get_anomaly_report(dataset, z_threshold, ratio_threshold)
    risk_table = get_risk_table(dataset, limit=top_n)

    total_locations = dataset["location_id"].nunique()
    flagged = int((anomalies["anomaly_flag"] == True).sum())

    col1, col2, col3 = st.columns(3)
    col1.metric("Locations analyzed", total_locations)
    col2.metric("Flagged anomalies", flagged)
    col3.metric("Top risk records", min(top_n, len(risk_table)))

    st.subheader("Top outbreak-risk locations")
    st.dataframe(
        risk_table[
            [
                "location_id",
                "state_ut",
                "district",
                "disease",
                "latest_cases",
                "risk_level",
                "score",
                "reasons",
            ]
        ].head(top_n),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Anomaly detection results")
    anomaly_view = anomalies.copy()
    anomaly_view["anomaly_flag"] = anomaly_view["anomaly_flag"].map({True: "Flagged", False: "Normal"})

    st.dataframe(
        anomaly_view[
            [
                "location_id",
                "state_ut",
                "district",
                "disease",
                "latest_cases",
                "recent_avg_cases",
                "historical_avg_cases",
                "baseline_ratio",
                "z_score",
                "risk_level",
                "score",
                "anomaly_flag",
                "reasons",
            ]
        ].head(top_n),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Interpretation")
    st.markdown(
        """
        - A location is flagged when the latest case count is substantially above its recent historical baseline.
        - The z-score measures how far the latest value sits from the expected range of historical values.
        - The risk score combines forecast elevation, recent trend changes, and environmental signals such as precipitation, temperature, and LAI.
        """
    )


if page == "Overview":
    render_overview()

elif page == "Risk Map":
    st.header("Risk Map")
    st.info("A district-level risk map can be connected here once the geospatial layer is ready.")
    st.markdown(
        """
        <div style='padding:1.2rem;border:1px solid rgba(148,163,184,0.4);border-radius:16px;background:rgba(15,118,110,0.08);'>
            <strong>Map placeholder</strong><br>
            This section is ready for district coordinates, risk color coding, and clickable locality markers.
        </div>
        """,
        unsafe_allow_html=True,
    )

elif page == "Community Analysis":
    st.header("Community Analysis")
    st.info("This section can show district-level signals, weekly trends, and explainable warning summaries.")
    dataset = get_dataset()
    if not dataset.empty:
        st.dataframe(dataset.head(10), use_container_width=True, hide_index=True)

elif page == "Alerts":
    st.header("Early Warning Center")
    st.error("🚨 HIGH RISK — Village A\n\nIncreased disease cases + poor water quality + heavy rainfall detected.")
    st.warning("⚠️ MEDIUM RISK — Village C\n\nAbnormal increase in reported symptoms detected.")


if __name__ == "__main__":
    pass
