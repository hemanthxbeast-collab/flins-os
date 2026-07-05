"""
FLINS-OS Skill Loader
Scans skills/<branch>/<skill>/SKILL.md and loads only what a given
query needs. Keyword-match now; swap in embeddings later without
changing the interface (load_relevant_skills stays the same).
"""

import os
import re
from dataclasses import dataclass

SKILLS_ROOT = os.path.join(os.path.dirname(__file__), "..", "skills")


@dataclass
class Skill:
    branch: str          # e.g. "productivity"
    name: str            # e.g. "email"
    path: str            # full path to SKILL.md
    triggers: list        # keywords pulled from the SKILL.md frontmatter
    content: str = ""    # lazy-loaded full text


def _parse_triggers(text: str) -> list:
    """Pull a `triggers: a, b, c` line out of the SKILL.md frontmatter."""
    match = re.search(r"^triggers:\s*(.+)$", text, re.MULTILINE | re.IGNORECASE)
    if not match:
        return []
    return [t.strip().lower() for t in match.group(1).split(",") if t.strip()]


def discover_skills() -> list:
    """Walk skills/ and return every Skill found (metadata only, no content read)."""
    found = []
    if not os.path.isdir(SKILLS_ROOT):
        return found

    for branch in sorted(os.listdir(SKILLS_ROOT)):
        branch_path = os.path.join(SKILLS_ROOT, branch)
        if not os.path.isdir(branch_path):
            continue
        for skill_name in sorted(os.listdir(branch_path)):
            skill_path = os.path.join(branch_path, skill_name)
            md_path = os.path.join(skill_path, "SKILL.md")
            if os.path.isfile(md_path):
                with open(md_path, "r", encoding="utf-8") as f:
                    head = f.read(1000)  # frontmatter is always near the top
                found.append(Skill(
                    branch=branch,
                    name=skill_name,
                    path=md_path,
                    triggers=_parse_triggers(head),
                ))
    return found


def load_relevant_skills(query: str, all_skills: list = None, max_skills: int = 3) -> list:
    """
    Return the Skill objects relevant to a query, with content loaded.
    Falls back to zero skills if nothing matches — FLINS should still
    be able to answer generically without a skill.
    """
    if all_skills is None:
        all_skills = discover_skills()

    query_lower = query.lower()
    scored = []
    for skill in all_skills:
        score = sum(1 for trig in skill.triggers if trig in query_lower)
        if score > 0:
            scored.append((score, skill))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = [s for _, s in scored[:max_skills]]

    for skill in top:
        with open(skill.path, "r", encoding="utf-8") as f:
            skill.content = f.read()

    return top


def list_all_skills_summary() -> str:
    """Used by the HUD to show what's installed, regardless of query relevance."""
    skills = discover_skills()
    lines = []
    for s in skills:
        lines.append(f"[{s.branch}] {s.name} — triggers: {', '.join(s.triggers) or 'none set'}")
    return "\n".join(lines) if lines else "No skills installed yet."


if __name__ == "__main__":
    print(list_all_skills_summary())
