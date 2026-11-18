
import pickle
import streamlit as st
import numpy as np

# =====================================================
# KONFIGURASI APLIKASI
# =====================================================
st.set_page_config(
    page_title="Toyota Car Price Estimator",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# SESSION STATE
# =====================================================
if "theme" not in st.session_state:
    st.session_state.theme = "Dark Mode"

if "hasil_prediksi" not in st.session_state:
    st.session_state.hasil_prediksi = None

if "input_terakhir" not in st.session_state:
    st.session_state.input_terakhir = None


# =====================================================
# PILIHAN TEMA
# =====================================================
with st.sidebar:
    st.title("🚘 AUTO ESTIMATOR")
    st.caption("TOYOTA USED CAR VALUATION")
    st.divider()

    pilihan_tema = st.radio(
        "Tampilan aplikasi",
        ["Dark Mode", "Light Mode"],
        index=0 if st.session_state.theme == "Dark Mode" else 1
    )

    st.session_state.theme = pilihan_tema

    st.divider()

    st.subheader("Tentang Aplikasi")
    st.write(
        "Aplikasi ini digunakan untuk memperkirakan harga "
        "mobil bekas Toyota menggunakan algoritma "
        "Machine Learning Linear Regression."
    )

    st.divider()

    st.caption("MODEL INFORMATION")
    st.write("Algoritma: Linear Regression")
    st.write("Dataset: Toyota Used Cars")
    st.write("Mata uang: GBP dan IDR")

    st.divider()
    st.caption("Toyota Car Price Estimator")
    st.caption("Machine Learning Application")


# =====================================================
# TEMA DAN WARNA
# =====================================================
if st.session_state.theme == "Dark Mode":
    bg_color = "#0B1424"
    card_color = "#142238"
    text_color = "#F2F6FC"
    muted_color = "#A5B4C9"
    border_color = "#2D425E"
    accent_color = "#55A9FF"
else:
    bg_color = "#F3F6FB"
    card_color = "#FFFFFF"
    text_color = "#172B46"
    muted_color = "#718198"
    border_color = "#DCE5F0"
    accent_color = "#267DD1"


# =====================================================
# CSS TAMPILAN
# =====================================================
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}

    [data-testid="stSidebar"] {{
        background-color: {card_color};
        border-right: 1px solid {border_color};
    }}

    [data-testid="stHeader"] {{
        background-color: {bg_color};
    }}

    h1, h2, h3, h4, p, label {{
        color: {text_color} !important;
    }}

    [data-testid="stCaptionContainer"] p {{
        color: {muted_color} !important;
    }}

    [data-testid="stMetric"] {{
        background-color: {card_color};
        border: 1px solid {border_color};
        padding: 20px;
        border-radius: 12px;
    }}

    [data-testid="stMetricLabel"] {{
        color: {muted_color} !important;
    }}

    [data-testid="stMetricValue"] {{
        color: {accent_color} !important;
        font-weight: 700;
    }}

    div[data-testid="stNumberInput"] input {{
        background-color: {card_color};
        color: {text_color};
        border: 1px solid {border_color};
        border-radius: 8px;
    }}

    div.stButton > button {{
        background-color: {accent_color};
        color: white;
        border: none;
        border-radius: 9px;
        min-height: 48px;
        font-weight: 700;
        width: 100%;
        transition: 0.2s;
    }}

    div.stButton > button:hover {{
        background-color: #287CC5;
        color: white;
        border: none;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border-radius: 14px;
        border-color: {border_color};
    }}

    hr {{
        border-color: {border_color};
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# LOAD MODEL
# =====================================================
@st.cache_resource
def load_model():
    with open("estimasi_mobil.sav", "rb") as file:
        return pickle.load(file)


try:
    model = load_model()
except Exception as e:
    st.error("Model tidak dapat dimuat. Pastikan file estimasi_mobil.sav tersedia.")
    st.exception(e)
    st.stop()


# =====================================================
# HEADER UTAMA
# =====================================================
st.title("Toyota Car Price Estimator")

st.caption(
    "SMART AUTOMOTIVE VALUATION SYSTEM  |  "
    "Machine Learning Powered"
)

st.write(
    "Sistem estimasi harga mobil bekas Toyota "
    "berdasarkan spesifikasi kendaraan."
)

st.divider()


# =====================================================
# INFORMASI SINGKAT
# =====================================================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("MODEL", "Linear Regression")

with col2:
    st.metric("BRAND", "Toyota")

with col3:
    st.metric("CURRENCY", "GBP / IDR")


st.write("")


# =====================================================
# FORM INPUT
# =====================================================
with st.container(border=True):

    st.subheader("Vehicle Specifications")
    st.caption("Masukkan spesifikasi kendaraan untuk melakukan estimasi harga.")

    col1, col2 = st.columns(2)

    with col1:
        year = st.number_input(
            "Tahun Produksi",
            min_value=1990,
            max_value=2026,
            value=2018,
            step=1,
            help="Tahun produksi kendaraan."
        )

        mileage = st.number_input(
            "Jarak Tempuh (Miles)",
            min_value=0,
            max_value=500000,
            value=30000,
            step=1000,
            help="Total jarak tempuh kendaraan dalam miles."
        )

        tax = st.number_input(
            "Pajak Kendaraan (£)",
            min_value=0,
            max_value=1000,
            value=150,
            step=5,
            help="Nilai pajak kendaraan dalam Poundsterling."
        )

    with col2:
        mpg = st.number_input(
            "Konsumsi BBM (MPG)",
            min_value=0.0,
            max_value=200.0,
            value=50.0,
            step=0.5,
            help="Konsumsi bahan bakar dalam miles per gallon."
        )

        engineSize = st.number_input(
            "Kapasitas Mesin (Liter)",
            min_value=0.0,
            max_value=10.0,
            value=1.8,
            step=0.1,
            help="Kapasitas mesin kendaraan."
        )

    st.write("")

    tombol_prediksi = st.button(
        "GENERATE PRICE ESTIMATION",
        use_container_width=True
    )


# =====================================================
# PROSES PREDIKSI
# =====================================================
if tombol_prediksi:

    # Urutan fitur tetap sama dengan model
    input_data = np.array([[
        year,
        mileage,
        tax,
        mpg,
        engineSize
    ]])

    predict = float(model.predict(input_data)[0])

    # Konversi GBP ke IDR
    kurs = 19000
    harga_idr = predict * kurs
    harga_juta = harga_idr / 1000000

    # Simpan hasil prediksi
    st.session_state.hasil_prediksi = {
        "gbp": predict,
        "idr": harga_idr,
        "juta": harga_juta
    }

    st.session_state.input_terakhir = {
        "year": year,
        "mileage": mileage,
        "tax": tax,
        "mpg": mpg,
        "engineSize": engineSize
    }


# =====================================================
# HASIL ESTIMASI
# =====================================================
if st.session_state.hasil_prediksi is not None:

    hasil = st.session_state.hasil_prediksi

    st.write("")
    st.divider()

    st.subheader("Estimated Vehicle Value")
    st.caption("Hasil estimasi berdasarkan spesifikasi kendaraan yang dimasukkan.")

    with st.container(border=True):

        st.caption("ESTIMATED PRICE IN POUNDSTERLING")

        st.title(
            f"£{hasil['gbp']:,.2f}"
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "ESTIMASI HARGA DALAM RUPIAH",
                f"Rp {hasil['idr']:,.0f}"
            )

        with col2:
            st.metric(
                "ESTIMASI HARGA DALAM JUTA RUPIAH",
                f"Rp {hasil['juta']:,.2f} juta"
            )

    st.write("")

    with st.expander("Lihat spesifikasi kendaraan yang digunakan"):

        data = st.session_state.input_terakhir

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Tahun Produksi:** {data['year']}")
            st.write(f"**Jarak Tempuh:** {data['mileage']:,} miles")
            st.write(f"**Pajak:** £{data['tax']:,.2f}")

        with col2:
            st.write(f"**Konsumsi BBM:** {data['mpg']} MPG")
            st.write(f"**Kapasitas Mesin:** {data['engineSize']} Liter")

    st.info(
        "Catatan: Hasil merupakan estimasi berdasarkan model "
        "Machine Learning, bukan harga jual pasti kendaraan. "
        "Konversi mata uang menggunakan kurs tetap "
        "Rp19.000 per GBP."
    )


# =====================================================
# FOOTER
# =====================================================
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.caption("TOYOTA CAR PRICE ESTIMATOR")

with col2:
    st.caption("Powered by Machine Learning | Linear Regression")

