# ==========================================
# HEALTHSEERS - DATA PREPROCESSING
# ==========================================

from pathlib import Path

import pandas as pd


NORTHEAST_INDIA_STATES = {
    "Arunachal Pradesh",
    "Assam",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Sikkim",
    "Tripura",
}


def preprocess_data(
    df,
    min_observations=10,
    region="northeast_india",
    save_to_csv=True,
    output_path=None
):
    """
    Preprocess HealthSeers raw disease data.

    Parameters
    ----------
    df : pandas.DataFrame
        Raw input dataset.

    min_observations : int, default=10
        Minimum number of observations required
        for a district-disease group.

    region : str, default="northeast_india"
        Region filter applied before training. Supported values include
        northeast_india, north_east_india, india, and all.

    save_to_csv : bool, default=True
        Whether to save the final processed DataFrame to CSV.

    output_path : str or Path, optional
        Custom CSV destination. If not provided and save_to_csv is True,
        the file is written to data/processed/<region>_processed.csv.

    Returns
    -------
    processed_df : pandas.DataFrame
        Cleaned and processed dataset ready
        for sequence preparation.
    """

    # ==========================================
    # 1. CREATE A COPY
    # ==========================================

    df = df.copy()

    print("=" * 60)
    print("HEALTHSEERS - DATA PREPROCESSING")
    print("=" * 60)

    print("\nOriginal Shape:", df.shape)


    # ==========================================
    # 2. REMOVE UNNECESSARY INDEX COLUMN
    # ==========================================

    df = df.drop(
        columns=["Unnamed: 0"],
        errors="ignore"
    )


    # ==========================================
    # 3. CHECK REQUIRED COLUMNS
    # ==========================================

    required_columns = [
        "state_ut",
        "district",
        "Disease",
        "year",
        "week_of_outbreak",
        "Cases",
        "preci",
        "LAI",
        "Temp",
        "Latitude",
        "Longitude"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: "
            f"{missing_columns}"
        )


    # ==========================================
    # 4. FILTER BY REGION (DEFAULT: NORTHEAST INDIA)
    # ==========================================

    region_key = str(region).strip().lower().replace("-", "_")
    region_map = {
        "northeast_india": NORTHEAST_INDIA_STATES,
        "northeast india": NORTHEAST_INDIA_STATES,
        "north_east_india": NORTHEAST_INDIA_STATES,
        "north_east india": NORTHEAST_INDIA_STATES,
        "india": None,
        "all": None,
    }

    region_states = region_map.get(region_key)
    if region_states is not None:
        df = df[
            df["state_ut"].isin(region_states)
        ].copy()
        print(f"\nFiltered to Northeast India states: {sorted(region_states)}")

    # ==========================================
    # 5. FILTER TARGET DISEASES
    # ==========================================

    target_diseases = [
        "Acute Diarrhoeal Disease",
        "Cholera"
    ]

    df = df[
        df["Disease"].isin(target_diseases)
    ].copy()

    print("\nDisease Distribution:")
    print(df["Disease"].value_counts())


    # ==========================================
    # 6. CLEAN CASES COLUMN
    # ==========================================

    df["Cases"] = pd.to_numeric(
        df["Cases"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip(),
        errors="coerce"
    )


    # ==========================================
    # 7. EXTRACT NUMERIC WEEK
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


    # ==========================================
    # 8. REMOVE INVALID ROWS
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

    print(
        f"\nRemoved "
        f"{before_rows - len(df)} invalid rows"
    )


    # ==========================================
    # 9. HANDLE MISSING ENVIRONMENTAL VALUES
    # ==========================================

    environmental_features = [
        "preci",
        "LAI",
        "Temp"
    ]

    for col in environmental_features:

        median_value = df[col].median()

        df[col] = df[col].fillna(
            median_value
        )


    # ==========================================
    # 10. DEFINE UNIQUE OBSERVATION
    # ==========================================

    group_columns = [
        "state_ut",
        "district",
        "Disease",
        "year",
        "week"
    ]


    # ==========================================
    # 11. AGGREGATE DUPLICATES
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


    # ==========================================
    # 12. SORT CHRONOLOGICALLY
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
    # 13. COUNT OBSERVATIONS PER LOCATION
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
    )


    # ==========================================
    # 14. KEEP VALID LSTM GROUPS
    # ==========================================

    valid_groups = group_counts[
        group_counts["observations"]
        >= min_observations
    ].copy()


    # ==========================================
    # 15. FILTER VALID GROUPS
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
    # 16. CREATE LOCATION ID
    # ==========================================

    df["location_id"] = (
        df["state_ut"].astype(str)
        + "_"
        + df["district"].astype(str)
        + "_"
        + df["Disease"].astype(str)
    )


    # ==========================================
    # 17. SELECT FINAL COLUMNS
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
    # 18. FINAL SORT
    # ==========================================

    processed_df = processed_df.sort_values(
        by=[
            "location_id",
            "year",
            "week"
        ]
    ).reset_index(drop=True)


    # ==========================================
    # 19. FINAL SUMMARY
    # ==========================================

    print("\n" + "=" * 60)
    print("PREPROCESSING COMPLETE")
    print("=" * 60)

    print(
        "\nProcessed Dataset Shape:",
        processed_df.shape
    )

    print(
        "Unique Locations:",
        processed_df["location_id"].nunique()
    )

    print("\nMissing Values:")
    print(
        processed_df.isnull().sum()
    )

    if save_to_csv:
        if output_path is None:
            base_dir = Path(__file__).resolve().parent.parent / "data" / "processed"
            base_dir.mkdir(parents=True, exist_ok=True)
            region_name = str(region).strip().lower().replace(" ", "_").replace("-", "_")
            output_path = base_dir / f"{region_name}_processed.csv"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

        processed_df.to_csv(output_path, index=False)
        print(f"\nSaved processed data to: {output_path}")

    return processed_df