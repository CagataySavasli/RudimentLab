# app.py
import streamlit as st
import streamlit.components.v1 as components
import json

# Web Audio scheduler without threads, with synced BPM input and slider

def main():
    st.set_page_config(page_title="RudimentLab", page_icon="🥁", layout="wide")
    st.title("RudimentLab 🥁")
    st.write("Drumming practice: Metronome or guided exercises (no threads).")

    # Initialize BPM in session state
    if 'bpm' not in st.session_state:
        st.session_state.bpm = 120
    # Helper to sync widgets
    def sync_bpm(widget_key):
        new_val = st.session_state[widget_key]
        st.session_state.bpm = new_val
        st.session_state.bpm_input = new_val
        st.session_state.bpm_slider = new_val

    # Set initial widget states if missing
    if 'bpm_input' not in st.session_state:
        st.session_state.bpm_input = st.session_state.bpm
    if 'bpm_slider' not in st.session_state:
        st.session_state.bpm_slider = st.session_state.bpm

    # BPM controls
    bpm_input = st.number_input(
        "Enter BPM", 40, 300,
        value=st.session_state.bpm_input,
        key='bpm_input',
        on_change=sync_bpm,
        args=('bpm_input',)
    )
    bpm_slider = st.slider(
        "Adjust BPM", 40, 300,
        value=st.session_state.bpm_slider,
        key='bpm_slider',
        on_change=sync_bpm,
        args=('bpm_slider',)
    )
    bpm = st.session_state.bpm
    st.write(f"**Current BPM:** {bpm}")

    # Mode selection
    mode = st.radio("Mode", ["Metronome", "Exercise"], key="mode")

    # Pattern setup
    if mode == "Metronome":
        st.write("**Metronome:** Accent on first beat")
        pattern = ["R"] + ["L"] * 3
    else:
        notation = st.text_input(
            "Exercise notation (R and L)",
            "RLRL RLRL RRLL RRLL",
            key="notation"
        )
        st.write(f"**Pattern:** {notation}")
        pattern = [c for c in notation.replace(" ","").upper() if c in ("R","L")]

    # Start/Stop controls
    start = st.button("▶️ Start", key="start")
    stop  = st.button("⏹ Stop", key="stop")

    # Prepare JS parameters
    pattern_js = json.dumps(pattern)
    interval_ms = 60000 / bpm

    # Inject Web Audio API JavaScript
    if start and pattern:
        js = f"""
        <script>
        if(window.metInterval) clearInterval(window.metInterval);
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        const ctx = new AudioContext();
        const pattern = {pattern_js};
        const interval = {interval_ms};
        let idx = 0;
        function playBeat() {{
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.frequency.value = pattern[idx] === 'R' ? 440 : 880;
            osc.connect(gain).connect(ctx.destination);
            gain.gain.setValueAtTime(1, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.05);
            osc.start(ctx.currentTime);
            osc.stop(ctx.currentTime + 0.05);
            idx = (idx + 1) % pattern.length;
        }}
        playBeat();
        window.metInterval = setInterval(playBeat, interval);
        </script>
        """
        components.html(js, height=0)  # removed key to fix IframeMixin error

    if stop:
        components.html(
            "<script>if(window.metInterval){clearInterval(window.metInterval);window.metInterval=null;}</script>",
            height=0  # removed key to fix IframeMixin error
        )

    st.markdown("*Implementation uses browser Web Audio API—no Python threads or server-side audio.*")


if __name__ == '__main__':
    main()  # single entry point
