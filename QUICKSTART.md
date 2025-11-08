# 🚀 Quick Start Guide

## Current Situation

Your system has Python 3.13, but PyTorch (required for this project) doesn't support Python 3.13 yet. You need Python 3.8-3.12.

## Option 1: Install Python 3.11 (Recommended)

```bash
# Install Python 3.11 using Homebrew
brew install python@3.11

# Remove the existing virtual environment
cd "/Users/rajrup/Desktop/polyglot podcaster"
rm -rf venv

# Run the setup script
./setup.sh
```

## Option 2: Manual Setup

```bash
# Navigate to the project directory
cd "/Users/rajrup/Desktop/polyglot podcaster"

# Remove existing venv
rm -rf venv

# Create new virtual environment with Python 3.11
python3.11 -m venv venv

# Activate it
source venv/bin/activate

# Install PyTorch for CPU
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install other dependencies
pip install streamlit chatterbox-tts
```

## Running the App

Once installed:

```bash
cd "/Users/rajrup/Desktop/polyglot podcaster"
source venv/bin/activate
streamlit run app.py
```

## Troubleshooting

### "No matching distribution found for torch"
- This means your Python version is not compatible
- Install Python 3.11 or 3.12 using Homebrew
- Recreate the virtual environment with the compatible Python version

### First Run Takes a Long Time
- The Chatterbox model needs to be downloaded (happens automatically)
- This is a one-time download
- Subsequent runs will be much faster

### Out of Memory Errors
- The model is quite large
- Close other applications
- If on a Mac with limited RAM, the CPU version will work but be slower

## Need Help?

The complete code is ready in `app.py`. Once you have a compatible Python version installed, the setup should be straightforward!
