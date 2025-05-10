# lib/metronome.py
import numpy as np
import sounddevice as sd
import time
from typing import List

class Metronome:
    def __init__(self, bpm: int = 120):
        self.bpm = bpm
        self.running = False
        # prepare beep waveforms
        dur = 0.05
        self.sr = 44100
        t = np.linspace(0, dur, int(self.sr * dur), endpoint=False)
        self.high = np.sin(2 * np.pi * 440 * t).astype(np.float32)
        self.low  = np.sin(2 * np.pi * 880 * t).astype(np.float32)

    def play_beep(self, wave: np.ndarray):
        sd.play(wave, self.sr)
        sd.wait()

    def metronome_loop(self):
        interval = 60.0 / self.bpm
        pattern: List[np.ndarray] = [self.high] + [self.low] * 3
        next_time = time.time()
        while self.running:
            self.play_beep(pattern[int((time.time() - next_time)/interval) % 4])
            next_time += interval
            time.sleep(max(0, next_time - time.time()))