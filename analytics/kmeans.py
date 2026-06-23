from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score
)

FEATURES = [
    "revenue",
    "profit",
    "quantity_sold",
    "avg_discount",
    "total_orders"
]


def prepare_data(df):

    scaler = StandardScaler()

    X = scaler.fit_transform(
        df[FEATURES]
    )

    return X


def calculate_elbow(df):

    X = prepare_data(df)

    wcss = []

    for k in range(1, 11):

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        model.fit(X)

        wcss.append(
            model.inertia_
        )

    return wcss


def calculate_silhouette(df):

    X = prepare_data(df)

    scores = []

    for k in range(2, 11):

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        labels = model.fit_predict(X)

        scores.append(
            silhouette_score(
                X,
                labels
            )
        )

    return scores


def perform_clustering(df, k):

    X = prepare_data(df)

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