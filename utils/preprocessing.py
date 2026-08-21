# ==========================================
# HEALTHSEERS - DATA PREPROCESSING
# ==========================================

import pandas as pd
from pathlib import Path


# ==========================================
# 1. PROJECT PATHS
# ==========================================

# Current file:
# HealthSeers/utils/preprocessing.py
#
# Go up from utils/ to HealthSeers/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Final_data.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "processed_data.csv"
)


# ==========================================
# 2. LOAD DATA
# ==========================================

print("=" * 60)
print("HEALTHSEERS - DATA PREPROCESSING")
print("=" * 60)

print("\nProject Root:")
print(PROJECT_ROOT)

print("\nLoading data from:")
print(DATA_PATH)

# Check whether the dataset exists
if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"\nDataset not found!\n"
        f"Expected location:\n{DATA_PATH}\n\n"
        f"Make sure your project structure is:\n"
        f"HealthSeers/\n"
        f"├── data/\n"
        f"│   └── raw/\n"
        f"│       └── Final_data.csv\n"
        f"└── utils/\n"
        f"    └── preprocessing.py"
    )

df = pd.read_csv(DATA_PATH)

print("\nOriginal Dataset Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())


# ==========================================
# 3. REMOVE UNNECESSARY INDEX COLUMN
# ==========================================

df = df.drop(
    columns=["Unnamed: 0"],
    errors="ignore"
)

print("\nShape after removing unnecessary columns:")
print(df.shape)


# ==========================================
# 4. FILTER WATER-BORNE DISEASES
# ==========================================

TARGET_DISEASES = [
    "Acute Diarrhoeal Disease",
    "Cholera"
]

df = df[
    df["Disease"].isin(TARGET_DISEASES)
].copy()

print("\n" + "=" * 60)
print("FILTERED DISEASES")
print("=" * 60)

print(df["Disease"].value_counts())

print("\nShape after filtering:")
print(df.shape)


# ==========================================
# 5. CLEAN CASES COLUMN
# ==========================================

df["Cases"] = pd.to_numeric(
    df["Cases"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.strip(),
    errors="coerce"
)

print("\n" + "=" * 60)
print("CASES COLUMN")
print("=" * 60)

print("Data Type:", df["Cases"].dtype)

print("Missing Cases:")
print(df["Cases"].isnull().sum())


# ==========================================
# 6. EXTRACT NUMERIC WEEK
# ==========================================

df["week"] = (
    df["week_of_outbreak"]
    .astype(str)
    .str.extract(r"(\d+)")[0]
)

df["week"] = pd.to_numeric(
    df["week"],
    errors="coerce"
)

print("\n" + "=" * 60)
print("WEEK PROCESSING")
print("=" * 60)

print(
    df[
        [
            "week_of_outbreak",
            "week"
        ]
    ].head(10)
)


# ==========================================
# 7. REMOVE INVALID ROWS
# ==========================================

before_rows = len(df)

df = df.dropna(
    subset=[
        "Cases",
        "year",
        "week"
    ]
).copy()

df["year"] = df["year"].astype(int)
df["week"] = df["week"].astype(int)

print("\nRows before removing invalid data:", before_rows)
print("Rows after removing invalid data:", len(df))


# ==========================================
# 8. HANDLE MISSING ENVIRONMENTAL DATA
# ==========================================

environmental_features = [
    "preci",
    "LAI",
    "Temp"
]

print("\n" + "=" * 60)
print("MISSING ENVIRONMENTAL VALUES - BEFORE")
print("=" * 60)

print(
    df[
        environmental_features
    ].isnull().sum()
)


# Fill missing environmental values using median
for col in environmental_features:

    median_value = df[col].median()

    df[col] = df[col].fillna(
        median_value
    )


print("\n" + "=" * 60)
print("MISSING ENVIRONMENTAL VALUES - AFTER")
print("=" * 60)

print(
    df[
        environmental_features
    ].isnull().sum()
)


# ==========================================
# 9. CHECK DUPLICATES
# ==========================================

group_columns = [
    "state_ut",
    "district",
    "Disease",
    "year",
    "week"
]

duplicate_count = df.duplicated(
    subset=group_columns
).sum()

print("\n" + "=" * 60)
print("DUPLICATE CHECK")
print("=" * 60)

print("Duplicate Records:", duplicate_count)


# ==========================================
# 10. AGGREGATE DUPLICATE RECORDS
# ==========================================

df = (
    df
    .groupby(
        group_columns,
        as_index=False
    )
    .agg(
        {
            "Cases": "sum",
            "preci": "mean",
            "LAI": "mean",
            "Temp": "mean",
            "Latitude": "first",
            "Longitude": "first"
        }
    )
)


print("\nShape after aggregation:")
print(df.shape)


# ==========================================
# 11. SORT CHRONOLOGICALLY
# ==========================================

df = df.sort_values(
    by=[
        "state_ut",
        "district",
        "Disease",
        "year",
        "week"
    ]
).reset_index(drop=True)


# ==========================================
# 12. COUNT OBSERVATIONS PER LOCATION
# ==========================================

group_counts = (
    df
    .groupby(
        [
            "state_ut",
            "district",
            "Disease"
        ]
    )
    .size()
    .reset_index(
        name="observations"
    )
    .sort_values(
        "observations",
        ascending=False
    )
)


print("\n" + "=" * 60)
print("OBSERVATIONS PER DISTRICT-DISEASE")
print("=" * 60)

print("\nTop 20 groups:")
print(group_counts.head(20))

print("\nObservation Statistics:")
print(
    group_counts[
        "observations"
    ].describe()
)


# ==========================================
# 13. KEEP LOCATIONS WITH ENOUGH DATA
# ==========================================

MIN_OBSERVATIONS = 10

valid_groups = group_counts[
    group_counts["observations"]
    >= MIN_OBSERVATIONS
].copy()


print("\n" + "=" * 60)
print("VALID LSTM GROUPS")
print("=" * 60)

print(
    f"Groups with at least "
    f"{MIN_OBSERVATIONS} observations:"
)

print(len(valid_groups))


# ==========================================
# 14. FILTER DATA TO VALID GROUPS
# ==========================================

df = df.merge(
    valid_groups[
        [
            "state_ut",
            "district",
            "Disease"
        ]
    ],
    on=[
        "state_ut",
        "district",
        "Disease"
    ],
    how="inner"
)


# ==========================================
# 15. CREATE UNIQUE LOCATION ID
# ==========================================

df["location_id"] = (
    df["state_ut"].astype(str)
    + "_"
    + df["district"].astype(str)
    + "_"
    + df["Disease"].astype(str)
)


# ==========================================
# 16. SELECT FINAL COLUMNS
# ==========================================

final_columns = [
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
    "Latitude",
    "Longitude"
]

processed_df = df[
    final_columns
].copy()


# ==========================================
# 17. FINAL CHRONOLOGICAL SORT
# ==========================================

processed_df = processed_df.sort_values(
    by=[
        "location_id",
        "year",
        "week"
    ]
).reset_index(drop=True)


# ==========================================
# 18. CREATE OUTPUT DIRECTORY
# ==========================================

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================
# 19. SAVE PROCESSED DATA
# ==========================================

processed_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ==========================================
# 20. FINAL RESULTS
# ==========================================

print("\n" + "=" * 60)
print("PREPROCESSING COMPLETE")
print("=" * 60)

print("\nFinal Dataset Shape:")
print(processed_df.shape)

print("\nUnique Locations:")
print(
    processed_df[
        "location_id"
    ].nunique()
)

print("\nDisease Distribution:")
print(
    processed_df[
        "Disease"
    ].value_counts()
)

print("\nMissing Values:")
print(
    processed_df.isnull().sum()
)

print("\nFirst 10 Rows:")
print(
    processed_df.head(10)
)

print("\nProcessed dataset saved successfully!")

print("\nOutput Location:")
print(OUTPUT_PATH)

print("\n" + "=" * 60)
print("HEALTHSEERS PREPROCESSING FINISHED SUCCESSFULLY")
print("=" * 60)