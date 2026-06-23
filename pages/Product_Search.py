import streamlit as st
import plotly.express as px

from analytics.tfidf_search import (
    search_products,
    get_top_keywords
)

from Utils import (
    load_product_search_data
)

st.title("🔍 Product Search Engine")

st.markdown("""
### Sistem Temu Kembali Informasi (STKI)

Metode:
- TF-IDF
- Cosine Similarity
""")

# ==========================
# LOAD DATA
# ==========================

df = load_product_search_data()

# ==========================
# KPI
# ==========================

st.metric(
    "Total Product",
    len(df)
)

# ==========================
# TOP KEYWORDS TF-IDF
# ==========================

st.subheader("Top Keywords TF-IDF")

keyword_df = get_top_keywords(df)

st.dataframe(
    keyword_df,
    use_container_width=True
)

fig = px.bar(
    keyword_df,
    x="tfidf_score",
    y="keyword",
    orientation="h",
    title="Top Keywords by TF-IDF Score"
)

fig.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# SEARCH BOX
# ==========================

query = st.text_input(
    "Masukkan Kata Kunci",
    placeholder="running shoes"
)

# ==========================
# SEARCH PROCESS
# ==========================

if query:

    result = search_products(
        df,
        query,
        top_n=10
    )

    # ==========================
    # RETRIEVAL RESULT
    # ==========================

    st.subheader("Top 10 Produk Relevan")

    st.dataframe(
        result,
        use_container_width=True
    )

    # ==========================
    # RANKING RESULT
    # ==========================

    result = result.reset_index(
        drop=True
    )

    result["rank"] = (
        result.index + 1
    )

    st.subheader("Ranking Result")

    st.dataframe(
        result[
            [
                "rank",
                "product_name",
                "similarity"
            ]
        ],
        use_container_width=True
    )

    # ==========================
    # SIMILARITY SCORE
    # ==========================

    st.subheader(
        "Similarity Score"
    )

    fig = px.bar(
        result,
        x="similarity",
        y="product_name",
        orientation="h",
        title="Cosine Similarity Ranking"
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==========================
    # DISTRIBUTION
    # ==========================

    st.subheader(
        "Similarity Distribution"
    )

    fig = px.histogram(
        result,
        x="similarity",
        nbins=10,
        title="Distribution of Similarity Score"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================
# STKI PROCESS
# ==========================

st.subheader(
    "Information Retrieval Process"
)

st.markdown("""
### 1. Data Selection
- Product Name
- Product Category
- Product Department

### 2. Preprocessing
- Text Concatenation
- Missing Value Handling

### 3. Transformation
- TF-IDF Weighting

### 4. Similarity Computation
- Cosine Similarity

### 5. Ranking
- Similarity Score Sorting

### 6. Retrieval
- Top 10 Most Relevant Products
""")