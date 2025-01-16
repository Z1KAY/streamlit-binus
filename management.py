import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
import os

secrets_file_path = os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml")
st.write(st.secrets)

# Database setup
conn = sqlite3.connect('customer_management.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL
)
''')
conn.commit()

# Fungsi untuk menambahkan pelanggan baru
def add_customer(name, email, phone):
    try:
        cursor.execute('''
        INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)
        ''', (name, email, phone))
        conn.commit()
        st.success(f"Pelanggan {name} berhasil ditambahkan!")
    except sqlite3.IntegrityError:
        st.error("Error: Email sudah terdaftar.")

# Fungsi untuk menampilkan daftar pelanggan
def list_customers():
    cursor.execute('SELECT * FROM customers')
    customers = cursor.fetchall()
    if customers:
        return customers
    else:
        return []

# Fungsi untuk memperbarui data pelanggan
def update_customer(customer_id, name, email, phone):
    cursor.execute('''
    UPDATE customers SET name = ?, email = ?, phone = ? WHERE id = ?
    ''', (name, email, phone, customer_id))
    conn.commit()
    st.success("Data pelanggan berhasil diperbarui!")

# Fungsi untuk menghapus pelanggan
def delete_customer(customer_id):
    cursor.execute('''
    DELETE FROM customers WHERE id = ?
    ''', (customer_id,))
    conn.commit()
    st.success("Pelanggan berhasil dihapus!")

# Fungsi untuk mengirim email promosi (diperbaiki)
def send_email_promotion(subject, message):
    # Access secrets, assuming 'my_secrets' section in secrets.toml
    sender_email = st.secrets["my_secrets"]["EMAIL"]  
    sender_password = st.secrets["my_secrets"]["PASSWORD"]

    try:
        cursor.execute('SELECT email FROM customers')
        emails = cursor.fetchall()

        if not emails:
            st.warning("Tidak ada pelanggan yang terdaftar untuk dikirim email.")
            return

        # Siapkan koneksi email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        for email in emails:
            recipient_email = email[0]
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))
            server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        st.success("Email berhasil dikirim ke semua pelanggan!")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

# Streamlit UI
st.title("Sistem Manajemen Pelanggan")

menu = st.sidebar.selectbox("Pilih Menu", ["Tambah Pelanggan", "Lihat Pelanggan", "Perbarui Pelanggan", "Hapus Pelanggan", "Kirim Email Promosi"])

if menu == "Tambah Pelanggan":
    st.header("Tambah Pelanggan Baru")
    name = st.text_input("Nama")
    email = st.text_input("Email")
    phone = st.text_input("Telepon")
    if st.button("Tambah"):
        add_customer(name, email, phone)

elif menu == "Lihat Pelanggan":
    st.header("Daftar Pelanggan")
    customers = list_customers()
    if customers:
        for customer in customers:
            st.write(f"ID: {customer[0]}, Nama: {customer[1]}, Email: {customer[2]}, Telepon: {customer[3]}")
    else:
        st.warning("Belum ada pelanggan yang terdaftar.")

elif menu == "Perbarui Pelanggan":
    st.header("Perbarui Data Pelanggan")
    customer_id = st.number_input("ID Pelanggan", min_value=1, step=1)
    name = st.text_input("Nama Baru")
    email = st.text_input("Email Baru")
    phone = st.text_input("Telepon Baru")
    if st.button("Perbarui"):
        update_customer(customer_id, name, email, phone)

elif menu == "Hapus Pelanggan":
    st.header("Hapus Pelanggan")
    customer_id = st.number_input("ID Pelanggan", min_value=1, step=1)
    if st.button("Hapus"):
        delete_customer(customer_id)

elif menu == "Kirim Email Promosi":
    st.header("Kirim Email Promosi")
    subject = st.text_input("Judul Email")
    message = st.text_area("Isi Pesan")
    if st.button("Kirim"):
            send_email_promotion(subject, message)

    email = st.secrets["ammarutbk@gmail.com"]
    password = st.secrets["Skyblockid345@."]
    sender_email = st.secrets["my_secrets"]["ammarutbk@gmail.com"]  
    sender_password = st.secrets["my_secrets"]["Skyblockid345@."]
