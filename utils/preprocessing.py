# ==========================================
# HEALTHSEERS - DATA PREPROCESSING
# ==========================================

import pandas as pd


def preprocess_data(
    df,
    min_observations=10
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
    # 4. FILTER TARGET DISEASES
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
    # 5. CLEAN CASES COLUMN
    # ==========================================

    df["Cases"] = pd.to_numeric(
        df["Cases"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip(),
        errors="coerce"
    )


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

    print(
        f"\nRemoved "
        f"{before_rows - len(df)} invalid rows"
    )


    # ==========================================
    # 8. HANDLE MISSING ENVIRONMENTAL VALUES
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
    # 9. DEFINE UNIQUE OBSERVATION
    # ==========================================

    group_columns = [
        "state_ut",
        "district",
        "Disease",
        "year",
        "week"
    ]


    # ==========================================
    # 10. AGGREGATE DUPLICATES
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
    )


    # ==========================================
    # 13. KEEP VALID LSTM GROUPS
    # ==========================================

    valid_groups = group_counts[
        group_counts["observations"]
        >= min_observations
    ].copy()


    # ==========================================
    # 14. FILTER VALID GROUPS
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
    # 15. CREATE LOCATION ID
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
    # 17. FINAL SORT
    # ==========================================

    processed_df = processed_df.sort_values(
        by=[
            "location_id",
            "year",
            "week"
        ]
    ).reset_index(drop=True)


    # ==========================================
    # 18. FINAL SUMMARY
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

    return processed_df