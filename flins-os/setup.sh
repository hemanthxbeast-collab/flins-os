#!/bin/bash
set -e

echo "=== FLINS-OS Setup ==="

# 1. Python venv
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi
source venv/bin/activate

# 2. Install deps
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Env file
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "Created .env — go fill in your ANTHROPIC_API_KEY and other keys."
fi

# 4. Vault check
mkdir -p vault/logs vault/research vault/projects
echo "✓ vault mounted"

# 5. Skills check
skill_count=$(find skills -name "SKILL.md" | wc -l)
echo "✓ skills linked ($skill_count found)"

echo ""
echo "Setup done. Run:"
echo "  source venv/bin/activate"
echo "  python core/main.py"
