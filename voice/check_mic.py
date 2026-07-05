"""
Run this FIRST, before anything else in voice/.
Just confirms sounddevice can see your mic and speakers.
No models loaded yet — this is a 10-second sanity check.
"""

import sounddevice as sd

print("=== Audio devices detected ===\n")
print(sd.query_devices())

print("\n=== Default input (mic) ===")
print(sd.query_devices(kind="input"))

print("\n=== Default output (speaker) ===")
print(sd.query_devices(kind="output"))

print("\nIf you see real device names above (not errors), your mic/speaker are ready.")
