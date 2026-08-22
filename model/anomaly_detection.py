# ==========================================
# HEALTHSEERS - ANOMALY DETECTION SCRIPT
# ==========================================

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from utils.preprocessing import preprocess_data
from utils.risk_engine import assess_risk


def parse_args():
    parser = argparse.ArgumentParser(
        description="Detect outbreak anomalies across districts and diseases."
    )
    parser.add_argument(
        "--data-path",
        type=Path,
        default=None,
        help="Path to raw or processed dataset. If omitted, uses the processed CSV if present else raw data.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "processed" / "anomaly_report.csv",
        help="Where to save the anomaly report CSV.",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=20,
        help="Number of highest-risk anomalies to print or save.",
    )
    parser.add_argument(
        "--z-threshold",
        type=float,
        default=2.0,
        help="Minimum absolute z-score to consider a location anomalous.",
    )
    parser.add_argument(
        "--ratio-threshold",
        type=float,
        default=1.35,
        help="Minimum ratio between latest cases and historical baseline for anomaly detection.",
    )
    parser.add_argument(
        "--region",
        type=str,
        default="northeast_india",
        help="Region filter to apply before anomaly detection. Example: northeast_india.",
    )
    return parser.parse_args()


def load_dataset(data_path=None, region="northeast_india"):
    if data_path is not None:
        path = data_path if data_path.is_absolute() else (ROOT / data_path)
    else:
        processed_candidates = [
            ROOT / "data" / "processed" / "northeast_india_processed.csv",
            ROOT / "data" / "processed" / "processed_data.csv",
            ROOT / "data" / "raw" / "Final_data.csv",
        ]
        path = next((candidate for candidate in processed_candidates if candidate.exists()), None)
        if path is None:
            raise FileNotFoundError(
                "No dataset found. Provide --data-path or ensure data/raw/Final_data.csv exists."
            )

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path)

    if "location_id" not in df.columns:
        print(f"Dataset {path.name} does not look processed. Preprocessing raw data for {region}...")
        df = preprocess_data(df, region=region, save_to_csv=True)

    return df


def detect_anomalies(df, z_threshold=2.0, ratio_threshold=1.35, region="northeast_india"):
    if df.empty:
        return pd.DataFrame(columns=[
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
        ])

    required_columns = {
        "location_id",
        "state_ut",
        "district",
        "Disease",
        "year",
        "week",
        "Cases",
        "preci",
        "LAI",
        "Temp",
    }
    missing = sorted(required_columns.difference(df.columns))
    if missing:
        raise ValueError(
            "Dataset is missing required columns for anomaly analysis: "
            + ", ".join(missing)
        )

    rows = []
    for location_id, group in df.groupby("location_id", sort=False):
        group = group.sort_values(["year", "week"]).reset_index(drop=True)
        if len(group) < 3:
            continue

        latest = group.iloc[-1]
        recent = group["Cases"].tail(4)
        historical = group["Cases"].iloc[:-1]

        if historical.empty:
            continue

        historical_mean = float(historical.mean())
        historical_std = float(historical.std(ddof=0))
        latest_cases = float(latest["Cases"])
        recent_avg = float(recent.mean())
        ratio = latest_cases / historical_mean if historical_mean > 0 else 0.0
        z_score = 0.0 if historical_std == 0 else abs((latest_cases - historical_mean) / historical_std)

        risk_assessment = assess_risk(
            predicted_cases=latest_cases,
            recent_cases=recent,
            historical_cases=historical,
            precipitation=latest["preci"],
            historical_precipitation=float(group["preci"].mean()),
            temperature=latest["Temp"],
            historical_temperature=float(group["Temp"].mean()),
            lai=latest["LAI"],
            historical_lai=float(group["LAI"].mean()),
        )

        anomaly_flag = bool(
            (ratio >= ratio_threshold and z_score >= z_threshold)
            or (latest_cases > recent_avg and ratio >= ratio_threshold)
        )

        if anomaly_flag:
            reasons = "; ".join(risk_assessment["reasons"])
        else:
            reasons = "Within expected range"

        rows.append(
            {
                "location_id": location_id,
                "state_ut": latest["state_ut"],
                "district": latest["district"],
                "disease": latest["Disease"],
                "latest_cases": latest_cases,
                "recent_avg_cases": recent_avg,
                "historical_avg_cases": historical_mean,
                "baseline_ratio": ratio,
                "z_score": z_score,
                "risk_level": risk_assessment["risk_level"],
                "score": risk_assessment["score"],
                "anomaly_flag": anomaly_flag,
                "reasons": reasons,
            }
        )

    result = pd.DataFrame(rows)
    if result.empty:
        return result

    if region is not None:
        region_key = str(region).strip().lower().replace("-", "_")
        if region_key in {"northeast_india", "northeast india", "north_east_india", "north_east india"}:
            allowed = {
                "Arunachal Pradesh",
                "Assam",
                "Manipur",
                "Meghalaya",
                "Mizoram",
                "Nagaland",
                "Sikkim",
                "Tripura",
            }
            result = result[result["state_ut"].isin(allowed)].copy()

    result = result.sort_values(
        by=["anomaly_flag", "score", "baseline_ratio"],
        ascending=[False, False, False],
    ).reset_index(drop=True)

    return result


def main():
    args = parse_args()

    df = load_dataset(args.data_path, region=args.region)
    anomalies = detect_anomalies(
        df,
        z_threshold=args.z_threshold,
        ratio_threshold=args.ratio_threshold,
        region=args.region,
    )

    output_path = args.output if args.output.is_absolute() else (ROOT / args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if anomalies.empty:
        print("No anomalies detected for the provided data.")
    else:
        top_rows = anomalies.head(args.top_n)
        print("\nTop anomaly signals:")
        print(top_rows.to_string(index=False))

    anomalies.to_csv(output_path, index=False)
    print(f"\nSaved anomaly report to: {output_path}")

    flagged = anomalies[anomalies["anomaly_flag"] == True]
    print(f"Detected {len(flagged)} anomaly records out of {len(anomalies)} locations.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
