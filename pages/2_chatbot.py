import streamlit as st
from groq import Groq
import time
import re

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

"apa metode yang digunakan":
"""Aplikasi CRYPZE AI menggunakan tiga metode prediksi, yaitu LSTM (Long Short-Term Memory), GRU (Gated Recurrent Unit), dan ARIMA (AutoRegressive Integrated Moving Average). Ketiga metode tersebut dapat dipilih oleh pengguna untuk membandingkan hasil prediksi harga cryptocurrency.""",

"ada berapa metode":
"""Aplikasi menyediakan tiga metode prediksi, yaitu LSTM, GRU, dan ARIMA.""",

"metode prediksi":
"""Metode prediksi yang tersedia pada aplikasi ini adalah LSTM, GRU, dan ARIMA.""",

"algoritma":
"""Algoritma yang digunakan pada aplikasi ini adalah LSTM, GRU, dan ARIMA untuk melakukan prediksi harga cryptocurrency.""",

"cara menggunakan aplikasi":
"""Langkah menggunakan aplikasi adalah:
1. Login ke sistem.
2. Masuk ke menu Prediksi Cryptocurrency.
3. Pilih aset cryptocurrency.
4. Pilih metode prediksi.
5. Tekan tombol Prediksi.
6. Lihat hasil prediksi dan grafik visualisasi.""",

"cara melakukan prediksi":
"""Untuk melakukan prediksi, buka menu Prediksi Cryptocurrency, pilih aset cryptocurrency, pilih metode prediksi, kemudian tekan tombol Prediksi. Sistem akan memproses data dan menampilkan hasil prediksi beserta grafik visualisasi.""",

"cara membaca grafik":
"""Grafik digunakan untuk menampilkan perubahan harga historis cryptocurrency serta hasil prediksi yang dihasilkan oleh model AI sehingga pengguna dapat membandingkan data aktual dan data prediksi.""",

"fungsi dashboard":
"""Dashboard berfungsi menampilkan informasi utama aplikasi seperti ringkasan cryptocurrency, navigasi menu, serta informasi umum mengenai aplikasi CRYPZE AI.""",

"fungsi chatbot":
"""Chatbot AI berfungsi membantu pengguna memperoleh informasi mengenai aplikasi, cryptocurrency, blockchain, serta metode prediksi seperti LSTM, GRU, dan ARIMA.""",

"fungsi dokumentasi":
"""Menu Dokumentasi digunakan untuk menampilkan dokumentasi penggunaan aplikasi serta informasi pendukung lainnya.""",

"fungsi riwayat":
"""Menu Riwayat digunakan untuk menyimpan hasil prediksi yang telah dilakukan sehingga pengguna dapat melihat kembali hasil prediksi sebelumnya.""",

"sumber data":
"""Data historis cryptocurrency pada aplikasi ini berasal dari Yahoo Finance yang digunakan sebagai dataset dalam proses prediksi.""",

"dataset":
"""Dataset yang digunakan berasal dari Yahoo Finance berupa data historis cryptocurrency yang terdiri dari harga Open, High, Low, Close, dan Volume.""",

"yahoo finance":
"""Yahoo Finance merupakan penyedia data historis pasar keuangan yang digunakan sebagai sumber dataset pada aplikasi CRYPZE AI.""",

"pengembang":
"""CRYPZE AI dikembangkan sebagai aplikasi skripsi berbasis web menggunakan Streamlit untuk melakukan prediksi harga cryptocurrency menggunakan metode LSTM, GRU, dan ARIMA.""",

"framework":
"""Framework utama yang digunakan pada aplikasi ini adalah Streamlit sebagai antarmuka web berbasis Python.""",

"streamlit":
"""Streamlit merupakan framework Python yang digunakan untuk membangun aplikasi web interaktif secara cepat tanpa memerlukan pengembangan frontend yang kompleks.""",

"python":
"""Python digunakan sebagai bahasa pemrograman utama karena memiliki banyak pustaka untuk machine learning, data science, dan pengembangan aplikasi berbasis AI.""",

"lstm":
"""LSTM (Long Short-Term Memory) merupakan algoritma Deep Learning yang mampu mempelajari pola data time series dan digunakan untuk prediksi harga cryptocurrency.""",

"gru":
"""GRU (Gated Recurrent Unit) merupakan pengembangan dari Recurrent Neural Network yang memiliki struktur lebih sederhana dibanding LSTM namun tetap efektif untuk data time series.""",

"arima":
"""ARIMA (AutoRegressive Integrated Moving Average) merupakan metode statistik yang digunakan untuk melakukan prediksi berdasarkan pola data historis time series.""",

"bitcoin":
"""Bitcoin (BTC) merupakan cryptocurrency pertama di dunia yang diperkenalkan oleh Satoshi Nakamoto dan menggunakan teknologi blockchain sebagai dasar sistemnya.""",

"ethereum":
"""Ethereum (ETH) merupakan platform blockchain yang mendukung Smart Contract dan pengembangan aplikasi terdesentralisasi (DApps).""",

"solana":
"""Solana (SOL) merupakan blockchain berkecepatan tinggi yang dirancang untuk mendukung transaksi dengan biaya rendah dan performa tinggi.""",

"cardano":
"""Cardano (ADA) merupakan blockchain berbasis Proof of Stake yang dikembangkan oleh Charles Hoskinson. Namun, pada aplikasi CRYPZE AI saat ini fitur prediksi hanya tersedia untuk Bitcoin, Ethereum, dan Solana.""",

"ada":
"""ADA merupakan aset cryptocurrency asli dari jaringan blockchain Cardano. Saat ini aplikasi CRYPZE AI hanya menyediakan prediksi untuk Bitcoin (BTC), Ethereum (ETH), dan Solana (SOL).""",

"blockchain":
"""Blockchain merupakan teknologi penyimpanan data terdistribusi yang bersifat transparan, aman, dan sulit dimanipulasi sehingga banyak digunakan pada cryptocurrency.""",

"nft":
"""NFT (Non-Fungible Token) merupakan aset digital unik yang kepemilikannya dicatat menggunakan teknologi blockchain.""",

"defi":
"""DeFi (Decentralized Finance) merupakan layanan keuangan berbasis blockchain yang memungkinkan transaksi dilakukan tanpa perantara seperti bank.""",

"wallet":
"""Wallet cryptocurrency merupakan dompet digital yang digunakan untuk menyimpan, menerima, dan mengirim aset cryptocurrency.""",

"trading":
"""Trading cryptocurrency merupakan aktivitas jual beli aset cryptocurrency dengan tujuan memperoleh keuntungan dari perubahan harga pasar.""",

"smart contract":
"""Smart Contract merupakan program otomatis pada blockchain yang akan dijalankan ketika syarat tertentu telah terpenuhi.""",

"proof of work":
"""Proof of Work merupakan mekanisme konsensus blockchain yang menggunakan proses komputasi untuk memvalidasi transaksi.""",

"proof of stake":
"""Proof of Stake merupakan mekanisme konsensus blockchain yang memilih validator berdasarkan jumlah aset yang dimiliki atau di-staking.""",

"kelebihan aplikasi":
"""Kelebihan aplikasi CRYPZE AI adalah mampu melakukan prediksi harga cryptocurrency menggunakan tiga metode berbeda, menampilkan visualisasi hasil prediksi, menyediakan dokumentasi, riwayat prediksi, serta chatbot AI.""",

"kekurangan aplikasi":
"""Versi aplikasi saat ini hanya mendukung prediksi untuk Bitcoin, Ethereum, dan Solana serta belum menggunakan data pasar secara real-time.""",

"tujuan aplikasi":
"""Aplikasi ini bertujuan membantu pengguna melakukan prediksi harga cryptocurrency menggunakan metode AI serta memberikan informasi mengenai cryptocurrency melalui chatbot.""",

"pengembangan selanjutnya":
"""Pengembangan selanjutnya dapat dilakukan dengan menambahkan cryptocurrency baru, integrasi data real-time, metode AI tambahan, serta peningkatan kemampuan chatbot.""",

"mengapa memilih lstm":
"""Metode LSTM dipilih karena mampu mempelajari pola data time series dalam jangka panjang sehingga sangat cocok digunakan untuk prediksi harga cryptocurrency yang memiliki pola historis.""",

"mengapa memilih gru":
"""GRU dipilih karena memiliki struktur yang lebih sederhana dibandingkan LSTM sehingga proses pelatihan model lebih cepat namun tetap mampu menghasilkan prediksi yang baik.""",

"mengapa menggunakan arima":
"""ARIMA digunakan sebagai metode statistik pembanding terhadap metode Deep Learning sehingga hasil prediksi dapat dibandingkan berdasarkan pendekatan yang berbeda.""",

"mengapa menggunakan streamlit":
"""Streamlit dipilih karena memudahkan pengembangan aplikasi web berbasis Python, memiliki antarmuka sederhana, serta mudah diintegrasikan dengan model Machine Learning.""",

"mengapa menggunakan python":
"""Python dipilih karena memiliki banyak pustaka Machine Learning seperti TensorFlow, Scikit-Learn, NumPy, Pandas, dan Plotly yang mendukung pengembangan sistem prediksi.""",

"mengapa yahoo finance":
"""Yahoo Finance dipilih karena menyediakan data historis cryptocurrency yang lengkap, mudah diakses, dan sering digunakan sebagai sumber data penelitian.""",

"mengapa memilih bitcoin":
"""Bitcoin dipilih karena merupakan cryptocurrency dengan kapitalisasi pasar terbesar serta memiliki data historis yang lengkap sehingga cocok digunakan sebagai objek penelitian.""",

"mengapa memilih ethereum":
"""Ethereum dipilih karena merupakan cryptocurrency terbesar kedua yang memiliki ekosistem blockchain yang luas dan banyak digunakan dalam penelitian.""",

"mengapa memilih solana":
"""Solana dipilih karena memiliki performa transaksi tinggi dan menjadi salah satu cryptocurrency dengan perkembangan yang pesat.""",

"mengapa tidak menggunakan cardano":
"""Pada versi aplikasi ini, prediksi difokuskan pada Bitcoin, Ethereum, dan Solana. Cardano dapat ditambahkan sebagai pengembangan pada penelitian berikutnya.""",

"mengapa tidak menggunakan cnn":
"""CNN lebih umum digunakan pada data citra. Penelitian ini menggunakan data time series sehingga metode LSTM, GRU, dan ARIMA dinilai lebih sesuai.""",

"mengapa tidak menggunakan random forest":
"""Random Forest lebih sesuai untuk data klasifikasi maupun regresi umum, sedangkan penelitian ini menggunakan data time series sehingga dipilih metode yang lebih sesuai.""",

"mengapa tidak menggunakan xgboost":
"""XGBoost merupakan algoritma machine learning yang sangat baik untuk data tabular, namun penelitian ini berfokus pada metode time series sehingga digunakan LSTM, GRU, dan ARIMA.""",

"apa itu machine learning":
"""Machine Learning merupakan cabang kecerdasan buatan yang memungkinkan komputer mempelajari pola dari data tanpa diprogram secara eksplisit.""",

"apa itu deep learning":
"""Deep Learning merupakan bagian dari Machine Learning yang menggunakan jaringan saraf tiruan dengan banyak lapisan untuk mempelajari pola data yang kompleks.""",

"apa itu artificial intelligence":
"""Artificial Intelligence atau AI merupakan teknologi yang memungkinkan komputer meniru kemampuan berpikir dan mengambil keputusan seperti manusia.""",

"apa itu time series":
"""Time Series merupakan kumpulan data yang tersusun berdasarkan urutan waktu sehingga dapat digunakan untuk menganalisis pola dan melakukan prediksi.""",

"apa itu epoch":
"""Epoch merupakan satu kali proses pelatihan model menggunakan seluruh data training.""",

"apa itu batch":
"""Batch merupakan jumlah data yang diproses dalam satu iterasi selama proses pelatihan model.""",

"apa itu loss":
"""Loss merupakan nilai kesalahan model selama proses pelatihan. Semakin kecil nilai loss maka performa model semakin baik.""",

"apa itu optimizer":
"""Optimizer merupakan algoritma yang digunakan untuk memperbarui bobot jaringan saraf agar model memperoleh hasil prediksi yang lebih baik.""",

"apa itu adam":
"""Adam merupakan salah satu optimizer yang banyak digunakan pada Deep Learning karena mampu mempercepat proses pelatihan model.""",

"apa itu scaler":
"""Scaler digunakan untuk melakukan normalisasi data sehingga nilai setiap fitur berada pada rentang yang sama sebelum diproses oleh model.""",

"apa itu minmax scaler":
"""MinMaxScaler merupakan metode normalisasi yang mengubah nilai data ke rentang tertentu, umumnya antara 0 hingga 1.""",

"apa itu normalisasi":
"""Normalisasi merupakan proses mengubah skala data agar setiap fitur memiliki rentang nilai yang seragam sehingga proses pelatihan model menjadi lebih stabil.""",

"apa itu mae":
"""MAE (Mean Absolute Error) merupakan metrik evaluasi yang mengukur rata-rata selisih absolut antara nilai aktual dan nilai prediksi.""",

"apa itu rmse":
"""RMSE (Root Mean Square Error) merupakan metrik evaluasi yang mengukur besarnya kesalahan prediksi dengan memberikan penalti lebih besar terhadap kesalahan yang tinggi.""",

"apa itu r2":
"""R² Score digunakan untuk mengukur seberapa baik model mampu menjelaskan variasi data. Semakin mendekati 1, semakin baik performa model.""",

"apa itu overfitting":
"""Overfitting merupakan kondisi ketika model terlalu menghafal data training sehingga performanya menurun saat digunakan pada data baru.""",

"apa itu underfitting":
"""Underfitting terjadi ketika model belum mampu mempelajari pola data dengan baik sehingga menghasilkan prediksi yang kurang akurat.""",

"apa tujuan penelitian":
"""Tujuan penelitian ini adalah merancang dan membangun aplikasi berbasis web yang mampu melakukan prediksi harga cryptocurrency menggunakan metode LSTM, GRU, dan ARIMA serta menyajikan hasil prediksi dalam bentuk visualisasi yang mudah dipahami pengguna.""",

"apa manfaat penelitian":
"""Penelitian ini diharapkan dapat membantu pengguna memperoleh gambaran tren harga cryptocurrency serta menjadi referensi dalam pengembangan sistem prediksi berbasis Artificial Intelligence.""",

"apa kontribusi penelitian":
"""Kontribusi penelitian ini adalah menghasilkan aplikasi prediksi cryptocurrency berbasis web yang menggabungkan tiga metode prediksi, yaitu LSTM, GRU, dan ARIMA sehingga pengguna dapat membandingkan performa masing-masing metode.""",

"mengapa membuat aplikasi ini":
"""Aplikasi ini dibuat untuk membantu pengguna melakukan prediksi harga cryptocurrency secara lebih mudah melalui antarmuka web yang sederhana serta memanfaatkan metode Artificial Intelligence.""",

"siapa target pengguna":
"""Target pengguna aplikasi ini adalah mahasiswa, peneliti, investor pemula, maupun masyarakat yang ingin mempelajari prediksi harga cryptocurrency.""",

"apa keunggulan aplikasi":
"""Keunggulan aplikasi ini adalah menyediakan tiga metode prediksi dalam satu aplikasi, menampilkan visualisasi grafik, menyimpan riwayat prediksi, serta dilengkapi chatbot AI sebagai media informasi.""",

"apa kelemahan aplikasi":
"""Kelemahan aplikasi saat ini adalah hanya mendukung prediksi Bitcoin, Ethereum, dan Solana serta belum menggunakan data pasar secara real-time.""",

"bagaimana alur aplikasi":
"""Alur aplikasi dimulai dari login pengguna, memilih menu prediksi, memilih aset cryptocurrency, memilih metode prediksi, menjalankan proses prediksi, kemudian sistem menampilkan grafik, evaluasi model, dan hasil prediksi.""",

"bagaimana proses prediksi":
"""Proses prediksi dimulai dari pengambilan dataset historis, preprocessing data, pemilihan metode prediksi, pelatihan model, evaluasi model, kemudian menghasilkan prediksi harga cryptocurrency.""",

"apa preprocessing":
"""Preprocessing merupakan tahap awal pengolahan data sebelum diproses oleh model, seperti pembersihan data, normalisasi, dan penyusunan data time series.""",

"apa training":
"""Training merupakan proses pembelajaran model menggunakan data historis sehingga model mampu mengenali pola yang terdapat pada data.""",

"apa testing":
"""Testing merupakan proses pengujian model menggunakan data yang belum pernah dipelajari sebelumnya untuk mengetahui kemampuan prediksi model.""",

"apa evaluasi model":
"""Evaluasi model dilakukan menggunakan metrik seperti MAE, RMSE, dan R² Score untuk mengetahui tingkat akurasi hasil prediksi.""",

"apa visualisasi":
"""Visualisasi digunakan untuk menampilkan data historis dan hasil prediksi dalam bentuk grafik sehingga lebih mudah dipahami oleh pengguna.""",

"mengapa menggunakan chatbot":
"""Chatbot ditambahkan untuk membantu pengguna memperoleh informasi mengenai aplikasi, cryptocurrency, blockchain, serta metode prediksi tanpa harus membuka dokumentasi secara manual.""",

"mengapa menggunakan groq":
"""Groq digunakan sebagai penyedia layanan Large Language Model (LLM) sehingga chatbot dapat memberikan jawaban yang cepat dan relevan terhadap pertanyaan pengguna.""",

"apa itu groq":
"""Groq merupakan penyedia layanan inferensi AI yang dirancang untuk menjalankan Large Language Model dengan kecepatan tinggi.""",

"apa itu llama":
"""Llama merupakan Large Language Model yang dikembangkan oleh Meta dan digunakan sebagai model bahasa pada chatbot CRYPZE AI.""",

"mengapa menggunakan llama":
"""Model Llama dipilih karena mampu menghasilkan jawaban yang cepat, relevan, dan mudah diintegrasikan dengan aplikasi berbasis Python.""",

"bagaimana chatbot bekerja":
"""Chatbot bekerja dengan memeriksa FAQ terlebih dahulu. Jika jawaban tidak ditemukan, pertanyaan akan diteruskan ke model AI Groq Llama untuk menghasilkan jawaban yang relevan.""",

"mengapa menggunakan faq":
"""FAQ digunakan agar pertanyaan yang sering muncul dapat dijawab secara instan tanpa perlu mengakses model AI sehingga respon menjadi lebih cepat dan konsisten.""",

"bagaimana pengembangan selanjutnya":
"""Pengembangan selanjutnya dapat dilakukan dengan menambahkan cryptocurrency baru, integrasi data real-time, metode prediksi tambahan, peningkatan akurasi model, serta pengembangan chatbot yang lebih cerdas.""",

"mengapa aplikasi berbasis web":
"""Aplikasi berbasis web dipilih karena dapat diakses dari berbagai perangkat tanpa memerlukan proses instalasi tambahan.""",

"apa manfaat streamlit":
"""Streamlit mempermudah pengembangan aplikasi Machine Learning karena mampu menampilkan visualisasi, grafik, dan antarmuka interaktif hanya dengan menggunakan Python.""",

"apa itu plotly":
"""Plotly merupakan pustaka visualisasi data yang digunakan untuk menampilkan grafik interaktif pada aplikasi.""",

"apa itu tensorflow":
"""TensorFlow merupakan framework Deep Learning yang digunakan untuk membangun dan melatih model LSTM maupun GRU.""",

"apa itu scikit learn":
"""Scikit-Learn merupakan pustaka Machine Learning Python yang digunakan untuk preprocessing data, normalisasi, serta evaluasi model.""",

"apa itu pandas":
"""Pandas merupakan pustaka Python yang digunakan untuk membaca, mengolah, dan memanipulasi dataset.""",

"apa itu numpy":
"""NumPy merupakan pustaka Python yang digunakan untuk melakukan komputasi numerik serta pengolahan array dalam proses Machine Learning.""",

"apakah aplikasi ini akurat":
"""Akurasi aplikasi bergantung pada metode prediksi yang dipilih serta kualitas data historis yang digunakan. Untuk mengukur performa model, aplikasi menggunakan metrik evaluasi seperti MAE, RMSE, dan R² Score.""",

"apakah hasil prediksi selalu benar":
"""Tidak. Hasil prediksi merupakan estimasi berdasarkan data historis sehingga tidak dapat menjamin kondisi pasar di masa depan yang dipengaruhi banyak faktor.""",

"mengapa hasil prediksi bisa berbeda":
"""Setiap metode memiliki cara kerja yang berbeda dalam mempelajari pola data sehingga hasil prediksi yang dihasilkan juga dapat berbeda.""",

"mengapa menggunakan tiga metode":
"""Penggunaan tiga metode bertujuan agar pengguna dapat membandingkan performa masing-masing metode dan mengetahui metode yang memberikan hasil terbaik pada dataset tertentu.""",

"metode mana yang paling baik":
"""Tidak ada satu metode yang selalu paling baik. Performa LSTM, GRU, dan ARIMA bergantung pada karakteristik data yang digunakan sehingga perlu dibandingkan menggunakan metrik evaluasi.""",

"berapa cryptocurrency yang didukung":
"""Saat ini aplikasi mendukung prediksi untuk tiga cryptocurrency, yaitu Bitcoin (BTC), Ethereum (ETH), dan Solana (SOL).""",

"apakah bisa prediksi cardano":
"""Saat ini aplikasi belum menyediakan fitur prediksi untuk Cardano (ADA). Cardano hanya dapat dijelaskan sebagai informasi umum melalui chatbot.""",

"apakah bisa prediksi xrp":
"""Saat ini aplikasi belum mendukung prediksi XRP. Pengembangan tersebut dapat ditambahkan pada versi berikutnya.""",

"apakah bisa prediksi dogecoin":
"""Saat ini aplikasi belum mendukung prediksi Dogecoin. Pengguna hanya dapat memperoleh informasi umum mengenai cryptocurrency tersebut.""",

"apakah aplikasi realtime":
"""Tidak. Prediksi dilakukan menggunakan dataset historis yang telah disiapkan sehingga belum menggunakan data pasar secara real-time.""",

"apakah chatbot menggunakan ai":
"""Ya. Chatbot menggunakan Large Language Model (LLM) melalui layanan Groq dengan model Llama sehingga mampu menjawab pertanyaan pengguna secara otomatis.""",

"apakah chatbot selalu benar":
"""Chatbot dirancang untuk memberikan jawaban berdasarkan pengetahuan yang dimiliki. Namun, pengguna tetap disarankan melakukan verifikasi terhadap informasi yang bersifat kritis atau terus berubah.""",

"bagaimana jika internet mati":
"""Apabila koneksi internet terputus, fitur chatbot yang menggunakan layanan Groq tidak dapat digunakan. Namun fitur lain yang tidak memerlukan layanan eksternal tetap dapat berjalan sesuai implementasi aplikasi.""",

"apakah chatbot bisa menjawab semua pertanyaan":
"""Tidak. Chatbot difokuskan untuk menjawab pertanyaan mengenai aplikasi CRYPZE AI, cryptocurrency, blockchain, serta metode prediksi seperti LSTM, GRU, dan ARIMA.""",

"berapa hari prediksi":
"""Pada implementasi aplikasi ini, model menghasilkan prediksi untuk beberapa hari ke depan sesuai rancangan penelitian yang digunakan.""",

"apa itu cryptocurrency":
"""Cryptocurrency merupakan aset digital yang menggunakan teknologi blockchain sebagai sistem pencatatan transaksi sehingga dapat digunakan tanpa perantara.""",

"apa itu btc":
"""BTC adalah singkatan dari Bitcoin, yaitu cryptocurrency pertama di dunia yang diperkenalkan oleh Satoshi Nakamoto.""",

"apa itu eth":
"""ETH merupakan singkatan dari Ethereum, yaitu cryptocurrency yang mendukung Smart Contract dan aplikasi terdesentralisasi.""",

"apa itu sol":
"""SOL merupakan singkatan dari Solana, yaitu cryptocurrency yang berjalan pada jaringan blockchain Solana.""",

"apa itu ada":
"""ADA merupakan cryptocurrency asli dari jaringan Cardano. Namun, aplikasi CRYPZE AI saat ini belum menyediakan fitur prediksi untuk ADA.""",

"apa itu altcoin":
"""Altcoin merupakan istilah untuk seluruh cryptocurrency selain Bitcoin.""",

"apa itu stablecoin":
"""Stablecoin merupakan cryptocurrency yang nilainya dipatok terhadap aset tertentu seperti mata uang dolar Amerika Serikat.""",

"apa itu market cap":
"""Market Capitalization merupakan total nilai pasar suatu cryptocurrency yang diperoleh dari harga aset dikalikan jumlah koin yang beredar.""",

"apa itu volume":
"""Volume perdagangan menunjukkan jumlah transaksi cryptocurrency yang terjadi dalam periode tertentu.""",

"apa itu candlestick":
"""Candlestick merupakan bentuk visualisasi harga yang menampilkan informasi Open, High, Low, dan Close dalam satu periode waktu.""",

"apa itu open high low close":
"""Open adalah harga pembukaan, High adalah harga tertinggi, Low adalah harga terendah, dan Close adalah harga penutupan pada periode tertentu.""",

"mengapa menggunakan data historis":
"""Data historis digunakan karena mengandung pola pergerakan harga yang dapat dipelajari oleh model AI untuk menghasilkan prediksi.""",

"apakah aplikasi gratis":
"""Aplikasi ini dikembangkan sebagai media penelitian dan pembelajaran sehingga dapat digunakan sesuai tujuan penelitian yang telah ditetapkan.""",

"bagaimana cara meningkatkan akurasi":
"""Akurasi dapat ditingkatkan dengan menggunakan dataset yang lebih banyak, melakukan tuning hyperparameter, menambahkan fitur baru, serta mencoba metode prediksi lain.""",

"apa perbedaan lstm dan gru":
"""LSTM memiliki struktur yang lebih kompleks dengan tiga gerbang utama sehingga mampu mengingat informasi dalam jangka panjang. GRU memiliki struktur lebih sederhana sehingga proses pelatihannya lebih cepat namun tetap memiliki performa yang baik pada data time series.""",

"apa perbedaan arima dan lstm":
"""ARIMA merupakan metode statistik berbasis time series, sedangkan LSTM merupakan metode Deep Learning yang mampu mempelajari pola data yang lebih kompleks.""",
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

        if any(re.search(rf"\b{re.escape(k)}\b", lower) for k in keywords):
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

Jika pertanyaan masih berkaitan dengan cryptocurrency,
blockchain,
Bitcoin,
Ethereum,
Solana,
NFT,
DeFi,
LSTM,
GRU,
ARIMA,
atau teknologi yang digunakan aplikasi,
maka jawablah secara normal.

Hanya jika pertanyaan benar-benar tidak berhubungan dengan aplikasi maupun cryptocurrency,
barulah jawab:

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