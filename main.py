import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables (for local dev)
load_dotenv()

# Read the API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# Streamlit UI
st.title("🤖 AI Friend")
st.markdown("Chat with your AI assistant")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your message here...")
if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_input)
    
    # Get AI response
    response = model.generate_content(user_input)
    bot_reply = response.text
    
    # Display AI response
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(bot_reply)