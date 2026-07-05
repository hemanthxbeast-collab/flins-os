"""
FLINS-OS Vault Writer
Writes every interaction/report back into the Obsidian vault as plain
markdown, with backlinks so Claude (or you) can traverse it later.
No database — the folder IS the memory.
"""

import os
import re
from datetime import datetime

VAULT_ROOT = os.path.join(os.path.dirname(__file__), "..", "vault")


def _slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[\s]+", "-", text)[:60]


def write_note(title: str, content: str, folder: str = "logs", links: list = None) -> str:
    """
    Write a markdown note into the vault.
    folder: subfolder inside vault/ (e.g. "research", "logs", "projects")
    links: list of other note titles to backlink with [[wiki links]]
    Returns the path written.
    """
    target_dir = os.path.join(VAULT_ROOT, folder)
    os.makedirs(target_dir, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H:%M")
    slug = _slugify(title)
    filename = f"{date_str}-{slug}.md"
    path = os.path.join(target_dir, filename)

    link_block = ""
    if links:
        link_block = "\n\n## Related\n" + "\n".join(f"- [[{l}]]" for l in links)

    body = f"""---
title: {title}
date: {date_str} {time_str}
tags: [flins, {folder}]
---

# {title}

{content}
{link_block}
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)

    return path


def read_recent_notes(folder: str = "logs", limit: int = 5) -> list:
    """Grab the most recent notes for context — used before answering follow-up queries."""
    target_dir = os.path.join(VAULT_ROOT, folder)
    if not os.path.isdir(target_dir):
        return []
    files = sorted(
        (f for f in os.listdir(target_dir) if f.endswith(".md")),
        reverse=True,
    )[:limit]
    notes = []
    for f in files:
        with open(os.path.join(target_dir, f), "r", encoding="utf-8") as fh:
            notes.append(fh.read())
    return notes


if __name__ == "__main__":
    p = write_note("Test Note", "This is FLINS writing its first memory.", folder="logs")
    print(f"Wrote: {p}")
