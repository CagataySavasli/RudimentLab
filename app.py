# app.py
import streamlit as st
import threading
from lib.metronome import Metronome
from lib.exercise import Exercise


def main():
    st.set_page_config(page_title="RudimentLab", page_icon="🥁", layout="wide")
    st.title("RudimentLab 🥁")
    st.write("Drumming practice: Metronome or guided exercises.")

    # Initialize defaults
    if 'bpm' not in st.session_state:
        st.session_state.bpm = 120
    if 'metronome' not in st.session_state:
        st.session_state.metronome = Metronome(st.session_state.bpm)
    if 'exercise' not in st.session_state:
        st.session_state.exercise = Exercise()

    # BPM controls
    col1, col2 = st.columns(2)
    bpm_input = col1.number_input(
        "Enter BPM", min_value=40, max_value=300,
        value=st.session_state.bpm, step=1, key='bpm_input'
    )
    bpm_slider = col2.slider(
        "Adjust BPM", min_value=40, max_value=300,
        value=st.session_state.bpm, step=1, key='bpm_slider'
    )
    # Sync BPM
    if bpm_input != st.session_state.bpm:
        st.session_state.bpm = bpm_input
    elif bpm_slider != st.session_state.bpm:
        st.session_state.bpm = bpm_slider
    bpm = st.session_state.bpm
    st.write(f"**Current BPM:** {bpm}")

    # Mode selector (no session_state assignment after)
    mode = st.radio(
        "Select mode", ['Metronome', 'Exercise'],
        index=0, key='mode'
    )

    # Update instances
    met = st.session_state.metronome
    ex = st.session_state.exercise
    met.bpm = bpm

    # Mode-specific controls
    if mode == 'Metronome':
        st.subheader("Metronome Mode")
        start_m = col1.button("▶️ Start Metronome", key='start_met')
        stop_m = col2.button("⏹ Stop Metronome", key='stop_met')
        if start_m and not met.running:
            met.running = True
            threading.Thread(target=met.metronome_loop, daemon=True).start()
        if stop_m and met.running:
            met.running = False
    else:
        st.subheader("Exercise Mode")
        notation = st.text_input(
            "Exercise notation (use R and L)",
            value=ex.notation, key='notation'
        )
        ex.notation = notation
        st.write(f"Pattern: {notation}")
        start_e = col1.button("▶️ Start Exercise", key='start_ex')
        stop_e = col2.button("⏹ Stop Exercise", key='stop_ex')
        if start_e and not ex.running:
            ex.running = True
            threading.Thread(target=lambda: ex.exercise_loop(bpm), daemon=True).start()
        if stop_e and ex.running:
            ex.running = False

    st.markdown(
        "*Note: Requires `sounddevice`, `numpy`. Run locally where PortAudio is available.*"
    )


if __name__ == '__main__':
    main()