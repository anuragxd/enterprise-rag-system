"""
Test the new HuggingFace token with Nebius provider
"""
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

# Your token from .env file
token = os.getenv("HUGGINGFACE_API_KEY")

print("Testing HuggingFace API with different models...")

# Try different model formats
models_to_try = [
    "Qwen/Qwen2.5-72B-Instruct",
    "meta-llama/Llama-3.2-3B-Instruct",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "HuggingFaceH4/zephyr-7b-beta",
]

try:
    client = InferenceClient(api_key=token)
    
    for model in models_to_try:
        print(f"\nTrying model: {model}")
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": "What is the capital of France? Answer in one sentence."}
                ],
                max_tokens=50,
                temperature=0.7
            )
            
            print(f"✅ SUCCESS!")
            print(f"Response: {completion.choices[0].message.content}")
            print(f"\n🎉 Working model found: {model}")
            print(f"\nUpdate your .env with: MODEL_NAME={model}")
            break
            
        except Exception as e:
            print(f"❌ Failed: {str(e)[:150]}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
