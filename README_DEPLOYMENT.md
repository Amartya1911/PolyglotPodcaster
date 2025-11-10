# Deployment Guide

## Why Streamlit Community Cloud Won't Work

Streamlit Community Cloud has limitations that prevent this app from running:
- **Memory**: Only 1GB RAM (model needs ~3GB)
- **Storage**: Limited disk space for model files
- **CPU Only**: No GPU acceleration
- **Timeout**: Build process times out with large dependencies

## Recommended: Deploy to HuggingFace Spaces

HuggingFace Spaces is the **best option** for this project:

### Advantages:
✅ **Free GPU access** (much faster inference)
✅ **16GB RAM** (enough for the model)
✅ **No timeouts** during model loading
✅ **Great for resume** (live demo link on huggingface.co)
✅ **Easy deployment** (git push)

### Steps to Deploy:

1. **Create HuggingFace Account**: https://huggingface.co/join

2. **Create a new Space**:
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose "Streamlit" as SDK
   - Select "CPU basic" (free) or "GPU" if available
   - Name it: `polyglot-podcaster`

3. **Push your code**:
   ```bash
   cd "/Users/rajrup/Desktop/polyglot podcaster"
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/polyglot-podcaster
   git push hf main
   ```

4. **Wait for build** (~5-10 minutes for first deployment)

5. **Share your live demo**: `https://huggingface.co/spaces/YOUR_USERNAME/polyglot-podcaster`

### Configuration Files Needed:

The repository already has:
- ✅ `app.py` (main application)
- ✅ `requirements.txt` (Python dependencies)
- ✅ `packages.txt` (system dependencies)

HuggingFace Spaces will automatically:
- Install all dependencies
- Download the 3GB model on first run
- Cache the model for future runs
- Provide a public URL

## Alternative: Local Deployment Only

If you prefer to keep it local:

1. **Document clearly in README.md** that it requires local setup
2. **Add video demo** to your GitHub repo showing it working
3. **Keep the GitHub repo clean** with good documentation

This is still valuable for a resume as it shows:
- Deep learning implementation skills
- Working with complex ML models
- Full-stack development (Streamlit UI + ML backend)

## Alternative: Use a Lighter Model

Replace chatterbox-tts with a smaller model like:
- **Coqui TTS** (~500MB)
- **pyttsx3** (offline, tiny)
- **gTTS** (Google Text-to-Speech, API-based)

Trade-offs:
- ❌ Loses zero-shot voice cloning capability
- ❌ Less impressive technically
- ✅ Deployable to Streamlit Community Cloud
- ✅ Faster inference

## Recommendation

**Deploy to HuggingFace Spaces** for the best of both worlds:
- Keeps the impressive zero-shot voice cloning
- Provides a live demo link
- Shows you can deploy complex ML applications
- Perfect for including on resume and portfolio
