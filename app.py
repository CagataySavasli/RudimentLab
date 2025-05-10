# app.py
import streamlit as st
from lib.audio_backend import LocalAudioBackend, BrowserAudioBackend


def main():
    st.set_page_config(page_title="RudimentLab", page_icon="🥁", layout="wide")
    st.title("RudimentLab 🥁")
    st.write("Drumming practice: Metronome or guided exercises.")

    # Detect runtime environment
    try:
        import sounddevice as sd
        sd.query_devices()
        backend_type = 'browser'
    except Exception:
        backend_type = 'browser'

    # Instantiate appropriate backend
    if backend_type == 'local':
        # Persist local backend across reruns to maintain running state
        if 'local_backend' not in st.session_state:
            st.session_state.local_backend = LocalAudioBackend(st.session_state.get('bpm', 120))
        backend = st.session_state.local_backend
    else:
        # Always fresh browser backend for each run
        backend = BrowserAudioBackend()
        # Prepare placeholder for browser audio
        audio_ph = st.empty()
        backend.set_placeholder(audio_ph)

    # BPM controls with sync
    if 'bpm' not in st.session_state:
        st.session_state.bpm = 120
    col1, col2 = st.columns(2)
    new_bpm = col1.number_input("Enter BPM", 40, 300, st.session_state.bpm, 1, key='bpm_input')
    new_bpm_slider = col2.slider("Adjust BPM", 40, 300, st.session_state.bpm, 1, key='bpm_slider')
    bpm = new_bpm if new_bpm != st.session_state.bpm else new_bpm_slider
    st.session_state.bpm = bpm
    st.write(f"**Current BPM:** {bpm}")

    # Mode selection
    mode = st.radio("Mode", ['Metronome', 'Exercise'], key='mode_radio')

    # Pattern definition
    if mode == 'Metronome':
        st.write("**Pattern:** R L L L")
        pattern = ['R'] + ['L'] * 3
    else:
        notation = st.text_input("Exercise notation (use R and L)", st.session_state.get('notation', 'RLRL RLRL RRLL RRLL'), key='notation_input')
        st.session_state.notation = notation
        st.write(f"**Pattern:** {notation}")
        pattern = [c for c in notation.replace(' ', '').upper() if c in ('R', 'L')]

    # Start/Stop buttons
    start = col1.button("▶️ Start", key='start')
    stop = col2.button("⏹ Stop", key='stop')

    # Play or stop
    if start:
        if mode == 'Metronome':
            backend.play_metronome(bpm)
        else:
            backend.play_exercise(pattern, bpm)
    if stop:
        if mode == 'Metronome':
            backend.stop_metronome()
        else:
            backend.stop_exercise()

    st.markdown(
        f"*Audio backend:* **{backend_type}**  *Local: uses sounddevice; Browser: uses audio playback via placeholder.*"
    )

if __name__ == '__main__':
    main()
