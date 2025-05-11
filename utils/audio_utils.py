import os
import io
from pydub import AudioSegment
# from utils.generate_click_sounds import generate_click_sounds

# Load or generate click sounds once
def load_click_sounds():
    # Resolve sound directory relative to this file
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'assets', 'sounds'))
    high_path = os.path.join(base_dir, 'click_high.wav')
    low_path = os.path.join(base_dir, 'click_low.wav')
    # Generate if missing
    # if not os.path.exists(high_path) or not os.path.exists(low_path):
    #     generate_click_sounds()
    high = AudioSegment.from_wav(high_path)
    low = AudioSegment.from_wav(low_path)
    return high, low

# Generate a pattern audio at given BPM
def generate_pattern_audio(pattern: str, bpm: int, loops: int = 16) -> bytes:
    high, low = load_click_sounds()
    beat_duration_ms = int(60000 / bpm)
    full = AudioSegment.silent(duration=0)
    for symbol in pattern:
        click = high if symbol.upper() == 'R' else low
        # Trim or pad to exact beat length
        duration = len(click)
        if duration > beat_duration_ms:
            click = click[:beat_duration_ms]
        elif duration < beat_duration_ms:
            click = click + AudioSegment.silent(duration=beat_duration_ms - duration)
        full += click
    # Repeat loops
    track = full * loops
    buf = io.BytesIO()
    track.export(buf, format="wav")
    return buf.getvalue()