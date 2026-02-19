# RAG Agent Application
import streamlit as st
import rag_helper
import os

st.set_page_config(page_title="RAG Agent 🤖", layout="wide")

st.title("Build Your Own RAG Agent")
st.markdown("""
### What is RAG?
Retrieval-Augmented Generation (RAG) is a technique that gives LLMs access to your specific data (like a PDF). 
Instead of just guessing, it **retrieves** relevant info from your file and uses it to **generate** an accurate answer.
""")

# Sidebar for file upload
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file:
        # Save temp file
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("PDF Uploaded Successfully!")

# Main area
query = st.text_input("Ask a question about your document:", placeholder="What is this document about?")

if st.button("Run RAG Agent"):
    if uploaded_file and query:
        with st.spinner("Thinking... (Searching document and generating answer)"):
            try:
                answer = rag_helper.get_answer_from_pdf("temp.pdf", query)
                st.subheader("Answer:")
                st.write(answer)
            except Exception as e:
                st.error(f"An error occurred: {e}")
            finally:
                # Cleanup
                if os.path.exists("temp.pdf"):
                    os.remove("temp.pdf")
    elif not uploaded_file:
        st.warning("Please upload a PDF first in the sidebar.")
    elif not query:
        st.warning("Please enter a question.")

st.divider()
st.info("Built with LangChain, FAISS, and Groq")
