#!/bin/bash
# Generate Lecture 14 narration with your ElevenLabs voice (sS4ouqpoDeVp4REpSCJj).
# Your API key is typed here and stays on your Mac. Nothing is sent to Claude.

cd "$(dirname "$0")" || exit 1

echo "============================================="
echo " ElevenLabs narration — Lecture 14"
echo "============================================="
echo "Paste your ElevenLabs API key (it will be hidden), then press Enter:"
read -r -s ELEVENLABS_API_KEY
export ELEVENLABS_API_KEY
echo ""

if [ -z "$ELEVENLABS_API_KEY" ]; then
  echo "No key entered. Aborting."
  read -n 1 -s -r -p "Press any key to close..."
  exit 1
fi

python3 el_tts.py
status=$?
echo ""
if [ $status -eq 0 ]; then
  echo "Voice export finished. Tell Claude it's done and I'll build the video."
fi
read -n 1 -s -r -p "Press any key to close..."
