# lib/sound_generator.py
import numpy as np
import io
from scipy.io.wavfile import write

class SoundGenerator:
    def __init__(self, sr: int = 44100, dur: float = 0.05):
        self.sr = sr
        t = np.linspace(0, dur, int(sr * dur), endpoint=False)
        self.high = (0.5 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)
        self.low  = (0.5 * np.sin(2 * np.pi * 880 * t)).astype(np.float32)
    def generate_pattern(self, pattern: list[str], bpm: int, duration: float) -> tuple[bytes,int]:
        interval = 60.0 / bpm
        spb = int(self.sr * interval)
        total_samples = int(self.sr * duration)
        buf = np.zeros(total_samples, dtype=np.float32)
        pos = 0
        idx = 0
        while pos + max(len(self.high), len(self.low)) < total_samples:
            clip = self.high if pattern[idx % len(pattern)] == 'R' else self.low
            buf[pos:pos+len(clip)] = clip
            pos += spb
            idx += 1
        mem = io.BytesIO()
        write(mem, self.sr, buf)
        return mem.getvalue(), self.sr