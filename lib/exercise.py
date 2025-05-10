# lib/exercise.py
import numpy as np
import sounddevice as sd
import time

class Exercise:
    def __init__(self, notation: str = "RLRL RLRL RRLL RRLL"):
        self.notation = notation
        self.running = False
        dur = 0.05
        self.sr = 44100
        t = np.linspace(0, dur, int(self.sr * dur), endpoint=False)
        self.high = np.sin(2 * np.pi * 440 * t).astype(np.float32)
        self.low  = np.sin(2 * np.pi * 880 * t).astype(np.float32)
    def exercise_loop(self, bpm: int):
        pattern = [c for c in self.notation.upper() if c in ('R','L')]
        interval = 60.0 / bpm
        next_time = time.time()
        idx = 0
        while self.running:
            wave = self.high if pattern[idx % len(pattern)] == 'R' else self.low
            sd.play(wave, self.sr)
            sd.wait()
            idx += 1
            next_time += interval
            time.sleep(max(0, next_time - time.time()))