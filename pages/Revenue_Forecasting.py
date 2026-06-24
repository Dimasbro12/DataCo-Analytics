import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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

st.title(
    "📈 Revenue Forecasting"
)

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "revenue_lstm.keras"
WINDOW_SIZE = 30


@st.cache_resource
def load_saved_model():
    from keras.models import load_model

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file tidak ditemukan: {MODEL_PATH}"
        )

    return load_model(str(MODEL_PATH))


def forecast_next_30_days(
    model,
    scaler,
    last_revenue,
    scaled_data,
    window_size=WINDOW_SIZE
):

    last_sequence = scaled_data[-window_size:]
    current_sequence = last_sequence.copy()
    future_diffs = []

    for _ in range(30):
        pred = model.predict(
            current_sequence.reshape(
                1,
                window_size,
                1
            ),
            verbose=0
        )

        future_diffs.append(pred[0][0])

        current_sequence = np.append(
            current_sequence[1:],
            pred
        ).reshape(
            window_size,
            1
        )

    future_diffs = scaler.inverse_transform(
        np.array(future_diffs).reshape(-1, 1)
    ).flatten()

    future_revenue = np.cumsum(future_diffs) + last_revenue
    return future_revenue


# =====================
# LOAD DATA
# =====================

df = load_lstmforecasting_data()

if len(df) < 100:
    st.error("Minimal 100 data harian.")
    st.stop()

# =====================
# OUTLIER
# =====================

outliers, lower, upper = detect_outliers_iqr(df)

df = cap_outliers(df, lower, upper)

# =====================
# DIFFERENCING
# =====================

df_diff = difference_data(df)

# =====================
# SCALING
# =====================

scaled_data, scaler = scale_data(df_diff)

# =====================
# FORECAST FROM SAVED MODEL
# =====================

try:
    model = load_saved_model()

    if len(scaled_data) < WINDOW_SIZE:
        st.warning(
            f"Data kurang dari {WINDOW_SIZE} baris setelah preprocessing."
        )
    else:
        future = forecast_next_30_days(
            model,
            scaler,
            df["revenue"].iloc[-1],
            scaled_data,
            window_size=WINDOW_SIZE
        )

        future_dates = pd.date_range(
            start=df["tanggal"].max() + pd.Timedelta(days=1),
            periods=30
        )

        forecast_df = pd.DataFrame({
            "tanggal": future_dates,
            "forecast": future.flatten()
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

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(forecast_df, use_container_width=True)

except FileNotFoundError as err:
    st.error(str(err))
    st.info(
        "Pastikan file model 'models/revenue_lstm.keras' sudah ada di folder aplikasi."
    )
except Exception as err:
    st.error(
        "Gagal memuat model atau memprediksi. Pastikan TensorFlow tersedia untuk memuat model Keras."
    )
    st.write(err)
