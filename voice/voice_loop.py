"""
FLINS-OS Voice Loop
Mic -> faster-whisper (STT) -> skill match -> Gemini/Anthropic -> vault log -> Kokoro (TTS)
Say "stop listening" or "goodbye flins" to exit.
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))

from stt import listen_once
from tts import speak
from skill_loader import discover_skills, load_relevant_skills
from vault_writer import write_note
from router import route
import actions

EXIT_PHRASES = ("stop listening", "goodbye flins", "exit flins", "shut down flins")

ALL_SKILLS = discover_skills()


def build_context(query: str) -> str:
    relevant = load_relevant_skills(query, ALL_SKILLS)
    if not relevant:
        return "No specific skill matched. Answer generically as FLINS."
    return "\n\n".join(f"### Skill: {s.branch}/{s.name}\n{s.content}" for s in relevant)


def handle_query(query: str) -> str:
    action_result = actions.try_action(query)
    if action_result:
        write_note(
            title=query[:50],
            content=f"**Query:** {query}\n\n**Action result:** {action_result}",
            folder="logs",
        )
        return action_result

    context = build_context(query)
    response = route(query, context, voice_mode=True)
    write_note(
        title=query[:50],
        content=f"**Query:** {query}\n\n**Response:** {response}",
        folder="logs",
    )
    return response


def run():
    print("=== FLINS voice loop active ===")
    print(f"Say one of {EXIT_PHRASES} to stop.\n")
    speak("FLINS online. I'm listening.")

    while True:
        heard = listen_once(seconds=5)
        if not heard:
            continue

        print(f"you said: \"{heard}\"")

        if any(phrase in heard.lower() for phrase in EXIT_PHRASES):
            speak("Shutting down. Talk soon.")
            print("=== FLINS voice loop stopped ===")
            break

        response = handle_query(heard)
        print(f"flins: {response}\n")
        speak(response)


if __name__ == "__main__":
    run()
