from utils.audio_utils import generate_pattern_audio

class Metronome:
    def __init__(self, bpm: int):
        self.bpm = bpm
        # Default pattern: RLLL
        self.pattern = 'RLLL'

    def set_bpm(self, bpm: int):
        self.bpm = bpm

    def set_pattern(self, pattern: str):
        self.pattern = pattern

    def get_audio(self) -> bytes:
        return generate_pattern_audio(self.pattern, self.bpm)