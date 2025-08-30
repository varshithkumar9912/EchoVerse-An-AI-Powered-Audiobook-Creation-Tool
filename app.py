import streamlit as st
from gtts import gTTS
import os

# ================= FUNCTIONS =================
def rewrite_text(text, tone):
    """Simple mock rewrite logic for demo"""
    if tone == "Neutral":
        return text
    elif tone == "Suspenseful":
        return text.replace(".", "... Something unexpected might happen.")
    elif tone == "Inspiring":
        return text.replace(".", "! Believe in yourself.")
    return text

def generate_audio_gtts(text, file_name="audiobook.mp3", lang="en"):
    """Generate audio using gTTS"""
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(file_name)
        return file_name
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return None

# ================= STREAMLIT APP =================
st.set_page_config(page_title="EchoVerse – AI Audiobook Tool", layout="centered")
st.title("📚 EchoVerse – AI-Powered Audiobook Creation Tool (Free Version)")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
tone = st.selectbox("🎭 Choose Tone", ["Neutral", "Suspenseful", "Inspiring"])

if uploaded_file:
    try:
        # Read file
        text = uploaded_file.read().decode("utf-8")
        
        # Display original text
        st.subheader("📖 Original Text")
        st.write(text)

        # Adapt tone
        adapted_text = rewrite_text(text, tone)

        # Show side-by-side comparison
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Original**")
            st.write(text)
        with col2:
            st.markdown(f"**{tone} Version**")
            st.write(adapted_text)

        # Generate audiobook
        if st.button("🎧 Generate Audiobook"):
            file_path = generate_audio_gtts(adapted_text)
            if file_path:
                with open(file_path, "rb") as f:
                    audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/mp3")
                st.download_button("⬇️ Download MP3", audio_bytes, file_name="audiobook.mp3")
    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload a .txt file to get started.")
