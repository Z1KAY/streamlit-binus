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
    })
    st.session_state.df = pd.concat([st.session_state.df, new_data], ignore_index=True)

# Tampilkan tabel
st.write(st.session_state.df)

# Opsi untuk menghapus baris
row_to_delete = st.number_input("Hapus Baris (indeks dimulai dari 0)", min_value=0, step=1, value=0)  # Default value to 0
if st.button("Hapus"):
    try:
        st.session_state.df = st.session_state.df.drop(index=row_to_delete)
        st.success(f"Baris {row_to_delete} berhasil dihapus.")
    except KeyError:
        st.error(f"Baris {row_to_delete} tidak ditemukan.")

# Tombol unduh CSV
csv = st.session_state.df.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="kalkulator_hasil.csv",
    mime="text/csv",
)
