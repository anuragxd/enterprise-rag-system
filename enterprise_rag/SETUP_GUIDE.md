# Setup Guide - Enterprise RAG System

## ⚠️ Important: LLM Provider Setup

Your HuggingFace token has limited permissions for the Inference API. Here are your options:

### Option 1: Use OpenAI (Recommended - Most Reliable)

1. **Get an OpenAI API Key:**
   - Go to https://platform.openai.com/api-keys
   - Create a new API key
   - Add $5-10 credit to your account

2. **Update your `.env` file:**
   ```env
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-proj-your_key_here
   MODEL_NAME=gpt-4o-mini
   ```

3. **Restart the app:**
   ```bash
   streamlit run app.py
   ```

### Option 2: Upgrade HuggingFace Token Permissions

1. Go to https://huggingface.co/settings/tokens
2. Create a new token with "Inference API" permissions
3. Update `.env` with the new token
4. Use a supported model like:
   ```env
   LLM_PROVIDER=huggingface
   HUGGINGFACE_API_KEY=your_new_token_here
   MODEL_NAME=HuggingFaceH4/zephyr-7b-beta
   ```

### Option 3: Use Local Models (No API Key Needed)

If you have a good GPU (8GB+ VRAM), you can run models locally:

1. **Install additional dependencies:**
   ```bash
   pip install accelerate bitsandbytes
   ```

2. **Update the LLM provider** to load models locally (requires code modification)

3. **Use smaller models** like:
   - `microsoft/phi-2` (2.7B parameters)
   - `TinyLlama/TinyLlama-1.1B-Chat-v1.0`

## 🎯 Quick Start with OpenAI (Easiest)

```bash
# 1. Edit .env file
notepad .env

# 2. Change these lines:
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
MODEL_NAME=gpt-4o-mini

# 3. Save and restart
streamlit run app.py
```

## 💰 Cost Estimate (OpenAI)

- **gpt-4o-mini**: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- **Typical query**: ~$0.001-0.005 per question
- **$5 credit**: ~1000-5000 questions

## ✅ Testing Your Setup

Run the test script to verify your configuration:

```bash
python test_hf_api.py
```

## 🆘 Need Help?

If you're having issues:
1. Check your API key is valid
2. Ensure you have credits (for OpenAI)
3. Check the logs in `logs/app.log`
4. Verify your internet connection

## 📝 Current Status

Your system is configured with:
- ✅ PDF processing
- ✅ Vector database (FAISS)
- ✅ Embeddings (sentence-transformers)
- ⚠️ LLM needs proper API key

Once you configure a working LLM provider, the system will be fully functional!
