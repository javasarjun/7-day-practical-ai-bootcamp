# Demo Studio (v1 — live app walkthrough)

Records a **narrated, live walkthrough of your running web app**. It drives the
app with a real browser (Playwright) while recording video, paces each step to
the length of its narration, and overlays your ElevenLabs voice in sync.

This is the third sibling to Narration Studio (slides) and Lab Studio (code).
Use it for the **demo lecture** — the part where the app actually runs.

> **Heads up:** this v1 drives a real browser, so it can't be tested without one.
> Expect to tweak selectors and timing on your first couple of runs. Use
> `--dry-run` to validate narration first, and `--audio-offset` to fine-tune sync.

## Setup

1. `cp .env.example .env` and add your `ELEVENLABS_API_KEY`.
2. Double-click `run.command` (creates a venv, installs deps, downloads Chromium).
   Or manually:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

## Workflow

1. **Start the app** you want to demo, in another terminal (and Ollama if used):
   ```bash
   streamlit run app.py
   ```
2. **Record the selectors** (do this once per app). Double-click `record.command`,
   or:
   ```bash
   ./.venv/bin/python demo_runner.py --codegen --url http://localhost:8501
   ```
   Click through your flow; Playwright's Inspector prints a selector for each
   action. Translate those into demo-script `do:` lines using **`SELECTORS.md`**
   (it has a direct mapping table). You only do this when the UI changes.
3. **Write the scenario**: wrap your `do:` lines into beats with a `narration:`
   line each (see `demo_script_day2.md`).
4. **Render the demo**:
   ```bash
   ./.venv/bin/python demo_runner.py demo_script_day2.md
   ```
   Output: `demo.mp4` next to the script. Use `--dry-run` to check narration
   first, and `--audio-offset` to fine-tune sync.

Flags:
- `--dry-run` — generate the narration and print the action plan, but don't open
  the browser. Good for checking your script and voice first.
- `--audio-offset -0.3` — shift all narration earlier (negative) or later
  (positive) in seconds, if the voice consistently leads or lags the picture.
- `--out my_demo.mp4`, `--voice-id ...`, `--model ...`, `--stability ...`.

## Demo-script format

A header (app URL, viewport) followed by **beats**. Each beat has zero or more
`do:` actions and one `narration:` line. The narration is spoken while the app
holds on the state produced by that beat's actions.

```
url: http://localhost:8501
viewport: 1280x800
headless: false

### Beat 1 — Intro
narration: Welcome back, let's run the app we just built...

### Beat 2 — Pick a task
do: select | label=Choose Prompt Type | value=Email Writing
narration: In the sidebar I'll choose Email Writing...

### Beat 3 — Compare
do: click | button=Compare AI Responses
do: wait_for | text=Response from Strong Prompt
narration: I hit Compare and both answers come back side by side...
```

### Actions (`do:`)

| verb        | params                                  | what it does |
|-------------|-----------------------------------------|--------------|
| `goto`      | `url=`                                  | navigate |
| `click`     | `button=` / `text=` / `selector=`       | click an element |
| `fill`      | `label=` / `placeholder=`, `value=`     | type into a field |
| `select`    | `label=`, `value=`                      | open a Streamlit dropdown and pick an option |
| `wait_for`  | `text=` / `selector=`                   | wait until it appears (up to 2 min) |
| `wait`      | `seconds=`                              | fixed pause |
| `press`     | `key=`                                  | keyboard key |
| `scroll`    | `y=`                                    | scroll by pixels |

Selectors are semantic (by visible text / label / role). Streamlit's DOM is
quirky, so if an action can't find its target, adjust the selector — the runner
prints a `[warn]` for any action that fails so you can see which one.

## How sync works

1. Narration for every beat is generated up front, so each clip's length is known.
2. While Playwright records, after each beat's actions settle the runner notes the
   real time offset and **holds for that clip's length** before moving on.
3. Those measured offsets are used to place each narration clip onto the recorded
   video, then audio + video are muxed. Because the picture waits for the voice,
   they stay aligned even when a model response takes a variable few seconds.

## Authoring demo scripts for Day 3–7

The same idea as Lab Studio's authoring prompt: describe the app's features and
let an LLM draft the beats (actions + narration), then you fix the selectors.
`demo_recording_guide.md` (in the lab_studio folder) is a good starting outline.
