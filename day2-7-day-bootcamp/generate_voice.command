#!/bin/bash
# Generates Indian-accent narration for Lecture 14 using macOS's built-in "Rishi" voice.
# Double-click this file (or run it in Terminal). No installation needed.

cd "$(dirname "$0")" || exit 1

VOICE="Rishi"
echo "=============================================="
echo " Lecture 14 narration — Indian English (Rishi)"
echo "=============================================="

# Check the Rishi voice is installed
if ! say -v '?' | grep -qi "Rishi"; then
  echo ""
  echo "  The 'Rishi' Indian English voice is not installed yet."
  echo "  Install it once (takes ~1 minute):"
  echo "    System Settings  >  Accessibility  >  Spoken Content"
  echo "    >  System Voice  >  Manage Voices...  >  English (India)  >  Rishi"
  echo ""
  echo "  Then double-click this file again."
  echo ""
  read -n 1 -s -r -p "Press any key to close..."
  exit 1
fi

mkdir -p narration
ok=0
for n in 1 2 3 4 5; do
  if [ ! -f "narration/slide${n}.txt" ]; then
    echo "  Missing narration/slide${n}.txt — skipping."
    continue
  fi
  echo "  Generating slide ${n} ..."
  say -v "$VOICE" -f "narration/slide${n}.txt" -o "narration/slide${n}.aiff" && ok=$((ok+1))
done

echo ""
echo "  Done. Created ${ok} of 5 audio clips in the 'narration' folder."
echo "  You can close this window and tell Claude the voice export is finished."
echo ""
read -n 1 -s -r -p "Press any key to close..."
