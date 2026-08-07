import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =========================
# AUTH CHECK
# =========================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Silakan login terlebih dahulu")
    st.switch_page("Home.py")

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="📚 Dokumentasi & Riwayat",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="auto"
)

# =========================
# CUSTOM ULTRA-MODERN CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #f8fafc !important;
}

.stApp {
    background: radial-gradient(circle at 10% 10%, rgba(56, 189, 248, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 90%, rgba(34, 197, 94, 0.08) 0%, transparent 40%),
                #07111e;
    color: #f8fafc;
}

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

/* KELAS JUDUL UTAMA (UKURAN BESAR 44px, TERPUSAT & WARNA GRADASI) */
.main-title {
    font-size: 44px !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
    text-align: center;
    background: linear-gradient(135deg, #38bdf8 0%, #22c55e 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
}

.subtitle {
    color: #94a3b8;
    font-size: 16px;
    font-weight: 400;
    text-align: center;
    margin-bottom: 30px;
    line-height: 1.5;
}

h2, h3 {
    color: #f1f5f9 !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px;
}

.stButton>button {
    background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
    transition: all 0.3s ease;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(14, 165, 233, 0.5);
}

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    margin-bottom: 20px;
}

.stTabs [data-baseweb="tab"] {
    background-color: rgba(17, 24, 39, 0.6);
    border-radius: 10px;
    color: #94a3b8;
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 8px 18px;
    font-weight: 600;
    font-size: 14px;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%) !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR (DENGAN LOGO & MENU UTAMA)
# =========================
with st.sidebar:
    st.success("🟢 System Online")

    st.divider()

    st.caption("Version 3.0 • Universitas Gunadarma")

# =========================
# HEADER (TERPUSAT DENGAN Kelas H1)
# =========================
st.markdown('<h1 class="main-title">📚 Dokumentasi & Riwayat Prediksi</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Pusat informasi panduan penggunaan sistem serta arsip riwayat hasil prediksi model AI.</p>', unsafe_allow_html=True)

# =========================
# TABS
# =========================
tabs = st.tabs(["📖 Dokumentasi Sistem", "📊 Log Riwayat Prediksi"])

# =========================
# TAB 1: DOKUMENTASI SISTEM
# =========================
with tabs[0]:
    st.subheader("🚀 Panduan Penggunaan Platform Crypze AI")
    
    with st.container(border=True):
        st.markdown("### 1. 🏠 Beranda (Home Dashboard)")
        st.write("Menampilkan ringkasan pasar cryptocurrency secara realtime (Bitcoin, Ethereum, Solana) yang dilengkapi dengan grafik mini (sparkline) serta pembaruan otomatis setiap 60 detik.")
        
        st.markdown("### 2. 📈 Prediksi AI (AI Prediction)")
        st.write("Pilih aset kripto dan model AI (LSTM, GRU, atau ARIMA) melalui panel kontrol di sidebar untuk melihat metrik evaluasi (R², MAE, RMSE) serta grafik proyeksi harga 5 hari ke depan.")
        
        st.markdown("### 3. 🤖 AI Assistant (Chatbot)")
        st.write("Berinteraksi langsung dengan Llama 3.1 untuk bertanya seputar analisis teknikal, definisi blockchain, tokenomics, hingga cara kerja model deep learning.")

    st.write("")
    st.subheader("🧠 Arsitektur Model Artificial Intelligence")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("#### 🧠 LSTM")
            st.write("Long Short-Term Memory, sangat optimal dalam mempelajari pola ketergantungan data historis jangka panjang pada time-series.")
        
    with col2:
        with st.container(border=True):
            st.markdown("#### ⚡ GRU")
            st.write("Gated Recurrent Unit, varian RNN yang lebih ringan dan cepat dalam proses training dengan performa akurasi tinggi.")
        
    with col3:
        with st.container(border=True):
            st.markdown("#### 📈 ARIMA")
            st.write("Autoregressive Integrated Moving Average, model statistik klasik yang digunakan sebagai pembanding andal.")

# =========================
# TAB 2: LOG RIWAYAT PREDIKSI
# =========================
with tabs[1]:
    st.subheader("📊 Arsip Riwayat Aktivitas & Prediksi")
    st.markdown('<p class="subtitle">Tabel di bawah ini merekam setiap sesi prediksi dan unduhan data yang dilakukan.</p>', unsafe_allow_html=True)

    HISTORY_FILE = "data/history_log.csv"

    if not os.path.exists("data"):
        os.makedirs("data")

    if os.path.exists(HISTORY_FILE):
        df_history = pd.read_csv(HISTORY_FILE)
    else:
        df_history = pd.DataFrame(columns=["Waktu", "Pengguna", "Cryptocurrency", "Model AI", "Status"])

    if not df_history.empty:
        st.dataframe(df_history, use_container_width=True)

        col_dl, col_clr = st.columns([2, 1])
        with col_dl:
            csv_data = df_history.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Unduh Log Riwayat (CSV)",
                data=csv_data,
                file_name="riwayat_prediksi_crypze.csv",
                mime="text/csv"
            )
        with col_clr:
            if st.button("🗑️ Bersihkan Riwayat", use_container_width=True):
                if os.path.exists(HISTORY_FILE):
                    os.remove(HISTORY_FILE)
                st.success("Riwayat berhasil dibersihkan!")
                st.rerun()
    else:
        st.info("ℹ️ Belum ada riwayat prediksi yang tercatat. Silakan lakukan prediksi melalui halaman **AI Prediction**.")

# =========================
# FOOTER
# =========================
st.write("")
st.divider()
st.markdown("""
<p style='text-align: center; color: #64748b; font-size: 13px; margin-top: 20px;'>
    📚 Crypze AI Documentation & History System • Universitas Gunadarma
</p>
""", unsafe_allow_html=True)