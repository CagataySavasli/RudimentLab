import numpy as np
import sounddevice as sd

class SoundMaker:
    def __init__(self):
        # Kısa bir beep için 0.1 sn, A4 frekansı
        duration = 0.1
        frequency = 440
        self.sample_rate = 44100
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)

        self.high_touch = np.sin(2 * np.pi * frequency * t)
        self.low_touch = np.sin(4 * np.pi * frequency * t)

    def play_beep(self, touch_type: bool):
        waveform = self.high_touch if touch_type else self.low_touch
        sd.play(waveform, self.sample_rate)
        sd.wait()

    def get_touch_time(self, touch_type: bool):
        waveform = self.high_touch if touch_type else self.low_touch
        return len(waveform)/self.sample_rate

    __call__ = play_beep