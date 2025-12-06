"""
Text splitting module for chunking documents
"""
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
except ImportError:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict
from loguru import logger

class TextSplitter:
    """Handles splitting text into chunks for embedding"""
    
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 100):
        """
        Initialize text splitter
        
        Args:
            chunk_size: Maximum size of each chunk
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        logger.info(f"TextSplitter initialized with chunk_size={chunk_size}, overlap={chunk_overlap}")
    
    def split_text(self, text: str, source: str = "unknown") -> List[Dict]:
        """
        Split text into chunks with metadata
        
        Args:
            text: Text to split
            source: Source document name
            
        Returns:
            List of dictionaries containing text chunks and metadata
        """
        try:
            chunks = self.splitter.split_text(text)
            
            # Add metadata to each chunk
            chunk_dicts = []
            for i, chunk in enumerate(chunks):
                chunk_dicts.append({
                    'text': chunk,
                    'metadata': {
                        'source': source,
                        'chunk_id': i,
                        'total_chunks': len(chunks)
                    }
                })
            
            logger.info(f"Split text from {source} into {len(chunks)} chunks")
            return chunk_dicts
            
        except Exception as e:
            logger.error(f"Error splitting text: {e}")
            return []
