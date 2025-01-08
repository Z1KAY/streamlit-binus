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

# Tambahkan kolom "Actions" dan tombol "Hapus" (Dimodifikasi)
for index in st.session_state.df.index:
    # Checkbox untuk mengaktifkan/menonaktifkan baris
    checked = st.checkbox("Pilih", key=f"checkbox_{index}", value=st.session_state.df.loc[index, "Pilih"])
    st.session_state.df.loc[index, "Pilih"] = checked

    # Tombol "Hapus" hanya muncul jika baris diaktifkan
    if checked:
        if st.button("Hapus", key=f"delete_{index}"):
            st.session_state.df = st.session_state.df.drop(index=index)
            st.rerun()

# Tampilkan tabel dengan kolom Actions
st.write(st.session_state.df[["Nama", "Biaya Produksi", "Markup (%)", "Harga Jual", "Keuntungan"]])  # Sembunyikan kolom "Pilih"

# Tombol unduh CSV
csv = st.session_state.df.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="kalkulator_hasil.csv",
    mime="text/csv",
)
