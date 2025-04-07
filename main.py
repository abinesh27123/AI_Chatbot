import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Read the API key from .env or Streamlit secrets
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# Streamlit UI setup
st.title("🤖 AI Friend")
st.markdown("Chat with your AI assistant powered by Gemini!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

# Chat input box
user_input = st.chat_input("Type your message here...")

# If user sends a message
if user_input:
    # Append and display user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_input)

    # Generate and display AI response
    try:
        response = model.generate_content(user_input)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"❌ Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(bot_reply)
