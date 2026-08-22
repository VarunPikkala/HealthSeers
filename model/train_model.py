# ==========================================
# HEALTHSEERS - MODEL TRAINING SCRIPT
# ==========================================

import argparse
import sys
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
import keras
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import Dense, Dropout, Input, LSTM
from keras.models import Sequential

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from utils.preprocessing import preprocess_data
from utils.prepare_sequences import prepare_sequences


def parse_args():
    parser = argparse.ArgumentParser(
        description="Train the HealthSeers LSTM outbreak prediction model."
    )
    parser.add_argument(
        "--data-path",
        type=Path,
        default=ROOT / "data" / "raw" / "Final_data.csv",
        help="Path to the raw dataset CSV.",
    )
    parser.add_argument(
        "--region",
        type=str,
        default="northeast_india",
        help="Region filter to use when preparing the dataset for training.",
    )
    parser.add_argument(
        "--sequence-length",
        type=int,
        default=6,
        help="Number of weeks to use as input sequence length.",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=100,
        help="Number of training epochs.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Training batch size.",
    )
    parser.add_argument(
        "--patience",
        type=int,
        default=10,
        help="Early stopping patience.",
    )
    parser.add_argument(
        "--model-name",
        type=str,
        default="healthseers_lstm.keras",
        help="Filename to save the trained model as.",
    )
    return parser.parse_args()


def set_seed(seed=42):
    np.random.seed(seed)
    tf.random.set_seed(seed)


def split_time_aware(X, y, metadata):
    meta = metadata.copy().reset_index(drop=True)
    meta["sequence_index"] = np.arange(len(meta))

    if "location_id" not in meta.columns:
        raise ValueError(
            "metadata must contain 'location_id' for location-wise time splitting."
        )

    time_cols = []
    for col in ["target_year", "target_week", "year", "week"]:
        if col in meta.columns:
            time_cols.append(col)

    if not time_cols:
        raise ValueError(
            "Could not find time columns in metadata. Expected target_year/target_week or year/week."
        )

    train_idx, val_idx, test_idx = [], [], []

    for _, group in meta.groupby("location_id", sort=False):
        group = group.sort_values(time_cols)
        idx = group["sequence_index"].to_numpy()
        n = len(idx)

        if n < 3:
            continue

        train_end = max(1, int(n * 0.70))
        val_end = max(train_end + 1, int(n * 0.85))
        val_end = min(val_end, n - 1)

        train_idx.extend(idx[:train_end])
        val_idx.extend(idx[train_end:val_end])
        test_idx.extend(idx[val_end:])

    train_idx = np.array(train_idx)
    val_idx = np.array(val_idx)
    test_idx = np.array(test_idx)

    if train_idx.size == 0 or val_idx.size == 0 or test_idx.size == 0:
        raise ValueError(
            "Not enough sequences for a valid train/validation/test split. "
            "Check sequence_length and dataset coverage."
        )

    X_train, y_train = X[train_idx], y[train_idx]
    X_val, y_val = X[val_idx], y[val_idx]
    X_test, y_test = X[test_idx], y[test_idx]

    return X_train, y_train, X_val, y_val, X_test, y_test


def scale_features(X_train, X_val, X_test):
    feature_scaler = MinMaxScaler()
    n_features = X_train.shape[2]

    X_train_2d = X_train.reshape(-1, n_features)
    X_val_2d = X_val.reshape(-1, n_features)
    X_test_2d = X_test.reshape(-1, n_features)

    X_train_scaled = feature_scaler.fit_transform(X_train_2d).reshape(X_train.shape)
    X_val_scaled = feature_scaler.transform(X_val_2d).reshape(X_val.shape)
    X_test_scaled = feature_scaler.transform(X_test_2d).reshape(X_test.shape)

    return X_train_scaled, X_val_scaled, X_test_scaled, feature_scaler


def scale_target(y_train, y_val, y_test):
    y_train_log = np.log1p(y_train)
    y_val_log = np.log1p(y_val)
    y_test_log = np.log1p(y_test)

    target_scaler = StandardScaler()
    y_train_scaled = target_scaler.fit_transform(y_train_log.reshape(-1, 1)).ravel()
    y_val_scaled = target_scaler.transform(y_val_log.reshape(-1, 1)).ravel()
    y_test_scaled = target_scaler.transform(y_test_log.reshape(-1, 1)).ravel()

    return y_train_scaled, y_val_scaled, y_test_scaled, target_scaler


def build_model(input_shape):
    model = Sequential()
    model.add(Input(shape=input_shape))
    model.add(LSTM(64))
    model.add(Dropout(0.2))
    model.add(Dense(32, activation="relu"))
    model.add(Dense(1))
    model.compile(
        optimizer="adam",
        loss=tf.keras.losses.Huber(),
        metrics=["mae"],
    )
    return model


def main():
    args = parse_args()
    set_seed(42)

    data_path = args.data_path
    data_path = data_path if data_path.is_absolute() else (ROOT / data_path)

    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")

    print("Loading data from:", data_path)
    raw_df = pd.read_csv(data_path)

    print(f"Preprocessing raw data for region: {args.region}...")
    processed_df = preprocess_data(raw_df, region=args.region, save_to_csv=True)

    print("Creating sequences...")
    X, y, metadata = prepare_sequences(
        processed_df,
        sequence_length=args.sequence_length,
    )

    print(f"X shape: {X.shape} | y shape: {y.shape}")

    X_train, y_train, X_val, y_val, X_test, y_test = split_time_aware(
        X,
        y,
        metadata,
    )

    print("Training split:", X_train.shape)
    print("Validation split:", X_val.shape)
    print("Testing split:", X_test.shape)

    X_train_scaled, X_val_scaled, X_test_scaled, feature_scaler = scale_features(
        X_train,
        X_val,
        X_test,
    )

    y_train_scaled, y_val_scaled, y_test_scaled, target_scaler = scale_target(
        y_train,
        y_val,
        y_test,
    )

    model = build_model((X_train_scaled.shape[1], X_train_scaled.shape[2]))
    model.summary()

    model_dir = ROOT / "models"
    model_dir.mkdir(parents=True, exist_ok=True)

    checkpoint_path = model_dir / "best_lstm.keras"
    final_model_path = model_dir / args.model_name

    callbacks = [
        EarlyStopping(
            monitor="val_loss",
            patience=args.patience,
            restore_best_weights=True,
        ),
        ModelCheckpoint(
            filepath=checkpoint_path,
            monitor="val_loss",
            save_best_only=True,
        ),
    ]

    print("Training model...")
    history = model.fit(
        X_train_scaled,
        y_train_scaled,
        validation_data=(X_val_scaled, y_val_scaled),
        epochs=args.epochs,
        batch_size=args.batch_size,
        callbacks=callbacks,
        verbose="1",
    )

    print("Evaluating model...")
    y_pred_scaled = model.predict(X_test_scaled, verbose="0")
    y_pred_log = target_scaler.inverse_transform(y_pred_scaled).ravel()
    y_pred = np.expm1(y_pred_log)
    y_pred = np.clip(y_pred, 0, None)
    y_actual = y_test.copy()

    mae = mean_absolute_error(y_actual, y_pred)
    mse = mean_squared_error(y_actual, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_actual, y_pred)

    baseline_pred = np.full_like(y_actual, fill_value=np.mean(y_train), dtype=float)
    baseline_mae = mean_absolute_error(y_actual, baseline_pred)
    baseline_rmse = np.sqrt(mean_squared_error(y_actual, baseline_pred))

    print("=" * 45)
    print("HEALTHSEERS LSTM - TEST EVALUATION")
    print("=" * 45)
    print(f"MAE          : {mae:.2f} cases")
    print(f"RMSE         : {rmse:.2f} cases")
    print(f"R²           : {r2:.4f}")
    print("-" * 45)
    print(f"Baseline MAE : {baseline_mae:.2f} cases")
    print(f"Baseline RMSE: {baseline_rmse:.2f} cases")

    model.save(final_model_path)
    joblib.dump(feature_scaler, model_dir / "feature_scaler.pkl")
    joblib.dump(target_scaler, model_dir / "target_scaler.pkl")

    plt.figure(figsize=(8, 4))
    plt.plot(history.history["loss"], label="Training Loss")
    plt.plot(history.history["val_loss"], label="Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Huber Loss")
    plt.title("Training vs Validation Loss")
    plt.legend()
    plt.tight_layout()
    plt.savefig(model_dir / "training_loss.png", dpi=150)
    plt.close()

    print(f"\nSaved model to: {final_model_path}")
    print(f"Saved scalers to: {model_dir / 'feature_scaler.pkl'} and {model_dir / 'target_scaler.pkl'}")
    print(f"Saved training curve to: {model_dir / 'training_loss.png'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
