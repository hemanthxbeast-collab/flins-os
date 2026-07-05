"""
FLINS-OS Text-to-Speech
Uses kokoro-onnx — fully local, no cloud, runs fine on CPU.
Needs two files on first setup (one-time download, see setup instructions):
  voice/models/kokoro-v1.0.onnx
  voice/models/voices-v1.0.bin
"""

import os
import sounddevice as sd
from kokoro_onnx import Kokoro

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "kokoro-v1.0.onnx")
VOICES_PATH = os.path.join(MODEL_DIR, "voices-v1.0.bin")

VOICE = "am_puck"   # locked in as FLINS's voice
SPEED = 1.0

_kokoro = None


def _load():
    global _kokoro
    if _kokoro is None:
        if not (os.path.exists(MODEL_PATH) and os.path.exists(VOICES_PATH)):
            raise FileNotFoundError(
                f"Kokoro model files missing. Expected:\n  {MODEL_PATH}\n  {VOICES_PATH}\n"
                "Run the download commands from the setup instructions first."
            )
        _kokoro = Kokoro(MODEL_PATH, VOICES_PATH)
    return _kokoro


def speak(text: str, voice: str = VOICE, speed: float = SPEED):
    """Synthesize text and play it through the default speaker."""
    kokoro = _load()
    samples, sample_rate = kokoro.create(text, voice=voice, speed=speed, lang="en-us")
    sd.play(samples, sample_rate)
    sd.wait()


if __name__ == "__main__":
    print("Speaking a test line...")
    speak("Hey, I'm FLINS. Voice output is working.")
    print("Done.")
