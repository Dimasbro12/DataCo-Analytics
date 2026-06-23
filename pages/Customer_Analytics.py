from typing import List
import streamlit as st
import pandas as pd
from Utils import (
    kpi_customer_analytics,
    segment_customer_analytics,
    revenue_customer_analysis,
    state_customer_analytics,
    top_customers_customer_analytics,
    distribution_customer_analytics,
    market_customer_analytics,
    segmentrevenue_customer_analytics,
    load_filter_data
)
import plotly.express as px

from pages.Executive_Dashboard import display_donut_chart

st.set_page_config(page_title="Customer Analytics", layout="wide")

# ── Header + Date Filter ────────────────────────────────────────────────────
col1, col2, col3 = st.columns([2, 1, 1])
col1.title("Customer Analytics")

filter_df = load_filter_data()

with col2:
    start_date = pd.Timestamp(st.date_input("Select Start Date", value=filter_df["tanggal"].min()))
with col3:
    end_date = pd.Timestamp(st.date_input("Select End Date", value=filter_df["tanggal"].max()))

st.divider()

# ── Sub-header + Dropdown Filters ──────────────────────────────────────────
# bug fix: st.columns([2,1,1]) bukan [2,1,1,1] karena hanya 3 variabel
col1, col2, col3 = st.columns([2, 1, 1])
col1.subheader("Customer Analytics — DataCo Supply Chain")

with col2:
    st.write("Filter Market")
    market_filter = st.multiselect(
        "Pilih Market",
        options=sorted(filter_df["market"].unique()),
        default=sorted(filter_df["market"].unique())
    )
with col3:
    # bug fix: label & filter disesuaikan ke customer_segment, bukan product_category_name
    st.write("Filter Customer Segment")
    segment_filter = st.multiselect(
        "Pilih Customer Segment",
        options=sorted(filter_df["customer_segment"].unique()) if "customer_segment" in filter_df.columns else [],
        default=sorted(filter_df["customer_segment"].unique()) if "customer_segment" in filter_df.columns else []
    )

# ── Load semua data ────────────────────────────────────────────────────────
kpi_df            = kpi_customer_analytics()
segment_df        = segment_customer_analytics()
revenue_df        = revenue_customer_analysis()
state_df          = state_customer_analytics()
top_customers_df  = top_customers_customer_analytics()
distribution_df   = distribution_customer_analytics()
market_df         = market_customer_analytics()
segmentrevenue_df = segmentrevenue_customer_analytics()


# ── Helper: terapkan filter ke dataframe ──────────────────────────────────
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

    # bug fix: pakai segment_filter (bukan category_filter yang tidak terdefinisi)
    if "customer_segment" in filtered.columns and segment_filter:
        filtered = filtered[filtered["customer_segment"].isin(segment_filter)]

    return filtered


# Terapkan filter ke setiap dataframe
segment_df_f        = apply_filters(segment_df)
revenue_df_f        = apply_filters(revenue_df)
state_df_f          = apply_filters(state_df)
top_customers_df_f  = apply_filters(top_customers_df)
distribution_df_f   = apply_filters(distribution_df)
market_df_f         = apply_filters(market_df)
segmentrevenue_df_f = apply_filters(segmentrevenue_df)

# KPI — tidak ada kolom tanggal/market jadi tidak di-filter
customers       = kpi_df["total_customers"].iloc[0]
average_order   = kpi_df["avg_orders_per_customer"].iloc[0]
average_revenue = kpi_df["avg_revenue_per_customer"].iloc[0]


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

def display_donut_chart(df: pd.DataFrame, category_col: str, value_col: str, title: str):
    st.subheader(title)
    if df.empty:
        st.info("Tidak ada data untuk filter yang dipilih.")
        return
    fig = px.pie(df, names=category_col, values=value_col,
                 color_discrete_sequence=COLORS, hole=0.4)
    fig.update_layout(**LAYOUT, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)


def display_histogram(df: pd.DataFrame, x_col: str, title: str):
    st.subheader(title)
    if df.empty:
        st.info("Tidak ada data untuk filter yang dipilih.")
        return
    fig = px.histogram(df, x=x_col, color_discrete_sequence=["#4F8BF9"])
    fig.update_layout(**LAYOUT, showlegend=False)
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


def bubble_chart(df: pd.DataFrame, x_col: str, y_col: str, size_col: str, title: str):
    st.subheader(title)
    if df.empty:
        st.info("Tidak ada data untuk filter yang dipilih.")
        return
    fig = px.scatter(df, x=x_col, y=y_col, size=size_col,
                     color_discrete_sequence=["#4F8BF9"], size_max=60)
    fig.update_layout(**LAYOUT, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


# ── KPI Cards ─────────────────────────────────────────────────────────────
st.write("Kondisi Bisnis")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Customers", value=f"{int(customers):,}")
with col2:
    st.metric(label="Average Order", value=f"${average_order:,.2f}")
with col3:
    st.metric(label="Average Revenue", value=f"${average_revenue:,.2f}")
# col4 sengaja dikosongkan, bisa diisi KPI lain kalau ada

st.divider()

# ── Charts ─────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    display_donut_chart(segmentrevenue_df_f, category_col="customer_segment", value_col="total_revenue", title="Revenue by Customer Segment")
with col2:
    display_horizontal_bar_chart(state_df_f, x_col="total_customer", y_col="customer_state", title="Customer Count by State")
col1, col2 = st.columns(2)
with col1:
    display_horizontal_bar_chart(top_customers_df_f, x_col="sk_customer", y_col="total_revenue", title="Top Customers by Revenue")
with col2:
    display_bar_chart(revenue_df_f, x_col="customer_segment", y_col="total_revenue", title="Revenue by Customer Segment")

col1, col2 = st.columns(2)
with col1:
    display_histogram(distribution_df_f, x_col="total_revenue", title="Revenue Distribution Across Customers")
with col2:
    display_bar_chart(market_df_f, x_col="market", y_col="total_customers", title="Customer Count by Market")


bubble_chart(segmentrevenue_df_f, x_col="customer_segment", y_col="total_revenue", size_col="total_revenue", title="Revenue by Customer Segment (Bubble Chart)")
