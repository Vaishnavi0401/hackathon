# get the possible products from the email text and return the product codes in a list
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st
import json
from validate_order import validate_response
import pandas as pd
from datetime import datetime
import uuid
from order import create_order
# Load the product catalog
catalog_df = pd.read_csv("product_catalog.csv")

# Load environment variables at the start
load_dotenv()

# Initialize OpenAI
CHAT_GPT_API_KEY = os.getenv("OPENAI_API_KEY")

def get_relevant_products(email_text):
    """
    Process email text to extract product information using LangChain
    """
    try:
        # Initialize the LLM
        llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            max_tokens=1000,
            api_key=CHAT_GPT_API_KEY
        )

        # Define the prompt template
        PROMPT_TEMPLATE = """You are a product information extractor. Analyze the following email text and extract product information in a structured format:

        {email_text}

        Extract the following information for each product mentioned:
        1. Product Name
        2. Quantity
        3. Description (if available)
        4. Delivery requirements (if mentioned)

        Return a text mentioning the product name, quantity and delivery requirements.
        """

        prompt_template = PromptTemplate(
            input_variables=["email_text"],
            template=PROMPT_TEMPLATE
        )

        # Create and run the chain
        chain = LLMChain(llm=llm, prompt=prompt_template)
        response = chain.invoke({"email_text": email_text})
        
        # Display the extracted information
        st.write("Extracted Information:")
        st.write(response['text'])
        
        # Validate the response against the catalog
        validated_products = validate_response(response['text'], catalog_df)
        
        if validated_products:
            # Extract delivery requirements from the response
            delivery_requirements = "Standard delivery"  # Default value
            if "delivery" in response['text'].lower():
                delivery_requirements = response['text'].split("delivery")[-1].strip()
            
            # Create the order
            order_id, order_records = create_order(validated_products, delivery_requirements, catalog_df=catalog_df)
            
            if order_id:
                st.success(f"Order created successfully! Order ID: {order_id}")
                st.markdown("### 📋 Order Details")
                st.json(order_records)
                
                # Show updated product quantities
                st.markdown("### 📊 Updated Product Quantities")
                st.dataframe(catalog_df[['Product_Code', 'Product_Name', 'Quantity']])
            else:
                st.error("Failed to create order")
        else:
            st.error("No valid products found in the order")

    except Exception as e:
        st.error(f"Error processing email text: {e}")
        return None

