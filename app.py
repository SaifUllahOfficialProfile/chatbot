import streamlit as st
import requests

# FastAPI backend URL
BACKEND_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="centered")

st.title("Gemini Chatbot")
st.caption("Powered by FastAPI + Gemini")

# Initialize chat history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("Type your message...")

if prompt:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send request to backend
    try:
        response = requests.post(
            BACKEND_URL,
            json={"message": prompt},
            timeout=60
        )
        response.raise_for_status()
        bot_reply = response.json()["response"]

    except requests.exceptions.RequestException as e:
        bot_reply = f"Error communicating with backend: {e}"

    # Show assistant response
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
