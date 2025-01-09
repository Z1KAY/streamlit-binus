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

# --- Perubahan 1: Tambahkan kolom "Actions" dan tombol "Hapus" ---
st.session_state.df['Actions'] = st.session_state.df.index.map(lambda x: st.button("Hapus", key=f"delete_{x}"))

# Tampilkan tabel
st.write(st.session_state.df)

# Opsi untuk menghapus baris
for index in st.session_state.df.index:
    if st.session_state.get(f"delete_{index}"):
        st.session_state.df = st.session_state.df.drop(index=index)
        st.experimental_rerun()
        break

# Fungsi untuk menghasilkan laporan
def generate_report(df):
    total_biaya_produksi = df["Biaya Produksi"].sum()
    total_harga_jual = df["Harga Jual"].sum()
    total_keuntungan = df["Keuntungan"].sum()

    report = f"""
    ## Laporan Hasil Perhitungan

    **Total Biaya Produksi:** Rp {total_biaya_produksi:,.2f}
    **Total Harga Jual:** Rp {total_harga_jual:,.2f}
    **Total Keuntungan:** Rp {total_keuntungan:,.2f}
    """
    return report

# Tampilkan laporan
st.markdown(generate_report(st.session_state.df))


# Tombol unduh CSV
csv = st.session_state.df.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="kalkulator_hasil.csv",
    mime="text/csv",
)
