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

# We'll use a globally cached embedding model to speed things up
_embeddings = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return _embeddings

def process_pdf(pdf_path):
    """Loads PDF and returns a searchable Vector Database."""
    # 1. Load the PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # 2. Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)

    # 3. Create/Store in FAISS
    embeddings = get_embeddings()
    vector_db = FAISS.from_documents(chunks, embeddings)

    return vector_db

def ask_rag_agent(vector_db, query):
    """Queries an existing Vector Database using modern LCEL pipeline."""
    # 1. Setup LLM (Groq)
    llm = ChatGroq(
        model=os.getenv("GROQ_MODEL", "llama3-8b-8192"),
        temperature=0
    )

    # 2. Build a RAG prompt template
    prompt = ChatPromptTemplate.from_template(
        """You are a helpful assistant. Use ONLY the following context to answer the question.
If the answer is not in the context, say "I don't know based on the provided document."

Context:
{context}

Question: {question}

Answer:"""
    )

    # 3. Helper to format retrieved docs into a single string
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # 4. Build LCEL chain: retrieve → format → prompt → LLM → parse
    retriever = vector_db.as_retriever()
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # 5. Invoke and return the answer
    return chain.invoke(query)

