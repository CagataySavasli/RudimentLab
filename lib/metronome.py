# lib/metronome.py
import numpy as np
import sounddevice as sd
import time

class Metronome:
    def __init__(self, bpm: int = 120):
        self.bpm = bpm
        self.running = False
        # Generate click waveforms
        dur = 0.05  # beep duration in seconds
        self.sample_rate = 44100
        t = np.linspace(0, dur, int(self.sample_rate * dur), endpoint=False)
        self.high = np.sin(2 * np.pi * 440 * t).astype(np.float32)
        self.low = np.sin(2 * np.pi * 880 * t).astype(np.float32)

    def play_beep(self, waveform):
        sd.play(waveform, self.sample_rate)
        sd.wait()

    def metronome_loop(self):
        interval = 60.0 / self.bpm
        start_time = time.time()
        beat = 0
        # pattern accent on first (R) then three lows
        pat = ['R','L','L','L']
        while self.running:
            scheduled = start_time + beat * interval
            now = time.time()
            if scheduled > now:
                time.sleep(scheduled - now)
            symbol = pat[beat % len(pat)]
            wave = self.high if symbol=='R' else self.low
            self.play_beep(wave)
            beat += 1

