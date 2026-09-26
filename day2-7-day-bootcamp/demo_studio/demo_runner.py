"""
Demo Studio — record a narrated, live walkthrough of a running web app.

Pipeline:
  1. Parse a demo script (beats: actions + narration).
  2. Generate narration audio per beat (ElevenLabs) and measure each length.
  3. Drive the app with Playwright while it records video. After each beat's
     actions settle, HOLD on screen for that beat's narration length, and record
     the real time offset where the narration should start.
  4. Overlay each narration clip onto the recorded video at its measured offset,
     then mux to an MP4.

Because the automation paces itself to the narration, voice and picture stay in
sync even though model responses take a variable amount of time.

Usage:
  python demo_runner.py demo_script_day2.md                 # full run (needs browser + app running)
  python demo_runner.py demo_script_day2.md --dry-run       # narration + plan only, no browser
  python demo_runner.py demo_script_day2.md --out demo.mp4 --audio-offset -0.2
"""

import argparse
import re
import sys
import time
from pathlib import Path

from pipeline import (
    load_env_key, clean_key, tts_elevenlabs, run_ffmpeg, media_duration,
    pick_encoder, FFMPEG, DEFAULT_VOICE_ID,
)

APP_DIR = Path(__file__).resolve().parent
SETTLE_MS = 700          # pause after actions before narration starts
TAIL_PAD = 0.4           # extra hold after each narration clip


# --------------------------------------------------------------------------- #
# Demo-script parsing
# --------------------------------------------------------------------------- #

def parse_demo(md_text):
    """Returns (config: dict, beats: list).
    Each beat: {title, actions: [(verb, params_dict)], narration: str}.

    Format:
        url: http://localhost:8501
        viewport: 1280x800

        ### Beat 1 — Title
        do: click | button=Compare AI Responses
        do: wait_for | text=Response from Strong Prompt
        narration: Now I click compare and both answers come back...
    """
    # header config = lines before the first '### Beat'
    head, _, rest = md_text.partition("\n### Beat")
    config = {}
    for line in head.splitlines():
        m = re.match(r"^([A-Za-z_]+):\s*(.+)$", line.strip())
        if m:
            config[m.group(1).lower()] = m.group(2).strip()

    beats = []
    blocks = re.split(r"^###\s+Beat\b[^\n]*$", md_text, flags=re.MULTILINE)
    titles = re.findall(r"^###\s+Beat\b([^\n]*)$", md_text, flags=re.MULTILINE)
    for title, body in zip(titles, blocks[1:]):
        actions = []
        for m in re.finditer(r"^do:\s*(.+)$", body, flags=re.MULTILINE):
            parts = [p.strip() for p in m.group(1).split("|")]
            verb = parts[0]
            params = {}
            for kv in parts[1:]:
                if "=" in kv:
                    k, v = kv.split("=", 1)
                    params[k.strip()] = v.strip()
            actions.append((verb, params))
        nm = re.search(r"^narration:\s*(.*?)(?=^\s*do:|^###|\Z)", body,
                       flags=re.MULTILINE | re.DOTALL)
        narration = ""
        if nm:
            narration = re.sub(r"\s+", " ", nm.group(1)).strip()
        beats.append({"title": title.strip(" —-"), "actions": actions,
                      "narration": narration})
    return config, beats


# --------------------------------------------------------------------------- #
# Narration
# --------------------------------------------------------------------------- #

def generate_narration(beats, work, voice_id, key, model_id, stability,
                       similarity, style):
    clips = []
    for i, b in enumerate(beats, start=1):
        if not b["narration"]:
            clips.append(None)
            continue
        audio = tts_elevenlabs(b["narration"], voice_id, key, model_id=model_id,
                               stability=stability, similarity=similarity, style=style)
        mp3 = work / f"beat{i}.mp3"
        mp3.write_bytes(audio)
        clips.append(mp3)
    return clips


# --------------------------------------------------------------------------- #
# Playwright driving
# --------------------------------------------------------------------------- #

def _locator(page, params):
    """Resolve a semantic selector to a Playwright locator. Prefer the stable
    keys (button=, textbox=, testid=, label=) over raw locator= (which often
    captures Streamlit's volatile st-emotion-cache classes)."""
    if "button" in params:
        return page.get_by_role("button", name=params["button"])
    if "testid" in params:
        return page.get_by_test_id(params["testid"])
    if "textbox" in params:
        return page.get_by_role("textbox", name=params["textbox"])
    if "label" in params:
        return page.get_by_label(params["label"])
    if "placeholder" in params:
        return page.get_by_placeholder(params["placeholder"])
    if "role" in params and "name" in params:
        return page.get_by_role(params["role"], name=params["name"])
    if "text_exact" in params:
        return page.get_by_text(params["text_exact"], exact=True)
    if "text" in params:
        return page.get_by_text(params["text"])
    if "locator" in params:
        return page.locator(params["locator"])
    if "selector" in params:
        return page.locator(params["selector"])
    raise ValueError(f"No usable selector in {params}")


def streamlit_select(page, params):
    """Open a Streamlit selectbox (identified by its label) and click an option.
    Streamlit selectboxes are not native <select> elements — you click to open
    the popup, then click the option text."""
    value = params["value"]
    if "label" in params:
        box = page.get_by_test_id("stSelectbox").filter(has_text=params["label"]).first
    else:
        box = _locator(page, params)
    box.click()
    try:
        page.get_by_role("option", name=value).first.click(timeout=4000)
    except Exception:
        page.get_by_text(value, exact=True).last.click()


def do_action(page, verb, params):
    if verb == "goto":
        page.goto(params.get("url") or params.get("value"))
    elif verb == "click":
        _locator(page, params).click()
    elif verb == "fill":
        _locator(page, params).fill(params.get("value", ""))
    elif verb == "select":
        streamlit_select(page, params)
    elif verb == "press":
        page.keyboard.press(params.get("key", "Enter"))
    elif verb == "wait_for":
        if "selector" in params:
            page.wait_for_selector(params["selector"], timeout=120000)
        else:
            _locator(page, params).wait_for(timeout=120000)
    elif verb == "wait":
        time.sleep(float(params.get("seconds", 1)))
    elif verb == "scroll":
        page.mouse.wheel(0, int(params.get("y", 400)))
    else:
        raise ValueError(f"Unknown action verb: {verb}")


def run_browser(config, beats, clips, work):
    """Drives the app, records video, returns (video_path, [(clip, offset)])."""
    from playwright.sync_api import sync_playwright

    w, h = 1280, 800
    if "viewport" in config and "x" in config["viewport"]:
        w, h = (int(x) for x in config["viewport"].lower().split("x"))
    url = config.get("url", "http://localhost:8501")

    placed = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.get("headless", "true") == "true")
        context = browser.new_context(
            viewport={"width": w, "height": h},
            record_video_dir=str(work),
            record_video_size={"width": w, "height": h},
        )
        page = context.new_page()
        rec_start = time.monotonic()
        page.goto(url, wait_until="load")
        page.wait_for_timeout(1500)  # let Streamlit hydrate

        for b, clip in zip(beats, clips):
            for verb, params in b["actions"]:
                try:
                    do_action(page, verb, params)
                except Exception as e:
                    print(f"  [warn] action {verb} {params} failed: {e}")
            page.wait_for_timeout(SETTLE_MS)
            if clip is not None:
                offset = time.monotonic() - rec_start
                dur = media_duration(clip)
                placed.append((clip, offset))
                time.sleep(dur + TAIL_PAD)
            else:
                time.sleep(0.5)

        context.close()
        video_path = Path(page.video.path())
        browser.close()
    return video_path, placed


# --------------------------------------------------------------------------- #
# Mux narration over the recording
# --------------------------------------------------------------------------- #

def mux(video_path, placed, out_path, work, audio_offset=0.0):
    video_dur = media_duration(video_path)
    # build a single audio track: each clip delayed to its measured offset
    inputs, filt = [], []
    for i, (clip, off) in enumerate(placed):
        inputs += ["-i", str(clip)]
        ms = max(0, int((off + audio_offset) * 1000))
        filt.append(f"[{i}:a]adelay={ms}:all=1[d{i}]")
    mix = "".join(f"[d{i}]" for i in range(len(placed)))
    filt.append(f"{mix}amix=inputs={len(placed)}:normalize=0[m]")
    filt.append(f"[m]aresample=48000,apad=whole_dur={video_dur}[a]")
    audio_wav = work / "demo_audio.wav"
    run_ffmpeg(inputs + ["-filter_complex", ";".join(filt),
                         "-map", "[a]", "-c:a", "pcm_s16le", str(audio_wav)])

    enc, extra = pick_encoder_for_video(work)
    run_ffmpeg([
        "-i", str(video_path), "-i", str(audio_wav),
        "-map", "0:v", "-map", "1:a",
        "-c:v", enc, *extra, "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out_path),
    ])
    return out_path


def pick_encoder_for_video(work):
    # libx264 first, then Apple hardware, then mpeg4
    for enc, extra in (("libx264", ["-preset", "veryfast", "-crf", "20"]),
                       ("h264_videotoolbox", ["-b:v", "6M"]),
                       ("mpeg4", ["-q:v", "4"])):
        try:
            run_ffmpeg(["-f", "lavfi", "-i", "color=c=black:s=320x240:d=0.3",
                        "-c:v", enc, *extra, "-pix_fmt", "yuv420p",
                        str(work / "_enc_probe.mp4")], quiet_errors=True)
            return enc, extra
        except Exception:
            continue
    raise RuntimeError("No working video encoder (try: brew install ffmpeg).")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def run_codegen(url):
    """Launch Playwright's interactive recorder. Click through the app by hand;
    it prints the selectors for everything you touch. Translate those into
    demo-script `do:` lines using SELECTORS.md."""
    import shutil
    import subprocess
    exe = shutil.which("playwright")
    if not exe:
        sys.exit("playwright not found. Run: pip install playwright && playwright install chromium")
    print(f"Opening Playwright recorder on {url} …")
    print("Click through your app; the Inspector window shows the selector for each action.")
    print("When done, copy the selectors into your demo script (see SELECTORS.md).")
    subprocess.run([exe, "codegen", url, "--target", "python"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script", nargs="?")
    ap.add_argument("--codegen", action="store_true",
                    help="launch Playwright's selector recorder against the app, then exit")
    ap.add_argument("--url", default=None, help="app URL (for --codegen)")
    ap.add_argument("--out", default="demo.mp4")
    ap.add_argument("--dry-run", action="store_true",
                    help="generate narration + print the plan; no browser")
    ap.add_argument("--audio-offset", type=float, default=0.0,
                    help="nudge all narration earlier(-)/later(+) in seconds")
    ap.add_argument("--voice-id", default=None)
    ap.add_argument("--model", default="eleven_multilingual_v2")
    ap.add_argument("--stability", type=float, default=0.90)
    ap.add_argument("--similarity", type=float, default=0.50)
    ap.add_argument("--style", type=float, default=0.0)
    args = ap.parse_args()

    if args.codegen:
        url = args.url
        if not url and args.script:
            cfg, _ = parse_demo(Path(args.script).read_text())
            url = cfg.get("url")
        run_codegen(url or "http://localhost:8501")
        return

    if not args.script:
        sys.exit("Pass a demo-script .md (or use --codegen to record selectors).")
    if FFMPEG is None:
        sys.exit("ffmpeg not found (brew install ffmpeg, or pip install imageio-ffmpeg).")

    config, beats = parse_demo(Path(args.script).read_text())
    print(f"Parsed {len(beats)} beats. App URL: {config.get('url','http://localhost:8501')}")
    for i, b in enumerate(beats, 1):
        acts = "; ".join(f"{v}({','.join(f'{k}={x}' for k,x in p.items())})" for v, p in b["actions"])
        print(f"  Beat {i}: {b['title']}  | actions: [{acts or 'none'}] | narration: {len(b['narration'])} chars")

    work = APP_DIR / "_demo_work"
    work.mkdir(exist_ok=True)

    key = clean_key(load_env_key(APP_DIR))
    voice_id = args.voice_id or DEFAULT_VOICE_ID
    if not args.dry_run and not key:
        sys.exit("No ELEVENLABS_API_KEY in .env.")

    if key:
        print("Generating narration...")
        clips = generate_narration(beats, work, voice_id, key, args.model,
                                   args.stability, args.similarity, args.style)
        print(f"  {sum(c is not None for c in clips)} narration clips.")
    else:
        clips = [None] * len(beats)

    if args.dry_run:
        print("\nDry run complete. Narration generated; browser not launched.")
        return

    print("Launching browser and recording (make sure the app is running)...")
    video_path, placed = run_browser(config, beats, clips, work)
    print(f"  Recorded: {video_path}  | {len(placed)} narration cues placed.")

    out = APP_DIR / args.out
    mux(video_path, placed, out, work, audio_offset=args.audio_offset)
    print(f"\nDone -> {out}")


if __name__ == "__main__":
    main()
