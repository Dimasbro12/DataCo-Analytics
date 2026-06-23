from typing import List
import streamlit as st
import pandas as pd
from Utils import (
    kpiavgship_logistic_analytics,
    kpilateorder_logistic_analytics,
    kpiontime_logistic_analytics,
    latedelivery_logistic_analytics,
    shipmode_logistic_analytics,
    deliverystatus_logistic_analytics,
    regionaldelay_logistic_analytics,
    marketdelay_logistic_analytics,
    deliveryperform_logistic_analytics,
    scheduledactual_logistic_analytics,
    shippingmodelatedeliv_logistic_analytics,
    load_filter_data,
)
import plotly.express as px

st.set_page_config(page_title="Logistic Analytics", layout="wide")

# ── Header + Date Filter ────────────────────────────────────────────────────
col1, col2, col3 = st.columns([2, 1, 1])
col1.title("Logistic Analytics")

filter_df = load_filter_data()

with col2:
    start_date = pd.Timestamp(st.date_input("Select Start Date", value=filter_df["tanggal"].min()))
with col3:
    end_date = pd.Timestamp(st.date_input("Select End Date", value=filter_df["tanggal"].max()))

st.divider()

# ── Sub-header + Dropdown Filters ──────────────────────────────────────────
col1, col2, col3 = st.columns([2, 1, 1])
col1.subheader("Logistic Analytics — DataCo Supply Chain")

with col2:
    st.write("Filter Market")
    market_filter = st.multiselect(
        "Pilih Market",
        options=sorted(filter_df["market"].unique()),
        default=sorted(filter_df["market"].unique())
    )
with col3:
    st.write("Filter Mode Shipping")
    shipping_filter = st.multiselect(
        "Pilih Mode Shipping",
        options=sorted(filter_df["shipping_mode"].unique()) if "shipping_mode" in filter_df.columns else [],
        default=sorted(filter_df["shipping_mode"].unique()) if "shipping_mode" in filter_df.columns else []
    )

# ── Load semua data ────────────────────────────────────────────────────────
kpi_avgship_df           = kpiavgship_logistic_analytics()
kpi_late_order_df        = kpilateorder_logistic_analytics()
kpi_on_time_df           = kpiontime_logistic_analytics()
late_delivery_df         = latedelivery_logistic_analytics()
shipmode_df              = shipmode_logistic_analytics()
deliverystatus_df        = deliverystatus_logistic_analytics()
regionaldelay_df         = regionaldelay_logistic_analytics()
marketdelay_df           = marketdelay_logistic_analytics()
deliveryperform_df       = deliveryperform_logistic_analytics()
scheduledactual_df       = scheduledactual_logistic_analytics()
shippingmodelatedeliv_df = shippingmodelatedeliv_logistic_analytics()


# ── Helper: terapkan filter ────────────────────────────────────────────────
def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df.copy()

    if "tanggal" in filtered.columns:
        filtered["tanggal"] = pd.to_datetime(filtered["tanggal"])
        filtered = filtered[
            (filtered["tanggal"] >= start_date) &
            (filtered["tanggal"] <= end_date)
        ]

    if "market" in filtered.columns and market_filter:
        filtered = filtered[filtered["market"].isin(market_filter)]

    if "shipping_mode" in filtered.columns and shipping_filter:
        filtered = filtered[filtered["shipping_mode"].isin(shipping_filter)]

    return filtered


# Terapkan filter
late_delivery_df_f         = apply_filters(late_delivery_df)
shipmode_df_f              = apply_filters(shipmode_df)
deliverystatus_df_f        = apply_filters(deliverystatus_df)
regionaldelay_df_f         = apply_filters(regionaldelay_df)
marketdelay_df_f           = apply_filters(marketdelay_df)
deliveryperform_df_f       = apply_filters(deliveryperform_df)
scheduledactual_df_f       = apply_filters(scheduledactual_df)
shippingmodelatedeliv_df_f = apply_filters(shippingmodelatedeliv_df)

# bug fix: KPI pakai .iloc[0] bukan Series langsung
average_shipping_time = kpi_avgship_df["average_shipping_time"].iloc[0] if not kpi_avgship_df.empty else 0
late_order            = kpi_late_order_df["late_order"].iloc[0]          if not kpi_late_order_df.empty else 0
on_time_rate          = kpi_on_time_df["on_time_rate"].iloc[0]           if not kpi_on_time_df.empty else 0


# ── Display helpers ────────────────────────────────────────────────────────
COLORS = ["#4F8BF9", "#00C49A", "#FF4B4B", "#FFB347", "#E694FF"]

LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#FFFFFF",
)


def display_bar_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str):
    st.subheader(title)
    if df.empty:
        st.info("Tidak ada data untuk filter yang dipilih.")
        return
    fig = px.bar(df, x=x_col, y=y_col,
                 color=x_col, color_discrete_sequence=COLORS)
    fig.update_layout(**LAYOUT, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def display_pie_chart(df: pd.DataFrame, category_col: str, value_col: str, title: str):
    st.subheader(title)
    if df.empty:
        st.info("Tidak ada data untuk filter yang dipilih.")
        return
    fig = px.pie(df, names=category_col, values=value_col,
                 color_discrete_sequence=COLORS)
    fig.update_traces(
        textfont_color="#FFFFFF",
        marker=dict(line=dict(color="#0E1117", width=2))
    )
    fig.update_layout(**LAYOUT, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)


def display_donut_chart(df: pd.DataFrame, category_col: str, value_col: str, title: str):
    st.subheader(title)
    if df.empty:
        st.info("Tidak ada data untuk filter yang dipilih.")
        return
    fig = px.pie(df, names=category_col, values=value_col,
                 color_discrete_sequence=COLORS, hole=0.4)
    fig.update_traces(
        textfont_color="#FFFFFF",
        marker=dict(line=dict(color="#0E1117", width=2))
    )
    fig.update_layout(**LAYOUT, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)


def display_horizontal_bar_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str):
    st.subheader(title)
    if df.empty:
        st.info("Tidak ada data untuk filter yang dipilih.")
        return
    fig = px.bar(df, x=x_col, y=y_col,
                 color=y_col, color_discrete_sequence=COLORS, orientation='h')
    fig.update_layout(**LAYOUT, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def display_line_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str):
    st.subheader(title)
    if df.empty:
        st.info("Tidak ada data untuk filter yang dipilih.")
        return
    fig = px.line(df, x=x_col, y=y_col, color_discrete_sequence=["#4F8BF9"])
    fig.update_traces(line_width=2)
    fig.update_layout(**LAYOUT, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def display_dual_axis_line_chart(df: pd.DataFrame, x_col: str, y1_col: str, y2_col: str, title: str):
    st.subheader(title)
    if df.empty:
        st.info("Tidak ada data untuk filter yang dipilih.")
        return
    fig = px.line(df, x=x_col, y=[y1_col, y2_col],
                  color_discrete_sequence=["#4F8BF9", "#FF4B4B"])
    fig.update_traces(line_width=2)
    fig.update_layout(**LAYOUT, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)


def display_stacked_bar_chart(df: pd.DataFrame, x_col: str, y_col: str, color_col: str, title: str):
    st.subheader(title)
    if df.empty:
        st.info("Tidak ada data untuk filter yang dipilih.")
        return
    fig = px.bar(df, x=x_col, y=y_col, color=color_col,
                 color_discrete_sequence=COLORS)
    fig.update_layout(**LAYOUT, barmode='stack', showlegend=True)
    st.plotly_chart(fig, use_container_width=True)


# ── KPI Cards ─────────────────────────────────────────────────────────────
st.write("Kondisi Logistik")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Average Shipping Time", value=f"{average_shipping_time} days")
with col2:
    st.metric(label="Late Orders", value=f"{int(late_order):,}")
with col3:
    # bug fix: on_time_rate sudah dalam persen (0-100), tidak perlu :.2%
    st.metric(label="On-Time Rate", value=f"{on_time_rate}%")

st.divider()

# ── Charts ─────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    display_donut_chart(late_delivery_df_f, category_col="late_delivery_risk", value_col="total_order", title="Late Delivery Risk Distribution")
with col2:
    display_horizontal_bar_chart(shipmode_df_f, x_col="avg_shipping_day", y_col="shipping_mode", title="Average Shipping Days by Shipping Mode")

col1, col2 = st.columns(2)
with col1:
    display_pie_chart(deliverystatus_df_f, category_col="delivery_status", value_col="total_order", title="Delivery Status Distribution")
with col2:
    display_horizontal_bar_chart(regionaldelay_df_f, x_col="late_order", y_col="market_order_region", title="Late Orders by Region")

col1, col2 = st.columns(2)
with col1:
    display_bar_chart(marketdelay_df_f, x_col="market", y_col="late_order", title="Late Orders by Market")
with col2:
    display_line_chart(deliveryperform_df_f, x_col="tanggal", y_col="on_time_rate", title="On-Time Rate Over Time")

col1, col2 = st.columns(2)
with col1:
    display_dual_axis_line_chart(scheduledactual_df_f, x_col="tanggal", y1_col="scheduled_days", y2_col="actual_days", title="Scheduled vs Actual Shipping Days")
with col2:
    display_stacked_bar_chart(shippingmodelatedeliv_df_f, x_col="shipping_mode", y_col="late_order", color_col="shipping_mode", title="Late Orders by Shipping Mode")