import streamlit as st
import pandas as pd

# Fungsi untuk membaca dataset dari CSV dan menghapus kolom 'Unnamed: 0'
def load_inventory():
    try:
        inventory = pd.read_csv('inventory.csv')
        inventory = inventory.drop(columns=['Unnamed: 0'], errors='ignore')  # Hapus kolom 'Unnamed: 0' jika ada
    except FileNotFoundError:
        st.error("File 'inventory.csv' tidak ditemukan. Pastikan file tersebut ada di direktori yang sama dengan notebook ini.")
        return pd.DataFrame()  # Mengembalikan DataFrame kosong jika file tidak ditemukan
    return inventory

# Memuat dataset saat program dimulai
inventory = load_inventory()

def display_inventory():
    st.subheader("Daftar Inventaris")
    st.dataframe(inventory, use_container_width=True)  

def search_product(query):
    results = inventory[inventory['category'].str.contains(query, case=False)]
    if results.empty:
        st.warning("Produk tidak ditemukan.")
    else:
        st.subheader("Hasil Pencarian")
        st.dataframe(results, use_container_width=True)

def add_product(product_id, product_name, category, price, rating, stock):
    global inventory
    new_product = {'product_id': product_id, 'product_name': product_name, 'category': category,
                   'price': price, 'rating': rating, 'stock': stock}
    inventory = pd.concat([inventory, pd.DataFrame([new_product])], ignore_index=True)

def update_stock(product_id, quantity):
    inventory.loc[inventory['product_id'] == product_id, 'stock'] += quantity

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
        product_id = st.number_input("Masukkan ID Produk:", value=inventory['product_id'].max() + 1 if not inventory.empty else 1, step=1)
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

    # Menyimpan dataset ke CSV saat program selesai
    inventory.to_csv('inventory.csv', index=False)

if __name__ == "__main__":
    main()
