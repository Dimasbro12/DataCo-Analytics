import numpy as np
import onnxruntime as ort
from pathlib import Path

MODEL_PATH = Path("models/revenue_lstm.onnx")
WINDOW_SIZE = 30


def load_saved_model():
    return ort.InferenceSession(
        str(MODEL_PATH),
        providers=["CPUExecutionProvider"]
    )


def forecast_next_30_days(
    session,
    scaler,
    last_revenue,
    scaled_data,
    window_size=WINDOW_SIZE
):

    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    current_sequence = scaled_data[-window_size:].copy()

    future_diffs = []

    for _ in range(30):

        pred = session.run(
            [output_name],
            {
                input_name:
                current_sequence.reshape(
                    1,
                    window_size,
                    1
                ).astype(np.float32)
            }
        )[0]

        future_diffs.append(pred[0][0])

        current_sequence = np.append(
            current_sequence[1:],
            pred
        ).reshape(window_size,1)

    future_diffs = scaler.inverse_transform(
        np.array(future_diffs).reshape(-1,1)
    ).flatten()

    return np.cumsum(future_diffs) + last_revenue