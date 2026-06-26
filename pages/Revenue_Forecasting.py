import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64

from Utils import load_lstmforecasting_data

from analytics.lstm_preprocessing import (
    detect_outliers_iqr,
    cap_outliers,
    difference_data,
    scale_data
)

from analytics.lstm_deploy import (
    load_saved_model,
    forecast_next_30_days
)

from analytics.lstm_utils import (
    split_data,
    create_sequences
)

from analytics.lstm_evaluation import (
    evaluate_model
)

# ======================
# Sidebar Background
# ======================

def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


sidebar_bg = get_base64("static/resized_200x900.png")

st.markdown(
    f"""
    <style>
    [data-testid="stSidebar"] {{
        background-image: url("data:image/jpg;base64,{sidebar_bg}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}

    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.set_page_config(
    page_title="Revenue Forecasting",
    layout="wide",
    page_icon="static/SUPERSTORE.png"
)

st.snow()
st.title("📈 Revenue Forecasting")

# ======================
# LOAD DATA
# ======================

df = load_lstmforecasting_data()

if len(df) < 100:
    st.error("Minimal 100 data harian.")
    st.stop()

# ======================
# PREPROCESSING
# ======================

outliers, lower, upper = detect_outliers_iqr(df)
df = cap_outliers(df, lower, upper)

df_diff = difference_data(df)

scaled_data, scaler = scale_data(df_diff)

# ======================
# LOAD MODEL
# ======================

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

        col1.metric("MSE", round(mse, 2))
        col2.metric("RMSE", round(rmse, 2))
        col3.metric("MAE", round(mae, 2))
        col4.metric("MAPE", f"{mape:.2f}%")

    else:
        st.warning("Tidak cukup data test untuk evaluasi model.")

    # ======================
    # FORECAST
    # ======================

    future = forecast_next_30_days(
        model,
        scaler,
        df["revenue"].iloc[-1],
        scaled_data
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

    st.dataframe(
        forecast_df,
        use_container_width=True
    )

except Exception as e:

    st.error("Model ONNX tidak dapat dimuat.")

    st.exception(e)
