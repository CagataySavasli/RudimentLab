# app.py
import streamlit as st
from lib.audio_backend import LocalAudioBackend, BrowserAudioBackend

def main():
    st.set_page_config(page_title="RudimentLab", page_icon="🥁", layout="wide")
    st.title("RudimentLab 🥁")
    st.write("Drumming practice: Metronome or guided exercises, browser-only mode.")

    # Always browser backend
    if 'backend' not in st.session_state:
        st.session_state.backend = BrowserAudioBackend()
    backend = st.session_state.backend
    audio_ph = st.empty()
    backend.set_placeholder(audio_ph)

    # BPM sync
    if 'bpm' not in st.session_state:
        st.session_state.bpm = 120
    col1, col2 = st.columns(2)
    nb = col1.number_input("Enter BPM", 40, 300, st.session_state.bpm, 1, key='bpm_in')
    sb = col2.slider("Adjust BPM", 40, 300, st.session_state.bpm, 1, key='bpm_sl')
    bpm = nb if nb != st.session_state.bpm else sb
    st.session_state.bpm = bpm
    st.write(f"**Current BPM:** {bpm}")

    # Mode
    mode = st.radio("Mode", ["Metronome", "Exercise"], key='mode')

    # Pattern
    if mode == "Metronome":
        pattern = ['R','L','L','L']
        st.write("**Pattern:** R L L L")
    else:
        if 'notation' not in st.session_state:
            st.session_state.notation = "RLRL RLRL RRLL RRLL"
        nt = st.text_input("Exercise notation (R and L)", st.session_state.notation, key='nt')
        st.session_state.notation = nt
        pattern = [c for c in nt.replace(' ','').upper() if c in ('R','L')]
        st.write(f"**Pattern:** {nt}")

    # Buttons
    start = col1.button("▶️ Start", key='st')
    stop = col2.button("⏹ Stop", key='sp')

    if start:
        backend.play_pattern(pattern, bpm)
    if stop:
        backend.stop()

    st.markdown("*Browser-only backend using pre-generated R/L audio URIs. No delays.*")

if __name__ == '__main__':
    main()
