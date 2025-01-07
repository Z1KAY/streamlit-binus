import streamlit as st
import pandas as pd

# Dataset yang berisi 30 produk
data = {
    'product_id': list(range(1, 31)),
    'product_name': [
        'Kursi Kayu', 'Meja Makan', 'Kursi Kantor', 'Rak Buku', 'Meja Kopi',
        'Sofa Recliner', 'Meja Samping', 'Kursi Makan', 'Rak TV', 'Kursi Santai',
        'Lemari Pakaian', 'Meja Belajar', 'Sofa Bed', 'Kursi Lesehan', 'Rak Dinding',
        'Meja Rias', 'Kursi Tamu', 'Lemari Penyimpanan', 'Meja Samping Modern', 'Sofa Minimalis',
        'Kursi Bar', 'Meja Kerja', 'Kursi Lipat', 'Rak Sepatu', 'Meja TV',
        'Sofa Keluarga', 'Kursi Goyang', 'Meja Makan Bulat', 'Rak Dapur', 'Kursi Santai Modern'
    ],
    'category': [
        'Kursi', 'Meja', 'Kursi', 'Rak', 'Meja',
        'Sofa', 'Meja', 'Kursi', 'Rak', 'Sofa',
        'Lemari', 'Meja', 'Sofa', 'Kursi', 'Rak',
        'Meja', 'Kursi', 'Lemari', 'Meja', 'Sofa',
        'Kursi', 'Meja', 'Kursi', 'Rak', 'Meja',
        'Sofa', 'Kursi', 'Meja', 'Rak', 'Kursi'
    ],
    'price': [
        500000, 1500000, 750000, 1000000, 800000,
        3000000, 400000, 600000, 1200000, 2000000,
        2500000, 900000, 3500000, 450000, 700000,
        1000000, 1200000, 2000000, 500000, 2800000,
        600000, 1200000, 300000, 800000, 1500000,
        3500000, 900000, 2000000, 1000000, 600000
    ],
    'rating': [
        4.5, 4.7, 4.2, 4.6, 4.3,
        4.8, 4.1, 4.4, 4.5, 4.6,
        4.7, 4.3, 4.9, 4.2, 4.5,
        4.6, 4.8, 4.1, 4.4, 4.3,
        4.7, 4.5, 4.2, 4.6, 4.4,
        4.8, 4.3, 4.5, 4.6, 4.2
    ],
    'stock': [10] * 30  # Menambahkan stok awal untuk setiap produk
}

# Membuat DataFrame dari data
inventory = pd.DataFrame(data)

def display_inventory():
    st.subheader("Daftar Inventaris")
    st.dataframe(inventory, use_container_width=True)  # Display using st.dataframe

def search_product(query):
    results = inventory[inventory['category'].str.contains(query, case=False)]
    if results.empty:
        st.warning("Produk tidak ditemukan.")
    else:
        st.subheader("Hasil Pencarian")
        st.dataframe(results, use_container_width=True)

@st.cache_data(experimental_allow_widgets=True)
def add_product(product_id, product_name, category, price, rating, stock):
    global inventory
    new_product = {'product_id': product_id, 'product_name': product_name, 'category': category,
                   'price': price, 'rating': rating, 'stock': stock}
    inventory = pd.concat([inventory, pd.DataFrame([new_product])], ignore_index=True)

@st.cache_data(experimental_allow_widgets=True)
def update_stock(product_id, quantity):
    inventory.loc[inventory['product_id'] == product_id, 'stock'] += quantity

@st.cache_data(experimental_allow_widgets=True)
def remove_product(product_id):
    global inventory
    inventory = inventory[inventory['product_id'] != product_id]
    st.success(f"Produk dengan ID {product_id} berhasil dihapus.")

def main():
    st.title("Manajemen Inventaris")

    menu_option = st.sidebar.selectbox("Pilih Opsi:",
                                      ("Tampilkan Inventaris", "Cari Produk", "Tambah Produk",
                                       "Perbarui Stok", "Hapus Produk"))

    if menu_option == "Tampilkan Inventaris":
        display_inventory()
    elif menu_option == "Cari Produk":
        query = st.text_input("Masukkan kategori produk:")
        if st.button("Cari"):
            search_product(query)
    elif menu_option == "Tambah Produk":
        product_id = st.number_input("Masukkan ID Produk:", value=inventory['product_id'].max() + 1, step=1)
        product_name = st.text_input("Masukkan Nama Produk:")
        category = st.text_input("Masukkan Kategori:")
        price = st.number_input("Masukkan Harga:", step=1000.0)
        rating = st.number_input("Masukkan Rating:", min_value=0.0, max_value=5.0, step=0.1)
        stock = st.number_input("Masukkan Jumlah Stok:", step=1)
        if st.button("Tambah"):
            add_product(product_id, product_name, category, price, rating, stock)
            st.success("Produk berhasil ditambahkan.")
    elif menu_option == "Perbarui Stok":
        product_id = st.selectbox("Pilih Produk:", inventory['product_id'].unique())
        quantity = st.number_input("Masukkan jumlah stok yang ingin ditambahkan:", step=1)
        if st.button("Perbarui"):
            update_stock(product_id, quantity)
            st.success("Stok berhasil diperbarui.")
    elif menu_option == "Hapus Produk":
        product_id = st.selectbox("Pilih Produk:", inventory['product_id'].unique())
        if st.button("Hapus"):
            remove_product(product_id)

st.cache_data.clear()
if __name__ == "__main__":
    main()
