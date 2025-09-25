# ui_streamlit.py
import streamlit as st
import requests
import os
st.set_page_config(page_title="RAG HR Chatbot", layout="centered")
st.title("RAG HR Chatbot")

# Fixed backend URL
api_url = os.environ.get("BACKEND_URL", "http://localhost:8000/query")

# Keep chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Input box for user question
question = st.text_input("Ask a question about HR Policy")

if st.button("Send") and question.strip():
    try:
        resp = requests.post(api_url, json={"question": question})
        if resp.status_code == 200:
            data = resp.json()
            answer = data.get("answer", "No answer")
            sources = data.get("sources", [])
            st.session_state.history.append(
                {"q": question, "a": answer, "sources": sources}
            )
        else:
            st.error(f"Error {resp.status_code}: {resp.text}")
    except Exception as e:
        st.error(f"Could not reach backend: {e}")

# Display chat history
for chat in st.session_state.history[::-1]:
    st.markdown(f"**You:** {chat['q']}")
    st.markdown(f"**Bot:** {chat['a']}")
    if chat["sources"]:
        st.markdown("**Sources:** " + ", ".join(chat["sources"]))
    st.markdown("---")