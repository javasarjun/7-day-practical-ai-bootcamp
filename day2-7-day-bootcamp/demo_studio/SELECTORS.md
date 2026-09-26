# Recording selectors with Playwright codegen → demo-script `do:` lines

You don't guess selectors. You record them once by clicking through the running
app, then translate what codegen prints into the demo-script format.

## 1. Start the app

In one terminal:
```bash
streamlit run app.py     # (and Ollama running, if the app uses it)
```

## 2. Record

In another terminal (or double-click `record.command`):
```bash
./.venv/bin/python demo_runner.py --codegen --url http://localhost:8501
```
Two windows open: your app, and the **Playwright Inspector**. Click, type, and
select through the exact flow you want to demo. For every action, the Inspector
writes a line of Python — e.g.:

```python
page.get_by_role("button", name="Compare AI Responses").click()
page.get_by_label("Enter your text, topic, or request:").fill("Write an email…")
page.get_by_role("combobox").filter(has_text="Choose Prompt Type").click()
page.get_by_role("option", name="Email Writing").click()
```

Copy those lines somewhere — they're your ground-truth selectors.

## 3. Curate first

Codegen records **everything**, including every stray arrow key and double-click.
Before translating, delete the noise — keep only the actions that actually drive
the demo. A 60-line recording usually boils down to 6–8 real steps.

## 4. Translate to `do:` lines

Map each *meaningful* recorded line to the demo-script syntax:

| Playwright codegen line | demo-script `do:` line |
|---|---|
| `get_by_role("button", name="X").click()` | `do: click \| button=X` |
| `get_by_role("textbox", name="X").fill("Y")` | `do: fill \| textbox=X \| value=Y` |
| `get_by_test_id("stBaseButton-primary").click()` | `do: click \| testid=stBaseButton-primary` |
| `get_by_label("X").fill("Y")` | `do: fill \| label=X \| value=Y` |
| `get_by_placeholder("X").fill("Y")` | `do: fill \| placeholder=X \| value=Y` |
| selectbox (a `div.filter(...).click()` then `get_by_text("Y").click()`) | `do: select \| label=<the label> \| value=Y` |
| `get_by_text("X").click()` | `do: click \| text=X` |
| waiting for a result to appear | `do: wait_for \| text=X` |

## 5. Streamlit gotchas (learned the hard way)

- **Selectbox is not a `<select>`.** Codegen records it as a `div` click to open
  plus a `get_by_text("Option").click()`. Don't copy that — just use one line:
  `do: select | label=Choose Prompt Type | value=Email Writing`. The runner finds
  the selectbox by its **label** and clicks the option for you.
- **Text inputs come through as `textbox` with a TRUNCATED name** — e.g. codegen
  prints `name="Enter your text, topic, or"` (cut off). Use that exact truncated
  string: `do: fill | textbox=Enter your text, topic, or | value=...`.
- **Primary/secondary buttons** often record as `get_by_test_id("stBaseButton-primary")`
  (Compare) and `...-secondary` (Save). The button's visible name usually also
  works (`button=Compare AI Responses`) and is more readable — prefer it.
- **NEVER keep an `st-emotion-cache-...` selector.** Those classes are generated
  and change between Streamlit versions, so the line will silently break. If
  codegen only gave you one of those for an element (e.g. clicking a saved item),
  find a stable handle instead: its visible text, a nearby label, or skip it (a
  freshly-saved prompt is already selected by default).
- After an action that triggers a model call (Compare / Run Saved Prompt), add a
  `do: wait_for | text=...` on something that only appears once the response is in,
  so the recording holds until the result is on screen.
- If a `do:` line can't find its target at run time, the runner prints a `[warn]`
  naming that action — re-record just that one and fix it.

See `demo_script_save_and_run.md` for a real recording cleaned into a working
scenario.

## 4. Add narration and run

Wrap the `do:` lines into beats with a `narration:` line each (see
`demo_script_day2.md`), then:
```bash
./.venv/bin/python demo_runner.py demo_script_day2.md
```

That's the whole loop: **record selectors once → paste into beats → add narration
→ render.** For a new scenario, you only re-record the parts that changed.
