---
name: control
branch: system
triggers: what can you do, capabilities, control my laptop, control my pc, help with my computer
---

# System Control Skill

This documents what FLINS can ACTUALLY do on the laptop (handled by core/actions.py,
matched before any LLM call — these are real, not hallucinated capabilities).

## Real capabilities
- Open apps: chrome, notepad, calculator, file explorer, vs code, word, excel,
  powerpoint, spotify, obsidian, edge, task manager, settings
- Open folders: desktop, downloads, documents, pictures, vault
- Check battery percentage and charging status
- Check CPU/RAM usage
- Take a screenshot (saved to vault/screenshots/)
- Find a file by name in Desktop/Downloads/Documents (shallow search)

## NOT capable of (be honest about this if asked)
- Cannot delete, move, or modify files
- Cannot shut down, restart, or sleep the machine
- Cannot run arbitrary commands or scripts
- Cannot browse the web or click things on screen
- Cannot install or uninstall software

## Notes
If asked "what can you do", answer with the real list above — don't invent
capabilities. If asked to do something outside this list, say so plainly
and suggest it could be added as a new whitelisted action later.
