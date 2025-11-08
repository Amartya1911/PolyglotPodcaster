#!/bin/bash

# Setup script for Polyglot Podcaster
# This script helps set up the project with the correct Python version

echo "🎙️ Polyglot Podcaster Setup"
echo "=============================="
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
MAJOR_VERSION=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR_VERSION=$(echo $PYTHON_VERSION | cut -d. -f2)

echo "Detected Python version: $PYTHON_VERSION"
echo ""

# Check if Python version is compatible (3.8-3.12)
if [ "$MAJOR_VERSION" -eq 3 ] && [ "$MINOR_VERSION" -ge 8 ] && [ "$MINOR_VERSION" -le 12 ]; then
    echo "✅ Python version is compatible with PyTorch"
    PYTHON_CMD="python3"
elif command -v python3.11 &> /dev/null; then
    echo "⚠️ Default Python is not compatible. Using python3.11 instead."
    PYTHON_CMD="python3.11"
elif command -v python3.12 &> /dev/null; then
    echo "⚠️ Default Python is not compatible. Using python3.12 instead."
    PYTHON_CMD="python3.12"
elif command -v python3.10 &> /dev/null; then
    echo "⚠️ Default Python is not compatible. Using python3.10 instead."
    PYTHON_CMD="python3.10"
else
    echo "❌ Error: PyTorch requires Python 3.8-3.12"
    echo ""
    echo "Please install a compatible Python version:"
    echo "  brew install python@3.11"
    echo ""
    exit 1
fi

echo ""
echo "📦 Setting up virtual environment..."
$PYTHON_CMD -m venv venv

echo "✅ Virtual environment created"
echo ""

echo "📥 Activating virtual environment and installing dependencies..."
source venv/bin/activate

echo "Installing PyTorch and torchaudio..."
pip install --quiet torch torchaudio --index-url https://download.pytorch.org/whl/cpu

echo "Installing Streamlit..."
pip install --quiet streamlit

echo "Installing Chatterbox TTS..."
pip install --quiet chatterbox-tts

echo ""
echo "✅ Installation complete!"
echo ""
echo "🚀 To run the application:"
echo "   1. Activate the virtual environment: source venv/bin/activate"
echo "   2. Run the app: streamlit run app.py"
echo ""
