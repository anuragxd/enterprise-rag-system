"""
RAG chain module for retrieval-augmented generation
"""
from typing import Dict, List
from loguru import logger
from backend.vector_db import VectorDB
from backend.llm_provider import LLMProvider

class RAGChain:
    """Retrieval-Augmented Generation pipeline"""
    
    def __init__(self, vector_db: VectorDB, llm_provider: str = "openai", 
                 model_name: str = "gpt-4o-mini", api_key: str = None):
        """
        Initialize RAG chain
        
        Args:
            vector_db: VectorDB instance for retrieval
            llm_provider: LLM provider ('openai' or 'huggingface')
            model_name: Name of the model to use
            api_key: API key for the provider
        """
        self.vector_db = vector_db
        self.llm = LLMProvider(provider=llm_provider, model_name=model_name, api_key=api_key)
        logger.info(f"RAGChain initialized with {llm_provider} provider")
    
    def generate_answer(self, query: str, top_k: int = 5) -> Dict:
        """
        Generate answer using RAG pipeline
        
        Args:
            query: User query
            top_k: Number of documents to retrieve
            
        Returns:
            Dictionary containing answer and retrieved chunks
        """
        try:
            # Retrieve relevant documents
            retrieved_chunks = self.vector_db.search(query, top_k=top_k)
            
            if not retrieved_chunks:
                logger.warning("No relevant documents found")
                return {
                    'answer': "Answer not found in documents.",
                    'chunks': []
                }
            
            # Prepare context from retrieved chunks
            context = self._prepare_context(retrieved_chunks)
            
            # Generate prompt
            prompt = self._create_prompt(query, context)
            
            # Generate answer
            answer = self.llm.generate(prompt)
            
            logger.info(f"Generated answer for query: {query[:50]}...")
            
            return {
                'answer': answer,
                'chunks': retrieved_chunks
            }
            
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            raise
    
    def _prepare_context(self, chunks: List[Dict]) -> str:
        """
        Prepare context from retrieved chunks
        
        Args:
            chunks: List of retrieved document chunks
            
        Returns:
            Formatted context string
        """
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            source = chunk['metadata'].get('source', 'Unknown')
            text = chunk['text']
            context_parts.append(f"[Source {i}: {source}]\n{text}")
        
        return "\n\n".join(context_parts)
    
    def _create_prompt(self, query: str, context: str) -> str:
        """
        Create prompt for LLM
        
        Args:
            query: User query
            context: Retrieved context
            
        Returns:
            Formatted prompt
        """
        prompt = f"""You are a helpful AI assistant that answers questions based on the provided context.

Context:
{context}

Question: {query}

Instructions:
- Answer the question based ONLY on the information provided in the context above
- If the context doesn't contain enough information to answer the question, say "Answer not found in documents."
- Be concise and accurate
- Cite the source numbers when referencing specific information

Answer:"""
        
        return prompt
