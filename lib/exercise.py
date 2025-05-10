# lib/exercise.py
import time
from lib.metronome import Metronome

class Exercise:
    def __init__(self, notation: str = "RLRL RLRL RRLL RRLL"):
        self.notation = notation
        self.running = False
        self.metronome = Metronome()

    def exercise_loop(self, bpm: int):
        self.metronome.bpm = bpm
        pattern = [c.upper() for c in self.notation if c.upper() in ("R", "L")]
        interval = 60.0 / bpm
        self.metronome.running = True
        while self.running:
            for symbol in pattern:
                if not self.running:
                    break
                waveform = self.metronome.high if symbol == "R" else self.metronome.low
                self.metronome.play_beep(waveform)
                time.sleep(max(0, interval - (len(waveform) / self.metronome.sample_rate)))
        self.metronome.running = False
