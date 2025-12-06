"""
Streamlit UI for Enterprise Document Search with RAG
"""
import streamlit as st
import os
from pathlib import Path
from loguru import logger
from backend.document_loader import DocumentLoader
from backend.text_splitter import TextSplitter
from backend.embedder import Embedder
from backend.vector_db import VectorDB
from backend.rag_chain import RAGChain
from config.settings import Settings

# Configure logger
logger.add("logs/app.log", rotation="10 MB")

# Initialize settings
settings = Settings()

# Page config
st.set_page_config(
    page_title="Enterprise Document Search",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if 'vector_db' not in st.session_state:
    st.session_state.vector_db = None
if 'rag_chain' not in st.session_state:
    st.session_state.rag_chain = None
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = []

def initialize_system():
    """Initialize the RAG system components"""
    try:
        # Check if API key is configured
        api_key = settings.OPENAI_API_KEY if settings.LLM_PROVIDER == "openai" else settings.HUGGINGFACE_API_KEY
        if not api_key or api_key == "your_openai_api_key_here":
            st.warning("⚠️ **API Key Not Configured!**")
            st.info("""
            Please configure your LLM provider:
            
            1. **For OpenAI (Recommended):**
               - Get API key from: https://platform.openai.com/api-keys
               - Edit `.env` file and set `OPENAI_API_KEY`
               
            2. **For HuggingFace:**
               - Get token from: https://huggingface.co/settings/tokens
               - Edit `.env` file and set `HUGGINGFACE_API_KEY`
            
            See `SETUP_GUIDE.md` for detailed instructions.
            """)
            return False
        
        embedder = Embedder(model_name=settings.EMBEDDING_MODEL)
        vector_db = VectorDB(embedder=embedder, index_path=settings.VECTOR_STORE_PATH)
        
        # Try to load existing index
        if vector_db.load_index():
            st.session_state.vector_db = vector_db
            st.session_state.rag_chain = RAGChain(
                vector_db=vector_db,
                llm_provider=settings.LLM_PROVIDER,
                model_name=settings.MODEL_NAME,
                api_key=api_key
            )
            logger.info("System initialized successfully")
            return True
        else:
            st.session_state.vector_db = vector_db
            logger.info("New vector database created")
            return True
    except Exception as e:
        logger.error(f"Error initializing system: {e}")
        st.error(f"Error initializing system: {e}")
        return False

def process_documents(uploaded_files):
    """Process uploaded PDF documents"""
    if not uploaded_files:
        st.warning("Please upload at least one PDF file")
        return
    
    with st.spinner("Processing documents..."):
        try:
            # Initialize components
            doc_loader = DocumentLoader()
            text_splitter = TextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP
            )
            
            all_chunks = []
            
            # Process each file
            for uploaded_file in uploaded_files:
                # Save uploaded file
                pdf_path = os.path.join(settings.PDF_DIR, uploaded_file.name)
                with open(pdf_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Extract text
                text = doc_loader.load_pdf(pdf_path)
                if text:
                    # Split into chunks
                    chunks = text_splitter.split_text(text, source=uploaded_file.name)
                    all_chunks.extend(chunks)
                    st.session_state.processed_files.append(uploaded_file.name)
                    logger.info(f"Processed {uploaded_file.name}: {len(chunks)} chunks")
            
            if all_chunks:
                # Add to vector database
                st.session_state.vector_db.add_documents(all_chunks)
                st.session_state.vector_db.save_index()
                
                # Initialize RAG chain
                st.session_state.rag_chain = RAGChain(
                    vector_db=st.session_state.vector_db,
                    llm_provider=settings.LLM_PROVIDER,
                    model_name=settings.MODEL_NAME,
                    api_key=settings.OPENAI_API_KEY if settings.LLM_PROVIDER == "openai" else settings.HUGGINGFACE_API_KEY
                )
                
                st.success(f"✅ Successfully processed {len(uploaded_files)} documents with {len(all_chunks)} chunks")
            else:
                st.error("No text could be extracted from the uploaded files")
                
        except Exception as e:
            logger.error(f"Error processing documents: {e}")
            st.error(f"Error processing documents: {e}")

def main():
    # Header
    st.title("🔍 Enterprise Document Search with RAG")
    st.markdown("Upload PDFs and ask questions to get AI-powered answers grounded in your documents")
    
    # Initialize system
    if st.session_state.vector_db is None:
        initialize_system()
    
    # Sidebar
    with st.sidebar:
        st.header("📄 Document Upload")
        
        uploaded_files = st.file_uploader(
            "Upload PDF files",
            type=['pdf'],
            accept_multiple_files=True
        )
        
        if st.button("Process Documents", type="primary"):
            if uploaded_files:
                process_documents(uploaded_files)
        
        st.divider()
        
        # Settings
        st.header("⚙️ Settings")
        st.write(f"**LLM Provider:** {settings.LLM_PROVIDER}")
        st.write(f"**Model:** {settings.MODEL_NAME}")
        st.write(f"**Chunk Size:** {settings.CHUNK_SIZE}")
        st.write(f"**Top K Results:** {settings.TOP_K}")
        
        if st.session_state.processed_files:
            st.divider()
            st.header("📚 Processed Files")
            for file in st.session_state.processed_files:
                st.write(f"✓ {file}")
    
    # Main content
    if st.session_state.rag_chain is None:
        st.info("👈 Please upload and process documents to start asking questions")
    else:
        st.header("💬 Ask Questions")
        
        query = st.text_input(
            "Enter your question:",
            placeholder="What is this document about?"
        )
        
        if st.button("Search", type="primary") and query:
            with st.spinner("Searching and generating answer..."):
                try:
                    result = st.session_state.rag_chain.generate_answer(
                        query=query,
                        top_k=settings.TOP_K
                    )
                    
                    # Display answer
                    st.subheader("📝 Answer")
                    st.write(result['answer'])
                    
                    # Display retrieved chunks
                    if result['chunks']:
                        st.divider()
                        st.subheader("📚 Source Documents")
                        
                        for i, chunk in enumerate(result['chunks'], 1):
                            with st.expander(f"Source {i}: {chunk['metadata'].get('source', 'Unknown')} (Score: {chunk['score']:.4f})"):
                                st.write(chunk['text'])
                    
                except Exception as e:
                    logger.error(f"Error generating answer: {e}")
                    st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
