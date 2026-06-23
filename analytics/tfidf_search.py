from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


def search_products(df, query, top_n=10):

    df = df.copy()

    df["document"] = (
        df["product_name"].fillna("") + " " +
        df["product_category_name"].fillna("") + " " +
        df["product_department_name"].fillna("")
    )

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(
        df["document"]
    )

    query_vector = vectorizer.transform(
        [query]
    )

    similarity_scores = cosine_similarity(
        query_vector,
        tfidf_matrix
    )

    df["similarity"] = similarity_scores.flatten()

    result = (
        df.sort_values(
            by="similarity",
            ascending=False
        )
        .head(top_n)
    )

    return result


def get_top_keywords(df, top_n=20):

    df = df.copy()

    df["document"] = (
        df["product_name"].fillna("") + " " +
        df["product_category_name"].fillna("") + " " +
        df["product_department_name"].fillna("")
    )

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(
        df["document"]
    )

    feature_names = (
        vectorizer.get_feature_names_out()
    )

    scores = tfidf_matrix.sum(axis=0)

    keyword_df = pd.DataFrame({
        "keyword": feature_names,
        "tfidf_score": scores.A1
    })

    keyword_df = (
        keyword_df
        .sort_values(
            by="tfidf_score",
            ascending=False
        )
        .head(top_n)
    )

    return keyword_df