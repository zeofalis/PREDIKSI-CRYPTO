import streamlit as st
from groq import Groq
import time

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="🤖 Crypze AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="auto"
)

# =====================================
# AUTH CHECK
# =====================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("Silakan login terlebih dahulu.")
    st.switch_page("Home.py")
    st.stop()

# =====================================
# GROQ CLIENT
# =====================================
client = None
try:
    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )
except Exception:
    client = None

# =====================================
# ULTRA-MODERN DARK GLASSMORPHISM CSS
# =====================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #f8fafc !important;
}

/* BACKGROUND FUTURISTIK */
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

header, footer, #MainMenu { visibility: hidden; }
[data-testid="collapsedControl"] { visibility: visible !important; display: block !important; }

/* JUDUL UTAMA (TERPUSAT & GRADASI KONSISTEN) */
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

/* KARTU SAMBUTAN GLASSMORPHISM */
.welcome-card {
    background: rgba(17, 24, 39, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 24px 28px;
    border-radius: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    margin-bottom: 25px;
}

/* TOMBOL UTAMA */
.stButton>button {
    width: 100%;
    background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 16px;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
    transition: all 0.3s ease;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(14, 165, 233, 0.5);
    background: linear-gradient(135deg, #1d4ed8 0%, #0284c7 100%);
}

/* SELECTBOX & INPUT STYLING */
.stSelectbox div[data-baseweb="select"], .stTextInput input {
    background-color: rgba(17, 24, 39, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# SIDEBAR
# =====================================
with st.sidebar:
    st.image("images/crypze_logo.png", use_container_width=True)
    
    st.success("🟢 System Online")
    st.divider()

    st.markdown("### 📂 Menu Utama")
    st.page_link("Home.py", label="🏠 Home Dashboard")
    st.page_link("pages/1_Prediksi_Bitcoin.py", label="📈 AI Prediction")
    st.page_link("pages/kemitraan.py", label="🤝 Kemitraan Kripto")
    st.page_link("pages/dokumentasi.py", label="📖 Dokumentasi & Riwayat")
    st.page_link("pages/tentang_kami.py", label="👥 Tentang Kami")
    st.page_link("pages/chatbot.py", label="🤖 AI Assistant")
    st.divider()

    st.markdown("### ⚙️ Panel AI")
    st.metric("Model AI", "Llama 3.1")
    st.metric("Provider", "Groq")
    
    st.divider()

    quick_questions = [
        "Pilih pertanyaan cepat...",
        "Apa itu Bitcoin?",
        "Apa itu Ethereum?",
        "Apa itu Solana?",
        "Apa itu LSTM?",
        "Apa itu GRU?",
        "Apa itu ARIMA?",
        "Bagaimana cara menggunakan aplikasi?",
        "Dari mana sumber data aplikasi?",
        "Apa metode yang digunakan?",
        "Siapa pengembang aplikasi?"
    ]

    selected = st.selectbox(
        "💡 Topik Pertanyaan Cepat",
        quick_questions
    )

    if selected != "Pilih pertanyaan cepat...":
        if st.button("🚀 Gunakan Pertanyaan"):
            st.session_state.quick_prompt = selected

    st.divider()

    if st.button("🧹 Bersihkan Riwayat Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Version 3.0 • Universitas Gunadarma")

# =====================================
# HEADER
# =====================================
st.markdown('<h1 class="main-title">🤖 Crypze AI Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Asisten cerdas analisis pasar & cryptocurrency berbasis Llama 3.1 🚀</p>', unsafe_allow_html=True)

# =====================================
# SESSION STATE
# =====================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================
# WELCOME CARD (JIKA BELUM ADA CHAT)
# =====================================
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="welcome-card">
        <h3 style="color: #38bdf8; margin-top:0;">👋 Selamat datang di Crypze AI Assistant!</h3>
        <p style="color: #94a3b8; margin-bottom: 10px;">Anda dapat bertanya mengenai berbagai topik seputar platform dan ekosistem aset digital:</p>
        <ul style="color: #cbd5e1; margin-bottom: 0; line-height: 1.6;">
            <li><b>Panduan Aplikasi:</b> Cara penggunaan, fitur utama, dan sumber data (Yahoo Finance)</li>
            <li><b>Aset Kripto:</b> Bitcoin (BTC), Ethereum (ETH), Solana (SOL), Blockchain, NFT, DeFi</li>
            <li><b>Model AI & Statistik:</b> Arsitektur LSTM, GRU, dan model time-series ARIMA</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# =====================================
# HISTORY DISPLAY
# =====================================
for msg in st.session_state.messages:
    with st.chat_message(
        msg["role"],
        avatar="🧑" if msg["role"] == "user" else "🤖"
    ):
        st.write(msg["content"])

# =====================================
# INPUT HANDLING
# =====================================
prompt = st.chat_input("Tulis pertanyaan Anda di sini...")

if "quick_prompt" in st.session_state:
    prompt = st.session_state.quick_prompt
    del st.session_state.quick_prompt

# =====================================
# FAQ KNOWLEDGE BASE
# =====================================
faq = {
    "bagaimana cara menggunakan aplikasi": """Langkah penggunaan aplikasi:
1. Login ke aplikasi.
2. Masuk ke menu Prediksi Cryptocurrency.
3. Pilih aset (Bitcoin, Ethereum, atau Solana).
4. Pilih metode (LSTM, GRU, atau ARIMA).
5. Klik tombol Prediksi.
6. Lihat hasil prediksi beserta grafik.
""",
    "cara menggunakan aplikasi": "Login → Pilih menu Prediksi → Pilih aset → Pilih metode → Klik Prediksi → Lihat hasil.",
    "siapa pengembang aplikasi": "CRYPZE AI dikembangkan sebagai aplikasi berbasis Streamlit untuk prediksi cryptocurrency menggunakan metode LSTM, GRU, dan ARIMA.",
    "pengembang": "CRYPZE AI merupakan aplikasi yang dibangun menggunakan Python dan Streamlit untuk kebutuhan analisis akademik.",
    "fitur aplikasi": """Fitur utama:\n• Dashboard\n• Prediksi Cryptocurrency\n• Chatbot AI\n• Dokumentasi & Riwayat\n• Kemitraan Kripto\n• Tentang Kami""",
    "sumber data": "Dataset historis cryptocurrency pada aplikasi ini berasal dari Yahoo Finance.",
    "dari mana sumber data": "Data historis cryptocurrency diambil langsung dari Yahoo Finance.",
    "metode": "Metode prediksi yang digunakan adalah Deep Learning (LSTM, GRU) dan statistik time-series (ARIMA).",
    "berapa aset": "Aplikasi mendukung tiga aset utama: Bitcoin (BTC), Ethereum (ETH), dan Solana (SOL).",
    "bitcoin": "Bitcoin adalah cryptocurrency pertama di dunia yang menggunakan teknologi desentralisasi blockchain.",
    "ethereum": "Ethereum merupakan jaringan blockchain yang mendukung Smart Contract dan aplikasi terdesentralisasi (DApps).",
    "solana": "Solana adalah blockchain berkecepatan tinggi dengan latensi rendah dan biaya transaksi yang sangat murah.",
    "blockchain": "Blockchain adalah buku besar digital terdistribusi yang aman dan transparan menggunakan kriptografi.",
    "nft": "NFT adalah aset digital unik yang kepemilikannya diverifikasi dan dicatat di atas blockchain.",
    "defi": "DeFi (Decentralized Finance) adalah layanan keuangan yang berjalan di atas blockchain tanpa perantara institusi.",
    "lstm": "LSTM adalah arsitektur Deep Learning (RNN) yang sangat optimal dalam mempelajari pola jangka panjang pada data time-series.",
    "gru": "GRU adalah pengembangan dari RNN yang memiliki struktur lebih sederhana dibanding LSTM namun tetap sangat efektif.",
    "arima": "ARIMA adalah metode statistik klasik yang digunakan untuk melakukan peramalan data deret waktu (time series).",
    "yahoo finance": "Yahoo Finance digunakan sebagai sumber data historis pasar cryptocurrency pada aplikasi CRYPZE AI.",
    "dashboard": "Dashboard menampilkan informasi pasar secara realtime beserta ringkasan tren aset kripto.",
    "chatbot": "Chatbot ini didukung oleh model Llama 3.1 melalui API Groq untuk menjawab pertanyaan seputar sistem.",
    "prediksi": "Menu Prediksi digunakan untuk memproyeksikan harga aset kripto ke depan menggunakan model kecerdasan buatan."
}

# =====================================
# PROCESS CHAT
# =====================================
if prompt:
    if client is None:
        st.error("❌ API Key Groq belum tersedia di `st.secrets`.")
        st.stop()

    lower = prompt.lower()
    reply = None

    for key, value in faq.items():
        if key in lower:
            reply = value
            break

    # Simpan pesan pengguna
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user", avatar="🧑"):
        st.write(prompt)

    # Ambil dari Groq jika tidak ada di FAQ lokal
    if reply is None:
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": """
Kamu adalah CRYPZE AI Assistant.
CRYPZE AI adalah aplikasi berbasis Streamlit untuk melakukan prediksi harga cryptocurrency.
Fitur aplikasi: Dashboard, Prediksi Cryptocurrency, Chatbot AI, Dokumentasi & Riwayat, Kemitraan Kripto, Tentang Kami.
Cryptocurrency yang didukung: Bitcoin (BTC), Ethereum (ETH), Solana (SOL).
Metode: LSTM, GRU, ARIMA.
Dataset: Yahoo Finance.
Tugasmu: Menjelaskan penggunaan aplikasi, fitur, aset kripto, metode prediksi (LSTM, GRU, ARIMA), blockchain, NFT, dan DeFi.
Jika pertanyaan di luar ruang lingkup aplikasi, jawablah:
"Maaf, saya hanya dapat membantu mengenai aplikasi CRYPZE AI, cryptocurrency, blockchain, serta metode prediksi LSTM, GRU, dan ARIMA."
Jawablah menggunakan Bahasa Indonesia yang ramah, profesional, dan maksimal 180 kata.
"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=350
            )
            reply = completion.choices[0].message.content
        except Exception:
            reply = "⚠️ Maaf, server AI Groq sedang tidak dapat dihubungi saat ini."

    # Efek Stream teks pada jawaban AI
    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        full_text = ""
        for word in reply.split():
            full_text += word + " "
            time.sleep(0.015)
            placeholder.markdown(full_text + "▌")
        placeholder.markdown(full_text)

    # Simpan respon AI
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

# =====================================
# FOOTER
# =====================================
st.write("")
st.divider()

st.markdown("""
<div style="text-align: center; padding: 15px; color: #94a3b8; font-size: 13px;">
    <b>🤖 CRYPZE AI Assistant</b><br>
    Powered by <b>Groq</b> • <b>Llama 3.1</b> • <b>Streamlit</b>
    <br><br>
    © 2026 CRYPZE AI • Universitas Gunadarma
</div>
""", unsafe_allow_html=True)