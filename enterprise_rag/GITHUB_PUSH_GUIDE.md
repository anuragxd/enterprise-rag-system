# GitHub Push Guide - Clean Push Without Secrets

## ⚠️ Issue: GitHub Blocked Push Due to API Token

GitHub's secret scanning detected your HuggingFace token in the commit history.

## ✅ Solution: Fresh Start

Follow these steps to push cleanly:

### Step 1: Navigate to Parent Directory

```powershell
cd ..
```

### Step 2: Remove Git History

```powershell
Remove-Item -Recurse -Force .git
```

### Step 3: Initialize Fresh Git Repo

```powershell
git init
```

### Step 4: Add Files (Excluding .env)

The `.gitignore` file already excludes `.env`, so your token won't be committed.

```powershell
git add .
```

### Step 5: Commit

```powershell
git commit -m "Initial commit - Enterprise RAG System"
```

### Step 6: Add Remote

```powershell
git remote add origin https://github.com/anuragxd/enterprise-rag-system.git
```

### Step 7: Push

```powershell
git push -u origin main --force
```

## 🔒 Security Best Practices

✅ **Never commit `.env` files** - Already in `.gitignore`  
✅ **Use environment variables** - For local development  
✅ **Use Streamlit secrets** - For cloud deployment  
✅ **Rotate exposed tokens** - If accidentally pushed  

## 📝 For Streamlit Cloud Deployment

After successful push:

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `anuragxd/enterprise-rag-system`
5. Set main file: `enterprise_rag/app.py`
6. Go to **App settings** → **Secrets**
7. Add your secrets:

```toml
LLM_PROVIDER = "huggingface"
HUGGINGFACE_API_KEY = "your_token_here"
MODEL_NAME = "Qwen/Qwen2.5-72B-Instruct"
```

## 🏠 Local Development (Current Setup)

Your app is already running locally at http://localhost:8502

This is the recommended approach for:
- Development and testing
- Processing sensitive documents
- Unlimited usage
- No deployment complexity

## 💡 Alternative: Keep Using Locally

You don't need to deploy to GitHub/Streamlit Cloud if you're happy with local usage!

Your current setup works perfectly for:
- Personal use
- Testing and development
- Processing private documents
- No cost or limits

Just keep using: http://localhost:8502
