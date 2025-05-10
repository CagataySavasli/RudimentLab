# app.py
import streamlit as st
import threading
import json
import numpy as np
from lib.sound_maker import SoundMaker

def main():
    st.set_page_config(page_title="RudimentLab", page_icon="🥁", layout="wide")
    st.title("RudimentLab 🥁")
    st.write("Drumming practice: Metronome or guided exercises.")

    # Determine audio backend
    try:
        import sounddevice as sd
        sd.query_devices()
        backend = 'sd'
    except Exception:
        backend = 'web'

    # BPM state
    if 'bpm' not in st.session_state:
        st.session_state.bpm = 120
    bpm_input = st.number_input("Enter BPM", 40, 300, st.session_state.bpm, 1)
    bpm_slider = st.slider("Adjust BPM", 40, 300, st.session_state.bpm, 1)
    bpm = bpm_input if bpm_input != st.session_state.bpm else bpm_slider
    st.session_state.bpm = bpm
    st.write(f"**Current BPM:** {bpm}")

    # Mode
    mode = st.radio("Select mode", ['Metronome', 'Exercise'])

    # Pattern
    if mode == 'Metronome':
        st.write("**Metronome:** R L L L")
        pattern = ['R'] + ['L'] * 3
    else:
        notation = st.text_input("Exercise notation (R & L)", "RLRL RLRL RRLL RRLL")
        st.write(f"**Pattern:** {notation}")
        pattern = [c for c in notation.replace(' ','').upper() if c in ('R','L')]

    # Buttons
    col1, col2 = st.columns(2)
    start = col1.button("▶️ Start")
    stop  = col2.button("⏹ Stop")

    if backend == 'sd':
        # sounddevice loop
        from lib.metronome import Metronome
        from lib.exercise import Exercise
        if 'metronome' not in st.session_state:
            st.session_state.metronome = Metronome(bpm)
        if 'exercise' not in st.session_state:
            st.session_state.exercise = Exercise()
        met = st.session_state.metronome
        ex = st.session_state.exercise
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
    else:
        # Web Audio API via minimal HTML injection
        sg = SoundGenerator()
        wav = sg.make_pattern_wav(pattern, bpm)
        if start:
            st.audio(wav, format='audio/wav', start_time=0)
        if stop:
            # stop by resetting audio widget
            st.empty()

    st.markdown("*Automatically selects sounddevice locally or browser audio on Cloud.*")

if __name__ == '__main__':
    main()