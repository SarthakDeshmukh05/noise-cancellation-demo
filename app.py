import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os

# -----------------------------
# 🎧 App Setup
# -----------------------------
st.set_page_config(page_title="Noise Cancellation Demo", page_icon="🎵", layout="centered")
st.title("🎧 Noise Cancellation Project Demo")
st.markdown("### Upload your noisy audio file to see its cleaned output")

# -----------------------------
# 📁 Predefined Mapping
# -----------------------------
file_map = {
    "noise1.wav": "clean1.wav",
    "noise2.wav": "clean2.wav",
    "noise3.wav": "clean3.wav",
    "noise4.wav": "clean4.wav"
}

# -----------------------------
# 📤 File Upload Section
# -----------------------------
uploaded_file = st.file_uploader("Upload a noisy audio file (.wav)", type=["wav"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    noisy_path = os.path.join("temp_input.wav")
    with open(noisy_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display uploaded file name
    st.success(f"✅ Uploaded: {uploaded_file.name}")

    # Plot uploaded noisy waveform
    fs1, noisy = wavfile.read(noisy_path)
    if noisy.dtype != np.float32:
        noisy = noisy.astype(np.float32) / np.iinfo(noisy.dtype).max

    st.audio(noisy_path, format="audio/wav")
    fig1, ax1 = plt.subplots(figsize=(8, 2))
    ax1.plot(noisy, color="red")
    ax1.set_title("Noisy Signal Waveform")
    ax1.set_xlabel("Samples")
    ax1.set_ylabel("Amplitude")
    st.pyplot(fig1)

    # -----------------------------
    # 🧠 Match Output File
    # -----------------------------
    file_name = uploaded_file.name.lower()

    if file_name in file_map:
        clean_path = file_map[file_name]

        if os.path.exists(clean_path):
            st.subheader("🎶 Cleaned Output")
            fs2, clean = wavfile.read(clean_path)
            if clean.dtype != np.float32:
                clean = clean.astype(np.float32) / np.iinfo(clean.dtype).max

            st.audio(clean_path, format="audio/wav")

            fig2, ax2 = plt.subplots(figsize=(8, 2))
            ax2.plot(clean, color="green")
            ax2.set_title("Cleaned Signal Waveform")
            ax2.set_xlabel("Samples")
            ax2.set_ylabel("Amplitude")
            st.pyplot(fig2)

            st.success("✨ Noise cancellation successful!")
        else:
            st.error(f"⚠️ Output file not found for {file_name}")
    else:
        st.warning("❌ No matching clean file found for this input. Please upload a valid noisy file name (e.g. noise1.wav, noise2.wav).")

else:
    st.info("⬆️ Upload a noisy audio file to begin.")
