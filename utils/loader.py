import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data(ttl=3600)
def load_data(file):

    df = pd.read_csv(file)

    # Hilangkan nama kolom jika ada
    df.columns.name = None

    # Rapikan nama kolom
    df.columns = [str(c).strip() for c in df.columns]

    # Rename Date -> Timestamp
    if "Date" in df.columns:
        df.rename(columns={"Date": "Timestamp"}, inplace=True)

    # Rename lowercase jika ada
    rename_map = {
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume"
    }

    df.rename(columns=rename_map, inplace=True)

    required = [
        "Timestamp",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume"
    ]

    missing = [c for c in required if c not in df.columns]

    if missing:
        st.error(f"Kolom tidak ditemukan: {missing}")
        st.stop()

    df = df[required]

    # Numeric
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df.dropna(inplace=True)

    # Timestamp
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    df.set_index("Timestamp", inplace=True)

    df.sort_index(inplace=True)

    return df

def create_sequences(
    data,
    seq_length,
    target_idx
):

    X, y = [], []

    for i in range(len(data) - seq_length):

        X.append(
            data[i:i+seq_length]
        )

        y.append(
            data[i+seq_length, target_idx]
        )

    return np.array(X), np.array(y)

def resample_data(data):

    daily_data = data.copy()

    daily_data.sort_index(inplace=True)
    daily_data.dropna(inplace=True)

    if len(daily_data) > 50000:
        daily_data = daily_data.tail(50000)

    return daily_data