from pathlib import Path

import pandas as pd
import streamlit as st

from model.anomaly_detection import detect_anomalies
from utils.preprocessing import preprocess_data
from utils.risk_engine import build_risk_table

DEMO_MODE = False
STATES = ["Assam", "Meghalaya", "Tripura", "Mizoram", "Manipur", "Nagaland", "Arunachal Pradesh"]
DISEASES = ["Acute Diarrhoeal Disease", "Cholera"]
REGION = "northeast_india"


@st.cache_data
def load_backend_dataset():
    raw_path = Path(__file__).resolve().parents[2] / "data" / "raw" / "Final_data.csv"
    processed_path = Path(__file__).resolve().parents[2] / "data" / "processed" / "northeast_india_processed.csv"

    if processed_path.exists():
        return pd.read_csv(processed_path)

    if raw_path.exists():
        return preprocess_data(pd.read_csv(raw_path), region=REGION, save_to_csv=True)

    raise FileNotFoundError("No processed or raw HealthSeers dataset was found.")


@st.cache_data
def load_data():
    if DEMO_MODE:
        return _demo_data()

    processed = load_backend_dataset()
    return _normalize_backend_data(processed)


def _demo_data():
    import numpy as np

    rng = np.random.default_rng(42)
    districts = [
        ("Assam", "Dibrugarh", 27.47, 94.91), ("Assam", "Kamrup", 26.14, 91.74),
        ("Assam", "Jorhat", 26.75, 94.22), ("Meghalaya", "East Khasi Hills", 25.58, 91.89),
        ("Meghalaya", "Ri-Bhoi", 25.90, 91.88), ("Tripura", "West Tripura", 23.83, 91.28),
        ("Mizoram", "Aizawl", 23.73, 92.72), ("Manipur", "Imphal West", 24.82, 93.94),
        ("Nagaland", "Kohima", 25.67, 94.11), ("Arunachal Pradesh", "Papum Pare", 27.10, 93.62),
    ]
    records = []
    for index, (state, district, latitude, longitude) in enumerate(districts):
        for disease in DISEASES:
            risk_level = ["HIGH", "MEDIUM", "LOW", "LOW", "MEDIUM"][index % 5]
            current_cases = [19, 14, 11, 6, 9, 4, 7, 5, 12, 3][index] + int(disease == "Cholera")
            trend = {"HIGH": 42, "MEDIUM": 18, "LOW": 2}[risk_level]
            predicted_cases = round(current_cases * (1 + trend / 100))
            history = [max(0, int(current_cases * value)) for value in [0.55, 0.62, 0.68, 0.74, 0.80, 0.88, 0.94, 1.0]]
            records.append({
                "state_ut": state, "district": district, "latitude": latitude, "longitude": longitude,
                "disease": disease, "date": pd.Timestamp("2026-08-15"), "current_cases": current_cases,
                "predicted_cases": predicted_cases, "historical_baseline": max(1, int(sum(history) / len(history))),
                "trend_percentage": trend, "risk_level": risk_level,
                "precipitation": 68 if risk_level == "HIGH" else 42 if risk_level == "MEDIUM" else 24,
                "temperature": round(27 + rng.uniform(-1.5, 3.5), 1), "lai": round(2.4 + rng.uniform(-0.5, 0.7), 2),
                "history": history,
            })
    return pd.DataFrame(records)


def _normalize_backend_data(processed):
    if processed.empty:
        return processed.copy()

    risk_table = build_risk_table(processed, limit=None, region=REGION)
    risk_map = risk_table.set_index("location_id")["risk_level"].to_dict()

    records = []
    for location_id, group in processed.groupby("location_id", sort=False):
        group = group.sort_values(["year", "week"]).reset_index(drop=True)
        latest = group.iloc[-1]
        history = group["Cases"].tail(8).astype(float).tolist()
        recent_average = float(group["Cases"].tail(4).mean()) if not group.empty else 0.0
        historical_average = float(group["Cases"].iloc[:-1].mean()) if len(group) > 1 else float(latest["Cases"])
        trend_pct = 0.0 if historical_average == 0 else ((recent_average - historical_average) / historical_average) * 100

        risk_level = risk_map.get(location_id, "LOW")
        records.append({
            "state_ut": latest["state_ut"],
            "district": latest["district"],
            "latitude": latest.get("Latitude", 0.0),
            "longitude": latest.get("Longitude", 0.0),
            "disease": latest["Disease"],
            "date": pd.Timestamp(year=int(latest["year"]), month=1, day=1),
            "current_cases": int(float(latest["Cases"])),
            "predicted_cases": int(float(latest["Cases"])),
            "historical_baseline": int(round(historical_average)),
            "trend_percentage": round(float(trend_pct), 2),
            "risk_level": risk_level,
            "precipitation": float(latest.get("preci", 0.0)),
            "temperature": float(latest.get("Temp", 0.0)),
            "lai": float(latest.get("LAI", 0.0)),
            "history": history,
        })

    result = pd.DataFrame(records)
    if result.empty:
        return result

    result = result.sort_values(["risk_level", "current_cases"], ascending=[False, False])
    return result.reset_index(drop=True)


def get_risk_summary(df):
    district_risk = df.sort_values("predicted_cases", ascending=False).drop_duplicates("district")
    counts = district_risk["risk_level"].value_counts()
    total = len(district_risk)
    high, medium = int(counts.get("HIGH", 0)), int(counts.get("MEDIUM", 0))
    return total, high, medium, total - high - medium, high


def filter_data(df, state="All", district="All", disease="All", risk="All"):
    filtered = df.copy()
    for column, value in [("state_ut", state), ("district", district), ("disease", disease), ("risk_level", risk)]:
        if value != "All":
            filtered = filtered[filtered[column] == value]
    return filtered


def get_high_risk_districts(df, limit=5):
    return df[df["risk_level"] == "HIGH"].sort_values("predicted_cases", ascending=False).drop_duplicates("district").head(limit)
