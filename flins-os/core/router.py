"""
FLINS-OS Router
Tiered decision: regex (free, instant) -> local model (if configured) -> cloud model.
Keeps most queries off the API entirely; only escalates when it needs real reasoning.

Supports two cloud backends — pick via FLINS_PROVIDER in .env:
  - "gemini"    (default, has a real free tier, no card needed to start)
  - "anthropic" (pay-as-you-go, needs billing set up)
"""

import os
import re
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("FLINS_PROVIDER", "gemini").lower()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.getenv("FLINS_MODEL", "claude-haiku-4-5-20251001")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("FLINS_GEMINI_MODEL", "gemini-2.5-flash")

# --- Tier 1: regex shortcuts, zero API cost ---
REGEX_RULES = [
    (re.compile(r"^\s*(hi|hello|hey)\s*(flins)?\s*$", re.I), "Hey, I'm here. What do you need?"),
    (re.compile(r"^\s*(what'?s? the )?time\s*$", re.I), None),  # handled specially below
]


def try_regex(query: str):
    import datetime
    for pattern, response in REGEX_RULES:
        if pattern.match(query):
            if response is None and "time" in query.lower():
                return f"It's {datetime.datetime.now().strftime('%H:%M')}."
            return response
    return None


SYSTEM_PROMPT_TEMPLATE = """You are FLINS, a voice-driven AI command center running locally for Hemanth.
Be direct and brief — no filler, no over-explaining. Match his tone: casual, to the point.

Relevant skill context for this query:
{context}
"""


# --- Tier 3a: Gemini (default) ---
def call_gemini(query: str, context: str) -> str:
    if not GEMINI_API_KEY:
        return (
            "[No GEMINI_API_KEY set in .env — get a free one at "
            "aistudio.google.com/apikey and paste it in.]"
        )

    from google import genai
    client = genai.Client(api_key=GEMINI_API_KEY)

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=context)

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=query,
        config={"system_instruction": system_prompt, "max_output_tokens": 500},
    )
    return response.text


# --- Tier 3b: Anthropic (optional swap) ---
def call_anthropic(query: str, context: str) -> str:
    if not ANTHROPIC_API_KEY:
        return (
            "[No ANTHROPIC_API_KEY set in .env — add one from console.anthropic.com "
            "to get real responses instead of this message.]"
        )

    from anthropic import Anthropic
    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=context)

    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=500,
        system=system_prompt,
        messages=[{"role": "user", "content": query}],
    )
    return response.content[0].text


def route(query: str, context: str) -> str:
    """Main entry point — tries cheapest tier first, then whichever cloud provider is configured."""
    regex_hit = try_regex(query)
    if regex_hit:
        return regex_hit

    # Tier 2 (local model) hooks in here later — e.g. Ollama call if OLLAMA_HOST is set
    # if os.getenv("OLLAMA_HOST"):
    #     return call_local_model(query, context)

    if PROVIDER == "anthropic":
        return call_anthropic(query, context)
    return call_gemini(query, context)
