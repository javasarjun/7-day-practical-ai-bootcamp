#!/bin/bash
# First-time setup for Demo Studio (creates venv, installs deps + Chromium).
cd "$(dirname "$0")" || exit 1

if [ ! -d ".venv" ]; then
  echo "Setting up Demo Studio..."
  python3 -m venv .venv || { echo "Need Python 3."; read -n1; exit 1; }
  ./.venv/bin/pip install --upgrade pip >/dev/null
  ./.venv/bin/pip install -r requirements.txt || { echo "Install failed."; read -n1; exit 1; }
  ./.venv/bin/playwright install chromium || { echo "Browser install failed."; read -n1; exit 1; }
fi

echo ""
echo "Setup done. To record a demo:"
echo "  1. In another terminal, start your app:   streamlit run app.py"
echo "     (and make sure Ollama is running)"
echo "  2. Then run:"
echo "     ./.venv/bin/python demo_runner.py demo_script_day2.md"
echo ""
echo "  Tip: add --dry-run to test narration without the browser,"
echo "       and --audio-offset -0.3 to nudge the voice earlier if it lags."
echo ""
read -n 1 -s -r -p "Press any key to close..."
