"""
FLINS-OS Speech-to-Text
Records a fixed window from the mic, transcribes locally with faster-whisper.
No cloud calls. First run downloads the model (~150MB for 'base').
"""

import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

MODEL_SIZE = "base"      # tiny / base / small / medium — base is a good speed/accuracy balance
SAMPLE_RATE = 16000       # whisper wants 16kHz mono
RECORD_SECONDS = 5

# Loaded once, reused across calls. "int8" runs fast even on CPU;
# swap to "float16" + device="cuda" once we confirm GPU works.
_model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")


def record_audio(seconds: int = RECORD_SECONDS) -> np.ndarray:
    device_info = sd.query_devices(kind="input")
    channels = device_info["max_input_channels"]
    # Array mics (like Intel Smart Sound) can be finicky on a single channel —
    # record all channels the device offers, then downmix to mono for whisper.
    print(f"[listening for {seconds}s on '{device_info['name']}' ({channels}ch)...]")
    audio = sd.rec(int(seconds * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=channels, dtype="float32")
    sd.wait()

    if channels > 1:
        audio = audio.mean(axis=1)
    else:
        audio = audio.flatten()

    peak = np.abs(audio).max()
    print(f"[peak input level: {peak:.4f}]" + ("  <-- looks silent, check mic!" if peak < 0.01 else ""))

    return audio


def transcribe(audio: np.ndarray) -> str:
    segments, _ = _model.transcribe(audio, language="en")
    text = " ".join(seg.text.strip() for seg in segments)
    return text.strip()


def listen_once(seconds: int = RECORD_SECONDS) -> str:
    """Record + transcribe in one call. Used by the main voice loop."""
    audio = record_audio(seconds)
    return transcribe(audio)


if __name__ == "__main__":
    print("Say something — recording starts now.")
    text = listen_once()
    print(f"\nTranscribed: \"{text}\"")
