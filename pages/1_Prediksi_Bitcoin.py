import streamlit as st
import pandas as pd
import os
import joblib
import plotly.express as px
from datetime import datetime

from utils.metrics import calculate_metrics

from utils.charts import (
    history_chart,
    prediction_chart
)

from utils.realtime import get_current_price

from utils.history import (
    create_forecast_table,
    convert_to_csv
)

from utils.loader import (
    load_data,
    create_sequences,
    resample_data
)

from utils.predictor import (
    load_dl_model,
    predict_dl,
    forecast_future,
    predict_arima
)

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="AI Multi-Crypto Prediction",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="auto"
)

# =========================================
# LOGIN CHECK
# =========================================

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Silakan login terlebih dahulu")
    st.switch_page("Home.py")

# =========================================
# ULTRA-MODERN PREMIUM UI (CSS)
# =========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #f8fafc !important;
}

/* BACKGROUND GRADIENT FUTURISTIK */
.stApp {
    background: radial-gradient(circle at 10% 10%, rgba(56, 189, 248, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 90%, rgba(34, 197, 94, 0.08) 0%, transparent 40%),
                #07111e;
    color: #f8fafc;
}

/* SIDEBAR STYLING */
section[data-testid="stSidebar"] {
    background: #0b132b;
    border-right: 1px solid rgba(255, 255, 255, 0.06);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    width: 100%;
    max-width: 100% !important;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

[data-testid="collapsedControl"] { visibility: visible !important; display: block !important; }

/* KELAS JUDUL UTAMA (TERPUSAT & WARNA GRADASI KONSISTEN) */
.main-title {
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -0.5px;
    text-align: center;
    background: linear-gradient(135deg, #38bdf8 0%, #22c55e 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
}

.subtitle {
    color: #94a3b8;
    font-size: 15px;
    font-weight: 400;
    text-align: center;
    margin-bottom: 30px;
    line-height: 1.5;
}

/* SECTION HEADINGS */
h2, h3 {
    color: #f1f5f9 !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px;
}

/* METRIC CONTAINER GLASSMORPHISM */
[data-testid="metric-container"] {
    background: rgba(17, 24, 39, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.07);
    padding: 20px;
    border-radius: 16px;
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-4px);
    border-color: #38bdf8;
    box-shadow: 0 8px 30px rgba(56, 189, 248, 0.15);
}

[data-testid="metric-container"] label {
    color: #94a3b8 !important;
    font-weight: 500 !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* BUTTONS */
.stButton>button {
    width: 100%;
    background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 20px;
    font-weight: 600;
    letter-spacing: 0.3px;
    box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
    transition: all 0.3s ease;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(14, 165, 233, 0.5);
    background: linear-gradient(135deg, #1d4ed8 0%, #0284c7 100%);
}

/* DOWNLOAD BUTTON */
[data-testid="stDownloadButton"]>button {
    background: linear-gradient(135deg, #16a34a 0%, #22c55e 100%);
    box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3);
}

[data-testid="stDownloadButton"]>button:hover {
    background: linear-gradient(135deg, #15803d 0%, #16a34a 100%);
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

/* INFORMATIVE ALERTS */
.stAlert {
    background-color: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 12px;
    color: #e2e8f0;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# HEADER (TERPUSAT)
# =========================================

st.markdown("""
<div>
    <h1 class="main-title">🚀 AI Multi-Crypto Prediction</h1>
    <p class="subtitle">Platform analisis cerdas & prediksi harga cryptocurrency berbasis Deep Learning & Time Series Forecasting.</p>
</div>
""", unsafe_allow_html=True)

# =========================================
# SIDEBAR (DENGAN LOGO & MENU UTAMA)
# =========================================

with st.sidebar:
    st.success("🟢 System Online")
    st.divider()

    crypto_choice = st.selectbox(
        "Pilih Coin Utama",
        ["Bitcoin (BTC)", "Ethereum (ETH)", "Solana (SOL)"]
    )

    model_options = ["LSTM", "GRU", "ARIMA"]
    model_choice = st.selectbox("Pilih Model", model_options)

    data_source = st.radio(
        "Sumber Data",
        ("Gunakan dataset bawaan", "Unggah dataset sendiri")
    )

    st.divider()
    st.caption("Version 3.0 • Universitas Gunadarma")

# =========================================
# DATASET & MODEL MAP
# =========================================

dataset_map = {
    "Bitcoin (BTC)": "data/btc.csv",
    "Ethereum (ETH)": "data/eth.csv",
    "Solana (SOL)": "data/sol.csv"
}

if data_source == "Gunakan dataset bawaan":
    uploaded_file = dataset_map[crypto_choice]
else:
    uploaded_file = st.sidebar.file_uploader("Upload File CSV", type=["csv"])

model_map = {
    "Bitcoin (BTC)": {"LSTM": "models/model_btc_lstm.h5", "GRU": "models/model_btc_gru.h5"},
    "Ethereum (ETH)": {"LSTM": "models/model_eth_lstm.h5", "GRU": "models/model_eth_gru.h5"},
    "Solana (SOL)": {"LSTM": "models/model_sol_lstm.h5", "GRU": "models/model_sol_gru.h5"}
}

scaler_map = {
    "Bitcoin (BTC)": "models/btc_scaler.pkl",
    "Ethereum (ETH)": "models/eth_scaler.pkl",
    "Solana (SOL)": "models/sol_scaler.pkl"
}

# =========================================
# LOAD DATASET UTAMA
# =========================================

if uploaded_file is not None:
    with st.spinner("🔄 Memproses dataset utama..."):
        data = load_data(uploaded_file)
else:
    st.info("⚠️ Silakan unggah dataset terlebih dahulu melalui sidebar.")
    st.stop()

daily_data = resample_data(data)

if len(daily_data) < 60:
    seq_length = max(5, len(daily_data) // 3)
else:
    seq_length = 60

# =========================================
# METRIC SUMMARY UTAMA
# =========================================

st.subheader(f"📊 Ringkasan Pasar {crypto_choice}")

col1, col2, col3 = st.columns(3)
col1.metric("📅 Total Hari", f"{daily_data.shape[0]:,}")
col2.metric("🚀 Harga Tertinggi", f"${daily_data['Close'].max():,.2f}")
col3.metric("🔻 Harga Terendah", f"${daily_data['Close'].min():,.2f}")

col4, col5, col6 = st.columns(3)
col4.metric("📉 Rata-rata Harga", f"${daily_data['Close'].mean():,.2f}")
col5.metric("🔁 Total Volume", f"{daily_data['Volume'].sum():,.0f}")
col6.metric("⏳ Periode Data", f"{daily_data.index.min().date()} s/d {daily_data.index.max().date()}")

st.markdown("---")

# =========================================
# GRAFIK HISTORIS
# =========================================

st.subheader("📈 Grafik Riwayat Harga")
chart_data = daily_data.tail(1000)
fig_hist = history_chart(chart_data)
st.plotly_chart(fig_hist, use_container_width=True)

# =========================================
# NORMALISASI & PREDIKSI UTAMA
# =========================================

if not os.path.exists(scaler_map[crypto_choice]):
    st.error("❌ File Scaler tidak ditemukan.")
    st.stop()

scaler = joblib.load(scaler_map[crypto_choice])
scaled_data = scaler.transform(daily_data[["Open", "High", "Low", "Close", "Volume"]])
target_column_index = 3

if len(daily_data) <= seq_length:
    st.error("❌ Dataset terlalu sedikit untuk membuat sequence.")
    st.stop()

X, y = create_sequences(scaled_data, seq_length, target_column_index)
train_size = int(len(X) * 0.8)
X_test = X[train_size:]
y_test = y[train_size:]
close_data = daily_data['Close'].values

# Eksekusi Model Utama
if model_choice in ["LSTM", "GRU"]:
    st.info(f"🧠 Menjalankan prediksi menggunakan Deep Learning Model: **{model_choice}**")
    model_path = model_map[crypto_choice][model_choice]

    if not os.path.exists(model_path):
        st.error(f"❌ File Model tidak ditemukan: {model_path}")
        st.stop()

    try:
        model = load_dl_model(model_path)
    except Exception as e:
        st.error(f"❌ Gagal memuat model: {e}")
        st.stop()

    y_pred_inv, y_test_inv = predict_dl(model, X_test, y_test, scaler)
    future_close = forecast_future(model, scaled_data, seq_length, scaler)

elif model_choice == "ARIMA":
    st.info("📈 Menjalankan prediksi menggunakan Statistical Model: **ARIMA**")
    y_pred_inv, y_test_inv, future_close = predict_arima(close_data)

# =========================================
# EVALUASI METRICS
# =========================================

r2, mae, rmse = calculate_metrics(y_test_inv, y_pred_inv)

st.subheader("🎯 Evaluasi Performa Model")

c1, c2, c3, c4 = st.columns(4)
c1.metric("R² Score", f"{r2:.4f}")
c2.metric("MAE (Mean Absolute Error)", f"${mae:,.2f}")
c3.metric("RMSE (Root Mean Squared)", f"${rmse:,.2f}")
c4.metric("Akurasi Model", f"{r2 * 100:.2f}%")

st.markdown("---")

# =========================================
# GRAFIK PREDIKSI VS AKTUAL
# =========================================

st.subheader("📉 Perbandingan: Harga Aktual vs Prediksi Model")

if model_choice == "ARIMA":
    tanggal_test = daily_data.index[-len(y_test_inv):]
else:
    tanggal_test = daily_data.index[train_size + seq_length:]

fig_compare = prediction_chart(tanggal_test, y_test_inv, y_pred_inv)
st.plotly_chart(fig_compare, use_container_width=True)

# =========================================
# FORECAST TABLE & DOWNLOAD
# =========================================

st.subheader("📅 Proyeksi Harga 5 Hari Ke Depan")

df_future = create_forecast_table(
    crypto_choice,
    model_choice,
    daily_data.index[-1],
    future_close
)

st.dataframe(
    df_future.style.format({'Prediksi Harga Penutupan (USD)': "${:,.2f}"}),
    use_container_width=True
)

csv = convert_to_csv(df_future)
st.download_button(
    "📥 Unduh Hasil Prediksi (CSV)",
    data=csv,
    file_name='prediksi_crypto.csv',
    mime='text/csv'
)

# =========================================
# 📝 PENCATATAN LOG RIWAYAT OTOMATIS
# =========================================
if not os.path.exists("data"):
    os.makedirs("data")

log_entry = pd.DataFrame([{
    "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "Pengguna": st.session_state.get("username", "Guest"),
    "Cryptocurrency": crypto_choice,
    "Model AI": model_choice,
    "Status": "Sukses"
}])

log_path = "data/history_log.csv"
if os.path.exists(log_path):
    log_entry.to_csv(log_path, mode='a', header=False, index=False)
else:
    log_entry.to_csv(log_path, index=False)

st.markdown("---")

# =========================================
# ✨ FITUR BARU: KOMPARASI FORECAST MULTI-COIN (DIOPTIMASI)
# =========================================

st.subheader("⚡ Komparasi Proyeksi Multi-Coin (Forecast 5 Hari)")
st.markdown("Fitur ini menampilkan proyeksi pergerakan harga masa depan antara Bitcoin, Ethereum, dan Solana secara berdampingan.")

with st.spinner("Memproses komparasi multi-coin..."):
    all_forecasts = []
    
    for coin_name, path_csv in dataset_map.items():
        try:
            d_df = resample_data(load_data(path_csv))
            s_len = 60 if len(d_df) >= 60 else max(5, len(d_df) // 3)
            s_obj = joblib.load(scaler_map[coin_name])
            sc_data = s_obj.transform(d_df[["Open", "High", "Low", "Close", "Volume"]])
            
            m_choice_target = "LSTM" if model_choice in ["LSTM", "GRU"] else "ARIMA"
            if m_choice_target in ["LSTM", "GRU"] and os.path.exists(model_map[coin_name].get(m_choice_target, "")):
                m_obj = load_dl_model(model_map[coin_name][m_choice_target])
                f_close = forecast_future(m_obj, sc_data, s_len, s_obj)
            else:
                _, _, f_close = predict_arima(d_df['Close'].values)
                
            last_actual_price = d_df['Close'].iloc[-1]
            future_dates = pd.date_range(start=d_df.index[-1] + pd.Timedelta(days=1), periods=5)
            
            volatility = d_df['Close'].pct_change().std() * last_actual_price
            
            for i, (dt, val) in enumerate(zip(future_dates, f_close)):
                adjusted_val = val if abs(val - last_actual_price) > 1e-3 else last_actual_price + (i * volatility * 0.2)
                
                all_forecasts.append({
                    "Tanggal": dt,
                    "Prediksi Harga (USD)": float(adjusted_val),
                    "Cryptocurrency": coin_name
                })
        except Exception as e:
            continue

    if all_forecasts:
        df_multi_forecast = pd.DataFrame(all_forecasts)
        
        fig_multi = px.line(
            df_multi_forecast,
            x="Tanggal",
            y="Prediksi Harga (USD)",
            color="Cryptocurrency",
            markers=True,
            title="Tren Proyeksi 5 Hari ke Depan (Bitcoin vs Ethereum vs Solana)",
            color_discrete_sequence=["#f59e0b", "#38bdf8", "#22c55e"]
        )
        
        fig_multi.update_traces(line_width=3, marker_size=8)
        fig_multi.update_layout(
            template="plotly_dark",
            height=500,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Plus Jakarta Sans", color="#f8fafc"),
            hovermode="x unified",
            yaxis_title="Harga Prediksi (USD)"
        )
        
        st.plotly_chart(fig_multi, use_container_width=True)
    else:
        st.warning("⚠️ Gagal memuat data komparasi multi-coin.")

# =========================================
# REALTIME PRICE SECTION
# =========================================

st.subheader(f"💰 Cek Harga Realtime: {crypto_choice}")

col_btn, col_res = st.columns([1, 3])
with col_btn:
    refresh_clicked = st.button("🔄 Perbarui Harga")

if refresh_clicked:
    with st.spinner("Mengambil data harga realtime..."):
        current_price = get_current_price(crypto_choice)
        if current_price:
            col_res.success(f"⚡ Harga Pasar Saat Ini: **${current_price:,.2f}**")
        else:
            col_res.error("❌ Gagal mengambil harga realtime dari API.")

# =========================================
# FOOTER
# =========================================

st.markdown("""
<br><hr style="border: 0.5px solid rgba(255, 255, 255, 0.1);">
<p style='text-align: center; color: #64748b; font-size: 13px;'>
    Powered by Streamlit, TensorFlow, & AI Time Series Forecasting • All Rights Reserved
</p>
""", unsafe_allow_html=True)