# Demo — Save and Reuse a Prompt
url: http://localhost:8501
viewport: 1280x800
headless: false

# Cleaned from a Playwright codegen recording: the dozens of arrow-key presses
# and the st-emotion-cache selectors were dropped; only the meaningful, stable
# actions remain. Note how selectbox uses `select`, inputs use `textbox=` (with
# the truncated accessible name codegen showed), and buttons use their names.

### Beat 1 — Intro
narration: We have already built the prompt library. Now let's see the part that makes it genuinely useful, saving a prompt once and reusing it later with brand new input.

### Beat 2 — Pick a task
do: select | label=Choose Prompt Type | value=Email Writing
narration: I'll pick Email Writing, so the app builds a strong email prompt for us.

### Beat 3 — Enter a request
do: fill | textbox=Enter your text, topic, or | value=Write an email to my manager for taking a two day leave.
narration: Then I'll type a real request, an email to my manager asking for two days of leave.

### Beat 4 — The reusable template
narration: Down in the save section, notice the Prompt to Save box is already filled in for us. The app has taken our strong prompt and swapped our exact request for the placeholder, open brace user input close brace. That is what turns it into a reusable template.

### Beat 5 — Name and save it
do: fill | textbox=Prompt Name | value=Professional Email Writer
do: click | button=Save Prompt
narration: I'll give it a name, Professional Email Writer, and hit Save. Behind the scenes, that prompt is now appended as a new entry inside prompt library dot json on disk.

### Beat 6 — Reuse it with new input
do: fill | textbox=Enter input for this saved | value=Write an email asking for one day of sick leave.
narration: Now, down in the Use a Saved Prompt section, our template is already selected. I'll give it a completely different request, this time a one-day sick leave email.

### Beat 7 — Run the saved prompt
do: click | button=Run Saved Prompt
do: wait_for | text=AI Response
narration: And I hit Run. The app drops my new input into the saved template where the placeholder was, sends it to the model, and out comes a fresh email, same proven structure, brand new content. That is the whole create, save, reuse loop working end to end.
