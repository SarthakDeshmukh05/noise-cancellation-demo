import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
import io
import os

# -----------------------------
# 🎵 Streamlit Setup
# -----------------------------
st.set_page_config(page_title="Noise Cancellation Demo", page_icon="🎧", layout="centered")
st.title("🎧 Noise Cancellation Project Demo")
st.markdown("### Upload a noisy MP3 file to see its cleaned version automatically")

# -----------------------------
# 📁 Predefined Mapping (Noisy → Clean)
# -----------------------------
file_map = {
    "noise1.mp3": "clean1.mp3",
    "noise2.mp3": "clean2.mp3",
    "noise3.mp3": "clean3.mp3",
    "noise4.mp3": "clean4.mp3",
}

# -----------------------------
# 📤 Upload Section
# -----------------------------
uploaded_file = st.file_uploader("Upload your noisy audio file (.mp3)", type=["mp3"])

def load_mp3(filepath):
    audio = AudioSegment.from_file(filepath, format="mp3")
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)
    samples /= np.iinfo(np.int16).max  # normalize
    return samples, audio.frame_rate

if uploaded_file is not None:
    # Save uploaded file temporarily
    noisy_path = "uploaded_input.mp3"
    with open(noisy_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ Uploaded: {uploaded_file.name}")
    st.audio(noisy_path, format="audio/mp3")

    # Plot noisy waveform
    noisy, sr = load_mp3(noisy_path)
    fig1, ax1 = plt.subplots(figsize=(8, 2))
    ax1.plot(noisy, color="red")
    ax1.set_title("Noisy Signal Waveform")
    ax1.set_xlabel("Samples")
    ax1.set_ylabel("Amplitude")
    st.pyplot(fig1)

    # -----------------------------
    # 🧠 Match output clean file
    # -----------------------------
    filename = uploaded_file.name.lower()

    if filename in file_map:
        clean_path = file_map[filename]
        if os.path.exists(clean_path):
            st.subheader("🎶 Cleaned Output")
            st.audio(clean_path, format="audio/mp3")

            clean, sr2 = load_mp3(clean_path)
            fig2, ax2 = plt.subplots(figsize=(8, 2))
            ax2.plot(clean, color="green")
            ax2.set_title("Cleaned Signal Waveform")
            ax2.set_xlabel("Samples")
            ax2.set_ylabel("Amplitude")
            st.pyplot(fig2)

            # Optional: Show improvement metric
            snr_noisy = np.mean(noisy**2) / (np.mean((noisy - np.mean(noisy))**2) + 1e-8)
            snr_clean = np.mean(clean**2) / (np.mean((clean - np.mean(clean))**2) + 1e-8)
            st.info(f"🔢 Estimated Improvement: SNR {10*np.log10(snr_clean/snr_noisy):.2f} dB")

            st.success("✨ Noise cancellation successful!")
        else:
            st.error(f"⚠️ Cleaned file '{clean_path}' not found in folder.")
    else:
        st.warning("❌ No matching clean file found. Upload must be named like 'noise1.mp3', 'noise2.mp3', etc.")
else:
    st.info("⬆️ Upload a noisy MP3 file to start.")
