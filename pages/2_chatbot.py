import streamlit as st
from groq import Groq
import time

# =====================================
# AUTH
# =====================================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Silakan login terlebih dahulu")
    st.switch_page("Home.py")

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="🤖 Crypze AI Assistant",
    page_icon="🚀",
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
    text-align: center;
    font-size: 46px;
    font-weight: 800;
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
    api_key = st.secrets["GROQ_API_KEY"]

    st.success(f"API Key terbaca: {api_key[:10]}...")

    client = Groq(api_key=api_key)

except Exception as e:
    st.error(f"Secrets Error: {e}")
    client = None

# =====================================
# HEADER
# =====================================
st.markdown('<div class="main-title">🤖 Crypze AI Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Asisten cerdas analisis pasar & cryptocurrency berbasis Groq Llama 3 🚀</div>', unsafe_allow_html=True)

# =====================================
# SIDEBAR
# =====================================
with st.sidebar:
    st.markdown("### ⚙️ Panel Kontrol AI")
    st.markdown("---")
    st.success("🟢 GROQ API Connected")

    st.metric("🤖 AI Model", "Llama 3.1", "Instant")
    st.metric("⚡ Provider", "GROQ Cloud")
    st.metric("🪙 Fokus Sesi", "Crypto & AI")
    st.markdown("---")

    quick_questions = [
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

    if st.button("🚀 Gunakan Pertanyaan Ini"):
        st.session_state.quick_prompt = selected

    st.markdown("---")
    if st.button("🧹 Hapus Riwayat Chat"):
        st.session_state.messages = []
        st.rerun()

# =====================================
# SESSION STATE
# =====================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================
# WELCOME MESSAGE
# =====================================
if len(st.session_state.messages) == 0:
    st.info("""
👋 **Selamat datang di Crypze AI Assistant!**

Anda dapat bertanya seputar topik berikut:
* **Aset Utama:** Bitcoin (BTC), Ethereum (ETH), Solana (SOL)
* **Teknologi Web3:** NFT, DeFi, Blockchain
* **Trading & Model AI:** Strategi Trading, LSTM, GRU, ARIMA
""")

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

    # SAVE USER MESSAGE
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.write(prompt)

    # =====================================
    # AI RESPONSE VIA GROQ (DENGAN FALLBACK)
    # =====================================
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🤖 Crypze AI sedang menyusun jawaban..."):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system",
                            "content": """
Kamu adalah Crypze AI Assistant.
Tugas:
- Hanya menjawab tentang cryptocurrency, blockchain, dan model AI prediksi (LSTM, GRU, ARIMA).
- Jawab dengan singkat, padat, jelas, profesional, dan mudah dipahami.
"""
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    timeout=10
                )
                reply = completion.choices[0].message.content
            except Exception as e:
                # Fallback aman jika API Groq gangguan atau kuota habis
                reply = "⚠️ **Peringatan Sistem:** Gagal terhubung ke server AI Groq saat ini. Silakan periksa koneksi internet Anda atau coba beberapa saat lagi."

        # =====================================
        # STREAM EFFECT
        # =====================================
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
<p style='text-align: center; color: #64748b; font-size: 13px;'>
    🚀 Crypze AI Assistant — Powered by GROQ, Streamlit, & Llama 3.1
</p>
""", unsafe_allow_html=True)
