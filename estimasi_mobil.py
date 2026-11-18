
import pickle
import streamlit as st
import numpy as np

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(
    page_title="Toyota Car Price Estimator",
    page_icon="🚘",
    layout="wide"
)

# ==========================================
# 2. SESSION STATE
# ==========================================

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

if "hasil_prediksi" not in st.session_state:
    st.session_state.hasil_prediksi = None

# ==========================================
# 3. PENGATURAN TEMA
# ==========================================

st.sidebar.title("⚙️ Pengaturan")

tema = st.sidebar.radio(
    "Pilih Tampilan",
    ["Dark Mode", "Light Mode"],
    index=0 if st.session_state.theme == "Dark" else 1
)

st.session_state.theme = (
    "Dark" if tema == "Dark Mode" else "Light"
)

# ==========================================
# 4. WARNA TEMA
# ==========================================

if st.session_state.theme == "Dark":

    bg = "#101C2E"
    text = "#F5F9FF"
    card = "#203650"
    muted = "#B3C4D9"
    border = "#3B5675"
    input_bg = "#263D59"

else:

    bg = "#F0F5FC"
    text = "#172B46"
    card = "#FFFFFF"
    muted = "#71839C"
    border = "#D9E4F1"
    input_bg = "#FFFFFF"

# ==========================================
# 5. CUSTOM CSS
# ==========================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background-color: {bg};
        color: {text};
    }}

    [data-testid="stHeader"] {{
        background-color: transparent;
    }}

    .block-container {{
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}

    h1, h2, h3, p, label {{
        color: {text};
    }}

    div[data-testid="stNumberInput"] input {{
        background-color: {input_bg};
        color: {text};
        border: 1px solid {border};
        border-radius: 10px;
    }}

    div[data-testid="stNumberInput"] button {{
        background-color: {input_bg};
        color: {text};
    }}

    div.stButton > button {{
        width: 100%;
        min-height: 50px;
        background: linear-gradient(100deg, #246BCE, #439CF4);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: bold;
        font-size: 15px;
    }}

    div.stButton > button:hover {{
        color: white;
        border: none;
        background: #1958AE;
    }}

    div[data-testid="stMetric"] {{
        background-color: {card};
        border: 1px solid {border};
        padding: 18px;
        border-radius: 14px;
    }}

    div[data-testid="stMetricLabel"] {{
        color: {muted};
    }}

    div[data-testid="stMetricValue"] {{
        color: {text};
    }}

    hr {{
        border-color: {border};
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# 6. MEMUAT MODEL
# ==========================================

@st.cache_resource
def load_model():

    with open("estimasi_mobil.sav", "rb") as file:
        return pickle.load(file)

try:

    model = load_model()

except Exception as e:

    st.error("Model estimasi_mobil.sav gagal dimuat.")
    st.exception(e)
    st.stop()

# ==========================================
# 7. HEADER APLIKASI
# ==========================================

st.markdown(
    """
    <div style="
        background: linear-gradient(120deg, #183B65, #2368A9, #328BD2);
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 20px;
    ">
        <div style="
            font-size: 13px;
            font-weight: bold;
            letter-spacing: 2px;
            color: #D5E9FF;
        ">
            SMART AUTOMOTIVE SYSTEM
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Judul menggunakan komponen asli Streamlit
st.title("🚘 Toyota Car Price Estimator")

# Deskripsi menggunakan komponen asli Streamlit
st.write(
    "Sistem estimasi harga mobil bekas Toyota "
    "menggunakan teknologi Machine Learning."
)

st.write("")

# ==========================================
# 8. FORM SPESIFIKASI MOBIL
# ==========================================

st.subheader("🚗 Spesifikasi Kendaraan")

st.caption(
    "Masukkan informasi kendaraan untuk mendapatkan estimasi harga."
)

col1, col2 = st.columns(2)

with col1:

    year = st.number_input(
        "📅 Tahun Mobil",
        min_value=1990,
        max_value=2026,
        value=2019,
        step=1
    )

    mileage = st.number_input(
        "🛣️ Jarak Tempuh (KM)",
        min_value=0,
        value=5000,
        step=1000
    )

    tax = st.number_input(
        "💰 Pajak Mobil",
        min_value=0,
        value=145,
        step=5
    )

with col2:

    mpg = st.number_input(
        "⛽ Konsumsi BBM (MPG)",
        min_value=0.0,
        value=30.2,
        step=0.1
    )

    engineSize = st.number_input(
        "⚙️ Ukuran Mesin (Engine Size)",
        min_value=0.0,
        value=2.0,
        step=0.1
    )

# ==========================================
# 9. RINGKASAN KENDARAAN
# ==========================================

st.divider()

st.subheader("📋 Ringkasan Kendaraan")

summary1, summary2, summary3, summary4, summary5 = st.columns(5)

with summary1:
    st.metric("Tahun", str(year))

with summary2:
    st.metric("Jarak Tempuh", f"{mileage:,} KM")

with summary3:
    st.metric("Pajak", f"{tax:,}")

with summary4:
    st.metric("Konsumsi BBM", f"{mpg} MPG")

with summary5:
    st.metric("Ukuran Mesin", f"{engineSize} L")

# ==========================================
# 10. KURS RUPIAH
# ==========================================

# Kurs asumsi 1 GBP = Rp19.000
kurs = 19000

# ==========================================
# 11. PROSES PREDIKSI
# ==========================================

st.write("")

if st.button("✦ HITUNG ESTIMASI HARGA MOBIL"):

    try:

        input_data = np.array([
            [year, mileage, tax, mpg, engineSize]
        ])

        # Prediksi menggunakan model
        predict = float(model.predict(input_data)[0])

        # Konversi GBP ke Rupiah
        harga_idr = predict * kurs

        # Konversi ke juta Rupiah
        harga_juta = harga_idr / 1000000

        # Simpan hasil prediksi
        st.session_state.hasil_prediksi = {
            "pounds": predict,
            "idr": harga_idr,
            "juta": harga_juta
        }

    except Exception as e:

        st.error("Terjadi kesalahan saat melakukan prediksi.")
        st.exception(e)

# ==========================================
# 12. HASIL PREDIKSI
# ==========================================

if st.session_state.hasil_prediksi is not None:

    hasil = st.session_state.hasil_prediksi

    st.divider()

    st.subheader("💰 Hasil Estimasi Harga")

    st.caption(
        "Berikut hasil estimasi berdasarkan spesifikasi kendaraan."
    )

    result1, result2, result3 = st.columns(3)

    with result1:

        st.metric(
            label="HARGA DALAM POUNDS",
            value=f"£{hasil['pounds']:,.2f}"
        )

    with result2:

        st.metric(
            label="HARGA DALAM RUPIAH",
            value=f"Rp {hasil['idr']:,.0f}"
        )

    with result3:

        st.metric(
            label="HARGA DALAM JUTA RUPIAH",
            value=f"Rp {hasil['juta']:,.2f} juta"
        )

    st.info(
        f"Konversi menggunakan kurs asumsi "
        f"£1 = Rp{kurs:,}. Nilai kurs dapat berubah."
    )

else:

    st.info(
        "Masukkan spesifikasi kendaraan, kemudian tekan "
        "tombol HITUNG ESTIMASI HARGA MOBIL."
    )

# ==========================================
# 13. INFORMASI APLIKASI
# ==========================================

st.divider()

st.subheader("ℹ️ Informasi Sistem")

st.write(
    """
    Aplikasi ini menggunakan algoritma **Linear Regression**
    untuk memperkirakan harga mobil bekas Toyota berdasarkan
    lima variabel, yaitu tahun produksi, jarak tempuh, pajak,
    konsumsi bahan bakar, dan ukuran mesin.

    Hasil prediksi merupakan estimasi berdasarkan pola data
    pelatihan, bukan harga jual pasti kendaraan.
    """
)

st.markdown(
    """
    <div style="
        text-align:center;
        padding:20px;
        color:#65B5FF;
        font-size:12px;
        font-weight:bold;
    ">
        TOYOTA CAR PRICE ESTIMATOR
        <br>
        MACHINE LEARNING · LINEAR REGRESSION
    </div>
    """,
    unsafe_allow_html=True
)

