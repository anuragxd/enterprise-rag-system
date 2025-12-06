"""
Configuration settings for Enterprise RAG system
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # Directories
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    PDF_DIR = DATA_DIR / "pdfs"
    PROCESSED_DIR = DATA_DIR / "processed"
    VECTOR_STORE_DIR = DATA_DIR / "vector_store"
    VECTOR_STORE_PATH = str(VECTOR_STORE_DIR / "faiss_index")
    
    # Embedding settings
    EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
    
    # Text splitting settings
    CHUNK_SIZE = 800
    CHUNK_OVERLAP = 100
    
    # Retrieval settings
    TOP_K = 5
    
    # LLM settings - support both local .env and Streamlit secrets
    try:
        import streamlit as st
        # Try to get from Streamlit secrets first (for cloud deployment)
        LLM_PROVIDER = st.secrets.get("LLM_PROVIDER", os.getenv("LLM_PROVIDER", "openai"))
        MODEL_NAME = st.secrets.get("MODEL_NAME", os.getenv("MODEL_NAME", "gpt-4o-mini"))
        OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))
        HUGGINGFACE_API_KEY = st.secrets.get("HUGGINGFACE_API_KEY", os.getenv("HUGGINGFACE_API_KEY", ""))
    except:
        # Fallback to environment variables (for local development)
        LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
        MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
    
    # HuggingFace model options (if using local models)
    # MODEL_NAME = "meta-llama/Llama-3-8B-Instruct"
    
    def __init__(self):
        """Create necessary directories"""
        self.PDF_DIR.mkdir(parents=True, exist_ok=True)
        self.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        self.VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
        
        # Create logs directory
        logs_dir = self.BASE_DIR / "logs"
        logs_dir.mkdir(exist_ok=True)
