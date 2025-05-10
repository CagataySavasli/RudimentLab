# lib/metronome.py
import numpy as np
import sounddevice as sd
from time import sleep

class Metronome:
    def __init__(self, bpm: int = 120):
        self.bpm = bpm
        self.running = False
        # Pre-generate click waveforms
        duration = 0.1
        self.sample_rate = 44100
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        self.high = np.sin(2 * np.pi * 440 * t).astype(np.float32)
        self.low = np.sin(2 * np.pi * 880 * t).astype(np.float32)

    def play_beep(self, waveform):
        sd.play(waveform, self.sample_rate)
        sd.wait()

    def metronome_loop(self):
        interval = 60.0 / self.bpm
        while self.running:
            for i in range(4):
                if not self.running:
                    return
                waveform = self.high if i == 0 else self.low
                self.play_beep(waveform)
                sleep(max(0, interval - (len(waveform) / self.sample_rate)))
