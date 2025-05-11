import streamlit as st
import base64
from metronome import Metronome
from exercise import Exercise

st.set_page_config(page_title="RudimentLab", layout="centered")
st.title("RudimentLab: Practice Metronome & Exercises")

# Initialize audio placeholder for looped playback
audio_placeholder = st.empty()

# Sidebar for feature selection
feature = st.sidebar.selectbox("Select Feature", ["Metronome", "Exercise"])

# Common controls
def get_looping_audio(audio_bytes):
    # Encode to base64 for HTML embedding
    b64 = base64.b64encode(audio_bytes).decode()
    return f"<audio autoplay loop><source src='data:audio/wav;base64,{b64}' type='audio/wav'></audio>"

if feature == "Metronome":
    st.header("Metronome")
    bpm = st.number_input("BPM", min_value=40, max_value=480, value=120)
    pattern_input = st.text_input("Pattern (optional)", value="RLLL")
    start = st.button("Start Metronome")
    stop = st.button("Stop")

    if start:
        metro = Metronome(bpm)
        metro.set_pattern(pattern_input)
        audio_bytes = metro.get_audio()
        html = get_looping_audio(audio_bytes)
        audio_placeholder.markdown(html, unsafe_allow_html=True)

    if stop:
        audio_placeholder.empty()

elif feature == "Exercise":
    st.header("Exercise")
    bpm = st.number_input("BPM", min_value=40, max_value=480, value=100)
    notation = st.text_input("Enter Notation (e.g. RLRL RRLL)", value="RLRL RLRL RRLL RRLL")
    start = st.button("Start Exercise")
    stop = st.button("Stop")

    if start and notation:
        ex = Exercise(bpm, notation)
        audio_bytes = ex.get_audio()
        html = get_looping_audio(audio_bytes)
        audio_placeholder.markdown(html, unsafe_allow_html=True)

    if stop:
        audio_placeholder.empty()