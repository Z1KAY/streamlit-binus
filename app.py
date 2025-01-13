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
    
    # Menambahkan indikator ketersediaan (dengan batas 500 produk)
    total_stock = inventory['stock'].sum()
    if total_stock < 500:
        st.markdown(f"<p style='color: green;'>Gudang tersedia ({total_stock}/500)</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='color: red;'>Gudang tidak tersedia ({total_stock}/500)</p>", unsafe_allow_html=True)

def search_product(query):
    results = inventory[inventory['category'].str.contains(query, case=False)]
    if results.empty:
        st.warning("Produk tidak ditemukan.")
    else:
        st.subheader("Hasil Pencarian")
        st.dataframe(results, use_container_width=True)

def add_product(product_id, product_name, category, price, rating, stock):
    global inventory
    if product_id in inventory['product_id'].values:
        st.error(f"Produk dengan ID {product_id} sudah ada.")
        return
    new_product = {'product_id': product_id, 'product_name': product_name, 'category': category,
                   'price': price, 'rating': rating, 'stock': stock}
    inventory = pd.concat([inventory, pd.DataFrame([new_product])], ignore_index=True)
    st.success("Produk berhasil ditambahkan.")

def update_product(product_id, quantity, new_price=None, new_rating=None):
    global inventory
    inventory.loc[inventory['product_id'] == product_id, 'stock'] += quantity
    
    # Perbarui harga hanya jika new_price tidak kosong
    if new_price:  
        inventory.loc[inventory['product_id'] == product_id, 'price'] = new_price
    
    # Perbarui rating hanya jika new_rating tidak kosong
    if new_rating:  
        inventory.loc[inventory['product_id'] == product_id, 'rating'] = new_rating 

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
    elif menu_option == "Perbarui Stok":
        product_id = st.selectbox("Pilih Produk:", inventory['product_id'].unique())
        quantity = st.number_input("Masukkan jumlah stok yang ingin ditambahkan:", step=1)
        new_price = st.number_input("Masukkan harga baru (opsional):", step=1000.0)
        new_rating = st.number_input("Masukkan rating baru (opsional):", min_value=0.0, max_value=5.0, step=0.1)
        if st.button("Perbarui"):
            update_product(product_id, quantity, new_price, new_rating)
            st.success("Produk berhasil diperbarui.")
    elif menu_option == "Hapus Produk":
        product_id = st.selectbox("Pilih Produk:", inventory['product_id'].unique())
        if st.button("Hapus"):
            remove_product(product_id)

    # Menyimpan dataset ke CSV saat program selesai
    inventory.to_csv('inventory.csv', index=False)

if __name__ == "__main__":
    main()
