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
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

.stApp{
    background:#07111e;
}

.main-title{
    text-align:center;
    font-size:46px;
    font-weight:bold;
    color:white;
}

.subtitle{
    text-align:center;
    color:#9ca3af;
    margin-bottom:25px;
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

    st.title("⚙️ Panel AI")

    st.success("🟢 Online")

    st.metric(
        "Model",
        "Llama 3.1"
    )

    st.metric(
        "Provider",
        "Groq"
    )

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
👋 Selamat datang di CRYPZE AI Assistant.

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

    # ===========================
    # APLIKASI
    # ===========================

    "bagaimana cara menggunakan aplikasi":
    """Langkah penggunaan aplikasi:

1. Login ke aplikasi.
2. Masuk ke menu Prediksi Cryptocurrency.
3. Pilih aset (Bitcoin, Ethereum, atau Solana).
4. Pilih metode (LSTM, GRU, atau ARIMA).
5. Klik tombol Prediksi.
6. Lihat hasil prediksi beserta grafik.
""",

    "cara menggunakan aplikasi":
    """Login → Pilih menu Prediksi → Pilih aset → Pilih metode → Klik Prediksi → Lihat hasil.""",

    "siapa pengembang aplikasi":
    "CRYPZE AI dikembangkan sebagai aplikasi skripsi berbasis Streamlit untuk prediksi cryptocurrency menggunakan metode LSTM, GRU, dan ARIMA.",

    "pengembang":
    "CRYPZE AI merupakan aplikasi skripsi yang dibangun menggunakan Python dan Streamlit.",

    "fitur aplikasi":
    """Fitur utama:

• Dashboard
• Prediksi Cryptocurrency
• Chatbot AI
• Dokumentasi
• Riwayat
• Kemitraan
• Tentang Kami
""",

    "sumber data":
    "Dataset historis cryptocurrency berasal dari Yahoo Finance.",

    "dari mana sumber data":
    "Data historis cryptocurrency diambil dari Yahoo Finance.",

    "metode":
    "Metode yang digunakan adalah LSTM, GRU, dan ARIMA.",

    "berapa aset":
    "Aplikasi mendukung Bitcoin (BTC), Ethereum (ETH), dan Solana (SOL).",

    "bitcoin":
    "Bitcoin adalah cryptocurrency pertama di dunia yang menggunakan teknologi blockchain.",

    "ethereum":
    "Ethereum merupakan blockchain yang mendukung Smart Contract dan aplikasi terdesentralisasi.",

    "solana":
    "Solana adalah blockchain berkecepatan tinggi dengan biaya transaksi rendah.",

    "blockchain":
    "Blockchain adalah buku besar digital yang terdistribusi dan diamankan dengan kriptografi.",

    "nft":
    "NFT adalah aset digital unik yang kepemilikannya dicatat pada blockchain.",

    "defi":
    "DeFi adalah layanan keuangan terdesentralisasi yang berjalan di atas blockchain.",

    "lstm":
    "LSTM adalah algoritma Deep Learning yang mampu mempelajari pola data time series jangka panjang.",

    "gru":
    "GRU adalah pengembangan dari RNN yang lebih sederhana dibanding LSTM namun tetap efektif untuk time series.",

    "arima":
    "ARIMA merupakan metode statistik untuk melakukan prediksi berdasarkan data historis time series.",

    "yahoo finance":
    "Yahoo Finance digunakan sebagai sumber data historis cryptocurrency pada aplikasi CRYPZE AI.",

    "dashboard":
    "Dashboard menampilkan informasi market cryptocurrency dan ringkasan aplikasi.",

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

        if key in lower:

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