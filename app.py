import streamlit as st
import threading
from lib.metronome import Metronome
from lib.exercise import Exercise

def main():
    st.set_page_config(page_title="RudimentLab", page_icon="🥁", layout="wide")
    st.title("RudimentLab 🥁")
    st.write("Practice your drumming rudiments with a customizable metronome and guided exercises.")

    # Initialize BPM state
    if 'metronome_bpm' not in st.session_state:
        st.session_state.metronome_bpm = 120

    # Direct number input for BPM
    bpm_direct = st.number_input(
        "Enter BPM directly",
        min_value=40, max_value=300,
        value=st.session_state.metronome_bpm,
        step=1, key="bpm_direct"
    )
    # Slider input for BPM
    bpm_slider = st.slider(
        "Adjust BPM with slider",
        min_value=40, max_value=300,
        value=st.session_state.metronome_bpm,
        step=1, key="bpm_slider"
    )
    # Synchronize BPM value
    if bpm_direct != st.session_state.metronome_bpm:
        st.session_state.metronome_bpm = bpm_direct
    elif bpm_slider != st.session_state.metronome_bpm:
        st.session_state.metronome_bpm = bpm_slider
    bpm = st.session_state.metronome_bpm

    # Mode selection: Metronome or Exercise
    mode = st.radio(
        "Select mode", ["Metronome", "Exercise"],
        index=0, key="mode"
    )
    st.write(f"**Current BPM:** {bpm}")

    # Initialize instances in session state
    if 'metronome' not in st.session_state:
        st.session_state.metronome = Metronome(bpm)
    if 'exercise' not in st.session_state:
        st.session_state.exercise = Exercise()
    met = st.session_state.metronome
    ex = st.session_state.exercise

    # Update metronome BPM
    met.bpm = bpm

    if mode == "Metronome":
        col1, col2 = st.columns(2)
        if col1.button("▶️ Start Metronome", key="start_metronome"):
            if not met.running:
                met.running = True
                st.info(f"Metronome started at {bpm} BPM")
                t = threading.Thread(target=met.metronome_loop, daemon=True)
                t.start()
                st.session_state._metronome_thread = t
        if col2.button("⏹ Stop Metronome", key="stop_metronome"):
            if met.running:
                met.running = False
                st.info("Metronome stopped.")

    else:  # Exercise mode
        # Notation input for exercise
        notation = st.text_input(
            "Enter exercise notation (use R and L with spaces)",
            value=ex.notation, key="notation"
        )
        ex.notation = notation
        st.write("**Exercise Pattern:**", notation)

        col1, col2 = st.columns(2)
        if col1.button("▶️ Start Exercise", key="start_exercise"):
            if not ex.running:
                ex.running = True
                st.info(f"Exercise started at {bpm} BPM")
                t_ex = threading.Thread(target=lambda: ex.exercise_loop(bpm), daemon=True)
                t_ex.start()
                st.session_state._exercise_thread = t_ex
        if col2.button("⏹ Stop Exercise", key="stop_exercise"):
            if ex.running:
                ex.running = False
                st.info("Exercise stopped.")

    st.markdown(
        "*Note: Install dependencies with `pip install streamlit sounddevice numpy`*"
    )

if __name__ == "__main__":
    main()
