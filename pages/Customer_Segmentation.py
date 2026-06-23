import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from analytics.rfm import (
    calculate_elbow,
    calculate_silhouette,
    perform_clustering
)
from Utils import (
    load_rfm_data
)
st.title("👥 Customer Segmentation (RFM Analysis)")



df = load_rfm_data()

# =====================================
# RECENCY
# =====================================

analysis_date = df["last_purchase"].max()

df["recency"] = (
    analysis_date - df["last_purchase"]
).dt.days

# =====================================
# KPI
# =====================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Customer",
        len(df)
    )

with col2:
    st.metric(
        "Average Frequency",
        round(df["frequency"].mean(), 2)
    )

with col3:
    st.metric(
        "Average Monetary",
        f"${df['monetary'].mean():,.0f}"
    )

# =====================================
# ELBOW METHOD
# =====================================

st.subheader("Elbow Method")

wcss = calculate_elbow(df)

elbow_df = pd.DataFrame({
    "K": range(1,11),
    "WCSS": wcss
})

fig = px.line(
    elbow_df,
    x="K",
    y="WCSS",
    markers=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# SILHOUETTE
# =====================================

st.subheader("Silhouette Score")

scores = calculate_silhouette(df)

silhouette_df = pd.DataFrame({
    "K": range(2,11),
    "Score": scores
})

fig = px.line(
    silhouette_df,
    x="K",
    y="Score",
    markers=True
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
    f"Jumlah cluster terbaik: {best_k}"
)

# =====================================
# CLUSTERING
# =====================================

k = st.slider(
    "Jumlah Cluster",
    2,
    10,
    int(best_k)
)

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
st.subheader("Model Evaluation")

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

# =====================================
# SCATTER
# =====================================

st.subheader("Customer Segmentation")

fig = px.scatter(
    df_cluster,
    x="frequency",
    y="monetary",
    color=df_cluster["cluster"].astype(str),
    size="frequency",
    hover_data=["recency"]
)
centroids = (
    df_cluster
    .groupby("cluster")
    [["frequency", "monetary"]]
    .mean()
)

fig.add_trace(
    go.Scatter(
        x=centroids["frequency"],
        y=centroids["monetary"],
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

# =====================================
# SUMMARY
# =====================================

st.subheader("Cluster Summary")

summary = (
    df_cluster
    .groupby("cluster")
    .agg({
        "recency":"mean",
        "frequency":"mean",
        "monetary":"mean"
    })
    .round(2)
)

st.dataframe(
    summary,
    use_container_width=True
)


def assign_segment(row):
    if (
        row["monetary"] > summary["monetary"].median()
        and row["frequency"] > summary["frequency"].median()
    ):
        return "VIP Customer"

    elif (
        row["recency"] < summary["recency"].median()
        and row["frequency"] < summary["frequency"].median()
    ):
        return "New Customer"

    elif (
        row["recency"] > summary["recency"].median()
    ):
        return "Lost Customer"

    else:
        return "Regular Customer"

summary["segment"] = summary.apply(
    assign_segment,
    axis=1
)

# =====================================
# DISTRIBUSI
# =====================================

st.subheader("Customer Distribution")

distribution = (
    df_cluster["cluster"]
    .value_counts()
    .reset_index()
)

distribution.columns = [
    "cluster",
    "customer_count"
]

fig = px.pie(
    distribution,
    names="cluster",
    values="customer_count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================
# TOP CUSTOMER
# ==================================
st.subheader(
    "Top Customer by Cluster"
)

selected_cluster = st.selectbox(
    "Select Cluster",
    sorted(
        df_cluster["cluster"].unique()
    )
)

top_customer = (
    df_cluster[
        df_cluster["cluster"]
        == selected_cluster
    ]
    .sort_values(
        by="monetary",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_customer[
        [
            "sk_customer",
            "recency",
            "frequency",
            "monetary"
        ]
    ],
    use_container_width=True
)

# ==================================
# INTEPRETASI
# ==================================
st.subheader(
    "Cluster Interpretation"
)

for idx, row in summary.iterrows():

    st.info(
        f"""
        Cluster {idx}

        Segment : {row['segment']}

        Recency : {row['recency']:.2f}

        Frequency : {row['frequency']:.2f}

        Monetary : {row['monetary']:.2f}
        """
    )