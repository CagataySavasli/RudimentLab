# app.py
import streamlit as st
import threading
from lib.metronome import Metronome
from lib.exercise import Exercise


def main():
    st.set_page_config(page_title="RudimentLab", page_icon="🥁", layout="wide")
    st.title("RudimentLab 🥁")
    st.write("Drumming practice: Metronome or guided exercises without HTML.")

    # Initialize session_state defaults
    if 'bpm' not in st.session_state:
        st.session_state.bpm = 120
    if 'mode' not in st.session_state:
        st.session_state.mode = 'Metronome'
    if 'metronome' not in st.session_state:
        st.session_state.metronome = Metronome(st.session_state.bpm)
    if 'exercise' not in st.session_state:
        st.session_state.exercise = Exercise()

    met = st.session_state.metronome
    ex = st.session_state.exercise

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

    # Mode selector
    mode = st.radio(
        "Select mode", ['Metronome', 'Exercise'],
        index=0 if st.session_state.mode=='Metronome' else 1,
        key='mode_radio'
    )
    st.session_state.mode = mode

    # Metronome Mode
    if mode == 'Metronome':
        st.subheader("Metronome Mode")
        start = col1.button("▶️ Start Metronome", key='start_met')
        stop = col2.button("⏹ Stop Metronome", key='stop_met')
        met.bpm = bpm
        if start and not met.running:
            met.running = True
            threading.Thread(target=met.metronome_loop, daemon=True).start()
        if stop and met.running:
            met.running = False

    # Exercise Mode
    else:
        st.subheader("Exercise Mode")
        notation = st.text_input(
            "Enter exercise notation (R and L)",
            value=ex.notation, key='notation_input'
        )
        ex.notation = notation
        st.write(f"Pattern: {notation}")

        start = col1.button("▶️ Start Exercise", key='start_ex')
        stop = col2.button("⏹ Stop Exercise", key='stop_ex')
        if start and not ex.running:
            ex.running = True
            threading.Thread(target=lambda: ex.exercise_loop(bpm), daemon=True).start()
        if stop and ex.running:
            ex.running = False

    st.markdown(
        "*Note: Requires local audio hardware and `sounddevice`, `numpy`.*"
    )


if __name__ == '__main__':
    main()