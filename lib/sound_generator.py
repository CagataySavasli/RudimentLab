# lib/sound_generator.py
import numpy as np
import io
from scipy.io.wavfile import write

class SoundGenerator:
    def __init__(self, sr: int = 44100, beep_duration: float = 0.05):
        self.sr = sr
        t = np.linspace(0, beep_duration, int(sr * beep_duration), endpoint=False)
        self.high = (0.5 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)
        self.low  = (0.5 * np.sin(2 * np.pi * 880 * t)).astype(np.float32)

    def generate_pattern(self, pattern: list[str], bpm: int, duration: float) -> tuple[bytes,int]:
        """
        Generate a WAV buffer containing the given pattern repeated for 'duration' seconds.
        Returns (wav_bytes, sample_rate).
        """
        interval = 60.0 / bpm
        spb = int(self.sr * interval)
        total_samples = int(self.sr * duration)
        buf = np.zeros(total_samples, dtype=np.float32)
        # fill pattern cyclically
        idx = 0
        pos = 0
        while pos + max(len(self.high), len(self.low)) < total_samples:
            sym = pattern[idx % len(pattern)]
            clip = self.high if sym == 'R' else self.low
            end = pos + len(clip)
            buf[pos:end] = clip
            pos += spb
            idx += 1
        # write to WAV
        mem = io.BytesIO()
        write(mem, self.sr, buf)
        return mem.getvalue(), self.sr