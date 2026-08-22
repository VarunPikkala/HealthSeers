from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

DEMO_MODE = True
STATES = ["Assam", "Meghalaya", "Tripura", "Mizoram", "Manipur", "Nagaland", "Arunachal Pradesh"]
DISEASES = ["Acute Diarrhoeal Disease", "Cholera", "Typhoid", "Leptospirosis"]


@st.cache_data
def load_demo_data():
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
                "predicted_cases": predicted_cases, "historical_baseline": max(1, int(np.mean(history))),
                "trend_percentage": trend, "risk_level": risk_level,
                "precipitation": 68 if risk_level == "HIGH" else 42 if risk_level == "MEDIUM" else 24,
                "temperature": round(27 + rng.uniform(-1.5, 3.5), 1), "lai": round(2.4 + rng.uniform(-0.5, 0.7), 2),
                "history": history,
            })
    return pd.DataFrame(records)


@st.cache_data
def load_data():
    csv_path = Path(__file__).resolve().parents[2] / "data" / "raw" / "Final_data.csv"
    if not DEMO_MODE and csv_path.exists():
        try:
            raw = pd.read_csv(csv_path)
            return _normalize_real_data(raw)
        except (OSError, ValueError, KeyError):
            pass
    return load_demo_data()


def _normalize_real_data(raw):
    required = {"state_ut", "district", "Latitude", "Longitude", "Disease", "Cases"}
    if not required.issubset(raw.columns):
        raise KeyError("Final_data.csv does not contain the expected fields")
    grouped = raw.sort_values("year").groupby(["state_ut", "district", "Disease"], as_index=False)
    latest = grouped.tail(1).copy()
    latest["latitude"] = latest["Latitude"]
    latest["longitude"] = latest["Longitude"]
    latest["disease"] = latest["Disease"]
    latest["current_cases"] = latest["Cases"].fillna(0).astype(int)
    latest["predicted_cases"] = latest["current_cases"]
    latest["historical_baseline"] = latest["current_cases"]
    latest["trend_percentage"] = 0
    latest["risk_level"] = "LOW"
    latest["precipitation"] = latest.get("preci", 0)
    latest["temperature"] = latest.get("Temp", 0)
    latest["lai"] = latest.get("LAI", 0)
    latest["history"] = latest["current_cases"].apply(lambda value: [int(value)] * 8)
    return latest


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
