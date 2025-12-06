"""
Vector database module using FAISS
"""
import faiss
import numpy as np
import pickle
from pathlib import Path
from typing import List, Dict, Tuple
from loguru import logger
from backend.embedder import Embedder

class VectorDB:
    """FAISS-based vector database for document retrieval"""
    
    def __init__(self, embedder: Embedder, index_path: str = "data/vector_store/faiss_index"):
        """
        Initialize vector database
        
        Args:
            embedder: Embedder instance for generating embeddings
            index_path: Path to save/load FAISS index
        """
        self.embedder = embedder
        self.index_path = index_path
        self.dimension = embedder.get_embedding_dimension()
        self.index = None
        self.documents = []
        
        logger.info(f"VectorDB initialized with dimension={self.dimension}")
    
    def add_documents(self, documents: List[Dict]):
        """
        Add documents to the vector database
        
        Args:
            documents: List of document dictionaries with 'text' and 'metadata'
        """
        try:
            if not documents:
                logger.warning("No documents to add")
                return
            
            # Extract texts
            texts = [doc['text'] for doc in documents]
            
            # Generate embeddings
            embeddings = self.embedder.embed_texts(texts)
            
            # Create or update index
            if self.index is None:
                self.index = faiss.IndexFlatL2(self.dimension)
                logger.info("Created new FAISS index")
            
            # Add embeddings to index
            self.index.add(embeddings.astype('float32'))
            
            # Store documents
            self.documents.extend(documents)
            
            logger.info(f"Added {len(documents)} documents to vector database")
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for similar documents
        
        Args:
            query: Query text
            top_k: Number of top results to return
            
        Returns:
            List of dictionaries containing matched documents and scores
        """
        try:
            if self.index is None or len(self.documents) == 0:
                logger.warning("No documents in database")
                return []
            
            # Generate query embedding
            query_embedding = self.embedder.embed_text(query)
            query_embedding = query_embedding.reshape(1, -1).astype('float32')
            
            # Search
            distances, indices = self.index.search(query_embedding, min(top_k, len(self.documents)))
            
            # Prepare results
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx < len(self.documents):
                    results.append({
                        'text': self.documents[idx]['text'],
                        'metadata': self.documents[idx]['metadata'],
                        'score': float(dist)
                    })
            
            logger.info(f"Found {len(results)} results for query")
            return results
            
        except Exception as e:
            logger.error(f"Error searching: {e}")
            raise
    
    def save_index(self):
        """Save FAISS index and documents to disk"""
        try:
            if self.index is None:
                logger.warning("No index to save")
                return
            
            # Create directory if it doesn't exist
            Path(self.index_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Save FAISS index
            faiss.write_index(self.index, f"{self.index_path}.faiss")
            
            # Save documents
            with open(f"{self.index_path}.pkl", 'wb') as f:
                pickle.dump(self.documents, f)
            
            logger.info(f"Saved index with {len(self.documents)} documents to {self.index_path}")
            
        except Exception as e:
            logger.error(f"Error saving index: {e}")
            raise
    
    def load_index(self) -> bool:
        """
        Load FAISS index and documents from disk
        
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            index_file = f"{self.index_path}.faiss"
            docs_file = f"{self.index_path}.pkl"
            
            if not Path(index_file).exists() or not Path(docs_file).exists():
                logger.info("No existing index found")
                return False
            
            # Load FAISS index
            self.index = faiss.read_index(index_file)
            
            # Load documents
            with open(docs_file, 'rb') as f:
                self.documents = pickle.load(f)
            
            logger.info(f"Loaded index with {len(self.documents)} documents from {self.index_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading index: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """Get statistics about the vector database"""
        return {
            'total_documents': len(self.documents),
            'dimension': self.dimension,
            'index_size': self.index.ntotal if self.index else 0
        }
