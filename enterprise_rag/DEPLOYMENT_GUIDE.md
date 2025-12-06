# Deployment Guide - Streamlit Community Cloud

## 🚀 Deploy Your RAG System Online

### Prerequisites
- GitHub account
- Git installed on your computer

### Step-by-Step Deployment

#### 1. Create a GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., "enterprise-rag-system")
3. Make it **Public** (required for free Streamlit deployment)
4. Don't initialize with README (we already have files)

#### 2. Push Your Code to GitHub

Open PowerShell in your project directory and run:

```powershell
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Enterprise RAG System"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

#### 3. Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set:
   - **Main file path:** `enterprise_rag/app.py`
   - **Python version:** 3.10

#### 4. Configure Secrets

In Streamlit Cloud, go to **App settings** → **Secrets** and add:

```toml
# .streamlit/secrets.toml format
LLM_PROVIDER = "huggingface"
HUGGINGFACE_API_KEY = "your_huggingface_token_here"
MODEL_NAME = "Qwen/Qwen2.5-72B-Instruct"
```

#### 5. Update Code to Use Secrets

The app needs to read from `st.secrets` instead of `.env` in production.

### ⚠️ Important Notes

1. **Don't commit your .env file** - It contains your API keys!
2. **Use .gitignore** - Already configured to exclude sensitive files
3. **Free tier limits:**
   - 1 GB RAM
   - 1 CPU core
   - May sleep after inactivity

### 🏠 Local Development (Recommended for Now)

Your app is already running locally at:
- **http://localhost:8502**

This is the best option for:
- Testing and development
- Processing large documents
- Unlimited usage
- No deployment complexity

### 💡 Alternative: Docker Deployment

If you want to deploy elsewhere (AWS, Azure, etc.), use Docker:

```bash
# Build image
docker build -t enterprise-rag .

# Run container
docker run -p 8501:8501 \
  -e HUGGINGFACE_API_KEY=your_key \
  -e MODEL_NAME=Qwen/Qwen2.5-72B-Instruct \
  enterprise-rag
```

### 🎯 Recommendation

**For now, use the local version** at http://localhost:8502

It's:
- ✅ Already working
- ✅ Faster (no network latency)
- ✅ More private (your documents stay local)
- ✅ No deployment hassle
- ✅ Free unlimited usage

Deploy to cloud only if you need:
- Remote access from anywhere
- Sharing with team members
- 24/7 availability
