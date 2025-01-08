import streamlit as st
import pandas as pd

st.title("Kalkulator Biaya Produksi, Harga Jual, dan Keuntungan")

# Pertama, input biaya produksi
biaya_produksi = st.number_input("Biaya Produksi (Rp)", min_value=0.0, format="%.2f")

# Kedua, input markup (auto dalam persentase)
markup = st.number_input("Markup (%)", min_value=0.0, format="%.2f")

# Ketiga, hitung harga jual dan keuntungan
harga_jual = biaya_produksi + (biaya_produksi * (markup / 100))
keuntungan = harga_jual - biaya_produksi

# Hasil
st.write("Harga Jual: Rp {:,.2f}".format(harga_jual))
st.write("Keuntungan: Rp {:,.2f}".format(keuntungan))

# Dataframe ini
data = {
    "Biaya Produksi": [biaya_produksi],
    "Markup (%)": [markup],
    "Harga Jual": [harga_jual],
    "Keuntungan": [keuntungan],
}
df = pd.DataFrame(data)

st.write(df)

# Download le
csv = df.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="kalkulator_hasil.csv",
    mime="text/csv",
)
