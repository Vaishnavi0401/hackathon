import os
import pandas as pd
from datetime import datetime
import uuid
import streamlit as st

def create_order(validated_products, delivery_requirements, catalog_df):
    """
    Create an order and update product quantities
    
    Args:
        validated_products (list): List of validated product dictionaries
        delivery_requirements (str): Delivery requirements for the order
        catalog_df (DataFrame): Product catalog DataFrame
    
    Returns:
        tuple: (order_id, order_records) or (None, None) if error
    """
    try:
        # Generate a unique order ID
        order_id = str(uuid.uuid4())[:8]
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create order records
        order_records = []
        for product in validated_products:
            # Find the product in catalog
            product_row = catalog_df[catalog_df['Product_Name'] == product['product_name']].iloc[0]
            
            # Create order record
            order_record = {
                'Order_ID': order_id,
                'Order_Date': order_date,
                # 'Product_Code': product_row['Product_Code'],
                'Product_Name': product_row['Product_Name'],
                'Quantity': product['quantity'],
                'Delivery_Requirements': delivery_requirements,
                'Description': product['description']
            }
            order_records.append(order_record)
            
            # Update product quantity in catalog
            catalog_df.loc[catalog_df['Product_Code'] == product_row['Product_Code'], 'Available_in_Stock'] -= product['quantity']
        
        # Create or append to orders.csv
        orders_df = pd.DataFrame(order_records)
        if os.path.exists('orders.csv'):
            orders_df.to_csv('orders.csv', mode='a', header=False, index=False)
        else:
            orders_df.to_csv('orders.csv', index=False)
        
        # Update product catalog
        catalog_df.to_csv('product_catalog.csv', index=False)
        
        return order_id, order_records
        
    except Exception as e:
        st.error(f"Error creating order: {e}")
        return None, None 