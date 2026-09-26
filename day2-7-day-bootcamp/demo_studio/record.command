#!/bin/bash
# Double-click to record selectors with Playwright's recorder.
# Make sure your app is already running (streamlit run app.py) first.
cd "$(dirname "$0")" || exit 1

if [ ! -d ".venv" ]; then
  echo "Run setup first: double-click run.command"
  read -n1; exit 1
fi

URL="${1:-http://localhost:8501}"
echo "Opening the Playwright recorder on $URL"
echo "Click through your app; copy the selector lines it prints."
echo "Then translate them into demo-script 'do:' lines using SELECTORS.md."
echo ""
./.venv/bin/python demo_runner.py --codegen --url "$URL"
