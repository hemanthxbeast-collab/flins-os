"""
FLINS-OS System Actions
Whitelisted, deterministic actions FLINS can perform on the machine.
Deliberately NOT arbitrary command execution — every action here is a named,
safe, reviewed function. This is checked BEFORE the query goes to any LLM,
so opening an app or checking battery never costs an API call and never
depends on the model "deciding" to do something risky.
"""

import os
import re
import json
import subprocess
from datetime import datetime

VAULT_ROOT = os.path.join(os.path.dirname(__file__), "..", "vault")
SCREENSHOT_DIR = os.path.join(VAULT_ROOT, "screenshots")
APPS_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "apps.json")

# App name -> the command Windows' "start" resolves via App Paths / PATH.
APP_MAP = {
    "chrome": "chrome",
    "google chrome": "chrome",
    "notepad": "notepad",
    "calculator": "calc",
    "calc": "calc",
    "file explorer": "explorer",
    "explorer": "explorer",
    "vs code": "code",
    "vscode": "code",
    "visual studio code": "code",
    "word": "winword",
    "excel": "excel",
    "powerpoint": "powerpnt",
    "spotify": "spotify",
    "obsidian": "obsidian",
    "edge": "msedge",
    "task manager": "taskmgr",
    "settings": "ms-settings:",
}


def _load_app_overrides():
    """apps.json lets the user add apps (e.g. DaVinci, Genshin) without touching this file."""
    if os.path.exists(APPS_CONFIG_PATH):
        try:
            with open(APPS_CONFIG_PATH, "r", encoding="utf-8") as f:
                user_apps = json.load(f)
            return {k.lower(): v for k, v in user_apps.items() if not k.startswith("_")}
        except (json.JSONDecodeError, OSError):
            pass
    return {}


APP_MAP = {**APP_MAP, **_load_app_overrides()}

FOLDER_MAP = {
    "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
    "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
    "documents": os.path.join(os.path.expanduser("~"), "Documents"),
    "pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
    "vault": os.path.abspath(VAULT_ROOT),
}


def _open_app(name: str) -> str:
    target = APP_MAP.get(name.lower().strip())
    if not target:
        return None
    os.system(f'start "" "{target}"')
    return f"Opening {name}."


def _open_folder(name: str) -> str:
    target = FOLDER_MAP.get(name.lower().strip())
    if not target:
        return None
    os.startfile(target)
    return f"Opened {name} folder."


def _battery_status() -> str:
    import psutil
    battery = psutil.sensors_battery()
    if battery is None:
        return "No battery detected — probably a desktop, not a laptop."
    plugged = "charging" if battery.power_plugged else "on battery"
    return f"{battery.percent}% battery, {plugged}."


def _system_status() -> str:
    import psutil
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    return f"CPU at {cpu}%, RAM at {ram}%."


def _take_screenshot() -> str:
    from PIL import ImageGrab
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = os.path.join(SCREENSHOT_DIR, filename)
    img = ImageGrab.grab()
    img.save(path)
    return f"Screenshot saved to vault/screenshots/{filename}."


def _search_files(query: str) -> str:
    """Shallow search across common user folders for a filename match."""
    search_dirs = [FOLDER_MAP["desktop"], FOLDER_MAP["downloads"], FOLDER_MAP["documents"]]
    matches = []
    for base in search_dirs:
        if not os.path.isdir(base):
            continue
        for root, dirs, files in os.walk(base):
            # keep it shallow — don't crawl the whole disk
            depth = root[len(base):].count(os.sep)
            if depth >= 2:
                dirs[:] = []
                continue
            for f in files:
                if query.lower() in f.lower():
                    matches.append(os.path.join(root, f))
            if len(matches) >= 10:
                break
    if not matches:
        return f"No files matching '{query}' found in Desktop, Downloads, or Documents."
    listing = "\n".join(matches[:10])
    return f"Found {len(matches)} match(es):\n{listing}"


# --- Intent matching: regex pattern -> handler ---
# Order matters — more specific patterns first.
ACTION_PATTERNS = [
    (re.compile(r"open (?:the )?(.+?) folder", re.I), lambda m: _open_folder(m.group(1))),
    (re.compile(r"open (.+)", re.I), lambda m: _open_app(m.group(1))),
    (re.compile(r"launch (.+)", re.I), lambda m: _open_app(m.group(1))),
    (re.compile(r"battery|charge left|power level", re.I), lambda m: _battery_status()),
    (re.compile(r"system status|cpu usage|ram usage|how'?s my (?:pc|laptop|system)", re.I), lambda m: _system_status()),
    (re.compile(r"(?:take a |take )?screenshot", re.I), lambda m: _take_screenshot()),
    (re.compile(r"find (?:a |the )?file (?:called |named )?(.+)", re.I), lambda m: _search_files(m.group(1))),
    (re.compile(r"search (?:for )?(?:a |the )?file (?:called |named )?(.+)", re.I), lambda m: _search_files(m.group(1))),
]


def try_action(query: str):
    """
    Returns a result string if the query matched a known safe action,
    or None if nothing matched (caller should fall through to the LLM).
    """
    for pattern, handler in ACTION_PATTERNS:
        match = pattern.search(query)
        if match:
            try:
                result = handler(match)
                if result:
                    return result
            except Exception as e:
                return f"Tried to do that but hit an error: {e}"
    return None


if __name__ == "__main__":
    # quick manual test
    tests = ["open chrome", "open downloads folder", "what's my battery", "take a screenshot"]
    for t in tests:
        print(f"{t} -> {try_action(t)}")
