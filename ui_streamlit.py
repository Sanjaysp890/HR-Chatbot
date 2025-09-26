# ui_streamlit.py
import streamlit as st
import requests
import os

st.set_page_config(page_title="RAG HR Chatbot", layout="centered")

# Title & subtitle
st.title("RAG HR Chatbot")
st.write("Ask a question about the HR Policy (the bot answers only from the uploaded policy).")

# Backend URL
api_url = os.environ.get("BACKEND_URL", "http://localhost:8000/query")

# Keep chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Input row for user question
col1, col2 = st.columns([4, 1])
with col1:
    question = st.text_input("e.g. How many paid leaves are there?", label_visibility="collapsed")
with col2:
    send = st.button("Send")

if send and question.strip():
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

# Collapsible PDF upload section
with st.expander("(Optional) Upload a PDF to index locally (developer only)"):
    uploaded_file = st.file_uploader(
        "Upload PDF", type=["pdf"], accept_multiple_files=False
    )
    if uploaded_file:
        st.info(f"Uploaded: {uploaded_file.name}")
    if st.button("Ingest uploaded docs (run ingest.py)"):
        if uploaded_file:
            # Save uploaded file to data/ folder for ingest.py
            save_path = os.path.join("data", uploaded_file.name)
            os.makedirs("data", exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Saved {uploaded_file.name} to {save_path}. Run ingest.py to index it.")
        else:
            st.warning("Please upload a PDF first.")

# Display chat history
for chat in st.session_state.history[::-1]:
    st.markdown(f"**You:** {chat['q']}")
    st.markdown(f"**Bot:** {chat['a']}")
    if chat["sources"]:
        st.markdown("**Sources:** " + ", ".join(chat["sources"]))
    st.markdown("---")
