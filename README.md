---
title: Polyglot Podcaster
emoji: 🎙️
colorFrom: purple
colorTo: indigo
sdk: streamlit
sdk_version: 1.28.0
app_file: app.py
pinned: false
license: mit
---

# 🎙️ Polyglot Podcaster

A Streamlit-based web application for zero-shot multilingual voice cloning using the Chatterbox TTS model.

## 🌟 Features

- **Zero-Shot Voice Cloning**: Record your voice or upload a short voice sample and generate speech in any supported language
- **Browser-Based Recording**: Record audio directly in your browser - no need to upload files!
- **File Upload Support**: Alternative option to upload pre-recorded .wav files
- **23 Languages Supported**: English, Spanish, French, German, Italian, Portuguese, Polish, Turkish, Russian, Dutch, Arabic, Swedish, Danish, Greek, Finnish, Hebrew, Hindi, Japanese, Korean, Malay, Norwegian, Swahili, and Chinese
- **Simple Web Interface**: Easy-to-use Streamlit interface with tabbed input options
- **GPU Acceleration**: Automatically uses GPU if available for faster generation

## 🚀 Installation

### Prerequisites

⚠️ **Important:** PyTorch currently requires Python 3.8-3.12. Python 3.13 is not yet supported.

If you have Python 3.13, you'll need to install Python 3.11 or 3.12:
```bash
# Using Homebrew on macOS
brew install python@3.11
```

### Installation Steps

1. **Navigate to the project directory:**
   ```bash
   cd "/Users/rajrup/Desktop/polyglot podcaster"
   ```

2. **Create a virtual environment with Python 3.11 or 3.12:**
   ```bash
   # If you have Python 3.11
   python3.11 -m venv venv
   
   # OR if you have Python 3.12
   python3.12 -m venv venv
   
   # OR use the default python3 if it's 3.8-3.12
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

4. **Install PyTorch first:**
   ```bash
   # For CPU-only (smaller download)
   pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
   
   # OR for GPU support (if you have CUDA)
   pip install torch torchaudio
   ```

5. **Install remaining dependencies:**
   ```bash
   pip install streamlit chatterbox-tts
   ```

## 📖 Usage

1. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

2. **Use the application:**
   
   **Option A: Record Audio (Recommended)**
   - Click the "🎤 Record Audio" tab
   - Click "🎙️ Click to Record" button to start recording
   - Speak for 10-15 seconds
   - Click "⏹️ Click to Stop" to finish recording
   - Your recorded audio will be displayed
   
   **Option B: Upload File**
   - Click the "📤 Upload File" tab
   - Upload a 10-15 second `.wav` file of the target voice
   
   **Then:**
   - Enter the text you want to generate
   - Select the language of your text
   - Click "🎵 Generate Speech"
   - Listen to the generated audio!

## 📋 Requirements

- Python 3.10+
- streamlit
- streamlit-audiorecorder
- chatterbox-tts
- torch
- torchaudio

## 🎯 How It Works

1. The app loads the Chatterbox Multilingual TTS model (cached for performance)
2. You provide a voice sample as a reference
3. The model generates new speech in your chosen language using the voice characteristics from the sample
4. The generated audio is saved and played back in the browser

## ⚠️ Notes

- The first run will download the Chatterbox model (may take some time)
- GPU is recommended for faster generation
- Input audio should be in `.wav` format
- Best results with clear, 10-15 second voice samples

## 📄 License

This project uses the Chatterbox TTS library. Please refer to the Chatterbox TTS license for usage terms.
