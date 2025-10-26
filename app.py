import streamlit as st
import requests

st.title("RAG-Powered Web QA System")

with st.expander("📄 Index New URLs"):
    urls_input = st.text_area("Enter URLs (one per line)")
    if st.button("Index URLs"):
        urls = urls_input.strip().split("\n")
        response = requests.post("http://localhost:8000/api/v1/index", json={"urls": urls})
        st.write("Status Code:", response.status_code)
        st.write("Response:", response.json())

query = st.text_input("Ask a question based on the indexed websites")
if st.button("Submit") and query:
    response = requests.post("http://localhost:8000/api/v1/chat", json={"query": query})
    st.write("Status Code:", response.status_code)
    st.write("Raw Text:", response.text)

    try:
        data = response.json()
        if "answer" in data:
            st.markdown(data["answer"])
        else:
            st.error(data.get("error", "Unknown error"))
    except Exception as e:
        st.error(f"Error parsing response: {e}")