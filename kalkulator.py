import streamlit as st
import pandas as pd

st.title("Profit Counter Calculator")

# Inisialisasi session state untuk menyimpan data tabel
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Nama", "Biaya Produksi", "Markup (%)", "Harga Jual", "Keuntungan", "Pajak", "Jumlah Produk"])

# Hitung total biaya produksi
total_biaya_produksi = st.session_state.df['Biaya Produksi'].sum()

# Input pajak jika total biaya produksi <= 4.8 miliar
if total_biaya_produksi <= 4800000000:
    pajak_aktif = st.checkbox("Pajak 0,5% (hanya jika total biaya produksi <= 4,8 miliar)")
else:
    pajak_aktif = False  # Pajak tidak berlaku jika total biaya produksi > 4,8 miliar

# Input nama
nama = st.text_input("Nama Produk")

# Input biaya produksi
biaya_produksi = st.number_input("Biaya Produksi (Rp)", min_value=0.0, format="%.2f")

# Input markup (dalam persentase)
markup = st.number_input("Markup (%)", min_value=0.0, format="%.2f")

# Input jumlah produk
jumlah_produk = st.number_input("Jumlah Produk", min_value=1, step=1)

# Hitung harga jual dan keuntungan
if pajak_aktif:
    harga_jual = biaya_produksi + (biaya_produksi * (markup / 100)) + (biaya_produksi * 0.005)
    keuntungan = harga_jual - biaya_produksi - (biaya_produksi * 0.005)
    pajak_rp = biaya_produksi * 0.005
else:
    harga_jual = biaya_produksi + (biaya_produksi * (markup / 100))
    keuntungan = harga_jual - biaya_produksi
    pajak_rp = 0

# Hitung biaya produksi per produk
biaya_per_produk = biaya_produksi / jumlah_produk if jumlah_produk > 0 else 0

# Tambahkan data ke tabel jika tombol "Add" ditekan
if st.button("Add"):
    new_data = pd.DataFrame({
        "Nama": [nama],
        "Biaya Produksi": [biaya_produksi],
        "Markup (%)": [markup],
        "Harga Jual": [harga_jual],
        "Keuntungan": [keuntungan],
        "Pajak": [pajak_rp],
        "Jumlah Produk": [jumlah_produk],
        # "Biaya per Produk": [biaya_per_produk],  # Hapus baris ini
    })
    st.session_state.df = pd.concat([st.session_state.df, new_data], ignore_index=True)

# Tampilkan tabel pertama (tanpa kolom "Biaya per Produk")
st.write(st.session_state.df[["Nama", "Biaya Produksi", "Markup (%)", "Harga Jual", "Keuntungan", "Pajak", "Jumlah Produk"]])

# Tabel biaya produksi per produk
biaya_per_produk_df = st.session_state.df[["Nama", "Biaya Produksi", "Jumlah Produk"]]
biaya_per_produk_df["Biaya per Produk"] = biaya_per_produk_df["Biaya Produksi"] / biaya_per_produk_df["Jumlah Produk"]
biaya_per_produk_df = biaya_per_produk_df[["Nama", "Biaya per Produk"]]
st.write("Biaya Produksi per Produk:")
st.write(biaya_per_produk_df)

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
st.write(f"Total Biaya Produksi: Rp {st.session_state.df['Biaya Produksi'].sum():,.2f}")
st.write(f"Total Harga Jual: Rp {st.session_state.df['Harga Jual'].sum():,.2f}")
st.write(f"Total Keuntungan: Rp {st.session_state.df['Keuntungan'].sum():,.2f}")
st.write(f"Total Pajak: Rp {st.session_state.df['Pajak'].sum():,.2f}")
st.write(f"Total Jumlah Produk: {st.session_state.df['Jumlah Produk'].sum()}") 

# Tombol unduh CSV
csv = st.session_state.df.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="kalkulator_hasil.csv",
    mime="text/csv",
)
