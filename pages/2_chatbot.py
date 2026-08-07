import streamlit as st
from groq import Groq
import time

# =====================================
# AUTH CHECK
# =====================================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Silakan login terlebih dahulu")
    st.switch_page("Home.py")

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="🤖 Crypze AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# CUSTOM ULTRA-MODERN CSS
# =====================================
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
    max-width: 1400px;
}

header, footer, #MainMenu { visibility: hidden; }
[data-testid="collapsedControl"] { visibility: visible !important; display: block !important; }

/* MAIN TITLE (GRADASI & TERPUSAT) */
.main-title {
    text-align: center;
    font-size: 44px !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #38bdf8 0%, #22c55e 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0px;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 16px;
    font-weight: 400;
    margin-top: 5px;
    margin-bottom: 30px;
}

/* CHAT MESSAGE CONTAINERS */
[data-testid="stChatMessage"] {
    background: rgba(17, 24, 39, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 16px;
    padding: 15px;
    backdrop-filter: blur(10px);
    margin-bottom: 12px;
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

/* BUTTONS */
.stButton>button {
    width: 100%;
    background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 20px;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
    transition: all 0.3s ease;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(14, 165, 233, 0.5);
    background: linear-gradient(135deg, #1d4ed8 0%, #0284c7 100%);
}

/* INPUTS & SELECTS */
.stSelectbox div[data-baseweb="select"], .stTextInput input {
    background-color: rgba(17, 24, 39, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: white !important;
    border-radius: 12px !important;
}

/* INFO BOX */
.stInfo {
    background-color: rgba(17, 24, 39, 0.8) !important;
    border: 1px solid rgba(56, 189, 248, 0.2) !important;
    border-radius: 14px !important;
    color: #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# GROQ CLIENT
# =====================================
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    client = None

# =====================================
# SIDEBAR
# =====================================
with st.sidebar:
    st.image("Images/crypze_logo.png", use_column_width=True)
    
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

    st.markdown("### ⚙️ Panel Kontrol AI")
    st.success("🟢 GROQ API Connected")

    st.metric("🤖 AI Model", "Llama 3.1", "Instant")
    st.metric("⚡ Provider", "GROQ Cloud")
    st.metric("🪙 Fokus Sesi", "Crypto & AI")
    st.markdown("---")

    quick_questions = [
        "Pilih pertanyaan cepat...",
        "Apa itu Bitcoin?",
        "Apa itu Ethereum?",
        "Apa itu Solana?",
        "Apa itu NFT?",
        "Apa itu DeFi?",
        "Jelaskan blockchain",
        "Jelaskan LSTM",
        "Jelaskan GRU",
        "Apa itu ARIMA?"
    ]

    selected = st.selectbox("💡 Pertanyaan Cepat", quick_questions)

    if selected != "Pilih pertanyaan cepat...":
        if st.button("🚀 Gunakan Pertanyaan Ini"):
            st.session_state.quick_prompt = selected

    st.markdown("---")
    if st.button("🧹 Hapus Riwayat Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Version 3.0 • Universitas Gunadarma")

# =====================================
# HEADER
# =====================================
st.markdown('<div class="main-title">🤖 Crypze AI Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Asisten cerdas analisis pasar & cryptocurrency berbasis Groq Llama 3 🚀</div>', unsafe_allow_html=True)

# =====================================
# SESSION STATE
# =====================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================
# WELCOME MESSAGE
# =====================================
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="welcome-card">
        <h3 style="color: #38bdf8; margin-top:0;">👋 Selamat datang di Crypze AI Assistant!</h3>
        <p style="color: #94a3b8; margin-bottom: 10px;">Anda dapat bertanya seputar topik berikut:</p>
        <ul style="color: #cbd5e1; margin-bottom: 0; line-height: 1.6;">
            <li><b>Aset Utama:</b> Bitcoin (BTC), Ethereum (ETH), Solana (SOL)</li>
            <li><b>Teknologi Web3:</b> NFT, DeFi, Blockchain</li>
            <li><b>Trading & Model AI:</b> Strategi Trading, LSTM, GRU, ARIMA</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# =====================================
# SHOW CHAT HISTORY
# =====================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🤖"):
        st.write(msg["content"])

# =====================================
# INPUT HANDLER
# =====================================
prompt = st.chat_input("Tanya apa saja seputar cryptocurrency atau model AI...")

# QUICK PROMPT OVERRIDE
if "quick_prompt" in st.session_state:
    prompt = st.session_state.quick_prompt
    del st.session_state.quick_prompt

# =====================================
# FILTER TOPIC KEYWORDS
# =====================================
crypto_keywords = [
    "bitcoin", "ethereum", "solana", "crypto", "cryptocurrency",
    "blockchain", "nft", "defi", "trading", "lstm", "gru", "arima",
    "btc", "eth", "sol"
]

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
    "siapa pengembang aplikasi": "CRYPZE AI dikembangkan sebagai aplikasi skripsi berbasis Streamlit untuk prediksi cryptocurrency menggunakan metode LSTM, GRU, dan ARIMA.",
    "pengembang": "CRYPZE AI merupakan aplikasi skripsi yang dibangun menggunakan Python dan Streamlit.",
    "fitur aplikasi": """Fitur utama:\n• Dashboard\n• Prediksi Cryptocurrency\n• Chatbot AI\n• Dokumentasi\n• Riwayat\n• Kemitraan\n• Tentang Kami""",
    "sumber data": "Dataset historis cryptocurrency berasal dari Yahoo Finance.",
    "dari mana sumber data": "Data historis cryptocurrency diambil dari Yahoo Finance.",
    "metode": "Metode yang digunakan adalah LSTM, GRU, dan ARIMA.",
    "berapa aset": "Aplikasi mendukung Bitcoin (BTC), Ethereum (ETH), dan Solana (SOL).",
    "bitcoin": "Bitcoin adalah cryptocurrency pertama di dunia yang menggunakan teknologi blockchain.",
    "ethereum": "Ethereum merupakan blockchain yang mendukung Smart Contract dan aplikasi terdesentralisasi.",
    "solana": "Solana adalah blockchain berkecepatan tinggi dengan biaya transaksi rendah.",
    "blockchain": "Blockchain adalah buku besar digital yang terdistribusi dan diamankan dengan kriptografi.",
    "nft": "NFT adalah aset digital unik yang kepemilikannya dicatat pada blockchain.",
    "defi": "DeFi adalah layanan keuangan terdesentralisasi yang berjalan di atas blockchain.",
    "lstm": "LSTM adalah algoritma Deep Learning yang mampu mempelajari pola data time series jangka panjang.",
    "gru": "GRU adalah pengembangan dari RNN yang lebih sederhana dibanding LSTM namun tetap efektif untuk time series.",
    "arima": "ARIMA merupakan metode statistik untuk melakukan prediksi berdasarkan data historis time series.",
    "yahoo finance": "Yahoo Finance digunakan sebagai sumber data historis cryptocurrency pada aplikasi CRYPZE AI.",
    "dashboard": "Dashboard menampilkan informasi market cryptocurrency dan ringkasan aplikasi.",
    "chatbot": "Chatbot menggunakan model Llama 3.1 melalui API Groq.",
    "prediksi": "Menu Prediksi digunakan untuk melakukan prediksi harga Bitcoin, Ethereum, dan Solana menggunakan metode LSTM, GRU, atau ARIMA."
}

# =====================================
# PROCESS CHAT
# =====================================
if prompt:
    if client is None:
        st.error("❌ API Key Groq belum dikonfigurasi dengan benar di `st.secrets`.")
        st.stop()

    # VALIDASI TOPIK
    if not any(keyword in prompt.lower() for keyword in crypto_keywords):
        reply = "⚠️ Maaf, saya hanya dapat menjawab topik seputar cryptocurrency, blockchain, dan model AI terkait prediksi pasar."
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

    # CEK FAQ LOKAL TERLEBIH DAHULU
    lower = prompt.lower()
    reply = None
    for key, value in faq.items():
        if key in lower:
            reply = value
            break

    # SAVE USER MESSAGE
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.write(prompt)

    # =====================================
    # AI RESPONSE VIA GROQ (JIKA TIDAK ADA DI FAQ)
    # =====================================
    if reply is None:
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🤖 Crypze AI sedang menyusun jawaban..."):
                try:
                    completion = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {
                                "role": "system",
                                "content": """
Kamu adalah CRYPZE AI Assistant.
CRYPZE AI adalah aplikasi berbasis Streamlit untuk melakukan prediksi harga cryptocurrency.
Fitur aplikasi: Dashboard, Prediksi Cryptocurrency, Chatbot AI, Dokumentasi, Riwayat Prediksi, Kemitraan, Tentang Kami.
Cryptocurrency yang didukung: Bitcoin (BTC), Ethereum (ETH), Solana (SOL).
Metode: LSTM, GRU, ARIMA.
Dataset: Yahoo Finance.
Tugasmu: Menjelaskan penggunaan aplikasi, fitur, aset kripto, metode prediksi (LSTM, GRU, ARIMA), blockchain, NFT, dan DeFi.
Jika pertanyaan di luar ruang lingkup aplikasi, jawablah:
"Maaf, saya hanya dapat membantu mengenai aplikasi CRYPZE AI, cryptocurrency, blockchain, serta metode prediksi LSTM, GRU, dan ARIMA."
Jawablah menggunakan Bahasa Indonesia, maksimal 180 kata, dengan format yang rapi.
"""
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.3,
                        max_tokens=350,
                        timeout=10
                    )
                    reply = completion.choices[0].message.content
                except Exception as e:
                    reply = "⚠️ **Peringatan Sistem:** Gagal terhubung ke server AI Groq saat ini. Silakan periksa koneksi internet Anda atau coba beberapa saat lagi."

    # =====================================
    # STREAM EFFECT
    # =====================================
    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        full_text = ""

        for word in reply.split():
            full_text += word + " "
            time.sleep(0.015)
            placeholder.markdown(full_text + "▌")

        placeholder.markdown(full_text)

    # SAVE AI RESPONSE
    st.session_state.messages.append({"role": "assistant", "content": reply})

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