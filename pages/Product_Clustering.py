import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from analytics.kmeans import (
    calculate_elbow,
    calculate_silhouette,
    perform_clustering
)

from Utils import (
    load_product_clustering_data
)
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
st.set_page_config(page_title="Product Clustering", layout="wide", page_icon="static/SUPERSTORE.png")
st.snow()
st.title("📦 Product Clustering")

# ==================================
# LOAD DATA
# ==================================

df = load_product_clustering_data()

# ==================================
# KPI
# ==================================

st.subheader("Product Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Product",
        len(df)
    )

with col2:
    st.metric(
        "Category",
        df["product_category_name"].nunique()
    )

with col3:
    st.metric(
        "Department",
        df["product_department_name"].nunique()
    )

# ==================================
# ELBOW METHOD
# ==================================

st.subheader("Elbow Method")

wcss = calculate_elbow(df)

elbow_df = pd.DataFrame({
    "K": range(1, 11),
    "WCSS": wcss
})

fig = px.line(
    elbow_df,
    x="K",
    y="WCSS",
    markers=True,
    title="Elbow Method"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================
# SILHOUETTE SCORE
# ==================================

st.subheader("Silhouette Score")

scores = calculate_silhouette(df)

silhouette_df = pd.DataFrame({
    "K": range(2, 11),
    "Score": scores
})

fig = px.line(
    silhouette_df,
    x="K",
    y="Score",
    markers=True,
    title="Silhouette Score"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

best_k = silhouette_df.loc[
    silhouette_df["Score"].idxmax(),
    "K"
]

st.success(
    f"Jumlah cluster terbaik berdasarkan Silhouette Score = {best_k}"
)

# ==================================
# CLUSTER SELECTION
# ==================================

k = st.slider(
    "Jumlah Cluster",
    min_value=2,
    max_value=10,
    value=int(best_k)
)

# ==================================
# KMEANS
# ==================================

(
    df_cluster,
    model,
    silhouette,
    dbi,
    ch
) = perform_clustering(
    df,
    k
)

# ==================================
# EVALUATION
# ==================================

st.subheader("Cluster Evaluation")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Silhouette Score",
        round(silhouette, 3)
    )

with col2:
    st.metric(
        "Davies-Bouldin",
        round(dbi, 3)
    )

with col3:
    st.metric(
        "Calinski-Harabasz",
        round(ch, 2)
    )

# ==================================
# CLUSTER VISUALIZATION
# ==================================

st.subheader("Product Cluster")

fig = px.scatter(
    df_cluster,
    x="revenue",
    y="profit",
    color="cluster",
    symbol="cluster",
    size="quantity_sold",
    hover_name="product_name",
    hover_data=[
        "total_orders",
        "avg_discount"
    ]
)

# # log scale
# fig.update_xaxes(
#     type="log",
#     title="Revenue"
# )

# fig.update_yaxes(
#     type="log",
#     title="Profit"
# )

# centroid

centroids = (
    df_cluster
    .groupby("cluster")
    [["revenue", "profit"]]
    .mean()
)

fig.add_trace(
    go.Scatter(
        x=centroids["revenue"],
        y=centroids["profit"],
        mode="markers+text",
        text=[
            f"C{i}"
            for i in centroids.index
        ],
        textposition="top center",
        marker=dict(
            size=20,
            symbol="x"
        ),
        name="Centroid"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================
# CLUSTER SUMMARY
# ==================================

st.subheader("Cluster Summary")

summary = (
    df_cluster
    .groupby("cluster")
    .agg({
        "revenue": "mean",
        "profit": "mean",
        "quantity_sold": "mean",
        "avg_discount": "mean",
        "total_orders": "mean"
    })
    .round(2)
)

summary = summary.sort_values(
    by="revenue",
    ascending=False
)

segment_names = [
    "Best Seller",
    "Regular Product",
    "Low Performer",
    "Emerging Product",
    "Niche Product",
    "Seasonal Product",
    "Growth Product",
    "Premium Product",
    "Discount Product",
    "Other"
]

summary["segment"] = (
    segment_names[:len(summary)]
)

st.dataframe(
    summary,
    use_container_width=True
)

# ==================================
# CLUSTER DISTRIBUTION
# ==================================

st.subheader("Cluster Distribution")

cluster_dist = (
    df_cluster["cluster"]
    .value_counts()
    .reset_index()
)

cluster_dist.columns = [
    "cluster",
    "total_product"
]

fig = px.pie(
    cluster_dist,
    names="cluster",
    values="total_product",
    title="Product Distribution by Cluster"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================
# TOP PRODUCT
# ==================================

st.subheader("Top Product by Cluster")

selected_cluster = st.selectbox(
    "Select Cluster",
    sorted(
        df_cluster["cluster"].unique()
    )
)

top_product = (
    df_cluster[
        df_cluster["cluster"]
        == selected_cluster
    ]
    .sort_values(
        by="revenue",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_product[
        [
            "product_name",
            "revenue",
            "profit",
            "quantity_sold",
            "total_orders"
        ]
    ],
    use_container_width=True
)

# ==================================
# INTERPRETATION
# ==================================

st.subheader("Cluster Interpretation")

for idx, row in summary.iterrows():

    st.info(
        f"""
        Cluster {idx}

        Segment : {row['segment']}

        Revenue : {row['revenue']:,.2f}

        Profit : {row['profit']:,.2f}

        Quantity Sold : {row['quantity_sold']:,.2f}

        Average Discount : {row['avg_discount']:,.2f}

        Total Orders : {row['total_orders']:,.2f}
        """
    )

# ==================================
# DATA MINING PROCESS
# ==================================

st.subheader("Data Mining Process")

st.markdown("""
### 1. Data Selection
- Revenue
- Profit
- Quantity Sold
- Average Discount
- Total Orders

### 2. Preprocessing
- Data aggregation per product
- Missing value handling
- Duplicate checking

### 3. Transformation
- StandardScaler normalization

### 4. Data Mining
- K-Means Clustering

### 5. Evaluation
- Elbow Method
- Silhouette Score
- Davies-Bouldin Index
- Calinski-Harabasz Index

### 6. Knowledge Presentation
- Product Segmentation
- Cluster Visualization
- Business Insight
""")