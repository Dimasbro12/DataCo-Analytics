import pandas as pd

from sklearn.preprocessing import MinMaxScaler


def detect_outliers_iqr(df):

    Q1 = df["revenue"].quantile(0.25)
    Q3 = df["revenue"].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - (1.5 * IQR)
    upper = Q3 + (1.5 * IQR)

    outliers = df[
        (df["revenue"] < lower) |
        (df["revenue"] > upper)
    ]

    return outliers, lower, upper


def cap_outliers(df, lower, upper):

    df = df.copy()

    df["revenue"] = df["revenue"].clip(
        lower=lower,
        upper=upper
    )

    return df


def difference_data(df):

    df = df.copy()

    df["revenue_diff"] = (
        df["revenue"].diff()
    )

    df = df.dropna()

    return df


def scale_data(df):

    scaler = MinMaxScaler()

    scaled = scaler.fit_transform(
        df[["revenue_diff"]]
    )

    return scaled, scaler