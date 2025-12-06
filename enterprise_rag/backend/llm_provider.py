"""
LLM provider module supporting OpenAI and HuggingFace models
"""
from typing import Optional
from loguru import logger
import os

class LLMProvider:
    """Handles LLM interactions for multiple providers"""
    
    def __init__(self, provider: str = "openai", model_name: str = "gpt-4o-mini", 
                 api_key: Optional[str] = None):
        """
        Initialize LLM provider
        
        Args:
            provider: Provider name ('openai' or 'huggingface')
            model_name: Model name to use
            api_key: API key for the provider
        """
        self.provider = provider.lower()
        self.model_name = model_name
        self.api_key = api_key
        
        if self.provider == "openai":
            self._init_openai()
        elif self.provider == "huggingface":
            self._init_huggingface()
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        
        logger.info(f"LLMProvider initialized with {provider}/{model_name}")
    
    def _init_openai(self):
        """Initialize OpenAI client"""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
            logger.info("OpenAI client initialized")
        except ImportError:
            logger.error("OpenAI package not installed. Install with: pip install openai")
            raise
        except Exception as e:
            logger.error(f"Error initializing OpenAI: {e}")
            raise
    
    def _init_huggingface(self):
        """Initialize HuggingFace Inference API"""
        try:
            from huggingface_hub import InferenceClient
            
            logger.info(f"Initializing HuggingFace Inference API with model: {self.model_name}")
            self.client = InferenceClient(api_key=self.api_key)
            logger.info("HuggingFace Inference API initialized")
        except ImportError:
            logger.error("HuggingFace Hub package not installed. Install with: pip install huggingface-hub")
            raise
        except Exception as e:
            logger.error(f"Error initializing HuggingFace: {e}")
            raise
    
    def generate(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """
        Generate text using the configured LLM
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated text
        """
        try:
            if self.provider == "openai":
                return self._generate_openai(prompt, max_tokens, temperature)
            elif self.provider == "huggingface":
                return self._generate_huggingface(prompt, max_tokens, temperature)
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            raise
    
    def _generate_openai(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate using OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    def _generate_huggingface(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate using HuggingFace Inference API"""
        try:
            logger.info(f"Calling HuggingFace API with model: {self.model_name}")
            
            # Use chat.completions.create (new API format)
            messages = [{"role": "user", "content": prompt}]
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Extract the response text
            answer = response.choices[0].message.content.strip()
            logger.info(f"Successfully generated response of length {len(answer)}")
            return answer
            
        except Exception as e:
            logger.error(f"HuggingFace generation error: {e}")
            logger.error(f"Model: {self.model_name}, Prompt length: {len(prompt)}")
            raise
