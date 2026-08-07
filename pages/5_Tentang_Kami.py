import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================
# AUTH
# =========================================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Silakan login terlebih dahulu")
    st.switch_page("Home.py")

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="📘 Tentang Kami | CRYPZE",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================
# SIDEBAR
# =========================================

with st.sidebar:

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.switch_page("Home.py")


# =========================================
# CUSTOM CSS
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
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
    max-width: 1400px;
}

/* MAIN TITLE */
.main-title {
    font-size: 52px;
    font-weight: 800;
    text-align: center;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #38bdf8 0%, #22c55e 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 10px;
    margin-bottom: 0px;
}

.highlight {
    color: #38bdf8;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 18px;
    font-weight: 400;
    margin-top: 10px;
    margin-bottom: 35px;
}

/* METRIC BOX GLASSMORPHISM */
.metric-box {
    background: rgba(17, 24, 39, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 20px;
    padding: 22px;
    text-align: center;
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
}

.metric-box:hover {
    transform: translateY(-4px);
    border-color: #38bdf8;
    box-shadow: 0 8px 30px rgba(56, 189, 248, 0.15);
}

.metric-box h2 {
    color: #22c55e !important;
    font-size: 32px !important;
    margin-bottom: 0px !important;
    font-weight: 800 !important;
}

.metric-box p {
    color: #94a3b8 !important;
    font-size: 14px !important;
    margin-top: 5px !important;
    margin-bottom: 0px !important;
    font-weight: 500 !important;
}

.footer {
    text-align: center;
    color: #64748b;
    margin-top: 40px;
    font-size: 14px;
}

hr {
    border: 0.5px solid rgba(255, 255, 255, 0.08);
    margin-top: 30px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# HERO SECTION
# =========================================
st.markdown("""
<div class="main-title">
    🚀 Tentang <span class="highlight">CRYPZE AI</span>
</div>
<div class="subtitle">
    Platform Prediksi Cryptocurrency Berbasis Artificial Intelligence
</div>
""", unsafe_allow_html=True)

# =========================================
# METRICS
# =========================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-box">
        <h2>3</h2>
        <p>Cryptocurrency</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-box">
        <h2>3</h2>
        <p>AI Models</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-box">
        <h2>24/7</h2>
        <p>Realtime Prediction</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-box">
        <h2>AI</h2>
        <p>Analytics Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# =========================================
# MAIN CARD (Menggunakan Container Streamlit agar bersih)
# =========================================
with st.container(border=True):
    st.markdown("""
    CRYPZE adalah platform prediksi cryptocurrency modern yang dibangun menggunakan **Artificial Intelligence (AI), Machine Learning**, dan **Time Series Forecasting**.

    Platform ini dirancang untuk membantu pengguna memahami tren pasar cryptocurrency secara lebih cepat, mudah, dan interaktif.

    ### 🪙 Cryptocurrency yang Didukung:
    * ₿ **Bitcoin (BTC)**
    * ⟠ **Ethereum (ETH)**
    * ◎ **Solana (SOL)**
    
    ---
    
    ### 🤖 Teknologi Model AI
    CRYPZE menggunakan kombinasi beberapa model Artificial Intelligence modern:
    * **LSTM (Long Short-Term Memory):** Digunakan untuk mendeteksi pola historis jangka panjang pada harga cryptocurrency.
    * **GRU (Gated Recurrent Unit):** Model neural network ringan dengan performa cepat dan efisien.
    * **ARIMA:** Metode statistik *time-series forecasting* untuk memprediksi tren harga.

    ---

    ### 🚀 Keunggulan Platform
    * ✅ Multi-Cryptocurrency Prediction
    * ✅ Multi-AI Models
    * ✅ Realtime Market Analytics
    * ✅ Interactive Visualization
    * ✅ Modern Dashboard UI
    * ✅ Download Prediction CSV

    ---

    ### 🎯 Visi & Misi CRYPZE
    * **Visi:** Menjadi platform AI cryptocurrency analytics modern yang membantu masyarakat memahami pasar digital secara lebih cerdas, sederhana, dan transparan.
    * **Misi:**
      * 📚 Meningkatkan literasi keuangan digital.
      * 🧠 Menyediakan prediksi berbasis AI dan data historis.
      * ⚡ Mengembangkan dashboard crypto AI yang modern.
      * 📈 Membantu pengguna memahami tren pasar cryptocurrency.

    ---

    ### 🛠️ Teknologi yang Digunakan
    **Python • Streamlit • TensorFlow • Plotly • Pandas • Scikit-Learn • Statsmodels**

    *Terima kasih telah menggunakan CRYPZE 💙 Mari menjelajahi dunia cryptocurrency menggunakan AI dengan lebih cerdas.*
    """)

st.write("")

# ==========================
# AI MODEL PERFORMANCE
# ==========================

st.write("")
st.subheader("📊 Perbandingan Rata-rata Nilai R² Model Prediksi")

st.caption(
    "Nilai yang ditampilkan merupakan rata-rata R² Score hasil pengujian "
    "pada Bitcoin, Ethereum, dan Solana."
)

models = [
    (
        "🧠 LSTM",
        "Deep Learning",
        "Mampu mempelajari pola historis jangka panjang pada data time series cryptocurrency.",
        0.9772,
    ),
    (
        "⚡ GRU",
        "Deep Learning",
        "Memiliki arsitektur yang lebih sederhana sehingga proses komputasi lebih efisien.",
        0.9772,
    ),
    (
        "📈 ARIMA",
        "Statistical",
        "Model statistik sebagai pembanding terhadap metode Deep Learning.",
        -0.2451,
    ),
]

cols = st.columns(3)

for col, (title, tipe, desc, r2) in zip(cols, models):

    with col:

        with st.container(border=True):

            st.markdown(f"## {title}")

            st.caption(tipe)

            st.write(desc)

            progress = max(min(r2, 1), 0)

            st.progress(progress)

            st.metric(
                label="Average R² Score",
                value=f"{r2:.4f}"
            )

            if r2 >= 0.95:
                st.success("🟢 Sangat Baik")

            elif r2 >= 0.75:
                st.info("🔵 Baik")

            elif r2 >= 0:
                st.warning("🟡 Cukup")

            else:
                st.error("🔴 Kurang Baik")

df_r2 = pd.DataFrame({
    "Model": ["LSTM", "GRU", "ARIMA"],
    "Average R²": [0.9772, 0.9772, -0.2451]
})

fig = px.bar(
    df_r2,
    x="Model",
    y="Average R²",
    text="Average R²",
    template="plotly_dark"
)

fig.update_traces(
    texttemplate="%{text:.4f}",
    textposition="outside"
)

fig.update_layout(
    title="Average R² Score Comparison",
    height=450,
    xaxis_title="Model",
    yaxis_title="Average R² Score",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig, use_container_width=True)

# =========================================
# CONTACT SECTION
# =========================================
st.subheader("📬 Hubungi Kami")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("📧 **Email**\n\nsupport@crypze.ai")

with col2:
    st.info("🌐 **Website**\n\nwww.crypze.ai")

with col3:
    st.info("🐙 **GitHub**\n\ngithub.com/crypze-ai")

# =========================================
# FOOTER
# =========================================
st.markdown("""
<hr>
<div class="footer">
    © 2026 CRYPZE AI — Built with Python, Streamlit & TensorFlow 🚀
</div>
""", unsafe_allow_html=True)