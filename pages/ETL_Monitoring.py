import streamlit as st

from Utils import (
    load_etl_monitoring
)

st.title("⚙️ ETL Monitoring")

(
    fact_count,
    product_count,
    customer_count,
    market_count,
    refresh_date
) = load_etl_monitoring()

# ======================
# KPI
# ======================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Fact Rows",
        fact_count.iloc[0]["total_fact"]
    )

with col2:
    st.metric(
        "Product Dim",
        product_count.iloc[0]["total_product"]
    )

with col3:
    st.metric(
        "Customer Dim",
        customer_count.iloc[0]["total_customer"]
    )

with col4:
    st.metric(
        "Market Dim",
        market_count.iloc[0]["total_market"]
    )

# ======================
# LAST REFRESH
# ======================

st.subheader("Last Refresh")

st.success(
    refresh_date.iloc[0]["last_refresh"]
)

# ======================
# SUMMARY TABLE
# ======================

summary = {
    "Table": [
        "Fact Transaction",
        "Dim_Product",
        "Dim_Customer",
        "Dim_Market"
    ],
    "Rows": [
        fact_count.iloc[0]["total_fact"],
        product_count.iloc[0]["total_product"],
        customer_count.iloc[0]["total_customer"],
        market_count.iloc[0]["total_market"]
    ]
}

st.dataframe(
    summary,
    use_container_width=True
)