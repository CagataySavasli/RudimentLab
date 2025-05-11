from utils.audio_utils import generate_pattern_audio

class Exercise:
    def __init__(self, bpm: int, notation: str):
        self.bpm = bpm
        # Clean spaces
        self.notation = notation.replace(' ', '')

    def set_bpm(self, bpm: int):
        self.bpm = bpm

    def set_notation(self, notation: str):
        self.notation = notation.replace(' ', '')

    def get_audio(self) -> bytes:
        return generate_pattern_audio(self.notation, self.bpm)