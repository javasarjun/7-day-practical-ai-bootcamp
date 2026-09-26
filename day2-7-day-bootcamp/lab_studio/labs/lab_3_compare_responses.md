# Compare Weak and Strong Prompt Responses

### Step 1 — The compare button and a guard
**File:** app.py
**Lang:** python
**StartLine:** 177

```python
run_button = st.button("Compare AI Responses", type="primary")

if run_button:
    if not user_input:
        st.warning("Please enter some input first.")
    else:
```

**Walkthrough:**
@ "run_button = st.button("Compare AI Responses", type="primary")"
Okay, this is the moment everything has been building toward. We have our weak prompt and our strong prompt on screen, now we add a button to actually send them to the model and compare the answers. St dot button draws the button, and it returns True on the exact run where it gets clicked, which we capture in run button. That type equals primary just makes it the bold, colored button, a small visual cue telling the user, this is the main action on the page.

@ "if run_button:"
Everything inside this if only fires on the click. And notice the very first thing we do, before any expensive model call, is check that the user actually typed something. If the input is empty, we show a friendly warning and stop right there. Validate before you do real work, it is cheaper and kinder than letting an empty request travel all the way to the model and come back with nonsense. Guard clauses like this are a habit that will save you constantly.

### Step 2 — Packaging the prompts as messages
**File:** app.py
**Lang:** python
**StartLine:** 183

```python
        weak_messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant.",
            },
            {
                "role": "user",
                "content": weak_prompt,
            },
        ]

        strong_messages = [
            {
                "role": "system",
                "content": "You are a helpful, reliable, and practical AI assistant.",
            },
            {
                "role": "user",
                "content": strong_prompt,
            },
        ]
```

**Walkthrough:**
@ "weak_messages = ["
Now we package the weak prompt into the shape the model expects, a list of messages. And here is where I want to reconnect to Day 1. Remember the ask ai service we built back then, the one that takes a list of messages and quietly talks to Ollama or OpenAI for us? This is that exact format. We are not writing any new model code today, we are just preparing the input for a service we already trust.

@ "You are a helpful AI assistant."
Each message has two parts, a role and content. The system message sets the assistant's overall behavior, think of it as the standing instructions it always keeps in mind. The user message carries the specific request, here, our weak prompt. A simple way to hold it in your head, system is who the assistant is, user is what we are asking it right now.

@ "strong_messages = ["
Then we build the very same structure for the strong prompt. Identical shape, the only real difference is the prompt tucked inside, and you will notice the system message is a touch richer here too. The whole experiment depends on this being a fair fight, same model, same message format, we change exactly one thing, the quality of the prompt, and then we watch what happens.

### Step 3 — Calling the service and showing both answers
**File:** app.py
**Lang:** python
**StartLine:** 205

```python
        response_col1, response_col2 = st.columns(2)

        with response_col1:
            st.subheader("Response from Weak Prompt")

            with st.spinner("Generating weak prompt response..."):
                weak_response = ask_ai(weak_messages)
                st.markdown(weak_response)

        with response_col2:
            st.subheader("Response from Strong Prompt")

            with st.spinner("Generating strong prompt response..."):
                strong_response = ask_ai(strong_messages)
                st.markdown(strong_response)
```

**Walkthrough:**
@ "response_col1, response_col2 = st.columns(2)"
We split the screen into two columns so both answers sit right next to each other. Putting them shoulder to shoulder is what makes the difference impossible to miss.

@ "with st.spinner("Generating weak prompt response..."):"
Before the call, a small but genuinely lovely touch, st dot spinner. Talking to a model takes a few seconds, and a frozen screen makes people think the app broke. The spinner shows a little loading message while we wait. Always give the user feedback during anything slow, it is the difference between an app that feels responsive and one that feels broken.

@ "weak_response = ask_ai(weak_messages)"
And here is the actual call, ask ai with the weak messages. This is the Day 1 service doing all the heavy lifting for us, picking the provider, making the HTTP request, handling errors, pulling out the text. From up here in the UI, all of that collapses into one clean line. We take what it hands back and render it with markdown.

@ "strong_response = ask_ai(strong_messages)"
Same call in the right column, this time with the strong messages. And that is the entire comparison fully wired up. Here is the one idea I really want you to hold onto, the model is identical for both of these calls. When you run this, the weak side comes back vague and loosely formatted, while the strong side comes back structured, on format, and actually grounded in what you asked for. Same model, the only thing that changed was how clearly we gave the instructions. That contrast, sitting side by side, is the whole point of this lab, it turns the value of a good prompt into something you can see with your own eyes.
