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

faq = {

# =========================
# PENGGUNAAN APLIKASI
# =========================

"cara menggunakan aplikasi":
"""Untuk menggunakan aplikasi CRYPZE AI, pengguna terlebih dahulu melakukan login menggunakan akun yang telah terdaftar. Setelah berhasil masuk, buka menu Prediksi Cryptocurrency, pilih aset yang ingin diprediksi, kemudian pilih metode prediksi (LSTM, GRU, atau ARIMA). Selanjutnya tekan tombol Prediksi dan sistem akan menampilkan grafik, evaluasi model, serta hasil prediksi harga cryptocurrency.""",

"login":
"""Pengguna harus melakukan login menggunakan username dan password yang telah didaftarkan. Setelah login berhasil, seluruh fitur aplikasi dapat digunakan.""",

"register":
"""Jika belum memiliki akun, pengguna dapat membuat akun melalui menu Register dengan mengisi username dan password. Setelah akun berhasil dibuat, pengguna dapat login ke aplikasi.""",

"prediksi":
"""Untuk melakukan prediksi harga cryptocurrency, buka menu Prediksi Cryptocurrency. Selanjutnya pilih aset cryptocurrency, tentukan metode prediksi yang diinginkan, lalu tekan tombol Prediksi. Sistem akan memproses data dan menampilkan hasil prediksi beserta grafik visualisasi.""",

"dataset":
"""Dataset historis cryptocurrency berasal dari Yahoo Finance. Pada versi aplikasi ini pengguna menggunakan dataset yang telah disediakan oleh sistem sehingga tidak perlu mengunggah dataset secara manual.""",

"grafik":
"""Grafik menampilkan pergerakan harga cryptocurrency berdasarkan data historis serta hasil prediksi model. Sumbu horizontal menunjukkan waktu, sedangkan sumbu vertikal menunjukkan harga aset. Grafik digunakan untuk membantu pengguna memahami tren harga serta membandingkan hasil prediksi.""",

"hasil prediksi":
"""Hasil prediksi menunjukkan estimasi harga cryptocurrency berdasarkan metode yang dipilih. Selain grafik, sistem juga menampilkan evaluasi model sehingga pengguna dapat membandingkan performa masing-masing metode.""",

# =========================
# MENU
# =========================

"home":
"""Menu Home merupakan halaman utama aplikasi yang menampilkan informasi umum mengenai CRYPZE AI dan fitur-fitur yang tersedia.""",

"dokumentasi":
"""Menu Dokumentasi dan Riwayat digunakan untuk melihat dokumentasi sistem serta riwayat hasil prediksi yang pernah dilakukan pengguna.""",

"riwayat":
"""Riwayat prediksi menyimpan hasil prediksi yang telah dilakukan sehingga pengguna dapat melihat kembali hasil sebelumnya.""",

"kemitraan":
"""Menu Kemitraan berisi informasi mengenai kerja sama, pengembangan aplikasi, serta peluang kolaborasi.""",

"tentang":
"""Menu Tentang Kami berisi informasi mengenai aplikasi CRYPZE AI, tujuan pengembangan, serta teknologi yang digunakan.""",

# =========================
# DATA
# =========================

"yahoo":
"""Seluruh data historis cryptocurrency yang digunakan pada aplikasi ini berasal dari Yahoo Finance. Data tersebut digunakan sebagai dataset untuk proses pelatihan model dan prediksi harga.""",

# =========================
# METODE
# =========================

"lstm":
"""LSTM (Long Short-Term Memory) merupakan algoritma Deep Learning yang dirancang untuk mempelajari pola data time series sehingga sangat cocok digunakan untuk prediksi harga cryptocurrency.""",

"gru":
"""GRU (Gated Recurrent Unit) merupakan pengembangan dari Recurrent Neural Network yang memiliki struktur lebih sederhana dibandingkan LSTM namun tetap mampu menghasilkan prediksi yang akurat.""",

"arima":
"""ARIMA (AutoRegressive Integrated Moving Average) merupakan metode statistik berbasis data time series yang digunakan sebagai pembanding terhadap metode Deep Learning dalam melakukan prediksi harga cryptocurrency.""",

# =========================
# CRYPTO
# =========================

"bitcoin":
"""Bitcoin (BTC) merupakan cryptocurrency pertama yang menggunakan teknologi blockchain. Bitcoin dikembangkan sebagai mata uang digital tanpa perantara dan saat ini menjadi aset kripto dengan kapitalisasi pasar terbesar di dunia.""",

"ethereum":
"""Ethereum (ETH) merupakan platform blockchain yang mendukung Smart Contract dan aplikasi terdesentralisasi (dApps). Ethereum banyak digunakan dalam pengembangan NFT, DeFi, dan berbagai aplikasi Web3.""",

"solana":
"""Solana (SOL) merupakan blockchain berperforma tinggi yang dirancang untuk mendukung transaksi dengan kecepatan tinggi dan biaya rendah. Solana banyak digunakan untuk aplikasi DeFi dan NFT.""",

"blockchain":
"""Blockchain merupakan teknologi penyimpanan data berbentuk rantai blok yang bersifat terdistribusi, transparan, dan sulit dimanipulasi sehingga menjadi dasar dari cryptocurrency.""",

"nft":
"""NFT (Non-Fungible Token) merupakan aset digital unik yang kepemilikannya dicatat menggunakan teknologi blockchain sehingga tidak dapat dipertukarkan secara identik.""",

"defi":
"""DeFi (Decentralized Finance) merupakan layanan keuangan berbasis blockchain yang memungkinkan transaksi dilakukan tanpa perantara seperti bank.""",
"membaca grafik":
"""Grafik digunakan untuk menampilkan perubahan harga cryptocurrency berdasarkan data historis serta hasil prediksi.

Sumbu horizontal menunjukkan waktu.

Sumbu vertikal menunjukkan harga cryptocurrency.

Grafik membantu pengguna melihat tren harga dan membandingkan hasil prediksi.""",

"upload dataset":
"""Saat ini aplikasi menggunakan dataset historis dari Yahoo Finance.

Versi aplikasi ini belum menyediakan fitur upload dataset pribadi.""",

"metode terbaik":
"""Aplikasi menyediakan tiga metode yaitu LSTM, GRU, dan ARIMA.

Pengguna dapat membandingkan hasil evaluasi masing-masing metode sebelum menentukan metode terbaik.""",

"dashboard":
"""Dashboard merupakan halaman utama aplikasi yang menampilkan informasi singkat mengenai aplikasi serta akses menuju seluruh fitur.""",

"riwayat prediksi":
"""Riwayat prediksi digunakan untuk menyimpan hasil prediksi yang telah dilakukan sehingga pengguna dapat melihat kembali hasil sebelumnya.""",
"metode":
"""Aplikasi CRYPZE AI menyediakan tiga metode prediksi yaitu:

1. LSTM (Long Short-Term Memory)
2. GRU (Gated Recurrent Unit)
3. ARIMA (AutoRegressive Integrated Moving Average)

Ketiga metode tersebut dapat dipilih oleh pengguna untuk melakukan prediksi harga cryptocurrency dan membandingkan performanya.""",
"algoritma":
"""Aplikasi menggunakan tiga metode prediksi yaitu LSTM, GRU, dan ARIMA.""",

"model":
"""Model yang tersedia pada aplikasi ini adalah LSTM, GRU, dan ARIMA.""",
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

        keywords = [
            key,
            key.replace("cara ", ""),
            key.replace(" aplikasi", "")
        ]

        if any(k in lower for k in keywords):
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

"bitcoin","btc",

"ethereum","eth",

"solana","sol",

"crypto","cryptocurrency",

"blockchain",

"nft",

"defi",

"lstm",

"gru",

"arima",

"grafik",

"chart",

"dataset",

"csv",

"prediksi",

"dashboard",

"menu",

"home",

"login",

"register",

"riwayat",

"dokumentasi",

"kemitraan",

"tentang",

"fitur",

"chatbot",

"aplikasi",

"yahoo",

"metode",
"digunakan",
"berapa",
"jumlah",
"algoritma",
"model"

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
9. Menjelaskan cara membaca grafik.
10. Menjelaskan cara menggunakan aplikasi.
11. Menjelaskan sumber dataset.
12. Menjelaskan fungsi Dashboard.
13. Menjelaskan fungsi Dokumentasi.
14. Menjelaskan Riwayat Prediksi.
15. Menjelaskan cara memilih metode.
16. Menjelaskan kelebihan LSTM dibanding GRU.
17. Menjelaskan perbedaan ARIMA dan Deep Learning.

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

                temperature=0.5,
                max_tokens=600

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