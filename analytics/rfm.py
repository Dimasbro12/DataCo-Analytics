from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import (silhouette_score, davies_bouldin_score, calinski_harabasz_score)


RFM_FEATURES = [
    "recency",
    "frequency",
    "monetary"
]


def prepare_rfm(df):

    scaler = StandardScaler()

    X = scaler.fit_transform(
        df[RFM_FEATURES]
    )

    return X


def calculate_elbow(df):

    X = prepare_rfm(df)

    wcss = []

    for k in range(1, 11):

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        model.fit(X)

        wcss.append(model.inertia_)

    return wcss


def calculate_silhouette(df):

    X = prepare_rfm(df)

    scores = []

    for k in range(2, 11):

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        labels = model.fit_predict(X)

        scores.append(
            silhouette_score(X, labels)
        )

    return scores

def perform_clustering(df, k):

    X = prepare_rfm(df)

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(X)

    df = df.copy()

    df["cluster"] = labels

    silhouette = silhouette_score(
        X,
        labels
    )

    dbi = davies_bouldin_score(
        X,
        labels
    )

    ch = calinski_harabasz_score(
        X,
        labels
    )

    return (
        df,
        model,
        silhouette,
        dbi,
        ch
    )
