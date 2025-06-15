import streamlit as st
import openai
import os
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
import pandas as pd
from chromadb.utils import embedding_functions
from text_process import get_relevant_products
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from order import create_order

# Load environment variables
load_dotenv()

# ---- Setup ----
st.set_page_config(page_title="Product Catalog Search", layout="centered")

st.title("🔍 Product Catalog Search")

# Get API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("Please set your OPENAI_API_KEY in the .env file")
    st.stop()

# Initialize OpenAI embedding function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_api_key,
    model_name="text-embedding-ada-002"
)

# Initialize ChromaDB client with OpenAI embeddings
chroma_client = chromadb.Client(Settings(
    persist_directory="chroma_db",
    anonymized_telemetry=False
))

# Create or get collection with OpenAI embeddings
collection = chroma_client.get_or_create_collection(
    name="product_catalog",
    embedding_function=openai_ef,
    metadata={"hnsw:space": "cosine"}
)

def process_csv_to_chromadb():
    """Process CSV file and add products to ChromaDB"""
    try:
        # Read CSV file
        df = pd.read_csv('Product_Catalog.csv')
        
        # Ensure required columns exist
        required_columns = ['Product_Code', 'Product_Name', 'Description']
        if not all(col in df.columns for col in required_columns):
            st.error(f"CSV must contain these columns: {', '.join(required_columns)}")
            return False
        
        # Convert DataFrame to list of documents
        documents = []
        metadatas = []
        ids = []
        
        for idx, row in df.iterrows():
            # Create a formatted document with the specific fields
            doc = f"Product_Code: {row['Product_Code']}\nProduct_Name: {row['Product_Name']}\nDescription: {row['Description']}"
            documents.append(doc)
            
            # Store metadata with the original values
            metadata = {
                "Product_Code": str(row['Product_Code']),
                "Product_Name": str(row['Product_Name']),
                "Description": str(row['Description'])
            }
            metadatas.append(metadata)
            ids.append(f"product_{row['Product_Code']}")
        
        # Add to ChromaDB
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        st.success(f"Successfully added {len(documents)} products to ChromaDB")
        return True
        
    except Exception as e:
        st.error(f"Error processing CSV and adding to ChromaDB: {e}")
        return False

def display_chromadb_contents():
    """Display all contents from ChromaDB collection"""
    try:
        # Get all data from the collection
        results = collection.get()
        
        if not results['ids']:
            st.info("No data in ChromaDB collection yet.")
            return
        
        # Create a DataFrame for better display
        data = []
        for i in range(len(results['ids'])):
            data.append({
                'ID': results['ids'][i],
                'Document': results['documents'][i],
                'Product Code': results['metadatas'][i]['product_code'],
                'Product Name': results['metadatas'][i]['product_name'],
                'Description': results['metadatas'][i]['description']
            })
        
        df = pd.DataFrame(data)
        
        # Display the data
        st.markdown("### 📊 ChromaDB Contents")
        st.dataframe(df)
        
        # Display some statistics
        st.markdown("### 📈 Collection Statistics")
        st.write(f"Total number of products: {len(results['ids'])}")
        
    except Exception as e:
        st.error(f"Error displaying ChromaDB contents: {e}")

# ---- Sidebar ----
st.sidebar.title("Controls")

# Add button to process CSV
if st.sidebar.button("Process CSV and Add to ChromaDB"):
    with st.spinner("Processing CSV and adding to ChromaDB..."):
        process_csv_to_chromadb()

# Add button to view ChromaDB contents
if st.sidebar.button("View ChromaDB Contents"):
    display_chromadb_contents()

# ---- Search Interface ----
st.markdown("### 🔍 Search Products")
search_query = st.text_input("Enter your search query:")

if search_query:
    llm_response = get_relevant_products(search_query)
    print(search_query)
    
   
        # Search in ChromaDB
    #     results = collection.query(
    #         query_texts=[search_query],
    #         n_results=5
    #     )
        
    #     st.markdown("### 📋 Search Results")
    #     for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
    #         st.markdown(f"#### Product {i+1}")
    #         st.write(f"**Product Code:** {metadata['product_code']}")
    #         st.write(f"**Product Name:** {metadata['product_name']}")
    #         st.write(f"**Description:** {metadata['description']}")
    #         st.markdown("---")
            
    # except Exception as e:
    #     st.error(f"Error searching products: {e}")



# ---- Footer ----
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and ChromaDB")
