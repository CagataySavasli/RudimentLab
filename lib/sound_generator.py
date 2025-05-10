# lib/sound_generator.py
import numpy as np
import io
from scipy.io.wavfile import write

class SoundGenerator:
    def __init__(self, sr: int = 44100, beep_dur: float = 0.05):
        self.sr = sr
        t = np.linspace(0, beep_dur, int(sr * beep_dur), endpoint=False)
        self.high = (0.5 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)
        self.low  = (0.5 * np.sin(2 * np.pi * 880 * t)).astype(np.float32)

    def generate_wav_bytes(self, clip: np.ndarray) -> bytes:
        buf = io.BytesIO()
        write(buf, self.sr, clip)
        return buf.getvalue()