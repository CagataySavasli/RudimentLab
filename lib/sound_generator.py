# lib/sound_generator.py
import numpy as np
import io
from scipy.io.wavfile import write

class SoundGenerator:
    def __init__(self, sr=44100, dur=0.05):
        self.sr = sr
        t = np.linspace(0, dur, int(sr * dur), endpoint=False)
        self.high = (0.5 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)
        self.low  = (0.5 * np.sin(2 * np.pi * 880 * t)).astype(np.float32)

    def make_pattern_wav(self, pattern, bpm: int) -> bytes:
        interval = 60.0 / bpm
        spb = int(self.sr * interval)
        total = spb * len(pattern)
        buf = np.zeros(total, dtype=np.float32)
        for i, sym in enumerate(pattern):
            start = i * spb
            clip = self.high if sym=='R' else self.low
            buf[start:start+len(clip)] = clip
        mem = io.BytesIO()
        write(mem, self.sr, buf)
        return mem.getvalue()