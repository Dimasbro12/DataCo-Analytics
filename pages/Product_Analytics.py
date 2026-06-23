from typing import List
import streamlit as st
import pandas as pd
from Utils import (
    kpi_product_analytics,
    topsales_product_analytics,
    topprof_product_analytics,
    topcat_product_analytics,
    topcatprofit_product_analytics,
    topdepart_product_analytics,
    salesprof_product_analytics,
    quantisold_product_analytics,
    discoimpact_product_analytics,
    revecontri_product_analytics,
    load_filter_data
)
import plotly.express as px

st.set_page_config(page_title="Product Analytics", layout="wide")

# ── Header + Date Filter ────────────────────────────────────────────────────
col1, col2, col3 = st.columns([2, 1, 1])
col1.title("Product Analytics")

filter_df = load_filter_data()

with col2:
    start_date = pd.Timestamp(st.date_input("Select Start Date", value=filter_df["tanggal"].min()))
with col3:
    end_date = pd.Timestamp(st.date_input("Select End Date", value=filter_df["tanggal"].max()))

st.divider()

# ── Sub-header + Dropdown Filters ──────────────────────────────────────────
col1, col2, col3 = st.columns([2, 1, 1])
col1.subheader("Product Analytics — DataCo Supply Chain")

with col2:
    st.write("Filter Kuartal")
    kuartal_filter = st.multiselect(
        "Pilih Kuartal",
        options=sorted(filter_df["kuartal"].unique()),
        default=sorted(filter_df["kuartal"].unique())
    )
with col3:
    st.write("Filter Kategori Produk")
    category_filter = st.multiselect(
        "Pilih Kategori Produk",
        options=sorted(filter_df["product_category_name"].unique()),
        default=sorted(filter_df["product_category_name"].unique())
    )

# ── Load semua data ────────────────────────────────────────────────────────
kpi_df            = kpi_product_analytics()
top_sales_df      = topsales_product_analytics()
top_profit_df     = topprof_product_analytics()
top_cat_df        = topcat_product_analytics()
top_cat_profit_df = topcatprofit_product_analytics()
top_depart_df     = topdepart_product_analytics()
sales_profit_df   = salesprof_product_analytics()
quan_sold_df      = quantisold_product_analytics()
disco_impact_df   = discoimpact_product_analytics()
reve_contri_df    = revecontri_product_analytics()


# ── Helper: terapkan filter ────────────────────────────────────────────────
def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df.copy()

    if "tanggal" in filtered.columns:
        filtered["tanggal"] = pd.to_datetime(filtered["tanggal"])
        filtered = filtered[
            (filtered["tanggal"] >= start_date) &
            (filtered["tanggal"] <= end_date)
        ]

    if "kuartal" in filtered.columns and kuartal_filter:
        filtered = filtered[filtered["kuartal"].isin(kuartal_filter)]

    if "product_category_name" in filtered.columns and category_filter:
        filtered = filtered[filtered["product_category_name"].isin(category_filter)]

    return filtered


# Terapkan filter
top_sales_df_f      = apply_filters(top_sales_df)
top_profit_df_f     = apply_filters(top_profit_df)
top_cat_df_f        = apply_filters(top_cat_df)
top_cat_profit_df_f = apply_filters(top_cat_profit_df)
top_depart_df_f     = apply_filters(top_depart_df)
sales_profit_df_f   = apply_filters(sales_profit_df)
quan_sold_df_f      = apply_filters(quan_sold_df)
disco_impact_df_f   = apply_filters(disco_impact_df)
reve_contri_df_f    = apply_filters(reve_contri_df)

# KPI — ambil dari kolom yang sudah disesuaikan di Utils
total_product         = kpi_df["total_product"].iloc[0]
total_revenue_product = kpi_df["total_revenue_product"].iloc[0]
total_profit_product  = kpi_df["total_profit_product"].iloc[0]


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


def display_scatter_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str):
    st.subheader(title)
    if df.empty:
        st.info("Tidak ada data untuk filter yang dipilih.")
        return
    fig = px.scatter(df, x=x_col, y=y_col, color_discrete_sequence=["#4F8BF9"])
    fig.update_layout(**LAYOUT, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


# ── KPI Cards ─────────────────────────────────────────────────────────────
st.write("Kondisi Bisnis")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Product", value=f"{int(total_product):,}")
with col2:
    st.metric(label="Total Revenue", value=f"${total_revenue_product:,.2f}")
with col3:
    st.metric(label="Total Profit", value=f"${total_profit_product:,.2f}")
# col4 kosong, bisa diisi KPI lain

st.divider()

# ── Charts ─────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    display_horizontal_bar_chart(top_sales_df_f, x_col="total_sales", y_col="product_name", title="Top 10 Products by Revenue")
with col2:
    display_horizontal_bar_chart(top_profit_df_f, x_col="total_profit", y_col="product_name", title="Top 10 Products by Profit")

col1, col2 = st.columns(2)
with col1:
    display_bar_chart(top_cat_df_f, x_col="product_category_name", y_col="total_sales", title="Revenue by Product Category")
with col2:
    display_bar_chart(top_cat_profit_df_f, x_col="product_category_name", y_col="total_profit", title="Profit by Product Category")

col1, col2 = st.columns(2)
with col1:
    display_donut_chart(top_depart_df_f, category_col="product_department_name", value_col="total_sales", title="Revenue by Product Department")
with col2:
    display_scatter_chart(sales_profit_df_f, x_col="total_sales", y_col="total_profit", title="Sales vs Profit by Product")

col1, col2 = st.columns(2)
with col1:
    display_horizontal_bar_chart(quan_sold_df_f, x_col="total_quantity", y_col="product_name", title="Top 10 Products by Quantity Sold")
with col2:
    # bug fix: x_col pakai "avg_discount" sesuai alias di query
    display_scatter_chart(disco_impact_df_f, x_col="avg_discount", y_col="total_profit", title="Discount Impact on Profit")

display_donut_chart(reve_contri_df_f, category_col="product_category_name", value_col="revenue_contribution", title="Revenue Contribution by Category")