# lib/exercise.py
import time
import sounddevice as sd
import numpy as np
from typing import List

class Exercise:
    def __init__(self, notation: str = "RLRL RLRL RRLL RRLL"):
        self.notation = notation
        self.running = False
        # prepare beep waveforms
        dur = 0.05
        self.sr = 44100
        t = np.linspace(0, dur, int(self.sr * dur), endpoint=False)
        self.high = np.sin(2 * np.pi * 440 * t).astype(np.float32)
        self.low  = np.sin(2 * np.pi * 880 * t).astype(np.float32)

    def exercise_loop(self, bpm: int):
        interval = 60.0 / bpm
        pattern: List[str] = [c for c in self.notation.replace(' ', '').upper() if c in ('R','L')]
        next_time = time.time()
        idx = 0
        while self.running:
            wave = self.high if pattern[idx % len(pattern)] == 'R' else self.low
            sd.play(wave, self.sr)
            sd.wait()
            idx += 1
            next_time += interval
            time.sleep(max(0, next_time - time.time()))