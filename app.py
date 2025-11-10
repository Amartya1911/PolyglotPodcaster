import streamlit as st
import torch
import torchaudio
import tempfile
import os
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
from googletrans import Translator

# Language mapping: User-friendly name -> 2-letter code
LANGUAGES = {
    "English": "en", "Spanish": "es", "French": "fr", "German": "de",
    "Italian": "it", "Portuguese": "pt", "Polish": "pl", "Turkish": "tr",
    "Russian": "ru", "Dutch": "nl", "Arabic": "ar", "Swedish": "sv",
    "Danish": "da", "Greek": "el", "Finnish": "fi", "Hebrew": "he",
    "Hindi": "hi", "Japanese": "ja", "Korean": "ko", "Malay": "ms",
    "Norwegian": "no", "Swahili": "sw", "Chinese": "zh"
}

@st.cache_resource
def load_model():
    """
    Load the ChatterboxMultilingualTTS model with GPU/CPU detection.
    This function is cached to ensure the model is loaded only once.
    """
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    st.info(f"Loading model on device: {device}")
    model = ChatterboxMultilingualTTS.from_pretrained(device=device)
    return model

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Polyglot Podcaster",
        page_icon="🎙️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        /* Dark theme base */
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        }
        
        /* Main header with metallic purple gradient */
        .main-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 50%, #a78bfa 100%);
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(139, 92, 246, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .main-header h1 {
            color: white;
            font-size: 3rem;
            margin: 0;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
            background: linear-gradient(to right, #ffffff, #e9d5ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .main-header p {
            color: #e9d5ff;
            font-size: 1.2rem;
            margin-top: 0.5rem;
            text-shadow: 1px 1px 4px rgba(0,0,0,0.3);
        }
        
        /* Buttons with silver-purple metallic effect */
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #c0c0c0 0%, #8b5cf6 50%, #a78bfa 100%);
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.2);
            padding: 0.75rem 2rem;
            font-size: 1.1rem;
            font-weight: bold;
            border-radius: 12px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4),
                        inset 0 1px 0 rgba(255, 255, 255, 0.2);
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(139, 92, 246, 0.6),
                        inset 0 1px 0 rgba(255, 255, 255, 0.3);
            background: linear-gradient(135deg, #d0d0d0 0%, #9b6cf6 50%, #b78bfa 100%);
        }
        
        /* Text input fields with metallic silver-purple */
        .stTextArea textarea, .stTextInput input {
            background: linear-gradient(135deg, #2a2a3e 0%, #1f1f3a 100%) !important;
            border: 2px solid rgba(192, 192, 192, 0.3) !important;
            border-radius: 10px !important;
            color: #e9d5ff !important;
            box-shadow: inset 0 2px 8px rgba(0,0,0,0.3),
                        0 0 0 1px rgba(139, 92, 246, 0.2) !important;
        }
        .stTextArea textarea:focus, .stTextInput input:focus {
            border: 2px solid rgba(139, 92, 246, 0.8) !important;
            box-shadow: 0 0 15px rgba(139, 92, 246, 0.5),
                        inset 0 2px 8px rgba(0,0,0,0.3) !important;
        }
        
        /* Select box with metallic effect */
        .stSelectbox > div > div {
            background: linear-gradient(135deg, #2a2a3e 0%, #1f1f3a 100%) !important;
            border: 2px solid rgba(192, 192, 192, 0.3) !important;
            border-radius: 10px !important;
            color: #e9d5ff !important;
            box-shadow: inset 0 2px 8px rgba(0,0,0,0.3) !important;
        }
        
        /* File uploader with metallic styling */
        .stFileUploader > div {
            background: linear-gradient(135deg, #2a2a3e 0%, #1f1f3a 100%) !important;
            border: 2px dashed rgba(139, 92, 246, 0.5) !important;
            border-radius: 12px !important;
            padding: 2rem !important;
        }
        
        /* Info boxes with dark theme */
        .info-box {
            background: linear-gradient(135deg, #2a2a3e 0%, #1f1f3a 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 2px solid rgba(139, 92, 246, 0.4);
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.2);
            color: #e9d5ff;
        }
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #16213e 0%, #1a1a2e 100%);
            border-right: 1px solid rgba(139, 92, 246, 0.3);
        }
        
        /* Headers and text */
        h1, h2, h3, h4, h5, h6 {
            color: #e9d5ff !important;
        }
        
        p, span, div {
            color: #d1d5db;
        }
        
        /* Success/Info/Warning boxes */
        .stSuccess, .stInfo, .stWarning {
            background: rgba(139, 92, 246, 0.1) !important;
            border-left: 4px solid #8b5cf6 !important;
            color: #e9d5ff !important;
        }
        
        /* Audio player */
        .stAudio {
            margin-top: 1rem;
            filter: drop-shadow(0 4px 10px rgba(139, 92, 246, 0.3));
        }
        
        /* Download button */
        .stDownloadButton>button {
            background: linear-gradient(135deg, #c0c0c0 0%, #8b5cf6 100%) !important;
            color: white !important;
            border: 2px solid rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>🎙️ Polyglot Podcaster</h1>
            <p>Zero-Shot Multilingual Voice Cloning | Clone any voice in 23 languages!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 About")
        st.markdown("""
        **Polyglot Podcaster** uses advanced AI to clone voices and make them speak in multiple languages.
        
        **Powered by:**
        - 🤖 Chatterbox TTS (ResembleAI)
        - 🔄 Google Translate API
        - 🎨 Streamlit
        
        **Supports 23 Languages:**
        """)
        
        # Display languages in a nice format
        langs_display = ", ".join(sorted(LANGUAGES.keys()))
        st.caption(langs_display)
        
        st.markdown("---")
        st.markdown("### ⚙️ Tips for Best Results")
        st.markdown("""
        - Use **10-15 second** voice samples
        - Ensure **clear audio** with minimal background noise
        - Speak at a **normal pace** in the sample
        - Keep text **concise** for faster generation
        """)
        
        st.markdown("---")
        st.markdown("### 📖 How to Use")
        st.markdown("""
        1. **Upload** a voice sample (.wav file)
        2. **Type** your message in any language
        3. **Select** the output language
        4. **Click** Generate Speech
        5. **Download** your audio file!
        """)
        
        st.markdown("---")
        st.caption("Created by Amartya Chaudhuri")
    
    # Load model (cached, happens only once)
    model = load_model()
    
    # Two-column layout
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 🎤 Step 1: Upload Voice Sample")
        uploaded_file = st.file_uploader(
            "Choose a .wav file (10-15 seconds recommended)",
            type=['wav'],
            help="Upload a clear audio sample of the voice you want to clone."
        )
        
        if uploaded_file:
            st.success("✅ Voice sample uploaded!")
            st.audio(uploaded_file, format='audio/wav')
        
        st.markdown("### ✍️ Step 2: Enter Your Text")
        target_text = st.text_area(
            "What should the voice say?",
            height=150,
            placeholder="Type your message here in any language...",
            help="Enter the text you want to be spoken. It can be in any language!"
        )
    
    with col2:
        st.markdown("### 🌍 Step 3: Choose Language & Settings")
        
        selected_language = st.selectbox(
            "Output Language",
            options=list(LANGUAGES.keys()),
            help="Select the language for the generated speech"
        )
        language_code = LANGUAGES[selected_language]
        
        # Auto-translate option
        translate_option = st.checkbox(
            "🔄 Auto-translate to selected language",
            value=True,
            help="Automatically translate your text to the selected language"
        )
        
        # Info box
        st.markdown("""
            <div class="info-box">
                <strong>💡 How it works:</strong><br>
                1. Upload a voice sample (your voice or any voice)<br>
                2. Type your message in any language<br>
                3. Select the output language<br>
                4. The AI will clone the voice and speak in the selected language!
            </div>
        """, unsafe_allow_html=True)
    
    # Generate button (full width)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🎵 Generate Speech", type="primary"):
        # Input validation
        if uploaded_file is None:
            st.error("❌ Please upload a voice sample (.wav file) first!")
            return
        
        if not target_text.strip():
            st.error("❌ Please enter some text to generate!")
            return
        
        # Translate text if auto-translate is enabled
        text_to_speak = target_text
        if translate_option:
            try:
                with st.spinner("🔄 Translating text..."):
                    translator = Translator()
                    translation = translator.translate(target_text, dest=language_code)
                    text_to_speak = translation.text
                    
                    # Show translation
                    if translation.src != language_code:
                        st.info(f"📝 Translated from {translation.src.upper()} to {language_code.upper()}:")
                        st.code(text_to_speak, language=None)
                    else:
                        st.info(f"✅ Text is already in {selected_language}")
            except Exception as e:
                st.warning(f"⚠️ Translation failed: {e}. Using original text...")
                text_to_speak = target_text
        
        # Create temporary file for the uploaded audio
        temp_input_path = None
        
        try:
            # Save uploaded file to temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_input:
                temp_input.write(uploaded_file.getvalue())
                temp_input_path = temp_input.name
            
            # Validate audio file
            try:
                import torchaudio as ta
                audio_data, sample_rate = ta.load(temp_input_path)
                st.info(f"📊 Audio info: Shape={audio_data.shape}, Sample rate={sample_rate}Hz, Duration={audio_data.shape[1]/sample_rate:.2f}s")
            except Exception as e:
                st.error(f"⚠️ Could not read audio file: {e}")
                return
            
            # Generate speech
            with st.spinner(f"🎵 Generating audio in {selected_language}... this may take a moment."):
                wav = model.generate(
                    text=text_to_speak,
                    language_id=language_code,
                    audio_prompt_path=temp_input_path
                )
            
            # Save output
            output_path = "output.wav"
            
            # Ensure wav is in correct shape for saving (channels, samples)
            if wav.dim() == 1:
                wav = wav.unsqueeze(0)  # Add channel dimension: (samples,) -> (1, samples)
            elif wav.dim() == 2 and wav.shape[0] > wav.shape[1]:
                wav = wav.T  # Transpose if needed: (samples, channels) -> (channels, samples)
            
            torchaudio.save(
                output_path,
                wav,
                model.sr,
                bits_per_sample=16
            )
            
            # Display success message with celebration
            st.balloons()
            st.success("🎉 Audio generated successfully!")
            
            # Create two columns for result display
            result_col1, result_col2 = st.columns([2, 1])
            
            with result_col1:
                st.markdown("### 🎧 Your Generated Audio")
                st.audio(output_path)
                
                # Download button
                with open(output_path, 'rb') as audio_file:
                    st.download_button(
                        label="📥 Download Audio",
                        data=audio_file,
                        file_name=f"polyglot_output_{selected_language}.wav",
                        mime="audio/wav"
                    )
            
            with result_col2:
                st.markdown("### 📊 Details")
                st.info(f"""
                **Language:** {selected_language}  
                **Code:** {language_code.upper()}  
                **Sample Rate:** {model.sr} Hz  
                **Text Used:**  
                _{text_to_speak[:100]}{'...' if len(text_to_speak) > 100 else ''}_
                """)
            
            # Optional: Display audio info
            with st.expander("🔍 Technical Information"):
                st.write(f"**Language:** {selected_language} ({language_code})")
                st.write(f"**Sample Rate:** {model.sr} Hz")
                st.write(f"**Text Length:** {len(target_text)} characters")
        
        except Exception as e:
            st.error(f"❌ An error occurred during generation: {str(e)}")
        
        finally:
            # Cleanup: Delete temporary input file
            if temp_input_path and os.path.exists(temp_input_path):
                try:
                    os.unlink(temp_input_path)
                except:
                    pass
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray; font-size: 0.9em;'>
        Powered by Chatterbox TTS | Built with Streamlit
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
