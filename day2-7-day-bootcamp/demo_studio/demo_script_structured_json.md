# Demo — Structured JSON Output
url: http://localhost:8501
viewport: 1280x800
headless: false

### Beat 1 — Intro
narration: Here is the task that really shows why prompt engineering matters for real applications, getting the model to return clean, structured data that another program can actually use.

### Beat 2 — Choose Structured JSON Output
do: select | label=Choose Prompt Type | value=Structured JSON Output
narration: I'll pick Structured JSON Output as our task type.

### Beat 3 — Paste some messy notes
do: fill | textbox=Enter your text, topic, or | value=Meeting notes: We discussed launching the AI resume analyzer next Friday. Arjun will handle the Streamlit UI. Priya will test the resume scoring prompt. The team is positive but concerned about API cost.
narration: And I'll paste in some messy, free-form meeting notes, the kind of thing a human jots down quickly.

### Beat 4 — Weak vs strong prompt
narration: Now look at the strong prompt on the right. It does not just ask for JSON, it demands it. Return only valid JSON, no markdown, no explanation, and if a field is missing use an empty string. It even shows the exact shape it wants. That strictness is what makes the output safe to feed into code.

### Beat 5 — Generate the responses
do: click | button=Compare AI Responses
do: wait_for | text=Response from Strong Prompt
narration: Let's compare. Same notes, sent through both prompts.

### Beat 6 — The difference
narration: And this is the one that really lands. The weak prompt gives us a chatty, human-friendly answer, lovely to read, useless to a program. The strong prompt gives us clean, valid JSON, a title, a summary, the main points, action items, and a sentiment field. That is the difference between an AI that talks and an AI you can actually build software on top of.
