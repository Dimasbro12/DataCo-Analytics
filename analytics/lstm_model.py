import os
import numpy as np
import tensorflow as tf
Sequential = tf.keras.Sequential
LSTM = tf.keras.layers.LSTM
Dense = tf.keras.layers.Dense
Dropout = tf.keras.layers.Dropout
EarlyStopping = tf.keras.callbacks.EarlyStopping
ModelCheckpoint = tf.keras.callbacks.ModelCheckpoint


MODEL_PATH = (
    "models/revenue_lstm.keras"
)


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


def build_model():

    model = Sequential()

    model.add(
        LSTM(
            64,
            return_sequences=True,
            input_shape=(30, 1)
        )
    )

    model.add(
        Dropout(0.2)
    )

    model.add(
        LSTM(32)
    )

    model.add(
        Dropout(0.2)
    )

    model.add(
        Dense(1)
    )

    model.compile(
        optimizer="adam",
        loss="mse"
    )

    return model


def train_model(data):

    train, val, test = (
        split_data(data)
    )

    X_train, y_train = (
        create_sequences(train)
    )

    X_val, y_val = (
        create_sequences(val)
    )

    X_test, y_test = (
        create_sequences(test)
    )

    model = build_model()

    os.makedirs(
        "models",
        exist_ok=True
    )

    early_stop = EarlyStopping(
        monitor="val_loss",
        patience=10,
        restore_best_weights=True
    )

    checkpoint = ModelCheckpoint(
        MODEL_PATH,
        save_best_only=True,
        monitor="val_loss"
    )

    history = model.fit(
        X_train,
        y_train,
        validation_data=(
            X_val,
            y_val
        ),
        epochs=300,
        batch_size=32,
        callbacks=[
            early_stop,
            checkpoint
        ],
        verbose=1
    )

    return (
        model,
        history,
        X_test,
        y_test
    )


def load_saved_model():

    return tf.keras.models.load_model(
        MODEL_PATH
    )

def forecast_next_30_days(
    model,
    scaler,
    last_revenue,
    scaled_data,
    window_size=30
):

    last_sequence = (
        scaled_data[-window_size:]
    )

    current_sequence = (
        last_sequence.copy()
    )

    future_diffs = []

    for _ in range(30):

        pred = model.predict(
            current_sequence.reshape(
                1,
                window_size,
                1
            ),
            verbose=0
        )

        future_diffs.append(
            pred[0][0]
        )

        current_sequence = np.append(
            current_sequence[1:],
            pred
        ).reshape(
            window_size,
            1
        )

    future_diffs = scaler.inverse_transform(
        np.array(future_diffs)
        .reshape(-1, 1)
    ).flatten()

    future_revenue = (
        np.cumsum(future_diffs)
        + last_revenue
    )

    return future_revenue