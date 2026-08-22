# ==========================================
# HEALTHSEERS - SEQUENCE PREPARATION
# ==========================================

import pandas as pd
import numpy as np


def prepare_sequences(
    df,
    sequence_length=6,
    feature_columns=None,
    target_column="Cases"
):
    """
    Convert processed HealthSeers data into sequences
    suitable for LSTM training.

    Parameters
    ----------
    df : pandas.DataFrame
        Processed dataset.

    sequence_length : int
        Number of previous observations used
        to predict the next observation.

    feature_columns : list
        Features used as input to the model.

    target_column : str
        Column to predict.

    Returns
    -------
    X : numpy.ndarray
        Input sequences with shape:
        (samples, sequence_length, features)

    y : numpy.ndarray
        Target values.

    metadata : pandas.DataFrame
        Information about each target observation.
    """

    # ------------------------------------------
    # 1. DEFAULT FEATURES
    # ------------------------------------------

    if feature_columns is None:
        feature_columns = [
            "Cases",
            "preci",
            "LAI",
            "Temp"
        ]

    # ------------------------------------------
    # 2. CHECK REQUIRED COLUMNS
    # ------------------------------------------

    required_columns = (
        [
            "location_id",
            "year",
            "week",
            target_column
        ]
        + feature_columns
    )

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: "
            f"{missing_columns}"
        )

    # ------------------------------------------
    # 3. SORT DATA
    # ------------------------------------------

    df = df.copy()

    df = df.sort_values(
        by=[
            "location_id",
            "year",
            "week"
        ]
    ).reset_index(drop=True)

    # ------------------------------------------
    # 4. INITIALIZE STORAGE
    # ------------------------------------------

    X = []
    y = []

    location_ids = []
    target_years = []
    target_weeks = []

    # ------------------------------------------
    # 5. CREATE SEQUENCES
    # ------------------------------------------

    for location_id, group in df.groupby("location_id"):

        group = group.sort_values(
            by=[
                "year",
                "week"
            ]
        ).reset_index(drop=True)

        # Skip groups without enough observations
        if len(group) <= sequence_length:
            continue

        features = group[
            feature_columns
        ].values.astype(np.float32)

        targets = group[
            target_column
        ].values.astype(np.float32)

        # Create sliding window sequences
        for i in range(
            len(group) - sequence_length
        ):

            # Previous observations
            sequence = features[
                i : i + sequence_length
            ]

            # Next observation
            target_index = (
                i + sequence_length
            )

            target = targets[
                target_index
            ]

            X.append(sequence)
            y.append(target)

            # Save target metadata
            location_ids.append(location_id)

            target_years.append(
                group.iloc[target_index]["year"]
            )

            target_weeks.append(
                group.iloc[target_index]["week"]
            )

    # ------------------------------------------
    # 6. CONVERT TO NUMPY ARRAYS
    # ------------------------------------------

    X = np.array(
        X,
        dtype=np.float32
    )

    y = np.array(
        y,
        dtype=np.float32
    )

    # ------------------------------------------
    # 7. CREATE METADATA
    # ------------------------------------------

    metadata = pd.DataFrame(
        {
            "location_id": location_ids,
            "target_year": target_years,
            "target_week": target_weeks,
            "target_cases": y
        }
    )

    return X, y, metadata