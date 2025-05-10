# lib/audio_backend.py
from abc import ABC, abstractmethod
import threading

class AudioBackend(ABC):
    @abstractmethod
    def play_metronome(self, bpm: int): pass
    @abstractmethod
    def stop_metronome(self): pass
    @abstractmethod
    def play_exercise(self, pattern: list[str], bpm: int): pass
    @abstractmethod
    def stop_exercise(self): pass

from lib.metronome import Metronome
from lib.exercise import Exercise

class LocalAudioBackend(AudioBackend):
    def __init__(self, bpm: int):
        self.metronome = Metronome(bpm)
        self.exercise = Exercise()
    def play_metronome(self, bpm: int):
        self.metronome.bpm = bpm
        if not self.metronome.running:
            self.metronome.running = True
            threading.Thread(target=self.metronome.metronome_loop, daemon=True).start()
    def stop_metronome(self):
        self.metronome.running = False
    def play_exercise(self, pattern: list[str], bpm: int):
        self.exercise.notation = ''.join(pattern)
        if not self.exercise.running:
            self.exercise.running = True
            threading.Thread(target=lambda: self.exercise.exercise_loop(bpm), daemon=True).start()
    def stop_exercise(self):
        self.exercise.running = False

from lib.sound_generator import SoundGenerator

class BrowserAudioBackend(AudioBackend):
    def __init__(self):
        self.sound_gen = SoundGenerator()
        self.placeholder = None
    def set_placeholder(self, ph):
        self.placeholder = ph
    def play_metronome(self, bpm: int):
        pattern = ['R'] + ['L'] * 3
        self._play_loop(pattern, bpm)
    def stop_metronome(self):
        if self.placeholder:
            self.placeholder.empty()
    def play_exercise(self, pattern: list[str], bpm: int):
        self._play_loop(pattern, bpm)
    def stop_exercise(self):
        if self.placeholder:
            self.placeholder.empty()
    def _play_loop(self, pattern: list[str], bpm: int):
        # Generate 300s of audio
        wav_bytes, sr = self.sound_gen.generate_pattern(pattern, bpm, duration=300)
        if self.placeholder:
            self.placeholder.audio(wav_bytes, format='audio/wav', sample_rate=sr)