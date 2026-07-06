import requests
import streamlit as st
from gtts import gTTS
import io

def get_groq_response(input_text, language):
    json_body = {
        "input": {
            "language": language,
            "text": input_text
        },
        "config": {},
        "kwargs": {}
    }
    
    response = requests.post(
        "http://127.0.0.1:8001/chain/invoke",
        json=json_body
    )
    return response.json()

# Map selection names to gTTS language codes
LANG_CODES = {
    "French": "fr",
    "Hindi": "hi",
    "Bengali": "bn",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja",
    "Korean": "ko",
    "Russian": "ru",
    "Italian": "it",
    "Portuguese": "pt",
    "Arabic": "ar",
    "Turkish": "tr",
    "Dutch": "nl",
    "Swedish": "sv",
    "Ukrainian": "uk",
    "Norwegian": "no",
    "Danish": "da",
    "United States English": "en",
    "British English": "en-uk",
    "Finnish": "fi",
    "Polish": "pl",
    "Czech": "cs",
    "Slovak": "sk"
}

st.set_page_config(page_title="AIbot Translator Pro", layout="centered")
st.title("AIbot : Advanced Translation & Speech")

# Inject Custom CSS for the dynamic speaking animation bars
st.markdown("""
<style>
    .audio-container {
        display: flex;
        align-items: center;
        gap: 15px;
        background: #f0f2f6;
        padding: 10px 15px;
        border-radius: 10px;
        margin-top: 10px;
    }
    .playing-animation {
        display: flex;
        align-items: flex-end;
        width: 30px;
        height: 24px;
        gap: 3px;
    }
    .playing-animation span {
        display: block;
        width: 4px;
        background-color: #ff4b4b;
        animation: bounce 1.2s ease-in-out infinite;
        border-radius: 2px;
    }
    .playing-animation span:nth-child(1) { height: 30%; animation-delay: 0.1s; }
    .playing-animation span:nth-child(2) { height: 60%; animation-delay: 0.3s; }
    .playing-animation span:nth-child(3) { height: 90%; animation-delay: 0.5s; }
    .playing-animation span:nth-child(4) { height: 40%; animation-delay: 0.2s; }

    @keyframes bounce {
        0%, 100% { transform: scaleY(1); }
        50% { transform: scaleY(2); }
    }
</style>
""", unsafe_allow_html=True)

# Language selection zone
language = st.selectbox(
    "Select language to translate into:",
    list(LANG_CODES.keys())
)

# Audio Settings Panel
with st.expander("🔊 Advanced Speech Settings"):
    speed_option = st.radio("Playback Speed Profile:", ["Normal", "Slow (Dictation Mode)"], index=0)
    is_slow = True if speed_option == "Slow (Dictation Mode)" else False

# Text input
input_text = st.text_input("Enter text to translate:")

# Output execution block
if input_text:
    with st.spinner("Translating..."):
        try:
            # 1. Fetch text translation from backend
            result = get_groq_response(input_text, language)
            translated_output = result["output"]
            
            st.subheader("Translated Text:")
            st.info(translated_output)
            
            # 2. Generate Audio Track based on user configuration
            with st.spinner("Generating target audio track..."):
                lang_code = LANG_CODES.get(language, "en")
                tts = gTTS(text=translated_output, lang=lang_code, slow=is_slow)
                
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)
            
            # 3. Render Dashboard Player controls & Animations
            st.write("### Audio Controls")
            
            # Layout grouping components
            col_anim, col_player = st.columns([0.1, 0.9])
            
            with col_anim:
                # Displays the dynamic waveform visualizer when audio content is ready
                st.markdown("""
                    <div class="playing-animation">
                        <span></span><span></span><span></span><span></span>
                    </div>
                """, unsafe_allow_html=True)
                
            with col_player:
                # Built-in Streamlit HTML5 audio interface includes play/pause, seek track, volume, 
                # playback speed modifier adjustments, and direct local downloading features automatically!
                st.audio(audio_fp, format="audio/mp3")
                
        except Exception as e:
            st.error(f"Failed to process translation or speech engine: {e}")