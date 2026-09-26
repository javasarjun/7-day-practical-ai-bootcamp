"""
Lab Studio — turn a Lab-Mode markdown file (code + speaker notes per step) into
a narrated code-walkthrough video. IDE-style code visuals (rendered from your
real code) instead of slides, narrated in your ElevenLabs voice, assembled with
the same drift-free lead-in pipeline as Narration Studio.

Run:  streamlit run app.py
"""

import tempfile
from pathlib import Path

import streamlit as st

from pipeline import (
    DEFAULT_VOICE_ID, FFMPEG, load_env_key, clean_key,
    tts_elevenlabs, build_video, list_encoders,
)
from editor_render import (
    parse_lab, render_code_image, resolve_highlight, viewport_first, THEMES,
)
import author

APP_DIR = Path(__file__).resolve().parent

st.set_page_config(page_title="Lab Studio", page_icon="🧑‍💻", layout="wide")
st.title("🧑‍💻 Lab Studio")
st.caption("Lab-Mode markdown → narrated code-walkthrough video, in your voice.")

if FFMPEG is None:
    st.error("ffmpeg not found. Install with: pip install imageio-ffmpeg (or brew install ffmpeg)")
    st.stop()

with st.sidebar:
    st.header("Settings")
    mode = st.radio("Mode", ["Render video", "Author lab from code"])
    st.divider()
    env_key = load_env_key(APP_DIR)
    if env_key:
        st.success("API key loaded from .env")
        api_key = env_key
    else:
        st.warning("No .env key found — paste one below.")
        api_key = st.text_input("ElevenLabs API key", type="password")
    voice_id = st.text_input("Voice ID", value=DEFAULT_VOICE_ID)
    model_id = st.selectbox("Model", ["eleven_multilingual_v2", "eleven_turbo_v2_5"], index=0)
    st.markdown("**Voice settings**")
    stability = st.slider("Stability", 0.0, 1.0, 0.90, 0.05,
                          help="Higher = calmer delivery, fewer breath sounds")
    similarity = st.slider("Similarity boost", 0.0, 1.0, 0.50, 0.05,
                           help="Lower = fewer breaths reproduced from the voice samples")
    style = st.slider("Style", 0.0, 1.0, 0.0, 0.05)
    speaker_boost = st.checkbox("Speaker boost", value=False,
                                help="Off reduces breath/artifacts; on boosts voice likeness")
    st.markdown("**Editor & timing**")
    theme = st.selectbox("Editor theme", list(THEMES.keys()), index=0)
    font_size = st.slider("Code font size", 20, 40, 28, 1)
    lead = st.slider("Lead-in before voice (s)", 0.0, 3.0, 1.2, 0.1)
    tail = st.slider("Tail after voice (s)", 0.0, 2.0, 0.6, 0.1)
    fps = st.selectbox("Frame rate", [25, 30], index=0)

    with st.expander("ffmpeg diagnostics"):
        st.caption(f"binary: {FFMPEG or 'NOT FOUND'}")
        encs = list_encoders()
        have = [e for e in ("libx264", "h264_videotoolbox", "mpeg4") if e in encs]
        st.caption("video encoders: " + (", ".join(have) or "none detected"))
        if "libx264" not in encs and "h264_videotoolbox" not in encs:
            st.warning("No h264 encoder found. For best results: brew install ffmpeg")

# --------------------------------------------------------------------------- #
# AUTHOR MODE — generate Lab-Mode .md from code + notes via a frontier LLM
# --------------------------------------------------------------------------- #
if mode == "Author lab from code":
    st.subheader("Author a lab from code + notes")
    st.caption("Sends your code and notes through lab_authoring_prompt.md to a "
               "frontier model, and returns ready-to-render Lab-Mode markdown.")

    provider = st.selectbox("Provider", ["Anthropic", "OpenAI"], index=0)
    default_model = author.DEFAULT_MODELS[provider]
    a_model = st.text_input("Model", value=default_model)
    a_key = author.read_env(APP_DIR, author.ENV_KEY[provider])
    if a_key:
        st.success(f"{author.ENV_KEY[provider]} loaded from .env")
    else:
        st.warning(f"No {author.ENV_KEY[provider]} in .env — paste one below.")
        a_key = st.text_input(f"{provider} API key", type="password")
    max_tokens = st.slider("Max output tokens", 2000, 16000, 8000, 1000)

    code_files = st.file_uploader(
        "Project code files (the day's source)", accept_multiple_files=True,
        type=["py", "js", "ts", "tsx", "jsx", "java", "go", "rb", "rs", "c",
              "cpp", "cs", "php", "sql", "sh", "txt", "json"],
    )
    notes_file = st.file_uploader("Teaching notes (.md / .txt)", type=["md", "markdown", "txt"])
    notes_text = st.text_area("…or paste teaching notes here", height=200)

    if st.button("✨ Generate lab markdown", type="primary"):
        if not a_key:
            st.error("No API key for the selected provider.")
            st.stop()
        if not code_files:
            st.error("Upload at least one code file.")
            st.stop()
        files = {f.name: f.read().decode("utf-8", "ignore") for f in code_files}
        notes = notes_text or ""
        if notes_file is not None:
            notes = notes_file.read().decode("utf-8", "ignore") + "\n\n" + notes
        try:
            system = author.load_system_prompt(APP_DIR)
            user = author.build_user_message(files, notes)
            with st.spinner(f"Generating with {provider} {a_model}… (can take a minute)"):
                out = author.generate(provider, a_model, a_key.strip(),
                                      system, user, max_tokens=max_tokens)
            st.session_state.author_output = out
        except Exception as e:
            st.error(str(e))
            st.stop()

    out = st.session_state.get("author_output")
    if out:
        st.success("Draft generated. Review and edit below, then save.")
        edited = st.text_area("Generated Lab-Mode markdown", value=out, height=500,
                              key="author_edit")
        files_out = author.split_files(edited)
        st.caption("Detected files: " + ", ".join(n for n, _ in files_out))
        labs_dir = APP_DIR / "labs"
        labs_dir.mkdir(exist_ok=True)
        if st.button("💾 Save to labs/ folder"):
            saved = []
            for name, content in files_out:
                (labs_dir / name).write_text(content)
                saved.append(name)
            st.success("Saved: " + ", ".join(saved) +
                       "  — switch Mode to 'Render video' and upload one to make the video.")
        for name, content in files_out:
            st.download_button(f"⬇️ {name}", data=content, file_name=name,
                               mime="text/markdown", key=f"dl_{name}")
    st.stop()

lab_file = st.file_uploader("Lab-Mode markdown (.md)", type=["md", "markdown", "txt"])

with st.expander("Lab-Mode file format"):
    st.code(
        "### Step 1 — Sending a request to the model\n"
        "**File:** app/services/llm_service.py\n"
        "**StartLine:** 12      # optional: real line numbers, no reset to 1\n\n"
        "```python\n"
        "class LLMService:\n"
        "    def send_request(self, message): ...\n"
        "```\n\n"
        "**Walkthrough:**\n"
        "@ send_request                 # whole function highlighted (intro)\n"
        "Inside this file we add a new function...\n\n"
        "@ 13-17                        # a line range\n"
        "Here we build the payload...\n\n"
        '@ "if response.status_code"    # a quoted code substring\n'
        "This condition protects us when the request fails...",
        language="markdown",
    )

if lab_file:
    md_text = lab_file.read().decode("utf-8", "ignore")
    steps = parse_lab(md_text)
    if not steps:
        st.error("No steps found. Each step must start with a '### Step N — ...' header.")
        st.stop()

    if "lab_work" not in st.session_state:
        st.session_state.lab_work = tempfile.mkdtemp(prefix="labstudio_")
    work = Path(st.session_state.lab_work)
    img_dir = work / "frames"
    img_dir.mkdir(exist_ok=True)

    total_beats = sum(len(s["beats"]) for s in steps)
    st.subheader(f"Review {len(steps)} steps · {total_beats} beats")

    # flat lists across all beats, in order
    frames = []   # (img_path, narration_text, label)
    for si, s in enumerate(steps, start=1):
        n_lines = s["code"].count("\n") + 1
        offset = s.get("start_line", 1) - 1
        # one stable viewport per step: center on every line this step touches
        focus_union = set()
        for b in s["beats"]:
            focus_union |= resolve_highlight(s["code"], b["highlight"], offset)
        vp = viewport_first(n_lines, focus_union, font_size)

        st.markdown(f"**Step {si} — {s['title']}**  ·  `{s['file']}`")
        for bi, b in enumerate(s["beats"], start=1):
            img_p = img_dir / f"s{si}_b{bi}.png"
            render_code_image(s["code"], s["file"], img_p, lang=s["lang"],
                              highlight=b["highlight"], font_size=font_size,
                              viewport=vp, line_offset=offset, theme=theme)
            c1, c2 = st.columns([1.3, 1])
            c1.image(str(img_p), use_container_width=True,
                     caption=f"beat {bi} · highlight: {b['highlight'] or '(none)'}")
            key_id = f"note_{si}_{bi}"
            text = c2.text_area(f"Narration {si}.{bi}", value=b["text"], height=240, key=key_id)
            frames.append((img_p, text, f"{si}.{bi}"))
        st.divider()

    out_name = st.text_input("Output file name", value="lab_walkthrough.mp4")

    if st.button("🎙️ Generate narration & build video", type="primary"):
        key = clean_key(api_key)
        if not key:
            st.error("No API key. Add one to .env or paste it in the sidebar.")
            st.stop()

        audio_dir = work / "audio"
        audio_dir.mkdir(exist_ok=True)
        n = len(frames)
        prog = st.progress(0.0, text="Generating narration…")
        img_paths, mp3_paths = [], []
        try:
            for i, (img_p, text, label) in enumerate(frames, start=1):
                audio = tts_elevenlabs(text, voice_id, key, model_id=model_id,
                                       stability=stability, similarity=similarity, style=style,
                                       use_speaker_boost=speaker_boost)
                mp3 = audio_dir / f"f{i}.mp3"
                mp3.write_bytes(audio)
                img_paths.append(img_p)
                mp3_paths.append(mp3)
                prog.progress(i / (n * 2), text=f"Narration {label} ({i}/{n})")

            out_path = work / out_name
            encoder, _ = build_video(
                img_paths, mp3_paths, work, out_path,
                lead=lead, tail=tail, fps=fps,
                progress=lambda k: prog.progress(0.5 + k / (n * 2),
                                                 text=f"Building beat {k}/{n}"),
            )
            prog.progress(1.0, text="Done")
        except Exception as e:
            st.error(str(e))
            st.stop()

        st.success(f"Video ready (encoder: {encoder}).")
        video_bytes = out_path.read_bytes()
        st.video(video_bytes)
        st.download_button("⬇️ Download MP4", data=video_bytes,
                           file_name=out_name, mime="video/mp4")
        saved = APP_DIR / out_name
        saved.write_bytes(video_bytes)
        st.caption(f"Also saved to: {saved}")
else:
    st.info("Upload a Lab-Mode .md to begin. See the format above, or start from sample_lab.md.")
