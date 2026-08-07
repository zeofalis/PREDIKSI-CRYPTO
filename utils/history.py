import pandas as pd


def create_forecast_table(
    crypto_choice,
    model_choice,
    last_date,
    future_close
):

    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=5
    )

    df_future = pd.DataFrame({

        "Crypto": crypto_choice,
        "Model": model_choice,
        "Tanggal": future_dates.strftime("%Y-%m-%d"),
        "Prediksi Harga Penutupan (USD)": future_close

    })

    return df_future


def convert_to_csv(df):

    return df.to_csv(
        index=False
    ).encode("utf-8")