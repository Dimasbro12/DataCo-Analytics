from typing import List
import streamlit as st
import pandas as pd
# import folium
# from folium.plugins import HeatMap,FastMarkerCluster
# from streamlit_folium import st_folium
import plotly.express as px
from Utils import (
    totalrevenue_geographic_analytics,
    totalprofit_geographic_analytics,
    totalcity_geographic_analytics,
    revenuemap_geographic_analytics,
    profitmap_geographic_analytics,
    topcityrevenue_geographic_analytics,
    topcityprofit_geographic_analytics,
    revenueregion_geographic_analytics,
    profitregion_geographic_analytics,
    revenueheatmap_geographic_analytics,
    revenueprofitcity_geographic_analytics,
    load_filter_data
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
st.set_page_config(page_title="Geographic Analytics", layout="wide", page_icon="static/SUPERSTORE.png")
st.snow()


# ── Header + Date Filter ────────────────────────────────────────────────────
col1, col2, col3 = st.columns([2, 1, 1])
col1.title("Geographic Analytics")

filter_df = load_filter_data()

with col2:
    start_date = pd.Timestamp(st.date_input("Select Start Date", value=filter_df["tanggal"].min()))
with col3:
    end_date = pd.Timestamp(st.date_input("Select End Date", value=filter_df["tanggal"].max()))

st.divider()

# ── Sub-header + Dropdown Filters ──────────────────────────────────────────
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
col1.subheader("Geographic Analytics — DataCo Supply Chain")

with col2:
    st.write("Filter Market")
    market_filter = st.multiselect(
        "Pilih Market",
        options=sorted(filter_df["market"].unique()),
        default=sorted(filter_df["market"].unique())
    )
with col3:
    st.write("Filter Region")
    region_filter = st.multiselect(
        "Pilih Market Region",
        options=sorted(filter_df["market_order_region"].unique()) if "market_order_region" in filter_df.columns else [],
        default=sorted(filter_df["market_order_region"].unique()) if "market_order_region" in filter_df.columns else []
    )
with col4:
    st.write("Filter Market City")
    city_filter = st.multiselect(
        "Pilih Market City",
        options=sorted(filter_df["market_order_city"].unique()) if "market_order_city" in filter_df.columns else [],
        default=sorted(filter_df["market_order_city"].unique()) if "market_order_city" in filter_df.columns else []
    )

# ── Load semua data ────────────────────────────────────────────────────────
kpi_totalprofit_df   = totalprofit_geographic_analytics()
kpi_totalrevenue_df  = totalrevenue_geographic_analytics()
kpi_totalcity_df     = totalcity_geographic_analytics()
revenuemap_df        = revenuemap_geographic_analytics()
profitmap_df         = profitmap_geographic_analytics()
topcityrevenue_df    = topcityrevenue_geographic_analytics()
topcityprofit_df     = topcityprofit_geographic_analytics()
revenueregion_df     = revenueregion_geographic_analytics()
profitregion_df      = profitregion_geographic_analytics()
revenueheatmap_df    = revenueheatmap_geographic_analytics()
revenueprofitcity_df = revenueprofitcity_geographic_analytics()


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

    if "market_order_region" in filtered.columns and region_filter:
        filtered = filtered[filtered["market_order_region"].isin(region_filter)]

    if "market_order_city" in filtered.columns and city_filter:
        filtered = filtered[filtered["market_order_city"].isin(city_filter)]

    return filtered


# Terapkan filter
kpi_totalprofit_df_f   = apply_filters(kpi_totalprofit_df)
kpi_totalrevenue_df_f  = apply_filters(kpi_totalrevenue_df)
kpi_totalcity_df_f     = apply_filters(kpi_totalcity_df)
revenuemap_df_f        = apply_filters(revenuemap_df)
profitmap_df_f         = apply_filters(profitmap_df)
topcityrevenue_df_f    = apply_filters(topcityrevenue_df)
topcityprofit_df_f     = apply_filters(topcityprofit_df)
revenueregion_df_f     = apply_filters(revenueregion_df)
profitregion_df_f      = apply_filters(profitregion_df)
revenueheatmap_df_f    = apply_filters(revenueheatmap_df)
revenueprofitcity_df_f = apply_filters(revenueprofitcity_df)

# KPI
total_revenue = kpi_totalrevenue_df_f["total_revenue"].iloc[0] if not kpi_totalrevenue_df_f.empty else 0
total_profit  = kpi_totalprofit_df_f["total_profit"].iloc[0]   if not kpi_totalprofit_df_f.empty else 0
total_city    = kpi_totalcity_df_f["total_city"].iloc[0]       if not kpi_totalcity_df_f.empty else 0

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
    fig = px.bar(
        df, x=x_col, y=y_col,
        color=x_col,
        color_discrete_sequence=COLORS,
    )
    fig.update_layout(
        **LAYOUT,
        showlegend=False,
        bargap=0.2,
        xaxis=dict(tickangle=-30),
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)


def display_scatter_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str):
    st.subheader(title)
    if df.empty:
        st.info("Tidak ada data untuk filter yang dipilih.")
        return
    fig = px.scatter(
        df, x=x_col, y=y_col,
        hover_name="market_order_city" if "market_order_city" in df.columns else None,
        color_discrete_sequence=["#4F8BF9"],
    )
    fig.update_layout(**LAYOUT, showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)

def display_bubble_map(
    df,
    lat_col,
    lon_col,
    value_col,
    name_col,
    title
):
    st.subheader(title)

    if df.empty:
        st.info("Tidak ada data.")
        return

    map_df = df.copy()

    map_df[lat_col] = pd.to_numeric(
        map_df[lat_col],
        errors="coerce"
    )

    map_df[lon_col] = pd.to_numeric(
        map_df[lon_col],
        errors="coerce"
    )

    map_df = map_df.dropna(
        subset=[lat_col, lon_col]
    )
    st.write(df.shape)
    st.dataframe(df.head())
    st.map(
        map_df,
        latitude=lat_col,
        longitude=lon_col,
        size=value_col
    )

def display_map(
    df,
    lat_col,
    lon_col,
    value_col,
    title
):
    st.subheader(title)

    if df.empty:
        st.info("Tidak ada data.")
        return
    st.write(df.shape)
    st.dataframe(df.head())
    st.map(
        df,
        latitude=lat_col,
        longitude=lon_col
    )

# ── KPI Cards ─────────────────────────────────────────────────────────────
st.write("Kondisi Geografis")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
with col2:
    st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
with col3:
    st.metric(label="Total City", value=f"{int(total_city):,}")

st.divider()

# ── Charts ─────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    display_bubble_map(revenuemap_df_f, lat_col="market_latitude", lon_col="market_longitude", value_col="total_revenue", name_col="market_order_city", title="Revenue by City")
with col2:
    display_bubble_map(profitmap_df_f, lat_col="market_latitude", lon_col="market_longitude", value_col="total_profit", name_col="market_order_city", title="Profit by City")

col1, col2 = st.columns(2)
with col1:
    display_bar_chart(topcityrevenue_df_f, x_col="market_order_city", y_col="total_revenue", title="Top 10 City by Revenue")
with col2:
    display_bar_chart(topcityprofit_df_f, x_col="market_order_city", y_col="total_profit", title="Top 10 City by Profit")

col1, col2 = st.columns(2)
with col1:
    display_bar_chart(revenueregion_df_f, x_col="market_order_region", y_col="total_revenue", title="Revenue by Region")
with col2:
    display_bar_chart(profitregion_df_f, x_col="market_order_region", y_col="total_profit", title="Profit by Region")

col1, col2 = st.columns(2)
with col1:
    display_map(revenueheatmap_df_f, lat_col="market_latitude", lon_col="market_longitude", value_col="total_revenue", title="Revenue Density Map")
with col2:
    display_scatter_chart(revenueprofitcity_df_f, x_col="total_revenue", y_col="total_profit", title="Revenue vs Profit by City")