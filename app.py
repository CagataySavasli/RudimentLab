# app.py
import streamlit as st
from lib.sound_generator import SoundGenerator
from lib.metronome import Metronome
from lib.exercise import Exercise
import time
import threading


def main():
    st.set_page_config(page_title="RudimentLab", page_icon="🥁", layout="wide")
    st.title("RudimentLab 🥁")
    st.write("Drumming practice UI that runs both locally (sounddevice) and on Streamlit Cloud (browser audio).")

    # Detect if sounddevice is available (local) or not (deploy/cloud)
    try:
        import sounddevice as sd
        sd.query_devices()
        backend = 'local'
    except Exception:
        backend = 'browser'

    # BPM input & slider synchronized via session_state
    if 'bpm' not in st.session_state:
        st.session_state.bpm = 120
    bpm = st.session_state.bpm
    col1, col2 = st.columns(2)
    new_bpm = col1.number_input("BPM", min_value=40, max_value=300, value=bpm, step=1, key='bpm_input')
    new_bpm_slider = col2.slider("BPM Slider", min_value=40, max_value=300, value=bpm, step=1, key='bpm_slider')
    if new_bpm != bpm:
        bpm = new_bpm
    elif new_bpm_slider != bpm:
        bpm = new_bpm_slider
    st.session_state.bpm = bpm
    st.write(f"**Current BPM:** {bpm}")

    # Mode selection
    mode = st.radio("Mode", ['Metronome', 'Exercise'], key='mode_radio')

    # Pattern definition
    if mode == 'Metronome':
        st.write("**Metronome pattern:** Accent on 1st beat (R L L L)")
        pattern = ['R'] + ['L'] * 3
    else:
        notation = st.text_input("Exercise notation (use R and L)", "RLRL RLRL RRLL RRLL", key='notation_input')
        st.write(f"**Pattern:** {notation}")
        pattern = [c for c in notation.replace(' ', '').upper() if c in ('R','L')]

    # Start/Stop buttons
    start = col1.button("▶️ Start", key='start')
    stop  = col2.button("⏹ Stop", key='stop')

    # LOCAL: use threading + sounddevice via Metronome/Exercise classes
    if backend == 'local':
        # initialize if needed
        if 'met' not in st.session_state:
            st.session_state.met = Metronome(bpm)
        if 'ex' not in st.session_state:
            st.session_state.ex = Exercise()
        met = st.session_state.met
        ex  = st.session_state.ex
        met.bpm = bpm
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

    # BROWSER: generate WAV clip and play via st.audio
    else:
        sg = SoundGenerator()
        # generate e.g. 10 seconds of audio (looping pattern)
        wav_bytes, sr = sg.generate_pattern(pattern, bpm, duration=10)
        if start:
            st.audio(wav_bytes, format='audio/wav', sample_rate=sr)
        if stop:
            # no direct stop for st.audio; re-render clears audio
            st.empty()

    st.markdown(
        f"*Backend:* **{backend}** *Note:* Local uses sounddevice; Cloud uses browser audio (st.audio)."
    )

if __name__ == '__main__':
    main()