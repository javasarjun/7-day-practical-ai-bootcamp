# Run Saved Prompts from the Library

### Step 1 — Showing what's in the library
**File:** app.py
**Lang:** python
**StartLine:** 267

```python
library = load_prompt_library()

if library:
    for index, item in enumerate(library, start=1):
        with st.expander(f"{index}. {item['name']} — {item['task_type']}"):
            st.caption(f"Created at: {item.get('created_at', 'N/A')}")
            st.code(item["prompt"], language="text")
else:
    st.info("No prompts saved yet.")
```

**Walkthrough:**
@ "library = load_prompt_library()"
A library you cannot see into is not really a library, it is a black box. So the first thing we do is load everything back from the file, reusing that exact same load function we wrote last lecture. And notice, we are not rewriting that logic, we wrote it once, we trust it, we just call it again. That is the whole payoff of building small, focused functions, you get to keep cashing in on them.

@ "for index, item in enumerate(library, start=1):"
Then we loop through them. We are using enumerate here, which is a little nicer than a plain for loop, it hands you both the item and a running count at the same time. And start equals one is a small human touch, it numbers them one, two, three instead of zero, one, two, because we are showing this to a person, not a machine.

@ "with st.expander("
For each prompt we use an expander. Think of it as a collapsible drawer, the user sees just the name and the task type, and only opens the ones they actually care about. Some of these prompts run forty lines long, you really do not want all of them dumped on the screen at once. This keeps the page calm and easy to scan.

@ st.code(item["prompt"]
Open one up and we show when it was created and the full prompt text. And that is our reader done, the user can now browse their whole collection at a glance. But browsing is only half the feature. A library you can only look at is a scrapbook. The real magic is running these prompts again, so let us build that next.

### Step 2 — Choosing a prompt to run
**File:** app.py
**Lang:** python
**StartLine:** 287

```python
prompt_options = [
    f"{index + 1}. {item['name']} — {item['task_type']}"
    for index, item in enumerate(library)
]

selected_prompt_label = st.selectbox(
    "Choose a saved prompt",
    prompt_options,
)

selected_index = prompt_options.index(selected_prompt_label)
selected_prompt = library[selected_index]["prompt"]
```

**Walkthrough:**
@ "prompt_options = ["
So let us let them actually pick one to run. First we build a list of clean labels, one readable line per saved prompt, with this list comprehension. If comprehensions still feel like magic, just read it right to left, for each item in the library, make this nice label string. It is a compact way to turn raw data into the text we will show on screen.

@ "selected_prompt_label = st.selectbox("
We drop those labels into a dropdown. But here is the catch a lot of beginners trip over, the dropdown does not hand you back the prompt object, it hands you back the label, just the text the user clicked. So now we are holding a string like, two, professional email writer, and what we really need is the actual prompt sitting behind it.

@ "selected_index = prompt_options.index(selected_prompt_label)"
So we ask the options list, hey, what position is this label in? And that gives us an index, just a number, like position two.

@ selected_prompt = library[selected_index]
And we use that same index to reach into the library and grab the real prompt object. This little two-step, label to index to data, is a pattern you will use constantly, with dropdowns, with search results, with any list where the thing on screen and the thing in memory are not the same object. Get comfortable with it, it shows up everywhere.

### Step 3 — Filling in the placeholder and running it
**File:** app.py
**Lang:** python
**StartLine:** 303

```python
saved_prompt_input = st.text_area(
    "Enter input for this saved prompt",
    height=180,
)

if st.button("Run Saved Prompt"):
    final_prompt = selected_prompt.replace(
        "{user_input}",
        saved_prompt_input.strip(),
    )

    messages = [
        {"role": "system", "content": "You are a helpful, reliable, and practical AI assistant."},
        {"role": "user", "content": final_prompt},
    ]

    response = ask_ai(messages)
    st.markdown(response)
```

**Walkthrough:**
@ "saved_prompt_input = st.text_area("
Remember, the prompt we saved has a placeholder sitting where the real input used to be. So we give the user a fresh box to type whatever they want to run it on this time. The template is the reusable shell, and this is the new filling that goes inside it.

@ final_prompt = selected_prompt.replace
On run, we do the exact reverse of what we did when saving. Back then we swapped the real input out for the placeholder, now we swap the placeholder back out for the new input. So a saved template that reads, explain the placeholder to a beginner, becomes, explain Python dictionaries to a beginner. Same proven structure, brand new topic. That little round trip, real text to placeholder when you save, placeholder back to real text when you run, that is the entire reusable-template idea, captured in two lines.

@ "messages = ["
We wrap that final prompt in our familiar messages structure, a system message and a user message, same as always.

@ "response = ask_ai(messages)"
And we send it through ask ai, the very same service we built back in Day 1. Notice we are not writing one line of new model code here, we just lean on what is already solid. The answer comes back, we show it, and that closes the full loop of the entire day. Create a prompt, test it, save it as a template, and reuse it on demand. That right there, that loop, is the difference between just chatting with an AI and actually building a tool around it.
