import streamlit as st
import pandas as pd
import plotly.express as px

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
    page_title="🤝 Kemitraan Kripto",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="auto"
)

# =========================
# CUSTOM ULTRA-MODERN FIXED CSS
# =========================
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
    width: 100%;
    max-width: 100% !important;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

/* KELAS JUDUL UTAMA (UKURAN BESAR & TERPUSAT) */
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
}

/* SECTION HEADINGS */
h2, h3 {
    color: #f1f5f9 !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px;
}

/* CRYPTO CARD GLASSMORPHISM REFINED */
.crypto-card {
    background: rgba(17, 24, 39, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.07);
    padding: 24px 28px;
    border-radius: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    margin-bottom: 24px;
    transition: all 0.3s ease;
}

.crypto-card:hover {
    transform: translateY(-3px);
    border-color: rgba(56, 189, 248, 0.4);
    box-shadow: 0 8px 30px rgba(56, 189, 248, 0.12);
}

.platform-name {
    font-size: 24px;
    font-weight: 700;
    color: #38bdf8;
    margin-bottom: 4px;
}

.desc {
    color: #94a3b8;
    margin-top: 4px;
    margin-bottom: 12px;
    font-size: 14px;
    line-height: 1.5;
}

/* METRIC BOX GLASSMORPHISM REFINED */
.metric-box {
    background: rgba(15, 23, 42, 0.75);
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.07);
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.metric-box:hover {
    border-color: rgba(34, 197, 94, 0.4);
    transform: translateY(-2px);
}

.metric-box h2 {
    color: #22c55e !important;
    font-size: 26px !important;
    margin-bottom: 2px !important;
}

.metric-box p {
    color: #94a3b8 !important;
    font-size: 13px !important;
    margin: 0 !important;
    font-weight: 500;
}

/* BADGE REFINED */
.badge {
    background: rgba(34, 197, 94, 0.12);
    color: #22c55e;
    border: 1px solid rgba(34, 197, 94, 0.25);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.3px;
    display: inline-block;
    margin-bottom: 12px;
}

/* STLINK BUTTON OVERRIDE */
.stLinkButton>a {
    background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(14, 165, 233, 0.25) !important;
    transition: all 0.3s ease !important;
    padding: 10px 16px !important;
}

.stLinkButton>a:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(14, 165, 233, 0.4) !important;
    background: linear-gradient(135deg, #1d4ed8 0%, #0284c7 100%) !important;
}

/* DATAFRAME & TABS STYLING */
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

/* INPUTS */
.stTextInput input, .stMultiSelect div[data-baseweb="select"] {
    background-color: rgba(17, 24, 39, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: white !important;
    border-radius: 12px !important;
    font-size: 14px !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR (DENGAN LOGO)
# =========================
with st.sidebar:
    st.success("🟢 System Online")
    st.divider()

    st.metric("🪙 Crypto", "3 Aset")
    st.metric("🤖 AI Model", "3 Metode")
    st.metric("⚡ Status", "Realtime")

    st.divider()

    st.caption("Version 3.0 • Universitas Gunadarma")

# =========================
# DATA
# =========================
platforms = [
    {
        "Nama": "Indodax",
        "Situs": "https://indodax.com",
        "Deskripsi": "Platform jual beli kripto terbesar dan pionir di Indonesia dengan likuiditas tinggi.",
        "Logo": "https://png.pngitem.com/pimgs/s/378-3781496_indodax-logo-png-transparent-png.png",
        "Rating": 4.8,
        "Maker": 0.20,
        "Taker": 0.30,
        "Coin": "BTC, ETH, ADA, XRP, SOL",
        "Deposit": "Rp 10.000",
        "Kelebihan": "Likuiditas tinggi & market paling lengkap"
    },
    {
        "Nama": "Tokocrypto",
        "Situs": "https://www.tokocrypto.com",
        "Deskripsi": "Didukung penuh oleh ekosistem Binance, populer dengan fitur trading yang canggih.",
        "Logo": "https://assets.bitdegree.org/images/tokocrypto-review-logo-square.png?tr=w-250",
        "Rating": 4.7,
        "Maker": 0.10,
        "Taker": 0.20,
        "Coin": "BTC, ETH, BNB, ADA",
        "Deposit": "Rp 50.000",
        "Kelebihan": "Terintegrasi langsung dengan ekosistem Binance"
    },
    {
        "Nama": "Reku",
        "Situs": "https://reku.id",
        "Deskripsi": "Platform modern dan ramah pemula dengan fitur investasi otomatis (staking/DCA).",
        "Logo": "https://play-lh.googleusercontent.com/LEJzj7BKoim_x6AmxY_oREOCL6wpqNTWkiGhd40r31-08lVOJE-qL6erP8fSaofiXww",
        "Rating": 4.6,
        "Maker": 0.10,
        "Taker": 0.20,
        "Coin": "BTC, ETH, SOL",
        "Deposit": "Rp 50.000",
        "Kelebihan": "UI/UX sangat modern dan mudah digunakan"
    },
    {
        "Nama": "Pintu",
        "Situs": "https://pintu.co.id",
        "Deskripsi": "Aplikasi investasi kripto yang legal, simpel, dan dirancang khusus untuk mobile-first.",
        "Logo": "https://assets.coingecko.com/coins/images/20281/large/image_1_8dd79a68aa.png?1696519686",
        "Rating": 4.7,
        "Maker": 0.25,
        "Taker": 0.35,
        "Coin": "BTC, ETH, ADA",
        "Deposit": "Rp 50.000",
        "Kelebihan": "Sangat ramah dan mudah dipahami pemula"
    },
    {
        "Nama": "Triv",
        "Situs": "https://triv.co.id",
        "Deskripsi": "Broker aset kripto legal dengan dukungan berbagai metode pembayaran instan 24/7.",
        "Logo": "https://triv.co.id/assets/logo_triv-6bfd8b14aab606f32abb737168e7d6ce14c567877614d274e9675d768da1a505.png",
        "Rating": 4.5,
        "Maker": 0.20,
        "Taker": 0.30,
        "Coin": "BTC, ETH",
        "Deposit": "Rp 50.000",
        "Kelebihan": "Metode deposit dan penarikan super fleksibel"
    },
]

# =========================
# HEADER (MENGGUNAKAN TAG H1 AGAR BESAR)
# =========================
st.markdown('<h1 class="main-title">🤝 Kemitraan & Platform Kripto</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Direktori platform bursa kripto resmi, terpercaya, dan teregulasi BAPPEBTI di Indonesia 🇮🇩</p>', unsafe_allow_html=True)

# =========================
# METRICS
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-box">
        <h2>5+</h2>
        <p>Platform Partner Resmi</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-box">
        <h2>100+</h2>
        <p>Aset Koin Didukung</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-box">
        <h2>100%</h2>
        <p>Terverifikasi BAPPEBTI</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# =========================
# SEARCH
# =========================
search = st.text_input("🔎 Cari Platform Kripto...", placeholder="Ketik nama platform (cth: Indodax, Reku)...")

filtered_platforms = [
    p for p in platforms
    if search.lower() in p["Nama"].lower()
]

st.write("")

# =========================
# TABS
# =========================
tabs = st.tabs([
    "🏢 Daftar Platform",
    "📈 Grafik Fee",
    "⚖️ Perbandingan",
    "🏦 Metode Deposit"
])

# =========================
# TAB PLATFORM
# =========================
with tabs[0]:
    st.write("")
    if not filtered_platforms:
        st.warning("⚠️ Platform yang dicari tidak ditemukan.")
    
    for p in filtered_platforms:
        st.markdown('<div class="crypto-card">', unsafe_allow_html=True)

        col1, col2 = st.columns([1, 5], gap="medium")

        with col1:
            st.image(p["Logo"], width=80)

        with col2:
            st.markdown(f'<div class="platform-name">{p["Nama"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="desc">{p["Deskripsi"]}</div>', unsafe_allow_html=True)
            st.markdown('<div class="badge">✅ TERVERIFIKASI BAPPEBTI</div>', unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            c1.metric("⭐ Rating", p["Rating"])
            c2.metric("💸 Maker Fee", f"{p['Maker']}%")
            c3.metric("💰 Min. Deposit", p["Deposit"])

            st.markdown(f"<div style='margin-top: 12px; margin-bottom: 6px; font-size: 14px;'>✨ <b>Keunggulan:</b> {p['Kelebihan']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-bottom: 16px; font-size: 13px; color: #94a3b8;'>🪙 <b>Coin Populer:</b> {p['Coin']}</div>", unsafe_allow_html=True)

            st.link_button(
                "🚀 Kunjungi Platform Resmi",
                p["Situs"],
                use_container_width=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# TAB GRAFIK
# =========================
with tabs[1]:
    st.subheader("📈 Analisis Perbandingan Trading Fee")
    st.markdown('<p class="subtitle">Perbandingan persentase biaya transaksi (Maker & Taker Fee) antar bursa.</p>', unsafe_allow_html=True)

    df_chart = pd.DataFrame({
        "Platform": [p["Nama"] for p in platforms],
        "Maker Fee": [p["Maker"] for p in platforms],
        "Taker Fee": [p["Taker"] for p in platforms]
    })

    fig = px.bar(
        df_chart,
        x="Platform",
        y=["Maker Fee", "Taker Fee"],
        barmode="group",
        title="Perbandingan Trading Fee (%)",
        color_discrete_sequence=["#38bdf8", "#22c55e"]
    )

    fig.update_layout(
        template="plotly_dark",
        height=480,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", color="#f8fafc"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB PERBANDINGAN
# =========================
with tabs[2]:
    st.subheader("⚖️ Matriks Perbandingan Platform")
    st.markdown('<p class="subtitle">Pilih beberapa platform sekaligus untuk membandingkan spesifikasinya secara berdampingan.</p>', unsafe_allow_html=True)

    selected = st.multiselect(
        "Pilih Platform untuk Dibandingkan",
        [p["Nama"] for p in platforms],
        default=[platforms[0]["Nama"], platforms[1]["Nama"]]
    )

    st.write("")
    if selected:
        compare_df = pd.DataFrame([
            {
                "Platform": p["Nama"],
                "Rating": p["Rating"],
                "Maker Fee (%)": p["Maker"],
                "Taker Fee (%)": p["Taker"],
                "Minimum Deposit": p["Deposit"],
                "Coin Utama": p["Coin"]
            }
            for p in platforms if p["Nama"] in selected
        ])

        st.dataframe(compare_df, use_container_width=True)
    else:
        st.info("💡 Silakan pilih minimal satu platform di atas.")

# =========================
# TAB DEPOSIT
# =========================
with tabs[3]:
    st.subheader("🏦 Dukungan Metode Pembayaran & Deposit")
    st.markdown('<p class="subtitle">Tabel kemudahan transaksi penyetoran dana pada masing-masing bursa.</p>', unsafe_allow_html=True)

    deposit_data = {
        "Platform": ["Indodax", "Tokocrypto", "Reku", "Pintu", "Triv"],
        "Transfer Bank": ["✅", "✅", "✅", "✅", "✅"],
        "E-Wallet": ["✅", "✅", "❌", "✅", "✅"],
        "Kartu Debit": ["❌", "❌", "❌", "❌", "✅"],
        "Crypto Deposit": ["✅", "✅", "✅", "✅", "✅"]
    }

    df_deposit = pd.DataFrame(deposit_data)

    st.dataframe(
        df_deposit.set_index("Platform"),
        use_container_width=True
    )

    st.info("📌 Informasi fitur dan metode pembayaran dapat berubah sewaktu-waktu mengikuti kebijakan internal masing-masing platform.")

# =========================
# FOOTER
# =========================
st.write("")
st.divider()

st.markdown("""
<p style='text-align: center; color: #64748b; font-size: 13px; margin-top: 20px;'>
    ⚠️ <b>Disclaimer:</b> Investasi aset kripto memiliki tingkat risiko yang tinggi. Selalu lakukan riset mandiri (DYOR) sebelum melakukan transaksi atau berinvestasi.
</p>
""", unsafe_allow_html=True)