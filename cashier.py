import streamlit as st
import pandas as pd

# Load the inventory CSV file
inventory = pd.read_csv('inventory.csv')

# Function to update the inventory CSV
def update_inventory(updated_inventory):
    updated_inventory.to_csv('inventory.csv', index=False)

# Cashier app interface
st.title("Cashier App")

# Get customer items
customer_items = st.text_input("Enter customer items (comma-separated product IDs):")

if customer_items:
    # Split items into a list
    items_list = [int(item.strip()) for item in customer_items.split(',')]

    # Create a DataFrame for customer items
    customer_df = pd.DataFrame({'product_id': items_list})

    # Merge customer items with inventory to get prices and update stock
    merged_df = pd.merge(customer_df, inventory, on='product_id', how='left')

    # Calculate total price
    total_price = merged_df['price'].sum()

    # Update inventory stock
    for product_id in items_list:
        inventory.loc[inventory['product_id'] == product_id, 'stock'] -= 1

    # Display customer items, total price, and updated inventory
    st.subheader("Customer Items")
    st.dataframe(merged_df[['product_id', 'product_name', 'price']], use_container_width=True)
    st.write(f"Total Price: {total_price}")
    st.subheader("Updated Inventory")
    st.dataframe(inventory, use_container_width=True)

    # Update the inventory CSV file
    update_inventory(inventory)