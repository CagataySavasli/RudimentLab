from pydub.generators import Sine

# Parameters
HIGH_FREQ = 880  # Hz for high click (Right)
LOW_FREQ = 440   # Hz for low click (Left)
BEAT_DURATION_MS = 100  # Duration of each click in milliseconds

# Generate sine wave segments
high_click = Sine(HIGH_FREQ).to_audio_segment(duration=BEAT_DURATION_MS)
low_click  = Sine(LOW_FREQ).to_audio_segment(duration=BEAT_DURATION_MS)

# Export to WAV files
high_click.export("assets/sounds/click_high.wav", format="wav")
low_click.export("assets/sounds/click_low.wav", format="wav")

print("Generated click_high.wav and click_low.wav in assets/sounds/")