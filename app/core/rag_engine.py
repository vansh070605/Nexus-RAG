"""
app/rag_engine.py — RAG Pipeline
Handles PDF ingestion, vector indexing, and LLM querying.
"""
import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# ── Singleton embedding model (loaded once, reused) ────────────────────────────
_embeddings: HuggingFaceEmbeddings | None = None


def get_embeddings() -> HuggingFaceEmbeddings:
    """Return a cached instance of the HuggingFace embedding model."""
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return _embeddings


# ── PDF Processing ─────────────────────────────────────────────────────────────

def process_pdf(pdf_path: str) -> FAISS:
    """
    Load a PDF, split it into chunks, embed them, and return a FAISS vector store.

    Args:
        pdf_path: Absolute path to the PDF file.

    Returns:
        A FAISS vector store ready for similarity search.
    """
    # 1. Load pages
    print(f"DEBUG: Loading PDF from {pdf_path}")
    try:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
    except Exception as e:
        print(f"DEBUG: Error loading PDF: {str(e)}")
        if isinstance(e, IndexError):
            raise ValueError(f"PDF Parsing Error: The file structure is invalid or data is missing (IndexError).")
        raise ValueError(f"Could not read PDF: {str(e)}")
    
    if not documents:
        print("DEBUG: No pages were loaded from the PDF.")
        raise ValueError("The PDF document appears to be empty or unreadable.")

    print(f"DEBUG: Loaded {len(documents)} pages.")

    # 2. Chunk the text
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    chunks = splitter.split_documents(documents)

    if not chunks:
        print("DEBUG: No text chunks were created (likely no text content found).")
        raise ValueError("No text could be extracted from the PDF. It might be image-only (scanned).")

    print(f"DEBUG: Created {len(chunks)} text chunks.")

    # 3. Embed and index
    vector_db = FAISS.from_documents(chunks, get_embeddings())
    return vector_db


# ── RAG Query ──────────────────────────────────────────────────────────────────

_RAG_PROMPT = ChatPromptTemplate.from_template(
    """You are a precise, helpful document analyst.
Use ONLY the context below to answer the question.
If the answer is not present in the context, say:
"I don't have enough information in the document to answer that."

Context:
{context}

Question: {question}

Answer:"""
)


def ask(vector_db: FAISS, query: str) -> str:
    """
    Run a RAG query against an indexed vector store.

    Args:
        vector_db: A FAISS vector store (from process_pdf).
        query:     The user's natural-language question.

    Returns:
        The LLM's answer as a plain string.
    """
    llm = ChatGroq(
        model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        temperature=0,
    )

    def _format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    retriever = vector_db.as_retriever(search_kwargs={"k": 5})

    chain = (
        {"context": retriever | _format_docs, "question": RunnablePassthrough()}
        | _RAG_PROMPT
        | llm
        | StrOutputParser()
    )

    return chain.invoke(query)
