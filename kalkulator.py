import streamlit as st
import pandas as pd

st.title("Profit Counter Calculator")

# Inisialisasi session state untuk menyimpan data tabel
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Nama", "Biaya Produksi", "Markup (%)", "Harga Jual", "Keuntungan", "Pajak"])

# Input nama
nama = st.text_input("Nama Produk")

# Input biaya produksi
biaya_produksi = st.number_input("Biaya Produksi (Rp)", min_value=0.0, format="%.2f")

# Input markup (dalam persentase)
markup = st.number_input("Markup (%)", min_value=0.0, format="%.2f")

# Input pajak jika biaya produksi <= 4.8 miliar
if biaya_produksi <= 4800000000:
    pajak = st.checkbox("Pajak 0,5% (hanya jika biaya produksi <= 4,8 miliar)")
else:
    pajak = False  # Pajak tidak berlaku jika biaya produksi > 4,8 miliar

# Hitung harga jual dan keuntungan
if pajak:
    harga_jual = biaya_produksi + (biaya_produksi * (markup / 100)) + (biaya_produksi * 0.005)  # Tambahkan pajak 0,5%
    keuntungan = harga_jual - biaya_produksi - (biaya_produksi * 0.005)  # Kurangi pajak dari keuntungan
    pajak_rp = biaya_produksi * 0.005 # Hitung nilai pajak dalam rupiah
else:
    harga_jual = biaya_produksi + (biaya_produksi * (markup / 100))
    keuntungan = harga_jual - biaya_produksi
    pajak_rp = 0  # Pajak 0 jika tidak berlaku

# Tambahkan data ke tabel jika tombol "Add" ditekan
if st.button("Add"):
    new_data = pd.DataFrame({
        "Nama": [nama],
        "Biaya Produksi": [biaya_produksi],
        "Markup (%)": [markup],
        "Harga Jual": [harga_jual],
        "Keuntungan": [keuntungan],
        "Pajak": [pajak_rp], # tambahkan kolom pajak
    })
    st.session_state.df = pd.concat([st.session_state.df, new_data], ignore_index=True)

# Tampilkan tabel
st.write(st.session_state.df)

# Tampilkan tabel
st.write(st.session_state.df)

# Opsi untuk menghapus baris
row_to_delete = st.number_input("Hapus Baris (indeks dimulai dari 0)", min_value=0, step=1, value=0) 
if st.button("Hapus"):
    try:
        st.session_state.df = st.session_state.df.drop(index=row_to_delete)
        st.success(f"Baris {row_to_delete} berhasil dihapus.")
        st.rerun() # Menjalankan ulang skrip untuk memperbarui UI
    except KeyError:
        st.error(f"Baris {row_to_delete} tidak ditemukan.")

# Laporan sederhana
st.write(f"Total Biaya Produksi: {st.session_state.df['Biaya Produksi'].sum():,.2f}")
st.write(f"Total Harga Jual: {st.session_state.df['Harga Jual'].sum():,.2f}")
st.write(f"Total Keuntungan: {st.session_state.df['Keuntungan'].sum():,.2f}")

# Tombol unduh CSV
csv = st.session_state.df.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="kalkulator_hasil.csv",
    mime="text/csv",
)
