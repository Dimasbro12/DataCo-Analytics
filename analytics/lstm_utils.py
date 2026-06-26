import numpy as np

def create_sequences(
    data,
    window_size=30
):

    X = []
    y = []

    for i in range(
        window_size,
        len(data)
    ):

        X.append(
            data[
                i-window_size:i
            ]
        )

        y.append(
            data[i]
        )

    return (
        np.array(X),
        np.array(y)
    )


def split_data(data):

    train_size = int(
        len(data) * 0.70
    )

    val_size = int(
        len(data) * 0.15
    )

    train = data[:train_size]

    val = data[
        train_size:
        train_size + val_size
    ]

    test = data[
        train_size + val_size:
    ]

    return train, val, test