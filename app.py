# app.py
import streamlit as st
import base64
from lib.sound_maker import SoundMaker

# Utility to embed WAV bytes in HTML audio tag

def get_audio_tag(wav_bytes: bytes) -> str:
    b64 = base64.b64encode(wav_bytes).decode()
    return f'<audio src="data:audio/wav;base64,{b64}" autoplay loop></audio>'


def main():
    st.set_page_config(page_title="RudimentLab", page_icon="🥁", layout="wide")
    st.title("RudimentLab 🥁")
    st.write("Practice your drumming rudiments with a built‑in metronome and customizable exercises.")

    # Initialize SoundMaker and placeholder
    if 'sm' not in st.session_state:
        st.session_state.sm = SoundMaker()
    if 'audio_placeholder' not in st.session_state:
        st.session_state.audio_placeholder = st.empty()

    sm = st.session_state.sm
    placeholder = st.session_state.audio_placeholder

    # BPM controls
    if 'bpm' not in st.session_state:
        st.session_state.bpm = 120
    bpm_direct = st.number_input(
        "Enter BPM directly", min_value=40, max_value=300,
        value=st.session_state.bpm, step=1, key="bpm_direct"
    )
    bpm_slider = st.slider(
        "Or adjust BPM with slider", min_value=40, max_value=300,
        value=st.session_state.bpm, step=1, key="bpm_slider"
    )
    # Sync BPM
    if bpm_direct != st.session_state.bpm:
        st.session_state.bpm = bpm_direct
    elif bpm_slider != st.session_state.bpm:
        st.session_state.bpm = bpm_slider
    bpm = st.session_state.bpm
    st.write(f"**Current BPM:** {bpm}")

    # Mode selection
    mode = st.radio("Select mode", ["Metronome", "Exercise"], index=0, key="mode")

    # Determine pattern
    if mode == "Metronome":
        pattern = ['R'] + ['L'] * 3  # accent on first beat
        st.write("**Metronome mode**: clear click with accent pattern R L L L")
    else:
        notation = st.text_input(
            "Enter exercise notation (use R and L separated by spaces)",
            value="RLRL RLRL RRLL RRLL", key="notation"
        )
        # extract R/L symbols
        pattern = [c.upper() for c in notation if c.upper() in ("R", "L")]
        st.write("**Exercise pattern:**", notation)

    # Start/Stop buttons
    col1, col2 = st.columns(2)
    if col1.button("▶️ Start", key="start"):
        if pattern:
            wav = sm.make_pattern_wav(pattern, bpm)
            tag = get_audio_tag(wav)
            placeholder.markdown(tag, unsafe_allow_html=True)
    if col2.button("⏹ Stop", key="stop"):
        placeholder.empty()

    st.markdown("*Note: Requires `numpy`, `scipy`, and `streamlit`. " \
                "Embed this in Streamlit Cloud or run locally.*")


if __name__ == "__main__":
    main()