# lib/sound_maker.py
import numpy as np
import io
from scipy.io.wavfile import write

class SoundMaker:
    def __init__(self, sample_rate: int = 44100, beep_duration: float = 0.1):
        self.sr = sample_rate
        t = np.linspace(0, beep_duration, int(self.sr * beep_duration), endpoint=False)
        # High click (A4) and low click (A5)
        self.high = (0.5 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)
        self.low  = (0.5 * np.sin(2 * np.pi * 880 * t)).astype(np.float32)
        self.beep_samples = len(t)

    def make_pattern_wav(self, pattern, bpm: int) -> bytes:
        """
        Build a single WAV for one cycle of the given pattern at the specified BPM.
        The returned bytes can be looped via HTML audio.
        """
        interval = 60.0 / bpm
        samples_per_beat = int(self.sr * interval)
        total_samples = samples_per_beat * len(pattern)
        wav = np.zeros(total_samples, dtype=np.float32)
        for i, symbol in enumerate(pattern):
            start = i * samples_per_beat
            clip = self.high if symbol.upper() == 'R' else self.low
            wav[start:start + self.beep_samples] = clip
        # Write to in-memory WAV
        buf = io.BytesIO()
        write(buf, self.sr, wav)
        return buf.getvalue()
