# src/main.py
import streamlit as st
from langgraph import decision_and_run, ingest_pdf
from config import settings
import os

st.set_page_config(page_title="LangGraph RAG Demo", layout="wide")

st.title("LangGraph + LangChain + RAG (OpenAI + FAISS)")

if "history" not in st.session_state:
    st.session_state.history = []

# Left: PDF uploader & ingest
st.sidebar.header("Docs (PDF)")
uploaded = st.sidebar.file_uploader("Upload PDF to ingest", type=["pdf"])
if uploaded:
    with open("uploaded_doc.pdf", "wb") as f:
        f.write(uploaded.getbuffer())
    count = ingest_pdf("uploaded_doc.pdf")
    st.sidebar.success(f"Ingested {count} text chunks into vector store.")

# Input area
with st.form("query_form"):
    user_q = st.text_input("Ask something (weather or ask about the uploaded PDF):")
    submitted = st.form_submit_button("Send")

if submitted and user_q:
    with st.spinner("Running..."):
        out = decision_and_run(user_q)
        st.session_state.history.append((user_q, out))

# Show history
for q, r in reversed(st.session_state.history):
    st.markdown(f"**You:** {q}")
    if r.get("mode") == "weather":
        if r.get("error"):
            st.error(r["error"])
        else:
            st.markdown(f"**Assistant (weather):** {r.get('response')}")
    else:
        st.markdown(f"**Assistant (pdf):** {r.get('response')}")
        if r.get("context"):
            with st.expander("Context from PDF"):
                for c in r["context"]:
                    st.write(c[:1000])
