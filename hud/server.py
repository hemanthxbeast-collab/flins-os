"""
FLINS-OS HUD Server
Small Flask app that exposes live skill/vault data as JSON,
and serves the dashboard front end.
"""

import os
import sys
from datetime import datetime
from flask import Flask, jsonify, send_from_directory

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))
from skill_loader import discover_skills

VAULT_ROOT = os.path.join(os.path.dirname(__file__), "..", "vault")

app = Flask(__name__, static_folder="static", static_url_path="")


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/skills")
def api_skills():
    skills = discover_skills()
    grouped = {}
    for s in skills:
        grouped.setdefault(s.branch, []).append(s.name)
    return jsonify(grouped)


@app.route("/api/vault-stats")
def api_vault_stats():
    total_notes = 0
    folders = {}
    if os.path.isdir(VAULT_ROOT):
        for folder in os.listdir(VAULT_ROOT):
            fpath = os.path.join(VAULT_ROOT, folder)
            if os.path.isdir(fpath):
                count = len([f for f in os.listdir(fpath) if f.endswith(".md")])
                folders[folder] = count
                total_notes += count
    return jsonify({"total_notes": total_notes, "folders": folders})


@app.route("/api/recent-logs")
def api_recent_logs():
    logs_dir = os.path.join(VAULT_ROOT, "logs")
    entries = []
    if os.path.isdir(logs_dir):
        files = sorted(
            (f for f in os.listdir(logs_dir) if f.endswith(".md")),
            reverse=True,
        )[:8]
        for f in files:
            path = os.path.join(logs_dir, f)
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()
            title = f.replace(".md", "")
            entries.append({"title": title, "preview": content[:120]})
    return jsonify(entries)


@app.route("/api/status")
def api_status():
    return jsonify({
        "time": datetime.now().strftime("%H:%M:%S"),
        "name": "FLINS",
        "state": "online",
    })


if __name__ == "__main__":
    print("FLINS HUD running at http://localhost:5000")
    app.run(debug=True, port=5000)
