# Day 2 Wrap-Up and Student Challenge

# NOTE: This is a summary lecture, not a code walkthrough. It uses plain-text
# "boards" instead of source files. If you'd rather present it with slides,
# it also works well in Narration Studio.

### Step 1 — The mental model
**File:** day2_mental_model.txt
**Lang:** text

```text
HOW THE PIECES FIT TOGETHER

prompt_templates.py   ->  Creates the instructions
                          (weak, strong, role, reasoning summary)

llm_service.py        ->  Sends those instructions to the model
                          (ask_ai picks Ollama or OpenAI)

app.py                ->  Connects user actions to prompts and the model
                          (the Streamlit UI and the workflow)

prompt_library.json   ->  Stores reusable prompt templates
                          (saved, loaded, and run again later)
```

**Walkthrough:**
@ HOW THE PIECES
Take a breath, we covered a lot today. Let us zoom all the way out and look at what we actually built, because honestly it is more impressive than it felt while we were heads down in the code. We did not write one giant tangled file. We built four small pieces, and every single one of them has exactly one job. That, by the way, is how real software is structured, small parts that each do one thing well.

@ prompt_templates.py
Piece one, prompt templates. This is our writer. It builds the weak prompts, the strong ones, the role prompts, the reasoning summaries. And remember its superpower, it only ever works with text, it never touches a model. That tight focus is exactly why it was so easy to reason about.

@ llm_service.py
Piece two, the LLM service. This is our messenger. It takes those instructions and carries them to the model. And ask ai, our little front door, hides whether we are on Ollama or OpenAI, so nobody upstream ever has to think about it. One job, done cleanly.

@ app.py
Piece three, app dot py. This is the conductor. Yes, it draws the Streamlit interface, but please do not file it away as just a frontend, it is the part that orchestrates everything, wiring what the user clicks to the right prompt and the right model call. It is the glue that makes the other three feel like one single app.

@ prompt_library.json
And piece four, the prompt library, our memory. It is just a plain JSON file, but it is what lets a great prompt outlive a single session, save it once, reuse it forever. Four files, four responsibilities. Keep your projects shaped like this, and they stay easy to grow instead of turning into spaghetti.

### Step 2 — Your challenges
**File:** day2_challenges.txt
**Lang:** text

```text
KEEP BUILDING

Beginner
    Add a new prompt type: "Interview Preparation"
    It should generate questions, sample answers, and tips.

Intermediate
    Add a prompt quality checklist:
    Does the prompt have a role? a clear task? rules?
    an output format? Does it avoid vague wording?

Advanced
    Add prompt versioning to saved templates
    (store a "version" number alongside each prompt).
```

**Walkthrough:**
@ KEEP BUILDING
Now, the best way to lock all of this in is to go build something with it yourself. So here are three challenges, stacked by difficulty. Find the one that feels just slightly uncomfortable for you, that little stretch is exactly where the learning happens.

@ Beginner
If you are still finding your feet, add a brand new prompt type, interview preparation. It should produce common interview questions, sample answers, and a few tips. And here is why this is the perfect first challenge, you already know the pattern from build strong prompt. You are not learning something new, you are proving to yourself that you genuinely understood it. That is a great feeling, chase it.

@ Intermediate
Want a real stretch? Build a prompt quality checklist right into the app. Have it inspect a prompt and ask, does this have a role? a clear task? rules? an output format? and then warn the user if something is missing. You would basically be turning everything we learned today into a little tool that coaches the next person. It is a fun, slightly meta project.

@ Advanced
And if you are hungry for the real thing, add versioning to your saved prompts. Each template carries a version number, and when you improve it, you bump the version instead of overwriting the old one. Now you can actually see how a prompt evolved over time. That is a genuinely professional feature, the kind of thing you would find in a real product, and it will teach you a lot about handling data that changes.

### Step 3 — The one idea to remember
**File:** day2_takeaway.txt
**Lang:** text

```text
THE KEY TAKEAWAY

The model did not change between our weak prompt
and our strong prompt.

The response improved because the instructions
became clearer, more specific, and more structured.

Better prompts, better software.
```

**Walkthrough:**
@ THE KEY TAKEAWAY
Okay, last thing, and then I will let you go. If everything else from today fades and you remember just one sentence, make it this one.

@ The model did not change
The model never changed. Not once. The exact same model answered our weak prompt and our strong prompt. So whatever got better between them, it was not the AI.

@ The response improved
What changed was us, the instruction. The output got sharper because we made it clearer, more specific, and more structured. That, right there, is the entire craft of prompt engineering in a nutshell, and it is the quiet skill that turns a fun chat toy into software you can actually ship. You did real engineering today, so be proud of it. Rest up, and I will see you in Day three.
