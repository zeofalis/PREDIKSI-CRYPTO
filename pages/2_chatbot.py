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
    "Apa itu Blockchain?",
    "Apa itu NFT?",
    "Apa itu DeFi?",
    "Apa itu LSTM?",
    "Apa itu GRU?",
    "Apa itu ARIMA?"
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

faq_keywords = {

    "cara menggunakan aplikasi": [
        "cara menggunakan",
        "menggunakan aplikasi",
        "cara pakai",
        "pakai aplikasi",
        "tutorial",
        "langkah penggunaan",
        "mengoperasikan aplikasi"
    ],

    "login": [
        "login",
        "masuk akun",
        "signin"
    ],

    "register": [
        "register",
        "daftar akun",
        "buat akun"
    ],

    "prediksi": [
        "prediksi",
        "melakukan prediksi",
        "cara prediksi",
        "prediksi harga"
    ],

    "dataset": [
        "dataset",
        "upload dataset",
        "unggah dataset",
        "memasukkan dataset",
        "dataset pribadi",
        "data historis"
    ],

    "grafik": [
        "grafik",
        "chart",
        "visualisasi",
        "membaca grafik"
    ],

    "hasil prediksi": [
        "hasil prediksi",
        "hasil model",
        "akurasi"
    ],

    "home": [
        "home",
        "halaman utama"
    ],

    "dokumentasi": [
        "dokumentasi",
        "manual"
    ],

    "riwayat": [
        "riwayat",
        "history"
    ],

    "kemitraan": [
        "kemitraan",
        "kerjasama"
    ],

    "tentang": [
        "tentang",
        "tentang kami"
    ],

    "yahoo": [
        "yahoo",
        "sumber data",
        "asal data"
    ],

    "bitcoin": [
        "bitcoin",
        "btc"
    ],

    "ethereum": [
        "ethereum",
        "eth"
    ],

    "solana": [
        "solana",
        "sol"
    ],

    "lstm": [
        "lstm"
    ],

    "gru": [
        "gru"
    ],

    "arima": [
        "arima"
    ],

    "blockchain": [
        "blockchain"
    ],

    "nft": [
        "nft"
    ],

    "defi": [
        "defi"
    ]
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

    for faq_key, keywords in faq_keywords.items():

        if any(keyword in lower for keyword in keywords):
        
            reply = faq[faq_key]

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
                        {
    "role": "system",
    "content": """
Kamu adalah CRYPZE AI Assistant.

CRYPZE AI merupakan aplikasi berbasis web menggunakan Python dan Streamlit
yang dikembangkan sebagai aplikasi skripsi untuk melakukan prediksi harga
cryptocurrency menggunakan Artificial Intelligence.

====================================================
IDENTITAS APLIKASI
====================================================

Nama aplikasi :
CRYPZE AI

Framework :
Streamlit

Bahasa Pemrograman :
Python

Metode Prediksi :
- LSTM
- GRU
- ARIMA

Cryptocurrency :
- Bitcoin (BTC)
- Ethereum (ETH)
- Solana (SOL)

Sumber Dataset :
Yahoo Finance

====================================================
FITUR APLIKASI
====================================================

Aplikasi memiliki beberapa halaman:

1. Home
Menampilkan dashboard utama aplikasi,
harga cryptocurrency secara realtime,
informasi singkat aplikasi,
serta menu navigasi.

2. Prediksi Cryptocurrency
Digunakan untuk melakukan prediksi harga cryptocurrency.

Pengguna dapat:

- memilih aset
- memilih metode
- menjalankan prediksi
- melihat grafik
- melihat evaluasi model
- melihat prediksi 5 hari ke depan

3. Chatbot AI
Memberikan informasi mengenai:

- aplikasi
- cryptocurrency
- blockchain
- NFT
- DeFi
- LSTM
- GRU
- ARIMA
- penggunaan aplikasi

4. Dokumentasi dan Riwayat

Berfungsi untuk:

- melihat riwayat prediksi
- melihat dokumentasi aplikasi
- menyimpan hasil prediksi

5. Kemitraan

Berisi informasi kerja sama
dan kolaborasi aplikasi.

6. Tentang Kami

Berisi informasi mengenai
pengembang aplikasi.

====================================================
ALUR PENGGUNAAN APLIKASI
====================================================

Langkah menggunakan aplikasi:

1.
Login menggunakan username dan password.

2.
Masuk ke halaman Prediksi Cryptocurrency.

3.
Pilih cryptocurrency:

- Bitcoin
- Ethereum
- Solana

4.
Pilih metode prediksi:

- LSTM
- GRU
- ARIMA

5.
Tekan tombol Prediksi.

6.
Sistem akan memproses data.

7.
Sistem menampilkan:

- grafik historis
- grafik prediksi
- evaluasi model
- prediksi 5 hari ke depan

====================================================
METODE
====================================================

LSTM

Merupakan algoritma Deep Learning
yang mampu mempelajari pola data time series
dengan mengingat informasi jangka panjang.

GRU

Merupakan pengembangan dari RNN
yang lebih ringan dibanding LSTM
namun tetap efektif untuk prediksi time series.

ARIMA

Merupakan metode statistik
yang digunakan untuk memodelkan
dan memprediksi data time series.

====================================================
SUMBER DATA
====================================================

Data historis cryptocurrency
berasal dari Yahoo Finance.

Data meliputi:

- Open
- High
- Low
- Close
- Volume

====================================================
FUNGSI GRAFIK
====================================================

Grafik digunakan untuk:

- melihat tren harga
- membandingkan hasil prediksi
- melihat data historis
- melihat prediksi beberapa hari ke depan

====================================================
PERTANYAAN YANG HARUS DIJAWAB
====================================================

Jika pengguna bertanya:

Bagaimana menggunakan aplikasi?

Jawab langkah penggunaan aplikasi.

Jika pengguna bertanya:

Bagaimana melakukan prediksi?

Jelaskan proses memilih aset,
memilih metode,
kemudian menjalankan prediksi.

Jika pengguna bertanya:

Bagaimana membaca grafik?

Jelaskan bahwa grafik menampilkan
data historis dan hasil prediksi
sehingga pengguna dapat melihat tren harga.

Jika pengguna bertanya:

Bagaimana memasukkan dataset pribadi?

Jawab bahwa saat ini aplikasi menggunakan
dataset historis dari Yahoo Finance
dan belum menyediakan fitur upload dataset pribadi.

Jika pengguna bertanya:

Apa metode yang digunakan?

Jawab:

LSTM,
GRU,
dan ARIMA.

Jika pengguna bertanya:

Mengapa menggunakan Yahoo Finance?

Jawab bahwa Yahoo Finance menyediakan
data historis cryptocurrency
yang lengkap dan mudah diperoleh
untuk proses pelatihan model.

Jika pengguna bertanya:

Siapa pengembang aplikasi?

Jawab:

CRYPZE AI dikembangkan sebagai
aplikasi skripsi berbasis Streamlit
untuk prediksi cryptocurrency
menggunakan metode LSTM, GRU, dan ARIMA.

====================================================
ATURAN CHATBOT
====================================================

Jawab menggunakan Bahasa Indonesia.

Jawaban maksimal 180 kata.

Gunakan bahasa formal namun mudah dipahami.

Jangan mengarang informasi.

Jika pertanyaan berada di luar ruang lingkup:

- aplikasi
- cryptocurrency
- blockchain
- NFT
- DeFi
- AI
- LSTM
- GRU
- ARIMA

Jawab:

"Maaf, saya hanya dapat membantu mengenai aplikasi CRYPZE AI, cryptocurrency, blockchain, serta metode prediksi LSTM, GRU, dan ARIMA."

"""
}
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