import streamlit as st
import openai
import os

# ---- Setup ----
st.set_page_config(page_title="AI Hackathon App", layout="centered")

st.title("🚀 AI Hackathon App Template")

# ---- API Key Input ----
openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")

# ---- User Input ----
user_input = st.text_area("Ask something or give a command:")

# ---- Submit Button ----
submit = st.button("Run AI")

# ---- Response Output ----
if submit and openai_api_key and user_input:
    with st.spinner("Thinking..."):
        try:
            openai.api_key = openai_api_key
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input},
                ]
            )
            output = response["choices"][0]["message"]["content"]
            st.success("Done!")
            st.markdown("### 💡 AI Response:")
            st.write(output)
        except Exception as e:
            st.error(f"Error: {e}")

# ---- Sidebar ----
st.sidebar.title("App Controls")
st.sidebar.info("You can customize this app to handle specific tasks like summarizing, answering questions, etc.")

# ---- Footer ----
st.markdown("---")
st.markdown("Made for Hackathons with ❤️ using Streamlit and OpenAI")
