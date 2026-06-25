from typing import List
import streamlit as st
import pandas as pd
from Utils import (
    kpi_executive_dashboard, trend_executive_dashboard,
    profit_executive_dashboard, sales_executive_dashboard,
    segment_executive_dashboard, status_executive_dashboard,
    shipping_executive_dashboard, load_filter_data
)
import plotly.express as px
import base64
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
    unsafe_allow_html=True
)
st.set_page_config(page_title="Executive Dashboard", layout="wide", page_icon="static/SUPERSTORE.png")
st.snow()


# ── Header + Date Filter ────────────────────────────────────────────────────
col1, col2, col3 = st.columns([2, 1, 1])
col1.title("Executive Dashboard")

filter_df = load_filter_data()

with col2:
    start_date = pd.Timestamp(st.date_input("Select Start Date", value=filter_df["tanggal"].min()))
with col3:
    end_date = pd.Timestamp(st.date_input("Select End Date", value=filter_df["tanggal"].max()))

st.divider()

# ── Sub-header + Dropdown Filters ──────────────────────────────────────────
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
col1.subheader("Executive Dashboard — DataCo Supply Chain")

with col2:
    st.write("Filter Kuartal")
    kuartal_filter = st.multiselect(
        "Pilih Kuartal",
        options=sorted(filter_df["kuartal"].unique()),
        default=sorted(filter_df["kuartal"].unique())
    )
with col3:
    st.write("Filter Market")
    market_filter = st.multiselect(
        "Pilih Market",
        options=sorted(filter_df["market"].unique()),
        default=sorted(filter_df["market"].unique())
    )
with col4:
    st.write("Filter Kategori Produk")
    category_filter = st.multiselect(
        "Pilih Kategori Produk",
        options=sorted(filter_df["product_category_name"].unique()),
        default=sorted(filter_df["product_category_name"].unique())
    )

# ── Load semua data ────────────────────────────────────────────────────────
kpi_df            = kpi_executive_dashboard()
trend_df          = trend_executive_dashboard()
profit_df         = profit_executive_dashboard()
sales_by_market_df = sales_executive_dashboard()
segment_df        = segment_executive_dashboard()
status_df         = status_executive_dashboard()
shipping_df       = shipping_executive_dashboard()


# ── Helper: terapkan filter ke dataframe ──────────────────────────────────
def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Terapkan date + kuartal + market + category ke dataframe manapun
    yang punya kolom tersebut."""
    filtered = df.copy()

    if "tanggal" in filtered.columns:
        filtered["tanggal"] = pd.to_datetime(filtered["tanggal"])
        filtered = filtered[
            (filtered["tanggal"] >= start_date) &
            (filtered["tanggal"] <= end_date)
        ]

    if "kuartal" in filtered.columns and kuartal_filter:
        filtered = filtered[filtered["kuartal"].isin(kuartal_filter)]

    if "market" in filtered.columns and market_filter:
        filtered = filtered[filtered["market"].isin(market_filter)]

    if "product_category_name" in filtered.columns and category_filter:
        filtered = filtered[filtered["product_category_name"].isin(category_filter)]

    return filtered


# Terapkan filter ke setiap dataframe
trend_df_f          = apply_filters(trend_df)
profit_df_f         = apply_filters(profit_df)
sales_by_market_df_f = apply_filters(sales_by_market_df)
segment_df_f        = apply_filters(segment_df)
status_df_f         = apply_filters(status_df)
shipping_df_f       = apply_filters(shipping_df)

# KPI di-rekalkulasi dari trend (karena kpi_df tidak punya kolom tanggal/market)
# Jika Utils kamu punya fungsi KPI yang bisa filter, ganti bagian ini
total_sales     = kpi_df["total_sales"].iloc[0]
total_profit    = kpi_df["total_profit"].iloc[0]
total_orders    = kpi_df["total_orders"].iloc[0]
total_customers = kpi_df["total_customers"].iloc[0]

# Kalau trend_df punya kolom revenue & profit, hitung ulang dari filtered data
if "revenue" in trend_df_f.columns:
    total_sales = trend_df_f["revenue"].sum()
if "profit" in profit_df_f.columns:
    total_profit = profit_df_f["profit"].sum()


# ── Display helpers ────────────────────────────────────────────────────────
COLORS = ["#4F8BF9", "#00C49A", "#FF4B4B", "#FFB347", "#E694FF"]

LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#FFFFFF",
)


def display_trend_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str):
    st.subheader(title)
    if df.empty:
        st.info("Tidak ada data untuk filter yang dipilih.")
        return
    fig = px.line(df, x=x_col, y=y_col, color_discrete_sequence=["#4F8BF9"])
    fig.update_traces(line_width=2)
    fig.update_layout(**LAYOUT)
    st.plotly_chart(fig, use_container_width=True)


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
                 hole=0.5, color_discrete_sequence=COLORS)
    fig.update_traces(
        textfont_color="#FFFFFF",
        marker=dict(line=dict(color="#0E1117", width=2))
    )
    fig.update_layout(**LAYOUT)
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
    fig.update_layout(**LAYOUT)
    st.plotly_chart(fig, use_container_width=True)


# ── KPI Cards ─────────────────────────────────────────────────────────────
st.write("Kondisi Bisnis")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
with col2:
    st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
with col3:
    st.metric(label="Total Orders", value=f"{int(total_orders):,}")
with col4:
    st.metric(label="Total Customers", value=f"{int(total_customers):,}")

st.divider()

# ── Charts ─────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    display_trend_chart(trend_df_f, x_col="tanggal", y_col="revenue", title="Revenue Over Time")
with col2:
    display_trend_chart(profit_df_f, x_col="tanggal", y_col="profit", title="Profit Over Time")

col1, col2 = st.columns(2)
with col1:
    display_bar_chart(sales_by_market_df_f, x_col="market", y_col="total_sales", title="Total Sales by Market")
with col2:
    display_donut_chart(segment_df_f, category_col="customer_segment", value_col="total_sales", title="Sales by Customer Segment")

col1, col2 = st.columns(2)
with col1:
    display_pie_chart(status_df_f, category_col="order_status", value_col="total_orders", title="Orders by Status")
with col2:
    display_pie_chart(shipping_df_f, category_col="shipping_mode", value_col="avg_shipping_days", title="Average Shipping Days by Shipping Mode")