# lib/metronome.py
from lib.sound_maker import SoundMaker
from time import sleep

class Metronome:
    def __init__(self, bpm: int = 120):
        self.bpm = bpm
        self.running = False

        self.sound_maker = SoundMaker()





    def metronome_loop(self):
        interval = 60.0 / self.bpm
        while self.running:
            for i in range(4):
                if not self.running:
                    return
                touch_type = True if i == 0 else False
                self.sound_maker(touch_type)
                touch_time = self.sound_maker.get_touch_time(touch_type)
                sleep(max(0, interval - touch_time))
