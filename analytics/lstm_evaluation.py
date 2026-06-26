import numpy as np

from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error
)


def evaluate_model(
    session,
    X_test,
    y_test,
    scaler,
    prev_revenue=None,
    actual_revenue=None
):

    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    pred = session.run(
        [output_name],
        {
            input_name: X_test.astype(np.float32)
        }
    )[0]

    pred = scaler.inverse_transform(
        pred
    )

    actual_diff = scaler.inverse_transform(
        y_test
    )

    epsilon = 1e-10

    if prev_revenue is not None and actual_revenue is not None:
        revenue_pred = prev_revenue.reshape(-1, 1) + pred
        revenue_pred = revenue_pred.flatten()
        actual_revenue = np.asarray(actual_revenue).flatten()

        mse = mean_squared_error(
            actual_revenue,
            revenue_pred
        )

        rmse = np.sqrt(
            mse
        )

        mae = mean_absolute_error(
            actual_revenue,
            revenue_pred
        )

        mape = np.mean(
            np.abs(
                (actual_revenue - revenue_pred) /
                (np.abs(actual_revenue) + epsilon)
            )
        ) * 100
    else:
        mse = mean_squared_error(
            actual_diff,
            pred
        )

        rmse = np.sqrt(
            mse
        )

        mae = mean_absolute_error(
            actual_diff,
            pred
        )

        mape = np.mean(
            np.abs(
                (actual_diff - pred) /
                (np.abs(actual_diff) + epsilon)
            )
        ) * 100

    return (
        mse,
        rmse,
        mae,
        mape
    )