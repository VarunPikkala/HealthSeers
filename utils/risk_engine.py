"""Explainable community-level outbreak risk scoring for HealthSeers.

The engine intentionally does not diagnose individuals. It combines a model
forecast with recent case activity and environmental signals to produce a
simple, explainable district-level warning.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

import pandas as pd


LOW = "LOW"
MEDIUM = "MEDIUM"
HIGH = "HIGH"


def _number(value: Optional[float | int], name: str) -> Optional[float]:
	"""Return a finite float, or None when an optional signal is absent."""
	if value is None:
		return None
	try:
		result = float(value)
	except (TypeError, ValueError) as error:
		raise ValueError(f"{name} must be numeric") from error
	if result != result or result in (float("inf"), float("-inf")):
		raise ValueError(f"{name} must be finite")
	return result


def _average(values: Optional[Iterable[float | int]], name: str) -> Optional[float]:
	if values is None:
		return None
	cleaned = [_number(value, name) for value in values]
	if not cleaned:
		return None
	return sum(value for value in cleaned if value is not None) / len(cleaned)


def _elevation_score(value: Optional[float], baseline: Optional[float]) -> int:
	"""Score a signal compared with its local historical baseline."""
	if value is None or baseline is None or baseline <= 0:
		return 0
	ratio = value / baseline
	if ratio >= 1.5:
		return 3
	if ratio >= 1.2:
		return 2
	if ratio >= 1.05:
		return 1
	return 0


def classify_risk(score: int) -> str:
	"""Map the explainability score to the dashboard risk levels."""
	if score >= 6:
		return HIGH
	if score >= 3:
		return MEDIUM
	return LOW


def assess_risk(
	predicted_cases: float | int,
	recent_cases: Iterable[float | int],
	historical_cases: Optional[Iterable[float | int]] = None,
	precipitation: Optional[float | int] = None,
	historical_precipitation: Optional[float | int] = None,
	temperature: Optional[float | int] = None,
	historical_temperature: Optional[float | int] = None,
	lai: Optional[float | int] = None,
	historical_lai: Optional[float | int] = None,
) -> dict:
	"""Calculate an explainable district-level outbreak risk assessment.

	``historical_cases`` and environmental baselines should represent a
	comparable local period, such as the same district and disease. Signals
	without a baseline are ignored instead of being assigned an arbitrary
	risk. ``recent_cases`` should be ordered from oldest to newest.
	"""
	forecast = _number(predicted_cases, "predicted_cases")
	recent_average = _average(recent_cases, "recent_cases")
	historical_average = _average(historical_cases, "historical_cases")
	precipitation_value = _number(precipitation, "precipitation")
	precipitation_baseline = _number(
		historical_precipitation, "historical_precipitation"
	)
	temperature_value = _number(temperature, "temperature")
	temperature_baseline = _number(
		historical_temperature, "historical_temperature"
	)
	lai_value = _number(lai, "lai")
	lai_baseline = _number(historical_lai, "historical_lai")

	if historical_average is None or historical_average <= 0:
		raise ValueError("historical_cases must contain a positive baseline")

	score = 0
	reasons = []

	forecast_score = _elevation_score(forecast, historical_average)
	score += forecast_score
	if forecast_score:
		reasons.append("Predicted cases are above the historical baseline")
	if forecast_score >= 2:
		reasons.append("The forecast indicates a significant increase in cases")

	trend_score = _elevation_score(recent_average, historical_average)
	score += trend_score
	if trend_score:
		reasons.append("Recent cases are increasing above the historical baseline")

	precipitation_score = _elevation_score(
		precipitation_value, precipitation_baseline
	)
	score += precipitation_score
	if precipitation_score:
		reasons.append("Recent precipitation is high for this location")

	temperature_score = _elevation_score(temperature_value, temperature_baseline)
	score += temperature_score
	if temperature_score:
		reasons.append("Temperature is elevated compared with the local baseline")

	lai_score = 0
	if lai_value is not None and lai_baseline is not None and lai_baseline > 0:
		if lai_value / lai_baseline <= 0.8:
			lai_score = 1
			reasons.append("LAI is below the local environmental baseline")
	score += lai_score

	risk_level = classify_risk(score)
	if not reasons:
		reasons.append("Cases and available environmental signals are near baseline")

	recommendations = {
		LOW: ["Continue routine community health monitoring"],
		MEDIUM: [
			"Increase surveillance in the affected district",
			"Check local water and sanitation conditions",
		],
		HIGH: [
			"Issue a preventive health advisory",
			"Test local water sources",
			"Increase health surveillance and field reporting",
		],
	}[risk_level]

	return {
		"risk_level": risk_level,
		"score": score,
		"predicted_cases": forecast,
		"recent_average_cases": recent_average,
		"historical_average_cases": historical_average,
		"reasons": reasons,
		"recommended_actions": recommendations,
	}


def build_risk_table(
	data: pd.DataFrame,
	limit: Optional[int] = 20,
	region: Optional[str] = None,
) -> pd.DataFrame:
	"""Build a risk table from the processed HealthSeers dataset.

	Until the LSTM is integrated, the latest observed case count is used as a
	forecast proxy. This keeps the report useful for testing without hiding
	the fact that it is not yet an AI prediction.
	"""
	required_columns = {
		"location_id", "state_ut", "district", "Disease", "Cases",
		"preci", "LAI", "Temp",
	}
	missing_columns = required_columns.difference(data.columns)
	if missing_columns:
		raise ValueError(
			"Processed data is missing columns: " + ", ".join(sorted(missing_columns))
		)

	rows = []
	for location_id, group in data.groupby("location_id", sort=False):
		group = group.reset_index(drop=True)
		latest = group.iloc[-1]
		assessment = assess_risk(
			predicted_cases=latest["Cases"],
			recent_cases=group["Cases"].tail(4),
			historical_cases=group["Cases"],
			precipitation=latest["preci"],
			historical_precipitation=float(group["preci"].mean()),
			temperature=latest["Temp"],
			historical_temperature=float(group["Temp"].mean()),
			lai=latest["LAI"],
			historical_lai=float(group["LAI"].mean()),
		)
		rows.append({
			"location_id": location_id,
			"state_ut": latest["state_ut"],
			"district": latest["district"],
			"disease": latest["Disease"],
			"latest_cases": latest["Cases"],
			"risk_level": assessment["risk_level"],
			"score": assessment["score"],
			"reasons": "; ".join(assessment["reasons"]),
		})

	result = pd.DataFrame(rows).sort_values(
		by=["score", "latest_cases"], ascending=False
	)
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
	return result.head(limit) if limit is not None else result


def _print_risk_table() -> None:
	data_path = Path(__file__).resolve().parent.parent / "data" / "processed" / "processed_data.csv"
	if not data_path.exists():
		print(f"Processed dataset not found: {data_path}")
		print("Run utils/preprocessing.py first.")
		return

	risk_table = build_risk_table(pd.read_csv(data_path))
	if risk_table.empty:
		print("No district-disease records found.")
		return

	print("HealthSeers Risk Report (latest observed cases as forecast proxy)")
	print(risk_table.to_string(index=False))


if __name__ == "__main__":
	_print_risk_table()
