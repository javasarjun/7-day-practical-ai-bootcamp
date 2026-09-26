# Save Prompts to a Prompt Library

### Step 1 — Turning a prompt into a reusable template
**File:** app.py
**Lang:** python
**StartLine:** 130

```python
if user_input:
    weak_prompt = build_weak_prompt(task_type, user_input)
    strong_prompt = build_strong_prompt(task_type, user_input)

    strong_prompt += f"\n\nStyle instruction: {style_instruction}"

    # Convert the generated prompt into a reusable template.
    # Instead of saving the exact input, we replace it with a placeholder.
    reusable_prompt = strong_prompt.replace(user_input, "{user_input}")
```

**Walkthrough:**
@ "if user_input:"
Our strong prompt is genuinely good now, but it has one sneaky flaw that blocks reuse, it has the user's exact input baked right into it. Save it like that and it is a one-hit wonder, it only ever works for that one article, that one email. What we actually want is a template, something we can fill in again and again. So before we touch any files, let us fix that.

@ reusable_prompt = strong_prompt.replace
Here is the move, and it is almost embarrassingly simple. We take the finished strong prompt and call replace on it. We find the user's original input sitting inside the prompt and swap it out for a placeholder, open brace, user input, close brace. So a prompt that literally said, summarize this article about renewable energy, becomes a template that says, summarize, then the placeholder. It is like turning a handwritten letter into a fill-in-the-blanks form. That one line is what turns a single-use prompt into something reusable, and it is the whole idea behind a prompt library.

### Step 2 — Loading the library safely
**File:** app.py
**Lang:** python
**StartLine:** 32

```python
def load_prompt_library():
    if not os.path.exists(PROMPT_LIBRARY_FILE):
        return []

    try:
        with open(PROMPT_LIBRARY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []
```

**Walkthrough:**
@ load_prompt_library
Now we need a place to keep these templates, and we will use a simple JSON file on disk, no database, nothing fancy. This function, load prompt library, reads that file back into Python. And I want you to notice how paranoid it is, because reading a file from disk can go wrong in more ways than beginners expect, and a good engineer plans for every one of them.

@ "if not os.path.exists(PROMPT_LIBRARY_FILE):"
First line of defense, does the file even exist? The very first time anyone runs this app, there is no library yet. Instead of letting that explode, we just return an empty list and carry on. Your app should work perfectly on day one, with zero saved prompts.

@ return json.load(file)
If the file is there, we open it and let json dot load turn that text on disk back into real Python data, a list of prompt dictionaries, and hand it back. This is the happy path, the normal everyday case.

@ "except json.JSONDecodeError:"
And here is the safety net I really want you to internalize. Picture a user opening that JSON file by hand, fat-fingering it, deleting a bracket, and saving. Now it is not valid JSON anymore. Json dot load would throw an error and crash your whole app. So we wrap it in a try, catch that exact error, and fall back to an empty list. One corrupted file should never take down the entire application. This kind of defensive thinking is what separates a toy from something you would actually ship.

### Step 3 — Saving a new prompt
**File:** app.py
**Lang:** python
**StartLine:** 43

```python
def save_prompt_to_library(name, task_type, prompt):
    library = load_prompt_library()

    library.append(
        {
            "name": name,
            "task_type": task_type,
            "prompt": prompt,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )

    with open(PROMPT_LIBRARY_FILE, "w", encoding="utf-8") as file:
        json.dump(library, file, indent=2)
```

**Walkthrough:**
@ save_prompt_to_library
This function is the mirror image, it saves a new prompt into the library. The name, the task type, and the prompt text all come in as parameters.

@ "library = load_prompt_library()"
Stop on this very first line, because this is the one beginners get wrong and then file a very confused bug report about. Before we add anything, we load what is already there. Now picture the alternative. If you skipped this and just wrote out a fresh list with your one new prompt in it, you would silently wipe out every prompt the user had saved before. This is the classic read, then modify, then write pattern. Load first, every time, or your save button quietly becomes a delete-everything button.

@ "library.append("
With the existing list safely in hand, we append a new dictionary, the name, the task type, and the prompt itself.

@ created_at
We also stamp it with the current date and time. Tiny detail, real payoff, once a user has thirty saved prompts, being able to tell which one is newest is genuinely useful. A timestamp costs you almost nothing to add right now, and you will be glad it is there later.

@ json.dump(library
Then we open the file in write mode, and json dot dump writes the whole updated list back out. That indent equals two is a small kindness, it pretty-prints the JSON, so when you open the file to peek inside, it reads as a clean, indented list instead of one giant unreadable line.

### Step 4 — The save prompt interface
**File:** app.py
**Lang:** python
**StartLine:** 234

```python
prompt_name = st.text_input(
    "Prompt Name",
)

prompt_to_save = st.text_area(
    "Prompt to Save",
    value=reusable_prompt,
    height=320,
)

if st.button("Save Prompt"):
    if not prompt_to_save.strip():
        st.warning("Please enter or generate a prompt before saving.")
    elif not prompt_name.strip():
        st.warning("Please enter a prompt name.")
    else:
        save_prompt_to_library(
            prompt_name.strip(),
            task_type,
            prompt_to_save.strip(),
        )
        st.success("Prompt saved to prompt_library.json")
```

**Walkthrough:**
@ "prompt_name = st.text_input("
Now the front end, the part the user actually touches. First a text box for the prompt's name, so they can recognize it later in the list. Naming things well is honestly half the battle in any kind of library.

@ "prompt_to_save = st.text_area("
Then a bigger text area, and notice it comes pre-filled with the reusable template we generated earlier. But here is a deliberate decision, we leave it editable. The user can tweak the wording before they commit it. Always give people a chance to review before you write to disk, it builds trust in your app.

@ "if not prompt_to_save.strip():"
On click, we validate before we save. Strip quietly trims the spaces off both ends, which catches that sneaky case where the box looks empty but actually holds a few stray spaces, the kind of thing that would slip right past a naive is-it-empty check. We also make sure they actually gave it a name. Cheap guardrails up front, far less junk in your library later.

@ save_prompt_to_library(
If both checks pass, we call save prompt to library with the cleaned-up values, and show a success message. And here is the satisfying part, the instant you click save, your new prompt is appended as a fresh entry inside prompt library dot json, right there on disk. Open that file and you can see exactly what got written. That is what makes persistence feel real, your prompt is saved now, and it will still be there the next time you open the app.
