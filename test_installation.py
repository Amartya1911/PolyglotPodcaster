"""
Test script to verify the Polyglot Podcaster installation
Run this after installation to check if all dependencies are working
"""

import sys

def test_imports():
    """Test if all required packages can be imported"""
    print("🧪 Testing imports...")
    
    errors = []
    
    try:
        import streamlit
        print("✅ streamlit imported successfully")
    except ImportError as e:
        errors.append(f"❌ streamlit: {e}")
    
    try:
        import torch
        print(f"✅ torch imported successfully (version {torch.__version__})")
        print(f"   CUDA available: {torch.cuda.is_available()}")
    except ImportError as e:
        errors.append(f"❌ torch: {e}")
    
    try:
        import torchaudio
        print(f"✅ torchaudio imported successfully")
    except ImportError as e:
        errors.append(f"❌ torchaudio: {e}")
    
    try:
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS
        print("✅ chatterbox-tts imported successfully")
    except ImportError as e:
        errors.append(f"❌ chatterbox-tts: {e}")
    
    print("\n" + "="*50)
    
    if errors:
        print("❌ Some imports failed:")
        for error in errors:
            print(f"   {error}")
        print("\nPlease install missing packages:")
        print("   pip install streamlit torch torchaudio chatterbox-tts")
        return False
    else:
        print("✅ All dependencies installed correctly!")
        print("\n🚀 You can now run the app with:")
        print("   streamlit run app.py")
        return True

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and 8 <= version.minor <= 12:
        print("✅ Python version is compatible with PyTorch")
        return True
    else:
        print("⚠️ Warning: PyTorch officially supports Python 3.8-3.12")
        if version.minor >= 13:
            print("   Your Python version might not be supported yet.")
        return False

if __name__ == "__main__":
    print("🎙️ Polyglot Podcaster - Installation Test")
    print("="*50)
    print()
    
    check_python_version()
    print()
    test_imports()
