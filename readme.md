# HealthSeers

**Smart India Hackathon 2026 — Problem Statement SIH25001**
Smart Community Health Monitoring and Early Warning System for Water-Borne Diseases in Rural Northeast India

> **"See the Risk. Stop the Outbreak."**

---

## 1. Problem

Water-borne disease outbreaks spread fast in rural communities. By the time a spike in reported cases is obvious, exposure has often already happened. Health, water-quality, and weather data usually sit in separate silos, so early warning signals go unnoticed or arrive too late.

**Goal:** move from reactive outbreak *response* to proactive outbreak *prevention*.

## 2. Solution

HealthSeers is an AI-powered platform that fuses multiple signals — health-worker reports, water-quality readings, rainfall/weather data, geography, and historical outbreak patterns — into a single **community-level outbreak risk score**, with a plain-language explanation of *why* a village is flagged.

```
Community / Health Workers / Sensors / Public Data
                    │
              Data Collection
                    │
   Health + Water + Weather + Environmental Data
                    │
              Data Processing
                    │
             Anomaly Detection
                    │
             AI Risk Prediction
                    │
      Community Outbreak Risk Score
                    │
               Early Warning
                    │
     Health Authority Dashboard + Alerts
                    │
              Preventive Action
```

Example output style:

> **Village A → HIGH RISK** — Increased cases + contaminated water + recent heavy rainfall detected.

not just a bare probability number — the reasoning is the point.

## 3. MVP Scope

Built for hackathon demo purposes, not production scale:

- **1 simulated district**, ~25 villages
- **6 months of weekly data** (spans a monsoon period, since rainfall → contamination → case-spike is the core causal story)
- **2 diseases tracked:** Acute Diarrhoeal Disease, Cholera

## 4. Tech Stack

| Layer | Tool |
|---|---|
| Frontend | React |
| Backend | FastAPI (Python) |
| Database | PostgreSQL + PostGIS |
| ML | Scikit-learn, XGBoost |
| Visualization | Plotly |
| Maps | Leaflet / Mapbox |
| AI Assistant (optional) | Gemini + RAG over verified public-health guidelines |
| Deployment | Docker |

Stack may still shift depending on feasibility during the build.

## 5. Data

### Synthetic prototype dataset (`/dataset`)
Generated to have realistic causal structure rather than random noise — heavy rainfall → water contamination (lagged ~1 week) → case spike (lagged ~2-4 weeks) → decay. Used to unblock model-building before real data was sourced.

- `villages.csv` — 25 villages: location, population, water source type, past outbreak history
- `weekly_observations.csv` — 650 rows: rainfall, water quality, case counts, `risk_score` / `risk_level` per village-week
- `outbreak_events.csv` — ground-truth log of injected outbreak events, useful for demo narration

### Real-world reference data
- **[EpiClim](https://zenodo.org/records/14580510)** — weekly, district-wise epidemic + climate dataset for India (2009–2023), built from the government's IDSP surveillance data. Includes Acute Diarrhoeal Disease and Cholera case counts alongside rainfall, temperature, and geographic coordinates. Being filtered to Northeast Indian districts to ground the model/demo in real numbers.
- **[Water Potability (Kaggle)](https://www.kaggle.com/datasets/adityakadiwal/water-potability)** — realistic turbidity/pH/contamination value ranges, since no public dataset has village-level water-quality sensor readings at this granularity.

## 6. Project Structure

```
HealthSeers/
├── README.md
├── dataset/
│   ├── generate_dataset.py        # synthetic data generator
│   ├── villages.csv
│   ├── weekly_observations.csv
│   └── outbreak_events.csv
├── model/                         # (planned) risk prediction model
├── backend/                       # (planned) FastAPI service
├── frontend/                      # (planned) React dashboard + map
└── presentation/                  # (planned) SIH pitch deck assets
```

## 7. Status

| Stage | Status |
|---|---|
| Problem framing & pitch narrative | ✅ Done |
| Synthetic dataset (prototype) | ✅ Done |
| Real dataset sourcing (EpiClim) | 🔄 In progress — filtering to NE India |
| Risk prediction model | ⬜ Not started |
| Dashboard / map / alerts | ⬜ Not started |
| Pitch deck (Slides 4–10) | ⬜ Not started |

## 8. Team — HealthSeers

- Team ID / PS ID: SIH25001
- College: IEM UEM Kolkata

## 9. Next Steps

1. Download and filter EpiClim to Northeast Indian districts
2. Train a baseline risk classifier (XGBoost) — validate it flags risk *before* case counts peak
3. Build the FastAPI + PostgreSQL backend around the model
4. Build the React + Leaflet dashboard
5. Continue the pitch deck from Slide 4 onward