import streamlit as st
import torch
import torchaudio
import tempfile
import os
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

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
        layout="centered"
    )
    
    # Title
    st.title("🎙️ Polyglot Podcaster: Zero-Shot Multilingual Voice Cloning")
    st.markdown("---")
    
    # Load model (cached, happens only once)
    model = load_model()
    
    # UI Components
    st.header("📤 Upload Voice Sample")
    uploaded_file = st.file_uploader(
        "Upload a .wav file",
        type=['wav'],
        help="Please upload a 10-15 second .wav file of the target voice."
    )
    
    st.header("✍️ Enter Target Text")
    target_text = st.text_area(
        "Text to generate",
        height=150,
        placeholder="Enter the text you want to generate in the selected language..."
    )
    
    st.header("🌍 Select Language")
    selected_language = st.selectbox(
        "Choose the language of your text",
        options=list(LANGUAGES.keys())
    )
    language_code = LANGUAGES[selected_language]
    
    st.markdown("---")
    
    # Generate button
    if st.button("🎵 Generate Speech", type="primary"):
        # Input validation
        if uploaded_file is None:
            st.error("❌ Please upload a voice sample (.wav file) first!")
            return
        
        if not target_text.strip():
            st.error("❌ Please enter some text to generate!")
            return
        
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
                    text=target_text,
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
            
            # Display success message and audio
            st.success("✅ Audio generated successfully!")
            st.audio(output_path)
            
            # Optional: Display audio info
            with st.expander("ℹ️ Audio Information"):
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
