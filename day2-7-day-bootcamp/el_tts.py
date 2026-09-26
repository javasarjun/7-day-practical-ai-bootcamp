#!/usr/bin/env python3
"""Generate Lecture 14 narration with an ElevenLabs voice.
Reads narration/slide1.txt..slide5.txt and writes narration/slide1.mp3..slide5.mp3.
Your API key is read from the ELEVENLABS_API_KEY environment variable and never leaves your machine.
"""
import os, sys, json, re, urllib.request, pathlib

VOICE_ID = "sS4ouqpoDeVp4REpSCJj"
MODEL_ID = "eleven_multilingual_v2"   # high quality; change to eleven_turbo_v2_5 for faster/cheaper
OUTPUT_FORMAT = "mp3_44100_128"

raw = os.environ.get("ELEVENLABS_API_KEY", "")
# Scrub anything that isn't a valid API-key character (spaces, newlines, NBSP,
# smart quotes pasted around the key, etc.). ElevenLabs keys are [A-Za-z0-9_].
key = re.sub(r"[^A-Za-z0-9_]", "", raw)
if not key:
    sys.exit("ERROR: set ELEVENLABS_API_KEY first (export ELEVENLABS_API_KEY=sk_...).")
print(f"  API key looks like: {key[:3]}...{key[-2:]}  (length {len(key)})")
if len(raw.strip()) != len(key):
    print(f"  (cleaned {len(raw.strip()) - len(key)} stray character(s) from the pasted key)")

# Optional: pass slide numbers to (re)generate only those, e.g. `python3 el_tts.py 3`
which = [int(a) for a in sys.argv[1:] if a.isdigit()] or [1, 2, 3, 4, 5]

here = pathlib.Path(__file__).resolve().parent
narr = here / "narration"

ok = 0
for n in which:
    txt_path = narr / f"slide{n}.txt"
    if not txt_path.exists():
        print(f"  slide{n}: missing {txt_path.name}, skipping")
        continue
    text = txt_path.read_text(encoding="utf-8").strip()
    body = json.dumps({
        "text": text,
        "model_id": MODEL_ID,
        # Low-breath preset: high stability + low similarity_boost + speaker boost off
        # minimizes the inhale/breath sounds a cloned voice reproduces from its samples.
        "voice_settings": {"stability": 0.9, "similarity_boost": 0.5, "style": 0.0, "use_speaker_boost": False},
        "seed": 12345,
    }).encode("utf-8")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}?output_format={OUTPUT_FORMAT}"
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "xi-api-key": key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    })
    print(f"  Generating slide{n} ...")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            audio = r.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")
        if "<html" in body.lower():
            sys.exit(f"  slide{n} failed: HTTP {e.code} from the frontend (not ElevenLabs).\n"
                     f"  This usually means the API key still has a bad character, or the key is invalid.\n"
                     f"  Double-check you copied the FULL key with no spaces/line breaks, then re-run.")
        sys.exit(f"  slide{n} failed: HTTP {e.code} {body[:400]}")
    out = narr / f"slide{n}.mp3"
    out.write_bytes(audio)
    print(f"    saved {out.name} ({len(audio)//1024} KB)")
    ok += 1

print(f"\nDone. Created {ok} of 5 mp3 clips in {narr}")
