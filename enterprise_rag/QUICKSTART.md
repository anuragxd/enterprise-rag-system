# Quick Start Guide

## ✅ Installation Complete!

All dependencies have been installed successfully.

## 🔑 Next Steps

### 1. Configure Your API Key

Edit the `.env` file and add your OpenAI API key:

```bash
# Open .env file in your editor
notepad .env
```

Replace `your_openai_api_key_here` with your actual OpenAI API key:
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

### 2. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 3. Use the System

1. **Upload PDFs**: Click "Browse files" in the sidebar
2. **Process**: Click "Process Documents" button
3. **Ask Questions**: Enter your question and click "Search"

## 🎯 Example Workflow

1. Upload a PDF document (e.g., a research paper, manual, or report)
2. Wait for processing (you'll see a success message)
3. Ask questions like:
   - "What is the main topic of this document?"
   - "Summarize the key findings"
   - "What are the recommendations?"

## 🔧 Troubleshooting

### If you don't have an OpenAI API key:

Get one from: https://platform.openai.com/api-keys

### Alternative: Use HuggingFace (Local Models)

Edit `.env`:
```
LLM_PROVIDER=huggingface
MODEL_NAME=meta-llama/Llama-3-8B-Instruct
```

Note: Local models require significant RAM (8GB+) and GPU for best performance.

## 📁 Project Features

✅ PDF text extraction with error handling
✅ Smart text chunking (800 tokens, 100 overlap)
✅ FAISS vector database for fast search
✅ Source citations showing which chunks were used
✅ Persistent storage (indices saved automatically)
✅ Comprehensive logging in `logs/` directory

## 🚀 Ready to Go!

Your Enterprise RAG system is ready. Just add your API key and run!
