# app.py
import streamlit as st
import threading
import time
from lib.metronome import Metronome
from lib.exercise import Exercise
from lib.sound_generator import SoundGenerator


def main():
    st.set_page_config(page_title="RudimentLab", page_icon="🥁", layout="wide")
    st.title("RudimentLab 🥁")
    st.write("Drumming practice: Metronome or guided exercises.")

    # Detect backend: sounddevice available locally?
    try:
        import sounddevice as sd
        sd.query_devices()
        backend = 'local'
    except Exception:
        backend = 'browser'

    # BPM controls
    bpm = st.slider("BPM", min_value=40, max_value=300, value=120, step=1)

    # Mode selection
    mode = st.radio("Mode", ['Metronome', 'Exercise'])

    # Pattern
    if mode == 'Metronome':
        st.write("**Metronome pattern:** R L L L")
        pattern = ['R'] + ['L'] * 3
    else:
        notation = st.text_input("Exercise notation (R and L)", "RLRL RLRL RRLL RRLL")
        st.write(f"**Pattern:** {notation}")
        pattern = [c for c in notation.replace(' ','').upper() if c in ('R','L')]

    # Buttons
    col1, col2 = st.columns(2)
    start = col1.button("▶️ Start")
    stop  = col2.button("⏹ Stop")

    if backend == 'local':
        # Use Metronome/Exercise classes with sounddevice
        if 'met' not in st.session_state:
            st.session_state.met = Metronome(bpm)
        if 'ex' not in st.session_state:
            st.session_state.ex = Exercise()
        met = st.session_state.met
        ex = st.session_state.ex
        met.bpm = bpm
        ex_start = False

        if mode == 'Metronome':
            if start and not met.running:
                met.running = True
                threading.Thread(target=met.metronome_loop, daemon=True).start()
            if stop and met.running:
                met.running = False
        else:
            ex.notation = ''.join(pattern)
            if start and not ex.running:
                ex.running = True
                threading.Thread(target=lambda: ex.exercise_loop(bpm), daemon=True).start()
            if stop and ex.running:
                ex.running = False

    else:
        # Browser backend: generate WAV buffer and play via st.audio
        sg = SoundGenerator()
        duration = 30  # seconds of audio
        buf, sr = sg.generate_pattern(pattern, bpm, duration)
        if start:
            st.audio(buf, sample_rate=sr)
        if stop:
            # no direct stop API; restart app or mute
            pass

    st.markdown("*Backend:* **%s** *Note: Local uses sounddevice; browser uses generated WAV via st.audio (30s clips)." % backend)

if __name__ == '__main__':
    main()
