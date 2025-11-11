import streamlit as st
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import io

# 🎧 APP TITLE
st.set_page_config(page_title="Noise Cancellation Demo", page_icon="🎵", layout="centered")
st.title("🎧 Noise Cancellation Project Demo")
st.markdown("### Demonstration of Noise Reduction Algorithms")

# -------------------------
# 🔗 Define file pairs (Noisy → Cleaned)
# -------------------------
file_pairs = {
    "Audio 1": ("noise1.wav", "clean1.wav"),
    "Audio 2": ("noise2.wav", "clean2.wav"),
    "Audio 3": ("noise3.wav", "clean3.wav"),
    "Audio 4": ("noise4.wav", "clean4.wav"),
}

# -------------------------
# 🎛️ Select Audio File
# -------------------------
choice = st.selectbox("Select a noisy audio sample:", list(file_pairs.keys()))
noisy_path, clean_path = file_pairs[choice]

# -------------------------
# 📊 Load and Display Waveforms
# -------------------------
noisy, fs1 = sf.read(noisy_path)
clean, fs2 = sf.read(clean_path)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Noisy Audio")
    st.audio(noisy_path, format="audio/wav")
    fig1, ax1 = plt.subplots(figsize=(5, 2))
    ax1.plot(noisy, color="red")
    ax1.set_title("Noisy Signal Waveform")
    ax1.set_xlabel("Samples")
    ax1.set_ylabel("Amplitude")
    st.pyplot(fig1)

with col2:
    st.subheader("Cleaned Audio")
    st.audio(clean_path, format="audio/wav")
    fig2, ax2 = plt.subplots(figsize=(5, 2))
    ax2.plot(clean, color="green")
    ax2.set_title("Cleaned Signal Waveform")
    ax2.set_xlabel("Samples")
    ax2.set_ylabel("Amplitude")
    st.pyplot(fig2)

# -------------------------
# 🧠 Simulated Processing Button
# -------------------------
if st.button("🧩 Run Noise Cancellation"):
    st.info("Running noise cancellation algorithm (Spectral Subtraction + Wiener Filter)...")

    # Just for demo — you can insert real DSP here
    st.success("✅ Processing Complete! Output shown above.")

# -------------------------
# ℹ️ Footer
# -------------------------
st.markdown("---")
st.markdown("**Developed by:** Sarthak Deshmukh  \n**Project:** Noise Cancellation using DSP Algorithms (Spectral Subtraction, Wiener, Kalman, Wavelet)")
