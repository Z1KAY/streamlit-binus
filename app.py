import streamlit as st
import pandas as pd
import requests
from io import StringIO

CSV_URL = "your_raw_csv_url_here" # Ganti dengan URL raw file CSV Anda

@st.cache_resource(hash_funcs={pd.DataFrame: lambda _: None})
def load_data(csv_url):
    response = requests.get(csv_url)
    response.raise_for_status()
    inventory = pd.read_csv(StringIO(response.text))
    return inventory

def save_data(inventory, csv_url):
    csv_buffer = StringIO()
    inventory.to_csv(csv_buffer, index=False)
    # Gunakan requests atau GitPython untuk menyimpan csv_buffer ke csv_url di GitHub

inventory = load_data(CSV_URL)

st.title("Manajemen Inventaris")
st.dataframe(inventory)

with st.form("add_product_form"):
    st.write("Tambah Produk Baru")
    product_id = st.number_input("ID Produk:", value=inventory['product_id'].max() + 1)
    product_name = st.text_input("Nama Produk:")
    category = st.text_input("Kategori:")
    price = st.number_input("Harga:")
    rating = st.number_input("Rating:")
    stock = st.number_input("Stok:")
    submitted = st.form_submit_button("Tambah")
    if submitted:
        new_product = {'product_id': product_id, 'product_name': product_name, 'category': category,
                        'price': price, 'rating': rating, 'stock': stock}
        inventory = pd.concat([inventory, pd.DataFrame([new_product])], ignore_index=True)
        # Panggil save_data() untuk menyimpan inventory ke file CSV di GitHub
        # save_data(inventory, CSV_URL)
        st.success("Produk berhasil ditambahkan!")
        st.cache_resource.clear() # Hapus cache agar data diperbarui
        st.experimental_rerun()

if __name__ == "__main__":
    main()
