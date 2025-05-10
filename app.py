# app.py
import streamlit as st
import streamlit.components.v1 as components
import json

# Web Audio scheduler without threads

def main():
    st.set_page_config(page_title="RudimentLab", page_icon="🥁", layout="wide")
    st.title("RudimentLab 🥁")
    st.write("Drumming practice: Metronome or guided exercises.")

    # BPM controls
    bpm = st.slider("BPM", 40, 300, 120, key="bpm")
    st.write(f"**Current BPM:** {bpm}")

    # Mode selection
    mode = st.radio("Mode", ["Metronome", "Exercise"], key="mode")

    # Pattern setup
    if mode == "Metronome":
        st.write("**Metronome:** Accent on first beat")
        pattern = ["R"] + ["L"] * 3
    else:
        notation = st.text_input("Exercise notation (R and L)", "RLRL RLRL RRLL RRLL", key="notation")
        st.write(f"**Pattern:** {notation}")
        pattern = [c for c in notation.replace(" ","").upper() if c in ("R","L")]

    # Start/Stop controls
    start = st.button("▶️ Start", key="start")
    stop  = st.button("⏹ Stop", key="stop")

    # Convert pattern to JSON for JS
    pattern_js = json.dumps(pattern)
    interval_ms = 60000 / bpm

    # Inject Web Audio API JavaScript
    if start:
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
        components.html(js, height=0)

    if stop:
        js = """
        <script>
        if(window.metInterval){ clearInterval(window.metInterval); window.metInterval = null; }
        </script>
        """
        components.html(js, height=0)

    st.markdown("*Implementation uses browser Web Audio API—no Python threads or server-side audio.*")

if __name__ == '__main__':
    main()
