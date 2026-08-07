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
    initial_sidebar_state="expanded"
)

# =====================================
# AUTH
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
# CUSTOM CSS (UI DIPERCANTIK DENGAN GLASSMORPHISM)
# =====================================

st.markdown("""
<style>

.stApp{
    background: radial-gradient(circle at 10% 10%, rgba(56, 189, 248, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 90%, rgba(34, 197, 94, 0.08) 0%, transparent 40%),
                #07111e;
    color: #f8fafc;
}

header, footer, #MainMenu { visibility: hidden; }
[data-testid="collapsedControl"] { visibility: visible !important; display: block !important; }

/* SIDEBAR STYLING */
section[data-testid="stSidebar"] {
    background: #0b132b;
    border-right: 1px solid rgba(255, 255, 255, 0.06);
}

.main-title{
    text-align:center;
    font-size:44px !important;
    font-weight:800 !important;
    background: linear-gradient(135deg, #38bdf8 0%, #22c55e 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
}

.subtitle{
    text-align:center;
    color:#9ca3af;
    font-size:16px;
    margin-bottom:25px;
}

/* CHAT MESSAGE CONTAINERS (GLASSMORPHISM) */
[data-testid="stChatMessage"] {
    background: rgba(17, 24, 39, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 16px;
    padding: 15px;
    backdrop-filter: blur(10px);
    margin-bottom: 12px;
}

/* KARTU WELCOME INFO */
.stInfo {
    background-color: rgba(17, 24, 39, 0.8) !important;
    border: 1px solid rgba(56, 189, 248, 0.2) !important;
    border-radius: 16px !important;
    color: #e2e8f0 !important;
    backdrop-filter: blur(10px);
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
.stSelectbox div[data-baseweb="select"] {
    background-color: rgba(17, 24, 39, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# HEADER
# =====================================

st.markdown(
    "<div class='main-title'>🤖 CRYPZE AI Assistant</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Asisten AI Cryptocurrency Berbasis Llama 3.1</div>",
    unsafe_allow_html=True
)

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:
    st.success("🟢 System Online")
    st.divider()

    st.metric("🪙 Crypto", "3 Aset")
    st.metric("🤖 AI Model", "3 Metode")
    st.metric("⚡ Status", "Realtime")
    st.divider()

    st.caption("Version 3.0 • Universitas Gunadarma")

    st.divider()

    quick_questions = [

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
        "Pertanyaan Cepat",
        quick_questions
    )

    if st.button("Gunakan"):

        st.session_state.quick_prompt = selected

    st.divider()

    if st.button("🧹 Hapus Chat"):

        st.session_state.messages = []

        st.rerun()

# =====================================
# SESSION
# =====================================

if "messages" not in st.session_state:

    st.session_state.messages = []

# =====================================
# WELCOME
# =====================================

if len(st.session_state.messages)==0:

    st.info(
"""
👋 **Selamat datang di CRYPZE AI Assistant.**

Anda dapat bertanya mengenai:

• Cara menggunakan aplikasi

• Bitcoin

• Ethereum

• Solana

• LSTM

• GRU

• ARIMA

• Yahoo Finance

• Blockchain

• NFT

• DeFi

• Prediksi Cryptocurrency
"""
    )

# =====================================
# HISTORY
# =====================================

for msg in st.session_state.messages:

    with st.chat_message(
        msg["role"],
        avatar="🧑" if msg["role"]=="user" else "🤖"
    ):

        st.write(msg["content"])

# =====================================
# INPUT
# =====================================

prompt = st.chat_input(
    "Tulis pertanyaan..."
)

if "quick_prompt" in st.session_state:

    prompt = st.session_state.quick_prompt

    del st.session_state.quick_prompt

# =====================================
# FAQ KNOWLEDGE BASE
# =====================================

faq = {

# =================================================
# PENGGUNAAN APLIKASI
# =================================================

"bagaimana cara menggunakan aplikasi":
"""Langkah penggunaan aplikasi:

1. Login ke aplikasi.
2. Pilih menu Prediksi Cryptocurrency.
3. Pilih aset cryptocurrency (Bitcoin, Ethereum, atau Solana).
4. Pilih metode prediksi (LSTM, GRU, atau ARIMA).
5. Klik tombol Prediksi.
6. Sistem akan menampilkan grafik, evaluasi model, dan hasil prediksi harga.
""",

"cara menggunakan aplikasi":
"""Langkah penggunaan aplikasi:

1. Login.
2. Pilih menu Prediksi Cryptocurrency.
3. Pilih aset.
4. Pilih metode.
5. Klik Prediksi.
6. Lihat hasil prediksi.
""",

"bagaimana cara melakukan prediksi harga":
"""Untuk melakukan prediksi harga:

1. Masuk ke menu Prediksi Cryptocurrency.
2. Pilih aset cryptocurrency.
3. Pilih metode prediksi (LSTM, GRU, atau ARIMA).
4. Tekan tombol Prediksi.
5. Sistem akan memproses data dan menampilkan grafik beserta hasil prediksi harga.
""",

"cara melakukan prediksi":
"""Masuk ke menu Prediksi Cryptocurrency, pilih aset, pilih metode, kemudian klik tombol Prediksi.""" ,

# =================================================
# SUMBER DATA
# =================================================

"dari mana sumber data aplikasi":
"Data historis cryptocurrency pada aplikasi berasal dari Yahoo Finance.",

"sumber data":
"Dataset historis cryptocurrency diperoleh dari Yahoo Finance.",

"yahoo finance":
"Yahoo Finance digunakan sebagai sumber data historis cryptocurrency pada aplikasi.",

# =================================================
# METODE
# =================================================

"apa metode yang digunakan":
"Aplikasi menggunakan tiga metode prediksi yaitu LSTM, GRU, dan ARIMA.",

"metode":
"Metode prediksi yang tersedia yaitu LSTM, GRU, dan ARIMA.",

"lstm":
"LSTM merupakan algoritma Deep Learning yang mampu mempelajari pola data time series jangka panjang.",

"gru":
"GRU merupakan pengembangan dari Recurrent Neural Network (RNN) yang lebih sederhana dibandingkan LSTM.",

"arima":
"ARIMA merupakan metode statistik untuk melakukan prediksi berdasarkan data historis time series.",

# =================================================
# ASET
# =================================================

"bitcoin":
"Bitcoin merupakan cryptocurrency pertama yang menggunakan teknologi blockchain.",

"ethereum":
"Ethereum merupakan platform blockchain yang mendukung Smart Contract.",

"solana":
"Solana merupakan blockchain dengan kecepatan transaksi tinggi dan biaya rendah.",

"aset":
"Aplikasi mendukung tiga aset cryptocurrency yaitu Bitcoin (BTC), Ethereum (ETH), dan Solana (SOL).",

# =================================================
# PENGEMBANG
# =================================================

"siapa pengembang aplikasi":
"CRYPZE AI dikembangkan sebagai aplikasi skripsi berbasis Streamlit untuk melakukan prediksi cryptocurrency menggunakan metode LSTM, GRU, dan ARIMA.",

"pengembang":
"CRYPZE AI merupakan aplikasi skripsi yang dikembangkan menggunakan Python dan Streamlit.",

# =================================================
# MENU
# =================================================

"fitur":
"""Menu pada aplikasi terdiri dari:

• Home
• Prediksi Cryptocurrency
• Chatbot AI
• Dokumentasi dan Riwayat
• Kemitraan
• Tentang Kami
""",

"dashboard":
"Dashboard menampilkan informasi market cryptocurrency secara realtime.",

"chatbot":
"Chatbot menggunakan model Llama 3.1 melalui API Groq.",

"prediksi":
"Menu Prediksi digunakan untuk melakukan prediksi harga Bitcoin, Ethereum, dan Solana menggunakan metode LSTM, GRU, atau ARIMA."
}

# =====================================
# PROCESS CHAT
# =====================================

if prompt:

    if client is None:
        st.error("❌ API Key Groq belum tersedia.")
        st.stop()

    lower = prompt.lower()

    reply = None

    # ===========================
    # FAQ
    # ===========================

    for key, value in faq.items():
        if key.lower() in lower:
            reply = value
            break

    # ===========================
    # SIMPAN USER CHAT
    # ===========================

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message(
        "user",
        avatar="🧑"
    ):
        st.write(prompt)

    if reply is None:

        allowed = [
            "bitcoin","ethereum","solana",
            "crypto","cryptocurrency",
            "blockchain","nft","defi",
            "lstm","gru","arima",
            "prediksi","aplikasi",
            "dashboard","chatbot",
            "pengembang","yahoo",
            "menu","fitur"
        ]

    if not any(x in lower for x in allowed):
        reply = (
            "Maaf, saya hanya dapat membantu mengenai aplikasi CRYPZE AI, "
            "cryptocurrency, blockchain, serta metode prediksi LSTM, GRU, dan ARIMA."
        )
    # ===========================
    # GROQ
    # ===========================

    if reply is None:

        try:

            completion = client.chat.completions.create(

                model="llama-3.1-8b-instant",

                messages=[

                    {
                        "role":"system",

                        "content":"""
Kamu adalah CRYPZE AI Assistant.

CRYPZE AI adalah aplikasi berbasis Streamlit untuk melakukan prediksi harga cryptocurrency.

Fitur aplikasi:

1. Dashboard
2. Prediksi Cryptocurrency
3. Chatbot AI
4. Dokumentasi
5. Riwayat Prediksi
6. Kemitraan
7. Tentang Kami

Cryptocurrency yang didukung:

• Bitcoin (BTC)
• Ethereum (ETH)
• Solana (SOL)

Metode:

• LSTM
• GRU
• ARIMA

Dataset:

• Yahoo Finance

Tugasmu:

1. Menjelaskan penggunaan aplikasi.
2. Menjelaskan fitur aplikasi.
3. Menjelaskan cryptocurrency.
4. Menjelaskan LSTM, GRU, ARIMA.
5. Menjelaskan blockchain.
6. Menjelaskan NFT.
7. Menjelaskan DeFi.
8. Menjawab pertanyaan mengenai aplikasi.

Jika pertanyaan di luar ruang lingkup aplikasi,
jawablah:

"Maaf, saya hanya dapat membantu mengenai aplikasi CRYPZE AI, cryptocurrency, blockchain, serta metode prediksi LSTM, GRU, dan ARIMA."

Jawablah menggunakan Bahasa Indonesia.

Jawaban maksimal 180 kata.

Gunakan format yang rapi.
"""
                    },

                    {
                        "role":"user",
                        "content":prompt
                    }

                ],

                temperature=0.3,
                max_tokens=350

            )

            reply = completion.choices[0].message.content

        except Exception:

            reply = "⚠️ Maaf, server AI Groq sedang tidak dapat dihubungi."

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

    # =====================================
    # SIMPAN JAWABAN AI
    # =====================================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply
        }
    )

# =====================================
# FOOTER
# =====================================

st.divider()

st.markdown(
    """
<div style="
text-align:center;
padding:15px;
color:#94a3b8;
font-size:14px;
">

<b>🤖 CRYPZE AI Assistant</b><br>

Powered by
<b>Groq</b> •
<b>Llama 3.1</b> •
<b>Streamlit</b>

<br><br>

© 2026 CRYPZE AI

</div>
""",
unsafe_allow_html=True
)