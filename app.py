import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import os
import tempfile

st.set_page_config(page_title="Noise Cancellation Demo", page_icon="🎧", layout="centered")
st.title("🎧 Noise Cancellation Project Demo")
st.markdown("### Upload a noisy MP3 file to see its cleaned output")

# Mapping (input → output)
file_map = {
    "noise1.mp3": "clean1.mp3",
    "noise2.mp3": "clean2.mp3",
    "noise3.mp3": "clean3.mp3",
    "noise4.mp3": "clean4.mp3"
}

# Function to convert mp3 → wav for plotting
def mp3_to_wav(mp3_path):
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
    subprocess.run(["ffmpeg", "-y", "-i", mp3_path, temp_wav], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return temp_wav

# Upload area
uploaded_file = st.file_uploader("Upload your noisy audio file (.mp3)", type=["mp3"])

if uploaded_file:
    noisy_path = "uploaded_input.mp3"
    with open(noisy_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ Uploaded: {uploaded_file.name}")
    st.audio(noisy_path, format="audio/mp3")

    # Convert to wav for waveform
    wav_noisy = mp3_to_wav(noisy_path)
    import scipy.io.wavfile as wav
    fs1, noisy = wav.read(wav_noisy)
    noisy = noisy.astype(np.float32) / np.iinfo(noisy.dtype).max

    fig1, ax1 = plt.subplots(figsize=(8, 2))
    ax1.plot(noisy, color="red")
    ax1.set_title("Noisy Signal Waveform")
    st.pyplot(fig1)

    # Match corresponding clean file
    filename = uploaded_file.name.lower()
    if filename in file_map:
        clean_path = file_map[filename]
        if os.path.exists(clean_path):
            st.subheader("🎶 Cleaned Output")
            st.audio(clean_path, format="audio/mp3")

            # Convert clean to wav for plotting
            wav_clean = mp3_to_wav(clean_path)
            fs2, clean = wav.read(wav_clean)
            clean = clean.astype(np.float32) / np.iinfo(clean.dtype).max

            fig2, ax2 = plt.subplots(figsize=(8, 2))
            ax2.plot(clean, color="green")
            ax2.set_title("Cleaned Signal Waveform")
            st.pyplot(fig2)

            # Optional: Basic SNR comparison
            snr_noisy = np.mean(noisy**2) / (np.mean((noisy - np.mean(noisy))**2) + 1e-8)
            snr_clean = np.mean(clean**2) / (np.mean((clean - np.mean(clean))**2) + 1e-8)
            st.info(f"🔢 Estimated SNR Improvement: {10*np.log10(snr_clean/snr_noisy):.2f} dB")

            st.success("✨ Noise cancellation successful!")
        else:
            st.error(f"⚠️ Clean file '{clean_path}' not found.")
    else:
        st.warning("❌ Unknown filename. Upload noise1.mp3 – noise4.mp3 only.")
else:
    st.info("⬆️ Upload an MP3 file to start.")
