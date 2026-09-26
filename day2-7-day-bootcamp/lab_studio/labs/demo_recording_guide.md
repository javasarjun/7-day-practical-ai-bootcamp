# Day 2 Demo — Recording Guide

This is the **live run** you record yourself, after the six code-walkthrough
labs. The labs build the app; this is where you switch it on and show it working.

## Before you hit record

1. Make sure Ollama is running and the model is pulled:
   ```bash
   ollama run llama3.2:3b
   ```
   (Or set `LLM_PROVIDER=openai` in `.env` if you want to demo with OpenAI.)
2. Start with an **empty** `prompt_library.json` containing just `[]`, so the
   audience watches the first prompt get saved live.
3. Launch the app:
   ```bash
   streamlit run app.py
   ```
4. Have your editor open in a second window so you can flip to
   `prompt_library.json` and show it change after a save.

## Demo flow (suggested order)

### 1. Weak vs strong — the core "aha"
- Sidebar → **Email Writing**.
- Paste the email test input (below).
- Point out the **weak** and **strong** prompts side by side.
- Click **Compare AI Responses**.
- Talk through it: same model, only the instructions changed. Note the strong
  side has a subject line, a professional tone, structure, and no invented facts.

### 2. Show a second task type
- Switch to **Structured JSON Output**, paste the meeting-notes input.
- Run it. Show that the strong side returns clean, valid JSON — the kind of
  output you could feed straight into another program.

### 3. Save a reusable template
- Go back to a strong prompt you like (e.g. Coding Help).
- Name it `Beginner-Friendly Concept Explainer`, click **Save Prompt**.
- Flip to `prompt_library.json` in your editor — show the new object on disk.
- Point out the `{user_input}` placeholder that replaced your real text.

### 4. Run the saved prompt with new input
- Scroll to **Use a Saved Prompt**, select the one you just saved.
- Enter new input: `Python dictionaries`.
- Click **Run Saved Prompt**.
- Show the **Final Prompt Sent to AI** — highlight how `{user_input}` got
  swapped for the new text — then the response.
- Land the closing line: create → test → save → reuse.

## Test inputs (copy/paste ready)

**Email Writing**
```
Write an email to my manager asking for an extension on the project deadline because we found unexpected bugs during testing.
```

**Summarization**
```
Artificial intelligence is being used across industries to automate repetitive tasks, improve decision-making, personalize customer experiences, and generate content. However, companies must also consider privacy, bias, security, and accuracy when adopting AI tools.
```

**Coding Help**
```
Explain Python functions to a beginner with an example.
```

**Structured JSON Output**
```
Meeting notes: We discussed launching the AI resume analyzer next Friday. Arjun will handle the Streamlit UI. Priya will test the resume scoring prompt. The team is positive but concerned about API cost.
```

**Saved-prompt new input**
```
Python dictionaries
```

## If you automate this later (separate project)

The natural way to automate this demo is a scripted browser run (Playwright or
Selenium) that drives the Streamlit UI — selects task types, types the inputs,
clicks the buttons, and screen-records the result — so you can re-shoot the demo
on every code change without doing it by hand. Worth its own project, not part
of Lab Studio.
