import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import tensorflow as tf
from pathlib import Path

from Utils import (
    load_lstmforecasting_data
)

from analytics.lstm_preprocessing import (
    detect_outliers_iqr,
    cap_outliers,
    difference_data,
    scale_data
)

from analytics.lstm_model import (
    train_model,
    forecast_next_30_days,
    split_data,
    create_sequences
)

from analytics.lstm_evaluation import (
    evaluate_model
)

st.title(
    "📈 Revenue Forecasting"
)

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "revenue_lstm.keras"

@st.cache_resource
def load_saved_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file tidak ditemukan: {MODEL_PATH}"
        )

    return tf.keras.models.load_model(
        str(MODEL_PATH)
    )

# =====================
# LOAD DATA
# =====================

df = load_lstmforecasting_data()

if len(df) < 100:

    st.error(
        "Minimal 100 data harian."
    )

    st.stop()

# =====================
# OUTLIER
# =====================

outliers, lower, upper = (
    detect_outliers_iqr(df)
)

df = cap_outliers(
    df,
    lower,
    upper
)

# =====================
# DIFFERENCING
# =====================

df_diff = difference_data(df)

# =====================
# SCALING
# =====================

scaled_data, scaler = (
    scale_data(df_diff)
)

# =====================
# TRAIN BUTTON
# =====================

if st.button(
    "Train Model"
):

    with st.spinner(
        "Training..."
    ):

        model, history, X_test, y_test = (
            train_model(
                scaled_data
            )
        )

        train, val, test = split_data(scaled_data)
        test_start = len(scaled_data) - len(test)
        window_size = 30

        if len(X_test) > 0:
            prev_revenue = df["revenue"].iloc[
                test_start + window_size:
                test_start + window_size + len(y_test)
            ].values

            actual_revenue_targets = df["revenue"].iloc[
                test_start + window_size + 1:
                test_start + window_size + 1 + len(y_test)
            ].values
        else:
            prev_revenue = None
            actual_revenue_targets = None

        mse, rmse, mae, mape = (
            evaluate_model(
                model,
                X_test,
                y_test,
                scaler,
                prev_revenue=prev_revenue,
                actual_revenue=actual_revenue_targets
            )
        )

        st.success(
            "Model berhasil disimpan."
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "MSE",
            round(mse, 2)
        )

        col2.metric(
            "RMSE",
            round(rmse, 2)
        )

        col3.metric(
            "MAE",
            round(mae, 2)
        )

        col4.metric(
            "MAPE",
            f"{mape:.2f}%"
        )

 

# =====================
# LOAD MODEL
# =====================

try:

    model = load_saved_model()

    train, val, test = split_data(scaled_data)
    X_test, y_test = create_sequences(test)
    test_start = len(scaled_data) - len(test)
    window_size = 30

    if len(X_test) > 0:
        prev_revenue = df["revenue"].iloc[
            test_start + window_size:
            test_start + window_size + len(y_test)
        ].values

        actual_revenue_targets = df["revenue"].iloc[
            test_start + window_size + 1:
            test_start + window_size + 1 + len(y_test)
        ].values

        mse, rmse, mae, mape = evaluate_model(
            model,
            X_test,
            y_test,
            scaler,
            prev_revenue=prev_revenue,
            actual_revenue=actual_revenue_targets
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "MSE",
            round(mse, 2)
        )

        col2.metric(
            "RMSE",
            round(rmse, 2)
        )

        col3.metric(
            "MAE",
            round(mae, 2)
        )

        col4.metric(
            "MAPE",
            f"{mape:.2f}%"
        )
    else:
        st.warning(
            "Tidak cukup data test untuk evaluasi model."
        )

    future = forecast_next_30_days(
        model,
        scaler,
        df["revenue"].iloc[-1],
        scaled_data
    )

    future_dates = pd.date_range(
        start=df["tanggal"].max()
        + pd.Timedelta(days=1),
        periods=30
    )

    forecast_df = pd.DataFrame({
        "tanggal":
        future_dates,

        "forecast":
        future.flatten()
    })

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["tanggal"],
            y=df["revenue"],
            name="Actual Revenue"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_df["tanggal"],
            y=forecast_df["forecast"],
            name="Forecast Revenue"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        forecast_df,
        use_container_width=True
    )

except:

    st.info(
        "Silakan train model terlebih dahulu."
    )