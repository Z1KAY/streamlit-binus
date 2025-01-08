import streamlit as st
import pandas as pd

st.title("Profit Counter Calculator")

# Inisialisasi session state untuk menyimpan data tabel
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Nama", "Biaya Produksi", "Markup (%)", "Harga Jual", "Keuntungan"])

# Input nama
nama = st.text_input("Nama Produk")

# Input biaya produksi
biaya_produksi = st.number_input("Biaya Produksi (Rp)", min_value=0.0, format="%.2f")

# Input markup (dalam persentase)
markup = st.number_input("Markup (%)", min_value=0.0, format="%.2f")

# Hitung harga jual dan keuntungan
harga_jual = biaya_produksi + (biaya_produksi * (markup / 100))
keuntungan = harga_jual - biaya_produksi

# Tambahkan data ke tabel jika tombol "Add" ditekan
if st.button("Add"):
    new_data = pd.DataFrame({
        "Nama": [nama],
        "Biaya Produksi": [biaya_produksi],
        "Markup (%)": [markup],
        "Harga Jual": [harga_jual],
        "Keuntungan": [keuntungan],
        "Pilih": [False],  # Inisialisasi kolom "Pilih" dengan False
    })
    st.session_state.df = pd.concat([st.session_state.df, new_data], ignore_index=True)

# Menampilkan tabel dengan checkbox di sebelah kolom "Keuntungan"
displayed_df = st.session_state.df[["Nama", "Biaya Produksi", "Markup (%)", "Harga Jual", "Keuntungan"]].copy()  # Salin DataFrame untuk ditampilkan
for index in st.session_state.df.index:
    # Checkbox untuk memilih baris
    st.session_state.df.loc[index, "Pilih"] = st.checkbox("Pilih", key=f"checkbox_{index}", value=st.session_state.df.loc[index, "Pilih"])

st.write(displayed_df) # Tampilkan DataFrame tanpa kolom "Pilih"

# Menampilkan tombol "Hapus" jika ada baris yang dipilih
if any(st.session_state.df["Pilih"]):
    if st.button("Hapus yang dipilih"):
        indexes_to_delete = st.session_state.df[st.session_state.df["Pilih"]].index
        st.session_state.df = st.session_state.df.drop(indexes_to_delete)
        st.rerun()

# Tombol unduh CSV
csv = st.session_state.df.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="kalkulator_hasil.csv",
    mime="text/csv",
)
)
