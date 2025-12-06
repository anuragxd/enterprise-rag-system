"""
Test script to verify HuggingFace API connection
"""
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("HUGGINGFACE_API_KEY")

print(f"Testing HuggingFace API...")
print(f"API Key: {api_key[:10]}..." if api_key else "No API key found")

# List of models to try (free tier compatible)
models_to_try = [
    "HuggingFaceH4/zephyr-7b-beta",
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "meta-llama/Llama-2-7b-chat-hf",
    "tiiuae/falcon-7b-instruct",
]

try:
    client = InferenceClient(token=api_key)
    
    # Test with a simple prompt
    prompt = "Answer this question in one sentence: What is the capital of France?"
    
    print(f"\nTest prompt: {prompt}\n")
    
    for model in models_to_try:
        print(f"Trying model: {model}")
        try:
            response = client.text_generation(
                prompt,
                model=model,
                max_new_tokens=50,
                temperature=0.7
            )
            print(f"✅ SUCCESS!")
            print(f"Response: {response}\n")
            print(f"✅ Working model found: {model}")
            print(f"\nUpdate your .env file with:")
            print(f"MODEL_NAME={model}")
            break
        except Exception as e:
            print(f"❌ Failed: {str(e)[:100]}\n")
            
except Exception as e:
    print(f"\n❌ Error: {e}")
