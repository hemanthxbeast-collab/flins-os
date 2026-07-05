"""
Run once to hear all male Kokoro voices back to back, then tell FLINS
which one to lock in as default (edit VOICE in tts.py).
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from tts import _load

MALE_VOICES = ["am_adam", "am_michael", "am_echo", "am_eric", "am_liam", "am_onyx", "am_puck", "bm_george", "bm_lewis"]

SAMPLE_TEXT = "Hey, I'm FLINS. This is what I sound like."


def main():
    kokoro = _load()
    import sounddevice as sd

    for voice in MALE_VOICES:
        try:
            print(f"\nPlaying: {voice}")
            samples, sample_rate = kokoro.create(SAMPLE_TEXT, voice=voice, speed=1.0, lang="en-us")
            sd.play(samples, sample_rate)
            sd.wait()
        except Exception as e:
            print(f"  skipped {voice} (not available in this model): {e}")

    print("\nDone. Tell me which one sounded best (by name) and I'll set it as default.")


if __name__ == "__main__":
    main()
