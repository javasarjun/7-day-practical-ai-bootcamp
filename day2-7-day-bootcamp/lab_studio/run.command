#!/bin/bash
# Double-click to launch Lab Studio. First run sets up a local environment.
cd "$(dirname "$0")" || exit 1

if [ ! -d ".venv" ]; then
  echo "First-time setup: creating a local Python environment..."
  python3 -m venv .venv || { echo "Could not create venv. Is Python 3 installed?"; read -n1; exit 1; }
  ./.venv/bin/pip install --upgrade pip >/dev/null
  ./.venv/bin/pip install -r requirements.txt || { echo "Install failed."; read -n1; exit 1; }
fi

echo "Starting Lab Studio in your browser..."
./.venv/bin/streamlit run app.py
