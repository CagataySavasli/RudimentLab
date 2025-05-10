# app.py
import streamlit as st
import threading
from lib.audio_backend import LocalAudioBackend, BrowserAudioBackend


def main():
    st.set_page_config(page_title="RudimentLab", page_icon="🥁", layout="wide")
    st.title("RudimentLab 🥁")
    st.write("Drumming practice: Metronome or guided exercises. Have Fun !!!")

    # Determine backend: local if sounddevice available, else browser
    try:
        import sounddevice as sd
        sd.query_devices()
        backend_type = 'local'
    except Exception:
        backend_type = 'browser'

    # Instantiate backend once
    if 'audio_backend' not in st.session_state:
        if backend_type == 'local':
            st.session_state.audio_backend = LocalAudioBackend(st.session_state.get('bpm', 120))
        else:
            st.session_state.audio_backend = BrowserAudioBackend()
    backend = st.session_state.audio_backend

    # BPM controls
    if 'bpm' not in st.session_state:
        st.session_state.bpm = 120
    col1, col2 = st.columns(2)
    new_bpm = col1.number_input("Enter BPM", 40, 300, st.session_state.bpm, 1, key='bpm_input')
    new_bpm_slider = col2.slider("Adjust BPM", 40, 300, st.session_state.bpm, 1, key='bpm_slider')
    # Sync BPM
    bpm = new_bpm if new_bpm != st.session_state.bpm else new_bpm_slider
    st.session_state.bpm = bpm
    st.write(f"**Current BPM:** {bpm}")

    # Mode selection
    mode = st.radio("Mode", ['Metronome', 'Exercise'], key='mode_radio')

    # Pattern
    if mode == 'Metronome':
        st.write("**Pattern:** R L L L")
        pattern = ['R'] + ['L'] * 3
    else:
        default_notation = st.session_state.get('notation', 'RLRL RLRL RRLL RRLL')
        notation = st.text_input("Exercise notation (use R and L)", default_notation, key='notation_input')
        st.session_state.notation = notation
        st.write(f"**Pattern:** {notation}")
        pattern = [c for c in notation.replace(' ', '').upper() if c in ('R', 'L')]

    # Prepare browser backend placeholder
    if backend_type == 'browser':
        if 'audio_ph' not in st.session_state:
            st.session_state.audio_ph = st.empty()
        backend.set_placeholder(st.session_state.audio_ph)

    # Start/Stop buttons
    start = col1.button("▶️ Start", key='start')
    stop  = col2.button("⏹ Stop", key='stop')

    # Play or stop based on mode and backend
    if start and mode == 'Metronome':
        backend.play_metronome(bpm)
    if start and mode == 'Exercise':
        backend.play_exercise(pattern, bpm)
    if stop and mode == 'Metronome':
        backend.stop_metronome()
    if stop and mode == 'Exercise':
        backend.stop_exercise()

    st.markdown(
        f"*Audio backend:* **{backend_type}**\n"
        "*Local uses sounddevice; Browser generates pattern buffer via SoundGenerator.*"
    )

if __name__ == '__main__':
    main()