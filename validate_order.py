import pandas as pd
import streamlit as st

catalog_df = pd.read_csv("product_catalog.csv")

def validate_response(requested_products, catalog_df):

    #Assuming we get the response in a list of dictionaries with the fields product_name, quantity, description, delivery_requirements 
    requested_products = [
    {
        "product_name": "Desk TRÄNHOLM 19",
        "description": "Not available",
        "quantity": 8,
        "delivery_requirements": "Deliver to 2-11-3 Meguro, Tokyo, Japan before June 18, 2025"
    },
    {
        "product_name": "Desk NORDMARK 476",
        "description": "Not available",
        "quantity": 1,
        "delivery_requirements": "Deliver to 2-11-3 Meguro, Tokyo, Japan before June 18, 2025"
    },
    {
        "product_name": "Desk VIKTSTA 642",
        "description": "Not available",
        "quantity": 3,
        "delivery_requirements": "Deliver to 2-11-3 Meguro, Tokyo, Japan before June 18, 2025"
    }
    ]

    validated = []

    for product in requested_products:
        name = product["product_name"]
        qty_requested = product["quantity"]

        match = catalog_df[catalog_df["Product_Name"].str.lower() == name.lower()]

        if match.empty:
            validated.append({**product, "status": "❌ SKU not found"})
            continue

        row = match.iloc[0]
        moq = row["Min_Order_Quantity"]
        inventory = row["Available_in_Stock"]

        if qty_requested < moq:
            validated.append({**product, "status": f"❌ Below MOQ ({moq})"})
        elif qty_requested > inventory:
            validated.append({**product, "status": f"❌ Insufficient inventory (only {inventory} available)"})
        else:
            validated.append({**product, "status": "✅ Valid"})

   
    
    return validated

    