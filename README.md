# FLINS-OS

Your own voice-driven AI command center. Skills + memory + voice, 100% local where it counts, forkable per client.

Built by [hemanthxbeast](https://github.com/hemanthxbeast-collab).

## Status

- [x] **Skill architecture** — drop a `SKILL.md` in `skills/<branch>/<name>/`, FLINS auto-discovers and matches by keyword
- [x] **Obsidian vault memory** — every interaction logs as plain markdown, no database
- [x] **Voice loop** — mic in (faster-whisper, local) -> skill routing -> Gemini/Anthropic -> speech out (Kokoro, local)
- [x] **Model-agnostic router** — regex shortcuts first (free), then Gemini (default, free tier) or Anthropic (optional, paid)
- [ ] HUD dashboard (built, functional, currently unused — CLI is the main interface)
- [ ] OS-level command execution (open apps, control the machine directly — next up)

## Quick start

**1. Clone and set up:**
```powershell
git clone https://github.com/hemanthxbeast-collab/flins-os.git
cd flins-os
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\setup.ps1
.\venv\Scripts\Activate.ps1
```
(Mac/Linux: `chmod +x setup.sh && ./setup.sh && source venv/bin/activate`)

**2. Add your API key** — edit `.env`:
```
GEMINI_API_KEY=your_key_here
```
Free key: https://aistudio.google.com/apikey (no card needed)

**3. Text mode (fastest way to test):**
```powershell
python core\main.py
```

**4. Voice mode — needs two extra downloads first (one-time, ~350MB):**
```powershell
mkdir voice\models
Invoke-WebRequest -Uri "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx" -OutFile "voice\models\kokoro-v1.0.onnx"
Invoke-WebRequest -Uri "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin" -OutFile "voice\models\voices-v1.0.bin"
python voice\voice_loop.py
```
Say "stop listening" to exit the voice loop.

## Structure
```
flins-os/
├── core/
│   ├── skill_loader.py   # scans skills/, matches by trigger keywords
│   ├── vault_writer.py   # writes memory as Obsidian markdown
│   ├── router.py         # regex -> Gemini/Anthropic tiered decision
│   └── main.py           # text-mode orchestrator / REPL
├── voice/
│   ├── stt.py            # faster-whisper mic transcription
│   ├── tts.py             # Kokoro local speech synthesis
│   ├── voice_loop.py      # full mic -> brain -> speaker loop
│   ├── check_mic.py       # audio device diagnostic
│   └── voice_sampler.py   # sample all Kokoro voices to pick one
├── hud/                   # optional web dashboard (not required)
├── skills/
│   └── <branch>/<name>/SKILL.md   # add new skills here, no code changes needed
├── vault/                 # Obsidian-compatible memory (gitignored: personal notes)
├── .env.example
├── requirements.txt
├── setup.sh / setup.ps1
└── .gitignore
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

## Switching model providers
Set `FLINS_PROVIDER=anthropic` in `.env` and fill `ANTHROPIC_API_KEY` — no code changes, the router handles it.

## Fork per client
This whole repo is meant to be forked and reskinned — clone it, swap the `skills/` folder for a different domain, rename the voice/persona, and it's a different product.
