# 🔍 Enterprise Document Search with RAG

A production-ready Retrieval-Augmented Generation (RAG) system that enables intelligent document search and question-answering over your PDF documents using state-of-the-art AI models.

## 🌟 Features

- **PDF Document Processing**: Upload and process multiple PDF documents
- **Intelligent Chunking**: Smart text splitting with configurable chunk sizes and overlap
- **Vector Search**: FAISS-powered similarity search for fast retrieval
- **Multiple LLM Support**: Works with OpenAI GPT models or local HuggingFace models
- **Source Citation**: View which document chunks were used to generate answers
- **Modern UI**: Clean Streamlit interface with real-time processing
- **Persistent Storage**: Automatic saving and loading of vector indices
- **Comprehensive Logging**: Detailed logging with loguru for debugging

## 🏗️ Architecture

```
┌─────────────┐
│   PDF Files │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Document Loader │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Text Splitter  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Embedder     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FAISS Index   │
└────────┬────────┘
         │
         ▼
    ┌────────┐
    │ Query  │
    └───┬────┘
        │
        ▼
┌─────────────────┐
│   Retriever     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   LLM (GPT)     │
└────────┬────────┘
         │
         ▼
    ┌────────┐
    │ Answer │
    └────────┘
```

## 📋 Prerequisites

- Python 3.10 or higher
- OpenAI API key (for GPT models) OR
- HuggingFace account (for local models)
- 4GB+ RAM (8GB+ recommended for local models)

## 🚀 Installation

1. **Clone or download the project**

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your configuration:
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4o-mini
```

## 🎯 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Using the System

1. **Upload Documents**
   - Click "Browse files" in the sidebar
   - Select one or more PDF files
   - Click "Process Documents"

2. **Ask Questions**
   - Enter your question in the text input
   - Click "Search"
   - View the AI-generated answer and source documents

### Example Queries

- "What is the main topic of these documents?"
- "Summarize the key findings"
- "What are the recommendations mentioned?"
- "Explain the methodology used"

## 🐳 Docker Deployment

### Build the image
```bash
docker build -t enterprise-rag .
```

### Run the container
```bash
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your_key_here \
  -v $(pwd)/data:/app/data \
  enterprise-rag
```

## 📁 Project Structure

```
enterprise_rag/
│
├── app.py                      # Streamlit UI
│
├── backend/
│   ├── __init__.py
│   ├── document_loader.py      # PDF text extraction
│   ├── text_splitter.py        # Text chunking
│   ├── embedder.py             # Embedding generation
│   ├── vector_db.py            # FAISS vector database
│   ├── rag_chain.py            # RAG pipeline
│   └── llm_provider.py         # LLM integration
│
├── config/
│   ├── __init__.py
│   └── settings.py             # Configuration
│
├── data/
│   ├── pdfs/                   # Uploaded PDFs
│   ├── processed/              # Processed documents
│   └── vector_store/           # FAISS indices
│
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

## ⚙️ Configuration

Edit `config/settings.py` to customize:

- **CHUNK_SIZE**: Size of text chunks (default: 800)
- **CHUNK_OVERLAP**: Overlap between chunks (default: 100)
- **TOP_K**: Number of documents to retrieve (default: 5)
- **EMBEDDING_MODEL**: Sentence transformer model
- **LLM_PROVIDER**: 'openai' or 'huggingface'
- **MODEL_NAME**: Specific model to use

## 🔧 Advanced Features

### Using Local Models (HuggingFace)

Update your `.env`:
```env
LLM_PROVIDER=huggingface
MODEL_NAME=meta-llama/Llama-3-8B-Instruct
```

Note: Local models require significant RAM and GPU for optimal performance.

### Custom Embedding Models

Modify `config/settings.py`:
```python
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # Faster, smaller
# or
EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"  # Better quality
```

## 📊 Performance Tips

- **Chunk Size**: Smaller chunks (400-600) for precise answers, larger (800-1200) for context
- **Top K**: Increase for more comprehensive answers, decrease for faster responses
- **Embedding Model**: Use smaller models for speed, larger for accuracy
- **GPU**: Use CUDA-enabled PyTorch for faster embedding generation

## 🐛 Troubleshooting

### "No text extracted from PDF"
- PDF might be image-based (scanned). Consider using OCR tools like pytesseract
- PDF might be corrupted or password-protected

### "OpenAI API Error"
- Check your API key in `.env`
- Verify you have sufficient credits
- Check rate limits

### "Out of Memory"
- Reduce batch size in embedder
- Use smaller embedding model
- Process fewer documents at once

## 🚀 Future Enhancements

- [ ] **Multi-modal Support**: Images, tables, charts
- [ ] **Advanced Reranking**: Cross-encoder reranking for better results
- [ ] **Metadata Filtering**: Filter by date, author, document type
- [ ] **Conversational Memory**: Multi-turn conversations
- [ ] **Azure Cognitive Search**: Enterprise-grade search integration
- [ ] **Agent Framework**: LangChain agents for complex queries
- [ ] **Authentication**: User management and access control
- [ ] **API Endpoint**: FastAPI REST API for programmatic access
- [ ] **Batch Processing**: Background job processing for large documents
- [ ] **Analytics Dashboard**: Usage statistics and insights

## 📝 License

MIT License - feel free to use this project for commercial or personal use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on the repository.

---

Built with ❤️ using LangChain, FAISS, and Streamlit
