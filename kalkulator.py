import streamlit as st
import pandas as pd

st.title("Kalkulator Biaya Produksi, Harga Jual, dan Keuntungan")

# Input biaya produksi
biaya_produksi = st.number_input("Biaya Produksi (Rp)", min_value=0.0, format="%.2f")

# Input markup (dalam persentase)
markup = st.number_input("Markup (%)", min_value=0.0, format="%.2f")

# Hitung harga jual dan keuntungan
harga_jual = biaya_produksi + (biaya_produksi * (markup / 100))
keuntungan = harga_jual - biaya_produksi

# Tampilkan hasil dengan format mata uang rupiah
st.write("Harga Jual: Rp {:,.2f}".format(harga_jual))
st.write("Keuntungan: Rp {:,.2f}".format(keuntungan))

# Buat DataFrame untuk hasil
data = {
    "Biaya Produksi": [biaya_produksi],
    "Markup (%)": [markup],
    "Harga Jual": [harga_jual],
    "Keuntungan": [keuntungan],
}
df = pd.DataFrame(data)

# Tampilkan DataFrame
st.write(df)

# Tombol unduh CSV
csv = df.to_csv(index=False)
st.download_button(
    label="Unduh CSV",
    data=csv,
    file_name="kalkulator_hasil.csv",
    mime="text/csv",
)