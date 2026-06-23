import pandas as pd
import numpy as np
import streamlit as st
@st.cache_data(ttl=600)
def load_transaction_data():
    conn = st.connection("postgresql")
    df = conn.query("""
                    select
                    sk_orderdate,
                    sk_customer,
                    sk_product,
                    sk_market,
                    sk_order_shipping,
                    order_id,
                    order_status,
                    order_item_total,
                    sales,
                    order_profit_per_order,
                    order_item_discount_rate,
                    order_item_quantity,
                    days_for_shipping_real,
                    days_for_shipment_scheduled,
                    late_delivery_risk,
                    tanggal,
                    tahun_angka,
                    kuartal,
                    bulan,
                    customer_segment,
                    customer_state,
                    product_name,
                    product_price,
                    product_category_name,
                    product_department_name,
                    market,
                    market_order_city,
                    market_order_region,
                    market_order_state,
                    market_latitude,
                    market_longitude,
                    shipping_mode,
                    delivery_status
                    from fact.fact_transaction_dataco""")
    return df
    
@st.cache_data(ttl=600)
def kpi_executive_dashboard():
    conn = st.connection("postgresql")
    df = conn.query("""
                    select 
                    sum(sales) as total_sales,
                    sum(order_profit_per_order) as total_profit,
                    count(distinct order_id) as total_orders,
                    count(distinct sk_customer) as total_customers
                    from fact.fact_transaction_dataco
                    """)
    return df

@st.cache_data(ttl=600)
def trend_executive_dashboard():
    conn = st.connection("postgresql")
    df = conn.query("""
                    select
                    tanggal,
                    sum(sales) as revenue
                    from fact.fact_transaction_dataco
                    group by tanggal
                    order by tanggal;
                    """)
    return df

@st.cache_data(ttl=600)
def profit_executive_dashboard():
    conn = st.connection("postgresql")
    df = conn.query("""
                    select
                    tanggal,
                    sum(order_profit_per_order) as profit
                    from fact.fact_transaction_dataco
                    group by tanggal
                    order by tanggal;
                    """)
    return df

@st.cache_data(ttl=600)
def sales_executive_dashboard():
    conn = st.connection("postgresql")
    df = conn.query("""
                    select
                    market,
                    sum(sales) as total_sales
                    from fact.fact_transaction_dataco
                    group by market
                    order by total_sales desc;
                    """)
    return df

@st.cache_data(ttl=600)
def segment_executive_dashboard():
    conn = st.connection("postgresql")
    df = conn.query("""
                    select
                    customer_segment,
                    sum(sales) as total_sales
                    from fact.fact_transaction_dataco
                    group by customer_segment;
                    """)
    return df

@st.cache_data(ttl=600)
def status_executive_dashboard():
    conn = st.connection("postgresql")
    df = conn.query("""
                    select
                    order_status,
                    count(*) as total_orders
                    from fact.fact_transaction_dataco
                    group by order_status;
                    """)
    return df

@st.cache_data(ttl=600)
def shipping_executive_dashboard():
    conn = st.connection("postgresql")
    df = conn.query("""
                    select
                    shipping_mode,
                    AVG(days_for_shipping_real) as avg_shipping_days
                    from fact.fact_transaction_dataco
                    group by shipping_mode;
                    """)
    return df

@st.cache_data(ttl=600)
def kpi_customer_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
                    select 
                    count(distinct sk_customer) as total_customers,
                    sum(sales) / count(distinct sk_customer) as avg_revenue_per_customer,
                    count(order_id)::numeric/count(distinct sk_customer) as avg_orders_per_customer
                    from fact.fact_transaction_dataco
                    """)
    return df

@st.cache_data(ttl=600)
def segment_customer_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
                    select
                    customer_segment,
                    count(distinct sk_customer) as total_customer
                    from fact.fact_transaction_dataco
                    group by customer_segment
                    order by total_customer desc;
                    """)
    return df

@st.cache_data(ttl=600)
def revenue_customer_analysis():
    conn = st.connection("postgresql")
    df = conn.query("""
                    select
                    customer_segment,
                    sum(sales) as total_revenue
                    from fact.fact_transaction_dataco
                    group by customer_segment
                    order by total_revenue desc;
                    """)
    return df


@st.cache_data(ttl=600)
def state_customer_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
                    select
                    customer_state,
                    count(distinct sk_customer) as total_customer
                    from fact.fact_transaction_dataco
                    group by customer_state
                    order by total_customer desc
                    limit 10;
                    """)
    return df

@st.cache_data(ttl=600)
def top_customers_customer_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
                    select
                    sk_customer,
                    sum(sales) as total_revenue
                    from fact.fact_transaction_dataco
                    group by sk_customer
                    order by total_revenue desc
                    limit 10;
                    """)
    return df

@st.cache_data(ttl=600)
def distribution_customer_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
                    select
                    sk_customer,
                    sum(sales) as total_revenue
                    from fact.fact_transaction_dataco
                    group by sk_customer;
                    """)
    return df

@st.cache_data(ttl=600)
def market_customer_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
                    select
                    market,
                    count(distinct sk_customer) as total_customers
                    from fact.fact_transaction_dataco
                    group by market
                    order by total_customers desc;
                    """)
    return df

@st.cache_data(ttl=600)
def segmentrevenue_customer_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
                    select
                    customer_segment,
                    count(distinct sk_customer) as total_customers,
                    sum(sales) as total_revenue
                    from fact.fact_transaction_dataco
                    group by customer_segment;
                    """)
    return df



@st.cache_data(ttl=600)
def kpi_product_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            COUNT(DISTINCT product_name)            AS total_product,
            SUM(sales)                              AS total_revenue_product,
            SUM(order_profit_per_order)             AS total_profit_product
        FROM fact.fact_transaction_dataco
    """)
    return df
 
@st.cache_data(ttl=600)
def topsales_product_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            product_name,
            SUM(sales) AS total_sales
        FROM fact.fact_transaction_dataco
        GROUP BY product_name
        ORDER BY total_sales DESC
        LIMIT 10
    """)
    return df
 
@st.cache_data(ttl=600)
def topprof_product_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            product_name,
            SUM(order_profit_per_order) AS total_profit
        FROM fact.fact_transaction_dataco
        GROUP BY product_name
        ORDER BY total_profit DESC
        LIMIT 10
    """)
    return df
 
@st.cache_data(ttl=600)
def topcat_product_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            product_category_name,
            SUM(sales) AS total_sales
        FROM fact.fact_transaction_dataco
        GROUP BY product_category_name
        ORDER BY total_sales DESC
    """)
    return df
 
@st.cache_data(ttl=600)
def topcatprofit_product_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            product_category_name,
            SUM(order_profit_per_order) AS total_profit
        FROM fact.fact_transaction_dataco
        GROUP BY product_category_name
        ORDER BY total_profit DESC
    """)
    return df
 
@st.cache_data(ttl=600)
def topdepart_product_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            product_department_name,
            SUM(sales) AS total_sales
        FROM fact.fact_transaction_dataco
        GROUP BY product_department_name
        ORDER BY total_sales DESC
    """)
    return df
 
@st.cache_data(ttl=600)
def salesprof_product_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            product_name,
            SUM(sales)                  AS total_sales,
            SUM(order_profit_per_order) AS total_profit
        FROM fact.fact_transaction_dataco
        GROUP BY product_name
    """)
    return df
 
@st.cache_data(ttl=600)
def quantisold_product_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            product_name,
            SUM(order_item_quantity) AS total_quantity
        FROM fact.fact_transaction_dataco
        GROUP BY product_name
        ORDER BY total_quantity DESC
        LIMIT 10
    """)
    return df
 
@st.cache_data(ttl=600)
def discoimpact_product_analytics():
    conn = st.connection("postgresql")
    # bug fix: tambah koma yang hilang antara avg_discount_rate dan sum(profit)
    # bug fix: rename avg_discount_rate -> avg_discount supaya cocok dengan chart x_col
    df = conn.query("""
        SELECT
            product_name,
            AVG(order_item_discount_rate) AS avg_discount,
            SUM(order_profit_per_order)   AS total_profit
        FROM fact.fact_transaction_dataco
        GROUP BY product_name
    """)
    return df
 
@st.cache_data(ttl=600)
def revecontri_product_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            product_category_name,
            SUM(sales)                                                          AS total_sales,
            ROUND(
                (SUM(sales) * 100.0 / SUM(SUM(sales)) OVER ())::numeric, 2
            )                                                                   AS revenue_contribution
        FROM fact.fact_transaction_dataco
        GROUP BY product_category_name
        ORDER BY revenue_contribution DESC
    """)
    return df


@st.cache_data(ttl=600)
def kpiavgship_logistic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            ROUND(AVG(days_for_shipping_real)::numeric, 2) AS average_shipping_time
        FROM fact.fact_transaction_dataco
    """)
    return df
 
@st.cache_data(ttl=600)
def kpilateorder_logistic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            COUNT(*) AS late_order
        FROM fact.fact_transaction_dataco
        WHERE late_delivery_risk = 1
    """)
    return df
 
@st.cache_data(ttl=600)
def kpiontime_logistic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            ROUND(
                100.0 * SUM(CASE WHEN late_delivery_risk = 0 THEN 1 ELSE 0 END)
                / COUNT(*)::numeric, 2
            ) AS on_time_rate
        FROM fact.fact_transaction_dataco
    """)
    return df
 
@st.cache_data(ttl=600)
def latedelivery_logistic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            late_delivery_risk,
            COUNT(*) AS total_order
        FROM fact.fact_transaction_dataco
        GROUP BY late_delivery_risk
        ORDER BY late_delivery_risk
    """)
    return df
 
@st.cache_data(ttl=600)
def shipmode_logistic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            shipping_mode,
            ROUND(AVG(days_for_shipping_real)::numeric, 2) AS avg_shipping_day
        FROM fact.fact_transaction_dataco
        GROUP BY shipping_mode
        ORDER BY avg_shipping_day
    """)
    return df
 
@st.cache_data(ttl=600)
def deliverystatus_logistic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            delivery_status,
            COUNT(*) AS total_order
        FROM fact.fact_transaction_dataco
        GROUP BY delivery_status
        ORDER BY total_order DESC
    """)
    return df
 
@st.cache_data(ttl=600)
def regionaldelay_logistic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            market_order_region,
            COUNT(*) AS late_order
        FROM fact.fact_transaction_dataco
        WHERE late_delivery_risk = 1
        GROUP BY market_order_region
        ORDER BY late_order DESC
        LIMIT 10
    """)
    return df
 
@st.cache_data(ttl=600)
def marketdelay_logistic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            market,
            SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) AS late_order
        FROM fact.fact_transaction_dataco
        GROUP BY market
        ORDER BY late_order DESC
    """)
    return df
 
@st.cache_data(ttl=600)
def deliveryperform_logistic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            tanggal,
            ROUND(AVG(days_for_shipping_real)::numeric, 2) AS avg_shipping_day,
            ROUND(
                100.0 * SUM(CASE WHEN late_delivery_risk = 0 THEN 1 ELSE 0 END)
                / COUNT(*)::numeric, 2
            ) AS on_time_rate
        FROM fact.fact_transaction_dataco
        GROUP BY tanggal
        ORDER BY tanggal
    """)
    return df
 
@st.cache_data(ttl=600)
def scheduledactual_logistic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            tanggal,
            ROUND(AVG(days_for_shipping_real)::numeric, 2)       AS actual_days,
            ROUND(AVG(days_for_shipment_scheduled)::numeric, 2)  AS scheduled_days
        FROM fact.fact_transaction_dataco
        GROUP BY tanggal
        ORDER BY tanggal
    """)
    return df
 
@st.cache_data(ttl=600)
def shippingmodelatedeliv_logistic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            shipping_mode,
            SUM(CASE WHEN late_delivery_risk = 1 THEN 1 ELSE 0 END) AS late_order
        FROM fact.fact_transaction_dataco
        GROUP BY shipping_mode
        ORDER BY late_order DESC
    """)
    return df

 
@st.cache_data(ttl=600)
def totalrevenue_geographic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            SUM(sales) AS total_revenue
        FROM fact.fact_transaction_dataco
    """)
    return df
 
@st.cache_data(ttl=600)
def totalprofit_geographic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            SUM(order_profit_per_order) AS total_profit
        FROM fact.fact_transaction_dataco
    """)
    return df
 
@st.cache_data(ttl=600)
def totalcity_geographic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            COUNT(DISTINCT market_order_city) AS total_city
        FROM fact.fact_transaction_dataco
    """)
    return df
 
@st.cache_data(ttl=600)
def revenuemap_geographic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            market_order_city,
            AVG(market_latitude)  AS market_latitude,
            AVG(market_longitude) AS market_longitude,
            SUM(sales)            AS total_revenue
        FROM fact.fact_transaction_dataco
        GROUP BY market_order_city
        ORDER BY total_revenue DESC
    """)
    return df

@st.cache_data(ttl=600)
def profitmap_geographic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            market_order_city,
            AVG(market_latitude)        AS market_latitude,
            AVG(market_longitude)       AS market_longitude,
            SUM(order_profit_per_order) AS total_profit
        FROM fact.fact_transaction_dataco
        GROUP BY market_order_city
        ORDER BY total_profit DESC
    """)
    return df

@st.cache_data(ttl=600)
def revenueheatmap_geographic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            AVG(market_latitude)  AS market_latitude,
            AVG(market_longitude) AS market_longitude,
            SUM(sales)            AS total_revenue
        FROM fact.fact_transaction_dataco
        GROUP BY market_order_city
        ORDER BY total_revenue DESC
    """)
    return df
 
@st.cache_data(ttl=600)
def topcityrevenue_geographic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            market_order_city,
            SUM(sales) AS total_revenue
        FROM fact.fact_transaction_dataco
        GROUP BY market_order_city
        ORDER BY total_revenue DESC
        LIMIT 10
    """)
    return df

@st.cache_data(ttl=600)
def topcityprofit_geographic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            market_order_city,
            SUM(order_profit_per_order) AS total_profit
        FROM fact.fact_transaction_dataco
        GROUP BY market_order_city
        ORDER BY total_profit DESC
        LIMIT 10
    """)
    return df
 
@st.cache_data(ttl=600)
def revenueregion_geographic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            market_order_region,
            SUM(sales) AS total_revenue
        FROM fact.fact_transaction_dataco
        GROUP BY market_order_region
        ORDER BY total_revenue DESC
    """)
    return df
 
@st.cache_data(ttl=600)
def profitregion_geographic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            market_order_region,
            SUM(order_profit_per_order) AS total_profit
        FROM fact.fact_transaction_dataco
        GROUP BY market_order_region
        ORDER BY total_profit DESC
    """)
    return df
 
@st.cache_data(ttl=600)
def revenueheatmap_geographic_analytics():
    conn = st.connection("postgresql")
    df = conn.query("""
        SELECT
            market_latitude,
            market_longitude,
            SUM(sales) AS total_revenue
        FROM fact.fact_transaction_dataco
        GROUP BY market_latitude, market_longitude
    """)
    return df
 
@st.cache_data(ttl=600)
def revenueprofitcity_geographic_analytics():
    conn = st.connection("postgresql")
    # bug fix: tambah koma setelah market_order_city yang hilang
    df = conn.query("""
        SELECT
            market_order_city,
            SUM(sales)                  AS total_revenue,
            SUM(order_profit_per_order) AS total_profit
        FROM fact.fact_transaction_dataco
        GROUP BY market_order_city
    """)
    return df

@st.cache_data(ttl=600)
def load_product_clustering_data():
    conn = st.connection("postgresql")

    return conn.query("""
        select
            product_name,
            product_category_name,
            product_department_name,
            sum(sales) as revenue,
            sum(order_profit_per_order) as profit,
            sum(order_item_quantity) as quantity_sold,
            avg(order_item_discount_rate) as avg_discount,
            count(distinct order_id) as total_orders
        from fact.fact_transaction_dataco
        group by product_name, product_category_name, product_department_name
    """)

@st.cache_data(ttl=600)
def load_rfm_data():

    conn = st.connection("postgresql")

    return conn.query("""
        SELECT
            sk_customer,
            MAX(tanggal) AS last_purchase,
            COUNT(DISTINCT order_id) AS frequency,
            SUM(sales) AS monetary
        FROM fact.fact_transaction_dataco
        GROUP BY sk_customer
    """)

def load_product_search_data():

    conn = st.connection("postgresql")

    df = conn.query("""
        select
            product_name,
            product_category_name,
            product_department_name,

            avg(product_price) as product_price,
            sum(sales) as revenue

        from fact.fact_transaction_dataco

        group by
            product_name,
            product_category_name,
            product_department_name
    """)

    return df

def load_lstmforecasting_data():
    conn = st.connection("postgresql")
    df = conn.query("""
        select
            tanggal,
            sum(sales) as revenue
        from fact.fact_transaction_dataco
        group by tanggal
        order by tanggal
    """)
    df["tanggal"] = pd.to_datetime(
        df["tanggal"]
    )

    return df

# @st.cache_data(ttl=300)
# def load_data_quality():

#     conn = st.connection("postgresql")

#     duplicate_df = conn.query("""
#         SELECT
#             COUNT(*) - COUNT(DISTINCT transaksi_id)
#             AS duplicate_order
#         FROM fact.fact_transaction_dataco
#     """)

#     missing_df = conn.query("""
#         SELECT
#             SUM(
#                 CASE
#                     WHEN product_name IS NULL
#                     THEN 1 ELSE 0
#                 END
#             ) AS missing_product,

#             SUM(
#                 CASE
#                     WHEN customer_segment IS NULL
#                     THEN 1 ELSE 0
#                 END
#             ) AS missing_customer,

#             SUM(
#                 CASE
#                     WHEN sales IS NULL
#                     THEN 1 ELSE 0
#                 END
#             ) AS missing_sales

#         FROM fact.fact_transaction_dataco
#     """)

#     orphan_df = conn.query("""
#         SELECT COUNT(*) AS orphan_product
#         FROM fact.fact_transaction_dataco f
#         LEFT JOIN dimensi.dim_product p
#             ON f.sk_product = p.sk_product
#         WHERE p.sk_product IS NULL
#     """)

#     return (
#         duplicate_df,
#         missing_df,
#         orphan_df
#     )

@st.cache_data(ttl=300)
def load_etl_monitoring():

    conn = st.connection("postgresql")

    fact_count = conn.query("""
        select count(*) total_fact
        from fact.fact_transaction_dataco
    """)

    product_count = conn.query("""
        select count(*) total_product
        from dimensi.dim_product
    """)

    customer_count = conn.query("""
        select count(*) total_customer
        from dimensi.dim_customer
    """)

    market_count = conn.query("""
        select count(*) total_market
        from dimensi.dim_market
    """)

    refresh_date = conn.query("""
        select
            max(tanggal)
            as last_refresh
        from fact.fact_transaction_dataco
    """)

    return (
        fact_count,
        product_count,
        customer_count,
        market_count,
        refresh_date
    )

@st.cache_data(ttl=600)
def load_filter_data():
    conn = st.connection("postgresql")
    df = conn.query("""
                    select
                    tanggal,
                    kuartal,
                    market,
                    product_category_name,
                    customer_segment,
                    market_order_region,
                    market_order_city
                    from fact.fact_transaction_dataco
                    order by tanggal, kuartal, market, product_category_name, customer_segment, shipping_mode, market_order_region, market_order_city;
                    """)
    return df
