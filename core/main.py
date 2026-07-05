"""
FLINS-OS — Core Orchestrator
Text-mode entry point (voice loop plugs in on top of this later).
Flow: query -> load relevant skills -> (call LLM with skill context) -> write to vault -> respond
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from skill_loader import discover_skills, load_relevant_skills
from vault_writer import write_note
from router import route

# Loaded once at startup — cheap, just metadata + triggers, no file content yet
ALL_SKILLS = discover_skills()


def build_context(query: str) -> str:
    """Assemble the system context Claude/local-model sees for this turn."""
    relevant = load_relevant_skills(query, ALL_SKILLS)
    if not relevant:
        return "No specific skill matched. Answer generically as FLINS."

    context_blocks = [f"### Skill: {s.branch}/{s.name}\n{s.content}" for s in relevant]
    return "\n\n".join(context_blocks)


def handle_query(query: str) -> str:
    context = build_context(query)
    response = route(query, context)
    write_note(
        title=query[:50],
        content=f"**Query:** {query}\n\n**Response:** {response}",
        folder="logs",
    )
    return response


def repl():
    print("FLINS-OS online. Type 'exit' to quit, 'skills' to list installed skills.\n")
    while True:
        query = input("you> ").strip()
        if query.lower() in ("exit", "quit"):
            break
        if query.lower() == "skills":
            for s in ALL_SKILLS:
                print(f"  [{s.branch}] {s.name} — {', '.join(s.triggers)}")
            continue
        if not query:
            continue
        print(f"flins> {handle_query(query)}\n")


if __name__ == "__main__":
    repl()
