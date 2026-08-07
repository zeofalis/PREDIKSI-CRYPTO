import streamlit as st
import pandas as pd
import plotly.express as px
from auth import login_user, register_user

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(
    page_title="CRYPZE AI",
    page_icon="images/crypze_logo.png",
    layout="wide",
    initial_sidebar_state="auto",
)

# ==========================
# SESSION STATE
# ==========================
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("username", "")

# ==========================
# LOAD DATA
# ==========================
@st.cache_data
def load_market():
    try:
        btc = pd.read_csv("data/btc.csv")
        eth = pd.read_csv("data/eth.csv")
        sol = pd.read_csv("data/sol.csv")
    except FileNotFoundError as e:
        st.error(f"Gagal memuat data pasar: {e}")
        st.stop()

    for df in (btc, eth, sol):
        df["Date"] = pd.to_datetime(df["Date"])
        df.sort_values("Date", inplace=True)

    return btc, eth, sol

btc, eth, sol = load_market()

def get_change(df):
    last = df.iloc[-1]["Close"]
    prev = df.iloc[-2]["Close"]
    change = ((last - prev) / prev) * 100
    return last, change

btc_price, btc_change = get_change(btc)
eth_price, eth_change = get_change(eth)
sol_price, sol_change = get_change(sol)

# ==========================
# SIDEBAR (DENGAN LOGO KEMBALI)
# ==========================
with st.sidebar:
    st.success("🟢 System Online")
    st.divider()

    st.metric("🪙 Crypto", "3 Aset")
    st.metric("🤖 AI Model", "3 Metode")
    st.metric("⚡ Status", "Realtime")
    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True,
        key="sidebar_logout"
    ):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    st.caption("Version 3.0 • Universitas Gunadarma")

# ==========================
# STYLING (ULTRA-MODERN DARK GLASSMORPHISM)
# ==========================
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

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

[data-testid="collapsedControl"] { visibility: visible !important; display: block !important; }

/* SIDEBAR MODERN STYLING */
section[data-testid="stSidebar"] {
    background: #0b132b;
    border-right: 1px solid rgba(255, 255, 255, 0.06);
}

section[data-testid="stSidebar"] .stMetric {
    background: rgba(17, 24, 39, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 8px;
}

section[data-testid="stSidebar"] [data-testid="stPageLink"] a {
    background-color: rgba(17, 24, 39, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-radius: 12px !important;
    color: #cbd5e1 !important;
    font-weight: 600 !important;
    padding: 10px 15px !important;
    margin-bottom: 8px !important;
    transition: all 0.3s ease !important;
}

section[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {
    background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%) !important;
    color: #ffffff !important;
    border-color: #38bdf8 !important;
    transform: translateX(4px);
    box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
}

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

.card {
    background: rgba(17, 24, 39, 0.7);
    border-radius: 18px;
    padding: 22px;
    border: 1px solid rgba(255, 255, 255, 0.07);
    backdrop-filter: blur(12px);
    transition: 0.25s;
    height: 100%;
}

.card:hover {
    transform: translateY(-6px);
    border-color: #38bdf8;
    box-shadow: 0 12px 30px rgba(56, 189, 248, 0.15);
}

.footer {
    text-align: center;
    color: #64748b;
    padding: 30px;
}

h2, h3 {
    color: #f1f5f9 !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# HERO SECTION (DISELARASKAN)
# ==========================
st.markdown("""
<div style="text-align: center; padding: 20px 0 20px 0;">
    <h1 class="main-title">🚀 CRYPZE AI</h1>
    <p class="subtitle">
        Artificial Intelligence Cryptocurrency Prediction Platform<br>
        Platform prediksi cryptocurrency berbasis Artificial Intelligence menggunakan arsitektur LSTM, GRU, dan ARIMA.
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ==========================================
# REALTIME AUTO-REFRESH FRAGMENT
# ==========================================
@st.fragment(run_every=60)
def render_live_market():
    btc_price, btc_change = get_change(btc)
    eth_price, eth_change = get_change(eth)
    sol_price, sol_change = get_change(sol)

    a, b, c, d = st.columns(4)
    a.metric("₿ Bitcoin", f"${btc_price:,.2f}", f"{btc_change:.2f}%")
    b.metric("⟠ Ethereum", f"${eth_price:,.2f}", f"{eth_change:.2f}%")
    c.metric("◎ Solana", f"${sol_price:,.2f}", f"{sol_change:.2f}%")
    d.metric("🤖 AI Model", "3", "LSTM • GRU • ARIMA")

    st.write("")
    st.subheader("📊 Live Market Dashboard")

    def sparkline(df, color):
        fig = px.area(df.tail(30), x="Date", y="Close", template="plotly_dark")
        fig.update_traces(line_color=color, fillcolor=color, opacity=0.15, line_width=2)
        fig.update_layout(
            height=70,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_visible=False,
            yaxis_visible=False,
            showlegend=False,
        )
        return fig

    def market_card(col, title, symbol, df, price, change):
        color = "#22c55e" if change >= 0 else "#ef4444"
        arrow = "▲" if change >= 0 else "▼"

        with col:
            with st.container(border=False):
                st.markdown(f"""
                <div class="card">
                    <h2>{symbol} {title}</h2>
                    <h1 style="margin-bottom:0">${price:,.2f}</h1>
                    <h3 style="color:{color}; margin-top:5px;">{arrow} {change:.2f}%</h3>
                </div>
                """, unsafe_allow_html=True)
                st.plotly_chart(sparkline(df, color), use_container_width=True, config={"displayModeBar": False})

    c1, c2, c3 = st.columns(3)
    market_card(c1, "Bitcoin", "₿", btc, btc_price, btc_change)
    market_card(c2, "Ethereum", "⟠", eth, eth_price, eth_change)
    market_card(c3, "Solana", "◎", sol, sol_price, sol_change)

render_live_market()

st.write("")

# ==========================
# LOGIN / REGISTER SECTION
# ==========================
left, center, right = st.columns([1.5, 2, 1.5])

with center:
    if not st.session_state.logged_in:
        st.subheader("🔐 Autentikasi Pengguna")
        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            username = st.text_input("Username", key="login_user_input")
            password = st.text_input("Password", type="password", key="login_pass_input")

            if st.button("🚀 Login", use_container_width=True):
                if not username or not password:
                    st.warning("Username dan Password wajib diisi.")
                elif login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login berhasil.")
                    st.rerun()
                else:
                    st.error("Username atau Password salah.")

        with tab2:
            new_user = st.text_input("Username Baru", key="reg_user_input")
            new_pass = st.text_input("Password Baru", type="password", key="reg_pass_input")

            if st.button("📝 Register", use_container_width=True):
                if not new_user or not new_pass:
                    st.warning("Username dan Password wajib diisi.")
                elif register_user(new_user, new_pass):
                    st.success("Akun berhasil dibuat. Silakan login.")
                else:
                    st.error("Username sudah digunakan.")
    else:
        st.success(
            f"👋 Selamat datang kembali, **{st.session_state.username}**!"
    )                
    

st.divider()

# ==========================
# CHART + AI INFO
# ==========================
left, right = st.columns([3, 1])

with left:
    st.subheader("📈 Bitcoin Price History")
    fig = px.line(btc.tail(365), x="Date", y="Close", template="plotly_dark")
    fig.update_traces(line_width=3, line_color="#38bdf8")
    fig.update_layout(
        height=650,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="",
        yaxis_title="Price (USD)",
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"Data terakhir: {btc['Date'].max().strftime('%d %B %Y')}")

with right:
    st.subheader("🤖 AI Information")
    st.info("🧠 **Model**\n\nLSTM • GRU • ARIMA")
    st.info("📂 **Dataset**\n\nBitcoin • Ethereum • Solana")
    st.info("🎯 **Prediction**\n\n5 Hari ke depan")
    st.info("⚙️ **Framework**\n\nTensorFlow • Streamlit • Plotly")
    st.info("🎓 **Project**\n\nUniversitas Gunadarma")

# ==========================
# AI MODELS
# ==========================
st.write("")
st.subheader("🤖 Artificial Intelligence Models")

models = [
    ("🧠 LSTM", "Deep Learning", "Mempelajari pola historis jangka panjang cryptocurrency.", 96),
    ("⚡ GRU", "Neural Network", "Lebih ringan dan cepat dibandingkan LSTM.", 95),
    ("📈 ARIMA", "Statistical", "Model time-series sebagai pembanding AI.", 91),
]

for col, (title, tipe, desc, acc) in zip(st.columns(3), models):
    with col:
        with st.container(border=True):
            st.markdown(f"## {title}")
            st.caption(tipe)
            st.write(desc)
            st.progress(acc)
            st.write(f"**Accuracy : {acc}%**")

# ==========================
# FEATURES
# ==========================
st.write("")
st.subheader("🚀 Platform Features")

features = [
    ("🪙", "Multi Cryptocurrency"),
    ("🤖", "Artificial Intelligence"),
    ("📊", "Interactive Dashboard"),
    ("⚡", "Realtime Prediction"),
]

for col, (icon, title) in zip(st.columns(4), features):
    with col:
        with st.container(border=True):
            st.markdown(f"# {icon}")
            st.write(f"### {title}")

# ==========================
# LEARN CRYPTOCURRENCY
# ==========================
st.write("")
st.subheader("📚 Learn Cryptocurrency")

videos = [
    ("Bitcoin", "https://www.youtube.com/watch?v=bBC-nXj3Ng4"),
    ("Ethereum", "https://www.youtube.com/watch?v=QGH8XnUnOps"),
    ("Solana", "https://www.youtube.com/watch?v=GZ-bYOCMfmE"),
]

for col, (item) in zip(st.columns(3), videos):
    title, url = item
    with col:
        with st.container(border=True):
            st.write(f"### {title}")
            st.video(url)

# ==========================
# QUICK ACCESS
# ==========================
st.write("")
st.subheader("🚀 Quick Access")

left, right = st.columns(2)

with left:
    if st.button("📈 Start Prediction", use_container_width=True):
        if st.session_state.logged_in:
            st.switch_page("pages/1_Prediksi_Bitcoin.py")
        else:
            st.warning("Silakan login terlebih dahulu.")

with right:
    if st.button("🤖 AI Assistant", use_container_width=True):
        if st.session_state.logged_in:
            st.switch_page("pages/2_chatbot.py")
        else:
            st.warning("Silakan login terlebih dahulu.")

# ==========================
# FOOTER
# ==========================
st.write("")
st.divider()

st.markdown("""
<div class="footer">
    <h2>🚀 CRYPZE AI</h2>
    Artificial Intelligence Cryptocurrency Prediction Platform
    <br>
    Powered by <b>Python • TensorFlow • Streamlit • Plotly</b>
    <br><br>
    Universitas Gunadarma
</div>
""", unsafe_allow_html=True)
