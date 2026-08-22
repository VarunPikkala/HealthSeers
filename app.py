# ==========================================
# HEALTHSEERS - STREAMLIT DASHBOARD
# ==========================================

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from model.anomaly_detection import detect_anomalies, load_dataset
from utils.risk_engine import build_risk_table


st.set_page_config(
    page_title="HealthSeers Risk Monitor",
    page_icon="🩺",
    layout="wide",
)


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


def main():
    st.title("🩺 HealthSeers | Outbreak Risk Monitor")
    st.caption("AI-powered district-level anomaly and risk detection for water-borne disease outbreaks.")

    dataset = get_dataset()

    if dataset.empty:
        st.warning("No dataset rows were loaded. Please check the data folder.")
        return

    st.sidebar.header("Detection settings")
    z_threshold = st.sidebar.slider("Z-score threshold", 0.5, 5.0, 2.0, step=0.1)
    ratio_threshold = st.sidebar.slider("Baseline ratio threshold", 1.05, 5.0, 1.35, step=0.05)
    top_n = st.sidebar.number_input("Number of top records to show", min_value=5, max_value=50, value=10)

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
        risk_table[[
            "location_id",
            "state_ut",
            "district",
            "disease",
            "latest_cases",
            "risk_level",
            "score",
            "reasons",
        ]].head(top_n),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Anomaly detection results")
    anomaly_view = anomalies.copy()
    anomaly_view["anomaly_flag"] = anomaly_view["anomaly_flag"].map({True: "Flagged", False: "Normal"})

    st.dataframe(
        anomaly_view[[
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
        ]].head(top_n),
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


if __name__ == "__main__":
    main()
