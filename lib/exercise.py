# lib/exercise.py
import numpy as np
import sounddevice as sd
import time

class Exercise:
    def __init__(self, notation: str = "RLRL RLRL RRLL RRLL"):
        self.notation = notation
        self.running = False
        # Generate click waveforms
        dur = 0.05
        self.sample_rate = 44100
        t = np.linspace(0, dur, int(self.sample_rate * dur), endpoint=False)
        self.high = np.sin(2 * np.pi * 440 * t).astype(np.float32)
        self.low = np.sin(2 * np.pi * 880 * t).astype(np.float32)

    def exercise_loop(self, bpm: int):
        interval = 60.0 / bpm
        start_time = time.time()
        beat = 0
        pattern = [c for c in self.notation.replace(' ','').upper() if c in ('R','L')]
        while self.running and pattern:
            scheduled = start_time + beat * interval
            now = time.time()
            if scheduled > now:
                time.sleep(scheduled - now)
            symbol = pattern[beat % len(pattern)]
            wave = self.high if symbol=='R' else self.low
            sd.play(wave, self.sample_rate)
            sd.wait()
            beat += 1
