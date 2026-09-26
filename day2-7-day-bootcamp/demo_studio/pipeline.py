"""Core pipeline for Narration Studio (no Streamlit; unit-testable).

PDF -> slide images, speaker-notes markdown -> per-slide text, ElevenLabs TTS,
and drift-free assembly: continuous audio over frame-locked slide durations,
with a lead-in so each slide appears before its narration begins.
"""

import os
import re
import shutil
import subprocess
from pathlib import Path

import requests

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None


def _resolve_ffmpeg():
    """Prefer a real system ffmpeg (most codecs, incl. videotoolbox on macOS);
    fall back to the pip-installed imageio-ffmpeg binary."""
    sys_ff = shutil.which("ffmpeg")
    if sys_ff:
        return sys_ff
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


FFMPEG = _resolve_ffmpeg()
DEFAULT_VOICE_ID = "sS4ouqpoDeVp4REpSCJj"

# Encoder candidates tried in order. All h264 outputs play in browsers; mpeg4 is
# a last-resort that always exists (download-only preview).
ENCODER_CANDIDATES = [
    ("libx264", ["-preset", "veryfast", "-tune", "stillimage"]),
    ("h264_videotoolbox", ["-b:v", "8M"]),
    ("mpeg4", ["-q:v", "3"]),
]


# --------------------------------------------------------------------------- #
# Notes / key helpers
# --------------------------------------------------------------------------- #

def load_env_key(app_dir: Path) -> str:
    env_path = Path(app_dir) / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() == "ELEVENLABS_API_KEY":
                return v.strip().strip('"').strip("'")
    return os.environ.get("ELEVENLABS_API_KEY", "").strip()


def clean_key(raw: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "", raw or "")


def parse_notes(md_text: str):
    """Split '### Slide N — Title' markdown into ordered per-slide narration."""
    parts = re.split(r"^###\s+Slide\b.*$", md_text, flags=re.MULTILINE)
    sections = []
    for body in parts[1:]:
        body = body.replace("---", "").strip()
        body = re.sub(r"\n{3,}", "\n\n", body).strip()
        if body:
            sections.append(body)
    return sections


def render_pdf(pdf_bytes: bytes, out_dir: Path, target_w: int = 1920):
    """Render each PDF page to an even-dimension PNG. Returns list of paths."""
    if fitz is None:
        raise RuntimeError("PyMuPDF (pymupdf) is not installed.")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    paths = []
    for i, page in enumerate(doc, start=1):
        zoom = target_w / page.rect.width
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        p = out_dir / f"slide-{i}.png"
        pix.save(str(p))
        paths.append(p)
    doc.close()
    return paths


# --------------------------------------------------------------------------- #
# ElevenLabs
# --------------------------------------------------------------------------- #

def tts_elevenlabs(text, voice_id, key, model_id="eleven_multilingual_v2",
                   stability=0.9, similarity=0.5, style=0.0,
                   use_speaker_boost=False, seed=12345):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128"
    body = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity,
            "style": style,
            "use_speaker_boost": use_speaker_boost,
        },
        "seed": seed,
    }
    headers = {"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"}
    r = requests.post(url, json=body, headers=headers, timeout=180)
    if r.status_code != 200:
        snippet = r.text[:300]
        if "<html" in snippet.lower():
            raise RuntimeError(
                f"HTTP {r.status_code} from the frontend (not ElevenLabs) — "
                "the API key is likely invalid or malformed."
            )
        raise RuntimeError(f"ElevenLabs HTTP {r.status_code}: {snippet}")
    return r.content


# --------------------------------------------------------------------------- #
# ffmpeg helpers
# --------------------------------------------------------------------------- #

def run_ffmpeg(args, quiet_errors=False):
    if FFMPEG is None:
        raise RuntimeError("ffmpeg not found (pip install imageio-ffmpeg, or brew install ffmpeg).")
    cmd = [FFMPEG, "-y", "-v", "error"] + args
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        if quiet_errors:
            raise RuntimeError(p.stderr.strip())
        raise RuntimeError(
            "ffmpeg command failed.\n"
            f"  args: {' '.join(str(a) for a in args)}\n"
            f"  error:\n{p.stderr.strip()}"
        )
    return p


def list_encoders():
    if FFMPEG is None:
        return set()
    p = subprocess.run([FFMPEG, "-hide_banner", "-encoders"],
                       capture_output=True, text=True)
    return {m for m in re.findall(r"\b([A-Za-z0-9_]+)\b", p.stdout)}


def _still_args(img, dur, fps, encoder, extra, out):
    """Canonical, widely-compatible still-image -> video command."""
    vf = "format=yuv420p,scale=trunc(iw/2)*2:trunc(ih/2)*2"
    return (["-loop", "1", "-framerate", str(fps), "-t", str(dur), "-i", str(img),
             "-vf", vf, "-r", str(fps), "-c:v", encoder] + extra +
            ["-an", str(out)])


def pick_encoder(sample_img, work, fps=25):
    """Find an encoder that actually works in THIS ffmpeg build by trying a
    short test encode. Returns (encoder_name, extra_args)."""
    work = Path(work)
    test = work / "_enc_test.mp4"
    errors = []
    for enc, extra in ENCODER_CANDIDATES:
        try:
            run_ffmpeg(_still_args(sample_img, 0.5, fps, enc, extra, test),
                       quiet_errors=True)
            try:
                test.unlink(missing_ok=True)
            except OSError:
                pass
            return enc, extra
        except RuntimeError as e:
            errors.append(f"{enc}: {str(e).splitlines()[-1][:120]}")
    raise RuntimeError(
        "No working video encoder found in this ffmpeg build.\n  Tried:\n  - "
        + "\n  - ".join(errors)
        + "\n\nFix: install a full ffmpeg with `brew install ffmpeg`, then relaunch."
    )


def media_duration(path):
    p = subprocess.run([FFMPEG, "-i", str(path)], capture_output=True, text=True)
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", p.stderr)
    if not m:
        raise RuntimeError(f"Could not read duration of {path}")
    h, mn, s = m.groups()
    return int(h) * 3600 + int(mn) * 60 + float(s)


# --------------------------------------------------------------------------- #
# Assembly
# --------------------------------------------------------------------------- #

def build_video(slide_imgs, mp3_paths, work, out_path,
                lead=1.2, tail=0.6, fps=25, progress=None):
    work = Path(work)
    slide_imgs = list(slide_imgs)
    mp3_paths = list(mp3_paths)

    # choose one encoder up front so every segment uses the same codec (needed
    # for stream-copy concat) and we fail fast with a clear message if none work
    encoder, extra = pick_encoder(slide_imgs[0], work, fps=fps)

    vlist, alist = [], []
    for n, (img, mp3) in enumerate(zip(slide_imgs, mp3_paths), start=1):
        narr = media_duration(mp3)
        frames = round((lead + narr + tail) * fps)
        dur = frames / fps
        delay_ms = int(lead * 1000)

        a_wav = work / f"a{n}.wav"
        run_ffmpeg([
            "-i", str(mp3),
            "-filter_complex",
            f"[0:a]aresample=48000,adelay={delay_ms}:all=1,apad=whole_dur={dur}[a]",
            "-map", "[a]", "-c:a", "pcm_s16le", str(a_wav),
        ])
        v_mp4 = work / f"v{n}.mp4"
        run_ffmpeg(_still_args(img, dur, fps, encoder, extra, v_mp4))

        vlist.append(v_mp4.name)
        alist.append(a_wav.name)
        if progress:
            progress(n)

    (work / "vlist.txt").write_text("".join(f"file '{x}'\n" for x in vlist))
    (work / "alist.txt").write_text("".join(f"file '{x}'\n" for x in alist))
    run_ffmpeg(["-f", "concat", "-safe", "0", "-i", str(work / "vlist.txt"),
                "-c", "copy", str(work / "video_only.mp4")])
    run_ffmpeg(["-f", "concat", "-safe", "0", "-i", str(work / "alist.txt"),
                "-c", "copy", str(work / "full_audio.wav")])
    run_ffmpeg([
        "-i", str(work / "video_only.mp4"), "-i", str(work / "full_audio.wav"),
        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
        "-b:a", "192k", "-movflags", "+faststart", str(out_path),
    ])
    return encoder, out_path
