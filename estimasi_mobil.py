
import pickle
import streamlit as st
import numpy as np

# Memuat model
with open('estimasi_mobil.sav', 'rb') as file:
    model = pickle.load(file)

# Judul aplikasi
st.title('Estimasi Harga Mobil Bekas')
st.write('Masukkan spesifikasi mobil untuk memperkirakan harganya.')

# Input data mobil
year = st.number_input('Input Tahun Mobil', min_value=1990, max_value=2026, value=2019)
mileage = st.number_input('Input Km Mobil', min_value=0, value=5000)
tax = st.number_input('Input Pajak Mobil', min_value=0, value=145)
mpg = st.number_input('Input Konsumsi BBM Mobil', min_value=0.0, value=30.2)
engineSize = st.number_input('Input Engine Size', min_value=0.0, value=2.0)

# Nilai tukar GBP ke IDR (contoh asumsi)
kurs = 19000

# Tombol estimasi
if st.button('Estimasi Harga'):

    # Prediksi harga dalam Pounds
    input_data = np.array([[year, mileage, tax, mpg, engineSize]])
    predict = model.predict(input_data)[0]

    # Konversi ke Rupiah
    harga_idr = predict * kurs

    # Konversi ke juta Rupiah
    harga_juta = harga_idr / 1000000

    # Menampilkan hasil
    st.success('Hasil Estimasi Harga Mobil')

    st.write(f'Estimasi harga dalam Pounds: £{predict:,.2f}')
    st.write(f'Estimasi harga dalam Rupiah: Rp{harga_idr:,.0f}')
    st.write(f'Estimasi harga dalam Juta Rupiah: Rp{harga_juta:,.2f} juta')

