import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.initializers import Orthogonal


def custom_dense(**kwargs):
    kwargs.pop("quantization_config", None)
    return Dense(**kwargs)


def load_dl_model(model_path):

    model = load_model(
        model_path,
        custom_objects={
            "Dense": custom_dense,
            "Orthogonal": Orthogonal,
        },
        compile=False,
    )

    return model


# =========================================
# ARIMA
# =========================================

def predict_arima(close_data):

    from statsmodels.tsa.arima.model import ARIMA

    train_size_arima = int(len(close_data) * 0.8)

    train_data = np.log(close_data[:train_size_arima])
    test_data = np.log(close_data[train_size_arima:])

    model = ARIMA(
        train_data,
        order=(1, 1, 1)
    )

    model_fit = model.fit()

    y_pred_log = model_fit.forecast(
        steps=len(test_data)
    )

    y_pred_inv = np.exp(y_pred_log)
    y_test_inv = np.exp(test_data)

    future_log = model_fit.forecast(steps=5)
    future_close = np.exp(future_log)

    return y_pred_inv, y_test_inv, future_close


def predict_dl(model, X_test, y_test, scaler):

    y_pred = model.predict(
        X_test,
        verbose=0
    )

    y_pred_inv = scaler.inverse_transform(
        np.concatenate(
            (
                np.zeros((len(y_pred), 3)),
                y_pred,
                np.zeros((len(y_pred), 1))
            ),
            axis=1
        )
    )[:, 3]

    y_test_inv = scaler.inverse_transform(
        np.concatenate(
            (
                np.zeros((len(y_test), 3)),
                y_test.reshape(-1, 1),
                np.zeros((len(y_test), 1))
            ),
            axis=1
        )
    )[:, 3]

    return y_pred_inv, y_test_inv


def forecast_future(model, scaled_data, seq_length, scaler):

    n_future = 5

    last_seq = scaled_data[-seq_length:]
    last_seq = last_seq.reshape(
        (1, seq_length, scaled_data.shape[1])
    )

    future_preds_scaled = []

    for _ in range(n_future):

        pred = model.predict(
            last_seq,
            verbose=0
        )[0]

        future_preds_scaled.append(pred)

        new_step = last_seq[0, -1, :].copy()

        # Close index = 3
        new_step[3] = pred[0]

        last_seq = np.roll(
            last_seq,
            -1,
            axis=1
        )

        last_seq[0, -1, :] = new_step

    future_close = scaler.inverse_transform(
        np.concatenate(
            (
                np.zeros((n_future, 3)),
                np.array(future_preds_scaled)[:, 0:1],
                np.zeros((n_future, 1))
            ),
            axis=1
        )
    )[:, 3]

    return future_close
