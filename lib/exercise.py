import time
from lib.sound_maker import SoundMaker

class Exercise:
    def __init__(self, notation: str = "RLRL RLRL RRLL RRLL"):
        self.notation = notation
        self.running = False
        self.sound_maker = SoundMaker()

    def exercise_loop(self, bpm: int):
        """
        Continuously plays the given notation at the specified BPM until stopped.
        """
        interval = 60.0 / bpm
        # Build pattern from notation string (only R and L)
        pattern = [c.upper() for c in self.notation if c.upper() in ("R", "L")]
        # Loop until user stops
        while self.running:
            for symbol in pattern:
                if not self.running:
                    break
                touch = (symbol == "R")
                # Play the touch
                self.sound_maker(touch)
                # Calculate beep duration to maintain timing
                duration = self.sound_maker.get_touch_time(touch)
                # Wait for remainder of interval
                time.sleep(max(0, interval - duration))
        # Once stopped, exit gracefully
        self.running = False
