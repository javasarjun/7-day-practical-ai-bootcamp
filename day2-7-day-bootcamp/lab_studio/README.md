# Lab Studio

For **hands-on coding lectures**. Turn a Lab-Mode markdown file (your code +
speaker notes, one step per function) into a narrated **code-walkthrough video**.
Visuals are real **IDE-style code images** rendered from your actual code —
filename tab, line numbers, syntax highlighting, the target function highlighted,
surrounding code dimmed — not PowerPoint slides.

Narration is generated in your ElevenLabs voice and assembled with the same
drift-free, lead-in pipeline as Narration Studio (each editor view appears, then
the narration begins).

## Two modes

The sidebar has a **Mode** switch:

- **Render video** — upload a Lab-Mode `.md` and produce the narrated video.
- **Author lab from code** — upload the day's source files + teaching notes and a
  frontier LLM (Anthropic or OpenAI) generates the Lab-Mode `.md` for you, using
  `lab_authoring_prompt.md`. Review/edit the draft in-app, save it to `labs/`,
  then switch to Render mode to make the video. This is how you scale to Day
  3–7: feed in each day's code + notes, get ready-to-render labs.

## Setup

1. Put your ElevenLabs key in a `.env` file (copy `.env.example` to `.env`):

   ```
   ELEVENLABS_API_KEY=sk_your_real_key
   ```

2. Launch:
   - **Easiest:** double-click `run.command` (first run installs dependencies).
   - **Or manually:** `pip install -r requirements.txt && streamlit run app.py`

**Most reliable:** `brew install ffmpeg` (guarantees in-browser h264 preview).
Otherwise the app uses the pip `imageio-ffmpeg` binary and auto-selects an encoder.

## Lab-Mode file format

One step per function/method. Each step shows the code once, then a
**walkthrough** of "beats" — each beat highlights just the line(s) being
narrated and is shown for exactly that piece of audio. The viewport stays
fixed across a step, so the function holds still and only the highlight moves
down, line by line.

```
### Step 1 — Sending a request to the model
**File:** app/services/llm_service.py
**Lang:** python                   # optional; inferred from the file extension
**StartLine:** 12                  # optional; real line where this snippet sits

```python
class LLMService:
    def send_request(self, message: str) -> str:
        payload = {"model": self.model, "prompt": message}
        response = requests.post(OLLAMA_URL, json=payload)
        ...
```

**Walkthrough:**
@ send_request
Inside this file we add a new function. It takes the user's message...

@ "def send_request"
Look at the signature. The first parameter is the user's message...

@ 13-17
Here we build the payload that gets sent to the model...

@ "if response.status_code != 200:"
This condition protects us when the request fails...
```

Each beat begins with a line starting `@ <target>`, followed by the narration
for that beat. The **target** picks which line(s) to highlight:

- **a function/class/method name** (e.g. `@ send_request`) — highlights its whole
  body. Good for the opening beat.
- **a quoted code substring** (e.g. `@ "if response.status_code != 200:"`) —
  highlights the matching line(s). **Most robust**, since it doesn't depend on
  line numbers.
- **a line range or single line** (e.g. `@ 13-17`, `@ 21`) — counted from the
  top of the code block (line 1 = first line shown).
- **empty** (`@` alone) — no highlight; the whole view is shown undimmed.

Tip: prefer names and quoted substrings over raw line numbers — they stay
correct even if you edit the code above them.

**StartLine** (optional) sets the real line number the snippet begins at, so the
gutter shows true file positions instead of restarting at 1 every step. Use it
when you show several functions from the same file across steps, so it reads
like one file being built up. When StartLine is set, any numeric `@ a-b` targets
refer to those real line numbers too (names and substrings are unaffected).

**Backward compatible:** a step may instead use a single `**Highlight:**` +
`**Notes:**` pair (one beat for the whole function), as in earlier versions.

See `sample_lab.md` for a complete two-step example.

## How to use

1. Author your lab as a `.md` (or have the Lab-Mode authoring prompt generate it).
2. Launch the app, upload the `.md`.
3. Each step shows its rendered editor image + an editable narration box.
4. Click **Generate narration & build video**, then preview and download the MP4.

## Settings (sidebar)

- **Voice ID / Model / Stability / Similarity / Style** — ElevenLabs voice controls.
- **Code font size** — larger = fewer visible lines per editor view.
- **Lead-in / Tail** — silence before/after narration on each step.
- **Frame rate** — 25 or 30 fps.

## Notes

- The editor theme is VS Code "Dark+". A monospace font is auto-detected
  (Menlo on macOS, DejaVu Sans Mono on Linux).
- If a step's code is longer than fits on screen, the view auto-centers on the
  highlighted function so it's always visible with surrounding context.
- Your API key is read from `.env` and never leaves your machine.
