# import streamlit as st
# import openai
# import os
# from dotenv import load_dotenv
# import psycopg2
# from psycopg2 import Error

# # Load environment variables
# load_dotenv()

# # ---- Setup ----
# st.set_page_config(page_title="AI Hackathon App", layout="centered")

# st.title("🚀 AI Hackathon App Template")

# # Get API key from environment variable
# openai_api_key = os.getenv("OPENAI_API_KEY")

# if not openai_api_key:
#     st.error("Please set your OPENAI_API_KEY in the .env file")
#     st.stop()

# # Database connection function
# def get_db_connection():
#     try:
#         connection = psycopg2.connect(
#             host=os.getenv("DB_HOST", "localhost"),
#             database=os.getenv("DB_NAME"),
#             user=os.getenv("DB_USER"),
#             password=os.getenv("DB_PASSWORD"),
#             port=os.getenv("DB_PORT", "5432")
#         )
#         return connection
#     except Error as e:
#         st.error(f"Error connecting to PostgreSQL: {e}")
#         return None

# # Test database connection
# def test_db_connection():
#     conn = get_db_connection()
#     if conn:
#         try:
#             cursor = conn.cursor()
#             cursor.execute("SELECT version();")
#             db_version = cursor.fetchone()
#             st.sidebar.success(f"Connected to PostgreSQL: {db_version[0]}")
#             cursor.close()
#             conn.close()
#             return True
#         except Error as e:
#             st.sidebar.error(f"Database error: {e}")
#             return False
#     return False

# # ---- User Input ----
# user_input = st.text_area("Ask something or give a command:")

# # ---- Submit Button ----
# submit = st.button("Run AI")

# # ---- Response Output ----
# if submit and user_input:
#     with st.spinner("Thinking..."):
#         try:
#             openai.api_key = openai_api_key
#             response = openai.ChatCompletion.create(
#                 model="gpt-4",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {"role": "user", "content": user_input},
#                 ]
#             )
#             output = response["choices"][0]["message"]["content"]
#             st.success("Done!")
#             st.markdown("### 💡 AI Response:")
#             st.write(output)
#         except Exception as e:
#             st.error(f"Error: {e}")

# # ---- Sidebar ----
# st.sidebar.title("App Controls")
# st.sidebar.info("You can customize this app to handle specific tasks like summarizing, answering questions, etc.")

# # Test database connection
# test_db_connection()

# # ---- Footer ----
# st.markdown("---")
# st.markdown("Made for Hackathons with ❤️ using Streamlit and OpenAI")
