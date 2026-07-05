# FLINS-OS

Your own voice-driven AI command center. Skills + memory + voice, 100% local, forkable per client.

## Status: Step 1 done (Skill Architecture + Memory Vault)

## Quick start

**Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
source venv/bin/activate
python core/main.py
```

**Windows PowerShell:**
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\setup.ps1
.\venv\Scripts\Activate.ps1
python core\main.py
```
(Run `.\setup.ps1` directly — don't spawn it via `powershell -File`, that launches a
nested process that can lose track of your working directory.)

Type a query. FLINS matches it to the right skill(s) in `skills/`, and logs the
interaction as a markdown note in `vault/logs/`. Open the `vault/` folder in
Obsidian to see it as a graph.

## Structure
```
flins-os/
├── core/
│   ├── skill_loader.py   # scans skills/, matches by trigger keywords
│   ├── vault_writer.py   # writes memory as Obsidian markdown
│   └── main.py           # orchestrator / REPL
├── skills/
│   └── <branch>/<skill>/SKILL.md   # add new skills here
├── vault/                # your Obsidian vault (memory)
├── voice/                # Step 3 — empty for now
├── hud/                  # Step 4 — empty for now
├── .env.example
├── requirements.txt
└── setup.sh
```

## Adding a new skill
Create `skills/<branch>/<name>/SKILL.md`:
```markdown
---
name: myskill
branch: mybranch
triggers: keyword1, keyword2
---
# instructions for the skill go here
```
No code changes needed — the loader picks it up automatically.

## Roadmap
- [x] Step 1: Skill architecture
- [x] Step 2: Obsidian vault memory
- [ ] Step 3: 100% local voice (faster-whisper + Kokoro)
- [ ] Step 4: V.A.U.L.T. HUD dashboard
- [ ] Step 5: bundle/ship — fork per client
