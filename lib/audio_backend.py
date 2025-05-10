# lib/audio_backend.py
from abc import ABC, abstractmethod
import threading
import base64
import json

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

class BrowserAudioBackend:
    def __init__(self):
        self.sg = SoundGenerator()
        # Pre-generate URIs for R and L
        r_bytes = self.sg.generate_wav_bytes(self.sg.high)
        l_bytes = self.sg.generate_wav_bytes(self.sg.low)
        self.r_uri = f"data:audio/wav;base64,{base64.b64encode(r_bytes).decode()}"
        self.l_uri = f"data:audio/wav;base64,{base64.b64encode(l_bytes).decode()}"
        self.ph = None

    def set_placeholder(self, ph):
        self.ph = ph

    def play_pattern(self, pattern, bpm: int):
        if not self.ph: return
        pattern_js = json.dumps(pattern)
        interval = 60000 / bpm
        js = f"""
        <script>
        if(window.metInterval) clearInterval(window.metInterval);
        const pattern = {pattern_js};
        const interval = {interval};
        const rAudio = new Audio('{self.r_uri}');
        const lAudio = new Audio('{self.l_uri}');
        let idx = 0;
        function playBeat() {{
            const a = pattern[idx] === 'R' ? rAudio.cloneNode() : lAudio.cloneNode();
            a.play();
            idx = (idx + 1) % pattern.length;
        }}
        playBeat();
        window.metInterval = setInterval(playBeat, interval);
        </script>
        """
        self.ph.markdown(js, unsafe_allow_html=True)

    def stop(self):
        if self.ph:
            js = "<script>if(window.metInterval){clearInterval(window.metInterval);window.metInterval=null;}</script>"
            self.ph.markdown(js, unsafe_allow_html=True)