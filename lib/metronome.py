# lib/metronome.py
import numpy as np
import sounddevice as sd
import time

class Metronome:
    def __init__(self, bpm: int = 120):
        self.bpm = bpm
        self.running = False
        dur = 0.05
        self.sr = 44100
        t = np.linspace(0, dur, int(self.sr * dur), endpoint=False)
        self.high = np.sin(2 * np.pi * 440 * t).astype(np.float32)
        self.low  = np.sin(2 * np.pi * 880 * t).astype(np.float32)
    def play_beep(self, wave):
        sd.play(wave, self.sr)
        sd.wait()
    def metronome_loop(self):
        interval = 60.0 / self.bpm
        pattern = [self.high] + [self.low] * 3
        next_time = time.time()
        beat = 0
        while self.running:
            wave = pattern[beat % len(pattern)]
            self.play_beep(wave)
            beat += 1
            next_time += interval
            time.sleep(max(0, next_time - time.time()))